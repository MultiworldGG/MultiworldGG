from __future__ import annotations

import asyncio
import time

from CommonClient import logger

from ..core import TextColour, colored_text, reconcile_traps
from ..universal_tracker import PLANET_ID_TO_REGION
from ..core.address_maps import SUPPORTED_GAMES
from ..core.save_data import highest_weapon_levels
from .constants import PINE_CONNECT_SETTLE_DELAY_S, POLL_INTERVAL
from .other_ratchet_games import GAME_ID_TO_OTHER_RATCHET

_WEAPON_STATE_PUSH_INTERVAL: float = 5.0


class PineMixin:
    """Detect the supported region before driving Core and recheck every poll."""

    def _select_game_region(self, game_id: str) -> None:
        """Called under the PINE lock, before any initial reads or game ticks."""
        if self._wiring.select_game(game_id):
            self._weapon_state_restored = False
            self._ap_loadout_restored = False
            self._connection_sync_pending = True
            self._pending_item_apply = True
            self.current_planet = "Galaxy"
            logger.info(f"[RAC] Selected {SUPPORTED_GAMES[game_id]} addresses [{game_id}].")

    async def _teardown_pine_connection(self) -> None:
        """Drop the raw socket. Safe to call even if it's already down."""
        self.pine_connected = False
        try:
            self._wiring.native.close()
        except Exception:
            logger.debug("[RAC] Could not release native loader gate during teardown", exc_info=True)
        try:
            self.pine.disconnect()
        except Exception:
            logger.debug("[RAC] pine.disconnect() raised during teardown", exc_info=True)

    async def reconnect_pine(self) -> None:
        async with self._pine_lock:
            await self._teardown_pine_connection()
        await self._attempt_pine_connect(is_reconnect=True)

    async def _reject_wrong_game(self, game_id: str, *, is_disconnect: bool) -> None:
        known_game = GAME_ID_TO_OTHER_RATCHET.get(game_id)
        if is_disconnect:
            msg = (
                f"PCSX2 is now running {known_game or game_id} — Size Matters client disconnected. "
                "Use /reconnect once R&C: Size Matters is loaded again."
            )
            try:
                raise ConnectionError(msg)
            except ConnectionError:
                self.handle_connection_loss(f"[RAC] {msg}")
        elif known_game:
            logger.warning(
                f"[RAC] Wrong game in PCSX2: detected {known_game} [{game_id}]. This client is for "
                "Ratchet & Clank: Size Matters (US/EU/JP). Connection rejected."
            )
        else:
            logger.warning(f"[RAC] Unsupported game in PCSX2: {game_id!r} (supported: {', '.join(SUPPORTED_GAMES)}). "
                            "Connection rejected.")
        async with self._pine_lock:
            await self._teardown_pine_connection()

    async def _attempt_pine_connect(self, is_reconnect: bool = False) -> None:
        async with self._pine_lock:
            def _connect_and_get_game_id() -> str:
                self.pine.connect()
                return self.pine.get_game_id()
            try:
                game_id = _connect_and_get_game_id()
            except Exception:
                logger.warning("[RAC] Could not connect to PCSX2. Use /reconnect once the emulator is running.")
                await self._teardown_pine_connection()
                return

        if game_id not in SUPPORTED_GAMES:
            await self._reject_wrong_game(game_id, is_disconnect=False)
            return

        await asyncio.sleep(PINE_CONNECT_SETTLE_DELAY_S)

        # PCSX2 may have changed games during the settle delay.
        async with self._pine_lock:
            game_id = self.pine.get_game_id()
        if game_id not in SUPPORTED_GAMES:
            await self._reject_wrong_game(game_id, is_disconnect=False)
            return

        async with self._pine_lock:
            logger.info(
                f"[RAC] {'Reconnected' if is_reconnect else 'Connected'} to PCSX2 - "
                f"R&C: Size Matters {SUPPORTED_GAMES[game_id]} [{game_id}] detected."
            )
            self.pine_connected = True
            try:
                self._select_game_region(game_id)
                self._wiring.sync_from_ap(self._checked_location_names())
                self._connection_sync_pending = True
                self._wiring._ap_inventory_ready = False
                self._read_initial_state_sync()
                if not self._wiring.at_main_menu:
                    reconcile_traps(self.pine)
            except Exception as exc:
                logger.warning(
                    f"[RAC] Initial state read failed: {exc}. Use /reconnect once the game is fully loaded."
                )
                await self._teardown_pine_connection()
                return
            self._write_notification_text(colored_text(
                "Reconnected to " if is_reconnect else "Connected to ", TextColour.YELLOW,
                "PCSX2", TextColour.WHITE,
            ))

        try:
            self._notification_item_index = len(self.items_received)
            if is_reconnect:
                self._weapon_state_restored = False
            await self.force_sync()
            await self._send_map_page(self.current_planet)
        except Exception as exc:
            logger.warning(f"[RAC] Lost PCSX2 connection while starting up: {exc}. Use /reconnect.")
            async with self._pine_lock:
                await self._teardown_pine_connection()

    async def _read_initial_state(self) -> None:
        try:
            async with self._pine_lock:
                self._read_initial_state_sync()
        except Exception as exc:
            self._log(f"[RAC] Initial state read failed: {exc}", "warning")

    def _read_initial_state_sync(self) -> None:
        if self._items_received_ready and self._save_data_received:
            self._wiring.tick()
        planet_id = self._wiring.planet.planet_id
        self.current_planet = PLANET_ID_TO_REGION.get(planet_id, "Galaxy")

    async def game_watcher(self) -> None:
        try:
            while not self.exit_event.is_set():
                await asyncio.sleep(POLL_INTERVAL)
                if not self.pine_connected:
                    continue
                try:
                    await self._poll_game()
                except Exception as exc:
                    logger.warning(f"[RAC] Lost PINE connection or poll failed: {exc}")
                    try:
                        self._wiring.native.close()
                    except Exception:
                        logger.debug("[RAC] Could not release native loader gate after poll failure", exc_info=True)
                    self.pine_connected = False
        finally:
            try:
                self._wiring.native.close()
            except Exception:
                logger.debug("[RAC] Could not release native loader gate on shutdown", exc_info=True)

    async def _poll_game(self) -> None:
        async with self._pine_lock:
            game_id = self.pine.get_game_id()
            if game_id in SUPPORTED_GAMES:
                self._select_game_region(game_id)
        if game_id not in SUPPORTED_GAMES:
            await self._reject_wrong_game(game_id, is_disconnect=True)
            return

        if self._connection_sync_pending:
            await self.force_sync()
        prev_planet = self.current_planet
        async with self._pine_lock:
            self._wiring.native.ap_connected = bool(
                self.slot is not None and self.server and self.server.socket
                and not self.server.socket.closed)
            if self._items_received_ready and self._save_data_received:
                self._try_restore_weapon_state()
                self._wiring.tick()
            else:
                self._wiring.native.tick()
        self.current_planet = PLANET_ID_TO_REGION.get(self._wiring.planet.planet_id, "Galaxy")
        if self.current_planet != prev_planet:
            await self._send_map_page(self.current_planet)

        await self._apply_received_items()
        self._maybe_persist_weapon_state()
        self._maybe_sync_ammo_link()
        self._maybe_sync_bolt_link()
        self._maybe_sync_ghost_link()

    def _maybe_persist_weapon_state(self, *, force: bool = False) -> None:
        """Cache live levels and publish changes, never temporary vendor values."""
        if (self.slot is None or not self.pine_connected or not self._weapon_state_restored
                or not self._save_data_received or not self._items_received_ready
                or not self._wiring.planet.weapons_available or self._wiring.at_main_menu
                or self._wiring.vendor_active or self._wiring.native.waiting):
            return
        weapons = self._wiring.planet.weapons
        live = weapons.level_snapshot()
        snapshot = weapons.within_level_ceilings(highest_weapon_levels(self._local_weapon_state, live))
        dropped = {name: (live.get(name), level) for name, level in snapshot.items() if live.get(name) != level}
        if dropped:
            logger.warning(f"[RAC] Weapon levels dropped unexpectedly, keeping known levels: {dropped}")
            weapons.restore_levels(snapshot)
        self._local_weapon_state = snapshot
        now = time.monotonic()
        if not force and now - self._last_weapon_state_push < _WEAPON_STATE_PUSH_INTERVAL:
            return
        if snapshot == self._pushed_weapon_state:
            return
        self._last_weapon_state_push = now
        self._pushed_weapon_state = snapshot
        asyncio.create_task(self._persist_weapon_state(snapshot))

    async def _send_map_page(self, planet: str) -> None:
        if self.slot is None:
            return
        team = getattr(self, "team", 0)
        await self.send_msgs([{
            "cmd": "Set",
            "key": f"rsm_current_planet_{self.slot}_{team}",
            "default": "Galaxy",
            "want_reply": False,
            "operations": [{"operation": "replace", "value": planet}],
        }])

    def _append_location_by_name(self, name: str) -> None:
        """Wired as Core.wire(send_location=...). Silently no-ops for a name outside the location
        table, already checked, or excluded from this seed's pool (e.g. an option-gated location)."""
        loc_id = self._location_name_to_id.get(name)
        if loc_id is None:
            return
        if loc_id in self._locally_checked_locations or loc_id in self.checked_locations:
            return
        server_locations = getattr(self, "server_locations", None)
        if server_locations is not None and loc_id not in server_locations:
            return
        self._locally_checked_locations.add(loc_id)
        self._log(f"[RAC] Location checked: {name}")
        self._wiring.planet.weapons.sync_from_ap(self._checked_location_names())
        asyncio.create_task(self.check_locations({loc_id}))

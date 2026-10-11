from __future__ import annotations

import asyncio

from CommonClient import logger
from NetUtils import ClientStatus

from ..core import ARMOUR_SET_CHECKS
from ..core import address_maps
from ..core.address_maps import PLAYER_BOLT_COUNT
from ..core.player_bolts import MAX_PLAYER_BOLTS


class ChallengeHandlerMixin:
    def _on_challenge_armour_earned(self, loc_name: str) -> None:
        """Fired when a new armour piece is detected after a challenge completes."""
        self._pending_challenge_checks.append(loc_name)



class CutsceneHandlerMixin:
    async def _send_goal_status(self) -> None:
        if not self.finished_game:
            await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
            self.finished_game = True



class EventsHandlerMixin:
    async def _send_playing_status(self) -> None:
        """Tell the server we're in-game, not sitting at the main menu.
        Fired from Core's on_initial_load hook, when a save has just loaded."""
        await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_PLAYING}])

    def _on_planet_ready(self) -> None:
        """Reapply AP inventory and saved levels after the planet array is reset."""
        if self._save_data_received and not self._ap_loadout_restored:
            saved = self._stored_save_data()
            if saved.quick_select:
                self._wiring.quick_select.load(saved.quick_select)
                self._wiring.quick_select.restore()
            if saved.armour_slots:
                self._wiring.armour.sync_equipped(saved.armour_slots)
            self._ap_loadout_restored = True
        asyncio.create_task(self._apply_received_items())
        asyncio.create_task(self._grant_starting_items())
        self._try_restore_weapon_state(force=True)

    def _on_weapon_level_up(self) -> None:
        """Persist an organic level-up immediately."""
        self._maybe_persist_weapon_state(force=True)

    async def _grant_starting_items(self) -> None:
        if self._starting_items_sent or not self.pine_connected:
            return
        self._starting_items_sent = True
        starting_bolts = int(self.slot_data.get("starting_bolts", 0))
        if starting_bolts <= 0:
            asyncio.create_task(self._persist_starting_items_sent())
            return
        async with self._pine_lock:
            try:
                current = self.pine.read_int32(address_maps.PLAYER_BOLT_COUNT)
                granted = min(current + starting_bolts, MAX_PLAYER_BOLTS)
                self.pine.write_int32(address_maps.PLAYER_BOLT_COUNT, granted)
                self._wiring.player_bolts.rebaseline(granted)
            except Exception as exc:
                logger.warning(f"[RAC] Could not grant starting bolts: {exc}")
                self.pine_connected = False
                self._starting_items_sent = False
                return
        asyncio.create_task(self._persist_starting_items_sent())

    def _on_vendor_close(self) -> None:
        """Apply deliveries deferred while browsing; weapon views keep real inventory."""
        self._on_menu_close_for_armour_sets()
        asyncio.create_task(self._apply_received_items())

    def _on_equipped_armour_saved(self, data: dict) -> None:
        """Fired when the pause/equip menu closes — the actual moment
        equipped armour can change, unlike vendor close."""
        self._on_menu_close_for_armour_sets()
        asyncio.create_task(self._persist_armour_slots(data))

    def _on_menu_close_for_armour_sets(self) -> None:
        if not self._armour_set_checks_enabled:
            return
        equipped = self._wiring.armour.read()
        for name, check in ARMOUR_SET_CHECKS.items():
            if check.matches(equipped):
                self._append_location_by_name(name)

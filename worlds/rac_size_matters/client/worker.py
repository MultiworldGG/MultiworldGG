"""PCSX2 worker process: owns PINE, Core and every game-memory read/write.

The client process mirrors AP state in (see protocol.py) and executes whatever this
worker asks of the server, so the GUI keeps running while PCSX2 is slow or stalled.
"""

import asyncio
import logging
import threading
from collections.abc import Callable
from dataclasses import replace
from typing import Any

from CommonClient import logger

from ..constants import Rac5CutsceneLocations
from ..constants.options import Rac5Options
from ..core import RAC5SaveData, TextColour, address_maps, colored_text, set_trap_durations, vendor_presentation
from ..core.core import Core
from ..core.notifications import sent_text
from ..core.options import ClientOptions
from ..core.save_data import highest_weapon_levels
from ..core.skins import Skin
from ..locations import ALL_LOCATIONS
from ..pypine import Pine
from ..world import RACSizeMatterWorld
from . import protocol
from .ammo_link import AmmoLinkMixin
from .bolt_link import BoltLinkMixin
from .constants import GAME_NAME
from .deathlink import DeathLinkMixin
from .ghost_link import GhostLinkMixin
from .handlers import CutsceneHandlerMixin, EventsHandlerMixin
from .pine_mixin import PineMixin
from .vendor import InventoryMixin, VendorHandlerMixin
from .vendor_scouts import VendorScouts


class GameWorker(
    PineMixin,
    CutsceneHandlerMixin,
    EventsHandlerMixin,
    DeathLinkMixin,
    AmmoLinkMixin,
    BoltLinkMixin,
    GhostLinkMixin,
    VendorHandlerMixin,
    InventoryMixin,
):
    """Game half of the client; the mixins see AP state through the mirrors below."""

    game = GAME_NAME
    current_planet: str = "Galaxy"

    def __init__(self, post: Callable[[tuple], None]) -> None:
        self._post = post
        self.exit_event = asyncio.Event()

        # Mirrors of the client's CommonContext state.
        self.slot: int | None = None
        self.team: int = 0
        self.auth: str | None = None
        self.slot_data: dict[str, Any] = {}
        self.slot_info: dict[int, Any] = {}
        self.player_names: dict[int, str] = {}
        self.items_received: list = []
        self.item_names = {GAME_NAME: dict(RACSizeMatterWorld.item_id_to_name)}
        self.stored_data: dict[str, Any] = {}
        self.checked_locations: set[int] = set()
        self.server_locations: set[int] = set()
        self.finished_game = False
        self.ap_connected = False

        self.pine = Pine()
        self.pine_connected = False
        self._pine_lock = asyncio.Lock()

        self._location_name_to_id = {name: data.code for name, data in ALL_LOCATIONS.items()}
        self.vendor_scouts = VendorScouts(self._location_name_to_id)
        self._locally_checked_locations: set[int] = set()

        self._pending_armour_pickup_locs: list[str] = []
        self._processed_item_count = 0
        self._processed_trap_count = 0
        self._filler_checkpoint_synced = False
        self._ap_loadout_restored = False
        self._starting_items_sent = False
        self._death_count = 0
        self._pending_item_apply = True
        self._already_hinted: set[int] = set()
        self._notification_item_index: int = 0
        self._last_mod_unlock_write: float = 0.0
        self._armour_set_checks_enabled = False

        self._last_weapon_state_push: float = 0.0
        self._pushed_weapon_state: dict[str, int] = {}
        self._local_weapon_state: dict[str, int] = {}
        self._weapon_state_restored = False
        self._save_data_received = False
        self._items_received_ready = False
        self._connection_sync_pending = True
        self._starting_skin_option = 0
        self._ap_icon_chosen_by_command = False
        # /skin_patch choice; None follows the YAML's Experimental Skins option.
        self._multiplayer_skins_override: bool | None = None

        self._death_link_enabled = False
        self._last_death_link = 0.0
        self._debug_messages = False
        self._challenge_defaults_written = False

        self._ammo_link_enabled = False
        self._last_ammo_link_push: float = 0.0
        self._pushed_ammo_link: dict[str, int] = {}
        self._applied_ammo_link: dict[str, int] = {}

        self._bolt_link_enabled = False
        self._last_bolt_link_push: float = 0.0
        self._pushed_bolt_link: int | None = None

        self._ghost_link_enabled = False
        self._ghost_link_interval: float = 5.0
        self._last_ghost_link_push: float = 0.0
        self._ghost_link_slots: list[int] = []
        self._ghost_link_peers: dict[int, tuple[int, float, float, float, float]] = {}
        self._ghost_link_following: int | None = None

        self._wiring = Core(self.pine, log=self._log)
        self._wiring.native.vendor_scouts = self.vendor_scouts

    # --- CommonContext stand-ins: requests the client process carries out ---

    async def send_msgs(self, msgs: list[dict[str, Any]]) -> None:
        self._post((protocol.SEND_MSGS, msgs))

    async def check_locations(self, locations) -> set[int]:
        locations = set(locations)
        self._post((protocol.CHECK_LOCATIONS, sorted(locations)))
        return locations

    def set_notify(self, *keys: str) -> None:
        self._post((protocol.SET_NOTIFY, list(keys)))

    async def update_death_link(self, death_link: bool) -> None:
        self._post((protocol.UPDATE_DEATH_LINK, death_link))

    async def _update_link_tag(self, tag: str, enabled: bool) -> None:
        self._post((protocol.UPDATE_LINK_TAG, tag, enabled))

    def handle_connection_loss(self, msg: str) -> None:
        logger.warning(msg)
        self._post((protocol.GUI_ERROR, msg))

    # --- Shared helpers (formerly on RACContext) ---

    async def _guarded_wiring_call(self, fn: Callable[[], None]) -> None:
        async with self._pine_lock:
            try:
                fn()
            except Exception as exc:
                logger.warning(
                    f"[RAC] PINE call failed during wiring sync: {exc}. If syncing stops working, use /reconnect."
                )
                self.pine_connected = False

    def _set_skin_patch(self, enabled: bool) -> None:
        """Switch the skin patch and its multiplayer loader, equipping the default skin when disabling;
        NativeRuntime reloads the planet, which reloads its code without (or with) the patch."""
        native = self._wiring.native
        if not enabled and self.pine_connected:
            self._wiring.skin.set(Skin.DEFAULT)
        self._multiplayer_skins_override = enabled
        native.patch_options = replace(native.patch_options, skins=enabled, multiplayer_skins=enabled)

    def _filler_applied_key(self) -> str:
        return f"racsm_filler_applied_{self.team}_{self.slot}"

    def _save_data_key(self) -> str:
        return f"racsm_save_data_{self.team}_{self.slot}"

    def _stored_save_data(self) -> RAC5SaveData:
        return RAC5SaveData.from_dict(self.stored_data.get(self._save_data_key()))

    def _try_restore_weapon_state(self, *, force: bool = False) -> None:
        """Restore levels only, after this connection's storage reply has arrived."""
        if (
            not self._save_data_received
            or not self.pine_connected
            or (not force and self._weapon_state_restored)
            or not self._wiring.planet.weapons_available
            or self._wiring.at_main_menu
            or self._wiring.vendor_active
        ):
            return
        weapons = self._wiring.planet.weapons
        data = weapons.within_level_ceilings(highest_weapon_levels(
            self._local_weapon_state, self._stored_save_data().weapon_state, weapons.level_snapshot()
        ))
        weapons.restore_levels(data)
        self._local_weapon_state = dict(data)
        self._weapon_state_restored = True

    def _starting_items_key(self) -> str:
        return f"racsm_starting_items_sent_{self.team}_{self.slot}"

    async def _persist_starting_items_sent(self) -> None:
        if self.slot is None:
            return
        await self.send_msgs(
            [
                {
                    "cmd": "Set",
                    "key": self._starting_items_key(),
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": 1}],
                }
            ]
        )

    async def _persist_save_data_field(self, field_name: str, data: dict) -> None:
        """Merge one RAC5SaveData field into the slot's single save-data key, leaving the
        other fields (pushed independently, on their own triggers/cadence) untouched."""
        if self.slot is None:
            return
        await self.send_msgs(
            [
                {
                    "cmd": "Set",
                    "key": self._save_data_key(),
                    "default": {},
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": {field_name: data}}],
                }
            ]
        )

    async def _persist_quick_select(self, data: dict) -> None:
        await self._persist_save_data_field("quick_select", data)

    async def _persist_armour_slots(self, data: dict) -> None:
        await self._persist_save_data_field("armour_slots", data)

    async def _persist_weapon_state(self, data: dict) -> None:
        await self._persist_save_data_field("weapon_state", data)

    def _checked_location_names(self) -> set[str]:
        id_to_name = {v: k for k, v in self._location_name_to_id.items()}
        return {
            id_to_name[lid] for lid in (self.checked_locations | self._locally_checked_locations) if lid in id_to_name
        }

    def _log(self, msg: str, level: str = "info") -> None:
        if not self._debug_messages:
            return
        if level == "warning":
            logger.warning(msg)
        else:
            logger.info(msg)

    # --- Client messages ---

    async def handle(self, message: tuple) -> None:
        kind, *args = message
        if kind == protocol.CONNECTED:
            self._on_connected(*args)
        elif kind == protocol.AP_DISCONNECTED:
            self.ap_connected = False
            self._wiring.native.ap_connected = False
        elif kind == protocol.LOCATIONS:
            self.checked_locations, self.server_locations = set(args[0]), set(args[1])
        elif kind == protocol.RECEIVED_ITEMS:
            self._on_received_items(*args)
        elif kind == protocol.STORED:
            self._on_stored(*args)
        elif kind == protocol.BOUNCED:
            data = args[0]
            if self._death_link_enabled and data.get("source") != self.auth:
                asyncio.create_task(self._receive_death_link(data))
        elif kind == protocol.VENDOR_REWARDS:
            self.vendor_scouts.rewards = dict(args[0])
        elif kind == protocol.ITEM_SENT:
            self._write_notification_text(sent_text(*args))
        elif kind == protocol.CALL:
            method, call_args = args
            if not method.startswith("cmd_"):
                raise ValueError(f"Refusing worker call {method!r}")
            result = getattr(self, method)(*call_args)
            if asyncio.iscoroutine(result):
                await result
        else:
            raise ValueError(f"Unknown worker message {kind!r}")

    def _on_connected(self, payload: dict[str, Any]) -> None:
        self.slot = payload["slot"]
        self.team = payload["team"]
        self.auth = payload["auth"]
        self.slot_data = payload["slot_data"]
        self.slot_info = payload["slot_info"]
        self.player_names = payload["player_names"]
        self.checked_locations = set(payload["checked_locations"])
        self.server_locations = set(payload["server_locations"])
        self.ap_connected = True
        self._wiring.native.ap_connected = True
        self._wiring.vendor.configure_rules(self.slot_data.get("vendor_rules"))
        self._wiring.native.enabled = True
        native_ids = self.server_locations
        self._wiring.native.allowed_locations = {
            name for name, location_id in self._location_name_to_id.items() if location_id in native_ids
        }
        self._wiring.planet_unlock.split_infobots = bool(self.slot_data.get("split_infobots", False))
        self._already_hinted.clear()
        self.vendor_scouts.rewards.clear()
        scout_request = self.vendor_scouts.request(native_ids)
        if scout_request["locations"]:
            asyncio.create_task(self.send_msgs([scout_request]))
        self._ap_loadout_restored = False
        self._weapon_state_restored = False
        self._local_weapon_state = {}
        self._pushed_weapon_state = {}
        self._last_weapon_state_push = 0.0
        self._save_data_received = False
        self._items_received_ready = False
        self._connection_sync_pending = True
        self._wiring._ap_inventory_ready = False
        self._death_link_enabled = bool(self.slot_data.get(Rac5Options.DEATH_LINK, False))
        self._ammo_link_enabled = bool(self.slot_data.get(Rac5Options.AMMO_LINK, False))
        self._bolt_link_enabled = bool(self.slot_data.get(Rac5Options.BOLT_LINK, False))
        self._ghost_link_enabled = bool(self.slot_data.get(Rac5Options.GHOST_LINK, False))
        self._ghost_link_interval = float(self.slot_data.get(Rac5Options.GHOST_LINK_UPDATE_INTERVAL, 5) or 0)
        if self._ghost_link_enabled:
            self._refresh_ghost_link_slots()
        self._armour_set_checks_enabled = bool(self.slot_data.get(Rac5Options.ARMOUR_SET_CHECKS, False))
        self._wiring.options = ClientOptions.from_slot_data(self.slot_data)
        self._wiring.planet.giant_clank_allowed = bool(self.slot_data.get(Rac5Options.GIANT_CLANK, False))
        self._wiring.planet.set_starting_planet(self.slot_data.get("starting_planet_id"))
        self._wiring.planet_unlock.set_random_start(
            int(self.slot_data.get(Rac5Options.RANDOM_STARTING_PLANET, 0)) != 0
        )
        self._wiring.planet.weapons.experience_multiplier = (
            int(self.slot_data.get(Rac5Options.WEAPON_EXPERIENCE_MULTIPLIER, 0)) or 1
        )
        self._wiring.planet.weapons.progressive_mode = int(self.slot_data.get(Rac5Options.PROGRESSIVE_WEAPONS, 0))
        self._wiring.progressive_challenge_mode_enabled = bool(
            self.slot_data.get(Rac5Options.PROGRESSIVE_CHALLENGE_MODE, False)
        )
        self._wiring.native.progressive_challenge_mode_enabled = self._wiring.progressive_challenge_mode_enabled
        if self._wiring.progressive_challenge_mode_enabled:
            challenge_mode_option = 0
        else:
            challenge_mode_option = int(self.slot_data.get(Rac5Options.CHALLENGE_MODE, 0))
            self._wiring.planet.weapons.challenge_mode = challenge_mode_option
            self._wiring.vendor.challenge_mode = challenge_mode_option
        self._wiring.player_bolts.multiplier = int(self.slot_data.get(Rac5Options.BOLT_MULTIPLIER, 0)) or 1
        self._wiring.player_health_exp.multiplier = (
            int(self.slot_data.get(Rac5Options.NANOTECH_EXPERIENCE_MULTIPLIER, 0)) or 1
        )
        trap_duration = self.slot_data.get(Rac5Options.TRAP_DURATION)
        if isinstance(trap_duration, dict):
            set_trap_durations(trap_duration)
        self._starting_skin_option = int(self.slot_data.get(Rac5Options.STARTING_SKIN, 0))
        self._wiring.native.patch_options = replace(
            self._wiring.native.patch_options,
            multiplayer_skins=(
                bool(self.slot_data.get(Rac5Options.EXPERIMENTAL_SKINS, False))
                if self._multiplayer_skins_override is None
                else self._multiplayer_skins_override
            ),
            balance_patch=bool(self.slot_data.get(Rac5Options.BALANCE_PATCH, False)),
        )
        if not self._ap_icon_chosen_by_command:
            try:
                vendor_presentation.set_icon_style(str(self.slot_data.get(Rac5Options.AP_ICON, "original")))
            except ValueError as e:
                logger.info(f"[RAC] {e}")
        for tag, enabled in (
            ("DeathLink", self._death_link_enabled),
            ("AmmoLink", self._ammo_link_enabled),
            ("BoltLink", self._bolt_link_enabled),
            ("GhostLink", self._ghost_link_enabled),
        ):
            if enabled:
                asyncio.create_task(self._update_link_tag(tag, True))
        self._wiring.wire(
            send_location=self._append_location_by_name,
            send_deathlink=self._send_death_link_from_sync,
            death_amnesty=lambda: int(self.slot_data.get(Rac5Options.DEATH_AMNESTY, 1)),
            death_link_enabled=lambda: self._death_link_enabled,
            on_goal=lambda: asyncio.create_task(self._send_goal_status()),
            on_vendor_open=lambda: asyncio.create_task(self._send_vendor_hints()),
            on_vendor_close=self._on_vendor_close,
            on_equipped_armour_saved=self._on_equipped_armour_saved,
            on_bonus_weapon_pickup=self._grant_random_bonus_item,
            on_scripted_gadget_pickup=self._handle_scripted_gadget_pickup,
            on_planet_ready=self._on_planet_ready,
            on_weapon_level_up=self._on_weapon_level_up,
            on_initial_load=lambda: asyncio.create_task(self._send_playing_status()),
        )
        checked = self._checked_location_names()
        starting_skin = self._starting_skin_option if self._wiring.native.patch_options.skins else Skin.DEFAULT.equip_id
        skin_patch = self._wiring.native.patch_options.multiplayer_skins
        asyncio.create_task(
            self._guarded_wiring_call(
                lambda: (
                    self._wiring.skin.set_by_option(starting_skin),
                    None if skin_patch else self._wiring.skin.clear_multiplayer(),
                    self._wiring.challenge_mode.set_by_option(challenge_mode_option),
                    self._wiring.sync_from_ap(checked),
                )
            )
        )
        self._pending_item_apply = True
        asyncio.create_task(self.force_sync())
        self._write_notification_text(
            colored_text(
                "Connected to ",
                TextColour.YELLOW,
                "Archipelago",
                TextColour.WHITE,
            )
        )
        if not self.pine_connected:
            if payload.get("pine_port") is not None:
                self.pine.set_slot(payload["pine_port"])
            asyncio.create_task(self._attempt_pine_connect(), name="PCSX2 PINE connect")
        else:
            asyncio.create_task(self._send_map_page(self.current_planet))
        self._wiring.quick_select.on_save = lambda data: asyncio.create_task(self._persist_quick_select(data))
        link_keys = []
        if self._ammo_link_enabled:
            link_keys.append(self._ammo_link_key())
        if self._bolt_link_enabled:
            link_keys.append(self._bolt_link_key())
        if self._ghost_link_enabled:
            link_keys += [self._ghost_link_key(slot) for slot in self._ghost_link_slots]
        keys = [self._filler_applied_key(), self._save_data_key(), self._starting_items_key(), *link_keys]
        self.set_notify(*keys)
        asyncio.create_task(self.send_msgs([{"cmd": "Get", "keys": keys}]))

    def _on_stored(self, updated: dict[str, Any]) -> None:
        if self.slot is None:
            return
        self.stored_data.update(updated)
        if self._save_data_key() in updated:
            self._save_data_received = True
        if self._save_data_received and not self._ap_loadout_restored:
            save_data = self._stored_save_data()
            if save_data.quick_select:
                self._wiring.quick_select.load(save_data.quick_select)
                if self._wiring.planet.is_ready:
                    self._wiring.quick_select.restore()
            if save_data.armour_slots and self._wiring.planet.is_ready:
                self._wiring.armour.sync_equipped(save_data.armour_slots)
            self._ap_loadout_restored = True
        self._try_restore_weapon_state()
        if self._ammo_link_enabled:
            asyncio.create_task(self._guarded_wiring_call(self._apply_ammo_link_update))
        if self._bolt_link_enabled:
            asyncio.create_task(self._guarded_wiring_call(self._apply_bolt_link_update))
        if self._ghost_link_enabled:
            self._refresh_ghost_link_peers()
        starting_items_key = self._starting_items_key()
        if starting_items_key in self.stored_data:
            self._starting_items_sent = self._starting_items_sent or bool(self.stored_data[starting_items_key])
            if not self._starting_items_sent and self._wiring.planet.is_ready:
                asyncio.create_task(self._grant_starting_items())
        if not self._filler_checkpoint_synced:
            key = self._filler_applied_key()
            if key in self.stored_data:
                checkpoint = min(int(self.stored_data[key] or 0), len(self.items_received))
                self._processed_item_count = checkpoint
                self._processed_trap_count = checkpoint
                self._filler_checkpoint_synced = True
                self._pending_item_apply = True
                asyncio.create_task(self._apply_received_items())

    def _on_received_items(self, items: list, index: int) -> None:
        self.items_received = list(items)
        if index == 0:
            self._items_received_ready = True
            self._notification_item_index = len(self.items_received)
        checked = self._checked_location_names()
        asyncio.create_task(self._guarded_wiring_call(lambda: self._wiring.sync_from_ap(checked)))
        self._pending_item_apply = True
        asyncio.create_task(self._apply_received_items())

    # --- Commands forwarded from RACCommandProcessor ---

    async def cmd_reconnect(self) -> None:
        await self.reconnect_pine()

    async def cmd_force_sync(self) -> None:
        await self.force_sync()

    def _states(self) -> tuple:
        w = self._wiring
        return (
            w.armour, w.bolts, w.player_bolts, w.planet_unlock, w.quick_select,
            w.clank, w.skyboard, w.shrink_ray, w.skill_points, w.missions, w.skin,
              w.planet, w.planet.weapons, w.planet.player, w.planet.menu, w.ghost_ratchet,
            w.weapon_vendor, w.mod_vendor, w.vendor,
        )

    def cmd_states(self) -> None:
        for state in self._states():
            logger.info(repr(state))

    def cmd_rac5_info(self) -> None:
        options = "\n".join(f"{key}: {value}" for key, value in self.slot_data.items())
        logger.info(f"[RAC] Options:\n{options}")
        logger.info("[RAC] States: " + " ".join(repr(state) for state in self._states()))
        goal = Rac5CutsceneLocations.QUODRONA_GOAL
        completion = ALL_LOCATIONS[goal].completed
        logger.info(
            "[RAC] Goal: game_id=%s planet_id=%s tracked=%s worker_finished_game=%s",
            address_maps.GAME_ID, self._wiring.planet.planet_id,
            goal in self._wiring.missions.completed, self.finished_game,
        )
        if self.pine_connected:
            try:
                address = address_maps.save_address(completion.key)
                raw = self.pine.read_int16(address)
                logger.info(
                    "[RAC] Goal memory: address=0x%08X raw=0x%04X mask=0x%04X matched=%s",
                    address, raw, completion.mask, bool(raw & completion.mask),
                )
            except Exception as exc:
                logger.warning("[RAC] Could not read goal memory: %s", exc)

    def cmd_vendor_refresh(self) -> None:
        self._wiring.vendor.force_refresh()
        logger.info(f"[RAC] {self._wiring.vendor!r}")

    async def cmd_skin(self, skin: Skin) -> None:
        if not self.pine_connected:
            logger.info("[RAC] Connect to PCSX2 before changing skins.")
            return
        if skin.unlock_mask is None and not self._wiring.native.patch_options.multiplayer_skins:
            logger.info("[RAC] Multiplayer skins need the skin patch: /skin_patch on.")
            return
        await self._guarded_wiring_call(lambda: self._wiring.skin.set(skin))
        logger.info("[RAC] Skin queued: %s. Applies when gameplay is ready.", skin.name)

    async def cmd_skin_patch(self, enabled: bool | None) -> None:
        options = self._wiring.native.patch_options
        if enabled is None:
            state = ("enabled" if options.multiplayer_skins else "enabled without multiplayer skins") \
                if options.skins else "disabled"
            logger.info(f"[RAC] Skin patch {state}. Use /skin_patch on|off.")
            return
        if (options.skins and options.multiplayer_skins) if enabled else not options.skins:
            logger.info(f"[RAC] Skin patch already {'enabled' if enabled else 'disabled'}.")
            return
        await self._guarded_wiring_call(lambda: self._set_skin_patch(enabled))
        logger.info(f"[RAC] Skin patch {'enabled' if enabled else 'disabled and default skin equipped'}. "
                    "Reloading the planet to apply it.")

    def cmd_apicon(self, style: str) -> None:
        if not style:
            logger.info(f"[RAC] AP icon style: {vendor_presentation.get_icon_style()}. "
                        f"Choices: {', '.join(vendor_presentation.ICON_STYLES)}")
            return
        try:
            vendor_presentation.set_icon_style(style)
        except ValueError as e:
            logger.info(f"[RAC] {e}")
            return
        self._ap_icon_chosen_by_command = True
        logger.info(f"[RAC] AP icon style set to {vendor_presentation.get_icon_style()}.")

    async def cmd_spawn_ghost(self) -> None:
        async with self._pine_lock:
            spawned = self._wiring.spawn_ghost_ratchet()
        if spawned:
            logger.info("[RAC] Ghost Ratchet spawned.")
        else:
            logger.info("[RAC] Ghost Ratchet isn't available on this planet yet.")

    def cmd_debug(self) -> None:
        self._debug_messages = not self._debug_messages
        logger.info(f"[RAC] Debug messages {'enabled' if self._debug_messages else 'disabled'}.")

    async def cmd_toggle_deathlink(self) -> None:
        await self._set_death_link_enabled(not self._death_link_enabled)

    async def cmd_toggle_ammolink(self) -> None:
        await self._set_ammo_link_enabled(not self._ammo_link_enabled)

    async def cmd_toggle_boltlink(self) -> None:
        await self._set_bolt_link_enabled(not self._bolt_link_enabled)


def worker_main(inbox, outbox) -> None:
    """multiprocessing entry point (spawned, so this module is re-imported in the child)."""
    root = logging.getLogger()
    for handler in list(root.handlers):
        root.removeHandler(handler)
    root.addHandler(protocol.ForwardingLogHandler(outbox.put))
    root.setLevel(logging.INFO)
    asyncio.run(_run(inbox, outbox))


async def _run(inbox, outbox) -> None:
    loop = asyncio.get_running_loop()
    messages: asyncio.Queue = asyncio.Queue()

    def pump() -> None:
        while True:
            message = inbox.get()
            loop.call_soon_threadsafe(messages.put_nowait, message)
            if message[0] == protocol.SHUTDOWN:
                return

    threading.Thread(target=pump, name="RAC worker inbox", daemon=True).start()
    worker = GameWorker(outbox.put)
    watcher = asyncio.create_task(worker.game_watcher(), name="RAC game watcher")
    try:
        while True:
            message = await messages.get()
            if message[0] == protocol.SHUTDOWN:
                break
            try:
                await worker.handle(message)
            except Exception:
                logger.exception(f"[RAC] Worker failed handling {message[0]!r}")
    finally:
        worker.exit_event.set()
        await watcher
        await worker._teardown_pine_connection()

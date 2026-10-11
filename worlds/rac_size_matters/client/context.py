from __future__ import annotations

import asyncio
from collections.abc import Callable
from dataclasses import replace
from typing import Any

from ..constants.options import Rac5Options

tracker_loaded: bool = False
dynamicpine_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import UT_VERSION, TrackerGameContext as CommonContext

    tracker_loaded = True
except ImportError:
    from CommonClient import CommonContext
try:
    from worlds.dynamicpine import DYNAMIC_PINE_VERSION, get_pending_auth, get_pine_port, launched_via_hub

    dynamicpine_loaded = True
except ImportError:
    DYNAMIC_PINE_VERSION = None
from CommonClient import logger

from ..core import RAC5SaveData, TextColour, colored_text, set_trap_durations
from ..core.core import Core
from ..core import vendor_presentation
from ..core.options import ClientOptions
from ..core.save_data import highest_weapon_levels
from ..locations import ALL_LOCATIONS
from ..pypine import Pine
from ..world import RACSizeMatterWorld
from .ammo_link import AmmoLinkMixin
from .bolt_link import BoltLinkMixin
from .command_processor import RACCommandProcessor
from .constants import GAME_NAME
from .deathlink import DeathLinkMixin
from .ghost_link import GhostLinkMixin
from .handlers import CutsceneHandlerMixin, EventsHandlerMixin
from .pine_mixin import PineMixin
from .vendor import InventoryMixin, VendorHandlerMixin
from .vendor_scouts import VendorScouts

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

class RACContext(
    PineMixin,
    CutsceneHandlerMixin,
    EventsHandlerMixin,
    DeathLinkMixin,
    AmmoLinkMixin,
    BoltLinkMixin,
    GhostLinkMixin,
    VendorHandlerMixin,
    InventoryMixin,
    CommonContext,
):
    game = GAME_NAME
    command_processor = RACCommandProcessor
    items_handling = 0b111
    current_planet: str = "Galaxy"
    tags = CommonContext.tags - {"Tracker"}

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)

        self.pine = Pine()
        self.pine_connected = False
        self._pine_lock = asyncio.Lock()
        self.slot_data: dict[str, Any] = {}

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

    async def _guarded_wiring_call(self, fn: Callable[[], None]) -> None:
        async with self._pine_lock:
            try:
                fn()
            except Exception as exc:
                logger.warning(
                    f"[RAC] PINE call failed during wiring sync: {exc}. If syncing stops working, use /reconnect."
                )
                self.pine_connected = False

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

    def _dyanmic_pine_port(self) -> None:
        """Resolve the PCSX2 port Dynamic Pine assigned this instance. Gated on launched_via_hub(),
        not just self.auth, so a stale hub-launched port never leaks into a manual launch."""
        if not self.auth or not dynamicpine_loaded:
            return
        if not launched_via_hub():
            return
        port = get_pine_port(GAME_NAME, self.auth)
        if port is not None:
            self.pine.set_slot(port)

    def _dynamic_pine_auth(self) -> None:
        """Pre-fills auth from the slot name the hub's /launch command was given, so it matches
        what _dyanmic_pine_port() later looks the PCSX2 instance's port up under."""
        if self.auth or not dynamicpine_loaded:
            return
        if not launched_via_hub():
            return
        pending = get_pending_auth()
        if pending:
            self.auth = pending

    async def _update_link_tag(self, tag: str, enabled: bool) -> None:
        """Generic counterpart to CommonContext.update_death_link — sets/clears an arbitrary
        connection tag and pushes ConnectUpdate if already connected."""
        old_tags = self.tags.copy()
        if enabled:
            self.tags.add(tag)
        else:
            self.tags -= {tag}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": list(self.tags)}])

    def _log(self, msg: str, level: str = "info") -> None:
        if not self._debug_messages:
            return
        if level == "warning":
            logger.warning(msg)
        else:
            logger.info(msg)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        self._dynamic_pine_auth()
        await self.get_username()
        await self.send_connect(game=self.game)

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        super().on_package(cmd, args)

        if cmd in ("LocationInfo", "DataPackage", "RoomUpdate"):
            self.vendor_scouts.update(
                self.locations_info.values(),
                self.item_names.lookup_in_slot,
                lambda slot: self.player_names.get(slot, f"Player {slot}"),
            )

        if cmd == "Connected":
            self._wiring.native.ap_connected = True
            self.slot_data = args.get("slot_data", {})
            self._wiring.vendor.configure_rules(self.slot_data.get("vendor_rules"))
            self._wiring.native.enabled = True
            native_ids = set(args.get("missing_locations", ())) | set(args.get("checked_locations", ()))
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
                multiplayer_skins=bool(self.slot_data.get(Rac5Options.EXPERIMENTAL_SKINS, False)),
                balance_patch=bool(self.slot_data.get(Rac5Options.BALANCE_PATCH, False)),
            )
            if not self._ap_icon_chosen_by_command:
                try:
                    vendor_presentation.set_icon_style(str(self.slot_data.get(Rac5Options.AP_ICON, "original")))
                except ValueError as e:
                    logger.info(f"[RAC] {e}")
            link_tags = [
                tag
                for tag, enabled in (
                    ("DeathLink", self._death_link_enabled),
                    ("AmmoLink", self._ammo_link_enabled),
                    ("BoltLink", self._bolt_link_enabled),
                    ("GhostLink", self._ghost_link_enabled),
                )
                if enabled
            ]
            if link_tags:
                self.tags |= set(link_tags)
                asyncio.create_task(self.send_msgs([{"cmd": "ConnectUpdate", "tags": list(self.tags)}]))
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
            starting_skin = self._starting_skin_option
            asyncio.create_task(
                self._guarded_wiring_call(
                    lambda: (
                        self._wiring.skin.set_by_option(starting_skin),
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
                self._dyanmic_pine_port()
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
            for key in (
                self._filler_applied_key(),
                self._save_data_key(),
                self._starting_items_key(),
                *link_keys,
            ):
                self.set_notify(key)
            asyncio.create_task(
                self.send_msgs(
                    [
                        {
                            "cmd": "Get",
                            "keys": [
                                self._filler_applied_key(),
                                self._save_data_key(),
                                self._starting_items_key(),
                                *link_keys,
                            ],
                        }
                    ]
                )
            )
            return

        if cmd in ("Retrieved", "SetReply") and self.slot is not None:
            save_reply = (
                self._save_data_key() in args.get("keys", {})
                if cmd == "Retrieved"
                else args.get("key") == self._save_data_key()
            )
            if save_reply:
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
            return

        if cmd == "ReceivedItems":
            if args.get("index", 0) == 0:
                self._items_received_ready = True
                self._notification_item_index = len(self.items_received)
            checked = self._checked_location_names()
            asyncio.create_task(self._guarded_wiring_call(lambda: self._wiring.sync_from_ap(checked)))
            self._pending_item_apply = True
            asyncio.create_task(self._apply_received_items())
            return

        if cmd == "Bounced" and self._death_link_enabled and "DeathLink" in args.get("tags", []):
            data = args.get("data", {})
            if data.get("source") != self.auth:
                asyncio.create_task(self._receive_death_link(data))

    async def connection_closed(self) -> None:
        self._wiring.native.ap_connected = False
        await super().connection_closed()

    def on_print_json(self, args: dict) -> None:
        super().on_print_json(args)
        if args.get("type") == "ItemSend" and args["item"].player == self.slot:
            self._show_item_send_notification(args["item"], args["receiving"])

    def make_gui(self):
        ui = super().make_gui()
        version = RACSizeMatterWorld.world_version.as_simple_string()
        base_name = "R&C: 5" if tracker_loaded and dynamicpine_loaded else "R&C: Size Matters Client"
        ui.base_title = f"{base_name} v{version}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"
        if dynamicpine_loaded:
            ui.base_title += f" | Dynamic Pine v{DYNAMIC_PINE_VERSION}"

        ui.base_title += f" | {apname}"
        return ui

import asyncio
import logging
from typing import Any

from NetUtils import ClientStatus

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

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"
    
from ..locations import ALL_LOCATIONS
from ..world import RACSizeMatterWorld
from . import protocol
from .command_processor import RACCommandProcessor
from .constants import GAME_NAME
from .vendor_scouts import VendorScouts
from .worker_link import WorkerLink


class RACContext(CommonContext):
    """AP side of the client. All PCSX2 access lives in the worker process (see worker.py)."""

    game = GAME_NAME
    command_processor = RACCommandProcessor
    items_handling = 0b111
    tags = CommonContext.tags - {"Tracker"}

    def __init__(self, server_address: str | None, password: str | None) -> None:
        super().__init__(server_address, password)
        self.slot_data: dict[str, Any] = {}
        self._location_name_to_id = {name: data.code for name, data in ALL_LOCATIONS.items()}
        self.vendor_scouts = VendorScouts(self._location_name_to_id)
        self._worker = WorkerLink(self._on_worker_message, self._on_worker_exit)
        # Latest state per kind, replayed into a restarted worker.
        self._worker_state: dict[str, tuple] = {}
        self._stored_for_worker: dict[str, Any] = {}

    # --- Worker lifecycle ---

    def start_worker(self) -> None:
        self._worker.start(asyncio.get_running_loop())
        for message in self._worker_state.values():
            self._worker.send(message)
        if self._stored_for_worker:
            self._worker.send((protocol.STORED, dict(self._stored_for_worker)))

    def call_worker(self, method: str, *args: Any) -> None:
        """Run a worker cmd_* method; restarts the worker first if it has died."""
        if not self._worker.alive:
            logger.info("[RAC] Restarting the PCSX2 worker.")
            self.start_worker()
        self._worker.send((protocol.CALL, method, args))

    def _to_worker(self, message: tuple, *, remember: bool = False) -> None:
        if remember:
            self._worker_state[message[0]] = message
        self._worker.send(message)

    def _on_worker_exit(self, exitcode: int | None) -> None:
        logger.warning(f"[RAC] The PCSX2 worker stopped (exit code {exitcode}). Use /reconnect to restart it.")

    def _on_worker_message(self, message: tuple) -> None:
        kind, *args = message
        if kind == protocol.LOG:
            name, level, text = args
            logging.getLogger(name).log(level, text)
        elif kind == protocol.SEND_MSGS:
            msgs = args[0]
            if any(msg.get("cmd") == "StatusUpdate" and msg.get("status") == ClientStatus.CLIENT_GOAL
                   for msg in msgs):
                self.finished_game = True
            # A worker restart/Continue can announce PLAYING after victory.
            # Keep the AP-side latch authoritative, including for a new worker.
            if self.finished_game:
                msgs = [msg for msg in msgs if not (
                    msg.get("cmd") == "StatusUpdate"
                    and msg.get("status") == ClientStatus.CLIENT_PLAYING
                )]
            if msgs:
                asyncio.create_task(self.send_msgs(msgs))
        elif kind == protocol.CHECK_LOCATIONS:
            asyncio.create_task(self.check_locations(args[0]))
        elif kind == protocol.SET_NOTIFY:
            self.set_notify(*args[0])
        elif kind == protocol.UPDATE_DEATH_LINK:
            asyncio.create_task(self.update_death_link(args[0]))
        elif kind == protocol.UPDATE_LINK_TAG:
            asyncio.create_task(self._update_link_tag(*args))
        elif kind == protocol.GUI_ERROR:
            self._messagebox_connection_loss = self.gui_error(args[0], ConnectionError(args[0]))
        else:
            logger.warning(f"[RAC] Unknown worker message {kind!r}")

    # --- AP connection ---

    def _dynamic_pine_port(self) -> int | None:
        """Resolve the PCSX2 port Dynamic Pine assigned this instance. Gated on launched_via_hub(),
        not just self.auth, so a stale hub-launched port never leaks into a manual launch."""
        if not self.auth or not dynamicpine_loaded or not launched_via_hub():
            return None
        return get_pine_port(GAME_NAME, self.auth)

    def _dynamic_pine_auth(self) -> None:
        """Pre-fills auth from the slot name the hub's /launch command was given, so it matches
        what _dynamic_pine_port() later looks the PCSX2 instance's port up under."""
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

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        self._dynamic_pine_auth()
        await self.get_username()
        await self.send_connect(game=self.game)

    def _send_locations(self) -> None:
        self._to_worker((protocol.LOCATIONS, set(self.checked_locations), set(self.server_locations)),
                        remember=True)

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        super().on_package(cmd, args)

        if cmd in ("LocationInfo", "DataPackage", "RoomUpdate"):
            self.vendor_scouts.update(
                self.locations_info.values(),
                self.item_names.lookup_in_slot,
                lambda slot: self.player_names.get(slot, f"Player {slot}"),
            )
            self._to_worker((protocol.VENDOR_REWARDS, dict(self.vendor_scouts.rewards)), remember=True)

        if cmd == "RoomUpdate":
            self._send_locations()

        if cmd == "Connected":
            self.slot_data = args.get("slot_data", {})
            self.vendor_scouts.rewards.clear()
            self._stored_for_worker.clear()
            self._worker_state.clear()
            self._to_worker((protocol.CONNECTED, {
                "slot": self.slot,
                "team": self.team,
                "auth": self.auth,
                "slot_data": self.slot_data,
                "slot_info": dict(self.slot_info),
                "player_names": dict(self.player_names),
                "checked_locations": set(self.checked_locations),
                "server_locations": set(self.server_locations),
                "pine_port": self._dynamic_pine_port(),
            }), remember=True)
            self._send_locations()
            return

        if cmd in ("Retrieved", "SetReply") and self.slot is not None:
            updated = dict(args.get("keys", {})) if cmd == "Retrieved" else {args.get("key"): args.get("value")}
            self._stored_for_worker.update(updated)
            self._to_worker((protocol.STORED, updated))
            return

        if cmd == "ReceivedItems":
            self._to_worker((protocol.RECEIVED_ITEMS, list(self.items_received), args.get("index", 0)))
            self._worker_state[protocol.RECEIVED_ITEMS] = (protocol.RECEIVED_ITEMS, list(self.items_received), 0)
            return

        if cmd == "Bounced" and "DeathLink" in args.get("tags", []):
            self._to_worker((protocol.BOUNCED, args.get("data", {})))

    async def connection_closed(self) -> None:
        self._to_worker((protocol.AP_DISCONNECTED,))
        await super().connection_closed()

    def on_print_json(self, args: dict) -> None:
        super().on_print_json(args)
        if args.get("type") == "ItemSend" and args["item"].player == self.slot:
            receiving = args["receiving"]
            if receiving == self.slot:
                return
            receiver_game = self.slot_info[receiving].game if receiving in self.slot_info else self.game
            item_name = self.item_names[receiver_game].get(args["item"].item, "???")
            player_name = self.player_names.get(receiving, f"Player {receiving}")
            self._to_worker((protocol.ITEM_SENT, item_name, player_name))

    async def shutdown(self) -> None:
        await asyncio.to_thread(self._worker.stop)
        await super().shutdown()

    def make_gui(self):
        ui = super().make_gui()
        version = RACSizeMatterWorld.world_version.as_simple_string()
        base_name = "R&C: 5" if tracker_loaded and dynamicpine_loaded else "R&C: Size Matters Client"
        ui.base_title = f"{base_name} v{version}"
        if tracker_loaded:
            ui.base_title += f" | Universal Tracker {UT_VERSION}"
        if dynamicpine_loaded:
            ui.base_title += f" | Dynamic Pine v{DYNAMIC_PINE_VERSION}"

        ui.base_title += " | {apname}"
        return ui

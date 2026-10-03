import asyncio
import sys
import urllib.parse

import CommonClient
import NetUtils
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from typing import Any, Dict, List, Optional, Set

tracker_loaded: bool = False

try:
    from worlds.tracker.TrackerClient import TrackerGameContext as Context
    from worlds.tracker.TrackerClient import TrackerCommandProcessor as CommandProcessor

    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as Context
    from CommonClient import ClientCommandProcessor as CommandProcessor

from .data_funcs import (
    item_names_to_id,
    item_names_to_item,
    location_names_to_id,
    id_to_client_seed_information,
    id_to_craftable_spell_behaviors,
    id_to_deathsanity,
    id_to_entrance_randomizer,
    id_to_hotspots,
    id_to_in_game_overlay_options,
    id_to_items,
    id_to_landmarksanity,
    id_to_locations,
    id_to_goals,
    id_to_starting_locations,
)

from .enums import ZorkGrandInquisitorInGameOverlayOptions, ZorkGrandInquisitorItems, ZorkGrandInquisitorLocations
from .game_controller import GameController


class ZorkGrandInquisitorCommandProcessor(CommandProcessor):
    ctx: "ZorkGrandInquisitorContext"

    def _cmd_zork(self) -> None:
        """Attach to an open Zork Grand Inquisitor process."""
        if not self.ctx.server or not self.ctx.slot:
            self.output(f"You must be connected to your {apname} server before using /zork.")
            return

        result: bool = self.ctx.game_controller.open_process_handle()

        if result:
            self.ctx.process_attached_at_least_once = True
            self.output("Successfully attached to Zork Grand Inquisitor process.")

            self.ctx.game_controller.output_seed_information()
            self.ctx.game_controller.output_starter_kit()

            Utils.async_start(
                self.ctx.send_msgs([
                    {
                        "cmd": "StatusUpdate",
                        "status": CommonClient.ClientStatus.CLIENT_PLAYING
                    }
                ])
            )
        else:
            self.output("Failed to attach to Zork Grand Inquisitor process.")

    def _cmd_deathlink(self) -> None:
        """Toggle deathlink status."""
        if not self.ctx.game_controller.option_death_link:
            return

        self.ctx.death_link_status = not self.ctx.death_link_status

    def _cmd_overlay(self) -> None:
        """Toggle the in-game overlay."""
        if not self.ctx.server or not self.ctx.slot:
            self.output("You must be connected to an Archipelago server before using /overlay.")
            return

        self.ctx.game_controller.is_overlay_enabled = not self.ctx.game_controller.is_overlay_enabled

        if self.ctx.game_controller.is_overlay_enabled:
            self.output("In-game overlay enabled.")
        else:
            self.output("In-game overlay disabled.")

    def _cmd_overlay_tracker(self) -> None:
        """Toggle the in-game list of locations in logic."""
        if not self.ctx.server or not self.ctx.slot:
            self.output("You must be connected to an Archipelago server before using /overlay_tracker.")
            return

        if not tracker_loaded:
            self.output("The in-game list of locations in logic requires Universal Tracker, which isn't installed.")
            return

        self.ctx.game_controller.is_in_logic_overlay_enabled = not self.ctx.game_controller.is_in_logic_overlay_enabled

        if self.ctx.game_controller.is_in_logic_overlay_enabled and not self.ctx.game_controller.is_overlay_enabled:
            self.output("In-game list of locations in logic enabled. It will show when the overlay is turned on with /overlay.")
        elif self.ctx.game_controller.is_in_logic_overlay_enabled:
            self.output("In-game list of locations in logic enabled.")
        else:
            self.output("In-game list of locations in logic disabled.")


class ZorkGrandInquisitorContext(Context):
    tags: Set[str] = {"AP"}
    game: str = "Zork Grand Inquisitor"
    command_processor: CommonClient.ClientCommandProcessor = ZorkGrandInquisitorCommandProcessor
    items_handling: int = 0b111
    want_slot_data: bool = True

    item_name_to_id: Dict[str, int] = item_names_to_id()
    location_name_to_id: Dict[str, int] = location_names_to_id()

    id_to_items: Dict[int, ZorkGrandInquisitorItems] = id_to_items()
    id_to_locations: Dict[int, ZorkGrandInquisitorLocations] = id_to_locations()

    game_controller: GameController
    data_storage_key: Optional[str]
    death_link_status: bool = False
    entrance_randomizer_data_by_name: Optional[Dict[str, str]]

    controller_task: Optional[asyncio.Task]

    process_attached_at_least_once: bool
    can_display_process_message: bool

    is_goal_sent: bool

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)

        self.game_controller = GameController(logger=CommonClient.logger)

        self.data_storage_key = None
        self.entrance_randomizer_data_by_name = None

        self.controller_task = None

        self.process_attached_at_least_once = False
        self.can_display_process_message = True

        self.is_goal_sent = False

        if tracker_loaded:
            def update_locations_in_logic(locations_in_logic: List[str]) -> None:
                self.game_controller.locations_in_logic = locations_in_logic

            self.update_callback = update_locations_in_logic

    def make_gui(self):
        from .client_gui.client_gui import bootstrap_client_gui
        return bootstrap_client_gui(super().make_gui())

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)

        await self.get_username()
        await self.send_connect()

    async def disconnect(self, allow_autoreconnect: bool = False):
        try:
            self.game_controller.close_process_handle()
        except Exception:
            pass

        self.game_controller.reset()

        self.data_storage_key = None

        self.is_goal_sent = False

        self.items_received = []
        self.locations_info = {}

        if self.ui:
            self.ui.update_tabs()

        await super().disconnect(allow_autoreconnect)

    async def shutdown(self):
        self.game_controller.clear_overlays()

        await super().shutdown()

    def on_package(self, cmd: str, _args: Any) -> None:
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game

            # Options
            self.game_controller.option_goal = id_to_goals()[_args["slot_data"]["goal"]]

            self.game_controller.option_artifacts_of_magic_required = (
                _args["slot_data"]["artifacts_of_magic_required"]
            )

            self.game_controller.option_artifacts_of_magic_total = (
                _args["slot_data"]["artifacts_of_magic_total"]
            )

            self.game_controller.option_landmarks_required = (
                _args["slot_data"]["landmarks_required"]
            )

            self.game_controller.option_deaths_required = (
                _args["slot_data"]["deaths_required"]
            )

            self.game_controller.option_starting_location = (
                id_to_starting_locations()[_args["slot_data"]["starting_location"]]
            )

            self.game_controller.option_hotspots = (
                id_to_hotspots()[_args["slot_data"]["hotspots"]]
            )

            self.game_controller.option_craftable_spells = (
                id_to_craftable_spell_behaviors()[_args["slot_data"]["craftable_spells"]]
            )

            self.game_controller.option_wild_voxam = _args["slot_data"]["wild_voxam"] == 1
            self.game_controller.option_wild_voxam_chance = _args["slot_data"]["wild_voxam_chance"]

            self.game_controller.option_deathsanity = (
                id_to_deathsanity()[_args["slot_data"]["deathsanity"]]
            )

            self.game_controller.option_landmarksanity = (
                id_to_landmarksanity()[_args["slot_data"]["landmarksanity"]]
            )

            self.game_controller.option_shuffle_time_tunnels = _args["slot_data"]["shuffle_time_tunnels"] == 1

            self.game_controller.option_entrance_randomizer = (
                id_to_entrance_randomizer()[_args["slot_data"]["entrance_randomizer"]]
            )

            self.game_controller.option_entrance_randomizer_include_subway_destinations = (
                _args["slot_data"]["entrance_randomizer_include_subway_destinations"] == 1
            )

            self.game_controller.option_trap_percentage = _args["slot_data"]["trap_percentage"]

            self.game_controller.option_grant_missable_location_checks = (
                _args["slot_data"]["grant_missable_location_checks"] == 1
            )

            if self.game_controller.option_grant_missable_location_checks and not tracker_loaded:
                CommonClient.logger.info(
                    "Grant Missable Location Checks is enabled but requires Universal Tracker, which isn't installed. "
                    "No missable location checks will be granted."
                )

            self.game_controller.option_client_seed_information = (
                id_to_client_seed_information()[_args["slot_data"]["client_seed_information"]]
            )

            self.game_controller.option_in_game_overlay = (
                id_to_in_game_overlay_options()[_args["slot_data"]["in_game_overlay"]]
            )

            self.game_controller.is_overlay_enabled = (
                self.game_controller.option_in_game_overlay != ZorkGrandInquisitorInGameOverlayOptions.DISABLED
            )

            self.game_controller.is_in_logic_overlay_enabled = (
                self.game_controller.option_in_game_overlay == ZorkGrandInquisitorInGameOverlayOptions.ENABLED_WITH_TRACKER
            )

            is_death_link = _args["slot_data"]["death_link"] == 1

            self.game_controller.option_death_link = is_death_link  # Represents the option; will never change
            self.death_link_status = is_death_link  # Represents the toggleable status

            # Starter Kit
            self.game_controller.starter_kit = _args["slot_data"]["starter_kit"]

            # Initial Totemizer Destination
            self.game_controller.initial_totemizer_destination = item_names_to_item()[
                _args["slot_data"]["initial_totemizer_destination"]
            ]

            # Time Tunnel Destinations
            self.game_controller.time_tunnel_destinations = _args["slot_data"]["time_tunnel_destinations"]

            # Entrance Randomizer Data
            self.game_controller.entrance_randomizer_data = _args["slot_data"]["entrance_randomizer_data"]
            self.entrance_randomizer_data_by_name = _args["slot_data"]["entrance_randomizer_data_by_name"]

            # Save IDs
            self.game_controller.save_ids = tuple(_args["slot_data"]["save_ids"])

            # Data Storage
            self.data_storage_key = f"zork_grand_inquisitor_{self.team}_{self.slot}"

            Utils.async_start(
                self.send_msgs([
                    {
                        "cmd": "Set",
                        "key": self.data_storage_key,
                        "want_reply": True,
                        "default": {
                            "discovered_entrances": list(),
                        },
                        "operations": [
                            {"operation": "default", "value": None},
                        ],
                    },
                    {
                        "cmd": "SetNotify",
                        "keys": [self.data_storage_key],
                    }
                ])
            )

            # Locations Checked
            if "checked_locations" in _args:
                locations_checked: Set[ZorkGrandInquisitorLocations] = set(
                    [self.id_to_locations[location_id] for location_id in _args["checked_locations"]]
                )

                self.game_controller.completed_locations |= locations_checked

            # UI Tabs
            if self.ui:
                self.ui.update_tabs()
        elif cmd == "ReceivedItems":
            if self.ui:
                self.ui.update_tabs()
        elif cmd == "SetReply":
            if _args["key"] == self.data_storage_key and self.ui:
                self.ui.update_tabs()

        super().on_package(cmd, _args)

    def on_print_json(self, args: Dict[str, Any]) -> None:
        if args.get("type") == "ItemSend" and self.game_controller.is_process_running():
            network_item: NetUtils.NetworkItem = args["item"]
            receiving: int = args["receiving"]
            item_name: str = self.item_names.lookup_in_slot(network_item.item, receiving)

            if network_item.player == self.slot and receiving == self.slot:
                self.game_controller.show_toast(f"Found {item_name}")
            elif receiving == self.slot:
                self.game_controller.show_toast(f"Received {item_name} from {self.player_names[network_item.player]}")
            elif network_item.player == self.slot:
                self.game_controller.show_toast(f"Sent {item_name} to {self.player_names[receiving]}")

        super().on_print_json(args)

    def on_deathlink(self, data: Dict[str, Any]) -> None:
        self.last_death_link = max(data["time"], self.last_death_link)
        self.game_controller.pending_death_link = (True, data.get("source"), data.get("cause"))

    async def controller(self):
        while not self.exit_event.is_set():
            await asyncio.sleep(0.1)

            # Enqueue Received Item Delta
            goal_item_count: int = 0

            received_traps: List[ZorkGrandInquisitorItems] = list()

            network_item: NetUtils.NetworkItem
            for network_item in self.items_received:
                item: ZorkGrandInquisitorItems = self.id_to_items[network_item.item]

                if item in self.game_controller.all_goal_items:
                    goal_item_count += 1
                    continue
                elif item in self.game_controller.all_trap_items:
                    received_traps.append(item)
                    continue
                elif item not in self.game_controller.received_items:
                    if item not in self.game_controller.received_items_queue:
                        self.game_controller.received_items_queue.append(item)

            if goal_item_count > self.game_controller.goal_item_count:
                self.game_controller.goal_item_count = goal_item_count
                self.game_controller.output_goal_item_update()

            self.game_controller.received_traps = received_traps

            # Game Controller Update
            if self.game_controller.is_process_running():
                self.game_controller.update()
                self.can_display_process_message = True
            else:
                process_message: str

                if self.process_attached_at_least_once:
                    process_message = (
                        "Connection to the Zork Grand Inquisitor process was lost. Ensure you are connected "
                        "to an Archipelago server and the game is running, then use the /zork command to reconnect."
                    )
                else:
                    process_message = (
                        "To start playing, connect to an Archipelago server and use the /zork command to "
                        "link to an active Zork Grand Inquisitor process."
                    )

                if self.can_display_process_message:
                    CommonClient.logger.info(process_message)
                    self.can_display_process_message = False

            # Network Operations
            if self.server and self.slot:
                # Send Checked Locations
                checked_location_ids: List[int] = list()

                while len(self.game_controller.completed_locations_queue) > 0:
                    location: ZorkGrandInquisitorLocations = self.game_controller.completed_locations_queue.popleft()
                    location_id: int = self.location_name_to_id[location.value]

                    checked_location_ids.append(location_id)

                await self.check_locations(checked_location_ids)

                # Check for Goal Completion
                if self.game_controller.goal_completed and not self.is_goal_sent:
                    await self.send_msgs([
                        {
                            "cmd": "StatusUpdate",
                            "status": CommonClient.ClientStatus.CLIENT_GOAL
                        }
                    ])

                    self.is_goal_sent = True

                # Update Data Storage
                if self.data_storage_key is not None and self.data_storage_key in self.stored_data:
                    update_dict: Dict[str, Any] = dict()

                    current_discovered_entrances: Set[str] = set(
                        self.stored_data[self.data_storage_key]["discovered_entrances"]
                    )

                    update_discovered_entrances: Set[str] = (
                        current_discovered_entrances | self.game_controller.discovered_entrances
                    )

                    if len(update_discovered_entrances) > len(current_discovered_entrances):
                        update_dict["discovered_entrances"] = sorted(update_discovered_entrances)

                    if len(update_dict):
                        await self.send_msgs([
                            {
                                "cmd": "Set",
                                "key": self.data_storage_key,
                                "want_reply": True,
                                "operations": [
                                    {"operation": "update", "value": update_dict},
                                ],
                            }
                        ])

                # Handle Energy Link
                while len(self.game_controller.energy_link_queue) > 0:
                    energy_to_add: int = self.game_controller.energy_link_queue.popleft()

                    await self.send_msgs([
                        {
                            "cmd": "Set",
                            "key": f"EnergyLink{self.team}",
                            "operations":
                                [
                                    {"operation": "add", "value": energy_to_add},
                                ],
                        },
                    ])

                    CommonClient.logger.info(f"Added {energy_to_add} J to the Energy Link pool")

                # Handle Death Link
                await self.update_death_link(self.death_link_status)

                if self.game_controller.outgoing_death_link[0]:
                    if self.death_link_status:
                        death_cause: Optional[str] = self.game_controller.outgoing_death_link[1]

                        if death_cause:
                            death_cause = death_cause.replace(
                                "PLAYER",
                                self.player_names[self.slot]
                            )
                        else:
                            death_cause = ""

                        await self.send_death(death_cause)

                    self.game_controller.outgoing_death_link = (False, None)


def main(*args) -> None:
    Utils.init_logging("ZorkGrandInquisitorClient", exception_logger="Client")

    parser = CommonClient.get_base_parser(description="Zork Grand Inquisitor Client")

    parser.add_argument("url", nargs="?", help="Archipelago Connection URL")
    parser.add_argument("--name", default=None, help="Archipelago Slot Name")

    args = parser.parse_args(args)

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    async def _main(_args):
        ctx: ZorkGrandInquisitorContext = ZorkGrandInquisitorContext(_args.connect, _args.password)
        ctx.auth = _args.name

        ctx.server_task = asyncio.create_task(CommonClient.server_loop(ctx), name="server loop")
        ctx.controller_task = asyncio.create_task(ctx.controller(), name="ZorkGrandInquisitorController")

        if tracker_loaded:
            ctx.run_generator()

        if CommonClient.gui_enabled:
            ctx.run_gui()

        ctx.run_cli()

        await ctx.exit_event.wait()
        await ctx.shutdown()

    import colorama

    colorama.just_fix_windows_console()

    asyncio.run(_main(args))

    colorama.deinit()


if __name__ == "__main__":
    main(*sys.argv[1:])

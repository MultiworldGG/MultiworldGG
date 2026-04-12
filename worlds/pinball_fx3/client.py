import asyncio
import sys
import urllib.parse

import CommonClient
import NetUtils
import Utils

from typing import Any, Dict, List, Optional, Set

from .data_funcs import (
    item_names_to_id,
    location_names_to_id,
    id_to_exclude_high_tier_challenge_stars,
    id_to_goals,
    id_to_items,
    id_to_locations,
    id_to_requirement_modes,
)

from .enums import PinballFX3APUsefulItems, PinballFX3Tables
from .game_controller import GameController


class PinballFX3CommandProcessor(CommonClient.ClientCommandProcessor):
    ctx: "PinballFX3Context"


class PinballFX3Context(CommonClient.CommonContext):
    tags: Set[str] = {"AP"}
    game: str = "Pinball FX3"
    command_processor: CommonClient.ClientCommandProcessor = PinballFX3CommandProcessor
    items_handling: int = 0b111
    want_slot_data: bool = True

    item_name_to_id: Dict[str, int] = item_names_to_id()
    location_name_to_id: Dict[str, int] = location_names_to_id()

    id_to_items: Dict[int, str] = id_to_items()
    id_to_locations: Dict[int, str] = id_to_locations()

    game_controller: GameController
    data_storage_key: Optional[str]

    controller_task: Optional[asyncio.Task]

    seen_item_indices: Set[int] = set()

    can_display_process_found_message: bool
    can_display_process_not_found_message: bool

    shiny_quarters_total: int
    shiny_quarters_required: int

    target_score_ratios: Dict[PinballFX3Tables, float]

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)

        self.game_controller = GameController(logger=CommonClient.logger)

        self.data_storage_key = None

        self.controller_task = None

        self.seen_item_indices = set()

        self.can_display_process_found_message = True
        self.can_display_process_not_found_message = True

        self.shiny_quarters_total = 0
        self.shiny_quarters_required = 0

        self.target_score_ratios = dict()

    def make_gui(self):
        from .client_gui.client_gui import PinballFX3Manager
        return PinballFX3Manager

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

        self.items_received = list()
        self.locations_info = dict()

        self.seen_item_indices = set()

        self.can_display_process_found_message = True
        self.can_display_process_not_found_message = True

        self.shiny_quarters_total = 0
        self.shiny_quarters_required = 0

        self.target_score_ratios = dict()

        self.ui.update_tabs()

        await super().disconnect(allow_autoreconnect)

    def on_package(self, cmd: str, _args: Any) -> None:
        if cmd == "Connected":
            self.game = self.slot_info[self.slot].game

            # Options
            self.game_controller.option_goal = id_to_goals()[_args["slot_data"]["goal"]]

            self.game_controller.option_shiny_quarters_total = _args["slot_data"]["shiny_quarters_total"]
            self.game_controller.option_shiny_quarters_required = _args["slot_data"]["shiny_quarters_required"]

            self.shiny_quarters_total = _args["slot_data"]["shiny_quarters_total"]
            self.shiny_quarters_required = _args["slot_data"]["shiny_quarters_required"]

            self.game_controller.option_pinball_table_selection = _args["slot_data"]["pinball_table_selection"]
            self.game_controller.option_pinball_table_count = _args["slot_data"]["pinball_table_count"]

            self.game_controller.option_exclude_high_tier_target_scores = _args["slot_data"]["exclude_high_tier_target_scores"]

            self.game_controller.option_target_score_requirement_mode = id_to_requirement_modes()[
                _args["slot_data"]["target_score_requirement_mode"]
            ]

            self.game_controller.option_target_score_requirement_percentage = _args["slot_data"][
                "target_score_requirement_percentage"
            ]

            self.game_controller.option_progressive_challenge_access = _args["slot_data"]["progressive_challenge_access"]

            self.game_controller.option_exclude_high_tier_challenge_stars = id_to_exclude_high_tier_challenge_stars()[
                _args["slot_data"]["exclude_high_tier_challenge_stars"]
            ]

            self.game_controller.option_challenge_star_requirement_mode = id_to_requirement_modes()[
                _args["slot_data"]["challenge_star_requirement_mode"]
            ]

            self.game_controller.option_challenge_low_tier_star_requirement = _args["slot_data"][
                "challenge_low_tier_star_requirement"
            ]

            self.game_controller.option_challenge_mid_tier_star_requirement = _args["slot_data"][
                "challenge_mid_tier_star_requirement"
            ]

            self.game_controller.option_challenge_high_tier_star_requirement = _args["slot_data"][
                "challenge_high_tier_star_requirement"
            ]

            self.game_controller.option_starsanity = _args["slot_data"]["starsanity"]
            self.game_controller.option_useful_item_percentage = _args["slot_data"]["useful_item_percentage"]

            self.game_controller.option_useful_item_weights = _args["slot_data"]["useful_item_weights"] = {
                PinballFX3APUsefulItems(item_name): weight for item_name, weight in _args["slot_data"]["useful_item_weights"].items()
            }

            self.game_controller.selected_starting_table = PinballFX3Tables(_args["slot_data"]["selected_starter_table"])

            self.game_controller.selected_tables = [
                PinballFX3Tables(table_name) for table_name in _args["slot_data"]["selected_tables"]
            ]

            if _args["slot_data"].get("selected_goal_table") is not None:
                self.game_controller.selected_goal_table = PinballFX3Tables(_args["slot_data"]["selected_goal_table"])

            self.game_controller.target_scores = {
                PinballFX3Tables(table_name): scores for table_name, scores in _args["slot_data"]["target_scores"].items()
            }

            self.game_controller.challenge_stars = {
                PinballFX3Tables(table_name): stars for table_name, stars in _args["slot_data"]["challenge_stars"].items()
            }

            # Metadata
            self.target_score_ratios = {
                PinballFX3Tables(table_name): ratio for table_name, ratio in _args["slot_data"]["target_score_ratios"].items()
            }

            # Assemble Locations + Initialize Useful Items
            self.game_controller.assemble_single_player_locations()
            self.game_controller.assemble_challenge_locations()

            self.game_controller.initialize_useful_items()

            # Data Storage
            self.data_storage_key = f"pinball_fx3_{self.team}_{self.slot}"

            # Playing Status
            Utils.async_start(
                self.send_msgs([
                    {
                        "cmd": "StatusUpdate",
                        "status": CommonClient.ClientStatus.CLIENT_PLAYING
                    }
                ])
            )

            # UI Tabs
            self.ui.update_tabs()

    async def controller(self):
        while not self.exit_event.is_set():
            await asyncio.sleep(0.2)

            # Enqueue Received Item Delta
            i: int
            network_item: NetUtils.NetworkItem
            for i, network_item in enumerate(self.items_received):
                if i in self.seen_item_indices:
                    continue

                item: str = self.id_to_items[network_item.item]

                self.game_controller.received_items_queue.append(item)
                self.seen_item_indices.add(i)

            # Network Operations
            if self.server and self.slot:
                # Game Controller Update
                if not self.game_controller.is_process_running():
                    if not self.game_controller.open_process_handle():
                        if self.can_display_process_not_found_message:
                            CommonClient.logger.info("Looking for Pinball FX3 process...")

                            self.can_display_process_found_message = True
                            self.can_display_process_not_found_message = False

                if self.game_controller.is_process_running():
                    if self.can_display_process_found_message:
                        CommonClient.logger.info("Pinball FX3 process found!")

                        self.can_display_process_found_message = False
                        self.can_display_process_not_found_message = True

                    self.game_controller.update()

                # Send Checked Locations
                checked_location_ids: List[int] = list()

                while len(self.game_controller.completed_locations_queue) > 0:
                    location: str = self.game_controller.completed_locations_queue.popleft()
                    location_id: int = self.location_name_to_id[location]

                    checked_location_ids.append(location_id)

                await self.check_locations(checked_location_ids)

                # Check for Goal Completion
                if self.game_controller.goal_completed:
                    await self.send_msgs([
                        {
                            "cmd": "StatusUpdate",
                            "status": CommonClient.ClientStatus.CLIENT_GOAL
                        }
                    ])


def main(*args) -> None:
    Utils.init_logging("PinballFX3Client", exception_logger="Client")

    parser = CommonClient.get_base_parser(description="Pinball FX3 Client")

    parser.add_argument("url", nargs="?", help="Archipelago Connection URL")
    parser.add_argument('--name', default=None, help="Archipelago Slot Name")

    args = parser.parse_args(args)

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    async def _main(_args):
        ctx: PinballFX3Context = PinballFX3Context(args.connect, args.password)

        ctx.server_task = asyncio.create_task(CommonClient.server_loop(ctx), name="server loop")
        ctx.controller_task = asyncio.create_task(ctx.controller(), name="PinballFX3Controller")

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

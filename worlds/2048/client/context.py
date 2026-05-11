import asyncio
from typing import Any

import kvui
from CommonClient import CommonContext
from NetUtils import ClientStatus, NetworkItem

from ..world import TwoThousandAndFortyEightWorld
from .game import TwoThousandAndFortyEightGame
from .game_manager import TwoThousandAndFortyEightManager


class TwoThousandAndFortyEightContext(CommonContext):
    game = "2048"
    items_handling = 0b111  # full remote
    connected = False
    current_seed = None

    client_loop: asyncio.Task[None]
    game_logic: TwoThousandAndFortyEightGame | None
    highest_processed_item_index: int = 0

    ui: TwoThousandAndFortyEightManager

    def __init__(self, server_address: str | None = None, password: str | None = None) -> None:
        super().__init__(server_address, password)
        self.game_logic = None

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    async def client_logic_loop(self) -> None:
        while not self.exit_event.is_set():
            await asyncio.sleep(0.5)
            if not self.connected:
                continue

            assert self.game_logic is not None
            await self.check_locations(self.game_logic.checked_locations)

            rerender = False

            new_items = self.items_received[self.highest_processed_item_index :]
            for item in new_items:
                self.highest_processed_item_index += 1
                self.game_logic.receive_item(item.item)
                rerender = True
                if item.player == self.slot:
                    location_name = TwoThousandAndFortyEightWorld.location_id_to_name[item.location]
                    self.ui.game_view.show_popup(
                        f"Found {TwoThousandAndFortyEightWorld.item_id_to_name[item.item]} ({location_name})"
                    )
                else:
                    location_name = self.location_names.lookup_in_slot(item.location, item.player)
                    player_name = self.player_names[item.player]
                    self.ui.game_view.show_popup(
                        f"Received {TwoThousandAndFortyEightWorld.item_id_to_name[item.item]} from {player_name} "
                        f"({location_name})"
                    )

            if rerender:
                self.render()

            if not self.finished_game and self.game_logic.got_2048:
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                self.finished_game = True

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Connected":
            seed = f"{self.seed_name}|{self.player_names[self.slot]}"
            if self.current_seed != seed:
                game = TwoThousandAndFortyEightGame(self.missing_locations)
                self.game_logic = game
                self.ui.set_game(game)
                self.highest_processed_item_index = 0
                self.current_seed = seed
            self.connected = True
            self.render()
        if cmd == "Connected" or cmd == "RoomUpdate":
            assert self.game_logic is not None
            new_locations = self.checked_locations.difference(self.game_logic.checked_locations)
            if new_locations:
                self.game_logic.checked_locations.update(new_locations)
                new_scores = new_locations.intersection(self.game_logic.unmet_score_thresholds)
                if new_scores:
                    for score_goal in new_scores:
                        self.game_logic.unmet_score_thresholds.remove(score_goal)

                self.render()
                self.ui.game_view.update_score(self.game_logic.score)

    def on_print_json(self, args: dict[str, Any]) -> None:
        super().on_print_json(args)

        if args.get("type") == "ItemSend":
            item: NetworkItem = args["item"]
            if item.player == self.slot and args["receiving"] != self.slot:
                item_name = self.item_names.lookup_in_slot(item.item, args["receiving"])
                receiving_player_name = self.player_names[args["receiving"]]
                location_name = TwoThousandAndFortyEightWorld.location_id_to_name[item.location]
                self.ui.game_view.show_popup(f"Sent {item_name} to {receiving_player_name} ({location_name})")

    async def disconnect(self, *args: Any, **kwargs: Any) -> None:
        self.finished_game = False
        self.connected = False
        await super().disconnect(*args, **kwargs)

    def render(self) -> None:
        if hasattr(self, "ui") and self.ui:
            self.ui.render(self.game_logic)

    def input_and_rerender(self, input_key: Any) -> None:
        if self.game_logic is not None and self.game_logic.input(input_key):
            self.ui.game_view.update_score(self.game_logic.score)
            self.render()

    def make_gui(self) -> "type[kvui.GameManager]":
        return TwoThousandAndFortyEightManager

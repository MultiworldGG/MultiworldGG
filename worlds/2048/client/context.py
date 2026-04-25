import asyncio
from typing import Any

import kvui
from CommonClient import CommonContext
from NetUtils import ClientStatus

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
            await self.check_locations(self.game_logic.checked_locations)

            rerender = False

            new_items = self.items_received[self.highest_processed_item_index:]
            for item in new_items:
                self.highest_processed_item_index += 1
                self.game_logic.receive_item(item.item)
                rerender = True

            if rerender:
                self.render()

            if 2048 in self.game_logic.checked_locations and not self.finished_game:
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                self.finished_game = True

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "RoomInfo":
            if self.current_seed != args["seed_name"]:
                self.game_logic = TwoThousandAndFortyEightGame()
            self.connected = True
            self.render()

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
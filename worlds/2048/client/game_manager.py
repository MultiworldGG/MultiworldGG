from typing import TYPE_CHECKING

from kivy.uix.layout import Layout

from kvui import GameManager

from .game import TwoThousandAndFortyEightGame
from .game_view import TwoThousandAndFortyEightGameView
from .tile import TileWidget

if TYPE_CHECKING:
    from .context import TwoThousandAndFortyEightContext

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "AP"

class TwoThousandAndFortyEightManager(GameManager):
    base_title = f"2048 {apname} Client"
    ctx: "TwoThousandAndFortyEightContext"

    game_view: TwoThousandAndFortyEightGameView
    tile_widgets: list[list[TileWidget]]

    def render(self, game: TwoThousandAndFortyEightGame | None) -> None:
        if not self.game_view:
            return
        for x in range(4):
            for y in range(4):
                if game is None:
                    val = 0
                else:
                    val = game.grid[x][y]
                self.tile_widgets[x][y].set_value(val)

    def build(self) -> Layout:
        container = super().build()
        game_view = TwoThousandAndFortyEightGameView(self.ctx.input_and_rerender)
        self.game_view = game_view
        self.tile_widgets = []
        for _ in range(4):
            row = []
            for _ in range(4):
                tile = TileWidget()
                self.game_view.grid_layout.add_widget(tile)
                row.append(tile)
            self.tile_widgets.append(row)

        self.add_client_tab("2048 Game", game_view)
        self.render(None)
        return container

    def set_game(self, game: TwoThousandAndFortyEightGame):
        self.game_view.game = game
        self.game_view.update_score(0)
        for tile_list in self.tile_widgets:
            for tile in tile_list:
                tile.game = game

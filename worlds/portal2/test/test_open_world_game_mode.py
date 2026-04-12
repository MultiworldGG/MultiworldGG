from .bases import Portal2TestBase
from .test_normal_game_mode import NormalGameMode
from ..Options import GameModeOption


class OpenWorldGameMode(NormalGameMode):
    options = {
        "game_mode": GameModeOption.OPEN_WORLD
    }

from .bases import Portal2TestBase
from .test_normal_game_mode import NormalGameMode
from ..Options import GameModeOption


class ChaoticGameMode(NormalGameMode):
    options = {
        "game_mode": GameModeOption.CHAOTIC
    }

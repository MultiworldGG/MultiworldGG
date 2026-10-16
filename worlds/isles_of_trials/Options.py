import typing
from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

class PlayerSprite(Choice):
    """
    Which character to play as. They are functionally identical.
    """

    display_name = "Player Sprite"

    option_slash = 0
    option_misty = 1

    default = option_slash

@dataclass
class IslesTrialsOptions(PerGameCommonOptions):
    player_sprite: PlayerSprite
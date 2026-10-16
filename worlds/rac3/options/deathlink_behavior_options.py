"""This module contains options for how Deathlink is handled in the world."""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class DeathlinkBehavior(Choice):
    """
    Determines how the player is affected by a Deathlink.
    ---------------------------------------------------------------------------------------------------------
    Instant Kill: The player is killed immediately.
    Nanopak Save: The Nanopak can save the player from the Deathlink.
    ---------------------------------------------------------------------------------------------------------
    This option has no effect if Deathlink is disabled.
    """
    display_name = RAC3OPTION.DEATHLINK_BEHAVIOR
    option_instant_kill = 0
    option_nanopak_save = 1
    default = 0
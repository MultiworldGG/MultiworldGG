"""This module contains options for trap items in the item pool"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class EnableTraps(Toggle):
    """
    Determines whether trap items are included in the item pool.
    ------------------------------------------------------------
    No:   No traps will be included in the item pool.
    Yes:  Traps will be included in the item pool.
    ------------------------------------------------------------
    """
    display_name = RAC3OPTION.ENABLE_TRAPS

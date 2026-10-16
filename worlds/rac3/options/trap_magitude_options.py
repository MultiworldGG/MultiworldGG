"""This module contains options for the magnitude of traps in the item pool"""

from Options import ItemDict
from worlds.rac3.constants.data.item import trap_data, trap_magnitude_data
from worlds.rac3.constants.options import RAC3OPTION


class TrapMagnitude(ItemDict):
    """
    Sets the duration/impact of trap items in the item pool.
    A higher value increases the duration in seconds of a timed trap or the impact up to 100% of a non-timed trap.
    This option has no effect when traps are disabled.

    Min value is 1, max value is 300.
    """
    display_name = RAC3OPTION.TRAP_MAGNITUDE
    min = 1
    max = 300
    valid_keys = trap_data.keys()
    default = {k: v for k, v in trap_magnitude_data.items() if k in trap_data.keys()}

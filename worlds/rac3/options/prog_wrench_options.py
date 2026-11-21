"""This module contains options for the Progressive OmniWrench in the item pool"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class ProgressiveWrench(Toggle):
    """
    Determines if Progressive OmniWrench items are included in the item pool.
    ------------------------------------------------------------------------------------
    Disable for the vanilla OmniWrench behaviour.
    Enable for OmniWrench upgrades to be included in the item pool.
    ------------------------------------------------------------------------------------
    Note: Experimental feature. You will start with no wrench.
    May occasionally crash PCSX2 when landing on a planet,
    possibly due to a race condition between our instruction patching and PCSX2's recompiler.
    """
    display_name = RAC3OPTION.PROGRESSIVE_WRENCH

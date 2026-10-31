"""This module contains options for what part of the endgame is restricted by completion conditions"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class LockCommandCenter(Toggle):
    """
    Determines if completing all conditions unlocks the Planet Command Center
    --------------------------------------------------------------------------------------
    No:   Completing all conditions will unlock the dropship on Command Center
    Yes:  Completing all conditions will unlock the Command Center Infobot
    ---------------------------------------------------------------------------------------
    Biobliterator and Dr Nefarious goal conditions are never required to activate either the dropship or the infobot
    """
    display_name = RAC3OPTION.LOCK_CC

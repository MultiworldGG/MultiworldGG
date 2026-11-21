"""This module contains options for what part of the endgame is restricted by completion conditions"""

from Options import Toggle
from worlds.rac3.constants.options import RAC3OPTION


class LockCommandCenter(Toggle):
    """
    Determines if completing all conditions unlocks the Planet Command Center
    --------------------------------------------------------------------------------------
    No:   The Command Center Infobot is shuffled into the item pool like any other planet, so Command Center can be
          visited before the other conditions are completed
    Yes:  Completing all conditions will unlock the Command Center Infobot. Locations on Command Center, and the
          Insomniac Museum condition, are not counted towards the other conditions
    ---------------------------------------------------------------------------------------
    The Command Center Infobot is only locked when Dr Nefarious or the Biobliterator is a goal condition. They are
    never required to unlock it
    """
    display_name = RAC3OPTION.LOCK_CC

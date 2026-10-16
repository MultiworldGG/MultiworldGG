"""This module contains options for toggling generation behavior"""

from Options import Choice
from worlds.rac3.constants.options import RAC3OPTION


class GenerationBehavior(Choice):
    """
    Determines how generation should handle too many items and not enough locations.
    ------------------------------------------------------------------------------
    Error: Generation will return an OptionError indicating the options to change to improve generation.
    Start Inventory:  Generation will place the extra items into your starting inventory.
    ------------------------------------------------------------------------------
    """
    display_name = RAC3OPTION.GENERATION_BEHAVIOR
    option_error = 0
    option_start_inventory = 1
    default = 1

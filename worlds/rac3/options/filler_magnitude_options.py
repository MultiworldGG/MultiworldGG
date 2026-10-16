"""This module contains options for the magnitude of filler items in the item pool"""

from Options import ItemDict
from worlds.rac3.constants.data.item import filler_data, filler_magnitude_data
from worlds.rac3.constants.options import RAC3OPTION


class FillerMagnitude(ItemDict):
    """
    Sets the duration/impact of filler items in the item pool.
    A higher value increases the duration in seconds of jackpot or the percentage of bolts or nanotech XP gained.
    Bolts and nanotech are still capped at 200,000 and 300,000 per filler respectively,
    but a higher value will increase the amount gained up to that cap.

    Min value is 1, max value is 300.
    """
    display_name = RAC3OPTION.FILLER_MAGNITUDE
    min = 1
    max = 300
    valid_keys = filler_data.keys()
    default = {k: v for k, v in filler_magnitude_data.items() if k in filler_data.keys()}

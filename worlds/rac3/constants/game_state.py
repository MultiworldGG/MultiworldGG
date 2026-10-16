"""This module defines the possible game states that can be read from memory"""
from enum import IntEnum


class RAC3GAMESTATE(IntEnum):
    """Enum for the possible game states in single player of rac3"""
    INVALID = -1
    UNPAUSED = 0
    MOVIE = 1
    CUTSCENE = 2
    PAUSED = 3
    QUICK_SELECT = 4
    VENDOR = 5
    PLANET_CHANGE = 6
    MINIGAME = 7
    WEAPON_UPGRADE = 8
    CREDITS = 9

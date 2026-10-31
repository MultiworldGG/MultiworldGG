"""This module contains options for how many planets are required to be completed to goal"""

from Options import Range
from worlds.rac3.constants.options import RAC3OPTION


class GoalPlanets(Range):
    """
    Determines how many Planets must be completed to goal. 0 - 16
    -----------------------------------------------------------------------------------------------
    These are the following conditions for a "Planet Completion"
    - Florana: Defeat Qwark
    - Marcadia: Find Al
    - Annihilation Nation: Grand Prize Bout AND Meet Courtney Gears
    - Aquatos: Infiltrate the Nefarious Base
    - Tyhrranosis: Destroy the Momma Tyhrranoid
    - Daxx: Infiltrate the Weapon Facility AND Defeat the Warship
    - Obani Gemini: Meet Skidd
    - Blackwater City: Mission 3
    - Holostar Studios: Return to your ship
    - Obani Draco: Defeat Courtney Gears
    - Zeldrin Starport: Escape the Exploding Ship
    - Metropolis: Defeat Klunk
    - Crash Site: Escape Pod
    - Aridia: Mission 5
    - Qwarks Hideout: Find Qwark
    - Koros: Fire the Cannon
    -----------------------------------------------------------------------------------------------
    Any planet completions that require options that have been disabled will not be expected to be required.
    """

    display_name = RAC3OPTION.GOAL_PLANETS
    range_start = 0
    range_end = 16
    default = 0

"""This module contains options for Skill Point Pick and Mix"""

from Options import OptionSet
from worlds.rac3.constants.options import RAC3OPTION


class SkillPointsPickAndMix(OptionSet):
    """
    Determines which skill points should be locations when pick_and_mix is selected for skill_points.
    Any Skill Points locked behind other locations such as Ranger Missions require those options to be enabled.
    Example: ["Reflect on how to score", "Pirate booty - set a new record for Qwark"]
    -----------------------------------------------------------------------------------------------
    The valid keys are the following:
    - Stay Squeaky Clean
    - Beat Helga's best time
    - Turn Up The Heat
    - Monkeying Around
    - Reflect on how to score
    - Bash the bug
    - Be an eight time champ
    - Flee Flawlessly
    - Lights, camera, action!
    - Search for sunken treasure
    - Hit the motherload
    - Be a sharpshooter
    - Bugs to Birds
    - Get to the belt
    - Bash the party
    - Feeling Lucky?
    - 2002 was a good year in the city
    - Suck it up!
    - Aim High
    - Zap back at ya'
    - Go for hang time
    - Break the Dan
    - You break it, you win it
    - Spread your germs
    - Strive for arcade perfection
    - Pirate booty - set a new record for Qwark
    - Deja Q All over Again - set a new record for Qwark
    - Arriba Amoeba! - set a new record for Qwark
    - Shadow of the robot - set a new record for Qwark
    - The Shaming of the Q - set a new record for Qwark
    """
    display_name = RAC3OPTION.SKILL_POINTS_PICK_AND_MIX
    valid_keys = frozenset({
        "Go for hang time",
        "Stay Squeaky Clean",
        "Strive for arcade perfection",
        "Beat Helga's best time",
        "Turn Up The Heat",
        "Monkeying Around",
        "Reflect on how to score",
        "Bugs to Birds",
        "Bash the bug",
        "Be an eight time champ",
        "Flee Flawlessly",
        "Lights, camera, action!",
        "Search for sunken treasure",
        "Be a sharpshooter",
        "Get to the belt",
        "Bash the party",
        "Feeling Lucky?",
        "You break it, you win it",
        "2002 was a good year in the city",
        "Suck it up!",
        "Aim High",
        "Zap back at ya'",
        "Break the Dan",
        "Spread your germs",
        "Hit the motherload",
        "Pirate booty - set a new record for Qwark",
        "Deja Q All over Again - set a new record for Qwark",
        "Arriba Amoeba! - set a new record for Qwark",
        "Shadow of the robot - set a new record for Qwark",
        "The Shaming of the Q - set a new record for Qwark"
    })
    default = frozenset()

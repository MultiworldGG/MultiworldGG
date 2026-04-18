import json
from enum import auto, IntFlag
from pkgutil import get_data

from BaseClasses import ItemClassification

_MANIFEST = json.loads(get_data("worlds.lego_star_wars_tcs", "archipelago.json"))

GAME_NAME = _MANIFEST["game"]

_MAJOR, _MINOR, _PATCH = map(int, _MANIFEST["world_version"].split("."))
AP_WORLD_VERSION: tuple[int, int, int] = (_MAJOR, _MINOR, _PATCH)
del _MANIFEST
# Logic version, used for Universal Tracker compatibility across patch versions.
UT_LOGIC_VERSION = 1


# todo: These are the abilities from the manual logic, not the real abilities.
class CharacterAbility(IntFlag):
    NONE = 0
    ASTROMECH = auto()
    # todo: This will eventually need to be split into separate Grapple and Blaster.
    BLASTER = auto()
    BOUNTY_HUNTER = auto()
    HOVER = auto()
    HIGH_JUMP = auto()
    IMPERIAL = auto()
    JEDI = auto()
    PROTOCOL_DROID = auto()
    SHORTIE = auto()
    SITH = auto()
    # Relevant for some Imperial access and 6-1 Bounty Hunter access.
    CAN_WEAR_HAT = auto()
    # CAN_WEAR_HAT + BLASTER (grapple) on a single character.
    CAN_WEAR_HAT_AND_GRAPPLE = auto()
    # CAN_WEAR_HAT + JEDI on a single character.
    CAN_WEAR_HAT_AND_DOUBLE_JUMP = auto()
    CAN_RIDE_VEHICLES = auto()
    CAN_PULL_LEVERS = auto()
    CAN_PUSH_OBJECTS = auto()  # Blocks and Spinners
    CAN_BUILD_BRICKS = auto()
    CAN_JUMP_NORMALLY = auto()  # Has at least a basic jump
    CAN_ATTACK_UP_CLOSE = auto()
    CAN_DAGOBAH_SWAMP = auto()  # Basically just "this character is an Astromech Droid"
    # todo: Lots more abilities to add to split up and replace the basic existing ones...
    # GHOST = auto()
    # DROID = auto()
    # UNTARGETABLE = auto()  # Are there any characters other than Ghosts?
    IS_A_VEHICLE = auto()
    VEHICLE_TIE = auto()
    VEHICLE_TOW = auto()
    VEHICLE_BLASTER = auto()


# Workaround for Python 3.10 support. Iterating Flag instances was only added in Python 3.11.
# There is probably a better way to do this, but it will get the job done.
if getattr(CharacterAbility.NONE, "__iter__", None) is None:
    def __iter__(self: CharacterAbility):
        none_flag = CharacterAbility.NONE
        for flag in CharacterAbility:
            if flag is not none_flag and flag in self:
                yield flag
    CharacterAbility.__iter__ = __iter__  # type: ignore
    del __iter__


ASTROMECH = CharacterAbility.ASTROMECH
BLASTER = CharacterAbility.BLASTER
BOUNTY_HUNTER = CharacterAbility.BOUNTY_HUNTER
HOVER = CharacterAbility.HOVER
HIGH_JUMP = CharacterAbility.HIGH_JUMP
IMPERIAL = CharacterAbility.IMPERIAL
JEDI = CharacterAbility.JEDI
PROTOCOL_DROID = CharacterAbility.PROTOCOL_DROID
SHORTIE = CharacterAbility.SHORTIE
SITH = CharacterAbility.SITH
VEHICLE_TIE = CharacterAbility.VEHICLE_TIE
VEHICLE_TOW = CharacterAbility.VEHICLE_TOW
VEHICLE_BLASTER = CharacterAbility.VEHICLE_BLASTER

# Chapter-specific flags.
CAN_WEAR_HAT = CharacterAbility.CAN_WEAR_HAT
CAN_WEAR_HAT_AND_GRAPPLE = CharacterAbility.CAN_WEAR_HAT_AND_GRAPPLE
CAN_WEAR_HAT_AND_DOUBLE_JUMP = CharacterAbility.CAN_WEAR_HAT_AND_DOUBLE_JUMP
CAN_DAGOBAH_SWAMP = CharacterAbility.CAN_DAGOBAH_SWAMP
IS_A_VEHICLE = CharacterAbility.IS_A_VEHICLE

# Extremely common ability flags.
CAN_RIDE_VEHICLES = CharacterAbility.CAN_RIDE_VEHICLES
CAN_PULL_LEVERS = CharacterAbility.CAN_PULL_LEVERS
CAN_PUSH_OBJECTS = CharacterAbility.CAN_PUSH_OBJECTS
CAN_BUILD_BRICKS = CharacterAbility.CAN_BUILD_BRICKS
CAN_JUMP_NORMALLY = CharacterAbility.CAN_JUMP_NORMALLY
CAN_ATTACK_UP_CLOSE = CharacterAbility.CAN_ATTACK_UP_CLOSE

# todo: VEHICLE_TOW can probably be included in the future too.
# todo: GHOST can probably be included in the future too.
# todo: PROTOCOL_DROID_PANEL can probably be included in the future too.
RARE_AND_USEFUL_ABILITIES = ASTROMECH | BOUNTY_HUNTER | HIGH_JUMP | SHORTIE | SITH | PROTOCOL_DROID | HOVER

CHAPTER_SPECIFIC_FLAGS = (
        CAN_WEAR_HAT_AND_GRAPPLE
        | CAN_WEAR_HAT_AND_DOUBLE_JUMP
        | CAN_WEAR_HAT
        | CAN_DAGOBAH_SWAMP
        | IS_A_VEHICLE
        # Commander Cody in 3-3 and Darth Vader in 6-5 have IMPERIAL, but IMPERIAL is not needed to complete either
        # chapter. In 6-5, it is at least used for the Minikits.
        | IMPERIAL
        # SITH could be included here, but there is only 6-5 with a SITH Story character, and SITH is needed to
        # complete 6-5.
)
"""
These flags should not be required to access chapters based on the abilities of the Story characters because they are
only relevant to a limited number of chapters, where there are alternatives that the logic should consider.
"""

GOLD_BRICK_EVENT_NAME = "Gold Brick"

if AP_WORLD_VERSION >= (2, 0, 0):
    raise Exception("Deprecation: Use ItemClassification.progression_deprioritized_skip_balancing directly.")
# Use deprioritzed on AP 0.6.3+, but still allow generation on older AP versions.
progression_deprioritized_skip_balancing: ItemClassification = getattr(
    ItemClassification,
    "progression_deprioritized_skip_balancing",
    ItemClassification.progression_skip_balancing
)
progression_deprioritized: ItemClassification = getattr(
    ItemClassification,
    "progression_deprioritized",
    ItemClassification.progression
)

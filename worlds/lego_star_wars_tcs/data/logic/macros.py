from rule_builder.rules import True_, Or, False_, And, HasFromListUnique

from .option_filters import logic_options, OT_HIGH_JUMP_ENABLED
from .rules import HasAbility, HasAnyAbilities, HasAbilityExceptCharacters, HasSingleJumpDistance, HasAnyCharacterExcept
from ..characters import Character
from ..extras import Extra
from ..items.character_items import NON_VEHICLE_CHARACTER_TO_ITEM_DATA
from ..items.vehicle_items import VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from ...character_ability import *

__all__ = [
    "CAN_USE_SELF_DESTRUCT",
    "CAN_SUPER_EWOK_CATAPULT",
    "HAS_FLUTTER_CHARACTER",
    "CAN_JUMP_DISTANCE_0_56_BOBA_BOY_PLUS",
    "CAN_JUMP_DISTANCE_0_7_CLONE_PLUS",
    "CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS",
    "CAN_JUMP_DISTANCE_0_904_LANDO_PLUS",
    "CAN_SITH_FORCE",
    "CAN_DESTROY_CLOSE_SILVER_BRICKS",
    "CAN_USE_DEFLECT_BOLTS",
    "CAN_SUPER_ZAP",
    "CAN_DAMAGE_AT_CLOSE_RANGE",
    "CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT",
    "CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE",
    "CAN_DAMAGE_SHIELDED_DROIDEKA",
    "CAN_DESTROY_FAR_SILVER_BRICKS",
    "CAN_GRAPPLE",
    "CAN_SITH_FORCE_AND_GRAPPLE",
    "CAN_FIGHT_OR_BYPASS_SKIPPABLE_DROIDEKA",
    "CAN_ACTIVATE_CLOSE_TARGET",
    "CAN_ORIGINAL_TRILOGY_HIGH_JUMP",
    "CAN_USE_BOUNTY_HUNTER_ROCKETS",
    "HAS_ANY_YODA",
    "CAN_YODA_CLIP",
    "CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS",
    "MODERATE_PLUS",
    "HAS_DOUBLE_JUMP_EXCEPT_ACKBAR",
    "HAS_P2_AI_DOUBLE_JUMP",
    "HAS_EXTRA_DISTANCE_DOUBLE_JUMP",
    "HAS_GAS_IMMUNE",
    "HAS_GAS_IMMUNE_EXCEPT_GHOSTS",
    "HAS_CAN_REFLECT_BLASTER_BOLTS",
    "HAS_HIGH_JUMP_EXCEPT_BODYGUARD",
    "HAS_HIGH_JUMP_EXCEPT_BODYGUARD_OT",
    "HAS_WALL_CLIMB",
    "HAS_0_53_JUMP_HEIGHT_CHARACTER",
    "HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE",
    "HAS_CAN_WEAR_HAT_AND_GRAPPLE",
    "HAS_VEHICLE_LEVEL_CHARACTER_SWAPPING",
]

# Implemented as a CharacterAbility for now.
# can_jetpack_hover = Character.has_any(Character.BOBA_FETT, Character.JANGO_FETT)
CAN_USE_SELF_DESTRUCT = logic_options(
    base=False_(),
    normal=HasAbility(CAN_SELF_DESTRUCT) & Extra.SELF_DESTRUCT.has(),
)
CAN_SUPER_EWOK_CATAPULT = logic_options(
    base=False_(),
    normal=HasAbility(WEAPON_EWOK) & Extra.SUPER_EWOK_CATAPULT.has()
)

HAS_FLUTTER_CHARACTER = Character.has_any(Character.GEONOSIAN, Character.WATTO)


# FIXME: Jump Distance needs to be a custom rule so that Extra Toggle rules can correctly adjust it if an Extra Toggle
#  character has the requested jump distance.
def can_jump_distance_rule(distance_or_character: float | Character) -> HasSingleJumpDistance:
    distance: float
    if isinstance(distance_or_character, Character):
        distance = NON_VEHICLE_CHARACTER_TO_ITEM_DATA[distance_or_character].single_jump_distance
    else:
        distance = distance_or_character

    return HasSingleJumpDistance(distance)


# No rule is defined for being able to jump at least as far as Boba Fett (Boy) (0.56) because he is the only character
# with that jump distance, and has the worst jump distance.
CAN_JUMP_DISTANCE_0_56_BOBA_BOY_PLUS = HasAbility(CAN_BARELY_JUMP)
CAN_JUMP_DISTANCE_0_7_CLONE_PLUS = can_jump_distance_rule(Character.CLONE)
CAN_JUMP_DISTANCE_0_77_DEXTER_PLUS = can_jump_distance_rule(Character.DEXTER_JETTSTER)
CAN_JUMP_DISTANCE_0_904_LANDO_PLUS = can_jump_distance_rule(Character.LANDO_CALRISSIAN)


# All Sith are Jedi.
CAN_SITH_FORCE = logic_options(
    base=HasAbility(SITH),
    # Alternative because SITH implies JEDI:
    # normal=And(
    #     HasAbility(JEDI),
    #     HasAbility(SITH) | Extra.DARK_SIDE.has(),
    # )
    normal=Or(
        HasAbility(SITH),
        Extra.DARK_SIDE.has() & HasAbility(JEDI),
    )
)

CAN_DESTROY_CLOSE_SILVER_BRICKS = logic_options(
    base=HasAbility(BOUNTY_HUNTER),
    normal=Or(
        HasAbility(BOUNTY_HUNTER),
        CAN_USE_SELF_DESTRUCT,
        Extra.EXPLODING_BLASTER_BOLTS.has() & HasAnyAbilities(BLASTER | WEAPON_EWOK),
        Extra.SUPER_EWOK_CATAPULT.has() & HasAbility(WEAPON_EWOK),
    ),
)

CAN_USE_DEFLECT_BOLTS = Or(
    HasAbility(CAN_DEFLECT_BOLTS),
    HasAbility(CAN_AGGRAVATE_ENEMIES) & Extra.DEFLECT_BOLTS.has(),
)
CAN_SUPER_ZAP = HasAbility(WEAPON_ZAPPER) & Extra.SUPER_ZAPPER.has()
CAN_DAMAGE_AT_CLOSE_RANGE = logic_options(
    base=HasAnyAbilities(BLASTER | WEAPON_EWOK | CAN_MELEE),
    normal=Or(
        HasAnyAbilities(BLASTER | WEAPON_EWOK | CAN_MELEE),
        CAN_USE_SELF_DESTRUCT,
    ),
)
CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT = CAN_DAMAGE_AT_CLOSE_RANGE.base

# Some objects can only be destroyed by melee attacks that count as 'combo' attacks.
CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE = logic_options(
    base=HasAnyAbilities(BLASTER | WEAPON_EWOK | JEDI | CAN_HIGH_JUMP_SLAM) | Character.IMPERIAL_GUARD.has(),
    normal=Or(
        HasAnyAbilities(BLASTER | WEAPON_EWOK | JEDI | CAN_HIGH_JUMP_SLAM),
        Character.IMPERIAL_GUARD.has(),
        CAN_USE_SELF_DESTRUCT,
    ),
)

# can_fight_close_droids = logic_options(
#     base=CAN_DAMAGE_AT_CLOSE_RANGE,
#     normal=Or(
#         CAN_DAMAGE_AT_CLOSE_RANGE,
#         CAN_SUPER_ZAP,
#     ),
#     moderate=Or(
#         CAN_DAMAGE_AT_CLOSE_RANGE,
#         CAN_SUPER_ZAP,
#         CAN_USE_DEFLECT_BOLTS,
#     ),
# )
CAN_DAMAGE_SHIELDED_DROIDEKA = logic_options(
    # Only expect slam attacks, Bounty Hunter thermal detonators, or Droideka bolts.
    base=Or(
        HasAnyAbilities(JEDI | BOUNTY_HUNTER | CAN_HIGH_JUMP_SLAM),
        Character.DROIDEKA.has(),
    ),
    # Adds zappers and Extras.
    normal=Or(
        HasAnyAbilities(JEDI | BOUNTY_HUNTER | CAN_HIGH_JUMP_SLAM),
        Character.DROIDEKA.has(),
        HasAbility(WEAPON_ZAPPER) & CAN_DAMAGE_AT_CLOSE_RANGE,
        CAN_SUPER_ZAP,
        Or(
            CAN_USE_SELF_DESTRUCT,
            Extra.EXPLODING_BLASTER_BOLTS.has() & HasAnyAbilities(BLASTER | WEAPON_EWOK),
            Extra.SUPER_EWOK_CATAPULT.has() & HasAbility(WEAPON_EWOK),
        )
    ),
    # Adds Deflect Bolts Extra.
    moderate=Or(
        HasAnyAbilities(JEDI | BOUNTY_HUNTER | CAN_HIGH_JUMP_SLAM),
        Character.DROIDEKA.has(),
        HasAbility(WEAPON_ZAPPER) & CAN_DAMAGE_AT_CLOSE_RANGE,
        CAN_SUPER_ZAP,
        Or(
            CAN_USE_SELF_DESTRUCT,
            Extra.EXPLODING_BLASTER_BOLTS.has() & HasAnyAbilities(BLASTER | WEAPON_EWOK),
            Extra.SUPER_EWOK_CATAPULT.has() & HasAbility(WEAPON_EWOK),
            CAN_USE_DEFLECT_BOLTS,
        )
    ),
)
CAN_DESTROY_FAR_SILVER_BRICKS = logic_options(
    base=HasAbility(BOUNTY_HUNTER),
    normal=Or(
        HasAbility(BOUNTY_HUNTER),
        HasAbility(BLASTER) & Extra.EXPLODING_BLASTER_BOLTS.has(),
    ),
),
CAN_GRAPPLE = logic_options(
    base=HasAbility(GRAPPLE),
    normal=Or(
        HasAbility(GRAPPLE),
        HasAbility(JEDI) & Extra.FORCE_GRAPPLE_LEAP.has()
    )
)
# Pre-optimised version of can_sith_force & can_grapple.
CAN_SITH_FORCE_AND_GRAPPLE = logic_options(
    base=CAN_SITH_FORCE & HasAbility(GRAPPLE),
    normal=CAN_SITH_FORCE & (HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has()),
)
CAN_FIGHT_OR_BYPASS_SKIPPABLE_DROIDEKA = logic_options(
    base=CAN_DAMAGE_SHIELDED_DROIDEKA,
    normal=True_(),
)

CAN_ACTIVATE_CLOSE_TARGET = logic_options(
    base=HasAbility(BLASTER),
    # Ewoks are awkward because they don't auto-target the targets.
    normal=HasAnyAbilities(BLASTER | WEAPON_EWOK),
    # Self Destruct works too, though this is probably not well known.
    moderate=Or(
        HasAnyAbilities(BLASTER | WEAPON_EWOK),
        CAN_USE_SELF_DESTRUCT,
    ),
)

CAN_ORIGINAL_TRILOGY_HIGH_JUMP = HasAbility(HIGH_JUMP) & OT_HIGH_JUMP_ENABLED

CAN_USE_BOUNTY_HUNTER_ROCKETS = logic_options(
    base=False_(),
    normal=HasAbility(JETPACK) & Extra.BOUNTY_HUNTER_ROCKETS.has(),
)

HAS_ANY_YODA = Character.has_any(Character.YODA, Character.YODA_GHOST)
"""Check for having any Yoda character. This is typically used on its own in Normal logic only, when Yoda can double
jump across a gap that other Jedi cannot. Base logic tends to not consider Yoda's increased double jump distance, and
Moderate logic introduces triple jumps for increased jump distance (and height), and Yodas have the worst distance out
of Jedi. Occasionally, Yodas can be used to grab minikits through thin walls on their own, without needing to switch to
another character to perform a typical 'Yoda Clip'."""

CAN_YODA_CLIP = logic_options(
    base=False_(),
    hard=And(
        # Yoda's collision box is messed up, presumably due to the Y-offset Yoda has.
        HAS_ANY_YODA,
        # Any other character without the messed up Y-offset is required.
        # Logic cannot depend on having Yoda + Womp Rat, where Womp Rat is a character forced onto the player because
        # they only have 1 character unlocked because if the player were to gain Yoda (Ghost) as their next character,
        # the player could lose access to locations, so there can be a very small window of out-of-logic Yoda Clips.
        HasAnyCharacterExcept(Character.YODA, Character.YODA_GHOST),
    ),
)
"""Note: Checks for having at least some other character that is not a Yoda, if it is guaranteed that the player must
have some other, non-Yoda character, then the CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS macro should be used instead."""

CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS = logic_options(
    base=False_(),
    hard=HAS_ANY_YODA,
)
"""CAN_YODA_CLIP, but skip checking for other characters in cases where it is known that the player must have
a non-Yoda character if they have managed to reach the current region."""

# NORMAL_PLUS = logic_options(
#     base=False_(),
#     normal=True_(),
# )

MODERATE_PLUS = logic_options(
    base=False_(),
    moderate=True_(),
)

# HARD_PLUS = logic_options(
#     base=False_(),
#     hard=True_(),
# )

HAS_DOUBLE_JUMP_EXCEPT_ACKBAR = HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.ADMIRAL_ACKBAR)
HAS_P2_AI_DOUBLE_JUMP = HAS_DOUBLE_JUMP_EXCEPT_ACKBAR

HAS_EXTRA_DISTANCE_DOUBLE_JUMP = HAS_ANY_YODA | Character.ADMIRAL_ACKBAR.has()

HAS_GAS_IMMUNE = HasAnyAbilities(ASTROMECH_PANEL | PROTOCOL_PANEL) | Character.has_any(
    # PROTOCOL_PANEL
    # Character.TC_14,
    # Character.C_3PO,

    # ASTORMECH_PANEL
    # Character.R2_D2,
    # Character.R4_P17,
    # Character.R2_Q5,
    # Character.IG_88,
    # Character.FOUR_LOM,
    Character.GONK_DROID,
    Character.PK_DROID,
    Character.BATTLE_DROID,
    Character.BATTLE_DROID_SECURITY,
    Character.BATTLE_DROID_COMMANDER,
    Character.DROIDEKA,
    Character.PIT_DROID,
    Character.BATTLE_DROID_GEONOSIS,
    Character.SUPER_BATTLE_DROID,
    Character.GRIEVOUS_BODYGUARD,
    Character.BEN_KENOBI_GHOST,
    Character.ANAKIN_SKYWALKER_GHOST,
    Character.YODA_GHOST,

    # Extra Toggle characters
    # Character.BUZZ_DROID,
    # Character.TRAINING_REMOTE,
    # Character.DROID_1,
    # Character.DROID_2,
    # Character.DROID_3,
    # Character.DROID_4,
    # Character.MOUSE_DROID,
)

HAS_GAS_IMMUNE_EXCEPT_GHOSTS = HasAnyAbilities(ASTROMECH_PANEL | PROTOCOL_PANEL) | Character.has_any(
    Character.GONK_DROID,
    Character.PK_DROID,
    Character.BATTLE_DROID,
    Character.BATTLE_DROID_SECURITY,
    Character.BATTLE_DROID_COMMANDER,
    Character.DROIDEKA,
    Character.PIT_DROID,
    Character.BATTLE_DROID_GEONOSIS,
    Character.SUPER_BATTLE_DROID,
    Character.GRIEVOUS_BODYGUARD,
)

HAS_CAN_REFLECT_BLASTER_BOLTS = HasAbility(IS_NON_GHOST_JEDI) | Character.GENERAL_GRIEVOUS.has()
"""Grievous can *reflect* bolts. Bodyguard, Imperial Guard, Tarpals and Gamorrean Guard can each only *deflect* bolts"""

HAS_HIGH_JUMP_EXCEPT_BODYGUARD = HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD)
HAS_HIGH_JUMP_EXCEPT_BODYGUARD_OT = HAS_HIGH_JUMP_EXCEPT_BODYGUARD & OT_HIGH_JUMP_ENABLED

HAS_WALL_CLIMB = Character.GENERAL_GRIEVOUS.has() & HasAnyCharacterExcept(
    Character.GENERAL_GRIEVOUS,
    # Wall climbing works because General Grievous has a larger radius than most characters (0.13), and maybe because he
    # has a non-1.0 scale (1.25) too.
    # 0.12 radius:
    Character.DROID_4,
    Character.GONK_DROID,
    Character.EVENT_SUPER_GONK_DROID,
    Character.MOUSE_DROID,
    Character.SUPER_BATTLE_DROID,  # Was tested, so it is assumed others that are equal radius or larger do not work.
    # 0.13 radius:
    Character.WOMP_RAT,
    Character.DROID_1,
    # 0.15 radius:
    Character.DROID_2,
    # 0.18 radius:
    Character.BUZZ_DROID,
    # 0.19 radius:
    Character.DROIDEKA,
    Character.DEXTER_JETTSTER,
)
"""Grievous can climb up some walls by partially clipping into them following a character swap with the control stick in
 neutral, and then jumping again. Characters with large collision boxes are excluded."""

HAS_0_53_JUMP_HEIGHT_CHARACTER = Character.has_any(Character.GAMORREAN_GUARD, Character.EVENT_SUPER_GONK_DROID)

# Force Grapple leap can replace CAN_WEAR_HAT_AND_GRAPPLE.
HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE = logic_options(
    base=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT_AND_GRAPPLE),
    normal=Or(
        HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT_AND_GRAPPLE),
        And(
            Extra.FORCE_GRAPPLE_LEAP.has(),
            # Ackbar, Jar Jar, Tarpals, Bodyguard and Grievous are the only non-jedi that can double jump, and none of
            # them can wear hats, so all characters that can wear hats and double jump are jedi.
            HasAbility(CAN_WEAR_HAT_AND_DOUBLE_JUMP),
        )
    )
)
HAS_CAN_WEAR_HAT_AND_GRAPPLE = logic_options(
    base=HasAbility(CAN_WEAR_HAT_AND_GRAPPLE),
    normal=Or(
        HasAbility(CAN_WEAR_HAT_AND_GRAPPLE),
        And(
            Extra.FORCE_GRAPPLE_LEAP.has(),
            # Ackbar, Jar Jar, Tarpals, Bodyguard and Grievous are the only non-jedi that can double jump, and none of
            # them can wear hats, so all characters that can wear hats and double jump are jedi.
            HasAbility(CAN_WEAR_HAT_AND_DOUBLE_JUMP),
        )
    )
)
HAS_VEHICLE_LEVEL_CHARACTER_SWAPPING = HasFromListUnique(
    *(data.name for data in VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA),
    count=2
)

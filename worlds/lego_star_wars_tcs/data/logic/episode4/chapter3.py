from rule_builder.rules import And, Or, Rule

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
    CAN_YODA_CLIP,
    HAS_0_53_JUMP_HEIGHT_CHARACTER,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED, ot_high_jump_ternary
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
    HasAbilityCombination,
    HasAnyCharacterExcept,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData, MinikitData

from ...areas import Area
from ...characters import Character
from ...levels import Level

from ....character_ability import *
from ...items.character_items import NON_VEHICLE_CHARACTER_TO_ITEM_DATA

NAME = "Mos Eisley Spaceport"

R_SPAWN = "Spawn"
R_IMPERIAL_SHOWERS_AND_POOL = "Imperial Showers And Pool"
R_ABOVE_FIRST_STORMTROOPER_GATE = "Above First Stormtrooper Gate"
R_AFTER_STORMTROOPER_GATE_IMPERIAL_EXIT = "After Stormtrooper Gate (Imperial Exit)"
R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT = "After Stormtrooper Gate (Protocol Exit)"
R_WOMP_RAT_SHOOTING_RANGE = "Womp Rat Shooting Range"
R_AFTER_BLOCKED_STREET = "After Blocked Street"
R_CANTINA_ENTRANCE = "Cantina Entrance"
R_INSIDE_CANTINA = "Inside Cantina"
R_SPY_CHASE_START = "Spy Chase Start"
R_SPY_CHASE_SPAWN_FIRST_STOREY = "Spy Chase Spawn First Storey"
R_SPY_CHASE_SPAWN_SECOND_STOREY = "Spy Chase Spawn Second Storey"
R_SPY_CHASE_BOMB_GROUND_LEVEL = "Spy Chase Bomb Ground Level"
R_SPY_CHASE_BOMB_LEVER = "Spy Chase Bomb Lever"
R_SPY_CHASE_RIGHT_PATH = "Spy Chase Right Path"
R_TURNIPS_MINIKIT_LEDGE = "Turnips Minikit Ledge"
R_STORMTROOPER_AND_DEWBACK_COURTYARD = "Stormtrooper And Dewback Courtyard"
R_CINEMA = "Cinema"
R_HANGAR = "Hangar"

CAN_BUILD_FIRST_AT_ST = HasAllAbilities(PROTOCOL_PANEL | JEDI | ASTROMECH_PANEL)


def _make_can_pass_cantina_anti_droid_field() -> Rule:
    affected_by_anti_droid_field: set[Character] = {
        Character.R2_D2,
        Character.C_3PO,
        Character.GONK_DROID,
        Character.EVENT_SUPER_GONK_DROID,
        Character.GRIEVOUS_BODYGUARD,
        Character.DROIDEKA,
        Character.R4_P17,
        Character.BATTLE_DROID,
        Character.BATTLE_DROID_COMMANDER,
        Character.BATTLE_DROID_GEONOSIS,
        Character.BATTLE_DROID_SECURITY,
        Character.TC_14,
        Character.SUPER_BATTLE_DROID,
        Character.PK_DROID,
        Character.IG_88,
        Character.FOUR_LOM,
        Character.PIT_DROID,
        Character.R2_Q5,
        # Extra toggle characters:
        Character.DROID_1,
        Character.DROID_2,
        Character.DROID_3,
        Character.DROID_4,
        # While Mouse Droid and Buzz Droid might be affected, they are not available in this chapter.
    }
    # Remove droids that can destroy the anti-droid field on their own.
    for character in tuple(affected_by_anti_droid_field):
        if BLASTER in NON_VEHICLE_CHARACTER_TO_ITEM_DATA[character].abilities:
            affected_by_anti_droid_field.remove(character)
    characters_rule = HasAnyCharacterExcept(*affected_by_anti_droid_field)
    # The ceiling has no collision, so Bodyguard can jump over the emitters when either OT high jump is enabled, or by
    # performing a triple jump.
    characters_rule_moderate = HasAnyCharacterExcept(
        *(affected_by_anti_droid_field - {Character.GRIEVOUS_BODYGUARD})
    )
    return logic_options(
        base=characters_rule,
        moderate=characters_rule_moderate,
    )


CAN_PASS_CANTINA_ANTI_DROID_FIELD = _make_can_pass_cantina_anti_droid_field()
del _make_can_pass_cantina_anti_droid_field


helper = ChapterHelper(
    area=Area.MOSEISLEY,
    start_region=R_SPAWN,
)


MOS_EISLEY_SPACEPORT = helper.make_chapter(
    intended_completion_path={
        "base": (
            R_ABOVE_FIRST_STORMTROOPER_GATE,
            R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT,
            R_AFTER_BLOCKED_STREET,
            R_CANTINA_ENTRANCE,
            R_INSIDE_CANTINA,
            R_SPY_CHASE_START,
            R_SPY_CHASE_SPAWN_FIRST_STOREY,
            R_SPY_CHASE_BOMB_GROUND_LEVEL,
            R_SPY_CHASE_BOMB_LEVER,
            # Go back down.
            R_SPY_CHASE_BOMB_GROUND_LEVEL,
            R_STORMTROOPER_AND_DEWBACK_COURTYARD,
            R_HANGAR,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_IMPERIAL_SHOWERS_AND_POOL,
                # Note: Grievous and Droideka are too big to fit through the door.
                HasAbility(IMPERIAL),
            ),
            ExitData(
                R_ABOVE_FIRST_STORMTROOPER_GATE,
                logic_options(
                    base=And(
                        # Expect fighting the Stormtroopers.
                        CAN_DAMAGE_AT_CLOSE_RANGE,
                        # Force the steps into a ramp, or high jump up.
                        HasAbility(JEDI) | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    # Just double jump up, next to where the ramp goes.
                    normal=HasAbility(CAN_DOUBLE_JUMP),
                    # Walk up the steps, then jump on, and then over the left wall.
                    moderate=HasAbility(CAN_JUMP_HEIGHT_0_37),
                )
            ),
        ),
        R_IMPERIAL_SHOWERS_AND_POOL: (),
        R_ABOVE_FIRST_STORMTROOPER_GATE: (
            ExitData(
                R_AFTER_STORMTROOPER_GATE_IMPERIAL_EXIT,
                HasAbility(IMPERIAL),
                new_level=Level.MOSEISLEY_B,
            ),
            ExitData(
                R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT,
                HasAbility(PROTOCOL_PANEL),
                new_level=Level.MOSEISLEY_B,
            ),
        ),
        R_AFTER_STORMTROOPER_GATE_IMPERIAL_EXIT: (
            # Drop down.
            ExitData(R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT),
            ExitData(
                R_WOMP_RAT_SHOOTING_RANGE,
                logic_options(
                    base=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                    # A good single-jump distance can cross the broken bridge.
                    moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER | CAN_JUMP_DISTANCE_0_92),
                ),
            ),
        ),
        R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT: (
            ExitData(
                R_WOMP_RAT_SHOOTING_RANGE,
                logic_options(
                    # Only expect high jumping.
                    base=CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Double jump up the corner.
                    normal=HasAbility(CAN_DOUBLE_JUMP),
                    # You can also get up here by jumping out of an AT-ST, but the first AT-ST requires force to build
                    # it, making it logically redundant, but there is a second AT-ST later into the level, that you
                    # could bring all the way back here, but it doesn't spawn unless you build the first AT-ST :(
                ),
            ),
            ExitData(
                R_AFTER_BLOCKED_STREET,
                Or(
                    CAN_BUILD_FIRST_AT_ST & HasAbility(CAN_RIDE_VEHICLES),
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                ),
            ),
        ),
        R_WOMP_RAT_SHOOTING_RANGE: (),
        R_AFTER_BLOCKED_STREET: (
            ExitData(
                R_CANTINA_ENTRANCE,
                CAN_DAMAGE_AT_CLOSE_RANGE,
                new_level=Level.MOSEISLEY_C,
            ),
        ),
        R_CANTINA_ENTRANCE: (
            ExitData(
                R_INSIDE_CANTINA,
                CAN_PASS_CANTINA_ANTI_DROID_FIELD,
            ),
        ),
        R_INSIDE_CANTINA: (
            ExitData(
                R_SPY_CHASE_START,
                new_level=Level.MOSEISLEY_D,
            ),
        ),
        R_SPY_CHASE_START: (
            ExitData(
                R_SPY_CHASE_SPAWN_FIRST_STOREY,
                logic_options(
                    base=CAN_GRAPPLE,
                    normal=HasAbility(CAN_DOUBLE_JUMP) | CAN_GRAPPLE,
                ),
            ),
        ),
        R_SPY_CHASE_SPAWN_FIRST_STOREY: (
            ExitData(
                R_SPY_CHASE_SPAWN_SECOND_STOREY,
                logic_options(
                    base=CAN_GRAPPLE & HasAbility(CAN_BUILD_BRICKS),
                    normal=Or(
                        HasAbility(CAN_DOUBLE_JUMP),
                        CAN_GRAPPLE & HasAbility(CAN_BUILD_BRICKS),
                    ),
                ),
            ),
            ExitData(R_SPY_CHASE_BOMB_GROUND_LEVEL),
        ),
        R_SPY_CHASE_SPAWN_SECOND_STOREY: (
            ExitData(
                R_SPY_CHASE_RIGHT_PATH,
                logic_options(
                    base=HasAbility(BOUNTY_HUNTER),
                    # Triple jump over the bounty hunter door.
                    moderate=HasAnyAbilities(BOUNTY_HUNTER | JEDI | CAN_HIGH_JUMP_SLAM),
                    # High jump onto the antenna on the building to the left of the bounty hunter door, then jump over
                    # the bounty hunter door.
                    # This probably could be in moderate logic, though it is more obscure.
                    hard=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(BOUNTY_HUNTER | JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(BOUNTY_HUNTER | JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
            ExitData(
                R_SPY_CHASE_BOMB_LEVER,
                CAN_GRAPPLE | HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
            ),
            ExitData(
                R_TURNIPS_MINIKIT_LEDGE,
                HasAbility(HOVER),
            ),
        ),
        R_SPY_CHASE_BOMB_GROUND_LEVEL: (
            ExitData(
                R_SPY_CHASE_BOMB_LEVER,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    # I don't think it will ever be relevant, but Gamorrean Guard/Super Gonk can just jump straight up
                    # here.
                    moderate=HasAbility(CAN_DOUBLE_JUMP) | HAS_0_53_JUMP_HEIGHT_CHARACTER,
                ),
            ),
            ExitData(
                R_STORMTROOPER_AND_DEWBACK_COURTYARD,
                logic_options(
                    base=And(
                        helper.can_reach_region(R_SPY_CHASE_BOMB_LEVER),
                        HasAbility(CAN_PULL_LEVERS),
                        CAN_DAMAGE_AT_CLOSE_RANGE,
                    ),
                    # You can just blow up the door yourself.
                    normal=Or(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        And(
                            helper.can_reach_region(R_SPY_CHASE_BOMB_LEVER),
                            HasAbility(CAN_PULL_LEVERS),
                            CAN_DAMAGE_AT_CLOSE_RANGE,
                        )
                    )
                ),
            ),
            ExitData(
                R_SPY_CHASE_RIGHT_PATH,
                HasAbility(PROTOCOL_PANEL),
            ),
        ),
        R_SPY_CHASE_BOMB_LEVER: (
            ExitData(
                R_TURNIPS_MINIKIT_LEDGE,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    normal=HasAbility(CAN_JUMP_0_44),
                ),
            ),
        ),
        R_SPY_CHASE_RIGHT_PATH: (
            ExitData(
                R_STORMTROOPER_AND_DEWBACK_COURTYARD,
                CAN_SITH_FORCE,
            ),
        ),
        R_TURNIPS_MINIKIT_LEDGE: (),
        R_STORMTROOPER_AND_DEWBACK_COURTYARD: (
            ExitData(
                R_CINEMA,
                HasAbility(ASTROMECH_PANEL),
                new_level=Level.MOSEISLEY_E,
            ),
            ExitData(
                R_HANGAR,
                logic_options(
                    base=HasAbility(CAN_RIDE_VEHICLES),
                    # Jump on the turnip, jump on the sloped bit of wall adjacent to the turnip, jump to where the hat
                    # machine is, jump onto the wall of that area, then, finally, jump across to the section that leads
                    # to the spaceport.
                    # Bodyguard, who has reduced jump distance, can triple jump to make up for it.
                    moderate=HasAnyAbilities(CAN_RIDE_VEHICLES | CAN_DOUBLE_JUMP),
                )
            ),
            ExitData(
                R_SPY_CHASE_RIGHT_PATH,
                CAN_SITH_FORCE,
            ),
        ),
        R_CINEMA: (),
        R_HANGAR: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=HasAbility(BLASTER),
                    # There are pipes you can jump on to then jump to the upper level, to kill the stormtroopers up
                    # there.
                    normal=Or(
                        HasAbility(BLASTER),
                        HasAbility(CAN_DOUBLE_JUMP) & CAN_DAMAGE_AT_CLOSE_RANGE,
                    )
                    # Droideka and General Grievous are too big to fit in the door of the Millennium Falcon.
                ) & HasAnyCharacterExcept(Character.DROIDEKA, Character.GENERAL_GRIEVOUS),
            ),
        ),
    },
    minikits={
        "Drain Imperial Pool Minikit": minikit_data(
            R_IMPERIAL_SHOWERS_AND_POOL,
            HasAbility(JEDI),
            pickup_name="WATER_M",
        ),
        "Reveal Three Carrots Minikit": MinikitData(
            R_SPAWN,
            logic_options(
                base=And(
                    # Basic melee attacks do not work on the barrels hiding the carrots.
                    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                    Or(
                        # Hover across the broken bridge, use the Bounty Hunter panel, then build the fan from the
                        # bricks that spawn.
                        HasAllAbilities(HOVER | BOUNTY_HUNTER | CAN_BUILD_BRICKS),
                        # Just jump up to the bridge and then jump up to the minikit.
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                ),
                # Allow DOUBLE_JUMP to get to the Bounty Hunter panel instead of requiring HOVER. Either double jump
                # across the gap in the bridge, double jump starting from a nearby barrel, or double jump up the terrain
                # that sticks out on the side of the bridge near the bounty hunter panel.
                normal=And(
                    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                    Or(
                        HasAllAbilities(BOUNTY_HUNTER | CAN_BUILD_BRICKS) & HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                        # Just jump up to the bridge and then jump up to the minikit.
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                ),
                # Allow triple jump to reach the minikit.
                moderate=And(
                    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                    Or(
                        HasAllAbilities(BOUNTY_HUNTER | CAN_BUILD_BRICKS) & HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                        # Just jump up to the bridge and then jump up to the minikit.
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                            capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        ),
                    ),
                )
            ),
            pickup_names=(
                "C_M1",
                "C_M2",
                "C_M3",
            ),
        ),
        "Minikit Beneath Dark Side Roof": minikit_data(
            R_SPAWN,
            CAN_SITH_FORCE,
            pickup_name="m_pup1",
        ),
        "Womp Rat Shooting Range Minikit": minikit_data(
            R_WOMP_RAT_SHOOTING_RANGE,
            HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES),
            pickup_name="WOMPRAT",
        ),
        "Stack Boxes Near AT-ST Minikit": minikit_data(
            R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT,
            logic_options(
                # Stack the boxes and double jump up.
                base=HasAbility(JEDI),
                # You can build the AT-ST and jump out of it to get this minikit, but you need JEDI to build the AT-ST
                # in the first place, so this is logically irrelevant.
                # CAN_BUILD_FIRST_AT_ST & HasAbility(CAN_RIDE_VEHICLES),
                normal=ot_high_jump_ternary(
                    # High jump up from one of the boxes.
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAbility(JEDI),
                ),
                moderate=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    # Triple jump up.
                    capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            pickup_name="mk_1",
        ),
        "Tall Tower Minikit": minikit_data(
            R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT,
            logic_options(
                base=And(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                    CAN_GRAPPLE,
                ),
                normal=And(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                    Or(
                        CAN_GRAPPLE,
                        # Build the AT-ST, then double jump out.
                        CAN_BUILD_FIRST_AT_ST & HasAbilityCombination(CAN_DOUBLE_JUMP | CAN_RIDE_VEHICLES),
                    ),
                ),
                moderate=Or(
                    And(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                        Or(
                            CAN_GRAPPLE,
                            # Build the AT-ST, then double jump out of it.
                            CAN_BUILD_FIRST_AT_ST & HasAbilityCombination(CAN_DOUBLE_JUMP | CAN_RIDE_VEHICLES),
                        ),
                    ),
                    # Triple High Jump up without making the tower more upright.
                    Character.GENERAL_GRIEVOUS.has() & OT_HIGH_JUMP_ENABLED,
                ),
            ),
            pickup_name="mk_0",
        ),
        "Cantina Force Field Minikit": minikit_data(
            R_INSIDE_CANTINA,
            logic_options(
                base=HasAbility(SHORTIE),
                hard=HasAbility(SHORTIE) | CAN_YODA_CLIP,
            ),
            pickup_name="m_pup1",
        ),
        "Reveal Three Turnips Minikit": MinikitData(
            R_TURNIPS_MINIKIT_LEDGE,
            And(
                # The barrels cannot be destroyed with basic melee attacks, only the lids of the barrels.
                # The barrels are pretty weird in general, since the lids cannot be hit by lightsabers, but Bodyguard
                # can hit the lids without issue.
                CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                # Third turnip.
                helper.can_reach_region(R_STORMTROOPER_AND_DEWBACK_COURTYARD),
                # Second turnip.
                helper.can_reach_region(R_SPY_CHASE_RIGHT_PATH),
                # First turnip.
                helper.can_reach_region(R_SPY_CHASE_START),
            ),
            pickup_names=(
                "M_T1",
                "M_T2",
                "M_T3",
            ),
        ),
        "Two Player Force Gate Minikit": minikit_data(
            R_SPY_CHASE_RIGHT_PATH,
            logic_options(
                base=HasAbility(JEDI),
                # Triple high jump from the barrel in the corner to get enough height to get over the colision of the
                # wall and land in the area behind the minikit. You are now trapped and must restart the level.
                hard=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    capped=HasAbility(JEDI),
                ),
            ),
            pickup_name="m_pup1",
        ),
        "Cinema Minikit": minikit_data(
            R_CINEMA,
            logic_options(
                base=HasAbility(JEDI),
                # Triple high jump over the jumbled cinema screen.
                moderate=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    capped=HasAbility(JEDI),
                ),
            ),
            pickup_name="m_pup1",
        ),
    },
    power_brick=LocationData(
        R_SPAWN,
        HasAllAbilities(JEDI | ASTROMECH_PANEL),
    ),
    ridables={
        Character.SPEEDER_LAND: LocationData(R_SPAWN),
        Character.MOSCANNON: LocationData(R_WOMP_RAT_SHOOTING_RANGE, HasAbility(CAN_BUILD_BRICKS)),
        Character.ATST: LocationData(
            R_AFTER_STORMTROOPER_GATE_PROTOCOL_EXIT,
            CAN_BUILD_FIRST_AT_ST,
        ),
        Character.DEWBACK: LocationData(R_STORMTROOPER_AND_DEWBACK_COURTYARD),
    }
)

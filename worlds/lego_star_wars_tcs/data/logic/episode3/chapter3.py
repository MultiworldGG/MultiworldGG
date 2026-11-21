from rule_builder.rules import True_, Or, False_, And

from ..macros import (
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_USE_SELF_DESTRUCT,
    can_jump_distance_rule,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities, HasAbilityCombination
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra

from ....character_ability import *

R_CIRCULAR_PLATFORM = "Circular Platform"
R_FAR_LEFT_SILVER_BRICK_SECTION = "Far Left Silver Brick Section"
R_FIRST_EXPLOSIVES_SECTION = "First Explosives Section"
R_LOW_PLATFORM_WITH_POWER_UP = "Low Platform With Power Up"
R_THIRD_EXPLOSIVES_SECTION_GAP_AREA = "Third Explosives Section Gap Area"
R_FAR_RIGHT_LOW_PLATFORM = "Far Right Low Platform"
R_SHOOT_SECOND_EXPLOSIVES_SECTION = "Shoot Second Explosives Section"
R_FORCE_THIRD_EXPLOSIVES_SECTION = "Force Third Explosives Section"
R_THIRD_EXPLOSIVES_CLIFF = "Third Explosives Cliff"
R_BRIDGE_AND_MINES_BUILDING = "Bridge And Mines Building"
R_BRICK_COVERED_MINIKIT_ALCOVE = "Brick Covered Minikit Alcove"

_helper = ChapterHelper(
    area=Area.GRIEVOUS,
    start_region=R_CIRCULAR_PLATFORM,
)

# To complete the chapter, 3 sets of explosives need to be destroyed in a row.
# The logic for these explosives could be implemented using events, however, if 3-3 is the starting chapter, having a
# chain of events at the start like this could cause progression balancing to apply too strongly, so the logic is
# chained together using CanReach rules instead.

CAN_HURT_GRIEVOUS = logic_options(
    # Only consider melee attackers because other attacks are awkward.
    base=HasAbility(CAN_MELEE),
    # Non-melee is awkward.
    # Grievous tends to bug out when using Exploding Blaster Bolts, so don't have the logic expect it.
    # todo: See if the client can fix this by either ending the level manually, or by giving Grievous +1 health when
    #  he's alive with zero health.
    # normal=Or(
    #     HasAbility(CAN_MELEE),
    #     CAN_DESTROY_CLOSE_SILVER_BRICKS,
    # ),
    # Allow Blasters/Ewoks/Self Destruct.
    moderate=CAN_DAMAGE_AT_CLOSE_RANGE,
)

# The first explosives are not active until you hurt Grievous.
CAN_EXPLODE_FIRST_EXPLOSIVES = CAN_HURT_GRIEVOUS.and_rule(
    logic_options(
        # Shoot them from the spawn region.
        base=HasAbility(BLASTER),
        normal=Or(
            HasAllAbilities(JEDI | BLASTER),
            # If you walk up to Grievous, the explosives explode.
            _helper.can_reach_region(R_FIRST_EXPLOSIVES_SECTION),
        )
    )
)

# To shoot the first explosives from R_SHOOT_SECOND_EXPLOSIVES_SECTION requires shooting the first explosives so that a
# force platform spawns that a blaster character can stand on and jump to be able to shoot the second explosives.
# The second explosive do NOT require the first explosives to be destroyed.
CAN_EXPLODE_SECOND_EXPLOSIVES = logic_options(
    # In base logic, exploding the first explosives and shooting the second explosives is expected.
    base=And(
        CAN_EXPLODE_FIRST_EXPLOSIVES,
        HasAbility(JEDI),
        HasAbilityCombination(BLASTER | CAN_JUMP_HEIGHT_0_37),
        _helper.can_reach_region(R_SHOOT_SECOND_EXPLOSIVES_SECTION),
    ),
    normal=And(
        CAN_EXPLODE_FIRST_EXPLOSIVES,
        Or(
            # If you walk up to Grievous the second explosives explode.
            _helper.can_reach_region(R_FORCE_THIRD_EXPLOSIVES_SECTION),
            And(
                HasAbilityCombination(BLASTER | CAN_JUMP_HEIGHT_0_37),
                _helper.can_reach_region(R_SHOOT_SECOND_EXPLOSIVES_SECTION),
            ),
        ),
    ),
    moderate=Or(
        # Walking up the second explosives makes them explode even if the first explosives have not been destroyed and
        # Grievous is not at the second explosives yet. I am considering this a glitch, so skipping the first explosives
        # is requiring moderate logic.
        _helper.can_reach_region(R_FORCE_THIRD_EXPLOSIVES_SECTION),
        And(
            HasAbilityCombination(BLASTER | CAN_JUMP_HEIGHT_0_37),
            _helper.can_reach_region(R_SHOOT_SECOND_EXPLOSIVES_SECTION),
        ),
    ),
)

CAN_EXPLODE_FIRST_TWO_EXPLOSIVES = CAN_EXPLODE_SECOND_EXPLOSIVES.and_rule(
    # Moderate+ logic can explode the second explosives without exploding the first explosives.
    CAN_EXPLODE_FIRST_EXPLOSIVES, apply_to="moderate+"
)

# The last explosives are not active until the first and second explosives have been exploded.
CAN_EXPLODE_LAST_EXPLOSIVES = logic_options(
    # Destroy the wall, force the explosive into position, then shoot it.
    base=HasAllAbilities(JEDI | BLASTER) & _helper.can_reach_region(R_FORCE_THIRD_EXPLOSIVES_SECTION),
    normal=And(
        HasAbility(JEDI) & _helper.can_reach_region(R_FORCE_THIRD_EXPLOSIVES_SECTION),
        Or(
            HasAbility(BLASTER),
            # Walking up to Grievous also makes the explosives explode instead of needing to shoot them.
            _helper.can_reach_region(R_THIRD_EXPLOSIVES_CLIFF),
        ),
    ),
).and_rule(
    # Require the first two explosives rules for each logic difficulty.
    CAN_EXPLODE_FIRST_TWO_EXPLOSIVES
)

# CAN_MELEE_BRICKS_BLOCKING_ALCOVE_MINIKIT = logic_options(
#     # Only expect shooting.
#     base=False_(),
#     # Yoda can melee this, but tends to die.
#     moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
# )


GENERAL_GRIEVOUS = _helper.make_chapter(
    # The region connections are a mess, and the entrance to the Chapter Completion region is at the start, but with a
    # rule that checks for access to regions.
    intended_completion_path={
        "base": (
            R_FIRST_EXPLOSIVES_SECTION,
            R_SHOOT_SECOND_EXPLOSIVES_SECTION,
            R_FORCE_THIRD_EXPLOSIVES_SECTION,
            # Jump back to the platform to actually complete the chapter.
            R_CIRCULAR_PLATFORM,
        ),
    },
    regions={
        R_CIRCULAR_PLATFORM: (
            ExitData(
                R_FAR_LEFT_SILVER_BRICK_SECTION,
                logic_options(
                    base=HasAbility(HOVER),
                    # Yoda cannot make it, but Grievous' Bodyguard can.
                    moderate=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            ExitData(
                R_FIRST_EXPLOSIVES_SECTION,
                logic_options(
                    base=Or(
                        HasAbility(HOVER),
                        # Fight Grievous, then shoot the explosives, and then force to make the bridge.
                        HasAllAbilities(BLASTER | JEDI),
                    ),
                    # Yoda and Ackbar can double jump across, but it's close, so this is only in Moderate+.
                    moderate=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE) | HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                ),
            ),
            ExitData(
                R_LOW_PLATFORM_WITH_POWER_UP,
                logic_options(
                    base=HasAbility(CAN_JUMP_DISTANCE_0_69),
                    moderate=HasAbility(CAN_BARELY_JUMP),
                ),
                er_rule=logic_options(
                    # Ewok (jump_distance>=0.69) can make it across fairly easily jumping across the left/middle of the
                    # gap.
                    base=can_jump_distance_rule(Character.EWOK),
                    # Boba Fett (Boy) (jump_distance>=0.56) can only barely make it by jumping across the shortest
                    # distance between the platforms along the far left. Jumping immediately upon landing is probably
                    # required to prevent sliding off.
                    moderate=can_jump_distance_rule(Character.BOBA_FETT_BOY),
                ),
            ),
            ExitData(
                R_THIRD_EXPLOSIVES_SECTION_GAP_AREA,
                logic_options(
                    base=False_(),
                    # The collision on the plants by the wall is weird, you can jump on them and then double jump again.
                    moderate=HasAbility(CAN_DOUBLE_JUMP),
                )
            ),
            ExitData(
                R_FAR_RIGHT_LOW_PLATFORM,
                # Moderate logic can double jump to the middle platform and drop down to here instead, so the triple
                # jump across the gap is logically irrelevant.
                HasAbility(HOVER),
                er_rule=logic_options(
                    base=HasAbility(HOVER),
                    # Yoda cannot make it, but Grievous' Bodyguard can.
                    moderate=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM)
                ),
            ),
            ExitData(
                "Chapter Completion",
                # Note: Contains a few CanReachRegion rules.
                CAN_EXPLODE_LAST_EXPLOSIVES,
            )
        ),
        R_FAR_LEFT_SILVER_BRICK_SECTION: (
            # The rule from "Circular Platform -> First Explosives Section" is the same as
            # "Circular Platform -> Far Left Silver Brick Section", so if you can get to
            # R_FAR_LEFT_SILVER_BRICK_SECTION, you can also get to R_FIRST_EXPLOSIVES_SECTION.
            # ExitData(
            #     R_FIRST_EXPLOSIVES_SECTION,
            #     logic_options(
            #         base=HasAbility(HOVER),
            #         # Yoda cannot make the jump with a triple jump, but can make the jump with a double jump instead.
            #         moderate=HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
            #     ),
            # ),
        ),
        R_FIRST_EXPLOSIVES_SECTION: (
            ExitData(
                R_SHOOT_SECOND_EXPLOSIVES_SECTION,
                logic_options(
                    base=HasAnyAbilities(GRAPPLE | CAN_DOUBLE_JUMP),
                    normal=HasAnyAbilities(GRAPPLE | CAN_DOUBLE_JUMP | CAN_JUMP_0_44),
                    moderate=Or(
                        HasAnyAbilities(GRAPPLE | CAN_DOUBLE_JUMP | CAN_JUMP_0_44),
                        # (movement speed/jump height/jump distance)
                        # Boba Fett (Boy) I don't think can make the second or third jumps (0.8/0.37/0.56)
                        #   Not enough movement speed to slide up the second jump that he doesn't have enough height for
                        #   and not enough movement speed to make it across the third jump.
                        # Geonosian cannot make any of the jumps (height) (1.5/0.3/'0.65')
                        # Clone struggles with all the jumps (distance and height) (1.0/0.37/0.7)
                        # Captain Panaka struggles with the second jump (getting height) (1.2/0.37/0.84)
                        # Ewok/Ugnaught struggle with the last jump (getting distance) (0.9/0.44/0.69)
                        # Gamorrean Guard struggles with the last jump (getting distance) (0.75/0.53/0.69)
                        HasAbilityCombination(CAN_JUMP_HEIGHT_0_37 | CAN_JUMP_DISTANCE_0_69),
                    ),
                ),
            ),
            ExitData(
                R_FAR_LEFT_SILVER_BRICK_SECTION,
                logic_options(
                    base=HasAbility(HOVER),
                    # Yoda cannot make the jump with a triple jump, but can make the jump with a double jump instead.
                    moderate=HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                )
            ),
        ),
        R_LOW_PLATFORM_WITH_POWER_UP: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=False_(),
                    hard=HasAbility(BLASTER),
                ),
                name="Grieve-Cheese",
            ),
            # Logically irrelevant because "Low Platform With Power Up -> Third Explosives Section Gap Area" only
            # requires high jump height, and then
            # "Third Explosives Section Gap Area -> Shoot Second Explosives Section" only requires CAN_DOUBLE_JUMP.
            # ExitData(
            #     R_SHOOT_SECOND_EXPLOSIVES_SECTION,
            #     logic_options(
            #         base=False_(),
            #         # Near max height triple jump needed.
            #         moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            #     ),
            # ),
            ExitData(
                R_THIRD_EXPLOSIVES_SECTION_GAP_AREA,
                logic_options(
                    base=HasAbility(HIGH_JUMP),
                    # Logically irrelevant because "Circular Platform -> Third Explosives Section Gap Area" with
                    # CAN_DOUBLE_JUMP.
                    moderate=False_(),
                ),
                er_rule=logic_options(
                    base=HasAbility(HIGH_JUMP),
                    # Triple jump or high jump.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
                ),
            ),
        ),
        R_THIRD_EXPLOSIVES_SECTION_GAP_AREA: (
            ExitData(
                R_SHOOT_SECOND_EXPLOSIVES_SECTION,
                logic_options(
                    # Expect going around the top instead.
                    base=False_(),
                    normal=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                ),
            ),
            ExitData(
                R_THIRD_EXPLOSIVES_CLIFF,
                logic_options(
                    # Expect hovering across from R_SHOOT_SECOND_EXPLOSIVES_SECTION
                    base=False_(),
                    normal=HasAbility(HIGH_JUMP),
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
                ),
            ),
            ExitData(
                R_FORCE_THIRD_EXPLOSIVES_SECTION,
                logic_options(
                    base=HasAbility(GRAPPLE),
                    # You can get under the cliff a little bit for some extra height, enough to high jump up.
                    # Jedi can triple jump up, though a good amount of height is needed.
                    moderate=HasAnyAbilities(GRAPPLE | HIGH_JUMP | JEDI),
                )
            ),
            ExitData(
                R_BRIDGE_AND_MINES_BUILDING,
                logic_options(
                    base=HasAbility(HIGH_JUMP),
                    moderate=HasAnyAbilities(HIGH_JUMP | JEDI),
                )
            ),
            ExitData(
                R_BRICK_COVERED_MINIKIT_ALCOVE,
                logic_options(
                    base=HasAbility(CAN_DOUBLE_JUMP),
                    normal=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | CAN_JUMP_0_44),
                )
            )
        ),
        R_FAR_RIGHT_LOW_PLATFORM: (
            ExitData(
                R_THIRD_EXPLOSIVES_SECTION_GAP_AREA,
                # Jetpack Hover can also get here on moderate logic, but all JETPACK can GRAPPLE.
                HasAnyAbilities(GRAPPLE | CAN_DOUBLE_JUMP),
            ),
        ),
        R_SHOOT_SECOND_EXPLOSIVES_SECTION: (
            # Dropping down to R_LOW_PLATFORM_WITH_POWER_UP is logically useless because being able to reach any upper
            # area to drop down from, can also use "Circular Platform -> Low Platform With Power Up".
            # ExitData(
            #     R_LOW_PLATFORM_WITH_POWER_UP
            # ),
            ExitData(
                R_THIRD_EXPLOSIVES_SECTION_GAP_AREA,
                logic_options(
                    # Expect going around the top or far right instead.
                    base=False_(),
                    normal=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER)
                ),
            ),
            ExitData(
                R_FORCE_THIRD_EXPLOSIVES_SECTION,
                # Exploding the second explosives spawns bricks that can be forced into stairs.
                logic_options(
                    base=HasAbility(JEDI) & CAN_EXPLODE_SECOND_EXPLOSIVES,
                    normal=Or(
                        HasAbility(JEDI) & CAN_EXPLODE_SECOND_EXPLOSIVES,
                        HasAbility(HIGH_JUMP),
                    ),
                    # Triple jump or high jump up.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP)
                ),
            ),
            ExitData(
                R_BRICK_COVERED_MINIKIT_ALCOVE,
                # Only covers getting to the alcove. Destroying the bricks in the way is covered by the minikit
                # location itself.
                logic_options(
                    # Only expect access from R_THIRD_EXPLOSIVES_SECTION_GAP_AREA.
                    base=False_(),
                    normal=Or(
                        HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                        # Astromech hover can make it, so long as the bricks from the second explosives have
                        # spawned so that there is enough starting height.
                        HasAbility(ASTROMECH_DROID) & CAN_EXPLODE_SECOND_EXPLOSIVES,
                    ),
                ),
            ),
        ),
        R_FORCE_THIRD_EXPLOSIVES_SECTION: (
            # The base logic can be expected to drop down here instead of double jumping across the gap between
            # R_SHOOT_SECOND_EXPLOSIVES_SECTION and R_THIRD_EXPLOSIVES_SECTION_GAP_AREA.
            ExitData(
                R_THIRD_EXPLOSIVES_SECTION_GAP_AREA,
                logic_options(
                    base=True_(),
                    # Entrance is logically irrelevant, so don't create it.
                    normal=False_(),
                ),
                er_rule=True_(),
            ),
            ExitData(
                R_THIRD_EXPLOSIVES_CLIFF,
                logic_options(
                    base=HasAbility(HOVER),
                    moderate=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                )
            ),
            ExitData(
                R_BRICK_COVERED_MINIKIT_ALCOVE,
                logic_options(
                    # Expect double jump from R_THIRD_EXPLOSIVES_SECTION_GAP_AREA.
                    base=False_(),
                    # Getting into the alcove can be a pain/luck with some characters.
                    # While Gonk Droid might not be able to fall down into here (slides out due to low movement speed),
                    # I'm pretty sure all characters that can reach R_FORCE_THIRD_EXPLOSIVES_SECTION can get into the
                    # alcove.
                    moderate=True_(),
                )
            ),
        ),
        R_THIRD_EXPLOSIVES_CLIFF: (
            ExitData(
                R_BRIDGE_AND_MINES_BUILDING,
                logic_options(
                    # Only expect hover because the cliff gets very thin and is technically not walkable; you slide off
                    # rather slowly.
                    base=HasAbility(HOVER),
                    # Hug the cliff between these two areas, and you won't fall down, unless you're Gonk Droid, but Gonk
                    # Droid can't get up here on its own to begin with.
                    normal=True_(),
                ),
            ),
        ),
        R_BRIDGE_AND_MINES_BUILDING: (
            ExitData(
                R_THIRD_EXPLOSIVES_CLIFF,
                # If the player can get to R_BRIDGE_AND_MINES_BUILDING without going through R_THIRD_EXPLOSIVES_CLIFF,
                # then they already have the necessary jump height to go from the bridge to the slightly higher cliff
                # section.
                logic_options(
                    base=HasAbility(HOVER),
                    normal=True_(),
                ),
                er_rule=logic_options(
                    # Jump up and then only expect hover because the cliff gets very thin and is technically not
                    # walkable; you slide off rather slowly.
                    base=HasAllAbilities(HOVER & CAN_JUMP_0_44),
                    # Jump up and then hug the cliff between these two areas, so you won't fall down.
                    normal=HasAbility(CAN_JUMP_0_44),
                ),
            ),
        ),
        R_BRICK_COVERED_MINIKIT_ALCOVE: (),
    },
    minikits={
        "Minikit Behind Silver Brick Wall": minikit_data(
            R_FAR_LEFT_SILVER_BRICK_SECTION,
            logic_options(
                base=HasAbility(BOUNTY_HUNTER),
                normal=And(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    HasAbility(CAN_JUMP_HEIGHT_0_37),
                ),
                moderate=Or(
                    # Triple jump over the silver brick wall.
                    # The devs made the collision box come forwards at the top, but didn't make it high enough, so
                    # making the collision box come forwards actually helps here.
                    # Triple high jump can get enough height from next to the silver brick wall, whereas Jedi need to
                    # move back a bit from the wall, to the slightly higher area, otherwise they do not get enough
                    # height.
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    And(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        # Astromech droids can also make it up with their hover.
                        HasAnyAbilities(CAN_JUMP_HEIGHT_0_37 | ASTROMECH_DROID),
                    ),
                ),
            ),
            er_rule=logic_options(
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_JUMP_HEIGHT_0_37),
                moderate=Or(
                    # Triple jump over the silver brick wall.
                    # The devs made the collision box come forwards at the top, but didn't make it high enough, so
                    # making the collision box come forwards actually helps here.
                    # Triple high jump can get enough height from next to the silver brick wall, whereas Jedi need to
                    # move back a bit from the wall, to the slightly higher area, otherwise they do not get enough
                    # height.
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    And(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        # Astromech droids can also make it up with their hover.
                        HasAnyAbilities(CAN_JUMP_HEIGHT_0_37 | ASTROMECH_DROID),
                    ),
                ),
            ),
            pickup_name="m_pup3",
        ),
        "Force Platforms High Minikit": minikit_data(
            R_FIRST_EXPLOSIVES_SECTION,
            logic_options(
                # Fight Grievous and explode the first explosives, then force the platforms and double jump up.
                base=HasAbility(JEDI),
                # Triple high jump to skip forcing the platforms.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pup4",
        ),
        "Minikit On Platform With Power Up": minikit_data(
            R_LOW_PLATFORM_WITH_POWER_UP,
            pickup_name="mk_1",
        ),
        R_BRICK_COVERED_MINIKIT_ALCOVE: minikit_data(
            R_BRICK_COVERED_MINIKIT_ALCOVE,
            # The logic for destroying the bricks is defined here.
            # BLASTER works from all regions that can reach here.
            # Self Destruct also works from all regions that can reach here, but is not always expected.
            logic_options(
                base=HasAbility(BLASTER),
                normal=Or(
                    # Ewoks work too.
                    HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    And(
                        # R_FORCE_THIRD_EXPLOSIVES_SECTION also works for slam/explode, but if the player can reach
                        # there, they can also reach Third Explosives Section Gap Area
                        _helper.can_reach_region(R_THIRD_EXPLOSIVES_SECTION_GAP_AREA),
                        Or(
                            # Slam next to the bricks.
                            HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                            # Explode next to the bricks.
                            CAN_USE_SELF_DESTRUCT,
                        ),
                    ),
                ),
                moderate=Or(
                    HasAnyAbilities(BLASTER | WEAPON_EWOK),
                    # Exploding also works from "General Grievous - Shoot Second Explosives Section".
                    CAN_USE_SELF_DESTRUCT,
                    And(
                        _helper.can_reach_region(R_THIRD_EXPLOSIVES_SECTION_GAP_AREA),
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
            pickup_name="mk_0"
        ),
        "Force Third Explosives Minikit": minikit_data(
            R_FORCE_THIRD_EXPLOSIVES_SECTION,
            # The minikit spawns when the explosives are forced into position.
            # The explosives cannot be forced until the first and second explosives have been destroyed and Grievous has
            # jumped up to R_THIRD_EXPLOSIVES_CLIFF.
            # Mostly copied from CAN_EXPLODE_LAST_EXPLOSIVES, but BLASTER is not needed because the explosives do not
            # need to be destroyed to spawn the minikit.
            CAN_EXPLODE_FIRST_TWO_EXPLOSIVES.and_rule(HasAbility(JEDI)),
            pickup_name="m_pup6",
        ),
        "High Minikit Above Third Explosives": minikit_data(
            R_FORCE_THIRD_EXPLOSIVES_SECTION,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                normal=Or(
                    HasAbility(HIGH_JUMP),
                    And(
                        HasAbility(JEDI),
                        Or(
                            # Double Jump + Slam with Stud Magnet active can reach the minikit.
                            Extra.STUD_MAGNET.has(),
                            # Force the third explosives partially out, then jump on top of them as they return, to get
                            # extra height, to then double jump to the minikit.
                            CAN_EXPLODE_FIRST_TWO_EXPLOSIVES,
                        ),
                    ),
                ),
                # Triple jump or high jump to the minikit.
                moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            pickup_name="m_pup5",
        ),
        "Grievous Last Cliff Minikit": minikit_data(
            R_THIRD_EXPLOSIVES_CLIFF,
            pickup_name="m_pup7",
        ),
        "Far Right Low Platform Minikit": minikit_data(
            R_FAR_RIGHT_LOW_PLATFORM,
            pickup_name="m_pup8",
        ),
        "Bridge Minikit": minikit_data(
            R_BRIDGE_AND_MINES_BUILDING,
            pickup_name="m_pup9",
        ),
        "Destroy All Mines Minikit": minikit_data(
            R_BRIDGE_AND_MINES_BUILDING,
            logic_options(
                # Expect a ranged weapon.
                base=HasAnyAbilities(BLASTER | WEAPON_EWOK),
                # Let's hope you have a ranged weapon, Force Ghost or Invincibility, or that Death Link is disabled.
                # P2 can be baited into the mines to avoid dying yourself.
                normal=True_(),
            ),
            pickup_name="m_pup2",
        ),
    },
    power_brick=LocationData(
        R_BRIDGE_AND_MINES_BUILDING,
        HasAbility(JEDI),
    )
)

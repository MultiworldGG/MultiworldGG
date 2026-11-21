from rule_builder.rules import And, Or, False_, True_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_YODA_CLIP,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED, ot_high_jump_ternary
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities, HasAbilityExceptCharacters
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_ACROSS_GAP = "Across Gap"
R_SILVER_BRICKS_SIDE_PATH_LOWER_BEFORE_SILVER_BRICKS = "Silver Bricks Side Path Lower Before Silver Bricks"
R_BEHIND_SITH_FORCE_DOORS = "Behind Sith Force Doors"
R_SILVER_BRICKS_SIDE_PATH_LOWER = "Silver Bricks Side Path Lower"
R_SILVER_BRICKS_SIDE_PATH_UPPER = "Silver Bricks Side Path Upper"
R_PLATFORM_ABOVE_TIN_CANS = "Platform Above Tin Cans"
R_SANDCRAWLER_APPROACH_BEFORE_QUICKSAND = "Sandcrawler Approach Before Quicksand"
R_SANDCRAWLER_GROUND_LEVEL = "Sandcrawler Ground Level"
R_TOP_OF_SANDCRAWLER = "Top Of Sandcrawler"
R_SANDCRAWLER_EXTERIOR_ACCESS_HATCH_EXIT = "Sandcrawler Exterior Access Hatch Exit"
R_SANDCRAWLER_INTERIOR_START = "Sandcrawler Interior Start"
R_SANDCRAWLER_ELEVATOR_ROOM = "Sandcrawler Elevator Room"
R_SANDCRAWLER_TWIN_SWITCHES_ROOM = "Sandcrawler Twin Switches Room"
R_SANDCRAWLER_CAGED_DROIDS_ROOM = "Sandcrawler Caged Droids Room"
R_SANDCRAWLER_LAVA_FLOW = "Sandcrawler Lava Flow"
R_SANDCRAWLER_ENCLOSED_AREA_AFTER_LAVA_FLOW = "Sandcrawler Enclosed Area After Lava Flow"
R_SANDCRAWLER_EXIT_ROOM = "Sandcrawler Exit Room"
R_POST_SANDCRAWLER_SPAWN = "Post-Sandcrawler Spawn"
R_BANTHA_OASIS = "Bantha Oasis"
R_POST_SANDCRAWLER_ELEVATED_GRAPPLE_AREA = "Post-Sandcrawler Elevated Grapple Area"
R_AFTER_QUICKSAND_ARCH = "After Quicksand Arch"
R_LARGE_QUICKSAND_POOL = "Large Quicksand Pool"
R_AFTER_LARGE_QUICKSAND_POOL = "After Large Quicksand Pool"
R_BEFORE_SEA_OF_QUICKSAND = "Before Sea Of Quicksand"
R_ACROSS_SEA_OF_QUICKSAND = "Across Sea Of Quicksand"


THROUGH_THE_JUNDLAND_WASTES = Chapter(
    area=Area.TATOOINE,
    start_region=R_SPAWN,
    intended_completion_path={
        "base": (
            R_ACROSS_GAP,
            R_SANDCRAWLER_APPROACH_BEFORE_QUICKSAND,
            R_SANDCRAWLER_GROUND_LEVEL,
            R_TOP_OF_SANDCRAWLER,
            R_SANDCRAWLER_INTERIOR_START,
            R_SANDCRAWLER_ELEVATOR_ROOM,
            R_SANDCRAWLER_TWIN_SWITCHES_ROOM,
            R_SANDCRAWLER_CAGED_DROIDS_ROOM,
            R_SANDCRAWLER_EXIT_ROOM,
            R_POST_SANDCRAWLER_SPAWN,
            R_AFTER_QUICKSAND_ARCH,
            R_LARGE_QUICKSAND_POOL,
            R_AFTER_LARGE_QUICKSAND_POOL,
            R_BEFORE_SEA_OF_QUICKSAND,
            R_ACROSS_SEA_OF_QUICKSAND,
        ),
        "moderate": (
            R_ACROSS_GAP,
            R_SANDCRAWLER_APPROACH_BEFORE_QUICKSAND,
            R_SANDCRAWLER_GROUND_LEVEL,
            # Skip going to the top of the sandcrawler and activating the suction, by triple jumping into the
            # transition directly.
            R_SANDCRAWLER_INTERIOR_START,
            R_SANDCRAWLER_ELEVATOR_ROOM,
            R_SANDCRAWLER_TWIN_SWITCHES_ROOM,
            R_SANDCRAWLER_CAGED_DROIDS_ROOM,
            R_SANDCRAWLER_EXIT_ROOM,
            R_POST_SANDCRAWLER_SPAWN,
            R_AFTER_QUICKSAND_ARCH,
            R_LARGE_QUICKSAND_POOL,
            R_AFTER_LARGE_QUICKSAND_POOL,
            R_BEFORE_SEA_OF_QUICKSAND,
            R_ACROSS_SEA_OF_QUICKSAND,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_ACROSS_GAP,
                # `HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED` can cross the entire gap, but this is not
                # logically relevant.
                Or(
                    CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_JUMP_HEIGHT_0_37),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
            ),
            ExitData(
                R_SILVER_BRICKS_SIDE_PATH_LOWER_BEFORE_SILVER_BRICKS,
                logic_options(
                    base=HasAbility(HOVER),
                    # Even without high jump enabled, Grievous and Bodyguard can make it with a triple jump.
                    moderate=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                ),
            ),
        ),
        R_ACROSS_GAP: (
            ExitData(
                R_BEHIND_SITH_FORCE_DOORS,
                logic_options(
                    base=CAN_SITH_FORCE,
                    # Triple jump from the elevated area with the Access Hatch, and get over the top of the Sith Force
                    # doors. Yoda cannot get the required distance. Bodyguard can only get the required distance when
                    # high jump is enabled.
                    moderate=Or(
                        CAN_SITH_FORCE,
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                            capped=HasAbility(CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        ),
                    ),
                ),
            ),
            ExitData(
                R_PLATFORM_ABOVE_TIN_CANS,
                logic_options(
                    base=False_(),
                    # Stand on destroyable objects or where the tin cans go, and high jump up.
                    normal=HasAbility(HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                    # Triple jump up.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
            ExitData(
                R_SILVER_BRICKS_SIDE_PATH_UPPER,
                logic_options(
                    # It's not immediately obvious that there is a slightly raised area on the right side, that can be
                    # used to high jump up to the upper area of the silver bricks side path, so using high jump here is
                    # requiring normal+ logic.
                    base=False_(),
                    normal=HasAbility(HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                    # Triple jump up.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
            ExitData(
                R_SANDCRAWLER_APPROACH_BEFORE_QUICKSAND,
                logic_options(
                    base=HasAbility(JEDI),
                    # High jump up is easier on the right side.
                    normal=HasAbility(JEDI) | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Allow triple jump when High Jump is capped.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
                new_level=Level.TATOOINE_D,
            ),
        ),
        R_SILVER_BRICKS_SIDE_PATH_LOWER_BEFORE_SILVER_BRICKS: (
            ExitData(
                R_SILVER_BRICKS_SIDE_PATH_LOWER,
                logic_options(
                    base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    # Allow triple jump, except yoda, as well as high jump when enabled.
                    moderate=Or(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | HIGH_JUMP),
                            capped=HasAbility(CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        ),
                    ),
                    # Allow yoda, who has a harder time getting over the silver bricks due to his low movement speed and
                    # the top of the silver bricks being sloped. To get yoda over the silver bricks,
                    hard=Or(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(JEDI | CAN_TRIPLE_JUMP_GREAT_DISTANCE | HIGH_JUMP),
                            capped=HasAnyAbilities(JEDI | CAN_TRIPLE_JUMP_GREAT_DISTANCE)
                        ),
                    ),
                    # From on top of the silver bricks, it's pretty easy to get onto the edge of the level/out-of-bounds
                    # on the left side. This can be used to get the access hatch minikit.
                ),
            ),
        ),
        R_BEHIND_SITH_FORCE_DOORS: (),
        R_SILVER_BRICKS_SIDE_PATH_LOWER: (
            ExitData(
                R_SILVER_BRICKS_SIDE_PATH_UPPER,
                logic_options(
                    base=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAbility(JEDI),
                    ),
                    # Allow triple jump.
                    # Allow jetpack hover by starting from one of the destroyable objects for extra height, then hover
                    # up the left side. The right side also works, but seems slightly more difficult.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP | JETPACK),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM | JETPACK),
                    ),
                ),
            ),
        ),
        R_SILVER_BRICKS_SIDE_PATH_UPPER: (
            # Drop down. I'm not sure if this is ever logically relevant.
            ExitData(R_ACROSS_GAP),
            # Drop down.
            ExitData(R_SILVER_BRICKS_SIDE_PATH_LOWER),
            ExitData(
                R_PLATFORM_ABOVE_TIN_CANS,
                logic_options(
                    base=HasAbility(HOVER),
                    # Allow triple jump.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                        # Yoda and Bodyguard can't make it (though they can just triple jump up to this platform from
                        # below).
                        capped=HasAnyAbilities(HOVER | CAN_TRIPLE_JUMP_GREAT_DISTANCE)
                    )
                ),
            ),
        ),
        R_PLATFORM_ABOVE_TIN_CANS: (),
        R_SANDCRAWLER_APPROACH_BEFORE_QUICKSAND: (
            ExitData(
                R_SANDCRAWLER_GROUND_LEVEL,
                logic_options(
                    # Hover across the quicksand.
                    # Build the object, push it into position and double jump to the platforms over the quicksand.
                    # High jump straight up to the platforms over the quicksand.
                    base=Or(
                        HasAnyAbilities(HOVER | JEDI) | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        HasAllAbilities(CAN_JUMP_0_44 | CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                    ),
                    # Hug the left side of the cliff, and double jump up to the second platform over the quicksand.
                    # Lower jump height can make it up too, but requires enough movement speed to prevent sliding down.
                    # Boba Fett (Boy) (run_speed=0.8) cannot make the jump.
                    # Clone (run_speed=1.0, jump_height=0.37) can make the jump.
                    normal=Or(
                        HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                        And(
                            HasAllAbilities(CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                            Or(
                                HasAbility(CAN_JUMP_0_44),
                                HasAbilityExceptCharacters(CAN_JUMP_HEIGHT_0_37, Character.BOBA_FETT_BOY)
                                # HasAbilityCombination(CAN_JUMP_HEIGHT_0_37 | RUN_SPEED_1_18_OR_HIGHER),
                            )
                        )
                    ),
                ),
            ),
        ),
        R_SANDCRAWLER_GROUND_LEVEL: (
            ExitData(
                R_TOP_OF_SANDCRAWLER,
                logic_options(
                    base=HasAllAbilities(JEDI | CAN_BUILD_BRICKS | CAN_PULL_LEVERS) & CAN_GRAPPLE,
                    # All forcing the first platform, stacking two boxes, then high jumping up to the first platform.
                    normal=And(
                        HasAllAbilities(JEDI | CAN_PULL_LEVERS),
                        Or(
                            HasAbility(CAN_BUILD_BRICKS) & CAN_GRAPPLE,
                            CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        ),
                    ),
                    moderate=HasAllAbilities(JEDI | CAN_PULL_LEVERS),
                ),
            ),
            ExitData(
                R_SANDCRAWLER_INTERIOR_START,
                logic_options(
                    base=False_(),
                    # Triple jump under the entrance, and you can hit the loading zone without needing to activate the
                    # suction effect.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
                new_level=Level.TATOOINE_B,
            ),
            ExitData(
                R_SANDCRAWLER_EXTERIOR_ACCESS_HATCH_EXIT,
                # Yoda Clip from below.
                logic_options(
                    base=False_(),
                    hard=CAN_YODA_CLIP,
                )
            )
        ),
        # If you Yoda Clipped into here from below, you can Yoda Clip or SHORTIE to get on top of the sandcrawler, but
        # Yoda can just get to the top of the sandcrawler from ground-level on his own anyway, so this is not logically
        # relevant.
        R_SANDCRAWLER_EXTERIOR_ACCESS_HATCH_EXIT: (),
        R_TOP_OF_SANDCRAWLER: (
            ExitData(
                R_SANDCRAWLER_INTERIOR_START,
                HasAllAbilities(CAN_PULL_LEVERS | SHORTIE) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                new_level=Level.TATOOINE_B,
            ),
            ExitData(
                R_SANDCRAWLER_EXTERIOR_ACCESS_HATCH_EXIT,
                HasAbility(SHORTIE),
            )
        ),
        R_SANDCRAWLER_INTERIOR_START: (
            ExitData(
                R_SANDCRAWLER_ELEVATOR_ROOM,
                HasAbility(JEDI),
            ),
        ),
        R_SANDCRAWLER_ELEVATOR_ROOM: (
            ExitData(
                R_SANDCRAWLER_TWIN_SWITCHES_ROOM,
                logic_options(
                    base=HasAbility(ASTROMECH_PANEL),
                    # Ceiling clip and jump into the loading zone.
                    hard=HasAbility(ASTROMECH_PANEL) | CAN_YODA_CLIP,
                ),
            ),
        ),
        R_SANDCRAWLER_TWIN_SWITCHES_ROOM: (
            ExitData(
                R_SANDCRAWLER_CAGED_DROIDS_ROOM,
                HasAllAbilities(CAN_PULL_LEVERS | RUN_SPEED_0_9_OR_HIGHER),
            ),
            ExitData(
                R_SANDCRAWLER_LAVA_FLOW,
                logic_options(
                    base=CAN_SITH_FORCE & HasAbility(SHORTIE),
                    hard=Or(
                        CAN_SITH_FORCE & HasAbility(SHORTIE),
                        # Ceiling clip over the fence.
                        CAN_YODA_CLIP,
                    ),
                ),
            ),
        ),
        R_SANDCRAWLER_CAGED_DROIDS_ROOM: (
            ExitData(
                R_SANDCRAWLER_ENCLOSED_AREA_AFTER_LAVA_FLOW,
                logic_options(
                    base=False_(),
                    # Jump up onto the fence in this room, then hover across to the minikit.
                    # Triple jump is needed to get back.
                    # Note that the fence around the enclosed area with the minikit has collision that reaches the
                    # ceiling, so you must hover around to where there is no fence.
                    moderate=Or(
                        HasAbility(JETPACK),
                        HasAllAbilities(HOVER | CAN_JUMP_0_44),
                    ),
                ).or_rule(
                    # Yoda Clip through the ceiling and over the wall collision of this enclosed area.
                    apply_to="hard+",
                    rule=CAN_YODA_CLIP,
                ),
            ),
            ExitData(
                R_SANDCRAWLER_EXIT_ROOM,
                logic_options(
                    base=HasAbility(PROTOCOL_PANEL),
                    hard=Or(
                        HasAbility(PROTOCOL_PANEL),
                        # Ceiling clip over the door.
                        CAN_YODA_CLIP,
                    ),
                ),
            ),
        ),
        R_SANDCRAWLER_LAVA_FLOW: (
            ExitData(
                R_SANDCRAWLER_ENCLOSED_AREA_AFTER_LAVA_FLOW,
                HasAllAbilities(JEDI | HOVER),
            ),
        ),
        R_SANDCRAWLER_ENCLOSED_AREA_AFTER_LAVA_FLOW: (),
        R_SANDCRAWLER_EXIT_ROOM: (
            ExitData(
                R_POST_SANDCRAWLER_SPAWN,
                # Bizarrely, they can be shot, but not damaged by other sources.
                HasAnyAbilities(JEDI | BLASTER | WEAPON_EWOK),
                new_level=Level.TATOOINE_C,
            ),
        ),
        R_POST_SANDCRAWLER_SPAWN: (
            ExitData(
                R_BANTHA_OASIS,
                logic_options(
                    base=Or(
                        CAN_SITH_FORCE,
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    normal=Or(
                        CAN_SITH_FORCE,
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    # Allow Triple jump.
                    # Allow jumping onto the left cliff edge and hovering across. The terrain is deliberately slippery
                    # to prevent Astromechs from getting across, but Jetpacks can jump first, and then hover, for
                    # slightly more distance.
                    moderate=Or(
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        HasAllAbilities(JETPACK),
                    ),
                ),
            ),
            ExitData(
                R_POST_SANDCRAWLER_ELEVATED_GRAPPLE_AREA,
                logic_options(
                    base=Or(
                        # Build the grapple point, force the hook, then grapple up.
                        HasAllAbilities(CAN_BUILD_BRICKS | JEDI) & CAN_GRAPPLE,
                        # High jump directly up.
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    ),
                    # Allow triple jump.
                    moderate=HasAbility(JEDI) | CAN_ORIGINAL_TRILOGY_HIGH_JUMP
                ),
            ),
            ExitData(
                R_AFTER_QUICKSAND_ARCH,
                # There is anti-hover triggers under the arch, preventing hovering over the quicksand.
                logic_options(
                    base=HasAbility(PROTOCOL_PANEL),
                    # Triple jump to the top right of the arch.
                    moderate=HasAnyAbilities(PROTOCOL_PANEL | JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        ),
        R_BANTHA_OASIS: (),
        R_POST_SANDCRAWLER_ELEVATED_GRAPPLE_AREA: (
            ExitData(
                R_AFTER_QUICKSAND_ARCH,
                logic_options(
                    base=False_(),
                    # Hover to the top right of the arch.
                    normal=HasAbility(JETPACK),
                    # Astromech hover can just barely make it.
                    moderate=HasAbility(HOVER),
                ),
            ),
        ),
        R_AFTER_QUICKSAND_ARCH: (
            ExitData(
                R_LARGE_QUICKSAND_POOL,
                logic_options(
                    # Force the bones to make a bridge.
                    base=HasAbility(JEDI),
                    # Jetpack hover across.
                    # Yoda can also double jump across.
                    normal=HasAnyAbilities(JEDI | JETPACK),
                    moderate=HasAnyAbilities(JEDI | JETPACK | CAN_HIGH_JUMP_SLAM)
                ),
            ),
        ),
        R_LARGE_QUICKSAND_POOL: (
            ExitData(
                R_AFTER_LARGE_QUICKSAND_POOL,
                logic_options(
                    base=HasAllAbilities(CAN_JUMP_0_44 | CAN_PUSH_OBJECTS | PROTOCOL_PANEL | JEDI),
                    # You can hug the right wall to avoid dying in the quicksand. There is one part midway through that
                    # you must jump around, and a second part right at the end.
                    moderate=Or(
                        HasAbility(CAN_BARELY_JUMP),
                        HasAllAbilities(CAN_JUMP_0_44 | CAN_PUSH_OBJECTS | PROTOCOL_PANEL | JEDI)
                    ),
                ),
            ),
        ),
        R_AFTER_LARGE_QUICKSAND_POOL: (
            ExitData(R_BEFORE_SEA_OF_QUICKSAND, new_level=Level.TATOOINE_E),
        ),
        R_BEFORE_SEA_OF_QUICKSAND: (
            ExitData(
                R_ACROSS_SEA_OF_QUICKSAND,
                logic_options(
                    # Fix the landspeeder and ride it across.
                    base=HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES),
                    # Grievous can triple jump across the entire quicksand sea.
                    moderate=Or(
                        HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES),
                        Character.GENERAL_GRIEVOUS.has() & OT_HIGH_JUMP_ENABLED,
                    ),
                ),
            ),
        ),
        R_ACROSS_SEA_OF_QUICKSAND: (
            ExitData(
                "Chapter Completion",
                HasAbility(CAN_PULL_LEVERS),
            ),
        ),
    },
    minikits={
        "Sith Force Area Alcove Minikit": minikit_data(
            R_BEHIND_SITH_FORCE_DOORS,
            logic_options(
                base=HasAbility(JEDI),
                # High jump can jump up on the right side where the minikit alcove is slightly lower.
                normal=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAbility(JEDI),
                ),
                moderate=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            pickup_name="mk_1",
        ),
        "Access Hatch Minikit": minikit_data(
            R_ACROSS_GAP,
            logic_options(
                base=Or(
                    HasAllAbilities(CAN_BUILD_BRICKS | HOVER) & CAN_GRAPPLE,
                    HasAbility(HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                ),
                # Allow double jumping across with Yoda/Ackbar.
                normal=Or(
                    And(
                        HasAbility(CAN_BUILD_BRICKS) & CAN_GRAPPLE,
                        HasAbility(HOVER) | HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                    ),
                    HasAbility(HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                ),
                # Allow triple jump.
                moderate=Or(
                    HasAllAbilities(CAN_BUILD_BRICKS | HOVER) & CAN_GRAPPLE,
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    HasAbility(HIGH_JUMP) & OT_HIGH_JUMP_ENABLED,
                ),
            ).and_rule(
                HasAbility(SHORTIE),
            ).or_rule(
                # Allow walking through the gap as Womp Rat, skipping the access hatch entirely.
                apply_to="moderate+",
                rule=Extra.EXTRA_TOGGLE.has(),
            ),
            pickup_name="mk_0",
        ),
        "Above Tin Cans Minikit": minikit_data(
            R_PLATFORM_ABOVE_TIN_CANS,
            pickup_name="mk_2",
        ),
        "Sandcrawler Exterior Access Hatch Minikit": minikit_data(
            R_SANDCRAWLER_EXTERIOR_ACCESS_HATCH_EXIT,
            pickup_name="m_pup1",
        ),
        "Sandcrawler Elevator Room Minikit": minikit_data(
            R_SANDCRAWLER_ELEVATOR_ROOM,
            # You can also Yoda Grab to get this, but Yoda can just get the minikit the intended way.
            HasAllAbilities(CAN_PULL_LEVERS | CAN_PUSH_OBJECTS),
            pickup_name="mk_1",
        ),
        "Sandcrawler Lava Platform Minikit": minikit_data(
            R_SANDCRAWLER_ENCLOSED_AREA_AFTER_LAVA_FLOW,
            pickup_name="mk_0",
        ),
        "Bantha Oasis Minikit": minikit_data(
            R_BANTHA_OASIS,
            logic_options(
                base=HasAbility(CAN_RIDE_VEHICLES),
                # Yoda can also magically grab this through the wall without needing to activate the buttons.
                # Droideka and Grievous also can with a character swap.
                moderate=Or(
                    HasAbility(CAN_RIDE_VEHICLES),
                    Character.has_any(Character.DROIDEKA, Character.GENERAL_GRIEVOUS),
                ),
            ),
            pickup_name="mk_0",
        ),
        "Grapple And Fight Tusken Raiders Minikit": minikit_data(
            R_POST_SANDCRAWLER_ELEVATED_GRAPPLE_AREA,
            pickup_name="mk_1",
        ),
        "Collapse The Column Minikit": minikit_data(
            R_LARGE_QUICKSAND_POOL,
            logic_options(
                base=HasAllAbilities(HOVER | CAN_JUMP_0_44) | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                # Allow triple jump.
                moderate=Or(
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    HasAllAbilities(HOVER | CAN_JUMP_0_44),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
            ),
            pickup_name="mk_2",
        ),
        "Minikit Far Out In Quicksand Sea": minikit_data(
            R_BEFORE_SEA_OF_QUICKSAND,
            And(
                HasAllAbilities(CAN_BUILD_BRICKS | CAN_RIDE_VEHICLES),
                HasAbility(CAN_DOUBLE_JUMP) | CAN_GRAPPLE
            ),
            pickup_name="m_pup1",
        )
    },
    power_brick=LocationData(
        R_SILVER_BRICKS_SIDE_PATH_LOWER,
        logic_options(
            base=ot_high_jump_ternary(
                uncapped=HasAllAbilities(JEDI | CAN_PUSH_OBJECTS) & HasAnyAbilities(HOVER | HIGH_JUMP),
                capped=HasAllAbilities(JEDI | HOVER | CAN_PUSH_OBJECTS),
            ),
            # Triple jump across the gap between the raised areas.
            # Even with OT High Jump enabled, regular high jump cannot get up to the first raised area where the force
            # blocks are, due to not getting enough jump distance.
            moderate=HasAbility(CAN_PUSH_OBJECTS) & HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
        ),
    ),
    ridables={
        Character.BANTHA: LocationData(R_SPAWN),
        Character.DEWBACK: LocationData(
            R_ACROSS_SEA_OF_QUICKSAND,
            logic_options(
                # Expect fighting the Stormtroopers
                base=CAN_DAMAGE_AT_CLOSE_RANGE,
                normal=True_(),
            ),
        ),
        Character.SPEEDER_LAND: LocationData(R_BEFORE_SEA_OF_QUICKSAND, HasAbility(CAN_BUILD_BRICKS)),
    },
)

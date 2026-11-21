from rule_builder.rules import And, Or, True_, False_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_YODA_CLIP,
    CAN_GRAPPLE,
    HAS_ANY_YODA,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT,
    CAN_USE_DEFLECT_BOLTS,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
    HAS_HIGH_JUMP_EXCEPT_BODYGUARD_OT,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
    HasAnyCharacterExcept,
    HasAbilityExceptCharacters,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level


from ....character_ability import *

R_SKIFF_1 = "Skiff 1"
R_SKIFF_2 = "Skiff 2"
R_SKIFF_3_BOBA_FIGHT = "Skiff 3 (Boba Fight)"
R_SKIFF_4 = "Skiff 4"
R_SAIL_BARGE_RIGHT_SIDE = "Sail Barge Right Side"
R_SAIL_BARGE_FRONT_AND_LEFT_SIDE = "Sail Barge Front and Left Side"
R_SAIL_BARGE_FRONT_RAISED_LEVERS_AREA = "Sail Barge Front Raised Levers Area"
R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA = "Sail Barge Left Side Upper Area"
R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA_END = "Sail Barge Left Side Upper Area End"
R_SAIL_BARGE_REAR = "Sail Barge Rear"
R_SAIL_BARGE_REAR_UPPER_LEVERS_AREA = "Sail Barge Rear Upper Levers Area"
R_SAIL_BARGE_REAR_INTERIOR = "Sail Barge Rear Interior"
R_SAIL_BARGE_REAR_INTERIOR_LIFT_ROOM = "Sail Barge Rear Interior Lift Room"
R_SAIL_BARGE_REAR_INTERIOR_ACCESS_HATCH_AREA = "Sail Barge Rear Interior Access Hatch Area"
R_SAIL_BARGE_MAIN_INTERIOR_SPAWN = "Sail Barge Main Interior Spawn"
R_SAIL_BARGE_MAIN_INTERIOR_POST_DISCO = "Sail Barge Main Interior Post Disco"
R_SAIL_BARGE_DECK = "Sail Barge Deck"
R_SAIL_BARGE_FIRST_PLATFORM_BENEATH_FRONT_SAIL = "Sail Barge First Platform Beneath Front Sail"
R_SAIL_BARGE_MINIKIT_PLATFORM_BENEATH_FRONT_SAIL = "Sail Barge Minikit Platform Beneath Front Sail"

_CAN_DAMAGE_BOBA_FETT = logic_options(
    base=CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT,
    # Allow defeating Boba Fett by deflecting his bolts back at him. This is awkward because if you're too close, Boba
    # will melee you instead.
    hard=CAN_DAMAGE_AT_CLOSE_RANGE_NO_SELF_DESTRUCT | CAN_USE_DEFLECT_BOLTS
)
"""For some reason, Boba Fett is immune to explosions, so Self Destruct is not a suitable source of damage."""

_helper = ChapterHelper(
    area=Area.SARLACCPIT,
    start_region=R_SKIFF_1,
)

_LEFT_SIDE_ACTIVATE_BOTH_PLATFORMS_TO_REAR = logic_options(
    # Expect Jedi to move the panels covering the lever in the lower area.
    base=And(
        _helper.can_reach_region(R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA),
        HasAllAbilities(JEDI | CAN_PULL_LEVERS)
    ),
    # Skip the Jedi requirement.
    normal=And(
        _helper.can_reach_region(R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA),
        HasAbility(CAN_PULL_LEVERS)
    ),
)

_RIGHT_SIDE_ACTIVATE_ALL_PLATFORMS_TO_REAR = logic_options(
    # Force one of the panels to stand on, jump up to the pushable box and push it down.
    # Build the grapple point and grapple up.
    # Walk through the upper area and pull the lever.
    # Expect Jedi to move the panels covering the lever in the lower area.
    # All jedi can push objects, pull levers and build bricks.
    base=HasAbility(JEDI) & CAN_GRAPPLE,
    # Alternatively, substitute JEDI for HIGH_JUMP when enabled.
    normal=Or(
        HasAbility(JEDI),
        # The platform with the pushable box is easily reachable with HIGH_JUMP.
        HasAllAbilities(HIGH_JUMP | CAN_PUSH_OBJECTS | CAN_PULL_LEVERS | CAN_BUILD_BRICKS) & OT_HIGH_JUMP_ENABLED,
    ) & CAN_GRAPPLE,
)

THE_GREAT_PIT_OF_CARKOON = _helper.make_chapter(
    intended_completion_path={
        "base": (
            R_SKIFF_2,
            R_SKIFF_3_BOBA_FIGHT,
            R_SKIFF_4,
            R_SAIL_BARGE_RIGHT_SIDE,
            R_SAIL_BARGE_REAR,
            R_SAIL_BARGE_REAR_INTERIOR,
            R_SAIL_BARGE_REAR_INTERIOR_LIFT_ROOM,
            R_SAIL_BARGE_MAIN_INTERIOR_SPAWN,
            R_SAIL_BARGE_MAIN_INTERIOR_POST_DISCO,
            R_SAIL_BARGE_DECK,
        ),
    },
    regions={
        R_SKIFF_1: (
            ExitData(
                R_SKIFF_2,
                logic_options(
                    base=HasAllAbilities(CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
                    # Allow hovering across from the fence of the first Skiff, to the fence of the second Skiff.
                    normal=Or(
                        HasAllAbilities(CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
                        HasAbility(HOVER),
                    ),
                    # While it is fairly simple to jump across with a double jump, it is not in any way obvious that
                    # only the very back of the skiff can be stood on, and that the sides on the back of the skiff are
                    # slippery.
                    moderate=Or(
                        HasAllAbilities(CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37),
                        HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                    )
                )
            ),
        ),
        R_SKIFF_2: (
            ExitData(
                R_SKIFF_3_BOBA_FIGHT,
                # Note: Dive rolls can get enough distance to cross the gap, but then always seem to slide off and die.
                logic_options(
                    base=HasAllAbilities(JEDI | CAN_PULL_LEVERS),
                    # There is a slight complication here for Normal logic, in that, if the player hovers across to
                    # Skiff 2, then P2's AI won't follow, meaning that the player will need to pull both levers
                    # themselves. While all Jedi can pull both levers themselves, it is not obvious because the timing
                    # window is tight, so Normal logic expects pulling the levers on the first Skiff to allow P2's AI to
                    # help with the levers on Skiff 2.
                    # Regular Astromech Hover cannot hover across to the fence on Skiff 3, it's too high, so only
                    # Jetpack hover is allowed.
                    normal=Or(
                        HasAllAbilities(CAN_PULL_LEVERS | CAN_BUILD_BRICKS | CAN_JUMP_HEIGHT_0_37 | JEDI),
                        HasAbility(JETPACK),
                    ),
                    # Allow double jump and astromech hover.
                    moderate=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                )
            ),
        ),
        R_SKIFF_3_BOBA_FIGHT: (
            ExitData(
                R_SKIFF_4,
                # Only Boba Fett needs to be defeated for Skiff 4 to move into place.
                _CAN_DAMAGE_BOBA_FETT,
            ),
        ),
        R_SKIFF_4: (
            ExitData(
                R_SAIL_BARGE_RIGHT_SIDE,
                logic_options(
                    base=HasAbility(JEDI),
                    # Allow hover.
                    normal=HasAnyAbilities(JEDI | HOVER),
                    # Allow triple jump with slam characters.
                    moderate=HasAnyAbilities(JEDI | HOVER | CAN_HIGH_JUMP_SLAM),
                    # Allow double jump.
                    hard=HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                ),
            ),
            ExitData(
                R_SAIL_BARGE_FRONT_AND_LEFT_SIDE,
                logic_options(
                    base=CAN_SITH_FORCE,
                    # Allow extra distance double jump, and high jump when enabled (except bodyguard)
                    normal=Or(
                        CAN_SITH_FORCE, HasAbility(HOVER),
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                        HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD) & OT_HIGH_JUMP_ENABLED,
                    ),
                    moderate=Or(
                        CAN_SITH_FORCE,
                        HasAbility(HOVER),
                        HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GRIEVOUS_BODYGUARD)
                    ),

                )
            ),
            ExitData(
                R_SAIL_BARGE_FRONT_RAISED_LEVERS_AREA,
                # The cable connecting the skiff to the barge has collision. While it is difficult to stand on for any
                # time without sliding off, it does allow you to jump again, so you can jump most of the way up, and
                # then triple jump to the raised area with the levers.
                logic_options(
                    base=False_(),
                    hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                )
            )
        ),
        R_SAIL_BARGE_RIGHT_SIDE: (
            ExitData(
                R_SAIL_BARGE_REAR,
                logic_options(
                    base=_RIGHT_SIDE_ACTIVATE_ALL_PLATFORMS_TO_REAR,
                    # Allow activating only the first and third platforms and hovering across.
                    normal=Or(
                        HasAllAbilities(CAN_PULL_LEVERS | HOVER),
                        _RIGHT_SIDE_ACTIVATE_ALL_PLATFORMS_TO_REAR,
                    ),
                    # Allow triple jumps to cross with only the first and third platforms activated.
                    moderate=Or(
                        HasAllAbilities(CAN_PULL_LEVERS | JEDI),
                        HasAllAbilities(CAN_PULL_LEVERS | CAN_HIGH_JUMP_SLAM),
                        HasAllAbilities(CAN_PULL_LEVERS | HOVER),
                        _RIGHT_SIDE_ACTIVATE_ALL_PLATFORMS_TO_REAR,
                    ),
                ),
            ),
        ),
        R_SAIL_BARGE_FRONT_AND_LEFT_SIDE: (
            ExitData(
                R_SAIL_BARGE_FRONT_RAISED_LEVERS_AREA,
                logic_options(
                    strict=False,
                    base=CAN_GRAPPLE,
                    # Allow triple high jump and Yoda's slightly higher triple jump.
                    moderate=Or(
                        CAN_GRAPPLE,
                        HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED,
                        HAS_ANY_YODA & HasAnyCharacterExcept(Character.YODA, Character.YODA_GHOST),
                    ),
                    # todo: You can also get up here with Bodyguard's non-high-jump triple jump + character swap to an
                    #  astromech, but I haven't figured out which combinations work. This would be Hard+ logic only due
                    #  to requiring a specific combination of 2 characters.
                ),
            ),
            ExitData(
                R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA,
                logic_options(
                    base=CAN_GRAPPLE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Allow triple jump.
                    moderate=Or(
                        CAN_GRAPPLE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    )
                ),
            ),
            ExitData(
                R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA_END,
                logic_options(
                    base=False_(),
                    # Triple jump directly to the end where the minikit is.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            ExitData(
                R_SAIL_BARGE_REAR,
                _LEFT_SIDE_ACTIVATE_BOTH_PLATFORMS_TO_REAR.or_rule(
                    # Right platform activated.
                    apply_to="normal+",
                    rule=logic_options(
                        base=False_(),
                        normal=HasAbility(CAN_PULL_LEVERS) & Or(
                            HasAbility(HOVER),
                            HAS_HIGH_JUMP_EXCEPT_BODYGUARD_OT,
                        ),
                        moderate=And(
                            HasAbility(CAN_PULL_LEVERS) & Or(
                                HasAnyAbilities(HOVER | JEDI | CAN_HIGH_JUMP_SLAM),
                                HAS_HIGH_JUMP_EXCEPT_BODYGUARD_OT,
                            )
                        ),
                    )
                ).or_rule(
                    # Neither platform activated.
                    apply_to="normal+",
                    rule=HasAbility(JETPACK),
                )
            ),
        ),
        R_SAIL_BARGE_FRONT_RAISED_LEVERS_AREA: (),
        R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA: (
            ExitData(
                R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA_END,
                # Activate the panels in the lower area, and destroy the silver bricks at the end.
                HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ),
        ),
        R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA_END: (),
        R_SAIL_BARGE_REAR: (
            ExitData(
                R_SAIL_BARGE_REAR_UPPER_LEVERS_AREA,
                logic_options(
                    base=HasAbility(CAN_BUILD_BRICKS) & CAN_GRAPPLE,
                    # Use the force to move up one of the panels covering the colors, then stand on top of the panel and
                    # triple jump up.
                    moderate=HasAbility(JEDI) | HasAllAbilities(CAN_BUILD_BRICKS | GRAPPLE),
                ),
            ),
            ExitData(
                R_SAIL_BARGE_REAR_INTERIOR,
                HasAllAbilities(JEDI | CAN_PUSH_OBJECTS),
                new_level=Level.SARLACCPIT_B,
            ),
        ),
        R_SAIL_BARGE_REAR_UPPER_LEVERS_AREA: (),

        # JEDI is strictly required from here on.
        R_SAIL_BARGE_REAR_INTERIOR: (
            # JEDI can destroy the objects and build and ride the turret to proceed.
            ExitData(R_SAIL_BARGE_REAR_INTERIOR_LIFT_ROOM),
        ),
        R_SAIL_BARGE_REAR_INTERIOR_LIFT_ROOM: (
            ExitData(
                R_SAIL_BARGE_REAR_INTERIOR_ACCESS_HATCH_AREA,
                logic_options(
                    base=HasAbility(SHORTIE),
                    # Just ceiling clip to get into the Access Hatch area.
                    hard=HasAbility(SHORTIE) | CAN_YODA_CLIP,
                )
            ),
            ExitData(
                R_SAIL_BARGE_MAIN_INTERIOR_SPAWN,
                logic_options(
                    base=HasAbility(PROTOCOL_PANEL),
                    # The collider that blocks access to the next area doesn't actually spawn until you fully build the
                    # generator object, so if you can reach the transition, you can skip the Protocol Panel.
                    # JEDI is required to reach here, so just triple jump up.
                    moderate=True_(),
                ),
            ),
        ),
        R_SAIL_BARGE_REAR_INTERIOR_ACCESS_HATCH_AREA: (),
        R_SAIL_BARGE_MAIN_INTERIOR_SPAWN: (
            # No logical relevance currently.
            # ExitData(
            #     "Sail Barge Main Interior Storage Room",
            #     logic_options(
            #         base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
            #         # Allow Yoda Ceiling Clip. Stand on top of the silver bricks to get enough height.
            #         hard=CAN_DESTROY_CLOSE_SILVER_BRICKS | CAN_YODA_CLIP,
            #     )
            # ),
            ExitData(
                R_SAIL_BARGE_MAIN_INTERIOR_POST_DISCO,
                logic_options(
                    base=HasAbility(GRAPPLE),
                    # Allow Force Grapple Leap.
                    normal=HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has(),
                    # Triple jump up instead of needing to grapple.
                    moderate=True_(),
                    # # Allow Yoda Ceiling Clip from the top area (triple jump to get up initially.
                    # hard=HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has() | CAN_YODA_CLIP,
                ),
            ),
        ),
        R_SAIL_BARGE_MAIN_INTERIOR_POST_DISCO: (
            ExitData(
                R_SAIL_BARGE_DECK,
                new_level=Level.SARLACCPIT_C,
            ),
        ),
        # Because JEDI is required to reach here, the R_SAIL_BARGE_DECK region covers pretty much the entire deck
        # because any JEDI can traverse pretty much the entire deck.
        R_SAIL_BARGE_DECK: (
            ExitData(
                R_SAIL_BARGE_FIRST_PLATFORM_BENEATH_FRONT_SAIL,
                logic_options(
                    # Expect Grappling up because the double jump up is a bit awkward due to easily hitting your head if
                    # you don't jump far enough away with the initial jump before double jumping up.
                    base=CAN_GRAPPLE,
                    # There is a porthole to destroy, which then lets you force smaller platforms onto the sail's
                    # 'mast', which can be jumped up with a JEDI.
                    normal=True_(),
                ),
            ),
            ExitData(
                "Chapter Completion",
                # Push the explosives on the side close to the camera, activate the Protocol Panel on the other side,
                # then reload the big cannon through its Astromech Panel, and shoot the targets.
                logic_options(
                    base=HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL),
                    # Allow destroying the targets without using the big cannon.
                    normal=Or(
                        HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL),
                        HasAbility(PROTOCOL_PANEL) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    )
                ),
            ),
        ),
        R_SAIL_BARGE_FIRST_PLATFORM_BENEATH_FRONT_SAIL: (
            # Logic skips the second platform because all JEDI can jump across to it.
            ExitData(
                R_SAIL_BARGE_MINIKIT_PLATFORM_BENEATH_FRONT_SAIL,
                logic_options(
                    # Base logic expects CAN_GRAPPLE to get here, which is enough to get to the minikit platform.
                    base=True_(),
                    # Grapple or HIGH_JUMP up.
                    normal=HasAbility(GRAPPLE) | Extra.FORCE_GRAPPLE_LEAP.has() | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Triple jump up with a JEDI.
                    moderate=True_(),
                ),
            ),
        ),
        R_SAIL_BARGE_MINIKIT_PLATFORM_BENEATH_FRONT_SAIL: (),
    },
    minikits={
        "Build Four Skiff Cannons Minikit": minikit_data(
            R_SKIFF_2,
            # All jedi can reach the minikit.
            HasAllAbilities(CAN_PULL_LEVERS | JEDI | CAN_BUILD_BRICKS),
            pickup_name="m_pup2",
        ),
        "Skiff Walk The Plank Minikit": minikit_data(
            R_SKIFF_2,
            logic_options(
                # Expect HOVER to easily grab the minikit without dying.
                base=HasAbility(HOVER),
                # If you can reach R_SKIFF_2, then you can reach the minikit.
                normal=True_(),
            ),
            pickup_name="mk_0",
        ),
        "Barge Rear Three Levers Minikit": minikit_data(
            R_SAIL_BARGE_REAR_UPPER_LEVERS_AREA,
            # All jedi/sith can pull levers.
            # All jedi/sith as AI can pull both regular levers
            logic_options(
                # Require getting P2's AI to follow.
                base=And(
                    Or(
                        # AI will only jump across when all 3 platforms are extended, but will happily jump across with
                        # any character that can jump.
                        And(
                            _helper.can_reach_region(R_SAIL_BARGE_RIGHT_SIDE),
                            _RIGHT_SIDE_ACTIVATE_ALL_PLATFORMS_TO_REAR
                        ),
                        # AI won't even attempt to cross the gap unless the first platform is extended.
                        # AI will only use astromechs to cross.
                        # AI will die repeatedly if only the first platform is extended.
                        And(
                            _helper.can_reach_region(R_SAIL_BARGE_FRONT_AND_LEFT_SIDE),
                            HasAbility(ASTROMECH_DROID),
                            _LEFT_SIDE_ACTIVATE_BOTH_PLATFORMS_TO_REAR,
                        ),
                    ),
                    CAN_GRAPPLE,
                    CAN_SITH_FORCE
                ),
                # If needed, drop in P2 and then drop them out to teleport them to P1.
                normal=CAN_GRAPPLE & CAN_SITH_FORCE,
            ),
            pickup_name="m_pup3",
        ),
        "Barge Front Between Two Levers Minikit": minikit_data(
            R_SAIL_BARGE_FRONT_RAISED_LEVERS_AREA,
            CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_BUILD_BRICKS),
            er_rule=(
                (
                    (CAN_DAMAGE_AT_CLOSE_RANGE & HasAbility(CAN_JUMP_HEIGHT_0_37))
                    | CAN_DESTROY_CLOSE_SILVER_BRICKS
                )
                & HasAbility(CAN_BUILD_BRICKS)
            ),
            pickup_name="m_pup1",
        ),
        "Barge Left Side Minikit": minikit_data(
            R_SAIL_BARGE_LEFT_SIDE_UPPER_AREA_END,
            # Access to the region contains all the logic necessary to reach the minikit.
            pickup_name="mk_2",
        ),
        "Barge Interior Access Hatch Minikit": minikit_data(
            R_SAIL_BARGE_REAR_INTERIOR_ACCESS_HATCH_AREA,
            pickup_name="m_pup1",
        ),
        "Barge Interior Window Shutters Minikit": minikit_data(
            R_SAIL_BARGE_MAIN_INTERIOR_POST_DISCO,
            # JEDI is required to reach here, so there are no requirements.
            pickup_name="m_pup2",
        ),
        "Barge Deck Minikit Beneath Sail": minikit_data(
            R_SAIL_BARGE_MINIKIT_PLATFORM_BENEATH_FRONT_SAIL,
            pickup_name="mk_0",
        ),
        "Minikit Between Barge Deck Targets": minikit_data(
            R_SAIL_BARGE_DECK,
            logic_options(
                # Expect using the big cannon to destroy the target closest to the camera.
                base=HasAbility(ASTROMECH_PANEL),
                normal=HasAbility(ASTROMECH_PANEL) | CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ),
            pickup_name="mk_1",
        ),
        "Barge Deck Access Hatch Minikit": minikit_data(
            R_SAIL_BARGE_DECK,
            logic_options(
                base=HasAbility(SHORTIE),
                # It's possible to grab this through the wall with Yoda + General Grievous by walking against the fence
                # close to the minikit as Grievous and then swapping to Yoda.
                # todo: I don't know what other combinations work.
                hard=Or(
                    HasAbility(SHORTIE),
                    HAS_ANY_YODA & Character.has_any(
                        Character.GENERAL_GRIEVOUS,
                    ),
                )
            ),
            pickup_name="mk_2",
        ),
    },
    power_brick=LocationData(
        R_SAIL_BARGE_DECK,
        logic_options(
            # Maybe Base logic could require HOVER to go between the platforms, but double jumps work and JEDI is
            # required to reach here.
            base=CAN_GRAPPLE,
            # Grievous and Bodyguard, with OT High Jump enabled, can barely jump from the box, containing the grapple
            # point bricks, to the closest platform. Tarpals and Jar Jar have slightly worse high jump height, so
            # cannot make this jump (or if they can, it's too difficult for Normal logic).
            # Destroying the box means restarting the level, and because this is right at the end of the level, I am not
            # including this in Normal logic for now.
            # normal=Or(
            #     CAN_GRAPPLE,
            #     HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED,
            # ),
            # Just triple jump directly to the Power Brick.
            moderate=True_(),
        )
    ),
    ridables={
        Character.CANNON: LocationData(
            R_SKIFF_1,
            HasAbility(JEDI) | (HasAbility(CAN_BUILD_BRICKS) & CAN_DAMAGE_AT_CLOSE_RANGE)
        ),
        Character.BIGGUN: LocationData(
            # Does not need to be reloaded to get in.
            R_SAIL_BARGE_DECK,
        ),
    }
)

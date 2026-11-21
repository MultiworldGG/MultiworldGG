from rule_builder.rules import And, Or, True_, False_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_YODA_CLIP,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    HAS_ANY_YODA,
    HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
    HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED, ot_high_jump_ternary
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
    HasAbilityExceptCharacters,
    HasAnyCharacterExcept,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_FIRST_CORRIDOR = "First Corridor"
R_HANGAR_OBSERVATION_AND_CONTROL_ROOM = "Hangar Observation And Control Room"
R_TWIN_CORRIDORS_SPAWN = "Twin Corridors Spawn"
R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP = "Twin Corridors Right Corridor Across Gap"
R_TWIN_CORRIDORS_LEFT_CORRIDOR_ACROSS_BRIDGE_GAP = "Twin Corridors Left Corridor Across Bridge Gap"
R_TURNTABLE_BRIDGE_ROOM = "Turntable Bridge Room"
R_IMPERIAL_DATA_CENTER_ROOM = "Imperial Data Center Room"
R_AFTER_IMPERIAL_PHONES_ROOM_IMPERIAL_PANEL_AND_HOLDING_CELLS = \
    "After Imperial Phones Room Imperial Panel, And Holding Cells"


helper = ChapterHelper(
    area=Area.DEATHSTARRESCUE,
    start_region=R_SPAWN
)

RESCUE_THE_PRINCESS = helper.make_chapter(
    intended_completion_path={
        "base": (
            R_FIRST_CORRIDOR,
            R_HANGAR_OBSERVATION_AND_CONTROL_ROOM,
            R_TWIN_CORRIDORS_SPAWN,
            R_TWIN_CORRIDORS_LEFT_CORRIDOR_ACROSS_BRIDGE_GAP,
            R_TURNTABLE_BRIDGE_ROOM,
            R_IMPERIAL_DATA_CENTER_ROOM,
            R_AFTER_IMPERIAL_PHONES_ROOM_IMPERIAL_PANEL_AND_HOLDING_CELLS,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_FIRST_CORRIDOR,
                HasAbility(JEDI),
            ),
        ),
        R_FIRST_CORRIDOR: (
            ExitData(
                R_HANGAR_OBSERVATION_AND_CONTROL_ROOM,
                # Base logic would also expect defeating the Stormtroopers, but all Jedi can do that.
                logic_options(
                    base=HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT),
                    # Ceiling clip to bypass the panel.
                    hard=Or(
                        HasAnyAbilities(IMPERIAL | CAN_WEAR_HAT),
                        CAN_YODA_CLIP,
                    )
                ),
            ),
        ),
        R_HANGAR_OBSERVATION_AND_CONTROL_ROOM: (
            ExitData(
                R_TWIN_CORRIDORS_SPAWN,
                # All Jedi can build bricks
                # base=HasAllAbilities(CAN_BUILD_BRICKS | ASTROMECH_PANEL),
                # While Hard logic could Yoda Ceiling Clip past the door, the level transition is not active until
                # the Astromech Panel is activated, so skipping over the door is useless.
                HasAbility(ASTROMECH_PANEL),
                new_level=Level.DEATHSTARRESCUE_B,
            ),
        ),
        R_TWIN_CORRIDORS_SPAWN: (
            ExitData(
                R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP,
                logic_options(
                    base=HasAbility(HOVER),
                    # Yoda's extra double jump distance makes this easy with him.
                    # Ackbar's double-jump-dive makes this easy with him.
                    # Captain Tarpals and Jar Jar Binks can also cross this gap without too much trouble due to their
                    # higher movement speed than Jedi, but this is especially niche knowledge, so is not considered for
                    # Normal logic.
                    # All high jumpers can cross the gap without much trouble when OT High jump is enabled
                    normal=Or(
                        HasAbility(HOVER),
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                    ),
                    moderate=Or(
                        HasAbility(HOVER),
                        ot_high_jump_ternary(
                            # Jedi can barely cross the gap with a double jump, a triple jump can also be used, but is
                            # similar in difficulty because of the air movement speed at the end of a triple jump, and
                            # the fact that a triple jump here gets way too much height, making landing across the gap,
                            # without sliding off into the pit, more difficult.
                            uncapped=HasAbility(CAN_DOUBLE_JUMP),
                            # The triple jump is possible, but sucks with Grievous, due to his large size and
                            # unremarkable movement speed. Grievous' bodyguard is smaller and has high movement speed,
                            # so it's triple jump to cross the gap isn't that bad.
                            capped=HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GENERAL_GRIEVOUS),
                        ),
                    ),
                    # Now also allows General Grievous when OT High Jump is not enabled.
                    hard=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                ),
            ),
            ExitData(
                R_TWIN_CORRIDORS_LEFT_CORRIDOR_ACROSS_BRIDGE_GAP,
                logic_options(
                    # AI will only cross with Hover, but we'll allow high jump characters that have good distance.
                    base=ot_high_jump_ternary(
                        uncapped=HasAbility(HOVER) | HasAbilityExceptCharacters(HIGH_JUMP,
                                                                                Character.GRIEVOUS_BODYGUARD),
                        capped=HasAbility(HOVER),
                    ),
                    # The jump isn't that bad with all Jedi/Tarpals/Jar Jar.
                    # Grievous and Bodyguard don't seem to be able to make it across if they cannot high jump.
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                        capped=Or(
                            HasAbility(HOVER),
                            HasAbilityExceptCharacters(CAN_DOUBLE_JUMP,
                                                       Character.GENERAL_GRIEVOUS, Character.GRIEVOUS_BODYGUARD)
                        )
                    ),
                    # Triple jump allows all double jump characters to cross.
                    moderate=HasAnyAbilities(HOVER | CAN_DOUBLE_JUMP),
                # Force the bridge across from the right side.
                # ).or_rule(helper.can_reach_region(R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP) & HasAbility(JEDI))
                # JEDI is required at the start of the chapter so checking for it can be skipped.
                # There are no cases where you would be able to reach this region, but not cross the bridge gap.
                # ).or_rule(helper.can_reach_region(R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP))
                ),
            ),
        ),
        R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP: (
            # There is a one-way door that requires destroying an object on this side of the door to open it.
            ExitData(
                R_TWIN_CORRIDORS_LEFT_CORRIDOR_ACROSS_BRIDGE_GAP,
            ),
            # There is a Sith Force door here, but it takes you to an area that is always accessible from
            # R_TWIN_CORRIDORS_LEFT_CORRIDOR_ACROSS_BRIDGE_GAP, and there is already an entrance to that region that
            # requires nothing.
        ),
        R_TWIN_CORRIDORS_LEFT_CORRIDOR_ACROSS_BRIDGE_GAP: (
            # A Jedi is needed at the start of the chapter, so there is no need to logically separate 'after explosives'
            # as a new region.
            # ExitData(
            #     "Twin Corridors Left Corridor After Explosives",
            #     # These explosives cannot be destroyed by melee attacks for some reason, so a blaster, slam, or
            #     # explosion are needed.
            #     # todo: Check that Ewok attacks work.
            #     er_rule=logic_options(
            #         base=HasAnyAbilities(BLASTER | JEDI | CAN_HIGH_JUMP_SLAM | WEAPON_EWOK),
            #         normal=Or(
            #             HasAnyAbilities(BLASTER | JEDI | CAN_HIGH_JUMP_SLAM),
            #             CAN_DESTROY_CLOSE_SILVER_BRICKS,
            #         ),
            #         moderate=Or(
            #             HasAnyAbilities(BLASTER | JEDI | CAN_HIGH_JUMP_SLAM),
            #             CAN_DESTROY_CLOSE_SILVER_BRICKS,
            #             # Jump up the left side of the explosives, and then a short character can walk over the top.
            #             And(
            #                 HasAbility(CAN_JUMP_HEIGHT_0_37),
            #                 Or(
            #                     HasAbility(ASTROMECH_DROID),
            #                     # todo: There are probably more characters.
            #                     # Try: Jawa/Ugnaught/Gonk Droid/PK Droid/Pit Droid/Ewok/Wicket
            #                     Character.has_any(
            #                         # Character.YODA,  # Can slam, so irrelevant.
            #                         # Character.YODA_GHOST,  # Can slam, so irrelevant.
            #                         Character.BOBA_FETT_BOY,
            #                     ),
            #                     # Mouse Droid is tiny.
            #                     Extra.EXTRA_TOGGLE.has(),
            #                 ),
            #             )
            #         )
            #     )
            # ),
            ExitData(
                R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP,
                logic_options(
                    base=False_(),
                    # The one-way door can be opened from the wrong side with a large enough AOE attack.
                    moderate=Or(
                        Extra.SUPER_JEDI_SLAM.has(),
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    ),
                ),
            ),
            ExitData(
                R_TURNTABLE_BRIDGE_ROOM,
                # While Yoda can ceiling clip over the door, the level transition is not active until the Imperial panel
                # is used.
                HasAnyAbilities(CAN_WEAR_HAT | IMPERIAL),
                new_level=Level.DEATHSTARRESCUE_C,
            ),
        ),
        R_TURNTABLE_BRIDGE_ROOM: (
            ExitData(
                R_IMPERIAL_DATA_CENTER_ROOM,
                logic_options(
                    # The platforms are too high for High Jump.
                    base=CAN_GRAPPLE,
                    # # Allow triple jump.
                    # moderate=HasAnyAbilities(JEDI | GRAPPLE | CAN_HIGH_JUMP_SLAM),
                    # A Jedi is required at the start of the chapter.
                    moderate=True_(),
                ),
            ),
        ),
        R_IMPERIAL_DATA_CENTER_ROOM: (
            ExitData(
                # "After Imperial Phones Room Imperial Panel",
                R_AFTER_IMPERIAL_PHONES_ROOM_IMPERIAL_PANEL_AND_HOLDING_CELLS,
                logic_options(
                    strict=False,
                    base=HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE
                # Allow Yoda ceiling clip past the door.
                ).or_rule(apply_to="hard+", rule=HAS_ANY_YODA),
            ),
        ),
        # Droideka can get out-of-bounds on the far left of the room with the levers before the holding cells, between
        # the left wall and one of the destroyable objects.
        # "After Imperial Phones Room Imperial Panel": (
        R_AFTER_IMPERIAL_PHONES_ROOM_IMPERIAL_PANEL_AND_HOLDING_CELLS: (
            # There is no logical purpose to this region currently, so it is not created.
            # ExitData(
            #     "Pool Double Score Zone",
            #     # There might be an out-of-bounds through Yoda Clip to get under the floor and then into the elevator,
            #     # but it seems difficult because the bottom of the elevator has collision.
            #     HAS_IMPERIAL_OR_CAN_WEAR_HAT_AND_GRAPPLE,
            # ),
            # There are no requirements to get here, and to get from the control room to the holding cells themselves
            # only requires pulling levers, which all jedi can do.
            # ExitData(
            #     "Holding Cell Control Room",
            # ),
            ExitData(
                "Chapter Completion",
                True_(),
                er_rule=HasAbility(CAN_PULL_LEVERS),
            ),
        ),
    },
    minikits={
        # You can also triple jump and swap to mouse droid to get down to where the imperials are.
        "Defeat 10 Imperials With Crane Minikit": minikit_data(
            R_FIRST_CORRIDOR,
            # All Jedi can ride vehicles.
            # HasAbility(CAN_RIDE_VEHICLES),
            pickup_name="m_pup1",
        ),
        "Hangar Observation Room Protocol Panel Minikit": minikit_data(
            R_HANGAR_OBSERVATION_AND_CONTROL_ROOM,
            logic_options(
                strict=False,
                base=HasAbility(PROTOCOL_PANEL)).or_rule(
                # Ceiling clip to get into the mini elevator room containing the minikit (Yoda can ceiling clip back out
                # too).
                apply_to="hard+", rule=CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS
            ),
            pickup_name="mk_0",
        ),
        "Right Corridor Alcove Minikit": minikit_data(
            R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP,
            pickup_name="mk_1",
        ),
        "Right Corridor Access Hatch Minikit": minikit_data(
            R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP,
            logic_options(
                # All grapple characters can destroy the fences to allow hovering across with ease.
                base=Or(
                    CAN_GRAPPLE & HasAllAbilities(HOVER | SHORTIE),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP
                ),
                # The access hatch is actually pointless because you can just hover across after grappling up.
                normal=Or(
                    And(
                        CAN_GRAPPLE,
                        Or(
                            HasAbility(HOVER),
                            # Yoda/Ackbar's extra far double jump can cross the initial gap without needing HOVER.
                            And(
                                HasAbility(SHORTIE),
                                HAS_EXTRA_DISTANCE_DOUBLE_JUMP,
                            ),
                        ),
                    ),
                    CAN_GRAPPLE & HasAbility(HOVER),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP
                ),
                # Allow triple jump to reach the minikit.
                # moderate=Or(
                #     HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                #     CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                #     HasAllAbilities(GRAPPLE | HOVER),
                # )
                # Jedi is required to reach here, so there are no extra requirements on moderate+.
                moderate=True_()
            ),
            pickup_name="mk_2",
        ),
        "Tractor Beam Control Minikit": minikit_data(
            R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP,
            # The bridge parts must be forced out the way first, but a Jedi is required at the start of the chapter.
            # This also means there is no need to check for being able to pull levers, and CAN_GRAPPLE can be optimised.
            logic_options(
                base=HasAbility(GRAPPLE),
                # Allow Force Grapple Leap, and Grievous/Bodyguard High Jumps.
                normal=Or(
                    HasAbility(GRAPPLE),
                    Extra.FORCE_GRAPPLE_LEAP.has(),
                    # Grievous and Bodyguard can high jump up, but other high jumpers (Tarpals + Jar Jar) cannot.
                    Character.has_any(Character.GRIEVOUS_BODYGUARD, Character.GENERAL_GRIEVOUS) & OT_HIGH_JUMP_ENABLED,
                ),
                # Triple jump to the minikit after pulling the levers.
                moderate=True_(),
            ),
            pickup_name="pup1",
        ),
        "Right Corridor High Minikit": minikit_data(
            R_TWIN_CORRIDORS_RIGHT_CORRIDOR_ACROSS_GAP,
            # JEDI is required to reach here, so CAN_SITH_FORCE can be optimized.
            logic_options(
                strict=False,
                base=HasAbility(SITH)).or_rule(
                apply_to="normal+", rule=Extra.DARK_SIDE.has()).or_rule(
                apply_to="moderate+", rule=HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED).or_rule(
                apply_to="hard+", rule=And(
                    Extra.STUD_MAGNET.has(),
                    HAS_ANY_YODA,
                    HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            er_rule=logic_options(
                strict=False,
                base=CAN_SITH_FORCE).or_rule(
                # Triple High Jump can reach the minikit.
                apply_to="moderate+", rule=HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED).or_rule(
                # Using Yoda's glitchy height, you can swap from yoda to another character and have them spawn
                # slightly above ground. With Stud Magnet, this is enough extra starting height for a triple jump to
                # reach the Minikit. Some characters will immediately fall down when swapping to them, so you need
                # the desired Jedi/Slam character to be adjacent to Yoda/Yoda (Ghost) in the Free Play selection, or
                # for all the characters between Yoda/Yoda (Ghost) and the desired character to be characters that
                # do not fall down upon being switched to.
                # todo: Maybe a client command to temporarily lock specific characters could be added, since the
                #  Free Play selection will skip over characters that are not unlocked.
                apply_to="hard+",
                rule=And(
                    Extra.STUD_MAGNET.has(),
                    HAS_ANY_YODA,
                    # Or(
                    #     HasAbility(CAN_HIGH_JUMP_SLAM),
                    #     HasAbilityExceptCharacters(JEDI, Character.YODA, Character.YODA_GHOST),
                    # ),
                    # This more efficiently covers all-Jedi-except-Yodas, and both High Jump Slam characters, though
                    # the latter is irrelevant when OT High Jump is enabled.
                    # There are no Extra Toggle Jedi characters, so it doesn't matter that the
                    # HasAbilityExceptCharacters rule is being used.
                    # Eventually the commented out rules should optimise to this HasAnyAbilities rule
                    HasAnyAbilities(CAN_TRIPLE_JUMP_GREAT_DISTANCE | CAN_HIGH_JUMP_SLAM),
                ),
            ),
            pickup_name="mk_0",
        ),
        "Turntable Bridge Room Minikit": minikit_data(
            R_TURNTABLE_BRIDGE_ROOM,
            logic_options(
                base=CAN_GRAPPLE & HasAbility(HOVER),
                # moderate=Or(
                #     HasAllAbilities(GRAPPLE | HOVER),
                #     HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                # ),
                # Triple jump can reach it and a Jedi is required at the start of the chapter.
                moderate=True_()
            ),
            pickup_name="mk_0",
        ),
        "Destroy Data Center Consoles Minikit": minikit_data(
            R_IMPERIAL_DATA_CENTER_ROOM,
            True_(),
            # Yeah, you can actually punch these consoles.
            er_rule=CAN_DAMAGE_AT_CLOSE_RANGE,
            pickup_name="m_pup1",
        ),
        "Caged Minikit": minikit_data(
            R_AFTER_IMPERIAL_PHONES_ROOM_IMPERIAL_PANEL_AND_HOLDING_CELLS,
            # JEDI is needed at the start of the chapter.
            True_(),
            er_rule=logic_options(
                base=HasAbility(JEDI),
                # No need to stack objects, you can double jump off the sloped terrain by the minikit.
                normal=HasAllAbilities(CAN_DOUBLE_JUMP | CAN_PUSH_OBJECTS),
                # Walk against the cage and swap to Droideka, and Droideka's large collision can grab the minikit before
                # being pushed out of the cage's collision.
                moderate=Or(
                    HasAllAbilities(CAN_DOUBLE_JUMP | CAN_PUSH_OBJECTS),
                    And(
                        Character.DROIDEKA.has(),
                        HasAnyCharacterExcept(Character.DROIDEKA),
                    )
                )
            ),
            pickup_name="mk_1"
        ),
        "Protocol Panel Holding Cell Minikit": minikit_data(
            R_AFTER_IMPERIAL_PHONES_ROOM_IMPERIAL_PANEL_AND_HOLDING_CELLS,
            HasAbility(PROTOCOL_PANEL),
            pickup_name="mk_2",
        ),
    },
    power_brick=LocationData(
        R_TWIN_CORRIDORS_SPAWN,
        logic_options(
            base=And(
                HasAllAbilities(ASTROMECH_PANEL),
                Or(
                    HasAbility(HOVER) & CAN_GRAPPLE,
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
            ),
            moderate=And(
                HasAbility(ASTROMECH_PANEL),
                Or(
                    # Optimised out CAN_GRAPPLE because all Jedi can get to the Power Brick on their own.
                    HasAllAbilities(HOVER | GRAPPLE),
                    ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
        # Allow ceiling clip over the door, or ceiling clip directly to the Power Brick (clip through the ceiling by
        # the pipes just to the right of the door). **Navigating to the Power Brick must be performed blind**
        # because the camera will not shift into the room when skipping using the door.
        ).ror_rule(CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS, "hard+"),
    ),
    ridables={
        # There are more towards the end of the chapter used to control the turbolasers, but they are not logically
        # relevant when this GRABBERCONTROL is here.
        Character.GRABBERCONTROL: LocationData(R_FIRST_CORRIDOR),
    },
)

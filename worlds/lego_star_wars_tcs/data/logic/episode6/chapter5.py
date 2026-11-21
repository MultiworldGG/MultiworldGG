from rule_builder.rules import And, Or, True_, False_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_GRAPPLE,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    CAN_YODA_CLIP,
    HAS_ANY_YODA,
    HAS_0_53_JUMP_HEIGHT_CHARACTER,
)
from ..option_filters import logic_options, ot_high_jump_ternary
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
R_FIGHT_PHASE_1_COMPLETED = "Fight Phase 1 Completed"
R_ELECTRIC_FLOOR_PANELS = "Electric Floor Panels"
R_ELECTRIC_FLOOR_PANELS_FIGHT_PHASE_2 = "Electric Floor Panels (Fight Phase 2)"
R_ELEVATOR_AREA_FIGHT_PHASE_3 = "Elevator Area (Fight Phase 3)"
R_ELEVATOR_AREA_PLATFORM_FIGHT_PHASE_4 = "Elevator Area Platform (Fight Phase 4)"
R_ELEVATOR_AREA_PLATFORM = "Elevator Area Platform"
R_RED_ROOM_DOOR_EXPLOSIVE_PLATFORM = "Red Room Door Explosive Platform"
R_RED_ROOM = "Red Room"
R_RED_ROOM_FAR_LEFT_LEVER_PLATFORM = "Red Room: Far Left Lever Platform"
R_RED_ROOM_ACCESS_HATCH_BRICKS_PLATFORM = "Red Room: Access Hatch Bricks Platform"
R_RED_ROOM_ACCESS_HATCH_PLATFORM = "Red Room: Access Hatch Platform"
R_RED_ROOM_TOP_OF_ELEVATOR_PLATFORM = "Red Room, Top Of Elevator Platform"
R_BEHIND_RED_ROOM_FORCE_FIELD_LEFT_OF_ELEVATOR = "Red Room: Behind Force Field Left Of Elevator"
R_RED_ROOM_ACCESS_HATCH_TUNNEL_END = "Red Room: Access Hatch Tunnel End"
R_RED_ROOM_ACCESS_HATCH_TUNNEL_END_MINIKIT = "Red Room: Access Hatch Tunnel End Minikit"


# Yoda Grab:
# Swapping from some other characters, to Yoda, briefly causes Yoda's collision to appear in front of the character
# before snapping into the correct place. This allows for grabbing minikits, and studs, through some walls. To see this
# in action, keep an eye on the circle that appears above the player's head when they swap characters. For characters
# where Yoda is affected by this glitch, you can see the circle briefly appear in front of the player when swapping to
# Yoda, and then snapping into the correct place.
# Some characters cause a similar glitch with Yoda, but instead of causing the collision to appear in front of Yoda, the
# collision appears at Yoda's last X and Z coordinates, but at the current Y coordinate.
_CAN_YODA_GRAB_ACCESS_HATCH_MINIKIT_THROUGH_WALL = And(
    HAS_ANY_YODA,
    Or(
        HasAbilityExceptCharacters(
            JEDI,
            Character.YODA,
            Character.YODA_GHOST,
            Character.LUKE_SKYWALKER_DAGOBAH,
            Character.LUKE_SKYWALKER_BESPIN,
            Character.LUKE_SKYWALKER_JEDI,
            Character.LUKE_SKYWALKER_ENDOR,
            Character.COUNT_DOOKU,
        ),
        Character.has_any(
            # Be Yoda.
            # Double jump + slam close to the wall beneath the minikit.
            # **Allow the slam animation to play a small amount.**
            # Swap to General Grievous.
            # Swap back to Yoda.
            # Minikit should now be grabbed.
            Character.GENERAL_GRIEVOUS,
            # Theoretically, this might also be possible with Tarpals/Imperial-Guard, though probably not Ackbar.
        ),
    ),
)
# Logically irrelevant because you can Yoda Clip to get to this minikit.
# _CAN_YODA_GRAB_ELEVATOR_LEFT_MINIKIT_THROUGH_FORCE_FIELD = And(
#     HAS_ANY_YODA,
#     Or(
#         HasAbilityExceptCharacters(
#             JEDI,
#             Character.YODA,
#             Character.YODA_GHOST,
#             Character.LUKE_SKYWALKER_DAGOBAH,
#             Character.LUKE_SKYWALKER_BESPIN,
#             Character.LUKE_SKYWALKER_JEDI,
#             Character.LUKE_SKYWALKER_ENDOR,
#         ),
#         Character.has_any(
#             Character.GENERAL_GRIEVOUS,
#             # Seems a bit difficult, but still possible.
#             Character.CAPTAIN_TARPALS,
#             Character.IMPERIAL_GUARD,
#             # Dive roll into the force field, and near the very start of the dive roll, swap to Yoda.
#             Character.ADMIRAL_ACKBAR,
#         ),
#     ),
# )
_CAN_YODA_GRAB_FAR_LEFT_MINIKIT = And(
    HAS_ANY_YODA,
    Or(
        # Grab through both the grate and force field.
        HasAbilityExceptCharacters(
            JEDI,
            Character.YODA,
            Character.YODA_GHOST,
            # Luke cannot Yoda Grab.
            Character.LUKE_SKYWALKER_DAGOBAH,
            Character.LUKE_SKYWALKER_BESPIN,
            Character.LUKE_SKYWALKER_JEDI,
            Character.LUKE_SKYWALKER_ENDOR,
            # Custom characters also cannot Yoda Grab, but they don't have the JEDI ability on their own, so don't need
            # to be considered for logic here.
        ),
        # Grievous has a similar Yoda Grab distance as most Jedi, so can grab the minikit through both the grate and
        # force field.
        Character.GENERAL_GRIEVOUS.has(),
        And(
            # Remove the grate with Sith Force.
            HasAbility(SITH) | Extra.DARK_SIDE.has(),
            # Tarpals, Imperial Guard and Ackbar can cause a Yoda Grab, but with limited grab distance.
            Character.has_any(
                Character.CAPTAIN_TARPALS,
                Character.IMPERIAL_GUARD,
                # Dive roll into the force field, and near the very start of the dive roll, swap to Yoda.
                Character.ADMIRAL_ACKBAR,
            )
        ),
    )
)


_helper = ChapterHelper(
    area=Area.EMPERORFIGHT,
    start_region=R_SPAWN,
)

_SPAWN_TO_ELECTRIC_FLOOR = logic_options(
    base=CAN_SITH_FORCE,
    # Allow triple jumps. Either follow the same route for High Jump, or triple jump from the circular bits of terrain
    # beneath the catwalk.
    # Allow high jump from the objects blocking the Bounty Hunter panel, to the Sith Force grate beneath the right side
    # of the electric floor, and then high jump up.
    # The bricks for the fan can also be spawned by making the camera pan around to where the right minikit from spawn
    # is, and then going back to the area with the fan, though this is logically irrelevant due to triple jumps.
    moderate=Or(
        ot_high_jump_ternary(
            uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
            capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
        ),
    ),
)

JEDI_DESTINY = _helper.make_chapter(
    intended_completion_path={
        "base": (
            R_FIGHT_PHASE_1_COMPLETED,
            R_ELECTRIC_FLOOR_PANELS_FIGHT_PHASE_2,
            R_ELEVATOR_AREA_FIGHT_PHASE_3,
            R_ELEVATOR_AREA_PLATFORM_FIGHT_PHASE_4,
        ),
    },
    regions={
        R_SPAWN: (
            ExitData(
                R_FIGHT_PHASE_1_COMPLETED,
                logic_options(
                    # Expect melee attacks.
                    base=HasAbility(CAN_MELEE),
                    # Allow explosions.
                    normal=HasAbility(CAN_MELEE) | CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    # Allow blasters.
                    # Hitting him is awkward, but I find it easiest to walk in and out of his aggro range.
                    # Technically Ewoks can also defeat him, but that sucks even with Invincibility.
                    moderate=HasAnyAbilities(CAN_MELEE | BLASTER) | CAN_DESTROY_CLOSE_SILVER_BRICKS,
                )
            ),
            ExitData(
                R_ELECTRIC_FLOOR_PANELS,
                logic_options(
                    # Expect finishing the first phase to spawn the bricks for the fan.
                    base=False_(),
                    # Now allow skipping the first phase.
                    moderate=_SPAWN_TO_ELECTRIC_FLOOR,
                )
            ),
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=False_(),
                    # "Ultra Kill" The Emperor, similar to how the speedrun does it.
                    # Logic expects safety slashes.
                    # The Emperor does not block against regular melee attacks very well, so a combo-type melee attack
                    # is required.
                    # None of the 1P2C that would be used in the speedrun is necessary. Stand in the corner of the upper
                    # platform to bait The Emperor out, then jump down the stairs and face The Emperor as he tries to
                    # walk back up the stairs, then perform use 'safety slashes' to push him all the way to the pit.
                    # This could maybe be moved to Hard logic if it is deemed too technically difficult, since baiting
                    # The Emperor down the stairs (making the trick easier) is a knowledge check.
                    # I personally find Yoda more difficult than other characters due to how much Yoda moves when
                    # attacking.
                    # Grievous' Bodyguard is also a little more difficult because it barely pushes The Emperor with its
                    # 'safety slashes', so many additional 'safety slashes' are required.
                    # Imperial Guard does not seem to be able to push The Emperor at all, despite having a combo-type
                    # melee attack.
                    moderate=HasAnyAbilities(IS_NON_GHOST_JEDI | CAN_HIGH_JUMP_SLAM),
                ),
                name = "\"Ultra Kill\" The Emperor",
            ),
            ExitData(
                R_RED_ROOM_DOOR_EXPLOSIVE_PLATFORM,
                logic_options(
                    # High jump to the platform, or reveal and use the Access Hatch.
                    base=Or(
                        CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                        HasAbility(SHORTIE) & CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                    ),
                    # Allow triple jump.
                    # Ignore the requirement to destroy the object in front of the Access Hatch because you can actually
                    # use the Access Hatch without destroying the object in the way. You still need to destroy the
                    # bombs, but basic melee attacks work on the bombs.
                    moderate=Or(
                        ot_high_jump_ternary(
                            uncapped=HasAnyAbilities(JEDI | HIGH_JUMP | SHORTIE),
                            capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM | SHORTIE),
                        ),
                        HasAbility(SHORTIE) & CAN_DAMAGE_AT_CLOSE_RANGE,
                    ),
                ),
            ),
            ExitData(
                R_ELEVATOR_AREA_PLATFORM,
                logic_options(
                    # Expect finishing the first three phases and using the elevator.
                    base=False_(),
                    # Triple jump from the highest fence part of the elevator platform. Near-maximum height is required
                    # for non-Yodas. Triple high jump is easy.
                    # Alternatively, if you repeatedly double jump + slam from the highest fence part, the elevator
                    # bricks spawn for some reason, allowing you to build them, and use the elevator normally (requiring
                    # Sith Force). This alternative is logically irrelevant on Moderate+ logic.
                    moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                )
            )
        ),
        R_FIGHT_PHASE_1_COMPLETED: (
            ExitData(
                R_ELECTRIC_FLOOR_PANELS_FIGHT_PHASE_2,
                _SPAWN_TO_ELECTRIC_FLOOR,
            ),
        ),
        R_ELECTRIC_FLOOR_PANELS: (),
        R_ELECTRIC_FLOOR_PANELS_FIGHT_PHASE_2: (
            ExitData(R_ELECTRIC_FLOOR_PANELS),
            ExitData(
                R_ELEVATOR_AREA_FIGHT_PHASE_3,
                # Even C-3PO can walk fast enough to get through the electric floor paths, and Gonk Droid cannot
                # get up to the Phase 2 part of the fight alone, so the player must have some other suitable
                # character.
                True_(),
            )
        ),
        R_ELEVATOR_AREA_FIGHT_PHASE_3: (
            ExitData(
                R_ELEVATOR_AREA_PLATFORM_FIGHT_PHASE_4,
                # Blaster-only is much more annoying for phase 3, but only for the first hit of damage, so it is always
                # possible to complete Phase 3 if Phase 1 and 2 can be completed.
                logic_options(
                    # Base logic is expected to take the elevator.
                    base=CAN_SITH_FORCE,
                    # Allow other means of damaging The Emperor and traversing to the upper area.
                    normal=CAN_SITH_FORCE | _helper.can_reach_region(R_ELEVATOR_AREA_PLATFORM),
                ),
            ),
        ),
        R_ELEVATOR_AREA_PLATFORM_FIGHT_PHASE_4: (
            ExitData(R_ELEVATOR_AREA_PLATFORM),
            # Phase 5 is just a drop-down and continue fighting. And phase 6 is just chase after The Emperor.
            # Going to Phase 5 with just BLASTER is a pain, but at least only for the first hit. Make use of the Power
            # Up in one of the destroyable objects on the left side.
            # All characters that can reach this platform can jump across the two sides without issue.
            ExitData("Chapter Completion"),
        ),
        R_ELEVATOR_AREA_PLATFORM: (
            ExitData(
                R_RED_ROOM,
                logic_options(
                    base=False_(),
                    # There is no ceiling here, and the floor goes as far back as the minikit behind the force field.
                    # Triple jump from one of the destroyable objects to get over the wall, then drop down behind the
                    # minikit and walk towards the R_RED_ROOM area.
                    hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
                new_level=Level.EMPERORFIGHT_B,
            ),
        ),
        R_RED_ROOM_DOOR_EXPLOSIVE_PLATFORM: (
            ExitData(
                R_RED_ROOM,
                HasAbility(CAN_PUSH_OBJECTS) & CAN_DAMAGE_AT_CLOSE_RANGE,
                new_level=Level.EMPERORFIGHT_B,
            ),
            ExitData(
                R_ELEVATOR_AREA_PLATFORM,
                logic_options(
                    base=False_(),
                    # Double jump, or triple jump (much easier for Grievous).
                    # Bodyguard can only make it by pushing the block down, and then triple-high-jumping from the bombs.
                    moderate=ot_high_jump_ternary(
                        uncapped=Or(
                            HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GRIEVOUS_BODYGUARD),
                            # Allow pushing the block down, avoiding destroying the bombs, and then triple-high-jump
                            # with Bodyguard.
                            HasAllAbilities(CAN_HIGH_JUMP_SLAM | CAN_PUSH_OBJECTS),
                        ),
                        capped=HasAbilityExceptCharacters(CAN_DOUBLE_JUMP, Character.GRIEVOUS_BODYGUARD),
                    ),
                ),
            ),
        ),
        R_RED_ROOM: (
            ExitData(
                R_RED_ROOM_FAR_LEFT_LEVER_PLATFORM,
                logic_options(
                    strict=False,
                    base=CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_GRAPPLE,
                ).ror_rule(
                    apply_to="normal",
                    rule=CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ).ror_rule(
                    apply_to="moderate+",
                    rule=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                    ),
                ),
            ),
            ExitData(
                R_RED_ROOM_TOP_OF_ELEVATOR_PLATFORM,
                logic_options(
                    strict=False,
                    # Destroy the chair in the center of the room (basic melee attacks do not work) to reveal bricks for
                    # a spinner, and then build it.
                    # Go up to the platform on the far left of the room (as seen by the camera) pull the Lever to
                    # spawn the bricks for a pushable object, and then build that object.
                    # Push the pushable object onto the turntable and turn the spinner to spin the pushable object.
                    # Push the, now rotated, pushable object all the way to the elevator to activate it.
                    base=And(
                        HasAllAbilities(CAN_PUSH_OBJECTS | CAN_BUILD_BRICKS | CAN_PUSH_OBJECTS),
                        _helper.can_reach_region(R_RED_ROOM_FAR_LEFT_LEVER_PLATFORM),
                        CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                    ),
                ).ror_rule(
                    # Allow double jump onto the inside of the alcove with the force field, then triple jump to the
                    # platform at the top of the elevator.
                    apply_to="moderate+",
                    rule=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM)
                ),
            ),
            ExitData(
                R_BEHIND_RED_ROOM_FORCE_FIELD_LEFT_OF_ELEVATOR,
                # Stand up against the force field, then Yoda Ceiling Clip over it.
                # It is possible with big characters, like Droideka, but can be more difficult.
                # Performing a Yoda Grab can also get this minikit from outside the force field. Tarpals, Imperial Guard
                # and Ackbar can also get the minikit with their reduced Yoda Grab distance.
                logic_options(
                    base=False_(),
                    hard=CAN_YODA_CLIP,
                ),
            ),
            ExitData(
                R_RED_ROOM_ACCESS_HATCH_TUNNEL_END_MINIKIT,
                logic_options(
                    base=False_(),
                    hard=_CAN_YODA_GRAB_ACCESS_HATCH_MINIKIT_THROUGH_WALL,
                ),
            ),
            ExitData(
                R_RED_ROOM_ACCESS_HATCH_PLATFORM,
                logic_options(
                    base=HasAbility(JEDI),
                    normal=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAbility(JEDI),
                    ),
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
            ),
        ),
        R_RED_ROOM_FAR_LEFT_LEVER_PLATFORM: (
            ExitData(
                R_RED_ROOM_ACCESS_HATCH_BRICKS_PLATFORM,
                logic_options(
                    base=False_(),
                    # The collision of this platform actually sticks out a lot more than the visuals would suggest,
                    # making this jump pretty easy, even when using Bodyguard without OT High Jump enabled.
                    normal=HasAbility(CAN_DOUBLE_JUMP),
                ),
            ),
            ExitData(
                R_RED_ROOM_ACCESS_HATCH_PLATFORM,
                logic_options(
                    base=False_(),
                    normal=HasAbility(HOVER),
                ),
            ),
        ),
        R_RED_ROOM_ACCESS_HATCH_BRICKS_PLATFORM: (
            # Just drop down.
            ExitData(R_RED_ROOM_ACCESS_HATCH_PLATFORM),
            ExitData(
                R_RED_ROOM_FAR_LEFT_LEVER_PLATFORM,
                logic_options(
                    base=False_(),
                    normal=HasAbility(CAN_DOUBLE_JUMP),
                ),
            ),
        ),
        R_RED_ROOM_ACCESS_HATCH_PLATFORM: (
            ExitData(
                R_RED_ROOM_ACCESS_HATCH_BRICKS_PLATFORM,
                logic_options(
                    strict=False,
                    base=HasAbility(CAN_DOUBLE_JUMP),
                ).or_rule(
                    apply_to="moderate+",
                    # The jump is not easy, but is possible.
                    rule=HAS_0_53_JUMP_HEIGHT_CHARACTER,
                )
            ),
            ExitData(
                R_RED_ROOM_ACCESS_HATCH_TUNNEL_END,
                logic_options(
                    base=HasAbility(SHORTIE) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    # Allow Yoda Clip.
                    hard=And(
                        HasAbility(SHORTIE),
                        CAN_DESTROY_CLOSE_SILVER_BRICKS | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    )
                ),
            ),
        ),
        R_RED_ROOM_TOP_OF_ELEVATOR_PLATFORM: (
            ExitData(
                R_BEHIND_RED_ROOM_FORCE_FIELD_LEFT_OF_ELEVATOR,
                # Destroy the objects by the entrance door and build and use the Protocol panel to lower the platform in
                # front of the left lever, then pull the lever to remove the force field.
                # Then jump up to the minikit from ground level.
                logic_options(
                    base=And(
                        HasAllAbilities(PROTOCOL_PANEL | CAN_PULL_LEVERS | CAN_DOUBLE_JUMP),
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    ),
                    # So long as you don't destroy the chair close to the force field, Gamorrean Guard and Super Gonk
                    # Droid can also jump up to the minikit.
                    normal=And(
                        HasAllAbilities(PROTOCOL_PANEL | CAN_PULL_LEVERS),
                        HasAbility(CAN_DOUBLE_JUMP) | HAS_0_53_JUMP_HEIGHT_CHARACTER,
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    ),
                    # Standing on top of the far right lever in the Red Room, you can get enough height to Yoda Ceiling
                    # Clip through the ceiling, then work around the outside of elevator out-of-bounds, and walk/jump
                    # the way to the minikit. This is a bit too much out-of-bounds movement for Hard logic in my
                    # opinion, but is pretty easy Expert logic.
                ),
            ),
        ),
        R_BEHIND_RED_ROOM_FORCE_FIELD_LEFT_OF_ELEVATOR: (),
        R_RED_ROOM_ACCESS_HATCH_TUNNEL_END: (
            ExitData(R_RED_ROOM_ACCESS_HATCH_TUNNEL_END_MINIKIT),
        ),
        R_RED_ROOM_ACCESS_HATCH_TUNNEL_END_MINIKIT: (),
    },
    minikits={
        "Spawn Left Alcove Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAbility(JEDI),
                ),
                # Allow Ackbar + Grievous + Bodyguard
                normal=ot_high_jump_ternary(
                    uncapped=HasAnyAbilities(JEDI | HIGH_JUMP),
                    capped=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ) | Character.ADMIRAL_ACKBAR.has(),
                # Allow triple jumps (logic ends up identical to Normal)
            ),
            pickup_name="mk_0",
        ),
        "Grapple Platform Right Of Spawn Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & CAN_GRAPPLE,
                # Allow triple jump. High jumps are not enough.
                moderate=Or(
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(GRAPPLE),
                ),
            ),
            pickup_name="pup1",
        ),
        "Silver Brick Panels And Red Buttons Minikit": minikit_data(
            R_SPAWN,
            # Protocol Droids are the second slowest (shared with a few other characters), and can activate the buttons
            # fine.
            # Gonk Droid is too slow even with 1P2C.
            # Watto and Geonosian do not activate the buttons while fluttering, and walk too slowly to activate them on
            # their own.
            # While two of the panels are fake Silver Bricks (can be destroyed by other attacks), even if you managed to
            # activate all the floor buttons with fast characters/1P2C, the minikit will not spawn unless all four
            # panels have been destroyed.
            # Typically, a small jump is required to reach the minikit.
            logic_options(
                # Destroy the Silver Brick panels on the walls.
                strict=False,
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ).and_rule(
                # Activate the buttons on the floor.
                logic_options(
                    base=HasAnyCharacterExcept(
                        Character.GONK_DROID,
                        Character.WATTO,
                        Character.GEONOSIAN,
                    ),
                    # Allow Watto and Geonosian to activate the buttons by using 1P2C and walking around the buttons in
                    # opposite directions with each player.
                    hard=HasAnyCharacterExcept(Character.GONK_DROID),
                ),
            ).and_rule(
                # Reach the minikit that spawns over the gap in the middle of the buttons.
                logic_options(
                    base=HasAbility(CAN_BARELY_JUMP),
                    # Allow some bigger characters that are unable to jump.
                    moderate=Or(
                        HasAbility(CAN_BARELY_JUMP),
                        Character.DROIDEKA.has(),
                        # C-3PO and TC-14 cannot get the minikit even with Stud Magnet enabled.
                        # I assumed PK Droid and Pit Droid are too small, but did not check.
                        Extra.STUD_MAGNET.has() & Character.has_any(
                            Character.BATTLE_DROID,
                            Character.BATTLE_DROID_GEONOSIS,
                            Character.BATTLE_DROID_SECURITY,
                            Character.BATTLE_DROID_COMMANDER,
                            Character.SUPER_BATTLE_DROID,
                        ),
                    ),
                ),
            ),
            pickup_name="MINI_3",
        ),
        "Below Electric Floor Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=HasAllAbilities(SITH | CAN_BUILD_BRICKS | BOUNTY_HUNTER | HOVER),
                # Just jump off some of the destroyable objects.
                normal=HasAbility(CAN_DOUBLE_JUMP),
            ),
            pickup_name="mk_1",
        ),
        "Protocol Panel Walkway Room Minikit": minikit_data(
            R_SPAWN,
            # Even if you clip into the room early, the minikit bricks don't spawn until the Protocol Panel is used.
            HasAllAbilities(BOUNTY_HUNTER | PROTOCOL_PANEL | CAN_BUILD_BRICKS),
            pickup_name="MINI_PI",
        ),
        "Silver Bricks Central Column Minikit": minikit_data(
            R_SPAWN,
            # Even if you clip inside the room with the minikit, the minikit does not spawn until the silver bricks are
            # destroyed.
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            pickup_name="m_pup1",
        ),
        "Four Lights Force Field Minikit": minikit_data(
            R_ELEVATOR_AREA_PLATFORM,
            # A:
            # Sith Force the lights on the back wall of the Electric Floor Panels.
            # This Spawns bricks for a Bounty Hunter Panel on the attached catwalk. Build and use the panel to spawn the
            # first light.
            # B:
            # Destroy the silver bricks on the central column that face the Red Buttons room.
            # Use the Imperial Panel inside to spawn the bricks for the second light.
            # C:
            # Destroy the objects on the Elevator Area Platform to reveal the final two lights.
            # These two lights require Sith Force and destroying Silver Bricks respectively, once built.
            logic_options(
                strict=False,
                base=And(
                    HasAllAbilities(BOUNTY_HUNTER | CAN_BUILD_BRICKS | IMPERIAL),
                    CAN_SITH_FORCE,
                    _helper.can_reach_region(R_ELECTRIC_FLOOR_PANELS),
                ),
                # Same as the trick to get into the Red Room, but you intentionally go to where the minikit is, instead
                # of behind it.
                # Because the intended route requires Sith Force, this makes the intended route logically irrelevant.
                # Hard logic can skip the silver bricks requirement in part B of the intended route by Yoda Ceiling
                # Clipping into the small room with the Imperial panel, but this is logically irrelevant when Yodas can
                # get to the minikit on their own.
                hard=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="M_RED",
        ),
        "Red Room Left Force Field Minikit": minikit_data(
            R_BEHIND_RED_ROOM_FORCE_FIELD_LEFT_OF_ELEVATOR,
            pickup_name="mk_0",
        ),
        "Red Room Access Hatch Minikit": minikit_data(
            # Force chairs into a stack and jump up to the access hatch bricks and build most of the access hatch.
            # Destroy the silver brick objects by the door to reveal a Grapple point. Grapple up and then destroy the
            # silver brick wall panels to reveal the door of the Access Hatch.
            # Sith Force the door of the Access Hatch into place.
            # Use the Access Hatch and then Destroy the Silver Brick fan in the way. Alternatively Yoda Ceiling Clip
            # over the fan (irrelevant since you need to destroy Silver Bricks to spawn the hatch door.
            R_RED_ROOM_ACCESS_HATCH_TUNNEL_END_MINIKIT,
            pickup_name="m_pup1",
        ),
        "Red Room Grate Force Field Minikit": minikit_data(
            R_RED_ROOM,
            # Destroy the silver bricks next to the grate to reveal Astromech Panel bricks.
            # Build and use the Astromech Panel to remove the force field.
            # Sith Force to remove the grate.
            logic_options(
                strict=False,
                base=CAN_SITH_FORCE & CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(ASTROMECH_PANEL),
            ).or_rule(
                apply_to="hard+",
                rule=_CAN_YODA_GRAB_FAR_LEFT_MINIKIT,
            ),
            pickup_name="mk_1",
        )
    },
    power_brick=LocationData(R_SPAWN, CAN_SITH_FORCE),
)

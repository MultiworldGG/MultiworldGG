from rule_builder.rules import And, True_, Or
from ..macros import CAN_YODA_CLIP

from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities, HasAnyCharacterExcept
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...levels import Level

from ....character_ability import *

R_MEETING_ROOM = "Meeting Room"
R_MAIN_CORRIDOR = "Main Corridor"
R_SINGLE_FORCE_FIELD_ROOM = "Single Force Field Room"
R_HIGH_FORCE_FIELDS_ROOM = "High Force Fields Room"
R_VULTURE_DROID_ROOM = "Vulture Droid Room"
R_SMALL_ROOM_BETWEEN_MAIN_CORRIDOR_AND_ROOM_BEFORE_HANGAR = "Small Room Between Main Corridor and Room Before Hangar"
R_ROOM_BEFORE_HANGAR = "Room Before Hangar"
R_MAIN_HANGAR = "Main Hangar"
R_POWER_BRICK_ROOM = "Power Brick Room"
R_MTT_HANGAR = "MTT Hangar"

NEGOTIATIONS = Chapter(
    area=Area.NEGOTIATIONS,
    start_region=R_MEETING_ROOM,
    regions={
        R_MEETING_ROOM: (
            ExitData(R_MAIN_CORRIDOR, HasAbility(JEDI)),
        ),
        R_MAIN_CORRIDOR: (
            # Droideka can clip out-of-bounds, into the right wall, on the destroyable object that spawns the power up.
            ExitData(
                R_SINGLE_FORCE_FIELD_ROOM,
                logic_options(
                    base=HasAbility(PROTOCOL_PANEL),
                    # Yoda Clip is possible here, but the way the collision is laid out makes it more complicated than
                    # just standing in front of the door and clipping over the ceiling directly above the door.
                    # The collision above the door has two layers, making a Yoda clip not possible because you can only
                    # clip through one layer, though maybe Yoda Clipping with a very short character could fit between
                    # the two ceilings.
                    # To Yoda Clip here, you need to stand further back from the door so that the arch's ceiling is not
                    # above you, then, you need to Yoda Clip with good height, to get over the collision wall of the top
                    # of the arch.
                    # If you get in here with only a single character through a Yoda Clip, and you drop in P2 to
                    # activate the buttons. This can make leaving the room more difficult if you don't have a
                    # triple-high-jump character (there's no ceiling within the room), but you can stand on the box
                    # below all the Blue Studs for extra triple jump height (remember that triple jumps with Yoda get
                    # extra height, so start the triple jump as Yoda, then switch).
                    hard=HasAbility(PROTOCOL_PANEL) | CAN_YODA_CLIP,
                ),
            ),
            ExitData(
                R_HIGH_FORCE_FIELDS_ROOM,
                logic_options(
                    base=HasAbility(PROTOCOL_PANEL),
                    # Same door collision as the single force field room.
                    hard=HasAbility(PROTOCOL_PANEL) | CAN_YODA_CLIP,
                )
            ),
            ExitData(
                R_VULTURE_DROID_ROOM,
                # I am aware of a Yoda Clip for this door, but you tend to get stuck behind the door, or hit the
                # backwards transition instead of the forwards transition, so I don't know how the Yoda Clip for this
                # door is supposed to work.
                HasAbility(ASTROMECH_PANEL),
                new_level=Level.NEGOTIATIONS_B,
            ),
            ExitData(
                R_SMALL_ROOM_BETWEEN_MAIN_CORRIDOR_AND_ROOM_BEFORE_HANGAR,
                logic_options(
                    base=HasAbility(PROTOCOL_PANEL),
                    # Same door collision as the single force field room.
                    hard=HasAbility(PROTOCOL_PANEL) | CAN_YODA_CLIP,
                )
            ),
        ),
        R_SINGLE_FORCE_FIELD_ROOM: (),
        R_HIGH_FORCE_FIELDS_ROOM: (),
        R_VULTURE_DROID_ROOM: (),
        R_SMALL_ROOM_BETWEEN_MAIN_CORRIDOR_AND_ROOM_BEFORE_HANGAR: (
            ExitData(
                R_ROOM_BEFORE_HANGAR,
                # If you can get to this room, you can use this entrance.
                True_(),
                er_rule=logic_options(
                    base=HasAllAbilities(JEDI | CAN_BUILD_BRICKS | PROTOCOL_PANEL),
                    hard=HasAllAbilities(JEDI | CAN_BUILD_BRICKS | PROTOCOL_PANEL) | CAN_YODA_CLIP,
                ),
            ),
        ),
        R_ROOM_BEFORE_HANGAR: (
            ExitData(
                R_MAIN_HANGAR,
                True_(),
                er_rule=HasAbility(JEDI),
                new_level=Level.NEGOTIATIONS_C,
            ),
        ),
        R_MAIN_HANGAR: (
            ExitData(
                R_POWER_BRICK_ROOM,
                logic_options(
                    base=HasAbility(ASTROMECH_PANEL),
                    # There is no ceiling here, and you can just barely triple-high-jump to get over the collision wall.
                    # Note that triple-high-jump and then swap to Jar Jar/Tarpals/Bodyguard is impossible due to their
                    # higher gravity, it is just barely possible to swap to them and then immediately swap back, but,
                    # for logic simplicity, those characters will be excluded.
                    # Once over the wall, be careful not to hit the backwards transition. You can either walk backwards
                    # to hit the forwards transition, or triple jump over the backwards transition and into the Power
                    # Brick room directly.
                    # If you're swapping
                    hard=Or(
                        HasAbility(ASTROMECH_PANEL),
                        # todo: Could you Wall Climb here? That would allow Jar Jar + Tarpals.
                        And(
                            Character.GENERAL_GRIEVOUS.has(),
                            HasAnyCharacterExcept(
                                # Obviously need to exclude Grievous himself.
                                Character.GENERAL_GRIEVOUS,
                                # High gravity (-7.00).
                                Character.JAR_JAR_BINKS,
                                Character.CAPTAIN_TARPALS,
                                # Swapping from Grievous -> Bodyguard is impossible.
                                # Swapping from Grievous -> Bodyguard -> Grievous is *barely* possible and probably too
                                # difficult for Hard logic.
                                # But if you have Bodyguard, it is much easier to swap from Bodyguard -> Grievous to get
                                # enough height, so there is no need to exclude Bodyguard here.
                                # Character.GRIEVOUS_BODYGUARD,
                                # Don't need to exclude Yoda's because you can swap back to Grievous and still get
                                # enough height because Grievous' gravity is the standard -6.00.
                            ),
                        ),
                        And(
                            Character.GRIEVOUS_BODYGUARD.has(),
                            HasAnyCharacterExcept(
                                # Obviously need to exclude Bodyguard itself.
                                Character.GRIEVOUS_BODYGUARD,
                                # High gravity (-7.00).
                                Character.JAR_JAR_BINKS,
                                Character.CAPTAIN_TARPALS,
                                # Don't need to exclude Grievous because Grievous has -6.00 gravity, so starting the
                                # triple-high-jump as Bodyguard and then swapping to Grievous after slamming is enough
                                # to get the required height.
                                # Character.GENERAL_GRIEVOUS
                                # Yoda's have to be excluded too because if you intend to triple-high-jump with a swap
                                # to a Yoda, you need to swap back to the original character, Bodyguard in this case,
                                # because Yodas have a height offset in their collision, but Bodyguard's gravity is too
                                # high to make the jump if you swap back to it.
                                Character.YODA,
                                Character.YODA_GHOST,
                            ),
                        ),
                    ),
                    # With a Yoda Clip, it is super easy to get out-of-bounds from where the far left Battle Droid
                    # stands, and then you can walk under the level to get into the Power Brick room.
                ),
                er_rule=And(
                    HasAbility(ASTROMECH_PANEL),
                    logic_options(
                        base=HasAbility(JEDI),
                        # ER Note: With ER, entering the Main Hangar from the MTT Hangar would require Moderate logic
                        #  to use Jetpack to get to the Power Brick Room entrance.
                        normal=HasAnyAbilities(CAN_DOUBLE_JUMP | JETPACK),
                    )
                ),
            ),
            ExitData(
                R_MTT_HANGAR,
                er_rule=logic_options(
                    # Defeat the Droideka and force the platforms to jump over the fence.
                    base=HasAbility(JEDI),
                    # Alternatively high jump over the fence, potentially ignoring the Droideka.
                    normal=HasAnyAbilities(JEDI | HIGH_JUMP),
                    # Alternatively jump + jetpack hover from on top of the magnet to get over the fence.
                    moderate=HasAnyAbilities(JEDI | HIGH_JUMP | JETPACK),
                )
            ),
        ),
        R_POWER_BRICK_ROOM: (),
        R_MTT_HANGAR: (
            ExitData(
                "Chapter Completion",
                er_rule=HasAbility(PROTOCOL_PANEL),
            ),
        ),
    },
    minikits={
        "Blue Levers Minikit": minikit_data(
            R_MAIN_CORRIDOR,
            er_rule=HasAbility(JEDI),
            pickup_name="m_pup4",
        ),
        "Purple Levers Minikit": minikit_data(
            R_MAIN_CORRIDOR,
            er_rule=HasAbility(JEDI),
            pickup_name="m_pup1",
        ),
        "Force Field With Battle Droids Minikit": minikit_data(
            R_SINGLE_FORCE_FIELD_ROOM,
            # Yoda Grab does not appear to get enough distance, so you'll need to drop in P2 if you Yoda Clipped into
            # the room.
            pickup_name="m_pup3",
        ),
        "Minikit Behind Left High Force Field": minikit_data(
            R_HIGH_FORCE_FIELDS_ROOM,
            logic_options(
                base=HasAbility(PROTOCOL_PANEL),
                # Allow Yoda Clip to activate the button.
                # You can also Yoda Grab the minikit through the force field.
                hard=HasAbility(PROTOCOL_PANEL) | CAN_YODA_CLIP,
            ),
            pickup_name="m_pup5",
        ),
        "Minikit Behind Right High Force Field": minikit_data(
            R_HIGH_FORCE_FIELDS_ROOM,
            logic_options(
                base=HasAbility(PROTOCOL_PANEL),
                # Allow Yoda Clip to activate the button.
                # You can also Yoda Grab the minikit through the force field.
                hard=HasAbility(PROTOCOL_PANEL) | CAN_YODA_CLIP,
            ),
            er_rule=logic_options(
                # Disable the force field with SHORTIE, stack 3 boxes, double jump on top, then double jump to the
                # Minikit.
                base=HasAllAbilities(SHORTIE | JEDI),
                # Alternatively, high jump up to the minikit, either holding the control stick in the
                # direction of the elevated area to prevent sliding off, or by standing on
                normal=HasAbility(SHORTIE) & HasAnyAbilities(JEDI | HIGH_JUMP),
                # Moderate (simpler): Triple jump up to the minikit.
                hard=Or(
                    HasAbility(SHORTIE) & HasAnyAbilities(JEDI | HIGH_JUMP),
                    CAN_YODA_CLIP,
                ),
            ),
            pickup_name="pup2",
        ),
        "High Minikit In Vulture Droid Room": minikit_data(
            R_VULTURE_DROID_ROOM,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                moderate=True_(),
            ),
            er_rule=logic_options(
                # Stand on the moving platform. P2 will force the platform into position, then high jump to the
                # minikit.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                # Stand on the air tanks by the table, then high jump up to the minikit.
                normal=HasAbility(HIGH_JUMP),
                # A triple jump can be used instead of a high jump.
                moderate=HasAnyAbilities(JEDI | HIGH_JUMP),
            ),
            # Simplified without ER.
            pickup_name="m_pup1",
        ),
        "Minikit Above Repaired Vulture Droid": minikit_data(
            R_VULTURE_DROID_ROOM,
            logic_options(
                base=HasAllAbilities(HIGH_JUMP | HOVER),
                normal=HasAllAbilities(HOVER),
                moderate=True_(),
            ),
            er_rule=logic_options(
                # Force the grate out of the way, high jump into the vent, hover across the gap, then high jump up
                # to the minikit.
                base=HasAllAbilities(JEDI | HIGH_JUMP | HOVER),
                # Force the grate most of the way down, then jump onto the grate as it starts to return upwards and use
                # that extra height to jump into the vent. Hover across the gap, then double jump to the minikit by
                # standing on one of the wings of the vulture droid. Slam for extra height if you are having trouble.
                # While not relevant until ER, and not logically relevant either way, a double jump is just enough to
                # get back into the vent if this minikit has been reached without a character that can use Astromech
                # panels.
                normal=HasAllAbilities(JEDI | HOVER),
                # Force the grate out of the way and triple jump up to the vent. Triple jump across the gap (may take a
                # few tries, you'll need good timing), and then triple jump up to the minikit.
                moderate=HasAbility(JEDI),
            ),
            pickup_name="pup2",
        ),
        "High Minikit In Room Before Hangar": minikit_data(
            R_ROOM_BEFORE_HANGAR,
            logic_options(
                base=HasAbility(HIGH_JUMP),
                normal=True_(),
            ),
            er_rule=logic_options(
                # Force the grate, and then high jump from the grate's bricks.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                # TODO: Can a regular double jump + Stud Magnet also reach it?
                # A double jump + slam can reach the minikit.
                normal=HasAbility(JEDI),
                # A high triple jump can also reach the minikit, but both ways to get to the minikit require a Jedi, so
                # this is not relevant even with ER.
            ),
            pickup_name="m_pup2",
        ),
        "Minikit Left of Hangar Entrance": minikit_data(
            R_MAIN_HANGAR,
            er_rule=logic_options(
                # If the jump from the entrance with to where the minikit is, is missed, the force can be used on boxes
                # to build a tower back up to the entrance.
                base=HasAbility(JEDI),
                # Don't mess up the jump to where the minikit is, though a high jump can also get back to the entrance
                # with some platforming.
                normal=HasAbility(CAN_DOUBLE_JUMP),
            ),
            pickup_name="m_pup1",
        ),
        "Moving Platform Minikit": minikit_data(
            R_MAIN_HANGAR,
            er_rule=logic_options(
                # Stack the boxes and force the lever to activate the platform.
                base=HasAbility(JEDI),
                # Triple jump up to the platform then triple jump to the minikit.
                moderate=HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="m_pup2",
        ),
    },
    power_brick=LocationData(
        R_POWER_BRICK_ROOM,
        er_rule=logic_options(
            base=HasAbility(JEDI),
            normal=HasAnyAbilities(JEDI | HIGH_JUMP),
        )
    ),
    ridables={
        Character.STAP2: LocationData(
            R_MAIN_HANGAR,
            er_rule=HasAbility(CAN_BUILD_BRICKS),
        )
    },
)

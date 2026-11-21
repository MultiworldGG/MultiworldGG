from rule_builder.rules import And, Or

from ..macros import (
    CAN_GRAPPLE,
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_USE_DEFLECT_BOLTS,
    CAN_DAMAGE_SHIELDED_DROIDEKA,
    CAN_ACTIVATE_CLOSE_TARGET,
    HAS_FLUTTER_CHARACTER,
    HAS_WALL_CLIMB,
    HAS_ANY_YODA,
)
from ..option_filters import logic_options
from ..rules import HasAbility, HasAllAbilities, HasAnyAbilities, HasAnyCharacterExcept
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_ENTRANCE_CORRIDOR = "Entrance Corridor"
R_FACTORY_CONVEYOR = "Factory Conveyor"
R_AFTER_FACTORY_CONVEYOR = "After Factory Conveyor"
R_COLOR_MIXING_ROOM = "Color Mixing Room"
R_FURNACE_START = "Furnace Start"
R_AFTER_FIRST_CRUCIBLE_PUZZLE = "After First Crucible Puzzle"
R_ROLLING_PLATFORMS_ROOM = "Rolling Platforms Room"
R_LAVA_ROOM = "Lava Room"
R_GEONOSIAN_HIVE = "Geonosian Hive"
R_FORCE_FIELDS_MAZE_ROOM = "Force Fields Maze Room"
R_GEONOSIAN_HIVE_ACROSS_LAVA = "Geonosian Hive Across Lava"
R_TWIN_CONVEYOR_ROOM = "Twin Conveyor Room"
R_OBI_WAN_HOLDING_CELL_ROOM = "Obi-Wan Holding Cell Room"


DROID_FACTORY = Chapter(
    area=Area.FACTORY,
    start_region=R_ENTRANCE_CORRIDOR,
    regions={
        R_ENTRANCE_CORRIDOR: (
            ExitData(
                R_FACTORY_CONVEYOR,
                logic_options(
                    # The Geonosians must be killed to proceed.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE,
                    # Allow Deflect Bolts.
                    moderate=CAN_DAMAGE_AT_CLOSE_RANGE | CAN_USE_DEFLECT_BOLTS,
                ),
                new_level=Level.FACTORY_B,
            ),
        ),
        R_FACTORY_CONVEYOR: (
            ExitData(
                R_AFTER_FACTORY_CONVEYOR,
                logic_options(
                    # No fancy tricks, just outrun the conveyor enough to pass under the crusher.
                    # There is a Droideka in the middle that base logic is expected to be able to defeat.
                    base=HasAbility(RUN_SPEED_0_9_OR_HIGHER) & CAN_DAMAGE_SHIELDED_DROIDEKA,
                    # Yoda/Yoda (Ghost) can attack to move faster.
                    # Boba Fett (Boy) can safely jump beneath the crusher, whereas other slow characters appear to be
                    # unable to, instead hitting the crusher's hurtbox and dying.
                    normal=Or(
                        HasAnyAbilities(RUN_SPEED_0_9_OR_HIGHER | JEDI),
                        Character.BOBA_FETT_BOY.has(),
                    ),
                    # All characters can walk around crushers by hugging the edge of the conveyor, except Gonk Droid,
                    # who is unable to walk over the slight increases in height between each flap along the edge of the
                    # conveyor.
                    # At moderate, we also expect jumping on the collapsing flaps to go around the crushers, potentially
                    # needing to restart the level if messing up.
                    moderate=Or(
                        HasAnyAbilities(RUN_SPEED_0_9_OR_HIGHER | CAN_BARELY_JUMP),
                        # HasAny(*(c for c in NON_VEHICLE_CHARACTER_BY_INDEX.values()
                        #        if c.is_sendable
                        #        and CAN_PASS_UNDER_DROID_FACTORY_CRUSHERS not in c.abilities
                        #        and JEDI not in c.abilities
                        #        and c.name != "Gonk Droid"))
                        Character.has_any(Character.C_3PO, Character.PK_DROID, Character.PIT_DROID, Character.TC_14),
                    ),
                    # Even Gonk Droid can actually move past the crushers because the trigger for the conveyor flaps
                    # collapsing does not extend all the way along the flap, so hugging the top of the flaps allows for
                    # walking along the flaps without them collapsing. The issue is that messing this up and causing
                    # *any* flap to drop requires restarting the level, and doing this sucks in general because of how
                    # slow Gonk Droid is.
                    # expert=True_(),
                ),
            ),
        ),
        R_AFTER_FACTORY_CONVEYOR: (
            ExitData(
                R_COLOR_MIXING_ROOM,
                logic_options(
                    # JEDI is definitely not needed, but I can't imagine it not being intended.
                    # GRAPPLE implies BLASTER.
                    base=HasAllAbilities(JEDI | GRAPPLE | BLASTER | IMPERIAL),
                    normal=And(
                        HasAnyAbilities(CAN_DOUBLE_JUMP | HOVER),
                        # Despite being a target, it is just a regular destroyable object.
                        CAN_DAMAGE_AT_CLOSE_RANGE,
                        HasAbility(IMPERIAL),
                    ),
                    # You can Wall Climb over the top of the wall, but the transition is inside the door collision, and
                    # I could not manage to hit it from behind.
                ),
            ),
            ExitData(
                R_FURNACE_START,
                logic_options(
                    # Force a fan and then float up.
                    base=HasAbility(JEDI),
                    # From the entrance to the Color Mixing Room, jetpack hover across.
                    normal=HasAnyAbilities(JEDI | JETPACK),
                    # Triple jump can also get up.
                    # The grapple point from the entrance to the Color Mixing Room can be stood on, so double jump onto
                    # it (only non-slam high jump is relevant here) and then astromech hover across.
                    moderate=Or(
                        HasAnyAbilities(JEDI | JETPACK | CAN_HIGH_JUMP_SLAM),
                        HasAllAbilities(CAN_DOUBLE_JUMP | HOVER),
                    ),
                ),
                new_level=Level.FACTORY_D,
            ),
        ),
        R_COLOR_MIXING_ROOM: (),
        R_FURNACE_START: (
            ExitData(
                R_AFTER_FIRST_CRUCIBLE_PUZZLE,
                logic_options(
                    base=Or(
                        # Activate the first two targets by grappling up to them and shooting the targets, then jump off
                        # the now moving crucible to get to the upper area.
                        CAN_GRAPPLE,
                        # Skip the first two targets and hover to the second, where objects must be destroyed to spawn
                        # a third target, and then the third target must be activated. A basic jump is required to get
                        # onto the crucible that is now moving up and down.
                        # This is considered intended because P2's AI will hover over here
                        HasAllAbilities(HOVER | JEDI) & CAN_ACTIVATE_CLOSE_TARGET
                    ),
                    # General Grievous can just high jump up with good timing so that he rolls forwards at the edge of
                    # the platform, but this is too niche of trick for normal imo.
                    normal=Or(
                        # Skip the first two targets, but instead of spawning and activating the third target, the
                        # machinery on the wall with the two lights has collision that can be stood on by jumping with
                        # high jump, which can then jump up to the upper area.
                        HasAllAbilities(HOVER | HIGH_JUMP),
                        And(
                            CAN_ACTIVATE_CLOSE_TARGET,
                            Or(
                                # Activate the first two targets.
                                CAN_GRAPPLE,
                                # Skip the first two targets [...]
                                HasAllAbilities(HOVER | JEDI)
                            ),
                        ),
                    ),
                    moderate=Or(
                        # Triple jump up to the second target platform and then the upper area, or triple jump across
                        # the hover gap to the third target, and then triple jump up to the upper area.
                        HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                        # Skip the first two targets, but instead of spawning and activating the third target, the
                        # machinery on the wall with the two lights has collision that can be stood on by jumping with
                        # high jump, which can then jump up to the upper area.
                        HasAllAbilities(HOVER | HIGH_JUMP),
                        # Activate the first two targets. can_grapple is irrelevant because JEDI alone can traverse this
                        # entrance, so can_activate_close_target is also irrelevant because all GRAPPLE have BLASTER.
                        HasAbility(GRAPPLE),
                    ),
                ),
            ),
        ),
        R_AFTER_FIRST_CRUCIBLE_PUZZLE: (
            ExitData(
                R_ROLLING_PLATFORMS_ROOM,
                logic_options(
                    base=HasAbility(ASTROMECH_PANEL),
                    # Allow Wall Climbing over the wall
                    hard=HasAbility(ASTROMECH_PANEL) | HAS_WALL_CLIMB,
                )
            ),
            ExitData(
                R_LAVA_ROOM,
                logic_options(
                    base=And(
                        HasAnyAbilities(HOVER | GRAPPLE | CAN_DOUBLE_JUMP),
                        HasAbility(ASTROMECH_PANEL),
                        CAN_DAMAGE_AT_CLOSE_RANGE,
                    ),
                    moderate=And(
                        HasAbility(ASTROMECH_PANEL),
                        Or(
                            HasAnyAbilities(HOVER | GRAPPLE | CAN_DOUBLE_JUMP),
                            HAS_FLUTTER_CHARACTER,
                        ),
                    ),
                ).or_rule(
                    # Wedge yourself between the two explosives closest to the panel.
                    # Swap to Droideka/Dexter (radii of 0.19).
                    # Roll/walk partially inside the door (don't go too far otherwise you cannot swap characters and
                    # will need to roll/walk/jump back out of the door)
                    # Character swap to upwarp to the collision floor on the top of the door.
                    # Walk forwards to hit the level transition.
                    apply_to="hard+",
                    # General Grievous is the character with next largest radius (excluding a few Extra Toggle
                    # characters not available in this level), at a radius of 0.13, but this is not enough to clip into
                    # the door.
                    rule=Or(
                        Character.DEXTER_JETTSTER.has(),
                        Character.DROIDEKA.has() & HasAbility(CAN_JUMP_HEIGHT_0_37),
                    ),
                    # Technically, you can wall climb here to get over the collision and hit the transition from behind,
                    # but the collision wall is huge and a significant part of the collision extends beyond the wall's
                    # model, making the wall climb close to blind towards the end.
                ),
                new_level=Level.FACTORY_E,
            ),
        ),
        R_ROLLING_PLATFORMS_ROOM: (),
        R_LAVA_ROOM: (
            ExitData(
                R_GEONOSIAN_HIVE,
                logic_options(
                    # The door has a protocol panel.
                    # Jedi can use the spinning platforms in the centre of the room.
                    # Hover can go basically wherever in this room.
                    # Grapple can take the outer route.
                    base=HasAbility(PROTOCOL_PANEL) & HasAnyAbilities(JEDI | HOVER | GRAPPLE),
                    # Jar Jar, Tarpals and Grievous can double jump across the spinning platforms.
                    # Grievous' Bodyguard also barely can, but jumping to the middle platform along the outside is
                    # easier (which Jedi can also jump to from the spinning platforms).
                    normal=HasAbility(PROTOCOL_PANEL) & HasAnyAbilities(JEDI | HOVER | GRAPPLE | HIGH_JUMP),
                    # Technically, you can wall climb here, but it seems that you need a specific line (some of the wall
                    # seems to not work), and the end of the climb is blind because the collision extends beyond the
                    # wall's model.
                ),
                new_level=Level.FACTORY_F,
            ),
        ),
        R_GEONOSIAN_HIVE: (
            ExitData(
                R_FORCE_FIELDS_MAZE_ROOM,
                CAN_DAMAGE_AT_CLOSE_RANGE,
            ),
            ExitData(
                R_GEONOSIAN_HIVE_ACROSS_LAVA,
                logic_options(
                    # Grapple up to the cave support thing and destroy it, force the platform and then jump across.
                    base=HasAllAbilities(GRAPPLE | JEDI),
                    normal=Or(
                        # Shoot the cave support thing from afar to avoid needing GRAPPLE.
                        HasAllAbilities(BLASTER | JEDI),
                        # Grapple up to the cave support thing, shoot it, and then hover across from the higher area.
                        And(
                            # Grapple or high jump up to the cave support thing and destroy it, then hover across.
                            Or(
                                HasAbility(GRAPPLE),
                                HasAbility(HIGH_JUMP) & CAN_DAMAGE_AT_CLOSE_RANGE,
                            ),
                            HasAbility(HOVER),
                        ),
                        # JETPACK implies GRAPPLE and HOVER, so JETPACK does not need to be checked explicitly.
                        # # JETPACK hover can actually just cross the entire gap.
                        # HasAbility(JETPACK),
                    ),
                    moderate=Or(
                        # JEDI/Grievous can triple jump up to the cave support now and just triple jump across the lava,
                        # or force the platform as Yoda.
                        HasAnyAbilities(JEDI | CAN_TRIPLE_JUMP_GREAT_DISTANCE),
                        And(
                            # Grapple or high jump up to the cave support thing and destroy it, then hover across.
                            Or(
                                HasAbility(GRAPPLE),
                                HasAbility(HIGH_JUMP) & CAN_DAMAGE_AT_CLOSE_RANGE,
                            ),
                            HasAbility(HOVER),
                        ),
                    ),
                ),
            ),
        ),
        R_FORCE_FIELDS_MAZE_ROOM: (),
        R_GEONOSIAN_HIVE_ACROSS_LAVA: (
            ExitData(
                R_TWIN_CONVEYOR_ROOM,
                HasAbility(PROTOCOL_PANEL),
                new_level=Level.FACTORY_G,
            ),
        ),
        R_TWIN_CONVEYOR_ROOM: (
            ExitData(
                R_OBI_WAN_HOLDING_CELL_ROOM,
                HasAllAbilities(JEDI | ASTROMECH_PANEL),
            ),
        ),
        R_OBI_WAN_HOLDING_CELL_ROOM: (
            ExitData(
                "Chapter Completion",
                # Impossible to get in here without JEDI.
                # HasAbility(JEDI),
            ),
        ),
    },
    minikits={
        "Minikit Behind Spawn Camera": minikit_data(
            R_ENTRANCE_CORRIDOR,
            pickup_name="m_pup1",
        ),
        "Entrance Corridor Right Alcove Minikit": minikit_data(
            R_ENTRANCE_CORRIDOR,
            logic_options(
                base=HasAbility(CAN_JUMP_HEIGHT_0_37),
                normal=HasAbility(CAN_BARELY_JUMP),
            ),
            pickup_name="m_pup2",
        ),
        "Conveyor Start Access Hatch Minikit": minikit_data(
            R_FACTORY_CONVEYOR,
            logic_options(
                # While it may become missable without restarting the chapter if the platform retracts before grabbing
                # this minikit, it is right towards the start of the chapter, and this is probably the developer
                # intended solution.
                base=HasAllAbilities(CAN_DOUBLE_JUMP | SHORTIE),
                # High jump can skip needing to use the Access Hatch.
                normal=Or(
                    HasAbility(HIGH_JUMP),
                    And(
                        HasAnyAbilities(JETPACK | CAN_DOUBLE_JUMP),
                        HasAbility(SHORTIE),
                    )
                ),
                # Triple jump gets more height than high jump, so all Jedi can also skip using the Access Hatch.
                moderate=Or(
                    HasAnyAbilities(JEDI | HIGH_JUMP),
                    HasAllAbilities(JETPACK | SHORTIE),
                ),
            ),
            pickup_name="mk_0",
        ),
        "Color Mixing Minikit": minikit_data(
            R_COLOR_MIXING_ROOM,
            HasAbility(ASTROMECH_PANEL),
            pickup_name="mk_1",
        ),
        "Minikit After First Crucibles": minikit_data(
            R_AFTER_FIRST_CRUCIBLE_PUZZLE,
            pickup_name="mk_0",
        ),
        "Rolling Platforms Minikit": minikit_data(
            R_ROLLING_PLATFORMS_ROOM,
            pickup_name="mk_1",
        ),
        "Lava Room Minikit": minikit_data(
            R_LAVA_ROOM,
            logic_options(
                base=CAN_GRAPPLE,
                # JEDI/HIGH_JUMP can jump from the corner of a spinning platform.
                normal=CAN_GRAPPLE | HasAbility(HIGH_JUMP),
            ),
            pickup_name="m_pup1",
        ),
        "High Minikit Inside Hive Wall": minikit_data(
            R_GEONOSIAN_HIVE,
            logic_options(
                # The jump is pretty tight, but seems to be intended.
                base=HasAllAbilities(JEDI | HIGH_JUMP),
                # Triple high jump straight up.
                moderate=HasAllAbilities(JEDI | HIGH_JUMP) | HasAbility(CAN_HIGH_JUMP_SLAM),
            ),
            pickup_name="mk_1",
        ),
        "Minikit Behind Droidekas Across Lava": minikit_data(
            R_GEONOSIAN_HIVE_ACROSS_LAVA,
            pickup_name="mk_0",
        ),
        "High Minikit In Twin Conveyor Room": minikit_data(
            R_TWIN_CONVEYOR_ROOM,
            logic_options(
                # Activate the left conveyor, force to build the platform, then high jump from the top after P2 has used
                # force to extend the platform.
                base=HasAllAbilities(JEDI | ASTROMECH_PANEL | HIGH_JUMP),
                normal=And(
                    HasAllAbilities(JEDI | ASTROMECH_PANEL),
                    Or(
                        HasAbility(HIGH_JUMP),
                        # Double jump slam with Stud Magnet active can reach the minikit.
                        Extra.STUD_MAGNET.has(),
                    ),
                ),
                # Triple jump reaches higher than high jump.
                moderate=Or(
                    HasAllAbilities(JEDI | ASTROMECH_PANEL),
                    # Stand on one of the astromech panel blocks for a bit of extra height, then triple high jump to the
                    # minikit.
                    HasAbility(CAN_HIGH_JUMP_SLAM),
                )
            ),
            pickup_name="m_pup1",
        )
    },
    power_brick=LocationData(
        R_FORCE_FIELDS_MAZE_ROOM,
        logic_options(
            # Complete the maze the intended way.
            base=HasAbility(ASTROMECH_PANEL),
            # Triple high jump over the force field walls.
            # Yoda triple jumps are allowed due to their better height.
            moderate=Or(
                HasAnyAbilities(ASTROMECH_PANEL | CAN_HIGH_JUMP_SLAM),
                HAS_ANY_YODA & HasAnyCharacterExcept(Character.YODA, Character.YODA_GHOST),
            ),
            # Jedi triple jump can also just barely get over the walls with a near max height triple jump.
            # This maybe could be in moderate logic, but feels surprisingly difficult, so is only in hard logic
            # currently.
            hard=HasAnyAbilities(ASTROMECH_PANEL | CAN_HIGH_JUMP_SLAM | JEDI),
        )
    ),
)

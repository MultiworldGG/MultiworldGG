from rule_builder.rules import And, Or, True_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_USE_DEFLECT_BOLTS,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
)
from ..option_filters import logic_options, OT_HIGH_JUMP_ENABLED, OT_HIGH_JUMP_DISABLED
from ..rules import HasAbility, HasAnyAbilities, HasAllAbilities, HasAbilityExceptCharacters
from ..types import minikit_data, ExitData, ChapterHelper, LocationData, MinikitData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_FIRST_HALLWAY = "First Hallway"
R_SECOND_HALLWAY = "Second Hallway"
R_SITH_DOUBLE_SCORE_ZONE = "Sith Double Score Zone"
R_GRAPPLE_ROOM = "Grapple Room"
R_GRAPPLE_ROOM_TOP = "Grapple Room Top"
R_VADER_EXPLOSIVES_HALLWAY = "Vader Explosives Hallway"
R_SECOND_STORMTROOPER_BATTLE = "Second Stormtrooper Battle"
R_SIDE_ACCESS_CORRIDOR = "Side Access Corridor"
R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD = "Side Access Corridor Behind Force Field"
R_SLIDING_BLOCKS_ROOM = "Sliding Blocks Room"
R_ACCESS_CORRIDOR_BEFORE_R2_D2_AND_LEIA = "Access Corridor Before R2-D2 And Leia"
R_R2_D2_AND_LEIA_ACCESS_CORRIDOR = "R2-D2 And Leia Access Corridor"
R_CRANE_ROOM = "Crane Room"
R_CRANE_ROOM_ACROSS_GAP = "Crane Room Across Gap"
R_CAPTIVE_REBELS_HALLWAY = "Captive Rebels Hallway"
R_VENT_IMPERIALS_INTO_SPACE = "Vent Imperials Into Space Room"
R_ESCAPE_POD_CORRIDOR = "Escape Pod Corridor"


_helper = ChapterHelper(
    area=Area.BLOCKADERUNNER,
    start_region=R_SPAWN,
)

# The ridables logic is also used in a Minikit location that requires riding a vehicle, so the individual logic is
# created here, and referenced in both that Minikit location's logic and the individual ridables' logic.
MOON_CAR_LOGIC = logic_options(
    base=HasAbility(CAN_BUILD_BRICKS) & CAN_DESTROY_CLOSE_SILVER_BRICKS,
    hard=And(
        HasAbility(CAN_BUILD_BRICKS),
        Or(
            CAN_DESTROY_CLOSE_SILVER_BRICKS,
            # You can push a stormtrooper all the way into the corridor and deflect one of their bolts into
            # near the silver bricks.
            # Only relevant to Darth Vader/The Emperor/Imperial Guard while there is no panel randomizer.
            Extra.EXPLODING_BLASTER_BOLTS.has() & CAN_USE_DEFLECT_BOLTS,
        ),
    ),
)
TOWN_CAR_LOGIC = HasAbility(JEDI)

SECRET_PLANS = _helper.make_chapter(
    regions={
        _helper.start_region: (
            ExitData(R_FIRST_HALLWAY, HasAbility(CAN_BUILD_BRICKS), name="Build bricks to restore power"),
        ),
        R_FIRST_HALLWAY: (
            ExitData(R_SECOND_HALLWAY, HasAbility(CAN_PULL_LEVERS), name="Open lever door"),
        ),
        R_SECOND_HALLWAY: (
            ExitData(R_SITH_DOUBLE_SCORE_ZONE, CAN_SITH_FORCE),
            # The Stormtroopers must be defeated to continue.
            ExitData(R_GRAPPLE_ROOM, CAN_DAMAGE_AT_CLOSE_RANGE, new_level=Level.BLOCKADERUNNER_B),
        ),
        R_SITH_DOUBLE_SCORE_ZONE: (),
        R_GRAPPLE_ROOM: (
            ExitData(
                R_GRAPPLE_ROOM_TOP,
                # The astromech panel is useless because the elevator can only go to the top once the bridge has been
                # extended, which requires reacing the top.
                logic_options(
                    base=CAN_GRAPPLE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                    # Triple jump up.
                    moderate=CAN_GRAPPLE | CAN_ORIGINAL_TRILOGY_HIGH_JUMP | HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                ),
            ),
        ),
        R_GRAPPLE_ROOM_TOP: (
            ExitData(
                R_VADER_EXPLOSIVES_HALLWAY,
                logic_options(
                    # High jumpers, except Bodyguard can high jump across the gap.
                    # All Jedi can build, so the triple jump great distance includes General Grievous for no logic cost.
                    base=Or(
                        HasAnyAbilities(CAN_BUILD_BRICKS | HOVER),
                        HasAbilityExceptCharacters(HIGH_JUMP, Character.GRIEVOUS_BODYGUARD) & OT_HIGH_JUMP_ENABLED,
                    ),
                    # Bodyguard has to go one floor down, and jump from there instead.
                    # Yoda can double jump across the gap without building the bridge, though that has no logic
                    # relevance.
                    normal=HasAnyAbilities(CAN_BUILD_BRICKS | HOVER) | CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
                ),
            ),
        ),
        R_VADER_EXPLOSIVES_HALLWAY: (
            ExitData(
                R_SECOND_STORMTROOPER_BATTLE,
                # Ewok weapons do not work on the explosives.
                # Super Jedi Slam cannot reach.
                logic_options(
                    base=HasAllAbilities(CAN_PULL_LEVERS | BLASTER),
                    normal=And(
                        HasAbility(CAN_PULL_LEVERS),
                        Or(
                            HasAbility(BLASTER),
                            And(
                                HasAbility(WEAPON_EWOK),
                                Extra.has_any(Extra.EXPLODING_BLASTER_BOLTS, Extra.SUPER_EWOK_CATAPULT),
                            ),
                        ),
                    ),
                    # Adds deflecting bolts with Exploding Blaster Bolts active.
                    moderate=And(
                        HasAbility(CAN_PULL_LEVERS),
                        Or(
                            HasAbility(BLASTER),
                            And(
                                HasAbility(WEAPON_EWOK),
                                Extra.has_any(Extra.EXPLODING_BLASTER_BOLTS, Extra.SUPER_EWOK_CATAPULT),
                            ),
                            # Exploding Blaster Bolts is technically not required, but it would be *extremely* slow
                            # relying on random deflections to hit the explosives enough times.
                            # The Stormtroopers can be aggro-ed with a melee-only character, by attacking one of the
                            # boxes in the same area, so getting aggro with a melee character is fine.
                            Extra.EXPLODING_BLASTER_BOLTS.has() & CAN_USE_DEFLECT_BOLTS,
                        ),
                    ),
                ),
            ),
        ),
        R_SECOND_STORMTROOPER_BATTLE: (
            ExitData(R_SIDE_ACCESS_CORRIDOR, HasAnyAbilities(IMPERIAL | BOUNTY_HUNTER)),
            ExitData(
                R_SLIDING_BLOCKS_ROOM,
                logic_options(
                    base=CAN_DAMAGE_AT_CLOSE_RANGE,
                    # You can just ignore these Stormtroopers.
                    normal=True_(),
                ),
                new_level=Level.BLOCKADERUNNER_C
            ),
        ),
        R_SIDE_ACCESS_CORRIDOR: (
            ExitData(R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD, HasAbility(PROTOCOL_PANEL)),
        ),
        R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD: (),
        R_SLIDING_BLOCKS_ROOM: (
            ExitData(R_ACCESS_CORRIDOR_BEFORE_R2_D2_AND_LEIA, HasAbility(CAN_PUSH_OBJECTS) & CAN_DAMAGE_AT_CLOSE_RANGE),
        ),
        R_ACCESS_CORRIDOR_BEFORE_R2_D2_AND_LEIA: (
            ExitData(R_R2_D2_AND_LEIA_ACCESS_CORRIDOR, HasAbility(PROTOCOL_PANEL)),
        ),
        R_R2_D2_AND_LEIA_ACCESS_CORRIDOR: (
            ExitData(R_CRANE_ROOM, HasAbility(ASTROMECH_PANEL)),
        ),
        R_CRANE_ROOM: (
            ExitData(
                R_CRANE_ROOM_ACROSS_GAP,
                logic_options(
                    base=HasAbility(CAN_RIDE_VEHICLES),
                    # Grievous and Bodyguard cannot ride vehicles, but can jump on the silver brick object, and then
                    # jump onto the raise platforms to walk across without using the crane.
                    normal=HasAnyAbilities(CAN_RIDE_VEHICLES | CAN_DOUBLE_JUMP),
                    # Astromech droids can hover onto the side of the platform the minikit spawns above, hover across to
                    # one of the fences around the gap, and then hover across to the other side.
                    moderate=HasAnyAbilities(CAN_RIDE_VEHICLES | CAN_DOUBLE_JUMP | HOVER),
                )
            ),
        ),
        R_CRANE_ROOM_ACROSS_GAP: (
            ExitData(
                R_CAPTIVE_REBELS_HALLWAY,
                # Alternatively, use the crane to pick up P2 and carry them to the panel, but all characters that
                # can use the crane have at jump that can cross the gap...
                # moderate=HasAbility(PROTOCOL_PANEL) & HasAnyAbilities(CAN_BARELY_JUMP | CAN_RIDE_VEHICLES),
                HasAllAbilities(PROTOCOL_PANEL | CAN_BARELY_JUMP),
                new_level=Level.BLOCKADERUNNER_D
            ),
        ),
        R_CAPTIVE_REBELS_HALLWAY: (
            ExitData(R_ESCAPE_POD_CORRIDOR, CAN_DAMAGE_AT_CLOSE_RANGE),
        ),
        R_ESCAPE_POD_CORRIDOR: (
            ExitData(R_VENT_IMPERIALS_INTO_SPACE, HasAbility(IMPERIAL)),
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL | CAN_PULL_LEVERS),
                    # Allow Yoda ceiling clip into the escape pod. Unlike the other escape pods, where the levers do not
                    # appear to be usable until the escape pod doors have opened, the astromech panel in the right
                    # escape pod can be used without opening the escape pod door first.
                    hard=Or(
                        HasAllAbilities(PROTOCOL_PANEL | ASTROMECH_PANEL | CAN_PULL_LEVERS),
                        HasAbility(ASTROMECH_PANEL) & CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                    ),
                ),
            ),
        ),
        R_VENT_IMPERIALS_INTO_SPACE: (),
    },
    minikits={
        "Dark Side Double Score Zone Minikit": minikit_data(
            R_SITH_DOUBLE_SCORE_ZONE,
            pickup_name="m_pup1",
        ),
        "Grapple Room Beneath Floor Minikit": minikit_data(
            R_GRAPPLE_ROOM,
            logic_options(
                # General Grievous is too big to walk around under here, though that is fortunately not logically
                # relevant.
                # Expect getting back out, so that the level does not need to be restarted.
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS & HasAbility(CAN_DOUBLE_JUMP),
                normal=CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ),
            pickup_name="mk_0",
        ),
        "Grapple Room High Minikit": minikit_data(
            R_GRAPPLE_ROOM_TOP,
            logic_options(
                base=HasAbility(JEDI),
                moderate=Or(
                    HasAbility(JEDI),
                    # Triple jump. With High Jump disabled, General Grievous can only just get this minikit by using
                    # Stud Magnet.
                    (Extra.STUD_MAGNET.has() & Character.GENERAL_GRIEVOUS.has()) & OT_HIGH_JUMP_DISABLED,
                    HasAbility(CAN_HIGH_JUMP_SLAM) & OT_HIGH_JUMP_ENABLED,
                )
            ),
            pickup_name="m_pup2",
        ),
        "Build Door Minikit": minikit_data(
            R_SIDE_ACCESS_CORRIDOR,
            HasAbility(CAN_BUILD_BRICKS),
            pickup_name="mk_1",
        ),
        "Three Grape Tiles Minikit": MinikitData(
            # Physically, this minikit spawns in Side Access Corridor.
            # Logically this is behind the force field because one of the tiles is there, and to access that tile means
            # you have access to where the minikit spawns.
            R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD,
            CAN_DAMAGE_AT_CLOSE_RANGE,
            pickup_names=(
                "m_pup1",
                "m_pup3",
                "m_pup4",
            ),
        ),
        "Sliding Blocks Room Minikit": minikit_data(
            R_SLIDING_BLOCKS_ROOM,
            logic_options(
                base=HasAbility(JEDI),
                # You can jump onto the curved terrain, and then jump to the minikit.
                normal=HasAbility(CAN_DOUBLE_JUMP),
            ),
            pickup_name="mk_0",
        ),
        "Secret Wall Compartment Minikit": minikit_data(
            R_R2_D2_AND_LEIA_ACCESS_CORRIDOR,
            HasAbility(JEDI),
            pickup_name="pup1",
        ),
        "Crane Room Ride A Car Minikit": minikit_data(
            R_CRANE_ROOM,
            # The ridesanity entrances won't exist unless Ridesanity is enabled, so the access rules from them are
            # copied here.
            And(
                # HasAbility(CAN_RIDE_VEHICLES) is only automatically added to ridable rules, so, in this minikit rule,
                # HasAbility(CAN_RIDE_VEHICLES) must be explicitly checked.
                HasAbility(CAN_RIDE_VEHICLES),
                Or(
                    _helper.can_reach_region(R_SIDE_ACCESS_CORRIDOR) & MOON_CAR_LOGIC,
                    _helper.can_reach_region(R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD) & TOWN_CAR_LOGIC,
                ),
            ),
            pickup_name="m_pup1",
        ),
        "Three Flowers Minikit": MinikitData(
            R_ESCAPE_POD_CORRIDOR,
            logic_options(
                base=And(
                    CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    _helper.can_reach_region(R_VENT_IMPERIALS_INTO_SPACE),
                ),
                moderate=And(
                    Or(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        # Darth Vader, The Emperor and Imperial Guard can deflect bolts fired by stormtroopers into near
                        # the silver bricks, exploding them.
                        Extra.EXPLODING_BLASTER_BOLTS.has() & CAN_USE_DEFLECT_BOLTS,
                    ),
                    _helper.can_reach_region(R_VENT_IMPERIALS_INTO_SPACE),
                ),
            ),
            pickup_names=(
                "m_pup3",
                "m_pup2",
                "m_pup4",
            ),
        ),
        "Pull The Plug Minikit": minikit_data(
            R_ESCAPE_POD_CORRIDOR,
            CAN_SITH_FORCE & HasAbility(ASTROMECH_PANEL),
            pickup_name="m_pup1",
        ),
    },
    power_brick=LocationData(R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD, HasAbility(JEDI)),
    ridables={
        Character.MOONCAR: LocationData(R_SIDE_ACCESS_CORRIDOR, MOON_CAR_LOGIC),
        Character.TOWNCAR: LocationData(R_SIDE_ACCESS_CORRIDOR_BEHIND_FORCE_FIELD, TOWN_CAR_LOGIC),
        Character.GRABBERCONTROL: LocationData(R_CRANE_ROOM),
    },
)

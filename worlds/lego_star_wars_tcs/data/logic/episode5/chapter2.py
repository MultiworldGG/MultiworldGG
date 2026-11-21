from rule_builder.rules import And, Or, False_, True_

from ..macros import (
    CAN_DAMAGE_AT_CLOSE_RANGE,
    CAN_SITH_FORCE,
    CAN_DESTROY_CLOSE_SILVER_BRICKS,
    CAN_GRAPPLE,
    CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
    CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
    CAN_USE_DEFLECT_BOLTS,
    HAS_ANY_YODA,
    CAN_ORIGINAL_TRILOGY_HIGH_JUMP,
)
from ..option_filters import logic_options, ot_high_jump_ternary
from ..rules import (
    HasAbility,
    HasAnyAbilities,
    HasAllAbilities,
)
from ..types import minikit_data, ExitData, ChapterHelper, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_FIRST_CORRIDOR = "First Corridor"
R_BREAK_ROOM = "Break Room"
R_CROSSROADS_CORRIDOR_WITH_TURRET = "Crossroads Corridor With Turret"
R_LARGE_ICY_ROOM_WITH_FLOOR_FANS_THROUGH_TO_ICE_SLIDE_ROOM = "Large Icy Room With Floor Fans, through to Ice Slide Room"
R_SNOWTROOPER_FISHING_ROOM = "Snowtrooper Fishing Room"
R_BLOCKED_OFF_FLOOR_FAN_ROOM = "Blocked Off Floor Fan Room"
R_AFTER_ICE_SLIDE_ROOM_START_OF_DOUBLE_SCORE_ZONE_ROOM_AND_HANGAR = ("After Ice Slide Room, Start Of Double Score Zone"
                                                                     " Room, and Hangar")
R_DOUBLE_SCORE_ZONE_TUBE_ROOM = "Double Score Zone Tube Room"
R_HANGAR_OBSERVATION_ROOM = "Hangar Observation Room"
R_TOP_OF_SLIPPERY_SNOW_SLOPE = "Top Of Slippery Snow Slope"
R_SNOW_CANOPY_AREA = "Snow Canopy Area"


_helper = ChapterHelper(
    area=Area.HOTHESCAPE,
    start_region=R_SPAWN,
)


ESCAPE_FROM_ECHO_BASE = _helper.make_chapter(
    regions={
        R_SPAWN: (
            ExitData(
                R_FIRST_CORRIDOR,
                HasAbility(CAN_BUILD_BRICKS),
            ),
        ),
        R_FIRST_CORRIDOR: (
            ExitData(
                R_BREAK_ROOM,
                logic_options(
                    strict=False,
                    # Tarpals cannot hit the heater.
                    base=CAN_DAMAGE_AT_CLOSE_RANGE_NO_BASIC_MELEE,
                # You can deflect bolts from the three snowtroopers into the heater after building it.
                ).or_rule(
                    apply_to="moderate+",
                    rule=logic_options(
                        base=False_(),
                        # It is a bit inconsistent because there are only 3 enemies, which don't respawn, and the heater
                        # needs to be hit 3 times to proceed, so expect Exploding Blaster Bolts, which fully activates
                        # the heater in a single shot (and probably killing the player in the process).
                        moderate=CAN_USE_DEFLECT_BOLTS & Extra.EXPLODING_BLASTER_BOLTS.has(),
                        # It's definitely doable without Exploding Blaster Bolts however, so Hard logic expects without.
                        hard=CAN_USE_DEFLECT_BOLTS,
                    ),
                ),
            ),
        ),
        R_BREAK_ROOM: (
            ExitData(
                R_CROSSROADS_CORRIDOR_WITH_TURRET,
                HasAbility(CAN_PUSH_OBJECTS)
            ),
        ),
        R_CROSSROADS_CORRIDOR_WITH_TURRET: (
            ExitData(
                R_LARGE_ICY_ROOM_WITH_FLOOR_FANS_THROUGH_TO_ICE_SLIDE_ROOM,
                # If you can reach here, you can build bricks, and can ride vehicles (implied by CAN_PUSH_OBJECTS).
                # You can yoda clip over the door, but the level transition trigger is not present until the panel is
                # used.
                HasAbility(PROTOCOL_PANEL),
                er_rule=HasAllAbilities(PROTOCOL_PANEL | CAN_RIDE_VEHICLES),
                new_level=Level.HOTHESCAPE_B,
            ),
        ),
        R_LARGE_ICY_ROOM_WITH_FLOOR_FANS_THROUGH_TO_ICE_SLIDE_ROOM: (
            ExitData(
                R_SNOWTROOPER_FISHING_ROOM,
                # The player must have a PROTOCOL_PANEL character to reach here.
                HasAbility(ASTROMECH_PANEL) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS
            ),
            ExitData(
                R_BLOCKED_OFF_FLOOR_FAN_ROOM,
                HasAbility(JEDI),
            ),
            ExitData(
                R_AFTER_ICE_SLIDE_ROOM_START_OF_DOUBLE_SCORE_ZONE_ROOM_AND_HANGAR,
                new_level=Level.HOTHESCAPE_C,
            ),
        ),
        R_SNOWTROOPER_FISHING_ROOM: (),
        R_BLOCKED_OFF_FLOOR_FAN_ROOM: (),
        R_AFTER_ICE_SLIDE_ROOM_START_OF_DOUBLE_SCORE_ZONE_ROOM_AND_HANGAR: (
            ExitData(
                R_DOUBLE_SCORE_ZONE_TUBE_ROOM,
                logic_options(
                    base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
                    # You don't even need to Yoda clip. The silver brick collision that blocks access doesn't extend all
                    # the way to the ceiling. Most characters are too big to fit through the gap over the top, but Yoda
                    # fits and can easily double jump over.
                    moderate=CAN_DESTROY_CLOSE_SILVER_BRICKS | HAS_ANY_YODA,
                    # Allow swapping from a double jump character to a character that is short enough to fit through the
                    # gap.
                    hard=Or(
                        CAN_DESTROY_CLOSE_SILVER_BRICKS,
                        HAS_ANY_YODA,
                        # todo: Try more small characters
                        And(
                            # A box needs to be destroyed for the door to open.
                            CAN_DAMAGE_AT_CLOSE_RANGE,
                            # Astromech Droids fit in the gap.
                            HasAllAbilities(CAN_DOUBLE_JUMP | ASTROMECH_DROID),
                        ),
                    ),
                ),
            ),
            ExitData(
                R_TOP_OF_SLIPPERY_SNOW_SLOPE,
                CAN_SITH_FORCE,
            ),
            ExitData(
                R_HANGAR_OBSERVATION_ROOM,
                logic_options(
                    base=False_(),
                    # In the front of the hangar, you can clip into the 'observation area' with the RNG levers that lift
                    # the shutters in the hangar. Use the boxes in the corner for extra height, otherwise the clip is
                    # really difficult, even with characters that are easiest to clip with, like Droideka and General
                    # Grievous.
                    hard=CAN_SITH_FORCE | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                ),
            ),
            ExitData(
                "Chapter Completion",
            ),
        ),
        R_DOUBLE_SCORE_ZONE_TUBE_ROOM: (),
        R_HANGAR_OBSERVATION_ROOM: (
            ExitData(
                R_TOP_OF_SLIPPERY_SNOW_SLOPE,
                logic_options(
                    base=False_(),
                    hard=CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS
                ),
            ),
        ),
        R_TOP_OF_SLIPPERY_SNOW_SLOPE: (
            ExitData(
                R_HANGAR_OBSERVATION_ROOM,
                # Hard logic can Yoda Clip to skip the Astromech Panel, but hard logic can Yoda Clip from the hangar to
                # the observation room anyway, so it is not logically relevant to consider Yoda Clip to bypass the
                # Astromech Panel.
                HasAbility(ASTROMECH_PANEL),
                er_rule=logic_options(
                    base=HasAbility(ASTROMECH_PANEL),
                    hard=HasAbility(ASTROMECH_PANEL) | CAN_YODA_CLIP_SKIP_OTHER_CHARACTERS,
                )
            ),
            ExitData(
                R_SNOW_CANOPY_AREA,
                logic_options(
                    base=CAN_GRAPPLE,
                    # You can triple/high jump to hit the trigger. For Jar Jar and Tarpals, you will need to stand on
                    # the closest destroyable box for extra height.
                    moderate=ot_high_jump_ternary(
                        uncapped=HasAnyAbilities(GRAPPLE | JEDI | HIGH_JUMP),
                        capped=HasAnyAbilities(GRAPPLE | JEDI | CAN_HIGH_JUMP_SLAM),
                    ),
                ),
                new_level=Level.HOTHESCAPE_D,
            ),
        ),
        R_SNOW_CANOPY_AREA: (),
    },
    minikits={
        "Spawn Room Consoles Minikit": minikit_data(
            R_SPAWN,
            HasAbility(JEDI),
            pickup_name="m_pup2",
        ),
        "Double Score Zone Alcove Above Track Minikit": minikit_data(
            # The player has to be able to destroy/activate the heater earlier in the level to get here, so they must be
            # able to destroy the boxes blocking access to the door. Though you can also just build and ride the turret,
            # since all characters that can push blocks can ride vehicles and vice versa.
            R_CROSSROADS_CORRIDOR_WITH_TURRET,
            logic_options(
                # Expect double jump so that if the player sends away the cart before getting the minikit, they can
                # still get the minikit.
                base=HasAbility(CAN_DOUBLE_JUMP),
                # CAN_BUILD_BRICKS and CAN_PUSH_OBJECTS are required to reach here.
                # Characters with CAN_BUILD_BRICKS all have at least 0.37 jump height, which is enough to jump from the
                # cart to the minikit.
                normal=True_(),
            ),
            er_rule=logic_options(
                base=HasAbility(CAN_DOUBLE_JUMP),
                normal=Or(
                    HasAllAbilities(CAN_JUMP_HEIGHT_0_37 | CAN_BUILD_BRICKS),
                    HasAbility(CAN_DOUBLE_JUMP)
                ),
            ),
            pickup_name="m_pup3",
        ),
        "Four Buttons Thaw Skeletons Minikit": minikit_data(
            R_CROSSROADS_CORRIDOR_WITH_TURRET,
            logic_options(
                strict=False,
                base=CAN_DESTROY_CLOSE_SILVER_BRICKS,
            ).or_rule(
                apply_to="moderate+",
                # 'Encourage' two snowtroopers (using the turret spawns two) onto the buttons. Extras are logically
                # expected for survivability. Deflect Bolts is too likely to kill the snowtroopers, so is not
                # considered for survivability in this case.
                rule=And(
                    # Passive characters cannot get here on their own due to needing to both build bricks and deal
                    # damage, except force ghosts, who cannot push enemies.
                    HasAbility(CAN_AGGRAVATE_ENEMIES),
                    Extra.has_any(Extra.INVINCIBILITY, Extra.DISARM_TROOPERS, Extra.REGENERATE_HEARTS)
                ),
            ).or_rule(
                apply_to="hard+",
                # Bring snowtroopers to the silver bricks and then deflect their bolts into the silver bricks with
                # Exploding Blaster Bolts active.
                rule=CAN_USE_DEFLECT_BOLTS & Extra.EXPLODING_BLASTER_BOLTS.has(),
            ),
            # Expert logic probably could use a force ghost + passive character to force confuse the snowtroopers and
            # then push the snowtroopers onto the buttons with the non-force-ghost passive character. The force confuse
            # is necessary because the snowtroopers have an idle walk path that they follow.
            pickup_name="m_pup1",
        ),
        "High Minikit In Snowmobile Room": minikit_data(
            R_LARGE_ICY_ROOM_WITH_FLOOR_FANS_THROUGH_TO_ICE_SLIDE_ROOM,
            # Build the snowmobile, stand on it, and then double jump to the minikit.
            # Or double jump + slam directly under the minikit.
            # Or high jump (when enabled) under the minikit.
            # Character jump height seems to determine how high they get launched by the snowmobile, so the
            # snowmobile does not help much.
            HasAbility(CAN_DOUBLE_JUMP),
            er_rule=logic_options(
                base=Or(
                    HasAllAbilities(CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP | CAN_RIDE_VEHICLES),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP
                ),
                moderate=Or(
                    HasAllAbilities(CAN_BUILD_BRICKS | CAN_DOUBLE_JUMP | CAN_RIDE_VEHICLES),
                    HasAnyAbilities(JEDI | CAN_HIGH_JUMP_SLAM),
                    CAN_ORIGINAL_TRILOGY_HIGH_JUMP
                )
            ),
            pickup_name="pup4",
        ),
        "Hidden Minikit In Snowmobile Room Wall": minikit_data(
            R_LARGE_ICY_ROOM_WITH_FLOOR_FANS_THROUGH_TO_ICE_SLIDE_ROOM,
            pickup_name="pup2",
        ),
        "Snowtrooper Fishing Minikit": minikit_data(
            R_SNOWTROOPER_FISHING_ROOM,
            HasAbility(JEDI),
            pickup_name="pup1",
        ),
        "Fan Minikit In Blocked Off Room": minikit_data(
            R_BLOCKED_OFF_FLOOR_FAN_ROOM,
            pickup_name="m_pup1",
        ),
        "Minikit In Double Score Zone Tube": minikit_data(
            R_DOUBLE_SCORE_ZONE_TUBE_ROOM,
            pickup_name="pup1",
        ),
        "Minikit Inside Green-Yellow Shutter": minikit_data(
            R_AFTER_ICE_SLIDE_ROOM_START_OF_DOUBLE_SCORE_ZONE_ROOM_AND_HANGAR,
            _helper.can_reach_region(R_HANGAR_OBSERVATION_ROOM) & HasAbility(CAN_PULL_LEVERS),
            pickup_name="pup2",
        ),
        "Snow Canopy Access Hatch Minikit": minikit_data(
            R_SNOW_CANOPY_AREA,
            # There are infinite walls all around the spawn, you can Yoda Clip through the ceiling, but then have
            # infinite walls surrounding you.
            HasAbility(SHORTIE),
            pickup_name="pup1",
        )
    },
    power_brick=LocationData(
        R_AFTER_ICE_SLIDE_ROOM_START_OF_DOUBLE_SCORE_ZONE_ROOM_AND_HANGAR,
        _helper.can_reach_region(R_HANGAR_OBSERVATION_ROOM) & HasAbility(CAN_PULL_LEVERS),
    ),
    ridables={
        Character.TROOPERCANNON: LocationData(R_CROSSROADS_CORRIDOR_WITH_TURRET),
        Character.SNOWMOB: LocationData(R_LARGE_ICY_ROOM_WITH_FLOOR_FANS_THROUGH_TO_ICE_SLIDE_ROOM),
        Character.TAUNTAUN: LocationData(R_AFTER_ICE_SLIDE_ROOM_START_OF_DOUBLE_SCORE_ZONE_ROOM_AND_HANGAR),
    },
)

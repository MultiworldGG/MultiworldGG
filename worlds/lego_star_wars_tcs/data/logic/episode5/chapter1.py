from rule_builder.rules import True_

from ..option_filters import logic_options
from ..rules import HasAbility
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...characters import Character
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_FIRST_AREA_BEHIND_TIE_GATE = "First Area Behind TIE Gate"
R_FIRST_AREA_TIE_GATE_CAVE = "First Area TIE Gate Cave"
R_SECOND_AREA_SPAWN = "Second Area Spawn"
R_SECOND_AREA_BEHIND_TIE_GATE = "Second Area Behind TIE Gate"
R_FINAL_BATTLE = "Final Battle"


HOTH_BATTLE = Chapter(
    area=Area.HOTHBATTLE,
    start_region=R_SPAWN,
    regions={
        R_SPAWN: (
            ExitData(
                R_FIRST_AREA_BEHIND_TIE_GATE,
                logic_options(
                    base=HasAbility(VEHICLE_TIE),
                    # Skip the gate by performing a loop and dropping in P2 at the top of the loop.
                    # Use the height from the loop to bypass the gate (easily with larger vehicles), using the fact
                    # that P1 and P2 will push each other apart to gain movement over the gate (may be required for
                    # smaller vehicles.
                    # I'm pretty sure that every vehicle can clear this gate, though large vehicles are far easier.
                    hard=True_(),
                ),
            ),
            ExitData(
                R_SECOND_AREA_SPAWN,
                # I am aware of a clip involving Arcfighter, but have been unable to pull it off. Perhaps it requires a
                # specific refresh rate. Theoretically, if you could get enough height, and speed, the next level
                # trigger extends above the mountain and is active even without destroying the wall. I tried similar
                # tricks to the TIE gate skips in this level, but could not get anything to work.
                HasAbility(VEHICLE_TOW),
                new_level=Level.HOTHBATTLE_C,
            )
        ),
        R_FIRST_AREA_BEHIND_TIE_GATE: (
            ExitData(
                R_FIRST_AREA_TIE_GATE_CAVE,
                logic_options(
                    base=HasAbility(VEHICLE_TOW),
                    # Similar to the TIE gate, I think every vehicle can get over the top of the wall by using the same
                    # trick.
                    hard=True_(),
                ),
                new_level=Level.HOTHBATTLE_B,
            ),
        ),
        R_FIRST_AREA_TIE_GATE_CAVE: (),
        R_SECOND_AREA_SPAWN: (
            ExitData(
                R_SECOND_AREA_BEHIND_TIE_GATE,
                logic_options(
                    strict=False,
                    base=HasAbility(VEHICLE_TIE),
                # The level transition trigger extends above the mountain again, so you can do similar to the first TIE
                # gate skip by performing a loop as P1 and dropping in P2 to get enough height to drive up the mountain
                # and hit the level transition trigger. The right side seems to be easiest to get up and vehicles with
                # big loops, low gravity and high speed area easiest.
                # Try to loop next to the arch instead of under the arch because looping under the arch tends to give
                # the vehicle a lot of momentum away from the arch.
                # Vehicles that can get a lot of height may even skip over the level transition trigger, potentially
                # hitting the return trigger by mistake.
                ).or_rule(
                    apply_to="hard+",
                    rule=Character.has_any(
                        Character.CLONE_ARCFIGHTER,
                        Character.ANAKINS_POD,  # High speed makes up for lower loop height.
                        Character.NABOO_STARFIGHTER,
                        Character.X_WING,
                        Character.Y_WING,
                        # Character.SNOWSPEEDER,  # Might not be possible, I could not get enough height/speed.
                        Character.MILLENNIUM_FALCON,
                        Character.IMPERIAL_SHUTTLE,
                        Character.SLAVE_1,
                        # Character.ANAKINS_SPEEDER,  # Might not be possible, I could not get enough height/speed.
                        Character.REPUBLIC_GUNSHIP,  # More difficult due to lower loop height.
                        Character.JEDI_STARFIGHTER_YELLOW,  # More difficult due to lower loop height.
                        Character.JEDI_STARFIGHTER_RED,  # More difficult due to lower loop height.
                        Character.SEBULBAS_POD,  # High speed makes up for lower loop height.
                        # Character.ZAMS_AIRSPEEDER,  # Might not be possible, I could not get enough height/speed.
                        # Maybe possible, but it would probably be too difficult for Hard logic if it is.
                        # Character.DROID_TRIFIGHTER,
                    ),
                ),
                new_level=Level.HOTHBATTLE_D,
            ),
            ExitData(
                R_FINAL_BATTLE,
                new_level=Level.HOTHBATTLE_E,
            ),
        ),
        R_SECOND_AREA_BEHIND_TIE_GATE: (),
        R_FINAL_BATTLE: (
            ExitData("Chapter Completion"),
        ),
    },
    minikits={
        "Minikit Behind Wall In First Area": minikit_data(
            R_SPAWN,
            logic_options(
                base=HasAbility(VEHICLE_BLASTER),
                # Torpedoes do not target the minikit, and while hitting the minikit with a torpedo isn't too hard, the
                # torpedoes are still likely to miss, so I'm not putting this into Normal logic.
                moderate=HasAbility(VEHICLE_BLASTER) | Extra.INFINITE_TORPEDOS.has(),
                # Also allow Deflect Bolts.
                hard=HasAbility(BLASTER) | Extra.has_any(Extra.INFINITE_TORPEDOS, Extra.DEFLECT_BOLTS),
            ),
            pickup_name="m_pup1",
        ),
        "First TIE Gate Behind Rock Minikit": minikit_data(
            R_FIRST_AREA_BEHIND_TIE_GATE,
            logic_options(
                base=True_(),
                # I could not get Torpedoes to hit the rock.
                hard=HasAbility(VEHICLE_BLASTER) | Extra.DEFLECT_BOLTS.has(),
            ),
            pickup_name="m_pup2",
        ),
        "First Area Trip AT-STs Minikit": minikit_data(
            R_SPAWN,
            HasAbility(VEHICLE_TOW),
            pickup_name="m_pup3",
        ),
        "Rescue Rebels In Cave Minikit": minikit_data(
            R_FIRST_AREA_TIE_GATE_CAVE,
            logic_options(
                # If you can get here, you must have VEHICLE_BLASTER since all VEHICLE_TIE and VEHICLE_TOW have
                # VEHICLE_BLASTER.
                base=True_(),
                # Torpedoes can destroy the AT-STs and the Minikit, but I could not get torpedoes to destroy the Speeder
                # Bikes.
                # Deflect Bolts can be used to destroy the AT-STs and the Speeder Bikes, but the minikit only spawns
                # when they have all been destroyed, so there is then no enemies to use to deflect bolts into the
                # minikit.
                hard=HasAbility(VEHICLE_BLASTER) | (Extra.has_all(Extra.DEFLECT_BOLTS, Extra.INFINITE_TORPEDOS)),
            ),
            pickup_name="m_pup4",
        ),
        "Second Area Trip AT-STs Minikit": minikit_data(
            R_SECOND_AREA_SPAWN,
            pickup_name="m_pup7",
        ),
        "Second Area Minikit Right Of Last Wall": minikit_data(
            R_SECOND_AREA_SPAWN,
            pickup_name="m_pup8",
        ),
        "Second TIE Gate Cave Minikit": minikit_data(
            R_SECOND_AREA_BEHIND_TIE_GATE,
            pickup_name="m_pup5",
        ),
        "Second TIE Gate Rock After Cave Minikit": minikit_data(
            R_SECOND_AREA_BEHIND_TIE_GATE,
            pickup_name="m_pup6",
        ),
        "Final Battle Behind Rock Minikit 1": minikit_data(
            R_FINAL_BATTLE,
            pickup_name="m_pup9",
        ),
        "Final Battle Behind Rock Minikit 2": minikit_data(
            R_FINAL_BATTLE,
            pickup_name="m_pup10",
        ),
    },
    power_brick=LocationData(R_SECOND_AREA_BEHIND_TIE_GATE),
)

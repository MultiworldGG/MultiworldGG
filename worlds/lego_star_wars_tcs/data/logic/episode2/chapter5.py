from rule_builder.rules import True_, Or, HasFromListUnique

from ..macros import HAS_VEHICLE_LEVEL_CHARACTER_SWAPPING
from ..option_filters import logic_options
from ..rules import HasAbility
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_BEHIND_FIRST_FORCE_FIELD = "Behind First Force Field"
R_CONTROL_SHIP_BATTLE = "Control Ship Battle"
R_CONTROL_SHIP_BATTLE_MINIKITS = "Control Ship Battle Minikits"

GUNSHIP_CAVALRY = Chapter(
    area=Area.GUNSHIP,
    start_region=R_SPAWN,
    extra_entrance_rules=HasAbility(IS_A_VEHICLE),
    regions={
        R_SPAWN: (
            ExitData(
                R_BEHIND_FIRST_FORCE_FIELD,
                logic_options(
                    base=HasAbility(VEHICLE_TOW),
                    # While flying around the force field (and invisible wall), spam character swaps to maintain height
                    # and avoid falling into the kill plane.
                    # This maybe could maybe be moved to Moderate logic.
                    hard=Or(
                        HasAbility(VEHICLE_TOW),
                        HAS_VEHICLE_LEVEL_CHARACTER_SWAPPING,
                    )
                ),
            ),
        ),
        R_BEHIND_FIRST_FORCE_FIELD: (
            ExitData(
                R_CONTROL_SHIP_BATTLE,
                # If you can get through/around the first force field, you can also get through/around the second one.
                True_(),
                er_rule=logic_options(
                    base=HasAbility(VEHICLE_TOW),
                    hard=Or(
                        HasAbility(VEHICLE_TOW),
                        HAS_VEHICLE_LEVEL_CHARACTER_SWAPPING,
                    )
                ),
                new_level=Level.GUNSHIP_B,
            ),
        ),
        R_CONTROL_SHIP_BATTLE: (
            ExitData(
                R_CONTROL_SHIP_BATTLE_MINIKITS,
                logic_options(
                    # VEHICLE_TOW required to reach here.
                    base=True_(),
                    # Unlike the minikits in the first level, these minikits cannot be collected by ramming into them.
                    hard=Or(
                        HasAbility(VEHICLE_BLASTER),
                        # Deflect enemy blaster fire into the minikits.
                        Extra.DEFLECT_BOLTS.has(),
                        # Infinite Torpedos [sic] does not work in this level.
                        # Extra.INFINITE_TORPEDOS.has(),
                    )
                ),
            ),
            ExitData(
                "Chapter Completion",
                # TOW is strictly required, there is no way to skip this at all.
                HasAbility(VEHICLE_TOW),
            ),
        ),
        R_CONTROL_SHIP_BATTLE_MINIKITS: (),
    },
    minikits={
        # The only vehicles that cannot shoot minikits are pod racers, which fly low enough to the ground to collect the
        # minikits by ramming into them.
        "Freestanding Minikit Before Lasers": minikit_data(
            R_SPAWN,
            pickup_name="m_pup1",
        ),
        "Freestanding Minikit After Fourth Laser": minikit_data(
            R_SPAWN,
            pickup_name="m_pup2",
        ),
        "TIE Area Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=HasAbility(VEHICLE_TIE),
                # TIE vehicles can access as normal.
                #
                # For other vehicles use the Loop and P2 drop-in trick:
                # For larger vehicles:
                # Approach the gate from the north and input a loop while moving south parallel to the TIE gate.
                # Drop in P2 at the top of the loop, and have P2 move immediately to the left to get on top of and
                # over the TIE gate. Some vehicles will pretty much spawn on top of the cliff, trivialising the
                # trick.
                # A few of the larger vehicles can clear the gate doing this on their own, even without a drop-in
                # because the cliff face north of the TIE gate tends to push the player to the left as they loop
                # into it.
                #
                # For smaller vehicles:
                # Approach the gate from the south and allow the vehicle to freely travel north along the gate. Upon
                # reaching the top of the gate, the vehicle will automatically turn to the right. Input a loop here,
                # and drop-in P2 at the apex of the loop. P2 should spawn in, and then P1 will push P2 over the TIE
                # gate.
                # Sometimes, P1 will get over the gate on their own even without the P2 drop-in, but it does not seem
                # very consistent.
                #
                # Can use either method (method for smaller vehicles is easier though):
                # - Anakin's Pod
                # - Snowspeeder
                #
                # Use method for larger vehicles (can also get over on its own pretty consistently):
                # - Naboo Starfighter
                # - X-wing
                # - Y-wing (might not be able to get back out on its own)
                #
                # Use method for larger vehicles:
                # - Millennium Falcon
                # - Imperial Shuttle
                # - Slave 1
                # - Clone Arcfighter
                #
                # Use method for smaller vehicles:
                # - Anakin's Speeder
                # - Republic Gunship
                # - Sebulba's Pod
                # - Zam's Airspeeder
                # - Droid Trifighter
                # - Vulture Droid
                hard=True_(),
            ),
            pickup_name="m_pup3",
        ),
        "Freestanding Minikit After First Force Field": minikit_data(
            R_BEHIND_FIRST_FORCE_FIELD,
            pickup_name="m_pup4",
        ),
        "Minikit Behind Yellow Wall": minikit_data(
            R_BEHIND_FIRST_FORCE_FIELD,
            # Every logic difficulty either requires VEHICLE_TOW to reach here, or can skip both the VEHICLE_TOW to
            # reach here, and the VEHICLE_TOW to reach this minikit.
            True_(),
            er_rule=logic_options(
                base=HasAbility(VEHICLE_TOW),
                # Every vehicle can get over this will using the loop + drop in P2 method. Anakin's and Zam's Speeders
                # are probably the most difficult.
                hard=True_(),
            ),
            pickup_name="m_pup5",
        ),
        "Control Ship Battle Minikit 1": minikit_data(
            R_CONTROL_SHIP_BATTLE_MINIKITS,
            pickup_name="m_pup1",
        ),
        "Control Ship Battle Minikit 2": minikit_data(
            R_CONTROL_SHIP_BATTLE_MINIKITS,
            pickup_name="m_pup2",
        ),
        "Control Ship Battle Minikit 3": minikit_data(
            R_CONTROL_SHIP_BATTLE_MINIKITS,
            pickup_name="m_pup3",
        ),
        "Control Ship Battle Minikit 4": minikit_data(
            R_CONTROL_SHIP_BATTLE_MINIKITS,
            pickup_name="m_pup4",
        ),
        "Control Ship Battle Minikit 5": minikit_data(
            R_CONTROL_SHIP_BATTLE_MINIKITS,
            pickup_name="m_pup5",
        ),
    },
    power_brick=LocationData(R_BEHIND_FIRST_FORCE_FIELD),
)

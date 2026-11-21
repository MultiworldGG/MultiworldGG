from rule_builder.options import OptionFilter
from rule_builder.rules import True_

from ..option_filters import logic_options, ut_glitched_rule
from ..rules import HasAbility
from ..types import minikit_data, ExitData, Chapter, LocationData, MinikitData

from ...areas import Area
from ...extras import Extra
from ...levels import Level

from ....character_ability import *
from ....options import LogicExpectNonInfiniteTorpedoesPodRacer21

R_SPAWN = "Spawn"
R_FIRST_FORCEFIELD_TRAP = "First Forcefield Trap"
R_AFTER_FIRST_FORCEFIELD_TRAP = "After First Forcefield Trap"
R_SECOND_FORCEFIELD_TRAP = "Second Forcefield Trap"

# Either Infinite Torpedos [sic] is unlocked, or the player enabled gathering torpedoes within the level.
CAN_DESTROY_OBJECTS_WITH_POD_RACERS = ut_glitched_rule(
    normal_rule=Extra.INFINITE_TORPEDOS.has() | OptionFilter(LogicExpectNonInfiniteTorpedoesPodRacer21, True),
    glitched_rule=True_(),
)
CAN_SHOOT_ALLOW_TORPEDOES = HasAbility(VEHICLE_BLASTER) | CAN_DESTROY_OBJECTS_WITH_POD_RACERS

BOUNTY_HUNTER_PURSUIT = Chapter(
    area=Area.PURSUIT,
    start_region=R_SPAWN,
    extra_entrance_rules=HasAbility(IS_A_VEHICLE),
    regions={
        R_SPAWN: (
            ExitData(R_FIRST_FORCEFIELD_TRAP, new_level=Level.PURSUIT_B),
        ),
        R_FIRST_FORCEFIELD_TRAP: (
            ExitData(R_AFTER_FIRST_FORCEFIELD_TRAP, new_level=Level.PURSUIT_C),
        ),
        R_AFTER_FIRST_FORCEFIELD_TRAP: (
            ExitData(R_SECOND_FORCEFIELD_TRAP, new_level=Level.PURSUIT_D),
        ),
        R_SECOND_FORCEFIELD_TRAP: (
            # Logically, pursuit_e is skipped because that is just the boss battle itself.
            ExitData(
                "Chapter Completion",
                HasAbility(VEHICLE_BLASTER),
            ),
        ),
    },
    minikits={
        "Destroy First Turrets Minikit": MinikitData(
            R_SPAWN,
            logic_options(
                base=HasAbility(VEHICLE_BLASTER),
                normal=CAN_SHOOT_ALLOW_TORPEDOES,
            ),
            pickup_names=("TKIT1", "TKIT2", "TKIT3", "TKIT4", "TKIT5")
        ),
        "Torpedo Spires Minikit": MinikitData(
            R_SPAWN,
            # These are awful to target. It would be nice to require Infinite Torpedos [sic] on the lowest logic
            # difficulty, but the lowest logic difficulty specifically avoids including Extras in logic.
            pickup_names=("SPIRES1", "SPIRES2", "SPIRES3", "SPIRES4", "SPIRES5")
        ),
        "Traffic Light Minikit": minikit_data(
            R_SPAWN,
            logic_options(
                base=HasAbility(VEHICLE_BLASTER),
                normal=CAN_SHOOT_ALLOW_TORPEDOES,
            ),
            pickup_name="JJ_KIT",
        ),
        "First TIE Gate Minikit": minikit_data(
            R_SPAWN,
            HasAbility(VEHICLE_TIE),
            pickup_name="MINTIE"
        ),
        "Cylinder Advertisements Minikit": MinikitData(
            R_AFTER_FIRST_FORCEFIELD_TRAP,
            # Some of these objects are particularly difficult to target with torpedoes, potentially needing a direct
            # shot in one case, so normal logic does not consider using torpedoes, and moderate logic always expects
            # Infinite Torpedos [sic] if using torpedoes.
            # ER Note: Needs `CanReachRegion("Bounty Hunter Pursuit - Spawn") &`
            logic_options(
                base=HasAbility(VEHICLE_BLASTER),
                moderate=HasAbility(VEHICLE_BLASTER) | Extra.INFINITE_TORPEDOS.has(),
                hard=CAN_SHOOT_ALLOW_TORPEDOES,
            ),
            pickup_names=(
                # In R_SPAWN.
                "m_1A",
                "m_1",
                "m_2",
                "m_3",
                "m_4",
                "m_5",
                # In R_AFTER_FIRST_FORCEFIELD_TRAP.
                "m_15",
                "m_14",
                "m_13",
                "m_11",
            )
        ),
        "First Forcefield Trap Minikit": minikit_data(
            R_FIRST_FORCEFIELD_TRAP,
            HasAbility(VEHICLE_BLASTER),
            pickup_name="mK",
        ),
        "Second TIE Gate Minikit": minikit_data(
            R_AFTER_FIRST_FORCEFIELD_TRAP,
            HasAbility(VEHICLE_TIE),
            pickup_name="TIEMIN",
        ),
        "Triple Triangle Sign Minikit": minikit_data(
            R_AFTER_FIRST_FORCEFIELD_TRAP,
            # Cannot be hit with torpedoes.
            HasAbility(VEHICLE_BLASTER),
            pickup_name="TRI_KIT",
        ),
        "Destroy Second Turrets Minikit": MinikitData(
            R_AFTER_FIRST_FORCEFIELD_TRAP,
            logic_options(
                base=HasAbility(VEHICLE_BLASTER),
                normal=CAN_SHOOT_ALLOW_TORPEDOES,
            ),
            pickup_names=("TKIT1", "TKIT2", "TKIT3", "TKIT4", "TKIT5")
        ),
        "Second Forcefield Trap Minikit": minikit_data(
            R_SECOND_FORCEFIELD_TRAP,
            HasAbility(VEHICLE_BLASTER),
            pickup_name="mK1",
        )
    },
    power_brick=LocationData(R_AFTER_FIRST_FORCEFIELD_TRAP, HasAbility(VEHICLE_BLASTER))
)

# This is one of the only Minikits in the entire game that is split across multiple levels.
BOUNTY_HUNTER_PURSUIT.level_minikits[Level.PURSUIT_A]["Cylinder Advertisements Minikit"] \
    = BOUNTY_HUNTER_PURSUIT.minikits["Cylinder Advertisements Minikit"]

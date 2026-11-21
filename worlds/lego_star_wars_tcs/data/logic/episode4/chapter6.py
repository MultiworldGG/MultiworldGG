from rule_builder.rules import False_, True_

from ..option_filters import logic_options
from ..rules import (
    HasAbility,
    HasAllAbilities,
)
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area
from ...extras import Extra
from ...levels import Level

from ....character_ability import *

R_SPAWN = "Spawn"
R_AFTER_SECOND_FORCE_FIELD = "After Second Force Field"
R_AFTER_THIRD_FORCE_FIELD = "After Third Force Field"
R_TRENCH_RUN_AND_EXHAUST_PORT = "Trench Run, and Exhaust Port"


# Maybe this could be in Moderate logic, but it kind of sucks due to RNG and how long it can take, so it's going in Hard
# logic.
_CAN_DEFLECT_BOLTS_TO_DESTROY_THINGS = logic_options(
    base=False_(),
    hard=Extra.DEFLECT_BOLTS.has(),
)

REBEL_ATTACK = Chapter(
    area=Area.DEATHSTARBATTLE,
    start_region=R_SPAWN,
    extra_entrance_rules=HasAbility(IS_A_VEHICLE),
    regions={
        R_SPAWN: (
            ExitData(
                R_AFTER_SECOND_FORCE_FIELD,
                logic_options(
                    # Expect a blaster vehicle beyond this point.
                    base=HasAbility(VEHICLE_BLASTER),
                    # Just shoot a torpedo at the wall after lowering the force field.
                    normal=True_(),
                ),
                new_level=Level.DEATHSTARBATTLE_B,
            ),
        ),
        R_AFTER_SECOND_FORCE_FIELD: (
            ExitData(
                R_AFTER_THIRD_FORCE_FIELD,
                # Base logic expects a blaster vehicle, and normal logic is expected to shoot these walls with
                # torpedoes.
                # todo: Maybe Normal logic should expect a blaster vehicle at some point?
                #  Or normal logic could expect either a Blaster Vehicle or one out of Invincibility, Deflect Bolts,
                #  Regenerate Hearts, for survivability purposes.
                new_level=Level.DEATHSTARBATTLE_C,
            ),
        ),
        R_AFTER_THIRD_FORCE_FIELD: (
            ExitData(
                R_TRENCH_RUN_AND_EXHAUST_PORT,
                new_level=Level.DEATHSTARBATTLE_D,
            ),
        ),
        R_TRENCH_RUN_AND_EXHAUST_PORT: (
            ExitData(
                "Chapter Completion",
                logic_options(
                    base=True_(),
                    # The turrets have to be destroyed to lower the force field over the exhaust port.
                    normal=HasAbility(VEHICLE_BLASTER),
                    # It is pretty easy to hover directly over a turret to use Deflect Bolts to destroy that turret.
                    moderate=HasAbility(VEHICLE_BLASTER) | Extra.DEFLECT_BOLTS.has(),
                )
            ),
        ),
    },
    minikits={
        "First Spinner Minikit": minikit_data(
            R_SPAWN,
            HasAbility(VEHICLE_BLASTER) | _CAN_DEFLECT_BOLTS_TO_DESTROY_THINGS,
            pickup_name="m_pup1",
        ),
        "First Hidden Alcove Minikit": minikit_data(
            R_SPAWN,
            HasAbility(VEHICLE_BLASTER) | _CAN_DEFLECT_BOLTS_TO_DESTROY_THINGS,
            pickup_name="m_pup2",
        ),
        "First TIE Gate Minikit": minikit_data(
            R_SPAWN,
            # The typical TIE gate skip of dropping in P2 at the top of P1's loop doesn't seem to work here. There are
            # out-of-bounds tricks in this level (seems to require Clone Arcfighter), but I could not get them to work.
            HasAbility(VEHICLE_TIE),
            pickup_name="m_pup3",
        ),
        "Second Spinner Minikit By Second TIE Gate": minikit_data(
            R_AFTER_SECOND_FORCE_FIELD,
            logic_options(
                # Base logic expects a VEHICLE_BLASTER to get here.
                base=True_(),
                # Normal logic can get here by shooting a torpedo at the wall.
                normal=HasAbility(VEHICLE_BLASTER) | _CAN_DEFLECT_BOLTS_TO_DESTROY_THINGS,
            ),
            pickup_name="m_pup4",
        ),
        "Second TIE Gate Green Tiles Minikit": minikit_data(
            R_AFTER_SECOND_FORCE_FIELD,
            HasAbility(VEHICLE_TIE),
            pickup_name="m_pup5",
        ),
        "Second Hidden Alcove Minikit": minikit_data(
            R_AFTER_SECOND_FORCE_FIELD,
            logic_options(
                # Base logic expects a VEHICLE_BLASTER to get here.
                base=True_(),
                # Expect VEHICLE_BLASTER for Normal logic.
                normal=HasAbility(VEHICLE_BLASTER),
                # Just use torpedoes instead.
                moderate=True_(),
            ),
            pickup_name="m_pup6",
        ),
        "Third TIE Gate Behind Force Field Minikit": minikit_data(
            R_AFTER_SECOND_FORCE_FIELD,
            # The minikit is not interactable until the force field has been taken down with bombs.
            HasAllAbilities(VEHICLE_TIE | VEHICLE_TOW),
            pickup_name="m_pup7",
        ),
        "Third Spinner Minikit": minikit_data(
            R_AFTER_THIRD_FORCE_FIELD,
            logic_options(
                # Base logic expects a VEHICLE_BLASTER to get here.
                base=True_(),
                # Normal logic can get here by shooting a torpedo at the wall.
                normal=HasAbility(VEHICLE_BLASTER) | _CAN_DEFLECT_BOLTS_TO_DESTROY_THINGS,
            ),
            pickup_name="m_pup8",
        ),
        "Third Alcove Minikit Before Trench Run": minikit_data(
            R_AFTER_THIRD_FORCE_FIELD,
            logic_options(
                # Base logic expects a VEHICLE_BLASTER to get here.
                base=True_(),
                # Unlike the previous alcove, torpedoes seem to be extremely difficult to use to access this minikit,
                # and I couldn't get Deflect Bolts to work, so a blaster vehicle is always expected. It should be noted
                # that using Torpedoes is possible, so maybe Hard logic could logically allow Infinite Torpedos here,
                # but it's still extremely difficult to get the torpedoes to hit the objects and gain access to the
                # minikit.
                normal=HasAbility(VEHICLE_BLASTER),
            ),
            pickup_name="m_pup9",
        ),
        "Fourth Spinner Minikit By Exhaust Port": minikit_data(
            R_TRENCH_RUN_AND_EXHAUST_PORT,
            logic_options(
                base=True_(),
                # There are no respawning enemy TIE fighters here, and the turbolaser bolts seem to be difficult, or
                # maybe impossible, to deflect into the spinner, so VEHICLE_BLASTER is always expected.
                normal=HasAbility(VEHICLE_BLASTER),
            ),
            pickup_name="m_pup10",
        ),
    },
    power_brick=LocationData(
        R_TRENCH_RUN_AND_EXHAUST_PORT,
    ),
)

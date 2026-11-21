from ..rules import HasAbility
from ..types import minikit_data, ExitData, Chapter, LocationData

from ...areas import Area

from ....character_ability import VEHICLE_TIE, IS_A_VEHICLE

NAME = "Mos Espa Pod Race"

R_RACETRACK = "Racetrack"

MOS_ESPA_POD_RACE = Chapter(
    area=Area.PODSPRINT,
    start_region=R_RACETRACK,
    extra_entrance_rules=HasAbility(IS_A_VEHICLE),
    regions={
        R_RACETRACK: (
            ExitData("Chapter Completion"),
        ),
    },
    minikits={
        "TIE Service Ramp Minikit": minikit_data(
            R_RACETRACK,
            # todo: I'm pretty sure it is possible to clip through the TIE gate, or to squeeze behind it on the left,
            #  using character swapping.
            HasAbility(VEHICLE_TIE),
            pickup_name="m_pup3"
        ),
        "Cave Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup4"
        ),
        "Tusken Canyon Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup5"
        ),
        "Corner After Tusken Canyon Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup6"
        ),
        "Beneath Rock Arches Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup7"
        ),
        "After Rock Arches Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup8",
        ),
        "Finish Straight Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup9"
        ),
        "Before Finish Line Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup10"
        ),
        "Lap 2 Center Path Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup1"
        ),
        "Lap 3 End Of Right Path Minikit": minikit_data(
            R_RACETRACK,
            pickup_name="m_pup2"
        ),
    },
    power_brick=LocationData(
        R_RACETRACK,
    ),
)

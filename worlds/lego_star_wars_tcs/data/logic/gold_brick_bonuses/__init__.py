from .indy_trailer import INDY_TRAILER
from .pod_race_original import POD_RACE_ORIGINAL
from .anakins_flight import ANAKINS_FLIGHT
from .gunship_cavalry_original import GUNSHIP_CAVALRY_ORIGINAL
from .a_new_hope import A_NEW_HOPE
from .lego_city import LEGO_CITY
from .new_town import NEW_TOWN
from ..types import GoldBrickBonus
from ...areas import Area

__all__ = [
    "GOLD_BRICK_BONUSES",
    "AREA_TO_GOLD_BRICK_BONUS",
]

GOLD_BRICK_BONUSES: tuple[GoldBrickBonus, ...] = (
    INDY_TRAILER,
    POD_RACE_ORIGINAL,
    ANAKINS_FLIGHT,
    GUNSHIP_CAVALRY_ORIGINAL,
    A_NEW_HOPE,
    LEGO_CITY,
    NEW_TOWN,
)

AREA_TO_GOLD_BRICK_BONUS: dict[Area, GoldBrickBonus] = {bonus.area: bonus for bonus in GOLD_BRICK_BONUSES}

from ..types import GoldBrickBonus, ExitData
from ...areas import Area

INDY_TRAILER = GoldBrickBonus(
    area=Area.LOSTTEMPLE,
    start_region="Watch the trailer",
    regions={"Watch the trailer": (ExitData(GoldBrickBonus.COMPLETION_REGION_NAME),)},
    gold_brick_requirement=0,
)

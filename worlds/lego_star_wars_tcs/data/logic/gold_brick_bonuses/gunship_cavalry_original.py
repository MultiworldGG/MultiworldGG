from ..types import GoldBrickBonus, ExitData
from ...areas import Area
from ...levels import Level

GUNSHIP_CAVALRY_ORIGINAL = GoldBrickBonus(
    area=Area.BONUS_GUNSHIP,
    start_region="Spawn",
    # The level only has Story mode, so logic rules are not needed.
    regions={
        "Spawn": (
            ExitData("Versus Control Ship", new_level=Level.BONUS_GUNSHIP_B),
        ),
        "Versus Control Ship": (
            ExitData(GoldBrickBonus.COMPLETION_REGION_NAME),
        )
    },
    gold_brick_requirement=10,
)

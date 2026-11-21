from ..types import GoldBrickBonus, ExitData
from ...areas import Area
from ...levels import Level

POD_RACE_ORIGINAL = GoldBrickBonus(
    area=Area.PODRACE,
    start_region="Starting Line",
    # Technically there are 3 laps, so regions for the other laps could be added, but they are unlikely to be needed for
    # logic in the near future.
    # The level only has Story mode, so logic rules are not needed.
    regions={
        "Starting Line": (
            ExitData("Tusken Pass", new_level=Level.PODRACE_C),
        ),
        "Tusken Pass": (
            ExitData("Finish Straight", new_level=Level.PODRACE_A),
        ),
        "Finish Straight": (
            ExitData(GoldBrickBonus.COMPLETION_REGION_NAME),
        )
    },
    gold_brick_requirement=10,
)

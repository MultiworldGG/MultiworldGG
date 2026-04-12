from .sms_region_helper import *

# Delfino Airstrip
DELFINO_AIRSTRIP: SmsRegion = SmsRegion(
    SmsRegionName.AIRSTRIP,
    shines=[
        Shine(
            "Delfino Airstrip Dilemma",
            requirements=[Requirements(SPRAY_OR_HOVER, skip_forward=False)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO, skip_forward=False)],
            in_game_bit=86,
        ),
        Shine(
            "Red Coin Waterworks",
            [Requirements([[NozzleType.turbo]], corona=True)],
            in_game_bit=88,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Ice Cube",
            requirements=[
                Requirements(TURBO_AND_SPRAY_OR_TURBO_AND_HOVER, corona=True)
            ],
            hard=[Requirements([[NozzleType.turbo]], corona=True)],
            in_game_bit=120,
        )
    ],
    parent_region="Menu",
)
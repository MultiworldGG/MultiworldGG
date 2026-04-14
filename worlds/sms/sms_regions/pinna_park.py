from .sms_region_helper import *

PINNA_PARK_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_ENTRANCE,
    requirements=[Requirements(shines=10)],
    hard=[],
    advanced=[],
    tears=[],
    ticketed="Pinna Park Ticket",
    parent_region=SmsRegionName.PLAZA,
)

PINNA_PARK_ONE: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_ONE,
    shines=[
        Shine(
            "Mecha-Bowser Appears!",
            [Requirements([[NozzleType.spray]])],
            in_game_bit=30,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Tree Sand Shine",
            requirements=[Requirements(ANY_SPLASHER)],
            advanced=[Requirements(ANY_SPLASHER_OR_TURBO)],
            in_game_bit=348,
        ),
        BlueCoin(
            "Cannon Sand Shine",
            requirements=[Requirements(ANY_SPLASHER)],
            advanced=[Requirements(ANY_SPLASHER_OR_TURBO)],
            in_game_bit=349,
        ),
        BlueCoin(
            "Orange Wall M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=320,
        ),
        BlueCoin(
            "Sand M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=321,
        ),
        BlueCoin(
            "Green Clam",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=322,
        ),
        BlueCoin(
            "Left O",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=323,
        ),
        BlueCoin(
            "Entrance Bird",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=324,
        ),
        BlueCoin(
            "Pineapple Bird",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=325,
        ),
        BlueCoin(
            "Ship Peak",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=326,
        ),
        BlueCoin(
            "Cage Platform",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=327,
        ),
        BlueCoin(
            "Right O",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=328,
        ),
        BlueCoin(
            "White Wall X",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=329,
        ),
        BlueCoin(
            "Tree X",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=330,
        ),
        BlueCoin(
            "Ferris M",
            [
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=331,
        ),
        BlueCoin(
            "Banana Triangle",
            requirements=[
                Requirements(SPRAY_AND_HOVER),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=332,
        ),
        BlueCoin(
            "Ferris Triangle",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=333,
        ),
        BlueCoin(
            "Stairs",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=334,
        ),
        BlueCoin(
            "Girder",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=336,
        ),
        BlueCoin("Coaster Ledge", in_game_bit=337),
        BlueCoin(
            "Cage",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=338,
        ),
        BlueCoin(
            "Stackin Stus",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel",
                ),
            ],
            in_game_bit=339,
        ),
        BlueCoin(
            "Beach Butterfly A", [Requirements([[NozzleType.yoshi]])], in_game_bit=343
        ),
        BlueCoin(
            "Beach Butterfly B", [Requirements([[NozzleType.yoshi]])], in_game_bit=344
        ),
    ],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_TWO: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_TWO,
    requirements=[
        Requirements(location=f"{SmsRegionName.PINNA_ONE} - Mecha-Bowser Appears!")
    ],
    shines=[
        Shine(
            "The Beach Cannon's Secret",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=31,
        ),
        Shine(
            "Red Coins in the Cannon",
            requirements=[
                Requirements(
                    SPRAY_OR_HOVER,
                    location=f"{SmsRegionName.PINNA_TWO} - The Beach Cannon's Secret",
                )
            ],
            hard=[
                Requirements(
                    location=f"{SmsRegionName.PINNA_TWO} - The Beach Cannon's Secret",
                )
            ],
            in_game_bit=38,
        ),
        Shine(
            "100 Coins",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            tears=[Requirements(manual_none=True)],
            hundred=True,
            in_game_bit=103,
        ),
    ],
    blue_coins=[
        BlueCoin("Spawn Basket", in_game_bit=340),
        BlueCoin("Flower Basket", in_game_bit=341),
        BlueCoin("Gate Basket", in_game_bit=342),
        BlueCoin("Rock Basket", in_game_bit=345),
        BlueCoin("Middle Basket", in_game_bit=346),
        BlueCoin("Sunflower Basket", in_game_bit=347),
    ],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_THREE: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_THREE,
    requirements=[
        Requirements(location=f"{SmsRegionName.PINNA_TWO} - The Beach Cannon's Secret")
    ],
    shines=[
        Shine(
            "Red Coins of the Pirate Ships",
            requirements=[
                Requirements(
                    [[NozzleType.hover]],
                    location=f"{SmsRegionName.PINNA_TWO} - The Beach Cannon's Secret",
                )
            ],
            hard=[
                Requirements(
                    manual_none=True,
                    location=f"{SmsRegionName.PINNA_TWO} - The Beach Cannon's Secret",
                )
            ],
            in_game_bit=32,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_FOUR,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.PINNA_THREE} - Red Coins of the Pirate Ships"
        )
    ],
    shines=[
        Shine(
            "The Wilted Sunflowers",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements([[NozzleType.turbo]])],
            in_game_bit=33,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.PINNA_FOUR} - The Wilted Sunflowers")
    ],
    shines=[
        Shine(
            "The Runaway Ferris Wheel",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=34,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_SIX: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_SIX,
    requirements=[
        Requirements(location=f"{SmsRegionName.PINNA_FIVE} - The Runaway Ferris Wheel")
    ],
    shines=[
        Shine(
            "The Yoshi-Go-Round's Secret",
            [Requirements([[NozzleType.yoshi]])],
            in_game_bit=35,
        ),
        Shine(
            "Red Coins in the Yoshi-Go-Round",
            requirements=[Requirements(YOSHI_AND_HOVER)],
            hard=[Requirements([[NozzleType.yoshi]])],
            in_game_bit=39,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Park Butterfly", [Requirements([[NozzleType.yoshi]])], in_game_bit=335
        )
    ],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_SEVEN,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.PINNA_SIX} - The Yoshi-Go-Round's Secret"
        )
    ],
    shines=[
        Shine(
            "Shadow Mario in the Park",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=36,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

PINNA_PARK_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.PINNA_EIGHT,
    requirements=[
        Requirements(location=f"{SmsRegionName.PINNA_SEVEN} - Shadow Mario in the Park")
    ],
    shines=[
        Shine(
            "Roller Coaster Balloons",
            [Requirements([[NozzleType.spray]])],
            in_game_bit=37,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PINNA_ENTRANCE,
)

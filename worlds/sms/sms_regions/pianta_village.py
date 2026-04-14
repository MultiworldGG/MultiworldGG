from .sms_region_helper import *

# Pianta Village
PIANTA_VILLAGE_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_ENTRANCE,
    requirements=[Requirements([[NozzleType.rocket]])],
    hard=[Requirements([[NozzleType.rocket]]), Requirements([[NozzleType.yoshi]], shines=5),
        Requirements([[NozzleType.yoshi]], skip_forward=True)],
    advanced=[Requirements([[NozzleType.rocket]]), Requirements([[NozzleType.yoshi]], shines=5),
        Requirements([[NozzleType.yoshi]], skip_forward=True), Requirements([[NozzleType.hover]])],
    tears=[Requirements()],
    ticketed="Pianta Village Ticket",
    parent_region=SmsRegionName.PLAZA,
)

PIANTA_VILLAGE_ONE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_ONE,
    shines=[
        Shine(
            "Chain Chomplets Unchained",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=60,
        ),
        Shine("100 Coins", hundred=True, in_game_bit=106),
    ],
    blue_coins=[
        BlueCoin("River End", in_game_bit=432),
        BlueCoin("Grass", in_game_bit=433),
        BlueCoin(
            "Back Tree",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=434,
        ),
        BlueCoin("River Bridge", in_game_bit=435),
        BlueCoin(
            "Left Tree",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=438,
        ),
        BlueCoin(
            "Waterfall",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=439,
        ),
        BlueCoin(
            "Wall Triangle",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            in_game_bit=443,
        ),
        BlueCoin(
            "Hot Tub Triangle",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            in_game_bit=444,
        ),
        BlueCoin(
            "Left M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            in_game_bit=445,
        ),
        BlueCoin(
            "Right M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            in_game_bit=446,
        ),
        BlueCoin(
            "Spawn M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            in_game_bit=447,
        ),
        BlueCoin("Underside M", [Requirements(SPRAY_AND_HOVER)], in_game_bit=448),
        BlueCoin(
            "Moon",
            requirements=[Requirements(SPROVER_OR_SPROCKET)],
            hard=[
                Requirements(SPRAY_AND_ANY_FLUDD),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            tears=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside",
                ),
            ],
            in_game_bit=420,
        ),
        BlueCoin("Statue's Nose", in_game_bit=429),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_TWO: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_TWO,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_ONE} - Chain Chomplets Unchained")
    ],
    shines=[
        Shine(
            "Il Piantissimo's Crazy Climb",
            [Requirements(manual_none=True)],
            in_game_bit=65,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Sign",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=431,
        )
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_THREE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_THREE,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.PIANTA_TWO} - Il Piantissimo's Crazy Climb"
        )
    ],
    shines=[
        Shine(
            "The Goopy Inferno",
            requirements=[Requirements(SPROCKET_OR_HOVER)],
            hard=[Requirements(SPROCKET_OR_HOVER_OR_TURBO)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=62,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Giant M",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=430,
        ),
        BlueCoin(
            "Burning Pianta",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=442,
        ),
        BlueCoin("FLUDD M", [Requirements([[NozzleType.spray]])], in_game_bit=449),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_FOUR,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_THREE} - The Goopy Inferno")
    ],
    shines=[
        Shine(
            "Chain Chomp's Bath",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=61,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_FOUR} - Chain Chomp's Bath")
    ],
    shines=[
        Shine(
            "Secret of the Village Underside",
            requirements=[Requirements([[NozzleType.yoshi]])],
            advanced=[Requirements(HOVER_OR_YOSHI)],
            in_game_bit=64,
        ),
        Shine(
            "Red Coin Chucksters",
            requirements=[Requirements(YOSHI_AND_HOVER)],
            advanced=[Requirements([[NozzleType.hover]])],
            tears=[Requirements(HOVER_OR_YOSHI)],
            in_game_bit=68,
        ),
    ],
    blue_coins=[
        BlueCoin("Back Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=436),
        BlueCoin(
            "Front Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=437
        ),
        BlueCoin("Butterflies", [Requirements([[NozzleType.yoshi]])], in_game_bit=440),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_SIX: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_SIX,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside"
        )
    ],
    shines=[
        Shine(
            "Piantas in Need",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=63,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Pianta in Need A",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=421,
        ),
        BlueCoin(
            "Pianta in Need B",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=422,
        ),
        BlueCoin(
            "Pianta in Need C",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=423,
        ),
        BlueCoin(
            "Pianta in Need D",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=424,
        ),
        BlueCoin(
            "Pianta in Need E",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=425,
        ),
        BlueCoin(
            "Pianta in Need F",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=426,
        ),
        BlueCoin(
            "Pianta in Need G",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=427,
        ),
        BlueCoin(
            "Pianta in Need H",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=428,
        ),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_SEVEN,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_SIX} - Piantas in Need")
    ],
    shines=[
        Shine(
            "Shadow Mario Runs Wild",
            requirements=[
                Requirements(
                    [[NozzleType.spray]],
                )
            ],
            advanced=[
                Requirements(
                    SPRAY_OR_HOVER,
                )
            ],
            in_game_bit=66,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_EIGHT,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_SEVEN} - Shadow Mario Runs Wild")
    ],
    shines=[
        Shine(
            "Fluff Festival Coin Hunt",
            requirements=[
                Requirements(
                    ROCKET_OR_HOVER,
                    location=f"{SmsRegionName.PIANTA_SEVEN} - Shadow Mario Runs Wild",
                )
            ],
            advanced=[
                Requirements(
                    ROCKET_OR_HOVER_OR_TURBO,
                    location=f"{SmsRegionName.PIANTA_SEVEN} - Shadow Mario Runs Wild",
                )
            ],
            in_game_bit=67,
        ),
        Shine(
            "Soak the Sun",
            requirements=[Requirements(SPROCKET_OR_SPROVER)],
            hard=[Requirements(SPRAY_AND_OTHER_FLUDD)],
            in_game_bit=69,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Bird",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            tears=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=441,
        )
    ],
    nozzle_boxes=[
        NozzleBox(
            "Rocket Box",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=882,
        )
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

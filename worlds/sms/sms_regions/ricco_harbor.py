from .sms_region_helper import *

RICCO_HARBOR_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_ENTRANCE,
    requirements=[
        Requirements(ANY_SPLASHER, shines=3),
    ],
    ticketed="Ricco Harbor Ticket",
    parent_region=SmsRegionName.PLAZA,
)

RICCO_HARBOR_ONE: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_ONE,
    shines=[
        Shine(
            "Ricco 1 Only - Gooper Blooper Breaks Out",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=10,
        ),
        Shine(
            "100 Coins",
            requirements=[
                Requirements(ROCKET_OR_HOVER),
                Requirements(
                    location=f"{SmsRegionName.RICCO_FIVE} - Gooper Blooper Returns"
                ),
            ],
            hard=[Requirements(manual_none=True)],
            hundred=True,
            in_game_bit=101,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Tower Wall",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=221,
        ),
        BlueCoin(
            "Outer Ship M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=222,
        ),
        BlueCoin(
            "Spawn Building Top M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=223,
        ),
        BlueCoin(
            "Fruit Machine X",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=224,
        ),
        BlueCoin(
            "Rooftop M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=226,
        ),
        BlueCoin(
            "Far Ledge",
            requirements=[
                Requirements(SPROCKET_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            tears=[Requirements(SPROCKET_OR_HOVER_OR_TURBO)],
            in_game_bit=228,
        ),
        BlueCoin(
            "Short Beam",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=229,
        ),
        BlueCoin(
            "Tower Platform",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=230,
        ),
        BlueCoin(
            "Long Beam",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=231,
        ),
        BlueCoin(
            "Off Catwalk",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=232,
        ),
        BlueCoin(
            "Crane",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=234,
        ),
        BlueCoin(
            "Blooper Open Water",
            requirements=[
                Requirements(ROCKET_OR_TURBO),
                Requirements(
                    location=f"{SmsRegionName.RICCO_TWO} - Blooper Surfing Safari",
                ),
            ],
            advanced=[
                Requirements(ROCKET_OR_HOVER_OR_TURBO),
                Requirements(
                    location=f"{SmsRegionName.RICCO_TWO} - Blooper Surfing Safari",
                ),
            ],
            in_game_bit=235,
        ),
        BlueCoin("Fountain", in_game_bit=237),
        BlueCoin("Underwater", in_game_bit=238),
        BlueCoin(
            "Tower X",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=239,
        ),
        BlueCoin(
            "Fountain M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.RICCO_EIGHT} - Yoshi's Fruit Adventure",
                ),
            ],
            in_game_bit=240,
        ),
        BlueCoin("Tower Crate", in_game_bit=248),
        BlueCoin(
            "Tower Rocket",
            requirements=[Requirements([[NozzleType.rocket]])],
            advanced=[Requirements(ROCKET_OR_TURBO)],
            in_game_bit=233,
        ),
        BlueCoin(
            "Tower Ground M",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=227,
        ),
        BlueCoin(
            "Spawn Building Side M",
            [Requirements(SPRAY_OR_HOVER)],
            in_game_bit=241,
        ),
        BlueCoin(
            "Inner Ship M",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=246,
        ),
        BlueCoin(
            "Yellow Submarine",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=249,
        ),
    ],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_TWO: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_TWO,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.RICCO_ONE} - Ricco 1 Only - Gooper Blooper Breaks Out"
        )
    ],
    shines=[
        Shine("Blooper Surfing Safari", in_game_bit=11),
        Shine("Blooper-Surfing Sequel", in_game_bit=19),
    ],
    blue_coins=[BlueCoin("Blooper Underground Entrance", in_game_bit=236)],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_THREE: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_THREE,
    requirements=[
        Requirements(location=f"{SmsRegionName.RICCO_TWO} - Blooper Surfing Safari")
    ],
    shines=[
        Shine(
            "The Caged Shine Sprite",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=12,
        ),
    ],
    blue_coins=[
        BlueCoin("Mesh Wall Klamber", in_game_bit=243),
        BlueCoin("Mesh Ceiling Klamber", in_game_bit=244),
    ],
    nozzle_boxes=[
        NozzleBox(
            "Rocket Box",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=874,
        )
    ],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_FOUR,
    requirements=[
        Requirements(location=f"{SmsRegionName.RICCO_THREE} - The Caged Shine Sprite")
    ],
    shines=[
        Shine(
            "The Secret of Ricco Tower",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=13,
        ),
        Shine("Red Coins in Ricco Tower", in_game_bit=18),
    ],  # TODO: Fix logic with difficulties
    blue_coins=[
        BlueCoin(
            "Caged Blooper",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=247,
        )
    ],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.RICCO_FOUR} - The Secret of Ricco Tower")
    ],
    shines=[
        Shine(
            "Gooper Blooper Returns",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=14,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_SIX: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_SIX,
    requirements=[
        Requirements(location=f"{SmsRegionName.RICCO_FIVE} - Gooper Blooper Returns")
    ],
    shines=[Shine("Red Coins on the Water", in_game_bit=15)],
    blue_coins=[],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_SEVEN,
    requirements=[
        Requirements(location=f"{SmsRegionName.RICCO_SIX} - Red Coins on the Water")
    ],
    shines=[
        Shine(
            "Shadow Mario Revisited",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=16,
        )
    ],
    blue_coins=[],
    nozzle_boxes=[NozzleBox("Turbo Box", in_game_bit=875)],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

RICCO_HARBOR_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.RICCO_EIGHT,
    requirements=[
        Requirements(location=f"{SmsRegionName.RICCO_SEVEN} - Shadow Mario Revisited")
    ],
    shines=[
        Shine(
            "Yoshi's Fruit Adventure",
            requirements=[Requirements([[NozzleType.yoshi]])],
            advanced=[Requirements(YOSHI_OR_ROCKET)],
            in_game_bit=17,
        )
    ],
    blue_coins=[
        BlueCoin("Butterflies", [Requirements([[NozzleType.yoshi]])], in_game_bit=220),
        BlueCoin(
            "Wall Klamber",
            requirements=[Requirements([[NozzleType.yoshi]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=225,
        ),
        BlueCoin(
            "High Platform M",
            requirements=[Requirements([[NozzleType.yoshi]])],
            hard=[Requirements(SPROCKET_OR_HOVER)],
            in_game_bit=242,
        ),
        BlueCoin(
            "Fish Basket",
            requirements=[Requirements(ANY_SPLASHER)],
            hard=[Requirements(ANY_SPLASHER_OR_TURBO)],
            advanced=[Requirements(ANY_NOZZLE)],
            in_game_bit=245,
        ),
    ],
    parent_region=SmsRegionName.RICCO_ENTRANCE,
)

from .sms_region_helper import *

BIANCO_HILLS_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_ENTRANCE,
    requirements=[Requirements(ANY_SPLASHER), Requirements(skip_forward=True)],
    ticketed="Bianco Hills Ticket",
    parent_region=SmsRegionName.PLAZA,
)

BIANCO_HILLS_ONE: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_ONE,
    shines=[
        Shine(
            "Road to the Big Windmill",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=0,
        ),
        Shine(
            "100 Coins",
            requirements=[
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements([[NozzleType.hover]]),
                Requirements(
                    SPRAY_OR_HOVER,
                    location=f"{SmsRegionName.BIANCO_ONE} - Road to the Big Windmill",
                ),
                Requirements(
                    SPRAY_OR_HOVER,
                    location=f"{SmsRegionName.BIANCO_ONE} - Road to the Big Windmill",
                ),
                Requirements(
                    SPRAY_OR_HOVER_OR_TURBO,
                    location=f"{SmsRegionName.BIANCO_SEVEN} - Shadow Mario on the Loose",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
            ],
            hundred=True,
            in_game_bit=100,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Windmill M",
            requirements=[
                Requirements([[NozzleType.hover]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=170,
        ),
        BlueCoin(
            "Windmill Pillar",
            requirements=[
                Requirements(SPRAY_OR_HOVER_OR_ROCKET),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(ANY_FLUDD),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=171,
        ),
        BlueCoin(
            "Towers House M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=188,
        ),
        BlueCoin(
            "Balcony",
            requirements=[
                Requirements([[NozzleType.hover]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(ANY_FLUDD),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=173,
        ),
        BlueCoin("Underwater Right", in_game_bit=180),
        BlueCoin(
            "Wall Side M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=186,
        ),
        BlueCoin(
            "Wall Top M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=187,
        ),
        BlueCoin(
            "Towers House",
            requirements=[
                Requirements(ROCKET_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[Requirements(manual_none=True)],
            in_game_bit=172,
        ),
        BlueCoin(
            "Pinwheel",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=189,
        ),
        BlueCoin(
            "X Behind Wall",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=190,
        ),
        BlueCoin("River End", in_game_bit=191),
        BlueCoin(
            "X Between Walls",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=197,
        ),
        BlueCoin(
            "Sail Platform",
            requirements=[
                Requirements([[NozzleType.hover]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[Requirements(manual_none=True)],
            in_game_bit=198,
        ),
    ],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_TWO: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_TWO,
    requirements=[
        Requirements(location=f"{SmsRegionName.BIANCO_ONE} - Road to the Big Windmill")
    ],
    shines=[
        Shine(
            "Down with Petey Piranha!",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=1,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_THREE: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_THREE,
    requirements=[
        Requirements(location=f"{SmsRegionName.BIANCO_TWO} - Down with Petey Piranha!")
    ],
    shines=[
        Shine(
            "The Hillside Cave Secret",
            requirements=[Requirements(SPRAY_OR_HOVER_OR_ROCKET)],
            hard=[Requirements(ANY_FLUDD)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=2,
        ),
        Shine(
            "Red Coins of the Hillside Cave",
            requirements=[
                Requirements(
                    ROCKET_OR_HOVER,
                    location=f"{SmsRegionName.BIANCO_THREE} - The Hillside Cave Secret",
                ),
            ],
            advanced=[
                Requirements(
                    location=f"{SmsRegionName.BIANCO_THREE} - The Hillside Cave Secret"
                )
            ],
            in_game_bit=8,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Treetop",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(ANY_FLUDD),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=174,
        ),
        BlueCoin(
            "Tourist",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=175,
        ),
        BlueCoin(
            "Windmill Pokey",
            requirements=[
                Requirements(ROCKET_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[Requirements(manual_none=True)],
            in_game_bit=184,
        ),
        BlueCoin(
            "Cliff",
            requirements=[
                Requirements(ROCKET_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(ROCKET_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=192,
        ),
        BlueCoin(
            "Highest Platform",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=199,
        ),
    ],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_FOUR,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.BIANCO_THREE} - The Hillside Cave Secret"
        )
    ],
    shines=[
        Shine(
            "Red Coins of Windmill Village",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=3,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Hillside Pokey",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=178,
        ),
        BlueCoin("Bridge Underside", in_game_bit=183),
    ],
    nozzle_boxes=[NozzleBox("Rocket Box", in_game_bit=872)],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_FIVE,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.BIANCO_FOUR} - Red Coins of Windmill Village"
        )
    ],
    shines=[
        Shine(
            "Petey Piranha Strikes Back",
            requirements=[Requirements(SPROCKET_OR_SPROVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=4,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Wall Tower Pianta",
            requirements=[
                Requirements(SPROCKET_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPROCKET_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=177,
        ),
        BlueCoin(
            "Platforms Cross",
            requirements=[
                Requirements(ROCKET_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_ROCKET),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(ANY_FLUDD),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=185,
        ),
    ],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_SIX: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_SIX,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.BIANCO_FIVE} - Petey Piranha Strikes Back"
        )
    ],
    shines=[
        Shine(
            "The Secret of the Dirty Lake",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=5,
        ),
        Shine(
            "Red Coins of the Dirty Lake",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=9,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Petey Pillar",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_ROCKET),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(ANY_FLUDD),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=179,
        ),
        BlueCoin("Underwater Left", in_game_bit=181),
        BlueCoin(
            "Blue Bird",
            requirements=[Requirements([[NozzleType.spray]])],
            tears=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=182,
        ),
        BlueCoin("Chuckster Momma", in_game_bit=193),
    ],
    nozzle_boxes=[
        NozzleBox(
            "Turbo Box",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(ANY_FLUDD)],
            in_game_bit=873,
        )
    ],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_SEVEN,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.BIANCO_SIX} - The Secret of the Dirty Lake"
        )
    ],
    shines=[
        Shine(
            "Shadow Mario on the Loose",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=6,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Towers House O",
            [
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=194,
        ),
        BlueCoin(
            "Balcony House O",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.BIANCO_EIGHT} - The Red Coins of the Lake",
                ),
            ],
            in_game_bit=195,
        ),
    ],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

BIANCO_HILLS_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.BIANCO_EIGHT,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.BIANCO_SEVEN} - Shadow Mario on the Loose"
        )
    ],
    shines=[
        Shine(
            "The Red Coins of the Lake",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=7,
        )
    ],
    blue_coins=[
        BlueCoin("Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=176),
        BlueCoin("Butterfly", [Requirements([[NozzleType.yoshi]])], in_game_bit=196),
    ],
    parent_region=SmsRegionName.BIANCO_ENTRANCE,
)

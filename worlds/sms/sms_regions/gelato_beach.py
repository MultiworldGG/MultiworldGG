from .sms_region_helper import *
from .sms_region_helper import SPRAY_OR_HOVER

GELATO_BEACH_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_ENTRANCE,
    requirements=[Requirements(SPRAY_OR_HOVER, shines=5)],
    hard=[],
    advanced=[],
    tears=[],
    ticketed="Gelato Beach Ticket",
    parent_region=SmsRegionName.PLAZA,
)

GELATO_BEACH_ONE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_ONE,
    shines=[
        Shine(
            "Dune Bud Sand Castle Secret",
            [Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=20,
        ),
        Shine(
            "Red Coins in the Sand Castle",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=28,
        ),
        Shine(
            "Sandy Shine Sprite",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=29,
        ),
        Shine(
            "100 Coins",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.turbo]],
                    location=f"{SmsRegionName.GELATO_SEVEN} - It's Shadow Mario! After Him!",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.rocket]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
                Requirements(
                    [[NozzleType.turbo]],
                    location=f"{SmsRegionName.GELATO_SEVEN} - It's Shadow Mario! After Him!",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.rocket]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
                Requirements(
                    location=f"{SmsRegionName.GELATO_SEVEN} - It's Shadow Mario! After Him!",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.turbo]],
                    location=f"{SmsRegionName.GELATO_THREE} - Wiggler Ahoy! Full Steam Ahead!",
                ),
                Requirements(
                    [[NozzleType.rocket]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
                Requirements(
                    location=f"{SmsRegionName.GELATO_SEVEN} - It's Shadow Mario! After Him!",
                ),
            ],
            hundred=True,
            in_game_bit=102,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Juicer",
            [
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint"
                ),
            ],
            in_game_bit=275,
        ),
        BlueCoin(
            "Rocket M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=276,
        ),
        BlueCoin(
            "Spawn Triangle",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=277,
        ),
        BlueCoin(
            "Trees Triangle",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=278,
        ),
        BlueCoin(
            "Left Bird",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=280,
        ),
        BlueCoin(
            "Right Bird",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=281,
        ),
        BlueCoin(
            "Highest Rope",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=282,
        ),
        BlueCoin(
            "Pole",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=283,
        ),
        BlueCoin("Deck", in_game_bit=288),
        BlueCoin(
            "Swing",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=289,
        ),
        BlueCoin("Big Tree", in_game_bit=290),
        BlueCoin("Crevice", in_game_bit=291),
        BlueCoin("Sand Cabana Roof", in_game_bit=293),
        BlueCoin(
            "Shack",
            requirements=[Requirements([[NozzleType.rocket]])],
            hard=[Requirements(ROCKET_OR_HOVER)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=294,
        ),
        BlueCoin(
            "Red Cataquack",
            requirements=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=270,
        ),
        BlueCoin(
            "Sand Shine at Sand Cabana",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=271,
        ),
        BlueCoin(
            "Sand Shine at Surf Cabana",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=272,
        ),
        BlueCoin(
            "Middle Sand Shine",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=274,
        ),
        BlueCoin("Close Underwater", in_game_bit=284),
        BlueCoin("Far Underwater", in_game_bit=285),
        BlueCoin(
            "Blue Fish",
            requirements=[Requirements([[NozzleType.turbo]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=286,
        ),
        BlueCoin(
            "Red Fish",
            requirements=[Requirements([[NozzleType.turbo]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=287,
        ),
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_TWO: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_TWO,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_ONE} - Dune Bud Sand Castle Secret"
        )
    ],
    shines=[
        Shine(
            "Mirror Madness! Tilt, Slam, Bam!",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=21,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Big Sand Shine",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            in_game_bit=292,
        )
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_THREE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_THREE,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_TWO} - Mirror Madness! Tilt, Slam, Bam!"
        )
    ],
    shines=[
        Shine(
            "Wiggler Ahoy! Full Steam Ahead!",
            [Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=22,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_FOUR,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_THREE} - Wiggler Ahoy! Full Steam Ahead!"
        )
    ],
    shines=[
        Shine(
            "The Sand Bird is Born",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=23,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Sand Bird A",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=296,
        ),
        BlueCoin(
            "Sand Bird B",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=297,
        ),
        BlueCoin(
            "Sand Bird C",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=298,
        ),
        BlueCoin(
            "Sand Bird D",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=299,
        ),
    ],
    nozzle_boxes=[NozzleBox("Turbo Box", in_game_bit=877)],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.GELATO_FOUR} - The Sand Bird is Born")
    ],
    shines=[
        Shine(
            "Il Piantissimo's Sand Sprint",
            requirements=[Requirements(ROCKET_OR_HOVER_OR_TURBO)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=24,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Blue Cataquack",
            [
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef",
                ),
            ],
            [Requirements(manual_none=True)],
            in_game_bit=273,
        )
    ],
    nozzle_boxes=[
        NozzleBox(
            "Rocket Box",
            requirements=[
                Requirements(ANY_FLUDD),
                Requirements(
                    ANY_NOZZLE,
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            hard=[Requirements(manual_none=True)],
            in_game_bit=876,
        )
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_SIX: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_SIX,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint"
        )
    ],
    shines=[Shine("Red Coins in the Coral Reef", in_game_bit=25)],
    blue_coins=[
        BlueCoin(
            "Yellow Goo Dune Bud", [Requirements([[NozzleType.yoshi]])], in_game_bit=279
        ),
        BlueCoin("Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=295),
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_SEVEN,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef"
        )
    ],
    shines=[
        Shine(
            "It's Shadow Mario! After Him!",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=26,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_EIGHT,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_SEVEN} - It's Shadow Mario! After Him!"
        )
    ],
    shines=[
        Shine(
            "The Watermelon Festival",
            requirements=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=27,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

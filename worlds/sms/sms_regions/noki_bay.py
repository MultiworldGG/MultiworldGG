from .sms_region_helper import *

NOKI_BAY_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_ENTRANCE,
    requirements=[Requirements(shines=20)],
    hard=[],
    advanced=[],
    tears=[],
    ticketed="Noki Bay Ticket",
    parent_region=SmsRegionName.PLAZA,
)

NOKI_BAY_ONE: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_ONE,
    shines=[
        Shine(
            "Uncork the Waterfall",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=50,
        ),
        Shine(
            "A Golden Bird",
            requirements=[Requirements([[NozzleType.spray]])],
            advanced=[Requirements(SPRAY_OR_HOVER)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=59,
        ),
        Shine(
            "100 Coins",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            hundred=True,
            in_game_bit=105,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Rocket Alcove",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            tears=[Requirements(ROCKET_OR_HOVER_OR_TURBO)],
            in_game_bit=470,
        ),
        BlueCoin(
            "Bottom Secret Path",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=471,
        ),
        BlueCoin(
            "Top Secret Path",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=472,
        ),
        BlueCoin(
            "Rocket",
            requirements=[Requirements([[NozzleType.rocket]])],
            tears=[Requirements(ROCKET_OR_TURBO)],
            in_game_bit=473,
        ),
        BlueCoin(
            "Bottom Pulley",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=474,
        ),
        BlueCoin(
            "Top Pulley",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=475,
        ),
        BlueCoin(
            "Tall Alcove",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=476,
        ),
        BlueCoin(
            "Turbo Alcove",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=477,
        ),
        BlueCoin(
            "Shell Alcove",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(ROCKET_OR_HOVER)],
            tears=[Requirements(ROCKET_OR_HOVER_OR_TURBO)],
            in_game_bit=478,
        ),
        BlueCoin("Top Right Panel", [Requirements(SPRAY_AND_HOVER)], in_game_bit=479),
        BlueCoin("Bottom Left Panel", [Requirements(SPRAY_AND_HOVER)], in_game_bit=480),
        BlueCoin("Top Right Tunnel", [Requirements(SPRAY_AND_HOVER)], in_game_bit=481),
        BlueCoin(
            "Bottom Right Tunnel", [Requirements(SPRAY_AND_HOVER)], in_game_bit=482
        ),
        BlueCoin(
            "Bottom Right Alcove", [Requirements(SPRAY_AND_HOVER)], in_game_bit=483
        ),
        BlueCoin("Left Tunnel", [Requirements(SPRAY_AND_HOVER)], in_game_bit=484),
        BlueCoin(
            "Bottom Left Alcove", [Requirements(SPRAY_AND_HOVER)], in_game_bit=485
        ),
        BlueCoin("Bird Cliff Panel", [Requirements(SPRAY_AND_HOVER)], in_game_bit=486),
        BlueCoin("Bird Cliff Alcove", [Requirements(SPRAY_AND_HOVER)], in_game_bit=487),
        BlueCoin(
            "Spawn",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=490,
        ),  # With clear water, this is easy with turbo
        BlueCoin(
            "Coast",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=491,
        ),
        BlueCoin("Underwater", in_game_bit=492),
        BlueCoin(
            "Top Secret Path M",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=493,
        ),
    ],
    nozzle_boxes=[
        NozzleBox(
            "Rocket Box",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            tears=[Requirements(ROCKET_OR_HOVER_OR_TURBO)],
            in_game_bit=884,
        )
    ],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_TWO: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_TWO,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_ONE} - Uncork the Waterfall")
    ],
    shines=[
        Shine(
            "The Boss of Tricky Ruins",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=51,
        ),
    ],
    blue_coins=[
        BlueCoin("Right Urn", [Requirements(SPRAY_OR_HOVER)], in_game_bit=488),
        BlueCoin("Left Urn", [Requirements(SPRAY_OR_HOVER)], in_game_bit=489),
    ],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_THREE: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_THREE,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_TWO} - The Boss of Tricky Ruins")
    ],
    shines=[
        Shine(
            "Red Coins in a Bottle",
            requirements=[Requirements([[NozzleType.hover]])],
            tears=[Requirements(manual_none=True)],
            in_game_bit=52,
        ),
    ],  # Underwater Nozzle
    blue_coins=[],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_FOUR,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_THREE} - Red Coins in a Bottle")
    ],
    shines=[
        Shine(
            "Eely-Mouth's Dentist",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=53,
        ),
    ],  # Underwater Nozzle
    blue_coins=[
        BlueCoin(
            "Deep Sea Front Pillar",
            [Requirements([[NozzleType.hover]])],
            in_game_bit=495,
        ),
        BlueCoin(
            "Deep Sea Right Pillar",
            [Requirements([[NozzleType.hover]])],
            in_game_bit=496,
        ),
        BlueCoin(
            "Deep Sea Close Left Pillar",
            [Requirements([[NozzleType.hover]])],
            in_game_bit=497,
        ),
        BlueCoin(
            "Deep Sea Far Left Pillar",
            [Requirements([[NozzleType.hover]])],
            in_game_bit=499,
        ),
    ],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_FOUR} - Eely-Mouth's Dentist")
    ],
    shines=[
        Shine(
            "Il Piantissimo's Surf Swim",
            in_game_bit=54,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_SIX: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_SIX,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_FIVE} - Il Piantissimo's Surf Swim")
    ],
    shines=[
        Shine(
            "The Shell's Secret",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=55,
        ),
        Shine(
            "Red Coins on the Half Shell",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=58,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Spawn O",
            [Requirements(SPRAY_AND_TURBO_OR_HOVER_AND_TURBO)],
            [Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=494,
        ),
        BlueCoin(
            "Boathouse O",
            [Requirements(SPRAY_AND_TURBO_OR_HOVER_AND_TURBO)],
            [Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=498,
        ),
    ],
    nozzle_boxes=[
        NozzleBox(
            "Turbo Box",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=885,
        )
    ],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_SEVEN,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_SIX} - The Shell's Secret")
    ],
    shines=[
        Shine(
            "Hold It, Shadow Mario!",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            advanced=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=56,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

NOKI_BAY_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.NOKI_EIGHT,
    requirements=[
        Requirements(location=f"{SmsRegionName.NOKI_SEVEN} - Hold It, Shadow Mario!")
    ],
    shines=[
        Shine(
            "The Red Coin Fish",
            requirements=[Requirements([[NozzleType.hover]])],
            tears=[Requirements(manual_none=True)],
            in_game_bit=57,
        ),
    ],  # Underwater Nozzle
    blue_coins=[],
    parent_region=SmsRegionName.NOKI_ENTRANCE,
)

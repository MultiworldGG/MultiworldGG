from .sms_region_helper import *

# Non-ticket requires yoshi to clear out the pineapple blocking the pipe. Ticket removes pineapple.
SIRENA_BEACH_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_ENTRANCE,
    requirements=[Requirements([[NozzleType.yoshi]], shines=5), Requirements([[NozzleType.yoshi]], skip_forward=True)],
    ticketed="Sirena Beach Ticket",
    parent_region=SmsRegionName.PLAZA,
)

SIRENA_BEACH_ONE: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_ONE,
    shines=[
        Shine(
            "The Manta Storm",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=40,
        ),
        Shine(
            "100 Coins",  # Maybe revisit this one. Can probably get more detailed, but I really don't want to do it
            requirements=[
                Requirements(
                    [[NozzleType.spray]],
                    location=f"{SmsRegionName.SIRENA_TWO} - The Hotel Lobby's Secret",
                )
            ],
            advanced=[Requirements(SPRAY_OR_HOVER)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            hundred=True,
            in_game_bit=104,
        ),
    ],
    blue_coins=[
        BlueCoin("Ocean", in_game_bit=387),
        BlueCoin(
            "Right Male Noki",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=373,
        ),
        BlueCoin(
            "Right Female Noki",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=374,
        ),
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_TWO: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_TWO,
    requirements=[
        Requirements(location=f"{SmsRegionName.SIRENA_ONE} - The Manta Storm")
    ],
    shines=[
        Shine(
            "The Hotel Lobby's Secret",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=41,
        ),
        Shine(
            "Red Coins in Boo's Big Mouth",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=48,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Sign",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=370,
        ),
        BlueCoin("Cabana Roof", in_game_bit=371),
        BlueCoin(
            "Outside Torch",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=372,
        ),
        BlueCoin(
            "Hotel Ledge",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(ROCKET_OR_HOVER_OR_TURBO)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=375,
        ),
        BlueCoin(
            "Flowers",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=386,
        ),
        BlueCoin(
            "Third Floor Lamp",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=392,
        ),
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_THREE: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_THREE,
    requirements=[
        Requirements(location=f"{SmsRegionName.SIRENA_TWO} - The Hotel Lobby's Secret")
    ],
    shines=[
        Shine(
            "Mysterious Hotel Delfino",
            requirements=[Requirements(ALL_SPLASHERS)],
            hard=[Requirements(YOSHI_AND_SPRAY_OR_YOSHI_AND_HOVER)],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=42,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Big Light",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=376,
        ),
        BlueCoin(
            "Box Hole",
            requirements=[Requirements([[NozzleType.yoshi]])],
            advanced=[Requirements(manual_none=True)],
            in_game_bit=378,
        ),  # This hard requires Yoshi without Episode rando
        BlueCoin("Glass Hole", in_game_bit=379),
        BlueCoin(
            "White Painting",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=380,
        ),
        BlueCoin(
            "Dolpic Poster",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            advanced=[Requirements(ANY_FLUDD)],
            in_game_bit=381,
        ),
        BlueCoin(
            "Bookshelf",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=382,
        ),
        BlueCoin("Attic", in_game_bit=383),
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_FOUR,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.SIRENA_THREE} - Mysterious Hotel Delfino"
        )
    ],
    shines=[
        Shine(
            "The Secret of Casino Delfino",
            [Requirements([[NozzleType.spray]])],
            in_game_bit=43,
        ),
        Shine(
            "Red Coin Winnings in the Casino",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements([[NozzleType.spray]])],
            in_game_bit=49,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Casino Torch",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=398,
        ),
        BlueCoin("Slot machine", in_game_bit=399),
        BlueCoin("Crate", in_game_bit=377),
        BlueCoin("Attic Boo", in_game_bit=385),
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_FIVE,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.SIRENA_FOUR} - The Secret of Casino Delfino"
        )
    ],
    shines=[
        Shine(
            "King Boo Down Below",
            requirements=[Requirements([[NozzleType.spray]])],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=44,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Casino M",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=391,
        )
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_SIX: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_SIX,
    requirements=[
        Requirements(location=f"{SmsRegionName.SIRENA_FIVE} - King Boo Down Below")
    ],
    shines=[
        Shine(
            "Scrubbing Sirena Beach",
            requirements=[Requirements([[NozzleType.spray]])],
            tears=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=45,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Left Male Noki",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=384,
        ),
        BlueCoin(
            "Left Female Noki",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=390,
        ),
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_SEVEN,
    requirements=[
        Requirements(location=f"{SmsRegionName.SIRENA_SIX} - Scrubbing Sirena Beach")
    ],
    shines=[
        Shine(
            "Shadow Mario Checks In",
            requirements=[Requirements([[NozzleType.spray]])],
            tears=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=46,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Outside M",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=388,
        ),
        BlueCoin(
            "Second Floor M",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=389,
        ),
        BlueCoin(
            "Ground Floor Triangle",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=393,
        ),
        BlueCoin(
            "First Floor Triangle",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=394,
        ),
        BlueCoin(
            "Attic M",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=395,
        ),
        BlueCoin(
            "Second Floor X",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=396,
        ),
        BlueCoin(
            "First Floor X",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=397,
        ),
    ],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

SIRENA_BEACH_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.SIRENA_EIGHT,
    requirements=[
        Requirements(location=f"{SmsRegionName.SIRENA_SEVEN} - Shadow Mario Checks In")
    ],
    shines=[
        Shine(
            "Red Coins in the Hotel",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=47,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.SIRENA_ENTRANCE,
)

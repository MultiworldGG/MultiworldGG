from .sms_region_helper import *

CORONA_MOUNTAIN: SmsRegion = SmsRegion(
    SmsRegionName.CORONA,
    requirements=[Requirements(corona=True)],
    blue_coins=[
        BlueCoin(
            "Platform",
            requirements=[Requirements([[NozzleType.hover]])],
            tears=[Requirements(SPRAY_OR_HOVER_OR_ROCKET)],
            in_game_bit=540,
        ),
        BlueCoin(
            "Back Right Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=541,
        ),
        BlueCoin(
            "Left Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=542,
        ),
        BlueCoin(
            "Front Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=543,
        ),
        BlueCoin(
            "Front Left Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=544,
        ),
        BlueCoin(
            "Front Right Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=545,
        ),
        BlueCoin(
            "Back Left Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=546,
        ),
        BlueCoin(
            "Far Back Left Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=547,
        ),
        BlueCoin(
            "Far Back Right Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=548,
        ),
        BlueCoin(
            "Right Lava",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=549,
        ),
    ],
    nozzle_boxes=[
        NozzleBox(
            "Rocket Box",
            requirements=[Requirements(SPRAY_AND_HOVER)],
            tears=[Requirements(manual_none=True)],
            in_game_bit=886,
        )
    ],
    parent_region=SmsRegionName.PLAZA,
)

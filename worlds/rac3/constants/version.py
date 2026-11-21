"""This module contains the constant strings used to determine which version of RAC3 is being played"""

from worlds.rac3.constants.galactic_map import RAC3GALACTICMAP
from worlds.rac3.constants.region import PLANET_LOAD_OFFSET, PLANET_MENU_OFFSET, RAC3REGION
from worlds.rac3.constants.status import RAC3STATUS


class RAC3VERSION:
    """Constant Strings for the ID of each known version of RAC3"""
    US_ID = "SCUS-97353"
    US_BETA_ID = "SCUS-97413"
    US_DEMO_ID = "SCUS-97411"
    US_GH_ID = "SCUS-97518"
    JP_ID = "SCPS-15084"
    JP_TRIAL_ID = "PCPX-96653"
    JP_TB_ID = "SCPS-19309"
    KO_ID = "SCKA-20037"
    CH_ID = "SCAJ-20109"
    EU_ID = "SCES-52456"
    EU_BETA_ID = "TCES-52456"
    EU_DEMO_ID = "SCED-52847"


GAME_ID_TO_VERSION: dict[str, str] = {
    RAC3VERSION.US_ID: "US release",
    RAC3VERSION.US_BETA_ID: "US beta",
    RAC3VERSION.US_DEMO_ID: "US demo",
    RAC3VERSION.US_GH_ID: "US Greatest Hits release",
    RAC3VERSION.JP_ID: "Japanese release",
    RAC3VERSION.JP_TRIAL_ID: "Japanese trial version",
    RAC3VERSION.JP_TB_ID: "Japanese The Best release",
    RAC3VERSION.KO_ID: "Korean release",
    RAC3VERSION.CH_ID: "Chinese release",
    RAC3VERSION.EU_ID: "EU release",
    RAC3VERSION.EU_BETA_ID: "EU beta",
    RAC3VERSION.EU_DEMO_ID: "EU demo",
}

GAME_ID_TO_OFFSET: dict[str, int] = {
    RAC3VERSION.US_ID: 0x0,
    RAC3VERSION.EU_ID: -0x80,
}

PAL_SHIFTED_PLANETS: list[str] = [
    RAC3REGION.VELDIN,
    RAC3REGION.FLORANA,
    RAC3REGION.STARSHIP_PHOENIX,
    RAC3REGION.MARCADIA,
    RAC3REGION.DAXX,
    RAC3REGION.TYHRRANOSIS,
    RAC3REGION.ZELDRIN_STARPORT,
    RAC3REGION.BLACKWATER_CITY,
    RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3REGION.ARIDIA,
    RAC3REGION.OBANI_DRACO,
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK,
    RAC3REGION.METROPOLIS_RANGERS,
    RAC3REGION.QWARK_VID_COMIC_1,
    RAC3REGION.QWARK_VID_COMIC_2,
    RAC3REGION.QWARK_VID_COMIC_3,
    RAC3REGION.QWARK_VID_COMIC_5,
]

JP_SHIFTED_PLANETS: list[str] = [
    RAC3REGION.FLORANA,
    RAC3REGION.AQUATOS_SEWERS,
    RAC3REGION.AQUATOS_BASE,
    RAC3REGION.PHOENIX_ASSAULT,
    RAC3REGION.OBANI_GEMINI,
    RAC3REGION.OBANI_DRACO,
    RAC3REGION.CRASH_SITE,
    RAC3REGION.HOLOSTAR_STUDIOS_CLANK,
    RAC3REGION.AQUATOS,
    RAC3REGION.ZELDRIN_STARPORT,
    RAC3REGION.ANNIHILATION_NATION,
    RAC3REGION.MUSEUM,
    RAC3REGION.HOLOSTAR_STUDIOS,
    RAC3REGION.KOROS,
    RAC3REGION.QWARKS_HIDEOUT,
    RAC3REGION.METROPOLIS,
    RAC3REGION.MARCADIA,
]

JP_VENDOR_OFFSET_CORRECTION: dict[str, int] = {
    RAC3REGION.QWARKS_HIDEOUT: -0x40,
    RAC3REGION.MARCADIA: -0x40,
    RAC3REGION.TYHRRANOSIS: -0x40,
    RAC3REGION.OBANI_DRACO: -0x40,
}


def jp_convert_address(address: int, planet: str) -> int:
    """Convert a US-relative address to its JP equivalent."""
    load_offset = PLANET_LOAD_OFFSET.get(planet)
    if load_offset is not None:
        for base in (RAC3STATUS.PLANET_LOAD_BASE, RAC3STATUS.PLANET_STRING_TABLE_BASE):
            field = base + load_offset
            if field <= address < field + 4:
                return address + 0x9380
    pause_offset = PLANET_MENU_OFFSET.get(planet)
    if pause_offset is not None:
        pause_base = RAC3STATUS.PAUSE_BASE + pause_offset
        if pause_offset < 0:
            # Vid-comics use a separate word instead of a menu screen record.
            if pause_base <= address < pause_base + 4:
                return address + 0x92D4
        else:
            # The 0x18-byte gameplay screen record and its initialization word.
            if pause_base <= address < pause_base + 0x1C:
                return address + 0x9398
            # Two bolt-HUD animation records followed by their display bookkeeping.
            bolt_hud = RAC3STATUS.PLANET_BOLT_DIFFERENCE_BASE + pause_offset
            if bolt_hud <= address < bolt_hud + 0x34:
                return address + 0x9380
    rows_base = RAC3GALACTICMAP.get_rows_address(planet)
    if rows_base is not None:
        manager_state = RAC3GALACTICMAP.get_ui_manager_state_address(planet)
        if manager_state <= address < manager_state + 4:
            return address + 0x93A0
        if rows_base <= address < rows_base + RAC3GALACTICMAP.MAX_ROWS * RAC3GALACTICMAP.ROW_SIZE:
            # This array has one shift throughout, even across the generic ranges below.
            offset = 0x93C0 + JP_VENDOR_OFFSET_CORRECTION.get(planet, 0)
            if planet == RAC3REGION.MUSEUM:
                offset -= 0x40
            return address + offset
    addr = address
    if planet in JP_SHIFTED_PLANETS and 0x001DE000 <= addr < 0x001DF000:
        addr += 0x80
    # Remaining ranges are legacy fallbacks, not universal overlay boundaries.
    for start, end, offset in [
        (0x0016C000, 0x0016CFFF, 0x9280),
        (0x00140000, 0x0019FFFF, -0x80),
        (0x001A0000, 0x001B0000, 0x9280),
        (0x0010BB00, 0x001CD0BF, 0x9298),
        (0x001CD0C0, 0x001D4D7F, 0x92C0),
        (0x001DEF34, 0x001DEF34, 0x9380),
        (0x001D4D80, 0x001DF000, 0x9300),
        (0x001DF001, 0x001DFFFF, 0x9380),
        (0x001E0000, 0x00200000, 0x106C),
        (0x00200001, 0x00234000, 0x9380),
        (0x00234CD0, 0x00234CD0, 0x9380),
        (0x00235650, 0x00235650, 0x9380),
        (0x00234001, 0x00237910, 0x93C0),
        (0x00237911, 0x002417CF, 0x9380),
        (0x002417D0, 0x00260000, 0x93C0),
    ]:
        if start <= addr <= end:
            addr += offset
            break
    return addr



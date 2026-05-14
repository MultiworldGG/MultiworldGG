from enum import Enum, auto
from pymem import Pymem


from .common_addresses import steam_to_gog, gog_to_steam


class GameVersion(Enum):
    GOG = auto()
    STEAM = auto()


# The Steam and GOG versions are slightly different compiled builds. Memory addresses are offset at various points, a
# small number of library functions have different compiled instructions, and there are a few references file paths with
# different contents.
IDENTIFIER_ADDRESS = 0x75e978
# The address is the same in both GOG and Steam.
assert gog_to_steam(IDENTIFIER_ADDRESS) == IDENTIFIER_ADDRESS
assert steam_to_gog(IDENTIFIER_ADDRESS) == IDENTIFIER_ADDRESS
GOG_PREFIX = rb"d:\\projects\\game_saga"
STEAM_PREFIX = rb"d:\\projects\\legosagapc"
IDENTIFIER_SUFFIX = rb"\\nu2api.saga\\nucore\\nufile.c"
GOG_IDENTIFIER = GOG_PREFIX + IDENTIFIER_SUFFIX
STEAM_IDENTIFIER = STEAM_PREFIX + IDENTIFIER_SUFFIX


def get_game_version(process: Pymem) -> tuple[GameVersion | None, int]:
    """
    Get the game version of the connected process and an offset from the expected address used to identify the game
    version.

    :param process: An opened LegoStarWarsSaga process.
    :return: The game version and an offset to be added to all non-raw memory reads/writes.
    """
    identifier_start = process.read_bytes(IDENTIFIER_ADDRESS, max(len(GOG_PREFIX), len(STEAM_PREFIX)))

    # GOG
    if identifier_start.startswith(GOG_PREFIX):
        return GameVersion.GOG, 0

    # Steam
    if identifier_start.startswith(STEAM_PREFIX):
        return GameVersion.STEAM, 0

    # GOG-like
    found_address = process.pattern_scan_module(GOG_IDENTIFIER, process.process_base)
    if found_address is not None:
        return GameVersion.GOG, found_address - IDENTIFIER_ADDRESS

    # Steam-like
    found_address = process.pattern_scan_module(STEAM_IDENTIFIER, process.process_base)
    if found_address is not None:
        return GameVersion.STEAM, found_address - IDENTIFIER_ADDRESS

    return None, 0

# from https://github.com/icebound777/PMR-SeedGenerator/blob/dev_multiworld/util/multiworld_item_info_to_pmString.py
"""
Utility module for turning item info of multiworld items (from tools like
Archipelago) into formatted pmStrings, which can be used to overwrite
in-game item descriptions for item shop displays.
"""

from enum import IntEnum, unique
from BaseClasses import ItemClassification


@unique
class FormattingToken(IntEnum):
    END = 0
    LINEBREAK = 1
    SAVE_COLOR = 2
    RESTORE_COLOR = 3
    SET_COLOR = 4
    COLOR_RED = 5
    COLOR_CYAN = 6
    COLOR_BLUE = 7
    COLOR_PURPLE = 8
    COLOR_YELLOW = 9
    COLOR_NONE = 10


def multiworld_item_info_to_pmString(
    player_name: str,
    item_name: str,
    progression_type: ItemClassification,
    node_id: str,
) -> tuple[int, list[int]]:  # (rom_location, byte_list)
    """
    For the given data returns the translated byte list to write into the ROM
    to create a custom multiworld shop item description, as well as the ROM
    location to write this byte list to.
    If some of the provided data is too long to fit into a single line of
    item description, the data will be right-trimmed until it fits into the
    item description box.

    If an unsupported character is found within the player_name or item_name
    arguments, that character is simply ignored.
    If an unsupported progression_type is provided, no color change will be
    applied to the text of item_name.
    If the provided node_id does not correspond to any shop location defined
    in the seed generator, then the first value of returned tuple is set
    to -1. This is an error state.

    The returned byte_list represents an item description in the following
    scheme:

    player_name's
    item_name

    with item_name's text colored in accordance with the provided progression
    type.
    """
    assert isinstance(player_name, str)
    assert isinstance(item_name, str)
    assert isinstance(progression_type, ItemClassification) or isinstance(
        progression_type, int
    )
    assert isinstance(node_id, str)

    pmString: list[int] = []
    LINE_MAX_WIDTH: int = 600

    # Player name
    cur_line_width = 0
    # reserve space for the 's at the end
    cur_line_width += _get_char_width("'")
    cur_line_width += _get_char_width("s")

    for char in player_name:
        pmChar, pmChar_width = _char_to_pmChar(char)
        if cur_line_width + pmChar_width > LINE_MAX_WIDTH:
            break
        pmString.append(pmChar)
        cur_line_width += pmChar_width
    pmString.append(_char_to_pmChar("'")[0])
    pmString.append(_char_to_pmChar("s")[0])
    pmString.extend(_get_formatting_token(FormattingToken.LINEBREAK))

    # Item name
    cur_line_width = 0

    pmString.extend(_get_formatting_token(FormattingToken.SAVE_COLOR))
    pmString.extend(_get_formatting_token(FormattingToken.SET_COLOR))

    if (    ItemClassification.trap in progression_type
        and ItemClassification.progression in progression_type
    ):
        pmString.extend(_get_formatting_token(FormattingToken.COLOR_YELLOW))
    elif ItemClassification.progression in progression_type:
        pmString.extend(_get_formatting_token(FormattingToken.COLOR_PURPLE))
    elif ItemClassification.trap in progression_type:
        pmString.extend(_get_formatting_token(FormattingToken.COLOR_RED))
    elif ItemClassification.useful in progression_type:
        pmString.extend(_get_formatting_token(FormattingToken.COLOR_BLUE))
    elif ItemClassification.filler in progression_type:
        pmString.extend(_get_formatting_token(FormattingToken.COLOR_CYAN))
    else:  # fallback
        pmString.extend(_get_formatting_token(FormattingToken.COLOR_NONE))

    for char in item_name:
        pmChar, pmChar_width = _char_to_pmChar(char)
        if cur_line_width + pmChar_width > LINE_MAX_WIDTH:
            break
        if pmChar != 0:
            pmString.append(pmChar)
        cur_line_width += pmChar_width

    pmString.extend(_get_formatting_token(FormattingToken.RESTORE_COLOR))

    # Finish string
    pmString.extend(_get_formatting_token(FormattingToken.END))

    rom_location = _get_rom_location(node_id)

    return (rom_location, pmString)


def _char_to_pmChar(input_char: str) -> tuple[int, int]:
    """
    Returns the byte value used by Paper Mario for a given character, as well
    as its character width when printed into an item description box.
    If a character is not supported or recognized, instead (0, 0) will be
    returned.
    """
    char_byte_map: dict = {
        "0": 0x10,
        "1": 0x11,
        "2": 0x12,
        "3": 0x13,
        "4": 0x14,
        "5": 0x15,
        "6": 0x16,
        "7": 0x17,
        "8": 0x18,
        "9": 0x19,
        "A": 0x21,
        "B": 0x22,
        "C": 0x23,
        "D": 0x24,
        "E": 0x25,
        "F": 0x26,
        "G": 0x27,
        "H": 0x28,
        "I": 0x29,
        "J": 0x2A,
        "K": 0x2B,
        "L": 0x2C,
        "M": 0x2D,
        "N": 0x2E,
        "O": 0x2F,
        "P": 0x30,
        "Q": 0x31,
        "R": 0x32,
        "S": 0x33,
        "T": 0x34,
        "U": 0x35,
        "V": 0x36,
        "W": 0x37,
        "X": 0x38,
        "Y": 0x39,
        "Z": 0x3A,
        "a": 0x41,
        "b": 0x42,
        "c": 0x43,
        "d": 0x44,
        "e": 0x45,
        "f": 0x46,
        "g": 0x47,
        "h": 0x48,
        "i": 0x49,
        "j": 0x4A,
        "k": 0x4B,
        "l": 0x4C,
        "m": 0x4D,
        "n": 0x4E,
        "o": 0x4F,
        "p": 0x50,
        "q": 0x51,
        "r": 0x52,
        "s": 0x53,
        "t": 0x54,
        "u": 0x55,
        "v": 0x56,
        "w": 0x57,
        "x": 0x58,
        "y": 0x59,
        "z": 0x5A,
        " ": 0xF7,
        "!": 0x01,
        "?": 0x1F,
        "'": 0x07,
        ",": 0x0C,
        "-": 0x0D,
        ".": 0x0E,
        ":": 0x1A,
        "(": 0x3B,
        ")": 0x3D,
        "_": 0x3F,
    }

    if input_char in char_byte_map:
        return (char_byte_map[input_char], _get_char_width(input_char))
    else:
        return (0x00, 0)


def _get_char_width(input_char: str) -> int:
    """
    Returns an input_char's width when printed into an item description box.
    If the input_char is not recognized, return 0 instead.
    This width is more or less arbitrary and does not actually represent
    any tangible value used by Paper Mario's source code. Instead, these values
    are relative to an item description box's draw width, and are only supposed
    to help gauge how much space is left within the item description box.
    """
    char_width_map: dict = {
        "ABCDEFGHJKLMNOPQRSTUVWXYZadmpw023456789?_-": 22.3,  # fits ~27 times
        "bcefgkngnqrstuvxyz!()": 20,  # fits ~30 times
        "Ihjo1": 17.7,  # fits ~34 times
        " ,": 15,  # fits ~40 times
        ".:": 12.3,  # fits ~49 times
        "il'": 10,  # fits ~60 times
    }

    char_width = 0

    for char_list, width in char_width_map.items():
        if input_char in char_list:
            char_width = width
            break

    return char_width


def _get_formatting_token(input_formatting: FormattingToken) -> list[int]:
    """
    Returns a list of one or more bytes representing input_formatting in
    Paper Mario's message system as control characters and formatting tokens.
    """
    char_map: dict = {
        FormattingToken.END: [0xFD],
        FormattingToken.LINEBREAK: [0xF0],
        FormattingToken.SAVE_COLOR: [0xFF, 0x24],
        FormattingToken.RESTORE_COLOR: [0xFF, 0x25],
        FormattingToken.SET_COLOR: [0xFF, 0x05],
        FormattingToken.COLOR_RED: [0x07],
        FormattingToken.COLOR_PURPLE: [0x08],
        FormattingToken.COLOR_CYAN: [0x01],
        FormattingToken.COLOR_BLUE: [0x02],
        FormattingToken.COLOR_YELLOW: [0x05],
        FormattingToken.COLOR_NONE: [0x0A],
    }

    if input_formatting in char_map:
        return char_map[input_formatting]
    else:
        return list()


def _get_rom_location(node_id: str) -> int:
    """
    Returns the ROM location of a given node_id's shop item's multiworld string.
    If an invalid shop node_id is provided, returns -1 instead.
    """
    node_romoffset_map: dict = {
        # Toad Town - Shroom Grocery
        "MAC_00/ShopItemA": 0x1C7E5C8,  # ErrCode 24 181
        "MAC_00/ShopItemB": 0x1C7E64C,  # ErrCode 24 182
        "MAC_00/ShopItemC": 0x1C7E6D0,  # ErrCode 24 183
        "MAC_00/ShopItemD": 0x1C7E754,  # ErrCode 24 184
        "MAC_00/ShopItemE": 0x1C7E7D8,  # ErrCode 24 185
        "MAC_00/ShopItemF": 0x1C7E85C,  # ErrCode 24 186
        # Toad Town - Rowf
        "MAC_01/ShopBadgeA": 0x1C7E908,  # ErrCode 24 191
        "MAC_01/ShopBadgeB": 0x1C7E98C,  # ErrCode 24 192
        "MAC_01/ShopBadgeC": 0x1C7EA10,  # ErrCode 24 193
        "MAC_01/ShopBadgeD": 0x1C7EA94,  # ErrCode 24 194
        "MAC_01/ShopBadgeE": 0x1C7EB18,  # ErrCode 24 195
        "MAC_01/ShopBadgeF": 0x1C7EB9C,  # ErrCode 24 196
        "MAC_01/ShopBadgeG": 0x1C7EC20,  # ErrCode 24 197
        "MAC_01/ShopBadgeH": 0x1C7ECA4,  # ErrCode 24 198
        "MAC_01/ShopBadgeI": 0x1C7ED28,  # ErrCode 24 199
        "MAC_01/ShopBadgeJ": 0x1C7EDAC,  # ErrCode 24 19A
        "MAC_01/ShopBadgeK": 0x1C7EE30,  # ErrCode 24 19B
        "MAC_01/ShopBadgeL": 0x1C7EEB4,  # ErrCode 24 19C
        "MAC_01/ShopBadgeM": 0x1C7EF38,  # ErrCode 24 19D
        "MAC_01/ShopBadgeN": 0x1C7EFBC,  # ErrCode 24 19E
        "MAC_01/ShopBadgeO": 0x1C7F040,  # ErrCode 24 19F
        "MAC_01/ShopBadgeP": 0x1C7F0C4,  # ErrCode 24 1A0
        # Toad Town - Harry's shop
        "MAC_04/ShopItemA": 0x1C7F148,  # ErrCode 24 1A1
        "MAC_04/ShopItemB": 0x1C7F1CC,  # ErrCode 24 1A2
        "MAC_04/ShopItemC": 0x1C7F250,  # ErrCode 24 1A3
        "MAC_04/ShopItemD": 0x1C7F2D4,  # ErrCode 24 1A4
        "MAC_04/ShopItemE": 0x1C7F358,  # ErrCode 24 1A5
        "MAC_04/ShopItemF": 0x1C7F3DC,  # ErrCode 24 1A6
        # Star Haven
        "HOS_03/ShopItemA": 0x1C7F488,  # ErrCode 24 1B1
        "HOS_03/ShopItemB": 0x1C7F50C,  # ErrCode 24 1B2
        "HOS_03/ShopItemC": 0x1C7F590,  # ErrCode 24 1B3
        "HOS_03/ShopItemD": 0x1C7F614,  # ErrCode 24 1B4
        "HOS_03/ShopItemE": 0x1C7F698,  # ErrCode 24 1B5
        "HOS_03/ShopItemF": 0x1C7F71C,  # ErrCode 24 1B6
        # Merlow's
        "HOS_06/ShopBadgeA": 0x1C80B44,  # ErrCode 24 220
        "HOS_06/ShopBadgeB": 0x1C80BC8,  # ErrCode 24 221
        "HOS_06/ShopBadgeC": 0x1C80C4C,  # ErrCode 24 222
        "HOS_06/ShopBadgeD": 0x1C80CD0,  # ErrCode 24 223
        "HOS_06/ShopBadgeE": 0x1C80D54,  # ErrCode 24 224
        "HOS_06/ShopBadgeF": 0x1C80DD8,  # ErrCode 24 225
        "HOS_06/ShopBadgeG": 0x1C80E5C,  # ErrCode 24 226
        "HOS_06/ShopBadgeH": 0x1C80EE0,  # ErrCode 24 227
        "HOS_06/ShopBadgeI": 0x1C80F64,  # ErrCode 24 228
        "HOS_06/ShopBadgeJ": 0x1C80FE8,  # ErrCode 24 229
        "HOS_06/ShopBadgeK": 0x1C8106C,  # ErrCode 24 22A
        "HOS_06/ShopBadgeL": 0x1C810F0,  # ErrCode 24 22B
        "HOS_06/ShopBadgeM": 0x1C81174,  # ErrCode 24 22C
        "HOS_06/ShopBadgeN": 0x1C811F8,  # ErrCode 24 22D
        "HOS_06/ShopBadgeO": 0x1C8127C,  # ErrCode 24 22E
        "HOS_06/ShopRewardA": 0x1C81304,  # ErrCode 24 230
        "HOS_06/ShopRewardB": 0x1C81388,  # ErrCode 24 231
        "HOS_06/ShopRewardC": 0x1C8140C,  # ErrCode 24 232
        "HOS_06/ShopRewardD": 0x1C81490,  # ErrCode 24 233
        "HOS_06/ShopRewardE": 0x1C81514,  # ErrCode 24 234
        "HOS_06/ShopRewardF": 0x1C81598,  # ErrCode 24 235
        # Koopa Village
        "NOK_01/ShopItemA": 0x1C7F7C8,  # ErrCode 24 1C1
        "NOK_01/ShopItemB": 0x1C7F84C,  # ErrCode 24 1C2
        "NOK_01/ShopItemC": 0x1C7F8D0,  # ErrCode 24 1C3
        "NOK_01/ShopItemD": 0x1C7F954,  # ErrCode 24 1C4
        "NOK_01/ShopItemE": 0x1C7F9D8,  # ErrCode 24 1C5
        "NOK_01/ShopItemF": 0x1C7FA5C,  # ErrCode 24 1C6
        # Dry Dry Outpost
        "DRO_01/ShopItemA": 0x1C7FB08,  # ErrCode 24 1D1
        "DRO_01/ShopItemB": 0x1C7FB8C,  # ErrCode 24 1D2
        "DRO_01/ShopItemC": 0x1C7FC10,  # ErrCode 24 1D3
        "DRO_01/ShopItemD": 0x1C7FC94,  # ErrCode 24 1D4
        "DRO_01/ShopItemE": 0x1C7FD18,  # ErrCode 24 1D5
        "DRO_01/ShopItemF": 0x1C7FD9C,  # ErrCode 24 1D6
        # Boo's Mansion
        "OBK_03/ShopItemA": 0x1C7FE48,  # ErrCode 24 1E1
        "OBK_03/ShopItemB": 0x1C7FECC,  # ErrCode 24 1E2
        "OBK_03/ShopItemC": 0x1C7FF50,  # ErrCode 24 1E3
        "OBK_03/ShopItemD": 0x1C7FFD4,  # ErrCode 24 1E4
        "OBK_03/ShopItemE": 0x1C80058,  # ErrCode 24 1E5
        "OBK_03/ShopItemF": 0x1C800DC,  # ErrCode 24 1E6
        # Yoshi Village
        "JAN_03/ShopItemA": 0x1C80188,  # ErrCode 24 1F1
        "JAN_03/ShopItemB": 0x1C8020C,  # ErrCode 24 1F2
        "JAN_03/ShopItemC": 0x1C80290,  # ErrCode 24 1F3
        "JAN_03/ShopItemD": 0x1C80314,  # ErrCode 24 1F4
        "JAN_03/ShopItemE": 0x1C80398,  # ErrCode 24 1F5
        "JAN_03/ShopItemF": 0x1C8041C,  # ErrCode 24 1F6
        # Shiver City
        "SAM_02/ShopItemA": 0x1C804C8,  # ErrCode 24 201
        "SAM_02/ShopItemB": 0x1C8054C,  # ErrCode 24 202
        "SAM_02/ShopItemC": 0x1C805D0,  # ErrCode 24 203
        "SAM_02/ShopItemD": 0x1C80654,  # ErrCode 24 204
        "SAM_02/ShopItemE": 0x1C806D8,  # ErrCode 24 205
        "SAM_02/ShopItemF": 0x1C8075C,  # ErrCode 24 206
        # Bowser's Castle
        "KPA_96/ShopItemA": 0x1C80808,  # ErrCode 24 211
        "KPA_96/ShopItemB": 0x1C8088C,  # ErrCode 24 212
        "KPA_96/ShopItemC": 0x1C80910,  # ErrCode 24 213
        "KPA_96/ShopItemD": 0x1C80994,  # ErrCode 24 214
        "KPA_96/ShopItemE": 0x1C80A18,  # ErrCode 24 215
        "KPA_96/ShopItemF": 0x1C80A9C,  # ErrCode 24 216
    }

    if node_id in node_romoffset_map:
        return node_romoffset_map[node_id]
    else:
        return -1
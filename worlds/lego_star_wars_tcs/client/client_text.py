import re
import unicodedata
from typing import TypeVar

from BaseClasses import ItemClassification

from ..options import TextColorChoice
from ..slot_data import TCSSlotDataOptions


STR = TypeVar("STR", str, bytes)


# I have no idea how these colors are determined, or whether some of these colors are just reading memory beyond their
# intended bounds.
# Note that all values need to be only 1 byte when encoded in utf-8 if the code for adding colors to text is to support
# string formatting. Values that encode to more than 1 byte (value >= 0x80) can be supported, but color formatting codes
# would have to always be added after strings have been converted to bytes, or all conversion steps from str to bytes
# would need to parse color formatting codes.
# ~{color}{text to color}~~
COLOR_FORMATTING = {
    # "black": "\x01",  # 000000, almost unreadable due to the black outlines.
    # "deep_blue": "\x02",  # 0000FF
    # "dark_blue": "\x03",  # 00007E
    # "black": "\x04",
    # "black": "\x05",
    # "blue": "\x06",
    # "dark_blue": "\x07",

    # "???": "\x08",  # Unstable. Changes on each run.
    # "???": "\x09",  # Unstable. Changes on each run.
    # "???": "\x0A",  # Unstable. Value has been seen to change, but less frequently than the previous two.
    "red_pink": "\x0B",  # FF007E
    "darker_red": "\x0C",  # 640000
    # "black": "\x0D",

    # "cyan": "\x0E",  # 00FFFF
    # "dark_cyan": "\x0F",  # 007E7E
    # "black": "\x10",
    # "black": "\x11",
    # "cyan_with_brighter_outlines": "\x12",  # 00FFFF, but the outlines are brighter and more blue
    "dark_cyan": "\x13",  # 007E7E
    "purple": "\x14",  # 6E00DE
    # "very_dark_blue": "\x15",  # 000024, almost unreadable
    "blue": "\x16",  # 007EFF
    "dark_sea_green": "\x17",  # 007E76
    # "blue": "\x18",
    # "blue": "\x19",
    # "yellow": "\x1A",  # FFFF00
    "dark_yellow": "\x1B",  # 7E7E00
    # "black": "\x1C",
    # "blue": "\x1D",
    "white_green_outline": "\x1E",  # FFFFFF, but with a green outline
    "light_blue_purple": "\x1F",  # 7E7EFF

    # Characters before here are not printable, so I think are more likely to not be consistent, and are more likely to
    # be reading some unexpected part of memory.
    # "bright_green": "\x20",  # 00FF00
    # "very_dark_green": "\x21",  # 002400, more readable than very_dark_blue, but still bad
    "pea_green": "\x22",  # 80FF00
    # "dark_yellowy_orange": "\x23",  # 7E7600, dark_gold is too similar
    # "cyan": "\x24",
    # "green": "\x25",  # 00FF00
    # "magenta": "\x26",  # FF00FF
    "dark_red": "\x27",  # 7E0000, maybe a little dark to be "red"
    # "deep_blue": "\x28",
    # "bright_green": "\x29",
    "white_red_outline": "\x2a",  # FFFFFF, but with a red outline
    "mint_green": "\x2b",  # 7EFFC0
    "red": "\x2c",  # DE0000, matches in LB1
    # "very_dark_red": "\x2d",  # 240000, more readable than very_dark_blue, but still bad, matches in LB1
    # "bright_red": "\x2e",  # FF0000, matches in LB1
    # "dark_red_2": "\x2f",  # 760000, slightly darker than dark_red, matches in LB1.

    # The 0x30 to 0x39 range are most likely those that are actually intended for use because they are the characters
    # 0-9.
    "white": "\x30",  # FFFFFF
    "bright_red": "\x31",  # FF0000
    "bright_green": "\x32",  # 00FF00
    "deep_blue": "\x33",  # 0000FF
    "cyan": "\x34",  # 00FFFF
    "magenta": "\x35",  # FF00FF
    "yellow": "\x36",  # FFFF00
    "orange": "\x37",  # FFC000, orange is a commonly used color by the game for general text.
    "black": "\x38",  # 000000, almost unreadable.
    # "black": "\x39",
    # "black": "\x3A",
    # "black": "\x3B",
    # "almost_white": "\x3C",  # FFFFFE. Yellow in LB1
    # "deep_blue": "\x3D",  # 0000FF
    # "almost_magenta": "\x3E",  # FF00FE. Red in LB1
    # "cyan": "\x3F",
    # "almost_yellow": "\x40",  # FFFF02
    # "green": "\x41",
    # "bright_red": "\x42",
    # "dark_red2": "\x43",  # C00000

    "dark_blue": "\x47",  # 00007E
    "pale_yellow": "\x4b",  # FFFF7E
    "dark_green": "\x53",  # 007E00
    "near_white_yellow": "\x56",  # FEFFEA
    "dark_orange": "\x57",  # FF7E00
    # "dark_red": "\x5f",  # 7E0000
    "overbrightened_white": "\x64",  # FFFFFF but the outlines are brighter

    # These are above 0x80, so cannot be used without adjusting how the formatting codes are added into strings because
    # utf-8 encoding uses two bytes for them.
    # "sea_green": "\xa3",  # 007E7E
    # "dark_yellow": "\xaf",  # 7E7E00
    # "dark_pink": "\xc3",  # 7E007E
    # "grey": "\xcb",  # 7E7E7E
    # "gray": "\xcb",  # 7E7E7E
    # "brighter_purple": "\xdb",  # 7E00FF
    # "blue": "\xff",  # 007EFF
    # "black2": "9",
    # "cyan2": "a",  # Cyan text and cyan outline?
    # "cyan3": "\\",  # Cyan text and cyan outline?
}


USABLE_CHARACTERS = set(
    # No ".
    # No $ because it becomes a checkmark/tick like would be seen in a checkbox.
    " !#%&'()*+,-./"
    "0123456789"
    ":;<=>?@"
    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    "[\\]^_`"
    "abcdefghijklmnopqrstuvwxyz"
    # No | because it becomes the R1 Button.
    # No ~ because it is used for color formatting and symbol replacement.
    "{}"
    # These both display as "'" for some reason. Ignoring them for now.
    # "\x91\x92"
    "¡©®²´º¿"
    "ÀÁÃÄÅÆÈÉÍÏÑÓØÙÚÜßàáâãäåæçèéêëìíîïñòóôöøùúüĄąĆćĘęŁłńœŚśźŻż"
    "’“”…™"
    # No Ъ. я seems to become a special - sometimes, I'm not sure how it works.
    "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюя"
)


# These characters become special symbols.
_SYMBOLS = {
    "R1 Button": "|",  # 124
    "L1 Button": "¶",  # 182
    "Square Button": "û",  # 251
    "X Button": "ý",  # 253
    "Circle Button": "þ",  # 254
    "Triangle Button": "ÿ",  # 255
}


_REPLACEMENTS = {
    "Đ": "D",
    "Ħ": "H",
    "Ŀ": "L",
    "Ŋ": "N",
    "Œ": "OE",
    "Ŧ": "T",
    "Ð": "TH",
    "¢": "c",
    "đ": "d",
    "ħ": "h",
    "ı": "i",
    "ĸ": "k",
    "ŀ": "l",
    "ŋŉ": "n",
    "Þðþ": "th",
    "×χ˟": "x",
    # " does not exist for some reason, so replace it with "“".
    '"': "“",
    # $ becomes a checkmark/tick like would be seen in a checkbox.
    # £ becomes a down arrow, like how < and > become left and right arrows.
    # € is not supported.
    # ~ is used as a special character for formatting.
    # ¤ becomes a down arrow with a tail, like ↓.
    # ¬ becomes an up arrow with a tail.
    # ѐ becomes a "-"
    # Symbols: |¶ûýþÿ
    "$£€~¤ѐ" + "".join(_SYMBOLS.values()): "?",
    "‘": "'",
    "‚": ",",
    "Ω": "?",
    "˂": "<",
    "˃": ">",
    "˄": "^",
    "˅": "¤",
    "Ъ": "Ь",
    "♥": "<3",
}
REPLACEMENTS = {c: v for k, v in _REPLACEMENTS.items() for c in k}


# Development helper to check if any explicit replacements would get replaced automatically using `unicodedata`.
# for k, expected_v in REPLACEMENTS.items():
#     normalized_nfkd = unicodedata.normalize("NFKD", k)
#     normalized_no_combining_characters = "".join(c2 for c2 in normalized_nfkd
#                                                  if unicodedata.category(c2) != "Mn")
#     if normalized_no_combining_characters == expected_v:
#         print(f"Do not need to handle: '{k}'")


def clean_string(s: str) -> str:
    """Clean up a string to be displayed in-game."""
    # Double [[<special value>]] gets replaced with an icon or similar through _TextDecodeCodeword(). e.g. "[[start]]"
    # becomes a 'start button'.
    s = re.sub(r"\[\[+", "[", s)
    s = re.sub(r"]]+", "]", s)
    if any(unicodedata.category(c) == "Mn" for c in s):
        # Combine combining characters with their base character if possible, e.g. "e"+"́" ("é") -> "é".
        # This can mess with other characters in ways we don't want, so it is only run when a combining character is
        # found, which should be very rare.
        s = unicodedata.normalize("NFKC", s)
    to_convert = list(reversed(s))
    initial_length = len(s)
    characters = []
    while to_convert:
        c = to_convert.pop()
        if c in USABLE_CHARACTERS:
            # The character can be used as-is.
            characters.append(c)
        elif c in REPLACEMENTS:
            # The character has a hardcoded replacement, which could be more than one character.
            characters.extend(REPLACEMENTS[c])
        else:
            # Turn characters with diacritics into the base character plus a combining diacritic character(s).
            normalized_nfkd = unicodedata.normalize("NFKD", c)
            if len(normalized_nfkd) == 1:
                # If the single character did not become more than one character, then there were no combining
                # characters.
                characters.append("?")
            else:
                # Remove all combining characters.
                normalized_no_combining_characters = "".join(c2 for c2 in normalized_nfkd
                                                             if unicodedata.category(c2) != "Mn")
                # Warning: If there is a character that repeatedly produces the same extra character over and over, then
                # this could loop infinitely.
                to_convert.extend(reversed(normalized_no_combining_characters))
                if len(characters) > (2 * initial_length):
                    # Abort to prevent infinite loops.
                    return s
    return "".join(characters)


class ClientText:
    _prog_useful_color: str = COLOR_FORMATTING["yellow"]
    _prog_useful_color_b: bytes = _prog_useful_color.encode("utf-8")
    _progression_color: str = COLOR_FORMATTING["purple"]
    _progression_color_b: bytes = _progression_color.encode("utf-8")
    _useful_color: str = COLOR_FORMATTING["blue"]
    _useful_color_b: bytes = _useful_color.encode("utf-8")
    _filler_color: str = COLOR_FORMATTING["cyan"]
    _filler_color_b: bytes = _filler_color.encode("utf-8")
    _trap_color: str = COLOR_FORMATTING["red"]
    _trap_color_b: bytes = _trap_color.encode("utf-8")
    _player_color: str = COLOR_FORMATTING["near_white_yellow"]
    _player_color_b: bytes = _player_color.encode("utf-8")
    _location_color: str = COLOR_FORMATTING["pea_green"]
    _location_color_b: bytes = _location_color.encode("utf-8")

    def prog_useful(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._prog_useful_color}{s}~~"
        else:
            return b"~" + self._prog_useful_color_b + s + b"~~"

    def progression(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._progression_color}{s}~~"
        else:
            return b"~" + self._progression_color_b + s + b"~~"

    def useful(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._useful_color}{s}~~"
        else:
            return b"~" + self._useful_color_b + s + b"~~"

    def filler(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._filler_color}{s}~~"
        else:
            return b"~" + self._filler_color_b + s + b"~~"

    def trap(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._trap_color}{s}~~"
        else:
            return b"~" + self._trap_color_b + s + b"~~"

    def player_name(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._player_color}{s}~~"
        else:
            return b"~" + self._player_color_b + s + b"~~"

    def location_name(self, s: STR) -> STR:
        if isinstance(s, str):
            return f"~{self._location_color}{s}~~"
        else:
            return b"~" + self._location_color_b + s + b"~~"

    def from_classification(self, classification: ItemClassification, s: STR) -> STR:
        if (ItemClassification.progression | ItemClassification.useful) in classification:
            return self.prog_useful(s)
        elif ItemClassification.progression in classification:
            return self.progression(s)
        # Whether a Useful + Trap item should show up as Useful or Trap color is questionable.
        elif ItemClassification.trap in classification:
            return self.trap(s)
        elif ItemClassification.useful in classification:
            return self.useful(s)
        else:
            return self.filler(s)

    @staticmethod
    def from_text_color_choice(text_color_choice: TextColorChoice, s: STR) -> STR:
        format_str = COLOR_FORMATTING[text_color_choice.current_key_no_hex_value]
        if isinstance(s, str):
            return f"~{format_str}{s}~~"
        else:
            return b"~" + format_str.encode("utf-8") + s + b"~~"

    @classmethod
    def from_slot_data(cls, slot_data: TCSSlotDataOptions):
        self = cls()
        item_colors = slot_data.item_colors.value
        (
            prog_useful_color,
            progression_color,
            useful_color,
            filler_color,
            trap_color,
            player_color,
            location_color,
        ) = (COLOR_FORMATTING[s] for s in TextColorChoice.colors_from_slot_data(list(item_colors)))

        self._prog_useful_color = prog_useful_color
        self._prog_useful_color_b = prog_useful_color.encode()
        self._progression_color = progression_color
        self._progression_color_b = progression_color.encode()
        self._useful_color = useful_color
        self._useful_color_b = useful_color.encode()
        self._filler_color = filler_color
        self._filler_color_b = filler_color.encode()
        self._trap_color = trap_color
        self._trap_color_b = trap_color.encode()
        self._player_color = player_color
        self._player_color_b = player_color.encode()
        self._location_color = location_color
        self._location_color_b = location_color.encode()
        return self

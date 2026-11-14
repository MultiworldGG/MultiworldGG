from enum import IntEnum, auto

from ..rom import Rom
from ..text import Language, MessageType, encode_text
from .constants.game_data import message_text_addr, story_text_addr

INTRO_TEXT_ID = 0

# Keep this in sync with MessageId in constants/text.h
HINT_MESSAGE_ID_START = 44


class HintStatue(IntEnum):
    LONG_BEAM = 0
    ICE_BEAM = auto()
    WAVE_BEAM = auto()
    BOMBS = auto()
    SPEED_BOOSTER = auto()
    HI_JUMP = auto()
    SCREW_ATTACK = auto()
    VARIA_SUIT = auto()


def write_intro_text(rom: Rom, data: dict) -> None:
    for lang, text in data.items():
        lang = Language[lang]
        base_text_addr = rom.read_ptr(story_text_addr(rom) + lang.value * 4)
        text_ptr = base_text_addr + INTRO_TEXT_ID * 4
        encoded_text = encode_text(rom, MessageType.CONTINUOUS, text)
        rom.write_data_with_pointers(encoded_text, [text_ptr])


def write_hint_text(rom: Rom, data: dict) -> None:
    for lang, hints in data.items():
        lang = Language[lang]
        base_text_addr = rom.read_ptr(message_text_addr(rom) + lang.value * 4)
        for hint, text in hints.items():
            hint = HintStatue[hint]
            encoded_text = encode_text(rom, MessageType.TWO_LINE, text, centered=True)
            msg_id = HINT_MESSAGE_ID_START + hint.value
            text_ptr = base_text_addr + msg_id * 4
            rom.write_data_with_pointers(encoded_text, [text_ptr])

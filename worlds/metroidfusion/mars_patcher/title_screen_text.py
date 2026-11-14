from .mf import auto_generated_types as mf_types
from .zm import auto_generated_types as zm_types
from .constants.game_data import title_text_addr
from .mf.constants.reserved_space import ReservedPointersMF
from .rom import Rom

TitleTextItem = mf_types.MarsschemamfTitleTextItem | zm_types.MarsschemazmTitleTextItem

TITLE_TEXT_POINTER_ADDR = ReservedPointersMF.TITLE_SCREEN_TEXT_POINTERS_POINTER_ADDR.value
MAX_LENGTH = 30
MAX_LINE_NUM = 20


def write_title_text(rom: Rom, lines: list[TitleTextItem]) -> None:
    seen_lines: set[int] = set()
    line_ptrs = title_text_addr(rom)

    for line in lines:
        line_num = line["line_num"]
        if line_num in seen_lines:
            raise ValueError(f"Title screen text line {line_num} already provided")
        seen_lines.add(line_num)

        text = line["text"]
        if len(text) > MAX_LENGTH:
            raise ValueError(f'Title screen text line exceeds {MAX_LENGTH} characters\n"{text}"')

        if rom.is_zm():
            text += "\0"
        addr = rom.read_ptr(line_ptrs + (line_num * 4))
        rom.write_bytes(addr, text.encode("ascii"))

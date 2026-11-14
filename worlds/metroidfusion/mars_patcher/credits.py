from .constants.credits import (
    LINE_TYPE_HEIGHTS,
    TEXT_LINE_TYPES,
    LineType,
)
from .mf.auto_generated_types import MarsschemamfCreditsTextItem
from .rom import Rom
from .zm.auto_generated_types import MarsschemazmCreditsTextItem

CreditsTextItem = MarsschemamfCreditsTextItem | MarsschemazmCreditsTextItem

FULL_LINE_LEN = 36
LINE_WIDTH = 30


class CreditsLine:
    def __init__(
        self,
        line_type: LineType,
        blank_lines: int = 0,
        text: str | None = None,
        centered: bool = True,
    ):
        self.line_type = line_type
        self.blank_lines = blank_lines
        self.text = text
        self.centered = centered

    @classmethod
    def from_json(cls, data: CreditsTextItem) -> "CreditsLine":
        line_type = LineType[data["line_type"]]
        blank_lines = data.get("blank_lines", 0)
        text = data.get("text")
        centered = data.get("centered", True)
        return CreditsLine(line_type, blank_lines, text, centered)


class CreditsWriter:
    def __init__(self, rom: Rom):
        self.rom = rom
        self.data = bytearray()
        self.num_lines = 0

    def write_lines(self, lines: list[CreditsLine]) -> None:
        for line in lines:
            line_data = bytearray([line.line_type.value])
            if self.rom.is_mf():
                line_data.append(line.blank_lines)
            if line.line_type in TEXT_LINE_TYPES and line.text:
                text = line.text
                if self.rom.is_mf() and line.centered:
                    spacing = " " * ((LINE_WIDTH - len(text)) // 2)
                    text = spacing + text
                line_data.extend(text.encode("ascii"))

            # Write line data
            if len(line_data) > FULL_LINE_LEN:
                raise ValueError(f"Line too long: {text}")
            self.data += line_data
            remainder = FULL_LINE_LEN - len(line_data)

            # Fill remainder of line with 0
            self.data.extend([0] * remainder)

            # Add blank lines
            if self.rom.is_zm():
                for _ in range(line.blank_lines):
                    self.data.append(LineType.BLANK.value)
                    self.data.extend([0] * (FULL_LINE_LEN - 1))

            # Update the total number of lines
            line_height = LINE_TYPE_HEIGHTS.get(line.line_type, 0)
            self.num_lines += line_height + line.blank_lines


def get_credits_size(rom: Rom, addr: int) -> int:
    start = addr
    while True:
        line_type = rom.read_8(addr)
        addr += FULL_LINE_LEN
        if line_type == LineType.END:
            break
    return addr - start

from enum import IntEnum


class LineType(IntEnum):
    BLUE = 0
    RED = 1
    WHITE_BIG = 2
    WHITE = 3
    BLANK = 5
    END = 6
    COPYRIGHT1 = 10
    COPYRIGHT2 = 11
    COPYRIGHT3 = 12
    COPYRIGHT4 = 13


LINE_TYPE_HEIGHTS = {
    LineType.BLUE: 1,
    LineType.RED: 1,
    LineType.WHITE_BIG: 2,
    LineType.WHITE: 1,
    LineType.BLANK: 1,
    LineType.END: 0,
    LineType.COPYRIGHT1: 1,
    LineType.COPYRIGHT2: 1,
    LineType.COPYRIGHT3: 1,
    LineType.COPYRIGHT4: 1,
}

TEXT_LINE_TYPES = {LineType.BLUE, LineType.RED, LineType.WHITE, LineType.WHITE_BIG}

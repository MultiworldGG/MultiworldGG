from ....common.patching.z80asm.Assembler import Z80Assembler
from ..hide_and_seek import free_hns_data_space, randomize_hns_pattern
from ..hide_and_seek_data import Direction, MoveDirection

disabled_hns_data = [
    [
        # First screen
        {
            "start": 0x72,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Down, 0x20),
            ],
        },
        {
            "start": 0x74,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Down, 0x20),
            ],
        },
    ],
    [
        # Second screen
        {
            "start": 0x64,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x30),
            ],
        },
        {
            "start": 0x74,
            "start_angle": Direction.Down,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Down, 0x20),
            ],
        },
    ],
    [
        # Third screen
        {
            "start": 0x20,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x20),
            ],
        },
        {
            "start": 0x40,
            "start_angle": Direction.Left,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Left, 0x20),
            ],
        },
    ],
    [
        # Fourth screen
        {
            "start": 0x02,
            "start_angle": Direction.Up,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Up, 0x20),
            ],
        },
        {
            "start": 0x06,
            "start_angle": Direction.Up,
            "moves": [
                (MoveDirection.Wait, 60),
                (MoveDirection.Up, 0x20),
            ],
        },
    ],
]


def disable_hns(assembler: Z80Assembler) -> None:
    free_hns_data_space(assembler)
    for i in range(1, 5):
        randomize_hns_pattern(assembler, i, disabled_hns_data[i - 1])

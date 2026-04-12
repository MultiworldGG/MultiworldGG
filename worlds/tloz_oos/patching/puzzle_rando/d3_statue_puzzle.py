import random


def randomize_d3_statue_puzzle(room_data: list[bytearray]) -> None:
    room = room_data[0x558]

    # I don't have much more elegant, so here's an hardcoded list of all valid configurations for the puzzle
    # We skip the first and last element, since they cannot go anywhere but down
    chosen_config = random.choice([
        (0x2c, 0x2c, 0x2d, 0x2d), # Trivial
        (0x2c, 0x2d, 0x2c, 0x2d),
        (0x2c, 0x2d, 0x2d, 0x2c), # Vanilla
        (0x2d, 0x2c, 0x2c, 0x2d), # Vanilla mirrored
        # (0x2d, 0x2c, 0x2d, 0x2c), Don't think that one is possible
        (0x2d, 0x2d, 0x2c, 0x2c), # That one is delicate as you need to push a block UP
    ])

    room[0x75:0x79] = chosen_config
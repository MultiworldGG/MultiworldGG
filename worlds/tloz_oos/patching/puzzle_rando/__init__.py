from typing import Any

from .d3_statue_puzzle import randomize_d3_statue_puzzle
from .d7_armos_puzzle import randomize_d7_armos_puzzle
from .d8_ice_puzzle import randomize_d8_ice_puzzle
from .dance_rando import randomize_dance
from .hide_and_seek import randomize_hns
from ...common.patching.RomData import RomData
from ...common.patching.z80asm.Assembler import Z80Assembler


def randomize_puzzles(rom: RomData, assembler: Z80Assembler, room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    if not patch_data["options"]["randomize_puzzles"]:
        return
    randomize_dance(rom)
    randomize_hns(assembler)
    randomize_d3_statue_puzzle(room_data)
    randomize_d7_armos_puzzle(rom, assembler, room_data)
    randomize_d8_ice_puzzle(room_data)

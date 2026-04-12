import random

from ...common.patching.RomData import RomData
from ...common.patching.z80asm.Assembler import GameboyAddress


def randomize_dance(rom: RomData) -> None:
    rom.write_bytes(GameboyAddress(0x09, 0x5ed1).address_in_rom(), random.choices(range(3), k=4) * 4)  # The low sample makes sure this has an impact

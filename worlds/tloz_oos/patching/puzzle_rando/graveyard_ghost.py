import random

from ...common.patching.RomData import RomData
from ...common.patching.z80asm.Assembler import GameboyAddress


def randomize_ghini(rom: RomData, texts: dict[str, str]) -> None:
    # Tables are at 0F:7C9E, 0F:7CAE and 0F:7CBE

    if random.randint(0, 1) == 0:
        # Odd
        texts["TX_4c15"] = texts["TX_4c15"].replace("there were more", "had an odd count")
        texts["TX_4c17"] = texts["TX_4c17"].replace("were there more\nof, ", "was the odd,\n")

        rom.write_bytes(GameboyAddress(0x0F, 0x7C9E).address_in_rom(),
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0])
        rom.write_bytes(GameboyAddress(0x0F, 0x7CAE).address_in_rom(),
                        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        rom.write_bytes(GameboyAddress(0x0F, 0x7CBE).address_in_rom(),
                        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0])

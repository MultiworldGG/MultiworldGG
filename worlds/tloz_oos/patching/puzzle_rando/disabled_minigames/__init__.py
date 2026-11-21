from ....common.patching.RomData import RomData
from ....common.patching.z80asm.Assembler import GameboyAddress, Z80Assembler
from .hide_and_seek import disable_hns


def disable_minigames(rom: RomData, assembler: Z80Assembler) -> None:
    disable_hns(assembler)
    rom.write_word_be(GameboyAddress(0x09, 0x5C12).address_in_rom(), 0xCF5D)  # Skip dance
    rom.write_word_be(GameboyAddress(0x0B, 0x7DF1).address_in_rom(), 0x7E53)  # Skip linked game swimming challenge
    rom.write_word(GameboyAddress(0x0B, 0x7C31).address_in_rom(), 0x7C83)  # Skip ghini minigame

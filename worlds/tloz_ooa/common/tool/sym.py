import os

from ..patching.Util import simple_hex
from ..patching.z80asm.Assembler import GameboyAddress, Z80Assembler


def make_sym(assembler: Z80Assembler):
    """"
    Creates a symbol (.sym) file from a Gameboy ROM

    Parameters:
        assembler (Z80Assembler): The assembler used for the building of the symbol file.
    """
    if not os.path.isdir("output"):
        os.mkdir("output")

    with open("output/oracleGame.sym", "w+", encoding="utf-8") as f:
        for label in assembler.global_labels:
            address: GameboyAddress = assembler.global_labels[label]
            f.write(f"{simple_hex(address.bank)}:{address.to_word()[1:]} {label}\n")
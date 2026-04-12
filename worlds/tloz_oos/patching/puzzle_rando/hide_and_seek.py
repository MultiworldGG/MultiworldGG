import random

from ...common.patching.Util import script_delay, simple_hex
from ...common.patching.z80asm.Assembler import Z80Assembler, Z80Block
from ..puzzle_rando.hide_and_seek_data import hide_and_seek_data


def randomize_hns_pattern(assembler: Z80Assembler, screen: int):
    screen_data = list(hide_and_seek_data[screen - 1])
    random.shuffle(screen_data)
    # Maybe check if the patterns don't collide later

    for brother in range(1, 3):
        header_name = f"brother{brother}_screen{screen}"
        pattern_header = ("db jumptable_memoryaddress\n"
                          "dw $cfd0\n"
                          f"dw {header_name}_pattern1\n"
                          f"dw {header_name}_pattern2\n")
        for pattern in range(1, 3):
            current_pattern = screen_data.pop()
            pattern_code = (f"db setcoords,${current_pattern['start'] // 0x10}8,${current_pattern['start'] % 0x10}8\n"
                            f"db setangleandanimation,${simple_hex(current_pattern['start_angle'])}\n")
            pattern_name = f"{header_name}_pattern{pattern}"
            if brother == 1:
                if screen == 1:
                    pattern_code += ("db callscript\n"
                                     "dw $67dd\n")  # Start dialogue
                else:
                    pattern_code += ("db asm15\n"
                                     "dw $5e4e\n")  # subrosianHiding_createDetectionHelper
                pattern_label = f"0b//{pattern_name}"
            else:
                if screen == 1:
                    pattern_code += ("db callscript\n"
                                     "dw $67f4\n")
                else:
                    pattern_code += ("db asm15\n"
                                     "dw $5e4e\n")  # subrosianHiding_createDetectionHelper
                pattern_code += ("db loadscript,$14\n"
                                 f"dw {pattern_name}_script\n")

                assembler.add_block(Z80Block(f"0b//{pattern_name}", pattern_code))
                pattern_code = ""
                pattern_label = f"14//{pattern_name}_script"
            for move in current_pattern["moves"]:
                if isinstance(move, int):
                    if move < 0x100:  # Look somewhere
                        pattern_code += f"db setangleandanimation,${simple_hex(move)}\n"
                    else:  # Look in few places
                        pattern_code += ("db callscript\n"
                                         f"dw ${simple_hex(move, 4)}\n")
                else:  # tuple
                    if move[0] == 0:  # Wait
                        pattern_code += script_delay(move[1])
                    else:
                        pattern_code += f"db ${simple_hex(move[0])},${simple_hex(move[1])}\n"
            pattern_code += f"db ${simple_hex(0xa7 + brother)},scriptend\n"  # 0xa7 + brother is the appropriate xorcfc0bit
            assembler.add_block(Z80Block(pattern_label, pattern_code))
        assembler.add_block(Z80Block(f"0b//{header_name}", pattern_header))


def randomize_hns(assembler: Z80Assembler) -> None:
    assembler.bank_caves[0x0b].insert(0, [0x27a1, 0x27dc])
    assembler.bank_caves[0x0b].insert(0, [0x27fd, 0x296d])
    assembler.bank_caves[0x0b].insert(0, [0x2990, 0x29f9])
    assembler.bank_caves[0x14].insert(0, [0x0f51, 0x10c9])
    for i in range(1, 5):
        randomize_hns_pattern(assembler, i)

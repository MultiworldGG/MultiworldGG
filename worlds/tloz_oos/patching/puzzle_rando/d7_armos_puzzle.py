import random

from ...common.patching.RomData import RomData
from ...common.patching.z80asm.Assembler import GameboyAddress, Z80Assembler


def randomize_d7_armos_puzzle(rom: RomData, assembler: Z80Assembler, room_data: list[bytearray]) -> None:
    room = room_data[0x635]

    # Empty the room
    room[0x17] = 0xa0
    room[0x32] = 0xa0
    room[0x35] = 0xa3
    room[0x37] = 0xa3
    room[0x3b] = 0xa0
    room[0x52] = 0xa0
    room[0x57] = 0xa2
    room[0x59] = 0xa3
    room[0x5b] = 0xa0
    room[0x79] = 0xa3
    room[0x95] = 0xa0
    room[0x97] = 0xa0

    armoses = [0x35, 0x37, 0x39, 0x55, 0x59, 0x75, 0x77, 0x79]
    buttons = random.sample(range(5), k=4) # Up left, Middle left, Bottom left, Bottom middle and Bottom right
    for button_id in range(3, -1, -1):
        button = buttons[button_id]
        if button < 2: # Left button
            for i in range(len(armoses)):
                if armoses[i] // 0x10 == button * 2 + 3:
                    armoses[i] += 0x02

        else: # Bottom button
            for i in range(len(armoses)):
                if armoses[i] % 0x10 == (button - 2) * 2 + 5:
                    armoses[i] -= 0x20

    under_armos = []
    for armos in armoses:
        under_armos.append(armos)
        under_armos.append(room[armos])
        room[armos] = 0x27
    under_armos.append(0x00)
    assembler.add_floating_chunk("under_armos", under_armos)

    button_positions = [0x32, 0x52, 0x95, 0x97, 0x99]
    button_part_address = GameboyAddress(0x11, 0x52ac).address_in_rom()
    behavior_addresses = [
        GameboyAddress(0x09, 0x565c).address_in_rom(),
        GameboyAddress(0x09, 0x564a).address_in_rom(),
        GameboyAddress(0x09, 0x5638).address_in_rom(),
        GameboyAddress(0x09, 0x5626).address_in_rom(),
    ]
    for button in buttons:
        button_position = button_positions[button]
        room[button_position] = 0x0c
        rom.write_byte(button_part_address, button_position)
        button_part_address += 3

        behavior_address = behavior_addresses.pop()
        rom.write_byte(behavior_address, button_position)
        if button < 2:
            function = 0x5694 # Horizontal shift
        else:
            function = 0x56a5 # Vertical shift
        rom.write_word(behavior_address + 2, function)
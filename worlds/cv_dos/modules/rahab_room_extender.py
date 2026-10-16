from typing import NamedTuple


class BossRoomData(NamedTuple):
    layer_pointer: int  # Pointer to where layer data is stored
    room_pointer: int  # Raw pointer of the room's tile data
    entity_end: int  # End of this room's entity list
    file: str  # Which file this room is in
    base_tile: int = 0x00  # Tile to replace floor with. Defaults to blank tile
    one_tile_wall: bool = False  # Whether or not this room's walls are only 1 tile thick


room_data = {
    "Lost Village": BossRoomData(0x022E24A9, 0x2EAC18, 0x020A110C, "overlay_14"),
    "Dark Chapel": BossRoomData(0x022E508D, 0x2563FC, 0x020AEB94, "overlay_8", 0x021B),
    "Dark Chapel Inner": BossRoomData(0x022E475D, 0x255ACC, 0x020AEB10, "overlay_8"),
    "Garden of Madness": BossRoomData(0x022E27BD, 0x315B2C, 0x020AC518, "overlay_16", 0x00, True),
    "Demon Guest House": BossRoomData(0x022DF6F1, 0x2A6460, 0x020A56FC, "overlay_11", 0x05, True),
    "Cursed Clock Tower": BossRoomData(0x022EA985, 0x2750F4, 0x020B8DD0, "overlay_9"),
    "The Pinnacle": BossRoomData(0x022DC961, 0x286ED0, 0x020BADE0, "overlay_10", 0x4E, True),
    "Mine of Judgment": BossRoomData(0x022EF921, 0x23EC90, 0x020B236C, "overlay_7")
}

# Byte sequences of tiles that make up a valid segment of wall.
# This is not any existing graphics or room data, I patterned these using available tiles to use the minimum data
# necessary to still look decent.
byte_sequences = {
    "Lost Village": bytes.fromhex("""AD 01 19 01 19 01 19 01 19 01 19 01 19 01 19 01
                                     19 01 19 01 19 01 19 01 19 01 19 01 19 01 19 01
                                     19 01 19 01 19 01 19 01 19 01 19 01 19 01 19 01
                                     19 01 19 01 19 01 19 01 19 01 19 01 AD 41 5A 42
                                     BD 01 19 01 19 01 19 01 19 01 19 01 19 01 19 01
                                     19 01 19 01 19 01 19 01 19 01 19 01 19 01 19 01
                                     19 01 19 01 19 01 19 01 19 01 19 01 19 01 19 01
                                     19 01 19 01 19 01 19 01 19 01 19 01 BD 41 2A 42"""),

    "Dark Chapel": bytes.fromhex("""E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41
                                    E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                    1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41"""),

    "Dark Chapel Inner": bytes.fromhex("""E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41
                                          E0 01 A0 C1 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 1B 02
                                          1B 02 1B 02 1B 02 1B 02 1B 02 1B 02 A0 81 E0 41"""),

    "Garden of Madness": bytes.fromhex("""67 00 60 01 60 01 60 01 60 01 60 01 60 01 60 01
                                          60 01 60 01 60 01 60 01 60 01 60 01 60 01 60 01
                                          60 01 60 01 60 01 60 01 60 01 60 01 60 01 60 01
                                          60 01 60 01 60 01 60 01 60 01 60 01 60 01 64 00
                                          77 00 60 01 60 01 60 01 60 01 60 01 60 01 60 01
                                          60 01 60 01 60 01 60 01 60 01 60 01 60 01 60 01
                                          60 01 60 01 60 01 60 01 60 01 60 01 60 01 60 01
                                          60 01 60 01 60 01 60 01 60 01 60 01 60 01 74 00"""),

    "Demon Guest House": bytes.fromhex("""78 40 05 00 05 00 05 00 05 00 05 00 05 00 05 00
                                          05 00 05 00 05 00 05 00 05 00 05 00 05 00 05 00
                                          05 00 05 00 05 00 05 00 05 00 05 00 05 00 05 00
                                          05 00 05 00 05 00 05 00 05 00 05 00 05 00 78 80
                                          78 40 05 00 05 00 05 00 05 00 05 00 05 00 05 00
                                          05 00 05 00 05 00 05 00 05 00 05 00 05 00 05 00
                                          05 00 05 00 05 00 05 00 05 00 05 00 05 00 05 00
                                          05 00 05 00 05 00 05 00 05 00 05 00 05 00 78 80"""),

    "Cursed Clock Tower": bytes.fromhex(("""A0 00 A1 00 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02
                                            2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02
                                            2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02
                                            2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 A1 40 A0 40
                                            B0 00 B1 00 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02
                                            2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02
                                            2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 2E 02
                                            2E 02 2E 02 2E 02 2E 02 2E 02 2E 02 B1 40 B0 40""")),

    "The Pinnacle": bytes.fromhex(("""1F C0 68 00 68 00 68 00 68 00 68 00 68 00 68 00
                                      68 00 68 00 68 00 68 00 68 00 68 00 68 00 68 00
                                      68 00 68 00 68 00 68 00 68 00 68 00 68 00 68 00
                                      68 00 68 00 68 00 68 00 68 00 68 00 68 00 1F 80
                                      1F C0 68 00 68 00 68 00 68 00 68 00 68 00 68 00
                                      68 00 68 00 68 00 68 00 68 00 68 00 68 00 68 00
                                      68 00 68 00 68 00 68 00 68 00 68 00 68 00 68 00
                                      68 00 68 00 68 00 68 00 68 00 68 00 68 00 1F 80""")),


    "Mine of Judgment": bytes.fromhex("""76 00 77 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 77 40 76 40
                                         86 00 87 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 D5 00
                                         D5 00 D5 00 D5 00 D5 00 D5 00 D5 00 87 40 86 40""")
}


def expand_rahab_room(rom, room):
    # TODO! Pinnacle has no background beneath its floor
    # TODO! Set Pinnacle's Base Tile to 4E
    import struct
    data = room_data[room]
    if room == "Dark Chapel Inner":
        is_chapel2 = True
        floor_offset = 0x40  # We want to copy the top floor, not the lower set
    else:
        is_chapel2 = False
        floor_offset = 0

    if room == "Dark Chapel":
        rom.write_to_file(0x020AEB8D, "arm9", bytearray([0x00]))  # We need to delete these entities in DC
        rom.write_to_file(0x020AEB81, "arm9", bytearray([0x00]))  # so that the waterline is able to spawn

    rom.write_to_file(data.layer_pointer, data.file, bytearray([0x02]))  # Mark this room as having 2 height
    # Repoint the layer to the new room
    rom.write_to_file(data.layer_pointer + 0x0B, data.file, struct.pack("I", 0x021C8564))

    rom.copy_bytes(data.room_pointer, 0x300, 0xF5384)  # First we need to copy the original room's data
    for i in range(6):  # Next we need to extend the walls downward.
        rom.write_to_file(0x021C8864 + (0x80 * i), "overlay_0", byte_sequences[room])

    if room != "Lost Village":  # Every room except for Village we can just copy the existing floor data.
        if data.one_tile_wall:
            rom.copy_bytes(0xF5646, 0x3C, 0xF5946)  # Copy the room's original floor down
            for i in range(0x1E):
                # Clear out the original floor
                rom.write_to_file(0x021C8826 + (i * 2), "overlay_0", struct.pack("H", data.base_tile))
        else:
            rom.copy_bytes(0xF5648 - floor_offset, 0x38, 0xF5948)  # Copy the room's original floor down
            for i in range(0x1C):
                # Clear out the original floor
                rom.write_to_file(0x021C8828 + (i * 2), "overlay_0", struct.pack("H", data.base_tile))

                if is_chapel2:
                    #  We need to also clear the higher floor of Chapel 2
                    rom.write_to_file(0x21C87E8 + (i * 2), "overlay_0", struct.pack("H", 0x00))
    else:
        rom.write_to_file(0x020A1105, "arm9", bytearray([0x00]))  # Clear out LV's ent hider
        for i in range(20):
            rom.write_to_file(0x21C87EE + (i * 2), "overlay_0", struct.pack("H", 0x00))  # Zero out the
            rom.write_to_file(0x21C882E + (i * 2), "overlay_0", struct.pack("H", 0x00))  # original floor

        for i in range(0x1E):
            rom.write_to_file(0x21C8B26 + (i * 2), "overlay_0", struct.pack("H", 0x01BA))

    if room == "Dark Chapel Inner":
        rom.write_to_file(0x21C881A, "overlay_0", bytearray([0x37, 0xC1, 0x50, 0x81, 0x50, 0x81]))  # Corner the ramp
        rom.write_to_file(0x21C881A + 0x340, "overlay_0", bytearray([0x50, 0x01, 0x50, 0x01, 0x50, 0x01]))  # Cleanup the last tiles
    elif room == "Garden of Madness":
        rom.write_to_file(0x020AC511, "arm9", bytearray([0x00]))  # Clear the hider
        rom.write_to_file(0x020AC4E1, "arm9", bytearray([0x00]))  # Dario scene obj
        for i in range(0x1E):
            rom.write_to_file(0x022E277E + (2 * i), "overlay_16", struct.pack("H", 0x0161))  # Replace fake floor
    elif room == "The Pinnacle":
        rom.write_to_file(0x02225C3C, "overlay_0", struct.pack("H", 0x8005))  # Set a waterline for the mirror world
        for i in range(0x1E):
            rom.write_to_file(0x022DCF42 + (2 * i), "overlay_10", struct.pack("H", 0xC0))  # Cover up blank tile

    rom.write_to_file(data.entity_end, "arm9", struct.pack("H", 0x8005))  # Tell the room to spawn a waterline

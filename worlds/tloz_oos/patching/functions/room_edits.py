import pkgutil
from typing import Any

from settings import get_settings

from ... import patching
from ...common.patching.RomData import RomData
from ...common.patching.rooms.decoding import decompress_rooms
from ...Options import OracleOfSeasonsLinkedHerosCave

### How rooms work:
# Room number 0xYZZ = group Y, room ZZ
# Groups 0-3 are seasons spring to winter (usually 0ZZ)
# Group 4 is subrosia/maku/grottos (usually 1ZZ/2ZZ/3ZZ)
# Group 5-6 are the big rooms (usually 4ZZ/6ZZ and 5ZZ/7ZZ)

# Positions are assessed with YX format
# Positions in small rooms are written in decimal, as a line is 10 tiles long
# Positions in big rooms are written in hew, as a line is 16 tiles long (last tile is always 0)


def apply_room_edits(rom_data: RomData, patch_data: dict[str, Any]) -> list[bytearray]:
    room_data = decompress_rooms(rom_data, True)

    apply_d0_alt_entrance_edits(room_data, patch_data)
    apply_d2_alt_entrance_edits(room_data, patch_data)
    apply_samasa_dungeon_edits(room_data, patch_data)
    apply_anti_softlock_edits(room_data)
    apply_misc_edits(room_data)

    return room_data


def apply_d0_alt_entrance_edits(room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    if not patch_data["options"]["remove_d0_alt_entrance"]:
        return
    for room_id in range(0x0D4, 0x400, 0x100):
        # Remove the grass and the soil in all seasons
        room_data[room_id][17] = 0x11
        room_data[room_id][26] = 0x11
        room_data[room_id][27] = 0x11
        room_data[room_id][28] = 0x11

        # Remove the chimney
        room_data[room_id][57] = 0xAF

    # Add stairs to the chest
    room_data[0x505][0x5A] = 0x53


def apply_d2_alt_entrance_edits(room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    for room_id in range(0x08E, 0x400, 0x100):
        # Replace the vines by stairs in all seasons
        room_data[room_id][34] = 0x36
        room_data[room_id][35] = 0xD0
        room_data[room_id][36] = 0x35
        room_data[room_id][44] = 0x51
        room_data[room_id][45] = 0xD0
        room_data[room_id][46] = 0x50
        if not patch_data["options"]["remove_d2_alt_entrance"]:
            continue

        # Remove the stairs
        room_data[room_id][12] = 0x04
        room_data[room_id - 1][18] = 0x04


def apply_samasa_dungeon_edits(room_data: list[bytearray], patch_data: dict[str, Any]) -> None:
    if patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.samasa:
        # Add the dungeon entrance
        samasa_desert_dungeon_data = pkgutil.get_data(patching.__name__, "rooms/samasa_dungeon.dat")
        assert samasa_desert_dungeon_data is not None
        room_data[0x1CF] = bytearray(samasa_desert_dungeon_data)
        if patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.no_alt_entrance:
            room_data[0x1CF][28] = 0x04  # Remove the grass
            room_data[0x1CF][48] = 0xAF  # Remove the chimney

    if patch_data["options"]["linked_heros_cave"] & OracleOfSeasonsLinkedHerosCave.no_alt_entrance:
        room_data[0x62C][0x42] = 0x52  # Add stairs to the alt entrance chest


def apply_anti_softlock_edits(room_data: list[bytearray]) -> None:
    # In room 016, move the tree in front of the door left to avoid locking the player
    for room_id in range(0x016, 0x300, 0x100):
        room_data[room_id][16] = 0x70
        room_data[room_id][17] = 0x71
        room_data[room_id][18] = 0x0F
        room_data[room_id][26] = 0x80
        room_data[room_id][27] = 0x81
        room_data[room_id][28] = 0x70
    # In winter, it needs to be different
    room_data[0x316][16] = 0x65
    room_data[0x316][17] = 0x66
    room_data[0x316][18] = 0x0F
    room_data[0x316][26] = 0x55
    room_data[0x316][27] = 0x56
    room_data[0x316][28] = 0x65

    # Remove the natzu bridge lever
    for natzu_room in [0x056, 0x256]:  # Ricky and Dimitri
        room = room_data[natzu_room]
        room[66] = 0x04

        room[43] = 0xFD
        room[44] = 0xFD
        room[53] = 0xFD
        room[54] = 0xFD

    # Shallow water to leave d4
    for room_id in range(0x01D, 0x300, 0x100):
        room_data[room_id][31] = 0xFA
        room_data[room_id][32] = 0xFA
        room_data[room_id][33] = 0xFA
        room_data[room_id][34] = 0xFA
        room_data[room_id][35] = 0xFA
        room_data[room_id][36] = 0xFA
    # Ice for winter
    room_data[0x31D][31] = 0xDC
    room_data[0x31D][32] = 0xDC
    room_data[0x31D][33] = 0xDC
    room_data[0x31D][34] = 0xDC
    room_data[0x31D][35] = 0xDC

    # Spool swamp had one to leave to east in spring, but it wasn't kept

    # Some snow piles in suburbs to WoW were removed, but this change wasn't kept

    # Remove a snow pile to prevent the statue blocking the path in winter if pushed left
    room_data[0x301][54] = 0x04

    # Remove a snow pile in front of Holly's house to avoid a needless softlock
    room_data[0x37F][56] = 0x04

    # D7 snow piles aren't removed, warp isn't far, and this impacts logic positively

    for room_id in range(0x09A, 0x400, 0x100):
        # Remove rock across pit blocking exit from D5
        room_data[room_id][14] = 0x12

        # Remove bush next to rosa portal
        room_data[room_id][34] = 0x04

    # Add rock at bottom of cliff to block ricky
    for room_id in range(0x08A, 0x400, 0x100):
        room_data[room_id][66] = 0x64

    # Add a ledge from lower portal
    for room_id in range(0x025, 0x400, 0x100):
        room_data[room_id][32] = 0x3A
        room_data[room_id][33] = 0xCF
        room_data[room_id][34] = 0x4B


def apply_misc_edits(room_data: list[bytearray]) -> None:
    # Remove access to first refill room on 4 essences
    for i in range(2, 80, 10):
        for j in range(6):
            room_data[0x41C][i + j] = 0x62 + j

    # Remove access to second refill room on 6 essences
    room_data[0x44B][3] = 0x63

    # Reveal hidden subrosia digging spots if required
    if get_settings()["tloz_oos_options"]["reveal_hidden_subrosia_digging_spots"]:
        room_data[0x406][18] = 0x2F
        room_data[0x457][38] = 0x2F
        room_data[0x447][33] = 0x2F
        room_data[0x43A][46] = 0x2F
        room_data[0x407][13] = 0x2F
        room_data[0x420][68] = 0x2F
        room_data[0x442][14] = 0x2F

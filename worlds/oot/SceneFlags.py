from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .LocationList import OOTLocation

from .LocationList import location_table


# Loop through all of the locations in the world. Extract ones that use our flag system to start building our xflag tables
def build_xflags_from_world(world):
    scene_flags = {}
    alt_list = []
    for i in range(0, 101):
        scene_flags[i] = {}
        for location in world.get_locations():
            if location.scene == i and location.type in ["Freestanding", "Pot", "FlyingPot", "Crate", "SmallCrate", "Beehive", "RupeeTower", "SilverRupee", "Wonderitem"]:
                default = location.default
                if isinstance(default, list):  # List of alternative room/setup/flag to use
                    primary_tuple = default[0]
                    if len(primary_tuple) == 3:
                        room, setup, flag = primary_tuple
                        subflag = 0
                        primary_tuple = (room, setup, flag, subflag)
                    for c in range(1, len(default)):
                        alt = default[c]
                        if len(alt) == 3:
                            room, setup, flag = alt
                            subflag = 0
                            alt = (room, setup, flag, subflag)
                        alt_list.append((location, alt, primary_tuple))
                    default = primary_tuple  # Use the first tuple as the primary tuple
                if isinstance(default, tuple):
                    if len(default) == 3:
                        room, setup, flag = default
                        subflag = 0
                    elif len(default) == 4:
                        room, setup, flag, subflag = default
                    room_setup = (setup, room)
                    if room_setup not in scene_flags[i]:
                        scene_flags[i][room_setup] = []
                    scene_flags[i][room_setup].append((flag, subflag))

        if len(scene_flags[i].keys()) == 0:
            del scene_flags[i]
    return scene_flags, alt_list


# Take the data from build_xflags_from_world and create the actual tables that will be stored in the ROM
def build_xflag_tables(xflags):
    scene_table = bytearray([0xFF] * 202)
    room_table = bytearray(0)
    room_blob = bytearray(0)
    bits = 0
    for scene in xflags.keys():
        num_room_setups = len(xflags[scene].keys())
        room_table_offset = len(room_table)
        scene_table[scene*2] = (room_table_offset & 0xFF00) >> 8
        scene_table[scene*2 + 1] = (room_table_offset & 0x00FF)
        room_table.append(num_room_setups)
        for setup, room in xflags[scene].keys():
            if scene == 0x3E:
                room_setup = bytearray([setup, room])
            else:
                room_setup = bytearray([(setup << 6) + room])
            room_xflags, room_bits = build_room_xflags(xflags[scene][(setup, room)])
            diff_flags, rlc_flags = encode_room_xflags(room_xflags)
            room_table.extend(room_setup)
            room_blob_offset = len(room_blob)
            room_table.append((room_blob_offset & 0xFF00) >> 8)
            room_table.append(room_blob_offset & 0x00FF)
            room_blob.append((bits & 0xFF00) >> 8)
            room_blob.append(bits & 0x00FF)
            room_blob.append(len(rlc_flags))
            room_blob.extend(bytearray(rlc_flags))
            bits += room_bits
    return scene_table, room_table, room_blob, bits


# Create a 256 byte array representing each actor in the room.
# Each value in the array is the bit index that will be used for that actor, accounting for sub_ids.
# room_locations - list of (actor_id, sub_id) in the room
def build_room_xflags(room_locations):
    room_xflags = [0] * 256
    for actor_id, subflag in room_locations:
        if subflag >= room_xflags[actor_id]:
            room_xflags[actor_id] = subflag + 1
    bits = 0
    room_xflags2 = [0] * 256
    last = 1
    for i in range(0, 256):
        if room_xflags[i] != 0:
            room_xflags2[i] = last
            last = room_xflags[i]
        bits += room_xflags[i]
    return room_xflags2, bits


def encode_room_xflags(xflags):
    # Run length coding
    rlc_flags = []
    curr_token = xflags[0]
    curr_token_count = 1
    for i in range(1, 256):
        if xflags[i] == curr_token:
            curr_token_count += 1
        else:
            rlc_flags.append(curr_token)
            rlc_flags.append(curr_token_count)
            curr_token = xflags[i]
            curr_token_count = 1
    return xflags, rlc_flags


# Build a list of alternative overrides for alternate scene setups
def get_alt_list_bytes(alt_list):
    bytes = bytearray()
    for entry in alt_list:
        location, alt, primary = entry
        room, scene_setup, flag, subflag = alt

        if location.scene is None:
            continue
        alt_scene = location.scene
        if location.scene == 0x0A:
            alt_scene = 0x19

        alt_override = (scene_setup << 22) | (room << 16) | (flag << 8) | (subflag)
        room, scene_setup, flag, subflag = primary
        primary_override = (scene_setup << 22) | (room << 16) | (flag << 8) | (subflag)
        bytes.append(alt_scene)
        bytes.append(0x06)
        bytes.append(0x00)
        bytes.append(0x00)
        bytes.append((alt_override & 0xFF000000) >> 24)
        bytes.append((alt_override & 0x00FF0000) >> 16)
        bytes.append((alt_override & 0x0000FF00) >> 8)
        bytes.append((alt_override & 0x000000FF))
        bytes.append(location.scene)
        bytes.append(0x06)
        bytes.append(0x00)
        bytes.append(0x00)
        bytes.append((primary_override & 0xFF000000) >> 24)
        bytes.append((primary_override & 0x00FF0000) >> 16)
        bytes.append((primary_override & 0x0000FF00) >> 8)
        bytes.append((primary_override & 0x000000FF))
    return bytes


# AP method to retrieve address + bit for each collectible item location.
# Uses the xflag bit addressing scheme from build_xflag_tables.
# Returns {location.address: [0, global_bit_position]} for the Lua connector.
def get_collectible_flag_addresses(world, xflags_tables):
    # Build room_xflags per (scene, setup, room) and track cumulative bit positions,
    # mirroring the exact iteration order of build_xflag_tables.
    bit_map = {}  # (scene, setup, room, actor_id, subflag) -> global_bit_position
    cumulative_bits = 0

    for scene in xflags_tables.keys():
        for setup, room in xflags_tables[scene].keys():
            room_locations = xflags_tables[scene][(setup, room)]

            # Compute room_xflags: number of subflags per actor_id
            room_xflags = [0] * 256
            for actor_id, subflag in room_locations:
                if subflag >= room_xflags[actor_id]:
                    room_xflags[actor_id] = subflag + 1

            # Bits are packed sequentially: all subflags of actor 0, then actor 1, etc.
            # global bit for (actor_id, subflag) = cumulative_bits + prefix_bits + subflag
            prefix_bits = 0
            for actor_id in range(256):
                if room_xflags[actor_id] != 0:
                    for subflag in range(room_xflags[actor_id]):
                        bit_map[(scene, setup, room, actor_id, subflag)] = cumulative_bits + prefix_bits + subflag
                    prefix_bits += room_xflags[actor_id]

            cumulative_bits += sum(room_xflags)

    collectible_flag_addresses = {}
    for location in world.get_locations():
        if location.type in ["Freestanding", "Pot", "FlyingPot", "Crate", "SmallCrate", "Beehive", "RupeeTower", "SilverRupee", "Wonderitem"]:
            default = location.default
            if isinstance(default, list):
                default = default[0]
            if isinstance(default, tuple):
                if len(default) == 3:
                    room, setup, flag = default
                    subflag = 0
                elif len(default) == 4:
                    room, setup, flag, subflag = default
                else:
                    continue
                key = (location.scene, setup, room, flag, subflag)
                if key in bit_map:
                    collectible_flag_addresses[location.address] = [0, bit_map[key]]

    return collectible_flag_addresses

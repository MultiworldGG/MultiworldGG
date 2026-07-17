# warps are in bank 04
WARP_DEST_TABLE = 0x12f5b
WARP_SOURCE_TABLE = 0x1359e

# Reminder for warp destination content (none of this will be touched) :
# byte 0 is the toom index to warp to (the group is implicit from the address)
# byte 1  Y/X position to spawn at.
# byte 2 Parameter. What this does depends on the transition type? (ie. walk in from top or bottom of screen?)
# byte 3 Transition dest type (see constants/transitions.s).

# Reminder for warp source content :
# byte 0 is misc data for the warp (shouldn't be touched ?)
# byte 1 is the room index from where the warp come from (the group is implicit from the address) (shouldn't be touched)
# byte 2 is the Warp dest index of the warp (is modified)
# byte 3 (first halfbyte) is the warp group of destination (is modified)
# byte 3 (second halfbyte) is the transition type (shouldn't be touched ?)

def GetWarpNameFromDungeonNumber(dungeon):
    for warpName, warpData in WARPS_DATA.items():
        if ("dungeon" in warpData and warpData["dungeon"] == dungeon):
            return warpName
    return ""

def GetWarpDataFromDungeonNumber(dungeon):
    return WARPS_DATA[GetWarpNameFromDungeonNumber(dungeon)]

# "outside_warp" : Warp source of the warp from outside to inside (NOTE : This is not the exact address of the warp entry, but the address + 2)
# "inside_warp" : Warp source of the warp from inside to outside
# "custom_map_tile" : By default, map tile use the room and the group to be generated, but if there is a custom_map_tile, it's used instead
# "present" : is the warp in the present (will be used to randomize only entrance in the past with past and vice versa)
# "dungeon" : if set, this is a dungeon entrance, and this is for the dungeon given here
# "is_deadend" : if set, can be paired with entrance that have the "must_lead_to_deadend" tag
# "must_lead_to_deadend" : See above.

# regions from all warps are automatically created from this struct and (if no randomization is done) logic connect outside and inside as a two way connection. 
# On the outside side, the region will be name "outside <NAME>"
# On the inside side, the region will be name "inside <NAME>"

OUTSIDE_TAG = "outside "
INSIDE_TAG = "inside "

WARPS_DATA = {

    # LYNNA CITY
    "vasu's shop" :{
        "outside_warp": 0x7628,
        "inside_warp": 0x7948,
        "present": True,
    },

    #DUNGEONS
    "d0": {
        "outside_warp": 0x7728,
        "inside_warp": 0x7aec,
        "custom_txt_id": 0xe9,
        "present": False,
        "dungeon": 0,
    },
    "d1": {
        "outside_warp": 0x7718,
        "inside_warp": 0x7ad0,
        "present": True,
        "dungeon": 1,
    },
    "d2": {
        "outside_warp": 0x772c,
        "inside_warp": 0x7ad4,
        "present": False,
        "dungeon": 2,
    },
    "d3": {
        "outside_warp": 0x75c8,
        "inside_warp": 0x7ad8,
        "present": True,
        "dungeon": 3,
    },
    "d4": {
        "outside_warp": 0x75cc,
        "inside_warp": 0x7adc,
        "present": True,
        "dungeon": 4,
    },
    "d5": {
        "outside_warp": 0x76b0,
        "inside_warp": 0x7ae0,
        "present": True,
        "dungeon": 5,
    },
    "d6 present": {
        "outside_warp": 0x7748,
        "inside_warp": 0x7c48,
        "custom_map_tile": 0x03c,
        "present": True,
        "dungeon": 6,
    },
    "d7": {
        "outside_warp": 0x7874,
        "inside_warp": 0x7c60,
        "custom_map_tile": 0x090,
        "present": True,
        "dungeon": 7,
        "is_underwater": True,
    },
    "d8": {
        "outside_warp": 0x7730,
        "inside_warp": 0x7c74,
        "present": False,
        "dungeon": 8,
    },
    "d11": {
        "outside_warp": 0x770c,
        "inside_warp": 0x7ae4,
        "present": True,
        "dungeon": 11,
        "require_option": "linked_heros_cave"
    },
    "d6 past": {
        "outside_warp": 0x79b4,
        "inside_warp": 0x7c54,
        "custom_map_tile": 0x13c,
        "custom_txt_id": 0xe1,
        "present": False,
        "dungeon": 9,
    }
}
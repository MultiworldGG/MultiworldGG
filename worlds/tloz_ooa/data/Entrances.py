from .Items import ITEMS_DATA

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

#PRESENT TIME

    # FOREST OF TIME
    "nayru's house": {
        "outside_warp": 0x7660,
        "inside_warp": 0x7a10,  #room 3 9E
        "present": True,
    },
#room 3 9F, room 3 AE

    "lower tingle cave": {
        "outside_warp": 0x7644,
        "inside_warp": 0x78CC,    #room 2 9E, t11
        "present": True,
    },
    "upper tingle stairs": {
        "outside_warp": 0x763c,
        "inside_warp": 0x78D0,    #room 2 9E, t67/68
        "present": True,
    },

    # LYNNA CITY
    "vasu's shop": {
        "outside_warp": 0x7628,
        "inside_warp": 0x7948,  #room 2 EE
        "present": True,
    },
    "lynna city shop": {
        "outside_warp": 0x7714,
        "inside_warp": 0x78A4,    #room 2 5E
        "present": True,
    },

#room 2 5F for the single room connector, outside 5e 0e 2 2
#room 2 7E for the shop
    "hidden entrance shop": {
        "outside_warp": 0x7710,
        "inside_warp": 0x78A0,   #room 2 5E
        "present": True,
    },

    "mayor's house": {
        "outside_warp": 0x7624,
        "inside_warp": 0x7a90,  #room 3 F8
        "present": True,
    },
    # the house where the kid gets frozen in time on the cutscene where veran takes over naryu at the beginning, i dont have a better name for this
    "petrified kid's house": {
        "outside_warp": 0x7620,   #room 0 56
        "inside_warp": 0x7878,    #room 2 0E
        "present": True,
    },

    "know it all birds house": {
        "outside_warp": 0x761C,   #room 0 55
        "inside_warp": 0x7A8C,    #room 3 F7
        "present": True,
    },

    "mamamu yan house": {
        "outside_warp": 0x7630,   #room 0 66
        "inside_warp": 0x7930,    #room 2 E7
        "present": True,
    },

#stairs to vire 0x7B5C
    "black tower ruins": {
        "outside_warp": 0x7638,   #room 0 76
        "inside_warp": [0x7B54, 0x7B58],    #room 4 E6
        "present": True,
        "require_option": "secret_locations"
    },

    "troy's house": {
        "outside_warp": 0x760C,   #room 0 45
        "inside_warp": 0x7a98,    #room 3 FB
        "present": True,
    },

    "left bippin blossom door": {
        "outside_warp": 0x7700,   #room 0 47
        "inside_warp": 0x793C,    #room 2 EA
        "present": True,
    },

    "right bippin blossom door": {
        "outside_warp": 0x7704,   #room 0 47
        "inside_warp": 0x7940,    #room 2 EB
        "present": True,
    },

    "happy mask shop": {
        "outside_warp": 0x7618,   #room 0 53
        "inside_warp": 0x792C,    #room 2 E6
        "present": True,
    },

    # YOLL GRAVEYARD
    "cheval grave": {
        "outside_warp": 0x768C,   #room 0 5B
        "inside_warp": 0x7CC4,    #room 5 BE
        "present": True,
    },
    "syrup hut": {
        "outside_warp": 0x762C,   #room 0 5D
        "inside_warp": 0x7a7c,    #room 3 ED
        "present": True,
    },
    "grave under the tree": {
        "outside_warp": 0x771C,   #room 0 8D, t56
        "inside_warp": 0x7d78,    #room 5 ED
        "present": True,
        "item_lock": "Ember Seeds",
        "lock_flag": 0xc78d,
        "lock_mask": 0x80,
        "lock_text": 0x5a26,
    },
    "poe grave": {
        "outside_warp": 0x7640,   #room 0 7c
        "inside_warp": 0x7888,    #room 2 2E
        "present": True,
    },
    # NUUN HIGHLANDS
    "nuun fairy cave": {
        "outside_warp": 0x75e4,   #room 0 06
        "inside_warp": 0x7918,    #room 2 DF
        "present": True,
    },

    # PRESENT SYMMETRY
    "present top left symmetry house": {
        "outside_warp": 0x75d4,   #room 0 02
        "inside_warp": 0x7a08,    #room 3 8E
        "present": True,
    },
    "present top right symmetry house": {
        "outside_warp": 0x75d8,   #room 0 04
        "inside_warp": 0x7a70,    #room 3 EA
        "present": True,
    },
    "present bottom left symmetry house": {
        "outside_warp": 0x75dc,   #room 0 12
        "inside_warp": 0x7a74,    #room 3 EB
        "present": True,
    },
    "present bottom right symmetry house": {
        "outside_warp": 0x75e0,   #room 0 14
        "inside_warp": 0x7a78,    #room 3 EC
        "present": True,
    },

    # WESTERN ROLLING RIDGE
    "present goron city lower": {
        "outside_warp": 0x7680,   #room 0 28
        "inside_warp": 0x7cb4,    #room 5 B9
        "present": True,
    },

    #chest stairs at 21 2e 52, deeper stairs at 57 23 52
    "present goron city upper": {
        "outside_warp": 0x76c8,   #room 0 18
        "inside_warp": 0x7cc8,    #room 5 C0
        "present": True,
    },

    #right side inside stairs ID at 2b 2a 52
    "present goron city stairs": {
        "outside_warp": 0x76cc,   #room 0 18
        "inside_warp": 0x7dec,    #room 5 C2
        "present": True,
    },

    "present west ridge fairy cave": {
        "outside_warp": 0x76d4,   #room 0 1B
        "inside_warp": 0x79e0,    #room 3 3F
        "present": True,
    },

    #access from moblin keep always out of logic,
    # cannot guarantee real entrance not be locked behind itself
    # through either chest or exit
    #first sewer room with falling fire, right exit 01 02 73
    #"moblin keep sewer stairs": {
    #    "outside_warp": 0x76a8,   #room 0 09
    #    "inside_warp": 0x7e60,    #room 7 01
    #    "present": True,
    #},
#moblin keep sewer chest room, room 2 BE
#staircase back down to side scroller bf 06 72
    "moblin keep sewer exit": {
        "outside_warp": 0x76ac,   #room 0 0A
        "inside_warp": 0x78fc,    #room 2 BF
        "present": True,
    },
    #the cave directly behind moblin keep
    "cave behind moblin keep front": {
        "outside_warp": 0x76a4,   #room 0 09
        "inside_warp": 0x7d28,    #room 5 DA
        "present": True,
        # Moblin keep have a special behavior, and is always blocked if not triggered, whatever it the option
        #"lock_flag": 0xc709,
        #"lock_mask": 0x01,
        #"lock_text": 0x5a27
    },
    #the side of the moblin keep connector that takes you to crown dungeon ledge
    "cave behind moblin keep back": {
        "outside_warp": 0x76bc,   #room 0 0B
        "inside_warp": 0x7d2c,    #room 5 DB
        "present": True,
    },
    # the connector that takes you from crown dungeon ledge to upper ridge
    "crown ledge to upper ridge cave front": {
        "outside_warp": 0x76b8,   #room 0 0B
        "inside_warp": 0x7964,    #room 2 F9
        "present": True,
    },
    # the connector that takes you from upper ridge to crown dungeon ledge
    # other staircase in room is fb 44 22
    "crown ledge to upper ridge cave back": {
        "outside_warp": 0x76d0,   #room 0 1B
        "inside_warp": 0x7970,    #room 2 FB
        "present": True,
    },

    # EASTERN ROLLING RIDGE
    # the cave that becomes treasure hunting goron in the past
    "empty cave by echo portal under rock": {
        "outside_warp": 0x76b4,   #room 0 0B
        "inside_warp": 0x7958,    #room 2 F6
        "present": True,
    },
    # the connector that takes you to the base of east ridge from the top
    # other warp is at 2e 4f 52
    "present east ridge upper to lower cave top": {
        "outside_warp": 0x75f0,   #room 0 0C
        "inside_warp": 0x79d0,    #room 3 2E
        "present": True,
    },
    # the connector that takes you to the top of east ridge from the base
    "present east ridge upper to lower cave base": {
        "outside_warp": 0x7684,   #room 0 2B
        "inside_warp": 0x7d48,    #room 5 E2
        "present": True,
    },
    #where the dance hall ends up at the very top
    #stairs that leads to chest at 0x7D7C
    "upper ridge present northeast cave left": {
        "outside_warp": 0x76c0,   #room 0 0D
        "inside_warp": 0x7d7c,    #room 5 EE
        "present": True,
    },

    # needs tune of currents to access, it's inside warp is a one way
    "upper ridge present northeast cave right": {
        "outside_warp": 0x76c4,   #room 0 0D
        "inside_warp": 0x7d80,    #room 5 EE
        "present": True,
    },

#room 2 ED present graceful goron room
# upstairs id at 0x797c
    "present goron dance hall lower": {
        "outside_warp": 0x76f8,   #room 0 3D
        "inside_warp": 0x7978,    #room 2 FD
        "present": True,
    },

#room 3 4E, room outside big bang game; room 3 3E, big bang game
    "present goron dance hall middle": {
        "outside_warp": 0x76d8,   #room 0 1C
        "inside_warp": 0x79c0,    #room 3 1E
        "present": True,
    },
    "present east ridge base fairy cave": {
        "outside_warp": 0x76fc,   #room 0 3D
        "inside_warp": 0x79e8,    #room 3 4F
        "present": True,
    },
    "present mermaid cave front porch": {
        "outside_warp": 0x7688,   #room 0 3C
        "inside_warp": 0x774c,    #room 1 0E
        "present": True,
    },
#room 3 0E, door mat chest


    "greedy old man bush": {
        "outside_warp": 0x7614,   #room 0 4D
        "inside_warp": 0x7898,    #room 2 4E
        "present": True,
        "item_lock": "Ember Seeds",
        "lock_flag": 0xc74d,
        "lock_mask": 0x80,
        "lock_text": 0x5a26
    },
    "empty cave left of target carts": {
        "outside_warp": 0x76dc,   #room 0 1C
        "inside_warp": 0x79f0,    #room 3 5F
        "present": True,
    },
    "empty cave right of target carts": {
        "outside_warp": 0x76e4,   #room 0 1D
        "inside_warp": 0x79ec,    #room 3 5E
        "present": True,
    },
    "target carts": {
        "outside_warp": 0x76e0,   #room 0 1D
        "inside_warp": 0x7d24,    #room 5 D8
        "present": True,
    },
#PRESENT LYNNA SEAS
    "present underwater sea of storms cave": {
        "outside_warp": 0x78ec,   #room 2 B7
        "inside_warp": 0x7a68,    #room 3 E8
        "present": True,
        "is_underwater": True,
        "require_option": "secret_locations"
    },
    "present drifting island house": {
        "outside_warp": 0x7650,   #room 0 C5
        "inside_warp": 0x7a40,    #room 3 CE
        "present": True,
    },
    "present underwater zora duplex left": {
        "outside_warp": 0x79a4,   #room 2 D0
        "inside_warp": 0x7a54,    #room 3 E3
        "present": True,
        "is_underwater": True,
    },
    "present underwater zora duplex right": {
        "outside_warp": 0x79a8,   #room 2 D0
        "inside_warp": 0x7a58,    #room 3 E4
        "present": True,
        "is_underwater": True,
    },
    "present underwater zora house": {
        "outside_warp": 0x7904,   #room 2 C1
        "inside_warp": 0x7a4c,    #room 3 DE
        "present": True,
        "is_underwater": True,
    },

    #throne room stairs 0x7d94
    "present zora palace": {
        "outside_warp": 0x78e0,   #room 2 A1
        "inside_warp": 0x7d90,    #room 5 AC
        "present": True,
        "is_underwater": True,
    },
    #bombable cave in the top left of zora village above water
    "zora crypt cave": {
        "outside_warp": 0x7690,   #room 0 A0
        "inside_warp": 0x7ce8,    #room 5 C7
        "present": True,
        "item_lock": "Bombs (10)",
        "lock_flag": 0xc7a0,
        "lock_mask": 0x80,
        "lock_text": 0x5a25
    },
    "present fairy queen cave": {
        "outside_warp": 0x7648,   #room 0 A3
        "inside_warp": 0x7a80,    #room 3 EE
        "present": True,
    },
    "present library": {
        "outside_warp": 0x7694,   #room 0 A5
        "inside_warp": 0x7d08,    #room 5 D0
        "present": True,
        "lock_flag": 0xc8a5,
        "lock_mask": 0x80,
        "lock_text": 0x5a28
    },
#PRESENT CRESCENT
    "southern fairy cave": {
        "outside_warp": 0x7658,   #room 0 DA
        "inside_warp": 0x7a88,    #room 3 F6
        "present": True,
    },
    "wild tokay museum": {
        "outside_warp": 0x764c,   #room 0 BD
        "inside_warp": 0x7928,    #room 2 E5
        "present": True,
    },
    "present chicken hut": {
        "outside_warp": 0x7654,   #room 0 CD
        "inside_warp": 0x790c,    #room 2 CF
        "present": True,
    },
    "tokay chef house": {
        "outside_warp": 0x765c,   #room 0 DD
        "inside_warp": 0x7894,    #room 2 3F
        "present": True,
    },
    "underwater maze cave": {
        "outside_warp": 0x78f0,   #room 2 BA
        "inside_warp": 0x7aa0,    #room 3 FD
        "present": True,
        "is_underwater": True,
    },
#PAST ENTRANCES
#LYNNA VILLAGE

    "town shooting gallery": {
        "outside_warp": 0x7854,   #room 1 58
        "inside_warp": 0x7938,    #room 2 E9
        "present": False,
    },
    "advance shop": {
        "outside_warp": 0x7858,   #room 1 58
        "inside_warp": 0x7aa4,    #room 3 FE
        "present": False,
        "require_option": "advance_shop"
    },
    "postman house": {
        "outside_warp": 0x77c0,   #room 1 57
        "inside_warp": 0x788c,    #room 2 2F
        "present": False,
    },
    "sad boi house": {
        "outside_warp": 0x77bc,   #room 1 56
        "inside_warp": 0x794c,    #room 2 F3
        "present": False,
    },
    "gasha farmer house": {
        "outside_warp": 0x77ac,   #room 1 45
        "inside_warp": 0x7a9c,    #room 3 FC
        "present": False,
    },
    "toilet hand house": {
        "outside_warp": 0x77b8,   #room 1 55
        "inside_warp": 0x7890,    #room 2 3E
        "present": False,
    },
    #mamamu yan house in the past
    "advisor house": {
        "outside_warp": 0x77cc,   #room 1 66
        "inside_warp": 0x7a94,    #room 3 FA
        "present": False,
    },

    "cheval house": {
        "outside_warp": 0x77e0,   #room 1 79
        "inside_warp": 0x787c,    #room 2 0F
        "present": False,
    },
    "rafton house left": {
        "outside_warp": 0x785c,
        "inside_warp": 0x7880,
        "present": False,
    },
    "rafton house right": {
        "outside_warp": 0x7860,
        "inside_warp": 0x7884,
        "present": False,
    },
#DEKU FOREST
    #the cave with the heart piece on a ledge,
    # the stairs at the beginning of the forest
    "deku forest heart cave stairs": {
        "outside_warp": 0x77dc,   #room 1 74
        "inside_warp": 0x7ca4,    #room 5 B2
        "present": False,
    },
    #the cave with 3 push blocks in front of a chest
    "deku forest push block cave stairs": {
        "outside_warp": 0x77d8,   #room 1 72
        "inside_warp": 0x7ca8,    #room 5 B3
        "present": False,
    },
    #the burnable tree that grants access to the HP
    "deku forest heart cave bush stairs": {
        "outside_warp": 0x77e4,   #room 1 91
        "inside_warp": 0x7ca0,    #room 5 B0
        "present": False,
        "item_lock": "Ember Seeds",
        "lock_flag": 0xc891,
        "lock_mask": 0x80,
        "lock_text": 0x5a26
    },
    #stairs that lead to the mystery seed tree
    "mystery seed cave front stairs": {
        "outside_warp": 0x77d4,   #room 1 71
        "inside_warp": 0x7cb0,    #room 5 b5
        "present": False,
    },
    #stairs that lead to the cheap shield deku scrub
    "mystery seed cave back left stairs": {
        "outside_warp": 0x7864,   #room 1 70
        "inside_warp": 0x7dbc,    #room 5 B4, t21
        "present": False,
    },
    #stairs that lead to the mystery seed tree
    "mystery seed cave back right stairs": {
        "outside_warp": 0x7868,   #room 1 70
        "inside_warp": 0x7dc0,    #room 5 B4, t-alot
        "present": False,
    },
#PAST TALUS + SYMMETRY
    "past top left symmetry house": {
        "outside_warp": 0x7750,   #room 1 02
        "inside_warp": 0x79f4,    #room 3 6E
        "present": False,
    },
    "past top right symmetry house": {
        "outside_warp": 0x7770,   #room 1 04
        "inside_warp": 0x79f8,    #room 3 6F
        "present": False,
    },
    "past bottom left symmetry house": {
        "outside_warp": 0x7774,   #room 1 12
        "inside_warp": 0x79fc,    #room 3 7E
        "present": False,
    },
    "past bottom right symmetry house": {
        "outside_warp": 0x777c,   #room 1 14
        "inside_warp": 0x7a00,    #room 3 7F
        "present": False,
    },

    #stairs to basement, left = 93 34 22 and right = 9b 35 22
    "symmetry town hall": {
        "outside_warp": 0x7778,   #room 1 13
        "inside_warp": 0x7da4,    #room 5 F6
        "present": False,
        #basement room 2 e8
    },

    "tokkey dive spot": {
        "outside_warp": 0x7E88,   #room 7 0A
        "inside_warp": 0x7A0C,    #room 3 8F
        "present": False,
    },
    "talus waterfall cave front": {
        "outside_warp": 0x77B4,   #room 1 51
        "inside_warp": 0x78C4,    #room 2 8F
        "present": False,
    },
    "talus waterfall cave left": {
        "outside_warp": 0x784C,   #room 1 41
        "inside_warp": 0x7D64,    #room 5 EA
        "present": False,
    },
    "talus waterfall cave right": {
        "outside_warp": 0x7850,   #room 1 41
        "inside_warp": 0x7D68,    #room 5 EA
        "present": False,
    },

    #stairs to restoration ceremony - 0x7a28
    "patch cave": {
        "outside_warp": 0x778c,   #room 1 23
        "inside_warp": 0x7a2c,    #room 3 BE
        "present": False,
    },
    "restoration wall base cave": {
        "outside_warp": 0x77a8,   #room 1 43
        "inside_warp": 0x7a24,    #room 3 AF
        "present": False,
    },
#AMBI'S PALACE

#secret entrance stairs at 7D14, d2 47 12
    "palace front door": {
        "outside_warp": 0x7758,   #room 1 06
        "inside_warp": 0x7D18,    #room 5 D2
        "present": False,
    },

#upstairs stairs at 7D10, D1 0a 13
    "palace left door": {
        "outside_warp": 0x7754,   #room 1 05
        "inside_warp": 0x7D0C,    #room 5 D1
        "present": False,
    },
    "palace right door": {
        "outside_warp": 0x775C,   #room 1 07
        "inside_warp": 0x7D1C,    #room 5 D3
        "present": False,
    },
    "palace secret entrance": {
        "outside_warp": 0x7828,   #room 1 27
        "inside_warp": 0x782c,    #room 1 E2
        "present": False,
    },
#PAST WEST RIDGE
    "old zora cave": {
        "outside_warp": 0x77c8,   #room 1 5A
        "inside_warp": 0x7954,    #room 2 F5
        "present": False,
    },
    "past goron city lower": {
        "outside_warp": 0x7790,   #room 1 28
        "inside_warp": 0x7CD8,    #room 5 C3
        "present": False,
    },

    #stairs eb 31 5 2, 0x7D70
    "past goron city upper": {
        "outside_warp": 0x7780,   #room 1 18
        "inside_warp": 0x7D6C,    #room 5 EB
        "present": False,
    },
    #cave with two different sized square holes
    "past behind moblin keep cave": {
        "outside_warp": 0x7760,   #room 1 09
        "inside_warp": 0x7d50,    #room 5 E5
        "present": False,
    },
    "treasure hunting goron cave": {
        "outside_warp": 0x783c,   #room 1 0b
        "inside_warp": 0x795c,    #room 2 f7
        "present": False,
    },
    #theres just a lot of seemingly random holes
    "cave left of treasure hunting goron": {
        "outside_warp": 0x7838,   #room 1 0b, t47
        "inside_warp": 0x7D54,    #room 5 E6
        "present": False,
    },
#PAST EAST RIDGE
    "goron face bomb cave": {
        "outside_warp": 0x776C,   #room 1 0d
        "inside_warp": 0x7974,    #room 2 FC
        "present": False,
        "item_lock": "Bombs (10)",
        "lock_flag": 0xc80d,
        "lock_mask": 0x80,
        "lock_text": 0x5a25
    },
    #since you're intended to come from the
    #bottom to reach the top, that's how im labeling this cave
    #cave from past east ridge base to past east ridge upper
    "east ridge lower to upper cave top": {
        "outside_warp": 0x7768,   #room 1 0c
        "inside_warp": 0x79d8,    #room 3 2F
        "present": False,
    },
    #cave from past east ridge upper to east ridge base
    "east ridge lower to upper cave base": {
        "outside_warp": 0x7794,   #room 1 2b
        "inside_warp": 0x7D40,    #room 5 E0
        "present": False,
    },
    "past mermaid cave front porch": {
        "outside_warp": [0x7840,0x7844,0x7848],   #room 1 3c
        "inside_warp": [0x79b8, 0x79bc],    #room 3 0F
        "present": False,
    },

#room 2 EF, graceful goron past
    #staircase upstairs 0x7984, ff 4b 52
    "past goron dance hall lower": {
        "outside_warp": 0x77a4,   #room 1 3D
        "inside_warp": 0x7980,    #room 2 FF
        "present": False,
    },

    "past goron dance hall middle": {
        "outside_warp": 0x7784,   #room 1 1C
        "inside_warp": 0x79C8,    #room 3 1F
        "present": False,
    },
    "goron shooting gallery": {
        "outside_warp": 0x7788,   #room 1 1D
        "inside_warp": 0x7A64,    #room 3 E7
        "present": False,
    },

    "past east ridge fairy cave": {
        "outside_warp": 0x7798,   #room 1 2D
        "inside_warp": 0x7960,    #room 2 F8
        "present": False,
    },
    "generous old man bush": {
        "outside_warp": 0x77B0,   #room 1 4D
        "inside_warp": 0x7A6C,    #room 3 E9
        "present": False,
        "item_lock": "Ember Seeds",
        "lock_flag": 0xc84d,
        "lock_mask": 0x80,
        "lock_text": 0x5a26
    },
#PAST LYNNA SEAS
    "past underwater sea of storms cave": {
        "outside_warp": 0x7A3C,   #room 3 C7
        "inside_warp": 0x7AA8,    #room 3 FF
        "present": False,
        "is_underwater": True,
    },
    "past underwater drifting island cave": {
        "outside_warp": 0x7A38,   #room 3 C5
        "inside_warp": 0x789C,    #room 2 4F
        "present": False,
        "is_underwater": True,
    },
    "past drifting island house": {
        "outside_warp": 0x7808,   #room 1 C5
        "inside_warp": 0x7A44,    #room 3 CF
        "present": False,
    },
    "past underwater zora duplex left": {
        "outside_warp": 0x7AC8,   #room 3 D0
        "inside_warp": 0x7A5C,    #room 3 E5
        "present": False,
        "is_underwater": True,
    },
    "past underwater zora duplex right": {
        "outside_warp": 0x7ACC,   #room 3 D0
        "inside_warp": 0x7A60,    #room 3 E6
        "present": False,
        "is_underwater": True,
    },
    "past underwater zora house": {
        "outside_warp": 0x7A34,   #room 3 C1
        "inside_warp": 0x7A50,    #room 3 DF
        "present": False,
        "is_underwater": True,
    },

    #stairs to throne room 0x7DA0, ae 5f 52
    "past zora palace": {
        "outside_warp": 0x7A1C,   #room 3 A1
        "inside_warp": 0x7D9C,    #room 5 AE
        "present": False,
        "is_underwater": True,
    },

    "past fairy queen cave": {
        "outside_warp": 0x77E8,   #room 1 A3
        "inside_warp": 0x7A84,    #room 3 EF
        "present": False,
    },
    "past library": {
        "outside_warp": 0x77EC,   #room 1 A5
        "inside_warp": 0x7D74,    #room 5 EC
        "present": False,
        "item_lock": "Library Key",
        "lock_flag": 0xc8a5,
        "lock_mask": 0x80,
        "lock_text": 0x5a29
    },
#PAST CRESCENT
    "lost shield tokay cave": {
        "outside_warp": 0x7814,   #room 1 D9
        "inside_warp": 0x7D5C,    #room 5 E9
        "present": False,
    },
    "hero trials cave": {
        "outside_warp": 0x77F8,   #room 1 BA
        "inside_warp": 0x7DB0,    #room 5 F9
        "present": False,
        "item_lock": "Tokay Eyeball",
        "lock_flag": 0xc8ba,
        "lock_mask": 0x80,
        "lock_text": 0x5a2e
    },
    "crystal tokay cave": {
        "outside_warp": 0x77FC,   #room 1 BB
        "inside_warp": 0x7D88,    #room 5 CA
        "present": False,
    },

    #if we figure out dive spots, downward stairs at 0x7DF0
    "flipper tokay cave stairs": {
        "outside_warp": 0x7800,   #room 1 BC
        "inside_warp": 0x7DF4,    #room 5 CC
        "present": False,
    },
    "flipper tokay bomb cave": {
        "outside_warp": 0x780C,   #room 1 CB
        "inside_warp": 0x7CEC,    #room 5 CC
        "present": False,
        "item_lock": "Bombs (10)",
        "lock_flag": 0xc8cb,
        "lock_mask": 0x80,
        "lock_text": 0x5a25
    },

    #$cd warpSource7df6 stairs, too lazy to do rn
    "crescent pot grotto right": {
        "outside_warp": 0x781C,   #room 1 DB
        "inside_warp": 0x7CF8,    #room 5 CD
        "present": False,
    },
    "crescent pot grotto left": {
        "outside_warp": 0x7818,   #room 1 DA
        "inside_warp": 0x7CF4,    #room 5 CD
        "present": False,
    },
    "long hook pot cave": {
        "outside_warp": 0x7820,   #room 1 DD
        "inside_warp": 0x7DAC,    #room 5 F7
        "present": False,
    },

    #hut cave stairs to hut back at 0x79A0
    "past chicken hut stairs": {
        "outside_warp": 0x7870,   #room 1 CD
        "inside_warp": 0x799C,    #room 2 CE
        "present": False,
    },

    #hut back stairs to hut cave at 0x7920
    "past chicken hut front": {
        "outside_warp": 0x786C,   #room 1 CD
        "inside_warp": 0x791C,    #room 2 E3
        "present": False,
    },
    "wild tokay game": {
        "outside_warp": 0x7804,   #room 1 BD
        "inside_warp": 0x7914,    #room 2 DE
        "present": False,
        "item_lock": "Ember Seeds",
        "lock_flag": 0xc8bd,
        "lock_mask": 0x80,
        "lock_text": 0x5a25
    },
    "tokay shop": {
        "outside_warp": 0x77F4,   #room 1 AD
        "inside_warp": 0x7924,    #room 2 E4
        "present": False,
    },

    #ladder to invisible floor room 0x7 E7C
    "underwater hero trials cave": {
        "outside_warp": 0x7A04,   #room 3 8C
        "inside_warp": 0x7E80,    #room 7 08 because sidescroller
        "present": False,
        "is_underwater": True,
    },
    # DUNGEONS
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
        "item_lock": "Bombs (10)",
        "lock_flag": 0xc883,
        "lock_mask": 0x80,
        "lock_text": 0x5a25
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
        "item_lock": "Crown Key",
        "lock_flag": 0xc70a,
        "lock_mask": 0x80,
        "lock_text": 0x5a2a
    },
    "d6 present": {
        "outside_warp": 0x7748,
        "inside_warp": 0x7c48,
        "custom_map_tile": 0x03c,
        "present": True,
        "dungeon": 6,
        "item_lock": "Old Mermaid Key",
        "lock_flag": 0xc80e,
        "lock_mask": 0x80,
        "lock_text": 0x5a2b
    },
    "d7": {
        "outside_warp": 0x7874,
        "inside_warp": 0x7c60,
        "custom_map_tile": 0x090,
        "present": True,
        "dungeon": 7,
        "is_underwater": True,
        "lock_flag": 0xc6d6,
        "lock_mask": 0x02,
        "lock_text": 0x5a2d
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
        "item_lock": "Mermaid Key",
        "lock_flag": 0xc80f,
        "lock_mask": 0x80,
        "lock_text": 0x5a2c
    }
}




#    "maku road front": {
#        "outside_warp": 7708,   #room 0 48
#        #   "inside_warp": ,    #room 4 04
#        "present": True,
#    },

#    "maku road stairs": {
#       #   "outside_warp": ,   #room 0 38
#        #   "inside_warp": ,    #room 4 01
#        "present": True,
#    },

#    "maku tree hole": {
#        #   "outside_warp": ,   #room 0 38
#        #   "inside_warp": ,    #room 5 CF
#        "present": True,
#    },





    # putting this here to be a completionist but I don't think this one should be randomized
    # since the game already cant tell which cave is supposed to be here
#    "nuun animal cave": {
#           "outside_warp": ,
#           "inside_warp": ,
#        "present": True,
#    },
#   nuun ricky inside #room 2 EC
#   nuun moosh inside #room 2 F4
#   nuun dimitri inside #room 5 B8

    # added to be completionist, not sure what we want to do for these entrances
    # since they're not always accessible
    #potentially keep the keep after beating great moblin,
    #but move the cave to the right and be a locked door while great
    #moblin is unbeaten and the stairs to the left over the ledge


#left door is 44 19 24, right door is 46 1a 24
#    "moblin keep left door": {
#        #   "outside_warp": ,   #room 0 09, t40
#        #   "inside_warp": ,   #room 2 9F
#        "present": True,
#    },
#    "moblin keep right door": {
#        #   "outside_warp": ,   #room 0 09, t42
#        #   "inside_warp": ,   #room 2 9F
#        "present": True,
#    },
#room 2 AE, moblin keep center room; room 2 AF, great moblin arena

#    surely we wouldn't be mad enough to do this..... unless?
#    "black tower": {
#        #   "outside_warp": ,   #room 1 76
#        #   "inside_warp": ,    #room 4 E7
#        "present": False,
#    },


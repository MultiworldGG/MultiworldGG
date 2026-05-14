import ctypes

from ...common import TCSContext
from ...common_addresses import StaticUint
from ...common_types import CharacterDataFlag3, CharacterEntryFlag2

p_CharCategoryAddr = StaticUint(0x93b2a0)
p_CHARCATEGORYCOUNT = StaticUint(0x93b28c)


class CharCategory(ctypes.Structure):
    _fields_ = [
        ("name", ctypes.c_uint),  # This is a pointer to the game's memory (char*).
        ("data_flag_3", ctypes.c_uint),
        ("character_entry_flag_2", ctypes.c_uint),
    ]


VANILLA_CATEGORIES = [
    "Jedi",  # CharacterDataFlag3.JEDI
    "JediBaddie",  # CharacterDataFlag3.JEDI | CharacterDataFlag3.BADDIE
    "BountyHunter",  # CharacterDataFlag3.BOUNTY_HUNTER | CharacterDataFlag3.BLASTER | CharacterDataFlag3.ZIPUP
    "Teleport",  # CharacterDataFlag3.TELEPORT (shortie)
    "HighJump",  # CharacterEntryFlag2.CAN_HIGH_JUMP
    "Astromech",  # CharacterDataFlag3.ASTROMECH
    "Protocol",  # CharacterDataFlag3.PROTOCOL
    "ZipUp",  # CharacterDataFlag3.ZIPUP | CharacterDataFlag3.BLASTER
    "Blaster",  # CharacterDataFlag3.BLASTER
    None
]
LSW_CHARCATEGORY_ADDR = 0x007f25f0
# The 10th category is empty to mark the end of the array.
LSW_CHARCATEGORY_SIZE = ctypes.sizeof(CharCategory) * (len(VANILLA_CATEGORIES) - 1)
EXPECTED_BASE_CATEGORY_COUNT = 9
assert EXPECTED_BASE_CATEGORY_COUNT + 1 == len(VANILLA_CATEGORIES)


# Vanilla categories are reproduced with pointers to their original names because there are game functions for looking
# up categories by name.
# Because we are replacing the categories at runtime. Game scripts that use `CategoryIs` and similar, have already
# loaded and initialised, which includes looking up the index of the named category in the `CategoryIs`. This means that
# all the vanilla categories must remain at their original indices, otherwise the AI will try to match characters to
# indices
_CUSTOM_CHAR_CATEGORIES = [
    # Custom category to pick a jetpack character (Boba/Jango Fett).
    # CharacterDataFlag3.JETPACK cannot be used on its own because Geonosion and Watto also have this flag, but cannot
    # hover.
    CharCategory(
        0x007628cc,  # "jetpack"
        CharacterDataFlag3.JETPACK | CharacterDataFlag3.BOUNTY_HUNTER,
        0
    ),
    # Custom category to pick a 'tightrope_walk' character (unused in vanilla, but characters that can use astromech
    # panels are being set to this)
    CharCategory(
        0x00762d10,  # "tightrope_walk"
        0,
        CharacterEntryFlag2.TIGHTROPE_WALK,
    ),
    # Custom category to pick Grievous' Bodyguard or General Grievous first when picking a High Jumper.
    CharCategory(
        0x00754c08,  # "superjedislam"
        CharacterDataFlag3.BADDIE,
        CharacterEntryFlag2.CAN_HIGH_JUMP,
    ),
    # Custom category to pick Droideka (unused in vanilla, but Droideka is being set to this)
    CharCategory(
        0x007627f8,  # "tightrope_tilt"
        0,
        CharacterEntryFlag2.TIGHTROPE_TILT,
    ),
    # Custom category to pick a Yoda character. This flag is for some reason used by a number of Extra Toggle characters
    # in vanilla, but these are not selectable for Free Play. Yoda and Yoda (Ghost) are being given this flag.
    # This is deliberately picked after Droideka, to try to get Droideka and Yoda next to each other in the Free Play
    # character list, due to their relevant speedrunning tricks.
    CharCategory(
        0x00762818,  # "wall_jump"
        0,
        CharacterEntryFlag2.WALL_JUMP,
    ),
    # Custom category to pick a character that can zap. This flag is unused in vanilla, but characters that can zap are
    # being set to have this flag.
    CharCategory(
        0x00762b70,  # "can_zap"
        0,
        CharacterEntryFlag2.GOT_BATARANG,
    ),
    # Custom category to pick a ghost if available.
    CharCategory(
        0x00762e0c,  # "ghost"
        0,
        CharacterEntryFlag2.IS_GHOST,
    ),
    # A category with NULL name at the end signifies the end of the array.
    CharCategory(0, 0, 0)
]


async def set_custom_character_categories(ctx: TCSContext):
    actual_vanilla_category_count = p_CHARCATEGORYCOUNT.get(ctx)
    if actual_vanilla_category_count != EXPECTED_BASE_CATEGORY_COUNT:
        raise Exception(f"Error: Expected {EXPECTED_BASE_CATEGORY_COUNT} vanilla character categories, but found"
                        f" {actual_vanilla_category_count}. Please report this in the Lego Star Wars: The Complete"
                        f" Saga discord channel.")
    # Read the base categories, excluding the empty category at the end.
    vanilla_categories = ctx.read_bytes(LSW_CHARCATEGORY_ADDR, LSW_CHARCATEGORY_SIZE)
    custom_categories = [
        # The name is a pointer to a string in the game's memory, so it needs to be adjusted.
        CharCategory(ctx.adjust_gog_address(c.name), c.data_flag_3, c.character_entry_flag_2)
        for c in _CUSTOM_CHAR_CATEGORIES
    ]
    array_class = CharCategory * len(_CUSTOM_CHAR_CATEGORIES)
    array_instance = array_class(*custom_categories)
    bytes_to_write = vanilla_categories + bytes(array_instance)

    allocated_addr = ctx.allocate(len(bytes_to_write))
    ctx.write_bytes(allocated_addr, bytes_to_write, len(bytes_to_write), raw=True)

    ctx.write_uint(p_CharCategoryAddr, allocated_addr)
    # The last element in the array is empty, signifying the end of the array.
    ctx.write_uint(p_CHARCATEGORYCOUNT, actual_vanilla_category_count + len(custom_categories) - 1)

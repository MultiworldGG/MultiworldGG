# from https://github.com/icebound777/PMR-SeedGenerator/blob/main/metadata/palettes_meta.py
"""Module for modifying sprite palettes"""

from ..data.enum_options import RandomPalettes
from ..data.palettes_meta import (
    mario_n_partner_sprite_names,
    boss_sprite_names,
    enemy_sprite_names,
    hammer_sprite_names,
    special_vanilla_palette_ids,
    palette_table,
)

class CoinPalette:
    def __init__(self, data=None, targets=None, crcs=None) -> None:
        self.data = data
        self.targets = targets
        self.crcs = crcs


def get_randomized_coinpalette(color_id: int):
    """
    Choose and return a color palette for coin sprites in accordance to chosen
    settings, as well as all locations in ROM where the palette needs to be
    written to.
    We do it this way, because
    "swapping these coin palettes at runtime is pretty ugly" (-clover)
    """
    COIN_COLOR_GOLD = 0
    COIN_COLOR_RED = 1
    COIN_COLOR_BLUE = 2
    COIN_COLOR_PURPLE = 3
    COIN_COLOR_SILVER = 4

    # byte data for gold palette (default)
    palette_coin_gold = [
        0x294AE739,
        0xEED5E64F,
        0xE5CDDD49,
        0xBC49AB87,
        0x92C76A09,
        0xC4CB8289,
        0x00010001,
        0x00010001
    ]

    # byte data for red palette
    palette_coin_red = [
        0x294AE739,
        0xEB15E24F,
        0xE18DD90B,
        0xB90DA8CD,
        0x90CF610F,
        0xC14D810F,
        0x00010001,
        0x00010001
    ]

    # byte data for blue palette
    palette_coin_blue = [
        0x294AE739,
        0x653F4C7D,
        0x43BD32FB,
        0x327121AD,
        0x21252119,
        0x3AF3215D,
        0x00010001,
        0x00010001
    ]

    # byte data for purple palette
    palette_coin_purple = [
        0x294AE739,
        0xCC75C2F5,
        0xAA739933,
        0x792B60E7,
        0x50E138D7,
        0x916D491D,
        0x00010001,
        0x00010001
    ]

    # byte data for silver palette
    palette_coin_silver = [
        0x294AE739,
        0xC5F1B5AF,
        0xA52B9CA9,
        0x7BA3631B,
        0x5257294B,
        0x94654211,
        0x00010001,
        0x00010001
    ]

    coin_color_palettes = {
        COIN_COLOR_GOLD: palette_coin_gold,
        COIN_COLOR_RED: palette_coin_red,
        COIN_COLOR_BLUE: palette_coin_blue,
        COIN_COLOR_PURPLE: palette_coin_purple,
        COIN_COLOR_SILVER: palette_coin_silver,
    }

    target_rom_locations = [
        0x09A030,
        0x09A0D0,
        0x09A170,
        0x09A210,
        0x09A2B0,
        0x09A350,
        0x09A3F0,
        0x09A490,
        0x09A530,
        0x09A5D0,
        0x1FB9F0,
        0x1FBB30,
        0x1FBC70,
        0x1FBDB0,
        0x1FBEF0,
        0x1FC030,
        0x1FC170,
        0x1FC2B0,
        0x1FC3F0,
        0x1FC530
    ]

    # temp. unused
    all_coin_palette_crcs = {
        COIN_COLOR_GOLD: [
            0xD4C3F881,
            0xCB3B5A00
        ],
        COIN_COLOR_RED: [
            0x2BCD223A,
            0x3CC7D7D5
        ],
        COIN_COLOR_BLUE: [
            0xEE094F68,
            0x421628A3
        ],
        COIN_COLOR_PURPLE: [
            0xB99EDAC8,
            0x7E0C334A
        ],
        COIN_COLOR_SILVER: [
            0x82A4AB59,
            0xBF600802
        ]
    }

    return coin_color_palettes.get(color_id), target_rom_locations, None


def get_randomized_palettes(world) -> list:
    """
    Set up and return a list of dbkey/value pairs for sprite palette changes,
    according to given settings.
    Each dbkey is associated with one sprite, which in turn has at least two
    color palettes (vanilla palette + at least 1 custom one). If a sprite
    is not found in the dbkeys, then we don't provide custom palettes for it
    yet.
    Some color palettes are shared among several sprites (like for toads,
    toadettes, dryites, or shy guys).
    If a sprite is to be left vanilla, then we have to determine the vanilla
    sprite id first using a local function. The affected sprites have their
    vanilla sprite id encoded in the sprite name.
    """
    def get_vanilla_palette_id(sprite_name: str) -> int:
        if sprite_name not in special_vanilla_palette_ids:
            return 0
        else:
            return int(sprite_name[3:4])

    PALETTEVALUE_ALWAYS_RANDOM = 0xFFFFFFFF

    palettes_data = []
    all_palettes = []

    all_palettes.append(("Mario", world.options.mario_palette.value))
    all_palettes.append(("01_0_Goombario", world.options.goombario_palette.value))
    all_palettes.append(("02_0_Kooper", world.options.kooper_palette.value))
    all_palettes.append(("03_0_Bombette", world.options.bombette_palette.value))
    all_palettes.append(("04_0_Parakarry", world.options.parakarry_palette.value))
    all_palettes.append(("05_0_Bow", world.options.bow_palette.value))
    all_palettes.append(("06_0_Watt", world.options.watt_palette.value))
    all_palettes.append(("07_0_Sushie", world.options.sushie_palette.value))
    all_palettes.append(("08_0_Lakilester", world.options.lakilester_palette.value))

    # Selectable palettes
    for palette_tuple in all_palettes:
        cur_sprite_name = palette_tuple[0]
        cur_option = palette_tuple[1]
        palette_info = palette_table[cur_sprite_name]
        palette_count = palette_info[2]

        # sprite value is 0 for vanilla, 1 to x for a chosen palette,
        # 10 to 12 for one of the random options

        if 0 <= cur_option < palette_count:
            chosen_palette = cur_option
        elif cur_option == RandomPalettes.RANDOM_PICK:
            chosen_palette = world.random.randrange(0, palette_count)
        elif cur_option == RandomPalettes.RANDOM_PICK_NOT_VANILLA:
            chosen_palette = world.random.randrange(1, palette_count)
        elif cur_option == RandomPalettes.ALWAYS_RANDOM:
            chosen_palette = PALETTEVALUE_ALWAYS_RANDOM
        else:
            chosen_palette = get_vanilla_palette_id(cur_sprite_name)
        palettes_data.append((palette_info[1], chosen_palette))

    # Bosses, enemies and general NPC palettes
    for sprite, palette_info in palette_table.items():
        if sprite in mario_n_partner_sprite_names:
            continue

        if sprite in boss_sprite_names:
            cur_setting = RandomPalettes.get_setting_value(world.options.boss_palette.value)
        elif sprite in enemy_sprite_names:
            cur_setting = RandomPalettes.get_setting_value(world.options.enemy_palette.value)
        elif sprite in hammer_sprite_names:
            cur_setting = RandomPalettes.get_setting_value(world.options.hammer_palette.value)
        else:  # other NPC settings
            cur_setting = RandomPalettes.get_setting_value(world.options.npc_palette.value)

        if cur_setting == RandomPalettes.RANDOM_PICK_SETTING:
            palette_count = palette_info[2]
            chosen_palette = world.random.randrange(0, palette_count)
        elif cur_setting == RandomPalettes.RANDOM_PICK_NOT_VANILLA_SETTING:
            palette_count = palette_info[2]
            chosen_palette = world.random.randrange(1, palette_count)
        elif cur_setting == RandomPalettes.ALWAYS_RANDOM_SETTING:
            chosen_palette = PALETTEVALUE_ALWAYS_RANDOM
        else:
            chosen_palette = get_vanilla_palette_id(sprite)
        palettes_data.append((palette_info[1], chosen_palette))

    return palettes_data

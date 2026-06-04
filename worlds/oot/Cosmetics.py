from .Utils import data_path
from .Colors import *
import logging
import os
from itertools import chain
from . import Music as music
from . import Sounds as sfx
from . import IconManip as icon
from Utils import local_path

logger = logging.getLogger('')

# Options are all lowercase and have underscores instead of spaces
# this needs to be undone for the oot generator
def format_cosmetic_option_result(option_result):
    def format_word(word):
        special_words = {
            'nes': 'NES',
            'gamecube': 'GameCube',
            'of': 'of'
        }
        return special_words.get(word, word.capitalize())
    words = option_result.split('_')
    return ' '.join([format_word(word) for word in words])


def patch_targeting(rom, ootworld, symbols):
    # Set default targeting option to Hold
    if ootworld.default_targeting == 'hold':
        rom.write_byte(0xB71E6D, 0x01)
    else:
        rom.write_byte(0xB71E6D, 0x00)


def patch_dpad(rom, ootworld, symbols):
    # Display D-Pad HUD
    if ootworld.display_dpad != 'off':
        rom.write_byte(symbols['CFG_DISPLAY_DPAD'], 0x01)
    else:
        rom.write_byte(symbols['CFG_DISPLAY_DPAD'], 0x00)


def patch_dpad_info(rom, ootworld, symbols):
    # Display D-Pad HUD in pause menu for either dungeon info or equips
    if ootworld.dpad_dungeon_menu:
        rom.write_byte(symbols['CFG_DPAD_DUNGEON_INFO_ENABLE'], 0x01)
    else:
        rom.write_byte(symbols['CFG_DPAD_DUNGEON_INFO_ENABLE'], 0x00)


def patch_music_changes(rom, ootworld, symbols):
    if 'CFG_SPEEDUP_MUSIC_FOR_LAST_TRIFORCE_PIECE' in symbols and hasattr(ootworld, 'speedup_music_for_last_triforce_piece'):
        rom.write_byte(symbols['CFG_SPEEDUP_MUSIC_FOR_LAST_TRIFORCE_PIECE'], int(bool(ootworld.speedup_music_for_last_triforce_piece)))
    if 'CFG_SLOWDOWN_MUSIC_WHEN_LOWHP' in symbols and hasattr(ootworld, 'slowdown_music_when_lowhp'):
        rom.write_byte(symbols['CFG_SLOWDOWN_MUSIC_WHEN_LOWHP'], int(bool(ootworld.slowdown_music_when_lowhp)))


def patch_correct_model_colors(rom, ootworld, symbols):
    if 'CFG_CORRECT_MODEL_COLORS' in symbols and hasattr(ootworld, 'correct_model_colors'):
        rom.write_byte(symbols['CFG_CORRECT_MODEL_COLORS'], int(bool(ootworld.correct_model_colors)))


def patch_yaxis(rom, ootworld, symbols):
    if 'CFG_UNINVERT_YAXIS_IN_FIRST_PERSON_CAMERA' in symbols and hasattr(ootworld, 'uninvert_y_axis_in_first_person_camera'):
        rom.write_byte(symbols['CFG_UNINVERT_YAXIS_IN_FIRST_PERSON_CAMERA'], int(bool(ootworld.uninvert_y_axis_in_first_person_camera)))


def patch_dpad_left(rom, ootworld, symbols):
    if 'CFG_DPAD_ON_THE_LEFT' in symbols:
        rom.write_byte(symbols['CFG_DPAD_ON_THE_LEFT'], 0x01 if ootworld.display_dpad == 'left' else 0x00)


def patch_input_viewer(rom, ootworld, symbols):
    if 'CFG_INPUT_VIEWER' in symbols:
        rom.write_byte(symbols['CFG_INPUT_VIEWER'], int(bool(getattr(ootworld, 'input_viewer', False))))


def patch_song_names(rom, ootworld, symbols):
    if 'CFG_SONG_NAME_STATE' not in symbols:
        return
    mode = getattr(ootworld, 'display_custom_song_names', 'off')
    if mode == 'top':
        rom.write_byte(symbols['CFG_SONG_NAME_STATE'], 0x01)
    elif mode == 'pause':
        rom.write_byte(symbols['CFG_SONG_NAME_STATE'], 0x02)
    else:
        rom.write_byte(symbols['CFG_SONG_NAME_STATE'], 0x00)


def patch_music(rom, ootworld, symbols):
    music_dir = getattr(ootworld, 'music_dir', None) or None
    log = {}
    if ootworld.background_music != 'normal' or ootworld.fanfares != 'normal':
        music.restore_music(rom)
        log, errors = music.randomize_music(rom, ootworld, {}, symbols=symbols, music_dir=music_dir)
        if errors:
            logger.error(errors)
    else:
        music.restore_music(rom)
    if getattr(ootworld, 'disable_battle_music', False):
        rom.write_byte(0xBE447F, 0x00)
    if 'CFG_SONG_NAMES' in symbols:
        # Only write names if music was re-randomized (log non-empty) or the table is uninitialized.
        # This preserves names the generator already wrote when the adjuster runs without re-randomizing.
        first_entry_blank = all(rom.read_byte(symbols['CFG_SONG_NAMES'] + j) == 0 for j in range(50))
        if log or first_entry_blank:
            for i, (name, seq_id) in enumerate(music.bgm_sequence_ids[:47]):
                display_name = log.get(name, name)
                if display_name == 'None':
                    name_bytes = b''
                else:
                    name_bytes = str(display_name)[:49].encode('ascii', errors='replace')
                name_bytes = name_bytes + b'\x00' * (50 - len(name_bytes))
                rom.write_bytes(symbols['CFG_SONG_NAMES'] + i * 50, list(name_bytes))


def patch_model_colors(rom, color, model_addresses):
    main_addresses, dark_addresses, light_addresses = model_addresses

    if color is None:
        for address in main_addresses + dark_addresses + light_addresses:
            original = rom.original.read_bytes(address, 3)
            rom.write_bytes(address, original)
        return

    for address in main_addresses:
        rom.write_bytes(address, color)

    darkened_color = list(map(lambda light: int(max((light - 0x32) * 0.6, 0)), color))
    for address in dark_addresses:
        rom.write_bytes(address, darkened_color)

    lightened_color = list(map(lambda main_color: int(min((main_color / 0.6) + 0x32, 255)), color))
    for address in light_addresses:
        rom.write_bytes(address, lightened_color)


def patch_tunic_icon(rom, tunic, color):
    # patch tunic icon colors
    icon_locations = {
        'Kokiri Tunic': 0x007FE000,
        'Goron Tunic': 0x007FF000,
        'Zora Tunic': 0x00800000,
    }

    if color is not None:
        tunic_icon = icon.generate_tunic_icon(color)
    else:
        tunic_icon = rom.original.read_bytes(icon_locations[tunic], 0x1000)

    rom.write_bytes(icon_locations[tunic], tunic_icon)


def patch_tunic_colors(rom, ootworld, symbols):
    # patch tunic colors
    tunic_address = symbols.get('CFG_TUNIC_COLORS', 0x00B6DA38)
    tunics = [
        ('Kokiri Tunic', 'kokiri_color', tunic_address),
        ('Goron Tunic',  'goron_color',  tunic_address + 3),
        ('Zora Tunic',   'zora_color',   tunic_address + 6),
    ]
    tunic_color_list = get_tunic_colors()

    for tunic, tunic_setting, address in tunics:
        tunic_option = format_cosmetic_option_result(ootworld.__dict__[tunic_setting])

        # handle random
        if tunic_option == 'Random Choice':
            tunic_option = ootworld.random.choice(tunic_color_list)
        # handle completely random
        if tunic_option == 'Completely Random':
            color = generate_random_color()
        # grab the color from the list
        elif tunic_option in tunic_colors:
            color = list(tunic_colors[tunic_option])
        # build color from hex code
        else:
            color = hex_to_color(tunic_option)
            tunic_option = 'Custom'
        # "Weird" weirdshots will crash if the Kokiri Tunic Green value is > 0x99. Brickwall it.
        if ootworld.logic_rules != 'glitchless' and tunic == 'Kokiri Tunic':
            color[1] = min(color[1],0x98)
        rom.write_bytes(address, color)

        # patch the tunic icon
        if [tunic, tunic_option] not in [['Kokiri Tunic', 'Kokiri Green'], ['Goron Tunic', 'Goron Red'], ['Zora Tunic', 'Zora Blue']]:
            patch_tunic_icon(rom, tunic, color)
        else:
            patch_tunic_icon(rom, tunic, None)


def patch_navi_colors(rom, ootworld, symbols):
    # patch navi colors
    navi = [
        # colors for Navi
        ('Navi Idle',            'navi_color_default',
         [0x00B5E184],  # Default (Player)
         symbols.get('CFG_RAINBOW_NAVI_IDLE_INNER_ENABLED', None), symbols.get('CFG_RAINBOW_NAVI_IDLE_OUTER_ENABLED', None)),
        ('Navi Targeting Enemy', 'navi_color_enemy',
            [0x00B5E19C, 0x00B5E1BC],  # Enemy, Boss
            symbols.get('CFG_RAINBOW_NAVI_ENEMY_INNER_ENABLED', None), symbols.get('CFG_RAINBOW_NAVI_ENEMY_OUTER_ENABLED', None)),
        ('Navi Targeting NPC',   'navi_color_npc',
            [0x00B5E194], # NPC
            symbols.get('CFG_RAINBOW_NAVI_NPC_INNER_ENABLED', None), symbols.get('CFG_RAINBOW_NAVI_NPC_OUTER_ENABLED', None)),
        ('Navi Targeting Prop',  'navi_color_prop',
            [0x00B5E174, 0x00B5E17C, 0x00B5E18C, 0x00B5E1A4, 0x00B5E1AC,
             0x00B5E1B4, 0x00B5E1C4, 0x00B5E1CC, 0x00B5E1D4], # Everything else
            symbols.get('CFG_RAINBOW_NAVI_PROP_INNER_ENABLED', None), symbols.get('CFG_RAINBOW_NAVI_PROP_OUTER_ENABLED', None)),
    ]

    navi_color_list = get_navi_colors()
    rainbow_error = None

    for navi_action, navi_setting, navi_addresses, rainbow_inner_symbol, rainbow_outer_symbol in navi:
        navi_option_inner = format_cosmetic_option_result(ootworld.__dict__[navi_setting+'_inner'])
        navi_option_outer = format_cosmetic_option_result(ootworld.__dict__[navi_setting+'_outer'])

        # choose a random choice for the whole group
        if navi_option_inner == 'Random Choice':
            navi_option_inner = ootworld.random.choice(navi_color_list)
        if navi_option_outer == 'Random Choice':
            navi_option_outer = ootworld.random.choice(navi_color_list)

        if navi_option_outer == 'Match Inner':
            navi_option_outer = navi_option_inner

        colors = []
        option_dict = {}
        for address_index, address in enumerate(navi_addresses):
            address_colors = {}
            colors.append(address_colors)
            for index, (navi_part, option, rainbow_symbol) in enumerate([
                ('inner', navi_option_inner, rainbow_inner_symbol),
                ('outer', navi_option_outer, rainbow_outer_symbol),
            ]):
                color = None

                # set rainbow option
                if rainbow_symbol is not None and option == 'Rainbow':
                    rom.write_byte(rainbow_symbol, 0x01)
                    color = [0x00, 0x00, 0x00]
                elif rainbow_symbol is not None:
                    rom.write_byte(rainbow_symbol, 0x00)
                elif option == 'Rainbow':
                    rainbow_error = "Rainbow Navi is not supported by this patch version. Using 'Completely Random' as a substitute."
                    option = 'Completely Random'

                # completely random is random for every subgroup
                if color is None and option == 'Completely Random':
                    color = generate_random_color()

                # grab the color from the list
                if color is None and option in NaviColors:
                    color = list(NaviColors[option][index])

                # build color from hex code
                if color is None:
                    color = hex_to_color(option)
                    option = 'Custom'

                # Check color validity
                if color is None:
                    raise Exception(f'Invalid {navi_part} color {option} for {navi_action}')

                address_colors[navi_part] = color
                option_dict[navi_part] = option

            # write color
            color = address_colors['inner'] + [0xFF] + address_colors['outer'] + [0xFF]
            rom.write_bytes(address, color)


    if rainbow_error:
        logger.error(rainbow_error)


def patch_sword_trails(rom, ootworld, symbols):
    # patch sword trail duration
    rom.write_byte(0x00BEFF8C, ootworld.sword_trail_duration)

    # patch sword trail colors
    sword_trails = [
        ('Sword Trail', 'sword_trail_color',
            [(0x00BEFF7C, 0xB0, 0x40, 0xB0, 0xFF), (0x00BEFF84, 0x20, 0x00, 0x10, 0x00)],
            symbols.get('CFG_RAINBOW_SWORD_INNER_ENABLED', None), symbols.get('CFG_RAINBOW_SWORD_OUTER_ENABLED', None)),
    ]

    sword_trail_color_list = get_sword_trail_colors()
    rainbow_error = None

    for trail_name, trail_setting, trail_addresses, rainbow_inner_symbol, rainbow_outer_symbol in sword_trails:
        option_inner = format_cosmetic_option_result(ootworld.__dict__[trail_setting+'_inner'])
        option_outer = format_cosmetic_option_result(ootworld.__dict__[trail_setting+'_outer'])

        # handle random choice
        if option_inner == 'Random Choice':
            option_inner = ootworld.random.choice(sword_trail_color_list)
        if option_outer == 'Random Choice':
            option_outer = ootworld.random.choice(sword_trail_color_list)

        if option_outer == 'Match Inner':
            option_outer = option_inner

        colors = []
        option_dict = {}
        for address_index, (address, inner_transparency, inner_white_transparency, outer_transparency, outer_white_transparency) in enumerate(trail_addresses):
            address_colors = {}
            colors.append(address_colors)
            transparency_dict = {}
            for index, (trail_part, option, rainbow_symbol, white_transparency, transparency) in enumerate([
                ('inner', option_inner, rainbow_inner_symbol, inner_white_transparency, inner_transparency),
                ('outer', option_outer, rainbow_outer_symbol, outer_white_transparency, outer_transparency),
            ]):
                color = None

                # set rainbow option
                if rainbow_symbol is not None and option == 'Rainbow':
                    rom.write_byte(rainbow_symbol, 0x01)
                    color = [0x00, 0x00, 0x00]
                elif rainbow_symbol is not None:
                    rom.write_byte(rainbow_symbol, 0x00)
                elif option == 'Rainbow':
                    rainbow_error = "Rainbow Sword Trail is not supported by this patch version. Using 'Completely Random' as a substitute."
                    option = 'Completely Random'

                # completely random is random for every subgroup
                if color is None and option == 'Completely Random':
                    color = generate_random_color()

                # grab the color from the list
                if color is None and option in sword_trail_colors:
                    color = list(sword_trail_colors[option])

                # build color from hex code
                if color is None:
                    color = hex_to_color(option)
                    option = 'Custom'

                # Check color validity
                if color is None:
                    raise Exception(f'Invalid {trail_part} color {option} for {trail_name}')

                # handle white transparency
                if option == 'White':
                    transparency_dict[trail_part] = white_transparency
                else:
                    transparency_dict[trail_part] = transparency

                address_colors[trail_part] = color
                option_dict[trail_part] = option

            # write color
            color = address_colors['outer'] + [transparency_dict['outer']] + address_colors['inner'] + [transparency_dict['inner']]
            rom.write_bytes(address, color)

    if rainbow_error:
        logger.error(rainbow_error)


def patch_bombchu_trails(rom, ootworld, symbols):
    # patch bombchu trail colors
    bombchu_trails = [
        ('Bombchu Trail', 'bombchu_trail_color', get_bombchu_trail_colors(), bombchu_trail_colors,
            (symbols['CFG_BOMBCHU_TRAIL_INNER_COLOR'], symbols['CFG_BOMBCHU_TRAIL_OUTER_COLOR'],
             symbols['CFG_RAINBOW_BOMBCHU_TRAIL_INNER_ENABLED'], symbols['CFG_RAINBOW_BOMBCHU_TRAIL_OUTER_ENABLED'])),
    ]

    patch_trails(rom, ootworld, bombchu_trails)


def patch_boomerang_trails(rom, ootworld, symbols):
    # patch boomerang trail colors
    boomerang_trails = [
        ('Boomerang Trail', 'boomerang_trail_color', get_boomerang_trail_colors(), boomerang_trail_colors,
            (symbols['CFG_BOOM_TRAIL_INNER_COLOR'], symbols['CFG_BOOM_TRAIL_OUTER_COLOR'],
             symbols['CFG_RAINBOW_BOOM_TRAIL_INNER_ENABLED'], symbols['CFG_RAINBOW_BOOM_TRAIL_OUTER_ENABLED'])),
    ]

    patch_trails(rom, ootworld, boomerang_trails)


def patch_trails(rom, ootworld, trails):
    for trail_name, trail_setting, trail_color_list, trail_color_dict, trail_symbols in trails:
        color_inner_symbol, color_outer_symbol, rainbow_inner_symbol, rainbow_outer_symbol = trail_symbols
        option_inner = format_cosmetic_option_result(ootworld.__dict__[trail_setting+'_inner'])
        option_outer = format_cosmetic_option_result(ootworld.__dict__[trail_setting+'_outer'])

        # handle random choice
        if option_inner == 'Random Choice':
            option_inner = ootworld.random.choice(trail_color_list)
        if option_outer == 'Random Choice':
            option_outer = ootworld.random.choice(trail_color_list)

        if option_outer == 'Match Inner':
            option_outer = option_inner

        option_dict = {}
        colors = {}

        for index, (trail_part, option, rainbow_symbol, color_symbol) in enumerate([
            ('inner', option_inner, rainbow_inner_symbol, color_inner_symbol),
            ('outer', option_outer, rainbow_outer_symbol, color_outer_symbol),
        ]):
            color = None

            # set rainbow option
            if option == 'Rainbow':
                rom.write_byte(rainbow_symbol, 0x01)
                color = [0x00, 0x00, 0x00]
            else:
                rom.write_byte(rainbow_symbol, 0x00)

            # handle completely random
            if color is None and option == 'Completely Random':
                # Specific handling for inner bombchu trails for contrast purposes.
                if trail_name == 'Bombchu Trail' and trail_part == 'inner':
                    fixed_dark_color = [0, 0, 0]
                    color = [0, 0, 0]
                    # Avoid colors which have a low contrast so the bombchu ticking is still visible
                    while contrast_ratio(color, fixed_dark_color) <= 4:
                        color = generate_random_color()
                else:
                    color = generate_random_color()

            # grab the color from the list
            if color is None and option in trail_color_dict:
                color = list(trail_color_dict[option])

            # build color from hex code
            if color is None:
                color = hex_to_color(option)
                option = 'Custom'

            option_dict[trail_part] = option
            colors[trail_part] = color

            # write color
            rom.write_bytes(color_symbol, color)



def patch_gauntlet_colors(rom, ootworld, symbols):
    # patch gauntlet colors
    gauntlets = [
        ('Silver Gauntlets', 'silver_gauntlets_color', 0x00B6DA44,
            ([0x173B4CC], [0x173B4D4, 0x173B50C, 0x173B514], [])), # GI Model DList colors
        ('Gold Gauntlets', 'golden_gauntlets_color',  0x00B6DA47,
            ([0x173B4EC], [0x173B4F4, 0x173B52C, 0x173B534], [])), # GI Model DList colors
    ]
    gauntlet_color_list = get_gauntlet_colors()

    for gauntlet, gauntlet_setting, address, model_addresses in gauntlets:
        gauntlet_option = format_cosmetic_option_result(ootworld.__dict__[gauntlet_setting])

        # handle random
        if gauntlet_option == 'Random Choice':
            gauntlet_option = ootworld.random.choice(gauntlet_color_list)
        # handle completely random
        if gauntlet_option == 'Completely Random':
            color = generate_random_color()
        # grab the color from the list
        elif gauntlet_option in gauntlet_colors:
            color = list(gauntlet_colors[gauntlet_option])
        # build color from hex code
        else:
            color = hex_to_color(gauntlet_option)
            gauntlet_option = 'Custom'
        rom.write_bytes(address, color)
        if ootworld.correct_model_colors:
            patch_model_colors(rom, color, model_addresses)
        else:
            patch_model_colors(rom, None, model_addresses)

def patch_shield_frame_colors(rom, ootworld, symbols):
    # patch shield frame colors
    shield_frames = [
        ('Mirror Shield Frame', 'mirror_shield_frame_color',
            [0xFA7274, 0xFA776C, 0xFAA27C, 0xFAC564, 0xFAC984, 0xFAEDD4],
            ([0x1616FCC], [0x1616FD4], [])),
    ]
    shield_frame_color_list = get_shield_frame_colors()

    for shield_frame, shield_frame_setting, addresses, model_addresses in shield_frames:
        shield_frame_option = format_cosmetic_option_result(ootworld.__dict__[shield_frame_setting])

        # handle random
        if shield_frame_option == 'Random Choice':
            shield_frame_option = ootworld.random.choice(shield_frame_color_list)
        # handle completely random
        if shield_frame_option == 'Completely Random':
            color = [ootworld.random.getrandbits(8), ootworld.random.getrandbits(8), ootworld.random.getrandbits(8)]
        # grab the color from the list
        elif shield_frame_option in shield_frame_colors:
            color = list(shield_frame_colors[shield_frame_option])
        # build color from hex code
        else:
            color = hex_to_color(shield_frame_option)
            shield_frame_option = 'Custom'
        for address in addresses:
            rom.write_bytes(address, color)
        if ootworld.correct_model_colors and shield_frame_option != 'Red':
            patch_model_colors(rom, color, model_addresses)
        else:
            patch_model_colors(rom, None, model_addresses)


def patch_heart_colors(rom, ootworld, symbols):
    # patch heart colors
    hearts = [
        ('Heart Color', 'heart_color', symbols['CFG_HEART_COLOR'], 0xBB0994,
            ([0x14DA474, 0x14DA594, 0x14B701C, 0x14B70DC, 0x160929C, 0x1609304, 0x160939C],
             [0x14B70FC, 0x14DA494, 0x14DA5B4, 0x14B700C, 0x14B702C, 0x14B703C, 0x14B704C, 0x14B705C,
              0x14B706C, 0x14B707C, 0x14B708C, 0x14B709C, 0x14B70AC, 0x14B70BC, 0x14B70CC, 0x16092A4],
             [0x16092FC, 0x1609394])), # GI Model and Potion DList colors
    ]
    heart_color_list = get_heart_colors()

    for heart, heart_setting, symbol, file_select_address, model_addresses in hearts:
        heart_option = format_cosmetic_option_result(ootworld.__dict__[heart_setting])

        # handle random
        if heart_option == 'Random Choice':
            heart_option = ootworld.random.choice(heart_color_list)
        # handle completely random
        if heart_option == 'Completely Random':
            color = generate_random_color()
        # grab the color from the list
        elif heart_option in heart_colors:
            color = list(heart_colors[heart_option])
        # build color from hex code
        else:
            color = hex_to_color(heart_option)
            heart_option = 'Custom'
        rom.write_int16s(symbol, color) # symbol for ingame HUD
        rom.write_int16s(file_select_address, color) # file select normal hearts
        if heart_option != 'Red':
            rom.write_int16s(file_select_address + 6, color) # file select DD hearts
        else:
            original_dd_color = rom.original.read_bytes(file_select_address + 6, 6)
            rom.write_bytes(file_select_address + 6, original_dd_color)
        if ootworld.correct_model_colors and heart_option != 'Red':
            patch_model_colors(rom, color, model_addresses) # heart model colors
            icon.patch_overworld_icon(rom, color, 0xF43D80) # Overworld Heart Icon
        else:
            patch_model_colors(rom, None, model_addresses)
            icon.patch_overworld_icon(rom, None, 0xF43D80)

def patch_magic_colors(rom, ootworld, symbols):
    # patch magic colors
    magic = [
        ('Magic Meter Color', 'magic_color', symbols["CFG_MAGIC_COLOR"],
            ([0x154C654, 0x154CFB4, 0x160927C, 0x160927C, 0x16092E4, 0x1609344],
             [0x154C65C, 0x154CFBC, 0x1609284],
             [0x16092DC, 0x160933C])), # GI Model and Potion DList colors
    ]
    magic_color_list = get_magic_colors()

    for magic_color, magic_setting, symbol, model_addresses in magic:
        magic_option = format_cosmetic_option_result(ootworld.__dict__[magic_setting])

        if magic_option == 'Random Choice':
           magic_option = ootworld.random.choice(magic_color_list)

        if magic_option == 'Completely Random':
            color = generate_random_color()
        elif magic_option in magic_colors:
            color = list(magic_colors[magic_option])
        else:
            color = hex_to_color(magic_option)
            magic_option = 'Custom'
        rom.write_int16s(symbol, color)
        if magic_option != 'Green' and ootworld.correct_model_colors:
            patch_model_colors(rom, color, model_addresses)
            icon.patch_overworld_icon(rom, color, 0xF45650, data_path('icons/magicSmallExtras.raw')) # Overworld Small Pot
            icon.patch_overworld_icon(rom, color, 0xF47650, data_path('icons/magicLargeExtras.raw')) # Overworld Big Pot
        else:
            patch_model_colors(rom, None, model_addresses)
            icon.patch_overworld_icon(rom, None, 0xF45650)
            icon.patch_overworld_icon(rom, None, 0xF47650)

def patch_button_colors(rom, ootworld, symbols):
    buttons = [
        ('A Button Color', 'a_button_color', a_button_colors,
            [('A Button Color', symbols['CFG_A_BUTTON_COLOR'],
                None),
             ('Text Cursor Color', symbols['CFG_TEXT_CURSOR_COLOR'],
                [(0xB88E81, 0xB88E85, 0xB88E9)]), # Initial Inner Color
             ('Shop Cursor Color', symbols['CFG_SHOP_CURSOR_COLOR'],
                None),
             ('Save/Death Cursor Color', None,
                [(0xBBEBC2, 0xBBEBC3, 0xBBEBD6), (0xBBEDDA, 0xBBEDDB, 0xBBEDDE)]), # Save Cursor / Death Cursor
             ('Pause Menu A Cursor Color', None,
                [(0xBC7849, 0xBC784B, 0xBC784D), (0xBC78A9, 0xBC78AB, 0xBC78AD), (0xBC78BB, 0xBC78BD, 0xBC78BF)]), # Inner / Pulse 1 / Pulse 2
             ('Pause Menu A Icon Color', None,
                [(0x845754, 0x845755, 0x845756)]),
             ('A Note Color', symbols['CFG_A_NOTE_COLOR'], # For Textbox Song Display
                [(0xBB299A, 0xBB299B, 0xBB299E), (0xBB2C8E, 0xBB2C8F, 0xBB2C92), (0xBB2F8A, 0xBB2F8B, 0xBB2F96)]), # Pause Menu Song Display
            ]),
        ('B Button Color', 'b_button_color', b_button_colors,
            [('B Button Color', symbols['CFG_B_BUTTON_COLOR'],
                None),
            ]),
        ('C Button Color', 'c_button_color', c_button_colors,
            [('C Button Color', symbols['CFG_C_BUTTON_COLOR'],
                None),
             ('Pause Menu C Cursor Color', None,
                [(0xBC7843, 0xBC7845, 0xBC7847), (0xBC7891, 0xBC7893, 0xBC7895), (0xBC78A3, 0xBC78A5, 0xBC78A7)]), # Inner / Pulse 1 / Pulse 2
             ('Pause Menu C Icon Color', None,
                [(0x8456FC, 0x8456FD, 0x8456FE)]),
             ('C Note Color', symbols['CFG_C_NOTE_COLOR'], # For Textbox Song Display
                [(0xBB2996, 0xBB2997, 0xBB29A2), (0xBB2C8A, 0xBB2C8B, 0xBB2C96), (0xBB2F86, 0xBB2F87, 0xBB2F9A)]), # Pause Menu Song Display
            ]),
        ('Start Button Color', 'start_button_color', start_button_colors,
            [('Start Button Color', None,
                [(0xAE9EC6, 0xAE9EC7, 0xAE9EDA)]),
            ]),
    ]

    for button, button_setting, button_colors, patches in buttons:
        button_option = format_cosmetic_option_result(ootworld.__dict__[button_setting])
        color_set = None
        colors = {}

        # handle random
        if button_option == 'Random Choice':
            button_option = ootworld.random.choice(list(button_colors.keys()))
        # handle completely random
        if button_option == 'Completely Random':
            fixed_font_color = [10, 10, 10]
            color = [0, 0, 0]
            # Avoid colors which have a low contrast with the font inside buttons (eg. the A letter)
            while contrast_ratio(color, fixed_font_color) <= 3:
                color = generate_random_color()
        # grab the color from the list
        elif button_option in button_colors:
            color_set = [button_colors[button_option]] if isinstance(button_colors[button_option][0], int) else list(button_colors[button_option])
            color = color_set[0]
        # build color from hex code
        else:
            color = hex_to_color(button_option)
            button_option = 'Custom'

        # apply all button color patches
        for i, (patch, symbol, byte_addresses) in enumerate(patches):
            if color_set is not None and len(color_set) > i and color_set[i]:
                colors[patch] = color_set[i]
            else:
                colors[patch] = color

            if symbol:
                rom.write_int16s(symbol, colors[patch])

            if byte_addresses:
                for r_addr, g_addr, b_addr in byte_addresses:
                    rom.write_byte(r_addr, colors[patch][0])
                    rom.write_byte(g_addr, colors[patch][1])
                    rom.write_byte(b_addr, colors[patch][2])


def patch_sfx(rom, ootworld, symbols):
    # Configurable Sound Effects
    sfx_config = [
          ('sfx_navi_overworld',  sfx.SoundHooks.NAVI_OVERWORLD),
          ('sfx_navi_enemy',      sfx.SoundHooks.NAVI_ENEMY),
          ('sfx_low_hp',          sfx.SoundHooks.HP_LOW),
          ('sfx_menu_cursor',     sfx.SoundHooks.MENU_CURSOR),
          ('sfx_menu_select',     sfx.SoundHooks.MENU_SELECT),
          ('sfx_nightfall',       sfx.SoundHooks.NIGHTFALL),
          ('sfx_horse_neigh',     sfx.SoundHooks.HORSE_NEIGH),
          ('sfx_hover_boots',     sfx.SoundHooks.BOOTS_HOVER),
          ('sfx_iron_boots',      sfx.SoundHooks.BOOTS_IRON),
          ('sfx_silver_rupee',    sfx.SoundHooks.SILVER_RUPEE),
          ('sfx_boomerang_throw', sfx.SoundHooks.BOOMERANG_THROW),
          ('sfx_hookshot_chain',  sfx.SoundHooks.HOOKSHOT_CHAIN),
          ('sfx_arrow_shot',      sfx.SoundHooks.ARROW_SHOT),
          ('sfx_slingshot_shot',  sfx.SoundHooks.SLINGSHOT_SHOT),
          ('sfx_magic_arrow_shot',sfx.SoundHooks.MAGIC_ARROW_SHOT),
          ('sfx_bombchu_move',    sfx.SoundHooks.BOMBCHU_MOVE),
          ('sfx_get_small_item',  sfx.SoundHooks.GET_SMALL_ITEM),
          ('sfx_explosion',       sfx.SoundHooks.EXPLOSION),
          ('sfx_daybreak',        sfx.SoundHooks.DAYBREAK),
          ('sfx_cucco',           sfx.SoundHooks.CUCCO),
    ]
    # These hooks store sound IDs with the SFX bank bit set; strip it before writing
    sfx_flag_hooks = {sfx.SoundHooks.BOOTS_HOVER, sfx.SoundHooks.BOOMERANG_THROW, sfx.SoundHooks.HOOKSHOT_CHAIN, sfx.SoundHooks.BOMBCHU_MOVE}

    sound_dict = sfx.get_patch_dict()

    for setting, hook in sfx_config:
        selection = ootworld.__dict__[setting].replace('_', '-')

        if selection == 'default':
            for loc in hook.value.locations:
                sound_id = rom.original.read_int16(loc)
                rom.write_int16(loc, sound_id)
        else:
            if selection == 'random-choice':
                selection = ootworld.random.choice(sfx.get_hook_pool(hook)).value.keyword
            elif selection == 'random-ear-safe':
                selection = ootworld.random.choice(sfx.get_hook_pool(hook, True)).value.keyword
            elif selection == 'completely-random':
                selection = ootworld.random.choice(sfx.standard).value.keyword
            sound_id = sound_dict[selection]
            if hook in sfx_flag_hooks and sound_id > 0x7FF:
                sound_id -= 0x800
            for loc in hook.value.locations:
                rom.write_int16(loc, sound_id)

        if setting == 'sfx_get_small_item' and 'GET_ITEM_SEQ_ID' in symbols:
            rom.write_int16(symbols['GET_ITEM_SEQ_ID'], sound_id if selection != 'default' else rom.original.read_int16(hook.value.locations[0]))



def patch_instrument(rom, ootworld, symbols):
    # Player Instrument
    instruments = {
           #'none':            0x00,
            'ocarina':         0x01,
            'malon':           0x02,
            'whistle':         0x03,
            'harp':            0x04,
            'grind_organ':     0x05,
            'flute':           0x06,
           #'another_ocarina': 0x07,
    }

    choice = ootworld.sfx_ocarina
    if choice == 'random-choice':
        choice = ootworld.random.choice(list(instruments.keys()))

    rom.write_byte(0x00B53C7B, instruments[choice])
    rom.write_byte(0x00B4BF6F, instruments[choice]) # For Lost Woods Skull Kids' minigame in Lost Woods


def _voice_age_name(age):
    return 'Child' if age == 0 else 'Adult'


def _voice_base_path(*parts):
    return os.path.join(data_path('Voices'), *parts)


def _voice_user_path(*parts):
    return local_path('voices', 'oot', *parts)


def _voice_roots(age_name):
    return [
        _voice_user_path(age_name),
        _voice_base_path(age_name),
    ]


def get_voice_choices(age, include_random=True):
    age_name = _voice_age_name(age) if isinstance(age, int) else age
    choices = {'default': 'Default', 'silent': 'Silent'}
    for root in reversed(_voice_roots(age_name)):
        if not os.path.isdir(root):
            continue
        for entry in os.listdir(root):
            path = os.path.join(root, entry)
            if os.path.isdir(path):
                choices[entry.casefold()] = entry
    names = list(choices.values())
    if include_random and len(names) > 2:
        names.append('Random')
    return names


def _normalize_voice_setting(voice_setting):
    voice_setting = str(voice_setting or 'Default').strip().replace('_', ' ')
    special_names = {
        'default': 'Default',
        'silent': 'Silent',
        'random': 'Random',
    }
    return special_names.get(voice_setting.casefold(), voice_setting)


def _find_voice_path(age_name, voice_setting):
    for root in _voice_roots(age_name):
        candidate = os.path.join(root, voice_setting)
        if os.path.isdir(candidate):
            return candidate
        if not os.path.isdir(root):
            continue
        for entry in os.listdir(root):
            if entry.casefold() == voice_setting.casefold():
                return os.path.join(root, entry)
    return None


def _find_silent_voice_path():
    for path in (_voice_user_path('SilentVoiceSFX.bin'), _voice_base_path('SilentVoiceSFX.bin')):
        if os.path.isfile(path):
            return path
    return None


def read_default_voice_data(rom):
    audiobank = 0xD390
    audiotable = 0x79470
    soundbank = audiobank + rom.read_int32(audiobank + 0x4)
    n_sfx = 0x88

    soundbank_entries = {}
    for i in range(n_sfx):
        audiobank_offset = rom.read_int32(soundbank + i * 0x8)
        sfxid = f"00-00{i:02x}"
        soundbank_entries[sfxid] = {
            "length": rom.read_int32(audiobank + audiobank_offset),
            "romoffset": audiotable + rom.read_int32(audiobank + audiobank_offset + 0x4),
        }
    return soundbank_entries


def _patch_voice_bin(rom, sfxid, binsfx, soundbank_entries, source_name):
    if sfxid not in soundbank_entries:
        logger.error(f"Voice patch skipped unknown SFX file {source_name}.")
        return
    length = soundbank_entries[sfxid]["length"]
    rom.write_bytes(soundbank_entries[sfxid]["romoffset"], binsfx.ljust(length, b'\0'))


def patch_silent_voice(rom, sfxidlist, soundbank_entries):
    voice_path = _find_silent_voice_path()
    if voice_path is None:
        logger.error(f"Could not find silent voice sfx at {_voice_user_path('SilentVoiceSFX.bin')} or {_voice_base_path('SilentVoiceSFX.bin')}. Skipping voice patching.")
        return

    with open(voice_path, 'rb') as binsfxin:
        binsfx = bytearray(binsfxin.read())

    for decid in sfxidlist:
        sfxid = f"00-00{decid:02x}"
        _patch_voice_bin(rom, sfxid, binsfx, soundbank_entries, voice_path)


def apply_voice_patch(rom, voice_path, soundbank_entries):
    for binsfxfilename in os.listdir(voice_path):
        if not binsfxfilename.lower().endswith(".bin"):
            continue
        sfxid = binsfxfilename.split('.')[0].lower()
        bin_path = os.path.join(voice_path, binsfxfilename)
        with open(bin_path, 'rb') as binsfxin:
            binsfx = bytearray(binsfxin.read())
        _patch_voice_bin(rom, sfxid, binsfx, soundbank_entries, bin_path)


def patch_voices(rom, ootworld, symbols):
    rom.write_bytes(0x00079470, rom.original.read_bytes(0x00079470, 0x460AD0))

    soundbank_entries = read_default_voice_data(rom)
    voice_ages = (
        ('Child', getattr(ootworld, 'sfx_link_child', 'Default'), get_voice_choices(0, False), chain([0x14, 0x87], range(0x1C, 0x36 + 1), range(0x3E, 0x4C + 1))),
        ('Adult', getattr(ootworld, 'sfx_link_adult', 'Default'), get_voice_choices(1, False), chain([0x37, 0x38, 0x3C, 0x3D, 0x86], range(0x00, 0x13 + 1), range(0x15, 0x1B + 1), range(0x4D, 0x58 + 1))),
    )

    for age_name, voice_setting, choices, silence_sfx_ids in voice_ages:
        voice_setting = _normalize_voice_setting(voice_setting)
        if voice_setting == 'Random':
            random_choices = [choice for choice in choices if choice not in {'Default', 'Silent'}]
            voice_setting = ootworld.random.choice(random_choices) if random_choices else 'Default'

        if voice_setting == 'Silent':
            patch_silent_voice(rom, silence_sfx_ids, soundbank_entries)
        elif voice_setting != 'Default':
            voice_path = _find_voice_path(age_name, voice_setting)
            if voice_path is None:
                logger.error(f"{age_name} Voice not patched: Cannot find voice data directory for {voice_setting}.")
                continue
            apply_voice_patch(rom, voice_path, soundbank_entries)


legacy_cosmetic_data_headers = [
    0x03481000,
    0x03480810,
]

patch_sets = {}
global_patch_sets = [
    patch_targeting,
    patch_music,
    patch_tunic_colors,
    patch_navi_colors,
    patch_sword_trails,
    patch_gauntlet_colors,
    patch_shield_frame_colors,
    # patch_voices,
    patch_sfx,
    patch_instrument,
]

# 3.14.1
patch_sets[0x1F04FA62] = {
    "patches": [
        patch_dpad,
        patch_sword_trails,
    ],
    "symbols": {
        "CFG_DISPLAY_DPAD": 0x0004,
        "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x0005,
        "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x0006,
    },
}

# 3.14.11
patch_sets[0x1F05D3F9] = {
    "patches": patch_sets[0x1F04FA62]["patches"] + [],
    "symbols": {**patch_sets[0x1F04FA62]["symbols"]},
}

# 4.5.7
patch_sets[0x1F0693FB] = {
    "patches": patch_sets[0x1F05D3F9]["patches"] + [
        patch_heart_colors,
        patch_magic_colors,
    ],
    "symbols": {
        "CFG_MAGIC_COLOR": 0x0004,
        "CFG_HEART_COLOR": 0x000A,
        "CFG_DISPLAY_DPAD": 0x0010,
        "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x0011,
        "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x0012,
    }
}

# 5.2.6
patch_sets[0x1F073FC9] = {
    "patches": patch_sets[0x1F0693FB]["patches"] + [
        patch_button_colors,
    ],
    "symbols": {
        "CFG_MAGIC_COLOR": 0x0004,
        "CFG_HEART_COLOR": 0x000A,
        "CFG_A_BUTTON_COLOR": 0x0010,
        "CFG_B_BUTTON_COLOR": 0x0016,
        "CFG_C_BUTTON_COLOR": 0x001C,
        "CFG_TEXT_CURSOR_COLOR": 0x0022,
        "CFG_SHOP_CURSOR_COLOR": 0x0028,
        "CFG_A_NOTE_COLOR": 0x002E,
        "CFG_C_NOTE_COLOR": 0x0034,
        "CFG_DISPLAY_DPAD": 0x003A,
        "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x003B,
        "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x003C,
    }
}

# 5.2.76
patch_sets[0x1F073FD8] = {
    "patches": patch_sets[0x1F073FC9]["patches"] + [
        patch_navi_colors,
        patch_boomerang_trails,
        patch_bombchu_trails,
    ],
    "symbols": {
        **patch_sets[0x1F073FC9]["symbols"],
        "CFG_BOOM_TRAIL_INNER_COLOR": 0x003A,
        "CFG_BOOM_TRAIL_OUTER_COLOR": 0x003D,
        "CFG_BOMBCHU_TRAIL_INNER_COLOR": 0x0040,
        "CFG_BOMBCHU_TRAIL_OUTER_COLOR": 0x0043,
        "CFG_DISPLAY_DPAD": 0x0046,
        "CFG_RAINBOW_SWORD_INNER_ENABLED": 0x0047,
        "CFG_RAINBOW_SWORD_OUTER_ENABLED": 0x0048,
        "CFG_RAINBOW_BOOM_TRAIL_INNER_ENABLED": 0x0049,
        "CFG_RAINBOW_BOOM_TRAIL_OUTER_ENABLED": 0x004A,
        "CFG_RAINBOW_BOMBCHU_TRAIL_INNER_ENABLED": 0x004B,
        "CFG_RAINBOW_BOMBCHU_TRAIL_OUTER_ENABLED": 0x004C,
        "CFG_RAINBOW_NAVI_IDLE_INNER_ENABLED": 0x004D,
        "CFG_RAINBOW_NAVI_IDLE_OUTER_ENABLED": 0x004E,
        "CFG_RAINBOW_NAVI_ENEMY_INNER_ENABLED": 0x004F,
        "CFG_RAINBOW_NAVI_ENEMY_OUTER_ENABLED": 0x0050,
        "CFG_RAINBOW_NAVI_NPC_INNER_ENABLED": 0x0051,
        "CFG_RAINBOW_NAVI_NPC_OUTER_ENABLED": 0x0052,
        "CFG_RAINBOW_NAVI_PROP_INNER_ENABLED": 0x0053,
        "CFG_RAINBOW_NAVI_PROP_OUTER_ENABLED": 0x0054,
    }
}

# 6.2.218
patch_sets[0x1F073FD9] = {
    "patches": patch_sets[0x1F073FD8]["patches"] + [
        patch_dpad_info,
    ],
    "symbols": {
        **patch_sets[0x1F073FD8]["symbols"],
        "CFG_DPAD_DUNGEON_INFO_ENABLE": 0x0055,
    }
}

# 7.1.79
patch_sets[0x1F073FDA] = {
    "patches": patch_sets[0x1F073FD9]["patches"] + [
        patch_sfx,
    ],
    "symbols": {
        **patch_sets[0x1F073FD9]["symbols"],
        "GET_ITEM_SEQ_ID": 0x0056,
    }
}

# 7.1.96
patch_sets[0x1F073FDB] = {
    "patches": patch_sets[0x1F073FDA]["patches"] + [
        patch_tunic_colors,
    ],
    "symbols": {
        **patch_sets[0x1F073FDA]["symbols"],
        "CFG_RAINBOW_TUNIC_ENABLED": 0x005A,
        "CFG_TUNIC_COLORS": 0x005B,
    }
}

# 7.1.110
patch_sets[0x1F073FDC] = {
    "patches": patch_sets[0x1F073FDB]["patches"] + [
        patch_music_changes,
    ],
    "symbols": {
        **patch_sets[0x1F073FDB]["symbols"],
        "CFG_SPEEDUP_MUSIC_FOR_LAST_TRIFORCE_PIECE": 0x0058,
        "CFG_SLOWDOWN_MUSIC_WHEN_LOWHP": 0x0059,
    }
}

# 7.1.123
patch_sets[0x1F073FDD] = {
    "patches": patch_sets[0x1F073FDC]["patches"] + [
        patch_music,  # Versioned after custom instrument-set support.
    ],
    "symbols": {
        **patch_sets[0x1F073FDC]["symbols"],
        "CFG_AUDIOBANK_TABLE_EXTENDED_ADDR": 0x0064,
    }
}

# 7.1.134
patch_sets[0x1F073FDE] = {
    "patches": patch_sets[0x1F073FDD]["patches"] + [
        patch_correct_model_colors,
    ],
    "symbols": {
        **patch_sets[0x1F073FDD]["symbols"],
        "CFG_CORRECT_MODEL_COLORS": 0x0068,
    }
}

# 7.1.144
patch_sets[0x1F073FDF] = {
    "patches": patch_sets[0x1F073FDE]["patches"] + [
        patch_yaxis,
    ],
    "symbols": {
        **patch_sets[0x1F073FDE]["symbols"],
        "CFG_UNINVERT_YAXIS_IN_FIRST_PERSON_CAMERA": 0x0069,
    }
}

# 8.0
patch_sets[0x1F073FE0] = {
    "patches": patch_sets[0x1F073FDF]["patches"] + [
        patch_dpad_left,
    ],
    "symbols": {
        **patch_sets[0x1F073FDF]["symbols"],
        "CFG_DPAD_ON_THE_LEFT": 0x006A,
    }
}

# 8.1.4
patch_sets[0x1F073FE1] = {
    "patches": patch_sets[0x1F073FE0]["patches"] + [
        patch_input_viewer,
    ],
    "symbols": {
        **patch_sets[0x1F073FE0]["symbols"],
        "CFG_INPUT_VIEWER": 0x006B,
    }
}

# 8.1.29
patch_sets[0x1F073FE2] = {
    "patches": patch_sets[0x1F073FE1]["patches"] + [
        patch_song_names,
    ],
    "symbols": {
        **patch_sets[0x1F073FE1]["symbols"],
        "CFG_SONG_NAME_STATE": 0x006C,
        "CFG_SONG_NAMES": 0x006D,
    }
}


def patch_cosmetics(ootworld, rom):
    from worlds.oot.Models import patch_model_adult, patch_model_child

    # try to detect the cosmetic patch data format
    versioned_patch_set = None
    cosmetic_context = rom.read_int32(rom.sym('RANDO_CONTEXT') + 4)
    if cosmetic_context >= 0x80000000 and cosmetic_context <= 0x80F7FFFC:
        cosmetic_context = (cosmetic_context - 0x80400000) + 0x3480000 # convert from RAM to ROM address
        cosmetic_version = rom.read_int32(cosmetic_context)
        versioned_patch_set = patch_sets.get(cosmetic_version)
    else:
        # If cosmetic_context is not a valid pointer, then try to
        # search over all possible legacy header locations.
        for header in legacy_cosmetic_data_headers:
            cosmetic_context = header
            cosmetic_version = rom.read_int32(cosmetic_context)
            if cosmetic_version in patch_sets:
                versioned_patch_set = patch_sets[cosmetic_version]
                break

    # patch version specific patches
    if versioned_patch_set:
        # offset the cosmetic_context struct for absolute addressing
        cosmetic_context_symbols = {
            sym: address + cosmetic_context
            for sym, address in versioned_patch_set['symbols'].items()
        }

        # warn if patching a legacy format
        if cosmetic_version != rom.read_int32(rom.sym('COSMETIC_FORMAT_VERSION')):
            logger.error("ROM uses old cosmetic patch format.")

        # patch cosmetics that use vanilla oot data, and always compatible
        for patch_func in [patch for patch in global_patch_sets if patch not in versioned_patch_set['patches']]:
            patch_func(rom, ootworld, {})

        for patch_func in versioned_patch_set['patches']:
            patch_func(rom, ootworld, cosmetic_context_symbols)
    else:
        # patch cosmetics that use vanilla oot data, and always compatible
        for patch_func in global_patch_sets:
            patch_func(rom, ootworld, {})

        # Unknown patch format
        logger.error("Unable to patch some cosmetics. ROM uses unknown cosmetic patch format.")

    # adjuster-only; skipped during normal generation
    if getattr(ootworld, 'model_adult', 'Default') != 'Default' or getattr(ootworld, 'model_adult_filepicker', ''):
        patch_model_adult(rom, ootworld)
    if getattr(ootworld, 'model_child', 'Default') != 'Default' or getattr(ootworld, 'model_child_filepicker', ''):
        patch_model_child(rom, ootworld)

import tkinter as tk
import argparse
import logging
import os
import zipfile
from itertools import chain

from BaseClasses import MultiWorld
from Options import Choice, Range, Toggle
from worlds.oot import OOTWorld, launch_rom as launch_oot_rom
from worlds.oot.Cosmetics import patch_cosmetics
from worlds.oot.Options import (cosmetic_options, sfx_options,
    DpadDungeonMenu, SpeedupMusicForLastTriforcePiece, SlowdownMusicWhenLowhp,
    UninvertYAxisInFirstPersonCamera, InputViewer, DisableBattleMusic, CreditsMusic)
from worlds.oot.Rom import Rom, compress_rom_file
from worlds.oot.N64Patch import apply_patch_file
from Utils import local_path, user_path

logger = logging.getLogger('OoTAdjuster')


def launch_rom(path: str) -> None:
    launch_oot_rom(path, logger)


def main(launcher_args):
    parser = argparse.ArgumentParser()

    parser.add_argument('--rom', default='', 
        help='Path to an OoT randomized ROM to adjust.')
    parser.add_argument('--vanilla_rom', default='',
        help='Path to a vanilla OoT ROM for patching.')
    for name, option in chain(cosmetic_options.items(), sfx_options.items()):
        parser.add_argument('--'+name, default=None,
            help=option.__doc__)
    parser.add_argument('--music_dir', default=None,
        help='Path to a folder of custom music files (.ootrs, .mmrs) to include in randomization.')
    parser.add_argument('--model_adult', default='Default',
        help='Adult Link model name from data/Models/Adult/ folder, or Default.')
    parser.add_argument('--model_child', default='Default',
        help='Child Link model name from data/Models/Child/ folder, or Default.')
    parser.add_argument('--deathlink',
        help='Enable DeathLink system', action='store_true')

    args = parser.parse_args(launcher_args)
    if not os.path.isfile(args.rom):
        adjustGUI()
    else:
        adjust(args)

def adjustGUI():
    from tkinter import Tk, LEFT, BOTTOM, TOP, E, W, \
        StringVar, IntVar, Checkbutton, Frame, Label, X, Entry, Button, \
        OptionMenu, filedialog, messagebox, ttk
    from argparse import Namespace
    from Utils import __version__ as MWVersion
    try:
        from Utils import instance_name as apname
    except ImportError:
        apname = "Archipelago"

    window = tk.Tk()
    window.wm_title(f"{apname} {MWVersion} OoT Adjuster")
    set_icon(window)

    opts = Namespace()

    # Select ROM
    romDialogFrame = Frame(window)
    romLabel = Label(romDialogFrame, text='Rom/patch to adjust')
    vanillaLabel = Label(romDialogFrame, text='OoT Base Rom')
    opts.rom = StringVar()
    opts.vanilla_rom = StringVar(value="The Legend of Zelda - Ocarina of Time.z64")
    romEntry = Entry(romDialogFrame, textvariable=opts.rom)
    vanillaEntry = Entry(romDialogFrame, textvariable=opts.vanilla_rom)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64", ".apz5")), ("All Files", "*")])
        opts.rom.set(rom)
    def VanillaSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        opts.vanilla_rom.set(rom)

    romSelectButton = Button(romDialogFrame, text='Select Rom', command=RomSelect)
    vanillaSelectButton = Button(romDialogFrame, text='Select Rom', command=VanillaSelect)
    romDialogFrame.pack(side=TOP, expand=True, fill=X)
    romLabel.pack(side=LEFT)
    romEntry.pack(side=LEFT, expand=True, fill=X)
    romSelectButton.pack(side=LEFT)
    vanillaLabel.pack(side=LEFT)
    vanillaEntry.pack(side=LEFT, expand=True, fill=X)
    vanillaSelectButton.pack(side=LEFT)

    # Custom music folder picker
    musicFolderFrame = Frame(window)
    musicFolderLabel = Label(musicFolderFrame, text='Custom Music Folder (.ootrs/.mmrs)')
    opts.music_dir = StringVar()

    def MusicDirSelect():
        d = filedialog.askdirectory(title='Select Custom Music Folder')
        if d:
            opts.music_dir.set(d)

    musicFolderEntry = Entry(musicFolderFrame, textvariable=opts.music_dir)
    musicFolderButton = Button(musicFolderFrame, text='Select Folder', command=MusicDirSelect)
    musicFolderFrame.pack(side=TOP, expand=True, fill=X)
    musicFolderLabel.pack(side=LEFT)
    musicFolderEntry.pack(side=LEFT, expand=True, fill=X)
    musicFolderButton.pack(side=LEFT)

    from worlds.oot.Models import get_model_choices

    adultModelFrame = Frame(window)
    adultModelLabel = Label(adultModelFrame, text='Adult Link Model')
    opts.model_adult = StringVar(value='Default')
    adultModelMenu = OptionMenu(adultModelFrame, opts.model_adult, *get_model_choices(0))
    adultModelFrame.pack(side=TOP, expand=True, fill=X)
    adultModelLabel.pack(side=LEFT)
    adultModelMenu.pack(side=LEFT)

    childModelFrame = Frame(window)
    childModelLabel = Label(childModelFrame, text='Child Link Model')
    opts.model_child = StringVar(value='Default')
    childModelMenu = OptionMenu(childModelFrame, opts.model_child, *get_model_choices(1))
    childModelFrame.pack(side=TOP, expand=True, fill=X)
    childModelLabel.pack(side=LEFT)
    childModelMenu.pack(side=LEFT)

    # Cosmetic options
    romSettingsFrame = Frame(window)

    def dropdown_option(type, option_name, row, column):
        if type == 'cosmetic':
            option = cosmetic_options[option_name]
        elif type == 'sfx':
            option = sfx_options[option_name]
        optionFrame = Frame(romSettingsFrame)
        optionFrame.grid(row=row, column=column, sticky=E)
        optionLabel = Label(optionFrame, text=option.display_name)
        optionLabel.pack(side=LEFT)
        setattr(opts, option_name, StringVar())
        getattr(opts, option_name).set(option.name_lookup[option.default])
        optionMenu = OptionMenu(optionFrame, getattr(opts, option_name), *option.name_lookup.values())
        optionMenu.pack(side=LEFT)

    dropdown_option('cosmetic', 'default_targeting', 0, 0)
    dropdown_option('cosmetic', 'display_dpad', 0, 1)
    dropdown_option('cosmetic', 'correct_model_colors', 0, 2)
    dropdown_option('cosmetic', 'background_music', 1, 0)
    dropdown_option('cosmetic', 'fanfares', 1, 1)
    dropdown_option('cosmetic', 'ocarina_fanfares', 1, 2)
    dropdown_option('cosmetic', 'kokiri_color', 2, 0)
    dropdown_option('cosmetic', 'goron_color', 2, 1)
    dropdown_option('cosmetic', 'zora_color', 2, 2)
    dropdown_option('cosmetic', 'silver_gauntlets_color', 3, 0)
    dropdown_option('cosmetic', 'golden_gauntlets_color', 3, 1)
    dropdown_option('cosmetic', 'mirror_shield_frame_color', 3, 2)
    dropdown_option('cosmetic', 'navi_color_default_inner', 4, 0)
    dropdown_option('cosmetic', 'navi_color_default_outer', 4, 1)
    dropdown_option('cosmetic', 'navi_color_enemy_inner', 5, 0)
    dropdown_option('cosmetic', 'navi_color_enemy_outer', 5, 1)
    dropdown_option('cosmetic', 'navi_color_npc_inner', 6, 0)
    dropdown_option('cosmetic', 'navi_color_npc_outer', 6, 1)
    dropdown_option('cosmetic', 'navi_color_prop_inner', 7, 0)
    dropdown_option('cosmetic', 'navi_color_prop_outer', 7, 1)
    # sword_trail_duration, 8, 2
    dropdown_option('cosmetic', 'sword_trail_color_inner', 8, 0)
    dropdown_option('cosmetic', 'sword_trail_color_outer', 8, 1)
    dropdown_option('cosmetic', 'bombchu_trail_color_inner', 9, 0)
    dropdown_option('cosmetic', 'bombchu_trail_color_outer', 9, 1)
    dropdown_option('cosmetic', 'boomerang_trail_color_inner', 10, 0)
    dropdown_option('cosmetic', 'boomerang_trail_color_outer', 10, 1)
    dropdown_option('cosmetic', 'heart_color', 11, 0)
    dropdown_option('cosmetic', 'magic_color', 12, 0)
    dropdown_option('cosmetic', 'a_button_color', 11, 1)
    dropdown_option('cosmetic', 'b_button_color', 11, 2)
    dropdown_option('cosmetic', 'c_button_color', 12, 1)
    dropdown_option('cosmetic', 'start_button_color', 12, 2)

    dropdown_option('cosmetic', 'display_custom_song_names', 13, 0)

    opts.credits_music = IntVar(value=CreditsMusic.default)
    Checkbutton(romSettingsFrame, text="Credits Music as BGM", variable=opts.credits_music).grid(row=13, column=1, sticky=W)

    opts.disable_battle_music = IntVar(value=DisableBattleMusic.default)
    Checkbutton(romSettingsFrame, text="Disable Battle Music", variable=opts.disable_battle_music).grid(row=13, column=2, sticky=W)

    dropdown_option('sfx', 'sfx_navi_overworld', 14, 0)
    dropdown_option('sfx', 'sfx_navi_enemy', 14, 1)
    dropdown_option('sfx', 'sfx_low_hp', 14, 2)
    dropdown_option('sfx', 'sfx_menu_cursor', 15, 0)
    dropdown_option('sfx', 'sfx_menu_select', 15, 1)
    dropdown_option('sfx', 'sfx_nightfall', 15, 2)
    dropdown_option('sfx', 'sfx_horse_neigh', 16, 0)
    dropdown_option('sfx', 'sfx_hover_boots', 16, 1)
    dropdown_option('sfx', 'sfx_ocarina', 16, 2)

    dropdown_option('sfx', 'sfx_iron_boots', 17, 0)
    dropdown_option('sfx', 'sfx_silver_rupee', 17, 1)
    dropdown_option('sfx', 'sfx_boomerang_throw', 17, 2)
    dropdown_option('sfx', 'sfx_hookshot_chain', 18, 0)
    dropdown_option('sfx', 'sfx_arrow_shot', 18, 1)
    dropdown_option('sfx', 'sfx_slingshot_shot', 18, 2)
    dropdown_option('sfx', 'sfx_magic_arrow_shot', 19, 0)
    dropdown_option('sfx', 'sfx_bombchu_move', 19, 1)
    dropdown_option('sfx', 'sfx_get_small_item', 19, 2)
    dropdown_option('sfx', 'sfx_explosion', 20, 0)
    dropdown_option('sfx', 'sfx_daybreak', 20, 1)
    dropdown_option('sfx', 'sfx_cucco', 20, 2)

    # Special cases
    # Sword trail duration is a range
    option = cosmetic_options['sword_trail_duration']
    optionFrame = Frame(romSettingsFrame)
    optionFrame.grid(row=8, column=2, sticky=E)
    optionLabel = Label(optionFrame, text=option.display_name)
    optionLabel.pack(side=LEFT)
    setattr(opts, 'sword_trail_duration', StringVar())
    getattr(opts, 'sword_trail_duration').set(option.default)
    optionMenu = OptionMenu(optionFrame, getattr(opts, 'sword_trail_duration'), *range(4, 21))
    optionMenu.pack(side=LEFT)

    # Toggle cosmetic options as checkboxes
    opts.dpad_dungeon_menu = IntVar(value=DpadDungeonMenu.default)
    Checkbutton(romSettingsFrame, text="D-Pad Dungeon Info", variable=opts.dpad_dungeon_menu).grid(row=21, column=0, sticky=W)

    opts.speedup_music_for_last_triforce_piece = IntVar(value=SpeedupMusicForLastTriforcePiece.default)
    Checkbutton(romSettingsFrame, text="Speed Up Music (Last Triforce Piece)", variable=opts.speedup_music_for_last_triforce_piece).grid(row=21, column=1, sticky=W)

    opts.slowdown_music_when_lowhp = IntVar(value=SlowdownMusicWhenLowhp.default)
    Checkbutton(romSettingsFrame, text="Slowdown Music When Low HP", variable=opts.slowdown_music_when_lowhp).grid(row=21, column=2, sticky=W)

    opts.uninvert_y_axis_in_first_person_camera = IntVar(value=UninvertYAxisInFirstPersonCamera.default)
    Checkbutton(romSettingsFrame, text="Uninvert Y-Axis (First Person)", variable=opts.uninvert_y_axis_in_first_person_camera).grid(row=22, column=0, sticky=W)

    opts.input_viewer = IntVar(value=InputViewer.default)
    Checkbutton(romSettingsFrame, text="Input Viewer", variable=opts.input_viewer).grid(row=22, column=1, sticky=W)


    # Deathlink is a checkbox
    opts.deathlink = IntVar(value=0)
    deathlink_checkbox = Checkbutton(romSettingsFrame, text="DeathLink (Team Deaths)", variable=opts.deathlink)
    deathlink_checkbox.grid(row=23, column=1, sticky=W)

    romSettingsFrame.pack(side=TOP)

    def adjustRom():
        try:
            guiargs = Namespace()
            options = vars(opts)
            for o in options:
                result = options[o].get()
                if result == 'true':
                    result = True
                if result == 'false':
                    result = False
                setattr(guiargs, o, result)
            guiargs.sword_trail_duration = int(guiargs.sword_trail_duration)
            path = adjust(guiargs)
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
        else:
            from worlds.LauncherComponents import launch_subprocess
            from worlds.oot.client import main as client_main
            launch_rom(path)
            launch_subprocess(client_main, name="OoTClient")
            messagebox.showinfo(title="Success", message=f"Rom adjusted to {path}")

    # Adjust button
    bottomFrame = Frame(window)
    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=BOTTOM, padx=(5, 5))
    bottomFrame.pack(side=BOTTOM, pady=(5, 5))

    window.mainloop()

def set_icon(window):
    logo = tk.PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)

def adjust(args):
    # Create a fake multiworld and OOTWorld to use as a base
    multiworld = MultiWorld(1)
    ootworld = OOTWorld(multiworld, 1)
    # Set options in the fake OOTWorld
    for name, option in chain(cosmetic_options.items(), sfx_options.items()):
        result = getattr(args, name, None)
        if result is None:
            if issubclass(option, Choice):
                result = option.name_lookup[option.default]
            elif issubclass(option, Range) or issubclass(option, Toggle):
                result = option.default
            else:
                raise Exception("Unsupported option type")
        setattr(ootworld, name, result)
    ootworld.logic_rules = 'glitchless'
    ootworld.death_link = args.deathlink
    ootworld.music_dir = getattr(args, 'music_dir', None) or None
    ootworld.model_adult = getattr(args, 'model_adult', 'Default')
    ootworld.model_adult_filepicker = ''
    ootworld.model_child = getattr(args, 'model_child', 'Default')
    ootworld.model_child_filepicker = ''

    delete_zootdec = False
    if os.path.splitext(args.rom)[-1] in ['.z64', '.n64']:
        # Load up the ROM
        rom = Rom(file=args.rom, force_use=True)
        delete_zootdec = True
    elif os.path.splitext(args.rom)[-1] in ['.apz5', '.zpf']:
        # Load vanilla ROM
        rom = Rom(file=args.vanilla_rom, force_use=True)
        apz5_file = args.rom
        base_name = os.path.splitext(apz5_file)[0]
        # Patch file
        apply_patch_file(rom, apz5_file,
            sub_file=(os.path.basename(base_name) + '.zpf'
                if zipfile.is_zipfile(apz5_file)
                else None))
    else:
        raise Exception("Invalid file extension; requires .n64, .z64, .apz5, .zpf")
    # Call patch_cosmetics
    try:
        patch_cosmetics(ootworld, rom)
        rom.write_byte(rom.sym('DEATH_LINK'), args.deathlink)
        # Output new file
        path_pieces = os.path.splitext(args.rom)
        decomp_path = path_pieces[0] + '-adjusted-decomp.n64'
        comp_path = path_pieces[0] + '-adjusted.n64'
        rom.write_to_file(decomp_path)
        compress_rom_file(decomp_path, comp_path)
        os.remove(decomp_path)
    finally:
        if delete_zootdec:
            decomp_file = user_path('ZOOTDEC.z64')
            if os.path.exists(decomp_file):
                os.remove(decomp_file)
    return comp_path

def launch(*launcher_args: str):
    main(launcher_args)

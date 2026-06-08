import tkinter as tk
import argparse
import logging
import os
import zipfile
from itertools import chain

from BaseClasses import MultiWorld
from Options import Choice, Range, Toggle
from . import OOTWorld, launch_rom as launch_oot_rom
from .Cosmetics import get_voice_choices, patch_cosmetics
from . import Music as music
from .MusicHelpers import find_mm_audiobin_path
from .Options import (cosmetic_options, sfx_options, voice_options,
    DpadDungeonMenu, SpeedupMusicForLastTriforcePiece, SlowdownMusicWhenLowhp,
    UninvertYAxisInFirstPersonCamera, InputViewer, DisableBattleMusic, CreditsMusic)
from .Rom import Rom, compress_rom_file
from .N64Patch import apply_patch_file
from .Utils import __version__ as oot_version
from Utils import local_path, user_path, persistent_store, get_adjuster_settings_no_defaults

logger = logging.getLogger('OoTAdjuster')

def launch_rom(path: str) -> None:
    launch_oot_rom(path, logger)


def get_mmrs_missing_audiobin_warning(args) -> str | None:
    if getattr(args, 'background_music', 'normal') == 'normal' and getattr(args, 'fanfares', 'normal') == 'normal':
        return None

    music_dir = getattr(args, 'music_dir', None) or None
    if not music_dir or not os.path.isdir(music_dir):
        return None

    if find_mm_audiobin_path(music_dir):
        return None

    for _dirpath, _dirnames, filenames in os.walk(music_dir, followlinks=True):
        if any(fname.lower().endswith('.mmrs') for fname in filenames):
            return (
                ".mmrs custom music files were ignored because MM.audiobin was not found. "
                f"Place MM.audiobin in {music_dir} to enable .mmrs tracks from that folder."
            )
    return None


def get_argparser():
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

    return parser


def get_default_adjuster_settings():
    adjuster_settings = get_argparser().parse_known_args(args=[])[0]
    adjuster_settings.vanilla_rom = "The Legend of Zelda - Ocarina of Time.z64"
    for name, option in chain(cosmetic_options.items(), sfx_options.items()):
        if issubclass(option, Choice):
            setattr(adjuster_settings, name, option.name_lookup[option.default])
        elif issubclass(option, Range) or issubclass(option, Toggle):
            setattr(adjuster_settings, name, option.default)
        else:
            raise Exception("Unsupported option type")
    for name in voice_options:
        setattr(adjuster_settings, name, 'Default')
    return adjuster_settings


def get_adjuster_settings():
    adjuster_settings = get_adjuster_settings_no_defaults(OOTWorld.game)
    default_settings = get_default_adjuster_settings()

    # Fill in settings added after a user's persistent storage was created.
    settings = argparse.Namespace(**vars(adjuster_settings), **{
        k: v for k, v in vars(default_settings).items() if k not in vars(adjuster_settings)
    })
    settings.rom = ''
    return settings


def save_adjuster_settings(args):
    stored_args = argparse.Namespace(**vars(args))
    if hasattr(stored_args, "rom"):
        delattr(stored_args, "rom")
    persistent_store("adjuster", OOTWorld.game, stored_args)


def main(launcher_args):
    parser = get_argparser()
    launcher_args = launcher_args or ()

    adjuster_settings = get_adjuster_settings_no_defaults(OOTWorld.game)
    if not any(arg == '--rom' or arg.startswith('--rom=') for arg in launcher_args):
        adjuster_settings.rom = ''
    args = parser.parse_args(launcher_args, namespace=adjuster_settings)
    if not os.path.isfile(args.rom):
        adjustGUI()
    else:
        adjust(args)
        save_adjuster_settings(args)

def adjustGUI():
    from tkinter import Tk, LEFT, BOTTOM, TOP, E, W, \
        StringVar, IntVar, Checkbutton, Frame, Label, X, Entry, Button, \
        OptionMenu, filedialog, messagebox, ttk
    from argparse import Namespace
    import threading
    from queue import Empty, Queue
    from Utils import __version__ as MWVersion
    try:
        from Utils import instance_name as apname
    except ImportError:
        apname = "Archipelago"

    window = tk.Tk()
    window.wm_title(f"Ocarina of Time Adjuster (OoT APWorld {oot_version}) | {apname} {MWVersion}")
    set_icon(window)

    opts = Namespace()
    adjuster_settings = get_adjuster_settings()

    # Select ROM
    romDialogFrame = Frame(window)
    romLabel = Label(romDialogFrame, text='Rom/patch to adjust')
    vanillaLabel = Label(romDialogFrame, text='OoT Base Rom')
    opts.rom = StringVar(value=getattr(adjuster_settings, 'rom', ''))
    opts.vanilla_rom = StringVar(value=adjuster_settings.vanilla_rom)
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
    opts.music_dir = StringVar(value=adjuster_settings.music_dir or '')

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

    from .Models import get_model_choices

    adultModelFrame = Frame(window)
    adultModelLabel = Label(adultModelFrame, text='Adult Link Model')
    opts.model_adult = StringVar(value=adjuster_settings.model_adult)
    adultModelMenu = OptionMenu(adultModelFrame, opts.model_adult, *get_model_choices(0))
    adultModelFrame.pack(side=TOP, expand=True, fill=X)
    adultModelLabel.pack(side=LEFT)
    adultModelMenu.pack(side=LEFT)

    childModelFrame = Frame(window)
    childModelLabel = Label(childModelFrame, text='Child Link Model')
    opts.model_child = StringVar(value=adjuster_settings.model_child)
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
        getattr(opts, option_name).set(getattr(adjuster_settings, option_name))
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

    opts.credits_music = IntVar(value=adjuster_settings.credits_music)
    Checkbutton(romSettingsFrame, text="Credits Music as BGM", variable=opts.credits_music).grid(row=13, column=1, sticky=W)

    opts.disable_battle_music = IntVar(value=adjuster_settings.disable_battle_music)
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

    def voice_dropdown(option_name, age, row, column):
        option = voice_options[option_name]
        optionFrame = Frame(romSettingsFrame)
        optionFrame.grid(row=row, column=column, sticky=E)
        optionLabel = Label(optionFrame, text=option.display_name)
        optionLabel.pack(side=LEFT)
        setattr(opts, option_name, StringVar(value=getattr(adjuster_settings, option_name)))
        optionMenu = OptionMenu(optionFrame, getattr(opts, option_name), *get_voice_choices(age))
        optionMenu.pack(side=LEFT)

    voice_dropdown('sfx_link_adult', 1, 21, 0)
    voice_dropdown('sfx_link_child', 0, 21, 1)

    # Special cases
    # Sword trail duration is a range
    option = cosmetic_options['sword_trail_duration']
    optionFrame = Frame(romSettingsFrame)
    optionFrame.grid(row=8, column=2, sticky=E)
    optionLabel = Label(optionFrame, text=option.display_name)
    optionLabel.pack(side=LEFT)
    setattr(opts, 'sword_trail_duration', StringVar())
    getattr(opts, 'sword_trail_duration').set(adjuster_settings.sword_trail_duration)
    optionMenu = OptionMenu(optionFrame, getattr(opts, 'sword_trail_duration'), *range(4, 21))
    optionMenu.pack(side=LEFT)

    # Toggle cosmetic options as checkboxes
    opts.dpad_dungeon_menu = IntVar(value=adjuster_settings.dpad_dungeon_menu)
    Checkbutton(romSettingsFrame, text="D-Pad Dungeon Info", variable=opts.dpad_dungeon_menu).grid(row=22, column=0, sticky=W)

    opts.speedup_music_for_last_triforce_piece = IntVar(value=adjuster_settings.speedup_music_for_last_triforce_piece)
    Checkbutton(romSettingsFrame, text="Speed Up Music (Last Triforce Piece)", variable=opts.speedup_music_for_last_triforce_piece).grid(row=22, column=1, sticky=W)

    opts.slowdown_music_when_lowhp = IntVar(value=adjuster_settings.slowdown_music_when_lowhp)
    Checkbutton(romSettingsFrame, text="Slowdown Music When Low HP", variable=opts.slowdown_music_when_lowhp).grid(row=22, column=2, sticky=W)

    opts.uninvert_y_axis_in_first_person_camera = IntVar(value=adjuster_settings.uninvert_y_axis_in_first_person_camera)
    Checkbutton(romSettingsFrame, text="Uninvert Y-Axis (First Person)", variable=opts.uninvert_y_axis_in_first_person_camera).grid(row=23, column=0, sticky=W)

    opts.input_viewer = IntVar(value=adjuster_settings.input_viewer)
    Checkbutton(romSettingsFrame, text="Input Viewer", variable=opts.input_viewer).grid(row=23, column=1, sticky=W)

    opts.randomize_all_sfx = IntVar(value=adjuster_settings.randomize_all_sfx)
    Checkbutton(romSettingsFrame, text="Randomize All SFX", variable=opts.randomize_all_sfx).grid(row=23, column=2, sticky=W)


    # Deathlink is a checkbox
    opts.deathlink = IntVar(value=adjuster_settings.deathlink)
    deathlink_checkbox = Checkbutton(romSettingsFrame, text="DeathLink (Team Deaths)", variable=opts.deathlink)
    deathlink_checkbox.grid(row=24, column=1, sticky=W)

    romSettingsFrame.pack(side=TOP)

    progress_overlay = None

    def make_guiargs():
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
        return guiargs

    def show_progress_overlay(progress_text):
        nonlocal progress_overlay
        progress_overlay = tk.Toplevel(window)
        progress_overlay.wm_title("Adjusting ROM")
        progress_overlay.resizable(False, False)
        progress_overlay.transient(window)
        progress_overlay.protocol("WM_DELETE_WINDOW", lambda: None)

        progress_frame = Frame(progress_overlay, padx=20, pady=16)
        progress_label = Label(progress_frame, textvariable=progress_text)
        progress_bar = ttk.Progressbar(progress_frame, mode="indeterminate", length=280)
        progress_label.pack(side=TOP, anchor=W)
        progress_bar.pack(side=TOP, fill=X, pady=(10, 0))
        progress_frame.pack(side=TOP, fill=X)
        progress_bar.start(12)

        progress_overlay.update_idletasks()
        window_x = window.winfo_rootx()
        window_y = window.winfo_rooty()
        window_width = window.winfo_width()
        window_height = window.winfo_height()
        overlay_width = progress_overlay.winfo_width()
        overlay_height = progress_overlay.winfo_height()
        x = window_x + max(0, (window_width - overlay_width) // 2)
        y = window_y + max(0, (window_height - overlay_height) // 2)
        progress_overlay.geometry(f"+{x}+{y}")
        progress_overlay.grab_set()

    def hide_progress_overlay():
        nonlocal progress_overlay
        if progress_overlay is None:
            return
        try:
            progress_overlay.grab_release()
        except tk.TclError:
            pass
        progress_overlay.destroy()
        progress_overlay = None

    def adjustRom():
        try:
            guiargs = make_guiargs()
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while adjusting Rom", message=str(e))
            return

        result_queue = Queue()
        progress_text = StringVar(value="Preparing ROM adjustment...")
        adjustButton.configure(state="disabled")
        show_progress_overlay(progress_text)

        def worker():
            try:
                path = adjust(guiargs, status_callback=lambda status: result_queue.put(("status", status)))
                result_queue.put(("success", path))
            except Exception as e:
                logging.exception(e)
                result_queue.put(("error", e))

        def check_result():
            try:
                while True:
                    result, value = result_queue.get_nowait()
                    if result == "status":
                        progress_text.set(value)
                        continue

                    hide_progress_overlay()
                    adjustButton.configure(state="normal")

                    if result == "error":
                        messagebox.showerror(title="Error while adjusting Rom", message=str(value))
                        return

                    path = value
                    save_adjuster_settings(guiargs)
                    from worlds.LauncherComponents import launch_subprocess
                    from .client import main as client_main
                    warning = get_mmrs_missing_audiobin_warning(guiargs)
                    if warning:
                        messagebox.showwarning(title="Custom music skipped", message=warning)
                    launch_rom(path)
                    launch_subprocess(client_main, name="OoTClient")
                    messagebox.showinfo(title="Success", message=f"Rom adjusted to {path}")
                    return
            except Empty:
                window.after(100, check_result)

        threading.Thread(target=worker, daemon=True).start()
        window.after(100, check_result)

    # Adjust button
    bottomFrame = Frame(window)
    adjustButton = Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=LEFT, padx=(5, 5))

    def saveGUISettings():
        try:
            save_adjuster_settings(make_guiargs())
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while saving settings", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Settings saved to persistent storage")

    saveButton = Button(bottomFrame, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5, 5))
    bottomFrame.pack(side=BOTTOM, pady=(5, 5))

    window.mainloop()

def set_icon(window):
    logo = tk.PhotoImage(file=local_path('data', 'icon.png'))
    window.tk.call('wm', 'iconphoto', window._w, logo)


def _option_display_value(args, name, option=None):
    value = getattr(args, name, None)
    if isinstance(value, bool):
        return "on" if value else "off"
    if option is not None and issubclass(option, Toggle) and isinstance(value, int):
        return "on" if value else "off"
    return str(value)


def _append_option_section(lines, title, args, options):
    lines.append(f"{title}:")
    for name, option in options.items():
        display_name = getattr(option, "display_name", name)
        lines.append(f"  {display_name} ({name}): {_option_display_value(args, name, option)}")
    lines.append("")


def _append_music_log(lines, ootworld):
    music_log = getattr(ootworld, "cosmetic_music_log", {}) or {}
    music_errors = getattr(ootworld, "cosmetic_music_errors", []) or []
    sequence_ids = []
    seen = set()
    for name, seq_id in (
        music.bgm_sequence_ids
        + music.fanfare_sequence_ids
        + music.ocarina_sequence_ids
        + music.credit_sequence_ids
        + music.fileselect_sequence_id
    ):
        if name in seen:
            continue
        seen.add(name)
        sequence_ids.append((name, seq_id))

    lines.append("Music Placements:")
    if music_log:
        for name, seq_id in sequence_ids:
            if name in music_log:
                lines.append(f"  0x{seq_id:02X} {name}: {music_log[name]}")
        for name in sorted(set(music_log) - seen):
            lines.append(f"  {name}: {music_log[name]}")
    else:
        lines.append("  No randomized music placements were written.")
    lines.append("")

    if music_errors:
        lines.append("Music Warnings/Errors:")
        for error in music_errors:
            lines.append(f"  {error}")
        lines.append("")


def write_adjuster_cosmetics_log(args, ootworld, output_rom_path, log_path):
    lines = [
        "OoT Adjuster Cosmetics Log",
        f"Input file: {args.rom}",
        f"Base ROM: {getattr(args, 'vanilla_rom', '')}",
        f"Output ROM: {output_rom_path}",
        f"OoT APWorld version: {oot_version}",
        "",
    ]
    _append_option_section(lines, "Cosmetic Options", args, cosmetic_options)
    _append_option_section(lines, "SFX Options", args, sfx_options)
    lines.append("Models and Adjuster Options:")
    lines.append(f"  Adult Link Model: {getattr(args, 'model_adult', 'Default')}")
    lines.append(f"  Child Link Model: {getattr(args, 'model_child', 'Default')}")
    lines.append(f"  Custom Music Folder: {getattr(args, 'music_dir', None) or ''}")
    lines.append(f"  DeathLink: {'on' if bool(getattr(args, 'deathlink', False)) else 'off'}")
    lines.append("")
    _append_music_log(lines, ootworld)

    with open(log_path, "w", encoding="utf-8") as stream:
        stream.write("\n".join(lines).rstrip() + "\n")


def adjust(args, status_callback=None):
    def update_status(status):
        if status_callback:
            status_callback(status)

    # Create a fake multiworld and OOTWorld to use as a base
    update_status("Preparing options...")
    warning = get_mmrs_missing_audiobin_warning(args)
    if warning:
        logger.warning(warning)
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
        update_status("Loading ROM...")
        rom = Rom(file=args.rom, force_use=True)
        delete_zootdec = True
    elif os.path.splitext(args.rom)[-1] in ['.apz5', '.zpf']:
        # Load vanilla ROM
        update_status("Loading base ROM...")
        rom = Rom(file=args.vanilla_rom, force_use=True)
        apz5_file = args.rom
        base_name = os.path.splitext(apz5_file)[0]
        # Patch file
        update_status("Applying patch file...")
        apply_patch_file(rom, apz5_file,
            sub_file=(os.path.basename(base_name) + '.zpf'
                if zipfile.is_zipfile(apz5_file)
                else None))
    else:
        raise Exception("Invalid file extension; requires .n64, .z64, .apz5, .zpf")
    # Call patch_cosmetics
    try:
        update_status("Applying cosmetic changes...")
        patch_cosmetics(ootworld, rom)
        rom.write_byte(rom.sym('DEATH_LINK'), args.deathlink)
        # Output new file
        path_pieces = os.path.splitext(args.rom)
        decomp_path = path_pieces[0] + '-adjusted-decomp.n64'
        comp_path = path_pieces[0] + '-adjusted.n64'
        update_status("Writing adjusted ROM...")
        rom.write_to_file(decomp_path)
        update_status("Compressing adjusted ROM...")
        compress_rom_file(decomp_path, comp_path)
        update_status("Writing cosmetics log...")
        write_adjuster_cosmetics_log(args, ootworld, comp_path, path_pieces[0] + '_cosmetics.log')
        os.remove(decomp_path)
        update_status("Finishing...")
    finally:
        if delete_zootdec:
            decomp_file = user_path('ZOOTDEC.z64')
            if os.path.exists(decomp_file):
                os.remove(decomp_file)
    return comp_path

def launch(*launcher_args: str):
    main(launcher_args)

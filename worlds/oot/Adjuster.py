import tkinter as tk
import argparse
import logging
import os
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
from .appp import patch_to_rom
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
    from tkinter import LEFT, BOTTOM, TOP, W, \
        StringVar, IntVar, Frame, Label, X, filedialog, messagebox, ttk
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

    # ROM selection and actions stay visible while switching settings tabs.
    rom_frame = ttk.LabelFrame(window, text="ROM Files", padding=10)
    rom_frame.pack(side=TOP, fill=X, padx=10, pady=(10, 8))
    rom_frame.columnconfigure(1, weight=1)
    opts.rom = StringVar(value=getattr(adjuster_settings, 'rom', ''))
    opts.vanilla_rom = StringVar(value=adjuster_settings.vanilla_rom)

    def RomSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64", ".apoot")), ("All Files", "*")])
        if rom:
            opts.rom.set(rom)

    def VanillaSelect():
        rom = filedialog.askopenfilename(filetypes=[("Rom Files", (".z64", ".n64")), ("All Files", "*")])
        if rom:
            opts.vanilla_rom.set(rom)

    for row, (label, variable, command) in enumerate((
        ("ROM / patch to adjust", opts.rom, RomSelect),
        ("OoT Base ROM", opts.vanilla_rom, VanillaSelect),
    )):
        ttk.Label(rom_frame, text=label).grid(row=row, column=0, sticky=W, padx=(0, 10), pady=3)
        ttk.Entry(rom_frame, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=3)
        ttk.Button(rom_frame, text="Select ROM", command=command).grid(row=row, column=2, padx=(10, 0), pady=3)

    notebook = ttk.Notebook(window)
    notebook.pack(side=TOP, fill="both", expand=True, padx=10, pady=(0, 8))

    def tab(title):
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=title)
        return frame

    def section(parent, title):
        frame = ttk.LabelFrame(parent, text=title, padding=10)
        frame.pack(side=TOP, fill=X, pady=(0, 10))
        return frame

    def choice_control(parent, name, label, choices, row, column=0):
        variable = StringVar(value=getattr(adjuster_settings, name))
        setattr(opts, name, variable)
        column *= 2
        ttk.Label(parent, text=label).grid(row=row, column=column, sticky=W, padx=(0, 8), pady=4)
        menu = ttk.Combobox(parent, textvariable=variable, values=tuple(choices), state="readonly", width=24)
        menu.grid(row=row, column=column + 1, sticky="ew", padx=(0, 16), pady=4)
        parent.columnconfigure(column + 1, weight=1)

    def dropdown_option(parent, name, row, column=0):
        option = cosmetic_options.get(name) or sfx_options[name]
        if issubclass(option, Range):
            choices = range(option.range_start, option.range_end + 1)
        else:
            choices = option.name_lookup.values()
        choice_control(parent, name, option.display_name, choices, row, column)

    def dropdowns(parent, names, columns=2):
        for index, name in enumerate(names):
            dropdown_option(parent, name, index // columns, index % columns)

    def checkbox(parent, name, label, row, column=0):
        variable = IntVar(value=getattr(adjuster_settings, name))
        setattr(opts, name, variable)
        ttk.Checkbutton(parent, text=label, variable=variable).grid(
            row=row, column=column * 2, columnspan=2, sticky=W, padx=(0, 16), pady=4)

    general_tab = tab("General")
    from .Models import get_model_choices

    models = section(general_tab, "Link Models")
    choice_control(models, 'model_adult', 'Adult Link Model', get_model_choices(0), 0)
    choice_control(models, 'model_child', 'Child Link Model', get_model_choices(1), 1)
    controls = section(general_tab, "Controls and Display")
    dropdowns(controls, ('default_targeting', 'display_dpad'))
    checkbox(controls, 'dpad_dungeon_menu', "D-Pad Dungeon Info", 1)
    checkbox(controls, 'input_viewer', "Input Viewer", 1, 1)
    checkbox(controls, 'uninvert_y_axis_in_first_person_camera', "Uninvert Y-Axis (First Person)", 2)
    multiplayer = section(general_tab, "Multiworld")
    checkbox(multiplayer, 'deathlink', "DeathLink (Team Deaths)", 0)

    equipment_tab = tab("Equipment")
    tunics = section(equipment_tab, "Tunic Colors")
    dropdowns(tunics, ('kokiri_color', 'goron_color', 'zora_color'), columns=1)
    gauntlets = section(equipment_tab, "Gauntlet Colors")
    dropdowns(gauntlets, ('silver_gauntlets_color', 'golden_gauntlets_color'))
    shield = section(equipment_tab, "Mirror Shield Frame Color")
    dropdown_option(shield, 'mirror_shield_frame_color', 0)

    hud_tab = tab("HUD Colors")
    meters = section(hud_tab, "Heart and Magic Colors")
    dropdowns(meters, ('heart_color', 'magic_color'))
    buttons = section(hud_tab, "Button Colors")
    dropdowns(buttons, ('a_button_color', 'b_button_color', 'c_button_color', 'start_button_color'))
    model_colors = section(hud_tab, "Item Model Colors")
    checkbox(model_colors, 'correct_model_colors', "Item Model Colors Match Cosmetics", 0)

    navi_tab = tab("Navi Colors")
    navi = section(navi_tab, "Navi Colors")
    dropdowns(navi, (
        'navi_color_default_inner', 'navi_color_default_outer',
        'navi_color_enemy_inner', 'navi_color_enemy_outer',
        'navi_color_npc_inner', 'navi_color_npc_outer',
        'navi_color_prop_inner', 'navi_color_prop_outer',
    ))

    trails_tab = tab("Trails")
    sword = section(trails_tab, "Sword Trail")
    dropdowns(sword, ('sword_trail_color_inner', 'sword_trail_color_outer', 'sword_trail_duration'))
    bombchu = section(trails_tab, "Bombchu Trail")
    dropdowns(bombchu, ('bombchu_trail_color_inner', 'bombchu_trail_color_outer'))
    boomerang = section(trails_tab, "Boomerang Trail")
    dropdowns(boomerang, ('boomerang_trail_color_inner', 'boomerang_trail_color_outer'))

    music_tab = tab("Custom Music")
    music_folder = section(music_tab, "Custom Music Folder (.ootrs / .mmrs)")
    opts.music_dir = StringVar(value=adjuster_settings.music_dir or '')

    def MusicDirSelect():
        directory = filedialog.askdirectory(title='Select Custom Music Folder')
        if directory:
            opts.music_dir.set(directory)

    ttk.Entry(music_folder, textvariable=opts.music_dir).pack(side=LEFT, expand=True, fill=X)
    ttk.Button(music_folder, text='Select Folder', command=MusicDirSelect).pack(side=LEFT, padx=(10, 0))
    music_settings = section(music_tab, "Music and Fanfares")
    dropdowns(music_settings, ('background_music', 'fanfares', 'display_custom_song_names'))
    checkbox(music_settings, 'ocarina_fanfares', "Ocarina Songs as Fanfares", 2)
    checkbox(music_settings, 'credits_music', "Credits Music as BGM", 2, 1)
    music_behavior = section(music_tab, "Music Behavior")
    checkbox(music_behavior, 'disable_battle_music', "Disable Battle Music", 0)
    checkbox(music_behavior, 'speedup_music_for_last_triforce_piece', "Speed Up Music (Last Triforce Piece)", 1)
    checkbox(music_behavior, 'slowdown_music_when_lowhp', "Slowdown Music When Low HP", 2)

    sfx_tab = tab("SFX")
    sound_effects = section(sfx_tab, "Sound Effects (SFX)")
    checkbox(sound_effects, 'randomize_all_sfx', "Randomize All SFX", 0)
    ttk.Label(sound_effects, text="Also randomizes music settings; Link voices are selected separately.").grid(
        row=1, column=0, columnspan=4, sticky=W, pady=(0, 6))
    for index, name in enumerate((
        'sfx_navi_overworld', 'sfx_navi_enemy',
        'sfx_menu_cursor', 'sfx_menu_select',
        'sfx_low_hp', 'sfx_silver_rupee',
        'sfx_daybreak', 'sfx_nightfall',
        'sfx_horse_neigh', 'sfx_cucco',
        'sfx_hover_boots', 'sfx_iron_boots',
        'sfx_boomerang_throw', 'sfx_hookshot_chain',
        'sfx_arrow_shot', 'sfx_slingshot_shot',
        'sfx_magic_arrow_shot', 'sfx_bombchu_move',
        'sfx_explosion', 'sfx_get_small_item',
        'sfx_ocarina',
    )):
        dropdown_option(sound_effects, name, index // 2 + 2, index % 2)
    voices = section(sfx_tab, "Link Voices")
    for column, (name, age) in enumerate((('sfx_link_adult', 1), ('sfx_link_child', 0))):
        choice_control(voices, name, voice_options[name].display_name, get_voice_choices(age), 0, column)

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
    bottomFrame = ttk.Frame(window)
    adjustButton = ttk.Button(bottomFrame, text='Adjust Rom', command=adjustRom)
    adjustButton.pack(side=LEFT, padx=(5, 5))

    def saveGUISettings():
        try:
            save_adjuster_settings(make_guiargs())
        except Exception as e:
            logging.exception(e)
            messagebox.showerror(title="Error while saving settings", message=str(e))
        else:
            messagebox.showinfo(title="Success", message="Settings saved to persistent storage")

    saveButton = ttk.Button(bottomFrame, text='Save Settings', command=saveGUISettings)
    saveButton.pack(side=LEFT, padx=(5, 5))
    bottomFrame.pack(side=BOTTOM, pady=(5, 5))

    window.update_idletasks()
    window.minsize(window.winfo_reqwidth(), window.winfo_reqheight())
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
    elif os.path.splitext(args.rom)[-1] == '.apoot':
        update_status("Applying patch file...")
        rom = patch_to_rom(args.rom, args.vanilla_rom)
    else:
        raise Exception("Invalid file extension; requires .n64, .z64, .apoot")
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

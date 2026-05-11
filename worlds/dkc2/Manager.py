import io
import zipfile
import logging
import math
import json
import textwrap
import argparse
import tkinter as tk
from argparse import Namespace
from tkinter import Tk, Frame, Label, StringVar, IntVar, Entry, filedialog, messagebox, Button, LEFT, X, Y, BOTH, TOP, LabelFrame, \
    Checkbutton, E, W, BOTTOM, RIGHT, font as font, BooleanVar, Canvas, INSERT, Spinbox, VERTICAL, OptionMenu
from tkinter.ttk import Separator, Scrollbar
from tkinter.constants import DISABLED, NORMAL
from Utils import persistent_store, persistent_load, get_adjuster_settings_no_defaults, tkinter_center_window, open_filename

import ModuleUpdate
ModuleUpdate.update()

GAME_NAME = "Donkey Kong Country 2"
WINDOW_MIN_HEIGHT = 360
WINDOW_MIN_WIDTH = 760

from worlds.dkc2_trivia.games import aliases
from worlds.dkc2_trivia.trivia import retrieve_topics
trivia_topics = retrieve_topics(is_dkc2=True)
trivia_topics = dict(sorted(trivia_topics.items()))

class ArgumentDefaultsHelpFormatter(argparse.RawTextHelpFormatter):

    def _get_help_string(self, action):
        return textwrap.dedent(action.help)
    

def get_argparser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)

    return parser


def main(launcher_args):
    parser = get_argparser()
    args = parser.parse_args(launcher_args, namespace=get_adjuster_settings_no_defaults(GAME_NAME))

    manager_gui()


def manager_gui():    
    manager_window = Tk()
    manager_window.minsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    manager_window.maxsize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
    manager_window.resizable(True, False)
    manager_window.wm_title(f"Donkey Kong Country 2 Manager")

    left_frame = Frame(manager_window)
    right_frame = Frame(manager_window)

    linked_frame, linked_vars = create_linked_frame(left_frame)
    global_frame, global_vars = create_global_frame(left_frame)
    trivia_frame, trivia_vars, trivia_canvas_frame = create_trivia_frame(right_frame)
    file_frame, vars_ns = create_file_frame(left_frame, [linked_vars, trivia_vars], trivia_canvas_frame)

    file_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    linked_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    global_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)
    trivia_frame.pack(side=TOP, padx=8, pady=8, fill=BOTH)

    left_frame.pack(side=LEFT, fill=BOTH, expand=True)
    right_frame.pack(side=LEFT, fill=BOTH, expand=True)

    tkinter_center_window(manager_window)
    manager_window.mainloop()


def create_file_frame(parent=None, external_vars=None, canvas_frame=None):
    vars_ns = Namespace()
    if external_vars:
        for var_group in external_vars:
            for key, value in vars(var_group).items():
                setattr(vars_ns, key, value)

    frame = LabelFrame(parent, text="File Manager", padx=8, pady=8, name="file_manager")

    vars_ns.patch_path = StringVar()
    load_frame = Frame(frame)
    file_label = Label(load_frame, text="Patch file: ")
    file_label.pack(side=LEFT, fill=X)
    file_value = Entry(load_frame, textvariable=vars_ns.patch_path, state="readonly")
    file_value.pack(side=RIGHT, fill=X, expand=True)

    def load_patch_window():
        nonlocal vars_ns, canvas_frame

        file_path = filedialog.askopenfilename(
            filetypes=[("DKC2 Patch Files", ".apdkc2")])
        try:
            vars_ns.patch_path.set(file_path)
            load_data_from_patch(file_path, vars_ns, canvas_frame)
        except Exception as e:
            messagebox.showerror(title="Error while reading DKC2 Patch file", message=str(e))

    def save_patch_window():
        nonlocal vars_ns
        if "" == vars_ns.patch_path.get():
            return
        save_adjusted_data(vars_ns)
        messagebox.showinfo(title="Success", message="Saved changes to DKC2 Patch file!")

    load_button = Button(frame, text="Load DKC2 Patch", command=load_patch_window)
    save_button = Button(frame, text="Save changes to DKC2 Patch", command=save_patch_window)

    load_frame.pack(side=TOP, fill=X)
    load_button.pack(side=TOP, fill=X)
    save_button.pack(side=TOP, fill=X)

    return frame, vars_ns


def load_data_from_patch(patch_path, vars_ns, canvas_frame: Frame):
    file = zipfile.ZipFile(patch_path)
    options_file = json.loads(file.read("data.json").decode("UTF-8"))

    if "death_link" in options_file.keys():
        vars_ns.death_link_active.set(options_file["death_link"])
    if "damage_link" in options_file.keys():
        vars_ns.damage_link_active.set(options_file["damage_link"])
    if "energy_link" in options_file.keys():
        vars_ns.energy_link_active.set(options_file["energy_link"])
    if "trap_link" in options_file.keys():
        vars_ns.trap_link_active.set(options_file["trap_link"])

    if "games_in_session" in options_file.keys():
        games_in_session = options_file["games_in_session"]
        for idx, game in enumerate(games_in_session):
            if game in aliases.keys():
                games_in_session[idx] = aliases[game]

        games_in_session: set = set(games_in_session)

        for game in games_in_session:
            if game not in vars_ns.valid_topics.keys():
                continue 
            if vars_ns.valid_topics[game].get() == "Session":
                vars_ns.valid_topics[game].set("Included")

        sanitized_games = {filter_characters(game): game for game in games_in_session}
        for widget_frame in canvas_frame.winfo_children():
            if widget_frame.winfo_name() not in sanitized_games.keys():
                continue
            for widget in widget_frame.winfo_children():
                if isinstance(widget, OptionMenu):
                    menu = widget["menu"]
                    menu.delete(0, "end")
                    game = sanitized_games[widget_frame.winfo_name()]
                    if vars_ns.valid_topics[game].get() != "Excluded":
                        menu.add_command(label="Included", command=tk._setit(vars_ns.valid_topics[game], "Included"))
                    menu.add_command(label="Forced", command=tk._setit(vars_ns.valid_topics[game], "Forced"))
                    menu.add_command(label="Excluded", command=tk._setit(vars_ns.valid_topics[game], "Excluded"))

        easy_count = 0
        medium_count = 0
        hard_count = 0
        for topic_name, topic_setting in vars_ns.valid_topics.items():
            if topic_setting.get() in ["Forced", "Included"]:
                easy_count, medium_count, hard_count = add_trivia_count(topic_name, easy_count, medium_count, hard_count)
        
        vars_ns.question_total_count.set(f"Easy: {easy_count} | Medium: {medium_count} | Hard: {hard_count}")

        return games_in_session


def save_adjusted_data(vars_ns):
    patch_path = vars_ns.patch_path.get()
    file = zipfile.ZipFile(patch_path)

    zip_files = dict()
    for file_name in file.namelist():
        zip_files[file_name] = file.read(file_name)

    options_file = json.loads(file.read("data.json").decode("UTF-8"))
    options_file["death_link"] = vars_ns.death_link_active.get()
    options_file["damage_link"] = vars_ns.damage_link_active.get()
    options_file["energy_link"] = vars_ns.energy_link_active.get()
    options_file["trap_link"] = vars_ns.trap_link_active.get()

    zip_files["data.json"] = json.dumps(options_file)

    zip_bytes = create_zipfile(zip_files)    
    if patch_path:
        with open(patch_path, "wb") as f:
            f.write(zip_bytes)


def create_linked_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Linked Options (applied to the current patch)", padx=8, pady=8)

    vars.death_link_active = BooleanVar()
    death_frame = Frame(frame)
    death_check = Checkbutton(death_frame, variable=vars.death_link_active)
    death_check.pack(side=LEFT, fill=X)
    death_label = Label(death_frame, text="Enable Death Link")
    death_label.pack(side=LEFT, fill=X)

    vars.damage_link_active = BooleanVar()
    damage_frame = Frame(frame)
    damage_check = Checkbutton(damage_frame, variable=vars.damage_link_active)
    damage_check.pack(side=LEFT, fill=X)
    damage_label = Label(damage_frame, text="Enable Damage Link")
    damage_label.pack(side=LEFT, fill=X)

    vars.energy_link_active = BooleanVar()
    energy_frame = Frame(frame)
    energy_check = Checkbutton(energy_frame, variable=vars.energy_link_active)
    energy_check.pack(side=LEFT, fill=X)
    energy_label = Label(energy_frame, text="Enable Energy Link")
    energy_label.pack(side=LEFT, fill=X)

    vars.trap_link_active = BooleanVar()
    trap_frame = Frame(frame)
    trap_check = Checkbutton(trap_frame, variable=vars.trap_link_active)
    trap_check.pack(side=LEFT, fill=X)
    trap_label = Label(trap_frame, text="Enable Trap Link")
    trap_label.pack(side=LEFT, fill=X)

    death_frame.pack(side=TOP, fill=X)
    damage_frame.pack(side=TOP, fill=X)
    energy_frame.pack(side=TOP, fill=X)
    trap_frame.pack(side=TOP, fill=X)

    return frame, vars


def create_global_frame(parent=None):
    vars_ns = Namespace()
    frame = LabelFrame(parent, text="Global Options (applies to all sessions)", padx=8, pady=8)

    def save_callback():
        nonlocal vars_ns
        save_vars = Namespace()
        save_vars.guaranteed_rewards = vars_ns.guaranteed_rewards.get()
        save_vars.random_rewards = vars_ns.random_rewards.get()
        persistent_store("global_settings", GAME_NAME, save_vars)

    vars_ns.guaranteed_rewards = BooleanVar()
    guaranteed_rewards_frame = Frame(frame)
    guaranteed_rewards_check = Checkbutton(guaranteed_rewards_frame, variable=vars_ns.guaranteed_rewards, command=save_callback)
    guaranteed_rewards_check.pack(side=LEFT, fill=X)
    guaranteed_rewards_label = Label(guaranteed_rewards_frame, text="Guaranteed DK Coins and G letters in goals")
    guaranteed_rewards_label.pack(side=LEFT, fill=X)

    vars_ns.random_rewards = BooleanVar()
    random_rewards_frame = Frame(frame)
    random_rewards_check = Checkbutton(random_rewards_frame, variable=vars_ns.random_rewards, command=save_callback)
    random_rewards_check.pack(side=LEFT, fill=X)
    random_rewards_label = Label(random_rewards_frame, text="Random rewards in goals")
    random_rewards_label.pack(side=LEFT, fill=X)
    
    persistent_settings = persistent_load().get("global_settings", {}).get(GAME_NAME, Namespace())
    if hasattr(persistent_settings, "guaranteed_rewards"):
            vars_ns.guaranteed_rewards.set(persistent_settings.guaranteed_rewards)
    else:
        vars_ns.guaranteed_rewards.set(False)
    if hasattr(persistent_settings, "random_rewards"):
            vars_ns.random_rewards.set(persistent_settings.random_rewards)
    else:
        vars_ns.random_rewards.set(False)

    guaranteed_rewards_frame.pack(side=TOP, fill=X)
    random_rewards_frame.pack(side=TOP, fill=X)

    return frame, vars_ns


def create_trivia_frame(parent=None):
    vars = Namespace()
    frame = LabelFrame(parent, text="Trivia Options (applies to all sessions)", padx=8, pady=8, name="trivia_options")
    vars.question_count = IntVar()
    vars.question_total_count = StringVar()
    vars.valid_topics = {}

    states = ["Session", "Forced", "Excluded"]

    persistent_settings = persistent_load().get("trivia_settings", {}).get(GAME_NAME, Namespace())
    
    if hasattr(persistent_settings, "question_count"):
        if persistent_settings.question_count == 0:
            vars.question_count.set(1)
        else:
            vars.question_count.set(persistent_settings.question_count)
    else:
        vars.question_count.set(1)

    def on_spin_update():
        nonlocal vars

        #string: str = vars.question_total_count.get()
        #easy_count = int(string.split("|")[0].split(":")[1].strip())
        #medium_count = int(string.split("|")[1].split("|")[0].split(":")[1].strip())
        #hard_count = int(string.split("|")[2].split(":")[1].strip())

        #min_count = min(easy_count, medium_count, hard_count)
        #current_count = vars.question_count.get() * 6
        #if current_count >= min_count:
        #    vars.question_count.set(min_count // 6)

        save_vars = Namespace()
        save_vars.valid_topics = {}
        save_vars.question_count = vars.question_count.get()
        for topic_name, topic_bool in vars.valid_topics.items():
            option = topic_bool.get()
            if option == "Included":
                option = "Session"
            save_vars.valid_topics[topic_name] = option
        persistent_store("trivia_settings", GAME_NAME, save_vars)

    question_count_frame = Frame(frame)
    question_count_spin = Spinbox(question_count_frame, textvariable=vars.question_count, from_=1, to=6, width=3, relief="sunken",
                                   repeatdelay=500, repeatinterval=100, command=on_spin_update)
    question_count_label = Label(question_count_frame, text="Question count: ")
    question_total_label = Label(question_count_frame, text="")
    question_total_count_label = Label(question_count_frame, textvariable=vars.question_total_count)

    question_count_label.pack(side=LEFT, fill=X)
    question_count_spin.pack(side=LEFT, fill=X)
    question_total_count_label.pack(side=RIGHT, fill=X)
    question_total_label.pack(side=RIGHT, fill=X)

    separator_count = Separator(frame, orient=tk.HORIZONTAL)

    questions_frame = Frame(frame)

    canvas = Canvas(questions_frame)
    canvas.pack(side=LEFT, fill=BOTH)
    scrollbar = Scrollbar(questions_frame, orient=VERTICAL, command=canvas.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    canvas.configure(yscrollcommand=scrollbar.set)
    scrollable_frame = Frame(canvas)

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    def update_trivia(*args):
        nonlocal vars
        easy_count = 0
        medium_count = 0
        hard_count = 0
        save_vars = Namespace()
        save_vars.valid_topics = {}
        save_vars.question_count = vars.question_count.get()
        for topic_name, topic_setting in vars.valid_topics.items():
            save_vars.valid_topics[topic_name] = topic_setting.get()
            if save_vars.valid_topics[topic_name] == "Included":
                save_vars.valid_topics[topic_name] = "Session"
            if topic_setting.get() in ["Forced", "Included"]:
                easy_count, medium_count, hard_count = add_trivia_count(topic_name, easy_count, medium_count, hard_count)
        
        vars.question_total_count.set(f"Easy: {easy_count} | Medium: {medium_count} | Hard: {hard_count}")
        
        #min_count = min(easy_count, medium_count, hard_count)
        #current_count = vars.question_count.get() * 6
        #if current_count >= min_count:
        #    vars.question_count.set(min_count // 6)

        persistent_store("trivia_settings", GAME_NAME, save_vars)

    easy_count = 0
    medium_count = 0
    hard_count = 0
    for topic_name, topic in trivia_topics.items():
        vars.valid_topics[topic_name] = StringVar()
        vars.valid_topics[topic_name].trace_add("write", update_trivia)
        vars.valid_topics[topic_name].set("Session")

        sanitized_name = filter_characters(topic_name)
        topic_frame = Frame(scrollable_frame, name=sanitized_name)
        #topic_check = Checkbutton(topic_frame, variable=vars.valid_topics[topic_name], command=on_checkbox_toggle)
        topic_check = OptionMenu(topic_frame, vars.valid_topics[topic_name], *states)
        topic_check.config(width=8)
        topic_check.pack(side=LEFT, fill=X)
        topic_label = Label(topic_frame, text=topic_name)
        topic_label.pack(side=LEFT, fill=X)
        topic_frame.pack(side=TOP, fill=X)
        
        if topic_name == "Donkey Kong Country 2":
            vars.valid_topics["Donkey Kong Country 2"].set("Forced")
            topic_check.config(state="disabled")
            if not hasattr(persistent_settings, "valid_topics"):
                persistent_settings.valid_topics = {}
            persistent_settings.valid_topics["Donkey Kong Country 2"] = "Forced"

        if hasattr(persistent_settings, "valid_topics"):
            if topic_name in persistent_settings.valid_topics:
                vars.valid_topics[topic_name].set(persistent_settings.valid_topics[topic_name])
                if persistent_settings.valid_topics[topic_name] == "Forced":
                    easy_count, medium_count, hard_count = add_trivia_count(topic_name, easy_count, medium_count, hard_count)

    vars.question_total_count.set(f"Easy: {easy_count} | Medium: {medium_count} | Hard: {hard_count}")

    #min_count = min(easy_count, medium_count, hard_count)
    #current_count = vars.question_count.get() * 6
    #if current_count >= min_count:
    #    vars.question_count.set(min_count // 6)

    question_count_frame.pack(side=TOP, fill=X)
    separator_count.pack(fill=X, expand=True, pady=10)
    questions_frame.pack(side=TOP, fill=X)

    return frame, vars, scrollable_frame


def add_trivia_count(topic_name: str, easy_count: int, medium_count: int, hard_count: int) -> list[int, int, int]:
    easy_count += len(trivia_topics[topic_name].easy_questions)
    medium_count += len(trivia_topics[topic_name].medium_questions)
    hard_count += len(trivia_topics[topic_name].hard_questions)
    if topic_name == "Donkey Kong Country 2":
        easy_count += 7
        medium_count += 15
        hard_count += 19

    return easy_count, medium_count, hard_count


def create_zipfile(files: dict[str, bytes]) -> io.BytesIO:
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
        for filename, content in files.items():
            zf.writestr(filename, content)
    zip_buffer.seek(0)
    return zip_buffer.getvalue()


def filter_characters(string: str, maintain_casing: bool = False) -> str:
    if not maintain_casing:
        string = string.lower()
    string = string.replace(" -", "")
    f = "!#$%&/()+-/':."
    for char in f:
        string = string.replace(char, "")
    string = string.replace(" ", "_")
    return string


def launch(*launcher_args):
    main(launcher_args)


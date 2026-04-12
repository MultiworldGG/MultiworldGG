import os
import pkgutil
import re
from pathlib import Path
from textwrap import dedent

from kvui import ThemedApp, ScrollBox, MDTextField, MDBoxLayout, MDLabel
from kivy.core.clipboard import Clipboard
from kivy.factory import Factory
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivymd.uix.behaviors import HoverBehavior
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

import Utils
from .json_megamix import process_mods, ConflictException
from .. import MegaMixWorld
from ..DataHandler import restore_originals, game_paths


class AssociatedMDLabel(MDLabel):
    def __init__(self, text, associate):
        MDLabel.__init__(self)
        self.text = text
        self.associate = associate
        self.valign = 'center'

    def on_touch_down(self, touch):
        MDLabel.on_touch_down(self, touch)
        if self.collide_point(touch.pos[0], touch.pos[1]):
            self.associate.active = not self.associate.active

class MDBoxLayoutHover(MDBoxLayout, HoverBehavior):
    pass

class DivaJSONGenerator(ThemedApp):
    container: MDBoxLayout = ObjectProperty(None)
    pack_list_scroll: ScrollBox = ObjectProperty(None)
    filter_input: MDTextField = ObjectProperty(None)

    mods_folder = game_paths().get("mods")
    self_mod_name = game_paths().get("modname")
    labels = []

    def find_db_folder(self, dbs: set[str]) -> list:
        found = []

        for root, _, files in os.walk(self.mods_folder):
            if not any(f in dbs for f in files):
                continue

            folder_name = str(Path(root).parent.relative_to(Path(self.mods_folder)))
            if self.self_mod_name and folder_name.startswith(self.self_mod_name):
                continue

            found.append((root, folder_name))

        return sorted(found)

    def create_pack_list(self):
        self.labels = []
        self.pack_list_scroll.layout.clear_widgets()

        for _, folder_name in self.find_db_folder({'mod_pv_db.txt', 'mod_nc_pv_db.txt'}):
            self.pack_list_scroll.layout.add_widget(self.create_pack_line(folder_name))

    def find_nc_db_ids(self):
        nc_db_ids = set()

        for pack, _ in self.find_db_folder({'nc_db.toml'}):
            with open(os.path.join(pack, 'nc_db.toml'), 'r') as nc_db:
                # The power of not vendoring TOML
                nc_ids = [int(i) for i in re.findall("^id\s*=\s*(\d+)$", nc_db.read(), re.MULTILINE)]
                nc_db_ids.update(nc_ids)

        print(sorted(nc_db_ids))

    def create_pack_line(self, name: str):
        box = MDBoxLayoutHover()

        checkbox = CheckBox()
        label = AssociatedMDLabel(name, checkbox)
        self.labels.append(label)

        box.add_widget(checkbox)
        box.add_widget(label)

        return box

    def toggle_checkbox(self, active: bool = True, search: str = "", import_dml: bool = False):
        dml_config = ""
        if import_dml:
            dml_path = os.path.join(os.path.dirname(self.mods_folder), "config.toml")
            try:
                with open(dml_path, "r", encoding='utf-8', errors='ignore') as DMLConfig:
                    dml_config = DMLConfig.read()
                self.show_snackbar("Imported from DML")
            except Exception as e:
                dialog_dml = Factory.DialogGeneric()
                dialog_dml.icon = "alert"
                dialog_dml.title = "Could not locate or read DML config"
                dialog_dml.field = str(e)
                dialog_dml.open()

        for label in self.labels:
            # The split may need to be /-aware in the future.
            if import_dml and label.text.split("\\")[0] not in dml_config:
                continue
            elif search:
                if "/" == search[0] == search[-1]:
                    if not re.search(search[1:-1], label.text):
                        continue
                elif search.lower() not in label.text.lower():
                    continue
            label.associate.active = active

    def toggle_checkbox_from_input(self, active: bool = False):
        if self.filter_input.text:
            self.toggle_checkbox(active=active, search=self.filter_input.text)

    def filter_pack_list(self, _, search: str):
        self.pack_list_scroll.layout.clear_widgets()
        self.pack_list_scroll.scroll_y = 1

        for label in self.labels:
            if search:
                if "/" == search[0] == search[-1]:
                    if not re.search(search[1:-1], label.text):
                        continue
                elif search.lower() not in label.text.lower():
                    continue
            self.pack_list_scroll.layout.add_widget(label.parent)

    def process_to_clipboard(self):
        checked_packs = [str(os.path.join(self.mods_folder, label.text)) for label in self.labels if label.associate.active]
        mod_pv_db_paths_list = [folder_path for folder_path in checked_packs]

        if not mod_pv_db_paths_list:
            self.show_snackbar("No song packs selected")
            return

        try:
            count, mod_pv_db_json = process_mods(self.mods_folder, mod_pv_db_paths_list)
        except ConflictException as e:
            self.copy(str(e))

            dialog_conflict = Factory.DialogGeneric()
            dialog_conflict.title = "Conflicting IDs prevent generating"
            dialog_conflict.desc = dedent("""\
                                        [b]This is not for use in the YAML.[/b]
                                        
                                        This is common for packs that target the base game or add covers.
                                        Listed below are conflicting packs and IDs. Uncheck some or all of them.
                                        """)
            dialog_conflict.field = str(e)
            dialog_conflict.open()

            return

        json_length = round(len(mod_pv_db_json) / 1024, 2)

        dialog_export = Factory.DialogExport()
        dialog_export.title = "Generated mod string"
        if self.copy(mod_pv_db_json):
            dialog_export.desc = "The mod string was automatically copied to the clipboard.\n\n"
        dialog_export.desc += f"{len(checked_packs)} pack(s) ({json_length} KiB)\n{count} unique song IDs\n"
        dialog_export.field = mod_pv_db_json

        dialog_export.open()

        return

    def open_mods_folder(self):
        Utils.open_file(self.mods_folder)

    @staticmethod
    def open_help():
        Utils.open_file("https://github.com/Cynichill/DivaAPworld/blob/main/docs/setup_en.md#mod-songs")

    @staticmethod
    def show_snackbar(message: str = "ooeeoo"):
        MDSnackbar(MDSnackbarText(text=message)).open()

    @staticmethod
    def copy(content: str) -> bool:
        print(content)
        if Utils.is_windows:
            Clipboard.copy(content)
        return Utils.is_windows

    @staticmethod
    def save(content: str, suggest: str = "*.txt"):
        path = Utils.save_filename("Save generator output as...", [("Text files", ["*.txt"])], suggest)

        with open(path, "w", encoding='utf-8') as file:
            file.write(content + "\n")

    def process_restore_originals(self):
        mod_pv_dbs = [f"{self.mods_folder}/{pack}/rom/mod_pv_db.txt" for pack in [label.text for label in self.labels]]
        try:
            restore_originals(mod_pv_dbs)
            self.show_snackbar("Song packs restored")
        except Exception as e:
            self.show_snackbar(str(e))

    def build(self):
        self.title = "Hatsune Miku Project Diva Mega Mix+ JSON Generator"

        data = pkgutil.get_data(MegaMixWorld.__module__, "generator_megamix/generator.kv").decode()
        self.container = Builder.load_string(data)
        self.pack_list_scroll = self.container.ids.pack_list_scroll
        self.filter_input = self.container.ids.filter_input
        self.create_pack_list()

        self.set_colors()
        self.container.md_bg_color = self.theme_cls.backgroundColor

        return self.container


def launch():
    DivaJSONGenerator().run()

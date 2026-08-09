tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import (
        TrackerGameContext as CommonContext,
        TrackerCommandProcessor as ClientCommandProcessor,
    )

    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext, ClientCommandProcessor
import asyncio
import logging

from Utils import async_start
from kvui import GameManager, ScrollBox
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton
from kivymd.uix.label import MDLabel

from .. import Portal2World

HOST = "localhost"
PORT = int(Portal2World.settings.default_portal2_port)

logger = logging.getLogger("Portal2Client")


async def send_instant_command(command: str):
    try:
        _, writer = await asyncio.open_connection(HOST, PORT)
        writer.write((command + "\n").encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
    except:
        logger.error(f"Connection to portal 2 failed for instant command")


class P2ClientCommandProcessor(ClientCommandProcessor):

    def __init__(self, context: "P2CommonContext"):
        super().__init__(context)


class PlayMapButton(MDButton):

    def __init__(self, playable: bool = False, on_release = None):
        if playable:
            button_text = "Play Map"
        else:
            button_text = "Map not yet available"
        super().__init__(
            MDButtonText(text=button_text),
            disabled=not playable
        )
        
            
        if on_release is not None:
            self.bind(on_release=on_release)


class MapInfo(MDBoxLayout):

    def __init__(self, map_data: dict):
        super().__init__(
            orientation="vertical",
            padding=[dp(12), dp(8)],
            spacing=dp(8),
            md_bg_color=[1, 1, 1, 0.12],
            radius=dp(6)
        )
        self.map_data = map_data
        self.build()

    def build(self):
        chapter_name_label = MDLabel(text=self.map_data["title"], halign="center", height=dp(40), size_hint_y=None)
        self.add_widget(chapter_name_label)
        
        required_items_str = "Required Items:\n"

        if self.map_data["required_items"]:
            required_items_str += ", ".join(self.map_data["required_items"])
        else:
            required_items_str += "All required items acquired"

        required_items_label = MDLabel(text=required_items_str)
        self.add_widget(required_items_label)

        if self.map_data["sub_locations"]:
            sub_location_str = "Sub locations:\n"
            sub_locations_incomplete = [
                name
                for name, complete in self.map_data["sub_locations"].items()
                if not complete
            ]
            if sub_locations_incomplete:
                sub_location_str += ", ".join(sub_locations_incomplete)
            else:
                sub_location_str += "All sub locations completed"

            sub_location_label = MDLabel(text=sub_location_str)
            self.add_widget(sub_location_label)

        if self.map_data["disabled"]:
            self.play_map_button = PlayMapButton(playable=False)
        else:
            self.play_map_button = PlayMapButton(
                playable=True, on_release=lambda btn: self.play_map()
            )

        self.add_widget(self.play_map_button)

    def play_map(self):
        """
        Send map command to the game to load the selected map
        """

        async_start(
            send_instant_command(f"{self.map_data['command']}"), "send_map_command"
        )


class SelectableButton(ButtonBehavior, MDBoxLayout):
    def __init__(self, name_text: str, count_text: str, on_release):
        self.name = name_text
        super().__init__(
            orientation="horizontal",
            padding=[dp(12), dp(8)],
            spacing=dp(8),
            size_hint_y=None,
            height=dp(40),
            width=dp(220),
            size_hint_x=None,
            md_bg_color=[1, 1, 1, 0.12],
            radius=dp(6),
        )

        self.name_label = MDLabel(
            text=name_text, width=dp(150), size_hint_x=None, halign="left"
        )
        self.count_label = MDLabel(
            text=count_text,
            halign="right",
        )

        self.add_widget(self.name_label)
        self.add_widget(self.count_label)

        if on_release is not None:
            self.bind(on_release=on_release)

    def select(self):
        self.md_bg_color = [1, 1, 1, 0.3]

    def deselect(self):
        self.md_bg_color = [1, 1, 1, 0.12]


class ChapterButton(SelectableButton):

    def __init__(self, chapter_name: str, chapter_maps: list, on_release):
        self.chapter_name = chapter_name
        self.chapter_maps = chapter_maps
        finished_checks, total_checks = self.calculate_completeness()

        super().__init__(
            self.chapter_name, f"{finished_checks}/{total_checks}", on_release
        )

    def calculate_completeness(self) -> tuple:
        total_checks = 0
        finished_checks = 0
        for map in self.chapter_maps:
            total_checks += map["total_locations"]
            finished_checks += map["finished_locations"]

        return finished_checks, total_checks

    def update_title(self, chapter_maps: list):
        self.chapter_maps = chapter_maps
        finished_checks, total_checks = self.calculate_completeness()
        self.count_label.text = f"{finished_checks}/{total_checks}"


class MenuLayout(MDGridLayout):

    def __init__(self):
        super().__init__(rows=1, cols=3, padding=[40, 10], spacing=dp(10))
        self.menu_info = {}
        self.selected_chapter_btn: ChapterButton = None
        self.selected_map_btn: SelectableButton = None
        self.map_area = None
        self.map_info = None
        self.is_open_world = False
        self.return_to_menu = False
        self.chapter_buttons: list[ChapterButton] = []
        self.map_buttons: list[SelectableButton] = []
        self.built = False

    def update_menu(self, menu_data: dict[str, list], location_id: int | None = None):
        """
        - Set the map data
        - Update the menu
        """
        self.menu_info = menu_data

        self.refresh_chapter_titles()

        if self.map_area and self.selected_chapter_btn:
            self.select_chapter(
                self.selected_chapter_btn.name, self.selected_chapter_btn
            )

            if self.selected_map_btn:
                if not self.return_to_menu and location_id == self.map_info.map_data["location_id"]:
                    # Try to select next map in chapter
                    current_map = next(
                        (
                            m
                            for m in self.map_buttons
                            if m.name == self.selected_map_btn.name
                        ),
                        None,
                    )
                    if current_map:
                        index = self.map_buttons.index(current_map)
                        if index + 1 < len(self.map_buttons):
                            self.select_map(
                                self.map_buttons[index + 1].name,
                                self.map_buttons[index + 1],
                            )
                else:
                    self.select_map(self.selected_map_btn.name)

    def refresh_chapter_titles(self):
        for cb in self.chapter_buttons:
            cb.update_title(self.menu_info[cb.chapter_name])

    def set_open_world(self):
        self.is_open_world = True

    def build(self):
        """
        - List of chapter buttons on the left side
        - Add a dynamic list of map buttons on the right side of the grid that updates based on the selected chapter
        """

        if self.built:
            return

        self.built = True

        if self.menu_info is None:
            raise Exception(
                "Menu data not set. Call update_menu() once before build()."
            )

        self.clear_widgets()
        self.chapter_area = ScrollBox()
        self.chapter_area.layout.orientation = "vertical"
        self.chapter_area.layout.spacing = dp(3)
        self.chapter_area.scroll_type = ["bars"]
        self.chapter_area.do_scroll_x = False
        self.add_widget(self.chapter_area)

        self.map_area = ScrollBox()
        self.map_area.layout.orientation = "vertical"
        self.map_area.layout.spacing = dp(3)
        self.map_area.scroll_type = ["bars"]
        self.map_area.do_scroll_x = False
        self.add_widget(self.map_area)

        for chapter_name, maps in self.menu_info.items():
            chapter_button = ChapterButton(
                chapter_name,
                maps,
                lambda btn, chapter=chapter_name: self.select_chapter(chapter, btn),
            )
            self.chapter_buttons.append(chapter_button)
            self.chapter_area.layout.add_widget(chapter_button)

        menu_toggle_box = MDGridLayout(
            cols=2,
            row_default_height=40,
            row_force_default=True,
            padding=dp(10),
            md_bg_color=[1, 1, 1, 0.1],
            width=dp(220),
            size_hint_x=None,
            height=dp(60),
            size_hint_y=None,
            radius=dp(10),
        )
        self.auto_next_map_button = MDIconButton(
            icon="checkbox-blank-outline", on_release=self.toggle_switch
        )
        button_label = MDLabel(text="Return to menu on map finish: ")
        menu_toggle_box.add_widget(button_label)
        menu_toggle_box.add_widget(self.auto_next_map_button)
        self.chapter_area.layout.add_widget(menu_toggle_box)

    def select_chapter(self, chapter_name: str, btn: ChapterButton = None):
        """
        - Remove the old map buttons
        - Add the list of new map buttons
        """

        if self.selected_chapter_btn:
            self.selected_chapter_btn.deselect()

        if btn:
            self.selected_chapter_btn = btn
            self.selected_chapter_btn.select()

        if self.map_area is None:
            raise Exception(
                "Map area not initialized. Call build() before select_chapter()."
            )

        for child in self.map_area.layout.children[:]:
            self.map_area.layout.remove_widget(child)

        if not self.menu_info:
            no_maps_label = MDLabel(text="No maps available for this chapter")
            self.map_area.layout.add_widget(no_maps_label)
            return

        self.map_buttons = []
        map_data = self.menu_info[chapter_name]
        disable_map = False
        for map in map_data:
            map_button = SelectableButton(
                map["title"],
                f"{map["finished_locations"]}/{map["total_locations"]}",
                on_release=lambda btn, _map_name=map["title"]: self.select_map(
                    _map_name, btn
                ),
            )
            self.map_buttons.append(map_button)
            self.map_area.layout.add_widget(map_button)
            map["disabled"] = disable_map
            if not self.is_open_world:
                disable_map = not map["completed"]

    def select_map(self, map_name: str, btn: SelectableButton = None):
        """
        - Handle the selection of a map button
        - Send map command to the game to load the selected map
        """

        if self.selected_map_btn:
            self.selected_map_btn.deselect()

        if btn:
            self.selected_map_btn = btn
        else:
            possible_buttons = [btn for btn in self.map_buttons if btn.name == map_name]
            if len(possible_buttons) > 0:
                self.selected_map_btn = possible_buttons[0]

        self.selected_map_btn.select()

        maps = self.menu_info[self.selected_chapter_btn.chapter_name]
        map_data = next((map for map in maps if map["title"] == map_name), None)

        if not map_data:
            print(
                f"Map '{map_name}' not found in chapter '{self.selected_chapter_btn.chapter_name}'"
            )
            return

        # Replace the map info area
        if self.map_info:
            self.remove_widget(self.map_info)

        self.map_info = MapInfo(map_data)
        self.add_widget(self.map_info)

    def toggle_switch(self, instance):
        self.return_to_menu = not self.return_to_menu
        if self.return_to_menu:
            self.auto_next_map_button.icon = "checkbox-outline"
        else:
            self.auto_next_map_button.icon = "checkbox-blank-outline"


class P2GameManager(GameManager):

    def build(self):
        container = super().build()

        game_menu = self.add_client_tab("Maps", MenuLayout())
        self.log_panels["Maps"] = game_menu.content

        return container


class P2CommonContext(CommonContext):

    def make_gui(self) -> "type[kvui.GameManager]":
        ui = super().make_gui()

        class TextManager(ui, P2GameManager):
            base_title = "Portal 2 Text Client"
            icon = r"worlds/portal2/data/Portalpelago.png"

        return TextManager

    def get_menu(self) -> "MenuLayout":
        return self.ui.log_panels["Maps"]

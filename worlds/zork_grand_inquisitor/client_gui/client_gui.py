from typing import List, Optional, Set, Tuple

from kvui import GameManager

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget

from ..client import ZorkGrandInquisitorContext, tracker_loaded
from ..enums import ZorkGrandInquisitorEntranceRandomizer

from .client_gui_layouts import ItemsTabLayout, EntrancesTabLayout, TrackerPageLocationLabel

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

def bootstrap_client_gui(gui: type[GameManager]) -> type[GameManager]:
    class ZorkGrandInquisitorManager(gui):
        ctx: ZorkGrandInquisitorContext

        logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
        base_title: str = f"{apname} Zork Grand Inquisitor Client"

        items_tab_layout: ItemsTabLayout
        entrances_tab_layout: Optional[EntrancesTabLayout]

        items_tab: Widget
        entrances_tab: Optional[Widget]

        def build(self) -> Layout:
            container: Layout = super().build()

            self.items_tab_layout = ItemsTabLayout(self.ctx)
            self.items_tab = self.add_client_tab("Items", self.items_tab_layout)

            self.entrances_tab_layout = None
            self.entrances_tab = None

            if tracker_loaded and self.ctx.tracker_page is not None:
                self.ctx.tracker_page.viewclass = TrackerPageLocationLabel

            return container

        def add_client_tab(self, title: str, content: Widget, index: int = -1) -> Widget:
            tab: Widget = super().add_client_tab(title, content, index)

            if title == "Map Page":
                divider: Widget = self.tabs.children[1]

                self.tabs.remove_widget(tab)
                self.tabs.remove_widget(divider)

                tracker_page_index: int = next(
                    i for i, child in enumerate(self.tabs.children) if getattr(child, "text", None) == "Tracker Page"
                )

                self.tabs.add_widget(divider, index=tracker_page_index)
                self.tabs.add_widget(tab, index=tracker_page_index)

                screen_names: List[str] = [name for name in self.screens.local_screen_names if name != title]
                screen_names.insert(screen_names.index("Tracker Page") + 1, title)

                self.screens.local_screen_names = screen_names

            return tab

        def update_tabs(self) -> None:
            self.items_tab_layout.update()

            allowable_entrance_randomizer_values: Set[ZorkGrandInquisitorEntranceRandomizer] = {
                ZorkGrandInquisitorEntranceRandomizer.COUPLED,
                ZorkGrandInquisitorEntranceRandomizer.UNCOUPLED,
            }

            is_entrance_randomizer_enabled: bool = (
                self.ctx.game_controller.option_entrance_randomizer in allowable_entrance_randomizer_values
            )

            if is_entrance_randomizer_enabled and self.entrances_tab is None:
                self.entrances_tab_layout = EntrancesTabLayout(self.ctx)
                self.entrances_tab = self.add_client_tab("Entrances", self.entrances_tab_layout)
            elif not is_entrance_randomizer_enabled and self.entrances_tab is not None:
                if self.screens.current == "Entrances":
                    self.items_tab.dispatch("on_release")

                self.remove_client_tab(self.entrances_tab)

                self.entrances_tab_layout = None
                self.entrances_tab = None

            if self.entrances_tab_layout is not None:
                self.entrances_tab_layout.update()

    return ZorkGrandInquisitorManager

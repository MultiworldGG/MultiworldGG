from typing import List, Tuple

from kvui import GameManager

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget

from ..client import PeggleDeluxeContext

from .client_gui_layouts import PeggleDeluxeTabLayout
try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

class PeggleDeluxeManager(GameManager):
    ctx: PeggleDeluxeContext

    logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
    base_title: str = f"{apname} Peggle Deluxe Client"

    peggle_deluxe_tab_layout: PeggleDeluxeTabLayout

    peggle_deluxe_tab: Widget

    def build(self) -> Layout:
        container: Layout = super().build()

        self.peggle_deluxe_tab_layout = PeggleDeluxeTabLayout(self.ctx)
        self.peggle_deluxe_tab = self.add_client_tab("Peggle Deluxe", self.peggle_deluxe_tab_layout)

        return container

    def update_tabs(self) -> None:
        self.peggle_deluxe_tab_layout.update()

from typing import List, Tuple

from kvui import GameManager

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget

from ..client import PeggleNightsContext

from .client_gui_layouts import PeggleNightsTabLayout

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

class PeggleNightsManager(GameManager):
    ctx: PeggleNightsContext

    logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
    base_title: str = f"{apname} Peggle Nights Client"

    peggle_nights_tab_layout: PeggleNightsTabLayout

    peggle_nights_tab: Widget

    def build(self) -> Layout:
        container: Layout = super().build()

        self.peggle_nights_tab_layout = PeggleNightsTabLayout(self.ctx)
        self.peggle_nights_tab = self.add_client_tab("Peggle Nights", self.peggle_nights_tab_layout)

        return container

    def update_tabs(self) -> None:
        self.peggle_nights_tab_layout.update()

from typing import List, Tuple

from kvui import GameManager

from kivy.uix.layout import Layout
from kivy.uix.widget import Widget

from ..client import PinballFX3Context

from .client_gui_layouts import PinballFX3TabLayout

try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

class PinballFX3Manager(GameManager):
    ctx: PinballFX3Context

    logging_pairs: List[Tuple[str, str]] = [("Client", "Archipelago")]
    base_title: str = f"{apname} Pinball FX3 Client"

    pinball_fx3_tab_layout: PinballFX3TabLayout

    pinball_fx3_tab: Widget

    def build(self) -> Layout:
        container: Layout = super().build()

        self.pinball_fx3_tab_layout = PinballFX3TabLayout(self.ctx)
        self.pinball_fx3_tab = self.add_client_tab("Pinball FX3", self.pinball_fx3_tab_layout)

        return container

    def update_tabs(self) -> None:
        self.pinball_fx3_tab_layout.update()

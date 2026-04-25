from collections.abc import Callable
from typing import Any

from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel

INPUT_MAP_SPECIAL_INT = {
    273: "up",
    274: "down",
    276: "left",
    275: "right",
}


class TwoThousandAndFortyEightGameView(BoxLayout):
    input_function: Callable[[Any], None]
    grid_layout: GridLayout
    score_label: MDLabel

    def __init__(self, input_function: Callable[[Any], None], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.input_function = input_function
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        header_container = BoxLayout(orientation="horizontal", size_hint_y=None, height="60dp")
        self.score_label = MDLabel(
            text="Score: 0",
            font_style="Headline",
            role="medium",
            theme_text_color="Primary",
            halign="left",
            valign="center",
        )
        header_container.add_widget(self.score_label)

        self.reset_button = MDButton(
            MDButtonText(
                text="Reset Game",
            ),
            style="filled",
            on_release=lambda x: self.input_function("reset"),
        )
        header_container.add_widget(self.reset_button)
        self.add_widget(header_container)

        self.grid_layout = GridLayout(cols=4, rows=4, spacing=15, size_hint=(1, 1))
        self.add_widget(self.grid_layout)

        Window.bind(on_key_down=self._on_keyboard_down)

    def _on_keyboard_down(self, _: Any, keycode_int: int, _2: Any, _3: str, _4: Any) -> bool:
        direction = INPUT_MAP_SPECIAL_INT.get(keycode_int)
        if direction:
            self.input_function(direction)
            return True
        return False

    def update_score(self, score: int):
        self.score_label.text = f"Score: {score}"

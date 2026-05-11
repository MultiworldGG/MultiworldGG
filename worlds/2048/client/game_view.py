from collections.abc import Callable
from typing import Any

from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText

from .game import TwoThousandAndFortyEightGame

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
    game: TwoThousandAndFortyEightGame | None
    current_popup: MDSnackbar | None
    queue: list[str]

    def __init__(self, input_function: Callable[[Any], None], **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.current_popup = None
        self.queue = []
        self.input_function = input_function
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 10

        header_container = BoxLayout(orientation="horizontal", size_hint_y=None, height="60dp")
        self.score_label = MDLabel(
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
        if self.game is not None and self.game.unmet_score_thresholds:
            objective = self.game.unmet_score_thresholds[0]
            self.score_label.text = f"Score: {score}/{objective}"
        else:
            self.score_label.text = f"Score: {score}"

    def show_popup(self, message: str) -> None:
        if self.current_popup is None:
            new_popup = MDSnackbar(
                MDSnackbarText(
                    text=message,
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.8,
                duration=2.5,
            )
            self.current_popup = new_popup
            new_popup.bind(on_dismiss=self.remove_popup)
            new_popup.open()
        else:
            self.queue.append(message)

    def remove_popup(self, *_) -> None:
        self.current_popup = None
        if self.queue:
            self.show_popup(self.queue.pop(0))

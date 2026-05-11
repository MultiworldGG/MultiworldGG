import math

from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel

from .game import TwoThousandAndFortyEightGame


class TileWidget(MDFloatLayout):
    def __init__(self):
        super().__init__()
        self.game: TwoThousandAndFortyEightGame | None = None
        self.size_hint = (1, 1)
        self.value = 0

        self.label = MDLabel(
            text="",
            halign="center",
            valign="center",
            size_hint=(1, 1),
            pos_hint={"center_x": .5, "center_y": .5},
            theme_text_color="Custom",
            text_color=(0.1, 0.1, 0.1, 1),
            bold=True
        )
        self.label.bind(size=self.label.setter("text_size"))

        self.add_widget(self.label)
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *_):
        self.label.font_size = self.height * 0.45
        self.set_value(self.value)

    def set_value(self, value: int):
        self.value = value
        self.label.text = str(value) if value > 0 else ""

        if value == 0:
            bg_color = (0.8, 0.75, 0.71, 1)
        else:
            step = math.log2(value)

            r = 0.95
            g = max(0.2, 0.9 - (step * 0.1))
            b = max(0.1, 0.8 - (step * 0.15))
            bg_color = (r, g, b, 1)

        if self.game is not None and value in self.game.owned_merges:
            alpha = 1
        else:
            alpha = 0.5

        if value <= 4:
            if self.game is not None and alpha == 1 and value * 2 not in self.game.checked_locations:
                self.label.text_color = (0.3, 0.3, 0.7, 1)
            else:
                self.label.text_color = (0.3, 0.3, 0.3, alpha)
        else:
            if alpha == 1 and value * 2 not in self.game.checked_locations:
                self.label.text_color = (0.5, 0.9, 1, 1)
            else:
                self.label.text_color = (1, 1, 1, alpha)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(6)])
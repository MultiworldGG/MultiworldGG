import math

from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel

class TileWidget(MDFloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
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
            # font_size removed from here as it's now dynamic
            bold=True
        )
        self.label.bind(size=self.label.setter('text_size'))

        self.add_widget(self.label)
        # update_canvas will now handle both background and font resizing
        self.bind(pos=self.update_canvas, size=self.update_canvas)

    def update_canvas(self, *args):
        # This ensures the text scales whenever the window or grid resizes
        self.label.font_size = self.height * 0.45
        self.set_value(self.value)

    def set_value(self, val: int):
        self.value = val
        self.label.text = str(val) if val > 0 else ""

        # 1. Default for empty tiles
        if val == 0:
            bg_color = (0.8, 0.75, 0.71, 1)
        else:
            # 2. Get the "step" (2->1, 4->2, 8->3, 16->4, etc.)
            step = math.log2(val)

            # 3. Compute a simple color shift
            # As step increases, Red stays high, Green drops, Blue drops
            r = 0.95
            g = max(0.2, 0.9 - (step * 0.1))
            b = max(0.1, 0.8 - (step * 0.15))
            bg_color = (r, g, b, 1)

        # 4. Text contrast: Dark text for small numbers, White for large
        self.label.text_color = (0.3, 0.3, 0.3, 1) if val <= 4 else (1, 1, 1, 1)

        self.canvas.before.clear()
        with self.canvas.before:
            Color(*bg_color)
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(6)])
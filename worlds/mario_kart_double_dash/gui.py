from importlib import resources
from io import BytesIO
from kivy.core.image import Image
from kivy.metrics import dp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.fitimage import FitImage
from kvui import GameManager, MDBoxLayout, MDGridLayout, MDLabel
from . import game_data, version
try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

def make_gui(base_class: type[GameManager], ut_title: str) -> type[GameManager]:
    class MKDDManager(base_class):
        logging_pairs = [("Client", "Archipelago")]
        base_title = f"MKDD AP Client {version.get_version()}{ut_title} | {apname}"
        

        def build(self):
            container = super().build()

            def get_image(source: str, width: int = 0, height: int = 0) -> FitImage:
                """Loads and image from images/ folder and returns it as a widget."""
                img = resources.files(__package__ + ".images").joinpath(source)
                data = img.read_bytes()
                raw_image = Image(BytesIO(data), ext=img.suffix[1:])
                image = FitImage(texture=raw_image.texture)
                if width > 0:
                    image.size_hint_x = None
                    image.width = dp(width)
                if height > 0:
                    image.size_hint_y = None
                    image.height = dp(height)
                return image
            
            self.status_bar = MDGridLayout(
                rows=2,
                size_hint_y = None,
                height = dp(100),
                spacing = dp(5),
                padding = dp(5),
            )
            self.grid.add_widget(self.status_bar)
            
            # Trophies
            self.status_bar.add_widget(get_image("trophy_1.png", 36, 36))
            self.trophies_text: MDLabel = MDLabel(text="0/10", halign="left", role="large")
            self.status_bar.add_widget(self.trophies_text)

            # Characters
            self.status_bar.add_widget(MDLabel(text="Characters", halign="right", role="large"))
            char_grid = MDGridLayout(rows = 2, padding = 0, size_hint_x = None, width = dp(180))
            self.status_bar.add_widget(char_grid)
            self.character_icons: list[FitImage] = []
            for i in range(20):
                self.character_icons.append(get_image(f"character_{i + 1}.png", 18, 18))
            # Grid is filled in row-major order, but characters are in column-major, so we need to pivot.
            for y in range(2):
                for x in range(10):
                    char_grid.add_widget(self.character_icons[x * 2 + y])

            # Cups
            cup_box = MDBoxLayout(orientation="horizontal", spacing=dp(5))
            self.status_bar.add_widget(cup_box)
            cup_box.add_widget(MDLabel()) # For alignment...
            self.cc_text: MDLabel = MDLabel(text="50CC", halign="right", role="large", size_hint_x=None, width=dp(50))
            cup_box.add_widget(self.cc_text)
            self.cup_icons: list[FitImage] = []
            for i in range(4):
                self.cup_icons.append(get_image(f"cup_{i + 1}.png", 36, 36))
                cup_box.add_widget(self.cup_icons[i])

            # Speed
            self.status_bar.add_widget(get_image("speed.png", 36, 36))
            self.speed_text: MDLabel = MDLabel(text="0/3", halign="left", role="large")
            self.status_bar.add_widget(self.speed_text)

            # Karts
            self.status_bar.add_widget(MDLabel(text="Karts", halign="right", role="large"))
            kart_grid = MDGridLayout(rows=2, padding=0, size_hint_x=None, width=dp(18 * 11))
            self.status_bar.add_widget(kart_grid)
            self.kart_icons: list[FitImage] = []
            for i in range(20):
                self.kart_icons.append(get_image(f"character_{i + 1}.png", 18, 18))
            self.kart_icons.append(get_image("trophy_1.png", 18, 18))
            # Grid is filled in row-major order, but karts are in column-major, so we need to pivot.
            for y in range(2):
                for x in range(10):
                    kart_grid.add_widget(self.kart_icons[x * 2 + y])
                    if x == 9 and y == 0:
                        kart_grid.add_widget(self.kart_icons[20])

            self.launch_button: MDButton = MDButton(MDButtonText(text="Launch Game"), style="filled", radius=5)
            self.status_bar.add_widget(self.launch_button)
            # Don't ask why, but the layout screws up if there isn't a button here, so a placeholder.
            # One would think disabling the button would do something, but for whatever reason it disables only visually.
            self.launch_button2: MDButton = MDButton(MDButtonText(text="Launch Game"), radius=5)
            return container
        
        def set_launch_func(self, f) -> None:
            self.launch_button.bind(on_release=f)
        
        def show_launch_button(self, show: bool) -> None:
            if show:
                if self.launch_button not in self.status_bar.children:
                    self.status_bar.add_widget(self.launch_button)
                    self.status_bar.remove_widget(self.launch_button2)
            else:
                if self.launch_button in self.status_bar.children:
                    self.status_bar.remove_widget(self.launch_button)
                    self.status_bar.add_widget(self.launch_button2)

        def update_trophies(self, current: int, goal: int) -> None:
            self.trophies_text.text = f"{current}/{goal}"

        def update_characters(self, unlocked_characters: list[int]) -> None:
            for idx, img in enumerate(self.character_icons):
                img.opacity = 1 if idx in unlocked_characters else .2

        def update_cc(self, current_vehile_class: int) -> None:
            self.cc_text.text = ["50CC", "100CC", "150CC", "Mirror"][min(3, current_vehile_class)]

        def update_cups(self, unlocked_cups: list[int]) -> None:
            for idx, img in enumerate(self.cup_icons):
                img.opacity = 1 if idx in unlocked_cups else .2
    
        def update_speed_upgrades(self, current: int, in_pool: int) -> None:
            self.speed_text.text = f"{current}/{in_pool}"

        def update_karts(self, unlocked_karts: list[int]) -> None:
            # Kart ids are different from character ids, but they are shown in order of the characters.
            for idx, img in enumerate(self.kart_icons):
                kart_no: int = 20 # Parade Kart isn't anybody's default.
                if idx < 20:
                    kart_no = game_data.CHARACTERS[idx].default_kart
                img.opacity = 1 if kart_no in unlocked_karts else .2
        
    return MKDDManager

import kvui  # noqa: F401 # isort: skip

import os
import shutil
from pathlib import Path

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText

import Utils
from CommonClient import gui_enabled
from settings import get_settings

from ...patching.RomData import RomData
from ..microbmp import MicroBMP
from ..sprite import blue_palette, bw_palette, green_palette, orange_palette, red_palette
from ..sprite.decoding import load_link_data, load_link_sprite
from ..sprite.encoding import encode_sprite, has_separator, remap_sprite


async def main() -> None:
    if not gui_enabled:
        raise RuntimeError("GUI not enabled.")

    Utils.init_logging("Oracle of Seasons Sprite Editor")
    ImageApp().run()


oos_button_text = "Select sprite for OoS"
sprite_cache_folder = Path(Utils.cache_path("oos_ooa/sprites"))
class ImageApp(MDApp):
    def build(self):
        sprite_cache_folder.mkdir(parents=True, exist_ok=True)

        layout = BoxLayout(orientation="vertical")

        self.img = Image(source="", fit_mode="contain", size_hint_y=1)
        layout.add_widget(self.img)

        bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=48)
        bar.add_widget(MDButton(MDButtonText(text="Load Link"), on_release=self.load_link))
        bar.add_widget(MDButton(MDButtonText(text="Load Last Sprite"), on_release=self.load_last))
        bar.add_widget(MDButton(MDButtonText(text="Load Sprite..."), on_release=self.load_sprite))
        bar.add_widget(MDButton(MDButtonText(text="Switch Palette"), on_release=self.switch_palette))
        bar.add_widget(MDButton(MDButtonText(text="Switch Separator"), on_release=self.switch_separator))
        layout.add_widget(bar)

        bar = BoxLayout(orientation="horizontal", size_hint_y=None, height=48)
        bar.add_widget(MDButton(MDButtonText(text="Export Image"), on_release=self.export_image))
        bar.add_widget(MDButton(MDButtonText(text="Export Binary"), on_release=self.export_binary))
        settings = get_settings()
        if hasattr(settings, "tloz_oos_options") and not isinstance(settings.tloz_oos_options, dict):
            # OoS is loaded
            bar.add_widget(MDButton(MDButtonText(text=oos_button_text), on_release=self.select_sprite))
        if hasattr(settings, "tloz_ooa_options") and not isinstance(settings.tloz_ooa_options, dict):
            # OoA is loaded
            bar.add_widget(MDButton(MDButtonText(text="Select sprite for OoA"), on_release=self.select_sprite))
        layout.add_widget(bar)
        return layout

    def load_link(self, *_) -> None:
        file_name = str(sprite_cache_folder.joinpath("link.bmp"))

        settings = get_settings()
        if hasattr(settings, "tloz_oos_options"):
            rom_file = get_settings().tloz_oos_options.rom_file
        else:
            rom_file = get_settings().tloz_ooa_options.rom_file
        rom = RomData(bytes(open(rom_file, "rb").read()))
        sprite_data = load_link_data(rom)
        image = load_link_sprite(sprite_data)
        image.palette = green_palette
        image.save(file_name)

        self.img.source = file_name
        self.img.reload()
        self.img.texture.mag_filter = "nearest"  # prevents blur when scaling up
        self.img.texture.min_filter = "nearest"  # prevents blur when scaling down

    def load_sprite_from_path(self, path: str):
        new_file_name = str(sprite_cache_folder.joinpath(f"{Path(path).stem}.bmp"))
        if path.endswith(".bin"):
            image = load_link_sprite(Path(path).read_bytes())
            image.palette = green_palette
            image.save(new_file_name)
        else:
            image = MicroBMP().load(path)
            remap_sprite(image)
            image.save(new_file_name)
        self.img.source = new_file_name
        self.img.reload()
        self.img.texture.mag_filter = "nearest"  # prevents blur when scaling up
        self.img.texture.min_filter = "nearest"  # prevents blur when scaling down

    def load_last(self, *_) -> None:
        sprites = sprite_cache_folder.glob("*.bmp")
        latest_file = max(sprites, key=os.path.getmtime, default=None)
        if latest_file is None:
            return
        self.load_sprite_from_path(str(latest_file))

    def load_sprite(self, *_) -> None:
        file_name = Utils.open_filename(
            "Select sprite file", (("*", (".bin", ".bmp")), ("Binary", (".bin",)), ("Image", (".bmp",)))
        )
        if not file_name:
            return
        self.load_sprite_from_path(file_name)

    def switch_palette(self, *_) -> None:
        if self.img.source == "":
            return

        image = MicroBMP().load(self.img.source)
        remap_sprite(image)
        if image.palette == bw_palette:
            image.palette = green_palette
        elif image.palette == green_palette:
            image.palette = blue_palette
        elif image.palette == blue_palette:
            image.palette = red_palette
        elif image.palette == red_palette:
            image.palette = orange_palette
        else:
            image.palette = bw_palette
        image.save(self.img.source)
        self.img.reload()
        self.img.texture.mag_filter = "nearest"  # prevents blur when scaling up
        self.img.texture.min_filter = "nearest"  # prevents blur when scaling down

    def switch_separator(self, *_) -> None:
        if self.img.source == "":
            return

        image = MicroBMP().load(self.img.source)
        remap_sprite(image)
        palette = image.palette
        encoded = encode_sprite(image)
        image = load_link_sprite(encoded, not has_separator(image))
        image.palette = palette
        image.save(self.img.source)
        self.img.reload()
        self.img.texture.mag_filter = "nearest"  # prevents blur when scaling up
        self.img.texture.min_filter = "nearest"  # prevents blur when scaling down

    def export_image(self, *_) -> None:
        if self.img.source == "":
            return

        image_name = Path(self.img.source).stem
        file_path = Utils.save_filename("Save sprite file", (("BMP", (".bmp",)),), f"{image_name}.bmp")
        if not file_path:
            return
        shutil.copy(self.img.source, file_path)

    def export_binary(self, *_) -> None:
        if self.img.source == "":
            return

        image_name = Path(self.img.source).stem
        file_path = Utils.save_filename("Save sprite binary", (("BIN", (".bin",)),), f"{image_name}.bin")
        if not file_path:
            return

        image = MicroBMP().load(self.img.source)
        remap_sprite(image)
        encoded = encode_sprite(image)

        with open(file_path, "wb") as f:
            f.write(encoded)

    def select_sprite(self, *args) -> None:
        if self.img.source == "":
            return
        button_label = args[0].children[0].text
        seasons = button_label == oos_button_text
        image = MicroBMP().load(self.img.source)
        remap_sprite(image)
        encoded = encode_sprite(image)

        image_name = Path(self.img.source).stem
        if image_name == "link":
            image_name = "custom sprite"
        sprite_folder = Utils.local_path(os.path.join("data", "sprites", "oos_ooa"))
        if not os.path.exists(sprite_folder):
            os.makedirs(sprite_folder)
        file_path = Path(sprite_folder, f"{image_name}.bin")
        with open(file_path, "wb") as f:
            f.write(encoded)

        palette_name: str | None
        if image.palette == green_palette:
            palette_name = "green"
        elif image.palette == blue_palette:
            palette_name = "blue"
        elif image.palette == red_palette:
            palette_name = "red"
        elif image.palette == orange_palette:
            palette_name = "orange"
        else:
            palette_name = None
        settings = get_settings()
        if seasons and hasattr(settings, "tloz_oos_options") and not isinstance(settings.tloz_oos_options, dict):
            settings.tloz_oos_options.character_sprite = image_name
            if palette_name is not None:
                settings.tloz_oos_options.character_palette = palette_name
            settings.tloz_oos_options._changed = True

        if not seasons and hasattr(settings, "tloz_ooa_options") and not isinstance(settings.tloz_ooa_options, dict):
            settings.tloz_ooa_options.character_sprite = image_name
            if palette_name is not None:
                settings.tloz_ooa_options.character_palette = palette_name
            settings.tloz_ooa_options._changed = True

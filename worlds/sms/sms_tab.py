from kvui import GameManager, MDLabel, MDBoxLayout, MDScreen, MDFloatLayout
from kivymd.uix.fitimage import FitImage

def build_gui(ui: GameManager):
    ui.sms_layout = MDBoxLayout(orientation="vertical")
    _make_progressive_layout(ui)
    ui.add_client_tab("SMS Items", ui.sms_layout)

def _make_progressive_layout(ui: GameManager, debug: bool = False):
    debug_color = [0,0,0,0]
    if debug:
        debug_color = [0,0,1,1]

    root_layout = MDBoxLayout(padding=[5, 5, 5, 5], line_color=debug_color)
    ui.shine_count = MDLabel(text="0 / 0", halign="center", font_style="Display", role="small")
    root_layout.add_widget(_make_text_layout("Required Shines:", ui.shine_count))
    ui.sms_layout.add_widget(root_layout)

    second_layout = MDBoxLayout(padding=[5, 5, 5, 5], line_color=debug_color)
    ui.blue_coins = MDLabel(text="0 / 0", halign="center", font_style="Display", role="small")
    second_layout.add_widget(_make_text_layout("Required Blue Coins:", ui.blue_coins))
    ui.sms_layout.add_widget(second_layout)

    third_layout = MDBoxLayout(line_color=debug_color)
    ui.tickets = MDLabel(text="N/A", halign="center", font_style="Display", role="small")
    third_layout.add_widget(_make_text_layout("Current Tickets:", ui.tickets))
    ui.sms_layout.add_widget(third_layout)

    # second_layout = MDBoxLayout(padding=[5, 5, 5, 5], line_color=debug_color)
    # ui.king_boo_label = MDLabel(text="0", font_style="Display", halign="center")
    # ui.balcony_boo_label = MDLabel(text="0", font_style="Display", halign="center")
    # second_layout.add_widget(_make_text_layout("King Boo", ui.king_boo_label))
    # second_layout.add_widget(_make_text_layout("Balcony Boo", ui.balcony_boo_label))
    #ui.sms_layout.add_widget(second_layout)

def _make_image_layout(image_path: str, debug: bool = False):
    debug_color = [0,0,0,0]
    if debug:
        debug_color = [0,0,1,1]
    layout = MDFloatLayout(line_color=debug_color)
    screen = MDScreen(layout)
    image = FitImage(source=image_path, fit_mode="contain")

    layout.add_widget(image)
    layout.add_widget(MDLabel(text="0", font_style="Display", halign="right", pos_hint={"center_y":.1}))

    return screen

def _make_text_layout(text: str, counter: MDLabel, debug: bool = False):
    debug_color = [0,0,0,0]
    if debug:
        debug_color = [0,0,1,1]
    layout = MDBoxLayout(orientation="vertical", line_color=debug_color, padding=[5, 5, 5, 5])
    label = MDLabel(text=text, font_style="Display", role="small", halign="center", pos_hint={ "center_x":.5,"center_y":.5 }, width=200)

    layout.add_widget(label)
    layout.add_widget(counter)

    return layout
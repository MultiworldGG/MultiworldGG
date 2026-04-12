from kvui import GameManager, MDLabel, MDBoxLayout, MDScreen, MDLinearProgressIndicator, MDFloatLayout
from kivymd.uix.fitimage import FitImage

def build_gui(ui: GameManager):
    ui.lm_layout = MDBoxLayout(orientation="vertical")
    ui.wallet_progress_bar = MDLinearProgressIndicator(type="indeterminate", size_hint_x=.9, pos_hint={'center_x':.5, 'center_y':.5 }, max=1)
    ui.boo_progress_bar = MDLinearProgressIndicator(type="indeterminate", size_hint_x=.9, pos_hint={'center_x':.5, 'center_y':.5 }, max=1)
    ui.boo_count = MDLabel(text="0 / 50", halign="center", font_style="Display", role="medium")
    ui.wallet_ui = MDLabel(text="0 / Required Money: 0", halign="center", font_style="Display", role="medium", width=5000)

    _make_progressive_layout(ui)
    _make_progress_bar_layout(ui, ui.boo_count, ui.boo_progress_bar, "Boos")
    _make_progress_bar_layout(ui, ui.wallet_ui, ui.wallet_progress_bar, "Wallet")

    ui.add_client_tab("Luigi's Mansion", ui.lm_layout)

def _make_progress_bar_layout(ui: GameManager, counter: MDLabel, progress_bar: MDLinearProgressIndicator, label: str):
    root_layout = MDBoxLayout(orientation="vertical", padding=[5, 5, 5, 10])
    ui.important_labels[label] = MDLabel(text=label, halign="center", font_style="Display", role="small", width=5)
    root_layout.add_widget(ui.important_labels[label])
    root_layout.add_widget(counter)
    root_layout.add_widget(progress_bar)

    ui.lm_layout.add_widget(root_layout)

def _make_progressive_layout(ui: GameManager, debug: bool = False):
    debug_color = [0,0,0,0]
    if debug:
        debug_color = [0,0,1,1]

    root_layout = MDBoxLayout(padding=[5, 5, 5, 5], line_color=debug_color)
    ui.flower_label = MDLabel(text="0", font_style="Display", halign="center")
    ui.vacuum_label = MDLabel(text="0", font_style="Display", halign="center")
    root_layout.add_widget(_make_text_layout("Vacuum", ui.vacuum_label))
    root_layout.add_widget(_make_text_layout("Flower", ui.flower_label))
    ui.lm_layout.add_widget(root_layout)

    second_layout = MDBoxLayout(padding=[5, 5, 5, 5], line_color=debug_color)
    ui.king_boo_label = MDLabel(text="0", font_style="Display", halign="center")
    ui.balcony_boo_label = MDLabel(text="0", font_style="Display", halign="center")
    second_layout.add_widget(_make_text_layout("King Boo", ui.king_boo_label))
    second_layout.add_widget(_make_text_layout("Balcony Boo", ui.balcony_boo_label))
    ui.lm_layout.add_widget(second_layout)

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
    label = MDLabel(text=text, font_style="Display", role="large", halign="center", pos_hint={ "center_x":.5,"center_y":.5 }, width=200)

    layout.add_widget(label)
    layout.add_widget(counter)

    return layout

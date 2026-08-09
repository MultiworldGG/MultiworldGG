if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()


from kvui import (ThemedApp, ScrollBox, MainLayout, ContainerLayout, dp, Widget, MDBoxLayout, TooltipLabel, MDLabel,
                  ToggleButton, MarkupDropdown, ResizableTextField, MDLinearProgressIndicator)
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.behaviors.button import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelContent, MDExpansionPanelHeader
from kivymd.uix.list import MDListItem, MDListItemTrailingIcon, MDListItemSupportingText
from kivymd.uix.slider import MDSlider
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDButton, MDButtonIcon, MDButtonText, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivy.core.text.markup import MarkupLabel
from kivy.utils import escape_markup
from kivy.lang.builder import Builder
from kivy.properties import ObjectProperty
from textwrap import dedent
from copy import deepcopy
import Utils
import typing
import webbrowser
import re
import json
import logging
import os
import threading
from zipfile import BadZipFile, ZipFile
from urllib.parse import urlparse
import worlds
from worlds import AutoWorldRegister
from worlds.AutoWorld import World
from Options import (Option, Toggle, TextChoice, Choice, FreeText, NamedRange, Range, OptionSet, OptionList,
                     OptionCounter, Visibility)
apname = Utils.instance_name if Utils.instance_name else "Archipelago"

def validate_url(x):
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except AttributeError:
        return False


def filter_tooltip(tooltip):
    if tooltip is None:
        tooltip = "No tooltip available."
    tooltip = dedent(tooltip).strip().replace("\n", "<br>").replace("&", "&amp;") \
        .replace("[", "&bl;").replace("]", "&br;")
    tooltip = re.sub(r"\*\*(.+?)\*\*", r"[b]\g<1>[/b]", tooltip)
    tooltip = re.sub(r"\*(.+?)\*", r"[i]\g<1>[/i]", tooltip)
    return escape_markup(tooltip)


def option_can_be_randomized(option: typing.Type[Option]):
    # most options can be randomized, so we should just check for those that cannot
    if not option.supports_weighting:
        return False
    elif issubclass(option, FreeText) and not issubclass(option, TextChoice):
        return False
    return True


def check_random(value: typing.Any):
    if not isinstance(value, str):
        return value  # cannot be random if evaluated
    if value.startswith("random-"):
        return "random"
    return value


class TrailingPressedIconButton(ButtonBehavior, RotateBehavior, MDListItemTrailingIcon):
    pass


class WorldButton(ToggleButton):
    world_cls: typing.Type[World] | None = None
    world_source: worlds.WorldSource
    game_name: str


class OptionRow(MDBoxLayout):
    pass


def _world_source_game_name(source: worlds.WorldSource) -> str:
    """Read only the tiny world manifest, never the world's Python option modules."""
    try:
        if source.is_zip:
            with ZipFile(source.resolved_path, "r") as archive:
                manifests = sorted(
                    (name for name in archive.namelist() if name.lower().endswith("/archipelago.json")),
                    key=lambda name: (name.count("/"), len(name)),
                )
                if manifests:
                    return json.loads(archive.read(manifests[0])).get("game") or source.name
        else:
            manifest_path = os.path.join(source.resolved_path, "archipelago.json")
            if os.path.isfile(manifest_path):
                with open(manifest_path, encoding="utf-8") as manifest_file:
                    return json.load(manifest_file).get("game") or source.name
    except (BadZipFile, OSError, ValueError, TypeError):
        logging.debug("Could not read manifest for %s", source.resolved_path, exc_info=True)
    return source.name


class VisualRange(MDBoxLayout):
    option: typing.Type[Range]
    name: str
    tag: MDLabel = ObjectProperty(None)
    slider: MDSlider = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Range], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)

        def update_points(*update_args):
            pass

        self.slider._update_points = update_points


class VisualChoice(MDButton):
    option: typing.Type[Choice]
    name: str
    text: MDButtonText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[Choice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class VisualNamedRange(MDBoxLayout):
    option: typing.Type[NamedRange]
    name: str
    range: VisualRange = ObjectProperty(None)
    choice: MDButton = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[NamedRange], name: str, range_widget: VisualRange, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)
        self.range = range_widget
        self.add_widget(self.range)


class VisualFreeText(ResizableTextField):
    option: typing.Type[FreeText] | typing.Type[TextChoice]
    name: str

    def __init__(self, *args, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class VisualTextChoice(MDBoxLayout):
    option: typing.Type[TextChoice]
    name: str
    choice: VisualChoice = ObjectProperty(None)
    text: VisualFreeText = ObjectProperty(None)

    def __init__(self, *args, option: typing.Type[TextChoice], name: str, choice: VisualChoice,
                 text: VisualFreeText, **kwargs):
        self.option = option
        self.name = name
        super(MDBoxLayout, self).__init__(*args, **kwargs)
        self.choice = choice
        self.text = text
        self.add_widget(self.choice)
        self.add_widget(self.text)


class VisualToggle(MDBoxLayout):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[Toggle]
    name: str

    def __init__(self, *args, option: typing.Type[Toggle], name: str, **kwargs):
        self.option = option
        self.name = name
        super().__init__(*args, **kwargs)


class CounterItemValue(ResizableTextField):
    pat = re.compile('[^0-9]')

    def insert_text(self, substring, from_undo=False):
        return super().insert_text(re.sub(self.pat, "", substring), from_undo=from_undo)


class VisualListSetCounter(MDDialog):
    button: MDIconButton = ObjectProperty(None)
    option: typing.Type[OptionSet] | typing.Type[OptionList] | typing.Type[OptionCounter]
    scrollbox: ScrollBox = ObjectProperty(None)
    add: MDIconButton = ObjectProperty(None)
    save: MDButton = ObjectProperty(None)
    input: ResizableTextField = ObjectProperty(None)
    dropdown: MDDropdownMenu
    valid_keys: typing.Iterable[str]

    def __init__(self, *args, option: typing.Type[OptionSet] | typing.Type[OptionList],
                 name: str, valid_keys: typing.Iterable[str], **kwargs):
        self.option = option
        self.name = name
        self.valid_keys = valid_keys
        super().__init__(*args, **kwargs)
        self.update_width()
        self.dropdown = MarkupDropdown(caller=self.input, border_margin=dp(2),
                                       width=self.input.width, position="bottom")
        self.input.bind(text=self.on_text)
        self.input.bind(on_text_validate=self.validate_add)

    def update_width(self, *args) -> None:
        """Use the available desktop space instead of MDDialog's narrow mobile-oriented cap."""
        self.size_hint_max_x = max(dp(640), min(dp(900), Window.width - dp(96)))

    def validate_add(self, instance):
        if self.valid_keys:
            if self.input.text not in self.valid_keys:
                MDSnackbar(MDSnackbarText(text="Item must be a valid key for this option."), y=dp(24),
                           pos_hint={"center_x": 0.5}, size_hint_x=0.5).open()
                return

        if not issubclass(self.option, OptionList):
            if any(self.input.text == child.text.text for child in self.scrollbox.layout.children):
                MDSnackbar(MDSnackbarText(text="This value is already in the set."), y=dp(24),
                           pos_hint={"center_x": 0.5}, size_hint_x=0.5).open()
                return

        self.add_set_item(self.input.text)
        self.input.set_text(self.input, "")

    def remove_item(self, button: MDIconButton):
        list_item = button.parent
        self.scrollbox.layout.remove_widget(list_item)

    def add_set_item(self, key: str, value: int | None = None):
        text = MDListItemSupportingText(text=key, id="value")
        if issubclass(self.option, OptionCounter):
            value_txt = CounterItemValue(text=str(value) if value is not None else "1", size_hint_x=None, width=dp(180))
            item = MDListItem(text,
                              value_txt,
                              MDIconButton(icon="delete-outline", on_release=self.remove_item), focus_behavior=False,
                              size_hint_y=None, height=dp(56))
            item.value = value_txt
        else:
            item = MDListItem(text, MDIconButton(icon="delete-outline", on_release=self.remove_item),
                              focus_behavior=False, size_hint_y=None, height=dp(56))
        item.text = text
        self.scrollbox.layout.add_widget(item)

    def on_text(self, instance, value):
        if not self.valid_keys:
            return
        if len(value) >= 3:
            self.dropdown.items.clear()

            def on_press(txt):
                split_text = MarkupLabel(text=txt, markup=True).markup
                self.input.set_text(self.input, "".join(text_frag for text_frag in split_text
                                                        if not text_frag.startswith("[")))
                self.input.focus = True
                self.dropdown.dismiss()

            lowered = value.lower()
            for item_name in self.valid_keys:
                try:
                    index = item_name.lower().index(lowered)
                except ValueError:
                    pass  # substring not found
                else:
                    text = escape_markup(item_name)
                    text = text[:index] + "[b]" + text[index:index + len(value)] + "[/b]" + text[index + len(value):]
                    self.dropdown.items.append({
                        "text": text,
                        "on_release": lambda txt=text: on_press(txt),
                        "markup": True
                    })
            if not self.dropdown.parent:
                self.dropdown.open()
        else:
            self.dropdown.dismiss()


class OptionsCreator(ThemedApp):
    base_title: str = f"{apname} Options Creator"
    container: ContainerLayout
    main_layout: MainLayout
    scrollbox: ScrollBox
    main_panel: MainLayout
    player_options: MainLayout
    option_layout: MainLayout
    name_input: ResizableTextField
    game_label: MDLabel
    current_game: str
    options: typing.Dict[str, typing.Any]

    def __init__(self):
        self.title = self.base_title + " " + Utils.__version__
        self.icon = r"data/icon.png"
        self.current_game = ""
        self.options = {}
        self.world_buttons: list[WorldButton] = []
        self.selected_world_button: WorldButton | None = None
        super().__init__()

    @staticmethod
    def show_result_snack(text: str) -> None:
        MDSnackbar(MDSnackbarText(text=text), y=dp(24), pos_hint={"center_x": 0.5}, size_hint_x=0.5).open()

    def on_export_result(self, text: str | None) -> None:
        self.container.disabled = False
        if text is not None:
            Clock.schedule_once(lambda _: self.show_result_snack(text), 0)

    def export_options_background(self, options: dict[str, typing.Any]) -> None:
        try:
            file_name = Utils.save_filename("Export Options File As...", [("YAML", [".yaml"])],
                                            Utils.get_file_safe_name(f"{self.name_input.text}.yaml"))
        except Exception:
            self.on_export_result("Could not open dialog. Already open?")
            raise

        if not file_name:
            self.on_export_result(None)  # No file selected. No need to show a message for this.
            return

        try:
            with open(file_name, 'w') as f:
                f.write(Utils.dump(options, sort_keys=False))
                f.close()
                self.on_export_result("File saved successfully.")
        except Exception:
            self.on_export_result("Could not save file.")
            raise

    def export_options(self, button: Widget) -> None:
        if 0 < len(self.name_input.text) < 17 and self.current_game:
            import threading
            options = {
                "name": self.name_input.text,
                "description": f"YAML generated by {apname} {Utils.__version__}.",
                "game": self.current_game,
                self.current_game: {k: check_random(v) for k, v in self.options.items()}
            }
            threading.Thread(target=self.export_options_background, args=(options,), daemon=True).start()
            self.container.disabled = True
        elif not self.name_input.text:
            self.show_result_snack("Name must not be empty.")
        elif not self.current_game:
            self.show_result_snack("You must select a game to play.")
        else:
            self.show_result_snack("Name cannot be longer than 16 characters.")

    def create_range(self, option: typing.Type[Range], name: str, bind=True):
        def update_text(range_box: VisualRange):
            self.options[name] = int(range_box.slider.value)
            range_box.tag.text = str(int(range_box.slider.value))
            return

        box = VisualRange(option=option, name=name)
        if bind:
            box.slider.bind(value=lambda _, _1: update_text(box))
        self.options[name] = option.default
        return box

    def create_named_range(self, option: typing.Type[NamedRange], name: str):
        def set_to_custom(range_box: VisualNamedRange):
            range_box.range.tag.text = str(int(range_box.range.slider.value))
            if range_box.range.slider.value in option.special_range_names.values():
                value = next(key for key, val in option.special_range_names.items()
                             if val == range_box.range.slider.value)
                self.options[name] = value
                set_button_text(box.choice, value.title())
            else:
                self.options[name] = int(range_box.range.slider.value)
                set_button_text(range_box.choice, "Custom")

        def set_button_text(button: MDButton, text: str):
            button.text.text = text

        def set_value(text: str, range_box: VisualNamedRange):
            range_box.range.slider.value = min(max(option.special_range_names[text.lower()], option.range_start),
                                               option.range_end)
            range_box.range.tag.text = str(option.special_range_names[text.lower()])
            set_button_text(range_box.choice, text)
            self.options[name] = text.lower()
            range_box.range.slider.dropdown.dismiss()

        def open_dropdown(button):
            # for some reason this fixes an issue causing some to not open
            box.range.slider.dropdown.open()

        box = VisualNamedRange(option=option, name=name, range_widget=self.create_range(option, name, bind=False))
        default: int | str = option.default
        if default in option.special_range_names:
            # value can get mismatched in this case
            box.range.slider.value = min(max(option.special_range_names[default], option.range_start),
                                               option.range_end)
            box.range.tag.text = str(int(box.range.slider.value))
        elif default in option.special_range_names.values():
            # better visual
            default = next(key for key, val in option.special_range_names.items() if val == option.default)
            set_button_text(box.choice, default.title())
        box.range.slider.bind(value=lambda _, _2: set_to_custom(box))
        items = [
            {
                "text": choice.title(),
                "on_release": lambda text=choice.title(): set_value(text, box)
            }
            for choice in option.special_range_names
        ]
        box.range.slider.dropdown = MDDropdownMenu(caller=box.choice, items=items)
        box.choice.bind(on_release=open_dropdown)
        self.options[name] = default
        return box

    def create_free_text(self, option: typing.Type[FreeText] | typing.Type[TextChoice], name: str):
        text = VisualFreeText(option=option, name=name)

        def set_value(instance, value):
            self.options[name] = value

        text.bind(text=set_value)
        self.options[name] = option.default
        return text

    def create_choice(self, option: typing.Type[Choice], name: str):
        def set_button_text(button: VisualChoice, text: str):
            button.text.text = text

        def set_value(text, value):
            set_button_text(main_button, text)
            self.options[name] = value
            dropdown.dismiss()

        def open_dropdown(button):
            # for some reason this fixes an issue causing some to not open
            dropdown.open()

        default_string = isinstance(option.default, str)
        main_button = VisualChoice(option=option, name=name)
        main_button.bind(on_release=open_dropdown)

        items = [
            {
                "text": option.get_option_name(choice),
                "on_release": lambda val=choice: set_value(option.get_option_name(val), option.name_lookup[val])
            }
            for choice in option.name_lookup
        ]
        dropdown = MDDropdownMenu(caller=main_button, items=items)
        self.options[name] = option.name_lookup[option.default] if not default_string else option.default
        return main_button

    def create_text_choice(self, option: typing.Type[TextChoice], name: str):
        def set_button_text(button: MDButton, text: str):
            for child in button.children:
                if isinstance(child, MDButtonText):
                    child.text = text

        box = VisualTextChoice(option=option, name=name, choice=self.create_choice(option, name),
                               text=self.create_free_text(option, name))

        def set_value(instance):
            set_button_text(box.choice, "Custom")
            self.options[name] = instance.text

        box.text.bind(on_text_validate=set_value)
        return box

    def create_toggle(self, option: typing.Type[Toggle], name: str) -> Widget:
        def set_value(instance: MDIconButton):
            if instance.icon == "checkbox-outline":
                instance.icon = "checkbox-blank-outline"
            else:
                instance.icon = "checkbox-outline"
            self.options[name] = bool(not self.options[name])

        self.options[name] = bool(option.default)
        checkbox = VisualToggle(option=option, name=name)
        checkbox.button.bind(on_release=set_value)

        return checkbox

    def create_popup(self, option: typing.Type[OptionList] | typing.Type[OptionSet] | typing.Type[OptionCounter],
                     name: str, world: typing.Type[World]):

        valid_keys = sorted(option.valid_keys)
        if option.verify_item_name:
            valid_keys += list(world.item_name_to_id.keys())
            if option.convert_name_groups:
                valid_keys += list(world.item_name_groups.keys())
        if option.verify_location_name:
            valid_keys += list(world.location_name_to_id.keys())
            if option.convert_name_groups:
                valid_keys += list(world.location_name_groups.keys())

        if not issubclass(option, OptionCounter):
            def apply_changes(button):
                self.options[name].clear()
                for list_item in reversed(dialog.scrollbox.layout.children):
                    self.options[name].append(getattr(list_item.text, "text"))
                dialog.dismiss()
        else:
            def apply_changes(button):
                self.options[name].clear()
                for list_item in reversed(dialog.scrollbox.layout.children):
                    self.options[name][getattr(list_item.text, "text")] = int(getattr(list_item.value, "text"))
                dialog.dismiss()

        dialog = VisualListSetCounter(option=option, name=name, valid_keys=valid_keys)
        dialog.scrollbox.layout.theme_bg_color = "Custom"
        dialog.scrollbox.layout.md_bg_color = self.theme_cls.surfaceContainerLowColor
        dialog.scrollbox.layout.spacing = dp(4)
        dialog.scrollbox.layout.padding = [dp(8), dp(8), dp(8), dp(8)]

        if issubclass(option, OptionCounter):
            for value in sorted(self.options[name]):
                dialog.add_set_item(value, self.options[name].get(value, None))
        elif issubclass(option, OptionList):
            for value in self.options[name]:
                dialog.add_set_item(value)
        else:
            for value in sorted(self.options[name]):
                dialog.add_set_item(value)

        dialog.save.bind(on_release=apply_changes)
        dialog.open()

    def create_option_set_list_counter(self, option: typing.Type[OptionList] | typing.Type[OptionSet] |
                                       typing.Type[OptionCounter], name: str, world: typing.Type[World]):
        main_button = MDButton(MDButtonIcon(icon="pencil-outline"), MDButtonText(text="Edit entries"),
                               on_release=lambda x: self.create_popup(option, name, world))

        if name not in self.options:
            # convert from non-mutable to mutable
            # We use list syntax even for sets, set behavior is enforced through GUI
            if issubclass(option, OptionCounter):
                self.options[name] = deepcopy(option.default)
            elif issubclass(option, OptionList):
                self.options[name] = list(option.default)
            else:
                self.options[name] = sorted(option.default)

        return main_button

    def create_option(self, option: typing.Type[Option], name: str, world: typing.Type[World]) -> Widget:
        option_base = OptionRow(orientation="horizontal", size_hint_y=None, height=dp(72),
                                padding=[dp(16), dp(8), dp(12), dp(8)], spacing=dp(16),
                                theme_bg_color="Custom", md_bg_color=self.theme_cls.surfaceContainerLowColor,
                                radius=[dp(12), dp(12), dp(12), dp(12)])

        tooltip = filter_tooltip(option.__doc__)
        option_label = TooltipLabel(text=f"[ref=0|{tooltip}]{getattr(option, 'display_name', name)}",
                                    halign="left", valign="middle")
        option_label.bind(size=lambda label, size: setattr(label, "text_size", (size[0], None)))
        label_box = MDBoxLayout(orientation="horizontal", size_hint_x=0.48, spacing=dp(8))
        label_anchor = MDAnchorLayout(anchor_x="left", anchor_y="center")
        label_anchor.add_widget(option_label)
        label_box.add_widget(label_anchor)

        option_base.add_widget(label_box)
        control_box = MDAnchorLayout(anchor_x="right", anchor_y="center", size_hint_x=0.52)
        if issubclass(option, NamedRange):
            option_control = self.create_named_range(option, name)
        elif issubclass(option, Range):
            option_control = self.create_range(option, name)
        elif issubclass(option, Toggle):
            option_control = self.create_toggle(option, name)
        elif issubclass(option, TextChoice):
            option_control = self.create_text_choice(option, name)
        elif issubclass(option, Choice):
            option_control = self.create_choice(option, name)
        elif issubclass(option, FreeText):
            option_control = self.create_free_text(option, name)
        elif any(issubclass(option, cls) for cls in (OptionSet, OptionList, OptionCounter)):
            option_control = self.create_option_set_list_counter(option, name, world)
        else:
            option_control = MDLabel(text="Unsupported here; edit the exported YAML manually.",
                                     halign="right", valign="middle")
        control_box.add_widget(option_control)
        option_base.add_widget(control_box)

        if option_can_be_randomized(option):
            def randomize_option(instance: Widget, value: str):
                value = value == "down"
                if value:
                    self.options[name] = "random-" + str(self.options[name])
                else:
                    self.options[name] = self.options[name].replace("random-", "")
                    if self.options[name].isnumeric():
                        self.options[name] = int(self.options[name])
                    elif self.options[name] in ("True", "False"):
                        self.options[name] = self.options[name] == "True"

                option_control.disabled = value

            default_random = option.default == "random"
            random_toggle = ToggleButton(MDButtonText(text="Random"), size_hint_x=None, width=dp(96),
                                         theme_width="Custom", size_hint_y=None, height=dp(40), theme_height="Custom",
                                         state="down" if default_random else "normal")
            random_toggle.bind(state=randomize_option)
            label_box.add_widget(random_toggle)
            if default_random:
                randomize_option(random_toggle, "down")

        return option_base

    def create_options_panel(self, world_button: WorldButton):
        self.option_layout.clear_widgets()
        self.options.clear()
        cls = world_button.world_cls
        assert cls is not None

        self.current_game = cls.game
        if not cls.web.options_page:
            self.current_game = ""
            self.game_label.text = "Game: None"
            self.show_panel_status("Options unavailable",
                                   f"{cls.game} does not provide an Options Creator page.")
            return
        elif isinstance(cls.web.options_page, str):
            self.current_game = ""
            if validate_url(cls.web.options_page):
                webbrowser.open(cls.web.options_page)
                MDSnackbar(MDSnackbarText(text="Launching in default browser..."), y=dp(24), pos_hint={"center_x": 0.5},
                           size_hint_x=0.5).open()
                world_button.state = "normal"
            else:
                # attach onto archipelago.gg and see if we pass
                new_url = "https://multiworld.gg/" + cls.web.options_page
                if validate_url(new_url):
                    webbrowser.open(new_url)
                    MDSnackbar(MDSnackbarText(text="Launching in default browser..."), y=dp(24),
                               pos_hint={"center_x": 0.5},
                               size_hint_x=0.5).open()
                else:
                    MDSnackbar(MDSnackbarText(text="Invalid options page, please report to world developer."), y=dp(24),
                               pos_hint={"center_x": 0.5},
                               size_hint_x=0.5).open()
                world_button.state = "normal"
                # else just fall through
        else:
            expansion_box = ScrollBox()
            expansion_box.layout.orientation = "vertical"
            expansion_box.layout.spacing = dp(10)
            expansion_box.layout.padding = [dp(16), dp(8), dp(16), dp(24)]
            expansion_box.scroll_type = ["bars", "content"]
            expansion_box.do_scroll_x = False
            group_names = ["Game Options", *(group.name for group in cls.web.option_groups)]
            groups = {name: [] for name in group_names}
            for name, option in cls.options_dataclass.type_hints.items():
                group = next((group.name for group in cls.web.option_groups if option in group.options), "Game Options")
                groups[group].append((name, option))

            for group, options in groups.items():
                options = [(name, option) for name, option in options
                           if name and option.visibility & Visibility.simple_ui]
                if not options:
                    continue  # Game Options can be empty if every other option is in another group
                    # Can also have an option group of options that should not render on simple ui
                group_item = MDExpansionPanel(size_hint_y=None)
                group_header = MDExpansionPanelHeader(MDListItem(MDListItemSupportingText(text=group),
                                                                 TrailingPressedIconButton(icon="chevron-right",
                                                                                           on_release=lambda x,
                                                                                           item=group_item:
                                                                                           self.tap_expansion_chevron(
                                                                                               item, x)),
                                                                 md_bg_color=self.theme_cls.surfaceContainerLowestColor,
                                                                 theme_bg_color="Custom",
                                                                 on_release=lambda x, item=group_item:
                                                                 self.tap_expansion_chevron(item, x)))
                group_content = MDExpansionPanelContent(orientation="vertical", theme_bg_color="Custom",
                                                        md_bg_color=self.theme_cls.surfaceContainerLowestColor,
                                                        # KivyMD removes 88dp from the measured content height to
                                                        # reserve its header. Preserve that space plus our 12dp gap.
                                                        padding=[dp(12), dp(88), dp(12), dp(12)],
                                                        spacing=dp(8))
                group_item.add_widget(group_header)
                group_item.add_widget(group_content)
                group_box = ScrollBox()
                group_box.layout.orientation = "vertical"
                group_box.layout.spacing = dp(3)
                for name, option in options:
                    group_content.add_widget(self.create_option(option, name, cls))
                expansion_box.layout.add_widget(group_item)
            self.option_layout.add_widget(expansion_box)
        self.game_label.text = f"Game: {self.current_game or 'None'}"

    @staticmethod
    def tap_expansion_chevron(panel: MDExpansionPanel, chevron: TrailingPressedIconButton | MDListItem):
        if isinstance(chevron, MDListItem):
            chevron = next((child for child in chevron.ids.trailing_container.children
                            if isinstance(child, TrailingPressedIconButton)), None)
        panel.open() if not panel.is_open else panel.close()
        if chevron:
            panel.set_chevron_down(
                chevron
            ) if not panel.is_open else panel.set_chevron_up(chevron)

    def show_panel_status(self, headline: str, detail: str = "", loading: bool = False) -> None:
        self.option_layout.clear_widgets()
        status = MDBoxLayout(orientation="vertical", padding=[dp(72), dp(80), dp(72), dp(40)], spacing=dp(16))
        status.add_widget(Widget())
        status.add_widget(MDLabel(text=headline, halign="center", adaptive_height=True,
                                  font_style="Headline", role="small"))
        if detail:
            status.add_widget(MDLabel(text=detail, halign="center", adaptive_height=True,
                                      theme_text_color="Secondary"))
        if loading:
            status.add_widget(MDLinearProgressIndicator(type="indeterminate", size_hint=(0.7, None), height=dp(4),
                                                        pos_hint={"center_x": 0.5}))
        status.add_widget(Widget())
        self.option_layout.add_widget(status)

    def filter_worlds(self, query: str) -> None:
        query = query.strip().casefold()
        self.scrollbox.layout.clear_widgets()
        for button in self.world_buttons:
            if not query or query in button.game_name.casefold():
                self.scrollbox.layout.add_widget(button)

    def _finish_world_load(self, world_button: WorldButton, world_cls: typing.Type[World] | None,
                           error: str | None) -> None:
        self.scrollbox.disabled = False
        if error or world_cls is None:
            world_button.state = "normal"
            if self.selected_world_button is world_button:
                self.selected_world_button = None
            self.current_game = ""
            self.game_label.text = "Game: None"
            self.show_panel_status("Could not load this game", error or "The world did not register a playable game.")
            return

        world_button.world_cls = world_cls
        world_button.game_name = world_cls.game
        for child in world_button.children:
            if isinstance(child, MDButtonText):
                child.text = world_cls.game
        self.create_options_panel(world_button)

    def _load_world_background(self, world_button: WorldButton) -> None:
        source = world_button.world_source
        try:
            if source.is_zip:
                # This performs compatibility and manifest checks, but imports only this apworld.
                worlds._load_apworlds([source])
            else:
                worlds._set_current_loading_world(source.name)
                if not source.load():
                    raise RuntimeError(f"The {world_button.game_name} world failed while importing.")

            world_cls = AutoWorldRegister.world_types.get(world_button.game_name)
            if world_cls is None:
                module_prefix = f"worlds.{source.name}"
                candidates = [
                    cls for cls in AutoWorldRegister.world_types.values()
                    if cls.__module__ == module_prefix or cls.__module__.startswith(module_prefix + ".")
                ]
                world_cls = next((cls for cls in candidates if not cls.hidden), None)
            if world_cls is None or world_cls.hidden:
                raise RuntimeError(f"{world_button.game_name} does not expose options in the Options Creator.")
        except Exception as exc:
            logging.exception("Could not lazy-load world %s", source.name)
            Clock.schedule_once(lambda _dt, message=str(exc): self._finish_world_load(world_button, None, message), 0)
        else:
            Clock.schedule_once(lambda _dt: self._finish_world_load(world_button, world_cls, None), 0)
        finally:
            worlds._set_current_loading_world(None)

    def select_world(self, world_button: WorldButton) -> None:
        if self.selected_world_button is not None and self.selected_world_button is not world_button:
            self.selected_world_button.state = "normal"
        self.selected_world_button = world_button
        world_button.state = "down"

        if world_button.world_cls is not None:
            self.create_options_panel(world_button)
            return

        self.current_game = ""
        self.options.clear()
        self.game_label.text = f"Loading: {world_button.game_name}"
        self.show_panel_status(f"Loading {world_button.game_name}", "Preparing this game's options…", loading=True)
        self.scrollbox.disabled = True
        threading.Thread(target=self._load_world_background, args=(world_button,),
                         name=f"OptionsCreator-{world_button.world_source.name}", daemon=True).start()

    def build(self):
        self.set_colors()
        Window.minimum_width = 900
        Window.minimum_height = 650
        Window.size = (1100, 920)
        self.options = {}
        self.container = Builder.load_file(Utils.local_path("data/optionscreator.kv"))
        self.root = self.container
        self.main_layout = self.container.ids.main
        self.scrollbox = self.container.ids.scrollbox
        self.main_panel = self.container.ids.player_layout
        self.player_options = self.container.ids.player_options
        self.game_label = self.container.ids.game
        self.name_input = self.container.ids.player_name
        self.option_layout = self.container.ids.options

        # Manifests are tiny JSON files. Reading them gives us the catalog without importing
        # hundreds of Python option modules; the selected module is imported on demand.
        catalog: dict[str, tuple[str, worlds.WorldSource]] = {}
        hidden_source_names = {"debug", "generic", "tracker"}
        for source in worlds.world_sources:
            if source.name in hidden_source_names:
                continue
            game_name = _world_source_game_name(source)
            key = game_name.casefold()
            existing = catalog.get(key)
            if existing is None or (existing[1].is_zip and not source.is_zip):
                catalog[key] = (game_name, source)

        for game_name, source in sorted(catalog.values(), key=lambda entry: entry[0].casefold()):
            world_text = MDButtonText(text=game_name, halign="left", valign="middle",
                                      pos_hint={"center_y": 0.5})
            world_text.text_size = (world_text.width, None)
            world_text.bind(width=lambda *x, text=world_text: text.setter('text_size')(text, (text.width, None)),
                            texture_size=lambda *x, text=world_text: text.setter("height")(text,
                                                                                           world_text.texture_size[1]))
            world_button = WorldButton(world_text, size_hint_x=1, size_hint_y=None, height=dp(48),
                                       theme_width="Custom", theme_height="Custom",
                                       radius=(dp(10), dp(10), dp(10), dp(10)))
            world_button.bind(on_release=self.select_world)
            world_button.world_source = source
            world_button.game_name = game_name
            self.world_buttons.append(world_button)

        self.filter_worlds("")
        self.container.ids.world_search.bind(text=lambda _field, value: self.filter_worlds(value))
        self.show_panel_status("Choose a game", "Its options will load only when you select it.")

        def set_height(instance, value):
            instance.height = value[1]

        self.game_label.bind(texture_size=set_height)

        # Uncomment to re-enable the Kivy console/live editor
        # Ctrl-E to enable it, make sure numlock/capslock is disabled
        # from kivy.modules.console import create_console
        # from kivy.core.window import Window
        # create_console(Window, self.container)

        return self.container


def launch():
    OptionsCreator().run()


if __name__ == "__main__":
    Utils.init_logging("OptionsCreator")
    launch()

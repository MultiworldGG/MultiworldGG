"""
MultiworldGG Launcher for bundled app.

* If run with a patch file as argument, launch corresponding client with the patch file as an argument.
* If run with component name as argument, run it passing argv[2:] as arguments.
* If run without arguments or unknown arguments, open launcher GUI.

Additional components can be added to worlds.LauncherComponents.components.
"""

import argparse
import importlib
import logging
import re
import logging.handlers
import multiprocessing
import os
import shlex
import subprocess
import sys
import threading
import urllib.parse
import webbrowser
from collections.abc import Callable, Sequence
from os.path import isfile
from shutil import which
from typing import Any

if __name__ == "__main__":
    import ModuleUpdate

    ModuleUpdate.update()

import settings
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from Utils import (env_cleared_lib_path, init_logging, is_frozen, is_linux, is_macos, is_windows, local_path,
                   messagebox, open_filename, user_path)
from Updater import get_latest_release_info, download_and_install_win

if __name__ == "__main__":
    init_logging('Launcher')

from worlds.LauncherComponents import Component, components, has_world_components, icon_paths, resolve_icon_path, SuffixIdentifier, Type
from worlds import failed_world_loads

apname = "Archipelago" if not Utils.instance_name else Utils.instance_name

def open_host_yaml():
    s = settings.get_settings()
    file = s.filename
    s.save()
    assert file, "host.yaml missing"
    if is_linux:
        exe = which('sensible-editor') or which('gedit') or \
              which('xdg-open') or which('gnome-open') or which('kde-open')
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(file)
        return

    env = env_cleared_lib_path()
    subprocess.Popen([exe, file], env=env)

def open_patch():
    suffixes = []
    for c in components:
        if c.type == Type.CLIENT and \
                isinstance(c.file_identifier, SuffixIdentifier) and \
                (c.script_name is None or isfile(get_exe(c)[-1])):
            suffixes += c.file_identifier.suffixes
    try:
        filename = open_filename("Select patch", (("Patches", suffixes),))
    except Exception as e:
        messagebox("Error", str(e), error=True)
    else:
        file, component = identify(filename)
        if file and component:
            exe = get_exe(component)
            if exe is None or not isfile(exe[-1]):
                exe = get_exe("Launcher")

            try:
                from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
                from kivy.metrics import dp
                MDSnackbar(
                    MDSnackbarText(text="Patching file now..."),
                    y=dp(24),
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.5,
                ).open()
            except ImportError:
                pass

            launch([*exe, file], component.cli)


def generate_yamls(*args):
    from Options import generate_yaml_templates

    parser = argparse.ArgumentParser(description="Generate Template Options", usage="[-h] [--skip_open_folder]")
    parser.add_argument("--skip_open_folder", action="store_true")
    args = parser.parse_args(args)

    target = Utils.user_path("Players", "Templates")
    generate_yaml_templates(target, False)
    if not args.skip_open_folder:
        open_folder(target)


def browse_files():
    open_folder(user_path())


def open_folder(folder_path):
    if is_linux:
        exe = which('xdg-open') or which('gnome-open') or which('kde-open')
    elif is_macos:
        exe = which("open")
    else:
        webbrowser.open(folder_path)
        return

    if exe:
        env = env_cleared_lib_path()
        subprocess.Popen([exe, folder_path], env=env)
    else:
        logging.warning(f"No file browser available to open {folder_path}")


def update_settings(skip_cache: bool = False):
    from settings import get_settings
    get_settings().save(write_launcher_cache=not skip_cache)


def precache_world_data() -> None:
    """Build launcher cache (called post-install to warm cache)."""
    import worlds
    worlds.ensure_worlds_loaded()
    worlds.rebuild_world_caches()



def ensure_launcher_components_available() -> None:
    if has_world_components():
        return

    import worlds
    worlds.ensure_worlds_loaded()


components.extend([
    # Functions
    Component("Open host.yaml", func=open_host_yaml,
                description="Open the host.yaml file to change settings for generation, games, and more."),
    Component("Open Patch", func=open_patch,
              description="Open a patch file, downloaded from the room page or provided by the host."),
    Component("Generate Template Options", func=generate_yamls,
              description="Generate template YAMLs for currently installed games."),
    Component("MultiworldGG Website", func=lambda: webbrowser.open("https://multiworld.gg/"),
              description="Open multiworld.gg in your browser."),
    Component("Unofficial AP Discord", icon="discord", func=lambda: webbrowser.open("https://discord.multiworld.gg"),
              description="Join the Discord server to play public multiworlds, report issues, or just chat!"),
    Component("Browse Files", func=browse_files,
              description="Open the MultiworldGG installation folder in your file browser."),
])


def handle_uri(path: str) -> tuple[list[Component], Component]:
    url = urllib.parse.urlparse(path)
    queries = urllib.parse.parse_qs(url.query)
    client_components = []
    text_client_component = None
    game = queries["game"][0]
    for component in components:
        if component.supports_uri and game in component.game_name:
            client_components.append(component)
        elif component.display_name == "Text Client":
            text_client_component = component
    return client_components, text_client_component


def build_uri_popup(component_list: list[Component], launch_args: tuple[str, ...]) -> None:
    from kvui import ButtonsPrompt
    component_options = {
        component.display_name: component for component in component_list
    }
    popup = ButtonsPrompt("Connect to Multiworld",
                          "Select client to open and connect with.",
                          lambda component_name: run_component(component_options[component_name], *launch_args),
                          *component_options.keys())
    popup.open()


def identify(path: None | str) -> tuple[None | str, None | Component]:
    if path is None:
        return None, None
    for component in components:
        if component.handles_file(path):
            return path, component
        elif path == component.display_name or path == component.script_name:
            return None, component
    return None, None


def get_exe(component: str | Component) -> Sequence[str] | None:
    if isinstance(component, str):
        name = component
        component = None
        if name.startswith(apname):
            name = name[len(apname):]
        if name.endswith(".exe"):
            name = name[:-4]
        if name.endswith(".py"):
            name = name[:-3]
        if not name:
            return None
        for c in components:
            if c.script_name == name or c.frozen_name == apname + name:
                component = c
                break
        if not component:
            return None
    if is_frozen():
        suffix = ".exe" if is_windows else ""
        return [local_path(f"{component.frozen_name}{suffix}")] if component.frozen_name else None
    else:
        return [sys.executable, local_path(f"{component.script_name}.py")] if component.script_name else None


def _resolve_component_callable(module_name: str, qualname: str):
    if module_name.startswith("worlds."):
        import worlds
        worlds.ensure_worlds_loaded()
    module = importlib.import_module(module_name)
    target = module
    for part in qualname.split("."):
        if part == "<locals>":
            raise AttributeError(f"Unable to resolve nested local callable: {module_name}.{qualname}")
        target = getattr(target, part)
    if not callable(target):
        raise TypeError(f"Resolved target is not callable: {module_name}.{qualname}")
    return target


def run_component_callable(module_name: str, qualname: str, *args: str) -> None:
    target = _resolve_component_callable(module_name, qualname)
    # Reset sys.argv so client launch functions that call parse_args() without
    # explicit args don't see the --run_component_callable launcher flags.
    sys.argv = [sys.argv[0], *args]
    target(*args)


def launch_component_callable(module_name: str, qualname: str, launch_args: Sequence[str] = ()) -> subprocess.Popen[Any] | None:
    launcher_exe = get_exe("Launcher")
    if not launcher_exe:
        return None
    return subprocess.Popen([*launcher_exe, "--run_component_callable", module_name, qualname, "--", *launch_args])


def launch(exe: Sequence[str], in_terminal: bool = False) -> bool:
    """Runs the given command/args in `exe` in a new process.

    If `in_terminal` is True, it will attempt to run in a terminal window,
    and the return value will indicate whether one was found."""
    if in_terminal:
        if is_windows:
            # intentionally using a window title with a space so it gets quoted and treated as a title
            subprocess.Popen(["start", f"Running {apname}", *exe], shell=True)
            return True
        elif is_linux:
            # Attempt to use xdg-terminal-exec first to allow user-defined defaults
            xdg = which('xdg-terminal-exec')
            if xdg:
                subprocess.Popen([xdg, '--', *exe])
                return True
            terminal = which('x-terminal-emulator') or which("konsole") or which('gnome-terminal') or which('xterm')
            if terminal:
                # Clear LD_LIB_PATH during terminal startup, but set it again when running command in case it's needed
                ld_lib_path = os.environ.get("LD_LIBRARY_PATH")
                lib_path_setter = f"env LD_LIBRARY_PATH={shlex.quote(ld_lib_path)} " if ld_lib_path else ""
                env = env_cleared_lib_path()

                subprocess.Popen([terminal, "-e", lib_path_setter + shlex.join(exe)], env=env)
                return True
        elif is_macos:
            terminal = [which("open"), "-W", "-a", "Terminal.app"]
            subprocess.Popen([*terminal, *exe])
            return True
    subprocess.Popen(exe)
    return False


def create_shortcut(button: Any, component: Component) -> None:
    from pyshortcuts import make_shortcut
    env = os.environ
    if "APPIMAGE" in env:
        script = env["ARGV0"]
        wkdir = None # defaults to ~ on Linux
    else:
        script = sys.argv[0]
        wkdir = Utils.local_path()

    script = f"{script} \"{component.display_name}\""
    make_shortcut(script, name=f"MultiworldGG {component.display_name}", icon=local_path("data", "icon.ico"),
                  startmenu=False, terminal=False, working_dir=wkdir, noexe=Utils.is_frozen())
    button.menu.dismiss()


refresh_components: Callable[[], None] | None = None


def run_gui(launch_components: list[Component], args: Any) -> None:
    from kvui import (ThemedApp, MDFloatLayout, MDGridLayout, ScrollBox)
    from kivy.properties import ObjectProperty
    from kivy.core.window import Window
    from kivy.metrics import dp
    from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
    from kivymd.uix.card import MDCard
    from kivymd.uix.menu import MDDropdownMenu
    from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
    from kivymd.uix.textfield import MDTextField
    from kivy.clock import Clock
    from kivy.uix.widget import Widget
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.progressbar import ProgressBar
    from kivy.uix.scrollview import ScrollView
    from kivy.uix.label import Label
    from kivy.uix.popup import Popup
    from kivy.graphics import Color, Rectangle
    from kivy.app import App
    from kivy.lang.builder import Builder

    class LauncherCard(MDCard):
        component: Component | None
        image: str
        context_button: MDIconButton = ObjectProperty(None)

        def __init__(self, *args, component: Component | None = None, image_path: str = "", **kwargs):
            self.component = component
            self.image = image_path
            super().__init__(args, kwargs)

    class Launcher(ThemedApp):
        base_title: str = apname + " Launcher"
        top_screen: MDFloatLayout = ObjectProperty(None)
        navigation: MDGridLayout = ObjectProperty(None)
        grid: MDGridLayout = ObjectProperty(None)
        button_layout: ScrollBox = ObjectProperty(None)
        search_box: MDTextField = ObjectProperty(None)
        cards: list[LauncherCard]
        current_filter: Sequence[str | Type] | None
        failed_worlds: bool = bool(failed_world_loads)

        def __init__(self, ctx=None, components=None, args=None):
            self.title = self.base_title + " " + Utils.__version__
            self.ctx = ctx
            self.icon = r"data/icon.png"
            self.favorites = []
            self.launch_components = components
            self.launch_args = args
            self.cards = []
            self.current_filter = (Type.CLIENT, Type.TOOL, Type.ADJUSTER, Type.MISC)
            self._loading_overlay = None
            self._loading_overlay_label = None
            self._loading_overlay_subtitle_label = None
            self._loading_world_poll_event = None
            self._cache_refresh_started = False
            persistent = Utils.persistent_load()
            if "launcher" in persistent:
                if "favorites" in persistent["launcher"]:
                    self.favorites.extend(persistent["launcher"]["favorites"])
                if "filter" in persistent["launcher"]:
                    if persistent["launcher"]["filter"]:
                        filters = []
                        for filter in persistent["launcher"]["filter"].split(", "):
                            if filter == "favorites":
                                filters.append(filter)
                            else:
                                filters.append(Type[filter])
                        self.current_filter = filters
            super().__init__()

        def set_favorite(self, caller):
            if caller.component.display_name in self.favorites:
                self.favorites.remove(caller.component.display_name)
                caller.icon = "star-outline"
            else:
                self.favorites.append(caller.component.display_name)
                caller.icon = "star"

        def build_card(self, component: Component) -> LauncherCard:
            """
                Builds a card widget for a given component.

                :param component: The component associated with the button.

                :return: The created Card Widget.
                """
            image_path = resolve_icon_path(icon_paths.get(component.icon, local_path("data", "icon.png")))
            button_card = LauncherCard(component=component,
                                       image_path=image_path)

            def open_menu(caller):
                caller.menu.open()

            menu_items = [
                {
                    "text": "Add shortcut on desktop",
                    "leading_icon": "laptop",
                    "on_release": lambda: create_shortcut(button_card.context_button, component)
                }
            ]
            button_card.context_button.menu = MDDropdownMenu(caller=button_card.context_button, items=menu_items)
            button_card.context_button.bind(on_release=open_menu)

            return button_card

        def _rebuild_cards_from_components(self) -> None:
            self.cards.clear()
            for component in components:
                self.cards.append(self.build_card(component))

            if self.search_box and self.search_box.text:
                self.filter_clients_by_name(self.search_box, self.search_box.text)
            else:
                self._refresh_components(self.current_filter)


        def _set_loading_overlay_text(self, text: str | None = None, subtitle: str | None = None) -> None:
            if text is not None and self._loading_overlay_label is not None:
                self._loading_overlay_label.text = text
            if subtitle is not None and self._loading_overlay_subtitle_label is not None:
                self._loading_overlay_subtitle_label.text = subtitle

        def _show_loading_overlay(self, text: str = "Validating APWorld info...") -> None:
            if self._loading_overlay is not None:
                self._set_loading_overlay_text(text=text)
                return
            overlay = BoxLayout(
                orientation="vertical",
                pos_hint={"center_x": 0.625, "center_y": 0.5},
                size_hint=(0.52, None),
                height=dp(118),
                padding=(dp(16), dp(14)),
                spacing=dp(4),
            )
            with overlay.canvas.before:
                Color(0.12, 0.12, 0.12, 0.82)
                rect = Rectangle(pos=overlay.pos, size=overlay.size)
            overlay.bind(pos=lambda inst, val: setattr(rect, "pos", val))
            overlay.bind(size=lambda inst, val: setattr(rect, "size", val))
            label = Label(
                text=text,
                halign="center",
                valign="bottom",
                font_size="18sp",
                color=(0.95, 0.95, 0.95, 1.0),
                size_hint_y=None,
                height=dp(36),
            )
            label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
            subtitle_label = Label(
                text="",
                halign="center",
                valign="top",
                font_size="13sp",
                color=(0.78, 0.78, 0.78, 1.0),
                shorten=True,
                shorten_from="center",
                size_hint_y=None,
                height=dp(26),
            )
            subtitle_label.bind(size=lambda inst, val: setattr(inst, "text_size", val))
            overlay.add_widget(Widget())
            overlay.add_widget(label)
            overlay.add_widget(subtitle_label)
            overlay.add_widget(Widget())
            self.top_screen.add_widget(overlay)
            self._loading_overlay = overlay
            self._loading_overlay_label = label
            self._loading_overlay_subtitle_label = subtitle_label

        def _start_loading_world_poll(self) -> None:
            if self._loading_world_poll_event is not None:
                return

            def _poll_loading_world(dt: float) -> None:
                import worlds
                world_name = getattr(worlds, "_current_loading_world", None)
                subtitle = f"Parsing {world_name}" if world_name else ""
                self._set_loading_overlay_text(subtitle=subtitle)

            self._loading_world_poll_event = Clock.schedule_interval(_poll_loading_world, 0.1)
            _poll_loading_world(0)

        def _dismiss_loading_overlay(self) -> None:
            if self._loading_world_poll_event is not None:
                self._loading_world_poll_event.cancel()
                self._loading_world_poll_event = None
            if self._loading_overlay is not None:
                self.top_screen.remove_widget(self._loading_overlay)
                self._loading_overlay = None
                self._loading_overlay_label = None
                self._loading_overlay_subtitle_label = None

        def _background_refresh_worker(self) -> None:
            import worlds
            import os
            import shutil

            # If frozen, check for cache in install dir and copy to user dir
            if is_frozen():
                from worlds.LauncherComponents import _LAUNCHER_CACHE_PATH
                install_cache = local_path("data", "world_launcher_cache.json.gz")
                if not os.path.isfile(_LAUNCHER_CACHE_PATH) and os.path.isfile(install_cache):
                    try:
                        os.makedirs(os.path.dirname(_LAUNCHER_CACHE_PATH), exist_ok=True)
                        shutil.copy2(install_cache, _LAUNCHER_CACHE_PATH)
                    except Exception as exc:
                        logging.warning(f"Failed to copy cache from install dir: {exc}")

            cache_exists = worlds.has_launcher_cache()

            if not cache_exists:
                # Load worlds in the worker thread so launcher UI stays responsive.
                load_ok = False
                try:
                    worlds.ensure_worlds_loaded()
                    load_ok = True
                except Exception as exc:
                    logging.warning("World loading failed: %s", exc)
                finally:
                    def _finish_on_main(dt):
                        if load_ok:
                            self._rebuild_cards_from_components()
                        self._dismiss_loading_overlay()

                    Clock.schedule_once(_finish_on_main, 0)
            else:
                # Valid Cache
                def _finish_from_cache(dt):
                    from worlds.LauncherComponents import _hydrate_launcher_components_from_cache
                    _hydrate_launcher_components_from_cache()
                    self._rebuild_cards_from_components()
                    self._dismiss_loading_overlay()
                Clock.schedule_once(_finish_from_cache, 0)

        def _start_background_cache_refresh(self) -> None:
            if self._cache_refresh_started:
                return

            self._cache_refresh_started = True
            threading.Thread(
                target=self._background_refresh_worker,
                name="LauncherCacheRefresh",
                daemon=True,
            ).start()

        def _refresh_components(self, type_filter: Sequence[str | Type] | None = None) -> None:
            if not type_filter:
                type_filter = [Type.CLIENT, Type.ADJUSTER, Type.TOOL, Type.MISC]
            favorites = "favorites" in type_filter

            # clear before repopulating
            assert self.button_layout, "must call `build` first"
            tool_children = reversed(self.button_layout.layout.children)
            for child in tool_children:
                self.button_layout.layout.remove_widget(child)

            cards = [card for card in self.cards if card.component.type in type_filter
                     or favorites and card.component.display_name in self.favorites]

            self.current_filter = type_filter

            for card in cards:
                self.button_layout.layout.add_widget(card)

            top = self.button_layout.children[0].y + self.button_layout.children[0].height \
                           - self.button_layout.height
            scroll_percent = self.button_layout.convert_distance_to_scroll(0, top)
            self.button_layout.scroll_y = max(0, min(1, scroll_percent[1]))

        def filter_clients_by_type(self, caller: MDButton):
            self._refresh_components(caller.type)
            self.search_box.text = ""

        def filter_clients_by_name(self, caller: MDTextField, name: str) -> None:
            if len(name) == 0:
                self._refresh_components(self.current_filter)
                return

            sub_matches = [
                card for card in self.cards
                if name.lower() in card.component.display_name.lower() and card.component.type != Type.HIDDEN
            ]
            self.button_layout.layout.clear_widgets()
            for card in sub_matches:
                self.button_layout.layout.add_widget(card)

        def build(self):
            self.top_screen = Builder.load_file(Utils.local_path("data/launcher.kv"))
            self.grid = self.top_screen.ids.grid
            self.navigation = self.top_screen.ids.navigation
            self.button_layout = self.top_screen.ids.button_layout
            self.search_box = self.top_screen.ids.search_box
            self.set_colors()
            self.top_screen.md_bg_color = self.theme_cls.backgroundColor

            global refresh_components
            refresh_components = self._refresh_components
            from worlds import LauncherComponents as _lc
            _lc._rebuild_launcher_ui = self._rebuild_cards_from_components
            Window.size = (1100, 920)
            Window.bind(on_drop_file=self._on_drop_file)
            Window.bind(on_keyboard=self._on_keyboard)

            self._rebuild_cards_from_components()

            # Uncomment to re-enable the Kivy console/live editor
            # Ctrl-E to enable it, make sure numlock/capslock is disabled
            # from kivy.modules.console import create_console
            # create_console(Window, self.top_screen)

            return self.top_screen

        def on_start(self):
            self._show_loading_overlay("Validating APWorld info...")
            self._start_loading_world_poll()

            if self.launch_components:
                build_uri_popup(self.launch_components, self.launch_args)
                self.launch_components = None
                self.launch_args = None

            if is_frozen() and is_windows:
                # Check for updates first, then start cache refresh after user responds
                Clock.schedule_once(self._maybe_show_update_dialog, 0.2)
            else:
                # No update check, start cache refresh immediately
                Clock.schedule_once(lambda dt: self._start_background_cache_refresh(), 0.2)

        def _maybe_show_update_dialog(self, dt):
            try:
                latest_ver, download_url, changelog = get_latest_release_info()
            except Exception as e:
                logging.warning("Launcher update check failed: %s", e)
                # Update check failed, proceed with cache refresh
                self._start_background_cache_refresh()
                return

            if latest_ver > Utils.version_tuple:

                def _md_to_kivy(text: str) -> str:
                    def inline(s: str) -> str:
                        s = re.sub(r"\[([^\]]*)\]\([^\)]*\)", r"\1", s)  # [text](url) → text
                        s = s.replace("[", r"\[")                          # escape literal [
                        s = re.sub(r"\*\*(.+?)\*\*", r"[b]\1[/b]", s)   # **bold**
                        s = re.sub(r"__(.+?)__",      r"[b]\1[/b]", s)   # __bold__
                        s = re.sub(r"\*(.+?)\*",      r"[i]\1[/i]", s)   # *italic*
                        s = re.sub(r"`(.+?)`", r"[color=#79b8ff]\1[/color]", s)  # `code`
                        return s
                    out = []
                    for line in text.split("\n"):
                        s = line.strip()
                        if s.startswith("## "):
                            out.append(f"[b][color=#aaddff]{inline(s[3:])}[/color][/b]")
                        elif s.startswith("### "):
                            out.append(f"[b]{inline(s[4:])}[/b]")
                        elif s.startswith("# "):
                            out.append(f"[b][color=#ffffff]{inline(s[2:])}[/color][/b]")
                        elif re.match(r"^[-*+] ", s):
                            out.append(f"  \u2022 {inline(s[2:])}")
                        elif re.match(r"^---+$|^\*\*\*+$", s):
                            out.append("\u2500" * 40)
                        else:
                            out.append(inline(line))
                    return "\n".join(out)

                # --- Right column: terminal-style changelog box ---
                changelog_label = Label(
                    text=_md_to_kivy(changelog),
                    size_hint_y=None,
                    halign="left",
                    valign="top",
                    markup=True,
                    font_size="12sp",
                    color=(0.85, 0.85, 0.85, 1),
                    padding=(8, 8),
                )
                changelog_label.bind(
                    width=lambda inst, val: setattr(inst, "text_size", (val, None))
                )
                changelog_label.bind(
                    texture_size=lambda inst, val: setattr(inst, "height", val[1])
                )

                changelog_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=False)
                changelog_scroll.add_widget(changelog_label)

                with changelog_scroll.canvas.before:
                    Color(0.08, 0.08, 0.08, 1)
                    bg_rect = Rectangle(pos=changelog_scroll.pos, size=changelog_scroll.size)
                changelog_scroll.bind(
                    pos=lambda inst, val: setattr(bg_rect, "pos", val),
                    size=lambda inst, val: setattr(bg_rect, "size", val),
                )

                # --- Left column: version, disclaimer, buttons ---
                version_label = Label(
                    text=(
                        f"[b]{Utils.instance_name} {latest_ver.as_simple_string()}[/b]"
                        f" is available\n\nYou are currently using version {Utils.version_tuple.as_simple_string()}."
                    ),
                    size_hint_y=None,
                    halign="left",
                    valign="top",
                    markup=True,
                    font_size="20sp",
                    color=(0.9, 0.9, 0.9, 1),
                )
                version_label.bind(
                    width=lambda inst, val: setattr(inst, "text_size", (val, None))
                )
                version_label.bind(
                    texture_size=lambda inst, val: setattr(inst, "height", val[1])
                )

                disclaimer_label = Label(
                    text=(
                        "If you are currently playing a game listed in the changelog, "
                        "consider finishing it before updating."
                    ),
                    size_hint=(1, None),
                    halign="left",
                    valign="top",
                    markup=False,
                    font_size="17sp",
                    color=(1.0, 0.85, 0.4, 1),
                )
                disclaimer_label.bind(
                    width=lambda inst, val: setattr(inst, "text_size", (val, None))
                )
                disclaimer_label.bind(
                    texture_size=lambda inst, val: setattr(inst, "height", val[1])
                )

                later_btn = MDButton(MDButtonText(text="Later"), style="text")
                update_btn = MDButton(MDButtonText(text="Update Now"), style="filled")

                btn_row = BoxLayout(
                    orientation="horizontal",
                    size_hint_y=None,
                    height=dp(48),
                    spacing=dp(8),
                )
                btn_row.add_widget(Widget())
                btn_row.add_widget(later_btn)
                btn_row.add_widget(update_btn)

                left_col = BoxLayout(
                    orientation="vertical",
                    size_hint_x=0.42,
                    spacing=dp(8),
                )
                left_col.add_widget(version_label)
                left_col.add_widget(disclaimer_label)
                left_col.add_widget(Widget())
                left_col.add_widget(btn_row)

                # --- Two-column body inside Popup ---
                body = BoxLayout(
                    orientation="horizontal",
                    spacing=dp(12),
                    padding=(dp(12), dp(16), dp(12), dp(12)),
                )
                body.add_widget(left_col)
                body.add_widget(changelog_scroll)

                popup = Popup(
                    title="Update Available",
                    title_align="center",
                    title_size="26sp",
                    content=body,
                    size_hint=(0.85, 0.62),
                    auto_dismiss=False,
                )

                def _on_later(*args):
                    popup.dismiss()
                    # User declined update, proceed with cache refresh
                    self._start_background_cache_refresh()

                later_btn.bind(on_release=_on_later)
                update_btn.bind(on_release=lambda *a: self._on_user_requested_update(popup, download_url))
                popup.open()
            else:
                # No update available, proceed with cache refresh
                self._start_background_cache_refresh()

        def _on_user_requested_update(self, dialog, download_url):
            dialog.dismiss()

            status_label = Label(
                text="Downloading update...",
                halign="center",
                valign="middle",
                size_hint_y=None,
                height=dp(28),
                font_size="16sp",
                color=(0.9, 0.9, 0.9, 1),
            )
            status_label.bind(width=lambda inst, val: setattr(inst, "text_size", (val, None)))
            progress_bar = ProgressBar(max=100, value=0, size_hint=(1, None), height=dp(20))

            inner = BoxLayout(
                orientation="vertical",
                spacing=dp(8),
                size_hint=(0.82, None),
                height=dp(28 + 8 + 20),
            )
            inner.add_widget(status_label)
            inner.add_widget(progress_bar)

            row = BoxLayout(orientation="horizontal", size_hint_y=None, height=inner.height)
            row.add_widget(Widget(size_hint_x=0.09))
            row.add_widget(inner)
            row.add_widget(Widget(size_hint_x=0.09))

            content = BoxLayout(orientation="vertical", padding=(dp(12), dp(16), dp(12), dp(12)))
            content.add_widget(Widget())
            content.add_widget(row)
            content.add_widget(Widget())

            downloading = Popup(
                title="Downloading Update",
                title_align="center",
                title_size="26sp",
                content=content,
                size_hint=(0.6, 0.24),
                auto_dismiss=False,
            )
            downloading.open()

            def on_progress(downloaded, total):
                def _update(dt):
                    if total > 0:
                        progress_bar.value = downloaded / total * 100
                        mb_done = downloaded / 1_048_576
                        mb_total = total / 1_048_576
                        status_label.text = f"Downloading update... {mb_done:.1f} / {mb_total:.1f} MB"
                    else:
                        mb_done = downloaded / 1_048_576
                        status_label.text = f"Downloading update... {mb_done:.1f} MB"
                Clock.schedule_once(_update)

            def _run():
                try:
                    download_and_install_win(download_url, progress_callback=on_progress)
                except Exception as e:
                    def _err(dt):
                        downloading.dismiss()
                        logging.error(f"Update download failed: {e}")
                    Clock.schedule_once(_err)

            threading.Thread(target=_run, daemon=True).start()

        @staticmethod
        def _show_launch_toast(text: str = "Opening in a new window...", persist: bool = False):
            snackbar = MDSnackbar(
                MDSnackbarText(text=text),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.5,
            )
            if persist:
                snackbar.auto_dismiss = False
            snackbar.open()
            return snackbar

        def component_action(self, button):
            button.disabled = True
            component = button.component
            is_cached_stub = getattr(component, "_mwgg_component_origin", None) == "cache_stub"
            launch_toast = self._show_launch_toast(persist=True)
            launch_toast_seconds = 4.0

            def _dismiss_launch_toast(_dt: float = 0.0) -> None:
                if not launch_toast:
                    return
                try:
                    launch_toast.dismiss()
                except Exception:
                    pass

            Clock.schedule_once(_dismiss_launch_toast, launch_toast_seconds)

            def _execute_launch() -> str | None:
                if component.func:
                    component.func()
                    return None
                exe = get_exe(component)
                if not exe:
                    raise FileNotFoundError(f"Unable to resolve executable for component {component.display_name}")
                if not component.cli:
                    subprocess.Popen(exe)
                    return None
                # if launch returns False, it started the process in background (not in a new terminal)
                if not launch(exe, component.cli):
                    return "Running in the background..."
                return None

            if is_cached_stub:
                def _worker() -> None:
                    post_toast: str | None = None
                    try:
                        post_toast = _execute_launch()
                    except Exception as exc:
                        logging.exception("Failed to launch component %s: %s", component.display_name, exc)
                        post_toast = "Failed to open component."
                    finally:
                        def _finish(dt) -> None:
                            button.disabled = False
                            if post_toast:
                                self._show_launch_toast(post_toast)

                        Clock.schedule_once(_finish, 0)

                threading.Thread(
                    target=_worker,
                    name=f"LaunchComponent:{component.display_name}",
                    daemon=True,
                ).start()
                return

            def _do_action(dt):
                post_toast: str | None = None
                try:
                    post_toast = _execute_launch()
                except Exception as exc:
                    logging.exception("Failed to launch component %s: %s", component.display_name, exc)
                    post_toast = "Failed to open component."
                finally:
                    button.disabled = False
                if post_toast:
                    self._show_launch_toast(post_toast)

            Clock.schedule_once(_do_action, 0)

        @staticmethod
        def copy_to_clipboard(text):
            from kivy.core.clipboard import Clipboard
            Clipboard.copy(text)
            MDSnackbar(MDSnackbarText(text="Copied to clipboard."), y=dp(24), pos_hint={"center_x": 0.5},
                       size_hint_x=0.5).open()

        def display_failed(self):
            """Display a dialog showing the exceptions produced by any world that failed to load during
            initialization."""
            if not self.failed_worlds:
                return
            from kivymd.uix.dialog import MDDialog, MDDialogIcon, MDDialogHeadlineText, MDDialogContentContainer
            from kivymd.uix.divider import MDDivider
            from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText
            entries = []
            for world, reason in failed_world_loads.items():
                entries.append(MDListItem(
                    MDListItemHeadlineText(text=world),
                    MDListItemSupportingText(text=reason),
                    on_release=lambda x, r=reason: self.copy_to_clipboard(r)
                ))
            dialog = MDDialog(
                MDDialogIcon(icon="alert"),
                MDDialogHeadlineText(text="Failed World Loads"),
                MDDialogContentContainer(
                    MDDivider(),
                    *entries,
                    orientation="vertical",
                )
            )
            dialog.open()

        def _on_drop_file(self, window: Window, filename: bytes, x: int, y: int) -> None:
            """ When a patch file is dropped into the window, run the associated component. """
            file, component = identify(filename.decode())
            if file and component:
                self._show_launch_toast("Patching file now...")
                run_component(component, file)
            else:
                logging.warning(f"unable to identify component for {filename}")

        def _on_keyboard(self, window: Window, key: int, scancode: int, codepoint: str, modifier: list[str]):
            # Activate search as soon as we start typing, no matter if we are focused on the search box or not.
            # Focus first, then capture the first character we type, otherwise it gets swallowed and lost.
            # Limit text input to ASCII non-control characters (space bar to tilde).
            if not self.search_box.focus:
                self.search_box.focus = True
                if key in range(32, 126):
                    self.search_box.text += codepoint

        def _stop(self, *largs):
            # ran into what appears to be https://groups.google.com/g/kivy-users/c/saWDLoYCSZ4 with PyCharm.
            # Closing the window explicitly cleans it up.
            self.root_window.close()
            super()._stop(*largs)

        def on_stop(self):
            Utils.persistent_store("launcher", "favorites", self.favorites)
            Utils.persistent_store("launcher", "filter", ", ".join(filter.name if isinstance(filter, Type) else filter
                                                                   for filter in self.current_filter))
            super().on_stop()

    Launcher(components=launch_components, args=args).run()

    # avoiding Launcher reference leak
    # and don't try to do something with widgets after window closed
    global refresh_components
    refresh_components = None
    from worlds import LauncherComponents as _lc
    _lc._rebuild_launcher_ui = None


def run_component(component: Component, *args):
    if component.func:
        component.func(*args)
        if refresh_components:
            refresh_components()
    elif component.script_name:
        subprocess.run([*get_exe(component.script_name), *args])
    else:
        logging.warning(f"Component {component} does not appear to be executable.")


def main(args: argparse.Namespace | dict | None = None):
    if isinstance(args, argparse.Namespace):
        args = {k: v for k, v in args._get_kwargs()}
    elif not args:
        args = {}

    args.setdefault("update_settings", False)
    args.setdefault("skip_cache", False)
    args.setdefault("precache", False)
    args.setdefault("run_component_callable", None)
    args.setdefault("args", ())

    if args["precache"]:
        precache_world_data()
        return

    if args["run_component_callable"]:
        module_name, qualname = args["run_component_callable"]
        call_args = []
        primary_arg = args.get("Patch|Game|Component|url")
        if primary_arg is not None:
            call_args.append(primary_arg)
        call_args.extend(args["args"])
        run_component_callable(module_name, qualname, *call_args)
        return

    path = args.get("Patch|Game|Component|url", None)
    if path is not None:
        if path.startswith("archipelago://") or path.startswith("mwgg://"):
            args["args"] = (path, *args.get("args", ()))
            # add the url arg to the passthrough args
            launch_components, text_client_component = handle_uri(path)
            if not launch_components:
                ensure_launcher_components_available()
                launch_components, text_client_component = handle_uri(path)
            if not launch_components:
                args["component"] = text_client_component
            else:
                args['launch_components'] = [text_client_component, *launch_components]
        else:
            file, component = identify(path)
            if not component:
                ensure_launcher_components_available()
                file, component = identify(path)
            if file:
                args['file'] = file
            if component:
                args['component'] = component
            if not component:
                logging.warning(f"Could not identify Component responsible for {path}")

    if args["update_settings"]:
        update_settings(args["skip_cache"])
    if "file" in args:
        run_component(args["component"], args["file"], *args["args"])
    elif "component" in args:
        run_component(args["component"], *args["args"])
    elif not args["update_settings"]:
        run_gui(args.get("launch_components", None), args.get("args", ()))


if __name__ == '__main__':
    multiprocessing.freeze_support()
    multiprocessing.set_start_method("spawn")  # if launched process uses kivy, fork won't work
    parser = argparse.ArgumentParser(
        description=f'{apname} Launcher',
        usage="[-h] [--update_settings] [--skip-cache] [--precache] "
              "[Patch|Game|Component] [-- component args here]"
    )
    run_group = parser.add_argument_group("Run")
    run_group.add_argument("--update_settings", action="store_true",
                           help="Update host.yaml and exit.")
    run_group.add_argument("--skip-cache", action="store_true",
                           help="Skip launcher cache writes during host.yaml update.")
    run_group.add_argument("--precache", action="store_true",
                           help="Build launcher cache and exit.")
    run_group.add_argument("--run_component_callable", nargs=2, metavar=("MODULE", "QUALNAME"),
                           help=argparse.SUPPRESS)
    run_group.add_argument("Patch|Game|Component|url", type=str, nargs="?",
                           help="Pass either a patch file, a generated game, the component name to run, or a url to "
                                "connect with.")
    run_group.add_argument("args", nargs="*",
                           help="Arguments to pass to component.")
    main(parser.parse_args())

    from worlds.LauncherComponents import processes

    for process in processes:
        # we await all child processes to close before we tear down the process host
        # this makes it feel like each one is its own program, as the Launcher is closed now
        process.join()

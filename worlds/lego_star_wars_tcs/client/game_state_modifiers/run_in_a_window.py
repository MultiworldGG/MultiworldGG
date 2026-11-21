"""Lego Star Wars TCS has no option for playing in a Window, either in-game, or through configuration edits.

Instead, the AP client is able to manually flip a BOOL in the D3D Core struct used by the game."""
import logging
import struct

# Tests may try to import client modules that import this module, but the win32 modules won't exist on the ubuntu/macos
# test runners. The client is expected to always be run through Windows Archipelago, where these modules should exist.
try:
    import win32gui
    import win32con
    _WIN32_PRESENT = True
except ModuleNotFoundError:
    _WIN32_PRESENT = False

from settings import get_settings

from ..events import (
    OnGameWatcherDisconnectedTickEvent,
    OnGameWatcherTickEvent,
    OnUnhookFromGameEvent,
    subscribe_event,
)
from ..common import StaticBOOL, StaticUint, ClientComponent
from ..type_aliases import TCSContext
from ...constants import SETTINGS_KEY
from ...host_yaml_settings import LegoStarWarsTCSSettings

_CLIENT_LOGGER = logging.getLogger("Client")
_DEBUG_LOGGER = logging.getLogger("TCS Debug")

_C_D3D_CORE_WINDOWED = StaticBOOL(0x029765e8 + 0x65c)
_MAIN_WINDOW_HWND = StaticUint(0x00924884)
_PC_SETTINGS_SCREEN_WIDTH = StaticUint(0x00826070 + 0x404)
# Height is directly after width, so both are read in a single call.
# PC_SETTINGS_SCREEN_HEIGHT = StaticUint(0x00826070 + 0x408)
_UNPACK_WITH_AND_HEIGHT = struct.Struct("<II")


class RunInAWindow(ClientComponent):
    _last_width: int | None = None
    _last_height: int | None = None
    _do_auto_resize: bool = True

    def __init__(self):
        super().__init__()
        settings: LegoStarWarsTCSSettings = get_settings()[SETTINGS_KEY]
        self._do_auto_resize = bool(settings.auto_resize_window)

    @staticmethod
    def set_windowed(ctx: TCSContext, windowed: bool):
        was_windowed = bool(_C_D3D_CORE_WINDOWED.get(ctx))
        if windowed != was_windowed:
            _C_D3D_CORE_WINDOWED.set(ctx, windowed)
            if windowed:
                noun = "a window"
            else:
                noun = "fullscreen"
            _CLIENT_LOGGER.info("The game will now run in %s. Enter the Video Settings menu and "
                                "Confirm, or alt+tab out and back in, to update the game.", noun)

        # fixme: If the game is fullscreen, the game won't update to be in a window until either the user enters the
        #  video/effects menu and accepts (even without making changes), or alt-tabs out of the game and then back in.
        #  I have tried to use Windows APIs (through win32gui) to hide/show the window, but they do not seem to have the
        #  same effect. For now, users will just have to alt-tab or use the video/effects menu.

    if _WIN32_PRESENT:
        @subscribe_event
        async def on_tick(self, event: OnGameWatcherTickEvent):
            self._check_and_update_window_size_if_resolution_changed(event.context)

        @subscribe_event
        async def on_disconnected_tick(self, event: OnGameWatcherDisconnectedTickEvent):
            self._check_and_update_window_size_if_resolution_changed(event.context)

    @subscribe_event
    async def on_disconnected_from_game(self, event: OnUnhookFromGameEvent):
        self.reset_last_known_resolution()

    def reset_last_known_resolution(self):
        self._last_width = None
        self._last_height = None

    def _check_and_update_window_size_if_resolution_changed(self, ctx: TCSContext):
        """When Windowed mode is forced by the client, changing the resolution in-game does not automatically resize the
        window to match unless the player restarts their game.

        Resizing the window manually is a pain. So, using Windows APIs, the client can update the size of the game
        window to match the change in resolution."""
        if not self._do_auto_resize:
            # There is a host.yaml option to disable auto-resizing, in-case it
            return
        if not _C_D3D_CORE_WINDOWED.get(ctx):
            # Windowed mode has not been forced, so do nothing.
            return

        width_and_height_bytes = ctx.read_bytes(_PC_SETTINGS_SCREEN_WIDTH, 8)
        width, height = _UNPACK_WITH_AND_HEIGHT.unpack(width_and_height_bytes)
        changed = False
        if self._last_height is None:
            self._last_height = height
        elif self._last_height != height:
            changed = True
            self._last_height = height

        if self._last_width is None:
            self._last_width = width
        elif self._last_width != width:
            changed = True
            self._last_width = width

        if not changed:
            # Nothing to do.
            return

        _DEBUG_LOGGER.info("Game resolution has changed, changing window size to match.")

        hwnd = _MAIN_WINDOW_HWND.get(ctx)

        if not win32gui.IsWindow(hwnd):
            # Probably cannot happen unless the player closes the game in the middle of this code running.
            return

        flags = 0
        # Retain the window position (ignore the X and Y arguments)
        flags |= win32con.SWP_NOMOVE
        # Do not change the window's Z-order (ignore the InsertAfter argument)
        flags |= win32con.SWP_NOZORDER
        # Post the request to the thread that owns the window (unsure if this is needed, but we're definitely sending
        # this request from a different thread so it sounds relevant)
        flags |= win32con.SWP_ASYNCWINDOWPOS
        # Do not activate the window and do not move it to the topmost group.
        flags |= win32con.SWP_NOACTIVATE
        # First ensure the window is not minimized, otherwise setting the window pos does nothing.
        # NOACTIVATE will prevent activating the window if it was not active.
        _DEBUG_LOGGER.info("Ensuring game window is shown")
        win32gui.ShowWindow(hwnd, win32con.SW_SHOWNOACTIVATE)
        _DEBUG_LOGGER.info("Setting game window size")
        win32gui.SetWindowPos(hwnd, 0, 0, 0, width, height, flags)

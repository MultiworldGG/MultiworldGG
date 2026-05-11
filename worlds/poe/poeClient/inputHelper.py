import logging
import os
import sys

# Load vendor modules before any other imports that depend on them
try:
    from . import fileHelper
    fileHelper.load_vendor_modules()
except ImportError:
    # Fallback for when running as a script
    import fileHelper
    fileHelper.load_vendor_modules()

import asyncio
try:
    import pywinctl as gw
except:
    import pygetwindow as gw  # type: ignore
import time

logger = logging.getLogger("poeClient")


class KeyboardAutomationUnavailable(RuntimeError):
    """Raised when the keyboard automation backend needed by the PoE client cannot load."""


_keyboard_backend_error: Exception | None = None
try:
    from pynput import keyboard as pynput_keyboard
    from pynput.keyboard import Controller, Key
except ImportError as e:
    pynput_keyboard = None
    Controller = None
    Key = None
    _keyboard_backend_error = e

try:
    keyboard_controller = Controller() if Controller else None
except Exception as e:
    keyboard_controller = None
    _keyboard_backend_error = e
_debug = True
_last_called = None
DEBOUNCE_TIME = 1  # seconds
_send_lock = asyncio.Lock()  # Add asyncio lock

GAME_WINDOW_TITLE = "Path of Exile"


def require_keyboard_automation():
    if _keyboard_backend_error is not None:
        raise KeyboardAutomationUnavailable(
            "Path of Exile client keyboard automation is unavailable. "
            "The pynput keyboard backend could not be loaded; install the PoE client dependencies "
            "or run the client in an environment with a supported keyboard backend."
        ) from _keyboard_backend_error
    if keyboard_controller is None or Key is None or pynput_keyboard is None:
        raise KeyboardAutomationUnavailable(
            "Path of Exile client keyboard automation is unavailable because no keyboard backend was loaded."
        )


def get_keyboard_module():
    require_keyboard_automation()
    return pynput_keyboard

def get_clipboard():
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        value = root.clipboard_get()
    except tk.TclError:
        value = ""
    root.destroy()
    return value

def set_clipboard(value):
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    root.clipboard_clear()
    root.clipboard_append(value)
    root.update()  # Ensure clipboard is set before destroying
    root.destroy()
    
def get_then_set_clipboard(new_value: str) -> str:
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()
    try:
        value = root.clipboard_get()
    except tk.TclError:
        value = ""
    root.clipboard_clear()
    root.update()
    root.clipboard_append(new_value)
    root.update()  # Ensure clipboard is set before destroying
    root.destroy()
    return value

async def important_send_poe_text(command: str, retry_times: int = 9001, retry_delay: float = 0.5):
    return await send_poe_text(command, retry_times, retry_delay)

async def send_poe_text_ignore_debounce(command: str):
    global _last_called
    async with _send_lock:  # Use lock for thread safety
        _last_called = None  # Ignore debounce time
    return await send_poe_text(command)

async def send_poe_text(command: str, retry_times: int = 1, retry_delay: float = 0):
    return await send_multiple_poe_text([command], retry_times, retry_delay)

async def send_multiple_poe_text(commands: list[str], retry_times: int = 1, retry_delay: float = 0):
    require_keyboard_automation()
    window = gw.getActiveWindow()
    global _last_called
    # if windows is active
    now = time.monotonic()
    async with _send_lock:  # Acquire lock before any operations
        if window is not None and window.title == GAME_WINDOW_TITLE and not (_last_called is not None and now - _last_called < DEBOUNCE_TIME):

            logger.debug("Found active Path of Exile window")

            _last_called = now

            clipboard_value = get_then_set_clipboard(commands[0])
            for i, command in enumerate(commands):
                if not i == 0:
                    set_clipboard(command)
                logger.debug(f"Sending command: {command}")
                # Press Enter
                keyboard_controller.press(Key.enter)
                keyboard_controller.release(Key.enter)

                await asyncio.sleep(0.05)
                # Type command
                keyboard_controller.press(Key.ctrl)
                keyboard_controller.press('v')
                keyboard_controller.release('v')
                keyboard_controller.release(Key.ctrl)

                await asyncio.sleep(0.05)
                # Press Enter again
                keyboard_controller.press(Key.enter)
                keyboard_controller.release(Key.enter)

            set_clipboard(clipboard_value)
            if _debug:
                logger.info("Sent command to Path of Exile:" + command)
            await asyncio.sleep(0.05)
            return True

    if retry_times > 0:
        if _debug:
            logger.info(f"Path of Exile window not active, retrying {retry_times} times with {retry_delay} seconds delay")
        delay = retry_delay
        if _last_called is not None and now - _last_called < DEBOUNCE_TIME:
            delay += DEBOUNCE_TIME - (now - _last_called)
            if _debug:
                logger.info(f"Debounced: Waiting {delay} seconds before retrying")
        await asyncio.sleep(delay)
        return await send_multiple_poe_text(commands, retry_times - 1, retry_delay)
    else:
        if _debug:
            logger.info("Path of Exile window not active, no retries left")
        return False

import asyncio
import hashlib
import logging
import re
import pickle
import asyncio
import importlib.util
import sys
import traceback
import types
from collections import deque
from pathlib import Path

if sys.platform == "win32":
    import winreg

import typing
if typing.TYPE_CHECKING:
    from worlds.poe.Client import PathOfExileContext

_debug = True
lock = asyncio.Lock()  # Lock to ensure thread-safe access to settings file
settings_file_path = Path("poe_settings.pkl")
client_txt_last_modified_time = None
callbacks_on_file_change: list[callable] = []
logger = logging.getLogger("poeClient")

from Utils import local_path
vendor_dir = Path(local_path("lib")) / "poe_client_vendor"

def _ensure_stdlib_shims():
    """Provide minimal shims for stdlib modules missing in the frozen runtime."""
    if 'doctest' not in sys.modules:
        shim = types.ModuleType('doctest')
        # minimal API; pyrect only imports doctest, doesn't use at import time
        def testmod(*args, **kwargs):
            return None

        shim.testmod = testmod
        sys.modules['doctest'] = shim


def load_vendor_modules():
    import os
    import sys
    import zipfile
    import tempfile
    import atexit
    import shutil
    import pkgutil
    from Utils import is_frozen

    # In frozen builds, dependencies are already in library.zip via requirements.txt
    # Only load vendor modules when running from source
    if is_frozen():
        return

    # Import version after other imports to avoid circular imports
    try:
        from ..Version import POE_VERSION
    except ImportError:
        POE_VERSION = "unknown"

    # Prevent double-load
    if getattr(sys, "_vendor_modules_loaded", False):
        return
    sys._vendor_modules_loaded = True

    if vendor_dir in sys.path:
        return
    
    _ensure_stdlib_shims()
    
    # Check if vendor directory exists and has matching version
    version_file = vendor_dir / "poe_version.txt"
    should_recreate = True
    zip_dest = os.path.join(vendor_dir, "vendor_modules.zip")
    if vendor_dir.exists():
        try:
            if version_file.exists():
                with open(version_file, 'r') as f:
                    stored_version = f.read().strip()
                if stored_version == POE_VERSION:
                    should_recreate = False
                    logger.debug(f"[vendor] Version {POE_VERSION} matches, using existing vendor directory")
                else:
                    logger.info(f"[vendor] Version mismatch: stored={stored_version}, current={POE_VERSION}, recreating vendor directory")
            else:
                logger.info("[vendor] No version file found, recreating vendor directory")
        except Exception as e:
            logger.warning(f"[vendor] Error checking version: {e}, recreating vendor directory")
    
    if should_recreate:
        # Remove existing directory if it exists
        if vendor_dir.exists():
            try:
                shutil.rmtree(vendor_dir)
            except PermissionError:
                # Directory is in use (likely during tests), just skip recreation
                logger.debug("[vendor] Vendor directory in use, skipping recreation")
                if str(vendor_dir) not in sys.path:
                    sys.path.append(str(vendor_dir))
                    # Add subdirectories as well
                    for subdir in vendor_dir.iterdir():
                        if subdir.is_dir():
                            sys.path.append(str(subdir))
                return

        # Ensure vendor directory exists
        os.makedirs(vendor_dir, exist_ok=True)
        
        try:
            vendor_zip_data = pkgutil.get_data("worlds.poe.poeClient", "vendor/vendor_modules.zip")

            if vendor_zip_data is None:
                base_dir = os.path.dirname(__file__)
                vendor_zip_path = os.path.join(base_dir, "vendor_modules.zip")

                if not os.path.isfile(vendor_zip_path):
                    logger.warning("[vendor] vendor_modules.zip not found in package or current directory")
                    return
                shutil.copy2(vendor_zip_path, zip_dest)
            else:
                with open(zip_dest, "wb") as f:
                    f.write(vendor_zip_data)

            with zipfile.ZipFile(zip_dest, 'r') as vendor_zip:
                vendor_zip.extractall(vendor_dir)

            # Clean up the copied zip file after extraction
            os.remove(zip_dest)
            
            # Write version file
            with open(version_file, 'w') as f:
                f.write(POE_VERSION)
            logger.info(f"[vendor] Created vendor directory for version {POE_VERSION}")

        except Exception as e:
            logger.error(f"[vendor] Failed to extract vendor modules: {e}")
            raise

    # Add vendor modules to sys.path
    sys.path.append(str(vendor_dir))
    
    # Add subdirectories, with httpx and httpcore at the end to avoid stdlib conflicts
    last_vendor_modules = ['httpx', 'httpcore']

    for subdir in vendor_dir.iterdir():
        if subdir.is_dir():
            if subdir.name in last_vendor_modules:
                sys.path.append(str(subdir))
            else:
                sys.path.insert(0, str(subdir))
            # Add each subdirectory to the path as well
            for subdir in vendor_dir.iterdir():
                if subdir.is_dir():
                    if subdir.name in last_vendor_modules:
                        sys.path.append(str(subdir))
                    else:
                        sys.path.insert(0, str(subdir))


def safe_filename(filename: str) -> str:
    # Replace problematic characters with underscores
    return re.sub(r"[^\w\-_\. ]", "", filename)


async def callback_on_file_change(filepath: Path, async_callbacks: list[callable]):
    """Monitor file for changes and call callbacks. Can be cancelled."""

    async def zone_change_callback(line: str):
        for callback in async_callbacks:
            if callable(callback):
                try:
                    await callback(line)
                except asyncio.CancelledError:
                    logger.info("Callback cancelled during execution")
                    raise
                except Exception as e:
                    logger.error(f"Error in callback: {e}")
                    raise

    try:
        await callback_on_file_line_change(filepath, zone_change_callback)
    except asyncio.CancelledError:
        logger.info(f"File monitoring cancelled for {filepath}")
        raise


async def callback_on_file_line_change(filepath: Path, async_callback: callable):
    """Monitor file line changes. Cancelable version."""
    logger.info(f"Starting file monitoring for {filepath}")

    try:
        if not filepath.exists():
            logger.warning(f"File does not exist: {filepath}")
            return

        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            f.seek(0, 2)  # Move to end of file

            while True:
                if asyncio.current_task().cancelled():
                    logger.info("File monitoring task cancelled")
                    break

                try:
                    line = f.readline()
                    if not line:
                        await asyncio.sleep(0.3)
                        continue

                    line = line.strip()
                    await async_callback(line)

                except asyncio.CancelledError:
                    logger.info("File monitoring cancelled during callback")
                    raise
                except Exception as e:
                    logger.error(f"Error reading file {filepath}: {e}")
                    raise

    except asyncio.CancelledError:
        logger.info(f"File monitoring for {filepath} was cancelled")
        raise
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        raise
    except PermissionError:
        logger.error(f"Permission denied reading file: {filepath}")
        logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        raise
    except OSError as e:
        logger.error(f"OS error monitoring file {filepath}: {e}")
        logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        raise
    except IOError as e:
        logger.error(f"I/O error monitoring file {filepath}: {e}")
        logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        raise
    except Exception as e:
        logger.error(''.join(traceback.format_exception(type(e), e, e.__traceback__)))
        logger.error(f"Unexpected error monitoring {filepath} ({type(e).__name__}): {e}")
        raise
    finally:
        logger.info(f"File monitoring stopped for {filepath}")


def get_last_n_lines_of_file(filepath, n=1):
    with open(filepath, 'r') as f:
        return list(deque(f, n))


def short_hash(s: str) -> str:
    return hashlib.sha256(s.encode()).hexdigest()[:8]


def build_world_key(ctx: "PathOfExileContext") -> str:
    """
    Build a unique key for the world based on the context.
    This key is used to store and retrieve settings for the specific world.
    """
    if ctx is None:
        return "unconnected"
    world_prefix = ctx.slot_data.get('poe-uuid', '')
    return f"world {str((ctx.seed_name if ctx.seed_name is not None else '') + world_prefix + " : " + (ctx.username if ctx.username is not None else ''))}"

async def save_settings(ctx: "PathOfExileContext", path: Path = settings_file_path):
    # Read existing settings first
    async with lock:
        existing_settings = await read_dict_from_pickle_file(path)

        # Create new world entry
        world_key = build_world_key(ctx)
        default_key = "world default"
        new_world_data = {
            "tts_speed": str(ctx.filter_options.tts_speed),
            "tts_enabled": bool(ctx.filter_options.tts_enabled),
            "loot_filter_sounds": int(ctx.filter_options.loot_filter_sounds),
            "loot_filter_display": int(ctx.filter_options.loot_filter_display),
            "client_txt": str(ctx.client_text_path),
            "last_char": str(ctx.character_name),
            "base_item_filter": str(ctx.base_item_filter),
            "poe_doc_path": str(ctx.poe_doc_path),
            "whisper_updates": str(ctx.whisper_updates_enabled),
            "already_received_items": ctx.previously_received_item_ids,
        }

        # Add/update the world entry in existing settings
        existing_settings[world_key] = new_world_data
        existing_settings[default_key] = new_world_data

        # Write back the merged settings
        await write_dict_to_pickle_file(existing_settings, path)

    if _debug:
        logger.info(f"[DEBUG] Saved settings for {world_key}. Total worlds: {len(existing_settings)}")


async def load_settings(ctx: "PathOfExileContext", path: Path = settings_file_path, ) -> dict:
    if not path.exists():
        if _debug:
            logger.info(f"[DEBUG] Settings file {path} does not exist. Returning empty settings.")
        return {}
    try:
        async with lock:
            all_settings = await read_dict_from_pickle_file(path)
        # Get settings for the specific world
        world_key = build_world_key(ctx)
        default_key = "world default"
        world_settings = all_settings.get(world_key, {})
        default_settings = all_settings.get(default_key, {})
        if _debug:
            logger.info(f"[DEBUG] Loaded settings from {path}.")
            if world_settings:
                logger.info(f"[DEBUG] Found settings for {world_key}")
            else:
                logger.info(f"[DEBUG] No settings found for {world_key}")

        loaded_data = {
            "tts_speed": world_settings.get("tts_speed", default_settings.get("tts_speed")),
            "tts_enabled": world_settings.get("tts_enabled", default_settings.get("tts_enabled")),
            "loot_filter_sounds": world_settings.get("loot_filter_sounds", default_settings.get("loot_filter_sounds")),
            "loot_filter_display": world_settings.get("loot_filter_display", default_settings.get("loot_filter_display")),
            "client_txt": world_settings.get("client_txt",
                                             default_settings.get("client_txt", find_possible_client_txt_path())),
            "last_char": world_settings.get("last_char", None),
            "base_item_filter": world_settings.get("base_item_filter", default_settings.get("base_item_filter")),
            "whisper_updates": world_settings.get("whisper_updates", default_settings.get("whisper_updates", None)),
            # List of item IDs already received for whisper updates. Not saved to defaults, nor loaded from defaults.
            "already_received_items": world_settings.get("already_received_items", []),
        }

        return loaded_data

    except Exception as e:
        logger.info(f"[ERROR] Failed to load settings from {path}: {e}")
        return {}


async def write_dict_to_pickle_file(data: dict, file_path: Path):
    with open(file_path, 'wb') as f:
        pickle.dump(data, f)
    if _debug:
        logger.info(f"[DEBUG] Dictionary with {len(data)} items written to {file_path}")


async def read_dict_from_pickle_file(file_path: Path) -> dict:
    data = {}
    if not file_path.exists():
        logger.info(f"File {file_path} does not exist.")
        return data

    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
        if _debug:
            logger.info(f"[DEBUG] Dictionary with {len(data)} items read from {file_path}")
    except (pickle.PickleError, EOFError, FileNotFoundError) as e:
        logger.info(f"[ERROR] Failed to read pickle file {file_path}: {e}")
        data = {}

    return data


def get_poe_install_location_from_registry() -> str | None:
    """Retrieve the Path of Exile install location from the Windows registry."""
    if sys.platform != "win32":
        return None
    try:
        registry_key = r"Software\GrindingGearGames\Path of Exile"
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_key) as key:
            install_location, _ = winreg.QueryValueEx(key, "InstallLocation")
            return install_location
    except FileNotFoundError:
        print("Registry key not found.")
        return None
    except Exception as e:
        print(f"Error accessing registry: {e}")
        return None


def find_possible_client_txt_path() -> Path | None:
    """Return the first valid path for the client.txt file."""
    registry_path = get_poe_install_location_from_registry()
    if registry_path:
        log_path = Path(registry_path) / "logs" / "client.txt"
        if log_path.exists():
            print(f"Found client.txt (via registry) at: {log_path}")
            logger.debug(f"Found client.txt (via registry) at: {log_path}")
            return log_path
    intermediate_paths = [
        Path(""),
        Path("games"),
        Path("Program Files (x86)"),
        Path("Program Files"),
        Path("Program Files (x86)/Steam"),
        Path("Program Files/Steam"),
        Path("Steam"),
        Path("SteamLibrary"),
        Path("games/SteamLibrary"),
        Path("steamlibraryd"),
    ]
    possible_paths = [
        Path("steamapps/common/Path of Exile"),
        Path("Path of Exile"),
        Path("poe"),
    ]
    suffix_path = Path("logs") / "client.txt"
    # Windows specific, I know....
    for drive in ["D", "C", "E", "F", "G"]:
        drive_path = Path(f"{drive}:/")
        for intermediate in intermediate_paths:
            for possible in possible_paths:
                to_check = drive_path / intermediate / possible / suffix_path
                print(f"Checking path: {to_check}")
                if to_check.exists():
                    print(f"Found client.txt at: {to_check}")
                    logger.debug(f"Found client.txt at: {to_check}")
                    return to_check

    return None


if __name__ == "__main__":
    # For testing purposes, find the client.txt path

    print("Finding client.txt path...")
    client_txt_path = find_possible_client_txt_path()

    print("log check")
    if client_txt_path:
        print(f"Found client.txt at: {client_txt_path}")
    else:
        print("Could not find client.txt in any of the expected locations.")
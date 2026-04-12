import json
import shutil
import zipfile
from typing import Optional, cast, Dict, Any
import asyncio
import multiprocessing
import os
import subprocess
import traceback
import socket
import platform
import errno
import tkinter as tk
from tkinter import filedialog

from CommonClient import get_base_parser, logger, server_loop, gui_enabled
from NetUtils import ClientStatus
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"

from settings import get_settings
from .data.Planets import get_all_active_locations
from . import Rac2Settings
from .Container import Rac2ProcedurePatch
from .ClientCheckLocations import handle_checked_location
from .Callbacks import update, init
from .ClientReceiveItems import handle_received_items
from .NotificationManager import NotificationManager
from .Rac2Interface import HUD_MESSAGE_DURATION, ConnectionState, create_pine_interface, Rac2Interface, Rac2Planet
from configparser import ConfigParser
from . import get_world_version

DEFAULT_PINE_PORT = 28011

# Load Universal Tracker
tracker_loaded: bool = False
try:
    from worlds.tracker.TrackerClient import (
        TrackerCommandProcessor as ClientCommandProcessor,
        TrackerGameContext as CommonContext,
        UT_VERSION
    )

    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor, CommonContext

def find_free_port(start=28021, end=28031):
    system_name = platform.system()

    # On Windows, keep the old TCP-based logic
    if system_name == "Windows":
        for port in range(start, end + 1):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                try:
                    s.bind(("127.0.0.1", port))
                    return port
                except OSError:
                    continue
        return DEFAULT_PINE_PORT

    # On Linux/macOS, check for existing socket files instead
    base_dir = os.environ.get("XDG_RUNTIME_DIR") or os.environ.get("TMPDIR") or "/tmp"

    for port in range(start, end + 1):
        if port == DEFAULT_PINE_PORT:
            sock_path = os.path.join(base_dir, "pcsx2.sock")
        else:
            sock_path = os.path.join(base_dir, f"pcsx2.sock.{port}")

        # If socket file exists, test whether it’s actually active
        if os.path.exists(sock_path):
            try:
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                    s.connect(sock_path)
                    # If we connected, it’s in use
                    continue
            except OSError as e:
                # Connection failed → likely stale socket file, safe to remove
                if e.errno in (errno.ECONNREFUSED, errno.ENOENT):
                    try:
                        os.remove(sock_path)
                    except OSError:
                        pass
                # In either case, we can reuse this port now
                return port
        else:
            # No such file → definitely free
            return port

    # Fallback if all taken
    return DEFAULT_PINE_PORT

def ensure_pine_settings(ini_path: str, port: int = 28011):
    """Ensure INI has configuration for PINE."""
    config = ConfigParser()
    config.optionxform = str  # Preserve key case exactly

    ini_dir = os.path.dirname(ini_path)
    if not os.path.exists(ini_dir):
        os.makedirs(ini_dir, exist_ok=True)

    # Create minimal INI if missing
    if not os.path.exists(ini_path):
        with open(ini_path, 'w') as f:
            f.write("[EmuCore]\n")

    config.read(ini_path)

    # --- EmuCore section ---
    if 'EmuCore' not in config:
        config['EmuCore'] = {}
    # Normalize capitalization
    for key in list(config['EmuCore'].keys()):
        if key.lower() == 'enablepine' and key != 'EnablePINE':
            config['EmuCore']['EnablePINE'] = config['EmuCore'].pop(key)
        elif key.lower() == 'pineslot' and key != 'PINESlot':
            config['EmuCore']['PINESlot'] = config['EmuCore'].pop(key)
    # Ensure required settings exist and are correct
    config['EmuCore']['EnablePINE'] = 'true'
    config['EmuCore']['PINESlot'] = str(port)

    # --- Achievements section ---
    if 'Achievements' not in config:
        config['Achievements'] = {}
    # Normalize capitalization
    for key in list(config['Achievements'].keys()):
        if key.lower() == 'enabled' and key != 'Enabled':
            config['Achievements']['Enabled'] = config['Achievements'].pop(key)
    config['Achievements']['Enabled'] = 'false'

    # Write updated config back
    with open(ini_path, 'w') as f:
        config.write(f)

def setup_pine():
    """Determine port and create Pine instance."""
    host_settings = get_settings()
    game_ini = host_settings.get('rac2_options', {}).get('game_ini')

    # Only pick port here; do not touch ini yet
    if game_ini and os.path.exists(os.path.dirname(game_ini)):
        port = find_free_port()
    else:
        port = 28011

    create_pine_interface(port)
    return port

# Run early so Pine instance exists for Rac2Interface
pine_port = setup_pine()

def validate_rac2_settings() -> bool:
    """Validate rac2_options from host.yaml before continuing.
    Logs warnings but does not abort."""
    host_settings = get_settings()
    rac2_opts = host_settings.get("rac2_options", {})

    problems = []

    # ISO file check
    iso_file = rac2_opts.get("iso_file")
    if not iso_file:
        problems.append("Missing 'iso_file' in rac2_options.")
    else:
        iso_file_expanded = os.path.expandvars(os.path.expanduser(iso_file))
        if not os.path.isfile(iso_file_expanded):
            problems.append(f"ISO file not found: {iso_file_expanded}")

    # ISO start (PCSX2 path)
    iso_start = rac2_opts.get("iso_start")
    if not iso_start:
        problems.append("Missing 'iso_start' — should be path to PCSX2 executable.")
    elif isinstance(iso_start, str):
        iso_start_expanded = os.path.expandvars(os.path.expanduser(iso_start))
        if not os.path.isfile(iso_start_expanded):
            problems.append(f"'iso_start' path does not exist: {iso_start_expanded}")
        else:
            system = platform.system().lower()
            exe_name = os.path.basename(iso_start_expanded).lower()
            # Windows check
            if system == "windows" and not exe_name.endswith(("pcsx2.exe", "pcsx2-qt.exe")):
                problems.append(f"On Windows, PCSX2 executable usually ends with pcsx2.exe — got {exe_name}")
            # Linux/macOS check
            elif system in ("linux", "darwin") and "pcsx2" not in exe_name:
                problems.append(f"Expected 'pcsx2' binary on {system.capitalize()}, got {exe_name}")

    # Game INI
    game_ini = rac2_opts.get("game_ini")
    if not game_ini:
        problems.append("Missing 'game_ini' path — should point to a PCSX2 game settings INI file.")
    else:
        game_ini_expanded = os.path.expandvars(os.path.expanduser(game_ini))
        if not os.path.isfile(game_ini_expanded):
            problems.append(f"Game INI not found: {game_ini_expanded}")

    # Always warn, never block
    if problems:
        logger.warning("⚠ Rac2 configuration issues detected:")
        for p in problems:
            logger.warning(f"  - {p}")
        logger.warning("Continuing anyway; the game may still launch normally.")

        # Notify user in-client
        try:
            ctx = globals().get("ctx")  # use context if available
            if ctx and hasattr(ctx, "notification_manager"):
                ctx.notification_manager.queue_notification("Some RAC2 config issues found (see above). Continuing anyway.")
        except Exception:
            pass

    return True  # Always return True now

class Rac2CommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: CommonContext):
        super().__init__(ctx)

    def _cmd_test_hud(self, *args):
        """Send a message to the game interface."""
        if isinstance(self.ctx, Rac2Context):
            self.ctx.notification_manager.queue_notification(' '.join(map(str, args)))

    def _cmd_status(self):
        """Display the current PCSX2 connection status."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(f"Connection status: {'Connected' if self.ctx.is_connected else 'Disconnected'}")

    def _cmd_segments(self):
        """Display the memory segment table."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(self.ctx.game_interface.get_segment_pointer_table())

    def _cmd_test_deathlink(self, deaths: str):
        """Queue up specified number of deaths."""
        if isinstance(self.ctx, Rac2Context):
            logger.info(f"Queuing {deaths} deaths.")
            self.ctx.notification_manager.queue_notification("Received test deathlink")
            self.ctx.queued_deaths = int(deaths)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, Rac2Context):
            self.ctx.death_link_enabled = not self.ctx.death_link_enabled
            Utils.async_start(self.ctx.update_death_link(
                self.ctx.death_link_enabled), name="Update Deathlink")
            message = f"Deathlink {'enabled' if self.ctx.death_link_enabled else 'disabled'}"
            logger.info(message)
            self.ctx.notification_manager.queue_notification(message)

    def _cmd_start(self):
        """Select and start with a .aprac2 patch file."""
        if not isinstance(self.ctx, Rac2Context):
            logger.error("Not in a valid RAC2 context.")
            return

        # Prevent launching if already connected to PCSX2
        if self.ctx.game_interface.get_connection_state():
            msg = "Already connected to Ratchet & Clank 2 / PCSX2 — please close old instance or open another client."
            logger.warning(msg)
            self.ctx.notification_manager.queue_notification(msg)
            return

        # Validate rac2 host.yaml options
        if not validate_rac2_settings():
            return

        # Open file dialog
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename(
            title="Select a Ratchet & Clank 2 .aprac2 file",
            filetypes=[(f"{apname} RAC2 Patch Files", "*.aprac2"), ("All Files", "*.*")]
        )
        root.destroy()

        if not file_path:
            logger.info("No file selected.")
            return

        # Launch async patching + game startup
        logger.info(f"Selected patch: {file_path}")
        self.ctx.notification_manager.queue_notification("Launching selected patch file...")

        async def start_patch():
            try:
                await patch_and_run_game(file_path)
                self.ctx.auth = get_name_from_aprac2(file_path)
                
                connect_address = get_connection_info_from_aprac2(file_path)
                if connect_address:
                    logger.info(f"Auto-connecting to {connect_address}")
                    self.ctx.server_address = connect_address
                    await self.ctx.connect(connect_address)
                logger.info("Game launch initiated.")
            except Exception as e:
                logger.error(f"Failed to start patch: {e}")
                self.ctx.notification_manager.queue_notification(f"Error: {e}")

        Utils.async_start(start_patch(), name="Manual Patch Launch")


class Rac2Context(CommonContext):
    current_planet: Optional[Rac2Planet] = None
    previous_planet: Optional[Rac2Planet] = None
    is_pending_death_link_reset = False
    command_processor = Rac2CommandProcessor
    game_interface: Rac2Interface
    notification_manager: NotificationManager
    game = "Ratchet & Clank 2"
    items_handling = 0b111
    pcsx2_sync_task = None
    is_connected = ConnectionState.DISCONNECTED
    is_loading: bool = False
    slot_data: dict[str, Utils.Any] = None
    last_error_message: Optional[str] = None
    death_link_enabled = False
    queued_deaths: int = 0
    previous_decoy_glove_ammo: int = 0

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.client_version = tuple(get_world_version())
        self.server_version = None
        self.game_interface = Rac2Interface(logger)
        self.notification_manager = NotificationManager(HUD_MESSAGE_DURATION)

    def _normalize_version(self, v):
        return tuple(v[i] if i < len(v) else 0 for i in range(4))

    def run_generator(self):
        if tracker_loaded:
            super().run_generator()

    def make_gui(self):
        ui = super().make_gui()
        client_ver = '.'.join(map(str, self.client_version))
        title = f"Ratchet & Clank 2 Client v{client_ver}"
        if tracker_loaded:
            try:
                from worlds.tracker.TrackerClient import UT_VERSION
                title += f" | Universal Tracker {UT_VERSION}"
            except Exception:
                pass
        # AP version is added behind this automatically
        title += f" | {apname}"
        ui.base_title = title
        return ui

    def _update_window_title(self):
        if not hasattr(self, "ui") or not getattr(self.ui, "root", None):
            return

        client_ver = '.'.join(map(str, self.client_version))
        title = f"Ratchet & Clank 2 Client v{client_ver}"

        if self.server_version:
            server_ver = '.'.join(map(str, self.server_version))
            title += f" | Host v{server_ver}"
        else:
            title += " | Host v?"

        if tracker_loaded:
            try:
                from worlds.tracker.TrackerClient import UT_VERSION
                title += f" | Universal Tracker {UT_VERSION}"
            except Exception:
                pass

        title += f" | {apname}"

        try:
            self.ui.base_title = title
            self.ui.root.title(title)
        except Exception:
            pass

    def on_deathlink(self, data: Utils.Dict[str, Utils.Any]) -> None:
        super().on_deathlink(data)
        if self.death_link_enabled:
            self.queued_deaths += 1
            cause = data.get("cause", "")
            if cause:
                self.notification_manager.queue_notification(f"DeathLink: {cause}")
            else:
                self.notification_manager.queue_notification(f"DeathLink: Received from {data['source']}")

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(Rac2Context, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args["slot_data"]

            # Version handling
            raw_version = self.slot_data.get("world_version")
            if raw_version:
                self.server_version = tuple(raw_version)
            else:
                self.server_version = None

            client_v = self._normalize_version(self.client_version)
            server_v = self._normalize_version(self.server_version) if self.server_version else None

            if server_v:
                if client_v[:2] != server_v[:2]:
                    logger.warning(
                        f"Incompatible version! Host: {server_v}, Client: {client_v}. "
                        f"(Replace your apworld + restart {apname})"
                    )
                elif client_v != server_v:
                    logger.info(
                        f"Minor version difference. Host: {server_v}, Client: {client_v}. "
                        f"(Universal Tracker may not work correctly)"
                    )
            else:
                logger.info("Host world version unknown.")

            # Set death link tag if it was requested in options
            if "death_link" in self.slot_data:
                self.death_link_enabled = bool(self.slot_data["death_link"])
                Utils.async_start(self.update_death_link(self.death_link_enabled))

            # Scout all active locations for lookups that may be required later on
            all_locations = [loc.location_id for loc in get_all_active_locations(self.slot_data)]
            self.locations_scouted = set(all_locations)
            Utils.async_start(self.send_msgs([{
                "cmd": "LocationScouts",
                "locations": list(self.locations_scouted)
            }]))

            # Update title after connect
            self._update_window_title()


def update_connection_status(ctx: Rac2Context, status: bool):
    if ctx.is_connected == status:
        return

    if status:
        logger.info("Connected to Ratchet & Clank 2")
    else:
        logger.info("Unable to connect to the PCSX2 instance, attempting to reconnect...")
    ctx.is_connected = status


async def pcsx2_sync_task(ctx: Rac2Context):
    logger.info("Starting Ratchet & Clank 2 Connector, attempting to connect to emulator...")
    ctx.game_interface.connect_to_game()
    while not ctx.exit_event.is_set():
        try:
            is_connected = ctx.game_interface.get_connection_state()
            update_connection_status(ctx, is_connected)
            if is_connected:
                await _handle_game_ready(ctx)
            else:
                await _handle_game_not_ready(ctx)
        except ConnectionError:
            ctx.game_interface.disconnect_from_game()
        except Exception as e:
            if isinstance(e, RuntimeError):
                logger.error(str(e))
            else:
                logger.error(traceback.format_exc())
            await asyncio.sleep(3)
            continue


async def handle_check_goal_complete(ctx: Rac2Context):
    if ctx.current_planet is Rac2Planet.Yeedil:
        moby = ctx.game_interface.get_moby(197)
        if moby is not None and ctx.game_interface.get_moby(197).state == 0x11:
            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])


async def handle_deathlink(ctx: Rac2Context):
    if ctx.game_interface.get_alive():
        if ctx.is_pending_death_link_reset:
            ctx.is_pending_death_link_reset = False
        if ctx.queued_deaths > 0 and ctx.game_interface.get_pause_state() == 0 and ctx.game_interface.get_ratchet_state() != 97:
            ctx.is_pending_death_link_reset = True
            ctx.game_interface.kill_player()
            ctx.queued_deaths -= 1
    else:
        if not ctx.is_pending_death_link_reset:
            await ctx.send_death(ctx.player_names[ctx.slot] + " ran out of Nanotech.")
            ctx.is_pending_death_link_reset = True


async def _handle_game_ready(ctx: Rac2Context):
    if ctx.is_loading:
        if not ctx.game_interface.is_loading():
            ctx.is_loading = False
            #current_planet = ctx.game_interface.get_current_planet()
            #if current_planet is not None:
            #    logger.info(f"Loaded planet {current_planet} ({current_planet.name})")
            await asyncio.sleep(1)
        await asyncio.sleep(0.1)
        return
    elif ctx.game_interface.is_loading():
        #ctx.game_interface.logger.info("Waiting for planet to load...")
        ctx.is_loading = True
        return

    connected_to_server = (ctx.server is not None) and (ctx.slot is not None)
    if ctx.current_planet != ctx.game_interface.get_current_planet() and connected_to_server:
        ctx.previous_planet = ctx.current_planet
        ctx.current_planet = ctx.game_interface.get_current_planet()
        init(ctx)
    update(ctx, connected_to_server)

    if ctx.server:
        ctx.last_error_message = None
        if not ctx.slot:
            await asyncio.sleep(1)
            return

        current_inventory = ctx.game_interface.get_current_inventory()
        if ctx.current_planet is not None and ctx.current_planet > 0 and ctx.game_interface.get_pause_state() in [0, 5]:
            await handle_received_items(ctx, current_inventory)
        if ctx.current_planet and ctx.current_planet > 0:
            await handle_checked_location(ctx)
        await handle_check_goal_complete(ctx)

        if ctx.death_link_enabled:
            await handle_deathlink(ctx)
        await asyncio.sleep(0.1)
    else:
        message = "Waiting for player to connect to server"
        if ctx.last_error_message is not message:
            logger.info("Waiting for player to connect to server")
            ctx.last_error_message = message
        await asyncio.sleep(1)


async def _handle_game_not_ready(ctx: Rac2Context):
    """If the game is not connected, this will attempt to retry connecting to the game."""
    ctx.game_interface.connect_to_game()
    await asyncio.sleep(3)


async def run_game(iso_file):
    auto_start = get_settings().rac2_options.get("iso_start", True)

    if auto_start is True:
        import webbrowser
        webbrowser.open(iso_file)
    elif os.path.isfile(auto_start):
        subprocess.Popen([auto_start, iso_file, "-batch"],
                         stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


async def patch_and_run_game(aprac2_file: str):
    """Patch ISO if needed, ensure copied INI has correct PINE configuration, and launch game."""
    settings: Optional[Rac2Settings] = get_settings().get("rac2_options", False)
    assert settings, "No Rac2 Settings?"

    aprac2_file = os.path.abspath(aprac2_file)
    base_name = os.path.splitext(aprac2_file)[0]
    output_path = base_name + '.iso'

    # Patch ISO if missing
    if not os.path.exists(output_path):
        from .PatcherUI import PatcherUI
        patcher = PatcherUI(aprac2_file, output_path, logger)
        await patcher.async_run()
        if patcher.errored:
            raise Exception("Patching Failed")

    game_ini_path: str = settings.game_ini
    if os.path.exists(game_ini_path):
        version = Rac2ProcedurePatch.get_game_version_from_iso(output_path)
        crc = get_pcsx2_crc(output_path)
        if version and crc:
            file_name = f"{version}_{crc:X}.ini"
            file_path = os.path.join(os.path.dirname(game_ini_path), file_name)

            # Always create or refresh a CRC-based ini copy
            shutil.copy(game_ini_path, file_path)
            ensure_pine_settings(file_path, pine_port)

            logger.info(f"Configured PINE (port {pine_port}) in {os.path.basename(file_path)}")
    else:
        logger.warning("No valid game_ini found; skipping INI setup.")

    Utils.async_start(run_game(output_path))


def get_name_from_aprac2(aprac2_path: str) -> str:
    with zipfile.ZipFile(aprac2_path) as zip_file:
        with zip_file.open("archipelago.json") as file:
            archipelago_json = file.read().decode("utf-8")
            archipelago_json = json.loads(archipelago_json)
    return cast(Dict[str, Any], archipelago_json)["player_name"]

def get_connection_info_from_aprac2(aprac2_path: str) -> Optional[str]:
    try:
        with zipfile.ZipFile(aprac2_path) as zip_file:
            with zip_file.open("archipelago.json") as file:
                archipelago_json = json.loads(file.read().decode("utf-8"))

        server = archipelago_json.get("server")

        if not server:
            return None

        # Already includes port (new WebHost format)
        if ":" in server:
            return server

        # Older format fallback
        port = archipelago_json.get("port")
        if port:
            return f"{server}:{port}"

    except Exception as e:
        logger.debug(f"No valid connection info in patch: {e}")

    return None


def get_pcsx2_crc(iso_path: str) -> Optional[int]:
    if not os.path.exists(iso_path):
        return False

    ELF_START: int = 0x00258800
    ELF_SIZE: int = 0x27F53C
    crc: int = 0
    with open(iso_path, "rb") as iso_file:
        iso_file.seek(ELF_START)
        for i in range(int(ELF_SIZE / 4)):
            crc ^= int.from_bytes(iso_file.read(4), "little")

    return crc

def launch():
    Utils.init_logging("RAC2 Client")

    async def main():
        multiprocessing.freeze_support()
        logger.info("main")
        parser = get_base_parser()
        parser.add_argument('aprac2_file', default="", type=str, nargs="?",
                            help='Path to an aprac2 file')
        args = parser.parse_args()

        connect_address = args.connect
        
        # If no manual connect address, try to get from patch file
        if not connect_address and args.aprac2_file and os.path.isfile(args.aprac2_file):
            connect_address = get_connection_info_from_aprac2(args.aprac2_file)
            if connect_address:
                logger.info(f"Auto-connect address found in patch: {connect_address}")
        
        ctx = Rac2Context(connect_address, args.password)

        if os.path.isfile(args.aprac2_file):
            logger.info("aprac2 file supplied, beginning patching process...")
            await patch_and_run_game(args.aprac2_file)
            ctx.auth = get_name_from_aprac2(args.aprac2_file)

        logger.info("Connecting to server...")
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="Server Loop")

        if tracker_loaded:
            ctx.run_generator()
            ctx.tags.remove("Tracker")

        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        logger.info("Running game...")
        ctx.pcsx2_sync_task = asyncio.create_task(pcsx2_sync_task(ctx), name="PCSX2 Sync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.pcsx2_sync_task:
            await asyncio.sleep(3)
            await ctx.pcsx2_sync_task

    import colorama

    colorama.init()

    asyncio.run(main())
    colorama.deinit()


if __name__ == '__main__':
    launch()

# Install the bundled (forked) dolphin_memory_engine before ANY dme import,
# then import it eagerly here. The client is only ever imported when actually
# running the connector (never during generation/patching), so this is the
# right place for the native load to happen and to surface a clean error if
# the binary can't load. We publish the module onto TTYDPatcher so that
# .ttyd_runtime's `from .TTYDPatcher import dolphin` (run during the import
# below) binds the real module without a circular import.
from . import TTYDPatcher
TTYDPatcher.setup_dme_path()
import dolphin_memory_engine_ttyd as dolphin
TTYDPatcher.dolphin = dolphin

import asyncio
import struct
import subprocess
import traceback
import typing
import settings
import Patch
import Utils
from CommonClient import ClientCommandProcessor, get_base_parser, gui_enabled, logger, server_loop
from NetUtils import NetworkItem, ClientStatus
from . import Ghosts
from .Data import location_gsw_info, location_to_unit, GSWType
from .Items import items_by_id

from .ttyd_runtime import (
    _on_ghost_disconnect,
    _on_inbound_hit,
    _vlink_on_bounce,
    _vlink_send_part,
    vlink_force_presence,
    ttyd_ghost_sync_task,
)


RECEIVED_INDEX = 0x803DB860
RECEIVED_ITEM_ARRAY = 0x80001000
RECEIVED_LENGTH = 0x80000FFC
SEED = 0x80003210
GP_BASE = 0x803DAC18
GSWF_BASE = 0x178
GSW0 = 0x174
GSW_BASE = 0x578
ROOM = 0x803DF728
GAME_ID_ADDRESS = 0x80000000
EXPECTED_GAME_ID = b"G8ME01"

RECV_FLAG_RING = 0x80004600
RECV_FLAG_HEAD = RECV_FLAG_RING + 0x0
RECV_FLAG_TAIL = RECV_FLAG_RING + 0x2
RECV_FLAG_EVENTS = RECV_FLAG_RING + 0x4
RECV_FLAG_CAPACITY = 64

def _check_universal_tracker_version() -> bool:
    import re
    if tracker_loaded:
        match = re.search(r"v\d+.(\d+).(\d+)", UT_VERSION)
        if len(match.groups()) < 2:
            return False
        if int(match.groups()[0]) < 2:
            return False
        if int(match.groups()[1]) < 12:
            return False
        return True
    return False
tracker_loaded = False
try:
    from worlds.tracker.TrackerClient import TrackerGameContext as cmmCtx, UT_VERSION
    tracker_loaded = True
except ModuleNotFoundError:
    from CommonClient import CommonContext as cmmCtx
    tracker_loaded = False

def validate_connection() -> bool:
    """Verify DME is hooked to TTYD by checking the GameCube disc Game ID in memory."""
    try:
        game_id = dolphin.read_bytes(GAME_ID_ADDRESS, 6)
        return game_id == EXPECTED_GAME_ID
    except Exception:
        return False

def read_string(address: int, length: int):
    try:
        return dolphin.read_bytes(address, length).decode().strip("\0")
    except Exception as e:
        logger.error(f"Error reading string from address {hex(address)}: {e}")
        return ""

def get_rom_item_id(item: NetworkItem):
    return items_by_id[item.item].rom_id

def _get_bit_address(bit_number: int) -> tuple:
    word_index = bit_number >> 5
    bit_position = bit_number & 0x1F
    word_address = GP_BASE + (word_index * 4) + GSWF_BASE
    byte_within_word = 3 - (bit_position >> 3)
    byte_address = word_address + byte_within_word
    bit = bit_position & 0x7
    return byte_address, bit

def gswf_set(bit_number: int):
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    new_byte = current_byte | bit_mask
    dolphin.write_byte(byte_address, new_byte)
    return result

def gswf_check(bit_number: int) -> bool:
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    return bool(current_byte & bit_mask)

def gswf_clear(bit_number: int):
    """Clear a single GSWF bit (set to 0). Sibling to gswf_set."""
    result = _get_bit_address(bit_number)
    if not result: return False
    byte_address, bit = result
    current_byte = dolphin.read_byte(byte_address)
    bit_mask = 1 << bit
    new_byte = current_byte & ~bit_mask & 0xFF
    dolphin.write_byte(byte_address, new_byte)
    return result

def gsw_set(index, value):
    dolphin.write_word(GP_BASE + GSW0, value) if index == 0 else dolphin.write_byte(GP_BASE + index + GSW_BASE, value)

def gsw_check(index):
    return dolphin.read_word(GP_BASE + GSW0) if index == 0 else dolphin.read_byte(GP_BASE + index + GSW_BASE)


class TTYDCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx):
        super().__init__(ctx)


    def _cmd_ghost(self, *args):
        """Manage ghost peer settings.

        Subcommands:
          /ghost names [on|off|toggle]     - hide/show your name tag
          /ghost name [text]               - set your ghost display name (blank to clear)
          /ghost test [on|off|toggle]      - single-client loopback test ghost
        """
        if not args:
            logger.info("ghost: subcommands - names, name, test")
            return
        sub = args[0].strip().lower()
        rest = args[1:]
        if sub == "names":
            self._ghost_names(*rest)
        elif sub == "name":
            self._ghost_name(*rest)
        elif sub == "test":
            self._ghost_test(*rest)
        else:
            logger.info(f"ghost: unknown subcommand '{sub}'. Use names, name, test.")



    def _cmd_gswf(self, *args):
        """Manipulate GSWF (global state word flag) bits. Debug only.

        Subcommands:
          /gswf set <bit_number>
          /gswf check <bit_number>
        """
        if not args:
            logger.info("gswf: subcommands - set / check")
            return
        sub = args[0].strip().lower()
        rest = args[1:]
        if sub == "set":
            if not rest:
                logger.info("gswf: usage: /gswf set <bit_number>")
                return
            self._gswf_set(rest[0])
        elif sub == "check":
            if not rest:
                logger.info("gswf: usage: /gswf check <bit_number>")
                return
            self._gswf_check(rest[0])
        else:
            logger.info(f"gswf: unknown subcommand '{sub}'. Use set/check.")

    def _cmd_gsw(self, *args):
        """Manipulate GSW (global state word) values. Debug only.

        Subcommands:
          /gsw set <index> <value>
          /gsw check <index>
        """
        if not args:
            logger.info("gsw: subcommands - set / check")
            return
        sub = args[0].strip().lower()
        rest = args[1:]
        if sub == "set":
            if len(rest) < 2:
                logger.info("gsw: usage: /gsw set <index> <value>")
                return
            self._gsw_set(rest[0], rest[1])
        elif sub == "check":
            if not rest:
                logger.info("gsw: usage: /gsw check <index>")
                return
            self._gsw_check(rest[0])
        else:
            logger.info(f"gsw: unknown subcommand '{sub}'. Use set/check.")


    def _gswf_set(self, bit_number: int):
        """Used to manually set a GSWF bit."""
        byte_address, bit = gswf_set(int(bit_number))
        logger.info(f"Bit {bit} written at {byte_address}")

    def _gswf_check(self, bit_number: int):
        """Used to manually check a GSWF bit."""
        result = gswf_check(int(bit_number))
        logger.info(f"GSWF Check: 0x{format(result, 'x')}")

    def _gsw_set(self, gsw: int, value: int):
        """Used to manually set a GSW flag."""
        gsw_set(int(gsw), int(value))

    def _gsw_check(self, gsw: int):
        """Used to manually check a GSW flag."""
        result = gsw_check(int(gsw))
        logger.info(f"GSWF Check: {result}")

    def _ghost_names(self, mode: str = "toggle"):
        """Toggle ghost name tags. Affects both what you see (other
        players' name tags above their ghosts) and what others see of
        you (your name tag above your ghost on their screens). Defaults
        ON each session; not persisted across reconnect.

        Usage: /ghost_names         - toggle current state
               /ghost_names on      - force on
               /ghost_names off     - force off
        """
        ctx = self.ctx
        m = (mode or "toggle").strip().lower()
        cur_hidden = getattr(ctx, "_ghost_names_hidden", False)
        if m in ("on", "show", "1", "true"):
            new_hidden = False
        elif m in ("off", "hide", "0", "false"):
            new_hidden = True
        elif m in ("toggle", "t", ""):
            new_hidden = not cur_hidden
        else:
            logger.info(f"ghost_names: unknown mode '{mode}'. Use on/off/toggle.")
            return

        ctx._ghost_names_hidden = new_hidden

        try:
            vlink_force_presence(ctx)
        except Exception:
            pass

        logger.info(f"Ghost name tags {'OFF' if new_hidden else 'ON'} "
                    f"(both your view and peers' view of you).")

    def _ghost_name(self, *parts):
        """Set the display name shown above your ghost on other players'
        screens. Useful when two clients share one AP slot (co-op) so
        peers can tell them apart. Blank clears the override and falls
        back to the AP slot name. Not persisted across reconnect.

        Usage: /ghost name Luigi     - set display name to "Luigi"
               /ghost name           - clear override (use slot name)
        """
        ctx = self.ctx
        name = " ".join(parts).strip()[:16]
        ctx._ghost_display_name = name or None
        try:
            vlink_force_presence(ctx)
        except Exception:
            pass
        if name:
            logger.info(f"Ghost display name set to '{name}'.")
        else:
            logger.info("Ghost display name cleared (using slot name).")

    """def _ghost_test(self, mode: str = "toggle"):
        Single-client loopback: spawn a copy of your own Mario as a
        ghost ~100 units to your right so you can verify ghost rendering
        without a second client. Not persisted across reconnect.

        Usage: /ghost test          - toggle
               /ghost test on       - force on
               /ghost test off      - force off
        ctx = self.ctx
        m = (mode or "toggle").strip().lower()
        cur = getattr(ctx, "_ghost_test", False)
        if m in ("on", "1", "true"):
            new = True
        elif m in ("off", "0", "false"):
            new = False
        elif m in ("toggle", "t", ""):
            new = not cur
        else:
            logger.info(f"ghost test: unknown mode '{mode}'. Use on/off/toggle.")
            return
        ctx._ghost_test = new
        logger.info(f"Ghost test loopback {'ON' if new else 'OFF'}.")"""


class TTYDContext(cmmCtx):
    command_processor = TTYDCommandProcessor
    game = "Paper Mario: The Thousand-Year Door"
    tags = {"AP", Ghosts.VLINK_TAG}
    dolphin_connected: bool = False
    seed_verified: bool = False
    slot_data: dict | None = {}
    checked_locations = set()
    previous_room = None
    death_sent: bool = False

    _ghost_subscribed: bool = False
    _ghost_peers: dict = {}

    _ghost_addrs: typing.Optional[dict] = None

    def __init__(self, server_address, password):
        super().__init__(server_address, password)
        self.items_handling = 0b101
        self._pushed_recv_flags = set()

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(TTYDContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd in {"Connected"}:
            self.slot = args["slot"]
            self.slot_data = args["slot_data"]
            self.team = args["team"]
            self._ghost_multiplayer = bool(self.slot_data.get("multiplayer", 1))
            if not self._ghost_multiplayer:
                if Ghosts.VLINK_TAG in self.tags:
                    self.tags = set(self.tags) - {Ghosts.VLINK_TAG}
                    Utils.async_start(self.send_msgs([{"cmd": "ConnectUpdate", "tags": list(self.tags)}]))
            if "remote_items" not in self.slot_data:
                logger.warning("slot_data has no 'remote_items' key - seed was generated "
                               "with an older apworld; remote items will not work until regenerated.")
            items_handling = 0b101 | (0b010 if self.slot_data.get("remote_items") else 0)
            if items_handling != self.items_handling:
                self.items_handling = items_handling
                Utils.async_start(self.send_msgs([{"cmd": "ConnectUpdate", "items_handling": items_handling}]))
            if "death_link" in args["slot_data"]:
                Utils.async_start(self.update_death_link(bool(args["slot_data"]["death_link"])))
        elif cmd == "RoomInfo":
            self.seed_name = args["seed_name"]
        elif cmd == "Bounced":
            data = args.get("data") or {}
            if data.get("ttyd_hit") is True:
                _on_inbound_hit(self, data)
            elif data.get(Ghosts.VLINK_KIND) is not None:
                _vlink_on_bounce(self, data)

    def on_deathlink(self, data: typing.Dict[str, typing.Any]) -> None:
        super().on_deathlink(data)
        trigger_death(self)

    async def disconnect(self, allow_autoreconnect: bool = False):
        try:
            await _vlink_send_part(self)
        except Exception:
            pass
        await super().disconnect()
        self.slot = None
        self.slot_data = None
        self.team = None
        self.checked_locations = set()
        self.seed_name = None
        self.seed_verified = False
        self._pushed_recv_flags = set()
        _on_ghost_disconnect(self)

    def make_gui(self) -> "type[kvui.GameManager]":
        from kvui import GameManager
        class TTYDManager(GameManager):
            logging_pairs = [("Client", "Archipelago")]
            base_title = "Archipelago TTYD Client"
        if not _check_universal_tracker_version():
            return TTYDManager
        class TrackerManager(super().make_gui()):
            logging_pairs = [("Client", "Archipelago")]
            base_title = f"Archipelago TTYD Client with {UT_VERSION}"
        return TrackerManager

    async def receive_items(self):
        current_length = dolphin.read_word(RECEIVED_LENGTH)
        index = dolphin.read_word(RECEIVED_INDEX)
        if current_length != 0:
            return
        if index > len(self.items_received):
            return
        items = min(len(self.items_received) - index, 255)
        if items <= 0:
            return
        item_ids = [get_rom_item_id(self.items_received[i]) for i in range(index, index + items)]
        packed_data = struct.pack(f'>{len(item_ids)}H', *item_ids)
        dolphin.write_bytes(RECEIVED_ITEM_ARRAY, packed_data)
        dolphin.write_word(RECEIVED_LENGTH, items)

    def _push_recv_flag(self, flag: int) -> bool:
        try:
            head = struct.unpack(">H", dolphin.read_bytes(RECV_FLAG_HEAD, 2))[0]
            tail = struct.unpack(">H", dolphin.read_bytes(RECV_FLAG_TAIL, 2))[0]
            next_head = (head + 1) & 0xFFFF
            if next_head == tail:
                return False  # ring full
            slot = head % RECV_FLAG_CAPACITY
            dolphin.write_bytes(RECV_FLAG_EVENTS + slot * 2, struct.pack(">H", flag & 0xFFFF))
            dolphin.write_bytes(RECV_FLAG_HEAD, struct.pack(">H", next_head))
            return True
        except Exception:
            logger.error(traceback.format_exc())
            return False

    async def set_received_item_flags(self):
        if not self.slot_data.get("remote_items"):
            return
        for item in self.items_received:
            if item.player != self.slot:
                continue
            info = location_gsw_info.get(item.location)
            if info is None or info[0] != GSWType.GSWF:
                continue
            flag = info[1]
            # Tattle locations don't use the placeholder flag stored in
            # location_gsw_info; the game tracks them at 0x117A + unit_id.
            # Mirror the translation done in check_ttyd_locations so we push
            # the real in-game GSWF bit, not the AP-internal placeholder.
            if 78780850 <= item.location <= 78780973:
                flag = 0x117A + location_to_unit[item.location][0]
            if flag <= 0:
                continue  # no valid flag to set; never push 0 into the ring
            if flag in self._pushed_recv_flags:
                continue
            if gswf_check(flag):
                self._pushed_recv_flags.add(flag)  # already set in-game
                continue
            if self._push_recv_flag(flag):
                self._pushed_recv_flags.add(flag)
            else:
                break  # ring full; retry remaining flags next tick

    async def check_ttyd_locations(self):
        locations_to_send = set()
        try:
            for location, gsw_info in location_gsw_info.items():
                gsw_type, offset, value = gsw_info
                if offset == 0:
                    continue
                if 78780850 <= location <= 78780973:
                    offset = 0x117A + location_to_unit[location][0]
                if gsw_type.value == 0:
                    if gsw_check(offset) >= value:
                        locations_to_send.add(location)
                elif gsw_type.value == 1:
                    if gswf_check(offset):
                        locations_to_send.add(location)
            if len(locations_to_send) > 0:
                self.checked_locations &= locations_to_send
                await self.send_msgs([{"cmd": 'LocationChecks', "locations": locations_to_send}])
        except Exception as e:
            logger.error(traceback.format_exc())

    async def check_death(self):
        death_byte = dolphin.read_byte(0x80003240)
        if death_byte > 1:
            return
        if death_byte == 1:
            dolphin.write_byte(0x80003240, 0)
            if not self.death_sent:
                await self.send_death(self.player_names[self.slot] + " had no life shrooms.")
            self.death_sent = False

    def save_loaded(self) -> bool:
        value = dolphin.read_byte(0x80003228)
        if value > 1:
            return False
        return value > 0


def _dolphin_sys_gamesettings_dir(dolphin_path: str) -> str:
    """Resolve <Dolphin install>/Sys/GameSettings from the same path used to
    launch the emulator. We don't run the exe for this - we just walk from it
    to the Sys folder that ships beside it (inside the .app bundle on macOS)."""
    import os
    import sys

    exe_dir = os.path.dirname(os.path.abspath(dolphin_path))

    if sys.platform == "darwin":
        # dolphin_path may be the .app bundle itself or the inner binary.
        app = os.path.abspath(dolphin_path)
        while app and not app.endswith(".app"):
            parent = os.path.dirname(app)
            if parent == app:
                app = ""
                break
            app = parent
        if app:
            return os.path.join(app, "Contents", "Resources", "Sys", "GameSettings")
        # Fall through to exe-relative if not a bundle.

    return os.path.join(exe_dir, "Sys", "GameSettings")



def _apply_dolphin_game_settings(dolphin_path: str) -> None:
    import os

    core_settings = {
        "MMU": "True",
        "RAMOverrideEnable": "True",
        "MEM1Size": "67108864",  # 0x04000000 = 64 MB
    }
    try:
        ini_path = os.path.join(_dolphin_sys_gamesettings_dir(dolphin_path), "G8ME01.ini")
        os.makedirs(os.path.dirname(ini_path), exist_ok=True)

        lines = []
        if os.path.isfile(ini_path):
            with open(ini_path, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()

        core_start = -1
        core_end = -1   # index of the line after [Core]'s last entry
        key_idx = {}    # lower-cased [Core] key -> line index
        current = None
        for idx, line in enumerate(lines):
            s = line.strip()
            if s.startswith("[") and s.endswith("]"):
                if current == "core":
                    core_end = idx
                current = s[1:-1].strip().lower()
                if current == "core":
                    core_start = idx
            elif current == "core" and "=" in s:
                key_idx[s.split("=", 1)[0].strip().lower()] = idx
        if core_start != -1 and core_end == -1:
            core_end = len(lines)

        if core_start == -1:
            if lines and lines[-1].strip():
                lines.append("")
            lines.append("[Core]")
            for k, v in core_settings.items():
                lines.append(f"{k} = {v}")
        else:
            for k, v in core_settings.items():
                existing = key_idx.get(k.lower(), -1)
                if existing != -1:
                    lines[existing] = f"{k} = {v}"
                else:
                    lines.insert(core_end, f"{k} = {v}")
                    core_end += 1

        with open(ini_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")
        logger.info(f"Applied G8ME01 Dolphin settings (MMU + 64MB MEM1) in {ini_path}")
    except Exception:
        logger.warning("Could not auto-apply Dolphin game settings (MMU + 64MB MEM1 "
                       "override). Set them manually: right-click the game in Dolphin > "
                       "Properties > Advanced (Enable MMU, and the memory size override).",
                       exc_info=True)


async def _run_game(rom: str):
    import os
    import sys
    auto_start = settings.get_settings().ttyd_options.rom_start

    if auto_start is True:
        dolphin_path = settings.get_settings().ttyd_options.dolphin_path
        exec_arg = f"--exec={os.path.realpath(rom)}"

        if sys.platform == "darwin" and dolphin_path.endswith(".app"):
            inner = os.path.join(dolphin_path, "Contents", "MacOS", "Dolphin")
            if os.path.isfile(inner):
                cmd = [inner, exec_arg]
            else:
                cmd = ["open", "-a", dolphin_path, "--args", exec_arg]
        else:
            cmd = [dolphin_path, exec_arg]

        subprocess.Popen(
            cmd,
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
async def _patch_and_run_game(patch_file: str):
    metadata, output_file = Patch.create_rom_file(patch_file)
    Utils.async_start(_run_game(output_file))
    return metadata

def _installed_world_version():
    """world_version of the apworld currently running this client."""
    import pkgutil
    import json
    try:
        data = pkgutil.get_data(__name__, "archipelago.json")
        if data is None:
            return None
        return json.loads(data.decode("utf-8")).get("world_version")
    except Exception:
        return None


def _patch_world_version(patch_file: str):
    """world_version that was baked into the patch's options.json at generation.
    The .apttyd is a zip archive; read the member directly without patching."""
    import zipfile
    import json
    try:
        with zipfile.ZipFile(patch_file) as zf:
            with zf.open("options.json") as f:
                return json.loads(f.read().decode("utf-8")).get("world_version")
    except Exception:
        return None


async def ttyd_sync_task(ctx: TTYDContext):
    if getattr(ctx, "patch_provided", False):
        patch_version = getattr(ctx, "patch_world_version", None)
        current_version = _installed_world_version()
        if patch_version is None:
            logger.warning("This patch is missing a world version - it was generated with an "
                           "older apworld. The client will still connect, but behavior may be "
                           "incorrect; regenerate with a matching apworld if you hit issues.")
        elif current_version is not None and patch_version != current_version:
            logger.warning(f"Patch world version ({patch_version}) does not match the installed "
                           f"apworld version ({current_version}). The client will still connect, "
                           f"but behavior may be incorrect; use the matching apworld version or "
                           f"regenerate your patch if you hit issues.")
    logger.info("Starting Dolphin connector...")
    while not ctx.exit_event.is_set():
        try:
            hooked = dolphin.is_hooked()
        except Exception:
            logger.error(traceback.format_exc())
            logger.info("Dolphin memory engine unavailable; retrying...")
            ctx.dolphin_connected = False
            await asyncio.sleep(3)
            continue
        if hooked and ctx.dolphin_connected:
            if ctx.slot:
                try:
                    if not validate_connection():
                        logger.info("TTYD is no longer running. Disconnecting from Dolphin.")
                        try:
                            await _vlink_send_part(ctx)
                        except Exception:
                            pass
                        dolphin.un_hook()
                        ctx.dolphin_connected = False
                        ctx.seed_verified = False
                        await asyncio.sleep(3)
                        continue
                    if not ctx.seed_verified:
                        logger.info("Checking ROM seed...")
                        seed = read_string(SEED, 0x10)
                        if seed not in ctx.seed_name:
                            logger.info(ctx.seed_name)
                            await ctx.disconnect()
                            logger.info("ROM Seed does not match Room seed. Please make sure you are using the correct patch.")
                            dolphin.un_hook()
                            await asyncio.sleep(3)
                            continue
                        ctx.seed_verified = True
                        logger.info("ROM Seed verified successfully.")
                    if "DeathLink" in ctx.tags:
                        await ctx.check_death()
                    if not ctx.save_loaded():
                        await asyncio.sleep(0.5)
                        continue
                    current_room = read_string(ROOM, 6)
                    if ctx.previous_room != current_room:
                        ctx.previous_room = current_room
                        await ctx.send_msgs([{
                            "cmd": "Set",
                            "key": f"ttyd_room_{ctx.team}_{ctx.slot}",
                            "default": 0,
                            "want_reply": False,
                            "operations": [{"operation": "replace", "value": current_room}]
                        }])
                    await ctx.receive_items()
                    await ctx.set_received_item_flags()
                    await ctx.check_ttyd_locations()
                    goal = ctx.slot_data.get("goal", 0)
                    if goal == 1: # Shadow Queen
                        if not ctx.finished_game and gsw_check(1708) >= 18:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    elif goal == 2: # Crystal Stars
                        star_count = dolphin.read_byte(0x8000323B)
                        if not ctx.finished_game and star_count <= 7 and star_count >= ctx.slot_data["goal_stars"]:
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    else:
                        if not ctx.finished_game and gswf_check(5085):
                            await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                    await asyncio.sleep(.5)
                except Exception as e:
                    logger.info(traceback.format_exc())
                    dolphin.un_hook()
                    ctx.dolphin_connected = False
                    await asyncio.sleep(1)
            else:
                await asyncio.sleep(1)
        else:
            try:
                logger.info("Attempting to connect to Dolphin...")
                dolphin.hook()
                if not dolphin.is_hooked():
                    logger.info("Connection to Dolphin failed... Attempting again")
                    ctx.dolphin_connected = False
                    await ctx.disconnect()
                    await asyncio.sleep(3)
                    continue
                if not validate_connection():
                    logger.info("Dolphin hooked but TTYD is not running. "
                                "Please load Paper Mario: The Thousand-Year Door.")
                    dolphin.un_hook()
                    ctx.dolphin_connected = False
                    await asyncio.sleep(5)
                    continue
                logger.info("Dolphin connected successfully.")
                ctx.dolphin_connected = True
            except Exception as e:
                dolphin.un_hook()
                logger.info("Connection to Dolphin failed... Attempting again")
                logger.error(traceback.format_exc())
                ctx.dolphin_connected = False
                await ctx.disconnect()
                await asyncio.sleep(3)
                continue


def trigger_death(ctx):
    try:
        if ctx.slot is not None and dolphin.is_hooked() and ctx.dolphin_connected and validate_connection():
            ctx.death_sent = True
            dolphin.write_byte(0x8000323F, 1)
    except Exception:
        logger.exception("trigger_death: write failed")


def launch(*args):
    async def main(args):
        try:
            _apply_dolphin_game_settings(settings.get_settings().ttyd_options.dolphin_path)
        except Exception:
            pass
        if args.patch_file:
            await asyncio.create_task(_patch_and_run_game(args.patch_file))
        ctx = TTYDContext(args.connect, args.password)
        ctx.patch_world_version = None
        ctx.patch_provided = bool(args.patch_file)
        if args.patch_file:
            ctx.patch_world_version = _patch_world_version(args.patch_file)
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")
        if gui_enabled:
            if tracker_loaded:
                ctx.run_generator()
            ctx.run_gui()
        ctx.run_cli()
        ctx.gl_sync_task = asyncio.create_task(ttyd_sync_task(ctx), name="TTYD Sync Task")
        ctx.ghost_sync_task = asyncio.create_task(
            ttyd_ghost_sync_task(ctx), name="GhostSync")

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

    parser = get_base_parser()
    parser.add_argument("patch_file", default="", type=str, nargs="?", help="Path to an APTTYD file")
    args = parser.parse_args(args)

    import colorama

    colorama.just_fix_windows_console()
    asyncio.run(main(args))
    colorama.deinit()

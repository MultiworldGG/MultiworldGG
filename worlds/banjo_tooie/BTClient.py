import asyncio, hashlib, json, os, multiprocessing, copy, sys, time, atexit, pkgutil
import bsdiff4 # pyright: ignore[reportMissingTypeStubs]
from typing import TYPE_CHECKING, Any, List, TypedDict, cast
from collections import Counter
from dataclasses import dataclass


# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, gui_enabled, \
    ClientCommandProcessor, logger, get_base_parser
import Utils
from Utils import async_start, instance_name
apname = instance_name if instance_name else "Archipelago"

from . import BanjoTooieWorld
from .client import state as emu_state, game as emu_game, addresses as emu_addresses

# For when its a global package
try:
    from emu_loader import EmuLoaderClient, ProcessMemory
# For when its in the apworld itself
except ImportError:
    from .emu_loader import EmuLoaderClient, ProcessMemory

if TYPE_CHECKING:
    from kvui import UILog


# BTHACK signature validation
RDRAM_BASE = 0x80000000  # KSEG0 start; RDRAM mirror
RDRAM_SIZE = 0x800000  # 8 MB with expansion pak (required by BT)
BTHACK_ANCHOR_OFFSET = 0x400000  # physical RDRAM offset of AP_MEMORY_PTR
BTHACK_STRUCT_SIZE = 52
BTHACK_SUB_POINTER_OFFSETS = (
    0x04,  # pc
    0x08,  # pc_message
    0x0C,  # signpost_messages
    0x10,  # pc_settings
    0x14,  # pc_items
    0x18,  # pc_traps
    0x1C,  # pc_exit_map
    0x20,  # n64
    0x24,  # n64_saves_real
    0x28,  # n64_saves_fake
    0x2C,  # n64_saves_nests
    0x30,  # n64_saves_signposts
)


def is_rdram_pointer(value: int) -> bool:
    return RDRAM_BASE <= value < RDRAM_BASE + RDRAM_SIZE


class BTEmuLoaderClient(EmuLoaderClient):
    """EmuLoaderClient with BTHACK pointer-chase helpers."""

    def __init__(self) -> None:
        super().__init__(validation_func= validate_bt_signature)

    def deref(self, address: int) -> int | None:
        ptr = self.read_u32(address)
        return ptr & 0x7FFFFFFF if is_rdram_pointer(ptr) else None

    def get_anchor(self) -> int | None:
        return self.deref(RDRAM_BASE + BTHACK_ANCHOR_OFFSET)

    def get_rom_version(self) -> tuple[int, int, int] | None:
        anchor = self.get_anchor()
        if anchor is None:
            return None
        major = self.read_u16(RDRAM_BASE + anchor + 0x0)
        minor = self.read_u8(RDRAM_BASE + anchor + 0x2)
        patch = self.read_u8(RDRAM_BASE + anchor + 0x3)
        return (major, minor, patch)


def validate_bt_signature(pm: ProcessMemory, rdram_base: int) -> bool:
    """Return True if ``rdram_base`` looks like AP-Banjo-Tooie RDRAM.

    - u32 at ``rdram_base + 0x400000`` must be a valid 0x80xxxxxx pointer
      (BTHACK's ``AP_MEMORY_PTR``).
    - At the dereferenced ``ap_memory_ptr_t`` struct, all 12 sub-pointers
      at offsets 0x04..0x30 must themselves be valid RDRAM pointers. The
      patch's ``inject_hooks()`` populates every one of them at game boot.
    """
    try:
        anchor = int.from_bytes(
            pm.read_bytes(rdram_base + BTHACK_ANCHOR_OFFSET, 4), "little"
        )
    except Exception:
        return False
    if not is_rdram_pointer(anchor):
        return False
    physical = anchor & 0x7FFFFFFF
    if physical + BTHACK_STRUCT_SIZE > RDRAM_SIZE:
        return False
    try:
        struct_bytes = pm.read_bytes(rdram_base + physical, BTHACK_STRUCT_SIZE)
    except Exception:
        return False
    for offset in BTHACK_SUB_POINTER_OFFSETS:
        sub_ptr = int.from_bytes(struct_bytes[offset : offset + 4], "little")
        if not is_rdram_pointer(sub_ptr):
            return False
    return True

SYSTEM_MESSAGE_ID = 0

CONNECTION_TIMING_OUT_STATUS = "Connection timing out. Please restart your emulator (or banjo_tooie_connector if you're on real hardware)."
CONNECTION_REFUSED_STATUS = "Connection refused. Start your emulator (or banjo_tooie_connector for real hardware) and try again."
CONNECTION_RESET_STATUS = "Connection was reset. Please restart your emulator (or banjo_tooie_connector if you're on real hardware)."
CONNECTION_TENTATIVE_STATUS = "Initial Connection Made"
CONNECTION_CONNECTED_STATUS = "Connected"
CONNECTION_INITIAL_STATUS = "Connection has not been initiated"

# Payload: bridge -> client
# {
#     playerName: string,
#     locations: dict,
#     deathlinkActive: bool,
#     taglinkActive: bool,
#     isDead: bool,
#     isTag: bool,
#     gameComplete: bool
# }
#
# Payload: client -> bridge
# {
#     items: list,
#     playerNames: list,
#     triggerDeath: bool,
#     triggerTag: bool,
#     messages: string
# }
#
# Deathlink logic:
# "Dead" is true <-> Banjo is at 0 hp.
#
# deathlink_pending: we need to kill the player
# deathlink_sent_this_death: we interacted with the multiworld on this death, waiting to reset with living link

bt_loc_name_to_id = BanjoTooieWorld.location_name_to_id
bt_itm_name_to_id = BanjoTooieWorld.item_name_to_id
script_version: int = 5
version: str = BanjoTooieWorld.world_version.as_simple_string()
patch_md5: str = "8077f58d9d6cd9da6f4b4610d32aba25"
bt_options = BanjoTooieWorld.settings
program = None

def read_file(path: str) -> bytes:
  with open(path, "rb") as fi:
    data = fi.read()
  return data

def write_file(path: str, data: bytes):
  with open(path, "wb") as fi:
    fi.write(data)

def open_world_file(resource: str) -> bytes:
  assert __package__ is not None, "BTClient needs to be loaded as a package."
  ret = pkgutil.get_data(__package__, resource)
  assert ret is not None, f"Unable to find: {resource}"
  return ret

def patch_rom(rom_path: str, dst_path: str, patch_path: str):
  rom: bytes = read_file(rom_path)
  md5 = hashlib.md5(rom).hexdigest()
  if md5 == "ca0df738ae6a16bfb4b46d3860c159d9": # byte swapped
    swapped = bytearray(b'\0'*len(rom))
    for i in range(0, len(rom), 2):
      swapped[i] = rom[i+1]
      swapped[i+1] = rom[i]
    rom = bytes(swapped)
  elif md5 != "40e98faa24ac3ebe1d25cb5e5ddf49e4":
    logger.error(f"Unknown ROM! Please use /patch or restart the Banjo-Tooie Client to try again.")
    return False
  patch = open_world_file(patch_path)
  patched_rom = cast(bytes, bsdiff4.patch(rom, patch)) # pyright: ignore[reportUnknownMemberType]
  write_file(dst_path, patched_rom)
  lua = Utils.local_path("data", "lua", "BT_companion.lua")
  if os.access(os.path.split(lua)[0], os.W_OK):
      with open(lua, "w") as to:
          to.write(open_world_file("assets/BT_companion.lua").decode())
  return True

async def patch_and_run(show_path: bool):
  global program
  game_name = "Banjo-Tooie"
  patch_path = bt_options.get("patch_path", "")
  patch_name = f"{game_name} AP {version}.z64"
  if patch_path and os.access(patch_path, os.W_OK):
    patch_path = os.path.join(patch_path, patch_name)
  elif os.access(Utils.user_path(), os.W_OK):
    patch_path = Utils.user_path(patch_name)
  elif os.access(Utils.cache_path(), os.W_OK):
    patch_path = Utils.cache_path(patch_name)
  else:
    patch_path = None
  existing_md5 = None
  if patch_path and os.path.isfile(patch_path):
    rom = read_file(patch_path)
    existing_md5 = hashlib.md5(rom).hexdigest()
  await asyncio.sleep(0.01)
  patch_successful = True
  if not patch_path or existing_md5 != patch_md5:
    rom = bt_options.get("rom_path", "")
    if not rom or not os.path.isfile(rom):
      rom = Utils.open_filename(f"Open your {game_name} US ROM", (("Rom Files", (".z64", ".n64")), ("All Files", "*"),))
    if not rom:
      logger.error(f"No ROM selected. Please use /patch or restart the {game_name} Client to try again.")
      return
    if not patch_path:
      patch_path = os.path.split(rom)[0]
      if os.access(patch_path, os.W_OK):
        patch_path = os.path.join(patch_path, patch_name)
      else:
        logger.error(f"Unable to find writable path... Please use /patch or restart the {game_name} Client to try again.")
        return
    logger.info("Patching...")
    patch_successful = patch_rom(rom, patch_path, "assets/Banjo-Tooie.patch")
    if patch_successful:
      bt_options.rom_path = rom
      bt_options.patch_path = os.path.split(patch_path)[0]
    else:
      bt_options.rom_path = None
    bt_options._changed = True
  if patch_successful:
    if show_path:
      logger.info(f"Patched {game_name} is located here: {patch_path}")
    program_path = bt_options.get("program_path", "")
    if program_path and os.path.isfile(program_path) and (not program or program.poll() != None):
      import shlex, subprocess
      logger.info(f"Automatically starting {program_path}")
      args = [*shlex.split(program_path)]
      program_args = bt_options.program_args
      if program_args:
        args.append(program_args)
      args.append(patch_path)
      program = subprocess.Popen(
        args,
        cwd=Utils.local_path("."),
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
      )

class BanjoTooieClientTab:
    content: "UILog"

class BanjoTooieItemTracker:

  def __init__(self, ctx: "BanjoTooieContext"):
    self.ctx = ctx
    self.items: Counter[str] = Counter()
    self.refresh_items()

  def refresh_items(self):
    self.items.clear()
    for item in self.ctx.items_received:
      self.items[self.ctx.item_names.lookup_in_game(item.item)] += 1
    data: list[dict[str, str]] = []
    for item_name, amount in sorted(self.items.items()):
      if amount > 1: data.append({"text":f"{item_name}: {amount}"})
      else: data.append({"text":f"{item_name}"})
    self.ctx.tab_items.content.data = data

class BanjoTooieCommandProcessor(ClientCommandProcessor):
    def __init__(self, ctx: "BanjoTooieContext"):
        super().__init__(ctx)

    def _cmd_patch(self):
        """Reruns the patcher."""
        asyncio.create_task(patch_and_run(True))
        return True

    def _cmd_autostart(self):
        """Configure a program to automatically start with the client (e.g.
            launch your emulator with the patched ROM).
            If already configured, disables the configuration."""
        program_path = bt_options.get("program_path", "")
        if program_path == "" or not os.path.isfile(program_path):
            program_path = Utils.open_filename(f"Select your program to automatically start", (("All Files", "*"),))
            if program_path:
                bt_options.program_path = program_path
                bt_options._changed = True
                logger.info(f"Autostart configured for: {program_path}")
                if not program or program.poll() != None:
                    asyncio.create_task(patch_and_run(False))
            else:
                logger.error("No file selected...")
                return False
        else:
            bt_options.program_path = ""
            bt_options._changed = True
            logger.info("Autostart disabled.")
        return True

    def _cmd_rom_path(self, path: str = ""):
        """Sets (or unsets) the file path of the vanilla ROM used for patching."""
        bt_options.rom_path = path
        bt_options._changed = True
        if path:
            logger.info("rom_path set!")
        else:
            logger.info("rom_path unset!")
        return True

    def _cmd_patch_path(self, path: str = ""):
        """Sets (or unsets) the folder path of where to save the patched ROM."""
        bt_options.patch_path = path
        bt_options._changed = True
        if path:
            logger.info("patch_path set!")
        else:
            logger.info("patch_path unset!")
        return True

    def _cmd_program_args(self, path: str = ""):
        """Sets (or unsets) the arguments to pass to the automatically run program."""
        bt_options.program_args = path
        bt_options._changed = True
        if path:
            logger.info("program_args set!")
        else:
            logger.info("program_args unset!")
        return True

    def _cmd_n64(self):
        """Check N64 connection state (emu_loader + socket transports)."""
        if isinstance(self.ctx, BanjoTooieContext):
            logger.info(f"Emulator: {self.ctx.emu_status}")
            logger.info(f"Socket (EverDrive): {self.ctx.n64_status}")

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        if isinstance(self.ctx, BanjoTooieContext):
            self.ctx.deathlink_client_override = True
            self.ctx.deathlink_enabled = not self.ctx.deathlink_enabled
            async_start(self.ctx.update_death_link(self.ctx.deathlink_enabled), name="Update Deathlink")

    def _cmd_taglink(self):
        """Toggle taglink from client. Overrides default setting."""
        if isinstance(self.ctx, BanjoTooieContext):
            self.ctx.taglink_client_override = True
            self.ctx.taglink_enabled = not self.ctx.taglink_enabled
            async_start(self.ctx.update_tag_link(self.ctx.taglink_enabled), name="Update Taglink")

    def _cmd_writesettings(self):
        """Manually push slot settings into BTHACK memory via emu_loader (the ROM refuses to boot until settings are populated)."""
        if not isinstance(self.ctx, BanjoTooieContext):
            return
        ctx = self.ctx
        if ctx.emu_loader is None or not ctx.emu_loader.is_connected():
            return
        if not ctx.slot_data:
            return
        if emu_game.write_slot_settings(ctx.emu_loader, ctx.slot_data):
            ctx.emu_settings_written = True

@dataclass
class CreateHintsParams:
    location: int
    player: int

class BanjoTooieContext(CommonContext):
    command_processor = BanjoTooieCommandProcessor
    items_handling = 0b111 #full
    tab_items: BanjoTooieClientTab

    def __init__(self, server_address: str | None, password: str | None):
        super().__init__(server_address, password)
        self.game = "Banjo-Tooie"
        self.n64_streams: tuple[asyncio.StreamReader, asyncio.StreamWriter] | None = None
        self.n64_sync_task = None
        self.n64_status = CONNECTION_INITIAL_STATUS
        self.emu_loader: BTEmuLoaderClient | None = None
        self.emu_monitor_task: asyncio.Task | None = None
        self.emu_settings_written: bool = False
        self.emu_last_items_count: int = -1
        self.emu_sent_world_entrances: set[int] = set()
        self.emu_goal_printed: bool = False
        self.emu_waiting_logged: bool = False
        self.emu_attached_logged: bool = False
        self.emu_status: str = "Not attached"
        self.awaiting_rom = False
        self.location_table = {}
        self.movelist_table: dict[str, bool] = {}
        self.cheatorewardslist_table: dict[str, bool] = {}
        self.honeybrewardslist_table: dict[str, bool] = {}
        self.treblelist_table: dict[str, bool] = {}
        self.stationlist_table: dict[str, bool] = {}
        self.jinjofamlist_table: dict[str, bool] = {}
        self.jinjolist_table: dict[str, bool] = {}
        self.pages_table: dict[str, bool] = {}
        self.honeycomb_table: dict[str, bool] = {}
        self.glowbo_table: dict[str, bool] = {}
        self.doubloon_table: dict[str, bool] = {}
        self.notes_table: dict[str, bool] = {}
        self.worldlist_table: dict[str, bool] = {}
        self.chuffy_table: dict[str, bool] = {}
        self.mystery_table: dict[str, bool] = {}
        self.roystenlist_table: dict[str, bool] = {}
        self.jiggychunks_table: dict[str, bool] = {}
        self.goggles_table = False
        self.dino_kids_table: dict[str, bool] = {}
        self.boggy_kids_table: dict[str, bool] = {}
        self.alien_kids_table: dict[str, bool] = {}
        self.skivvies_table: dict[str, bool] = {}
        self.mr_fit_table: dict[str, bool] = {}
        self.bt_tickets_table: dict[str, bool] = {}
        self.green_relics_table: dict[str, bool] = {}
        self.beans_table: dict[str, bool] = {}
        self.signpost_table = {}
        self.warppads_table: dict[str, bool] = {}
        self.silos_table: dict[str, bool] = {}
        self.nests_table: dict[str, bool] = {}
        self.roar = False
        self.jiggy_table: dict[str, bool] = {}
        self.current_map = 0
        self.deathlink_enabled = False
        self.deathlink_pending = False
        self.deathlink_sent_this_death = False
        self.deathlink_client_override = False

        self.taglink_enabled = False
        self.pending_tag_link = False
        self.taglink_sent_this_tag = False
        self.taglink_client_override = False
        self.version_warning = False
        self.rom_version = ""
        self.messages: dict[int, dict[str, str | int] | str] = {}
        self.slot_data = {}
        self.sendSlot = False
        self.sync_ready = False
        self.startup = False
        self.handled_scouts: list[CreateHintsParams] = []

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super(BanjoTooieContext, self).server_auth(password_requested)
        if not self.auth:
            await self.get_username()
            await self.send_connect()
            self.awaiting_rom = True
            return
        return

    def set_message(self, msg: dict[str, str | int] | str):
        self.messages[len(self.messages)+1] = msg

    def on_deathlink(self, data: dict[str, Any]):
        self.deathlink_pending = True
        self.last_death_link = max(data["time"], self.last_death_link)
        text = data.get("cause", "")
        if text:
            logger.info(f"DeathLink: {text}")

    async def send_death(self, death_text: str = ""):
        if self.server and self.server.socket and self.slot is not None:
            logger.info(f"(DeathLink: Sending death to your friends...)")
            self.last_death_link = time.time()
            await self.send_msgs([{
                "cmd": "Bounce", "tags": ["DeathLink"],
                "data": {
                    "time": self.last_death_link,
                    "source": self.player_names[self.slot],
                    "cause": death_text
                }
            }])

    async def update_tag_link(self, tag_link: bool):
        """Helper function to set tag Link connection tag on/off and update the connection if already connected."""
        old_tags = self.tags.copy()
        if tag_link:
            self.tags.add("TagLink")
        else:
            self.tags -= {"TagLink"}
        if old_tags != self.tags and self.server and not self.server.socket.closed:
            await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

    async def send_tag_link(self):
        """Send a tag link message."""
        if "TagLink" not in self.tags or self.slot is None:
            return
        if not hasattr(self, "instance_id"):
            self.instance_id = time.time()
        await self.send_msgs([{"cmd": "Bounce", "tags": ["TagLink"],
             "data": {
                "time": time.time(),
                "source": self.instance_id,
                "tag": True}}])

    def run_gui(self):
        from kvui import GameManager, Window, UILog

        Window.bind(on_request_close=self.on_request_close) # pyright: ignore[reportArgumentType]
        asyncio.create_task(patch_and_run(True))

        class BanjoTooieManager(GameManager):
            ctx: BanjoTooieContext
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = "Banjo-Tooie Client "+ version + " for " + apname

            def build(self):
                ret = super().build()
                self.ctx.tab_items = cast(BanjoTooieClientTab, self.add_client_tab("Items", UILog()))
                return ret

        self.ui = BanjoTooieManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def on_request_close(self, *args: Any):
        from kvui import MessageBox

        title = "Warning: Autostart program still running!"
        message = "Attempting to close this window again will forcibly close it."
        def cleanup(messagebox: MessageBox):
            self._messagebox = None
        if self._messagebox and self._messagebox.title == title: # pyright: ignore[reportUnknownMemberType]
            return False
        if program and program.poll() == None:
            self.gui_error(title, message)
            if self._messagebox:
              self._messagebox.bind(on_dismiss=cleanup) # pyright: ignore[reportCallIssue]
            return True
        return False

    def on_package(self, cmd: str, args: dict[Any, Any]):
        if cmd == "Connected":
            self.tracker = BanjoTooieItemTracker(self)
            self.slot_data: dict[str, Any] = args.get("slot_data", {})
            assert self.slot_data, "This slot doesn't have any data..."
            slot_version = self.slot_data.get("custom_bt_data", {}).get("version", "N/A")
            assert version == slot_version, (
                "Your Banjo-Tooie AP does not match with the generated world.\n" +
                f"Your version: {version} | Generated version: {self.slot_data['custom_bt_data']['version']}"
            )
            if self.rom_version != "" and version != self.rom_version:
                assert False, (
                    f"ERROR: Your Patched ROM is version {self.rom_version}, expected {version}. " +
                    "Please update to the latest version. " +
                    f"Your connection to the {apname} server will not be accepted."
                )
            self.deathlink_enabled = bool(self.slot_data["options"]["death_link"])
            self.taglink_enabled = bool(self.slot_data["options"]["tag_link"])
            self.n64_sync_task = asyncio.create_task(n64_sync_task(self), name="N64 Sync")
        elif cmd == "ReceivedItems":
            self.tracker.refresh_items()
            if self.startup == False:
                for item in args["items"]:
                    player = ""
                    item_name = ""
                    for (i, name) in self.player_names.items():
                        if i == item.player:
                            player = name
                            break
                    for (name, i) in bt_itm_name_to_id.items():
                        if item.item == i:
                            item_name = name
                            break
                    logger.info(player + " sent " + item_name)
                logger.info("The above items will be sent when Banjo-Tooie is loaded.")
                self.startup = True
        if isinstance(args.get("data", {}), dict):
            source_name = args.get("data", {}).get("source", None)
            if not hasattr(self, "instance_id"):
                self.instance_id = time.time()
            if "TagLink" in self.tags and source_name != self.instance_id and "TagLink" in args.get("tags", []):
                if not hasattr(self, "pending_tag_link"):
                    self.pending_tag_link = False
                else:
                    self.pending_tag_link = True

    def on_print_json(self, args: dict[Any, Any]):
        if self.ui:
            self.ui.print_json(copy.deepcopy(args["data"]))
            relevant = args.get("type") == "ItemSend"
            if relevant:
                relevant = False
                item = args["item"]
                if self.slot_concerns_self(args["receiving"]): # pyright: ignore[reportUnknownMemberType]
                    relevant = True
                elif self.slot_concerns_self(item.player): # pyright: ignore[reportUnknownMemberType]
                    relevant = True

                if relevant == True:
                    player = self.player_names[int(args["data"][0]["text"])]
                    to_player = self.player_names[int(args["data"][0]["text"])]
                    for id, data in enumerate(args["data"]):
                        if id == 0:
                            continue
                        if "type" in data and data["type"] == "player_id":
                            to_player = self.player_names[int(data["text"])]
                            break
                    item_name = self.item_names.lookup_in_slot(int(args["data"][2]["text"]))
                    self.set_message({"player":player, "item":item_name, "item_id":int(args["data"][2]["text"]), "to_player":to_player })
        else:
            text = self.jsontotextparser(copy.deepcopy(args["data"]))
            logger.info(text)
            relevant = args.get("type") == "ItemSend"
            if relevant:
                player = self.player_names[int(args["data"][0]["text"])]
                to_player = self.player_names[int(args["data"][0]["text"])]
                for id, data in enumerate(args["data"]):
                        if id == 0:
                            continue
                        if "type" in data and data["type"] == "player_id":
                            to_player = self.player_names[int(data["text"])]
                            break
                item_name = self.item_names.lookup_in_slot(int(args["data"][2]["text"]))
                self.set_message({"player":player, "item":item_name, "item_id":int(args["data"][2]["text"]), "to_player":to_player})

def get_payload(ctx: BanjoTooieContext):
    if ctx.deathlink_enabled and ctx.deathlink_pending:
        trigger_death = True
        ctx.deathlink_sent_this_death = True
        ctx.deathlink_pending = False
    else:
        trigger_death = False

    if ctx.taglink_enabled and ctx.pending_tag_link:
        trigger_tag = True
        ctx.taglink_sent_this_tag = True
        ctx.pending_tag_link = False
    else:
        trigger_tag = False

    if ctx.sync_ready == True:
        ctx.startup = True
        payload = json.dumps({
                "items": [item.item for item in ctx.items_received],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "triggerTag": trigger_tag,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    else:
        payload = json.dumps({
                "items": [],
                "playerNames": [name for (i, name) in ctx.player_names.items() if i != 0],
                "triggerDeath": trigger_death,
                "triggerTag": trigger_tag,
                "messages": [message for (i, message) in ctx.messages.items() if i != 0],
            })
    if len(ctx.messages) > 0:
        ctx.messages = {}

    return payload

def get_slot_payload(ctx: BanjoTooieContext):
    payload = json.dumps({
            "slot_player": ctx.slot_data["custom_bt_data"]["player_name"],
            "slot_seed": ctx.slot_data["custom_bt_data"]["seed"],
            "slot_deathlink": ctx.deathlink_enabled,
            "slot_taglink": ctx.taglink_enabled,
            "slot_tower_of_tragedy": ctx.slot_data["options"]["tower_of_tragedy"],
            "slot_randomize_bk_moves": ctx.slot_data["options"]["randomize_bk_moves"],
            "slot_speed_up_minigames": ctx.slot_data["options"]["speed_up_minigames"],
            "slot_skip_puzzles": ctx.slot_data["options"]["skip_puzzles"],
            "slot_backdoors": ctx.slot_data["options"]["backdoors"],
            "slot_open_hag1": ctx.slot_data["options"]["open_hag1"],
            "slot_randomize_chuffy": ctx.slot_data["options"]["randomize_chuffy"],
            "slot_world_requirements": ctx.slot_data["custom_bt_data"]["world_requirements"], #??
            "slot_world_order": ctx.slot_data["custom_bt_data"]["world_order"], #??
            "slot_skip_klungo": ctx.slot_data["options"]["skip_klungo"],
            "slot_victory_condition": ctx.slot_data["options"]["victory_condition"],
            "slot_minigame_hunt_length": ctx.slot_data["options"]["minigame_hunt_length"],
            "slot_boss_hunt_length": ctx.slot_data["options"]["boss_hunt_length"],
            "slot_jinjo_family_rescue_length": ctx.slot_data["options"]["jinjo_family_rescue_length"],
            "slot_token_hunt_length": ctx.slot_data["options"]["token_hunt_length"],
            "slot_version": version,
            "slot_silo_costs": ctx.slot_data["custom_bt_data"]["jamjars_silo_costs"],
            "slot_preopened_silo": ctx.slot_data["custom_bt_data"]["preopened_silos_ids"],
            "slot_randomize_warp_pads": ctx.slot_data["options"]["randomize_warp_pads"],
            "slot_randomize_silos": ctx.slot_data["options"]["randomize_silos"],
            "slot_zones": ctx.slot_data["custom_bt_data"]["loading_zones"],
            "slot_dialog_character": ctx.slot_data["options"]["dialog_character"],
            "slot_nestsanity": ctx.slot_data["options"]["nestsanity"],
            "slot_hints": ctx.slot_data["custom_bt_data"]["hints"],
            "slot_hints_activated": ctx.slot_data["options"]["signpost_hints"],
            "slot_extra_cheats": ctx.slot_data["options"]["extra_cheats"],
            "slot_easy_canary": ctx.slot_data["options"]["easy_canary"],
            "slot_randomize_signposts": ctx.slot_data["options"]["randomize_signposts"],
            "slot_auto_enable_cheats": ctx.slot_data["options"]["auto_enable_cheats"],
            "slot_cheato_rewards": ctx.slot_data["options"]["cheato_rewards"],
            "slot_honeyb_rewards": ctx.slot_data["options"]["honeyb_rewards"],
            "slot_open_gi_entrance": ctx.slot_data["options"]["open_gi_frontdoor"],
            "slot_randomize_tickets": ctx.slot_data["options"]["randomize_tickets"],
            "slot_randomize_green_relics": ctx.slot_data["options"]["randomize_green_relics"],
            "slot_randomize_beans": ctx.slot_data["options"]["randomize_beans"]
        })
    ctx.sendSlot = False
    return payload

class Payload(TypedDict):
    playerName: str
    deathlinkActive: bool
    taglinkActive: bool
    DEMO: Any
    chuffy: dict[str, bool]
    treble: dict[str, bool]
    stations: dict[str, bool]
    mystery: dict[str, bool]
    roysten: dict[str, bool]
    jinjofam: dict[str, bool]
    jinjos: dict[str, bool]
    pages: dict[str, bool]
    honeycomb: dict[str, bool]
    glowbo: dict[str, bool]
    doubloon: dict[str, bool]
    notes: dict[str, bool]
    unlocked_moves: dict[str, bool]
    hag: Any
    cheato_rewards: dict[str, bool]
    honeyb_rewards: dict[str, bool]
    jiggy_chunks: dict[str, bool]
    goggles: Any
    jiggies: dict[str, bool]
    dino_kids: dict[str, bool]
    boggy_kids: dict[str, bool]
    alien_kids: dict[str, bool]
    skivvies: dict[str, bool]
    fit_events: dict[str, bool]
    nests: dict[str, bool]
    roar: Any
    signposts: dict[str, bool]
    warppads: dict[str, bool]
    silos: dict[str, bool]
    worlds: dict[str, bool]
    banjo_map: Any
    bt_tickets: dict[str, bool]
    green_relics: dict[str, bool]
    beans: dict[str, bool]
    isDead: bool
    isTag: bool

async def parse_payload(payload: Payload, ctx: BanjoTooieContext, force: bool):

    # Refuse to do anything if ROM is detected as changed
    if ctx.auth and payload["playerName"] != ctx.auth:
        logger.warning("ROM change detected. Disconnecting and reconnecting...")
        ctx.deathlink_enabled = False
        ctx.deathlink_client_override = False
        ctx.deathlink_pending = False
        ctx.deathlink_sent_this_death = False
        ctx.taglink_enabled = False
        ctx.taglink_client_override = False
        ctx.pending_tag_link = False
        ctx.taglink_sent_this_tag = False

        ctx.finished_game = False
        ctx.location_table = {}
        ctx.chuffy_table = {}
        ctx.movelist_table = {}
        ctx.auth = payload["playerName"]
        await ctx.send_connect()
        return

    # Turn on deathlink if it is on, and if the client hasn't overriden it
    if payload["deathlinkActive"] and ctx.deathlink_enabled and not ctx.deathlink_client_override:
        await ctx.update_death_link(True)
        ctx.deathlink_enabled = True

    # Turn on taglink if it is on, and if the client hasn't overriden it
    if payload["taglinkActive"] and ctx.taglink_enabled and not ctx.taglink_client_override:
        await ctx.update_tag_link(True)
        ctx.taglink_enabled = True

    # Locations handling
    demo = payload["DEMO"]
    chuffy = payload["chuffy"]
    treblelist = payload["treble"]
    stationlist = payload["stations"]
    mystery = payload["mystery"]
    roystenlist = payload["roysten"]
    jinjofamlist = payload["jinjofam"]
    jinjolist = payload["jinjos"]
    pageslist = payload["pages"]
    honeycomblist = payload["honeycomb"]
    glowbolist = payload["glowbo"]
    doubloonlist = payload["doubloon"]
    noteslist = payload["notes"]
    movelist = payload["unlocked_moves"]
    hag = payload["hag"]
    cheatorewardslist = payload["cheato_rewards"]
    honeybrewardslist = payload["honeyb_rewards"]
    jiggychunklist = payload["jiggy_chunks"]
    goggles = payload["goggles"]
    jiggylist = payload["jiggies"]
    dino_kids = payload["dino_kids"]
    boggy_kids = payload["boggy_kids"]
    alien_kids = payload["alien_kids"]
    skivvies = payload["skivvies"]
    mr_fit = payload["fit_events"]
    nests = payload["nests"]
    roar_obtain = payload["roar"]
    signposts = payload["signposts"]
    warp_pads = payload["warppads"]
    silos = payload["silos"]
    worldslist = payload["worlds"]
    banjo_map = payload["banjo_map"]
    bt_tickets = payload["bt_tickets"]
    green_relics = payload["green_relics"]
    beans = payload["beans"]


    # Some JSON encoders serialize an empty dict as a list; coerce back for safety:
    if isinstance(chuffy, list):
        chuffy = {}
    if isinstance(treblelist, list):
        treblelist = {}
    if isinstance(stationlist, list):
        stationlist = {}
    if isinstance(mystery, list):
        mystery = {}
    if isinstance(roystenlist, list):
        roystenlist = {}
    if isinstance(jinjofamlist, list):
        jinjofamlist = {}
    if isinstance(cheatorewardslist, list):
        cheatorewardslist = {}
    if isinstance(honeybrewardslist, list):
        honeybrewardslist = {}
    if isinstance(jiggychunklist, list):
        jiggychunklist = {}
    if isinstance(worldslist, list):
        worldslist = {}
    if isinstance(dino_kids, list):
        dino_kids = {}
    if isinstance(boggy_kids, list):
        boggy_kids = {}
    if isinstance(alien_kids, list):
        alien_kids = {}
    if isinstance(skivvies, list):
        skivvies = {}
    if isinstance(mr_fit, list):
        mr_fit = {}
    if isinstance(nests, list):
        nests = {}
    if isinstance(signposts, list):
        signposts = {}
    if not isinstance(goggles, bool):
        goggles = False
    if not isinstance(demo, bool):
        demo = True
    if not isinstance(banjo_map, int):
        banjo_map = 0
    if isinstance(jiggylist, list):
        jiggylist = {}
    if isinstance(jinjolist, list):
        jinjolist = {}
    if isinstance(movelist, list):
        movelist = {}
    if isinstance(pageslist, list):
        pageslist = {}
    if isinstance(honeycomblist, list):
        honeycomblist = {}
    if isinstance(glowbolist, list):
        glowbolist = {}
    if isinstance(doubloonlist, list):
        doubloonlist = {}
    if isinstance(noteslist, list):
        noteslist = {}
    if isinstance(warp_pads, list):
        warp_pads = {}
    if isinstance(silos, list):
        silos = {}
    if not isinstance(hag, bool):
        hag = False
    if not isinstance(roar_obtain, bool):
        roar_obtain = False
    if isinstance(bt_tickets, list):
        bt_tickets = {}
    if isinstance(green_relics, list):
        green_relics = {}
    if isinstance(beans, list):
        beans = {}

    if demo == False and ctx.sync_ready == True:
        locs1: list[int] = []
        create_hints_params: List[CreateHintsParams] = []
        if ctx.chuffy_table != chuffy:
            ctx.chuffy_table = chuffy
            for locationId, value in chuffy.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.treblelist_table != treblelist:
            ctx.treblelist_table = treblelist
            for locationId, value in treblelist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.stationlist_table != stationlist:
            ctx.stationlist_table = stationlist
            for locationId, value in stationlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.mystery_table != mystery:
            ctx.mystery_table = mystery
            for locationId, value in mystery.items():
                if locationId == "REMOVE": #Don't need to handle this here
                    continue
                if value == True:
                    locs1.append(int(locationId))
        if ctx.roystenlist_table != roystenlist:
            ctx.roystenlist_table = roystenlist
            for locationId, value in roystenlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jiggychunks_table != jiggychunklist:
            ctx.jiggychunks_table = jiggychunklist
            for locationId, value in jiggychunklist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.goggles_table != goggles:
            ctx.goggles_table = goggles
            if goggles == True:
                locs1.append(1231005)
        if ctx.dino_kids_table != dino_kids:
            ctx.dino_kids_table = dino_kids
            for locationId, value in dino_kids.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.boggy_kids_table != boggy_kids:
            ctx.boggy_kids_table = boggy_kids
            for locationId, value in boggy_kids.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.alien_kids_table != alien_kids:
            ctx.alien_kids_table = alien_kids
            for locationId, value in alien_kids.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.skivvies_table != skivvies:
            ctx.skivvies_table = skivvies
            for locationId, value in skivvies.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.mr_fit_table != mr_fit:
            ctx.mr_fit_table = mr_fit
            for locationId, value in mr_fit.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.nests_table != nests:
            ctx.nests_table = nests
            for locationId, value in nests.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.current_map != banjo_map:  #Fix for not resending activated Hints
            ctx.signpost_table = signposts #sets only when transistioning on a new map
        if ctx.signpost_table != signposts:
                ctx.signpost_table = signposts
                actual_hints = ctx.slot_data["custom_bt_data"]["hints"]
                for locationId, value in signposts.items():
                    if value == True:
                        locs1.append(int(locationId))
                        hint = actual_hints.get(str(locationId), None)

                        if not hint is None and hint.get('should_add_hint')\
                            and not hint.get('location_id') is None\
                            and not hint.get('location_player_id') is None:

                            player_id = hint['location_player_id']
                            location_id = hint['location_id']
                            params = CreateHintsParams(location_id, player_id)
                            if not params in ctx.handled_scouts:
                                create_hints_params.append(params)
        if ctx.warppads_table != warp_pads:
            ctx.warppads_table = warp_pads
            for locationId, value in warp_pads.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.silos_table != silos:
            ctx.silos_table = silos
            for locationId, value in silos.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.bt_tickets_table != bt_tickets:
            ctx.bt_tickets_table = bt_tickets
            for locationId, value in bt_tickets.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.green_relics_table != green_relics:
            ctx.green_relics_table = green_relics
            for locationId, value in green_relics.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.beans_table != beans:
            ctx.beans_table = beans
            for locationId, value in beans.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.roar != roar_obtain:
            ctx.roar = roar_obtain
            if roar_obtain == True:
                locs1.append(1231009)
        if ctx.jiggy_table != jiggylist:
            ctx.jiggy_table = jiggylist
            for locationId, value in jiggylist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jinjolist_table != jinjolist:
            ctx.jinjolist_table = jinjolist
            for locationId, value in jinjolist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.pages_table != pageslist:
            ctx.pages_table = pageslist
            for locationId, value in pageslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.honeycomb_table != honeycomblist:
            ctx.honeycomb_table = honeycomblist
            for locationId, value in honeycomblist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.glowbo_table != glowbolist:
            ctx.glowbo_table = glowbolist
            for locationId, value in glowbolist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.doubloon_table != doubloonlist:
            ctx.doubloon_table = doubloonlist
            for locationId, value in doubloonlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.notes_table != noteslist:
            ctx.notes_table = noteslist
            for locationId, value in noteslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.movelist_table != movelist:
            ctx.movelist_table = movelist
            for locationId, value in movelist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.jinjofamlist_table != jinjofamlist:
            ctx.jinjofamlist_table = jinjofamlist
            for locationId, value in jinjofamlist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.cheatorewardslist_table != cheatorewardslist:
            ctx.cheatorewardslist_table = cheatorewardslist
            for locationId, value in cheatorewardslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.honeybrewardslist_table != honeybrewardslist:
            ctx.honeybrewardslist_table = honeybrewardslist
            for locationId, value in honeybrewardslist.items():
                if value == True:
                    locs1.append(int(locationId))
        if ctx.slot_data["options"]["skip_puzzles"] == 1:
            if ctx.worldlist_table != worldslist:
                ctx.worldlist_table = worldslist
                for locationId, value in worldslist.items():
                    if value == True:
                        locs1.append(int(locationId))
        #Mumbo Tokens
        if ctx.slot_data["options"]["victory_condition"] == 1 or ctx.slot_data["options"]["victory_condition"] == 2 or \
            ctx.slot_data["options"]["victory_condition"] == 3 or ctx.slot_data["options"]["victory_condition"] == 4 or \
            ctx.slot_data["options"]["victory_condition"] == 6:
                locs1 = mumbo_tokens_loc(locs1, ctx.slot_data["options"]["victory_condition"])

        if len(locs1) > 0:
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": locs1
            }])

        for params in create_hints_params:
            await ctx.send_msgs([{
                "cmd": "CreateHints",
                "locations": [params.location],
                "player": params.player
            }])
            ctx.handled_scouts.append(params)

        #GAME VICTORY
        #Beat Hag-1
        if hag == True and (ctx.slot_data["options"]["victory_condition"] == 0 or ctx.slot_data["options"]["victory_condition"] == 4 or\
            ctx.slot_data["options"]["victory_condition"] == 6) and not ctx.finished_game:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": 30
            }])
            ctx.finished_game = True
            ctx.set_message("You have completed your goal")

        #Mumbo Tokens
        if (ctx.slot_data["options"]["victory_condition"] == 1 or ctx.slot_data["options"]["victory_condition"] == 2) and not ctx.finished_game:
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if ((ctx.slot_data["options"]["victory_condition"] == 1 and mumbo_tokens >= ctx.slot_data["options"]["minigame_hunt_length"]) or
                        (ctx.slot_data["options"]["victory_condition"] == 2 and mumbo_tokens >= ctx.slot_data["options"]["boss_hunt_length"]) or
                        (ctx.slot_data["options"]["victory_condition"] == 3 and mumbo_tokens >= ctx.slot_data["options"]["jinjo_family_rescue_length"])):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True
                        ctx.set_message("You have completed your goal")

        if (ctx.current_map == 401 and ctx.slot_data["options"]["victory_condition"] == 5 and not ctx.finished_game):
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if (mumbo_tokens >= ctx.slot_data["options"]["token_hunt_length"]):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True

        if (ctx.current_map == 401 and ctx.slot_data["options"]["victory_condition"] == 3 and not ctx.finished_game):
            mumbo_tokens = 0
            for networkItem in ctx.items_received:
                if networkItem.item == 1230798:
                    mumbo_tokens += 1
                    if (mumbo_tokens >= ctx.slot_data["options"]["jinjo_family_rescue_length"]):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": 30
                        }])
                        ctx.finished_game = True

        # Ozone & Mia's Banjo-Tooie Tracker
        if ctx.current_map != banjo_map:
            ctx.current_map = banjo_map
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"Banjo_Tooie_{ctx.team}_{ctx.slot}_map",
                "default": hex(0),
                "want_reply": False,
                "operations": [{"operation": "replace",
                    "value": hex(banjo_map)}]
            }])
    if "sync_ready" in payload and payload["sync_ready"] == "true" and ctx.sync_ready == False:
        ctx.sync_ready = True

    # Deathlink handling
    if ctx.deathlink_enabled:
        if payload["isDead"]: #Banjo died
            ctx.deathlink_pending = False
            if not ctx.deathlink_sent_this_death:
                ctx.deathlink_sent_this_death = True

                await ctx.send_death()
        else: # Banjo is somehow still alive
            ctx.deathlink_sent_this_death = False

    if ctx.taglink_enabled:
        if payload["isTag"]: #Banjo tagged
            ctx.pending_tag_link = False
            if not ctx.taglink_sent_this_tag:
                ctx.taglink_sent_this_tag = True

                await ctx.send_tag_link()
        else:
            ctx.taglink_sent_this_tag = False

def mumbo_tokens_loc(locs: list[int], goaltype: int) -> list[int]:
    for locationId in locs:
        if goaltype == 1 or goaltype == 4:
            if locationId == 1230598: #MT
                locs.append(1230968)
            if locationId == 1230610: #GM
                locs.append(1230969)
            if locationId == 1230616: #WW
                locs.append(1230970)
            if locationId == 1230617: #WW
                locs.append(1230971)
            if locationId == 1230619: #WW
                locs.append(1230972)
            if locationId == 1230620: #WW
                locs.append(1230973)
            if locationId == 1230626: #JRL
                locs.append(1230974)
            if locationId == 1230641: #TDL
                locs.append(1230975)
            if locationId == 1230648: #GI
                locs.append(1230976)
            if locationId == 1230654: #GI
                locs.append(1230977)
            if locationId == 1230663: #HFP
                locs.append(1230978)
            if locationId == 1230668: #CCL
                locs.append(1230979)
            if locationId == 1230670: #CCL
                locs.append(1230980)
            if locationId == 1230673: #CCL
                locs.append(1230981)
            if locationId == 1230749: #CCL
                locs.append(1230982)
        if goaltype == 2 or goaltype == 4 or goaltype == 6:
            if locationId == 1230596: #MT
                locs.append(1230960)
            if locationId == 1230606: #GGM
                locs.append(1230961)
            if locationId == 1230618: #WW
                locs.append(1230962)
            if locationId == 1230632: #JRL
                locs.append(1230963)
            if locationId == 1230639: #TDL
                locs.append(1230964)
            if locationId == 1230745: #GI
                locs.append(1230965)
            if locationId == 1230656: #HFP
                locs.append(1230966)
            if locationId == 1230666: #CC
                locs.append(1230967)
        if goaltype == 3 or goaltype == 4:
            if locationId == 1230676: #JINJOFAM
                locs.append(1230983)
            if locationId == 1230677: #JINJOFAM
                locs.append(1230984)
            if locationId == 1230678: #JINJOFAM
                locs.append(1230985)
            if locationId == 1230679: #JINJOFAM
                locs.append(1230986)
            if locationId == 1230680: #JINJOFAM
                locs.append(1230987)
            if locationId == 1230681: #JINJOFAM
                locs.append(1230988)
            if locationId == 1230682: #JINJOFAM
                locs.append(1230989)
            if locationId == 1230683: #JINJOFAM
                locs.append(1230990)
            if locationId == 1230684: #JINJOFAM
                locs.append(1230991)
    return locs

async def n64_sync_task(ctx: BanjoTooieContext):
    logger.info("Starting socket transport (EverDrive 64). Use /n64 for status information.")
    while not ctx.exit_event.is_set():
        # If the emu_loader transport is already attached to an emulator,
        # there's no reason to keep poking 21221 (and no reason to log about
        # it). Idle quietly until the emulator detaches.
        if ctx.emu_loader is not None and ctx.emu_loader.is_connected():
            if ctx.n64_streams is not None:
                (_, writer) = ctx.n64_streams
                try:
                    writer.close()
                except Exception:
                    pass
                ctx.n64_streams = None
            ctx.n64_status = "Idle (emu_loader attached)"
            try:
                await asyncio.wait_for(ctx.exit_event.wait(), timeout=5.0)
                return
            except asyncio.TimeoutError:
                continue

        error_status = None
        if ctx.n64_streams:
            (reader, writer) = ctx.n64_streams
            if ctx.sendSlot == True:
                msg = get_slot_payload(ctx).encode()
            else:
                msg = get_payload(ctx).encode()
            writer.write(msg)
            writer.write(b'\n')
            try:
                await asyncio.wait_for(writer.drain(), timeout=1.5)
                try:
                    data = await asyncio.wait_for(reader.readline(), timeout=10)
                    data_decoded = json.loads(data.decode())
                    reported_version = data_decoded.get("scriptVersion", 0)
                    getSlotData = data_decoded.get("getSlot", 0)
                    if getSlotData == True:
                        ctx.sendSlot = True
                    elif reported_version >= script_version:
                        if ctx.game is not None and "jiggies" in data_decoded:
                            # Not just a keep alive ping, parse
                            async_start(parse_payload(data_decoded, ctx, False))
                        if not ctx.auth:
                            ctx.auth = data_decoded["playerName"]
                            if ctx.awaiting_rom:
                                await ctx.server_auth(False)
                    else:
                        if not ctx.version_warning:
                            logger.warning(f"Your N64 bridge is version {reported_version}, expected {script_version}. "
                                "Please update to the latest version. "
                                f"Your connection to the {apname} server will not be accepted.")
                            ctx.version_warning = True
                except asyncio.TimeoutError:
                    logger.debug("Read Timed Out, Reconnecting")
                    error_status = CONNECTION_TIMING_OUT_STATUS
                    writer.close()
                    ctx.n64_streams = None
                except ConnectionResetError:
                    logger.debug("Read failed due to Connection Lost, Reconnecting")
                    error_status = CONNECTION_RESET_STATUS
                    writer.close()
                    ctx.n64_streams = None
            except TimeoutError:
                logger.debug("Connection Timed Out, Reconnecting")
                error_status = CONNECTION_TIMING_OUT_STATUS
                writer.close()
                ctx.n64_streams = None
            except ConnectionResetError:
                logger.debug("Connection Lost, Reconnecting")
                error_status = CONNECTION_RESET_STATUS
                writer.close()
                ctx.n64_streams = None
            if ctx.n64_status == CONNECTION_TENTATIVE_STATUS:
                if not error_status:
                    logger.info("Successfully Connected to N64")
                    ctx.n64_status = CONNECTION_CONNECTED_STATUS
                else:
                    ctx.n64_status = f"Was tentatively connected but error occured: {error_status}"
            elif error_status:
                ctx.n64_status = error_status
                logger.info("Lost connection to N64 and attempting to reconnect. Use /n64 for status updates")
        else:
            try:
                logger.debug("Attempting to connect to N64")
                ctx.n64_streams = await asyncio.wait_for(asyncio.open_connection("localhost", 21221), timeout=10)
                ctx.n64_status = CONNECTION_TENTATIVE_STATUS
            except TimeoutError:
                logger.debug("Connection Timed Out, Trying Again")
                ctx.n64_status = CONNECTION_TIMING_OUT_STATUS
                continue
            except ConnectionRefusedError:
                logger.debug("Connection Refused, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue
            except OSError:
                logger.debug("Connection Failed, Trying Again")
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                continue
            except Exception as error:
                logger.info("Unknown Error: %r", error)
                ctx.n64_status = CONNECTION_REFUSED_STATUS
                break

async def emu_loader_monitor_task(ctx: BanjoTooieContext):
    """Direct-emulator-memory bridge."""
    poll_interval = 0.2

    # wait_for_emulator() has its own internal retry loop
    # lets instead do this just one time so we dont get spammed
    logger.info(
        "Waiting for a supported emulator to attach... "
        "(EverDrive users: ignore — use banjo_tooie_connector instead.)"
    )
    ctx.emu_waiting_logged = True

    while not ctx.exit_event.is_set():
      ctx.emu_status = "Waiting for emulator"
      ctx.emu_loader = BTEmuLoaderClient()
      ctx.emu_settings_written = False
      ctx.emu_last_items_count = -1
      ctx.emu_sent_world_entrances.clear()
      ctx.emu_goal_printed = False
      setattr(emu_loader_monitor_task, "_prev", None)
      await ctx.emu_loader.wait_for_emulator()

      if ctx.exit_event.is_set():
          return

      emu_name = ctx.emu_loader.emulator_info.id
      logger.info(f"Connected to {emu_name}.")
      ctx.emu_status = f"Connected to {emu_name}"
      ctx.emu_attached_logged = True

      while not ctx.exit_event.is_set():
        try:
            if ctx.version_warning:
                logger.error(f"ERROR: Your Patched ROM is version {ctx.rom_version}, expected {version}. " +
                    "Please update to the latest version.")
                return

            bth = emu_state.BTHReader(ctx.emu_loader)

            rom_version_tuple = ctx.emu_loader.get_rom_version()
            if rom_version_tuple is not None and rom_version_tuple[0] > 0 and ctx.version_warning is False:
                ctx.rom_version = str(rom_version_tuple[0]) +"."+ str(rom_version_tuple[1]) + "." + str(rom_version_tuple[2])
                if version != ctx.rom_version:
                    ctx.version_warning = True
                    continue
            # Compare ROM-side seed to expected
            expected_seed = None
            if ctx.slot_data:
                s = ctx.slot_data.get("custom_bt_data", {}).get("seed")
                if isinstance(s, int) and s:
                    expected_seed = s & 0xFFFFFFFF

            settings_ptr = bth.settings_ptr()
            if expected_seed is not None and settings_ptr is not None:
                current_seed = ctx.emu_loader.read_u32(settings_ptr + emu_game.SETTING_SEED)
                if current_seed != expected_seed:
                    emu_game.write_slot_settings(ctx.emu_loader, ctx.slot_data)
                    ctx.emu_last_items_count = -1
                    ctx.emu_sent_world_entrances.clear()
                    ctx.emu_goal_printed = False
                ctx.emu_settings_written = True

            current_items_count = len(ctx.items_received) if ctx.items_received else 0
            if (ctx.emu_settings_written
                    and current_items_count != ctx.emu_last_items_count
                    and bth.items_ptr() is not None
                    and bth.traps_ptr() is not None):
                emu_game.write_received_items(ctx.emu_loader, ctx.items_received)
                ctx.emu_last_items_count = current_items_count

            if ctx.emu_settings_written and ctx.deathlink_enabled:
                pc_ptr = bth.pc_ptr()
                if pc_ptr is not None:
                    n64_us = bth.n64_death()
                    pc_us = bth.pc_death()
                    if n64_us != pc_us:
                        ctx.emu_loader.write_u8(pc_ptr + emu_state.PC_DEATH_US, n64_us & 0xFF)
                        if not ctx.deathlink_sent_this_death and ctx.server is not None:
                            ctx.deathlink_sent_this_death = True
                            await ctx.send_death()
                    else:
                        ctx.deathlink_sent_this_death = False
                    if ctx.deathlink_pending:
                        cur_ap = ctx.emu_loader.read_u8(pc_ptr + emu_state.PC_DEATH_AP)
                        ctx.emu_loader.write_u8(pc_ptr + emu_state.PC_DEATH_AP, (cur_ap + 1) & 0xFF)
                        ctx.deathlink_pending = False

            if ctx.emu_settings_written and ctx.slot_data:
                eligible = emu_game.check_world_entrances_open(ctx.emu_loader, ctx.slot_data)
                new_entrances = [loc for loc in eligible if loc not in ctx.emu_sent_world_entrances]
                if new_entrances and ctx.server is not None:
                    missing = ctx.missing_locations or set()
                    to_send = [b for b in new_entrances if b in missing] if missing else list(new_entrances)
                    if to_send:
                        await ctx.send_msgs([{
                            "cmd": "LocationChecks",
                            "locations": to_send,
                        }])
                    ctx.emu_sent_world_entrances.update(new_entrances)

                emu_game.apply_hag1_open(ctx.emu_loader, ctx.slot_data)

                if not ctx.finished_game and ctx.server is not None:
                    if emu_game.check_victory(ctx.emu_loader, ctx.slot_data):
                        await ctx.send_msgs([{"cmd": "StatusUpdate", "status": 30}])
                        ctx.finished_game = True

                # Goal-info dialog
                cur_map = bth.current_map()
                if ctx.emu_goal_printed and cur_map not in (0x158, 0x18B, 0x0):
                    ctx.emu_goal_printed = False
                if not ctx.emu_goal_printed and cur_map == 0x158:
                    pc_q = emu_game.read_pc_text_queue(ctx.emu_loader)
                    n64_q = emu_game.read_n64_text_queue(ctx.emu_loader)
                    if pc_q == n64_q:
                        goal_msg = emu_game.build_goal_info_message(ctx.slot_data)
                        if goal_msg is not None:
                            text, icon = goal_msg
                            if emu_game.send_pc_dialog(ctx.emu_loader, text, icon):
                                ctx.emu_goal_printed = True

                # Drain queued item-received messages ("You can now use X.",
                # world-unlock toasts, etc.). One per tick at most, since the
                # ROM serialises dialog reads.
                if ctx.messages and ctx.auth:
                    options = ctx.slot_data.get("options", {}) or {}
                    dialog_char = emu_game.opt(options, "dialog_character", 110)
                    consumed = emu_game.drain_item_messages(
                        ctx.emu_loader, ctx.messages, ctx.auth, dialog_char,
                    )
                    if consumed:
                        ctx.messages.pop(consumed, None)

                # Ozone & Mia's Banjo-Tooie Tracker
                if ctx.current_map != bth.current_map():
                    ctx.current_map = bth.current_map()
                    await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"Banjo_Tooie_{ctx.team}_{ctx.slot}_map",
                    "default": hex(0),
                    "want_reply": False,
                    "operations": [{"operation": "replace",
                        "value": hex(bth.current_map())}]
                    }])

            collected = emu_state.poll_all_locations(bth)
            prev = getattr(emu_loader_monitor_task, "_prev", None)
            if prev is None:
                new_btids = [b for b, v in collected.items() if v]
            else:
                new_btids = [b for b, v in collected.items() if v and not prev.get(b, False)]

            #Mumbo Tokens
            if ctx.slot_data:
                vc = ctx.slot_data.get("options", {}).get("victory_condition")
                if vc in (1, 2, 3, 4, 6):
                    new_btids = mumbo_tokens_loc(new_btids, vc)

            if new_btids and ctx.server is not None:
                missing = ctx.missing_locations or set()
                to_send = [b for b in new_btids if b in missing] if missing else list(new_btids)
                if to_send:
                    await ctx.send_msgs([{
                        "cmd": "LocationChecks",
                        "locations": to_send,
                    }])

                # Walking up to a signpost should also fire CreateHints
                signpost_btids = emu_addresses.BY_CATEGORY.get("SIGNPOSTS", {})
                if signpost_btids and ctx.slot_data:
                    actual_hints = ctx.slot_data.get("custom_bt_data", {}).get("hints") or {}
                    for btid in new_btids:
                        if btid not in signpost_btids:
                            continue
                        hint = actual_hints.get(str(btid))
                        if (hint is None
                                or not hint.get("should_add_hint")
                                or hint.get("location_id") is None
                                or hint.get("location_player_id") is None):
                            continue
                        params = CreateHintsParams(hint["location_id"], hint["location_player_id"])
                        if params in ctx.handled_scouts:
                            continue
                        await ctx.send_msgs([{
                            "cmd": "CreateHints",
                            "locations": [params.location],
                            "player": params.player,
                        }])
                        ctx.handled_scouts.append(params)

            setattr(emu_loader_monitor_task, "_prev", collected)
        except Exception:
            logger.exception("Banjo-Tooie emulator monitor lost its connection; reconnecting")
            ctx.emu_status = "Lost emulator connection; reconnecting..."
            try:
                if ctx.emu_loader is not None:
                    ctx.emu_loader.disconnect()
            except Exception:
                pass
            ctx.emu_loader = None
            break

        try:
            await asyncio.wait_for(ctx.exit_event.wait(), timeout=poll_interval)
            return
        except asyncio.TimeoutError:
            pass


@atexit.register
def close_program():
  global program
  if program and program.poll() == None:
    program.kill()
    program = None

def main():
    Utils.init_logging("Banjo-Tooie Client")
    parser = get_base_parser()
    args = sys.argv[1:]  # the default for parse_args()
    if "Banjo-Tooie Client" in args:
        args.remove("Banjo-Tooie Client")
    args = parser.parse_args(args)

    async def _main():
        multiprocessing.freeze_support()

        ctx = BanjoTooieContext(args.connect, args.password)
        ctx.emu_monitor_task = asyncio.create_task(emu_loader_monitor_task(ctx), name="EmuLoader Monitor")
        if gui_enabled:
            ctx.run_gui()
        ctx.run_cli()

        await ctx.exit_event.wait()
        ctx.server_address = None

        await ctx.shutdown()

        if ctx.n64_sync_task:
            await ctx.n64_sync_task

        if ctx.emu_monitor_task:
            try:
                await asyncio.wait_for(ctx.emu_monitor_task, timeout=3.0)
            except (asyncio.TimeoutError, asyncio.CancelledError):
                pass
            if ctx.emu_loader is not None:
                try:
                    ctx.emu_loader.disconnect()
                except Exception:
                    pass

    import colorama

    colorama.init()

    asyncio.run(_main())
    colorama.deinit()


if __name__ == "__main__":
    main()

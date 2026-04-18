import colorama, asyncio, bsdiff4, pathlib, os, Utils, hashlib, sys, zipfile, settings, atexit, time, typing
from CommonClient import CommonContext, ClientCommandProcessor, get_base_parser, gui_enabled, logger
from NetUtils import ClientStatus
try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

from . import locations, items, data
from .version import version
from .ids import option_name_to_id, location_name_to_id, item_name_to_id, AP_CMD, AP_STATE
from .rules import StarFox64Rules
from .options import StarFox64OptionsList

game_name = "Star Fox 64"
vanilla_version = "v1.1"
patch_name = f"{game_name} AP v{version.major}.{version.minor}.{version.build}.z64"

program = None
sf64_options = settings.get_settings().sf64_options

def read_file(path):
  with open(path, "rb") as fi:
    data = fi.read()
  return data

def write_file(path, data):
  with open(path, "wb") as fi:
    fi.write(data)

def open_world_file(resource: str, mode: str = "rb", encoding: str = None):
  filename = sys.modules[__name__].__file__
  apworldExt = ".apworld"
  game = "star_fox_64/"
  if apworldExt in filename:
    zip_path = pathlib.Path(filename[:filename.index(apworldExt) + len(apworldExt)])
    with zipfile.ZipFile(zip_path) as zf:
      zipFilePath = game + resource
      if mode == "rb":
        return zf.open(zipFilePath, "r")
      else:
        return io.TextIOWrapper(zf.open(zipFilePath, "r"), encoding)
  else:
    return open(os.path.join(pathlib.Path(__file__).parent, resource), mode, encoding=encoding)

def patch_rom(rom_path, dst_path, patch_path):
  rom = read_file(rom_path)
  md5 = hashlib.md5(rom).hexdigest()
  if (md5 == "ef9a76901153f66123dafccb0c13cd94"): # byte swapped
    swapped = bytearray(b'\0'*len(rom))
    for i in range(0, len(rom), 2):
      swapped[i] = rom[i+1]
      swapped[i+1] = rom[i]
    rom = bytes(swapped)
  elif (md5 != "741a94eee093c4c8684e66b89f8685e8"):
    logger.error(f"Unknown ROM! Please use /patch or restart the {game_name} Client to try again.")
    return False
  with open_world_file(patch_path) as f:
    patch = f.read()
  write_file(dst_path, bsdiff4.patch(rom, patch))
  return True

async def patch_and_run(show_path):
  global program
  patch_path = sf64_options.get("patch_path", "")
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
  with open_world_file(f"assets/{game_name.replace(' ', '_')}_Patched.z64-md5") as f:
    patch_md5 = f.read().decode()
  await asyncio.sleep(0.01)
  patch_successful = True
  if not patch_path or existing_md5 != patch_md5:
    rom = sf64_options.get("rom_path", "")
    if not rom or not os.path.isfile(rom):
      rom = Utils.open_filename(f"Open your {game_name} {vanilla_version} ROM", (("Rom Files", (".z64", ".n64")), ("All Files", "*"),))
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
    patch_successful = patch_rom(rom, patch_path, f"assets/{game_name.replace(' ', '_')}.patch")
    if patch_successful:
      sf64_options.rom_path = rom
      sf64_options.patch_path = os.path.split(patch_path)[0]
    else:
      sf64_options.rom_path = None
    sf64_options._changed = True
  if patch_successful:
    if show_path:
      logger.info(f"Patched {game_name} is located here: {patch_path}")
    program_path = sf64_options.get("program_path", "")
    if program_path and os.path.isfile(program_path) and (not program or program.poll() != None):
      import shlex, subprocess
      logger.info(f"Automatically starting {program_path}")
      lua = Utils.local_path("data", "lua", "connector_sf64_bizhawk.lua")
      if os.access(os.path.split(lua)[0], os.W_OK):
        with open(lua, "w") as to:
          with open_world_file("assets/connector_sf64_bizhawk.lua") as f:
            to.write(f.read().decode())
      args = [*shlex.split(program_path)]
      program_args = sf64_options.program_args
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

class StarFox64CommandProcessor(ClientCommandProcessor):
  def _cmd_patch(self):
    """Reruns the patcher."""
    asyncio.create_task(patch_and_run(True))
    return True

  def _cmd_autostart(self):
    """Allows configuring a program to automatically start with the client.
      This allows you to, for example, automatically start Bizhawk with the patched ROM and lua.
      If already configured, disables the configuration."""
    program_path = sf64_options.get("program_path", "")
    if program_path == "" or not os.path.isfile(program_path):
      program_path = Utils.open_filename(f"Select your program to automatically start", (("All Files", "*"),))
      if program_path:
        sf64_options.program_path = program_path
        sf64_options._changed = True
        logger.info(f"Autostart configured for: {program_path}")
        if not program or program.poll() != None:
          asyncio.create_task(patch_and_run(False))
      else:
        logger.error("No file selected...")
        return False
    else:
      sf64_options.program_path = ""
      sf64_options._changed = True
      logger.info("Autostart disabled.")
    return True

  def _cmd_rom_path(self, path=""):
    """Sets (or unsets) the file path of the vanilla ROM used for patching."""
    sf64_options.rom_path = path
    sf64_options._changed = True
    if path:
      logger.info("rom_path set!")
    else:
      logger.info("rom_path unset!")
    return True

  def _cmd_patch_path(self, path=""):
    """Sets (or unsets) the folder path of where to save the patched ROM."""
    sf64_options.patch_path = path
    sf64_options._changed = True
    if path:
      logger.info("patch_path set!")
    else:
      logger.info("patch_path unset!")
    return True

  def _cmd_program_args(self, path=""):
    """Sets (or unsets) the arguments to pass to the automatically run program. Defaults to passing the lua to Bizhawk."""
    sf64_options.program_args = path
    sf64_options._changed = True
    if path:
      logger.info("program_args set!")
    else:
      logger.info("program_args unset!")
    return True

  def _cmd_deathlink(self):
    """Toggles Death Link."""
    asyncio.create_task(self.ctx.update_death_link(not "DeathLink" in self.ctx.tags))
    return True

  def _cmd_ringlink(self):
    """Toggles Ring Link."""
    asyncio.create_task(self.ctx.update_ring_link(not "RingLink" in self.ctx.tags))
    return True

  def _cmd_tracker(self):
    """Toggles the built in logic Tracker."""
    sf64_options.enable_tracker = not sf64_options.enable_tracker
    sf64_options._changed = True
    self.ctx.tracker.update_locations()
    return True

class StarFox64Tracker:
  player = 1

  def __init__(self, ctx):
    self.ctx = ctx
    self.regions = {}
    self.locations = set()
    self.items = {item_name: 0 for item_name in items.name_to_id}
    self.options = StarFox64OptionsList(**{
      option_key: option_class(ctx.slot_data["options"][option_key])
      for option_key, option_class in typing.get_type_hints(StarFox64OptionsList).items()
    })
    parser = StarFox64Rules(self)
    for region_name, region in data.regions.items():
      self.regions[region_name] = {}
      for key, value in region.items():
        self.regions[region_name][key] = {}
        for name, entry in value.items():
          self.regions[region_name][key][name] = parser.parse(entry["logic"], f"Tracker, {key}: {region_name} -> {name}")
    self.refresh_items()

  def check_region(self, region_name, checked_regions):
    checked_regions.add(region_name)
    region = data.regions[region_name]
    for key, value in region.items():
      logic = self.regions[region_name][key]
      match key:
        case "locations":
          if region_name == "Menu": continue
          for location_name, location in value.items():
            item_name = items.pick_name(self, location["item"], location.get("group"))
            if logic[location_name](self):
              if items.is_event(self, data.items[item_name].get("type", item_name)):
                self.items[item_name] += 1
              else: self.locations.add(locations.name_to_id[location_name])
        case "exits":
          for exit_name, _exit in value.items():
            if exit_name in checked_regions: continue
            if logic[exit_name](self):
              self.check_region(exit_name, checked_regions)

  def update_locations(self):
    if sf64_options.enable_tracker:
      self.ctx.tab_locations.content.data = sorted([
        {"text": self.ctx.location_names.lookup_in_game(location)}
        for location in (self.locations - self.ctx.checked_locations)
      ], key=lambda e: e["text"])
    else: self.ctx.tab_locations.content.data = [{"text":"Tracker disabled. Use /tracker to enable it."}]

  def refresh_locations(self):
    self.locations.clear()
    self.check_region("Menu", set())
    self.update_locations()

  def refresh_items(self):
    for item in self.items:
      self.items[item] = 0
    for item in self.ctx.items_received:
      self.items[self.ctx.item_names.lookup_in_game(item.item)] += 1
    self.ctx.tab_items.content.data = []
    for item_name, amount in sorted(self.items.items()):
      if amount == 0: continue
      if amount > 1: self.ctx.tab_items.content.data.append({"text":f"{item_name}: {amount}"})
      else: self.ctx.tab_items.content.data.append({"text":f"{item_name}"})
    self.refresh_locations()

  def has(self, item, player, count = 1):
    return self.items[item] >= count

  def has_all(self, items, player):
    for item in items:
      if not self.items[item]:
        return False
    return True

  def has_any(self, items, player):
    for item in items:
      if self.items[item]:
        return True
    return False

  def has_all_counts(self, item_counts, player):
    for item, count in item_counts.items():
      if self.items[item] < count:
        return False
    return True

  def has_any_count(self, item_counts, player):
    for item, count in item_counts.items():
      if self.items[item] >= count:
        return True
      return False

  def count(self, item, player):
    return self.items[item]

class StarFox64Context(CommonContext):
  tags = CommonContext.tags
  game = "Star Fox 64"
  items_handling = 0b111
  want_slot_data = True
  command_processor = StarFox64CommandProcessor
  last_ring_link: float = time.time()  # last received ring link on AP layer
  seed_name = 0
  slot_data = {}
  n64_sockets = set()

  def make_gui(self):
    from kvui import GameManager, Window, UILog

    Window.bind(on_request_close=self.on_request_close)
    asyncio.create_task(patch_and_run(True))

    class StarFox64Manager(GameManager):
      base_title = f"Star Fox 64 Client {version.as_string()} | {apname}"

      def build(self):
        ret = super().build()
        self.ctx.tab_items = self.add_client_tab("Items", UILog())
        self.ctx.tab_locations = self.add_client_tab("Tracker", UILog())
        return ret

    return StarFox64Manager

  def on_request_close(self, *args):
    title = "Warning: Autostart program still running!"
    message = "Attempting to close this window again will forcibly close it."
    def cleanup(messagebox):
      self._messagebox = None
    if self._messagebox and self._messagebox.title == title:
      return False
    if program and program.poll() == None:
      self.gui_error(title, message)
      self._messagebox.bind(on_dismiss=cleanup)
      return True
    return False

  async def server_auth(self, password_requested=False):
    if password_requested and not self.password:
      await super().server_auth(password_requested)
    await self.get_username()
    await self.send_connect()

  async def disconnect(self, allow_autoreconnect: bool = False):
    self.seed_name = 0
    self.tags = {"AP"}
    await super().disconnect(allow_autoreconnect)

  async def check_assert(self, condition, title, message):
    if not condition:
      self.gui_error(title, message)
      await self.disconnect()
      raise AssertionError(f"{title}: {message}")

  def on_package(self, cmd, args):
    asyncio.create_task(self.on_cmd(cmd, args))

  async def on_cmd(self, cmd, args):
    try:
      match cmd:
        case "RoomInfo":
          self.seed_name = args["seed_name"]
        case "RoomUpdate":
          if "checked_locations" in args:
            self.tracker.update_locations()
            self.n64_send_checked_locations(locations=set(args["checked_locations"]))
        case "Connected":
          await self.check_assert("slot_data" in args, "Missing Slot Data", "Necessary data is missing from this slot...")
          self.slot_data = args["slot_data"]
          await self.check_assert(version.as_u32() == self.slot_data["version"], "Version Mismatch", "The client version does not match the generated version.")
          old_tags = self.tags.copy()
          if self.slot_data["options"]["deathlink"]: self.tags.add("DeathLink")
          if self.slot_data["options"]["ringlink"]: self.tags.add("RingLink")
          if old_tags != self.tags: await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])
          self.tracker = StarFox64Tracker(self)
          self.n64_send_seed()
          self.n64_send_slot_data()
          self.n64_send_ready()
          self.n64_send_checked_locations()
        case "ReceivedItems":
          self.tracker.refresh_items()
          self.n64_send_items(items=args["items"])
        case "Bounced":
          tags = args.get("tags", [])
          if "RingLink" in tags and self.last_ring_link != args["data"]["time"]:
            self.on_ringlink(args["data"])
        case "PrintJSON":
          match args["type"]:
            case "ItemSend" | "ItemCheat":
              item = args["item"]
              if args["receiving"] == self.slot:
                for n64 in self.n64_sockets:
                  n64.messages.append(f"RECEIVED {self.item_names.lookup_in_game(item.item)}")
                  if len(n64.messages) == 1: self.n64_send_message("", n64)
    except AssertionError as e:
      logger.error(e)

  def on_deathlink(self, data):
    super().on_deathlink(data)
    self.n64_send_deathlink()

  def on_ringlink(self, data):
    # This is for an incoming ringlink.
    rings = data["amount"]
    source = data["source"]
    event_time = data["time"]
    if source == self.slot: return
    self.n64_send_ringlink(rings)

  async def update_ring_link(self, ring_link: bool):
    """Helper function to set Ring Link connection tag on/off and update the connection if already connected."""
    old_tags = self.tags.copy()
    if ring_link:
      self.tags.add("RingLink")
    else:
      self.tags -= {"RingLink"}
    if old_tags != self.tags:
      self.slot_data["ringlink"] = 1 if "RingLink" in self.tags else 0
      self.n64_send_slot_data()
      if self.server and not self.server.socket.closed:
        await self.send_msgs([{"cmd": "ConnectUpdate", "tags": self.tags}])

  async def send_ring(self, amount: int = 1):
    """Helper function to send a ringlink"""
    if self.server and self.server.socket:
      self.last_ring_link = time.time()
      msg = [{
        "cmd": "Bounce", "tags": ["RingLink"],
        "data": {
          "amount": amount,
          "source": self.slot,
          "time": int(self.last_ring_link)
        }
      }]
      await self.send_msgs(msg)

  def n64_send_seed(self, socket=None):
    if self.seed_name == None: return
    send = AP_CMD.SEED.to_bytes(2, "big")
    send += self.team.to_bytes(2, "big")
    send += self.slot.to_bytes(2, "big")
    send += self.seed_name.encode()
    self.n64_send(send, socket)

  def n64_send_slot_data(self, socket=None):
    if self.seed_name == None: return
    send = bytes()
    for name, value in self.slot_data["options"].items():
      send += option_name_to_id[name].to_bytes(2, "big")
      send += value.to_bytes(2, "big")
    self.n64_split_and_send(AP_CMD.OPTIONS.to_bytes(2, "big"), send, 4, socket)

  def n64_send_ready(self, socket=None):
    if self.seed_name == None: return
    send = AP_CMD.READY.to_bytes(2, "big")
    self.n64_send(send, socket)

  def n64_send_checked_locations(self, socket=None, locations=None):
    if self.seed_name == None: return
    if not locations: locations = self.checked_locations
    send = bytes()
    for location in locations:
      send += location.to_bytes(4, "big")
    self.n64_split_and_send(AP_CMD.LOCATIONS.to_bytes(2, "big"), send, 4, socket)

  def n64_send_items(self, socket=None, items=None):
    if self.seed_name == None: return
    if not items: items = self.items_received
    send = bytes()
    for item in items:
      send += item.item.to_bytes(4, "big")
    self.n64_split_and_send(AP_CMD.ITEMS.to_bytes(2, "big"), send, 4, socket)

  def n64_send_deathlink(self, socket=None):
    if self.seed_name == None: return
    send = AP_CMD.DEATHLINK.to_bytes(2, "big")
    self.n64_send(send, socket)

  def n64_send_ringlink(self, amount, socket=None):
    """For RingLink messages etc"""
    if self.seed_name == None: return
    send = AP_CMD.RINGLINK.to_bytes(2, "big")
    send += amount.to_bytes(2, "big", signed=True)
    self.n64_send(send, socket)

  def n64_send_message(self, message, socket=None):
    send = AP_CMD.MESSAGE.to_bytes(2, "big")
    message = message.upper()
    for char in message:
      send += ord(char).to_bytes(1, "big")
    send += b"\0"
    self.n64_send(send, socket)

  def n64_send(self, send, socket=None):
    send = len(send).to_bytes(2, "big") + send
    sockets = self.n64_sockets
    if socket: sockets = {socket}
    for n64 in sockets:
      n64.writer.write(send)

  def n64_split_and_send(self, cmd, send, element_size, socket=None):
    max_packet_size = 510 # not including cmd
    size = max_packet_size - max_packet_size % element_size
    for idx in range(0, len(send), size):
      self.n64_send(cmd + send[idx:idx+size], socket)

class N64Socket:

  @classmethod
  async def create(cls, reader, writer, ctx):
    self = cls()
    self.reader = reader
    self.writer = writer
    self.ctx = ctx
    self.ping = True
    self.state = AP_STATE.DISCONNECTED
    self.messages = []
    logger.info(f"[N64] Connecting")
    asyncio.create_task(self.ping_loop())
    await self.loop()
    self.ping = False
    ctx.n64_sockets -= {self}
    writer.close()
    await writer.wait_closed()
    logger.info(f"[N64] Disconnected")
    return self

  async def loop(self):
    try:
      while not self.reader.at_eof():
        size = int.from_bytes(await self.reader.readexactly(2), "big")-2
        if size < 0 or size > 512:
          logger.error(f"[N64] Invalid packet")
          return
        cmd = int.from_bytes(await self.reader.readexactly(2), "big")
        data = b""
        if size:
          data = await self.reader.readexactly(size)
        match self.state & ~AP_STATE.PINGED:
          case AP_STATE.DISCONNECTED:
            match cmd:
              case AP_CMD.HANDSHAKE:
                v = int.from_bytes(data[:4], "big")
                if v != version.as_u32():
                  logger.error(f"[N64] ROM Version Mismatch: {hex(version.as_u32())} (client) vs {hex(v)} (ROM)")
                  return
                if data[4:] != b"HELO":
                  logger.error(f"[N64] Unexpected packet")
                  return
                send = AP_CMD.HANDSHAKE.to_bytes(2, "big")
                send += v.to_bytes(4, "big")
                send += b"'LO!"
                self.ctx.n64_send(send, self)
                self.state = AP_STATE.CONNECTING
          case AP_STATE.CONNECTING:
            match cmd:
              case AP_CMD.PING:
                self.ctx.n64_send(AP_CMD.PONG.to_bytes(2, "big"), self)
                self.state = AP_STATE.CONNECTED
                self.ctx.n64_send_seed(self)
                self.ctx.n64_send_slot_data(self)
                self.ctx.n64_send_ready(self)
                self.ctx.n64_send_checked_locations(self)
                self.ctx.n64_send_items(self)
                self.ctx.n64_sockets.add(self)
                logger.info(f"[N64] Connected")
          case AP_STATE.CONNECTED:
            self.state &= ~AP_STATE.PINGED
            match cmd:
              case AP_CMD.PING:
                self.ctx.n64_send(AP_CMD.PONG.to_bytes(2, "big"), self)
              case AP_CMD.LOCATIONS:
                locations = set()
                for idx in range(0, len(data), 4):
                  location = int.from_bytes(data[idx:idx+4], "big")
                  if location == location_name_to_id["Goal Completed"]:
                    self.ctx.finished_game = True
                    await self.ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])
                  else:
                    locations.add(location)
                await self.ctx.send_msgs([{"cmd": 'LocationChecks', "locations": tuple(locations)}])
              case AP_CMD.DEATHLINK:
                if "DeathLink" in self.ctx.tags: await self.ctx.send_death()
              case AP_CMD.RINGLINK:
                if "RingLink" in self.ctx.tags:
                  ring_amount = int.from_bytes(data[:2], "big", signed=True)
                  await self.ctx.send_ring(ring_amount)
              case AP_CMD.MESSAGE:
                if len(self.messages):
                  self.ctx.n64_send_message(self.messages.pop(0), self)
              case _:
                logger.error(f"[N64] Unexpected packet: {cmd}")
                return
    except asyncio.IncompleteReadError:
      pass

  async def ping_loop(self):
    while self.ping:
      await asyncio.sleep(5)
      if self.writer.is_closing():
        return
      if self.state & AP_STATE.PINGED:
        logger.info(f"[N64] Ping timeout")
        self.writer.close()
        await self.writer.wait_closed()
        return
      else:
        self.state |= AP_STATE.PINGED

@atexit.register
def close_program():
  global program
  if program and program.poll() == None:
    program.kill()
    program = None

def run(*args):

  async def main(args):
    ctx = StarFox64Context(args.connect, args.password)
    ctx.auth = args.name
    if gui_enabled:
      ctx.run_gui()
    ctx.run_cli()
    try:
      await asyncio.start_server(lambda r, w: N64Socket.create(r, w, ctx), port=0x5F64)
    except OSError:
      logger.error("[N64] Unable to open port 24420")
    await ctx.exit_event.wait()
    await ctx.shutdown()

  parser = get_base_parser(description="Star Fox 64 Archipelago Client.")
  parser.add_argument('--name', default=None, help="Slot Name to connect as.")
  parser.add_argument("url", nargs="?", help="Archipelago connection url")
  args = parser.parse_args(args)
  if args.url:
    url = urllib.parse.urlparse(args.url)
    if url.scheme == "archipelago":
      args.connect = url.netloc
      if url.username:
        args.name = urllib.parse.unquote(url.username)
      if url.password:
        args.password = urllib.parse.unquote(url.password)
    else:
      parser.error(f"bad url, found {args.url}, expected url in form of archipelago://archipelago.gg:38281")

  colorama.init()
  asyncio.run(main(args))
  colorama.deinit()

if __name__ == '__main__':
  run(*sys,argv[1:])

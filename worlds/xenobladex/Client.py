import asyncio
import os
import pathlib
import shutil
import sys
import zipfile
import subprocess
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import BaseServer
import socket
import random
import re
import urllib.parse
import requests
import Utils
apname = Utils.instance_name if Utils.instance_name else "Archipelago"
from NetUtils import ClientStatus, NetworkItem
from typing import Any, Counter, List, NamedTuple, Optional, Set, cast, Callable
from itertools import groupby
import colorama

# CommonClient import first to trigger ModuleUpdater
from CommonClient import CommonContext, server_loop, logger, get_base_parser, gui_enabled
from settings import get_settings

from worlds.xenobladex import XenobladeXWorld
from worlds.xenobladex.rules.level import get_logic_level_count, get_upper_real_level_from_logic_count
from .drops.item import dropItemData
from .drops.lot import dropLotData
from .drops.skill import dropSkillsData
from .items.dollFrames import doll_frame_ids
from .items.groundAugments import ground_augments_data, ground_augments_type_data
from .items.dollAugments import doll_augments_type_data
from .items.groundArmor import ground_armor_type_data
from .items.groundWeapons import ground_weapons_type_data
from .items.dollArmor import doll_armor_type_data
from .items.dollWeapons import doll_weapons_type_data
from .Items import game_type_item_to_offset
from .Locations import game_type_location_to_offset
from .Options import XenobladeXOption

CEMU_MODS_NOT_FOUND = "Unable to find the Cemu Mods please make sure to download the community mods " \
                      "within Cemu settings first"
CEMU_APPDATA_NOT_FOUND = "Unable to find the Cemu Appdata folder, please make sure to start Cemu once beforehand"
CEMU_APWORLD_NOT_FOUND = "Unable to find the Xenoblade X *.apworld"
CEMU_GRAPHIC_PACK_MISSING = "Unable to add the necessary graphic pack to Cemu. " \
                            "Please check your installation directory and Cemu installation"
CEMU_SETTINGS_NOT_FOUND = "Cemu settings.xml file was not found. " \
                          "Please check your installation directory and Cemu installation"
CEMU_NOT_FOUND = "Cemu was not found. Please check your installation directory and Cemu installation"
XENO_DEFAULT_PORT = 45872


class GameItem(NamedTuple):
    type: int
    id: int
    level: int = 1


class XenobladeXHttpServer(HTTPServer):
    address_family = socket.AF_INET6
    locations = ""
    items = ""
    items_debug = ""
    death_link = ""
    messages: List[str] = []
    upload_count = 0
    upload_limit = 25

    def __init__(self, server_address, bind_and_activate: bool = True, debug: bool = False) -> None:
        self.debug = debug
        self.process_game_event: asyncio.Event = asyncio.Event()
        self.process_server_event: asyncio.Event = asyncio.Event()
        super().__init__(server_address, XenobladeXHTTPRequestHandler, bind_and_activate)

    class Gear(NamedTuple):
        affix_1: int = 0
        affix_2: int = 0
        affix_3: int = 0
        slots: int = 0

    def generate_gear(self, item_name: Optional[str], seed_name: Optional[str]) -> Optional[Gear]:
        if not seed_name or not item_name or item_name not in dropItemData:
            return None
        random.seed(seed_name + item_name)

        affix_lot = dropItemData[item_name].affixLot
        affix_num_lot = dropItemData[item_name].affixNumLot
        slot_lot = dropItemData[item_name].slotNumLot
        # set good lot at 5%, which is the minimum value used in game
        # it is way to complex to calculate the exact rate, because that depends on the enemy that droped it
        # check gold lot https://xenoblade.github.io/xbx/bdat/common_local_us/DRP_LotRankTable.html for all values
        if random.random() < 0.05:
            affix_lot = dropItemData[item_name].affixLotGood
            affix_num_lot = dropItemData[item_name].affixNumLotGood
            slot_lot = dropItemData[item_name].slotNumLotGood

        affix_num = 0
        if random.random() < dropLotData[affix_num_lot].lot1Prob / 100:
            affix_num += 1
        if random.random() < dropLotData[affix_num_lot].lot2Prob / 100:
            affix_num += 1
        if random.random() < dropLotData[affix_num_lot].lot3Prob / 100:
            affix_num += 1

        affixes = [0, 0, 0]
        for affix in range(affix_num):
            for skill in dropSkillsData[affix_lot]:
                if random.random() < skill.prob / 100 and affixes[affix] == 0:
                    # matching name only from ground augments but works for skell as well because they are name matched
                    affix_id = [x.name for x in ground_augments_data].index(skill.name)
                    if affix_id not in affixes:
                        affixes[affix] = affix_id
        affixes.sort(reverse=True)

        slot_num = 0
        if random.random() < dropLotData[slot_lot].lot1Prob / 100:
            slot_num += 1
        if random.random() < dropLotData[slot_lot].lot2Prob / 100:
            slot_num += 1
        if random.random() < dropLotData[slot_lot].lot3Prob / 100:
            slot_num += 1

        return self.Gear(affixes[0], affixes[1], affixes[2], slot_num)

    def clear_uploaded_items(self) -> None:
        self.items = ""
        self.upload_count = 0

    def adjust_item_type(self, item_game_type: int, item_game_id: int) -> int:
        if 0x01 <= item_game_type <= 0x05:
            return item_game_type + ground_armor_type_data[item_game_id - 1] - 1
        elif 0x06 <= item_game_type <= 0x07:
            return item_game_type + ground_weapons_type_data[item_game_id - 1] - 1
        elif 0x0a <= item_game_type <= 0x0e:
            return item_game_type + doll_armor_type_data[item_game_id - 1] - 1
        elif 0x0f <= item_game_type <= 0x13:
            return item_game_type + doll_weapons_type_data[item_game_id - 1] - 1
        elif 0x14 <= item_game_type <= 0x15:
            augment_idx = max([id for id in ground_augments_type_data.keys() if id <= item_game_id])
            return item_game_type + ground_augments_type_data[augment_idx]
        elif 0x16 <= item_game_type <= 0x18:
            augment_idx = max([id for id in doll_augments_type_data.keys() if id <= item_game_id])
            return item_game_type + doll_augments_type_data[augment_idx]
        return item_game_type

    def _upload_gear(self, item_game_type: int, item_game_id: int, seed_name: Optional[str],
                     item_name: str) -> None:
        gear = self.generate_gear(item_name, seed_name)
        item_game_type = self.adjust_item_type(item_game_type, item_game_id)
        if gear:
            self.items += f"G Tp={item_game_type:08x} Id={item_game_id:08x} A1={gear.affix_1:08x} " \
                            f"A2={gear.affix_2:08x} A3={gear.affix_3:08x} Sc={gear.slots:08x}\n"
        else:
            if item_game_type == 0x9 and item_name in doll_frame_ids:
                item_game_id = doll_frame_ids[item_name]
            self.items += f"I Tp={item_game_type:08x} Id={item_game_id:08x}\n"

    # Example: Invoke-WebRequest http://localhost:45872/items -Method POST -Body "I Tp=00000007 Id=00000039`n"
    def upload_item(self, item_game_type: int, item_game_id: int, seed_name: Optional[str],
                    prefix: str, item_name: str, player_name: str, item_game_level: int = 1,
                    uploaded_level: int = 0, logic_level_steps: int = 0) -> None:
        if self.upload_count > self.upload_limit:
            return
        self.upload_count += 1

        if item_game_type == 0:
            if item_name == "Level":
                if logic_level_steps == 0:
                    return
                item_game_level = get_upper_real_level_from_logic_count(item_game_level, logic_level_steps)
            self.items += f"K Id={item_game_id:08x} Fg={item_game_level:08x}\n"
        elif item_game_type < 0x20:
            self._upload_gear(item_game_type, item_game_id, seed_name, item_name)
        elif item_game_type < 0x21:
            self.items += f"A Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x22:
            self.items += f"S Id={item_game_id:08x} Lv={1:08x}\n"
        elif item_game_type < 0x23:
            self.items += f"F Id={item_game_id:08x} Lv={item_game_level * 10:08x}\n"
        elif item_game_type < 0x24:
            if item_game_level > 4 and not uploaded_level < 4:
                return
            self.items += f"D Id={item_game_id:08x} Lv={min(item_game_level, 4) + 1:08x}\n"
        elif item_game_type < 0x25:
            self.items += f"C Id={item_game_id:08x} Lv={10:08x}\n"

        if not item_name.startswith("DEBUG"):
            self.upload_message(f"{prefix} from {player_name}", item_name)

        logger.debug(f"Upload Item: {item_name} Id: {item_game_id} Type: {item_game_type}")

    def _match_line(self, data: list["GameItem"], game_type: Optional[int], regex: str, min: int = 1, max: int = 0xFFFF,
                    has_lvl: bool = False, lvl_change: Callable[[int], int] = lambda lvl: lvl) -> None:
        match = re.findall(regex, self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        data += [GameItem(game_type if game_type is not None else entry[1], entry[0], 10000 if not has_lvl
                          else lvl_change(entry[1])) for entry in match if min <= entry[1] <= max]

    def upload_death(self) -> None:
        self.death_link += f"K Id={6:08x} Fg={1:08x}\n"

    def upload_message(self, heading: str, body: str) -> None:
        self.messages += [self._generate_message(heading, body)]

    def _sanitize_message(self, message: str) -> str:
        return re.sub(r"[\r\n]", "", message)

    def _generate_message(self, heading: str, body: str) -> str:
        return f"M {self._sanitize_message(heading)}\r{(self._sanitize_message(body))[:60]}\n"

    def clear_locations(self) -> None:
        self.locations = ""

    def download_locations(self) -> list[GameItem]:
        locations: list[GameItem] = []

        self._match_line(locations, 0, r'^CP Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(locations, 1, r'^EN Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(locations, 2, r'^FN Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1})\n')
        self._match_line(locations, 3, r'^SG Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) AId=[0-9a-fA-F]{2}\n', min=3)
        self._match_line(locations, 4, r'^LC Id=([0-9a-fA-F]{3}) Fg=([0-9a-fA-F]{1}) Tp=[0-9a-fA-F]{1}\n')

        return locations

    def _match_line_augment(self, data: list[GameItem], game_type: int, regex: str,
                            lower: int = 0, upper: int = 0xFFFF) -> None:
        match = re.findall(regex, self.locations, re.MULTILINE)
        match = [tuple(int(entry_id, 16) for entry_id in entry_tuple) for entry_tuple in match]
        data += [GameItem(game_type, entry[i]) for entry in match if lower <= entry[1] <= upper
                 for i in range(2, re.compile(regex).groups) if 0 < entry[i] < 0xFFFF]

    def download_items(self, logic_level_steps: int) -> list[GameItem]:
        items: list[GameItem] = []

        self._match_line(items, 0, r'^KY Id=([1-9a-fA-F]{1}) Fg=([0-9a-fA-F]{2})\n', has_lvl=True)
        self._match_line(items, 0, r'^KY Id=([eE]{1}) Fg=([0-9a-fA-F]{2})\n', has_lvl=True,
                         lvl_change=lambda lvl: get_logic_level_count(lvl, logic_level_steps))
        self._match_line(items, None, r'^IT Id=([0-9a-fA-F]{3}) Tp=([0-9a-fA-F]{2})(?:\n| S1Id)')
        self._match_line(items, 0x1c, r'^IT Id=([0-9a-fA-F]{3}) Tp=1[cC] Cn=([0-9a-fA-F]{3})', has_lvl=True)
        self._match_line(items, 0x1d, r'^IT Id=([0-9a-fA-F]{3}) Tp=1[dD] Cn=([0-9a-fA-F]{3})', has_lvl=True)
        equip_regex = r'^EQ CId=[0-9a-fA-F]{3} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})'
        self._match_line(items, 0x6, equip_regex, min=0, max=1)
        self._match_line(items, 0x1, equip_regex, min=2, max=11)
        doll_regex = r'^DL GIx=[0-9a-fA-F]{2} Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})'
        self._match_line(items, 0xf, doll_regex, min=0, max=0x9)
        self._match_line(items, 0x9, doll_regex, min=0xa, max=0xa)
        self._match_line(items, 0xa, doll_regex, min=0xb, max=0xf)
        augment_regex_suffix = r'.*A1Id=([0-9a-fA-F]{4}) A2Id=([0-9a-fA-F]{4}) A3Id=([0-9a-fA-F]{4})'
        augment_regex = r'.*Id=([0-9a-fA-F]{3}) Tp=([0-9a-fA-F]{2})' + augment_regex_suffix
        self._match_line_augment(items, 0x14, rf'^IT{augment_regex}', lower=1, upper=7)
        self._match_line_augment(items, 0x16, rf'^IT{augment_regex}', lower=0xa, upper=0x13)
        augment_equip_regex = r'.*Id=([0-9a-fA-F]{3}) Ix=([0-9a-fA-F]{1})' + augment_regex_suffix
        self._match_line_augment(items, 0x14, rf'^EQ{augment_equip_regex}')
        self._match_line_augment(items, 0x16, rf'^DL{augment_equip_regex}')
        self._match_line(items, 0x20, r'^AT Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')
        self._match_line(items, 0x21, r'^SK Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')
        self._match_line(items, 0x22, r'^FD Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{2}) Ch=.*\n',
                         has_lvl=True, lvl_change=lambda lvl: int(lvl / 10) if lvl else 0)
        self._match_line(items, 0x23, r'^FS Id=([0-9a-fA-F]{1}) Lv=([0-9a-fA-F]{1})\n',
                         has_lvl=True, lvl_change=lambda lvl: lvl - 1)
        self._match_line(items, 0x24, r'^CL Id=([0-9a-fA-F]{2}) Lv=([0-9a-fA-F]{1})\n')

        return items

    def download_death(self) -> bool:
        pattern = r'^KY Id=6 .*\n'
        result: bool = len(re.findall(pattern, self.locations, re.MULTILINE)) != 0
        re.sub(pattern, "", self.locations)
        if result:
            self.upload_message("Deathlink", "Sent death")
        return result


class XenobladeXHTTPRequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server: BaseServer) -> None:
        self.http_server: XenobladeXHttpServer = cast(XenobladeXHttpServer, server)
        super().__init__(request, client_address, server)

    def respond_success(self) -> None:
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()

    def get_items(self) -> None:
        self.respond_success()
        if self.http_server.process_server_event.is_set():
            self.http_server.process_server_event.clear()
            messages = "".join(self.http_server.messages[-2:])
            self.http_server.messages = self.http_server.messages[:-2]
            items_text = messages + self.http_server.items + self.http_server.death_link + self.http_server.items_debug
            self.http_server.items = ""
            self.http_server.items_debug = ""
            self.http_server.death_link = ""
            self.wfile.write(items_text.encode())
            if items_text:
                logger.debug(f"{items_text.encode()!r}")

    def post_locations(self) -> None:
        locations = (self.rfile.read(int(self.headers['content-length']))).decode('cp437').replace(":", "\n")
        self.respond_success()
        if "^" in locations[0]:
            self.http_server.locations = ""
            locations = locations[1:]
        upload_ended = "$" in locations[-1]
        if upload_ended:
            locations = locations[0:-2]
        self.http_server.locations += locations
        if upload_ended:
            self.http_server.process_game_event.set()

    # Silence connection request logging
    def log_request(self, code: int | str = '-', size: int | str = '-') -> None:
        return

    def debug_get_locations(self) -> None:
        self.respond_success()
        self.wfile.write(self.http_server.locations.encode())

    def debug_post_items(self) -> None:
        self.http_server.items_debug = (self.rfile.read(int(self.headers['content-length']))).decode('cp437')
        self.respond_success()

    def do_GET(self) -> None:
        if self.path == "/items":
            self.get_items()
        if self.path == "/locations" and self.http_server.debug:
            self.debug_get_locations()

    def do_POST(self) -> None:
        if self.path == "/locations":
            self.post_locations()
        if self.path == "/items" and self.http_server.debug:
            self.debug_post_items()


class XenobladeXContext(CommonContext):
    game = "Xenoblade X"
    items_handling = 0b111  # get items from your own world
    want_slot_data = True

    cemu_process: Optional[subprocess.Popen[bytes]] = None
    locations_checked: Set[int]
    death_link = False
    death_link_pending = False
    logic_level_steps = 0

    def __init__(self, server_address: Optional[str], password: Optional[str], xeno_port: int,
                 debug: bool = False) -> None:
        self.http_server = XenobladeXHttpServer(('::', xeno_port), debug=debug)
        self.xeno_port = xeno_port
        super().__init__(server_address, password)

    async def server_auth(self, password_requested: bool = False) -> None:
        if password_requested and not self.password:
            await super(XenobladeXContext, self).server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict[str, Any]) -> None:
        if cmd == "Connected":
            slot_data = args.get('slot_data', None)
            if slot_data:
                cemu_options: list[XenobladeXOption] = [XenobladeXOption(**option)
                                                        for option in slot_data["cemu_options"]]
                options = slot_data.get("options", None)
                if options:
                    self.death_link = options.get("death_link", 0) != 0
                    self.logic_level_steps = options.get("logic_level_steps", 0)
                self.http_server.clear_locations()
                self.prepare_cemu(cemu_options)
        if cmd in {"RoomInfo"}:
            self.seed_name = args["seed_name"]

    def on_deathlink(self, data: dict[str, Any]) -> None:
        self.death_link_pending = True
        death_source = data["source"]
        self.http_server.upload_death()
        self.http_server.upload_message(f"From {death_source}", "Death")
        super().on_deathlink(data)

    def on_print_json(self, args: dict[str, Any]) -> None:
        print_type = args.get("type", "")
        if print_type in ["ItemSend", "ItemCheat", "Hint"]:
            item: NetworkItem = args["item"]
            sender = item.player
            receiver: int = args["receiving"]
            if (not self.slot_concerns_self(receiver)) and self.slot_concerns_self(sender):
                item_name = self.item_names.lookup_in_slot(item.item, receiver)
                self.http_server.upload_message(f"To {self.player_names[receiver]}", item_name)
        elif print_type == "Chat":
            chatting_player = self.player_names[args["slot"]]
            self.http_server.upload_message(f"From {chatting_player}", args["message"])
        elif print_type == "ServerChat":
            self.http_server.upload_message("From Server", args["message"])
        elif print_type == "Join":
            self.http_server.upload_message("Joined", self.player_names[args["slot"]])
        elif print_type == "Part":
            self.http_server.upload_message("Disconnected", self.player_names[args["slot"]])
        elif print_type == "Goal":
            self.http_server.upload_message("Reached Goal", self.player_names[args["slot"]])
        super(XenobladeXContext, self).on_print_json(args)

    def run_gui(self) -> None:
        from kvui import GameManager

        class XenobladeXManager(GameManager):
            logging_pairs = [
                ("Client", "Archipelago")
            ]
            base_title = apname + " Xenoblade X Client"

        self.ui = XenobladeXManager(self)
        self.ui_task = asyncio.create_task(self.ui.async_run(), name="UI")

    def get_level(self, archipelago_item_id: int) -> int:
        return len([item.item for item in self.items_received if item.item == archipelago_item_id])

    def archipelago_item_to_name(self, archipelago_item_id: int) -> str:
        return re.sub(r"^[A-Z]*?: ", "", XenobladeXWorld.item_id_to_name[archipelago_item_id])

    def archipelago_item_to_prefix(self, archipelago_item_id: int) -> str:
        return XenobladeXWorld.item_id_to_name[archipelago_item_id].split(":")[0]

    def archipelago_item_to_game_item(self, archipelago_item_id: int) -> GameItem:
        game_item_type_offset = max([id for id in game_type_item_to_offset.values()
                                     if id < archipelago_item_id - XenobladeXWorld.base_id])
        game_item_type = min([key for key, offset in game_type_item_to_offset.items()
                              if offset == game_item_type_offset])
        return GameItem(game_item_type, (archipelago_item_id - XenobladeXWorld.base_id) - game_item_type_offset)

    def game_item_to_archipelago_item(self, game_item: GameItem) -> int:
        return XenobladeXWorld.base_id + game_type_item_to_offset[game_item.type] + game_item.id

    def game_location_to_archipelago_location(self, game_location: GameItem) -> int:
        return XenobladeXWorld.base_id + game_type_location_to_offset[game_location.type] + game_location.id

    async def download_game_locations(self) -> None:
        game_locations = {self.game_location_to_archipelago_location(location)
                          for location in self.http_server.download_locations()}
        new_locations = game_locations.difference(self.locations_checked)
        if new_locations:
            await self.send_msgs([{"cmd": 'LocationChecks', "locations": new_locations}])
            self.locations_checked = game_locations

    async def upload_game_items(self) -> None:
        self.http_server.clear_uploaded_items()
        uploaded_server_items = self.http_server.download_items(self.logic_level_steps)
        uploaded_items = {self.game_item_to_archipelago_item(itm): itm.level for itm in uploaded_server_items}
        player_item_names = {net_item.item: self.player_names[net_item.player] for net_item in self.items_received}
        server_items = Counter(network_item.item for network_item in self.items_received)
        for item, level in server_items.items():
            uploaded_level = uploaded_items.get(item, 0)
            if level <= uploaded_level:
                continue
            game_item = self.archipelago_item_to_game_item(item)
            prefix = self.archipelago_item_to_prefix(item)
            item_name = self.archipelago_item_to_name(item)
            self.http_server.upload_item(game_item.type, game_item.id, self.seed_name,
                                         prefix, item_name, player_item_names[item], level,
                                         uploaded_level, self.logic_level_steps)
            if item_name == "Victory":
                await self.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

    async def process_game(self) -> None:
        await self.check_server()
        while not self.exit_event.is_set():
            try:
                await self.update_death_link(self.death_link)
                if self.http_server.process_game_event.is_set():
                    self.http_server.process_game_event.clear()
                    if "DeathLink" in self.tags and self.http_server.download_death():
                        if self.death_link_pending:
                            self.death_link_pending = False
                        else:
                            await self.send_death()
                    await self.download_game_locations()
                    await self.upload_game_items()
                    self.http_server.process_server_event.set()
                await asyncio.sleep(0.1)
            except Exception as e:
                logger.exception(e, extra={"compact_gui": True})
                msg = "Aborted Xenoblade X Connection"
                logger.error(msg)
                self.gui_error(msg, e)
                self.exit_event.set()

    async def check_server(self) -> None:
        url = f"http://localhost:{self.xeno_port}/"
        # Give server time to spin up
        while not self.exit_event.is_set():
            await asyncio.sleep(2)
            try:
                # Check if items is reachable. Should be enough to test if game can connect.
                response = requests.get(f"{url}items", timeout=3)
                if not response.status_code == 200:
                    raise Exception(f"XenoX Server refused connection for items with code: {response.status_code}")
                else:
                    return

            except Exception as e:
                logger.exception(e, extra={"compact_gui": True})
                msg = "Unable to establish the game server"
                detail = f"Check your firewall popups and settings. Make sure that '{url}' " \
                         f"is reachable. Check docs for more info."
                logger.error(msg)
                self.gui_error(msg, detail)
                while self.ui and self._messagebox and self._messagebox._is_open:
                    await asyncio.sleep(1)

    # region Cemu-Config
    def prepare_cemu(self, options: list[XenobladeXOption]) -> None:
        try:
            mod_path = "graphicPacks/downloadedGraphicPacks/XenobladeChroniclesX/Mods/"
            settings_path = "settings.xml"
            appdata = None
            if Utils.is_windows:
                appdata = os.getenv('APPDATA')
            elif Utils.is_linux:
                home_path = pathlib.Path.home()
                appdata = os.path.join(home_path, ".var/app/info.cemu.Cemu/config")
                if not os.path.isdir(appdata):
                    appdata = os.path.join(home_path, ".local/share")
            if not appdata:
                raise Exception(CEMU_APPDATA_NOT_FOUND)
            cemu_appdata_path = os.path.join(appdata, "Cemu")
            if not os.path.isdir(cemu_appdata_path):
                raise Exception(CEMU_SETTINGS_NOT_FOUND)
            cemu_mod_path = os.path.join(cemu_appdata_path, mod_path)
            cemu_settings_path = os.path.join(cemu_appdata_path, settings_path)
            if Utils.is_linux:
                config = os.path.join(pathlib.Path.home(), ".config/Cemu")
                if not os.path.isdir(cemu_mod_path):
                    cemu_mod_path = os.path.join(config, mod_path)
                if not os.path.isdir(cemu_settings_path):
                    cemu_settings_path = os.path.join(config, settings_path)
            self.copy_cemu_files(cemu_mod_path)
            self.set_cemu_graphic_packs(cemu_settings_path, mod_path, options)
            self.copy_port(cemu_mod_path)
            self.open_cemu()
        except Exception as e:
            logger.exception(str(e), extra={"compact_gui": True})
            logger.error(str(e))
            self.gui_error(str(e), e)
            self.exit_event.set()

    def copy_cemu_files(self, cemu_mod_path: str) -> None:
        archipelago_graphic_pack_path = "worlds/xenobladex/cemu_graphicpack/"
        cemu_ap_path = os.path.join(cemu_mod_path, "AP")
        if not os.path.isdir(cemu_mod_path):
            raise Exception(CEMU_MODS_NOT_FOUND)
        if not os.path.exists(cemu_ap_path):
            os.makedirs(cemu_ap_path)
        if not os.path.isdir(archipelago_graphic_pack_path):
            self.copy_from_apworld(cemu_ap_path)
            return
        try:
            shutil.copytree(archipelago_graphic_pack_path, cemu_ap_path, dirs_exist_ok=True)
        except Exception:
            raise Exception(CEMU_GRAPHIC_PACK_MISSING)

    def copy_from_apworld(self, cemu_ap_path: str) -> None:
        try:
            zip_path = XenobladeXWorld.zip_path
            if not zip_path:
                raise
            with zipfile.ZipFile(zip_path, "r") as z:
                for file in z.namelist():
                    filename = os.path.basename(file)
                    if file.startswith("xenobladex/cemu_graphicpack/") and filename:
                        z.getinfo(file).filename = filename
                        z.extract(file, cemu_ap_path)
        except Exception:
            raise Exception(CEMU_APWORLD_NOT_FOUND)

    def set_cemu_graphic_packs(self, settings_path: str, mod_path: str,
                               options: list[XenobladeXOption]) -> None:
        try:
            with open(settings_path, "r") as file:
                filedata = file.read()

            # Group by cemu pack
            sorted_options = sorted(options, key=lambda option: option.cemu_pack)
            grouped_options = [list(result) for key, result
                               in groupby(sorted_options, key=lambda option: option.cemu_pack)]

            for settings in grouped_options:
                cemu_pack: str = settings[0].cemu_pack

                # Cleanup
                pack_regex = rf'<Entry filename="{mod_path}{cemu_pack}/rules.txt"(/>\n|>.*?</Entry>\n)'
                filedata = re.sub(pack_regex, "", filedata, flags=re.DOTALL)

                # Abort whenever a single setting of a pack is off
                if any(setting.cemu_selection == "off" for setting in settings):
                    continue

                # Addition
                content = ""
                for setting in settings:
                    if setting.cemu_option != "":
                        category = f"<category>{setting.cemu_option}</category>" \
                                   if setting.cemu_option != "Active preset" else ""
                        content += f"<Preset>\n{category}<preset>{setting.cemu_selection}</preset>\n</Preset>\n"
                pack_content = (f'<Entry filename="{mod_path}{cemu_pack}/rules.txt">\n{content}</Entry>\n\n')
                filedata = re.sub(r'</GraphicPack>', f"{pack_content}</GraphicPack>", filedata)

            with open(settings_path, "w") as file:
                file.write(filedata)
        except Exception:
            raise Exception(CEMU_SETTINGS_NOT_FOUND)

    def copy_port(self, cemu_mod_path: str) -> None:
        cemu_ap_rules = os.path.join(cemu_mod_path, "AP/rules.txt")
        with open(cemu_ap_rules, "r") as rules:
            ruledata = rules.read()

        ruledata = re.sub(rf"\$curlPort = {XENO_DEFAULT_PORT}", f"$curlPort = {self.xeno_port}", ruledata)

        with open(cemu_ap_rules, "w") as rules:
            rules.write(ruledata)

    def open_cemu(self) -> None:
        try:
            cemu_exe = get_settings()["xenobladex_options"]["executable"]
            if not self.cemu_process or self.cemu_process.poll() is not None:
                self.cemu_process = subprocess.Popen(cemu_exe)
        except Exception:
            raise Exception(CEMU_NOT_FOUND)
    # endregion


async def main(args: dict[str, Any]) -> None:
    Utils.init_logging("XenobladeXClient", exception_logger="Client")

    # handle if launched using the "archipelago://name:pass@host:port" url from webhost
    if args["url"]:
        url = urllib.parse.urlparse(args["url"])
        if url.scheme == "archipelago":
            args["connect"] = url.netloc
            if url.username:
                args["name"] = urllib.parse.unquote(url.username)
            if url.password:
                args["password"] = urllib.parse.unquote(url.password)
        else:
            logger.error(f"bad url, found {args['url']}, expected url in form of archipelago://archipelago.gg:38281")

    ctx = XenobladeXContext(args["connect"], args["password"], args["xeno_port"], args["debug"])
    ctx.auth = args["name"]
    if ctx.server_task is None:
        ctx.server_task = asyncio.create_task(server_loop(ctx), name="ServerLoop")

    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    asyncio.create_task(asyncio.to_thread(ctx.http_server.serve_forever), name="XenobladeXHttpServer")
    xeno_sync_task = asyncio.create_task(ctx.process_game(), name="XenobladeXSync")

    await ctx.exit_event.wait()
    await xeno_sync_task

    ctx.server_address = None
    await ctx.shutdown()
    ctx.http_server.shutdown()


def launch(*args: str) -> None:
    parser = get_base_parser()
    parser.add_argument("-d", "--debug", action="store_true", help="Enable full server exposure for debugging purposes")
    parser.add_argument("--xeno_port", nargs="?", type=int, default=XENO_DEFAULT_PORT,
                        help="Port of the Xenoblade X server")
    parser.add_argument('--name', default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    parsed_args = parser.parse_args(args)

    colorama.init()
    asyncio.run(main(vars(parsed_args)))
    colorama.deinit()


if __name__ == '__main__':
    launch(*sys.argv[1:])

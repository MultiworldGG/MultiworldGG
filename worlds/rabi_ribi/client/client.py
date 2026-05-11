from typing import Dict, NamedTuple, Optional, Set, Tuple
import ast
import asyncio
import os
import time
import hashlib
import urllib.parse
import Utils

from BaseClasses import CollectionState
from CommonClient import (
    CommonContext,
    get_base_parser,
    logger,
    server_loop,
    gui_enabled,
)
from NetUtils import ClientStatus, NetworkItem
try:
    from Utils import instance_name as apname
except ImportError:
    apname = "Archipelago"

from worlds.AutoWorld import World
from worlds.rabi_ribi import RabiRibiWorld
from worlds.rabi_ribi.client.memory_io import RabiRibiMemoryIO
from worlds.rabi_ribi.items import consumable_table
from worlds.rabi_ribi.locations import all_locations
from worlds.rabi_ribi.names import ItemName
from worlds.rabi_ribi.options import AttackMode
from worlds.rabi_ribi.utility import (
    load_text_file,
    convert_existing_rando_name_to_ap_name
)

try:
    from worlds.tracker.TrackerClient import UT_VERSION, TrackerCommandProcessor, TrackerGameContext # type: ignore

    tracker_loaded = True
except ImportError:
    from CommonClient import ClientCommandProcessor

    class TrackerCore:
        player_id: int

        def get_current_world(self) -> World | None: ...

    class CurrentTrackerState(NamedTuple):
        state: CollectionState

    class TrackerGameContext(CommonContext):
        tracker_core: TrackerCore

        def run_generator(self) -> None: ...
        def updateTracker(self) -> CurrentTrackerState: ...

    class TrackerCommandProcessor(ClientCommandProcessor):
        ctx: TrackerGameContext

    tracker_loaded = False
    UT_VERSION = "Not found"

STRANGE_BOX_ITEM_ID = 30
TROPHY_ITEM_ID = 42
TRIGGER_BLOCK_EVENT_ID1 = 576

class RabiRibiCommandProcessor(TrackerCommandProcessor): # type: ignore
    ctx: "RabiRibiContext"

    def _cmd_eggs(self) -> None:
        """Tells you how many Easter Eggs you have, and how many you need to beat the game"""
        self.ctx.print_egg_amounts()

    def _cmd_disable_crosswarp_check(self) -> None:
        """Disables crosswarp check for Strange Box warping"""
        self.ctx.disable_crosswarp()

    def _cmd_attack_mode(self, mode: str = "") -> None:
        """Updates the player's attack mode. Options are normal, super, or hyper"""
        if mode is None or mode not in AttackMode.options:
            logger.info("Provide an attack mode using /attack_mode [mode]. Available options for mode are normal, super, or hyper")
            return
        self.ctx.set_attack_mode_flag(mode)

    def _cmd_deathlink(self):
        """Toggle deathlink from client. Overrides default setting."""
        self.ctx.death_link_enabled = not self.ctx.death_link_enabled
        Utils.async_start(self.ctx.update_death_link(self.ctx.death_link_enabled), name="Update Deathlink")
        logger.info(f"Deathlink is now {'enabled' if self.ctx.death_link_enabled else 'disabled'}")

class RabiRibiContext(TrackerGameContext): # type: ignore
    """Rabi Ribi Game Context"""
    game = "Rabi-Ribi"
    tags = {"AP"}

    @property
    def player(self) -> int:
        try:
            return self.player_id
        except AttributeError:
            return self.tracker_core.player_id

    def get_world(self) -> World | None:
        try:
            return self.tracker_core.get_current_world()
        except AttributeError:
            return self.multiworld.worlds[self.player]

    def get_updated_state(self) -> CollectionState:
        try:
            from worlds.tracker.TrackerClient import updateTracker # type: ignore

            return updateTracker(self).state
        except:
            return self.updateTracker().state

    def __init__(self, server_address: Optional[str], password: Optional[str]) -> None:
        super().__init__(server_address, password)
        self.items_handling = 0b101  # local except starting items
        self.command_processor = RabiRibiCommandProcessor
        self.rr_interface = RabiRibiMemoryIO()
        self.location_coordinates_to_ap_location_name, self.item_name_to_rabi_ribi_item_id = \
            self.read_location_coordinates_and_rr_item_ids()

        self.ap_location_name_to_location_coordinates: Dict[str, Tuple[int, int, int]] = {}
        for area, v in self.location_coordinates_to_ap_location_name.items():
            for (x, y), name in v.items():
                self.ap_location_name_to_location_coordinates[name] = (area, x, y)

        self.current_area_id = -1
        self.current_room: Tuple[int, int] = (-1, 1)
        self.state_giving_item = False
        self.collected_eggs: Set[Tuple[int,int,int]] = set()
        self.seed_name = None
        self.slot_data = None

        # populated when we have the unique seed ID
        self.custom_seed_subdir = None
        self.seed_player = None
        self.seed_player_id = None

        self.time_since_last_paused = time.time()
        self.time_since_main_menu = time.time()
        self.time_since_last_item_obtained = time.time()
        self.time_since_last_warp_menu = time.time()
        self.time_since_last_costume_menu = time.time()
        self.time_since_last_save_menu = time.time()
        self.time_since_last_death = time.time()
        
        self.items_received_rabi_ribi_ids = []
        self.obtained_items_queue: asyncio.Queue[NetworkItem] = asyncio.Queue()

        self.critical_section_lock = asyncio.Lock()

        self.death_link_enabled = False
        self.death_link_buffer = []
        self.has_died = False

        self.is_crosswarp_disabled = True
        self.updated_attack_mode = None

    def make_gui(self):
        ui = super().make_gui()
        ui.base_title = f"Rabi-Ribi Client v{RabiRibiWorld.world_version.as_simple_string()}"
        if tracker_loaded:
            ui.base_title += f" | UT {UT_VERSION}"

        ui.base_title += f" | {apname}"
        return ui

    def read_location_coordinates_and_rr_item_ids(self):
        """
        This method retrieves the location coordinates of each item from
        locations_items.txt, and dumps it in a mapping for later use.

        It also retrieves the rabi ribi item ids for each item and dumps
        that in a seperate map for later use.

        This is a slightly modified version of the code found in
        worlds.rabi_ribi.existing_randomizer.visualizer.load_item_locs()
        """
        coordinate_to_location_name = {}
        item_name_to_rabi_ribi_item_id = {
            ItemName.attack_up: 223,
            ItemName.mp_up: 287,
            ItemName.regen_up: 351,
            ItemName.hp_up: 159,
            ItemName.pack_up: 415
        }

        # location_items.txt contains 3 sets of items:
        #   - Items, for items that can be found lying around.
        #   - ShufflableGiftItems, for items normally gifted to the player, but have a location
        #     added by the randomizer.
        #   - AdditionalItems, for items that are either bought at the shop, or given to the player
        #     but have not been added as a location to the randomizer
        # While Items and ShufflableGiftItems have are stored in the same format, AdditionalItems
        # does not contain location information, so we need to read them separately.
        locations_items_file = os.path.join('existing_randomizer', 'locations_items.txt')
        f = load_text_file(locations_items_file)
        reading_items = False
        reading_additional_items = False
        for line in f.splitlines():
            if '===Items===' in line or '===ShufflableGiftItems===' in line:
                reading_items = True
                continue
            elif '===AdditionalItems===' in line:
                reading_additional_items = True
                continue
            elif '===' in line:
                reading_items = False
                reading_additional_items = False
                continue
            if reading_items:
                l = line
                if '//' in line:
                    l = l[:l.find('//')]
                l = l.strip()
                if len(l) == 0: continue
                coords, areaid, rabi_ribi_item_id, name = (x.strip() for x in l.split(':'))

                # Set location coordinate to location name mapping
                area_id = int(areaid)
                x, y = ast.literal_eval(coords)
                ap_name = convert_existing_rando_name_to_ap_name(name)
                if area_id not in coordinate_to_location_name:
                    coordinate_to_location_name[area_id] = {(x, y): ap_name}
                else:
                    coordinate_to_location_name[area_id][(x, y)] = ap_name

                # Set item name to Rabi Ribi item ID mapping
                item_id = int(rabi_ribi_item_id)
                item_name_to_rabi_ribi_item_id[ap_name] = item_id
            if reading_additional_items:
                l = line
                if '//' in line:
                    l = l[:l.find('//')]
                l = l.strip()
                if len(l) == 0: continue
                name, rabi_ribi_item_id = (x.strip() for x in line.split(':'))

                # Only set item name to Rabi Ribi item ID mapping
                ap_name = convert_existing_rando_name_to_ap_name(name)
                item_id = int(rabi_ribi_item_id)
                item_name_to_rabi_ribi_item_id[ap_name] = item_id

        return coordinate_to_location_name, item_name_to_rabi_ribi_item_id

    async def server_auth(self, password_requested: bool = False):
        if password_requested and not self.password:
            await super().server_auth(password_requested)
        await self.get_username()
        await self.send_connect()

    def on_package(self, cmd: str, args: dict):
        super().on_package(cmd, args)
        if cmd == "Connected":
            self.slot_data = args["slot_data"]
            self.seed_player = f"{self.seed_name}-{self.auth}"
            self.seed_player_id = str(hashlib.sha256(self.seed_player.encode()).hexdigest()[:7])
            self.custom_seed_subdir = f"{RabiRibiWorld.settings.game_installation_path}/custom/{self.seed_player}"

            if not os.path.isfile(f"{self.custom_seed_subdir}/area0.map"):
                asyncio.create_task(self.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": self.server_locations
                }]))

        if cmd == "ReceivedItems":
            asyncio.create_task(self.set_received_rabi_ribi_item_ids())

        if cmd == "RoomInfo":
            self.seed_name = args['seed_name']

        elif cmd == "LocationInfo":
            if len(args["locations"]) == len(self.server_locations):
                # initial request on first connect.
                self.patch_if_recieved_all_data()
            else:
                # request after an item is obtained
                asyncio.create_task(self.obtained_items_queue.put(args["locations"][0]))

    def client_recieved_initial_server_data(self):
        """
        This method waits until the client finishes the initial conversation with the server.
        This means:
            - All LocationInfo packages recieved - requested only if patch files dont exist.
            - DataPackage package recieved (id_to_name maps and name_to_id maps are popualted)
            - Connection package recieved (slot number populated)
            - RoomInfo package recieved (seed name populated)
        """
        return (
            self.custom_seed_subdir and
            self.slot
        )

    async def wait_for_initial_connection_info(self):
        """
        This method waits until the client finishes the initial conversation with the server.
        See client_recieved_initial_server_data for wait requirements.
        """
        if self.client_recieved_initial_server_data():
            return

        logger.info("Waiting for connect from server...")
        while not self.client_recieved_initial_server_data() and not self.exit_event.is_set():
            await asyncio.sleep(1)
        if not self.exit_event.is_set():
            # wait an extra second to process data
            await asyncio.sleep(1)
            assert self.slot_data
            self.death_link_enabled = bool(self.slot_data['death_link'])
            await self.update_death_link(self.death_link_enabled)

            logger.info("Received initial data from server!")
            logger.info("****************************************************")
            logger.info("Please press F5 on the main menu and start scenario:")
            logger.info(f"       {self.seed_player}")
            logger.info("****************************************************")
            logger.info("Softlocked? Disable the Strange Box in your inventory and unpause to open the warp menu!")

    def patch_if_recieved_all_data(self):
        """
        See client_recieved_initial_server_data for wait requirements.
        """
        if self.client_recieved_initial_server_data():
            assert self.custom_seed_subdir
            # Patch the map files if we haven't done so already
            if not os.path.isdir(self.custom_seed_subdir):
                os.mkdir(self.custom_seed_subdir)
            if not os.path.isfile(f"{self.custom_seed_subdir}/area0.map"):
                from worlds.rabi_ribi.client.patch import patch_map_files
                patch_map_files(self)

    async def give_item(self):
        """
        Give an item to the player. This method will always give the oldest
        item that the player has recieved from AP, but not in game yet.
        """
        # Find the first item ID that the player has not recieved yet
        last_received_item_index = self.rr_interface.get_last_received_item_index()
        remaining_items = self.items_received_rabi_ribi_ids[last_received_item_index:]
        skipped_items, cur_item_id = next(((idx, item_id) for idx, item_id in enumerate(remaining_items) if item_id != -1), (-1, -1))

        if cur_item_id > 0:
            already_has_item = self.rr_interface.does_player_have_item_id(cur_item_id)
            if not already_has_item:
                self.rr_interface.give_item(cur_item_id)
            # Update index regardless to move to the next item in the queue
            self.rr_interface.set_last_received_item_index(last_received_item_index + skipped_items + 1)
            if not already_has_item:
                await asyncio.sleep(1)
            await self.wait_until_out_of_item_receive_animation()
        elif len(remaining_items) > 0:
            # Update index to mark the player as not waiting for Nothing items
            self.rr_interface.set_last_received_item_index(last_received_item_index + len(remaining_items))

    async def set_received_rabi_ribi_item_ids(self):
        async with self.critical_section_lock:
            self.items_received_rabi_ribi_ids = []
            #  Subtract 30 since those are reserved for shop and super / hyper attack modes
            potion_ids = {
                ItemName.attack_up: 223 - 30,
                ItemName.mp_up: 287 - 30,
                ItemName.regen_up: 351 - 30,
                ItemName.hp_up: 159 - 30,
                ItemName.pack_up: 415 - 30
            }

            for network_item in self.items_received:
                item_name = self.item_names.lookup_in_game(network_item.item)
                if item_name == ItemName.nothing:
                    self.items_received_rabi_ribi_ids.append(-1)
                elif item_name in potion_ids:
                    self.items_received_rabi_ribi_ids.append(potion_ids[item_name])
                    potion_ids[item_name] -= 1
                elif item_name == ItemName.easter_egg:
                    if self.slot_concerns_self(network_item.player):
                        location_name = self.location_names.lookup_in_game(network_item.location)
                        egg_coordinates = self.ap_location_name_to_location_coordinates[location_name]
                        self.collected_eggs.add(egg_coordinates)
                else:
                    self.items_received_rabi_ribi_ids.append(
                        int(self.item_name_to_rabi_ribi_item_id[item_name]))

    def is_item_queued(self):
        """
        To determine if we have any items to give, look at the last recieved item index
        and check if we have received more items.
        """
        if self.items_received:
            last_received_item_index = self.rr_interface.get_last_received_item_index()
            return last_received_item_index < len(self.items_received_rabi_ribi_ids)
        return False

    def is_in_shaft(self):
        """
        Returns true if the player is in the starting shaft. We want to avoid giving them items
        if this is the case since its pitch black so you cant see any of the items that you get.
        """
        area_id, x, y = self.rr_interface.read_player_tile_position()
        return area_id == 0 and \
            ((110 <= x <= 112 and 36 <= y <= 91) or \
             (69 <= x <= 71 and 81 <= y <= 136))

    async def wait_until_out_of_shaft(self):
        """
        Waits until the player is out of the starting shaft, plus a few extra seconds for safety.
        If the player isnt in the starting shaft, returns immediatly.
        """
        if not self.is_in_shaft():
            return
        while self.is_in_shaft() and not self.exit_event.is_set():
            await asyncio.sleep(1)
        if not self.exit_event.is_set():
            await asyncio.sleep(5)

    async def handle_egg_changes(self):
        player_current_eggs = self.rr_interface.get_collected_eggs()
        for (area, x, y) in player_current_eggs:
            if (area, x, y) not in self.collected_eggs:
                self.collected_eggs.add((area, x, y))
                if area in self.location_coordinates_to_ap_location_name and (x, y) in self.location_coordinates_to_ap_location_name[area]:
                    location_name = self.location_coordinates_to_ap_location_name[area][(x, y)]
                    location_id = all_locations[location_name]
                    if location_id not in self.locations_checked:
                        self.locations_checked.add(location_id)
                        await self.check_locations([location_id])

    def handle_consumable_changes(self):
        """
        Checks if the player has any consumable items,
        and sets the events to open them at the start warp point.
        """
        rumi_donut_id = self.item_name_to_rabi_ribi_item_id[ItemName.rumi_donut]
        for item_name in consumable_table.keys():
            item_id = self.item_name_to_rabi_ribi_item_id[item_name]
            if self.rr_interface.does_player_have_item_id(self.item_name_to_rabi_ribi_item_id[item_name]):
                event_id = TRIGGER_BLOCK_EVENT_ID1 + (item_id - rumi_donut_id)
                self.rr_interface.set_event_state(event_id, True)

    async def update_player_location(self):
        area_id, x, y = self.rr_interface.read_player_tile_position()
        if self.current_area_id != area_id:
            self.current_area_id = area_id
            await self.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": f"{self.slot}_{self.team}_rabi_ribi_area_id",
                        "default": 0,
                        "want_reply": False,
                        "operations": [
                            {
                                "operation": "replace",
                                "value": self.current_area_id
                            }
                        ],
                    }
                ]
            )

        room_x = x // 20
        room_y = 0 if y < 12 else (((y - 12) // 45) * 4) + (((y - 12) % 45) // 11)

        if self.current_room != (room_x, room_y):
            self.current_room = (room_x, room_y)
            await self.send_msgs(
                [
                    {
                        "cmd": "Set",
                        "key": f"{self.slot}_{self.team}_rabi_ribi_coords",
                        "default": 0,
                        "want_reply": False,
                        "operations": [
                            {
                                "operation": "replace",
                                "value": self.current_room
                            }
                        ],
                    }
                ]
            )

    def is_player_paused(self):
        paused = self.rr_interface.is_player_paused()
        if paused:
            if self.has_zero_health():
                return False
            self.time_since_last_paused = time.time()
        return paused
    
    def is_player_in_warp_menu(self):
        in_warp_menu = self.rr_interface.is_in_warp_menu()
        if in_warp_menu:
            self.time_since_last_warp_menu = time.time()
        return in_warp_menu

    def is_player_in_costume_menu(self):
        in_costume_menu = self.rr_interface.is_in_costume_menu()
        if in_costume_menu:
            self.time_since_last_costume_menu = time.time()
        return in_costume_menu

    def is_player_in_save_menu(self):
        in_save_menu = self.rr_interface.is_in_save_menu()
        if in_save_menu:
            self.time_since_last_save_menu = time.time()
        return in_save_menu

    def in_state_where_can_give_items(self):
        cur_time = time.time()
        return (
            (cur_time - self.time_since_last_paused >= 2) and
            (cur_time - self.time_since_last_warp_menu >= 5.5) and
            (cur_time - self.time_since_last_costume_menu >= 2) and
            (cur_time - self.time_since_last_save_menu >= 2) and
            not self.rr_interface.is_player_frozen() and
            len(self.death_link_buffer) == 0 and
            self.is_item_queued()
        )

    def in_state_where_should_open_warp_menu(self):
        cur_time = time.time()
        return (
            (cur_time - self.time_since_last_paused >= .5) and
            not self.rr_interface.is_player_frozen() and
            not self.is_item_queued() and
            self.rr_interface.get_item_state(STRANGE_BOX_ITEM_ID) == -1
        )

    async def watch_for_menus(self):
        """
        Run this on a faster loop. We want to detect pauses really fast since players
        can reload a save really fast with quick save reload. We want to make sure that
        we dont give items too soon after a save load since this lags the game hard.
        """
        while self.rr_interface.is_connected() and not self.exit_event.is_set():
            self.is_player_paused()
            self.is_player_in_warp_menu()
            self.is_player_in_costume_menu()
            self.is_player_in_save_menu()
            await asyncio.sleep(0.1)

    def is_on_main_menu(self):
        on_main_menu = self.rr_interface.is_on_main_menu()
        if on_main_menu:
            self.time_since_main_menu = time.time()
        return on_main_menu

    def open_warp_menu(self):
        # Reenable the Strange Box first.
        self.rr_interface.set_item_state(STRANGE_BOX_ITEM_ID, 1)
        if self.is_crosswarp_disabled and self.rr_interface.is_near_crosswarp():
            logger.info("Cannot open the warp menu on a cross-map event tile, please move Erina somewhere else and try again!")
            logger.info("If this issue persists, you may use /disable_crosswarp_check to disable this check.")
            return
        self.rr_interface.open_warp_menu()

    def in_deathlink_eligible_state(self):
        cur_time = time.time()
        return (
            (cur_time - self.time_since_last_paused >= 2) and
            (cur_time - self.time_since_last_warp_menu >= 5.5) and
            (cur_time - self.time_since_last_costume_menu >= 2) and
            (cur_time - self.time_since_last_save_menu >= 2) and
            (cur_time - self.time_since_last_death >= 5.5) and
            not self.rr_interface.is_player_frozen() and
            not self.has_died and
            len(self.death_link_buffer) > 0
        )

    def on_deathlink(self, data: dict):
        self.death_link_buffer.append(data)
        super().on_deathlink(data)

    def trigger_death(self):
        self.rr_interface.set_player_health_to_zero()
        self.time_since_last_death = time.time()
        self.death_link_buffer = []
        self.has_died = True

    def has_zero_health(self):
        return self.rr_interface.has_zero_health()

    def find_closest_item_location(self):
        """
        Finds the closest location to the player for the purpose of finding which
        check they just cleared. Returns None if it cannot find any location within
        10 tiles.

        :returns int, (int, int, int): the ap id of the closest location and the coordinates of it
        """
        # Just recieved an item, mark the closet location as the one found
        area_id, x, y = self.rr_interface.read_player_tile_position()
        closest_location_id = None
        closest_location_coordinates = None
        closest_distance = 9999

        if area_id not in self.location_coordinates_to_ap_location_name:
            return None, None
        for coordinate_entry, location_name in self.location_coordinates_to_ap_location_name[area_id].items():
            if location_name.startswith("Unknown Item"):
                # Skip DLC Items
                continue
            location_id = all_locations[location_name]
            if location_id in self.locations_checked:
                # Ignore already sent locations
                continue
            distance = abs(x - coordinate_entry[0]) + abs(y - coordinate_entry[1])
            if distance < closest_distance:
                closest_distance = distance
                closest_location_id = location_id
                closest_location_coordinates = (area_id, *coordinate_entry)

        if closest_distance < 10 and closest_location_id in self.server_locations:
            return closest_location_id, closest_location_coordinates
        return None, None

    async def wait_until_out_of_item_receive_animation(self):
        """
        Waits until the player is outside the item receive animation, and then returns.
        """
        while self.rr_interface.is_in_item_receive_animation() and not self.exit_event.is_set():
            await asyncio.sleep(0.1)

    def print_egg_amounts(self) -> None:
        if self.client_recieved_initial_server_data():
            assert self.slot_data
            required_egg_count = self.slot_data["required_egg_count"] if "required_egg_count" in self.slot_data else 5
            logger.info(f"You have {len(self.collected_eggs)} Easter Eggs")
            logger.info(f"You need {required_egg_count} Easter Eggs total to beat the game")

    def set_attack_mode_flag(self, mode) -> None:
        """Flags the attack mode for update to a new setting."""
        self.updated_attack_mode = AttackMode.from_any(mode)

    def update_attack_mode(self) -> None:
        """Updates the player's attack mode"""
        MAX_ATTACK_UP_ID = 223
        attack_mode = self.updated_attack_mode
        self.updated_attack_mode = None
        for i in range(0, 30):
            if attack_mode == AttackMode.option_hyper or (i < 20 and attack_mode == AttackMode.option_super):
                self.rr_interface.set_item_state(MAX_ATTACK_UP_ID - i, 1)
            else:
                self.rr_interface.set_item_state(MAX_ATTACK_UP_ID - i, 0)

    def reset_client_state(self):
        """
        Reset client back to default values
        """
        self.locations_checked = set()
        self.location_coordinates_to_ap_location_name, self.item_name_to_rabi_ribi_item_id = \
            self.read_location_coordinates_and_rr_item_ids()

        self.ap_location_name_to_location_coordinates: Dict[str, Tuple[int, int, int]] = {}
        for area, v in self.location_coordinates_to_ap_location_name.items():
            for (x, y), name in v.items():
                self.ap_location_name_to_location_coordinates[name] = (area, x, y)

        self.current_area_id = -1
        self.current_room = (-1, -1)
        self.state_giving_item = False
        self.collected_eggs = set()
        self.seed_name = None
        self.slot_data = None

        self.custom_seed_subdir = None
        self.seed_player = None
        self.seed_player_id = None

        self.time_since_last_paused = time.time()
        self.time_since_main_menu = time.time()
        self.time_since_last_item_obtained = time.time()
        self.time_since_last_warp_menu = time.time()
        self.time_since_last_costume_menu = time.time()
        self.time_since_last_save_menu = time.time()
        self.time_since_last_death = time.time()

        self.items_received_rabi_ribi_ids = []
        self.obtained_items_queue = asyncio.Queue()

        self.is_crosswarp_disabled = True
        self.updated_attack_mode = None
    
    def disable_crosswarp(self):
        self.is_crosswarp_disabled = False
        logger.info("Crosswarp check disabled.")

async def rabi_ribi_watcher(ctx: RabiRibiContext):
    """
    Client loop, watching the rabi ribi game process.
    Handles game hook attachments, checking locations, giving items, etc.

    :RabiRibiContext ctx: The Rabi Ribi Client context instance.
    """
    await ctx.wait_for_initial_connection_info()
    while not ctx.exit_event.is_set():
        if not ctx.server:
            # client disconnected from server
            ctx.reset_client_state()
            await ctx.wait_for_initial_connection_info()
        if not ctx.rr_interface.is_connected():
            logger.info("Waiting for connection to Rabi Ribi")
            await ctx.rr_interface.connect(ctx.exit_event)
            watch_menu_task = asyncio.create_task(ctx.watch_for_menus())
        try:
            while True:
                if not ctx.server:
                    break
                await asyncio.sleep(0.5)
                if ctx.exit_event.is_set():
                    break
                if ctx.seed_player_id is None:
                    continue
                if not ctx.rr_interface.is_on_correct_scenerio(ctx.seed_player_id):
                    continue
                if ctx.is_on_main_menu():
                    continue
                if time.time() - ctx.time_since_main_menu < 4:
                    continue
                break
            if ctx.exit_event.is_set():
                break
            if not ctx.server:
                continue
            await ctx.wait_until_out_of_shaft()

            cur_time = time.time()

            if not ctx.has_zero_health() and (cur_time - ctx.time_since_last_death) >= 5.5:
                ctx.has_died = False

            if ctx.in_deathlink_eligible_state():
                ctx.trigger_death()

            if ctx.has_zero_health() and not ctx.has_died and ctx.death_link_enabled:
                ctx.has_died = True
                ctx.time_since_last_death = time.time()
                await ctx.send_death(f"{ctx.player_names[ctx.slot]} was defeated...")

            await ctx.handle_egg_changes()

            await check_for_locations(ctx)
            await ctx.update_player_location()

            if ctx.in_state_where_should_open_warp_menu():
                ctx.open_warp_menu()

            if ctx.in_state_where_can_give_items():
                await ctx.give_item()

            ctx.handle_consumable_changes()

            if ctx.updated_attack_mode is not None:
                ctx.update_attack_mode()

            # Fallback if player collected items while the client was disconnected.
            #   Make sure the player never has an exclamation point in their inventory.
            #   (or else they wont be able to see/collect any other exclamation point)
            if cur_time - ctx.time_since_last_item_obtained > 7:
                ctx.rr_interface.remove_exclamation_point_from_inventory()

            if ctx.slot_data:
                if (not ctx.finished_game and
                    not ctx.rr_interface.is_on_main_menu() and
                    ctx.rr_interface.does_player_have_item_id(TROPHY_ITEM_ID)):
                    ctx.finished_game = True
                    await ctx.send_msgs([{"cmd": "StatusUpdate", "status": ClientStatus.CLIENT_GOAL}])

        except Exception as err:
            # Process closed trap
            if type(err) is AttributeError and not ctx.rr_interface.is_connected():
                # Stop the ayncio task. No cleanup is necessary
                if watch_menu_task is not None:
                    try:
                        watch_menu_task.cancel()
                    except:
                        pass
                # attempt to reconnect at the top of the loop
                continue

            # Other Errors
            logger.warning("*******************************")
            logger.warning("Encountered error. Please post a message to the Rabi-Ribi thread on the AP discord")
            logger.warning("*******************************")
            logger.exception(str(err))
            # attempt to reconnect at the top of the loop
            continue
        await asyncio.sleep(0.5)

async def check_for_locations(ctx: RabiRibiContext):
    """
    This method checks if the player coordinates overlaps with any location checks.
    If it is, it will update the locations_checked set to include the location
    (if it's not already included).

    :RabiRibiContext ctx: The Rabi Ribi Client context instance.
    """
    # Game paused or just got item
    if ctx.rr_interface.is_in_item_receive_animation():
        ap_location_id, coordinates = ctx.find_closest_item_location()
        if not ap_location_id:
            # logger.warning("Detected item obtained, but unable to find location.")
            return
        if ap_location_id not in ctx.locations_checked:
            ctx.locations_checked.add(ap_location_id)
            await ctx.check_locations([ap_location_id])
            await remove_exclamation_point(ctx, coordinates)

async def remove_exclamation_point(ctx: RabiRibiContext, coordinates):
    ctx.rr_interface.remove_exclamation_point_from_in_memory_map(coordinates[0], coordinates[1], coordinates[2])
    from worlds.rabi_ribi.client.patch import remove_exclamation_point_from_map
    remove_exclamation_point_from_map(ctx, coordinates[0], coordinates[1], coordinates[2])
    while ctx.rr_interface.is_player_frozen():
        await asyncio.sleep(0.25)
    ctx.rr_interface.remove_exclamation_point_from_inventory()

async def main(args):
    """
    Launch a client instance (threaded)
    """
    ctx = RabiRibiContext(args.connect, args.password)
    ctx.server_task = asyncio.create_task(server_loop(ctx), name="Rabi-Ribi Server Loop")

    if tracker_loaded:
        ctx.run_generator()
    if gui_enabled:
        ctx.run_gui()
    ctx.run_cli()

    watcher = asyncio.create_task(
        rabi_ribi_watcher(ctx),
        name="Rabi-Ribi Progression Watcher"
    )
    await ctx.exit_event.wait()
    await watcher
    await ctx.shutdown()

def launch(*args) -> None:
    """
    Launch a client instance (wrapper / args parser)
    """
    parser = get_base_parser(description="Rabi-Ribi Client")
    parser.add_argument("--name", default=None, help="Slot Name to connect as.")
    parser.add_argument("url", nargs="?", help="Archipelago connection url")
    args = parser.parse_args(args)

    if args.url:
        url = urllib.parse.urlparse(args.url)
        args.connect = url.netloc
        if url.username:
            args.name = urllib.parse.unquote(url.username)
        if url.password:
            args.password = urllib.parse.unquote(url.password)

    asyncio.run(main(args))

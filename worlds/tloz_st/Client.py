import itertools

from .DSZeldaClient.DSZeldaClient import *
from .DSZeldaClient.subclasses import storage_key, split_bits
from .data.Addresses import STAddr
from .data.Items import ITEMS
from .data.Entrances import ENTRANCES, entrance_tuple_to_entrance
from settings import get_settings
from typing import Literal
from .Subclasses import EntranceGroups

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor
    from . import SpiritTracksSettings
    from .Subclasses import STTransition

# gMapManager -> mCourse -> mSmallKeys
SMALL_KEY_OFFSET = 0x260
STAGE_FLAGS_OFFSET = 176
TRAIN_SPEED_OFFSET = 0x94
TRAIN_GEAR_OFFSET = 0x27c
ZELDA_TEXT_OFFSET = 276
TRAIN_QUICK_STATION_OFFSET = 0x80
default_train_speed = (-143, 0, 115, 193)

train_speed_addresses = [STAddr.train_speed_reverse, STAddr.train_speed_stop, STAddr.train_speed_med, STAddr.train_speed_fast]

# Addresses to read each cycle
read_keys_always = [STAddr.game_state, STAddr.received_item_index, STAddr.stage, STAddr.room, STAddr.entrance, STAddr.slot_id, STAddr.menu,
                    STAddr.loading_room, STAddr.mid_load, STAddr.saving, STAddr.map_open, STAddr.rabbit_blocker]
read_keys_land = [STAddr.getting_location, STAddr.getting_item_safety, STAddr.health]
read_keys_train = [STAddr.train_health]

rabbit_storage_key = "rabbit_locs"
saved_scene_key = "last_saved_scene"
checked_entrances_key = "st_checked_entrances"
traversed_entrances_key = "st_traversed_entrances"
redisconnected_entrances_key = "st_redisconnected_entrances"
visited_scenes_key = "st_visited_scenes"
processed_locations_key = "st_processed_locations"

def count_bits(n):
    count = 0
    while n:
        n &= n-1
        count += 1
    return count

def get_client_as_command_processor(self: "BizHawkClientCommandProcessor"):
    ctx = self.ctx
    from worlds._bizhawk.context import BizHawkClientContext
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, SpiritTracksClient)
    return client

def cmd_train_option(self: "BizHawkClientCommandProcessor",
                     option: Literal["snap_speed", "quick_station", "speed", "options"] = "options",
                     *args: str):
    """
    Change various train options. Currently implemented:
      - speed <speed: int | "default" | "reset" | "list"> <gear>
      - snap_speed (True): instantly switch to new speeds on changing gear. Never active for stopping gear
      - quick_station (True): enter stations at any speed if gear is on stop
      - options: lists current option values
    """
    # Thanks to Silvris's mm2 implementation for help with bizhawk command processing
    valid_options = ["snap_speed", "quick_station", "speed", "options"]
    option = option.lower()
    if option not in valid_options:
        self.output(f"  \"{option}\" is not a valid option! {valid_options}")
        return False

    if option == "speed":
        return cmd_train_speed(self, *args)

    client = get_client_as_command_processor(self)
    if option == "options":
        self.output(f"  Current train options:")
        self.output(f"    speed: {client.train_speed}")
        self.output(f"    snap_speed: {client.train_snap_speed}")
        self.output(f"    quick_station: {client.train_quick_station}")
        return True

    value = args[0].lower() if args else "true"
    valid_bool_values = {"0": False, "1": True, "false": False, "true": True, "default": True, "reset": True}
    value_bool = valid_bool_values.get(value, None)
    if value_bool is None:
        self.output(f"  \"{value}\" is not a valid boolean!")
        return False

    setattr(client, f"train_{option}", value_bool)
    host_settings: SpiritTracksSettings = get_settings().get('tloz_st_options')
    host_settings.update({f"train_{option}": value_bool})
    self.output(f"  Set option {option} to {value_bool}")
    return True

def cmd_train_speed(self: "BizHawkClientCommandProcessor",
                    speed: int or str = "list",
                    gear: str = "2"):

    def set_speed(speed_list):
        client.train_speed = list(speed_list)
        client.update_train_speed = True
        self.output(f"  Setting train speeds: {speed_list}")
        host_settings: SpiritTracksSettings = get_settings().get('tloz_st_options')
        host_settings.update({f"train_speed": speed_list})

    client = get_client_as_command_processor(self)
    special_speeds = ["list", "default", "reset"]
    if speed in special_speeds:
        if speed == "list":
            self.output(f"  Current train speeds: {client.train_speed}")
            return True
        elif speed in ["default", "reset"]:
            set_speed(default_train_speed)
            return True

    valid_gears = {"reverse": 0, "stop": 1, "slow": 2, "fast": 3,
                   "back": 0, "backwards": 0, "pause": 1, "neutral": 1, "mid": 2, "max": 2,
                   "-1": 0, "0": 1, "1": 2, "2": 3}
    if gear.lower() in valid_gears:
        gear_int = valid_gears[gear]
    else:
        self.output(f"  \"{gear}\" is not a valid gear! {[s for s in valid_gears]}")
        return False

    try:
        speed = min(int(speed), 9999)
        speed = max(speed, -9999)  # soft cap of 9999
    except ValueError:
        self.output(f"  \"{speed}\" is not a valid speed, must be an int or in {special_speeds}")
        return False

    client.train_speed[gear_int] = speed
    set_speed(client.train_speed)
    return True

def cmd_warp_to_start(self: "BizHawkClientCommandProcessor"):
    """Prime a warp to start that triggers on entering any entrance. Run again to cancel"""
    client = get_client_as_command_processor(self)
    client.warp_to_start_flag = not client.warp_to_start_flag
    if client.warp_to_start_flag:
        self.output(f"Primed a warp to start. Enter any entrance or save and quit warp to ")
    else:
        self.output(f"Canceled Warp to Start")
    return True

def cmd_goal(self: "BizHawkClientCommandProcessor"):
    """Display the current goal and progress towards it. Only works while in-game."""
    client = get_client_as_command_processor(self)
    client.display_goal = True
    return True

def cmd_print_actors(self: "BizHawkClientCommandProcessor", offset: int=12):
    """Debug print certain actor data"""
    client = get_client_as_command_processor(self)
    try:
        client.display_actors = int(offset)
    except TypeError:
        self.output(f"Error: Offset needs to be an int")
    return True

def cmd_print_objects(self: "BizHawkClientCommandProcessor", offset: int=0):
    """Debug print certain map object data"""
    client = get_client_as_command_processor(self)
    try:
        client.display_objects = int(offset)
    except TypeError:
        self.output(f"Error: Offset needs to be an int")
    return True

def cmd_count_entrances(self: "BizHawkClientCommandProcessor"):
    """Count how many randomized entrances you have checked out of the total in this seed."""
    client = get_client_as_command_processor(self)
    client.display_entrances = True
    return True

class SpiritTracksClient(DSZeldaClient):
    game = "Spirit Tracks"
    system = "NDS"
    train_speed_addr: "Address"
    train_speed_pointer: "Address"
    train_gear_addr: "Address"

    item_reconnect_lookup, item_and_reconnect_lookup = build_item_name_to_reconnected_entrances()

    def __init__(self) -> None:
        super().__init__()

        # Required variables
        self.starting_flags = STARTING_FLAGS
        self.dungeon_key_data = DUNGEON_KEY_DATA
        self.starting_entrance = (0x2F, 0, 1)  # stage, room, entrance
        self.scene_addr = (STAddr.stage, STAddr.room, STAddr.floor, STAddr.entrance)  # Stage, room, floor, entrance

        self.er_y_offest = 0  # In ph i use coords who's y is 164 off the entrance y
        self.stage_flag_offset = STAGE_FLAGS_OFFSET

        self.in_stamp_stand: bool = False
        self.scene_to_stamp = build_scene_to_stamp()
        self.goal_locations = build_location_to_goal()
        self.location_id_to_location = {l['id']: l for l in LOCATIONS_DATA.values()}
        self.location_id_to_vanilla_item = {l['id']: l.get("vanilla_item", None) for l in LOCATIONS_DATA.values()}

        self.has_goal_location = False
        self.loading_stage = False  # Used to set stage flags mid loading cause the usual time is too late
        self.treasure_tracker: dict = {}
        self.item_data = ITEMS
        self.item_groups = ITEM_GROUPS

        # Mandatory addresses
        self.addr_game_state: "Address" = STAddr.game_state
        self.addr_slot_id: "Address" = STAddr.slot_id
        self.addr_stage: "Address" = STAddr.stage
        self.addr_room: "Address" = STAddr.room
        self.addr_entrance: "Address" = STAddr.entrance
        self.addr_received_item_index: "Address" = STAddr.received_item_index
        self.health_address: "Address" = STAddr.health
        self.mot_active_address: "Address" = STAddr.map_object_table

        self.update_rabbits: bool = False
        self.rabbit_tracker: list[int] = [0]*7  # list of bytes(as ints) for found overworld rabbits
        self.rabbit_counter: list[int] = [0]*5  # list of counts for each rabbit type caught in the overworld

        self.traversed_entrances = set()
        self.checked_entrances = set()
        self.redisconnected_entrances = set()

        self.event_reads: list["Address"] = []
        self.sent_event: bool = False
        self.event_data: list[dict] = []
        self.entrances: dict[str, "STTransition"] = ENTRANCES
        self.boss_warp_entrance = None
        self.location_id_to_name = {loc["id"]: loc_name for loc_name, loc in LOCATIONS_DATA.items()}
        self.exit_coords_addr: tuple = (STAddr.train_trans_x, STAddr.train_trans_y, STAddr.train_trans_z)

        # Train speed stuff
        self.reset_cycles: int = 0
        self.last_train_gear: int = 2
        self.reload_on_item: bool = False
        self.train_snap_speed: bool = True
        self.train_quick_station: bool = True
        self.update_train_speed: bool = False
        self.train_speed = [-143, 0, 115, 193]
        self.set_train_in_overworld: int = 2

        self.key_address = STAddr.small_keys
        self.hint_data = HINT_DATA
        self.got_item_no_loc = False
        self.potion_tracker = [0, 0]
        self.save_ammo = None
        self.drinking_potion = False
        self.addr_drinking_potion = None


        self.boss_key_y = None
        self.boss_key_read = None
        self.snurglar_addr = None
        self.last_anticipated_locations = []
        self.saving = False
        self.saving_safety = False

        self.display_goal: bool = False
        self.display_actors: int = -1
        self.display_objects: int = -1
        self.display_entrances = False
        self.oct_bk_offset = None

        self.selected_station: int = 0
        self.map_warp: None | STTransition = None
        self.unlocked_map: int = 0
        self.has_map_tracks: bool = False
        self.stage_flags: dict[int, list[int]] = STAGE_FLAGS
        self.safe_respawn: tuple[int, int, int] | None = None
        self.warp_portal_addr: Address | None = None
        self.safe_respawn_rooms: list[int] = safe_respawn_rooms
        self.zelda_text_address: Address | None = None

        self.map_warp_item_cache: tuple[bool] | False = None
        self.block_entrance_animation: bool = False

        self.max_total_rabbits: list[int] = [0]*5
        self.processed_locations: set = set()
        self.saved_train_parts: list[int] = []

        self.key_door_watches: list["Address"] = []
        self.boss_door_addr = None
        self.reload_stage_flags: bool = False
        self.reload_map_objects: int = 0
        self.was_in_clog: bool = False
        self.on_train = False

    # Commands

    def printl_goal_info(self, ctx):
        slot_data = ctx.slot_data

        if slot_data["goal"] != -1:
            from .Options import SpiritTracksGoal
            logger.info(f"Your goal is {SpiritTracksGoal(slot_data['goal']).current_key}.")
            return

        if slot_data["endgame_scope"] == 5:
            logger.info(f"Your goal to is enter the Dark Realm.")
        else:
            logger.info(f"Your goal is to defeat Malladus in the Dark Realm.")

        if slot_data["dark_realm_access"] in [0, 1]:
            has_compass = "" if self.item_count(ctx, "Compass of Light") else "don't "
            logger.info(f"You need the Compass of Light to access the Dark Realm. You {has_compass}have it.")
        if slot_data["dark_realm_access"] in [1, 3]:
            specific = "specific " if slot_data.get("require_specific_dungeons", False) else ""
            dungeon_locs = slot_data["required_boss_locs"]
            has_locs = sum([1 for loc in ctx.checked_locations if loc in dungeon_locs])
            logger.info(
                f"You need to complete {specific}dungeons to enter the dark realm. Progress: {has_locs}/{slot_data['dungeons_required']}")
            if slot_data.get("dungeon_hints", 1):
                dungeons_locs = [self.location_id_to_name[i] for i in slot_data["required_boss_locs"]]
                logger.info(f"Your dungeon locations: {dungeons_locs}")
        if slot_data["dark_realm_access"] in [2, 3]:
            shard_count = self.item_count(ctx, "Compass of Light Shard")
            logger.info(
                f"You need Compass Shards to access the Dark Realm. You have {shard_count}/{slot_data['compass_shard_count']}")

    async def print_train_actors(self, ctx, offset=11):
        """Print debug info about actors"""
        actor_table = await self.get_actor_table(ctx)
        actor_idents = await self.get_table_data(ctx, actor_table, offset)
        print(f"Printing Actors")
        identifiers = {
            0x21405e8: "Demon Train",
            0x2140860: "Moink... or not",
            0x22d7184: "Outset Rabbit",
            0x2141438: "False crasher",
            0x21413bc: "One of these crashes",
            0x2149988: "Still Train",
            0x2140efc: "Train Spawner CS Trigger?",
            0x2141854: "Snow realm crasher"
        }

        for k, i in actor_idents.items():
            ident = identifiers.get(i, "")
            print(f"{hex_f(k)}: {hex_f(i)} {ident}")

    async def print_map_objects(self, ctx, offset=0):
        """Print debug info about map objects"""
        table_size = await self.load_map_object_table(ctx)
        actor_idents = await self.get_table_data(ctx, STAddr.map_object_table, offset, table_size=table_size)
        print(f"Printing Map Object Table {offset}")

        for k, i in actor_idents.items():
            ident = ""
            if offset == 0:
                ident = map_object_identifiers.get(i-0x2000000, "")

            print(f"{hex_f(k)}: {hex_f(i)} {ident}")

    async def count_visited_entrances(self, ctx):
        self.checked_entrances |= set(get_stored_data(ctx, checked_entrances_key, set()))
        self.traversed_entrances |= set(get_stored_data(ctx, traversed_entrances_key, set()))

        valid_entrances = [int(e) for e in ctx.slot_data["er_pairings"] if self.entrance_id_to_entrance[int(e)].category_group not in [EntranceGroups.NONE, EntranceGroups.EVENT]]
        valid_entrance_count = len(valid_entrances)
        visited_entrances = [e for e in self.checked_entrances | self.traversed_entrances if self.entrance_id_to_entrance[int(e)].category_group not in [EntranceGroups.NONE, EntranceGroups.EVENT]]
        traversed_entrances = [e for e in self.traversed_entrances if self.entrance_id_to_entrance[int(e)].category_group not in [EntranceGroups.NONE, EntranceGroups.EVENT]]

        remaining = set(valid_entrances) - set(traversed_entrances)
        remaining_names = [self.entrance_id_to_entrance[e].name for e in remaining]

        if ctx.slot_data["ut_blocked_entrances_behaviour"] == 2:
            logger.info(f"You have checked {len(traversed_entrances)}/{len(visited_entrances)}/{valid_entrance_count} entrances (traversed/checked/total).")
            printl(f"Remaining entrances: {remaining_names}")
        else:
            logger.info(f"You have checked {len(traversed_entrances)}/{valid_entrance_count} entrances (checked/total).")


    # Utility

    # @staticmethod
    # def in_game_comparison(in_game):
    #     return in_game

    async def get_small_key_address(self, ctx) -> int:
        return STAddr.small_keys

    def get_coord_address(self, at_sea=None, multi=False):
        return STAddr.link_x, STAddr.link_y, STAddr.link_z

    async def get_coords(self, ctx, multi=False):
        # printl(f"Coords: {[self.read_result.get(a, 0) for c, a in zip(['x', 'y', 'z'], self.get_coord_address())]}")
        # return {c: self.read_result.get(a, 0) for c, a in zip(['x', 'y', 'z'], self.get_coord_address())}
        if self.current_stage < 0x13:
            coords = await read_multiple(ctx, STAddr.train_coords, True)
            train_coords = {l: c for c, l in zip(coords.values(), ['x', 'y', 'z'])}
            # printl(f"Train coords: {train_coords}")
            return train_coords
        coords = await read_multiple(ctx, self.get_coord_address(multi=multi), signed=True)
        # printl(f"Coords: {coords}")
        return {
            "x": coords[STAddr.link_x],
            "y": coords[STAddr.link_y],
            "z": coords[STAddr.link_z]
        }

    @staticmethod
    async def get_table_data(ctx, array_start, comp_offset, size:int or list=4, table_label=True, table_size=128) -> dict["Address", int | list[int]]:
        """
        Collect data from a table of pointers at a given offset.
        """

        rl = []
        for i in range(table_size):
            rl.append(Address.from_pointer(array_start + i * 4, size=3))
        actors = await read_multiple(ctx, rl)
        # print(f"Objects: {hex_f(actors)}")

        if table_label:
            labels = [k for k, v in actors.items() if v]
        else: labels = None

        # Multiple offsets at once
        if isinstance(comp_offset, Iterable):
            actors_start = [[Address.from_pointer(v, size=i) for v in actors.values() if 0 < v < 0x400000] for i in size]
            reads: dict["Address", list[int]] = {}
            for i, offset in enumerate(comp_offset):
                reads_2 = await read_multiple(ctx, actors_start[i], offset=offset * 4, keys=labels)
                for r, v in reads_2.items():
                    reads.setdefault(r, [0]*len(comp_offset))[i] = v
            return reads

        # single offset
        actors_start = [Address.from_pointer(v, size=size) for v in actors.values() if 0 < v < 0x400000]
        reads_2 = await read_multiple(ctx, actors_start, offset=comp_offset * 4, keys=labels)
        return reads_2

    @staticmethod
    async def get_actor_table(ctx):
        await STAddr.actor_table.load(ctx)
        return STAddr.actor_table

    @staticmethod
    async def load_map_object_table(ctx):
        pointer = await STAddr.gMapObjectManager.read(ctx)
        reads = await read_multiple(ctx, [Address.from_pointer(pointer, size=3), Address.from_pointer(pointer+4, size=3)])
        start, last = list(reads.values())
        STAddr.map_object_table.set_addr(start)
        size = (last-start)//4
        print(f"Start, last: {hex_f(start)}, {hex_f(last)} = {size}")

        return size

    async def has_special_dynamic_requirements(self, ctx: "BizHawkClientContext", data) -> bool:
        def check_dungeon_reqs():
            if "dungeons" in data:
                if ctx.slot_data["dark_realm_access"] not in [1, 3]:
                    return data["dungeons"]  # Case where dungeons are not required for dark realm
                printl(f"{ctx.slot_data['required_boss_locs']}")
                dungeon_locs = ctx.slot_data["required_boss_locs"]
                has_locs = sum([1 for loc in ctx.checked_locations if loc in dungeon_locs])
                comp = has_locs >= ctx.slot_data["dungeons_required"]
                printl(f"Checking dungeons: {has_locs} >= {ctx.slot_data['dungeons_required']} for comp {data['dungeons']}")
                return comp == data["dungeons"]
            return True

        async def check_coords():
            coord_data = data.get("coords", {})
            if coord_data:
                coords = await self.get_coords(ctx)
                printl(f"\t\tCoords: {coords} reqs {coord_data}")
                print(f"\t{coord_data.get('x_max', 0xFFFFFFF)} > {coords['x']} > {coord_data.get('x_min', -0xFFFFFFF)} = {coord_data.get('x_max', 0xFFFFFFF) > coords['x'] > coord_data.get('x_min', -0xFFFFFFF)}")
                return all([
                    coord_data.get("x_max", 0xFFFFFFF) > coords['x'] > coord_data.get("x_min", -0xFFFFFFF),
                    coord_data.get("y", coords['y']) + 2000 > coords['y'] >= coord_data.get("y", coords['y']),
                    coord_data.get("z_max", 0xFFFFFFF) > coords['z'] > coord_data.get("z_min", -0xFFFFFFF),
                ])

            return True

        def check_visited_scenes():
            desired_scenes = data.get("visited_scenes", [])
            if not desired_scenes:
                return True

            visited_scenes = get_stored_data(ctx, visited_scenes_key, [])
            for scene in desired_scenes:
                if scene in visited_scenes:
                    return True
            printl(f"\t{data['name']} has not visited scenes {hex_f(desired_scenes)} {get_stored_data(ctx, visited_scenes_key, [])}")
            return False

        def check_unvisited_scenes():
            desired_scenes = data.get("not_visited_scenes", [])
            if not desired_scenes:
                return True

            visited_scenes = get_stored_data(ctx, visited_scenes_key, [])
            for scene in desired_scenes:
                if scene in visited_scenes:
                    printl(f"\t{data['name']} has visited bad scenes {hex_f(desired_scenes)}")
                    return False
            return True

        def check_traversed_entrances():
            entrances = data.get("has_traversed_entrances", [])
            if not entrances:
                return True
            if not self.traversed_entrances:
                return False

            for e in entrances:
                if ENTRANCES[e].id not in self.traversed_entrances:
                    return False
            return True


        if not check_dungeon_reqs():
            printl(f"\t{data['name']} does not have dungeon requirements")
            return False
        if not await check_coords():
            printl(f"\t{data['name']} does not have coordinate requirements")
            return False
        if not check_visited_scenes():
            return False
        if not check_unvisited_scenes():
            return False
        if not check_traversed_entrances():
            printl(f"\t{data['name']} has not traversed entrances")
            return False

        # Update stage flags
        if "update_stage_flags" in data and "on_scenes" in data:
            printl(f"\t{data['name']} is setting stage flags")
            self.update_stage_flag((data["on_scenes"][0] & 0xFF00) >> 8, data["update_stage_flags"])

        return True

    def custom_er_message(self, ctx, message):
        if message == "$goal":
            logger.info(f"You're missing dark realm requirements")
            self.printl_goal_info(ctx)

    async def store_event(self, ctx, event_name: str):
        await self.store_events(ctx, [event_name])

    async def store_events(self, ctx, event_list: Iterable[str]):
        print(f"Storing Events: {event_list}")
        entrance_ids = {ENTRANCES[e].id for e in event_list}
        key = storage_key(ctx, traversed_entrances_key)
        self.traversed_entrances |= set(get_stored_data(ctx, key, set()))
        new_events = {e for e in entrance_ids if e not in self.traversed_entrances}
        if new_events:
            print(f"\tStoring new events: {new_events}")
            await self.store_data(ctx, key, new_events)
        self.traversed_entrances.update(new_events)

    async def refill_ammo(self, ctx, text=""):
        await self.full_heal(ctx)
        if self.item_count(ctx, "Bomb Bag"):
            bomb_prog = 1 + self.item_count(ctx, "Bomb Bag Upgrade")
        else:
            bomb_prog = self.item_count(ctx, "Bombs (Progressive)")
        if self.item_count(ctx, "Bow"):
            arrow_prog = 1 + self.item_count(ctx, "Quiver Upgrade")
        else:
            arrow_prog = self.item_count(ctx, "Bow (Progressive)")
        if bomb_prog:
            bomb_prog = min(bomb_prog, len(self.item_data["Bombs (Progressive)"].give_ammo))
            await STAddr.bomb_count.overwrite(ctx, self.item_data["Bombs (Progressive)"].give_ammo[bomb_prog-1])
        if arrow_prog:
            arrow_prog = min(arrow_prog, len(self.item_data["Bow (Progressive)"].give_ammo))
            await STAddr.arrow_count.overwrite(ctx, self.item_data["Bow (Progressive)"].give_ammo[arrow_prog-1])

    async def full_heal(self, ctx, bonus=0):
        hearts = (self.item_count(ctx, "Heart Container") + 3)*4
        printl(f"Full Heal: {hearts}")
        await STAddr.health.overwrite(ctx, hearts+bonus)

    # Initialization

    async def check_game_version(self, ctx: "BizHawkClientContext") -> bool:
        rom_name_bytes = await STAddr.game_identifier.read_bytes(ctx)
        rom_name = bytes([byte for byte in rom_name_bytes[0] if byte != 0]).decode("ascii")
        printl(f"Rom Name: {rom_name}")
        if rom_name == "SPIRITTRACKSBKIP":  # EU
            version = await STAddr.game_version.read(ctx)
            if version != 0:
                logger.info(f"Wrong rom version 1.{version}, please use version 1.0")
                return False

            # Set commands
            if "train_speed" not in ctx.command_processor.commands:
                ctx.command_processor.commands["train"] = cmd_train_option
            if "warp_to_start" not in ctx.command_processor.commands:
                ctx.command_processor.commands["warp_to_start"] = cmd_warp_to_start
            if "goal" not in ctx.command_processor.commands:
                ctx.command_processor.commands["goal"] = cmd_goal
            if "print_actors" not in ctx.command_processor.commands:
                ctx.command_processor.commands["print_actors"] = cmd_print_actors
            if "print_objects" not in ctx.command_processor.commands:
                ctx.command_processor.commands["print_objects"] = cmd_print_objects
            if "count_entrances" not in ctx.command_processor.commands:
                ctx.command_processor.commands["count_entrances"] = cmd_count_entrances
            return True
        elif rom_name == "SPIRITTRACKSBKIE":  # US
            logger.info(f"The US Version is not supported yet, please use the EU version 1.0")
        return False

    # Main Loop

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        await super().game_watcher(ctx)


    def clear_variables(self):
        pass

    async def update_main_read_list(self, ctx: "BizHawkClientContext", stage: int, in_game=True):
        read_keys = read_keys_always.copy()
        if stage in range(4, 0xb):
            self.on_train = True
            read_keys += read_keys_train
            self.health_address = STAddr.train_health

            train_speed_thingy = (await STAddr.train_speed_pointer.read(ctx))
            printl(f"Train speed thingy {hex(train_speed_thingy)}")
            if 0x400000 > train_speed_thingy > 0:
                self.train_speed_pointer = train_speed_thingy
                self.train_gear_addr = Address.from_pointer(self.train_speed_pointer+TRAIN_GEAR_OFFSET)
                read_keys.append(self.train_gear_addr)
        else:
            self.on_train = False
            read_keys += read_keys_land
            self.health_address = STAddr.health

            offset = 0xf80 if self.current_stage == 0x29 else 0xf64
            potion_addr = await STAddr.drinking_potion_pointer.read(ctx) - 0x2000000 + offset
            if 0x400000 > potion_addr > 0:
                self.addr_drinking_potion = Address.from_pointer(potion_addr, size=4)
                read_keys.append(self.addr_drinking_potion)
            printl(f"Potion pointer {hex(potion_addr)}")

            self.mot_active_address = Address.from_pointer(await STAddr.gMapObjectManager.read(ctx)+3)
            read_keys.append(self.mot_active_address)

            if stage == 0x13:
                self.zelda_text_address = Address.from_pointer(await STAddr.zelda_pointer.read(ctx) + ZELDA_TEXT_OFFSET, size=4)
                print(f"Zelda text address: {self.zelda_text_address}")
                read_keys.append(self.zelda_text_address)


        self.main_read_list = read_keys
        printl(f"read keys len: {len(read_keys)}")
        printl(self.main_read_list, read_keys)
        # printl(f"Slot data {ctx.slot_data}")

    async def on_connect(self, ctx):
        self.rabbit_tracker = [0]*7
        keys_to_fetch = [
            rabbit_storage_key,
            saved_scene_key,
            checked_entrances_key,
            traversed_entrances_key,
            redisconnected_entrances_key,
            visited_scenes_key,
            processed_locations_key
        ]
        await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [storage_key(ctx, k) for k in keys_to_fetch],
            }])

        # Get train settings from host.yaml
        host_settings: SpiritTracksSettings = get_settings().get('tloz_st_options')
        printl(f"SETTINGS: {host_settings.get('train_speed', self.train_speed)}")
        self.train_speed = host_settings.get("train_speed", self.train_speed)
        self.train_snap_speed = host_settings.get("train_snap_speed", self.train_snap_speed)
        self.train_quick_station = host_settings.get("train_quick_station", self.train_quick_station)

    async def process_in_menu(self, ctx, read_result):
        await self.get_saved_scene(ctx, saved_scene_key)

    async def watched_intro_cs(self, ctx):
        if not STAddr.adv_flags_1:
            s = STAddr.watched_intro
            print(s)
            await load_adv_flags(ctx)
            print(f"intr addr: {STAddr.watched_intro}")

        watched_intro = await STAddr.watched_intro.read(ctx, silent=True) & 1
        if not watched_intro and await STAddr.fade_timer.read(ctx, silent=True) < 0xffff:
            self.precision_mode = [STAddr.stage, 0x79, "wts"]
        return watched_intro

    async def _set_starting_flags(self, ctx):
        await super()._set_starting_flags(ctx)

        # Process bonus starting locations
        for i in range(1, 11):
            await self._process_checked_locations(ctx, f"Bonus Starting Item {i}")

    async def set_special_starting_flags(self, ctx: "BizHawkClientContext") -> list[tuple[int, list, str]]:
        res = []
        if ctx.slot_data.get("shuffle_hyrule_castle", 0) > 0:
            res.append(STAddr.adv_flags_6.get_inner_write_list(0xFC))
        if ctx.slot_data["enable_map_warp"]:
            res.append(STAddr.adv_flags_1.get_inner_write_list(0x80))

        return res

    async def enter_game(self, ctx):
        starting_entr = ENTRANCES[ctx.slot_data["starting_entrance"]]
        self.starting_entrance = starting_entr.entrance
        self.safe_respawn_rooms = safe_respawn_rooms + [starting_entr.scene]

        self.checked_entrances |= set(get_stored_data(ctx, checked_entrances_key, set()))
        self.traversed_entrances |= set(get_stored_data(ctx, traversed_entrances_key, set()))
        self.redisconnected_entrances |= set(get_stored_data(ctx, redisconnected_entrances_key, set()))
        self.visited_scenes |= set(get_stored_data(ctx, visited_scenes_key, set()))

        # Set settings specific stage flags
        if ctx.slot_data["open_blue_warps"]:
            for stage, flags in zip(range(0x19, 0x1E), OPEN_WARPS):
                self.update_stage_flag(stage, flags)

        self.get_max_total_rabbit_counts(ctx)

        if ctx.slot_data["starting_train"] == -1:
            await self.save_custom_train(ctx)

    async def process_read_list(self, ctx: "BizHawkClientContext", read_result: dict):
        # reload when necessary
        if not self.reload_map_objects and read_result.get(self.mot_active_address, 2) != 2:
            self.reload_map_objects = 1

        if self.precision_operation and self.precision_operation[0] == "special_ow_actors":
            printl(f"Starting delete operation")
            self.precision_operation = []
            await self._set_er_coords(ctx)
            await self.setup_evil_train_deletion(ctx, "delete_ow_actors", 0)

        current_menu: "Address" = read_result[STAddr.menu]

        # Getting location reads
        if not self.on_train:
            self.in_stamp_stand = current_menu == 0x0E

            getting_location = read_result[STAddr.getting_location] and not read_result[STAddr.saving] and not self.saving
            self.getting_location = getting_location or self.reset_cycles

            if self.getting_location:
                self.reset_cycles = True

            if self.reset_cycles and not getting_location and not read_result[STAddr.getting_item_safety]:
                self.reset_cycles = False

            # Fix for stamp stand not counting as getting item
            if self.in_stamp_stand and self.receiving_location:
                self.getting_location = True

        if not self.saving:
            self.saving = read_result[STAddr.saving]
            self.saving_safety = read_result.get(STAddr.getting_item_safety)
        else:
            safe_save = False
            if self.current_stage in range(0x1e, 0x23):
                safe_save = self.saving_safety == read_result[STAddr.getting_item_safety]
                # printl(f"Checking Safe Save!")
            self.saving = read_result.get(STAddr.getting_item_safety, False) or read_result[STAddr.saving] or safe_save

        # Weird scene value on load from menu, set to last saved scene
        if read_result[STAddr.stage] == 0x79 and self.last_saved_scene:
            stage = (self.last_saved_scene & 0xFF00) >> 8

            printl(f"Overwriting weird scene: {hex(self.last_saved_scene)}")
            stage, room = (self.last_saved_scene & 0xFF00) >> 8, self.last_saved_scene & 0xFF

            self.current_scene = self.last_saved_scene
            self.current_stage = read_result[STAddr.stage] = stage
            read_result[STAddr.room] = room
            printl(hex(self.current_scene), hex(self.current_stage))
            await STAddr.stage.overwrite(ctx, stage)
            await STAddr.room.overwrite(ctx, room)

        # printl(f"Goal check {ctx.slot_data['goal']} last {self.last_stage} current {hex(self.current_stage)}")
        if ctx.slot_data["goal"] == -1:
            if self.last_stage == 0x27 and self.current_stage == 0x25:
                self.has_goal_location = True
                await self.store_event(ctx, "GOAL: Defeat Malladus")

        # Precise delete bad train actors when missing glyphs
        if self.precision_operation and self.precision_operation[0] == "delete_ow_actors":
            await self.frame_advance(ctx)  # lol it be picky
            await self.delete_bad_ow_actors(ctx, self.precision_operation[1])
            if (self.current_entrance == 4 and self.current_stage == 4) or (self.current_entrance == 1 and self.current_stage == 0x5):
                await STAddr.entrance_animation.overwrite(ctx, 0x30)
                self.block_entrance_animation = True
            self.precision_operation = []
            await bizhawk.unlock(ctx.bizhawk_ctx)
            ctx.watcher_timeout = 0.1

    def process_loading_variable(self, read_result) -> bool:
        mid_load = read_result.get(STAddr.mid_load, True) == 0xFF
        if self._loading_scene and not self.loading_stage:
            if mid_load:
                self.loading_stage = True

        if self.loading_stage:
            if not mid_load:
                self.loading_stage = False
                return mid_load

        return not read_result.get(STAddr.loading_room, 27) and read_result[STAddr.menu] in [0, 0x1, 0x4, 0xFF]

    async def detected_new_scene(self, ctx):
        await self.save_tos_keycount(ctx)
        self.event_reads = []
        self.sent_event = False
        self.boss_key_y = None
        self.boss_door_addr = None
        if self.last_scene == 0x700:
            await self.reset_snurglar_door(ctx)

        if self.current_scene in potion_location_lookup:
            printl(f"Setting shop models")
            await self.set_shop_models(ctx)

        await self.change_entrance_animation(ctx)

        if not self._just_entered_game and self.last_stage == self.current_stage and self.current_stage in [4, 5]:
            printl(f"Starting special operation")
            await self.setup_evil_train_deletion(ctx, "special_ow_actors", 2)
            print(f"Setup special operation {self.precision_operation}")


    async def process_on_room_load(self, ctx, current_scene, read_result: dict):
        await self.update_treasure_tracker(ctx, "room_load")
        await self.update_potion_tracker(ctx, "room_load")
        await self.update_rabbit_count(ctx)

        # printl(F"Room load goal: {ctx.slot_data['goal']}, {ctx.slot_data['endgame_scope']}, {self.current_stage}")
        if (ctx.slot_data["goal"] == -1 and ctx.slot_data["endgame_scope"] == 5
                and self.current_stage in [0xF, 0x10, 0x24, 0x25, 0x27]):
            self.has_goal_location = True
            await self.store_event(ctx, "GOAL: Enter Dark Realm")

        if self.reload_stage_flags:
            await self.set_stage_flags(ctx, self.current_stage)

    async def process_hard_coded_rooms(self, ctx, current_scene):
        printl(f"Processing hard coded room stuff")
        self.reload_map_objects = 1

        if self.save_ammo:
            await write_multiple(ctx, list(self.save_ammo.keys()), list(self.save_ammo.values()))
            self.save_ammo = None

        if current_scene in ammo_shop_lookup and "ammo" in ctx.slot_data["shopsanity"]:
            ammo_addresses = [STAddr.bomb_count, STAddr.arrow_count]
            self.save_ammo = await read_multiple(ctx, ammo_addresses)
            await write_multiple(ctx, ammo_addresses, [0, 0])

        # Give tears of light when entering ToS
        if self.current_stage == 0x13 and ctx.slot_data["randomize_tears"] != -1:
            await self.set_tears(ctx)

        if current_scene not in potion_location_lookup:
            treasure = None
            if ctx.slot_data["excess_random_treasure"] == 2:
                treasure = ITEM_MODEL_LOOKUP["Red Rupee"].value
            elif ctx.slot_data["excess_random_treasure"] == 0:
                treasure = ITEM_MODEL_LOOKUP["Nothing"].value
            await self.reset_treasure_models(ctx, treasure)

        if current_scene == 0x131e:  # Set tears for ToS 6 on 30F instead of 31F.
            await self.set_tears(ctx)

        # Start Precision read for evil train deletion
        if not self._just_entered_game:
            await self.setup_evil_train_deletion(ctx, "delete_ow_actors", 0)

        # Save visited scenes
        if ctx.slot_data.get("enable_map_warp", 1) or ctx.slot_data["passenger_pickup"] == 1:
            warp_data = WARP_SCENES.get(self.current_scene, False)
            if warp_data and warp_data.is_valid(self.current_entrance, ctx.slot_data):
                if self.current_scene not in self.visited_scenes:
                    await self.store_data(ctx, storage_key(ctx, visited_scenes_key), [self.current_scene])
                    self.visited_scenes.add(self.current_scene)
                print(f"Visited {warp_data.region}")
                if warp_data.event:
                    event_entr = ENTRANCES[warp_data.event]
                    await self.store_visited_entrances(ctx, event_entr, event_entr.vanilla_reciprocal)

        print(f"last scene {hex_f(self.last_scene)}")
        if self.last_scene == 0x2f0B and ctx.slot_data["starting_train"] == -1:
            await self.save_custom_train(ctx)

        if current_scene == 0x2F0B and ctx.slot_data["starting_train"] == -1:
            self.set_train_in_overworld: int = 0

        # Validate locations
        await self.validate_location_processing(ctx)

    async def delay_room_action(self, ctx):
        print(f"# Delay Room Action")
        # Set train speed stuff
        if self.on_train:
            await self.set_train_speed(ctx)

        # await self.process_map_objects(ctx)

        # Set starting train
        if not await STAddr.set_starting_train.read(ctx) & 4:
            await self.set_starting_train(ctx)
            await STAddr.set_starting_train.set_bits(ctx, 4)

        # Set Shop Models for on purchase
        if self.current_scene in potion_location_lookup:
            await self.set_shop_models(ctx, False)

        # Lift item restrictions in TEAO boss rooms
        if self.current_scene in range(0x4b00, 0x5000):
            await STAddr.item_restrictions.overwrite(ctx, 0)

        # Change respawn data in special scenes
        if self.current_stage in special_respawn_stages:
            await write_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room, STAddr.respawn_entrance],
                                 special_respawn_stages[self.current_stage])
        elif self.safe_respawn:
            await write_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room, STAddr.respawn_entrance],
                                 self.safe_respawn)

        # Change respawn data to outside tower section in ToS
        if self.current_stage == 0x13:
            section = TOS_FLOOR_TO_SECTION[self.current_room]
            entrance = self.entrances[TOS_SECTION_TO_EXIT[section]]
            reverse_entrance: "STTransition" = self.entrance_id_to_entrance[
                ctx.slot_data["er_pairings"][str(entrance.id)]] if str(entrance.id) in ctx.slot_data[
                "er_pairings"] else entrance.vanilla_reciprocal
            respawn_data = reverse_entrance.entrance
            printl(f"Setting ToS respawn room {respawn_data}")
            await write_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room, STAddr.respawn_entrance],
                                 respawn_data)

        # Set key watches
        await self.load_boss_key_watch(ctx)

        # Set up snurglar reads
        if self.current_scene == 0x700:
            await self.set_up_snurglar_data(ctx)
        else:
            self.snurglar_addr = None

        # Move mtt b1 heatoise arena hitbox
        if self.current_scene == 0x1c02 and self.current_entrance != 3:
            # Amazing that this works at all
            pointer = await STAddr.mtt_b1_heatoise_trigger_pointer.read(ctx)
            await Address.from_pointer(pointer+1384, 4).overwrite(ctx, 70000)

    async def process_in_game(self, ctx, read_result: dict):
        if not read_result.get(STAddr.rabbit_blocker, 2):
            printl(f"Rabbit Blocker!")
            return

        await super().process_in_game(ctx, read_result)
        # Detect stamp stand locations
        if self.in_stamp_stand and not self.receiving_location:
            self.receiving_location = True
            stamp_location = self.scene_to_stamp[self.current_scene]
            await self.update_stamps(ctx)
            await self._process_checked_locations(ctx, stamp_location)

        await self.detect_boss_key(ctx)
        await self.process_train_speed(ctx, read_result)
        await self.detect_ut_event(ctx, self.current_scene)
        await self.process_map_warp(ctx)

        if self.current_stage == 0x13:
            if self.read_result[self.zelda_text_address] == 0x30000:
                link_coords = await self.get_coords(ctx)
                zelda_pointer = await STAddr.zelda_pointer.read(ctx)
                await write_multiple(ctx, [Address.from_pointer(zelda_pointer + 7*4 + i*4, size=4) for i in range(3)],
                                     list(link_coords.values()))
            elif self.read_result[self.zelda_text_address] not in [0xFFFFFFFF, 0xd0024]:
                await self.zelda_text_address.overwrite(ctx, 0xFFFFFFFF)

        if read_result[STAddr.menu] == 9:
            clog = await STAddr.flip_clog.read(ctx, silent=True)
            if clog == 0x14 and not self.warp_to_start_flag:
                self.warp_to_start_flag = True
                stage = ENTRANCES[ctx.slot_data["starting_entrance"]].stage
                logger.info(f"Primed a warp to start. Enter any entrance or save and quit warp to {STAGES.get(stage, 'ERROR')}.")
            elif clog == 0 and self.warp_to_start_flag:
                self.warp_to_start_flag = False
                logger.info("Canceled warp to start.")
            elif self.map_warp:
                self.map_warp = None
                logger.info("Canceled map warp.")

            if not self.was_in_clog:
                await self.update_stamps(ctx)
                self.was_in_clog = True
        elif read_result[STAddr.menu] < 9:
            self.was_in_clog = False

    async def process_slow(self, ctx: "BizHawkClientContext", read_result: dict):
        await self.anticipate_location(ctx, read_result)

        if self.display_goal:
            self.printl_goal_info(ctx)
            self.display_goal = False
        if self.display_entrances:
            await self.count_visited_entrances(ctx)
            self.display_entrances = False

        if self.display_actors > -1:
            await self.print_train_actors(ctx, self.display_actors)
            self.display_actors = -1
        if self.display_objects > -1:
            await self.print_map_objects(ctx, self.display_objects)
            self.display_objects = -1

    async def process_fast(self, ctx: "BizHawkClientContext", read_result: dict):
        await self.save_scene(ctx, read_result, STAddr.saving, saved_scene_key, range(1, 5))
        await self.drink_potion(ctx, read_result)

        if self.reload_map_objects == 1 and read_result.get(self.mot_active_address, 0) == 2:
            self.reload_map_objects = 0
            await self.process_map_objects(ctx)

        if self.snurglar_addr in read_result:
            if read_result[self.snurglar_addr] & 0x20:
                printl(f"Opening Mountain Temple! {self.snurglar_addr}")
                await self.snurglar_addr.set_bits(ctx, 0x10)
                self.main_read_list.remove(self.snurglar_addr)

        # Prevent key door cs skips from opening too slow and closing again
        if self.key_door_watches:
            reads = await read_multiple(ctx, self.key_door_watches)
            for a, v in reads.items():
                if 8 > v > 2:
                    await write_multiple(ctx, [a, Address.from_pointer(a+27*4, 1)], [7, 0xff])
                    self.key_door_watches.remove(a)
                    if self.current_stage == 0x13:
                        await self.save_tos_keycount(ctx)
                    break
                if v == 8:
                    self.key_door_watches.remove(a)

    # Misc item handling

    async def receive_item_post_processing(self, ctx, item_name, item_data):
        printl(f"Post Processing {item_name}")

        if "Rabbit" in item_name:
            await self.update_rabbit_count(ctx)
        if "Treasure:" in item_name:
            await self.update_treasure_tracker(ctx, "item_process")
        if item_name in ["Bombs (Progressive)", "Bomb Bag"] and self.current_scene == 0x4503:
            await STAddr.adv_flags_22.unset_bits(ctx, 2)

        if self.reload_on_item:
            printl(f"Reloading dynamic entrances")
            self.reload_on_item = False
            await self._set_dynamic_entrances(ctx, self.current_scene)
            await self._set_dynamic_flags(ctx, self.current_scene)
        if item_name == "Compass of Light Shard" and ctx.slot_data["dark_realm_access"] in [2, 3]:
            required_shards = ctx.slot_data["compass_shard_count"]
            if self.item_count(ctx, "Compass of Light Shard") >= required_shards:
                logger.info(f"Got {required_shards} Compass of Light Shards, unlocking the track to the Dark Realm!")
                await STAddr.rail_restorations.set_bits(ctx, 0x40)
                await STAddr.adv_flags_25.set_bits(ctx, 0x60)

        # Get spirit weapons from final tear of light
        if "Tear of Light" in item_name and ctx.slot_data["spirit_weapons"] == 1:
            section_count = min(5, ctx.slot_data["section_count"])
            if any([
                self.item_count(ctx, "Tear of Light (All Sections)") >= 4,
                self.item_count(ctx, "Tear of Light (Progressive)") >= section_count*3 + 1,
                self.item_count(ctx, "Big Tear of Light (All Sections)") >= 2,
                self.item_count(ctx, "Big Tear of Light (Progressive)") >= section_count + 1]):
                await STAddr.adv_flags_16.set_bits(ctx, 1)
                await STAddr.items_2.set_bits(ctx, 4)
                logger.info(f"You Unlocked the Lokomo Sword and the Bow of Light!")

        if item_name in ["Cannon", "Wagon"] and ctx.slot_data["starting_train"] != -1:
            await self.reset_train_model(ctx)

        if "ammo" in ctx.slot_data["shopsanity"] and self.current_scene in ammo_shop_lookup and item_name in ITEM_GROUPS["Ammo Items"]:
            addr = item_data.ammo_address if hasattr(item_data, "ammo_address") else item_data.address
            await addr.overwrite(ctx, 0)
            item_count = self.item_count(ctx, item_data.refill) if item_name in ITEM_GROUPS["Refill Items"] else self.item_count(ctx, item_name)
            self.save_ammo[addr] = item_data.give_ammo[item_count-1]

        # Open boss door if got key in that room
        if (item_name.startswith("Boss Key") or
            (item_name.startswith("Keyring") and ctx.slot_data["big_keyrings"])
        ) and self.current_scene in BOSS_KEY_DATA and self.boss_door_addr:
            await self.open_boss_door(ctx, self.boss_door_addr)

        # Complex blocked scenes for sources in boss rooms
        if (self.current_scene in BOSS_ROOM_TO_BLOCKED_ITEM_GROUP and
            BOSS_ROOM_TO_BLOCKED_ITEM_GROUP[self.current_scene] in item_data.item_groups):
            bit = 2 ** (self.current_stage-0x1a)
            await STAddr.sources.unset_bits(ctx, bit)

        if ctx.slot_data.get("ut_blocked_entrances_behaviour") == 2:
            await self.check_item_disconnects(ctx, item_name)

    async def update_potion_tracker(self, ctx, spec=""):
        reads = await read_multiple(ctx, [STAddr.potion_0, STAddr.potion_1])
        new_potions = list(reads.values())
        res = False
        if new_potions != self.potion_tracker:
            printl(F"New Potions: {new_potions} {spec}")
            res = True
        self.potion_tracker = new_potions
        return res

    async def check_potion_location(self, ctx):
        """Checks for potion locations in shops if treasure tracker doesn't find a treasure on a location"""
        if self.current_scene in potion_location_lookup and "potions" in ctx.slot_data["shopsanity"]:
            empty_slots = [addr for addr, prev in zip([STAddr.potion_0, STAddr.potion_1], self.potion_tracker) if prev == 0]
            if not empty_slots:
                return
            slot = await empty_slots[0].read(ctx)
            if not slot:
                return
            location = potion_location_lookup.get(self.current_scene, {}).get(slot, None)
            if location:
                if self.location_name_to_id[location] not in ctx.checked_locations:
                    await self._process_checked_locations(ctx, location)

    async def check_ammo_shop(self, ctx):
        if self.save_ammo is None or "ammo" not in ctx.slot_data["shopsanity"]:
            return
        for addr, loc in ammo_shop_lookup.get(self.current_scene, {}).items():
            current_ammo = await addr.read(ctx)
            if current_ammo == 0:
                continue
            if self.location_name_to_id[loc] not in ctx.checked_locations:
                await self._process_checked_locations(ctx, loc)
                return
            self.save_ammo[addr] = current_ammo

    async def update_treasure_tracker(self, ctx: "BizHawkClientContext", last_loc=None):
        read_list = [ITEMS[name].address for name in ITEM_GROUPS["All Treasures"]]
        new_treasure = await read_multiple(ctx, read_list)
        printl(f"Updating Treasure Tracker: {last_loc}")

        if last_loc == "no_loc":
            self.treasure_tracker = new_treasure
            self.got_item_no_loc = True
            return
        elif not (last_loc == "post_receive" and self.got_item_no_loc):
            self.treasure_tracker = new_treasure
            printl(f"No special treasure")
            return

        self.got_item_no_loc = False
        diff = {t: n - o for n, o, t in
                zip(new_treasure.values(), self.treasure_tracker.values(), ITEM_GROUPS["All Treasures"]) if n - o > 0}
        if not diff:
            await self.check_potion_location(ctx)
            return

        single_item = [t for t in diff][0]
        printl(f"Updated Treasure Tracker: {diff}")

        async def remove_treasure():
            reads = await read_multiple(ctx, [ITEMS[i].address for i in diff])
            await write_multiple(ctx, [a for a in reads], [v-1 for v in reads.values()])

        # Detect shop locations
        if "treasure" in ctx.slot_data["shopsanity"] and self.current_scene in SHOP_TREASURE_DATA:
            for data in SHOP_TREASURE_DATA[self.current_scene]:
                if single_item in ITEM_GROUPS[data["group"] + " Treasures"]:
                    for location in data["locations"]:
                        if self.location_name_to_id[location] not in ctx.checked_locations:
                            await remove_treasure()
                            await self._process_checked_locations(ctx, location)
                            await self.set_shop_models(ctx, False)
                            return

        # Do stuff with excess treasure
        if self.delay_reset:
            await remove_treasure()
            self.delay_reset = 0
            return
        if ctx.slot_data["excess_random_treasure"] in [0, 2]:
            printl(f"Removing {diff} from treasures")
            await remove_treasure()
            # self.last_vanilla_item.extend([t for t in diff])
        if ctx.slot_data["excess_random_treasure"] == 2:
            rupees = sum([TREASURE_PRICES[treasure]*count for treasure, count in diff.items()])
            printl(f"Getting {rupees} rupees")
            await STAddr.rupees.add(ctx, rupees)


        self.treasure_tracker = new_treasure

    async def check_item_disconnects(self, ctx, item_name):
        entrances: set = set()
        if item_name in self.item_reconnect_lookup:
            entrances.update(self.item_reconnect_lookup[item_name])
        if item_name in self.item_and_reconnect_lookup:
            for group, data in self.item_and_reconnect_lookup[item_name].items():
                if self.has_from_group(ctx, group):
                    entrances.update(data)
        reverse_entrances = {ctx.slot_data["er_pairings"][str(e)] for e in entrances if str(e) in ctx.slot_data["er_pairings"]}
        self.redisconnected_entrances |= set(get_stored_data(ctx, redisconnected_entrances_key, set()))
        new_entrances = reverse_entrances - (self.redisconnected_entrances | self.traversed_entrances)
        print(f"Redisconnect? {reverse_entrances} new: {new_entrances}")
        if new_entrances:
            await self.store_data(ctx, storage_key(ctx, redisconnected_entrances_key), new_entrances)

    async def drink_potion(self, ctx, read_results):
        drinking_potion = read_results.get(self.addr_drinking_potion, 0)
        if drinking_potion == 0x3b:
            self.drinking_potion = True
        if self.drinking_potion and drinking_potion == 0x39:
            self.drinking_potion = False
            await self.update_potion_tracker(ctx, "drunk_potion")

    async def get_item_read(self, ctx, item_name) -> int:
        if item_name == "Red Potion":
            return await STAddr.all_potions.read(ctx)

        return await super().get_item_read(ctx, item_name)

    async def update_stamps(self, ctx: "BizHawkClientContext"):
        # Set all stamp coords to 0x484848b8 repeating with starting flags
        # Fill stamp book as we go
        stamp_ids = await STAddr.stamp_ids.read(ctx)
        stamps = [(stamp_ids & (0xFF << 8*i)) >> 8*i for i in range(20)]
        has_stamps = [s for s in stamps if s != 255]
        stamp_count = len(has_stamps)

        def remove_wrong_stamps(indexes):
            for i in indexes:
                stamps[i] = 0xFF

        def add_missing_stamps(values):
            for v in values:
                stamps[stamps.index(255)] = v

        wrong_stamp_indexes = []
        missing_stamps = []

        if ctx.slot_data["randomize_stamps"] == 1:  # vanilla_with_location
            stamp_locations_received = [LOCATIONS_DATA[self.location_id_to_name[i]]["stamp"] for i in ctx.checked_locations if self.location_id_to_name[i] in LOCATION_GROUPS["Stamp Stands"]]
            wrong_stamp_indexes = [stamps.index(i) for i in has_stamps if i not in stamp_locations_received]
            missing_stamps = [i for i in stamp_locations_received if i not in has_stamps]

        elif ctx.slot_data["randomize_stamps"] in [2, 3]: # stamp items
            stamp_items_received = [self.item_id_to_name[i.item] for i in ctx.items_received if self.item_id_to_name[i.item] in ITEM_GROUPS["Stamps"]]
            stamp_values_received = [self.item_data[i].value for i in stamp_items_received]
            stamp_pack_count = sum([self.item_data[self.item_id_to_name[i.item]].value for i in ctx.items_received if self.item_id_to_name[i.item] in ITEM_GROUPS["Stamp Packs"]])
            stamp_pack_count = min(stamp_pack_count, len(ctx.slot_data.get("stamp_pack_order", [])))
            stamp_values_received += ctx.slot_data.get("stamp_pack_order",[])[:stamp_pack_count]

            wrong_stamp_indexes = [stamps.index(i) for i in has_stamps if i not in stamp_values_received]
            missing_stamps = [i for i in stamp_values_received if i not in has_stamps]


        elif ctx.slot_data["randomize_stamps"] == 4:
            stamp_locations_received = [LOCATIONS_DATA[i]["stamp"] for i in LOCATION_GROUPS["Stamp Stands"] if self.entrances[LOCATIONS_DATA[i]["ut_connect"]].id in self.traversed_entrances]
            print(f"traversed: {self.traversed_entrances}, stamps: {stamp_locations_received}")
            wrong_stamp_indexes = [stamps.index(i) for i in has_stamps if i not in stamp_locations_received]
            missing_stamps = [i for i in stamp_locations_received if i not in has_stamps]

        remove_wrong_stamps(wrong_stamp_indexes)
        add_missing_stamps(missing_stamps)
        await STAddr.stamp_ids.overwrite(ctx, stamps)
        has_stamps = [s for s in stamps if s != 255]
        stamp_count = len(has_stamps)

        printl(f"Has {stamp_count} stamps: {stamps}")

    async def set_tears(self, ctx):
        set_tears = (self.item_count(ctx, "Tear of Light (All Sections)")
                     or self.item_count(ctx, "Big Tear of Light (All Sections)") * 3)
        if not set_tears:
            section = TOS_FLOOR_TO_SECTION_SAFE.get(self.current_room, 0)
            if section == 0:  # These rooms remove tears
                return
            if section and ctx.slot_data["shuffle_tos_sections"] and ctx.slot_data.get("tear_sections", 2) == 2:
                printl(f"Section {section} is order {ctx.slot_data['tower_section_lookup']}!")
                section = ctx.slot_data["tower_section_lookup"][str(section)]

            if section == 6 or section == 0:
                return
            big_prog_sub = section - 1
            set_tears = (self.item_count(ctx, f"Tear of Light (ToS {section})")
                         or self.item_count(ctx, f"Big Tear of Light (ToS {section})") * 3
                         or max(0, (self.item_count(ctx, "Big Tear of Light (Progressive)") - big_prog_sub) * 3)
                         or max(0, self.item_count(ctx, "Tear of Light (Progressive)") - big_prog_sub * 3)
                         )
            set_tears = min(set_tears, 3)
            printl(f"Setting tears for section {section} tears {set_tears}")
        else:
            printl(f"Setting tears {set_tears}")

        await STAddr.tears_of_light.overwrite(ctx, set_tears)

    async def detect_ut_event(self, ctx, scene):
        """
        Send UT event locations on certain flags being set in certain scenes.
        """
        if scene in UT_EVENT_DATA and not self.sent_event:
            if not self.event_reads:
                data = UT_EVENT_DATA[scene]
                data = [data] if isinstance(data, dict) else data
                printl(f"Event Data {data}")
                self.event_data = data
                await self.get_stage_flags(ctx)
                for i, event in enumerate(data):
                    address = Address.from_pointer(self.stage_flag_address + event.get("offset", 0), size=event.get("size", 1)) if event["address"] == "stage_flags" else event["address"]
                    self.event_reads.append(address)
                print(f"Event reads: {hex_f(self.event_reads)}")

            read_results = await read_multiple(ctx, self.event_reads)
            for event in self.event_data:
                if event["address"] == "stage_flags":

                    res = read_results[Address.from_pointer(self.stage_flag_address + event.get("offset", 0))]
                else:
                    res = read_results[event["address"]]
                if (not event.get("exact_read", False) and event["value"] & res) or event["value"] == res:
                    if "entrance" in event:
                        printl(f"Event detection Success!, {event['entrance']} {hex_f(res)}")
                        entrance = self.entrances[event["entrance"]]
                        await self.store_visited_entrances(ctx, entrance, entrance.vanilla_reciprocal)

                    # self.event_reads.remove(event["address"])
                    self.event_data.remove(event)
            if not self.event_data:
                printl(f"All events sent!")
                self.sent_event = True

        else:
            self.sent_event = True

    async def set_starting_train(self, ctx):
        res = []
        train = ctx.slot_data["starting_train"]
        if train == -1:  # all parts
            res += STAddr.train_parts.get_write_list(0xFFFFFFFF)
            if self.saved_train_parts:
                res += [a.get_inner_write_list(p) for a, p in zip(STAddr.train_part_array, self.saved_train_parts)]
            else:
                res += [a.get_inner_write_list(0) for a in STAddr.train_part_array]
        else:
            res += STAddr.train_parts.get_write_list(0xF << (train*4))
            res += [a.get_inner_write_list(train) for a in STAddr.train_part_array]
        printl(f"Setting starting train {res}")
        await bizhawk.write(ctx.bizhawk_ctx, res)

    async def reset_train_model(self, ctx):
        await STAddr.set_starting_train.unset_bits(ctx, 4)
        self.set_train_in_overworld = 2

    async def save_custom_train(self, ctx):
        train_parts = await read_multiple(ctx, STAddr.train_part_array)
        self.saved_train_parts = [p if p < 0xff else 0 for p in train_parts.values()]
        print(f"Saving custom train {self.saved_train_parts}")

    # Model Stuff

    async def anticipate_location(self, ctx: "BizHawkClientContext", read_result: dict):
        if read_result[STAddr.stage] < 0x13 or self.getting_location:
            return
        # printl(f"Locations in scene: {[l for l in self.locations_in_scene]}")
        coords = await self.get_coords(ctx)
        valid_locations = []
        priority = 30
        for loc_name, loc in self.locations_in_scene.items():
            if (loc.get("x_max", 0x8FFFFFFF) > coords["x"] > loc.get("x_min", -0x8FFFFFFF) and
                    loc.get("z_max", 0x8FFFFFFF) > coords["z"] > loc.get("z_min", -0x8FFFFFFF) and
                    loc.get("y", coords["y"]) + 1000 > coords["y"] >= loc.get("y", coords["y"])):

                if 'no_model' in loc or 'stamp' in loc:
                    continue

                # Check priority
                if priority is None or "priority" not in loc:
                    priority = None
                    valid_locations.append(loc_name)
                elif priority > loc['priority']:
                    priority = loc['priority']
                    valid_locations = [loc_name]
                elif priority == loc['priority']:
                    valid_locations.append(loc_name)

        if self.last_anticipated_locations == valid_locations:
            return
        if not valid_locations:
            printl(f"\tno location")
        else:
            await self.swap_models(ctx, valid_locations)
        self.last_anticipated_locations = valid_locations

    @staticmethod
    async def reset_treasure_models(ctx: "BizHawkClientContext", model=None):
        """
        Set all treasure models to *model*. if model is None, sets them to their vanilla model
        """
        write_list = []
        for i in range(66, 85):
            treasure_model = OFFSET_TO_MODEL[i]

            bits = split_bits(treasure_model.value, 4) if model is None else split_bits(model, 4)
            bits.reverse()
            write_list.append((STAddr.item_model_table.addr + 4*i, bits, "Main RAM"))
        printl(f"Reseting treasure models")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def swap_models(self, ctx, locations: list, treasure_mode=False):
        printl(f"\tMultiple locations: {locations}")
        generic_model = [
            ITEM_MODEL_LOOKUP["Force Gem 17"].value,
            ITEM_MODEL_LOOKUP["Letter"].value,
            ITEM_MODEL_LOOKUP["Gold Rupee"].value,
        ][ctx.slot_data.get("multiworld_item_default_models", 0)]
        item_location_check = {}  # dict of item to location id for what location determines the model
        item_priority = {}
        for loc_name in locations:
            loc_data = LOCATIONS_DATA[loc_name]
            vanilla_item = loc_data.get("vanilla_item", []) or loc_data.get("hidden_vanilla_item", [])
            vanilla_items = [vanilla_item] if isinstance(vanilla_item, str) else vanilla_item
            priority = loc_data.get("priority", 0)

            if loc_data.get("farmable", "") in ["remove", "conditional"] and loc_data["id"] in ctx.checked_locations:
                continue

            for item in vanilla_items:
                if not priority:
                    # set location_id to None if there's a location conflict
                    item_location_check[item] = None if item in item_location_check else loc_data['id']
                    continue

                # Sort locations by priority if applicable
                if item in item_priority and priority >= item_priority[item]:
                    continue

                if hasattr(self.item_data[item], "progressive_model"):
                    for prog_item in self.item_data[item].progressive_model:
                        item_location_check[prog_item] = loc_data['id']

                item_location_check[item] = loc_data['id']
                item_priority[item] = priority

        printl(f"Items with locations: {[(i, l) for i, l in item_location_check.items()]}")

        model_data = ctx.slot_data.get("model_lookup", {})
        write_list = []
        printl_list = {}
        # look up locations
        for i, l in item_location_check.items():
            if i not in self.item_data: continue
            item_data = self.item_data[i]
            item_model = item_data.vanilla_model

            # Handle progressive items that change their models
            if hasattr(item_data, "progressive_model"):
                if self.current_scene in potion_location_lookup:
                    item_model = item_data.progressive_model[1]
                else:
                    count = min(self.item_count(ctx, i), len(item_data.progressive_model)-1)
                    item_model = item_data.progressive_model[count]

            if item_model is None: continue
            vanilla_model = ITEM_MODEL_LOOKUP[item_model]

            # Choose model for location
            if l is None:  # conflict
                model_value = generic_model
                model_name = "Generic"
            elif l in ctx.missing_locations | ctx.checked_locations:  # randomized
                model_value = OFFSET_TO_MODEL[model_data[str(l)]].value if str(l) in model_data else generic_model
                model_name = OFFSET_TO_MODEL[model_data[str(l)]].name if model_value != generic_model else "Force Gem"
            else:  # vanilla
                    printl(f"Vanilla item {i}, {l}")
                    model_name = ITEMS[i].model
                    model_value = ITEM_MODEL_LOOKUP[model_name].value if model_name else generic_model


            # add models to write list
            bits = split_bits(model_value, 4)
            bits.reverse()
            write_list.append((STAddr.item_model_table.addr + 4 * vanilla_model.offset, bits, "Main RAM"))
            if l is not None:
                printl_list[self.location_id_to_name[l]] = model_name

        printl(f"Swapped Models: {printl_list}")
        if write_list:
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def unset_special_vanilla_items(self, ctx, location, item):
        # las chest is the only conditional for now, if las is shuffled make it give nothing
        if location.get("farmable", "") == "conditional" and not str(self.entrances["Lost at Sea Dungeon Reward Room South"].id) in ctx.slot_data["er_pairings"]:
            self.last_vanilla_item.pop()

    async def set_shop_models(self, ctx: "BizHawkClientContext", on_load=True):
        """Load shop models in bulk"""
        valid_locations = []
        valid_locations += list(self.location_area_to_watches.get(self.current_scene, {}).keys())
        # valid_locations += list(ammo_shop_lookup.get(self.current_scene, {}).values())
        if not on_load:
            valid_locations += list(potion_location_lookup.get(self.current_scene, {}).values())
            valid_locations += [loc for treasures in SHOP_TREASURE_DATA.get(self.current_scene, []) for loc in treasures.get("locations", [])]
        printl(f"Setting shop models {self.current_scene}: {valid_locations}")
        for loc in valid_locations.copy():
            if self.location_name_to_id[loc] in ctx.checked_locations:
                valid_locations.remove(loc)
                printl(f"Already checked location {loc}!")
        await self.swap_models(ctx, valid_locations)
        if on_load:
            await self.reset_treasure_models(ctx)

    # Misc location handling

    def cancel_location_read(self, location) -> bool:
        if "stamp" in location:
            return True
        if "rabbit" in location:
            return True
        return False

    async def validate_location_processing(self, ctx):
        """Catch locations sent from console, and post process them"""
        self.processed_locations |= set(get_stored_data(ctx, processed_locations_key, set()))
        # print(f"Processed locations: {self.processed_locations} {get_stored_data(ctx, processed_locations_key, set())}")
        diff = set(ctx.checked_locations) - self.processed_locations
        if not self.processed_locations or not diff: return
        for loc_id in diff:
            print(f"Got location from console: {self.location_id_to_name[loc_id]}")
            await self.check_location_post_processing(ctx, self.location_id_to_location[loc_id])

    async def check_location_post_processing(self, ctx, location: dict):
        printl(f"Post processing loc {location}")
        if not location:
            await self.update_treasure_tracker(ctx, "no_loc")
            return

        if "goal" in location:
            from .data.Entrances import goal_event_lookup
            goal = ctx.slot_data.get("goal", -1)
            loc_goal = location["goal"]
            printl(f"Processing goal locations: {goal_event_lookup[goal]} == {loc_goal}")
            if goal_event_lookup[goal] == loc_goal:
                await self.store_event(ctx, loc_goal)
                self.has_goal_location = True

        if "rabbit" in location and "address" in location:
            await self.store_rabbit(ctx, location)

        # Connect event
        if "ut_connect" in location:
            event_name = location["ut_connect"]
            await self.store_event(ctx, event_name)

        if location["name"] in ["Outset Bee Tree", "Outset Clear Rocks"]:
            self.reload_on_item = True

        if "Tear of Light" in location.get("vanilla_item", "") and ctx.slot_data["randomize_tears"] != -1:
            await STAddr.tears_of_light.overwrite(ctx, 1)  # prevent cutscene and underflow

        if location["name"] in ["ToS 1F Chest"] and ctx.slot_data["randomize_tears"] != -1:
            await self.set_tears(ctx)

        if self.current_scene in [0x1309, 0x1318] and isinstance(location.get("vanilla_item", ""), str) and location.get("vanilla_item", "").startswith("Boss Key"):
            printl("Opening ToS boss door after having key and getting boss key location")
            await self.open_boss_door(ctx, self.boss_door_addr, True)

        if self.snurglar_addr and location["name"] in LOCATION_GROUPS["Snurglars"]:
            await self.snurglar_addr.unset_bits(ctx, 0x0F)

        if location["name"] == "Goron Village Get Wagon":
            await self.reset_train_model(ctx)

        if location["name"] == "Capbone Boss Reward" and str(self.entrances["Capbone Exit"].id) in ctx.slot_data["er_pairings"]:
            post_fight = self.entrances["Desert Temple B2 North Post-Fight"]
            entrance = self.entrance_id_to_entrance[ctx.slot_data["er_pairings"][str(self.entrances["Capbone Exit"].id)]]
            self.er_map.setdefault(entrance.scene, {})[entrance] = post_fight

        await self.store_data(ctx, storage_key(ctx, processed_locations_key), {location['id']}, default=set())

    async def process_post_receive(self, ctx):
        if not self.delay_pickup:
            await self.update_treasure_tracker(ctx, "post_receive")  # always update treasure tracker, lots of random treasures on ground!

        if "ammo" in ctx.slot_data["shopsanity"] and self.current_scene in ammo_shop_lookup:
            await STAddr.bomb_count.overwrite(ctx, 0)
            await STAddr.arrow_count.overwrite(ctx, 0)


    # Rabbit handling

    async def update_rabbit_count(self, ctx):
        if self.current_stage in range(4, 8):  # self.on_train triggers rabbit locs early
            self.update_rabbit_tracker(ctx)
            rabbit_bits = self.rabbit_tracker
        else:
            realms = rabbit_realms
            rabbit_counts = [min(sum([ITEMS[i].value*self.item_count(ctx, i) for i in ITEM_GROUPS[f"{realm} Rabbits"]]), 10) for realm in realms]
            rabbit_bits = sum([(2 ** count - 1) << 10*i for i, count in enumerate(rabbit_counts)])
            printl(f"Updating rabbit bits {hex(rabbit_bits)}")
        await STAddr.rabbits.overwrite(ctx, rabbit_bits)

    def get_max_total_rabbit_counts(self, ctx):
        counts = [0]*5
        realm_lookup = {"Grass": 0,
                        "Snow": 1,
                        "Ocean": 2,
                        "Mountain": 3,
                        "Sand": 4
                        }
        for loc_id in ctx.slot_data["active_rabbit_locs"]:
            loc_data = self.location_id_to_location[loc_id]
            count = loc_data.get("count", 0)
            if not count:
                continue
            realm_index = realm_lookup[loc_data["realm"]]
            counts[realm_index] = max(count, counts[realm_index])
        self.max_total_rabbits = counts

    async def store_rabbit(self, ctx, loc_data):
        key = storage_key(ctx, rabbit_storage_key)
        index = loc_data["address"] - STAddr.rabbits
        self.rabbit_tracker[index] |= loc_data["value"]
        self.update_rabbit_tracker(ctx)
        await self.store_data(ctx, key, self.rabbit_tracker, operation="replace")

        # Send total location
        if ctx.slot_data["rabbitsanity"] in [3, 4]:
            rabbit_type = loc_data["vanilla_item"]
            rabbit_type_lookup = ["Grass Rabbit", "Snow Rabbit", "Ocean Rabbit", "Mountain Rabbit", "Sand Rabbit"]
            type_index = rabbit_type_lookup.index(rabbit_type)
            rabbit_count = self.rabbit_counter[type_index]
            if rabbit_count <= 0:
                rabbit_count = 1  # Hope this just works
            plural = "s" if rabbit_count > 1 else ""
            total_loc = f"Catch {rabbit_count} {rabbit_type}{plural}"
            printl(f"Sending rabbit total location {total_loc} {self.rabbit_counter}")
            await self._process_checked_locations(ctx, total_loc)

            # Store total rabbit events
            if rabbit_count >= self.max_total_rabbits[type_index]:
                await self.store_events(ctx, [f"EVENT: {loc}" for loc in LOCATION_GROUPS[f"Unique {rabbit_type}s"]])
            else:
                await self.store_event(ctx, f"EVENT: {loc_data['name']}")

    def update_rabbit_tracker(self, ctx):
        rabbit_storage = ctx.stored_data.get(storage_key(ctx, rabbit_storage_key), None)
        rabbit_storage = [0]*7 if rabbit_storage is None else rabbit_storage
        printl(f"\tRabbit storage: {rabbit_storage}")
        self.rabbit_tracker = [s | c for s, c in zip(rabbit_storage, self.rabbit_tracker)]
        printl(f"\trabbit tracker {self.rabbit_tracker}")
        all_rabbits = sum([r << 8*i for i, r in enumerate(self.rabbit_tracker)])
        printl(f"\tall rabbits: {hex(all_rabbits)}")
        self.rabbit_counter = [count_bits(all_rabbits & (0x3FF << n*10)) for n in range(5)]
        printl(f"Updating Rabbit tracker: {[hex(i) for i in self.rabbit_tracker]} {self.rabbit_counter}")

    # Important Processes

    async def process_game_completion(self, ctx: "BizHawkClientContext"):
        if self.has_goal_location:
            return True
        return False

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead, stage, read_result):
        if (read_result[STAddr.menu]
            or self.current_scene in [0x3802, 0x3b00, 0x3b01, 0x3b02, 0x3b03] # healthless minigames
            or self.getting_location):
            return
        dead_health = 0
        if stage < 0x13:  # deaths work badly on train
            dead_health = 1

        if ctx.last_death_link > self.last_deathlink and not is_dead:
            # A death was received from another player, make our player die as well

            await self.health_address.overwrite(ctx, dead_health)

            self.is_expecting_received_death = True
            self.last_deathlink = ctx.last_death_link

        if not self.was_alive_last_frame and not is_dead:
            # We revived from any kind of death
            self.was_alive_last_frame = True
        elif self.was_alive_last_frame and is_dead:
            # Our player just died...
            self.was_alive_last_frame = False
            if self.is_expecting_received_death:
                # ...because of a received deathlink, so let's not make a circular chain of deaths please
                self.is_expecting_received_death = False
            else:
                # ...because of their own incompetence, so let's make their mates pay for that
                message = " crashed their train." if stage < 0x13 else " has disappointed the Train Spirits."
                await ctx.send_death(ctx.player_names[ctx.slot] + message)
                self.last_deathlink = ctx.last_death_link

    # Stage Flags

    async def get_stage_flags(self, ctx):
        stage_address = await STAddr.stage_flag_pointer.read(ctx)
        self.stage_flag_address = Address.from_pointer(stage_address + STAGE_FLAGS_OFFSET - 0x2000000, size=4)
        print(f"Got stage flag address: {hex_f(self.stage_flag_address)}")
        return self.stage_flag_address

    async def set_stage_flags(self, ctx, stage):
        self.reload_stage_flags = False
        if stage in self.stage_flags:
            stage_flag_address = await self.get_stage_flags(ctx)

            printl(f"Setting stage flags for stage {hex(stage)} at {stage_flag_address}: {hex_f(self.stage_flags[stage])}")
            await stage_flag_address.set_bits(ctx, self.stage_flags[stage])
        if self.set_train_in_overworld and stage <= 0xA:
            await self.set_starting_train(ctx)
            self.set_train_in_overworld -= 1

    def update_stage_flag(self, stage: int, new: list[int]):
        self.stage_flags[stage] = [o | n for o, n in itertools.zip_longest(STAGE_FLAGS.get(stage, [0,0,0,0]), new, fillvalue=0)]
        print(f"Updating Stage Flags: {hex_f(stage)} {hex_f(new)} : {hex_f(self.stage_flags[stage])}")
        self.reload_stage_flags = True


    # Snurglars

    async def set_up_snurglar_data(self, ctx):
        snurglar_pointer = await STAddr.snurglar_pointer.read(ctx)

        snurglar_flags = Address.from_pointer(snurglar_pointer + 0xC0)

        printl(f"Tried snurglar flags @ {snurglar_flags}")
        if not (0x400000 > snurglar_flags > 0):
            return
        self.snurglar_addr = snurglar_flags
        for color in ["Gold", "Purple", "Orange"]:
            self.watches[f"Snurglars {color} Key"] = snurglar_flags

        if self.item_count(ctx, "Mountain Temple Snurglar Key") >= 3 or self.item_count(ctx, "Snurglar Keyring"):
            if (not any([self.item_count(ctx, i) for i in ITEM_GROUPS["Tracks: Mountain Temple Tracks"]])
                    or not self.item_count(ctx, "Cannon")
                    or all([LOCATIONS_DATA[i]['id'] in ctx.checked_locations for i in LOCATION_GROUPS["Snurglars"]])):
                printl(f"Got Snurglar keys, opening mountain temple")
                await self.snurglar_addr.overwrite(ctx, 0x30)
            else:
                printl(f"Got Snurglar keys, adding to main read list")
                self.main_read_list.append(snurglar_flags)

    async def reset_snurglar_door(self, ctx):
        if self.last_scene == 0x700:
            snurglar_ids = [self.location_name_to_id[f"Snurglars {color} Key"] for color in ["Purple", "Orange", "Gold"]]
            for i in snurglar_ids:
                if i not in ctx.checked_locations:
                    await self.snurglar_addr.unset_bits(ctx, 0x30)
                    break

    # Keys and doors

    async def save_tos_keycount(self, ctx):
        """ToS keycount is not dependent on stage, so save current count on room change or save"""
        printl(f"Saving Keycount {self.last_stage} {self.last_scene}")
        if self.last_stage != 0x13 or self.last_scene is None:
            return

        current_keys = await self.key_address.read(ctx)
        current_section = TOS_FLOOR_TO_SECTION[self.last_scene & 0xFF]  # triggers after scene change
        section_key = 0x130 + current_section
        if section_key in DUNGEON_KEY_DATA:
            key_data = await STAddr.key_storage_tos.read(ctx)
            blank_data = key_data & (0xFF - DUNGEON_KEY_DATA[section_key]["filter"])
            new_data = blank_data + DUNGEON_KEY_DATA[section_key]["value"]*current_keys
            if new_data != key_data:
                printl(f"Saving ToS key count: {hex(new_data)}")
                await STAddr.key_storage_tos.overwrite(ctx, new_data)

    async def enter_special_key_room(self, ctx, stage, scene_id):
        if stage == 0x13:
            section = TOS_FLOOR_TO_SECTION[self.current_room]
            key_code = 0x130 + section
            printl(f"Special Keycode: {key_code} {DUNGEON_KEY_DATA.get(key_code)}")
            if key_code in DUNGEON_KEY_DATA:
                key_data = DUNGEON_KEY_DATA[key_code]
                key_storage = await STAddr.key_storage_tos.read(ctx)
                current_keys = (key_storage & key_data["filter"]) // key_data["value"]
                printl(f"Current Keys = {current_keys} | {(key_storage & key_data['filter'])} / {key_data['value']}")
                await self.key_address.overwrite(ctx, current_keys)
            else:
                await self.key_address.overwrite(ctx, 0)
            return True
        if STAGES[stage] in ctx.slot_data["non_required_dungeons"] and ctx.slot_data["exclude_dungeons"] == 2:
            key_data = DUNGEON_KEY_DATA[stage]
            await self.key_address.overwrite(ctx, key_data["filter"]//key_data["value"])
            return True
        return False

    async def open_boss_door(self, ctx, door_obj, tos_loc=False):
        current_scene = self.current_scene
        if current_scene not in BOSS_KEY_DATA:
            return
        data = BOSS_KEY_DATA[self.current_scene]
        if (ctx.slot_data.get("randomize_boss_keys", 0)
            or (ctx.slot_data["exclude_dungeons"] == 2 and data["dungeon"] in ctx.slot_data["non_required_dungeons"])
            or (ctx.slot_data["exclude_sections"] == 2 and data.get("section", 0) in ctx.slot_data["non_required_sections"])
        ):

            has_key = (
                    self.item_count(ctx, f"Boss Key ({data['dungeon']})")
                    or (self.item_count(ctx, f"Keyring ({data['dungeon']})") and ctx.slot_data["big_keyrings"]))

            printl(f"Checking boss door: {has_key}")
            # Check has boss key
            if (
                (  # Normal Dungeons
                    current_scene & 0xff00 != 0x1300 and (
                        has_key or (ctx.slot_data["exclude_dungeons"] == 2 and data["dungeon"] in ctx.slot_data["non_required_dungeons"])
                    )
                ) or (  # ToS
                    current_scene & 0xff00 == 0x1300 and (
                        (  # ToS excluded
                            ctx.slot_data["exclude_sections"] == 2 and data.get("section", 0) in ctx.slot_data["non_required_sections"]
                        ) or ( # Tos with key needs key location to open door
                            has_key and (
                                tos_loc or
                                (current_scene == 0x1309 and self.location_name_to_id["ToS 10F Boss Key"] in ctx.checked_locations)
                                or (current_scene == 0x1318 and self.location_name_to_id["ToS 22F Boss Key"] in ctx.checked_locations)
                            )
                        )
                    )
                )
            ):
                # Open boss door
                printl(f"Opening boss door for {hex(current_scene)}")
                door_opener = Address.from_pointer(door_obj + 5 * 4 + 2)
                if await door_opener.read(ctx) != 0x5:
                    await door_opener.overwrite(ctx, 3)

    async def load_boss_key_watch(self, ctx):
        if self.current_scene in BOSS_KEY_DATA and ctx.slot_data.get("randomize_boss_keys", 0):
            actor_table = await self.get_actor_table(ctx)
            data = BOSS_KEY_DATA[self.current_scene]
            if self.location_name_to_id[data["location"]] in ctx.checked_locations:
                printl(f"Has found location {data['location']}, deleting boss key")
                await self.delete_boss_key(ctx)
            else:
                if "search_data" in data:
                    pointer, offset = await self.find_table_object(ctx, *data["search_data"], actor_table, return_index=True, reverse=False)
                    self.oct_bk_offset = offset
                    printl(f"Found bk in actor loop: {pointer} {offset}")
                else:
                    pointer = await actor_table.read(ctx)

                if pointer and pointer < 0x400000:
                    printl(f"Found Boss Key object: {hex_f(pointer)}")
                    offset = 12 if self.current_stage == 0x1c else 8
                    self.boss_key_read = Address.from_pointer(pointer + offset, size=4)
                    self.boss_key_y = data["y"]
                    printl(f"BK Read: {self.boss_key_read}")
                printl(f"Loaded boss key data: {pointer} y: {self.boss_key_y}")

    async def get_tos_bk_pointer(self, ctx) -> tuple[Address, int]:
        actor_table = await self.get_actor_table(ctx)
        offset = 0  # start of table + tos bk index
        pointer_addr = Address.from_pointer(actor_table + offset, size=3)
        pointer = await pointer_addr.read(ctx)
        printl(f"BK pointer from table read: {pointer_addr} -> {hex(pointer)} actor table: {actor_table}")
        return pointer_addr, pointer

    async def detect_boss_key(self, ctx):
        """Called each cycle while in a boss key room to detect a change in boss key position"""
        if self.boss_key_y is not None:
            bk_read = await self.boss_key_read.read(ctx, signed=True, silent=True)
            if (bk_read > self.boss_key_y + 10 and self.current_stage != 0x1c) or (self.current_stage == 0x1c and bk_read < self.boss_key_y):
                loc = BOSS_KEY_DATA[self.current_scene]["location"]
                await self._process_checked_locations(ctx, loc)
                printl(f"Found boss key location {loc} {bk_read} > {self.boss_key_y + 10} {hex(self.current_stage)}")
                await self.delete_boss_key(ctx)
                self.boss_key_y, self.boss_key_read = None, None

    async def delete_boss_key(self, ctx):
        pointer = await STAddr.boss_key_deletion_pointer.read(ctx)
        printl(f"Deleting boss key @ {hex(pointer)}")
        bk_data =  BOSS_KEY_DATA[self.current_scene]
        size, offset = bk_data.get("deletion_data", (12, 0))
        actor_table = await self.get_actor_table(ctx)
        if "search_data" in bk_data:
            print(f"Starting deletion: {self.oct_bk_offset}")
            if not self.oct_bk_offset:
                _, self.oct_bk_offset = await self.find_table_object(ctx, *bk_data["search_data"][:4], actor_table,
                                                              return_index=True, reverse=False)
                if not self.oct_bk_offset: return
            pointer = actor_table  # Ocean temple bk does not load into the first slot in memory
            offset, size = self.oct_bk_offset*4, 4
            print(f"Got offset from search: {offset} {hex_f(pointer+offset)} {self.oct_bk_offset}")
            self.oct_bk_offset = None
        if self.current_stage == 0x13:
            pointer, _ = await self.get_tos_bk_pointer(ctx)
        deletion_address = Address.from_pointer(pointer+offset, size)
        printl(f"Deleting boss key @ {deletion_address} size {size}")
        # printl(f"Deleting boss key @ {STAddr.boss_key_deletion}")
        await deletion_address.overwrite(ctx, 0)

    # Train stuff

    async def set_train_speed(self, ctx):
        await write_multiple(ctx, train_speed_addresses, self.train_speed)
        self.last_train_gear = -1  # force a quick speed increase
        self.train_speed_pointer = await STAddr.train_speed_pointer.read(ctx)
        try:
            self.train_speed_addr = Address.from_pointer(self.train_speed_pointer + TRAIN_SPEED_OFFSET, size=4)
            self.train_gear_addr = Address.from_pointer(self.train_speed_pointer + TRAIN_GEAR_OFFSET)
            print(f"Setting gear addr {hex_f(self.train_gear_addr)}")
            if self.train_gear_addr not in self.main_read_list:
                self.main_read_list.append(self.train_gear_addr)
        except AssertionError:
            logger.warning(f"Tried to load train speed while not on train")
            return

    async def process_train_speed(self, ctx, read_result):
        if self.current_stage not in range(4, 0xb):
            return
        if not hasattr(self, "train_speed_addr") or not hasattr(self, "train_gear_addr"):
            await self.set_train_speed(ctx)
        if not getattr(self, "train_gear_addr", False):
            logger.info(f"Oops the client does not know where you are. Warping to start is the safest fix.")
            await STAddr.stage.overwrite(ctx, 0x13)
            return

        instant_switch = False
        if self.update_train_speed:
            await write_multiple(ctx, train_speed_addresses, self.train_speed)
            self.update_train_speed = False
            instant_switch = True

        current_gear = read_result.get(self.train_gear_addr, 0)
        if current_gear != self.last_train_gear or instant_switch:
            self.last_train_gear = current_gear

            if self.train_quick_station and current_gear == 1:
                train_action_addr = Address.from_pointer(self.train_speed_pointer+TRAIN_QUICK_STATION_OFFSET)
                await train_action_addr.overwrite(ctx, 0x5c, silent=True)  # instant-enter station
            # Instant-set train speed
            if self.train_snap_speed and current_gear != 1:
                await self.train_speed_addr.overwrite(ctx, self.train_speed[current_gear]*0x10, silent=True)

    async def setup_evil_train_deletion(self, ctx, operation: str, comp: int):
        if self.current_stage == 4 and not self.has_from_group(ctx, "Tracks: Forest Glyph"):
            printl(f"Started normal train deletion")
            actor_table = await self.get_actor_table(ctx)
            self.precision_mode = [Address.from_pointer(actor_table + 17 * 4 + 3), comp, operation, actor_table]
        if self.current_stage == 5 and not self.has_from_group(ctx, "Tracks: Blizzard Temple Tracks"):
            printl(f"Started normal train deletion")
            actor_table = await self.get_actor_table(ctx)
            self.precision_mode = [Address.from_pointer(actor_table + 16 * 4 + 3), comp,
                                   operation, actor_table]

    async def delete_bad_ow_actors(self, ctx, table_start):
        actor_idents = await self.get_table_data(ctx, table_start, 12)
        crash_causers_0 = {
            0x1387b4: "Tanks",
            0x148d88: "Evil Train",
            0x137e64: "?",
            0x137b70: "?",
            0x138580: "Tank spawner",
            0x13784c: "Demon Train",
            0x138b10: "Purple Train"
        }

        crash_causers = {
            0x21405e8: "Demon Train",
        }
        actor_idents_0 = await self.get_table_data(ctx, table_start, 0, size=3)
        # old_crash_list = [Address.from_pointer(k.addr, size=4) for k, i in actor_idents.items() if i in crash_causers]
        # print(f"old crash list: {hex_f(old_crash_list)}")
        crash_list = [Address.from_pointer(k.addr, size=4) for k, i in actor_idents_0.items() if i in crash_causers_0]
        # crash_list += old_crash_list

        if crash_list:
            await self.frame_advance(ctx)
            await write_multiple(ctx, crash_list, [0]*len(crash_list))
            actor_print = {k: crash_causers_0[i] for k, i in actor_idents_0.items() if i in crash_causers_0}
            printl(f"Deleting bad actors: {hex_f(actor_print)}")

    # ER stuff

    def update_boss_warp(self, ctx, stage, scene_id):
        if scene_id in BOSS_WARP_SCENE_LOOKUP:  # Boss rooms
            reverse_exit = BOSS_WARP_SCENE_LOOKUP[scene_id]
            reverse_exit_id = self.entrances[reverse_exit].id
            pair = ctx.slot_data["er_pairings"].get(f"{reverse_exit_id}", self.entrances[reverse_exit].vanilla_reciprocal.id)
            if pair is None:
                printl(f"Boss Entrance not Randomized")
                self.boss_warp_entrance = reverse_exit
            self.boss_warp_entrance = self.entrance_id_to_entrance[pair]
            printl(f"Warp Stage: {stage}, current warp {self.boss_warp_entrance}")
            return self.boss_warp_entrance

        return None

    async def conditional_bounce(self, ctx, scene: int, entrance: int) -> "STTransition" or None:
        e_tuple = ((scene & 0xFF00) >> 8, scene & 0xFF, entrance)
        current_destination = entrance_tuple_to_entrance.get(e_tuple)
        if current_destination and not await self.conditional_er(ctx, current_destination, detect_data=current_destination.vanilla_reciprocal):
            return current_destination.vanilla_reciprocal
        return None

    async def conditional_er(self, ctx, exit_data, silent=False, detect_data=None) -> bool:
        if self._just_entered_game:
            return True

        def check_or(group):
            for or_group in group:
                if self.has_from_group(ctx, or_group):
                    return True
            return False

        # Check for required items from item groups
        for and_group in exit_data.required_groups:
            if isinstance(and_group, tuple):
                if not check_or(and_group):
                    if not silent:
                        logger.info(f"Missing Tracks: {' OR '.join([i.split('Tracks: ')[1] for i in and_group])}")
                    return False
            elif not self.has_from_group(ctx, and_group):
                if not silent:
                    logger.info(f"Missing Tracks: {' AND '.join([i.split('Tracks: ')[1] for i in exit_data.required_groups])}")
                return False

        # Check for cannon with cannon logic
        if (not ctx.slot_data["cannon_logic"]
                and (exit_data.category_group in [EntranceGroups.TRAIN_PORTAL, EntranceGroups.OVERWORLD_TRAIN]
                     or (exit_data.category_group == EntranceGroups.STATION
                         and exit_data.direction == EntranceGroups.UP))):
            if not self.item_count(ctx, "Cannon"):
                if not silent:
                    logger.info(f"You need the Cannon to board the train.")
                return False

        # Check tos tower conditions
        if "tower" in exit_data.extra_data:
            section = exit_data.extra_data["tower"]

            # Base Item
            if ctx.slot_data["tos_unlock_base_item"]:
                if ctx.slot_data["tos_section_unlocks"] != 2:
                    if not self.item_count(ctx, "Tower of Spirits Base"):
                        if not silent:
                            logger.info(f"Missing ToS tower item: Tower of Spirits Base.")
                        return False
                else:
                    section += 1

            # Sources
            if ctx.slot_data["tos_section_unlocks"] == 1:
                glyph_section = {
                    2: "Forest Source",
                    3: "Snow Source",
                    4: "Ocean Source",
                    5: "Fire Source"}
                current_source = glyph_section.get(section, "")
                if current_source and not self.has_from_group(ctx, f"Tracks: {current_source}"):
                    if not silent:
                        logger.info(f"Missing Tracks: {current_source}")
                    return False
            elif ctx.slot_data["tos_section_unlocks"] == 2:  # Progressive
                progressive_items = self.item_count(ctx, "Progressive ToS Section")
                if progressive_items < (section-1):
                    if not silent:
                        logger.info(f"Missing ToS tower items: Progressive ToS Section ({progressive_items}/{section-1})")
                    return False


        if detect_data:
            await self.update_safe_respawn(ctx, exit_data, detect_data)
        return True

    def add_special_er_data(self, ctx, er_map, scene, detect_data: "STTransition", exit_data: "STTransition"):
        #print(f"Checking ER map {detect_data.name} => {exit_data.name}")

        # Outset tutorial
        if detect_data.name == "Outset Board Train":
            outset_exit = self.entrances["Outset to Tutorial"]
            er_map.setdefault(0x2f00, {})[outset_exit] = exit_data
            printl(f"special ER: {outset_exit} => {exit_data}")

        # GTR has 2 exits
        if detect_data.exit == (0x7, 0, 4):
            gtr_exit = self.entrances["Goron Target Range Exit"]
            er_map.setdefault(0x3c01, {})[gtr_exit] = exit_data

        # Marine temple shortcut wants to link to underwater
        if exit_data.name == "Marine Temple Lobby Board Train":
            oct_exit = self.entrances["Marine Temple Train Exit Water Warp"]
            er_map.setdefault(0x1b0a, {})[oct_exit] = detect_data

        # Skip desert rocktite cave
        if detect_data.name == "Ocean Realm North Rocktite Cave":
            rocktite_entrance = self.entrances["Ocean Realm North Rocktite Cave Fight"]
            er_map.setdefault(0x600, {})[rocktite_entrance] = exit_data
            print(f"{rocktite_entrance} => {detect_data}")

        # Capbone states
        if exit_data.name == "Capbone Exit":
            post_fight = self.entrances["Skeldritch Post-Fight Exit"]
            er_map.setdefault(post_fight.scene, {})[post_fight] = detect_data
            if self.location_name_to_id["Capbone Boss Reward"] in ctx.checked_locations:
                er_map.setdefault(detect_data.scene, {})[detect_data] = post_fight
            else:
                er_map.setdefault(detect_data.scene, {})[detect_data] = exit_data
        if detect_data.name == "Desert Temple B2 North Entrance":
            desert_exit = self.entrances["Desert Temple B2 North Post-Fight"]
            er_map.setdefault(0x1d04, {})[desert_exit] = exit_data
        # ToS elevator linkup
        if detect_data.name == "Tower of Spirits Staircase Exit":
            elevator = self.entrances["Tower of Spirits Staircase Elevators"]
            er_map.setdefault(0x1700, {})[elevator] = exit_data

        # Fake mountain temple room
        if detect_data.name == "Mountain Temple 2F Central Staircase":
            mtt_alt = self.entrances["Mountain Temple 2F Central Staircase Alt"]
            er_map.setdefault(0x1c01, {})[mtt_alt] = exit_data
        if exit_data.name == "Mountain Temple 2F Central Staircase":
            mtt_alt = self.entrances["Mountain Temple 2F Central Staircase Alt"]
            er_map.setdefault(detect_data.scene, {})[detect_data] = mtt_alt
        if detect_data.name == "Mountain Temple 2F NE Staircase":
            mtt_alt = self.entrances["Mountain Temple 2F NE Staircase Alt"]
            er_map.setdefault(0x1c01, {})[mtt_alt] = exit_data
        if exit_data.name == "Mountain Temple 2F NE Staircase":
            mtt_alt = self.entrances["Mountain Temple 2F NE Staircase Alt"]
            er_map.setdefault(detect_data.scene, {})[detect_data] = mtt_alt

        return er_map

    async def change_entrance_animation(self, ctx):
        if self.block_entrance_animation:
            self.block_entrance_animation = False
            return
        lookup = (self.current_stage, self.current_room, self.current_entrance)
        new_exit = entrance_tuple_to_entrance.get(lookup, None)
        printl(f"New exit for animation change: {new_exit}")
        if not new_exit:
            return
        if new_exit.category_group == EntranceGroups.WARP_PORTAL:
            await STAddr.entrance_animation.overwrite(ctx, 0x19)  # prevent blue warps from isntant-warping you
        elif new_exit.stage == 0xA:
            await STAddr.entrance_animation.overwrite(ctx, 0x30)  # prevent path drawing underwater
        elif (new_exit.category_group == EntranceGroups.STATION and new_exit.direction == EntranceGroups.UP) or new_exit.category_group == EntranceGroups.TRAIN_PORTAL:
            if self.current_scene != self.last_scene:
                await STAddr.entrance_animation.overwrite(ctx, 0x39)
        elif "animation_override" in new_exit.extra_data:
            await STAddr.entrance_animation.overwrite(ctx, new_exit.extra_data["animation_override"])
        elif await STAddr.entrance_animation.read(ctx) in [0x9]:  # change glitchy entrances
            await STAddr.entrance_animation.overwrite(ctx, 0x18)

    # Respawn stuff

    async def ut_bounce_scene(self, ctx, scene):
        scene_data = scene_lookup.get(scene)
        # print(f"Scene data: {scene_data}")
        if not scene_data:
            return
        map_id = scene_data.map_id
        if not ctx.slot_data["shuffle_houses"] and scene_data.room_type == "house":
            printl(f"Not map switching due to house: {hex(scene)}")
            return
        if not ctx.slot_data["shuffle_caves"] and scene_data.room_type == "cave":
            printl(f"Not map switching due to cave: {hex(scene)}")
            return

        if not ctx.slot_data["shuffle_train_transitions"] and map_id <= 4:
            map_id = 0

        if not ctx.slot_data["shuffle_disorientation"] and scene_data.room_type == "disorientation":
            map_id = 209
        if not ctx.slot_data["shuffle_eote"] and scene_data.room_type == "eote":
            map_id = 31

        printl(f"Storing new scene for UT {hex(scene)}")
        await ctx.send_msgs([{
            "cmd": "Set",
            "key": f"{ctx.slot}_{ctx.team}_UT_MAP",
            "default": 0,
            "operations": [{"operation": "replace", "value": map_id}]
        }])

    async def store_visited_entrances(self, ctx: "BizHawkClientContext", detect_data: "STTransition", exit_data: "STTransition",
                                      interaction: str="traverse"):
        self.checked_entrances |= set(get_stored_data(ctx, checked_entrances_key, set()))
        self.traversed_entrances |= set(get_stored_data(ctx, traversed_entrances_key, set()))

        if detect_data.name == "Marine Temple Train Exit Water Warp":
            detect_data = self.entrances["Marine Temple Lobby Board Train"]
        elif detect_data.name == "Lost at Sea Lobby Enter Dungeon One-Way":
            detect_data = self.entrances["Lost at Sea Lobby Enter Dungeon"]
        elif detect_data.name == "Ocean Realm North Rocktite Cave Fight":
            detect_data = self.entrances["Ocean Realm North Rocktite Cave"]
        elif detect_data.name == "Desert Temple B2 North Post-Fight":
            detect_data = self.entrances["Desert Temple B2 North Entrance"]
        elif detect_data.name == "Mountain Temple 2F NE Staircase Alt":
            detect_data = self.entrances["Mountain Temple 2F NE Staircase"]
        elif detect_data.name == "Mountain Temple 2F Central Staircase Alt":
            detect_data = self.entrances["Mountain Temple 2F Central Staircase"]
        elif exit_data.name == "Mountain Temple 2F NE Staircase Alt":
            exit_data = self.entrances["Mountain Temple 2F NE Staircase"]
        elif exit_data.name == "Mountain Temple 2F Central Staircase Alt":
            exit_data = self.entrances["Mountain Temple 2F Central Staircase"]
        elif detect_data.name == "Tower of Spirits Staircase Elevators":
            detect_data = self.entrances["Tower of Spirits Staircase Exit"]

        new_data = {detect_data.id, exit_data.id} if not ctx.slot_data.get(
            "decouple_shuffled_entrances", False) and detect_data.two_way else {detect_data.id}
        printl(f"New Storage Data: {new_data}")

        if interaction == "check" and [i for i in new_data if i not in self.checked_entrances]:
            key = storage_key(ctx, checked_entrances_key)
            # self.checked_entrances.update(new_data)
        elif interaction == "traverse" and [i for i in new_data if i not in self.traversed_entrances]:
            key = storage_key(ctx, traversed_entrances_key)
            # self.traversed_entrances.update(new_data)
        else:
            printl(f"entrances {new_data} was not new")
            return
        printl(f"Storing new data: {key} {new_data} {self.traversed_entrances}")
        await self.store_data(ctx, key, new_data)

    async def save_scene(self, ctx, read_result, save_addr, save_key, save_comp: "Iterable"):
        if read_result.get(save_addr, False) in save_comp and not self.save_spam_protection:
            if not self.warp_to_start_flag:
                check_respawn = await read_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room])
                self.last_saved_scene = check_respawn[STAddr.respawn_stage] << 8 | check_respawn[STAddr.respawn_room]
            else:
                await write_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room, STAddr.respawn_entrance], self.starting_entrance)
                self.last_saved_scene = self.starting_entrance[0] << 8 | self.starting_entrance[1]
            printl(f"Saving scene {hex(self.last_saved_scene)}")
            await self.store_data(ctx, storage_key(ctx, save_key), self.last_saved_scene, "replace", default=0)
            self.save_spam_protection = True
            await self.save_tos_keycount(ctx)
            return True
        return False

    async def update_safe_respawn(self, ctx, new_exit: "STTransition", last_detect: "STTransition"):
        # await self.change_entrance_animation(ctx, new_exit)
        if new_exit.stage in unsafe_respawn_stages and new_exit.scene not in self.safe_respawn_rooms:
            if self.safe_respawn is None:
                self.safe_respawn = last_detect.entrance
                printl(f"Set new safe respawn: {hex_f(self.safe_respawn)}")
            return
        self.safe_respawn = None

    async def process_map_warp(self, ctx):
        if not ctx.slot_data["enable_map_warp"]:
            return

        async def check_tos():
            """Check for coords on the map that don't zoom in to a station."""
            raw_coords = await STAddr.quick_pen_coords.read(ctx, silent=True)
            if 0x40 < raw_coords & 0xFF < 0x70 < (raw_coords & 0xFF0000) >> 16 < 0x90:
                return "Tower of Spirits Lobby Staircase"
            if 0x15 < raw_coords & 0xFF < 0x29 and 0xc1 < (raw_coords & 0xFF0000) >> 16 < 0xda:
                return "Mountain Temple Lobby Enter Dungeon"
            if 0x59 < raw_coords & 0xFF < 0x75 and 0x23 < (raw_coords & 0xFF0000) >> 16 < 0x35:
                return "Wooded Temple Lobby Enter Dungeon"
            if 0x6 < raw_coords & 0xFF < 0x20 and 0x16 < (raw_coords & 0xFF0000) >> 16 < 0x2b:
                return "Blizzard Temple Lobby Enter Dungeon"
            if 0x87 < raw_coords & 0xFF < 0x9c and 0xdb < (raw_coords & 0xFF0000) >> 16 < 0xf4:
                return "Marine Temple Lobby Enter Dungeon"
            if 0x64 < raw_coords & 0xFF < 0x70 and 0xcc < (raw_coords & 0xFF0000) >> 16 < 0xe8:
                return "Desert Temple Lobby Enter Dungeon"
            return False

        def set_warp_flag(e: "STTransition"):
            self.selected_station = entrance.stage
            if e.scene in self.visited_scenes:
                self.map_warp = entrance
                aliases = {
                    "anouki"
                }
                logger.info(f"Selected station to warp to: {e.name}")
            else:
                logger.info(f"You have yet to visit {e.name}.")

        if self.read_result[STAddr.menu] in [1, 2, 5]:
            if not self.map_warp_item_cache:
                self.map_warp_item_cache = (self.has_from_group(ctx, "Tracks: Forest Glyph"),
                                            self.has_from_group(ctx, "Tracks: Fire Glyph"))
                printl(f"Set map warp cache: {self.map_warp_item_cache}")

            if not self.unlocked_map:
                await STAddr.adv_flags_2.set_bits(ctx, 0x4)
                self.unlocked_map = 1
                printl(f"Adding tracks init {1}")
                self.visited_scenes |= set(get_stored_data(ctx, visited_scenes_key, set()))
                printl(f"visited scenes: {self.visited_scenes} {set(get_stored_data(ctx, visited_scenes_key, set()))}")
            if self.read_result.get(STAddr.map_open, 0):
                if self.warp_to_start_flag:
                    self.warp_to_start_flag = None
                    logger.info(f"Canceled warp to start")
                selected_station = await STAddr.selected_station.read(ctx, silent=True)
                if selected_station:
                    if self.unlocked_map < 2:
                        if not self.map_warp_item_cache[0]:
                            await STAddr.adv_flags_1.unset_bits(ctx, 0x80)
                        if not self.map_warp_item_cache[1]:
                            await STAddr.adv_flags_2.unset_bits(ctx, 0x4)
                        self.unlocked_map = 2
                        printl(f"Removing tracks {2}")
                    if selected_station != self.selected_station:
                        printl(f"Selecting station")
                        self.selected_station = selected_station
                        if selected_station == 0x3f and await STAddr.last_x.read(ctx) > 0x45:
                            entrance = entrance_tuple_to_entrance[(0x3F, 0xA, 0)]
                        elif selected_station == 0x39:  # Lost at sea
                            entrance = entrance_tuple_to_entrance[(0x39, 0xA, 0)]
                        else:
                            entrance = entrance_tuple_to_entrance.get(
                                map_warp_redirects.get(selected_station, None),
                                entrance_tuple_to_entrance.get(
                                    (selected_station, 0, 0),
                                    None))
                        if not entrance:
                            logger.info(f"Oops that didn't work {(selected_station, 0, 0)}")
                        elif await self.conditional_er(ctx, entrance):
                            set_warp_flag(entrance)
                    in_submap = await STAddr.exiting_map.read(ctx, silent=True) != 0xFF

                    if self.unlocked_map == 2 and in_submap:
                        self.unlocked_map = 3
                        printl(f"Loaded submap {3}")
                    elif self.unlocked_map == 3 and not in_submap:
                        await STAddr.adv_flags_2.set_bits(ctx, 0x4)
                        self.unlocked_map = 4
                        printl(f"Unlocked submap {4}")
                elif self.unlocked_map == 4:  # not selected_station
                    self.unlocked_map = 1
                    printl(f"Reset cycle {1}")
                    if not self.map_warp_item_cache[0]:
                        await STAddr.adv_flags_1.set_bits(ctx, 0x80)
                else:
                    coord_warp = await check_tos()
                    if not coord_warp:
                        return
                    entrance = self.entrances[coord_warp]
                    if self.selected_station != entrance.stage:
                        set_warp_flag(entrance)

        elif self.unlocked_map:
            if not self.map_warp_item_cache[1]:
                await STAddr.adv_flags_2.unset_bits(ctx, 0x4)
            self.unlocked_map = 0
            self.selected_station = 0
            self.map_warp_item_cache = None
            printl(f"Quitting tracks {0}")

    async def process_map_objects(self, ctx):
        whitelisted_stages = list(range(0x18, 0x1e)) + list(range(0x30, 0x35)) + [0x13, 0x2D, 0x2E, 0x37, 0x3E, 0x3F, 0x41, 0x42] + list(range(0x45, 0x4B))
        if self.current_stage not in whitelisted_stages:
            return

        table_size = await self.load_map_object_table(ctx)
        actor_idents = await self.get_table_data(ctx, STAddr.map_object_table, 0,
                                                 size=3, table_label=False, table_size=table_size)
        printl(f"map objects: {hex_f(actor_idents)}")

        identifiers = map_object_identifiers

        write_list = []
        for addr, i in actor_idents.items():
            if addr == 0x5544:
                printl("Map Object Overflow!")
                break
            if i not in identifiers:
                printl(f"Unknown map object: {hex_f(i)} @ {addr}")
                continue

            if identifiers.get(i) in ["Blue Door", "Key Door", "Arena Door", "Bell Door", "Gem Door"]:
                write_list.append(Address.from_pointer(addr + 33*4 + 2, size=1).get_inner_write_list(0))  # closing
                write_list.append(Address.from_pointer(addr + 34*4 + 2, size=1).get_inner_write_list(0))  # opening

                if identifiers.get(i) == "Key Door":
                    self.key_door_watches.append(Address.from_pointer(addr + 22, 1))

                # if self.current_scene == 0x4206 and all([LOCATIONS_DATA[l]['id'] in ctx.checked_locations for l in [
                #         "Lost at Sea Final Challenge SE Chest", "Lost at Sea Final Challenge NE Chest",
                #         "Lost at Sea Final Challenge SW Chest", "Lost at Sea Final Challenge NW Chest"
                #     ]]):
                #         write_list.append(Address.from_pointer(addr + 22).get_inner_write_list(3))

            if identifiers.get(i) in ["Bridge"]:
                write_list.append(Address.from_pointer(addr+24*4, size=2).get_inner_write_list(0))

            if identifiers.get(i) in ["Switch"]:
                write_list.append(Address.from_pointer(addr+9*4 + 2, size=1).get_inner_write_list(0))

            if identifiers.get(i) in ["Spikes"]:
                write_list.append(Address.from_pointer(addr+19*4+3, size=1).get_inner_write_list(0))

            if identifiers.get(i) in ["Boss Door"]:
                await self.open_boss_door(ctx, addr)
                self.boss_door_addr = addr

            if identifiers.get(i) in ["Torch"]:
                write_list.append(Address.from_pointer(addr+33*4 + 2, size=1).get_inner_write_list(0))

            # if identifiers.get(i) in ["Flames"]:
            #     write_list.append(Address.from_pointer(addr + 33 * 4 + 2, size=1).get_inner_write_list(0))

        if write_list:
            printl(f"Deleting Cutscenes: {hex_f(write_list)}")
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

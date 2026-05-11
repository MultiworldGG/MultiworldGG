
from .DSZeldaClient.DSZeldaClient import *
from .DSZeldaClient.subclasses import storage_key, split_bits
from .data.Addresses import STAddr
from .data.Items import ITEMS
from .data.Entrances import ENTRANCES
from settings import get_settings
from typing import Literal

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor
    from . import SpiritTracksSettings
    from .Subclasses import STTransition

# gMapManager -> mCourse -> mSmallKeys
SMALL_KEY_OFFSET = 0x260
STAGE_FLAGS_OFFSET = 176
TRAIN_SPEED_OFFSET = 0x94
TRAIN_GEAR_OFFSET = 0x27c
TRAIN_QUICK_STATION_OFFSET = 0x80
default_train_speed = (-143, 0, 115, 193)

train_speed_addresses = [STAddr.train_speed_reverse, STAddr.train_speed_stop, STAddr.train_speed_med, STAddr.train_speed_fast]

# Addresses to read each cycle
read_keys_always = [STAddr.game_state, STAddr.received_item_index, STAddr.stage, STAddr.room, STAddr.entrance, STAddr.slot_id, STAddr.menu,
                    STAddr.loading_room, STAddr.mid_load, STAddr.saving]
read_keys_land = [STAddr.getting_location, STAddr.getting_item_safety, STAddr.health]
read_keys_train = [STAddr.train_health]

rabbit_storage_key = "rabbit_locs"
saved_scene_key = "last_saved_scene"
checked_entrances_key = "st_checked_entrances"

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
        self.output(f"Primed a warp to start. Enter any entrance or save and quit warp to Outset")
    else:
        self.output(f"Canceled Warp to Start")
    return True

def cmd_goal(self: "BizHawkClientCommandProcessor"):
    """Display the current goal and progress towards it. Only works while in-game."""
    client = get_client_as_command_processor(self)
    client.display_goal = True
    return True

class SpiritTracksClient(DSZeldaClient):
    game = "Spirit Tracks"
    system = "NDS"
    train_speed_addr: "Address"
    train_speed_pointer: "Address"
    train_gear_addr: "Address"

    def __init__(self) -> None:
        super().__init__()

        # Required variables
        self.starting_flags = STARTING_FLAGS
        self.dungeon_key_data = DUNGEON_KEY_DATA
        self.starting_entrance = (0x2F, 0, 1)  # stage, room, entrance
        self.scene_addr = (STAddr.stage, STAddr.room, STAddr.floor, STAddr.entrance)  # Stage, room, floor, entrance

        self.exit_coords_addr = ()  # TODO: x, y, z. what coords to spawn link at when entering a continuous transition
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
        self.addr_game_state = STAddr.game_state
        self.addr_slot_id = STAddr.slot_id
        self.addr_stage = STAddr.stage
        self.addr_room = STAddr.room
        self.addr_entrance = STAddr.entrance
        self.addr_received_item_index = STAddr.received_item_index
        self.health_address = STAddr.health

        self.update_rabbits = False
        self.rabbit_tracker = [0]*7  # list of bytes(as ints) for found overworld rabbits
        self.rabbit_counter = [0]*5  # list of counts for each rabbit type caught in the overworld

        self.visited_entrances = set()
        self.event_reads = []
        self.sent_event = False
        self.event_data = []
        self.entrances = ENTRANCES
        self.boss_warp_entrance = None
        self.location_id_to_name = {loc["id"]: loc_name for loc_name, loc in LOCATIONS_DATA.items()}
        self.exit_coords_addr = (STAddr.train_trans_x, STAddr.train_trans_y, STAddr.train_trans_z)

        # Train speed stuff
        self.reset_cycles = 0
        self.last_train_gear = 2
        self.reload_on_item = False
        self.train_snap_speed = True
        self.train_quick_station = True
        self.update_train_speed: bool = False
        self.train_speed = [-143, 0, 115, 193]
        self.key_address = STAddr.small_keys

        self.hint_data = HINT_DATA
        self.got_item_no_loc = False
        self.potion_tracker = [0, 0]
        self.save_ammo = None
        self.drinking_potion = False
        self.addr_drinking_potion = None
        self.set_train_in_overworld: bool = False

        self.boss_key_y = None
        self.boss_key_read = None
        self.snurglar_addr = None
        self.last_anticipated_locations = []
        self.delay_room_action: int = 0
        self.saving = False
        self.saving_safety = False

        self.display_goal = False
        self.oct_bk_offset = None


    def print_goal_info(self, ctx):
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
            dungeon_locs = slot_data["required_dungeons"]
            has_locs = sum([1 for loc in ctx.checked_locations if loc in dungeon_locs])
            logger.info(
                f"You need to complete {specific}dungeons to enter the dark realm. Progress: {has_locs}/{slot_data['dungeons_required']}")
            if slot_data["dungeon_hints"]:
                dungeons_locs = [self.location_id_to_name[i] for i in slot_data["required_dungeons"]]
                logger.info(f"Your dungeons: {dungeons_locs}")
        if slot_data["dark_realm_access"] in [2, 3]:
            shard_count = self.item_count(ctx, "Compass of Light Shard")
            logger.info(
                f"You need Compass Shards to access the Dark Realm. You have {shard_count}/{slot_data['compass_shard_count']}")


    async def get_small_key_address(self, ctx) -> int:
        return STAddr.small_keys

    async def check_game_version(self, ctx: "BizHawkClientContext") -> bool:
        rom_name_bytes = await STAddr.game_identifier.read_bytes(ctx)
        rom_name = bytes([byte for byte in rom_name_bytes[0] if byte != 0]).decode("ascii")
        print(f"Rom Name: {rom_name}")
        if rom_name == "SPIRITTRACKSBKIP":  # EU

            # Set commands
            if "train_speed" not in ctx.command_processor.commands:
                ctx.command_processor.commands["train"] = cmd_train_option
            if "warp_to_start" not in ctx.command_processor.commands:
                ctx.command_processor.commands["warp_to_start"] = cmd_warp_to_start
            if "goal" not in ctx.command_processor.commands:
                ctx.command_processor.commands["goal"] = cmd_goal
            return True
        return False

    async def set_special_starting_flags(self, ctx: "BizHawkClientContext") -> list[tuple[int, list, str]]:
        res = []
        return res

    def get_coord_address(self, at_sea=None, multi=False):
        return STAddr.link_x, STAddr.link_y, STAddr.link_z

    async def get_coords(self, ctx, multi=False):
        # print(f"Coords: {[self.read_result.get(a, 0) for c, a in zip(['x', 'y', 'z'], self.get_coord_address())]}")
        # return {c: self.read_result.get(a, 0) for c, a in zip(['x', 'y', 'z'], self.get_coord_address())}
        if self.current_stage < 0x13:
            coords = await read_multiple(ctx, STAddr.train_coords, True)
            train_coords = {l: c for c, l in zip(coords.values(), ['x', 'y', 'z'])}
            # print(f"Train coords: {train_coords}")
            return train_coords
        coords = await read_multiple(ctx, self.get_coord_address(multi=multi), signed=True)
        # print(f"Coords: {coords}")
        return {
            "x": coords[STAddr.link_x],
            "y": coords[STAddr.link_y],
            "z": coords[STAddr.link_z]
        }


    async def has_special_dynamic_requirements(self, ctx: "BizHawkClientContext", data) -> bool:
        def check_dungeon_reqs():
            if "dungeons" in data:
                if ctx.slot_data["dark_realm_access"] != 1:
                    return data["dungeons"]  # Case where dungeons are not required for dark realm
                print(f"{ctx.slot_data['required_dungeons']}")
                dungeon_locs = ctx.slot_data["required_dungeons"]
                has_locs = sum([1 for loc in ctx.checked_locations if loc in dungeon_locs])
                comp = has_locs >= ctx.slot_data["dungeons_required"]
                print(f"Checking dungeons: {has_locs} >= {ctx.slot_data['dungeons_required']} for comp {data['dungeons']}")
                return comp == data["dungeons"]
            return True

        async def check_coords():
            coord_data = data.get("coords", {})
            if coord_data:
                coords = await self.get_coords(ctx)
                print(f"\t\tCoords: {coords} reqs {coord_data}")
                return all([
                    coord_data.get("x_max", 0xFFFFFFF) > coords['x'] > coord_data.get("x_min", -0xFFFFFFF),
                    coord_data.get("y", coords['y']) + 2000 > coords['y'] >= coord_data.get("y", coords['y']),
                    coord_data.get("z_max", 0xFFFFFFF) > coords['z'] > coord_data.get("z_min", -0xFFFFFFF),
                ])

            return True

        if not check_dungeon_reqs():
            print(f"\t{data['name']} does not have dungeon requirements")
            return False
        if not await check_coords():
            print(f"\t{data['name']} does not have coordinate requirements")
            return False
        return True


    async def full_heal(self, ctx, bonus=0):

        hearts = (self.item_count(ctx, "Heart Container") + 3)*4
        print(f"Full Heal: {hearts}")
        await STAddr.health.overwrite(ctx, hearts+bonus)

    async def watched_intro_cs(self, ctx):
        watched_intro = await STAddr.watched_intro.read(ctx) & 1
        return watched_intro

    async def update_main_read_list(self, ctx: "BizHawkClientContext", stage: int, in_game=True):
        read_keys = read_keys_always
        if stage in range(4, 0xb):
            read_keys += read_keys_train
            self.health_address = STAddr.train_health

            train_speed_thingy = (await STAddr.train_speed_pointer.read(ctx)) - 0x2000000
            print(f"Train speed thingy {hex(train_speed_thingy)}")
            if 0x400000 > train_speed_thingy > 0:
                self.train_speed_pointer = train_speed_thingy
                self.train_gear_addr = Address.from_pointer(self.train_speed_pointer+TRAIN_GEAR_OFFSET)
                read_keys.append(self.train_gear_addr)
        else:
            read_keys += read_keys_land
            self.health_address = STAddr.health

            offset = 0xf80 if self.current_stage == 0x29 else 0xf64
            potion_addr = await STAddr.drinking_potion_pointer.read(ctx) - 0x2000000 + offset
            if 0x400000 > potion_addr > 0:
                self.addr_drinking_potion = Address.from_pointer(potion_addr, size=4)
                read_keys.append(self.addr_drinking_potion)
            print(f"Potion pointer {hex(potion_addr)}")

        self.main_read_list = read_keys
        # print(f"read keys len: {len(read_keys)}")
        # print(self.main_read_list, read_keys)
        # print(f"Slot data {ctx.slot_data}")

    def process_loading_variable(self, read_result) -> bool:
        mid_load = read_result.get(STAddr.mid_load, True) == 0xFF
        if self._loading_scene and not self.loading_stage:
            if mid_load:
                self.loading_stage = True

        if self.loading_stage:
            if not mid_load:
                self.loading_stage = False
                return mid_load
        return not read_result.get(STAddr.loading_room, 27)

    async def process_read_list(self, ctx: "BizHawkClientContext", read_result: dict):
        current_menu: "Address" = read_result[STAddr.menu]
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
            self.saving_safety = read_result[STAddr.getting_item_safety]
        else:
            safe_save = False
            if self.current_stage in range(0x1e, 0x23):
                safe_save = self.saving_safety == read_result[STAddr.getting_item_safety]
                # print(f"Checking Safe Save!")
            self.saving = read_result[STAddr.getting_location] or read_result[STAddr.saving] or safe_save

        # Weird scene value on load from menu, set to last saved scene
        if read_result[STAddr.stage] == 0x79 and self.last_saved_scene:
            stage = (self.last_saved_scene & 0xFF00) >> 8

            print(f"Overwriting weird scene: {hex(self.last_saved_scene)}")
            stage, room = (self.last_saved_scene & 0xFF00) >> 8, self.last_saved_scene & 0xFF

            self.current_scene = self.last_saved_scene
            self.current_stage = read_result[STAddr.stage] = stage
            read_result[STAddr.room] = room
            print(hex(self.current_scene), hex(self.current_stage))
            await STAddr.stage.overwrite(ctx, stage)
            await STAddr.room.overwrite(ctx, room)

        # print(f"Goal check {ctx.slot_data['goal']} last {self.last_stage} current {hex(self.current_stage)}")
        if ctx.slot_data["goal"] == -1:
            if self.last_stage == 0x27 and self.current_stage == 0x25:
                self.has_goal_location = True
                await self.store_event(ctx, "GOAL: Defeat Malladus")

    async def store_event(self, ctx, event_name):
        entr = self.entrances[event_name]
        await self.store_visited_entrances(ctx, entr, entr.vanilla_reciprocal)

    async def update_potion_tracker(self, ctx, spec=""):
        reads = await read_multiple(ctx, [STAddr.potion_0, STAddr.potion_1])
        new_potions = list(reads.values())
        res = False
        if new_potions != self.potion_tracker:
            print(F"New Potions: {new_potions} {spec}")
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
        print(f"Updating Treasure Tracker: {last_loc}")

        if last_loc == "no_loc":
            self.treasure_tracker = new_treasure
            self.got_item_no_loc = True
            return
        elif not (last_loc == "post_receive" and self.got_item_no_loc):
            self.treasure_tracker = new_treasure
            print(f"No special treasure")
            return

        self.got_item_no_loc = False
        diff = {t: n - o for n, o, t in
                zip(new_treasure.values(), self.treasure_tracker.values(), ITEM_GROUPS["All Treasures"]) if n - o > 0}
        if not diff:
            await self.check_potion_location(ctx)
            return

        single_item = [t for t in diff][0]
        print(f"Updated Treasure Tracker: {diff}")

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
        if ctx.slot_data["excess_random_treasure"] in [0, 2]:
            print(f"Removing {diff} from treasures")
            await remove_treasure()
            # self.last_vanilla_item.extend([t for t in diff])
        if ctx.slot_data["excess_random_treasure"] == 2:
            rupees = sum([TREASURE_PRICES[treasure]*count for treasure, count in diff.items()])
            print(f"Getting {rupees} rupees")
            await STAddr.rupees.add(ctx, rupees)


        self.treasure_tracker = new_treasure

    async def receive_item_post_processing(self, ctx, item_name, item_data):
        print(f"Post Processing {item_name}")

        if "Rabbit" in item_name:
            await self.update_rabbit_count(ctx)
        if "Treasure:" in item_name:
            await self.update_treasure_tracker(ctx, "item_process")
        if item_name == "Bombs (Progressive)" and self.current_scene == 0x4503:
            await STAddr.adv_flags_22.unset_bits(ctx, 2)

        if self.reload_on_item:
            print(f"Reloading dynamic entrances")
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
            self.set_train_in_overworld = True
            await self.set_starting_train(ctx)

        if "ammo" in ctx.slot_data["shopsanity"] and self.current_scene in ammo_shop_lookup and item_name in ITEM_GROUPS["Ammo Items"]:
            addr = item_data.ammo_address if hasattr(item_data, "ammo_address") else item_data.address
            await addr.overwrite(ctx, 0)
            item_count = self.item_count(ctx, item_data.refill) if item_name in ITEM_GROUPS["Refill Items"] else self.item_count(ctx, item_name)
            self.save_ammo[addr] = item_data.give_ammo[item_count-1]

        # Open boss door if got key in that room
        if (item_name.startswith("Boss Key") or
            (item_name.startswith("Keyring") and ctx.slot_data["big_keyrings"])
        ) and self.current_scene in BOSS_KEY_DATA:
            if self.current_stage == 0x13:
                await self.open_tos_boss_door(ctx, self.current_scene)
            else:
                data = BOSS_KEY_DATA[self.current_scene]
                if data["dungeon"] in item_name and (self.current_scene & 0xff00 != 0x1300 or self.location_name_to_id[data["location"]] in ctx.checked_locations):
                    print(f"Opening boss door for {hex(self.current_scene)}")
                    await data["door"].overwrite(ctx, 3)

        # Complex blocked scenes for sources in boss rooms
        if (self.current_scene in BOSS_ROOM_TO_BLOCKED_ITEM_GROUP and
            BOSS_ROOM_TO_BLOCKED_ITEM_GROUP[self.current_scene] in item_data.item_groups):
            bit = 2 ** (self.current_stage-0x1a)
            await STAddr.sources.unset_bits(ctx, bit)


    async def process_on_room_load(self, ctx, current_scene, read_result: dict):
        await self.update_treasure_tracker(ctx, "room_load")
        await self.update_potion_tracker(ctx, "room_load")
        await self.update_rabbit_count(ctx)

        # print(F"Room load goal: {ctx.slot_data['goal']}, {ctx.slot_data['endgame_scope']}, {self.current_stage}")
        if (ctx.slot_data["goal"] == -1 and ctx.slot_data["endgame_scope"] == 5
                and self.current_stage in [0xF, 0x10, 0x24, 0x25, 0x27]):
            self.has_goal_location = True
            await self.store_event(ctx, "GOAL: Enter Dark Realm")

    async def process_in_game(self, ctx, read_result: dict):
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

    async def set_train_speed(self, ctx):
        await write_multiple(ctx, train_speed_addresses, self.train_speed)
        self.last_train_gear = -1  # force a quick speed increase
        self.train_speed_pointer = (await STAddr.train_speed_pointer.read(ctx)) - 0x2000000
        try:
            self.train_speed_addr = Address.from_pointer(self.train_speed_pointer + TRAIN_SPEED_OFFSET, size=4)
        except AssertionError:
            logger.warning(f"Tried to load train speed while not on train")
            return

    async def process_slow(self, ctx: "BizHawkClientContext", read_result: dict):
        await self.anticipate_location(ctx, read_result)
        if self.delay_room_action:
            self.delay_room_action -= 1
            if self.delay_room_action > 0:
                return

            # Set train speed stuff
            if self.current_stage in range(4, 0xb):
                await self.set_train_speed(ctx)

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

            # Change respawn data to outside tower section in ToS
            if self.current_stage == 0x13:
                section = TOS_FLOOR_TO_SECTION[self.current_room]
                entrance = self.entrances[TOS_SECTION_TO_EXIT[section]]
                reverse_entrance: "STTransition" = self.entrance_id_to_entrance[
                    ctx.slot_data["er_pairings"][str(entrance.id)]] if str(entrance.id) in ctx.slot_data[
                    "er_pairings"] else entrance.vanilla_reciprocal
                respawn_data = reverse_entrance.entrance
                print(f"Setting ToS respawn room {respawn_data}")
                await write_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room, STAddr.respawn_entrance],
                                     respawn_data)

        if self.display_goal:
            self.print_goal_info(ctx)
            self.display_goal = False

    async def process_fast(self, ctx: "BizHawkClientContext", read_result: dict):
        await self.save_scene(ctx, read_result, STAddr.saving, saved_scene_key, range(1, 5))
        await self.drink_potion(ctx, read_result)

        if self.snurglar_addr in read_result:
            if read_result[self.snurglar_addr] & 0x20:
                print(f"Opening Mountain Temple! {self.snurglar_addr}")
                await self.snurglar_addr.set_bits(ctx, 0x10)
                self.main_read_list.remove(self.snurglar_addr)


    async def anticipate_location(self, ctx: "BizHawkClientContext", read_result: dict):
        if read_result[STAddr.stage] < 0x13 or self.getting_location:
            return
        # print(f"Locations in scene: {[l for l in self.locations_in_scene]}")
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
            print(f"\tno location")
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
        print(f"Reseting treasure models")
        await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def swap_models(self, ctx, locations: list, treasure_mode=False):
        print(f"\tMultiple locations: {locations}")
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
            for item in vanilla_items:
                if not priority:
                    # set location_id to None if there's a location conflict
                    item_location_check[item] = None if item in item_location_check else loc_data['id']
                    continue

                # Sort locations by priority if applicable
                if item in item_priority and priority >= item_priority[item]:
                    continue
                item_location_check[item] = loc_data['id']
                item_priority[item] = priority

        print(f"Items with locations: {[(i, l) for i, l in item_location_check.items()]}")

        model_data = ctx.slot_data.get("model_lookup", {})
        write_list = []
        print_list = {}
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
                    print(f"Vanilla item {i}, {l}")
                    model_name = ITEMS[i].model
                    model_value = ITEM_MODEL_LOOKUP[model_name].value if model_name else generic_model


            # add models to write list
            bits = split_bits(model_value, 4)
            bits.reverse()
            write_list.append((STAddr.item_model_table.addr + 4 * vanilla_model.offset, bits, "Main RAM"))
            if l is not None:
                print_list[self.location_id_to_name[l]] = model_name

        print(f"Swapped Models: {print_list}")
        if write_list:
            await bizhawk.write(ctx.bizhawk_ctx, write_list)

    async def drink_potion(self, ctx, read_results):
        drinking_potion = read_results.get(self.addr_drinking_potion, 0)
        if drinking_potion == 0x3b:
            self.drinking_potion = True
        if self.drinking_potion and drinking_potion == 0x39:
            self.drinking_potion = False
            await self.update_potion_tracker(ctx, "drunk_potion")

    def cancel_location_read(self, location) -> bool:
        if "stamp" in location:
            return True
        if "rabbit" in location:
            return True
        return False

    async def check_location_post_processing(self, ctx, location: dict):
        print(f"Post processing loc {location}")
        if not location:
            await self.update_treasure_tracker(ctx, "no_loc")
            return

        if "goal" in location:
            from .data.Entrances import goal_event_lookup
            goal = ctx.slot_data.get("goal", -1)
            loc_goal = location["goal"]
            if goal_event_lookup[goal] == loc_goal:
                await self.store_event(ctx, loc_goal)
                self.has_goal_location = True

        if "rabbit" in location and "address" in location:
            await self.store_rabbit(ctx, location)

        # Connect event
        if "ut_connect" in location:
            event_name = location["ut_connect"]
            await self.store_event(ctx, event_name)

        if location["name"] in ["Outset Bee Tree", "Outset Clear Rfocks"]:
            self.reload_on_item = True

        if "Tear of Light" in location.get("vanilla_item", "") and ctx.slot_data["randomize_tears"] != -1:
            await STAddr.tears_of_light.overwrite(ctx, 1)  # prevent cutscene and underflow

        if location["name"] in ["ToS 1F Chest"] and ctx.slot_data["randomize_tears"] != -1:
            await self.set_tears(ctx)

        if self.current_scene in [0x1309, 0x1318] and isinstance(location.get("vanilla_item", ""), str) and location.get("vanilla_item", "").startswith("Boss Key"):
            section = {0x1309: 3, 0x1318: 5}[self.current_scene]
            if self.item_count(ctx, f"Boss Key (ToS {section})") or (self.item_count(ctx, f"Keyring (ToS {section})") and ctx.slot_data["big_keyrings"]):
                print("Opening ToS boss door after having key and getting boss key location")
                await self.open_tos_boss_door(ctx, self.current_scene)

        if self.snurglar_addr and location["name"] in LOCATION_GROUPS["Snurglars"]:
            await self.snurglar_addr.unset_bits(ctx, 0xF)

    # fixes conflict with bizhawk_UT
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        await super().game_watcher(ctx)

    async def process_game_completion(self, ctx: "BizHawkClientContext"):
        if self.has_goal_location:
            return True
        return False

    async def update_rabbit_count(self, ctx):
        if self.current_stage in [4, 5, 6, 7]:
            self.update_rabbit_tracker(ctx)
            rabbit_bits = self.rabbit_tracker
        else:
            realms = rabbit_realms
            rabbit_counts = [min(sum([ITEMS[i].value*self.item_count(ctx, i) for i in ITEM_GROUPS[f"{realm} Rabbits"]]), 10) for realm in realms]
            rabbit_bits = sum([(2 ** count - 1) << 10*i for i, count in enumerate(rabbit_counts)])
            print(f"Updating rabbit bits {hex(rabbit_bits)}")
        await STAddr.rabbits.overwrite(ctx, rabbit_bits)

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
            rabbit_count = self.rabbit_counter[rabbit_type_lookup.index(rabbit_type)]
            if rabbit_count <= 0:
                rabbit_count = 1  # Hope this just works
            plural = "s" if rabbit_count > 1 else ""
            total_loc = f"Catch {rabbit_count} {rabbit_type}{plural}"
            print(f"Sending rabbit total location {total_loc} {self.rabbit_counter}")
            await self._process_checked_locations(ctx, total_loc)

    def update_rabbit_tracker(self, ctx):
        rabbit_storage = ctx.stored_data.get(storage_key(ctx, rabbit_storage_key), None)
        rabbit_storage = [0]*7 if rabbit_storage is None else rabbit_storage
        print(f"\tRabbit storage: {rabbit_storage}")
        self.rabbit_tracker = [s | c for s, c in zip(rabbit_storage, self.rabbit_tracker)]
        print(f"\trabbit tracker {self.rabbit_tracker}")
        all_rabbits = sum([r << 8*i for i, r in enumerate(self.rabbit_tracker)])
        print(f"\tall rabbits: {hex(all_rabbits)}")
        self.rabbit_counter = [count_bits(all_rabbits & (0x3FF << n*10)) for n in range(5)]
        print(f"Updating Rabbit tracker: {[hex(i) for i in self.rabbit_tracker]} {self.rabbit_counter}")

    async def on_connect(self, ctx):
        self.rabbit_tracker = [0]*7
        await ctx.send_msgs([{
                "cmd": "Get",
                "keys": [storage_key(ctx, rabbit_storage_key)],
            }])

        # Get train settings from host.yaml
        host_settings: SpiritTracksSettings = get_settings().get('tloz_st_options')
        print(f"SETTINGS: {host_settings.get('train_speed', self.train_speed)}")
        self.train_speed = host_settings.get("train_speed", self.train_speed)
        self.train_snap_speed = host_settings.get("train_snap_speed", self.train_snap_speed)
        self.train_quick_station = host_settings.get("train_quick_station", self.train_quick_station)


    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead, stage, read_result):
        if read_result[STAddr.menu] and stage >= 0x13:
            return
        # if stage < 0x13:  # deaths work badly on train
        #     return

        if ctx.last_death_link > self.last_deathlink and not is_dead:
            # A death was received from another player, make our player die as well
            await self.health_address.overwrite(ctx, 0)

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

    async def get_item_read(self, ctx, item_name) -> int:
        if item_name == "Red Potion":
            return await STAddr.all_potions.read(ctx)

        return await super().get_item_read(ctx, item_name)

    async def process_post_receive(self, ctx):
        if not self.delay_pickup:
            await self.update_treasure_tracker(ctx, "post_receive")  # always update treasure tracker, lots of random treasures on ground!

    async def set_stage_flags(self, ctx, stage):
        if stage in STAGE_FLAGS:
            stage_address = await STAddr.stage_flag_pointer.read(ctx)
            stage_flag_address = Address.from_pointer(stage_address + STAGE_FLAGS_OFFSET - 0x2000000, size=4)
            if ctx.slot_data["randomize_passengers"] == 0:
                if stage == 0x35:
                    STAGE_FLAGS[stage] = [0x16, 0x00, 0x00, 0x00]
                elif stage == 0x35:
                    STAGE_FLAGS[stage] = [0x16, 0x04, 0x00, 0x00]
            print(f"Setting stage flags for stage {hex(stage)} at {stage_flag_address}: {[hex(i) for i in STAGE_FLAGS[stage]]}")
            await stage_flag_address.set_bits(ctx, STAGE_FLAGS[stage])
        if self.set_train_in_overworld:
            await self.set_starting_train(ctx)
            self.set_train_in_overworld = False

        # Give tears of light when entering ToS
        if stage == 0x13 and ctx.slot_data["randomize_tears"] != -1:
            await self.set_tears(ctx)

    async def set_tears(self, ctx):
        set_tears = (self.item_count(ctx, "Tear of Light (All Sections)")
                     or self.item_count(ctx, "Big Tear of Light (All Sections)") * 3)
        if not set_tears:
            section = TOS_FLOOR_TO_SECTION.get(self.current_room, 0)
            if ctx.slot_data["shuffle_tos_sections"] and ctx.slot_data.get("tear_sections", 2) == 2:
                print(f"Section {section} is order {ctx.slot_data['tower_section_lookup']}!")
                section = ctx.slot_data["tower_section_lookup"][str(section)]

            if section == 6:
                return
            big_prog_sub = section - 1
            set_tears = (self.item_count(ctx, f"Tear of Light (ToS {section})")
                         or self.item_count(ctx, f"Big Tear of Light (ToS {section})") * 3
                         or max(0, (self.item_count(ctx, "Big Tear of Light (Progressive)") - big_prog_sub) * 3)
                         or max(0, self.item_count(ctx, "Tear of Light (Progressive)") - big_prog_sub * 3)
                         )
            print(f"Setting tears for section {section} tears {set_tears}")
        else:
            print(f"Setting tears {set_tears}")

        await STAddr.tears_of_light.overwrite(ctx, set_tears)

    async def process_in_menu(self, ctx, read_result):
        await self.get_saved_scene(ctx, saved_scene_key)

    # UT store entrances to defer
    async def store_visited_entrances(self, ctx: "BizHawkClientContext", detect_data, exit_data,
                                      interaction="traverse"):
        self.visited_entrances |= set(get_stored_data(ctx, checked_entrances_key, set()))
        new_data = {detect_data.id, exit_data.id} if not ctx.slot_data.get(
            "decouple_entrances", False) and detect_data.two_way else {detect_data.id}
        print(f"New Storage Data: {new_data}")

        if new_data:
            key = storage_key(ctx, checked_entrances_key)
            await self.store_data(ctx, key, new_data)

    async def reset_snurglar_door(self, ctx):
        if self.last_scene == 0x700:
            snurglar_ids = [self.location_name_to_id[f"Snurglars {color} Key"] for color in ["Purple", "Orange", "Gold"]]
            for i in snurglar_ids:
                if i not in ctx.checked_locations:
                    await self.snurglar_addr.unset_bits(ctx, 0x30)
                    break


    async def detected_new_scene(self, ctx):
        await self.save_tos_keycount(ctx)
        self.event_reads = []
        self.sent_event = False
        if self.last_scene == 0x700:
            await self.reset_snurglar_door(ctx)

        if self.current_scene in potion_location_lookup:
            print(f"Setting shop models")
            await self.set_shop_models(ctx)

    async def set_shop_models(self, ctx: "BizHawkClientContext", on_load=True):
        """Laad shop models in bulk"""
        valid_locations = []
        valid_locations += list(self.location_area_to_watches.get(self.current_scene, {}).keys())
        # valid_locations += list(ammo_shop_lookup.get(self.current_scene, {}).values())
        if not on_load:
            valid_locations += list(potion_location_lookup.get(self.current_scene, {}).values())
            valid_locations += [loc for treasures in SHOP_TREASURE_DATA.get(self.current_scene, []) for loc in treasures.get("locations", [])]
        print(f"Setting shop models {self.current_scene}: {valid_locations}")
        for loc in valid_locations.copy():
            if self.location_name_to_id[loc] in ctx.checked_locations:
                valid_locations.remove(loc)
                print(f"Already checked location {loc}!")
        await self.swap_models(ctx, valid_locations)
        if on_load:
            await self.reset_treasure_models(ctx)


    async def save_scene(self, ctx, read_result, save_addr, save_key, save_comp: "Iterable"):
        if read_result.get(save_addr, False) in save_comp and not self.save_spam_protection:
            if not self.warp_to_start_flag:
                check_respawn = await read_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room])
                self.last_saved_scene = check_respawn[STAddr.respawn_stage] << 8 | check_respawn[STAddr.respawn_room]
            else:
                await write_multiple(ctx, [STAddr.respawn_stage, STAddr.respawn_room, STAddr.respawn_entrance], self.starting_entrance)
                self.last_saved_scene = self.starting_entrance[0] << 8 | self.starting_entrance[1]
            print(f"Saving scene {hex(self.last_saved_scene)}")
            await self.store_data(ctx, storage_key(ctx, save_key), self.last_saved_scene, "replace", default=0)
            self.save_spam_protection = True
            await self.save_tos_keycount(ctx)
            return True
        return False


    async def save_tos_keycount(self, ctx):
        """ToS keycount is not dependent on stage, so save current count on room change or save"""
        print(f"Saving Keycount {self.last_stage} {self.last_scene}")
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
                print(f"Saving ToS key count: {hex(new_data)}")
                await STAddr.key_storage_tos.overwrite(ctx, new_data)

    async def enter_special_key_room(self, ctx, stage, scene_id):
        if stage == 0x13:
            section = TOS_FLOOR_TO_SECTION[self.current_room]
            key_code = 0x130 + section
            print(f"Special Keycode: {key_code} {DUNGEON_KEY_DATA.get(key_code)}")
            if key_code in DUNGEON_KEY_DATA:
                key_data = DUNGEON_KEY_DATA[key_code]
                key_storage = await STAddr.key_storage_tos.read(ctx)
                current_keys = (key_storage & key_data["filter"]) // key_data["value"]
                print(f"Current Keys = {current_keys} | {(key_storage & key_data['filter'])} / {key_data['value']}")
                await self.key_address.overwrite(ctx, current_keys)
            else:
                await self.key_address.overwrite(ctx, 0)
            return True

        return False

    async def detect_ut_event(self, ctx, scene):
        """
        Send UT event locations on certain flags being set in certain scenes.
        """
        if scene in UT_EVENT_DATA and not self.sent_event:
            if not self.event_reads:
                data = UT_EVENT_DATA[scene]
                data = [data] if isinstance(data, dict) else data
                print(f"Event Data {UT_EVENT_DATA} {data}")
                self.event_data = data
                for i, event in enumerate(data):
                    address = Address.from_pointer(self.stage_flag_address + event.get("offset", 0), size=event.get("size", 1)) if event["address"] == "stage_flags" else event["address"]
                    self.event_data[i]["address"] = address
                    self.event_reads.append(address)

            read_results = await read_multiple(ctx, self.event_reads)
            for event, res in zip(self.event_data, read_results.values()):
                # print(read_results)
                if event["value"] & res:
                    if "entrance" in event:
                        print(f"Event detection Success!, {event['entrance']}")
                        entrance = self.entrances[event["entrance"]]
                        await self.store_visited_entrances(ctx, entrance, entrance.vanilla_reciprocal)
                    # elif "event" in event:  # not implemented yet
                    #     print(f"Event detection Success!, {event['event']}")
                    #     key = storage_key(ctx, ut_events_key)
                    #     await self.store_data(ctx, key, [event["event"]])

                    self.event_reads.remove(event["address"])
                    self.event_data.remove(event)
            if not self.event_data:
                print(f"All events sent!")
                self.sent_event = True

        else:
            self.sent_event = True

    @staticmethod
    async def set_starting_train(ctx):
        res = []
        train = ctx.slot_data["starting_train"]
        if train == -1:  # all parts
            res += STAddr.train_parts.get_write_list(0xFFFFFFFF)
            train = 0
        else:
            res += STAddr.train_parts.get_write_list(0xF << (train*4))
        res += [a.get_inner_write_list(train) for a in [
            STAddr.equipped_engine, STAddr.equipped_cannon, STAddr.equipped_car, STAddr.equipped_cart,
        ]]
        print(f"Setting starting train {res}")
        await bizhawk.write(ctx.bizhawk_ctx, res)

    async def get_tos_bk_pointer(self, ctx) -> tuple[Address, int]:
        actor_table = await STAddr.tos_actor_table_pointer_safe.read(ctx)
        offset = 1040 + 8  # start of table + tos bk index
        pointer_addr = Address.from_pointer(actor_table + offset, size=3)
        pointer = await pointer_addr.read(ctx)
        print(f"BK pointer from table read: {pointer_addr} -> {hex(pointer)} actor table: {actor_table}")
        return pointer_addr, pointer

    async def process_hard_coded_rooms(self, ctx, current_scene):
        self.delay_room_action = 5
        if current_scene == 0x2f00 and not await STAddr.set_starting_train.read(ctx) & 4:
            await self.set_starting_train(ctx)
            await STAddr.set_starting_train.set_bits(ctx, 4)
        if self.save_ammo:
            await write_multiple(ctx, list(self.save_ammo.keys()), list(self.save_ammo.values()))
            self.save_ammo = None

        if current_scene in ammo_shop_lookup and "ammo" in ctx.slot_data["shopsanity"]:
            ammo_addresses = [STAddr.bomb_count, STAddr.arrow_count]
            self.save_ammo = await read_multiple(ctx, ammo_addresses)
            await write_multiple(ctx, ammo_addresses, [0, 0])

        # Boss key rando stuff
        if current_scene in BOSS_KEY_DATA and ctx.slot_data.get("randomize_boss_keys", 0):
            data = BOSS_KEY_DATA[self.current_scene]
            # Set key watches
            if self.location_name_to_id[data["location"]] in ctx.checked_locations:
                print(f"Has found location {data['location']}, deleting boss key")
                await self.delete_boss_key(ctx)
            else:
                if "search_data" in data:
                    pointer, offset = await self.find_table_object(ctx, *data["search_data"], return_index=True)
                    self.oct_bk_offset = offset
                    print(f"Found bk in actor loop: {pointer}")
                elif "pointer" in data:
                    pointer = await data["pointer"].read(ctx)
                    print(f"bk pointer: {data['pointer']} -> {hex(pointer)}")
                else:
                    pointer_addr, pointer = await self.get_tos_bk_pointer(ctx)

                if pointer < 0x400000:
                    offset = 12 if self.current_stage == 0x1c else 8
                    self.boss_key_read = Address.from_pointer(pointer+offset, size=4)
                    self.boss_key_y = data["y"]
                    print(f"BK Read: {self.boss_key_read}")
                print(f"Loaded boss key data: {pointer} y: {self.boss_key_y}")

            # Open door
            if self.item_count(ctx, f"Boss Key ({data['dungeon']})") or (self.item_count(ctx, f"Keyring ({data['dungeon']})") and ctx.slot_data["big_keyrings"]):
                if current_scene & 0xff00 != 0x1300:  # or self.location_name_to_id[data["location"]] in ctx.checked_locations:
                    print(f"Opening boss door for {hex(current_scene)}")
                    if await data["door"].read(ctx) != 0x5:
                        await data["door"].overwrite(ctx, 3)
                elif any([
                    current_scene == 0x1309 and self.location_name_to_id["ToS 10F Boss Key"] in ctx.checked_locations,
                    current_scene == 0x1318 and self.location_name_to_id["ToS 22F Boss Key"] in ctx.checked_locations
                ]):
                    await self.open_tos_boss_door(ctx, current_scene)
        else:
            self.boss_key_y, self.boss_key_read = None, None

        if current_scene == 0x700:
            snurglar_pointer = await STAddr.snurglar_pointer.read(ctx)

            snurglar_flags = Address.from_pointer(snurglar_pointer + 0xC0 - 0x2000000)
            self.snurglar_addr = snurglar_flags
            print(f"Got snurglar flags @ {snurglar_flags}")
            for color in ["Gold", "Purple", "Orange"]:
                self.watches[f"Snurglars {color} Key"] = snurglar_flags

            if self.item_count(ctx, "Mountain Temple Snurglar Key") >= 3 or self.item_count(ctx, "Snurglar Keyring"):
                if (not any([self.item_count(ctx, i) for i in ITEM_GROUPS["Tracks: Mountain Temple Tracks"]])
                        or not self.item_count(ctx, "Cannon")
                        or all([LOCATIONS_DATA[i]['id'] in ctx.checked_locations for i in LOCATION_GROUPS["Snurglars"]])):
                    print(f"Got Snurglar keys, opening mountain temple")
                    await self.snurglar_addr.overwrite(ctx, 0x30)
                else:
                    print(f"Got Snurglar keys, adding to main read list")
                    self.main_read_list.append(snurglar_flags)
        else:
            self.snurglar_addr = None

        if current_scene not in potion_location_lookup:
            treasure = None
            if ctx.slot_data["excess_random_treasure"] == 2:
                treasure = ITEM_MODEL_LOOKUP["Red Rupee"].value
            elif ctx.slot_data["excess_random_treasure"] == 0:
                treasure = ITEM_MODEL_LOOKUP["Nothing"].value
            await self.reset_treasure_models(ctx, treasure)

        if current_scene == 0x1c02 and self.current_entrance != 3:
            # Amazing that this works at all
            pointer = await STAddr.mtt_b1_heatoise_trigger_pointer.read(ctx)
            await Address.from_pointer(pointer+1384, 4).overwrite(ctx, 70000)


    @staticmethod
    async def open_tos_boss_door(ctx, scene):
        print(f"Opening ToS boss door")
        door_coords = BOSS_KEY_DATA[scene].get("door_coords", 0)
        if not door_coords:
            return
        pointer = await STAddr.tos_boss_door_pointer.read(ctx)
        object_pointer_table = await Address.from_pointer(pointer - 0x2000000, size=128).read(ctx, silent=True)
        test_pointer = 0
        for i in range(32):
            test_pointer = (object_pointer_table & (0xFFFFFF << 32*i)) >> 32*i
            # print(f"Test Pointer {hex(test_pointer)}")
            if not test_pointer:
                continue
            coords = await Address.from_pointer(test_pointer+4, size=12).read(ctx, silent=True)
            # print(f"Coords: {hex(coords)}")
            if coords == BOSS_KEY_DATA[scene].get("door_coords", 0):
                break

        boss_door = Address.from_pointer(test_pointer + 22)
        if await boss_door.read(ctx) != 5:
            await boss_door.overwrite(ctx, 3)

    async def process_train_speed(self, ctx, read_result):
        if self.current_stage in range(4, 0xb):
            if not hasattr(self, "train_speed_addr"):
                await self.set_train_speed(ctx)

            instant_switch = False
            if self.update_train_speed:
                await write_multiple(ctx, train_speed_addresses, self.train_speed)
                self.update_train_speed = False
                instant_switch = True

            current_gear = read_result[self.train_gear_addr]
            if current_gear != self.last_train_gear or instant_switch:
                self.last_train_gear = current_gear

                if self.train_quick_station and current_gear == 1:
                    train_action_addr = Address.from_pointer(self.train_speed_pointer+TRAIN_QUICK_STATION_OFFSET)
                    await train_action_addr.overwrite(ctx, 0x5c, silent=True)  # instant-enter station
                # Instant-set train speed
                if self.train_snap_speed and current_gear != 1:
                    await self.train_speed_addr.overwrite(ctx, self.train_speed[current_gear]*0x10, silent=True)


    def update_boss_warp(self, ctx, stage, scene_id):
        if scene_id in BOSS_WARP_SCENE_LOOKUP:  # Boss rooms
            reverse_exit = BOSS_WARP_SCENE_LOOKUP[scene_id]
            reverse_exit_id = self.entrances[reverse_exit].id
            pair = ctx.slot_data["er_pairings"].get(f"{reverse_exit_id}", self.entrances[reverse_exit].vanilla_reciprocal.id)
            if pair is None:
                print(f"Boss Entrance not Randomized")
                self.boss_warp_entrance = reverse_exit
            self.boss_warp_entrance = self.entrance_id_to_entrance[pair]
            print(f"Warp Stage: {stage}, current warp {self.boss_warp_entrance}")
            return self.boss_warp_entrance

        return None

    async def detect_boss_key(self, ctx):
        """Called each cycle while in a boss key room to detect a change in boss key position"""
        if self.boss_key_y is not None:
            bk_read = await self.boss_key_read.read(ctx, signed=True, silent=True)
            if (bk_read > self.boss_key_y + 10 and self.current_stage != 0x1c) or (self.current_stage == 0x1c and bk_read < self.boss_key_y):
                loc = BOSS_KEY_DATA[self.current_scene]["location"]
                await self._process_checked_locations(ctx, loc)
                print(f"Found boss key location {loc} {bk_read} >< {self.boss_key_y + 10} {hex(self.current_stage)}")
                await self.delete_boss_key(ctx)
                self.boss_key_y, self.boss_key_read = None, None


    async def delete_boss_key(self, ctx):
        pointer = await STAddr.boss_key_deletion_pointer.read(ctx)
        print(f"Deleting boss key @ {hex(pointer)}")
        size, offset = BOSS_KEY_DATA[self.current_scene].get("deletion_data", (12, 0))
        if self.current_stage == 0x1b:
            if not self.oct_bk_offset:
                data = BOSS_KEY_DATA[0x1b05]
                _, self.oct_bk_offset = await self.find_table_object(ctx, *data["search_data"], return_index=True)
                if not self.oct_bk_offset:
                    return
            pointer += (self.oct_bk_offset-2)*4  # Ocean temple bk does not load into the first slot in memory
            self.oct_bk_offset = None
            await Address.from_pointer(pointer+60, 4).overwrite(ctx, 0)  # also needs this to not crash
        if self.current_stage == 0x13:
            pointer, _ = await self.get_tos_bk_pointer(ctx)
        deletion_address = Address.from_pointer(pointer+offset, size)
        print(f"Deleting boss key @ {deletion_address} size {size}")
        # print(f"Deleting boss key @ {STAddr.boss_key_deletion}")
        await deletion_address.overwrite(ctx, 0)

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

        remove_wrong_stamps(wrong_stamp_indexes)
        add_missing_stamps(missing_stamps)
        await STAddr.stamp_ids.overwrite(ctx, stamps)
        has_stamps = [s for s in stamps if s != 255]
        stamp_count = len(has_stamps)

        print(f"Has {stamp_count} stamps: {stamps}")


    async def refill_ammo(self, ctx, text=""):
        await self.full_heal(ctx)
        bomb_prog = self.item_count(ctx, "Bombs (Progressive)")
        arrow_prog = self.item_count(ctx, "Bow (Progressive)")
        if bomb_prog:
            await STAddr.bomb_count.overwrite(ctx, self.item_data["Bombs (Progressive)"].give_ammo[bomb_prog-1])
        if arrow_prog:
            await STAddr.arrow_count.overwrite(ctx, self.item_data["Bow (Progressive)"].give_ammo[arrow_prog-1])
import math
import time
from typing import TYPE_CHECKING

import Utils
import worlds._bizhawk as bizhawk
from BaseClasses import ItemClassification
from NetUtils import ClientStatus
from worlds._bizhawk.client import BizHawkClient
from .battle_tower_data import BATTLE_TOWER_TIER_OFFSET, BATTLE_TOWER_TRAINER_OFFSET, BATTLE_TOWER_NUM_TRAINERS, \
    BATTLE_TOWER_NUM_TIERS
from .client_commands import register_commands
from .client_energy_link import ENERGY_LINK_NONE, handle_energy_link
from .client_tracker_events import BITFLAG_STORAGES, INVERTED_TRACKER_FLAGS
from .client_trap_link import handle_trap_link_setting, send_trap_link, resolve_trap_link_id
from .client_wonder_trade import WonderTradeMixin
from .client_event_sync import (E4_DOOR_SYNC_FLAG_MAP, E4_DOOR_SYNC_LAYOUT,
                                SYNC_GOAL_FLAGS, detect_sync_events, encode_sync_bitfield, apply_remote_sync_events,
                                detect_sync_goal_events, encode_sync_goal_bitfield)
from .data import data, load_json_data, is_flag_backed_warp
from .item_data import GRASS_OFFSET, POKEDEX_OFFSET, POKEDEX_COUNT_OFFSET, FLAG_ITEM_OFFSET, CANONICAL_ITEM_ID_MASK
from .items import item_const_name_to_id
from .options import ProvideShopHints, JohtoOnly, Goal
from .phone import PHONE_TRAP_COUNT
from .pokemon_data import ALL_UNOWN
from .rematch_trainer_data import REMATCH_TRAINER_LOCATION_BASE, NUM_REMATCH_TRAINER_LOCATIONS

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

EVENT_BYTES = math.ceil(max(data.event_flags.values()) / 8)
ENGINE_BYTES = math.ceil(max(data.engine_flags.values()) / 8)
DEX_BYTES = math.ceil(len(data.pokemon) / 8)
GRASS_BYTES = math.ceil(sum(len(tiles) for tiles in data.grass_tiles.values()) / 8)
TRADE_BYTES = math.ceil(len(data.trades) / 8)
SIGN_BYTES = math.ceil(len(data.unown_signs) / 8)
BATTLE_TOWER_TRAINER_BYTES = math.ceil(BATTLE_TOWER_NUM_TRAINERS / 8)
REMATCH_TRAINER_BYTES = math.ceil(NUM_REMATCH_TRAINER_LOCATIONS / 8)
NUM_FLYPOINTS = max(fly_region.spawn_flag for fly_region in data.fly_regions) + 1
FLYPOINT_BYTES = math.ceil(NUM_FLYPOINTS / 8)
FLYPOINT_MASK = (1 << NUM_FLYPOINTS) - 1
_WARP_IDS_JSON = load_json_data("warp_ids.json")
WARP_BYTES = _WARP_IDS_JSON["flag_bytes"]
WARP_ID_BY_BIT_POSITION = {w["bit_byte"] * 8 + w["bit_index"]: w["id"]
                           for w in _WARP_IDS_JSON["warps"] if is_flag_backed_warp(w)}
DEATH_LINK_MASK = 0b00010000
DEATH_LINK_SETTING_ADDR = data.ram_addresses["wArchipelagoOptions"] + 4
COUNT_ALL_POKEMON = len(data.pokemon)
BAG_POCKETS = {"ITEM": ("wNumItems", 2, "Items"), "BALL": ("wNumBalls", 2, "Balls"),
               "KEY_ITEM": ("wNumKeyItems", 1, "Key Items")}


HINT_FLAGS = {f"EVENT_SEEN_{mart_name}": [item.flag for item in mart_data.items if item.flag] for mart_name, mart_data
              in data.marts.items()}

HINT_FLAG_MAP = {data.event_flags[flag_name]: flag_name for flag_name in HINT_FLAGS.keys()}

SIGN_ID_TO_NAME = {sign.id: sign.name for sign in data.unown_signs.values()}
NUM_UNOWN = len(ALL_UNOWN)


class PokemonCrystalClient(WonderTradeMixin, BizHawkClient):
    game = data.manifest.game
    system = ("GB", "GBC")
    patch_suffix = ".apcrystal"

    local_checked_locations: set[int]
    goal_flags: list[int]
    local_set_events: dict[str, bool]
    local_set_events_2: dict[str, bool]
    local_set_events_3: dict[str, bool]
    local_set_static_events: dict[str, bool]
    local_set_rocket_trap_events: dict[str, bool]
    local_set_seen_kanto_mart_events: dict[str, bool]
    local_set_seen_johto_mart_events: dict[str, bool]
    local_found_key_items: dict[str, bool]
    local_seen_pokemon: set[int]
    local_caught_pokemon: set[int]
    local_hints: list[str]
    local_trades_completed: set[int]
    local_trades_finished: set[int]
    local_warps_visited: set[int]
    local_fly_unlocks: int
    local_battle_tower_tiers: set[int]
    phone_trap_locations: list[int]
    current_map: list[int]
    last_warp: int
    last_death_link: float
    grass_location_mapping: dict[str, int]
    trap_link_queue: list[int]
    notify_setup_complete: bool
    remote_seen_pokemon: set[int]
    remote_caught_pokemon: set[int]
    local_seen_signs: set[str]
    local_unown_dex: list[int]
    remote_unown_dex: list[int]
    local_sync_events: dict[str, bool]
    remote_sync_events: int
    local_e4_door_sync_events: dict[str, bool]
    remote_e4_door_sync_events: int
    local_sync_goal_events: dict[str, bool]
    remote_sync_goal_events: int
    local_unlocked_unowns: int
    remote_unlocked_unowns: int
    has_tracker_slot: bool
    commands_enabled: bool
    bag_full_warned_index: int | None

    def initialize_client(self) -> None:
        self.local_checked_locations = set()
        self.goal_flags = []
        for _, _, attr_name, _ in BITFLAG_STORAGES:
            setattr(self, attr_name, dict())
        self.local_seen_pokemon = set()
        self.local_caught_pokemon = set()
        self.local_hints = []
        self.local_trades_completed = set()
        self.local_trades_finished = set()
        self.local_warps_visited = set()
        self.local_fly_unlocks = 0
        self.local_battle_tower_tiers = set()
        self.phone_trap_locations = list()
        self.current_map = [0, 0]
        self.last_warp = 0
        self.last_death_link = 0
        self.grass_location_mapping = dict()
        self.trap_link_queue = list()
        self.notify_setup_complete = False
        self.remote_seen_pokemon = set()
        self.remote_caught_pokemon = set()
        self.local_seen_signs = set()
        self.local_unown_dex = list()
        self.remote_unown_dex = list()
        self.local_sync_events = dict()
        self.remote_sync_events = 0
        self.local_e4_door_sync_events = dict()
        self.remote_e4_door_sync_events = 0
        self.local_sync_goal_events = dict()
        self.remote_sync_goal_events = 0
        self.local_unlocked_unowns = 0
        self.remote_unlocked_unowns = 0
        self.has_tracker_slot = False
        self.sent_all_pokemon_seen = False
        self.commands_enabled = False
        self.bag_full_warned_index = None
        self.initialize_wonder_trade()

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        from CommonClient import logger

        try:

            # Check we're operating on a 2MB ROM
            if await bizhawk.get_memory_size(ctx.bizhawk_ctx, "ROM") != 2097152: return False

            # Check ROM name/patch version
            rom_info = ((await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_ROM_Header"], 11, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Version"], 2, "ROM"),
                                                              (data.rom_addresses["AP_ROM_Revision"], 1, "ROM"),
                                                              (data.rom_addresses["AP_Setting_RemoteItems"], 1, "ROM"),
                                                              (data.rom_addresses["AP_Version"], 32, "ROM")
                                                              ])))

            rom_name = bytes([byte for byte in rom_info[0] if byte != 0]).decode("ascii")
            rom_version = int.from_bytes(rom_info[1], "little")
            rom_revision = int.from_bytes(rom_info[2], "little")
            remote_items = int.from_bytes(rom_info[3], "little")

            if rom_name == "PM_CRYSTAL":
                logger.info("ERROR: You appear to be running an unpatched version of Pokemon Crystal. "
                            "You need to generate a patch file and use it to create a patched ROM.")
                return False
            if rom_name != "AP_CRYSTAL":
                return False

            required_rom_version = data.rom_version if rom_revision == 0 else data.rom_version_11
            if rom_version != required_rom_version:
                try:
                    generator_apworld_version = bytes([byte for byte in rom_info[4] if byte != 0]).decode("ascii")
                except UnicodeDecodeError:
                    generator_apworld_version = None

                if not generator_apworld_version:
                    generator_apworld_version = "too old to know"
                generator_version = "{0:x}".format(rom_version)
                client_version = "{0:x}".format(required_rom_version)
                logger.info("ERROR: The patch file used to create this ROM is not compatible with "
                            "this client. Double check your version of pokemon_crystal.apworld "
                            "against the version used to generate this game.")
                logger.info(f"Client APWorld version: {data.manifest.world_version}, "
                            f"Generator APWorld version: {generator_apworld_version}")
                logger.info(f"ROM Revision: V1.{rom_revision}, Client checksum: {client_version}, "
                            f"Generator checksum: {generator_version}")
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False  # Should verify on the next pass

        ctx.game = self.game
        ctx.items_handling = 0b011 if remote_items else 0b001
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125

        self.initialize_client()

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        import base64
        auth_raw = (await bizhawk.read(ctx.bizhawk_ctx, [(data.rom_addresses["AP_Seed_Auth"], 16, "ROM")]))[0]
        ctx.auth = base64.b64encode(auth_raw).decode("utf-8")

    async def warn_if_bag_full(self, ctx: "BizHawkClientContext", num_received_items: int,
                               overworld_guard: tuple) -> bool:
        from CommonClient import logger

        if num_received_items == self.bag_full_warned_index:
            return True
        self.bag_full_warned_index = None

        if num_received_items >= len(ctx.items_received):
            return True
        item = data.items.get(ctx.items_received[num_received_items].item & CANONICAL_ITEM_ID_MASK)
        if item is None or item.pocket not in BAG_POCKETS:
            return True

        count_label, entry_size, pocket_label = BAG_POCKETS[item.pocket]
        capacity = data.pocket_sizes[item.pocket]
        read_result = await bizhawk.guarded_read(
            ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemIndex"], 2, "WRAM"),
                              (data.ram_addresses[count_label], 1 + capacity * entry_size, "WRAM")], [overworld_guard])
        if read_result is None:
            return False
        if int.from_bytes(read_result[0], "little") != num_received_items:
            return True

        pocket = read_result[1]
        count = pocket[0]
        if count < capacity:
            return True
        entries = pocket[1:1 + count * entry_size]
        if entry_size == 1:
            fits = item.item_id in entries
        else:
            fits = any(entries[i] == item.item_id and entries[i + 1] < data.max_item_stack
                       for i in range(0, len(entries), 2))
        if not fits:
            logger.info(f"Your {pocket_label} pocket is full. {item.label} will be received once you make room.")
            self.bag_full_warned_index = num_received_items
        return True

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:

        if ctx.server is None or not ctx.server.socket.open or ctx.server.socket.closed or ctx.slot_data is None:
            return

        pokedex_seen_key = f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}"
        pokedex_caught_key = f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}"
        unown_dex_key = f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}"
        sync_events_key = f"pokemon_crystal_sync_events_{ctx.team}_{ctx.slot}"
        e4_door_sync_events_key = f"pokemon_crystal_e4_door_sync_events_{ctx.team}_{ctx.slot}"
        sync_goal_events_key = f"pokemon_crystal_sync_goal_events_{ctx.team}_{ctx.slot}"
        unlocked_unowns_key = f"pokemon_crystal_unlocked_unowns_{ctx.team}_{ctx.slot}"
        warps_key = f"pokemon_crystal_warps_{ctx.team}_{ctx.slot}"
        fly_unlocks_key = f"pokemon_crystal_fly_unlocks_{ctx.team}_{ctx.slot}"
        battle_tower_key = f"pokemon_crystal_battle_tower_{ctx.team}_{ctx.slot}"

        if not self.notify_setup_complete:
            if ctx.items_handling & 0b010:
                ctx.set_notify(pokedex_caught_key, pokedex_seen_key, unown_dex_key, sync_events_key,
                               e4_door_sync_events_key, sync_goal_events_key, unlocked_unowns_key, battle_tower_key,
                               fly_unlocks_key)
            ctx.set_notify(warps_key)
            ctx.set_notify(f"EnergyLink{ctx.team}")
            await bizhawk.write(ctx.bizhawk_ctx,
                                [(data.ram_addresses["wArchipelagoEnergyLinkStatus"],
                                  [ENERGY_LINK_NONE], "WRAM")])
            self.notify_setup_complete = True

        remote_warps = ctx.stored_data.get(warps_key)
        if remote_warps:
            self.local_warps_visited |= set(remote_warps)

        self.goal_flags = []
        goals = ctx.slot_data["goal"]
        if Goal.ELITE_FOUR in goals:
            self.goal_flags.append(data.event_flags["EVENT_BEAT_ELITE_FOUR"])
        if Goal.RED in goals:
            self.goal_flags.append(data.event_flags["EVENT_BEAT_RED"])
        if Goal.DIPLOMA in goals:
            self.goal_flags.append(data.event_flags["EVENT_OBTAINED_DIPLOMA"])
        if Goal.RIVAL in goals:
            self.goal_flags.extend([
                data.event_flags["EVENT_BEAT_CHERRYGROVE_RIVAL"],
                data.event_flags["EVENT_BEAT_AZALEA_RIVAL"],
                data.event_flags["EVENT_RIVAL_BURNED_TOWER"],
                data.event_flags["EVENT_BEAT_GOLDENROD_UNDERGROUND_RIVAL"],
                data.event_flags["EVENT_BEAT_VICTORY_ROAD_RIVAL"],
            ])
            if ctx.slot_data["johto_only"] == JohtoOnly.option_off:
                self.goal_flags.extend([
                    data.event_flags["EVENT_BEAT_RIVAL_IN_MT_MOON"],
                    data.event_flags["EVENT_BEAT_RIVAL_IN_INDIGO_PLATEAU"],
                ])
        if Goal.DEFEAT_TEAM_ROCKET in goals:
            self.goal_flags.extend([
                data.event_flags["EVENT_CLEARED_SLOWPOKE_WELL"],
                data.event_flags["EVENT_CLEARED_ROCKET_HIDEOUT"],
                data.event_flags["EVENT_BEAT_ROCKET_EXECUTIVEM_3"],
                data.event_flags["EVENT_CLEARED_RADIO_TOWER"],
            ])
            if ctx.slot_data["johto_only"] == JohtoOnly.option_off:
                self.goal_flags.append(data.event_flags["EVENT_DEFEATED_ROUTE_24_ROCKET"])
        if Goal.UNOWN_HUNT in goals:
            self.goal_flags.append(data.event_flags["EVENT_GOT_ALL_UNOWN"])
        if Goal.BATTLE_TOWER in goals:
            self.goal_flags.append(data.event_flags["EVENT_BEAT_ALL_BATTLE_TOWER_TIERS"])

        self.grass_location_mapping = ctx.slot_data["grass_location_mapping"]

        sync_e4_doors = (ctx.slot_data["lance_requires_elite_four"]
                         and "Pokemon League" in ctx.slot_data["randomize_entrances"])

        if not self.commands_enabled:
            self.commands_enabled = True
            register_commands(ctx)

        try:

            # all_pokemon_seen can be overridden at patch time, so report the ROM's value to the tracker
            if not self.sent_all_pokemon_seen:
                all_pokemon_seen = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(data.rom_addresses["AP_Setting_AllPokemonSeen_1"] + 1, 1, "ROM")]))[0][0]
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_all_pokemon_seen_{ctx.team}_{ctx.slot}",
                    "default": False,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": bool(all_pokemon_seen)}]
                }])
                self.sent_all_pokemon_seen = True

            # Scout the locations that can be hinted if provide hints is turned on
            if ctx.slot_data["provide_shop_hints"] != ProvideShopHints.option_off and ctx.locations_info == {}:
                hint_ids = []
                for locations in HINT_FLAGS.values():
                    hint_ids.extend(loc for loc in locations if loc in ctx.missing_locations)
                if hint_ids:
                    await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": hint_ids,
                        "create_as_hint": 0
                    }])

            overworld_guard = (data.ram_addresses["wArchipelagoSafeWrite"], [1], "WRAM")

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoItemReceived"], 7, "WRAM")], [overworld_guard])

            if read_result is None:  # Not in overworld
                return

            await handle_trap_link_setting(ctx, overworld_guard)

            await self.handle_wonder_trade(ctx)

            num_received_items = int.from_bytes([read_result[0][1], read_result[0][2]], "little")
            received_item_is_empty = read_result[0][0] == 0
            phone_trap_index = read_result[0][4]

            if not await self.warn_if_bag_full(ctx, num_received_items, overworld_guard):
                return

            max_items_per_pass = 32
            max_consume_polls = 8
            for _ in range(max_items_per_pass):
                if num_received_items < len(ctx.items_received) and received_item_is_empty:
                    next_item = ctx.items_received[num_received_items].item & CANONICAL_ITEM_ID_MASK
                    original_item = next_item

                    writes = []
                    if next_item >= FLAG_ITEM_OFFSET:
                        flag_item = next_item - FLAG_ITEM_OFFSET
                        next_item = item_const_name_to_id("FLAG_ITEM")
                        writes.append(
                            (data.ram_addresses["wArchipelagoFlagItemReceived"],
                             flag_item.to_bytes(1, "little"), "WRAM")
                        )

                    writes.append(
                        (data.ram_addresses["wArchipelagoItemReceived"],
                         next_item.to_bytes(1, "little"), "WRAM")
                    )

                    await bizhawk.write(ctx.bizhawk_ctx, writes)
                    await send_trap_link(ctx, original_item)
                elif self.trap_link_queue and not read_result[0][6]:
                    trap_id = self.trap_link_queue.pop(0) - FLAG_ITEM_OFFSET
                    await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoTrapReceived"],
                                                           trap_id.to_bytes(1, "little"), "WRAM")])
                else:
                    break

                for _ in range(max_consume_polls):
                    read_result = await bizhawk.guarded_read(
                        ctx.bizhawk_ctx,
                        [(data.ram_addresses["wArchipelagoItemReceived"], 7, "WRAM")], [overworld_guard])
                    if read_result is None:  # Left overworld mid-drain
                        return
                    num_received_items = int.from_bytes([read_result[0][1], read_result[0][2]], "little")
                    received_item_is_empty = read_result[0][0] == 0
                    if received_item_is_empty and not read_result[0][6]:
                        break
                else:
                    break  # game stopped consuming; resume next tick

            read_result = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wEventFlags"], EVENT_BYTES, "WRAM"),  # Flags
                 (data.ram_addresses["wArchipelagoPokedexCaught"], DEX_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoPokedexSeen"], DEX_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoGrassFlags"], GRASS_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoTradeFlags"], TRADE_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoSignFlags"], SIGN_BYTES, "WRAM"),
                 (data.ram_addresses["wUnownDex"], NUM_UNOWN, "WRAM"),
                 (data.ram_addresses["wMapGroup"], 2, "WRAM"),
                 (data.ram_addresses["wStatusFlags"], 1, "WRAM"),
                 (data.ram_addresses["wArchipelagoTrackerSlot"], 1, "WRAM"),
                 (data.ram_addresses["wUnlockedUnowns"], 1, "WRAM"),
                 (data.ram_addresses["wWarpFlags"], WARP_BYTES, "WRAM"),
                 (data.ram_addresses["wVisitedSpawns"], FLYPOINT_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoBattleTowerCompletedTiers"], 2, "WRAM"),
                 (data.ram_addresses["wArchipelagoBattleTowerTrainerFlags"], BATTLE_TOWER_TRAINER_BYTES, "WRAM"),
                 (data.ram_addresses["wArchipelagoRematchTrainerFlags"], REMATCH_TRAINER_BYTES, "WRAM"),
                 (data.ram_addresses["wLastWarpID"], 2, "WRAM"),
                 (data.ram_addresses["wArchipelagoTradeCompletedFlags"], TRADE_BYTES, "WRAM"), ],
                [overworld_guard]
            )

            if read_result is None:
                return

            pokedex_caught_bytes = read_result[1]
            pokedex_seen_bytes = read_result[2]
            grass_cut_bytes = read_result[3]
            trade_bytes = read_result[4]
            sign_bytes = read_result[5]
            unown_dex_bytes = read_result[6]
            current_map_bytes = read_result[7]
            status_flags_bytes = read_result[8]
            tracker_slot_bytes = read_result[9]
            local_unlocked_unowns = read_result[10][0]
            warp_flag_bytes = read_result[11]
            visited_spawn_bytes = read_result[12]
            battle_tower_bytes = read_result[13]
            battle_tower_trainer_bytes = read_result[14]
            rematch_trainer_bytes = read_result[15]
            last_warp_bytes = read_result[16]
            trade_completed_bytes = read_result[17]

            local_checked_locations = set()
            bitflag_locals = {attr_name: {flag: False for flag in flag_list}
                              for flag_list, _, attr_name, _ in BITFLAG_STORAGES}
            remote_seen_pokemon = ctx.stored_data[pokedex_seen_key] if pokedex_seen_key in ctx.stored_data else None
            local_seen_pokemon = set(remote_seen_pokemon) if remote_seen_pokemon else set()
            remote_caught_pokemon = ctx.stored_data[
                pokedex_caught_key] if pokedex_caught_key in ctx.stored_data else None
            local_caught_pokemon = set(remote_caught_pokemon) if remote_caught_pokemon else set()
            local_hints = {flag_name: False for flag_name in HINT_FLAGS.keys()}
            local_trades_completed = set()
            local_trades_finished = set()

            has_pokedex = status_flags_bytes[0] & 1

            goal_flags_cleared = {flag: False for flag in self.goal_flags}

            flag_bytes = read_result[0]
            for byte_i, byte in enumerate(flag_bytes):
                for i in range(8):
                    location_id = byte_i * 8 + i
                    event_set = byte & (1 << i)
                    if event_set != 0:
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

                        if location_id in goal_flags_cleared:
                            goal_flags_cleared[location_id] = True

                        for _, flag_map, attr_name, _ in BITFLAG_STORAGES:
                            if location_id in flag_map:
                                bitflag_locals[attr_name][flag_map[location_id]] = True

                        if location_id in HINT_FLAG_MAP:
                            local_hints[HINT_FLAG_MAP[location_id]] = True

            if ctx.items_handling & 0b010:
                for index, event in enumerate(SYNC_GOAL_FLAGS):
                    if self.remote_sync_goal_events & (1 << index):
                        event_id = data.event_flags[event]
                        if event_id in goal_flags_cleared:
                            goal_flags_cleared[event_id] = True

            local_sync_events = detect_sync_events(flag_bytes)
            local_e4_door_sync_events = detect_sync_events(flag_bytes, E4_DOOR_SYNC_FLAG_MAP)

            for byte_i, byte in enumerate(pokedex_caught_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        dex_number = (byte_i * 8 + i) + 1
                        location_id = dex_number + POKEDEX_OFFSET
                        if location_id in ctx.server_locations and has_pokedex:
                            local_checked_locations.add(location_id)
                        local_caught_pokemon.add(dex_number)

            for byte_i, byte in enumerate(pokedex_seen_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        dex_number = (byte_i * 8 + i) + 1
                        local_seen_pokemon.add(dex_number)

            for byte_i, byte in enumerate(grass_cut_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        location_id = (byte_i * 8 + i) + GRASS_OFFSET
                        if str(location_id) in self.grass_location_mapping:
                            location_id = self.grass_location_mapping[str(location_id)]
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

            for byte_i, byte in enumerate(trade_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        local_trades_completed.add(byte_i * 8 + i)

            for byte_i, byte in enumerate(trade_completed_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        local_trades_finished.add(byte_i * 8 + i)

            for byte_i, byte in enumerate(battle_tower_trainer_bytes):
                if not byte:
                    continue
                for i in range(8):
                    if byte & (1 << i):
                        canonical_idx = byte_i * 8 + i
                        if canonical_idx >= BATTLE_TOWER_NUM_TRAINERS:
                            continue
                        location_id = BATTLE_TOWER_TRAINER_OFFSET + canonical_idx
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

            for byte_i, byte in enumerate(rematch_trainer_bytes):
                if not byte:
                    continue
                for i in range(8):
                    if byte & (1 << i):
                        canonical_idx = byte_i * 8 + i
                        if canonical_idx >= NUM_REMATCH_TRAINER_LOCATIONS:
                            continue
                        location_id = REMATCH_TRAINER_LOCATION_BASE + canonical_idx
                        if location_id in ctx.server_locations:
                            local_checked_locations.add(location_id)

            local_battle_tower_tiers = set()
            for tier_idx in range(BATTLE_TOWER_NUM_TIERS):
                if battle_tower_bytes[tier_idx >> 3] & (1 << (tier_idx & 7)):
                    local_battle_tower_tiers.add(tier_idx)
                    location_id = BATTLE_TOWER_TIER_OFFSET + tier_idx
                    if location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

            # Sync completed-tier progress across saves via DataStorage (works whether
            # battle_tower_sanity is on or off, since it doesn't depend on AP locations).
            if ctx.items_handling & 0b010:
                remote_battle_tower_tiers = set(ctx.stored_data.get(battle_tower_key) or [])
                missing = remote_battle_tower_tiers - local_battle_tower_tiers
                if missing:
                    masks_per_byte: dict[int, int] = {}
                    for tier_idx in missing:
                        byte_idx = tier_idx >> 3
                        masks_per_byte[byte_idx] = masks_per_byte.get(byte_idx, 0) | (1 << (tier_idx & 7))
                    bt_sync_writes = []
                    bt_sync_guards = []
                    for byte_idx, mask in masks_per_byte.items():
                        addr = data.ram_addresses["wArchipelagoBattleTowerCompletedTiers"] + byte_idx
                        byte = battle_tower_bytes[byte_idx]
                        bt_sync_writes.append((addr, [byte | mask], "WRAM"))
                        # Guard against the in-game updating this byte (e.g. a tier just
                        # got completed) between the read above and this write.
                        bt_sync_guards.append((addr, [byte], "WRAM"))
                    if await bizhawk.guarded_write(ctx.bizhawk_ctx, bt_sync_writes, bt_sync_guards):
                        local_battle_tower_tiers |= remote_battle_tower_tiers

            local_warps_visited = set(self.local_warps_visited)
            for byte_i, byte in enumerate(warp_flag_bytes):
                if not byte:
                    continue
                base = byte_i * 8
                for i in range(8):
                    if byte & (1 << i):
                        warp_id = WARP_ID_BY_BIT_POSITION.get(base + i)
                        if warp_id is not None:
                            local_warps_visited.add(warp_id)

            local_fly_unlocks = int.from_bytes(visited_spawn_bytes, "little") & FLYPOINT_MASK

            packages = []

            if local_seen_pokemon != self.local_seen_pokemon:
                packages.append({
                    "cmd": "Set",
                    "key": pokedex_seen_key,
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update", "value": list(local_seen_pokemon)}, ]
                })

            if local_caught_pokemon != self.local_caught_pokemon:
                packages.append({
                    "cmd": "Set",
                    "key": pokedex_caught_key,
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update" if ctx.items_handling & 0b010 else "replace",
                                    "value": list(local_caught_pokemon)}, ]
                })

            if local_trades_completed != self.local_trades_completed:
                packages.append({
                    "cmd": "Set",
                    "key": f"pokemon_crystal_trades_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": list(local_trades_completed)}, ]
                })

            if local_trades_finished != self.local_trades_finished:
                packages.append({
                    "cmd": "Set",
                    "key": f"pokemon_crystal_trades_finished_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": list(local_trades_finished)}, ]
                })

            if local_warps_visited != self.local_warps_visited:
                packages.append({
                    "cmd": "Set",
                    "key": warps_key,
                    "default": [],
                    "want_reply": False,
                    "operations": [{"operation": "update", "value": list(local_warps_visited)}, ]
                })

            if local_fly_unlocks != self.local_fly_unlocks:
                packages.append({
                    "cmd": "Set",
                    "key": fly_unlocks_key,
                    "default": 0,
                    "want_reply": False,
                    "operations": [{"operation": "or", "value": local_fly_unlocks}, ]
                })

            if local_battle_tower_tiers != self.local_battle_tower_tiers:
                packages.append({
                    "cmd": "Set",
                    "key": battle_tower_key,
                    "default": [],
                    "want_reply": bool(ctx.items_handling & 0b010),
                    "operations": [{"operation": "update", "value": list(local_battle_tower_tiers)}, ]
                })

            if packages:
                await ctx.send_msgs(packages)

                self.local_seen_pokemon = local_seen_pokemon
                self.local_caught_pokemon = local_caught_pokemon
                self.local_trades_completed = local_trades_completed
                self.local_trades_finished = local_trades_finished
                self.local_warps_visited = local_warps_visited
                self.local_fly_unlocks = local_fly_unlocks
                self.local_battle_tower_tiers = local_battle_tower_tiers

            if ctx.slot_data["dexcountsanity_counts"] and has_pokedex:
                dex_count = len(local_caught_pokemon)
                check_counts = ctx.slot_data["dexcountsanity_counts"]

                for count in check_counts[:-1]:
                    location_id = count + POKEDEX_COUNT_OFFSET
                    if dex_count >= count and location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

                if dex_count >= check_counts[-1]:
                    location_id = COUNT_ALL_POKEMON + POKEDEX_COUNT_OFFSET
                    if location_id in ctx.server_locations:
                        local_checked_locations.add(location_id)

            if local_checked_locations != self.local_checked_locations:
                if "trap_locations" in ctx.slot_data:
                    for location in local_checked_locations - self.local_checked_locations:
                        if location not in ctx.checked_locations:
                            if str(location) in ctx.slot_data["trap_locations"]:
                                await send_trap_link(ctx, ctx.slot_data["trap_locations"][str(location)])

                self.local_checked_locations = local_checked_locations

            unacked_locations = local_checked_locations - ctx.checked_locations
            if unacked_locations:
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": list(unacked_locations)
                }])

            # Send game clear
            if not ctx.finished_game and all(goal_flags_cleared.values()):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
                ctx.finished_game = True

            if not self.phone_trap_locations:
                phone_result = await bizhawk.guarded_read(
                    ctx.bizhawk_ctx,
                    [(data.rom_addresses["AP_Setting_Phone_Trap_Locations"], PHONE_TRAP_COUNT * 2, "ROM")],
                    [overworld_guard]
                )
                if phone_result is not None:
                    read_locations = []
                    for i in range(0, PHONE_TRAP_COUNT):
                        loc = int.from_bytes(phone_result[0][i * 2:(i + 1) * 2], "little")
                        read_locations.append(loc)
                    self.phone_trap_locations = read_locations
            else:
                hint_locations = [location for location in self.phone_trap_locations[:phone_trap_index] if
                                  location != 0
                                  and location not in ctx.locations_scouted
                                  and location not in local_checked_locations
                                  and location not in ctx.checked_locations]
                if hint_locations:
                    ctx.locations_scouted.update(hint_locations)
                    await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": hint_locations,
                        "create_as_hint": 2
                    }])

            for flag_list, _, attr_name, key_suffix in BITFLAG_STORAGES:
                local_dict = bitflag_locals[attr_name]
                if local_dict != getattr(self, attr_name) and ctx.slot is not None:
                    bitfield = 0
                    for i, flag_name in enumerate(flag_list):
                        flag_set = local_dict[flag_name]
                        if flag_name in INVERTED_TRACKER_FLAGS:
                            flag_set = not flag_set
                        if flag_set:
                            bitfield |= 1 << i
                    await ctx.send_msgs([{
                        "cmd": "Set",
                        "key": f"pokemon_crystal_{key_suffix}_{ctx.team}_{ctx.slot}",
                        "default": 0,
                        "want_reply": False,
                        "operations": [{"operation": "or", "value": bitfield}],
                    }])
                    setattr(self, attr_name, local_dict)

            if local_sync_events != self.local_sync_events and ctx.items_handling & 0b010:
                event_bitfield = encode_sync_bitfield(local_sync_events)

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": sync_events_key,
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "or", "value": event_bitfield}],
                }])
                self.local_sync_events = local_sync_events

            if (sync_e4_doors and local_e4_door_sync_events != self.local_e4_door_sync_events
                    and ctx.items_handling & 0b010):
                e4_door_bitfield = encode_sync_bitfield(local_e4_door_sync_events, E4_DOOR_SYNC_LAYOUT)

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": e4_door_sync_events_key,
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "or", "value": e4_door_bitfield}],
                }])
                self.local_e4_door_sync_events = local_e4_door_sync_events

            local_sync_goal_events = detect_sync_goal_events(flag_bytes)
            if local_sync_goal_events != self.local_sync_goal_events and ctx.items_handling & 0b010:
                goal_bitfield = encode_sync_goal_bitfield(local_sync_goal_events)

                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": sync_goal_events_key,
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "or", "value": goal_bitfield}],
                }])
                self.local_sync_goal_events = local_sync_goal_events

            if local_unlocked_unowns != self.local_unlocked_unowns and ctx.items_handling & 0b010:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": unlocked_unowns_key,
                    "default": 0,
                    "want_reply": True,
                    "operations": [{"operation": "or", "value": local_unlocked_unowns}],
                }])
                self.local_unlocked_unowns = local_unlocked_unowns

            provide_shop_hints = ctx.slot_data["provide_shop_hints"]
            if provide_shop_hints != ProvideShopHints.option_off:
                hints_locations = []
                for flag, locations in HINT_FLAGS.items():
                    if local_hints[flag] and flag not in self.local_hints:
                        hints_locations.extend(locations)
                        self.local_hints.append(flag)

                if hints_locations:

                    if provide_shop_hints == ProvideShopHints.option_progression:
                        item_flag_mask = ItemClassification.progression
                    elif provide_shop_hints == ProvideShopHints.option_progression_and_useful:
                        item_flag_mask = ItemClassification.progression | ItemClassification.useful
                    else:
                        item_flag_mask = 0

                    hint_ids = []
                    for location_id in hints_locations:
                        if (location_id not in ctx.missing_locations
                                or location_id in self.local_checked_locations
                                or location_id not in ctx.locations_info):
                            continue
                        if not item_flag_mask or (ctx.locations_info[location_id].flags & item_flag_mask):
                            hint_ids.append(location_id)

                    if hint_ids:
                        await ctx.send_msgs([{
                            "cmd": "LocationScouts",
                            "locations": hint_ids,
                            "create_as_hint": 2
                        }])

            local_seen_signs = set()

            for byte_i, byte in enumerate(sign_bytes):
                for i in range(8):
                    if byte & (1 << i):
                        sign_id = (byte_i * 8 + i)
                        sign_name = SIGN_ID_TO_NAME[sign_id]
                        local_seen_signs.add(sign_name)

            if local_seen_signs != self.local_seen_signs:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_signs_{ctx.team}_{ctx.slot}",
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update", "value": list(local_seen_signs)}, ]
                }])
                self.local_seen_signs = local_seen_signs

            local_unown_dex = list(self.remote_unown_dex)
            for unown in unown_dex_bytes:
                if unown and unown not in local_unown_dex:
                    local_unown_dex.append(unown)

            if local_unown_dex != self.local_unown_dex:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": unown_dex_key,
                    "default": [],
                    "want_reply": ctx.items_handling & 0b010,
                    "operations": [{"operation": "update" if ctx.items_handling & 0b010 else "replace",
                                    "value": local_unown_dex}, ]
                }])
                self.local_unown_dex = local_unown_dex

            await self.handle_death_link(ctx, overworld_guard)

            await handle_energy_link(ctx, overworld_guard)

            if tracker_slot_bytes[0] and not self.has_tracker_slot:
                await ctx.send_msgs([{
                    "cmd": "Set",
                    "key": f"pokemon_crystal_tracker_slots_enabled_{ctx.team}_{ctx.slot}",
                    "default": False,
                    "want_reply": False,
                    "operations": [{"operation": "replace", "value": True}]
                }])
                self.has_tracker_slot = True

            current_map = [int(x) for x in current_map_bytes]
            last_warp = int.from_bytes(last_warp_bytes, "little")
            map_changed = self.current_map != current_map
            warp_changed = self.last_warp != last_warp
            if map_changed or warp_changed:
                tracker_slot = tracker_slot_bytes[0]
                self.current_map = current_map
                self.last_warp = last_warp
                # A map connection moves the player without a warp: map keys only.
                bounce_data = {f"mapGroup_{tracker_slot}": current_map[0],
                               f"mapNumber_{tracker_slot}": current_map[1]}
                if warp_changed:
                    bounce_data[f"lastWarp_{tracker_slot}"] = last_warp
                await ctx.send_msgs([{"cmd": "Bounce", "slots": [ctx.slot], "data": bounce_data}])

            if ctx.items_handling & 0b010:

                seen_bytes = bytearray(DEX_BYTES)
                caught_bytes = bytearray(DEX_BYTES)

                for i in range(1, len(data.pokemon) + 1):
                    poke_index = i - 1
                    byte_index = math.floor(poke_index / 8)
                    if i in local_seen_pokemon:
                        seen_bytes[byte_index] = seen_bytes[byte_index] | (1 << (poke_index % 8))
                    if i in local_caught_pokemon:
                        caught_bytes[byte_index] = caught_bytes[byte_index] | (1 << (poke_index % 8))

                await bizhawk.guarded_write(
                    ctx.bizhawk_ctx,
                    [(data.ram_addresses["wArchipelagoPokedexSeen"], seen_bytes, "WRAM"),
                     (data.ram_addresses["wArchipelagoPokedexCaught"], caught_bytes, "WRAM"),
                     (data.ram_addresses["wUnownDex"], local_unown_dex, "WRAM"), ],
                    [(data.ram_addresses["wArchipelagoPokedexSeen"], pokedex_seen_bytes, "WRAM"),
                     (data.ram_addresses["wArchipelagoPokedexCaught"], pokedex_caught_bytes, "WRAM"),
                     (data.ram_addresses["wUnownDex"], unown_dex_bytes, "WRAM")]
                )

                synced_event_bytes = apply_remote_sync_events(flag_bytes, self.remote_sync_events)
                if sync_e4_doors:
                    synced_event_bytes = apply_remote_sync_events(synced_event_bytes, self.remote_e4_door_sync_events,
                                                                  E4_DOOR_SYNC_LAYOUT)

                sync_event_writes = []
                sync_event_guards = []

                base_event_address = data.ram_addresses["wEventFlags"]

                for byte_index, byte in enumerate(synced_event_bytes):
                    if flag_bytes[byte_index] != byte:
                        sync_event_writes.append((base_event_address + byte_index, [byte], "WRAM"))
                        sync_event_guards.append((base_event_address + byte_index, [flag_bytes[byte_index]], "WRAM"))

                merged_unlocked_unowns = self.remote_unlocked_unowns | local_unlocked_unowns
                if merged_unlocked_unowns != local_unlocked_unowns:
                    sync_event_writes.append((data.ram_addresses["wUnlockedUnowns"], [merged_unlocked_unowns], "WRAM"))
                    sync_event_guards.append((data.ram_addresses["wUnlockedUnowns"], [local_unlocked_unowns], "WRAM"))

                visited_spawns = int.from_bytes(visited_spawn_bytes, "little")
                merged_fly_unlocks = visited_spawns | ((ctx.stored_data.get(fly_unlocks_key) or 0) & FLYPOINT_MASK)
                if merged_fly_unlocks != visited_spawns:
                    sync_event_writes.append((data.ram_addresses["wVisitedSpawns"],
                                              merged_fly_unlocks.to_bytes(FLYPOINT_BYTES, "little"), "WRAM"))
                    sync_event_guards.append((data.ram_addresses["wVisitedSpawns"], visited_spawn_bytes, "WRAM"))

                if sync_event_writes:
                    await bizhawk.guarded_write(ctx.bizhawk_ctx, sync_event_writes, sync_event_guards)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def handle_death_link(self, ctx: "BizHawkClientContext", guard) -> None:

        death_link_setting_status = await bizhawk.guarded_read(
            ctx.bizhawk_ctx,
            [(DEATH_LINK_SETTING_ADDR, 1, "WRAM")],
            [guard]
        )

        if death_link_setting_status and death_link_setting_status[0][0] & DEATH_LINK_MASK:

            if "DeathLink" not in ctx.tags:
                await ctx.update_death_link(True)
                self.last_death_link = ctx.last_death_link
                await bizhawk.write(ctx.bizhawk_ctx,
                                    [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])

            death_link_status = await bizhawk.guarded_read(
                ctx.bizhawk_ctx,
                [(data.ram_addresses["wArchipelagoDeathLink"], 1, "WRAM")], [guard])

            if not death_link_status: return

            if death_link_status[0][0] == 1:
                await ctx.send_death(ctx.player_names[ctx.slot] + " is out of usable Pokémon! "
                                     + ctx.player_names[ctx.slot] + " whited out!")
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])
                self.last_death_link = time.time()
            elif death_link_status[0][0] == 3:
                await ctx.send_death(ctx.player_names[ctx.slot] + " failed to dodge the spinner!")
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [0], "WRAM")])
                self.last_death_link = time.time()
            elif ctx.last_death_link > self.last_death_link and not death_link_status[0][0]:
                await bizhawk.write(ctx.bizhawk_ctx, [(data.ram_addresses["wArchipelagoDeathLink"], [2], "WRAM")])
                self.last_death_link = ctx.last_death_link
            elif ctx.last_death_link > self.last_death_link and death_link_status[0][0] == 2:
                # drop deathlinks if we have one queued
                self.last_death_link = ctx.last_death_link

        elif "DeathLink" in ctx.tags:
            await ctx.update_death_link(False)
            self.last_death_link = 0

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        super().on_package(ctx, cmd, args)

        if cmd == "Connected":
            wonder_trade_key = f"pokemon_wonder_trades_{ctx.team}"
            Utils.async_start(ctx.send_msgs([
                {"cmd": "SetNotify", "keys": [wonder_trade_key]},
                {
                    "cmd": "Set",
                    "key": wonder_trade_key,
                    "default": {"_lock": 0},
                    "operations": [{"operation": "default", "value": None}],
                },
            ]))

        if cmd == "SetReply" and args.get("key", "") == f"pokemon_wonder_trades_{ctx.team}":
            self.latest_wonder_trade_reply = args
            self.wonder_trade_update_event.set()

        if cmd == "Bounced":
            trap_id = resolve_trap_link_id(ctx, args)
            if trap_id is not None:
                self.trap_link_queue.append(trap_id)

        elif cmd == "Retrieved":
            if ctx.items_handling & 0b010:
                if f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_caught_pokemon = args["keys"][f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}"]
                    self.remote_caught_pokemon = set(remote_caught_pokemon) if remote_caught_pokemon else set()
                if f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_seen_pokemon = args["keys"][f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}"]
                    self.remote_seen_pokemon = set(remote_seen_pokemon) if remote_seen_pokemon else set()
                if f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_unown_dex = args["keys"][f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}"]
                    self.remote_unown_dex = remote_unown_dex if remote_unown_dex else list()
                if f"pokemon_crystal_sync_events_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_sync_events = args["keys"][f"pokemon_crystal_sync_events_{ctx.team}_{ctx.slot}"]
                    self.remote_sync_events = remote_sync_events if remote_sync_events else 0
                if f"pokemon_crystal_e4_door_sync_events_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_e4_door_sync_events = args["keys"][f"pokemon_crystal_e4_door_sync_events_{ctx.team}_{ctx.slot}"]
                    self.remote_e4_door_sync_events = remote_e4_door_sync_events if remote_e4_door_sync_events else 0
                if f"pokemon_crystal_sync_goal_events_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_sync_goal_events = args["keys"][f"pokemon_crystal_sync_goal_events_{ctx.team}_{ctx.slot}"]
                    self.remote_sync_goal_events = remote_sync_goal_events if remote_sync_goal_events else 0
                if f"pokemon_crystal_unlocked_unowns_{ctx.team}_{ctx.slot}" in args["keys"]:
                    remote_unlocked_unowns = args["keys"][f"pokemon_crystal_unlocked_unowns_{ctx.team}_{ctx.slot}"]
                    self.remote_unlocked_unowns = remote_unlocked_unowns if remote_unlocked_unowns else 0

        elif cmd == "SetReply":
            if args["key"] == f"pokemon_crystal_caught_pokemon_{ctx.team}_{ctx.slot}":
                self.remote_caught_pokemon = set(args.get("value", []))
            elif args["key"] == f"pokemon_crystal_seen_pokemon_{ctx.team}_{ctx.slot}":
                self.remote_seen_pokemon = set(args.get("value", []))
            elif args["key"] == f"pokemon_crystal_unowns_{ctx.team}_{ctx.slot}":
                self.remote_unown_dex = args.get("value", [])
            elif args["key"] == f"pokemon_crystal_sync_events_{ctx.team}_{ctx.slot}":
                self.remote_sync_events = args.get("value", 0)
            elif args["key"] == f"pokemon_crystal_e4_door_sync_events_{ctx.team}_{ctx.slot}":
                self.remote_e4_door_sync_events = args.get("value", 0)
            elif args["key"] == f"pokemon_crystal_sync_goal_events_{ctx.team}_{ctx.slot}":
                self.remote_sync_goal_events = args.get("value", 0)
            elif args["key"] == f"pokemon_crystal_unlocked_unowns_{ctx.team}_{ctx.slot}":
                self.remote_unlocked_unowns = args.get("value", 0)

import time
from typing import TYPE_CHECKING, Set, Dict

from NetUtils import ClientStatus
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from . import LOCATIONS_DATA, ITEMS_DATA, OracleOfAgesGoal, OracleOfAgesEnforcePotionInShop
from .common.Util import build_item_id_to_name_dict, build_location_name_to_id_dict

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext

ROOM_ZELDA_ENDING = 0x05F1

ROM_ADDRS = {
    "game_identifier": (0x0134, 11, "ROM"),
    "slot_name": (0xFFFC0, 64, "ROM"),
}

RAM_ADDRS = {
    "game_state": (0xC2EE, 1, "System Bus"),
    "received_item_index": (0xC6A8, 2, "System Bus"),
    "received_item": (0xCBFB, 1, "System Bus"),
    "location_flags": (0xC600, 0x500, "System Bus"),
    "global_flags": (0xC6D0, 0x10, "System Bus"),

    "current_map_group": (0xCC2d, 1, "System Bus"),
    "current_map_id": (0xCC30, 1, "System Bus"),
    "is_dead": (0xCDD5, 1, "System Bus"),

    "total_collected_rupees":  (0xC627, 2, "System Bus"),
    "kill_count":  (0xC620, 2, "System Bus"),
}

EVENT_FLAGS = {
    # param1 : IsGlobal
    # param2 : if global, global id, otherwise room flag address
    # param3 : mask for room flag
    "Raft Unlocked": (True, 0x26),
    "Planted Scent Seed": (False, 0xC8AC, 0x80),
    "D6 North Wall Bombed": (False, 0xCA3A, 0x01),
    "D6 Torches Lit": (False, 0xCA43, 0x40),
    "Cured King Zora": (True, 0x27),
    "Cured Fairy": (True, 0x30),
    "Jabu Jabu Permission": (True, 0x31),
    "Saved Nayru": (True, 0x11),
    "Obtained Maku Seed": (True, 0x35),
}


GASHA_ADDRS = {

    "Nuun Highlands Gasha Spot": (0xc705, 0x00), # 0
    "Rolling Ridge (Present, East) Gasha Spot": (0xc72c, 0x01), # 1
    "Talus Peeks (Present) Gasha Spot": (0xc730, 0x02), # 2
    "Yoll Graveyard Gasha Spot": (0xc77b, 0x03), # 3
    "Fairies' Woods Gasha Spot": (0xc790, 0x04), # 4
    "Crescent Island East (Present) Gasha Spot": (0xc7ad, 0x05), # 5
    "Crescent Island West (Present) Gasha Spot": (0xc7cb, 0x06), # 6
    "Sea of Storms (Present) Gasha Spot": (0xc7d7, 0x07), # 7
    "Talus Peeks (Past) Gasha Spot": (0xc801, 0x08), # 8
    "Rolling Ridge (Past, Upper) Gasha Spot": (0xc80a, 0x09), # 9
    "Rolling Ridge (Past, West) Gasha Spot": (0xc828, 0x0a), # a
    "Deku Forest Gasha Spot": (0xc834, 0x0b), # b
    "Lynna Village Gasha Spot": (0xc855, 0x0c), # c
    "Southern Shore Gasha Spot": (0xc895, 0x0d), # d
    "Zora Vilage Gasha Spot": (0xc8d0, 0x0e), # e
    "Crescent Island West (Past) Gasha Spot": (0xc8ca, 0x0f), # f

}

def hexa_to_decimal(num) -> int:
    remaining = num
    powerOfTen = 0
    result = 0
    while (remaining != 0):
        currentDecimalNumber = (remaining & 0xf) * (pow(10,powerOfTen))
        result += currentDecimalNumber
        remaining = remaining >> 4
        powerOfTen += 1
    return result

class OracleOfAgesClient(BizHawkClient):
    game = "The Legend of Zelda - Oracle of Ages"
    system = "GBC"
    patch_suffix = ".apooa"
    local_checked_locations: Set[int]
    local_scouted_locations: Set[int]
    item_id_to_name: Dict[int, str]
    location_name_to_id: Dict[str, int]
    flags_values: Dict[str, bool]
    total_collected_rupees = 0
    kill_count = 0

    def __init__(self) -> None:
        super().__init__()
        self.item_id_to_name = build_item_id_to_name_dict(ITEMS_DATA)
        self.location_name_to_id = build_location_name_to_id_dict(LOCATIONS_DATA)
        self.local_checked_locations = set()
        self.local_scouted_locations = set()
        self.local_tracker = {}
        self.flags_values = {}
        self.set_deathlink = False
        self.last_deathlink = None
        self.was_alive_last_frame = False
        self.is_expecting_received_death = False

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        try:
            # Check ROM name/patch version
            rom_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["game_identifier"]]))[0]
            rom_name = bytes([byte for byte in rom_name_bytes if byte != 0]).decode("ascii")
            if rom_name != "ZELDA NAYRU":
                return False
        except UnicodeDecodeError:
            return False
        except bizhawk.RequestFailedError:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b101  # Remote items + starting inventory
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.5

        return True

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        slot_name_bytes = (await bizhawk.read(ctx.bizhawk_ctx, [ROM_ADDRS["slot_name"]]))[0]
        ctx.auth = bytes([byte for byte in slot_name_bytes if byte != 0]).decode("utf-8")
        pass

    def on_package(self, ctx, cmd, args):
        if cmd == 'Connected':
            if 'death_link' in args['slot_data']['options'] and args['slot_data']['options']['death_link']:
                self.set_deathlink = True
                self.last_deathlink = time.time()
        super().on_package(ctx, cmd, args)

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        if not ctx.server or not ctx.server.socket.open or ctx.server.socket.closed:
            return

        # Enable "DeathLink" tag if option was enabled
        if self.set_deathlink:
            self.set_deathlink = False
            await ctx.update_death_link(True)



        try:
            read_result = await bizhawk.read(ctx.bizhawk_ctx, [
                RAM_ADDRS["game_state"],            # Current state of game (is the player actually in-game?)
                RAM_ADDRS["received_item_index"],   # Number of received items
                RAM_ADDRS["received_item"],         # Received item still pending?
                RAM_ADDRS["location_flags"],        # Location flags
                RAM_ADDRS["global_flags"],          # global flags
                RAM_ADDRS["current_map_group"],     # Current map group & id where the player is currently located
                RAM_ADDRS["current_map_id"],        # ^^^
                RAM_ADDRS["is_dead"],
                RAM_ADDRS["total_collected_rupees"],
                RAM_ADDRS["kill_count"]
            ])

            # If player is not in-game, don't do anything else
            if read_result is None or read_result[0][0] != 2:
                return

            num_received_items = int.from_bytes(read_result[1], "little")
            received_item_is_empty = (read_result[2][0] == 0)
            flag_bytes = read_result[3]
            global_bytes = read_result[4]
            current_room = (read_result[5][0] << 8) | read_result[6][0]
            is_dead = (read_result[7][0] != 0)
            hexa_total_rupee = int.from_bytes(read_result[8], "little")
            self.total_collected_rupees = hexa_to_decimal(hexa_total_rupee)
            self.kill_count = int.from_bytes(read_result[9], "little")

            await self.process_checked_locations(ctx, flag_bytes)
            await self.process_scouted_locations(ctx, flag_bytes)
            await self.process_event_flags(ctx, flag_bytes, global_bytes)
            await self.process_tracker_updates(ctx, flag_bytes, current_room)

            # Process received items (only if we aren't in Blaino's Gym to prevent him from calling us cheaters)
            if received_item_is_empty:
                await self.process_received_items(ctx, num_received_items)

            if not ctx.finished_game:
                await self.process_game_completion(ctx, flag_bytes, current_room)

            if "DeathLink" in ctx.tags:
                await self.process_deathlink(ctx, is_dead)

        except bizhawk.RequestFailedError:
            # Exit handler and return to main loop to reconnect
            pass

    async def process_checked_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        
        local_checked_locations = set(ctx.locations_checked)
        for name, location in LOCATIONS_DATA.items():
            if location["flag_byte"] is None:
                continue

            bytes_to_test = location["flag_byte"]

            if bytes_to_test == 0xFFFF:
                continue

            if not hasattr(bytes_to_test, "__len__"):
                bytes_to_test = [bytes_to_test]

            # Check all "flag_byte" to see if location has been checked
            for byte_addr in bytes_to_test:
                byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
                bit_mask = location["bit_mask"] if "bit_mask" in location else 0x20
                if flag_bytes[byte_offset] & bit_mask == bit_mask:
                    location_id = self.location_name_to_id[name]
                    local_checked_locations.add(location_id)
                    break

        
        # Check how many deterministic Gasha Nuts have been opened, and mark their matching locations as checked
        byte_offset = 0xC64C - RAM_ADDRS["location_flags"][0]
        gasha_counter = flag_bytes[byte_offset] >> 2
        for i in range(gasha_counter):
            name = f"Gasha Nut #{i + 1}"
            location_id = self.location_name_to_id[name]
            local_checked_locations.add(location_id)

        # Send locations
        if self.local_checked_locations != local_checked_locations:
            self.local_checked_locations = local_checked_locations
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": list(self.local_checked_locations)
            }])

    async def process_scouted_locations(self, ctx: "BizHawkClientContext", flag_bytes):
        
        if ctx.slot_data is not None:
            local_scouted_locations = set(ctx.locations_scouted)
            for name, location in LOCATIONS_DATA.items():
                if "scouting_byte" not in location or location["scouting_byte"] == 0xFFFF :
                    continue

                if name == "Lynna City: Shop Item #3":
                    if ctx.slot_data["options"]["enforce_potion_in_shop"] == OracleOfAgesEnforcePotionInShop.option_lynna_shop:
                        continue

                if name == "Yoll Graveyard: Syrup Shop Item #3":
                    if  ctx.slot_data["options"]["enforce_potion_in_shop"] == OracleOfAgesEnforcePotionInShop.option_syrup_hut:
                        continue


                # Check "scouting_byte" to see if map has been visited for scoutable locations
                byte_to_test = location["scouting_byte"]
                byte_offset = byte_to_test - RAM_ADDRS["location_flags"][0]
                bit_mask = location["scouting_mask"] if "scouting_mask" in location else 0x10
                if flag_bytes[byte_offset] & bit_mask == bit_mask:
                    # Map has been visited, scout the location if it hasn't been already
                    location_id = self.location_name_to_id[name]
                    local_scouted_locations.add(location_id)

            if self.local_scouted_locations != local_scouted_locations:
                self.local_scouted_locations = local_scouted_locations
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": list(self.local_scouted_locations),
                    "create_as_hint": int(2)
                }])
        
    
    async def process_event_flags(self, ctx: "BizHawkClientContext", flag_bytes, global_bytes):
        for flagname, data in EVENT_FLAGS.items():
            if (data[0]): # is global flag
                addr = data[1] >> 3
                flag = 1 << (data[1] & 0x7)
                self.flags_values[flagname] = global_bytes[addr] & flag != 0
            else:
                addr = data[1] - RAM_ADDRS["location_flags"][0]
                flag = data[2]
                self.flags_values[flagname] = flag_bytes[addr] & flag == flag

        

    async def process_received_items(self, ctx: "BizHawkClientContext", num_received_items: int):
        # If the game hasn't received all items yet and the received item struct doesn't contain an item, then
        # fill it with the next item
        if num_received_items < len(ctx.items_received):
            next_item_name = self.item_id_to_name[ctx.items_received[num_received_items].item]
            await bizhawk.write(ctx.bizhawk_ctx, [(0xCBFB, [
                ITEMS_DATA[next_item_name]["id"],
                ITEMS_DATA[next_item_name]["subid"] if "subid" in ITEMS_DATA[next_item_name] else 0
            ], "System Bus")])

    async def process_game_completion(self, ctx: "BizHawkClientContext", flag_bytes, current_room: int):
        game_clear = False
        if ctx.slot_data is not None:
            if ctx.slot_data['options']["goal"] == OracleOfAgesGoal.option_beat_veran:
                veran_flag_offset = 0xC6D8 - RAM_ADDRS["location_flags"][0]
                veran_was_beaten = (flag_bytes[veran_flag_offset] & 0x80 == 0x80)
                game_clear = veran_was_beaten
            elif ctx.slot_data['options']["goal"] == OracleOfAgesGoal.option_beat_ganon:
                # Room with Zelda lying down was reached, and Ganon was beaten
                ganon_flag_offset = 0xCAF1 - RAM_ADDRS["location_flags"][0]
                ganon_was_beaten = (flag_bytes[ganon_flag_offset] & 0x80 == 0x80)
                game_clear = (current_room == ROOM_ZELDA_ENDING) and ganon_was_beaten
        if game_clear:
            await ctx.send_msgs([{
                "cmd": "StatusUpdate",
                "status": ClientStatus.CLIENT_GOAL
            }])

    async def process_deathlink(self, ctx: "BizHawkClientContext", is_dead):
        if ctx.last_death_link > self.last_deathlink and not is_dead:
            # A death was received from another player, make our player die as well
            await bizhawk.write(ctx.bizhawk_ctx, [(RAM_ADDRS["received_item"][0], [0xFF], "System Bus")])
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
                await ctx.send_death(ctx.player_names[ctx.slot] + " might not be the Hero of Time after all.")
                self.last_deathlink = ctx.last_death_link

    async def process_tracker_updates(self, ctx: "BizHawkClientContext", flag_bytes: bytes, current_room: int):
        # Processes the gasha tracking
        local_tracker = dict(self.local_tracker)

        # Gasha handling
        byte_offset = 0xC64d - RAM_ADDRS["location_flags"][0]
        gasha_seed_bytes = flag_bytes[byte_offset] + flag_bytes[byte_offset + 1] * 0x100
        for gasha_name, data in GASHA_ADDRS.items():
            (byte_addr, flag) = data

            # Check if the seed has been harvested
            flag_mask = 0x01 << flag
            byte_offset = byte_addr - RAM_ADDRS["location_flags"][0]
            local_tracker[f"Planted {gasha_name}"] = (gasha_seed_bytes & flag_mask) != 0
            local_tracker[f"Harvested {gasha_name}"] = (flag_bytes[byte_offset] & 0x20) != 0

        # Position tracking
        local_tracker["Current Room"] = current_room
        local_tracker["Total Collected Rupee"] = self.total_collected_rupees
        local_tracker["Kill Count"] = self.kill_count

        for event, data in self.flags_values.items():
            local_tracker[event] = data

        # Wild seed/bomb tracking
        wild_item_data = [
            (0x03, "Bombs"),
            (0x20, "Ember"),
            (0x21, "Scent"),
            (0x22, "Pegasus"),
            (0x23, "Gale"),
            (0x24, "Mystery"),
        ]
        base_offset = 0xc69a - RAM_ADDRS["location_flags"][0]
        for item_id, item_name in wild_item_data:
            byte_offset = base_offset + item_id // 8
            mask = 0x01 << item_id % 8
            if flag_bytes[byte_offset] & mask:
                local_tracker[f"Obtained {item_name}"] = True

        # May get to event tracking once I figure out the event flags for what's shown on the poptracker pack.

        updates = {}
        for key, value in local_tracker.items():
            if key not in self.local_tracker or self.local_tracker[key] != value:
                updates[key] = value

        await self.send_bounce_cmd(ctx, updates, "Current Room")
        await self.send_bounce_cmd(ctx, updates, "Total Collected Rupee")
        await self.send_bounce_cmd(ctx, updates, "Kill Count")

        if len(updates) > 0:
            await ctx.send_msgs([{
                "cmd": "Set",
                "key": f"OoA_{ctx.team}_{ctx.slot}",
                "default": {},
                "operations": [{
                    "operation": "update",
                    "value": updates
                }],
            }])

        self.local_tracker = local_tracker

    async def send_bounce_cmd(self, ctx: "BizHawkClientContext", updates: dict, key: str):
        if key in updates:
            await ctx.send_msgs([{
                "cmd": "Bounce",
                "slots": [ctx.slot],
                "data": {
                    key: updates[key]
                }
            }])
            del updates[key]
        
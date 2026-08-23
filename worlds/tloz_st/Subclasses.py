
from .DSZeldaClient.subclasses import DSTransition
from .DSZeldaClient.ItemClass import DSItem, receive_normal, remove_vanilla_normal, receive_small_key, remove_vanilla_progressive
from enum import IntEnum
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from .Client import SpiritTracksClient
from .data.Addresses import STAddr

async def receive_tos_key(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    key_count = item.value if item.name.startswith("Keyring") else 1

    async def write_keys_to_storage(dungeon) -> tuple[int, list, str] or False:
        from .data.Constants import DUNGEON_KEY_DATA
        key_data = DUNGEON_KEY_DATA.get(dungeon, {})
        if not key_data:
            return False
        prev = await key_data["address"].read(ctx)
        bit_filter = key_data["filter"]
        new_v = prev | bit_filter \
            if (prev & bit_filter) + (key_data["value"]*key_count) > bit_filter \
            else prev + (key_data["value"]*key_count)
        print(f"Writing {key_data['name']} key to storage: {hex(prev)} -> {hex(new_v)}")
        return key_data["address"].get_inner_write_list(new_v)

    res = []
    if client.current_stage == item.dungeon and client.current_room in item.rooms:
        print("Getting ToS key in correct section")
        if client.last_vanilla_item and client.last_vanilla_item[-1] == "Small Key (ToS)":
            if key_count > 1:
                await client.key_address.add(ctx, key_count-1)
            client.last_vanilla_item.pop()
        else:
            await client.key_address.add(ctx, key_count)
    else:
        dungeon_key = 0x130 + item.section
        storage_data = await write_keys_to_storage(dungeon_key)
        if storage_data:
            res.append(storage_data)
    return res

async def receive_tear_of_light(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    if client.current_stage == 0x13 and ctx.slot_data["randomize_tears"] != -1:  # avoid calcing tears when vanilla
        await client.set_tears(ctx)

    return []

async def receive_potion(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    empty_slots = [addr for addr, prev in zip([STAddr.potion_0, STAddr.potion_1], client.potion_tracker) if prev == 0]
    print(f"\tGetting potion {item.name} {empty_slots}")
    if not empty_slots:
        overflow_item = client.item_data[item.overflow_item]
        return await receive_normal(client, ctx, overflow_item, rii)
    await empty_slots[0].overwrite(ctx, item.value)
    await client.update_potion_tracker(ctx, "receive_potion")
    return []

async def remove_treasure(client, ctx, item, rii):
    addr = item.address
    value = client.treasure_tracker[addr]
    print(f"Removing treasure {item}")
    return addr.get_write_list(value)

async def remove_tear_of_light(client, ctx, item: "STItem", rii):
    if ctx.slot_data["randomize_tears"] == -1:
        return []
    await client.set_tears(ctx)
    return []

async def remove_potion(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    empty_slots = [addr for addr, prev in zip([STAddr.potion_0, STAddr.potion_1], client.potion_tracker) if prev == 0]
    if not empty_slots:
        overflow_item = client.item_data[item.overflow_item]
        return await remove_vanilla_normal(client, ctx, overflow_item, rii)
    # Remove potion
    await empty_slots[0].overwrite(ctx, 0)
    await client.update_potion_tracker(ctx, "remove_vanilla")
    return []

async def remove_passenger(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    if ctx.slot_data["randomize_passengers"] == 1:
        return []
    prev_value = await item.address.read(ctx)
    res = [
        STAddr.has_passenger_0.get_inner_write_list(0xFFFFFFFF),
        STAddr.has_passenger_1.get_inner_write_list(0xFFFFFFFF),
        STAddr.passenger_tag_0.get_inner_write_list(0),
        STAddr.passenger_tag_1.get_inner_write_list(0),
        STAddr.passenger_goal.get_inner_write_list(0xFFFFFFFF),
        item.address.get_inner_write_list(item.value & prev_value)  # Write the passenger flag
    ]
    return res

async def remove_vanilla_tracks(client: "SpiritTracksClient", ctx, item: "STItem", num_received_items: int):
    group_name = f"Tracks: {item.name}"
    print(f"Group names: {group_name} | {group_name[:len(group_name)-7]}")
    group = client.item_groups.get(group_name, client.item_groups.get(group_name[:len(group_name)-7], []))
    print(f"\tgroup: {group}")
    for track in group:
        if client.item_count(ctx, track):
            return []
    print(f"Didn't have track")
    prev = await item.address.read(ctx, silent=True)
    return item.address.get_write_list(prev & (~item.value))

async def remove_cargo(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    if ctx.slot_data["randomize_cargo"] == 1:
        return []
    res = [
        STAddr.cargo_0.get_inner_write_list(0xFFFFFFFF),
        STAddr.cargo_1.get_inner_write_list(0xFFFFFFFF),
        STAddr.cargo_count_0.get_inner_write_list(0),
        STAddr.cargo_count_1.get_inner_write_list(0),
    ]
    return res

async def handle_stamps(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    await client.update_stamps(ctx)
    return []

async def remove_vanilla_bow(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    bow_item = client.item_data["Bow (Progressive)"]
    return await remove_vanilla_progressive(client, ctx, bow_item, rii)

async def remove_vanilla_bow_of_light(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    if not ctx.slot_data["spirit_weapons"]:
        return await remove_vanilla_normal(client, ctx, item, rii)
    if any([
        client.item_count(ctx, "Tear of Light (All Sections)") >= 6,
        client.item_count(ctx, "Tear of Light (Progressive)") >= 16,
        client.item_count(ctx, "Big Tear of Light (All Sections)") >= 2,
        client.item_count(ctx, "Big Tear of Light (Progressive)") >= 6]):
        return []
    return await remove_vanilla_normal(client, ctx, item, rii)

async def dummy(*args):
    print(f"Receiving dummy item")
    return []

class STItem(DSItem):
    rooms: list[int]
    section: int
    model: str = None
    progressive_model: list[str]
    vanilla_model: str = None
    all_item_groups: dict[str, set[str]]

    def __init__(self, name, data, all_items):
        super().__init__(name, data, all_items)

        self.vanilla_model = self.model if self.vanilla_model is None else self.vanilla_model

    def get_receive_function(self):
        res = super().get_receive_function()
        if self.name.startswith("Passenger:"):
            return dummy
        if "Tear of Light" in self.name:
            return receive_tear_of_light
        if self.name.startswith("Small Key (ToS") or self.name.startswith("Keyring (ToS"):
            return receive_tos_key
        if self.name.startswith("Keyring ("):
            return receive_small_key
        if "Potion" in self.name:
            return receive_potion
        if self.name.startswith("Stamp") and not self.name == "Stamp Book":
            return handle_stamps
        if res is None:
            return dummy
        return res

    def get_remove_vanilla_function(self):
        if "treasure" in self.tags:
            return remove_treasure
        if "Tear of Light" in self.name:
            return remove_tear_of_light
        if "Potion" in self.name:
            return remove_potion
        if self.name == "Dummy Bow":
            return remove_vanilla_bow
        if self.name == "Bow of Light":
            return remove_vanilla_bow_of_light
        if self.name == "Rabbit Net" or self.name in self.all_item_groups["Snurglar Key"]:
            return dummy
        if self.name.startswith("Passenger:"):
            return remove_passenger
        if self.name.startswith("Cargo:"):
            return remove_cargo
        if self.name.startswith("Stamp") and not self.name == "Stamp Book":
            return handle_stamps
        if self.name in self.all_item_groups["Basic Tracks"]:
            return remove_vanilla_tracks
        return super().get_remove_vanilla_function()

direction_lookup = {
    0: "none",
    1: "left",
    2: "right",
    3: "up",
    4: "down",
    5: "enter",
    6: "exit"}
type_lookup = {
    0: "plando",
    1: "house",
    2: "cave",
    3: "station",
    4: "overworld",
    5: "dungeon_entr",
    6: "boss",
    7: "dungeon_room",
    8: "warp",
    9: "portal",
    10: "event",
    11: "tos_section",
    12: "transition",
    13: "tos_room",
    14: "tos_lobby",
    15: "castle",
    16: "disorientation",
    17: "eote",
    18: "las"
}
dungeon_lookup = {
    0: "none",
    1: "tos_1",
    2: "tos_2",
    3: "tos_3",
    4: "tos_4",
    5: "tos_5",
    6: "tos_6",
    7: "wooded",
    8: "blizzard",
    9: "marine",
    10: "mountain",
    11: "desert"
}

dungeon_to_enum = {
    'ToS 1': 1,
    'ToS 2': 2,
    'ToS 3': 3,
    'ToS 4': 4,
    'ToS 5': 5,
    'ToS 6': 6,
    'Wooded Temple': 7,
    'Blizzard Temple': 8,
    'Marine Temple': 9,
    'Mountain Temple': 10,
    'Desert Temple': 11,
}

def decode_entrance_groups(group):
    direction = group & EntranceGroups.DIRECTION_MASK
    area = (group & EntranceGroups.AREA_MASK) >> 3
    dung = (group & EntranceGroups.DUNGEON_MASK) >> 8
    dung_text = ""
    if dung:
        dung_text = f"-{dungeon_lookup[dung]}"

    return f"{direction_lookup[direction]}-{type_lookup[area]}{dung_text}"

def decode_recursive(data):
    if isinstance(data, dict):
        return {decode_recursive(k): decode_recursive(v) for k, v in data.items()}
    elif isinstance(data, Iterable):
        return [decode_recursive(i) for i in data]
    elif isinstance(data, int):
        return decode_entrance_groups(data)
    return data


class EntranceGroups(IntEnum):
    NONE = 0
    # Directions
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    # Types
    HOUSE = 1 << 3
    CAVE = 2 << 3
    STATION = 3 << 3
    OVERWORLD = 4 << 3
    DUNGEON_ENTRANCE = 5 << 3
    BOSS = 6 << 3
    DUNGEON_ROOM = 7 << 3
    WARP_PORTAL = 8 << 3
    TRAIN_PORTAL = 9 << 3
    EVENT = 10 << 3
    TOS_SECTION = 11 << 3
    OVERWORLD_TRAIN = 12 << 3
    TOS_ROOM = 13 << 3
    TOS_LOBBY = 14 << 3
    CASTLE = 15 << 3
    DISORIENTATION = 16 << 3
    EOTE = 17 << 3
    LAS = 18 << 3

    # dungeons
    TOS_1 = 1 << 8
    TOS_2 = 2 << 8
    TOS_3 = 3 << 8
    TOS_4 = 4 << 8
    TOS_5 = 5 << 8
    TOS_6 = 6 << 8
    WOODED = 7 << 8
    BLIZZARD = 8 << 8
    MARINE = 9 << 8
    MOUNTAIN = 10 << 8
    DESERT = 11 << 8

    AREA_MASK = 0x1F << 3
    DIRECTION_MASK = 0x7
    DUNGEON_MASK = 0xF << 8
    NON_DUNGEON_MASK = 0xFF

    def __str__(self):
        return decode_entrance_groups(self.value)

OPPOSITE_ENTRANCE_GROUPS = {
    EntranceGroups.RIGHT: EntranceGroups.LEFT,
    EntranceGroups.LEFT: EntranceGroups.RIGHT,
    EntranceGroups.UP: EntranceGroups.DOWN,
    EntranceGroups.DOWN: EntranceGroups.UP,
    0: 0,
    EntranceGroups.NONE: EntranceGroups.NONE
}

# Entrance data format
class STTransition(DSTransition):
    entrance_groups = EntranceGroups
    opposite_entrance_groups = OPPOSITE_ENTRANCE_GROUPS
    required_groups: list[str | tuple[str]]
    vanilla_reciprocal: "STTransition"

    @classmethod
    def from_data(cls, entrance_data):
        res = dict()
        counter = {}
        ident = 0
        for name, data in entrance_data.items():
            data["id"] = ident
            res[name] = cls(name, data)
            # print(f"{i} {ENTRANCES[name].entrance_region} -> {ENTRANCES[name].exit_region}")
            ident += 1
            point = data["entrance_region"] + "<=>" + data["exit_region"]
            counter.setdefault(point, 0)
            counter[point] += 1
            if "one_way_data" in data:
                res[name].extra_data |= data["one_way_data"]

            if data.get("two_way", True):
                two_way = True
            else:
                two_way = False
            reverse_name = data.get("return_name", f"Unnamed Entrance {ident}")
            reverse_data = {
                "entrance_region": data.get("reverse_exit_region", data["exit_region"]),
                "exit_region": data.get("reverse_entrance_region", data["entrance_region"]),
                "id": ident,
                "entrance": data.get("exit", data.get("entrance", None)),
                "exit": data["entrance"],
                "two_way": two_way,
                "type": data["type"],
                "island": data.get("return_island", data.get("island", cls.entrance_groups.NONE)),
                "direction": cls.opposite_entrance_groups[data["direction"]],
                "coords": data.get("reverse_coords", data.get("coords", None)),

            }
            if reverse_data["coords"] == "flip_h":
                c = data["coords"]
                reverse_data["coords"] = (-c[0], c[1], c[2])
            elif reverse_data["coords"] == "flip_v":
                c = data["coords"]
                reverse_data["coords"] = (c[0], c[1],- c[2])

            if "extra_data" in data:
                reverse_data["extra_data"] = data["extra_data"]
            if "reverse_one_way_data" in data:
                reverse_data.setdefault("extra_data", {})
                reverse_data["extra_data"] = data["reverse_one_way_data"]
            if reverse_name in res:
                print(f"DUPLICATE ENTRANCE!!! {reverse_name}")
            res[reverse_name] = cls(reverse_name, reverse_data)

            res[name].vanilla_reciprocal = res[reverse_name]
            res[reverse_name].vanilla_reciprocal = res[name]

            res[name].required_groups = data.get("required_groups", [])
            res[reverse_name].required_groups = data.get("reverse_required_groups", [])

            # print(f"{i} {ENTRANCES[reverse_name].entrance_region} -> {ENTRANCES[reverse_name].exit_region}")
            ident += 1
            point: str = reverse_data["entrance_region"] + "<=>" + reverse_data["exit_region"]
            counter.setdefault(point, 0)
            counter[point] += 1
        return res


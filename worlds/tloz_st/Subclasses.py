
from .DSZeldaClient.subclasses import DSTransition
from .DSZeldaClient.ItemClass import DSItem, receive_normal, remove_vanilla_normal, receive_small_key, remove_vanilla_progressive
from enum import IntEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Client import SpiritTracksClient
from .data.Addresses import STAddr

async def receive_tos_key(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    key_count = item.value if item.name.startswith("Keyring") else 1

    async def write_keys_to_storage(dungeon) -> tuple[int, list, str]:
        from .data.Constants import DUNGEON_KEY_DATA
        key_data = DUNGEON_KEY_DATA[dungeon]
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
        res.append(await write_keys_to_storage(dungeon_key))
    return res

async def receive_tear_of_light(client: "SpiritTracksClient", ctx, item: "STItem", rii):
    if client.current_stage == 0x13 and client.last_vanilla_item[-1] != item.name:  # avoid calcing tears when vanilla
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

    bow_count = min(client.item_count(ctx, "Bow (Progressive)"), 3)
    bow_item = client.item_data["Bow (Progressive)"]
    if bow_count == 0:
        return await remove_vanilla_progressive(client, ctx, bow_item, rii)
    prog_address, prog_value = bow_item.progressive[bow_count-1]
    if bow_count == 1:
        prog_value |= await prog_address.read(ctx)
    return [prog_address.get_inner_write_list(prog_value), bow_item.ammo_address.get_inner_write_list(bow_item.give_ammo[bow_count-1])]

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
        if self.name.startswith("Passenger:"):
            return remove_passenger
        if self.name.startswith("Cargo:"):
            return remove_cargo
        if self.name.startswith("Stamp") and not self.name == "Stamp Book":
            return handle_stamps
        if self.name in self.all_item_groups["Basic Tracks"]:
            return remove_vanilla_tracks
        return super().get_remove_vanilla_function()

class EntranceGroups(IntEnum):
    NONE = 0
    # Directions
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4
    INSIDE = 5
    OUTSIDE = 6
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

    AREA_MASK = 0xF << 3

OPPOSITE_ENTRANCE_GROUPS = {
    EntranceGroups.RIGHT: EntranceGroups.LEFT,
    EntranceGroups.LEFT: EntranceGroups.RIGHT,
    EntranceGroups.UP: EntranceGroups.DOWN,
    EntranceGroups.DOWN: EntranceGroups.UP,
    0: 0,
    EntranceGroups.NONE: EntranceGroups.NONE,
    EntranceGroups.INSIDE: EntranceGroups.OUTSIDE,
    EntranceGroups.OUTSIDE: EntranceGroups.INSIDE
}

# Entrance data format
class STTransition(DSTransition):
    entrance_groups = EntranceGroups
    opposite_entrance_groups = OPPOSITE_ENTRANCE_GROUPS
import itertools
import json
from collections import Counter
from textwrap import indent
from typing import Dict, List, NamedTuple, Set, TYPE_CHECKING

import worlds.am2r.options
from BaseClasses import Item, ItemClassification
from .options import LocationSettings ,MetroidsInPool, MetroidsRequired

if TYPE_CHECKING:
    from . import AM2RWorld
else:
    AM2RWorld = object

class ItemData(NamedTuple):
    code: int
    group: str
    classification: ItemClassification = ItemClassification.progression
    game_id: int = 0
    required_num: int = 0
    

class AM2RItem(Item):
    game: str = "AM2R"


def create_item(player: int, name: str, progression: bool) -> Item:
    item_data = item_table[name]
    if progression:
        classification = ItemClassification.progression
        # print(f"forcing progression item: {name}")
    else:
        classification = item_data.classification
    # input(f"Creating item: {name} with classification {classification}")
    return AM2RItem(name, classification, item_data.code, player)


def create_fixed_item_pool() -> List[str]:
    required_items: Dict[str, int] = {name: data.required_num for name, data in item_table.items()}
    return list(Counter(required_items).elements())


def create_metroid_items(MetroidsRequired: MetroidsRequired, MetroidsInPool: MetroidsInPool, LocationSettings: LocationSettings) -> List[str]:
    if MetroidsRequired > MetroidsInPool:
        metroid_count = MetroidsRequired
    else:
        metroid_count = MetroidsInPool

    if LocationSettings == LocationSettings.option_items_and_A6:
        metroid_count -= 46  # metroids are forced vanilla in those settings and thats where you collect them from so don't add them to the pool

    if LocationSettings == LocationSettings.option_items_no_A6:
        metroid_count -= 41  # metroids are forced vanilla in those settings and thats where you collect them from so don't add them to the pool but exclude the 5 in A6

    if metroid_count < 0:
        metroid_count = 0  # dont generate negative metroids

    return ["Metroid" for _ in range(metroid_count)]


def create_trap_items(world: AM2RWorld, locations_to_trap: int) -> List[str]:
    trap_pool = trap_weights.copy()

    if world.options.RemoveFloodTrap.value == 1:
        del trap_pool["Flood Trap"]

    if world.options.RemoveTossTrap.value == 1:
        del trap_pool["Big Toss Trap"]

    if world.options.RemoveShortBeam.value == 1:
        del trap_pool["Short Beam"]

    if world.options.RemoveEMPTrap.value == 1:
        del trap_pool["EMP Trap"]
    
    if world.options.RemoveTouhouTrap.value == 1:
        del trap_pool["Touhou Trap"]

    if world.options.RemoveOHKOTrap.value == 1:
        del trap_pool["OHKO Trap"]

    if world.options.RemoveWrongWarpTrap == 1:
        del trap_pool["Wrong Warp"]

    if world.options.RemoveIceTrap.value == 1:
        del trap_pool["Ice Trap"]

    return world.random.choices(
        population=list(trap_pool.keys()),
        weights=list(trap_pool.values()),
        k=locations_to_trap
    )


def create_random_items(remaining_items: int, world: AM2RWorld) -> List[str]:
    # print(f"Creating {remaining_items} filler items")
    total_weight = world.options.PowerBombWeight.value + world.options.EnergyTankWeight.value + world.options.SuperMissileWeight.value + world.options.MissileWeight
    super_total = (int(remaining_items * (world.options.SuperMissileWeight.value / total_weight)))
    e_total = (int(remaining_items * (world.options.EnergyTankWeight.value / total_weight)))
    pb_count = (int(remaining_items * (world.options.PowerBombWeight / total_weight)))
    # print(f"Filler Items Breakdown - Supers: {super_total}, E Tanks: {e_total}, PBs: {pb_count}")

    super_total = abs(super_total - 1)
    e_total = abs(e_total - 1)
    pb_count = abs(pb_count - 3)
    missile_count =  remaining_items - (super_total + e_total + pb_count)
    # print(f"Filler Items Breakdown - Missiles: {missile_count}, Supers: {super_total}, E Tanks: {e_total}, PBs: {pb_count}")

    items_to_create = []

    for _ in range(pb_count):
        items_to_create.append("Power Bomb")
    for _ in range(e_total):
        items_to_create.append("Energy Tank")
    for _ in range(super_total):
        items_to_create.append("Super Missile")
    for _ in range(missile_count):
        items_to_create.append("Missile")

    # print(f'Items to create: {Counter(items_to_create)}')

    return items_to_create

    # print(f"Remaining items to fill: {remaining_items}\n"
    #       f"PBs to create: {pb_count}, Es to create: {e_total}, Supers to create: {super_total} missiles to create: {missile_count}")
    # input("This info will now do nothing good day\nAlso press enter to continue")
    #
    #
    # filler_pool = filler_weights.copy()
    #
    # return world.random.choices(
    #     population=list(filler_pool.keys()),
    #     weights=list(filler_pool.values()),
    #     k=remaining_items
    # )


def create_all_items(world: AM2RWorld) -> None:
    supers = 1
    PBs = 3
    player = world.player
    sum_locations = len(world.multiworld.get_unfilled_locations(player))
    # print(f"Total Locations for Player {player}: {sum_locations}")

    itempool = (
        create_fixed_item_pool()
        + create_metroid_items(world.options.MetroidsRequired, world.options.MetroidsInPool, world.options.LocationSettings)
    )
    # print(f"Fixed Items: {itempool}")
    # print(Counter(itempool))

    trap_percentage = world.options.TrapFillPercentage
    trap_fill = trap_percentage / 100

    random_count = sum_locations - len(itempool)
    locations_to_trap = int(trap_fill * random_count)
    itempool += create_trap_items(world, locations_to_trap)

    random_count = sum_locations - len(itempool)
    random_items = create_random_items(random_count, world)
    itempool += random_items

    # print(f'Random Items: {Counter(itempool)}')
    for name in itempool:
        # print(f"NAME: {name}")
        progression = False
        if name == "Super Missile" and supers > 0:
            supers -= 1
            progression = True
        if name == "Power Bomb" and PBs > 0:
            PBs -= 1
            progression = True

        world.multiworld.itempool += [create_item(player, name, progression)]


item_table: Dict[str, ItemData] = {
    "Missile":                  ItemData(108678000, "Ammo", ItemClassification.filler, 15),
    "Super Missile":            ItemData(108678001, "Ammo", ItemClassification.filler, 16, 1),
    "Power Bomb":               ItemData(108678002, "Ammo", ItemClassification.filler, 18, 3),
    "Energy Tank":              ItemData(108678003, "Ammo", ItemClassification.useful, 17, 1),
    "Bombs":                    ItemData(108678007, "Equipment", ItemClassification.progression, 0, 1),
    "Spider Ball":              ItemData(108678008, "Equipment", ItemClassification.progression, 2, 1),
    "Hi Jump":                  ItemData(108678009, "Equipment", ItemClassification.progression, 4, 1),
    "Spring Ball":              ItemData(108678010, "Equipment", ItemClassification.progression, 3, 1),
    "Space Jump":               ItemData(108678011, "Equipment", ItemClassification.progression, 6, 1),
    "Speed Booster":            ItemData(108678012, "Equipment", ItemClassification.progression, 7, 1),
    "Screw Attack":             ItemData(108678013, "Equipment", ItemClassification.progression, 8, 1),
    "Varia Suit":               ItemData(108678014, "Equipment", ItemClassification.useful, 5, 1),
    "Gravity Suit":             ItemData(108678015, "Equipment", ItemClassification.progression, 9, 1),
    "Charge Beam":              ItemData(108678016, "Beam", ItemClassification.progression, 10, 1),
    "Wave Beam":                ItemData(108678017, "Beam", ItemClassification.useful, 12, 1),
    "Spazer":                   ItemData(108678018, "Beam", ItemClassification.useful, 13, 1),
    "Plasma Beam":              ItemData(108678019, "Beam", ItemClassification.useful, 14, 1),
    "Ice Beam":                 ItemData(108678020, "Beam", ItemClassification.progression, 11, 1),
    "Flood Trap":               ItemData(108678021, "Trap", ItemClassification.trap, 21),
    "Big Toss Trap":            ItemData(108678022, "Trap", ItemClassification.trap, 22),
    "Short Beam":               ItemData(108678023, "Trap", ItemClassification.trap, 23),
    "EMP Trap":                 ItemData(108678024, "Trap", ItemClassification.trap, 24),
    "OHKO Trap":                ItemData(108678026, "Trap", ItemClassification.trap, 25),
    "Touhou Trap":              ItemData(108678027, "Trap", ItemClassification.trap, 26),
    "Wrong Warp":               ItemData(108678028, "Trap", ItemClassification.trap, 27),
    "Ice Trap":                 ItemData(108678029, "Trap", ItemClassification.trap, 28),
    "Metroid":                  ItemData(108678025, "MacGuffin", ItemClassification.progression_skip_balancing, 19),
  # "AP Item":                  ItemData(None     , "AP", ItemClassification.progression_skip_balancing, 100),
  # "Unimportant Item":         ItemData(None     , "AP", ItemClassification.progression_skip_balancing, 101),

}
filler_weights: Dict[str, int] = {
    "Missile":          44,
    "Super Missile":    9,
    "Power Bomb":       8,
    "Energy Tank":      9
}

trap_weights: Dict[str, int] = {
    "Flood Trap":           1,
    "Big Toss Trap":        1,
    "Short Beam":           1,
    "EMP Trap":             1,
    "Touhou Trap":          1,
    "OHKO Trap":            1,
    "Wrong Warp":           1,
    "Ice Trap":             1
}


def get_item_group(item_name: str) -> str:
    return item_table[item_name].group


def item_is_filler(item_name: str) -> bool:
    return item_table[item_name].classification == ItemClassification.filler


def item_is_trap(item_name: str) -> bool:
    return item_table[item_name].classification == ItemClassification.trap


trap_items: List[str] = list(filter(item_is_trap, item_table.keys()))
filler_items: List[str] = list(filter(item_is_filler, item_table.keys()))

item_name_to_id: Dict[str, int] = {name: data.code for name, data in item_table.items()}


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in itertools.groupby(item_table, get_item_group)
}

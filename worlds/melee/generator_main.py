import pkgutil
import os
import typing
import logging
from BaseClasses import Item, ItemClassification
from typing import Dict
from .Items import filler_item_table, item_table
from .Locations import get_locations
from .setup_game import setup_gamevars, place_static_items, calculate_trophy_based_locations
from .in_game_data import global_trophy_table
from .Regions import init_areas
from .Rules import set_location_rules
from .Rom import apply_patch, MeleePlayerContainer


class SSBMItem(Item):
    game: str = "Super Smash Bros. Melee"


def generate_early(world):
    setup_gamevars(world)
    world.authentication_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    for item in world.multiworld.precollected_items[world.player]:  # First add starting inventories to the Trophy Pool
        if item.name in global_trophy_table:
            world.picked_trophies.add(item.name)

    calculate_trophy_based_locations(world)  # Check if the current Trophy Pool will affect the location pool
    excess_trophies = len(world.picked_trophies) - (world.location_count - world.required_item_count)

    if excess_trophies > 0:
        logging.warning(f"""Warning: {world.multiworld.get_player_name(world.player)}'s generated Trophy Count is higher than the number of locations and required items.
                Your Trophy counts have automatically been lowered as necessary.""")

    # TODO; slice and shuffle this i guess? dont get it
    for i in range(excess_trophies):
        world.removed_list = sorted(world.picked_trophies)
        world.picked_trophies.remove(world.random.choice(world.removed_list))
        if world.options.extra_trophies:
            world.options.extra_trophies.value -= 1
        else:
            world.options.trophies_required.value -= 1

    calculate_trophy_based_locations(world)  # If the Trophy Pool was adjusted, recalculate this to remove the locations
    init_areas(world, get_locations(world))
    place_static_items(world)


def create_items(world) -> None:
    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)
    pool.remove(set_classifications(world, world.starting_character))  # Don't add a copy of the starter into the pool
    if world.options.lottery_pool_mode == 1:
        for i in range(4):
            pool.append(set_classifications(world, "Progressive Lottery Pool"))
    elif world.options.lottery_pool_mode == 2:
        pool.append(set_classifications(world, "Lottery Pool Upgrade (Adventure/Classic Clear)")),
        pool.append(set_classifications(world, "Lottery Pool Upgrade (Secret Characters)")),
        pool.append(set_classifications(world, "Lottery Pool Upgrade (200 Vs. Matches)")),
        pool.append(set_classifications(world, "Lottery Pool Upgrade (250 Trophies)")),

    if world.options.randomize_battle_items:
        pool.extend([
            set_classifications(world, "Capsule"),
            set_classifications(world, "Crate"),
            set_classifications(world, "Barrel"),
            set_classifications(world, "Egg"),
            set_classifications(world, "Party Ball"),
            set_classifications(world, "Barrel Cannon"),
            set_classifications(world, "Bob-omb"),
            set_classifications(world, "Mr. Saturn"),
            set_classifications(world, "Heart Container"),
            set_classifications(world, "Maxim Tomato"),
            set_classifications(world, "Starman"),
            set_classifications(world, "Home-Run Bat"),
            set_classifications(world, "Beam Sword"),
            set_classifications(world, "Parasol"),
            set_classifications(world, "Green Shell"),
            set_classifications(world, "Red Shell"),
            set_classifications(world, "Ray Gun"),
            set_classifications(world, "Freezie"),
            set_classifications(world, "Food"),
            set_classifications(world, "Motion-Sensor Bomb"),
            set_classifications(world, "Flipper"),
            set_classifications(world, "Super Scope"),
            set_classifications(world, "Star Rod"),
            set_classifications(world, "Lip's Stick"),
            set_classifications(world, "Fan"),
            set_classifications(world, "Fire Flower"),
            set_classifications(world, "Super Mushroom"),
            set_classifications(world, "Poison Mushroom"),
            set_classifications(world, "Hammer"),
            set_classifications(world, "Warp Star"),
            set_classifications(world, "Screw Attack"),
            set_classifications(world, "Bunny Hood"),
            set_classifications(world, "Metal Box"),
            set_classifications(world, "Cloaking Device"),
            set_classifications(world, "Poké Ball")])

    for trophy in world.picked_trophies:
        if trophy not in world.options.start_inventory:  # Don't create any extra trophies that are in start inventory
            pool.append(set_classifications(world, trophy))

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)
    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool


def set_rules(world) -> None:
    set_location_rules(world)


def generate_output(world, output_directory: str) -> None:
    from Main import __version__
    try:
        basepatch = pkgutil.get_data(__name__, "data/melee_base.xml")
        base_str = basepatch.decode("utf-8")
        world.encoded_slot_name = bytearray(f'SSBM{__version__.replace(".", "")[0:3]}_{world.player:05d}_{world.authentication_id:09d}\0', "utf8")[:27]
        world.rom_name = world.encoded_slot_name.decode("ascii").rstrip("\x00")
        world.encoded_slot_name = ''.join(f'{b:02X}' for b in world.encoded_slot_name)

        output_patch = apply_patch(world, base_str, output_directory)
        output_file_path = os.path.join(output_directory, f"AP-{world.multiworld.seed_name}-P{world.player}-{world.multiworld.get_file_safe_player_name(world.player)}.zip")
        #with open(output_file_path, "w") as file:
            #file.write(output_patch)
        patch_name = f"{world.multiworld.get_out_file_name_base(world.player)}"
        melee_container = MeleePlayerContainer(output_patch, output_file_path,
            world.multiworld.player_name[world.player], world.player, patch_name)
        melee_container.write()

    except Exception:
        raise
    finally:
        world.rom_name_available_event.set()


def fill_slot_data(world) -> Dict[str, typing.Any]:
    if world.options.lottery_pool_mode == 2:
        lottery_type = "Static"
    elif world.options.lottery_pool_mode == 1:
        lottery_type = "Progressive"
    else:
        lottery_type = "N/A"

    return {
        "authentication_id": world.authentication_id,
        "goal_triggers": world.options.goal_triggers.value,
        "total_trophies_required": world.options.trophies_required.value,
        "lottery_pool_mode": lottery_type
    }


def set_classifications(world, name) -> SSBMItem:
    item_data = item_table[name]
    item = SSBMItem(name, item_data.classification, item_data.code, world.player)
    if item_data.category == "Battle Items" and world.options.bonus_checks:
        item.classification = ItemClassification.progression
        
    if name == "Warp Star" and world.options.event_checks:
        item.classification = ItemClassification.progression
    return item


def create_item(world, name: str) -> SSBMItem:
    data = set_classifications(world, name)
    return SSBMItem(name, data.classification, data.code, world.player)


def modify_multidata(world, multidata: dict) -> None:
    # wait for world.rom_name to be available.
    world.rom_name_available_event.wait()
    rom_name = getattr(world, "rom_name", None)
    if rom_name:
        multidata["connect_names"][world.rom_name] = multidata["connect_names"][world.multiworld.player_name[world.player]]


def get_filler_item_name(world) -> str:  #
    return world.random.choice(filler_item_table)

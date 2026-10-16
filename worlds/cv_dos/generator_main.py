import typing
import os
import pkgutil

from typing import Dict, TextIO
from BaseClasses import Item, ItemClassification
from .Items import item_table
from .Options import SoulRandomizer, SoulsanityLevel
from .Rom import patch_rom, DoSProcPatch
from .setup_game import setup_game, place_souls


class CVDoSItem(Item):
    game: str = "Castlevania: Dawn of Sorrow"


def generate_early(world) -> None:
    from .setup_game import setup_souls
    if hasattr(world.multiworld, "re_gen_passthrough"):  # If UT
        if "Castlevania: Dawn of Sorrow" not in world.multiworld.re_gen_passthrough:
            return
        passthrough = world.multiworld.re_gen_passthrough["Castlevania: Dawn of Sorrow"]
        world.options.goal.value = passthrough["goal"]
        world.options.soul_randomizer.value = passthrough["soul_randomizer"]
        world.options.soulsanity_level.value = passthrough["soulsanity_level"]
        world.starting_warp_room = passthrough["starting_warp"]
        world.options.open_drawbridge = passthrough["open_drawbridge"]
        world.options.boost_speed = passthrough["speed_boost"]
        world.red_soul_walls = passthrough["soul_walls"]
        world.options.gate_items.value = passthrough["buttonsanity"]
        world.magic_seal_table = passthrough["seals"]
        world.options.menace_condition.value = passthrough["menace_condition"]
        world.options.mine_condition.value = passthrough["mine_condition"]
        world.options.garden_condition.value = passthrough["garden_condition"]
        world.connected_doors = passthrough["door_map"]
        world.options.no_logical_grinding.value = passthrough["no_grinding"]
    setup_game(world)
    setup_souls(world)

    world.auth_id = world.random.getrandbits(32)


def create_regions(world) -> None:
    from .setup_game import place_static_items, place_static_souls
    from .Regions import init_areas

    init_areas(world)
    place_static_items(world)
    if world.options.soul_randomizer != SoulRandomizer.option_soulsanity:
        place_static_souls(world)


def connect_entrances(world) -> None:
    from .modules.area_shuffle import shuffle_doors, set_ut_regions
    if world.connected_doors:
        set_ut_regions(world)

    if world.options.randomize_doors and not world.connected_doors:
        shuffle_doors(world)


def create_items(world) -> None:
    pool = []
    for name, data in item_table.items():
        for _ in range(data.default_count):
            item = set_classifications(world, name)
            pool.append(item)
    if world.options.start_with_doppelganger:
        pool.remove(set_classifications(world, "Doppelganger Soul"))

    if world.options.gate_items:
        pool.extend([set_classifications(world, "West Lab Gate Key"),
                     set_classifications(world, "East Lab Gate Key"),
                     set_classifications(world, "Garden Gate Key"),
                     set_classifications(world, "Cavern Gate Key")])

    placed_seals = []

    for seal in world.magic_seal_table:
        if seal in ["Mine of Judgment", "The Abyss"] and world.mine_status == "Disabled" or world.iron_mode:
            continue
        else:
            if world.magic_seal_table[seal] not in placed_seals:
                pool.append(set_classifications(world, world.magic_seal_table[seal]))  # Create the seal items if necessary)
                placed_seals.append(world.magic_seal_table[seal])

    place_souls(world, pool)

    filler_location_count = len(world.multiworld.get_unfilled_locations(world.player)) - len(pool)

    for i in range(filler_location_count):
        item = set_classifications(world, get_filler_item_name(world))
        pool.append(item)

    world.multiworld.itempool += pool


def set_classifications(world, name: str) -> CVDoSItem:
    data = item_table[name]
    item = CVDoSItem(name, data.classification, data.code, world.player)
    if name in world.important_souls:
        item.classification = ItemClassification.progression

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        if name == "Soul Eater Ring" and world.options.soulsanity_level == SoulsanityLevel.option_rare:
            item.classification = ItemClassification.progression

    return item


def create_item(world, name: str) -> CVDoSItem:
    data = set_classifications(world, name)
    return CVDoSItem(name, data.classification, data.code, world.player)


def create_progress_event(world, name: str) -> CVDoSItem:
    # Create item name [str] as a Progression Event item.
    return CVDoSItem(name, ItemClassification.progression, None, world.player)


def get_filler_item_name(world) -> str:
    from .setup_game import update_soul_pool
    from .Items import consumable_table, money_table, good_food_table
    weights = {"good_weapon": 5, "soul": 10, "good_food": 8, "good_armor": 15, "money": 20,
               "weapon": 30, "armor": 40, "consumable": 60}

    # If these pools have been exhausted, set their weights to 0
    if not world.weapon_table:
        weights["weapon"] = 0

    if not world.armor_table:
        weights["armor"] = 0

    if not world.good_weapon_table:
        weights["good_weapon"] = 0

    if not world.good_armor_table:
        weights["good_armor"] = 0

    filler_type = world.random.choices(list(weights), weights=list(weights.values()), k=1)[0]
    weight_table = {
        "soul": world.filler_souls,
        "good_weapon": world.good_weapon_table,
        "weapon": world.weapon_table,
        "armor": world.armor_table,
        "good_armor": world.good_armor_table,
        "money": money_table,
        "consumable": consumable_table,
        "good_food": good_food_table
    }

    filler_item = world.random.choice(weight_table[filler_type])

    if not world.has_tried_chaos_ring:
        world.has_tried_chaos_ring = True
        if world.random.randint(0, 101) <= 10:  # Chaos ring should have a single 10/100 chance to be placed
            filler_item = "Chaos Ring"

    if filler_item in world.weapon_table:
        world.weapon_table.remove(filler_item)
    elif filler_item in world.armor_table:
        world.armor_table.remove(filler_item)
    elif filler_item in world.good_armor_table:
        world.good_armor_table.remove(filler_item)
    elif filler_item in world.good_weapon_table:
        world.good_weapon_table.remove(filler_item)

    if filler_item in world.filler_souls:
        update_soul_pool(world, filler_item)

    return filler_item


def create_static_soul(world, soul):
    item = CVDoSItem(soul, ItemClassification.progression, None, world.player)  # Create an event item of the soul
    return item


def set_rules(world) -> None:
    from .Rules import set_location_rules
    set_location_rules(world)


def fill_slot_data(world) -> Dict[str, typing.Any]:
    return {
        "goal": world.options.goal.value,
        "starting_warp": world.starting_warp_room,
        "soul_randomizer": world.options.soul_randomizer.value,
        "soulsanity_level": world.options.soulsanity_level.value,
        "open_drawbridge": world.options.open_drawbridge.value,
        "speed_boost": world.options.boost_speed.value,
        "soul_walls": world.red_soul_walls,
        "buttonsanity": world.options.gate_items.value,
        "seals": world.magic_seal_table,
        "menace_condition": world.options.menace_condition.value,
        "garden_condition": world.options.garden_condition.value,
        "mine_condition": world.options.mine_condition.value,
        "door_map": world.connected_doors,
        "no_grinding": world.options.no_logical_grinding.value
    }


def generate_output(world, output_directory: str) -> None:
    world.has_generated_output = True  # Make sure data defined in generate output doesn't get added to spoiler only mode
    try:
        code_patch = pkgutil.get_data(__name__, "src/overlay_41.bin")
        patch = DoSProcPatch(player=world.player, player_name=world.multiworld.player_name[world.player])
        patch.write_file("dos_base.bsdiff4", pkgutil.get_data(__name__, "src/dos_base.bsdiff4"))
        patch_rom(world, patch, code_patch)

        world.rom_name = patch.name

        patch.write(os.path.join(output_directory,
                                 f"{world.multiworld.get_out_file_name_base(world.player)}{patch.patch_file_ending}"))
    except Exception:
        raise
    finally:
        world.rom_name_available_event.set()  # make sure threading continues and errors are collected


def modify_multidata(world, multidata: dict) -> None:
    # wait for self.rom_name to be available.
    world.rom_name_available_event.wait()
    rom_name = getattr(world, "rom_name", None)
    if rom_name:
        multidata["connect_names"][world.rom_name] = multidata["connect_names"][world.player_name]


def write_spoiler_header(world, spoiler_handle: TextIO) -> None:
    from .modules.area_shuffle import door_data
    if world.options.shuffle_starting_warp_room:
        spoiler_handle.write(f"Default Warp Room:    {world.starting_warp_room}\n")

    if world.options.randomize_red_soul_walls:
        spoiler_handle.write(f"\nSoul Barriers:\n")
        spoiler_handle.write(f" Paranoia 1:  {world.red_soul_walls[1]}\n")
        spoiler_handle.write(f" Paranoia 2:  {world.red_soul_walls[0]}\n")
        spoiler_handle.write(f" Paranoia 3:  {world.red_soul_walls[3]}\n")
        spoiler_handle.write(f" Dark Chapel Catacombs:  {world.red_soul_walls[2]}\n")

    if world.options.boss_shuffle:
        spoiler_handle.write(f"\nBosses:\n")
        for boss in world.boss_slots:
            spoiler_handle.write(f" {boss}:  {world.boss_slots[boss].new_boss}\n")

    if world.options.seal_shuffle:
        spoiler_handle.write(f"\nMagic Seals:\n")
        for seal in world.magic_seal_table:
            if seal in ["Mine of Judgment", "The Abyss"] and world.mine_status == "Disabled":  # Ignore Magic Seals that are past the endgame trigger
                continue
            else:
                spoiler_handle.write(f" {seal}:  {world.magic_seal_table[seal]}\n")

    if world.options.randomize_doors:
        spoiler_handle.write("\nEntrances:")
        for door in world.connected_doors:
            if not door_data[door[0]].is_left_facing:
                continue
            spoiler_handle.write(f"\n   {door_data[door[0]].entrance_name} <=> {door_data[door[1]].entrance_name}")
    spoiler_handle.write("\n")
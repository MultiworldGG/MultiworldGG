import logging

from BaseClasses import Item, ItemClassification

from ..data.Constants import (
    DUNGEON_NAMES,
    ESSENCES,
    ITEM_GROUPS,
    MARKET_LOCATIONS,
    SEED_ITEMS,
    VALID_ORE_ITEM_VALUES,
    VALID_RUPEE_ITEM_VALUES,
)
from ..data.items import ITEMS_DATA
from ..data.locations import LOCATIONS_DATA
from ..generation.create_regions import location_is_active
from ..options import (
    OracleOfSeasonsDuplicateSeedTree,
    OracleOfSeasonsFoolsOre,
    OracleOfSeasonsLogicDifficulty,
    OracleOfSeasonsMasterKeys,
    OracleOfSeasonsShopPrices,
    OracleOfSeasonsStartingPosition,
)
from ..world import OracleOfSeasonsWorld


def create_item(world: OracleOfSeasonsWorld, name: str) -> Item:
    # If item name has a "!PROG" suffix, force it to be progression. This is typically used to create the right
    # amount of progression rupees while keeping them a filler item as default
    if name.endswith("!PROG"):
        name = name.removesuffix("!PROG")
        classification = ItemClassification.progression_deprioritized_skip_balancing
    elif name.endswith("!USEFUL"):
        # Same for above but with useful. This is typically used for Required Rings,
        # as we don't want those locked in a barren dungeon
        name = name.removesuffix("!USEFUL")
        classification = ITEMS_DATA[name]["classification"]
        if classification == ItemClassification.filler:
            classification = ItemClassification.useful
    elif name.endswith("!FILLER"):
        name = name.removesuffix("!FILLER")
        classification = ItemClassification.filler
    else:
        classification = ITEMS_DATA[name]["classification"]
    ap_code = world.item_name_to_id[name]

    # A few items become progression only in hard logic
    progression_items_in_medium_logic = [
        "Expert's Ring",
        "Fist Ring",
        "Swimmer's Ring",
        "Energy Ring",
        "Heart Ring L-2",
    ]
    progression_items_in_hard_logic = [
        "Heart Ring L-1",
        "Toss Ring",
    ]
    if (
        world.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium
        and name in progression_items_in_medium_logic
    ):
        classification = ItemClassification.progression_deprioritized_skip_balancing
    elif (
        world.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_hard
        and name in progression_items_in_hard_logic
    ):
        classification = ItemClassification.progression_deprioritized_skip_balancing
    # As many Gasha Seeds become progression as the number of deterministic Gasha Nuts
    elif world.remaining_progression_gasha_seeds > 0 and name == "Gasha Seed":
        world.remaining_progression_gasha_seeds -= 1
        classification = ItemClassification.progression_deprioritized
    # Some number of containers depending on logic difficulty becomes prog
    elif world.remaining_progression_containers > 0 and name == "Heart Container":
        world.remaining_progression_containers -= 1
        classification = ItemClassification.progression_skip_balancing

    # Players in Medium+ are expected to know the default paths through Lost Woods, Phonograph becomes filler
    elif (
        world.options.logic_difficulty >= OracleOfSeasonsLogicDifficulty.option_medium
        and not world.options.randomize_lost_woods_item_sequence
        and name == "Phonograph"
    ):
        classification = ItemClassification.filler

    return Item(name, classification, ap_code, world.player)


def create_items(world: OracleOfSeasonsWorld) -> None:
    item_pool_dict = build_item_pool_dict(world)
    items = [create_item(world, item_name) for item_name, quantity in item_pool_dict.items() for _ in range(quantity)]
    filter_confined_dungeon_items_from_pool(world, items)

    if (
        world.options.start_position == OracleOfSeasonsStartingPosition.option_sunken_city
        or world.options.start_position == OracleOfSeasonsStartingPosition.option_samasa_desert
        or world.options.start_position == OracleOfSeasonsStartingPosition.option_tarm_entrance
    ):
        nothing_item = Item("Nothing", ItemClassification.useful, -1, world.player)
        nothing_item_2 = Item("Nothing", ItemClassification.useful, -1, world.player)
        # Put it useful so that it can be swapped with anything
        items.append(nothing_item)
        items.append(nothing_item_2)
        world.nothing_items = [nothing_item, nothing_item_2]

    world.multiworld.itempool.extend(items)
    pre_fill_seeds(world)


def build_item_pool_dict(world: OracleOfSeasonsWorld) -> dict[str, int]:
    excluded_mapass = set()
    if world.options.exclude_dungeons_without_essence and not world.options.shuffle_essences:
        for i, essence_name in enumerate(ESSENCES, 1):
            if essence_name not in world.essences_in_game:
                excluded_mapass.add(f"Dungeon Map ({DUNGEON_NAMES[i]})")
                excluded_mapass.add(f"Compass ({DUNGEON_NAMES[i]})")

    item_pool_dict = {}
    filler_item_count = 0
    rupee_item_count = 0
    ore_item_count = 0

    if world.options.enforce_potion_in_shop:
        world.get_location("Horon Village: Shop #3").place_locked_item(create_item(world, "Potion"))
        filler_item_count -= 1

    for loc_name, loc_data in LOCATIONS_DATA.items():
        if not location_is_active(world, loc_name, loc_data):
            continue
        if "local" in loc_data:
            continue

        item_name = loc_data["vanilla_item"]
        if item_name == "Hint":
            continue
        if "Ring" in item_name:
            item_name = "Random Ring"
        if item_name == "Filler Item":
            filler_item_count += 1
            continue
        if item_name.startswith("Rupees ("):
            if world.options.shop_prices == OracleOfSeasonsShopPrices.option_free:
                filler_item_count += 1
            else:
                rupee_item_count += 1
            continue
        if item_name.startswith("Ore Chunks ("):
            if (
                world.options.shop_prices == OracleOfSeasonsShopPrices.option_free
                or not world.options.shuffle_golden_ore_spots
            ):
                filler_item_count += 1
            else:
                ore_item_count += 1
            continue
        if world.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled and "Small Key" in item_name:
            # Small Keys don't exist if Master Keys are set to replace them
            filler_item_count += 1
            continue
        if world.options.master_keys == OracleOfSeasonsMasterKeys.option_all_dungeon_keys and "Boss Key" in item_name:
            # Boss keys don't exist if Master Keys are set to replace them
            filler_item_count += 1
            continue
        if world.options.starting_maps_compasses and ("Compass" in item_name or "Dungeon Map" in item_name):
            # Compasses and Dungeon Maps don't exist if player starts with them
            filler_item_count += 1
            continue
        if "essence" in loc_data and loc_data["essence"] is True:
            # If essence was decided not to be placed because of "Placed Essences" option or
            # because of pedestal being an excluded location, replace it with a filler item
            if item_name not in world.essences_in_game:
                filler_item_count += 1
                continue
            # If essences are not shuffled, place and lock this item directly on the pedestal.
            # Otherwise, the fill algorithm will take care of placing them anywhere in the multiworld.
            if not world.options.shuffle_essences:
                essence_item = create_item(world, item_name)
                world.get_location(loc_name).place_locked_item(essence_item)
                continue

        if item_name == "Gasha Seed":
            # Remove all gasha seeds from the pool to read as many as needed a later
            # while limiting their impact on the item pool
            filler_item_count += 1
            continue

        if item_name == "Fool's Ore" and world.options.fools_ore == OracleOfSeasonsFoolsOre.option_excluded:
            filler_item_count += 1
            continue

        if item_name.startswith("Bombs (") or item_name.startswith("Bombchus ("):
            # We're changing the bomb distribution
            filler_item_count += 1
            continue

        if item_name == "Flute":
            item_name = world.options.animal_companion.current_key.title() + "'s Flute"
        elif item_name in excluded_mapass:
            item_name += "!FILLER"

        if item_name.endswith("Jewel"):
            filler_item_count += 1
            continue

        item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

    item_pool_dict["Bomb Upgrade"] = 3
    item_pool_dict["Bombchu Upgrade"] = 3
    extra_items = 6
    if world.options.cross_items:
        item_pool_dict["Cane of Somaria"] = 1
        item_pool_dict["Switch Hook"] = 2
        item_pool_dict["Seed Shooter"] = 1
        extra_items += 4

    # If Master Keys are enabled, put one for every dungeon
    if world.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled:
        for small_key_name in sorted(ITEM_GROUPS["Master Keys"]):
            if world.options.linked_heros_cave or small_key_name != "Master Key (Linked Hero's Cave)":
                item_pool_dict[small_key_name] = 1
                extra_items += 1

    # Add the required gasha seeds to the pool
    required_gasha_seeds = world.options.deterministic_gasha_locations.value
    item_pool_dict["Gasha Seed"] = required_gasha_seeds
    extra_items += required_gasha_seeds

    # Add the jewels back to the pool, they are added here to control the classification
    jewels = sorted(ITEM_GROUPS["Jewels"])
    world.random.shuffle(jewels)
    required_jewels = world.options.tarm_gate_required_jewels.value
    for jewel_number, jewel in enumerate(jewels):
        if jewel_number >= required_jewels:
            jewel_name = f"{jewel}!USEFUL"
        else:
            jewel_name = jewel
        item_pool_dict[jewel_name] = 1
    extra_items += 4

    # Add the 3rd sword to the pool
    item_pool_dict["Progressive Sword"] += 1
    extra_items += 1

    if rupee_item_count > 0:
        rupee_item_pool, filler_item_count = build_rupee_item_dict(world, rupee_item_count, filler_item_count)
        item_pool_dict.update(rupee_item_pool)

    if ore_item_count > 0:
        ore_item_pool, filler_item_count = build_ore_item_dict(world, ore_item_count, filler_item_count)
        item_pool_dict.update(ore_item_pool)

    # Remove items from pool
    for item, removed_amount in world.options.remove_items_from_pool.items():
        if item in item_pool_dict:
            current_amount = item_pool_dict[item]
        else:
            current_amount = 0
        new_amount = current_amount - removed_amount
        if new_amount < 0:
            logging.warning(
                f"Not enough {item} to satisfy {world.player_name}'s remove_items_from_pool: {-new_amount} missing"
            )
            new_amount = 0
        item_pool_dict[item] = new_amount
        filler_item_count += current_amount - new_amount

    # Add the required rings
    ring_copy = sorted(world.options.required_rings.value.copy())
    for _ in range(len(ring_copy)):
        ring_name = f"{ring_copy.pop()}!USEFUL"
        item_pool_dict[ring_name] = item_pool_dict.get(ring_name, 0) + 1

        if item_pool_dict["Random Ring"] > 0:
            # Take from set ring pool first
            item_pool_dict["Random Ring"] -= 1
        else:
            # Take from filler after
            filler_item_count -= 1

    assert filler_item_count >= extra_items
    filler_item_count -= extra_items

    if filler_item_count > 0:
        item_pool_dict["Rupees (1)"] = 1
        filler_item_count -= 1

    # Add as many filler items as required
    for _ in range(filler_item_count):
        random_filler_item = world.get_filler_item_name()
        item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1

    if "Random Ring" in item_pool_dict:
        quantity = item_pool_dict["Random Ring"]
        for _ in range(quantity):
            ring_name = world.get_random_ring_name()
            item_pool_dict[ring_name] = item_pool_dict.get(ring_name, 0) + 1
        del item_pool_dict["Random Ring"]

    return item_pool_dict


def build_rupee_item_dict(
    world: OracleOfSeasonsWorld, rupee_item_count: int, filler_item_count: int
) -> tuple[dict[str, int], int]:
    sorted_shop_values = sorted(world.shop_requirements.values())
    total_cost = sorted_shop_values[-1]

    return build_currency_item_dict(
        world, rupee_item_count, filler_item_count, total_cost, "Rupees", VALID_RUPEE_ITEM_VALUES
    )


def build_ore_item_dict(
    world: OracleOfSeasonsWorld, ore_item_count: int, filler_item_count: int
) -> tuple[dict[str, int], int]:
    total_cost = sum([world.shop_prices[loc] for loc in MARKET_LOCATIONS])

    return build_currency_item_dict(
        world, ore_item_count, filler_item_count, total_cost, "Ore Chunks", VALID_ORE_ITEM_VALUES
    )


def build_currency_item_dict(
    world: OracleOfSeasonsWorld,
    currency_item_count: int,
    filler_item_count: int,
    total_cost: int,
    currency_name: str,
    valid_currency_item_values: list[int],
) -> tuple[dict[str, int], int]:
    average_value = total_cost / currency_item_count
    deviation = average_value / 2.5
    currency_item_dict = {}
    target = total_cost
    for _ in range(0, currency_item_count):
        value = world.random.gauss(average_value, deviation)
        value = min(valid_currency_item_values, key=lambda x: abs(x - value))
        if value > average_value / 3:
            # Put a "!PROG" suffix to force them to be created as progression items (see `create_item`)
            item_name = f"{currency_name} ({value})!PROG"
            target -= value
        else:
            # Don't count little packs as progression since they are likely irrelevant
            item_name = f"{currency_name} ({value})"
        currency_item_dict[item_name] = currency_item_dict.get(item_name, 0) + 1
    # If the target is positive, it means there aren't enough rupees, so we'll steal a filler from the pool and reroll
    if target > 0:
        return build_currency_item_dict(
            world,
            currency_item_count + 1,
            filler_item_count - 1,
            total_cost,
            currency_name,
            valid_currency_item_values,
        )
    return currency_item_dict, filler_item_count


def filter_confined_dungeon_items_from_pool(world: OracleOfSeasonsWorld, items: list[Item]) -> None:
    confined_dungeon_items = []
    excluded_dungeons = []
    if world.options.exclude_dungeons_without_essence and not world.options.shuffle_essences:
        for i, essence_name in enumerate(ESSENCES):
            if essence_name not in world.essences_in_game:
                excluded_dungeons.append(i + 1)

    # Put Small Keys / Master Keys unless keysanity is enabled for those
    if world.options.master_keys != OracleOfSeasonsMasterKeys.option_disabled:
        small_keys_name = "Master Key"
    else:
        small_keys_name = "Small Key"
    if not world.options.keysanity_small_keys:
        confined_dungeon_items.extend([item for item in items if item.name.startswith(small_keys_name)])
    else:
        for i in excluded_dungeons:
            confined_dungeon_items.extend(
                [item for item in items if item.name == f"{small_keys_name} ({DUNGEON_NAMES[i]})"]
            )

    # Put Boss Keys unless keysanity is enabled for those
    if not world.options.keysanity_boss_keys:
        confined_dungeon_items.extend([item for item in items if item.name.startswith("Boss Key")])
    else:
        for i in excluded_dungeons:
            confined_dungeon_items.extend([item for item in items if item.name == f"Boss Key ({DUNGEON_NAMES[i]})"])

    # Put Maps & Compasses unless keysanity is enabled for those
    if not world.options.keysanity_maps_compasses:
        excluded_map_compass = [
            item for item in items if item.name.startswith("Dungeon Map") or item.name.startswith("Compass")
        ]
        for item in excluded_map_compass:
            items.remove(item)
        world.nonprog_pre_fill_items.extend(excluded_map_compass)

    for item in confined_dungeon_items:
        items.remove(item)
    world.prog_pre_fill_items.extend(confined_dungeon_items)


def pre_fill_seeds(world: OracleOfSeasonsWorld) -> None:
    # The prefill algorithm for seeds has a few constraints:
    #   - it needs to place the "default seed" into Horon Village seed tree
    #   - it needs to place a random seed on the "duplicate tree" (can be Horon's tree)
    #   - it needs to place one of each seed on the 5 remaining trees
    # This has a few implications:
    #   - if Horon is the duplicate tree, this is the simplest case: we just place a starting seed in Horon's tree
    #     and scatter the 5 seed types on the 5 other trees
    #   - if Horon is NOT the duplicate tree, we need to remove Horon's seed from the pool of 5 seeds to scatter
    #     and put a random seed inside the duplicate tree. Then, we place the 4 remaining seeds on the 4 remaining
    #     trees
    trees_table = {
        OracleOfSeasonsDuplicateSeedTree.option_horon_village: "Horon Village: Seed Tree",
        OracleOfSeasonsDuplicateSeedTree.option_woods_of_winter: "Woods of Winter: Seed Tree",
        OracleOfSeasonsDuplicateSeedTree.option_north_horon: "Holodrum Plain: Seed Tree",
        OracleOfSeasonsDuplicateSeedTree.option_spool_swamp: "Spool Swamp: Seed Tree",
        OracleOfSeasonsDuplicateSeedTree.option_sunken_city: "Sunken City: Seed Tree",
        OracleOfSeasonsDuplicateSeedTree.option_tarm_ruins: "Tarm Ruins: Seed Tree",
    }
    duplicate_tree_name = trees_table[world.options.duplicate_seed_tree.value]

    def place_seed(seed_name: str, location_name: str):
        seed_item = create_item(world, seed_name)
        world.get_location(location_name).place_locked_item(seed_item)

    seeds_to_place = list(SEED_ITEMS)

    manually_placed_trees = set()

    # Place default seed type
    if world.options.start_position == OracleOfSeasonsStartingPosition.option_horon_village:
        default_tree = "Horon Village: Seed Tree"
    elif world.options.start_position == OracleOfSeasonsStartingPosition.option_sunken_city:
        default_tree = "Sunken City: Seed Tree"
    elif world.options.start_position == OracleOfSeasonsStartingPosition.option_tarm_entrance:
        default_tree = "Spool Swamp: Seed Tree"
    else:
        default_tree = None
    if default_tree is not None:
        place_seed(SEED_ITEMS[world.options.default_seed.value], default_tree)
        manually_placed_trees.add(default_tree)
        if duplicate_tree_name != default_tree:
            # If duplicate tree is not default's, remove default seed from the pool of placeable seeds
            del seeds_to_place[world.options.default_seed.value]

    if duplicate_tree_name not in manually_placed_trees:
        place_seed(world.random.choice(SEED_ITEMS), duplicate_tree_name)
        manually_placed_trees.add(duplicate_tree_name)

    trees_to_process = [name for name in trees_table.values() if name not in manually_placed_trees]

    # Place remaining seeds on remaining trees
    world.random.shuffle(trees_to_process)
    for seed in seeds_to_place:
        place_seed(seed, trees_to_process.pop())

    assert not trees_to_process, "Not all trees were filled with seeds"

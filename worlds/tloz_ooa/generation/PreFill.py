from ..data import *
from ..data.Constants import *
from Fill import fill_restrictive, FillError
from Options import OptionError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import OracleOfAgesWorld

import logging

def pre_fill(world: "OracleOfAgesWorld") -> None:
    pre_fill_seeds(world)
    pre_fill_dungeon_items(world)

    # world.debug_pre_fill("Dimitri's Flute", "Impa Gift")


def debug_pre_fill(world: "OracleOfAgesWorld", i, l):
    collection_state = world.multiworld.get_all_state(False)

    locations = [
        loc for loc in world.multiworld.get_locations(world.player) if l in loc.name
    ]
    item = [world.create_item(i)]
    print(item)
    print(locations)
    fill_restrictive(
        world.multiworld,
        collection_state,
        locations,
        item,
        single_player_placement=True,
        lock=True,
        allow_excluded=True,
    )


def pre_fill_dungeon_items(world: "OracleOfAgesWorld"):
    # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
    # of those which makes them pretty crowded.
    # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
    # To circumvent this, we perform a restricted pre-fill here, placing only those dungeon items
    # before anything else.
    collection_state = world.multiworld.get_all_state(False)
    D6_remaining_location = []

    for i in range(11):
        if i == 10:
            if world.options.linked_heros_cave.value > 0:
                i = 11
            else:
                continue
        # Build a list of locations in this dungeon
        dungeon_location_names = [
            name
            for name, loc in LOCATIONS_DATA.items()
            if "dungeon" in loc and loc["dungeon"] == i
        ]
        dungeon_locations = [
            loc
            for loc in world.multiworld.get_locations(world.player)
            if loc.name in dungeon_location_names
        ]

        # Build a list of dungeon items that are "confined" (i.e. must be placed inside this dungeon)
        # See `create_items` to see how `world.dungeon_items` is populated depending on current options.
        confined_dungeon_items = [
            item
            for item in world.dungeon_items
            if item.name.endswith(f"({DUNGEON_NAMES[i]})")
            or (i == 8 and "Slate" in item.name)
        ]
        if len(confined_dungeon_items) == 0:
            if i == 9 or i == 6:
                D6_remaining_location += dungeon_locations
            continue  # This list might be empty with some keysanity options
        for item in confined_dungeon_items:
            collection_state.remove(item)

        # Perform a prefill to place confined items inside locations of this dungeon
        for attempts_remaining in range(2, -1, -1):
            world.random.shuffle(dungeon_locations)
            try:
                fill_restrictive(
                    world.multiworld,
                    collection_state,
                    dungeon_locations,
                    confined_dungeon_items,
                    single_player_placement=True,
                    lock=True,
                    allow_excluded=True,
                )
                if i == 9 or i == 6:
                    D6_remaining_location += dungeon_locations
                break
            except FillError as exc:
                if attempts_remaining == 0:
                    raise exc
                logging.debug(
                    f"Failed to shuffle dungeon items for player {world.player}. Retrying..."
                )

    # D6 specific item that can appear in both dungeon (the boss key)
    d6CommonDungeon = "(Mermaid's Cave)"

    confined_dungeon_items = [
        item for item in world.dungeon_items if item.name.endswith(d6CommonDungeon)
    ]

    for item in confined_dungeon_items:
        collection_state.remove(item)

    # Preplace D6 Boss key
    for attempts_remaining in range(2, -1, -1):
        world.random.shuffle(D6_remaining_location)
        try:
            fill_restrictive(
                world.multiworld,
                collection_state,
                D6_remaining_location,
                confined_dungeon_items,
                single_player_placement=True,
                lock=True,
                allow_excluded=True,
            )
            break
        except FillError as exc:
            if attempts_remaining == 0:
                raise exc
            logging.debug(
                f"Failed to shuffle dungeon items for player {world.player}. Retrying..."
            )


def pre_fill_seeds(world: "OracleOfAgesWorld") -> None:
    # Grab/validate the duplicate trees setting
    duplicate_trees = world.options.duplicate_seed_trees.value

    if len(duplicate_trees) > 3:
        raise OptionError("Can't select more than 3 duplicate seed trees")

    for entry in duplicate_trees:
        if entry not in TREES_TABLE:
            raise OptionError(f"Invalid duplicate seed tree entry: {entry}")

    duplicate_trees_to_process = [TREES_TABLE[tree] for tree in duplicate_trees]

    # If all is good, proceed to seed placement...

    def place_seed(seed_name: str, location_name: str):
        seed_item = world.create_item(seed_name)
        world.multiworld.get_location(location_name, world.player).place_locked_item(
            seed_item
        )
        world.pre_fill_items.append(seed_item)

    # Grab the seeds to place. We'll shuffle the duplicate seeds list, since we're only getting 3 (or 2...) of the 5 types
    seeds_to_place = list(SEED_ITEMS)
    duplicate_seeds_to_place = list(SEED_ITEMS)

    # Consolidate the lists of non-duplicate trees and duplicates
    manually_placed_trees = ["Lynna City: Seed Tree"] + duplicate_trees_to_process
    trees_to_process = [
        name for key, name in TREES_TABLE.items() if name not in manually_placed_trees
    ]

    # If there are fewer than 3 duplicates specified, choose random ones (other than Lynna) to get it up to 3
    world.random.shuffle(trees_to_process)
    for i in range(3 - len(duplicate_trees_to_process)):
        duplicate_trees_to_process.append(trees_to_process.pop())

    # Place default seed type in Lynna tree
    place_seed(SEED_ITEMS[world.options.default_seed.value], "Lynna City: Seed Tree")

    # Cleanup depending on whether Lynna was specified as a duplicate...
    if "Lynna City: Seed Tree" not in duplicate_trees_to_process:
        # If Lynna was NOT specified as a duplicate, we just need to remove the default seed type from the list of seeds.
        # In this case, it's not going to be in either trees_to_process or duplicate_trees_to_process
        del seeds_to_place[world.options.default_seed.value]
    else:
        # If Lynna is specified as a duplicate, then we just remove it from the list of duplicates, since we already placed
        # something there. We don't need to worry about anything else; in this case trees_to_process will contain 5 trees
        # representing all 5 types. One of those will match whatever Lynna is, guaranteeing it to be a duplicate as desired.
        del duplicate_seeds_to_place[world.options.default_seed.value]
        duplicate_trees_to_process.remove("Lynna City: Seed Tree")

    # Place remaining seeds on remaining trees
    for seed in seeds_to_place:
        place_seed(seed, trees_to_process.pop())

    # Fill out the duplicates
    world.random.shuffle(duplicate_seeds_to_place)
    for tree in duplicate_trees_to_process:
        place_seed(duplicate_seeds_to_place.pop(), tree)
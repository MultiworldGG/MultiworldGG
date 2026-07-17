from ..data import *
from ..data.Constants import *
from Fill import fill_restrictive, FillError
from Options import OptionError
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .. import OracleOfAgesWorld

import logging

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def pre_fill(world: "OracleOfAgesWorld") -> None:
    pre_fill_seeds(world)
    pre_fill_dungeon_items(world)

    # world.debug_pre_fill("Dimitri's Flute", "Impa Gift")


# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
#def debug_pre_fill(world: "OracleOfAgesWorld", i, l):
#    collection_state = world.multiworld.get_all_state(False)
#
#    # NOTE : Create_item shouldn't be called during the pre_fill process. No new items should be created during this step
#    # But for debug, it work. It's shouldn't be pushed tho.
#    locations = [
#        loc for loc in world.multiworld.get_locations(world.player) if l in loc.name
#    ]
#    item = [create_item(world, i)]
#    print(item)
#    print(locations)
#    fill_restrictive(
#        world.multiworld,
#        collection_state,
#        locations,
#        item,
#        single_player_placement=True,
#        lock=True,
#        allow_excluded=True,
#    )


# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
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

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def pre_fill_seeds(world: "OracleOfAgesWorld") -> None:
    for loc, seedItem in world.pre_fill_seeds.items():
        world.multiworld.get_location(loc, world.player).place_locked_item(seedItem)
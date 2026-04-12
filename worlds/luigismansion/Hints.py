import copy
from typing import Any, List, TYPE_CHECKING

from BaseClasses import Location,  MultiWorld
if TYPE_CHECKING:
    from . import LMWorld

ALWAYS_HINT: dict[str, int] = {"Madame Clairvoya": 3, "Foyer Toad": 2, "Wardrobe Balcony Toad": 40, "1F Washroom Toad": 16,
                               "Courtyard Toad": 24,"Left Telephone": 53, "Center Telephone": 53, "Right Telephone": 53}

PORTRAIT_HINTS: dict[str, int] = {"<father>": 35, "<mother>": 34, "<baby>": 26, "<dancer>": 9, "<situji>": 18,
                                  "<pianist>": 22, "<eater>": 8, "<dog01>": 11, "<builder>": 23, "<hustler>": 12,
                                  "<fat>": 48, "<obaasan>": 49, "<girl>": 29, "<dboy>":27, "<denwa>": 41,
                                  "<gaka>": 60, "<snowman>": 64, "<doll1>": 59, "<doll2>": 59, "<doll3>": 59}


def get_progression_only_items(world: "LMWorld", hinted_loc, prog_items_no_skip) -> Location:
    prog_items_location_list: set[Location] = (set([pItem.location for pItem in prog_items_no_skip]))

    # Only returns true if all items in the above list exist in hinted_loc list
    if prog_items_location_list.issubset(hinted_loc):
        return world.random.choice(sorted(prog_items_no_skip)).location

    non_hinted_items = [pItem for pItem in prog_items_no_skip if pItem.location not in hinted_loc]
    return world.random.choice(sorted(non_hinted_items)).location


def get_other_items(world: "LMWorld", hinted_loc, other_items) -> Location:
    other_items_location_list: set[Location] = (set([oItem.location for oItem in other_items]))

    # Only returns true if all items in the above list exist in hinted_loc list
    if other_items_location_list.issubset(hinted_loc):
        return world.random.choice(sorted(other_items)).location

    non_hinted_items = [oItem for oItem in other_items if oItem.location not in hinted_loc]
    return world.random.choice(sorted(non_hinted_items)).location


def get_hints_by_option(multiworld: MultiWorld, player_hints: set[int]) -> None:
    # Since locations are optional and you cannot hint items with no location, these will get filtered out.
    all_placed_items = [loc.item for loc in multiworld.get_filled_locations() if not loc is None and loc.item.location is loc]
    player_hint_worlds = sorted(player_hints)
    for player_int in player_hint_worlds:
        world: "LMWorld" = multiworld.worlds[player_int]
        prog_no_skip = [item for item in all_placed_items if item.advancement and not item.code is None and
            item.location is not None and not item.skip_in_prog_balancing and
            (item.player == player_int or item.location.player == player_int)]
        other_items = [item for item in all_placed_items if not item.advancement and not item.code is None and
            item.location is not None and (item.player == player_int or item.location.player == player_int)]
        already_hinted_locations: List[Location] = []
        hint_list: dict[str, int] = copy.deepcopy(ALWAYS_HINT)
        if world.options.portrait_hints == 1:
            hint_list.update(PORTRAIT_HINTS)
        for name in hint_list.keys():
            if name == "Madame Clairvoya":
                if world.open_doors[72] == 0:
                    locs: list[Location] = multiworld.find_item_locations("Spade Key", player_int, True)
                else:
                    iname: str = world.random.choice(sorted(["Mario's Glove", "Mario's Letter", "Mario's Hat", "Mario's Star",
                                                     "Mario's Shoe"]))
                    locs: list[Location] = multiworld.find_item_locations(iname, player_int, True)

                if not locs:
                    locs = [get_progression_only_items(world, already_hinted_locations, prog_no_skip)]

                loc: Location = world.random.choice(sorted(locs))
                hint = {name: {"Item": loc.item.name,
                               "Location": loc.name,
                               "Location ID": str(loc.address),
                               "Rec Player": multiworld.player_name[loc.item.player],
                               "Send Player": multiworld.player_name[loc.player],
                               "Send Player ID": str(loc.player),
                               "Game": loc.game,
                               "Class": "Prog"}}
                already_hinted_locations.append(loc)
                world.hints.update(hint)
            else:
                loc: Any = None
                if world.options.hint_distribution.value == 0 or world.options.hint_distribution.value == 4:
                    hint_type = world.random.choices(sorted(["Prog", "Other"]), [60, 40], k=1)[0]
                    if hint_type == "Prog":
                        loc = get_progression_only_items(world, already_hinted_locations, prog_no_skip)
                    else:
                        loc = get_other_items(world, already_hinted_locations, other_items)
                elif world.options.hint_distribution.value == 3 or world.options.hint_distribution.value == 1:
                    hint_type = world.random.choices(sorted(["Prog", "Other"]), [90, 10], k=1)[0]
                    if hint_type == "Prog":
                        loc = get_progression_only_items(world, already_hinted_locations, prog_no_skip)
                    else:
                        loc = get_other_items(world, already_hinted_locations, other_items)
                elif world.options.hint_distribution.value == 2:
                    non_hinted_items = [aItem for aItem in all_placed_items if aItem.location not in already_hinted_locations
                        and not aItem.code is None and (aItem.player == player_int or aItem.location.player == player_int)]
                    loc = world.random.choice(sorted(non_hinted_items)).location
                if loc.item.advancement:
                    icolor = "Prog"
                elif loc.item.trap:
                    icolor = "Trap"
                else:
                    icolor = "Other"
                item_name: str = loc.item.name
                if loc.player in world.multiworld.groups:
                    loc: Location = world.random.choice(sorted(world.multiworld.find_item_locations(
                        item_name, loc.player, True)))
                hint = {name: {"Item": item_name,
                               "Location": loc.name,
                               "Location ID": str(loc.address),
                               "Rec Player": multiworld.player_name[loc.item.player],
                               "Send Player": multiworld.player_name[loc.player],
                               "Send Player ID": str(loc.player),
                               "Game": loc.game,
                               "Class": icolor}}
                already_hinted_locations.append(loc)
                world.hints.update(hint)
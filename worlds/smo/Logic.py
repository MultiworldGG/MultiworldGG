from BaseClasses import CollectionState
from .Items import outfits, shop_items, moon_types, world_list

def count_moons(self, state: CollectionState, kingdom : str, player: int) -> int:
    """ Counts the number of in logic moons available for a given kingdom.
        Args:
            self: SMOWorld object for this player's world.
            state: The CollectionState of the current player.
            kingdom: A string containing the kingdom name.
            player: The index of this world's player.
        Return:
            Count of the moons for Kingdom 'kingdom'
    """
    amt = 0
    player_prog_items = state.prog_items[player]

    kingdom_name = "" if self.options.progressive_moons else f'{kingdom} '

    amt += 0 if not f"{kingdom_name}Power Moon" in player_prog_items else player_prog_items[f"{kingdom_name}Power Moon"]
    amt += 0 if not f"{kingdom_name}Story Moon" in player_prog_items else player_prog_items[f"{kingdom_name}Story Moon"]
    amt += 0 if not f"{kingdom_name}Multi-Moon" in player_prog_items else player_prog_items[f"{kingdom_name}Multi-Moon"] * 3

    if self.options.progressive_moons:
        amt -= sum(self.indexed_moon_counts[0:world_list.index(kingdom)])

    return amt


def total_moons(self, state: CollectionState, player: int) -> int:
    """Returns the cumulative count of items from an item group present in state.
        Args:
            self: SMOWorld object for this player's world.
            state: The CollectionState of the current player.
            player: The index of this world's player.
        Return:
            The number of total in logic power moons.
    """
    amt = 0

    for item_name in moon_types:
        if "Multi-Moon" in item_name:
            amt += state.count(item_name, player) * 3
        else:
            amt += state.count(item_name, player)

    return amt



from BaseClasses import CollectionState
from test.bases import WorldTestBase
from ..data import data


class PokemonCrystalTestBase(WorldTestBase):
    game = data.manifest.game


def swept_state(test, withheld) -> CollectionState:
    """Every itempool item except ``withheld``, then one sweep; placed events only when reachable."""
    withheld = set(withheld)
    state = CollectionState(test.multiworld)
    for item in test.multiworld.itempool:
        if item.name not in withheld:
            state.collect(item, prevent_sweep=True)
    state.sweep_for_advancements()
    return state


def verify_region_access(test, items_dont_collect, regions, items_collect=None):
    if items_collect is None:
        items_collect = items_dont_collect

    test.multiworld.state = swept_state(test, items_dont_collect)
    for region in regions:
        test.assertFalse(test.can_reach_region(region),
                         f"Region {region} reachable without items {items_dont_collect}.")
    test.multiworld.state = swept_state(test, set(items_dont_collect) - set(items_collect))
    for region in regions:
        test.assertTrue(test.can_reach_region(region), f"Region {region} unreachable with items {items_collect}.")


def verify_location_access(test, items_dont_collect, locations, items_collect=None):
    if items_collect is None:
        items_collect = items_dont_collect

    test.multiworld.state = swept_state(test, items_dont_collect)
    for location in locations:
        test.assertFalse(test.can_reach_location(location),
                         f"Location {location} reachable without items {items_dont_collect}.")
    test.multiworld.state = swept_state(test, set(items_dont_collect) - set(items_collect))
    for location in locations:
        test.assertTrue(test.can_reach_location(location),
                        f"Location {location} unreachable with items {items_collect}.")

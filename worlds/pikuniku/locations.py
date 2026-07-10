from __future__ import annotations

import math
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import PikunikuWorld

BASE_LOCATION_ID = 100

# Item requirement shorthands. Each location's requirements are absolute
# (they include everything needed to reach and clear the location).
# "Apple x3" is parsed as Has("Apple", count=3) in rules.py.
# "Coins" is only applied as a requirement when coinsanity is enabled.
VALLEY_MAIN = ("Pencil Hat",)
APPLE_TEMPLE = (*VALLEY_MAIN, "Apple x3")
FROG_TEMPLE = (*VALLEY_MAIN, "Water Hat")
PAST_EL_BUNKO = (*VALLEY_MAIN, "Sunglasses", "Magnetic Card")
VALLEY_REVISITED = (*PAST_EL_BUNKO, "Water Hat")
LAKE = (*PAST_EL_BUNKO, "Water Hat")
CAVE = (*LAKE, "The Cabin Key")
SUNSHINE_HQ = (*CAVE, "A Detonator")
COOP = ("Co-op Level Access",)

# Each "5 Coins" item is worth 5 coins. Shop prices are in coins.
COIN_VALUE = 5
SHOP_PRICES = {
    "Valley Plush Purchase": 15,
    "Forest Sunglasses Purchase": 1,
    "Forest Postcard Purchase": 1,
    "Forest X-Ray Goggles Purchase": 70,
}

# The number of "5 Coins" items that are progression: enough to afford every shop purchase (currently 20).
PROGRESSION_FIVE_COINS_COUNT = math.ceil(sum(SHOP_PRICES.values()) / COIN_VALUE)


def get_required_five_coins(shop_name: str) -> int:
    # Coins are spent when purchasing, which AP logic cannot model directly.
    # So each purchase logically requires enough coins for itself plus every cheaper purchase,
    # guaranteeing the player can never spend themselves out of logic.
    price = SHOP_PRICES[shop_name]
    cumulative_price = sum(other_price for other_price in SHOP_PRICES.values() if other_price <= price)
    return math.ceil(cumulative_price / COIN_VALUE)


class PikunikuLocationData(NamedTuple):
    name: str
    region: str
    requirements: tuple[str, ...] = ()


# Locations that always exist.
BASE_LOCATIONS = [
    # Trophies
    PikunikuLocationData("Walking Piku Trophy", "The Valley"),
    PikunikuLocationData("The Hidden Rock Trophy", "The Valley"),
    PikunikuLocationData("Baskick Champion Trophy", "The Valley"),
    PikunikuLocationData("Sam The Slime Trophy", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("The Resistance Trophy", "The Forest", (*VALLEY_MAIN, "Magnetic Card")),
    PikunikuLocationData("A Giant Robot Trophy", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Demonic Toast Trophy", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("PikDug Trophy", "The Lake", LAKE),
    PikunikuLocationData("Piku at The Beach Trophy", "The Valley", ("Water Hat",)),
    PikunikuLocationData("The Worms Trophy", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Ernie the Worm Trophy", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Sunshine Inc. Robot Trophy", "Sunshine HQ", SUNSHINE_HQ),
    PikunikuLocationData("Mr. Sunshine Trophy", "Sunshine HQ", SUNSHINE_HQ),
    # Dancing Bugs
    PikunikuLocationData("Valley Dancing Bug", "The Valley"),
    PikunikuLocationData("Road to Forest Dancing Bug", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Forest Dancing Bug", "The Forest", VALLEY_REVISITED),
    PikunikuLocationData("Cave Dancing Bug", "The Cave", CAVE),
    PikunikuLocationData("Sunshine HQ Dancing Bug", "Sunshine HQ", SUNSHINE_HQ),
    # Shops ("Coins" only applies when coinsanity is enabled)
    PikunikuLocationData("Valley Plush Purchase", "The Valley", ("Coins",)),
    PikunikuLocationData("Forest Sunglasses Purchase", "The Forest", ("Coins", *VALLEY_MAIN)),
    PikunikuLocationData("Forest Postcard Purchase", "The Forest", ("Coins", *VALLEY_MAIN)),
    PikunikuLocationData("Forest X-Ray Goggles Purchase", "The Forest", ("Coins", *VALLEY_MAIN)),
    # Other
    PikunikuLocationData("Pencil Hat", "The Valley"),
    PikunikuLocationData("Apple 1", "The Valley"),
    PikunikuLocationData("Apple 2", "The Valley"),
    PikunikuLocationData("Apple 3", "The Valley"),
    PikunikuLocationData("Beast Mask", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Flower Hat", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Draw on the Tree", "The Forest", (*VALLEY_MAIN, "Pencil Hat")),
    PikunikuLocationData("Magnetic Card", "The Forest", (*VALLEY_MAIN, "Sunglasses")),
    PikunikuLocationData("Defeat the First Giant Robot", "The Forest", PAST_EL_BUNKO),
    PikunikuLocationData("Water Hat", "The Forest", PAST_EL_BUNKO),
    PikunikuLocationData("Golden Tooth from the Silver Frog", "The Forest", (*VALLEY_MAIN, "Water Hat")),
    PikunikuLocationData(
        "Some Arms", "The Valley (Revisited)", (*LAKE, "The Golden Tooth from the Silver Frog")
    ),
    PikunikuLocationData("Defeat the Second Giant Robot", "The Valley (Revisited)", LAKE),
    PikunikuLocationData("The Cabin Key", "The Cave", LAKE),
    PikunikuLocationData("A Video Game", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("A Detonator", "The Cave", CAVE),
    PikunikuLocationData("Defeat the Third Giant Robot", "The Lake", SUNSHINE_HQ),
]

# Locations that only exist when the co-op levels option is enabled.
COOP_LOCATIONS = [
    PikunikuLocationData("Piku & Niku I Trophy", "Co-op Levels", COOP),
    PikunikuLocationData("Piku & Niku II Trophy", "Co-op Levels", COOP),
    PikunikuLocationData("Piku & Niku III Trophy", "Co-op Levels", COOP),
    PikunikuLocationData("Piku & Niku IV Trophy", "Co-op Levels", COOP),
    PikunikuLocationData("Piku & Niku V Trophy", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 1 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 2 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 3 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 4 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 5 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 6 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 7 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 8 Complete", "Co-op Levels", COOP),
    PikunikuLocationData("Co-op Level 9 Complete", "Co-op Levels", COOP),
]

# Freestanding coins. Only exist when coinsanity is enabled.
COIN_LOCATIONS = [
    # The Valley
    PikunikuLocationData("Valley: Coin near windmill 1", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin near windmill 2", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin near windmill 3", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above shop", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above umbrella", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above cloud 1", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above cloud 2", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above cloud 3", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above flower house", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin left under moving bridge", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin right under moving bridge", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above lower cornfield 1", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above lower cornfield 2", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above lower cornfield 3", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above lower cornfield 4", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin in air between cornfields 1", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin in air between cornfields 2", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above upper cornfield 1", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above upper cornfield 2", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above upper cornfield 3", "The Valley", VALLEY_MAIN),
    PikunikuLocationData("Valley: Coin above upper cornfield 4", "The Valley", VALLEY_MAIN),
    # Apple Temple
    PikunikuLocationData("Apple Temple: Coin next to spring", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin on spike trap", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin on first platform between spikes", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin on second platform between spikes", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin near hidden room", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin after breakable rock 1", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin after breakable rock 2", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin after breakable rock 3", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin requiring 2 buttons puzzle 1", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin requiring 2 buttons puzzle 2", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin requiring 2 buttons puzzle 3", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin requiring 2 buttons puzzle 4", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin requiring 2 buttons puzzle 5", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin requiring 2 buttons puzzle 6", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin between spike ceilings", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin at start of bounce pad chain", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin at end of temple 1", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin at end of temple 2", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin at end of temple 3", "Apple Temple", APPLE_TEMPLE),
    PikunikuLocationData("Apple Temple: Coin at end of temple 4", "Apple Temple", APPLE_TEMPLE),
    # The Valley Road
    PikunikuLocationData("Valley Road: Coin at start", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin near hooks", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on clouds above hooks", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on clouds after boulders", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin in mushroom cave", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on lower cave after door 1", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on lower cave after door 2", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on lower cave after door 3", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on upper cloud near flower", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 1", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 2", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 3", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 4", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 5", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 6", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 7", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 8", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 9", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 10", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 11", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 12", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 13", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on moving cloud 14", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin at end of moving clouds", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin in hook upper hidden room 1", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin in hook upper hidden room 2", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin in hook upper hidden room 3", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin in hook upper hidden room 4", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on zipline", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin on tree branch", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin near trees", "The Valley Road", VALLEY_MAIN),
    PikunikuLocationData("Valley Road: Coin in water hat area room 1", "The Valley Road", (*VALLEY_MAIN, "Water Hat")),
    PikunikuLocationData("Valley Road: Coin in water hat area room 2", "The Valley Road", (*VALLEY_MAIN, "Water Hat")),
    PikunikuLocationData("Valley Road: Coin in water hat area room 3", "The Valley Road", (*VALLEY_MAIN, "Water Hat")),
    PikunikuLocationData("Valley Road: Coin in water hat area room 4", "The Valley Road", (*VALLEY_MAIN, "Water Hat")),
    # The Forest
    PikunikuLocationData("Forest: Coin on cut down log", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on triple cut down logs 1", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on triple cut down logs 2", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on triple cut down logs 3", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on ramp", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on first log gear", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on top of first log gear log", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on second log gear", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on fourth log", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin between logs", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on fifth log gear", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin under sixth log gear", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin near owl on log", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin after logs", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on town tree branch left", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin on town tree branch right", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin above community house", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin to the right of toastopia house", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin after rope bridge right of houses", "The Forest", VALLEY_MAIN),
    PikunikuLocationData("Forest: Coin atop last tree branch 1", "The Forest", FROG_TEMPLE), # Requires water hat
    PikunikuLocationData("Forest: Coin atop last tree branch 2", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 1", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 2", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 3", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 4", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 5", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 6", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 7", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 8", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 9", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 10", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 11", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 12", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 13", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 14", "The Forest", FROG_TEMPLE),
    PikunikuLocationData("Forest: Coin on moving cloud 15", "The Forest", FROG_TEMPLE),
    # Temple of the Silver Frog
    PikunikuLocationData("Frog Temple: Coin left of entrance 1", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin left of entrance 2", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin left of entrance 3", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin on spike trap", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin before hook", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin after 2nd checkpoint", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin above arrow pit", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin at symbol puzzle hint", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin at nut bridge puzzle 1", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin at nut bridge puzzle 2", "Temple of the Silver Frog", FROG_TEMPLE),
    PikunikuLocationData("Frog Temple: Coin at nut bridge puzzle 3", "Temple of the Silver Frog", FROG_TEMPLE),
    # The Cave (before the detonator tunnel)
    PikunikuLocationData("Cave: Coin in spring tunnel 1", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin in spring tunnel 2", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin in spring tunnel 3", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin in spring tunnel 4", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin after first pipe tunnel 1", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin after first pipe tunnel 2", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin before detonator tunnel 1", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin before detonator tunnel 2", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin before detonator tunnel 3", "The Cave", CAVE),
    PikunikuLocationData("Cave: Coin before detonator tunnel 4", "The Cave", CAVE),
    # The Cave (past the detonator tunnel, requires Detonator)
    PikunikuLocationData("Cave: Coin near moving platforms", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin after first resistance puzzle 1", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin after first resistance puzzle 2", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin hidden near plant", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin after second resistance puzzle", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin above worm room 1", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin above worm room 2", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin under worm room", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin above ernie worm", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin above gray spinning cross 1", "The Cave", SUNSHINE_HQ),
    PikunikuLocationData("Cave: Coin above gray spinning cross 2", "The Cave", SUNSHINE_HQ),
]

ALL_LOCATIONS = [*BASE_LOCATIONS, *COOP_LOCATIONS, *COIN_LOCATIONS]

LOCATION_NAME_TO_ID = {
    location_data.name: BASE_LOCATION_ID + index for index, location_data in enumerate(ALL_LOCATIONS)
}

LOCATION_NAME_GROUPS = {
    "Trophies": {data.name for data in ALL_LOCATIONS if data.name.endswith("Trophy")},
    "Dancing Bugs": {data.name for data in BASE_LOCATIONS if data.name.endswith("Dancing Bug")},
    "Shops": {data.name for data in BASE_LOCATIONS if data.name.endswith("Purchase")},
    "Coins": {data.name for data in COIN_LOCATIONS},
    "Co-op Levels": {data.name for data in COOP_LOCATIONS},
}

# The victory event. Requirements per the logic sheet: everything needed to reach Mr. Sunshine.
VICTORY_EVENT_LOCATION = "Defeat Mr. Sunshine"
VICTORY_REQUIREMENTS = SUNSHINE_HQ


class PikunikuLocation(Location):
    game = "Pikuniku"


def get_active_location_data(world: PikunikuWorld) -> list[PikunikuLocationData]:
    active_locations = list(BASE_LOCATIONS)
    if world.options.coop_levels:
        active_locations += COOP_LOCATIONS
    if world.options.coinsanity:
        active_locations += COIN_LOCATIONS
    return active_locations


def create_all_locations(world: PikunikuWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: PikunikuWorld) -> None:
    locations_per_region: dict[str, dict[str, int | None]] = {}
    for location_data in get_active_location_data(world):
        locations_per_region.setdefault(location_data.region, {})[location_data.name] = LOCATION_NAME_TO_ID[
            location_data.name
        ]

    for region_name, region_locations in locations_per_region.items():
        world.get_region(region_name).add_locations(region_locations, PikunikuLocation)


def create_events(world: PikunikuWorld) -> None:
    sunshine_hq = world.get_region("Sunshine HQ")
    sunshine_hq.add_event(
        VICTORY_EVENT_LOCATION, "Victory", location_type=PikunikuLocation, item_type=items.PikunikuItem
    )

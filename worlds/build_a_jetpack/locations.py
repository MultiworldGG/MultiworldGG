from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, Location

from .items import BuildJetpackItem

if TYPE_CHECKING:
    from .world import BuildJetpackWorld

LOCATION_NAME_TO_ID = {
    "Diving Suit 1": 1,
    "Diving Suit 2": 2,
    "Diving Suit 3": 3,
    "Diving Suit 4": 4,
    "Diving Suit 5": 5,
    "Diving Suit 6": 6,
    "Diving Suit 7": 7,
    "Diving Suit 8": 8,
    "Oxygen Mask 1": 9,
    "Oxygen Mask 2": 10,
    "Oxygen Mask 3": 11,
    "Oxygen Mask 4": 12,
    "Oxygen Mask 5": 13,
    "Oxygen Mask 6": 14,
    "Oxygen Mask 7": 15,
    "Oxygen Mask 8": 16,
    "Backpack 1": 17,
    "Backpack 2": 18,
    "Backpack 3": 19,
    "Backpack 4": 20,
    "Backpack 5": 21,
    "Backpack 6": 22,
    "Backpack 7": 23,
    "Fins 1": 24,
    "Fins 2": 25,
    "Fins 3": 26,
    "Fins 4": 27,
    "Fins 5": 28,
    "Fins 6": 29,
    "Fins 7": 30,
    "Magnet 1": 31,
    "Magnet 2": 32,
    "Magnet 3": 33,
    "Magnet 4": 34,
    "Magnet 5": 35,
    "Magnet 6": 36,
    "Magnet 7": 37,
    "Magnet 8": 38,
    "Raft Expansion 1": 39,
    "Raft Expansion 2": 40,
    "Raft Expansion 3": 41,
    "Jetpack 1": 42,
    "Jetpack 2": 43,
    "Jetpack 3": 44,
    "Radar 1": 45,
    "Radar 2": 46,
    "Radar 3": 47,
    "Radar 4": 48,
    "Radar 5": 49,
    "Gold Statue": 50,
    "Tuna": 51,
    "Cod": 52,
    "Pollock": 53,
    "Mackerel": 54,
    "Flounder": 55,
    "Mahi": 56,
    "Halibut": 57,
    "Snapper": 58,
    "Grouper": 59,
    "Marlin": 60,
    "Pufferfish": 61,
    "Spikefin": 62,
    "Barracuda": 63,
    "Shark": 64,
    "Spacefish": 65,
    "Skyfish": 66,
    "Cloudswim": 67,
}

class BuildJetpackLocation(Location):
    game = "Build a Jetpack"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}

def get_all_shop_locations() -> dict[str, int | None]:
    shop_locations = ["Gold Statue"]

    for i in range(8):
        shop_locations.append("Diving Suit "+str(i+1))
        shop_locations.append("Oxygen Mask "+str(i+1))
        shop_locations.append("Magnet "+str(i+1))
    for i in range(7):
        shop_locations.append("Backpack "+str(i+1))
        shop_locations.append("Fins "+str(i+1))
    for i in range(5):
        shop_locations.append("Radar "+str(i+1))
    for i in range(3):
        shop_locations.append("Raft Expansion "+str(i+1))
        shop_locations.append("Jetpack "+str(i+1))
    
    return get_location_names_with_ids(shop_locations)

def create_all_locations(world: BuildJetpackWorld) -> None:
    create_regular_locations(world)
    create_events(world)

def create_regular_locations(world: BuildJetpackWorld) -> None:
    world.get_region("Raft").add_locations(get_all_shop_locations(), BuildJetpackLocation)

    if world.options.fishsanity:
        world.get_region("Sky 2").add_locations(get_location_names_with_ids(["Spacefish"]), BuildJetpackLocation)
        world.get_region("Sky 1").add_locations(get_location_names_with_ids(["Cloudswim","Skyfish"]), BuildJetpackLocation)
        world.get_region("Sea 1").add_locations(get_location_names_with_ids(["Tuna","Cod"]), BuildJetpackLocation)
        world.get_region("Sea 2").add_locations(get_location_names_with_ids(["Pollock","Mackerel","Spikefin"]), BuildJetpackLocation)
        world.get_region("Sea 3").add_locations(get_location_names_with_ids(["Flounder"]), BuildJetpackLocation)
        world.get_region("Sea 4").add_locations(get_location_names_with_ids(["Mahi"]), BuildJetpackLocation)
        world.get_region("Sea 5").add_locations(get_location_names_with_ids(["Halibut","Barracuda"]), BuildJetpackLocation)
        world.get_region("Sea 6").add_locations(get_location_names_with_ids(["Snapper","Pufferfish"]), BuildJetpackLocation)
        world.get_region("Sea 7").add_locations(get_location_names_with_ids(["Grouper","Marlin"]), BuildJetpackLocation)
        world.get_region("Sea 8").add_locations(get_location_names_with_ids(["Shark"]), BuildJetpackLocation)



def create_events(world: BuildJetpackWorld) -> None:
    sky3 = world.get_region("Sky 3")
    sea2 = world.get_region("Sea 2")
    sea3 = world.get_region("Sea 3")
    sea5 = world.get_region("Sea 5")
    sea6 = world.get_region("Sea 6")
    sea8 = world.get_region("Sea 8")

    # technically wood also exists as a sea 1 item, but sea 1 is sphere 1 so i feel no need to make an event for that

    sea2.add_event(
        "Obtain Strings", "Strings", location_type=BuildJetpackLocation, item_type=BuildJetpackItem
    )
    
    sea3.add_event(
        "Obtain Rock", "Rock", location_type=BuildJetpackLocation, item_type=BuildJetpackItem
    )
    
    sea5.add_event(
        "Obtain More Rock", "More Rock", location_type=BuildJetpackLocation, item_type=BuildJetpackItem
    )
    
    sea6.add_event(
        "Obtain Gold", "Gold", location_type=BuildJetpackLocation, item_type=BuildJetpackItem
    )
    
    sea8.add_event(
        "Obtain More Gold", "More Gold", location_type=BuildJetpackLocation, item_type=BuildJetpackItem
    )
    
    sky3.add_event(
        "Reach for the Stars", "Victory", location_type=BuildJetpackLocation, item_type=BuildJetpackItem
    )
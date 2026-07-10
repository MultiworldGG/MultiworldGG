from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import items

if TYPE_CHECKING:
    from .world import SkulWorld

def _build_location_name_to_id() -> dict[str, int]:
    locs: dict[str, int] = {}

    # Bone upgrades (100-159)
    bone_base = 100
    for name in [
        "Marrow Transplant", "Thick Bone", "Fatal Mind",
        "Quick Dislocation", "Fracture Prevention", "Ancestral Fortitude",
    ]:
        for i in range(1, 11):
            locs[f"{name} {i}"] = bone_base
            bone_base += 1

    # Dark Quartz upgrades (160-171)
    dq_base = 160
    for name in [
        "Nutrition Supply", "Heavy Frame", "Spirit Acceleration",
        "Exoskeleton Reinforcement", "Reassemble", "Ancient Alchemy",
    ]:
        for i in range(1, 3):
            locs[f"{name} {i}"] = dq_base
            dq_base += 1

    # # Shop items (Forest 196-203, Grand Hall 204-211, Black Lab 212-219)
    # for area, base in [
    #     ("Forest of Harmony", 196),
    #     ("Grand Hall",        204),
    #     ("The Black Lab",     212),
    # ]:
    #     for i in range(1, 9):
    #         locs[f"{area} Shop Item {i}"] = base + i - 1

    # Castle Repair (220-223)
    for i in range(1, 5):
        locs[f"Castle Repair {i}"] = 220 + i - 1

    # # Fortress shop items (228-235)
    # for i in range(1, 9):
    #     locs[f"Fortress of Fate Shop Item {i}"] = 228 + i - 1

    # Mini boss and boss defeats (236-243)
    locs["Forest of Harmony Mini Boss Defeated"]  = 236
    locs["Forest of Harmony Boss Defeated"]       = 237
    locs["Grand Hall Mini Boss Defeated"]          = 238
    locs["Fortress of Fate Mini Boss Defeated"]    = 239
    locs["Grand Hall Boss Defeated"]               = 240
    locs["The Black Lab Mini Boss Defeated"]       = 241
    locs["The Black Lab Boss Defeated"]            = 242
    locs["Fortress of Fate Boss Defeated"]         = 243

    # Shrine checks (550+, up to 50)
    for i in range(1, 51):
        locs[f"Shrine {i}"] = 550 + i - 1

    # Room-cleared checks (Forest 500+, Grand Hall 600+, Black Lab 700+, Fortress 800+)
    for area, base in [
        ("Forest of Harmony", 500),
        ("Grand Hall",        600),
        ("The Black Lab",     700),
        ("Fortress of Fate",  800),
    ]:
        for room in range(1, 17):
            locs[f"{area} Room {room} Cleared"] = base + room - 1

    return locs


LOCATION_NAME_TO_ID = _build_location_name_to_id()

class SkulLocation(Location):
    game = "Skul: The Hero Slayer"

def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: SkulWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: SkulWorld) -> None:
    stronghold = world.get_region("Stronghold")
    forest = world.get_region("Forest of Harmony")
    grand_hall = world.get_region("Grand Hall")
    black_lab = world.get_region("The Black Lab")
    fortress = world.get_region("Fortress of Fate")

    req_rooms = world.options.req_room_count.value
    shrine_checks_count = world.options.shrine_checks_count.value

    # Stronghold: bone upgrades and castle repair
    stronghold_locs: list[str] = []
    for name in [
        "Marrow Transplant", "Thick Bone", "Fatal Mind",
        "Quick Dislocation", "Fracture Prevention", "Ancestral Fortitude",
    ]:
        stronghold_locs += [f"{name} {i}" for i in range(1, 11)]
    for name in [
        "Nutrition Supply", "Heavy Frame", "Spirit Acceleration",
        "Exoskeleton Reinforcement", "Reassemble", "Ancient Alchemy",
    ]:
        stronghold_locs += [f"{name} {i}" for i in range(1, 3)]
    stronghold_locs += [f"Castle Repair {i}" for i in range(1, 5)]
    stronghold_locs += [f"Shrine {i}" for i in range(1, shrine_checks_count + 1)]
    stronghold.add_locations(get_location_names_with_ids(stronghold_locs), SkulLocation)

    # Stage areas: room-cleared checks, mini boss + boss defeats, shop items
    for area, region in [
        ("Forest of Harmony", forest),
        ("Grand Hall",        grand_hall),
        ("The Black Lab",     black_lab),
        ("Fortress of Fate",  fortress),
    ]:
        area_locs = {f"{area} Room {i} Cleared": LOCATION_NAME_TO_ID[f"{area} Room {i} Cleared"]
                     for i in range(1, req_rooms + 1)}
        area_locs[f"{area} Mini Boss Defeated"] = LOCATION_NAME_TO_ID[f"{area} Mini Boss Defeated"]
        area_locs[f"{area} Boss Defeated"]       = LOCATION_NAME_TO_ID[f"{area} Boss Defeated"]
        # area_locs |= {f"{area} Shop Item {i}": LOCATION_NAME_TO_ID[f"{area} Shop Item {i}"]
        #               for i in range(1, 9)}
        region.add_locations(area_locs, SkulLocation)


def create_events(world: SkulWorld) -> None:
    sacred_grounds = world.get_region("Sacred Grounds")
    sacred_grounds.add_event(
        "Final Boss Defeated", "Victory", location_type=SkulLocation, item_type=items.SkulItem
    )

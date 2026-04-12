from typing import Any, Dict, List, Set, Tuple, Union

import json

from BaseClasses import ItemClassification

from .data.entrance_data import Entrance, EntranceRuleData
from .data.item_data import item_data, ZorkGrandInquisitorItemData
from .data.location_data import location_data, ZorkGrandInquisitorLocationData
from .data.transform_data import item_data_transforms, location_data_transforms
from .data.universal_tracker_data import tracker_location_groups, tracker_location_group_configuration

from .enums import (
    ZorkGrandInquisitorClientSeedInformation,
    ZorkGrandInquisitorCraftableSpellBehaviors,
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorEntranceRandomizer,
    ZorkGrandInquisitorEvents,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorHotspots,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorItemTransforms,
    ZorkGrandInquisitorLandmarksanity,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorLocationTransforms,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorStartingLocations,
    ZorkGrandInquisitorTags,
)


def item_names_to_id() -> Dict[str, int]:
    return {item.value: data.archipelago_id for item, data in item_data.items()}


def item_names_to_item() -> Dict[str, ZorkGrandInquisitorItems]:
    return {item.value: item for item in item_data}


def location_names_to_id() -> Dict[Any, int]:
    return {
        location.value: data.archipelago_id
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def location_names_to_location() -> Dict[Any, ZorkGrandInquisitorLocations]:
    return {
        location.value: location
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def id_to_client_seed_information() -> Dict[int, ZorkGrandInquisitorClientSeedInformation]:
    return {info.value: info for info in ZorkGrandInquisitorClientSeedInformation}


def id_to_craftable_spell_behaviors() -> Dict[int, ZorkGrandInquisitorCraftableSpellBehaviors]:
    return {behavior.value: behavior for behavior in ZorkGrandInquisitorCraftableSpellBehaviors}


def id_to_deathsanity() -> Dict[int, ZorkGrandInquisitorDeathsanity]:
    return {deathsanity.value: deathsanity for deathsanity in ZorkGrandInquisitorDeathsanity}


def id_to_entrance_randomizer() -> Dict[int, ZorkGrandInquisitorEntranceRandomizer]:
    return {er.value: er for er in ZorkGrandInquisitorEntranceRandomizer}


def id_to_goals() -> Dict[int, ZorkGrandInquisitorGoals]:
    return {goal.value: goal for goal in ZorkGrandInquisitorGoals}


def id_to_hotspots() -> Dict[int, ZorkGrandInquisitorHotspots]:
    return {hotspot.value: hotspot for hotspot in ZorkGrandInquisitorHotspots}


def id_to_items() -> Dict[int, ZorkGrandInquisitorItems]:
    return {data.archipelago_id: item for item, data in item_data.items()}


def id_to_landmarksanity() -> Dict[int, ZorkGrandInquisitorLandmarksanity]:
    return {landmarksanity.value: landmarksanity for landmarksanity in ZorkGrandInquisitorLandmarksanity}


def id_to_locations() -> Dict[int, ZorkGrandInquisitorLocations]:
    return {
        data.archipelago_id: location
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def id_to_starting_locations() -> Dict[int, ZorkGrandInquisitorStartingLocations]:
    return {
        starting_location.value: starting_location
        for starting_location in ZorkGrandInquisitorStartingLocations
    }


def item_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    item: ZorkGrandInquisitorItems
    data: ZorkGrandInquisitorItemData
    for item, data in item_data.items():
        if data.tags is not None:
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(item.value)

    return {k: v for k, v in groups.items() if len(v)}


def items_with_tag(tag: ZorkGrandInquisitorTags) -> Set[ZorkGrandInquisitorItems]:
    items: Set[ZorkGrandInquisitorItems] = set()

    item: ZorkGrandInquisitorItems
    data: ZorkGrandInquisitorItemData
    for item, data in item_data.items():
        if data.tags is not None and tag in data.tags:
            items.add(item)

    return items


def game_id_to_items() -> Dict[int, ZorkGrandInquisitorItems]:
    mapping: Dict[int, ZorkGrandInquisitorItems] = dict()

    item: ZorkGrandInquisitorItems
    data: ZorkGrandInquisitorItemData
    for item, data in item_data.items():
        if data.statemap_keys is not None:
            for key in data.statemap_keys:
                mapping[key] = item

    return mapping


def location_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    tag: ZorkGrandInquisitorTags
    for tag in ZorkGrandInquisitorTags:
        groups[tag.value] = list()

    location: ZorkGrandInquisitorLocations
    data: ZorkGrandInquisitorLocationData
    for location, data in location_data.items():
        if data.tags is not None:
            for tag in data.tags:
                groups[tag.value].append(location.value)

    return {k: v for k, v in groups.items() if len(v)}


def locations_by_region_for_world(
    world_location_data: Dict[
        Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents],
        ZorkGrandInquisitorLocationData,
    ]
) -> Dict[ZorkGrandInquisitorRegions, List[ZorkGrandInquisitorLocations]]:
    mapping: Dict[ZorkGrandInquisitorRegions, List[ZorkGrandInquisitorLocations]] = dict()

    region: ZorkGrandInquisitorRegions
    for region in ZorkGrandInquisitorRegions:
        mapping[region] = list()

    location: ZorkGrandInquisitorLocations
    data: ZorkGrandInquisitorLocationData
    for location, data in world_location_data.items():
        mapping[data.region].append(location)

    return mapping


def locations_with_tag(tag: ZorkGrandInquisitorTags) -> Set[ZorkGrandInquisitorLocations]:
    location: ZorkGrandInquisitorLocations
    data: ZorkGrandInquisitorLocationData

    return {location for location, data in location_data.items() if data.tags is not None and tag in data.tags}


def prepare_item_data(
    starting_location: ZorkGrandInquisitorStartingLocations,
    goal: ZorkGrandInquisitorGoals,
    deathsanity: ZorkGrandInquisitorDeathsanity,
    landmarksanity: ZorkGrandInquisitorLandmarksanity,
    entrance_randomizer: ZorkGrandInquisitorEntranceRandomizer,
) -> Dict[ZorkGrandInquisitorItems, ZorkGrandInquisitorItemData]:
    transformed_item_data: Dict[ZorkGrandInquisitorItems, ZorkGrandInquisitorItemData] = dict()

    # Filter items
    item: ZorkGrandInquisitorItems
    data: ZorkGrandInquisitorItemData
    for item, data in item_data.items():
        # Filter here...
        transformed_item_data[item] = data

    # Apply transformations
    items_to_make_filler: Set[ZorkGrandInquisitorItems] = set()
    items_to_make_deprioritized_skip_balancing: Set[ZorkGrandInquisitorItems] = set()

    for context in (starting_location, goal, deathsanity, landmarksanity):
        if item_data_transforms[context] is not None:
            transform: ZorkGrandInquisitorItemTransforms
            items: Tuple[ZorkGrandInquisitorItems, ...]
            for transform, items in item_data_transforms[context].items():
                if transform == ZorkGrandInquisitorItemTransforms.MAKE_FILLER:
                    if context == starting_location:
                        if entrance_randomizer != ZorkGrandInquisitorEntranceRandomizer.DISABLED:
                            continue

                    item: ZorkGrandInquisitorItems
                    for item in items:
                        items_to_make_filler.add(item)
                elif transform == ZorkGrandInquisitorItemTransforms.MAKE_DEPRIORITIZED_SKIP_BALANCING:
                    item: ZorkGrandInquisitorItems
                    for item in items:
                        items_to_make_deprioritized_skip_balancing.add(item)

    item: ZorkGrandInquisitorItems
    for item in items_to_make_filler:
        transformed_item_data[item] = transformed_item_data[item]._replace(
            classification=ItemClassification.filler
        )

    for item in items_to_make_deprioritized_skip_balancing:
        transformed_item_data[item] = transformed_item_data[item]._replace(
            classification=ItemClassification.progression_deprioritized_skip_balancing
        )

    return transformed_item_data


def prepare_location_data(
    starting_location: ZorkGrandInquisitorStartingLocations,
    goal: ZorkGrandInquisitorGoals,
    deathsanity: ZorkGrandInquisitorDeathsanity,
    landmarksanity: ZorkGrandInquisitorLandmarksanity,
) -> Dict[
    Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents], ZorkGrandInquisitorLocationData
]:
    transformed_location_data: Dict[
        Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents], ZorkGrandInquisitorLocationData
    ] = dict()

    # Filter locations
    location: Union[ZorkGrandInquisitorLocations, ZorkGrandInquisitorEvents]
    data: ZorkGrandInquisitorLocationData
    for location, data in location_data.items():
        # Filter here...
        transformed_location_data[location] = data

    # Apply transformations
    locations_to_remove: List[ZorkGrandInquisitorLocations] = list()

    for context in (starting_location, goal, deathsanity, landmarksanity):
        if location_data_transforms[context] is not None:
            transform: ZorkGrandInquisitorLocationTransforms
            locations: Tuple[ZorkGrandInquisitorLocations, ...]
            for transform, locations in location_data_transforms[context].items():
                if transform == ZorkGrandInquisitorLocationTransforms.REMOVE:
                    location: ZorkGrandInquisitorLocations
                    for location in locations:
                        locations_to_remove.append(location)

    location: ZorkGrandInquisitorLocations
    for location in locations_to_remove:
        if location in transformed_location_data:
            del transformed_location_data[location]

    return transformed_location_data


def entrances_by_region_for_world(
    entrance_rule_data: EntranceRuleData
) -> Dict[ZorkGrandInquisitorRegions, List[Entrance]]:
    entrances_by_region: Dict[ZorkGrandInquisitorRegions, List[Entrance]] = {
        ZorkGrandInquisitorRegions.ANYWHERE: list(),
        ZorkGrandInquisitorRegions.ENDGAME: list(),
    }

    region_from: ZorkGrandInquisitorRegions
    region_to: ZorkGrandInquisitorRegions
    for region_from, region_to in entrance_rule_data.keys():
        if region_from not in entrances_by_region:
            entrances_by_region[region_from] = list()

        entrances_by_region[region_from].append((region_from, region_to))

    return entrances_by_region


def generate_universal_tracker_location_data() -> None:
    universal_tracker_data: List[Dict[str, Any]] = [
        {
            "name": "Zork Grand Inquisitor",
            "children": list()
        }
    ]

    location_size: int = 24
    location_size_with_margin: int = int(location_size * 1.25)

    location_group: str
    locations: Tuple[ZorkGrandInquisitorLocations]
    for location_group, locations in tracker_location_groups.items():
        location_group_configuration: Tuple[int, int, bool, int] = tracker_location_group_configuration[location_group]

        x_offset: int = location_group_configuration[0]
        y_offset: int = location_group_configuration[1]
        is_left_to_right: bool = location_group_configuration[2]
        maximum_locations_per_row: int = location_group_configuration[3]
        count: int = 1
        overflows: int = 0

        if not is_left_to_right:
            locations = tuple(reversed(locations))

        i: int
        location: ZorkGrandInquisitorLocations
        for i, location in enumerate(locations):
            universal_tracker_data[0]["children"].append(
                {
                    "name": location.value,
                    "map_locations": [
                        {
                            "map": "map",
                            "x": x_offset,
                            "y": y_offset,
                            "size": location_size,
                            "border_thickness": 2,
                        }
                    ],
                    "sections": [
                        {
                            "name": location.value,
                        }
                    ]
                }
            )

            count += 1

            if count > maximum_locations_per_row:
                overflows += 1
                count = 1

                x_offset = location_group_configuration[0]
                y_offset = location_group_configuration[1] + (location_size_with_margin * overflows)
            else:
                if is_left_to_right:
                    x_offset += location_size_with_margin
                else:
                    x_offset -= location_size_with_margin

    with open("worlds/zork_grand_inquisitor/ut/locations/locations.json", "w") as f:
        json.dump(universal_tracker_data, f, indent=4)

from typing import Dict, List

from .data.item_data import PeggleNightsItemData, item_data
from .data.location_data import PeggleNightsLocationData, location_data

from .enums import (
    PeggleNightsAPGoals,
    PeggleNightsAPMasterSelectionModes,
    PeggleNightsAPRequirementModes,
    PeggleNightsAPTags,
)


def id_to_goals() -> Dict[int, PeggleNightsAPGoals]:
    return {goal.value: goal for goal in PeggleNightsAPGoals}


def id_to_items() -> Dict[int, str]:
    return {data.archipelago_id: item for item, data in item_data.items()}


def id_to_locations() -> Dict[int, str]:
    return {
        data.archipelago_id: location
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def id_to_master_selection_modes() -> Dict[int, PeggleNightsAPMasterSelectionModes]:
    return {
        mode.value: mode for mode in PeggleNightsAPMasterSelectionModes
    }


def id_to_requirement_modes() -> Dict[int, PeggleNightsAPRequirementModes]:
    return {
        mode.value: mode for mode in PeggleNightsAPRequirementModes
    }


def item_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    item: str
    data: PeggleNightsItemData
    for item, data in item_data.items():
        if data.tags is not None:
            tag: PeggleNightsAPTags
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(item)

    return {k: v for k, v in groups.items() if len(v)}


def item_names_to_id() -> Dict[str, int]:
    return {item: data.archipelago_id for item, data in item_data.items()}


def items_with_tag(tag: PeggleNightsAPTags) -> List[str]:
    item: str
    data: PeggleNightsItemData

    return [item for item, data in item_data.items() if data.tags is not None and tag in data.tags]


def location_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    location: str
    data: PeggleNightsLocationData
    for location, data in location_data.items():
        if data.tags is not None:
            tag: PeggleNightsAPTags
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(location)

    return {k: v for k, v in groups.items() if len(v)}


def location_names_to_id() -> Dict[str, int]:
    return {
        location: data.archipelago_id
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def locations_with_tag(tag: PeggleNightsAPTags) -> List[str]:
    location: str
    data: PeggleNightsLocationData

    return [location for location, data in location_data.items() if data.tags is not None and tag in data.tags]

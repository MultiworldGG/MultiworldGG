from typing import Dict, List

from .data.item_data import PinballFX3ItemData, item_data
from .data.location_data import PinballFX3LocationData, location_data
from .data.mapping_data import dlc_to_tables

from .enums import (
    PinballFX3APExcludeHighTierChallengeStars,
    PinballFX3APGoals,
    PinballFX3APRequirementModes,
    PinballFX3APTags,
    PinballFX3DLC,
    PinballFX3Tables,
)


def generate_dlc_table_strings() -> List[str]:
    table_strings = list()

    dlc: PinballFX3DLC
    tables: List[PinballFX3Tables]
    for dlc, tables in dlc_to_tables.items():
        table: PinballFX3Tables
        for table in tables:
            table_strings.append(f"[{dlc.value}] {table.value}")

    return table_strings


def id_to_exclude_high_tier_challenge_stars() -> Dict[int, PinballFX3APExcludeHighTierChallengeStars]:
    return {option.value: option for option in PinballFX3APExcludeHighTierChallengeStars}


def id_to_goals() -> Dict[int, PinballFX3APGoals]:
    return {goal.value: goal for goal in PinballFX3APGoals}


def id_to_items() -> Dict[int, str]:
    return {data.archipelago_id: item for item, data in item_data.items()}


def id_to_locations() -> Dict[int, str]:
    return {
        data.archipelago_id: location
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def id_to_requirement_modes() -> Dict[int, PinballFX3APRequirementModes]:
    return {mode.value: mode for mode in PinballFX3APRequirementModes}


def item_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    item: str
    data: PinballFX3ItemData
    for item, data in item_data.items():
        if data.tags is not None:
            tag: PinballFX3APTags
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(item)

    return {k: v for k, v in groups.items() if len(v)}


def item_names_to_id() -> Dict[str, int]:
    return {item: data.archipelago_id for item, data in item_data.items()}


def items_with_tag(tag: PinballFX3APTags) -> List[str]:
    item: str
    data: PinballFX3ItemData

    return [item for item, data in item_data.items() if data.tags is not None and tag in data.tags]


def location_groups() -> Dict[str, List[str]]:
    groups: Dict[str, List[str]] = dict()

    location: str
    data: PinballFX3LocationData
    for location, data in location_data.items():
        if data.tags is not None:
            tag: PinballFX3APTags
            for tag in data.tags:
                groups.setdefault(tag.value, list()).append(location)

    return {k: v for k, v in groups.items() if len(v)}


def location_names_to_id() -> Dict[str, int]:
    return {
        location: data.archipelago_id
        for location, data in location_data.items()
        if data.archipelago_id is not None
    }


def locations_with_tag(tag: PinballFX3APTags) -> List[str]:
    location: str
    data: PinballFX3LocationData

    return [location for location, data in location_data.items() if data.tags is not None and tag in data.tags]

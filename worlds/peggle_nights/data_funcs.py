from typing import Any, Dict, List, Tuple

from .data.item_data import PeggleNightsItemData, item_data
from .data.location_data import PeggleNightsLocationData, location_data

from .enums import (
    PeggleNightsAPGoals,
    PeggleNightsAPItems,
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


def location_access_rule_for(location: str, player: int) -> str:
    data: PeggleNightsLocationData = location_data[location]

    if data.requirements is None:
        return "lambda state: True"

    lambda_string: str = "lambda state: "

    i: int
    requirement: Tuple[Any]
    for i, requirement in enumerate(data.requirements):
        if isinstance(requirement[0], PeggleNightsAPItems):
            lambda_string += f"state.has(\"{requirement[0].value}\", {player}, {requirement[1]})"
        elif isinstance(requirement[0], tuple):
            lambda_string += "("

            ii: int
            sub_requirement: tuple[Any]
            for ii, sub_requirement in enumerate(requirement):
                lambda_string += f"state.has(\"{sub_requirement[0].value}\", {player}, {sub_requirement[1]})"

                if ii < len(requirement) - 1:
                    lambda_string += " or "

            lambda_string += ")"

        if i < len(data.requirements) - 1:
            lambda_string += " and "

    return lambda_string

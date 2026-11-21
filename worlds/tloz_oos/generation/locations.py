from typing import Any

from BaseClasses import LocationProgressType

from ..data.constants import (
    ESSENCES,
    FREESTANDING_LOCATIONS,
    LOCATION_GROUPS,
    RUPEE_OLD_MAN_LOCATIONS,
    SCRUB_LOCATIONS,
    SECRETS,
    SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS,
    TRADE_LOCATIONS,
)
from ..options import (
    OracleOfSeasonsOldMenShuffle,
)
from ..world import OracleOfSeasonsWorld


def location_is_active(world: OracleOfSeasonsWorld, location_name: str, location_data: dict[str, Any]) -> Any:
    if not location_data.get("conditional", False):
        return True

    region_id = location_data["region_id"]
    if region_id == "advance shop":
        return world.options.advance_shop
    if location_name in SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS:
        return world.options.shuffle_golden_ore_spots
    if location_name in RUPEE_OLD_MAN_LOCATIONS:
        return world.options.shuffle_old_men == OracleOfSeasonsOldMenShuffle.option_turn_into_locations
    if location_name in SCRUB_LOCATIONS:
        return world.options.shuffle_business_scrubs
    if location_name.startswith("Gasha Nut #"):
        return int(location_name[11:]) <= world.options.deterministic_gasha_locations
    if location_name in FREESTANDING_LOCATIONS and not world.options.freestanding:
        return False
    if location_name == "Horon Village: Item Inside Maku Tree (3+ Essences)":
        return len(world.essences_in_game) >= 3
    if location_name == "Horon Village: Item Inside Maku Tree (5+ Essences)":
        return len(world.essences_in_game) >= 5
    if location_name == "Horon Village: Item Inside Maku Tree (7+ Essences)":
        return len(world.essences_in_game) >= 7
    if location_name in TRADE_LOCATIONS and not world.options.trade_sequence:
        return False
    if location_name in SECRETS:
        return world.options.secret_locations
    if location_name in LOCATION_GROUPS["D11"]:
        return world.options.linked_heros_cave
    if "owl_id" in location_data:
        return world.options.bird_hint.owl()
    if location_name.startswith("Maple Rare Drop"):
        # Currently disabled
        return False
    return True


def exclude_locations_automatically(world: OracleOfSeasonsWorld) -> None:
    locations_to_exclude = set()
    if world.options.freestanding:
        # If goal essence requirement is set to a specific value, prevent essence-bound checks which require more
        # essences than this goal to hold anything of value
        if world.options.required_essences < 7 <= len(world.essences_in_game):
            locations_to_exclude.add("Horon Village: Item Inside Maku Tree (7+ Essences)")
            if world.options.required_essences < 5 <= len(world.essences_in_game):
                locations_to_exclude.add("Horon Village: Item Inside Maku Tree (5+ Essences)")
                if world.options.required_essences < 3 <= len(world.essences_in_game):
                    locations_to_exclude.add("Horon Village: Item Inside Maku Tree (3+ Essences)")
    if world.options.required_essences < world.options.treehouse_old_man_requirement:
        locations_to_exclude.add("Holodrum Plain: Old Man in Treehouse")

    # If dungeons without essence need to be excluded, do it if conditions are met
    if world.options.exclude_dungeons_without_essence and not world.options.shuffle_essences:
        for i, essence_name in enumerate(ESSENCES):
            if essence_name not in world.essences_in_game:
                locations_to_exclude.update(world.location_name_groups[f"D{i + 1}"])

    # Don't exclude the dungeon scrubs, since they don't exist
    if not world.options.shuffle_business_scrubs:
        locations_to_exclude.difference_update(SCRUB_LOCATIONS)

    if world.options.randomize_ai:
        locations_to_exclude.add("Western Coast: Black Beast's Chest")

    for name in locations_to_exclude:
        world.get_location(name).progress_type = LocationProgressType.EXCLUDED

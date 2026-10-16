from __future__ import annotations

from collections import Counter

from .minor_caches import (
    MINOR_CACHE_FAMILY_BY_LOCATION,
    MINOR_CACHE_REWARD_BY_LOCATION,
)
from .minor_pickups import MINOR_PICKUP_REWARD_BY_LOCATION, SCRIPTED_MINOR_REWARDS
from .locations import canonicalize_location_name


# Scripted Beast Shard rewards bypass the generic CollectableItemPickup and
# minor-cache paths. They still use the Beast Shard family and its
# beast_shard_randomization option.
SCRIPTED_BEAST_SHARD_REWARD_BY_LOCATION: dict[str, str] = {
    "Marrowmaw - Beast Shard": "Beast Shard",
    "Craggler - Beast Shard": "Beast Shard",
    "Moorwing - Beast Shard": "Beast Shard",
    "Pilgrim's Rest - Beast Shard": "Beast Shard",
    "Memorium - Beast Shard": "Beast Shard",
    "Sprintmaster - Beast Shard": "Beast Shard",
}


# Definition order determines YAML and documentation presentation as well as
# the order of family-specific item-pool lanes.
MINOR_FAMILY_DEFINITIONS: tuple[
    tuple[str, str, str, str],
    ...,
] = (
    (
        "frayed_rosary_string",
        "frayed_rosary_string_randomization",
        "Frayed Rosary String",
        "Frayed Rosary String",
    ),
    (
        "rosary_string",
        "rosary_string_randomization",
        "Rosary String",
        "Rosary String",
    ),
    (
        "rosary_necklace",
        "rosary_necklace_randomization",
        "Rosary Necklace",
        "Rosary Necklace",
    ),
    (
        "heavy_rosary_necklace",
        "heavy_rosary_necklace_randomization",
        "Heavy Rosary Necklace",
        "Heavy Rosary Necklace",
    ),
    (
        "pale_rosary_necklace",
        "pale_rosary_necklace_randomization",
        "Pale Rosary Necklace",
        "Pale Rosary Necklace",
    ),
    (
        "shard_bundle",
        "shard_bundle_randomization",
        "Shard Bundle",
        "Shard Bundle",
    ),
    (
        "beast_shard",
        "beast_shard_randomization",
        "Beast Shard",
        "Beast Shard",
    ),
    (
        "pristine_core",
        "pristine_core_randomization",
        "Pristine Core",
        "Pristine Core",
    ),
    (
        "rosary_cache",
        "rosary_cache_randomization",
        "Rosary Cache",
        "Rosaries (10)",
    ),
    (
        "shell_shard_cache",
        "shell_shard_cache_randomization",
        "Shell Shard Cache",
        "Shell Shards (10)",
    ),
)

MINOR_FAMILY_KEYS: tuple[str, ...] = tuple(
    family_key
    for family_key, _option_name, _display_name, _reward_name
    in MINOR_FAMILY_DEFINITIONS
)
MINOR_FAMILY_OPTION_BY_KEY: dict[str, str] = {
    family_key: option_name
    for family_key, option_name, _display_name, _reward_name
    in MINOR_FAMILY_DEFINITIONS
}
MINOR_FAMILY_DISPLAY_NAME_BY_KEY: dict[str, str] = {
    family_key: display_name
    for family_key, _option_name, display_name, _reward_name
    in MINOR_FAMILY_DEFINITIONS
}
MINOR_FAMILY_REWARD_NAME_BY_KEY: dict[str, str] = {
    family_key: reward_name
    for family_key, _option_name, _display_name, reward_name
    in MINOR_FAMILY_DEFINITIONS
}
MINOR_FAMILY_KEY_BY_REWARD_NAME: dict[str, str] = {
    reward_name: family_key
    for family_key, reward_name in MINOR_FAMILY_REWARD_NAME_BY_KEY.items()
}
MINOR_FAMILY_KEY_BY_REWARD_NAME.update({
    reward_name: MINOR_CACHE_FAMILY_BY_LOCATION[location_name]
    for location_name, reward_name in MINOR_CACHE_REWARD_BY_LOCATION.items()
})

MINOR_REWARD_BY_LOCATION: dict[str, str] = {
    **SCRIPTED_MINOR_REWARDS,
    **{
        canonicalize_location_name(location_name): reward_name
        for location_name, reward_name in MINOR_PICKUP_REWARD_BY_LOCATION.items()
    },
    **{
        canonicalize_location_name(location_name): reward_name
        for location_name, reward_name in MINOR_CACHE_REWARD_BY_LOCATION.items()
    },
    **{
        canonicalize_location_name(location_name): reward_name
        for location_name, reward_name
        in SCRIPTED_BEAST_SHARD_REWARD_BY_LOCATION.items()
    },
}
MINOR_REWARD_COUNTS: dict[str, int] = dict(
    Counter(MINOR_REWARD_BY_LOCATION.values())
)
MINOR_FAMILY_BY_LOCATION: dict[str, str] = {
    location_name: MINOR_FAMILY_KEY_BY_REWARD_NAME[reward_name]
    for location_name, reward_name in MINOR_REWARD_BY_LOCATION.items()
}
MINOR_FAMILY_LOCATION_NAMES: dict[str, tuple[str, ...]] = {
    family_key: tuple(
        location_name
        for location_name, location_family in
        MINOR_FAMILY_BY_LOCATION.items()
        if location_family == family_key
    )
    for family_key in MINOR_FAMILY_KEYS
}
MINOR_FAMILY_REWARD_COUNTS: dict[str, dict[str, int]] = {
    family_key: dict(
        Counter(
            MINOR_REWARD_BY_LOCATION[location_name]
            for location_name in location_names
        )
    )
    for family_key, location_names in MINOR_FAMILY_LOCATION_NAMES.items()
}

MINOR_FAMILY_CATEGORY_PREFIX = "Resource:"
MINOR_FAMILY_CATEGORIES: tuple[str, ...] = tuple(
    MINOR_FAMILY_CATEGORY_PREFIX + family_key
    for family_key in MINOR_FAMILY_KEYS
)


def get_minor_family_category(family_key: str) -> str:
    if family_key not in MINOR_FAMILY_OPTION_BY_KEY:
        raise ValueError(f"Unknown minor pickup family: {family_key!r}")
    return MINOR_FAMILY_CATEGORY_PREFIX + family_key


def get_minor_family_category_for_location(
    location_name: str,
) -> str:
    try:
        family_key = MINOR_FAMILY_BY_LOCATION[location_name]
    except KeyError as exc:
        raise ValueError(
            f"No minor pickup family for {location_name!r}."
        ) from exc
    return get_minor_family_category(family_key)


def get_base_randomization_category(category: str) -> str:
    if category.startswith(MINOR_FAMILY_CATEGORY_PREFIX):
        return "Resource"
    return category

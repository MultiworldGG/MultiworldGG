from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass, field
from itertools import count
from typing import Any, ClassVar

from rule_builder.options import OptionFilter

BASE_ID = 77_700_000
_LOCATION_IDS = count(BASE_ID + 1)


@dataclass(frozen=True)
class Rac5Categories:
    """String constants for Rac5Locations.categories tags, so location definitions can't
    typo a category name and silently drop out of its LocationView/region-order grouping."""

    TITANIUM_BOLT = "titanium_bolt"
    ARMOUR_PICKUP = "armour_pickup"
    ARMOUR_SET_CHECK = "armour_set_check"
    BOSS = "boss"
    CHALLENGE = "challenge"
    CHALLENGE_MODE_1_ARMOUR = "challenge_mode_1_armour"
    CHALLENGE_MODE_1_ARMOUR_SET = "challenge_mode_1_armour_set"
    CHALLENGE_MODE_2_ARMOUR = "challenge_mode_2_armour"
    CHALLENGE_MODE_2_ARMOUR_SET = "challenge_mode_2_armour_set"
    CHALLENGE_MODE_MAX_LEVEL = "challenge_mode_max_level"
    CHALLENGE_MODE_MOD = "challenge_mode_mod"
    CHALLENGE_MODE_NANOTECH_LEVEL = "challenge_mode_nanotech_level"
    CHALLENGE_MODE_RYNO = "challenge_mode_ryno"
    CHALLENGE_MODE_SUB_MAX_LEVEL = "challenge_mode_sub_max_level"
    CHALLENGE_MODE_WEAPON_LEVEL = "challenge_mode_weapon_level"
    CLANK_CHALLENGE_SKILL_POINT = "clank_challenge_skill_point"
    CUTSCENE = "cutscene"
    EASY_SKILL_POINT = "easy_skill_point"
    EXTRA_SKYBOARD = "extra_skyboard"
    GADGET_PICKUP = "gadget_pickup"
    GADGET_VENDOR = "gadget_vendor"
    HARD_SKILL_POINT = "hard_skill_point"
    MISSION = "mission"
    NANOTECH_LEVEL = "nanotech_level"
    NG_PLUS_ARMOUR_SET = "ng_plus_armour_set"
    NG_PLUS_WEAPON_LEVEL = "ng_plus_weapon_level"
    SHRINK_RAY_SKIP = "shrink_ray_skip"
    SKILL_POINT = "skill_point"
    SKYBOARD_CHALLENGE_SKILL_POINT = "skyboard_challenge_skill_point"
    SKYBOARD_ITEM = "skyboard_item"
    STORY_MISSION = "story_mission"
    ALL_CLANK = "all_clank"
    WEAPON_LEVEL = "weapon_level"
    WEAPON_MAX_LEVEL = "weapon_max_level"
    WEAPON_MOD_VENDOR = "weapon_mod_vendor"
    WEAPON_SUB_MAX_LEVEL = "weapon_sub_max_level"
    WEAPON_TITAN_VENDOR = "weapon_titan_vendor"
    WEAPON_VENDOR = "weapon_vendor"


REGION_CATEGORY_ORDER = (
    Rac5Categories.TITANIUM_BOLT,
    Rac5Categories.ARMOUR_PICKUP,
    Rac5Categories.BOSS,
    Rac5Categories.GADGET_PICKUP,
    Rac5Categories.WEAPON_VENDOR,
    Rac5Categories.GADGET_VENDOR,
    Rac5Categories.WEAPON_TITAN_VENDOR,
    Rac5Categories.STORY_MISSION,
    Rac5Categories.CUTSCENE,
    Rac5Categories.EASY_SKILL_POINT,
    Rac5Categories.HARD_SKILL_POINT,
    Rac5Categories.CLANK_CHALLENGE_SKILL_POINT,
    Rac5Categories.SKYBOARD_CHALLENGE_SKILL_POINT,
    Rac5Categories.WEAPON_MOD_VENDOR,
    Rac5Categories.CHALLENGE,
    Rac5Categories.ALL_CLANK,
    Rac5Categories.SKYBOARD_ITEM,
    Rac5Categories.EXTRA_SKYBOARD,
    Rac5Categories.SHRINK_RAY_SKIP,
    Rac5Categories.ARMOUR_SET_CHECK,
    Rac5Categories.WEAPON_MAX_LEVEL,
    Rac5Categories.CHALLENGE_MODE_MAX_LEVEL,
    Rac5Categories.WEAPON_SUB_MAX_LEVEL,
    Rac5Categories.CHALLENGE_MODE_SUB_MAX_LEVEL,
    Rac5Categories.NANOTECH_LEVEL,
)


@dataclass(frozen=True, slots=True)
class LocationOptions:
    """All availability requirements for one location, evaluated against world options."""

    requirements: tuple[OptionFilter, ...] = ()
    weapon: str | None = None
    challenge_group: str | None = None
    nanotech_level: int | None = None

    def __call__(self, options) -> bool:
        if not all(requirement.check(options) for requirement in self.requirements):
            return False
        if self.weapon is not None and self.weapon not in options.enabled_weapons.value:
            return False
        if self.challenge_group is not None and self.challenge_group not in options.clank_challenge_groups.value:
            return False
        if self.nanotech_level is not None:
            interval = options.nanotech_level_interval.value
            return (
                interval > 0
                and self.nanotech_level % interval == 0
                and self.nanotech_level <= options.nanotech_level_max.value
            )
        return True


@dataclass(frozen=True)
class Rac5CompletionSources:
    """String constants for Completion.source — must name a field on LocationObservation
    (observation.py), which `getattr(observation, source)` reads."""

    BOLT_BITS = "bolt_bits"
    SKILL_BITS = "skill_bits"
    MISSIONS = "missions"
    EVENTS = "events"
    ARMOUR = "armour"
    CHALLENGES = "challenges"
    SKYBOARD = "skyboard"
    WEAPON_LEVELS = "weapon_levels"
    NANOTECH_LEVELS = "nanotech_levels"


@dataclass(frozen=True, slots=True)
class Completion:
    """Evaluate a decoded observation without performing emulator I/O."""

    source: str
    key: Any
    mask: int = 0
    planet_id: int | None = None
    minimum: int | None = None
    increasing: bool = False

    def __call__(self, observation) -> bool:
        if self.planet_id is not None and observation.planet_id != self.planet_id:
            return False
        value = getattr(observation, self.source)
        if self.minimum is not None:
            return value.get(self.key, 0) >= self.minimum
        if self.increasing:
            return value.get(self.key, 0) > observation.previous.get(self.key, 0)
        if self.mask:
            if self.key is not None:
                value = value.get(self.key, 0)
            return bool(value & self.mask)
        return self.key in value


@dataclass(frozen=True, slots=True)
class ArmourSetCompletion:
    chestplate: int | None = None
    helmet: int | None = None
    gloves: int | None = None
    boots: int | None = None
    source: ClassVar[str] = "armour_sets"

    def required_mask(self):
        return sum(1 << (value - 1) for value in {self.chestplate, self.helmet, self.gloves, self.boots} - {None})

    def is_unlocked(self, unlocks):
        required = self.required_mask()
        return required & unlocks.owned_mask() == required

    def matches(self, equipped):
        if equipped is None:
            return False
        return all(
            required is None or all(getattr(equipped, field) == required for field in fields)
            for required, fields in (
                (self.chestplate, ("chestplate",)),
                (self.helmet, ("helmet",)),
                (self.gloves, ("gloves_left", "gloves_right")),
                (self.boots, ("boots_left", "boots_right")),
            )
        )

    def __call__(self, observation):
        return self.matches(observation.equipped)


@dataclass(frozen=True, slots=True)
class Rac5Locations:
    name: str
    planet: str
    rule: Callable
    completed: Callable
    code: int | None = None  # None takes the next sequential ID; pass one to pin a location added after the originals.
    options: LocationOptions | None = None
    categories: frozenset[str] = frozenset()
    weapon: str | None = None
    gadget: str | None = None
    mod_slot: str | None = None
    level: int | None = None
    reload_planet: int | None = None
    grants_location: str | None = None
    native_planets: tuple[int, ...] = ()
    check_order: int = 0
    definition_order: int = 0  # Preserve generation and reporting order when grouping records by planet.

    def __post_init__(self) -> None:
        if self.code is None:
            object.__setattr__(self, "code", next(_LOCATION_IDS))

    @property
    def region(self) -> str:
        return self.planet

    def available(self, options) -> bool:
        return self.options is None or self.options(options)

    @property
    def region_order(self) -> int:
        return next(index for index, category in enumerate(REGION_CATEGORY_ORDER) if category in self.categories)


class LocationView(Mapping):
    """Read-only projection of the canonical records; no copied location dictionaries."""

    def __init__(
        self,
        locations,
        predicate=lambda location: True,
        key=lambda location: location.name,
        value=lambda location: location,
    ):
        self.locations = locations
        self.predicate, self.key, self.value = predicate, key, value

    def items(self):
        return ((self.key(location), self.value(location)) for location in self.locations if self.predicate(location))

    def values(self):
        return (value for _, value in self.items())

    def __iter__(self):
        return (key for key, _ in self.items())

    def __len__(self):
        return sum(1 for _ in self)

    def __getitem__(self, key):
        for candidate, value in self.items():
            if candidate == key:
                return value
        raise KeyError(key)

    def __or__(self, other):
        return dict(self.items()) | dict(other)

    def __ror__(self, other):
        return dict(other) | dict(self.items())


class FlatLocationView(LocationView):
    def items(self):
        return (
            (key, self.value(location))
            for location in self.locations
            if self.predicate(location)
            for key in self.key(location)
        )

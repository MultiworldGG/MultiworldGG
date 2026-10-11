from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SkillPoint:
    planet_id: int
    bit: int
    region: str

    @property
    def mask(self) -> int:
        return 1 << self.bit


from ...locations.model import LocationView
from ...locations.shared import LOCATIONS

SKILL_POINTS = LocationView(
    LOCATIONS,
    lambda location: location.completed.source == "skill_bits",
    value=lambda location: SkillPoint(
        location.native_planets[0], location.completed.mask.bit_length() - 1, location.planet
    ),
)
HARD_SKILL_POINTS = frozenset(location.name for location in LOCATIONS if "hard_skill_point" in location.categories)
CLANK_CHALLENGE_SKILL_POINTS = frozenset(
    location.name for location in LOCATIONS if "clank_challenge_skill_point" in location.categories
)
SKYBOARD_CHALLENGE_SKILL_POINTS = frozenset(
    location.name for location in LOCATIONS if "skyboard_challenge_skill_point" in location.categories
)
SKILL_POINT_BY_PLANET_AND_MASK = LocationView(
    LOCATIONS,
    lambda location: location.completed.source == "skill_bits",
    key=lambda location: (location.native_planets[0], location.completed.mask),
    value=lambda location: location.name,
)
LOCATION_SKILL_POINTS = LocationView(
    LOCATIONS,
    lambda location: location.completed.source == "skill_bits",
    value=lambda location: location.completed.mask,
)

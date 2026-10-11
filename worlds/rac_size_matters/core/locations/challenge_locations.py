from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum, IntFlag

from ...constants import (
    Rac5Planets,
    Rac5SkillPoints,
)
from ...data.challenges import CHALLENGE_GROUP_DERBY, CHALLENGE_GROUP_GADGETBOT, CHALLENGE_GROUP_GADGETBOT_TOSS
from ...locations.model import LocationView
from ...locations.shared import LOCATIONS
from ..address_maps.us_addresses import PLANET_ADDRESSES  # Canonical catalog addresses.

_METALIS_BASE: int = PLANET_ADDRESSES[0x04].clank_challenge_base
_DAYNI_BASE: int = PLANET_ADDRESSES[0x08].clank_challenge_base
_KALIDON_SKY: int = PLANET_ADDRESSES[0x03].skyboard_base
_OO_SKY: int = PLANET_ADDRESSES[0x06].skyboard_base


@dataclass(frozen=True, slots=True)
class ChallengePickup:
    address: int
    name: str
    planet: str


@dataclass(frozen=True, slots=True)
class SkyboardPickup:
    attempted_addr: int
    completed_addr: int  # Four packed two-bit win counters, each saturating at 3.
    mask: SkyboardBit
    name: str
    planet: str


class SkyboardBit(IntFlag):
    # Either bit means at least one win, including a counter value of 2.
    RACE_1 = 0x03
    RACE_2 = 0x0C
    RACE_3 = 0x30
    RACE_4 = 0xC0


class ChallengeSection(IntEnum):
    """The three independently-unlockable clank challenge sections on a planet."""

    DERBY = 0
    GADGETBOT_TOSS = 1
    GADGETBOT = 2


METALIS_CLANK_UNLOCK_ADDR: int = _METALIS_BASE
METALIS_CLANK_UNLOCK_BYTES: bytes = bytes([0x0F, 0x0F, 0x0F])

DAYNI_CLANK_UNLOCK_ADDR: int = _DAYNI_BASE
DAYNI_CLANK_DERBY_UNLOCK_ADDR: int = _DAYNI_BASE
DAYNI_CLANK_GADGETBOT_TOSS_UNLOCK_ADDR: int = _DAYNI_BASE + 1
DAYNI_CLANK_GADGETBOT_UNLOCK_ADDR: int = _DAYNI_BASE + 2
DAYNI_CLANK_UNLOCK_BYTES: bytes = bytes([0x0F, 0x0F, 0x0F])

CLANK_SECTION_UNLOCK_ADDRESSES: dict[str, dict[ChallengeSection, int]] = {
    Rac5Planets.METALIS: {
        ChallengeSection.DERBY: _METALIS_BASE,
        ChallengeSection.GADGETBOT_TOSS: _METALIS_BASE + 1,
        ChallengeSection.GADGETBOT: _METALIS_BASE + 2,
    },
    Rac5Planets.DAYNI_MOON: {
        ChallengeSection.DERBY: _DAYNI_BASE,
        ChallengeSection.GADGETBOT_TOSS: _DAYNI_BASE + 1,
        ChallengeSection.GADGETBOT: _DAYNI_BASE + 2,
    },
}


_CHALLENGES = tuple(
    sorted(
        (location for location in LOCATIONS if location.completed.source == "challenges"),
        key=lambda location: location.check_order,
    )
)
_SKYBOARD = tuple(
    sorted(
        (location for location in LOCATIONS if location.completed.source == "skyboard"),
        key=lambda location: location.check_order,
    )
)


def _pickups(group):
    locations = sorted(
        (location for location in _CHALLENGES if location.options.challenge_group == group),
        key=lambda location: (location.planet != Rac5Planets.METALIS, location.completed.key),
    )
    return [ChallengePickup(location.completed.key, location.name, location.planet) for location in locations]


DERBY_CLANK_PICKUPS = _pickups(CHALLENGE_GROUP_DERBY)
GADGETBOT_TOSS_CLANK_PICKUPS = _pickups(CHALLENGE_GROUP_GADGETBOT_TOSS)
GADGETBOT_CLANK_PICKUPS = _pickups(CHALLENGE_GROUP_GADGETBOT)
CHALLENGE_PICKUPS = [
    ChallengePickup(location.completed.key, location.name, location.planet)
    for location in _CHALLENGES
    if "challenge" in location.categories
]
CHALLENGE_ADDRESS_MAP = LocationView(
    _CHALLENGES,
    lambda location: "challenge" in location.categories,
    key=lambda location: location.completed.key,
    value=lambda location: location.name,
)
ALL_CLANK_ADDRESS_MAP = LocationView(
    _CHALLENGES, key=lambda location: location.completed.key, value=lambda location: location.name
)
COUNT_BASED_CHALLENGE_ADDRS = frozenset(
    location.completed.key for location in _CHALLENGES if location.completed.increasing
)
METALIS_CHALLENGE_NAMES = frozenset(location.name for location in _CHALLENGES if location.planet == Rac5Planets.METALIS)
DAYNI_MOON_CHALLENGE_NAMES = frozenset(
    location.name for location in _CHALLENGES if location.planet == Rac5Planets.DAYNI_MOON
)
GLADIATOR_FAILSAFE = {
    Rac5Planets.METALIS: Rac5SkillPoints.METALIS_GLADIATOR,
    Rac5Planets.DAYNI_MOON: Rac5SkillPoints.DAYNI_MOON_GLADIATOR,
}
CHALLENGE_NAME_TO_GROUP = LocationView(_CHALLENGES, value=lambda location: location.options.challenge_group)
ALL_SKYBOARD_PICKUPS = [
    SkyboardPickup(
        location.completed.key + 1,
        location.completed.key,
        SkyboardBit(location.completed.mask),
        location.name,
        location.planet,
    )
    for location in _SKYBOARD
]
KALIDON_SKYBOARD_PICKUPS = [pickup for pickup in ALL_SKYBOARD_PICKUPS if pickup.planet == Rac5Planets.KALIDON]
OUTPOST_OMEGA_SKYBOARD_PICKUPS = [
    pickup for pickup in ALL_SKYBOARD_PICKUPS if pickup.planet == Rac5Planets.OUTPOST_OMEGA
]
SKYBOARD_ADDRESS_MASK_MAP = LocationView(
    _SKYBOARD,
    key=lambda location: (location.completed.key, location.completed.mask),
    value=lambda location: location.name,
)
# The adjacent byte counts attempts, including losses. Neither byte is an
# unlock bitfield: never write attempts or wins just to make a race available.

CHALLENGE_ONLY_ITEMS: frozenset[str] = frozenset(
    {
        "Polarizer",
        "Sludge Mk9 Gloves",
        "Crystallix Helmet",
        "Crystallix Gloves",
        "Mega Bomb Gloves",
        "Mega Bomb Boots",
        "Electroshock Boots",
    }
)

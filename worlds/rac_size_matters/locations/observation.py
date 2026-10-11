from dataclasses import dataclass, field
from functools import lru_cache

from ..core import address_maps
from ..core.address_maps import SKILL_POINTS_BASE, TITANIUM_BOLT_BASE
from .shared import LOCATIONS


@lru_cache(maxsize=None)
def source_addresses(source):

    return tuple(sorted({location.completed.key for location in LOCATIONS if location.completed.source == source}))


@dataclass(frozen=True, slots=True)
class LocationObservation:
    planet_id: int | None = None
    bolt_bits: int = 0
    skill_bits: int = 0
    missions: dict[int, int] = field(default_factory=dict)
    events: frozenset[str] = frozenset()
    armour: dict[str, int] = field(default_factory=dict)
    challenges: dict[int, int] = field(default_factory=dict)
    previous: dict[int, int] = field(default_factory=dict)
    skyboard: dict[int, int] = field(default_factory=dict)
    weapon_levels: frozenset[tuple[str, int]] = frozenset()
    nanotech_levels: frozenset[int] = frozenset()
    equipped: object | None = None

    @classmethod
    def read_bytes(cls, pine, planet_id, skill_points=False, clank=False, skyboard=False):

        addresses = source_addresses("missions")
        challenges = source_addresses("challenges") if clank else ()
        races = source_addresses("skyboard") if skyboard else ()
        requests = [(4, address_maps.TITANIUM_BOLT_BASE), (1, address_maps.TITANIUM_BOLT_BASE + 4)]
        if skill_points:
            requests += [(4, address_maps.SKILL_POINTS_BASE), (1, address_maps.SKILL_POINTS_BASE + 4)]
        requests += [(2, address_maps.save_address(address)) for address in addresses]
        requests += [(1, address_maps.save_address(address)) for address in (*challenges, *races)]
        values = pine.batch_read(requests)
        if len(values) != len(requests):
            raise ValueError("Incomplete location snapshot")
        offset = 4 if skill_points else 2
        challenge_start = offset + len(addresses)
        race_start = challenge_start + len(challenges)
        return cls(
            planet_id,
            values[0] | values[1] << 32,
            values[2] | values[3] << 32 if skill_points else 0,
            dict(zip(addresses, values[offset:challenge_start], strict=True)),
            challenges=dict(zip(challenges, values[challenge_start:race_start], strict=True)),
            skyboard=dict(zip(races, values[race_start:], strict=True)),
        )

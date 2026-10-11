from typing import TYPE_CHECKING

from ..constants import Rac5Infobots, Rac5Planets
from ..locations import (
    GADGET_PICKUP_LOCATIONS,
    GADGET_VENDOR_LOCATIONS,
    WEAPON_MOD_VENDOR_LOCATIONS,
    WEAPON_VENDOR_LOCATIONS,
)
from .planets import Planets

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld

STARTING_PLANET_CANDIDATES: tuple[str, ...] = (
    Rac5Planets.POKITARU,
    Rac5Planets.RYLLUS,
    Rac5Planets.KALIDON,
    Rac5Planets.METALIS,
    Rac5Planets.OUTPOST_OMEGA,
    Rac5Planets.CHALLAX,
    Rac5Planets.DAYNI_MOON,
)

PLANET_TO_INFOBOT: dict[str, str] = {
    Rac5Planets.POKITARU:      Rac5Infobots.POKITARU,
    Rac5Planets.RYLLUS:        Rac5Infobots.RYLLUS,
    Rac5Planets.KALIDON:       Rac5Infobots.KALIDON,
    Rac5Planets.METALIS:       Rac5Infobots.METALIS,
    Rac5Planets.OUTPOST_OMEGA: Rac5Infobots.OUTPOST_OMEGA,
    Rac5Planets.CHALLAX:       Rac5Infobots.CHALLAX,
    Rac5Planets.DAYNI_MOON:    Rac5Infobots.DAYNI_MOON,
}

PLANET_TO_ID: dict[str, int] = {
    Rac5Planets.POKITARU:      Planets.POKITARU.planet_id,
    Rac5Planets.RYLLUS:        Planets.RYLLUS.planet_id,
    Rac5Planets.KALIDON:       Planets.KALIDON.planet_id,
    Rac5Planets.METALIS:       Planets.METALIS.planet_id,
    Rac5Planets.OUTPOST_OMEGA: Planets.OUTPOST_OMEGA_2.planet_id,
    Rac5Planets.CHALLAX:       Planets.CHALLAX.planet_id,
    Rac5Planets.DAYNI_MOON:    Planets.DAYNI_MOON.planet_id,
}

_WEAPON_LOCATION_NAMES = frozenset(WEAPON_VENDOR_LOCATIONS) | frozenset(WEAPON_MOD_VENDOR_LOCATIONS)
_GADGET_LOCATION_NAMES = frozenset(GADGET_PICKUP_LOCATIONS) | frozenset(GADGET_VENDOR_LOCATIONS)


def _planet_location_weight(world: "RACSizeMatterWorld", planet: str) -> int:
    """Locations available on `planet` under the current options. Weapon/gadget vendor
    locations only count when starting with random weapons/gadgets; weapon level checks
    are excluded entirely since they're all anchored to Pokitaru."""
    region = world.multiworld.get_region(planet, world.player)
    count_weapons = world.options.starting_weapons.value > 0
    count_gadgets = world.options.starting_gadgets.value > 0
    weight = 0
    for location in region.locations:
        if location.name in _WEAPON_LOCATION_NAMES:
            weight += count_weapons
        elif location.name in _GADGET_LOCATION_NAMES:
            weight += count_gadgets
        else:
            weight += 1
    return max(weight, 1)


def choose_starting_planets(world: "RACSizeMatterWorld", weighted: bool, count: int = 2) -> list[str]:
    """Pick `count` distinct planets from STARTING_PLANET_CANDIDATES. weighted=True
    samples by _planet_location_weight; weighted=False samples uniformly at random."""
    candidates = list(STARTING_PLANET_CANDIDATES)
    count = min(count, len(candidates))
    if not weighted:
        return world.random.sample(candidates, count)

    weights = [_planet_location_weight(world, planet) for planet in candidates]
    chosen: list[str] = []
    for _ in range(count):
        [pick] = world.random.choices(candidates, weights=weights, k=1)
        idx = candidates.index(pick)
        chosen.append(candidates.pop(idx))
        weights.pop(idx)
    return chosen

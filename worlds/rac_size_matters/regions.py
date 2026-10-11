from BaseClasses import Region

from .constants import Rac5Planets
from .data.models import RACLocation
from .locations import LOCATIONS, MENU_REGION, PLANET_ORDER
from .locations.quodrona import victory_rule

PLANET_NAMES = PLANET_ORDER
REGION_LOCATIONS = tuple(sorted(LOCATIONS, key=lambda location: location.region_order))


def create_regions(world) -> None:

    player, multiworld = world.player, world.multiworld
    regions = {name: Region(name, player, multiworld) for name in (MENU_REGION, *PLANET_NAMES)}
    for definition in REGION_LOCATIONS:
        if definition.available(world.options):
            region = regions[definition.planet]
            location = RACLocation(player, definition.name, definition.code, region)
            location.rule_factory = definition.rule
            region.locations.append(location)

    quodrona = regions[Rac5Planets.QUODRONA]
    victory = RACLocation(player, "Quodrona Completed", None, quodrona)
    victory.rule_factory = victory_rule
    victory.place_locked_item(world.create_event("Victory"))
    quodrona.locations.append(victory)

    for planet in PLANET_NAMES:
        regions[MENU_REGION].connect(regions[planet], f"To {planet}")
    multiworld.regions += list(regions.values())

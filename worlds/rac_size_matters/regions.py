from BaseClasses import Region

from .data.models import RACItem, RACLocation
from .goals import create_victory
from .locations import LOCATIONS, MENU_REGION, PLANET_ORDER
from .rules.entrances import ENTRANCE_RULES, EVENT_INFOBOT_RULES

PLANET_NAMES = PLANET_ORDER
REGION_LOCATIONS = tuple(sorted(LOCATIONS, key=lambda location: location.region_order))


def create_regions(world) -> None:
    player, multiworld = world.player, world.multiworld
    regions = {name: Region(name, player, multiworld) for name in (MENU_REGION, *PLANET_NAMES)}
    region_locations: dict[str, dict[str, int]] = {name: {} for name in regions}
    for definition in REGION_LOCATIONS:
        if definition.available(world.options):
            region_locations[definition.planet][definition.name] = definition.code
    for name, locations in region_locations.items():
        regions[name].add_locations(locations, RACLocation)

    create_victory(world, regions)

    for event, (region, rule) in EVENT_INFOBOT_RULES.items():
        regions[region].add_event(f"Receive {event}", event, rule, location_type=RACLocation, item_type=RACItem)

    for planet in PLANET_NAMES:
        world.create_entrance(regions[MENU_REGION], regions[planet], ENTRANCE_RULES[planet], f"To {planet}")
    multiworld.regions += list(regions.values())

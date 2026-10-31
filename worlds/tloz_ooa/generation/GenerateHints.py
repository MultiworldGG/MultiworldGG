
from ..data.Hints import *
from ..data.Locations import *
from ..common.patching.text import normalize_text
from ..common.patching.Util import simple_hex
from .. import OracleOfAgesWorld

from BaseClasses import Item

def locations_in_region(region_name: str) -> list[str]:
    hinted_locations = []
    for locName, locData in LOCATIONS_DATA.items():
        if "hint_region" in locData and locData["hint_region"] == region_name:
            hinted_locations.append(locName)
    return hinted_locations

def compute_location_per_region() -> dict[str, list[str]]:
    result = {}
    for region in HINT_REGIONS:
        result[region] = locations_in_region(region)
    return result

def create_region_hints(world: OracleOfAgesWorld) -> list[tuple[str, str | int]]:
    hinted_regions: list[str] = world.random.sample(HINT_REGIONS, k=len(KNOW_IT_ALL_BIRDS_TX))
    hint_data: list[tuple[str, str | int]] = []

    for region in hinted_regions:
        num_locations = 0
        num_progression = 0
        for location_name in locations_in_region(region):
            try:
                location = world.get_location(location_name)
                num_locations += 1
                if location.advancement:
                    num_progression += 1
            except KeyError:
                pass
        ratio = num_progression / num_locations
        if ratio == 0:
            region_type = "Foolish"
        elif ratio == 1:
            region_type = "Golden"
        else:
            region_type = num_progression
        hint_data.append((region, region_type))
    return hint_data


def create_item_hints(world: OracleOfAgesWorld) -> list[Item | None]:
    spheres = world.multiworld.get_spheres()
    non_hintable: dict[int, set[Item]] = {}
    past_items: set[Item] = set()

    for sphere in spheres:
        if len(sphere) == 0:
            break
        current_items = set()
        for location in sphere:
            item = location.item
            assert item is not None
            if item.player == world.player:
                if item.name == "Hint":
                    non_hintable[LOCATIONS_DATA[location.name]["owl_id"]] = past_items
                elif item.advancement and not item.deprioritized and not location.is_event and not location.locked:
                    current_items.add(item)
            past_items.update(current_items)

    hinted_items: dict[int, Item | None] = {}
    random_order_owl = list(range(len(OWL_STATUE_TX)))
    world.random.shuffle(random_order_owl)
    for owl_id in random_order_owl:
        if world.random.randrange(30) == 0:
            hinted_items[owl_id] = None
        if owl_id in non_hintable:
            hintables = past_items.difference(non_hintable[owl_id])
            if not hintables:
                # It was a last-sphere item, take a random one then
                hintables = past_items
        else:
            # Owl is logically unreachable, take a random item
            hintables = past_items
        if hintables:
            hintables_list = sorted(hintables)
            item = world.random.choice(hintables_list)
            hinted_items[owl_id] = item
            past_items.remove(item)
        else:
            hinted_items[owl_id] = None
    return [hinted_items[i] for i in range(len(random_order_owl))]
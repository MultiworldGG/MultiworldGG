from typing import Dict, NamedTuple, TYPE_CHECKING
from BaseClasses import Item
from BaseClasses import ItemClassification as IC
from Options import OptionError
from worlds.phoa.Locations import PhoaLocationData
from . import PhoaOptions

if TYPE_CHECKING:
    from .. import PhoaWorld


class PhoaItem(Item):
    game: str = "Phoenotopia: Awakening"


class PhoaItemData(NamedTuple):
    code: int
    amount: int
    type: IC


# @formatter:off
item_table: Dict[str, PhoaItemData] = {
    "Heart Ruby":               PhoaItemData(3,     3,  IC.useful),
    "Energy Gem":               PhoaItemData(4,     2,  IC.useful),
    "Moonstone":                PhoaItemData(5,     10, IC.filler),
    "Wooden Bat":               PhoaItemData(6,     1,  IC.progression),
    "Composite Bat":            PhoaItemData(7,     1,  IC.useful),
    "Life Saver":               PhoaItemData(14,    1,  IC.progression),
    "Spear Bomb":               PhoaItemData(17,    1,  IC.progression),
    "Treble Shot":              PhoaItemData(28,    1,  IC.progression),
    "Bandit's Flute":           PhoaItemData(29,    1,  IC.progression),
    "Slingshot":                PhoaItemData(30,    1,  IC.progression),
    "Bombs":                    PhoaItemData(31,    1,  IC.progression),
    "Crank Lamp":               PhoaItemData(32,    1,  IC.progression),  # Ignore light requirement option?
    "Sonic Spear":              PhoaItemData(33,    1,  IC.progression),
    "Rocket Boots":             PhoaItemData(34,    1,  IC.progression),
    "Spheralis":                PhoaItemData(35,    1,  IC.progression),
    "Civilian Crossbow":        PhoaItemData(37,    1,  IC.progression),
    "Double Crossbow":          PhoaItemData(38,    1,  IC.progression),
    "Refurbished Crank Lamp":   PhoaItemData(39,    1,  IC.progression),
    "Fishing Rod":              PhoaItemData(40,    1,  IC.useful),
    "Serpent Rod":              PhoaItemData(41,    1,  IC.useful),
    "Kobold Blaster":           PhoaItemData(42,    1,  IC.progression),
    "Neutron Lamp":             PhoaItemData(43,    1,  IC.progression),  # Ignore light requirement option?
    "Remote Bombs":             PhoaItemData(44,    1,  IC.progression),
    "Doki Herb":                PhoaItemData(45,    7,  IC.filler),
    "Pumpkin Muffin":           PhoaItemData(47,    1,  IC.filler),
    "Cooked Toad Leg":          PhoaItemData(49,    1,  IC.filler),
    "Berry Fruit":              PhoaItemData(50,    1,  IC.filler),
    "Perro Egg":                PhoaItemData(52,    3,  IC.filler),
    "Fruit Jam":                PhoaItemData(57,    2,  IC.filler),
    "Potato Lunch":             PhoaItemData(59,    1,  IC.filler),
    "Cheese":                   PhoaItemData(64,    1,  IC.filler),
    "Milk":                     PhoaItemData(67,    2,  IC.filler),
    "Anuri Pearlstone":         PhoaItemData(98,    10, IC.progression),  # Dungeon option?
    "Lunar Frog":               PhoaItemData(99,    1,  IC.filler),
    "Lunar Vase":               PhoaItemData(100,   1,  IC.filler),
    "Dandelion":                PhoaItemData(101,   4,  IC.filler),
    "Panselo Potato":           PhoaItemData(102,   4,  IC.filler),
    "Mystery Meat":             PhoaItemData(112,   18, IC.filler),
    "Song of Ouroboros":        PhoaItemData(124,   1,  IC.progression),
    "GEO Song":                 PhoaItemData(125,   1,  IC.progression),
    "Royal Hymn":               PhoaItemData(126,   1,  IC.progression),
    "Prelude of Panselo":       PhoaItemData(127,   1,  IC.useful),
    "Mysterious Golem Head":    PhoaItemData(166,   1,  IC.filler),
    "Dragon's Scale":           PhoaItemData(185,   1,  IC.filler),
    "Progressive Bat":          PhoaItemData(293,   2,  IC.useful),
    "Progressive Slingshot":    PhoaItemData(294,   2,  IC.progression),
    "Progressive Bombs":        PhoaItemData(295,   2,  IC.progression),
    "Progressive Crank Lamp":   PhoaItemData(296,   2,  IC.progression),  # Ignore light requirement option?
    "Progressive Spear":        PhoaItemData(297,   2,  IC.progression),
    "Progressive Crossbow":     PhoaItemData(298,   2,  IC.progression),
    "Progressive Fishing Rod":  PhoaItemData(299,   2,  IC.useful),
    "5 Rin":                    PhoaItemData(305,   1,  IC.filler),
    "9 Rin":                    PhoaItemData(309,   1,  IC.filler),
    "15 Rin":                   PhoaItemData(315,   3,  IC.filler),
    "20 Rin":                   PhoaItemData(320,   3,  IC.filler),
    "25 Rin":                   PhoaItemData(325,   1,  IC.filler),
    "30 Rin":                   PhoaItemData(330,   1,  IC.filler),
    "35 Rin":                   PhoaItemData(335,   3,  IC.filler),
    "50 Rin":                   PhoaItemData(350,   1,  IC.filler),
}
# @formatter:on

upgrade_groups = [
    ("upgradable_bats", "Progressive Bat", ["Wooden Bat", "Composite Bat"]),
    ("upgradable_tools", "Progressive Slingshot", ["Slingshot", "Treble Shot"]),
    ("upgradable_tools", "Progressive Bombs", ["Bombs", "Remote Bombs"]),
    ("upgradable_tools", "Progressive Crank Lamp", ["Crank Lamp", "Neutron Lamp"]),
    ("upgradable_tools", "Progressive Crossbow", ["Civilian Crossbow", "Double Crossbow"]),
    ("upgradable_tools", "Progressive Fishing Rod", ["Fishing Rod", "Serpent Rod"]),
    ("upgradable_spear", "Progressive Spear", ["Sonic Spear", "Spear Bomb"]),
]

item_inclusion_priority: list[str] = \
    ["Progressive Bat", "Composite Bat", "Progressive Fishing Rod", "Serpent Rod", "Fishing Rod", "Prelude of Panselo",
     "Energy Gem", "Heart Ruby", "Dragon's Scale", "35 Rin", "25 Rin", "20 Rin", "15 Rin", "Pumpkin Muffin",
     "Cooked Toad Leg", "Milk", "Cheese", "Panselo Potato", "Mystery Meat", "Fruit Jam", "Berry Fruit", "Perro Egg",
     "Doki Herb", "Dandelion", "9 Rin", "5 Rin", "Lunar Frog", "Lunar Vase", "Moonstone", "Mysterious Golem Head"]


def get_item_pool(world: "PhoaWorld", locations: dict[str, PhoaLocationData]) -> tuple[list[str], list[str]]:
    local_item_table = dict(item_table)

    # Determine item classifications based on settings
    local_item_table = filter_upgradable_items(local_item_table, world.options)

    # Remove events from locations
    locations = {key: location for key, location in locations.items() if location.vanillaItem}
    location_count = len(locations)

    # Initialize item pools based on classifications
    progressive_items: list[str] = []
    useful_items: list[str] = []

    for item_name, item_data in local_item_table.items():
        if item_data.type == IC.progression or item_name in world.progressive_item_classifications_overrides:
            progressive_items.extend([item_name] * item_data.amount)
        elif item_data.type == IC.useful:
            useful_items.extend([item_name] * item_data.amount)

    # Remove progressive and useful items from the items_from_locations
    upgrade_map = build_upgrade_map(world.options)
    items_from_locations: list[str] = [
        upgrade_map.get(location.vanillaItem, location.vanillaItem)
        for location in locations.values()
    ]

    items_from_locations = [item for item in items_from_locations if item not in set(progressive_items)]
    items_from_locations = [item for item in items_from_locations if item not in set(useful_items)]

    # Filter out the Wooden Bat or a Progressive Bat and add it to precollected items if starting with one
    precollected_items: list[str] = []
    if world.options.start_with_wooden_bat:
        for items in (progressive_items, useful_items):
            for item in items:
                if item in ["Wooden Bat", "Progressive Bat"]:
                    items.remove(item)
                    precollected_items.append(item)
                    break

    # Check whether enough locations are available to place all progressive items
    if len(progressive_items) > location_count:
        raise OptionError(
            f"Not enough progress locations({str(location_count)}) "
            f"to place all progressive items({str(len(progressive_items))})"
        )

    # Sort items on importance
    def sort_by_priority(items, priority_list: list[str]) -> list[str]:
        priority_map = {item: i for i, item in enumerate(priority_list)}
        default_priority = len(priority_list)
        return sorted(items, key=lambda x: priority_map.get(x, default_priority))

    useful_items = sort_by_priority(useful_items, item_inclusion_priority)
    items_from_locations = sort_by_priority(items_from_locations, item_inclusion_priority)

    # Construct the item pool
    item_pool = progressive_items.copy()

    remaining_slots = location_count - len(item_pool)

    item_pool.extend(useful_items[:remaining_slots])
    remaining_slots = location_count - len(item_pool)

    item_pool.extend(items_from_locations[:remaining_slots])
    remaining_slots = location_count - len(item_pool)

    item_pool.extend(world.get_filler_item_name() for _ in range(remaining_slots))

    return item_pool, precollected_items


def filter_upgradable_items(items, options: PhoaOptions) -> dict[str, PhoaItemData]:
    for option, progressive, bases in upgrade_groups:
        if getattr(options, option):
            for base in bases:
                items.pop(base, None)
            continue
        items.pop(progressive, None)

    removal_map = [
        (not options.enable_heart_ruby_locations
         and not options.keep_excluded_status_upgrades_in_item_pool,
         ["Heart Ruby"]),
        (not options.enable_energy_gem_locations
         and not options.keep_excluded_status_upgrades_in_item_pool,
         ["Energy Gem"]),
        (not options.enable_moonstone_locations
         and not options.keep_excluded_status_upgrades_in_item_pool,
         ["Moonstone"]),
    ]

    for condition, names in removal_map:
        if condition:
            for name in names:
                items.pop(name, None)

    return items


def build_upgrade_map(options: PhoaOptions) -> dict[str, str]:
    mapping = {}

    for option, progressive, bases in upgrade_groups:
        if getattr(options, option):
            for base in bases:
                mapping[base] = progressive

    return mapping

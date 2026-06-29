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
    "Heart Ruby":                       PhoaItemData(3,     14, IC.useful),
    "Energy Gem":                       PhoaItemData(4,     9,  IC.useful),
    "Moonstone":                        PhoaItemData(5,     37, IC.filler),
    "Wooden Bat":                       PhoaItemData(6,     1,  IC.progression),
    "Composite Bat":                    PhoaItemData(7,     1,  IC.useful),
    "Sky Vest":                         PhoaItemData(11,    1,  IC.useful),
    "Life Saver":                       PhoaItemData(14,    1,  IC.progression),
    "Tusk Strike":                      PhoaItemData(15,    1,  IC.useful),
    "Spear Bomb":                       PhoaItemData(17,    1,  IC.progression),
    "Treble Shot":                      PhoaItemData(28,    1,  IC.progression),
    "Bandit's Flute":                   PhoaItemData(29,    1,  IC.progression),
    "Slingshot":                        PhoaItemData(30,    1,  IC.progression),
    "Bombs":                            PhoaItemData(31,    1,  IC.progression),
    "Crank Lamp":                       PhoaItemData(32,    1,  IC.progression),  # Ignore light requirement option?
    "Sonic Spear":                      PhoaItemData(33,    1,  IC.progression),
    "Rocket Boots":                     PhoaItemData(34,    1,  IC.progression),
    "Spheralis":                        PhoaItemData(35,    1,  IC.progression),
    "Civilian Crossbow":                PhoaItemData(37,    1,  IC.progression),
    "Double Crossbow":                  PhoaItemData(38,    1,  IC.progression),
    "Refurbished Crank Lamp":           PhoaItemData(39,    1,  IC.progression),
    "Fishing Rod":                      PhoaItemData(40,    1,  IC.useful),
    "Serpent Rod":                      PhoaItemData(41,    1,  IC.useful),
    "Kobold Blaster":                   PhoaItemData(42,    1,  IC.progression),
    "Neutron Lamp":                     PhoaItemData(43,    1,  IC.progression),  # Ignore light requirement option?
    "Remote Bombs":                     PhoaItemData(44,    1,  IC.progression),
    "Doki Herb":                        PhoaItemData(45,    7,  IC.filler),
    "Pumpkin Muffin":                   PhoaItemData(47,    1,  IC.filler),
    "Cooked Toad Leg":                  PhoaItemData(49,    1,  IC.filler),
    "Berry Fruit":                      PhoaItemData(50,    1,  IC.filler),
    "Perro Egg":                        PhoaItemData(52,    4,  IC.filler),
    "Nectear":                          PhoaItemData(53,    13, IC.filler),
    "Honey Brew":                       PhoaItemData(54,    3,  IC.filler),
    "Pooki Jerky":                      PhoaItemData(56,    3,  IC.filler),
    "Fruit Jam":                        PhoaItemData(57,    2,  IC.filler),
    "Canned Beans":                     PhoaItemData(58,    4,  IC.filler),
    "Potato Lunch":                     PhoaItemData(59,    1,  IC.filler),
    "Curry Bento":                      PhoaItemData(61,    1,  IC.filler),
    "Turtle":                           PhoaItemData(63,    1,  IC.filler),
    "Cheese":                           PhoaItemData(64,    2,  IC.filler),
    "Drake Tail":                       PhoaItemData(66,    1,  IC.filler),
    "Milk":                             PhoaItemData(67,    3,  IC.filler),
    "Chocolate":                        PhoaItemData(68,    1,  IC.filler),
    "Raw Meat":                         PhoaItemData(73,    1,  IC.filler),
    "Big Raw Meat":                     PhoaItemData(74,    1,  IC.filler),
    "Prime Fish Fillet":                PhoaItemData(81,    1,  IC.filler),
    "Honey Drop":                       PhoaItemData(89,    2,  IC.filler),
    "Anuri Pearlstone":                 PhoaItemData(98,    10, IC.progression),  # Dungeon option?
    "Lunar Frog":                       PhoaItemData(99,    1,  IC.filler),
    "Lunar Vase":                       PhoaItemData(100,   1,  IC.filler),
    "Dandelion":                        PhoaItemData(101,   4,  IC.filler),
    "Panselo Potato":                   PhoaItemData(102,   4,  IC.filler),
    "Moon Kelp":                        PhoaItemData(104,   1,  IC.filler),
    "Prickle Fruit":                    PhoaItemData(106,   6,  IC.filler),
    "Stink Root":                       PhoaItemData(107,   1,  IC.filler),
    "Ouro Guard Key":                   PhoaItemData(108,   5,  IC.progression),  # Only progressive when option enabled
    "Rubber Ducky":                     PhoaItemData(109,   2,  IC.filler),
    "Ouroboros Proof":                  PhoaItemData(111,   3,  IC.progression),
    "Mystery Meat":                     PhoaItemData(112,   35, IC.filler),
    "Lisa's ID Card":                   PhoaItemData(122,   1,  IC.progression),
    "Bottle of Wine":                   PhoaItemData(123,   1,  IC.progression),
    "Song of Ouroboros":                PhoaItemData(124,   1,  IC.progression),
    "GEO Song":                         PhoaItemData(125,   1,  IC.progression),
    "Royal Hymn":                       PhoaItemData(126,   1,  IC.progression),
    "Prelude of Panselo":               PhoaItemData(127,   1,  IC.useful),
    "GEO Ticket":                       PhoaItemData(140,   1,  IC.filler),
    "Baroque of Battle":                PhoaItemData(129,   1,  IC.useful),
    "Perro":                            PhoaItemData(139,   2,  IC.filler),
    "Antique Pin":                      PhoaItemData(141,   1,  IC.filler),
    "Ouroboros Scroll":                 PhoaItemData(143,   4,  IC.progression),  # Only progressive when option enabled
    "Lunar Drake":                      PhoaItemData(145,   1,  IC.filler),
    "Strange Urn":                      PhoaItemData(161,   1,  IC.filler),
    "Mysterious Golem Head":            PhoaItemData(166,   1,  IC.filler),
    "Saffron Milk":                     PhoaItemData(177,   2,  IC.filler),
    "Vala Bean":                        PhoaItemData(178,   1,  IC.filler),
    "Falafel":                          PhoaItemData(179,   1,  IC.filler),
    "Desert Squash":                    PhoaItemData(180,   1,  IC.filler),
    "Cooked Squash":                    PhoaItemData(181,   1,  IC.filler),
    "Dragon's Scale":                   PhoaItemData(185,   1,  IC.filler),
    "Honey Bun":                        PhoaItemData(205,   3,  IC.filler),
    "Spell of Rejuvenation":            PhoaItemData(216,   1,  IC.useful),
    "Progressive Prelude of Panselo":   PhoaItemData(292,   2,  IC.useful),
    "Progressive Bat":                  PhoaItemData(293,   2,  IC.useful),
    "Progressive Slingshot":            PhoaItemData(294,   2,  IC.progression),
    "Progressive Bombs":                PhoaItemData(295,   2,  IC.progression),
    "Progressive Crank Lamp":           PhoaItemData(296,   2,  IC.progression),  # Ignore light requirement option?
    "Progressive Spear":                PhoaItemData(297,   2,  IC.progression),
    "Progressive Crossbow":             PhoaItemData(298,   2,  IC.progression),
    "Progressive Fishing Rod":          PhoaItemData(299,   2,  IC.useful),
    "1 Rin":                            PhoaItemData(301,   4,  IC.filler),
    "5 Rin":                            PhoaItemData(305,   1,  IC.filler),
    "9 Rin":                            PhoaItemData(309,   1,  IC.filler),
    "15 Rin":                           PhoaItemData(315,   3,  IC.filler),
    "20 Rin":                           PhoaItemData(320,   7,  IC.filler),
    "25 Rin":                           PhoaItemData(325,   6,  IC.filler),
    "30 Rin":                           PhoaItemData(330,   8,  IC.filler),
    "35 Rin":                           PhoaItemData(335,   10, IC.filler),
    "40 Rin":                           PhoaItemData(340,   2,  IC.filler),
    "45 Rin":                           PhoaItemData(345,   2,  IC.filler),
    "50 Rin":                           PhoaItemData(350,   4,  IC.filler),
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
    ("upgradable_prelude", "Progressive Prelude of Panselo", ["Prelude of Panselo", "Spell of Rejuvenation"]),
]

item_inclusion_priority: list[str] = \
    ["Progressive Bat", "Composite Bat", "Progressive Fishing Rod", "Serpent Rod", "Fishing Rod",
     "Progressive Prelude of Panselo", "Prelude of Panselo", "Spell of Rejuvenation", "Baroque of Battle", "Sky Vest",
     "Tusk Strike", "Energy Gem", "Heart Ruby", "Dragon's Scale", "50 Rin", "45 Rin", "40 Rin", "35 Rin", "30 Rin",
     "25 Rin", "20 Rin", "15 Rin", "Perro", "Honey Brew", "Curry Bento", "Honey Drop", "Rubber Ducky", "Stink Root",
     "Pumpkin Muffin", "Honey Bun", "Cooked Toad Leg", "Saffron Milk", "Milk", "Cheese", "Canned Beans", "Pooki Jerky",
     "Panselo Potato", "Mystery Meat", "Chocolate", "Falafel", "Desert Squash", "Cooked Squash", "Big Raw Meat",
     "Raw Meat", "Drake Tail", "Prime Fish Fillet", "Fruit Jam", "Vala Bean", "Berry Fruit", "Perro Egg", "Nectear",
     "Prickle Fruit", "Moon Kelp", "Doki Herb", "Dandelion", "9 Rin", "5 Rin", "1 Rin", "Strange Urn", "Lunar Frog",
     "Lunar Vase", "Lunar Drake", "Moonstone", "Antique Pin", "Turtle", "Mysterious Golem Head"]


def get_item_pool(world: "PhoaWorld", locations: dict[str, PhoaLocationData]) -> tuple[list[str], list[str]]:
    local_item_table = dict(item_table)

    # Determine item classifications based on settings
    local_item_table = filter_upgradable_items(local_item_table, world)

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

    # Remove progressive and useful items from the items_from_locations
    items_from_locations = [item for item in items_from_locations if item not in set(progressive_items)]
    items_from_locations = [item for item in items_from_locations if item not in set(useful_items)]

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


def filter_upgradable_items(items, world: "PhoaWorld") -> dict[str, PhoaItemData]:
    for option, progressive, bases in upgrade_groups:
        if getattr(world.options, option):
            for base in bases:
                items.pop(base, None)
            continue
        items.pop(progressive, None)

    removal_map = [
        (not world.options.enable_heart_ruby_locations
         and not world.options.keep_excluded_status_upgrades_in_item_pool,
         ["Heart Ruby"]),
        (not world.options.enable_energy_gem_locations
         and not world.options.keep_excluded_status_upgrades_in_item_pool,
         ["Energy Gem"]),
        (not world.options.enable_moonstone_locations
         and not world.options.keep_excluded_status_upgrades_in_item_pool,
         ["Moonstone"]),
    ]

    for condition, names in removal_map:
        if condition:
            for name in names:
                if name in world.progressive_item_classifications_overrides:
                    raise OptionError(
                        "KeepExcludedStatusUpgradesInItemPool Error: "
                        "Items excluded from the item pool are progression items for enabled locations. "
                        "Consider disabling these locations or keeping status upgrades in the item pool."
                    )
                items.pop(name, None)

    return items


def build_upgrade_map(options: PhoaOptions) -> dict[str, str]:
    mapping = {}

    for option, progressive, bases in upgrade_groups:
        if getattr(options, option):
            for base in bases:
                mapping[base] = progressive

    return mapping

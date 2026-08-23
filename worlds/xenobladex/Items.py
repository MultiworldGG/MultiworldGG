from collections import Counter, OrderedDict
import itertools
import logging
from BaseClasses import Item, ItemClassification as ItCl
from dataclasses import replace
from typing import TYPE_CHECKING, Generator, cast

if TYPE_CHECKING:
    from . import XenobladeXWorld

from . import Options
from .rules.level import get_logic_level_count

from .items import Itm
from .items.arts import arts_data
from .items.classes import classes_data
from .items.dataprobes import dataprobes_data
from .items.dollArmor import doll_armor_data
from .items.dollAugments import doll_augments_data
from .items.dollFrames import doll_frames_data
from .items.dollWeapons import doll_weapons_data
from .items.fieldSkills import field_skills_data
from .items.friends import friends_data
from .items.groundArmor import ground_armor_data
from .items.groundAugments import ground_augments_data
from .items.groundWeapons import ground_weapons_data
from .items.importantItems import important_items_data
# from .items.blueprints import blueprints_data
from .items.keys import keys_data
from .items.skills import skills_data


class XenobladeXItem(Item):
    """A generated item"""
    game: str = "Xenoblade X"


game_type_item_to_offset: OrderedDict[int, int] = OrderedDict()


class _Itms:
    table_size = 0
    last_table_size = 0

    @staticmethod
    def gen(prefix: str, type: int, data: list[Itm], prog: ItCl | None = None,
            type_count: int = 1) -> Generator[Itm, None, None]:
        _Itms.table_size += _Itms.last_table_size
        for typ in range(type, type + type_count):
            game_type_item_to_offset[typ] = _Itms.table_size
        _Itms.last_table_size = len(data)
        return (replace(e, type=type, id=_Itms.table_size + i + 1, prefix=prefix,
                        progression=prog if prog else e.progression, type_count=type_count)
                for i, e in enumerate(data) if e.valid)


xenobladeXImportantItems = [
    *_Itms.gen("KEY", type=0, data=keys_data, prog=ItCl.progression),
    *_Itms.gen("SKF", type=9, data=doll_frames_data, prog=ItCl.progression_deprioritized_skip_balancing),
    *_Itms.gen("DP", type=0x1c, data=dataprobes_data, prog=ItCl.progression_deprioritized_skip_balancing),
    *_Itms.gen("ART", type=0x20, data=arts_data, prog=ItCl.useful),
    *_Itms.gen("SKL", type=0x21, data=skills_data, prog=ItCl.useful),
    *_Itms.gen("FRD", type=0x22, data=friends_data, prog=ItCl.progression_deprioritized_skip_balancing),
    *_Itms.gen("FLDSK", type=0x23, data=field_skills_data, prog=ItCl.progression),
    *_Itms.gen("CL", type=0x24, data=classes_data, prog=ItCl.useful),
]

xenobladeXArmor = [*_Itms.gen("AMR", type=1, type_count=5, data=ground_armor_data)]
xenobladeXWeapons = [*_Itms.gen("WPN", type=6, type_count=2, data=ground_weapons_data)]
xenobladeXSkellArmor = [*_Itms.gen("SKAMR", type=0xa, type_count=5, data=doll_armor_data)]
xenobladeXSkellWeapons = [*_Itms.gen("SKWPN", type=0xf, type_count=5, data=doll_weapons_data)]
xenobladeXAugments = [
    *_Itms.gen("AUG", type=0x14, type_count=2, data=ground_augments_data),
    *_Itms.gen("SKAUG", type=0x16, type_count=3, data=doll_augments_data),
]
xenobladeXImpItems = [*_Itms.gen("IMPIT", type=0x1d, data=important_items_data, prog=ItCl.progression_skip_balancing)]
# xenobladeXBlueprints = [*_Itms.gen("BLP", type=0x41, data=blueprints_data)]

xenobladeXOptionalItems: dict[str | None, list[Itm]] = {
    xenobladeXArmor[0].prefix: xenobladeXArmor,
    xenobladeXWeapons[0].prefix: xenobladeXWeapons,
    xenobladeXSkellArmor[0].prefix: xenobladeXSkellArmor,
    xenobladeXSkellWeapons[0].prefix: xenobladeXSkellWeapons,
    xenobladeXAugments[0].prefix: xenobladeXAugments,
}

xenobladeXOptionalFullItems: list[Itm] = [
    *xenobladeXImpItems,
    # *xenobladeXBlueprints,
]

xenobladeXItems: dict[str, Itm] = {
    **{itm.get_item(): itm for itm in xenobladeXImportantItems},
    **{itm.get_item(): itm for itm in xenobladeXOptionalFullItems},
    **{itm.get_item(): itm for itm in itertools.chain(*xenobladeXOptionalItems.values())},
}


def create_optional_items(world: "XenobladeXWorld", count: int) -> list[XenobladeXItem]:
    # Add all optional Items to the item pool, these are selected at random,
    # depending on how many slots are left in the location pool
    optional_items: list[Itm] = []

    optionals_data = {prefix: len(category) for prefix, category in xenobladeXOptionalItems.items()
                      if prefix and getattr(world.options, prefix.lower()).value}
    optionals_length: int = sum(optionals_data.values())
    missing_item_count: int = min(count, optionals_length)
    # Throw error if overfilled. Make more graceful in future
    assert missing_item_count >= 0, f"{world.get_player_name()} overfilled locations. " \
        "Please select more locations or less items"

    if len(optionals_data) > 0:
        max_category_size = 950  # -49 for shop item buffer
        maxed_categories: list[str] = []
        optionals_counter: Counter[str] = Counter()
        while True:
            optionals_data_temp = optionals_data.copy()
            # Remove maxed categories from further rolls
            for prefix in maxed_categories:
                optionals_data_temp.pop(prefix, None)

            optional_roll = world.random.choices([*optionals_data_temp.keys()], [*optionals_data_temp.values()],
                                                 k=missing_item_count)
            optionals_counter += Counter(optional_roll)

            # Some categories are too big
            if max(optionals_counter.values()) > max_category_size:
                # Reroll the optional items that overflow a category onto the other categories
                missing_item_count = 0
                for prefix, count in optionals_counter.items():
                    if count > max_category_size:
                        missing_item_count += count - max_category_size
                        optionals_counter[prefix] = max_category_size
                        maxed_categories += [prefix]

            # No oversized categories detected
            else:
                for prefix, count in optionals_counter.items():
                    # Cap count to list size, should have no effect in almost all cases except for SKWPN on reroll
                    count = min(count, len(xenobladeXOptionalItems[prefix]))
                    optional_items += world.random.sample(xenobladeXOptionalItems[prefix], count)
                break
    return [world.create_item(itm.get_item()) for itm in optional_items]


def create_items(world: "XenobladeXWorld") -> None:
    """Create all items"""
    options = cast(Options.XenobladeXOptions, world.options)
    logic_level_steps = options.logic_level_steps.value
    logic_level_overcap = options.logic_level_overcap.value
    logic_levels = 0
    if logic_level_steps > 0:
        logic_levels = get_logic_level_count(99, logic_level_steps) + logic_level_overcap

    # Keep enough space for the victory item_event
    total_locations = len(world.multiworld.get_unfilled_locations(world.player)) - 1

    # Add starting inventory items
    world.random.seed(world.multiworld.seed)
    combat_starting_items = options.combat_starting_items.value
    if combat_starting_items > 0:
        combat_items = [itm for itm in xenobladeXImportantItems if itm.prefix in ["ART", "SKL", "CL"]]
        for combat_itm in world.random.sample(combat_items, combat_starting_items):
            world.push_precollected(world.create_item(combat_itm.get_item()))

    itempool: list[Item] = []
    requiredOptionalItems = [itm for itm in xenobladeXItems.values() if itm.required]
    optionalFullItems = [itm for itm in xenobladeXOptionalFullItems
                         if itm.prefix and getattr(world.options, itm.prefix.lower()).value]
    # Add all important Items, these are always added to the item pool
    for item in xenobladeXImportantItems + requiredOptionalItems + optionalFullItems:
        item_count = item.count if not item.get_item() == "KEY: Level" else logic_levels
        for idx in range(item_count):
            xeno_item = world.create_item(item.get_item())
            if idx < item_count - world.multiworld.precollected_items[world.player].count(xeno_item):
                itempool += [xeno_item]

    for xeno_item in create_optional_items(world, total_locations - len(itempool)):
        if xeno_item not in world.multiworld.precollected_items[world.player]:
            itempool += [xeno_item]
    world.multiworld.itempool += itempool

    world.multiworld.itempool += [world.create_item(world.get_filler_item_name())
                                  for _ in range(total_locations - len(itempool))]


def create_item(world:  "XenobladeXWorld", item_name: str) -> XenobladeXItem:
    """Create another item"""
    assert item_name in xenobladeXItems, f"Item not found: {item_name}"
    return XenobladeXItem(item_name, xenobladeXItems[item_name].progression,
                          world.item_name_to_id[item_name], world.player)


def create_filler(world:  "XenobladeXWorld") -> XenobladeXItem:
    return create_item(world, "KEY: Filler")


def get_random_filler_item_name(world: "XenobladeXWorld") -> str:
    return world.random.choice([*itertools.chain(*xenobladeXOptionalItems.values())]).get_item()


def debug_print_duplicates() -> None:
    xs = [i.get_item() for i in xenobladeXItems.values()]
    dup = {x: xs.count(x) for x in xs if xs.count(x) > 1}
    for name, n in dup.items():
        logging.debug(f"Duplicate: {name}, Count: {n}")

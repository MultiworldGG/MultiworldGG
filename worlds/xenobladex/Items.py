from collections import Counter, OrderedDict
import itertools
import logging
from BaseClasses import Item, ItemClassification as ItCl, MultiWorld
from dataclasses import dataclass, replace
from typing import Dict, Generator, List, Optional

from .Options import XenobladeXOptions
from .Regions import get_logic_level_count


@dataclass(frozen=True)
class Itm:
    name: str
    valid: bool = True
    count: int = 1
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    progression: ItCl = ItCl.filler
    type_count: int = 1
    required: bool = False

    def get_item(self):
        if self.prefix is None:
            return self.name
        return f"{self.prefix}: {self.name}"


from .items.arts import arts_data  # noqa: E402
from .items.classes import classes_data  # noqa: E402
from .items.dataprobes import dataprobes_data  # noqa: E402
from .items.dollArmor import doll_armor_data  # noqa: E402
from .items.dollAugments import doll_augments_data  # noqa: E402
from .items.dollFrames import doll_frames_data  # noqa: E402
from .items.dollWeapons import doll_weapons_data  # noqa: E402
from .items.fieldSkills import field_skills_data  # noqa: E402
from .items.friends import friends_data  # noqa: E402
from .items.groundArmor import ground_armor_data  # noqa: E402
from .items.groundAugments import ground_augments_data  # noqa: E402
from .items.groundWeapons import ground_weapons_data  # noqa: E402
from .items.importantItems import important_items_data  # noqa: E402
# from .items.blueprints import blueprints_data  # noqa: E402
from .items.keys import keys_data  # noqa: E402
from .items.skills import skills_data  # noqa: E402


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
xenobladeXImpItems = [*_Itms.gen("IMPIT", type=0x1d, data=important_items_data,
                                 prog=ItCl.progression_skip_balancing)]
# xenobladeXBlueprints = [*_Itms.gen("BLP", type=0x41, data=blueprints_data)]

xenobladeXOptionalItems: Dict[str | None, List[Itm]] = {
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

xenobladeXItems: List[Itm] = [
    *xenobladeXImportantItems,
    *xenobladeXOptionalFullItems,
    *(itertools.chain(*xenobladeXOptionalItems.values())),
]


def create_items(world: MultiWorld, player, base_id, options: XenobladeXOptions, item_name_to_id: Dict[str, int]):
    """Create all items"""
    logic_level_steps = options.logic_level_steps.value
    logic_level_overcap = options.logic_level_overcap.value
    logic_levels = 0
    if logic_level_steps > 0:
        logic_levels = get_logic_level_count(99, logic_level_steps) + logic_level_overcap

    itempool: List[Item] = []
    requiredOptionalItems = [itm for itm in xenobladeXItems if itm.required]
    optionalFullItems = [itm for itm in xenobladeXOptionalFullItems
                         if itm.prefix and getattr(options, itm.prefix.lower()).value]
    # Add all important Items, these are always added to the item pool
    for item in xenobladeXImportantItems + requiredOptionalItems + optionalFullItems:
        item_count = item.count if not item.get_item() == "KEY: Level" else logic_levels
        for idx in range(item_count):
            xeno_item = XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player)
            if idx < item_count - world.precollected_items[player].count(xeno_item):
                itempool += [xeno_item]

    # Add all optional Items to the item pool, these are selected at random,
    # depending on how many slots are left in the location pool
    optional_items: List[Itm] = []

    # Keep enough space for the victory item_event
    total_locations = len(world.get_unfilled_locations(player)) - 1
    optionals_data = {prefix: len(category) for prefix, category in xenobladeXOptionalItems.items()
                      if prefix and getattr(options, prefix.lower()).value}
    optionals_length: int = sum(optionals_data.values())
    missing_item_count: int = min(total_locations - len(itempool), optionals_length)
    # Throw error if overfilled. Make more graceful in future
    assert missing_item_count >= 0, f"{world.get_player_name(player)} overfilled locations. " \
        "Please select more locations or less items"

    if len(optionals_data) > 0:
        world.random.seed(world.seed)
        max_category_size = 950  # -49 for shop item buffer
        maxed_categories: list[str] = []
        optionals_counter: Counter = Counter()
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

    for item in optional_items:
        xeno_item = XenobladeXItem(item.get_item(), item.progression, base_id + item.id, player)
        if xeno_item not in world.precollected_items[player]:
            itempool += [xeno_item]
    world.itempool += itempool

    world.itempool += [create_filler(player, item_name_to_id) for _ in range(total_locations - len(itempool))]


def create_item(item_name: str, player: int, abs_id: int, is_prog: bool = True) -> XenobladeXItem:
    """Create another item"""
    return XenobladeXItem(item_name, ItCl.progression if is_prog else ItCl.filler, abs_id, player)


def create_filler(player: int, item_name_to_id: Dict[str, int]) -> XenobladeXItem:
    return create_item("KEY: Filler", player, item_name_to_id["KEY: Filler"], is_prog=False)


def debug_print_duplicates():
    xs = [i.get_item() for i in xenobladeXItems]
    dup = {x: xs.count(x) for x in xs if xs.count(x) > 1}
    for name, n in dup.items():
        logging.debug(f"Duplicate: {name}, Count: {n}")

from random import Random
import logging

from BaseClasses import ItemClassification, Item
from typing import Dict, List, Union, Protocol

from . import Weapon
from .Options import LunacidOptions
from .data.item_data import (all_items, LunacidItemData, base_unique_items, starting_weapon, shop_starting_weapons,
                             drop_starting_weapons, base_special_item_counts, shop_unique_items, shop_item_count,
                             all_item_data_by_name, quench_starting_weapons)
from .data.weapon_info import all_weapons, ranged_weapons, all_weapon_info_by_name
from .data.spell_info import all_spells, ranged_spells, all_spell_info_by_name
from .strings.items import UniqueItem, Coins, Door, Voucher, Switch, Trap, CustomItem, Upgrade, SpookyItem, Progressives
from .strings.properties import Elements, Types
from .strings.spells import Spell, MobSpell, CrimpusSpell, SpookySpell
from .strings.weapons import SpookyWeapon

logger = logging.getLogger(__name__)


class LunacidItemFactory(Protocol):
    def __call__(self, name: Union[str, LunacidItemData], override_classification: ItemClassification = None) -> Item:
        raise NotImplementedError


def initialize_items_by_name() -> List[LunacidItemData]:
    items = []
    for item in all_items:
        items.append(item)
    return items


item_table = initialize_items_by_name()
complete_items_by_name = {item.name: item for item in item_table}
all_items_by_element = {weapon: all_weapon_info_by_name[weapon].element for weapon in all_weapon_info_by_name}
for spell in all_spell_info_by_name:
    all_items_by_element[spell] = all_spell_info_by_name[spell].element


def determine_weapon_elements(options: LunacidOptions, random: Random) -> Dict[str, str]:
    elements = {}
    if not options.random_elements:
        for weapon in all_weapon_info_by_name:
            elements[weapon] = all_weapon_info_by_name[weapon].element
        for spell in all_spell_info_by_name:
            elements[spell] = all_spell_info_by_name[spell].element
        return elements
    excluded_list = [item.name for item in all_spells if item.style == Types.support or item.element == Elements.ignore]

    weapons = [weapon for weapon in all_weapons if weapon.name not in excluded_list]
    spells = [item.name for item in all_spells if item.name not in excluded_list]
    for item in weapons:
        if item.style == Types.melee:
            elements[item.name] = random.choice(Elements.all_elements)
        else:
            elements[item.name] = random.choice(Elements.spell_elements)
    for item in spells:
        elements[item] = random.choice(Elements.spell_elements)
    for item in excluded_list:
        elements[item] = all_items_by_element[item]
    return elements


def create_items(item_factory: LunacidItemFactory, locations_count: int, items_to_exclude: List[Item],
                 weapon_elements: Dict[str, str], month: int, level: int, ut_starting_weapon: str, options: LunacidOptions,
                 random: Random) -> (List[Item], List[Item], Item):
    items: List[Item] = []
    lunacid_items = create_lunacid_items(item_factory, weapon_elements, month, level, options)
    for item in items_to_exclude:
        if item in lunacid_items:
            lunacid_items.remove(item)
    assert len(
        lunacid_items) <= locations_count, (f"There should be at least as many locations [{locations_count}] "
                                            f"as there are mandatory items [{len(lunacid_items)}]")
    items += lunacid_items
    if ut_starting_weapon != "":
        chosen_weapon = ut_starting_weapon
    else:
        chosen_weapon = determine_starting_weapon(random, options)
    if weapon_elements[chosen_weapon] in [Elements.light, Elements.fire, Elements.dark_and_fire,
                                          Elements.normal_and_fire, Elements.dark_and_light]:
        starting_weapon_choice = item_factory(chosen_weapon, ItemClassification.progression)
    elif (weapon_elements[chosen_weapon] in [Elements.poison, Elements.ice_and_poison] and chosen_weapon in ranged_weapons
          or chosen_weapon in ranged_spells):
        starting_weapon_choice = item_factory(chosen_weapon, ItemClassification.progression)
    elif chosen_weapon in quench_starting_weapons:
        starting_weapon_choice = item_factory(chosen_weapon, ItemClassification.progression)
    else:
        starting_weapon_choice = item_factory(chosen_weapon)
    for item in items:
        if item.name == starting_weapon_choice.name:
            items.remove(item)
            break
    logger.debug(f"Created {len(lunacid_items)} unique items")
    filler_slots = locations_count - len(items)
    _, local_filler = create_filler(item_factory, options, random, filler_slots, month, items)

    return items, local_filler, starting_weapon_choice


def create_lunacid_items(item_factory: LunacidItemFactory, weapon_elements: Dict[str, str], month: int, level: int,
                         options: LunacidOptions) -> List[Item]:
    items = []
    create_weapons(item_factory, weapon_elements, options, items)
    create_spells(item_factory, weapon_elements, options, items)
    create_special_items(item_factory, options, items)
    create_switch_items(item_factory, options, items)
    create_door_items(item_factory, options, items)
    create_hallo_items(item_factory, month, weapon_elements, options, items)
    create_stat_items(item_factory, level, options, items)
    return items


def create_weapons(item_factory: LunacidItemFactory, equipment_by_elements: Dict[str, str],
                   options: LunacidOptions, items: List[Item]) -> List[Item]:
    for item in Weapon.base_weapons:
        append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons,
                                                                     options, equipment_by_elements, items)
    if options.shopsanity:
        for item in Weapon.shop_weapons:
            append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons,
                                                                         options, equipment_by_elements, items)
    if options.dropsanity:
        for item in Weapon.drop_weapons:
            append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons,
                                                                         options, equipment_by_elements, items)
    if options.quenchsanity:
        for item in Weapon.quenchsanity_weapons:
            append_item_with_progression_determined_by_element_and_range(item_factory, item, ranged_weapons,
                                                                         options, equipment_by_elements, items)
    if options.etnas_pupil:
        append_item_with_progression_determined_by_element_and_range(item_factory, Weapon.limbo, ranged_weapons,
                                                                     options, equipment_by_elements, items)
    return items


def append_item_with_progression_determined_by_element_and_range(item_factory: LunacidItemFactory, item: str,
                                                                 ranged_list: List[str], options: LunacidOptions,
                                                                 equipment_by_elements: Dict[str, str], items: List[Item]):
    if equipment_by_elements[item] in [Elements.light, Elements.fire, Elements.dark_and_fire, Elements.normal_and_fire,
                                       Elements.dark_and_light]:
        items.append(item_factory(item, ItemClassification.progression))
    elif equipment_by_elements[item] in [Elements.poison, Elements.ice_and_poison] and item in ranged_list:
        items.append(item_factory(item, ItemClassification.progression))
    elif options.quenchsanity and item in Weapon.quenchable_weapons:
        items.append(item_factory(item, ItemClassification.progression))
    elif item == Weapon.limbo:
        items.append(item_factory(item, ItemClassification.progression))
    else:
        items.append(item_factory(item))


def create_spells(item_factory: LunacidItemFactory, equipment_by_elements: Dict[str, str], options: LunacidOptions,
                  items: List[Item]) -> List[Item]:
    force_progressive = (options.ending == options.ending.option_ending_e)
    for item in Spell.base_spells:
        if all_spell_info_by_name[item].style == Types.support:
            items.append(item_factory(item, determine_item_classification(item, force_progressive)))
        elif equipment_by_elements[item] in [Elements.light, Elements.fire, Elements.dark_and_fire,
                                             Elements.normal_and_fire, Elements.dark_and_light]:
            items.append(item_factory(item, ItemClassification.progression))
        elif equipment_by_elements[item] in [Elements.poison, Elements.ice_and_poison] and item in ranged_spells:
            items.append(item_factory(item, ItemClassification.progression))
        elif options.breakables and item in [Spell.blue_flame_arc, Spell.moon_beam, Spell.ice_tear, Spell.lava_chasm]:
            items.append(item_factory(item, ItemClassification.progression))
        else:
            items.append(item_factory(item, determine_item_classification(item, force_progressive)))
    if options.dropsanity != options.dropsanity.option_off:
        for item in MobSpell.drop_spells:
            if all_spell_info_by_name[item].style == Types.support:
                items.append(item_factory(item, determine_item_classification(item, force_progressive)))
            elif equipment_by_elements[item] in [Elements.light, Elements.fire, Elements.dark_and_fire,
                                                 Elements.normal_and_fire, Elements.dark_and_light]:
                items.append(item_factory(item, ItemClassification.progression))
            elif equipment_by_elements[item] in [Elements.poison, Elements.ice_and_poison] and item in ranged_spells:
                items.append(item_factory(item, ItemClassification.progression))
            else:
                items.append(item_factory(item, determine_item_classification(item, force_progressive)))
    return items


def determine_starting_weapon(random: Random, options: LunacidOptions) -> str:
    starting_selection = starting_weapon.copy()
    if options.shopsanity:
        starting_selection += shop_starting_weapons
    if options.dropsanity:
        starting_selection += drop_starting_weapons
    if options.quenchsanity:
        starting_selection += quench_starting_weapons
    if options.starting_class == options.starting_class.option_forsaken or (options.starting_class == options.starting_class.option_custom and options.custom_class["Intelligence"] == 1):
        starting_selection = [weapon for weapon in starting_selection if weapon not in Spell.base_spells and weapon not in MobSpell.drop_spells]
    chosen_weapon_name = random.choice(starting_selection)
    return chosen_weapon_name


def determine_item_classification(item: str, progression: bool) -> ItemClassification:
    return ItemClassification.progression if progression else all_item_data_by_name[item].classification


def create_special_items(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    for item in base_unique_items:
        if item == UniqueItem.white_tape and options.ending == options.ending.option_ending_e:
            items.append(item_factory(item, ItemClassification.progression))
            continue
        elif item == UniqueItem.dusty_crystal_orb and options.secret_door_lock == options.secret_door_lock.option_true:
            items.append(item_factory(item, ItemClassification.progression))
            continue
        items.append(item_factory(item))
    for item in Voucher.vouchers:
        items.append(item_factory(item, ItemClassification.progression))
    for item in base_special_item_counts:
        items.extend(item_factory(special_item) for special_item in [item] * base_special_item_counts[item])
    if options.progressive_symbols:
        items.extend(item_factory(symbol) for symbol in [Progressives.vampiric_symbol]*3)
    else:
        items.append(item_factory(UniqueItem.vampiric_symbol_w))
        items.append(item_factory(UniqueItem.vampiric_symbol_a))
        items.append(item_factory(UniqueItem.vampiric_symbol_e))
    if options.shopsanity:
        for item in shop_unique_items:
            if item == UniqueItem.oil_lantern and options.starting_area == options.starting_area.option_tomb:
                continue  # We will force place it.
            items.append(item_factory(item))
        for item in shop_item_count:
            items.extend([item_factory(filler) for filler in [item] * shop_item_count[item]])
    if options.dropsanity:
        items.extend(item_factory(item) for item in [Upgrade.drop_chance]*3)
    if options.levelsanity:
        items.append(item_factory(CustomItem.lucky_bangle))
    create_strange_coins(item_factory, options, items)
    items.append(item_factory(CustomItem.bestial_mastery))
    return items


def create_strange_coins(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    if options.ending != options.ending.option_ending_b and options.ending != options.ending.option_any_ending:
        return items
    total_coins = max(options.required_strange_coin.value, options.total_strange_coin.value)
    required_coins = options.required_strange_coin.value
    count = 0
    while count < required_coins:
        items.append(item_factory(Coins.strange_coin, ItemClassification.progression | ItemClassification.useful))
        count += 1
    count = 0
    while count < total_coins - required_coins:
        items.append(item_factory(Coins.strange_coin, ItemClassification.progression))
        count += 1
    return items

def create_switch_items(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    if not options.switch_locks:
        return items
    for item in Switch.switches:
        items.append(item_factory(item))
    return items


def create_door_items(item_factory: LunacidItemFactory, options: LunacidOptions, items: List[Item]) -> List[Item]:
    if not options.door_locks:
        return items
    for key in Door.all_door_keys:
        items.append(item_factory(key))
    return items


def create_hallo_items(item_factory: LunacidItemFactory, month: int, equipment_by_elements: Dict[str, str],
                       options: LunacidOptions, items: List[Item]) -> List[Item]:
    if month != 10:
        return items
    if equipment_by_elements[SpookySpell.pumpkin_pop] in [Elements.light, Elements.fire, Elements.dark_and_fire,
                                                          Elements.normal_and_fire, Elements.dark_and_light,
                                                          Elements.poison, Elements.ice_and_poison]:
        items.append(item_factory(SpookySpell.pumpkin_pop, ItemClassification.progression))
    else:
        items.append(item_factory(SpookySpell.pumpkin_pop))
    items.extend(item_factory(candy) for candy in [SpookyItem.soul_candy]*35)
    if options.dropsanity:
        if equipment_by_elements[SpookyWeapon.cavalry_saber] in [Elements.light, Elements.fire, Elements.dark_and_fire,
                                                                 Elements.normal_and_fire, Elements.dark_and_light]:
            items.append(item_factory(SpookyWeapon.cavalry_saber, ItemClassification.progression))
        else:
            items.append(item_factory(SpookyWeapon.cavalry_saber))
    return items


def create_crimpus_items(item_factory: LunacidItemFactory, month: int, equipment_by_elements: Dict[str, str],
                         items: List[Item]) -> List[Item]:
    if month != 12:
        return items
    if equipment_by_elements[CrimpusSpell.jingle_bells] in [Elements.light, Elements.fire, Elements.dark_and_fire,
                                                            Elements.normal_and_fire, Elements.dark_and_light,
                                                            Elements.poison, Elements.ice_and_poison]:
        items.append(item_factory(CrimpusSpell.jingle_bells, ItemClassification.progression))
    else:
        items.append(item_factory(CrimpusSpell.jingle_bells))
    return items


def create_stat_items(item_factory: LunacidItemFactory, level: int, options: LunacidOptions, items: List[Item]):
    if not options.levelsanity:
        return items
    items.extend([item_factory(item, ItemClassification.progression) for item in [CustomItem.experience]*(100 - level)])
    items.extend([item_factory(item, ItemClassification.useful) for item in [CustomItem.experience]*level])
    return items


def create_filler(item_factory: LunacidItemFactory, options: LunacidOptions, random: Random,
                  filler_slots: int, month: int, items: List[Item]) -> (List[Item], List[Item]):
    filler_count = filler_slots
    if filler_count == 0:
        return items
    filler_weights = {filler: options.filler.value[filler] for filler in options.filler.value if options.filler.value[filler] != 0}
    trap_weights = {trap: options.traps.value[trap] for trap in options.traps.value if options.traps.value[trap] != 0}
    trap_percent = options.trap_percent / 100
    if len(filler_weights) == 0:
        filler_weights[Coins.silver] = 1
        filler_weights[CustomItem.experience] = 1
    if options.levelsanity:
        del filler_weights[CustomItem.experience]
    if month != 12:
        if Trap.eggnog in trap_weights:
            del trap_weights[Trap.eggnog]
        if Trap.coal in trap_weights:
            del trap_weights[Trap.coal]
    if len(trap_weights) == 0:
        trap_percent = 0
    if trap_percent > 0:
        trap_count = int(filler_slots * trap_percent)
        filler_count = filler_slots - trap_count
        trap_table = random.choices(population=list(trap_weights.keys()), weights=list(trap_weights.values()), k=trap_count)
        for trap in trap_table:
            items.append(item_factory(trap))

    local_filler_count = int(filler_count * (options.filler_local_percent / 100))
    local_filler: List[Item] = []
    filler_table = random.choices(population=list(filler_weights.keys()), weights=list(filler_weights.values()), k=filler_count)
    for filler in filler_table:
        if local_filler_count > 0:
            local_filler.append(item_factory(filler, ItemClassification.filler))
            local_filler_count -= 1
            continue
        items.append(item_factory(filler, ItemClassification.filler))  # Someone said this bleeds progression somehow??
    return items, local_filler


all_filler = [item for item in item_table if item.classification is ItemClassification.filler]

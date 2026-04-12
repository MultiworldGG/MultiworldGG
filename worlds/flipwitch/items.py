from random import Random
import logging

from BaseClasses import ItemClassification, Item
from typing import Dict, List, Union, Protocol, Tuple

from worlds.flipwitch import FlipwitchOptions
from worlds.flipwitch.data.items import FlipwitchItemData, all_items, base_items, gacha_items, filler_items, shop_items, quest_items, warp_items
from worlds.flipwitch.strings.items import Coin, Upgrade, GoalItem, QuestItem, Custom, hint_base_items, Warp

logger = logging.getLogger(__name__)


class FlipwitchItemFactory(Protocol):
    def __call__(self, name: Union[str, FlipwitchItemData], override_classification: ItemClassification = None) -> Item:
        raise NotImplementedError


def initialize_items_by_name() -> List[FlipwitchItemData]:
    items = []
    for item in all_items:
        items.append(item)
    return items


item_table = initialize_items_by_name()
complete_items_by_name = {item.name: item for item in item_table}


def create_items(item_factory: FlipwitchItemFactory, locations_count: int, items_to_exclude: List[Item], options: FlipwitchOptions,
                 random: Random) -> Tuple[List[Item], Dict[str, Item]]:
    items = []
    hints: Dict[str, Item] = {}
    flipwitch_items = create_flipwitch_items(item_factory, options, hints, random)
    for item in items_to_exclude:
        if item in flipwitch_items:
            flipwitch_items.remove(item)
    assert len(
        flipwitch_items) <= locations_count, f"There should be at least as many locations [{locations_count}] as there are mandatory items [{len(flipwitch_items)}]"
    items += flipwitch_items
    logger.debug(f"Created {len(flipwitch_items)} unique items")
    filler_slots = locations_count - len(items)
    create_filler(item_factory, random, filler_slots, items)
    return items, hints


def create_flipwitch_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, hints_lookup: Dict[str, Item], random: Random) -> List[Item]:
    items = []
    create_base_items(item_factory, options, hints_lookup, items)
    create_gacha_items(item_factory, options, items, random)
    create_shop_items(item_factory, options, hints_lookup, items)
    create_quest_items(item_factory, options, hints_lookup, items)
    create_warp_items(item_factory, options, items)
    create_extra_movement_items(item_factory, options, items)
    return items


def create_base_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, hints_lookup: Dict[str, Item], items: List[Item]):
    for item in base_items:
        if item.classification == ItemClassification.filler or item.classification == ItemClassification.trap:
            continue
        elif item.name == Upgrade.bewitched_bubble and (options.quest_for_sex == options.quest_for_sex.option_off or options.quest_for_sex == options.quest_for_sex.option_sensei):
            continue
        elif item.name == Upgrade.health:
            if options.stat_shuffle == options.stat_shuffle.option_false:
                continue
            upgrade_name = item.name
            items.extend([item_factory(stat) for stat in [upgrade_name]*10])
        elif item.name == Upgrade.mana:
            if options.stat_shuffle == options.stat_shuffle.option_false:
                continue
            upgrade_name = item.name
            items.extend([item_factory(stat) for stat in [upgrade_name]*10])
        elif item.name == Upgrade.peachy_peach:
            if options.quest_for_sex == options.quest_for_sex.option_off:
                continue
            items.extend([item_factory(peach, ItemClassification.progression | ItemClassification.useful) for peach in [Upgrade.peachy_peach]*8])
            items.extend([item_factory(peach) for peach in [Upgrade.peachy_peach]*3])
        elif item.name == Upgrade.wand:
            if options.quest_for_sex == options.quest_for_sex.option_off:
                continue
            items.extend([item_factory(weapon) for weapon in [Upgrade.wand]*2])
        elif item.name == GoalItem.chaos_piece:
            if options.shuffle_chaos_pieces == options.shuffle_chaos_pieces.option_false:
                continue
            count = 1
            for piece in [GoalItem.chaos_piece] * 6:
                chaos_item = item_factory(piece)
                items.append(chaos_item)
                hints_lookup[piece + " " + str(count)] = chaos_item
                count += 1
        elif item.name == Coin.lucky_coin:
            continue
        elif item.name == Upgrade.barrier:
            items.extend(item_factory(barrier) for barrier in [Upgrade.barrier]*2)
        elif item.name == Upgrade.peachy_upgrade:
            if options.quest_for_sex == options.quest_for_sex.option_off:
                continue
            items.extend(item_factory(upgrade) for upgrade in [Upgrade.peachy_upgrade]*2)
        elif item.name in hint_base_items:
            hint_item = item_factory(item.name)
            hints_lookup[item.name] = hint_item
            items.append(hint_item)
        else:
            items.append(item_factory(item.name))
    return items


def create_gacha_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, items: List[Item], random: Random) -> List[Item]:
    if options.gachapon_shuffle == options.gachapon_shuffle.option_off:
        return items
    is_fully_randomized = options.gachapon_shuffle == options.gachapon_shuffle.option_all
    lucky_coins_without_promotional = [coin for coin in Coin.lucky_coins if coin != Coin.promotional_coin]
    for item in gacha_items:
        if item.name in lucky_coins_without_promotional:
            items.extend(item_factory(lucky) for lucky in [item.name] * 10)
        elif item.name == Coin.promotional_coin:
            items.append(item_factory(item.name))
        elif is_fully_randomized:
            items.append(item_factory(item.name))
    chosen_additional = random.sample(Coin.lucky_coins, 3)
    for item in chosen_additional:
        items.append(item_factory(item))
    return items


def create_shop_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, hints_lookup: Dict[str, Item], items: List[Item]) -> List[Item]:
    if options.shopsanity == options.shopsanity.option_false:
        return items
    for item in shop_items:
        if item.name == QuestItem.fairy_bubble:
            fairy_item = item_factory(item.name)
            hints_lookup[item.name] = fairy_item
            items.append(fairy_item)
            continue
        items.append(item_factory(item.name))
    return items


def create_quest_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, hints_lookup: Dict[str, Item], items: List[Item]) -> List[Item]:
    if options.quest_for_sex == options.quest_for_sex.option_off or options.quest_for_sex == options.quest_for_sex.option_sensei:
        return items
    for item in quest_items:
        if item.name == Custom.sex_experience:
            if options.quest_for_sex != options.quest_for_sex.option_all:
                continue
            items.extend(item_factory(sex) for sex in [item.name] * 40)
        elif item.name == QuestItem.summon_stone:
            count = 1
            for stone in [QuestItem.summon_stone]*3:
                stone_item = item_factory(stone)
                hints_lookup[stone + " " + str(count)] = stone_item
                items.append(stone_item)
                count += 1
        elif item.name == QuestItem.soul_fragment:
            count = 1
            for soul in [QuestItem.soul_fragment]*3:
                soul_item = item_factory(soul)
                hints_lookup[soul + " " + str(count)] = soul_item
                items.append(soul_item)
                count += 1
        else:
            misc_item = item_factory(item.name)
            hints_lookup[item.name] = misc_item
            items.append(misc_item)
    return items


def create_warp_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, items: List[Item]):
    if options.crystal_teleports == options.crystal_teleports.option_false:
        return items
    for item in warp_items:
        if item.name == Warp.area_to_warp[options.starting_area.value]:
            continue
        items.append(item_factory(item.name))
    return items


def create_extra_movement_items(item_factory: FlipwitchItemFactory, options: FlipwitchOptions, items: List[Item]):
    if options.shuffle_double_jump:
        items.append(item_factory(Upgrade.rose_ribbon))
    if options.shuffle_dodge:
        items.append(item_factory(Upgrade.orb_of_avoidance))
    return items


def create_filler(item_factory: FlipwitchItemFactory, random: Random, filler_slots: int, items: List[Item]):
    if filler_slots == 0:
        return items
    filler_list = [item.name for item in filler_items]
    items.extend([item_factory(filler) for filler in random.choices(filler_list, k=filler_slots)])
    return items



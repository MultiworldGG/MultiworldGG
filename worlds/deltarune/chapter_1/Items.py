from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
from worlds.deltarune.LogicHelper import (
    include_doorkey,
    randomized_chapters,
    include_hidden_items,
    include_secret_bosses_items_requirement,
    include_secret_bosses_items_reward,
    include_unused_items,
    progressive_area_unlocks,
    not_progressive_area_unlocks,
)
from worlds.deltarune.Items import (
    ItemData,
    ItemGroups,
    ItemIDs,
    items,
    generic_create_items,
    generic_get_filler_and_trap_items,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter1_items = [
    ItemData(ItemIDs.dark_candy, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.rouxlsroux, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.clubsandwich, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(
        ItemIDs.dark_burger,
        ItemClassification.filler,
        groups=[ItemGroups.healing_item, ItemGroups.fusion_ingredient],
    ),
    ItemData(ItemIDs.heartsdonut, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.chocdiamond, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.revivemint, ItemClassification.filler, groups=[ItemGroups.healing_item], amount=2),
    ItemData(ItemIDs.spincake, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.amber_card, ItemClassification.filler, groups=[ItemGroups.armors, ItemGroups.fusion_ingredient]),
    ItemData(ItemIDs.glowshard, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dice_brace, ItemClassification.useful, groups=[ItemGroups.armors], amount=1),
    ItemData(
        ItemIDs.spookysword, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons], amount=1
    ),
    ItemData(
        ItemIDs.brave_ax, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons], amount=1
    ),
    ItemData(
        ItemIDs.ragger, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons], amount=1
    ),
    ItemData(
        ItemIDs.daintyscarf, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons], amount=1
    ),
    ItemData(ItemIDs.manual, ItemClassification.progression, amount=2),
    ItemData(
        ItemIDs.bake_sale_ticket, 
        ItemClassification.progression, 
        groups=[ItemGroups.region_blockers], 
        should_be_included=not_progressive_area_unlocks,
        amount=1
    ),
    ItemData(
        ItemIDs.castle_key, 
        ItemClassification.progression,
        groups=[ItemGroups.region_blockers], 
        should_be_included=not_progressive_area_unlocks,
        amount=1
    ),
    ItemData(
        ItemIDs.progressive_ch1_area_unlock, 
        ItemClassification.progression,
        groups=[ItemGroups.region_blockers, ItemGroups.progressive_area_unlocks], 
        should_be_included=progressive_area_unlocks,
        amount=2
    ),
    ItemData(ItemIDs.brokencake, ItemClassification.progression, amount=1),
    ItemData(ItemIDs.top_cake, ItemClassification.progression, amount=1),
    ItemData(
        ItemIDs.ironshackle,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.white_ribbon,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.king_shape_key_piece,
        ItemClassification.progression_skip_balancing,
        groups=[ItemGroups.region_blockers],
        amount=0,
    ),
    ItemData(
        ItemIDs.chapter_1_egg,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.castle_moss,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.moss],
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.broken_key_a,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement,
        groups=[ItemGroups.jevil_keys],
        amount=1,
    ),
    ItemData(
        ItemIDs.broken_key_b,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement,
        groups=[ItemGroups.jevil_keys],
        amount=1,
    ),
    ItemData(
        ItemIDs.broken_key_c,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement,
        groups=[ItemGroups.jevil_keys],
        amount=1,
    ),
    ItemData(
        ItemIDs.door_key,
        ItemClassification.progression,
        should_be_included=include_doorkey,
        groups=[ItemGroups.jevil_keys],
        amount=1,
    ),
    ItemData(
        ItemIDs.jevilstail,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.armors],
        amount=1,
    ),
    ItemData(
        ItemIDs.devilsknife,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.susie_weapons],
        amount=1,
    ),
    ItemData(
        ItemIDs.shadowcrystal,
        ItemClassification.filler,
        should_be_included=include_secret_bosses_items_reward,
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.chapter_1_unlock,
        ItemClassification.progression,
        should_be_included=randomized_chapters,
        groups=[ItemGroups.region_blockers],
        amount=1,
    ),
    ItemData(
        ItemIDs.brokencake_consumable,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.gigasalad,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.favsandwich,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.mouse_token,
        ItemClassification.useful,
        should_be_included=include_unused_items,
        groups=[ItemGroups.armors, ItemGroups.unused_items],
        amount=1,
    ),
    ItemData(
        ItemIDs.trefoil,
        ItemClassification.useful,
        should_be_included=include_unused_items,
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons, ItemGroups.unused_items],
        amount=1,
    ),
]


def create_items(world: "DeltaruneWorld"):
    return generic_create_items(world, chapter1_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter1_items)

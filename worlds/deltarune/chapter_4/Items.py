from typing import TYPE_CHECKING
from BaseClasses import ItemClassification

from worlds.deltarune.LogicHelper import (
    randomized_chapters,
    include_hidden_items,
    include_secret_bosses_items_reward,
)
from worlds.deltarune.Items import (
    ItemIDs,
    ItemData,
    ItemData,
    generic_create_items,
    generic_get_filler_and_trap_items,
    DeltaruneItem,
    ItemGroups,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter4_items = [
    ItemData(ItemIDs.dark_candy, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.ancientsweet, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.rhapsotea, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.revivemint, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.bittertear, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.spincake, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.tensiongem, ItemClassification.filler, groups=[ItemGroups.tension_items]),
    ItemData(ItemIDs.absorbax, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons]),
    ItemData(ItemIDs.jingleblade, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    ItemData(ItemIDs.wingblade, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    ItemData(ItemIDs.claimbclaws, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(ItemIDs.sheetmusic, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(
        ItemIDs.dogdollar,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.currencies, ItemGroups.fusion_ingredient],
        amount=1,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.scarlixir,
        ItemClassification.filler,
        groups=[ItemGroups.healing_item, ItemGroups.fusion_ingredient],
        amount=2,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.goldwidow,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.mysticband,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.powerband,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        amount=2,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.scarfmark,
        ItemClassification.useful,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.princessrbn,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.combination_lock_digit,
        ItemClassification.progression_skip_balancing,
        groups=[ItemGroups.region_blockers],
        amount=0,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.justiceaxe,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.susie_weapons],
    ),
    ItemData(
        ItemIDs.shadowcrystal,
        ItemClassification.filler,
        should_be_included=include_secret_bosses_items_reward,
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.chapter_4_egg,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.sacred_moss,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.moss],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.chapter_4_unlock,
        ItemClassification.progression,
        should_be_included=randomized_chapters,
        groups=[ItemGroups.region_blockers],
    ),
]


def create_items(world: "DeltaruneWorld") -> list[DeltaruneItem]:
    return generic_create_items(world, chapter4_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter4_items)

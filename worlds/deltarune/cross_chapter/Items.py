from enum import StrEnum
from worlds.deltarune.Items import (
    ItemData,
    ItemData,
    ItemIDs,
    generic_create_items,
    generic_get_filler_and_trap_items,
    ItemGroups,
)
from typing import TYPE_CHECKING
from BaseClasses import ItemClassification

if TYPE_CHECKING:
    from .. import DeltaruneWorld


cross_chapter_items = [
    ItemData(
        ItemIDs.lancer_cookie,
        ItemClassification.filler,
        should_be_included=lambda world: world.has_at_least_one_chapter_included([1, 2, 4]),
        groups=[ItemGroups.healing_item],
    ),
    ItemData(ItemIDs.dark_dollar_1, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dark_dollars_20, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dark_dollars_40, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dark_dollars_80, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dark_dollars_100, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dark_dollars_250, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.dark_dollars_500, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.what_interesting_behavior, ItemClassification.progression | ItemClassification.useful, amount=0),
    ItemData(
        ItemIDs.s_r_n_actions,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_fun_gang_actions_unlockable()
        and world.has_at_least_one_chapter_included([2, 3, 4]),
    ),
    ItemData(
        ItemIDs.kris,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=lambda world: world.is_kris_unlockable(),
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.susie,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=lambda world: world.is_characters_unlockables(),
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.ralsei,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=lambda world: world.is_characters_unlockables(),
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.noelle,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=lambda world: world.include_chapter(2) and world.is_characters_unlockables(),
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.dd_burger,
        ItemClassification.filler,
        should_be_included=lambda world: world.can_access_fusion(),
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.silver_card,
        ItemClassification.filler,
        should_be_included=lambda world: world.can_access_fusion(),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.twin_ribbon,
        ItemClassification.useful,
        should_be_included=lambda world: world.can_access_fusion()
        and world.has_at_least_one_chapter_included([2, 3])
        and world.has_at_least_one_chapter_included([1, 2, 3]),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.spikeband,
        ItemClassification.useful,
        should_be_included=lambda world: world.can_access_fusion()
        and world.include_chapter(1)
        and world.has_at_least_one_chapter_included([2, 4]),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.tensionbow,
        ItemClassification.useful,
        should_be_included=lambda world: world.can_access_fusion()
        and world.include_chapter(2)
        and not world.is_weird_route(),
        groups=[ItemGroups.tension_items, ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.progressive_kris_weapons,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_kris_weapons_progressive(),
        groups=[ItemGroups.weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.progressive_susie_weapons,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_susie_weapons_progressive(),
        groups=[ItemGroups.weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.progressive_ralsei_weapons,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_ralsei_weapons_progressive(),
        groups=[ItemGroups.weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.progressive_noelle_weapons,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=lambda world: world.include_chapter(2) and world.is_noelle_weapons_progressive(),
        groups=[ItemGroups.weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.twistedswd,
        ItemClassification.useful,
        should_be_included=lambda world: world.can_access_fusion()
        and world.include_chapter(2)
        and world.is_unused_items_included()
        and world.is_weird_route(),
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.purecrystal,
        ItemClassification.progression,
        should_be_included=lambda world: world.can_access_fusion()
        and world.include_chapter(2)
        and world.is_unused_items_included()
        and world.is_weird_route(),
        groups=[ItemGroups.fusion_ingredient, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.everybodyweapon,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_everybodyweapon_included(),
        groups=[
            ItemGroups.weapons,
            ItemGroups.kris_weapons,
            ItemGroups.susie_weapons,
            ItemGroups.ralsei_weapons,
            ItemGroups.noelle_weapons,
            ItemGroups.unused_items,
        ],
        amount=4,
    ),
]

def create_items(world: "DeltaruneWorld"):
    return generic_create_items(world, cross_chapter_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, cross_chapter_items)

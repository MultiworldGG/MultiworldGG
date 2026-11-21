from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
from worlds.deltarune.LogicHelper import (
    include_unused_items,
    randomized_chapters,
    normal_route,
    weird_route,
    include_hidden_items,
    include_hidden_items_chapter2_weird_route_exclusion,
    include_secret_bosses_items_requirement_chapter2_weird_route_exclusion,
    include_secret_bosses_items_reward,
    include_secret_bosses_items_reward_chapter2_weird_route_exclusion,
    progressive_area_unlocks,
    normal_route_and_not_progressive_area_unlocks,
    not_progressive_area_unlocks,
)
from worlds.deltarune.Items import (
    DeltaruneItem,
    ItemData,
    ItemGroups,
    ItemIDs,
    generic_create_items,
    generic_get_filler_and_trap_items,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter2_items = [
    ItemData(ItemIDs.cd_bagel, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.lightcandy, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.clubsandwich, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.revivemint, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.spincake, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.tensiongem, ItemClassification.filler, groups=[ItemGroups.tension_items]),
    ItemData(
        ItemIDs.joe_life_savings,
        ItemClassification.filler,
        groups=[ItemGroups.currencies],
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.mechasaber, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons], amount=1
    ),
    ItemData(
        ItemIDs.autoaxe, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons], amount=1
    ),
    ItemData(
        ItemIDs.fiberscarf, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons], amount=1
    ),
    ItemData(
        ItemIDs.ragger2, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons], amount=1
    ),
    ItemData(
        ItemIDs.bounceblade, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons], amount=1
    ),
    ItemData(
        ItemIDs.progressive_ch2_area_unlock, 
        ItemClassification.progression,
        groups=[ItemGroups.region_blockers, ItemGroups.progressive_area_unlocks], 
        should_be_included=progressive_area_unlocks,
        amount=2
    ),
    ItemData(
        ItemIDs.tensionbit,
        ItemClassification.filler,
        groups=[ItemGroups.tension_items, ItemGroups.fusion_ingredient],
        changing_classification=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.glowwrist,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        amount=2,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.pink_ribbon,
        ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
        amount=1,
    ),
    ItemData(ItemIDs.silver_watch, ItemClassification.useful, groups=[ItemGroups.armors], amount=1),
    ItemData(
        ItemIDs.safety_vest, 
        ItemClassification.progression, 
        groups=[ItemGroups.region_blockers], 
        should_be_included=not_progressive_area_unlocks,
        amount=1
    ),
    ItemData(
        ItemIDs.keygen_2_segment,
        ItemClassification.progression_skip_balancing,
        groups=[ItemGroups.region_blockers],
        amount=0,
    ),
    ItemData(
        ItemIDs.mannequin,
        ItemClassification.filler,
        groups=[ItemGroups.armors],
        should_be_included=normal_route,
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.spagetticode,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.butjuice,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.kris_tea,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.noelle_tea,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.ralsei_tea,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.susie_tea,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.revivedust,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.royalpin,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.frayedbowtie,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.glowshard,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.currencies],
    ),
    ItemData(
        ItemIDs.dogdollar,
        ItemClassification.filler,
        should_be_included=include_hidden_items_chapter2_weird_route_exclusion,
        groups=[ItemGroups.currencies, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.chapter_2_egg,
        ItemClassification.filler,
        should_be_included=include_hidden_items_chapter2_weird_route_exclusion,
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.city_moss,
        ItemClassification.filler,
        should_be_included=include_hidden_items_chapter2_weird_route_exclusion,
        groups=[ItemGroups.moss],
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.chainmail,
        ItemClassification.useful,
        should_be_included=normal_route,
        groups=[ItemGroups.armors],
        amount=1,
    ),
    ItemData(
        ItemIDs.brokenswd,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.weapons],
        blacklist_filler=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.mansion_reservation,
        ItemClassification.progression,
        should_be_included=normal_route_and_not_progressive_area_unlocks,
        groups=[ItemGroups.region_blockers],
        amount=1,
    ),
    ItemData(
        ItemIDs.bshotbowtie,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
        amount=1,
    ),
    ItemData(
        ItemIDs.freezering,
        ItemClassification.useful,
        should_be_included=weird_route,
        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons],
        amount=1,
    ),
    ItemData(
        ItemIDs.thornring,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=weird_route,
        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons, ItemGroups.fusion_ingredient],
        amount=1,
    ),
    ItemData(
        ItemIDs.chapter_2_unlock,
        ItemClassification.progression,
        should_be_included=randomized_chapters,
        groups=[ItemGroups.region_blockers],
        amount=1,
    ),
    ItemData(
        ItemIDs.emptydisk,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement_chapter2_weird_route_exclusion,
        groups=[ItemGroups.spamton_access],
        amount=1,
    ),
    ItemData(
        ItemIDs.keygen,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement_chapter2_weird_route_exclusion,
        groups=[ItemGroups.spamton_access],
        amount=1,
    ),
    ItemData(
        ItemIDs.dealmaker,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward_chapter2_weird_route_exclusion,
        groups=[ItemGroups.armors],
        amount=1,
    ),
    ItemData(
        ItemIDs.puppetscarf,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons],
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
        ItemIDs.javacookie,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.revivebrite,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.mannequin_consumable,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.darkgoldband,
        ItemClassification.filler,
        should_be_included=include_unused_items,
        groups=[ItemGroups.currencies, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.skymantle,
        ItemClassification.useful,
        should_be_included=include_unused_items,
        groups=[ItemGroups.armors, ItemGroups.unused_items],
        amount=1,
    ),
    ItemData(
        ItemIDs.spikeshackle,
        ItemClassification.useful,
        should_be_included=include_unused_items,
        groups=[ItemGroups.armors, ItemGroups.unused_items],
        amount=1,
    ),
    ItemData(
        ItemIDs.cheerscarf,
        ItemClassification.useful,
        should_be_included=include_unused_items,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons, ItemGroups.unused_items],
        amount=1,
    ),
]

def create_items(world: "DeltaruneWorld") -> list[DeltaruneItem]:
    return generic_create_items(world, chapter2_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter2_items)

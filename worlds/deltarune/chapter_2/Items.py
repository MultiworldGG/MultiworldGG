from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
from worlds.deltarune.LogicHelper import (
    randomized_chapters,
    normal_route,
    weird_route,
    include_hidden_items,
    include_hidden_items_chapter2_weird_route_exclusion,
    include_secret_bosses_items_requirement_chapter2_weird_route_exclusion,
    include_secret_bosses_items_reward,
    include_secret_bosses_items_reward_chapter2_weird_route_exclusion,
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
    ItemData(ItemIDs.revivemint, ItemClassification.filler, groups=[ItemGroups.healing_item], amount=2),
    ItemData(ItemIDs.spincake, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.tensiongem, ItemClassification.filler, groups=[ItemGroups.tension_items]),
    ItemData(
        ItemIDs.joe_life_savings,
        ItemClassification.filler,
        groups=[ItemGroups.currencies],
        blacklist_filler=True,
    ),
    ItemData(ItemIDs.mechasaber, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    ItemData(ItemIDs.autoaxe, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons]),
    ItemData(ItemIDs.fiberscarf, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons]),
    ItemData(ItemIDs.ragger2, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons]),
    ItemData(ItemIDs.bounceblade, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    # Noelle royal pin
    ItemData(ItemIDs.royalpin, ItemClassification.useful, groups=[ItemGroups.armors]),
    ItemData(
        ItemIDs.tensionbit,
        ItemClassification.filler,
        groups=[ItemGroups.tension_items, ItemGroups.fusion_ingredient],
        changing_classification=True,
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
    ),
    ItemData(ItemIDs.safety_vest, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
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
        ItemClassification.useful,
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
        amount=1,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.chapter_2_egg,
        ItemClassification.filler,
        should_be_included=include_hidden_items_chapter2_weird_route_exclusion,
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.city_moss,
        ItemClassification.filler,
        should_be_included=include_hidden_items_chapter2_weird_route_exclusion,
        groups=[ItemGroups.moss],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.chainmail,
        ItemClassification.useful,
        should_be_included=normal_route,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.brokenswd,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.weapons],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.mansion_reservation,
        ItemClassification.progression,
        should_be_included=normal_route,
        groups=[ItemGroups.region_blockers],
    ),
    ItemData(
        ItemIDs.bshotbowtie,
        ItemClassification.filler,
        should_be_included=normal_route,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.freezering,
        ItemClassification.useful,
        should_be_included=weird_route,
        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons],
    ),
    ItemData(
        ItemIDs.thornring,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=weird_route,
        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons, ItemGroups.fusion_ingredient],
    ),
    ItemData(
        ItemIDs.chapter_2_unlock,
        ItemClassification.progression,
        should_be_included=randomized_chapters,
        groups=[ItemGroups.region_blockers],
    ),
    ItemData(
        ItemIDs.emptydisk,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement_chapter2_weird_route_exclusion,
        groups=[ItemGroups.spamton_access],
    ),
    ItemData(
        ItemIDs.keygen,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement_chapter2_weird_route_exclusion,
        groups=[ItemGroups.spamton_access],
    ),
    ItemData(
        ItemIDs.dealmaker,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward_chapter2_weird_route_exclusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.puppetscarf,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons],
    ),
    ItemData(
        ItemIDs.shadowcrystal,
        ItemClassification.filler,
        should_be_included=include_secret_bosses_items_reward,
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.javacookie,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.revivebrite,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.mannequin_consumable,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.darkgoldband,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.currencies, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.skymantle,
        ItemClassification.useful,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.armors, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.spikeshackle,
        ItemClassification.useful,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.armors, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.cheerscarf,
        ItemClassification.useful,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons, ItemGroups.unused_items],
    ),
]

def create_items(world: "DeltaruneWorld") -> list[DeltaruneItem]:
    return generic_create_items(world, chapter2_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter2_items)

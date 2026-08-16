from typing import TYPE_CHECKING
from BaseClasses import ItemClassification

from worlds.deltarune.Items import (
    ItemIDs,
    ItemData,
    ItemData,
    generic_create_items,
    generic_get_filler_and_trap_items,
    DeltaruneItem,
    ItemGroups,
)
from worlds.deltarune.LogicHelper import (
    include_hidden_items,
    include_mysterykey,
    include_secret_bosses_items_requirement,
    include_secret_bosses_items_reward,
    include_unused_items,
    not_weird_route_only,
    randomized_chapters,
)
from worlds.deltarune.Options import ChosenRoute

if TYPE_CHECKING:
    from .. import DeltaruneWorld

chapter5_items = [
    ItemData(ItemIDs.flavinge, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.greentea, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.revivemint, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.spincake, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.orangejuice, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.s_potion, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.raw_moon, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.phanta, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.flowerysoda, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.shikacola, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.schadenbrot, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.treecake, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.flowerydollars_10, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.flowerydollars_25, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.flowerydollars_50, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.flowerydollars_100, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.netskiehat, ItemClassification.filler, groups=[ItemGroups.armors], amount=3),
    ItemData(ItemIDs.redribbon, ItemClassification.filler, groups=[ItemGroups.armors], amount=3),
    ItemData(
        ItemIDs.chapter_5_egg,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.castle_moss,
        ItemClassification.filler,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.moss],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.shadowcrystal,
        ItemClassification.filler,
        should_be_included=include_secret_bosses_items_reward,
        blacklist_filler=True,
    ),
    ItemData(ItemIDs.susie_can_wear_ribbons, ItemClassification.useful),
    ItemData(ItemIDs.woodblade2, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    ItemData(ItemIDs.thatchet, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons]),
    ItemData(ItemIDs.mistlewp, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons]),
    ItemData(
        ItemIDs.gildedrose,
        ItemClassification.useful,
        should_be_included=include_unused_items,
        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons],
    ),
    ItemData(
        ItemIDs.dogdollar,
        ItemClassification.progression | ItemClassification.deprioritized,
        should_be_included=include_hidden_items,
        groups=[ItemGroups.currencies, ItemGroups.fusion_ingredient],
        amount=1,
        changing_classification=True,
    ),
    ItemData(ItemIDs.petalfeather, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(ItemIDs.compliment_list_yellow, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(ItemIDs.compliment_list_green, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(
        ItemIDs.jarona_lesson,
        ItemClassification.progression_skip_balancing,
        groups=[ItemGroups.region_blockers],
        amount=0,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.chapter_5_unlock,
        ItemClassification.progression,
        should_be_included=randomized_chapters,
        groups=[ItemGroups.region_blockers],
    ),
    ItemData(
        ItemIDs.pinkcoin,
        ItemClassification.progression,
        should_be_included=include_secret_bosses_items_requirement,
        amount=19,
    ),
    ItemData(
        ItemIDs.pinkkey,
        ItemClassification.progression,
        should_be_included=include_mysterykey,
    ),
    ItemData(
        ItemIDs.aquaknife,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons],
    ),
    ItemData(
        ItemIDs.blueshoes,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons],
    ),
    ItemData(
        ItemIDs.greenapron,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.yellowhat,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.ogloves,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.sethspecs,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.brokenscarf,
        ItemClassification.useful,
        should_be_included=include_secret_bosses_items_reward,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons],
    ),
]


def create_items(world: "DeltaruneWorld") -> list[DeltaruneItem]:
    if world.options.chosen_route.value == ChosenRoute.option_weird_route:
        return generic_create_items(
            world,
            [
                ItemData(
                    ItemIDs.chapter_5_unlock,
                    ItemClassification.progression,
                    should_be_included=randomized_chapters,
                    groups=[ItemGroups.region_blockers],
                )
            ],
        )

    return generic_create_items(world, chapter5_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    if world.options.chosen_route.value == ChosenRoute.option_weird_route:
        return []
    return generic_get_filler_and_trap_items(world, chapter5_items)

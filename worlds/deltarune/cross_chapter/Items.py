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
from worlds.deltarune.LogicHelper import (
    can_access_fusion,
    include_actions,
    include_characters,
    include_deluxedinner_fusion,
    include_dogwidow_fusion,
    include_everybodyweapon,
    include_kris,
    include_lancer_cookie,
    include_monarchrbn_fusion,
    include_noelle,
    include_punchbowl_fusion,
    include_spike_band_fusion,
    include_tensionbow_fusion,
    include_tensionmax_fusion,
    include_truetie_fusion,
    include_tvdinner_fusion,
    include_twin_ribbon_fusion,
    include_twistedsword_fusion,
    progressive_weapons_kris,
    progressive_weapons_noelle,
    progressive_weapons_ralsei,
    progressive_weapons_susie,
)
from worlds.deltarune.Options import ChosenRoute

if TYPE_CHECKING:
    from .. import DeltaruneWorld


cross_chapter_items = [
    # Traps
    ItemData(
        ItemIDs.spoison,
        ItemClassification.trap,
        groups=[ItemGroups.traps],
    ),
    ItemData(
        ItemIDs.bromider,
        ItemClassification.trap,
        groups=[ItemGroups.traps],
    ),
    ItemData(
        ItemIDs.bromidef,
        ItemClassification.trap,
        groups=[ItemGroups.traps],
    ),
    # The rest
    ItemData(
        ItemIDs.lancer_cookie,
        ItemClassification.filler,
        should_be_included=include_lancer_cookie,
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
        should_be_included=include_actions,
    ),
    ItemData(
        ItemIDs.kris,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=include_kris,
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.susie,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=include_characters,
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.ralsei,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=include_characters,
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.noelle,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=include_noelle,
        groups=[ItemGroups.characters],
    ),
    ItemData(
        ItemIDs.dd_burger,
        ItemClassification.filler,
        should_be_included=can_access_fusion,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.silver_card,
        ItemClassification.filler,
        should_be_included=can_access_fusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.twin_ribbon,
        ItemClassification.useful,
        should_be_included=include_twin_ribbon_fusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.spikeband,
        ItemClassification.useful,
        should_be_included=include_spike_band_fusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.tensionbow,
        ItemClassification.useful,
        should_be_included=include_tensionbow_fusion,
        groups=[ItemGroups.tension_items, ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.progressive_kris_weapons,
        ItemClassification.useful,
        should_be_included=progressive_weapons_kris,
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons, ItemGroups.progressive_weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.progressive_susie_weapons,
        ItemClassification.useful,
        should_be_included=progressive_weapons_susie,
        groups=[ItemGroups.weapons, ItemGroups.susie_weapons, ItemGroups.progressive_weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.progressive_ralsei_weapons,
        ItemClassification.useful,
        should_be_included=progressive_weapons_ralsei,
        groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons, ItemGroups.progressive_weapons],
        amount=0,
        changing_classification=True,
    ),
    ItemData(
        ItemIDs.progressive_noelle_weapons,
        ItemClassification.progression | ItemClassification.useful,
        should_be_included=progressive_weapons_noelle,
        groups=[ItemGroups.weapons, ItemGroups.noelle_weapons, ItemGroups.progressive_weapons],
        amount=0,
    ),
    ItemData(
        ItemIDs.twistedswd,
        ItemClassification.useful,
        should_be_included=include_twistedsword_fusion,
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.purecrystal,
        ItemClassification.progression,
        should_be_included=include_twistedsword_fusion,
        groups=[ItemGroups.fusion_ingredient, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.deluxedinner,
        ItemClassification.filler,
        should_be_included=include_deluxedinner_fusion,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.tvdinner,
        ItemClassification.filler,
        should_be_included=include_tvdinner_fusion,
        groups=[ItemGroups.healing_item, ItemGroups.fusion_ingredient],
    ),
    ItemData(
        ItemIDs.tensionmax,
        ItemClassification.filler,
        should_be_included=include_tensionmax_fusion,
        groups=[ItemGroups.tension_items],
    ),
    ItemData(
        ItemIDs.punchbowl,
        ItemClassification.filler,
        should_be_included=include_punchbowl_fusion,
        groups=[ItemGroups.healing_item],
    ),
    ItemData(
        ItemIDs.monarchrbn,
        ItemClassification.useful,
        should_be_included=include_monarchrbn_fusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.truetie,
        ItemClassification.useful,
        should_be_included=include_truetie_fusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.dogwidow,
        ItemClassification.useful,
        should_be_included=include_dogwidow_fusion,
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.everybodyweapon,
        ItemClassification.useful,
        should_be_included=include_everybodyweapon,
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
    if world.included_chapters == [5] and world.options.chosen_route.value == ChosenRoute.option_weird_route:
        return []

    return generic_create_items(world, cross_chapter_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    if world.included_chapters == [5] and world.options.chosen_route.value == ChosenRoute.option_weird_route:
        return []

    return generic_get_filler_and_trap_items(world, cross_chapter_items)

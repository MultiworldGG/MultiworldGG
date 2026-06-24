from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
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
    ItemData(ItemIDs.dice_brace, ItemClassification.useful, groups=[ItemGroups.armors]),
    ItemData(ItemIDs.spookysword, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    ItemData(ItemIDs.brave_ax, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons]),
    ItemData(ItemIDs.ragger, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons]),
    ItemData(ItemIDs.daintyscarf, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons]),
    ItemData(ItemIDs.manual, ItemClassification.progression, amount=2),
    ItemData(ItemIDs.bake_sale_ticket, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(ItemIDs.castle_key, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(ItemIDs.brokencake, ItemClassification.progression),
    ItemData(ItemIDs.top_cake, ItemClassification.progression),
    ItemData(
        ItemIDs.ironshackle,
        ItemClassification.progression | ItemClassification.useful,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
    ),
    ItemData(
        ItemIDs.white_ribbon,
        ItemClassification.progression,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
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
        should_be_included=lambda world: world.is_hidden_items_randomized(),
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.castle_moss,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_hidden_items_randomized(),
        groups=[ItemGroups.moss],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.broken_key_a,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_secret_bosses_items_requirement_randomized(),
        groups=[ItemGroups.jevil_keys],
    ),
    ItemData(
        ItemIDs.broken_key_b,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_secret_bosses_items_requirement_randomized(),
        groups=[ItemGroups.jevil_keys],
    ),
    ItemData(
        ItemIDs.broken_key_c,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_secret_bosses_items_requirement_randomized(),
        groups=[ItemGroups.jevil_keys],
    ),
    ItemData(
        ItemIDs.door_key,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_secret_bosses_items_requirement_randomized(),
        groups=[ItemGroups.jevil_keys],
    ),
    ItemData(
        ItemIDs.jevilstail,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_secret_bosses_randomized(),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.devilsknife,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_secret_bosses_randomized(),
        groups=[ItemGroups.weapons, ItemGroups.susie_weapons],
    ),
    ItemData(
        ItemIDs.shadowcrystal,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_secret_bosses_randomized(),
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.chapter_1_unlock,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_chapters_randomized(),
        groups=[ItemGroups.region_blockers],
    ),
    ItemData(
        ItemIDs.brokencake_consumable,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_unused_items_included(),
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.gigasalad,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_unused_items_included(),
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.favsandwich,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_unused_items_included(),
        groups=[ItemGroups.healing_item, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.mouse_token,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_unused_items_included(),
        groups=[ItemGroups.armors, ItemGroups.unused_items],
    ),
    ItemData(
        ItemIDs.trefoil,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_unused_items_included(),
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons, ItemGroups.unused_items],
    ),
]


def create_items(world: "DeltaruneWorld"):
    return generic_create_items(world, chapter1_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter1_items)

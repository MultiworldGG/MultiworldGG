from typing import TYPE_CHECKING
from BaseClasses import ItemClassification
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

chapter3_items = [
    ItemData(ItemIDs.flatsoda, ItemClassification.filler, groups=[ItemGroups.healing_item], amount=0),
    ItemData(ItemIDs.tvslop, ItemClassification.filler, groups=[ItemGroups.healing_item], amount=3),
    ItemData(ItemIDs.deluxedinner, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.tvdinner, ItemClassification.filler, groups=[ItemGroups.healing_item], amount=3),
    ItemData(ItemIDs.revivemint, ItemClassification.filler, groups=[ItemGroups.healing_item], amount=2),
    ItemData(ItemIDs.execbuffet, ItemClassification.filler, groups=[ItemGroups.healing_item]),
    ItemData(ItemIDs.dogdollar, ItemClassification.filler, groups=[ItemGroups.currencies], amount=0),
    ItemData(ItemIDs.point_1, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.points_2, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.points_10, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.points_50, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.points_120, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.points_300, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.points_500, ItemClassification.filler, groups=[ItemGroups.currencies]),
    ItemData(ItemIDs.tensiongem, ItemClassification.filler, groups=[ItemGroups.tension_items]),
    ItemData(ItemIDs.tensionmax, ItemClassification.filler, groups=[ItemGroups.tension_items], amount=0),
    ItemData(ItemIDs.smile, ItemClassification.filler),
    ItemData(ItemIDs.lodestone, ItemClassification.filler, groups=[ItemGroups.armors]),
    ItemData(ItemIDs.gingerguard, ItemClassification.filler, groups=[ItemGroups.armors]),
    ItemData(ItemIDs.toxicaxe, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.susie_weapons]),
    ItemData(ItemIDs.saber10, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.kris_weapons]),
    ItemData(ItemIDs.flexscarf, ItemClassification.useful, groups=[ItemGroups.weapons, ItemGroups.ralsei_weapons]),
    ItemData(ItemIDs.execbuffet, ItemClassification.useful, groups=[ItemGroups.healing_item]),
    ItemData(
        ItemIDs.white_ribbon,
        ItemClassification.progression,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
    ),
    ItemData(
        ItemIDs.pink_ribbon,
        ItemClassification.progression,
        groups=[ItemGroups.armors, ItemGroups.fusion_ingredient],
    ),
    ItemData(ItemIDs.board_2_cartridge, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(ItemIDs.vip_pass, ItemClassification.progression, groups=[ItemGroups.region_blockers]),
    ItemData(
        ItemIDs.remote_battery,
        ItemClassification.progression_skip_balancing,
        groups=[ItemGroups.region_blockers],
        amount=0,
    ),
    ItemData(
        ItemIDs.tennatie,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_hidden_items_randomized(),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.blue_ribbon,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_hidden_items_randomized(),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.shadowmantle,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_shadow_mantle_included()
        and (world.is_mantle_randomized() or world.is_mantleless()),
        groups=[ItemGroups.armors],
    ),
    ItemData(
        ItemIDs.blackshard,
        ItemClassification.useful,
        should_be_included=lambda world: world.is_secret_bosses_randomized(),
        groups=[ItemGroups.weapons, ItemGroups.kris_weapons],
    ),
    ItemData(
        ItemIDs.shadowcrystal,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_secret_bosses_randomized(),
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.chapter_3_egg,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_hidden_items_randomized(),
        groups=[ItemGroups.eggs],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.board_moss,
        ItemClassification.filler,
        should_be_included=lambda world: world.is_hidden_items_randomized()
        and ((not world.is_weird_route()) or world.is_all_routes()),
        groups=[ItemGroups.moss],
        blacklist_filler=True,
    ),
    ItemData(
        ItemIDs.chapter_3_unlock,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_chapters_randomized(),
        groups=[ItemGroups.region_blockers],
    ),
    ItemData(
        ItemIDs.odd_controller,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_mantle_randomized() or world.is_mantleless(),
        groups=[ItemGroups.mantle_items],
    ),
    ItemData(
        ItemIDs.ice_key,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_mantle_randomized() or world.is_mantleless(),
        groups=[ItemGroups.mantle_items],
    ),
    ItemData(
        ItemIDs.shelter_key,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_mantle_randomized() or world.is_mantleless(),
        groups=[ItemGroups.mantle_items],
    ),
    ItemData(
        ItemIDs.tripticket,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_hidden_items_randomized()
        and ((not world.is_weird_route()) or world.is_all_routes()),
        groups=[ItemGroups.mantle_items],
    ),
]


def create_items(world: "DeltaruneWorld") -> list[DeltaruneItem]:
    return generic_create_items(world, chapter3_items)


def get_filler_and_trap_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter3_items)

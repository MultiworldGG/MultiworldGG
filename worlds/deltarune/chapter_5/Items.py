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

chapter5_items = [
    ItemData(
        ItemIDs.chapter_5_unlock,
        ItemClassification.progression,
        should_be_included=lambda world: world.is_chapters_randomized(),
        groups=[ItemGroups.region_blockers],
    )
]


def create_items(world: "DeltaruneWorld") -> list[DeltaruneItem]:
    return generic_create_items(world, chapter5_items, chapter5_items)


def get_filler_items(world: "DeltaruneWorld"):
    return generic_get_filler_and_trap_items(world, chapter5_items, chapter5_items)

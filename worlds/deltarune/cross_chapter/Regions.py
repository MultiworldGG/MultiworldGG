from enum import StrEnum
from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.options import OptionFilter
from rule_builder.rules import Has
from worlds.deltarune.Options import RandomizeChapters
from worlds.deltarune.Regions import Regions, add_location_to_region
from worlds.deltarune.cross_chapter.Locations import cross_chapter_locations
from worlds.deltarune.Items import items, ItemIDs

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    chapter_select = Region(Regions.chapter_select, world.player, world.multiworld)
    fusion = Region(Regions.fusion, world.player, world.multiworld)

    regions = [chapter_select, fusion]

    if world.has_at_least_one_chapter_included([1, 3]):
        lost_rabbick = Region(Regions.lost_rabbick, world.player, world.multiworld)
        regions.append(lost_rabbick)

    if world.include_chapter(1):
        chapter_1 = Region(Regions.chapter_1, world.player, world.multiworld)
        chapter_select.connect(
            chapter_1,
            "Chapter 1",
            Has(items[ItemIDs.chapter_1_unlock])
            | OptionFilter(RandomizeChapters, RandomizeChapters.option_all_unlocked),
        )
        regions.append(chapter_1)

    if world.include_chapter(2):
        chapter_2 = Region(Regions.chapter_2, world.player, world.multiworld)
        chapter_select.connect(
            chapter_2,
            "Chapter 2",
            Has(items[ItemIDs.chapter_2_unlock])
            | OptionFilter(RandomizeChapters, RandomizeChapters.option_all_unlocked),
        )
        chapter_2.connect(fusion)
        regions.append(chapter_2)

    if world.include_chapter(3):
        chapter_3 = Region(Regions.chapter_3, world.player, world.multiworld)
        chapter_select.connect(
            chapter_3,
            "Chapter 3",
            Has(items[ItemIDs.chapter_3_unlock])
            | OptionFilter(RandomizeChapters, RandomizeChapters.option_all_unlocked),
        )
        regions.append(chapter_3)

    if world.include_chapter(4):
        chapter_4 = Region(Regions.chapter_4, world.player, world.multiworld)
        chapter_select.connect(
            chapter_4,
            "Chapter 4",
            Has(items[ItemIDs.chapter_4_unlock])
            | OptionFilter(RandomizeChapters, RandomizeChapters.option_all_unlocked),
        )
        chapter_4.connect(fusion)
        regions.append(chapter_4)

    for region in regions:
        if region.name in cross_chapter_locations:
            add_location_to_region(region, cross_chapter_locations[region.name], world)
        world.multiworld.regions.append(region)

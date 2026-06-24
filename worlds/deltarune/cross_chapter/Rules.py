from rule_builder.options import OptionFilter
from rule_builder.rules import Has, True_

from worlds.deltarune.Options import (
    IncludeChapter1,
    IncludeChapter2,
    IncludeChapter3,
    IncludeChapter4,
    RandomizeChapters,
    RemoveStartingEquipment,
)
from worlds.generic.Rules import set_rule

from typing import TYPE_CHECKING

from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import glitched_item_name, items, ItemIDs
from worlds.deltarune.Rules import have_thornring

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    if world.can_access_fusion():
        have_chapter2_equipment_not_in_order = [
            OptionFilter(IncludeChapter2, IncludeChapter2.option_true),
            OptionFilter(RemoveStartingEquipment, RemoveStartingEquipment.option_false),
            OptionFilter(RandomizeChapters, RandomizeChapters.option_in_order, operator="ne"),
        ]

        have_chapter2_equipment_in_order_glitched = Has(
            glitched_item_name,
            options=[
                OptionFilter(IncludeChapter1, IncludeChapter1.option_true),
                OptionFilter(IncludeChapter2, IncludeChapter2.option_true),
                OptionFilter(RemoveStartingEquipment, RemoveStartingEquipment.option_false),
                OptionFilter(RandomizeChapters, RandomizeChapters.option_in_order),
            ],
        )

        have_chapter2_equipment_first_chapter = [
            OptionFilter(IncludeChapter1, IncludeChapter1.option_false),
            OptionFilter(IncludeChapter2, IncludeChapter2.option_true),
            OptionFilter(RandomizeChapters, RandomizeChapters.option_in_order),
        ]

        have_white_ribbon = (
            Has(items[ItemIDs.white_ribbon])
            | have_chapter2_equipment_not_in_order
            | have_chapter2_equipment_in_order_glitched
            | have_chapter2_equipment_first_chapter
        )

        if world.has_at_least_one_chapter_included([2, 3]) and (
            (world.is_starting_equipment_removed() and world.has_at_least_one_chapter_included([1, 3]))
            or (not world.is_starting_equipment_removed() and world.has_at_least_one_chapter_included([1, 2, 3]))
        ):
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_twin_ribbon_fusion]),
                have_white_ribbon & Has(items[ItemIDs.pink_ribbon]),
            )

        have_glowwrist = (
            Has(items[ItemIDs.glowwrist])
            | True_(
                options=[
                    OptionFilter(IncludeChapter3, IncludeChapter3.option_true),
                    OptionFilter(RemoveStartingEquipment, RemoveStartingEquipment.option_false),
                ]
            )
            | True_(
                options=[
                    OptionFilter(IncludeChapter4, IncludeChapter4.option_true),
                    OptionFilter(RemoveStartingEquipment, RemoveStartingEquipment.option_false),
                ]
            )
        )

        if world.include_chapter(1) and (
            world.include_chapter(2)
            or (
                not world.is_starting_equipment_removed()
                and (world.include_chapter(4) or world.have_all_chapters_included([3, 4]))
            )
        ):
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_spike_band_fusion]),
                have_glowwrist & Has(items[ItemIDs.ironshackle]),
            )

        if world.include_chapter(2) and world.is_not_weird_route_only():
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_tensionbow_fusion]),
                Has(items[ItemIDs.bshotbowtie]) & Has(items[ItemIDs.tensionbit]),
            )

        # TwistedSwd
        if world.is_unused_items_included() and world.include_chapter(2) and world.is_weird_route():
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_twistedsword_fusion]),
                have_thornring & Has(items[ItemIDs.purecrystal]),
            )


def get_location(world: "DeltaruneWorld", chapter: int):
    if chapter == 1:
        return world.multiworld.get_location(locations[LocationIDs.ch1_fountain_sealed], world.player)
    if chapter == 2:
        return world.multiworld.get_location(locations[LocationIDs.ch2_fountain_sealed], world.player)
    if chapter == 3:
        return world.multiworld.get_location(locations[LocationIDs.ch3_fountain_sealed], world.player)
    if chapter == 4:
        return world.multiworld.get_location(locations[LocationIDs.ch4_third_sanctuary_fountain_sealed], world.player)


def get_unlock_item(world: "DeltaruneWorld", chapter: int):
    if chapter == 1:
        return items[ItemIDs.chapter_1_unlock]
    if chapter == 2:
        return items[ItemIDs.chapter_2_unlock]
    if chapter == 3:
        return items[ItemIDs.chapter_3_unlock]
    if chapter == 4:
        return items[ItemIDs.chapter_4_unlock]
    if chapter == 5:
        return items[ItemIDs.chapter_5_unlock]


def handle_locked_items(world: "DeltaruneWorld"):
    if world.is_chapters_in_order():
        playable_chapters = world.get_playable_chapters()

        for current_chapter in playable_chapters:
            next_chapter = world.get_next_in_order_chapter(current_chapter)
            if next_chapter == -1:
                continue

            get_location(world, current_chapter).place_locked_item(
                world.create_item(get_unlock_item(world, next_chapter))
            )

from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachRegion, Has, True_
from BaseClasses import LocationProgressType

from worlds.deltarune.LogicHelper import (
    all_included_chapter,
    both_routes,
    can_access_fusion,
    can_access_fusion_post_chapter_5,
    chapters_in_order,
    have_access_to_rock_video,
    include_dogwidow_fusion,
    include_hidden_items,
    include_spike_band_fusion,
    include_tensionbow_fusion,
    include_truetie_fusion,
    include_twin_ribbon_fusion,
    include_twistedsword_fusion,
    included_chapter,
    normal_route,
    not_weird_route_only,
    rock_video_sanity_enabled,
    rock_video_sanity_enabled_ch5,
    rock_video_sanity_hard_enabled,
    rock_video_sanity_hard_enabled_ch5,
    weird_route,
)
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
from worlds.deltarune.Items import ItemGroups, glitched_item_name, items, ItemIDs
from worlds.deltarune.Rules import have_thornring
from worlds.deltarune.Regions import Regions

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    if can_access_fusion(world):
        have_white_ribbon = Has(items[ItemIDs.white_ribbon]) | (
            CanReachRegion(
                Regions.chapter_2,
                options=[
                    OptionFilter(IncludeChapter2, IncludeChapter2.option_true),
                    OptionFilter(RemoveStartingEquipment, RemoveStartingEquipment.option_false),
                ],
            )
        )

        if include_twin_ribbon_fusion(world):
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_twin_ribbon_fusion]),
                have_white_ribbon & Has(items[ItemIDs.pink_ribbon]),
            )

        have_glowwrist = Has(items[ItemIDs.glowwrist]) | (
            CanReachRegion(
                Regions.chapter_4,
                options=[
                    OptionFilter(IncludeChapter4, IncludeChapter4.option_true),
                    OptionFilter(RemoveStartingEquipment, RemoveStartingEquipment.option_false),
                ],
            )
        )

        if include_spike_band_fusion(world):
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_spike_band_fusion]),
                have_glowwrist & Has(items[ItemIDs.ironshackle]),
            )

        if include_tensionbow_fusion(world):
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_tensionbow_fusion]),
                Has(items[ItemIDs.bshotbowtie]) & Has(items[ItemIDs.tensionbit]),
            )

        # TwistedSwd
        if include_twistedsword_fusion(world):
            world.set_rule(
                world.get_location(locations[LocationIDs.cc_castle_town_twistedsword_fusion]),
                have_thornring(world) & Has(items[ItemIDs.purecrystal]),
            )

        if can_access_fusion_post_chapter_5(world):
            if included_chapter(world, 4):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_monarchrbn_fusion]),
                    (
                        Has(items[ItemIDs.scarfmark])
                        | Has(
                            items[ItemIDs.progressive_ralsei_weapons],
                            world.get_weapon_progression_index(ItemGroups.ralsei_weapons, ItemIDs.scarfmark),
                        )
                    )
                    & Has(items[ItemIDs.princessrbn]),
                )

            if include_truetie_fusion(world):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_truetie_fusion]),
                    Has(items[ItemIDs.frayedbowtie]) & Has(items[ItemIDs.tennatie]),
                )

            if included_chapter(world, 3):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_tvdinner_fusion]),
                    Has(items[ItemIDs.tvslop], 2),
                )

            if included_chapter(world, 3):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_deluxedinner_fusion]),
                    Has(items[ItemIDs.tvdinner], 2),
                )

            if included_chapter(world, 4):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_punchbowl_fusion]),
                    Has(items[ItemIDs.scarlixir], 1) & Has(items[ItemIDs.powerband]),
                )

            if included_chapter(world, 4):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_tensionmax_fusion]),
                    Has(items[ItemIDs.scarlixir], 1) & Has(items[ItemIDs.mysticband]),
                )

            if included_chapter(world, 4):
                world.set_rule(
                    world.get_location(locations[LocationIDs.cc_castle_town_dogwidow_fusion]),
                    Has(items[ItemIDs.dogdollar]) & Has(items[ItemIDs.goldwidow]),
                )

    if rock_video_sanity_enabled(world) and have_access_to_rock_video(world):

        if world.options.exclude_t_rank_rock_video == 1:
            world.get_location(locations[LocationIDs.cc_rock_video_knock_you_down_T]).progress_type = LocationProgressType.EXCLUDED
            world.get_location(locations[LocationIDs.cc_rock_video_tv_time_T]).progress_type = LocationProgressType.EXCLUDED
            world.get_location(locations[LocationIDs.cc_rock_video_raise_up_your_bat_T]).progress_type = LocationProgressType.EXCLUDED

            if rock_video_sanity_enabled_ch5(world):
                world.get_location(locations[LocationIDs.cc_rock_video_4rd_sanctuary_T]).progress_type = LocationProgressType.EXCLUDED

            if rock_video_sanity_hard_enabled(world):
                world.get_location(locations[LocationIDs.cc_rock_video_knock_you_down_T_hard]).progress_type = LocationProgressType.EXCLUDED
                world.get_location(locations[LocationIDs.cc_rock_video_tv_time_T_hard]).progress_type = LocationProgressType.EXCLUDED
                world.get_location(locations[LocationIDs.cc_rock_video_raise_up_your_bat_T_hard]).progress_type = LocationProgressType.EXCLUDED

                if rock_video_sanity_hard_enabled_ch5(world):
                    world.get_location(locations[LocationIDs.cc_rock_video_4rd_sanctuary_T_hard]).progress_type = LocationProgressType.EXCLUDED

        if world.options.exclude_z_rank_rock_video == 1:
            world.get_location(locations[LocationIDs.cc_rock_video_knock_you_down_Z]).progress_type = LocationProgressType.EXCLUDED
            world.get_location(locations[LocationIDs.cc_rock_video_tv_time_Z]).progress_type = LocationProgressType.EXCLUDED
            world.get_location(locations[LocationIDs.cc_rock_video_raise_up_your_bat_Z]).progress_type = LocationProgressType.EXCLUDED

            if rock_video_sanity_enabled_ch5(world):
                world.get_location(locations[LocationIDs.cc_rock_video_4rd_sanctuary_Z]).progress_type = LocationProgressType.EXCLUDED


def get_location(world: "DeltaruneWorld", chapter: int):
    if chapter == 1:
        return world.get_location(locations[LocationIDs.ch1_fountain_sealed])
    if chapter == 2:
        if both_routes(world):
            return world.get_location(
                world.random.choice(
                    [locations[LocationIDs.ch2_fountain_sealed], locations[LocationIDs.ch2_fountain_sealed_weird_route]]
                )
            )
        elif normal_route(world):
            return world.get_location(locations[LocationIDs.ch2_fountain_sealed])
        elif weird_route(world):
            return world.get_location(locations[LocationIDs.ch2_fountain_sealed_weird_route])
    if chapter == 3:
        return world.get_location(locations[LocationIDs.ch3_fountain_sealed])
    if chapter == 4:
        return world.get_location(locations[LocationIDs.ch4_third_sanctuary_fountain_sealed])


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
    if chapters_in_order(world):
        for current_chapter in world.included_chapters:
            next_chapter = world.get_next_in_order_chapter(current_chapter)
            if next_chapter == -1:
                continue

            get_location(world, current_chapter).place_locked_item(
                world.create_item(get_unlock_item(world, next_chapter))
            )

    if include_truetie_fusion(world) and not include_hidden_items:
        world.get_location(locations[LocationIDs.cc_castle_town_truetie_fusion]).place_locked_item(
            world.create_item(items[ItemIDs.truetie])
        )

    if include_dogwidow_fusion(world) and not include_hidden_items:
        world.get_location(locations[LocationIDs.cc_castle_town_dogwidow_fusion]).place_locked_item(
            world.create_item(items[ItemIDs.dogwidow])
        )

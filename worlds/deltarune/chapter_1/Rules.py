from typing import TYPE_CHECKING
from rule_builder.rules import CanReachRegion, Has
from worlds.deltarune.Items import ItemIDs, items
from worlds.deltarune.Locations import LocationIDs, locations
from worlds.deltarune.Regions import Regions
from worlds.deltarune.Rules import (
    can_recruit_chapter1,
    have_kris_susie_or_ralsei,
    can_lost_chapter1_pre_castle,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    world.set_rule(
        world.get_location(locations[LocationIDs.ch1_bake_sale_repair_door_key]),
        Has(items[ItemIDs.broken_key_a]) & Has(items[ItemIDs.broken_key_b]) & Has(items[ItemIDs.broken_key_c]),
    )
    world.set_rule(
        world.get_location(locations[LocationIDs.ch1_seam_seap_talk_about_strange_prisoner]),
        CanReachRegion(Regions.ch1_card_castle),
    )

    # Cake quest
    world.set_rule(
        world.get_location(locations[LocationIDs.ch1_bake_sale_repair_top_cake]), Has(items[ItemIDs.brokencake])
    )
    world.set_rule(world.get_location(locations[LocationIDs.ch1_field_return_top_cake]), Has(items[ItemIDs.top_cake]))

    # Manuals
    world.set_rule(world.get_location(locations[LocationIDs.ch1_throw_away_manual]), Has(items[ItemIDs.manual]))
    world.set_rule(
        world.get_location(locations[LocationIDs.ch1_throw_away_manual_again]), Has(items[ItemIDs.manual], 2)
    )

    if world.is_chapter_1_recruit_system_enabled():
        if world.is_all_recruits():
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_rudinn]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_hathy]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_jigsawry]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_ponman]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_rabbick]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_bloxer]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_head_hathy]), can_recruit_chapter1)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_recruit_rudinn_ranger]), can_recruit_chapter1)

        if world.is_weird_route():
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_rudinn]), can_lost_chapter1_pre_castle)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_hathy]), can_lost_chapter1_pre_castle)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_jigsawry]), can_lost_chapter1_pre_castle)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_ponman]), can_lost_chapter1_pre_castle)
            world.set_rule(world.get_location(locations[LocationIDs.cc_lost_rabbick]), can_lost_chapter1_pre_castle)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_bloxer]), can_lost_chapter1_pre_castle)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_head_hathy]), have_kris_susie_or_ralsei)
            world.set_rule(world.get_location(locations[LocationIDs.ch1_lost_rudinn_ranger]), have_kris_susie_or_ralsei)


def handle_locked_items(world: "DeltaruneWorld"):
    if not world.is_secret_bosses_randomized():
        world.get_location(locations[LocationIDs.ch1_card_castle_jevil_1]).place_locked_item(
            world.create_item(items[ItemIDs.jevilstail])
        )
        world.get_location(locations[LocationIDs.ch1_card_castle_jevil_2]).place_locked_item(
            world.create_item(items[ItemIDs.devilsknife])
        )
        world.get_location(locations[LocationIDs.ch1_card_castle_jevil_3]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )

    # Hidden items
    if not world.is_hidden_items_randomized():
        world.get_location(locations[LocationIDs.ch1_forest_man]).place_locked_item(
            world.create_item(items[ItemIDs.chapter_1_egg])
        )
        world.get_location(locations[LocationIDs.ch1_card_castle_moss]).place_locked_item(
            world.create_item(items[ItemIDs.castle_moss])
        )

    if not world.is_secret_bosses_items_requirement_randomized():
        world.get_location(locations[LocationIDs.ch1_seam_seap_talk_about_strange_prisoner]).place_locked_item(
            world.create_item(items[ItemIDs.broken_key_a])
        )
        world.get_location(locations[LocationIDs.ch1_forest_hidden_chest_near_dancers]).place_locked_item(
            world.create_item(items[ItemIDs.broken_key_b])
        )
        world.get_location(locations[LocationIDs.ch1_field_chest_before_great_board]).place_locked_item(
            world.create_item(items[ItemIDs.broken_key_c])
        )
        world.get_location(locations[LocationIDs.ch1_bake_sale_repair_door_key]).place_locked_item(
            world.create_item(items[ItemIDs.door_key])
        )

from typing import TYPE_CHECKING
from BaseClasses import LocationProgressType
from rule_builder.rules import CanReachRegion, Has

from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.LogicHelper import (
    excluded_t_rank,
    excluded_z_rank,
    include_hidden_items,
    include_lose_recruits,
    include_mantle,
    include_recruits,
    include_secret_bosses_items_reward,
    include_shadow_mantle,
    randomized_mantle,
)
from worlds.deltarune.Regions import Regions
from worlds.deltarune.Rules import (
    can_recruit_shadowguy,
    can_recruit_pippins,
    can_recruit_shuttah,
    can_recruit_water_cooler,
    can_recruit_zapper,
    can_lost_chapter3,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    if include_recruits(world):
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_recruit_shadowguy]),
            can_recruit_shadowguy & (CanReachRegion(Regions.ch3_tv_world) | Has(glitched_item_name)),
        )
        world.set_rule(world.get_location(locations[LocationIDs.ch3_recruit_pippins]), can_recruit_pippins)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_recruit_shuttah]),
            can_recruit_shuttah & (CanReachRegion(Regions.ch3_tv_world) | Has(glitched_item_name)),
        )
        world.set_rule(world.get_location(locations[LocationIDs.ch3_recruit_water_cooler]), can_recruit_water_cooler)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_recruit_zapper]),
            can_recruit_zapper,
        )

    if include_lose_recruits(world) and not include_recruits(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch3_lost_shadowguy]), can_lost_chapter3)
        world.set_rule(world.get_location(locations[LocationIDs.ch3_lost_pippins]), can_lost_chapter3)
        world.set_rule(world.get_location(locations[LocationIDs.ch3_lost_shuttah]), can_lost_chapter3)
        world.set_rule(world.get_location(locations[LocationIDs.ch3_lost_water_cooler]), can_lost_chapter3)
        world.set_rule(world.get_location(locations[LocationIDs.ch3_lost_zapper]), can_lost_chapter3)
    elif include_lose_recruits(world):
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_lost_shadowguy]),
            can_lost_chapter3 & (CanReachRegion(Regions.ch3_tv_world) | Has(glitched_item_name)),
        )
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_lost_pippins]),
            can_lost_chapter3 & (CanReachRegion(Regions.ch3_tv_world) | Has(glitched_item_name)),
        )
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_lost_shuttah]),
            can_lost_chapter3 & (CanReachRegion(Regions.ch3_tv_world) | Has(glitched_item_name)),
        )
        world.set_rule(world.get_location(locations[LocationIDs.ch3_lost_water_cooler]), can_lost_chapter3)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch3_lost_zapper]),
            can_lost_chapter3 & (CanReachRegion(Regions.ch3_tv_world) | Has(glitched_item_name)),
        )

    world.set_rule(world.get_location(locations[LocationIDs.ch3_tv_world_man]), Has(items[ItemIDs.tripticket]))

    if excluded_t_rank(world):
        world.get_location(locations[LocationIDs.ch3_board_1_t_rank]).progress_type = LocationProgressType.EXCLUDED
        world.get_location(locations[LocationIDs.ch3_board_2_t_rank]).progress_type = LocationProgressType.EXCLUDED

    if excluded_z_rank(world):
        world.get_location(locations[LocationIDs.ch3_board_1_z_rank]).progress_type = LocationProgressType.EXCLUDED
        world.get_location(locations[LocationIDs.ch3_board_2_z_rank]).progress_type = LocationProgressType.EXCLUDED


def handle_locked_items(world: "DeltaruneWorld"):
    # MANTLE
    if not randomized_mantle(world):
        world.get_location(locations[LocationIDs.ch3_mantle_susie_gift]).place_locked_item(
            world.create_item(items[ItemIDs.flatsoda])
        )
        world.get_location(locations[LocationIDs.ch3_mantle_out_of_bounds_chest]).place_locked_item(
            world.create_item(items[ItemIDs.ice_key])
        )
        world.get_location(locations[LocationIDs.ch3_mantle_northern_light_item]).place_locked_item(
            world.create_item(items[ItemIDs.shelter_key])
        )
        world.get_location(locations[LocationIDs.ch3_s_rank_room_oddcontroller]).place_locked_item(
            world.create_item(items[ItemIDs.odd_controller])
        )

        if include_shadow_mantle(world):
            world.get_location(locations[LocationIDs.ch3_mantle_defeat]).progress_type = LocationProgressType.EXCLUDED

    if not include_shadow_mantle(world) and include_mantle(world):
        world.get_location(locations[LocationIDs.ch3_mantle_defeat]).place_locked_item(
            world.create_item(items[ItemIDs.shadowmantle])
        )

    # Secret Bosses
    if not include_secret_bosses_items_reward(world):
        world.get_location(locations[LocationIDs.ch3_cold_place_knight_defeat_item_1]).place_locked_item(
            world.create_item(items[ItemIDs.blackshard])
        )
        world.get_location(locations[LocationIDs.ch3_cold_place_knight_defeat_item_2]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )

    # Hidden items
    if not include_hidden_items(world):
        world.get_location(locations[LocationIDs.ch3_board_2_moss]).place_locked_item(
            world.create_item(items[ItemIDs.board_moss])
        )
        world.get_location(locations[LocationIDs.ch3_b_rank_room_golden_prize_1]).place_locked_item(
            world.create_item(items[ItemIDs.execbuffet])
        )
        world.get_location(locations[LocationIDs.ch3_b_rank_room_golden_prize_2]).place_locked_item(
            world.create_item(items[ItemIDs.tennatie])
        )
        world.get_location(locations[LocationIDs.ch3_b_rank_room_golden_prize_3]).place_locked_item(
            world.create_item(items[ItemIDs.tensionmax])
        )
        world.get_location(locations[LocationIDs.ch3_b_rank_room_golden_prize_4]).place_locked_item(
            world.create_item(items[ItemIDs.blue_ribbon])
        )
        world.get_location(locations[LocationIDs.ch3_b_rank_room_golden_prize_5]).place_locked_item(
            world.create_item(items[ItemIDs.revivemint])
        )

        world.get_location(locations[LocationIDs.ch3_tv_world_man]).place_locked_item(
            world.create_item(items[ItemIDs.chapter_3_egg])
        )
        world.get_location(locations[LocationIDs.ch3_tv_world_tripticket]).place_locked_item(
            world.create_item(items[ItemIDs.tripticket])
        )

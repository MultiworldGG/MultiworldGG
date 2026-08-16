from BaseClasses import LocationProgressType
from rule_builder.rules import Has

from typing import TYPE_CHECKING
from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import ItemIDs, items, glitched_item_name
from worlds.deltarune.LogicHelper import (
    all_recruits_route,
    include_actions,
    include_freeze_recruits_chapter2,
    include_hidden_items,
    include_lose_recruits,
    include_lose_swatchlings_weird_route,
    include_recruit_swatchlings_weird_route,
    include_recruits,
    include_secret_bosses_items_requirement,
    include_secret_bosses_items_reward,
    not_weird_route_only,
    weird_route,
)
from worlds.deltarune.Rules import (
    have_kris_susie_or_ralsei,
    have_noelle,
    can_lost_chapter2_with_noelle,
    have_kris_or_noelle,
    can_recruit_werewire,
    can_recruit_tasque,
    can_recruit_virovirokun,
    can_recruit_poppup,
    can_recruit_ambuy_lance,
    can_recruit_maus,
    can_recruit_swatchling,
    can_recruit_tasque_manager,
    can_recruit_mauswheel,
    can_recruit_werewerewire,
    can_lost_chapter2,
    can_lost_chapter2_with_noelle,
)

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    # Character requirement
    world.set_rule(
        world.get_location(locations[LocationIDs.ch2_castle_town_jigsaw_joe_challenge]), have_kris_susie_or_ralsei
    )
    world.set_rule(
        world.get_location(locations[LocationIDs.ch2_castle_town_clover_rematch_challenge]), have_kris_susie_or_ralsei
    )

    world.set_rule(world.get_location(locations[LocationIDs.ch2_cyber_city_cheese_maze_chest]), have_kris_or_noelle)

    if weird_route(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch2_cyber_city_purchase_freezering]), have_noelle)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_cyber_city_purchase_thornring]),
            have_noelle | Has(glitched_item_name),
        )

    if include_freeze_recruits_chapter2(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_werewire]), can_lost_chapter2)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_tasque]), can_lost_chapter2)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_virovirokun]), can_lost_chapter2)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_poppup]), can_lost_chapter2_with_noelle)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_ambyu_lance]), can_lost_chapter2_with_noelle)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_maus]), can_lost_chapter2_with_noelle)
    if include_lose_recruits(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_tasque_manager]), can_lost_chapter2)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_mauswheel]), can_lost_chapter2)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_werewerewire]), can_lost_chapter2)
        if include_lose_swatchlings_weird_route(world):
            world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_swatchlings]), can_lost_chapter2)

    if include_recruits(world):
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_werewire]), can_recruit_werewire)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_tasque]), can_recruit_tasque)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_virovirokun]), can_recruit_virovirokun)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_poppup]), can_recruit_poppup)
        if not weird_route(world):
            world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_ambyu_lance]), can_recruit_ambuy_lance)
            world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_maus]), can_recruit_maus)
        if include_recruit_swatchlings_weird_route(world):
            world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_swatchling]), can_recruit_swatchling)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_recruit_tasque_manager]), can_recruit_tasque_manager
        )
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_mauswheel]), can_recruit_mauswheel)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_werewerewire]), can_recruit_werewerewire)

        if all_recruits_route(world) and world.options.exclude_post_chapter_2_locations.value == 1:
            world.get_location(locations[LocationIDs.ch2_castle_town_tasque_manager_says_challenge]).progress_type = (
                LocationProgressType.EXCLUDED
            )
            world.get_location(locations[LocationIDs.ch2_castle_town_all_stars_challenge]).progress_type = (
                LocationProgressType.EXCLUDED
            )


def handle_locked_items(world: "DeltaruneWorld"):
    if not include_actions(world):
        world.get_location(locations[LocationIDs.ch2_cyber_field_fun_gang_actions_unlock]).place_locked_item(
            world.create_item(items[ItemIDs.s_r_n_actions])
        )

    if not include_secret_bosses_items_reward(world):
        world.get_location(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_1]).place_locked_item(
            world.create_item(items[ItemIDs.puppetscarf])
        )
        world.get_location(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_2]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )
        if not_weird_route_only(world):
            world.get_location(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_3]).place_locked_item(
                world.create_item(items[ItemIDs.dealmaker])
            )

    # Hidden items
    if not_weird_route_only(world):
        if not include_hidden_items(world):
            world.get_location(locations[LocationIDs.ch2_cyber_city_man]).place_locked_item(
                world.create_item(items[ItemIDs.chapter_2_egg])
            )
            world.get_location(locations[LocationIDs.ch2_cyber_city_moss]).place_locked_item(
                world.create_item(items[ItemIDs.city_moss])
            )
            world.get_location(locations[LocationIDs.ch2_cyber_city_annoying_dog]).place_locked_item(
                world.create_item(items[ItemIDs.dogdollar])
            )

        if not include_secret_bosses_items_requirement(world):
            world.get_location(locations[LocationIDs.ch2_spamton_shop_1]).place_locked_item(
                world.create_item(items[ItemIDs.keygen])
            )
            world.get_location(locations[LocationIDs.ch2_mansion_basement_mechanism]).place_locked_item(
                world.create_item(items[ItemIDs.emptydisk])
            )

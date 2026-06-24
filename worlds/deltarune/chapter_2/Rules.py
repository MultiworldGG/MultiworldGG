from BaseClasses import LocationProgressType
from rule_builder.rules import Has

from typing import TYPE_CHECKING
from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import ItemIDs, items, glitched_item_name
from worlds.deltarune.Rules import (
    have_kris_susie_or_ralsei,
    have_noelle,
    can_snowgrave,
    have_kris_or_susie,
    can_lost_chapter2_with_noelle,
    can_recruit,
    can_recruit_with_kris_susie,
    have_kris_or_noelle,
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

    # Weird Route
    if world.is_weird_route():
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_werewire]), have_kris_or_susie)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_tasque]), have_kris_susie_or_ralsei)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_virovirokun]), have_kris_susie_or_ralsei)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_poppup]), can_lost_chapter2_with_noelle)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_ambyu_lance]), can_lost_chapter2_with_noelle)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_lost_maus]), can_lost_chapter2_with_noelle)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_cyber_city_purchase_freezering]),
            have_noelle)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_cyber_city_purchase_thornring]),
            have_noelle | Has(glitched_item_name),
        )
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_lost_tasque_manager]),
            have_kris_susie_or_ralsei & (can_snowgrave | Has(glitched_item_name)),
        )
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_lost_mauswheel]),
            have_kris_susie_or_ralsei & (can_snowgrave | Has(glitched_item_name)),
        )
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_lost_werewerewire]),
            have_kris_susie_or_ralsei & (can_snowgrave | Has(glitched_item_name)),
        )
        if world.options.include_lose_swatchling.value == 1:
            world.set_rule(
                world.get_location(locations[LocationIDs.ch2_lost_swatchlings]),
                have_kris_susie_or_ralsei & (can_snowgrave | Has(glitched_item_name)),
            )

    if world.is_all_recruits():
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_werewire]), can_recruit_with_kris_susie)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_tasque]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_virovirokun]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_poppup]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_ambyu_lance]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_maus]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_tasque_manager]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_mauswheel]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_werewerewire]), can_recruit)
        world.set_rule(world.get_location(locations[LocationIDs.ch2_recruit_swatchling]), can_recruit)
        world.set_rule(
            world.get_location(locations[LocationIDs.ch2_recruit_ambyu_lance]), can_lost_chapter2_with_noelle
        )

        if world.options.exclude_post_chapter_2_locations.value == 1:
            world.get_location(locations[LocationIDs.ch2_castle_town_tasque_manager_says_challenge]).progress_type = (
                LocationProgressType.EXCLUDED
            )
            world.get_location(locations[LocationIDs.ch2_castle_town_all_stars_challenge]).progress_type = (
                LocationProgressType.EXCLUDED
            )


def handle_locked_items(world: "DeltaruneWorld"):
    if not world.is_fun_gang_actions_unlockable():
        world.get_location(locations[LocationIDs.ch2_cyber_field_fun_gang_actions_unlock]).place_locked_item(
            world.create_item(items[ItemIDs.s_r_n_actions])
        )

    if not world.is_secret_bosses_randomized():
        world.get_location(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_1]).place_locked_item(
            world.create_item(items[ItemIDs.puppetscarf])
        )
        world.get_location(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_2]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )
        if world.is_not_weird_route_only():
            world.get_location(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_3]).place_locked_item(
                world.create_item(items[ItemIDs.dealmaker])
            )

    # Hidden items
    if world.is_not_weird_route_only():
        if not world.is_hidden_items_randomized():
            world.get_location(locations[LocationIDs.ch2_cyber_city_man]).place_locked_item(
                world.create_item(items[ItemIDs.chapter_2_egg])
            )
            world.get_location(locations[LocationIDs.ch2_cyber_city_moss]).place_locked_item(
                world.create_item(items[ItemIDs.city_moss])
            )
            world.get_location(locations[LocationIDs.ch2_cyber_city_annoying_dog]).place_locked_item(
                world.create_item(items[ItemIDs.dogdollar])
            )

        if not world.is_secret_bosses_items_requirement_randomized():
            world.get_location(locations[LocationIDs.ch2_spamton_shop_1]).place_locked_item(
                world.create_item(items[ItemIDs.keygen])
            )
            world.get_location(locations[LocationIDs.ch2_mansion_basement_mechanism]).place_locked_item(
                world.create_item(items[ItemIDs.emptydisk])
            )

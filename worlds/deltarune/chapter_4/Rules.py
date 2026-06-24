from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import Has

from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Rules import have_susie, have_kris_susie_or_ralsei, have_kris

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):
    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_1]), have_susie
    )
    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_2]), have_susie
    )

    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_castle_town_lanino_elnina_challenge]), have_kris_susie_or_ralsei
    )

    world.set_rule(
        world.get_location(locations[LocationIDs.ch4_third_sanctuary_annoying_dog]), Has(items[ItemIDs.sheetmusic])
    )

    world.set_rule(world.get_location(locations[LocationIDs.ch4_dark_sanctuary_jackenstein_gift]), have_kris)
    world.set_rule(world.get_location(locations[LocationIDs.ch4_dark_sanctuary_climbing_tutorial_chest]), have_kris)

    if world.is_mike_games_included() and world.options.exclude_mike_platinum.value == 1:
        world.get_location(locations[LocationIDs.ch4_mike_pluey_platinum]).progress_type = LocationProgressType.EXCLUDED
        world.get_location(locations[LocationIDs.ch4_mike_battat_platinum]).progress_type = (
            LocationProgressType.EXCLUDED
        )
        world.get_location(locations[LocationIDs.ch4_mike_jongler_platinum]).progress_type = (
            LocationProgressType.EXCLUDED
        )

    if world.is_all_recruits():
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_organikk]), have_kris_susie_or_ralsei)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_wicabel]), have_kris_susie_or_ralsei)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_recruit_winglade]), have_kris_susie_or_ralsei)
    if world.is_weird_route():
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_organikk]), have_kris_susie_or_ralsei)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_wicabel]), have_kris_susie_or_ralsei)
        world.set_rule(world.get_location(locations[LocationIDs.ch4_lost_winglade]), have_kris_susie_or_ralsei)


def handle_locked_items(world: "DeltaruneWorld"):
    player = world.player
    multiworld = world.multiworld

    if not world.is_secret_bosses_randomized():
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_1]).place_locked_item(
            world.create_item(items[ItemIDs.justiceaxe])
        )
        world.get_location(locations[LocationIDs.ch4_dark_sanctuary_hammer_of_justice_defeat_item_2]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )

    # Hidden Items
    if not world.is_hidden_items_randomized():
        world.get_location(locations[LocationIDs.ch4_second_sanctuary_man]).place_locked_item(
            world.create_item(items[ItemIDs.chapter_4_egg])
        )
        world.get_location(locations[LocationIDs.ch4_second_sanctuary_moss]).place_locked_item(
            world.create_item(items[ItemIDs.sacred_moss])
        )

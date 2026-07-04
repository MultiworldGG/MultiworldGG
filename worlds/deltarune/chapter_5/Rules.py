from typing import TYPE_CHECKING

from BaseClasses import LocationProgressType
from rule_builder.rules import Has

from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Rules import have_susie, have_kris_susie_or_ralsei, have_kris

if TYPE_CHECKING:
    from .. import DeltaruneWorld


def set_rules(world: "DeltaruneWorld"):

    world.set_rule(locations[LocationIDs.ch5_mew_mew_shop_4], Has(items[ItemIDs.pinkcoin], 10))
    # Region lockers

    # Macguffin


def handle_locked_items(world: "DeltaruneWorld"):
    if not world.is_secret_bosses_randomized():
        world.get_location(locations[LocationIDs.ch5_top_castle_mad_mew_mew]).place_locked_item(
            world.create_item(items[ItemIDs.shadowcrystal])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_aqua_item]).place_locked_item(
            world.create_item(items[ItemIDs.aquaknife])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_blue_item]).place_locked_item(
            world.create_item(items[ItemIDs.blueshoes])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_green_item]).place_locked_item(
            world.create_item(items[ItemIDs.greenapron])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_yellow_item]).place_locked_item(
            world.create_item(items[ItemIDs.yellowhat])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_orange_item]).place_locked_item(
            world.create_item(items[ItemIDs.ogloves])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_seth_item]).place_locked_item(
            world.create_item(items[ItemIDs.sethspecs])
        )
        world.get_location(locations[LocationIDs.ch5_flower_reward_flowery_item]).place_locked_item(
            world.create_item(items[ItemIDs.floweryscarf])
        )

    if not world.is_secret_bosses_items_requirement_randomized():
        world.get_location(locations[LocationIDs.ch5_mew_mew_shop_4]).place_locked_item(
            world.create_item(items[ItemIDs.pinkkey])
        )
        for i in range(19):
            world.get_location(locations[LocationIDs.ch5_pink_dollar_1 + i]).place_locked_item(
                world.create_item(items[ItemIDs.pinkcoin])
            )

    # Hidden Items
    if not world.is_hidden_items_randomized():
        return

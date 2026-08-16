from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachEntrance, CanReachLocation, CanReachRegion, Has, True_
from worlds.deltarune.LogicHelper import all_recruits_route, normal_route, weird_route
from worlds.deltarune.Options import (
    ChosenRoute,
    MacGuffinChapter5,
    RandomizeChapters,
    RandomizeSecretBosses,
)
from worlds.deltarune.Regions import Regions, add_location_to_region, get_entrance_name
from worlds.deltarune.chapter_5.Locations import chapter5_locations, chapter5_weird_route_locations
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import locations, LocationIDs
from worlds.deltarune.Rules import (
    have_kris_susie_or_ralsei,
    have_kris_susie_and_ralsei,
    have_kris,
)

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    if weird_route(world):
        weird_route_region = Region(Regions.ch5_weird_route, world.player, world.multiworld)

        add_location_to_region(weird_route_region, chapter5_weird_route_locations[weird_route_region.name], world)
        world.multiworld.regions.append(weird_route_region)

        world.get_region(Regions.chapter_5).connect(
            weird_route_region,
            rule=(
                Has(items[ItemIDs.chapter_5_unlock])
                | OptionFilter(RandomizeChapters, RandomizeChapters.option_all_unlocked)
            ),
        )

    if normal_route(world):
        castle_town = Region(Regions.ch5_castle_town, world.player, world.multiworld)
        dojo = Region(Regions.ch5_dojo, world.player, world.multiworld)
        garden_no_character_required = Region(Regions.ch5_garden_no_character_required, world.player, world.multiworld)
        garden = Region(Regions.ch5_garden, world.player, world.multiworld)
        greens_cafe = Region(Regions.ch5_greens_cafe, world.player, world.multiworld)
        dark_garden = Region(Regions.ch5_dark_garden, world.player, world.multiworld)
        garden_aqua = Region(Regions.ch5_garden_aqua, world.player, world.multiworld)
        garden_petal_feather = Region(Regions.ch5_garden_petal_feather, world.player, world.multiworld)
        dark_garden_petal_feather = Region(Regions.ch5_dark_garden_petal_feather, world.player, world.multiworld)
        cliffs = Region(Regions.ch5_cliffs, world.player, world.multiworld)
        pinks_shop = Region(Regions.ch5_pinks_shop, world.player, world.multiworld)
        flower_castle = Region(Regions.ch5_flower_castle, world.player, world.multiworld)
        vending_machine = Region(Regions.ch5_vending_machine, world.player, world.multiworld)
        castle_west = Region(Regions.ch5_castle_west, world.player, world.multiworld)
        castle_east = Region(Regions.ch5_castle_east, world.player, world.multiworld)
        castle_top = Region(Regions.ch5_castle_top, world.player, world.multiworld)
        pink_room = Region(Regions.ch5_pink_room, world.player, world.multiworld)
        flower_rewards = Region(Regions.ch5_flower_rewards, world.player, world.multiworld)
        fountains = Region(Regions.ch5_fountains, world.player, world.multiworld)

        regions = [
            castle_town,
            dojo,
            garden_no_character_required,
            garden,
            greens_cafe,
            dark_garden,
            garden_aqua,
            garden_petal_feather,
            dark_garden_petal_feather,
            cliffs,
            pinks_shop,
            flower_castle,
            vending_machine,
            castle_west,
            castle_east,
            castle_top,
            pink_room,
            flower_rewards,
            fountains,
        ]

        for region in regions:
            if region.name in chapter5_locations:
                add_location_to_region(region, chapter5_locations[region.name], world)
            world.multiworld.regions.append(region)

        world.get_region(Regions.chapter_5).connect(castle_town)

        castle_town.connect(dojo)

        castle_town.connect(garden_no_character_required)

        garden_no_character_required.connect(garden, rule=have_kris_susie_or_ralsei)

        garden.connect(greens_cafe)

        garden.connect(dark_garden)

        garden_no_character_required.connect(garden_petal_feather, rule=Has(items[ItemIDs.petalfeather]))

        # aqua fight needs kris
        dark_garden.connect(garden_aqua, rule=have_kris)

        garden_aqua.connect(dark_garden_petal_feather, rule=Has(items[ItemIDs.petalfeather]))

        dark_garden_petal_feather.connect(cliffs)

        cliffs.connect(pinks_shop)

        cliffs.connect(flower_castle)

        flower_castle.connect(vending_machine)

        flower_castle.connect(castle_east, rule=Has(items[ItemIDs.compliment_list_green]))

        flower_castle.connect(castle_west, rule=Has(items[ItemIDs.compliment_list_yellow]))

        # need everyone for green & orange fight and blue & yellow fight
        flower_castle.connect(
            castle_top,
            rule=have_kris_susie_and_ralsei
            & Has(items[ItemIDs.compliment_list_green])
            & Has(items[ItemIDs.compliment_list_yellow]),
        )

        castle_top.connect(pink_room, rule=Has(items[ItemIDs.pinkkey]))

        pink_room.connect(
            flower_rewards,
            rule=Has(items[ItemIDs.pinkcoin], 16) | Has(items[ItemIDs.pinkcoin], 11) & Has(glitched_item_name),
        )

        secret_boss_mandatory = CanReachLocation(locations[LocationIDs.ch5_castle_top_pink_defeat]) | [
            OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory, operator="ne")
        ]

        if all_recruits_route(world):
            all_recruits = (
                CanReachLocation(locations[LocationIDs.ch5_recruit_floradinn])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_sheary])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_netskie])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_shi])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_leafling])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_kawkaw])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_shinobeetle])
                & CanReachLocation(locations[LocationIDs.ch5_recruit_terakota])
            )

            castle_top.connect(
                fountains,
                rule=secret_boss_mandatory
                & all_recruits
                & Has(items[ItemIDs.jarona_lesson], FromOption(MacGuffinChapter5)),
            )
        else:
            castle_top.connect(
                fountains,
                rule=secret_boss_mandatory & Has(items[ItemIDs.jarona_lesson], FromOption(MacGuffinChapter5)),
            )

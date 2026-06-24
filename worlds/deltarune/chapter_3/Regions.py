from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachLocation, Has
from worlds.deltarune.Options import (
    IncludeShadowMantle,
    MacGuffinChapter3,
    RandomizeMANTLE,
    RandomizeSecretBosses,
)
from worlds.deltarune.Regions import Regions, add_location_to_region, get_entrance_name
from worlds.deltarune.chapter_3.Locations import chapter3_locations
from worlds.deltarune.Rules import (
    have_actions,
    have_kris_susie_and_ralsei,
    have_kris_susie_or_ralsei,
    have_kris,
    have_susie_or_ralsei,
)
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import LocationIDs, locations

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    couch_cliffs = Region(Regions.ch3_couch_cliffs, world.player, world.multiworld)
    board_1 = Region(Regions.ch3_board_1, world.player, world.multiworld)
    sword_1 = Region(Regions.ch3_sword_1, world.player, world.multiworld)
    green_room = Region(Regions.ch3_green_room, world.player, world.multiworld)
    board_2 = Region(Regions.ch3_board_2, world.player, world.multiworld)
    sword_2 = Region(Regions.ch3_sword_2, world.player, world.multiworld)
    doom_board = Region(Regions.ch3_doom_board, world.player, world.multiworld)
    tv_world = Region(Regions.ch3_tv_world, world.player, world.multiworld)
    sword_3 = Region(Regions.ch3_sword_3, world.player, world.multiworld)
    cold_place = Region(Regions.ch3_cold_place, world.player, world.multiworld)

    regions = [
        couch_cliffs,
        board_1,
        sword_1,
        green_room,
        board_2,
        sword_2,
        doom_board,
        tv_world,
        sword_3,
        cold_place,
    ]

    for region in regions:
        if region.name in chapter3_locations:
            add_location_to_region(region, chapter3_locations[region.name], world)
        world.multiworld.regions.append(region)

    world.get_region(Regions.chapter_3).connect(couch_cliffs)

    # Require at least one character for Elnina Lanino and shadowguy fights
    couch_cliffs.connect(board_1, rule=have_kris | (have_susie_or_ralsei & have_actions))

    board_1.connect(green_room)
    board_1.connect(sword_1, rule=Has(items[ItemIDs.odd_controller]))

    green_room.connect(board_2, rule=Has(items[ItemIDs.board_2_cartridge]))

    # Require all characters for Turning off Zapper during Doom Board
    board_2.connect(doom_board, rule=have_kris_susie_and_ralsei)
    board_2.connect(sword_2, rule=Has(items[ItemIDs.ice_key]) & Has(items[ItemIDs.odd_controller]))

    doom_board.connect(tv_world, rule=Has(items[ItemIDs.vip_pass]))

    tv_world.connect(
        sword_3,
        rule=Has(items[ItemIDs.shelter_key]) & Has(items[ItemIDs.ice_key]) & Has(items[ItemIDs.odd_controller]),
    )
    tv_world.connect(world.get_region(Regions.lost_rabbick))

    mantle_mandatory = CanReachLocation(
        locations[LocationIDs.ch3_mantle_defeat],
        options=[
            OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory),
            OptionFilter(RandomizeMANTLE, RandomizeMANTLE.option_mantleless, operator="ne"),
        ],
        filtered_resolution=True,
    )

    shadow_mantle = (
        Has(items[ItemIDs.shadowmantle])
        | OptionFilter(IncludeShadowMantle, IncludeShadowMantle.option_false)
        | OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory, operator="ne")
        | Has(glitched_item_name)
    )

    tv_world.connect(
        cold_place,
        rule=mantle_mandatory & shadow_mantle & Has(items[ItemIDs.remote_battery], FromOption(MacGuffinChapter3)),
    )

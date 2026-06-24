from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachLocation, CanReachRegion, Has
from worlds.deltarune.Options import ChosenRoute, MacGuffinChapter2, RandomizeSecretBosses
from worlds.deltarune.Regions import Regions, add_location_to_region, get_entrance_name
from worlds.deltarune.chapter_2.Locations import chapter2_locations
from worlds.deltarune.Rules import (
    have_actions,
    have_kris_or_susie,
    have_kris,
    can_snowgrave,
    have_kris_or_noelle,
    have_kris_or_ralsei,
    have_kris_susie_or_ralsei,
    can_recruit_with_kris_susie,
    have_susie,
)
from worlds.deltarune.Items import items, ItemIDs, glitched_item_name
from worlds.deltarune.Locations import LocationIDs, locations

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    castle_town = Region(Regions.ch2_castle_town, world.player, world.multiworld)
    dojo = Region(Regions.ch2_dojo, world.player, world.multiworld)
    cyber_field = Region(Regions.ch2_cyber_field, world.player, world.multiworld)
    cyber_field_post_dj = Region(Regions.ch2_cyber_field_post_dj, world.player, world.multiworld)
    music_shop = Region(Regions.ch2_music_shop, world.player, world.multiworld)
    trash_zone = Region(Regions.ch2_trash_zone, world.player, world.multiworld)
    spamton_shop = Region(Regions.ch2_spamton_shop, world.player, world.multiworld)
    cyber_city = Region(Regions.ch2_cyber_city, world.player, world.multiworld)
    cyber_city_spamton_fight = Region(Regions.ch2_cyber_city_spamton_fight, world.player, world.multiworld)
    cyber_city_post_spamton = Region(Regions.ch2_cyber_city_post_spamton, world.player, world.multiworld)
    mansion_lobby = Region(Regions.ch2_mansion_lobby, world.player, world.multiworld)
    swatch_cafe = Region(Regions.ch2_swatch_cafe, world.player, world.multiworld)
    mansion = Region(Regions.ch2_mansion, world.player, world.multiworld)
    tunnel_of_love = Region(Regions.ch2_tunnel_of_love, world.player, world.multiworld)
    mansion_recruits = Region(Regions.ch2_mansion_recruits, world.player, world.multiworld)
    werewerewire = Region(Regions.ch2_werewerewire, world.player, world.multiworld)
    mansion_basement = Region(Regions.ch2_mansion_basement, world.player, world.multiworld)
    spamton_neo = Region(Regions.ch2_spamton_neo, world.player, world.multiworld)
    post_chapter_castle_town = Region(Regions.ch2_post_chapter_castle_town, world.player, world.multiworld)

    regions = [
        castle_town,
        dojo,
        cyber_field,
        cyber_field_post_dj,
        music_shop,
        trash_zone,
        spamton_shop,
        cyber_city,
        cyber_city_spamton_fight,
        cyber_city_post_spamton,
        mansion_lobby,
        swatch_cafe,
        mansion,
        tunnel_of_love,
        mansion_recruits,
        werewerewire,
        mansion_basement,
        spamton_neo,
        post_chapter_castle_town,
    ]

    for region in regions:
        if region.name in chapter2_locations:
            add_location_to_region(region, chapter2_locations[region.name], world)
        world.multiworld.regions.append(region)

    world.get_region(Regions.chapter_2).connect(castle_town)

    access_to_cyber_field = (
        (
            can_recruit_with_kris_susie
            & OptionFilter(ChosenRoute, [ChosenRoute.option_all_recruits, ChosenRoute.option_all_routes], operator="in")
        )
        | (have_kris_or_susie & Has(glitched_item_name))
    ) | (
        have_kris_or_susie
        & OptionFilter(ChosenRoute, [ChosenRoute.option_weird_route, ChosenRoute.option_neutral_route], operator="in")
    )

    # Require Kris or Susie for the werewire fight
    world.get_region(Regions.chapter_2).connect(
        cyber_field,
        rule=access_to_cyber_field,
    )

    castle_town.connect(dojo)
    # Require Kris or Susie for the werewire fight
    castle_town.connect(
        cyber_field,
        rule=access_to_cyber_field,
    )

    # Require actions and at least one character for DJ-fight unless you ww into the fight (but can't end it) or Bagel Overflow to mansion and come back with plot value updated
    cyber_field.connect(
        cyber_field_post_dj,
        rule=(have_actions & have_kris_susie_or_ralsei),
    )
    cyber_field.connect(
        trash_zone, get_entrance_name(cyber_field_post_dj, trash_zone, "BagelOverflow"), Has(glitched_item_name)
    )
    cyber_field.connect(
        mansion_lobby, get_entrance_name(cyber_field, mansion_lobby, "BagelOverflow"), Has(glitched_item_name)
    )
    cyber_field.connect(
        cyber_field_post_dj,
        get_entrance_name(cyber_field, cyber_field_post_dj, "BagelOverflow / WrongWarp"),
        Has(glitched_item_name),
    )
    cyber_field_post_dj.connect(music_shop)
    # Require Safety vest and at least one character for berdly fight or Bagel Overflow to Trash Zone
    cyber_field_post_dj.connect(
        trash_zone,
        rule=(Has(items[ItemIDs.safety_vest]) & have_kris_susie_or_ralsei),
    )

    # Require Kris or Noelle for the Virovirokun after noelle
    trash_zone.connect(cyber_city, rule=have_kris_or_noelle | (have_kris_susie_or_ralsei & Has(glitched_item_name)))

    # Require Kris for Spamton fight unless you skip it with an Interaction Slide
    cyber_city.connect(cyber_city_spamton_fight, rule=have_kris)
    cyber_city.connect(mansion_lobby, rule=can_snowgrave)
    cyber_city.connect(
        cyber_city_post_spamton,
        get_entrance_name(cyber_city, cyber_city_post_spamton, "Interaction Slide"),
        Has(glitched_item_name),
    )

    cyber_city_spamton_fight.connect(cyber_city_post_spamton)

    cyber_city_post_spamton.connect(mansion_lobby)

    mansion_lobby.connect(swatch_cafe)
    # Require you to being able to spare spamton
    mansion_lobby.connect(
        spamton_shop,
        rule=CanReachRegion(Regions.ch2_cyber_city_post_spamton),
    )
    mansion_lobby.connect(mansion, rule=Has(items[ItemIDs.mansion_reservation]))
    mansion_lobby.connect(mansion_recruits, rule=can_snowgrave)
    mansion_lobby.connect(werewerewire, rule=can_snowgrave)
    mansion_lobby.connect(
        spamton_neo,
        rule=Has(items[ItemIDs.keygen_2_segment], FromOption(MacGuffinChapter2)) & can_snowgrave & have_kris,
    )

    spamton_neo.connect(
        post_chapter_castle_town,
        rule=can_snowgrave,
    )

    mansion.connect(mansion_recruits)
    mansion.connect(mansion_basement, rule=Has(items[ItemIDs.keygen]) & (have_kris | Has(glitched_item_name)))
    mansion.connect(tunnel_of_love, rule=have_kris_or_ralsei)

    tunnel_of_love.connect(werewerewire)

    mansion_basement.connect(spamton_neo, rule=Has(items[ItemIDs.emptydisk]))

    secret_boss_mandatory = CanReachLocation(locations[LocationIDs.ch2_mansion_spamton_neo_defeat_item_1]) | [
        OptionFilter(RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory, operator="ne")
    ]

    tunnel_of_love.connect(
        post_chapter_castle_town,
        rule=secret_boss_mandatory & Has(items[ItemIDs.keygen_2_segment], FromOption(MacGuffinChapter2)),
    )

from typing import TYPE_CHECKING

from BaseClasses import Region
from rule_builder.field_resolvers import FromOption
from rule_builder.options import OptionFilter
from rule_builder.rules import CanReachLocation, Has
from worlds.deltarune.Items import ItemIDs, items, glitched_item_name
from worlds.deltarune.Options import MacGuffinChapter1, RandomizeSecretBosses
from worlds.deltarune.Regions import add_location_to_region, Regions, get_entrance_name
from worlds.deltarune.Rules import have_kris_or_ralsei, have_kris_susie_or_ralsei, have_kris
from worlds.deltarune.Locations import LocationIDs, locations
from worlds.deltarune.chapter_1.Locations import chapter1_locations

if TYPE_CHECKING:
    from worlds.deltarune import DeltaruneWorld


def create_regions(world: "DeltaruneWorld"):
    unknown = Region(Regions.ch1_unknown, world.player, world.multiworld)
    castle_town = Region(Regions.ch1_castle_town, world.player, world.multiworld)
    fields = Region(Regions.ch1_fields, world.player, world.multiworld)
    fields_post_hathy = Region(Regions.ch1_fields_post_hathy, world.player, world.multiworld)
    seam_seap = Region(Regions.ch1_seam_seap, world.player, world.multiworld)
    great_board = Region(Regions.ch1_great_board, world.player, world.multiworld)
    forest = Region(Regions.ch1_forest, world.player, world.multiworld)
    bake_sale = Region(Regions.ch1_bake_sale, world.player, world.multiworld)
    forest_post_bake_sale = Region(Regions.ch1_forest_post_bake_sale, world.player, world.multiworld)
    card_castle = Region(Regions.ch1_card_castle, world.player, world.multiworld)
    rouxls_shop = Region(Regions.ch1_rouxls, world.player, world.multiworld)
    jevil = Region(Regions.ch1_jevil, world.player, world.multiworld)
    light_world = Region(Regions.ch1_light_world, world.player, world.multiworld)

    regions = [
        unknown,
        castle_town,
        fields,
        fields_post_hathy,
        seam_seap,
        great_board,
        forest,
        bake_sale,
        forest_post_bake_sale,
        card_castle,
        rouxls_shop,
        jevil,
        light_world,
    ]

    for region in regions:
        if region.name in chapter1_locations:
            add_location_to_region(region, chapter1_locations[region.name], world)
        world.multiworld.regions.append(region)

    world.get_region(Regions.chapter_1).connect(unknown)

    unknown.connect(castle_town)

    castle_town.connect(fields)

    # Kris or Ralsei required for Triple Hathy fight
    fields.connect(fields_post_hathy, rule=have_kris_or_ralsei)

    fields_post_hathy.connect(seam_seap)
    # Any character is required for the Jigsawry fight
    fields_post_hathy.connect(great_board, rule=have_kris_susie_or_ralsei)

    # Kris required for K.Round fight
    great_board.connect(forest, rule=have_kris)

    # Bake Sale Ticket is required to enter and Kris or Ralsei is required for Clover fight unless you do ARMS glitch
    forest.connect(
        bake_sale,
        rule=Has(items[ItemIDs.bake_sale_ticket]) & (have_kris_or_ralsei | Has(glitched_item_name)),
    )
    forest.connect(world.get_region(Regions.lost_rabbick))

    bake_sale.connect(forest_post_bake_sale)

    # Castle key is required with Kris or Ralsei to Vs. Susie and lancer fight
    forest_post_bake_sale.connect(
        card_castle,
        rule=Has(items[ItemIDs.castle_key]) & have_kris_or_ralsei,
    )

    # Door key is required with Kris, Susie or Ralsei
    card_castle.connect(jevil, rule=Has(items[ItemIDs.door_key]) & have_kris_susie_or_ralsei)
    card_castle.connect(rouxls_shop)

    secret_boss_mandatory = CanReachLocation(locations[LocationIDs.ch1_card_castle_jevil_1]) | OptionFilter(
        RandomizeSecretBosses, RandomizeSecretBosses.option_mandatory, operator="ne"
    )

    card_castle.connect(
        light_world,
        rule=secret_boss_mandatory
        & Has(items[ItemIDs.king_shape_key_piece], FromOption(MacGuffinChapter1))
        & have_kris,
    )

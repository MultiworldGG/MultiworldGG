# not entirely, but partially from
# https://github.com/icebound777/PMR-SeedGenerator/blob/main/rando_modules/logic.py
# follows examples in OoT's implementation

from collections import namedtuple
from itertools import chain

from .data.chapter_logic import (
    get_bowser_castle_removed_locations,
    areas_by_chapter,
    get_locations_beyond_spirit_requirements,
)
from .data.ItemList import (
    taycet_items,
    item_table,
    progression_miscitems,
    item_groups,
    item_multiples_base_name,
)
from .data.LocationsList import (
    location_groups,
    location_table,
    missable_locations,
    dojo_location_order,
    all_ch8_locations,
)
from .options import *
from .data.item_exclusion import (
    exclude_due_to_settings,
    exclude_from_taycet_placement,
)
from .modules.modify_itempool import get_randomized_itempool
from BaseClasses import ItemClassification as Ic, LocationProgressType
from .Locations import location_factory
from .data.chapter_logic import (
    get_chapter_excluded_item_names,
    get_chapter_excluded_location_names
)

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import PaperMarioWorld


def generate_itempool(pm_world):
    world = pm_world.multiworld
    player = pm_world.player

    (pool, placed_items, placed_items_excluded) = get_pool_core(pm_world)

    pm_world.itempool = [pm_world.create_item(item) for item in pool]
    for (location_name, item) in placed_items.items():
        location = world.get_location(location_name, player)
        location.place_locked_item(pm_world.create_item(item, allow_arbitrary_name=True))

    for (location_name, item) in placed_items_excluded.items():
        location = location_factory(location_name, player)
        location.place_locked_item(pm_world.create_item(item, allow_arbitrary_name=True))
        pm_world.ch_excluded_locations.append(location)


def get_pool_core(world: "PaperMarioWorld"):

    pool_misc_progression_items = []
    pool_other_items = []
    pool_progression_items = []
    pool_coins_only = []
    pool_illogical_consumables = []
    pool_badges = []
    pool = []

    placed_items = {}

    bc_removed_locations = []

    # items and locations excluded from chapters for LCL get handled differently
    # from normal excluded locations
    ch_excluded_locations = []
    ch_excluded_items = []
    placed_items_excluded = {}

    if world.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic:
        ch_excluded_locations = get_chapter_excluded_location_names(
            world.excluded_spirits,
            world.options.letter_rewards.value,
        )
        ch_excluded_items = get_chapter_excluded_item_names(world.excluded_spirits)

    # remove chapter 8 locations if star way is the goal
    # otherwise remove any bowser castle locations removed by shortened or boss
    # rush modes
    if world.options.seed_goal.value == SeedGoal.option_Open_Star_Way:
        ch_excluded_locations.extend(all_ch8_locations)
        ch_excluded_items.extend(get_chapter_excluded_item_names([8]))
    else:
        bc_removed_locations = get_bowser_castle_removed_locations(
            world.options.bowser_castle_mode.value
        )

    # Exclude locations that are either missable or are going to be considered
    # not in logic based on settings
    excluded_locations = missable_locations + get_locations_to_exclude(
        world,
        bc_removed_locations,
    )

    # remove unused items from the pool

    for loc_name in location_table:

        if (    loc_name not in ch_excluded_locations
            and loc_name not in bc_removed_locations
        ):
            location = world.get_location(loc_name)
        else:
            location = location_factory(loc_name, world.player)

        if location.vanilla_item is None:
            continue

        item = location.vanilla_item
        itemdata = item_table[item]
        shuffle_item = True

        # Excluded locations
        if location.name in excluded_locations:
            location.progress_type = LocationProgressType.EXCLUDED

        # Sometimes placed items

        if location.name in location_groups["OverworldCoin"]:
            shuffle_item = world.options.overworld_coins.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["BlockCoin"]:
            shuffle_item = world.options.coin_blocks.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["FoliageCoin"]:
            shuffle_item = world.options.foliage_coins.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["ShopItem"]:

            if location.identifier in ["DRO_01/ShopItemB", "DRO_01/ShopItemD", "DRO_01/ShopItemE"]:
                shuffle_item = (
                        world.options.random_puzzles.value
                    and world.options.include_shops.value
                    and not (    world.options.spirit_requirements.value == SpiritRequirements.option_Specific_And_Limit_Chapter_Logic
                             and 2 in world.excluded_spirits
                        )
                )
            else:
                shuffle_item = world.options.include_shops.value

            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["HiddenPanel"]:
            shuffle_item = world.options.shuffle_hidden_panels.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["FavorReward"]:
            # coins get shuffled only if other rewards are also shuffled
            if location.name in location_groups["FavorCoin"]:
                shuffle_item = (
                        world.options.koot_coins.value
                    and (world.options.koot_favors.value != ShuffleKootFavors.option_Vanilla)
                )
            else:
                shuffle_item = (world.options.koot_favors.value != ShuffleKootFavors.option_Vanilla)

            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["FavorItem"]:
            shuffle_item = (world.options.koot_favors.value == ShuffleKootFavors.option_Full_Shuffle)
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["LetterReward"]:
            if location.name == "GR Goomba Village Goompapa Letter Reward 2":
                shuffle_item = (world.options.letter_rewards.value in [
                    ShuffleLetters.option_Final_Letter_Chain_Reward,
                    ShuffleLetters.option_Full_Shuffle
                ])
            elif location.name in location_groups["LetterChain"]:
                shuffle_item = (world.options.letter_rewards.value == ShuffleLetters.option_Full_Shuffle)

            else:
                shuffle_item = (world.options.letter_rewards.value != ShuffleLetters.option_Vanilla)

            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["RadioTradeEvent"]:
            shuffle_item = world.options.trading_events.value
            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in location_groups["DojoReward"]:

            reward_num = dojo_location_order.index(location.name)
            shuffle_item = (reward_num < world.options.dojo.value)
            if not shuffle_item:
                location.disabled = True

        if location.vanilla_item == "Forest Pass":
            shuffle_item = (not world.options.open_forest.value)
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["Partner"]:
            shuffle_item = (world.options.partners.value != ShufflePartners.option_Off)
            if not shuffle_item:
                location.disabled = True

        if location.name in location_groups["MultiCoinBlock"]:
            shuffle_item = (world.options.super_multi_blocks.value > ShuffleSuperMultiBlocks.option_Off)

        if location.name in location_groups["SuperBlock"]:
            shuffle_item = world.options.partner_upgrades.value > PartnerUpgradeShuffle.option_Vanilla

        if location.name in location_groups["Gear"]:
            # hammer 1 bush is special in that it is made to not be empty even if starting with hammer
            if location.name == "GR Jr. Troopa's Playground In Hammer Bush":
                shuffle_item = (
                       world.options.gear_shuffle_mode.value != GearShuffleMode.option_Vanilla
                    or world.options.starting_hammer.value == StartingHammer.option_Hammerless
                )
            else:
                shuffle_item = (world.options.gear_shuffle_mode.value != GearShuffleMode.option_Vanilla)
            if not shuffle_item:
                location.disabled = True

        if location.name == "SSS Star Sanctuary Gift of the Stars":
            shuffle_item = world.options.shuffle_star_beam.value

            if not shuffle_item:
                location.disabled = True
                location.show_in_spoiler = False

        if location.name in ch_excluded_locations and item in ch_excluded_items:
            shuffle_item = False

        # add it to the proper pool, or place the item
        if shuffle_item:

            # hammer bush gets shuffled as a Tayce T item if shuffling
            # gear locations and not hammerless
            if (    location.name == "GR Jr. Troopa's Playground In Hammer Bush"
                and world.options.gear_shuffle_mode.value == GearShuffleMode.option_Gear_Location_Shuffle
                and world.options.starting_hammer.value != StartingHammer.option_Hammerless
            ):
                pool_progression_items.append(world.random.choice([
                    x
                    for x in taycet_items
                    if x not in exclude_from_taycet_placement
                ]))
            # some progression items need to be in replenishable locations, we
            # only need one of each
            elif item in progression_miscitems:
                if item not in pool_misc_progression_items:
                    pool_misc_progression_items.append(item)
                else:
                    pool_illogical_consumables.append(item)
            # progression items are shuffled; include gear and star pieces from
            # rip cheato
            elif (    (   itemdata[1] == Ic.progression
                       or (    location.name in location_groups["ShopItem"]
                           and world.options.include_shops.value
                           and "Star Piece" in item))
                  and item not in ch_excluded_items
            ):
                pool_progression_items.append(item)
            # split other items into their own pools; these other pools get
            # modified before being sent elsewhere
            elif itemdata[0] == "COIN":
                pool_coins_only.append(item)
            elif itemdata[0] == "ITEM":
                pool_illogical_consumables.append(item)
            elif itemdata[0] == "BADGE":
                pool_badges.append(item)
            else:
                pool_other_items.append(item)
        elif (   loc_name in ch_excluded_locations
              or loc_name in bc_removed_locations
        ):
            # keep out of logic placed items separate, remove the location and
            # item from remaining excluded lists
            placed_items_excluded[location.name] = item

            # remove locations with placed items from the respective lists so we
            # can get the item pool count correct
            if location.name in bc_removed_locations:
                bc_removed_locations.remove(location.name)

            if location.name in ch_excluded_locations:
                ch_excluded_locations.remove(location.name)

                # below only applies to key items in the chapter
                if item in ch_excluded_items:
                    ch_excluded_items.remove(item)

        else:
            placed_items[location.name] = item

    # end of location for loop

    # at this point every location's item should be either left unshuffled or
    # added to a pool
    # we want to modify these pools according to settings and make sure to have
    # the right number of items

    target_itempool_size = (
        len(pool_progression_items)
        + len(pool_misc_progression_items)
        + len(pool_coins_only)
        + len(pool_illogical_consumables)
        + len(pool_badges)
        + len(pool_other_items)
        - len(bc_removed_locations)
    )

    # add power stars
    if (    world.options.power_star_hunt.value
        and world.options.total_power_stars.value > 0
    ):
        for i in range(0, world.options.total_power_stars.value):
            pool_progression_items.append("Power Star")

    # add 5 item pouches
    if world.options.item_pouches.value:
        for i in range(0, 5):
            pool_other_items.append("Pouch Upgrade")

    # add beta items
    if world.options.beta_items.value:
        pool_other_items.extend(item_groups["ItemBeta"])
        for badge in item_groups["BadgeBeta"]:
            pool_badges.append(get_item_multiples_base_name(badge))

    # add unused badge dupes
    if world.options.unused_badge_dupes.value:
        for badge in item_groups["BadgeDupe"]:
            if not (world.options.beta_items.value and badge in item_groups["BadgeBeta"]):
                pool_badges.append(get_item_multiples_base_name(badge))

    # add progressive badges
    if world.options.progressive_badges.value:
        # 3 copies of each progressive badge
        for name in item_groups["ProgBadge"]:
            for i in range(0, 3):
                pool_badges.append(name)

    # add normal boots
    if world.options.starting_boots.value == StartingBoots.option_Jumpless:
        pool_progression_items.append("Progressive Boots")

    # add two of each partner upgrade item, remove the generic ones
    if world.options.partner_upgrades.value != PartnerUpgradeShuffle.option_Vanilla:
        for i in range(0, 2):
            for upgrade in item_groups["PartnerUpgrade"]:
                if upgrade == "Partner Upgrade":
                    for _ in range(0, 8):
                        pool_other_items.remove(upgrade)
                else:
                    pool_other_items.append(upgrade)

    # add traps
    max_traps = 0
    match world.options.item_traps.value:
        case ItemTraps.option_Sparse:
            max_traps = 15
        case ItemTraps.option_Moderate:
            max_traps = 35
        case ItemTraps.option_Plenty:
            max_traps = 80
        case _:
            max_traps = 0

    pool_other_items.extend(["Damage Trap"] * max_traps)

    # adjust item pools based on settings
    items_to_remove_from_pools = get_items_to_exclude(world)

    while items_to_remove_from_pools:
        item = items_to_remove_from_pools.pop()
        if item in pool_progression_items:
            pool_progression_items.remove(item)
            continue
        if item in pool_misc_progression_items:
            pool_misc_progression_items.remove(item)
            continue
        if item in pool_badges:
            pool_badges.remove(item)
            continue
        if item in pool_other_items:
            pool_other_items.remove(item)
            continue

    # If we have set a badge pool limit and exceed that, remove random badges
    # until that condition is satisfied
    if len(pool_badges) > world.options.badge_pool_limit.value:
        world.random.shuffle(pool_badges)
        while len(pool_badges) > world.options.badge_pool_limit.value:
            pool_badges.pop()

    # If the item pool is the wrong size now, fix it by filling up or clearing
    # out items
    cur_itempool_size = (
        len(pool_progression_items)
        + len(pool_misc_progression_items)
        + len(pool_coins_only)
        + len(pool_illogical_consumables)
        + len(pool_badges)
        + len(pool_other_items)
    )

    # add random tayce t items if we need to add items for some reason
    while target_itempool_size > cur_itempool_size:
        pool_illogical_consumables.append(world.random.choice([
            x
            for x in taycet_items
            if x not in exclude_from_taycet_placement
        ]))
        cur_itempool_size += 1

    # remove coins first, then consumables if we need to keep going
    if target_itempool_size < cur_itempool_size:
        world.random.shuffle(pool_illogical_consumables)
        while target_itempool_size < cur_itempool_size:
            if len(pool_coins_only) > 20 or len(pool_illogical_consumables) == 0:
                trashable_items = pool_coins_only
            else:
                trashable_items = pool_illogical_consumables
            if trashable_items:
                trashable_items.pop()
                cur_itempool_size -= 1
            else:
                raise ValueError(
                    f"Paper Mario: {world.player} ({world.multiworld.player_name[world.player]}) has "
                    "too large of an item pool for the number of locations; consider increasing the "
                    "number of checks available or reducing the badge or power star pools."
                )

    # Re-join the non-required items into one array
    pool_other_items.extend(pool_coins_only)
    pool_other_items.extend(pool_illogical_consumables)
    pool_other_items.extend(pool_badges)

    # Randomize consumables if needed
    pool_other_items = get_randomized_itempool(
        pool_other_items,
        world.options.consumable_item_pool.value,
        world.options.consumable_item_quality.value,
        world.options.beta_items.value,
        world.random
    )

    if ch_excluded_locations:
        world.random.shuffle(ch_excluded_locations)

        # shuffle items but sort to put useful items in front so that
        # filler items go to out of logic locations first
        world.random.shuffle(pool_other_items)
        pool_other_items.sort(key=lambda item: 1 if item_table[item][1] == Ic.filler else 0)

        # save some filler items for the excluded locations; not the
        # chapter ones, but from get_locations_to_exclude
        for _ in excluded_locations:
            pool.append(pool_other_items.pop())

        for loc in ch_excluded_locations:
            placed_items_excluded[loc] = pool_other_items.pop()

    # now we have the full pool

    pool.extend(pool_progression_items)
    pool.extend(pool_other_items)
    pool.extend(pool_misc_progression_items)

    return pool, placed_items, placed_items_excluded


def get_items_to_exclude(world: "PaperMarioWorld") -> list:
    """
    Returns a list of items that should not be placed or given to Mario at the
    start.
    """
    excluded_items = []

    if world.options.dojo.value:
        for item_name in exclude_due_to_settings.get("do_randomize_dojo"):
            excluded_items.append(item_name)

    if world.options.start_with_goombario.value:
        excluded_items.append("Goombario")
    if world.options.start_with_kooper.value:
        excluded_items.append("Kooper")
    if world.options.start_with_bombette.value:
        excluded_items.append("Bombette")
    if world.options.start_with_parakarry.value:
        excluded_items.append("Parakarry")
    if world.options.start_with_bow.value:
        excluded_items.append("Bow")
    if world.options.start_with_watt.value:
        excluded_items.append("Watt")
    if world.options.start_with_sushie.value:
        excluded_items.append("Sushie")
    if world.options.start_with_lakilester.value:
        excluded_items.append("Lakilester")

    if world.options.open_blue_house.value:
        for item_name in exclude_due_to_settings.get("startwith_bluehouse_open"):
            excluded_items.append(item_name)

    if world.options.open_forest.value:
        for item_name in exclude_due_to_settings.get("startwith_forest_open"):
            excluded_items.append(item_name)

    if world.options.magical_seeds.value < 4:
        for item_name in exclude_due_to_settings.get("magical_seeds_required").get(world.options.magical_seeds.value):
            excluded_items.append(item_name)

    if world.options.bowser_castle_mode.value > BowserCastleMode.option_Vanilla:
        for item_name in exclude_due_to_settings.get("shorten_bowsers_castle"):
            excluded_items.append(item_name)
    if world.options.bowser_castle_mode.value == BowserCastleMode.option_Boss_Rush:
        for item_name in exclude_due_to_settings.get("boss_rush"):
            excluded_items.append(item_name)
    if world.options.always_speedy_spin.value:
        for item_name in exclude_due_to_settings.get("always_speedyspin"):
            excluded_items.append(item_name)
    if world.options.always_ispy.value:
        for item_name in exclude_due_to_settings.get("always_ispy"):
            excluded_items.append(item_name)
    if world.options.always_peekaboo.value:
        for item_name in exclude_due_to_settings.get("always_peekaboo"):
            excluded_items.append(item_name)
    if world.options.progressive_badges.value:
        for item_name in exclude_due_to_settings.get("do_progressive_badges"):
            excluded_items.append(item_name)

    if world.options.starting_hammer.value == StartingHammer.option_Ultra:
        excluded_items.append("Progressive Hammer")
    if world.options.starting_hammer.value >= StartingHammer.option_Super:
        excluded_items.append("Progressive Hammer")
    if (world.options.starting_hammer.value >= StartingHammer.option_Normal and
            world.options.gear_shuffle_mode.value != GearShuffleMode.option_Gear_Location_Shuffle):
        excluded_items.append("Progressive Hammer")
    if world.options.starting_boots.value == StartingBoots.option_Ultra:
        excluded_items.append("Progressive Boots")
    if world.options.starting_boots.value >= StartingBoots.option_Super:
        excluded_items.append("Progressive Boots")

    if world.options.partner_upgrades.value:
        for item_name in exclude_due_to_settings.get("partner_upgrade_shuffle"):
            excluded_items.append(item_name)

    return excluded_items


def get_locations_to_exclude(
    world: "PaperMarioWorld",
    bc_removed_locations: list,
) -> list:
    excluded_locations = []

    # exclude locations which require more star spirits than are expected to be
    # needed to beat the seed
    if not world.options.power_star_hunt.value:
        excluded_locations.extend(
            get_locations_beyond_spirit_requirements(
                max([
                    world.options.star_way_spirits.value,
                    world.options.star_beam_spirits.value,
                ])
            )
        )

    # below lines turned off to see if letting late game locations not be
    # excluded is a problem or not
    # exclude some amount of chapter 8 locations depending upon access requirements
    # if world.options.seed_goal.value != SeedGoal.option_Open_Star_Way:
    #     late_game_locations = all_ch8_locations.copy()
    #     for bc_loc in bc_removed_locations:
    #         late_game_locations.remove(bc_loc)
    #
    #     if not world.options.shuffle_star_beam.value:
    #         late_game_locations.remove("SSS Star Sanctuary Gift of the Stars")
    #
    #     late_game_exclude_rate = get_star_haven_access_ratio(world.options) * 100
    #
    #     for location in late_game_locations:
    #         if world.random.randint(1, 100) <= late_game_exclude_rate:
    #             excluded_locations.append(location)

    # exclude merlow rewards
    if not world.options.merlow_items.value:
        excluded_locations.extend(location_groups["MerlowReward"])

    # exclude rowf item locations
    for location in location_groups["RowfShop"]:
        set_number: int = int(location[34])  # Example string: "TT Plaza District Rowf's Shop Set 1 - 1"
        if (    location not in excluded_locations
            and set_number > world.options.rowf_items.value
        ):
            excluded_locations.append(location)

    # exclude rip cheato locations
    for i in range(0, 11):
        location_name = location_groups["RipCheato"][i]
        if location_table[location_name][4] >= world.options.cheato_items.value:
            excluded_locations.append(location_groups["RipCheato"][i])

    # remove anything from the list that is already removed for LCL
    for loc in excluded_locations:
        if loc in world.ch_excluded_location_names:
            excluded_locations.remove(loc)

    return excluded_locations


def get_item_multiples_base_name(item_name: str) -> str:
    if item_name in item_multiples_base_name.keys():
        return item_multiples_base_name[item_name]
    return item_name


def get_star_haven_access_ratio(options: PaperMarioOptions):
    if options.seed_goal.value == SeedGoal.option_Open_Star_Way:
        return 1
    else:
        if options.power_star_hunt.value:
            return (
                (
                    (options.star_way_power_stars.value / options.total_power_stars.value)
                    + (options.star_way_spirits.value / 7)
                )
                / 2
            )
        else:
            return options.star_way_spirits.value / 7



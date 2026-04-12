from random import Random
from typing import List, Dict, Tuple

from . import FlipwitchOptions
from .data.locations import all_locations, gacha_locations, FlipwitchLocation, coin_locations, shop_locations, quest_locations, \
    sex_experience_locations, \
    stat_locations, warp_locations, base_locations, pot_locations
from .strings.items import Coin
from .strings.locations import WitchyWoods, GhostCastle, ClubDemon, AngelicHallway, SlimeCitadel, UmiUmi

location_table = all_locations
locations_by_name: Dict[str, FlipwitchLocation] = {location.name: location for location in location_table}


def create_locations(random: Random, options: FlipwitchOptions) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    locations = []
    locations_to_event = {}
    create_base_locations(options, locations, locations_to_event)
    create_shop_locations(options, locations, locations_to_event)
    create_gacha_locations(options, random, locations, locations_to_event)
    create_quest_locations(options, locations, locations_to_event)
    create_stat_locations(options, locations, locations_to_event)
    create_warp_locations(options, locations, locations_to_event)
    create_pot_locations(options, locations, locations_to_event)
    return locations, locations_to_event


def create_base_locations(options: FlipwitchOptions, locations: List[FlipwitchLocation],
                          locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    for location in base_locations:
        if location.name in [WitchyWoods.goblin_queen_chaos, GhostCastle.ghost_chaos, ClubDemon.demon_boss_chaos,
                             AngelicHallway.angelica_chaos, SlimeCitadel.slimy_princess_chaos, UmiUmi.frog_boss_chaos] and not options.shuffle_chaos_pieces:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
            continue
        locations.append(location)
    return locations, locations_to_event


def create_shop_locations(options: FlipwitchOptions, locations: List[FlipwitchLocation],
                          locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    if not options.shopsanity:
        for location in shop_locations:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
        return locations, locations_to_event
    for location in shop_locations:
        locations.append(location)
    return locations, locations_to_event


def create_gacha_locations(options: FlipwitchOptions, random: Random, locations: List[FlipwitchLocation],
                           locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    if options.gachapon_shuffle != options.gachapon_shuffle.option_all:
        for location in gacha_locations:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
    else:
        for location in gacha_locations:
            locations.append(location)
    if options.gachapon_shuffle == options.gachapon_shuffle.option_off:
        coins = [coin for coin in Coin.lucky_coins * 10 if coin != Coin.promotional_coin]
        coins.append(Coin.promotional_coin)
        chosen_coins = random.sample(Coin.lucky_coins, 3)
        coins.extend(chosen_coins)
        random.shuffle(coins)
        for location in coin_locations:
            chosen_coin = coins.pop()
            new_coin_location = FlipwitchLocation(location.location_id, location.name, location.region, chosen_coin)
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [new_coin_location]
            else:
                locations_to_event[location.region].append(new_coin_location)
    else:
        for location in coin_locations:
            locations.append(location)
    return locations, locations_to_event


def create_quest_locations(options: FlipwitchOptions, locations: List[FlipwitchLocation],
                           locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    quest_setting = options.quest_for_sex
    if quest_setting == options.quest_for_sex.option_off or quest_setting == options.quest_for_sex.option_sensei:
        for location in quest_locations:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
    else:
        for location in quest_locations:
            locations.append(location)
    if quest_setting == options.quest_for_sex.option_off:
        for location in sex_experience_locations:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
    else:
        for location in sex_experience_locations:
            locations.append(location)
    return locations, locations_to_event


def create_stat_locations(options: FlipwitchOptions, locations: List[FlipwitchLocation],
                           locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    if not options.stat_shuffle:
        for location in stat_locations:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
    else:
        for location in stat_locations:
            locations.append(location)
    return locations, locations_to_event


def create_warp_locations(options: FlipwitchOptions, locations: List[FlipwitchLocation],
                           locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    if not options.crystal_teleports:
        for location in warp_locations:
            if location.region not in locations_to_event:
                locations_to_event[location.region] = [location]
            else:
                locations_to_event[location.region].append(location)
    else:
        for location in warp_locations:
            locations.append(location)
    return locations, locations_to_event


def create_pot_locations(options: FlipwitchOptions, locations: List[FlipwitchLocation],
                           locations_to_event: Dict[str, List[FlipwitchLocation]]) -> Tuple[List[FlipwitchLocation], Dict[str, List[FlipwitchLocation]]]:
    if not options.pottery_lottery:
        return locations, locations_to_event
    for location in pot_locations:
        locations.append(location)
    return locations, locations_to_event


"""def construct_forced_local_items(lookup_table: Dict[str, List[Location]], player: int, options: FlipwitchOptions, random: Random):
    force_chaos_pieces(player, lookup_table, options)
    force_gacha_items(player, lookup_table, options, random)
    create_shop_locations(player, lookup_table, options)
    create_quest_locations(player, lookup_table, options)
    create_stat_locations(player, lookup_table, options)
    create_warp_locations(player, lookup_table, options)


def force_location_table(multiworld: MultiWorld, player: int):
    location_dictionary: Dict[str, List[Location]] = \
        {
            "Chaos Pieces": [],
            "Shop Locations": [],
            "Gacha Locations": [],
            "Coin Locations": [],
            "Quest Locations": [],
            "Sex Experience Locations": [],
            "Stat Locations": [],
            "Warp Locations": [],
        }
    for location in multiworld.get_locations(player):
        if location.name in [WitchyWoods.goblin_queen_chaos, GhostCastle.ghost_chaos, ClubDemon.demon_boss_chaos,
                             AngelicHallway.angelica_chaos, SlimeCitadel.slimy_princess_chaos, UmiUmi.frog_boss_chaos]:
            location_dictionary["Chaos Pieces"].append(location)
        elif location.name in [spot.name for spot in shop_locations]:
            location_dictionary["Shop Locations"].append(location)
        elif location.name in [spot.name for spot in gacha_locations]:
            location_dictionary["Gacha Locations"].append(location)
        elif location.name in [spot.name for spot in coin_locations]:
            location_dictionary["Coin Locations"].append(location)
        elif location.name in [spot.name for spot in quest_locations]:
            location_dictionary["Quest Locations"].append(location)
        elif location.name in [spot.name for spot in sex_experience_locations]:
            location_dictionary["Sex Experience Locations"].append(location)
        elif location.name in [spot.name for spot in stat_locations]:
            location_dictionary["Stat Locations"].append(location)
        elif location.name in [spot.name for spot in warp_locations]:
            location_dictionary["Warp Locations"].append(location)
    return location_dictionary


def get_forced_location_count(item_lookup: Dict[str, List[Location]], options: FlipwitchOptions):
    count = 0  # quests are always tracked, and have events associated with them.
    if options.shuffle_chaos_pieces == options.shuffle_chaos_pieces.option_false:
        count += len(item_lookup["Chaos Pieces"])
    if options.stat_shuffle == options.stat_shuffle.option_false:
        count += len(item_lookup["Stat Locations"])
    if options.gachapon_shuffle != options.gachapon_shuffle.option_all:
        count += len(item_lookup["Gacha Locations"])
        if options.gachapon_shuffle == options.gachapon_shuffle.option_off:
            count += len(item_lookup["Coin Locations"])
    if options.quest_for_sex != options.quest_for_sex.option_all and options.quest_for_sex != options.quest_for_sex.option_quests:
        count += len(item_lookup["Quest Locations"])
        if options.quest_for_sex == options.quest_for_sex.option_off:
            count += len(item_lookup["Sex Experience Locations"])
    if options.shopsanity == options.shopsanity.option_false:
        count += len(item_lookup["Shop Locations"])
    if not options.pottery_lottery:
        count += 147  # Sex event tracker
    if not options.crystal_teleports:
        count += len(item_lookup["Warp Locations"])
    return count


def force_chaos_pieces(player: int, lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.shuffle_chaos_pieces == options.shuffle_chaos_pieces.option_true:
        return
    for location in lookup_table["Chaos Pieces"]:
        created_item = Item(GoalItem.chaos_piece, item_name_to_item[GoalItem.chaos_piece].classification, None, player)
        location.place_locked_item(created_item)


def force_gacha_items(player: int, lookup_table: Dict[str, List[Location]], options: FlipwitchOptions, random: Random):
    if options.gachapon_shuffle == options.gachapon_shuffle.option_all:
        return
    for location in lookup_table["Gacha Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)
    if options.gachapon_shuffle == options.gachapon_shuffle.option_coin:
        return
    coins = [coin for coin in Coin.lucky_coins*10 if coin != Coin.promotional_coin]
    coins.append(Coin.promotional_coin)
    chosen_coins = random.sample(Coin.lucky_coins, 3)
    coins.extend(chosen_coins)
    random.shuffle(coins)
    coin_items = []
    for coin in coins:
        coin_items.append(Item(coin, ItemClassification.progression | ItemClassification.useful, None, player))
    for location in lookup_table["Coin Locations"]:
        static_item_name = coins.pop()
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)


def create_shop_locations(player: int, lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.shopsanity == options.shopsanity.option_true:
        return
    for location in lookup_table["Shop Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)


def create_quest_locations(player: int, lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.quest_for_sex == options.quest_for_sex.option_all or options.quest_for_sex == options.quest_for_sex.option_quests:
        return
    for location in lookup_table["Quest Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)
    if options.quest_for_sex == options.quest_for_sex.option_sensei:
        return
    count = 0
    for location in lookup_table["Sex Experience Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        if count < 8 and static_item_name == Upgrade.peachy_peach:
            created_item = Item(static_item_name, ItemClassification.progression | ItemClassification.useful, None, player)
            count += 1
        else:
            created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)


def create_stat_locations(player: int, lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.stat_shuffle == options.stat_shuffle.option_true:
        return
    count = 0
    for location in lookup_table["Stat Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        if count < 8 and static_item_name == Upgrade.health:
            created_item = Item(static_item_name, ItemClassification.progression | ItemClassification.useful, None, player)
            count += 1
        else:
            created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)

def create_warp_locations(player: int, lookup_table: Dict[str, List[Location]], options: FlipwitchOptions):
    if options.crystal_teleports:
        return
    for location in lookup_table["Warp Locations"]:
        static_item_name = locations_by_name[location.name].forced_off_item
        created_item = Item(static_item_name, item_name_to_item[static_item_name].classification, None, player)
        location.place_locked_item(created_item)"""
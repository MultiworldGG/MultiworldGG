from Options import OptionError
from ..Util import get_old_man_values_pool
from ..Options import *
from ...data import LOCATIONS_DATA, ITEMS_DATA
from ..data.Constants import DIRECTIONS, DIRECTION_LEFT, DIRECTION_UP, VALID_RUPEE_PRICE_VALUES, AVERAGE_PRICE_PER_LOCATION


def generate_early(world) -> None:
    if world.seasons and world.options.randomize_ai:
        world.options.golden_beasts_requirement.value = 0

    conflicting_rings = world.options.required_rings.value & world.options.excluded_rings.value
    if len(conflicting_rings) > 0:
        raise OptionError("Required Rings and Excluded Rings contain the same element(s)", conflicting_rings)

    world.remaining_progressive_gasha_seeds = world.options.deterministic_gasha_locations.value

    pick_essences_in_game(world)
    if world.seasons and len(world.essences_in_game) < world.options.treehouse_old_man_requirement:
        world.options.treehouse_old_man_requirement.value = len(world.essences_in_game)

    world.restrict_non_local_items()
    randomize_old_men(world)

    if world.options.linked_heros_cave.value:
        world.dungeon_entrances["d11 entrance"] = "enter d11"

    if world.seasons:
        randomize_default_seasons(world)
        from ...data.Constants import SEASONS
        
        def randomizeSequence(dir):
            # Pick 4 random seasons & directions (last one has to be the chosen direction)
            stuff = []
            for i in range(4):
                stuff.append([
                    world.random.choice(DIRECTIONS) if i < 3 else dir,
                    world.random.choice(SEASONS)
                ])
            return stuff

        if world.options.randomize_lost_woods_item_sequence:
            world.lost_woods_item_sequence = randomizeSequence(DIRECTION_LEFT)

        if world.options.randomize_lost_woods_main_sequence:
            world.lost_woods_main_sequence = randomizeSequence(DIRECTION_UP)

        if world.options.randomize_samasa_gate_code:
            world.samasa_gate_code = []
            for i in range(world.options.samasa_gate_code_length.value):
                world.samasa_gate_code.append(world.random.randint(0, 3))
    elif world.ages and world.options.shuffle_dungeons:
        # Ages uses an obsolete algorithm tht easily breaks when the new seasons apworld is dropped onto it.
        # Sadly, keeping the old algorithm is the only option to keep things going correctly.
        world.shuffle_dungeons()

    randomize_shop_order(world)
    randomize_shop_prices(world)
    compute_rupee_requirements(world)

    create_random_rings_pool(world)

    world.item_mapping_collect = {
        "Rupees (1)": ("Rupees", 1),
        "Rupees (5)": ("Rupees", 5),
        "Rupees (10)": ("Rupees", 10),
        "Rupees (20)": ("Rupees", 20),
        "Rupees (30)": ("Rupees", 30),
        "Rupees (50)": ("Rupees", 50),
        "Rupees (100)": ("Rupees", 100),
        "Rupees (200)": ("Rupees", 200),

        "Bombs (10)": ("Bombs", 10),
        "Bombs (20)": ("Bombs", 20),

        "Bombchus (10)": ("Bombchus", 10),
        "Bombchus (20)": ("Bombchus", 20),
    }
    if world.seasons:
        item_mapping_collect = {
             "_reached_d2_rupee_room": ("Rupees", 150),
            "_reached_d6_rupee_room": ("Rupees", 90),

            "Ore Chunks (10)": ("Ore Chunks", 10),
            "Ore Chunks (25)": ("Ore Chunks", 25),
            "Ore Chunks (50)": ("Ore Chunks", 50),
        }
        for type in item_mapping_collect:
            world.item_mapping_collect[type] = item_mapping_collect[type]
            
    for old_man in world.old_man_rupee_values:
        rupees = world.old_man_rupee_values[old_man]
        rupees = max(rupees, 0)  # We ignore negative value because they will most often do nothing
        # If this becomes an issue, state initialisation shall account for negative values
        world.item_mapping_collect[f"rupees from {old_man}"] = ("Rupees", rupees)


def pick_essences_in_game(world) -> None:
    # If the value for "Placed Essences" is lower than "Required Essences" (which can happen when using random
    # values for both), a new random value is automatically picked in the valid range.
    if world.options.required_essences > world.options.placed_essences:
        world.options.placed_essences.value = world.random.randint(world.options.required_essences.value, 8)

    # If some essence pedestal locations were excluded and essences are not shuffled,
    # remove those essences in priority
    if not world.options.shuffle_essences:
        excluded_locations_data = {name: data for name, data in LOCATIONS_DATA.items() if name in world.options.exclude_locations.value}
        for loc_name, loc_data in excluded_locations_data.items():
            if "essence" in loc_data and loc_data["essence"] is True:
                world.essences_in_game.remove(loc_data["vanilla_item"])
        if len(world.essences_in_game) < world.options.required_essences:
            raise ValueError("Too many essence pedestal locations were excluded, seed will be unbeatable")

    # If we need to remove more essences, pick them randomly
    world.random.shuffle(world.essences_in_game)
    world.essences_in_game = world.essences_in_game[0:world.options.placed_essences]


def randomize_default_seasons(world) -> None:
    from ...data.Constants import SEASONS, SEASON_NAMES
    if world.options.default_seasons == "randomized":
        seasons_pool = SEASONS
    elif world.options.default_seasons.current_key.endswith("singularity"):
        single_season = world.options.default_seasons.current_key.replace("_singularity", "")
        if single_season == "random":
            single_season = world.random.choice(SEASONS)
        else:
            single_season = next(byte for byte, name in SEASON_NAMES.items() if name == single_season)
        seasons_pool = [single_season]
    else:
        return

    for region in world.default_seasons:
        if region == "HORON_VILLAGE" and not world.options.normalize_horon_village_season:
            continue
        world.default_seasons[region] = world.random.choice(seasons_pool)


def randomize_old_men(world) -> None:
    if world.options.shuffle_old_men == OraclesOldMenShuffle.option_shuffled_values:
        shuffled_rupees = list(world.old_man_rupee_values.values())
        world.random.shuffle(shuffled_rupees)
        world.old_man_rupee_values = dict(zip(world.old_man_rupee_values, shuffled_rupees))
    elif world.options.shuffle_old_men == OraclesOldMenShuffle.option_random_values:
        for key in world.old_man_rupee_values.keys():
            sign = world.random.choice([-1, 1])
            world.old_man_rupee_values[key] = world.random.choice(get_old_man_values_pool()) * sign
    elif world.options.shuffle_old_men == OraclesOldMenShuffle.option_random_positive_values:
        for key in world.old_man_rupee_values.keys():
            world.old_man_rupee_values[key] = world.random.choice(get_old_man_values_pool())
    else:
        # Remove the old man values from the pool so that they don't count negative when they are shuffled as items
        world.old_man_rupee_values = {}


def randomize_shop_order(world) -> None:
    world.shop_order = [
        ["horonShop1", "horonShop2", "horonShop3"],
        ["memberShop1", "memberShop2", "memberShop3"]
    ] if world.seasons else [
        ["lynnaShop1", "lynnaShop2", "lynnaShop3"],
        ["hiddenShop1", "hiddenShop2", "hiddenShop3"]
    ] if world.ages else world.shop_order
    if not world.romhack:
        world.shop_order.append(["syrupShop1", "syrupShop2", "syrupShop3"])
        if world.options.advance_shop:
            world.shop_order.append(["advanceShop1", "advanceShop2", "advanceShop3"])
        if world.options.shuffle_business_scrubs:
            if world.seasons:
                world.shop_order.append(["spoolSwampScrub", "samasaCaveScrub", "d2Scrub", "d4Scrub"])
    world.random.shuffle(world.shop_order)


def randomize_shop_prices(world) -> None:
    if world.options.shop_prices == "vanilla":
        if world.options.enforce_potion_in_shop:
            world.shop_prices[world.shop_order[0][2]] = 300
        return
    if world.options.shop_prices == "free":
        world.shop_prices = {k: 0 for k in world.shop_prices}
        return

    # Prices are randomized, get a random price that follow set options for each shop location.
    # Values must be rounded to nearest valid rupee amount.
    average = AVERAGE_PRICE_PER_LOCATION[world.options.shop_prices.current_key]
    deviation = min(19 * (average / 50), 100)
    for i, shop in enumerate(world.shop_order):
        shop_price_factor = (i / len(world.shop_order)) + 0.5
        for location_code in shop:
            value = world.random.gauss(average, deviation) * shop_price_factor
            world.shop_prices[location_code] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - value))
    
    if world.seasons:
        # Subrosia market special cases
        for i in range(2, 6):
            value = world.random.gauss(average, deviation) * 0.5
            world.shop_prices[f"subrosianMarket{i}"] = min(VALID_RUPEE_PRICE_VALUES, key=lambda x: abs(x - value))
    elif world.ages:
        from ...data.Constants import VALID_SEED_PRICE_VALUES
        # Tokay Market special cases
        if average > 99:
            # The seed limit is 99 in ages. Because of that, we have to change the average variable to 99 if we were to ever hit the average cost case above that.
            average = 99
            # update deviation variable to meet our new average cost of 99 seeds.
            deviation = min(19 * (average / 49.5), 99)
        ## Loop until the tokay market shop prices are randomized.
        for i in range(1, 3):
            value = world.random.gauss(average, deviation) * 0.5
            world.shop_prices[f"tokayMarket{i}"] = min(VALID_SEED_PRICE_VALUES, key=lambda x: abs(x - value))


def compute_rupee_requirements(world) -> None:
    # Compute global rupee requirements for each shop, based on shop order and item prices
    cumulated_requirement = 0
    for shop in world.shop_order:
        if shop[0].startswith("advance") and not world.options.advance_shop:
            continue
        if shop[0].endswith("Scrub") and not world.options.shuffle_business_scrubs:
            continue
        # Add the price of each shop location in there to the requirement
        for shop_location in shop:
            cumulated_requirement += world.shop_prices[shop_location]
        # Deduce the shop name from the code of the first location
        shop_name = shop[0]
        if not shop_name.endswith("Scrub"):
            shop_name = shop_name[:-1]
        world.shop_rupee_requirements[shop_name] = cumulated_requirement


def create_random_rings_pool(world) -> None:
    # Get a subset of as many rings as needed, with a potential filter depending on chosen options
    ring_names = [name for name, idata in ITEMS_DATA.items() if "ring" in idata]

    # Remove required rings because they'll be added later anyway
    ring_names = [name for name in ring_names if name not in world.options.required_rings.value and name not in world.options.excluded_rings.value]

    world.random.shuffle(ring_names)
    world.random_rings_pool = ring_names

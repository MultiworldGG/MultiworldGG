import math
from typing import Dict, TextIO, List

from BaseClasses import CollectionState, Entrance, Item, ItemClassification, MultiWorld, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import (
    YachtDiceItem,
    item_groups,
    item_table,
    all_categories,
    find_category_index,
    get_normal_categories,
    get_alt_categories,
)
from .Locations import YachtDiceLocation, all_locations, ini_locations, LocData, starting_index
from .Options import (
    AddExtraPoints,
    AddStoryChapters,
    TotalNumberOfCategories,
    AllowedNormalCategories,
    AllowedAlternativeCategories,
    PercentageAlternativeCategories,
    AllowedStartingCategories,
    NumberOfStartingCategories,
    GameDifficulty,
    MinimalNumberOfDiceAndRolls,
    MinimizeExtraItems,
    PointsSize,
    YachtDiceOptions,
    DoubleCategoryCalculation,
    yd_option_groups,
)
from Fill import remaining_fill
from .Rules import (
    Category,
    dice_simulation_fill_pool,
    set_yacht_completion_rules,
    set_yacht_rules,
    dice_simulation_strings,
)


class YachtDiceWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Yacht Dice. This guide covers single-player, multiworld, and website.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]

    option_groups = yd_option_groups


class YachtDiceWorld(World):
    """
    Yacht Dice is a straightforward game, custom-made for Archipelago/MWGG,
    where you cast your dice to chart a course for high scores,
    unlocking valuable treasures along the way.
    Discover more dice, extra rolls, multipliers,
    and unlockable categories to navigate the depths of the game.
    Roll your way to victory by reaching the target score!
    """

    game: str = "Yacht Dice"
    options_dataclass = YachtDiceOptions

    web = YachtDiceWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in all_locations.items()}

    item_name_groups = item_groups
    
    apworld_version = "2.3.3"

    def _get_yachtdice_data(self):
        return {
            # "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "race": self.multiworld.is_race,
        }

    # print(
    #     dice_simulation_strings(
    #         [
    #             Category('Category Fives', 4),
    #             Category('Category Small Straight', 1),
    #             Category('Category Pair', 1),
    #             Category('Category Full House', 1),
    #         ],
    #         3,
    #         2,
    #         0.1,
    #         0.04,
    #         True,
    #         3,
    #         debug=True
    #     )
    # )
    # exit()

    def generate_early(self):
        """
        In generate early, we fill the item-pool, then determine the number of locations, and add filler items.
        """
        self.itempool = []
        self.precollected = []

        # number of dice and rolls in the pull
        opt_dice_and_rolls = self.options.minimal_number_of_dice_and_rolls

        if opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_5_dice_and_3_rolls:
            num_of_dice = 5
            num_of_rolls = 3
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_5_dice_and_5_rolls:
            num_of_dice = 5
            num_of_rolls = 5
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_6_dice_and_4_rolls:
            num_of_dice = 6
            num_of_rolls = 4
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_7_dice_and_3_rolls:
            num_of_dice = 7
            num_of_rolls = 3
        elif opt_dice_and_rolls == MinimalNumberOfDiceAndRolls.option_8_dice_and_2_rolls:
            num_of_dice = 8
            num_of_rolls = 2
        else:
            raise Exception(f"[Yacht Dice] Unknown MinimalNumberOfDiceAndRolls options {opt_dice_and_rolls}")

        # amount of dice and roll fragments needed to get a dice or roll
        self.frags_per_dice = self.options.number_of_dice_fragments_per_dice.value
        self.frags_per_roll = self.options.number_of_roll_fragments_per_roll.value

        if self.options.minimize_extra_items == MinimizeExtraItems.option_yes_please:
            self.frags_per_dice = min(self.frags_per_dice, 2)
            self.frags_per_roll = min(self.frags_per_roll, 2)

        # set difficulty
        self.difficulty = self.options.game_difficulty.value
        self.double_category_doubled = (
            self.options.double_category_calculation == DoubleCategoryCalculation.option_double
        )

        # which categories to use?
        normal_categories = []
        if self.options.percentage_alternative_categories.value < 100:
            normal_categories = sorted(self.options.allowed_normal_categories.value)
        alternative_categories = []
        if self.options.percentage_alternative_categories.value > 0:
            alternative_categories = sorted(self.options.allowed_alternative_categories.value)
        all_candidate_categories = normal_categories + alternative_categories

        if not all_candidate_categories:  # no categories chosen at all, just use all categories
            all_candidate_categories = list(all_categories.keys())
            normal_categories = list(get_normal_categories().keys())
            alternative_categories = list(get_alt_categories().keys())

        number_of_categories = min(
            len(normal_categories) + len(alternative_categories), self.options.total_number_of_categories.value
        )
        number_of_starting_categories = self.options.number_of_starting_categories.value

        weight_normal = 100 - self.options.percentage_alternative_categories.value
        weight_alt = self.options.percentage_alternative_categories.value

        weights = [weight_normal] * len(normal_categories) + [weight_alt] * len(alternative_categories)
        # first entry for regular weights, second for starting category weights
        weights = {i: [weights[i], weights[i]] for i in range(len(all_candidate_categories))}

        for i, cat in enumerate(all_candidate_categories):
            if cat not in self.options.allowed_starting_categories.value:
                weights[i][1] = 0

        adding_starting_categories = 1
        enabled_categories = []
        starting_categories = []
        for _ in range(number_of_categories):
            if adding_starting_categories:
                if sum([weights[i][1] for i in weights.keys()]) == 0:
                    weights = {i: [weights[i][0], weights[i][0]] for i in weights.keys()}

            if sum([weights[i][adding_starting_categories] for i in weights.keys()]) == 0:
                break
            ind = self.random.choices(
                list(weights.keys()), weights=[weights[i][adding_starting_categories] for i in weights.keys()]
            )[0]
            
            # Pop from weights and all_candidate_categories before appending
            enabled_categories.append(ind)
            if adding_starting_categories:
                starting_categories.append(ind)
            weights.pop(ind)

            if len(starting_categories) == number_of_starting_categories:
                adding_starting_categories = 0

        self.cat_indices = sorted(enabled_categories)
        self.possible_categories = [all_candidate_categories[i] for i in self.cat_indices]

        for cat in self.cat_indices:
            if cat in starting_categories:
                self.precollected.append(all_candidate_categories[cat])
            else:
                self.itempool.append(all_candidate_categories[cat])
        # end of category selection

        # Also start with one Roll and one Dice
        self.precollected.append("Dice")
        num_of_dice_to_add = num_of_dice - 1
        self.precollected.append("Roll")
        num_of_rolls_to_add = num_of_rolls - 1

        self.skip_early_locations = False
        if self.options.minimize_extra_items == MinimizeExtraItems.option_yes_please:
            self.precollected.append("Dice")
            num_of_dice_to_add -= 1
            self.precollected.append("Roll")
            num_of_rolls_to_add -= 1
            self.skip_early_locations = True

        if num_of_dice_to_add > 0:
            self.itempool.append("Dice")
            num_of_dice_to_add -= 1
        if num_of_rolls_to_add > 0:
            self.itempool.append("Roll")
            num_of_rolls_to_add -= 1

        # if one fragment per dice, just add "Dice" objects
        if num_of_dice_to_add > 0:
            if self.frags_per_dice == 1:
                self.itempool += ["Dice"] * num_of_dice_to_add  # minus one because one is in start inventory
            else:
                self.itempool += ["Dice Fragment"] * (self.frags_per_dice * num_of_dice_to_add)

        # if one fragment per roll, just add "Roll" objects
        if num_of_rolls_to_add > 0:
            if self.frags_per_roll == 1:
                self.itempool += ["Roll"] * num_of_rolls_to_add  # minus one because one is in start inventory
            else:
                self.itempool += ["Roll Fragment"] * (self.frags_per_roll * num_of_rolls_to_add)

        already_items = len(self.itempool)

        # Yacht Dice needs extra filler items so it doesn't get stuck in generation.
        # For now, we calculate the number of extra items we'll need later.
        if self.options.minimize_extra_items == MinimizeExtraItems.option_yes_please:
            extra_percentage = max(0.1, 0.8 - self.multiworld.players / 10)
        elif self.options.minimize_extra_items == MinimizeExtraItems.option_no_dont:
            extra_percentage = 0.72
        else:
            raise Exception(f"[Yacht Dice] Unknown MinimizeExtraItems options {self.options.minimize_extra_items}")

        extra_locations_needed = max(10, math.ceil(already_items * extra_percentage))

        # max score is the value of the last check. Goal score is the score needed to 'finish' the game
        self.max_score = self.options.score_for_last_check.value
        self.goal_score = min(self.max_score, self.options.score_for_goal.value)

        # it is possible the player starts with very bad items,
        # so we fill the starting inventory until at least 5 score is possible
        if self.options.fill_start_inventory_if_needed:
            c = 0
            while (
                dice_simulation_fill_pool(
                    self.precollected,
                    self.frags_per_dice,
                    self.frags_per_roll,
                    self.possible_categories,
                    self.double_category_doubled,
                    self.difficulty,
                )
                < 5
                and c < 16
            ):
                if c % 3 == 0:
                    category = self.random.choices(
                        self.possible_categories, weights=[2 if i < 9 else 1 for i in self.cat_indices]
                    )[0]
                    self.precollected.append(category)
                elif c % 3 == 1:
                    self.precollected.append("Dice")
                else:
                    self.precollected.append("Roll")
                c += 1

        # Yacht Dice adds items into the pool until a score of at least 1000 is reached.
        # the yaml contains weights, which determine how likely it is that specific items get added.
        # If all weights are 0, some of them will be made to be non-zero later.
        weights: Dict[str, float] = {
            "Dice": self.options.weight_of_dice.value,
            "Roll": self.options.weight_of_roll.value,
            "Fixed Score Multiplier": self.options.weight_of_fixed_score_multiplier.value,
            "Step Score Multiplier": self.options.weight_of_step_score_multiplier.value,
            "Double category": self.options.weight_of_double_category.value,
            "Points": self.options.weight_of_points.value,
        }

        # if the player wants extra rolls or dice, fill the pool with fragments until close to an extra roll/dice
        if weights["Dice"] > 0 and self.frags_per_dice > 1:
            self.itempool += ["Dice Fragment"] * (self.frags_per_dice - 1)
        if weights["Roll"] > 0 and self.frags_per_roll > 1:
            self.itempool += ["Roll Fragment"] * (self.frags_per_roll - 1)

        # calibrate the weights, since the impact of each of the items is different
        weights["Dice"] = weights["Dice"] / 5 * self.frags_per_dice
        weights["Roll"] = weights["Roll"] / 5 * self.frags_per_roll

        extra_points_added = [0]  # make it a mutible type so we can change the value in the function
        step_score_multipliers_added = [0]

        # function that will return which item to add next, based on weights and current pool
        def get_item_to_add(weights, extra_points_added, step_score_multipliers_added):
            all_items = self.itempool + self.precollected
            dice_fragments_in_pool = all_items.count("Dice") * self.frags_per_dice + all_items.count("Dice Fragment")
            if dice_fragments_in_pool + 1 >= 9 * self.frags_per_dice:
                weights["Dice"] = 0  # don't allow >=9 dice
            roll_fragments_in_pool = all_items.count("Roll") * self.frags_per_roll + all_items.count("Roll Fragment")
            if roll_fragments_in_pool + 1 >= 6 * self.frags_per_roll:
                weights["Roll"] = 0  # don't allow >= 6 rolls

            # Don't allow too many extra points
            if extra_points_added[0] > 400:
                weights["Points"] = 0

            if step_score_multipliers_added[0] > 10:
                weights["Step Score Multiplier"] = 0

            # if all weights are zero, allow to add fixed score multiplier, double category, points.
            if sum(weights.values()) == 0:
                weights["Fixed Score Multiplier"] = 1
                weights["Double category"] = 1
                if extra_points_added[0] <= 400:
                    weights["Points"] = 1

            # Next, add the appropriate item. We'll slightly alter weights to avoid too many of the same item
            which_item_to_add = self.random.choices(list(weights.keys()), weights=list(weights.values()))[0]

            if which_item_to_add == "Dice":
                weights["Dice"] /= 1 + self.frags_per_dice
                return "Dice" if self.frags_per_dice == 1 else "Dice Fragment"
            elif which_item_to_add == "Roll":
                weights["Roll"] /= 1 + self.frags_per_roll
                return "Roll" if self.frags_per_roll == 1 else "Roll Fragment"
            elif which_item_to_add == "Fixed Score Multiplier":
                weights["Fixed Score Multiplier"] /= 1.05
                return "Fixed Score Multiplier"
            elif which_item_to_add == "Step Score Multiplier":
                weights["Step Score Multiplier"] /= 1.1
                step_score_multipliers_added[0] += 1
                return "Step Score Multiplier"
            elif which_item_to_add == "Double category":
                # Below entries are the weights to add each category.
                # Prefer to add choice or number categories, because the other categories are too "all or nothing",
                # which often don't give any points, until you get overpowered, and then they give all points.

                weights["Double category"] /= 1.1
                return self.random.choices(
                    self.possible_categories, weights=[2 if i < 9 else 1 for i in self.cat_indices]
                )[0]
            elif which_item_to_add == "Points":
                score_dist = self.options.points_size
                probs = {"1 Point": 1, "10 Points": 0, "100 Points": 0}
                if score_dist == PointsSize.option_small:
                    probs = {"1 Point": 0.9, "10 Points": 0.1, "100 Points": 0}
                elif score_dist == PointsSize.option_medium:
                    probs = {"1 Point": 0, "10 Points": 1, "100 Points": 0}
                elif score_dist == PointsSize.option_large:
                    probs = {"1 Point": 0, "10 Points": 0.3, "100 Points": 0.7}
                elif score_dist == PointsSize.option_mix:
                    probs = {"1 Point": 0.3, "10 Points": 0.4, "100 Points": 0.3}
                else:
                    raise Exception(f"[Yacht Dice] Unknown PointsSize options {score_dist}")
                choice = self.random.choices(list(probs.keys()), weights=list(probs.values()))[0]
                if choice == "1 Point":
                    weights["Points"] /= 1.01
                    extra_points_added[0] += 1
                    return "1 Point"
                elif choice == "10 Points":
                    weights["Points"] /= 1.1
                    extra_points_added[0] += 10
                    return "10 Points"
                elif choice == "100 Points":
                    weights["Points"] /= 2
                    extra_points_added[0] += 100
                    return "100 Points"
                else:
                    raise Exception("Unknown point value (Yacht Dice)")
            else:
                raise Exception(f"Invalid index when adding new items in Yacht Dice: {which_item_to_add}")

        # adding 17 items as a start seems like the smartest way to get close to 1000 points
        for _ in range(17):
            self.itempool.append(get_item_to_add(weights, extra_points_added, step_score_multipliers_added))

        score_in_logic = dice_simulation_fill_pool(
            self.itempool + self.precollected,
            self.frags_per_dice,
            self.frags_per_roll,
            self.possible_categories,
            self.double_category_doubled,
            self.difficulty,
        )

        # if we overshoot, remove items until you get below 1000, then return the last removed item
        if score_in_logic > 1000:
            removed_item = ""
            while score_in_logic > 1000:
                removed_item = self.itempool.pop()
                score_in_logic = dice_simulation_fill_pool(
                    self.itempool + self.precollected,
                    self.frags_per_dice,
                    self.frags_per_roll,
                    self.possible_categories,
                    self.double_category_doubled,
                    self.difficulty,
                )
            self.itempool.append(removed_item)
        else:
            # Keep adding items until a score of 1000 is in logic
            while score_in_logic < 1000:
                item_to_add = get_item_to_add(weights, extra_points_added, step_score_multipliers_added)
                self.itempool.append(item_to_add)
                if item_to_add == "1 Point":
                    score_in_logic += 1
                elif item_to_add == "10 Points":
                    score_in_logic += 10
                elif item_to_add == "100 Points":
                    score_in_logic += 100
                else:
                    score_in_logic = dice_simulation_fill_pool(
                        self.itempool + self.precollected,
                        self.frags_per_dice,
                        self.frags_per_roll,
                        self.possible_categories,
                        self.double_category_doubled,
                        self.difficulty,
                    )

        # with this little categories, add more to reduce fill errors
        if len(self.possible_categories) == 3:
            self.itempool.append(self.possible_categories[0])
            self.itempool.append(self.possible_categories[1])
            self.itempool.append(self.possible_categories[2])
        elif len(self.possible_categories) == 2:
            self.itempool.append(self.possible_categories[0])
            self.itempool.append(self.possible_categories[1])
            self.itempool.append(self.possible_categories[0])
            self.itempool.append(self.possible_categories[1])
        elif len(self.possible_categories) == 1:
            self.itempool.append(self.possible_categories[0])
            self.itempool.append(self.possible_categories[0])
            self.itempool.append(self.possible_categories[0])
            self.itempool.append(self.possible_categories[0])
            self.multiworld.early_items[self.player][self.possible_categories[0]] = 2

        self.scores_in_logic = [
            f"{dice_simulation_fill_pool(self.itempool + self.precollected, self.frags_per_dice, self.frags_per_roll, self.possible_categories, self.double_category_doubled, d)}{'*' if d == self.difficulty else ''}"
            for d in [1, 2, 3, 4, 5, 6, 7]
        ]

        self.itempool += ["Key"] * self.options.number_of_keys.value

        # count the number of locations in the game.
        already_items = len(self.itempool) + 1  # +1 because of Victory item

        # We need to add more filler/useful items if there are many items in the pool to guarantee successful generation
        extra_locations_needed += (already_items - 45) // 15
        self.number_of_locations = already_items + extra_locations_needed

        # From here, we will count the number of items in the self.itempool, and add useful/filler items to the pool,
        # making sure not to exceed the number of locations.

        # first, we flood the entire pool with extra points (useful), if that setting is chosen.
        if self.options.add_bonus_points == AddExtraPoints.option_all_of_it:  # all of the extra points
            already_items = len(self.itempool) + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 100)

        # second, we flood the entire pool with story chapters (filler), if that setting is chosen.
        if self.options.add_story_chapters == AddStoryChapters.option_all_of_it:  # all of the story chapters
            already_items = len(self.itempool) + 1
            number_of_items = min(self.number_of_locations - already_items, 100)
            number_of_items = (number_of_items // 10) * 10  # story chapters always come in multiples of 10
            self.itempool += ["Story Chapter"] * number_of_items

        # add some extra points (useful)
        if self.options.add_bonus_points == AddExtraPoints.option_sure:  # add extra points if wanted
            already_items = len(self.itempool) + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 10)

        # add some story chapters (filler)
        if self.options.add_story_chapters == AddStoryChapters.option_sure:  # add extra points if wanted
            already_items = len(self.itempool) + 1
            if self.number_of_locations - already_items >= 10:
                self.itempool += ["Story Chapter"] * 10

        # add some more extra points if there is still room
        if self.options.add_bonus_points == AddExtraPoints.option_sure:
            already_items = len(self.itempool) + 1
            self.itempool += ["Bonus Point"] * min(self.number_of_locations - already_items, 10)

        # add some encouragements filler-items if there is still room
        already_items = len(self.itempool) + 1
        self.itempool += ["Encouragement"] * min(self.number_of_locations - already_items, 5)

        # add some fun facts filler-items if there is still room
        already_items = len(self.itempool) + 1
        self.itempool += ["Fun Fact"] * min(self.number_of_locations - already_items, 5)

        # finally, add some "Good RNG" and "Bad RNG" items to complete the item pool
        # these items are filler and do not do anything.

        # probability of Good and Bad rng, based on difficulty for fun :)
        p = min(1, max(0.2, 1.1 - 0.2 * self.difficulty))
        already_items = len(self.itempool) + 1

        number_of_RNG_items = self.number_of_locations - already_items

        num_good_rng = round(number_of_RNG_items * p)
        num_bad_rng = number_of_RNG_items - num_good_rng
        self.itempool += ["Good RNG"] * num_good_rng
        self.itempool += ["Bad RNG"] * num_bad_rng

        # we are done adding items. Now because of the last step, number of items should be number of locations
        already_items = len(self.itempool) + 1
        if already_items != self.number_of_locations:
            raise Exception(
                f"[Yacht Dice] Number in self.itempool is not number of locations "
                f"{already_items} {self.number_of_locations}."
            )

        # add precollected items using push_precollected. Items in self.itempool get created in create_items
        for item in self.precollected:
            self.multiworld.push_precollected(self.create_item(item))

        # make sure one dice and one roll is early, so that you will have 2 dice and 2 rolls soon
        self.multiworld.early_items[self.player]["Dice"] = 1
        self.multiworld.early_items[self.player]["Roll"] = 1

        # up next, prepare locations. We do this here because we might need to add more filler items
        # call the ini_locations function, that generates locations based on the inputs.
        self.score_locations = ini_locations(
            self.goal_score,
            self.max_score,
            self.number_of_locations,
            self.difficulty,
            self.skip_early_locations,
            self.multiworld.players,
            self.options.include_scores.value,
        )

        number_of_RNG_items = len(self.score_locations) - len(self.itempool) - 1

        # there should be exactly one more location than items (because of Victory event)
        if number_of_RNG_items > 0:
            self.num_good_rng = round(number_of_RNG_items * p)
            self.num_bad_rng = number_of_RNG_items - self.num_good_rng
            self.itempool += ["Good RNG"] * self.num_good_rng
            self.itempool += ["Bad RNG"] * self.num_bad_rng

    def create_items(self):
        num_rng_in_pool = 0
        self.lock_locally = []  # items that are locked locally, so they don't get added to the item pool
        for name in self.itempool:
            if name == "Good RNG" or name == "Bad RNG":
                num_rng_in_pool += 1
                if num_rng_in_pool > self.options.maximum_rng_in_itempool.value:
                    self.lock_locally.append(self.create_item(name))
                else:
                    self.multiworld.itempool.append(self.create_item(name))
            else:
                self.multiworld.itempool.append(self.create_item(name))

        weights = [(i + 1) * (10000 if i > 10 else 1) for i in range(len(self.available_locations))]
        for item in self.lock_locally:
            location = self.random.choices(self.available_locations, weights=weights, k=1)[0]
            weights.remove(weights[self.available_locations.index(location)])
            self.available_locations.remove(location)
            location.place_locked_item(item)

    def create_regions(self):
        location_table = {
            f"{score} score": LocData(starting_index + score, "Board", score) for score in self.score_locations
        }

        # simple menu-board construction
        menu = Region("Menu", self.player, self.multiworld)
        board = Region("Board", self.player, self.multiworld)

        # add locations to board, one for every location in the location_table
        board.locations = [
            YachtDiceLocation(self.player, loc_name, loc_data.score, loc_data.id, board)
            for loc_name, loc_data in location_table.items()
            if loc_data.region == board.name
        ]

        # Change the victory location to an event and place the Victory item there.
        victory_location_name = f"{self.goal_score} score"
        self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            Item("Victory", ItemClassification.progression, None, self.player)
        )

        # Randomly select self.lock_locally items from board.locations excluding the victory location
        self.available_locations = [loc for loc in board.locations if loc.name != victory_location_name]

        # add the regions
        connection = Entrance(self.player, "New Board", menu)
        menu.exits.append(connection)
        connection.connect(board)
        self.multiworld.regions += [menu, board]

    def get_filler_item_name(self) -> str:
        return "Good RNG"

    def set_rules(self):
        """
        set rules per location, and add the rule for beating the game
        """
        set_yacht_rules(
            self.multiworld,
            self.player,
            self.frags_per_dice,
            self.frags_per_roll,
            self.possible_categories,
            self.double_category_doubled,
            self.difficulty,
            self.options.number_of_keys.value,
        )
        set_yacht_completion_rules(self.multiworld, self.player)

    def fill_slot_data(self):
        """
        make slot data, which consists of yachtdice_data, options, and some other variables.
        """
        yacht_dice_data = self._get_yachtdice_data()
        yacht_dice_options = self.options.as_dict(
            "game_difficulty",
            "score_for_last_check",
            "score_for_goal",
            "number_of_dice_fragments_per_dice",
            "number_of_roll_fragments_per_roll",
            "which_story",
            "allow_manual_input",
            "receive_death_link_toggle",
            "send_death_link_toggle",
            "number_of_keys",
        )
        slot_data = {**yacht_dice_data, **yacht_dice_options}  # combine the two
        slot_data["number_of_dice_fragments_per_dice"] = self.frags_per_dice
        slot_data["number_of_roll_fragments_per_roll"] = self.frags_per_roll
        slot_data["double_category_doubled"] = self.double_category_doubled
        slot_data["goal_score"] = self.goal_score
        slot_data["last_check_score"] = self.max_score
        slot_data["allowed_categories"] = self.possible_categories
        slot_data["ap_world_version"] = self.apworld_version
        slot_data["precollected"] = [item.code for item in self.multiworld.precollected_items[self.player]]
        slot_data["number_of_locations"] = self.number_of_locations
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = YachtDiceItem(name, item_data.classification, item_data.code, self.player)
        return item

    # We overwrite these function to monitor when states have changed. See also dice_simulation in Rules.py
    def collect(self, state: CollectionState, item: Item) -> bool:
        change = super().collect(state, item)
        if change:
            state.prog_items[self.player]["state_is_fresh"] = 0

        return change

    def remove(self, state: CollectionState, item: Item) -> bool:
        change = super().remove(state, item)
        if change:
            state.prog_items[self.player]["state_is_fresh"] = 0

        return change

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        spoiler_handle.write(f"\nYacht Dice scores in logic for Player {self.player_name}: {self.scores_in_logic}")
        spoiler_handle.write(f"\nYacht Dice items in pool for Player {self.player_name}: {self.itempool}")
        spoiler_handle.write(f"\nYacht Dice starting categories for Player {self.player_name}: {self.precollected}")

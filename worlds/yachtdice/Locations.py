import typing

from BaseClasses import Location


class LocData(typing.NamedTuple):
    id: int
    region: str
    score: int


class YachtDiceLocation(Location):
    game: str = "Yacht Dice"

    def __init__(self, player: int, name: str, score: int, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.yacht_dice_score = score


all_locations = {}
starting_index = 16871244500  # 500 more than the starting index for items (not necessary, but this is what it is now)


def all_locations_fun(max_score):
    """
    Function that is called when this file is loaded, which loads in ALL possible locations, score 1 to 1000
    """
    return {f"{i} score": LocData(starting_index + i, "Board", i) for i in range(1, max_score + 1)}


def ini_locations(
    goal_score, max_score, number_of_locations, dif, skip_early_locations, number_of_players, include_scores
):
    """
    function that loads in all locations necessary for the game, so based on options.
    will make sure that goal_score and max_score are included locations
    """
    scaling = 2.2  # parameter that determines how many low-score location there are.
    # need more low-score locations or lower difficulties:
    if dif == 1:
        scaling = 3
    else:
        scaling = 2.3

    scores = []
    # the scores follow the function int( 1 + (percentage ** scaling) * (max_score-1) )
    # however, this will have many low values, sometimes repeating.
    # to avoid repeating scores, highest_score keeps tracks of the highest score location
    # and the next score will always be at least highest_score + 1
    # note that current_score is at most max_score-1
    highest_score = 0
    start_score = 0

    if skip_early_locations:
        scaling = 1.95
        if number_of_players > 2:
            scaling = max(1.3, 2.2 - number_of_players * 0.1)

    for i in range(number_of_locations - 1):
        percentage = i / number_of_locations
        current_score = int(start_score + 1 + (percentage**scaling) * (max_score - start_score - 2))
        if current_score <= highest_score:
            current_score = highest_score + 1
        highest_score = current_score
        scores += [current_score]

    if goal_score != max_score:
        # if the goal score is not in the list, find the closest one and make it the goal.
        if goal_score not in scores:
            closest_num = min(scores, key=lambda x: abs(x - goal_score))
            scores[scores.index(closest_num)] = goal_score

    scores += [max_score]

    if include_scores == {"Everything"}:
        include_scores = [str(i) for i in range(1, max_score)]
    else:
        include_scores = [x for x in include_scores if x != "Everything"]
        include_scores = sorted({int(x) for x in include_scores})[:10]

    # Adjust scores to include the values in the "include" list
    include_scores = [int(value) for value in sorted(include_scores)]
    for value in include_scores:
        if value not in scores and value < max_score:
            # Exclude goal_score, max_score, and already included values from search
            candidate_scores = [s for s in scores if s not in (goal_score, max_score) and s not in include_scores]

            if candidate_scores:  # If there are candidates to replace
                closest_num = min(candidate_scores, key=lambda x: abs(x - value))
                if abs(closest_num - value) < 100:  # only adjust score if it's close enough
                    scores[scores.index(closest_num)] = value  # Replace the closest candidate with the desired value
                else:
                    scores.append(value)
            else:
                scores.append(value)  # If no candidates remain, just add the value to scores

    return sorted(scores)


# we need to run this function to initialize all scores from 1 to 1000, even though not all are used
all_locations = all_locations_fun(1000)

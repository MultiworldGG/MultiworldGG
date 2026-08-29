from typing import TYPE_CHECKING, Dict, List, Tuple

from random import Random

from . import data_loader
from .data_loader import (original_portal_level_order, alternative_portal_level_order, grannys_island_level_order,
                          miscellaneous_level_order, unfinished_levels)
from .options import YellowTaxiOptions

def get_level_order(options: YellowTaxiOptions, random: Random, goal_portal : str) -> List[str]:
    portal_order : List[str] = []
    valid_portals : List[str] = []
    shuffled_portals : bool = False
    allow_excluded : bool = (options.allow_shuffling_removed_levels.value >=
                             options.allow_shuffling_removed_levels.option_portal_levels_only)
    if options.portal_order.value == options.portal_order.option_shuffle:
        num_portals : int
        num_portals, valid_portals = get_portal_randomization_count_and_pool(options, goal_portal)
        random.shuffle(valid_portals)
        goal_portal_index : int = original_portal_level_order.index(goal_portal)
        valid_portals.insert(goal_portal_index, goal_portal)
        for i in range(0, len(original_portal_level_order)):
            if i < num_portals:
                portal_order += [valid_portals[i]]
            else:
                portal_order += ["Excluded"]
        valid_portals.remove(goal_portal)
        shuffled_portals : bool = True
    else:
        base_portal_order : List[str]
        if options.portal_order.value == options.portal_order.option_internal:
            base_portal_order = alternative_portal_level_order
        else:
            base_portal_order = list(original_portal_level_order)

        skip_remaining : bool = False
        for portal in base_portal_order:
            if portal == goal_portal and options.remove_post_goal_portals:
                skip_remaining = True
            elif skip_remaining or portal in unfinished_levels:
                if allow_excluded and portal not in unfinished_levels:
                    valid_portals += [portal]
                portal_order += ["Excluded"]
                continue
            portal_order += [portal]

    grannys_order : List[str] = []
    valid_grannys : List[str] = []
    shuffled_grannys : bool = False
    allow_excluded = (options.allow_shuffling_removed_levels.value >=
                      options.allow_shuffling_removed_levels.option_any)
    if options.shuffle_grannys_levels:
        if allow_excluded:
            valid_grannys = ["Gym Gears", "Fecal Matters", "Flushed Away"]
        else:
            if options.gym_gears_unlock_condition.value != options.gym_gears_unlock_condition.option_exclude:
                valid_grannys += ["Gym Gears"]
            if options.fecal_matters_unlock_condition.value != options.fecal_matters_unlock_condition.option_exclude:
                valid_grannys += ["Fecal Matters"]
            # Limitation: Logical access to sewer island isn't considered here.
            # Fine for now but eventually look into making "default" work as expected. Portal pool is already known!
            if options.flushed_away_unlock_condition.value != options.flushed_away_unlock_condition.option_exclude:
                valid_grannys += ["Flushed Away"]

        random.shuffle(valid_grannys)

        grannys_index : int = 0

        if options.gym_gears_unlock_condition.value != options.gym_gears_unlock_condition.option_exclude:
            grannys_order += [valid_grannys[grannys_index]]
            grannys_index += 1
        else:
            grannys_order += ["Excluded"]
        if options.fecal_matters_unlock_condition.value != options.fecal_matters_unlock_condition.option_exclude:
            grannys_order += [valid_grannys[grannys_index]]
            grannys_index += 1
        else:
            grannys_order += ["Excluded"]
        # Limitation: Logical access to sewer island isn't considered here.
        # Fine for now but eventually look into making "default" work as expected. Portal pool is already known!
        if options.flushed_away_unlock_condition.value != options.flushed_away_unlock_condition.option_exclude:
            grannys_order += [valid_grannys[grannys_index]]
            grannys_index += 1
        else:
            grannys_order += ["Excluded"]

        shuffled_grannys = True
    else:
        grannys_order = list(grannys_island_level_order)

        if options.gym_gears_unlock_condition.value == options.gym_gears_unlock_condition.option_exclude:
            if allow_excluded:
                valid_grannys += ["Gym Gears"]
            grannys_order[0] = "Excluded"
        if options.fecal_matters_unlock_condition.value == options.fecal_matters_unlock_condition.option_exclude:
            if allow_excluded:
                valid_grannys += ["Fecal Matters"]
            grannys_order[1] = "Excluded"
        # Limitation: Logical access to sewer island isn't considered here.
        # Fine for now but eventually look into making "default" work as expected. Portal pool is already known!
        if options.flushed_away_unlock_condition.value == options.flushed_away_unlock_condition.option_exclude:
            if allow_excluded:
                valid_grannys += ["Flushed Away"]
            grannys_order[2] = "Excluded"


    misc_order : List[str] = []
    valid_misc : List[str] = []
    if options.shuffle_rocket_entrance:
        valid_misc += [miscellaneous_level_order[0]]
    if options.shuffle_time_trial_entrances:
        valid_misc += list(miscellaneous_level_order[1:4])
    if options.shuffle_psycho_taxi_entrance:
        valid_misc += [miscellaneous_level_order[4]]

    random.shuffle(valid_misc)

    misc_index : int = 0

    if options.rocket_unlock_condition.value == options.rocket_unlock_condition.option_exclude:
        misc_order += ["Excluded"]
    elif options.shuffle_rocket_entrance:
        misc_order += [valid_misc[misc_index]]
        misc_index += 1
    else:
        misc_order += [str(miscellaneous_level_order[0])]

    # Time trials don't get excluded in the same way as other levels
    if options.shuffle_time_trial_entrances:
        misc_order += list(valid_misc[misc_index:misc_index+3])
        misc_index += 3
    else:
        misc_order += list(miscellaneous_level_order[1:4])

    if (options.psycho_taxi_unlock_condition.value == options.psycho_taxi_unlock_condition.option_exclude or
            (options.use_separate_entrance_pools and options.psycho_taxi_unlock_condition.value ==
             options.psycho_taxi_unlock_condition.option_vanilla and "Arcade Panik" not in portal_order)):
        misc_order += ["Excluded"]
    elif options.shuffle_psycho_taxi_entrance:
        misc_order += [valid_misc[misc_index]]
    else:
        misc_order += [str(miscellaneous_level_order[4])]

    level_order : List[str] = portal_order + grannys_order + misc_order
    if options.use_separate_entrance_pools:
        return level_order

    valid_levels: List[str] = valid_portals + valid_grannys + valid_misc
    if not options.use_separate_entrance_pools and len(valid_levels) > 0:
        while len(valid_levels) > len(level_order) - level_order.count("Excluded"):
            if remove_worthless_level_from_pool(options, random, valid_levels):
                continue
            break

        # Run randomization until placement passes important tests
        while True:
            random.shuffle(valid_levels)
            # Closed Granny's Island has a very restrictive start. Make sure first portal remedies this somewhat
            if shuffled_portals and not options.open_grannys_island:
                # Don't let 1st portal be Rocket or Psycho Taxi
                if valid_levels[0] in ["Mosk's Rocket", "Psycho Taxi"]:
                    continue
                # If time trials don't have gears, don't let the first level be a time trial
                if not options.time_trial_gears and valid_levels[0].endswith("!"):
                    continue
            break
        valid_level_index : int = 0
        current_level_order : List[str] = []
        if shuffled_portals:
            for i in range(0, len(portal_order)):
                # Don't move goal or excluded levels
                if level_order[i] == "Excluded" or level_order[i] == goal_portal:
                    current_level_order += [level_order[i]]
                    continue
                current_level_order += [valid_levels[valid_level_index]]
                valid_level_index += 1
        else:
            current_level_order += portal_order
        if shuffled_grannys:
            for i in range(0, len(grannys_order)):
                if level_order[i + len(portal_order)] == "Excluded":
                    current_level_order += [level_order[i + len(portal_order)]]
                    continue
                current_level_order += [valid_levels[valid_level_index]]
                valid_level_index += 1
        else:
            current_level_order += grannys_order

        if options.rocket_unlock_condition.value == options.rocket_unlock_condition.option_exclude:
            current_level_order += ["Excluded"]
        elif options.shuffle_rocket_entrance:
            current_level_order += [valid_levels[valid_level_index]]
            valid_level_index += 1
        else:
            current_level_order += ["Mosk's Rocket"]

        if options.shuffle_time_trial_entrances:
            for i in range(0, 3):
                current_level_order += [valid_levels[valid_level_index]]
                valid_level_index += 1
        else:
            current_level_order += list(miscellaneous_level_order[1:4])

        if (options.psycho_taxi_unlock_condition.value == options.psycho_taxi_unlock_condition.option_exclude or
                (options.psycho_taxi_unlock_condition.value == options.psycho_taxi_unlock_condition.option_vanilla
                 and "Arcade Panik" not in current_level_order)):
            current_level_order += ["Excluded"]
        elif options.shuffle_psycho_taxi_entrance:
            current_level_order += [valid_levels[valid_level_index]]
            valid_level_index += 1
        else:
            current_level_order += ["Psycho Taxi"]

        return current_level_order

    return portal_order + grannys_order + misc_order

def remove_worthless_level_from_pool(options: YellowTaxiOptions, random: Random, valid_levels: List[str]) -> bool:
    if "Psycho Taxi" in valid_levels:
        valid_levels.remove("Psycho Taxi")
        return True

    if not options.time_trial_gears:
        tt_levels : List[str] = ["Baby Steps!", "Getting Gud!", "Pro Tricks!"]
        random.shuffle(tt_levels)
        for level in tt_levels:
            if level in valid_levels:
                valid_levels.remove(level)
                return True

    return False

def get_portal_randomization_count_and_pool(options: YellowTaxiOptions, goal_portal: str) -> Tuple[int, List[str]]:
    num_portals : int = 0
    valid_portals : List[str] = []
    past_goal : bool = False
    no_extras_in_pool : bool = (options.allow_shuffling_removed_levels.value ==
                                options.allow_shuffling_removed_levels.option_none)
    goal_portal_index : int = -1
    for portal in original_portal_level_order:
        if portal in unfinished_levels:
            continue
        if portal == goal_portal:
            past_goal = True
            num_portals += 1
            continue

        if past_goal and options.remove_post_goal_portals:
            if no_extras_in_pool:
                break
        else:
            num_portals += 1
        valid_portals += [portal]

    return num_portals, valid_portals
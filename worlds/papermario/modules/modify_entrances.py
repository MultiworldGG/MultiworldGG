from ..data.EntranceList import (
    bowser_shortened_entrances_add,
    bowser_shortened_entrances_rmv,
    bowser_boss_rush_entrances_add,
    bowser_boss_rush_entrances_rmv,
)


def get_entrance_pair(old_data, new_data) -> (int, int):
    old_area, old_map, old_exit = old_data

    new_area, new_map, new_exit = new_data

    key = ((0xA3 << 24) | (old_area << 16) | (old_map << 8) | old_exit)
    value = ((new_area << 16) | (new_map << 8) | new_exit)
    return key, value


def get_entrance_pairs(entrances_to_remove: list, entrances_to_add: list):
    entrance_list = []

    for i in range(0, len(entrances_to_remove)):
        entrance_list.append(
            get_entrance_pair(entrances_to_remove[i], entrances_to_add[i])
        )

    return entrance_list


def get_bowser_rush_pairs():
    return get_entrance_pairs(
        bowser_boss_rush_entrances_rmv,
        bowser_boss_rush_entrances_add,
    )


def get_bowser_shortened_pairs():
    return get_entrance_pairs(
        bowser_shortened_entrances_rmv,
        bowser_shortened_entrances_add,
    )

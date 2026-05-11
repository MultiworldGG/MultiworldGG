### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from random import Random

from ..enums import LevelShuffleMode
from ..names import regionnames
from . import leveldefs as ldef
from . import levelids as lmap


def get_level_shuffle_lists(
        use_dlc: bool,
        mode: LevelShuffleMode,
        shuffle_kingdice: bool
    ) -> list[tuple[list[str],list[str]]]:
    enabled = mode > 0
    separate_plane = mode == LevelShuffleMode.PLANE_SEPARATE

    level_lists: list[tuple[list[str],list[str]]] = []
    if enabled:
        if separate_plane:
            level_lists += [
                (list(ldef.level_boss_regular.keys()), [regionnames.level_boss_kingdice]),
                (list(ldef.level_boss_plane.keys()), []),
                (list(ldef.level_rungun.keys()), []),
            ]
        else:
            level_lists += [
                (list(ldef.level_boss.keys()), [regionnames.level_boss_kingdice]),
                (list(ldef.level_rungun.keys()), []),
            ]

    if shuffle_kingdice:
        level_lists.append((list(ldef.level_dicepalace_boss.keys()), []))

    if enabled and use_dlc:
        level_lists[0][0].extend(ldef.level_dlc_boss_regular.keys() if separate_plane else ldef.level_dlc_boss.keys())
        if separate_plane:
            level_lists[1][0].extend(ldef.level_dlc_boss_plane.keys())
        #level_lists.append((list(ldef.level_dlc_chesscastle_boss.keys()), [regionnames.level_dlc_chesscastle_run]))

    return level_lists

def get_level_shuffle_map(rand: Random, use_dlc: bool, mode: LevelShuffleMode, shuffle_kingdice: bool) -> dict[int,int]:
    level_shuffle_map: dict[int,int] = {}

    # level_lists format: (level_list, exclude_list)
    level_lists = get_level_shuffle_lists(use_dlc, mode, shuffle_kingdice)

    for level_list in level_lists:
        _shuffled_levels = shuffle_levels(rand, level_list[0], level_list[1])
        level_shuffle_map.update(_shuffled_levels)

    return level_shuffle_map

def shuffle_levels(rand: Random, level_list: list[str], level_exclude_list: list[str]) -> dict[int, int]:
    res: dict[int, int] = {}
    _levels = [lmap.level_to_id[x] for x in level_list if (x not in level_exclude_list)]
    _excluded_levels = [lmap.level_to_id[x] for x in level_list if (x in level_exclude_list)]

    levels_shuffled = list(_levels)
    rand.shuffle(levels_shuffled)

    for i in range(len(_levels)):
        res[_levels[i]] = levels_shuffled[i]
    if _excluded_levels:
        res.update({x: x for x in _excluded_levels})

    return res

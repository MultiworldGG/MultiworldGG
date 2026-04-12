from typing import TYPE_CHECKING
from BaseClasses import CollectionState
from ..generic.Rules import add_rule, set_rule

from .Locations import course_locations, Group, shared_hazard_locations, cup_locations
from .Options import Opt, GameMode, ShuffleDriftAbilities
from .Items import item_name_groups

if TYPE_CHECKING:
    from . import MK64World

karts = item_name_groups["Karts"]
qualify_item_score_values = {
    "Triple Red Shell Power": 1,
    "Blue Shell Power":       0.5,
    "Lightning Power":        1,
    "Star Power":             1,
    "Mushroom Power":         0.5,
    "Triple Mushroom Power":  1,
    "Super Mushroom Power":   1
}
win_item_score_values = {
    "Red Shell Power":        0.5,
    "Triple Red Shell Power": 1,
    "Blue Shell Power":       0.5,
    "Lightning Power":        0.5,
    "Star Power":             0.5,
    "Mushroom Power":         0.5,
    "Triple Mushroom Power":  1,
    "Super Mushroom Power":   0.5
}


def item_qualify_score(state: CollectionState, player: int) -> int:  # 0 to 6
    thing1 = [rating if state.has(item, player) else 0 for item, rating in qualify_item_score_values.items()]
    thing2 = [rating if state.has("P2 " + item, player) else 0 for item, rating in qualify_item_score_values.items()]
    sum1 = sum(thing1)
    sum2 = sum(thing2)
    maxsum = max(sum1, sum2)
    return maxsum


def item_win_score(state: CollectionState, player: int) -> int:  # 0 to 5
    return max(sum([rating for item, rating in win_item_score_values.items() if state.has(item, player)]),
               sum([rating for item, rating in win_item_score_values.items() if state.has("P2 " + item, player)]))


def kart_drift_score(state: CollectionState, player: int, opt: Opt, kart: str) -> int:
    match opt.drift:
        case ShuffleDriftAbilities.option_off:
            return 2
        case ShuffleDriftAbilities.option_free_drift:
            return 1 + state.has("Progressive Drift " + kart, player)
        case ShuffleDriftAbilities.option_free_mini_turbo:
            return 2 * state.has("Progressive Drift " + kart, player)
        case _:  # ShuffleDriftAbilities.option_on or ShuffleDriftAbilities.plentiful
            return min(state.count("Progressive Drift " + kart, player), 2)


def track_score(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 2
    return max((kart_drift_score(state, player, opt, kart) for kart in karts if state.has(kart, player)), default=0)


def off_road_score(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 3
    best = 0
    for kart in karts:
        if not state.has(kart, player):
            continue
        if opt.traction:
            current = state.has("Off-Road Tires " + kart, player)
        else:
            current = 1
        current += kart_drift_score(state, player, opt, kart)
        best = max(best, current)
    return best


def winter_score(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 3
    best = 0
    for kart in karts:
        if not state.has(kart, player):
            continue
        if (not opt.traction) or state.has("Winter Tires " + kart, player):
            current = 2
        elif state.has("Off-Road Tires " + kart, player):
            current = 1
        else:
            current = 0
        current += kart_drift_score(state, player, opt, kart)
        best = max(best, current)
    return best


def fence_score(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 8  # TODO: Check for feather item boxes on course
    if not opt.fences:
        return 8
    switch_ratings = [0, 4, 6, 7, 8]
    feather_ratings = [2, 1, 0, 0, 0]
    switch_count = state.count_group_unique("Switches", player)
    return (switch_ratings[switch_count]
            + (state.has_any({"Feather Power", "P2 Feather Power"}, player) and feather_ratings[switch_count]))


def score_track_qualify(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 16
    return fence_score(state, player, opt) + track_score(state, player, opt) + item_qualify_score(state, player)


def score_off_road_qualify(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 17
    return fence_score(state, player, opt) + off_road_score(state, player, opt) + item_qualify_score(state, player)


def score_winter_qualify(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 18
    return fence_score(state, player, opt) + winter_score(state, player, opt) + item_qualify_score(state, player)


def score_track_win(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 15
    return fence_score(state, player, opt) + track_score(state, player, opt) + item_win_score(state, player)


def score_off_road_win(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 16
    return fence_score(state, player, opt) + off_road_score(state, player, opt) + item_win_score(state, player)


def score_winter_win(state: CollectionState, player: int, opt: Opt) -> int:  # 0 to 17
    return fence_score(state, player, opt) + winter_score(state, player, opt) + item_win_score(state, player)


course_qualify_rules = [    # TODO: Refactor with coupling among score types after more play testing & timing
    # lambda:           score threshhold <= fence_score + terrain score + item power score + optional railings score
    lambda state, player, ease, opt: True,                                                            # Luigi Raceway
    lambda state, player, ease, opt: ease - 1 <= score_track_qualify(state, player, opt),                  # Moo Moo Farm
    lambda state, player, ease, opt: ease + 3 <= score_track_qualify(state, player, opt),                  # Koopa Troopa Beach
    lambda state, player, ease, opt: (ease - 1 <= score_off_road_qualify(state, player, opt))              # Kalimari Desert
                                or (state.has("Yellow Switch", player)
                                    and state.has_any({"Star Power", "P2 Star Power"}, player)),
    lambda state, player, ease, opt: ease - 1 <= score_track_qualify(state, player, opt),                  # Toad's Turnpike
    lambda state, player, ease, opt: ease + 4 <= score_winter_qualify(state, player, opt),                 # Frappe Snowland
    lambda state, player, ease, opt: ease + 0 <= score_off_road_qualify(state, player, opt),               # Choco Mountain
    lambda state, player, ease, opt: ease + 0 <= score_off_road_qualify(state, player, opt),               # Mario Raceway
    lambda state, player, ease, opt: ease + 2 <= score_off_road_qualify(state, player, opt),               # Wario Stadium
    lambda state, player, ease, opt: ease + 2 <= score_winter_qualify(state, player, opt),                 # Sherbet Land
    lambda state, player, ease, opt: ease + 3 <= score_off_road_qualify(state, player, opt),               # Royal Raceway
    lambda state, player, ease, opt: ease + 3 <= score_off_road_qualify(state, player, opt),               # Bowser's Castle
    lambda state, player, ease, opt: ease + 2 <= (score_off_road_qualify(state, player, opt)               # D.K.'s Jungle Parkway
                                             + state.has("Railings D.K.'s Jungle Parkway", player)),
    lambda state, player, ease, opt: ease + 5 <= (score_off_road_qualify(state, player, opt)               # Yoshi Valley
                                             + state.has("Railings Yoshi Valley Main Track", player)
                                             + state.has("Railings Yoshi Valley Maze", player)),
    lambda state, player, ease, opt: ease + 3 <= (score_track_qualify(state, player, opt)                  # Banshee Boardwalk
                                             + state.has("Railings Banshee Boardwalk North", player)
                                             + state.has("Railings Banshee Boardwalk South", player)),
    lambda state, player, ease, opt: ease + 4 <= (score_track_qualify(state, player, opt)                  # Rainbow Road
                                             + 2 * state.has("Railings Rainbow Road 1", player)
                                             + 2 * state.has("Railings Rainbow Road 2", player)
                                             + 2 * state.has("Railings Rainbow Road 3", player)
                                             + state.has("Railings Rainbow Road 5", player))
]

course_win_rules = [    # TODO: Refactor with coupling among score types after more play testing & timing
    # lambda:           score threshhold <= fence_score + terrain score + item power score + optional railings score
    lambda state, player, ease, opt: True,                                                            # Luigi Raceway
    lambda state, player, ease, opt: ease + 1 <= score_track_win(state, player, opt),                      # Moo Moo Farm
    lambda state, player, ease, opt: ease + 5 <= score_track_win(state, player, opt),                      # Koopa Troopa Beach
    lambda state, player, ease, opt: (ease + 1 <= score_off_road_win(state, player, opt))                  # Kalimari Desert
                                or (state.has("Yellow Switch", player)
                                    and state.has_any({"Star Power", "P2 Star Power"}, player)),
    lambda state, player, ease, opt: ease + 1 <= score_track_win(state, player, opt),                      # Toad's Turnpike
    lambda state, player, ease, opt: ease + 6 <= score_winter_win(state, player, opt),                     # Frappe Snowland
    lambda state, player, ease, opt: ease + 3 <= score_off_road_win(state, player, opt),                   # Choco Mountain
    lambda state, player, ease, opt: ease + 3 <= score_off_road_win(state, player, opt),                   # Mario Raceway
    lambda state, player, ease, opt: ease + 4 <= score_off_road_win(state, player, opt),                   # Wario Stadium
    lambda state, player, ease, opt: ease + 4 <= score_winter_win(state, player, opt),                     # Sherbet Land
    lambda state, player, ease, opt: ease + 5 <= score_off_road_win(state, player, opt),                   # Royal Raceway
    lambda state, player, ease, opt: ease + 5 <= score_off_road_win(state, player, opt),                   # Bowser's Castle
    lambda state, player, ease, opt: ease + 4 <= (score_off_road_win(state, player, opt)                   # D.K.'s Jungle Parkway
                                             + state.has("Railings D.K.'s Jungle Parkway", player)),
    lambda state, player, ease, opt: ease + 7 <= (score_off_road_win(state, player, opt)                   # Yoshi Valley
                                             + state.has("Railings Yoshi Valley Main Track", player)
                                             + state.has("Railings Yoshi Valley Maze", player)),
    lambda state, player, ease, opt: ease + 5 <= (score_track_win(state, player, opt)                      # Banshee Boardwalk
                                             + state.has("Railings Banshee Boardwalk North", player)
                                             + state.has("Railings Banshee Boardwalk South", player)),
    lambda state, player, ease, opt: ease + 6 <= (score_track_win(state, player, opt)                      # Rainbow Road
                                             + 2 * state.has("Railings Rainbow Road 1", player)
                                             + 2 * state.has("Railings Rainbow Road 2", player)
                                             + 2 * state.has("Railings Rainbow Road 3", player)
                                             + state.has("Railings Rainbow Road 5", player))
]


def can_win_trophy(state: CollectionState, player: int,
                   courses: frozenset[int], trophy_class: int, ease: int, opt: Opt) -> bool:
    return trophy_class <= sum(course_win_rules[course](state, player, ease, opt) for course in courses)


def set_star_access_rule(world: "MK64World", loc_name: str, player: int, opt: Opt) -> None:
    # Relevant Option
    if opt.two_player:
        set_rule(world.get_location(loc_name),
                 lambda state: state.has_any({"Star Power", "P2 Star Power"}, player))
    else:
        set_rule(world.get_location(loc_name), lambda state: state.has("Star Power", player))


def create_rules(world: "MK64World") -> None:
    multiworld = world.multiworld
    player = world.player
    opt = world.opt
    order = world.course_order

    # Make starting kart(s) required, which has them show up in the spoiler log Playthrough.
    if opt.mode == GameMode.option_cups:
        first_entrance = world.multiworld.get_region("Menu", player).get_exits()[0]
        if len(world.starting_karts) == 1:
            first_entrance.access_rule = lambda state, kart=world.starting_karts[0]: state.has(kart, player)
        else:
            first_entrance.access_rule = lambda state, kts=frozenset(world.starting_karts): state.has_all(kts, player)

    # Region (Entrance) Rules (handled in Regions.py instead for now)
    # if opt_game_mode == GameMode.option_cups:
    #    set_rule(multiworld.get_entrance("Flower Cup 1", player),
    #             lambda state: state.has("Progressive Cup Unlock", player, 1))
    #     set_rule(multiworld.get_entrance("Star Cup 1", player),
    #              lambda state: state.has("Progressive Cup Unlock", player, 2))
    #     set_rule(multiworld.get_entrance("Special Cup 1", player),
    #              lambda state: state.has("Progressive Cup Unlock", player, 3))
    # elif opt_game_mode == GameMode.option_courses:
    #     pass

    # Base Course Rules # TODO: Clean this up, probably combine with Star Access Rules section
    for locations in course_locations.values():
        for name, (code, group) in locations.items():
            if group == Group.base:
                if code % 3 < 2:
                    set_rule(world.get_location(name),
                             lambda state, c=code: course_win_rules[(c - 4660000) // 3](state, player, opt.logic, opt))
                else:
                    set_rule(world.get_location(name),
                             lambda state, c=code: course_qualify_rules[(c - 4660000) // 3](state, player, opt.logic, opt))

    # Item Spot Access Rules moved to Regions.py for context that knows which item box spots to apply rules to

    # Koopa Troopa Beach Rock Access
    if opt.special_boxes and opt.fences:
        set_rule(world.get_location("Koopa Troopa Beach Rock"),
                 lambda state: state.has_all({"Yellow Switch", "Blue Switch"}, player)
                               or state.has_all({"Red Switch", "Green Switch"}, player))

    if opt.secrets and opt.fences:
        # Kalimari Desert Secret Access
        set_rule(world.get_location("Kalimari Desert Secret"),
                 lambda state: state.has_any({"Yellow Switch", "Red Switch", "Blue Switch",
                                              "Feather Power", "P2 Feather Power"}, player))

        # Marty's Secret Access
        set_rule(world.get_location("Marty's Secret"),
                 lambda state: state.has_any({"Green Switch", "Feather Power", "P2 Feather Power"}, player))

    # Hazard Access, all use Star Power
    if opt.hazards:
        for locations in course_locations.values():
            for name, (_, group) in locations.items():
                if group == Group.hazard:
                    set_star_access_rule(world, name, player, opt)
        for name, _ in shared_hazard_locations.items():
            set_star_access_rule(world, name, player, opt)

        # Add Blue Fence rule to Mario sign
        if opt.fences:
            add_rule(world.get_location("Destroy Mario Sign"), lambda state: state.has("Blue Switch", player))

    # Cup Trophy Rules
    cup_courses = [frozenset(order[i:i + 4]) for i in range(0, len(order), 4)]
    if opt.mode == GameMode.option_cups:
        trophy_class_mapping = {"Bronze": 1, "Silver": 2, "Gold": 3}
        engine_class_mapping = {"100cc": 2, "150cc": 3}  # 50cc is 0
        for locations, courses in zip(cup_locations.values(), cup_courses):
            for loc_name in locations.keys():
                difficulty, trophy = loc_name.rsplit(" ", 2)[-2:]
                trophy_class = trophy_class_mapping[trophy]
                ease = opt.logic + engine_class_mapping.get(difficulty, 0)
                set_rule(world.get_location(loc_name),
                         lambda state, c=courses, t=trophy_class, e=ease: can_win_trophy(state, player, c, t, e, opt))

    # Completion Condition (Victory Rule)
    multiworld.completion_condition[player] = lambda state: state.has("Victory", player)

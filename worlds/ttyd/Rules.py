import json
import pkgutil
import typing

from worlds.generic.Rules import add_rule, add_item_rule, forbid_items_for_player
from . import StateLogic, location_table, EnemyRandomizer
from .Boss import parse_json_bosses
from .Options import Goal, PitItems, BossRandomizer
from .Data import stars, pit_exclusive_tattle_stars_required, location_to_unit, dazzle_location_names, dazzle_counts
from .Locations import get_location_ids, get_locations_by_tags, location_id_to_name
from .Options import PalaceSkip

if typing.TYPE_CHECKING:
    from . import TTYDWorld


def set_rules(world: "TTYDWorld"):
    for location, rule in create_lambda_from_json(pkgutil.get_data(__name__, "json/rules.json").decode(), world).items():
        if location not in world.disabled_locations:
            if location == "Glitzville Promoter's Office: Jolene's Trouble Reward" and not world.options.troublesanity:
                add_rule(world.multiworld.get_location(location, world.player), lambda state: state.has("Battle Trunks", world.player, 20))
                continue
            add_rule(world.multiworld.get_location(location, world.player), rule)

    for location in ["Palace of Shadow Final Staircase: Ultra Shroom", "Palace of Shadow Final Staircase: Jammin' Jelly"]:
        if location not in world.disabled_locations:
            add_rule(world.multiworld.get_location(location, world.player), lambda state: state.has("stars", world.player, world.options.goal_stars))

    for location in get_locations_by_tags("shop"):
        if location.name in world.disabled_locations:
            continue
        forbid_items_for_player(world.get_location(location.name), set([item for item in stars.values()]), world.player)

    for location in get_locations_by_tags("dazzle"):
        if location.name in world.disabled_locations:
            continue
        forbid_items_for_player(world.get_location(location.name), {"Star Piece"}, world.player)

    available_pieces = len(get_locations_by_tags(["star_piece", "panel"])) - world.unavailable_star_pieces
    for i, location_name in enumerate(dazzle_location_names):
        if location_name in world.disabled_locations:
            continue
        if dazzle_counts[i] > available_pieces // 2:
            add_item_rule(world.get_location(location_name), lambda item: not item.advancement)

    if world.limited_chapters:
        limited_gate_tags = [f"chapter_{chapter}" for chapter in world.limited_chapters]
        for location in get_locations_by_tags(limited_gate_tags):
            if location.name in world.disabled_locations:
                continue
            forbid_items_for_player(world.get_location(location.name), {"Star Piece"}, world.player)

def set_tattle_rules(world: "TTYDWorld"):
    for location in get_locations_by_tags("tattle"):
        if location.name in world.disabled_locations:
            continue
        add_rule(world.get_location(location.name), lambda state: state.has("Goombella", world.player))
    rules_dict = get_random_enemy_tattle_rules_dict(world) \
        if world.options.enemy_randomizer != EnemyRandomizer.option_vanilla \
        or world.options.boss_randomizer != BossRandomizer.option_vanilla \
        else get_tattle_rules_dict()
    for location_name, locations in rules_dict.items():
        if location_name in world.disabled_locations:
            continue
        if len(locations) == 0:
            # Require access to Shadow Queen
            if world.options.palace_skip == PalaceSkip.option_true and world.options.goal != Goal.option_shadow_queen:
                extra_condition = lambda state: state.has("stars", world.player, world.options.palace_stars)
            elif world.options.goal == Goal.option_shadow_queen:
                extra_condition = lambda state: state.can_reach("Shadow Queen", "Location", world.player)
            else:
                extra_condition = lambda state: state.can_reach("Palace of Shadow Final Staircase: Ultra Shroom", "Location", world.player)
        else:
            locations = [loc for loc in locations if location_id_to_name[loc] not in world.disabled_locations]
            if len(locations) == 0:
                continue
            pit_exclusive_names = {name for names in pit_exclusive_tattle_stars_required.values() for name in names}
            if world.options.pit_items != PitItems.option_all and location_name not in pit_exclusive_names:
                non_pit = [loc for loc in locations if loc not in get_location_ids(get_locations_by_tags("pit_floor"))]
                if non_pit:
                    locations = non_pit
            valid_locations = [location_id_to_name[loc] for loc in locations]
            extra_condition = lambda state, locs=valid_locations: any(
                state.can_reach(loc, "Location", world.player) for loc in locs
            )

        add_rule(world.get_location(location_name), extra_condition)


def create_lambda_from_json(json_string: str, world: "TTYDWorld") -> typing.Dict[str, typing.Callable]:
    lambda_functions = {}
    for location, requirements in json.loads(json_string).items():
        lambda_functions[location] = _build_single_lambda(requirements, world)
    return lambda_functions


def _build_single_lambda(req: typing.Dict, world: "TTYDWorld") -> typing.Callable:
    def build_expression(r):
        if "or" in r:
            conditions = [build_expression(condition) for condition in r["or"]]
            return f"({' or '.join(conditions)})"
        elif "and" in r:
            conditions = [build_expression(condition) for condition in r["and"]]
            return f"({' and '.join(conditions)})"
        elif "has" in r:
            has_value = r["has"]

            if isinstance(has_value, str):
                item = has_value
                count = r.get("count", 1)
            elif isinstance(has_value, dict):
                item = has_value.get("item", "")
                count = has_value.get("count", 1)
            else:
                item = str(has_value)
                count = r.get("count", 1)

            # Escape quotes in item names by using repr() which handles escaping properly
            escaped_item = repr(item)

            if count == 1:
                return f'state.has({escaped_item}, world.player)'
            else:
                return f'state.has({escaped_item}, world.player, {count})'
        elif "function" in r:
            fn = r["function"]
            if isinstance(fn, dict):
                function_name = fn.get("name", "")
                count = fn.get("count", None)
            else:
                function_name = fn
                count = None

            # Require count for chapter_completions (and validate it)
            if function_name == "chapter_completions":
                if count is None:
                    raise ValueError("chapter_completions requires 'count'")
                count = int(count)
                if count <= 0:
                    raise ValueError(f"chapter_completions count must be > 0, got {count}")
                return f"StateLogic.{function_name}(state, world.player, {count})"

            # For other functions, only pass count if provided
            if count is not None:
                return f"StateLogic.{function_name}(state, world.player, {int(count)})"
            return f"StateLogic.{function_name}(state, world.player)"

        elif "can_reach" in r:
            location = r["can_reach"]
            return f'state.can_reach({repr(location)}, "Location", world.player)'

        else:
            return "False"

    expression = build_expression(req)
    # Capture world and StateLogic in the lambda's closure
    return eval(f"lambda state: {expression}", {"world": world, "StateLogic": StateLogic})


def get_tattle_rules_dict() -> dict[str, typing.List[int]]:
    return {
        "Tattle: Goomba": [78780047],
        "Tattle: Paragoomba": [78780047],
        "Tattle: Spiky Goomba": [78780047],
        "Tattle: Spinia": [78780047],
        "Tattle: Spania": [78780145, 78780267, 78780638],
        "Tattle: Fuzzy": [78780170, 78780296, 78780638],
        "Tattle: Koopa Troopa": [78780193, 78780170],
        # Proxy is the sewers-side Shine Sprite in the pipe room (the fight is on the
        # sewers side); piece locations make bad proxies — they get DISABLED under
        # limited chapters, which would remove the tattle entirely.
        "Tattle: Blooper": [78780133],
        "Tattle: Lord Crump": [78780511],
        "Tattle: Cleft": [78780216, 78780639],
        "Tattle: Bald Cleft": [78780165],
        "Tattle: Bristle": [78780800, 78780296],
        "Tattle: Gold Fuzzy": [78780170],
        "Tattle: Paratroopa": [78780193],
        "Tattle: Dull Bones": [78780193, 78780267, 78780615, 78780638],
        "Tattle: Red Bones": [78780193, 78780615],
        "Tattle: Hooktail": [78780209],
        "Tattle: Pale Piranha": [78780216, 78780267],
        "Tattle: Dark Puff": [78780216, 78780267, 78780639],
        "Tattle: Vivian": [78780215],
        "Tattle: Marilyn": [78780215, 78780622],
        "Tattle: Beldam": [78780215, 78780622],
        "Tattle: X-Naut": [78780231, 78780595],
        "Tattle: Yux": [78780231],
        "Tattle: Mini-Yux": [78780231],
        "Tattle: Pider": [78780241, 78780267, 78780639],
        "Tattle: Magnus von Grapple": [78780232],
        "Tattle: KP Koopa": [78780267],
        "Tattle: KP Paratroopa": [78780267],
        "Tattle: Pokey": [78780267, 78780639],
        "Tattle: Spiny": [78780267, 78780640],
        "Tattle: Lakitu": [78780267, 78780640],
        "Tattle: Bandit": [78780267, 78780640],
        "Tattle: Big Bandit": [78780267],
        "Tattle: Hyper Bald Cleft": [78780267],
        "Tattle: Bob-omb": [78780267, 78780640],
        "Tattle: Swooper": [78780287, 78780436],
        "Tattle: Iron Cleft": [78780267],
        "Tattle: Red Spike Top": [78780296],
        "Tattle: Shady Koopa": [78780296, 78780641],
        "Tattle: Shady Paratroopa": [78780296],
        "Tattle: Green Fuzzy": [78780296, 78780470],
        "Tattle: Flower Fuzzy": [78780296, 78780470],
        "Tattle: Magikoopa": [78780511],
        "Tattle: Red Magikoopa": [78780296],
        "Tattle: White Magikoopa": [78780296],
        "Tattle: Green Magikoopa": [78780296],
        "Tattle: Hammer Bro": [78780296, 78780511],
        "Tattle: Boomerang Bro": [78780296],
        "Tattle: Fire Bro": [78780296],
        "Tattle: Dark Craw": [78780296, 78780644],
        "Tattle: Red Chomp": [78780296, 78780643],
        "Tattle: Koopatrol": [78780511],
        "Tattle: Dark Koopatrol": [78780296, 78780645],
        "Tattle: Rawk Hawk": [78780295],
        "Tattle: Macho Grubba": [78780287],
        "Tattle: Hyper Goomba": [78780319],
        "Tattle: Hyper Paragoomba": [78780319],
        "Tattle: Crazee Dayzee": [78780327],
        "Tattle: Hyper Spiky Goomba": [78780319],
        "Tattle: Amazy Dayzee": [78780327],
        "Tattle: Hyper Cleft": [78780329, 78780641],
        "Tattle: Buzzy Beetle": [78780450],
        "Tattle: Spike Top": [78780450],
        "Tattle: Atomic Boo": [78780434],
        "Tattle: Boo": [78780434],
        "Tattle: Doopliss": [78780437, 78780622],
        "Tattle: Ember": [78780503],
        "Tattle: Putrid Piranha": [78780470],
        "Tattle: Lava Bubble": [78780495, 78780642],
        "Tattle: Bullet Bill": [78780495],
        "Tattle: Bill Blaster": [78780495],
        "Tattle: Bulky Bob-omb": [78780495, 78780642],
        "Tattle: Parabuzzy": [78780503],
        "Tattle: Cortez": [78780511],
        "Tattle: Smorg": [78780554],
        "Tattle: Ruff Puff": [78780539],
        "Tattle: Poison Pokey": [78780541, 78780642],
        "Tattle: Spiky Parabuzzy": [78780543, 78780642],
        "Tattle: Ice Puff": [78780562, 78780643],
        "Tattle: Frost Piranha": [78780562, 78780644],
        "Tattle: Moon Cleft": [78780579, 78780643],
        "Tattle: Z-Yux": [78780579],
        "Tattle: Mini-Z-Yux": [78780579],
        "Tattle: Elite X-Naut": [78780584],
        "Tattle: X-Yux": [78780595],
        "Tattle: Mini-X-Yux": [78780595],
        "Tattle: X-Naut PhD": [78780595],
        "Tattle: Magnus von Grapple 2.0": [78780604],
        "Tattle: Spunia": [78780646, 78780156],
        "Tattle: Swoopula": [78780605, 78780645],
        "Tattle: Dry Bones": [78780605, 78780644],
        "Tattle: Bombshell Bill": [78780605, 78780609],
        "Tattle: B. Bill Blaster": [78780605, 78780609],
        "Tattle: Phantom Ember": [78780634, 78780645],
        "Tattle: Dark Bones": [78780609],
        "Tattle: Chain-Chomp": [78780634, 78780645],
        "Tattle: Dark Wizzerd": [78780634, 78780644],
        "Tattle: Gloomtail": [78780634],
        "Tattle: Sir Grodus": [],
        "Tattle: Grodus X": [],
        "Tattle: Kammy Koopa": [],
        "Tattle: Bowser": [],
        "Tattle: Shadow Queen": [],
        "Tattle: Gloomba": [78780638],
        "Tattle: Paragloomba": [78780639],
        "Tattle: Spiky Gloomba": [78780640],
        "Tattle: Dark Koopa": [78780641],
        "Tattle: Dark Paratroopa": [78780642],
        "Tattle: Badge Bandit": [78780643],
        "Tattle: Dark Boo": [78780643],
        "Tattle: Dark Lakitu": [78780644],
        "Tattle: Sky-Blue Spiny": [78780644],
        "Tattle: Wizzerd": [78780645],
        "Tattle: Piranha Plant": [78780646],
        "Tattle: Dark Bristle": [78780646],
        "Tattle: Arantula": [78780646],
        "Tattle: Elite Wizzerd": [78780647],
        "Tattle: Swampire": [78780647],
        "Tattle: Poison Puff": [78780647],
        "Tattle: Bob-ulk": [78780647],
        "Tattle: Bonetail": [78780647]
    }

BOSS_ARENA_INFO: dict[str, tuple[typing.Optional[int], list[str]]] = {
    "btlgrp_aji_aji_mbmkII":           (78780604, ["Tattle: Magnus von Grapple 2.0"]),
    "btlgrp_gon_gon_11_01_off_1":      (78780209, ["Tattle: Hooktail"]),
    "btlgrp_gor_gor_00_01_off_1":      (78780000, ["Tattle: Lord Crump"]),
    "btlgrp_gor_gor_02_01_off_1":      (78780047, ["Tattle: Gus"]),
    "btlgrp_hei_hei_10_01_off_1":      (78780170, ["Tattle: Gold Fuzzy"]),
    "btlgrp_jin_jin_00_atmic_teresa":  (78780434, ["Tattle: Atomic Boo"]),
    "btlgrp_jin_jin_01_faker_mario":   (78780437, ["Tattle: Doopliss"]),
    "btlgrp_jin_jin_04_ramper":        (78780437, ["Tattle: Doopliss"]),
    "btlgrp_jon_jon_100_01_off_1":     (78780647, ["Tattle: Bonetail"]),
    "btlgrp_las_las_09_rampell":       (78780622, ["Tattle: Doopliss", "Tattle: Beldam", "Tattle: Marilyn"]),
    "btlgrp_las_las_bunbaba":          (78780634, ["Tattle: Gloomtail"]),
    "btlgrp_las_las_28_koopa":         (78780634, ["Tattle: Bowser", "Tattle: Kammy Koopa"]),
    "btlgrp_las_las_28_batten_leader": (78780634, ["Tattle: Sir Grodus", "Tattle: Grodus X"]),
    "btlgrp_las_las_29_black_peach_1": (None, ["Tattle: Shadow Queen"]),
    "btlgrp_las_las_29_black_peach_2": (None, ["Tattle: Shadow Queen", "Tattle: Beldam", "Tattle: Marilyn",
                                               "Tattle: Vivian"]),
    "btlgrp_mri_mri_mb":               (78780232, ["Tattle: Magnus von Grapple"]),
    "btlgrp_muj_muj_kanbu":            (78780511, ["Tattle: Lord Crump", "Tattle: Koopatrol", "Tattle: Magikoopa"]),
    "btlgrp_muj_muj_cortez":           (78780511, ["Tattle: Cortez"]),
    "btlgrp_rsh_rsh_06_01_off_1":      (78780554, ["Tattle: Smorg"]),
    "btlgrp_tik_tik_gesso":            (78780133, ["Tattle: Blooper"]),
    "btlgrp_tou_tou_boss":             (78780287, ["Tattle: Macho Grubba"]),
    "btlgrp_tou_tou_champ":            (78780295, ["Tattle: Rawk Hawk"]),
    "btlgrp_tou_tou_koopa":            (78780287, ["Tattle: Bowser"]),
    "btlgrp_win_win_00_04_off_1":      (78780215, ["Tattle: Vivian", "Tattle: Beldam", "Tattle: Marilyn"]),
}


def get_random_enemy_tattle_rules_dict(world: "TTYDWorld") -> dict[str, list[int]]:
    base_rules = get_tattle_rules_dict()

    enemy_random = world.options.enemy_randomizer != EnemyRandomizer.option_vanilla
    boss_random = world.options.boss_randomizer != BossRandomizer.option_vanilla

    encounter_enemy_sets = [
        (enc.location_id, set(enc.enemy_ids))
        for enc in world.encounters
    ] if enemy_random else []

    boss_overrides: dict[str, list[int]] = {}
    boss_keys: set[str] = set()
    if boss_random:
        for _, arena_keys in BOSS_ARENA_INFO.values():
            boss_keys.update(arena_keys)
        group_source = {tuple(sorted(b.enemy_ids)): b.name for b in parse_json_bosses()}
        for arena in world.bosses:
            source_name = group_source.get(tuple(sorted(arena.enemy_ids)))
            if source_name is None:
                continue
            arena_proxy = BOSS_ARENA_INFO[arena.name][0]
            for key in BOSS_ARENA_INFO[source_name][1]:
                boss_overrides.setdefault(key, [])
                if arena_proxy is not None:
                    boss_overrides[key].append(arena_proxy)

    result: dict[str, list[int]] = {}

    for key in base_rules:
        tattle_ids = set(location_to_unit[location_table[key]])
        is_boss = key in boss_keys

        if is_boss:
            matching_locations = [
                loc_id
                for loc_id, enemy_set in encounter_enemy_sets
                if enemy_set & tattle_ids
            ]
            matching_locations += boss_overrides.get(key, [])
            result[key] = list(dict.fromkeys(matching_locations))
        elif enemy_random:
            matching_locations = [
                loc_id
                for loc_id, enemy_set in encounter_enemy_sets
                if enemy_set & tattle_ids
            ]
            # fallback to base rule if random finds nothing
            result[key] = matching_locations if matching_locations else list(base_rules[key])
        else:
            result[key] = list(base_rules[key])

        if key == "Tattle: Mini-Yux":
            result[key] = result["Tattle: Yux"]
        elif key == "Tattle: Mini-Z-Yux":
            result[key] = result["Tattle: Z-Yux"]
        elif key == "Tattle: Mini-X-Yux":
            result[key] = result["Tattle: X-Yux"]
        elif key == "Tattle: Sky-Blue Spiny":
            result[key] = result["Tattle: Dark Lakitu"]

    return result


import json
import pkgutil
import typing

from worlds.generic.Rules import add_rule, forbid_items_for_player
from . import StateLogic, location_table, EnemyRandomizer
from .Options import Goal, PitItems
from .Data import stars, pit_exclusive_tattle_stars_required, location_to_unit
from .Locations import get_location_ids, get_locations_by_tags, location_id_to_name
from .Options import PalaceSkip

if typing.TYPE_CHECKING:
    from . import TTYDWorld


def set_rules(world: "TTYDWorld"):
    for location, rule in create_lambda_from_json(pkgutil.get_data(__name__, "json/rules.json").decode(), world).items():
        if location not in world.disabled_locations:
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

def set_tattle_rules(world: "TTYDWorld"):
    for location in get_locations_by_tags("tattle"):
        if location.name in world.disabled_locations:
            continue
        add_rule(world.get_location(location.name), lambda state: state.has("Goombella", world.player))
    rules_dict = get_random_enemy_tattle_rules_dict(world) \
        if world.options.enemy_randomizer != EnemyRandomizer.option_vanilla \
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
            # Require access to any of the listed locations
            if world.options.pit_items != PitItems.option_all and location_name not in pit_exclusive_tattle_stars_required:
                locations = [loc for loc in locations if loc not in get_location_ids(get_locations_by_tags("pit_floor"))]
                if len(locations) == 0:
                    continue
            valid_locations = [
                location_id_to_name[loc] for loc in locations
                if location_id_to_name[loc] not in world.disabled_locations
            ]
            if len(valid_locations) == 0:
                continue
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
        "Tattle: Spania": [78780145, 78780267, 78780638],
        "Tattle: Fuzzy": [78780170, 78780296, 78780638],
        "Tattle: Koopa Troopa": [78780193, 78780170],
        "Tattle: Blooper": [78780184],
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
        "Tattle: Bullet Bill": [78780497],
        "Tattle: Bill Blaster": [78780497],
        "Tattle: Bulky Bob-omb": [78780497, 78780642],
        "Tattle: Parabuzzy": [78780503],
        "Tattle: Cortez": [78780511],
        "Tattle: Smorg": [78780554],
        "Tattle: Ruff Puff": [78780538],
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

def get_random_enemy_tattle_rules_dict(world: "TTYDWorld") -> dict[str, list[int]]:
    base_rules = get_tattle_rules_dict()

    encounter_enemy_sets = [
        (enc.location_id, set(enc.enemy_ids))
        for enc in world.encounters
    ]

    result: dict[str, list[int]] = {}

    for key in base_rules:
        tattle_ids = set(location_to_unit[location_table[key]])  # <-- FIX

        matching_locations = [
            loc_id
            for loc_id, enemy_set in encounter_enemy_sets
            if enemy_set & tattle_ids
        ]

        # fallback to base rule if random finds nothing
        result[key] = matching_locations if matching_locations else list(base_rules[key])

    return result


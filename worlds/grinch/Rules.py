from types import MappingProxyType
from typing import Callable

from BaseClasses import CollectionState
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from .Items import grinch_items


# Adds all rules from access_rules_dict to locations
def set_location_rules(world: World):
    all_locations = world.get_locations()
    for location in all_locations:
        loc_rules = rules_dict[location.name]
        rule_list = interpret_rule(loc_rules, world.player)
        for access_rule in rule_list:
            if rule_list.index(access_rule) == 0:
                add_rule(location, access_rule)
            else:
                add_rule(location, access_rule, "or")


def interpret_rule(
    rule_set: list[list[str]],
    player: int,
):
    # If a region/location does not have any items required, make the section(s) return no logic.
    if rule_set is None or len(rule_set) < 1:
        return []

    # Otherwise, if a region/location DOES have items required, make the section(s) return list of logic.
    access_list: list[Callable[[CollectionState], bool]] = []

    for item_set in rule_set:
        item_names_and_count: dict[str, int] = {}
        for item_name in item_set:
            if ":" in item_name:
                item_count: int = int(item_name.split(":")[0])
                req_item_name: str = str(item_name.split(":")[1])
                item_names_and_count[req_item_name] = item_count
            else:
                item_names_and_count[item_name] = 1
        access_list.append(
            lambda state, items=MappingProxyType(item_names_and_count): state.has_all_counts(items, player))

    return access_list

# Each item in the list is a separate list of rules. Each separate list is just an "OR" condition.
# NOTE: Locations will never be in logic if any of these are true ingame:
# - You can get softlocked in an area and would require restarting
# - You have a chance to get teleported back to the start by doing this
# - You take damage to brute force through certain areas
# - You waste a lot of Rotten Eggs when there are intentional game design alternatives not to.
# Example being guessing bell order in Countdown to Xmas Clock. Skipping areas via GC does not count.
# - Sections where you are camera locked in an area and have to perform precise jumps to get around it.
# Example using Pancake on Mole in North Shore up to the drill house
# - Locations that might just barely be enough in reach to jump towards without moving a boulder
# Example being WL - South Shore - MM BP on Grass Platform

access_rules_dict: dict[str, list[list[str]]] = {
    "Whoville": [
        [
            grinch_items.keys.WHOVILLE,
        ],
        [
            "1:"+grinch_items.keys.PROGRESSIVE_VACUUM_TUBE
        ],
    ],
    "Post Office": [
        [
            grinch_items.level_items.WV_WHO_CLOAK,
        ],
    ],
    "City Hall": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "Clock Tower": [
        [
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.level_items.WV_WHO_CLOAK,
        ],
    ],
    "Who Forest": [
        [
            grinch_items.keys.WHO_FOREST,
        ],
        [
            "2:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE
        ],
    ],
    "Ski Resort": [
        [
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
        ],
    ],
    "Civic Center": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
    ],
    "Who Dump": [
        [
            grinch_items.keys.WHO_DUMP,
        ],
        [
            "3:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE
        ],
    ],
    "Minefield": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "Power Plant": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "Generator Building": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "Who Lake": [
        [
            grinch_items.keys.WHO_LAKE,
        ],
        [
            "4:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE
        ],
    ],
    "Scout's Hut": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
    ],
    "North Shore": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.SNEAK,
        ],
    ],
    "Mayor's Villa": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
        ],
    ],
    "Submarine World": [
        [
            grinch_items.gadgets.MARINE_MOBILE,
        ]
    ],
    "Sleigh Room": [
        [
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ]
    ],
    "Sleigh Ride": [
        [
        grinch_items.sleigh_parts.EXHAUST_PIPES,
        grinch_items.sleigh_parts.TWIN_END_TUBA,
        grinch_items.sleigh_parts.SKIS,
        grinch_items.sleigh_parts.TIRES,
        # grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        # grinch_items.keys.WHOVILLE,
        # grinch_items.keys.WHO_FOREST,
        # grinch_items.keys.WHO_DUMP,
        # grinch_items.keys.WHO_LAKE,
        # grinch_items.gadgets.ROCKET_SPRING,
        # grinch_items.gadgets.MARINE_MOBILE,
        # grinch_items.moves.MAX,
        # grinch_items.moves.SEIZE,
        # grinch_items.moves.PANCAKE,
        # ],
        # [
        # grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        # "4:"+grinch_items.keys.PROGRESSIVE_VACUUM_TUBE,
        # grinch_items.gadgets.ROCKET_SPRING,
        # grinch_items.gadgets.MARINE_MOBILE,
        # grinch_items.moves.MAX,
        # grinch_items.moves.SEIZE,
        # grinch_items.moves.PANCAKE,
        # ]
        ],
    ],
    "Spin N' Win": [[]],
    "Dankamania": [[]],
    "The Copter Race Contest": [[]],
    "Bike Race": [[]],
}


rules_dict: dict[str, list[list[str]]] = {
    # Rules applied to regions first via the access_list, so "First Visit" checks should ALWAYS be empty
    # First Visit Checks (ALWAYS empty)
    "WV - First Visit": [[]],
    "WV - Post Office - First Visit": [[]],
    "WV - City Hall - First Visit": [[]],
    "WV - Clock Tower - First Visit": [[]],
    "WF - First Visit": [[]],
    "WF - Ski Resort - First Visit": [[]],
    "WF - Civic Center - First Visit": [[]],
    "WD - First Visit": [[]],
    "WD - Minefield - First Visit": [[]],
    "WD - Power Plant - First Visit": [[]],
    "WD - Generator Building - First Visit": [[]],
    "WL - South Shore - First Visit": [[]],
    "WL - Submarine World - First Visit": [[]],
    "WL - Scout's Hut - First Visit": [[]],
    "WL - North Shore - First Visit": [[]],
    "WL - Mayor's Villa - First Visit": [[]],
    # Whoville Missions
    "WV - Post Office - Shuffling The Mail": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WV - Smashing Snowmen": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Painting The Mayor's Posters": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Launching Eggs Into Houses": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - City Hall - Modifying The Mayor's Statue": [
        [
            grinch_items.level_items.WV_SCULPTING_TOOLS,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.level_items.WV_SCULPTING_TOOLS,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.level_items.WV_SCULPTING_TOOLS,
            grinch_items.gadgets.GRINCH_COPTER,
        ]
    ],
    "WV - Clock Tower - Advancing The Countdown-To-Xmas Clock": [
        [
            grinch_items.level_items.WV_HAMMER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.level_items.WV_HAMMER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WV - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.level_items.WV_WHO_CLOAK,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
        ],
        [
            "advanced_logic"

        ]
    ],
    # Who Forest Missions
    "WF - Making Xmas Trees Droop": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ]
    ],
    "WF - Sabotaging Snow Cannon With Glue": [
        [
            grinch_items.level_items.WF_GLUE_BUCKET,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.level_items.WF_GLUE_BUCKET,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Putting Beehives In Cabins": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Ski Resort - Sliming The Mayor's Skis": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.MAX,
        ]
    ],
    "WF - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.PANCAKE,
        ],
    ],
    # Who Dump Missions
    "WD - Stealing Food From Birds": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ]
    ],
    "WD - Feeding The Computer With Robot Parts": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ]
    ],
    "WD - Infesting The Mayor's House With Rats": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ]
    ],
    "WD - Minefield - Shaving Who Dump Guardian": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.level_items.WD_SCISSORS,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
            grinch_items.level_items.WD_SCISSORS,
        ],
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    # Who Lake Missions
    "WL - South Shore - Putting Thistles In Shorts": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,

        ],
    ],
    "WL - South Shore - Sabotaging The Tents": [
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes": [
        [
            grinch_items.level_items.WL_DRILL,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
        ],
    ],
    "WL - Submarine World - Modifying The Marine Mobile": [[]],
    "WL - Mayor's Villa - Hooking The Mayor's Bed To The Motorboat": [
        [
            grinch_items.level_items.WL_ROPE,
            grinch_items.level_items.WL_HOOK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - Squashing All Gifts": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    # Whoville Blueprints
    "WV - Binoculars BP on Post Office Roof": [[]],
    "WV - City Hall - Binoculars BP left side of Library": [
        [
            grinch_items.moves.SEIZE,
        ],
    ],
    "WV - City Hall - Binoculars BP front side of Library": [
        [
            grinch_items.moves.SEIZE,
        ],
    ],
    "WV - City Hall - Binoculars BP right side of Library": [
        [
            grinch_items.moves.SEIZE,
        ],
    ],
    "WV - REL BP left of City Hall": [[]],
    "WV - REL BP left of Clock Tower": [[]],
    "WV - Post Office - REL BP inside Gray Room": [
        [
            grinch_items.moves.MAX
        ],
    ],
    "WV - Post Office - REL BP at Entrance Door after Mission Completion": [
        [
            grinch_items.moves.MAX
        ],
    ],
    "WV - City Hall - GC BP in Safe Room": [
        [
            grinch_items.moves.SNEAK
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER
        ],
    ],
    "WV - City Hall - GC BP in Statue Room": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WV - Clock Tower - GC BP in Bedroom": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WV - Clock Tower - GC BP in Bell Room": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
        ],
    ],
    # Who Forest Blueprints
    "WF - RS BP behind Vacuum Tube": [[]],
    "WF - RS BP in front of 2nd House near Vacuum Tube": [[]],
    "WF - RS BP near Tree House on Ground": [[]],
    "WF - RS BP behind Cable Car House": [[]],
    "WF - RS BP near Who Snowball in Cave": [[]],
    "WF - RS BP on Branch Platform closest to Glue Cannon": [[]],
    "WF - RS BP on Branch Platform Near Beast": [[]],
    "WF - RS BP on Branch Platform Elevated next to House": [[]],
    "WF - RS BP on Tree House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - SS BP in Branch Platform Elevated House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in Branch Platform House next to Beast": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in House in front of Civic Center Cave": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in House next to Tree House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in House across from Tree House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Right Side": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in 2nd House near Vacuum Tube Left Side": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in 2nd House near Vacuum Tube inbetween Blueprints": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - SS BP in House near Vacuum Tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Ski Resort - GC BP inside Dog's Fence": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Ski Resort - GC BP in Max Cave": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WF - Civic Center - GC BP on Left Side in Bat Cave Wall": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WF - Civic Center - GC BP in Frozen Ice": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
    ],
    # Who Dump Blueprints
    "WD - OCD BP inside Pipe near Vacuum Tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - OCD BP inside Pipe on Minefield side": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - OCD BP in Vent to Mayor's House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - OCD BP inside Pipe on Power Plant side": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - OCD BP near Right Side of Power Plant Wall": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - OCD BP near Who-Bris' Shack": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ]
    ],
    "WD - Minefield - OCD BP on Left Side of House": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Minefield - OCD BP on Right Side of Shack": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Minefield - OCD BP inside Guardian's House": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Power Plant - GC BP in Max Cave": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Power Plant - GC BP After First Gate": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - Generator Building - GC BP on the Highest Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Generator Building - GC BP at the Entrance after Mission Completion": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    # Who Lake Blueprints
    "WL - South Shore - MM BP on Bridge to Scout's Hut": [
        [
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP across from Tent near Porcupine": [
        [
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP near Outhouse": [
        [
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP near Hill Bridge": [
        [
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP on Scout's Hut Roof": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP on Grass Platform": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
            grinch_items.moves.SEIZE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP across Zipline Platform": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - MM BP behind Summer Beast": [
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - Scout's Hut - Steal Scout's Hat": [
        [
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WL - Scout's Hut - Steal Scout's Shirt": [
        [
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - Scout's Hut - Steal Scout's Shorts": [
        [
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - MM BP below Bridge": [[]],
    "WL - North Shore - MM BP behind Skunk Hut": [[]],
    "WL - North Shore - MM BP inside Skunk Hut": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WL - North Shore - MM BP inside House's Fence": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WL - North Shore - MM BP inside Boulder Box near Bridge": [
        [
            grinch_items.moves.SEIZE,
        ],
    ],
    "WL - North Shore - MM BP inside Boulder Box behind Skunk Hut": [
        [
            grinch_items.moves.SEIZE,
        ],
    ],
    "WL - North Shore - MM BP inside Drill House": [
        [
        ],
    ],
    "WL - North Shore - MM BP on Crow Platform near Drill House": [
        [
        ],
    ],
    "WL - Submarine World - GC BP Just Below Water Surface": [[]],
    "WL - Submarine World - GC BP Underwater": [[]],
    "WL - Mayor's Villa - GC BP on Tree Branch": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - Mayor's Villa - GC BP in Pirate's Cave": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
    ],
    # Finale
    "WV - Exhaust Pipes": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ],
    ],
    "WF - Skis": [
        [
            grinch_items.keys.SLEIGH_ROOM_KEY,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Tires": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.keys.SLEIGH_ROOM_KEY,
            grinch_items.moves.SEIZE,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - Submarine World - Twin-End Tuba": [
        [
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.keys.SLEIGH_ROOM_KEY,
        ],
    ],
    "WL - South Shore - GPS": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.keys.SLEIGH_ROOM_KEY,
            grinch_items.moves.SNEAK,
        ],
    ],
    "MC - Sleigh Ride - Stealing All Gifts": [[]],
    "MC - Sleigh Ride - Neutralizing Santa": [[]],
    "MC - Sleigh Ride - Save Christmas": [[]],
    # Hearts of Stone
    "WV - Post Office - Heart of Stone": [[]],
    "WF - Ski Resort - Heart of Stone": [[]],
    "WD - Minefield - Heart of Stone": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WL - North Shore - Heart of Stone": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    # Supadows
    "Spin N' Win - Easy": [[]],
    "Spin N' Win - Hard": [[]],
    "Spin N' Win - Real Tough": [[]],
    "Dankamania - Easy - 15 Points": [[]],
    "Dankamania - Hard - 15 Points": [[]],
    "Dankamania - Real Tough - 15 Points": [[]],
    "The Copter Race Contest - Easy": [[]],
    "The Copter Race Contest - Hard": [[]],
    "The Copter Race Contest - Real Tough": [[]],
    "Bike Race - 1st Place": [[]],
    "Bike Race - Top 2": [[]],
    "Bike Race - Top 3": [[]],
    # Intro
    "MC - Collect Key in Boxes": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "MC - 1st Crate Squashed": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "MC - 2nd Crate Squashed": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "MC - 3rd Crate Squashed": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "MC - 4th Crate Squashed": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "MC - 5th Crate Squashed": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "MC - Interact with the Telescope": [[]],
    "MC - I hate Whos!": [[]],
    "MC - I hate Christmas!": [[]],
    "MC - My heart is like a pea!": [[]],
    "MC - Move Boulder": [
        [
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ],
    ],
    "MC - Collect Max Door Key": [
        [
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
        ],
    ],
    "MC - Open Door with Breath Analyzer": [
        [
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WV - Smashing Snowmen - Next to Vacuum Tube": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Left Side of Post Office": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Right Side of Clock Tower": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Left Side of Clock Tower": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Between Christmas Tree and Orange Round Building": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - East of Christmas Tree on Platform": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Near Vacuum Tube on Blue Platform near Orange Bridge": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Left side of City Hall": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - South of Christmas Tree": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Smashing Snowmen - Right side of City Hall around the back": [
        [
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ]
    ],
    "WV - Launching Eggs Into Houses - On Gray Building right side of City Hall": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - On Orange Round Building facing Christmas Tree": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - Left side of Snow Wall on Gray Building": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - Above Vacuum Tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - Above Child near right side of Post Office": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - On Orange Building right side of City Hall": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - Greenish Building facing Christmas Tree above Child": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - Above Post Office": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - On Skinny Building right side of Clock Tower": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Launching Eggs Into Houses - Orange Building facing away from Vacuum Tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WV - Painting The Mayor's Posters - Near Vacuum Tube on right side on Platform": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Left side of City Hall on Red Building": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Orange Building in front of Post Office upper level": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Left side of Post Office on Orange Building left side wall": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Right side of City Hall on Gray Building Platform": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Next to Vacuum Tube on left side": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Right side of Clock Tower on Swinging Platform": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Orange Building in front of Post Office lower level": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Left Side of City Hall on Gray Building Platform": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Painting The Mayor's Posters - Right Side of City Hall on Orange Building": [
        [
            grinch_items.level_items.WV_PAINT_BUCKET,
        ],
    ],
    "WV - Post Office - Shuffling The Mail - Pink Room (Room 1)": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WV - Post Office - Shuffling The Mail - Orange Room (Room 2)": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WV - Post Office - Shuffling The Mail - Blue Room (Room 3)": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WV - Post Office - Shuffling The Mail - Yellow Room (Room 4)": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WV - Post Office - Shuffling The Mail - Gray Room (Room 5)": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WV - Clock Tower - Open Hatch to Floor 2": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Open Hatch to Floor 3": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Open Hatch to Floor 4": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Open Hatch to Floor 5": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Ring 1st Bell": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Ring 2nd Bell": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Ring 3rd Bell": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Ring 4th Bell": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WV - Clock Tower - Ring 5th Bell": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WF - Making Xmas Trees Droop - Swinging platform farthest to Glue Cannon": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - 2nd closest to Civic Center cave": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Swinging platform closest to Glue Cannon": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Next to Tree house": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Closest to Civic Center cave": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Tree 3rd closest to vacuum tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Tree 2nd closest to vacuum tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Tree closest to vacuum tube": [
        [
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Tree 4th closest to vacuum tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Making Xmas Trees Droop - Left of cable car": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Closest to Vacuum Tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WF - Putting Beehives In Cabins - Red house on glue cannon platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Green house on glue cannon platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - 2nd closest to vacuum tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WF - Putting Beehives In Cabins - Yellow house across from Tree House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Red house next to Tree House": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Tree house": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Red house near Cable car": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Blue house in front of civic center cave": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Putting Beehives In Cabins - Green house left side of Cable car": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Front side of Civic Center building": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Left side of Civic Center building": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Across tree branch swinging platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Middle platform of super toy parkour": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Front of Bat Cave entrance": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Guarded by who below super toy platforms": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Furthest platform of super toy parkour": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SNEAK,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.MAX,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Across snow boulders": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - After ice wall near entrance left side": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Civic Center - Replacing The Candles On The Cake With Fireworks - Across bridge near entrance": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Left side of center area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Center area between pipes": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Right side of center area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Who Bris Shack Area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Right area near robot parts vacuum": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Right area near entrance to center area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Right area near shooting pipe": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Near inward pipe in left area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Left area on right electric fence": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Feeding The Computer With Robot Parts - Left area on left electric fence": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in right side of center area": [[]],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in left side of center area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Shooting pipe in left area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in left area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Shooting pipe in right side": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,

        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Seizing pipe in rat area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,

        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Shooting pipe in right side inside pipe": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in center area pipe": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Swinging pipe in left area pipe": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,

        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Conducting The Stinky Gas To Who-Bris' Shack - Final pipe screw in Who Bris' Shack area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 1": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 2": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 3": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 4": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 5": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 6": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 7": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 8": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 9": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Infesting The Mayor's House With Rats - Rat 10": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.MAX,
        ],
    ],
    "WD - Stealing Food From Birds - Left area on right electric fence": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Right area near Minefield entrance": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Who Bris Shack Area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WD - Stealing Food From Birds - Shooting pipe near right area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Right area in rat section": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Left area near inward pipe": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Left area on left electric fence": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Left area below spinning pipe near blue tube": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Stealing Food From Birds - Near blue tube in center area": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WD - Stealing Food From Birds - TV Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant - Yellow Generator (4th)": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant - Orange Generator (3rd)": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant - Pink Generator (2nd)": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WD - Generator Building - Short-Circuiting Power-Plant - Blue Generator (1st)": [
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Right side of bridge to Scout Hut": [
        [
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Left side of summer beast": [
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Across from boulder": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Grass platform": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Left side of bridge right of rope wall": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Right side of summer beast": [
        [
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Across from clothes line": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Across swinging line": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Across from clothes line near North Shore bridge": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Sabotaging The Tents - Left of North Shore bridge": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Left of rack guarded by child": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Left of rack near entrance": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Middle of rack near entrance": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Right of rack near entrance": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Left of rack on wall platform": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Right of rack on wall platform": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
        ],
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Right of rack near North Shore Bridge": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Left of rack near North Shore Bridge": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Right of rack guarded by child": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - South Shore - Putting Thistles In Shorts - Middle of rack guarded by child": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Right side adjacent to fence area": [
        [
            grinch_items.level_items.WL_DRILL,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Left side adjacent to fence area": [
        [
            grinch_items.level_items.WL_DRILL,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Left side in fence area": [
        [
            grinch_items.level_items.WL_DRILL,
            grinch_items.moves.MAX,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Right side in fence area": [
        [
            grinch_items.level_items.WL_DRILL,
            grinch_items.moves.MAX,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - On beach left side below max house": [
        [
            grinch_items.level_items.WL_DRILL,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - On beach right side below max house": [
        [
            grinch_items.level_items.WL_DRILL,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Middle side in fence area": [
        [
            grinch_items.level_items.WL_DRILL,
            grinch_items.moves.MAX,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Behind max house": [
        [
            grinch_items.level_items.WL_DRILL,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Right side on top of car": [
        [
            grinch_items.level_items.WL_DRILL,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WL - North Shore - Drilling Holes In Canoes - Left side on top of car": [
        [
            grinch_items.level_items.WL_DRILL,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WL - Submarine World - Modifying The Marine Mobile - Outer Fast-moving Fish": [[]],
    "WL - Submarine World - Modifying The Marine Mobile - Inner Slow-moving Fish": [[]],
    "WL - Submarine World - Modifying The Marine Mobile - Pirate Ship in Cave": [[]],
    "WL - Submarine World - Modifying The Marine Mobile - Sea Cow Leaves": [[]],
    "WL - Submarine World - Modifying The Marine Mobile - Timed Cage": [[]],
    "WD - Power Plant - Touch Grass": [[]],
    "WL - South Shore - Touch Grass": [[]],
    "WL - North Shore - Touch Grass": [[]],
    "WL - Mayor's Villa - Touch Grass": [[]],
    "WV - Collect all Rotten Egg Launcher Blueprints": [
        [
            grinch_items.level_items.WV_WHO_CLOAK,
            grinch_items.moves.MAX,
        ],
    ],
    "WF - Collect all Rocket Spring Blueprints": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
    ],
    "WF - Collect all Slime Shooter Blueprints": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
        ],
    ],
    "WD - Collect all Octopus Climbing Device Blueprints": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WL - Collect all Marine Mobile Blueprints": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
        ],
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.SEIZE,
            grinch_items.moves.MAX,
            grinch_items.moves.SNEAK,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "MC - Collect all Grinch Copter Blueprints": [
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            grinch_items.keys.WHOVILLE,
            grinch_items.keys.WHO_FOREST,
            grinch_items.keys.WHO_DUMP,
            grinch_items.keys.WHO_LAKE,
        ],
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.keys.WHOVILLE,
            grinch_items.keys.WHO_FOREST,
            grinch_items.keys.WHO_DUMP,
            grinch_items.keys.WHO_LAKE,
        ],
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.OCTOPUS_CLIMBING_DEVICE,
            "4:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE,
        ],
        [
            grinch_items.level_items.WL_SCOUT_CLOTHES,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.level_items.WF_CABLE_CAR_ACCESS_CARD,
            grinch_items.gadgets.MARINE_MOBILE,
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.SNEAK,
            grinch_items.moves.PANCAKE,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            "4:" + grinch_items.keys.PROGRESSIVE_VACUUM_TUBE,
        ],
    ],
    "WV - Collect all Binoculars Blueprints": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.moves.SEIZE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 1 time": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 2 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 3 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 4 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 5 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 6 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 7 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 8 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 9 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Squash the Groundhog 10 times": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Shoot Down North West Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Shoot Down South West Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Shoot Down South Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Shoot Down South East Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WD - Shoot Down North East Platform": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WV - Painting Bucket": [
        [
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WV - Clock Tower - Who Cloak": [[]],
    "WV - Clock Tower - Hammer": [
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.MAX,
            grinch_items.moves.SEIZE,
            grinch_items.moves.SNEAK,
        ],
    ],
    "WV - City Hall - Sculpting Tools": [
        [
            grinch_items.moves.SNEAK,
            grinch_items.moves.SEIZE,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.moves.SEIZE,
            grinch_items.moves.PANCAKE,
        ],
        [
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.SEIZE,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WF - Glue Bucket": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    "WF - Cable Car Access Card": [
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.ROCKET_SPRING,
            grinch_items.moves.BAD_BREATH,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.moves.BAD_BREATH,
            grinch_items.gadgets.SLIME_SHOOTER,
        ],
    ],
    "WD - Minefield - Scissors": [
        [
            grinch_items.gadgets.GRINCH_COPTER,
        ],
        [
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
            grinch_items.gadgets.SLIME_SHOOTER,
            grinch_items.gadgets.ROCKET_SPRING,
        ],
    ],
    "WL - Scout's Hut - Scout Clothes": [
        [
            grinch_items.moves.BAD_BREATH,
            grinch_items.moves.PANCAKE,
        ],
    ],
    "WL - North Shore - Drill": [[]],
    "WL - Mayor's Villa - Rope": [
        [
            grinch_items.moves.MAX,
        ],
    ],
    "WL - Mayor's Villa - Hook": [
        [
            grinch_items.moves.BAD_BREATH,
            grinch_items.gadgets.GRINCH_COPTER,
            grinch_items.gadgets.ROTTEN_EGG_LAUNCHER,
        ],
    ],
    # "Green Present": [
    #     []
    # ],
    # "Red Present": [
    #     []
    # ],
    # "Pink Present": [
    #     [grinch_items.gadgets.ROTTEN_EGG_LAUNCHER],
    #     [move_rando]
    #     [PC]
    # ],
    # "Yellow Present": [
    #     []
    #     "move_rando"
    #     [PC]
    # ]
}

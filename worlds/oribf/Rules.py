from typing import Set, cast

from .RulesData import location_rules
from .RulesData import connection_rules
from .Items import OriBlindForestItem, item_dict
from .Locations import OriBlindForestLocation, tagged_locations_dict, event_location_list
from .Options import OriBlindForestOptions, MapstoneLogic
from BaseClasses import CollectionState, Location, Entrance, ItemClassification, Region
from ..AutoWorld import World
from ..generic.Rules import add_rule, set_rule


def apply_location_rules(world: World):
    # for each region in location rules, and for each location
    # create a location and call process_access_point
    for region_name, locations in location_rules.items():
        region = world.get_region(region_name)
        valid_location_ids: dict[str, int | None] = get_location_ids(world, list(locations.keys()))
        region.add_locations(valid_location_ids, OriBlindForestLocation)

        for location, rulesets in locations.items():
            if location in valid_location_ids.keys():
                process_access_point(world, world.get_location(location), rulesets)


def get_location_ids(world: World, locations: list[str]) -> dict[str, int | None]:
    # get the ids for each location in the list as long as they aren't excluded
    # if the location is an event, create it with a None id
    # otherwise add its id from the name_to_id list
    ids: dict[str, int | None] = {}
    for location in locations:
        if location not in world.location_exclusion_list:
            if location in event_location_list:
                ids[location] = None
            else:
                ids[location] = world.location_name_to_id[location]

    return ids


def apply_connection_rules(world: World):
    # for each region in connection rules, and for each connecting region, 
    # create an entrance and call process_access_point
    for region_name, connections in connection_rules.items():
        region = world.get_region(region_name)
        id = 1
        for connection, rulesets in connections.items():
            entrance_name = region_name + "_to_" + connection + "_" + str(id)
            id += 1
            region.connect(world.get_region(connection), entrance_name)
            access_point = world.get_entrance(entrance_name)
            process_access_point(world, access_point, rulesets)


def process_access_point(world: World, access_point: Location | Entrance, rulesets: dict[str, list[list[str | tuple[str, int]]]]):
    # preface with a false so all other rules can be combined with OR
    set_rule(access_point, lambda state: False)

    # for each ruleset in the location/entrance, call process_ruleset
    for ruleset_name, ruleset in rulesets.items():
        if ruleset_name in world.logic_sets:
            process_ruleset(world, access_point, ruleset)


def process_ruleset(world: World, access_point: Location | Entrance, ruleset: list[list[str | tuple[str, int]]]):
    # for each access set in the ruleset, call process_access_set
    for access_set in ruleset:
        process_access_set(world, access_point, access_set)

def process_access_set(world: World, access_point: Location | Entrance, access_set: list[str | tuple[str, int]]):
    # add the rule for the access set list using oribf_has
    # this line needs to be in a separate function from the previous for loop in order to work properly 
    # (likely lambda function strangeness)
    add_rule(access_point, lambda state: all(oribf_has(world, state, item) for item in access_set), "or")
            
    
def oribf_has(world: World, state: CollectionState, item: str | tuple[str, int]) -> bool:
    options: OriBlindForestOptions = cast(OriBlindForestOptions, world.options)

    if type(item) == str:
        if item in item_dict.keys():
            # handles normal abilities like Dash, Climb, Wind, etc.
            return state.has(item, world.player)
        
        elif item == "Free":
            return True
        
        elif item == "Lure":
            return "Lure" in options.logic_modifiers.value
        
        elif item == "DoubleBash":
            return "DoubleBash" in options.logic_modifiers.value and state.has("Bash", world.player)
        
        elif item == "GrenadeJump":
            return "GrenadeJump" in options.logic_modifiers.value and state.has_all(["Climb", "ChargeJump", "Grenade"], world.player)
        
        elif item == "ChargeFlameBurn":
            return "ChargeFlameBurn" in options.logic_modifiers.value and \
                state.has("ChargeFlame", world.player) and state.has("AbilityCell", world.player, 3)
        
        elif item in ["ChargeDash", "RocketJump"]:
            return "ChargeDash" in options.logic_modifiers.value and \
                state.has("Dash", world.player) and state.has("AbilityCell", world.player, 6)
        
        elif item == "AirDash": 
            return "AirDash" in options.logic_modifiers.value and \
                state.has("Dash", world.player) and state.has("AbilityCell", world.player, 3)
        
        elif item == "TripleJump":
            return "TripleJump" in options.logic_modifiers.value and \
                state.has("DoubleJump", world.player) and state.has("AbilityCell", world.player, 12)
        
        elif item == "UltraDefense":
            return "DamageBoost" in options.logic_modifiers.value and state.has("AbilityCell", world.player, 12)
        
        elif item == "BashGrenade":
            return state.has_all(["Bash", "Grenade"], world.player)
        
        elif item == "Rekindle":
            return "Rekindle" in options.logic_modifiers.value
        
        elif item == "Open":
            # closed dungeons not implemented
            return True

        elif item == "OpenWorld":
            # open world not implemented yet
            return False
        else:
            return False
    else:
        # if item isnt a string its a tuple (check for number of health, keystones, etc.)
        # if item is a health cell, only add it if damage boost is enabled
        if (item[0] == "HealthCell" and "DamageBoost" in options.logic_modifiers.value) or item[0] != "HealthCell":
            return state.has(item[0], world.player, int(item[1]))

    return False


def oribf_has_all(state: CollectionState, items: Set[str], player: int) -> bool:
    return all(state.has(item, player) if type(item) == str else state.has(item[0], player, int(item[1]))
               for item in items)


def create_progressive_maps(world: World):
    # place the locked items in the events that were created before
    for event in event_location_list:
        world.get_location(event).place_locked_item(OriBlindForestItem(event, ItemClassification.progression, None, world.player))

    # create the progressive map locations
    menu_region: Region = world.get_region("Menu")
    menu_region.add_locations({location: world.location_name_to_id[location] for location in tagged_locations_dict["ProgressiveMap"]}, \
                               OriBlindForestLocation)

    for location_name in tagged_locations_dict["ProgressiveMap"]:
        location: Location = world.get_location(location_name)
        amount: int = int(location_name[-1])
        set_progressive_mapstone_rule(world, location, amount)

def set_progressive_mapstone_rule(world: World, location: Location, amount: int):
    set_rule(location, lambda state: (at_least([state.can_reach_location(map_event, world.player) \
                                               for map_event in event_location_list], amount=amount)) and \
                                      state.has("MapStone", world.player, count=amount))

def at_least(conditions: list[bool], amount: int) -> bool:
    count: int = 0
    for flag in conditions:
        if flag:
            count += 1
    return count >= amount        

def get_goal_condition(world: World, state: CollectionState, goal: str):
    options: OriBlindForestOptions = cast(OriBlindForestOptions, world.options)

    if goal == "HoruEscape":
        return state.can_reach_region("HoruEscapeInnerDoor", world.player)

    elif goal == "AllSkillTrees":
        return all(state.can_reach_location(skill_tree, world.player) for skill_tree in tagged_locations_dict["Skill"])

    elif goal == "AllMaps":
        location_tag: str = ""
        if options.mapstone_logic == MapstoneLogic.option_progressive:
            location_tag = "ProgressiveMap"
        else:
            location_tag = "Map"

        return all(state.can_reach_location(area_map, world.player) for area_map in tagged_locations_dict[location_tag])

    elif goal == "WarmthFragments":
        return state.has("WarmthFragment", world.player, options.warmth_fragments_required.value)

    elif goal == "WorldTour":
        return state.has("Relic", world.player, options.relic_count.value)

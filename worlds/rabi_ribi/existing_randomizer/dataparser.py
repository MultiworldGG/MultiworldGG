import ast, re, os
from typing import Any, Dict, List

from .utility import *
from ..options import RabiRibiOptions
from ..utility import resource_listdir

"""
Knowledge levels:
    BASIC
    INTERMEDIATE
    ADVANCED
    OBSCURE

Difficulty levels:
    NORMAL
    HARD
    V_HARD
    EXTREME
    STUPID
"""

KNOWLEDGE_INTERMEDIATE = 'KNOWLEDGE_INTERMEDIATE'
KNOWLEDGE_ADVANCED = 'KNOWLEDGE_ADVANCED'
KNOWLEDGE_OBSCURE = 'KNOWLEDGE_OBSCURE'
DIFFICULTY_HARD = 'DIFFICULTY_HARD'
DIFFICULTY_V_HARD = 'DIFFICULTY_V_HARD'
DIFFICULTY_EXTREME = 'DIFFICULTY_EXTREME'
DIFFICULTY_STUPID = 'DIFFICULTY_STUPID'
OPEN_MODE = 'OPEN_MODE'

NO_CONDITIONS = lambda v : True
INFTY = 99999

def define_config_flags():
    d = {
        "ZIP_REQUIRED": False,
        "BUNSTRIKE_ZIP_REQUIRED": False,
        "SEMISOLID_CLIPS_REQUIRED": False,
        "BLOCK_CLIPS_REQUIRED": True,
        "BORING_TRICKS_REQUIRED": False,
        "POST_GAME_ALLOWED": True,
        "POST_IRISU_ALLOWED": True,
        "HALLOWEEN_REACHABLE": False,
        "PLURKWOOD_REACHABLE": True,
        "WARP_DESTINATION_REACHABLE": False,
        "DARKNESS_WITHOUT_LIGHT_ORB": True,
        "UNDERWATER_WITHOUT_WATER_ORB": True,
        "EXPLOSIVES_WITH_CARROT_SHOOTER": True,
        "EVENT_WARPS_REQUIRED": True,
    }
    return d

def define_setting_flags(settings):
    return {
        # Truths
        "TRUE": True,
        "FALSE": False,
        # Difficulty Flags
        KNOWLEDGE_INTERMEDIATE: False,
        KNOWLEDGE_ADVANCED: False,
        KNOWLEDGE_OBSCURE: False,
        DIFFICULTY_HARD: False,
        DIFFICULTY_V_HARD: False,
        DIFFICULTY_EXTREME: False,
        DIFFICULTY_STUPID: False,
        # Other Flags
        OPEN_MODE: settings.open_mode,
    }

# The values can be either a expression constrant, which is expressed as a string,
# or a lambda, that takes in a variables object and returns a bool.
def define_pseudo_items():
    return {
        "WALL_JUMP_LV2": "WALL_JUMP & TOWN_SHOP",
        "HAMMER_ROLL_LV3": "rHAMMER_ROLL & TOWN_SHOP & CHAPTER_3",
        "AIR_DASH_LV3": "rAIR_DASH & TOWN_SHOP",
        "SPEED_BOOST_LV3": "SPEED_BOOST & TOWN_SHOP",
        "BUNNY_AMULET_LV2": "(BUNNY_AMULET & (TOWN_SHOP | ((POST_GAME | POST_IRISU) & TM_RUMI))) | CHAPTER_3",
        "BUNNY_AMULET_LV3": "(BUNNY_AMULET & (TOWN_SHOP | ((POST_GAME | POST_IRISU) & TM_RUMI))) | CHAPTER_4",
        "BUNNY_AMULET_LV4": "BUNNY_AMULET & (POST_GAME | POST_IRISU) & TM_RUMI",
        "PIKO_HAMMER_LEVELED": "PIKO_HAMMER",
        "CARROT_BOMB_ENTRY": "CARROT_BOMB",
        "CARROT_SHOOTER_ENTRY": "CARROT_SHOOTER",
        "CHARGE_CARROT_SHOOTER_ENTRY" : "CARROT_SHOOTER & CHARGE_RING",

        "COCOA_1": "FOREST_COCOA_ROOM",
        "KOTRI_1": "PARK_KOTRI",
        "ASHURI_2": "RIVERBANK_LEVEL3",
        "BOSS_KEKE_BUNNY": "PLURKWOOD_MAIN",
        "BOSS_RIBBON": "SPECTRAL_WARP",

        "TM_COCOA": "CHAPTER_1 & COCOA_1 & KOTRI_1 & CAVE_COCOA",
        "TM_ASHURI": "RIVERBANK_LEVEL3 & TOWN_MAIN & SPECTRAL_WEST",
        "TM_RITA": "SNOWLAND_RITA",
        "TM_CICINI": "SPECTRAL_CICINI_ROOM",
        "TM_SAYA": "EVERNIGHT_SAYA & EVERNIGHT_EAST_OF_WARP",
        "TM_SYARO": "SYSTEM_INTERIOR_MAIN",
        "TM_PANDORA": "PYRAMID_MAIN",
        "TM_NIEVE": "PALACE_LEVEL_5 & ICY_SUMMIT_NIXIE",
        "TM_NIXIE": "PALACE_LEVEL_5 & ICY_SUMMIT_NIXIE",
        "TM_ARURAUNE": "FOREST_NIGHT_WEST",
        "TM_SEANA": "TM_VANILLA & TM_CHOCOLATE & TM_CICINI & TM_SYARO & TM_NIEVE & TM_NIXIE & AQUARIUM_SEANA & PARK_TOWN_ENTRANCE",
        "TM_LILITH": "SKY_ISLAND_MAIN & TM_CICINI",
        "TM_VANILLA": "SKY_BRIDGE_EAST_LOWER",
        "TM_CHOCOLATE": "CHAPTER_1 & RAVINE_CHOCOLATE",
        "TM_KOTRI": "GRAVEYARD_KOTRI & VOLCANIC_MAIN",
        "TM_KEKE_BUNNY": "BOSS_KEKE_BUNNY & PLURKWOOD_MAIN & TOWN_MAIN",
        "TM_MIRIAM": "HALL_OF_MEMORIES",
        "TM_RUMI": "FORGOTTEN_CAVE_2",
        "TM_IRISU": "WARP_DESTINATION_HOSPITAL & CHAPTER_5 & 15TM & TM_MIRIAM & TM_RUMI & LIBRARY_IRISU",

        "2TM": lambda v: count_town_members(v) >= 2,
        "3TM": lambda v: count_town_members(v) >= 3,
        "4TM": lambda v: count_town_members(v) >= 4,
        "7TM": lambda v: count_town_members(v) >= 7,
        "10TM": lambda v: count_town_members(v) >= 10,
        "SPEEDY": "ITM & TM_CICINI & TOWN_MAIN & 3TM",

        "3_MAGIC_TYPES": lambda v : count_magic_types(v) >= 3,
        "ITEM_MENU": "TOWN_MAIN | (ADV & 3_MAGIC_TYPES)",

        "CHAPTER_1": "TOWN_MAIN",
        "CHAPTER_2": "TOWN_MAIN & 2TM",
        "CHAPTER_3": "TOWN_MAIN & 4TM",
        "CHAPTER_4": "TOWN_MAIN & 7TM",
        "CHAPTER_5": "TOWN_MAIN & 10TM",
        "CHAPTER_6": "CHAPTER_5",
        "CHAPTER_7": "TM_RUMI",
        "15TM": lambda v: enough_town_members_irisu(v),

        "CONSUMABLE_USE": "ITEM_MENU & (RUMI_DONUT | RUMI_CAKE | COCOA_BOMB | GOLD_CARROT)",
        "AMULET_FOOD": lambda v : enough_amu_food(v, 1),
        "2_AMULET_FOOD": lambda v : enough_amu_food(v, 2),
        "3_AMULET_FOOD": lambda v : enough_amu_food(v, 3),
        "4_AMULET_FOOD": lambda v : enough_amu_food(v, 4),
        "6_AMULET_FOOD": lambda v : enough_amu_food(v, 6),
        "MANY_AMULET_FOOD": "ITEM_MENU & TOWN_SHOP & BUNNY_AMULET",

        "BOOST": "BEACH_MAIN | (RUMI_DONUT & ITEM_MENU)",
        "BOOST_MANY": "ITEM_MENU & TOWN_SHOP",
        "BOOST_BORING": "(BEACH_MAIN & BORING) | (RUMI_DONUT & ITEM_MENU)",
    }


def define_alternate_conditions(settings, variable_names_set, default_expressions):
    d = {
        "SOUL_HEART": "TOWN_SHOP",
        "BOOK_OF_CARROT": "TOWN_SHOP",
        "HEALING_STAFF": "TOWN_SHOP",
        "MAX_BRACELET": "TOWN_SHOP",
        "STRANGE_BOX": "TM_SYARO & TOWN_MAIN",
        "BUNNY_AMULET": "CHAPTER_2",
        "RUMI_DONUT": "TOWN_SHOP",
        "RUMI_CAKE": "TOWN_SHOP",
        "COCOA_BOMB": "TM_COCOA & TOWN_MAIN & 3TM",
    }
    if not settings.shuffle_gift_items:
        d.update({
            "SPEED_BOOST": "TOWN_SHOP",
            "BUNNY_STRIKE": "SLIDING_POWDER & TOWN_SHOP & TM_CICINI",
            "P_HAIRPIN": "BOSS_KEKE_BUNNY & PLURKWOOD_MAIN",
        })

    # AP Change: Fixed reuse of d (dict[str, str])
    callable_d = {}
    for key in d.keys():
        if type(d[key]) == str:
            callable_d[key] = parse_expression_lambda(d[key], variable_names_set, default_expressions)
    return callable_d


def define_default_expressions(variable_names_set):
    # Default expressions take priority over actual variables.
    # so if we parse an expression that has AIR_DASH, the default expression AIR_DASH will be used instead of the variable AIR_DASH.
    # however, the expressions parsed in define_default_expressions (just below) cannot use default expressions in their expressions.
    expr = lambda s : parse_expression(s, variable_names_set)
    expr_all = lambda d : dict((k,expr(v) if type(v)==str else v) for k,v in d.items())

    def1 = expr_all({
        "INTERMEDIATE": "KNOWLEDGE_INTERMEDIATE",
        "ADVANCED": "KNOWLEDGE_ADVANCED",
        "OBSCURE": "KNOWLEDGE_OBSCURE",
        "HARD": "DIFFICULTY_HARD",
        "V_HARD": "DIFFICULTY_V_HARD",
        "EXTREME": "DIFFICULTY_EXTREME",
        "STUPID": "DIFFICULTY_STUPID",

        "ZIP": "ZIP_REQUIRED",
        "SEMISOLID_CLIP": "SEMISOLID_CLIPS_REQUIRED",
        "BLOCK_CLIP": "BLOCK_CLIPS_REQUIRED",
        "BORING": "BORING_TRICKS_REQUIRED",
        "POST_GAME": "POST_GAME_ALLOWED",
        "POST_IRISU": "POST_IRISU_ALLOWED",
        "HALLOWEEN": "HALLOWEEN_REACHABLE",
        "PLURKWOOD": "PLURKWOOD_REACHABLE",
        "WARP_DESTINATION": "WARP_DESTINATION_REACHABLE",
        "BUNNY_STRIKE": "SLIDING_POWDER & BUNNY_STRIKE & PIKO_HAMMER",
        "BUNNY_WHIRL": "BUNNY_WHIRL & PIKO_HAMMER",
        "AIR_DASH": "AIR_DASH & PIKO_HAMMER",
        "AIR_DASH_LV3": "AIR_DASH_LV3 & PIKO_HAMMER",
        "HAMMER_ROLL": "HAMMER_ROLL & BUNNY_WHIRL & PIKO_HAMMER",
        "HAMMER_ROLL_LV3": "HAMMER_ROLL_LV3 & BUNNY_WHIRL & PIKO_HAMMER",
        "DARKNESS": "DARKNESS_WITHOUT_LIGHT_ORB | LIGHT_ORB",
        "UNDERWATER": "UNDERWATER_WITHOUT_WATER_ORB | WATER_ORB",
        "CARROT_SHOOTER": "CARROT_SHOOTER & EXPLOSIVES_WITH_CARROT_SHOOTER",
        "EVENT_WARP": "EVENT_WARPS_REQUIRED",
        "PROLOGUE_TRIGGER": "CHAPTER_1 | OPEN_MODE",
        #"RIBBON": "TRUE",
        #"WARP": "TRUE",
        "NONE": "TRUE",
        "IMPOSSIBLE": "FALSE",
    })

    expr = lambda s : parse_expression(s, variable_names_set, def1)
    def2 = expr_all({
        "ITM": "INTERMEDIATE",
        "ITM_HARD": "INTERMEDIATE & HARD",
        "ITM_VHARD": "INTERMEDIATE & V_HARD",
        "ADV": "ADVANCED",
        "ADV_HARD": "ADVANCED & HARD",
        "ADV_VHARD": "ADVANCED & V_HARD",
        "ADV_EXT": "ADVANCED & EXTREME",
        "ADV_STUPID": "ADVANCED & STUPID",
        "OBS": "OBSCURE",
        "OBS_HARD": "OBSCURE & HARD",
        "OBS_VHARD": "OBSCURE & V_HARD",
        "OBS_EXT": "OBSCURE & EXTREME",
        "OBS_STUPID": "OBSCURE & STUPID",
    })
    def1.update(def2)

    expr = lambda s : parse_expression(s, variable_names_set, def1)
    def3 = expr_all({
        "HAMMER_ROLL_ZIP": "ZIP & HAMMER_ROLL_LV3",
        "SLIDE_ZIP": "ZIP & SLIDING_POWDER",
        "ROLL_BONK_ZIP": "ZIP & HAMMER_ROLL & OBS_VHARD",
        "BUNSTRIKE_ZIP": "ZIP & BUNSTRIKE_ZIP_REQUIRED & BUNNY_STRIKE",
        "WHIRL_BONK": "BUNNY_WHIRL & ITM_HARD",
        "WHIRL_BONK_CANCEL": "BUNNY_WHIRL & ((BUNNY_AMULET & ITM_HARD) | OBS_VHARD)",
        "SLIDE_JUMP_BUNSTRIKE": "BUNNY_STRIKE & INTERMEDIATE",
        "SLIDE_JUMP_BUNSTRIKE_CANCEL": "BUNNY_STRIKE & BUNNY_AMULET & ITM_HARD",
        "DOWNDRILL_SEMISOLID_CLIP": "PIKO_HAMMER_LEVELED & SEMISOLID_CLIP",
        "2TILE_DOWNDRILL_SEMISOLID_CLIP": "PIKO_HAMMER_LEVELED & SEMISOLID_CLIP & OBS_EXT",
        "8TILE_WALLJUMP": "(ITM & (HARD | WALL_JUMP)) | RABI_SLIPPERS | AIR_JUMP",

        "EXPLOSIVES": "CARROT_BOMB | (CARROT_SHOOTER & BOOST)",
        "EXPLOSIVES_ENEMY": "CARROT_BOMB | CARROT_SHOOTER",

        "SPEED1": "SPEED_BOOST | SPEEDY",
        "SPEED2": "SPEED_BOOST_LV3 | SPEEDY",
        "SPEED3": "SPEED_BOOST_LV3 | (SPEED_BOOST & SPEEDY)",
        "SPEED5": "SPEED_BOOST_LV3 & SPEEDY",
    })
    def1.update(def3)

    expr = lambda s : parse_expression(s, variable_names_set, def1)
    def4 = expr_all({
        "1TILE_ZIP": "SLIDE_ZIP",
        "2TILE_ZIP": "SLIDE_ZIP & ADV_VHARD",
        "3TILE_ZIP": "SLIDE_ZIP & HARD",
        "4TILE_ZIP": "SLIDE_ZIP & HARD",
        "5TILE_ZIP": "RABI_SLIPPERS & SLIDE_ZIP & ADV_VHARD",

        "5TILE_WALL_CLIMB": "\
            AIR_JUMP | AIR_DASH | (ADV_VHARD & RABI_SLIPPERS & AMULET_FOOD)\
            | (ADV_EXT & WALL_JUMP & 2_AMULET_FOOD & (BUNNY_AMULET | STUPID))\
            | (OBS_STUPID & BORING & 6_AMULET_FOOD)\
        ",

        "5TILE_WALL_CLIMB_BUNSTRIKE": "\
            (RABI_SLIPPERS & SLIDE_JUMP_BUNSTRIKE)\
            | (ADV_EXT & SLIDE_JUMP_BUNSTRIKE_CANCEL & 2_AMULET_FOOD)\
        ",
    })
    def1.update(def4)

    return def1

def shufflable_gift_item_map_modifications():
    # AP Change: Use os.path.join
    return [
        os.path.join('existing_randomizer', 'maptemplates', 'shuffle_gift_items', 'mod_p_hairpin.txt'),
        os.path.join('existing_randomizer', 'maptemplates', 'shuffle_gift_items', 'mod_bunstrike_speedboost.txt')
    ]

# AP Change: Moved get_default_areaids to utility.py

TOWN_MEMBERS = (
    'TM_COCOA', 'TM_ASHURI', 'TM_RITA', 'TM_CICINI',
    'TM_SAYA', 'TM_SYARO', 'TM_PANDORA', 'TM_NIEVE',
    'TM_NIXIE', 'TM_ARURAUNE', 'TM_SEANA', 'TM_LILITH',
    'TM_VANILLA', 'TM_CHOCOLATE', 'TM_KOTRI', 'TM_KEKE_BUNNY',
    )
def count_town_members(variables):
    return sum(1 for tm in TOWN_MEMBERS if variables[tm])

# removed TM_VANILLA, TM_CHOCOLATE, TM_CICINI, TM_SYARO, TM_NIEVE, and TM_NIXIE from requirements since TM_SEANA is encompasses them
TOWN_MEMBERS_IRISU = (
    'TM_COCOA', 'TM_ASHURI', 'TM_RITA', 'TM_SAYA',
    'TM_PANDORA', 'TM_ARURAUNE', 'TM_SEANA', 'TM_LILITH',
    'TM_KOTRI',
    )
def enough_town_members_irisu(variables):
    return sum(1 for tm in TOWN_MEMBERS_IRISU if variables[tm]) >= 9

MAGIC_TYPES = ('SUNNY_BEAM','CHAOS_ROD','HEALING_STAFF','EXPLODE_SHOT','CARROT_SHOOTER')
def count_magic_types(variables):
    return sum(1 for tm in MAGIC_TYPES if variables[tm]) + 1

CONSUMABLE_ITEMS = ('RUMI_DONUT','RUMI_CAKE','COCOA_BOMB','GOLD_CARROT')
NORMAL_CONSUMABLE_ITEMS = ('RUMI_CAKE','COCOA_BOMB','GOLD_CARROT')
def enough_amu_food(variables, amount):
    amulet = 0
    food = 0
    if variables['BUNNY_AMULET_LV4']: amulet = 4
    elif variables['BUNNY_AMULET_LV3']: amulet = 3
    elif variables['BUNNY_AMULET_LV2']: amulet = 2
    elif variables['BUNNY_AMULET']: amulet = 1
    if variables['ITEM_MENU']:
        if variables['RUMI_DONUT']:
            food = 1
            if variables['BUNNY_AMULET']: amulet += 1
        food += sum(1 for tm in NORMAL_CONSUMABLE_ITEMS if variables[tm])
    if amulet >= 4 and variables['TM_KOTRI'] and variables['3TM']:
        amulet += 1
    return (amulet + food) >= amount


def evaluate_pseudo_item_constraints(pseudo_items, variable_names_set, default_expressions):
    for key in pseudo_items.keys():
        if type(pseudo_items[key]) == str:
            pseudo_items[key] = parse_expression_lambda(pseudo_items[key], variable_names_set, default_expressions)


def parse_locations_and_items():
    locations = {}
    items = []
    shufflable_gift_items = []
    additional_items = {}
    map_transitions = []
    start_locations = []

    # AP Change: Use pkgutil to read file from .apworld
    locations_items_file = os.path.join('existing_randomizer', 'locations_items.txt')
    lines = read_file_and_strip_comments(locations_items_file)

    type_map = {
        "WARP" : LOCATION_WARP,
        "MAJOR" : LOCATION_MAJOR,
        "MINOR" : LOCATION_MINOR,
    }

    READING_NOTHING = 0
    READING_LOCATIONS = 1
    READING_MAP_TRANSITIONS = 2
    READING_ADDITIONAL_ITEMS = 3
    READING_SHUFFLABLE_GIFT_ITEMS = 4
    READING_ITEMS = 5
    READING_START_LOCATIONS = 6

    currently_reading = READING_NOTHING

    for line in lines:
        if line.startswith('===Locations==='):
            currently_reading = READING_LOCATIONS
        elif line.startswith('===MapTransitions==='):
            currently_reading = READING_MAP_TRANSITIONS
        elif line.startswith('===AdditionalItems==='):
            currently_reading = READING_ADDITIONAL_ITEMS
        elif line.startswith('===ShufflableGiftItems==='):
            currently_reading = READING_SHUFFLABLE_GIFT_ITEMS
        elif line.startswith('===Items==='):
            currently_reading = READING_ITEMS
        elif line.startswith('===StartLocations==='):
            currently_reading = READING_START_LOCATIONS
        elif currently_reading == READING_LOCATIONS:
            if len(line) <= 0: continue
            location, location_type = (x.strip() for x in line.split(':'))
            location_type = type_map[location_type]
            if location in locations:
                fail('Location %s already defined!' % location)
            locations[location] = location_type
        elif currently_reading == READING_ADDITIONAL_ITEMS:
            if len(line) <= 0: continue
            item_name, item_id = (x.strip() for x in line.split(':'))
            item_id = int(item_id)
            if item_name in additional_items:
                fail('Additional Item %s already defined!' % item_name)
            additional_items[item_name] = item_id
        elif currently_reading == READING_SHUFFLABLE_GIFT_ITEMS:
            if len(line) <= 0: continue
            if item_name in shufflable_gift_items:
                fail('Shufflable Gift Item %s already defined!' % item_name)
            shufflable_gift_items.append(parse_item_from_string(line))
        elif currently_reading == READING_ITEMS:
            if len(line) <= 0: continue
            if item_name in items:
                fail('Item %s already defined!' % item_name)
            items.append(parse_item_from_string(line))
        elif currently_reading == READING_MAP_TRANSITIONS:
            if len(line) <= 0: continue
            # Line format:
            # area : (x, y, w, h) : origin_location : direction : map_event : trigger_id : entrance_id
            area_current, rect, origin_location, walking_direction, area_target_ev, entry_target_ev, entry_current_ev = [x.strip() for x in line.split(':')]

            if walking_direction == 'MovingRight': walking_right = True
            elif walking_direction == 'MovingLeft': walking_right = False
            else: fail('Undefined map transition direction: %s' % walking_direction)
            area_target = int(area_target_ev) - 161
            entry_target = int(entry_target_ev) - 200
            entry_current = (int(entry_current_ev)-227 if int(entry_current_ev) >= 227 else int(entry_current_ev)-176+6)

            map_transitions.append(MapTransition(
                origin_location = origin_location,
                area_current = int(area_current),
                entry_current = entry_current,
                area_target = area_target,
                entry_target = entry_target,
                walking_right = walking_right,
                rect = rect,
            ))
        elif currently_reading == READING_START_LOCATIONS:
            if len(line) <= 0: continue
            # Line format:
            # area : (x, y) : location
            area, position, weight, location = [x.strip() for x in line.split(':')]
            if not location in locations:
                fail('Location %s is not defined!' % location)
            start_locations.append(StartLocation(
                area = int(area),
                position = position,
                weight = int(weight),
                location = location,
            ))



    # Validate map transition locations
    if set(mt.origin_location for mt in map_transitions) - set(locations.keys()):
        print_err('Unknown locations: %s' % '\n'.join(
            set(mt.origin_location for mt in map_transitions) - set(locations.keys())
        ))

    return locations, map_transitions, items, additional_items, shufflable_gift_items, start_locations

# throws errors for invalid formats.
def parse_edge_constraints(locations_set, variable_names_set, default_expressions):
    # AP Change: Use pkgutil to read file from .apworld
    constraints_graph = os.path.join('existing_randomizer', 'constraints_graph.txt')
    lines = read_file_and_strip_comments(constraints_graph)
    jsondata = ' '.join(lines)
    jsondata = re.sub(r',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split(r'}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'
    cdicts = parse_json(jsondata)

    constraints = []

    for cdict in cdicts:
        from_location, to_location = (x.strip() for x in cdict['edge'].split('->'))
        if from_location not in locations_set: fail('Unknown location: %s' % from_location)
        if to_location not in locations_set: fail('Unknown location: %s' % to_location)
        prereq = parse_expression(cdict['prereq'], variable_names_set, default_expressions)
        constraints.append(EdgeConstraintData(from_location, to_location, prereq))

    # Validate that there are no duplicate edges defined
    if len(constraints) != len(set(cdict['edge'] for cdict in cdicts)):
        # Error: duplicate edge. Find the duplicate edge.
        edge_names = [cdict['edge'] for cdict in cdicts]
        duplicates = [edge for edge in set(edge_names) if edge_names.count(edge) > 1]
        fail('Duplicate edge definition(s) in constraints!\n%s' % '\n'.join(duplicates))

    return constraints

def parse_item_constraints(settings, items_set, shufflable_gift_items_set, locations_set, variable_names_set, default_expressions):
    # AP Change: Use pkgutil to read file from .apworld
    constraints = os.path.join('existing_randomizer', 'constraints.txt')
    lines = read_file_and_strip_comments(constraints)
    jsondata = ' '.join(lines)
    jsondata = re.sub(r',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split(r'}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'
    cdicts = parse_json(jsondata)

    def parse_alternates(alts):
        if alts == None: return {}
        return dict( (name, ExpressionData( parse_expression(constraint, variable_names_set, default_expressions)) )
            for name, constraint in alts.items())

    item_constraints: List[ItemConstraintData] = []

    valid_keys = set(('item','from_location','to_location','entry_prereq','exit_prereq','alternate_entries','alternate_exits'))
    for cdict in cdicts:
        if not valid_keys.issuperset(cdict.keys()): fail('Unknown keys in item constraint: \n' + str(cdict))
        item, from_location = cdict['item'], cdict['from_location']
        if not settings.shuffle_gift_items and item in shufflable_gift_items_set: continue
        if item not in items_set: fail('Unknown item: %s' % item)
        if from_location not in locations_set: fail('Unknown location: %s' % from_location)

        item_constraints.append(ItemConstraintData(
            item = item,
            from_location = from_location,
            entry_prereq = parse_expression(cdict['entry_prereq'], variable_names_set, default_expressions),
            exit_prereq = parse_expression(cdict['exit_prereq'], variable_names_set, default_expressions),
            alternate_entries = parse_alternates(cdict.get('alternate_entries')),
            alternate_exits = parse_alternates(cdict.get('alternate_exits')),
        ))

    # Validate that there are no duplicate items defined
    if len(cdicts) != len(set(cdict['item'] for cdict in cdicts)):
        # Error: duplicate item. Find the duplicate item.
        item_names = [cdict['item'] for cdict in cdicts]
        duplicates = [item for item in set(item_names) if item_names.count(item) > 1]
        fail('Duplicate item definition(s) in constraints!\n%s' % '\n'.join(duplicates))

    return item_constraints

# AP Change: Use os.path.join
DIR_TEMPLATE_PATCH_FILES = os.path.join('existing_randomizer', 'maptemplates', 'constraint_shuffle')

def parse_template_constraints(settings, locations_set, variable_names_set, default_expressions, edge_constraints):
    # AP Change: Use pkgutil to read file from .apworld
    template_constraints = os.path.join('existing_randomizer', 'maptemplates', 'template_constraints.txt')
    lines = read_file_and_strip_comments(template_constraints)
    if settings.shuffle_start_location:
        start_rando_template_constraints = os.path.join('existing_randomizer', 'maptemplates', 'start_rando_template_constraints.txt')
        lines += read_file_and_strip_comments(start_rando_template_constraints)
    jsondata = ' '.join(lines)
    jsondata = re.sub(r',\s*}', '}', jsondata)
    jsondata = '},{'.join(re.split(r'}\s*{', jsondata))
    jsondata = '[' + jsondata + ']'

    cdicts = parse_json(jsondata)

    
    # AP Change: Use pkg_resources to read directory contents from .apworld
    patch_files = resource_listdir(DIR_TEMPLATE_PATCH_FILES)
    patch_names = []
    for patch_file in patch_files:
        if not patch_file.startswith('CS_'): fail('Patch file %s does not start with CS_' % patch_file)
        patch_name = patch_file[len('CS_'):patch_file.rfind('.')]
        patch_names.append(patch_name)
    name_to_patch_file = dict(zip(patch_names, patch_files))

    original_prereqs = dict(((e.from_location, e.to_location), e.prereq_expression) for e in edge_constraints)

    def parse_change(change):
        from_location, to_location = (x.strip() for x in change['edge'].split('->'))
        if from_location not in locations_set: fail('Unknown location: %s' % from_location)
        if to_location not in locations_set: fail('Unknown location: %s' % to_location)
        current_expression = original_prereqs[(from_location, to_location)]
        prereq = parse_expression(change['prereq'], variable_names_set, default_expressions, current_expression)
        return EdgeConstraintData(from_location, to_location, prereq)

    template_constraints = []
    for cdict in cdicts:
        name = cdict['name']
        if name not in name_to_patch_file: fail('Unknown template constraint %s' % name)
        weight = int(cdict['weight'])
        changes = [parse_change(change) for change in cdict['changes']]

        template_constraints.append(TemplateConstraintData(
            name=name,
            weight=weight,
            template_file=os.path.join(DIR_TEMPLATE_PATCH_FILES, name_to_patch_file[name]),
            changes=changes,
        ))
    template_constraints.sort(key=lambda tc:tc.name)

    for src_t in template_constraints:
        for cmp_t in template_constraints:
            if src_t.conflicts_with(cmp_t):
                src_t.conflicts_names.append(cmp_t.name)
    return template_constraints


def read_config(default_setting_flags, item_locations_set, shufflable_gift_items_set, config_flags_set, predefined_additional_items_set, settings):
    lines = read_file_and_strip_comments(settings.config_file)
    jsondata = ' '.join(lines)
    jsondata = re.sub(r',\s*]', ']', jsondata)
    jsondata = re.sub(r',\s*}', '}', jsondata)
    jsondata = re.sub(r'\],\s*$', ']', jsondata)
    config_dict = parse_json('{' + jsondata + '}')

    knowledge = "BASIC"
    difficulty = "NORMAL"
    included_additional_items = list()
    must_be_reachable = set()
    config_settings = dict()

    if 'to_shuffle' not in config_dict:
        fail('Missing "to_shuffle" in config')
    to_shuffle = set(config_dict['to_shuffle'])
    if 'must_be_reachable' in config_dict:
        must_be_reachable = set(config_dict['must_be_reachable'])
    if 'additional_items' in config_dict:
        included_additional_items = config_dict['additional_items']
    if 'settings' in config_dict:
        config_settings = config_dict['settings']
    if 'knowledge' in config_dict:
        knowledge = config_dict['knowledge']
    if 'trick_difficulty' in config_dict:
        difficulty = config_dict['trick_difficulty']

    # AP Change: Replace config file with player options
    if hasattr(settings, 'ap_options'):
        ap_options: RabiRibiOptions = settings.ap_options
        read_ap_config_settings(config_settings, ap_options)
        knowledge_options = ['BASIC', 'INTERMEDIATE', 'ADVANCED', 'OBSCURE']
        knowledge = knowledge_options[ap_options.knowledge.value]
        difficulty_options = ['NORMAL', 'HARD', 'V_HARD', 'EXTREME', 'STUPID']
        difficulty = difficulty_options[ap_options.trick_difficulty.value]
    if settings.shuffle_gift_items:
        included_additional_items = [item_name for item_name in included_additional_items if not item_name in shufflable_gift_items_set]
    else:
        to_shuffle -= shufflable_gift_items_set
        must_be_reachable -= shufflable_gift_items_set

    # Settings
    setting_flags = dict(default_setting_flags)
    for key, value in config_settings.items():
        if key not in config_flags_set:
            fail('Undefined flag: %s' % key)
        if not type(value) is bool:
            fail('Flag %s does not map to a boolean variable in config' % key)
        setting_flags[key] = value

    # Knowledge
    if knowledge == 'BASIC':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = False
        setting_flags[KNOWLEDGE_ADVANCED] = False
        setting_flags[KNOWLEDGE_OBSCURE] = False
    elif knowledge == 'INTERMEDIATE':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = True
        setting_flags[KNOWLEDGE_ADVANCED] = False
        setting_flags[KNOWLEDGE_OBSCURE] = False
    elif knowledge == 'ADVANCED':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = True
        setting_flags[KNOWLEDGE_ADVANCED] = True
        setting_flags[KNOWLEDGE_OBSCURE] = False
    elif knowledge == 'OBSCURE':
        setting_flags[KNOWLEDGE_INTERMEDIATE] = True
        setting_flags[KNOWLEDGE_ADVANCED] = True
        setting_flags[KNOWLEDGE_OBSCURE] = True
    else:
        fail('Unknown knowledge level: %s. Either BASIC, INTERMEDIATE, ADVANCED or OBSCURE.' % knowledge)

    # Difficulty
    if difficulty == 'NORMAL':
        setting_flags[DIFFICULTY_HARD] = False
        setting_flags[DIFFICULTY_V_HARD] = False
        setting_flags[DIFFICULTY_EXTREME] = False
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'HARD':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = False
        setting_flags[DIFFICULTY_EXTREME] = False
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'V_HARD':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = True
        setting_flags[DIFFICULTY_EXTREME] = False
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'EXTREME':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = True
        setting_flags[DIFFICULTY_EXTREME] = True
        setting_flags[DIFFICULTY_STUPID] = False
    elif difficulty == 'STUPID':
        setting_flags[DIFFICULTY_HARD] = True
        setting_flags[DIFFICULTY_V_HARD] = True
        setting_flags[DIFFICULTY_EXTREME] = True
        setting_flags[DIFFICULTY_STUPID] = True
    else:
        fail('Unknown difficulty level: %s. Either NORMAL, HARD, V_HARD, EXTREME or STUPID.' % difficulty)

    if set(included_additional_items) - predefined_additional_items_set:
        fail('\n'.join([
            'Unknown additional items defined:',
            '\n'.join(map(str, set(included_additional_items) - predefined_additional_items_set)),
        ]))

    if to_shuffle - item_locations_set:
        fail('\n'.join([
            'Unknown items defined in config:',
            '\n'.join(map(str, to_shuffle - item_locations_set)),
        ]))

    if must_be_reachable - item_locations_set:
        fail('\n'.join([
            'Unknown items defined in config:',
            '\n'.join(map(str, must_be_reachable - item_locations_set)),
        ]))

    config_data = ConfigData(
        knowledge=knowledge,
        difficulty=difficulty,
        settings=config_settings,
    )

    return setting_flags, sorted(list(to_shuffle)), must_be_reachable, included_additional_items, config_data

# AP Change: Added method to read config data from player options
def read_ap_config_settings(config_settings, ap_options):
    """Updates the default configuration settings with the player options from Archipelago."""
    config_settings['DARKNESS_WITHOUT_LIGHT_ORB'] = bool(ap_options.darkness_without_light_orb.value)
    config_settings['UNDERWATER_WITHOUT_WATER_ORB'] = bool(ap_options.underwater_without_water_orb.value)
    config_settings['EXPLOSIVES_WITH_CARROT_SHOOTER'] = bool(ap_options.carrot_shooter_in_logic.value)
    config_settings['ZIP_REQUIRED'] = bool(ap_options.zips_required.value)
    config_settings['SEMISOLID_CLIPS_REQUIRED'] = bool(ap_options.semi_solid_clips_required.value)
    config_settings['BLOCK_CLIPS_REQUIRED'] = bool(ap_options.block_clips_required.value)
    config_settings['PLURKWOOD_REACHABLE'] = bool(ap_options.include_plurkwood.value)
    config_settings['WARP_DESTINATION_REACHABLE'] = bool(ap_options.include_warp_destination.value)
    config_settings['POST_GAME_ALLOWED'] = bool(ap_options.include_post_game.value)
    config_settings['POST_IRISU_ALLOWED'] = bool(ap_options.include_post_irisu.value)
    config_settings['HALLOWEEN_REACHABLE'] = bool(ap_options.include_halloween.value)
    config_settings['EVENT_WARPS_REQUIRED'] = bool(ap_options.event_warps_in_logic.value)

def parse_item_from_string(line):
    pos, areaid, itemid, name = (s.strip() for s in line.split(':', 3))
    name = name if (len(name) > 0 and name != 'None') else None
    item = Item(ast.literal_eval(pos), int(areaid), int(itemid), name)
    return item

class RandomizerData(object):
    # Attributes:
    #
    # Raw Information
    #
    # dict: setting_flags   (setting_name -> bool)
    # dict: pseudo_items   (psuedo_item_name -> condition)
    # dict: additional_items   (item_name -> item_id)
    # dict: locations   (location -> location_type)
    # list: items   (Item objects)
    # dict: alternate_conditions   (item_name -> constraint lambda)
    # list: edge_constraints   (EdgeConstraintData objects)
    # list: item_constraints   (ItemConstraintData objects)
    # list: map_transitions   (MapTransition objects)
    # list: start_locations   (StartLocation objects)
    #
    # obj: config_data  (ConfigData object. Used for analysis printing, not used in generation.)
    #
    # Intermediate Information
    #
    # list: item_names
    # list: location_list
    # set: locations_set
    #
    #
    # Preprocessed - Based on settings
    #
    # dict: configured_variables        (variable_name -> value)
    # dict: pessimistic_variables        (variable_name -> value)
    # list: graph_vertices           (list(node_name))
    # dict: item_locations_in_node   (node_name -> list(item_name))
    # list: initial_edges             (edge_id -> GraphEdge)
    # dict: initial_outgoing_edges     (node_name -> list(edge_id))
    # dict: initial_incoming_edges     (node_name -> list(edge_id))
    #
    #
    # Preprocessed Information
    #
    # list: items_to_allocate
    # dict: edge_progression (variable_name -> set(edge_id))
    #
    # list: walking_left_transitions
    # list: walking_right_transitions
    #
    # int: nLocations
    # int: nNormalItems
    # int: nAdditionalItems
    # int: originalNEggs
    # int: nEggs


    def __init__(self, settings):
        self.default_config_flags = define_config_flags()
        self.pessimistic_config_flags = dict((key, False) for key in self.default_config_flags.keys())

        self.default_setting_flags = define_setting_flags(settings)
        self.pessimistic_setting_flags = dict(self.default_setting_flags)

        self.default_setting_flags.update(self.default_config_flags)
        self.pessimistic_setting_flags.update(self.pessimistic_config_flags)

        self.pseudo_items = define_pseudo_items()
        self.locations, self.map_transitions, self.items, self.all_additional_items, self.shufflable_gift_items, self.start_locations = parse_locations_and_items()
        self.additional_items = dict(self.all_additional_items)

        self.gift_item_map_modifications = shufflable_gift_item_map_modifications()
        self.default_map_modifications = []
        if settings.shuffle_gift_items:
            self.items += self.shufflable_gift_items
            self.default_map_modifications += self.gift_item_map_modifications
            for item in self.shufflable_gift_items:
                del self.additional_items[item.name]
        shufflable_gift_items_set = set(item.name for item in self.shufflable_gift_items)

        self.nHardToReach = settings.num_hard_to_reach

        # Do some preprocessing of variable names
        self.item_names = [item.name for item in self.items]
        self.location_list = sorted(list(self.locations.keys()))
        self.variable_names_list = self.location_list + \
                                   self.item_names + \
                                   list(self.additional_items.keys()) + \
                                   list(self.pseudo_items.keys()) + \
                                   list(self.default_setting_flags.keys())
        self.variable_names_list.sort()

        variable_names_set = set(self.variable_names_list)
        if len(variable_names_set) < len(self.variable_names_list):
            # Repeats detected! Fail.
            repeat_names = [x for x in variable_names_set if self.variable_names_list.count(x) > 1]
            fail('Repeat names detected: %s' % ','.join(repeat_names))

        self.locations_set = set(self.location_list)
        items_set = set(self.item_names)

        # More config loading
        config_flags_set = set(self.default_config_flags.keys())
        self.configured_setting_flags, self.to_shuffle, self.must_be_reachable, self.included_additional_items, self.config_data = \
            read_config(self.default_setting_flags, items_set, shufflable_gift_items_set, config_flags_set, set(self.all_additional_items.keys()), settings)

        default_expressions = define_default_expressions(variable_names_set)
        evaluate_pseudo_item_constraints(self.pseudo_items, variable_names_set, default_expressions)
        self.alternate_conditions = define_alternate_conditions(settings, variable_names_set, default_expressions)
        self.edge_constraints = parse_edge_constraints(self.locations_set, variable_names_set, default_expressions)
        self.item_constraints = parse_item_constraints(settings, items_set, shufflable_gift_items_set, self.locations_set, variable_names_set, default_expressions)
        self.template_constraints = parse_template_constraints(settings, self.locations_set, variable_names_set, default_expressions, self.edge_constraints)

        self.preprocess_data(settings)
        self.preprocess_variables(settings)
        self.preprocess_graph(settings)

        self.preprocess_backward_reachable(settings)
        self.preprocess_template_constraints(settings)

    def preprocess_variables_with_settings(self, setting_flags, settings):
        # Mark all unconstrained pseudo-items
        variables: Dict[str, bool] = dict((name, False) for name in self.variable_names_list)
        variables.update(setting_flags)

        to_remove = set()
        unreached_pseudo_items = dict()
        has_changes = True
        while has_changes:
            has_changes = False
            to_remove.clear()
            for target, condition in unreached_pseudo_items.items():
                if condition(variables):
                    variables[target] = True
                    to_remove.add(target)
                    has_changes = True

            for target in to_remove:
                del unreached_pseudo_items[target]

        return variables

    def preprocess_variables(self, settings):
        self.configured_variables = self.preprocess_variables_with_settings(self.configured_setting_flags, settings)
        self.pessimistic_variables = self.preprocess_variables_with_settings(self.pessimistic_setting_flags, settings)

    def preprocess_graph(self, settings):
        pessimistic_variables = self.pessimistic_variables

        # Partial Graph Construction
        graph_vertices = list(self.location_list)
        item_locations_in_node = dict((node, []) for node in graph_vertices)

        edges = []
        for item_constraint in self.item_constraints:
            if item_constraint.no_alternate_paths and \
                    item_constraint.entry_prereq.expression_lambda(pessimistic_variables) and \
                    item_constraint.exit_prereq.expression_lambda(pessimistic_variables):
                # Unconstrained - Merge directly into from_location
                item_locations_in_node[item_constraint.from_location].append(item_constraint.item)
            else:
                # Constrained - Create new node
                item_node_name = 'ITEM_%s' % item_constraint.item
                graph_vertices.append(item_node_name)
                item_locations_in_node[item_node_name] = [item_constraint.item]

                edges.append(GraphEdge(
                    edge_id=len(edges),
                    from_location=item_constraint.from_location,
                    to_location=item_node_name,
                    constraint=item_constraint.entry_prereq.expression_lambda,
                    constraint_expr=item_constraint.entry_prereq.expression,
                    progression=item_constraint.entry_progression,
                    backtrack_cost=0,
                ))

                edges.append(GraphEdge(
                    edge_id=len(edges),
                    from_location=item_node_name,
                    to_location=item_constraint.from_location,
                    constraint=item_constraint.exit_prereq.expression_lambda,
                    constraint_expr=item_constraint.exit_prereq.expression,
                    progression=item_constraint.exit_progression,
                    backtrack_cost=0,
                ))

                for entry_node, expression_data in item_constraint.alternate_entries.items():
                    edges.append(GraphEdge(
                        edge_id=len(edges),
                        from_location=entry_node,
                        to_location=item_node_name,
                        constraint=expression_data.exp_lambda,
                        constraint_expr=expression_data.exp,
                        progression=expression_data.exp_literals,
                        backtrack_cost=1,
                    ))

                for exit_node, expression_data in item_constraint.alternate_exits.items():
                    edges.append(GraphEdge(
                        edge_id=len(edges),
                        from_location=item_node_name,
                        to_location=exit_node,
                        constraint=expression_data.exp_lambda,
                        constraint_expr=expression_data.exp,
                        progression=expression_data.exp_literals,
                        backtrack_cost=1,
                    ))

        # check all replacement potencial nodes
        replacement_edges = set(
            (change.from_location, change.to_location)
            for t in self.template_constraints
            for change in t.changes
        )

        # marge non-replacement potencial nodes into initial_edges
        edge_constraints = self.edge_constraints
        sifted_edge_constraints = []
        for graph_edge in edge_constraints:
            if (graph_edge.from_location, graph_edge.to_location) not in replacement_edges:
                edges.append(GraphEdge(
                    edge_id=len(edges),
                    from_location=graph_edge.from_location,
                    to_location=graph_edge.to_location,
                    constraint=graph_edge.prereq_lambda,
                    constraint_expr=graph_edge.prereq_expression,
                    progression=graph_edge.prereq_literals,
                    backtrack_cost=1,
                ))
            else:
                sifted_edge_constraints.append(graph_edge)
        self.edge_constraints = sifted_edge_constraints

        # replacement potencial nodes
        self.replacement_edges_id = len(edges)
        for graph_edge in sifted_edge_constraints:
            edges.append(GraphEdge(
                edge_id=len(edges),
                from_location=graph_edge.from_location,
                to_location=graph_edge.to_location,
                constraint=graph_edge.prereq_lambda,
                constraint_expr=graph_edge.prereq_expression,
                backtrack_cost=1,
            ))

        initial_outgoing_edges = dict((node, []) for node in graph_vertices)
        initial_incoming_edges = dict((node, []) for node in graph_vertices)

        for edge in edges:
            initial_outgoing_edges[edge.from_location].append(edge.edge_id)
            initial_incoming_edges[edge.to_location].append(edge.edge_id)

        # map transition nodes
        self.transition_edges_id = len(edges)
        for rtr, ltr in zip(self.walking_right_transitions, self.walking_left_transitions):
            edge1 = GraphEdge(
                edge_id=len(edges),
                from_location=rtr.origin_location,
                to_location=ltr.origin_location,
                constraint=NO_CONDITIONS,
                constraint_expr=OpLit('TRUE'),
                backtrack_cost=INFTY,
            )
            edge2 = GraphEdge(
                edge_id=len(edges)+1,
                from_location=ltr.origin_location,
                to_location=rtr.origin_location,
                constraint=NO_CONDITIONS,
                constraint_expr=OpLit('TRUE'),
                backtrack_cost=INFTY,
            )
            edges.append(edge1)
            edges.append(edge2)

        self.graph_vertices = graph_vertices
        self.item_locations_in_node = item_locations_in_node
        self.initial_edges = edges
        self.initial_outgoing_edges = initial_outgoing_edges
        self.initial_incoming_edges = initial_incoming_edges
        self.edge_progression = generate_progression_dict(self.variable_names_list, edges, keep_progression=False)

    def preprocess_data(self, settings):
        ### For item shuffle
        to_shuffle_set = set(self.to_shuffle)
        do_not_shuffle = [item.name for item in self.items if not item.name in to_shuffle_set]

        items_to_shuffle = [item_name for item_name in self.to_shuffle if not is_egg(item_name)]
        unshuffled_items = [item_name for item_name in do_not_shuffle if not is_egg(item_name)]

        eggs_to_shuffle = [item_name for item_name in self.to_shuffle if is_egg(item_name)]
        unshuffled_eggs = [item_name for item_name in do_not_shuffle if is_egg(item_name)]

        self.nItemSpots = len(self.to_shuffle)
        self.nNormalItems = len(items_to_shuffle)
        self.nAdditionalItems = len(self.included_additional_items)
        self.nOriginalEggs = len(eggs_to_shuffle)


        # Remove eggs so that number of items to allocate == number of locations
        self.nEggs = self.nOriginalEggs - self.nAdditionalItems
        if self.nEggs < 0:
            fail('Too few eggs to remove to make room for additional items.')

        self.items_to_allocate = items_to_shuffle + self.included_additional_items + eggs_to_shuffle[:self.nEggs]
        self.item_slots = items_to_shuffle + eggs_to_shuffle
        self.unshuffled_allocations = list(zip(unshuffled_items, unshuffled_items))
        if settings.egg_goals:
            minShuffledEggs = self.nHardToReach + settings.extra_eggs
            if self.nEggs < minShuffledEggs:
                fail('Not enough shuffled eggs for egg goals. Needs at least %d.' % minShuffledEggs)
            self.unshuffled_allocations += [(egg_loc, None) for egg_loc in unshuffled_eggs]
        else:
            self.unshuffled_allocations += list(zip(unshuffled_eggs, unshuffled_eggs))

        # map_transitions
        walking_right_transitions = [tr for tr in self.map_transitions if tr.walking_right]
        walking_right_transitions.sort(key=lambda tr : (tr.origin_location, tr.rect))
        walking_left_transitions = []

        left_transition_dict = dict(( (tr.area_current, tr.entry_current), tr )
            for tr in self.map_transitions if not tr.walking_right)

        for rtr in walking_right_transitions:
            key = (rtr.area_target, rtr.entry_target)
            ltr = left_transition_dict.get(key)
            if ltr == None:
                fail('Matching map transition not found for %s' % rtr.origin_location)
                break
            if rtr.area_current != ltr.area_target or rtr.entry_current != ltr.entry_target:
                fail("Map transitions don't match! %s vs %s" % (rtr.origin_location, ltr.origin_location))
                break
            walking_left_transitions.append(ltr)
            del left_transition_dict[key]

        for ltr in left_transition_dict.values():
            fail('Matching map transition not found for %s' % ltr.origin_location)

        self.walking_right_transitions = walking_right_transitions
        self.walking_left_transitions = walking_left_transitions


    def generate_variables(self):
        return dict(self.configured_variables)

    def generate_pessimistic_variables(self):
        return dict(self.pessimistic_variables)

    def preprocess_backward_reachable(self, settings):
        variables = self.generate_variables()
        edges = self.initial_edges

        outgoing_edges = dict((key, list(edge_ids)) for key, edge_ids in self.initial_outgoing_edges.items())
        incoming_edges = dict((key, list(edge_ids)) for key, edge_ids in self.initial_incoming_edges.items())

        for edge in edges[self.transition_edges_id:]:
            outgoing_edges[edge.from_location].append(edge.edge_id)
            incoming_edges[edge.to_location].append(edge.edge_id)

        dynamic_edges_id = self.replacement_edges_id
        if(settings.constraint_changes <= 0 and
           settings.min_constraint_changes <= 0 and
           settings.max_constraint_changes <= 0):
            dynamic_edges_id = self.transition_edges_id
            if not settings.shuffle_map_transitions:
                dynamic_edges_id = len(edges)

        dfs_stack = [location for location, loc_type in self.locations.items() if loc_type == LOCATION_WARP]
        visited = set(dfs_stack)
        pending_edges = dict()

        while len(dfs_stack) > 0:
            current_dest = dfs_stack.pop()
            for edge_id in incoming_edges[current_dest]:
                target_src = edges[edge_id].from_location
                if edge_id >= dynamic_edges_id:
                        if current_dest not in pending_edges:
                            pending_edges[current_dest] = []
                        pending_edges[current_dest].append(edge_id)
                else:
                    if target_src in visited: continue
                    if edges[edge_id].satisfied(variables):
                        visited.add(target_src)
                        dfs_stack.append(target_src)

        pending_stack = set()
        for current_dest, from_edges in pending_edges.items():
            resolved = True
            for edge_id in from_edges:
                if edge_id >= self.transition_edges_id:
                    resolved = False
                    break
                target_src = edges[edge_id].from_location
                if target_src not in visited:
                    resolved = False
                    break
            if not resolved:
                pending_stack.add(current_dest)

        traversable_edges = set()
        backward_frontier = set()
        pending_static_edges = [False for _ in range(dynamic_edges_id)]
        for edge_id in range(dynamic_edges_id):
                edge = edges[edge_id]
                if edge.satisfied(variables):
                    traversable_edges.add(edge_id)
                    if edge.to_location in visited:
                        backward_frontier.add(edge.to_location)
                    if edge.from_location not in visited:
                        pending_static_edges[edge_id] = True


        self.initial_visited_edges = visited
        self.initial_pending_stack = list(sorted(pending_stack))
        self.initial_backward_frontier = backward_frontier
        self.initial_traversable_edges = traversable_edges
        self.initial_untraversable_edges = set(edge.edge_id for edge in edges) - traversable_edges
        self.pending_static_edges = pending_static_edges
        self.dynamic_edges_id = dynamic_edges_id

    def preprocess_template_constraints(self, settings):
        initial_template_index = dict()
        initial_template_weights = list()
        templates = self.template_constraints
        total_weight = 0
        for i in range(len(templates)):
            t = templates[i]
            total_weight += t.weight
            initial_template_index[t.name] = i
            initial_template_weights.append(total_weight)

        self.initial_template_index = initial_template_index
        self.initial_template_weights = initial_template_weights

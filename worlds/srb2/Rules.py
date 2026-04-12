from typing import Callable, Union, Dict, Set

from BaseClasses import MultiWorld, CollectionState
from ..generic.Rules import add_rule, set_rule
from .Locations import location_table
from .Options import SRB2Options
from .Regions import connect_regions, SRB2Zones
from .Items import character_item_data_table
from .Items import zones_item_data_table

def shuffle_dict_keys(world, dictionary: dict) -> dict:
    keys = list(dictionary.keys())
    values = list(dictionary.values())
    world.random.shuffle(keys)
    return dict(zip(keys, values))

def fix_reg(entrance_map: Dict[SRB2Zones, str], entrance: SRB2Zones, invalid_regions: Set[str],
            swapdict: Dict[SRB2Zones, str], world):
    if entrance_map[entrance] in invalid_regions: # Unlucky :C
        replacement_regions = [(rand_entrance, rand_region) for rand_entrance, rand_region in swapdict.items()
                               if rand_region not in invalid_regions]
        rand_entrance, rand_region = world.random.choice(replacement_regions)
        old_dest = entrance_map[entrance]
        entrance_map[entrance], entrance_map[rand_entrance] = rand_region, old_dest
        swapdict[entrance], swapdict[rand_entrance] = rand_region, old_dest
    swapdict.pop(entrance)









#can_break_weak_walls
#can_break_strong_walls
#can_break_floors
#can_pound_springs
#can_climb_walls
#can_break_spikes
#can_fit_under_roll_gaps
#can_generate_speed (spindash)
#jump_height_includes_flying
#makes_hard_stages_easy

#jump_height
#hover_length





def set_rules(world, options: SRB2Options, player: int, area_connections: dict, move_rando_bitvec: int):

    #set up info array
    character_info = {'Sonic': [100,'weak_walls','spin_walls', 'fits_under_gaps','instant_speed',"midair_speed","roll","badnik_bounce",'can_use_shields',"can_spindash"],
                      'Tails': [1500,'weak_walls','spin_walls', 'fits_under_gaps','instant_speed',"roll", 'free_flyer','makes_stages_easy','soft_jump',"badnik_bounce",'can_use_shields',"can_spindash"],
                      'Knuckles': [80,'weak_walls','spin_walls','strong_walls','climbs_walls', 'fits_under_gaps','instant_speed',"roll",'low_grav',"midair_speed",'soft_jump',"badnik_bounce",'can_use_shields',"can_spindash"],
                      'Amy': [115,'weak_walls','spin_walls', 'strong_walls', 'strong_floors', 'breaks_spikes', 'pounds_springs','soft_jump',"badnik_bounce",'can_use_shields','attacks_though_thin_walls'],
                      'Fang': [200,'strong_floors','lava_immune','soft_jump','downward_projectile','can_use_shields','attacks_though_thin_walls'],
                      'Metal Sonic': [100,'weak_walls','spin_walls', 'fits_under_gaps','instant_speed',"can_hover",'breaks_spikes',"roll",'soft_jump','makes_stages_easy',"badnik_bounce",'can_use_shields',"can_spindash"],
                      }
#tag descriptions:
    #jump_height
    #weak_walls (fhz ice)
    #spin_walls (dsz2 heart emblem wall)
    #strong_walls (most knuckles paths)
    #stronger_walls (ACZ2 minecart doors)
    #strong_floors (most nospin paths)
    #roll (can get momentum from slopes)
    #fits_under_gaps (most spin path gaps)
    #instant_speed (usually spindash, used when you need speed for a slope jump or momentum with little space)
    #midair_speed (instant speed but can be done faster/ midair, ie sonic's thok)
    #free_flyer (jump height includes being able to fly or a double jump that can get under things)
    #climbs_walls (only needs 1 wall to get to the top)
    #wall_jump (can use 2 walls to scale them, ie mario's wall jump)
    #low_grav (cez2 diamond emblem bullshit)
    #breaks_spikes
    #pounds_springs (extra height from hitting springs, such as amy's hammer)
    #can_spindash (dsz2 spindash switches)
    #can_use_shields (for active shield abilities)
    #soft_jump (can stand on monitors/tnt barrels by jumping/using their ability)
    #can_stomp (elemental shield replacement)
    #skims_water
    #lava_immune
    #insane_speed (dsz1 fast door)
    #downward_projectile (able to break monitors in shallow bouyant slime, ie fangs popgun)
    #shoots_player_blockers (able to break monitors through exclusively player blocking linedefs)#not implemented because fuck that
    # attacks_though_thin_walls (acz2 monitors near heart emblem can be broken by fangs popgun & amy's hammer)


    def char_needs_tags(state: CollectionState,tag_list,jump_height):
        for i in character_info:
            if state.has(i,player):
                if i == "Metal Sonic":
                    if state.count("Chaos Emerald", player) > 6 and "insane_speed" not in character_info[i]:
                        character_info[i].append("insane_speed")
                        character_info[i][0] = 200
                if i == "Sonic":
                    if state.count("Chaos Emerald", player) > 6 and "can_hover" not in character_info[i]:
                        character_info[i].append("can_hover")
                        character_info[i][0] = 200

                if character_info[i][0] < jump_height:
                    continue
                if set(tag_list).issubset(character_info[i]):
                    return True
        return False


    rf = RuleFactory(world, options, player, move_rando_bitvec)

    connect_regions(world, player, "Menu", "Greenflower Zone 1", lambda state: state.has("Greenflower Zone", player) or state.has("Greenflower Zone (Act 1)", player))
    connect_regions(world, player, "Menu", "Greenflower Zone 2", lambda state: state.has("Greenflower Zone", player) or state.has("Greenflower Zone (Act 2)", player))
    connect_regions(world, player, "Menu", "Greenflower Zone 3", lambda state: state.has("Greenflower Zone", player) or state.has("Greenflower Zone (Act 3)", player))

    connect_regions(world, player, "Menu", "Techno Hill Zone 1", lambda state: state.has("Techno Hill Zone", player) or state.has("Techno Hill Zone (Act 1)", player))
    connect_regions(world, player, "Menu", "Techno Hill Zone 2", lambda state: state.has("Techno Hill Zone", player) or state.has("Techno Hill Zone (Act 2)", player))
    connect_regions(world, player, "Menu", "Techno Hill Zone 3", lambda state: state.has("Techno Hill Zone", player) or state.has("Techno Hill Zone (Act 3)", player))

    connect_regions(world, player, "Techno Hill Zone 2", "Techno Hill Zone 2 Main",lambda state: state.has("Buoyant Slime", player))

    connect_regions(world, player, "Menu", "Deep Sea Zone 1", lambda state: state.has("Deep Sea Zone", player) or state.has("Deep Sea Zone (Act 1)", player))
    connect_regions(world, player, "Menu", "Deep Sea Zone 2", lambda state: state.has("Deep Sea Zone", player) or state.has("Deep Sea Zone (Act 2)", player))
    connect_regions(world, player, "Menu", "Deep Sea Zone 3", lambda state: state.has("Deep Sea Zone", player) or state.has("Deep Sea Zone (Act 3)", player))

    connect_regions(world, player, "Menu", "Castle Eggman Zone 1", lambda state: state.has("Castle Eggman Zone", player) or state.has("Castle Eggman Zone (Act 1)", player))
    connect_regions(world, player, "Menu", "Castle Eggman Zone 2", lambda state: state.has("Castle Eggman Zone", player) or state.has("Castle Eggman Zone (Act 2)", player))
    connect_regions(world, player, "Menu", "Castle Eggman Zone 3", lambda state: state.has("Castle Eggman Zone", player) or state.has("Castle Eggman Zone (Act 3)", player))

    connect_regions(world, player, "Menu", "Arid Canyon Zone 1", lambda state: state.has("Arid Canyon Zone", player) or state.has("Arid Canyon Zone (Act 1)", player))
    connect_regions(world, player, "Menu", "Arid Canyon Zone 2", lambda state: state.has("Arid Canyon Zone", player) or state.has("Arid Canyon Zone (Act 2)", player))
    connect_regions(world, player, "Menu", "Arid Canyon Zone 3", lambda state: state.has("Arid Canyon Zone", player) or state.has("Arid Canyon Zone (Act 3)", player))

    connect_regions(world, player, "Menu", "Red Volcano Zone 1", lambda state: state.has("Red Volcano Zone", player) or state.has("Red Volcano Zone (Act 1)", player))

    connect_regions(world, player, "Menu", "Egg Rock Zone 1", lambda state: state.has("Egg Rock Zone", player) or state.has("Egg Rock Zone (Act 1)", player))
    connect_regions(world, player, "Menu", "Egg Rock Zone 2", lambda state: state.has("Egg Rock Zone", player) or state.has("Egg Rock Zone (Act 2)", player))

    if options.bcz_emblem_percent==0:
        connect_regions(world, player, "Menu", "Black Core Zone 1", lambda state: state.has("Black Core Zone", player) or state.has("Black Core Zone (Act 1)", player))
        connect_regions(world, player, "Menu", "Black Core Zone 2", lambda state: state.has("Black Core Zone", player) or state.has("Black Core Zone (Act 2)", player))
        connect_regions(world, player, "Menu", "Black Core Zone 3", lambda state: state.has("Black Core Zone", player) or state.has("Black Core Zone (Act 3)", player))
    else:
        if options.actsanity:
            connect_regions(world, player, "Menu", "Black Core Zone 1", lambda state: state.has("Black Core Zone", player) or state.has("Black Core Zone (Act 1)", player))
            connect_regions(world, player, "Menu", "Black Core Zone 2", lambda state: state.has("Black Core Zone", player) or state.has("Black Core Zone (Act 2)", player))
        else:
            connect_regions(world, player, "Menu", "Black Core Zone 1", lambda state: state.has("Emblem", player, options.bcz_emblem_percent))
            connect_regions(world, player, "Menu", "Black Core Zone 2", lambda state: state.has("Emblem", player, options.bcz_emblem_percent))

        connect_regions(world, player, "Menu", "Black Core Zone 3", lambda state: state.has("Emblem", player, options.bcz_emblem_percent))

    connect_regions(world, player, "Black Core Zone 3", "Credits",lambda state: state.count("Chaos Emerald", player) > 6)

#todo re add credits as a region
    #fix dsz and atz chaos emerald locations
    #all time/ring emblems must use can_reach(zone clear)

    connect_regions(world, player, "Menu", "Frozen Hillside Zone", lambda state: state.has("Frozen Hillside Zone", player))
    connect_regions(world, player, "Menu", "Pipe Towers Zone", lambda state: state.has("Pipe Towers Zone", player))
    connect_regions(world, player, "Menu", "Forest Fortress Zone", lambda state: state.has("Forest Fortress Zone", player))
    connect_regions(world, player, "Menu", "Final Demo Zone", lambda state: state.has("Final Demo Zone", player))
    connect_regions(world, player, "Menu", "Haunted Heights Zone", lambda state: state.has("Haunted Heights Zone", player))
    connect_regions(world, player, "Menu", "Aerial Garden Zone", lambda state: state.has("Aerial Garden Zone", player))
    connect_regions(world, player, "Menu", "Azure Temple Zone", lambda state: state.has("Azure Temple Zone", player))
    if options.nights_maps:
        connect_regions(world, player, "Menu", "Floral Field Zone", lambda state: state.has("Floral Field Zone", player))
        connect_regions(world, player, "Menu", "Toxic Plateau Zone", lambda state: state.has("Toxic Plateau Zone", player))
        connect_regions(world, player, "Menu", "Flooded Cove Zone", lambda state: state.has("Flooded Cove Zone", player))
        connect_regions(world, player, "Menu", "Cavern Fortress Zone", lambda state: state.has("Cavern Fortress Zone", player))
        connect_regions(world, player, "Menu", "Dusty Wasteland Zone", lambda state: state.has("Dusty Wasteland Zone", player))
        connect_regions(world, player, "Menu", "Magma Caves Zone", lambda state: state.has("Magma Caves Zone", player))
        connect_regions(world, player, "Menu", "Egg Satellite Zone", lambda state: state.has("Egg Satellite Zone", player))
        connect_regions(world, player, "Menu", "Black Hole Zone", lambda state: state.has("Black Hole Zone", player))
        connect_regions(world, player, "Menu", "Christmas Chime Zone", lambda state: state.has("Christmas Chime Zone", player))
        connect_regions(world, player, "Menu", "Dream Hill Zone", lambda state: state.has("Dream Hill Zone", player))


        connect_regions(world, player, "Menu", "Alpine Paradise Zone 1", lambda state: state.has("Alpine Paradise Zone", player) or state.has("Alpine Paradise Zone (Act 1)", player))
        connect_regions(world, player, "Menu", "Alpine Paradise Zone 2",lambda state: state.has("Alpine Paradise Zone", player) or state.has("Alpine Paradise Zone (Act 2)", player))

    if options.match_maps:
        connect_regions(world, player, "Menu", "Jade Valley Zone", lambda state: state.has("Jade Valley Zone", player))
        connect_regions(world, player, "Menu", "Noxious Factory Zone", lambda state: state.has("Noxious Factory Zone", player))
        connect_regions(world, player, "Menu", "Tidal Palace Zone", lambda state: state.has("Tidal Palace Zone", player))
        connect_regions(world, player, "Menu", "Thunder Citadel Zone",lambda state: state.has("Thunder Citadel Zone", player))
        connect_regions(world, player, "Menu", "Desolate Twilight Zone", lambda state: state.has("Desolate Twilight Zone", player))
        connect_regions(world, player, "Menu", "Frigid Mountain Zone", lambda state: state.has("Frigid Mountain Zone", player))
        connect_regions(world, player, "Menu", "Orbital Hangar Zone", lambda state: state.has("Orbital Hangar Zone", player))
        connect_regions(world, player, "Menu", "Sapphire Falls Zone",lambda state: state.has("Sapphire Falls Zone", player))
        connect_regions(world, player, "Menu", "Diamond Blizzard Zone", lambda state: state.has("Diamond Blizzard Zone", player))
        connect_regions(world, player, "Menu", "Celestial Sanctuary Zone", lambda state: state.has("Celestial Sanctuary Zone", player))
        connect_regions(world, player, "Menu", "Frost Columns Zone", lambda state: state.has("Frost Columns Zone", player))
        connect_regions(world, player, "Menu", "Meadow Match Zone",lambda state: state.has("Meadow Match Zone" , player))
        connect_regions(world, player, "Menu", "Granite Lake Zone", lambda state: state.has("Granite Lake Zone", player))
        connect_regions(world, player, "Menu", "Summit Showdown Zone", lambda state: state.has("Summit Showdown Zone", player))
        connect_regions(world, player, "Menu", "Silver Shiver Zone", lambda state: state.has("Silver Shiver Zone", player))
        connect_regions(world, player, "Menu", "Uncharted Badlands Zone",lambda state: state.has("Uncharted Badlands Zone", player))
        connect_regions(world, player, "Menu", "Pristine Shores Zone",lambda state: state.has("Pristine Shores Zone" , player))
        connect_regions(world, player, "Menu", "Crystalline Heights Zone", lambda state: state.has("Crystalline Heights Zone", player))
        connect_regions(world, player, "Menu", "Starlit Warehouse Zone", lambda state: state.has("Starlit Warehouse Zone", player))
        connect_regions(world, player, "Menu", "Midnight Abyss Zone", lambda state: state.has("Midnight Abyss Zone", player))
        connect_regions(world, player, "Menu", "Airborne Temple Zone",lambda state: state.has("Airborne Temple Zone", player))


    # TODO add emerald token logic and other zones
    if options.difficulty != 2:
        # Greenflower
        if options.difficulty == 0:
            add_rule(world.get_location("Greenflower (Act 1) Diamond Emblem", player),
                     lambda state: lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [],350) or
                                                 char_needs_tags(state, ["wall_jump"], -1) or
                                                 char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Greenflower (Act 1) Heart Emblem", player),
                     lambda state: char_needs_tags(state, [], 500))#badnik bounce
            add_rule(world.get_location("Greenflower (Act 1) Clear", player),
                     lambda state: state.has("Yellow Springs", player) or
                                   char_needs_tags(state, [], 150) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], 100) and state.has("Whirlwind Shield",player)))
        else:
            add_rule(world.get_location("Greenflower (Act 1) Diamond Emblem", player),
                     lambda state: lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [],350) or
                                                 char_needs_tags(state, ["wall_jump"], -1) or
                                                 char_needs_tags(state, ["climbs_walls"], -1) or
                                                 char_needs_tags(state, ["instant_speed"], -1)
                     )
            add_rule(world.get_location("Greenflower (Act 1) Clear", player),
                 lambda state: state.has("Yellow Springs",player) or
                        char_needs_tags(state, [], 150) or
                        char_needs_tags(state, ['climbs_walls'], -1) or
                        (char_needs_tags(state, ["can_use_shields"], 100) and state.has("Whirlwind Shield",player))or
                        char_needs_tags(state, ['instant_speed'], 100))

        add_rule(world.get_location("Greenflower (Act 1) Emerald Token - Midair Top Path", player),
                 lambda state: state.has("Yellow Springs",player) or
                               char_needs_tags(state, [], 400) or
                                char_needs_tags(state, ["can_hover"], -1) or
                               (char_needs_tags(state, ["can_use_sheilds"], -1) and state.has("Whirlwind Shield",player)))


        add_rule(world.get_location("Greenflower (Act 1) Club Emblem", player),
                 lambda state: char_needs_tags(state,['spin_walls'],-1))#probably needs yellow springs

        add_rule(world.get_location("Greenflower (Act 1) Emerald Token - Breakable Wall Near Bridge", player),
                 lambda state: char_needs_tags(state,['spin_walls'],-1))

        add_rule(world.get_location("Greenflower (Act 2) Clear", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs", player)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, [], 250)) or
                               (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 250)) or
                               char_needs_tags(state, ["wall_jump"], -1)) or
                               char_needs_tags(state, [], 1200) or
                               char_needs_tags(state, ['climbs_walls'], -1))
        #fuck this is going to get messy



        add_rule(world.get_location("Greenflower (Act 2) Star Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs", player) and char_needs_tags(state,['spin_walls'],-1)) or
                               (state.has("Red Springs", player) or (state.has("Yellow Springs", player) and char_needs_tags(state, ['spin_walls'], 250))) or
                                char_needs_tags(state, ["wall_jump",'spin_walls'], -1) or
                                char_needs_tags(state, ['spin_walls'], 1200) or
                                char_needs_tags(state, ['climbs_walls','spin_walls'], -1))
        add_rule(world.get_location("Greenflower (Act 2) Spade Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs", player) and char_needs_tags(state,['fits_under_gaps'],-1)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, ['fits_under_gaps'], 250)) or
                               (state.has("Yellow Springs", player) and (char_needs_tags(state, ['fits_under_gaps'], 250))) or
                               char_needs_tags(state, ["wall_jump",'fits_under_gaps'], -1) or
                               char_needs_tags(state, ['fits_under_gaps'], 1200) or
                               char_needs_tags(state, ['climbs_walls','fits_under_gaps'], -1))
        add_rule(world.get_location("Greenflower (Act 2) Heart Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player) and char_needs_tags(state, ['strong_walls', 'strong_floors', "pounds_springs", "breaks_spikes"], -1)) or
                               ((state.has("Red Springs", player) or state.has("Yellow Springs", player)) and char_needs_tags(state, ['strong_walls', 'strong_floors', "pounds_springs", "breaks_spikes"], 250)) or
                               char_needs_tags(state, ['strong_walls', 'strong_floors', "wall_jump"], -1) or
                               char_needs_tags(state, ['strong_walls', 'strong_floors'], 1200) or
                               char_needs_tags(state, ['strong_walls', 'strong_floors', "climbs_walls"], -1))

        add_rule(world.get_location("Greenflower (Act 2) Diamond Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player) and (char_needs_tags(state,['strong_walls',"can_use_shields"],-1) and state.has("Whirlwind Shield",player))) or
                               ((state.has("Red Springs", player) or state.has("Yellow Springs", player)) and (char_needs_tags(state,['strong_walls',"can_use_shields"],250) and state.has("Whirlwind Shield",player))) or
                               char_needs_tags(state, ['strong_walls', "wall_jump"], -1) or
                               char_needs_tags(state, ['strong_walls'], 1200) or
                               char_needs_tags(state, ['strong_walls', "climbs_walls"], -1))

        add_rule(world.get_location("Greenflower (Act 2) Club Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs", player) or
                                char_needs_tags(state, [], 1200) or
                                char_needs_tags(state, ["climbs_walls"], -1)))
        add_rule(world.get_location("Greenflower (Act 2) Emerald Token - No Spin High on Ledge", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player) and (char_needs_tags(state, ['strong_floors', "pounds_springs", "breaks_spikes"], -1) or char_needs_tags(state, ['strong_floors'], 150))) or
                               ((state.has("Red Springs", player) or state.has("Yellow Springs", player)) and char_needs_tags(state,['strong_floors'],250)) or
                               char_needs_tags(state, ['strong_floors'], 1200) or
                               char_needs_tags(state, ['strong_floors', "climbs_walls"], -1))
        add_rule(world.get_location("Greenflower (Act 2) Emerald Token - Main Path Cave", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [], 300))
        add_rule(world.get_location("Greenflower (Act 2) Emerald Token - Under Bridge Near End", player),
                 lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player))

        if options.time_emblems:
            add_rule(world.get_location("Greenflower (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Greenflower (Act 1) Clear", player))
            add_rule(world.get_location("Greenflower (Act 2) Time Emblem", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Greenflower (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Greenflower (Act 1) Clear", player))
            add_rule(world.get_location("Greenflower (Act 2) Ring Emblem", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player))

        if options.oneup_sanity:
            add_rule(world.get_location("Greenflower (Act 1) Monitor - Upper Spin Path in Cave", player),
                     lambda state: (state.has("Yellow Springs", player) and char_needs_tags(state, ["spin_walls"], -1)) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ["fits_under_gaps"], -1)) or
                                   char_needs_tags(state, ["fits_under_gaps","climbs_walls"], -1) or
                                   char_needs_tags(state, ["fits_under_gaps", "wall_jump"], -1) or
                                   char_needs_tags(state, ["fits_under_gaps"], 600) or
                                   char_needs_tags(state, ["spin_walls"], 350) or
                                   char_needs_tags(state, ["spin_walls","climbs_walls"], -1) or
                                   char_needs_tags(state, ["spin_walls", "wall_jump"], -1))
            add_rule(world.get_location("Greenflower (Act 1) Monitor - Highest Ledge", player),
                     lambda state:char_needs_tags(state, ["climbs_walls"], -1) or
                     char_needs_tags(state, [], 350) or (state.has("Yellow Springs", player) and state.has("Whirlwind Shield", player) and char_needs_tags(state, ["can_use_shields"], -1)))
            add_rule(world.get_location("Greenflower (Act 1) Monitor - Single Pillar Near End", player),
                     lambda state:state.can_reach_location("Greenflower (Act 1) Clear", player))

            add_rule(world.get_location("Greenflower (Act 2) Monitor - Breakable Floor Near Springs 1", player),
                     lambda state:(state.has("Yellow Springs", player) and state.has("Red Springs", player) and char_needs_tags(state, ["strong_floors"], -1)) or
            (state.has("Red Springs", player) and char_needs_tags(state, ["strong_floors"], 250)) or
            (state.has("Yellow Springs", player) and (char_needs_tags(state, ["strong_floors"], 250)) or
             char_needs_tags(state, ["wall_jump","strong_floors"], -1)) or
            char_needs_tags(state, ["strong_floors"], 1200) or
            char_needs_tags(state, ['climbs_walls',"strong_floors"], -1))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Open Area Behind Checkered Pillar", player),
                     lambda state:state.can_reach_location("Greenflower (Act 2) Clear", player))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Fenced Flower Ledge", player),
                     lambda state:state.can_reach_location("Greenflower (Act 2) Clear", player))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Skylight in 2nd Cave", player),
                     lambda state:char_needs_tags(state, ["wall_jump"], -1) or
                        char_needs_tags(state, [], 1400) or
                        char_needs_tags(state, ['climbs_walls'], -1))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Near Star Emblem 1", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Star Emblem", player))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Pillar Next to End", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Waterfall Top Near Start", player),
                     lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                     char_needs_tags(state, [], 800) or
                     char_needs_tags(state, ["climbs_walls"], -1) or
                     char_needs_tags(state, ["wall_jump"], -1)) #YS+RS, #800jh #climbs walls, walljump)
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Inside Fence Above Start", player),
                     lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [], 300) or
                     char_needs_tags(state, ["climbs_walls"], -1) or
                     char_needs_tags(state, ["wall_jump"], -1))#ys or jh300 or cw or wj)

            if options.difficulty == 0:
                add_rule(world.get_location("Greenflower (Act 2) Monitor - High Ledge After Final Cave", player),
                     lambda state:char_needs_tags(state, [], 1400) or char_needs_tags(state, ["climbs_walls"], -1))

                rf.assign_rule("Greenflower (Act 2) Monitor - Waterfall Top Near Start","SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND") #Possible as amy but stupid
                rf.assign_rule("Greenflower (Act 2) Monitor - High Ledge After Final Cave", "TAILS | KNUCKLES") #badnik bounce
            else:
                add_rule(world.get_location("Greenflower (Act 2) Monitor - High Ledge After Final Cave", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player))
        if options.superring_sanity:
            add_rule(world.get_location("Greenflower (Act 1) Monitor - Across High Bridge in Flowers", player),
                     lambda state: state.can_reach_location("Greenflower (Act 1) Diamond Emblem", player))
            add_rule(world.get_location("Greenflower (Act 1) Monitor - Spring Pillar Near End 1", player),
                     lambda state: state.can_reach_location("Greenflower (Act 1) Clear", player))
            add_rule(world.get_location("Greenflower (Act 1) Monitor - Spring Pillar Near End 2", player),
                     lambda state: state.can_reach_location("Greenflower (Act 1) Clear", player))

            add_rule(world.get_location("Greenflower (Act 2) Monitor - Main Path Springs", player),
                     lambda state: state.has("Red Springs", player) or
                     char_needs_tags(state, [], 800) or
                     char_needs_tags(state, ["climbs_walls"], -1) or
                     char_needs_tags(state, ["wall_jump"], -1))
            if options.difficulty == 0:
                add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player),
                         lambda state: char_needs_tags(state, [], 800) or
                     char_needs_tags(state, ["climbs_walls"], -1) or
                     char_needs_tags(state, ["wall_jump"], -1))
            else:
                add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player),
                         lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player) and char_needs_tags(state, ["badnik_bounce"], 100)) or
                         char_needs_tags(state, [], 800) or char_needs_tags(state, ["climbs_walls"], -1) or
                                        char_needs_tags(state, ["wall_jump"], -1))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 2", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 3", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 4", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 5", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 6", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 7", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Very High Alcove 8", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Very High Alcove 1", player) )

            add_rule(world.get_location("Greenflower (Act 2) Monitor - Spade Emblem Cave 1", player),
                     lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player)) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, [],250)) or
                                   (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 300))) or
                                   char_needs_tags(state, ["wall_jump"], -1) or
                                   char_needs_tags(state, [], 1200) or
                                   char_needs_tags(state, ['climbs_walls'], -1))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Spade Emblem Cave 2", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Spade Emblem Cave 1", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Spade Emblem Cave 3", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Monitor - Spade Emblem Cave 1", player) )

            add_rule(world.get_location("Greenflower (Act 2) Monitor - In Fences Near Picnic", player),
                     lambda state: (state.has("Yellow Springs", player)) or
                                   char_needs_tags(state, ["wall_jump"], -1) or
                                   char_needs_tags(state, [], 300) or
                                   char_needs_tags(state, ['climbs_walls'], -1))


            add_rule(world.get_location("Greenflower (Act 2) Monitor - Log on Final Path", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Near Springs Before End", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Square Pillar Before Big Ramp", player),
                     lambda state: state.can_reach_location("Greenflower (Act 2) Clear", player) )
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Wall Under High Alcove", player),
                     lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player)) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, [],250)) or
                                   (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 300))) or
                                   char_needs_tags(state, ["wall_jump"], -1) or
                                   char_needs_tags(state, [], 1200) or
                                   char_needs_tags(state, ['climbs_walls'], -1))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - No Spin Inside Spikes", player),
                     lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player) and char_needs_tags(state, ["strong_floors"],-1)) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ["strong_floors"],250)) or
                                   char_needs_tags(state, ["wall_jump","strong_floors"], -1) or
                                   char_needs_tags(state, ["strong_floors"], 1200) or
                                   char_needs_tags(state, ['climbs_walls',"strong_floors"], -1))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Open Area on Ledge", player),
                     lambda state:state.can_reach_location("Greenflower (Act 2) Clear", player))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - High Path River", player),
                     lambda state:state.can_reach_location("Greenflower (Act 2) Monitor - Wall Under High Alcove", player))
            add_rule(world.get_location("Greenflower (Act 2) Monitor - Spin Path Red Springs", player),
                     lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs",player) and char_needs_tags(state, ["fits_under_gaps"],-1)) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ["fits_under_gaps"],250)) or
                                   char_needs_tags(state, ["wall_jump","fits_under_gaps"], -1) or
                                   char_needs_tags(state, ["fits_under_gaps"], 1200) or
                                   char_needs_tags(state, ['climbs_walls',"fits_under_gaps"], -1))

        # Techno Hill



        add_rule(world.get_location("Techno Hill (Act 1) Heart Emblem", player),
                 lambda state: char_needs_tags(state,[],900))
        add_rule(world.get_location("Techno Hill (Act 1) Diamond Emblem", player),
                 lambda state: char_needs_tags(state, [], 900) or char_needs_tags(state, ["climbs_walls"], -1))
        add_rule(world.get_location("Techno Hill (Act 1) Club Emblem", player),
                 lambda state: char_needs_tags(state, ['strong_walls'], 250) or char_needs_tags(state, ['strong_walls','climbs_walls'], -1))
        add_rule(world.get_location("Techno Hill (Act 1) Emerald Token - Alt Path Under Slime", player),
                 lambda state: state.has("Buoyant Slime", player))
        add_rule(world.get_location("Techno Hill (Act 2) Clear", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or
                               char_needs_tags(state, ['wall_jump'], -1) or char_needs_tags(state, [], 400))

        add_rule(world.get_location("Techno Hill (Act 2) Heart Emblem", player),
                 lambda state:(char_needs_tags(state, ["can_use_shields"], -1) and state.has("Elemental Shield",player)) or char_needs_tags(state, ["can_stomp"], -1) or state.has("Red Springs",player))


        add_rule(world.get_location("Techno Hill (Act 2) Star Emblem", player),
                 lambda state: char_needs_tags(state,['spin_walls'],-1))
        add_rule(world.get_location("Techno Hill (Act 2) Emerald Token - Knuckles Path Backtrack", player),
                 lambda state: char_needs_tags(state,['strong_walls','strong_floors'],-1))


        if options.difficulty == 0:
            add_rule(world.get_location("Techno Hill (Act 1) Clear", player),
                     lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [], 300) or char_needs_tags(state, ["climbs_walls"], -1) or state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Spade Emblem", player),
                     lambda state:((char_needs_tags(state, ["can_use_shields"], -1) and state.has("Elemental Shield",player)) or char_needs_tags(state, ["can_stomp"], -1)) and state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 2) Emerald Token - Deep in Slime", player),
                     lambda state:(char_needs_tags(state, ["can_use_shields"], -1) and state.has("Elemental Shield",player)) or char_needs_tags(state, ["can_stomp"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Club Emblem", player),
                     lambda state: char_needs_tags(state, [], 1400))

            add_rule(world.get_location("Techno Hill (Act 1) Star Emblem", player),
                     lambda state: char_needs_tags(state, [], 300) or char_needs_tags(state,['climbs_walls'],-1))
        else:
            add_rule(world.get_location("Techno Hill (Act 1) Spade Emblem", player),
                     lambda state: state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 2) Emerald Token - Deep in Slime", player),
                     lambda state:(char_needs_tags(state, ["can_use_shields"], -1) and state.has("Elemental Shield",player)) or char_needs_tags(state, ["can_stomp"], -1) or state.has("Red Springs",player))


        if options.time_emblems:
            add_rule(world.get_location("Techno Hill (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Clear", player))
            add_rule(world.get_location("Techno Hill (Act 2) Time Emblem", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Techno Hill (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Clear", player))
            add_rule(world.get_location("Techno Hill (Act 2) Ring Emblem", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Clear", player))


        if options.oneup_sanity:
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Spin Under Conveyor Belt Door", player),
                     lambda state: char_needs_tags(state, ["fits_under_gaps"], -1))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - In Slime Above Spade Emblem", player),
                     lambda state: state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Deep in Slime Near 2nd Checkpoint", player),
                     lambda state: state.has("Buoyant Slime", player) and
                                   (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 200) or
                                    char_needs_tags(state, ["spin_walls"], -1) or char_needs_tags(state, ["wall_jump"], -1)))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Outside Pipe Room High Ledge", player),
                     lambda state:char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 1400) )
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - High Ledge in Hole Near Start", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Star Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path Highest Ledge", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or (char_needs_tags(state, [], 400) and state.has("Buoyant Slime", player))) or
                                    char_needs_tags(state, ["free_flyer"], 1200))

            add_rule(world.get_location("Techno Hill (Act 2) Monitor - High Ledge Outside 1", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 200) or char_needs_tags(state, ["wall_jump"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)) or state.has("Red Springs", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Spade Emblem", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Spade Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime C", player),
                     lambda state: state.has("Red Springs", player) or state.has("Yellow Springs", player) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 200) or char_needs_tags(state, ["wall_jump"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Elemental Shield", player)) or char_needs_tags(state, ["stomp"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Behind Glass Piston Path", player),
                     lambda state: char_needs_tags(state, ["spin_walls"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Knuckles Path Under Spiked Hallway", player),
                     lambda state: char_needs_tags(state, ["strong_walls","climbs_walls"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Pillar Before End", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Clear", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Deep in Slime", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Monitor - Egg Corp Cavity Under Slime", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Amy Emerald Token", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Emerald Token - Knuckles Path Backtrack", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Tall Pillar Outside Glass", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Monitor - High Ledge Outside 1", player))

            if options.difficulty == 0:
                add_rule(world.get_location("Techno Hill (Act 1) Monitor - Top of Elevator Shaft", player),
                         lambda state: char_needs_tags(state, ["climbs_walls"], -1) or state.has("Buoyant Slime",player) or char_needs_tags(state, ["free_flyer"], 500))
                add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Cavity Under Slime", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls","stomp"], -1) or char_needs_tags(state, ["stomp"], 200) or char_needs_tags(state, ["wall_jump","stomp"], -1) or
                                   (char_needs_tags(state, ["can_use_shields","stomp"], -1) and state.has("Whirlwind Shield", player)) or (state.has("Red Springs", player) and char_needs_tags(state, ["stomp"], -1))) or
                                   (state.has("Elemental Shield", player) and (char_needs_tags(state, ["climbs_walls","can_use_shields"], -1) or char_needs_tags(state, ["can_use_shields"], 200) or char_needs_tags(state, ["wall_jump","can_use_shields"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)) or (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields"], -1)))))

            else:
                add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Cavity Under Slime", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 200) or char_needs_tags(state, ["wall_jump"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)) or state.has("Red Springs", player))


        if options.superring_sanity:

            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path Behind Pipe", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or (char_needs_tags(state, [], 400) and state.has("Buoyant Slime", player)) or
                                    char_needs_tags(state, ["free_flyer"], 1200)))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Deep in Slime Towards Factory", player),
                     lambda state: state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path on Ledge", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Monitor - Knuckles Path Behind Pipe", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path High Ledge", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Monitor - Knuckles Path Behind Pipe", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path on Pipes", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Monitor - Knuckles Path Behind Pipe", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - On Top of Piston Near End", player),
                     lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [], 300) or char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Before End on Crates", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Clear", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - In Slime Near 2nd Checkpoint", player),
                     lambda state: state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Factory Deep in Slime", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 1) Emerald Token - Alt Path Under Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Breakable Wall Ledge", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 200) or
                                    char_needs_tags(state, ["spin_walls"], -1) or char_needs_tags(state, ["wall_jump"], -1)))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - First Factory in Slime", player),
                     lambda state: state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - In First Slime River", player),
                     lambda state: state.has("Buoyant Slime", player))
            add_rule(world.get_location("Techno Hill (Act 1) Monitor - Deep in 2nd Slime River", player),
                     lambda state: state.has("Buoyant Slime", player))

            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Knuckles Path Exit 1", player),
                     lambda state: (char_needs_tags(state, ["strong_walls"], -1)))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Knuckles Path Exit 2", player),
                     lambda state: (char_needs_tags(state, ["strong_walls"], -1)))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Knuckles Path Metal Pillar", player),
                     lambda state: (char_needs_tags(state, ["strong_walls"], -1)))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - High Ledge Outside 2", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [],200) or char_needs_tags(state, ["wall_jump"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player)) or state.has("Red Springs", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - High Ledge Outside 3", player),
                     lambda state:state.can_reach_location("Techno Hill (Act 2) Monitor - High Ledge Outside 2", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime S", player),
                     lambda state: state.has("Red Springs", player) or state.has("Yellow Springs",player) or char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 200) or char_needs_tags(state,["wall_jump"],-1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Elemental Shield",player)) or char_needs_tags(state, ["stomp"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime W", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime S", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime E", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime S", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime N", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Monitor - Large Jump Into Slime S", player))

            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Knuckles Path Before Diagonal Conveyors", player),
                     lambda state: char_needs_tags(state, ["climbs_walls","strong_walls"], -1) or
                                   char_needs_tags(state, ["strong_walls"], 600) or char_needs_tags(state,["wall_jump","strong_walls"],-1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Final Room Cavity in Pillar", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Clear", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Behind Breakable Wall Near Start", player),
                     lambda state: char_needs_tags(state, ["strong_walls"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp High Glass Platform", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [],200) or char_needs_tags(state, ["wall_jump"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player)) or state.has("Red Springs", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Upper Cavity Around Corner", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Monitor - Egg Corp High Glass Platform", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime W", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["stomp"], -1) or char_needs_tags(state, [],200) or char_needs_tags(state, ["wall_jump"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and (state.has("Whirlwind Shield",player) or state.has("Elemental Shield",player))) or state.has("Red Springs", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime E", player),
                     lambda state:state.can_reach_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime W", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime N", player),
                     lambda state:state.can_reach_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime W", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime S", player),
                     lambda state:state.can_reach_location("Techno Hill (Act 2) Monitor - Egg Corp Under Slime W", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Before 2nd Checkpoint Breakable Wall L", player),
                     lambda state: char_needs_tags(state, ["strong_walls"], -1))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Before 2nd Checkpoint Breakable Wall R", player),
                     lambda state: char_needs_tags(state, ["strong_walls"], -1))

            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Heart Emblem 1", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Heart Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Heart Emblem 2", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Heart Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Heart Emblem 3", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Heart Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Diamond Emblem 1", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Diamond Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Diamond Emblem 2", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Diamond Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Club Emblem 1", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Club Emblem", player))
            add_rule(world.get_location("Techno Hill (Act 2) Monitor - Near Club Emblem 2", player),
                     lambda state: state.can_reach_location("Techno Hill (Act 2) Club Emblem", player))
            if options.difficulty == 0:
                add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path in Slime", player),
                         lambda state: ((char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [],400)) and state.has("Buoyant Slime", player)))
            else:
                add_rule(world.get_location("Techno Hill (Act 1) Monitor - Knuckles Path in Slime", player),
                         lambda state: ((char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [],400) or char_needs_tags(state, ["instant_speed"],-1)) and state.has("Buoyant Slime", player)))



        # Deep Sea













#115
        add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - V on Right Path", player),
                 lambda state: ((char_needs_tags(state, [], 250) or
                                 char_needs_tags(state, ['climbs_walls'], -1) or
                                 char_needs_tags(state, ['wall_jump'], -1)) or
                                (state.has("Yellow Springs", player) and state.has("Gargoyle Statues",player))))#todo bad logic

        add_rule(world.get_location("Deep Sea (Act 2) Clear", player),
                 lambda state:((state.has("Red Springs",player) and state.has("Yellow Springs",player)) or
                              (state.has("Red Springs",player) and char_needs_tags(state, ["strong_floor"],-1))) or char_needs_tags(state, ["climbs_walls"],0) or char_needs_tags(state, [],800))#todo or climb
        add_rule(world.get_location("Deep Sea (Act 2) Star Emblem", player),
                 lambda state: (state.has("Red Springs",player) or state.has("Gargoyle Statues",player)) and char_needs_tags(state, ['strong_floors'], -1))#technically this requires either jump height or 'strong_walls' but no reasonable character would make this impossible
        add_rule(world.get_location("Deep Sea (Act 2) Spade Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [],400))
        add_rule(world.get_location("Deep Sea (Act 2) Heart Emblem", player),
                 lambda state: char_needs_tags(state, ['spin_walls'], -1))
        add_rule(world.get_location("Deep Sea (Act 2) Diamond Emblem", player),
                 lambda state: char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or
                               (char_needs_tags(state, ['strong_walls','strong_floors',"pounds_springs"], 115) and state.has("Yellow Springs",player) and state.has("Gargoyle Statues",player)) or
                               char_needs_tags(state, ['strong_walls'], 400))
        add_rule(world.get_location("Deep Sea (Act 2) Club Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, ["wall_jump"], -1) or
                               char_needs_tags(state, [], 1400))
        add_rule(world.get_location("Deep Sea (Act 2) Emerald Token - Near Heart Emblem", player),
                 lambda state: char_needs_tags(state, ['spin_walls'], -1))
        add_rule(world.get_location("Deep Sea (Act 2) Emerald Token - No Spin Spring Turnaround", player),
                 lambda state: char_needs_tags(state, ['strong_floors'], -1) and (state.has("Air Bubbles", player) or state.has("Elemental Shield", player)))

        add_rule(world.get_location("Deep Sea (Act 2) Emerald Token - Down Right From Goal", player),
                 lambda state: ((state.has("Yellow Springs", player)) or
                                (state.has("Red Springs", player) and char_needs_tags(state, ["strong_floors"],-1))) or char_needs_tags(state,[], 800) or char_needs_tags(state,["climbs_walls"], -1))
        add_rule(world.get_location("Deep Sea (Act 2) Emerald Token - Red and Yellow Springs", player),
                 lambda state: ((state.has("Red Springs", player) and char_needs_tags(state,["can_spindash"], -1)) or char_needs_tags(state,[], 1200)))




        if options.difficulty == 0:
            add_rule(world.get_location("Deep Sea (Act 1) Clear", player),
                     lambda state: char_needs_tags(state, [], 250) or char_needs_tags(state, ['can_hover'],-1) or char_needs_tags(state, ['climbs_walls'], -1) or state.has("Yellow Springs", player))
            #not possible for amy
            add_rule(world.get_location("Deep Sea (Act 1) Star Emblem", player),
                 lambda state: char_needs_tags(state,['strong_walls',"pounds_springs",'can_hover'],-1) or
                                char_needs_tags(state,['strong_walls',"pounds_springs"],250) or
                                char_needs_tags(state,['strong_walls',"pounds_springs",'climbs_walls'],-1) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs"],-1) and state.has("Yellow Springs",player) and
                                state.has("Red Springs",player) and state.has("Gargoyle Statues",player)) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs",'can_use_shields'],-1) and state.has("Yellow Springs",player) and
                                state.has("Red Springs",player)and state.has("Whirlwind Shield",player) ) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs"],200) and state.has("Yellow Springs",player) and
                                state.has("Red Springs",player)) or
                               char_needs_tags(state,['strong_walls'],1500))
            add_rule(world.get_location("Deep Sea (Act 1) Spade Emblem", player),
                 lambda state:  (((char_needs_tags(state,[],200) and state.has("Yellow Springs",player)) or
                                char_needs_tags(state, [], 250) or
                               char_needs_tags(state,['can_hover'],-1)) and state.has("Red Springs",player)) or
                                (char_needs_tags(state, ['instant_speed'], 250) or
                                  (char_needs_tags(state, ["can_use_shields",'instant_speed'], 100) and state.has("Whirlwind Shield",player) and state.has("Yellow Springs",player)) or
                                  char_needs_tags(state, ['can_hover','instant_speed'], -1)) or
                                char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Deep Sea (Act 1) Heart Emblem", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 1000)) and (state.has("Air Bubbles",player) or state.has("Elemental Shield",player)))
            add_rule(world.get_location("Deep Sea (Act 1) Diamond Emblem", player),
                 lambda state: ((char_needs_tags(state, [], 250) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                                char_needs_tags(state, ['wall_jump'], -1)) or
                               (state.has("Yellow Springs", player) and state.has("Gargoyle Statues",player)))
                               and (state.has("Air Bubbles",player) or state.has("Elemental Shield",player)))
            add_rule(world.get_location("Deep Sea (Act 1) Club Emblem", player),
                 lambda state: (char_needs_tags(state, [], 250) or char_needs_tags(state, ['can_hover'],-1) or char_needs_tags(state, ['climbs_walls'], -1) or state.has("Yellow Springs", player)) and state.has("Gargoyle Statues",player))
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Underwater Air Pocket on Right Path", player),
                 lambda state: ((char_needs_tags(state, [], 250) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                                char_needs_tags(state, ['wall_jump'], -1)) or
                               (state.has("Yellow Springs", player) and state.has("Gargoyle Statues",player))))
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Waterslide Gargoyles", player),
                 lambda state: (char_needs_tags(state,[],250) or
                                char_needs_tags(state,['can_hover'],-1) or
                                char_needs_tags(state,['climbs_walls'],-1) or
                                state.has("Yellow Springs",player))and state.has("Gargoyle Statues",player))#todo bad logic
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Large Underwater Curve", player),
                 lambda state: ((char_needs_tags(state, ['can_hover'], -1) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, [], 250) or char_needs_tags(state, ['climbs_walls'], -1)) and
                                (state.has("Air Bubbles", player) or state.has("Elemental Shield", player))))
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Yellow Doors", player),
                 lambda state: (char_needs_tags(state, ["instant_speed",'fits_under_gaps'], -1) and state.has("Yellow Springs",player)) or
                               char_needs_tags(state, ['fits_under_gaps'], 1200) or char_needs_tags(state, ['fits_under_gaps',"climbs_walls"],-1) or char_needs_tags(state, ["instant_speed",'fits_under_gaps','can_hover'], -1))

        else:
            add_rule(world.get_location("Deep Sea (Act 1) Clear", player),
                 lambda state: char_needs_tags(state, [], 250) or char_needs_tags(state, ['can_hover'],-1) or
                               char_needs_tags(state, ['climbs_walls'], -1) or state.has("Yellow Springs", player) or char_needs_tags(state, ["badnik_bounce"], -1))
            add_rule(world.get_location("Deep Sea (Act 1) Star Emblem", player),
                 lambda state: char_needs_tags(state,['strong_walls',"pounds_springs",'can_hover'],-1) or
                                char_needs_tags(state,['strong_walls',"pounds_springs"],250) or
                                char_needs_tags(state,['strong_walls',"pounds_springs",'climbs_walls'],-1) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs"],-1) and state.has("Yellow Springs",player) and
                                state.has("Red Springs",player) and state.has("Gargoyle Statues",player)) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs",'can_use_shields'],-1) and state.has("Yellow Springs",player) and
                                state.has("Red Springs",player)and state.has("Whirlwind Shield",player) ) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs"],200) and state.has("Yellow Springs",player) and
                                state.has("Red Springs",player)) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs",'badnik_bounce'],-1) and state.has("Red Springs",player) and state.has("Gargoyle Statues",player)) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs",'can_use_shields','badnik_bounce'],-1) and state.has("Red Springs",player)and state.has("Whirlwind Shield",player) ) or
                                (char_needs_tags(state,['strong_walls',"pounds_springs",'badnik_bounce'],200) and state.has("Red Springs",player)) or
                               char_needs_tags(state,['strong_walls'],1500))
            add_rule(world.get_location("Deep Sea (Act 1) Spade Emblem", player),
                 lambda state:  (((char_needs_tags(state,[],200) and state.has("Yellow Springs",player)) or
                                  (char_needs_tags(state, ['badnik_bounce'], 200)) or
                                char_needs_tags(state, [], 250) or
                               char_needs_tags(state,['can_hover'],-1)) and state.has("Red Springs",player)) or
                                (char_needs_tags(state, ['instant_speed'], 250) or
                                 char_needs_tags(state, ['instant_speed','badnik_bounce'], -1) or
                                  (char_needs_tags(state, ["can_use_shields",'instant_speed'], 100) and state.has("Whirlwind Shield",player) and state.has("Yellow Springs",player)) or
                                (char_needs_tags(state, ["can_use_shields",'instant_speed','badnik_bounce'], 100) and state.has("Whirlwind Shield",player)) or
                                  char_needs_tags(state, ['can_hover','instant_speed'], -1)) or
                                char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Deep Sea (Act 1) Heart Emblem", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 1000) or
                                    (char_needs_tags(state, ["instant_speed"], 100) and state.has("Yellow Springs",player))) and (state.has("Air Bubbles",player) or state.has("Elemental Shield",player)))
            add_rule(world.get_location("Deep Sea (Act 1) Diamond Emblem", player),
                 lambda state: ((char_needs_tags(state, [], 250) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                                char_needs_tags(state, ['wall_jump'], -1) or
                                 char_needs_tags(state, ['badnik_bounce'], -1)) or
                               (state.has("Yellow Springs", player) and state.has("Gargoyle Statues",player)))
                               and (state.has("Air Bubbles",player) or state.has("Elemental Shield",player)))
            add_rule(world.get_location("Deep Sea (Act 1) Club Emblem", player),
                 lambda state: (char_needs_tags(state, [], 250) or char_needs_tags(state, ['badnik_bounce'],-1) or
                                char_needs_tags(state, ['can_hover'],-1) or char_needs_tags(state, ['climbs_walls'], -1) or
                                state.has("Yellow Springs", player)) and state.has("Gargoyle Statues",player))
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Underwater Air Pocket on Right Path", player),
                 lambda state: ((char_needs_tags(state, [], 250) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                                 char_needs_tags(state, ['badnik_bounce'], -1) or
                                char_needs_tags(state, ['wall_jump'], -1)) or
                               (state.has("Yellow Springs", player) and state.has("Gargoyle Statues",player))))
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Waterslide Gargoyles", player),
                 lambda state: (char_needs_tags(state,[],250) or
                                char_needs_tags(state,['can_hover'],-1) or
                                char_needs_tags(state,['climbs_walls'],-1) or
                                char_needs_tags(state, ['badnik_bounce'], -1) or
                                state.has("Yellow Springs",player))and state.has("Gargoyle Statues",player))#todo bad logic
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Large Underwater Curve", player),
                 lambda state: ((char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['badnik_bounce'], -1) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, [], 250) or char_needs_tags(state, ['climbs_walls'], -1))))
            add_rule(world.get_location("Deep Sea (Act 1) Emerald Token - Yellow Doors", player),
                 lambda state: (char_needs_tags(state, ["instant_speed",'fits_under_gaps'], -1) and state.has("Yellow Springs",player)) or
                               char_needs_tags(state, ['fits_under_gaps'], 1200) or char_needs_tags(state, ['fits_under_gaps',"climbs_walls"],-1) or char_needs_tags(state, ["instant_speed",'fits_under_gaps','can_hover'], -1)  or char_needs_tags(state, ["instant_speed",'fits_under_gaps','badnik_bounce'], -1))



        if options.time_emblems:
            add_rule(world.get_location("Deep Sea (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 2) Time Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Deep Sea (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 2) Ring Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Clear", player))


        if options.oneup_sanity:






            #"Deep Sea (Act 1) Monitor - x:8640 y:3168" - maybe at least require wind for normal - have to check other emblems if so (Club emblem) (NAH)

            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Heart Emblem Backtrack to Club 1", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Heart Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Near Waterslide Emerald Token", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Emerald Token - Waterslide Gargoyles", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Waterfall Cave Opposite Spade Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Spade Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Near Diamond Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Diamond Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Behind Cyan Door", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Emerald Token - V on Right Path", player))

            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Spindash Fast Door 1", player),
                     lambda state: (char_needs_tags(state, ["midair_speed","can_spindash"], -1)))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Gargoyle Path Wall Under Oval Platform", player),
                     lambda state: (char_needs_tags(state, ["spin_walls"], -1)))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Knuckles Path Dark High Ledge", player),
                     lambda state: (char_needs_tags(state, ["strong_walls"], -1)))#todo probably needs more
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Knuckles Path Crushing Ceiling", player),
                     lambda state: (char_needs_tags(state, ["strong_walls"], -1)))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Gargoyle Path Behind Periodic Waterfall", player),
                     lambda state: (char_needs_tags(state, ["can_spindash","instant_speed"], -1) or char_needs_tags(state, ["can_spindash","climbs_walls"], -1) or char_needs_tags(state, ["can_spindash","can_hover"], -1) or char_needs_tags(state, ["can_spindash"], 400)or
                                    (state.has("Gargoyle Statues", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)))))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Main Path Roll Down Ramp Into Breakable Wall", player),
                     lambda state: (char_needs_tags(state, ["spin_walls","instant_speed"], -1) or
                                    char_needs_tags(state, ["spin_walls","roll","can_spindash"], -1)))
            # "Deep Sea (Act 2) Monitor - Gargoyle Path Spiked Cliff Top" todo maybe require more
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Waterslide Fail 2nd Jump", player),
                     lambda state: (state.has("Yellow Springs", player) or char_needs_tags(state, ["climbs_walls"], -1)or char_needs_tags(state, ["wall_jump"], -1)or char_needs_tags(state, [], 800)))




            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Spindash Fast Door 2", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Monitor - Spindash Fast Door 1", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Spindash Fast Door 3", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Monitor - Spindash Fast Door 1", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Left Ledge Near End", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Near Club Emblem", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Club Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Waterslide Avoid Wall Spikes", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 2) Monitor - Waterslide Fail 2nd Jump", player))

            if options.difficulty == 0:
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Purple Switch", player),
                         lambda state: state.has("Gargoyle Statues", player) and (
                                 char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path First Water Around Corner", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 1",player),#getting into pillar
                    lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                  char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Broken Wall Near End", player),
                         lambda state: char_needs_tags(state, ["instant_speed"], 300) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["instant_speed"], -1)) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, [], 400) or
                                       (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player) and state.has("Yellow Springs", player)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Behind Fast Closing Door 1",player),
                    lambda state: state.has("Gargoyle Statues", player) and (char_needs_tags(state, ["can_hover","instant_speed","insane_speed"], -1) or (char_needs_tags(state, ["instant_speed","insane_speed"], -1) and state.has("Yellow Springs", player)) or
                                  (state.has("Red Springs", player) and (char_needs_tags(state, ["can_hover","insane_speed"], -1)  or (char_needs_tags(state, ["insane_speed"], -1) and state.has("Yellow Springs", player)))) or
                                  char_needs_tags(state, ["insane_speed"], 500) or char_needs_tags(state, ["climbs_walls","insane_speed"], -1) or char_needs_tags(state, ["wall_jump","insane_speed"], -1))) # rs+(hov/ys/bb)  (jh500/cw/wj)+gsw
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Waterfall Cave Near Cyan Door",player),
                    lambda state: char_needs_tags(state, ["free_flyer"], 300) or char_needs_tags(state, ["midair_speed"], 300) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["midair_speed"], -1)) or
                                  char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Breakable Wall Between Columns", player),
                         lambda state: char_needs_tags(state, ["spin_walls"], 300) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["spin_walls"], -1)) or
                                 char_needs_tags(state, ["can_hover","spin_walls"], -1) or char_needs_tags(state, ["climbs_walls","spin_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump","spin_walls"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Waterslide Hidden Spring Room",player),
                    lambda state: char_needs_tags(state, [], 300) or ((state.has("Yellow Springs", player) or
                                  char_needs_tags(state, ["can_hover"], -1)) and (char_needs_tags(state, [],150) and (state.has("Whirlwind Shield", player) and char_needs_tags(state, ["can_use_shields"],-1)))) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1))

                #rf.assign_rule("Deep Sea (Act 2) Monitor - Gargoyle Path Spiked Cliff Top", "TAILS | KNUCKLES | FANG")
            else:
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Purple Switch", player),
                         lambda state: state.has("Gargoyle Statues", player) and (
                                 char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path First Water Around Corner", player),#TODO better name
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 1", player),# getting into pillar
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                       char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state,["climbs_walls"],-1) or
                                       char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Broken Wall Near End", player),
                         lambda state: char_needs_tags(state, ["instant_speed"], 300) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["instant_speed"], -1)) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce","instant_speed"], -1) or char_needs_tags(state, [], 400) or
                         (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player) and state.has("Yellow Springs", player)) or
                         (char_needs_tags(state, ["can_use_shields","badnik_bounce"], -1) and state.has("Whirlwind Shield", player)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Behind Fast Closing Door 1",player),
                        lambda state: state.has("Gargoyle Statues", player) and (char_needs_tags(state, ["can_hover","instant_speed","insane_speed"], -1) or char_needs_tags(state, ["badnik_bounce","instant_speed","insane_speed"], -1) or (char_needs_tags(state, ["instant_speed","insane_speed"], -1) and state.has("Yellow Springs", player)) or
                                  (state.has("Red Springs", player) and (char_needs_tags(state, ["can_hover","insane_speed"], -1) or char_needs_tags(state, ["badnik_bounce","insane_speed"], -1) or (char_needs_tags(state, ["insane_speed"], -1) and state.has("Yellow Springs", player)))) or
                                  char_needs_tags(state, ["insane_speed"], 500) or char_needs_tags(state, ["climbs_walls","insane_speed"], -1) or char_needs_tags(state, ["wall_jump","insane_speed"], -1))) # rs+(hov/ys/bb)  (jh500/cw/wj)+gsw
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Waterfall Cave",player),
                    lambda state: char_needs_tags(state, ["free_flyer"], 300) or char_needs_tags(state, ["midair_speed"], 300) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["midair_speed"], -1)) or
                                  char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["midair_speed","badnik_bounce"],-1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Breakable Wall Between Columns", player),
                         lambda state: char_needs_tags(state, ["spin_walls"], 300) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["spin_walls"], -1)) or
                                 char_needs_tags(state, ["can_hover","spin_walls"], -1) or char_needs_tags(state, ["climbs_walls","spin_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump","spin_walls"], -1) or char_needs_tags(state, ["spin_walls","badnik_bounce"],-1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Waterslide Hidden Spring Room",player),
                    lambda state: char_needs_tags(state, [], 300) or ((state.has("Yellow Springs", player) or
                                  char_needs_tags(state, ["can_hover"], -1)) and (char_needs_tags(state, [],150) and (state.has("Whirlwind Shield", player) and char_needs_tags(state, ["can_use_shields"],-1)))) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], 150) or (char_needs_tags(state, ["badnik_bounce","can_use_shields"], -1) and state.has("Whirlwind Shield", player)))


            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Lower Route Sloped Ledge", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path First Water Around Corner", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Path Under Hidden Elevator", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path First Water Around Corner", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Yellow Switch", player),
                     lambda state: state.can_reach_location("Deep Sea (Act 1) Emerald Token - Yellow Doors", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Behind Fast Closing Door 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Behind Fast Closing Door 1", player))
        if options.superring_sanity:

            if options.difficulty == 0:
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Underwater After Red Spring Jump", player),
                         lambda state:(char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                        char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, ["wall_jump"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Path Beside Elevator", player),
                         lambda state:(char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                        char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, ["wall_jump"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 2",player),#getting into pillar
                    lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                  char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Underwater Switch 1",player),#getting into pillar
                    lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                  char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Lower Route Under Sloped Ledge", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Below Star Emblem", player),
                         lambda state: (state.has("Red Springs", player) and (char_needs_tags(state, [], 300) or
                                (state.has("Yellow Springs", player) and ((char_needs_tags(state, ["can_use_shields"],-1) and state.has("Whirlwind Shield", player)) or char_needs_tags(state, [], 200) or state.has("Gargoyle Statues", player))) or
                                 (char_needs_tags(state, ["can_hover","can_use_shields"], -1) and state.has("Whirlwind Shield", player)) or char_needs_tags(state, ["can_hover"], 200) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 (char_needs_tags(state, ["can_hover"], -1) and state.has("Gargoyle Statues", player)) or char_needs_tags(state, ["wall_jump"], -1))) or char_needs_tags(state, [], 1500))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Ledge Over Water", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Merge Underwater 1", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Ending Path on Rocks", player),
                         lambda state: char_needs_tags(state, [], 300) or (state.has("Yellow Springs", player) and (state.has("Red Springs", player) or char_needs_tags(state, [], 200) or state.has("Gargoyle Statues", player))) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath High Rock Alcove", player),
                         lambda state: char_needs_tags(state, [], 300) or (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 200) or char_needs_tags(state, ["instant_speed"], -1) or (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)))) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Ending Path High on Rocks", player),
                         lambda state: char_needs_tags(state, [], 300) or (state.has("Yellow Springs", player)) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 1", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Red Spring Jump Left", player),
                         lambda state: char_needs_tags(state, [], 600) or ((state.has("Yellow Springs", player) or char_needs_tags(state, [], 300)) and (state.has("Red Springs", player))) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1))


            else:
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Underwater After Red Spring Jump", player),
                         lambda state:(char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                        char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Path Beside Elevator", player),
                         lambda state:(char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                        char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 2",player),#getting into pillar
                    lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                  char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                  char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Underwater Switch 1", player),
                         lambda state:(char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                        char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1)))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Lower Route Under Sloped Ledge", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Below Star Emblem", player),
                         lambda state: (state.has("Red Springs", player) and (char_needs_tags(state, [], 300) or
                                (char_needs_tags(state, ["badnik_bounce","can_use_shields"], -1) and state.has("Whirlwind Shield", player)) or char_needs_tags(state, ["badnik_bounce"], 200) or (char_needs_tags(state, ["badnik_bounce"], -1) and state.has("Gargoyle Statues", player)) or
                                (state.has("Yellow Springs", player) and ((char_needs_tags(state, ["can_use_shields"],-1) and state.has("Whirlwind Shield", player)) or char_needs_tags(state, [], 200) or state.has("Gargoyle Statues", player))) or
                                 (char_needs_tags(state, ["can_hover","can_use_shields"], -1) and state.has("Whirlwind Shield", player)) or char_needs_tags(state, ["can_hover"], 200) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 (char_needs_tags(state, ["can_hover"], -1) and state.has("Gargoyle Statues", player)) or char_needs_tags(state, ["wall_jump"], -1))) or char_needs_tags(state, [], 1500))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Ledge Over Water", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Merge Underwater 1", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1)  or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Ending Path on Rocks", player),
                         lambda state: char_needs_tags(state, [], 300) or (state.has("Yellow Springs", player) and (state.has("Red Springs", player) or char_needs_tags(state, [], 200) or state.has("Gargoyle Statues", player))) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Ending Path High on Rocks", player),
                         lambda state: char_needs_tags(state, [], 300) or (state.has("Yellow Springs", player)) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 1", player),
                         lambda state: char_needs_tags(state, [], 300) or state.has("Yellow Springs", player) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))
                add_rule(world.get_location("Deep Sea (Act 1) Monitor - Red Spring Jump Left", player),
                         lambda state: char_needs_tags(state, [], 600) or ((state.has("Yellow Springs", player) or char_needs_tags(state, [], 300)) and (state.has("Red Springs", player))) or
                                 char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["climbs_walls"],-1) or
                                 char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))

            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 3", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 2", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Underwater Switch 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path Underwater Switch 1", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Path Underwater 1", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Path Beside Elevator", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Path Underwater 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Path Beside Elevator", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Shallow Water", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path Ledge Over Water", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Behind Rubble", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path Ledge Over Water", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Merge Underwater 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Right Subpath Merge Underwater 1", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Lower Path Before Broken Door", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Path Beside Elevator", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - After Waterslide", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path Shallow Water", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Before End Behind Pillar", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Pillar Button Path Behind First Gargoyle", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Sinking Pillar Button 2", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Behind Waterslide Start", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path Shallow Water", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Path First Arch Top", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Path Beside Elevator", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Ending Path Near Floating Mines", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Ending Path on Rocks", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Underwater Curve Cave on Rock", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Ending Path High on Rocks", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Near End Behind Rubble", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 1", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Left Path Underwater Near Waterslide", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - After Waterslide", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - After Waterslide Underwater Around Corner", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - After Waterslide", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Join Right Lower Route Underwater Wall Bottom", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Left Path Shallow Water", player))
            add_rule(world.get_location("Deep Sea (Act 1) Monitor - Right Right Subpath Inside Waterfall", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 1) Monitor - Right Right Subpath Behind Pillar 1", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Right Waterslide Path Cave", player),
                     lambda state: (state.has("Yellow Springs", player) or char_needs_tags(state, ["climbs_walls"], -1)or char_needs_tags(state, ["wall_jump"], -1)or char_needs_tags(state, [], 800)))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Diagonal Pillars Near Spring Emerald Token", player),
                     lambda state: (char_needs_tags(state, ["can_spindash"], -1) or ((char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400) or char_needs_tags(state, ["wall_jump"], -1)) and state.has("Gargoyle Statues", player))))

            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Gargoyle Path Behind Doors 1", player),
                     lambda state: state.has("Gargoyle Statues", player) and
                                   (char_needs_tags(state, ["roll"], -1) or char_needs_tags(state, ["climbs_walls"], -1) or
                                    char_needs_tags(state, [], 400) or char_needs_tags(state, ["wall_jump"], -1) or
                                    char_needs_tags(state, ["skims_water"], -1) or char_needs_tags(state, ["can_hover"], -1) or
                                    char_needs_tags(state, ["instant_speed"], -1) or state.has("Yellow Springs", player)))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Right Waterslide Path Switch Secret 1", player),
                     lambda state: state.has("Gargoyle Statues", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, ["climbs_walls"], -1)or
                                    char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, [], 800)))

            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Spring Button Door 1", player),
                     lambda state: (state.has("Elemental Shield", player) or state.has("Air Bubbles", player))and
                                   (char_needs_tags(state, ["strong_floors"], 400) or char_needs_tags(state, ["strong_floors","climbs_walls"], -1)) or (char_needs_tags(state, ["strong_floors"], -1) and state.has("Yellow Springs", player)))



            if options.difficulty == 0:
                add_rule(world.get_location("Deep Sea (Act 2) Monitor - Behind Plants Near End", player),
                     lambda state: (state.has("Yellow Springs", player) or char_needs_tags(state, ["climbs_walls"], -1) or
                                    char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, [], 800) or
                                    (char_needs_tags(state, ["strong_floors"], -1) and state.has("Red Springs", player) and (state.has("Air Bubbles", player) or state.has("Elemental Shield", player)))))
            else:
                add_rule(world.get_location("Deep Sea (Act 2) Monitor - Behind Plants Near End", player),
                     lambda state: (state.has("Yellow Springs", player) or char_needs_tags(state, ["climbs_walls"], -1) or
                                    char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, [], 800) or
                                    (char_needs_tags(state, ["strong_floors"], -1) and state.has("Red Springs", player))))

            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Before Final Gate", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Star Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind First Plants", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Star Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Fast Closing Door Front", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Monitor - Diagonal Pillars Near Spring Emerald Token", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Down Right From Goal on Rocky Ledge", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Gargoyle Path Behind Doors 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Monitor - Gargoyle Path Behind Doors 1", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Right Waterslide Path Switch Secret 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Monitor - Right Waterslide Path Switch Secret 1", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Before End 1", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Before End 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Clear", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Down Right From Goal Underwater Cave", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Monitor - Behind Plants Near End", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Spring Button Door 2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Spring Button Door 1", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner L1", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Star Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner L2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Star Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner R1", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Star Emblem", player))
            add_rule(world.get_location("Deep Sea (Act 2) Monitor - Nospin Path Behind Ruins Corner R2", player),
                    lambda state:state.can_reach_location("Deep Sea (Act 2) Star Emblem", player))

        # Castle Eggman

        add_rule(world.get_location("Castle Eggman (Act 1) Clear", player),
                 lambda state: (state.has("Swinging Maces",player) and state.has("Yellow Springs",player) and state.has("Red Springs",player)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, ["can_hover","instant_speed"], -1)) or
                                (state.has("Swinging Maces", player) and state.has("Yellow Springs",player) and char_needs_tags(state, ["can_hover"], -1)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                                char_needs_tags(state, [], 1200))

        add_rule(world.get_location("Castle Eggman (Act 1) Star Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1400))#wall jumps DONT work
        add_rule(world.get_location("Castle Eggman (Act 1) Spade Emblem", player),
                 lambda state: (state.has("Swinging Maces",player) and state.has("Yellow Springs",player) and state.has("Red Springs",player)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, ["can_hover","instant_speed"], -1)) or
                               (state.has("Swinging Maces", player) and state.has("Yellow Springs",player) and char_needs_tags(state, ["can_hover"], -1)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                                char_needs_tags(state, [], 1200))
        add_rule(world.get_location("Castle Eggman (Act 1) Heart Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Yellow Springs",player) and state.has("Red Springs",player)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, ["can_hover","instant_speed"], -1)) or
                               (state.has("Swinging Maces", player) and state.has("Yellow Springs",player) and char_needs_tags(state,["can_hover"],-1)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1200))
        add_rule(world.get_location("Castle Eggman (Act 1) Diamond Emblem", player),
                 lambda state: state.has("Swinging Maces",player) or state.has("Red Springs",player) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))

        add_rule(world.get_location("Castle Eggman (Act 1) Club Emblem", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))

        add_rule(world.get_location("Castle Eggman (Act 1) Emerald Token - Inside Castle", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
        add_rule(world.get_location("Castle Eggman (Act 1) Emerald Token - Spring Side Path", player),
                lambda state: (state.has("Swinging Maces", player)and (char_needs_tags(state, ["can_hover"], -1) or (char_needs_tags(state, ["instant_speed"], -1)and state.has("Yellow Springs",player))) or state.has("Red Springs",player)) or
                        char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, [], 1000))


        add_rule(world.get_location("Castle Eggman (Act 2) Clear", player),
                 lambda state: (state.has("Swinging Maces",player) and state.has("Yellow Springs",player)) or
                 (state.has("Swinging Maces",player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1000))
        add_rule(world.get_location("Castle Eggman (Act 2) Star Emblem", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 200))) or
                               (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_hover'], -1)) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 250))
        add_rule(world.get_location("Castle Eggman (Act 2) Spade Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 200))) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1400))
        add_rule(world.get_location("Castle Eggman (Act 2) Heart Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 200))) or
                               (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1200))
        add_rule(world.get_location("Castle Eggman (Act 2) Diamond Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Yellow Springs", player) and char_needs_tags(state, ["low_grav"], -1)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, ["low_grav"], 200)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, ['climbs_walls',"low_grav"], -1)) or char_needs_tags(state, [], 1500))
        add_rule(world.get_location("Castle Eggman (Act 2) Club Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Yellow Springs", player) and state.has("Red Springs", player)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                               (char_needs_tags(state, ["can_hover"], -1) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, ["can_hover"], 200) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1200)
                               )
        add_rule(world.get_location("Castle Eggman (Act 2) Emerald Token - First Outside Area", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 600))
        add_rule(world.get_location("Castle Eggman (Act 2) Emerald Token - Corner of Right Courtyard", player),
                 lambda state: state.can_reach_location("Castle Eggman (Act 2) Heart Emblem", player))#laziness
        add_rule(world.get_location("Castle Eggman (Act 2) Emerald Token - Back Window of Left Courtyard", player),
                 lambda state: state.can_reach_location("Castle Eggman (Act 2) Spade Emblem", player))

        add_rule(world.get_location("Castle Eggman (Act 2) Emerald Token - Spring Near Club Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Yellow Springs",player) and state.has("Red Springs",player)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, [], 800)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1200))
        add_rule(world.get_location("Castle Eggman (Act 2) Emerald Token - High Ledge Before Final Tower", player),
                 lambda state: (state.has("Yellow Springs", player) and char_needs_tags(state, ["instant_speed"], -1)) or
                               (char_needs_tags(state, ["instant_speed"], 200)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1200)
                               )
        add_rule(world.get_location("Castle Eggman (Act 3) Clear", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, [], 200) or char_needs_tags(state, ["climbs_walls"], -1))

        if options.time_emblems:
            add_rule(world.get_location("Castle Eggman (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Clear", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Time Emblem", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Clear", player))
            add_rule(world.get_location("Castle Eggman (Act 3) Time Emblem", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 3) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Castle Eggman (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Clear", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Ring Emblem", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Clear", player))
        if options.score_emblems:
            add_rule(world.get_location("Castle Eggman (Act 3) Score Emblem", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 3) Clear", player))
        #if options.difficulty == 0:
        #    rf.assign_rule("Castle Eggman (Act 2) Club Emblem", "TAILS | KNUCKLES | FANG | WIND")tbh this isnt really hard
        if options.oneup_sanity:
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Mud Path on Side Wall", player),
                     lambda state: (state.has("Swinging Maces", player) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 800)))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Outside Bars First Tall Castle Wall", player),
                     lambda state: (state.has("Swinging Maces", player)) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 800))

            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Second Area Behind Overgrown Bars", player),
                     lambda state: (state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['midair_speed'], -1))) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 800))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 1", player),
                     lambda state: (state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['midair_speed'], -1))) or state.has("Red Springs", player) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 1", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Main Path Sloped Spring Jumps", player),
                 lambda state: state.has("Swinging Maces",player) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))

            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Red Spring Path First Turnaround", player),
                 lambda state: state.has("Swinging Maces",player) and state.has("Red Springs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [],200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Red Spring Path Pillar With Robo-Hoods", player),
                 lambda state: (state.has("Swinging Maces",player) and state.has("Red Springs",player) and (state.has("Yellow Springs",player)  or char_needs_tags(state, [],200))) or
                               (state.has("Swinging Maces",player) and (char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"],-1))) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))

            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Spade Emblem 1", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Spade Emblem", player))


            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Bonfire Area Behind Tall Pillar", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Heart Emblem", player))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Rafter Above Starting Area", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, ["wall_jump"], -1) or
                               char_needs_tags(state, [], 250))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Front Left Path High Above Water", player),
                 lambda state: state.has("Yellow Springs",player) and ((char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player)) or char_needs_tags(state, ["instant_speed"], -1)) or
                               (char_needs_tags(state, ["can_use_shields"], 200) and state.has("Whirlwind Shield", player)) or
                               char_needs_tags(state, ["instant_speed"], 200) or
                               char_needs_tags(state, ["wall_jump"], -1) or
                                char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 250))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - High Bookshelf Before Final Tower", player),
                 lambda state: char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1000))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Under Bridge Near 3rd Checkpoint", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Front Left Path High Ledge Before Swinging Chains", player),
                 lambda state: char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 1000))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Bookshelf in Spike Pit Before Final Tower", player),
                 lambda state: ((state.has("Swinging Maces", player) or char_needs_tags(state, ['can_hover'],-1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs", player)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Top Path Hidden Ground Spring", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Outside Area Pillar Near Star Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs", player)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Miss Red Springs Before 4th Checkpoint", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Courtyard Corner Near Swinging Mace", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Rocky Ledge Opposite Club Emblem", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Path Mace Launch Side Corridor", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Path Thin Gray Bookshelf Top", player),
                 lambda state: char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Window of Left Courtyard", player),
                 lambda state: state.can_reach_location("Castle Eggman (Act 2) Emerald Token - Back Window of Left Courtyard", player))

        if options.superring_sanity:
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Lower Main Path Before Tilted Maces", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))


            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 2", player),
                     lambda state: (state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['midair_speed'], -1))) or state.has("Red Springs", player) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 2", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Main Path Tree Ledge", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200) or (char_needs_tags(state, ["instant_speed"], -1) and state.has("Red Springs",player))) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Wall Path Breakable Stone 1", player),
                     lambda state: (state.has("Swinging Maces", player) or state.has("Red Springs", player) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 800)))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Red Spring Path Start Behind Tree", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - First Swinging Mace Jump 1", player),
                     lambda state: (state.has("Swinging Maces", player) or state.has("Red Springs", player) or
                                   char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 800)))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - First Checkpoint Ring Circle", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Corner Behind 2nd Checkpoint", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Corner After Lower First Checkpoint", player),
                 lambda state: state.has("Swinging Maces",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, [], 200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or state.has("Red Springs",player) or
                               char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Red Spring Path Second Turnaround", player),
                 lambda state: (state.has("Swinging Maces",player) and state.has("Red Springs",player) and (state.has("Yellow Springs",player)  or char_needs_tags(state, [],200))) or
                               (state.has("Swinging Maces",player) and (char_needs_tags(state, ["midair_speed"], -1) or char_needs_tags(state, ["can_hover"],-1))) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 1000))


            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Spade Emblem 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Spade Emblem", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Spade Emblem 3", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Spade Emblem", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 3", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Main Path Cave Under Mud 2", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Titled Maces Cave 1", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Lower Main Path Before Tilted Maces", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 3", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 2", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Trees Near Final Checkpoint", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Clear", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Titled Maces Cave 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Titled Maces Cave 1", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Final Checkpoint R", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Clear", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Final Checkpoint L", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Clear", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Star Emblem 1", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Star Emblem", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Star Emblem 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Star Emblem", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - First Swinging Mace Jump 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - First Swinging Mace Jump 1", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Wall Mace Cave Bottom", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Lower Main Path Tilted Maces 2", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Wall Path Breakable Stone 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Wall Path Breakable Stone 1", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Before Lower First Checkpoint", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Corner After Lower First Checkpoint", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Club Emblem 1", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Club Emblem", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Near Club Emblem 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Club Emblem", player))
            add_rule(world.get_location("Castle Eggman (Act 1) Monitor - Red Spring Path On Slope", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 1) Monitor - Red Spring Path Second Turnaround", player))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Top Path Near Platforms", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Courtyard Behind Wood Pillar", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Gray Bookshelf Near Final Tower Token", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Below Right Courtyard Token", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Before Final Tower Spike Pit Around Corner", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Pillar After Side Mace Launch 1", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Near Club Emblem", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Behind Springs After Outside Path", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Courtyard Back Left Corner", player),
                 lambda state: (state.has("Swinging Maces", player) and (char_needs_tags(state, [], 200) or state.has("Yellow Springs", player))) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 250))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Outside Path Near Spiked Maces", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Courtyard Back Left Corner", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Courtyard Front Pillar", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location( "Castle Eggman (Act 2) Monitor - Left Courtyard Bottom Right Corner", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location( "Castle Eggman (Act 2) Monitor - Left Side Before Swinging Mace Launch", player),
                 lambda state: state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 200)) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 500))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Grass Room Spike Ball Stuck In Tree", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Library Cracked Statue Base", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location( "Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Cracked Stone", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Side Before Swinging Mace Launch", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Above Library Entrance 1", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Cracked Brick Right Library Outside", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Library Moving Platforms Left Bookshelf", player),
                 lambda state:  ((state.has("Swinging Maces",player) or char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed'], -1)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Side Mace Launch Right", player),
                 lambda state:  ((state.has("Swinging Maces",player)) and state.has("Yellow Springs",player)) or
                                (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Courtyard Square Pillar In Grass", player),
                 lambda state: state.has("Yellow Springs", player) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Courtyard First Pillar", player),
                 lambda state: state.has("Swinging Maces", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 200)) or char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 500))



            if options.difficulty == 0:
                add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Library Bookshelf Between Pillars 1", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, ['can_hover'], 200) or
                 (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
                add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Courtyard Back Left Corner", player),
                 lambda state: (state.has("Yellow Springs", player) and state.has("Red Springs", player)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))
            else:
                add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Library Bookshelf Between Pillars 1", player),
                 lambda state: ((char_needs_tags(state, ['can_hover'], -1) or char_needs_tags(state, ['instant_speed','midair_speed'], -1)) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, ['can_hover'], 200) or
                 (state.has("Swinging Maces", player) and char_needs_tags(state, [], 200)) or
                 char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 400))
                add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Courtyard Back Left Corner", player),
                 lambda state: (state.has("Yellow Springs", player) and (state.has("Red Springs", player))or char_needs_tags(state, ['badnik_bounce'], -1)) or
                               char_needs_tags(state, ['climbs_walls'], -1) or char_needs_tags(state, [], 200))



            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Top Path Stay On Platforms 1", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - First Top Path Near Platforms", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Courtyard Behind Fountain", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - First Top Path Near Platforms", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Before Final Tower Spike Pit Under Ledge", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Before Final Tower Spike Pit Around Corner", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Top Path Stay On Platforms 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - First Top Path Stay On Platforms 1", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Top Path Falling Floor", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - First Top Path Near Platforms", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Library Bookshelf Between Pillars 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Left Library Bookshelf Between Pillars 1", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Pillar After Side Mace Launch 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Pillar After Side Mace Launch 1", player))

            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Left Library First Spike Pit", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Right Library Cracked Statue Base", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Grass Room Small Tree Ledge", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Grass Room Spike Ball Stuck In Tree", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Above Library Entrance 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Above Library Entrance 1", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Library Moving Platforms Right Bookshelf", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Right Library Moving Platforms Left Bookshelf", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Library Fake Statue", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Right Library Cracked Statue Base", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Side Mace Launch Left", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Side Mace Launch Right", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Miss Jump 1", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Cracked Stone", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Miss Jump 2", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Right Courtyard Spring Path Cracked Stone", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Before First Courtyard Right Hallway", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - First Courtyard Behind Fountain", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - Grass Room Spike Pit Side Room", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - Grass Room Spike Ball Stuck In Tree", player))
            add_rule(world.get_location("Castle Eggman (Act 2) Monitor - First Courtyard Back Right Corner", player),
                     lambda state: state.can_reach_location("Castle Eggman (Act 2) Monitor - First Courtyard Back Left Corner", player))


        #"Castle Eggman (Act 2) Monitor - x:-3584 y:-14720" "directly above another monitor >:("

        # Arid Canyon
        add_rule(world.get_location("Arid Canyon (Act 1) Clear", player),
                 lambda state: (state.has("Rope Hangs",player) and state.has("Yellow Springs",player)and state.has("Red Springs",player) and (char_needs_tags(state, ['fits_under_gaps'], -1) or state.has("Dust Devils",player))) or
                               (state.has("Rope Hangs",player) and state.has("Red Springs",player) and char_needs_tags(state, ['can_hover'], -1) ) or char_needs_tags(state, [], 600) or
                               char_needs_tags(state, ['climbs_walls'], -1))#ropes,ys,rs,spinchar
        add_rule(world.get_location("Arid Canyon (Act 1) Star Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"],-1) or
                               (char_needs_tags(state, ["pounds_springs",'strong_floors'],-1) and state.has("Red Springs",player) and state.has("Rope Hangs",player)) or
                               (char_needs_tags(state, ["pounds_springs", 'strong_floors',"instant_speed"], -1) and state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player)) or
                               char_needs_tags(state, [],800))
#any + strong floors
        add_rule(world.get_location("Arid Canyon (Act 1) Heart Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                               (state.has("Red Springs",player) and state.has("Rope Hangs",player) and char_needs_tags(state,["roll"],-1)) or
                                (state.has("Red Springs",player) and state.has("Rope Hangs",player) and ((state.has("Yellow Springs",player) or char_needs_tags(state, [], 300))and state.has("Dust Devils",player)) or char_needs_tags(state, ["wall_jump"], -1)) or
                               (state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player)) or
                               char_needs_tags(state, [], 400))
        add_rule(world.get_location("Arid Canyon (Act 1) Club Emblem", player),
                 lambda state:(state.has("Red Springs", player) and (state.has("Yellow Springs", player) and (((char_needs_tags(state, ['can_use_shields','instant_speed'],-1)or char_needs_tags(state, ['can_use_shields','roll'],-1)) and state.has("Whirlwind Shield",player)) or char_needs_tags(state, ['can_hover'],-1)))) or
                     (state.has("Red Springs", player) and (state.has("Yellow Springs", player) and state.has("Dust Devils", player) and (char_needs_tags(state, ['instant_speed'],-1) or (state.has("Rope Hangs", player) and char_needs_tags(state, ['roll'],-1)))))or
                     (state.has("Rope Hangs", player) and (char_needs_tags(state, ['instant_speed','roll'],-1)) and state.has("Dust Devils", player))or
                     (state.has("Red Springs", player) and state.has("Dust Devils", player) and state.has("Rope Hangs", player) and (char_needs_tags(state, ['strong_floors'],200) or (char_needs_tags(state, ['strong_floors','pounds_springs','breaks_spikes','can_use_shields'],-1) and state.has("Yellow Springs", player) and state.has("Whirlwind Shield", player)))) or
                     char_needs_tags(state, ["can_hover"], 400) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))
#whirlwind works but idc
        add_rule(world.get_location("Arid Canyon (Act 1) Emerald Token - Speed Shoes Central Pillar", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                (state.has("Red Springs",player) and state.has("Rope Hangs",player)) or
                               (state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player)) or
                               char_needs_tags(state, [], 600))
        add_rule(world.get_location("Arid Canyon (Act 1) Emerald Token - Behind Pillar Before Exploding Ramp", player),
                 lambda state: state.can_reach_location("Arid Canyon (Act 1) Spade Emblem",player))
        add_rule(world.get_location("Arid Canyon (Act 1) Emerald Token - Behind Wall and Spikes", player),
                 lambda state: char_needs_tags(state, ['strong_walls',"breaks_spikes"], -1))#technically can be done with climbs_walls/jump_height and breaks spikes

        add_rule(world.get_location("Arid Canyon (Act 2) Clear", player),
                 lambda state: (state.has("Minecarts",player) and(
                     (state.has("Dust Devils",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, [], 200)))or
                     ((char_needs_tags(state, ["roll"], -1))or char_needs_tags(state, ["instant_speed"], -1) and state.has("Yellow Springs",player) and state.has("Red Springs",player)) or
                     (char_needs_tags(state, ["climbs_walls",'strong_walls','fits_under_gaps'], -1) or
                      (char_needs_tags(state, [], 800)
                 )))) or (char_needs_tags(state, ["stronger_walls"], -1) and state.has("Dust Devils",player)) or
                      ((char_needs_tags(state, ["stronger_walls","instant_speed"], -1) or (char_needs_tags(state, ["stronger_walls","roll"], -1) and state.has("Red Springs",player))) and state.has("Yellow Springs",player) and state.has("Red Springs",player)) or
                      (char_needs_tags(state, ["stronger_walls"], 600)))#todo amy can do this with a bunch of shit
        #strongerwalls + ys+rs/

        add_rule(world.get_location("Arid Canyon (Act 2) Spade Emblem", player),
                 lambda state: (state.has("Dust Devils",player) and char_needs_tags(state, ['strong_floors'],-1)) or
                                char_needs_tags(state, ['strong_floors'], 400) or
                               (char_needs_tags(state, ['roll','strong_floors'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed', 'strong_floors'], -1) or char_needs_tags(state, ["climbs_walls","strong_floors"], -1)#knuckles path can probably backtrack
                 )


        add_rule(world.get_location("Arid Canyon (Act 2) Club Emblem", player),
                 lambda state: state.has("Minecarts",player) and (char_needs_tags(state, ["climbs_walls"],-1) or
                               char_needs_tags(state, [],1400)))
        add_rule(world.get_location("Arid Canyon (Act 2) Emerald Token - Left No Spin Path Minecarts", player),
                 lambda state: state.has("Minecarts",player) and ((char_needs_tags(state, ['strong_floors'], 115)and state.has("Dust Devils",player)) or (char_needs_tags(state, ['strong_floors'], 400))) or
                 char_needs_tags(state, ["stronger_walls",'instant_speed'],-1) or char_needs_tags(state, ["stronger_walls"],400) or (state.has("Dust Devils",player) and char_needs_tags(state, ["stronger_walls"],-1))or
                 char_needs_tags(state, ["stronger_walls",'roll'],-1) and state.has("Red Springs",player))
        add_rule(world.get_location("Arid Canyon (Act 2) Emerald Token - Large Arch Cave Right Ledge", player),
                 lambda state: (state.has("Minecarts",player) and state.has("Dust Devils",player) and state.has("Red Springs",player)) or state.can_reach_location("Arid Canyon (Act 2) Star Emblem",player) or
                               (char_needs_tags(state, ["stronger_walls"],-1) and state.has("Dust Devils",player)) or char_needs_tags(state, ["stronger_walls"],400))
        add_rule(world.get_location("Arid Canyon (Act 2) Emerald Token - Knuckles Dark Path Around Wall", player),
                 lambda state: char_needs_tags(state, ["free_flyer"],600) or
                               (char_needs_tags(state, ["climbs_walls"],100)) or ((char_needs_tags(state, ["climbs_walls"],-1) or (char_needs_tags(state, ['strong_walls',"breaks_spikes","can_use_shields"],-1)and state.has("Whirlwind Shield",player))) and state.has("Yellow Springs",player))
                                )


        if options.difficulty == 0:
            add_rule(world.get_location("Arid Canyon (Act 1) Spade Emblem", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   (state.has("Red Springs",player) and state.has("Rope Hangs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, [],130))) or  # needs ys or jh130
                                   (state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player) and (state.has("Rope Hangs",player)) or char_needs_tags(state, [],300)) or
                                   char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 1) Diamond Emblem", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   (state.has("Red Springs",player) and state.has("Rope Hangs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ["roll"],130))) or  # needs ys or jh130
                                   (state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player) and (state.has("Rope Hangs",player)) or char_needs_tags(state, [],300)) or
                                   char_needs_tags(state, [], 400) or
                                   state.can_reach_location("Arid Canyon (Act 1) Heart Emblem",player))


            add_rule(world.get_location("Arid Canyon (Act 2) Star Emblem", player),
                     lambda state:
                                   state.has("Minecarts", player) and (
                                    (char_needs_tags(state, ['strong_floors','breaks_spikes'], 115) or
                                   char_needs_tags(state, ['strong_floors'], 150)) or
                                   char_needs_tags(state, ['strong_floors', 'breaks_spikes','stronger_walls'], 115) or
                                   char_needs_tags(state, ['strong_floors','stronger_walls'], 150) or
                                    char_needs_tags(state, ["climbs_walls"], -1) or
                                    char_needs_tags(state, [], 250)
                                    ) or
                                   (char_needs_tags(state, ["stronger_walls"], -1) and state.has("Dust Devils", player)) or
                                   char_needs_tags(state, ["stronger_walls",'instant_speed'], -1) or
                                   (char_needs_tags(state, ["stronger_walls",'roll'], -1) and state.has("Red Springs", player))
                                   )
            add_rule(world.get_location("Arid Canyon (Act 2) Heart Emblem", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, ["wall_jump"],-1) and state.has("Yellow Springs",player)) or char_needs_tags(state, ["wall_jump"],200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                                char_needs_tags(state, [], 1600) or
                               char_needs_tags(state, ['instant_speed', "wall_jump"], 100))

            add_rule(world.get_location("Arid Canyon (Act 2) Diamond Emblem", player),#can be gotten w/ instant speed and a bunch of other shit from the other side
                 lambda state: (state.has("Minecarts",player) and ((char_needs_tags(state, ['strong_floors'], 200) and state.has("Red Springs",player)) or char_needs_tags(state, ['strong_floors'], 800))) or
                               char_needs_tags(state, ["stronger_walls"], 800) or
                               ((char_needs_tags(state, ['roll', "stronger_walls"], -1) or char_needs_tags(state, ['instant_speed', "stronger_walls"], -1)) and state.has("Red Springs",player))
                               )


                     #knuckles path can probably backtrack


        else:
            add_rule(world.get_location("Arid Canyon (Act 1) Spade Emblem", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   (state.has("Red Springs",player) and state.has("Rope Hangs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, [],130))) or  # needs ys or jh130
                                   (state.has("Red Springs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ['instant_speed'],-1)) and state.has("Dust Devils",player) and state.has("Rope Hangs",player)) or
                                   (state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player) and (state.has("Rope Hangs",player)) or char_needs_tags(state, [],300)) or
                                   char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 1) Diamond Emblem", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   (state.has("Red Springs",player) and state.has("Rope Hangs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ['roll'],130))) or  # needs ys or jh130
                                   (state.has("Red Springs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, ['instant_speed'],-1)) and state.has("Dust Devils",player) and state.has("Rope Hangs",player)) or
                                   (state.has("Red Springs",player) and state.has("Yellow Springs",player) and state.has("Dust Devils",player) and (state.has("Rope Hangs",player)) or char_needs_tags(state, [],300)) or
                                   state.can_reach_location("Arid Canyon (Act 1) Heart Emblem", player) or
                                   char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 2) Star Emblem", player),
                     lambda state:
                                   (state.has("Minecarts", player) and
                                    (char_needs_tags(state, ['strong_floors','breaks_spikes'], 115) or
                                   char_needs_tags(state, ['strong_floors'], 150)) or
                                   char_needs_tags(state, ['strong_floors', 'breaks_spikes','stronger_walls'], 115) or
                                   char_needs_tags(state, ['strong_floors','stronger_walls'], 150) or
                                    char_needs_tags(state, ["climbs_walls"], -1) or
                                    char_needs_tags(state, [], 250) or
                                   (char_needs_tags(state, ["instant_speed"], 100) and state.has("Dust Devils", player))
                                    ) or
                                   (char_needs_tags(state, ["stronger_walls"], -1) and state.has("Dust Devils", player)) or
                                   char_needs_tags(state, ["stronger_walls",'instant_speed'], -1) or
                                   (char_needs_tags(state, ["stronger_walls",'roll'], -1) and state.has("Red Springs", player))
                                   )
            add_rule(world.get_location("Arid Canyon (Act 2) Heart Emblem", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, ["wall_jump"],-1) and state.has("Yellow Springs",player)) or char_needs_tags(state, ["wall_jump"],200)) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                                char_needs_tags(state, [], 1600) or
                               char_needs_tags(state, ['instant_speed', "wall_jump"], 100) or
                               (state.has("Dust Devils",player) and (char_needs_tags(state, ["badnik_bounce"],-1) and state.has("Yellow Springs",player)) or char_needs_tags(state, ["badnik_bounce"],200)) or
                               char_needs_tags(state, ["badnik_bounce"], 400))

            add_rule(world.get_location("Arid Canyon (Act 2) Diamond Emblem", player),#todo whirlwind shield stuff
                 lambda state: (state.has("Minecarts",player) and ((char_needs_tags(state, ['strong_floors'], 200) and state.has("Red Springs",player)) or char_needs_tags(state, ['strong_floors'], 800))) or
                               char_needs_tags(state, ["stronger_walls"], 800) or
                               ((char_needs_tags(state, ['roll', "stronger_walls"], -1) or char_needs_tags(state, ['instant_speed', "stronger_walls"], -1)) and state.has("Red Springs",player))
                               )


        if options.time_emblems:
            add_rule(world.get_location("Arid Canyon (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Clear", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Time Emblem", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 2) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Arid Canyon (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Clear", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Ring Emblem", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 2) Clear", player))
        if options.oneup_sanity:


            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Top Plank Before Path Split", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   ((state.has("Red Springs",player) or char_needs_tags(state, ['instant_speed'],-1) ) and state.has("Rope Hangs",player)) or
                                   ((state.has("Red Springs",player) and state.has("Yellow Springs",player)) and (char_needs_tags(state, ['instant_speed'],-1) or char_needs_tags(state, ['can_hover'],-1) or state.has("Dust Devils",player) or (char_needs_tags(state, ['can_use_shields'],-1) and state.has("Whirlwind Shield",player)))) or#add badnik bouncing
                                   (char_needs_tags(state, [], 200) and state.has("Dust Devils",player)) or
                                   char_needs_tags(state, [], 400))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area High Broken Road", player),
                     lambda state:
                     (state.has("Red Springs", player) and state.has("Rope Hangs", player) and state.has("Dust Devils", player) and char_needs_tags(state, ['instant_speed'],-1)) or
                     (state.has("Red Springs", player) and (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'],-1) and state.has("Whirlwind Shield",player)) and state.has("Dust Devils",player))) or
                     (state.has("Red Springs", player) and (state.has("Yellow Springs",player) or (state.has("Dust Devils",player) and state.has("Rope Hangs",player))) and char_needs_tags(state, ["can_hover"], -1)) or
                     char_needs_tags(state, ["can_hover"], 400) or
                     (char_needs_tags(state, ["instant_speed"], 400) and state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - High Ledge Above Start", player),
                     lambda state:
                     (char_needs_tags(state, ["strong_floors","pounds_springs","breaks_spikes"], -1) and state.has("Yellow Springs", player) and state.has("Red Springs", player) and state.has("Dust Devils", player)) or
                     (char_needs_tags(state, ["strong_floors"], 200) and state.has("Red Springs", player) and state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 250) or state.can_reach_location("Arid Canyon (Act 1) Club Emblem", player))

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Final Section Under Ceiling Near Checkpoint", player),
                     lambda state: char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["climbs_walls"], -1))

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - End of TNT Path Above Cave", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 400))




            if options.difficulty == 0:
                add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path High Above Exploding Plank", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                    (state.has("Red Springs", player) and (char_needs_tags(state, ['strong_floors','can_hover'],-1) or (char_needs_tags(state, ['strong_floors','can_use_shields'],-1) and state.has("Whirlwind Shield",player))) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'],-1) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player) and state.has("Dust Devils",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'], 200) and state.has("Dust Devils",player)) or
                                   ((state.has("Red Springs",player) and state.has("Yellow Springs",player)) and (char_needs_tags(state, ['instant_speed'],-1) or char_needs_tags(state, ['can_hover'],-1) or state.has("Dust Devils",player) or (char_needs_tags(state, ['can_use_shields'],-1) and state.has("Whirlwind Shield",player)))) or#add badnik bouncing
                                   ((char_needs_tags(state, [], 200) or state.has("Yellow Springs",player)) and state.has("Rope Hangs",player) and state.has("Red Springs",player)) or
                                   char_needs_tags(state, [], 600))



            else:
                add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path High Above Exploding Plank", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                    (state.has("Red Springs", player) and (char_needs_tags(state, ['strong_floors','can_hover'],-1) or (char_needs_tags(state, ['strong_floors','can_use_shields'],-1) and state.has("Whirlwind Shield",player))) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'],-1) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player) and state.has("Dust Devils",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'], 200) and state.has("Dust Devils",player)) or
                                   ((state.has("Red Springs",player) and state.has("Yellow Springs",player)) and (char_needs_tags(state, ['instant_speed'],-1) or char_needs_tags(state, ['can_hover'],-1) or state.has("Dust Devils",player) or (char_needs_tags(state, ['can_use_shields'],-1) and state.has("Whirlwind Shield",player)))) or#add badnik bouncing
                                   ((char_needs_tags(state, [], 200) or state.has("Yellow Springs",player) or char_needs_tags(state, ["instant_speed"], -1)) and state.has("Rope Hangs",player) and state.has("Red Springs",player)) or
                                   char_needs_tags(state, [], 600))



#500jh

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - End of Sneakers Path Brown Pillar", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Heart Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Sneakers Path Stone Pillar Ramp", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Club Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Near Amy Emerald Token", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Emerald Token - Behind Wall and Spikes", player))



            #
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Moving Platform Knuckles Wall", player),#todo stronger walls
                     lambda state: (state.has("Dust Devils", player) and (char_needs_tags(state, ["strong_walls"], 250) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["strong_walls"], -1)))and state.has("Minecarts", player) )or
                                   (state.has("Dust Devils", player) and (char_needs_tags(state, ["strong_walls","wall_jump"], 200) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["strong_walls","wall_jump"], -1)))) or

                                   (state.has("Dust Devils", player) and state.has("Red Springs", player) and state.has("Yellow Springs", player) and ((state.has("Minecarts", player) and char_needs_tags(state, ["strong_walls"], -1)) or char_needs_tags(state, ["strong_walls","wall_jump"], -1)) )or
                                   (state.has("Dust Devils", player) and ((char_needs_tags(state, ["can_use_shields",'wall_jump',"strong_walls"], -1) and state.has("Yellow Springs", player)) or char_needs_tags(state, ["roll","can_use_shields",'wall_jump',"strong_walls"], -1)) and state.has("Whirlwind Shield", player))or
                                    (state.has("Dust Devils", player) and ((char_needs_tags(state, ["can_use_shields","strong_walls"], -1) and state.has("Yellow Springs", player)) or char_needs_tags(state, ["roll","can_use_shields","strong_walls"], 250)) and state.has("Whirlwind Shield", player) and state.has("Minecarts", player) )or

                                   (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields",'roll','wall_jump','strong_walls'], -1) and state.has("Whirlwind Shield", player) and state.has("Dust Devils", player)) or
                     (state.has("Red Springs", player) and (char_needs_tags(state, ["can_use_shields",'roll','strong_walls'], 250)or (char_needs_tags(state, ["can_use_shields",'roll','strong_walls'], -1) and state.has("Yellow Springs", player))) and state.has("Whirlwind Shield", player)) or
                                   (((char_needs_tags(state, ["instant_speed","strong_walls",'strong_walls'], -1) and state.has("Yellow Springs", player))or char_needs_tags(state, ["instant_speed","strong_walls"], 200)) and state.has("Minecarts", player)) or
                                   (state.has("Red Springs", player) and state.has("Yellow Springs", player) and (state.has("Minecarts", player) or state.has("Dust Devils", player))and char_needs_tags(state, ['roll','strong_walls'], -1)) or

                     (char_needs_tags(state, ["instant_speed","strong_walls",'wall_jump'], -1) and state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls","strong_walls"], -1) or
                                   char_needs_tags(state, ["strong_walls"], 400))



            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - High Ledge Near Start", player),
                     lambda state:(state.has("Dust Devils", player) and state.has("Whirlwind Shield", player) and char_needs_tags(state, ["can_use_shields"], -1)) or
                     (state.has("Red Springs", player) and state.has("Whirlwind Shield", player) and char_needs_tags(state, ["roll","can_use_shields"], -1)) or
                    (state.has("Whirlwind Shield", player) and char_needs_tags(state, ["strong_walls","can_use_shields"], -1) and state.has("Red Springs", player) and state.has("Yellow Springs", player))or
                    (char_needs_tags(state, ["strong_walls"], 200) and state.has("Red Springs", player))or
                     char_needs_tags(state, ["instant_speed"], -1) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))


            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path End of Collapsing Plank", player),
                     lambda state: state.has("Dust Devils", player) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Large Arch Cave Thin Planks Right Side", player),
                     lambda state: (state.has("Minecarts", player) and ((state.has("Dust Devils", player) and state.has("Yellow Springs", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)))or
                                   (state.has("Dust Devils", player) and state.has("Yellow Springs", player)and char_needs_tags(state, ['stronger_walls'], -1)) or
                                    char_needs_tags(state, ["climbs_walls",'stronger_walls'], -1) or char_needs_tags(state, ['stronger_walls'], 400)
                     )

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Cliffside Ledge From Start", player),
                     lambda state:(state.has("Dust Devils", player) and state.has("Whirlwind Shield", player) and char_needs_tags(state, ["can_use_shields"], -1)) or
                     (state.has("Red Springs", player) and state.has("Whirlwind Shield", player) and char_needs_tags(state, ["roll","can_use_shields"], -1)) or
                    (state.has("Whirlwind Shield", player) and char_needs_tags(state, ["strong_walls","can_use_shields"], -1) and state.has("Yellow Springs", player))or
                    (char_needs_tags(state, ["strong_walls"], 200))or
                     char_needs_tags(state, ["instant_speed"], -1) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))


            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top Middle", player),
                     lambda state:(state.has("Red Springs", player) and char_needs_tags(state, ["roll"], -1)) or
                     char_needs_tags(state, ["instant_speed"], -1) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Tall Brown Rock Pillar", player),
                     lambda state:(state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Small Cave High Up", player),
                     lambda state:
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 1", player),
                 lambda state: (state.has("Dust Devils",player) and char_needs_tags(state, ['strong_walls'],-1)) or
                                char_needs_tags(state, ['strong_walls','climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll','strong_walls'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed', 'strong_walls'], -1)or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Low Ledge in Cave", player),
                 lambda state: (state.has("Dust Devils",player)) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed'], -1) or
                            char_needs_tags(state, [], 400))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path High Ledge Cave", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, [],200)or state.has("Yellow Springs",player))) or
                               (state.has("Dust Devils", player) and (char_needs_tags(state, ['roll','can_use_shields'], -1)and state.has("Whirlwind Shield",player))) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll','can_use_shields'], -1) and state.has("Red Springs",player)and state.has("Whirlwind Shield",player)) or
                               char_needs_tags(state, ['instant_speed'], -1)or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Visible From Minecarts", player),
                     lambda state: (state.has("Dust Devils", player) and (char_needs_tags(state, [], 200) or (state.has("Yellow Springs", player))) )or
                    (state.has("Dust Devils", player) and (char_needs_tags(state, ["roll","can_use_shields"], -1)) and state.has("Whirlwind Shield", player))or
                    (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields",'roll'], -1) and state.has("Whirlwind Shield", player) and state.has("Dust Devils", player)) or
                     (char_needs_tags(state, ["instant_speed"], -1) and state.has("Dust Devils", player)) or
                                   char_needs_tags(state, ["instant_speed",'stronger_walls'], -1) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)or
                    (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields",'roll','stronger_walls'], -1) and state.has("Whirlwind Shield", player)) or
                    (state.has("Red Springs", player) and char_needs_tags(state, ['roll','stronger_walls'], -1) and state.has("Yellow Springs", player)))


            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Behind TNT Crates Near Diamond Emblem", player),
                     lambda state: (state.has("Minecarts", player) and (state.has("Red Springs", player) and (
                                    (char_needs_tags(state, ['strong_floors','breaks_spikes'], 115) or
                                   char_needs_tags(state, ['strong_floors'], 150)) or
                                   char_needs_tags(state, ['strong_floors', 'breaks_spikes','stronger_walls'], 115) or
                                   char_needs_tags(state, ['strong_floors','stronger_walls'], 150) or
                                    char_needs_tags(state, ["climbs_walls"], -1)))) or
                                   (char_needs_tags(state, [], 250) and state.has("Minecarts", player))or
                                   (char_needs_tags(state, ["stronger_walls"], 200) and state.has("Dust Devils", player)) or
                                   char_needs_tags(state, ["stronger_walls",'instant_speed'], 200) or
                                   (state.has("Red Springs", player) and (char_needs_tags(state, ["stronger_walls",'instant_speed'], -1) or (char_needs_tags(state, ["stronger_walls"], -1) and state.has("Dust Devils", player))))or
                                   (char_needs_tags(state, ["stronger_walls",'roll'], -1) and state.has("Red Springs", player)))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Very High Ledge Between Left and Looping Path", player),
                     lambda state: char_needs_tags(state, [], 800) or char_needs_tags(state, ['climbs_walls'], -1))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - TNT Barrel Ledge Near Star Emblem", player),
                     lambda state:
                                   (state.has("Minecarts", player) and
                                    (char_needs_tags(state, ['strong_floors','breaks_spikes','soft_jump'], 115) or
                                   char_needs_tags(state, ['strong_floors','soft_jump'], 150)) or
                                   char_needs_tags(state, ['strong_floors', 'breaks_spikes','stronger_walls','soft_jump'], 115) or
                                   char_needs_tags(state, ['strong_floors','stronger_walls','soft_jump'], 150) or
                                    char_needs_tags(state, ["climbs_walls"], -1) or
                                    char_needs_tags(state, [], 300)
                                    ) or
                                   (char_needs_tags(state, ["stronger_walls",'soft_jump'], -1) and state.has("Dust Devils", player)) or
                                   char_needs_tags(state, ["stronger_walls",'instant_speed','soft_jump'], -1) or
                                   (char_needs_tags(state, ["stronger_walls",'roll','soft_jump'], -1) and state.has("Red Springs", player))
                                   )




            if options.difficulty == 0:
                add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Heart Emblem 1", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, ['attacks_through_thin_walls'],200)or (state.has("Yellow Springs",player) and char_needs_tags(state, ['attacks_through_thin_walls'],-1)))) or
                               char_needs_tags(state, ['attacks_through_thin_walls'], 400) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                            char_needs_tags(state, [], 1600))
            else:
                add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Heart Emblem 1", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, ['attacks_through_thin_walls'],200)or (state.has("Yellow Springs",player) and char_needs_tags(state, ['attacks_through_thin_walls'],-1)))) or
                            (state.has("Dust Devils",player) and (char_needs_tags(state, ['badnik_bounce'],200)or (state.has("Yellow Springs",player) and char_needs_tags(state, ['badnik_bounce'],-1)))) or
                               char_needs_tags(state, ['attacks_through_thin_walls'], 400) or
                               char_needs_tags(state, ['badnik_bounce'], 400) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                            char_needs_tags(state, [], 1600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Ending Minecarts", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 2) Clear", player))




            # dd -> ys|jh200 -> S2 -> minecarts -> 250jh|ys -> sw
            # dd -> ys|jh200 -> S2 -> dd -> wj -> sw
            # (roll+rs) -> wwsh|(rs+ys) -> ys|roll -> S2




            #rf.assign_rule("Arid Canyon (Act 2) Monitor - Looping Path Small Cave High Up","TAILS | KNUCKLES")
#
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - High Ledge Near Start", "SONIC | TAILS | KNUCKLES | METAL SONIC | WIND")
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - Left Cliffside Ledge From Start","SONIC | TAILS | KNUCKLES | METAL SONIC | WIND")
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top Middle","SONIC | TAILS | KNUCKLES | METAL SONIC")
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - Left Path Moving Platform Knuckles Wall", "KNUCKLES | AMY")
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - Left Path High Ledge Cave", "TAILS | KNUCKLES")
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 1", "KNUCKLES | AMY")
#
            #rf.assign_rule("Arid Canyon (Act 2) Monitor - Very High Ledge Between Left and Looping Path", "TAILS | KNUCKLES")
#
            #if options.difficulty == 0:
            #    rf.assign_rule("Arid Canyon (Act 2) Monitor - Behind TNT Crates Near Diamond Emblem","TAILS | KNUCKLES | AMY | FANG")
            #    rf.assign_rule("Arid Canyon (Act 2) Monitor - TNT Barrel Ledge Near Star Emblem","TAILS | KNUCKLES | AMY | FANG")
            #    rf.assign_rule("Arid Canyon (Act 2) Monitor - Near Heart Emblem 1", "KNUCKLES")
            #    rf.assign_rule("Arid Canyon (Act 1) Monitor - Main Area High Broken Road","TAILS | KNUCKLES")
            #else:
            #    rf.assign_rule("Arid Canyon (Act 1) Monitor - Main Area High Broken Road","SONIC | TAILS | KNUCKLES | METAL SONIC | WIND")
            #    rf.assign_rule("Arid Canyon (Act 2) Monitor - TNT Barrel Ledge Near Star Emblem","TAILS | KNUCKLES | AMY | FANG | WIND")


        if options.superring_sanity:
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - First House", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                    (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'],-1)) or
                                   state.has("Dust Devils", player) or
                                   char_needs_tags(state, [], 115))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Knuckles Path Before Climb 1", player),
                     lambda state: char_needs_tags(state, ["strong_walls"], -1) or
                                   char_needs_tags(state, ["free_flyer"], 500))

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area High Near Broken Road 1", player),
                     lambda state:
                     (state.has("Red Springs", player) and (state.has("Yellow Springs", player) and (((char_needs_tags(state, ['can_use_shields','instant_speed'],-1)or char_needs_tags(state, ['can_use_shields','roll'],-1)) and state.has("Whirlwind Shield",player)) or char_needs_tags(state, ['can_hover'],-1)))) or
                     (state.has("Red Springs", player) and (state.has("Yellow Springs", player) and state.has("Dust Devils", player) and (char_needs_tags(state, ['instant_speed'],-1) or (state.has("Rope Hangs", player) and char_needs_tags(state, ['roll'],-1)))))or
                     (state.has("Rope Hangs", player) and ((state.has("Red Springs", player) and char_needs_tags(state, ['roll'],-1)) or char_needs_tags(state, ['instant_speed'],-1)) and state.has("Dust Devils", player))or
                     (state.has("Red Springs", player) and state.has("Dust Devils", player) and state.has("Rope Hangs", player) and (char_needs_tags(state, ['strong_floors'],200) or (char_needs_tags(state, ['strong_floors','pounds_springs','breaks_spikes'],-1) and state.has("Yellow Springs", player)))) or
                     char_needs_tags(state, ["can_hover"], 400) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Path Ledge Near Rope Hangs", player),
                     lambda state: ((state.has("Red Springs", player) or char_needs_tags(state, ['instant_speed'],-1)) and state.has("Yellow Springs", player) and state.has("Rope Hangs", player))or
                                   (state.has("Yellow Springs", player) and state.has("Red Springs", player) and (char_needs_tags(state, ['can_hover'],-1) or (state.has("Dust Devils", player) and char_needs_tags(state, ['instant_speed'],-1)))) or
                                   char_needs_tags(state, [], 200) or char_needs_tags(state, ["climbs_walls"], -1)
                     )
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Knuckles Path Around Corner", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Heart Emblem", player) or
                                   char_needs_tags(state, ["climbs_walls",'strong_walls'], -1) or
                                   char_needs_tags(state, ["strong_walls",'wall_jump'], -1) or
                                   char_needs_tags(state, ["strong_walls"], 600))

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path High Ledge Before Exploding Ramp 1", player),
                     lambda state: (state.has("Red Springs", player) and state.has("Rope Hangs", player) and char_needs_tags(state, ['can_hover'], -1)) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 900))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - High Ledge Before First Path Split", player),
                     lambda state: (state.has("Red Springs", player) and (char_needs_tags(state, ['strong_floors','pounds_springs'], -1)or char_needs_tags(state, ['strong_floors'], 200))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path Behind Large Crate", player),
                     lambda state: (state.has("Rope Hangs", player) and (char_needs_tags(state, ["instant_speed"], -1)or state.has("Red Springs", player))) or
                                   (state.has("Red Springs", player) and state.has("Yellow Springs", player) and (char_needs_tags(state, ["can_hover"], -1) or state.has("Dust Devils", player) or (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or
                                   (state.has("Dust Devils", player) and char_needs_tags(state, [], 200)) or
                                   char_needs_tags(state, [], 300))


            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Nospin Path Behind Cacti", player),
                     lambda state:
                     (char_needs_tags(state, ["strong_floors","pounds_springs","breaks_spikes"], -1) and state.has("Yellow Springs", player) and state.has("Red Springs", player) and state.has("Dust Devils", player)) or
                     (char_needs_tags(state, ["strong_floors"], 200) and state.has("Red Springs", player) and state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 250) or state.can_reach_location("Arid Canyon (Act 1) Club Emblem", player))

            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area Miss Spring 1", player),
                     lambda state:
                     (state.has("Red Springs", player) and (state.has("Rope Hangs", player)or (state.has("Yellow Springs", player) and (state.has("Dust Devils", player)or char_needs_tags(state, ["can_hover"], -1)or (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)))))) or
                     (state.has("Dust Devils", player) and char_needs_tags(state, [], 200)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 900))



            if options.difficulty == 0:
                add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path Near Exploding Ramp", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                    (state.has("Red Springs", player) and (char_needs_tags(state, ['strong_floors','can_hover'],-1) or (char_needs_tags(state, ['strong_floors','can_use_shields'],-1) and state.has("Whirlwind Shield",player))) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'],-1) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player) and state.has("Dust Devils",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'], 200) and state.has("Dust Devils",player)) or
                                   ((state.has("Red Springs",player) and state.has("Yellow Springs",player)) and (char_needs_tags(state, ['instant_speed'],-1) or char_needs_tags(state, ['can_hover'],-1) or state.has("Dust Devils",player) or (char_needs_tags(state, ['can_use_shields'],-1) and state.has("Whirlwind Shield",player)))) or#add badnik bouncing
                                   ((char_needs_tags(state, [], 200) or state.has("Yellow Springs",player)) and state.has("Rope Hangs",player) and state.has("Red Springs",player)) or
                                   char_needs_tags(state, [], 600))
            else:
                add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path Near Exploding Ramp", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                    (state.has("Red Springs", player) and (char_needs_tags(state, ['strong_floors','can_hover'],-1) or (char_needs_tags(state, ['strong_floors','can_use_shields'],-1) and state.has("Whirlwind Shield",player))) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'],-1) and (state.has("Rope Hangs",player) or (state.has("Yellow Springs",player) and state.has("Dust Devils",player)))) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, ['strong_floors'], 200) and state.has("Dust Devils",player)) or
                                   ((state.has("Red Springs",player) and state.has("Yellow Springs",player)) and (char_needs_tags(state, ['instant_speed'],-1) or char_needs_tags(state, ['can_hover'],-1) or state.has("Dust Devils",player) or (char_needs_tags(state, ['can_use_shields'],-1) and state.has("Whirlwind Shield",player)))) or#add badnik bouncing
                                   ((char_needs_tags(state, [], 200) or state.has("Yellow Springs",player) or char_needs_tags(state, ["instant_speed"], -1)) and state.has("Rope Hangs",player) and state.has("Red Springs",player)) or
                                   char_needs_tags(state, [], 600))


            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area High Near Broken Road 2", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Monitor - Main Area High Near Broken Road 1", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Under Road Before Heart Emblem", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Heart Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Near Spade Emblem", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Spade Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Knuckles Path Before Climb 2", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Monitor - Knuckles Path Before Climb 1", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - TNT Path High Ledge Before Exploding Ramp 2", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Monitor - TNT Path High Ledge Before Exploding Ramp 1", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area Ledge After Plank 2", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Monitor - Main Area Ledge After Plank 1", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area Miss Spring 2", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Monitor - Main Area Miss Spring 1", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Main Area Miss Spring 3", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Monitor - Main Area Miss Spring 1", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Behind Cacti Near Falling Anvil", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Heart Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 1) Monitor - Behind Cacti End of TNT Path", player),
                     lambda state: state.can_reach_location("Arid Canyon (Act 1) Spade Emblem", player))


            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Under Collapsing Plank", player),
                     lambda state: state.has("Dust Devils", player) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Second Platform", player),
                     lambda state: state.has("Dust Devils", player) or char_needs_tags(state, ['instant_speed'], -1) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Behind Plank Near Diamond Emblem", player),
                     lambda state: (state.has("Minecarts", player) and ((state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))) or
                                   (state.has("Dust Devils", player) and char_needs_tags(state, ['stronger_walls'], -1)) or
                                    char_needs_tags(state, ["climbs_walls",'stronger_walls'], -1) or char_needs_tags(state, ['stronger_walls'], 400))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Low Ledge Behind Cacti", player),
                 lambda state: (state.has("Dust Devils",player)) or
                                char_needs_tags(state, [], 400) or
                               (char_needs_tags(state, ['roll'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed'], -1))#knuckles path can probably backtrack
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Large Arch Cave Gap After Spikes", player),#probably needs fitsundergaps/projectile but idc
                     lambda state: (state.has("Minecarts", player) and ((state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))) or
                                   (state.has("Dust Devils", player) and char_needs_tags(state, ['stronger_walls'], -1)) or
                                    char_needs_tags(state, ["climbs_walls",'stronger_walls'], -1) or char_needs_tags(state, ['stronger_walls'], 400))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top 1", player),
                lambda state: (state.has("Red Springs", player) and char_needs_tags(state, ["roll"], -1)) or
                       char_needs_tags(state, ["instant_speed"], -1) or
                       char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Behind Crate Near Spade Emblem", player),
                 lambda state: (state.has("Dust Devils",player)) or
                                char_needs_tags(state, [], 400) or
                               (char_needs_tags(state, ['roll'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed'], -1) or char_needs_tags(state, ["climbs_walls"], -1))#knuckles path can probably backtrack
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Canarivore Path Before Ramp 1", player),
                 lambda state: (state.has("Dust Devils",player) and state.has("Red Springs",player) and state.has("Yellow Springs",player)) or
                                char_needs_tags(state, [], 400) or
                               (char_needs_tags(state, ['roll'], -1) and state.has("Red Springs",player) and state.has("Yellow Springs",player)) or
                               char_needs_tags(state, ['instant_speed'], -1) or
                               (state.has("Dust Devils", player) and state.has("Whirlwind Shield",player) and char_needs_tags(state, ['can_use_shields'], -1)) or
                               (char_needs_tags(state, ['roll','can_use_shields'], -1) and state.has("Red Springs", player)and state.has("Whirlwind Shield", player)))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Tall Plank", player),
                     lambda state: (state.has("Dust Devils", player) and char_needs_tags(state, [], 115)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Large Arch Cave Middle Crates", player),
                     lambda state: (state.has("Minecarts", player) and ((state.has("Dust Devils", player) and state.has("Yellow Springs", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)))or
                                   (state.has("Dust Devils", player) and state.has("Yellow Springs", player)and char_needs_tags(state, ['stronger_walls'], -1)) or
                                    char_needs_tags(state, ["climbs_walls",'stronger_walls'], -1) or char_needs_tags(state, ['stronger_walls'], 400)
                     )
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Below Heart Emblem Area", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, [],200)or state.has("Yellow Springs",player))) or
                               (state.has("Dust Devils", player) and (char_needs_tags(state, ['roll','can_use_shields'], -1)and state.has("Whirlwind Shield",player))) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll','can_use_shields'], -1) and state.has("Red Springs",player)and state.has("Whirlwind Shield",player)) or
                               char_needs_tags(state, ['instant_speed'], -1)or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 2", player),
                 lambda state: (state.has("Dust Devils",player) and char_needs_tags(state, ['strong_walls'],-1)) or
                                char_needs_tags(state, ['strong_walls','climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll','strong_walls'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed', 'strong_walls'], -1)or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Knuckles Path Back Ledge 1", player),
                 lambda state: (char_needs_tags(state, ['strong_walls','can_use_shields','breaks_spikes'],115) and state.has("Whirlwind Shield",player) and state.has("Yellow Springs",player)) or
                                (char_needs_tags(state, ['strong_walls','can_use_shields'],200) and state.has("Whirlwind Shield",player)) or
                                (char_needs_tags(state, ['strong_walls','wall_jump','breaks_spikes'],-1) and state.has("Yellow Springs",player)) or
                                (char_needs_tags(state, ['strong_walls','wall_jump','breaks_spikes'],200)) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Nospin Path After First Minecart 1", player),
                 lambda state:(state.has("Minecarts",player) and
                  ((char_needs_tags(state, ['strong_floors','breaks_spikes'],115)) or
                   (char_needs_tags(state, ['strong_floors'], 150)))) or
                              ((char_needs_tags(state, ['strong_floors', 'breaks_spikes',"stronger_walls"], 115)) or
                               (char_needs_tags(state, ['strong_floors',"stronger_walls"], 150))) or

                                char_needs_tags(state, ['climbs_walls'], -1) or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Ledge Near Rock", player),
                 lambda state: (state.has("Dust Devils",player)) or
                                char_needs_tags(state, [], 400) or
                               (char_needs_tags(state, ['roll'], -1) and state.has("Red Springs",player)) or
                               char_needs_tags(state, ['instant_speed'], -1))#knuckles path can probably backtrack
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Nospin Path Before Second Minecart", player),
                 lambda state:(state.has("Minecarts",player) and
                  ((char_needs_tags(state, ['strong_floors','breaks_spikes'],115)) or
                   (char_needs_tags(state, ['strong_floors'], 150)))) or
                              ((char_needs_tags(state, ['strong_floors', 'breaks_spikes', "stronger_walls"], 115)) or
                               (char_needs_tags(state, ['strong_floors', "stronger_walls"], 150))) or
                                char_needs_tags(state, ['climbs_walls','strong_floors'], -1) or
                            char_needs_tags(state, ['strong_floors'], 600))

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Behind TNT Near End 1", player),#todo stronger walls and shoots_player_blockers
                     lambda state: (state.has("Dust Devils", player) and (char_needs_tags(state, [], 250) or (state.has("Yellow Springs", player)))and state.has("Minecarts", player) )or
                                   (state.has("Dust Devils", player) and (char_needs_tags(state, [], 200) or (state.has("Yellow Springs", player) and char_needs_tags(state, ["wall_jump"], -1)))) or

                                   (state.has("Dust Devils", player) and state.has("Red Springs", player) and state.has("Yellow Springs", player) and ((state.has("Minecarts", player)) or char_needs_tags(state, ["wall_jump"], -1)) )or
                                   (state.has("Dust Devils", player) and ((char_needs_tags(state, ["can_use_shields",'wall_jump'], -1) and state.has("Yellow Springs", player)) or char_needs_tags(state, ["roll","can_use_shields",'wall_jump'], -1)) and state.has("Whirlwind Shield", player))or
                                    (state.has("Dust Devils", player) and ((char_needs_tags(state, ["can_use_shields"], -1) and state.has("Yellow Springs", player)) or char_needs_tags(state, ["roll","can_use_shields"], 250)) and state.has("Whirlwind Shield", player) and state.has("Minecarts", player) )or

                                   (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields",'roll','wall_jump'], -1) and state.has("Whirlwind Shield", player) and state.has("Dust Devils", player)) or
                     (state.has("Red Springs", player) and (char_needs_tags(state, ["can_use_shields",'roll',], 250)or (char_needs_tags(state, ["can_use_shields",'roll'], -1) and state.has("Yellow Springs", player))) and state.has("Whirlwind Shield", player)) or
                                   (((char_needs_tags(state, ["instant_speed"], -1) and state.has("Yellow Springs", player))or char_needs_tags(state, ["instant_speed"], 200)) and state.has("Minecarts", player)) or
                                   (state.has("Red Springs", player) and state.has("Yellow Springs", player) and (state.has("Minecarts", player) or state.has("Dust Devils", player))and char_needs_tags(state, ['roll'], -1)) or

                                          (char_needs_tags(state, ["instant_speed",'wall_jump'], -1) and state.has("Dust Devils", player)) or
                     char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Near Wooden Bridge", player),
                     lambda state: (state.has("Dust Devils", player) and (char_needs_tags(state, [], 200) or (state.has("Yellow Springs", player))) )or
                    (state.has("Dust Devils", player) and (char_needs_tags(state, ["roll","can_use_shields"], -1)) and state.has("Whirlwind Shield", player))or
                    (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields",'roll'], -1) and state.has("Whirlwind Shield", player) and state.has("Dust Devils", player)) or
                     (char_needs_tags(state, ["instant_speed"], -1) and state.has("Dust Devils", player)) or
                                   char_needs_tags(state, ["instant_speed",'stronger_walls'], -1) or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)or
                    (state.has("Red Springs", player) and char_needs_tags(state, ["can_use_shields",'roll','stronger_walls'], -1) and state.has("Whirlwind Shield", player)) or
                    (state.has("Red Springs", player) and char_needs_tags(state, ['roll','stronger_walls'], -1) and state.has("Yellow Springs", player)))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Small Ledge Under Heart Emblem", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, [],200)or state.has("Yellow Springs",player))) or
                               (state.has("Dust Devils", player) and (char_needs_tags(state, ['roll','can_use_shields'], -1)and state.has("Whirlwind Shield",player))) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll','can_use_shields'], -1) and state.has("Red Springs",player)and state.has("Whirlwind Shield",player)) or
                               char_needs_tags(state, ['instant_speed'], -1)or
                            char_needs_tags(state, [], 600))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Climb Wooden Spring Ladder", player),
                     lambda state: (state.has("Dust Devils", player) and (state.has("Yellow Springs", player)or char_needs_tags(state, ["instant_speed",'midair_speed'], -1)))or
                     char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400))

            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Canarivore Path Join Left Path Ledge", player),
                 lambda state: (state.has("Dust Devils",player) and state.has("Red Springs",player) and state.has("Yellow Springs",player)) or
                               (state.has("Dust Devils", player) and (char_needs_tags(state, ['roll','can_use_shields'], -1)and state.has("Whirlwind Shield",player))) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                               (char_needs_tags(state, ['roll','can_use_shields'], -1) and state.has("Red Springs",player)and state.has("Whirlwind Shield",player)) or
                               char_needs_tags(state, ['instant_speed'], -1)or
                            char_needs_tags(state, [], 600))





            if options.difficulty == 0:
                add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Heart Emblem 2", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, ['attacks_through_thin_walls'],200)or (state.has("Yellow Springs",player) and char_needs_tags(state, ['attacks_through_thin_walls'],-1)))) or
                               char_needs_tags(state, ['attacks_through_thin_walls'], 400) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                            char_needs_tags(state, [], 1600))
            else:
                add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Heart Emblem 2", player),
                 lambda state: (state.has("Dust Devils",player) and (char_needs_tags(state, ['attacks_through_thin_walls'],200)or (state.has("Yellow Springs",player) and char_needs_tags(state, ['attacks_through_thin_walls'],-1)))) or
                            (state.has("Dust Devils",player) and (char_needs_tags(state, ['badnik_bounce'],200)or (state.has("Yellow Springs",player) and char_needs_tags(state, ['badnik_bounce'],-1)))) or
                               char_needs_tags(state, ['attacks_through_thin_walls'], 400) or
                               char_needs_tags(state, ['badnik_bounce'], 400) or
                                char_needs_tags(state, ['climbs_walls'], -1) or
                            char_needs_tags(state, [], 1600))


            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Large Arch Cave TNT Behind Crates", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Behind Plank Near Diamond Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Canarivore Path Half Pipe Top 1", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - TNT Barrels Near Star Emblem", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Star Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Canarivore Path Before Ramp 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Canarivore Path Before Ramp 1", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Side Ledge 1", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Behind Crate Near Spade Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Looping Path Side Ledge 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Behind Crate Near Spade Emblem", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Heart Emblem 3", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Near Heart Emblem 2", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 3", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - End Of Left Knuckles Path Around Corner 2", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Knuckles Path Back Ledge 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Left Knuckles Path Back Ledge 1", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Knuckles Path Main Platform", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Left Knuckles Path Back Ledge 1", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Arch Cave Token 1", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Emerald Token - Large Arch Cave Right Ledge", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Near Arch Cave Token 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Emerald Token - Large Arch Cave Right Ledge", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Behind TNT Near End 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Left Path Behind TNT Near End 1", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Left Path Alternate Rail", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Left Path Near Wooden Bridge", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Nospin Path After First Minecart 2", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Nospin Path After First Minecart 1", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Large Arch Cave Guarded By Green Snapper", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Monitor - Large Arch Cave Middle Crates", player))
            add_rule(world.get_location("Arid Canyon (Act 2) Monitor - Crate Before Final Minecart", player),
                lambda state: state.can_reach_location("Arid Canyon (Act 2) Clear", player))

        # Red Volcano
        #fang cant get club emblem
        add_rule(world.get_location("Red Volcano (Act 1) Star Emblem", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
        add_rule(world.get_location("Red Volcano (Act 1) Spade Emblem", player),
                 lambda state: char_needs_tags(state, ["free_flyer"],-1) or
                                char_needs_tags(state, [],800))
        add_rule(world.get_location("Red Volcano (Act 1) Heart Emblem", player),
                 lambda state: state.has("Red Springs",player) or
                               char_needs_tags(state, ["wall_jump"], -1) or
                               char_needs_tags(state, ["climbs_walls"],-1) or
                                char_needs_tags(state, [],800))
        add_rule(world.get_location("Red Volcano (Act 1) Diamond Emblem", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
        add_rule(world.get_location("Red Volcano (Act 1) Club Emblem", player),
                 lambda state: (state.has("Rollout Rocks",player) and char_needs_tags(state, ['spin_walls'],-1) and state.has("Yellow Springs",player)) or
                               char_needs_tags(state, ['spin_walls',"free_flyer"],1400) or
                               char_needs_tags(state, ['spin_walls',"lava_immune"], 150) )

        add_rule(world.get_location("Red Volcano (Act 1) Emerald Token - Rollout Rock Lavafall", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))





        add_rule(world.get_location("Red Volcano (Act 1) Emerald Token - Hidden Ledge Near 4th Checkpoint", player),
                 lambda state: char_needs_tags(state, ["free_flyer"],-1) or
                               (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player) or
                                char_needs_tags(state, [],800)) or
                                state.has("Fang",player))#hardcoded nonsense because fang is unique

        add_rule(world.get_location("Red Volcano (Act 1) Emerald Token - Behind Ending Rocket", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))



        if options.difficulty == 0:
            add_rule(world.get_location("Red Volcano (Act 1) Clear", player),
                     lambda state: (state.has("Rollout Rocks", player) and state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                                    (char_needs_tags(state, ["can_use_shields"],-1) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player) and state.has("Whirlwind Shield", player))or
                                    (char_needs_tags(state, [],150) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player))or
                                   (char_needs_tags(state, ["can_hover"],-1) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player))or
                                   char_needs_tags(state, ["lava_immune"], 150) or
                                   char_needs_tags(state, [], 1400)or
                                   char_needs_tags(state, ["climbs_walls"],-1))



            add_rule(world.get_location("Red Volcano (Act 1) Emerald Token - First Outside Area", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                        char_needs_tags(state, [], 1200) or
                        char_needs_tags(state, ["can_hover"], -1) or
                        (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player))
                     )

        else:
            add_rule(world.get_location("Red Volcano (Act 1) Emerald Token - First Outside Area", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 1200) or
                                   char_needs_tags(state, ["can_hover"], -1) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player) or
                                    char_needs_tags(state, ["can_badnik_bounce",'fits_under_gaps'], -1))
                     )
            add_rule(world.get_location("Red Volcano (Act 1) Clear", player),
                     lambda state: (state.has("Rollout Rocks", player) and state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                                    (char_needs_tags(state, ["can_use_shields"],-1) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player) and state.has("Whirlwind Shield", player))or
                                    (char_needs_tags(state, [],150) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player))or
                                   (char_needs_tags(state, ["badnik_bounce"],-1) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player)) or
                                   (char_needs_tags(state, ["badnik_bounce","midair_speed"], -1) and state.has("Yellow Springs", player))or
                                   (char_needs_tags(state, ["can_hover"],-1) and state.has("Rollout Rocks", player) and state.has("Yellow Springs", player))or
                                   char_needs_tags(state, ["lava_immune"], 150) or
                                   char_needs_tags(state, [], 1400)or
                                   char_needs_tags(state, ["climbs_walls"],-1))

        if options.time_emblems:
            add_rule(world.get_location("Red Volcano (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Red Volcano (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))

        if options.oneup_sanity:

            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Lava Waves Pillar", player),
                     lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Flame Jets Room Ledge", player),
                     lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Behind Pillar Near End", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Near Heart Emblem", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Heart Emblem", player))



        if options.superring_sanity:

            add_rule(world.get_location("Red Volcano (Act 1) Monitor - First Outside Area Tall Middle Rock", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 200) or
                                   (char_needs_tags(state, ["can_use_shields"], 115) and state.has("Whirlwind Shield",player) or
                                    (char_needs_tags(state, ["spin_walls",'fits_under_gaps'], -1) and state.has("Yellow Springs",player))))

            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Final Path Split Ledge", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Clear", player))
            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Near Lavafall Token 1", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Emerald Token - Rollout Rock Lavafall", player))
            add_rule(world.get_location("Red Volcano (Act 1) Monitor - Near Lavafall Token 2", player),
                 lambda state: state.can_reach_location("Red Volcano (Act 1) Emerald Token - Rollout Rock Lavafall", player))

        # Egg Rock
        add_rule(world.get_location("Egg Rock (Act 1) Clear", player),
                 lambda state: state.has("Zoom Tubes",player) and
                                  (state.has("Red Springs",player) and (char_needs_tags(state, [],300) or state.has("Yellow Springs",player)) or
                                char_needs_tags(state, [],800) or char_needs_tags(state, ["climbs_walls"],-1) or char_needs_tags(state, ["wall_jump"],-1) or#walljumps,climb,walljump 800jump
                               (state.has("Yellow Springs",player) and char_needs_tags(state, ['fits_under_gaps'], -1)) or char_needs_tags(state, ['fits_under_gaps'], 800) or char_needs_tags(state, ["climbs_walls",'fits_under_gaps'],-1) or char_needs_tags(state,["wall_jump",'fits_under_gaps'], -1)
                                ))#ys or the other stuff

#spin path requires zoom tubes, ys, 350jump or climb or wj

        add_rule(world.get_location("Egg Rock (Act 1) Star Emblem", player),
                 lambda state: (state.has("Yellow Springs",player) and char_needs_tags(state, ['fits_under_gaps'], -1)) or char_needs_tags(state, ['fits_under_gaps'], 800) or char_needs_tags(state, ["climbs_walls",'fits_under_gaps'],-1) or char_needs_tags(state,["wall_jump",'fits_under_gaps'], -1))

        add_rule(world.get_location("Egg Rock (Act 1) Spade Emblem", player),
                 lambda state: char_needs_tags(state, ['fits_under_gaps',"climbs_walls"],-1) or
                                char_needs_tags(state, ['fits_under_gaps'],300))

        add_rule(world.get_location("Egg Rock (Act 1) Diamond Emblem", player),
                 lambda state: state.has("Red Springs",player) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, [], 800))

        add_rule(world.get_location("Egg Rock (Act 1) Club Emblem", player),
                 lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))

        add_rule(world.get_location("Egg Rock (Act 1) Emerald Token - Moving Platforms", player),
                 lambda state: state.can_reach_location("Egg Rock (Act 1) Star Emblem", player))
        add_rule(world.get_location("Egg Rock (Act 1) Emerald Token - Gravity Conveyor Belts", player),
                 lambda state: state.can_reach_location("Egg Rock (Act 1) Diamond Emblem", player))

        add_rule(world.get_location("Egg Rock (Act 2) Clear", player),
                 lambda state: state.has("Zoom Tubes", player))
        add_rule(world.get_location("Egg Rock (Act 2) Star Emblem", player),
                 lambda state: state.has("Zoom Tubes",player) or char_needs_tags(state, [], 150) or char_needs_tags(state, ["climbs_walls"], -1))#requires invincibilty
        add_rule(world.get_location("Egg Rock (Act 2) Spade Emblem", player),
                 lambda state: state.has("Zoom Tubes",player))

        add_rule(world.get_location("Egg Rock (Act 2) Diamond Emblem", player),
                 lambda state: state.has("Zoom Tubes",player))

        add_rule(world.get_location("Egg Rock (Act 2) Club Emblem", player),
                 lambda state: state.has("Zoom Tubes",player) and (char_needs_tags(state, ["instant_speed"], -1) or
                                char_needs_tags(state, ["free_flyer"], -1) or
                                char_needs_tags(state, ["can_hover"], -1)))

        add_rule(world.get_location("Egg Rock (Act 2) Emerald Token - Skip Gravity Pad", player),
                 lambda state: state.has("Zoom Tubes",player))

        add_rule(world.get_location("Egg Rock (Act 2) Emerald Token - Disco Room", player),
                 lambda state: state.has("Zoom Tubes",player) and char_needs_tags(state, ['fits_under_gaps'], -1))

        if options.difficulty == 0:
            add_rule(world.get_location("Egg Rock (Act 1) Heart Emblem", player),
                     lambda state:  state.has("Zoom Tubes",player) and char_needs_tags(state, [], 1000))
            add_rule(world.get_location("Egg Rock (Act 2) Heart Emblem", player),
                     lambda state: state.has("Zoom Tubes", player) and (char_needs_tags(state, ["climbs_walls"], -1) or
                                                                        char_needs_tags(state, [], 1200)))
        else:
            add_rule(world.get_location("Egg Rock (Act 1) Heart Emblem", player),
                     lambda state:  state.has("Zoom Tubes",player) and (char_needs_tags(state, [], 1000) or
                     char_needs_tags(state, ['strong_walls',"climbs_walls"], -1)))
            add_rule(world.get_location("Egg Rock (Act 2) Heart Emblem", player),
                     lambda state: state.has("Zoom Tubes", player) and (char_needs_tags(state, ["climbs_walls"], -1) or
                                                                        char_needs_tags(state, [], 1200) or
                                                                        char_needs_tags(state, ["wall_jump"], -1))
                                                                        )

        if options.time_emblems:
            add_rule(world.get_location("Egg Rock (Act 1) Time Emblem", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 2) Time Emblem", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Egg Rock (Act 1) Ring Emblem", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 2) Ring Emblem", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Clear", player))

        if options.oneup_sanity:

            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Spin Path Crushers Corner", player),
                     lambda state:  char_needs_tags(state, ['fits_under_gaps'], -1))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Spin Path Guarded by Spincushion", player),
                     lambda state:  char_needs_tags(state, ['fits_under_gaps'], -1))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Tails Path in Lava", player),
                 lambda state: state.has("Zoom Tubes",player) and (state.has("Red Springs",player) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, [], 800)))





            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Near Diamond Emblem 1", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Diamond Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Near Star Emblem 1", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Near End Behind Blue Pillar", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Gravity Lava Room", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Monitor - Near End Behind Blue Pillar", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 1", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Club Emblem", player))

            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 1", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Left Path Behind Blue Pillars", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["wall_jump"], -1) or char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, [], 115) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 1", player),
                 lambda state: state.has("Zoom Tubes",player) )

            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Air Lock Room Small Ledge", player),
                 lambda state: state.has("Zoom Tubes",player) and (state.has("Rope Hangs",player) and (state.has("Yellow Springs",player) or char_needs_tags(state, [], 200))) or char_needs_tags(state, ['climbs_walls'], -1) or
                               char_needs_tags(state, ['wall_jump'], 200) or (char_needs_tags(state, ['wall_jump'], -1) and state.has("Yellow Springs",player)))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Left Path Surrounded by Eggman Monitors", player),
                 lambda state: state.has("Zoom Tubes",player) )



            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 1", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Near Spade Emblem", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Spade Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Near Star Emblem 1", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Near Star Emblem 1", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Disco Room 1", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Emerald Token - Disco Room", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Disco Room 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Emerald Token - Disco Room", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Skip Gravity Pad Near Token", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Emerald Token - Skip Gravity Pad", player))

            if options.difficulty == 0:
                add_rule(world.get_location("Egg Rock (Act 2) Monitor - Top of Turret Room", player),
                    lambda state: state.has("Zoom Tubes", player) and (char_needs_tags(state, ["climbs_walls"],-1) or char_needs_tags(state, ["wall_jump"],-1) or
                                                                       char_needs_tags(state, [], 200)))
            else:
                add_rule(world.get_location("Egg Rock (Act 2) Monitor - Top of Turret Room", player),
                    lambda state: state.has("Zoom Tubes", player) and (char_needs_tags(state, ["climbs_walls"],-1) or char_needs_tags(state, ["wall_jump"],-1) or
                                                                       char_needs_tags(state, [], 200) or char_needs_tags(state, ['can_hover'], -1)))

        if options.superring_sanity:

            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Main Path End 1", player),
                 lambda state: state.has("Zoom Tubes",player) and
                               char_needs_tags(state, ["climbs_walls"],-1) or char_needs_tags(state, ["wall_jump"],-1) or
                               (state.has("Yellow Springs",player) and char_needs_tags(state, ['fits_under_gaps'], -1)) or char_needs_tags(state, ['fits_under_gaps'], 400)
                                )
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Spin Path Crushers R", player),
                     lambda state:  char_needs_tags(state, ['fits_under_gaps'], -1))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Spin Path Crushers L", player),
                     lambda state:  char_needs_tags(state, ['fits_under_gaps'], -1))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Spin Path Gravity Room", player),
                     lambda state:  char_needs_tags(state, ['fits_under_gaps'], -1))

            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Knuckles Path Before Wall Conveyors", player),
                 lambda state: state.has("Zoom Tubes",player) and
                               (char_needs_tags(state, ["strong_walls",'climbs_walls'],-1) or
                                (state.has("Red Springs", player) and (char_needs_tags(state, ["strong_walls","breaks_spikes"],250) or char_needs_tags(state, ["strong_walls","lava_immune"],250))) or
                                (char_needs_tags(state, ["strong_walls",'free_flyer'],800))))




            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Near Star Emblem 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Near Star Emblem 3", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - 2D Area Zoom Tube Top", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Blue Pillar Before End", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Outside Air Pocket Near End", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Club Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Appearing Blocks Area Corner", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 3", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Monitor - 2D Area Behind Last Zoom Tube 2", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Near Diamond Emblem 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Diamond Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Metal Beam Before End", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Right Before End", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 1) Monitor - Main Path End 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 1) Monitor - Main Path End 1", player))

            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 2", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Outside Ledge 1", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Second Zoom Tube Exit", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Low Ledge", player),
                 lambda state: state.has("Zoom Tubes",player) )



            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 3", player),
                 lambda state: state.has("Zoom Tubes",player) )

            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Elevator Shaft", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Turret Room Back Right", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Auto Gravity Area Pop-up Turrets", player),
                 lambda state: state.has("Zoom Tubes",player) )
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Air Lock Room Floor", player),
                 lambda state: state.has("Zoom Tubes",player) and (char_needs_tags(state, ['climbs_walls'],-1) or char_needs_tags(state, [],115) or
                                                                   char_needs_tags(state, ['wall_jump'],-1)) or state.has("Rope Hangs",player))


            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 3", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Monitor - Auto Gravity Area Behind First Zoom Tube 2", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Outside Ledge 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Monitor - 2D Area Outside Ledge 1", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 4", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Monitor - 2D Area Above Air Pocket 3", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Near Star Emblem 2", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Near Star Emblem 3", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Star Emblem", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Near Zoom Tube Before Final Teleporter", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Clear", player))
            add_rule(world.get_location("Egg Rock (Act 2) Monitor - Turret Room Back Left", player),
                     lambda state: state.can_reach_location("Egg Rock (Act 2) Monitor - Turret Room Back Right", player))


        # Black Core - Nothing until rolling/objects are locked




        # Frozen Hillside/ other bonus stages go here
        add_rule(world.get_location("Frozen Hillside Clear", player),
                 lambda state: (state.has("Yellow Springs",player)) or
                               char_needs_tags(state, [], 200) or
                               char_needs_tags(state, ["climbs_walls"], -1))

        add_rule(world.get_location("Frozen Hillside Star Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and char_needs_tags(state, ['fits_under_gaps'], -1)) or
                               char_needs_tags(state, ['fits_under_gaps'], 250) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1))
        add_rule(world.get_location("Frozen Hillside Spade Emblem", player),
                 lambda state: (state.has("Yellow Springs",player)) or
                               char_needs_tags(state, [], 200) or
                               char_needs_tags(state, ["climbs_walls"], -1))
        add_rule(world.get_location("Frozen Hillside Heart Emblem", player),
                 lambda state: (state.has("Yellow Springs",player) and char_needs_tags(state, ["weak_walls"], -1)) or
                               char_needs_tags(state, ["weak_walls"], 200) or
                               char_needs_tags(state, ["climbs_walls","weak_walls"], -1))
        add_rule(world.get_location("Frozen Hillside Diamond Emblem", player),
                 lambda state: (state.has("Yellow Springs",player) and char_needs_tags(state, [], 140)) or
                               char_needs_tags(state, [], 200) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                            (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield",player)))

        if options.difficulty == 0:
            add_rule(world.get_location("Frozen Hillside Club Emblem", player),
                     lambda state:  char_needs_tags(state, ["weak_walls"], 200) or
                                   char_needs_tags(state, ["climbs_walls", "weak_walls"], -1))
        else:
            add_rule(world.get_location("Frozen Hillside Club Emblem", player),
                     lambda state: (state.has("Yellow Springs", player) and char_needs_tags(state, ["weak_walls","badnik_bounce"],-1)) or
                                   char_needs_tags(state, ["weak_walls"], 200) or
                                   char_needs_tags(state, ["climbs_walls", "weak_walls"], -1))

        if options.time_emblems:
            add_rule(world.get_location("Frozen Hillside Time Emblem", player),
                     lambda state: state.can_reach_location("Frozen Hillside Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Frozen Hillside Ring Emblem", player),
                     lambda state: state.can_reach_location("Frozen Hillside Clear", player))

        if options.oneup_sanity:
            add_rule(world.get_location("Frozen Hillside Monitor - First Snow Field Behind Ice", player),
                     lambda state:  char_needs_tags(state, ["weak_walls"], -1))
            add_rule(world.get_location("Frozen Hillside Monitor - Final Path Ledge Behind Ice", player),
                     lambda state: state.can_reach_location("Frozen Hillside Club Emblem", player))

        if options.superring_sanity:
            add_rule(world.get_location("Frozen Hillside Monitor - Ledge Near Start 1", player),
                     lambda state: (state.has("Yellow Springs", player)) or
                                   char_needs_tags(state, [], 250) or
                                   char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Frozen Hillside Monitor - Right Path Inside Ice", player),
                     lambda state: (state.has("Yellow Springs", player)) or
                                   char_needs_tags(state, [], 200) or
                                   char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Frozen Hillside Monitor - Left Path Cave Ledge", player),
                     lambda state: (state.has("Yellow Springs", player)) or
                                   char_needs_tags(state, [], 250) or
                                   char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Frozen Hillside Monitor - First Area Tall Pillar", player),
                     lambda state: (state.has("Yellow Springs", player)) or
                                   char_needs_tags(state, [], 300) or
                                   char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Frozen Hillside Monitor - First Area Lake Ledge", player),
                     lambda state: (state.has("Yellow Springs", player)) or
                                   char_needs_tags(state, [], 200) or
                                   char_needs_tags(state, ["climbs_walls"], -1))




            add_rule(world.get_location("Frozen Hillside Monitor - Ledge Near Start 2", player),
                     lambda state: state.can_reach_location("Frozen Hillside Monitor - Ledge Near Start 1", player))
            add_rule(world.get_location("Frozen Hillside Monitor - Left Path Flowing Snow Ledge", player),
                     lambda state: state.can_reach_location("Frozen Hillside Monitor - Left Path Cave Ledge", player))
            add_rule(world.get_location("Frozen Hillside Monitor - Frozen Lake Middle Platform", player),
                     lambda state: state.can_reach_location("Frozen Hillside Spade Emblem", player))
            add_rule(world.get_location("Frozen Hillside Monitor - Right Path Flowing Snow Behind Pillar", player),
                     lambda state: state.can_reach_location("Frozen Hillside Spade Emblem", player))
            add_rule(world.get_location("Frozen Hillside Monitor - Right Path Flowing Snow Lower Ice", player),
                     lambda state: state.can_reach_location("Frozen Hillside Spade Emblem", player))
            add_rule(world.get_location("Frozen Hillside Monitor - Converging Paths Under Overhang", player),
                     lambda state: state.can_reach_location("Frozen Hillside Clear", player))



        #pipe towers
        #yellow springs and red springs or 200jh and red springs or 800jh
        add_rule(world.get_location("Pipe Towers Clear", player),
                 lambda state: (state.has("Red Springs", player) and
                (state.has("Yellow Springs", player)) or char_needs_tags(state, ["pounds_springs"], -1) or char_needs_tags(state, [], 200) or (char_needs_tags(state, ['can_use_shields'], 130) and state.has("Whirlwind Shield", player))) or
                char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))

        add_rule(world.get_location("Pipe Towers Star Emblem", player),
                 lambda state: (state.has("Red Springs", player) and
                                (state.has("Yellow Springs", player) and char_needs_tags(state,[],200)) or (char_needs_tags(state, ['can_use_shields'], 130) and state.has("Whirlwind Shield", player))) or
                               char_needs_tags(state, [], 800))
        add_rule(world.get_location("Pipe Towers Spade Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], 200) or
                char_needs_tags(state, [], 800) or (state.has("Red Springs", player) and
                (state.has("Yellow Springs", player) and char_needs_tags(state, ["pounds_springs"], -1)) or char_needs_tags(state, ["pounds_springs"], 200) or (char_needs_tags(state, ['can_use_shields',"pounds_springs"], 130) and state.has("Whirlwind Shield", player))))
        add_rule(world.get_location("Pipe Towers Heart Emblem", player),
                 lambda state: char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ['wall_jump'], -1) or
                char_needs_tags(state, [], 1600))
        add_rule(world.get_location("Pipe Towers Diamond Emblem", player),
                 lambda state: state.can_reach_location("Pipe Towers Clear", player))
        add_rule(world.get_location("Pipe Towers Club Emblem", player),
                 lambda state: state.can_reach_location("Pipe Towers Clear", player))





        if options.time_emblems:
            add_rule(world.get_location("Pipe Towers Time Emblem", player),
                     lambda state: state.can_reach_location("Pipe Towers Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Pipe Towers Ring Emblem", player),
                     lambda state: state.can_reach_location("Pipe Towers Clear", player))
        if options.oneup_sanity:
            add_rule(world.get_location("Pipe Towers ? Block - Purple Mushroom Skylight", player),
                 lambda state: (state.has("Red Springs", player) and
                (state.has("Yellow Springs", player)) or char_needs_tags(state, ["pounds_springs"], -1) or char_needs_tags(state, [], 200) or (char_needs_tags(state, ['can_use_shields'], 130) and state.has("Whirlwind Shield", player))) or
                char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 800))

            add_rule(world.get_location("Pipe Towers ? Block - Ceiling Hole Near Flowing Water", player),
                 lambda state: state.can_reach_location("Pipe Towers Clear", player))
            add_rule(world.get_location("Pipe Towers ? Block - Near Diamond Emblem", player),
                 lambda state: state.can_reach_location("Pipe Towers Diamond Emblem", player))
            add_rule(world.get_location("Pipe Towers ? Block - Flowing Water Alt Path on Ledge", player),
                 lambda state: state.can_reach_location("Pipe Towers Clear", player))
            add_rule(world.get_location("Pipe Towers ? Block - Underground Thwomp Room", player),
                 lambda state: state.can_reach_location("Pipe Towers Clear", player))

        #none for forest fortress (yet)
        add_rule(world.get_location("Forest Fortress Clear", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Red Springs", player)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, [], 250)) or
                 char_needs_tags(state, [], 500) or
                 char_needs_tags(state, ["climbs_walls"], -1))


        add_rule(world.get_location("Forest Fortress Star Emblem", player),
                 lambda state: char_needs_tags(state, ['spin_walls'], -1))
        add_rule(world.get_location("Forest Fortress Spade Emblem", player),
                 lambda state: state.has("Swinging Maces", player) or char_needs_tags(state, [], 250) or
                 char_needs_tags(state, ["climbs_walls"], -1))
        add_rule(world.get_location("Forest Fortress Heart Emblem", player),
                 lambda state: state.has("Swinging Maces", player) or char_needs_tags(state, ['fits_under_gaps'], 250) or
                 char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1))
        add_rule(world.get_location("Forest Fortress Diamond Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Red Springs", player)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, [], 250)) or
                 char_needs_tags(state, [], 500) or
                 char_needs_tags(state, ["climbs_walls"], -1))
        add_rule(world.get_location("Forest Fortress Club Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Red Springs", player) and char_needs_tags(state, ['spin_walls'], -1)) or
                                (state.has("Swinging Maces", player) and state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, [], 250)) or
                 char_needs_tags(state, [], 500) or
                 char_needs_tags(state, ["climbs_walls"], -1))

        if options.time_emblems:
            add_rule(world.get_location("Forest Fortress Time Emblem", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Forest Fortress Ring Emblem", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))

        if options.oneup_sanity:

            add_rule(world.get_location("Forest Fortress Monitor - Near Hanging Wood Bridge 1", player),
                 lambda state: (state.has("Swinging Maces", player)) or
                 char_needs_tags(state, [], 110) or
                 char_needs_tags(state, ["instant_speed"], -1) or
                 char_needs_tags(state, ["climbs_walls"], -1))

            add_rule(world.get_location("Forest Fortress Monitor - High Ledge Before Second Checkpoint", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Yellow Springs", player) and char_needs_tags(state, ['spin_walls'], -1)) or
                               (state.has("Swinging Maces", player) and char_needs_tags(state, ['spin_walls'], 400)) or
                 char_needs_tags(state, [], 500) or
                 char_needs_tags(state, ["climbs_walls"], -1))

            add_rule(world.get_location("Forest Fortress Monitor - In Ceiling After Final Checkpoint", player),
                 lambda state: char_needs_tags(state, ["strong_walls"], 500) or
                 char_needs_tags(state, ["climbs_walls","strong_walls"], -1))



            add_rule(world.get_location("Forest Fortress Monitor - Low Ledge Before Goal 1", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))
            add_rule(world.get_location("Forest Fortress Monitor - High Ledge Before Second Checkpoint", player),
                 lambda state: char_needs_tags(state, ['strong_walls'], 500) or
                 char_needs_tags(state, ["climbs_walls","strong_walls"], -1))
            add_rule(world.get_location("Forest Fortress Monitor - Trees Near Diamond Emblem", player),
                     lambda state: state.can_reach_location("Forest Fortress Diamond Emblem", player))

        if options.superring_sanity:
            add_rule(world.get_location("Forest Fortress Monitor - Ledge Near First Swinging Mace", player),
                 lambda state: (state.has("Swinging Maces", player)) or
                 char_needs_tags(state, [], 250) or
                 char_needs_tags(state, ["instant_speed"], -1) or
                 char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Forest Fortress Monitor - Main Path Ring Circle", player),
                 lambda state: (state.has("Swinging Maces", player)) or
                 char_needs_tags(state, [], 110) or
                 char_needs_tags(state, ["instant_speed"], -1) or
                 char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Forest Fortress Monitor - Near Hanging Wood Bridge 2", player),
                 lambda state: (state.has("Swinging Maces", player)) or
                 char_needs_tags(state, [], 110) or
                 char_needs_tags(state, ["instant_speed"], -1) or
                 char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Forest Fortress Monitor - Overgrown Ledge Right Path 1", player),
                 lambda state: (state.has("Swinging Maces", player)) or
                 char_needs_tags(state, [], 250) or
                 char_needs_tags(state, ["instant_speed"], -1) or
                 char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Forest Fortress Monitor - Inside Tower Near End", player),
                     lambda state: (state.has("Swinging Maces", player) and state.has("Red Springs", player)) or
                                   (state.has("Red Springs", player) and char_needs_tags(state, [], 250)) or
                                   char_needs_tags(state, [], 500) or
                                   char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Forest Fortress Monitor - Tower Before Club Emblem", player),
                 lambda state: (state.has("Swinging Maces", player) and state.has("Red Springs", player) and char_needs_tags(state, ['spin_walls'], -1)) or
                               (state.has("Red Springs", player) and char_needs_tags(state, ['spin_walls'], 250)) or



                 char_needs_tags(state, [], 500) or
                 char_needs_tags(state, ["climbs_walls"], -1))





            add_rule(world.get_location("Forest Fortress Monitor - Near Hanging Wood Bridge 3", player),
                     lambda state: state.can_reach_location("Forest Fortress Monitor - Near Hanging Wood Bridge 2", player))
            add_rule(world.get_location("Forest Fortress Monitor - Main Path Tree Pillar", player),
                     lambda state: state.can_reach_location("Forest Fortress Monitor - Main Path Ring Circle", player))
            add_rule(world.get_location("Forest Fortress Monitor - First Castle Wall Near Water", player),
                     lambda state: state.can_reach_location("Forest Fortress Spade Emblem", player))
            add_rule(world.get_location("Forest Fortress Monitor - First Castle Wall Underwater", player),
                     lambda state: state.can_reach_location("Forest Fortress Spade Emblem", player))
            add_rule(world.get_location("Forest Fortress Monitor - Castle Lake Ledge", player),
                     lambda state: state.can_reach_location("Forest Fortress Spade Emblem", player))
            add_rule(world.get_location("Forest Fortress Monitor - Vertical Mace Jump Ledge", player),
                     lambda state: state.can_reach_location("Forest Fortress Spade Emblem", player))
            add_rule(world.get_location("Forest Fortress Monitor - Before Final Checkpoint", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))
            add_rule(world.get_location("Forest Fortress Monitor - Low Ledge Before Goal 2", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))
            add_rule(world.get_location("Forest Fortress Monitor - Low Ledge Before Goal 3", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))
            add_rule(world.get_location("Forest Fortress Monitor - Spike Room Near Yellow Spring", player),
                     lambda state: state.can_reach_location("Forest Fortress Monitor - Overgrown Ledge Right Path 1", player))
            add_rule(world.get_location("Forest Fortress Monitor - Near Club Emblem 1", player),
                     lambda state: state.can_reach_location("Forest Fortress Club Emblem", player))
            add_rule(world.get_location("Forest Fortress Monitor - Near Club Emblem 2", player),
                     lambda state: state.can_reach_location("Forest Fortress Club Emblem", player))
            add_rule(world.get_location("Forest Fortress Monitor - Overgrown Ledge Right Path 2", player),
                     lambda state: state.can_reach_location("Forest Fortress Monitor - Overgrown Ledge Right Path 1", player))
            add_rule(world.get_location("Forest Fortress Monitor - Before Final Spring Chain", player),
                     lambda state: state.can_reach_location("Forest Fortress Clear", player))
            add_rule(world.get_location("Forest Fortress Monitor - Castle Lake Underwater", player),
                     lambda state: state.can_reach_location("Forest Fortress Spade Emblem", player))

        add_rule(world.get_location("Final Demo Emerald Token - Greenflower (Act 1) Breakable Wall Near Bridge", player),
                 lambda state: char_needs_tags(state, ['spin_walls'], -1))
        add_rule(world.get_location("Final Demo Emerald Token - Greenflower (Act 2) Under Bridge Near End", player),
            lambda state: state.has("Red Springs", player) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
        add_rule(world.get_location("Final Demo Emerald Token - Greenflower (Act 2) Underwater Cave", player),
            lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                          char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))

        add_rule(world.get_location("Final Demo Emerald Token - Techno Hill (Act 1) On Pipes", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, [], 425))
        add_rule(world.get_location("Final Demo Emerald Token - Techno Hill (Act 1) Alt Path Fans", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) and char_needs_tags(state, ['fits_under_gaps'], -1)) or char_needs_tags(state, ['fits_under_gaps'], 250)) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, ['fits_under_gaps'], 425))

        add_rule(world.get_location("Final Demo Emerald Token - Techno Hill (Act 2) Breakable Wall", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 425))
        add_rule(world.get_location("Final Demo Emerald Token - Techno Hill (Act 2) Under Poison Near End", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 425))
        add_rule(world.get_location("Final Demo Emerald Token - Castle Eggman (Act 1) Small Lake Near Start", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 425))
        add_rule(world.get_location("Final Demo Emerald Token - Castle Eggman (Act 1) Small Lake Near Start", player),
                 lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 425))
        add_rule(world.get_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player),
                 lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 600))
        add_rule(world.get_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player),
                 lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 600))
        add_rule(world.get_location("Final Demo Clear", player),
                 lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                               char_needs_tags(state, [], 600))


        if options.oneup_sanity:

            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Skylight in 2nd Cave", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 1500))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Open Area Small Cave", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Greenflower (Act 2) Under Bridge Near End", player))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) Barrels Across Poison Lake", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))

            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 2) Ledge Near End", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 2) In Poison Near End", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Techno Hill (Act 2) Ledge Near End", player))

            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) On Castle Wall", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) On Castle Wall", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 600))

            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Spring Secret Cave 1", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 600))

            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) High Ledge Near Start", player),
                     lambda state: (state.has("Red Springs", player) and char_needs_tags(state, [], 250)) or
                                   (state.has("Red Springs", player) and state.has("Yellow Springs", player) and state.has("Whirlwind Shield", player)and char_needs_tags(state, [], 110))or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))

            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Spring Secret Cave 2", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Castle Eggman (Act 1) Red Spring Secret Cave 1", player))

            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 1", player),
                lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, [], 600))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard on Platform 1", player),
                lambda state: (state.has("Red Springs", player) and state.has("Yellow Springs", player)) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, [], 600))



            add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Start", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))
            add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Cave Near Falling Platforms", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, ["free_flyer"], 200) or
                              char_needs_tags(state, [], 600))
            add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 1", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))

            add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Cave Near Falling Platforms", player),
                     lambda state: (state.has("Yellow Springs", player) and (
                                 char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"],-1))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, ["wall_jump"], -1) or
                                   char_needs_tags(state, ["free_flyer"], 200) or
                                   char_needs_tags(state, [], 600))


            if options.difficulty == 0:
                add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Start", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))
                add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 1", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))
            else:
                add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Start", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))
                add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 1", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))


        if options.superring_sanity:
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 1", player),
                     lambda state: char_needs_tags(state, ["climbs_walls"], 300) or
                                   char_needs_tags(state, [], 600))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 1) Bridge Lake Top Ledge", player),
                     lambda state: state.has("Yellow Springs", player) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or
                                   char_needs_tags(state, [], 150) or
                                   (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Whirlwind Shield", player)))


            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 2", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 3", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 1) First Cave Skylight 1", player))

            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 1", player),
                     lambda state: state.has("Red Springs", player) or char_needs_tags(state, ["climbs_walls"],-1) or char_needs_tags(state, [],800))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Main Path Near Springs", player),
                     lambda state: state.has("Red Springs", player) or char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player),
                     lambda state: (state.has("Red Springs", player) and char_needs_tags(state, [],300)) or char_needs_tags(state, ["climbs_walls"],-1) or char_needs_tags(state, [],800))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Fence Near Spring Chain", player),
                     lambda state: (state.has("Red Springs", player)) or state.has("Yellow Springs", player) or
                                   char_needs_tags(state,["climbs_walls"],-1) or char_needs_tags(state, [], 400))


            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 2", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 1", player))

            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 2", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 3", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 4", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 5", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 6", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 7", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))
            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 8", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Very High Alcove 1", player))

            add_rule(world.get_location("Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 3", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Greenflower (Act 2) Waterfall Platforms 1", player))

            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) Ledge Above First Poison", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))

            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) Floating Platform 1", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Techno Hill (Act 1) On Pipes", player))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) Metal Platform After Poison Lake", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Techno Hill (Act 1) On Pipes", player))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) Right of Second Poison", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Techno Hill (Act 1) On Pipes", player))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) On Pipes Near Token", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Techno Hill (Act 1) On Pipes", player))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 1) Floating Platform 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Techno Hill (Act 1) On Pipes", player))

            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 2) Glass Conveyor Secret 1", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 2) Flowing Poison", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))

            add_rule(world.get_location("Final Demo Monitor - Techno Hill (Act 2) Glass Conveyor Secret 2", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Techno Hill (Act 2) Glass Conveyor Secret 1", player))


            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Left Water Secret", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Spring Cave", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 600))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Right Alcove Near Start", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 425))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Left Path Spring Cave", player),
                     lambda state: (state.has("Red Springs", player) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250))) or
                                   char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 600))


            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Moat Sewer 1", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Castle Eggman (Act 1) Left Water Secret", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Moat Sewer 2", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Castle Eggman (Act 1) Moat Sewer 1", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Left Tunnel Before Act Clear", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Right Tunnel Before Act Clear", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Tunnel Near Token", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 1", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 3", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 1) Red Button Trap 4", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 1) Tunnel Before Act Clear", player))

            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Secret Corner in Fountain", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 3", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Secret in Fountain 4", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Sewer Secret 1", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Sewer Secret 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Sewer Room On Pipe", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Sewer Room Switch Corner 1", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Sewer Room Switch Corner 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Sewer Room Switch Corner 3", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Overhang", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Pillar 1", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Pillar 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Pillar 3", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Platform 2", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))
            add_rule(world.get_location("Final Demo Monitor - Castle Eggman (Act 2) Right Courtyard Platform 3", player),
                     lambda state: state.can_reach_location("Final Demo Emerald Token - Castle Eggman (Act 2) Water Flow in Sewers", player))

            if options.difficulty == 0:
                add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 2", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))

            else:
                add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 2", player),
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ["instant_speed"], -1) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ["badnik_bounce"], -1))) or
                              char_needs_tags(state, ["climbs_walls"], -1) or
                              char_needs_tags(state, ["wall_jump"], -1) or
                              char_needs_tags(state, [], 200))

            add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Main Path After Checkpoint", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 2", player))
            add_rule(world.get_location("Final Demo Monitor - Red Volcano (Act 1) Main Path Under Pipes", player),
                     lambda state: state.can_reach_location("Final Demo Monitor - Red Volcano (Act 1) Across Broken Bridge 2", player))

        # haunted heights
        add_rule(world.get_location("Haunted Heights Clear", player),
                 lambda state:  (state.has("Buoyant Slime", player)) and#FUCK THIS
                                (
                                 char_needs_tags(state, ['fits_under_gaps', "wall_jump"], 100) or
                                 char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls"],-1) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 300) and state.has("Red Springs", player)) or
                                 char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 1000) or
                                 (char_needs_tags(state, ['strong_floors','breaks_spikes'], -1) and (state.has("Yellow Springs", player) or char_needs_tags(state,['strong_floors','breaks_spikes'],300))and state.has("Red Springs", player))
                                 ) or
                                (char_needs_tags(state,['fits_under_gaps'],100) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                (char_needs_tags(state, ['fits_under_gaps', "wall_jump"], 100) and state.has("Red Springs", player)) or
                                 char_needs_tags(state,['fits_under_gaps','climbs_walls'],100) or

                                (char_needs_tags(state, ['strong_floors'], 200)and state.has("Red Springs", player)) or
                                  char_needs_tags(state, ['strong_floors'], 600))
#300 Y 600 RED
#spin path (100jh,fug,rs,ys,bs
#knuxpath cw,ys(300jh),bs
        #amy Bspike rs600,ys300, sf
        #fang 200jh (rs to leave)



#alt ys(200jh) slime and zoom tube
        add_rule(world.get_location("Haunted Heights Star Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) and char_needs_tags(state, ['strong_floors'], 200)) or
                 char_needs_tags(state, ["climbs_walls",'strong_floors'], -1) or
                 char_needs_tags(state, ['strong_floors'], 250))

        add_rule(world.get_location("Haunted Heights Spade Emblem", player),
                 lambda state:  (state.has("Buoyant Slime", player)) and
                                (
                                 char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls"],-1) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 300) and state.has("Red Springs", player)) or
                                 char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 1000) or
                                 (char_needs_tags(state, ['strong_floors','breaks_spikes'], 200) and (state.has("Yellow Springs", player) or char_needs_tags(state,['strong_floors','breaks_spikes'],300))and state.has("Red Springs", player))
                                 )or
                                (char_needs_tags(state,['fits_under_gaps'],200) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                char_needs_tags(state, ['fits_under_gaps', 'climbs_walls'], 100) or
                                (char_needs_tags(state, ['strong_floors'], 200)and state.has("Red Springs", player)) or
                                char_needs_tags(state, ['strong_floors'], 600))

        add_rule(world.get_location("Haunted Heights Heart Emblem", player),
                 lambda state: (state.has("Yellow Springs", player) or char_needs_tags(state, [], 250)) and state.has("Buoyant Slime", player) and state.has("Zoom Tubes", player)
                 )
        add_rule(world.get_location("Haunted Heights Diamond Emblem", player),
                 lambda state: state.has("Buoyant Slime", player) and (char_needs_tags(state, ['fits_under_gaps', 'strong_walls', "climbs_walls"], -1) or
                                char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 800))
                 )
        add_rule(world.get_location("Haunted Heights Club Emblem", player),
                lambda state:  state.has("Buoyant Slime", player) and state.has("Red Springs", player) and#FUCK THIS
                ((char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls","can_use_shields"],-1) and state.has("Elemental Shield", player)) or
                                char_needs_tags(state, ['fits_under_gaps', 'strong_walls', "climbs_walls", "can_stomp"], -1) or
                                (char_needs_tags(state, ['fits_under_gaps', 'strong_walls', "can_stomp","can_use_shields"],-1) and state.has("Elemental Shield", player)) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls',"can_stomp"], 300))))
        #heart emblem bullshit as knuckles
        if options.time_emblems:
            add_rule(world.get_location("Haunted Heights Time Emblem", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Haunted Heights Ring Emblem", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))

        if options.oneup_sanity:
            add_rule(world.get_location("Haunted Heights Monitor - First Upper Path Disappearing Ledge", player),
                     lambda state:state.has("Yellow Springs", player) or
                     char_needs_tags(state,[],200) or
                     char_needs_tags(state,['climbs_walls'],-1))

            add_rule(world.get_location("Haunted Heights Monitor - Spin Path Spinning Maces", player),
                     lambda state: (char_needs_tags(state,['fits_under_gaps'],100) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                 char_needs_tags(state,['fits_under_gaps',"wall_jump"],100) or
                                 char_needs_tags(state,['fits_under_gaps','climbs_walls'],100))


            add_rule(world.get_location("Haunted Heights Monitor - Knuckles Path Slime Under Platform", player),
                     lambda state: state.has("Buoyant Slime", player) and (char_needs_tags(state,['fits_under_gaps','strong_walls'],200) or
                                 char_needs_tags(state,['fits_under_gaps','strong_walls','climbs_walls'],-1)))

            add_rule(world.get_location("Haunted Heights Monitor - Third Area High Alcove", player),
                 lambda state:  state.has("Buoyant Slime", player) and#FUCK THIS
                                 (
                                 char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls"],-1) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 300) and state.has("Red Springs", player)) or
                                 char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 1000) or
                                 ((char_needs_tags(state, ['strong_floors','breaks_spikes','instant_speed'], -1) or char_needs_tags(state, ['strong_floors','breaks_spikes','can_hover'], -1)or (char_needs_tags(state, ['strong_floors','breaks_spikes','can_use_shields'], -1) and state.has("Flame Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state,['strong_floors','breaks_spikes'],300))and state.has("Red Springs", player))
                                  )or
                                ((char_needs_tags(state,['fits_under_gaps','instant_speed'],100) or char_needs_tags(state,['fits_under_gaps','can_hover'],100) or (char_needs_tags(state,['fits_under_gaps','can_use_shields'],100) and state.has("Flame Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                 char_needs_tags(state,['fits_under_gaps','climbs_walls'],100) or



                                (char_needs_tags(state, ['strong_floors'], 200)and state.has("Red Springs", player)) or
                                  char_needs_tags(state, ['strong_floors'], 600))

            add_rule(world.get_location("Haunted Heights Monitor - Fang Path Breakable Floor Under Slime", player),
                 lambda state: state.has("Buoyant Slime", player) and (char_needs_tags(state, ['strong_floors'], 200) or
                               char_needs_tags(state, ['strong_floors', 'climbs_walls'], -1)))


            add_rule(world.get_location("Haunted Heights Monitor - Fang Path End Breakable Wall", player),
                 lambda state: char_needs_tags(state, ['strong_floors','strong_walls'], 200) or
                               char_needs_tags(state, ['strong_floors', 'climbs_walls','strong_walls'], -1) or
                               char_needs_tags(state, ['fits_under_gaps', 'strong_walls', "climbs_walls"], -1) or
                               char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 1000))
            add_rule(world.get_location("Haunted Heights Monitor - First Area Highest Pillar", player),#can be done with ww shields and nospin chars
                 lambda state: char_needs_tags(state, [], 400) or
                               char_needs_tags(state, ['climbs_walls'], -1))
            add_rule(world.get_location("Haunted Heights Monitor - First Lower Path Slimefall", player),
                 lambda state:  state.has("Buoyant Slime", player) and
                                 ((state.has("Yellow Springs", player)) or
                               char_needs_tags(state, [], 200) or
                               char_needs_tags(state, ['climbs_walls'], -1)))












            add_rule(world.get_location("Haunted Heights Monitor - Third Area Deep in Slimefall", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
            add_rule(world.get_location("Haunted Heights Monitor - Third Area Conveyor Pillar", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
            add_rule(world.get_location("Haunted Heights Monitor - Near Diamond Emblem", player),
                     lambda state: state.can_reach_location("Haunted Heights Diamond Emblem", player))
            add_rule(world.get_location("Haunted Heights Monitor - Ledge Before Final Checkpoint", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
            add_rule(world.get_location("Haunted Heights Monitor - Platform Before Goal", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
            add_rule(world.get_location("Haunted Heights Monitor - Second Area Left High Ledge", player),
                    lambda state: state.can_reach_location("Haunted Heights Monitor - First Upper Path Disappearing Ledge", player))
            add_rule(world.get_location("Haunted Heights Monitor - First Upper Path Dark Lower Ledge", player),
                    lambda state: state.can_reach_location("Haunted Heights Monitor - First Upper Path Disappearing Ledge", player))




        if options.superring_sanity:


            add_rule(world.get_location("Haunted Heights Monitor - First Slime Pit", player),
                 lambda state:  state.has("Buoyant Slime", player) and
                                 ((state.has("Yellow Springs", player)) or
                               char_needs_tags(state, [], 200) or
                               char_needs_tags(state, ['climbs_walls'], -1)))

            add_rule(world.get_location("Haunted Heights Monitor - Knuckles Path Center Slime Platform", player),
                 lambda state: ((state.has("Yellow Springs", player) and char_needs_tags(state, ['strong_walls','fits_under_gaps'], -1)) or
                               char_needs_tags(state, ['strong_walls','fits_under_gaps'], 200) or
                               char_needs_tags(state, ['climbs_walls','strong_walls','fits_under_gaps'], -1)))

            add_rule(world.get_location("Haunted Heights Monitor - Third Area Bottom Entrances", player),
                 lambda state:  (state.has("Buoyant Slime", player)) and#FUCK THIS
                                (
                                 char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls"],-1) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 300)) or
                                 (char_needs_tags(state, ['strong_floors','breaks_spikes'], -1) and (state.has("Yellow Springs", player) or char_needs_tags(state,['strong_floors','breaks_spikes'],300)))
                                 ) or
                                (char_needs_tags(state,['fits_under_gaps'],100) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                 char_needs_tags(state,['fits_under_gaps',"wall_jump"],100) or
                                 char_needs_tags(state,['fits_under_gaps','climbs_walls'],100) or

                                (char_needs_tags(state, ['strong_floors'], 200)))

            add_rule(world.get_location("Haunted Heights Monitor - First Area Near Top Exit", player),
                     lambda state:state.has("Yellow Springs", player) or
                     char_needs_tags(state,[],200) or
                     char_needs_tags(state,['climbs_walls'],-1))
            add_rule(world.get_location("Haunted Heights Monitor - Second Area Spike Ball Circle", player),
                     lambda state:state.has("Yellow Springs", player) or
                     char_needs_tags(state,[],200) or
                     char_needs_tags(state,['climbs_walls'],-1))
            add_rule(world.get_location("Haunted Heights Monitor - Second Area Grassy Ledge", player),
                     lambda state:state.has("Yellow Springs", player) or
                     char_needs_tags(state,[],200) or
                     char_needs_tags(state,['climbs_walls'],-1))

            add_rule(world.get_location("Haunted Heights Monitor - Third Area Knuckles Path Exit", player),
                 lambda state:  (state.has("Buoyant Slime", player)) and#FUCK THIS
                                (char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls"],-1) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 300)) or
                                 (char_needs_tags(state, ['strong_floors','breaks_spikes'], -1) and ((state.has("Yellow Springs", player)and state.has("Red Springs", player)) or char_needs_tags(state,['strong_floors','breaks_spikes'],300)))
                                 ) or
                                (char_needs_tags(state,['fits_under_gaps'],100) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                 char_needs_tags(state,['fits_under_gaps',"wall_jump"],100) or
                                 char_needs_tags(state,['fits_under_gaps','climbs_walls'],100) or(char_needs_tags(state, ['strong_floors'], 200)))
            add_rule(world.get_location("Haunted Heights Monitor - Before Nospin Path Entrance", player),
                     lambda state:state.has("Yellow Springs", player) or
                     char_needs_tags(state,[],200) or
                     char_needs_tags(state,['climbs_walls'],-1))


            add_rule(world.get_location("Haunted Heights Monitor - Spin Conveyor Path Slime Corner", player),
                 lambda state: ((char_needs_tags(state, ['fits_under_gaps'], 100) and (
                        state.has("Yellow Springs", player) or char_needs_tags(state, ['fits_under_gaps'], 300)) and (
                          state.has("Red Springs", player) or char_needs_tags(state, ['fits_under_gaps'], 600))) or
             char_needs_tags(state, ['fits_under_gaps', "wall_jump"], 100) or
             char_needs_tags(state, ['fits_under_gaps', 'climbs_walls'], 100)))
            add_rule(world.get_location("Haunted Heights Monitor - Nospin Path Behind Spikes", player),
                     lambda state:state.has("Yellow Springs", player) and (char_needs_tags(state, ['strong_floors'], -1)) or
                     char_needs_tags(state,['strong_floors'],200) or
                     char_needs_tags(state,['climbs_walls','strong_floors'],-1))

            add_rule(world.get_location("Haunted Heights Monitor - Fang Path Between Pipes", player),
                     lambda state:state.has("Yellow Springs", player) and (char_needs_tags(state, ['strong_floors','wall_jump'], -1)) or
                     char_needs_tags(state,['strong_floors'],200) or
                     char_needs_tags(state,['climbs_walls','strong_floors'],-1))

            add_rule(world.get_location("Haunted Heights Monitor - Spin Path Behind First Ledge", player),
                 lambda state: state.has("Yellow Springs", player) and (char_needs_tags(state, ['fits_under_gaps'], 100)) or
                     char_needs_tags(state,['fits_under_gaps'],200) or
                     char_needs_tags(state,['climbs_walls','fits_under_gaps'],100))
            add_rule(world.get_location("Haunted Heights Monitor - Amy Path Spikes In Slime", player),
                     lambda state:state.has("Buoyant Slime", player) and (state.has("Yellow Springs", player) and (char_needs_tags(state, ['strong_floors','breaks_spikes'], -1)) or
                     char_needs_tags(state,['strong_floors','breaks_spikes'],200) or
                     char_needs_tags(state,['climbs_walls','strong_floors','breaks_spikes'],-1) or
                     char_needs_tags(state,['strong_floors',"free_flyer"],200)))
            add_rule(world.get_location("Haunted Heights Monitor - First Lower Path Entrance", player),
                     lambda state:(state.has("Yellow Springs", player) and state.has("Buoyant Slime", player)) or
                     char_needs_tags(state,[],200) or
                     char_needs_tags(state,['climbs_walls'],-1))

            add_rule(world.get_location("Haunted Heights Monitor - Third Area Slimefall Lake", player),#biggest logic soup i have yet
                 lambda state:  (state.has("Buoyant Slime", player) and#FUCK THIS
                                ((char_needs_tags(state,['fits_under_gaps'],100) and (state.has("Yellow Springs", player) or char_needs_tags(state,['fits_under_gaps'],300))and (state.has("Red Springs", player) or char_needs_tags(state,['fits_under_gaps'],600))) or
                                 char_needs_tags(state,['fits_under_gaps',"wall_jump"],100) or
                                 char_needs_tags(state,['fits_under_gaps','climbs_walls'],100) or
                                 char_needs_tags(state,['fits_under_gaps','strong_walls',"climbs_walls"],-1) or
                                 (char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 300) and state.has("Red Springs", player)) or
                                 char_needs_tags(state, ['fits_under_gaps', 'strong_walls'], 1000) or
                                 (char_needs_tags(state, ['strong_floors','breaks_spikes'], -1) and (state.has("Yellow Springs", player) or char_needs_tags(state,['strong_floors','breaks_spikes'],300))and state.has("Red Springs", player))
                                  or (char_needs_tags(state, ['strong_floors'], 200)and state.has("Red Springs", player)) or
                                  char_needs_tags(state, ['strong_floors'], 600))) or
                                ((char_needs_tags(state, ['strong_floors','downward_projectile'], 200)and state.has("Red Springs", player)) or
                                  char_needs_tags(state, ['strong_floors','downward_projectile'], 600)))


            add_rule(world.get_location("Haunted Heights Monitor - Third Area Grated Platform 1", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
            add_rule(world.get_location("Haunted Heights Monitor - Third Area Grated Platform 2", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))
            add_rule(world.get_location("Haunted Heights Monitor - Nospin Path Under High Ledge", player),
                    lambda state: state.can_reach_location("Haunted Heights Monitor - Nospin Path Behind Spikes", player))
            add_rule(world.get_location("Haunted Heights Monitor - Third Area Ledge After Conveyors", player),
                     lambda state: state.can_reach_location("Haunted Heights Clear", player))



#2r  yellowspring(250) or rs+gs / lightning+IS 100jh

#3r 250jhys



#knuckles path avoids red springs if you can climb
        add_rule(world.get_location("Aerial Garden Star Emblem", player),
                 lambda state: state.has("Yellow Springs", player) or state.has("Gargoyle Statues", player) or
                               char_needs_tags(state, ["climbs_walls"], -1) or
                               char_needs_tags(state, ["wall_jump"], -1) or
                               (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Lightning Shield", player)) or
                               char_needs_tags(state, [], 115))

        add_rule(world.get_location("Aerial Garden Emerald Token - First Room High Tower", player),
                 lambda state: ((state.has("Yellow Springs", player) or char_needs_tags(state,[],200) or char_needs_tags(state,['wall_jump'],-1) or (char_needs_tags(state,['can_use_shields'],-1) and state.has("Lightning Shield", player))) and state.has("Red Springs", player)) or
                               char_needs_tags(state,[],600) or char_needs_tags(state,["climbs_walls"],-1))

        if options.difficulty == 0:
            add_rule(world.get_location("Aerial Garden Clear", player),#laziness
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                        char_needs_tags(state, [], 800) or
                       char_needs_tags(state, ["climbs_walls"], 100))

            add_rule(world.get_location("Aerial Garden Spade Emblem", player),
                 lambda state: ((char_needs_tags(state, ['strong_floors'], 200)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['strong_floors'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, ['strong_floors'], 500) or char_needs_tags(state, ['climbs_walls','strong_floors'], -1))

            add_rule(world.get_location("Aerial Garden Heart Emblem", player),
                 lambda state: ((char_needs_tags(state, [], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 700) or char_needs_tags(state, ['climbs_walls'], -1))

            add_rule(world.get_location("Aerial Garden Diamond Emblem", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], 100))

        else:
            add_rule(world.get_location("Aerial Garden Clear", player),#laziness
                lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                              (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                              (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player) and char_needs_tags(state, ['can_hover'], -1)))) or
                              char_needs_tags(state, [], 400) or
                              char_needs_tags(state, ["climbs_walls"], -1))

            add_rule(world.get_location("Aerial Garden Spade Emblem", player),
                 lambda state: ((char_needs_tags(state, ['strong_floors','can_use_shields'], 200) and state.has("Lightning Shield", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['strong_floors'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, ['strong_floors'], 500) or char_needs_tags(state, ['climbs_walls','strong_floors'], -1))

            add_rule(world.get_location("Aerial Garden Heart Emblem", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 700) or char_needs_tags(state, ['climbs_walls'], -1))

            add_rule(world.get_location("Aerial Garden Diamond Emblem", player),
                 lambda state: ((char_needs_tags(state, [], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 300)) and state.has("Red Springs", player)
                                ) or (((char_needs_tags(state, ["can_use_shields",'instant_speed'], -1) and state.has("Lightning Shield", player)) or char_needs_tags(state, ['can_hover'], -1)) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))



        add_rule(world.get_location("Aerial Garden Club Emblem", player),#laziness
                 lambda state: state.can_reach_location("Aerial Garden Clear",player))

        add_rule(world.get_location("Aerial Garden Emerald Token - Diamond Emblem 1", player),#laziness
                 lambda state: state.can_reach_location("Aerial Garden Diamond Emblem",player))
        add_rule(world.get_location("Aerial Garden Emerald Token - Diamond Emblem 2", player),#laziness
                 lambda state: state.can_reach_location("Aerial Garden Diamond Emblem",player))
        add_rule(world.get_location("Aerial Garden Emerald Token - Diamond Emblem 3", player),#laziness
                 lambda state: state.can_reach_location("Aerial Garden Diamond Emblem",player))
        add_rule(world.get_location("Aerial Garden Emerald Token - Diamond Emblem 4", player),#laziness
                 lambda state: state.can_reach_location("Aerial Garden Diamond Emblem",player))
        add_rule(world.get_location("Aerial Garden Emerald Token - Underwater on Pillar", player),#laziness
                 lambda state: state.can_reach_location("Aerial Garden Clear",player))

        if options.time_emblems:
            add_rule(world.get_location("Aerial Garden Time Emblem", player),
                     lambda state: state.can_reach_location("Aerial Garden Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Aerial Garden Ring Emblem", player),
                     lambda state: state.can_reach_location("Aerial Garden Clear", player) and state.has("Lightning Shield", player))


        if options.oneup_sanity:



            add_rule(world.get_location("Aerial Garden Monitor - First Area Small Far Platform", player),
                 lambda state: ((state.has("Yellow Springs", player) or char_needs_tags(state,[],200) or char_needs_tags(state,['wall_jump'],-1) or (char_needs_tags(state,['can_use_shields'],-1) and state.has("Lightning Shield", player))) and state.has("Red Springs", player)) or
                               char_needs_tags(state,[],600) or char_needs_tags(state,["climbs_walls"],-1))



            if options.difficulty == 0:
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 1", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Right 3 Behind Statues", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Spin Under Seaweed", player),
                 lambda state: (char_needs_tags(state, ['can_hover','fits_under_gaps'], -1) and (char_needs_tags(state, ['can_hover','fits_under_gaps'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover','fits_under_gaps'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover','fits_under_gaps'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls','fits_under_gaps'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Right 1 Across Moving Platforms", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 6 Waterfall Top 1", player),
                 lambda state: (state.has("Red Springs", player) and ((char_needs_tags(state, ['fits_under_gaps'], -1)) and(char_needs_tags(state, ['fits_under_gaps'], 115) or state.has("Gargoyle Statues", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['fits_under_gaps'], 300)))) or
                        (state.has("Red Springs", player) and ((char_needs_tags(state, ['wall_jump'], -1)) and(char_needs_tags(state, ['wall_jump'], 115) or state.has("Gargoyle Statues", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['wall_jump'], 300)))) or
                        (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed','wall_jump'], -1) or char_needs_tags(state, ['can_use_shields','wall_jump'], 115))and state.has("Lightning Shield", player) )or
                        (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover','wall_jump'], -1) and (char_needs_tags(state, ['can_hover','wall_jump'], 115) or (state.has("Gargoyle Statues", player)))) or
                       char_needs_tags(state, [], 800) or
                       char_needs_tags(state, ["climbs_walls"], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Rafters 1", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Second Area Ledge Behind Fountain", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Right 2 Tiny Platform", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], 200)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Underwater Path Spring Pillars", player),
                 lambda state: ((char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) and state.has("Yellow Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))


            else:
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 1", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Path Right 3 Behind Statues", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1))and state.has("Lightning Shield", player) )or
                                                (char_needs_tags(state, ['can_use_shields'], 115) and state.has("Lightning Shield", player))or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Spin Under Seaweed", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ['fits_under_gaps'], 115) or (state.has("Gargoyle Statues", player) and char_needs_tags(state, ['fits_under_gaps'], -1))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields', 'fits_under_gaps','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields', 'fits_under_gaps'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['fits_under_gaps','can_hover'], -1) and (char_needs_tags(state, ['fits_under_gaps','can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, ['fits_under_gaps'], 400) or
                                                char_needs_tags(state, ["climbs_walls", 'fits_under_gaps'], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Path Left 6 Waterfall Top 1", player),
                 lambda state: (state.has("Red Springs", player) and (char_needs_tags(state, ['fits_under_gaps'], -1) and(char_needs_tags(state, ['fits_under_gaps'], 115) or state.has("Gargoyle Statues", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['fits_under_gaps'], 300)))) or
                       char_needs_tags(state, [], 800) or
                       char_needs_tags(state, ["climbs_walls"], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Path Right 5 Vertical Moving Platforms", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Path Left 2 Spin Into Bushes", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, ['fits_under_gaps'], 115) or (state.has("Gargoyle Statues", player) and char_needs_tags(state, ['fits_under_gaps'], -1))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields', 'fits_under_gaps','instant_speed'], -1))and state.has("Lightning Shield", player) )or
                                                (char_needs_tags(state, ['can_use_shields', 'fits_under_gaps'], 115) and state.has("Lightning Shield", player))or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['fits_under_gaps','can_hover'], -1) and (char_needs_tags(state, ['fits_under_gaps','can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, ['fits_under_gaps'], 400) or
                                                char_needs_tags(state, ["climbs_walls", 'fits_under_gaps'], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Rafters 1", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Right 2 Tiny Platform", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 200))) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                char_needs_tags(state, [], 300) or
                                                char_needs_tags(state, ["climbs_walls"], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Underwater Path Spring Pillars", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 500) or
                                                char_needs_tags(state, ["climbs_walls"], -1))






            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Room Ledge 1", player),
                     lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 2 on Fountain", player),
                     lambda state: state.can_reach_location("Aerial Garden Monitor - Path Right 3 Behind Statues", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 4 Top Cave Clearing", player),
                     lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 1", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 1", player),
                     lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 2", player),
                     lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 3", player),
                     lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 4", player),
                     lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 4 High Thin Platforms", player),
                     lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 4 Top Cave Clearing", player))
            add_rule(world.get_location("Aerial Garden Monitor - Line Hallway Outside R", player),
                     lambda state: state.can_reach_location("Aerial Garden Monitor - Path Right 5 Vertical Moving Platforms", player))
            add_rule(world.get_location("Aerial Garden Monitor - Line Hallway Outside L", player),
                     lambda state: state.can_reach_location("Aerial Garden Monitor - Path Right 5 Vertical Moving Platforms", player))
            add_rule(world.get_location("Aerial Garden Monitor - First Room Near Emerald Token", player),
                     lambda state: state.can_reach_location("Aerial Garden Emerald Token - First Room High Tower", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Star Emblem 1", player),
                     lambda state: state.can_reach_location("Aerial Garden Star Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Star Emblem 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Star Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Room Ledge 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Fountain Room High Left Platform", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Line Hallway Outside R", player))
            add_rule(world.get_location("Aerial Garden Monitor - Falling End Platform Trap", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Top S 1", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Split Path Room Middle Ledge", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Underwater Path Behind Corner", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))


        if options.superring_sanity:
            if options.difficulty == 0:
                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway End 1", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 2", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Right 1 Grass Platform", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 6 Waterfall Top 2", player),
                 lambda state: (char_needs_tags(state, ['fits_under_gaps','can_hover'], -1) and (char_needs_tags(state, ['fits_under_gaps','can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'fits_under_gaps','can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['fits_under_gaps','can_hover'], 300)) and state.has("Red Springs", player)
                                ) or (char_needs_tags(state, ['wall_jump','can_hover'], -1) and (char_needs_tags(state, ['wall_jump','can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'wall_jump','can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['wall_jump','can_hover'], 300)) and state.has("Red Springs", player)
                                ) or char_needs_tags(state, [], 800) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 3 Left Block Ledge", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 3 Block On Grass", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Knuckles Path Tall Room On Pillar", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], 300)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Rafters 2", player),
                 lambda state: (char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or state.has("Gargoyle Statues", player) or (char_needs_tags(state, ["can_use_shields",'can_hover'], -1) and state.has("Lightning Shield", player))) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['can_hover'], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))


            else:
                add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway End 1", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 2", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 6 Waterfall Top 2", player),
                 lambda state: (state.has("Red Springs", player) and ((char_needs_tags(state, ['fits_under_gaps'], -1)) and(char_needs_tags(state, ['fits_under_gaps'], 115) or state.has("Gargoyle Statues", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['fits_under_gaps'], 300)))) or
                        (state.has("Red Springs", player) and ((char_needs_tags(state, ['wall_jump'], -1)) and(char_needs_tags(state, ['wall_jump'], 115) or state.has("Gargoyle Statues", player)) and (state.has("Yellow Springs", player) or char_needs_tags(state, ['wall_jump'], 300)))) or
                        (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed','wall_jump'], -1) or char_needs_tags(state, ['can_use_shields','wall_jump'], 115))and state.has("Lightning Shield", player) )or
                        (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover','wall_jump'], -1) and (char_needs_tags(state, ['can_hover','wall_jump'], 115) or (state.has("Gargoyle Statues", player)))) or
                       char_needs_tags(state, [], 800) or
                       char_needs_tags(state, ["climbs_walls"], -1))

                add_rule(world.get_location("Aerial Garden Monitor - Path Left 3 Left Block Ledge", player),
                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                char_needs_tags(state, [], 400) or
                                char_needs_tags(state, ["climbs_walls"], -1))
                add_rule(world.get_location("Aerial Garden Monitor - Path Left 3 Block On Grass", player),
                                  lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                                (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1))and state.has("Lightning Shield", player) )or
                                                (char_needs_tags(state, ['can_use_shields'], 115) and state.has("Lightning Shield", player))or
                                                (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                                char_needs_tags(state, [], 400) or
                                                char_needs_tags(state, ["climbs_walls"], -1))
            add_rule(world.get_location("Aerial Garden Monitor - Knuckles Path Tall Room On Pillar", player),
                 lambda state: ((char_needs_tags(state, [], 200)) and (state.has("Yellow Springs", player) or char_needs_tags(state, [], 300)) and state.has("Red Springs", player)) or
                               char_needs_tags(state, [], 500) or char_needs_tags(state, ['climbs_walls'], -1))
            add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Rafters 2", player),
                    lambda state: (state.has("Yellow Springs", player) and (char_needs_tags(state, [], 115) or (state.has("Gargoyle Statues", player))) and state.has("Red Springs", player)) or
                                  (state.has("Yellow Springs", player) and (char_needs_tags(state, ['can_use_shields','instant_speed'], -1) or char_needs_tags(state, ['can_use_shields'], 115))and state.has("Lightning Shield", player) )or
                                  (state.has("Yellow Springs", player) and char_needs_tags(state, ['can_hover'], -1) and (char_needs_tags(state, ['can_hover'], 115) or (state.has("Gargoyle Statues", player)))) or
                                  char_needs_tags(state, [], 400) or
                                  char_needs_tags(state, ["climbs_walls"], -1))



            add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway End 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Triangle Hallway End 1", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 3", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 2", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 5", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 6", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 7", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 8", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 9", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 10", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 11", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 12", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 13", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 14", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Block After First Conveyor", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 3 Block On Grass", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 15", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Underwater Path Below Token", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 4 Before Triangle Switch", player),
                lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 5 Thin Platforms Top 2", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 3 High Ledge 1", player),
                lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 3 Left Block Ledge", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 3 High Ledge 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 3 Left Block Ledge", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Right 3 High Ledge 1", player),
                lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 3 Left Block Ledge", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Right 3 High Ledge 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 3 Left Block Ledge", player))
            add_rule(world.get_location("Aerial Garden Monitor - Triangle Hallway Rafters 3", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Triangle Hallway Rafters 2", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 6 Waterfall Top 3", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 6 Waterfall Top 2", player))
            add_rule(world.get_location("Aerial Garden Monitor - Right Hallway Before Goal", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Outside Star Gate 1", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Top W", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Top E", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Final Elevator Top W", player))
            add_rule(world.get_location("Aerial Garden Monitor - Split Path Room Left Pillars", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Split Path Room Right Ledge", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Outside Star Gate 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Bottom 1", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Bottom 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Top S 2", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Final Elevator Top S 3", player),
                 lambda state: state.can_reach_location("Aerial Garden Clear", player))
            add_rule(world.get_location("Aerial Garden Monitor - Near Heart Emblem 16", player),
                 lambda state: state.can_reach_location("Aerial Garden Heart Emblem", player))
            add_rule(world.get_location("Aerial Garden Monitor - Path Left 2 Near Fountain", player),
                 lambda state: state.can_reach_location("Aerial Garden Monitor - Path Left 3 Block On Grass", player))


        if options.difficulty == 0:

            add_rule(world.get_location("Azure Temple Clear", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))

            add_rule(world.get_location("Azure Temple Star Emblem", player),
                     lambda state: (state.has("Air Bubbles", player) or state.has("Bubble Shield", player)) and (
                             char_needs_tags(state, ["free_flyer"], 1400) or
                             char_needs_tags(state, ["climbs_walls"], 100) or
                             (char_needs_tags(state, ["climbs_walls", "can_use_shields"], -1) and state.has(
                                 "Bubble Shield", player))
                     ))
            add_rule(world.get_location("Azure Temple Spade Emblem", player),
                     lambda state: (state.has("Air Bubbles", player)) and (
                         char_needs_tags(state, ["free_flyer"], 1400)))
            add_rule(world.get_location("Azure Temple Heart Emblem", player),  # no air needed
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or char_needs_tags(state, ["free_flyer",'fits_under_gaps'], 500) or char_needs_tags(state, ["can_hover",'fits_under_gaps'], -1)))

            add_rule(world.get_location("Azure Temple Diamond Emblem", player),  # no air needed
                     lambda state: state.has("Air Bubbles", player) and (
                             char_needs_tags(state, ['fits_under_gaps'], -1) or (
                                 char_needs_tags(state, ['strong_floors'], -1) and state.has("Yellow Springs",player)) or char_needs_tags(state, ['strong_floors'], 400)))

            add_rule(world.get_location("Azure Temple Club Emblem", player),
                     lambda state: state.has("Air Bubbles", player) and state.count("Chaos Emerald",player)>6 and
                         char_needs_tags(state, ["can_use_shields"], -1) and state.has("Armageddon Shield", player))


            # easy version
        else:
            add_rule(world.get_location("Azure Temple Clear", player),
                     lambda state: (state.has("Air Bubbles", player)))

            add_rule(world.get_location("Azure Temple Star Emblem", player),
                     lambda state: (state.has("Air Bubbles", player) or state.has("Bubble Shield", player)) and (
                             char_needs_tags(state, ["free_flyer"], 1400) or
                             char_needs_tags(state, ["climbs_walls"], 100) or
                             (char_needs_tags(state, ["climbs_walls", "can_use_shields"], -1) and state.has(
                                 "Bubble Shield", player))
                     ))
            add_rule(world.get_location("Azure Temple Spade Emblem", player),
                     lambda state: (state.has("Air Bubbles", player) or state.has("Bubble Shield", player)) and (
                         char_needs_tags(state, [], 400)))
            add_rule(world.get_location("Azure Temple Heart Emblem", player),  # no air needed
                     lambda state:  (
                         char_needs_tags(state, ['fits_under_gaps'], -1)))

            add_rule(world.get_location("Azure Temple Diamond Emblem", player),
                     lambda state: (state.has("Air Bubbles", player) or state.has("Bubble Shield", player)) and (
                             char_needs_tags(state, ['fits_under_gaps'], -1) or (
                                 char_needs_tags(state, ['strong_floors'], -1) and state.has("Yellow Springs",player)) or char_needs_tags(state, ['strong_floors'], 400)))
            add_rule(world.get_location("Azure Temple Club Emblem", player),  # no air needed
                     lambda state: state.has("Air Bubbles", player) and (
                         char_needs_tags(state, ["can_use_shields"], -1)) and state.has("Armageddon Shield", player))

        if options.time_emblems:
            add_rule(world.get_location("Azure Temple Time Emblem", player),
                     lambda state: state.can_reach_location("Azure Temple Clear", player))
        if options.ring_emblems:
            add_rule(world.get_location("Azure Temple Ring Emblem", player),
                     lambda state: state.can_reach_location("Azure Temple Clear", player))

        if options.oneup_sanity:

            add_rule(world.get_location("Azure Temple Monitor - Action Nospin Path Ledge After Spring", player),
                lambda state:state.has("Air Bubbles", player) and (char_needs_tags(state, ["climbs_walls",'strong_floors'], -1) or
                                                            char_needs_tags(state, ["wall_jump",'strong_floors'], -1) or char_needs_tags(state, ['strong_floors'], 200) or
                                                            (char_needs_tags(state, ['strong_floors','can_use_shields'], -1)and (state.has("Whirlwind Shield", player) or state.has("Bubble Shield", player)))))


            if options.difficulty == 0:
                add_rule(world.get_location("Azure Temple Monitor - Main Path Behind Statues", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Bottom Path Side of Statue Hallway", player),
                     lambda state: state.has("Air Bubbles", player) and (char_needs_tags(state, ["climbs_walls"], 100)or (char_needs_tags(state, ["climbs_walls","can_use_shields"], -1) and state.has("Bubble Shield", player))or
                            char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], 100)or(char_needs_tags(state, ["can_hover","can_use_shields"], -1) and state.has("Bubble Shield", player))))
                add_rule(world.get_location("Azure Temple Monitor - Rafters Near Spade Emblem 1", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], 400)))
                add_rule(world.get_location("Azure Temple Monitor - Top Path High Ledge Behind Bars", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], 200)))


                add_rule(world.get_location("Azure Temple Monitor - Top Path Near Spiked Platform Ledge 1", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Bottom Path Buggle Room Rafters", player),
                     lambda state: state.has("Air Bubbles", player) and (char_needs_tags(state, ["climbs_walls"], 100)or (char_needs_tags(state, ["climbs_walls","can_use_shields"], -1) and state.has("Bubble Shield", player))or
                            char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], 100)or(char_needs_tags(state, ["can_hover","can_use_shields"], -1) and state.has("Bubble Shield", player))))
                add_rule(world.get_location("Azure Temple Monitor - Action Path Rafters 1", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls",'strong_floors'], -1) or char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                                char_needs_tags(state, ["free_flyer",'strong_floors'], 500) or char_needs_tags(state, ["free_flyer",'fits_under_gaps'], 500) or
                                char_needs_tags(state, ["can_hover",'fits_under_gaps'], -1) or char_needs_tags(state, ["can_hover",'strong_floors'], 200) or (char_needs_tags(state, ["can_hover",'strong_floors'], -1) and state.has("Yellow Springs", player))))



            else:
                add_rule(world.get_location("Azure Temple Monitor - Bottom Path Side of Statue Hallway", player),
                     lambda state: (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Bubble Shield", player)) or char_needs_tags(state, [], 100))
                add_rule(world.get_location("Azure Temple Monitor - Rafters Near Spade Emblem 1", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)))
                add_rule(world.get_location("Azure Temple Monitor - Top Path High Ledge Behind Bars", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 200) or (char_needs_tags(state, ['can_use_shields'], 115) and state.has("Bubble Shield", player))))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Near Spiked Platform Ledge 1", player),
                     lambda state: state.has("Air Bubbles", player))
                add_rule(world.get_location("Azure Temple Monitor - Bottom Path Buggle Room Rafters", player),
                     lambda state: (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Bubble Shield", player)) or char_needs_tags(state, [], 100))
                add_rule(world.get_location("Azure Temple Monitor - Action Path Rafters 1", player),
                     lambda state:state.has("Air Bubbles", player) and (char_needs_tags(state, ['fits_under_gaps'], -1) or char_needs_tags(state, ["climbs_walls",'strong_floors'], -1) or
                                                                        char_needs_tags(state, ["wall_jump",'strong_floors'], -1) or char_needs_tags(state, ['strong_floors'], 200) or
                                                                        (char_needs_tags(state, ['strong_floors'], -1)and state.has("Yellow Springs", player))))



            add_rule(world.get_location("Azure Temple Monitor - Main Path High Rocky Ledge", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Main Path Behind Statues", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Star Emblem", player),
                    lambda state: state.can_reach_location("Azure Temple Star Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Puzzle Path Corner 1", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Club Emblem 1", player),
                    lambda state: state.can_reach_location("Azure Temple Club Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Club Emblem 2", player),
                    lambda state: state.can_reach_location("Azure Temple Club Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Club Emblem 3", player),
                    lambda state: state.can_reach_location("Azure Temple Club Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Inside Fountain Near End", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Heart Emblem 1", player),
                    lambda state: state.can_reach_location("Azure Temple Heart Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Gap Between Pillars Near First Checkpoint", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Main Path Behind Statues", player))
            add_rule(world.get_location("Azure Temple Monitor - End of Puzzle Path", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))

        if options.superring_sanity:


            add_rule(world.get_location("Azure Temple Monitor - Knuckles Path First Rocky Ledge", player),
                     lambda state: state.has("Air Bubbles", player) and (char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or char_needs_tags(state, ['strong_walls'], 1500)))
            add_rule(world.get_location("Azure Temple Monitor - Knuckles Path Second Rocky Ledge", player),
                     lambda state: state.has("Air Bubbles", player) and (char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or char_needs_tags(state, ['strong_walls','free_flyer'], 1500)))
            add_rule(world.get_location("Azure Temple Monitor - Action Nospin Path Pillar", player),
                     lambda state: state.has("Air Bubbles", player) and (char_needs_tags(state, ['strong_floors'], -1)))


            if options.difficulty == 0:
                add_rule(world.get_location("Azure Temple Monitor - Right Path Behind Corner", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - After First Checkpoint", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Knuckles Path Start", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls","strong_walls"], -1) or char_needs_tags(state, ["free_flyer","strong_walls"], 500) or char_needs_tags(state, ["can_hover","strong_walls"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Gap After First Statue Hallway 1", player),
                     lambda state: (state.has("Air Bubbles", player)) and(char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or char_needs_tags(state, ["free_flyer",'fits_under_gaps'], 500) or char_needs_tags(state, ["can_hover",'fits_under_gaps'], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Bubbles Before Checkpoint", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player),
                     lambda state: state.has("Air Bubbles", player) and (char_needs_tags(state, ["climbs_walls"], 100)or (char_needs_tags(state, ["climbs_walls","can_use_shields"], -1) and state.has("Bubble Shield", player))or
                            char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], 100)or(char_needs_tags(state, ["can_hover","can_use_shields"], -1) and state.has("Bubble Shield", player))))
                add_rule(world.get_location("Azure Temple Monitor - Rafters Near Spade Emblem 2", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], 400)))
                add_rule(world.get_location("Azure Temple Monitor - Knuckles Path Before Second Climb", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or char_needs_tags(state, ['strong_walls'], 1400) ))

                add_rule(world.get_location("Azure Temple Monitor - Knuckles Path End", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) ))
                add_rule(world.get_location("Azure Temple Monitor - Spade Emblem Room Knuckles Path Drop", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Behind Metal Bars", player),
                     lambda state: (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Near Spiked Platform Ledge 2", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, ["free_flyer"], 500) or char_needs_tags(state, ["can_hover"], -1)))
                add_rule(world.get_location("Azure Temple Monitor - Action Path Final Room First Ledge", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls",'strong_floors'], -1) or char_needs_tags(state, ["climbs_walls",'fits_under_gaps'], -1) or
                                char_needs_tags(state, ["free_flyer",'strong_floors'], 500) or char_needs_tags(state, ["free_flyer",'fits_under_gaps'], 500) or
                                char_needs_tags(state, ["can_hover",'fits_under_gaps'], -1) or char_needs_tags(state, ["can_hover",'strong_floors'], 200) or (char_needs_tags(state, ["can_hover",'strong_floors'], -1) and state.has("Yellow Springs", player))))





            else:
                add_rule(world.get_location("Azure Temple Monitor - Knuckles Path Start", player),
                     lambda state: char_needs_tags(state, ["strong_walls"], -1))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Gap After First Statue Hallway 1", player),
                     lambda state:char_needs_tags(state, ['fits_under_gaps'], -1))
                add_rule(world.get_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player),
                     lambda state: (char_needs_tags(state, ["can_use_shields"], -1) and state.has("Bubble Shield", player)) or char_needs_tags(state, [], 100))
                add_rule(world.get_location("Azure Temple Monitor - Rafters Near Spade Emblem 2", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ["climbs_walls"], -1) or char_needs_tags(state, [], 400)))
                add_rule(world.get_location("Azure Temple Monitor - Knuckles Path Before Second Climb", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or char_needs_tags(state, ['strong_walls'], 200) or (char_needs_tags(state, ['strong_walls','can_use_shields'], 115) and state.has("Bubble Shield", player)) ))
                add_rule(world.get_location("Azure Temple Monitor - Knuckles Path End", player),
                     lambda state: (state.has("Air Bubbles", player)) and (char_needs_tags(state, ['strong_walls',"climbs_walls"], -1) or char_needs_tags(state, [], 400) or (char_needs_tags(state, ['can_use_shields'], -1) and state.has("Bubble Shield", player)) ))
                add_rule(world.get_location("Azure Temple Monitor - Spade Emblem Room Knuckles Path Drop", player),
                     lambda state: state.has("Air Bubbles", player))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Behind Metal Bars", player),
                     lambda state: state.has("Air Bubbles", player))
                add_rule(world.get_location("Azure Temple Monitor - Top Path Near Spiked Platform Ledge 2", player),
                     lambda state: state.has("Air Bubbles", player))
                add_rule(world.get_location("Azure Temple Monitor - Action Path Final Room First Ledge", player),
                     lambda state:state.has("Air Bubbles", player) and (char_needs_tags(state, ['fits_under_gaps'], -1) or char_needs_tags(state, ["climbs_walls",'strong_floors'], -1) or
                                                                        char_needs_tags(state, ["wall_jump",'strong_floors'], -1) or char_needs_tags(state, ['strong_floors'], 200) or
                                                                        (char_needs_tags(state, ['strong_floors'], -1)and state.has("Yellow Springs", player))))

            add_rule(world.get_location("Azure Temple Monitor - Upper Main Path Behind Corner", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - After First Checkpoint", player))
            add_rule(world.get_location("Azure Temple Monitor - First Checkpoint Behind Stairs", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - After First Checkpoint", player))
            add_rule(world.get_location("Azure Temple Monitor - First Checkpoint Behind Stairs", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - After First Checkpoint", player))
            add_rule(world.get_location("Azure Temple Monitor - Top Path Gap After First Statue Hallway 2", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Top Path Gap After First Statue Hallway 1", player))
            add_rule(world.get_location("Azure Temple Monitor - Bottom Path Metal Bars", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player))
            add_rule(world.get_location("Azure Temple Monitor - Rafters Near Spade Emblem 3", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Rafters Near Spade Emblem 2", player))
            add_rule(world.get_location("Azure Temple Monitor - Top Path Corner After Checkpoint", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Top Path Bubbles Before Checkpoint", player))
            add_rule(world.get_location("Azure Temple Monitor - Top Path Near Spiked Platform Ledge 3", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Top Path Near Spiked Platform Ledge 2", player))
            add_rule(world.get_location("Azure Temple Monitor - Bottom Path Buggle Room Corner", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player))
            add_rule(world.get_location("Azure Temple Monitor - Puzzle Path First Room", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Bottom Path First Hallway Wall Gap 1", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player))
            add_rule(world.get_location("Azure Temple Monitor - Bottom Path First Hallway Wall Gap 2", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player))
            add_rule(world.get_location("Azure Temple Monitor - Puzzle Path Corner 2", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Puzzle Path Corner 3", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Action Path First Room Ledge", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Heart Emblem 2", player),
                    lambda state: state.can_reach_location("Azure Temple Heart Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Heart Emblem 3", player),
                    lambda state: state.can_reach_location("Azure Temple Heart Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Diamond Emblem 1", player),
                    lambda state: state.can_reach_location("Azure Temple Diamond Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Near Diamond Emblem 2", player),
                    lambda state: state.can_reach_location("Azure Temple Diamond Emblem", player))
            add_rule(world.get_location("Azure Temple Monitor - Bottom Path Buggle Room Behind Statues", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Bottom Path First Statue Hallway", player))
            add_rule(world.get_location("Azure Temple Monitor - Puzzle Path Final Room", player),
                    lambda state: state.can_reach_location("Azure Temple Clear", player))
            add_rule(world.get_location("Azure Temple Monitor - Action Path Rafters 2", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Action Path Final Room First Ledge", player))
            add_rule(world.get_location("Azure Temple Monitor - Action Path Rafters 3", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Action Path Final Room First Ledge", player))
            add_rule(world.get_location("Azure Temple Monitor - Top Path First Hallway Secret", player),
                    lambda state: state.can_reach_location("Azure Temple Monitor - Top Path Bubbles Before Checkpoint", player))


        if options.oneup_sanity and options.match_maps:
            add_rule(world.get_location("Sapphire Falls Monitor - Inside Central Platform", player),
                     lambda state: state.has("Red Springs", player) or char_needs_tags(state, ["can_hover"], -1) or char_needs_tags(state, ['instant_speed'], -1)or char_needs_tags(state, [], 400) or char_needs_tags(state, ['climbs_walls'], -1) or
                                   (state.has("Whirlwind Shield", player) and char_needs_tags(state, ["can_use_shields"], -1)))
            


        if options.superring_sanity and options.match_maps:
            rf.assign_rule("Noxious Factory Monitor - x:416 y:576", "TAILS | KNUCKLES | FANG")
            rf.assign_rule("Noxious Factory Monitor - x:736 y:768", "TAILS | KNUCKLES | FANG")
            rf.assign_rule("Noxious Factory Monitor - x:2112 y:-1920", "TAILS | KNUCKLES | FANG")
            rf.assign_rule("Noxious Factory Monitor - x:2496 y:3264", "TAILS | KNUCKLES | FANG | WIND")
            rf.assign_rule("Noxious Factory Monitor - x:2496 y:3136", "TAILS | KNUCKLES | FANG | WIND")
            rf.assign_rule("Noxious Factory Monitor - x:1440 y:-2336", "TAILS | KNUCKLES | FANG")

            rf.assign_rule("Tidal Palace Monitor - x:-2624 y:-3072", "TAILS")
            rf.assign_rule("Tidal Palace Monitor - x:-2912 y:-2976", "TAILS")
            rf.assign_rule("Tidal Palace Monitor - x:-2656 y:-2656", "TAILS")
            rf.assign_rule("Tidal Palace Monitor - x:1504 y:-96",  "TAILS | KNUCKLES")
            rf.assign_rule("Tidal Palace Monitor - x:1504 y:-224",  "TAILS | KNUCKLES")
            rf.assign_rule("Tidal Palace Monitor - x:-224 y:-672", "TAILS | KNUCKLES")
            rf.assign_rule("Tidal Palace Monitor - x:224 y:-672", "TAILS | KNUCKLES")

            rf.assign_rule("Desolate Twilight Monitor - x:-128 y:-2688", "TAILS | KNUCKLES")
            rf.assign_rule("Desolate Twilight Monitor - x:2913 y:212", "TAILS | KNUCKLES")
            rf.assign_rule("Desolate Twilight Monitor - x:2904 y:275", "TAILS | KNUCKLES")
            rf.assign_rule("Desolate Twilight Monitor - x:0 y:3584", "TAILS | KNUCKLES")

            rf.assign_rule("Diamond Blizzard Monitor - x:1296 y:400", "SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")
            rf.assign_rule("Diamond Blizzard Monitor - x:1904 y:-1040","SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")
            rf.assign_rule("Diamond Blizzard Monitor - x:608 y:-4544","TAILS | KNUCKLES | AMY+WIND | FANG+WIND")
            rf.assign_rule("Diamond Blizzard Monitor - x:928 y:-4544", "TAILS | KNUCKLES | AMY+WIND | FANG+WIND")

            rf.assign_rule("Frost Columns Monitor - x:0 y:-3520", "TAILS | KNUCKLES | AMY+WIND | FANG+WIND")
            rf.assign_rule("Frost Columns Monitor - x:-64 y:-3520", "TAILS | KNUCKLES | AMY+WIND | FANG+WIND")
            rf.assign_rule("Frost Columns Monitor - x:-1472 y:-96", "TAILS | KNUCKLES | AMY+WIND | FANG")
            rf.assign_rule("Frost Columns Monitor - x:-1472 y:-32", "TAILS | KNUCKLES | AMY+WIND | FANG")
            rf.assign_rule("Frost Columns Monitor - x:-3296 y:3200", "TAILS | KNUCKLES | AMY+WIND | FANG+WIND")
            rf.assign_rule("Frost Columns Monitor - x:-3328 y:3168", "TAILS | KNUCKLES | AMY+WIND | FANG+WIND")
            rf.assign_rule("Frost Columns Monitor - x:2112 y:-1088", "TAILS | AMY+WIND | FANG")
            rf.assign_rule("Frost Columns Monitor - x:2112 y:-1344", "TAILS | AMY+WIND | FANG")
            rf.assign_rule("Frost Columns Monitor - x:832 y:-1376", "SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")

            rf.assign_rule("Summit Showdown Monitor - x:-7456 y:-1696","SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")
            rf.assign_rule("Summit Showdown Monitor - x:-7008 y:-2144","SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")

            rf.assign_rule("Silver Shiver Monitor - x:-96 y:-2768","SONIC+WIND | TAILS | KNUCKLES | METAL SONIC")
            rf.assign_rule("Silver Shiver Monitor - x:32 y:-2768", "SONIC+WIND | TAILS | KNUCKLES | METAL SONIC")
            rf.assign_rule("Silver Shiver Monitor - x:15280 y:-26560", "TAILS | AMY | FANG | WIND")
            rf.assign_rule("Silver Shiver Monitor - x:15696 y:-26560", "TAILS | AMY | FANG | WIND")

            rf.assign_rule("Uncharted Badlands Monitor - x:1920 y:1024", "TAILS | KNUCKLES")

            rf.assign_rule("Pristine Shores Monitor - x:15808 y:12160", "TAILS | KNUCKLES")
            rf.assign_rule("Pristine Shores Monitor - x:14936 y:13448", "SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")
            rf.assign_rule("Pristine Shores Monitor - x:4160 y:7176", "SONIC | TAILS | KNUCKLES | METAL SONIC")
            rf.assign_rule("Pristine Shores Monitor - x:9944 y:7616", "TAILS | KNUCKLES")


            if options.difficulty == 0:
                rf.assign_rule("Summit Showdown Monitor - x:5600 y:2208","SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")
                rf.assign_rule("Summit Showdown Monitor - x:5088 y:1696","SONIC | TAILS | KNUCKLES | FANG | METAL SONIC | WIND")





        if options.nights_maps:
            #special stages
            if options.difficulty == 0:
                rf.assign_rule("Cavern Fortress Sun Emblem", "PARALOOP")
                rf.assign_rule("Flooded Cove Sun Emblem", "PARALOOP")
                rf.assign_rule("Magma Caves Moon Emblem", "PARALOOP")
                rf.assign_rule("Egg Satellite Sun Emblem", "PARALOOP")

            rf.assign_rule("Black Hole Sun Emblem", "PARALOOP")
            if options.ntime_emblems:
                rf.assign_rule("Magma Caves Time Emblem", "PARALOOP")
            if options.rank_emblems:
                rf.assign_rule("Egg Satellite A Rank Emblem", "EXTIME")
                rf.assign_rule("Black Hole A Rank Emblem", "EXTIME")


    if options.completion_type == 0:
        world.completion_condition[player] = lambda state: state.can_reach("Black Core Zone 3", 'Region', player)
    else:
        world.completion_condition[player] = lambda state: state.can_reach("Credits", 'Region', player)



class RuleFactory:

    world: MultiWorld
    player: int
    move_rando_bitvec: bool
    area_randomizer: bool
    capless: bool
    cannonless: bool
    moveless: bool

    token_table = {
        "SONIC": "Sonic",
        "TAILS": "Tails",
        "KNUCKLES": "Knuckles",
        "AMY": "Amy",
        "FANG": "Fang",
        "METAL SONIC": "Metal Sonic",
        # future concepts to implement
        #"SPIN": "Spindash",
        "WIND": "Whirlwind Shield",
        "ELEMENTAL": "Elemental Shield",
        "ARMAGEDDON": "Armageddon Shield",
        "BUBBLE": "Bubble Shield",
        "FLAME": "Flame Shield",
        "FORCE": "Force Shield",
        "LIGHTNING": "Lightning Shield",
        "PARALOOP": "Super Paraloop",
        "EXTIME" : "Extra Time",
        "EM1": "Green Chaos Emerald",
        "EM2": "Pink Chaos Emerald",
        "EM3": "Blue Chaos Emerald",
        "EM4": "Cyan Chaos Emerald",
        "EM5": "Yellow Chaos Emerald",
        "EM6": "Red Chaos Emerald",
        "EM7": "Gray Chaos Emerald"

        #"INVINCIBILITY": "Invincibility Monitors"
        # all other shields arent used in getting emblems directly
        # speed shoes, Attraction, Force, lightning, fire, bubble?
        # bubble might technically allow knuckles to get some emblem

    }

    class SRB2LogicException(Exception):
        pass

    def __init__(self, world, options: SRB2Options, player: int, move_rando_bitvec: int):
        self.world = world
        self.player = player
        #self.move_rando_bitvec = move_rando_bitvec
        #self.area_randomizer = options.area_rando > 0
        #self.capless = not options.strict_cap_requirements
        #self.cannonless = not options.strict_cannon_requirements
        #self.moveless = not options.strict_move_requirements

    def assign_rule(self, target_name: str, rule_expr: str):
        target = self.world.get_location(target_name, self.player) if target_name in location_table else self.world.get_entrance(target_name, self.player)
        cannon_name = "Cannon Unlock " + target_name.split(':')[0]
        try:
            rule = self.build_rule(rule_expr, cannon_name)
        except RuleFactory.SRB2LogicException as exception:
            raise RuleFactory.SRB2LogicException(
                f"Error generating rule for {target_name} using rule expression {rule_expr}: {exception}")
        if rule:
            set_rule(target, rule)

    def build_rule(self, rule_expr: str, cannon_name: str = '') -> Callable:
        expressions = rule_expr.split(" | ")
        rules = []
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression, cannon_name)
            if or_clause is True:
                return None
            if or_clause is not False:
                rules.append(or_clause)
        if rules:
            if len(rules) == 1:
                return rules[0]
            else:
                return lambda state: any(rule(state) for rule in rules)
        else:
            return None

    def combine_and_clauses(self, rule_expr: str, cannon_name: str) -> Union[Callable, bool]:
        expressions = rule_expr.split(" & ")
        rules = []
        for expression in expressions:
            and_clause = self.make_lambda(expression, cannon_name)
            if and_clause is False:
                return False
            if and_clause is not True:
                rules.append(and_clause)
        if rules:
            if len(rules) == 1:
                return rules[0]
            return lambda state: all(rule(state) for rule in rules)
        else:
            return True

    def make_lambda(self, expression: str, cannon_name: str) -> Union[Callable, bool]:
        if '+' in expression:
            tokens = expression.split('+')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name)
                if item is True:
                    continue
                if item is False:
                    return False
                items.add(item)
            if items:
                return lambda state: state.has_all(items, self.player)
            else:
                return True
        if '/' in expression:
            tokens = expression.split('/')
            items = set()
            for token in tokens:
                item = self.parse_token(token, cannon_name)
                if item is True:
                    return True
                if item is False:
                    continue
                items.add(item)
            if items:
                return lambda state: state.has_any(items, self.player)
            else:
                return False
        if '{{' in expression:
            return lambda state: state.can_reach(expression[2:-2], "Location", self.player)
        if '{' in expression:
            return lambda state: state.can_reach(expression[1:-1], "Region", self.player)
        item = self.parse_token(expression, cannon_name)
        if item in (True, False):
            return item
        return lambda state: state.has(item, self.player)

    def parse_token(self, token: str, cannon_name: str) -> Union[str, bool]:
        item = self.token_table.get(token, None)
        if not item:
            raise Exception(f"Invalid token: '{item}'")

        return item


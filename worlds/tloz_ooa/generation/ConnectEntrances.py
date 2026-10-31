from .. import OracleOfAgesWorld

from Options import OptionError
from BaseClasses import EntranceType
from entrance_rando import randomize_entrances, disconnect_entrance_for_randomization
from rule_builder.rules import Has, True_
from ..Options import *
from ..data.Entrances import WARPS_DATA, OUTSIDE_TAG, INSIDE_TAG
from ..data.Constants import OracleOfAgesConnectionType

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_create_entrances(world: OracleOfAgesWorld):

    option_no_ER = world.options.entrance_randomizer == OracleOfAgesEntranceRandomizer.option_disabled
    option_dungeon_only = world.options.entrance_randomizer == OracleOfAgesEntranceRandomizer.option_dungeon_only
    option_dungeon_grouping = world.options.entrance_randomizer_dungeon_pairing
    option_excluded_ER = world.options.entrance_randomizer_excluded_entrances.value

    unknown_entrances = []


    for excluded_entrance in option_excluded_ER:
        if (excluded_entrance not in WARPS_DATA):
            unknown_entrances.append(excluded_entrance)

    if len(unknown_entrances) > 0:
        raise OptionError("Unrecognized excluded entrances", unknown_entrances)

    world.randomized_entrances = {}
    for warpName, warpData in WARPS_DATA.items():

        dont_randomize = False

        if option_no_ER:
            dont_randomize = True
        elif "outside_warp" not in warpData or "inside_warp" not in warpData:
            dont_randomize = True
        elif "require_option" in warpData and (hasattr(world.options, warpData["require_option"]) == False or getattr(world.options, warpData["require_option"]) == False):
            dont_randomize = True
        elif option_dungeon_only and "dungeon" not in warpData:
            dont_randomize = True
        elif warpName in option_excluded_ER:
            dont_randomize = True

        regionOutside = world.get_region(OUTSIDE_TAG + warpName)
        regionInside = world.get_region(INSIDE_TAG + warpName)

        underwater_rule = "is_underwater" in warpData and warpData["is_underwater"] == True

        entranceGroup = 0
        if option_dungeon_only:
            if "dungeon" in warpData:
                entranceGroup = OracleOfAgesConnectionType.CONNECT_DUNGEON
        else:
            if underwater_rule:
                entranceGroup += OracleOfAgesConnectionType.CONNECT_UNDERWATER
            if "present" not in warpData or warpData["present"] == False:
                entranceGroup += OracleOfAgesConnectionType.CONNECT_PAST
            if "dungeon" in warpData and option_dungeon_grouping:
                entranceGroup = OracleOfAgesConnectionType.CONNECT_DUNGEON # in dungeon grouping, dungeons are just dungeons
        
        exit_out = regionOutside.create_exit(OUTSIDE_TAG + warpName)
        exit_out.randomization_group = entranceGroup
        exit_out.randomization_type = EntranceType.TWO_WAY

        exit_in = regionInside.create_exit(INSIDE_TAG + warpName)
        exit_in.randomization_group = entranceGroup | OracleOfAgesConnectionType.CONNECT_INSIDE
        exit_in.randomization_type = EntranceType.TWO_WAY

        if underwater_rule:
            world.set_rule(exit_out, Has("Progressive Flippers", 2))
            world.set_rule(exit_in, Has("Progressive Flippers", 2))
        else:
            world.set_rule(exit_out, True_())
            world.set_rule(exit_in, True_())

        if dont_randomize:
            exit_out.connect(regionInside)
            exit_in.connect(regionOutside)
        else:
            world.randomized_entrances[warpName] = warpName
            
            target_out = regionOutside.create_er_target(OUTSIDE_TAG + warpName)
            target_out.randomization_group = entranceGroup
            target_out.randomization_type = EntranceType.TWO_WAY

            target_in = regionInside.create_er_target(INSIDE_TAG + warpName)
            target_in.randomization_group = entranceGroup | OracleOfAgesConnectionType.CONNECT_INSIDE
            target_in.randomization_type = EntranceType.TWO_WAY

    
# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_setup_group_pairing(world: OracleOfAgesWorld):

    option_dungeon_only = world.options.entrance_randomizer == OracleOfAgesEntranceRandomizer.option_dungeon_only
    option_surface_underwater_grouping = world.options.entrance_randomizer_surface_underwater_pairing
    option_past_present_grouping = world.options.entrance_randomizer_past_present_pairing

    world.entrance_group_lookup[OracleOfAgesConnectionType.CONNECT_DUNGEON] = [OracleOfAgesConnectionType.CONNECT_DUNGEON | OracleOfAgesConnectionType.CONNECT_INSIDE] 
    world.entrance_group_lookup[OracleOfAgesConnectionType.CONNECT_DUNGEON | OracleOfAgesConnectionType.CONNECT_INSIDE] = [OracleOfAgesConnectionType.CONNECT_DUNGEON] 

    groupings = []
    if option_dungeon_only == False:
        if option_surface_underwater_grouping:
            if option_past_present_grouping:
                groupings = [[OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PRESENT],
                            [OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PAST],
                            [OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PRESENT],
                            [OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PAST]]
            else:
                groupings = [[OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PRESENT, OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PAST],
                            [OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PRESENT, OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PAST]]
        else:
            if option_past_present_grouping:
                groupings = [[OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PRESENT, OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PRESENT],
                            [OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PAST, OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PAST]]
            else:
                groupings = [[OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PRESENT, OracleOfAgesConnectionType.CONNECT_OVERWORLD_SURFACE_PAST, 
                                OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PRESENT, OracleOfAgesConnectionType.CONNECT_OVERWORLD_UNDERWATER_PAST]]

    for grouping in groupings:
        for current_group in grouping:
            world.entrance_group_lookup[current_group] = [] 
            world.entrance_group_lookup[current_group | OracleOfAgesConnectionType.CONNECT_INSIDE] = [] 
            for paired_group in grouping:
                world.entrance_group_lookup[current_group].append(paired_group | OracleOfAgesConnectionType.CONNECT_INSIDE)
                world.entrance_group_lookup[current_group | OracleOfAgesConnectionType.CONNECT_INSIDE].append(paired_group)

# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_randomize_and_update_world_for_patch(world: OracleOfAgesWorld):

    er_targets = sorted([entrance for region in world.multiworld.get_regions(world.player)
                             for entrance in region.entrances if not entrance.parent_region], key=lambda x: x.name)
    exits = sorted([ex for region in world.multiworld.get_regions(world.player)
                        for ex in region.exits if not ex.connected_region], key=lambda x: x.name)


    placement_state = randomize_entrances(world, True, world.entrance_group_lookup)

    for warp_name, warp_destination in world.randomized_entrances.items():
        inside_entrance = world.get_entrance(OUTSIDE_TAG + warp_name).connected_region.name
        outside_entrance = world.get_entrance(inside_entrance).connected_region.name
        if inside_entrance.startswith(INSIDE_TAG):
            world.randomized_entrances[warp_name] = inside_entrance[len(INSIDE_TAG):]
    
# -----------------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------------
def ooa_connect_entrance_according_to_slot_data(world: OracleOfAgesWorld):
    for warp_name, warp_destination in world.randomized_entrances.items():
        outside_entrance = world.get_region(OUTSIDE_TAG + warp_name)
        inside_entrance = world.get_region(INSIDE_TAG + warp_destination)
        
        outside_entrance.connect(inside_entrance)
        inside_entrance.connect(outside_entrance)

        


    
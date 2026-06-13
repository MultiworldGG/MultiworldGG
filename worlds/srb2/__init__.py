import typing
import os
import json
from .Items import (item_data_table, zones_item_data_table, character_item_data_table, other_item_table, item_table, mpmatch_item_table, traps_item_data_table, special_item_data_table, acts_item_data_table, objects_item_table,
                    nights_item_table, objects_item_table, custom_item_data_table, SRB2Item)
from .Locations import (location_table,
                  GFZ_table,THZ_table,DSZ_table,CEZ_table,ACZ_table,
                  RVZ_table,ERZ_table,BCZ_table,FHZ_table,PTZ_table,FFZ_table,FDZ_table,HHZ_table,AGZ_table,ATZ_table,
                  FFSP_table,TPSP_table,FCSP_table,CFSP_table,DWSP_table,MCSP_table,ESSP_table,BHSP_table,
                  CCSP_table,DHSP_table,APSP_table,EXTRA_table,tokens_table,
                  GFZ_1UP_monitors,THZ_1UP_monitors,DSZ_1UP_monitors,CEZ_1UP_monitors,ACZ_1UP_monitors,RVZ_1UP_monitors,
                  ERZ_1UP_monitors,BCZ_1UP_monitors,FHZ_1UP_monitors,PTZ_1UP_blocks,FFZ_1UP_monitors,FDZ_1UP_monitors,
                  HHZ_1UP_monitors,AGZ_1UP_monitors,ATZ_1UP_monitors,MPSFZ_1UP_monitors,
                  GFZ_ring_monitors,THZ_ring_monitors,DSZ_ring_monitors,CEZ_ring_monitors,ACZ_ring_monitors,RVZ_ring_monitors,
                  ERZ_ring_monitors,FHZ_ring_monitors,PTZ_1UP_blocks,FFZ_ring_monitors,FDZ_ring_monitors,
                  HHZ_ring_monitors,AGZ_ring_monitors,ATZ_ring_monitors,
                  MPJVZ_monitors,MPNFZ_monitors,MPTPZ_monitors,MPTCZ_monitors,MPDTZ_monitors,MPFMZ_monitors,
                  MPOHZ_monitors,MPSFZ_monitors,MPDBZ_monitors,MPCSZ_monitors,MPFCZ_monitors,MPMMZ_monitors,
                  MPGLZ_monitors,MPSuShZ_monitors,MPSiShZ_monitors,MPUBZ_monitors,MPPSZ_monitors,MPCHZ_monitors,
                  MPMAZ_monitors,MPATZ_monitors, annoying_locations, SRB2Location)

from .Options import srb2_options_groups, SRB2Options
from .Rules import set_rules
from .Regions import create_regions, SRB2Zones
from BaseClasses import Item, Tutorial, ItemClassification, Region
from ..AutoWorld import World, WebWorld
import random
from multiprocessing import Process
from worlds.LauncherComponents import Component, components, Type, launch_subprocess, icon_paths

class SRB2Web(WebWorld):
   tutorials = [Tutorial(
       "Multiworld Setup Guide",
       "A guide to setting up SRB2 for MultiWorld.",
       "English",
       "setup_en.md",
       "setup/en",
       ["GraymonDgt"]
   )]

option_groups = srb2_options_groups

def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="SRB2Client")

components.append(Component(
    "Sonic Robo Blast 2 Client",
    func=launch_client,
    component_type=Type.CLIENT,
    icon = "emblem"
))
icon_paths["emblem"] = f"ap:{__name__}/srb2emblem.png"
class SRB2World(World):
    """ 
    Sonic Robo Blast 2 is a 3D open-source Sonic the Hedgehog fangame built using a modified version of the Doom Legacy port of Doom. SRB2 is closely inspired by the original Sonic games from the Sega Genesis, and attempts to recreate the design in 3D.
    """
    game: str = "Sonic Robo Blast 2"
    topology_present = False

    item_name_to_id = item_table
    location_name_to_id = location_table
    web = SRB2Web()

    item_name_groups = {
        "Act":acts_item_data_table,
        "Zone":zones_item_data_table,
        "Character":{**character_item_data_table,**custom_item_data_table},
        "Match Zone":mpmatch_item_table,
        "Trap":traps_item_data_table,
        "Shield":other_item_table,
        "Powerup":nights_item_table,
        "Nights Stage":special_item_data_table,
        "Object":objects_item_table
    }

    location_name_groups = {
        "Greenflower Zone":GFZ_table,
        "Greenflower 1UP Monitors": GFZ_1UP_monitors,
        "Greenflower Ring Monitors": GFZ_ring_monitors,
        "Techno Hill Zone": THZ_table,
        "Techno Hill 1UP Monitors": THZ_1UP_monitors,
        "Techno Hill Ring Monitors": THZ_ring_monitors,
        "Deep Sea Zone": DSZ_table,
        "Deep Sea 1UP Monitors": DSZ_1UP_monitors,
        "Deep Sea Ring Monitors": DSZ_ring_monitors,
        "Castle Eggman Zone":CEZ_table,
        "Castle Eggman 1UP Monitors": CEZ_1UP_monitors,
        "Castle Eggman Ring Monitors": CEZ_ring_monitors,
        "Arid Canyon Zone":ACZ_table,
        "Arid Canyon 1UP Monitors": ACZ_1UP_monitors,
        "Arid Canyon Ring Monitors": ACZ_ring_monitors,
        "Red Volcano Zone":RVZ_table,
        "Red Volcano 1UP Monitors": RVZ_1UP_monitors,
        "Red Volcano Ring Monitors": RVZ_ring_monitors,
        "Egg Rock Zone":ERZ_table,
        "Egg Rock 1UP Monitors": ERZ_1UP_monitors,
        "Egg Rock Ring Monitors": ERZ_ring_monitors,
        "Black Core Zone":BCZ_table,
        "Black Core 1UP Monitors": BCZ_1UP_monitors,
        "Frozen Hillside Zone":FHZ_table,
        "Frozen Hillside 1UP Monitors": FHZ_1UP_monitors,
        "Frozen Hillside Ring Monitors": FHZ_ring_monitors,
        "Pipe Towers Zone":PTZ_table,
        "Pipe Towers 1UP Blocks": PTZ_1UP_blocks,
        "Forest Fortress Zone":FFZ_table,
        "Forest Fortress 1UP Monitors": FFZ_1UP_monitors,
        "Forest Fortress Ring Monitors": FFZ_ring_monitors,
        "Final Demo Zone": FDZ_table,
        "Final Demo 1UP Monitors": FDZ_1UP_monitors,
        "Final Demo Ring Monitors": FDZ_ring_monitors,
        "Haunted Heights Zone":HHZ_table,
        "Haunted Heights 1UP Monitors": HHZ_1UP_monitors,
        "Haunted Heights Ring Monitors": HHZ_ring_monitors,
        "Aerial Garden Zone":AGZ_table,
        "Aerial Garden 1UP Monitors": AGZ_1UP_monitors,
        "Aerial Garden Ring Monitors": AGZ_ring_monitors,
        "Azure Temple Zone":ATZ_table,
        "Azure Temple 1UP Monitors": AGZ_1UP_monitors,
        "Azure Temple Ring Monitors": AGZ_ring_monitors,
        "Floral Field Zone":FFSP_table,
        "Toxic Plateau Zone":TPSP_table,
        "Flooded Cove Zone":FCSP_table,
        "Cavern Fortress Zone":CFSP_table,
        "Dusty Wasteland Zone":DWSP_table,
        "Egg Satellite Zone":ESSP_table,
        "Black Hole Zone":BHSP_table,
        "Christmas Chime Zone":CCSP_table,
        "Dream Hill Zone":DHSP_table,
        "Alpine Paradise Zone":APSP_table,
        "Emerald Tokens":tokens_table,

        "1UP Monitors":{**GFZ_1UP_monitors,**THZ_1UP_monitors,**DSZ_1UP_monitors,**CEZ_1UP_monitors,**ACZ_1UP_monitors,**RVZ_1UP_monitors,**
                  ERZ_1UP_monitors,**BCZ_1UP_monitors,**FHZ_1UP_monitors,**PTZ_1UP_blocks,**FFZ_1UP_monitors,**FDZ_1UP_monitors,**
                  HHZ_1UP_monitors,**AGZ_1UP_monitors,**ATZ_1UP_monitors,**MPSFZ_1UP_monitors},
        "Ring Monitors":{**GFZ_ring_monitors,**THZ_ring_monitors,**DSZ_ring_monitors,**CEZ_ring_monitors,**ACZ_ring_monitors,**RVZ_ring_monitors,
                  **ERZ_ring_monitors,**FHZ_ring_monitors,**PTZ_1UP_blocks,**FFZ_ring_monitors,**FDZ_ring_monitors,
                  **HHZ_ring_monitors,**AGZ_ring_monitors,**ATZ_ring_monitors,
                  **MPJVZ_monitors,**MPNFZ_monitors,**MPTPZ_monitors,**MPTCZ_monitors,**MPDTZ_monitors,**MPFMZ_monitors,
                  **MPOHZ_monitors,**MPSFZ_monitors,**MPDBZ_monitors,**MPCSZ_monitors,**MPFCZ_monitors,**MPMMZ_monitors,
                  **MPGLZ_monitors,**MPSuShZ_monitors,**MPSiShZ_monitors,**MPUBZ_monitors,**MPPSZ_monitors,**MPCHZ_monitors,
                  **MPMAZ_monitors,**MPATZ_monitors},
        "Match Monitors":{**MPSFZ_1UP_monitors,**MPJVZ_monitors,**MPNFZ_monitors,**MPTPZ_monitors,**MPTCZ_monitors,**MPDTZ_monitors,**MPFMZ_monitors,
                  **MPOHZ_monitors,**MPSFZ_monitors,**MPDBZ_monitors,**MPCSZ_monitors,**MPFCZ_monitors,**MPMMZ_monitors,
                  **MPGLZ_monitors,**MPSuShZ_monitors,**MPSiShZ_monitors,**MPUBZ_monitors,**MPPSZ_monitors,**MPCHZ_monitors,
                  **MPMAZ_monitors,**MPATZ_monitors},
        "Annoying Locations":annoying_locations

    }



    required_client_version = (0, 3, 5)

    area_connections: typing.Dict[int, int]

    options_dataclass = SRB2Options

    number_of_locations: int
    filler_count: int
    star_costs: typing.Dict[str, int]

    # Spoiler specific variable(s)
    star_costs_spoiler_key_maxlen = len(max([
        'First Floor Big Star Door',
        'Basement Big Star Door',
        'Second Floor Big Star Door',
        'MIPS 1',
        'MIPS 2',
        'Endless Stairs',
    ], key=len))


    def generate_early(self):

        max_locations = 181#TODO up this once i have enough locations
        if self.options.time_emblems:
            max_locations += 27
        if self.options.ring_emblems:
            max_locations += 20
        if self.options.score_emblems:
            max_locations += 7
        if self.options.nights_maps:
            max_locations += 36
            if self.options.rank_emblems:
                max_locations += 12
            if self.options.ntime_emblems:
                max_locations += 12

        if self.options.oneup_sanity:
            max_locations += 247

        if self.options.superring_sanity:
            max_locations += 598

        if self.options.match_maps:
            max_locations += 21
            if self.options.oneup_sanity:
                max_locations += 1
            if self.options.superring_sanity:
                max_locations += 379


        #if self.options.superring_sanity and not self.options.oneup_sanity:#im going insane
        #    max_locations +=1
        self.number_of_locations = max_locations
        self.move_rando_bitvec = 0



    def create_regions(self):
        create_regions(self.multiworld, self.options, self.player)

    def set_rules(self):
        self.area_connections = {}
        set_rules(self.multiworld, self.options, self.player, self.area_connections, self.move_rando_bitvec)


    def create_item(self, name: str) -> Item:
        data = item_data_table[name]
        item = SRB2Item(name, data.classification, data.code, self.player)

        return item

    def create_items(self):
            disable_objects = False
            if self.options.object_locking:
                if self.options.superring_sanity and self.options.superring_sanity:
                    disable_objects = False

            # 1Up Mushrooms
            #actsanity valid starts w/ object rando
            #gfz1, thz1hard, dsz2? cez1 erz2
            if not self.options.actsanity:
                if not self.options.object_locking and disable_objects == False:
                    Valid_starts = ["Greenflower Zone", "Techno Hill Zone", "Deep Sea Zone", "Castle Eggman Zone",
                            "Arid Canyon Zone", "Red Volcano Zone", "Egg Rock Zone"]
                else:
                    Valid_starts = ["Greenflower Zone", "Techno Hill Zone", "Deep Sea Zone", "Castle Eggman Zone",
                            "Arid Canyon Zone", "Egg Rock Zone"]#zone boss means these always have a sphere 1
            else:

                if not self.options.object_locking and disable_objects == False:
                    Valid_starts = ["Greenflower Zone (Act 1)", "Greenflower Zone (Act 2)", "Techno Hill Zone (Act 1)",
                                    "Techno Hill Zone (Act 2)", "Deep Sea Zone (Act 1)", "Deep Sea Zone (Act 2)",
                                    "Castle Eggman Zone (Act 1)", "Castle Eggman Zone (Act 2)",
                                    "Arid Canyon Zone (Act 1)", "Arid Canyon Zone (Act 2)", "Red Volcano Zone (Act 1)",
                                    "Egg Rock Zone (Act 1)", "Egg Rock Zone (Act 2)",
                                    "Frozen Hillside Zone", "Pipe Towers Zone", "Forest Fortress Zone"]
                elif self.options.superring_sanity:
                        Valid_starts = ["Greenflower Zone (Act 1)","Greenflower Zone (Act 2)","Techno Hill Zone (Act 1)", "Deep Sea Zone (Act 2)",
                                        "Castle Eggman Zone (Act 1)","Castle Eggman Zone (Act 2)", "Arid Canyon Zone (Act 1)","Arid Canyon Zone (Act 2)","Red Volcano Zone (Act 1)",
                                        "Egg Rock Zone (Act 1)","Egg Rock Zone (Act 2)","Frozen Hillside Zone","Pipe Towers Zone"]
                elif self.options.oneup_sanity:
                        Valid_starts = ["Greenflower Zone (Act 1)","Techno Hill Zone (Act 1)", "Deep Sea Zone (Act 2)",
                                        "Castle Eggman Zone (Act 1)", "Arid Canyon Zone (Act 1)","Red Volcano Zone (Act 1)","Egg Rock Zone (Act 2)","Frozen Hillside Zone","Pipe Towers Zone"]
                else:
                        Valid_starts = ["Greenflower Zone (Act 1)", "Techno Hill Zone (Act 1)",
                                        "Castle Eggman Zone (Act 1)",
                                        "Egg Rock Zone (Act 2)"]  # append forest fortress if starting character can get through spin walls

            rand_idx = random.randrange(len(Valid_starts))

            Starting_zone = Valid_starts[rand_idx]
            self.multiworld.push_precollected(self.create_item(Starting_zone))



            slots_to_fill = self.number_of_locations

            if self.options.object_locking and disable_objects == False:
                for object_name in objects_item_table:
                    self.multiworld.itempool += [self.create_item(object_name)]
                    slots_to_fill -= 1
            else:
                for object_name in objects_item_table:
                    self.multiworld.push_precollected(self.create_item(object_name))







            if self.options.actsanity:
                for act_name in acts_item_data_table.keys():
                    if act_name == Starting_zone:
                        continue
                    if self.options.completion_type == 1 or self.options.completion_type == 0 or self.options.completion_type == 3:
                        if act_name == "Black Core Zone (Act 3)" and self.options.bcz_emblem_percent > 0:
                            continue
                    if self.options.completion_type == 2:
                        if (act_name == "Haunted Heights Zone" or act_name == "Aerial Garden Zone" or act_name == "Azure Temple Zone") and self.options.bcz_emblem_percent > 0:
                            continue
                    slots_to_fill-=1
                    self.multiworld.itempool += [self.create_item(act_name)]
            else:
                for zone_name in zones_item_data_table.keys():
                    if zone_name == Starting_zone:
                        continue
                    if self.options.completion_type == 1 or self.options.completion_type == 0 or self.options.completion_type == 3:
                        if zone_name == "Black Core Zone" and self.options.bcz_emblem_percent > 0:
                            continue
                    if self.options.completion_type == 2:
                        if (zone_name == "Haunted Heights Zone" or zone_name == "Aerial Garden Zone" or zone_name == "Azure Temple Zone") and self.options.bcz_emblem_percent > 0:
                            continue
                    slots_to_fill-=1
                    self.multiworld.itempool += [self.create_item(zone_name)]#and != starting_zone
            #not concise because I need to keep track of slots_to_fill
            char_list = []

            if self.options.random_start_char:
                length = 0
                for i in self.options.starting_character:
                    length += 1#len() didnt work and im too tired to figure out why
                rand_char = random.randrange(length)
                length = 0
                for i in self.options.starting_character:
                    if length == rand_char:
                        self.multiworld.push_precollected(self.create_item(i))
                        char_list.append(i)
                        break
                    length += 1#len() didnt work and im too tired to figure out why



            else:
                for char_name in self.options.starting_character:
                    self.multiworld.push_precollected(self.create_item(char_name))
                    char_list.append(char_name)



            for char_name in self.options.character_list:
                if char_name in char_list:
                    continue
                self.multiworld.itempool += [self.create_item(char_name)]
                slots_to_fill -= 1




            for shield in other_item_table.keys():
                self.multiworld.itempool += [self.create_item(shield)]
                slots_to_fill -=1
            if self.options.nights_maps:
                for spstage in special_item_data_table.keys():
                    if self.options.actsanity:
                        if spstage == "Alpine Paradise Zone":
                            self.multiworld.itempool += [self.create_item("Alpine Paradise Zone (Act 1)")]
                            self.multiworld.itempool += [self.create_item("Alpine Paradise Zone (Act 2)")]
                            slots_to_fill -= 2
                            continue
                    self.multiworld.itempool += [self.create_item(spstage)]
                    slots_to_fill -=1
                for shield in nights_item_table.keys():
                    self.multiworld.itempool += [self.create_item(shield)]
                    slots_to_fill -=1

            if self.options.match_maps:
                for zone in mpmatch_item_table.keys():
                    self.multiworld.itempool += [self.create_item(zone)]
                    slots_to_fill -= 1



            self.multiworld.itempool += [self.create_item("Chaos Emerald") for i in range(7)]
            slots_to_fill -= 7

            if self.options.radar_start:
                self.multiworld.push_precollected(self.create_item("Progressive Emblem Hint"))
                self.multiworld.push_precollected(self.create_item("Progressive Emblem Hint"))
            else:
                self.multiworld.itempool += [self.create_item("Progressive Emblem Hint")]
                self.multiworld.itempool += [self.create_item("Progressive Emblem Hint")]
                slots_to_fill -= 2

            self.multiworld.itempool += [self.create_item("+5 Starting Rings") for i in range(2)]
            slots_to_fill -= 2


            target_emblems = self.options.num_emblems

            if target_emblems > slots_to_fill:
                target_emblems = slots_to_fill

            for i in range(0,target_emblems):
                self.multiworld.itempool += [self.create_item("Emblem")]
                slots_to_fill -=1


            self.options.bcz_emblem_percent.value = round(target_emblems * (self.options.bcz_emblem_percent.value/100))

            if slots_to_fill != 0:
                self.multiworld.itempool += [self.create_item("Sound Test")]
                slots_to_fill -= 1

            if slots_to_fill>99:
                for i in range(int(slots_to_fill/100)):
                    self.multiworld.itempool += [self.create_item("+5 Starting Rings")]
                    slots_to_fill -= 1


            if slots_to_fill > 0:
                trap_slots = int(slots_to_fill*self.options.trap_percentage/100)
                total_trap_weights = 0
                for trap_weight in self.options.trap_weights:
                    total_trap_weights += self.options.trap_weights[trap_weight]
                ratio = trap_slots/total_trap_weights
                for trap in self.options.trap_weights:
                    for i in range(int(ratio*self.options.trap_weights[trap])):
                        self.multiworld.itempool += [self.create_item(trap)]
                        slots_to_fill -=1

            if slots_to_fill > 0:
                filler_slots = slots_to_fill
                total_filler_weights = 0
                for filler_weight in self.options.filler_weights:
                    total_filler_weights += self.options.filler_weights[filler_weight]
                ratio = filler_slots/total_filler_weights
                for filler in self.options.filler_weights:
                    for i in range(int(ratio*self.options.filler_weights[filler])):
                        self.multiworld.itempool += [self.create_item(filler)]
                        slots_to_fill -= 1

            while slots_to_fill > 0:
                self.multiworld.itempool += [self.create_item("1UP")]
                slots_to_fill -= 1


    def generate_basic(self): #use to force items in a specific location
        #self.multiworld.get_location()
        return
           #self.multiworld.get_location("BoB: Bob-omb Buddy", self.player).place_locked_item(self.create_item("Cannon Unlock BoB"))


    def get_filler_item_name(self) -> str:
        return "1UP"

    def fill_slot_data(self):
        return {
            "RingLink": self.options.ring_link.value,
            "DeathLink": self.options.death_link.value,
            "CompletionType": self.options.completion_type.value,
            "BlackCoreEmblems": self.options.bcz_emblem_percent.value,
            "EnableMatchMaps": self.options.match_maps.value,
            "ActSanity":self.options.actsanity.value,
            "LocalRingReset":self.options.ring_reset_zone_exit.value
        }

    def generate_output(self, output_directory: str):
        if self.multiworld.players != 1:
            return
        data = {
            "slot_data": self.fill_slot_data(),
            "location_to_item": {self.location_name_to_id[i.name] : item_table[i.item.name] for i in self.multiworld.get_locations()},
            "data_package": {
                "data": {
                    "games": {
                        self.game: {
                            "item_name_to_id": self.item_name_to_id,
                            "location_name_to_id": self.location_name_to_id
                        }
                    }
                }
            }
        }
        filename = f"{self.multiworld.get_out_file_name_base(self.player)}.apsrb2"
        with open(os.path.join(output_directory, filename), 'w') as f:
            json.dump(data, f)

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        return

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # Write calculated star costs to spoiler.
        star_cost_spoiler_header = '\n\n' + self.player_name + ' line 159, TODO find out what this does:\n\n'
        spoiler_handle.write(self.player_name)
        # - Reformat star costs dictionary in spoiler to be a bit more readable.



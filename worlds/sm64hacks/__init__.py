import settings
import math
from worlds.AutoWorld import World
from worlds.generic.Rules import add_rule
from typing import Union, Tuple, List, Dict, Set, ClassVar, Mapping, Any
from .Options import SM64HackOptions
from .Items import SM64HackItem, item_is_important
from .Locations import SM64HackLocation, location_names, location_names_that_exist
from .Data import sm64hack_items, star_like, traps, junk, useful, moves, badges, sr6_25_locations, create_json_folders, Data, cannons, fullmoves, tickets, badge_items
from .Requirements import check_requirement_string
from .WebWorld import SM64HackWebWorld
from .client import SM64HackClient
from settings import get_settings
from BaseClasses import Region, Location, Entrance, Item, ItemClassification, CollectionState, EntranceType
from Utils import visualize_regions
import logging
logger = logging.getLogger("SM64 Romhack")

class SM64HackSettings(settings.Group):
    class AutoUpdate(settings.Bool):
        """Automatically download updated json files from GitHub when generating SM64Hack worlds"""
    auto_update: AutoUpdate | bool = True



class SM64HackWorld(World):
    """
    The first Super Mario game to feature 3D gameplay, but heavily modded - with support for a lot of popular rom hacks.
    """
    game = "SM64 Romhack"
    options_dataclass = SM64HackOptions
    options: SM64HackOptions
    web = SM64HackWebWorld()
    settings: ClassVar[SM64HackSettings]
    topology_present = True
    explicit_indirect_conditions = False #it might be possible to avoid doing this by checking the requirements but that sounds quite annoying to do and regardless this feels safer incase i fuck up.
    data: Data

    base_id = 40693

    item_name_to_id = {name: id for
                       id, name in enumerate(sm64hack_items, base_id)}

    location_name_to_id = {name: id for
                       id, name in enumerate(location_names(), base_id)}
    
    item_name_groups = {
        "Tickets": tickets,
        "Cannons": cannons,
        "Moves": fullmoves,
        "Badges": badge_items
    }

    location_name_groups = {
        "Course 1": set(i for i in location_names() if i.startswith("Course 1")),
        "Course 2": set(i for i in location_names() if i.startswith("Course 2")),
        "Course 3": set(i for i in location_names() if i.startswith("Course 3")),
        "Course 4": set(i for i in location_names() if i.startswith("Course 4")),
        "Course 5": set(i for i in location_names() if i.startswith("Course 5")),
        "Course 6": set(i for i in location_names() if i.startswith("Course 6")),
        "Course 7": set(i for i in location_names() if i.startswith("Course 7")),
        "Course 8": set(i for i in location_names() if i.startswith("Course 8")),
        "Course 9": set(i for i in location_names() if i.startswith("Course 9")),
        "Course 10": set(i for i in location_names() if i.startswith("Course 10")),
        "Course 11": set(i for i in location_names() if i.startswith("Course 11")),
        "Course 12": set(i for i in location_names() if i.startswith("Course 12")),
        "Course 13": set(i for i in location_names() if i.startswith("Course 13")),
        "Course 14": set(i for i in location_names() if i.startswith("Course 14")),
        "Course 15": set(i for i in location_names() if i.startswith("Course 15")),
        "Bowser 1": set(i for i in location_names() if i.startswith("Bowser 1")),
        "Bowser 2": set(i for i in location_names() if i.startswith("Bowser 2")),
        "Bowser 3": set(i for i in location_names() if i.startswith("Bowser 3")),
        "Secret 1": set(i for i in location_names() if i.startswith("Secret 1")),
        "Secret 2": set(i for i in location_names() if i.startswith("Secret 2")),
        "Secret 3": set(i for i in location_names() if i.startswith("Secret 3")),
        "Slide": set(i for i in location_names() if i.startswith("Slide")),
        "Metal Cap Level": set(i for i in location_names() if i.startswith("Metal Cap ")),
        "Wing Cap Level": set(i for i in location_names() if i.startswith("Wing Cap ")),
        "Vanish Cap Level": set(i for i in location_names() if i.startswith("Vanish Cap ")),
        "Overworld": set(i for i in location_names() if i.startswith("Overworld")),
    }
    
    required_client_version: Tuple[int, int, int] = (0, 6, 0)

    def __init__(self,multiworld, player: int):
        self.stars_created = 0
        self.no_ticket_courses = set()
        super().__init__(multiworld, player)
        self.data = Data()

    @classmethod
    def stage_assert_generate(cls, multiworld): # this is supposed to be used for rom files but its the only bit of code that i could find that runs before everything and only once before generation so im using it
        create_json_folders(get_settings()["sm64hacks_options"]["auto_update"] and not hasattr(multiworld, "generation_is_fake"))

    def generate_early(self):
        json_val = self.options.json_file.value
        if isinstance(json_val, int):
            json_val = self.options.json_file.name_lookup[json_val]
        self.data.import_json(json_val)
        self.progressive_keys = self.options.progressive_keys.value
        
        if self.data.locations["Other"]["Settings"].get("Version") != "v0.5" and self.data.locations["Other"]["Settings"].get("Version") != "v0.6":
            raise ValueError("JSON is too old. \
                            \nPlease reimport the JSON into the website (https://dnvic.com/ArchipelagoGenerator), and export in order to use it with the current version")
        if self.progressive_keys == 3:
            try:
                self.progressive_keys = self.data.locations["Other"]["Settings"]["prog_key"]
            except TypeError:
                raise ValueError("JSON is too old and does not have a default for progressive keys")
        
        self.options.level_tickets.value &= self.data.locations["Other"]["Settings"].get("Entrances") not in {None, False} #only add tickets if the json supports it
        self.options.move_randomization.value &= (self.data.locations["Other"]["Settings"].get("Moves") not in {None, False} or self.options.force_move_randomization) #only add moves if the json supports it or if you are reckless
        if self.options.move_randomization:
            match self.options.starting_jump:
                case 0:
                    self.starting_jump = self.random.choice(["Progressive Jump", "Progressive Jump", "Progressive Jump", "Sideflip", "Long Jump", "Backflip"])
                    self.options.start_inventory.value |= {self.starting_jump:1}
                case 1:
                    self.starting_jump = "Progressive Jump"
                    self.options.start_inventory.value |= {self.starting_jump:1}
                case 2:
                    self.starting_jump = self.random.choice(["Dive", "Slidekick"])
                    self.options.start_inventory.value |= {self.starting_jump:1}
                case _:
                    self.starting_jump = None


        non_local_traps = [trap for trap in traps if trap not in ["Mario Choir", "Spin Trap", "Tempo Trap"]]
        self.options.non_local_items.value |= set(non_local_traps)

        if self.options.starting_tickets != 0 and self.options.level_tickets:
            courses = [course for course in self.data.locations if not self.data.locations[course].get("Overworld") and course in self.data.progression_courses]
            num_starting_courses = round((self.options.starting_tickets / 100) * len(courses))
            course_ticket_dict = {}
            for course in self.random.sample(courses, num_starting_courses):
                course_ticket_dict[f"{course} Ticket"] = 1
            self.options.start_inventory_from_pool.value |= course_ticket_dict
                    
        existing_location_names = location_names_that_exist(self.data, self.options)
        self.location_names_that_exist_to_id = dict(filter(lambda location: location[0] in existing_location_names, self.location_name_to_id.items()))

    def create_item(self, item: str, item_link = True) -> SM64HackItem:
        if item_link and item not in traps and item not in junk and item not in useful: #item link is dumb and i need to make all potentially progressive item_link items some sort of progression
            classification = ItemClassification.progression
            if item == "Power Star" or item == "Star Bundle" or item == "Blue Star" or item == "Blue Star Bundle":
                classification = ItemClassification.progression_deprioritized_skip_balancing
        else:
            alwaysuseful = False
            if item == "Power Star" or item == "Star Bundle":
                if self.stars_created < self.data.maxstarcount: #only create progression stars up to the max starcount for the hack
                    classification = ItemClassification.progression_deprioritized_skip_balancing
                    if item == "Power Star":
                        self.stars_created += 1
                    else:
                        self.stars_created += 2
                else:
                    classification = ItemClassification.useful
                if "decadeslater" in self.data.locations["Other"]["Settings"]:
                    classification = ItemClassification.progression_deprioritized_skip_balancing #given some things are decided by total star count not just blue/yellow stars this is a non-trivial problem that doesnt need to be solved since the game requires every star anyways
            
            elif item == "Blue Star" or item == "Blue Star Bundle":
                classification = ItemClassification.progression_deprioritized_skip_balancing
            elif item in traps:
                classification = ItemClassification.trap
            elif item in junk:
                classification = ItemClassification.filler
            elif item in useful:
                alwaysuseful = True
                classification = ItemClassification.useful
            elif item == "Steve":
                alwaysuseful = True
                classification = ItemClassification.useful | ItemClassification.trap #funny
            elif item.endswith("Star"): # cannon stars in sr6.25
                classification = ItemClassification.progression
                self.stars_created += 1
            elif item.endswith("Ticket"):
                classification = ItemClassification.progression #non-progressive tickets just dont exist
            else:
                classification = ItemClassification.progression if item_is_important(item, self.data) else ItemClassification.useful

            if hasattr(self.multiworld, "generation_is_fake") and classification == ItemClassification.useful and not alwaysuseful: #UT shenanigans
                classification = ItemClassification.progression if item != "Power Star" else ItemClassification.progression_deprioritized_skip_balancing
        return SM64HackItem(item, classification, self.item_name_to_id[item], self.player)

    def create_event(self, event: str):
        return SM64HackItem(event, ItemClassification.progression, None, self.player)

    def get_filler_item_name(self):
        total_weight = self.options.filler_trap_weight.value + self.options.filler_junk_weight.value + self.options.filler_useful_weight.value
        useful_percent = self.options.filler_useful_weight.value / total_weight
        trap_percent = self.options.filler_trap_weight.value / total_weight


        itemtype = self.random.uniform(0, 100)
        if itemtype < 1/100:
            return "Steve" #steve
        if itemtype < useful_percent * 100:
            return self.random.choice(useful)
        if itemtype < (useful_percent + trap_percent) * 100:
            enabledtraps = list(traps)
            if self.options.no_spin_trap:
                enabledtraps.remove("Spin Trap")
            return self.random.choice(enabledtraps)
        return self.random.choice(junk)
        

    def create_items(self) -> None:
        
        
        
        # Add items to the Multiworld.
        # If there are two of the same item, the item has to be twice in the pool.
        # Which items are added to the pool may depend on player settings,
        # e.g. custom win condition like triforce hunt.
        # Having an item in the start inventory won't remove it from the pool.
        # If an item can't have duplicates it has to be excluded manually.

        # List of items to exclude, as a copy since it will be destroyed below
        #exclude = [item for item in self.multiworld.precollected_items[self.player]]

        #for item in map(self.create_item, sm64hack_items):
        #    if item in exclude:
        #        exclude.remove(item)  # this is destructive. create unique list above
        #        self.multiworld.itempool.append(self.create_item("nothing"))
        #    else:
        #        self.multiworld.itempool.append(item)
        
        #add stars
        stars = 0
        bluestars = 0
        num_locations = len(self.location_names_that_exist_to_id)
        for course in self.data.locations:
            if(course == "Other"):
                continue
            if(f"{course} Cannon" in self.location_names_that_exist_to_id):
                self.multiworld.itempool += [self.create_item(f"{course} Cannon", False)]
                num_locations -= 1
            for i in range(8):
                if f"{course} Star {i + 1}" in self.location_names_that_exist_to_id:
                    if "sr6.25" not in self.data.locations["Other"]["Settings"] or (i != 7 or (course != "Course 1" and course != "Bowser 3")): #cannon star nonsense
                        stars += 1
                if f"{course} Blue Star {i + 1}" in self.location_names_that_exist_to_id:
                    bluestars += 1
                
            if self.options.level_tickets:
                if not self.data.locations[course].get("Overworld") and course in self.data.progression_courses:
                    self.multiworld.itempool += [self.create_item(f"{course} Ticket", False)]
                    num_locations -= 1
                else:
                    self.no_ticket_courses |= set([course])

        if self.progressive_keys > 0:
            for Key in range(2):
                if f"Key {Key + 1}" in self.location_names_that_exist_to_id:
                    self.multiworld.itempool += [self.create_item("Progressive Key", False)]
                    num_locations -= 1
        else:
            for Key in range(2):
                if sm64hack_items[Key] in self.location_names_that_exist_to_id:
                    self.multiworld.itempool += [self.create_item(sm64hack_items[Key], False)]
                    num_locations -= 1
        
        for item in range(2,5):
            if sm64hack_items[item] in self.location_names_that_exist_to_id:
                self.multiworld.itempool += [self.create_item(sm64hack_items[item], False)]
                num_locations -= 1
        
        if("sr7" in self.data.locations["Other"]["Settings"]):
            for item in range(5):
                if item < 2:
                    if badges[item] in self.location_names_that_exist_to_id:
                        self.multiworld.itempool += [self.create_item("Progressive Stomp Badge", False)]
                        num_locations -= 1
                else:
                    if badges[item] in self.location_names_that_exist_to_id:
                        self.multiworld.itempool += [self.create_item(badges[item], False)]
                        num_locations -= 1

        if("sr6.25" in self.data.locations["Other"]["Settings"]):
            self.multiworld.itempool += [self.create_item("Yellow Switch", False)]
            self.multiworld.itempool += [self.create_item("Overworld Cannon Star", False)]
            self.multiworld.itempool += [self.create_item("Bowser 2 Cannon Star", False)]
            stars += 8 #extra stars
            num_locations -= 3
        elif("sr3.5" in self.data.locations["Other"]["Settings"]):
            self.multiworld.itempool += [self.create_item("Black Switch", False)]
            num_locations -= 1
        elif("decadeslater" in self.data.locations["Other"]["Settings"]):
            self.multiworld.itempool += [self.create_item("Gray Switch", False)]
            num_locations -= 1
        elif(self.options.randomize_moat):
            if "Castle Moat" in self.location_names_that_exist_to_id:
                self.multiworld.itempool += [self.create_item("Castle Moat", False)]
                num_locations -= 1

        if(self.options.move_randomization):
            progressive_jumps = 3
            if "Triple Jump Badge" in self.location_names_that_exist_to_id:
                progressive_jumps -= 1
            if self.starting_jump == "Progressive Jump":
                progressive_jumps -= 1
            
            self.multiworld.itempool += [self.create_item(move, False) for move in moves if move != self.starting_jump]
            num_locations -= len([move for move in moves if move != self.starting_jump])
            self.multiworld.itempool += [self.create_item("Progressive Jump", False) for _ in range(progressive_jumps)]
            num_locations -= progressive_jumps
            if "Wall Badge" not in self.location_names_that_exist_to_id:
                self.multiworld.itempool += [self.create_item("Wallkick", False)]
                num_locations -= 1


        totalstars = stars + bluestars

        total_possible_star_bundles = math.floor(totalstars / 2)
        total_star_bundles = math.floor(total_possible_star_bundles * (self.options.star_bundles / 100))
        if(bluestars):
            star_bundles = math.floor(total_star_bundles / 2)
            blue_star_bundles = total_star_bundles - star_bundles
            stars -= star_bundles * 2
            bluestars -= blue_star_bundles * 2
            self.multiworld.itempool += [self.create_item("Star Bundle", False) for _ in range(star_bundles)]
            self.multiworld.itempool += [self.create_item("Blue Star Bundle", False) for _ in range(blue_star_bundles)]
        else:
            star_bundles = total_star_bundles
            blue_star_bundles = 0
            stars -= star_bundles * 2
            self.multiworld.itempool += [self.create_item("Star Bundle", False) for _ in range(star_bundles)]
        num_locations -= star_bundles
        num_locations -= blue_star_bundles

        totalstars = stars + bluestars

        if(num_locations >= totalstars):
            num_locations -= totalstars
            self.multiworld.itempool += [self.create_item("Power Star", False) for _ in range(stars)]
            self.multiworld.itempool += [self.create_item("Blue Star", False) for _ in range(bluestars)]
        else:
            total_star_bundles = totalstars - num_locations
            if(bluestars):
                star_bundles = math.floor(total_star_bundles / 2)
                blue_star_bundles = total_star_bundles - star_bundles
                stars -= star_bundles * 2
                bluestars -= blue_star_bundles * 2
            else:
                blue_star_bundles = 0
                star_bundles = total_star_bundles
                stars -= star_bundles * 2
                
            num_locations = num_locations - stars - star_bundles - bluestars - blue_star_bundles
            self.multiworld.itempool += [self.create_item("Star Bundle", False) for _ in range(star_bundles)] #because its first, the star bundles will be more progressive than the stars
            self.multiworld.itempool += [self.create_item("Power Star", False) for _ in range(stars)]
            self.multiworld.itempool += [self.create_item("Blue Star Bundle", False) for _ in range(blue_star_bundles)]
            self.multiworld.itempool += [self.create_item("Blue Star", False) for _ in range(bluestars)]
        
        if num_locations != 0:            
            self.multiworld.itempool += [self.create_item(self.get_filler_item_name(), False) for _ in range(num_locations)]

    def add_location_if_exists_to_region(self, location_name, seen_regions, course, zone):
        if location_name in self.location_names_that_exist_to_id:
            region = seen_regions[course, zone]
            region.add_locations(
                {location_name: self.location_names_that_exist_to_id[location_name]},
                SM64HackLocation
            )

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        if self.data.locations["Other"]["Settings"].get("Entrances"):
            seen_regions = {}
            for index, entrance in enumerate(self.data.locations["Other"]["Entrances"]):
                source_region = (entrance[0], entrance[1])
                if source_region not in seen_regions.keys():
                    seen_regions[source_region] = Region(f"{source_region[0]} Zone {source_region[1]}", self.player, self.multiworld)
                    self.multiworld.regions.append(seen_regions[source_region])
                destination_region = (entrance[2], entrance[3])
                if destination_region not in seen_regions.keys():
                    seen_regions[destination_region] = Region(f"{destination_region[0]} Zone {destination_region[1]}", self.player, self.multiworld)
                    self.multiworld.regions.append(seen_regions[destination_region])
                

                seen_regions[source_region].connect(
                    seen_regions[destination_region],
                    f"Entrance {index}",
                    lambda state, 
                           entrance_data = (entrance[0], entrance[2]), 
                           requirement_string = entrance[4]: 
                           check_requirement_string(state, self.player, requirement_string, self.options, self.data, entrancedata=entrance_data)
                )
                if(not entrance[5]): #as far as i can tell AP only has 1-way connections; theres a 1-way/2-way split for ER but thats just a flag so 1-way doesnt get shuffled with 2-way not actually logical without ER
                    seen_regions[destination_region].connect(
                        seen_regions[source_region],
                        f"Entrance {index} Reverse",
                        lambda state, 
                            entrance_data = (entrance[0], entrance[2]), 
                            requirement_string = entrance[4]: 
                            check_requirement_string(state, self.player, requirement_string, self.options, self.data, entrancedata=entrance_data)
                    )
                    
            menu_region.connect(seen_regions[("Overworld", '1')], "Starting Area")
            #assign items to regions
            #if anyone can think of a better way to do this than to loop over everything individually let me know
            for course, data in self.data.locations.items():
                match course:
                    case "Other":
                        for index, stardata in enumerate(data["Stars"]):
                            zone = stardata.get("Area")
                            if not zone:
                                zone = '1'
                            if index < 6:
                                location_name = sm64hack_items[index]
                                if index == 5:
                                    if "sr6.25" in self.data.locations["Other"]["Settings"]:
                                        location_name = "Yellow Switch"
                                    elif "sr3.5" in self.data.locations["Other"]["Settings"]:
                                        location_name = "Black Switch"
                                    elif "decadeslater" in self.data.locations["Other"]["Settings"]:
                                        location_name = "Gray Switch"
                            elif index == 6:
                                seen_regions[stardata["Level"], zone].add_locations(
                                    {"Victory Location": None},
                                    SM64HackLocation
                                )
                                continue
                            else: #badges
                                location_name = badges[index - 7]

                            if stardata.get("Level") is not None:
                                self.add_location_if_exists_to_region(location_name, seen_regions, stardata["Level"], zone)
                    case "Extra":
                        for index, stardata in enumerate(data["Stars"]):
                            zone = stardata.get("Area")
                            if not zone:
                                zone = '1'
                            location_name = sr6_25_locations[index + 1]
                            self.add_location_if_exists_to_region(location_name, seen_regions, course, zone)
                                # extra wont have cannons or other shit so it doesnt matter
                    case _:
                        for index, stardata in enumerate(data["Stars"]):
                            zone = stardata.get("Area")
                            if zone is None:
                                zone = '1'
                            location_name = f"{course} Star {index + 1}"
                            if index > 6 and "decadeslater" in self.data.locations["Other"]["Settings"]:
                                location_name = f"{course} Blue Star {index - 6}"
                            self.add_location_if_exists_to_region(location_name, seen_regions, course, zone)

                        for special in ["Cannon", "Troll Star", "Sign"]:
                            zone = data[special].get("Area")
                            if not zone:
                                zone = '1'
                            location_name = f"{course} {special}"
                            self.add_location_if_exists_to_region(location_name, seen_regions, course, zone)
        else:
            for course, data in self.data.locations.items():
                course_region = Region(course, self.player, self.multiworld)
                match course:
                    case "Other":
                        course_region.add_locations(
                            dict(filter(lambda location: location[0] in list(sm64hack_items[:6]), self.location_names_that_exist_to_id.items())),
                            SM64HackLocation
                        )
                        course_region.add_locations(
                            dict({"Victory Location": None}),
                            SM64HackLocation
                        )
                        if("sr7" in self.data.locations["Other"]["Settings"]):
                            course_region.add_locations(
                                dict(filter(lambda location: location[0] in badges, self.location_names_that_exist_to_id.items())),
                                SM64HackLocation
                            )
                        if("sr3.5" in self.data.locations["Other"]["Settings"]):
                            course_region.add_locations(
                                {"Black Switch": self.location_names_that_exist_to_id["Black Switch"]}
                            )
                    case "Extra": #EX only exists in sr6.25 (at least right now)
                        course_region.add_locations(
                            dict(filter(lambda location: location[0] in sr6_25_locations, self.location_names_that_exist_to_id.items())),
                            SM64HackLocation
                        )
                    case _:          
                        course_region.add_locations(
                            dict(filter(lambda location: location[0].startswith(course + ' '), self.location_names_that_exist_to_id.items())),
                            SM64HackLocation
                        )
                    
                    
                self.multiworld.regions.append(course_region)
                menu_region.connect(
                    course_region, 
                    f"{course} Connection", 
                    lambda state, requirement_string = data.get("Requirements"): check_requirement_string(state, self.player, requirement_string, self.options, self.data)
                )
    
    def add_requirement_if_location_exists(self, location_name, requirement_string, stardata = None):
        if location_name in self.location_names_that_exist_to_id:
            add_rule(self.multiworld.get_location(location_name, self.player),
                lambda state, requirement_string = requirement_string, stardata = stardata: check_requirement_string(state, self.player, requirement_string, self.options, self.data, stardata))

    def set_rules(self) -> None:
        for course in self.data.locations:
            if course == "Other":
                for item in range(6):
                    star_data = self.data.locations[course]["Stars"][item]
                    if item == 5:
                        if("sr6.25" in self.data.locations["Other"]["Settings"]):
                            self.add_requirement_if_location_exists("Yellow Switch", star_data.get("Requirements"))
                            continue
                        elif("sr3.5" in self.data.locations["Other"]["Settings"]):
                            self.add_requirement_if_location_exists("Black Switch", star_data.get("Requirements"))
                            continue
                        elif("decadeslater" in self.data.locations["Other"]["Settings"]):
                            self.add_requirement_if_location_exists("Gray Switch", star_data.get("Requirements"))
                            continue
                    location_name = sm64hack_items[item]
                    self.add_requirement_if_location_exists(location_name, star_data.get("Requirements"))

                if("sr7" in self.data.locations["Other"]["Settings"]):
                    for item in range(5):
                        star_data = self.data.locations[course]["Stars"][item + 7]
                        location_name = badges[item]
                        self.add_requirement_if_location_exists(location_name, star_data.get("Requirements"))

                star_data = self.data.locations[course]["Stars"][6]
                add_rule(self.multiworld.get_location("Victory Location", self.player),
                    lambda state, requirement_string = star_data.get("Requirements"): check_requirement_string(state, self.player, requirement_string, self.options, self.data))
                continue
            if course == "Extra":
                for star in range(8):
                    star_data = self.data.locations[course]["Stars"][star]
                    location_name = sr6_25_locations[star + 1]
                    self.add_requirement_if_location_exists(location_name, star_data.get("Requirements"))
                continue
                    
            for special in ["Cannon", "Troll Star", "Sign"]:
                star_data = self.data.locations[course][special]
                location_name = f"{course} {special}"
                self.add_requirement_if_location_exists(location_name, star_data.get("Requirements"))

            for star in range(8):
                if star == 7 and "decadeslater" in self.data.locations["Other"]["Settings"]:
                    continue
                star_data = self.data.locations[course]["Stars"][star]
                location_name = f"{course} Star {star + 1}"
                self.add_requirement_if_location_exists(location_name, star_data.get("Requirements"), (course, star))

                if "decadeslater" in self.data.locations["Other"]["Settings"]:
                    location_name = f"{course} Blue Star {star + 1}"
                    star_data = self.data.locations[course]["Stars"][star + 7]
                    self.add_requirement_if_location_exists(location_name, star_data.get("Requirements"), (course, star))
                
    
    def generate_basic(self) -> None:
        self.multiworld.get_location("Victory Location", self.player).place_locked_item(self.create_event("Victory"))
        if not self.options.randomize_moat.value and "Castle Moat" in self.location_names_that_exist_to_id:
            self.multiworld.get_location("Castle Moat", self.player).place_locked_item(self.create_item("Castle Moat", False))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        visualize_regions(self.multiworld.get_region("Menu", self.player), "sm64hacks.puml")

    def fill_slot_data(self) -> Mapping[str, Any]:
        decadeslater = 0
        if "decadeslater" in self.data.locations["Other"]["Settings"]:
            decadeslater = 1
            if "StartWithBlueStars" in self.options.hack_specific_options:
                decadeslater = 2
        return {
            "Cannons": self.data.locations["Other"]["Settings"]["cannons"],
            "ProgressiveKeys": self.progressive_keys,
            "DeathLink": self.options.death_link.value == True, # == True so it turns it into a boolean value
            "RingLink": self.options.ring_link.value,
            "Badges": "sr7" in self.data.locations["Other"]["Settings"],
            "sr6.25": "sr6.25" in self.data.locations["Other"]["Settings"],
            "sr3.5": "sr3.5" in self.data.locations["Other"]["Settings"],
            "decadeslater": decadeslater,
            "version": self.data.locations["Other"]["Settings"].get("Version"),
            "tickets": self.options.level_tickets.value == True,
            "moves": self.options.move_randomization.value == True,
            "NoTicketCourses": self.no_ticket_courses
        }
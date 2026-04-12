
import pkgutil
from typing import Any, Dict, List, Union

import orjson

from BaseClasses import Item, ItemClassification, Location, MultiWorld, Region, Tutorial

from worlds.AutoWorld import WebWorld, World

from .Items import RefunctItem, item_table, item_groups
from .Locations import location_table, RefunctLocation, starting_platform, platforms_with_button_on_them, platforms_without_button_ids, platforms_with_button_ids, block_brawl_scores, block_blub_scores
from .Options import Goal, RefunctOptions, Traps, Cubes, ExtraCubes, UnderwaterCubes, refunct_option_groups


class RefunctWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Refunct.",
            "English",
            "setup_en.md",
            "setup/en",
            ["Spineraks"],
        )
    ]


class RefunctWorld(World):
    """
    Refunct is a first-person platformer focused on movement and momentum.
    """

    game: str = "Refunct"
    options_dataclass = RefunctOptions
    option_groups = refunct_option_groups

    web = RefunctWeb()
    
    origin_region_name = "10010102"  # Platform 1-2

    item_name_to_id = {name: data.code for name, data in item_table.items()}

    location_name_to_id = {name: data.id for name, data in location_table.items()}
    
    item_name_groups = item_groups

    ap_world_version = "1.0.0"        
        
    def get_filler_item_name(self) -> str:
        return ":)"

    def create_items(self):
        items_to_add = []
        for name in item_table:
            if "Cluster" in name and name != "Cluster 1":
                items_to_add.append(name)
        items_to_add.append("Ledge Grab")
        items_to_add.append("Progressive Wall Jump")
        items_to_add.append("Progressive Wall Jump")
        items_to_add.append("Jump Pads")
        items_to_add.append("Swim")
        items_to_add.append("Pipes")
        items_to_add.append("Lifts")
            
        self.multiworld.push_precollected(self.create_item("Cluster 1"))
        
        self.amount_of_grass = self.options.amount_of_grass.value
        self.required_grass = (self.options.required_grass_percentage.value * self.amount_of_grass) // 100
        for _ in range(self.required_grass):
            items_to_add.append("Grass")
        for _ in range(self.amount_of_grass - self.required_grass):
            items_to_add.append(["Grass", True])
        for _ in range(250 - self.amount_of_grass):
            items_to_add.append("Flower")
            
        # cubes
        cube_bags = []
        total_locs_cubes = 0
        
        if self.options.cubes == Cubes.option_always:
            total_locs_cubes += 18
        if self.options.cubes == Cubes.option_red_cubes_bag:
            cube_bags.append("Red Cubes Bag")
            total_locs_cubes += 18
            
        if self.options.extra_cubes == ExtraCubes.option_always:
            total_locs_cubes += 10
        if self.options.extra_cubes == ExtraCubes.option_red_cubes_bag:
            cube_bags.append("Red Cubes Bag")
            total_locs_cubes += 10
        if self.options.extra_cubes == ExtraCubes.option_green_cubes_bag:
            cube_bags.append("Green Cubes Bag")
            total_locs_cubes += 10
            
        # if self.options.underwater_cubes == UnderwaterCubes.option_always:
        #     total_locs_cubes += 18
        # if self.options.underwater_cubes == UnderwaterCubes.option_red_cubes_bag:
        #     cube_bags.append("Red Cubes Bag")
        #     total_locs_cubes += 18
        # if self.options.underwater_cubes == UnderwaterCubes.option_blue_cubes_bag:
        #     cube_bags.append("Blue Cubes Bag")
        #     total_locs_cubes += 18
        
        cube_bags = sorted(list(set(cube_bags)))
        for c in cube_bags:
            items_to_add.append(c)
        for _ in range(total_locs_cubes - len(cube_bags)):
            items_to_add.append("Flower")
        
        num_unlocks = self.options.number_of_unlocks_per_minigame.value
        if "Vanilla Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Vanilla Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
                
        if "Seeker Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Seeker Minigame")
            for _ in range(10 - num_unlocks):
                items_to_add.append("Flower")
                
        if "Button Galore Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Button Galore Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
        
        if "OG Randomizer Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("OG Randomizer Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
                
        if "Block Brawl Minigame" in self.minigames:
            for color in ["Reds", "Blues", "Greens", "Yellows"]:
                for _ in range(num_unlocks):
                    items_to_add.append(f"Block Brawl Minigame {color}")
                for _ in range(20 - num_unlocks):
                    items_to_add.append("Flower")
                    
        if "Climb Line Minigame" in self.minigames:
            style = "Line"
            for _ in range(num_unlocks):
                items_to_add.append(f"Climb {style} Minigame")
            for _ in range(10 - num_unlocks):
                items_to_add.append("Flower")
        if "Climb Spiral Minigame" in self.minigames:
            style = "Spiral"
            for _ in range(num_unlocks):
                items_to_add.append(f"Climb {style} Minigame")
            for _ in range(10 - num_unlocks):
                items_to_add.append("Flower")
        if "Climb Chaos Minigame" in self.minigames:
            style = "Chaos"
            for _ in range(num_unlocks):
                items_to_add.append(f"Climb {style} Minigame")
            for _ in range(10 - num_unlocks):
                items_to_add.append("Flower")
                    
        if "Block Blub Minigame" in self.minigames:
            for color in ["Reds", "Blues", "Greens", "Yellows"]:
                for _ in range(num_unlocks):
                    items_to_add.append(f"Block Blub Minigame {color}")
                for _ in range(8 - num_unlocks):
                    items_to_add.append("Flower")
                    
        if "Refunct Mountain Minigame" in self.minigames:
            for _ in range(num_unlocks):
                items_to_add.append("Refunct Mountain Minigame")
            for _ in range(37 - num_unlocks):
                items_to_add.append("Flower")
                
        if self.options.nerf_minigame_checks.value:
            if "Vanilla Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Vanilla Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            # Seeker Minigame doesn't need locked flowers.
            if "Button Galore Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Button Galore Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "OG Randomizer Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "OG Randomizer Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "Block Brawl Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Block Brawl Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 60)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "Climb Line Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Climb Line" in i.name and "Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 20)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "Climb Spiral Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Climb Spiral" in i.name and "Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 20)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "Climb Chaos Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Climb Chaos" in i.name and "Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 20)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "Block Blub Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Block Blub Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 24)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
            if "Refunct Mountain Minigame" in self.minigames:
                location_names = [i.name for i in self.multiworld.get_locations(self.player) if "Refunct Mountain Minigame" in i.name]
                location_names_el = self.multiworld.random.sample(location_names, 27)
                for loc in location_names_el:
                    if "Flower" in items_to_add:
                        items_to_add.remove("Flower")
                        self.get_location(loc).place_locked_item(
                            self.create_item("Flower")
                        )
                        
        trap_items = []
        if self.options.traps == Traps.option_pretty or self.options.traps == Traps.option_all:
            trap_items = [
                "Dark skies",
                "No skylight",
                # "Disco sky",
                "Starry sky",
                "Red sky",
                "Hurricane",
            ] * 2
        if self.options.traps == Traps.option_all:
            trap_items += [
                "Slo-mo",
                "Fast-mo",
                "Blurrrrgh",
            ] * 2
        
        if trap_items:
            self.multiworld.random.shuffle(trap_items)
            for item in trap_items:
                if "Flower" in items_to_add:
                    items_to_add.remove("Flower")
                    items_to_add.append(item)
                    
        for item in items_to_add:
            if isinstance(item, list) and item[1] == True:
                self.multiworld.itempool.append(self.create_item(item[0], force_useful=True))
            else:
                self.multiworld.itempool.append(self.create_item(item))

    def create_regions(self):

        if hasattr(self.multiworld, "re_gen_passthrough"):
            self.minigames = self.multiworld.re_gen_passthrough[self.game]["minigames"]
            self.seeker_platforms = self.multiworld.re_gen_passthrough[self.game]["seeker_platforms"]
        else:
            minigames_weights = self.options.minigames_likeliness.value
            population = list(minigames_weights.keys())
            weights = list(minigames_weights.values())
            num_minigames = self.options.number_of_minigames.value
            if num_minigames == -1:
                num_minigames = len([w for w in weights if w > 0])

            k = min(num_minigames, len([w for w in weights if w > 0]))
            self.minigames = []
            for _ in range(k):
                choice = self.multiworld.random.choices(population=population, weights=weights, k=1)[0]
                idx = population.index(choice)
                self.minigames.append(choice)
                population.pop(idx)
                weights.pop(idx)

        regions = []
        
        def load_json_data_dict(data_name: str) -> Union[List[Any], Dict[str, Any]]:
            return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))

        clusters: Dict[int, Any] = load_json_data_dict("clusters.json")
        
        for key in clusters:
            regions.append(Region(f"{key}", self.player, self.multiworld))

        # We now need to add these regions to multiworld.regions so that AP knows about their existence.
        self.multiworld.regions += regions
        
        for loc_name, loc_data in [(a, b) for a, b in location_table.items()]:
            if loc_data.type_of_check == "Button" or \
                loc_data.type_of_check == "Platform" or \
                (self.options.cubes != Cubes.option_never and loc_data.type_of_check == "Cube") or \
                (self.options.extra_cubes != ExtraCubes.option_never and loc_data.type_of_check == "Extra Cube"):
                # (self.options.underwater_cubes != UnderwaterCubes.option_never and loc_data.type_of_check == "Underwater Cube"):
                region = None
                for cluster_key, node_list in clusters.items():
                    if loc_data.id in node_list:
                        region = cluster_key
                        break
                if region is None:
                    raise Exception(f"Could not find region for location {loc_name} with id {loc_data.id}")
                region_object = self.multiworld.get_region(f"{region}", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
            
        if "Vanilla Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Vanilla Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Vanilla"]:
                region_object = self.multiworld.get_region("Vanilla Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        # Seeker Minigame info
        all_platforms = platforms_without_button_ids.copy() + platforms_with_button_ids.copy()
        self.seeker_platforms = self.multiworld.random.sample(all_platforms, 10)
        
        if "Seeker Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Seeker Minigame", self.player, self.multiworld))
            search_for = []
            for id in self.seeker_platforms:
                search_for.append(((id % 10000) // 100, id % 100))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Seeker" and (b.main_nr, b.sub_nr) in search_for]:
                region_object = self.multiworld.get_region("Seeker Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Button Galore Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Button Galore Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Button Galore"]:
                region_object = self.multiworld.get_region("Button Galore Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
        
        if "OG Randomizer Minigame" in self.minigames:
            self.multiworld.regions.append(Region("OG Randomizer Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "OG Randomizer"]:
                region_object = self.multiworld.get_region("OG Randomizer Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
        
        if "Block Brawl Minigame" in self.minigames:
            for i, color in enumerate(["Reds", "Blues", "Greens", "Yellows"], start=1):
                self.multiworld.regions.append(Region(f"Block Brawl Minigame {color}", self.player, self.multiworld))
                for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Block Brawl" and b.main_nr == i]:
                    region_object = self.multiworld.get_region(f"Block Brawl Minigame {color}", self.player)
                    region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Climb Line Minigame" in self.minigames:
            style = "Line"
            self.multiworld.regions.append(Region(f"Climb {style} Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == f"Climb {style}"]:
                region_object = self.multiworld.get_region(f"Climb {style} Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Climb Spiral Minigame" in self.minigames:
            style = "Spiral"
            self.multiworld.regions.append(Region(f"Climb {style} Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == f"Climb {style}"]:
                region_object = self.multiworld.get_region(f"Climb {style} Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                
        if "Climb Chaos Minigame" in self.minigames:
            style = "Chaos"
            self.multiworld.regions.append(Region(f"Climb {style} Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == f"Climb {style}"]:
                region_object = self.multiworld.get_region(f"Climb {style} Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
        
        if "Block Blub Minigame" in self.minigames:
            for i, color in enumerate(["Reds", "Blues", "Greens", "Yellows"], start=1):
                self.multiworld.regions.append(Region(f"Block Blub Minigame {color}", self.player, self.multiworld))
                for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Block Blub" and b.main_nr == i]:
                    region_object = self.multiworld.get_region(f"Block Blub Minigame {color}", self.player)
                    region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
                    
        if "Refunct Mountain Minigame" in self.minigames:
            self.multiworld.regions.append(Region("Refunct Mountain Minigame", self.player, self.multiworld))
            for loc_name, loc_data in [(a, b) for a, b in location_table.items() if b.minigame == "Refunct Mountain"]:
                region_object = self.multiworld.get_region("Refunct Mountain Minigame", self.player)
                region_object.locations.append(RefunctLocation(self.player, loc_name, loc_data.id, region_object))
        

        
        # OG Randomizer Minigame info
        self.set_og_randomizer_order()
    
    def set_og_randomizer_order(self):
        # OG Randomizer Minigame info
        dependences = {}
        dependences[13] = [3, 11, 14, 15, # 23, 
                           24, 27]
        dependences[16] = [2, 17, 28]
        dependences[18] = [8]
        dependences[22] = [3, 11, 12, 20, 30]
        
        somewhat_close = {
            1: [2,4,6,10,3],
            2: [1,4,16,17,15,3],
            3: [23,22,12,11,10,1,2,15,13],
            4: [1,2,16,28,5,18,6],
            5: [16,28,18,6,4],
            6: [1,10,4,5,18,7,8,9],
            7: [6,18,8],
            8: [10,9,6,7,18],
            9: [19,11,10,6,8],
            10: [11,3,1,6,8,9,19],
            11: [12,3,1,1,9,19,21,20,30],
            12: [22,23,3,11,20,30],
            13: [24,27,14,15,3,23,11],
            14: [13,15,17,27,24],
            15: [13,14,17,16,2,3],
            16: [17,15,2,1,4,5,38],
            17: [27,14,15,2,16,28],
            18: [4,5,6,7,8],
            19: [21,20,11,10,9],
            20: [30,12,11,21],
            21: [19,20,11],
            22: [30,23,12],
            23: [22,13,12,3,29,24],
            24: [23,22,30,29,25,26,27,14,13],
            25: [24,26,29],
            26: [29,25,24,27],
            27: [14,17,13,24,26],
            28: [17,16,4,5,18],
            29: [26,25,24,23,22,30],
            30: [20,11,12,22,23,29],
        }
        
        self.og_randomizer_order = [1]
        remaining = list(range(2, 31))
        prev_far = 0.5
        while len(remaining) > 0:
            last = self.og_randomizer_order[-1]
            possible_next = []
            close = []
            for r in remaining:
                add = False
                if r in dependences:
                    if any([d in self.og_randomizer_order for d in dependences[r]]):
                        add = True
                else:
                    add = True
                if add:
                    possible_next.append(r)
                    if r in somewhat_close[last]:
                        close.append(r)
            options_next = possible_next
            
            if close and self.multiworld.random.random() < prev_far:
                options_next = close
            next_cluster = self.multiworld.random.choice(options_next)
            
            if next_cluster in close:
                prev_far = max(0, prev_far - 0.1)
            else:
                prev_far = 1            

            self.og_randomizer_order.append(next_cluster)
            remaining.remove(next_cluster)
        self.og_randomizer_order.append(31)
        
    def set_rules(self):
        def load_json_data_list_of_lists(data_name: str) -> List[List[Any]]:
            return orjson.loads(pkgutil.get_data(__name__, "data/" + data_name).decode("utf-8-sig"))    
        
        all_connections = load_json_data_list_of_lists("connections.json")
        
        cube_reqs = {}
        if self.options.cubes == Cubes.option_always:
            cube_reqs["Cubes"] = None
        if self.options.cubes == Cubes.option_red_cubes_bag:
            cube_reqs["Cubes"] = "Red Cubes Bag"
        if self.options.extra_cubes == ExtraCubes.option_always:
            cube_reqs["Extra Cubes"] = None
        if self.options.extra_cubes == ExtraCubes.option_red_cubes_bag:
            cube_reqs["Extra Cubes"] = "Red Cubes Bag"
        if self.options.extra_cubes == ExtraCubes.option_green_cubes_bag:
            cube_reqs["Extra Cubes"] = "Green Cubes Bag"
                
        for connection in all_connections:
            a = connection[0]
            b = connection[1]
            abis = connection[2:]
            abis = [cube_reqs.get(abi, None) if abi in cube_reqs else abi for abi in abis]
            abis += [None] * (4 - len(abis))  # pad with None
                    
            c1 = ((a - 10010000) % 10000) // 100
            c2 = ((b - 10010000) % 10000) // 100
            region_a = self.multiworld.get_region(f"{a}", self.player)
            region_b = self.multiworld.get_region(f"{b}", self.player)
            name = f"{a} to {b} | {abis}"
            
            region_a.connect(region_b, name,
                lambda state, c1=c1, c2=c2, abis=abis: all([
                    state.has(f"Cluster {c1}", self.player),
                    state.has(f"Cluster {c2}", self.player),
                    abis[0] is None or state.has(abis[0], self.player, abis[1]),
                    abis[2] is None or state.has(abis[2], self.player, abis[3])
                ]))

                    
        possible_final_platforms = [i for i,j in location_table.items() if j.type_of_check == "Platform"]

                    
        self.goal = None
            # option_button_31_1 = 0
            # option_button_1_1 = 1
            # option_random_known_button = 2
            # option_random_unknown_button = 3
            # option_platform_1_5 = 4
            # option_platform_21_1 = 5
            # option_platform_29_2 = 6
            # option_random_known_platform = 7
            # option_random_unknown_platform = 8
            # option_random_known = 9
            # option_random_unknown = 10
        if self.options.goal.value == Goal.option_button_31_1:
            self.goal = ("B", (31,1))
        elif self.options.goal.value == Goal.option_button_1_1:
            self.goal = ("B", (1,1))
        elif self.options.goal.value == Goal.option_random_known_button or self.options.goal.value == Goal.option_random_unknown_button:
            valid_candidates = list(platforms_with_button_on_them.values())
            finish_button = self.multiworld.random.choice(valid_candidates)
            self.goal = ("B", (finish_button[0], finish_button[1]))
        elif self.options.goal.value == Goal.option_platform_1_5:
            self.goal = ("P", (1,5))
        elif self.options.goal.value == Goal.option_platform_21_1:
            self.goal = ("P", (21,1))
        elif self.options.goal.value == Goal.option_platform_29_2:
            self.goal = ("P", (29,2))
        elif self.options.goal.value == Goal.option_random_known_platform or self.options.goal.value == Goal.option_random_unknown_platform:
            valid_candidates = possible_final_platforms
            finish_platform_name = self.multiworld.random.choice(valid_candidates)
            self.goal = ("P", (int(finish_platform_name.split(" ")[1].split("-")[0]), int(finish_platform_name.split(" ")[1].split("-")[1])))
        elif self.options.goal.value == Goal.option_random_known or self.options.goal.value == Goal.option_random_unknown:
            if self.multiworld.random.random() < 0.5:
                valid_candidates = list(platforms_with_button_on_them.values())
                finish_button = self.multiworld.random.choice(valid_candidates)
                self.goal = ("B", (finish_button[0], finish_button[1]))
            else:
                valid_candidates = possible_final_platforms
                finish_platform_name = self.multiworld.random.choice(valid_candidates)
                self.goal = ("P", (int(finish_platform_name.split(" ")[1].split("-")[0]), int(finish_platform_name.split(" ")[1].split("-")[1])))

        victory_location_name = f"{'Button' if self.goal[0] == 'B' else 'Platform'} {self.goal[1][0]}-{self.goal[1][1]}"
        # self.get_location(victory_location_name).address = None
        self.get_location(victory_location_name).place_locked_item(
            self.create_item("Goal Location")
        )
        self.multiworld.completion_condition[self.player] = lambda state: all([state.has("Goal Location", self.player), state.has("Grass", self.player, self.required_grass)])

        
        
        # minigames
        if "Vanilla Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Vanilla Minigame", self.player)
            region_a.connect(region_b, f"Enter Vanilla Minigame", 
                lambda state: state.has("Vanilla Minigame", self.player))
            
        if "Seeker Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Seeker Minigame", self.player)
            region_a.connect(region_b, f"Enter Seeker Minigame", 
                lambda state: state.has("Seeker Minigame", self.player))
            
        if "Button Galore Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Button Galore Minigame", self.player)
            region_a.connect(region_b, f"Enter Button Galore Minigame", 
                lambda state: state.has("Button Galore Minigame", self.player))
        
        if "OG Randomizer Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("OG Randomizer Minigame", self.player)
            region_a.connect(region_b, f"Enter OG Randomizer Minigame", 
                lambda state: state.has("OG Randomizer Minigame", self.player))
            
        if "Block Brawl Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            for color in ["Reds", "Blues", "Greens", "Yellows"]:
                region_b = self.multiworld.get_region(f"Block Brawl Minigame {color}", self.player)
                region_a.connect(region_b, f"Enter Block Brawl Minigame {color}", 
                    lambda state, color=color: state.has(f"Block Brawl Minigame {color}", self.player))
                for i, score in enumerate(block_brawl_scores):
                    loc_name = f"Block Brawl Minigame: {color} Score {score}"
                    location = self.get_location(loc_name)
                    num_colors_needed = i // 5 + 1
                    location.access_rule = lambda state, num_colors_needed=num_colors_needed: all([
                        state.has_group_unique(f"Block Brawl Cubes", self.player, num_colors_needed),
                    ])
                                        
        if "Climb Line Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            style = "Line"
            region_b = self.multiworld.get_region(f"Climb {style} Minigame", self.player)
            region_a.connect(region_b, f"Enter Climb {style} Minigame", 
                lambda state, style=style: state.has(f"Climb {style} Minigame", self.player))
                    
        if "Climb Spiral Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            style = "Spiral"
            region_b = self.multiworld.get_region(f"Climb {style} Minigame", self.player)
            region_a.connect(region_b, f"Enter Climb {style} Minigame", 
                lambda state, style=style: state.has(f"Climb {style} Minigame", self.player))
                    
        if "Climb Chaos Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            style = "Chaos"
            region_b = self.multiworld.get_region(f"Climb {style} Minigame", self.player)
            region_a.connect(region_b, f"Enter Climb {style} Minigame", 
                lambda state, style=style: state.has(f"Climb {style} Minigame", self.player))
                    
        if "Block Blub Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            for color in ["Reds", "Blues", "Greens", "Yellows"]:
                region_b = self.multiworld.get_region(f"Block Blub Minigame {color}", self.player)
                region_a.connect(region_b, f"Enter Block Blub Minigame {color}", 
                    lambda state, color=color: state.has(f"Block Blub Minigame {color}", self.player))
                for i, score in enumerate(block_blub_scores):
                    loc_name = f"Block Blub Minigame: {color} Score {score}"
                    location = self.get_location(loc_name)
                    num_colors_needed = i // 2 + 1
                    location.access_rule = lambda state, num_colors_needed=num_colors_needed: all([
                        state.has_group_unique(f"Block Blub Cubes", self.player, num_colors_needed),
                    ])
            
        if "Refunct Mountain Minigame" in self.minigames:
            region_a = self.multiworld.get_region("10010102", self.player)
            region_b = self.multiworld.get_region("Refunct Mountain Minigame", self.player)
            region_a.connect(region_b, f"Enter Refunct Mountain Minigame", 
                lambda state: state.has("Refunct Mountain Minigame", self.player))
        

    def create_item(self, name: str, force_useful = False) -> Item:
        item_data = item_table[name]
        if force_useful:
            item = RefunctItem(name, ItemClassification.useful, item_data.code, self.player)
        else:
            item = RefunctItem(name, item_data.classification, item_data.code, self.player)
        return item

    def fill_slot_data(self):
        """
        make slot data, which consists of refunct_data, options, and some other variables.
        """
        slot_data = {}
                
        slot_data["amount_grass"] = self.amount_of_grass
        slot_data["required_grass"] = self.required_grass
        
        slot_data["goal_t"] = self.goal[0]
        slot_data["goal_c"] = self.goal[1][0]
        slot_data["goal_p"] = self.goal[1][1]
        slot_data["goal_known"] = self.options.goal.value not in [Goal.option_random_unknown, Goal.option_random_unknown_button, Goal.option_random_unknown_platform]
        
        slot_data["minigames"] = self.minigames
        
        slot_data["cubes"] = self.options.cubes.value
        slot_data["extra_cubes"] = self.options.extra_cubes.value
        # slot_data["underwater_cubes"] = self.options.underwater_cubes.value
        
        slot_data["seeker_platforms"] = self.seeker_platforms
        slot_data["og_randomizer_order"] = self.og_randomizer_order
        
        slot_data["death_link"] = self.options.death_link.value
        
        slot_data["ap_world_version"] = self.ap_world_version

        return slot_data

    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return {"minigames": slot_data["minigames"], "seeker_platforms": slot_data["seeker_platforms"]}

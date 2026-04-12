import math
from typing import Optional

from .Exceptions import RE2ROptionError

class WeaponRandomizer():
    def __init__(self, world, character, scenario):
        self.world = world
        self.random = world.random
        self.character = character
        self.scenario = scenario
        self.mode = None

        self.weapons_by_level = {
            'light': [item for item in world.item_name_to_item.values() if item.get('type') == 'Weapon' and 'light_gun' in item.get('groups', [])],
            'medium': [item for item in world.item_name_to_item.values() if item.get('type') == 'Weapon' and 'medium_gun' in item.get('groups', [])],
            'heavy': [item for item in world.item_name_to_item.values() if item.get('type') == 'Weapon' and 'heavy_gun' in item.get('groups', [])]
        }
        # ammo == None only applies for endgame items, which we want to avoid randomizing into the location of normal weapons
        self.all_weapons = [item for item in world.item_name_to_item.values() if item.get('type') == 'Weapon' and item.get('ammo', None) != None]
        self.starting_ammo_name = 'Handgun Ammo'
        self.world.replacement_weapons[self.world.player] = {}
        self.world.replacement_ammo[self.world.player] = {}
        self.swap_queue = {}

    ###
    # CrossScenarioWeapons == "Starting"
    ###
    def starting(self):
        self.mode = "starting"
        random_weapon = self._determine_starting_weapon()
        self._queue_swap(self.starting_ammo_name, random_weapon['ammo'], "Ammo")

        self._swap_queued_at_locations()

    ###
    # CrossScenarioWeapons == "Match"
    ###
    def match(self):
        self.mode = "match"
        random_weapon = self._determine_starting_weapon('light') # match starting weapon level too
        self._queue_swap(self.starting_ammo_name, random_weapon['ammo'], "Ammo")
        weapons = self._get_weapons_from_locations()
        
        for weapon in weapons:
            for key in self.weapons_by_level.keys():
                if "groups" in weapon and "{}_gun".format(key) in weapon["groups"]: 
                    if len(self.weapons_by_level[key]) > 0: # starting weapon takes 1 out of the pool, so check length
                        matched = self.random.choice(self.weapons_by_level[key])
                    
                        self._queue_swap(weapon['name'], matched['name'], "Weapon")
                        self._queue_swap(weapon['ammo'], matched['ammo'], "Ammo")

                        # remove anything that was placed so it's not placed again
                        self.weapons_by_level[key] = [i for i in self.weapons_by_level[key] if i['name'] != matched['name']]

        self._swap_queued_at_locations()

    ###
    # CrossScenarioWeapons == "Full"
    ###
    def full(self, include_ammo: Optional[bool] = True):
        self.mode = self.mode or "full"
        random_weapon = self._determine_starting_weapon()

        if include_ammo:
            self._queue_swap(self.starting_ammo_name, random_weapon['ammo'], "Ammo")

        weapons = self._get_weapons_from_locations()

        for weapon in weapons:
            matched = self.random.choice(self.all_weapons)

            self._queue_swap(weapon['name'], matched['name'], "Weapon")

            # by default, this includes ammo. for options that rando ammo completely, this will be False
            if include_ammo:
                self._queue_swap(weapon['ammo'], matched['ammo'], "Ammo")

            # remove anything that was placed so it's not placed again
            self.all_weapons = [i for i in self.all_weapons if i['name'] != matched['name']]

        self._swap_queued_at_locations()

    ###
    # CrossScenarioWeapons == "All"
    ###
    def all(self, include_ammo: Optional[bool] = True):
        self.mode = self.mode or "all"
        self._determine_starting_weapon()
        weapons = self._get_weapons_from_locations()
        all_weapons = [*self.all_weapons] # make a copy so we can remove from it

        # replace the base weapons...
        for weapon in weapons:
            matched = self.random.choice(all_weapons)
            self._queue_swap(weapon['name'], matched['name'], "Weapon")

            # remove anything that was placed so it's not placed again
            all_weapons = [i for i in all_weapons if i['name'] != matched['name']]

        self._swap_queued_at_locations()

        # count for repeating identifier for spoiler log
        str_repeat_count = 1

        # ... then place all the remaining weapons
        for loc in self._get_locations_for_extra_weapons():
            if len(all_weapons) == 0:
                break

            matched = self.random.choice(all_weapons)

            loc['original_item'] = matched['name']
            loc_key = self._get_location_key(loc['region'], loc['name'])
            self.world.source_locations[self.world.player][loc_key] = loc

            self.world.replacement_weapons[self.world.player]["_" * str_repeat_count] = matched['name']
            str_repeat_count += 1

            # remove anything that was placed so it's not placed again
            all_weapons = [i for i in all_weapons if i['name'] != matched['name']]

        if include_ammo:
            self._split_ammo_by_level()

    ###
    # CrossScenarioWeapons == "Full Ammo"
    ###    
    def full_ammo(self):
        self.mode = "full_ammo"
        self.full(include_ammo=False)
        self._split_ammo_randomly()

    ###
    # CrossScenarioWeapons == "All Ammo"
    ###
    def all_ammo(self):
        self.mode = self.mode or "all_ammo"
        self.all(include_ammo=False)
        self._split_ammo_randomly()

    # Since Troll also calls All Ammo, we need to set the correct mode before calling it
    def all_ammo_troll(self):
        self.mode = "troll"
        self.all_ammo()

    ###
    # CrossScenarioWeapons == "Troll"
    ###
    def troll(self, weapon_count=2):
        # self.all_ammo() is called during processing of options, and self.troll() is specifically called after upgrades, gunpowder, etc.

        self.mode = self.mode or "troll"
        weapons = [w for w in self._get_weapons_from_locations() if w['name'] != self.world.starting_weapon[self.world.player]]
        only_weapons = [self.world.item_name_to_item.get(self.world.starting_weapon[self.world.player])]

        for _ in range(weapon_count):
            random_weapon = self.random.choice(weapons)
            only_weapons.append(random_weapon)
            weapons = [w for w in weapons if w['name'] != random_weapon]

        only_weapons_names = [w['name'] for w in only_weapons]

        for loc in self._get_weapon_locations():
            if loc.get('force_item', None) is not None and loc.get('force_item') not in only_weapons_names:
                loc['force_item'] = 'Wooden Boards'
                loc_key = self._get_location_key(loc['region'], loc['name'])
                self.world.source_locations[self.world.player][loc_key] = loc
                continue

            if loc.get('original_item', None) is not None and loc.get('original_item') not in only_weapons_names:
                loc['original_item'] = 'Wooden Boards'
                loc_key = self._get_location_key(loc['region'], loc['name'])
                self.world.source_locations[self.world.player][loc_key] = loc
                continue

        self.world.replacement_weapons[self.world.player] = {
            "Other Random Weapons": [
                w['name'] for w in only_weapons 
                    if w['name'] != self.world.starting_weapon[self.world.player]
            ]
        }

    ###
    # CrossScenarioWeapons == "TrollStarting"
    ###
    def troll_starting(self):
        self.mode = "troll_starting"
        return self.troll(0) # remove all weapons except the starting weapon

    ###
    # Function to be called after ANY weapon rando, so that the upgrades for the included weapons are also included
    ###
    def upgrades(self):
        all_upgrades = [item for item in self.world.item_name_to_item.values() if item.get('type') == 'Upgrade']

        # Now, find all upgrade items (orig or force) on locations that aren't randomized=0, add those locations to list to swap,
        #    and swap their orig & force to an upgrade at random for one of the new random weapons.
        #    Then, fill in any gaps with the first value in replacement ammo to match the starting weapon's ammo.
        location_names_with_upgrades = []
        available_upgrades = [item["name"] for item in all_upgrades if item.get('upgrades') in self.world.replacement_weapons[self.world.player].values() or item.get('upgrades') == self.world.starting_weapon[self.world.player]] # match to new weapons

        # NEED TO CHECK LOCATIONS BELOW TO MAKE SURE THEY'RE ACTUALLY RANDO'D
        # (i.e., L-Hawk Laser Sight)

        for loc_name, loc in self._get_locations().items():
            original_item = loc.get("original_item", None)
            original_item = self.world.item_name_to_item.get(original_item, {})

            force_item = loc.get("force_item", None)
            force_item = self.world.item_name_to_item.get(force_item, {})

            if original_item.get("type") == "Upgrade" or force_item.get("type") == "Upgrade":
                # if the location isn't randomized, it means that the original item (upgrade) is likely not able to be randomized
                #    so, leave the upgrade there, and remove that upgrade from the available upgrades so we don't try to place it again
                if loc.get("randomized", 1) == 0:
                    available_upgrades = [i for i in available_upgrades if i != original_item['name']]

                    continue

                location_names_with_upgrades.append(loc_name)

        if len(available_upgrades) > 0:
            extra_locations_needed = len(available_upgrades) - len(location_names_with_upgrades)

            if extra_locations_needed > 0:
                available_locations_for_extra = self._get_locations_for_extra_weapons()

                for x in range(extra_locations_needed):
                    loc = available_locations_for_extra[x]
                    loc_key = self._get_location_key(loc['region'], loc['name'])
                    location_names_with_upgrades.append(loc_key)

        if len(location_names_with_upgrades) > 0:
            extra_upgrades_needed = len(location_names_with_upgrades) - len(available_upgrades)

            if extra_upgrades_needed > 0:
                for x in range(extra_upgrades_needed):
                    replacement_item = list(self.world.replacement_ammo[self.world.player].values())[0][0]

                    if isinstance(replacement_item, list):
                        replacement_item = replacement_item[0]

                    available_upgrades.append(replacement_item)

        for loc_name in location_names_with_upgrades:
            if self.world.source_locations[self.world.player][loc_name].get("force_item"):
                self.world.source_locations[self.world.player][loc_name]["force_item"] = available_upgrades.pop(0)
            elif self.world.source_locations[self.world.player][loc_name].get("original_item"):
                self.world.source_locations[self.world.player][loc_name]["original_item"] = available_upgrades.pop(0)

    ###
    # Function to be called after ANY weapon rando, so that the high-grade gunpowder is split to support any weapon's ammo
    ###
    def high_grade_gunpowder(self):
        location_names_with_hgg = [] # hgg = high grade gunpowder

        # Finally, find all high grade gunpowder in the scenario, and split it half-and-half between white and yellow.
        #    To account for any possible weapons that show up in the scenario.
        for loc_name, loc in self._get_locations().items():
            original_item = loc.get("original_item", "")
            force_item = loc.get("force_item", "")

            if "High-Grade Gunpowder" in original_item or "High-Grade Gunpowder" in force_item:
                location_names_with_hgg.append(loc_name)

        # Alternate back and forth playing Yellow and White
        counter = 0
        for loc_name in location_names_with_hgg:
            if counter % 2 == 0:
                if self.world.source_locations[self.world.player][loc_name].get("original_item"):
                    self.world.source_locations[self.world.player][loc_name]["original_item"] = "High-Grade Gunpowder - Yellow"
                
                if self.world.source_locations[self.world.player][loc_name].get("force_item"):
                    self.world.source_locations[self.world.player][loc_name]["force_item"] = "High-Grade Gunpowder - Yellow"
            else:
                if self.world.source_locations[self.world.player][loc_name].get("original_item"):
                    self.world.source_locations[self.world.player][loc_name]["original_item"] = "High-Grade Gunpowder - White"
                
                if self.world.source_locations[self.world.player][loc_name].get("force_item"):
                    self.world.source_locations[self.world.player][loc_name]["force_item"] = "High-Grade Gunpowder - White"

            counter = counter + 1

    #################
    # Private methods for various tasks that each setting might need to do
    #################

    def _determine_starting_weapon(self, level: Optional[str] = None) -> dict:
        weapon_list = self.all_weapons

        if level:
            weapon_list = self.weapons_by_level[level]

        # pick random starting weapon and set for later slot data
        random_weapon = self.random.choice(weapon_list)

        # if the player set a starting weapon option, use that as the choice instead, and raise error if it's an invalid choice
        if self.world.options.starting_weapon.current_key != "default":
            starting_weapon_name = self.world.get_starting_weapon_name_from_option_value()
            weapons_with_name = [w for w in weapon_list if w['name'] == starting_weapon_name]

            if len(weapons_with_name) == 0:
                raise RE2ROptionError("Your 'Starting Weapon' option is not compatible with this weapon rando setting. Please adjust your YAML.")

            random_weapon = weapons_with_name[0]

        self.world.starting_weapon[self.world.player] = random_weapon["name"]
        # starting weapon isn't on a location, so no need to set replacement; but set replacement for ammo
        self.world.replacement_ammo[self.world.player][self.starting_ammo_name] = [random_weapon["ammo"]]

        # remove the starting
        self.all_weapons = [i for i in self.all_weapons if i['name'] != random_weapon['name']]

        for weapon_level in self.weapons_by_level.keys():
            self.weapons_by_level[weapon_level] = [i for i in self.weapons_by_level[weapon_level] if i['name'] != random_weapon['name']]

        return random_weapon

    def _queue_swap(self, old_item: str, new_item: str, item_type: str):
        if old_item not in self.swap_queue.keys():
            self.swap_queue[old_item] = []
        
        self.swap_queue[old_item].append({
            'old_item': old_item,
            'new_item': new_item,
            'item_type': item_type
        })

        old_item = self.world.item_name_to_item.get(old_item, {})

        if old_item.get('type') == 'Weapon':
            self.world.replacement_weapons[self.world.player][old_item['name']] = new_item

        if old_item.get('type') == 'Ammo':
            if old_item['name'] not in self.world.replacement_ammo[self.world.player].keys():
                self.world.replacement_ammo[self.world.player][old_item['name']] = []

            self.world.replacement_ammo[self.world.player][old_item['name']].append(new_item)

    def _swap_queued_at_locations(self):
        # counters to help with cycling through new item replacements for old items (if they have more than one replacement)
        queue_indexes = { k: 0 for k in self.swap_queue.keys() }
        
        self._smooth_ammo_counts() # only changes ammo counts if swap queue includes ammo

        for loc_name, loc in self._get_locations().items():
            # if the location has already been swapped, don't swap it again
            if loc.get('swapped', None) == True:
                continue

            original_item = loc.get("original_item", None)
            original_item = self.world.item_name_to_item.get(original_item, {})
            force_item = loc.get("force_item", None)
            force_item = self.world.item_name_to_item.get(force_item, {})
            swapped = False

            matched_by_force = [v2 for v in self.swap_queue.values() for v2 in v if force_item.get('type') == v2['item_type'] and force_item.get('name', None) == v2['old_item']]

            if not swapped and len(matched_by_force) > 0:
                old_item = matched_by_force[0]['old_item']
                queue_index = queue_indexes[old_item]

                # increment the indexes so we're alternating what replacement gets swapped in
                if queue_index >= len(self.swap_queue[old_item]):
                    queue_index = queue_indexes[old_item] = 0

                loc['force_item'] = matched_by_force[queue_index]['new_item']
                swapped = True
                queue_indexes[old_item] += 1

            matched_by_original = [v2 for v in self.swap_queue.values() for v2 in v if original_item.get('type') == v2['item_type'] and original_item.get('name', None) == v2['old_item']]

            if not swapped and len(matched_by_original) > 0:
                old_item = matched_by_original[0]['old_item']
                queue_index = queue_indexes[old_item]

                # increment the indexes so we're alternating what replacement gets swapped in
                if queue_index >= len(self.swap_queue[old_item]):
                    queue_index = queue_indexes[old_item] = 0
                    
                loc['original_item'] = matched_by_original[queue_index]['new_item']
                swapped = True
                queue_indexes[old_item] += 1

            # if anything was swapped, set the new location back
            if swapped:
                loc['swapped'] = True
                self.world.source_locations[self.world.player][loc_name] = loc
     
    def _smooth_ammo_counts(self):
        # we only want to smooth ammo counts for weapon rando modes that can change the weapon power density
        #   (also, we exclude "troll" and troll adjacent because unfair ammo splits is part of the appeal)
        if self.mode == "starting" or self.mode == "match" or "troll" in self.mode:
            return

        # if we're also swapping ammo, let's check the ammo pools for a stark difference between highest qty and lowest
        #    and, if present, let's smooth over those quantities a bit
        # - For B scenarios, this involves cutting the Large Cal ammo in half and sending the difference to Handgun Ammo
        # - For all other scenarios, identify if there's a qty >=30 and, if so, chop 10 off it and redistribute the 10 randomly between the two lowest categories <10
        ammo_swaps = {k: 0 for k, v in self.swap_queue.items() for v2 in v if v2['item_type'] == 'Ammo'}

        if len(ammo_swaps.keys()):
            if self.scenario.lower() == "b":
                lc_locs = [loc for loc_name, loc in self._get_locations().items() if loc.get('original_item') == "Large-Caliber Handgun Ammo"]
                
                # take half of the LCH ammo locations and change them to regular Handgun ammo
                for x in range(math.floor(len(lc_locs) / 2)):
                    if lc_locs[x].get('original_item'):
                        loc_name = lc_locs[x]['name']
                        lc_locs[x]['original_item'] = 'Handgun Ammo'
                        self.world.source_locations[self.world.player][loc_name] = lc_locs[x]
            else:
                for k in ammo_swaps.keys():
                    ammo_swaps[k] = len([loc for loc_name, loc in self._get_locations().items() if loc.get('original_item') == k])

                # get ammo w/ high counts and with low counts, and cut one high count by 10 and redistribute it between 2 low counts
                high_counts = [k for k, v in ammo_swaps.items() if v >= 30]
                low_counts = [k for k, v in ammo_swaps.items() if v < 10]
                count_in_reserve = 0
                reserve_split = []

                if len(high_counts) > 0:
                    count_in_reserve = 10

                if len(low_counts) > 0:
                    if len(low_counts) >= 2:
                        reserve_split.append(self.world.random.randint(0, 10)) # index 0
                        reserve_split.append(10 - reserve_split[0]) # index 1
                    else:
                        reserve_split = [10, 0]

                if count_in_reserve > 0 and len(reserve_split) > 0:
                    high_count_locs = [loc for loc_name, loc in self._get_locations().items() if loc.get('original_item') == high_counts[0]]

                    for x in range(count_in_reserve):
                        loc_name = f"{high_count_locs[x]['region']} - {high_count_locs[x]['name']}"
                        swapped = False

                        if reserve_split[0] > 0:
                            reserve_split[0] -= 1
                            swapped = True
                            high_count_locs[x]['original_item'] = low_counts[0]
                        elif reserve_split[1] > 0:
                            reserve_split[1] -= 1
                            swapped = True
                            high_count_locs[x]['original_item'] = low_counts[1]
                        
                        if swapped:
                            self.world.source_locations[self.world.player][loc_name] = high_count_locs[x]
         
    def _get_locations(self):
        locs = { k: l for k, l in self.world.source_locations[self.world.player].items() }
        return locs

    def _get_weapons_from_locations(self):
        weapons = []

        for loc in self._get_weapon_locations():
            original_item = loc.get("original_item", None)
            original_item = self.world.item_name_to_item.get(original_item, {})

            if original_item.get("type") == "Weapon" and original_item.get("ammo", None):
                if original_item not in weapons:
                    weapons.append(original_item)

                continue

            force_item = loc.get("force_item", None)
            force_item = self.world.item_name_to_item.get(force_item, {})

            if force_item.get("type") == "Weapon" and force_item.get("ammo", None):
                if force_item not in weapons:
                    weapons.append(force_item)

                continue

        return weapons
    
    def _get_weapon_locations(self):
        locations = []

        for _, loc in self._get_locations().items():
            original_item = loc.get("original_item", None)
            original_item = self.world.item_name_to_item.get(original_item, {})

            if original_item.get("type") == "Weapon" and original_item.get("ammo", None):
                if loc not in locations:
                    locations.append(loc)

                continue

            force_item = loc.get("force_item", None)
            force_item = self.world.item_name_to_item.get(force_item, {})

            if force_item.get("type") == "Weapon" and force_item.get("ammo", None):
                if loc not in locations:
                    locations.append(loc)

                continue

        return locations

    def _get_locations_for_extra_weapons(self) -> list:
        available_locations = []
        locations = list(self._get_locations().values())
        self.random.shuffle(locations)

        for loc in locations:
            # if the location has already been swapped, don't swap it again
            if loc.get('swapped', None) == True:
                continue

            # only use locations that don't have an item forced there and are randomized
            if loc.get('force_item', None) or loc.get('randomized', 1) == 0:
                continue

            if loc.get('original_item', None) in ['Handgun Ammo', 'Wooden Boards', 'Blue Herb']:
                available_locations.append(loc)

        return available_locations
    
    def _get_locations_having(self, item_name: str) -> list:
        return [loc for _, loc in self._get_locations().items() if loc.get('original_item') == item_name]

    def _split_ammo_by_level(self, level: Optional[str] = None):
        levels = self.weapons_by_level.keys()

        if level:
            levels = [level]
        else:
            self.world.replacement_ammo[self.world.player] = {} # if we're splitting all ammo by level, this includes starting, so remove it and anything else

        weapons_at_locations = [self.world.item_name_to_item.get(w.get('name')) for w in self._get_weapons_from_locations()]
        weapons_at_locations = [w for w in weapons_at_locations if w.get('name') in self.world.replacement_weapons[self.world.player].values()]
        starting_weapon = self.world.item_name_to_item.get(self.world.starting_weapon[self.world.player])
        weapons_at_locations.append(starting_weapon)

        placed_weapons_by_level = {
            'light': [w for w in weapons_at_locations if 'light_gun' in w['groups']],
            'medium': [w for w in weapons_at_locations if 'medium_gun' in w['groups']],
            'heavy': [w for w in weapons_at_locations if 'heavy_gun' in w['groups']]
        }
        needed_ammo_by_level = {
            'light': [],
            'medium': [],
            'heavy': []
        }
        placed_ammo_by_level = {
            'light': [],
            'medium': [],
            'heavy': []
        }
        
        for level, weapons in placed_weapons_by_level.items():
            for weapon in weapons:
                needed_ammo_by_level[level].append(weapon['ammo'])
                placed_ammo_by_level[level].extend([l for l in self._get_locations_having(weapon['ammo']) if l not in placed_ammo_by_level[level]])

            # de-dupe the ammo
            needed_ammo_by_level[level] = list(set(needed_ammo_by_level[level]))

        # if medium is included, fix the medium locations to not include locations from heavy and not include light ammo locations
        if 'medium' in levels:
            placed_ammo_by_level['medium'] = [
                l for l in placed_ammo_by_level['medium'] 
                    if l not in placed_ammo_by_level['heavy'] 
                        and l.get('original_item') not in ['Handgun Ammo', 'Large-Caliber Handgun Ammo']
            ]

        # if light is included, fix the light locations to not include locations from medium or heavy
        if 'light' in levels:
            placed_ammo_by_level['light'] = [
                l for l in placed_ammo_by_level['light'] 
                    if l not in placed_ammo_by_level['medium'] and l not in placed_ammo_by_level['heavy']
            ]

        for lev in levels:
            # take the amount of locations with ammo and divide by the number of ammo types, rounding down
            level_total = len(needed_ammo_by_level[lev])
            each_amount = math.floor(len(placed_ammo_by_level[lev]) / level_total)
            count = 0

            # loop over all the placed ammo, and update it to the correct ammo split based on the count
            # 0 to count is first ammo, count to count x 2 is second, etc. Last one might get extra because rounded down.
            for loc in placed_ammo_by_level[lev]:
                index = math.floor(count / each_amount)

                if index + 1 >= level_total:
                    index = level_total - 1

                loc['original_item'] = needed_ammo_by_level[lev][index]
                loc_key = self._get_location_key(loc['region'], loc['name'])
                self.world.source_locations[self.world.player][loc_key] = loc

                count += 1

            self.world.replacement_ammo[self.world.player]["{} Weapon Ammo".format(lev.title())] = needed_ammo_by_level[lev]

    def _split_ammo_randomly(self):
        self.world.replacement_ammo[self.world.player] = {} # all ammo is completely random, so skip starting listing(s) too

        placed_weapons = [self.world.item_name_to_item.get(w.get('name')) for w in self._get_weapons_from_locations()]
        starting_weapon = self.world.item_name_to_item.get(self.world.starting_weapon[self.world.player])
        placed_weapons.append(starting_weapon)

        needed_ammo = []
        placed_ammo = []
        
        for weapon in placed_weapons:
            needed_ammo.append(weapon['ammo'])

        for weapon in self.all_weapons:
            placed_ammo.extend(self._get_locations_having(weapon['ammo']))

        # de-dupe the ammo list
        needed_ammo = list(set(needed_ammo))
        forced_minimum_ammo = [*needed_ammo]
        more_minimum_ammo = [*needed_ammo] * 3

        # loop over all the placed ammo, and update it to a completely random ammo choice
        for loc in placed_ammo:
            if len(forced_minimum_ammo) > 0: # first, guaranteed a single pack of every ammo type
                loc['original_item'] = forced_minimum_ammo.pop()
            elif len(more_minimum_ammo) > len(needed_ammo): # ... then, have a chance to roll up to 3 more of any pack
                loc['original_item'] = more_minimum_ammo.pop()
            else: # ... then, just pick randomly
                loc['original_item'] = self.random.choice(needed_ammo)
            
            loc_key = self._get_location_key(loc['region'], loc['name'])
            self.world.source_locations[self.world.player][loc_key] = loc

        self.world.replacement_ammo[self.world.player]["Random Quantities"] = needed_ammo

    def _get_location_key(self, *location_parts):
        return " - ".join(location_parts)

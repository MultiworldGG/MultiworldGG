import re
import typing

from typing import Dict, Any, TextIO
from Utils import visualize_regions

from BaseClasses import ItemClassification, Item, Location, Region, CollectionState, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from ..generic.Rules import set_rule
from Fill import fill_restrictive

from .Data import Data
from .Exceptions import RE2ROptionError
from .Options import RE2ROptions
from .WeaponRandomizer import WeaponRandomizer


Data.load_data('leon', 'a')
Data.load_data('leon', 'b')
Data.load_data('claire', 'a')
Data.load_data('claire', 'b')


class RE2RLocation(Location):
    def stack_names(*area_names):
        return " - ".join(area_names)
    
    def stack_names_not_victory(*area_names):
        if area_names[-1] == "Victory": return area_names[-1]

        return RE2RLocation.stack_names(*area_names)

    def is_item_forbidden(item, location_data, current_item_rule):
        return current_item_rule(item) and ('forbid_item' not in location_data or item.name not in location_data['forbid_item'])

class ResidentEvil2RemakeWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the RE2 Remake Randomizer for MultiworldGG multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["Fuzzy"]
        )
    ]

class ResidentEvil2Remake(World):
    """
    'Leon, I am your father.' - Billy Birkin, probably
    """
    game: str = "Resident Evil 2 Remake"
    author: str = "Fuzzy"
    web = ResidentEvil2RemakeWeb()

    data_version = 2
    required_client_version = (0, 5, 0)
    apworld_release_version = "0.3.3" # defined to show in spoiler log

    item_id_to_name = { item['id']: item['name'] for item in Data.item_table }
    item_name_to_id = { item['name']: item['id'] for item in Data.item_table }
    item_name_to_item = { item['name']: item for item in Data.item_table }
    location_id_to_name = { loc['id']: RE2RLocation.stack_names(loc['region'], loc['name']) for loc in Data.location_table + Data.enemy_table }
    location_name_to_id = { RE2RLocation.stack_names(loc['region'], loc['name']): loc['id'] for loc in Data.location_table + Data.enemy_table }
    location_name_to_location = { RE2RLocation.stack_names(loc['region'], loc['name']): loc for loc in Data.location_table + Data.enemy_table }
    source_locations = {} # this is used to seed the initial item pool from original items, and is indexed by player as lname:loc locations

    # de-dupe the item names for the item group name
    item_name_groups = { key: set(values) for key, values in Data.item_name_groups.items() }

    # keep track of the weapon randomizer settings for use in various steps and in slot data
    starting_weapon = {}
    replacement_weapons = {}
    replacement_ammo = {}

    options_dataclass = RE2ROptions
    options: RE2ROptions

    def generate_early(self): # check weapon randomization before locations and items are processed, so we can swap non-randomized items as well
        # check for option values that UT passed via storing from slot data, and set our options to match if present
        for key, val in getattr(self.multiworld, 're_gen_passthrough', {}).get(self.game, {}).items():
            # gets the int val from the string option value name, then sets
            getattr(self.options, key).value = getattr(self.options, key).options[val]

        # if the enemy kills as locations option is enabled for a scenario that doesn't support it yet, throw an error
        if self._enemy_kill_rando() and not self._can_enemy_kill_rando():
            raise RE2ROptionError("The Enemy Kills as Locations option is only currently supported for Leon's A (1st) scenario on Assisted / Standard difficulty.")
            return

        # start with the normal locations per player for pool, then overwrite with weapon rando if needed
        self.source_locations[self.player] = self._get_locations_for_scenario(self._get_character(), self._get_scenario()) # id:loc combo
        self.source_locations[self.player] = { 
            RE2RLocation.stack_names(l['region'], l['name']): { **l, 'id': i } 
                for i, l in self.source_locations[self.player].items() 
        } # turn it into name:loc instead

        if self._enemy_kill_rando():
            # since enemy kills don't give items themselves, create a drop table of 
            # combat-related items to add to the pool for these locations
            enemy_kill_items = self._format_option_text(self.options.enemy_kill_items).lower()

            if enemy_kill_items == "Trash":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if i.get('type', 'None') in ['Lore'] or 'Trophy' in i['name'] 
                ]   
            elif enemy_kill_items == "Healing":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if i.get('type', 'None') in ['Recovery'] 
                ]
            elif enemy_kill_items == "Gunpowder":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if 'Gunpowder' in i['name'] 
                ]
            elif enemy_kill_items == "Ammo":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if i.get('type', 'None') in ['Ammo'] 
                ]
            elif enemy_kill_items == "Ammo Related":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if i.get('type', 'None') in ['Ammo'] or 'Gunpowder' in i['name'] 
                ]
            elif enemy_kill_items == "All Weapon Related":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if i.get('type', 'None') in ['Ammo', 'Subweapon'] or 'Gunpowder' in i['name'] 
                ]
            else: # == "Mixed"
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table if i.get('type', 'None') in ['Recovery', 'Ammo', 'Subweapon'] or 'Gunpowder' in i['name'] 
                ]   

            # get the list of viable items from the list of items currently on the scenario's locations
            enemy_kill_drop_names = list(set([
                l['original_item'] for l in self.source_locations[self.player].values() if l.get('original_item', 'None') in enemy_kill_valid_drops
            ]))
            enemy_kill_drops = []

            for x in range(len(Data.enemy_table)):
                drop_name = enemy_kill_drop_names[x % len(enemy_kill_drop_names)]
                enemy_kill_drops.append(drop_name)

            # replace placeholders for enemy kills with the chosen distribution of items
            for name, loc in self.source_locations[self.player].items():
                if loc.get('original_item') == "__Enemy Kill Drop Placeholder__":
                    loc['original_item'] = enemy_kill_drops.pop(0)

        weapon_rando = self._format_option_text(self.options.cross_scenario_weapons).lower()

        # if any of the "Oops! All X" weapon options are present, don't bother with weapon randomization since they'll all get overwritten
        #    and since starting with pistol is important to prevent softlock at Gator with all knives
        if self._get_oops_all_options_flag():
            if weapon_rando != "none":
                raise RE2ROptionError("Cannot apply 'Oops All' options alongside Cross Scenario Weapons. Please fix your yaml.")
            
            # also check for starting weapon option, which is incompatible with Oops! options
            if self.options.starting_weapon.current_key != "default":
                raise RE2ROptionError("Cannot apply 'Starting Weapon' options alongside 'Oops All' options. Please fix your yaml.")

            # also check for double weapons, which is incompatible with Oops! options
            if self._format_option_text(self.options.double_weapons) == 'True':
                raise RE2ROptionError("Cannot use 'Double Weapons' option alongside 'Oops All' options. Please fix your yaml.")

            return

        weapon_rando = self._format_option_text(self.options.cross_scenario_weapons).lower()

        # if the user didn't pick any weapon randomization, skip all of this
        if weapon_rando == "none":
            # if not using weapon rando (which handles its own starting weapon), set the starting weapon here
            if self.options.starting_weapon.current_key != "default":
                self.starting_weapon[self.player] = self.get_starting_weapon_name_from_option_value()

            return

        weapon_randomizer = WeaponRandomizer(self, self._get_character(), self._get_scenario())
        
        # if only randomizing the starting weapon, replace it and all of its ammo
        if weapon_rando == "starting": 
            weapon_randomizer.starting()
        elif weapon_rando == "match": 
            weapon_randomizer.match()
        elif weapon_rando == "full": 
            weapon_randomizer.full()
        elif weapon_rando == "all": 
            weapon_randomizer.all()
        elif weapon_rando == "full ammo": 
            weapon_randomizer.full_ammo()
        # all ammo and troll are identical, except there's a step after upgrades are placed for all weapons to remove all but a few weapons
        # so just do all_ammo here, then call the actual troll option after upgrades + gunpowder + whatever else
        elif weapon_rando == "all ammo" or weapon_rando == "troll" or weapon_rando == "troll starting": 
            if weapon_rando == "all ammo": weapon_randomizer.all_ammo()
            else: weapon_randomizer.all_ammo_troll()
        else:
            raise RE2ROptionError("Invalid weapon randomizer value!")

        weapon_randomizer.upgrades() # always swap upgrades after weapons are rando'd
        weapon_randomizer.high_grade_gunpowder() # always split high-grade gunpowder after weapons are rando'd

        if weapon_rando == "troll":
            weapon_randomizer.troll()
        if weapon_rando == "troll starting":
            weapon_randomizer.troll_starting()

    def create_regions(self): # and create locations
        scenario_locations = { l['id']: l for _, l in self.source_locations[self.player].items() }
        scenario_regions = self._get_region_table_for_scenario(self._get_character(), self._get_scenario())

        # used below if killsanity is on
        has_fire_weapon = False
        fire_weapons = ['GM 79', 'Chemical Flamethrower']

        if self._format_option_text(self.options.oops_all_rockets) == 'True':
            has_fire_weapon = True
        elif self._get_starting_weapon() in fire_weapons:
            has_fire_weapon = True
        else: # check the remaining weapons
            has_fire_weapon = len([
                location['original_item'] 
                    for _, location in scenario_locations.items() if location.get('original_item') in fire_weapons
            ]) > 0

        regions = [
            Region(region['name'], self.player, self.multiworld) 
                for region in scenario_regions
        ]
        
        for region in regions:
            region.locations = [
                RE2RLocation(self.player, RE2RLocation.stack_names_not_victory(region.name, location['name']), location['id'], region) 
                    for _, location in scenario_locations.items() if location['region'] == region.name
            ]
            region_data = [scenario_region for scenario_region in scenario_regions if scenario_region['name'] == region.name][0]
            
            for location in region.locations:
                location_data = scenario_locations[location.address]
                
                # if location has an item that should be forced there, place that. for cases where the item to place differs from the original.
                if 'force_item' in location_data and location_data['force_item']:
                    location.place_locked_item(self.create_item(location_data['force_item']))
                # if location is marked not rando'd, place its original item. 
                # if/elif here allows force_item + randomized=0, since a forced item is technically not randomized, but don't need to trigger both.
                elif 'randomized' in location_data and location_data['randomized'] == 0:
                    location.place_locked_item(self.create_item(location_data["original_item"]))
                # if location is not force_item'd or not not randomized, check for Labs progression option and apply
                # since Labs progression option doesn't matter for force_item'd or not randomized locations
                # we check for zone id > 3 because 3 is typically Sewers, and anything beyond that is Labs / endgame stuff
                elif self._format_option_text(self.options.allow_progression_in_labs) == 'False' and region_data['zone_id'] > 3:
                    location.item_rule = lambda item: not item.advancement
                elif self._format_option_text(self.options.allow_progression_in_labs) == 'True' and re.match(r'^Treatment Pool Room \(\w+?\) - Cable Car Table$', location.name):
                    location.place_locked_item(self.create_item("Sewers Key"))
                # END if

                # if the player doesn't have a fire weapon or rocket launchers in their item pool, make all Ivy enemy drops give filler / be useless
                if self._enemy_kill_rando() and "Ivy" in location.name and not has_fire_weapon:
                    location.progress_type = LocationProgressType.EXCLUDED
                    location.place_locked_item(self.create_item("Pink Scissors"))

                if 'forbid_item' in location_data and location_data['forbid_item']:
                    current_item_rule = location.item_rule or None

                    if not current_item_rule:
                        current_item_rule = lambda x: True

                    location.item_rule = lambda item, loc_data=location_data, cur_rule=current_item_rule: RE2RLocation.is_item_forbidden(item, loc_data, cur_rule)

                # now, set rules for the location access
                if "condition" in location_data and "items" in location_data["condition"]:
                    set_rule(location, lambda state, loc=location, loc_data=location_data: self._has_items(state, loc_data["condition"].get("items", [])))

            self.multiworld.regions.append(region)
                
        for connect in self._get_region_connection_table_for_scenario(self._get_character(), self._get_scenario()):
            # skip connecting on a one-sided connection because this should not be reachable backwards (and should be reachable otherwise)
            if 'limitation' in connect and connect['limitation'] in ['ONE_SIDED_DOOR']:
                continue

            from_name = connect['from'] if 'Menu' not in connect['from'] else 'Menu'
            to_name = connect['to'] if 'Menu' not in connect['to'] else 'Menu'

            region_from = self.multiworld.get_region(from_name, self.player)
            region_to = self.multiworld.get_region(to_name, self.player)
            ent = region_from.connect(region_to)

            if "condition" in connect and "items" in connect["condition"]:
                set_rule(ent, lambda state, en=ent, conn=connect: self._has_items(state, conn["condition"].get("items", [])))

        # Uncomment the below to see a connection of the regions (and their locations) for any scenarios you're testing.
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "region_uml")

        # Place victory and set the completion condition for having victory
        self.multiworld.get_location("Victory", self.player) \
            .place_locked_item(self.create_item("Victory"))

        self.multiworld.completion_condition[self.player] = lambda state: self._has_items(state, ['Victory'])

    def create_items(self):
        scenario_locations = self.source_locations[self.player]

        pool = [
            self.create_item(item['name'] if item else None) for item in [
                self.item_name_to_item[location['original_item']] if location.get('original_item') else None
                    for _, location in scenario_locations.items()
            ]
        ]

        # print([location['name'] + ' | ' + location.get('original_item', 'None') for _, location in scenario_locations.items()])

        pool = [item for item in pool if item is not None] # some of the locations might not have an original item, so might not create an item for the pool

        # if there's a starting weapon option set, remove the starting weapon from the pool and replace it with its ammo
        if self.options.starting_weapon.current_key != "default":
            starting_weapon_name = self.get_starting_weapon_name_from_option_value()
            starting_weapon_ammo = [item['ammo'] for item in self.item_name_to_item.values() if item['name'] == starting_weapon_name][0]

            # replace every instance of the weapon we started with (in the item pool) with its ammo
            pool = [item if item.name != starting_weapon_name else self.create_item(starting_weapon_ammo) for item in pool]

        # remove any already-placed items from the pool (forced items, etc.)
        for filled_location in self.multiworld.get_filled_locations(self.player):
            if filled_location.item.code and filled_location.item in pool: # not id... not address... "code"
                pool.remove(filled_location.item)

        # check the starting hip pouches option and add as precollected, removing from pool and replacing with junk
        starting_hip_pouches = int(self.options.starting_hip_pouches)

        if starting_hip_pouches > 0:
            hip_pouches = [item for item in pool if item.name == 'Hip Pouch'] # 6 total in every campaign, I think

            # if the hip pouches option exceeds the number of hip pouches in the pool, reduce it to the number in the pool
            if starting_hip_pouches > len(hip_pouches):
                starting_hip_pouches = len(hip_pouches)
                self.options.starting_hip_pouches.value = len(hip_pouches)

            for x in range(starting_hip_pouches):
                self.multiworld.push_precollected(hip_pouches[x]) # starting inv
                pool.remove(hip_pouches[x])

        # check the starting ink ribbons option and add as precollected, removing from pool and replacing with junk
        starting_ink_ribbons = int(self.options.starting_ink_ribbons)

        if self._format_option_text(self.options.difficulty) == 'Hardcore' and starting_ink_ribbons > 0:
            ink_ribbons = [item for item in pool if item.name == 'Ink Ribbon'] # 12+ total in every campaign, I think

            # if the ink ribbons option exceeds the number of ink ribbons in the pool, reduce it to the number in the pool
            if starting_ink_ribbons > len(ink_ribbons):
                starting_ink_ribbons = len(ink_ribbons)
                self.options.starting_ink_ribbons.value = len(ink_ribbons)

            for x in range(starting_ink_ribbons):
                self.multiworld.push_precollected(ink_ribbons[x]) # starting inv
                pool.remove(ink_ribbons[x])

        # check the bonus start option and add some heal items and ammo packs as precollected / starting items
        if self._format_option_text(self.options.bonus_start) == 'True':
            count_spray = 3
            count_ammo = 4
            count_grenades = 3
            count_bangs = 3

            for x in range(count_spray): self.multiworld.push_precollected(self.create_item('First Aid Spray'))

            if self.player in self.starting_weapon:
                starting_weapon = self.starting_weapon[self.player]
                starting_weapon_ammo = self.item_name_to_item[starting_weapon].get('ammo')
                for x in range(count_ammo): self.multiworld.push_precollected(self.create_item(starting_weapon_ammo))
            else:
                for x in range(count_ammo): self.multiworld.push_precollected(self.create_item('Handgun Ammo'))

            for x in range(count_grenades): self.multiworld.push_precollected(self.create_item('Hand Grenade'))
            for x in range(count_bangs): self.multiworld.push_precollected(self.create_item('Flash Grenade'))

        # do all the "no X" options here so we have more empty spots to use for traps, if needed
        if self._format_option_text(self.options.no_first_aid_spray) == 'True':
            pool = self._replace_pool_item_with(pool, 'First Aid Spray', 'Wooden Boards')

        if self._format_option_text(self.options.no_green_herb) == 'True':
            pool = self._replace_pool_item_with(pool, 'Green Herb', 'Wooden Boards')

        if self._format_option_text(self.options.no_red_herb) == 'True':
            pool = self._replace_pool_item_with(pool, 'Red Herb', 'Wooden Boards')
        
        if self._format_option_text(self.options.no_gunpowder) == 'True':
            replaceables = set(item.name for item in pool if 'Gunpowder' in item.name)
            less_useful_items = set(
                item.name for item in pool 
                    if 'Boards' in item.name or 'Cassette' in item.name or ('Film' in item.name and 'Hiding Place' not in item.name) or item.name == 'Blue Herb'
            )

            for from_item in replaceables:
                to_item = self.random.choice(list(less_useful_items))
                pool = self._replace_pool_item_with(pool, from_item, to_item)

        # figure out which traps are enabled, then swap them in for low-priority items
        # do this before the "oops all X" options so we can make use of extra Handgun Ammo spots before they get replaced out
        traps = []

        if self._format_option_text(self.options.add_damage_traps) == 'True':
            for x in range(int(self.options.damage_trap_count)):
                traps.append(self.create_item("Damage Trap"))

        if self._format_option_text(self.options.add_poison_traps) == 'True':
            for x in range(int(self.options.poison_trap_count)):
                traps.append(self.create_item("Poison Trap"))

        if len(traps) > 0:
            # use these spots for replacement first, since they're entirely non-essential
            available_spots = [
                item for item in pool 
                    if 'Boards' in item.name or 'Cassette' in item.name or ('Film' in item.name and 'Hiding Place' not in item.name)
            ]
            self.random.shuffle(available_spots)

            # use these spots for replacement next, since they're lower priority but we don't want to use as many of them
            # for gunpowder, only target the small / normal gunpowders
            extra_spots = [
                item for item in pool 
                    if 'Handgun Ammo' in item.name or item.name == 'Gunpowder'
            ]
            self.random.shuffle(extra_spots)
               
            for spot in available_spots:
                if len(traps) == 0: break

                trap_to_place = traps.pop()
                pool.remove(spot)
                pool.append(trap_to_place)
                
            for spot in extra_spots:
                if len(traps) == 0: break

                trap_to_place = traps.pop()
                pool.remove(spot)
                pool.append(trap_to_place)

        # add extras for Clock Tower items or Medallions, if configured
        # doing this before "oops all X" to make use of extra Handgun Ammo spots, too
        if self._format_option_text(self.options.extra_clock_tower_items) == 'True':
            replaceables = [
                item for item in pool if 
                    'Boards' in item.name or item.name == 'Handgun Ammo' or item.name == 'Large-Caliber Handgun Ammo' or item.name == "Gunpowder" or 
                    item.name == "Damage Trap" or item.name == "Poison Trap"
            ]
            
            for x in range(3):
                if len(replaceables) == 0: break
                pool.remove(replaceables.pop())

            pool.append(self.create_item('Mechanic Jack Handle'))
            pool.append(self.create_item('Small Gear'))
            pool.append(self.create_item('Large Gear'))

        if self._format_option_text(self.options.extra_medallions) == 'True':
            replaceables = replaceables = [
                item for item in pool if 
                    'Boards' in item.name or item.name == 'Handgun Ammo' or item.name == 'Large-Caliber Handgun Ammo' or item.name == "Gunpowder" or 
                    item.name == "Damage Trap" or item.name == "Poison Trap"
            ]       

            for x in range(2):
                if len(replaceables) == 0: break
                pool.remove(replaceables.pop())

            pool.append(self.create_item('Lion Medallion'))
            pool.append(self.create_item('Unicorn Medallion'))

            # The A scenarios have Maiden forced to the Bolt Cutters vanilla location, which is guaranteed to be accessible.
            # B scenarios have it randomized, so add a second randomized Maiden.
            if self._get_scenario().lower() == 'b':
                if len(replaceables) > 0:
                    pool.remove(replaceables.pop()) # remove the 3rd item to make room for a 3rd medallion

                pool.append(self.create_item('Maiden Medallion'))

        if self._format_option_text(self.options.early_medallions) == 'True':
            medallions = {i.name: len([i2 for i2 in pool if i2.name == i.name]) for i in pool if i.name in ['Lion Medallion', 'Unicorn Medallion', 'Maiden Medallion']}

            for item_name, item_qty in medallions.items():
                if item_qty > 0:
                    self.multiworld.early_items[self.player][item_name] = item_qty
   

        # check the "Oops! All ____" option. From the option description:
        #     Enabling this swaps all weapons, weapon ammo, and subweapons to the selected weapon. 
        #     (Except progression weapons, of course.)
        oops_all_flag = self._get_oops_all_options_flag()
        if oops_all_flag:            
            oops_items_map = {
                0x01: 'Single Use Rocket',
                0x02: 'Mini-Minigun',
                0x04: 'Hand Grenade',
                0x08: 'Combat Knife'
            }

            if oops_all_flag not in oops_items_map:
                raise RE2ROptionError("Cannot apply multiple 'Oops All' options. Please fix your yaml.")

            replacement_types = ['Weapon', 'Subweapon', 'Ammo']

            if self._enemy_kill_rando(): # if enemy kill rando, just replace gunpowder with the Oops weapon; players will need more firepower
                replacement_types.append('Gunpowder')
            else: # otherwise, we don't want the player to have gunpowder for bullets to make Oops options more thematic, so we swap them to random filler
                replacements = [
                    ['Picture Block', 'Stuffed Doll', 'Pink Scissors', 'Gas Station Key'], # variety of filter items, exclusive to Oops for now
                    ['Handgun Ammo', 'Flash Grenade'], # a few more useful replacements for the limited larges
                    ['Green Herb', 'Blue Herb', 'Wooden Boards'] # some okay non-filler replacements for yellows/whites
                ]

                for from_item in [item for item in self.item_name_to_item.values() if item.get('type') == 'Gunpowder']:
                    if "Yellow" in from_item['name'] or "White" in from_item['name']:
                        pool = self._replace_pool_item_with(pool, from_item['name'], self.random.choice(replacements[2]))
                    elif "Large" in from_item['name']:
                        pool = self._replace_pool_item_with(pool, from_item['name'], self.random.choice(replacements[1]))
                    else: # just plain Gunpowder
                        pool = self._replace_pool_item_with(pool, from_item['name'], self.random.choice(replacements[0]))

            # Leave the Anti-Tank Rocket on Tyrant alone so the player can finish the fight
            items_to_replace = [
                item for item in self.item_name_to_item.values() 
                if item.get('type') in replacement_types and item['name'] != 'Anti-tank Rocket'
            ]

            for from_item in items_to_replace:
                pool = self._replace_pool_item_with(pool, from_item['name'], oops_items_map[oops_all_flag])

            # Add Marvin's Knife back in. He gets cranky if you don't give him his knife.
            for item in pool:
                if item.name == oops_items_map[oops_all_flag]:
                    pool.remove(item)
                    pool.append(self.create_item("Combat Knife"))
                    break


        # if the number of unfilled locations exceeds the count of the pool, fill the remainder of the pool with extra maybe helpful items
        missing_item_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)

        if missing_item_count > 0:
            for x in range(missing_item_count):
                pool.append(self.create_item('Blue Herb'))

        # Make any items that result in a really quick BK either early or local items, so the BK time is reduced
        early_items = {}       

        # hardcore no longer removes the main hall shutter, so force bolt cutters early to prevent softlock
        if self._get_difficulty() == "hardcore":
            early_items["Bolt Cutters"] = 1 

        for item_name, item_qty in early_items.items():
            if item_qty > 0:
                self.multiworld.early_items[self.player][item_name] = item_qty

        all_weapon_names = [
            item['name'] for item in self.item_name_to_item.values() 
                if item.get('type') == "Weapon"
        ]

        local_items = {}       
        local_items["Fuse - Main Hall"] = len([i for i in pool if i.name == "Fuse - Main Hall"])

        if self._format_option_text(self.options.local_weapons) == 'True':
            for weapon_name in all_weapon_names:
                count = len([i for i in pool if i.name == weapon_name])

                if count:
                    local_items[weapon_name] = count

        for item_name, item_qty in local_items.items():
            if item_qty > 0:
                self.options.local_items.value.add(item_name)

        # if double weapons is on, add copies in the place of less useful items
        if self._format_option_text(self.options.double_weapons) == 'True':
            for weapon_name in all_weapon_names:            
                count = len([i for i in pool if i.name == weapon_name])

                # if the weapon isn't in the pool at all, or already has a duplicate, skip it
                if not count or count > 1:
                    continue

                eligible_items = [i for i in pool if i.classification == ItemClassification.filler]

                if len(eligible_items) == 0:
                    eligible_items = [i for i in pool if i.name in ["Wooden Boards", "Blue Herb", "Gunpowder"]]

                if len(eligible_items) == 0:
                    eligible_items = [i for i in pool if i.name in ["Handgun Ammo"]]

                if len(eligible_items) == 0: break # no more items to replace out, give up

                pool.append(self.create_item(weapon_name))
                pool.remove(eligible_items[0])

        # Check the item count against the location count, and remove items until they match
        extra_items = len(pool) - len(self.multiworld.get_unfilled_locations(self.player))

        for _ in range(extra_items):
            eligible_items = [i for i in pool if i.classification == ItemClassification.filler]

            if len(eligible_items) == 0:
                eligible_items = [i for i in pool if i.name in ["Wooden Boards", "Blue Herb", "Gunpowder"]]

            if len(eligible_items) == 0:
                eligible_items = [i for i in pool if i.name in ["Handgun Ammo"]]

            if len(eligible_items) == 0: break # no items to remove to match, give up

            pool.remove(eligible_items[0])

        # if enemy kills are added to the locations, remove all Wooden Boards so that players don't prevent themselves from killing window vaulting enemies
        if self._enemy_kill_rando():
            if self._get_oops_all_options_flag():
                pool = self._replace_pool_item_with(pool, "Wooden Boards", "Blue Herb") # enemy kill rando removes all gunpowder with Oops, so use a different replacement
            else:
                pool = self._replace_pool_item_with(pool, "Wooden Boards", "Gunpowder")

        self.multiworld.itempool += pool
            
    def create_item(self, item_name: str) -> Item:
        if not item_name: return

        item = self.item_name_to_item[item_name]

        if item.get('progression', False):
            classification = ItemClassification.progression
        elif item.get('type', None) not in ['Lore', 'Filler', 'Trap']:
            classification = ItemClassification.useful
        elif item.get('type', None) == 'Trap':
            classification = ItemClassification.trap
        else: # it's Lore/Filler
            classification = ItemClassification.filler

        new_item = Item(item['name'], classification, item['id'], player=self.player)
        return new_item

    def get_filler_item_name(self) -> str:
        return "Wooden Boards"

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "apworld_version": self.apworld_release_version,
            "character": self._get_character(),
            "scenario": self._get_scenario(),
            "difficulty": self._get_difficulty(),
            "unlocked_typewriters": self._format_option_text(self.options.unlocked_typewriters).split(", "),
            "weapon_rando": self._format_option_text(self.options.cross_scenario_weapons),
            "starting_weapon": self._get_starting_weapon(),
            "all_weapons": self._get_all_weapons(),
            "ammo_pack_modifier": self._format_option_text(self.options.ammo_pack_modifier),
            "damage_traps_can_kill": self._format_option_text(self.options.damage_traps_can_kill) == 'True',
            "death_link": self._format_option_text(self.options.death_link) == 'Yes' # why is this yes? lol
        }

        return slot_data
    
    # called by UT to pass slot data into the world dupe it's trying to generate, so you can make the options match for gen
    #     (if you return anything from this, UT will put it in self.multiworld.re_gen_passthrough[<game name>] for the single player that is running UT)
    def interpret_slot_data(self, slot_data: dict[str, Any]):
        if not slot_data:
            return False

        regen_values: dict[str, Any] = {}

        # below are the only options that affect logic during generation
        #    comparing and only sending what's different breaks with YAML random, so always just regen with the slot data
        regen_values['character'] = slot_data.get('character') or self._get_character()
        regen_values['scenario'] = slot_data.get('scenario') or self._get_scenario()
        regen_values['difficulty'] = slot_data.get('difficulty') or self._get_difficulty()

        return regen_values

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"RE2R_AP_World version: {self.apworld_release_version}\n")

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # if weapons were randomized across scenarios, list what was swapped for what here (excluding upgrades, because who cares)
        if self._format_option_text(self.options.cross_scenario_weapons) != "None":
            starting_weapon = self.starting_weapon[self.player]
            spoiler_handle.write(f"\n\nWeapon Swaps ({self.multiworld.player_name[self.player]}):\n")
            spoiler_handle.write(f"\n{'(Starting Weapon)'.ljust(30, ' ')} -> {starting_weapon}")

            for from_weapon, to_weapon in self.replacement_weapons[self.player].items():
                # if the from weapon is a placeholder string of underscores, all of these were added (no "old" weapon)
                if re.match('^[_]+$', from_weapon):
                    from_weapon = '(Added)'

                if isinstance(to_weapon, list):
                    if not to_weapon:
                        spoiler_handle.write(f"\n{from_weapon.ljust(30, ' ')} -> :(")
                        continue

                    spoiler_handle.write(f"\n{from_weapon.ljust(30, ' ')} -> {to_weapon[0]}")

                    if len(to_weapon) > 1:
                        for weapon in to_weapon[1:]:
                            spoiler_handle.write(f"\n{''.ljust(30, ' ')} -> {weapon}")
                else:
                    spoiler_handle.write(f"\n{from_weapon.ljust(30, ' ')} -> {to_weapon}")
            
            spoiler_handle.write(f"\n\nAmmo Swaps ({self.multiworld.player_name[self.player]}):\n")

            for from_ammo, to_ammo in self.replacement_ammo[self.player].items():
                ammo_set = list(set(to_ammo))
                ammo_count = len([l for _, l in self.source_locations[self.player].items() if l.get('original_item', None) == ammo_set[0]])                    

                spoiler_handle.write(f"\n{from_ammo.ljust(30, ' ')} -> {ammo_set[0]} ({ammo_count})")

                if len(ammo_set) > 1:
                    for ammo in ammo_set[1:]:
                        ammo_count = len([l for _, l in self.source_locations[self.player].items() if l.get('original_item', None) == ammo])                    
                        spoiler_handle.write(f"\n{''.ljust(30, ' ')} -> {ammo} ({ammo_count})")

            spoiler_handle.write("\n\n(Ammo totals are for the whole campaign, not per swap/category.)")
        elif self.options.starting_weapon.current_key != "default":
            starting_weapon = self.starting_weapon[self.player]
            spoiler_handle.write(f"\n\nStarting Weapon ({self.multiworld.player_name[self.player]}): {starting_weapon}\n")

    def _has_items(self, state: CollectionState, item_names: list) -> bool:
        # if there are no item requirements, this location is open, they "have the items needed"
        if len(item_names) == 0:
            return True

        # if the requirements are a single set of items, make it a list of a single set of items to support looping for multiple sets (below)
        if len(item_names) > 0 and type(item_names[0]) is not list:
            item_names = [item_names]

        for set_of_requirements in item_names:
            # if it requires all unique items, just do a state has all
            if len(set(set_of_requirements)) == len(set_of_requirements):
                if state.has_all(set_of_requirements, self.player):
                    return True
            # else, it requires some duplicates, so let's group them up and do some has w/ counts
            else:
                item_counts = {
                    item_name: len([i for i in set_of_requirements if i == item_name]) for item_name in set_of_requirements # e.g., { Spare Key: 2 }
                }
                missing_an_item = False

                for item_name, count in item_counts.items():
                    if not state.has(item_name, self.player, count):
                        missing_an_item = True

                if missing_an_item:
                    continue # didn't meet these requirements, so skip to the next set, if any
                
                # if we made it here, state has all the items and the quantities needed, return True
                return True

        # if we made it here, state didn't have enough to return True, so return False
        return False

    def _format_option_text(self, option) -> str:
        return re.sub(r'\w+\(', '', str(option)).rstrip(')')
    
    def _get_locations_for_scenario(self, character, scenario) -> dict:
        locations_pool = {
            loc['id']: loc for loc in Data.location_table
                if loc['character'] == character and loc['scenario'] == scenario
        }

        if self._enemy_kill_rando():
            locations_pool.update({
                enemy['id']: enemy for enemy in Data.enemy_table
                    if enemy['character'] == character and enemy['scenario'] == scenario
            })

        # if the player chose hardcore, take out any matching standard difficulty locations
        if self._format_option_text(self.options.difficulty) == 'Hardcore':
            for hardcore_loc in [loc for loc in locations_pool.values() if loc['difficulty'] == 'hardcore']:
                check_loc_region = re.sub(r'H\)$', ')', hardcore_loc['region']) # take the Hardcore off the region name
                check_loc_name = hardcore_loc['name']

                # if there's a standard location with matching name and region, it's obsoleted in hardcore, remove it
                standard_locs = [id for id, loc in locations_pool.items() if loc['region'] == check_loc_region and loc['name'] == check_loc_name and loc['difficulty'] != 'hardcore']

                if len(standard_locs) > 0:
                    del locations_pool[standard_locs[0]]

        # else, the player is still playing standard, take out all of the matching hardcore difficulty locations
        else:
            locations_pool = {
                id: loc for id, loc in locations_pool.items() if loc['difficulty'] != 'hardcore'
            }

        # now that we've factored in hardcore swaps, remove any hardcore locations that were just there for removing unused standard ones
        locations_pool = { id: loc for id, loc in locations_pool.items() if 'remove' not in loc }
        
        return locations_pool

    def _get_region_table_for_scenario(self, character, scenario) -> list:
        return [
            region for region in Data.region_table 
                if region['character'] == character and region['scenario'] == scenario
        ]
    
    def _get_region_connection_table_for_scenario(self, character, scenario) -> list:
        return [
            conn for conn in Data.region_connections_table
                if conn['character'] == character and conn['scenario'] == scenario
        ]
    
    def _get_character(self) -> str:
        return self._format_option_text(self.options.character).lower()
    
    def _get_scenario(self) -> str:
        return self._format_option_text(self.options.scenario).lower()
    
    def _get_difficulty(self) -> str:
        return self._format_option_text(self.options.difficulty).lower()
    
    def _get_starting_weapon(self) -> str:
        return self.starting_weapon[self.player] if self.player in self.starting_weapon else None

    def _get_all_weapons(self) -> list[str] | None:
        if self.player not in self.replacement_weapons:
            return None

        weapons_list = list(self.replacement_weapons[self.player].values())

        if weapons_list and isinstance(weapons_list[0], list):
            weapons_list = weapons_list[0]

        return [self._get_starting_weapon(), *weapons_list]

    # not private because used by weapon rando file
    def get_starting_weapon_name_from_option_value(self) -> str:
        lookups: dict = {
            "default": None,
            "handgun_matilda": "Matilda",
            "handgun_sls": "SLS 60",
            "handgun_m19": "M19",
            "handgun_quickdraw": "Quickdraw Army",
            "handgun_hp3": "JMB Hp3",
            "flamethrower": "Chemical Flamethrower",
            "shotgun_w870": "W-870",
            "grenadelauncher_gm79": "GM 79",
            "lightninghawk": "Lightning Hawk",
            "submachinegun_mq11": "MQ 11"
        }

        return lookups[self.options.starting_weapon.current_key]
    
    def _replace_pool_item_with(self, pool, from_item_name, to_item_name) -> list:
        items_to_remove = [item for item in pool if item.name == from_item_name]
        count_of_new_items = len(items_to_remove)

        for item in items_to_remove:
            pool.remove(item)

        for x in range(count_of_new_items):
            pool.append(self.create_item(to_item_name))

        return pool

    def _get_oops_all_options_flag(self) -> int:
        flag = 0
        if self._format_option_text(self.options.oops_all_rockets) == 'True':
            flag |= 0x01
        if self._format_option_text(self.options.oops_all_miniguns) == 'True':
            flag |= 0x02
        if self._format_option_text(self.options.oops_all_grenades) == 'True':
            flag |= 0x04
        if self._format_option_text(self.options.oops_all_knives) == 'True':
            flag |= 0x08
        return flag
       
    def _enemy_kill_rando(self) -> bool:
        return self._format_option_text(self.options.add_enemy_kills_as_locations) != "None"

    def _can_enemy_kill_rando(self) -> bool:
        return True # should be supported for all scenarios now thanks to contributions

    # def _output_items_and_locations_as_text(self):
    #     my_locations = [
    #         {
    #             'id': loc.address,
    #             'name': loc.name,
    #             'original_item': self.location_name_to_location[loc.name]['original_item'] if loc.name != "Victory" else "(Game Complete)"
    #         } for loc in self.multiworld.get_locations() if loc.player == self.player
    #     ]

    #     my_locations = set([
    #         "{} | {} | {}".format(loc['id'], loc['name'], loc['original_item'])
    #         for loc in my_locations
    #     ])
        
    #     my_items = [
    #         {
    #             'id': item.code,
    #             'name': item.name
    #         } for item in self.multiworld.get_items() if item.player == self.player
    #     ]

    #     my_items = set([
    #         "{} | {}".format(item['id'], item['name'])
    #         for item in my_items
    #     ])

    #     print("\n".join(sorted(my_locations)))
    #     print("\n".join(sorted(my_items)))

    #     raise BaseException("Done with debug output.")

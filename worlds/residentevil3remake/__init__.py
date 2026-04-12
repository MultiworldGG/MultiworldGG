import re
import typing

from typing import Dict, Any, TextIO
from Utils import visualize_regions

from BaseClasses import ItemClassification, Item, Location, Region, CollectionState, Tutorial
from worlds.AutoWorld import World, WebWorld
from ..generic.Rules import set_rule

from .Data import Data
from .Exceptions import RE3ROptionError
from .Options import RE3ROptions

Data.load_data('jill', 'a')


class UmbrellaNet(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide for setting up Resident Evil 3 Remake to be played in MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["TheRealSolidusSnake"]
    )]


class RE3RLocation(Location):
    def stack_names(*area_names):
        return " - ".join(area_names)

    def stack_names_not_victory(*area_names):
        if area_names[-1] == "Victory":
            return area_names[-1]
        return RE3RLocation.stack_names(*area_names)

    def is_item_allowed(item, location_data, current_item_rule):
        # Always allow items in the allow_item list
        if location_data.get('allow_item') and item.name in location_data['allow_item']:
            return True

        # Otherwise, apply the current rule
        return current_item_rule(item)


class ResidentEvil3Remake(World):
    """
    'Jill, I am your father.' - Nemesis, probably
    """
    game: str = "Resident Evil 3 Remake"
    author: str = "TheRealSolidusSnake"

    data_version = 2
    required_client_version = (0, 6, 5)
    apworld_release_version = "0.2.7"  # defined to show in spoiler log

    item_id_to_name = {item['id']: item['name'] for item in Data.item_table}
    item_name_to_id = {item['name']: item['id'] for item in Data.item_table}
    item_name_to_item = {item['name']: item for item in Data.item_table}

    # RE2-style: maps include enemy_table entries too
    location_id_to_name = {
        loc['id']: RE3RLocation.stack_names(loc['region'], loc['name'])
        for loc in (Data.location_table + Data.enemy_table)
    }
    location_name_to_id = {
        RE3RLocation.stack_names(loc['region'], loc['name']): loc['id']
        for loc in (Data.location_table + Data.enemy_table)
    }
    location_name_to_location = {
        RE3RLocation.stack_names(loc['region'], loc['name']): loc
        for loc in (Data.location_table + Data.enemy_table)
    }

    # this is used to seed the initial item pool from original items, and is indexed by player as name:loc
    source_locations = {}

    # de-dupe the item names for the item group name
    item_name_groups = {key: set(values) for key, values in Data.item_name_groups.items()}

    options_dataclass = RE3ROptions
    options: RE3ROptions
    web = UmbrellaNet()

    # -------------------------------------------------------------------------
    # Enemy kill rando helpers
    # -------------------------------------------------------------------------

    def _enemy_kill_rando(self) -> bool:
        return self._format_option_text(self.options.add_enemy_kills_as_locations) != "None"

    def _can_enemy_kill_rando(self) -> bool:
        return True  # supported for all scenarios now thanks to contributions

    def _bonus_start_enabled(self) -> bool:
        return (
            self._format_option_text(self.options.bonus_start) == 'True'
            or self._enemy_kill_rando()
            or (
                self._format_option_text(self.options.no_first_aid_spray) == 'True'
                and self._format_option_text(self.options.no_green_herb) == 'True'
            )
        )

    # -------------------------------------------------------------------------
    # Generation
    # -------------------------------------------------------------------------

    def generate_early(self):
        # check for option values that UT passed via storing from slot data, and set our options to match if present
        for key, val in getattr(self.multiworld, 're_gen_passthrough', {}).get(self.game, {}).items():
            getattr(self.options, key).value = getattr(self.options, key).options[val]

        # if the enemy kills as locations option is enabled for a scenario that doesn't support it yet, throw an error
        if self._enemy_kill_rando() and not self._can_enemy_kill_rando():
            raise RE3ROptionError("The Enemy Kills as Locations option is only currently supported for Standard difficulty.")

        # start with the normal locations per player for pool
        self.source_locations[self.player] = self._get_locations_for_scenario(self._get_character(), self._get_scenario())  # id:loc

        # turn it into name:loc (store id inside each loc dict too)
        self.source_locations[self.player] = {
            RE3RLocation.stack_names(l['region'], l['name']): {**l, 'id': i}
            for i, l in self.source_locations[self.player].items()
        }

        # Enemy kills: replace placeholder drops with deterministic distribution (RE2 behavior)
        if self._enemy_kill_rando():
            enemy_kill_items = self._format_option_text(self.options.enemy_kill_items).lower()

            # choose what counts as a valid "drop"
            if enemy_kill_items == "healing":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table
                    if i.get('type', 'None') in ['Recovery']
                ]
            elif enemy_kill_items == "gunpowder":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table
                    if 'Gunpowder' in i['name'] or i.get('type', 'None') == 'Gunpowder'
                ]
            elif enemy_kill_items == "ammo":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table
                    if i.get('type', 'None') in ['Ammo']
                ]
            elif enemy_kill_items == "ammo related":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table
                    if i.get('type', 'None') in ['Ammo'] or 'Gunpowder' in i['name'] or i.get('type', 'None') == 'Gunpowder'
                ]
            elif enemy_kill_items == "all weapon related":
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table
                    if i.get('type', 'None') in ['Ammo', 'Subweapon'] or 'Gunpowder' in i['name'] or i.get('type', 'None') == 'Gunpowder'
                ]
            else:  # mixed
                enemy_kill_valid_drops = [
                    i['name'] for i in Data.item_table
                    if i.get('type', 'None') in ['Recovery', 'Ammo', 'Subweapon'] or 'Gunpowder' in i['name'] or i.get('type', 'None') == 'Gunpowder'
                ]

            # get viable items from this scenario's location original items
            enemy_kill_drop_names = list(set([
                l['original_item']
                for l in self.source_locations[self.player].values()
                if l.get('original_item', 'None') in enemy_kill_valid_drops
            ]))

            # safety: if config yields no valid drops, just don't replace placeholders
            if enemy_kill_drop_names:
                enemy_kill_drops = []
                for x in range(len(Data.enemy_table)):
                    drop_name = enemy_kill_drop_names[x % len(enemy_kill_drop_names)]
                    enemy_kill_drops.append(drop_name)

                # replace placeholders for enemy kills with the chosen distribution of items
                for _, loc in self.source_locations[self.player].items():
                    if loc.get('original_item') == "__Enemy Kill Drop Placeholder__":
                        if enemy_kill_drops:
                            loc['original_item'] = enemy_kill_drops.pop(0)

    def create_regions(self):
        scenario_locations = {l['id']: l for _, l in self.source_locations[self.player].items()}
        scenario_regions = self._get_region_table_for_scenario(self._get_character(), self._get_scenario())

        regions = [Region(region['name'], self.player, self.multiworld) for region in scenario_regions]
        added_regions = []

        for region in regions:
            if region.name in added_regions:
                continue

            added_regions.append(region.name)
            region.locations = [
                RE3RLocation(self.player, RE3RLocation.stack_names_not_victory(region.name, location['name']), location['id'], region)
                for _, location in scenario_locations.items()
                if location['region'] == region.name
            ]
            region_data = [r for r in scenario_regions if r['name'] == region.name][0]

            for location in region.locations:
                location_data = scenario_locations[location.address]

                # forced / not randomized
                if location_data.get('force_item'):
                    location.place_locked_item(self.create_item(location_data['force_item']))
                elif location_data.get('randomized') == 0:
                    location.place_locked_item(self.create_item(location_data.get("original_item")))
                else:
                    # missable / nest restriction rules
                    if self._format_option_text(self.options.allow_missable_locations) == 'False' and region_data['zone_id'] != 6:
                        location.item_rule = lambda item: not item.advancement
                    elif self._format_option_text(self.options.allow_progression_in_nest) == 'False' and region_data['zone_id'] == 6:
                        location.item_rule = lambda item: not item.advancement

                # allow-item override
                if location_data.get('allow_item'):
                    current_item_rule = location.item_rule or (lambda _: True)
                    location.item_rule = lambda item, loc_data=location_data, cur_rule=current_item_rule: RE3RLocation.is_item_allowed(
                        item, loc_data, cur_rule
                    )

                # access rules
                if "condition" in location_data and "items" in location_data["condition"]:
                    set_rule(location, lambda state, loc_data=location_data: self._has_items(state, loc_data["condition"].get("items", [])))

            self.multiworld.regions.append(region)

        for connect in self._get_region_connection_table_for_scenario(self._get_character(), self._get_scenario()):
            if connect.get('limitation') in ['ONE_SIDED_DOOR']:
                continue

            from_name = connect['from'] if 'Menu' not in connect['from'] else 'Menu'
            to_name = connect['to'] if 'Menu' not in connect['to'] else 'Menu'

            region_from = self.multiworld.get_region(from_name, self.player)
            region_to = self.multiworld.get_region(to_name, self.player)
            ent = region_from.connect(region_to)

            if "condition" in connect and "items" in connect["condition"]:
                set_rule(ent, lambda state, conn=connect: self._has_items(state, conn["condition"].get("items", [])))

        # visualize_regions(self.multiworld.get_region("Menu", self.player), "region_uml")

        self.multiworld.get_location("Victory", self.player).place_locked_item(self.create_item("Victory"))
        self.multiworld.completion_condition[self.player] = lambda state: self._has_items(state, ['Victory'])

    def create_items(self, to_item_names=None):
        # Conflicting options
        grenades_enabled = self._format_option_text(self.options.oops_all_grenades) == 'True'
        handguns_enabled = self._format_option_text(self.options.oops_all_handguns) == 'True'

        if grenades_enabled and handguns_enabled:
            raise RE3ROptionError(
                f"{self.player_name}'s Resident Evil 3 Remake cannot have both Oops All options enabled at the same time."
            )

        scenario_locations = self.source_locations[self.player]

        pool = [
            self.create_item(item['name'] if item else None)
            for item in [
                self.item_name_to_item[location['original_item']] if location.get('original_item') else None
                for _, location in scenario_locations.items()
            ]
        ]
        pool = [item for item in pool if item is not None]

        # remove already-placed items from pool (forced items, etc.)
        for filled_location in self.multiworld.get_filled_locations(self.player):
            if filled_location.item.code and filled_location.item in pool:
                pool.remove(filled_location.item)

        # starting hip pouches: precollect and remove from pool
        starting_hip_pouches = int(self.options.starting_hip_pouches)
        if starting_hip_pouches > 0:
            hip_pouches = [item for item in pool if item.name == 'Hip Pouch']

            if starting_hip_pouches > len(hip_pouches):
                starting_hip_pouches = len(hip_pouches)
                self.options.starting_hip_pouches.value = len(hip_pouches)

            for x in range(starting_hip_pouches):
                self.multiworld.push_precollected(hip_pouches[x])
                pool.remove(hip_pouches[x])

        # bonus start
        if self._bonus_start_enabled() and grenades_enabled:
            for _ in range(3):
                self.multiworld.push_precollected(self.create_item('First Aid Spray'))
            for _ in range(3):
                self.multiworld.push_precollected(self.create_item('Hand Grenade'))
            for _ in range(3):
                self.multiworld.push_precollected(self.create_item('Flash Grenade'))

        if self._bonus_start_enabled() and not grenades_enabled:
            for _ in range(3):
                self.multiworld.push_precollected(self.create_item('First Aid Spray'))
            for _ in range(3):
                self.multiworld.push_precollected(self.create_item('Handgun Ammo'))

        # no X options
        if self._format_option_text(self.options.no_first_aid_spray) == 'True':
            pool = self._replace_pool_item_with(pool, 'First Aid Spray', 'Flash Grenade')

        if self._format_option_text(self.options.no_green_herb) == 'True':
            pool = self._replace_pool_item_with(pool, 'Green Herb', 'Flash Grenade')

        if self._format_option_text(self.options.no_red_herb) == 'True':
            pool = self._replace_pool_item_with(pool, 'Red Herb', 'Flash Grenade')

        if self._format_option_text(self.options.no_gunpowder) == 'True':
            replaceables = set(item.name for item in pool if 'Gunpowder' in item.name or 'Explosive' in item.name)
            less_useful_items = set(
                item.name for item in pool
                if item.name == 'Flash Grenade' or 'Herb' in item.name
            )
            less_useful_items = list(less_useful_items) or ["Flash Grenade"]

            for from_item in replaceables:
                to_item = self.random.choice(less_useful_items)
                pool = self._replace_pool_item_with(pool, from_item, to_item)

        # traps
        traps = []
        if self._format_option_text(self.options.add_damage_traps) == 'True':
            for _ in range(int(self.options.damage_trap_count)):
                traps.append(self.create_item("Damage Trap"))

        if traps:
            available_spots = [item for item in pool if 'Explosive' in item.name or 'Gunpowder' in item.name]
            self.random.shuffle(available_spots)

            extra_spots = [
                item for item in pool
                if 'Herb' in item.name or 'Ammo' in item.name or 'Rounds' in item.name or 'Grenade' in item.name
            ]
            self.random.shuffle(extra_spots)

            for spot in available_spots:
                if not traps:
                    break
                trap_to_place = traps.pop()
                pool.remove(spot)
                pool.append(trap_to_place)

            for spot in extra_spots:
                if not traps:
                    break
                trap_to_place = traps.pop()
                pool.remove(spot)
                pool.append(trap_to_place)

        # early / extra sewer items
        if self._format_option_text(self.options.early_fire_hose) == 'True':
            qty = len([i for i in pool if i.name == "Fire Hose"])
            if qty > 0:
                self.multiworld.early_items[self.player]["Fire Hose"] = qty

        if self._format_option_text(self.options.extra_sewer_items) == 'True':
            replaceables = [item for item in pool if item.name in ('Green Herb', 'Handgun Ammo')]
            for x in range(min(2, len(replaceables))):
                pool.remove(replaceables[x])
            pool.append(self.create_item('Battery Pack'))
            pool.append(self.create_item('Kendo Gate Key'))

        # Oops! options
        if grenades_enabled:
            items_to_replace = [
                item for item in self.item_name_to_item.values()
                if item.get('type') in ['Weapon', 'Ammo', 'Crafting', 'Upgrade']
            ]
            for from_item in items_to_replace:
                pool = self._replace_pool_item_with(pool, from_item['name'], 'Hand Grenade')

        if handguns_enabled:
            excluded_items = {'G18', 'Extended Mag - G19', 'Moderator - G19'}

            # Special: gunpowder handling to keep Oops thematic
            if self._enemy_kill_rando():
                # If enemy kills are enabled, keep combat power up: gunpowder -> handgun ammo
                for from_item in [i for i in self.item_name_to_item.values() if i.get('type') == 'Gunpowder' or 'Gunpowder' in i.get('name', '')]:
                    pool = self._replace_pool_item_with(pool, from_item['name'], 'Handgun Ammo')
            else:
                # Otherwise swap gunpowders to a curated set of mostly-filler replacements
                replacements_mid = ['Handgun Ammo', 'Flash Grenade']
                replacements_high = ['Green Herb']

                for from_item in [i for i in self.item_name_to_item.values() if i.get('type') == 'Gunpowder' or 'Gunpowder' in i.get('name', '')]:
                    name = from_item['name']
                    if "Explosive A" in name or "Explosive B" in name:
                        pool = self._replace_pool_item_with(pool, name, self.random.choice(replacements_high))
                    else:
                        pool = self._replace_pool_item_with(pool, name, self.random.choice(replacements_mid))

            items_to_replace = [
                item for item in self.item_name_to_item.values()
                if (
                    item.get('type') in ['Weapon', 'Subweapon', 'Ammo', 'Crafting', 'Upgrade']
                    and item.get('name') not in excluded_items
                )
            ]
            for from_item in items_to_replace:
                pool = self._replace_pool_item_with(pool, from_item['name'], 'Handgun Ammo')

        always_local_items = [
            "ID Card",
            "Red Jewel",
            "Blue Jewel",
            "Green Jewel",
        ]

        for item_name in always_local_items:
            count = len([i for i in pool if i.name == item_name])
            if count:
                self.options.local_items.value.add(item_name)

        all_weapon_names = [
            item['name'] for item in self.item_name_to_item.values()
            if item.get('type') == "Weapon"
        ]

        # Local Weapons: mark weapons as local based on pool contents
        if self._format_option_text(self.options.local_weapons) == 'True':
            local_items = {}
            for weapon_name in all_weapon_names:
                count = len([i for i in pool if i.name == weapon_name])
                if count:
                    local_items[weapon_name] = count

            for item_name, item_qty in local_items.items():
                if item_qty > 0:
                    # same behavior as RE2 (adds to the local_items option's set)
                    self.options.local_items.value.add(item_name)

        # Double Weapons: duplicate singletons by replacing filler first
        if self._format_option_text(self.options.double_weapons) == 'True':
            for weapon_name in all_weapon_names:
                count = len([i for i in pool if i.name == weapon_name])

                # if weapon not in pool, or already duplicated, skip
                if not count or count > 1:
                    continue

                eligible_items = [i for i in pool if i.classification == ItemClassification.filler]
                if not eligible_items:
                    eligible_items = [i for i in pool if i.name in ["Flash Grenade", "Gunpowder", "Handgun Ammo"]]

                if not eligible_items:
                    break

                pool.append(self.create_item(weapon_name))
                pool.remove(eligible_items[0])

        # If locations exceed pool, fill remainder
        missing_item_count = len(self.multiworld.get_unfilled_locations(self.player)) - len(pool)
        if missing_item_count > 0:
            for _ in range(missing_item_count):
                pool.append(self.create_item('Flash Grenade'))

        # If pool exceeds locations, trim filler first (keeps generation stable)
        extra_items = len(pool) - len(self.multiworld.get_unfilled_locations(self.player))
        for _ in range(max(0, extra_items)):
            eligible_items = [i for i in pool if i.classification == ItemClassification.filler]
            if not eligible_items:
                eligible_items = [i for i in pool if i.name in ["Flash Grenade", "Gunpowder", "Handgun Ammo"]]
            if not eligible_items:
                break
            pool.remove(eligible_items[0])

        self.multiworld.itempool += pool

    def create_item(self, item_name: str) -> Item:
        if not item_name:
            return

        item = self.item_name_to_item[item_name]

        # RE2-style classification so Double Weapons can find filler reliably
        if item.get('progression', False):
            classification = ItemClassification.progression
        elif item.get('type', None) == 'Trap':
            classification = ItemClassification.trap
        elif item.get('type', None) in ['Lore', 'Filler']:
            classification = ItemClassification.filler
        else:
            classification = ItemClassification.useful

        return Item(item['name'], classification, item['id'], player=self.player)

    def get_filler_item_name(self) -> str:
        return "Flash Grenade"

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = {
            "apworld_version": self.apworld_release_version,
            "difficulty": self._get_difficulty(),
            "unlocked_typewriters": self._format_option_text(self.options.unlocked_typewriters).split(", "),
            "ammo_pack_modifier": self._format_option_text(self.options.ammo_pack_modifier),
            "damage_traps_can_kill": self._format_option_text(self.options.damage_traps_can_kill) == 'True',
            "death_link": self._format_option_text(self.options.death_link) == 'Yes',
            "enemy_kills": self._format_option_text(self.options.add_enemy_kills_as_locations)
        }

        enemy_behavior = self._format_option_text(self.options.enemy_behavior)
        if enemy_behavior != "Off":
            slot_data["enemy_behavior"] = enemy_behavior

        return slot_data

    # called by UT to pass slot data into the world dupe it's trying to generate, so you can make the options match for gen
    def interpret_slot_data(self, slot_data: dict[str, Any]):
        if not slot_data:
            return False

        regen_values: dict[str, Any] = {}
        regen_values['difficulty'] = slot_data.get('difficulty') or self._get_difficulty()
        return regen_values

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"RE3R_AP_World version: {self.apworld_release_version}\n")

    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        # print(self._output_items_and_locations_as_text())
        return

    def _has_items(self, state: CollectionState, item_names: list) -> bool:
        if len(item_names) == 0:
            return True

        if len(item_names) > 0 and type(item_names[0]) is not list:
            item_names = [item_names]

        for set_of_requirements in item_names:
            if len(set(set_of_requirements)) == len(set_of_requirements):
                if state.has_all(set_of_requirements, self.player):
                    return True
            else:
                item_counts = {name: len([i for i in set_of_requirements if i == name]) for name in set_of_requirements}
                for item_name, count in item_counts.items():
                    if not state.has(item_name, self.player, count):
                        break
                else:
                    return True

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
            })

        if self._format_option_text(self.options.difficulty) == 'Inferno':
            locations_pool = {i: l for i, l in locations_pool.items() if l['difficulty'] not in ('assisted', 'hardcore', 'nightmare')}

            for inferno_loc in [l for l in locations_pool.values() if l['difficulty'] == 'inferno']:
                check_region = re.sub(r'I\)$', ')', inferno_loc['region'])
                check_name = inferno_loc['name']
                matching = [i for i, l in locations_pool.items() if l['region'] == check_region and l['name'] == check_name and l['difficulty'] != 'inferno']
                if matching:
                    del locations_pool[matching[0]]

        elif self._format_option_text(self.options.difficulty) == 'Nightmare':
            locations_pool = {i: l for i, l in locations_pool.items() if l['difficulty'] not in ('assisted', 'hardcore', 'inferno')}

            for nightmare_loc in [l for l in locations_pool.values() if l['difficulty'] == 'nightmare']:
                check_region = re.sub(r'N\)$', ')', nightmare_loc['region'])
                check_name = nightmare_loc['name']
                matching = [i for i, l in locations_pool.items() if l['region'] == check_region and l['name'] == check_name and l['difficulty'] != 'nightmare']
                if matching:
                    del locations_pool[matching[0]]

        elif self._format_option_text(self.options.difficulty) == 'Hardcore':
            locations_pool = {i: l for i, l in locations_pool.items() if l['difficulty'] not in ('assisted', 'nightmare', 'inferno')}

            for hardcore_loc in [l for l in locations_pool.values() if l['difficulty'] == 'hardcore']:
                check_region = re.sub(r'H\)$', ')', hardcore_loc['region'])
                check_name = hardcore_loc['name']
                matching = [i for i, l in locations_pool.items() if l['region'] == check_region and l['name'] == check_name and l['difficulty'] != 'hardcore']
                if matching:
                    del locations_pool[matching[0]]

        elif self._format_option_text(self.options.difficulty) == 'Assisted':
            locations_pool = {i: l for i, l in locations_pool.items() if l['difficulty'] not in ('hardcore', 'nightmare', 'inferno')}

            for assisted_loc in [l for l in locations_pool.values() if l['difficulty'] == 'assisted']:
                check_region = re.sub(r'A\)$', ')', assisted_loc['region'])
                check_name = assisted_loc['name']
                matching = [i for i, l in locations_pool.items() if l['region'] == check_region and l['name'] == check_name and l['difficulty'] != 'assisted']
                if matching:
                    del locations_pool[matching[0]]

        else:
            locations_pool = {
                i: l for i, l in locations_pool.items()
                if l['difficulty'] not in ('assisted', 'hardcore', 'nightmare', 'inferno')
            }

        if self._format_option_text(self.options.difficulty) == 'Assisted':
            locations_pool = {
                i: l for i, l in locations_pool.items()
                if 'remove' not in l and not l.get('remove_assisted', False)
            }
        else:
            locations_pool = {
                i: l for i, l in locations_pool.items()
                if 'remove' not in l
            }

        return locations_pool

    def _get_region_table_for_scenario(self, character, scenario) -> list:
        return [r for r in Data.region_table if r['character'] == character and r['scenario'] == scenario]

    def _get_region_connection_table_for_scenario(self, character, scenario) -> list:
        return [c for c in Data.region_connections_table if c['character'] == character and c['scenario'] == scenario]

    # Hard-fixed character and scenario (no longer options, they're not needed)
    def _get_character(self) -> str:
        return 'jill'

    def _get_scenario(self) -> str:
        return 'a'

    def _get_difficulty(self) -> str:
        return self._format_option_text(self.options.difficulty).lower()

    def _replace_pool_item_with(self, pool, from_item_name, to_item_name) -> list:
        items_to_remove = [item for item in pool if item.name == from_item_name]
        count_of_new_items = len(items_to_remove)

        for item in items_to_remove:
            pool.remove(item)

        for _ in range(count_of_new_items):
            pool.append(self.create_item(to_item_name))

        return pool

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
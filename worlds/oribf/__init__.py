from typing import Dict, Any
from BaseClasses import ItemClassification, Region, Tutorial
from worlds.AutoWorld import World, WebWorld

from .Items import OriBlindForestItem, skills, world_events, keystone_items, mapstone_items, filler_items, teleporters, base_items, item_dict, item_alias_list
from .Locations import location_dict, tagged_locations_dict, area_tags, event_location_list
from .Options import OriBlindForestOptions, LogicDifficulty, KeystoneLogic, MapstoneLogic, SeinLogic, Goal, slot_data_options
from .Rules import apply_location_rules, apply_connection_rules, create_progressive_maps, get_goal_condition
from .Regions import region_list
from ..generic.Rules import add_item_rule

class OriBlindForestWebWorld(WebWorld):
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Ori and the Blind Forest randomizer for MWGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["Gray"]
    )

    tutorials = [setup_en]

class OriBlindForestWorld(World):
    """
    Ori and the Blind Forest is a platform-adventure Metroidvania video game developed by Moon Studios in 2015.
    Players assume control of Ori, a small white spirit, and Sein, the "light and eyes" of the Forest's Spirit Tree. 
    They are tasked to move between platforms and solve puzzles.
    """
    game = "Ori and the Blind Forest"
    author: str = "Gray"
    options_dataclass = OriBlindForestOptions
    options: OriBlindForestOptions
    topology_present = True
    web = OriBlindForestWebWorld()
    # TODO: Determine if this is a good number to use
    base_id = 262144
    item_name_to_id = {name: id for id, name in enumerate(item_dict, base_id)}
    location_name_to_id = {name: id for id, name in enumerate(location_dict, base_id)}
    item_name_groups = item_alias_list
    location_name_groups = {location: set(tags) for location, tags in tagged_locations_dict.items()}

    def generate_early(self):
        self.logic_sets: set[str] = {"casual"} # always include at least casual
        self.world_tour_areas: list[str] = []
        self.world_tour_areas_unused: list[str] = area_tags.copy()
        self.fragments_available = 0

        # list of locations to not be included in the multiworld at all
        self.location_exclusion_list: list[str] = []

        if self.options.logic_difficulty == LogicDifficulty.option_master:
            self.logic_sets.add("master")
            self.logic_sets.add("expert")
            self.logic_sets.add("standard")

        if self.options.logic_difficulty == LogicDifficulty.option_expert:
            self.logic_sets.add("expert")
            self.logic_sets.add("standard")

        if self.options.logic_difficulty == LogicDifficulty.option_standard:
            self.logic_sets.add("standard")

        if "Glitches" in self.options.logic_modifiers.value:
            self.logic_sets.add("glitched")

        if self.options.mapstone_logic == MapstoneLogic.option_progressive:
            self.location_exclusion_list.extend(tagged_locations_dict["Map"])
        else:
            self.location_exclusion_list.extend(event_location_list)

    def create_region(self, name: str):
        return Region(name, self.player, self.multiworld)

    def create_regions(self) -> None:
        menu = self.create_region("Menu")
        self.multiworld.regions.append(menu)

        for region_name in region_list:
            region = self.create_region(region_name)
            self.multiworld.regions.append(region)

            # set the starting region
            if region_name == "SunkenGladesRunaway":
                menu.connect(region)

        apply_connection_rules(self)
        apply_location_rules(self)

        if self.options.mapstone_logic == MapstoneLogic.option_progressive:
            create_progressive_maps(self)
        
        if self.options.restrict_dungeon_keys == True:
            self.restrict_item("Ginso", "GinsoKey")
            self.restrict_item("Forlorn", "ForlornKey")
            self.restrict_item("Horu", "HoruKey")

    def restrict_item(self, tag: str, item_name: str):
        for location in tagged_locations_dict[tag]:
            if location not in self.location_exclusion_list:
                add_item_rule(self.get_location(location), lambda item: item.name != item_name)

    def create_item(self, name: str) -> OriBlindForestItem:
        return OriBlindForestItem(name, item_dict[name][0], self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        placed_first_energy_cell = False

        item_list = dict(base_items)
        item_count = 0

        if self.options.keystone_logic == KeystoneLogic.option_area_specific:
            item_list = { **item_list, **keystone_items["AreaSpecific"] }
        else:
            item_list = { **item_list, **keystone_items["Anywhere"] }

        if self.options.mapstone_logic == MapstoneLogic.option_area_specific:
            item_list = { **item_list, **mapstone_items["AreaSpecific"] }
        else:
            item_list = { **item_list, **mapstone_items["Anywhere"] }

        if self.options.include_teleporters == True:
            item_list = { **item_list, **teleporters }

        for item_key, item_value in item_list.items():
            # override the item values for counts that come from options
            if item_key == "WarmthFragment" and "WarmthFragments" in self.options.goal.value:
                # ensures there is always enough warmth fragments, even if required is greater than available
                self.fragments_available: int = max(self.options.warmth_fragments_available.value, self.options.warmth_fragments_required.value)
                item_value = (item_value[0], self.fragments_available)
            if item_key == "Relic" and "WorldTour" in self.options.goal.value:
                item_value = (item_value[0], self.options.relic_count.value)
            if item_key == "MapStone":
                item_value = (item_value[0], item_value[1] + self.options.extra_mapstones.value)
            if item_key in keystone_items["Anywhere"] or item_key in keystone_items["AreaSpecific"]:
                item_value = (item_value[0], int(item_value[1] * (1 + self.options.extra_keystones / 100)))
            if (item_key in skills or item_key in world_events) and self.options.extra_skills:
                item_value = (item_value[0], item_value[1] + 1)

            for count in range(item_value[1]):
                item = self.create_item(item_key)

                # place Sein either in the normal location or in the starting inventory based on options
                if item_key == "SpiritFlame":
                    if self.options.sein_logic == SeinLogic.option_vanilla:
                        self.get_location("Sein").place_locked_item(item)
                    else: # if SeinLogic.option_start
                        self.multiworld.push_precollected(item)
                    # if Sein ever gets randomized, it would be done here with another SeinLogic option

                # add the first energy cell to the starting inventory to allow the player to save right away
                elif item_key == "EnergyCell" and not placed_first_energy_cell:
                    self.multiworld.push_precollected(item)
                    placed_first_energy_cell = True
                
                # place relics in a random location from a random area
                # track which areas have been used in order to not have multiple relics in an area
                elif item_key == "Relic":
                    random_area: str = self.random.choice(self.world_tour_areas_unused)
                    self.world_tour_areas_unused.remove(random_area)
                    self.world_tour_areas.append(random_area)

                    random_location: str = self.random.choice(tagged_locations_dict[random_area])
                    # the random location can't be an excluded location or "Sein" (since this was locked above if vanilla Sein logic is on)
                    while random_location in self.location_exclusion_list or (self.options.sein_logic == SeinLogic.option_vanilla and random_location == "Sein"):
                        random_location = self.random.choice(tagged_locations_dict[random_area])
                    self.get_location(random_location).place_locked_item(item)

                # otherwise add the item normally
                else:
                    self.multiworld.itempool.append(item)
                    item_count += 1

        unfilled_locations = len(self.multiworld.get_unfilled_locations(self.player))
        self.multiworld.itempool += [self.create_filler() for _ in range(unfilled_locations - item_count)]

    def create_event(self, event: str) -> OriBlindForestItem:
        return OriBlindForestItem(event, ItemClassification.progression, None, self.player)

    def set_rules(self) -> None:
        # most of the rules are set above in create_regions

        # set the goal condition
        self.multiworld.completion_condition[self.player] = lambda state: \
            all(get_goal_condition(self, state, goal) for goal in self.options.goal.value) and \
            state.can_reach_region("HoruEscapeInnerDoor", self.player) if self.options.require_final_escape else True

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {}

        for option_name, option_value in self.options.as_dict(*slot_data_options).items():
            slot_data[option_name] = option_value

        slot_data["world_tour_areas"] = self.world_tour_areas
        slot_data["warmth_fragments_available"] = self.fragments_available

        return slot_data

    def get_filler_item_name(self) -> str:
        total = sum([item[1] for item in filler_items.values()])
        weights = [item[1] / total for item in filler_items.values()]
        return self.random.choices(list(filler_items.keys()), weights)[0]
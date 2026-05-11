from typing import Dict, List, Optional
from BaseClasses import Item, ItemClassification, Region, Tutorial, LocationProgressType
from Options import OptionError, Option
from rule_builder.rules import *
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, Type, components, launch as launch_component, icon_paths
from .regions import HitmanRegion
from .settings import HitmanSettings
from .items import HitmanItem, item_table, base_id
from .options import HitmanOptions
from .locations import HitmanLocation, location_table, sanity_location_table, level_completion_location_table, \
    goal_table, valid_targets_table, valid_targets_table_non_master, vanilla_target_table, game_changers_table, \
    LocationTableEntry, item_pickup_location_table, ut_named_sections_table, split_item_pickup_location_table


class HitmanWeb(WebWorld):
    theme = "partyTime"
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Hitman MultiworldGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["BenDipp"])]
    option_groups = options.option_groups

def launch_client(*args):
    from .client import launch
    launch_component(launch, name="HitmanClient", args=args)


components.append(Component("HITMAN World of Assassination Client", func=launch_client, component_type=Type.CLIENT,icon=__name__))
icon_paths[__name__] = f"ap:{__name__}/assets/icon.png"

class HitmanWorld(World):
    """
    Hitman: World of Assassination is a stealth action game developed by IO Interactive.
    Play as Agent 47, a genetically engineered assassin, and travel the globe to eliminate high-profile targets with creativity and precision.
    """

    game = "HITMAN World of Assassination"
    web = HitmanWeb()
    settings: HitmanSettings
    options_dataclass = HitmanOptions
    options: HitmanOptions
    topology_present = True

    tracker_world: ClassVar = {
        "map_page_folder" : "tracker",
        "map_page_maps" : "maps/maps.json",
        "map_page_locations" : ["locations/itempickup_map_locations.json",
                                "locations/itempickup_overview_locations.json",
                                "locations/itempickup_map_non_master_locations.json",
                                "locations/completion_locations.json",
                                "locations/elimination_locations.json",
                                "locations/disguise_locations.json"],
        "map_page_layouts": ["layouts/layout.json"]
        #"map_page_setting_key" : <optional tag that informs which data storage key will be watched for auto tabbing> TODO: is Autotabbing possible?
        #"map_page_index" : <optional function that will control the auto tabbing>
    }

    location_name_to_id = {name: data.id + base_id for name, data in location_table.items()}
    item_name_to_id = {name: data[0] + base_id for name, data in item_table.items()}

    #Keep as list with playerId to differentiate enttilements from multiple players using same world
    enabled_entitlements:Dict[int,list] = {}

    @staticmethod
    def build_name_groups(item_list, index):
        name_groups = {}
        for name, data in item_list.items():
            groups = data[index] 
            if not groups:  # skip if empty
                continue
            for group in groups:
                name_groups.setdefault(group, set()).add(name)
        return name_groups

    @staticmethod
    def build_location_groups(location_list):
        name_groups = {}
        for name, data in location_list.items():
            groups = data.location_groups
            if not groups:  # skip if empty
                continue
            for group in groups:
                name_groups.setdefault(group, set()).add(name)
        return name_groups

    location_name_groups = build_location_groups(location_table)
    item_name_groups = build_name_groups(item_table, 4)
    
    # Universal Tracker support:
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        return slot_data
    ut_can_gen_without_yaml = True

    def generate_early(self):
        if self.options.game_version.value < 3 and len(self.options.included_s3_locations.value) != 0:
            raise OptionError("Cannot enable HITMAN 3 Levels when HITMAN "+str(self.options.game_version.value)+" is selected as game")

        if self.options.game_version.value < 2 and len(self.options.included_s2_locations.value) != 0:
            raise OptionError("Cannot enable HITMAN 2 Levels when HITMAN "+str(self.options.game_version.value)+" is selected as game")

        if self.options.game_version.value < 3 and self.options.starting_location >= 15:
            raise OptionError("Cannot set a HITMAN 3 Level as starting level when HITMAN "+str(self.options.game_version.value)+" is selected as game")

        if self.options.game_version.value < 2 and self.options.starting_location >= 7:
            raise OptionError("Cannot set a HITMAN 2 Level as starting level when HITMAN "+str(self.options.game_version.value)+" is selected as game")

        if self.options.game_version.value < 3 and self.options.goal_level >= 15 \
        and (self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion
        or self.options.goal_mode.value == self.options.goal_mode.option_level_completion):
            raise OptionError("Cannot set a HITMAN 3 Level as goal level when HITMAN "+str(self.options.game_version.value)+" is selected as game")

        if self.options.game_version.value < 2 and self.options.goal_level >= 7 \
        and (self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion
        or self.options.goal_mode.value == self.options.goal_mode.option_level_completion):
            raise OptionError("Cannot set a HITMAN 2 Level as goal level when HITMAN "+str(self.options.game_version.value)+" is selected as game")

        if self.options.random_targets.value and self.options.min_number_of_targets.value > self.options.max_number_of_targets.value:
            print("WARNING "+self.player_name+": Minimum number of targets cannot exceed Maximum number of targets, Swapping values to avoid generation Failure.")
            min = self.options.min_number_of_targets.value
            self.options.min_number_of_targets.value = self.options.max_number_of_targets.value
            self.options.max_number_of_targets.value = min

        if self.options.random_complications.value and self.options.min_number_of_complications.value > self.options.max_number_of_complications.value:
            print("WARNING "+self.player_name+": Minimum number of complications cannot exceed Maximum number of complications, Swapping values to avoid generation Failure.")
            min = self.options.min_number_of_complications.value
            self.options.min_number_of_complications.value = self.options.max_number_of_complications.value
            self.options.max_number_of_complications.value = min

        if (self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion or
        self.options.goal_mode.value == self.options.goal_mode.option_level_completion) and\
        self.options.goal_level.value == self.options.starting_location.value:
            raise OptionError("Goal Level cannot be the same as Starting Level")

        if any(x.startswith("Level - ") for x in self.options.excluded_items.value):
            raise OptionError("Cannot exclude Level-Items. If you want to exclude a Level, use the \"included_x_locations\" options.")
        
        if any(x.startswith("Level - ") for x in self.options.excluded_starting_items.value):
            raise OptionError("Cannot exclude Level-Items. If you want to exclude a Level, use the \"included_x_locations\" options.")

        if self.options.include_sniper_assassin_weapons.value and self.options.game_version.value != 3:
            raise OptionError("Sniper Assassin Weapons can only be enabled when game version is HITMAN 3")

        self.enabled_entitlements[self.player] = []

        # Universal Tracker support:
        if hasattr(self.multiworld, "generation_is_fake"):
            if hasattr(self.multiworld, "re_gen_passthrough"):
                if self.game in self.multiworld.re_gen_passthrough:
                    slot_data = self.multiworld.re_gen_passthrough[self.game]
                    for key, value in slot_data.items():
                        opt: Optional[Option] = getattr(self.options, key, None)
                        if opt is not None:
                            # You can also set .value directly but that won't work if you have OptionSets
                            setattr(self.options, key, opt.from_any(value))
                    self.enabled_entitlements[self.player] = slot_data["entitlements"]
                    self.goal_location = self.location_id_to_name[slot_data["goal_location_id"]]
                    return
        
        # make sure the goal Level is added as location
        if self.options.goal_mode.value == self.options.goal_mode.option_level_completion or \
        self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion:
            self.enabled_entitlements[self.player].append(self.options.goal_level.current_key)
            match self.options.goal_rating.value:
                case self.options.goal_rating.option_any:
                                self.enabled_entitlements[self.player].append(self.options.goal_level.current_key+"_completed")
                                self.goal_location = goal_table[self.options.goal_level.current_key] + " Completed"
                case self.options.goal_rating.option_silent_assassin:
                                self.enabled_entitlements[self.player].append(self.options.goal_level.current_key+"_sa")
                                self.goal_location = goal_table[self.options.goal_level.current_key] + " Completed - Silent Assassin"
                case self.options.goal_rating.option_suit_only:
                                self.enabled_entitlements[self.player].append(self.options.goal_level.current_key+"_so")
                                self.goal_location = goal_table[self.options.goal_level.current_key] + " Completed - Suit Only"
                case self.options.goal_rating.option_silent_assassin_suit_only:
                                self.enabled_entitlements[self.player].append(self.options.goal_level.current_key+"_saso")
                                self.goal_location = goal_table[self.options.goal_level.current_key] + " Completed - Silent Assassin, Suit Only"
                case self.options.goal_rating.option_sniper_assassin:
                                self.enabled_entitlements[self.player].append(self.options.goal_level.current_key+"_sna")
                                self.goal_location = goal_table[self.options.goal_level.current_key] + " Completed - Sniper Assassin"

        # make sure the start Level is added as location
        self.enabled_entitlements[self.player].append(self.options.starting_location.current_key)

        self.enabled_entitlements[self.player].extend(self.options.included_s1_locations.value)
        self.enabled_entitlements[self.player].extend(self.options.included_s2_locations.value)
        self.enabled_entitlements[self.player].extend(self.options.included_s2_dlc_locations.value)
        self.enabled_entitlements[self.player].extend(self.options.included_s3_locations.value)

        if self.options.goal_mode.value == self.options.goal_mode.option_number_of_completions and\
           self.options.goal_amount.value > len(set(self.enabled_entitlements[self.player])):
            raise OptionError("Not enough levels enabled for chosen Goal Amount.")

        if (self.options.goal_mode.value == self.options.goal_mode.option_level_completion or
           self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion) and\
           self.options.goal_rating.value == self.options.goal_rating.option_sniper_assassin and\
           self.options.goal_level.value == self.options.goal_level.option_carpathian_mountains:
            raise OptionError("Carpathian Mountains Completed - Sniper Assassin cannot be set as goal, since Carpathian Mountains cannot be completed with a Sniper Assassin rating.")

        if self.options.goal_mode.value == self.options.goal_mode.option_number_of_completions and\
           self.options.goal_rating == self.options.goal_rating.option_sniper_assassin and\
           "carpathian_mountains" in self.enabled_entitlements[self.player] and\
           self.options.goal_amount.value > len(set(self.enabled_entitlements[self.player]))-1:
            raise OptionError("Not enough levels enabled for chosen Goal Amount. (Note: Carpathian Mountains cannot contain a Sniper Assassin check)")

        if self.options.goal_mode.value == self.options.goal_mode.option_number_of_completions:
            match self.options.goal_rating.value:
                case self.options.goal_rating.option_any:
                    self.options.levels_with_check_for_completion.value.add("all")
                case self.options.goal_rating.option_silent_assassin:
                    self.options.levels_with_check_for_sa.value.add("all")
                case self.options.goal_rating.option_suit_only:
                    self.options.levels_with_check_for_so.value.add("all")
                case self.options.goal_rating.option_silent_assassin_suit_only:
                    self.options.levels_with_check_for_saso.value.add("all")
                case self.options.goal_rating.option_sniper_assassin:
                    self.options.levels_with_check_for_sna.value.add("all")

        # enable completion checks
        if "all" in self.options.levels_with_check_for_completion.value:
            self.enabled_entitlements[self.player].append("completed")
        else:
            for location in self.options.levels_with_check_for_completion.value:
                self.enabled_entitlements[self.player].append(location+"_completed")

        if "all" in self.options.levels_with_check_for_sa.value:
            self.enabled_entitlements[self.player].append("sa")
        else:
            for location in self.options.levels_with_check_for_sa.value:
                self.enabled_entitlements[self.player].append(location+"_sa")

        if "all" in self.options.levels_with_check_for_so.value:
            self.enabled_entitlements[self.player].append("so")
        else:
            for location in self.options.levels_with_check_for_so.value:
                self.enabled_entitlements[self.player].append(location+"_so")

        if "all" in self.options.levels_with_check_for_saso.value:
            self.enabled_entitlements[self.player].append("saso")
        else:
            for location in self.options.levels_with_check_for_saso.value:
                self.enabled_entitlements[self.player].append(location+"_saso")

        if "all" in self.options.levels_with_check_for_sna.value:
            self.enabled_entitlements[self.player].append("sna")
        else:
            for location in self.options.levels_with_check_for_sna.value:
                self.enabled_entitlements[self.player].append(location+"_sna")

        if self.options.enable_itemsanity:
            if self.options.split_itemsanity:
                self.enabled_entitlements[self.player].append("split_itemsanity")
            else:
                self.enabled_entitlements[self.player].append("itemsanity")
        
        if self.options.enable_disguisesanity:
            self.enabled_entitlements[self.player].append("disguisesanity")

        if self.options.item_packages.value == self.options.item_packages.option_in_itempool:
            self.enabled_entitlements[self.player].append("packages_in_pool")
        
        if self.options.include_sniper_assassin_weapons:
            self.enabled_entitlements[self.player].append("heavy_snipers")

        if self.options.game_difficulty.value == self.options.game_difficulty.option_master:
            self.enabled_entitlements[self.player].append("master")

        #Check for version specific DLC
        match self.options.game_version.value:
            case self.options.game_version.option_hitman_world_of_assassination:
                self.enabled_entitlements[self.player].append("H3_BASE")
                
                if self.options.include_freelancer_items:
                    self.enabled_entitlements[self.player].append("H3_FREELANCER") 

                if self.options.include_deluxe_items:
                    self.enabled_entitlements[self.player].append("H3_DELUXE_PACK")

                if self.options.include_h2_expansion_items:
                    self.enabled_entitlements[self.player].append("H3_H2_EXPANSION")

                if self.options.include_sins_items: #TODO: options for individual enable
                    self.enabled_entitlements[self.player].append("H3_SINS_GREED")
                    self.enabled_entitlements[self.player].append("H3_SINS_PRIDE")
                    self.enabled_entitlements[self.player].append("H3_SINS_SLOTH")
                    self.enabled_entitlements[self.player].append("H3_SINS_LUST")
                    self.enabled_entitlements[self.player].append("H3_SINS_GLUTTONY")
                    self.enabled_entitlements[self.player].append("H3_SINS_ENVY")
                    self.enabled_entitlements[self.player].append("H3_SINS_WRATH")

                if self.options.include_trinity_items:
                    self.enabled_entitlements[self.player].append("H3_TRINITY")

                if self.options.include_street_art_items:
                    self.enabled_entitlements[self.player].append("H3_VANITY_CONCRETEART")

                if self.options.include_makeshift_items:
                    self.enabled_entitlements[self.player].append("H3_VANITY_MAKESHIFTSCRAP")

                # Check for H3 Elusive Target DLCs
                if self.options.include_splitter_items:
                    self.enabled_entitlements[self.player].append("H3_ET_LAMBIC")

                if self.options.include_disruptor_items:
                    self.enabled_entitlements[self.player].append("H3_ET_PENICILLIN")

                if self.options.include_undying_items:
                    self.enabled_entitlements[self.player].append("H3_ET_SAMBUCA")

                if self.options.include_drop_items:
                    self.enabled_entitlements[self.player].append("H3_ET_TOMORROWLAND")

                if self.options.include_banker_items:
                    self.enabled_entitlements[self.player].append("H3_ET_FRENCHMARTINI")

                if self.options.include_bruce_lee_items:
                    self.enabled_entitlements[self.player].append("H3_ET_BAIJU")

                if self.options.include_eminem_items:
                    self.enabled_entitlements[self.player].append("H3_ET_BELLINI")

                if self.options.include_jovovich_items:
                    self.enabled_entitlements[self.player].append("H3_ET_FILUR")

            case self.options.game_version.option_hitman_2:
                self.enabled_entitlements[self.player].append("H2_BASE")

                if self.options.include_h2_legacy_items:
                    self.enabled_entitlements[self.player].append("H2_LEGACY")

                if self.options.include_h2_silver_items \
                or self.options.include_h2_gold_items:
                    self.enabled_entitlements[self.player].append("H2_EXECUTIVE")
                    self.enabled_entitlements[self.player].append("H2_COLLECTORS_OR_EXECUTIVE")
                    self.enabled_entitlements[self.player].append("H2_WINTER_SPORTS")
                    self.enabled_entitlements[self.player].append("H2_GREEDY")

                if self.options.include_h2_gold_items:
                    self.enabled_entitlements[self.player].append("H2_COLLECTORS")
                    self.enabled_entitlements[self.player].append("H2_COLLECTORS_OR_EXECUTIVE")
                    self.enabled_entitlements[self.player].append("H2_SMART_CASUAL")
                    self.enabled_entitlements[self.player].append("H2_STINGRAY")

            # Check for H1 DLC
            case self.options.game_version.option_hitman_1:
                self.enabled_entitlements[self.player].append("H1_BASE")

                if self.options.include_h1goty_items:
                    self.enabled_entitlements[self.player].append("H1_GOTY")

                if self.options.include_requiempack_items:
                    self.enabled_entitlements[self.player].append("H1_REQUIEM_PACK")

        self.enabled_entitlements[self.player] = sorted(self.enabled_entitlements[self.player]) #Fix OptionSets giving non-deterministic order for same seed and yaml

        if self.options.random_targets.value:
            target_slot_data = ""
            already_used_targets = []
            for level in valid_targets_table:
                if level in self.enabled_entitlements[self.player]:
                    num_of_targets = self.random.randint(self.options.min_number_of_targets.value,self.options.max_number_of_targets.value)
                    valid_targets = valid_targets_table[level].copy()
                    if self.options.game_difficulty.value != self.options.game_difficulty.option_master:
                        valid_targets += valid_targets_table_non_master[level]
                    if len(valid_targets) == 0 and self.options.enable_target_checks.value:
                        for i in vanilla_target_table[level]:
                            self.enabled_entitlements[self.player].append("TARGET_"+str(i))
                    for i in range(0, num_of_targets):
                        if len(valid_targets) <= len(already_used_targets):
                            break
                        chosen_target = self.random.choice(list(target for target in valid_targets if target not in already_used_targets))
                        target_slot_data += str(chosen_target)+"_"
                        already_used_targets.append(chosen_target)

                        if self.options.enable_target_checks.value:
                            self.enabled_entitlements[self.player].append("TARGET_"+str(chosen_target))

                target_slot_data+="-"
                already_used_targets = []

            self.target_slotdata = target_slot_data
        else:
            self.enabled_entitlements[self.player].append("vanilla_targets")
            if self.options.enable_target_checks.value:
                for level in vanilla_target_table:
                    if level in self.enabled_entitlements[self.player]:
                        for i in vanilla_target_table[level]:
                            self.enabled_entitlements[self.player].append("TARGET_"+str(i)) #TODO: could be replaced with "vanilla_targets" entitlement

            self.target_slotdata = "vanilla"

        if self.options.random_complications.value:
            complication_slot_data = ""
            complication_weights = self.options.complications_weights.value

            for level in goal_table:
                if level in self.enabled_entitlements[self.player] and level != "carpathian_mountains":
                    num_of_complications = self.random.randint(self.options.min_number_of_complications.value,
                                                               self.options.max_number_of_complications.value)

                    already_used_complications = []
                    available_complications = complication_weights.copy()

                    if level == "dubai" and self.options.starting_location.value == self.options.starting_location.option_dubai:
                        #if dubai is starting location, there is no chance to gain other Starting Location to avoid softlock
                        available_complications["No Agility"] = 0

                    if level == "chongqing" and self.options.starting_location.value == self.options.starting_location.option_chongqing and\
                       not self.options.random_targets.value and not self.options.enable_target_checks.value and not self.options.enable_itemsanity and\
                       not self.options.enable_disguisesanity.value:
                        #if chongqing is starting location, has vanilla targets and there are only completion checks,
                        #there is no chance to gain other Starting Location to avoid softlock (one that skips reactor)
                        available_complications["No Agility"] = 0

                    for _ in range(0, num_of_complications):
                        if 0 == sum(1 for x, w in available_complications.items() if w != 0 and x not in already_used_complications):
                            break
                        chosen_complication = self.random.choice(
                            [x for x, w in available_complications.items()
                             for _ in range(w)
                             if w != 0 and x not in already_used_complications]
                        )

                        already_used_complications.append(chosen_complication)
                        for entitlement in game_changers_table[chosen_complication][1]:
                            self.enabled_entitlements[self.player].append(level+entitlement)

                        complication_slot_data += str(game_changers_table[chosen_complication][0]) + "_"

                complication_slot_data += "-"
            self.complications = complication_slot_data
        else:
            self.complications = "vanilla"

        if "chongqing_no_agility" in self.enabled_entitlements[self.player]\
        and "vanilla_targets" in self.enabled_entitlements[self.player]:
            self.enabled_entitlements[self.player].append("chongqing_need_to_skip_datacore")

        if self.options.disable_annoying_locations.value.get("skip_locations_with_wait_time", 0):
            self.enabled_entitlements[self.player].append("SKIP_LOCATIONS_WITH_WAIT_TIMES")
        if self.options.disable_annoying_locations.value.get("skip_locations_with_extra_steps", 0):
            self.enabled_entitlements[self.player].append("SKIP_LOCATIONS_WITH_EXTRA_STEPS")
        if self.options.disable_annoying_locations.value.get("skip_locations_carried_by_npcs", 0):
            self.enabled_entitlements[self.player].append("SKIP_LOCATIONS_FROM_CARRIED_ITEMS")
        if self.options.disable_annoying_locations.value.get("skip_locations_requiring_other_items", 0):
            self.enabled_entitlements[self.player].append("SKIP_LOCATIONS_THAT_REQUIRE_OTHER_ITEM")
        if self.options.disable_annoying_locations.value.get("skip_buried_locations", 0):
            self.enabled_entitlements[self.player].append("SKIP_BURIED_LOCATIONS")

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        map_region = Region("Non Menu Region", self.player, self.multiworld)
        self.multiworld.regions.append(map_region)
        menu_region.connect(map_region)

        if self.options.remove_goal_level_locations.value == self.options.remove_goal_level_locations.option_remove\
         and (self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion
         or  self.options.goal_mode.value == self.options.goal_mode.option_level_completion):
            while self.options.goal_level.current_key in self.enabled_entitlements[self.player]:
                self.enabled_entitlements[self.player].remove(self.options.goal_level.current_key)

        if self.options.max_sanity_checks_per_level.value > 0:
            if hasattr(self.multiworld, "re_gen_passthrough"):
                allowed_sanity_checks = self.multiworld.re_gen_passthrough[self.game]["allowed_sanity_checks"]
            else:
                max_per_level = self.options.max_sanity_checks_per_level.value

                # Build mapping: check -> set(levels it belongs to)
                check_levels = {}
                for check in sanity_location_table:
                    if not sanity_location_table[check].is_allowed(self.enabled_entitlements[self.player]):
                        continue
                    levels = set()

                    for level in goal_table:
                        if any(condition.is_fulfilled(self.enabled_entitlements[self.player]) and
                          "Level - "+goal_table[level] in condition.required_items
                          for condition in sanity_location_table[check].inclusion_conditions):
                            levels.add(level)

                    if levels:
                        check_levels[check] = levels

                # Track how many checks each level currently has
                level_counts = {level: 0 for level in goal_table}
                allowed_sanity_checks = []

                # Shuffle checks to keep randomness
                all_checks = list(check_levels.keys())
                self.random.shuffle(all_checks)

                for check in all_checks:
                    levels = check_levels[check]

                    # Only allow if ALL levels are still below cap
                    if all(level_counts[level] < max_per_level for level in levels):
                        allowed_sanity_checks.append(check)
                        for level in levels:
                            level_counts[level] += 1

                self.allowed_sanity_checks = allowed_sanity_checks
        else:
            allowed_sanity_checks = list(sanity_location_table.keys())

        for location in location_table:
            
            if location in sanity_location_table and location not in allowed_sanity_checks:
                continue

            if location_table[location].is_allowed(self.enabled_entitlements[self.player]):
                map_region.add_locations({location :self.location_name_to_id[location]},HitmanLocation)
                self.set_rule(self.multiworld.get_location(location, self.player), location_table[location].get_rule(self.enabled_entitlements[self.player]))

        if self.options.goal_mode.value == self.options.goal_mode.option_contract_collection or \
        self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion:
            map_region.add_locations({"All Contract Pieces Collected":self.location_name_to_id["All Contract Pieces Collected"]},HitmanLocation)
            self.set_rule(self.multiworld.get_location("All Contract Pieces Collected", self.player),
                          Has("Contract Piece",self.options.goal_required_contract_pieces.value))

        if self.options.goal_mode.value == self.options.goal_mode.option_number_of_completions:
            map_region.add_locations({"All Contract Pieces Collected":self.location_name_to_id["All Contract Pieces Collected"]},HitmanLocation)
            self.set_rule(self.multiworld.get_location("All Contract Pieces Collected", self.player),
                          Has("Contract Piece",self.options.goal_amount.value))

        if self.options.remove_goal_level_locations.value == self.options.remove_goal_level_locations.option_exclude\
         and (self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion
         or  self.options.goal_mode.value == self.options.goal_mode.option_level_completion):

            goal_item = "Level - "+goal_table[self.options.goal_level.current_key]
            for location in map_region.locations:
                if not any(item.startswith("Level - ") and item != goal_item for x in location_table[location.name].fulfilled_conditions(self.enabled_entitlements[self.player]) for item in x.required_items):
                    location.progress_type = LocationProgressType.EXCLUDED

        #Re-add goal location if it wasn't added because of remove_goal_level_locations
        if self.options.remove_goal_level_locations.value == self.options.remove_goal_level_locations.option_remove\
         and (self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion
         or  self.options.goal_mode.value == self.options.goal_mode.option_level_completion):
            self.enabled_entitlements[self.player].append(self.options.goal_level.current_key)
            if not any(location.name == self.goal_location for location in map_region.locations):
                map_region.add_locations({self.goal_location:self.location_name_to_id[self.goal_location]},HitmanLocation)
                self.set_rule(self.multiworld.get_location(self.goal_location, self.player), location_table[self.goal_location].get_rule(self.enabled_entitlements[self.player]))
                self.multiworld.get_location(self.goal_location, self.player).progress_type = LocationProgressType.EXCLUDED

        if hasattr(self.multiworld, "generation_is_fake") and self.options.enable_itemsanity.value:
            if not self.options.split_itemsanity.value:
                self.enabled_entitlements[self.player].append("split_itemsanity") #To be able to use the access_rules of the split_itemsanity versions
                for level in goal_table:
                    if not level in self.enabled_entitlements[self.player]:
                        continue

                    for location in map_region.locations:
                        if location.name in item_pickup_location_table and\
                        "Level - "+goal_table[level] in location_table[location.name].get_required_items(self.enabled_entitlements[self.player]):
                            new_name = location.name+("​"*(list(goal_table).index(level)+1))
                            self.create_ut_event(new_name,location.name,location_table[location.name.replace("-","- "+goal_table[level]+" -",1)].get_rule(self.enabled_entitlements[self.player]),menu_region)
            for section_tuple in ut_named_sections_table:
                for location in frozenset(self.get_locations()):
                    if location.name in section_tuple[1]:
                        if self.options.split_itemsanity.value:
                            self.create_ut_event(section_tuple[0], section_tuple[1][0], split_item_pickup_location_table[section_tuple[1][0]].get_rule(self.enabled_entitlements[self.player]), map_region)
                        else:
                            self.create_ut_event(section_tuple[0], section_tuple[1][1].strip("​"), split_item_pickup_location_table[section_tuple[1][0]].get_rule(self.enabled_entitlements[self.player]), map_region)
            if not self.options.split_itemsanity.value and "split_itemsanity" in self.enabled_entitlements[self.player]:
                self.enabled_entitlements[self.player].remove("split_itemsanity")

    def create_item(self, item:str) -> HitmanItem:
        return HitmanItem(item,item_table[item][2],item_table[item][0]+base_id,self.player)

    def create_item_with_classification(self, item:str, itemtype:ItemClassification) -> HitmanItem:
        return HitmanItem(item,itemtype,item_table[item][0]+base_id,self.player)

    def create_event(self, event: str) -> HitmanItem:
        return HitmanItem(event, ItemClassification.progression, None, self.player)

    def create_ut_event(self, name:str, real_location:str, rule:Rule, connecting_region:Region):
        region = HitmanRegion(name, self.player, self.multiworld)
        region.ut_mirrored_location = real_location #return true in "can_reach" if this location was checked
        connecting_region.connect(region, rule=rule)
        region.add_event(name, "Unused", True_(), HitmanLocation)
        self.multiworld.get_location(name,self.player).ut_mirrored_location = real_location

    def get_filler_item_name(self):
        return "Distraction - Coin"

    def create_items(self) -> None:
        item_pool : List[Item] = []

        valid_filler = []
        valid_useful = []
        priority_filler = []
        valid_duplicats = []
        starting_locaiton = "Level - "+goal_table[self.options.starting_location.current_key]
        required_itemgroups = list(group for location in location_table for group in location_table[location].get_required_item_groups(self.enabled_entitlements[self.player]))
        required_items = list(item for location in location_table for item in location_table[location].get_required_items(self.enabled_entitlements[self.player]))

        for item in item_table:
            if len(item_table[item][1][self.options.game_version.value]) == 0 or all(x in self.enabled_entitlements[self.player] for x in item_table[item][1][self.options.game_version.value]):
                if item in self.options.excluded_starting_items.value:
                    if any(itemgroup in item_table[item][4] for itemgroup in required_itemgroups) or\
                        item in required_items:
                        self.multiworld.push_precollected(self.create_item_with_classification(item, ItemClassification.progression))
                    else:
                        self.multiworld.push_precollected(self.create_item(item))
                    continue
                if item in self.options.excluded_items.value:
                    continue
                if item in required_items and item != starting_locaiton:
                    item_pool.append(self.create_item_with_classification(item, ItemClassification.progression))
                if item_table[item][2] == ItemClassification.filler and item not in self.options.prioritized_filler.value and item not in required_items:
                    valid_filler.append(item)
                if item_table[item][2] == ItemClassification.useful and item not in self.options.prioritized_filler.value and item not in required_items:
                    valid_useful.append(item)
                if item_table[item][3]: #is allowed to be duplicated
                    valid_duplicats.append(item)
                if item in self.options.prioritized_filler.value and item_table[item][2] != ItemClassification.progression:
                    priority_filler.append(item)

        for itemgroup in required_itemgroups:
            if not any(itemgroup in item_table[item.name][4] for item in item_pool+self.multiworld.precollected_items[self.player]): #nothing from required itemgroup is included yet
                priority_filler_in_group = list(item for item in priority_filler if itemgroup in item_table[item][4])
                if len(priority_filler_in_group) != 0:
                    chosen_item = self.random.choice(priority_filler_in_group)
                    priority_filler.remove(chosen_item)
                    item_pool.append(self.create_item_with_classification(chosen_item, ItemClassification.progression))
                    continue

                valid_items_in_group = list(item for item in (valid_filler+valid_useful) if itemgroup in item_table[item][4])
                if len(valid_items_in_group) == 0:
                    raise OptionError("Every item in itemgroup \""+itemgroup+"\" was excluded or disabled, but was required for one or more locations to be accessible.")
                chosen_item = self.random.choice(valid_items_in_group)
                if chosen_item in valid_filler:
                    valid_filler.remove(chosen_item)
                if chosen_item in valid_useful:
                    valid_useful.remove(chosen_item)
                item_pool.append(self.create_item_with_classification(chosen_item, ItemClassification.progression))

        if self.options.goal_mode.value == self.options.goal_mode.option_contract_collection or \
        self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion:
            for i in range(0, self.options.goal_required_contract_pieces.value+self.options.goal_additional_contract_pieces.value):
                item_pool.append(self.create_item_with_classification("Contract Piece", ItemClassification.progression_deprioritized_skip_balancing))

        if self.options.goal_mode.value == self.options.goal_mode.option_contract_collection_level_completion:
            item_pool.remove(self.create_item("Level - "+goal_table[self.options.goal_level.current_key]))
            self.multiworld.get_location("All Contract Pieces Collected", self.player).place_locked_item(self.create_item("Level - "+goal_table[self.options.goal_level.current_key]))

        if self.options.goal_mode.value == self.options.goal_mode.option_number_of_completions:
            goal_entitlement = None 
            match self.options.goal_rating.value:
                case self.options.goal_rating.option_any: goal_entitlement = "completed"
                case self.options.goal_rating.option_silent_assassin: goal_entitlement = "sa"
                case self.options.goal_rating.option_suit_only: goal_entitlement = "so"
                case self.options.goal_rating.option_silent_assassin_suit_only: goal_entitlement = "saso"
                case self.options.goal_rating.option_sniper_assassin: goal_entitlement = "sna"

            for check in level_completion_location_table:
                if level_completion_location_table[check].is_allowed(self.enabled_entitlements[self.player]) and\
                any(goal_entitlement in condition.require_any for condition in level_completion_location_table[check].inclusion_conditions):
                    self.get_location(check).place_locked_item(self.create_item("Contract Piece"))

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        total_excluded_locations = sum(1 for x in self.multiworld.get_unfilled_locations(self.player) if x.progress_type == LocationProgressType.EXCLUDED)
        total_items = len(item_pool)

        if len(item_pool) > (total_locations-total_excluded_locations):
            raise OptionError("Not enough locations for progression items. Consider adding more locations or remove some Contract Pieces.")

        #fill excludeds first, to make sure not everything get promoted to deprioritized_progression and excluded locations go empty
        valid_true_filler = list(item for item in valid_filler if not any(group in item_table[item][4] for group in required_itemgroups))
        priority_true_filler = list(item for item in priority_filler if not any(group in item_table[item][4] for group in required_itemgroups))
        valid_filler_duplicates = list(item for item in valid_duplicats if not any(group in item_table[item][4] for group in required_itemgroups))
        for _ in range(total_excluded_locations):
            if len(priority_true_filler) != 0:
                chosen_item = self.random.choice(priority_true_filler)
                priority_true_filler.remove(chosen_item)
                priority_filler.remove(chosen_item)
            elif len(valid_true_filler) != 0:
                chosen_item = self.random.choice(valid_true_filler)
                valid_true_filler.remove(chosen_item)
                valid_filler.remove(chosen_item)
            else:
                chosen_item = self.random.choice(valid_filler_duplicates)
            item_pool.append(self.create_item(chosen_item))

        for _ in range(total_locations - total_items - total_excluded_locations):
            if len(priority_filler) != 0:
                chosen_item = self.random.choice(priority_filler)
                priority_filler.remove(chosen_item)
            elif len(valid_useful) != 0:
                chosen_item = self.random.choice(valid_useful)
                valid_useful.remove(chosen_item)
            elif len(valid_filler) != 0:
                chosen_item = self.random.choice(valid_filler)
                valid_filler.remove(chosen_item)
            else:
                chosen_item = self.random.choice(valid_duplicats)

            if any(group in item_table[chosen_item][4] for group in required_itemgroups):
                item_pool.append(self.create_item_with_classification(chosen_item, ItemClassification.progression_deprioritized))
            else:
                item_pool.append(self.create_item(chosen_item))

        self.multiworld.push_precollected(self.create_item(starting_locaiton))
        self.multiworld.itempool.extend(item_pool)

    def fill_hook(self,
                  progitempool: List["Item"],
                  usefulitempool: List["Item"],
                  filleritempool: List["Item"],
                  fill_locations: List["Location"]) -> None:
        if self.options.goal_mode.value == self.options.goal_mode.option_level_completion:
            progitempool.sort(key = lambda item: item.player == self.player and item.name == "Level - "+goal_table[self.options.goal_level.current_key])

    def set_rules(self) -> None:
        match self.options.goal_mode.value:
            case self.options.goal_mode.option_level_completion | self.options.goal_mode.option_contract_collection_level_completion:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location(self.goal_location, self.player)
            case self.options.goal_mode.option_contract_collection | self.options.goal_mode.option_number_of_completions:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_location("All Contract Pieces Collected", self.player)
    
    def fill_slot_data(self):
        slotdata = self.options.as_dict( # copy options for yaml-less Universal Tracker
            "game_version",
            "game_difficulty", "enable_itemsanity", "split_itemsanity", "enable_disguisesanity", "max_sanity_checks_per_level",
            "enable_target_checks", "remove_goal_level_locations",
            "random_complications", "min_number_of_complications", "max_number_of_complications", "complications_weights",
            "included_s1_locations", "included_s2_locations", "included_s2_dlc_locations", "included_s3_locations",
            "excluded_items", "excluded_starting_items", "prioritized_filler", "item_packages",
            "include_sniper_assassin_weapons", "starting_location", "goal_mode", "goal_rating",
            "goal_level", "goal_amount", "goal_required_contract_pieces", "goal_additional_contract_pieces",
            "levels_with_check_for_completion", "levels_with_check_for_sa","levels_with_check_for_so",
            "levels_with_check_for_saso", "levels_with_check_for_sna",
            "random_targets", "min_number_of_targets", "max_number_of_targets"
        )
        slotdata["entitlements"] = self.enabled_entitlements[self.player]
        slotdata["starting_location_name"] = self.options.starting_location.current_key

        match self.options.game_difficulty.value:
            case self.options.game_difficulty.option_casual:
                slotdata["difficulty"] = "easy"
            case self.options.game_difficulty.option_professional:
                slotdata["difficulty"] = "normal"
            case self.options.game_difficulty.option_master:
                slotdata["difficulty"] = "hard"
        
        slotdata["goal_mode"] = self.options.goal_mode.current_key
        match self.options.goal_mode.value:
            case self.options.goal_mode.option_number_of_completions:
                slotdata["goal_amount"] = self.options.goal_amount.value
                slotdata["goal_rating"] = self.options.goal_rating.current_key
                slotdata["goal_location_id"] = self.location_name_to_id["All Contract Pieces Collected"]
            case self.options.goal_mode.option_level_completion:
                slotdata["goal_location_id"] = self.location_name_to_id[self.goal_location]
                slotdata["goal_location_name"] = self.options.goal_level.current_key
                slotdata["goal_rating"] = self.options.goal_rating.current_key
            case self.options.goal_mode.option_contract_collection:
                slotdata["goal_amount"] = self.options.goal_required_contract_pieces.value
                slotdata["goal_location_id"] = self.location_name_to_id["All Contract Pieces Collected"]
            case self.options.goal_mode.option_contract_collection_level_completion:
                slotdata["goal_location_id"] = self.location_name_to_id[self.goal_location]
                slotdata["goal_location_name"] = self.options.goal_level.current_key
                slotdata["goal_rating"] = self.options.goal_rating.current_key
                slotdata["goal_amount"] = self.options.goal_required_contract_pieces.value

        slotdata["targets"] = self.target_slotdata

        slotdata["item_packages"] = self.options.item_packages.current_key

        slotdata["complications"] = self.complications

        slotdata["gen_version"] = self.world_version.as_simple_string()

        if hasattr(self, "allowed_sanity_checks"):
            #TODO: Discouraged by "world api.md" docs, but found no other way to give that data to UT at the right time
            slotdata["allowed_sanity_checks"] = self.allowed_sanity_checks

        return slotdata
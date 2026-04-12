import json
from typing import Dict, List, Any, Union
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification
from Options import OptionError
from worlds.AutoWorld import World, WebWorld
from .Items import ItemType, base_id, item_list, fire2_weapons, item_groups
from .Locations import LocationType, UKEnemyLocation, location_list, start_weapon_locations, location_groups
from .Regions import Regions, SecretRegion
from .Rules import UltrakillRules
from .Options import UltrakillOptions
from .Music import multilayer_music, singlelayer_music, ordered_list


class UltrakillWeb(WebWorld):
    # theme = ""
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up ULTRAKILL randomizer and connecting to a MultiworldGG Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TRPG"]
    )]


class UltrakillWorld(World):
    """MANKIND IS DEAD. BLOOD IS FUEL. HELL IS FULL."""

    game = "ULTRAKILL"
    web = UltrakillWeb()

    item_name_to_id = {item.name: (base_id + index) for index, item in enumerate(item_list)}
    location_name_to_id = {loc.name: (base_id + index) for index, loc in enumerate(location_list)}

    item_name_groups = item_groups
    location_name_groups = location_groups
    options_dataclass = UltrakillOptions
    options: UltrakillOptions


    def __init__(self, multiworld, player):
        super(UltrakillWorld, self).__init__(multiworld, player)
        self.start_weapon: str = "Revolver - Piercer"
        self.start_location: str = "0-1: Weapon"
        self.skipped_location_types: List[LocationType] = []

        self.item_classifications: Dict[ItemType, Union[ItemClassification, None]] = {}
        self.item_classifications[ItemType.Weapon] = ItemClassification.progression
        self.item_classifications[ItemType.Fire2] = ItemClassification.progression
        self.item_classifications[ItemType.Stamina] = ItemClassification.progression
        self.item_classifications[ItemType.WallJump] = ItemClassification.progression
        self.item_classifications[ItemType.Slide] = ItemClassification.progression
        self.item_classifications[ItemType.Slam] = ItemClassification.progression
        self.item_classifications[ItemType.Skull] = ItemClassification.progression
        self.item_classifications[ItemType.Level] = ItemClassification.progression
        self.item_classifications[ItemType.Layer] = ItemClassification.progression
        self.item_classifications[ItemType.Filler] = ItemClassification.filler
        self.item_classifications[ItemType.Trap] = ItemClassification.trap
        self.item_classifications[ItemType.LimboSwitch] = ItemClassification.progression
        self.item_classifications[ItemType.ViolenceSwitch] = ItemClassification.progression
        self.item_classifications[ItemType.ClashMode] = ItemClassification.filler
        self.item_classifications[ItemType.RevStd] = ItemClassification.progression
        self.item_classifications[ItemType.RevAlt] = ItemClassification.progression
        self.item_classifications[ItemType.ShoStd] = ItemClassification.progression
        self.item_classifications[ItemType.ShoAlt] = ItemClassification.progression
        self.item_classifications[ItemType.NaiStd] = ItemClassification.progression
        self.item_classifications[ItemType.NaiAlt] = ItemClassification.progression
        self.item_classifications[ItemType.SecretMission] = ItemClassification.progression

        self.event_names: List[str] = []
        self.game_id_to_long: Dict[str, int] = {}
        self.music: Dict[str, str] = {}


    def set_rules(self):
        UltrakillRules(self).set_rules()


    def create_item(self, name: str) -> "UltrakillItem":
        item_id: int = self.item_name_to_id[name]
        id = item_id - base_id
        classification = ItemClassification.filler
        if self.item_classifications[item_list[id].type] != None:
            classification = self.item_classifications[item_list[id].type]

        if name == "Blue Skull (1-4)" and not self.options.hank_rewards:
            classification = ItemClassification.filler

        return UltrakillItem(name, classification, item_id, self.player)
    

    def create_event(self, event: str):
        return UltrakillItem(event, ItemClassification.progression_skip_balancing, None, self.player)
    

    def generate_early(self):
        # level options
        self.start_level = Regions.get_from_id(self.options.start_level.value)
        self.goal_level = Regions.get_from_id(self.options.goal_level.value)

        valid_levels = []
        for level in self.options.goal_level.options.values():
            if Regions.get_from_id(level).short_name not in self.options.skipped_levels.value:
                valid_levels.append(level)
        valid_starts = []
        for level in valid_levels:
            if level in self.options.start_level.options.values():
                valid_starts.append(level)

        #print(self.start_level.short_name, self.goal_level.short_name)
        #print(valid_starts)
        #print(valid_levels)

        def adjust_start_level() -> None:
            if self.options.start_level.value in valid_starts:
                valid_starts.remove(self.options.start_level.value)
            if self.options.start_level.value in valid_levels:
                valid_levels.remove(self.options.start_level.value)
            new_level: int = self.random.choice(valid_starts)
            #print(f"Start level {self.options.start_level.value} -> {new_level}")
            self.options.start_level.value = new_level
            self.start_level = Regions.get_from_id(new_level)

        def adjust_goal_level() -> None:
            if self.options.goal_level.value in valid_levels:
                valid_levels.remove(self.options.goal_level.value)
            new_level: int = self.random.choice(valid_levels)
            #print(f"Goal level {self.options.goal_level.value} -> {new_level}")
            self.options.goal_level.value = new_level
            self.goal_level = Regions.get_from_id(new_level)

        if self.start_level.short_name in self.options.skipped_levels.value and not self.options.start_level.randomized:
            raise OptionError(f"[ULTRAKILL - '{self.player_name}'] "
                            f"Start level ({self.start_level.short_name}) cannot be skipped.")
        while self.start_level.short_name in self.options.skipped_levels.value:
            adjust_start_level()

        if self.start_level.short_name == self.goal_level.short_name and not self.options.goal_level.randomized:
            raise OptionError(f"[ULTRAKILL - '{self.player_name}'] "
                            f"Start level and goal level cannot be the same. ({self.start_level.short_name})")
        while self.start_level.short_name == self.goal_level.short_name:
            adjust_goal_level()

        if self.goal_level.short_name in self.options.skipped_levels.value and not self.options.goal_level.randomized:
            raise OptionError(f"[ULTRAKILL - '{self.player_name}'] "
                            f"Goal level ({self.goal_level.short_name}) cannot be skipped.")
        while self.goal_level.short_name in self.options.skipped_levels.value:
            adjust_goal_level()

        self.start_location = self.random.choice(start_weapon_locations[self.start_level.short_name])

        level_leads_to_secret: List[int] = [ 2, 6, 12, 17, 20, 28 ]
        included_levels: int = self.options.goal_requirement.range_end - len(self.options.skipped_levels.value)

        if self.options.goal_requirement.value >= included_levels \
            and self.options.goal_level.value in level_leads_to_secret \
            and self.options.secret_mission_unlock_type == "secret_exits":
                print(f"[ULTRAKILL - '{self.player_name}'] "
                      f"Goal requirement cannot be {self.options.goal_requirement.value} because goal level "
                      f"{self.goal_level.short_name} leads to an inaccessible secret mission. Lowering goal "
                      f"requirement to {included_levels - 1}.")
                self.options.goal_requirement.value = included_levels - 1

        if self.options.goal_requirement.value > included_levels:
            raise OptionError(f"[ULTRAKILL - '{self.player_name}'] "
                            f"Goal requirement ({self.options.goal_requirement.value}) "
                            f"is higher than the number of included levels. ({included_levels})")


        # starting weapon
        def remove_from_dict(dict: Dict[str, int], key: str) -> None:
            if key in dict:
                del dict[key]
        
        start_weapons: Dict[str, int] = {k: v for k, v in self.options.starting_weapon_pool.value.items() if v > 0}

        if self.start_level.short_name in {"2-3", "8-2", "8-3"}:
            remove_from_dict(start_weapons, "Feedbacker")
            remove_from_dict(start_weapons, "Knuckleblaster")
            remove_from_dict(start_weapons, "Whiplash")

        if self.options.start_with_arm:
            remove_from_dict(start_weapons, "Feedbacker")
        else:
            remove_from_dict(start_weapons, "Whiplash")
            remove_from_dict(start_weapons, "Railcannon - Electric")
            remove_from_dict(start_weapons, "Railcannon - Screwdriver")
            remove_from_dict(start_weapons, "Railcannon - Malicious")
            remove_from_dict(start_weapons, "Rocket Launcher - Freezeframe")

        if not self.options.start_with_arm and self.options.randomize_secondary_fire:
            remove_from_dict(start_weapons, "Rocket Launcher - S.R.S. Cannon")
            remove_from_dict(start_weapons, "Rocket Launcher - Firestarter")

        if not self.options.start_with_arm and self.options.randomize_secondary_fire and self.options.nailgun_form:
            remove_from_dict(start_weapons, "Nailgun - Overheat")

        if len(start_weapons) < 1 or all(weight == 0 for weight in start_weapons.values()):
            raise OptionError(f"[ULTRAKILL - '{self.player_name}'] "
                            "No valid starting weapons available. Add more in your options.")

        self.start_weapon = self.random.choices(list(start_weapons.keys()), list(start_weapons.values()))[0]
        #print(self.start_weapon)

        # excluding items/locations
        if self.options.start_with_slide:
            self.item_classifications[ItemType.Slide] = None

        if self.options.start_with_slam:
            self.item_classifications[ItemType.Slam] = None

        if self.options.secret_mission_unlock_type == "secret_exits":
            self.item_classifications[ItemType.SecretMission] = None

        if self.options.secret_exit_behavior == "standard":
            self.skipped_location_types.append(LocationType.SecretExit)

        if self.options.unlock_type == "levels":
            self.item_classifications[ItemType.Layer] = None
        elif self.options.unlock_type == "layers":
            self.item_classifications[ItemType.Level] = None

        if self.options.enemy_rewards == "bosses":
            self.skipped_location_types.append(LocationType.BossExt)
            self.skipped_location_types.append(LocationType.Enemy)
        elif self.options.enemy_rewards == "extra":
            self.skipped_location_types.append(LocationType.Enemy)
        elif self.options.enemy_rewards == "disabled":
            self.skipped_location_types.append(LocationType.Boss)
            self.skipped_location_types.append(LocationType.BossExt)
            self.skipped_location_types.append(LocationType.Enemy)

        if not self.options.challenge_rewards:
            self.skipped_location_types.append(LocationType.Challenge)

        if not self.options.p_rank_rewards:
            self.skipped_location_types.append(LocationType.PerfectRank)

        if not self.options.hank_rewards:
            self.skipped_location_types.append(LocationType.Hank)

        if not self.options.randomize_clash_mode:
            self.skipped_location_types.append(LocationType.ClashMode)

        if not self.options.fish_rewards:
            self.skipped_location_types.append(LocationType.Fish)

        if not self.options.cleaning_rewards:
            self.skipped_location_types.append(LocationType.Clean)

        if not self.options.chess_reward:
            self.skipped_location_types.append(LocationType.Chess)

        if not self.options.rocket_race_reward:
            self.skipped_location_types.append(LocationType.Rocket)

        if not self.options.randomize_clash_mode:
            self.item_classifications[ItemType.ClashMode] = None

        if self.options.randomize_secondary_fire == "disabled" or self.options.randomize_secondary_fire == "progressive":
            self.item_classifications[ItemType.Fire2] = None

        if self.options.revolver_form == "standard":
            self.item_classifications[ItemType.RevStd] = None
        elif self.options.revolver_form == "alternate":
            self.item_classifications[ItemType.RevAlt] = None

        if self.options.shotgun_form == "standard":
            self.item_classifications[ItemType.ShoStd] = None
        elif self.options.shotgun_form == "alternate":
            self.item_classifications[ItemType.ShoAlt] = None

        if self.options.nailgun_form == "standard":
            self.item_classifications[ItemType.NaiStd] = None
        elif self.options.nailgun_form == "alternate":
            self.item_classifications[ItemType.NaiAlt] = None

        if not self.options.randomize_skulls:
            self.item_classifications[ItemType.Skull] = None

        if not self.options.randomize_limbo_switches:
            self.skipped_location_types.append(LocationType.LimboSwitch)
            self.item_classifications[ItemType.LimboSwitch] = None

        if not self.options.randomize_violence_switches:
            self.skipped_location_types.append(LocationType.ViolenceSwitch)
            self.item_classifications[ItemType.ViolenceSwitch] = None

        # music
        if self.options.music_randomizer:
            temp_dict: Dict[str, str] = {}
            multi1 = []
            multi1.extend(multilayer_music.keys())
            multi2 = [] 
            multi2.extend(multilayer_music.keys())

            while len(multi1) > 0:
                id1 = self.random.choice(multi1)
                id2 = self.random.choice(multi2)

                temp_dict[id1] = id2
                multi1.remove(id1)
                multi2.remove(id2)

            single1 = []
            single1.extend(singlelayer_music.keys())
            single2 = []
            single2.extend(singlelayer_music.keys())

            while len(single1) > 0:
                id1 = self.random.choice(single1)
                id2 = self.random.choice(single2)

                temp_dict[id1] = id2
                single1.remove(id1)
                single2.remove(id2)

            self.music = {i: temp_dict[i] for i in ordered_list}
            #print(self.music)

    
    #def write_spoiler_header(self, spoiler_handle):
    #    if self.options.music_randomizer:
    #        spoiler_handle.write("\nMusic:\n")
    #        for i, j in self.music.items():
    #            original: str
    #            changed: str
    #            if i in multilayer_music.keys():
    #                original = multilayer_music[i]
    #            elif i in singlelayer_music.keys():
    #                original = singlelayer_music[i]
    #            if j in multilayer_music.keys():
    #                changed = multilayer_music[j]
    #            elif j in singlelayer_music.keys():
    #                changed = singlelayer_music[j]
    #            spoiler_handle.write(f"({i}) {original} -> {changed}\n")


    def create_items(self):
        pool = []

        for item in item_list:
            if self.item_classifications[item.type] == None:
                continue
            elif (item.type == ItemType.Level or item.type == ItemType.SecretMission) and item.name in {self.start_level.full_name, self.goal_level.full_name}:
                continue
            elif item.type == ItemType.Filler or item.type == ItemType.Trap:
                continue
            
            count: int = item.count
            if item.type == ItemType.Stamina:
                count = 3 - self.options.starting_stamina.value
            elif item.type == ItemType.WallJump:
                count = 3 - self.options.starting_walljumps.value
            elif item.name == self.start_weapon:
                count = 0
            elif item.name == "Feedbacker":
                count = count - self.options.start_with_arm.value

            if item.type == ItemType.Weapon and item.name in fire2_weapons and self.options.randomize_secondary_fire == "progressive":
                if item.name == self.start_weapon:
                    count = 1
                else:
                    count = 2

            if count <= 0:
                continue
            else:
                for _ in range(count):
                    pool.append(self.create_item(item.name))
        
        junk: int = len(self.multiworld.get_unfilled_locations(self.player)) - (len(pool) + 1)

        trap: int = round(junk * (self.options.trap_percent / 100))
        filler: int = junk - trap

        for _ in range(trap):
            pool.append(self.create_item(self.random.choices(list(self.options.trap_weights.value.keys()), list(self.options.trap_weights.value.values()))[0]))

        for _ in range(filler):
            pool.append(self.create_item(self.random.choices(list(self.options.filler_weights.value.keys()), list(self.options.filler_weights.value.values()))[0]))
            
        self.multiworld.itempool += pool


    def get_filler_item_name(self):
        num: int = self.random.randint(0, 99)
        is_trap: bool = num < self.options.trap_percent

        if is_trap:
            return self.random.choices(list(self.options.trap_weights.value.keys()), list(self.options.trap_weights.value.values()))[0]
        else:
            return self.random.choices(list(self.options.filler_weights.value.keys()), list(self.options.filler_weights.value.values()))[0]


    def pre_fill(self):
        multiworld = self.multiworld
        player = self.player

        first_loc = multiworld.get_location(self.start_location, player)

        if first_loc.item != None:
            if not first_loc.item.name in item_groups["start_weapons"]:
                raise Exception(f"[ULTRAKILL - {multiworld.get_player_name(player)}] "
                                f"'{first_loc.item.name}' is not a valid starting weapon.")
            
            # plando check
            if first_loc.item.name != self.start_weapon:
                print(f"[ULTRAKILL - '{multiworld.get_player_name(player)}'] An item already exists at \"{self.start_location}\". "
                    "Selected starting weapon is being returned to the item pool.")
                
                multiworld.itempool.append(self.create_item(self.start_weapon))
        else:
            first_loc.place_locked_item(self.create_item(self.start_weapon))


    def create_regions(self):
        player = self.player
        multiworld = self.multiworld

        menu = Region("Menu", player, multiworld)

        for r in Regions.all_regions:
            multiworld.regions += [Region(r.full_name, player, multiworld)]
            if isinstance(r, SecretRegion):
                if self.options.secret_mission_unlock_type == "secret_exits":
                    multiworld.get_region(r.parent_level.full_name, player).add_exits({r.full_name})
                else:
                    menu.add_exits({r.full_name})
            else:
                menu.add_exits({r.full_name})

        multiworld.regions.append(menu)

        skipped = self.options.skipped_levels.value
        for index, loc in enumerate(location_list):
            if loc.type in self.skipped_location_types:
                continue
            self.game_id_to_long[loc.game_id] = (base_id + index)

            region: Region = self.get_region(loc.region.full_name)
            location: UltrakillLocation = UltrakillLocation(player, loc.name, (base_id + index), region)
            region.locations.append(location)

            if loc.region.short_name in skipped:
                if self.options.auto_exclude_skipped_locations or isinstance(loc, UKEnemyLocation):
                    self.options.exclude_locations.value.add(loc.name)
            elif isinstance(loc, UKEnemyLocation):
                if loc.applicable_levels.issubset(skipped):
                    self.options.exclude_locations.value.add(loc.name)

        # create events for level completion
        for r in [r for r in Regions.all_regions if not (r.short_name == "shop" or r.short_name == "museum")]:
            name: str = f"Cleared {r.short_name}"
            self.event_names.append(name)

            if r.short_name in self.options.skipped_levels.value:
                continue

            region: Region = self.get_region(r.full_name)
            location: UltrakillLocation = UltrakillLocation(player, name, None, region)

            if not self.goal_level.short_name in name:
                location.place_locked_item(self.create_event("Level Completed"))
            region.locations.append(location)

        victory: Location = self.get_location("Cleared " + self.goal_level.short_name)
        victory.place_locked_item(self.create_event("Victory"))

        multiworld.completion_condition[player] = lambda state: state.has("Victory", player)


    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "version": self.world_version.as_simple_string(),
            "locations": self.game_id_to_long,
            "start": self.start_level.short_name,
            "goal": self.goal_level.short_name,
            "goal_requirement": self.options.goal_requirement.value,
            "perfect_goal": bool(self.options.perfect_goal),
            "secret_mission_unlock_type": bool(self.options.secret_mission_unlock_type.value),
            "secret_exit_behavior": bool(self.options.secret_exit_behavior.value),
            "skipped_levels": self.options.skipped_levels.value,
            "enemy_rewards": self.options.enemy_rewards.value,
            "challenge_rewards": bool(self.options.challenge_rewards),
            "p_rank_rewards": bool(self.options.p_rank_rewards),
            "hank_rewards": bool(self.options.hank_rewards),
            "randomize_clash_mode": bool(self.options.randomize_clash_mode),
            "fish_rewards": bool(self.options.fish_rewards),
            "cleaning_rewards": bool(self.options.cleaning_rewards),
            "chess_reward": bool(self.options.chess_reward),
            "rocket_race_reward": bool(self.options.rocket_race_reward),
            "randomize_secondary_fire": self.options.randomize_secondary_fire.value,
            "start_with_arm": bool(self.options.start_with_arm),
            "starting_stamina": self.options.starting_stamina.value,
            "starting_walljumps": self.options.starting_walljumps.value,
            "start_with_slide": bool(self.options.start_with_slide),
            "start_with_slam": bool(self.options.start_with_slam),
            "revolver_form": self.options.revolver_form.value,
            "shotgun_form": self.options.shotgun_form.value,
            "nailgun_form": self.options.nailgun_form.value,
            "randomize_skulls": bool(self.options.randomize_skulls),
            "randomize_limbo_switches": bool(self.options.randomize_limbo_switches),
            "randomize_violence_switches": bool(self.options.randomize_violence_switches),
            "point_multiplier": self.options.point_multiplier.value,
            "ui_color_randomizer": self.options.ui_color_randomizer.value,
            "gun_color_randomizer": self.options.gun_color_randomizer.value,
            "music_randomizer": bool(self.options.music_randomizer),
            "music": self.music,
            "cybergrind_hints": bool(self.options.cybergrind_hints),
            "death_link": bool(self.options.death_link),
            "death_link_amnesty": self.options.death_link_amnesty.value
        }

        #self.export_lua()

        return slot_data
    

    def export_lua(self) -> None:
        with open("item_mapping.lua", "w") as item_map:
            item_map.write(f"-- Generated from apworld version {self.world_version.as_simple_string()}\n\nITEM_MAPPING = " + "{\n")
            for item in item_list:
                if item.tracker_strings == None:
                    continue
                item_map.write("    [" + str(self.item_name_to_id[item.name]) + "] = {\"" + "\", \"".join(item.tracker_strings) + "\"},\n")
            item_map.write("}")

        with open("location_mapping.lua", "w") as location_map:
            location_map.write(f"-- Generated from apworld version {self.world_version.as_simple_string()}\n\nLOCATION_MAPPING = " + "{\n")
            for location in location_list:
                location_map.write("    [" + str(self.location_name_to_id[location.name]) + "] = {\"" + location.tracker_string + "\"},\n")
            location_map.write("}")


class UltrakillItem(Item):
    game: str = "ULTRAKILL"


class UltrakillLocation(Location):
    game: str = "ULTRAKILL"


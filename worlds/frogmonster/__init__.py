from typing import Any, TextIO
from functools import partial
import orjson
import pkgutil

from BaseClasses import Region, LocationProgressType, Tutorial
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule
from Utils import visualize_regions
from .options import FrogmonsterOptions
from .items import item_id_table, item_data_table, item_name_groups, FrogmonsterItem
from .locations import location_id_table, location_data_table, location_name_groups, FrogmonsterLocation
from .regions import region_data_table
from .names import item_names as i
from .names import location_names as l
from .names import region_names as r
from .combat import Difficulty
from .bugs import every_bug
from .rules_access import parse_access_rule_group, access_rule_groups

class FrogmonsterWebWorld(WebWorld):
    theme = "jungle"

    setup_en = Tutorial(
        tutorial_name="Start Guide",
        description="A guide to setting up and playing the Frogmonster randomizer.",
        language="English",
        file_name="guide_en.md",
        link="guide/en",
        authors=["RoobyRoo"]
    )

    tutorials = [setup_en]

class FrogmonsterWorld(World):
    """Frogmonster is a first-person boss rush shooter adventure game where you play as the titular Frogmonster, slaying monsters, eating bugs, and saving the world from a mad bird god."""

    game = "Frogmonster"
    options: FrogmonsterOptions
    options_dataclass = FrogmonsterOptions
    location_name_to_id = location_id_table
    item_name_to_id = item_id_table
    origin_region_name = r.anywhere
    location_name_groups = location_name_groups
    item_name_groups = item_name_groups
    web = FrogmonsterWebWorld()

    shuffled_bug_effects: dict[int, int]
    starter_gun: FrogmonsterItem
    starter_spell: FrogmonsterItem

    # UT Support. 
    ut_can_gen_without_yaml = True

    def create_item(self, name: str) -> FrogmonsterItem:
        return FrogmonsterItem(name, item_data_table[name].type, item_data_table[name].id, self.player)
    
    def create_event(self, event: str) -> FrogmonsterItem:
        return FrogmonsterItem(event, item_data_table[event].type, None, self.player)
    
    def get_filler_item_name(self) -> str:
        return i.coins

    def generate_early(self) -> None:
        # UT Support. Override gen-specific options according to slot data
        if hasattr(self.multiworld, "re_gen_passthrough"):
            if "Frogmonster" in self.multiworld.re_gen_passthrough:
                slot_data = self.multiworld.re_gen_passthrough["Frogmonster"]
                self.options.game_difficulty.value = slot_data["difficulty"]
                self.options.goal.value = slot_data["goal"]
                self.options.shuffle_puzzles.value = 1 if slot_data["shuffle_puzzles"] else 0
                self.options.open_city.value = 1 if slot_data["open_city"] else 0  # deconverting from the bool it's stored as
                self.options.hardcore_parkour.value = slot_data["hardcore_parkour"]
                self.options.well_light_logic.value = slot_data["well_light_logic"]
                self.options.death_link = slot_data["death_link"]

        # Handling option: Shuffle Bug-Eating Effects
        bugs = [bug.bug_id for bug in every_bug if bug.name != i.mushroom]  
        shuffled_effects = bugs.copy()
        if self.options.shuffle_bug_effects:
            self.random.shuffle(shuffled_effects)
        shuffled_bugs = dict(zip(bugs, shuffled_effects))
        shuffled_bugs[36] = 36  # Mushroom is not shuffled but the client still expects this, it is always 36 and must be added back in manually.
        self.shuffled_bug_effects = shuffled_bugs  # stored as dict for local purposes, but client expects array (handled in slot data)

        # Handling option: Game Difficulty
        self.difficulty = Difficulty(self.options.game_difficulty.value)

        # Handling option: Start with Gear
        if self.options.i_hate_seedling:
            gun_list = [i.reeder, i.gatling_gun, i.machine_gun, i.finisher, i.weepwood_bow]  # no cannon/flamethrower since they're logical
            self.starter_gun = self.create_item(self.random.choice(gun_list))
            spell_list = [i.fireball, i.sharp_shot, i.beans, i.slam, i.mushbomb, i.zap, i.hive, i.puff]
            self.starter_spell = self.create_item(self.random.choice(spell_list))

    def create_regions(self) -> None:
        for region_name in region_data_table.keys():
            # Create base regions.
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)
            # Create base locations, add locations to regions.
            current_region_locations = {key:val.id for key,val in location_data_table.items() if val.region == region_name}
            # Handling option: Shuffle Puzzles
            if not self.options.shuffle_puzzles:
                pop_list: list[str] = []
                for location in current_region_locations.keys():
                    if "Puzzle" in location:
                        pop_list.append(location)
                for location in pop_list:
                    current_region_locations.pop(location)
            region.add_locations(current_region_locations, FrogmonsterLocation)

        # Connect regions to each other.
        for region_name, data in region_data_table.items():
            main_region = self.multiworld.get_region(region_name, self.player)
            for connection in data.connects:
                exit_region = self.multiworld.get_region(connection[0], self.player)
                access_rule = partial(connection[1], self.player, self.difficulty)
                main_region.connect(connecting_region=exit_region, rule=access_rule)

        for bug in every_bug:
            # Create bug region. Bugs can be found in multiple different parts of the map and as such they get their own regions, using region connections as logical access.
            bug_region = Region(bug.name, self.player, self.multiworld)
            for connection in bug.regions:
                home_region = self.multiworld.get_region(connection[0], self.player)
                access_rule = partial(connection[1], self.player, self.difficulty)
                home_region.connect(connecting_region=bug_region, rule=access_rule)
            # Create bug location on region.
            bug_location_data = location_data_table[f"Catch {bug.name}"]
            bug_location = {f"Catch {bug.name}": bug_location_data.id}  # add_locations expects a dict, so we convert here
            bug_region.add_locations(bug_location, FrogmonsterLocation)

        # Handling option: Open City
        if self.options.open_city:
            self.multiworld.get_region(r.lost_swamp, self.player).connect(self.multiworld.get_region(r.city, self.player), None, lambda state: True)

#        visualize_regions(self.multiworld.get_region(r.anywhere, self.player), "Regions.puml")

    def create_items(self) -> None:
        item_pool: list[FrogmonsterItem] = []
        dont_create: list[str] = []
        if self.options.goal == 1:
            dont_create.append(i.eye_fragment)
        if self.options.i_hate_seedling:
            dont_create.append(self.starter_gun.name)
            dont_create.append(self.starter_spell.name)
        if self.options.shuffle_workshop_key != 1:
            dont_create.append(i.workshop_key)
        for name, item in item_data_table.items():
            if item.id:  # excludes events
                if name not in dont_create:
                    for _ in range(item_data_table[name].qty):
                        item_pool.append(self.create_item(name))

        if self.options.shuffle_puzzles:
            for _ in range(7):
                item_pool.append(self.create_item(self.get_filler_item_name()))

        if self.options.shuffle_workshop_key == 2:
            item_pool.append(self.create_item(self.get_filler_item_name()))
            self.multiworld.push_precollected(self.create_item(i.workshop_key))

        self.multiworld.itempool += item_pool

    def set_rules(self) -> None:
        # Set location access requirements.
        for location in location_data_table.items():
            current_location = None
            try:
                current_location = self.multiworld.get_location(location[0], self.player)
            except KeyError:  # if the location does not exist, then it does not need access rules.
                pass
            if current_location:
                current_location.access_rule = partial(location[1].access_rule, self.player, self.difficulty)

        # Set completion condition.
        self.multiworld.completion_condition[self.player] = lambda state: state.has(i.victory, self.player)
        self.multiworld.get_location(l.goal, self.player).place_locked_item(self.create_event(i.victory))

        if self.options.goal == 1:
            self.multiworld.get_location(l.eye_fragment, self.player).place_locked_item(self.create_item(i.eye_fragment))
            self.multiworld.get_location(l.goal, self.player).access_rule = lambda state: state.can_reach(l.eye_fragment, "Location", self.player)
            parse_access_rule_group(self, access_rule_groups["goal_eye_chest_rules"])

        # Exclude or prioritize locations according to locations.py. This will be overwritten by any YAML declarations.
        for location in location_data_table.items():
            if location[1].progress_type != LocationProgressType.DEFAULT:
                self.multiworld.get_location(location[0], self.player).progress_type = location[1].progress_type

        # Handling Option: Start with Gear
        if self.options.i_hate_seedling:
            self.multiworld.get_location(l.reeder, self.player).place_locked_item(self.starter_gun)
            self.multiworld.get_location(l.fireball, self.player).place_locked_item(self.starter_spell)

        # Handling Option: Shuffle Workshop Key
        if self.options.shuffle_workshop_key == 0:
            self.multiworld.get_location(l.workshop_access, self.player).place_locked_item(self.create_item(i.workshop_key))

        # Handling Option: Well Light Logic
        if self.options.well_light_logic == 1 or self.options.well_light_logic == 3:
            well_access = self.multiworld.get_entrance(f'{r.old_wood} -> {r.well}', self.player)
            add_rule(well_access, lambda state: state.has(i.glowbug, self.player))
        if self.options.well_light_logic == 2 or self.options.well_light_logic == 3:
            fire_eater_blocked = [l.runi_key, l.coin_chest_4, l.metal_ore_7]
            for location in fire_eater_blocked:
                add_rule(self.multiworld.get_location(location, self.player), lambda state: state.has(i.fire_fruit_juicer, self.player))

        # Handling Option: Hardcore Parkour
        if self.options.hardcore_parkour:
            parse_access_rule_group(self, access_rule_groups["parkour_rules"])
            
        # Handling Option: Deathlink. If deathlink is on, death-get bugs are expected to be purchased at Wren's shop instead.
        if self.options.death_link:
            parse_access_rule_group(self, access_rule_groups["deathlink_rules"])

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data: dict[str, Any] = {}

        apworld_manifest = orjson.loads(pkgutil.get_data(__name__, "archipelago.json").decode("utf-8"))
        slot_data["apworld_version"] = apworld_manifest["world_version"]

        # Handling option: Shuffle Bug-Eating Effects
        bug_effect_array: list[int] = []
        for i in range (1, 41):
            bug_effect_array.append(self.shuffled_bug_effects[i])
        slot_data["shuffled_bug_effects"] = bug_effect_array

        # Other Options:
        slot_data["shop_multiplier"] = self.options.shop_multiplier.value / 100  # Convert to decimal for client
        slot_data["shuffle_puzzles"] = bool(self.options.shuffle_puzzles.value)  # Client expects true/false for these options
        slot_data["open_city"] = bool(self.options.open_city.value)
        slot_data["death_link"] = bool(self.options.death_link.value)
        slot_data["goal"] = self.options.goal.value
        # These options only matter for UT. They mean nothing to the client.
        slot_data["difficulty"] = self.options.game_difficulty.value
        slot_data["hardcore_parkour"] = self.options.hardcore_parkour.value
        slot_data["well_light_logic"] = self.options.well_light_logic.value
        return slot_data
    
    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        if self.options.shuffle_bug_effects:
            spoiler_handle.write("\n")
            spoiler_handle.write(f"{self.multiworld.get_player_name(self.player)}'s Shuffled Bug Effects:\n")
            bug_names = {bug.bug_id: bug.name for bug in every_bug}
            for bug_id, effect_id in sorted(self.shuffled_bug_effects.items()):
                spoiler_handle.write(f"{bug_names[bug_id]}: {bug_names[effect_id]}\n")
            spoiler_handle.write("\n")

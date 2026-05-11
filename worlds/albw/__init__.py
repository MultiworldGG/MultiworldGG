from .Utils import setup_lib
setup_lib()

import os
import orjson
from typing import Any, ClassVar, Dict, List, Optional, Sequence, Tuple
from worlds.AutoWorld import WebWorld, World
from BaseClasses import CollectionState, Item, ItemClassification, Location, LocationProgressType, MultiWorld, \
    Region, Tutorial
from Fill import fill_restrictive, sweep_from_pool
from settings import Group, UserFilePath, UserFolderPath
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from worlds.generic.Rules import set_rule
from .Hints import sanitize, generate_hints, generate_bow_of_light_hint
from .Items import ALBWItem, Items, ItemData, ItemType, all_items, item_table, vane_to_item, \
    convenient_hyrule_vanes, convenient_lorule_vanes, hyrule_vanes, lorule_vanes
from .Locations import ALBWLocation, LocationData, LocationType, all_locations, dungeon_table, location_table, \
    dungeon_bosses, dungeon_item_excludes, starting_weapon_locations
from .Options import ALBWOptions, CrackShuffle, InitialCrackState, Keysy, LogicMode, NiceItems, WeatherVanes, \
    create_randomizer_settings
from .Patch import PatchInfo, PatchItemInfo, ALBWProcedurePatch
from albwrandomizer import ArchipelagoInfo, Cracksanity, PyRandomizable, SeedInfo, randomize_pre_fill

albw_base_id = 6242624000

def launch_client(*args):
    from .Client import launch
    launch_subprocess(launch, name="ALBWClient", args=args)

components.append(
    Component(
        "A Link Between Worlds Client",
        func=launch_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apalbw")
    )
)

class ALBWWebWorld(WebWorld):
    display_name = "The Legend of Zelda: A Link Between Worlds"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing A Link Between Worlds with MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["randomsalience"],
    )

    tutorials = [setup_en]

class ALBWSettings(Group):
    class ALBWRomFile(UserFilePath):
        """File name of your decrypted North American A Link Between Worlds ROM"""
        description = "A Link Between Worlds ROM File"
        
        def browse(self, filetypes=None, **kwargs):
            filetypes = [("3ds ROM File", [".3ds", ".cci"])]
            return super().browse(filetypes=filetypes, **kwargs)

        @classmethod
        def validate(cls, path: str) -> None:
            pass #TODO add validation; hashing doesn't work for 3ds roms
    
    class ModPath(UserFolderPath):
        """Optional: path to mods folder (either "<path-to-azahar-folder>/load/mods" or "<path-to-sd-card>/luma/titles")
        Setting this to a non-empty value will cause the patcher to automatically install the mod."""
        description = "Mods Folder"
        required = False

    rom_file: ALBWRomFile = ALBWRomFile("Legend of Zelda, The - A Link Between Worlds (USA) (En,Fr,Es).cci")
    mod_path: ModPath = ModPath("")

class ALBWWorld(World):
    """
    A Link Between Worlds is a game in the classic Legend of Zelda series,
    and a sequel to A Link to the Past. Explore dungeons, fight monsters,
    discover magical items, and save the worlds of Hyrule and Lorule!
    """
    game: ClassVar[str] = "A Link Between Worlds"
    options_dataclass = ALBWOptions
    options: ALBWOptions
    topology_present: ClassVar[bool] = False
    required_client_version: Tuple[int, int, int] = (0, 5, 0)
    web: ClassVar[WebWorld] = ALBWWebWorld()
    settings: ALBWSettings
    settings_key: ClassVar[str] = "albw_settings"

    item_name_to_id: ClassVar[Dict[str, int]] = \
        {item.name: item.code + albw_base_id for item in all_items if item.code is not None}
    location_name_to_id: ClassVar[Dict[str, int]] = \
        {loc.name: loc.code + albw_base_id for loc in all_locations if loc.code is not None}

    itempool: List[Item]
    pre_fill_items: List[Item]
    starting_weapon: Optional[ItemData]

    seed: Optional[int]
    seed_info: Optional[SeedInfo]

    def create_item(self, name: str, num: Optional[int] = None) -> ALBWItem:
        item_id = self.item_name_to_id[name] if name in self.item_name_to_id else None
        if not self.options.maiamai_mayhem and name == Items.Maiamai.name:
            item_id = None # if Maiamai are unshuffled, make them an "event" item
        return ALBWItem(name, item_table[name].get_classification(self.options, num), item_id, self.player)
    
    def create_location(self, name: str, region: Region) -> ALBWLocation:
        loc_id = self.location_name_to_id[name] if name in self.location_name_to_id else None
        if not self.options.maiamai_mayhem and location_table[name].loctype == LocationType.Maiamai:
            loc_id = None
        return ALBWLocation(self.player, name, loc_id, region)
    
    def get_filler_item_name(self):
        filler_items = []
        for item in all_items:
            if item.itemtype == ItemType.Junk:
                for _ in range(item.count):
                    filler_items.append(item.name)
        return self.random.choice(filler_items)
    
    def generate_early(self) -> None:
        if self.options.nice_items == NiceItems.option_vanilla and self.options.shuffle_maiamai_rewards:
            print(f"Option shuffle_maiamai_rewards is not compatible with vanilla nice items. Turning off shuffle_maiamai_rewards for player {self.player_name}.")
            self.options.shuffle_maiamai_rewards.value = False

        settings = create_randomizer_settings(self.options)
        archipelago_info = ArchipelagoInfo()
        archipelago_info.name = self.player_name

        # try crack shuffle
        max_tries = 20
        for num_tries in range(max_tries + 1):
            if num_tries == max_tries:
                print(f"Too many attempts to generate world graph for player {self.player_name}. Turning off Crack Shuffle.")
                self.options.crack_shuffle.value = CrackShuffle.option_off
                settings.cracksanity = Cracksanity.Off
            self.seed = self.random.randrange(2**32)
            self.seed_info = randomize_pre_fill(self.seed, settings, archipelago_info)
            if self.seed_info.access_check():
                break

        # add starting weather vanes
        starting_vanes = []
        if self.options.weather_vanes in [WeatherVanes.option_hyrule, WeatherVanes.option_all]:
            starting_vanes += hyrule_vanes
        if self.options.weather_vanes in [WeatherVanes.option_lorule, WeatherVanes.option_all]:
            starting_vanes += lorule_vanes
        if self.options.weather_vanes == WeatherVanes.option_convenient:
            starting_vanes += convenient_hyrule_vanes
            if not self.options.crack_shuffle == CrackShuffle.option_off:
                starting_vanes += convenient_lorule_vanes
        for vane in starting_vanes:
            self.options.start_inventory.value[vane.name] = 1
    
    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(menu_region)

        assert self.seed_info is not None
        region_graph = self.seed_info.get_region_graph()

        # generate regions and locations
        for (region_name, (hint_name, locations, _)) in region_graph.items():
            region = Region(region_name, self.player, self.multiworld, hint_name)
            self.multiworld.regions.append(region)
            for location_name in locations:
                # skip locations like hint ghosts without AP counterparts
                if location_name not in location_table:
                    continue

                loc_data = location_table[location_name]
                if self._is_unrandomized(loc_data):
                    continue

                location = self.create_location(location_name, region)

                # place default item
                item = self._get_location_item(loc_data)
                if item is not None:
                    location.place_locked_item(self.create_item(item.name))

                # optionally prioritize bosses
                if self.options.progression_bosses and location_name in dungeon_bosses:
                    location.progress_type = LocationProgressType.PRIORITY

                set_rule(location, lambda state, location_name=location_name:
                    self.seed_info.can_reach(location_name, self._convert_state(state)))
                region.locations.append(location)

        ravio_shop_region = self.multiworld.get_region("RavioShop", self.player)
        menu_region.connect(ravio_shop_region)

        # generate connections
        path_counts = {}
        for (source_region_name, (_, _, paths)) in region_graph.items():
            for target_region_name in paths:
                source_region = self.multiworld.get_region(source_region_name, self.player)
                target_region = self.multiworld.get_region(target_region_name, self.player)
                name = f"{source_region_name} -> {target_region_name}"
                if name in path_counts.keys():
                    path_counts[name] += 1
                    name = f"{name} [{path_counts[name]}]"
                else:
                    path_counts[name] = 1
                source_region.connect(target_region, name=name, rule=
                    lambda state, source_region_name=source_region_name, target_region_name=target_region_name:
                    self.seed_info.can_traverse(source_region_name, target_region_name, self._convert_state(state)))
    
    def create_items(self) -> None:
        self.itempool = []
        self.pre_fill_items = []
        if self.options.assured_weapon:
            self.starting_weapon = self._get_random_weapon()
        else:
            self.starting_weapon = None
        
        for item in all_items:
            count = self._get_item_count(item)
            if self._save_for_pre_fill(item):
                for _ in range(count):
                    self.pre_fill_items.append(self.create_item(item.name))
                continue
            if item == self.starting_weapon:
                self.pre_fill_items.append(self.create_item(item.name))
                count -= 1
            for num in range(count):
                self.itempool.append(self.create_item(item.name, num))
        
        num_items = len(self.itempool) + len(self.pre_fill_items)
        num_locations = len(self.multiworld.get_unfilled_locations(self.player))
        for _ in range(num_locations - num_items):
            self.itempool.append(self.create_filler())
        
        self.random.shuffle(self.itempool)
        self.multiworld.itempool.extend(self.itempool)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Triforce", self.player)
    
    def pre_fill(self) -> None:
        # randomize dungeon prizes
        if self.options.randomize_dungeon_prizes:
            prize_itempool = [item for item in self.pre_fill_items if item_table[item.name].itemtype == ItemType.Prize]
            prize_location_names = [loc.name for loc in all_locations if loc.loctype == LocationType.Prize]
            self._initial_fill([(prize_itempool, prize_location_names)])

        # randomize dungeon items
        dungeon_items_and_locations = []
        for dungeon in dungeon_table:
            dungeon_itempool = [item for item in self.pre_fill_items if item_table[item.name] in dungeon.items]
            if dungeon.name == "Lorule Castle" and self.options.bow_of_light_in_castle:
                dungeon_itempool.append(self.create_item(Items.BowOfLight.name))
            dungeon_location_names = [loc.name for loc in dungeon.locations if loc.name not in dungeon_item_excludes
                and not (self.options.progression_bosses and loc.name in dungeon_bosses)]
            dungeon_items_and_locations.append((dungeon_itempool, dungeon_location_names))
        self._initial_fill(dungeon_items_and_locations)
        
        # starting weapon
        if self.starting_weapon is not None:
            starting_weapon_itempool = [item for item in self.pre_fill_items if item.name == self.starting_weapon.name]
            self._initial_fill([(starting_weapon_itempool, starting_weapon_locations)])
    
    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data = self.options.as_dict(
            "death_link",
            "logic_mode",
            "lorule_castle_requirement",
            "pedestal_requirement",
            "nice_items",
            "lamp_and_net_as_weapons",
            "no_progression_enemies",
            "maiamai_mayhem",
            "initial_crack_state",
            "crack_shuffle",
            "minigames_excluded",
            "trials_required",
            "open_trials_door",
            "weather_vanes",
            "dark_rooms_lampless",
            "swordless_mode",
            "chest_size_matches_contents",
        )
        slot_data["seed"] = self.seed
        return slot_data

    def generate_output(self, output_directory: str) -> None:
        # Create patch info object
        check_map = self._build_check_map()
        items = {loc.name: PatchItemInfo(sanitize(loc.item.name), loc.item.classification.as_flag())
                        for loc in self.multiworld.get_locations(self.player)}
        hints = generate_hints(self.multiworld, self.player, self.options, self.random)
        bow_of_light_hint = generate_bow_of_light_hint(self.multiworld, self.player)
        patch_info = PatchInfo(PatchInfo.cur_version.as_simple_string(), self.seed, self.player_name,
                               self.options, check_map, items, hints, bow_of_light_hint)

        # Write patch info to json file
        patch = ALBWProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("patch_info.json", patch_info.to_json())

        # Write patch file
        out_file_name = self.multiworld.get_out_file_name_base(self.player)
        patch.write(os.path.join(output_directory, f"{out_file_name}{patch.patch_file_ending}"))
    
    def _initial_fill(self, pools: List[Tuple[List[Item], List[str]]]) -> None:
        for itempool, _ in pools:
            for item in itempool:
                self.pre_fill_items.remove(item)
        state = CollectionState(self.multiworld)
        for item in self.pre_fill_items:
            state.collect(item, prevent_sweep=True)
        all_location_names = [name for _, loc_names in pools for name in loc_names]
        all_locations = [loc for loc in self.multiworld.get_locations(self.player) if loc.name in all_location_names]
        state = sweep_from_pool(state, self.itempool, locations=all_locations)
        for itempool, location_names in pools:
            locations = [loc for loc in self.multiworld.get_unfilled_locations(self.player) if loc.name in location_names]
            self.random.shuffle(locations)
            fill_restrictive(self.multiworld, state, locations, itempool,
                single_player_placement=True, lock=True, allow_excluded=True, allow_partial=False)

    def _convert_state(self, state: CollectionState) -> List[PyRandomizable]:
        randomizables = []
        for (name, count) in state.prog_items[self.player].items():
            item = item_table[name]
            randomizables.extend(item.progress[:count])
        return randomizables
    
    def _build_check_map(self) -> Dict[str, str]:
        # Replace all non-local items with Letter in a Bottle
        check_map = {loc.name: loc.item.name if loc.item.player == self.player
            else "AP Item" for loc in self.multiworld.get_locations(self.player)}
        
        # Fill in unrandomized Maiamai
        if not self.options.maiamai_mayhem:
            for loc in all_locations:
                if loc.loctype == LocationType.Maiamai:
                    check_map[loc.name] = Items.Maiamai.name
        
        # Fill in unrandomized upgrades
        if self.options.nice_items == NiceItems.option_vanilla:
            for loc in all_locations:
                if loc.loctype == LocationType.Upgrade:
                    assert loc.default_item is not None
                    check_map[loc.name] = loc.default_item.name
        elif not self.options.shuffle_maiamai_rewards:
            for loc in all_locations:
                if loc.loctype == LocationType.Upgrade:
                    check_map[loc.name] = Items.RupeeGreen.name
        else:
            check_map["Maiamai Great Spin"] = Items.RupeeGreen.name
                

        # Fill in unrandomized minigames
        if self.options.minigames_excluded:
            for loc in all_locations:
                if loc.is_minigame():
                    check_map[loc.name] = Items.RupeeGreen.name
        
        # Fill in inaccessible shop items
        check_map["Thieves' Town Item Shop (2)"] = Items.GoldBee.name
        check_map["Lorule Lakeside Item Shop (2)"] = Items.GoldBee.name

        return check_map

    def _get_item_count(self, item: ItemData):
        if item.itemtype == ItemType.Prize and self.options.randomize_dungeon_prizes:
            return 1
        if item.is_event():
            return 0
        if item.itemtype == ItemType.Junk:
            return 0
        if item == Items.Maiamai and not self.options.maiamai_mayhem:
            return 0
        if item.itemtype == ItemType.SmallKey and self.options.keysy in [Keysy.option_small, Keysy.option_all]:
            return 0
        if item.itemtype == ItemType.BigKey and self.options.keysy in [Keysy.option_big, Keysy.option_all]:
            return 0
        if item == Items.Quake and self.options.initial_crack_state != InitialCrackState.option_closed:
            return 0
        if item == Items.Merge and self.options.initial_crack_state != InitialCrackState.option_progressive:
            return 0
        if item == Items.Bracelet and self.options.initial_crack_state == InitialCrackState.option_progressive:
            return 0
        if (item == Items.Lamp or item == Items.Net) and not self.options.super_items:
            return 1
        if item.itemtype == ItemType.Ravio and self.options.nice_items != NiceItems.option_shuffled:
            return 1
        if item == Items.BeeBadge and self.options.logic_mode == LogicMode.option_hell:
            return 0
        if item == Items.Sword and self.options.swordless_mode:
            return 0
        return item.count
    
    def _get_location_item(self, location: LocationData) -> Optional[ItemData]:
        if location.loctype == LocationType.Prize and self.options.randomize_dungeon_prizes:
            return None
        if location.loctype == LocationType.Vane:
            assert self.seed_info is not None
            assert location.default_item is not None and location.default_item.vane is not None
            return vane_to_item[self.seed_info.vane_map[location.default_item.vane]]
        if location.loctype == LocationType.Upgrade and self.options.shuffle_maiamai_rewards:
            return None
        if location.loctype == LocationType.Maiamai and not self.options.maiamai_mayhem:
            return Items.Maiamai
        return location.default_item
    
    def _is_unrandomized(self, location: LocationData) -> bool:
        return (location.loctype == LocationType.Maiamai and not self.options.maiamai_mayhem
                                                        and not self.options.shuffle_maiamai_rewards) \
            or (location.loctype == LocationType.Upgrade and not self.options.shuffle_maiamai_rewards) \
            or (location.name == "Maiamai Great Spin" and self.options.shuffle_maiamai_rewards) \
            or (self.options.minigames_excluded and location.is_minigame())
    
    def _save_for_pre_fill(self, item: ItemData) -> bool:
        return item.is_dungeon_item() \
            or (item.itemtype == ItemType.Prize and bool(self.options.randomize_dungeon_prizes)) \
            or (item == Items.BowOfLight and bool(self.options.bow_of_light_in_castle))
    
    def _get_random_weapon(self) -> ItemData:
        weapons = [Items.Bow, Items.Bombs, Items.FireRod, Items.IceRod, Items.Hammer, Items.Boots]
        if not self.options.swordless_mode:
            weapons.append(Items.Sword)
        if self.options.lamp_and_net_as_weapons:
            weapons.extend([Items.Lamp, Items.Net])
        return self.random.choice(weapons)

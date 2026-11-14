# world/dsr/__init__.py
from typing import Dict, Set, List, ClassVar, TextIO, Any, Optional

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification, Location, LocationProgressType
from Fill import FillError
from Options import Toggle, OptionError, Option

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, add_item_rule
from rule_builder.rules import Rule, True_, Has, HasAll

from .Items import DSRItem, DSRItemCategory, item_dictionary, key_item_names, item_descriptions, _all_items
from .PoolGeneration import BuildRequiredItemPool, BuildGuaranteedItemPool, ReplaceItem, titanite_replacements
from .Locations import DSRLocation, DSRLocationCategory, location_tables, location_dictionary, location_skip_categories, \
    region_name_list
from .Groups import location_name_groups, item_name_groups, \
    dlc_prog_items, pw_prog_items, gh_prog_items, post_os_prog_items, post_os_cata_prog_items
from .Options import DSROption, option_groups, GoalConditionOption, LogicToAccessCatacombs, GhostDifficulty, \
    LocalRandoChoice
from .Rules import region_rules_table, DsrEntranceRule, location_rules_table, DsrLocationRule
from .Skips import get_all_skips
from . import Patch as Patch

from settings import Group, FilePath


class DSRWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the MultiworldGG Dark Souls Remastered randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["noka, ArsonAssassin"]
    )
    option_groups = option_groups


    tutorials = [setup_en]


class DSRSettings(Group):
    class UTPoptrackerPath(FilePath):
        """Path to the user's DSR Poptracker Pack."""
        description= "DSR Poptracker Pack zip file"
        required = False
    ut_poptracker_path: UTPoptrackerPath | str = UTPoptrackerPath()

    class GamePath(FilePath):
        """Path to the game executable"""
        description = "The DSR game executable"
        required = True
        md5s = ["878b4603a2cc1ba2cbcd15fc6248e37e"]
    exe_path : GamePath | str = GamePath(r'C:\Program Files (x86)\Steam\steamapps\common\DARK SOULS REMASTERED\DarkSoulsRemastered.exe')
    
def map_page_index(data: Any) -> int:
    if (data is None or data == ""):
        return 0
    return data
    
class DSRWorld(World):
    """
    Dark Souls is a game where you die.
    """

    game: str = "Dark Souls Remastered"
    options_dataclass = DSROption
    options: DSROption
    topology_present: bool = True
    web = DSRWeb()
    data_version = 0
    base_id = 11110000
    enabled_location_categories: Set[DSRLocationCategory]
    locked_location_categories: Set[DSRLocationCategory]
    ap_loc_categories = []
    local_loc_categories = []
    vanilla_loc_categories = []
    required_client_version = (0, 5, 1)
    item_name_to_id = DSRItem.get_name_to_id()
    location_name_to_id = DSRLocation.get_name_to_id()
    item_name_groups = item_name_groups
    item_descriptions = item_descriptions
    location_name_groups = location_name_groups
    settings: ClassVar[DSRSettings]
    # Start UT (Universal Tracker) support
    # UT map import from poptracker support
    tracker_world: ClassVar = {
        "map_page_maps" : "maps/maps.json",
        "map_page_locations" : "locations/locations.json",
        "external_pack_key" : "ut_poptracker_path",
        "map_page_setting_key" : "DSR_current_map_{team}_{player}",
        "map_page_index" : map_page_index,
        "item_page_items" : "items/items.json",
        "map_page_item_layouts_left" : [
            { "name": "Lord Souls",        "items": ["Lordvessel", "Lord Souls"],       "orientation": "lr", "cols": 5 },
            { "name": "Progression Items", "items": ["Key items", "Progression Items"], "orientation": "lr", "cols": 5 },
            { "name": "Fog Walls",         "items": "Fog Wall Keys",                    "orientation": "lr", "cols": 6, "item_size": (36, 48) },
            { "name": "Boss Fog Walls",    "items": "Boss Fog Wall Keys",               "orientation": "lr", "cols": 6, "item_size": (36, 48) }
        ]
    }

    # Tell UT we don't need a yaml
    ut_can_gen_without_yaml = True
    # Define function for it to get the options
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]) -> dict[str, Any]:
        # Trigger a regen in UT
        return slot_data
    # End UT support
    gc = 0 # good create
    bc = 0 # "bad" create (ignored item)
    bw = 0 # bonfire warp



    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.ignorable_items = set()
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()
        self.locked_location_categories = set()


    def generate_early(self):
        # For optional location categories, map their options to the slot data string. This has to be defined before UT yamlless support to map it backward
        acr_cat_map : List[tuple[str, Option, DSRLocationCategory]] = [
            ("BS", self.options.boss_soul_shuffle, DSRLocationCategory.BOSS_SOUL),
            ("BH", self.options.boss_humanity_shuffle, DSRLocationCategory.BOSS_HUMANITY),
            ("BB", self.options.boss_bone_shuffle, DSRLocationCategory.BOSS_BONE),

            # One Time Drop Shuffle
            ("BKW", self.options.bk_weapon_shuffle, DSRLocationCategory.BK_WEAPON),
            ("BKT", self.options.bk_titanite_shuffle, DSRLocationCategory.BK_TITANITE),
            ("LIZ", self.options.lizard_shuffle, DSRLocationCategory.CRYSTAL_LIZARD),
            ("MIM", self.options.mimic_drop_shuffle, DSRLocationCategory.MIMIC_DROP),
            ("MBD", self.options.miniboss_drop_shuffle, DSRLocationCategory.MINIBOSS_DROP),
            ("NPC", self.options.hostile_npc_drop_shuffle, DSRLocationCategory.HOSTILE_NPC_DROP),
            ("MIS", self.options.misc_drop_shuffle, DSRLocationCategory.MISC_DROP),

            # Item Pickup Shuffling
            ("CFI", self.options.corpse_filler_item_shuffle, DSRLocationCategory.CORPSE_FILLER_ITEM),
            ("CUI", self.options.corpse_useful_item_shuffle, DSRLocationCategory.CORPSE_USEFUL_ITEM),
            ("CRI", self.options.corpse_ring_item_shuffle, DSRLocationCategory.CORPSE_RING_ITEM),
        ]

        # Start UT yamlless support
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]

            slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_options.items():
                opt: Optional[Option] = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
            if "ap_loc_categories" in slot_data:
                # maybe go the other way, to check for unknown acronyms in the slot data?
                for (acr, copt, cat) in acr_cat_map:
                    if acr in slot_data["ap_loc_categories"].split(","):
                        copt.value = LocalRandoChoice.option_true




        # End UT yamlless support

        ## Soul Multiplier
        # If soul multiplier steps is 0, don't make there be an increase at all. Base is both the base and max
        if self.options.soul_multiplier_steps.value == 0:
            self.options.soul_multiplier_max.value = self.options.soul_multiplier_base.value

        # If soul multiplier base and max are equal, set steps to 0.
        if self.options.soul_multiplier_max.value == self.options.soul_multiplier_base.value:
            self.options.soul_multiplier_steps.value = 0

        # If soul multiplier base > max, reverse them
        if self.options.soul_multiplier_base.value > self.options.soul_multiplier_max.value:
            (self.options.soul_multiplier_base.value, self.options.soul_multiplier_max.value) = (self.options.soul_multiplier_max.value, self.options.soul_multiplier_base.value)

        ## Weight Multiplier
        # If weight multiplier steps is 0, don't make there be an increase at all. Base is both the base and min
        if self.options.weight_multiplier_steps.value == 0:
            self.options.weight_multiplier_min.value = self.options.weight_multiplier_base.value

        # If weight multiplier base and max are equal, set steps to 0.
        if self.options.weight_multiplier_min.value == self.options.weight_multiplier_base.value:
            self.options.weight_multiplier_steps.value = 0

        # If weight multiplier base < min, reverse them
        if self.options.weight_multiplier_base.value < self.options.weight_multiplier_min.value:
            (self.options.weight_multiplier_base.value, self.options.weight_multiplier_min.value) = (self.options.weight_multiplier_min.value, self.options.weight_multiplier_base.value)

        # If steps > 0 but no allowed infusion types, default to normal
        if self.options.incoming_weapon_upgrade_steps.value > 0 and len(
                self.options.incoming_weapon_upgrade_infusion_paths.value) == 0:
            self.options.incoming_weapon_upgrade_infusion_paths.value = ['Normal']

        ## Incoming Weapon Upgrades
        # If there won't be enough AP weapons for upgrades to matter much (and not many souls to replace), reduce steps to 0
        # This prevents the problem of having to remove weapons from the pool to support the weapon upgrade items
        if self.options.limited_shop_item_shuffle.value == False and self.options.corpse_filler_item_shuffle.value != LocalRandoChoice.option_true:
            if (self.options.incoming_weapon_upgrade_steps.value > 0):
                print(f"DSR [{self.player_name}]: Very few weapons and locations in item pool - disabling progressive incoming weapon upgrade system")
                self.options.incoming_weapon_upgrade_steps.value = 0

            # For O+S goal, 10 seems to be the max to add
            if self.options.goal_condition == GoalConditionOption.option_ornstein_and_smough and (self.options.soul_multiplier_steps.value + self.options.weight_multiplier_steps > 10):
                print(f"DSR [{self.player_name}]: Not enough locations for number of soul + weight multiplier steps. Decrease them to 10 total (e.g. 5 and 5)")
                raise OptionError(f"DSR [{self.player_name}]: Not enough locations for number of soul + weight multiplier steps. Decrease them to 10 total (e.g. 5 and 5)")

            # For gwyn goal, 20 as a limit is fine (weapon upgrades are already limited!)


        # If Incoming Weapon Upgrade Steps is 0, don't make there be an increase at all. Base is both the base and max
        if self.options.incoming_weapon_upgrade_steps.value == 0:
            self.options.incoming_weapon_upgrade_max.value = self.options.incoming_weapon_upgrade_base.value

        # If Incoming Weapon Upgrade base and max are equal, set steps to 0.
        if self.options.incoming_weapon_upgrade_base.value == self.options.incoming_weapon_upgrade_max.value:
            self.options.incoming_weapon_upgrade_steps.value = 0

        # If Incoming Weapon Upgrade base > max, reverse them
        if self.options.incoming_weapon_upgrade_base.value > self.options.incoming_weapon_upgrade_max.value:
            (self.options.incoming_weapon_upgrade_base.value, self.options.incoming_weapon_upgrade_max.value) = (
                self.options.incoming_weapon_upgrade_max.value, self.options.incoming_weapon_upgrade_base.value)

        # If goal_condition is o+s, force no dlc
        if self.options.include_dlc.value == True and self.options.goal_condition.value == GoalConditionOption.option_ornstein_and_smough:
            self.options.include_dlc.value = False

        # If goal_condition is manus, force dlc
        if self.options.include_dlc.value == False and self.options.goal_condition.value == GoalConditionOption.option_manus:
            self.options.include_dlc.value = True



        self.enabled_location_categories.add(DSRLocationCategory.EVENT)
        self.enabled_location_categories.add(DSRLocationCategory.BOSS)
        self.enabled_location_categories.add(DSRLocationCategory.BOSS_DROP)

        self.enabled_location_categories.add(DSRLocationCategory.CHEST_ITEM)

        # Always shuffle corpse prog items. If player wants to make them vanilla, they can use plando
        self.enabled_location_categories.add(DSRLocationCategory.CORPSE_PROG_ITEM)
        # Always shuffle frozen blacksmiths, and npc prog items
        self.enabled_location_categories.add(DSRLocationCategory.FROZEN_BLACKSMITH)
        self.enabled_location_categories.add(DSRLocationCategory.NPC_PROG_ITEM)


        self.ap_loc_categories = []
        self.local_loc_categories = []
        self.vanilla_loc_categories = []


        # Build optional ap location categories into their loc lists
        for (acr, copt, cat) in acr_cat_map:
            if copt.value == LocalRandoChoice.option_true:
                self.ap_loc_categories.append(acr)
            elif copt.value == LocalRandoChoice.option_local_only:
                self.local_loc_categories.append(acr)
            elif copt.value == LocalRandoChoice.option_false:
                self.vanilla_loc_categories.append(acr)
        # Use the values in the ap loc list to enable those categories specifically
        for (acr, copt, cat) in acr_cat_map:
            if acr in self.ap_loc_categories:
                self.enabled_location_categories.add(cat)

        if (self.options.lord_soul_shuffle == True):
            self.enabled_location_categories.add(DSRLocationCategory.LORD_SOUL) # Add to pool if setting is true
        else:
            self.locked_location_categories.add(DSRLocationCategory.LORD_SOUL) # Add as "event" items otherwise, so they aren't duplicated to pool

        if (self.options.fogwall_sanity.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.FOG_WALL)
        if (self.options.boss_fogwall_sanity.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.BOSS_FOG_WALL)


        if (self.options.limited_shop_item_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.SHOP_ITEM)
            self.enabled_location_categories.add(DSRLocationCategory.SHOP_EXTENDED_ITEM)
        else:
            self.locked_location_categories.add(DSRLocationCategory.SHOP_ITEM) # add shop_item as locked, so residence key and crest of artorias aren't duplicated to pool

        self.ignorable_items = [item.name for item in _all_items if
                              ((self.options.include_dlc.value == False) and item.name in dlc_prog_items)
                           or ((self.options.include_pw.value == False) and item.name in pw_prog_items)
                           or ((self.options.include_gh.value == False) and item.name in gh_prog_items)
                           or ((self.options.goal_condition.value == GoalConditionOption.option_ornstein_and_smough)
                               and item.name in post_os_prog_items)
                           or ((self.options.goal_condition.value == GoalConditionOption.option_ornstein_and_smough)
                               and self.options.logic_to_access_catacombs == LogicToAccessCatacombs.option_ornstein_and_smough
                                and item.name in post_os_cata_prog_items)]
        # print(f"DSR [{self.player_name}]: totg logic = {self.options.logic_to_access_totg.current_key}")
        # print(f"DSR [{self.player_name}]: sunlight maggot ignored = {"Sunlight Maggot" in self.ignorable_items}")
        # print(f"DSR [{self.player_name}]: ignorable items = {self.ignorable_items}")
        # Remove sunlight maggot from ignored items if it's required
        # if self.options.logic_to_access_totg.current_key == "sunlight_maggot" and "Sunlight Maggot" in self.ignorable_items:
        #     self.ignorable_items.remove("Sunlight Maggot")
        #     print("Removing Sunlight Maggot from ignorable list")


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])

        valid_regions: List = []
        valid_regions.extend(region_name_list.keys())

        removable_regions: List = []
        if not self.options.include_dlc.value:
            removable_regions.extend([reg for reg,tags in region_name_list.items() if "dlc" in tags])
        if not self.options.include_gh.value:
            removable_regions.extend([reg for reg,tags in region_name_list.items() if "gh" in tags])
        if not self.options.include_pw.value:
            removable_regions.extend([reg for reg,tags in region_name_list.items() if "pw" in tags])
        if self.options.goal_condition == GoalConditionOption.option_ornstein_and_smough:
            removable_regions.extend([reg for reg,tags in region_name_list.items() if "postos" in tags])
            if self.options.logic_to_access_catacombs == LogicToAccessCatacombs.option_ornstein_and_smough:
                removable_regions.extend([reg for reg,tags in region_name_list.items() if "postos_cata" in tags])
        for region in removable_regions:
            if region in valid_regions:
                valid_regions.remove(region)

        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in valid_regions})
        # print("DSR: created " + str(self.gc) + " real and "+ str(self.bc) + " fake locations")

        # Connect Regions
        def create_connection(from_region: str, to_region: str, rule: Rule=True_()):
            self.create_entrance(regions[from_region], regions[to_region], rule)

        for region in region_rules_table.keys():
            if region in valid_regions:
                # print(f"Creating region {region}")
                for entrance in region_rules_table[region]:
                    if entrance.source in valid_regions or entrance.source == "Menu":
                        # print(f"Creating connection {entrance.source} -> {region}")
                        create_connection(entrance.source, region, rule=entrance.rule)

        # for skip in get_all_skips():
        #     self.create_entrance(regions[skip.starting_location], regions[skip.ending_location], rule=skip.get_rule(self), name=f"SKIP {skip.name}", force_creation=True)
        

    # For each region, add the associated locations retrieved from the corresponding location_table
    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        #print("location table size: " + str(len(location_table)))
        
        for location in location_table:
            #print("Creating location: " + location.name)
            default_item = location.default_item
            if (default_item in titanite_replacements.keys()):
                default_item = ReplaceItem(self, default_item)

            # Allow progression items here - so that unrandomized progression items (e.g. archive cell key, or crest of artorias with shop shuffle off) are still considered for the rules
            if location.category in self.enabled_location_categories or self.is_item_prog(default_item) or self.is_item_useful(default_item):
                if (location.category in self.enabled_location_categories
                    and location.category not in location_skip_categories   # [DSRLocationCategory.EVENT, DSRLocationCategory.DOOR]:
                    and location.category not in self.locked_location_categories):
                    self.gc = self.gc + 1
                    if (location.category in [DSRLocationCategory.FOG_WALL, DSRLocationCategory.BOSS_FOG_WALL]):
                        default_item = "Fogwall Filler"
                    # print("Adding location: " + location.name + " with default item " + location.default_item)
                    new_location = DSRLocation(
                        self.player,
                        location.name,
                        location.category,
                        default_item,
                        self.location_name_to_id[location.name],
                        new_region
                    )
                    if location.category in [DSRLocationCategory.MISSABLE_DROP, DSRLocationCategory.MISSABLE_SHOP_ITEM]:
                        new_location.progress_type = LocationProgressType.EXCLUDED
                else:
                    self.bc = self.bc + 1
                    if (location.category in [DSRLocationCategory.FOG_WALL, DSRLocationCategory.BOSS_FOG_WALL,
                                              DSRLocationCategory.DOOR]):
                        default_item = "Nothing"
                        # print("Placing event: " + default_item + " in location: " + location.name)

                    # Replace non-randomized progression items with events
                    event_item = self.create_item(default_item)
                    # if event_item.classification != ItemClassification.progression:
                    #    continue
                    # print("Adding Location: " + location.name + " as an event with default item " + default_item)
                    new_location = DSRLocation(
                        self.player,
                        location.name,
                        location.category,
                        default_item,
                        None,
                        new_region
                    )
                    event_item.code = None
                    new_location.place_locked_item(event_item)
                

                new_region.locations.append(new_location)
        
        # print("created " + str(len(new_region.locations)) + " locations")
        self.multiworld.regions.append(new_region)
        #print("adding region: " + region_name)
        return new_region


    def create_items(self):
        skip_itemlocs: List[DSRItem, Location] = []
        skipitempool: List[DSRItem] = []
        itempool: List[DSRItem] = []
        itempoolSize = 0
        
        # print("Creating items")
        for location in self.multiworld.get_locations(self.player):
            itemname = location.default_item_name
            if (itemname in titanite_replacements.keys()):
                itemname = ReplaceItem(self, itemname)
            citem = self.create_item(itemname)
            
            if (location.category in location_skip_categories 
             or location.category in self.locked_location_categories): # [DSRLocationCategory.EVENT]:
                # print("Adding skip item: " + location.default_item_name + " for location: " + location.name)
                if self.is_item_prog(citem.name) or self.is_item_useful(citem.name):
                    skip_itemlocs.append((citem, location))
                    skipitempool.append(citem)
            elif location.category in self.enabled_location_categories:
                #print("Adding item: " + location.default_item_name)
                itempoolSize += 1
                itempool.append(citem)
        
        # print("Requesting itempool size: " + str(itempoolSize))
        # foo = BuildItemPool(itempoolSize, self.options, self)
        # print("Created item pool size: " + str(len(foo)))

        # Add any Key + useful items
        rip, required_skip_item_names = BuildRequiredItemPool(self, itempoolSize, self.ignorable_items)
        crip = [self.create_item(item.name) for item in rip]

        StillRequiredPool = [item for item in crip if item not in itempool and item not in skipitempool]
        guaranteedpool = BuildGuaranteedItemPool(self)

        filler_items = [item for item in itempool if item_dictionary[item.name].category in [DSRItemCategory.FILLER]]
        junk_items = [item for item in itempool if item.name in item_name_groups["Junk"]]
        removable_items = filler_items + junk_items

        # print(f"DSR [{self.player_name}]: stillRequiredPool: {StillRequiredPool}")

        # print("marked " + str(len(removable_items)) + " items as removable")
        # print("marked " + str(len(filler_items)) + " items as filler")
        # print("marked " + str(len(junk_items)) + " items as non filler")
        # for item in junk_items:
        #     print("junk:" + item.name)
        # print("itempool size " + str(len(itempool)) + "itempoolsize=" + str(itempoolSize))
        # print("skip_itemlocs size " + str(len(skip_itemlocs)))
        # print("rip size " + str(len(rip)))
        # print("StillRequiredPool size " + str(len(StillRequiredPool)))
        # print("disabled items " + str(len(disabled_items)))
        # for item in disabled_items:
        #     print("disabled:" + item.name)
        # for item in StillRequiredPool:
        #     print("StillRequiredPool item: " + str(item))
        # for item in skipitempool:
        #     print("skip item: " + str(item))
        # limited_pool = [item for item in StillRequiredPool if item_dictionary[item.name].category not in [DSRItemCategory.FOGWALL, DSRItemCategory.BOSSFOGWALL]]
        
        # for item in limited_pool:
        #     print("non-fogwall required item: " + str(item))

        # print(f"required pool = {StillRequiredPool}")
        replacable_filler = [
            "Soul of a Lost Undead",
            "Large Soul of a Lost Undead",
            "Soul of a Nameless Soldier",
            "Large Soul of a Nameless Soldier",
            "Soul of a Proud Knight",
            "Homeward Bone", # 11 in pool with boss bones on
        ]
        # Replace each of the above souls, in order, as needed
        if len(StillRequiredPool) + len(guaranteedpool) > len(removable_items):
            print(f"DSR [{self.player_name}]: Detected additional replacements required ({len(removable_items)}/{len(StillRequiredPool) + len(guaranteedpool)}).")
            for soul in replacable_filler:
                if (len([item for item in itempool if item.name == soul]) > 0):
                    print(f"DSR [{self.player_name}]: Adding " + str(len([item for item in itempool if item.name == soul])) + f" {soul} items to removable items.")
                    removable_items += [item for item in itempool if item.name == soul]
                    if len(StillRequiredPool) + len(guaranteedpool) <= len(removable_items):
                        break

        num_required_to_remove = len(StillRequiredPool) + len(guaranteedpool)
        num_removable = len(removable_items)
        print(f"DSR [{self.player_name}]: Now {num_removable} filler items are removable out of {num_required_to_remove} required")

        excluded_consumables = []
        if self.options.ghost_difficulty != GhostDifficulty.option_normal:
            excluded_consumables.extend(["Transient Curse x2", "Transient Curse x4"])

        consumables = [item.name for item in _all_items if item.category == DSRItemCategory.CONSUMABLE
                       and item.name not in [item2.name for item2 in removable_items]
                       and item.name not in excluded_consumables
                       ]


        if num_required_to_remove > num_removable:
            armors = [item.name for item in _all_items if item.category == DSRItemCategory.ARMOR]
            weapons = [item.name for item in _all_items if item.category == DSRItemCategory.WEAPON]
            shields = [item.name for item in _all_items if
                       item.category == DSRItemCategory.SHIELD and item.name not in ["Grass Crest Shield"]]
            upg_mats = [item.name for item in _all_items if item.category == DSRItemCategory.UPGRADE_MATERIAL]

            num_more_required = num_required_to_remove - num_removable
            print(f"DSR [{self.player_name}]: Could not remove enough Soul items to meet requirements from yaml settings...removing additional items")

            # list all the items, first
            # print("_items:")
            # print(f"{itempool}")
            # print("_req_items:")
            # print(f"{StillRequiredPool}")
            typelists = [("armor", armors, 0.6),
                         ("consumable", consumables, 0.8),
                         ("shield", shields, 0.8),
                         ("upgrade material", upg_mats, 0.9),
                         ("weapon", weapons, 0.7),
                         ]
            for i in range(5):
                if num_more_required <= 0:
                    break
                tlname = typelists[i][0]
                typelist = typelists[i][1]
                weight = typelists[i][2]
                type_removable_items = [item for item in itempool if item.name in typelist and item.name not in key_item_names and item.name not in self.options.guaranteed_items.value.keys()]
                self.random.shuffle(type_removable_items)
                num_items_to_replace = min(num_more_required, int(len(type_removable_items) * weight))  # don't replace more than weight *100 %
                print(f"DSR [{self.player_name}]: Removing {num_items_to_replace} {tlname} items from group of {len(type_removable_items)} eligible {tlname}s")
                removable_items += type_removable_items[0:num_items_to_replace]
                num_more_required -= num_items_to_replace
            # if after all of that, there still aren't enough removed, throw an error
            if num_more_required > 0:
                print(f"DSR [{self.player_name}]: ERROR: Still could not remove enough items to meet requirements from yaml settings ({len(removable_items)}/{len(StillRequiredPool) + len(guaranteedpool)}). Reduce number of \"steps\" specified.")
                raise FillError(f"DSR [{self.player_name}]: ERROR: Still could not remove enough items to meet requirements from yaml settings ({len(removable_items)}/{len(StillRequiredPool) + len(guaranteedpool)}). Reduce number of \"steps\" specified.")

        for item in removable_items:
            if len(StillRequiredPool) > 0:
                # print("removable item: " + item.name)
                itempool.remove(item)
                itempool.append(self.create_item(StillRequiredPool.pop().name))
            elif len(guaranteedpool) > 0:
                itempool.remove(item)
                itempool.append(self.create_item(guaranteedpool.pop().name))
            else:
                break

        filler_items = [item for item in itempool if item_dictionary[item.name].category in [DSRItemCategory.FILLER]]
        junk_items = [item for item in itempool if item.name in item_name_groups["Junk"]]
        removable_items = filler_items + junk_items
        # print("leftover removable items: " + str(len(removable_items)))
        # print("leftover filler items: " + str(len(filler_items)))

        # convert leftover filler into 'Soul of a Proud Knight' items (2k souls)
        for item in removable_items:
            # print("removable item: " + item.name)
            itempool.remove(item)
            itempool.append(self.create_item("Soul of a Proud Knight"))


        for item in itempool: 
            if item.name in required_skip_item_names:
                item.classification = ItemClassification.progression

        # Add regular items to itempool
        self.multiworld.itempool += itempool

        # Handle SKIP items separately
        for skip_item_loc in skip_itemlocs:
            location = skip_item_loc[1]
            location.place_locked_item(skip_item_loc[0])    
            #self.multiworld.itempool.append(skip_item)
            #print("Placing skip item: " + skip_item.name + " in location: " + location.name)
        
        #print("Final Item pool: ")
        #for item in self.multiworld.itempool:
            #print(item.name)

    def is_item_prog(self, name: str) -> bool:
        if (name in key_item_names or item_dictionary[name].category in [DSRItemCategory.EVENT,
                                                                         DSRItemCategory.KEY_ITEM,
                                                                         DSRItemCategory.FOGWALL,
                                                                         DSRItemCategory.BOSSFOGWALL]
                and name not in self.ignorable_items):
            return True
        return False

    def is_item_useful(self, name: str) -> bool:
        useful_categories = [
                DSRItemCategory.EMBER,
                DSRItemCategory.FIRE_KEEPER_SOUL,
                DSRItemCategory.PROGRESSIVE_MULTIPLIER,
                DSRItemCategory.USEFUL_KEY_ITEM,
                DSRItemCategory.USEFUL_CONSUMABLE,
            ]
        if item_dictionary[name].category in useful_categories:
            return True
        return False


    def create_item(self, name: str) -> DSRItem:


        data = self.item_name_to_id[name]

        if self.is_item_prog(name):
            item_classification = ItemClassification.progression
        elif self.is_item_useful(name):
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler
        # if (name in self.ignorable_items):
        # print(f"item {name} created as {item_classification}")
        return DSRItem(name, item_classification, data, self.player)


    def get_filler_item_name(self) -> str:
        return "Soul of a Proud Knight"
    
    def set_rules(self) -> None:           
        #print("Setting rules")   
        for region in self.multiworld.get_regions(self.player):
            for location in region.locations:
                self.set_rule(location, True_())
        match self.options.goal_condition:
            case GoalConditionOption.option_gwyn:
                self.set_completion_rule(Has("Gwyn, Lord of Cinder Defeated"))
            case GoalConditionOption.option_all_bosses:
                boss_defeated_items = [
                    item.name
                    for item in item_dictionary.values()
                    if item.category == DSRItemCategory.EVENT and "Defeated" in item.name
                    and item.name in [loc.item.name for loc in self.get_locations() if loc.player == self.player and loc.item is not None] # limit to active locations
                ]
                # Move this print to spoiler log, and add the boss list to slot data
                # print(f"--\nRequired bosses:{boss_defeated_items}\n--")

                self.set_completion_rule(HasAll(*boss_defeated_items))
                
            case GoalConditionOption.option_ornstein_and_smough:
                self.set_completion_rule(Has("Ornstein and Smough Defeated"))
            case GoalConditionOption.option_manus:
                self.set_completion_rule(Has("Manus, Father of the Abyss Defeated"))

        # Instead of setting rules for regions here, it's done on creating the connections
        
        # Set location-specific rules
        for loc in location_rules_table:
            self.set_rule(self.get_location(loc.loc_name), loc.rule)
            # print (f"Added rule for location: {loc.loc_name} -> requires {loc.rule}")

        # for debugging purposes, you may want to visualize the layout of your world. Uncomment the following code to
        # write a PlantUML diagram to the file "my_world.puml" that can help you see whether your regions and locations
        # are connected and placed as desired
        # from Utils import visualize_regions
        # visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
 
        
    def fill_slot_data(self) -> Dict[str, object]:
        slot_data: Dict[str, object] = {}
        name_to_dsr_code = {item.name: item.dsr_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_names = []
        items_upgrades = []
        items_address = []
        # for location in self.multiworld.get_filled_locations():
        #     if location.item.player == self.player:
        #         #we are the receiver of the item
        #         items_id.append(location.item.code)
        #         items_names.append(location.item.name)
        #         upgrade = UpgradeEquipment(location.item.code, self.options, self)
        #         items_upgrades.append(upgrade)
        #         items_address.append(f'{location.player}:{location.address}')

        slot_data = {
            "options": {
                # Game Options
                "goal_condition": self.options.goal_condition.current_key, # text of the option
                "guaranteed_items": self.options.guaranteed_items.value,
                "enable_deathlink": self.options.enable_deathlink.value,
                # QoL
                "can_warp_without_lordvessel": self.options.can_warp_without_lordvessel.value,
                "warp_to_all_bonfires": self.options.warp_to_all_bonfires.value,
                # Sanity
                "fogwall_sanity": self.options.fogwall_sanity.value,
                "boss_fogwall_sanity": self.options.boss_fogwall_sanity.value,
                # Difficulty
                "ghost_difficulty": self.options.ghost_difficulty.value,
                "soul_multiplier_base": self.options.soul_multiplier_base.value,
                "soul_multiplier_max": self.options.soul_multiplier_max.value,
                "soul_multiplier_steps": self.options.soul_multiplier_steps.value,
                "weight_multiplier_base": self.options.weight_multiplier_base.value,
                "weight_multiplier_min": self.options.weight_multiplier_min.value,
                "weight_multiplier_steps": self.options.weight_multiplier_steps.value,
                # Upgraded Weapons
                "incoming_weapon_upgrade_infusion_paths": self.options.incoming_weapon_upgrade_infusion_paths.value,
                "incoming_weapon_upgrade_base": self.options.incoming_weapon_upgrade_base.value,
                "incoming_weapon_upgrade_max": self.options.incoming_weapon_upgrade_max.value,
                "incoming_weapon_upgrade_steps": self.options.incoming_weapon_upgrade_steps.value,
                # Optional Region Selection
                "include_dlc": self.options.include_dlc.value,
                "include_pw": self.options.include_pw.value,
                "include_gh": self.options.include_gh.value,

                # lord soul setting
                "lord_soul_shuffle": self.options.lord_soul_shuffle.value,

                # info about which location categories are ap randomized
                "ap_loc_categories": ",".join(self.ap_loc_categories),
                "local_loc_categories": ",".join(self.local_loc_categories),

                # Shops
                "unlimited_shop_item_shuffle": self.options.unlimited_shop_item_shuffle.value,
                "limited_shop_item_shuffle": self.options.limited_shop_item_shuffle.value,
                "shop_hints": self.options.shop_hints.value,
                
                # Logic
                "logic_to_access_firelink_altar": self.options.logic_to_access_firelink_altar.current_key, # text of the option
                "logic_to_access_catacombs": self.options.logic_to_access_catacombs.current_key, # text of the option
                "logic_to_access_totg": self.options.logic_to_access_totg.current_key, # text of the option
                # Skips?
                
                # Equipment
                "randomize_starting_loadouts": self.options.randomize_starting_loadouts.value,
                "randomize_starting_gifts": self.options.randomize_starting_gifts.value,
                "require_one_handed_starting_weapons": self.options.require_one_handed_starting_weapons.value,
                "extra_starting_weapon_for_melee_classes": self.options.extra_starting_weapon_for_melee_classes.value,
                "extra_starting_shield_for_all_classes": self.options.extra_starting_shield_for_all_classes.value,
                "starting_sorcery": self.options.starting_sorcery.value,
                "starting_miracle": self.options.starting_miracle.value,
                "starting_pyromancy": self.options.starting_pyromancy.value,
                "no_weapon_requirements": self.options.no_weapon_requirements.value,
                "no_spell_stat_requirements": self.options.no_spell_stat_requirements.value,
                "no_miracle_covenant_requirements": self.options.no_miracle_covenant_requirements.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "apworld_api_version" : "0.3.0" # Manually set our apworld api level, for detecting compatibility with client
        }

        self.items_id = items_id
        self.items_names = items_names
        self.items_upgrades = items_upgrades
        self.items_address = items_address

        return slot_data
    #
    # def write_spoiler(self, spoiler_handle: TextIO) -> None:
    #     wrote_items = False
    #     if (len(self.items_upgrades) > 0):
    #         spoiler_handle.write(f"\nDSR weapon upgrades for {self.multiworld.player_name[self.player]}:\n")
    #         for i in range(len(self.items_upgrades)):
    #             if self.items_upgrades[i] == None or self.items_upgrades[i] == "":
    #                 continue
    #             spoiler_handle.write(f"\nitem {self.items_names[i]} at loc {self.items_address[i]} upgraded to {self.items_upgrades[i]}.")
    #             wrote_items = True
    #         if not wrote_items:
    #             spoiler_handle.write("\nNo items upgraded")
    #         spoiler_handle.write("\n") # Spacing

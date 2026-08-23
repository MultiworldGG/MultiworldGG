# world/dsr/__init__.py
from typing import Dict, Set, List, ClassVar, TextIO, Any, Optional

from BaseClasses import MultiWorld, Region, Item, Entrance, Tutorial, ItemClassification, Location, LocationProgressType
from Options import Toggle, OptionError, Option

from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, add_item_rule
from rule_builder.rules import Rule, True_, Has, HasAll

from .Items import DSRItem, DSRItemCategory, item_dictionary, key_item_names, item_descriptions 
from .PoolGeneration import BuildRequiredItemPool, BuildGuaranteedItemPool, UpgradeEquipment, ReplaceItem, titanite_replacements
from .Locations import DSRLocation, DSRLocationCategory, location_tables, location_dictionary, location_skip_categories, location_locked_categories
from .Groups import location_name_groups, item_name_groups
from .Options import DSROption, option_groups, GoalConditionOption
from .Rules import region_rules_table, DsrEntranceRule, location_rules_table, DsrLocationRule
from .Skips import get_all_skips


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
        "map_page_index" : map_page_index
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
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()
        self.all_excluded_locations = set()


    def generate_early(self):
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
        # End UT yamlless support
            
        # if upgrade level max < min, reverse them
        if self.options.upgraded_weapons_percentage.value > 0 and self.options.upgraded_weapons_max_level.value < self.options.upgraded_weapons_min_level.value:
            (self.options.upgraded_weapons_min_level, self.options.upgraded_weapons_max_level) = (self.options.upgraded_weapons_max_level, self.options.upgraded_weapons_min_level)

        # If % > 0 but no allowed infusion types, default to normal
        if self.options.upgraded_weapons_percentage.value > 0 and len(self.options.upgraded_weapons_allowed_infusions.value) == 0:
            self.options.upgraded_weapons_allowed_infusions.value = ['Normal']

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



        self.enabled_location_categories.add(DSRLocationCategory.EVENT)
        self.enabled_location_categories.add(DSRLocationCategory.BOSS)
        self.enabled_location_categories.add(DSRLocationCategory.ITEM_LOT)
        # self.enabled_location_categories.add(DSRLocationCategory.MISSABLE_DROP)
        self.enabled_location_categories.add(DSRLocationCategory.MIMIC_DROP)
        self.enabled_location_categories.add(DSRLocationCategory.LORD_SOUL)
        self.enabled_location_categories.add(DSRLocationCategory.BOSS_DROP)
        
        if (self.options.boss_soul_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.BOSS_SOUL)
        if (self.options.boss_humanity_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.BOSS_HUMANITY)
        if (self.options.boss_bone_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.BOSS_BONE)

        self.enabled_location_categories.add(DSRLocationCategory.BK_DROP)
        if (self.options.bk_weapon_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.BK_WEAPON)

        if (self.options.lizard_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.CRYSTAL_LIZARD)

        # self.enabled_location_categories.add(DSRLocationCategory.DOOR)
        if (self.options.fogwall_sanity.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.FOG_WALL)
        if (self.options.boss_fogwall_sanity.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.BOSS_FOG_WALL)
        # if (self.options.shop_sanity.value == True):
        if (self.options.limited_shop_item_shuffle.value == True):
            self.enabled_location_categories.add(DSRLocationCategory.SHOP_ITEM)
            # self.enabled_location_categories.add(DSRLocationCategory.MISSABLE_SHOP_ITEM)

        self.all_excluded_locations.update(self.options.exclude_locations.value)


    def create_regions(self):
        # Create Regions
        regions: Dict[str, Region] = {}
        regions["Menu"] = self.create_region("Menu", [])

        our_regions = [
            "Undead Asylum Cell",
            "Undead Asylum Cell Door",
            "Northern Undead Asylum - F2 East Door",
            "Northern Undead Asylum", 
            "Northern Undead Asylum - After Fog",
            "Northern Undead Asylum - After F2 East Door",
            "Northern Undead Asylum - Big Pilgrim Door",
            "Firelink Shrine", 
            "Upper Undead Burg - Before Fog", 
            "Upper Undead Burg - Fog", 
            "Upper Undead Burg", 
            "Upper Undead Burg - Pine Resin Chest",
            "Upper Undead Burg - Taurus Demon",
            "Upper Undead Burg - Hellkite Bridge",
            "Undead Parish - Before Fog", 
            "Undead Parish - Fog", 
            "Undead Parish", 
            "Undead Parish - Bell Gargoyles",
            "Firelink Shrine - After Undead Parish Elevator",
            "Northern Undead Asylum Second Visit",
            "Northern Undead Asylum Second Visit - F2 West Door",
            "Northern Undead Asylum Second Visit - Behind F2 West Door",
            # "Northern Undead Asylum Second Visit - Snuggly Trades",
            "Undead Burg Basement Door",
            "Lower Undead Burg", 
            "Lower Undead Burg - After Residence Key",
            "Lower Undead Burg - Capra Demon",
            "Lower Undead Burg - After Capra Demon",
            "Watchtower Basement",
            "Depths", 
            # "Depths - After Sewer Chamber Key",
            "Depths - Gaping Dragon",
            "Depths - After Gaping Dragon",
            "Depths to Blighttown Door",
            "Upper Blighttown Depths Side", 
            "Upper Blighttown VotD Side", 
            "Lower Blighttown - Fog", 
            "Lower Blighttown", 
            "Lower Blighttown - Quelaag", 
            "Lower Blighttown - After Quelaag", 
            "Valley of the Drakes", 
            "Valley of the Drakes - After Defeating Four Kings", 
            "Door between Upper New Londo and Valley of the Drakes",
            "Darkroot Basin", 
            "Darkroot Garden - Before Fog",
            "Darkroot Garden", 
            "Darkroot Garden - Behind Artorias Door", 
            "Darkroot Garden - Moonlight Butterfly",
            "Darkroot Garden - After Moonlight Butterfly",
            "The Great Hollow", 
            "Ash Lake",
            "Sen's Fortress",
            "Sen's Fortress - After First Fog",
            "Sen's Fortress - After Second Fog",
            "Sen's Fortress - After Cage Key",
            "Sen's Fortress - Iron Golem",
            "Sen's Fortress - After Iron Golem",
            "Anor Londo",
            "Anor Londo - After First Fog",
            "Anor Londo - Painting Room",
            "Anor Londo - After Second Fog",
            "Anor Londo - Ornstein and Smough",
            "Anor Londo - After Ornstein and Smough",
            "Anor Londo - Gwyndolin",
            "Anor Londo - After Gwyndolin",
            "Painted World of Ariamis",
            "Painted World of Ariamis - After Fog",
            "Painted World of Ariamis - After Annex Key",
            "Painted World of Ariamis - Crossbreed Priscilla",
            "Upper New Londo Ruins",
            "Upper New Londo Ruins - After Fog",
            "New Londo Ruins Door to the Seal",
            "Lower New Londo Ruins", 
            "The Abyss", 
            "The Abyss - After Four Kings", 
            "The Duke's Archives", 
            "The Duke's Archives - After First Seath Encounter",
            "The Duke's Archives - After Archive Tower Cell Key",
            "The Duke's Archives - After Archive Prison Extra Key",
            "The Duke's Archives - Out of Cell",
            "The Duke's Archives - After Archive Tower Giant Door Key", 
            "The Duke's Archives - Courtyard",
            "The Duke's Archives - Giant Cell", 
            "Crystal Cave", 
            "Crystal Cave - After Seath", 
            "The Duke's Archives - First Arena after Seath's Death", 
            "Demon Ruins - Early",
            "Demon Ruins - Ceaseless Discharge",
            "Demon Ruins", 
            "Demon Ruins - Demon Firesage",
            "Demon Ruins - After Demon Firesage",
            "Demon Ruins - Centipede Demon",
            "Demon Ruins Shortcut",
            "Lost Izalith", 
            "Lost Izalith - Bed of Chaos", 
            "The Catacombs", 
            "The Catacombs - Door 1",
            "The Catacombs - After Door 1",
            "The Catacombs - Pinwheel",
            "The Catacombs - After Pinwheel",
            "Tomb of the Giants", 
            "Tomb of the Giants - After White Fog", 
            "Tomb of the Giants - Behind Golden Fog Wall",
            "Tomb of the Giants - Nito",
            "Tomb of the Giants - After Nito",
            "Firelink Altar",
            "Kiln of the First Flame",
            "Kiln of the First Flame - Gwyn",
            "Sanctuary Garden", 
            "Sanctuary Garden - Sanctuary Guardian",
            "Oolacile Sanctuary", 
            "Royal Wood", 
            "Royal Wood - Artorias",
            "Royal Wood - After Hawkeye Gough",
            "Oolacile Township", 
            "Oolacile Township - Behind Light-Dispelled Walls",
            # "Oolacile Township - After Crest Key",
            "Chasm of the Abyss",
            "Chasm of the Abyss - Manus",
            # start merchants
            "Firelink Shrine - Trusty Patches",
            "Firelink Shrine - Griggs of Vinheim",
            "Firelink Shrine - Griggs of Vinheim, After Logan Leaves",
            "Firelink Shrine - Laurentius of the Great Swamp",
            "Firelink Shrine - Petrus of Thorolund",
            "Firelink Shrine - Rhea of Thorolund",
            "Firelink Shrine - Domhnall of Zena",
            # "Firelink Shrine - Domhnall of Zena - Post Iron Golem",
            # "Firelink Shrine - Domhnall of Zena - Post O+S",
            # "Firelink Shrine - Domhnall of Zena - Post Gwyndolin",
            # "Firelink Shrine - Domhnall of Zena - Post Artorias",
            "Upper Undead Burg - Male Undead Merchant",
            "Undead Parish - Andre of Astora",
            "Undead Parish - Oswald of Carim",
            "Lower Undead Burg - Female Undead Merchant",
            "Lower Blighttown - Shiva of the East",
            "Lower Blighttown - Quelana of Izalith",
            "Lower Blighttown - Eingyi",
            "Darkroot Basin - Princess Dusk",
            "Sen's Fortress - Crestfallen Merchant",
            "Anor Londo - Giant Blacksmith",
            "The Duke's Archives - Big Hat Logan",
            "Upper New Londo Ruins - Rickert of Vinheim",
            "Upper New Londo Ruins - Ingward",
            "The Catacombs - Vamos",
            "Oolacile Sanctuary - Elizabeth",
            "Royal Wood - Marvelous Chester",
            "Royal Wood - Hawkeye Gough",
            # start merchants' shared items
            "2 Merchants - Bottomless Box",
            "4 Merchants - Repairbox",
            "3 Blacksmiths - Smithboxen",
            ]
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in our_regions})
       
        # print("DSR: created " + str(self.gc) + " real and "+ str(self.bc) + " fake locations")

        # Connect Regions
        def create_connection(from_region: str, to_region: str, rule: Rule=True_()):
            self.create_entrance(regions[from_region], regions[to_region], rule)

        for region in region_rules_table.keys():
            for entrance in region_rules_table[region]:
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

            if (location.category in self.enabled_location_categories and 
                location.category not in location_skip_categories # [DSRLocationCategory.EVENT, DSRLocationCategory.DOOR]:
                and location.category not in location_locked_categories
                and not (self.options.excluded_location_behavior == "do_not_randomize" and location.name in self.all_excluded_locations)): 
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
                if (location.category in [DSRLocationCategory.MISSABLE_DROP, DSRLocationCategory.MISSABLE_SHOP_ITEM]):
                    new_location.progress_type = LocationProgressType.EXCLUDED
            # elif (location.category in self.enabled_location_categories and
            #       location.category in location_locked_categories): # DSRLocationCategory.BONFIRE_WARP
            #     self.bw = self.bw + 1
            #     default_item = location.default_item
            #     # Place bonfire warp locations statically
            #     event_item = self.create_item(default_item)
            #     new_location = DSRLocation(
            #         self.player,
            #         location.name,
            #         location.category,
            #         default_item,
            #         self.location_name_to_id[location.name],
            #         new_region
            #     )
            #     new_location.place_locked_item(event_item)
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
             or location.category in location_locked_categories): # [DSRLocationCategory.EVENT]:
                # print("Adding skip item: " + location.default_item_name + " for location: " + location.name)
                skip_itemlocs.append((citem, location))
                skipitempool.append(citem)
            elif location.category in self.enabled_location_categories:
                if self.options.excluded_location_behavior == "do_not_randomize" and location.name in self.all_excluded_locations:
                    # print("Adding skip item: " + location.default_item_name + " for location: " + location.name)
                    skip_itemlocs.append((citem, location))
                    skipitempool.append(citem)
                else:
                    #print("Adding item: " + location.default_item_name)
                    itempoolSize += 1
                    itempool.append(citem)
        
        # print("Requesting itempool size: " + str(itempoolSize))
        # foo = BuildItemPool(itempoolSize, self.options, self)
        # print("Created item pool size: " + str(len(foo)))

        # Add any Key + useful items
        rip, required_skip_item_names = BuildRequiredItemPool(self, itempoolSize)
        crip = [self.create_item(item.name) for item in rip]



        disabled_items = [loc.default_item for loc in location_dictionary.values() if loc.category not in self.enabled_location_categories]
        StillRequiredPool = [item for item in crip if item not in itempool and item not in skipitempool and item.name not in disabled_items]
        guaranteedpool = BuildGuaranteedItemPool(self)

        filler_items = [item for item in itempool if item_dictionary[item.name].category in [DSRItemCategory.FILLER]]
        junk_items = [item for item in itempool if item.name in item_name_groups["Junk"]]
        removable_items = filler_items + junk_items

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
        limited_pool = [item for item in StillRequiredPool if item_dictionary[item.name].category not in [DSRItemCategory.FOGWALL, DSRItemCategory.BOSSFOGWALL]]
        
        # for item in limited_pool:
        #     print("non-fogwall required item: " + str(item))

        # Replace "Soul of a Lost Undead" if needed
        if len(StillRequiredPool) + len(guaranteedpool) > len(removable_items):
            print("Adding " + str(len([item for item in itempool if item.name == 'Soul of a Lost Undead'])) +" Souls of a Lost Undead to removable items")
            removable_items += [item for item in itempool if item.name == 'Soul of a Lost Undead']
            print("now " + str(len(removable_items)) + " are removable")

        # Replace "Large Soul of a Lost Undead" if needed
        if len(StillRequiredPool) > len(removable_items):
            print("Adding " + str(len([item for item in itempool if item.name == 'Large Soul of a Lost Undead'])) +" Large Souls of a Lost Undead to removable items")
            removable_items += [item for item in itempool if item.name == 'Large Soul of a Lost Undead']
            print("now " + str(len(removable_items)) + " are removable")

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

        filler_items = [item for item in itempool if item_dictionary[item.name].category in [DSRItemCategory.FILLER]]
        junk_items = [item for item in itempool if item.name in item_name_groups["Junk"]]
        removable_items = filler_items + junk_items
        # print("leftover removable items: " + str(len(removable_items)))
        # print("leftover filler items: " + str(len(filler_items)))

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


    def create_item(self, name: str) -> DSRItem:
        useful_categories = [
            DSRItemCategory.EMBER,
            DSRItemCategory.FIRE_KEEPER_SOUL,
            DSRItemCategory.PROGRESSIVE_MULTIPLIER,
            DSRItemCategory.USEFUL_KEY_ITEM,
            DSRItemCategory.USEFUL_CONSUMABLE,
        ]

        data = self.item_name_to_id[name]

        if name in key_item_names or item_dictionary[name].category in [DSRItemCategory.EVENT, DSRItemCategory.KEY_ITEM, DSRItemCategory.FOGWALL, DSRItemCategory.BOSSFOGWALL]:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

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
                ]
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
        for location in self.multiworld.get_filled_locations():
            if location.item.player == self.player:
                #we are the receiver of the item
                items_id.append(location.item.code)
                items_names.append(location.item.name)
                upgrade = UpgradeEquipment(location.item.code, self.options, self)
                items_upgrades.append(upgrade)
                items_address.append(f'{location.player}:{location.address}')

        slot_data = {
            "options": {
                # Game Options
                "goal_condition": self.options.goal_condition.current_key, # text of the option
                "guaranteed_items": self.options.guaranteed_items.value,
                "enable_deathlink": self.options.enable_deathlink.value,
                # QoL
                "can_warp_without_lordvessel": self.options.can_warp_without_lordvessel.value,
                "warp_to_all_bonfires": self.options.warp_to_all_bonfires.value,
                # Difficulty
                "ghost_difficulty": self.options.ghost_difficulty.value,
                "soul_multiplier_base": self.options.soul_multiplier_base.value,
                "soul_multiplier_max": self.options.soul_multiplier_max.value,
                "soul_multiplier_steps": self.options.soul_multiplier_steps.value,
                "weight_multiplier_base": self.options.weight_multiplier_base.value,
                "weight_multiplier_min": self.options.weight_multiplier_min.value,
                "weight_multiplier_steps": self.options.weight_multiplier_steps.value,
                # Sanity
                "fogwall_sanity": self.options.fogwall_sanity.value,
                "boss_fogwall_sanity": self.options.boss_fogwall_sanity.value,
                # Shuffle
                "boss_soul_shuffle": self.options.boss_soul_shuffle.value,
                "boss_humanity_shuffle": self.options.boss_humanity_shuffle.value,
                "boss_bone_shuffle": self.options.boss_bone_shuffle.value,
                "bk_weapon_shuffle": self.options.bk_weapon_shuffle.value,
                "lizard_shuffle": self.options.lizard_shuffle.value,

                # Shops
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
                # Upgraded Weapons
                "upgraded_weapons_percentage": self.options.upgraded_weapons_percentage.value,
                "upgraded_weapons_allowed_infusions": self.options.upgraded_weapons_allowed_infusions.value,
                "upgraded_weapons_adjusted_levels": self.options.upgraded_weapons_adjusted_levels.value,
                "upgraded_weapons_min_level": self.options.upgraded_weapons_min_level.value,
                "upgraded_weapons_max_level": self.options.upgraded_weapons_max_level.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": self.base_id,  # to merge location and items lists
            "itemsId": items_id,
            "itemsUpgrades": items_upgrades,
            "itemsAddress": items_address,
            "apworld_api_version" : "0.2.5" # Manually set our apworld api level, for detecting compatibility with client
        }

        self.items_id = items_id
        self.items_names = items_names
        self.items_upgrades = items_upgrades
        self.items_address = items_address

        return slot_data

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        wrote_items = False
        if (len(self.items_upgrades) > 0):
            spoiler_handle.write(f"\nDSR weapon upgrades for {self.multiworld.player_name[self.player]}:\n")
            for i in range(len(self.items_upgrades)):
                if self.items_upgrades[i] == None or self.items_upgrades[i] == "":
                    continue
                spoiler_handle.write(f"\nitem {self.items_names[i]} at loc {self.items_address[i]} upgraded to {self.items_upgrades[i]}.")
                wrote_items = True
            if not wrote_items:
                spoiler_handle.write("\nNo items upgraded")
            spoiler_handle.write("\n") # Spacing

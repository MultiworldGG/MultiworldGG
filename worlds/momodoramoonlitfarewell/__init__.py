from .Items import MomodoraItem, item_table, skill_items, extra_skill_items, sigil_items, optional_sigil_items, grimoire_items, key_items, selin_door, progressive_upgrade_table, companion_table
from .Locations import MomodoraAdvancement, advancement_table, exclusion_table
from .Regions import momodora_regions, link_momodora_areas
from worlds.generic.Rules import exclusion_rules
from BaseClasses import Region, Entrance, Tutorial, Item, ItemClassification
from .Options import MomodoraOptions
from .Rules import set_rules, set_completion_rules
from worlds.AutoWorld import World, WebWorld
from multiprocessing import Process


class MomodoraWeb(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the Momodora Moonlit Farewell Randomizer for MultiworldGG multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["alditto"]
        )
    ]


class MomodoraWorld(World):
    """
    Momodora: Moonlit Farewell is a 2D side-scrolling Metroidvania. 
    The player controls priestess Momo Reinol as she explores an interconnected series of areas. 
    As she explores, she collects items which make her more powerful, and unlocks new abilities 
    which can be used to access different areas of the game world.
    """
    game = "Momodora Moonlit Farewell"
    options_dataclass = MomodoraOptions
    options: MomodoraOptions
    web = MomodoraWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in advancement_table.items()}
    

    def _get_momodora_data(self):
        return {
            "world_seed": self.random.getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
            "client_version": self.required_client_version,
            "race": self.multiworld.is_race,
            "OpenSpringleafPath": bool(self.options.OpenSpringleafPath.value),
            "Deathlink": bool(self.options.Deathlink.value),
            "OracleSigil": bool(self.options.OracleSigil.value),
            "Companionsanity": bool(self.options.Companionsanity.value),
            "BellHoverGeneration": bool(self.options.BellHoverGeneration.value),
            "RandomizeKeyItems": bool(self.options.RandomizeKeyItems.value),
            "SelinDoorKeysanity": bool(self.options.SelinDoorKeysanity.value),
            "Lilysanity": bool(self.options.Lilysanity.value),
            "Fairysanity": bool(self.options.Fairysanity.value),
            "Berrysanity": bool(self.options.Berrysanity.value),
            "LunarCrystalBranchShuffle": bool(self.options.LunarCrystalBranchShuffle.value),
            "VictoryCondition": self.options.VictoryCondition.current_key,
            # "fast_travel": self.options.fast_travel.current_key
        }
    
    def get_filler_item_name(self):
        return "10 Lunar Crystals"
    
    def create_items(self):
        # Generate item pool
        itempool = []
        # Add all required progression items
        for name, num in skill_items.items():
            itempool += [name] * num
        #Add useful skill items
        # if self.options.fast_travel.current_key == 2:
        for name, num in extra_skill_items["fast_travel"].items():
            itempool += [name] * num
        #Add all sigil items
        for name, num in sigil_items.items():
            itempool += [name] * num
        #Add Grimoire items
        for name, num in grimoire_items.items():
            itempool += [name] * num
        #Add Key Items
        if self.options.RandomizeKeyItems:
            for name, num in key_items.items():
                itempool += [name] * num    
       #Add Oracle Sigil if enabled
        if self.options.OracleSigil:
            item_table["Progressive Lumen Fairy"] = item_table["Progressive Lumen Fairy"]._replace(classification=ItemClassification.progression)
            for name, num in optional_sigil_items.items():
                itempool += [name] * num
        ##Add Companions
        if self.options.Companionsanity:
            for name, num in companion_table.items():
                itempool += [name] * num
        ##Add Final Boss Door if enabled
        if self.options.SelinDoorKeysanity:
            for name, num in selin_door.items():
                itempool += [name] * num

        if self.options.Lilysanity:
            for name, num in progressive_upgrade_table["progressive_damage"].items():
                itempool += [name] * num

        if self.options.Berrysanity:
            for name, num in progressive_upgrade_table["progressive_berry"].items():
                itempool += [name] * num

        if self.options.Fairysanity:
            for name, num in progressive_upgrade_table["progressive_fairy"].items():
                itempool += [name] * num

        #Choose locations to automatically exclude based on settings
        exclusion_pool = set()
        # if not self.options.RandomizeKeyItems:
        #     exclusion_pool.update(exclusion_table["random_key_items"])
        # if not self.options.OracleSigil:
        #     exclusion_pool.update(exclusion_table["OracleSigil"])

        exclusion_rules(self.multiworld, self.player, exclusion_pool)

        # Convert itempool into real items
        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        # Fill remaining items with randomly generated junk
        while len(itempool) < len(self.multiworld.get_unfilled_locations(self.player)):
            itempool.append(self.create_filler())

        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self)
        set_completion_rules(self)

    def create_regions(self):
        def MomodoraRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [MomodoraAdvancement(self.player, loc_name, loc_data.id, ret)
                              for loc_name, loc_data in advancement_table.items()
                                if loc_data.region == region_name and
                                (self.options.RandomizeKeyItems or 
                                 loc_name not in exclusion_table["random_key_items"]) and
                                 (self.options.OracleSigil or
                                  loc_name not in exclusion_table["OracleSigil"]) and
                                  (self.options.Lilysanity or
                                   loc_name not in exclusion_table["progressive_damage"]) and
                                   (self.options.Berrysanity or
                                    loc_name not in exclusion_table["progressive_berry"]) and
                                    (self.options.Fairysanity or
                                     loc_name not in exclusion_table["progressive_fairy"]) and
                                     (self.options.Companionsanity or
                                      loc_name not in exclusion_table["companions"]) and
                                      (self.options.LunarCrystalBranchShuffle or
                                       loc_name not in exclusion_table["lunar_crystal_branches"])]

            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret
        
        self.multiworld.regions += [MomodoraRegion(*r) for r in momodora_regions]
        link_momodora_areas(self.multiworld, self.player)

    def fill_slot_data(self):
        return self._get_momodora_data()
    
    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = MomodoraItem(name, item_data.classification, item_data.code, self.player)
        return item
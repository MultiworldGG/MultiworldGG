from .Regions import link_aus_areas, aus_regions
from BaseClasses import Region, Entrance, Tutorial, Item
from .Options import AUSOptions
from .Items import item_table, AUSItem, item_pool
from .Locations import base_location_table, AUSLocation, arcade_location_table, final_climb_location_table
from .Rules import AUSRules
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type
from multiprocessing import Process
from .Names import *

class AnUntitledStoryWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up the An Untitled Story randomizer for MultiworldGG.",
            "English",
            "setup_en.md",
            "setup/en",
            ["ThatOneGuy27"],
        )
    ]
class AUSWorld(World):
    """
    A freeware metroidvania game created by Maddy Thorson chronicling the travels of an adventurous egg.
    """
    game = "An Untitled Story"
    author: str = "ThatOneGuy27"
    options_dataclass = AUSOptions
    options: AUSOptions
    topology_present = False

    base_id = 72000
    web = AnUntitledStoryWeb()

    @staticmethod
    def get_location_table(options=None):
        full_location_table = {**base_location_table}
        if not options or options.arcade_mode.value != 0:
            full_location_table = {**full_location_table, **arcade_location_table}
        full_location_table = {**full_location_table, **final_climb_location_table}
        return full_location_table


    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in get_location_table().items()}

    def _get_aus_data(self):
        return {
            "world_seed": self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            "seed_name": self.multiworld.seed_name,
            "player_name": self.multiworld.get_player_name(self.player),
            "player_id": self.player,
        }

    def create_items(self):
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            for amount in range(item_pool.get(name, 1)):
                if name != VICTORY:
                    item = AUSItem(name, data.classification, data.code, self.player)
                    pool.append(item)

        if self.options.arcade_mode != 0:
            for newheart in range(3):
                item = AUSItem(I_HEART, item_table[I_HEART].classification, item_table[I_HEART].code, self.player)
                pool.append(item)
        self.multiworld.itempool += pool

    def create_regions(self):
        def AUSRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations += [AUSLocation(self.player, loc_name, loc_data.id, ret)
                             for loc_name, loc_data in AUSWorld.get_location_table(self.options).items()
                             if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [AUSRegion(*r) for r in aus_regions]
        link_aus_areas(self.multiworld, self.player)

        self.multiworld.get_location(VICTORY, self.player).place_locked_item(self.create_item(VICTORY))

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = AUSItem(name, item_data.classification, item_data.code, self.player)
        return item

    def set_rules(self) -> None:
        AUSRules(self).set_aus_rules()

    def get_filler_item_name(self) -> str:
        return self.random.choice(["10 Crystals", "25 Crystals", "35 Crystals"])
        
        
    def fill_slot_data(self) -> dict[str, object]:
        return {
            "gold_orbs_required": self.options.gold_orbs_required.value,
            "difficulty": self.options.difficulty.value,
            "arcade_mode": self.options.arcade_mode.value,
            "easy_rainbowdive": self.options.easy_rainbowdive.value,
            "disable_heart_barriers": self.options.disable_heart_barriers.value,
            "ghost_spawn_rate": self.options.ghost_spawn_rate.value,
            "special_boss_music": self.options.special_boss_music.value,
            "hard_logic": self.options.hard_logic.value,
            "closed_end_logic": self.options.closed_end_logic.value,
            "DeathLink": bool(self.options.death_link)
        }
        
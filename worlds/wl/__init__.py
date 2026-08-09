import os
import typing
import math
import settings
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import WLItem, ItemData, item_table, junk_table
from .Locations import WLLocation, all_locations, setup_locations
from .Options import WLOptions
from .Regions import create_regions, connect_regions
from .Levels import full_level_list, generate_level_list, location_id_to_level_id
from .Rules import set_rules
from worlds.generic.Rules import add_rule, exclusion_rules
from .Names import ItemName, LocationName
from worlds.AutoWorld import WebWorld, World
from .Rom import Rom, patch_rom, get_base_rom_path, WLDeltaPatch

# from Utils import visualize_regions
from Utils import __version__
from .Client import WarioLandClient


class WLSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the WL World rom"""

        description = "Wario Land ROM File"
        copy_to = "Wario Land - Super Mario Land 3 (World).gb"
        md5s = [WLDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class WLWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Wario Land randomizer connected to a MultiworldGG world.",
        "English",
        "setup_en.md",
        "setup/en",
        ["rand(0)"],
    )

    tutorials = [setup_en]


class WLWorld(World):
    # TODO: proper game description
    """
    Wario Land: Super Mario Land 3 is a 1994 platform game developed and published by Nintendo for the Game Boy.
    """
    game: str = "Wario Land"
    author: str = "rand0"
    options: WLOptions
    options_dataclass = WLOptions
    settings: typing.ClassVar[WLSettings]
    topology_present = False
    data_version = 0
    required_client_version = (0, 4, 3)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_dict: typing.Dict[int, int]
    web = WLWeb()

    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            # "death_link": self.options.death_link.value,
            "active_levels": self.active_level_dict,
        }

    """
    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in WLOptions:
            option = getattr(self.options, option_name)
            slot_data[option_name] = option.value
        return slot_data
    """

    def fill_slot_data(self) -> typing.Dict[str, typing.Any]:
        return {
            "goal": self.options.goal.value,
            "bosses_required": self.options.bosses_required.value,
            "progressive_powerup": self.options.progressive_powerup.value,
            "boss_unlocks": self.options.boss_unlocks.value,
            "world_unlocks": self.options.world_unlocks.value,
            "number_of_garlic_cloves": self.options.number_of_garlic_cloves.value,
            "percentage_of_garlic_cloves": self.options.percentage_of_garlic_cloves.value,
            "treasure_checks": self.options.treasure_checks.value,
            "blocksanity": self.options.blocksanity.value,
            "death_link": self.options.death_link.value,
            "get_previous_powerups": self.options.get_previous_powerups.value,
            # "level_shuffle": self.options.level_shuffle.value,
        }

    def create_regions(self):
        location_table = setup_locations(self.options)
        create_regions(self.multiworld, self.player, self.options, location_table)

        itempool: typing.List[WLItem] = []
        start_inventory = self.options.start_inventory.value.copy()
        self.active_level_dict = dict(
            zip(generate_level_list(self.multiworld, self.player), full_level_list)
        )
        # TODO: Implement level shuffle
        # self.topology_present = self.options.level_shuffle
        self.topology_present = 0
        connect_regions(
            self.multiworld, self.player, self.options, self.active_level_dict
        )

        totalLocations = len(location_table.items())

        if self.options.progressive_powerup:
            itempool += [
                self.create_item(ItemName.progressive_powerup) for _ in range(4)
            ]
        else:
            itempool += [self.create_item(ItemName.wario_garlic)]
            itempool += [self.create_item(ItemName.wario_bull)]
            itempool += [self.create_item(ItemName.wario_jet)]
            itempool += [self.create_item(ItemName.wario_dragon)]

        itempool += [self.create_item(ItemName.wario_climb)]
        itempool += [self.create_item(ItemName.wario_duck)]
        itempool += [self.create_item(ItemName.wario_createcoin)]
        itempool += [self.create_item(ItemName.wario_dash)]

        # Handle start with HJ
        hj = self.create_item(ItemName.wario_highjump)
        if self.options.start_with_hj:
            start_inventory[hj] = 1
            self.multiworld.push_precollected(hj)
        else:
            itempool += [hj]

        # Place the world-unlock items into the pool
        world_unlocks = [
            self.create_item(ItemName.ricebeach),
            self.create_item(ItemName.mtteapot),
            self.create_item(ItemName.stovecanyon),
            self.create_item(ItemName.parsleywoods),
            self.create_item(ItemName.ssteacup),
            self.create_item(ItemName.sherbetland),
            self.create_item(ItemName.syrupcastle),
        ]

        if self.options.world_unlocks:
            # Player always starts with a random world unlocked if there is more than one player
            # or if Blocksanity is active
            if self.multiworld.players > 1 or self.options.blocksanity == 1:
                self.multiworld.random.shuffle(world_unlocks)
                list_pick = world_unlocks.pop()
                start_inventory[list_pick] = 1
                self.multiworld.push_precollected(list_pick)
            # If there is only one player and one multiworld, a specific world unlock is forced for seed gen.
            # This is due to the fact that very few levels are accessable without items at the start
            else:
                # Parlsey Woods should be enough
                list_pick = world_unlocks.pop(3)
                start_inventory[list_pick] = 1
                self.multiworld.push_precollected(list_pick)
            for unlock in world_unlocks:
                itempool += [unlock]
        else:
            for unlock in world_unlocks:
                start_inventory[unlock.name] = 1
                self.multiworld.push_precollected(unlock)

        # Place the boss-unlock items into the pool
        boss_unlocks = [
            self.create_item(ItemName.ricebeach_bossunlock),
            self.create_item(ItemName.mtteapot_bossunlock),
            self.create_item(ItemName.stovecanyon_bossunlock),
            self.create_item(ItemName.parsleywoods_bossunlock),
            self.create_item(ItemName.ssteacup_bossunlock),
            self.create_item(ItemName.sherbetland_bossunlock),
        ]

        if self.options.boss_unlocks:
            for unlock in boss_unlocks:
                itempool += [unlock]
        else:
            for unlock in boss_unlocks:
                start_inventory[unlock.name] = 1
                self.multiworld.push_precollected(unlock)

        boss_location_names = [
            LocationName.ricebeach_boss,
            LocationName.mtteapot_boss,
            LocationName.sherbetland_boss,
            LocationName.stovecanyon_boss,
            LocationName.ssteacup_boss,
            LocationName.parsleywoods_boss,
        ]
        for location_name in boss_location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(
                self.create_item(ItemName.boss_token)
            )
            totalLocations -= 1

        if self.options.goal == "garlic_hunt":
            itempool += [
                self.create_item(ItemName.garlic_clove)
                for _ in range(self.options.number_of_garlic_cloves)
            ]
            self.multiworld.get_location(
                LocationName.garlic_goal, self.player
            ).place_locked_item(self.create_item(ItemName.victory))
            # garlic goal and removed genie location
            totalLocations -= 2
        else:
            self.multiworld.get_location(
                LocationName.syrupcastle_boss, self.player
            ).place_locked_item(self.create_item(ItemName.victory))
            totalLocations -= 1

        junk_count = totalLocations - len(itempool)
        trap_weights = []
        trap_weights += [
            ItemName.wario_grease_trap
        ] * self.options.grease_trap_weight.value
        trap_weights += [ItemName.wario_stun_trap] * self.options.stun_trap_weight.value
        trap_weights += [
            ItemName.wario_death_trap
        ] * self.options.death_trap_weight.value
        trap_weights += [
            ItemName.wario_timer_trap
        ] * self.options.timer_trap_weight.value
        trap_count = (
            0
            if (len(trap_weights) == 0)
            else math.ceil(
                junk_count * (self.options.trap_fill_percentage.value / 100.0)
            )
        )
        junk_count -= trap_count

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.multiworld.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        itempool += trap_pool

        junk_list = list(junk_table.keys())
        for _ in range(junk_count):
            junk_item = self.multiworld.random.choice(junk_list)
            itempool.append(self.create_item(junk_item))

        self.multiworld.itempool += itempool
        # visualize_regions(self.multiworld.get_region(LocationName.menu_region, self.player),"WL_Region_out.puml")

    def generate_output(self, output_directory: str):
        rompath = ""  # if variable is not declared finally clause may fail
        try:
            world = self.multiworld
            player = self.player

            rom = Rom(get_base_rom_path())
            patch_rom(self, rom)

            rompath = os.path.join(
                output_directory,
                f"{self.multiworld.get_out_file_name_base(self.player)}.gb",
            )
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = WLDeltaPatch(
                os.path.splitext(rompath)[0] + WLDeltaPatch.patch_file_ending,
                player=player,
                player_name=world.player_name[player],
                patched_path=rompath,
            )
            patch.write()
        except:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict):
        import base64

        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][
                self.multiworld.player_name[self.player]
            ]

    """
    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            world_names = [
                LocationName.ricebeach_region,
                LocationName.mtteapot_region,
                LocationName.sherbetland_region,
                LocationName.stovecanyon_region,
                LocationName.ssteacup_region,
                LocationName.parsleywoods_region,
                LocationName.syrupcastle_region,
            ]
            world_cutoffs = [
                0x07,
                0x13,
                0x1F,
                0x26,
                0x30,
                0x39,
                0x44,
                0x4F,
                0x59
            ]
            er_hint_data = {}
            for loc_name, level_data in location_id_to_level_id.items():
                level_id = level_data[0]

                if level_id not in self.active_level_dict:
                    continue

                keys_list = list(self.active_level_dict.keys())
                level_index = keys_list.index(level_id)
                for i in range(len(world_cutoffs)):
                    if level_index >= world_cutoffs[i]:
                        continue

                    if self.options.treasure_checks.value == 0 and "Treasure" in loc_name:
                        continue

                    location = self.multiworld.get_location(loc_name, self.player)
                    er_hint_data[location.address] = world_names[i]
                    break

            hint_data[self.player] = er_hint_data
    """

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif name == ItemName.garlic_clove:
            classification = ItemClassification.progression_skip_balancing
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        created_item = WLItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        junk_list = list(junk_table.keys())
        return self.multiworld.random.choice(junk_list)

    def set_rules(self):
        set_rules(self.multiworld, self.options, self.player)

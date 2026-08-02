import base64
from concurrent.futures import ThreadPoolExecutor, TimeoutError
import logging
import os
import shutil
import threading
import typing
from urllib.request import urlopen

# Imports of base Archipelago modules must be absolute.
from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Region, MultiWorld, Tutorial
from Options import OptionError
import settings
from worlds.AutoWorld import LogicMixin, WebWorld, World
from worlds.Files import APProcedurePatch
from worlds.alttpr import Sprites

# Imports of your world's files must be relative.
from .ALttPDoorRandomizer.BaseClasses import CrystalBarrier, FillError, World as DoorRandoWorld  # Avoid naming conflict with AP's World class
from .ALttPDoorRandomizer.Bosses import place_bosses
from .ALttPDoorRandomizer.source.classes.CustomSettings import CustomSettings
from .ALttPDoorRandomizer.source.enemizer.DamageTables import DamageTable
from .ALttPDoorRandomizer.source.rom.DataTables import init_data_tables
from .ALttPDoorRandomizer.source.item.District import init_districts
from .ALttPDoorRandomizer.Doors import create_doors
from .ALttPDoorRandomizer.DoorShuffle import connect_custom, link_doors, link_doors_prep
from .ALttPDoorRandomizer.Dungeons import create_dungeons
from .ALttPDoorRandomizer.source.dungeon.DungeonStitcher import GenerationException
from .ALttPDoorRandomizer.source.enemizer.Enemizer import randomize_enemies
from .ALttPDoorRandomizer.source.dungeon.EnemyList import enemy_names
from .ALttPDoorRandomizer.source.overworld.EntranceShuffle2 import link_entrances_new
from .ALttPDoorRandomizer.Fill import dungeon_tracking, fill_dungeons_restrictive, promote_dungeon_items, sell_potions, set_prize_drops
from .ALttPDoorRandomizer.source.item.FillUtil import create_item_pool_config, massage_item_pool
from .ALttPDoorRandomizer.ItemList import create_farm_locations, customize_shops, difficulties, fill_prizes, generate_itempool
from .ALttPDoorRandomizer.Items import ItemFactory
from .ALttPDoorRandomizer.KeyDoorShuffle import validate_key_placement
from .ALttPDoorRandomizer.OverworldShuffle import link_overworld
from .ALttPDoorRandomizer.OWEdges import create_owedges
from .ALttPDoorRandomizer.RaceRandom import init_race_random
from .ALttPDoorRandomizer.Regions import adjust_locations, create_regions, create_dungeon_regions, create_shops, lookup_name_to_id, mark_light_dark_world_regions
from .ALttPDoorRandomizer.Rom import apply_rom_settings, hud_format_text, patch_rom
from .ALttPDoorRandomizer.RoomData import create_rooms
from .ALttPDoorRandomizer.Rules import set_rules
from .Client import ALttPRSNIClient
from . import Items, Regions, Rules
from . import Options as alttpr_options  # rename due to a name conflict with World.options
from .Rom import ALttPRRom, JAP10HASH


logger = logging.getLogger("alttpr")

class ALttPRCollectionState(LogicMixin):
    alttpr_blocked_crystal_connections: dict[int, list[Entrance]]
    alttpr_reachable_crystal_regions: dict[int, dict[str, CrystalBarrier]]
    alttpr_stale_crystal_regions: dict[int, bool]

    def init_mixin(self, multiworld: MultiWorld):
        players = multiworld.get_game_players("The Legend of Zelda: A Link to the Past")
        self.alttpr_blocked_crystal_connections = {player: [] for player in players}
        self.alttpr_reachable_crystal_regions = {player: {} for player in players}
        self.alttpr_stale_crystal_regions = {player: True for player in players}


class ALttPRSettings(settings.Group):
    class ALttPRRomFile(settings.SNESRomPath):
        """File name of the Japanese 1.0 ALttP ROM file"""
        description = "A Link to the Past Japanese 1.0 ROM File"
        copy_to = "Zelda no Densetsu - Kamigami no Triforce (Japan).sfc"
        md5s = [JAP10HASH]

    rom_file: ALttPRRomFile = ALttPRRomFile(ALttPRRomFile.copy_to)


class ALttPRWebWorld(WebWorld):
    display_name = "The Legend of Zelda: A Link to the Past (Door Rando)"
    setup_en = Tutorial(
        "ALTTP Door Randomizer Setup Guide",
        "A guide to setting up ALTTP Door Randomizer for MultiworldGG on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["aurabot"]
    )
    tutorials = [setup_en]
    option_groups = alttpr_options.alttpr_option_groups


class ALttPRWorld(World):
    """
    This version of A Link to the Past is based on the Door Randomizer fork of ALTTPR, and brings in many new entrance randomization options 
    and many other modernizations to improve the gameplay experience.
    """

    # IMO Zelda games should start with "The Legend of Zelda", but no one else does it.
    # Be the change you want to see.
    door_rando_world = None
    game = "The Legend of Zelda: A Link to the Past"
    rom_name = None
    seed_hash = None  # This is the 5-item hash that appears on the file select screen.
    web = ALttPRWebWorld()

    options_dataclass = alttpr_options.ALttPROptions
    options: alttpr_options.ALttPROptions

    settings: typing.ClassVar[ALttPRSettings]

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    item_name_to_id = Items.item_name_to_id
    location_name_to_id = Regions.lookup_name_to_id
    item_name_groups = {
        "Bottles": {"Bottle", "Bottle (Green Potion)", "Bottle (Red Potion)", "Bottle (Blue Potion)", "Bottle (Bee)", "Bottle (Good Bee)", "Bottle (Fairy)"},
        "Ocarina": {"Ocarina", "Ocarina (Activated)"},
    }

    # There is always one region that the generator starts from & assumes you can always go back to.
    origin_region_name = "Menu"

    # We need to modify the multiworld to recognize the ALttPR ROM hash, but only after that ROM has finished generating
    finished_generating: threading.Event

    # To handle crystal switch logic, we need all possible paths to each entrance in a dungeon
    # that requires orange/blue blocks in a certain configuration.
    # This is a dict of regions to ALttPRCrystalPath, defined in Regions.py, not used here because of circular imports.
    crystal_paths = {}


    ###############################################################################
    # Generation functions.
    # All functions below are called in order from top to bottom while generating.
    ###############################################################################
    def interpret_slot_data(self, slot_data: dict[str, typing.Any]) -> None:
        # This is only called by clients such as Universal Tracker.
        # We need to pass in anything that is randomized during generation, such as
        # pendants/crystals, entrances in entrance shuffle, enemies in enemizer, etc.

        # Convert the enemy IDs to names. IDs are used in slot data to save space.
        if self.options.enemy_shuffle != "vanilla" and "enemies" in slot_data and "1" in slot_data["enemies"]:
            overworld_enemies = slot_data["enemies"]["1"]["Overworld"]
            for location_id in overworld_enemies:
                for i in overworld_enemies[location_id]:
                    enemy_kind = overworld_enemies[location_id][i]
                    overworld_enemies[location_id][i] = enemy_names[enemy_kind]
            underworld_enemies = slot_data["enemies"]["1"]["Underworld"]
            for location_id in underworld_enemies:
                for i in underworld_enemies[location_id]:
                    enemy_kind = underworld_enemies[location_id][i]
                    underworld_enemies[location_id][i] = enemy_names[enemy_kind]

        return slot_data


    def generate_early(self) -> None:
        self.seed_hash = self.random.randbytes(4)
        init_race_random(self.random)
        self.validate_options()

        # OWR sometimes fails to generate internally, before AP does anything. This is most common
        # in door rando with heavy limitations like no keysanity. Ideally generation would be guaranteed
        # to work, but that's a huge task involving rewriting the door algorithm; ain't nobody got time for that.
        # We'll use their solution, which is to keep retrying until it works. Peacemeal generation improvements
        # can be made over time.
        last_error = None
        successful_generation = False
        for i in range(0, 20):
            if successful_generation:
                break

            try:
                self.setup_randomizer()
            except (Exception, FillError, GenerationException, RuntimeError, TimeoutError) as e:
                last_error = e
                continue

            successful_generation = True

        if not successful_generation and last_error:
            raise last_error


    def create_regions(self) -> None:
        Regions.create_and_connect_regions(self)
        self.multiworld.register_indirect_condition(self.get_region("Swamp Trench 2 Pots"), self.get_entrance("Swamp Crystal Switch SE"))


    def set_rules(self) -> None:
        Rules.set_all_rules(self)


    def create_items(self) -> None:
        Items.create_all_items(self)


    def generate_basic(self):
        # This should be done in pre_fill, but Universal Tracker doesn't run pre_fill and needs to see the event items
        Items.place_pre_fill_items(self)


    # Our world class must also have a create_item function that can create any one of our items by name at any time.
    def create_item(self, name: str, classification: ItemClassification = ItemClassification.filler) -> Items.ALttPRItem:
        try:
            classification = Items.get_classification(name, self.options.door_shuffle != "vanilla" or self.options.boss_shuffle != "vanilla")
        except Exception:
            # Unknown item, should never reach here, but also shouldn't crash if we do
            pass
        return Items.create_item(self, name, classification)


    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return Items.get_random_filler_item_name(self)


    def generate_output(self, output_directory: str) -> None:
        # Now that Archipelago has placed every item, we tell the standalone randomizer where every item belongs.
        # Including creating AP items
        for location in self.multiworld.get_filled_locations(self.player):
            if location.item.player == self.player:
                dr_location = self.door_rando_world.get_location(location.name, 1)
                if dr_location.item is not None:
                    # This is a prefilled location, probably a dungeon item
                    continue

                dr_item_name = location.item.name if location.item.name not in Items.dr_ap_different_names else Items.dr_ap_different_names[location.item.name]
                dr_items = [item for item in self.door_rando_world.get_items() if item.name == dr_item_name and item.location is None]
                dr_item = dr_items[0] if dr_items else None
                if dr_item is None:
                    logger.error(f"Could not find item {location.item.name} in door rando itempool.")
                    raise Exception()
            else:
                # Using the green/blue/red clocks as placeholders for AP items.
                # TODO: Edit the base ROM to add AP items and matching sprites
                if location.item.classification & ItemClassification.progression:
                    dr_item = ItemFactory("Green Clock", 1)
                    dr_item.price = 100
                elif location.item.classification & ItemClassification.useful:
                    dr_item = ItemFactory("Blue Clock", 1)
                    dr_item.price = 50
                else:
                    dr_item = ItemFactory("Red Clock", 1)
                    dr_item.price = 20

                self.set_hint_and_credits_text(dr_item, location.item)

            self.door_rando_world.push_item(self.door_rando_world.get_location(location.name, 1), dr_item, collect=False, skip_access_check=True)

        # An extra function must be called to handle randomized items in shops
        if self.options.shopsanity.value:
            customize_shops(self.door_rando_world, 1)

        # Create hints for Saha and the Bomb Shop, if their prizes are in another world, and silver arrows
        hint_text = {}
        if self.options.prize_shuffle.value:
            for item_name in ["Crystal 5", "Crystal 6", "Green Pendant"]:
                if item_name not in self.options.start_inventory:
                    item_location = self.multiworld.find_item(item_name, self.player)
                    if item_location.player != self.player:
                        hint_text[item_name] = f"at {self.multiworld.player_name[item_location.player]}'s {item_location.name}"
        bow_locations = self.multiworld.find_item_locations("Progressive Bow", self.player)
        if any([location.player != self.player for location in bow_locations]):
            bow_location_names = [location.name if location.player == self.player else f"{self.multiworld.player_name[location.player]}'s {location.name}" for location in bow_locations]
            hint_text["Progressive Bow"] = " and ".join(bow_location_names)

        # Create a ROM patch
        rom = ALttPRRom(self.player, self.player_name, self.seed_hash)
        try:
            patch_rom(self.door_rando_world, rom, 1, 1, is_mystery=False, hint_text=hint_text)
        except RuntimeError as e:
            # TODO: We're in bad shape if this happens, because it still runs generate_output
            # But raising the exception freezes AP. Not sure what to do about errors in generate_output?
            logger.error(f"Unknown error occurred while patching the ALttPR ROM: {e}")

        # Set the ROM name with AP per-slot info, so AP can tell different LttP ROMs apart
        rom.name = bytearray(f"LTTP{self.world_version.as_simple_string().replace(".","")}_{self.player}_{self.multiworld.seed:11}", 'utf8')[:21]
        rom.name.extend([0] * (21 - len(rom.name)))
        rom.write_bytes(0x7FC0, rom.name)

        # Set AP player names in the ROM
        ROM_PLAYER_LIMIT = 255
        encoded_players = self.multiworld.players + len(self.multiworld.groups)
        for p in range(1, min(encoded_players, ROM_PLAYER_LIMIT) + 1):
            rom.write_bytes(0x195FFC + ((p - 1) * 32), hud_format_text(self.multiworld.player_name[p]))
        if encoded_players > ROM_PLAYER_LIMIT:
            rom.write_bytes(0x195FFC + ((ROM_PLAYER_LIMIT - 1) * 32), hud_format_text("Archipelago"))

        # Change settings which don't affect logic, like quickswapping
        self.apply_player_settings(rom)
        rom.write(os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.apalttpr"))
        self.rom_name = rom.name
        self.finished_generating.set()


    def fill_slot_data(self) -> dict[str, typing.Any]:
        world = self.door_rando_world
        world.settings.record_info(world)  # Bosses, medallions, and random seed (not being set)
        world.settings.record_overworld(world)
        if self.options.entrance_shuffle != "vanilla":
            world.settings.record_entrances(world)
        if self.options.door_shuffle != "vanilla":
            world.settings.record_doors(world)
        if self.options.enemy_shuffle != "vanilla":
            world.settings.record_enemies(world)
        return world.settings.world_rep


    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        # TODO: Does the hints show vanilla in crosskeys for outdoor locations?
        if self.options.entrance_shuffle == "vanilla" and self.options.door_shuffle == "vanilla":
            return

        hint_data[self.player] = {}
        for region in self.get_regions():
            if region.locations and any([location.address for location in region.locations]):
                if not region.type.is_indoors or (not region.is_in_dungeon and self.options.entrance_shuffle == "vanilla"):
                    continue

                outdoor_entrances = region.get_connecting_entrances([])
                for location in region.locations:
                    if location.address and outdoor_entrances and \
                       not (len(outdoor_entrances) == 1 and self.door_rando_world.get_entrance(outdoor_entrances[0], 1).vanilla):
                        hint_data[self.player][location.address] = ", ".join(outdoor_entrances)


    #########################################
    # Overridden Methods
    #########################################
    def collect(self, state: CollectionState, item: Item) -> bool:
        if item.advancement == ItemClassification.progression:
            state.alttpr_stale_crystal_regions[self.player] = True
        return super().collect(state, item)


    def remove(self, state: ALttPRCollectionState, item: Item) -> bool:
        if item.advancement == ItemClassification.progression:
            state.alttpr_stale_crystal_regions[self.player] = True
            state.alttpr_blocked_crystal_connections[self.player] = []
            state.alttpr_reachable_crystal_regions[self.player] = {}
        return super().remove(state, item)


    #########################################
    # Helper Functions
    #########################################
    def setup_randomizer(self):
        self.crystal_paths = {}

        # Have the Door Randomizer generate a world with all the locations, entrances, items, etc.
        # Items should not be placed except for not-fully-randomized stuff like dungeon items without keysanity,
        # or dungeon prizes. Otherwise let AP place all the items later.
        #
        # The world can create a multiworld with many players each with different options, but we only need to
        # generate for one player, hence all the "1"s everywhere.
        shuffled_doors = self.options.door_shuffle != "vanilla"
        self.door_rando_world = DoorRandoWorld(
            1, {1: "vanilla"}, {1: False}, {1: "none"}, {1: False}, {1: self.options.entrance_shuffle.current_key},
            {1: self.options.door_shuffle.current_key}, {1: "noglitches"}, {1: self.options.world_mode.current_key}, {1: "random"},
            {1: "normal"}, {1: None}, "none", "on", {1: self.options.goal.current_key},
            "balanced", {1: "locations"}, {1: True}, False, Items.default_items_dict, {1: False}, "none"
        )

        # There are sooo many fields that aren't set in the
        # door rando's world constructor :(
        self.door_rando_world.any_enemy_logic = {
            1: "none" if self.options.enemy_shuffle != "logical" else "allow_all"}
        self.door_rando_world.bigkeyshuffle = {1: "wild" if self.options.big_key_shuffle.value else "none"}
        self.door_rando_world.bombbag = {1: False}
        self.door_rando_world.boots_hint = {1: False}
        self.door_rando_world.boss_shuffle = {1: alttpr_options.boss_shuffle_string_from_option(self.options.boss_shuffle)}
        self.door_rando_world.bow_mode = {1: "progressive"}
        self.door_rando_world.compassshuffle = {1: "wild" if self.options.compass_shuffle.value else "none"}
        self.door_rando_world.crystals_needed_for_gt = {1: self.options.crystals_needed_for_ganons_tower.value}
        self.door_rando_world.crystals_needed_for_ganon = {1: self.options.crystals_needed_for_ganon.value}
        self.door_rando_world.customizer = None
        self.door_rando_world.door_type_mode = {1: self.options.door_type_shuffle.current_key}
        self.door_rando_world.dropshuffle = {1: "none" if not (self.options.key_drop_shuffle.value or shuffled_doors) else "keys"}
        self.door_rando_world.dungeon_counters = {1: self.options.dungeon_counters.current_key if not shuffled_doors else "on"}
        self.door_rando_world.enemy_shuffle = {
            1: alttpr_options.enemy_shuffle_string_from_option(self.options.enemy_shuffle)}
        self.door_rando_world.experimental = {
            1: False}  # This makes you a bunny if your spawn point is in the dark world
        self.door_rando_world.flute_mode = {1: "active" if self.options.pre_activated_flute.value else "normal"}
        self.door_rando_world.intensity = {1: 2 if not self.options.lobby_shuffle.value else 3}  # No door shuffle
        self.door_rando_world.keyshuffle = {1: "none" if not (self.options.small_key_shuffle.value or self.options.door_shuffle in ["partitioned", "crossed"]) else "wild"}
        self.door_rando_world.linked_drops = {
            1: "unset"}  # In entrance shuffle, whether dropdowns link with their matching exit is determined by the entrance setting
        self.door_rando_world.lock_aga_door_in_escape = True
        self.door_rando_world.mapshuffle = {1: "wild" if self.options.map_shuffle.value else "none"}
        self.door_rando_world.mirrorscroll = {1: self.options.mirror_scroll.value or shuffled_doors}
        self.door_rando_world.open_pyramid = {1: alttpr_options.open_pyramid_string_from_option(self.options.open_pyramid)}
        self.door_rando_world.override_bomb_check = True  # TODO: Bomb bag
        self.door_rando_world.overworld_map = {1: "default"}
        self.door_rando_world.owFluteShuffle = {1: alttpr_options.flute_shuffle_string_from_option(self.options.flute_shuffle)}
        self.door_rando_world.owFog = {1: False}
        self.door_rando_world.owKeepSimilar = {1: False}
        self.door_rando_world.owTerrain = {1: False}
        self.door_rando_world.owWhirlpoolShuffle = {1: False}
        self.door_rando_world.pottery = {1: "none" if not (self.options.key_drop_shuffle.value or shuffled_doors) else "keys"}
        self.door_rando_world.prizeshuffle = {1: "none" if not self.options.prize_shuffle.value else "wild"}
        self.door_rando_world.pseudoboots = {1: self.options.pseudoboots.value}
        self.door_rando_world.rom_seeds = {1: self.random.randint(0, 999999999)}
        self.door_rando_world.settings = CustomSettings()
        self.door_rando_world.shopsanity = {1: self.options.shopsanity.value}
        self.door_rando_world.shuffle_bonk_drops = {1: False}
        self.door_rando_world.shuffle_followers = {1: False}
        self.door_rando_world.shufflelinks = {1: self.options.shuffle_links_house.value}
        self.door_rando_world.shuffletavern = {1: self.options.shuffle_tavern.value}
        self.door_rando_world.skullwoods = {
            1: "followlinked" if self.options.zelgawoods.value else "original"}  # How to handle Skull Woods in entrance shuffle.
        self.door_rando_world.trap_door_mode = {1: "vanilla"}
        self.door_rando_world.treasure_hunt_count = {1: self.options.triforce_hunt_goal.value}
        self.door_rando_world.treasure_hunt_total = {1: self.options.triforce_hunt_total.value}

        self.door_rando_world.player_names = {}
        for player_id, player_name in self.multiworld.player_name.items():
            self.door_rando_world.player_names[player_id] = {1: player_name}

        self.door_rando_world.finish_init()
        self.finished_generating = threading.Event()
        self.door_rando_world.difficulty_requirements = {1: difficulties[self.door_rando_world.difficulty[1]]}

        for item_name, item_count in self.options.start_inventory.value.items():
            for i in range(0, item_count):
                door_rando_item = ItemFactory(item_name, 1)
                self.door_rando_world.push_precollected(door_rando_item)

        # This will let us export information needed by Universal Tracker, such as randomized entrances, doors, medallions, etc.
        class WorldSettings:
            race = False
            notes = ""

        if (hasattr(self.multiworld, "re_gen_passthrough") and self.game in self.multiworld.re_gen_passthrough) or self.options.test_slot_data:
            slot_data = self.options.test_slot_data if self.options.test_slot_data else self.multiworld.re_gen_passthrough[self.game]
            # All the 1's (representing the player) get converted to "1"'s when it's sent as slot data
            for key in slot_data.keys():
                if "1" in slot_data[key]:
                    slot_data[key][1] = slot_data[key]["1"]
                    del slot_data[key]["1"]
            self.door_rando_world.customizer = CustomSettings()
            self.door_rando_world.customizer.file_source = slot_data
        self.door_rando_world.settings = CustomSettings()
        self.door_rando_world.settings.create_from_world(self.door_rando_world, WorldSettings())

        create_regions(self.door_rando_world, 1)
        create_dungeon_regions(self.door_rando_world, 1)
        create_owedges(self.door_rando_world, 1)
        create_shops(self.door_rando_world, 1)
        create_doors(self.door_rando_world, 1)
        create_rooms(self.door_rando_world, 1)  # Not sure if this is needed or what it does?
        create_dungeons(self.door_rando_world, 1)
        self.door_rando_world.damage_table[1] = DamageTable()
        self.door_rando_world.data_tables[1] = init_data_tables(self.door_rando_world, 1)
        place_bosses(self.door_rando_world, 1)
        randomize_enemies(self.door_rando_world, 1)
        adjust_locations(self.door_rando_world, 1)
        link_overworld(self.door_rando_world, 1)
        mark_light_dark_world_regions(self.door_rando_world, 1)
        init_districts(self.door_rando_world)
        link_entrances_new(self.door_rando_world, 1)
        link_doors_prep(self.door_rando_world, 1)
        create_item_pool_config(self.door_rando_world)
        link_doors(self.door_rando_world, 1)
        mark_light_dark_world_regions(self.door_rando_world,
                                      1)  # This is run twice in OWR Main.py, not sure why but for now I'll do the same.
        self.door_rando_world.get_region("Menu",
                                         1).is_light_world = self.options.world_mode != "inverted"  # Never start as a bunny
        self.door_rando_world.get_region("Menu", 1).is_dark_world = self.options.world_mode == "inverted"
        set_prize_drops(self.door_rando_world, 1)
        create_farm_locations(self.door_rando_world, 1)
        generate_itempool(self.door_rando_world, 1)
        set_rules(self.door_rando_world, 1)
        dungeon_tracking(self.door_rando_world)

        if self.options.shopsanity.value:
            sell_potions(self.door_rando_world, 1)
            # Red Potions and Bees make sense as an item to purchase, but not as a random item to receive.
            # Usually they turn into rupees upon receiving them from another player, which is confusing.
            for item in self.door_rando_world.get_items():
                if item.name == "Bee" or (item.name == "Red Potion" and not item.priority):
                    self.door_rando_world.itempool.remove(item)
                    self.door_rando_world.itempool.append(ItemFactory("Rupees (20)", 1))

        massage_item_pool(self.door_rando_world)
        fill_prizes(self.door_rando_world)
        shuffled_locations = self.door_rando_world.get_unfilled_locations()
        self.random.shuffle(
            shuffled_locations)  # Make sure we use AP's random() features so that it generates consistently.
        fill_dungeons_restrictive(self.door_rando_world, shuffled_locations)

        for key_layout in self.door_rando_world.key_layout[1].values():
            if not validate_key_placement(key_layout, self.door_rando_world, 1):
                raise RuntimeError("Key placements are invalid.")


    def set_hint_and_credits_text(self, dr_item, ap_item):
        # Set the text for hints and end credits for AP items.
        # Setting a maximum length for each text. If the total text is too long, we'll get an exception while patching,
        # although we have ~14 KB of room for more text before that happens.
        # The bigger restriction is that the credits can only display 32 characters at a time
        item_name = ap_item.name
        if ap_item.classification == ItemClassification.progression:
            short_item_name = "Progressive Item"
        elif ap_item.classification == ItemClassification.useful:
            short_item_name = "Useful Item"
        else:
            short_item_name = "Filler Item"

        dr_item.fluteboy_credit_text = f"{item_name if len(item_name) <= 20 else short_item_name} boy returns"
        dr_item.hint_text = f"a {item_name}"
        dr_item.magicshop_credit_text = f"shrooms for {item_name if len(item_name) <= 20 else short_item_name}"
        dr_item.pedestal_credit_text = f"and the {item_name if len(item_name) <= 24 else short_item_name}"
        dr_item.pedestal_hint_text = f"{self.multiworld.player_name[ap_item.player]}'s\n{item_name}!"
        dr_item.sickkid_credit_text = f"{item_name if len(item_name) <= 28 else short_item_name} kid"
        dr_item.zora_credit_text = f"{item_name if len(item_name) <= 23 else short_item_name} for sale"


    def apply_player_settings(self, rom):
        ow_palettes = "default"
        quickswap = True
        reduce_flashing = True
        shuffle_sfx = False
        shuffle_sfxinstruments = False
        shuffle_songinstruments = False
        triforce_gfx = None
        uw_palettes = "default"

        apply_rom_settings(rom, alttpr_options.heart_beep_rate_string_from_option(self.options.heart_beep_rate),
                           self.options.heart_color.current_key, quickswap, self.options.fast_menu.current_key,
                           self.options.disable_music.value, self.get_sprite_file(), triforce_gfx, ow_palettes,
                           uw_palettes, reduce_flashing, shuffle_sfx, shuffle_sfxinstruments,
                           shuffle_songinstruments, self.options.msu_resume.value)


    def get_sprite_file(self) -> str | None:
        sprite_name = self.options.sprite.value.lower()
        if sprite_name == "link":
            return None
        if not sprite_name in Sprites.sprites:
            # This should never happen because validate_options also checks this, but better safe than sorry.
            logger.error(f"Invalid sprite option {self.options.sprite.value}. No custom sprite will be applied.")
            return None

        world_dir = os.path.dirname(self.zip_path) if self.zip_path else os.path.join(os.path.dirname(self.__file__), "..")
        sprite_dir = os.path.join(world_dir, "..", "data", "sprites", "alttp", "remote")
        if not os.path.exists(sprite_dir):
            logger.warning(f"Sprite directory {sprite_dir} does not exist. No custom sprite will be applied.")
            return None

        sprite_file = os.path.join(sprite_dir, Sprites.sprites[sprite_name]["filename"])
        if not os.path.exists(sprite_file):
            # TODO: Do this asynchronously
            try:
                with urlopen(Sprites.sprites[sprite_name]["url"], timeout=10) as response, open(sprite_file, "wb") as out:
                    shutil.copyfileobj(response, out)
            except Exception as e:
                logger.error(f"Could not download sprite {sprite_name} from {Sprites.sprites[sprite_name]['url']}: {e}. No custom sprite will be applied.")
                return None

        return sprite_file


    def modify_multidata(self, multidata: dict):
        self.finished_generating.wait()
        if self.rom_name:
            # SNIClient connects to the AP server using an encoded ROM filename, instead of the player's name, for some reason.
            # This tells the AP server to associate the ROM filename with our player's name.
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]
        else:
            logger.error("ROM name is not set, cannot make needed multiworld changes in modify_multidata()")


    def is_excluded_key_drop_location(self, location):
        return self.door_rando_world.dropshuffle[1] == "none" and ("Key Drop" in location.name or "Pot Key" in location.name)


    def validate_options(self) -> None:
        errors = []

        if self.options.goal in ["triforcehunt", "ganonhunt", "trinity"] and self.options.triforce_hunt_goal.value > self.options.triforce_hunt_total.value:
            errors.append("Triforce Hunt Goal cannot be greater than Triforce Hunt Total.")

        sprite = self.options.sprite.value.lower()
        if sprite != "link" and sprite not in Sprites.sprites:
            errors.append(f"{self.options.sprite.value} is not a valid sprite.")

        start_inventory = self.options.start_inventory.value.keys()
        if "Ocarina" in start_inventory and (self.options.pre_activated_flute or self.options.world_mode == "inverted"):
            self.options.start_inventory.value["Ocarina (Activated)"] = 1
            del self.options.start_inventory.value["Ocarina"]
        always_invalid_starting_items = ["Triforce Piece", "Green Clock", "Blue Clock", "Red Clock"]
        always_invalid_starting_items.extend([item for item in Items.progressive_items if item.startswith("Small Key")])
        invalid_items = []
        for item in start_inventory:
            if item in always_invalid_starting_items or item not in self.item_name_to_id:
                invalid_items.append(item)
        if len(invalid_items) > 0:
            errors.append("The following items are not allowed in the starting inventory: " + ", ".join(invalid_items))

        if self.options.world_mode == "standard" and self.options.door_shuffle != "vanilla":
            errors.append("Standard world mode is not allowed with door shuffle.")

        if len(errors) > 0:
            raise OptionError("\n".join(errors))


    def check_option(self, option_name: str, valid_values: list[str | int], errors: list[str]) -> None:
        if not getattr(self.options, option_name) in valid_values:
            errors.append(f"Invalid value for option {option_name}: {getattr(self.options, option_name)}")
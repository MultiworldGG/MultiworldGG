import binascii
import dataclasses
import os
import typing
import struct
import random
import logging
import settings
import Utils
from BaseClasses import CollectionState, Entrance, Item, ItemClassification, Location, Tutorial
from Fill import fill_restrictive
from worlds.AutoWorld import WebWorld, World
from worlds.LauncherComponents import Component, components, SuffixIdentifier, Type, launch, icon_paths
from worlds.generic.Rules import forbid_item
from .Common import *
from .ForeignItemIcons import ForeignItemIconMatcher
from .Items import (LinksAwakeningItem, ladxr_to_ap_item_name, ap_to_ladxr_item_name, links_awakening_items,
    links_awakening_items_by_name, links_awakening_item_name_groups,
    item_prefixes_to_skip_text_in_prefill, start_items_to_block_by_prefix, rupees)
from .LADXR.itempool import DEFAULT_ITEM_POOL, ItemPool as LADXRItemPool
from .LADXR.locations.instrument import Instrument
from .LADXR.locations.itemInfo import ItemInfo as LADXRItemInfo
from .LADXR.locations.chest import Chest as LADXRChest
from .LADXR.locations.droppedKey import DroppedKey as LADXRDroppedKey
from .LADXR.logic import Logic as LADXRLogic
from .LADXR.settings import Settings as LADXRSettings
from .LADXR.worldSetup import WorldSetup as LADXRWorldSetup
from .LADXR.hints import generate_hint_texts
from .Locations import (LinksAwakeningLocation, LinksAwakeningRegion, create_regions_from_ladxr,
    links_awakening_location_name_to_id, links_awakening_location_name_groups, dungeon_info)
from .Options import (DungeonItemShuffle, ShuffleInstruments, LinksAwakeningOptions, ladx_option_groups,
    convert_ap_options_to_ladxr)
from .Rom import LADXProcedurePatch, write_patch_data

DEVELOPER_MODE = False
TEST_PATCH = False

logger = logging.getLogger("Link's Awakening Logger")

def launch_client(*args):
    from .LinksAwakeningClient import launch as ladx_launch
    launch(ladx_launch, name=f"{LINKS_AWAKENING} Client", args=args)

components.append(Component(
    f"{LINKS_AWAKENING} Client",
    func=launch_client,
    component_type=Type.CLIENT,
    icon=LINKS_AWAKENING,
    file_identifier=SuffixIdentifier('.apladxb')))

icon_paths[LINKS_AWAKENING] = "ap:worlds.ladx_beta/assets/MarinV-3_small.png"


class LinksAwakeningSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the Link's Awakening DX rom"""
        copy_to = "Legend of Zelda, The - Link's Awakening DX (USA, Europe) (SGB Enhanced).gbc"
        description = "LADX ROM File"
        md5s = [LADXProcedurePatch.hash]

        @classmethod
        def validate(cls, path: str) -> None:
            try:
                super().validate(path)
            except ValueError:
                Utils.messagebox(
                    "Error",
                    "Provided rom does not match hash for English 1.0/revision-0 of Link's Awakening DX",
                    True)
                raise

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching)
                    true  for operating system default program
        Alternatively, a path to a program to open the .gbc file with
        Examples:
           Retroarch:
        rom_start: "C:/RetroArch-Win64/retroarch.exe -L sameboy"
           BizHawk:
        rom_start: "C:/BizHawk-2.9-win-x64/EmuHawk.exe --lua=data/lua/connector_ladx_bizhawk.lua"
        """

    class RetroarchHost(str):
        """Address and port of Retroarch connection"""

    class DisplayMsgs(settings.Bool):
        """Display message inside of Bizhawk"""

    class OptionOverrides(str):
        """
        Provided options will be used as overrides when patching.
        Aesthetic/QoL settings with no logic implications can be overriden. Some overrides are disabled for races.
        Example:
        option_overrides: { palette: { normal: 50, inverted: 50}, boots_controls: bracelet }
        """

    class GfxModFile(settings.FilePath):
        """
        Gfxmod file, select one from the `Archipelago/data/sprites/ladx/` folder,
        or make your own. You can generate a template here: https://ladx-gfx.3and3.dev/
        Only .bin or .bdiff files.
        Extended spritesheets from the upstream randomizer are not supported.
        """
        def browse(self, filetypes=None, **kwargs):
            filetypes = [("Binary / Patch files", [".bin", ".bdiff"])]
            return super().browse(filetypes=filetypes, **kwargs)

        @classmethod
        def validate(cls, path: str) -> None:
            with open(path, "rb", buffering=0) as f:
                header, size = struct.unpack("<II", f.read()[:8])
                if path.endswith('.bin') and header == 0xDEADBEEF and size < 1024:
                    # detect extended spritesheets from upstream ladxr
                    Utils.messagebox(
                        "Error",
                        "Extended sprite sheets are not supported. Try again with a different gfxmod file, "
                        "or provide no file to continue without modifying graphics.",
                        True)
                    raise ValueError("Provided gfxmod file is an extended sheet, which is not supported")

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True
    retroarch_host: RetroarchHost = RetroarchHost('127.0.0.1:55355')
    gfx_mod_file: GfxModFile = GfxModFile()

class LinksAwakeningWebWorld(WebWorld):
    display_name = "The Legend of Zelda: Link's Awakening DX (Beta)"
    custom_wiki_link_key = "Link's_Awakening_DX"
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Links Awakening DX for MultiWorld.",
            "English",
            "setup_en.md",
            "setup/en",
            ["zig"]),
        Tutorial(
            "Entrance/Boss/Miniboss Plando Guide",
            "Vanilla mappings for each and some tips.",
            "English",
            "plando_en.md",
            "plando/en",
            ["threeandthree"]),
        Tutorial(
            "Location Count Guide",
            "Details on how options change the location count.",
            "English",
            "location_counts_en.md",
            "location_counts/en",
            ["threeandthree"])
    ]
    theme = "ocean"
    option_groups = ladx_option_groups
    options_presets: typing.Dict[str, typing.Dict[str, typing.Any]] = {
        "Beginner": {
            "expand_start": "high",
            "logic": "casual",
            "goal": "seashells",
            "warps": "improved_additional",
            "overworld": "open_mabe",
            "shuffle_maps": "start_inventory",
            "shuffle_compasses": "start_inventory",
            "shuffle_stone_beaks": "start_inventory",
            "reserve_filler": 16,
            "filler_pool": {
                "Seashell": 8,
                "Medicine": 4,
                "Fairy": 4, 
            },
        },
        "Keysanity": {
            "shuffle_nightmare_keys": "any_world",
            "shuffle_small_keys": "any_world",
            "shuffle_maps": "any_world",
            "shuffle_compasses": "any_world",
            "shuffle_stone_beaks": "any_world",
            "in_game_hint_item_groups": {
                "Entrance Keys",
                "Equipment",
                "Nightmare Keys",
            },
        },
        "4 Specific": {
            "goal": "specific",
            "specific_optional_dungeons": "condense_and_exclude",
            "instrument_count": 4,
        },
        "Boss Rush": {
            "overworld": "dungeon_dive",
            "condense_dungeons": [
                "Color Dungeon",
                "Tail Cave",
                "Bottle Grotto",
                "Key Cavern",
                "Angler's Tunnel",
                "Catfish's Maw",
                "Face Shrine",
                "Eagle's Tower",
                "Turtle Rock",
            ]
        },
        "Shuffle Everything": {
            "expand_start": "disabled",
            "warps": "improved_additional",
            "shuffle_instruments": "any_world",
            "shuffle_nightmare_keys": "any_world",
            "shuffle_small_keys": "any_world",
            "shuffle_maps": "any_world",
            "shuffle_compasses": "any_world",
            "shuffle_stone_beaks": "any_world",
            "owlsanity": "both",
            "in_game_hint_item_groups": [ "Equipment" ],
            "filler_pool": {
                "Bombs": 10,
                "Single Arrow": 5,
                "10 Arrows": 10,
                "Magic Powder": 10,
                "Medicine": 1,
                "Cucco Party": 1,
                "Slime Storm": 5,
                "Bomb Drop": 5,
                "Zol Attack": 10,
                "Fairy": 5,
            },
            "entrance_rules": "wild",
            "shuffle_start": "global",
            "shuffle_dungeons": "global",
            "shuffle_basic": "global",
            "shuffle_junk": "global",
            "shuffle_connectors": "global",
            "shuffle_water": "global",
            "shuffle_annoying": "global",
            "boss_shuffle": "shuffle",
            "miniboss_shuffle": "shuffle",
            "enemizer": "overworld",
        }
    }

class LinksAwakeningWorld(World):
    """
    After a previous adventure, Link is stranded on Koholint Island, full of mystery and familiar faces.
    Gather the 8 Instruments of the Sirens to wake the Wind Fish, so that Link can go home!
    """
    game = LINKS_AWAKENING  # name of the game/world
    web = LinksAwakeningWebWorld()

    options_dataclass = LinksAwakeningOptions
    options: LinksAwakeningOptions
    settings: typing.ClassVar[LinksAwakeningSettings]
    topology_present = True  # show path to required location checks in spoiler
    ut_can_gen_without_yaml = True

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a propery.
    base_id = BASE_ID
    # Instead of dynamic numbering, IDs could be part of data.

    # The following two dicts are required for the generation to know which
    # items exist. They could be generated from json or something else. They can
    # include events, but don't have to since events will be placed manually.
    item_name_to_id = { item.item_name: BASE_ID + item.item_id for item in links_awakening_items }

    item_name_to_data = links_awakening_items_by_name

    location_name_to_id = links_awakening_location_name_to_id

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = links_awakening_item_name_groups
    location_name_groups = links_awakening_location_name_groups

    prefill_dungeon_items = None

    ladxr_settings: LADXRSettings
    ladxr_world_setup: LADXRWorldSetup
    ladxr_logic: LADXRLogic

    ladx_in_game_hints: dict

    filler_choices: list[str]
    filler_weights: list[int]

    multi_key: bytearray


    def generate_early(self) -> None:
        self.filler_choices = list(self.options.filler_pool.keys())
        self.filler_weights = list(self.options.filler_pool.values())

        self.ladxr_world_setup = LADXRWorldSetup()
        self.ladxr_world_setup.reserve_filler = self.options.reserve_filler.value

        # make some option corrections for dungeon dive
        if self.options.overworld == "dungeon_dive":
            self.options.tradequest.value = False
            if self.options.goal == "seashells":
                self.options.goal.set_to("instruments")
                logger.warning("Switched goal to instruments. Seashell goal can't be used with dungeon dive.")
            if self.options.owlsanity == "both":
                self.options.owlsanity.set_to("dungeon")
            elif self.options.owlsanity == "overworld":
                self.options.owlsanity.set_to("none")

        # discern our initial condensed and exluded dungeon lists
        for d in dungeon_info:
            if links_awakening_location_name_groups[d.name] <= self.options.exclude_locations.value:
                self.ladxr_world_setup.excluded_dungeons.append(d.index)
            if d.name in self.options.condense_dungeons.value or d.index in self.ladxr_world_setup.excluded_dungeons:
                self.ladxr_world_setup.condensed_dungeons.append(d.index)

        # instrument count corrections
        if self.options.shuffle_instruments.is_in_original_dungeon():
            available_instruments = sum(1 for d in dungeon_info
                if d.instrument and d.index not in self.ladxr_world_setup.excluded_dungeons)
            self.options.instrument_count.set_min(available_instruments)
        if self.options.goal == "specific" and self.options.instrument_count % 8 == 0: # 0 or 8
            self.options.goal.set_to("instruments")

        self.dungeon_item_types = {}
        for dungeon_item_type in ["maps", "compasses", "small_keys", "nightmare_keys", "stone_beaks", "instruments"]:
            option_name = "shuffle_" + dungeon_item_type
            option: DungeonItemShuffle = getattr(self.options, option_name)

            self.dungeon_item_types[option.ladxr_item] = option.value

            # The color dungeon does not contain an instrument
            num_dungeons = 8 if dungeon_item_type == "instruments" else 9

            # For any and different world, set item rule instead
            if option.value == option.option_own_world:
                self.options.local_items.value |= {
                    ladxr_to_ap_item_name[f"{option.ladxr_item}{i}"] for i in range(1, num_dungeons + 1)}
            elif option.value == option.option_different_world:
                self.options.non_local_items.value |= {
                    ladxr_to_ap_item_name[f"{option.ladxr_item}{i}"] for i in range(1, num_dungeons + 1)}
            elif dungeon_item_type != 'instruments' and option == 'start_inventory':
                for dungeon_index in range(1, num_dungeons + 1):
                    ladxr_item = f"{option.ladxr_item}{dungeon_index}"
                    self.options.start_inventory_from_pool.value.update({
                        ladxr_to_ap_item_name[ladxr_item]: DEFAULT_ITEM_POOL[ladxr_item]
                    })


    def create_regions(self) -> None:
        is_ut_regen = False
        if getattr(self.multiworld, "generation_is_fake", False):
            re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
            if re_gen_passthrough and self.game in re_gen_passthrough:
                is_ut_regen = True
                ut_slot_data: dict[str, typing.Any] = re_gen_passthrough[self.game]

        if is_ut_regen:
            self.ladxr_settings_dict = ut_slot_data["ladxr_settings"]
        else:
            self.ladxr_settings_dict = convert_ap_options_to_ladxr(self.options)
        self.ladxr_settings = LADXRSettings(self.ladxr_settings_dict)

        entrance_plando = {}
        boss_plando = {}
        miniboss_plando = {}
        if self.multiworld.plando_options & self.multiworld.plando_options.connections:
            entrance_plando = self.options.entrance_plando.value
        if self.multiworld.plando_options & self.multiworld.plando_options.bosses:
            boss_plando = {int(k): boss_to_dungeon_index[v] for k, v in self.options.boss_plando.value.items()}
            miniboss_plando = self.options.miniboss_plando.value

        if self.options.world_setup_seed.value:
            rnd = random.Random(f'{self.options.world_setup_seed.value}{self.multiworld.seed}')
        else:
            rnd = self.random

        # use mapping from slot data for universal tracker gens
        if is_ut_regen:
            self.ladxr_world_setup.goal = ut_slot_data["world_setup_goal"]
            self.ladxr_world_setup.entrance_mapping = ut_slot_data["entrance_mapping"]
            self.ladxr_world_setup.boss_mapping = ut_slot_data["boss_mapping"]
            self.ladxr_world_setup.miniboss_mapping = ut_slot_data["miniboss_mapping"]
            self.ladxr_world_setup.condensed_dungeons = ut_slot_data["condensed_dungeons"]
            self.ladxr_world_setup.excluded_dungeons = ut_slot_data["excluded_dungeons"]

        # handle start_inventory_from_pool ourselves since our item pool dynamically removes items
        # we would rather remove less stuff from our default item pool than create more filler
        precollected = {ap_to_ladxr_item_name[k]: v for k, v in self.options.start_inventory_from_pool.value.items()}
        
        # for universal tracker, just create the itempool for world_setup because we've already
        # fed in the other results
        if is_ut_regen:
            self.ladxr_world_setup.itempool = LADXRItemPool(
                self.ladxr_world_setup, self.ladxr_settings, precollected)
        else:
            self.ladxr_world_setup.randomize(
                self.ladxr_settings, rnd, entrance_plando, boss_plando, miniboss_plando, precollected)
        # when the itempool was created, precollected items were removed and the precollected dict
        # was updated with counts of what was actually in the pool
        # so now we empty sifp and push precollected ourselves
        self.options.start_inventory_from_pool.value = {}
        for name, amount in precollected.items():
            self.push_precollected(self.create_item(name))

        self.ladxr_logic = LADXRLogic(configuration_options=self.ladxr_settings, world_setup=self.ladxr_world_setup)

        regions = create_regions_from_ladxr(self.player, self.multiworld, self.ladxr_logic, self.ladxr_settings)
        self.multiworld.regions += regions

        # Connect Menu -> Start
        start = next(region for region in regions if region.name == "Start House")
        menu_region = LinksAwakeningRegion("Menu", None, "Menu", self.player, self.multiworld)
        menu_region.exits = [Entrance(self.player, "Start Game", menu_region)]
        menu_region.exits[0].connect(start)

        self.multiworld.regions.append(menu_region)

        assert self.ladxr_world_setup.itempool.count() == len(self.multiworld.get_locations(self.player)), \
            f"{self.ladxr_world_setup.itempool.count() - len(self.multiworld.get_locations(self.player))} too many items"

        # Place RAFT, other access events
        for region in regions:
            for loc in region.locations:
                if loc.address is None:
                    loc.place_locked_item(self.create_event(loc.ladxr_item.event))

        # Connect Windfish -> Victory
        windfish = self.multiworld.get_region("Windfish", self.player)
        l = Location(self.player, "Windfish", parent=windfish)
        windfish.locations = [l]

        l.place_locked_item(self.create_event("An Alarm Clock"))

        self.multiworld.completion_condition[self.player] = lambda state: state.has("An Alarm Clock", player=self.player)

    def get_filler_item_name(self) -> str:
        if getattr(self, 'filler_choices', None):
            return self.random.choices(self.filler_choices, self.filler_weights)[0]
        else:
            return 'Nothing'

    def create_item(self, item_name: str):
        item_name = ladxr_to_ap_item_name.get(item_name, item_name)
        return LinksAwakeningItem(links_awakening_items_by_name[item_name], self, self.player)

    def create_event(self, event: str):
        return Item(event, ItemClassification.progression, None, self.player)

    def create_items(self) -> None:
        itempool = []

        self.prefill_original_dungeon = [ [], [], [], [], [], [], [], [], [] ]
        self.prefill_own_dungeons = []
        self.pre_fill_items = []
        # option_original_dungeon = 0
        # option_own_dungeons = 1
        # option_own_world = 2
        # option_any_world = 3
        # option_different_world = 4
        # option_delete = 5

        for ladx_item_name, count in self.ladxr_world_setup.itempool.toDict().items():
            if ladx_item_name == 'FILLER':
                for _ in range(count):
                    itempool.append(self.create_filler())
            # event
            if ladx_item_name not in ladxr_to_ap_item_name:
                continue
            item_name = ladxr_to_ap_item_name[ladx_item_name]
            for _ in range(count):
                item = self.create_item(item_name)

                if item.item_data.dungeon_item_type:
                    item_type = item.item_data.ladxr_id[:-1]
                    shuffle_type = self.dungeon_item_types[item_type]

                    if(item.item_data.dungeon_item_type == 'INSTRUMENT' and
                        shuffle_type == ShuffleInstruments.option_vanilla):
                        d_info = dungeon_info[item.item_data.dungeon_index%9]
                        loc = self.multiworld.get_location(f"{d_info.instrument} ({d_info.name})", self.player)
                        loc.place_locked_item(item)
                    else:
                        if shuffle_type == DungeonItemShuffle.option_original_dungeon:
                            self.prefill_original_dungeon[item.item_data.dungeon_index - 1].append(item)
                            self.pre_fill_items.append(item)
                        elif shuffle_type == DungeonItemShuffle.option_own_dungeons:
                            self.prefill_own_dungeons.append(item)
                            self.pre_fill_items.append(item)
                        else:
                            itempool.append(item)
                else:
                    itempool.append(item)

        self.multi_key = self.generate_multi_key()
       
        self.dungeon_locations_by_dungeon = [[], [], [], [], [], [], [], [], []]     
        for r in self.multiworld.get_regions(self.player):
            # Set aside dungeon locations
            if r.dungeon_index:
                dungeon_excluded = r.dungeon_index in self.ladxr_world_setup.excluded_dungeons
                if dungeon_excluded:
                    self.options.exclude_locations.value |= {l.name for l in r.locations}
                else:
                    self.dungeon_locations_by_dungeon[r.dungeon_index - 1] += [l for l in r.locations if not l.item]
                for location in r.locations:
                    # testing if we still need this
                    #
                    # Don't place dungeon items on pit button chest, to reduce chance of the filler blowing up
                    # TODO: no need for this if small key shuffle
                    #if location.name == "Pit Button Chest (Tail Cave)" or location.item:
                    #    self.dungeon_locations_by_dungeon[r.dungeon_index - 1].remove(location)
                    # Properly fill locations within dungeon
                    location.dungeon = r.dungeon_index

        self.local_front_fill(itempool, int(self.options.expand_start))

        self.multiworld.itempool += itempool

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]) -> None:
        dungeon_name_to_inside = {d.name: f'{d.entrance}:inside' for d in dungeon_info}
        hint_data[self.player] = {}
        for location in self.multiworld.get_locations(self.player):
            if not location.item or location.is_event:
                continue
            area = location.ladxr_item.metadata.area
            if area not in dungeon_name_to_inside:
                continue
            target = dungeon_name_to_inside[area]
            entrances = [en for en, ex in self.ladxr_world_setup.entrance_mapping.items() if ex == target]
            hint_data[self.player][location.address] = ", ".join(entrances)

    def local_front_fill(self, itempool: list[Item], target: int) -> None:
        def get_reachable_locations(collection_state: CollectionState) -> list[Location]:
            return [l for r in collection_state.reachable_regions[self.player] for l in r.locations if not l.is_event]
        
        start_items = [item for item in itempool
            if item.advancement
            and item.name not in self.options.non_local_items
            and not any(x for x in start_items_to_block_by_prefix if x in item.item_data.ladxr_id)]
        self.random.shuffle(start_items)
        collection_state = CollectionState(self.multiworld)
        collection_state.sweep_for_advancements(self.get_locations())
        reachable_locations = get_reachable_locations(collection_state)
        while len(reachable_locations) < target and any(l for l in reachable_locations if not l.item):
            placed_item = False
            for item in start_items:
                test_collection_state = collection_state.copy()
                test_collection_state.collect(item, prevent_sweep=True)
                test_collection_state.sweep_for_advancements(self.get_locations())
                new_reachable_locations = get_reachable_locations(test_collection_state)
                if len(new_reachable_locations) > len(reachable_locations):
                    potential_locations = sorted([l for l in reachable_locations if not l.item])
                    location = next( # always start with Tarin's Gift
                        (l for l in potential_locations if l.name == "Tarin's Gift (Mabe Village)"),
                        self.random.choice(potential_locations))
                    start_items.remove(item)
                    item = itempool.pop(itempool.index(item))
                    location.place_locked_item(item)
                    reachable_locations = new_reachable_locations
                    placed_item = True
                    break
            if not placed_item:
                break

    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        for location in self.multiworld.get_locations(self.player):
            if (
                not isinstance(location, LinksAwakeningLocation)
                or isinstance(location.ladxr_item, LADXRChest) 
                or isinstance(location.ladxr_item, LADXRDroppedKey)
            ):
                continue
            forbid_item(location, ladxr_to_ap_item_name['GEL'], self.player)

        allowed_locations_by_item = {}

        # Set up filter rules

        # set containing the list of all possible dungeon locations for the player
        all_dungeon_locs = set()

        # Do dungeon specific things
        for dungeon_index in range(0, 9):
            # set up allow-list for dungeon specific items
            locs = set(loc for loc in self.dungeon_locations_by_dungeon[dungeon_index] if not loc.item)
            for item in self.prefill_original_dungeon[dungeon_index]:
                allowed_locations_by_item[item] = locs

            # ...and gather the list of all dungeon locations
            all_dungeon_locs |= locs
            # ...also set the rules for the dungeon
            for location in locs:
                orig_rule = location.item_rule
                # If an item is about to be placed on a dungeon location, it can go there iff 
                # 1. it fits the general rules for that location (probably 'return True' for most places)
                # 2. Either
                #    2a. it's not a restricted dungeon item
                #    2b. it's a restricted dungeon item and this location is specified as allowed
                location.item_rule = lambda item, location=location, orig_rule=orig_rule: \
                    (item not in allowed_locations_by_item or location in allowed_locations_by_item[item]) and orig_rule(item)

        # Now set up the allow-list for any-dungeon items
        for item in self.prefill_own_dungeons:
            # They of course get to go in any spot
            allowed_locations_by_item[item] = all_dungeon_locs

        # Get the list of locations and shuffle
        all_dungeon_locs_to_fill = sorted(all_dungeon_locs)

        self.random.shuffle(all_dungeon_locs_to_fill)

        # Get the list of items and sort by priority
        def priority(item):
            # 0 - Nightmare dungeon-specific
            # 1 - Key dungeon-specific
            # 2 - Other dungeon-specific
            # 3 - Nightmare any local dungeon
            # 4 - Key any local dungeon
            # 5 - Other any local dungeon
            i = 2
            if "Nightmare" in item.name:
                i = 0
            elif "Key" in item.name:
                i = 1
            if allowed_locations_by_item[item] is all_dungeon_locs:
                i += 3
            return i
        all_dungeon_items_to_fill = self.get_pre_fill_items()
        all_dungeon_items_to_fill.sort(key=priority)

        # Set up state
        partial_all_state = CollectionState(self.multiworld)
        # Collect every item from the item pool and every pre-fill item like MultiWorld.get_all_state, except not our own pre-fill items.
        for item in self.multiworld.itempool:
            partial_all_state.collect(item, prevent_sweep=True)
        for player in self.multiworld.player_ids:
            if player == self.player:
                # Don't collect the items we're about to place.
                continue
            subworld = self.multiworld.worlds[player]
            for item in subworld.get_pre_fill_items():
                partial_all_state.collect(item, prevent_sweep=True)

        # Sweep to pick up already placed items that are reachable with everything but the dungeon items.
        partial_all_state.sweep_for_advancements()

        fill_restrictive(self.multiworld, partial_all_state, all_dungeon_locs_to_fill, all_dungeon_items_to_fill, lock=True, single_player_placement=True, allow_partial=False)

    def post_fill(self):
        # sort precollected for better processing in game
        def sort_key(item):
            if any(x for x in item_prefixes_to_skip_text_in_prefill if item.item_data.ladxr_id.startswith(x)):
                return 1
            return 0
        self.multiworld.precollected_items[self.player].sort(key=sort_key)

        self.ladx_in_game_hints = generate_hint_texts(self)

    def generate_output(self, output_directory: str):
        self.rom_item_placements = []
        matcher = ForeignItemIconMatcher()
        # copy items back to locations
        for r in self.multiworld.get_regions(self.player):
            for loc in r.locations:
                if isinstance(loc, LinksAwakeningLocation):
                    if loc.item.is_event:
                        continue

                    spot = {}

                    # for our items, just use the item
                    if loc.item.player == self.player:
                        spot["item"] = loc.item.item_data.ladxr_id

                    # indicate progression at higher priority over displaying ladx items for other slots
                    elif self.options.foreign_item_icons == 'indicate_progression':
                        if loc.item.trap or (loc.item.advancement and not loc.item.deprioritized):
                            spot["item"] = 'ARCHIPELAGO_1'
                        elif loc.item.advancement:
                            spot["item"] = 'ARCHIPELAGO_2'
                        else:
                            spot["item"] = 'ARCHIPELAGO_3'

                    # If we're a links awakening item, just use the item
                    elif isinstance(loc.item, LinksAwakeningItem):
                        spot["item"] = loc.item.item_data.ladxr_id

                    # Foreign icon matching
                    else:
                        game = self.multiworld.game[loc.item.player]
                        spot["item"] = matcher.get_icon_for_other_world(loc.item.name, game)


                    spot["custom_item_name"] = loc.item.name

                    if loc.item:
                        spot["item_owner"] = loc.item.player
                    else:
                        spot["item_owner"] = self.player

                    spot["name_id"] = loc.ladxr_item.nameId
                    self.rom_item_placements.append(spot)

        
        patch = LADXProcedurePatch(player=self.player, player_name=self.player_name)
        write_patch_data(self, patch)
        out_path = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}"
                                                  f"{patch.patch_file_ending}")

        patch.write(out_path)

        if TEST_PATCH:
            import Patch
            Patch.create_rom_file(out_path)

    def generate_multi_key(self):
        return bytearray(self.random.getrandbits(8) for _ in range(10)) + self.player.to_bytes(2, 'big')

    def modify_multidata(self, multidata: dict):
        multidata["connect_names"][binascii.hexlify(self.multi_key).decode()] = multidata["connect_names"][self.player_name]

    def collect(self, state, item: Item) -> bool:
        change = super().collect(state, item)
        if change and isinstance(item, LinksAwakeningItem) and item.item_data.ladxr_id in rupees:
            state.prog_items[self.player]["RUPEES"] += rupees[item.item_data.ladxr_id]
        return change

    def remove(self, state, item: Item) -> bool:
        change = super().remove(state, item)
        if change and isinstance(item, LinksAwakeningItem) and item.item_data.ladxr_id in rupees:
            state.prog_items[self.player]["RUPEES"] -= rupees[item.item_data.ladxr_id]
        return change    

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, typing.Any]) -> dict[str, typing.Any]:
        # Trigger a regen in UT
        return slot_data

    def fill_slot_data(self):
        hint_data = {
            k: {"location": v["location"], "player": v["player"]}
            for k, v in self.ladx_in_game_hints.items()
            if v is not None
        }
        hint_data.update({
            0x030: {
                "location": self.location_name_to_id["Shop 200 Item (Mabe Village)"],
                "player": self.player,
            },
            0x02C: {
                "location": self.location_name_to_id["Shop 980 Item (Mabe Village)"],
                "player": self.player,
            }
        })
        slot_data = {
            "world_version": self.world_version.as_simple_string(),
			"death_link": self.options.death_link.value,
            "hint_data": hint_data,
        }

        if not self.multiworld.is_race:
            # all of these option are NOT used by the LADX- or Text-Client.
            # they are used by Magpie tracker (https://github.com/kbranch/Magpie/wiki/Autotracker-API)
            # for convenient auto-tracking of the generated settings and adjusting the tracker accordingly

            slot_options = ["instrument_count"]

            slot_options_display_name = [
                "goal",
                "logic",
                "tradequest",
                "rooster",
                "entrance_rules",
                "shuffle_start",
                "shuffle_dungeons",
                "shuffle_basic",
                "shuffle_junk",
                "shuffle_connectors",
                "shuffle_water",
                "shuffle_annoying",
                "trendy_game",
                "block_free_powder",
                "gfxmod",
                "shuffle_nightmare_keys",
                "shuffle_small_keys",
                "shuffle_maps",
                "shuffle_compasses",
                "shuffle_stone_beaks",
                "shuffle_instruments",
                "nag_messages",
                "hard_mode",
                "overworld",
                "owlsanity",
            ]

            # use the default behaviour to grab options
            slot_data.update(self.options.as_dict(*slot_options))

            # for options which should not get the internal int value but the display name use the extra handling
            slot_data.update({
                option: value.current_key
                for option, value in dataclasses.asdict(self.options).items() if option in slot_options_display_name
            })

            slot_data.update({
                "world_setup_goal": self.ladxr_world_setup.goal,
                "entrance_mapping": self.ladxr_world_setup.entrance_mapping,
                "boss_mapping": self.ladxr_world_setup.boss_mapping,
                "miniboss_mapping": self.ladxr_world_setup.miniboss_mapping,
                "condensed_dungeons": self.ladxr_world_setup.condensed_dungeons,
                "excluded_dungeons": self.ladxr_world_setup.excluded_dungeons,
                "ladxr_settings": self.ladxr_settings_dict,
            })

        return slot_data

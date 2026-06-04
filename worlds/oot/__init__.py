import logging
import threading
import copy
import functools
import settings
import typing
from typing import Optional, List, AbstractSet, Union  # remove when 3.8 support is dropped
from collections import Counter, deque

logger = logging.getLogger("Ocarina of Time")

from .Location import OOTLocation, LocationFactory, location_name_to_id, build_location_name_groups
from .Entrance import OOTEntrance
from .EntranceShuffle import shuffle_random_entrances, entrance_shuffle_table, EntranceShuffleError
from .HintList import getRequiredHints
from .Hints import HintArea, HintAreaNotFound, hint_dist_keys, get_hint_area, buildWorldGossipHints, populate_misc_hint_data
from .Items import OOTItem, item_table, oot_data_to_ap_id, oot_is_item_of_type, REWARD_COLORS, REWARD_TO_DUNGEON
from .ItemPool import generate_itempool, get_junk_item, get_junk_pool
from .Regions import OOTRegion, TimeOfDay
from .Rules import set_rules, set_shop_rules, set_entrances_based_rules
from .RuleParser import Rule_AST_Transformer
from .Options import EmptyDungeonList, EmptyDungeonRewards, OoTOptions, oot_option_groups
from .Utils import data_path, read_json, __version__ as oot_version
from .LocationList import business_scrubs, set_drop_location_names, dungeon_song_locations
from .DungeonList import dungeon_table, create_dungeons
from .LogicTricks import normalized_name_tricks, normalized_name_advanced_tricks
from .OcarinaSongs import SONG_TABLE, generate_song_list
from .Rom import Rom
from .Patches import OoTContainer, patch_rom
from .N64Patch import create_patch_file
from .Cosmetics import patch_cosmetics

from BaseClasses import MultiWorld, CollectionState, Tutorial
from Options import Range, Toggle, VerifyKeys, Accessibility, PlandoConnections, PlandoItems
from Fill import fill_restrictive, fast_fill, FillError
from worlds.generic.Rules import exclusion_rules, add_item_rule
from worlds.AutoWorld import World, AutoLogicRegister, WebWorld
from worlds.LauncherComponents import launch as launch_component, components, Component, Type, SuffixIdentifier, icon_paths

# OoT's generate_output doesn't benefit from more than 2 threads, instead it uses a lot of memory.
i_o_limiter = threading.Semaphore(2)

class _StartingItemRecord:
    def __init__(self, count: int):
        self.count = count


class _OOTDistribution:
    def __init__(self, world: "OOTWorld"):
        self.world = world

    @property
    def effective_starting_items(self):
        records = {}
        for item_name, count in self.world.starting_items.items():
            records[item_name] = _StartingItemRecord(count)
        for item in self.world.multiworld.precollected_items[self.world.player]:
            record = records.get(item.name)
            if record is None:
                records[item.name] = _StartingItemRecord(1)
            else:
                record.count += 1
        return records

    def configure_gossip(self, stone_ids):
        return

    def configure_songs(self):
        return {}

def launch_client(*args):
    from .client import main
    launch_component(main, name="OoTClient", args=args)


icon_paths["oot"] = f"ap:{__name__}/data/icon.png"
components.append(Component(display_name="Ocarina of Time Client", func=launch_client, component_type=Type.CLIENT,
                            file_identifier=SuffixIdentifier('.apz5'),
                            description=f"Connect to an OoT multiworld using OoT APWorld {oot_version}.", icon="oot"))


def launch_adjuster(*args):
    from .Adjuster import launch
    launch_component(launch, name="OoTAdjuster", args=args)


components.append(Component(display_name="Ocarina of Time Adjuster", component_type=Type.ADJUSTER, func=launch_adjuster,
                            description=f"Change Cosmetics and SFX for your OoT Seed using OoT APWorld {oot_version}.", icon="oot"))


class OOTCollectionState(metaclass=AutoLogicRegister):
    def init_mixin(self, parent: MultiWorld):
        oot_ids = parent.get_game_players(OOTWorld.game) + parent.get_game_groups(OOTWorld.game)
        self.child_reachable_regions = {player: set() for player in oot_ids}
        self.adult_reachable_regions = {player: set() for player in oot_ids}
        self.child_blocked_connections = {player: set() for player in oot_ids}
        self.adult_blocked_connections = {player: set() for player in oot_ids}
        self.day_reachable_regions = {player: set() for player in oot_ids}
        self.dampe_reachable_regions = {player: set() for player in oot_ids}
        self.age = {player: None for player in oot_ids}

    def copy_mixin(self, ret) -> CollectionState:
        ret.child_reachable_regions = {player: copy.copy(self.child_reachable_regions[player]) for player in
                                       self.child_reachable_regions}
        ret.adult_reachable_regions = {player: copy.copy(self.adult_reachable_regions[player]) for player in
                                       self.adult_reachable_regions}
        ret.child_blocked_connections = {player: copy.copy(self.child_blocked_connections[player]) for player in
                                         self.child_blocked_connections}
        ret.adult_blocked_connections = {player: copy.copy(self.adult_blocked_connections[player]) for player in
                                         self.adult_blocked_connections}
        ret.day_reachable_regions = {player: copy.copy(self.day_reachable_regions[player]) for player in
                                     self.day_reachable_regions}
        ret.dampe_reachable_regions = {player: copy.copy(self.dampe_reachable_regions[player]) for player in
                                       self.dampe_reachable_regions}
        return ret

    def has_medallions(self, count: int, player: int) -> bool:
        """Returns True if the player has at least 'count' medallions."""
        return self.has_group_unique("medallions", player, count)

    def has_stones(self, count: int, player: int) -> bool:
        """Returns True if the player has at least 'count' spiritual stones."""
        return self.has_group_unique("stones", player, count)

    def has_dungeon_rewards(self, count: int, player: int) -> bool:
        """Returns True if the player has at least 'count' dungeon rewards (stones + medallions)."""
        return self.has_group_unique("rewards", player, count)

    def has_hearts(self, count: int, player: int) -> bool:
        """Returns True if the player has at least 'count' total hearts."""
        containers = self.count("Heart Container", player)
        pieces = self.count("Piece of Heart", player) + self.count("Piece of Heart (Treasure Chest Game)", player)
        starting_hearts = self.multiworld.worlds[player].starting_hearts
        return max(starting_hearts, 3 + containers + pieces // 4) >= count

    def has_soul(self, enemy: str, player: int) -> bool:
        """
        v9.0 advanced logic references enemy souls extensively.
        AP does not currently model souls as progression, so this is a permissive compatibility stub.
        """
        return True


class OOTSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        """File name of the OoT v1.0 NTSC-U or NTSC-J ROM"""
        description = "Ocarina of Time ROM File"
        copy_to = "The Legend of Zelda - Ocarina of Time.z64"
        md5s = [
            "5bd1fe107bf8106b2ab6650abecd54d6",  # NTSC-U z64
            "6697768a7a7df2dd27a692a2638ea90b",  # NTSC-U n64, byte-swapped
            "05f0f3ebacbc8df9243b6148ffe4792f",  # NTSC-U decompressed z64
            "9f04c8e68534b870f707c247fa4b50fc",  # NTSC-J z64
            "7d44b555e0af3eec36319b5e76e31b0c",  # NTSC-J n64, byte-swapped
            "a6090ade6efb0490f5e74838d47bbfac",  # NTSC-J decompressed z64
        ]

    class RomStart(str):
        """
        Set this to false to never autostart a rom (such as after patching),
                    true  to open with emulator_path.
        If emulator_path is blank when patching finishes, the client will ask for it.
        """

    class EmulatorPath(settings.OptionalUserFilePath):
        """
        Path to an N64 emulator executable to auto-launch patched ROMs with.
        Leave blank to be asked for an emulator when patching finishes and rom_start is true.
        """
        is_exe = True
        description = "N64 Emulator Executable"

    rom_file: RomFile = RomFile(RomFile.copy_to)
    rom_start: typing.Union[RomStart, bool] = True
    emulator_path: EmulatorPath | str = ""


def launch_rom(
    path: str,
    logger: logging.Logger,
    status_callback: typing.Callable[[str], None] | None = None,
) -> None:
    import os
    import subprocess

    rom_path = os.path.realpath(path)
    auto_start = OOTWorld.settings.rom_start
    # Read the raw setting so a blank OptionalUserFilePath stays blank instead of resolving to ".exe".
    emulator_path = OOTWorld.settings.__dict__.get("emulator_path", OOTWorld.settings.__class__.emulator_path)

    if not auto_start:
        return

    if not emulator_path:
        logger.info("OoT emulator path is not configured. Asking for oot_options.emulator_path.")
        emulator_path = OOTWorld.settings.EmulatorPath("").browse()
        if not emulator_path:
            logger.error("Could not auto-launch OoT ROM: oot_options.emulator_path is required.")
            return

        OOTWorld.settings.emulator_path = emulator_path
        OOTWorld.settings._changed = True

    emulator = str(emulator_path.resolve() if hasattr(emulator_path, "resolve") else emulator_path)
    try:
        if status_callback:
            status_callback("Starting OoT emulator.")
        else:
            logger.info("Starting OoT emulator.")
        subprocess.Popen(
            [emulator, rom_path],
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except OSError as exc:
        logger.error("Could not auto-launch OoT ROM with %s: %s", emulator, exc)


class OOTWeb(WebWorld):
    display_name = "The Legend of Zelda: Ocarina of Time"
    setup = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Ocarina of Time Randomizer for Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["TreZ"]
    )

    setup_de = Tutorial(
        setup.tutorial_name,
        setup.description,
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["TreZ"]
    )

    tutorials = [setup, setup_de]
    option_groups = oot_option_groups
    game_info_languages = ["en", "de"]


class OOTWorld(World):
    """
    The Legend of Zelda: Ocarina of Time is a 3D action/adventure game. Travel through Hyrule in two time periods,
    learn magical ocarina songs, and explore twelve dungeons on your quest. Use Link's many items and abilities
    to rescue the Seven Sages, and then confront Ganondorf to save Hyrule!
    """
    game: str = "Ocarina of Time"
    options_dataclass = OoTOptions
    options: OoTOptions
    settings: typing.ClassVar[OOTSettings]
    topology_present: bool = True
    item_name_to_id = {item_name: oot_data_to_ap_id(data, False) for item_name, data in item_table.items() if
                       oot_data_to_ap_id(data, False) is not None and item_name not in {
                        'Buy Magic Bean', 'Milk',
                        'Small Key', 'Map', 'Compass', 'Boss Key',
                       }}  # These are items which aren't used, but have get-item values
    location_name_to_id = location_name_to_id
    web = OOTWeb()

    required_client_version = (0, 6, 4)

    item_name_groups = {
        # internal groups
        "medallions": {"Light Medallion", "Forest Medallion", "Fire Medallion",
            "Water Medallion", "Shadow Medallion", "Spirit Medallion"},
        "stones": {"Kokiri Emerald", "Goron Ruby", "Zora Sapphire"},
        "rewards": {"Light Medallion", "Forest Medallion", "Fire Medallion",
            "Water Medallion", "Shadow Medallion", "Spirit Medallion",
            "Kokiri Emerald", "Goron Ruby", "Zora Sapphire"},
        "logic_bottles": {"Bottle", "Bottle with Milk", "Deliver Letter",
            "Sell Big Poe", "Bottle with Red Potion", "Bottle with Green Potion",
            "Bottle with Blue Potion", "Bottle with Fairy", "Bottle with Fish",
            "Bottle with Blue Fire", "Bottle with Bugs", "Bottle with Poe"},

        # hint groups
        "Bottles": {"Bottle", "Bottle with Milk", "Rutos Letter",
            "Bottle with Big Poe", "Bottle with Red Potion", "Bottle with Green Potion",
            "Bottle with Blue Potion", "Bottle with Fairy", "Bottle with Fish",
            "Bottle with Blue Fire", "Bottle with Bugs", "Bottle with Poe"},
        "Adult Trade Item": {"Pocket Egg", "Pocket Cucco", "Cojiro", "Odd Mushroom",
            "Odd Potion", "Poachers Saw", "Broken Sword", "Prescription",
            "Eyeball Frog", "Eyedrops", "Claim Check"},
        "Keys": {"Small Key (Bottom of the Well)", "Small Key (Fire Temple)", "Small Key (Forest Temple)",
                 "Small Key (Ganons Castle)", "Small Key (Gerudo Training Ground)", "Small Key (Shadow Temple)",
                 "Small Key (Spirit Temple)", "Small Key (Thieves Hideout)", "Small Key (Water Temple)",
                 "Small Key Ring (Bottom of the Well)", "Small Key Ring (Fire Temple)",
                 "Small Key Ring (Forest Temple)", "Small Key Ring (Ganons Castle)",
                 "Small Key Ring (Gerudo Training Ground)", "Small Key Ring (Shadow Temple)",
                 "Small Key Ring (Spirit Temple)", "Small Key Ring (Thieves Hideout)", "Small Key Ring (Water Temple)",
                 "Boss Key (Fire Temple)", "Boss Key (Forest Temple)", "Boss Key (Ganons Castle)",
                 "Boss Key (Shadow Temple)", "Boss Key (Spirit Temple)", "Boss Key (Water Temple)"},

        # aliases
        "Longshot": {"Progressive Hookshot"},  # fuzzy hinting thought Longshot was Slingshot
        "Hookshot": {"Progressive Hookshot"},  # for consistency, mostly
    }

    location_name_groups = build_location_name_groups()


    def __init__(self, world, player):
        self.hint_data_available = threading.Event()
        self.collectible_flags_available = threading.Event()
        super(OOTWorld, self).__init__(world, player)


    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        oot_settings = OOTWorld.settings
        rom = Rom(file=oot_settings.rom_file)


    # Option parsing, handling incompatible options, building useful-item table
    def generate_early(self):
        self.parser = Rule_AST_Transformer(self, self.player)

        for option_name in self.options_dataclass.type_hints:
            result = getattr(self.options, option_name)
            if isinstance(result, Range):
                option_value = int(result)
            elif isinstance(result, Toggle):
                option_value = bool(result)
            elif isinstance(result, VerifyKeys):
                option_value = result.value
            elif isinstance(result, PlandoConnections):
                option_value = result.value
            elif isinstance(result, PlandoItems):
                option_value = result.value
            else:
                option_value = result.current_key
            setattr(self, option_name, option_value)

        self.regions = []  # internal caches of regions for this world, used later
        self._regions_cache = {}

        self.shop_prices = {}
        self.shop_location_flags = {}
        self.remove_from_start_inventory = []  # some items will be precollected but not in the inventory
        self.randomized_starting_items = {}
        self.starting_items = Counter()
        self.songs_as_items = False
        self.file_hash = [self.random.randint(0, 31) for i in range(5)]
        player_id = min(self.player, 255)
        self.connect_name = f"OOT{player_id:03d}-" + ''.join(f"{value:02x}" for value in self.file_hash)
        self.collectible_flag_addresses = {}
        self.song_notes = {name: notes for name, (_, _, notes) in SONG_TABLE.items()}

        starts_with_zeldas_letter = (
            self.options.start_inventory.value.get('Zeldas Letter', 0) > 0
            or any(item.name == 'Zeldas Letter' for item in self.multiworld.precollected_items[self.player])
        )

        # Set skip_child_zelda boolean for logic. Upstream models this as
        # starting with Zelda's Letter while Zelda's Letter itself is not shuffled.
        self.skip_child_zelda = starts_with_zeldas_letter and 'Zeldas Letter' not in self.shuffle_child_trade

        # Fix spawn positions option
        new_sp = []
        if self.spawn_positions in {'child', 'both'}:
            new_sp.append('child')
        if self.spawn_positions in {'adult', 'both'}:
            new_sp.append('adult')
        self.spawn_positions = new_sp

        # Closed forest and adult start are not compatible; closed forest takes priority
        if self.open_forest == 'closed':
            self.starting_age = 'child'
            # These ER options force closed forest to become closed deku
            if (self.shuffle_interior_entrances == 'all' or self.shuffle_overworld_entrances or self.warp_songs or self.spawn_positions):
                self.open_forest = 'closed_deku'

        # Ganon boss key should not be in itempool in triforce hunt
        if self.triforce_hunt:
            self.shuffle_ganon_bosskey = 'triforce'

        # Force itempool to higher settings if it doesn't have enough collectible hearts.
        max_required_hearts = 3
        if self.bridge == 'hearts':
            max_required_hearts = max(max_required_hearts, self.bridge_hearts)
        if self.shuffle_ganon_bosskey == 'hearts':
            max_required_hearts = max(max_required_hearts, self.ganon_bosskey_hearts)
        if max_required_hearts > self.starting_hearts and self.item_pool_value == 'minimal':
            self.item_pool_value = 'scarce'
        if max_required_hearts > self.starting_hearts + 9 and self.item_pool_value == 'scarce':
            self.item_pool_value = 'balanced'

        # If songs/keys locked to own world by settings, add them to local_items
        local_types = []
        if self.shuffle_song_items != 'any':
            local_types.append('Song')
        if self.shuffle_map != 'keysanity':
            local_types.append('Map')
        if self.shuffle_compass != 'keysanity':
            local_types.append('Compass')
        if self.shuffle_smallkeys != 'keysanity':
            local_types.append('SmallKey')
        if self.shuffle_hideoutkeys != 'keysanity':
            local_types.append('HideoutSmallKey')
        if self.shuffle_bosskeys != 'keysanity':
            local_types.append('BossKey')
        if self.shuffle_ganon_bosskey != 'keysanity':
            local_types.append('GanonBossKey')
        self.options.local_items.value |= set(name for name, data in item_table.items() if data[0] in local_types)

        # If any songs are itemlinked, set songs_as_items
        for group in self.multiworld.groups.values():
            if self.songs_as_items or group['game'] != self.game or self.player not in group['players']:
                continue
            for item_name in group['item_pool']:
                if oot_is_item_of_type(item_name, 'Song'):
                    self.songs_as_items = True
                    break

        # Determine skipped trials in GT
        # This needs to be done before the logic rules in GT are parsed
        trial_list = ['Forest', 'Fire', 'Water', 'Spirit', 'Shadow', 'Light']
        chosen_trials = self.random.sample(trial_list, self.trials)  # chooses a list of trials to NOT skip
        self.skipped_trials = {trial: (trial not in chosen_trials) for trial in trial_list}

        # Determine tricks in logic
        if self.logic_rules in ('glitchless', 'advanced'):
            for trick in self.allowed_tricks:
                normalized_name = trick.casefold()
                if normalized_name in normalized_name_tricks:
                    setattr(self, normalized_name_tricks[normalized_name]['name'], True)
                else:
                    raise Exception(f'Unknown OOT logic trick for player {self.player}: {trick}')

        if self.logic_rules == 'advanced':
            for trick_info in normalized_name_advanced_tricks.values():
                setattr(self, trick_info['name'], False)
            for trick in self.advanced_allowed_tricks:
                normalized_name = trick.casefold()
                if normalized_name in normalized_name_advanced_tricks:
                    setattr(self, normalized_name_advanced_tricks[normalized_name]['name'], True)
        else:
            # Always clear advanced tricks unless we are in advanced logic.
            # Prevents stale attrs from a previous world instance from leaking in.
            for trick_info in normalized_name_advanced_tricks.values():
                setattr(self, trick_info['name'], False)

        # No Logic forces all tricks on, prog balancing off and beatable-only
        if self.logic_rules == 'no_logic':
            self.options.progression_balancing.value = False
            self.options.accessibility.value = Accessibility.option_minimal
            for trick in normalized_name_tricks.values():
                setattr(self, trick['name'], True)

        # Not implemented for now, but needed to placate the generator. Remove as they are implemented
        self.mix_entrance_pools = False
        self.decouple_entrances = False
        self.available_tokens = 100
        # Deprecated LACS options
        self.lacs_condition = 'vanilla'
        self.lacs_stones = 3
        self.lacs_medallions = 6
        self.lacs_rewards = 9
        self.lacs_tokens = 100
        self.lacs_hearts = 20
        # RuleParser hack
        self.triforce_goal_per_world = self.triforce_goal

        # Set internal names used by the OoT generator
        self.keysanity = self.shuffle_smallkeys in ['keysanity', 'remove', 'any_dungeon', 'overworld']
        self.trials_random = self.options.trials.randomized
        self.mq_dungeons_random = self.options.mq_dungeons_count.randomized
        if (self.options.special_deal_price_min.randomized
                and self.options.special_deal_price_max.randomized
                and self.special_deal_price_min > self.special_deal_price_max):
            self.special_deal_price_min, self.special_deal_price_max = (
                self.special_deal_price_max, self.special_deal_price_min)
            self.options.special_deal_price_min.value = self.special_deal_price_min
            self.options.special_deal_price_max.value = self.special_deal_price_max
        if not self.easier_fire_arrow_entry:
            self.fae_torch_count = 24

        # Hint stuff
        self.clearer_hints = True  # this is being enforced since non-oot items do not have non-clear hint text
        self.gossip_hints = {}
        self.required_locations = []
        self.empty_areas = {}
        self.major_item_locations = []
        self.hinted_dungeon_reward_locations = {}
        for item in self.multiworld.precollected_items[self.player]:
            if item.name in self.item_name_groups['rewards']:
                self.hinted_dungeon_reward_locations[item.name] = None

        # ER names
        self.shuffle_special_dungeon_entrances = self.shuffle_dungeon_entrances == 'all'
        self.shuffle_dungeon_entrances = self.shuffle_dungeon_entrances != 'off'
        self.ensure_tod_access = (self.shuffle_interior_entrances != 'off') or self.shuffle_overworld_entrances or self.spawn_positions
        self.entrance_shuffle = (
            self.shuffle_interior_entrances != 'off'
            or self.shuffle_bosses != 'off'
            or self.shuffle_dungeon_entrances
            or self.shuffle_special_dungeon_entrances
            or self.spawn_positions
            or self.shuffle_grotto_entrances
            or self.shuffle_overworld_entrances
            or self.owl_drops
            or self.warp_songs
        )
        self.adult_trade_shuffle = bool(self.options.adult_trade_shuffle)
        self.disable_trade_revert = (self.shuffle_interior_entrances != 'off') or self.shuffle_overworld_entrances or self.adult_trade_shuffle
        self.shuffle_special_interior_entrances = self.shuffle_interior_entrances == 'all'
        if self.shuffle_bosses == 'off':
            self.shuffle_ganon_tower = False
        self.mixed_pools_bosses = self.shuffle_bosses == 'full'
        self.entrance_rando_reward_hints = (
            self.mixed_pools_bosses
            or self.shuffle_ganon_tower
            or self.shuffle_dungeon_rewards not in ('vanilla', 'reward')
        )

        # Convert the double option used by shopsanity into a single option
        if self.shopsanity == 'random_number':
            self.shopsanity = 'random'
        elif self.shopsanity == 'fixed_number':
            self.shopsanity = str(self.shop_slots)

        # Rename options
        self.dungeon_shortcuts_choice = self.dungeon_shortcuts
        if self.dungeon_shortcuts_choice == 'random_dungeons':
            self.dungeon_shortcuts_choice = 'random'
        self.key_rings_list          = {s.replace("'", "") for s in self.key_rings_list}
        self.dungeon_shortcuts       = {s.replace("'", "") for s in self.dungeon_shortcuts_list}
        self.mq_dungeons_specific    = {s.replace("'", "") for s in self.mq_dungeons_list}
        self.empty_dungeons_specific = {s.replace("'", "") for s in self.empty_dungeons_list}
        self.empty_dungeons_rewards  = {s.replace("'", "") for s in self.empty_dungeons_rewards}

        # Determine which dungeons have key rings.
        keyring_dungeons = [d['name'] for d in dungeon_table if d['small_key']] + ['Thieves Hideout', 'Treasure Chest Game']
        if self.key_rings == 'off':
            self.key_rings = []
        elif self.key_rings == 'all':
            self.key_rings = keyring_dungeons
        elif self.key_rings == 'choice':
            self.key_rings = self.key_rings_list
        elif self.key_rings == 'random_dungeons':
            self.key_rings = self.random.sample(keyring_dungeons,
                self.random.randint(0, len(keyring_dungeons)))

        # Determine which dungeons are MQ.
        mq_dungeons = set()
        all_dungeons = [d['name'] for d in dungeon_table]
        if self.mq_dungeons_mode == 'mq':
            mq_dungeons = all_dungeons
        elif self.mq_dungeons_mode == 'specific':
            mq_dungeons = self.mq_dungeons_specific
        elif self.mq_dungeons_mode == 'count':
            mq_dungeons = self.random.sample(all_dungeons, self.mq_dungeons_count)
        self.dungeon_mq = {item['name']: (item['name'] in mq_dungeons) for item in dungeon_table}
        self.dungeon_mq['Thieves Hideout'] = False  # fix for bug in SaveContext:287

        # Determine which reward dungeons are pre-completed.
        empty_dungeon_pool = self.get_empty_dungeon_pool()
        empty_dungeons = set()
        self.empty_dungeon_reward_assignments = {}
        if self.empty_dungeons_mode == 'specific':
            empty_dungeons = self.empty_dungeons_specific
        elif self.empty_dungeons_mode == 'count':
            empty_dungeons = set(self.random.sample(empty_dungeon_pool, self.empty_dungeons_count))
        elif self.empty_dungeons_mode == 'rewards':
            empty_dungeons = self.select_empty_dungeons_from_rewards(empty_dungeon_pool)
        self.precompleted_dungeons = {name: (name in empty_dungeons) for name in empty_dungeon_pool}
        self.empty_dungeon_starting_rewards = []

        # Determine which dungeons have shortcuts.
        shortcut_dungeons = ['Deku Tree', 'Dodongos Cavern', \
            'Jabu Jabus Belly', 'Forest Temple', 'Fire Temple', \
            'Water Temple', 'Shadow Temple', 'Spirit Temple']
        if self.dungeon_shortcuts_choice == 'off':
            self.dungeon_shortcuts = set()
        elif self.dungeon_shortcuts_choice == 'all':
            self.dungeon_shortcuts = set(shortcut_dungeons)
        elif self.dungeon_shortcuts_choice == 'random':
            self.dungeon_shortcuts = self.random.sample(shortcut_dungeons,
                self.random.randint(0, len(shortcut_dungeons)))
        # == 'choice', leave as previous

        # fixing some options
        # Fixes starting time spelling: "witching_hour" -> "witching-hour"
        self.starting_tod = self.starting_tod.replace('_', '-')
        self.shuffle_scrubs = self.shuffle_scrubs.replace('_prices', '')

        # Set selected_adult_trade_item for logic rules (used before ItemPool runs).
        # When shuffling all trade items there is no single fixed start, so leave it None.
        if not self.adult_trade_shuffle and self.adult_trade_start:
            self.selected_adult_trade_item = self.random.choice(sorted(self.adult_trade_start))
        else:
            self.selected_adult_trade_item = None

        # Get hint distribution
        self.hint_dist_user = read_json(data_path('Hints', f'{self.hint_dist}.json'))
        if 'combine_trial_hints' not in self.hint_dist_user:
            self.hint_dist_user['combine_trial_hints'] = False
        if 'boss_goal_names' not in self.hint_dist_user:
            self.hint_dist_user['boss_goal_names'] = True
        self.distribution = _OOTDistribution(self)
        self.song_notes = generate_song_list(
            self,
            frog='frog' in self.ocarina_songs,
            warp='warp' in self.ocarina_songs,
            frogs2='frogs2' in self.ocarina_songs,
        )

        self.added_hint_types = {}
        self.item_added_hint_types = {}
        self.hint_exclusions = set()
        if self.skip_child_zelda:
            self.hint_exclusions.add('Song from Impa')
        self.hint_type_overrides = {}
        self.item_hint_type_overrides = {}

        # unused hint stuff
        self.named_item_pool = {}
        self.hint_text_overrides = {}

        for dist in hint_dist_keys:
            self.added_hint_types[dist] = []
            for loc in self.hint_dist_user['add_locations']:
                if 'types' in loc:
                    if dist in loc['types']:
                        self.added_hint_types[dist].append(loc['location'])
            self.item_added_hint_types[dist] = []
            for i in self.hint_dist_user['add_items']:
                if dist in i['types']:
                    self.item_added_hint_types[dist].append(i['item'])
            self.hint_type_overrides[dist] = []
            for loc in self.hint_dist_user['remove_locations']:
                if dist in loc['types']:
                    self.hint_type_overrides[dist].append(loc['location'])
            self.item_hint_type_overrides[dist] = []
            for i in self.hint_dist_user['remove_items']:
                if dist in i['types']:
                    self.item_hint_type_overrides[dist].append(i['item'])

        self.always_hints = [hint.name for hint in getRequiredHints(self)]

        # Determine items which are not considered advancement based on settings. They will never be excluded.
        self.nonadvancement_items = {'Double Defense', 'Deku Stick Capacity', 'Deku Nut Capacity'}
        if (self.damage_multiplier != 'ohko' and self.damage_multiplier != 'quadruple' and
                self.shuffle_scrubs == 'off' and not self.shuffle_grotto_entrances):
            # nayru's love may be required to prevent forced damage
            self.nonadvancement_items.add('Nayrus Love')
        if getattr(self, 'logic_grottos_without_agony', False) and self.hints != 'agony':
            # Stone of Agony skippable if not used for hints or grottos
            self.nonadvancement_items.add('Stone of Agony')
        if (not self.shuffle_special_interior_entrances and not self.shuffle_overworld_entrances and
                not self.warp_songs and not self.spawn_positions):
            # Serenade and Prelude are never required unless one of those settings is enabled
            self.nonadvancement_items.add('Serenade of Water')
            self.nonadvancement_items.add('Prelude of Light')
        if not self.blue_fire_arrows:
            # Ice Arrows serve no purpose if they're not hacked to have one
            self.nonadvancement_items.add('Ice Arrows')
        if not self.free_bombchu_drops:
            # Nonrenewable bombchus are not a default logical explosive
            self.nonadvancement_items.update({
                'Bombchus (5)',
                'Bombchus (10)',
                'Bombchus (20)',
            })
        heart_requirement_needs_pool = (
            self.bridge == 'hearts' and self.bridge_hearts > self.starting_hearts
            or self.shuffle_ganon_bosskey == 'hearts' and self.ganon_bosskey_hearts > self.starting_hearts
        )
        if not heart_requirement_needs_pool:
            self.nonadvancement_items.update({
                'Heart Container',
                'Piece of Heart',
                'Piece of Heart (Treasure Chest Game)'
            })
        for dungeon_name, is_precompleted in self.precompleted_dungeons.items():
            if is_precompleted and self.accessibility != 'full':
                self.nonadvancement_items.update(self.get_dungeon_item_names(dungeon_name))
        if self.logic_rules == 'glitchless':
            # Both two-handed swords can be required in glitch logic, so only consider them nonprogression in glitchless
            self.nonadvancement_items.add('Biggoron Sword')
            self.nonadvancement_items.add('Giants Knife')
            if not getattr(self, 'logic_water_central_gs_fw', False):
                # Farore's Wind skippable if not used for this logic trick in Water Temple
                self.nonadvancement_items.add('Farores Wind')


    # Reads a group of regions from the given JSON file.
    def load_regions_from_json(self, file_path):
        region_json = read_json(file_path)

        for region in region_json:
            new_region = OOTRegion(region['region_name'], self.player, self.multiworld)
            if 'pretty_name' in region:
                new_region.pretty_name = region['pretty_name']
            if 'font_color' in region:
                new_region.font_color = region['font_color']
            if 'scene' in region:
                new_region.scene = region['scene']
            if 'dungeon' in region:
                new_region.dungeon = region['dungeon']
                new_region.set_hint_data(region['dungeon'])
            if 'is_boss_room' in region:
                new_region.is_boss_room = region['is_boss_room']
            if 'hint' in region:
                new_region.set_hint_data(region['hint'])
            if 'alt_hint' in region:
                new_region.alt_hint = HintArea[region['alt_hint']]
            if 'time_passes' in region:
                new_region.time_passes = region['time_passes']
                new_region.provides_time = TimeOfDay.ALL
            if new_region.name == 'Ganons Castle Grounds':
                new_region.provides_time = TimeOfDay.DAMPE
            if 'locations' in region:
                for location, rule in region['locations'].items():
                    new_location = LocationFactory(location, self.player)
                    if new_location.type in ['HintStone', 'Hint']:
                        continue
                    new_location.parent_region = new_region
                    new_location.rule_string = rule
                    self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        # We still need to fill the location even if ALR is off.
                        logger.debug('Unreachable location: %s', new_location.name)
                    new_location.player = self.player
                    # Change some attributes of Drop locations
                    if new_location.type == 'Drop':
                        new_location.name = new_region.name + ' ' + new_location.name
                        new_location.show_in_spoiler = False
                    new_region.locations.append(new_location)
            if 'events' in region:
                for event, rule in region['events'].items():
                    # Allow duplicate placement of events
                    lname = '%s from %s' % (event, new_region.name)
                    new_location = OOTLocation(self.player, lname, type='Event', parent=new_region)
                    new_location.rule_string = rule
                    self.parser.parse_spot_rule(new_location)
                    if new_location.never:
                        logger.debug('Dropping unreachable event: %s', new_location.name)
                    else:
                        new_location.player = self.player
                        new_region.locations.append(new_location)
                        self.make_event_item(event, new_location)
                        new_location.show_in_spoiler = False
            if 'exits' in region:
                for exit, rule in region['exits'].items():
                    new_exit = OOTEntrance(self.player, self.multiworld, '%s -> %s' % (new_region.name, exit), new_region)
                    new_exit.vanilla_connected_region = exit
                    new_exit.rule_string = rule
                    self.parser.parse_spot_rule(new_exit)
                    if new_exit.never:
                        logger.debug('Dropping unreachable exit: %s', new_exit.name)
                    else:
                        new_region.exits.append(new_exit)

            self.multiworld.regions.append(new_region)
            self.regions.append(new_region)
            self._regions_cache[new_region.name] = new_region


    # Sets deku scrub prices
    def set_scrub_prices(self):
        # Get Deku Scrub Locations
        scrub_locations = [location for location in self.get_locations() if location.type in {'Scrub', 'GrottoScrub'}]
        scrub_dictionary = {}
        self.scrub_prices = {}
        for location in scrub_locations:
            if location.default not in scrub_dictionary:
                scrub_dictionary[location.default] = []
            scrub_dictionary[location.default].append(location)

        # Loop through each type of scrub.
        for (scrub_item, default_price, text_id, text_replacement) in business_scrubs:
            price = default_price
            if self.shuffle_scrubs == 'low':
                price = 10
            elif self.shuffle_scrubs == 'random':
                # this is a random value between 0-99
                # average value is ~33 rupees
                price = int(self.random.betavariate(1, 2) * 99)

            # Set price in the dictionary as well as the location.
            self.scrub_prices[scrub_item] = price
            if scrub_item in scrub_dictionary:
                for location in scrub_dictionary[scrub_item]:
                    location.price = price
                    if location.item is not None:
                        location.item.price = price


    # Sets prices for shuffled shop locations
    def random_shop_prices(self):
        shop_item_indexes = ['7', '5', '8', '6']
        self.shop_prices = {}
        for region in self.regions:
            if self.shopsanity == 'random':
                shop_item_count = self.random.randint(0, 4)
            else:
                shop_item_count = int(self.shopsanity)

            for location in region.locations:
                if location.type == 'Shop':
                    if location.name[-1:] in shop_item_indexes[:shop_item_count]:
                        self.shop_prices[location.name] = self.new_shop_price(location)


    def calculate_shop_location_flags(self):
        current_shop_id = 0x32
        shop_location_flags = {}
        shop_regions = [
            ('KF Kokiri Shop', 'Shop'),
            ('Kak Bazaar', 'Shop'),
            ('Market Bazaar', 'Shop'),
            ('GC Shop', 'Shop'),
            ('ZD Shop', 'Shop'),
            ('Kak Potion Shop Front', 'Shop'),
            ('Market Potion Shop', 'Shop'),
            ('Market Bombchu Shop', 'Shop'),
            ('Market Mask Shop Storefront', 'MaskShop'),
        ]

        for region_name, location_type in shop_regions:
            for location in self.get_region(region_name).locations:
                if location.type != location_type:
                    continue

                selected_mask_shop_item = (
                    location.type == 'MaskShop'
                    and location.vanilla_item in self.shuffle_child_trade
                )
                vanilla_shop_item = isinstance(location.item, OOTItem) and location.item.type == 'Shop'
                custom_shop_item = not (
                    vanilla_shop_item
                    or (location.type == 'MaskShop' and not selected_mask_shop_item)
                )

                if custom_shop_item:
                    shop_location_flags[location.name] = current_shop_id - 0x32

                if location.type == 'MaskShop':
                    if custom_shop_item:
                        current_shop_id += 1
                elif any(c in location.name for c in {'5', '6', '7', '8'}):
                    current_shop_id += 1

        return shop_location_flags


    def new_shop_price(self, location):
        if self.special_deal_price_distribution == 'vanilla':
            return item_table[location.vanilla_item][3].get('price', 0)
        price_min = min(self.special_deal_price_min, self.special_deal_price_max)
        price_max = max(self.special_deal_price_min, self.special_deal_price_max)

        if price_max == price_min:
            return price_min
        elif self.special_deal_price_distribution == 'betavariate':
            return price_min + int(
                self.random.betavariate(1.5, 2) * (price_max - price_min) / 5) * 5
        elif self.special_deal_price_distribution == 'uniform':
            return self.random.randrange(price_min, price_max + 1, 5)
        else:
            raise NotImplementedError(
                f'Unimplemented special deal distribution: {self.special_deal_price_distribution}')


    def prepare_rauru_reward(self):
        # State consumed by pre_fill / fill_bosses / post_fill:
        #   self.rauru_starting_item:  reward forced at Rauru, pushed precollected immediately
        #   self.rauru_free_post_fill: extract whatever lands at Rauru post-fill into starting
        # The 9-unique-rewards invariant is preserved automatically by AP's precollected
        # processing: when push_precollected matches an item already in the pool, AP removes
        # one copy from the pool and substitutes junk - so all 8 other rewards remain.
        self.rauru_starting_item = None
        self.rauru_free_post_fill = False

        if self.skip_reward_from_rauru == 'not_free':
            return

        mode = self.shuffle_dungeon_rewards
        rauru_location = self.multiworld.get_location('ToT Reward from Rauru', self.player)

        if mode == 'vanilla':
            reward_name = rauru_location.vanilla_item
            self.rauru_starting_item = reward_name
            self._claim_rauru_starting(reward_name, rauru_location)
            return

        if mode == 'reward':
            reward_name = self.random.choice(sorted(
                self.item_name_groups['rewards'] - set(getattr(self, 'empty_dungeon_starting_rewards', []))))
            self.rauru_starting_item = reward_name
            self._claim_rauru_starting(reward_name, rauru_location)
            return

        if mode in ('dungeon', 'regional'):
            if self.skip_reward_from_rauru == 'free':
                self.rauru_free_post_fill = True
                return

            self.rauru_starting_item = 'Light Medallion'
            self._claim_rauru_starting('Light Medallion', rauru_location)
            return

        # any_dungeon / overworld / anywhere
        if self.skip_reward_from_rauru == 'free_forced':
            chosen = self.random.choice(sorted(
                self.item_name_groups['rewards'] - set(getattr(self, 'empty_dungeon_starting_rewards', []))))
            self.rauru_starting_item = chosen
            self._claim_rauru_starting(chosen, rauru_location)
            return

        self.rauru_free_post_fill = True

    def _claim_rauru_starting(self, reward_name: str, rauru_location):
        """Push a chosen reward as starting inventory and mark Rauru as a non-sendable check."""
        self.hinted_dungeon_reward_locations[reward_name] = None
        self.multiworld.push_precollected(self.create_item(reward_name))
        self._grant_rauru_skip_state()
        rauru_location.address = None
        rauru_location.show_in_spoiler = False
        if rauru_location in rauru_location.parent_region.locations:
            rauru_location.parent_region.locations.remove(rauru_location)

    def _grant_rauru_skip_state(self):
        if not any(item.name == 'Time Travel' for item in self.multiworld.precollected_items[self.player]):
            self.multiworld.push_precollected(self.create_item('Time Travel'))
        if 'Time Travel' not in self.remove_from_start_inventory:
            self.remove_from_start_inventory.append('Time Travel')


    @staticmethod
    def item_dungeon_name_from_name(item_name: str) -> Optional[str]:
        for dungeon_info in dungeon_table:
            dungeon_name = dungeon_info['name']
            if item_name.endswith(f'({dungeon_name})') or f'({dungeon_name} ' in item_name:
                return dungeon_name
        return None


    @staticmethod
    def get_dungeon_item_names(dungeon_name: str) -> set[str]:
        return {
            name for name, data in item_table.items()
            if data[0] in {'Map', 'Compass', 'SmallKey', 'BossKey', 'SilverRupee'}
            and OOTWorld.item_dungeon_name_from_name(name) == dungeon_name
        }


    def item_precompleted_dungeon_name(self, item) -> Optional[str]:
        if not getattr(item, 'restricted_dungeon_item', False):
            return None
        dungeon_name = self.item_dungeon_name_from_name(item.name)
        if dungeon_name is None:
            return None
        return dungeon_name if self.precompleted_dungeons.get(dungeon_name, False) else None


    def select_empty_dungeons_from_rewards(self, empty_dungeon_pool: list[str]) -> set[str]:
        selected_rewards = [
            reward for reward in sorted(self.empty_dungeons_rewards)
            if reward in EmptyDungeonRewards.valid_keys
        ]
        assignments = {}
        if self.shuffle_dungeon_rewards == 'reward':
            candidate_dungeons = list(empty_dungeon_pool)
            self.random.shuffle(candidate_dungeons)
            self.random.shuffle(selected_rewards)
            for reward_name, dungeon_name in zip(selected_rewards, candidate_dungeons):
                assignments[dungeon_name] = reward_name
        else:
            for reward_name in selected_rewards:
                dungeon_name = REWARD_TO_DUNGEON.get(reward_name)
                if dungeon_name in empty_dungeon_pool:
                    assignments[dungeon_name] = reward_name
        self.empty_dungeon_reward_assignments = assignments
        return set(assignments)


    @staticmethod
    def get_empty_dungeon_pool():
        empty_dungeon_names = {name.replace("'", "") for name in EmptyDungeonList.valid_keys}
        return [dungeon['name'] for dungeon in dungeon_table if dungeon['name'] in empty_dungeon_names]


    def get_empty_dungeon_reward_locations(self):
        reward_locations = {}
        for location in self.get_locations():
            if location.type != 'Boss' or location.vanilla_item not in self.item_name_groups['rewards']:
                continue
            try:
                dungeon_name = HintArea.at(location).dungeon_name
            except HintAreaNotFound:
                continue
            if dungeon_name in self.precompleted_dungeons:
                reward_locations[dungeon_name] = location
        return reward_locations


    def prepare_empty_dungeon_rewards(self):
        self.empty_dungeon_starting_rewards = []
        self.empty_dungeon_reward_location_names = set()
        if self.empty_dungeons_mode == 'none':
            return

        reward_locations = self.get_empty_dungeon_reward_locations()
        empty_reward_locations = [
            reward_locations[dungeon]
            for dungeon, is_empty in self.precompleted_dungeons.items()
            if is_empty
        ]
        if not empty_reward_locations:
            return

        reward_assignments = getattr(self, 'empty_dungeon_reward_assignments', {})
        if reward_assignments:
            reward_names = [
                reward_assignments[HintArea.at(loc).dungeon_name]
                for loc in empty_reward_locations
            ]
        elif self.shuffle_dungeon_rewards == 'reward':
            reward_pool = sorted(self.item_name_groups['rewards'])
            self.random.shuffle(reward_pool)
            reward_names = reward_pool[:len(empty_reward_locations)]
        else:
            reward_names = [loc.vanilla_item for loc in empty_reward_locations]

        for reward_name, location in zip(reward_names, empty_reward_locations):
            self.empty_dungeon_starting_rewards.append(reward_name)
            self.empty_dungeon_reward_location_names.add(location.name)
            self.hinted_dungeon_reward_locations[reward_name] = None
            self.multiworld.push_precollected(self.create_item(reward_name))
            location.place_locked_item(self.create_item('Rupee (1)'))


    def add_starting_hearts(self):
        if self.starting_hearts <= 3:
            return
        if self.options.start_inventory.value.get('Piece of Heart', 0) or self.options.start_inventory.value.get('Heart Container', 0):
            return

        hearts_to_collect = self.starting_hearts - 3
        if self.item_pool_value == 'plentiful':
            if self.starting_hearts >= 20:
                hearts_to_collect -= 1
                for _ in range(4):
                    self.multiworld.push_precollected(self.create_item('Piece of Heart'))
            for _ in range(hearts_to_collect):
                self.multiworld.push_precollected(self.create_item('Heart Container'))
            return

        for _ in range(4 * ((hearts_to_collect + 1) // 2)):
            self.multiworld.push_precollected(self.create_item('Piece of Heart'))
        for _ in range(hearts_to_collect // 2):
            self.multiworld.push_precollected(self.create_item('Heart Container'))


    def fill_bosses(self):
        mode = self.shuffle_dungeon_rewards
        if mode not in ('vanilla', 'reward'):
            return

        boss_location_names = [
            'Queen Gohma',
            'King Dodongo',
            'Barinade',
            'Phantom Ganon',
            'Volvagia',
            'Morpha',
            'Bongo Bongo',
            'Twinrova',
            'ToT Reward from Rauru'
        ]
        boss_location_names = [
            loc_name for loc_name in boss_location_names
            if loc_name not in getattr(self, 'empty_dungeon_reward_location_names', set())
        ]
        rauru_starting_item = self.rauru_starting_item
        if rauru_starting_item is not None:
            boss_location_names.remove('ToT Reward from Rauru')

        boss_rewards = sorted(map(self.create_item, self.item_name_groups['rewards']))
        boss_locations = [self.multiworld.get_location(loc, self.player) for loc in boss_location_names]

        placed_prizes = [loc.item.name for loc in boss_locations if loc.item is not None]
        if rauru_starting_item is not None:
            placed_prizes.append(rauru_starting_item)
        placed_prizes.extend(getattr(self, 'empty_dungeon_starting_rewards', []))
        prizepool = [item for item in boss_rewards if item.name not in placed_prizes]
        prize_locs = [loc for loc in boss_locations if loc.item is None]

        if mode == 'vanilla':
            # Place each reward at its specific vanilla Boss location.
            vanilla_map = {loc.vanilla_item: loc for loc in boss_locations}
            for item in list(prizepool):
                loc = vanilla_map.get(item.name)
                if loc and loc.item is None:
                    loc.place_locked_item(item)
                    self.hinted_dungeon_reward_locations[item.name] = loc
        else:  # mode == 'reward'
            while prize_locs:
                self.random.shuffle(prizepool)
                self.random.shuffle(prize_locs)
                item = prizepool.pop()
                loc = prize_locs.pop()
                loc.place_locked_item(item)
                self.hinted_dungeon_reward_locations[item.name] = loc


    # Separate the result from generate_itempool into main and prefill pools
    def divide_itempools(self):
        prefill_item_types = set()
        if self.shopsanity != 'off':
            prefill_item_types.add('Shop')
        if self.shuffle_song_items != 'any':
            prefill_item_types.add('Song')

        # Keep prefill close to upstream's restricted dungeon item pass. Items
        # that can legally leave their own dungeon are left in AP's main fill
        # and constrained by item rules instead.
        if self.shuffle_dungeon_rewards == 'dungeon':
            prefill_item_types.add('DungeonReward')

        main_items = []
        prefill_items = []
        for item in self.itempool:
            restricted_dungeon_item = getattr(item, 'restricted_dungeon_item', False)
            precompleted_dungeon_item = self.item_precompleted_dungeon_name(item) is not None
            dungeon_name = self.item_dungeon_name_from_name(item.name) if getattr(item, 'dungeonitem', False) else None
            precompleted_dungeon_extra = (
                dungeon_name is not None
                and self.precompleted_dungeons.get(dungeon_name, False)
                and not precompleted_dungeon_item
            )
            if precompleted_dungeon_extra:
                main_items.append(item)
            elif restricted_dungeon_item or item.type in prefill_item_types or precompleted_dungeon_item:
                prefill_items.append(item)
            else:
                main_items.append(item)
        return main_items, prefill_items


    # only returns proper result after create_items and divide_itempools are run
    def get_pre_fill_items(self):
        return self.pre_fill_items


    # Note on allow_arbitrary_name:
    # OoT defines many helper items and event names that are treated indistinguishably from regular items,
    #   but are only defined in the logic files. This means we need to create items for any name.
    # Allowing any item name to be created is dangerous in case of plando, so this is a middle ground.
    def create_item(self, name: str, allow_arbitrary_name: bool = False):
        if name in item_table:
            return OOTItem(name, self.player, item_table[name], False,
                           (name in self.nonadvancement_items if getattr(self, 'nonadvancement_items',
                                                                         None) else False))
        if allow_arbitrary_name:
            return OOTItem(name, self.player, ('Event', True, None, None), True, False)
        raise Exception(f"Invalid item name: {name}")

    def make_event_item(self, name, location, item=None):
        if item is None:
            item = self.create_item(name, allow_arbitrary_name=True)
        self.multiworld.push_item(location, item, collect=False)
        location.locked = True
        if name not in item_table:
            location.internal = True
        return item


    # Create regions, locations, and entrances
    def create_regions(self):
        if self.logic_rules == 'glitchless' or self.logic_rules == 'no_logic':  # enables ER + NL
            world_type = 'World'
        else:
            world_type = 'Glitched World'
        overworld_data_path = data_path(world_type, 'Overworld.json')
        bosses_data_path = data_path(world_type, 'Bosses.json')
        menu = OOTRegion('Menu', self.player, self.multiworld)
        start = OOTEntrance(self.player, self.multiworld, 'New Game', menu)
        menu.exits.append(start)
        self.multiworld.regions.append(menu)
        self.load_regions_from_json(overworld_data_path)
        self.load_regions_from_json(bosses_data_path)
        start.connect(self.get_region('Root'))
        create_dungeons(self)
        self.parser.create_delayed_rules()

        if self.shopsanity != 'off':
            self.random_shop_prices()
        self.set_scrub_prices()

        # Bind entrances to vanilla
        for region in self.regions:
            for exit in region.exits:
                exit.connect(self.get_region(exit.vanilla_connected_region))


    # Create items, starting item handling, boss prize fill (before entrance randomizer)
    def create_items(self):
        # Generate itempool
        generate_itempool(self)
        self.prepare_empty_dungeon_rewards()
        self.add_starting_hearts()
        self.prepare_rauru_reward()

        junk_pool = get_junk_pool(self)
        removed_items = []
        pool_removed_random_starting_items = Counter(self.randomized_starting_items)
        # Determine starting items
        for item in self.multiworld.precollected_items[self.player]:
            if item.name in self.remove_from_start_inventory:
                self.remove_from_start_inventory.remove(item.name)
                removed_items.append(item.name)
            else:
                self.starting_items[item.name] += 1
                if item.type == 'Song':
                    self.songs_as_items = True
                # Call the junk fill and get a replacement
                if pool_removed_random_starting_items[item.name]:
                    pool_removed_random_starting_items[item.name] -= 1
                elif item in self.itempool:
                    self.itempool.remove(item)
                    self.itempool.append(self.create_item(*get_junk_item(self.random, pool=junk_pool)))
        if self.start_with_consumables:
            self.starting_items['Deku Sticks'] = 30
            self.starting_items['Deku Nuts'] = 40
        if self.start_with_rupees:
            self.starting_items['Rupees'] = 999

        # NOTE: Silver rupees in vanilla mode are handled by ItemPool.py which places them
        # at their vanilla locations. No need to precollect here.

        # Divide itempool into prefill and main pools
        self.itempool, self.pre_fill_items = self.divide_itempools()

        self.remove_from_start_inventory.extend(removed_items)

        # Fill boss prizes. needs to happen before entrance shuffle
        self.fill_bosses()

        self.multiworld.itempool += self.itempool


    def remove_excess_junk_from_itempool(self):
        main_items = [item for item in self.multiworld.itempool if item.player == self.player]
        unfilled_locations = sum(1 for location in self.get_locations() if location.item is None)
        excess_items = len(main_items) + len(self.pre_fill_items) - unfilled_locations
        if excess_items <= 0:
            return

        removed_items = []
        for item in reversed(main_items):
            if item.excludable and not item.dungeonitem:
                self.multiworld.itempool.remove(item)
                if item in self.itempool:
                    self.itempool.remove(item)
                removed_items.append(item.name)
                if len(removed_items) == excess_items:
                    logger.debug(
                        "Removed excess OOT junk item(s) from player %s item pool: %s",
                        self.player, removed_items)
                    return

        raise FillError(
            f"OOT generated {excess_items} more items than unfilled locations for player {self.player}, "
            "but there was not enough removable junk in the main item pool."
        )


    def set_rules(self):
        # This has to run AFTER creating items but BEFORE set_entrances_based_rules
        if self.entrance_shuffle:
            # 10 attempts at shuffling entrances
            tries = 10
            while tries:
                try:
                    shuffle_random_entrances(self)
                except EntranceShuffleError as e:
                    tries -= 1
                    logger.debug(
                        f"Failed shuffling entrances for world {self.player}, retrying {tries} more times")
                    if tries == 0:
                        raise e
                    # Restore original state and delete assumed entrances
                    for entrance in self.get_shuffled_entrances():
                        if entrance.connected_region is not None:
                            entrance.disconnect()
                        entrance.connect(self.multiworld.get_region(entrance.vanilla_connected_region, self.player))
                        if entrance.assumed:
                            assumed_entrance = entrance.assumed
                            if assumed_entrance.connected_region is not None:
                                assumed_entrance.disconnect()
                            del assumed_entrance
                        entrance.reverse = None
                        entrance.replaces = None
                        entrance.assumed = None
                        entrance.shuffled = False
                    # Clean up root entrances
                    root = self.get_region("Root Exits")
                    root.exits = root.exits[:8]
                else:
                    break

        set_rules(self)
        set_entrances_based_rules(self)


    def generate_basic(self):  # mostly killing locations that shouldn't exist by settings

        # Gather items for ice trap appearances
        self.fake_items = []
        if self.ice_trap_appearance in ['major_only', 'anything']:
            self.fake_items.extend(item for item in self.itempool if item.index and self.is_major_item(item))
        if self.ice_trap_appearance in ['junk_only', 'anything']:
            self.fake_items.extend(item for item in self.itempool if
                                   item.index and not item.type == 'Shop' and not self.is_major_item(item) and item.name != 'Ice Trap')

        # Kill unreachable events that can't be gotten even with all items
        # Make sure to only kill actual internal events, not in-game "events"
        all_state = self.get_state_with_complete_itempool()
        all_locations = self.get_locations()
        all_state.sweep_for_advancements(locations=all_locations)
        reachable = self.multiworld.get_reachable_locations(all_state, self.player)
        unreachable = [loc for loc in all_locations if
                       (loc.internal or loc.type == 'Drop') and loc.address is None and loc.locked and loc not in reachable]
        for loc in unreachable:
            loc.parent_region.locations.remove(loc)
        # Exception: Sell Big Poe is an event which is only reachable if Bottle with Big Poe is in the item pool.
        # We allow it to be removed only if Bottle with Big Poe is not in the itempool.
        bigpoe = self.multiworld.get_location('Sell Big Poe from Market Guard House', self.player)
        if not all_state.has('Bottle with Big Poe', self.player) and bigpoe not in reachable:
            bigpoe.parent_region.locations.remove(bigpoe)

        # If free scarecrow then Pierre is unreachable as a separate location.
        if self.scarecrow_behavior == 'free':
            loc = self.multiworld.get_location("Pierre", self.player)
            loc.parent_region.locations.remove(loc)
        # If open zora's domain then we need to kill Deliver Rutos Letter
        if self.zora_fountain == 'open':
            loc = self.multiworld.get_location("Deliver Rutos Letter", self.player)
            loc.parent_region.locations.remove(loc)
        if not self.shuffle_100_skulltula_rupee:
            loc = self.multiworld.get_location("Kak 100 Gold Skulltula Reward", self.player)
            loc.parent_region.locations.remove(loc)
        if self.shuffle_gerudo_fortress_heart_piece != 'shuffle':
            loc = self.multiworld.get_location("GF Freestanding PoH", self.player)
            loc.parent_region.locations.remove(loc)

        # Exclude locations in Ganon's Castle proportional to the number of items required to make the bridge
        # Check for dungeon ER later
        if self.logic_rules == 'glitchless':
            if self.bridge == 'medallions':
                ganon_junk_fill = self.bridge_medallions / 9
            elif self.bridge == 'stones':
                ganon_junk_fill = self.bridge_stones / 9
            elif self.bridge == 'dungeons':
                ganon_junk_fill = self.bridge_rewards / 9
            elif self.bridge == 'vanilla':
                ganon_junk_fill = 2 / 9
            elif self.bridge == 'tokens':
                ganon_junk_fill = self.bridge_tokens / 100
            elif self.bridge == 'hearts':
                remaining_hearts = 20 - self.starting_hearts
                ganon_junk_fill = (
                    max(0, self.bridge_hearts - self.starting_hearts) / remaining_hearts
                    if remaining_hearts else 0
                )
            elif self.bridge == 'open':
                ganon_junk_fill = 0
            else:
                raise Exception("Unexpected bridge setting")

            ganon_junk_fill = min(1, ganon_junk_fill)
            gc = next(filter(lambda dungeon: dungeon.name == 'Ganons Castle', self.dungeons))
            locations = [loc.name for region in gc.regions for loc in region.locations if loc.item is None]
            junk_fill_locations = self.random.sample(locations, round(len(locations) * ganon_junk_fill))
            exclusion_rules(self.multiworld, self.player, junk_fill_locations)

        for loc in self.get_locations():
            if loc.address is not None and (
                    not loc.show_in_spoiler or oot_is_item_of_type(loc.item, 'Shop')
                    or (self.skip_child_zelda and loc.name in ['HC Zeldas Letter', 'Song from Impa'])):
                loc.address = None

        self.remove_excess_junk_from_itempool()


    def fill_hook(self, progitempool, usefulitempool, filleritempool, fill_locations):
        if self.empty_dungeons_mode == 'none':
            return

        empty_locations = []
        fill_location_set = set(fill_locations)
        for location in self.get_locations():
            if location.player != self.player or location.item is not None:
                continue
            dungeon = getattr(location.parent_region, 'dungeon', None)
            if dungeon is None:
                continue
            dungeon_name = dungeon.name
            if self.precompleted_dungeons.get(dungeon_name, False):
                if location in fill_location_set:
                    empty_locations.append(location)

        if not empty_locations:
            return

        empty_locations_by_dungeon = {}
        for location in empty_locations:
            dungeon_name = location.parent_region.dungeon.name
            empty_locations_by_dungeon.setdefault(dungeon_name, []).append(location)
        for dungeon_locations in empty_locations_by_dungeon.values():
            self.random.shuffle(dungeon_locations)

        def remove_nonprogression_item(item):
            if item in filleritempool:
                filleritempool.remove(item)
                return True
            if item in usefulitempool:
                usefulitempool.remove(item)
                return True
            return False

        def place_empty_item(location, item):
            fill_locations.remove(location)
            empty_locations.remove(location)
            self.multiworld.push_item(location, item, collect=False)

        for location in empty_locations[:getattr(self, 'empty_dungeon_free_junk_count', 0)]:
            place_empty_item(location, self.create_item('Rupee (1)'))

        local_nonprogression_items = [
            item for item in filleritempool
            if item.player == self.player
        ]
        local_nonprogression_items.extend(
            item for item in usefulitempool
            if item.player == self.player and not item.advancement
        )
        self.random.shuffle(local_nonprogression_items)

        # Preserve upstream's empty dungeon rule for dungeon items: items from a
        # precompleted dungeon stay in their own dungeon before generic junk fill.
        for item in list(local_nonprogression_items):
            dungeon_name = self.item_precompleted_dungeon_name(item)
            if dungeon_name is None:
                continue
            dungeon_locations = empty_locations_by_dungeon.get(dungeon_name)
            if not dungeon_locations:
                continue
            location = dungeon_locations.pop()
            if remove_nonprogression_item(item):
                local_nonprogression_items.remove(item)
                place_empty_item(location, item)

        nonprogression_items = [
            item for item in filleritempool
            if item.player == self.player and not getattr(item, 'dungeonitem', False)
        ]
        if len(nonprogression_items) < len(empty_locations):
            nonprogression_items.extend(
                item for item in usefulitempool
                if (item.player == self.player
                    and not item.advancement
                    and not getattr(item, 'dungeonitem', False))
            )
        if len(nonprogression_items) < len(empty_locations):
            raise FillError(
                f"OoT (Player {self.player}): not enough local non-progression items to fill "
                f"pre-completed dungeons.")

        self.random.shuffle(empty_locations)
        self.random.shuffle(nonprogression_items)
        for location, item in zip(empty_locations, nonprogression_items):
            remove_nonprogression_item(item)
            fill_locations.remove(location)
            self.multiworld.push_item(location, item, collect=False)


    def pre_fill(self):

        placed_prefill_items = []

        def prefill_state(base_state, excluded_items=None, collect_placed_items=True):
            excluded_item_ids = {id(item) for item in excluded_items or ()}
            state = base_state.copy()
            # Trial states may exclude keys/songs from the copied base state. OoT's
            # age/time reachability caches are monotonic, so clear them before
            # checking candidate locations or a stricter trial can inherit access
            # from a less restricted one.
            state.child_reachable_regions[self.player] = set()
            state.adult_reachable_regions[self.player] = set()
            state.child_blocked_connections[self.player] = set()
            state.adult_blocked_connections[self.player] = set()
            state.day_reachable_regions[self.player] = set()
            state.dampe_reachable_regions[self.player] = set()
            state._oot_stale[self.player] = True
            for item in placed_prefill_items:
                if id(item) in excluded_item_ids:
                    continue
                if not collect_placed_items:
                    continue
                self.collect(state, item)
            for item in self.get_pre_fill_items():
                if id(item) in excluded_item_ids:
                    continue
                self.collect(state, item)
            state.sweep_for_advancements(locations=self.get_locations())
            return state

        # Prefill shops, songs, and dungeon items
        items = self.get_pre_fill_items()
        locations = list(self.multiworld.get_unfilled_locations(self.player))
        self.random.shuffle(locations)

        def base_prefill_state(
            assume_song_of_time=True,
            assume_time_travel=True,
            assume_dungeon_rewards=True,
        ):
            # During prefill we assume every non-prefill item for this player could be found eventually.
            # Use the MultiWorld itempool here so rewards shuffled out of boss locations are also included.
            state = CollectionState(self.multiworld)
            for item in self.multiworld.itempool:
                if item.player == self.player:
                    if not assume_song_of_time and item.name == 'Song of Time':
                        continue
                    if not assume_time_travel and item.name == 'Time Travel':
                        continue
                    self.collect(state, item)
            if assume_dungeon_rewards:
                for loc in self.get_locations():
                    if loc.item is not None and loc.item.player == self.player and loc.item.type == 'DungeonReward':
                        self.collect(state, loc.item)

            # Some progression is intentionally not represented in the item pool.
            if self.scarecrow_behavior == 'free':
                state.collect(self.create_item("Scarecrow Song"), prevent_sweep=True)
            if not self.shuffle_ocarinas:
                state.collect(self.create_item("Ocarina"), prevent_sweep=True)
            if 'Weird Egg' not in self.shuffle_child_trade and 'Chicken' not in self.shuffle_child_trade:
                state.collect(self.create_item("Weird Egg"), prevent_sweep=True)
            if 'Zeldas Letter' not in self.shuffle_child_trade:
                state.collect(self.create_item("Zeldas Letter"), prevent_sweep=True)
            if assume_song_of_time and self.open_door_of_time not in ('open', 'stones'):
                state.collect(self.create_item("Song of Time"), prevent_sweep=True)
            # Dungeon/key prefill works with a complete-state assumption. Song
            # placement disables this when it would create a Song of Time cycle.
            if assume_time_travel:
                state.collect(self.create_item("Time Travel"), prevent_sweep=True)

            state.sweep_for_advancements(locations=self.get_locations())
            return state

        state = base_prefill_state()

        def remove_prefill_item(item):
            for index, prefill_item in enumerate(self.pre_fill_items):
                if prefill_item is item:
                    del self.pre_fill_items[index]
                    return
            raise ValueError(f"Could not remove prefill item by identity: {item}")

        # Pre-completed dungeons remain beatable but barren. Their traversal
        # items are still placed in the dungeon; non-required dungeon items are
        # discarded and replaced with green rupees in fill_hook.
        self.empty_dungeon_free_junk_count = 0
        empty_dungeon_payload_items = [
            item for item in self.pre_fill_items
            if (self.item_precompleted_dungeon_name(item) is not None
                and item.type not in {'SmallKey', 'BossKey', 'SilverRupee'})
        ]
        for item in empty_dungeon_payload_items:
            remove_prefill_item(item)
            self.empty_dungeon_free_junk_count += 1

        # Empty dungeons keep the traversal layout vanilla. This avoids making a
        # live-but-barren dungeon fail full accessibility because a key or
        # silver rupee puzzle item was shuffled behind itself.
        empty_dungeon_required_items = [
            item for item in self.pre_fill_items
            if (self.item_precompleted_dungeon_name(item) is not None
                and item.type in {'SmallKey', 'BossKey', 'SilverRupee'})
        ]

        def empty_dungeon_vanilla_locations(item):
            dungeon_name = self.item_precompleted_dungeon_name(item)
            vanilla_item_names = {item.name}
            if item.name.startswith('Small Key Ring ('):
                vanilla_item_names.add(f"Small Key ({dungeon_name})")
            return [
                location for location in self.multiworld.get_unfilled_locations(player=self.player)
                if (getattr(location.parent_region, 'dungeon', None) is not None
                    and location.parent_region.dungeon.name == dungeon_name
                    and location.vanilla_item in vanilla_item_names)
            ]

        for item in empty_dungeon_required_items:
            locations = empty_dungeon_vanilla_locations(item)
            if not locations:
                continue
            location = locations[0]
            remove_prefill_item(item)
            self.multiworld.push_item(location, item, collect=False)
            location.locked = True
            placed_prefill_items.append(item)

        # Place dungeon items
        special_fill_types = [
            'SmallKey', 'GanonBossKey', 'BossKey', 'HideoutSmallKey',
            'Map', 'Compass', 'SilverRupee',
        ]
        type_to_setting = {
            'Map': 'shuffle_map',
            'Compass': 'shuffle_compass',
            'SmallKey': 'shuffle_smallkeys',
            'BossKey': 'shuffle_bosskeys',
            'HideoutSmallKey': 'shuffle_hideoutkeys',
            'GanonBossKey': 'shuffle_ganon_bosskey',
            'SilverRupee': 'shuffle_silver_rupees',
        }
        special_fill_types.sort(key=lambda x: 0 if getattr(self, type_to_setting[x]) == 'dungeon' else 1)

        for fill_stage in special_fill_types:
            stage_items = list(filter(lambda item: oot_is_item_of_type(item, fill_stage), self.pre_fill_items))
            if not stage_items:
                continue
            if fill_stage in ['GanonBossKey', 'HideoutSmallKey']:
                locations = gather_locations(self.multiworld, fill_stage, self.player)
                if isinstance(locations, list):
                    for item in stage_items:
                        remove_prefill_item(item)
                    placement_items = stage_items[:]
                    self.random.shuffle(locations)
                    fill_restrictive(self.multiworld, prefill_state(state, excluded_items=placement_items),
                        locations, placement_items[:],
                        single_player_placement=True, lock=True, allow_excluded=True,
                        on_place=lambda loc: placed_prefill_items.append(loc.item))
            else:
                for dungeon_info in dungeon_table:
                    dungeon_name = dungeon_info['name']
                    dungeon_items = list(filter(lambda item: dungeon_name in item.name, stage_items))
                    if not dungeon_items:
                        continue
                    if self.precompleted_dungeons.get(dungeon_name, False):
                        locations = [
                            location for location in self.multiworld.get_unfilled_locations(player=self.player)
                            if valid_dungeon_item_location(self, 'dungeon', dungeon_name, location)
                        ]
                    else:
                        locations = gather_locations(self.multiworld, fill_stage, self.player, dungeon=dungeon_name)
                    if not isinstance(locations, list):
                        continue
                    for item in dungeon_items:
                        remove_prefill_item(item)
                    placement_items = dungeon_items[:]
                    self.random.shuffle(locations)
                    fill_restrictive(self.multiworld, prefill_state(state, excluded_items=placement_items),
                        locations, placement_items[:],
                        single_player_placement=True, lock=True, allow_excluded=True,
                        on_place=lambda loc: placed_prefill_items.append(loc.item))

        # Place songs
        # 15 built-in retries because this section can fail sometimes
        if self.shuffle_song_items != 'any':
            max_song_tries = 15
            tries = max_song_tries
            if self.shuffle_song_items == 'song':
                song_locations = list(filter(lambda location: location.type == 'Song',
                                             self.multiworld.get_unfilled_locations(player=self.player)))
            elif self.shuffle_song_items == 'dungeon':
                song_locations = list(filter(lambda location: location.name in dungeon_song_locations,
                                             self.multiworld.get_unfilled_locations(player=self.player)))
            else:
                raise Exception(f"Unknown song shuffle type: {self.shuffle_song_items}")

            songs = list(filter(lambda item: item.type == 'Song', self.pre_fill_items))
            for song in songs:
                self.pre_fill_items.remove(song)
            song_of_time = next((song for song in songs if song.name == 'Song of Time'), None)
            song_of_time_opens_door = (
                song_of_time is not None
                and self.open_door_of_time not in ('open', 'stones')
            )

            important_warps = (self.shuffle_special_interior_entrances or self.shuffle_overworld_entrances or
                               self.warp_songs or self.spawn_positions)
            song_order = {
                'Zeldas Lullaby': 1,
                'Eponas Song': 1,
                'Sarias Song': 3 if important_warps else 0,
                'Suns Song': 0,
                'Song of Time': 0,
                'Song of Storms': 3,
                'Minuet of Forest': 2 if important_warps else 0,
                'Bolero of Fire': 2 if important_warps else 0,
                'Serenade of Water': 2 if important_warps else 0,
                'Requiem of Spirit': 2,
                'Nocturne of Shadow': 2,
                'Prelude of Light': 2 if important_warps else 0,
            }
            songs.sort(key=lambda song: song_order.get(song.name, 0))

            while tries:
                placed_prefill_item_count = len(placed_prefill_items)
                try:
                    self.random.shuffle(song_locations)
                    if self.shuffle_song_items == 'dungeon':
                        song_locations.sort(key=lambda location: 0 if location.name == 'Sheik in Ice Cavern' else 1)
                    song_base_state = base_prefill_state(assume_dungeon_rewards=False)
                    if song_of_time_opens_door:
                        song_of_time_state = prefill_state(base_prefill_state(
                            assume_song_of_time=False,
                            assume_time_travel=False,
                            assume_dungeon_rewards=False,
                        ))
                        fill_restrictive(self.multiworld, song_of_time_state, song_locations[:], [song_of_time],
                            single_player_placement=True, lock=True, allow_excluded=True,
                            on_place=lambda loc: placed_prefill_items.append(loc.item))
                    song_state = prefill_state(song_base_state)
                    remaining_songs = [song for song in songs if song.location is None]
                    remaining_song_locations = [location for location in song_locations if location.item is None]

                    fill_restrictive(self.multiworld, song_state, remaining_song_locations, remaining_songs,
                                     single_player_placement=True, lock=True, allow_excluded=True,
                                     on_place=lambda loc: placed_prefill_items.append(loc.item))
                    logger.debug(
                        f"Successfully placed songs for player {self.player} "
                        f"after {max_song_tries + 1 - tries} attempt(s)")
                except FillError as e:
                    del placed_prefill_items[placed_prefill_item_count:]
                    tries -= 1
                    if tries == 0:
                        raise Exception(f"Failed placing songs for player {self.player}. Error cause: {e}")
                    logger.debug(f"Failed placing songs for player {self.player}. Retries left: {tries}")
                    # undo what was done
                    for song in songs:
                        song.location = None
                        song.world = None
                    for location in song_locations:
                        location.item = None
                        location.locked = False
                else:
                    break

        # Place dungeon rewards after dungeon items and songs. Rewards can be required
        # for bridge/Ganon access, so AP needs to place them with the real prefill state
        # instead of locking them randomly before reachability-sensitive fill.
        # `anywhere` skips this stage - those rewards stay in the main itempool.
        if self.shuffle_dungeon_rewards in ('dungeon', 'regional', 'any_dungeon', 'overworld'):
            reward_items = list(filter(lambda item: item.type == 'DungeonReward', self.pre_fill_items))
            placed_reward_names = {self.rauru_starting_item} if self.rauru_starting_item else set()
            reward_items = [r for r in reward_items if r.name not in placed_reward_names]

            mode = self.shuffle_dungeon_rewards
            # Place hardest-to-place rewards first - Light Medallion under `dungeon` mode is the
            # most constrained (only Temple of Time region) so attempt it first to fail fast.
            reward_items.sort(key=lambda r: 0 if (mode == 'dungeon' and r.name == 'Light Medallion') else 1)

            for reward in reward_items:
                self.pre_fill_items.remove(reward)
                candidate_locations = [
                    loc for loc in self.multiworld.get_unfilled_locations(player=self.player)
                    if valid_reward_location(self, mode, reward.name, loc)
                ]
                if not candidate_locations:
                    raise FillError(
                        f"OoT (Player {self.player}): no valid location for {reward.name} "
                        f"in {mode} reward shuffle.")
                self.random.shuffle(candidate_locations)
                fill_restrictive(self.multiworld, prefill_state(state), candidate_locations, [reward],
                    single_player_placement=True, lock=True, allow_excluded=True,
                    on_place=lambda loc: placed_prefill_items.append(loc.item))
                self.hinted_dungeon_reward_locations[reward.name] = reward.location

        # Place shop items
        # fast fill will fail because there is some logic on the shop items. we'll gather them up and place the shop items
        if self.shopsanity != 'off':
            shop_prog = list(filter(lambda item: item.type == 'Shop' and item.advancement, self.pre_fill_items))
            shop_junk = list(filter(lambda item: item.type == 'Shop' and not item.advancement, self.pre_fill_items))
            shop_locations = list(
                filter(lambda location: location.type == 'Shop' and location.name not in self.shop_prices,
                       self.multiworld.get_unfilled_locations(player=self.player)))
            shop_locations_to_hide = shop_locations.copy()
            shop_prog.sort(key=lambda item: {
                'Buy Deku Shield': 2 * int(self.open_forest == 'closed'),
                'Buy Goron Tunic': 1,
                'Buy Zora Tunic': 1,
            }.get(item.name, 0))  # place Deku Shields if needed, then tunics, then other advancement
            self.random.shuffle(shop_locations)
            self.pre_fill_items = []  # all prefill should be done
            fill_restrictive(self.multiworld, prefill_state(state), shop_locations, shop_prog,
                single_player_placement=True, lock=True, allow_excluded=True)
            fast_fill(self.multiworld, shop_junk, shop_locations)
            for loc in shop_locations_to_hide:
                loc.locked = True
                loc.address = None
                loc.show_in_spoiler = False
        set_shop_rules(self)  # sets wallet requirements on shop items, must be done after they are filled

    def post_fill(self):
        if self.rauru_free_post_fill:
            rauru_loc = self.multiworld.get_location('ToT Reward from Rauru', self.player)
            extracted = rauru_loc.item
            if extracted is not None:
                if extracted.location is rauru_loc:
                    extracted.location = None
                rauru_loc.item = None

                for index, item in enumerate(self.multiworld.itempool):
                    if item is extracted:
                        self.multiworld.itempool.pop(index)
                        break

                if extracted.name != 'Nothing':
                    target_world = self.multiworld.worlds[extracted.player]
                    if hasattr(target_world, 'starting_items'):
                        target_world.starting_items[extracted.name] += 1
                    self.multiworld.push_precollected(extracted)

                if (extracted.name != 'Nothing'
                        and isinstance(extracted, OOTItem)
                        and extracted.type == 'DungeonReward'):
                    self.hinted_dungeon_reward_locations[extracted.name] = None

                self._grant_rauru_skip_state()
                rauru_loc.address = None
                rauru_loc.show_in_spoiler = False
                if rauru_loc in rauru_loc.parent_region.locations:
                    rauru_loc.parent_region.locations.remove(rauru_loc)

        if self.shuffle_dungeon_rewards in ('dungeon', 'regional', 'any_dungeon', 'overworld', 'anywhere'):
            reward_names = set(self.item_name_groups['rewards'])
            sentinel = object()
            for loc in self.multiworld.get_filled_locations():
                if loc.item is None:
                    continue
                if loc.item.player != self.player:
                    continue
                if loc.item.name not in reward_names:
                    continue
                current = self.hinted_dungeon_reward_locations.get(loc.item.name, sentinel)
                if current is sentinel:
                    self.hinted_dungeon_reward_locations[loc.item.name] = loc


    def generate_output(self, output_directory: str):

        # Write entrances to spoiler log
        all_entrances = self.get_shuffled_entrances()
        all_entrances.sort(reverse=True, key=lambda x: (x.type, x.name))
        if not self.decouple_entrances:
            while all_entrances:
                loadzone = all_entrances.pop()
                if loadzone.type != 'Overworld':
                    if loadzone.primary:
                        entrance = loadzone
                    else:
                        entrance = loadzone.reverse
                    if entrance.reverse is not None:
                        self.multiworld.spoiler.set_entrance(entrance, entrance.replaces.reverse, 'both', self.player)
                    else:
                        self.multiworld.spoiler.set_entrance(entrance, entrance.replaces, 'entrance', self.player)
                else:
                    reverse = loadzone.replaces.reverse
                    if reverse in all_entrances:
                        all_entrances.remove(reverse)
                    self.multiworld.spoiler.set_entrance(loadzone, reverse, 'both', self.player)
        else:
            for entrance in all_entrances:
                self.multiworld.spoiler.set_entrance(entrance, entrance.replaces, 'entrance', self.player)

        if self.hints != 'none' or self.misc_hints:
            self.hint_data_available.wait()

        with i_o_limiter:
            # Make traps appear as other random items
            trap_location_ids = [loc.address for loc in self.get_locations() if loc.item.trap]
            self.trap_appearances = {}
            for loc_id in trap_location_ids:
                self.trap_appearances[loc_id] = self.create_item(self.random.choice(self.fake_items).name)

            # Seed hint RNG, used for ganon text lines also
            self.hint_rng = self.random

            outfile_name = self.multiworld.get_out_file_name_base(self.player)
            oot_settings = OOTWorld.settings
            rom = Rom(file=oot_settings.rom_file)
            try:
                if self.hints != 'none':
                    buildWorldGossipHints(self)
                patch_rom(self, rom)
                patch_cosmetics(self, rom)
            except Exception as e:
                logger.exception("Failed while generating OoT output for player %s.", self.player)
                raise e
            finally:
                self.collectible_flags_available.set()
            rom.update_header()
            patch_data = create_patch_file(rom, self.random)
            rom.restore()

            apz5 = OoTContainer(patch_data, outfile_name, output_directory,
                player=self.player,
                player_name=self.multiworld.get_player_name(self.player))
            apz5.write()


    # Gathers hint data for OoT. Loops over all world locations for woth, barren, and major item locations.
    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        oot_worlds = list(multiworld.get_game_worlds(cls.game))

        def hint_type_players(hint_type: str) -> set:
            return {autoworld.player for autoworld in oot_worlds
                    if autoworld.hints != 'none' 
                    and autoworld.hint_dist_user['distribution'][hint_type]['copies'] > 0
                    and (autoworld.hint_dist_user['distribution'][hint_type]['fixed'] > 0 
                      or autoworld.hint_dist_user['distribution'][hint_type]['weight'] > 0)}

        try:
            item_hint_players = hint_type_players('item')
            barren_hint_players = hint_type_players('barren')
            woth_hint_players = hint_type_players('woth')

            items_by_region = {}
            for player in barren_hint_players:
                items_by_region[player] = {}
                for r in multiworld.worlds[player].regions:
                    if r.hint:
                        items_by_region[player][r.hint] = {'dungeon': False, 'weight': 0, 'is_barren': True}
                for d in multiworld.worlds[player].dungeons:
                    items_by_region[player][HintArea.for_dungeon(d.name)] = {'dungeon': True, 'weight': 0, 'is_barren': True}
                items_by_region[player].pop(HintArea.ROOT, None)

            if item_hint_players:  # loop once over all locations to gather major items. Check oot locations for barren/woth if needed
                for loc in multiworld.get_locations():
                    player = loc.item.player
                    autoworld = multiworld.worlds[player]
                    if ((player in item_hint_players and (autoworld.is_major_item(loc.item) or loc.item.name in autoworld.item_added_hint_types['item']))
                                or (loc.player in item_hint_players and loc.name in multiworld.worlds[loc.player].added_hint_types['item'])):
                        autoworld.major_item_locations.append(loc)

                    if loc.game == cls.game and loc.item.code and (not loc.locked or
                        (oot_is_item_of_type(loc.item, 'Song') or
                            (oot_is_item_of_type(loc.item, 'SmallKey')         and multiworld.worlds[loc.player].shuffle_smallkeys     in ('overworld', 'any_dungeon', 'regional')) or
                            (oot_is_item_of_type(loc.item, 'HideoutSmallKey')  and multiworld.worlds[loc.player].shuffle_hideoutkeys   in ('overworld', 'any_dungeon', 'regional')) or
                            (oot_is_item_of_type(loc.item, 'BossKey')          and multiworld.worlds[loc.player].shuffle_bosskeys      in ('overworld', 'any_dungeon', 'regional')) or
                            (oot_is_item_of_type(loc.item, 'GanonBossKey')     and multiworld.worlds[loc.player].shuffle_ganon_bosskey in ('overworld', 'any_dungeon', 'regional')))):
                        if loc.player in barren_hint_players:
                            hint_area = get_hint_area(loc)
                            items_by_region[loc.player][hint_area]['weight'] += 1
                            if loc.item.advancement or loc.item.useful:
                                items_by_region[loc.player][hint_area]['is_barren'] = False
                        if loc.player in woth_hint_players and loc.item.advancement:
                            # Skip item at location and see if game is still beatable
                            state = CollectionState(multiworld)
                            state.locations_checked.add(loc)
                            if not multiworld.can_beat_game(state):
                                multiworld.worlds[loc.player].required_locations.append(loc)
            elif barren_hint_players or woth_hint_players:  # Check only relevant oot locations for barren/woth
                for player in (barren_hint_players | woth_hint_players):
                    for loc in multiworld.worlds[player].get_locations():
                        if loc.item.code and (not loc.locked or
                            (oot_is_item_of_type(loc.item, 'Song') or
                                (oot_is_item_of_type(loc.item, 'SmallKey')         and multiworld.worlds[loc.player].shuffle_smallkeys     in ('overworld', 'any_dungeon', 'regional')) or
                                (oot_is_item_of_type(loc.item, 'HideoutSmallKey')  and multiworld.worlds[loc.player].shuffle_hideoutkeys   in ('overworld', 'any_dungeon', 'regional')) or
                                (oot_is_item_of_type(loc.item, 'BossKey')          and multiworld.worlds[loc.player].shuffle_bosskeys      in ('overworld', 'any_dungeon', 'regional')) or
                                (oot_is_item_of_type(loc.item, 'GanonBossKey')     and multiworld.worlds[loc.player].shuffle_ganon_bosskey in ('overworld', 'any_dungeon', 'regional')))):
                            if player in barren_hint_players:
                                hint_area = get_hint_area(loc)
                                items_by_region[player][hint_area]['weight'] += 1
                                if loc.item.advancement or loc.item.useful:
                                    items_by_region[player][hint_area]['is_barren'] = False
                            if player in woth_hint_players and loc.item.advancement:
                                state = CollectionState(multiworld)
                                state.locations_checked.add(loc)
                                if not multiworld.can_beat_game(state):
                                    multiworld.worlds[player].required_locations.append(loc)
            for player in barren_hint_players:
                multiworld.worlds[player].empty_areas = {region: info for (region, info) in items_by_region[player].items()
                                                    if info['is_barren']}
            populate_misc_hint_data(oot_worlds)
        except Exception as e:
            raise e
        finally:
            for autoworld in oot_worlds:
                autoworld.hint_data_available.set()


    def fill_slot_data(self):
        self.collectible_flags_available.wait()
        if not self.shop_location_flags:
            self.shop_location_flags = self.calculate_shop_location_flags()

        slot_data = {
            'collectible_override_flags': self.collectible_override_flags,
            'collectible_flag_offsets': self.collectible_flag_offsets,
            'shop_flag_offsets': self.shop_location_flags,
        }
        slot_data.update(self.options.as_dict(
            "open_forest", "open_kakariko", "open_door_of_time", "zora_fountain", "gerudo_fortress",
            "bridge", "bridge_stones", "bridge_medallions", "bridge_rewards", "bridge_tokens", "bridge_hearts",
            "shuffle_ganon_bosskey", "ganon_bosskey_medallions", "ganon_bosskey_stones", "ganon_bosskey_rewards",
            "ganon_bosskey_tokens", "ganon_bosskey_hearts", "trials",
            "triforce_hunt", "triforce_goal", "extra_triforce_percentage",
            "shopsanity", "shop_slots", "special_deal_price_distribution", "special_deal_price_min",
            "special_deal_price_max", "tokensanity",
            "dungeon_shortcuts", "dungeon_shortcuts_list",
            "mq_dungeons_mode", "mq_dungeons_list", "mq_dungeons_count",
            "empty_dungeons_mode", "empty_dungeons_list", "empty_dungeons_rewards", "empty_dungeons_count",
            "shuffle_interior_entrances", "shuffle_grotto_entrances", "shuffle_dungeon_entrances",
            "shuffle_overworld_entrances", "shuffle_bosses", "shuffle_ganon_tower", "key_rings", "key_rings_list", "enhance_map_compass",
            "shuffle_map", "shuffle_compass", "shuffle_smallkeys", "shuffle_hideoutkeys", "shuffle_bosskeys",
            "logic_rules", "logic_no_night_tokens_without_suns_song", "allowed_tricks", "advanced_allowed_tricks",
            "warp_songs", "shuffle_song_items", "ocarina_songs", "shuffle_expensive_merchants",
            "shuffle_frog_song_rupees",
            "shuffle_100_skulltula_rupee",
            "shuffle_scrubs", "shuffle_child_trade", "shuffle_freestanding_items", "shuffle_pots", "shuffle_empty_pots", "shuffle_crates",
            "shuffle_empty_crates",
            "shuffle_cows", "shuffle_beehives", "shuffle_wonderitems", "shuffle_kokiri_sword", "shuffle_ocarinas", "shuffle_gerudo_card",
            "shuffle_beans", "shuffle_gerudo_fortress_heart_piece", "starting_age", "free_bombchu_drops", "spawn_positions", "owl_drops",
            "no_epona_race", "skip_some_minigame_phases", "complete_mask_quest", "scarecrow_behavior", "plant_beans", "easier_fire_arrow_entry", "fast_shadow_boat", "skip_reward_from_rauru",
            "chicken_count", "big_poe_count", "fae_torch_count", "blue_fire_arrows",
            "damage_multiplier", "deadly_bonks", "starting_tod", "junk_ice_traps", "custom_ice_trap_count", "custom_ice_trap_percent",
            "start_with_consumables", "starting_hearts", "add_random_starting_items", "random_starting_items_count",
            "random_starting_items_exclude", "adult_trade_start", "plando_connections"
            )
        )

        if not self.multiworld.is_race:
            dungeon_reward_locations = {}
            for reward_name, location in self.hinted_dungeon_reward_locations.items():
                if location is None:
                    dungeon_reward_locations[reward_name] = None
                elif location.player != self.player:
                    dungeon_reward_locations[reward_name] = "Another World"
                else:
                    try:
                        dungeon_reward_locations[reward_name] = HintArea.at(location).short_name
                    except Exception:
                        dungeon_reward_locations[reward_name] = None
            slot_data['dungeon_reward_locations'] = dungeon_reward_locations

            def boss_name_for_region(region):
                checked_regions = set()
                regions = [region]
                while regions:
                    current_region = regions.pop(0)
                    if current_region.name in checked_regions:
                        continue
                    checked_regions.add(current_region.name)
                    for location in current_region.locations:
                        if location.type == 'Boss' or location.name == 'Ganon':
                            return location.name
                    regions.extend(
                        region_exit.connected_region for region_exit in current_region.exits
                        if region_exit.connected_region is not None and region_exit.connected_region.is_boss_room
                    )
                return region.name

            dungeon_bosses = {}
            for entrance in (self.get_shufflable_entrances(type='ChildBoss', only_primary=True) +
                             self.get_shufflable_entrances(type='AdultBoss', only_primary=True) +
                             self.get_shufflable_entrances(type='SpecialBoss', only_primary=True)):
                if entrance.type == 'SpecialBoss':
                    dungeon_name = 'Ganons Tower'
                else:
                    try:
                        dungeon_name = HintArea.at(entrance.parent_region).dungeon_name
                    except Exception:
                        continue
                dungeon_bosses[dungeon_name] = boss_name_for_region(entrance.connected_region)
            slot_data['dungeon_bosses'] = dungeon_bosses

        return slot_data


    def modify_multidata(self, multidata: dict):

        # Replace connect name
        multidata['connect_names'][self.connect_name] = multidata['connect_names'][self.multiworld.player_name[self.player]]

        # Remove undesired items from start_inventory
        # This is because we don't want them to show up in the autotracker,
        # they just don't exist in-game.
        for item_name in self.remove_from_start_inventory:
            item_id = self.item_name_to_id.get(item_name, None)
            if item_id is None:
                continue
            multidata["precollected_items"][self.player].remove(item_id)

        # If skip child zelda, push item onto autotracker
        if self.skip_child_zelda:
            impa_item_id = self.item_name_to_id.get(self.get_location('Song from Impa').item.name, None)
            zelda_item_id = self.item_name_to_id.get(self.get_location('HC Zeldas Letter').item.name, None)
            if impa_item_id:
                multidata["precollected_items"][self.player].append(impa_item_id)
            if zelda_item_id:
                multidata["precollected_items"][self.player].append(zelda_item_id)


    def extend_hint_information(self, er_hint_data: dict):

        er_hint_data[self.player] = {}

        hint_entrances = set()
        for entrance in entrance_shuffle_table:
            if entrance[0] in {'Dungeon', 'DungeonSpecial', 'Interior', 'SpecialInterior', 'Grotto', 'Grave'}:
                hint_entrances.add(entrance[1][0])

        # Get main hint entrance to region.
        # If the region is directly adjacent to a hint-entrance, we return that one.
        # If it's in a dungeon, scan all the entrances for all the regions in the dungeon.
        #   This should terminate on the first region anyway, but we scan everything to be safe.
        # If it's one of the special cases, go one level deeper.
        # If it's a boss room, go one level deeper to the boss door region, which is in a dungeon.
        # Otherwise return None.
        def get_entrance_to_region(region):
            special_case_regions = {
                "Beyond Door of Time",
                "Kak Impas House Near Cow",
            }

            for entrance in region.entrances:
                if entrance.name in hint_entrances:
                    return entrance
            if region.dungeon is not None:
                for r in region.dungeon.regions:
                    for e in r.entrances:
                        if e.name in hint_entrances:
                            return e
            if region.is_boss_room or region.name in special_case_regions:
                return get_entrance_to_region(region.entrances[0].parent_region)
            return None

        if (self.shuffle_interior_entrances != 'off' or self.shuffle_dungeon_entrances
            or self.shuffle_grotto_entrances or self.shuffle_bosses != 'off'):
            for region in self.regions:
                if not any(bool(loc.address) for loc in region.locations): # check if region has any non-event locations
                    continue
                main_entrance = get_entrance_to_region(region)
                if main_entrance is not None and (main_entrance.shuffled or (region.is_boss_room and self.shuffle_bosses != 'off')):
                    for location in region.locations:
                        if type(location.address) == int:
                            er_hint_data[self.player][location.address] = main_entrance.name
                            logger.debug(f"Set {location.name} hint data to {main_entrance.name}")


    def write_spoiler(self, spoiler_handle: typing.TextIO) -> None:
        required_trials_str = ", ".join(t for t in self.skipped_trials if not self.skipped_trials[t])
        if required_trials_str == "":
            required_trials_str = "None"
        spoiler_handle.write(f"\n\nTrials ({self.multiworld.get_player_name(self.player)}): {required_trials_str}\n")

        if self.shopsanity != 'off':
            spoiler_handle.write(f"\nShop Prices ({self.multiworld.get_player_name(self.player)}):\n")
            for k, v in self.shop_prices.items():
                spoiler_handle.write(f"{k}: {v} Rupees\n")


    # Key ring handling:
    # Key rings are multiple items glued together into one, so we need to give
    # the appropriate number of keys in the collection state when they are
    # picked up.
    def keyring_gives_boss_key(self, dungeon_name: str) -> bool:
        return (
            dungeon_name in {'Forest Temple', 'Fire Temple', 'Water Temple', 'Shadow Temple', 'Spirit Temple'}
            and self.keyring_give_bk
            and dungeon_name in self.key_rings
            and self.shuffle_smallkeys != 'vanilla'
        )

    def _keyring_boss_key(self, item: OOTItem) -> str | None:
        if not item.name.startswith('Small Key Ring (') or not item.name.endswith(')'):
            return None
        dungeon_name = item.name[:-1].split(' (', 1)[1]
        if not self.keyring_gives_boss_key(dungeon_name):
            return None
        return f'Boss Key ({dungeon_name})'

    def collect(self, state: CollectionState, item: OOTItem) -> bool:
        state._oot_stale[self.player] = True
        if item.advancement and item.special and item.special.get('alias', False):
            alt_item_name, count = item.special.get('alias')
            state.prog_items[self.player][alt_item_name] += count
            if boss_key := self._keyring_boss_key(item):
                state.prog_items[self.player][boss_key] += 1
            return True
        return super().collect(state, item)

    def remove(self, state: CollectionState, item: OOTItem) -> bool:
        if item.advancement and item.special and item.special.get('alias', False):
            alt_item_name, count = item.special.get('alias')
            state.prog_items[self.player][alt_item_name] -= count
            if state.prog_items[self.player][alt_item_name] < 1:
                del (state.prog_items[self.player][alt_item_name])
            if boss_key := self._keyring_boss_key(item):
                state.prog_items[self.player][boss_key] -= 1
                if state.prog_items[self.player][boss_key] < 1:
                    del (state.prog_items[self.player][boss_key])
            # invalidate caches, nothing can be trusted anymore now
            state.child_reachable_regions[self.player] = set()
            state.child_blocked_connections[self.player] = set()
            state.adult_reachable_regions[self.player] = set()
            state.adult_blocked_connections[self.player] = set()
            state._oot_stale[self.player] = True
            return True
        changed = super().remove(state, item)
        if changed:
            # invalidate caches, nothing can be trusted anymore now
            state.child_reachable_regions[self.player] = set()
            state.child_blocked_connections[self.player] = set()
            state.adult_reachable_regions[self.player] = set()
            state.adult_blocked_connections[self.player] = set()
            state._oot_stale[self.player] = True
        return changed


    # Helper functions
    def region_has_shortcuts(self, regionname):
        region = self.get_region(regionname)
        try:
            dungeon_name = HintArea.at(region).dungeon_name
            return dungeon_name in self.dungeon_shortcuts
        except HintAreaNotFound:
            return False

    def get_shufflable_entrances(self, type=None, only_primary=False):
        return [entrance for entrance in self.get_entrances() if ((type == None or entrance.type == type)
            and (not only_primary or entrance.primary))]

    def get_shuffled_entrances(self, type=None, only_primary=False):
        return [entrance for entrance in self.get_shufflable_entrances(type=type, only_primary=only_primary) if
                entrance.shuffled]

    def get_locations(self):
        return self.multiworld.get_locations(self.player)

    def get_entrances(self):
        return self.multiworld.get_entrances(self.player)

    def is_major_item(self, item: OOTItem):
        if item.type == 'Token':
            return self.bridge == 'tokens' or self.lacs_condition == 'tokens'

        if item.name in self.nonadvancement_items:
            return True

        if item.type == 'DungeonReward' and self.shuffle_dungeon_rewards in ('vanilla', 'reward', 'dungeon'):
            return False

        if item.type in ('Drop', 'Event', 'Shop') or not item.advancement:
            return False

        if item.name.startswith('Bombchus') and not self.free_bombchu_drops:
            return False

        if item.type in ['Map', 'Compass']:
            return False
        if item.type == 'SmallKey' and self.shuffle_smallkeys in ['dungeon', 'vanilla']:
            return False
        if item.type == 'HideoutSmallKey' and self.shuffle_hideoutkeys == 'vanilla':
            return False
        if item.type == 'BossKey' and self.shuffle_bosskeys in ['dungeon', 'vanilla']:
            return False
        if item.type == 'GanonBossKey' and self.shuffle_ganon_bosskey in ['dungeon', 'vanilla']:
            return False
        if item.type == 'SilverRupee' and self.shuffle_silver_rupees in ['dungeon', 'vanilla']:
            return False

        return True

    # Specifically ensures that only real items are gotten, not any events.
    # Entrance validation still needs the complete age-travel assumption.
    def get_state_with_complete_itempool(self):
        all_state = CollectionState(self.multiworld)
        for item in self.itempool + self.pre_fill_items:
            self.multiworld.worlds[item.player].collect(all_state, item)
        for loc in self.get_locations():
            if loc.item is not None and loc.item.player == self.player and loc.item.type == 'DungeonReward':
                self.collect(all_state, loc.item)
        # If scarecrow behavior is free, give Scarecrow Song.
        if self.scarecrow_behavior == 'free':
            all_state.collect(self.create_item("Scarecrow Song"), prevent_sweep=True)
        if not self.shuffle_ocarinas:
            all_state.collect(self.create_item("Ocarina"), prevent_sweep=True)
        if 'Weird Egg' not in self.shuffle_child_trade and 'Chicken' not in self.shuffle_child_trade:
            all_state.collect(self.create_item("Weird Egg"), prevent_sweep=True)
        if 'Zeldas Letter' not in self.shuffle_child_trade:
            all_state.collect(self.create_item("Zeldas Letter"), prevent_sweep=True)
        if self.open_door_of_time not in ('open', 'stones'):
            all_state.collect(self.create_item("Song of Time"), prevent_sweep=True)
        all_state.collect(self.create_item("Time Travel"), prevent_sweep=True)
        all_state._oot_stale[self.player] = True

        return all_state

    def get_filler_item_name(self) -> str:
        return get_junk_item(self.random, count=1, pool=get_junk_pool(self))[0]


def valid_dungeon_item_location(world: OOTWorld, option: str, dungeon: str, loc: OOTLocation) -> bool:
    # loc.parent_region.dungeon is a Dungeon object (after Dungeon.__init__ runs), so compare .name
    loc_dungeon = loc.parent_region.dungeon
    loc_dungeon_name = loc_dungeon.name if loc_dungeon else None
    if (loc.type == 'Boss'
            and world.shuffle_dungeon_rewards in ('dungeon', 'regional', 'any_dungeon', 'overworld')):
        return False
    if option == 'dungeon':
        return (loc_dungeon_name == dungeon
            and (world.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations))
    elif option == 'any_dungeon':
        return (loc_dungeon is not None
            and (world.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations))
    elif option == 'overworld':
        return (loc_dungeon is None
            and (loc.type != 'Shop' or loc.name in world.shop_prices)
            and (world.shuffle_song_items != 'song' or loc.type != 'Song')
            and (world.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations))
    elif option == 'regional':
        color = HintArea.for_dungeon(dungeon).color
        return (HintArea.at(loc).color == color
            and (loc.type != 'Shop' or loc.name in world.shop_prices)
            and (world.shuffle_song_items != 'song' or loc.type != 'Song')
            and (world.shuffle_song_items != 'dungeon' or loc.name not in dungeon_song_locations))
    return False
    # raise ValueError(f'Unexpected argument to valid_dungeon_item_location: {option}')


def valid_reward_location(world: OOTWorld, mode: str, reward_name: str, loc: OOTLocation) -> bool:
    if loc.type == 'Boss' and not (reward_name == 'Light Medallion' and mode in ('dungeon', 'regional')):
        return False
    if loc.type == 'Shop' and loc.name not in world.shop_prices:
        return False
    if world.shuffle_song_items == 'song' and loc.type == 'Song':
        return False
    if world.shuffle_song_items == 'dungeon' and loc.name in dungeon_song_locations:
        return False
    loc_dungeon = loc.parent_region.dungeon
    loc_is_dungeon = loc_dungeon is not None or loc.parent_region.is_boss_room
    if mode == 'dungeon':
        # Stones / non-Light medallions go in their source dungeon.
        # Light Medallion lives in the Temple of Time hint area.
        source_dungeon = REWARD_TO_DUNGEON.get(reward_name)
        if source_dungeon is None:
            return HintArea.at(loc) == HintArea.TEMPLE_OF_TIME
        return loc_dungeon is not None and loc_dungeon.name == source_dungeon
    if mode == 'regional':
        return HintArea.at(loc).color == REWARD_COLORS[reward_name]
    if mode == 'any_dungeon':
        return loc_is_dungeon
    if mode == 'overworld':
        return not loc_is_dungeon
    return False


def gather_locations(multiworld: MultiWorld,
    item_type: str,
    players: Union[int, AbstractSet[int]],
    dungeon: str = ''
) -> Optional[List[OOTLocation]]:
    type_to_setting = {
        'Map': 'shuffle_map',
        'Compass': 'shuffle_compass',
        'SmallKey': 'shuffle_smallkeys',
        'BossKey': 'shuffle_bosskeys',
        'HideoutSmallKey': 'shuffle_hideoutkeys',
        'GanonBossKey': 'shuffle_ganon_bosskey',
        'SilverRupee': 'shuffle_silver_rupees',
    }

    # Special handling for atypical item types
    if item_type == 'HideoutSmallKey':
        dungeon = 'Thieves Hideout'
    elif item_type == 'GanonBossKey':
        dungeon = 'Ganons Castle'

    if isinstance(players, int):
        players = {players}
    fill_opts = {p: getattr(multiworld.worlds[p], type_to_setting[item_type]) for p in players}
    locations = []
    if any(map(lambda v: v == 'keysanity', fill_opts.values())):
        return None
    for player, option in fill_opts.items():
        condition = functools.partial(valid_dungeon_item_location,
            multiworld.worlds[player], option, dungeon)
        locations += filter(condition, multiworld.get_unfilled_locations(player=player))

    return locations

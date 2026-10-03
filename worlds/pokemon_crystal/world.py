import logging
import random
from collections import defaultdict
from dataclasses import replace
from threading import Event
from typing import ClassVar, Any

import settings
from BaseClasses import Tutorial, ItemClassification, MultiWorld, CollectionState, Item, Region
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, AutoLogicRegister, World
from .battle_tower_data import BATTLE_TOWER_NUM_TRAINERS, BATTLE_TOWER_NUM_TIERS
from .breeding import randomize_breeding, can_breed, breeding_is_randomized
from .data import PokemonData, TrainerData, MiscData, TMHMData, data as crystal_data, StaticPokemon, \
    MusicData, MoveData, FlyRegion, TradeData, MiscOption, StartingTown, EncounterType, EncounterKey, EncounterMon, \
    EvolutionType, TypeData, BugContestEncounter, FlypointWarp, friendly_entrance_name, \
    FRIENDLY_CONNECTION_NAME_OVERRIDES, internal_entrance_name, OUTDOOR_ENVIRONMENTS
from .evolution import randomize_evolution, evolution_in_logic
from .fly import get_free_fly_locations, randomize_fly_destinations, fly_flag_index
from .item_data import POKEDEX_OFFSET
from .items import PokemonCrystalItem, create_item_label_to_code_map, ITEM_GROUPS, \
    item_const_name_to_id, item_const_name_to_label, get_classification_override, get_random_filler_item, \
    get_random_ball, place_x_items, PokemonCrystalGlitchedToken, randomize_item_values, EVOLUTION_ITEMS
from .level_scaling import perform_level_scaling
from .locations import create_locations, PokemonCrystalLocation, create_location_label_to_id_map, LOCATION_GROUPS
from .misc import randomize_mischief, get_misc_spoiler_log
from .moves import randomize_tms, randomize_move_values, randomize_move_types, cap_hm_move_power, randomize_type_chart, \
    LOGIC_MOVES, modernise_moves
from .music import randomize_music
from .options import PokemonCrystalOptions, JohtoOnly, RandomizeBadges, HMBadgeRequirements, FreeFlyLocation, \
    VictoryRoadRequirement, EliteFourRequirement, MtSilverRequirement, RedRequirement, \
    Route44AccessRequirement, RadioTowerRequirement, RequireItemfinder, \
    OPTION_GROUPS, RandomizeFlyUnlocks, Shopsanity, Grasssanity, Goal, RandomizePokedex, BreedingMethodsRequired, \
    RemoveBadgeRequirement, SaffronGatehouseTea, ExpShareType, BattleTowerSanity, PokemonSourceLogic
from .phone import generate_phone_traps
from .phone_data import PhoneScript
from .pokemon import randomize_pokemon_data, randomize_starters, fill_wild_encounter_locations, fill_trade_locations, \
    randomize_unown_signs, randomize_trade_received_pokemon, randomize_trade_requested_pokemon, \
    randomize_request_pokemon, build_pokemon_pool_index, place_starters_in_early_wilds, \
    ensure_fly_learner_in_sphere_1
from .pokemon_pool import PokemonPool
from .pokemon_data import VANILLA_STARTERS
from .entrance_rando import EntranceRandoMixin, base_category
from .regions import create_regions, setup_free_fly_regions
from .rom import generate_output, PokemonCrystalProcedurePatch
from .rules import set_rules, PokemonCrystalLogic, verify_hm_accessibility
from .sign_data import FRIENDLY_SIGN_NAMES
from .trainers import set_rival_starter_pokemon, randomize_trainers, scale_red_levels
from .universal_tracker import load_ut_slot_data
from .utils import randomize_starting_town, adjust_options, randomize_rival, pretty_region_name, \
    validate_start_inventory, dexsanity_wild_in_logic, dexsanity_contest_in_logic, dexsanity_statics_in_logic, \
    dexsanity_breeding_in_logic, dexsanity_trades_in_logic
from .wild import randomize_wild_pokemon, randomize_static_pokemon, filter_time_of_day


class PokemonCrystalSettings(settings.Group):
    class RomFile(settings.UserFilePath):
        description = "Pokemon Crystal (UE) (V1.0 or V1.1) ROM File"
        copy_to = "Pokemon - Crystal Version (UE) [C][!].gbc"
        md5s = PokemonCrystalProcedurePatch.hash

    class OptionOverrides(dict):
        """
        Provided options will be used as overrides when patching.
        Pass the options as you would in an options yaml. (Option weights and triggers are not supported)
        Always available option overrides: trainer_name, game_options, field_move_menu_order, default_pokedex_mode
        Option overrides available when race mode is off: shopsanity_restrict_rare_candies, encounter_slot_distribution, reusable_tms, minimum_catch_rate, skip_elite_four, better_marts, build_a_mart, experience_modifier, starting_money, all_pokemon_seen

        example:
        option_overrides:
          experience_modifier: triple
          trainer_name: CHRIS
          game_options:
            turbo_button: a
            low_hp_beep: off
        """

    rom_file: RomFile = RomFile(RomFile.copy_to)
    option_overrides = {}

    class MaximumFillerTrapPercentage(int):
        """
        The maximum allowed filler_trap_percentage
        """

    maximum_filler_trap_percentage = MaximumFillerTrapPercentage(20)


class PokemonCrystalCollectionState(metaclass=AutoLogicRegister):
    """Per-player counters maintained by the PokemonCrystalWorld collect/remove hooks."""

    def init_mixin(self, parent: MultiWorld) -> None:
        game = crystal_data.manifest.game
        pc_ids = parent.get_game_players(game) + parent.get_game_groups(game)
        self.pc_unique_species = {player: 0 for player in pc_ids}
        self.pc_dex_species_count = {player: 0 for player in pc_ids}
        self.pc_dex_species_seen: dict[int, set[str]] = {player: set() for player in pc_ids}

    def copy_mixin(self, ret: CollectionState) -> CollectionState:
        ret.pc_unique_species = dict(self.pc_unique_species)
        ret.pc_dex_species_count = dict(self.pc_dex_species_count)
        ret.pc_dex_species_seen = {player: seen.copy() for player, seen in self.pc_dex_species_seen.items()}
        return ret


class PokemonCrystalWebWorld(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to playing Pokemon Crystal with MultiworldGG.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AliceMousie", "gerbiljames"]
    ), Tutorial(
        "Multiworld Setup Guide",
        "Eine Anleitung zum Spielen von Pokémon Kristall mit MultiworldGG.",
        "Deutsch",
        "setup_de.md",
        "setup/de",
        ["palex00"]
    ), Tutorial(
        "Multiworld Setup Guide",
        "Poradnik do grania w Pokémon Crystal z MultiworldGG.",
        "Polski",
        "setup_pl.md",
        "setup/pl",
        ["palex00"]
    )]

    option_groups = OPTION_GROUPS


class PokemonCrystalWorld(EntranceRandoMixin, World):
    """Pokémon Crystal is the culmination of the Generation I and II Pokémon games.
    Explore the Johto and Kanto regions, become the Pokémon League Champion, and
    defeat the elusive Red at the peak of Mt. Silver!"""
    game = crystal_data.manifest.game
    apworld_version = crystal_data.manifest.pokemon_crystal_version

    topology_present = True
    web = PokemonCrystalWebWorld()

    ut_can_gen_without_yaml = True
    glitches_item_name = PokemonCrystalGlitchedToken.TOKEN_NAME
    is_universal_tracker: bool

    found_entrances_datastorage_key = "pokemon_crystal_warps_{team}_{player}"

    settings_key = "pokemon_crystal_settings"
    settings: ClassVar[PokemonCrystalSettings]

    options_dataclass = PokemonCrystalOptions
    options: PokemonCrystalOptions

    required_client_version = (0, 6, 3)

    item_name_to_id = create_item_label_to_code_map()
    location_name_to_id = create_location_label_to_id_map()
    item_name_groups = ITEM_GROUPS  # item_groups
    location_name_groups = LOCATION_GROUPS  # location groups

    auth: bytes
    er_pairings: list[tuple[str, str]]

    dex_sources: frozenset[str] = frozenset()
    request_sources: frozenset[str] = frozenset()
    _dex_keys_cache: dict[str, tuple[str, ...]] = None  # type: ignore[assignment]
    _request_keys_cache: dict[str, tuple[str, ...]] = None  # type: ignore[assignment]

    free_fly_location: FlyRegion
    map_card_fly_location: FlyRegion

    starting_town: StartingTown
    fly_destinations: list[FlypointWarp] | None

    generated_moves: dict[str, MoveData]
    generated_types: dict[str, TypeData]
    generated_pokemon: dict[str, PokemonData]

    generated_trainers: dict[str, TrainerData]

    generated_tms: dict[str, TMHMData]
    generated_wild: dict[EncounterKey, list[EncounterMon]]
    generated_static: dict[EncounterKey, StaticPokemon]
    unique_static_wild_block: set[str]
    generated_trades: dict[str, TradeData]
    generated_lucky_number_trades: list[str]
    generated_contest: list[BugContestEncounter]

    generated_dexsanity: set[str]
    generated_dexcountsanity: list[int]
    generated_wooper: str
    generated_starters: tuple[list[str], list[str], list[str]]
    generated_starter_helditems: tuple[str, str, str]
    generated_palettes: dict[str, list[int]]
    generated_request_pokemon: list[str]
    generated_unown_signs: dict[str, str]
    generated_item_values: dict[int, int]

    generated_music: MusicData
    generated_misc: MiscData

    generated_phone_traps: list[PhoneScript]
    generated_phone_indices: list[int]

    trainer_name_list: list[str]
    trainer_level_list: list[int]
    trainer_name_level_dict: dict[str, int]
    static_name_list: list[str]
    static_level_list: list[int]
    encounter_region_name_list: list[str]
    encounter_region_levels_list: list[int]

    shop_locations_by_spheres: list[list[PokemonCrystalLocation]]

    itempool: list[PokemonCrystalItem]
    pre_fill_items: list[PokemonCrystalItem]
    logic: PokemonCrystalLogic
    pokemon_pool: PokemonPool

    filler_pool: list[list[str]]
    grass_location_mapping: dict[str, int]
    precollected_tod: str | None

    generated_rival: int

    finished_level_scaling: Event

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.generated_moves = dict(crystal_data.moves)
        self.generated_types = dict(crystal_data.types)
        self.generated_pokemon = dict(crystal_data.pokemon)
        self.generated_trainers = dict(crystal_data.trainers)
        self.generated_tms = dict(crystal_data.tmhm)
        self.generated_wild = {key: list(encounters) for key, encounters in crystal_data.wild.items()}
        self.generated_static = dict(crystal_data.static)
        self.unique_static_wild_block = set()
        self.generated_trades = dict(crystal_data.trades)
        self.generated_lucky_number_trades = []
        self.generated_contest = list(crystal_data.bug_contest_encounters)
        self.generated_dexsanity = set()
        self.generated_dexcountsanity = []
        self.generated_wooper = "WOOPER"
        self.generated_starters = tuple(list(line) for line in VANILLA_STARTERS)
        self.generated_starter_helditems = ("BERRY", "BERRY", "BERRY")
        self.generated_palettes = {}
        self.generated_request_pokemon = list(crystal_data.request_pokemon)
        self.generated_music = replace(crystal_data.music)
        self.generated_misc = replace(crystal_data.misc)
        self.generated_phone_traps = []
        self.generated_phone_indices = []
        self.generated_unown_signs = {}
        self.generated_rival = 0

        self.trainer_name_list = []
        self.trainer_level_list = []
        self.trainer_name_level_dict = {}
        self.static_name_list = []
        self.static_level_list = []
        self.encounter_region_name_list = []
        self.encounter_region_levels_list = []
        self.generated_item_values = {item.item_id: item.price for item in crystal_data.items.values()}

        self.shop_locations_by_spheres = []

        self.itempool = []
        self.pre_fill_items = []
        self.filler_pool = []
        self.grass_location_mapping = {}
        self.er_pairings = []
        self.er_entrances: list[tuple] = []
        self.fly_destinations = None
        self.precollected_tod = None

        self.finished_level_scaling = Event()

        self.is_universal_tracker = getattr(self.multiworld, "generation_is_fake", False)

    def generate_early(self) -> None:
        if not self.is_universal_tracker:
            adjust_options(self)
        filter_time_of_day(self)
        load_ut_slot_data(self)
        randomize_mischief(self)
        randomize_rival(self)
        self.logic = PokemonCrystalLogic(self)
        self.pokemon_pool = PokemonPool(self)

        if self.options.unlockable_time_of_day and self.options.time_of_day_encounters and not self.is_universal_tracker:
            tod_items = ["MORN_ITEM", "DAY_ITEM", "NITE_ITEM"]
            start_item = self.random.choice(tod_items)
            item = self.create_item_by_const_name(start_item)
            self.precollected_tod = item.name
            self.push_precollected(item)

        if not self.is_universal_tracker:
            if self.options.early_fly:
                self.multiworld.local_early_items[self.player]["HM02 Fly"] = 1
                if (self.options.hm_badge_requirements.value != HMBadgeRequirements.option_no_badges
                        and RemoveBadgeRequirement.FLY not in self.options.remove_badge_requirement.value
                        and self.options.randomize_badges == RandomizeBadges.option_completely_random):
                    self.multiworld.local_early_items[self.player]["Storm Badge"] = 1

            randomize_move_types(self)
            randomize_tms(self)
            randomize_pokemon_data(self)
            randomize_unown_signs(self)
            randomize_item_values(self)
            validate_start_inventory(self)

        self.logic.set_hm_compatible_pokemon(self)

    @classmethod
    def stage_generate_early(cls, multiworld: "MultiWorld") -> None:
        perm = list(range(BATTLE_TOWER_NUM_TRAINERS))
        rng = random.Random(multiworld.seed)
        rng.shuffle(perm)
        mon_seed = rng.getrandbits(64)
        wild_seed = rng.getrandbits(64)
        for world in multiworld.get_game_worlds(cls.game):
            if not hasattr(world, "battle_tower_trainer_permutation"):
                world.battle_tower_trainer_permutation = perm
            world.battle_tower_mon_seed = mon_seed
            world.shared_wild_seed = wild_seed

    def create_regions(self) -> None:

        randomize_starting_town(self)
        randomize_fly_destinations(self)
        regions = create_regions(self)

        preevolutions = randomize_evolution(self)

        max_evo_level = self.options.maximum_evolution_level.value
        if max_evo_level < 100:
            for pkmn_name, pkmn_data in self.generated_pokemon.items():
                new_evolutions = [
                    replace(evo, level=min(evo.level, max_evo_level))
                    if evo.evo_type in (EvolutionType.Level, EvolutionType.Stats) and evo.level > max_evo_level
                    else evo
                    for evo in pkmn_data.evolutions
                ]
                if new_evolutions != list(pkmn_data.evolutions):
                    self.generated_pokemon[pkmn_name] = replace(pkmn_data, evolutions=new_evolutions)

        randomize_breeding(self, preevolutions)

        build_pokemon_pool_index(self)

        randomize_starters(self)
        randomize_static_pokemon(self)
        randomize_wild_pokemon(self)

        randomize_trade_received_pokemon(self)

        self.pokemon_pool.ensure_base_pools()

        if self.options.randomize_lucky_number_show and not self.is_universal_tracker:
            from .utils import should_include_region
            reachable_trades = [t for rn, rd in crystal_data.regions.items()
                                if should_include_region(rd, self) for t in rd.trades]
            self.generated_lucky_number_trades = self.random.sample(reachable_trades, 3)

        create_locations(self, regions)
        self.multiworld.regions.extend(regions.values())

        if self.options.free_fly_location:
            if not self.is_universal_tracker:
                get_free_fly_locations(self)
            setup_free_fly_regions(self)

    def create_items(self) -> None:

        item_locations = [
            location
            for location in self.multiworld.get_locations(self.player)
            if location.address is not None and location.address < POKEDEX_OFFSET
        ]

        if self.options.randomize_badges == RandomizeBadges.option_shuffle:
            self.pre_fill_items.extend(
                self.create_item_by_code(loc.default_item_code) for loc in item_locations if "Badge" in loc.tags)
            item_locations = [location for location in item_locations if "Badge" not in location.tags]

        if (self.options.randomize_fly_unlocks == RandomizeFlyUnlocks.option_exclude_silver_cave
            and self.options.johto_only.value != JohtoOnly.option_on):
            item_locations = [location for location in item_locations if location.name != "Visit Silver Cave"]

        if self.options.remote_items and not self.options.randomize_pokegear:
            item_locations = [location for location in item_locations if "Pokegear" not in location.tags]

        if self.options.remote_items and not self.options.randomize_berry_trees:
            item_locations = [location for location in item_locations if "BerryTree" not in location.tags]

        badge_option_counts = [8]
        if self.options.radio_tower_requirement == RadioTowerRequirement.option_badges:
            badge_option_counts.append(self.options.radio_tower_count.value)
        if self.options.victory_road_requirement == VictoryRoadRequirement.option_badges:
            badge_option_counts.append(self.options.victory_road_count.value)
        if self.options.elite_four_requirement == EliteFourRequirement.option_badges:
            badge_option_counts.append(self.options.elite_four_count.value)
        if self.options.route_44_access_requirement == Route44AccessRequirement.option_badges:
            badge_option_counts.append(self.options.route_44_access_count.value)

        if self.options.johto_only == JohtoOnly.option_include_silver_cave:
            if self.options.mt_silver_requirement == MtSilverRequirement.option_badges:
                badge_option_counts.append(self.options.mt_silver_count.value)
            if self.options.red_requirement == RedRequirement.option_badges:
                badge_option_counts.append(self.options.red_count.value)

        required_badges = max(badge_option_counts)

        add_items = []
        # Extra badges to add to the pool in johto only
        if self.options.johto_only and required_badges > 8:
            kanto_badges = [item_data.item_const for item_data in crystal_data.items.values() if
                            "KantoBadge" in item_data.tags]
            self.random.shuffle(kanto_badges)
            add_items.extend(kanto_badges[:required_badges - 8])

        if self.options.johto_only:
            if self.options.progressive_rods:
                add_items.append("PROGRESSIVE_ROD")
            else:
                add_items.append("SUPER_ROD")

        if Shopsanity.BLUE_CARD in self.options.shopsanity.value:
            add_items.extend(["BLUE_CARD_PT"] * 5)

        if Goal.UNOWN_HUNT in self.options.goal:
            add_items.extend(["KABUTO_TILE"] * 16)
            add_items.extend(["OMANYTE_TILE"] * 16)
            add_items.extend(["AERO_TILE"] * 16)
            add_items.extend(["HO_OH_TILE"] * 16)

        if self.options.add_missing_useful_items:
            add_items.extend(["TM_9", "TWISTEDSPOON", "THICK_CLUB", "BRIGHTPOWDER", "STICK", "LUCKY_PUNCH",
                              "LIGHT_BALL", "METAL_POWDER"])

            if Shopsanity.GAME_CORNERS not in self.options.shopsanity.value:
                add_items.extend(["TM_14", "TM_15", "TM_25", "TM_32", "TM_38"])

            if self.options.johto_only != JohtoOnly.option_off:
                add_items.extend(["TM_3", "TM_6", "TM_7", "TM_17", "TM_19", "TM_29", "TM_42", "TM_47"])

        if MiscOption.NewItem in self.generated_misc.selected:
            add_items.extend(["OAKS_PARCEL"])

        if self.options.battle_tower_sanity or Goal.BATTLE_TOWER in self.options.goal:
            add_items.append("BATTLE_TOWER_UBER_PASS")
        if self.options.battle_tower_progressive_tier_unlocks and (
                self.options.battle_tower_sanity or Goal.BATTLE_TOWER in self.options.goal):
            add_items.extend(["BATTLE_TOWER_TIER_UNLOCK"] * 10)

        for location in item_locations:
            item_code = location.default_item_code
            if item_code > 0:
                self.itempool.append(self.create_item_by_code(item_code))
            else:  # item is NO_ITEM, trainersanity checks
                self.itempool.append(self.create_item_by_const_name(get_random_filler_item(self)))

        # Guarantee at least one of each evolution item in every seed
        pool_item_names = {item.name for item in self.itempool}
        add_items.extend(item_const for item_const in EVOLUTION_ITEMS
                         if item_const_name_to_label(item_const) not in pool_item_names)

        if self.options.dexsanity:
            self.itempool.extend(
                self.create_item_by_const_name(get_random_ball(self.random))
                for _ in self.generated_dexsanity)

        if self.generated_dexcountsanity:
            self.itempool.extend(
                self.create_item_by_const_name(get_random_ball(self.random))
                for _ in self.generated_dexcountsanity)

        if self.options.grasssanity:
            self.itempool.extend(
                self.create_item_by_const_name("GRASS_ITEM")
                for _ in [loc for loc in self.multiworld.get_locations(self.player) if "grass" in loc.tags])

        if self.options.unlockable_time_of_day and self.options.time_of_day_encounters:
            precollected_names = {item.name for item in self.multiworld.precollected_items[self.player]}
            for const_name in ["MORN_ITEM", "DAY_ITEM", "NITE_ITEM"]:
                item = self.create_item_by_const_name(const_name)
                if item.name not in precollected_names:
                    add_items.append(const_name)

        if self.options.johto_only.value != JohtoOnly.option_off:
            # Replace the S.S. Ticket with the Silver Wing for Johto only seeds
            self.itempool = [item if item.name != "S.S. Ticket" else self.create_item_by_const_name("SILVER_WING")
                             for item in self.itempool]

        if self.options.exp_share_type == ExpShareType.option_exp_all:
            self.itempool = [
                item if item.name != "Exp Share" else self.create_item_by_const_name("EXP_ALL")
                for item in self.itempool]

        if self.options.progressive_rods:
            self.itempool = [
                item if item.name not in ("Old Rod", "Good Rod", "Super Rod") else self.create_item_by_const_name(
                    "PROGRESSIVE_ROD") for item in self.itempool]

        if self.options.randomize_pokedex == RandomizePokedex.option_start_with:
            self.itempool = [
                item if item.name != "Pokedex" else self.create_item_by_const_name(get_random_filler_item(self)) for
                item in self.itempool]

            self.push_precollected(self.create_item_by_const_name("POKEDEX"))

        x_items_to_remove = place_x_items(self)
        if x_items_to_remove:
            filtered_itempool = []
            for item in self.itempool:
                if item.name in x_items_to_remove:
                    x_items_to_remove.remove(item.name)
                    continue
                filtered_itempool.append(item)
            self.itempool = filtered_itempool

        trap_names = [
            trap.label for trap in crystal_data.items.values() if trap.classification & ItemClassification.trap
        ]

        trap_weights = [self.options.trap_weights.get(trap, 0) for trap in trap_names]

        total_trap_weight = self.options.filler_trap_percentage.value if any(trap_weights) else 0

        for i in range(len(self.itempool)):
            if self.itempool[i].classification == ItemClassification.filler:
                if add_items:
                    self.itempool[i] = self.create_item_by_const_name(add_items.pop())
                elif total_trap_weight and self.random.randint(0, 100) <= total_trap_weight:
                    self.itempool[i] = self.create_item(self.random.choices(trap_names, trap_weights)[0])

        self.multiworld.itempool.extend(self.itempool)

    def set_rules(self) -> None:
        set_rules(self)

    def generate_basic(self) -> None:
        if self.is_universal_tracker: return

        ensure_fly_learner_in_sphere_1(self)
        modernise_moves(self)
        randomize_move_values(self)
        cap_hm_move_power(self)
        randomize_music(self)
        randomize_type_chart(self)

        self.auth = self.random.randbytes(16)

        if (self.options.randomize_fly_unlocks == RandomizeFlyUnlocks.option_exclude_silver_cave
            and self.options.johto_only != JohtoOnly.option_on):
            silver_cave = self.get_location("Visit Silver Cave")
            silver_cave.place_locked_item(self.create_item_by_code(silver_cave.default_item_code))

        if self.options.remote_items and not self.options.randomize_pokegear:
            pokegear_locations = [loc for loc in self.get_locations() if "Pokegear" in loc.tags]
            for loc in pokegear_locations:
                loc.place_locked_item(self.create_item_by_code(loc.default_item_code))

        if self.options.remote_items and not self.options.randomize_berry_trees:
            berry_locations = [loc for loc in self.get_locations() if "BerryTree" in loc.tags]
            for loc in berry_locations:
                loc.place_locked_item(self.create_item_by_code(loc.default_item_code))

        if self.options.randomize_badges == RandomizeBadges.option_shuffle:
            badge_items = []
            badge_items.extend(self.pre_fill_items)
            self.pre_fill_items.clear()

            if self.options.early_fly and RemoveBadgeRequirement.FLY not in self.options.remove_badge_requirement.value:
                early_badge_locs = [loc for loc in
                                    self.multiworld.get_reachable_locations(self.multiworld.state, self.player) if
                                    "Badge" in loc.tags]
                # take one of the early badge locations, set it to storm badge
                if early_badge_locs:
                    storm_loc = self.random.choice(early_badge_locs)
                    storm_badge = next(item for item in badge_items if item.name == "Storm Badge")
                    storm_loc.place_locked_item(storm_badge)
                    badge_items.remove(storm_badge)

            # If we can't do this in 5 attempts then just accept our fate
            for attempt in range(5):
                if attempt >= 1:
                    self.logic.guaranteed_hm_access = True
                state = self.get_world_collection_state()

                attempt_locs = [loc for loc in self.multiworld.get_locations(self.player) if
                                "Badge" in loc.tags and not loc.item]
                attempt_items = badge_items.copy()
                self.random.shuffle(attempt_locs)
                self.random.shuffle(attempt_items)
                fill_restrictive(self.multiworld, state, attempt_locs.copy(), attempt_items,
                                 single_player_placement=True, lock=True, allow_excluded=True, allow_partial=True)
                if not attempt_items:
                    break

                if attempt >= 4:
                    raise FillError(
                        f"Failed to shuffle badges for player {self.player} ({self.player_name}). Aborting.")

                for location in attempt_locs:
                    location.locked = False
                    if location.item is not None:
                        location.item.location = None
                        location.item = None

                logging.debug(f"Failed to shuffle badges for player {self.player} ({self.player_name}). Retrying.")

            self.logic.guaranteed_hm_access = False
            verify_hm_accessibility(self)

    @classmethod
    def stage_generate_output(cls, multiworld: MultiWorld, output_directory: str):
        shopsanity_players: set[int] = {
            w.player for w in multiworld.get_game_worlds(cls.game) if w.options.shopsanity
        }
        if shopsanity_players:
            exclude_shops = frozenset((
                "REGION_MART_BLUE_CARD", "REGION_MART_GOLDENROD_GAME_CORNER",
                "REGION_MART_CELADON_GAME_CORNER_PRIZE_ROOM", "REGION_MART_KURTS_BALLS",
            ))
            relevant_shop_locations: set[PokemonCrystalLocation] = {
                loc for player in shopsanity_players
                for loc in multiworld.get_locations(player)
                if "shopsanity" in loc.tags and loc.parent_region.name not in exclude_shops
            }

            shop_locations: dict[int, list[list[PokemonCrystalLocation]]] = defaultdict(list)
            for sphere in multiworld.get_spheres():
                sphere_relevant = sphere & relevant_shop_locations
                if not sphere_relevant:
                    continue
                shop_locations_in_sphere: dict[int, set[PokemonCrystalLocation]] = defaultdict(set)
                for location in sphere_relevant:
                    shop_locations_in_sphere[location.player].add(location)
                for player, locations in sorted(shop_locations_in_sphere.items()):
                    shop_locations[player].append(sorted(locations, key=lambda loc: loc.name))

            for world in multiworld.get_game_worlds(cls.game):
                if world.options.shopsanity:
                    world.shop_locations_by_spheres = shop_locations[world.player]

        perform_level_scaling(multiworld)


    def connect_entrances(self) -> None:
        if not self.is_universal_tracker:
            disconnected = []
            for entrance, _dest in self.er_entrances:
                if entrance.connected_region is not None:
                    target = entrance.connected_region
                    target.entrances.remove(entrance)
                    entrance.connected_region = None
                    disconnected.append((entrance, target))
            try:
                place_starters_in_early_wilds(self, allow_partial_entrances=True)
            finally:
                for entrance, target in disconnected:
                    entrance.connect(target)
            self.pokemon_pool.invalidate()
            randomize_trade_requested_pokemon(self)
            randomize_request_pokemon(self)
            self.refresh_source_sets()
        fill_wild_encounter_locations(self)
        fill_trade_locations(self)
        if not self.is_universal_tracker:
            verify_hm_accessibility(self)

        with self._plando_items_placed_for_er():
            self._shuffle_entrances()
        if self.is_universal_tracker:
            self._apply_friendly_entrance_names()

    def post_fill(self) -> None:
        self._apply_friendly_entrance_names()

    def _encounter_name_options(self) -> dict[str, bool]:
        return {"kanto": self.options.johto_only == JohtoOnly.option_off,
                "route_23": bool(self.options.route_23_restored)}

    def _friendly_name_overrides(self) -> dict[str, str]:
        """Names from FRIENDLY_CONNECTION_NAME_OVERRIDES for each option's current value.
        A value with no column (e.g. route_42_access "blocked") contributes nothing."""
        overrides: dict[str, str] = {}
        for option_name, columns in FRIENDLY_CONNECTION_NAME_OVERRIDES.items():
            value = getattr(self.options, option_name).current_key
            overrides.update(columns.get(value, {}))
        return overrides

    def _generated_entrance_names(self) -> dict[str, str]:
        """Display names for the synthesized fly, flypoint-unlock and start edges."""
        names = {f"REGION_FLY -> {fr.exit_region}": f"Fly to {fr.name}" for fr in crystal_data.fly_regions}
        for fr in crystal_data.fly_regions:
            if fr.unlock_region == fr.exit_region:
                continue
            for src in (fr.exit_region, *fr.unlock_sources):
                names[f"{src} -> {fr.unlock_region}"] = f"{fr.name} Flypoint ({pretty_region_name(src)})"
        names.update({f"Menu -> {town.region_id}": f"Start in {town.name}"
                      for town in crystal_data.starting_towns})
        return names

    def _apply_friendly_entrance_names(self) -> None:
        """Rename entrances to their display names once nothing looks them up by
        internal name anymore. The cache keeps the internal key as an alias so
        name-based lookups (e.g. UT's deferred reconnect from slot data) still resolve."""
        overrides = {**self._friendly_name_overrides(), **self._generated_entrance_names()}
        cache = self.multiworld.regions.entrance_cache[self.player]
        for entrance in list(self.multiworld.get_entrances(self.player)):
            name = entrance.name
            if name.startswith("Free Fly REGION_"):
                friendly = f"Free Fly to {pretty_region_name(name.removeprefix('Free Fly '))}"
            elif name.startswith("Fly Destination ") and entrance.connected_region is not None:
                friendly = (f"Fly Slot {name.removeprefix('Fly Destination ')} "
                            f"({pretty_region_name(entrance.connected_region.name)})")
            else:
                friendly = overrides.get(name) or friendly_entrance_name(name)
            if friendly != name:
                if friendly in cache:
                    raise RuntimeError(f"Duplicate entrance display name {friendly!r}")
                entrance.name = friendly
                cache[friendly] = entrance

    def generate_output(self, output_directory: str) -> None:
        generate_phone_traps(self)
        scale_red_levels(self)
        self.finished_level_scaling.wait()

        set_rival_starter_pokemon(self)
        randomize_trainers(self)

        patch = PokemonCrystalProcedurePatch(player=self.player, player_name=self.player_name)
        generate_output(self, output_directory, patch)

    def fill_slot_data(self) -> dict[str, Any]:
        slot_data = self.options.as_dict(
            "goal",
            "johto_only",
            "victory_road_requirement",
            "victory_road_count",
            "elite_four_requirement",
            "elite_four_count",
            "red_requirement",
            "red_count",
            "randomize_badges",
            "dexsanity",
            "randomize_pokegear",
            "hm_badge_requirements",
            "randomize_berry_trees",
            "remove_ilex_cut_tree",
            "radio_tower_requirement",
            "radio_tower_count",
            "route_44_access_requirement",
            "route_44_access_count",
            "route_32_condition",
            "mt_silver_requirement",
            "mt_silver_count",
            "east_west_underground",
            "undergrounds_require_power",
            "red_gyarados_access",
            "route_2_access",
            "blackthorn_dark_cave_access",
            "national_park_access",
            "route_22_access_requirement",
            "route_22_access_count",
            "route_3_access",
            "vanilla_event_chains",
            "static_pokemon_required",
            "breeding_methods_required",
            "evolution_gym_levels",
            "rematchsanity",
            "all_pokemon_seen",
            "dexcountsanity_leniency",
            "dexcountsanity_step",
            "provide_shop_hints",
            "randomize_fly_unlocks",
            "route_42_access",
            "mount_mortar_access",
            "randomize_pokemon_requests",
            "randomize_evolution",
            "randomize_breeding",
            "dark_areas",
            "require_flash",
            "victory_road_strength",
            "lock_kanto_gyms",
            "randomize_starting_town",
            "saffron_gatehouse_tea",
            "shopsanity",
            "wild_encounter_methods_required",
            "time_of_day_encounters",
            "unlockable_time_of_day",
            "evolution_methods_required",
            "remove_badge_requirement",
            "johto_trainersanity",
            "kanto_trainersanity",
            "randomize_hidden_items",
            "require_itemfinder",
            "skip_elite_four",
            "lance_requires_elite_four",
            "field_moves_always_usable",
            "grasssanity",
            "enforce_wild_encounter_methods_logic",
            "randomize_trades",
            "trades_required",
            "randomize_lucky_number_show",
            "trap_link",
            "randomize_bug_catching_contest",
            "randomize_phone_call_items",
            "phone_call_mode",
            "progressive_rods",
            "add_missing_useful_items",
            "ss_aqua_access",
            "magnet_train_access",
            "route_12_access",
            "route_30_battle",
            "require_pokegear_for_phone_numbers",
            "enforce_breeding_methods_logic",
            "randomize_pokedex",
            "momsanity",
            "route_30_access",
            "south_kanto_access",
            "south_kanto_condition",
            "remote_items",
            "maximum_evolution_level",
            "randomize_entrances",
            "mix_entrances",
            "coupled_entrances",
            "route_23_restored",
            "flooded_mine",
            "randomize_fly_destinations",
            "pokemon_request_logic",
            "dexsanity_logic",
            "battle_tower_sanity",
            "battle_tower_progressive_tier_unlocks",
        )

        slot_data["battle_tower_trainer_permutation"] = self.battle_tower_trainer_permutation
        slot_data["er_pairings"] = list(self.er_pairings)
        slot_data["apworld_version"] = self.apworld_version
        slot_data["tea_north"] = 1 if SaffronGatehouseTea.NORTH in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_east"] = 1 if SaffronGatehouseTea.EAST in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_south"] = 1 if SaffronGatehouseTea.SOUTH in self.options.saffron_gatehouse_tea.value else 0
        slot_data["tea_west"] = 1 if SaffronGatehouseTea.WEST in self.options.saffron_gatehouse_tea.value else 0
        slot_data["dexsanity_count"] = len(self.generated_dexsanity)
        slot_data["dexsanity_pokemon"] = [self.generated_pokemon[poke].id for poke in sorted(self.generated_dexsanity)]
        slot_data["logically_available_pokemon_count"] = len(
            self.pokemon_pool.get_filtered(self.options.dexsanity_logic))
        slot_data["diploma_count"] = len(self.pokemon_pool.all_available)

        # slot order matters: UT rebuilds generated_wild from this and per-slot rules index into it
        region_encounters = dict[str, list[int]]()
        for encounter_key, encounters in self.generated_wild.items():
            region_encounters[encounter_key.region_name()] = [self.generated_pokemon[enc.pokemon].id for enc in
                                                              encounters]

        for encounter_key, encounter in self.generated_static.items():
            region_encounters[encounter_key.region_name()] = [self.generated_pokemon[encounter.pokemon].id]

        slot_data["region_encounters"] = region_encounters

        slot_data["contest_encounters"] = [self.generated_pokemon[slot.pokemon].id for slot in self.generated_contest]

        slot_data["free_fly_location_option"] = self.options.free_fly_location.value
        slot_data["free_fly_location"] = 0
        slot_data["map_card_fly_location"] = 0

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card):
            slot_data["free_fly_location"] = self.free_fly_location.id

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card):
            slot_data["map_card_fly_location"] = self.map_card_fly_location.id

        slot_data["enable_mischief"] = 1 if (self.options.enable_mischief
                                             and MiscOption.Tracker.value in self.generated_misc.selected) else 0
        slot_data["enable_mischief_option"] = self.options.enable_mischief.value
        slot_data["teleporting_abra"] = 1 if MiscOption.TeleportingAbra.value in self.generated_misc.selected else 0

        slot_data["starting_town"] = 0
        if self.options.randomize_starting_town:
            slot_data["starting_town"] = self.starting_town.id

        slot_data["dexcountsanity"] = self.generated_dexcountsanity[-1] if self.generated_dexcountsanity else 0
        slot_data["dexcountsanity_option"] = self.options.dexcountsanity.value
        slot_data["dexcountsanity_checks"] = len(self.generated_dexcountsanity)
        slot_data["dexcountsanity_counts"] = self.generated_dexcountsanity

        if self.options.breeding_methods_required == BreedingMethodsRequired.option_any:
            breeding_method = 4
        elif self.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto:
            if self.options.enforce_breeding_methods_logic:
                breeding_method = 3
            else:
                breeding_method = 2
        else:
            if self.options.enforce_breeding_methods_logic:
                breeding_method = 1
            else:
                breeding_method = 0
        slot_data["breeding_method"] = breeding_method

        if not self.options.randomize_hidden_items:
            if not self.options.require_itemfinder:
                hidden_items_setting = 0
            elif self.options.require_itemfinder.value == RequireItemfinder.option_logically_required:
                hidden_items_setting = 1
            else:
                hidden_items_setting = 2
        else:
            if not self.options.require_itemfinder:
                hidden_items_setting = 3
            elif self.options.require_itemfinder.value == RequireItemfinder.option_logically_required:
                hidden_items_setting = 4
            else:
                hidden_items_setting = 5

        slot_data["hiddenitem_logic"] = hidden_items_setting
        slot_data["trainersanity"] = [loc.address for loc in self.get_locations() if "Trainersanity" in loc.tags]

        evolution_data = dict[int, list[dict]]()
        for pokemon_id, pokemon_data in self.generated_pokemon.items():
            evo_data = list()
            for evo in pokemon_data.evolutions:
                evo_data.append({
                    "into": self.generated_pokemon[evo.pokemon].id,
                    "method": str(evo.evo_type),
                    "level": evo.level,
                    "condition": evo.level if evo.evo_type is EvolutionType.Level else evo.condition
                })
            if evo_data: evolution_data[self.generated_pokemon[pokemon_id].id] = evo_data
        slot_data["evolution_info"] = evolution_data

        breeding_data = dict()
        for pokemon_id, pokemon_data in self.generated_pokemon.items():
            if not can_breed(self, pokemon_id): continue
            breeding_data[pokemon_data.id] = self.generated_pokemon[pokemon_data.produces_egg].id
        slot_data["breeding_info"] = breeding_data

        slot_data["request_pokemon"] = [self.generated_pokemon[poke].id for poke in self.generated_request_pokemon]

        hm_compat = dict[int, set[int]]()
        for pokemon_data in self.generated_pokemon.values():
            hm_compat[pokemon_data.id] = {
                index for index, move in enumerate(LOGIC_MOVES) if move in pokemon_data.tm_hm
            }
        slot_data["hm_compat"] = hm_compat

        slot_data["grass_location_mapping"] = self.grass_location_mapping

        slot_data["trades"] = {
            trade_id: {"requested": str(self.generated_pokemon[trade.requested_pokemon].id), "received": str(
                self.generated_pokemon[trade.received_pokemon].id)} for trade_id, trade in
            self.generated_trades.items()}

        slot_data["trap_weights"] = {
            trap.label: self.options.trap_weights.get(trap.label, 0) for trap in crystal_data.items.values() if
            trap.classification & ItemClassification.trap
        }

        if not self.options.remote_items and self.options.filler_trap_percentage:
            slot_data["trap_locations"] = {str(location.address): location.item.code for location in
                                           self.get_locations() if
                                           location.item.player == self.player and ("Trap" in location.item.tags)}

        slot_data["unown_signs"] = self.generated_unown_signs
        slot_data["lucky_number_trades"] = self.generated_lucky_number_trades
        slot_data["precollected_tod"] = self.precollected_tod

        if self.fly_destinations is not None:
            slot_data["fly_destinations"] = [[flypoint.map_name, flypoint.warp_index]
                                            for flypoint in self.fly_destinations]


        return slot_data

    def modify_multidata(self, multidata: dict[str, Any]):
        import base64
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] \
            = multidata["connect_names"][self.player_name]

    def write_spoiler(self, spoiler_handle) -> None:
        spoiler_handle.write(f"\nPokemon Crystal ({self.player_name}):\n")

        if Goal.DIPLOMA in self.options.goal:
            available_pokemon = len(self.pokemon_pool.all_available)
            spoiler_handle.write(f"Diploma requirement: {available_pokemon} species\n")

        if Goal.UNOWN_HUNT in self.options.goal:
            spoiler_handle.write("Unown locations:\n")
            for sign, unown in self.generated_unown_signs.items():
                sign_friendly_name = FRIENDLY_SIGN_NAMES[sign]
                spoiler_handle.write(f"{sign_friendly_name}: {unown.replace('_', ' ')}\n")
            spoiler_handle.write("\n")

        if self.options.randomize_starters:
            spoiler_handle.write("Starters: ")
            spoiler_handle.write(
                ", ".join([self.generated_pokemon[line[0]].friendly_name for line in self.generated_starters]))
            spoiler_handle.write("\n")

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                    FreeFlyLocation.option_free_fly_and_map_card):
            if not self.options.randomize_fly_destinations:
                spoiler_handle.write(f"Free Fly Location: {self.free_fly_location.name}\n")
            else:
                spoiler_handle.write(f"Free Fly Location: Fly Unlock {fly_flag_index(self, self.free_fly_location) + 1}\n")

        if self.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                    FreeFlyLocation.option_map_card):
            if not self.options.randomize_fly_destinations:
                spoiler_handle.write(f"Map Card Fly Location: {self.map_card_fly_location.name}\n")
            else:
                spoiler_handle.write(f"Map Card Fly Location: Fly Unlock {fly_flag_index(self, self.map_card_fly_location) + 1}\n")

        if self.options.randomize_starting_town:
            spoiler_handle.write(f"Starting Town: {self.starting_town.name}\n")

        if self.options.randomize_fly_destinations:
            spoiler_handle.write(f"Fly Destinations:\n")
            fly_destination_names = [next(friendly_entrance_name(name)
                                          for name, conn in crystal_data.entrance_connections.items()
                                          if conn.exit_warps[0].map_name == flypoint.map_name
                                          and flypoint.warp_index in (w.warp_index for w in conn.exit_warps))
                                     for flypoint in self.fly_destinations]
            for i, destination in enumerate(fly_destination_names, start=1):
                spoiler_handle.write(f"Fly Destination {i}: {destination}\n")

        if self.er_pairings:
            spoiler_handle.write(f"\nEntrances ({self.player_name}):\n")
            for source, target in sorted(self.er_pairings, key=lambda p: friendly_entrance_name(p[0])):
                spoiler_handle.write(f"{friendly_entrance_name(source)} => {friendly_entrance_name(target)}\n")

        name_options = self._encounter_name_options()
        encounters_per_pokemon = defaultdict(set)
        if self.options.randomize_wilds:
            for key, encounters in self.generated_wild.items():
                if key.encounter_type == EncounterType.Fish and key.region_id.startswith("Remoraid"):
                    # The Remoraid table is only for GS, not Crystal
                    continue
                for i, encounter in enumerate(encounters):
                    encounters_per_pokemon[encounter.pokemon].add(key.friendly_slot_region_name(i, **name_options))
            for slot in self.generated_contest:
                encounters_per_pokemon[slot.pokemon].add("Bug Catching Contest")
        if self.options.randomize_static_pokemon:
            for key, static in self.generated_static.items():
                if static.level_type != "ignore":
                    encounters_per_pokemon[static.pokemon].add(key.friendly_region_name(**name_options))
        else:
            key = EncounterKey.static("OddEgg")
            odd_egg = self.generated_static[key]
            encounters_per_pokemon[odd_egg.pokemon].add(key.friendly_region_name(**name_options))

        if encounters_per_pokemon:
            spoiler_handle.write(f"\nRandomized Pokemon ({self.player_name}):\n")
            lines = [f"{self.generated_pokemon[pokemon_id].friendly_name}: {', '.join(sorted(locations))}\n"
                     for pokemon_id, locations in encounters_per_pokemon.items()]
            lines.sort()
            for line in lines:
                spoiler_handle.write(line)

        if self.options.randomize_evolution:
            spoiler_handle.write(f"\nEvolutions ({self.player_name}):\n")

            for pokemon_id, pokemon_data in self.generated_pokemon.items():
                for evo in pokemon_data.evolutions:
                    pokemon_name = self.generated_pokemon[pokemon_id].friendly_name
                    evo_name = self.generated_pokemon[evo.pokemon].friendly_name
                    spoiler_handle.write(f"{pokemon_name} -> {evo.method} -> {evo_name}\n")

        if breeding_is_randomized(self):
            spoiler_handle.write(f"\nBreeding ({self.player_name}):\n")
            for pokemon, data in self.generated_pokemon.items():
                if not can_breed(self, pokemon): continue
                parent_name = self.generated_pokemon[pokemon].friendly_name
                child_name = self.generated_pokemon[data.produces_egg].friendly_name
                if child_name == "Nidoran F": child_name = "Nidoran F/Nidoran M"
                spoiler_handle.write(f"{parent_name} -> {child_name}\n")

        if self.options.randomize_pokemon_requests:
            request_pokemon = ", ".join(
                self.generated_pokemon[pokemon].friendly_name for pokemon in self.generated_request_pokemon)
            spoiler_handle.write(f"\nBill's Grandpa Pokemon ({self.player_name}): {request_pokemon}\n")

        if self.options.randomize_trades:
            spoiler_handle.write(f"\nTrades ({self.player_name}):\n")
            for trade in self.generated_trades.values():
                requested = self.generated_pokemon[trade.requested_pokemon].friendly_name
                received = self.generated_pokemon[trade.received_pokemon].friendly_name
                spoiler_handle.write(f"{trade.friendly_name}: {requested} -> {received}\n")

        if self.options.randomize_lucky_number_show:
            spoiler_handle.write(f"\nLucky Number Show ({self.player_name}):\n")
            prizes = ("1st Prize", "2nd Prize", "3rd Prize")
            for prize, trade_id in zip(prizes, self.generated_lucky_number_trades):
                trade = self.generated_trades[trade_id]
                requested = self.generated_pokemon[trade.requested_pokemon].friendly_name
                spoiler_handle.write(f"{prize}: {trade.friendly_name} ({requested})\n")

        if self.options.grasssanity == Grasssanity.option_one_per_area:
            spoiler_handle.write(f"\nGrass locations ({self.player_name}):\n")
            for loc_id in self.grass_location_mapping.keys():
                spoiler_handle.write(f"{self.location_id_to_name[int(loc_id)]}\n")

        if not self.options.field_moves_always_usable:
            hms = ("CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH")
            total_pokemon = len(self.generated_pokemon)
            low_compat_hms = [
                (hm, self.logic.compatible_hm_pokemon[hm])
                for hm in hms
                if total_pokemon > 0 and len(self.logic.compatible_hm_pokemon[hm]) / total_pokemon <= 0.20
            ]
            if low_compat_hms:
                spoiler_handle.write(f"\nHM Compatibility ({self.player_name}):\n")
                for hm, pokemon_ids in low_compat_hms:
                    names = ", ".join(self.generated_pokemon[pid].friendly_name for pid in pokemon_ids)
                    spoiler_handle.write(f"{hm.replace('_', ' ').title()}: {names}\n")

        if self.options.enable_mischief:
            spoiler_handle.write(f"\nMischief ({self.player_name}):\n")
            get_misc_spoiler_log(self, spoiler_handle.write)

    def extend_hint_information(self, hint_data: dict[int, dict[int, str]]):
        name_options = self._encounter_name_options()

        def whirl_flip(name: str) -> str:
            if MiscOption.WhirlDexLocations in self.generated_misc.selected and name.startswith("Whirl"):
                return name.replace(" N" if " N" in name else " S", " S" if " N" in name else " N") \
                    .replace("W " if "W " in name else "E ", "E " if "W " in name else "W ")
            return name

        def get_dexsanity_wild_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for key, encounters in self.generated_wild.items():
                if not dexsanity_wild_in_logic(self, key):
                    continue
                for i, encounter in enumerate(encounters):
                    if encounter.pokemon not in self.generated_dexsanity:
                        continue
                    dexsanity_hint_data[encounter.pokemon].add(whirl_flip(key.friendly_slot_region_name(i, **name_options)))
            if dexsanity_contest_in_logic(self):
                for encounter in self.generated_contest:
                    dexsanity_hint_data[encounter.pokemon].add("Bug Catching Contest")

        def get_dexsanity_static_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for key, static in self.generated_static.items():
                if static.pokemon not in self.generated_dexsanity or static.level_type == "ignore" or \
                        key.region_id in ["Entei", "Raikou"]:
                    continue
                dexsanity_hint_data[static.pokemon].add(key.friendly_region_name(**name_options))

        def get_dexsanity_evolution_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for pokemon_id, pokemon_data in self.generated_pokemon.items():
                for evo in pokemon_data.evolutions:
                    if not (evo.pokemon in self.generated_dexsanity and evolution_in_logic(self, evo)):
                        continue
                    hint_text = f"Evolve {self.generated_pokemon[pokemon_id].friendly_name}"
                    divergent_evolutions = ("EEVEE", "GLOOM", "POLIWHIRL", "SLOWPOKE", "TYROGUE")
                    if pokemon_id in divergent_evolutions:
                        hint_text += f" ({evo.method})"
                    dexsanity_hint_data[evo.pokemon].add(hint_text)

        def get_dexsanity_breeding_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for parent, data in self.generated_pokemon.items():
                if not can_breed(self, parent): continue
                child = data.produces_egg
                parent_name = self.generated_pokemon[parent].friendly_name
                if child == "NIDORAN_F" and parent != "NIDORAN_M" and "NIDORAN_M" in self.generated_dexsanity:
                    dexsanity_hint_data["NIDORAN_M"].add(f"Breed {parent_name}")
                if parent == child: continue
                if child in self.generated_dexsanity:
                    dexsanity_hint_data[child].add(f"Breed {parent_name}")

        def get_dexsanity_trade_hint_data(dexsanity_hint_data: dict[str, set[str]]):
            for trade in self.generated_trades.values():
                requested = self.generated_pokemon[trade.requested_pokemon].friendly_name
                dexsanity_hint_data[trade.received_pokemon].add(f"{trade.friendly_name} - Trade for {requested}")

        def get_entrance_hints() -> dict[str, set[str]]:
            def explore(region: Region, explored: set[str], shallowest: str | None) -> set[str]:
                """Recursively go back up regions' entrances to find the closest (shallowest)
                ERed entrances to an outdoor map that lead to this region"""
                entrance_hints = set()
                if region.name in explored: return entrance_hints

                map_name = "".join(w.title() for w in region.name.removeprefix("REGION_").split(":")[0].split("_"))
                # For the subset of regions this function gets called on, we can assert that none of the regions that
                # don't correspond to an in-game map are part of an outdoor map
                # These regions are shops, the Pokedex, the Battle Tower subregions, and the whirl entrance maps
                # (because the cardinals' case gets eaten by title())
                is_outdoor = map_name in crystal_data.maps and \
                        crystal_data.maps[map_name].environment in OUTDOOR_ENVIRONMENTS
                if is_outdoor:
                    added = {shallowest.removesuffix(" Entrance")} if shallowest is not None else set()
                    # Some maps are outdoors, but isolated, so we don't stop at them
                    if map_name not in {"MountMoonSquare", "TinTowerRoof", "OlivinePort", "VermilionPort",
                                        "NationalPark"}:
                        return added
                    # Unless we can fly there :^) (but we keep exploring the entrances that lead there)
                    if any(entrance for entrance in region.entrances if entrance.parent_region.name == "REGION_FLY"):
                        entrance_hints |= added

                explored.add(region.name)

                for parent_conn in region.entrances:
                    internal_name = internal_entrance_name(parent_conn.name)
                    if internal_name in crystal_data.entrance_connections:
                        entrance_category = crystal_data.entrance_connections[internal_name].category
                        is_er_conn = base_category(entrance_category) in self.options.randomize_entrances.value
                    else:
                        is_er_conn = False
                    next_shallowest = parent_conn.name if is_er_conn else shallowest
                    entrance_hints |= explore(parent_conn.parent_region, explored, next_shallowest)
                return entrance_hints

            region_entrance_hints = {}
            for region in self.get_regions():
                if any(location for location in region.locations
                       if location.address is not None
                       and location.player == self.player):
                    found_entrances = explore(region, set(), None)
                    if found_entrances:
                        region_entrance_hints[region.name] = found_entrances

            return region_entrance_hints

        player_hint_data = dict()
        if self.options.dexsanity:
            dexsanity_hint_data = defaultdict(set)
            get_dexsanity_wild_hint_data(dexsanity_hint_data)
            if dexsanity_statics_in_logic(self):
                get_dexsanity_static_hint_data(dexsanity_hint_data)
            if self.options.randomize_evolution and PokemonSourceLogic.EVOLUTION in self.options.dexsanity_logic.value:
                get_dexsanity_evolution_hint_data(dexsanity_hint_data)
            if dexsanity_breeding_in_logic(self) and breeding_is_randomized(self):
                get_dexsanity_breeding_hint_data(dexsanity_hint_data)
            if dexsanity_trades_in_logic(self):
                get_dexsanity_trade_hint_data(dexsanity_hint_data)
            player_hint_data |= {
                self.location_name_to_id[f"Pokedex - {self.generated_pokemon[pokemon_id].friendly_name}"]: ", ".join(
                    sorted(methods))
                for pokemon_id, methods in dexsanity_hint_data.items()}

        if self.options.randomize_entrances:
            region_entrance_hints = get_entrance_hints()
            for region, hint_entrances in region_entrance_hints.items():
                hint_str = ", ".join(sorted(hint_entrances))
                for location in self.get_region(region).locations:
                    if location.address is None or location.player != self.player: continue
                    player_hint_data[location.address] = hint_str

        if self.options.battle_tower_sanity.value == BattleTowerSanity.option_tiers_and_trainers:
            for tier in range(1, BATTLE_TOWER_NUM_TIERS + 1):
                tier_region = self.get_region(f"Battle Tower Tier {tier}")
                tier_trainers = [l for l in tier_region.locations if "Battle Tower Trainer" in l.tags]
                for battle, trainer_loc in enumerate(tier_trainers, start=1):
                    hint_str = f"Tier {tier} - Battle {battle}"
                    if trainer_loc.address not in player_hint_data:
                        player_hint_data[trainer_loc.address] = hint_str
                    else:
                        player_hint_data[trainer_loc.address] = f"{hint_str} @ " \
                                                                f"{player_hint_data[trainer_loc.address]}"

        hint_data[self.player] = player_hint_data

    def create_item(self, name: str) -> Item:
        if name == self.glitches_item_name: return PokemonCrystalGlitchedToken(self.player)
        return self.create_item_by_code(self.item_name_to_id[name])

    def get_filler_item_name(self) -> str:
        item = get_random_filler_item(self)
        return item_const_name_to_label(item)

    def create_item_by_const_name(self, item_const: str) -> PokemonCrystalItem:
        item_code = item_const_name_to_id(item_const)
        return self.create_item_by_code(item_code)

    def create_item_by_code(self, item_code: int) -> PokemonCrystalItem:
        item_data = crystal_data.items[item_code]
        override = get_classification_override(self, item_data)
        classification = override if override is not None else item_data.classification
        return PokemonCrystalItem(
            name=item_data.label,
            classification=classification,
            code=item_code,
            player=self.player,
            flag_index=item_data.flag_index
        )

    def has_species_via(self, state: CollectionState, species: str, sources: "frozenset[str]") -> bool:
        pi = state.prog_items[self.player]
        return any(pi[f"{species}@{src}"] for src in sources)

    def _get_dex_keys(self, species: str) -> tuple[str, ...]:
        cache = self._dex_keys_cache
        if cache is None:
            cache = self._dex_keys_cache = {}
        keys = cache.get(species)
        if keys is None:
            keys = cache[species] = tuple(f"{species}@{src}" for src in self.dex_sources)
        return keys

    def _get_request_keys(self, species: str) -> tuple[str, ...]:
        cache = self._request_keys_cache
        if cache is None:
            cache = self._request_keys_cache = {}
        keys = cache.get(species)
        if keys is None:
            keys = cache[species] = tuple(f"{species}@{src}" for src in self.request_sources)
        return keys

    def has_species_dex(self, state: CollectionState, species: str) -> bool:
        pi = state.prog_items[self.player]
        return any(pi[k] for k in self._get_dex_keys(species))

    def has_species_request(self, state: CollectionState, species: str) -> bool:
        pi = state.prog_items[self.player]
        return any(pi[k] for k in self._get_request_keys(species))

    def refresh_source_sets(self) -> None:
        """Recompute dex/request source sets from the current pool. Call after invalidate()."""
        self.dex_sources = self.pokemon_pool.effective_sources(self.options.dexsanity_logic,
                                                                required_species=self.generated_dexsanity)
        # Request selection (get_filtered) excludes UNOWN, so the gating must too, or a request
        # pool of only UNOWN reads as non-empty here and skips the all-sources fallback. Trades are
        # excluded for the same reason: the first trade picks before any trade is in the pool.
        self.request_sources = self.pokemon_pool.effective_sources(self.options.pokemon_request_logic,
                                                                    exclude_unown=True, without_trades=True)
        self._dex_keys_cache = None
        self._request_keys_cache = None

    def create_event(self, name: str, source: str | None = None) -> PokemonCrystalItem:
        return PokemonCrystalItem(
            name=name,
            classification=ItemClassification.progression,
            code=None,
            player=self.player,
            source=source
        )

    def get_world_collection_state(self) -> CollectionState:
        state = CollectionState(self.multiworld, True)
        progression_items = [item for item in self.itempool if item.advancement]
        locations = self.get_locations()
        for item in progression_items:
            state.collect(item, True)
        for item in self.get_pre_fill_items():
            state.collect(item, True)
        state.sweep_for_advancements(locations)
        return state

    def get_pre_fill_items(self):
        pre_fill_items = self.pre_fill_items.copy()
        if self.logic.guaranteed_hm_access:
            for hm in ("CUT", "FLY", "SURF", "STRENGTH", "FLASH", "WHIRLPOOL", "WATERFALL", "HEADBUTT", "ROCK_SMASH"):
                pre_fill_items.append(self.create_event(f"Teach {hm}"))
        return pre_fill_items

    def collect(self, state: CollectionState, item: Item) -> bool:
        changed = super().collect(state, item)
        if not changed:
            return False
        item_name = item.name
        if item_name in self.logic.pokemon_hm_use:
            state.prog_items[self.player].update(self.logic.pokemon_hm_use[item_name])
        source_key: str | None = getattr(item, "source_key", None)
        if source_key is not None:
            player = self.player
            pi = state.prog_items[player]
            pi[source_key] += 1
            if pi[item_name] == 1:
                state.pc_unique_species[player] += 1
            if item.source in self.dex_sources:
                seen = state.pc_dex_species_seen[player]
                if item_name not in seen:
                    seen.add(item_name)
                    state.pc_dex_species_count[player] += 1
        return True

    def remove(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if not changed:
            return False
        item_name = item.name
        if item_name in self.logic.pokemon_hm_use:
            state.prog_items[self.player].subtract(self.logic.pokemon_hm_use[item_name])
        source_key = getattr(item, "source_key", None)
        if source_key is not None:
            player = self.player
            pi = state.prog_items[player]
            pi[source_key] -= 1
            if pi[item_name] == 0:
                state.pc_unique_species[player] -= 1
            if item.source in self.dex_sources:
                seen = state.pc_dex_species_seen[player]
                if item_name in seen and not any(pi[f"{item_name}@{s}"] for s in self.dex_sources):
                    seen.discard(item_name)
                    state.pc_dex_species_count[player] -= 1
        return True

    # UT Stuff

    @property
    def ut_slot_data(self) -> dict[str, Any]:
        if hasattr(self.multiworld, "re_gen_passthrough"):
            return self.multiworld.re_gen_passthrough[self.game]
        else:
            return {}

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]):
        return slot_data

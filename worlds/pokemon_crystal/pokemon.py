import logging
import random
from collections.abc import Iterable
from dataclasses import replace
from typing import TYPE_CHECKING

from BaseClasses import ItemClassification, CollectionState, Location
from rule_builder.rules import Rule, And, HasAny
from worlds.generic.Rules import add_rule
from .data import data as crystal_data, LogicalAccess, EncounterType, MiscOption, EncounterMon, GrowthRate, \
    EvolutionType
from .evolution import get_random_pokemon_evolution
from .items import get_random_filler_item
from .logic_rules import ResolvedRule
from .moves import get_tmhm_compatibility, randomize_learnset, moves_convert_friendly_to_ids
from .options import RandomizeTypes, ModifyPalettes, RandomizeBaseStats, BaseStatsEvolutionMode, RandomizeStarters, \
    RandomizeTrades, DexsanityStarters, EncounterGrouping, RandomizePokemonRequests, Goal, GrowthRates, \
    WildEncounterMethodsRequired, PokemonSourceLogic
from .pokemon_pool import ENCOUNTER_TYPE_TO_SOURCE_KEY
from .pokemon_data import ALL_UNOWN, LEGENDARY_POKEMON, NON_LEGENDARY_POKEMON
from .utils import should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

# eeveelutions never inherit from their pre-evolution, they each get their own types and stats
__EEVEELUTIONS = ("FLAREON", "JOLTEON", "VAPOREON", "ESPEON", "UMBREON")

# maximum base form bst by number of stages in the evolution line
__LINE_BASE_BST_MAX = {1: 681, 2: 521, 3: 421}


def randomize_pokemon_data(world: "PokemonCrystalWorld"):
    if world.options.growth_rates == GrowthRates.option_normalized:
        for pkmn_name, pkmn_data in world.generated_pokemon.items():
            new_rate = GrowthRate.Slow if pkmn_data.friendly_name in LEGENDARY_POKEMON else GrowthRate.MediumFast
            if pkmn_data.growth_rate != new_rate:
                world.generated_pokemon[pkmn_name] = replace(pkmn_data, growth_rate=new_rate)

    # follow_evolutions can change types after the pokemon has already been randomized,
    # so we randomize types before all else
    if world.options.randomize_types.value:
        for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[0]):
            evolution_line_list = [pkmn_name]
            if world.options.randomize_types.value == RandomizeTypes.option_follow_evolutions:
                # skip evolved pokemon if follow_evolutions
                if not pkmn_data.is_base and pkmn_name not in __EEVEELUTIONS:
                    continue
                for evo in pkmn_data.evolutions:
                    evolution_line_list.append(evo.pokemon)
                    evo_poke = world.generated_pokemon[evo.pokemon]
                    for second_evo in evo_poke.evolutions:
                        evolution_line_list.append(second_evo.pokemon)

            new_types = get_random_types(world)
            for pokemon in evolution_line_list:
                world.generated_pokemon[pokemon] = replace(
                    world.generated_pokemon[pokemon],
                    types=new_types
                )

    move_blocklist = moves_convert_friendly_to_ids(world, world.options.move_blocklist)

    # random evolutions already require an increasing bst, and they are not known until create_regions
    follow_evolutions = (world.options.base_stats_evolution_mode == BaseStatsEvolutionMode.option_follow_evolutions
                         and world.options.randomize_base_stats.value
                         and not world.options.randomize_evolution.value)
    if follow_evolutions:
        randomize_base_stats_by_line(world)

    for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[0]):
        new_base_stats = pkmn_data.base_stats
        new_learnset = pkmn_data.learnset
        new_tm_hms = pkmn_data.tm_hm

        if world.options.modify_palettes.value and world.options.modify_palettes.value != ModifyPalettes.option_swap_shiny:
            if world.options.modify_palettes.value == ModifyPalettes.option_match_types:
                world.generated_palettes[pkmn_name] = get_type_colors(pkmn_data.types, world.random)
            elif world.options.modify_palettes.value == ModifyPalettes.option_randomize:
                world.generated_palettes[pkmn_name] = get_random_colors(world.random)
            else: # modify_palettes is gold_and_silver
                if pkmn_name in __GS_PALETTES:
                    world.generated_palettes[pkmn_name] = get_gs_colors(pkmn_name)

        if world.options.randomize_base_stats.value and not follow_evolutions:
            multiple = 5 if world.options.base_stats_multiples_of_five else 1

            if world.options.randomize_base_stats.value == RandomizeBaseStats.option_keep_bst:
                new_base_stats = get_random_base_stats(world.random, multiple, pkmn_data.bst)
            else:
                new_base_stats = get_random_base_stats(world.random, multiple)

        if world.options.randomize_learnsets or world.options.metronome_only:
            new_learnset = randomize_learnset(world, pkmn_name, move_blocklist)

        if (world.options.tm_same_type_compatibility >= 0
                or world.options.tm_other_type_compatibility >= 0
                or world.options.hm_same_type_compatibility >= 0
                or world.options.hm_other_type_compatibility >= 0
                or world.options.hm_compatibility_override.value):
            new_tm_hms = get_tmhm_compatibility(world, pkmn_name)

        world.generated_pokemon[pkmn_name] = replace(
            world.generated_pokemon[pkmn_name],
            tm_hm=new_tm_hms,
            learnset=new_learnset,
            base_stats=new_base_stats,
            bst=sum(new_base_stats)
        )

    if world.options.randomize_base_stats.value:
        multiple = 5 if world.options.base_stats_multiples_of_five else 1
        for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[0]):
            if not any(evo.evo_type is EvolutionType.Stats for evo in pkmn_data.evolutions):
                continue
            new_base_stats = list(pkmn_data.base_stats)
            physical_total = new_base_stats[1] + new_base_stats[2]
            new_base_stats[1] = new_base_stats[2] = physical_total // (2 * multiple) * multiple
            remainder = physical_total - 2 * new_base_stats[1]
            if remainder:
                candidates = [i for i in (0, 3, 4, 5) if new_base_stats[i] + remainder <= 255]
                new_base_stats[world.random.choice(candidates)] += remainder
            world.generated_pokemon[pkmn_name] = replace(
                pkmn_data,
                base_stats=new_base_stats,
                bst=sum(new_base_stats)
            )

    if MiscOption.DontFuckleWithShuckle.value in world.generated_misc.selected:
        new_base_stats = list(world.generated_pokemon["SHUCKLE"].base_stats)
        attack = new_base_stats[1]
        new_base_stats[1] = new_base_stats[2]
        new_base_stats[2] = attack
        sp_atk = new_base_stats[4]
        new_base_stats[4] = new_base_stats[5]
        new_base_stats[5] = sp_atk
        world.generated_pokemon["SHUCKLE"] = replace(
            world.generated_pokemon["SHUCKLE"],
            base_stats=new_base_stats,
        )


def randomize_starters(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.randomize_starters: return

    blocklist = world.options.starter_blocklist.get_ids(world)

    base_only = world.options.randomize_starters.value == RandomizeStarters.option_unevolved_only
    for evo_line in world.generated_starters:
        starter_pokemon = get_random_pokemon(world, base_only=base_only, starter=True, exclude_unown=True,
                                             blocklist=blocklist)
        blocklist.add(starter_pokemon)
        starter_data = world.generated_pokemon[starter_pokemon]
        evo_line[0] = starter_pokemon

        middle_evo_pokemon = get_random_pokemon_evolution(world.random, starter_pokemon, starter_data)
        middle_data = world.generated_pokemon[middle_evo_pokemon]
        evo_line[1] = middle_evo_pokemon

        final_evo_pokemon = get_random_pokemon_evolution(world.random, middle_evo_pokemon, middle_data)
        evo_line[2] = final_evo_pokemon

    if MiscOption.UnLuckyEgg.value in world.generated_misc.selected:
        new_helditems = ("LUCKY_EGG", "LUCKY_EGG", "LUCKY_EGG")
    else:
        new_helditems = (get_random_filler_item(world),
                         get_random_filler_item(world),
                         get_random_filler_item(world))

    world.generated_starter_helditems = new_helditems


def randomize_trade_received_pokemon(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker: return

    if world.options.randomize_trades.value not in (RandomizeTrades.option_received,
                                                    RandomizeTrades.option_both): return

    blocklist = world.options.static_blocklist.get_ids(world) | getattr(world, "unique_static_wild_block", set())
    for trade_id, trade in world.generated_trades.items():
        received_pokemon = trade.received_pokemon
        world.generated_trades[trade_id] = replace(
            trade,
            received_pokemon=get_random_pokemon(world, blocklist=blocklist or None),
            held_item=get_random_filler_item(world) if received_pokemon != "ABRA" else "TM_9"
        )


def randomize_trade_requested_pokemon(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker: return

    # Vanilla/received keep the vanilla requested species (__adjust_options_trades keeps them obtainable).
    if world.options.randomize_trades.value not in (RandomizeTrades.option_requested,
                                                    RandomizeTrades.option_both): return

    # Clearing every request first and assigning one at a time keeps a trade out of the pool until
    # it's assigned, so no trade can be asked for a Pokemon only another trade provides.
    world.pokemon_pool.trade_requests_assigned = True
    for trade_id, trade in world.generated_trades.items():
        world.generated_trades[trade_id] = replace(trade, requested_gender=0, requested_pokemon="")

    trade_ids = sorted(world.generated_trades)
    world.random.shuffle(trade_ids)

    requested = set[str]()
    for trade_id in trade_ids:
        world.pokemon_pool.invalidate()
        logically_available_pokemon = world.pokemon_pool.get_filtered(world.options.pokemon_request_logic,
                                                                      exclude_unown=True)

        assert logically_available_pokemon
        pokemon = world.random.choice(sorted(logically_available_pokemon - requested)
                                      or sorted(logically_available_pokemon))

        world.generated_trades[trade_id] = replace(world.generated_trades[trade_id], requested_pokemon=pokemon)
        requested.add(pokemon)

    world.pokemon_pool.invalidate()


def randomize_request_pokemon(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker: return

    if world.options.randomize_pokemon_requests in (RandomizePokemonRequests.option_items_and_pokemon,
                                                    RandomizePokemonRequests.option_pokemon):

        request_pool = world.pokemon_pool.get_filtered(world.options.pokemon_request_logic, exclude_unown=True)
        logically_available_pokemon = sorted(request_pool)

        assert logically_available_pokemon
        while len(logically_available_pokemon) < len(world.generated_request_pokemon):
            logically_available_pokemon.append(world.random.choice(logically_available_pokemon))

        world.random.shuffle(logically_available_pokemon)
        world.generated_request_pokemon = [logically_available_pokemon.pop() for _ in world.generated_request_pokemon]
    elif world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
        # ideally we should never need this, but best to be safe
        request_pool = world.pokemon_pool.get_filtered(world.options.pokemon_request_logic, exclude_unown=True)
        logically_available_pokemon = sorted(request_pool)

        world.generated_request_pokemon = [
            world.random.choice(logically_available_pokemon) if mon not in request_pool else mon for
            mon in world.generated_request_pokemon]


def fill_trade_locations(world: "PokemonCrystalWorld"):
    # Trades that aren't required still exist under UT, gated behind glitched logic.
    if not world.options.trades_required and not world.is_universal_tracker: return

    for trade_id, trade in world.generated_trades.items():
        try:
            location = world.get_location(trade_id)
            location.place_locked_item(world.create_event(trade.received_pokemon,
                                                          source=PokemonSourceLogic.TRADES))
        except KeyError:
            continue


def ensure_fly_learner_in_sphere_1(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.early_fly or world.options.field_moves_always_usable:
        return

    fly_override = world.options.hm_compatibility_override.value.get("Fly")
    if fly_override == 100:
        return
    if (fly_override is None
            and world.options.hm_same_type_compatibility.value == 100
            and world.options.hm_other_type_compatibility.value == 100):
        return

    fly_learners = set(world.logic.compatible_hm_pokemon["FLY"])

    state = CollectionState(world.multiworld)
    locations = world.multiworld.get_reachable_locations(state=state, player=world.player)
    early_region_keys = {
        loc.parent_region.key for loc in locations
        if "wild encounter" in loc.tags
        and world.logic.wild_regions[loc.parent_region.key] is LogicalAccess.InLogic
    }

    sphere_1_species: set[str] = set()
    for key in early_region_keys:
        for enc in world.generated_wild.get(key, ()):
            sphere_1_species.add(enc.pokemon)
        if key in world.generated_static:
            sphere_1_species.add(world.generated_static[key].pokemon)

    if sphere_1_species & fly_learners:
        return

    if not sphere_1_species:
        logging.warning(
            "Pokemon Crystal: early_fly is enabled but no sphere 1 Pokemon are catchable "
            "for player %s (%s); HM02 Fly may be unusable until later.",
            world.player, world.player_name)
        return

    target = world.random.choice(sorted(sphere_1_species))
    pkmn = world.generated_pokemon[target]
    if "FLY" not in pkmn.tm_hm:
        world.generated_pokemon[target] = replace(pkmn, tm_hm=tuple(pkmn.tm_hm) + ("FLY",))
        world.logic.add_hm_compatible_pokemon("FLY", target)


def place_starters_in_early_wilds(world: "PokemonCrystalWorld", allow_partial_entrances: bool = False):
    if (world.options.dexsanity_starters.value != DexsanityStarters.option_available_early
            or world.is_universal_tracker):
        return

    # Only move starters between encounter types that dexsanity_logic actually counts. Otherwise the
    # swap could shift a starter into an uncounted type (e.g. Land when only Fishing counts), silently
    # dropping it from the logical dex pool and desyncing the dexcountsanity milestones.
    def counts_for_dex(region) -> bool:
        return ENCOUNTER_TYPE_TO_SOURCE_KEY.get(region.key.encounter_type) in world.options.dexsanity_logic

    locations = world.multiworld.get_reachable_locations(
        state=CollectionState(world.multiworld, allow_partial_entrances=allow_partial_entrances),
        player=world.player)
    early_wild_regions = [loc.parent_region for loc in locations if "wild encounter" in loc.tags]
    early_wild_regions = [region for region in early_wild_regions if
                          world.logic.wild_regions[region.key] is LogicalAccess.InLogic
                          and region.key.encounter_type is not EncounterType.Static
                          and counts_for_dex(region)]
    early_wild_regions.sort(key=lambda region: region.name)
    world.random.shuffle(early_wild_regions)

    other_wild_regions = [loc.parent_region for loc in world.multiworld.get_locations(world.player) if
                          "wild encounter" in loc.tags
                          and loc.parent_region not in early_wild_regions
                          and world.logic.wild_regions[loc.parent_region.key] is LogicalAccess.InLogic
                          and loc.parent_region.key.encounter_type is not EncounterType.Static
                          and counts_for_dex(loc.parent_region)]
    other_wild_regions.sort(key=lambda region: region.name)
    world.random.shuffle(other_wild_regions)

    if not early_wild_regions:
        logging.warning(
            "Pokemon Crystal: dexsanity_starters is available_early but no sphere 1 wild encounters exist "
            "for player %s (%s); starters could not be placed early.",
            world.player, world.player_name)
        return
    if not other_wild_regions:
        return

    unplaced: list[str] = []
    for evo_line in world.generated_starters:
        starter = evo_line[0]
        if not early_wild_regions:
            unplaced.append(starter)
            continue
        source_region = None
        source_encounters = None

        if any(encounter
               for region in early_wild_regions
               for encounter in world.generated_wild[region.key]
               if encounter.pokemon == starter):
            continue

        for region in other_wild_regions:
            source_encounters = world.generated_wild[region.key]
            if starter in [encounter.pokemon for encounter in source_encounters]:
                source_region = region
                break

        if not source_region:
            unplaced.append(starter)
            continue
        target_region = None
        target_encounters: list[EncounterMon] = []
        while not target_encounters:
            if not early_wild_regions: break
            target_region = early_wild_regions.pop()
            target_encounters = world.generated_wild[target_region.key]

        if not target_encounters:
            unplaced.append(starter)
            continue

        if (world.options.encounter_grouping == EncounterGrouping.option_one_to_one
                or not world.options.randomize_wilds):
            pokemon_to_swap = target_encounters[0].pokemon
            target_indexes = [i for i, enc in enumerate(target_encounters) if enc.pokemon == pokemon_to_swap]
            source_indexes = [i for i, enc in enumerate(source_encounters) if enc.pokemon == starter]
            for i in target_indexes:
                target_encounters[i] = replace(target_encounters[i], pokemon=starter)
            for i in source_indexes:
                source_encounters[i] = replace(source_encounters[i], pokemon=pokemon_to_swap)
        elif world.options.encounter_grouping.value == EncounterGrouping.option_all_split:
            starter_index = next(
                i for i, encounter in enumerate(source_encounters) if encounter.pokemon == starter)
            source_encounters[starter_index] = replace(source_encounters[starter_index],
                                                       pokemon=target_encounters[0].pokemon)
            target_encounters[0] = replace(target_encounters[0], pokemon=starter)
        else:
            pokemon_to_swap = target_encounters[0].pokemon
            target_encounters = [replace(mon, pokemon=starter) for mon in target_encounters]
            source_encounters = [replace(mon, pokemon=pokemon_to_swap) for mon in source_encounters]
        world.generated_wild[source_region.key] = source_encounters
        world.generated_wild[target_region.key] = target_encounters

    if unplaced:
        logging.warning(
            "Pokemon Crystal: dexsanity_starters is available_early but %s could not be placed in sphere 1 "
            "for player %s (%s).",
            ", ".join(unplaced), world.player, world.player_name)


def add_unown_unlock_rule(world: "PokemonCrystalWorld", location: Location):
    unlocked = HasAny("ENGINE_UNLOCKED_UNOWNS_A_TO_K", "ENGINE_UNLOCKED_UNOWNS_L_TO_R",
                      "ENGINE_UNLOCKED_UNOWNS_S_TO_W", "ENGINE_UNLOCKED_UNOWNS_X_TO_Z")
    existing = location.access_rule
    if isinstance(existing, Rule.Resolved):
        world.set_rule(location, And(ResolvedRule(existing), unlocked))
    else:
        resolved = unlocked.resolve(world)
        world.register_rule_dependencies(resolved)
        add_rule(location, resolved)


def fill_wild_encounter_locations(world: "PokemonCrystalWorld"):
    for region_key, encounters in world.generated_wild.items():
        region_logic = world.logic.wild_regions[region_key]
        if region_logic is LogicalAccess.InLogic or (
                world.is_universal_tracker and region_logic is LogicalAccess.OutOfLogic):
            wild_source = ENCOUNTER_TYPE_TO_SOURCE_KEY.get(region_key.encounter_type)
            seen_pokemon = set()
            for i, encounter in enumerate(encounters):
                location = world.get_location(f"{region_key.region_name()}_{i + 1}")
                location.place_locked_item(world.create_event(encounter.pokemon, source=wild_source))
                if encounter.pokemon == "UNOWN":
                    add_unown_unlock_rule(world, location)
                if encounter.pokemon in seen_pokemon:
                    location.item.classification = ItemClassification.useful
                seen_pokemon.add(encounter.pokemon)

    for region_key, static in world.generated_static.items():
        access = world.logic.wild_regions[region_key]
        if access is LogicalAccess.InLogic or (world.is_universal_tracker and access is LogicalAccess.OutOfLogic):
            location = world.get_location(f"{region_key.region_name()}_1")
            location.place_locked_item(world.create_event(static.pokemon, source=PokemonSourceLogic.STATICS))

    if WildEncounterMethodsRequired.BUG_CATCHING_CONTEST in world.options.wild_encounter_methods_required or world.is_universal_tracker:
        for i, slot in enumerate(world.generated_contest):
            location = world.get_location(f"Bug Catching Contest Slot {i + 1}")
            location.place_locked_item(world.create_event(slot.pokemon,
                                                          source=PokemonSourceLogic.BUG_CATCHING_CONTEST))


def build_pokemon_pool_index(world: "PokemonCrystalWorld"):
    """Pre-compute indexed pokemon pools for fast lookup by type and BST.

    Must be called after all pokemon data mutations (types, base stats, evolutions) are finalized."""
    from bisect import insort

    by_type: dict[str, set[str]] = {}
    bst_sorted: list[tuple[int, str]] = []
    all_names: set[str] = set()
    base_only_names: set[str] = set()
    fully_evolved_names: set[str] = set()

    for pkmn_name, pkmn_data in world.generated_pokemon.items():
        all_names.add(pkmn_name)
        for t in pkmn_data.types:
            by_type.setdefault(t, set()).add(pkmn_name)
        insort(bst_sorted, (pkmn_data.bst, pkmn_name))
        if pkmn_data.is_base:
            base_only_names.add(pkmn_name)
        if not pkmn_data.evolutions:
            fully_evolved_names.add(pkmn_name)

    world._pokemon_pool_index = {
        "by_type": by_type,
        "bst_sorted": bst_sorted,
        "all": all_names,
        "base_only": base_only_names,
        "fully_evolved": fully_evolved_names,
        "evolved_pool_cache": {},
    }


def _level_evolutions(world: "PokemonCrystalWorld", pokemon: str, level: int):
    """Evolutions of a species that would have triggered by the given level."""
    return [evo for evo in world.generated_pokemon[pokemon].evolutions
            if evo.evo_type in (EvolutionType.Level, EvolutionType.Stats)
            and evo.level is not None and evo.level <= level]


def get_evolution_at_level(world: "PokemonCrystalWorld", pokemon: str, level: int) -> str:
    """
    Returns the Pokemon this species would have naturally evolved into by the given level.
    If more than one level evolution is available, one is picked at random
    """
    evolutions = _level_evolutions(world, pokemon, level)
    if not evolutions:
        return pokemon

    return get_evolution_at_level(world, world.random.choice(evolutions).pokemon, level)


def get_evolution_forms_at_level(world: "PokemonCrystalWorld", pokemon: str, level: int) -> set[str]:
    """Every form this species could have naturally evolved into by the given level."""
    evolutions = _level_evolutions(world, pokemon, level)
    if not evolutions:
        return {pokemon}

    return set().union(*(get_evolution_forms_at_level(world, evo.pokemon, level) for evo in evolutions))


def _evolved_pool_weights(world: "PokemonCrystalWorld", names: set[str], level: int,
                          cacheable: bool) -> dict[str, int]:
    """Evolve every name to the forms it would have reached at this level, weighted by how many evolve into it."""
    from collections import Counter

    cache = world._pokemon_pool_index["evolved_pool_cache"]
    if cacheable and level in cache:
        return cache[level]

    weights = Counter()
    for name in names:
        weights.update(get_evolution_forms_at_level(world, name, level))
    if cacheable:
        cache[level] = weights
    return weights


def _filter_bst_range(bst_sorted: list[tuple[int, str]], target_bst: int, bst_range: float) -> set[str]:
    """Return names of pokemon whose BST is within range of target, using binary search."""
    from bisect import bisect_left, bisect_right

    lo = bisect_left(bst_sorted, (int(target_bst - bst_range),))
    hi = bisect_right(bst_sorted, (int(target_bst + bst_range), "\xff"))
    return {name for _, name in bst_sorted[lo:hi]}


def get_random_pokemon(world: "PokemonCrystalWorld", priority_pokemon: set[str] | None = None, types=None,
                       base_only=False, force_fully_evolved_at=None, current_level=None, starter=False,
                       exclude_unown=False, blocklist: set[str] | None = None,
                       match_bst: int | None = None, evolve_at_level: int | None = None,
                       rng: random.Random | None = None) -> str:
    index = world._pokemon_pool_index
    rng = rng or world.random

    # Start with either the priority set or the full set
    if priority_pokemon:
        pool = set(priority_pokemon)
    else:
        pool = set(index["all"])

    # Evolve the pool up front so the filters below apply to the species that actually gets used
    evolved_weights = None
    if evolve_at_level is not None:
        evolved_weights = _evolved_pool_weights(world, pool, evolve_at_level, not priority_pokemon)
        pool = set(evolved_weights)

    # Apply blocklist
    if blocklist:
        pool -= blocklist

    # Exclude Unown
    if exclude_unown:
        pool.discard("UNOWN")

    # Filter by type — keep pokemon that match at least one of the requested types
    if types is not None:
        type_matches = set()
        for t in set(types):
            type_pool = index["by_type"].get(t)
            if type_pool:
                type_matches |= type_pool
        pool &= type_matches

    # Base-only filter
    if base_only:
        pool &= index["base_only"]

    # Force fully evolved filter
    if force_fully_evolved_at and current_level is not None and current_level >= force_fully_evolved_at:
        pool &= index["fully_evolved"]

    # Starter-specific filters
    if starter:
        if world.options.randomize_starters == RandomizeStarters.option_first_stage_can_evolve:
            pool &= index["base_only"] - index["fully_evolved"]
        elif world.options.randomize_starters == RandomizeStarters.option_base_stat_mode:
            bst_avg = world.options.starters_bst_average
            bst_matches = _filter_bst_range(index["bst_sorted"], bst_avg, bst_avg * .10)
            starter_pool = pool & bst_matches
            if not starter_pool:
                bst_matches = _filter_bst_range(index["bst_sorted"], bst_avg, bst_avg * .20)
                starter_pool = pool & bst_matches
            if starter_pool:
                pool = starter_pool

    # BST matching for trainer pokemon
    if match_bst is not None:
        bst_matches = _filter_bst_range(index["bst_sorted"], match_bst, match_bst * .10)
        bst_pool = pool & bst_matches
        if not bst_pool:
            bst_matches = _filter_bst_range(index["bst_sorted"], match_bst, match_bst * .20)
            bst_pool = pool & bst_matches
        if bst_pool:
            pool = bst_pool

    # Final fallback — if everything got filtered out, use all pokemon
    if not pool:
        pool = set(evolved_weights) if evolved_weights else set(index["all"])
        if exclude_unown:
            pool.discard("UNOWN")

    names = sorted(pool)
    if evolved_weights:
        return rng.choices(names, weights=[evolved_weights[name] for name in names])[0]
    return rng.choice(names)


def get_random_nezumi(random):
    # 🐁
    pokemon_pool = ["RATTATA", "RATICATE", "NIDORAN_F", "NIDORAN_M", "NIDORINA", "NIDORINO", "PIKACHU", "RAICHU",
                    "SANDSHREW", "SANDSLASH", "CYNDAQUIL", "QUILAVA", "SENTRET", "FURRET", "MARILL"]
    return random.choice(pokemon_pool)


def _locations_to_pokemon(world: "PokemonCrystalWorld", locations: Iterable[str]) -> set[str]:
    pokemon = set()
    for location in locations:
        parts = location.split("- ")
        if len(parts) != 2: continue
        if "Catch" in parts[1]: continue
        pokemon.add(parts[1])

    if "_Legendaries" in pokemon:
        pokemon.discard("_Legendaries")
        pokemon.update(LEGENDARY_POKEMON)
    elif "_Non-Legendaries" in pokemon:
        pokemon.discard("_Non-Legendaries")
        pokemon.update(NON_LEGENDARY_POKEMON)

    pokemon_ids = {pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                   pokemon_data.friendly_name in pokemon}

    return pokemon_ids


def get_chamber_event_for_unown(unown_letter: str) -> str:
    char = unown_letter[-1]
    if char < "L": return "ENGINE_UNLOCKED_UNOWNS_A_TO_K"
    if char < "S": return "ENGINE_UNLOCKED_UNOWNS_L_TO_R"
    if char < "X": return "ENGINE_UNLOCKED_UNOWNS_S_TO_W"
    return "ENGINE_UNLOCKED_UNOWNS_X_TO_Z"


def randomize_unown_signs(world: "PokemonCrystalWorld"):
    if Goal.UNOWN_HUNT not in world.options.goal: return
    available_signs = []
    for region in crystal_data.regions.values():
        if not should_include_region(region, world): continue
        for sign in region.signs:
            available_signs.append(sign)

    all_unown = list(ALL_UNOWN)
    world.random.shuffle(all_unown)
    world.random.shuffle(available_signs)

    for unown in all_unown:
        world.generated_unown_signs[available_signs.pop()] = unown


def get_priority_dexsanity(world: "PokemonCrystalWorld") -> set[str]:
    return _locations_to_pokemon(world, world.options.priority_locations.value)


def get_excluded_dexsanity(world: "PokemonCrystalWorld") -> set[str]:
    return _locations_to_pokemon(world, world.options.exclude_locations.value)


def get_pokemon_id_by_rom_id(id: int) -> str:
    return next(poke_id for poke_id, poke_data in crystal_data.pokemon.items() if poke_data.id == id)


def get_random_base_stats(random, multiple=1, bst=None):
    if bst is None:
        # sunkern to mewtwo
        bst = random.randrange(180, 681, multiple)
    return __base_stats_from_weights(random, __random_stat_weights(random), bst, multiple)


def __random_stat_weights(random):
    # add 0.5 to prevent a single stat exceeding 255
    # biggest possible variance on max bst is (1.5 * 680) / 4 = 255
    return [random.random() + 0.5 for _i in range(0, 6)]


def __jitter_stat_weights(random, weights):
    # clamped to the range of a fresh roll so the 255 cap still holds
    return [min(1.5, max(0.5, weight + random.uniform(-0.15, 0.15))) for weight in weights]


def __base_stats_from_weights(random, weights, bst, multiple):
    # multiple must not be a number where half-to-even rounds ((1.5 * 680) / (4 * multiple)) upward
    total = sum(weights)
    base_stats = [int(round((stat * bst) / (total * multiple)) * multiple) for stat in weights]
    return __place_base_stats_remainder(random, base_stats, bst - sum(base_stats), random.randint(0, 5))


def randomize_base_stats_by_line(world: "PokemonCrystalWorld"):
    multiple = 5 if world.options.base_stats_multiples_of_five else 1
    keep_bst = world.options.randomize_base_stats.value == RandomizeBaseStats.option_keep_bst

    for pkmn_name, pkmn_data in sorted(world.generated_pokemon.items(), key=lambda x: x[0]):
        if not pkmn_data.is_base:
            continue
        bst = pkmn_data.bst if keep_bst else world.random.randrange(
            180, __LINE_BASE_BST_MAX[__evolution_line_stages(world, pkmn_name)], multiple)
        __apply_line_base_stats(world, pkmn_name, __random_stat_weights(world.random), bst, multiple, keep_bst, set())


def __evolution_line_stages(world: "PokemonCrystalWorld", pkmn_name: str, explored: set[str] | None = None) -> int:
    if explored is None:
        explored = set()
    if pkmn_name in explored:
        return 0
    explored.add(pkmn_name)
    evolutions = world.generated_pokemon[pkmn_name].evolutions
    return 1 + max((__evolution_line_stages(world, evo.pokemon, explored) for evo in evolutions), default=0)


def __apply_line_base_stats(world: "PokemonCrystalWorld", pkmn_name: str, weights: list[float], bst: int,
                            multiple: int, keep_bst: bool, explored: set[str]):
    if pkmn_name in explored:
        return
    explored.add(pkmn_name)

    pkmn_data = world.generated_pokemon[pkmn_name]
    base_stats = __base_stats_from_weights(world.random, weights, bst, multiple)
    world.generated_pokemon[pkmn_name] = replace(pkmn_data, base_stats=base_stats, bst=sum(base_stats))

    for evo in pkmn_data.evolutions:
        evo_weights = (__random_stat_weights(world.random) if evo.pokemon in __EEVEELUTIONS
                       else __jitter_stat_weights(world.random, weights))
        # under keep_bst the evolution keeps its own vanilla bst, which is never lower than its pre-evolution's
        evo_bst = (world.generated_pokemon[evo.pokemon].bst if keep_bst
                   else __evolved_bst(world.random, bst, multiple))
        __apply_line_base_stats(world, evo.pokemon, evo_weights, evo_bst, multiple, keep_bst, explored)


def __evolved_bst(random, bst, multiple):
    return min(680, int(round(bst * random.uniform(1.15, 1.5) / multiple) * multiple))


def __place_base_stats_remainder(random, stats: list[int], remainder: int, stat: int):
    if remainder == 0:
        return stats

    new_base_stat = stats[stat] + remainder
    if new_base_stat > 255 or new_base_stat < 5:
        stats = __place_base_stats_remainder(random, stats, remainder, (stat + 1) % 6)
    else:
        stats[stat] = new_base_stat
    return stats

def get_random_types(world: "PokemonCrystalWorld") -> list[str]:
    all_types = list(crystal_data.types.keys())
    if world.options.shared_primary_type:
        new_types = [type_id for type_id, type_data in crystal_data.types.items() if
                     type_data.rom_id == world.options.shared_primary_type.value - 1]
    else:
        new_types = [world.random.choice(all_types)]
    # approx. 110/251 Pokemon are dual type in gen 2
    if world.random.randint(0, 24) < 11:
        new_types.append(world.random.choice([t for t in all_types if t not in new_types]))
    return new_types


def add_hm_compatibility(world: "PokemonCrystalWorld", pokemon_id: str, hm: str):
    pokemon_data = world.generated_pokemon[pokemon_id]
    world.generated_pokemon[pokemon_id] = replace(pokemon_data, tm_hm=[hm] + list(pokemon_data.tm_hm))
    world.logic.add_hm_compatible_pokemon(hm, pokemon_id)


# palettes stuff
def get_random_colors(random):
    return [
        c for _ in range(4)
        for c in convert_color(random.randint(0, 31), random.randint(0, 31), random.randint(0, 31))
    ]


def get_type_colors(types, random):
    type1 = types[0]
    type2 = types[-1]

    c1 = type_palettes[type1][0]
    c2 = type_palettes[type2][1]

    r1, g1, b1 = shift_color(c1[0], c1[1], c1[2], random)
    r2, g2, b2 = shift_color(c2[0], c2[1], c2[2], random)

    # normal colors
    color1 = convert_color(r1, g1, b1)
    color2 = convert_color(r2, g2, b2)

    # invert colors for shiny palette
    color3 = convert_color(31 - r1, 31 - g1, 31 - b1)
    color4 = convert_color(31 - r2, 31 - g2, 31 - b2)
    return list(color1 + color2 + color3 + color4)


def get_gs_colors(pkmn_name: str):
    return [convert_color(*colors) if colors is not None else None for colors in __GS_PALETTES[pkmn_name]]


def shift_color(r: int, g: int, b: int, random):
    return r + random.randint(-1, 1), \
           g + random.randint(-1, 1), \
           b + random.randint(-1, 1)


def convert_color(r: int, g: int, b: int):
    r = max(0, min(r, 31))
    g = max(0, min(g, 31))
    b = max(0, min(b, 31))

    color = (b << 10) | (g << 5) | r
    return color.to_bytes(2, "little")


type_palettes = {
    "NORMAL": [[31, 27, 31], [31, 24, 30]],
    "FIGHTING": [[30, 17, 1], [24, 9, 0]],
    "FLYING": [[17, 21, 31], [15, 11, 28]],
    "POISON": [[27, 21, 31], [15, 10, 24]],
    "GROUND": [[28, 19, 13], [24, 14, 0]],
    "ROCK": [[21, 20, 22], [18, 15, 4]],
    "BUG": [[23, 25, 6], [16, 18, 4]],
    "GHOST": [[10, 8, 14], [5, 3, 15]],
    "STEEL": [[19, 19, 21], [12, 14, 13]],
    "FIRE": [[31, 7, 0], [31, 15, 0]],
    "WATER": [[5, 8, 31], [2, 4, 26]],
    "GRASS": [[8, 31, 5], [4, 24, 2]],
    "ELECTRIC": [[31, 23, 7], [31, 17, 0]],
    "PSYCHIC_TYPE": [[31, 14, 30], [24, 4, 14]],
    "ICE": [[17, 25, 30], [22, 27, 30]],
    "DRAGON": [[16, 20, 25], [9, 12, 23]],
    "DARK": [[4, 2, 7], [3, 2, 6]],
}


# Jynx is a special case in that its colors were swapped in the sprite itself,
# and in its palette data, so it is visually the same between G/S and Crystal,
# so we can just leave it as vanilla
# Spearow had a significant enough redrawing that it looks more faithful to
# swap its primary and secondary colors
# All Shiny colors are the exact same between G/S and Crystal (except Jynx),
# so we have only the main palette
__GS_PALETTES = {
    "IVYSAUR": (None, (31, 12, 17)),
    "VENUSAUR": ((12, 31, 19), (31, 9, 19)),
    "CHARMANDER": ((31, 18, 4), (22, 11, 5)),
    "CHARMELEON": ((31, 14, 5), (23, 9, 10)),
    "CHARIZARD": ((31, 14, 0), (7, 11, 15)),
    "SQUIRTLE": (None, (12, 19, 31)),
    "WARTORTLE": (None, (12, 19, 31)),
    "CATERPIE": (None, (31, 12, 17)),
    "BUTTERFREE": ((15, 28, 31), (25, 10, 19)),
    "WEEDLE": ((29, 26, 5), (26, 7, 0)),
    "KAKUNA": ((31, 27, 4), (20, 12, 7)),
    "BEEDRILL": ((31, 26, 6), None),
    "PIDGEY": ((31, 21, 31), None),
    "PIDGEOTTO": ((31, 15, 23), None),
    "PIDGEOT": ((31, 15, 23), None),
    "RATTATA": ((22, 15, 30), (18, 9, 17)),
    "RATICATE": ((26, 16, 3), (14, 8, 3)),
    "SPEAROW": ((21, 8, 11), (29, 23, 13)),
    "FEAROW": ((22, 17, 7), (31, 11, 0)),
    "EKANS": ((31, 13, 23), (23, 3, 17)),
    "SANDSHREW": ((21, 16, 10), (14, 8, 1)),
    "SANDSLASH": ((23, 14, 4), None),
    "NIDORAN_F": ((19, 21, 31), (7, 16, 6)),
    "NIDORINA": ((16, 21, 31), None),
    "NIDOQUEEN": ((22, 21, 6), (7, 16, 25)),
    "NIDORAN_M": ((27, 17, 22), (21, 2, 8)),
    "NIDORINO": ((26, 17, 22), (21, 2, 8)),
    "NIDOKING": ((24, 10, 19), (13, 3, 15)),
    "CLEFAIRY": ((31, 13, 25), None),
    "CLEFABLE": ((31, 13, 25), None),
    "VULPIX": ((31, 18, 9), (23, 9, 10)),
    "NINETALES": ((31, 25, 9), None),
    "JIGGLYPUFF": ((31, 16, 31), None),
    "WIGGLYTUFF": ((31, 16, 31), None),
    "ZUBAT": ((15, 15, 27), (6, 7, 12)),
    "GOLBAT": ((18, 8, 21), (4, 9, 15)),
    "ODDISH": ((13, 23, 6), (7, 9, 16)),
    "GLOOM": ((31, 14, 7), None),
    "PARAS": (None, (28, 7, 6)),
    "VENONAT": ((31, 9, 5), None),
    "VENOMOTH": (None, (11, 12, 14)),
    "MEOWTH": ((31, 31, 5), (28, 10, 5)),
    "PSYDUCK": ((31, 27, 4), (17, 15, 0)),
    "GOLDUCK": ((27, 23, 4), (12, 9, 24)),
    "PRIMEAPE": ((31, 15, 6), (14, 9, 4)),
    "GROWLITHE": ((31, 23, 7), (31, 9, 4)),
    "ARCANINE": (None, (31, 9, 4)),
    "POLIWAG": ((26, 8, 17), (8, 5, 15)),
    "POLIWHIRL": ((16, 16, 26), (8, 5, 15)),
    "POLIWRATH": (None, (8, 5, 15)),
    "VICTREEBEL": (None, (31, 9, 19)),
    "GRAVELER": ((18, 17, 15), None),
    "GOLEM": ((18, 17, 15), None),
    "PONYTA": ((31, 19, 0), (31, 11, 3)),
    "RAPIDASH": ((30, 28, 0), (31, 11, 3)),
    "SLOWPOKE": ((31, 10, 31), (28, 6, 14)),
    "SLOWBRO": ((31, 10, 31), (14, 19, 12)),
    "MAGNEMITE": ((11, 20, 31), None),
    "MAGNETON": ((11, 20, 31), None),
    "DODUO": ((20, 16, 8), (9, 8, 6)),
    "SEEL": (None, (29, 11, 18)),
    "SHELLDER": ((18, 17, 20), (21, 11, 14)),
    "CLOYSTER": ((19, 10, 25), (9, 4, 13)),
    "GASTLY": ((30, 13, 30), None),
    "GENGAR": ((31, 8, 2), (17, 0, 19)),
    "ONIX": ((23, 18, 17), None),
    "HYPNO": ((30, 20, 7), (19, 12, 11)),
    "VOLTORB": ((25, 23, 17), (31, 9, 8)),
    "ELECTRODE": ((25, 23, 17), (31, 9, 8)),
    "EXEGGCUTE": ((31, 15, 26), (19, 12, 9)),
    "EXEGGUTOR": ((26, 16, 6), None),
    "CUBONE": ((22, 16, 11), (14, 8, 4)),
    "MAROWAK": ((22, 16, 11), (14, 8, 4)),
    "WEEZING": (None, (18, 6, 18)),
    "CHANSEY": ((27, 19, 23), (31, 8, 21)),
    "TANGELA": ((1, 31, 24), None),
    "KANGASKHAN": ((20, 19, 7), (13, 13, 0)),
    "SEADRA": ((28, 20, 12), (11, 9, 31)),
    "MAGMAR": (None, (23, 9, 10)),
    "PINSIR": ((18, 21, 18), (16, 11, 7)),
    "TAUROS": ((31, 24, 5), (19, 14, 9)),
    "GYARADOS": ((27, 20, 7), (7, 11, 26)),
    "EEVEE": ((24, 16, 11), (17, 10, 8)),
    "PORYGON": (None, (12, 11, 25)),
    "OMANYTE": ((23, 20, 10), (9, 11, 23)),
    "OMASTAR": ((27, 22, 11), (9, 11, 23)),
    "KABUTO": ((23, 15, 11), (14, 11, 8)),
    "KABUTOPS": ((23, 15, 11), (14, 11, 8)),
    "AERODACTYL": ((21, 15, 18), (13, 11, 8)),
    "SNORLAX": (None, (21, 7, 14)),
    "DRATINI": (None, (5, 11, 24)),
    "DRAGONAIR": ((14, 19, 31), (5, 11, 31)),
    "DRAGONITE": ((21, 18, 6), None),
    "MEWTWO": (None, (17, 8, 15)),
    "CHIKORITA": ((29, 23, 12), None),
    "BAYLEEF": ((27, 20, 13), None),
    "MEGANIUM": (None, (28, 12, 5)),
    "TYPHLOSION": ((31, 20, 4), (31, 9, 6)),
    "TOTODILE": ((10, 19, 26), None),
    "CROCONAW": ((10, 21, 18), (24, 9, 10)),
    "FERALIGATR": ((8, 17, 13), (18, 7, 1)),
    "LEDYBA": ((31, 14, 4), None),
    "LEDIAN": ((31, 14, 4), None),
    "SPINARAK": ((19, 8, 20), (8, 9, 17)),
    "CHINCHOU": (None, (7, 7, 20)),
    "LANTURN": (None, (8, 13, 22)),
    "IGGLYBUFF": ((31, 16, 31), (31, 9, 23)),
    "TOGETIC": ((31, 24, 8), None),
    "BELLOSSOM": ((28, 11, 26), (15, 23, 6)),
    "AZUMARILL": (None, (18, 9, 7)),
    "HOPPIP": (None, (21, 8, 3)),
    "JUMPLUFF": ((18, 18, 29), (7, 11, 25)),
    "AIPOM": ((27, 18, 4), (8, 3, 15)),
    "SUNKERN": ((23, 28, 1), (14, 18, 0)),
    "WOOPER": (None, (10, 8, 14)),
    "QUAGSIRE": ((15, 21, 26), (17, 8, 20)),
    "ESPEON": ((17, 15, 25), (14, 4, 17)),
    "UMBREON": ((17, 15, 0), None),
    "MURKROW": ((23, 19, 3), (10, 11, 20)),
    "SLOWKING": ((31, 10, 31), (30, 5, 6)),
    "UNOWN": ((11, 31, 15), (0, 15, 8)),
    "WOBBUFFET": ((12, 25, 24), (9, 16, 12)),
    "GIRAFARIG": (None, (17, 12, 5)),
    "PINECO": ((21, 15, 10), (7, 7, 14)),
    "FORRETRESS": ((17, 13, 14), (19, 6, 9)),
    "DUNSPARCE": (None, (9, 7, 16)),
    "GRANBULL": ((28, 16, 22), (17, 9, 11)),
    "QWILFISH": ((18, 24, 4), None),
    "SHUCKLE": (None, (18, 9, 6)),
    "HERACROSS": ((16, 13, 19), (3, 11, 15)),
    "SNEASEL": ((17, 24, 22), (14, 9, 1)),
    "URSARING": (None, (24, 14, 0)),
    "SLUGMA": ((26, 13, 2), (18, 6, 2)),
    "MAGCARGO": ((26, 10, 16), (15, 6, 6)),
    "SWINUB": ((24, 13, 13), None),
    "PILOSWINE": ((23, 18, 14), (10, 10, 10)),
    "REMORAID": ((13, 10, 25), (5, 3, 31)),
    "MANTINE": ((20, 16, 18), (3, 6, 19)),
    "SKARMORY": ((17, 18, 24), (4, 7, 10)),
    "HOUNDOUR": (None, (31, 6, 9)),
    "HOUNDOOM": (None, (31, 6, 9)),
    "KINGDRA": ((31, 10, 11), (5, 11, 31)),
    "PHANPY": (None, (23, 13, 9)),
    "HITMONTOP": ((26, 15, 18), None),
    "SMOOCHUM": ((31, 15, 4), None),
    "MAGBY": (None, (23, 9, 10)),
    "RAIKOU": (None, (30, 11, 1)),
    "ENTEI": ((31, 11, 1), (17, 4, 0)),
    "PUPITAR": ((12, 11, 28), None)
}

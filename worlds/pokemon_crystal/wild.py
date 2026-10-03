import random
from collections import defaultdict
from dataclasses import replace
from typing import TYPE_CHECKING

from .data import EncounterMon, LogicalAccess, EncounterKey, EncounterType, GrassTimeOfDay, FishTimeOfDay, data as crystal_data
from .options import RandomizeWilds, EncounterGrouping, RandomizePokemonRequests, \
    RandomizeTrades, EncounterSlotDistribution, Goal, WildEncounterMethodsRequired, WildMatchMode, \
    UniqueStaticPokemon, BreedingMethodsRequired
from .evolution import evolution_in_logic
from .pokemon import get_random_pokemon, get_priority_dexsanity
from .pokemon_data import LEGENDARY_STATIC_SLOTS, ODD_EGG_SPECIES, UNIQUE_STATIC_SLOTS


def _build_egg_producers(generated_pokemon) -> dict[str, list[str]]:
    out: dict[str, list[str]] = defaultdict(list)
    for name, pdata in generated_pokemon.items():
        if pdata.produces_egg:
            out[pdata.produces_egg].append(name)
    return out


def _expand_unique_block(species: str,
                         in_logic_preevos: dict[str, list[str]],
                         egg_producers: dict[str, list[str]]) -> set[str]:
    block = {species}
    frontier = {species}
    while frontier:
        new_frontier: set[str] = set()
        for sp in frontier:
            for pre in in_logic_preevos.get(sp, ()):
                if pre not in block:
                    block.add(pre)
                    new_frontier.add(pre)
            for producer in egg_producers.get(sp, ()):
                if producer not in block:
                    block.add(producer)
                    new_frontier.add(producer)
        frontier = new_frontier
    return block


def _build_in_logic_preevos(world) -> dict[str, list[str]]:
    """Inverse evolution map restricted to evolutions whose method is logically required."""
    out: dict[str, list[str]] = defaultdict(list)
    for pre_name, pre_data in world.generated_pokemon.items():
        for evo in pre_data.evolutions:
            if evolution_in_logic(world, evo):
                out[evo.pokemon].append(pre_name)
    return out

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def filter_time_of_day(world: "PokemonCrystalWorld"):
    if not world.options.time_of_day_encounters:
        def keep(key: EncounterKey) -> bool:
            if key.encounter_type is EncounterType.Grass:
                return key.time_of_day == GrassTimeOfDay.Day
            if key.encounter_type is EncounterType.Fish and key.time_of_day is not None:
                return key.time_of_day is FishTimeOfDay.Day
            return True

        world.generated_wild = {
            EncounterKey(key.encounter_type, key.region_id,
                         fishing_rod=key.fishing_rod, rarity=key.rarity): encounters
            for key, encounters in world.generated_wild.items()
            if keep(key)
        }


def _get_wild_match_params(world: "PokemonCrystalWorld", vanilla_pokemon: str):
    """Get match_bst and types params based on WildMatchMode option."""
    match_types = None
    match_bst = None
    if world.options.wild_match_mode.matches_types:
        match_types = crystal_data.pokemon[vanilla_pokemon].types
    if world.options.wild_match_mode.matches_base_stats:
        match_bst = crystal_data.pokemon[vanilla_pokemon].bst
    return match_types, match_bst


def randomize_wild_pokemon(world: "PokemonCrystalWorld"):
    shared = world.options.shared_wild_encounters and world.options.wild_match_mode == WildMatchMode.option_none
    rng = random.Random(world.shared_wild_seed) if shared else world.random

    if world.options.randomize_wilds and not world.is_universal_tracker:

        exclude_unown = Goal.UNOWN_HUNT in world.options.goal
        global_blocklist = world.options.wild_encounter_blocklist.get_ids(world)
        global_blocklist = global_blocklist | world.unique_static_wild_block

        world.generated_wooper = get_random_pokemon(world, exclude_unown=True, rng=rng)

        def get_random_wild(vanilla_pokemon: str, encounter_blocklist: set[str] | None = None) -> str:
            match_types, match_bst = _get_wild_match_params(world, vanilla_pokemon)
            blocklist = (encounter_blocklist | global_blocklist) if encounter_blocklist else global_blocklist
            return get_random_pokemon(world, blocklist=blocklist or None,
                                      exclude_unown=exclude_unown,
                                      types=match_types, match_bst=match_bst, rng=rng)

        def randomize_encounter_list(encounter_list: list[EncounterMon]) -> list[EncounterMon]:
            new_encounters = list[EncounterMon]()

            if world.options.encounter_grouping.value == EncounterGrouping.option_one_per_method:
                pokemon = get_random_wild(encounter_list[0].pokemon)
                for encounter in encounter_list:
                    new_encounters.append(replace(encounter, pokemon=pokemon))

            elif world.options.encounter_grouping.value == EncounterGrouping.option_one_to_one:
                distribution = defaultdict[str, list[int]](list)
                new_encounters = [encounter for encounter in encounter_list]
                encounter_blocklist = set()
                for i, encounter in enumerate(encounter_list):
                    distribution[encounter.pokemon].append(i)
                for vanilla_pokemon, slots in distribution.items():
                    pokemon = get_random_wild(vanilla_pokemon, encounter_blocklist)
                    encounter_blocklist.add(pokemon)
                    for slot in slots:
                        new_encounters[slot] = replace(new_encounters[slot], pokemon=pokemon)
            else:
                encounter_blocklist = set()
                for encounter in encounter_list:
                    pokemon = get_random_wild(encounter.pokemon, encounter_blocklist)
                    encounter_blocklist.add(pokemon)
                    new_encounters.append(replace(encounter, pokemon=pokemon))

            return new_encounters

        for region_key in world.generated_wild:
            encounters = world.generated_wild[region_key]
            world.generated_wild[region_key] = randomize_encounter_list(encounters)

        for i, slot in enumerate(world.generated_contest):
            pokemon = get_random_pokemon(world, exclude_unown=True,
                                         blocklist=global_blocklist or None, rng=rng) \
                if world.options.randomize_wilds else slot.pokemon
            world.generated_contest[i] = replace(
                slot,
                pokemon=pokemon,
                percentage=10 if world.options.encounter_slot_distribution == EncounterSlotDistribution.option_equal
                else slot.percentage)
    else:
        for region_key, wilds in world.generated_wild.items():
            if not world.is_universal_tracker and Goal.UNOWN_HUNT in world.options.goal and any(
                    wild.pokemon == "UNOWN" for wild in wilds):
                wilds = [replace(wild, pokemon="RATTATA") for wild in wilds]
                world.generated_wild[region_key] = wilds

    # Two-stage ensure_placed:
    # 1. "Should place" (best-effort) — guarantee modes like base_forms/evo_lines/catch_em_all, dexsanity priority
    # 2. "Must place" (required) — MAGIKARP, DITTO, trade requests — these are logic requirements
    # Should-place runs first so must-place can freely overwrite them if needed.

    should_place = list[str]()
    must_place = list[str]()

    if not world.is_universal_tracker:
        if world.options.randomize_wilds:
            if world.options.randomize_wilds.value == RandomizeWilds.option_base_forms:
                should_place.extend(
                    pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items()
                    if pokemon_data.is_base)
            elif world.options.randomize_wilds.value == RandomizeWilds.option_evolution_lines:
                for pokemon_id, pokemon_data in world.generated_pokemon.items():
                    if pokemon_data.is_base:
                        line = [pokemon_id]
                        for evo in pokemon_data.evolutions:
                            line.append(evo.pokemon)
                            for evo2 in world.generated_pokemon[evo.pokemon].evolutions:
                                line.append(evo2.pokemon)
                        should_place.append(rng.choice(line))
            elif world.options.randomize_wilds.value == RandomizeWilds.option_catch_em_all:
                should_place.extend(world.generated_pokemon.keys())

            should_place.extend(get_priority_dexsanity(world))

        if world.options.randomize_pokemon_requests:
            must_place.append("MAGIKARP")

        if world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items:
            must_place.extend(world.generated_request_pokemon)

        if world.options.breeding_methods_required:
            must_place.append("DITTO")

        if (world.options.trades_required or world.options.randomize_lucky_number_show) \
                and world.options.randomize_trades.value in (RandomizeTrades.option_received,
                                                             RandomizeTrades.option_vanilla):
            must_place.extend(trade.requested_pokemon for trade in world.generated_trades.values())

        # Unique Static Pokemon overrides best-effort wild guarantees (catch_em_all, base_forms,
        # evolution_lines, dexsanity priority): never force a blocked species back into wilds.
        if world.unique_static_wild_block:
            should_place = [pokemon for pokemon in should_place
                            if pokemon not in world.unique_static_wild_block]

        must_place_set = set(must_place)

        for stage, pokemon_list in [("should", should_place), ("must", must_place)]:
            logically_available = get_logically_available_wilds(world)
            remaining_to_place = set(pokemon_list) - logically_available

            for place_pokemon in pokemon_list:
                if place_pokemon not in remaining_to_place:
                    continue

                wilds = [(key, wilds) for key, wilds in world.generated_wild.items() if
                         world.logic.wild_regions[key] is LogicalAccess.InLogic and key.region_id is not None]

                wilds.sort(key=lambda x: x[0].region_id)
                rng.shuffle(wilds)

                seen_pokemon = set()
                to_replace = None
                encounter_key = None
                encounters = None

                # Protect all must-place pokemon from being overwritten, whether already placed or not.
                # For should-place, also protect must-place pokemon.
                # For must-place, protect the full must set (minus the current one) so placed ones aren't lost.
                protected = remaining_to_place - {place_pokemon} | (must_place_set - {place_pokemon})

                while (not to_replace or (to_replace in protected)) and (to_replace not in seen_pokemon):
                    if to_replace:
                        seen_pokemon.add(to_replace)
                    if not wilds:
                        break
                    encounter_key, encounters = wilds.pop()
                    to_replace = rng.choice(encounters).pokemon

                if encounter_key is None:
                    if stage == "must":
                        raise RuntimeError(f"{place_pokemon} could not be placed anywhere. Aborting.")
                    continue

                encounters = [
                    replace(encounter,
                            pokemon=place_pokemon if encounter.pokemon == to_replace else encounter.pokemon)
                    for encounter in encounters]

                world.generated_wild[encounter_key] = encounters
                remaining_to_place.discard(place_pokemon)
                remaining_to_place -= get_logically_available_wilds(world)


def randomize_static_pokemon(world: "PokemonCrystalWorld"):
    world.unique_static_wild_block = set()
    if not world.is_universal_tracker:
        if world.options.randomize_static_pokemon:
            logically_available_wilds = get_logically_available_wilds(world)
            priority_pokemon = get_priority_dexsanity(world) - logically_available_wilds
            blocklist = world.options.static_blocklist.get_ids(world)

            unique_mode = world.options.unique_static_pokemon.value
            breeding_in_logic = (
                world.options.breeding_methods_required.value != BreedingMethodsRequired.option_none
            )
            in_logic_preevos = _build_in_logic_preevos(world)
            egg_producers = _build_egg_producers(world.generated_pokemon) if breeding_in_logic else {}
            used_species: set[str] = set()

            for static_name, pkmn_data in world.generated_static.items():
                vanilla = pkmn_data.pokemon
                tracked = world.logic.wild_regions[static_name] is LogicalAccess.InLogic and (
                    unique_mode == UniqueStaticPokemon.option_all
                    or (unique_mode == UniqueStaticPokemon.option_legendaries_only
                        and vanilla in LEGENDARY_STATIC_SLOTS)
                    or (unique_mode == UniqueStaticPokemon.option_legendaries_and_uniques
                        and vanilla in UNIQUE_STATIC_SLOTS)
                )

                match_types = None
                if world.options.randomize_static_pokemon.matches_types:
                    match_types = crystal_data.pokemon[vanilla].types

                match_bst = None
                if world.options.randomize_static_pokemon.matches_base_stats:
                    match_bst = crystal_data.pokemon[vanilla].bst

                slot_blocklist = blocklist | used_species if tracked else blocklist

                pokemon = get_random_pokemon(
                    world=world,
                    exclude_unown=True,
                    base_only=pkmn_data.level_type == "giveegg",
                    priority_pokemon=priority_pokemon,
                    blocklist=slot_blocklist,
                    types=match_types,
                    match_bst=match_bst,
                )
                world.generated_static[static_name] = replace(
                    world.generated_static[static_name],
                    pokemon=pokemon,
                )
                priority_pokemon.discard(pokemon)

                if tracked:
                    used_species.add(pokemon)
                    world.unique_static_wild_block |= _expand_unique_block(
                        pokemon, in_logic_preevos, egg_producers)

        else:  # Still randomize the Odd Egg
            pokemon = world.random.choice(ODD_EGG_SPECIES)
            encounter_key = EncounterKey.static("OddEgg")
            world.generated_static[encounter_key] = replace(world.generated_static[encounter_key], pokemon=pokemon)


def get_logically_available_wilds(world: "PokemonCrystalWorld") -> set[str]:
    logical_pokemon = set[str]()

    for region_key, wilds in world.generated_wild.items():
        access = world.logic.wild_regions[region_key]
        if access is LogicalAccess.InLogic:
            logical_pokemon.update(wild.pokemon for wild in wilds)

    if WildEncounterMethodsRequired.BUG_CATCHING_CONTEST in world.options.wild_encounter_methods_required:
        logical_pokemon.update(slot.pokemon for slot in world.generated_contest)

    if Goal.UNOWN_HUNT in world.options.goal:
        logical_pokemon.add("UNOWN")

    return logical_pokemon

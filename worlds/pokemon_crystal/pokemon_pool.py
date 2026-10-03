from typing import TYPE_CHECKING

from .data import data as crystal_data, LogicalAccess, EncounterType
from .options import Goal, PokemonSourceLogic, WildEncounterMethodsRequired

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


ENCOUNTER_TYPE_TO_SOURCE_KEY = {
    EncounterType.Grass: PokemonSourceLogic.LAND,
    EncounterType.Water: PokemonSourceLogic.SURFING,
    EncounterType.Fish: PokemonSourceLogic.FISHING,
    EncounterType.Tree: PokemonSourceLogic.HEADBUTT,
    EncounterType.RockSmash: PokemonSourceLogic.ROCK_SMASH,
    EncounterType.Swarm: PokemonSourceLogic.SWARM,
}


class PokemonPool:
    """Lazy, cached views of the logically available Pokemon for various functions.

    A single invalidate() call clears all caches. Evolution and breeding relationship
    data continues to live on PokemonCrystalLogic; this class reads it but does not own it.
    """

    def __init__(self, world: "PokemonCrystalWorld"):
        self._world = world
        self._base_pool: set[str] | None = None
        self._all_available: set[str] | None = None
        self._filtered_cache: dict[tuple, set[str]] = {}
        self._completable_trades: set[str] = set()
        self.trade_requests_assigned = False

    def invalidate(self) -> None:
        """Clear every cached pool."""
        self._base_pool = None
        self._all_available = None
        self._filtered_cache.clear()

    def ensure_base_pools(self) -> None:
        """Compute wilds + statics + trades + evolution/breeding fixed-point.

        Populates `world.logic.evolution` and `world.logic.breeding` as a side
        effect. Received trade species must be randomized before this is called;
        requested species are randomized later and consume get_filtered().

        A trade only joins the pool once the species it asks for is in the pool, so trades
        can't bootstrap each other into it.
        """
        if self._base_pool is not None:
            return

        pool = set[str]()
        pool.update(self._compute_wilds())
        pool.update(self._compute_statics())

        self._completable_trades = set[str]()
        previous_size = -1
        while previous_size != len(pool):
            previous_size = len(pool)
            pool.update(self._compute_evolutions(pool))
            pool.update(self._compute_breeding(pool))
            pool.update(self._admit_trades(pool))

        self._base_pool = pool

    @property
    def all_available(self) -> set[str]:
        """Full set of logically available Pokemon (replaces logic.available_pokemon).

        Includes wilds, statics, trades, evolutions, and breeding.
        """
        if self._all_available is None:
            self.ensure_base_pools()
            self._all_available = set(self._base_pool)
        return self._all_available

    @property
    def diploma_count(self) -> int:
        """Diploma-requirement count. UT-aware."""
        world = self._world
        if world.is_universal_tracker:
            return world.ut_slot_data["diploma_count"]
        return len(self.all_available)

    @property
    def dexcountsanity_total(self) -> int:
        """Total Pokemon count for dexcountsanity. UT-aware."""
        world = self._world
        if world.is_universal_tracker:
            return world.ut_slot_data["logically_available_pokemon_count"]
        return len(self.get_filtered(world.options.dexsanity_logic))

    def get_filtered(self, source_logic: PokemonSourceLogic, exclude_unown: bool = False) -> set[str]:
        """Pokemon available under a source-logic filter.

        Falls back to the pool for all of the option's valid source keys if empty,
        matching the effective_sources fallback.
        """
        key = (frozenset(source_logic.value), exclude_unown)
        if key not in self._filtered_cache:
            self._filtered_cache[key] = self._compute_filtered(source_logic, exclude_unown)
        return self._filtered_cache[key]

    def effective_sources(self, source_logic: PokemonSourceLogic,
                          required_species: "set[str] | None" = None,
                          exclude_unown: bool = False,
                          without_trades: bool = False) -> frozenset[str]:
        """Source set that matches the pool returned by get_filtered.

        Falls back to all valid source keys when the configured filter is empty
        or any required species isn't in the filtered pool. Rule sites should
        use this so gating matches the pool used to pick species; pass the same
        `exclude_unown` as the corresponding get_filtered call, or the emptiness
        check can disagree (e.g. a request pool of only UNOWN). `without_trades` judges
        emptiness as if no trade were complete.
        """
        raw = self._compute_filtered(source_logic, exclude_unown=exclude_unown, allow_fallback=False,
                                     without_trades=without_trades)
        if not raw:
            return frozenset(source_logic.valid_keys)
        if required_species and not required_species.issubset(raw):
            return frozenset(source_logic.valid_keys)
        return frozenset(source_logic.value)

    def _compute_filtered(self, source_logic: PokemonSourceLogic, exclude_unown: bool,
                          allow_fallback: bool = True, without_trades: bool = False) -> set[str]:
        self.ensure_base_pools()
        world = self._world
        pool = set[str]()

        for region_key, wilds in world.generated_wild.items():
            if world.logic.wild_regions[region_key] is not LogicalAccess.InLogic:
                continue
            key = ENCOUNTER_TYPE_TO_SOURCE_KEY.get(region_key.encounter_type)
            if key and key in source_logic:
                pool.update(wild.pokemon for wild in wilds)

        if (PokemonSourceLogic.BUG_CATCHING_CONTEST in source_logic
                and WildEncounterMethodsRequired.BUG_CATCHING_CONTEST in world.options.wild_encounter_methods_required):
            pool.update(slot.pokemon for slot in world.generated_contest)

        if PokemonSourceLogic.STATICS in source_logic:
            for region_key, static in world.generated_static.items():
                if world.logic.wild_regions[region_key] is LogicalAccess.InLogic:
                    pool.add(static.pokemon)
            if Goal.UNOWN_HUNT in world.options.goal:
                pool.add("UNOWN")

        if PokemonSourceLogic.TRADES in source_logic and not without_trades:
            pool.update(world.generated_trades[trade_id].received_pokemon
                        for trade_id in self._completable_trades)

        include_evolution = PokemonSourceLogic.EVOLUTION in source_logic
        include_breeding = PokemonSourceLogic.BREEDING in source_logic
        if include_evolution or include_breeding:
            previous_size = -1
            while previous_size != len(pool):
                previous_size = len(pool)
                if include_evolution:
                    for pokemon in list(pool):
                        for evo, access in world.logic.evolution.get(pokemon, []):
                            if access is LogicalAccess.InLogic:
                                pool.add(evo.pokemon)
                if include_breeding:
                    for child, parents in world.logic.breeding.items():
                        for parent, access, _ in parents:
                            if access is LogicalAccess.InLogic and parent in pool:
                                pool.add(child)

        if exclude_unown:
            pool.discard("UNOWN")
        if not pool and allow_fallback:
            all_sources = type(source_logic)(["_All"])
            pool = self._compute_filtered(all_sources, exclude_unown, allow_fallback=False,
                                          without_trades=without_trades)
        return pool

    def _compute_wilds(self) -> set[str]:
        from .wild import get_logically_available_wilds
        return get_logically_available_wilds(self._world)

    def _compute_statics(self) -> set[str]:
        world = self._world
        return {static.pokemon for region_key, static in world.generated_static.items()
                if world.logic.wild_regions[region_key] is LogicalAccess.InLogic}

    def _compute_evolutions(self, available: set[str]) -> set[str]:
        from .evolution import evolution_in_logic
        world = self._world
        evolution_pokemon = set[str]()
        for evolver in world.logic.evolution.keys():
            world.logic.evolution[evolver] = []
        for evolving_pokemon in available:
            for evo in world.generated_pokemon[evolving_pokemon].evolutions:
                logical_access = (LogicalAccess.InLogic if evolution_in_logic(world, evo)
                                  else LogicalAccess.OutOfLogic)
                if not world.is_universal_tracker and logical_access is LogicalAccess.OutOfLogic:
                    continue
                world.logic.evolution[evolving_pokemon].append((evo, logical_access))
                if logical_access is LogicalAccess.InLogic:
                    evolution_pokemon.add(evo.pokemon)
        return evolution_pokemon

    def _compute_breeding(self, available: set[str]) -> set[str]:
        from .breeding import can_breed, breeding_requires_ditto
        world = self._world
        if not world.options.breeding_methods_required and not world.is_universal_tracker:
            return set()
        logical_access = (LogicalAccess.InLogic if world.options.breeding_methods_required
                          else LogicalAccess.OutOfLogic)
        breeding_pokemon = set[str]()
        for child in world.logic.breeding.keys():
            world.logic.breeding[child] = []
        for pokemon_id, data in world.generated_pokemon.items():
            if pokemon_id not in available:
                continue
            if not can_breed(world, pokemon_id):
                continue
            requires_ditto = breeding_requires_ditto(world, pokemon_id)
            world.logic.breeding[data.produces_egg].append((pokemon_id, logical_access, requires_ditto))
            if logical_access is LogicalAccess.InLogic:
                breeding_pokemon.add(data.produces_egg)
            if data.produces_egg == "NIDORAN_F":
                world.logic.breeding["NIDORAN_M"].append(
                    (pokemon_id, logical_access, breeding_requires_ditto(world, "NIDORAN_M")))
                if logical_access is LogicalAccess.InLogic:
                    breeding_pokemon.add("NIDORAN_M")
        return breeding_pokemon

    def _admit_trades(self, pool: set[str]) -> set[str]:
        """Received species of not-yet-admitted trades whose requested species is now in `pool`.

        Until the requests are assigned they're vanilla placeholders, so every trade is admitted:
        this pool builds the evolution/breeding locations, and must stay a superset of the final one.
        """
        from .utils import should_include_region
        world = self._world
        received = set[str]()
        if not world.options.trades_required:
            return received
        for region_data in crystal_data.regions.values():
            if not should_include_region(region_data, world):
                continue
            for trade_id in region_data.trades:
                if trade_id in self._completable_trades:
                    continue
                trade = world.generated_trades[trade_id]
                if self.trade_requests_assigned and trade.requested_pokemon not in pool:
                    continue
                self._completable_trades.add(trade_id)
                received.add(trade.received_pokemon)
        return received

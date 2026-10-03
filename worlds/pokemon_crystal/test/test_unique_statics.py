from collections import Counter

from .bases import PokemonCrystalTestBase
from ..data import LogicalAccess, data as crystal_data
from ..wild import LEGENDARY_STATIC_SLOTS, UNIQUE_STATIC_SLOTS


def _wild_species(world) -> set[str]:
    out: set[str] = set()
    for encounters in world.generated_wild.values():
        for enc in encounters:
            out.add(enc.pokemon)
    for slot in world.generated_contest:
        out.add(slot.pokemon)
    return out


def _in_logic_static(world) -> dict:
    return {key: slot for key, slot in world.generated_static.items()
            if world.logic.wild_regions[key] is LogicalAccess.InLogic}


def _trade_received(world) -> set[str]:
    return {t.received_pokemon for t in world.generated_trades.values()}


def _vanilla_static_species() -> dict[str, str]:
    return {key.region_id: slot.pokemon for key, slot in crystal_data.static.items()}


COMMON_OPTS = {
    "randomize_wilds": "completely_random",
    "randomize_static_pokemon": "completely_random",
    "randomize_trades": "both",
    "wild_encounter_methods_required": ["Grass", "Surf", "Rock Smash", "Fishing", "Headbutt", "Bug Catching Contest"],
}


class UniqueStaticsDisabledTest(PokemonCrystalTestBase):
    options = {**COMMON_OPTS, "unique_static_pokemon": "disabled"}

    def test_block_set_empty(self):
        block = getattr(self.world, "unique_static_wild_block", None)
        self.assertEqual(block, set(), "block set must be empty when option is disabled")


class UniqueStaticsAllTest(PokemonCrystalTestBase):
    options = {
        **COMMON_OPTS,
        "unique_static_pokemon": "all",
        "evolution_methods_required": [],
        "breeding_methods_required": "none",
    }

    def test_no_duplicate_static_species(self):
        species = [slot.pokemon for slot in _in_logic_static(self.world).values()]
        dupes = [s for s, c in Counter(species).items() if c > 1]
        self.assertEqual(dupes, [], f"static slots contain duplicate species: {dupes}")

    def test_static_species_absent_from_wilds(self):
        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        statics = {slot.pokemon for slot in _in_logic_static(self.world).values()}
        collisions = statics & wild
        # DITTO may be force-placed in wilds for breeding logic; tolerate that one case.
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"static species also appeared in wilds: {sorted(collisions)}")

    def test_static_species_absent_from_trade_received(self):
        self.assertTrue(self.world.generated_trades, "no trades generated; test would pass vacuously")
        statics = {slot.pokemon for slot in _in_logic_static(self.world).values()}
        collisions = statics & _trade_received(self.world)
        self.assertEqual(collisions, set(),
                         f"static species also appeared in trade rewards: {sorted(collisions)}")


class UniqueStaticsCatchEmAllTest(PokemonCrystalTestBase):
    """Catch 'em All tries to place every species in wilds; Unique Static must override it."""
    options = {
        **COMMON_OPTS,
        "randomize_wilds": "catch_em_all",
        "unique_static_pokemon": "all",
        "evolution_methods_required": [],
        "breeding_methods_required": "none",
    }

    def test_static_species_absent_from_wilds(self):
        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        statics = {slot.pokemon for slot in _in_logic_static(self.world).values()}
        collisions = statics & wild
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"static species force-placed into wilds by catch_em_all: {sorted(collisions)}")


class UniqueStaticsLegendariesOnlyTest(PokemonCrystalTestBase):
    options = {
        **COMMON_OPTS,
        "unique_static_pokemon": "legendaries_only",
        "evolution_methods_required": [],
        "breeding_methods_required": "none",
    }

    def test_block_only_from_legendary_slots(self):
        vanilla = _vanilla_static_species()
        legendary_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                           if vanilla.get(key.region_id) in LEGENDARY_STATIC_SLOTS}
        block = self.world.unique_static_wild_block
        # With evolution/breeding off, the block should equal exactly the legendary picks.
        self.assertEqual(block, legendary_picks,
                         f"block {sorted(block)} differs from legendary picks {sorted(legendary_picks)}")

    def test_legendary_picks_absent_from_wilds(self):
        vanilla = _vanilla_static_species()
        legendary_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                           if vanilla.get(key.region_id) in LEGENDARY_STATIC_SLOTS}
        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        collisions = legendary_picks & wild
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"legendary slot picks appeared in wilds: {sorted(collisions)}")

    def test_non_legendary_static_picks_not_blocked(self):
        """Non-legendary static picks should not be added to the unique block set."""
        vanilla = _vanilla_static_species()
        non_legendary_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                               if vanilla.get(key.region_id) not in LEGENDARY_STATIC_SLOTS}
        legendary_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                           if vanilla.get(key.region_id) in LEGENDARY_STATIC_SLOTS}
        block = self.world.unique_static_wild_block
        # Non-legendary picks may overlap legendary picks by coincidence — only test the difference.
        unexpectedly_blocked = (non_legendary_picks - legendary_picks) & block
        self.assertEqual(unexpectedly_blocked, set(),
                         f"non-legendary static species were blocked: {sorted(unexpectedly_blocked)}")


class UniqueStaticsLegendariesAndUniquesTest(PokemonCrystalTestBase):
    options = {
        **COMMON_OPTS,
        "unique_static_pokemon": "legendaries_and_uniques",
        "evolution_methods_required": [],
        "breeding_methods_required": "none",
    }

    def test_block_only_from_unique_slots(self):
        vanilla = _vanilla_static_species()
        unique_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                        if vanilla.get(key.region_id) in UNIQUE_STATIC_SLOTS}
        block = self.world.unique_static_wild_block
        self.assertEqual(block, unique_picks,
                         f"block {sorted(block)} differs from unique slot picks {sorted(unique_picks)}")

    def test_unique_picks_absent_from_wilds(self):
        vanilla = _vanilla_static_species()
        unique_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                        if vanilla.get(key.region_id) in UNIQUE_STATIC_SLOTS}
        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        collisions = unique_picks & wild
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"unique slot picks appeared in wilds: {sorted(collisions)}")

    def test_other_static_picks_not_blocked(self):
        vanilla = _vanilla_static_species()
        unique_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                        if vanilla.get(key.region_id) in UNIQUE_STATIC_SLOTS}
        other_picks = {slot.pokemon for key, slot in _in_logic_static(self.world).items()
                       if vanilla.get(key.region_id) not in UNIQUE_STATIC_SLOTS}
        block = self.world.unique_static_wild_block
        unexpectedly_blocked = (other_picks - unique_picks) & block
        self.assertEqual(unexpectedly_blocked, set(),
                         f"non-unique static species were blocked: {sorted(unexpectedly_blocked)}")


class UniqueStaticsEvolutionInLogicTest(PokemonCrystalTestBase):
    options = {
        **COMMON_OPTS,
        "unique_static_pokemon": "all",
        "evolution_methods_required": ["Level", "Use Item", "Happiness", "Level and Stat"],
        "breeding_methods_required": "none",
    }

    def test_preevolutions_of_statics_absent_from_wilds(self):
        from collections import defaultdict
        from ..evolution import evolution_in_logic as _eil

        statics = {slot.pokemon for slot in _in_logic_static(self.world).values()}

        # Only edges whose evolution method is in logic should produce blocks.
        in_logic_preevos: dict[str, list[str]] = defaultdict(list)
        for pre_name, pre_data in self.world.generated_pokemon.items():
            for evo in pre_data.evolutions:
                if _eil(self.world, evo):
                    in_logic_preevos[evo.pokemon].append(pre_name)

        expected_preevos: set[str] = set()
        for s in statics:
            frontier = {s}
            while frontier:
                nxt: set[str] = set()
                for sp in frontier:
                    for pre in in_logic_preevos.get(sp, ()):
                        if pre not in expected_preevos and pre not in statics:
                            expected_preevos.add(pre)
                            nxt.add(pre)
                frontier = nxt

        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        collisions = expected_preevos & wild
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"pre-evolutions of static species appeared in wilds: {sorted(collisions)}")


class UniqueStaticsCombinedEvolutionAndBreedingTest(PokemonCrystalTestBase):
    """Closure must walk both pre-evolutions and inverse produces_egg edges together."""
    options = {
        **COMMON_OPTS,
        "unique_static_pokemon": "all",
        "evolution_methods_required": ["Level", "Use Item", "Happiness", "Level and Stat"],
        "breeding_methods_required": "any",
        "randomize_breeding": "completely_random",
        "randomize_evolution": "increase_bst",
    }

    def test_combined_closure_absent_from_wilds(self):
        from collections import defaultdict
        from ..evolution import evolution_in_logic as _eil

        statics = {slot.pokemon for slot in _in_logic_static(self.world).values()}

        in_logic_preevos: dict[str, list[str]] = defaultdict(list)
        for pre_name, pre_data in self.world.generated_pokemon.items():
            for evo in pre_data.evolutions:
                if _eil(self.world, evo):
                    in_logic_preevos[evo.pokemon].append(pre_name)

        egg_producers: dict[str, list[str]] = defaultdict(list)
        for name, pdata in self.world.generated_pokemon.items():
            if pdata.produces_egg:
                egg_producers[pdata.produces_egg].append(name)

        expected: set[str] = set(statics)
        frontier = set(statics)
        while frontier:
            new: set[str] = set()
            for sp in frontier:
                for pre in in_logic_preevos.get(sp, ()):
                    if pre not in expected:
                        expected.add(pre)
                        new.add(pre)
                for producer in egg_producers.get(sp, ()):
                    if producer not in expected:
                        expected.add(producer)
                        new.add(producer)
            frontier = new

        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        collisions = expected & wild
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"combined closure species appeared in wilds: {sorted(collisions)}")


class UniqueStaticsBreedingInLogicTest(PokemonCrystalTestBase):
    options = {
        **COMMON_OPTS,
        "unique_static_pokemon": "all",
        "evolution_methods_required": [],
        "breeding_methods_required": "any",
        "randomize_breeding": "completely_random",
    }

    def test_egg_producers_of_statics_absent_from_wilds(self):
        statics = {slot.pokemon for slot in _in_logic_static(self.world).values()}
        # Without evolution-in-logic, closure expands only via produces_egg inversion.
        expected_producers: set[str] = set()
        frontier = set(statics)
        while frontier:
            nxt: set[str] = set()
            for name, pdata in self.world.generated_pokemon.items():
                if pdata.produces_egg in frontier and name not in expected_producers and name not in statics:
                    expected_producers.add(name)
                    nxt.add(name)
            frontier = nxt

        wild = _wild_species(self.world)
        self.assertTrue(wild, "no wild species generated; test would pass vacuously")
        collisions = expected_producers & wild
        collisions.discard("DITTO")
        self.assertEqual(collisions, set(),
                         f"egg producers of static species appeared in wilds: {sorted(collisions)}")

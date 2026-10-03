from dataclasses import replace

from .bases import PokemonCrystalTestBase
from ..trainers import set_rival_starter_pokemon, randomize_trainers
from ..pokemon_data import VANILLA_STARTERS
from ..moves import get_random_move_from_learnset
from ..pokemon import get_evolution_at_level
from ..data import LearnsetData, TMHMData, EvolutionType, data


class RivalStarterVanillaTrainersTest(PokemonCrystalTestBase):
    options = {
        "randomize_starters": "first_stage_can_evolve",
        "randomize_trainer_parties": "vanilla",
        "randomize_learnsets": "vanilla",
    }

    def test_rival_starter_species_matches_generated_starters(self):
        set_rival_starter_pokemon(self.world)

        for evo_line, vanilla_line in zip(self.world.generated_starters, VANILLA_STARTERS):
            for vanilla_name, expected_pokemon in zip(vanilla_line, evo_line):
                for trainer_name, trainer_data in self.world.generated_trainers.items():
                    if not trainer_name.startswith("RIVAL_" + vanilla_name):
                        continue
                    actual = trainer_data.pokemon[-1].pokemon
                    self.assertEqual(actual, expected_pokemon,
                                     f"{trainer_name}: expected {expected_pokemon}, got {actual}")

    def test_rival_starter_moves_not_vanilla(self):
        vanilla_moves = {}
        for trainer_name, trainer_data in self.world.generated_trainers.items():
            if trainer_name.startswith("RIVAL") and trainer_data.pokemon[-1].moves:
                vanilla_moves[trainer_name] = list(trainer_data.pokemon[-1].moves)

        set_rival_starter_pokemon(self.world)

        changed_count = 0
        for trainer_name, original_moves in vanilla_moves.items():
            new_moves = list(self.world.generated_trainers[trainer_name].pokemon[-1].moves)
            if new_moves != original_moves:
                changed_count += 1

        self.assertGreater(changed_count, 0, "No rival starter moves were changed")

    def test_rival_starter_moves_from_new_species_learnset(self):
        set_rival_starter_pokemon(self.world)

        for trainer_name, trainer_data in self.world.generated_trainers.items():
            if not trainer_name.startswith("RIVAL"):
                continue
            rival_pkmn = trainer_data.pokemon[-1]
            if not rival_pkmn.moves:
                continue

            pokemon_data = self.world.generated_pokemon[rival_pkmn.pokemon]
            move_pool = {lm.move for lm in pokemon_data.learnset
                         if lm.level <= rival_pkmn.level and lm.move != "NO_MOVE"}
            move_pool.update(self.world.generated_tms[tm].id for tm in pokemon_data.tm_hm
                             if self.world.generated_tms[tm].id != "BEAT_UP")

            for move in rival_pkmn.moves:
                self.assertIn(move, move_pool,
                              f"{trainer_name}: {rival_pkmn.pokemon} has move {move} not in its move pool")


class MoveSelectionWeightingTest(PokemonCrystalTestBase):
    options = {
        "randomize_learnsets": "vanilla",
    }

    LEARNSET_MOVES = ["TACKLE", "GROWL", "VINE_WHIP", "RAZOR_LEAF"]
    TMHM_MOVES = ["EARTHQUAKE", "FLAMETHROWER", "ICE_BEAM"]

    def _inject_test_mon(self):
        # build a Pokemon with a learnset and TM/HM pool that share no moves
        pokemon_name = next(iter(self.world.generated_pokemon))
        base = self.world.generated_pokemon[pokemon_name]
        learnset = [LearnsetData(1, move) for move in self.LEARNSET_MOVES]
        tm_names = []
        for i, move in enumerate(self.TMHM_MOVES):
            tm_name = f"TEST_TM_{i}"
            self.world.generated_tms[tm_name] = TMHMData(move, i + 1, "NORMAL", False, 0)
            tm_names.append(tm_name)
        self.world.generated_pokemon[pokemon_name] = replace(base, learnset=learnset, tm_hm=tm_names)
        return pokemon_name

    def test_falls_back_to_tmhm_when_no_learnset_available(self):
        pokemon_name = self._inject_test_mon()
        tmhm = set(self.TMHM_MOVES)
        # no learnset move is available at level 0, so every pick must be a TM/HM move
        for _ in range(50):
            move = get_random_move_from_learnset(self.world, pokemon_name, level=0)
            self.assertIn(move, tmhm)


class RivalStarterRandomizedTrainersTest(PokemonCrystalTestBase):
    options = {
        "randomize_starters": "first_stage_can_evolve",
        "randomize_trainer_parties": "match_types",
        "randomize_learnsets": "vanilla",
    }

    def test_rival_starter_moves_from_new_species_learnset(self):
        set_rival_starter_pokemon(self.world)
        randomize_trainers(self.world)

        for trainer_name, trainer_data in self.world.generated_trainers.items():
            if not trainer_name.startswith("RIVAL"):
                continue
            rival_pkmn = trainer_data.pokemon[-1]
            if not rival_pkmn.moves:
                continue

            pokemon_data = self.world.generated_pokemon[rival_pkmn.pokemon]
            move_pool = {lm.move for lm in pokemon_data.learnset
                         if lm.level <= rival_pkmn.level and lm.move != "NO_MOVE"}
            move_pool.update(self.world.generated_tms[tm].id for tm in pokemon_data.tm_hm
                             if self.world.generated_tms[tm].id != "BEAT_UP")

            for move in rival_pkmn.moves:
                self.assertIn(move, move_pool,
                              f"{trainer_name}: {rival_pkmn.pokemon} has move {move} not in its move pool")


class ForceFullyEvolvedAtEvolutionLevelTest(PokemonCrystalTestBase):
    options = {
        "randomize_trainer_parties": "completely_random",
        "force_fully_evolved": "evolution_level",
    }

    def _min_evolution_level(self, pokemon_name):
        levels = [evo.level for evo in self.world.generated_pokemon[pokemon_name].evolutions
                  if evo.evo_type in (EvolutionType.Level, EvolutionType.Stats) and evo.level is not None]
        return min(levels) if levels else None

    def test_trainer_pokemon_below_their_evolution_level(self):
        randomize_trainers(self.world)

        for trainer_name, trainer_data in self.world.generated_trainers.items():
            for pkmn in trainer_data.pokemon:
                evo_level = self._min_evolution_level(pkmn.pokemon)
                if evo_level is None:
                    continue
                self.assertLess(pkmn.level, evo_level,
                                f"{trainer_name}: {pkmn.pokemon} at level {pkmn.level} evolves at {evo_level}")

    def test_evolution_at_level_follows_level_evolutions(self):
        for pokemon_name, pokemon_data in self.world.generated_pokemon.items():
            evolved = get_evolution_at_level(self.world, pokemon_name, 100)
            self.assertIsNone(self._min_evolution_level(evolved),
                              f"{pokemon_name} evolved to {evolved}, which still evolves by level")


class ForceFullyEvolvedAtEvolutionLevelRandomEvolutionsTest(ForceFullyEvolvedAtEvolutionLevelTest):
    options = {
        "randomize_trainer_parties": "completely_random",
        "force_fully_evolved": "evolution_level",
        "randomize_evolution": "increase_bst",
    }


class ForceFullyEvolvedAtEvolutionLevelBlocklistTest(PokemonCrystalTestBase):
    BLOCKED = ["Gyarados", "Dragonite", "Raticate", "Golem", "Alakazam", "Machamp", "Butterfree"]
    options = {
        "randomize_trainer_parties": "completely_random",
        "force_fully_evolved": "evolution_level",
        "trainer_party_blocklist": BLOCKED,
    }

    def test_blocklisted_pokemon_not_reached_by_evolving(self):
        randomize_trainers(self.world)

        blocked = self.world.options.trainer_party_blocklist.get_ids(self.world)
        for trainer_name, trainer_data in self.world.generated_trainers.items():
            if "LASS_ALICE" in trainer_name:
                continue
            for pkmn in trainer_data.pokemon:
                self.assertNotIn(pkmn.pokemon, blocked, f"{trainer_name} uses blocklisted {pkmn.pokemon}")


class ForceFullyEvolvedAtEvolutionLevelMatchTest(PokemonCrystalTestBase):
    options = {
        "randomize_trainer_parties": "match_types_and_base_stats",
        "force_fully_evolved": "evolution_level",
    }

    def test_evolved_pokemon_still_match_types_and_base_stats(self):
        vanilla_parties = {name: [p.pokemon for p in trainer.pokemon]
                           for name, trainer in self.world.generated_trainers.items()}
        randomize_trainers(self.world)

        type_misses = bst_misses = total = 0
        for trainer_name, trainer_data in self.world.generated_trainers.items():
            if trainer_name.startswith("RIVAL") or "LASS_ALICE" in trainer_name:
                continue
            for vanilla_name, pkmn in zip(vanilla_parties[trainer_name], trainer_data.pokemon):
                vanilla = data.pokemon[vanilla_name]
                new = self.world.generated_pokemon[pkmn.pokemon]
                total += 1
                if not set(vanilla.types) & set(new.types):
                    type_misses += 1
                if abs(new.bst - vanilla.bst) > vanilla.bst * .2:
                    bst_misses += 1

        self.assertLess(type_misses, total * .02, f"{type_misses}/{total} pokemon share no type with the vanilla mon")
        self.assertLess(bst_misses, total * .1, f"{bst_misses}/{total} pokemon are outside 20% of the vanilla BST")

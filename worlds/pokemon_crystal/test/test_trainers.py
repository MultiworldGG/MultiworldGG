from .bases import PokemonCrystalTestBase
from ..trainers import set_rival_starter_pokemon, randomize_trainers
from ..pokemon_data import VANILLA_STARTERS


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

import unittest
from dataclasses import replace

from test.general import setup_multiworld
from worlds.AutoWorld import call_all
from .bases import PokemonCrystalTestBase
from ..data import LogicalAccess
from ..wild import get_logically_available_wilds


class WildMagikarpPlacementTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "randomize_pokemon_requests": "pokemon",
    }

    def test_magikarp_in_logical_wilds(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available, "MAGIKARP not found in logical wilds")


class WildMagikarpBlocklistedTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "randomize_pokemon_requests": "pokemon",
        "wild_encounter_blocklist": ["Magikarp"],
    }

    def test_magikarp_placed_despite_blocklist(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available, "MAGIKARP not placed despite being required for logic")


class WildDittoPlacementTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "breeding_methods_required": "with_ditto",
    }

    def test_ditto_in_logical_wilds(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("DITTO", available, "DITTO not found in logical wilds")


class WildCatchEmAllWithBlocklistTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "catch_em_all",
        "randomize_pokemon_requests": "pokemon",
        "wild_encounter_blocklist": ["Magikarp", "_Water"],
    }

    def test_magikarp_placed_with_catch_em_all_and_blocklist(self):
        """Must-place pokemon are placed even when blocklisted."""
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available)


class WildMustPlaceNotOverwrittenTest(PokemonCrystalTestBase):
    options = {
        "randomize_wilds": "completely_random",
        "randomize_pokemon_requests": "pokemon",
        "breeding_methods_required": "with_ditto",
        "wild_encounter_blocklist": ["Magikarp"],
    }

    def test_magikarp_and_ditto_both_placed(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("MAGIKARP", available, "MAGIKARP not found in logical wilds")
        self.assertIn("DITTO", available, "DITTO not found in logical wilds")


class WildSwarmDefaultOutOfLogicTest(PokemonCrystalTestBase):
    options = {
        "randomize_phone_call_items": "true",
        "phone_call_mode": "simple",
    }

    def test_swarm_regions_not_in_logic_by_default(self):
        from ..data import LogicalAccess
        for key, access in self.world.logic.wild_regions.items():
            if key.region_id is not None and key.region_id.endswith("_Swarm"):
                self.assertIsNot(access, LogicalAccess.InLogic,
                                 f"{key} should not be in logic when SWARM is not requested")


class WildSwarmInLogicTest(PokemonCrystalTestBase):
    options = {
        "randomize_phone_call_items": "true",
        "phone_call_mode": "simple",
        "randomize_pokegear": True,
        "wild_encounter_methods_required": [
            "Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Swarm",
        ],
    }

    def test_swarm_species_available(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("DUNSPARCE", available)
        self.assertIn("YANMA", available)
        self.assertIn("QWILFISH", available)


class WildSwarmInLogicWithoutItemsRandomizedTest(PokemonCrystalTestBase):
    """Swarms qualify independently of Randomize Phone Call Items / Phone Call Mode —
    if the player asked for SWARM in wild_encounter_methods_required, they get it."""
    options = {
        "randomize_phone_call_items": "false",
        "phone_call_mode": "simple",
        "randomize_pokegear": True,
        "wild_encounter_methods_required": [
            "Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Swarm",
        ],
    }

    def test_swarm_species_available(self):
        available = get_logically_available_wilds(self.world)
        self.assertIn("DUNSPARCE", available)
        self.assertIn("YANMA", available)
        self.assertIn("QWILFISH", available)


class WildSwarmRegistrationGatingTest(PokemonCrystalTestBase):
    options = {
        "randomize_phone_call_items": "true",
        "phone_call_mode": "simple",
        "randomize_pokegear": True,
        "wild_encounter_methods_required": [
            "Land", "Surfing", "Fishing", "Headbutt", "Rock Smash", "Bug Catching Contest", "Swarm",
        ],
    }

    def test_swarm_locations_gated_on_registration_event(self):
        from ..data import EncounterType
        from ..pokemon_data import SWARM_REGISTRATIONS
        swarm_loc = registration_event = None
        for loc in self.world.multiworld.get_locations(self.world.player):
            key = getattr(loc.parent_region, "key", None)
            if (key is not None and key.encounter_type is EncounterType.Swarm
                    and "wild encounter" in loc.tags):
                cfg = SWARM_REGISTRATIONS.get(key.region_id)
                if cfg is not None:
                    swarm_loc, registration_event = loc, cfg["registration_event"]
                    break
        self.assertIsNotNone(swarm_loc, "expected a swarm wild-encounter location with a registration event")
        self.assertTrue(swarm_loc.access_rule(self.multiworld.get_all_state(False)),
                        "swarm location should be reachable in all-state")
        state = self.multiworld.get_all_state(False)
        state.remove(self.world.create_event(registration_event))
        self.assertFalse(swarm_loc.access_rule(state),
                         "removing the registration event should gate the swarm location")


class SharedWildEncountersTest(unittest.TestCase):
    options = {
        "randomize_wilds": "completely_random",
        "time_of_day_encounters": "true",
    }

    def _generate(self, shared: bool):
        from ..world import PokemonCrystalWorld
        options = {**self.options, "shared_wild_encounters": str(shared).lower()}
        multiworld = setup_multiworld([PokemonCrystalWorld, PokemonCrystalWorld], seed=1, options=[options, options])
        return [multiworld.worlds[player] for player in multiworld.player_ids]

    def test_shared_encounters_match(self):
        first, second = self._generate(True)
        self.assertEqual(first.generated_wild, second.generated_wild)
        self.assertEqual(first.generated_contest, second.generated_contest)
        self.assertEqual(first.generated_wooper, second.generated_wooper)

    def test_unshared_encounters_differ(self):
        first, second = self._generate(False)
        self.assertNotEqual(first.generated_wild, second.generated_wild)

    def test_catch_em_all_shared(self):
        self.options = {**self.options, "randomize_wilds": "catch_em_all"}
        first, second = self._generate(True)
        self.assertEqual(first.generated_wild, second.generated_wild)

    def test_match_mode_not_shared(self):
        self.options = {**self.options, "wild_match_mode": "match_types"}
        first, second = self._generate(True)
        self.assertNotEqual(first.generated_wild, second.generated_wild)


class UnownGateFollowsFinalSpeciesTest(unittest.TestCase):
    """Starter placement changes wild species after set_rules, so the Unown unlock gate must follow the final
    species rather than the ones present when rules were set."""

    UNLOCKS = ("ENGINE_UNLOCKED_UNOWNS_A_TO_K", "ENGINE_UNLOCKED_UNOWNS_L_TO_R",
               "ENGINE_UNLOCKED_UNOWNS_S_TO_W", "ENGINE_UNLOCKED_UNOWNS_X_TO_Z")

    def test_unown_gate_follows_species_changed_after_set_rules(self):
        from ..world import PokemonCrystalWorld
        multiworld = setup_multiworld(PokemonCrystalWorld,
                                      ("generate_early", "create_regions", "create_items", "set_rules"), seed=1)
        world = multiworld.worlds[1]
        in_logic = [key for key in world.generated_wild
                    if world.logic.wild_regions.get(key) is LogicalAccess.InLogic]
        loses_unown = next(key for key in in_logic if any(e.pokemon == "UNOWN" for e in world.generated_wild[key]))
        gains_unown = next(key for key in in_logic if all(e.pokemon != "UNOWN" for e in world.generated_wild[key]))

        lost_slots = [i for i, e in enumerate(world.generated_wild[loses_unown]) if e.pokemon == "UNOWN"]
        world.generated_wild[loses_unown] = [replace(e, pokemon="PIDGEY") if e.pokemon == "UNOWN" else e
                                             for e in world.generated_wild[loses_unown]]
        gained = world.generated_wild[gains_unown]
        world.generated_wild[gains_unown] = [replace(gained[0], pokemon="UNOWN")] + gained[1:]
        call_all(multiworld, "connect_entrances")

        state = multiworld.get_all_state(False)
        for unlock in self.UNLOCKS:
            while state.has(unlock, world.player):
                state.remove(world.create_event(unlock))
        self.assertFalse(world.get_location(f"{gains_unown.region_name()}_1").access_rule(state),
                         "a slot that became Unown must require a chamber unlock")
        for i in lost_slots:
            location = world.get_location(f"{loses_unown.region_name()}_{i + 1}")
            self.assertTrue(location.access_rule(state), f"{location.name} is no longer Unown but is still gated")

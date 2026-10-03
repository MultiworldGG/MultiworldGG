import tempfile
from unittest.mock import patch as mock_patch

from Fill import distribute_items_restrictive
from .bases import PokemonCrystalTestBase, verify_region_access
from ..data import data


class SkipEliteFourRequirementTest(PokemonCrystalTestBase):
    options = {
        "skip_elite_four": "on",
        "randomize_badges": "completely_random",
        "victory_road_count": 0,
        "elite_four_requirement": "johto_badges",
        "elite_four_count": 8,
    }

    def test_skip_requires_elite_four_badges(self):
        verify_region_access(self, ["Hive Badge"], ["REGION_LANCES_ROOM", "REGION_HALL_OF_FAME"])


class SkipEliteFourLeagueERTest(PokemonCrystalTestBase):
    options = {
        "skip_elite_four": "on",
        "randomize_entrances": ["Pokemon League", "Gym Interior"],
        "mix_entrances": ["Pokemon League", "Gym Interior"],
        "plando_connections": [{
            "entrance": "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_LANCES_ROOM",
            "exit": "REGION_SAFFRON_GYM:SE -> REGION_SAFFRON_GYM:ENTRANCE",
            "direction": "both",
        }],
    }

    def test_skip_edges_randomized(self):
        pairings = set(self.world.er_pairings)
        self.assertIn(("REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_LANCES_ROOM",
                       "REGION_SAFFRON_GYM:ENTRANCE -> REGION_SAFFRON_GYM:SE"), pairings)
        self.assertIn(("REGION_SAFFRON_GYM:ENTRANCE -> REGION_SAFFRON_GYM:SE",
                       "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_LANCES_ROOM"), pairings)
        self.assertNotIn(("REGION_LANCES_ROOM -> REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE",
                          "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_LANCES_ROOM"), pairings)


class SkipEliteFourNonLeagueERTest(PokemonCrystalTestBase):
    options = {
        "skip_elite_four": "on",
        "randomize_entrances": ["Gym Interior"],
    }

    def test_lance_exit_returns_to_gate(self):
        entrance = self.multiworld.get_entrance(
            "REGION_LANCES_ROOM -> REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE", self.player)
        self.assertEqual(entrance.connected_region.name, "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE")
        self.assertNotIn(entrance.name, {source for source, _ in self.world.er_pairings})

    def test_rom_lance_exit_warps_to_gate(self):
        distribute_items_restrictive(self.multiworld)
        self.world.finished_level_scaling.set()
        tokens: dict[int, bytes] = {}

        def capture(self_patch, token_type, offset, payload):
            tokens[offset] = bytes(payload)

        with tempfile.TemporaryDirectory() as tmp, \
                mock_patch("worlds.pokemon_crystal.rom.PokemonCrystalProcedurePatch.write_token", capture):
            self.world.generate_output(tmp)

        gate = bytes([4, *data.map_constants["INDIGO_PLATEAU_POKECENTER_1F"]])
        for label in ("AP_Warp_LancesRoom_1", "AP_Warp_LancesRoom_2"):
            self.assertEqual(tokens[data.rom_addresses[label] + 2], gate)

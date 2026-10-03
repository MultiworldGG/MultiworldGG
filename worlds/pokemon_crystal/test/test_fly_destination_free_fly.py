import tempfile
from unittest.mock import patch as mock_patch

from Fill import distribute_items_restrictive
from .bases import PokemonCrystalTestBase
from ..data import data
from ..fly import get_fly_regions, fly_flag_index, flypoint_arrival_connections


class FlyDestinationsFreeFlyJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "johto_only": "on",
        "randomize_fly_destinations": "on",
        "free_fly_location": "free_fly_and_map_card",
    }

    def test_indigo_uses_seed_index(self):
        indigo = next(fr for fr in data.fly_regions if fr.name == "Indigo Plateau")
        self.assertEqual(fly_flag_index(self.world, indigo), 11)

    def test_free_fly_picked_from_seed_fly_regions(self):
        fly_regions = get_fly_regions(self.world)
        self.assertIn(self.world.free_fly_location, fly_regions)
        self.assertIn(self.world.map_card_fly_location, fly_regions)

    def test_free_fly_connects_to_seed_destination(self):
        for fly_region in (self.world.free_fly_location, self.world.map_card_fly_location):
            flypoint = self.world.fly_destinations[fly_flag_index(self.world, fly_region)]
            dest = flypoint_arrival_connections(flypoint)[0].entrance_region
            self.multiworld.get_entrance(f"Free Fly {dest}", self.player)

    def test_rom_free_fly_bits_use_seed_index(self):
        distribute_items_restrictive(self.multiworld)
        self.world.finished_level_scaling.set()
        tokens: dict[int, bytes] = {}

        def capture(self_patch, token_type, offset, payload):
            tokens[offset] = bytes(payload)

        with tempfile.TemporaryDirectory() as tmp, \
                mock_patch("worlds.pokemon_crystal.rom.PokemonCrystalProcedurePatch.write_token", capture):
            self.world.generate_output(tmp)

        free_fly_flag = fly_flag_index(self.world, self.world.free_fly_location)
        free_fly_bytes = tokens[data.rom_addresses["AP_Setting_FreeFly"]]
        self.assertEqual(int.from_bytes(free_fly_bytes, "little"), 1 << free_fly_flag)

        map_fly_flag = fly_flag_index(self.world, self.world.map_card_fly_location)
        self.assertEqual(tokens[data.rom_addresses["AP_Setting_MapCardFreeFly_Byte"] + 1],
                         bytes([1 << (map_fly_flag % 8)]))
        self.assertEqual(tokens[data.rom_addresses["AP_Setting_MapCardFreeFly_Offset"] + 1],
                         (map_fly_flag // 8).to_bytes(2, "little"))

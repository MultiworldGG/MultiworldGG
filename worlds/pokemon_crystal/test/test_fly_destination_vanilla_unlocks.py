import tempfile
from unittest.mock import patch as mock_patch

from BaseClasses import CollectionState
from Fill import distribute_items_restrictive
from .bases import PokemonCrystalTestBase
from ..data import data
from ..fly import get_fly_regions
from ..items import item_const_name_to_id


class FlyDestinationsVanillaUnlocksTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_destinations": "on",
        "randomize_fly_unlocks": "off",
        "remote_items": "false",
    }

    def test_destinations_gated_on_positional_visit_event(self):
        for i, fly_region in enumerate(get_fly_regions(self.world), start=1):
            entrance = self.multiworld.get_entrance(f"Fly Destination {i}", self.player)
            state = CollectionState(self.multiworld)
            self.assertFalse(entrance.access_rule(state), f"Fly Destination {i} open without any visit")
            state.collect(self.world.create_event(f"EVENT_VISITED_{fly_region.base_identifier}"), prevent_sweep=True)
            self.assertTrue(entrance.access_rule(state),
                            f"Fly Destination {i} not opened by visiting {fly_region.name}")

    def test_rom_flag_item_table_uses_position(self):
        distribute_items_restrictive(self.multiworld)
        self.world.finished_level_scaling.set()
        tokens: dict[int, bytes] = {}

        def capture(self_patch, token_type, offset, payload):
            tokens[offset] = bytes(payload)

        with tempfile.TemporaryDirectory() as tmp, \
                mock_patch("worlds.pokemon_crystal.rom.PokemonCrystalProcedurePatch.write_token", capture):
            self.world.generate_output(tmp)

        table = data.rom_addresses["AP_Setting_FlagItems_Table_Events"]
        flag_item = item_const_name_to_id("FLAG_ITEM")
        fly_regions = get_fly_regions(self.world)
        for i, fly_region in enumerate(fly_regions, start=1):
            self.assertEqual(tokens[data.rom_addresses[f"AP_FlyUnlock_{fly_region.base_identifier}"]], bytes([flag_item]))
            event_flag = data.event_flags[f"EVENT_VISITED_{fly_region.base_identifier}"]
            self.assertEqual(tokens[table + event_flag], bytes([i]), fly_region.name)
        for fly_region in set(data.fly_regions) - set(fly_regions):
            self.assertEqual(tokens[data.rom_addresses[f"AP_FlyUnlock_{fly_region.base_identifier}"]], b"\x00",
                             fly_region.name)


class FlyDestinationsVanillaUnlocksJohtoOnlyTest(FlyDestinationsVanillaUnlocksTest):
    options = {**FlyDestinationsVanillaUnlocksTest.options, "johto_only": "on"}

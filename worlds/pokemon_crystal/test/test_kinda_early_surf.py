from .bases import PokemonCrystalTestBase

gated_entrances = [
    "REGION_GOLDENROD_MAGNET_TRAIN_STATION -> REGION_SAFFRON_MAGNET_TRAIN_STATION",
    "REGION_MAHOGANY_TOWN -> REGION_MAHOGANY_TOWN:EAST",
    "REGION_RADIO_TOWER_2F -> REGION_RADIO_TOWER_2F:TAKEOVER",
    "REGION_ECRUTEAK_TIN_TOWER_ENTRANCE -> REGION_ECRUTEAK_TIN_TOWER_ENTRANCE:BEHIND_SAGE",
    "REGION_VERMILION_CITY -> REGION_ROUTE_11",
    "REGION_VERMILION_CITY -> REGION_VERMILION_CITY:DIGLETTS_CAVE_ENTRANCE",
    "REGION_VIRIDIAN_CITY -> REGION_VIRIDIAN_GYM",
    "REGION_PEWTER_CITY -> REGION_PEWTER_GYM",
    "REGION_CERULEAN_CITY -> REGION_CERULEAN_GYM",
    "REGION_VERMILION_CITY:GYM_ENTRANCE -> REGION_VERMILION_GYM",
    "REGION_SAFFRON_CITY -> REGION_SAFFRON_GYM:ENTRANCE",
    "REGION_CELADON_CITY:GYM_ENTRANCE -> REGION_CELADON_GYM",
    "REGION_FUCHSIA_CITY -> REGION_FUCHSIA_GYM",
    "REGION_ROUTE_20:SEAFOAM -> REGION_SEAFOAM_GYM",
]

gated_locations = [
    "EVENT_JASMINE_RETURNED_TO_GYM",
    "EVENT_FOUGHT_SNORLAX",
    "Olivine Gym - Mineral Badge from Jasmine",
    "Olivine Gym - TM23 from Jasmine",
]


class KindaEarlySurfTest(PokemonCrystalTestBase):
    options = {
        "kinda_early_surf": "true",
        "field_moves_always_usable": "true",
        "hm_badge_requirements": "no_badges",
    }

    def test_surf_gates_entrances_and_locations(self):
        self.collect_all_but(["HM03 Surf", "EVENT_JASMINE_RETURNED_TO_GYM", "EVENT_FOUGHT_SNORLAX"])
        state = self.multiworld.state
        for entrance in gated_entrances:
            self.assertFalse(state.can_reach_entrance(entrance, self.player),
                             f"Entrance {entrance} reachable without Surf when kinda_early_surf is on.")
        for location in gated_locations:
            self.assertFalse(state.can_reach_location(location, self.player),
                             f"Location {location} reachable without Surf when kinda_early_surf is on.")
        self.collect_by_name(["HM03 Surf", "EVENT_JASMINE_RETURNED_TO_GYM", "EVENT_FOUGHT_SNORLAX"])
        state = self.multiworld.state
        for entrance in gated_entrances:
            self.assertTrue(state.can_reach_entrance(entrance, self.player),
                            f"Entrance {entrance} unreachable with Surf.")
        for location in gated_locations:
            self.assertTrue(state.can_reach_location(location, self.player),
                            f"Location {location} unreachable with Surf.")


class KindaEarlySurfDisabledByJohtoOnlyTest(PokemonCrystalTestBase):
    options = {
        "kinda_early_surf": "true",
        "johto_only": "on",
    }

    def test_option_force_disabled(self):
        self.assertFalse(bool(self.world.options.kinda_early_surf))


class KindaEarlySurfDisabledByRandomStartingTownTest(PokemonCrystalTestBase):
    options = {
        "kinda_early_surf": "true",
        "randomize_starting_town": "true",
    }

    def test_option_force_disabled(self):
        self.assertFalse(bool(self.world.options.kinda_early_surf))


class KindaEarlySurfDisabledByEntranceRandoTest(PokemonCrystalTestBase):
    options = {
        "kinda_early_surf": "true",
        "randomize_entrances": ["Dungeon"],
    }

    def test_option_force_disabled(self):
        self.assertFalse(bool(self.world.options.kinda_early_surf))

from .bases import PokemonCrystalTestBase

class FriendlyMapNamesTest(PokemonCrystalTestBase):
    options = {}

    def test_friendly_map_names_match(self):
        """Prevent data drift by checking that the list of friendly map names in data corresponds exactly
        to the flypoints' maps."""
        from ..data import OUTDOOR_WARP_MAP_FRIENDLY_NAMES
        from ..fly import _get_flyable_warps
        internal_map_names = {"".join(part.title() for part in name.split(" "))
                              for name in OUTDOOR_WARP_MAP_FRIENDLY_NAMES}
        flypoint_maps = set()
        for flypoints in _get_flyable_warps().values():
            flypoint_maps |= {flypoint.map_name for flypoint in flypoints}
        self.assertEqual(internal_map_names, flypoint_maps)

class FlyDestinationPlandoTest(PokemonCrystalTestBase):
    options = {
        "randomize_fly_destinations": "true",
        "fly_destination_plando": {
            "Fly Destination 1": "Route 30"
        },
        "fly_destination_blocklist": ["Route 30 Berry House Entrance"]
    }

    def test_plando_map_ignores_blocklisted_warps(self):
        """Check that a combination of plandoing a map and blocklisting some warps on that map
        filters out the blocklisted warps while keeping a flypoint on that map"""
        from ..data import data
        # Route 30 has only 2 warps, and we blocklisted the Berry House,
        # so Fly Destination 1 should always be Mr. Pokemon's House
        flypoint_1 = self.world.fly_destinations[0]
        mr_pokemons_house_warp = data.entrance_connections["REGION_ROUTE_30 -> REGION_MR_POKEMONS_HOUSE"].exit_warps[0]
        self.assertEqual((flypoint_1.map_name, flypoint_1.warp_index),
                         (mr_pokemons_house_warp.map_name, mr_pokemons_house_warp.warp_index))

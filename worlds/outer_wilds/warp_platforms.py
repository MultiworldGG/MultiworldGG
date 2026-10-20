from random import Random
from .options import Spawn
from Options import OptionError

# Use lists instead of sets for collections whose copies will get shuffled to ensure determinism.
warp_platforms = [
    "SS",  # Sun Station
    "ST",  # Sun Tower on Ash Twin
    "ET",  # Ember Twin
    "ETT",  # Ember Twin Tower
    "ATP",  # inside Ash Twin Project
    "ATT",  # Ash Twin Tower on Ash Twin's surface
    "TH",  # Timber Hearth
    "THT",  # Timber Hearth Tower on Ash Twin
    "BHNG",  # Brittle Hollow Northern Glacier
    "WHS",  # White Hole Station
    "BHF",  # the pad on the Hanging City ceiling used to access Black Hole Forge
    "BHT",  # Brittle Hollow Tower on Ash Twin
    "GD",  # Giant's Deep
    "GDT",  # Giant's Deep Tower on Ash Twin
]
warp_platform_to_logical_region = {
    "SS": "Sun Station",
    "ST": "Hourglass Twins",
    "ET": "Hourglass Twins",
    "ETT": "Hourglass Twins",
    "ATP": "Ash Twin Interior",
    "ATT": "Hourglass Twins",
    "TH": "Timber Hearth",
    "THT": "Hourglass Twins",
    "BHNG": "Brittle Hollow",
    "WHS": "White Hole Station",
    "BHF": "Hanging City Ceiling",
    "BHT": "Hourglass Twins",
    "GD": "Giant's Deep",
    "GDT": "Hourglass Twins",
}
warp_platform_required_items = {
    "SS": ["Spacesuit"],
    "ST": ["Spacesuit"],
}

vanilla_warp_mapping = [
    ("SS", "ST"),
    ("ET", "ETT"),
    ("ATP", "ATT"),
    ("TH", "THT"),
    ("BHNG", "WHS"),
    ("BHF", "BHT"),
    ("GD", "GDT"),
]


class WarpPlatforms:
    def __init__(self):
        self.mappings: list[tuple[str, str]] = []

        # These are the warp platforms which (logically) can only be reached via another warp platform.
        self.dead_end_platforms = [
            "SS",
            "ATP",
            "BHF",
        ]
        self.itemless_warp_region_connections = {
            "Brittle Hollow": {"White Hole Station"},
            "Hanging City Ceiling": {"White Hole Station", "Brittle Hollow"},
        }


    def apply_vanilla_warp_platform_mapping(self):
        self.mappings = vanilla_warp_mapping.copy()


    def randomize_unmapped_warps(self, random: Random, spawn: Spawn) -> None:
        unmapped_platforms = self.get_unmapped_warps()
        platforms_reachable_by_ship = [p for p in warp_platforms if p not in self.dead_end_platforms]
        # Handle dead ends first to avoid pairing dead ends with other dead ends (e.g. Sun Station <-> ATP)
        for dead_end_platform in self.dead_end_platforms:
            if dead_end_platform not in unmapped_platforms:
                continue # Warp has been connected via plando.
            available_platforms = [p for p in unmapped_platforms if p in platforms_reachable_by_ship]

            # Sun Station is the only warp platform that disappears about halfway through the loop.
            # Technically every other platform is exposed by then, but for some the margin is just too small.
            if dead_end_platform == 'SS':  # actually falls into the sun at 11:30 - 11:40
                available_platforms = [p for p in available_platforms if p not in [
                    'THT',  # exposed at ~10:30
                    'BHT',  # exposed at ~10:30
                    'GDT'   # exposed at ~11:00
                ]]
                # The above rules out a direct THT/BHT/GDT->SS warp, but we also need to rule out a longer
                # warp path through THT/BHT/GDT being the only way to SS. Such a path would have to go
                # through Brittle Hollow because it's the only planet besides HGT with multiple warp pads.
                if spawn != Spawn.option_brittle_hollow:
                    available_platforms = [p for p in available_platforms if p not in ['BHNG', 'WHS']]

            if len(available_platforms) == 0:
                raise OptionError(f"Error while randomizing warps: Can't connect dead end warp {dead_end_platform} to non dead end warp.")
            destination = random.choice(available_platforms)
            self.mappings.append((dead_end_platform, destination))
            unmapped_platforms.remove(dead_end_platform)
            unmapped_platforms.remove(destination)

        random.shuffle(unmapped_platforms)
        it = iter(unmapped_platforms)
        self.mappings.extend(list(zip(it, it)))


    def shipless_connection_exists(self, from_region: str, to_region: str, two_way: bool = False) -> bool:
        if from_region not in warp_platform_to_logical_region.values():
            return False
        return self._connection_exists_recursive_impl(from_region, to_region, two_way, set())


    # Here we make the strong assumption that all logic outside of this file is irrelevant,
    # because this is only used to tell if a "shipless warp path" exists between two platforms
    def _connection_exists_recursive_impl(self, from_region: str, to_region: str, two_way: bool, already_checked_regions: set[str]) -> bool:
        if from_region in already_checked_regions:
            return False

        # First expand the from_region into a list of all warp-containing regions reachable by walking/falling without the ship
        warp_regions_reachable_warpless = { from_region }
        if from_region in self.itemless_warp_region_connections.keys():
            if two_way:
                warp_regions_reachable_warpless.update({r for r in self.itemless_warp_region_connections[from_region] if from_region in self.itemless_warp_region_connections[r]})
            else:
                warp_regions_reachable_warpless.update(self.itemless_warp_region_connections[from_region])

        warp_regions_reachable_warpless.difference_update(already_checked_regions)
        from_warps = [warp for warp, region in warp_platform_to_logical_region.items() if region in warp_regions_reachable_warpless]
        already_checked_regions.update(warp_regions_reachable_warpless)

        # Then check the actual warp connections, with recursive calls to search for a complete path
        while len(from_warps) > 0:
            next_target_warp = self.get_connected_warp(from_warps.pop(0))
            if next_target_warp is None:
                continue
            next_target_region = warp_platform_to_logical_region[next_target_warp]
            if next_target_region == to_region or self._connection_exists_recursive_impl(next_target_region, to_region, two_way, already_checked_regions):
                return True
        return False


    def get_connected_warp(self, warp: str) -> str|None:
        source = [w1 for (w1, w2) in self.mappings if w2 == warp]  # if arg was a destination
        destination = [w2 for (w1, w2) in self.mappings if w1 == warp]  # if arg was a source
        return [*source, *destination, None][0]  # Assume mappings contains every warp at most once, return None if both lists are empty.


    def get_unmapped_warps(self) -> list[str]:
        unmapped_warps = warp_platforms.copy()
        for (w1, w2) in self.mappings:
            unmapped_warps.remove(w1)
            unmapped_warps.remove(w2)
        return unmapped_warps


    def apply_warp_plando(self, connections: dict[str, str]):
        unmapped_warps = self.get_unmapped_warps()
        for w1, w2 in connections.items():
            if w1 in self.dead_end_platforms and w2 in self.dead_end_platforms:
                raise OptionError(f"Error while processing warp plando: Trying to connect 2 dead ends ({w1} - {w2})")
            if w1 == w2:
                raise OptionError(f"Error while processing warp plando: Trying to connect {w1} to itself.")
            # Remove any existing connection (ie vanilla warp).
            connections_to_remove = []
            for warp_to_disconnect in (w1, w2):
                for (wm1, wm2) in self.mappings:
                    if wm1 == warp_to_disconnect or wm2 == warp_to_disconnect:
                        connections_to_remove.append((wm1, wm2))
            for connection in connections_to_remove:
                self.mappings.remove(connection)
                unmapped_warps.extend(connection)

            self.mappings.append((w1, w2))
            unmapped_warps.remove(w1)
            unmapped_warps.remove(w2)


    def apply_ac_modifications(self, random: Random) -> None:
        unmapped_warps = self.get_unmapped_warps()
        # Astral Codec requires a shipless warp path from the Hourglass Twins to Timber Hearth.
        # For simplicity, we connect HGT to TH directly, only randomizing which HGT pad gets used.

        if "TH" not in unmapped_warps:
            if self.shipless_connection_exists("Hourglass Twins", "Timber Hearth"):
                return # Connection already exists via plando or vanilla mapping.
            raise OptionError("Astral Codec requires Hourglass Twins to be connected to Timber Hearth, but TH is connected to somewhere else.")

        available_hgt_platforms = [w for w in unmapped_warps if warp_platform_to_logical_region[w] == "Hourglass Twins"]
        if len(available_hgt_platforms) == 0:
            raise OptionError("Astral Codec requires Hourglass Twins to be connected to Timber Hearth, but all HGT warps are connected to somewhere else.")
        hgt_platform = random.choice(available_hgt_platforms)
        self.mappings.append(("TH", hgt_platform))


    def apply_eh_modifications(self) -> None:
        self.dead_end_platforms.remove("BHF")
        bh_connections = self.itemless_warp_region_connections.get("Brittle Hollow")
        if bh_connections:
            bh_connections.add("Hanging City Ceiling")

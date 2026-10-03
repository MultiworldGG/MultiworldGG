from .bases import PokemonCrystalTestBase

from ..data import data
from ..entrance_rando import base_category, build_reverse_conn_lookup
from ..rom import _resolve_arrival, write_entrance_pairings


def _simulate_elevator_writes(world):
    """Run write_entrance_pairings and capture {(label, offset): (warp, group, map)} for elevator labels."""
    elev_addrs = {}
    for conn in data.entrance_connections.values():
        for ew in conn.exit_warps:
            if ew.label and ew.label.startswith("AP_ElevFloor_"):
                base = data.rom_addresses.get(ew.label)
                if base is not None:
                    elev_addrs[base + ew.addr_offset] = (ew.label, ew.addr_offset)

    writes: dict[tuple[str, int], tuple[int, int, int]] = {}

    def capture(byte_values, address):
        if address in elev_addrs:
            writes[elev_addrs[address]] = tuple(byte_values)

    write_entrance_pairings(world, capture)
    return writes


def _lift_entry_failures(world):
    """Return doors that land in a lift room but whose origin matches no floor's entry map (offset 4)."""
    conns = data.entrance_connections
    reverse_lookup = build_reverse_conn_lookup(conns)
    map_consts = data.map_constants
    resolve = lambda tgt: _resolve_arrival(conns, map_consts, reverse_lookup, tgt)
    lift_maps = {map_consts[k] for k in map_consts if k.endswith("_DEPT_STORE_ELEVATOR")}
    writes = _simulate_elevator_writes(world)

    label_lift = {}
    for conn in conns.values():
        if base_category(conn.category) == "Elevator" and "ELEVATOR:" in conn.entrance_region:
            lift = map_consts.get(conn.arrival_map_const)
            for ew in conn.exit_warps:
                if ew.label and ew.addr_offset == 4 and lift is not None:
                    label_lift[ew.label] = lift

    entry_maps: dict[tuple[int, int], set] = {}
    for (label, off), v in writes.items():
        if off == 4 and label in label_lift:
            entry_maps.setdefault(label_lift[label], set()).add(v[1:])

    failures = []
    for source_name, target_name in world.er_pairings:
        arrival = resolve(target_name)
        if arrival is None or arrival[1:] not in lift_maps:
            continue
        origin = resolve(source_name)
        cands = entry_maps.get(arrival[1:], set())
        if origin is None or origin[1:] not in cands:
            failures.append((source_name, target_name, origin[1:] if origin else None, sorted(cands)))
    return failures


def _get_elevator_labels():
    """Return all AP_ElevFloor_* labels from entrance_data."""
    labels: set[str] = set()
    for conn in data.entrance_connections.values():
        if base_category(conn.category) == "Elevator":
            for ew in conn.exit_warps:
                if ew.label and ew.label.startswith("AP_ElevFloor_"):
                    labels.add(ew.label)
    return sorted(labels)


def _get_elevator_conn_names():
    """Return (forward_names, reverse_names) sets for elevator connections."""
    forward = set()  # "Floor -> Elevator:NF" connections
    reverse = set()  # "Elevator:NF -> Floor" connections
    for name, conn in data.entrance_connections.items():
        if base_category(conn.category) != "Elevator":
            continue
        if "ELEVATOR:" in conn.entrance_region:
            forward.add(name)
        elif "ELEVATOR:" in conn.exit_region:
            reverse.add(name)
    return forward, reverse


class ElevatorConnectionStructureTest(PokemonCrystalTestBase):
    """Verify elevator connections in entrance_data have the correct format."""
    auto_construct = False

    def test_forward_patches_floor_warp_and_entry_map(self):
        """Forward (Floor -> Elevator:NF) should patch the floor warp_event and elevfloor entry map (offset 4)."""
        for name, conn in data.entrance_connections.items():
            if base_category(conn.category) != "Elevator" or "ELEVATOR:" not in conn.entrance_region:
                continue
            regular_warps = [ew for ew in conn.exit_warps if ew.label is None]
            elev_warps = [ew for ew in conn.exit_warps if ew.label is not None]
            self.assertGreaterEqual(len(regular_warps), 1, f"{name}: expected at least 1 regular warp")
            for ew in regular_warps:
                self.assertEqual(ew.addr_offset, 2, f"{name}: regular warp addr_offset should be 2")
            self.assertEqual(len(elev_warps), 1, f"{name}: expected 1 elevfloor warp")
            self.assertEqual(elev_warps[0].addr_offset, 4, f"{name}: elevfloor addr_offset should be 4")

    def test_reverse_patches_exit_map(self):
        """Reverse (Elevator:NF -> Floor) should patch elevfloor exit map (offset 1)."""
        for name, conn in data.entrance_connections.items():
            if base_category(conn.category) != "Elevator" or "ELEVATOR:" not in conn.exit_region:
                continue
            self.assertEqual(len(conn.exit_warps), 1, f"{name}: expected 1 exit_warp")
            self.assertEqual(conn.exit_warps[0].addr_offset, 1, f"{name}: addr_offset should be 1")

    def test_forward_arrival_points_to_elevator_room(self):
        """Forward connection arrival should point to the elevator room."""
        elevator_rooms = {"CeladonDeptStoreElevator", "GoldenrodDeptStoreElevator"}
        for name, conn in data.entrance_connections.items():
            if base_category(conn.category) != "Elevator" or "ELEVATOR:" not in conn.entrance_region:
                continue
            self.assertIn(conn.arrival_map, elevator_rooms,
                          f"{name}: arrival should be elevator room, got {conn.arrival_map}")

    def test_forward_and_reverse_share_label(self):
        """Forward and reverse for the same floor should patch the same AP_ElevFloor label."""
        labels_by_floor: dict[str, set[str]] = {}
        for conn in data.entrance_connections.values():
            if base_category(conn.category) != "Elevator":
                continue
            for ew in conn.exit_warps:
                if ew.label and ew.label.startswith("AP_ElevFloor_"):
                    labels_by_floor.setdefault(ew.label, set()).add(conn.name)
        for label, conn_names in labels_by_floor.items():
            self.assertEqual(len(conn_names), 2,
                             f"{label}: expected 2 connections, got {conn_names}")


class ElevatorERCoupledTest(PokemonCrystalTestBase):
    options = {
        "randomize_entrances": ["Elevator", "Building"],
        "coupled_entrances": True,
    }

    def test_both_directions_appear_as_source(self):
        """Both forward and reverse elevator connections should appear as pairing sources."""
        forward_names, reverse_names = _get_elevator_conn_names()
        sources = {src for src, _ in self.world.er_pairings}
        for name in forward_names:
            self.assertIn(name, sources, f"Forward '{name}' not in pairing sources")
        for name in reverse_names:
            self.assertIn(name, sources, f"Reverse '{name}' not in pairing sources")

    def test_all_elevator_labels_patched(self):
        """Every elevator label should have both exit (offset 1) and entry (offset 4) writes."""
        writes = _simulate_elevator_writes(self.world)
        for label in _get_elevator_labels():
            self.assertIn((label, 1), writes, f"No exit write (offset 1) for {label}")
            self.assertIn((label, 4), writes, f"No entry write (offset 4) for {label}")

    def test_every_lift_entry_matches_a_floor(self):
        """Every door landing in a lift room must match a floor's entry map."""
        failures = _lift_entry_failures(self.world)
        self.assertEqual(failures, [],
                         f"{len(failures)} lift entries match no floor entry map: {failures[:3]}")


class ElevatorERDecoupledTest(PokemonCrystalTestBase):
    options = {
        "randomize_entrances": ["Elevator", "Building"],
        "coupled_entrances": False,
    }

    def test_decoupled_generates(self):
        """Decoupled ER with elevators should generate without errors."""
        self.assertTrue(len(self.world.er_pairings) > 0)

    def test_all_elevator_labels_patched(self):
        """Every elevator label should have both exit and entry writes."""
        writes = _simulate_elevator_writes(self.world)
        for label in _get_elevator_labels():
            self.assertIn((label, 1), writes, f"No exit write (offset 1) for {label}")
            self.assertIn((label, 4), writes, f"No entry write (offset 4) for {label}")

    def test_every_lift_entry_matches_a_floor(self):
        """Every door landing in a lift room must match a floor's entry map."""
        failures = _lift_entry_failures(self.world)
        self.assertEqual(failures, [],
                         f"{len(failures)} lift entries match no floor entry map: {failures[:3]}")

import unittest
from unittest.mock import MagicMock

from ..client import (
    PokemonCrystalClient,
    SYNC_EVENT_FLAGS,
    SYNC_EVENTS_FLAG_MAP,
    EVENT_BYTES,
    detect_sync_events,
    encode_sync_bitfield,
    apply_remote_sync_events,
    compute_gym_count,
)
from ..data import data


def make_ctx(team=0, slot=1, items_handling=0b010):
    ctx = MagicMock()
    ctx.team = team
    ctx.slot = slot
    ctx.items_handling = items_handling
    return ctx


def make_client():
    client = PokemonCrystalClient()
    client.initialize_client()
    return client


def sync_key(team=0, slot=1):
    return f"pokemon_crystal_sync_events_{team}_{slot}"


def flag_bytes_with_events(event_names):
    """Build flag bytes with the given event names set."""
    fb = bytearray(EVENT_BYTES)
    for name in event_names:
        eid = data.event_flags[name]
        fb[eid // 8] |= 1 << (eid % 8)
    return fb


class TestSyncEventsFlagData(unittest.TestCase):
    """Validates that SYNC_EVENT_FLAGS and SYNC_EVENTS_FLAG_MAP are well-formed."""

    def test_all_sync_events_exist_in_data(self):
        for event_name in SYNC_EVENT_FLAGS:
            self.assertIn(event_name, data.event_flags)

    def test_flag_map_round_trips(self):
        for event_name in SYNC_EVENT_FLAGS:
            event_id = data.event_flags[event_name]
            self.assertEqual(SYNC_EVENTS_FLAG_MAP[event_id], event_name)

    def test_no_duplicate_event_ids(self):
        event_ids = [data.event_flags[e] for e in SYNC_EVENT_FLAGS]
        self.assertEqual(len(event_ids), len(set(event_ids)))

    def test_no_duplicate_event_names(self):
        self.assertEqual(len(SYNC_EVENT_FLAGS), len(set(SYNC_EVENT_FLAGS)))

    def test_event_ids_fit_in_event_bytes(self):
        for event_name in SYNC_EVENT_FLAGS:
            self.assertLess(data.event_flags[event_name] // 8, EVENT_BYTES)

    def test_first_16_are_gym_leaders(self):
        for flag in SYNC_EVENT_FLAGS[:16]:
            self.assertTrue(flag.startswith("EVENT_BEAT_"), f"{flag} is not a gym event")

    def test_exactly_16_gym_events(self):
        gym_events = [f for f in SYNC_EVENT_FLAGS if f.startswith("EVENT_BEAT_")]
        self.assertEqual(len(gym_events), 16)


class TestDetectSyncEvents(unittest.TestCase):

    def test_empty_flags(self):
        result = detect_sync_events(bytearray(EVENT_BYTES))
        self.assertTrue(all(not v for v in result.values()))

    def test_single_event(self):
        for event_name in SYNC_EVENT_FLAGS:
            result = detect_sync_events(flag_bytes_with_events([event_name]))
            self.assertTrue(result[event_name], f"{event_name} should be detected")
            others_set = [e for e in SYNC_EVENT_FLAGS if e != event_name and result[e]]
            self.assertEqual(others_set, [], f"Only {event_name} should be set")

    def test_multiple_events(self):
        events = ["EVENT_BEAT_FALKNER", "EVENT_BEAT_CLAIR", "EVENT_CLEARED_RADIO_TOWER"]
        result = detect_sync_events(flag_bytes_with_events(events))
        for e in events:
            self.assertTrue(result[e])

    def test_non_sync_event_ignored(self):
        """An event flag that isn't a sync event shouldn't appear in results."""
        non_sync = next(
            name for name, eid in data.event_flags.items()
            if name not in SYNC_EVENT_FLAGS and eid not in SYNC_EVENTS_FLAG_MAP
        )
        result = detect_sync_events(flag_bytes_with_events([non_sync]))
        self.assertTrue(all(not v for v in result.values()))


class TestEncodeSyncBitfield(unittest.TestCase):

    def test_no_events(self):
        events = {flag: False for flag in SYNC_EVENT_FLAGS}
        self.assertEqual(encode_sync_bitfield(events), 0)

    def test_all_events(self):
        events = {flag: True for flag in SYNC_EVENT_FLAGS}
        self.assertEqual(encode_sync_bitfield(events), (1 << len(SYNC_EVENT_FLAGS)) - 1)

    def test_single_event_bit_position(self):
        for i, flag in enumerate(SYNC_EVENT_FLAGS):
            events = {f: (f == flag) for f in SYNC_EVENT_FLAGS}
            self.assertEqual(encode_sync_bitfield(events), 1 << i)

    def test_gym_leaders_fill_low_16_bits(self):
        events = {f: (i < 16) for i, f in enumerate(SYNC_EVENT_FLAGS)}
        self.assertEqual(encode_sync_bitfield(events), 0xFFFF)


class TestApplyRemoteSyncEvents(unittest.TestCase):

    def test_zero_bitfield_no_change(self):
        base = bytearray(EVENT_BYTES)
        self.assertEqual(apply_remote_sync_events(base, 0), base)

    def test_sets_correct_flag_byte(self):
        for i, event_name in enumerate(SYNC_EVENT_FLAGS):
            result = apply_remote_sync_events(bytearray(EVENT_BYTES), 1 << i)
            eid = data.event_flags[event_name]
            self.assertTrue(result[eid // 8] & (1 << (eid % 8)),
                            f"{event_name} not set")

    def test_preserves_existing_flags(self):
        base = bytearray(EVENT_BYTES)
        base[0] = 0xFF
        result = apply_remote_sync_events(base, 1)
        self.assertEqual(result[0], 0xFF, "Existing flags should be preserved")

    def test_all_events(self):
        all_bits = (1 << len(SYNC_EVENT_FLAGS)) - 1
        result = apply_remote_sync_events(bytearray(EVENT_BYTES), all_bits)
        for event_name in SYNC_EVENT_FLAGS:
            eid = data.event_flags[event_name]
            self.assertTrue(result[eid // 8] & (1 << (eid % 8)), f"{event_name} not set")

    def test_does_not_mutate_input(self):
        base = bytearray(EVENT_BYTES)
        original = bytes(base)
        apply_remote_sync_events(base, (1 << len(SYNC_EVENT_FLAGS)) - 1)
        self.assertEqual(bytes(base), original)


class TestComputeGymCount(unittest.TestCase):

    def test_no_gyms(self):
        self.assertEqual(compute_gym_count(bytearray(EVENT_BYTES)), 0)

    def test_all_16_gyms(self):
        synced = apply_remote_sync_events(bytearray(EVENT_BYTES), 0xFFFF)
        self.assertEqual(compute_gym_count(synced), 16)

    def test_johto_only(self):
        synced = apply_remote_sync_events(bytearray(EVENT_BYTES), 0xFF)
        self.assertEqual(compute_gym_count(synced), 8)

    def test_kanto_only(self):
        synced = apply_remote_sync_events(bytearray(EVENT_BYTES), 0xFF00)
        self.assertEqual(compute_gym_count(synced), 8)

    def test_non_gym_events_dont_count(self):
        non_gym_bits = ((1 << len(SYNC_EVENT_FLAGS)) - 1) & ~0xFFFF
        synced = apply_remote_sync_events(bytearray(EVENT_BYTES), non_gym_bits)
        self.assertEqual(compute_gym_count(synced), 0)

    def test_single_gym(self):
        for i in range(16):
            synced = apply_remote_sync_events(bytearray(EVENT_BYTES), 1 << i)
            self.assertEqual(compute_gym_count(synced), 1,
                             f"{SYNC_EVENT_FLAGS[i]} should count as 1 gym")


class TestRoundTrip(unittest.TestCase):
    """Encode -> decode round-trips preserve event data."""

    def test_all_events_round_trip(self):
        fb = flag_bytes_with_events(SYNC_EVENT_FLAGS)
        detected = detect_sync_events(fb)
        bitfield = encode_sync_bitfield(detected)
        decoded = apply_remote_sync_events(bytearray(EVENT_BYTES), bitfield)

        for event_name in SYNC_EVENT_FLAGS:
            eid = data.event_flags[event_name]
            self.assertTrue(decoded[eid // 8] & (1 << (eid % 8)),
                            f"Round-trip lost {event_name}")

    def test_subset_round_trip(self):
        subset = ["EVENT_BEAT_FALKNER", "EVENT_CLEARED_ROCKET_HIDEOUT", "EVENT_RELEASED_THE_BEASTS"]
        fb = flag_bytes_with_events(subset)
        detected = detect_sync_events(fb)
        bitfield = encode_sync_bitfield(detected)
        decoded = apply_remote_sync_events(bytearray(EVENT_BYTES), bitfield)

        re_detected = detect_sync_events(decoded)
        for event in SYNC_EVENT_FLAGS:
            self.assertEqual(re_detected[event], event in subset,
                             f"Round-trip mismatch for {event}")


class TestOnPackageRetrievedSyncEvents(unittest.TestCase):

    def test_sets_remote_sync_events(self):
        client = make_client()
        client.on_package(make_ctx(), "Retrieved", {"keys": {sync_key(): 0b10101}})
        self.assertEqual(client.remote_sync_events, 0b10101)

    def test_none_value_defaults_to_zero(self):
        client = make_client()
        client.on_package(make_ctx(), "Retrieved", {"keys": {sync_key(): None}})
        self.assertEqual(client.remote_sync_events, 0)

    def test_missing_key_leaves_default(self):
        client = make_client()
        client.on_package(make_ctx(), "Retrieved", {"keys": {"unrelated_key": 42}})
        self.assertEqual(client.remote_sync_events, 0)

    def test_ignores_when_items_handling_disabled(self):
        client = make_client()
        client.on_package(make_ctx(items_handling=0b000), "Retrieved", {"keys": {sync_key(): 0xFF}})
        self.assertEqual(client.remote_sync_events, 0)

    def test_uses_team_and_slot_in_key(self):
        client = make_client()
        client.on_package(make_ctx(team=3, slot=7), "Retrieved", {"keys": {sync_key(3, 7): 99}})
        self.assertEqual(client.remote_sync_events, 99)

    def test_wrong_team_slot_ignored(self):
        client = make_client()
        client.on_package(make_ctx(team=0, slot=1), "Retrieved", {"keys": {sync_key(0, 2): 99}})
        self.assertEqual(client.remote_sync_events, 0)


class TestOnPackageSetReplySyncEvents(unittest.TestCase):

    def test_sets_remote_sync_events(self):
        client = make_client()
        client.on_package(make_ctx(), "SetReply", {"key": sync_key(), "value": 0xBEEF})
        self.assertEqual(client.remote_sync_events, 0xBEEF)

    def test_missing_value_defaults_to_zero(self):
        client = make_client()
        client.on_package(make_ctx(), "SetReply", {"key": sync_key()})
        self.assertEqual(client.remote_sync_events, 0)

    def test_wrong_key_ignored(self):
        client = make_client()
        client.on_package(make_ctx(), "SetReply", {"key": "pokemon_crystal_sync_events_0_99", "value": 123})
        self.assertEqual(client.remote_sync_events, 0)

    def test_overwrites_previous_value(self):
        client = make_client()
        ctx = make_ctx()
        client.on_package(ctx, "SetReply", {"key": sync_key(), "value": 0xFF})
        client.on_package(ctx, "SetReply", {"key": sync_key(), "value": 0x01})
        self.assertEqual(client.remote_sync_events, 0x01)


class TestClientSyncEventInit(unittest.TestCase):

    def test_initial_local_sync_events_empty(self):
        self.assertEqual(make_client().local_sync_events, {})

    def test_initial_remote_sync_events_zero(self):
        self.assertEqual(make_client().remote_sync_events, 0)

    def test_reinitialize_resets_state(self):
        client = make_client()
        client.remote_sync_events = 0xFFFF
        client.local_sync_events = {"foo": True}
        client.initialize_client()
        self.assertEqual(client.remote_sync_events, 0)
        self.assertEqual(client.local_sync_events, {})

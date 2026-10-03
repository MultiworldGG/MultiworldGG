import json
import unittest

from ..util_wonder_trade import (
    PARTY_MON_LENGTH,
    NICK_LENGTH,
    OT_LENGTH,
    MON_SPECIES,
    MON_LEVEL,
    MON_DVS,
    MON_MOVES,
    MON_ID,
    pokemon_data_to_json,
    json_to_pokemon_data,
    trade_is_eligible,
)


def make_mon(species=25, level=20, dvs=0xABCD, moves=(33, 84, 0, 0),
             pps=(35 | (1 << 6), 30, 0, 0), exp=125000, trainer_id=0x1234) -> bytes:
    mon = bytearray(PARTY_MON_LENGTH)
    mon[MON_SPECIES] = species
    for i, m in enumerate(moves):
        mon[MON_MOVES + i] = m
    mon[MON_ID:MON_ID + 2] = trainer_id.to_bytes(2, "big")
    mon[8:11] = exp.to_bytes(3, "big")
    for i in range(5):
        mon[11 + i * 2:13 + i * 2] = (5000 * (i + 1)).to_bytes(2, "big")
    mon[MON_DVS:MON_DVS + 2] = dvs.to_bytes(2, "big")
    for i, pp in enumerate(pps):
        mon[23 + i] = pp
    mon[MON_LEVEL] = level
    mon[29:31] = bytes([level, 14])  # caught level, caught location
    return bytes(mon)


def make_nick(text="PIKACHU") -> bytes:
    out = bytearray()
    for ch in text:
        out.append(0x80 + (ord(ch) - ord("A")))
    out.append(0x50)
    while len(out) < NICK_LENGTH:
        out.append(0x50)
    return bytes(out[:NICK_LENGTH])


def make_ot(text="ASH") -> bytes:
    out = bytearray()
    for ch in text:
        out.append(0x80 + (ord(ch) - ord("A")))
    out.append(0x50)
    while len(out) < OT_LENGTH:
        out.append(0x50)
    return bytes(out[:OT_LENGTH])


class TestWonderTradeRoundTrip(unittest.TestCase):
    def test_crystal_through_pool_back_to_crystal_lossless(self):
        original_dvs = 0xABCD  # nibbles A,B,C,D
        mon = make_mon(species=25, level=20, dvs=original_dvs)
        blob = pokemon_data_to_json(mon, make_nick("PIKACHU"), make_ot("ASH"),
                                    trainer_id=0x1234, player_female=False)

        decoded = json_to_pokemon_data(blob)
        round_dvs = int.from_bytes(decoded["party_mon"][MON_DVS:MON_DVS + 2], "big")
        self.assertEqual(round_dvs, original_dvs)

        self.assertEqual(decoded["party_mon"][MON_SPECIES], 25)
        self.assertEqual(decoded["nickname"][:7], make_nick("PIKACHU")[:7])

    def test_json_schema_contains_required_fields(self):
        mon = make_mon()
        blob = pokemon_data_to_json(mon, make_nick(), make_ot(),
                                    trainer_id=0x1234, player_female=True)
        payload = json.loads(blob)
        for key in ("version", "species", "experience", "ivs", "evs", "moves",
                    "trainer", "nickname", "language", "ability", "conditions",
                    "pokerus", "location_met", "level_met", "game", "ball"):
            self.assertIn(key, payload)
        self.assertEqual(len(payload["ivs"]), 6)
        self.assertEqual(len(payload["evs"]), 6)
        self.assertEqual(len(payload["moves"]), 4)
        self.assertTrue(payload["trainer"]["female"])

    def test_iv_scaling(self):
        # DV=15 → IV=31; DV=0 → IV=1 with our IV=DV*2+1 convention
        for nib in (0, 7, 15):
            dvs = (nib << 12) | (nib << 8) | (nib << 4) | nib
            blob = pokemon_data_to_json(make_mon(dvs=dvs), make_nick(), make_ot(),
                                        trainer_id=1, player_female=False)
            payload = json.loads(blob)
            self.assertEqual(payload["ivs"][1], nib * 2 + 1)  # Atk
            self.assertEqual(payload["ivs"][2], nib * 2 + 1)  # Def
            self.assertEqual(payload["ivs"][3], nib * 2 + 1)  # Spe
            self.assertEqual(payload["ivs"][4], nib * 2 + 1)  # SpA
            self.assertEqual(payload["ivs"][5], nib * 2 + 1)  # SpD


class TestWonderTradeFallbacks(unittest.TestCase):
    def test_species_above_crystal_range_becomes_unown(self):
        blob = json.dumps({
            "version": "1", "species": 386, "experience": 0, "ivs": [0] * 6,
            "evs": [0] * 6, "moves": [[33, 35, 0]] * 4,
            "trainer": {"name": "X", "id": 1, "female": False},
            "nickname": "BAD", "language": "English", "level_met": 5,
        })
        decoded = json_to_pokemon_data(blob)
        self.assertEqual(decoded["party_mon"][MON_SPECIES], 201)

    def test_gen3_moves_are_dropped_and_remaining_compacted(self):
        blob = json.dumps({
            "version": "1", "species": 25, "experience": 0, "ivs": [0] * 6,
            "evs": [0] * 6,
            "moves": [[33, 35, 0], [350, 5, 0], [400, 5, 0], [84, 30, 0]],
            "trainer": {"name": "X", "id": 1, "female": False},
            "nickname": "PK", "language": "English", "level_met": 5,
        })
        decoded = json_to_pokemon_data(blob)
        moves = decoded["party_mon"][MON_MOVES:MON_MOVES + 4]
        # 33 + 84 survive; Gen3 350/400 dropped; trailing slots zeroed.
        self.assertEqual(moves[0], 33)
        self.assertEqual(moves[1], 84)
        self.assertEqual(moves[2], 0)
        self.assertEqual(moves[3], 0)

    def test_location_met_uses_in_game_trade_sentinel_outbound(self):
        # A Crystal mon caught at LANDMARK_ROUTE_29 (=2) should not serialize
        # location_met=2, because foreign games would render that as some
        # unrelated location (e.g. Dewford Town in Gen3).
        mon = make_mon()
        # Force caught location byte to 2 (Route 29).
        mon = bytearray(mon)
        mon[30] = 2
        blob = pokemon_data_to_json(bytes(mon), make_nick(), make_ot(),
                                    trainer_id=1, player_female=False)
        payload = json.loads(blob)
        self.assertEqual(payload["location_met"], 0xFE)  # METLOC_IN_GAME_TRADE

    def test_inbound_caught_location_becomes_gift_landmark(self):
        # Any inbound location_met (Hoenn, fateful, whatever) becomes
        # Crystal's LANDMARK_GIFT (0x7E) so the summary screen reads
        # "an apparently kind trainer".
        blob = json.dumps({
            "version": "1", "species": 25, "experience": 0, "ivs": [0] * 6,
            "evs": [0] * 6, "moves": [[33, 35, 0]] * 4,
            "trainer": {"name": "X", "id": 1, "female": False},
            "nickname": "PK", "language": "English",
            "level_met": 10, "location_met": 42,
        })
        decoded = json_to_pokemon_data(blob)
        # Byte at MON_CAUGHTDATA+1: high bit is gender, low 7 bits are landmark
        self.assertEqual(decoded["party_mon"][30] & 0x7F, 0x7E)

    def test_held_item_mapped_outbound_and_inbound(self):
        # Crystal Leftovers (id 134) maps to the pool's Leftovers id (200).
        mon = bytearray(make_mon())
        mon[1] = 134
        blob = pokemon_data_to_json(bytes(mon), make_nick(), make_ot(),
                                    trainer_id=1, player_female=False)
        payload = json.loads(blob)
        self.assertEqual(payload["item"], 200)

        # And back: JSON carrying pool Leftovers id 200 deserializes to
        # Crystal Leftovers id 134.
        payload["nickname"] = "X"
        payload["trainer"] = {"name": "X", "id": 1, "female": False}
        payload["language"] = "English"
        payload["level_met"] = 5
        decoded = json_to_pokemon_data(json.dumps(payload))
        self.assertEqual(decoded["party_mon"][1], 134)

    def test_tm_maps_by_slot_number(self):
        # Crystal TM_1 (item 198) → pool TM01 (289).
        mon = bytearray(make_mon())
        mon[1] = 198
        blob = pokemon_data_to_json(bytes(mon), make_nick(), make_ot(),
                                    trainer_id=1, player_female=False)
        self.assertEqual(json.loads(blob)["item"], 289)
        # Reverse: pool TM50 (338) → Crystal TM_50 (247).
        payload = json.loads(blob)
        payload["item"] = 338
        payload["nickname"] = "X"
        payload["trainer"] = {"name": "X", "id": 1, "female": False}
        payload["language"] = "English"
        payload["level_met"] = 5
        decoded = json_to_pokemon_data(json.dumps(payload))
        self.assertEqual(decoded["party_mon"][1], 247)

    def test_held_item_unknown_in_other_game_is_stripped(self):
        # Crystal MIRACLEBERRY (no pool equivalent in our map) → no item field.
        mon = bytearray(make_mon())
        mon[1] = 66  # MIRACLEBERRY
        blob = pokemon_data_to_json(bytes(mon), make_nick(), make_ot(),
                                    trainer_id=1, player_female=False)
        payload = json.loads(blob)
        self.assertNotIn("item", payload)

    def test_all_gen3_moves_fall_back_to_razor_wind(self):
        blob = json.dumps({
            "version": "1", "species": 25, "experience": 0, "ivs": [0] * 6,
            "evs": [0] * 6,
            "moves": [[300, 5, 0], [350, 5, 0], [400, 5, 0], [320, 5, 0]],
            "trainer": {"name": "X", "id": 1, "female": False},
            "nickname": "PK", "language": "English", "level_met": 5,
        })
        decoded = json_to_pokemon_data(blob)
        moves = decoded["party_mon"][MON_MOVES:MON_MOVES + 4]
        self.assertEqual(moves[0], 13)  # Razor Wind
        self.assertEqual(moves[1], 0)
        self.assertEqual(moves[2], 0)
        self.assertEqual(moves[3], 0)


class TestEligibilityFilter(unittest.TestCase):
    def _make_pool_entry(self, slot, species=25, moves=((33, 35, 0),) * 4):
        return [slot, json.dumps({
            "version": "1", "species": species, "experience": 0, "ivs": [0] * 6,
            "evs": [0] * 6, "moves": list(moves),
            "trainer": {"name": "X", "id": 1, "female": False},
            "nickname": "PK", "language": "English", "level_met": 5,
        })]

    def test_rejects_own_id(self):
        self.assertFalse(trade_is_eligible(self._make_pool_entry(slot=7), own_id=7))

    def test_rejects_gen3_species(self):
        self.assertFalse(trade_is_eligible(self._make_pool_entry(slot=1, species=386), own_id=7))

    def test_rejects_all_gen3_moves(self):
        gen3 = [(400, 5, 0)] * 4
        self.assertFalse(trade_is_eligible(self._make_pool_entry(slot=1, moves=gen3), own_id=7))

    def test_accepts_partial_overlap(self):
        moves = [(33, 35, 0), (400, 5, 0), (400, 5, 0), (400, 5, 0)]
        self.assertTrue(trade_is_eligible(self._make_pool_entry(slot=1, moves=moves), own_id=7))

    def test_foreign_slot_entry_accepted_when_no_id_collision(self):
        # An Emerald-style entry (small slot int as identity field) is fine
        # as long as it doesn't coincidentally match our TID.
        self.assertTrue(trade_is_eligible(self._make_pool_entry(slot=1), own_id=0x1234))

    def test_foreign_slot_entry_rejected_on_id_collision(self):
        # If our TID happens to equal a foreign slot id, we reject as self.
        # ~0.015% per Emerald entry in practice; documented collision.
        self.assertFalse(trade_is_eligible(self._make_pool_entry(slot=1), own_id=1))


class TestWonderTradeSendFinally(unittest.IsolatedAsyncioTestCase):
    """Regression: wonder_trade_in_flight must clear when posting fails so the
    next offer can post."""

    async def test_in_flight_clears_when_acquire_returns_none(self):
        from worlds.pokemon_crystal.client import PokemonCrystalClient

        # Hand-roll just enough of the client to exercise wonder_trade_send's
        # try/finally without bringing up the full BizHawk stack.
        client = PokemonCrystalClient.__new__(PokemonCrystalClient)
        client.wonder_trade_in_flight = True

        async def fake_acquire(ctx, keep_trying=False):
            return None

        client.wonder_trade_acquire = fake_acquire
        await client.wonder_trade_send(ctx=None, blob="{}", own_tid=0)
        self.assertFalse(client.wonder_trade_in_flight)

    async def test_in_flight_clears_when_acquire_raises(self):
        from worlds.pokemon_crystal.client import PokemonCrystalClient

        client = PokemonCrystalClient.__new__(PokemonCrystalClient)
        client.wonder_trade_in_flight = True

        async def boom(ctx, keep_trying=False):
            raise RuntimeError("connection lost")

        client.wonder_trade_acquire = boom
        with self.assertRaises(RuntimeError):
            await client.wonder_trade_send(ctx=None, blob="{}", own_tid=0)
        self.assertFalse(client.wonder_trade_in_flight)


if __name__ == "__main__":
    unittest.main()

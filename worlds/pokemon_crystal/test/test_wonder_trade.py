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

    def test_level_met_strips_caught_time_bits(self):
        mon = bytearray(make_mon())
        for caught_time in range(4):
            with self.subTest(caught_time=caught_time):
                mon[29] = (caught_time << 6) | 5
                blob = pokemon_data_to_json(bytes(mon), make_nick(), make_ot(),
                                            trainer_id=1, player_female=False)
                self.assertEqual(json.loads(blob)["level_met"], 5)

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

    def test_rejects_malformed_entries_without_raising(self):
        good = json.loads(self._make_pool_entry(slot=1)[1])
        malformed = [
            "not json",
            json.dumps([1, 2, 3]),
            json.dumps({**good, "moves": [["tackle", 35, 0]]}),
            json.dumps({**good, "moves": [[33, 35, 0], [None, 1, 0]]}),
            json.dumps({**good, "experience": "lots"}),
            json.dumps({**good, "ivs": ["a"] * 6}),
            json.dumps({**good, "trainer": "X"}),
            None,
        ]
        for blob in malformed:
            with self.subTest(blob=blob):
                self.assertFalse(trade_is_eligible([1, blob], own_id=7))


class TestWonderTradeSendFinally(unittest.IsolatedAsyncioTestCase):
    """Regression: wonder_trade_in_flight must clear when posting fails so the
    next offer can post."""

    async def test_in_flight_clears_when_acquire_returns_none(self):
        from worlds.pokemon_crystal.client import PokemonCrystalClient

        # Hand-roll just enough of the client to exercise wonder_trade_send's
        # try/finally without bringing up the full BizHawk stack.
        client = PokemonCrystalClient.__new__(PokemonCrystalClient)
        client.wonder_trade_in_flight = True
        client.wonder_trade_send_token = None

        async def fake_acquire(ctx, keep_trying=False):
            return None

        client.wonder_trade_acquire = fake_acquire
        await client.wonder_trade_send(ctx=None, blob="{}", own_tid=0, send_buffer=bytes(70), token=None)
        self.assertFalse(client.wonder_trade_in_flight)

    async def test_in_flight_clears_when_acquire_raises(self):
        from worlds.pokemon_crystal.client import PokemonCrystalClient

        client = PokemonCrystalClient.__new__(PokemonCrystalClient)
        client.wonder_trade_in_flight = True
        client.wonder_trade_send_token = None

        async def boom(ctx, keep_trying=False):
            raise RuntimeError("connection lost")

        client.wonder_trade_acquire = boom
        with self.assertRaises(RuntimeError):
            await client.wonder_trade_send(ctx=None, blob="{}", own_tid=0, send_buffer=bytes(70), token=None)
        self.assertFalse(client.wonder_trade_in_flight)


class TestWonderTradePostedMarker(unittest.IsolatedAsyncioTestCase):
    """Regression: a restarted client must not re-post a trade it already posted."""

    async def test_zeroed_species_is_not_reposted(self):
        from unittest.mock import AsyncMock, MagicMock, patch
        from worlds.pokemon_crystal.client import PokemonCrystalClient

        client = PokemonCrystalClient.__new__(PokemonCrystalClient)
        client.initialize_wonder_trade()
        client.wonder_trade_cooldown_timer = 1
        ctx = MagicMock(stored_data={}, watcher_timeout=0.1)
        send_blob = bytes(70)
        read = AsyncMock(return_value=[b"\xa5\x5a\xc3", b"\x01", send_blob, b"\x12\x34"])
        with patch("worlds._bizhawk.read", read), \
                patch("worlds.pokemon_crystal.client_wonder_trade.Utils.async_start") as async_start:
            await client.handle_wonder_trade(ctx)
        async_start.assert_not_called()
        self.assertTrue(client.wonder_trade_in_flight)


def _make_client():
    from worlds.pokemon_crystal.client import PokemonCrystalClient
    client = PokemonCrystalClient.__new__(PokemonCrystalClient)
    client.initialize_wonder_trade()
    return client


def _make_ctx(connected=True):
    from unittest.mock import AsyncMock, MagicMock
    ctx = MagicMock(team=0, stored_data={}, watcher_timeout=0.1)
    ctx.server.socket.open = connected
    ctx.server.socket.closed = not connected
    ctx.send_msgs = AsyncMock()
    ctx.exit_event.is_set.return_value = False
    return ctx


def _confirm_sets(client, ctx):
    async def reply(msgs):
        client.on_wonder_trade_reply({"uuid": msgs[0]["uuid"], "value": {"_lock": 0}, "original_value": {}})

    ctx.send_msgs.side_effect = reply


class TestWonderTradeSendMarker(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.client = _make_client()
        self.client.wonder_trade_in_flight = True
        self.client.wonder_trade_send_token = None

        async def fake_acquire(ctx, keep_trying=False):
            return {"value": {"_lock": 1}}

        self.client.wonder_trade_acquire = fake_acquire
        self.send_buffer = bytes([25]) + bytes(69)

    async def test_successful_post_zeroes_species_guarded_on_status_and_buffer(self):
        from unittest.mock import AsyncMock, patch
        from ..data import data

        ctx = _make_ctx()
        _confirm_sets(self.client, ctx)
        guarded_write = AsyncMock(return_value=True)
        with patch("worlds._bizhawk.guarded_write", guarded_write):
            await self.client.wonder_trade_send(ctx, "{}", 0x1234, self.send_buffer, None)

        ctx.send_msgs.assert_awaited_once()
        send_addr = data.sram_addresses["sArchipelagoWonderTradeSendBuffer"]
        status_addr = data.sram_addresses["sArchipelagoWonderTradeStatus"]
        _, writes, guards = guarded_write.await_args.args
        self.assertEqual(writes, [(send_addr, [0], "CartRAM")])
        self.assertIn((status_addr, [1], "CartRAM"), guards)
        self.assertIn((send_addr, self.send_buffer, "CartRAM"), guards)
        self.assertTrue(self.client.wonder_trade_in_flight)

    async def test_disconnected_post_is_retried_not_marked(self):
        from unittest.mock import AsyncMock, patch

        ctx = _make_ctx(connected=False)
        guarded_write = AsyncMock(return_value=True)
        with patch("worlds._bizhawk.guarded_write", guarded_write):
            await self.client.wonder_trade_send(ctx, "{}", 0x1234, self.send_buffer, None)

        ctx.send_msgs.assert_not_awaited()
        guarded_write.assert_not_awaited()
        self.assertFalse(self.client.wonder_trade_in_flight)

    async def test_unconfirmed_post_is_retried_not_marked(self):
        from unittest.mock import AsyncMock, patch

        ctx = _make_ctx()
        guarded_write = AsyncMock(return_value=True)
        with patch("worlds._bizhawk.guarded_write", guarded_write), \
                patch("worlds.pokemon_crystal.client_wonder_trade.REPLY_TIMEOUT_S", 0.01):
            await self.client.wonder_trade_send(ctx, "{}", 0x1234, self.send_buffer, None)

        ctx.send_msgs.assert_awaited_once()
        guarded_write.assert_not_awaited()
        self.assertFalse(self.client.wonder_trade_in_flight)
        self.assertEqual(self.client.wonder_trade_pending_replies, {})

    async def test_failed_marker_write_is_retried_by_watcher(self):
        from unittest.mock import AsyncMock, patch
        import worlds._bizhawk as bizhawk

        ctx = _make_ctx()
        _confirm_sets(self.client, ctx)
        with patch("worlds._bizhawk.guarded_write", AsyncMock(side_effect=bizhawk.RequestFailedError)):
            await self.client.wonder_trade_send(ctx, "{}", 0x1234, self.send_buffer, None)
        self.assertTrue(self.client.wonder_trade_in_flight)
        self.assertEqual(self.client.wonder_trade_unmarked_buffer, self.send_buffer)

        read = AsyncMock(return_value=[b"\xa5\x5a\xc3", b"\x01", self.send_buffer, b"\x12\x34"])
        guarded_write = AsyncMock(return_value=True)
        with patch("worlds._bizhawk.read", read), patch("worlds._bizhawk.guarded_write", guarded_write):
            await self.client.handle_wonder_trade(ctx)
        guarded_write.assert_awaited_once()
        self.assertIsNone(self.client.wonder_trade_unmarked_buffer)

    async def test_stale_task_does_not_clear_newer_in_flight(self):
        async def superseded_acquire(ctx, keep_trying=False):
            self.client.wonder_trade_send_token = object()
            return None

        self.client.wonder_trade_acquire = superseded_acquire
        await self.client.wonder_trade_send(_make_ctx(), "{}", 0x1234, self.send_buffer, None)
        self.assertTrue(self.client.wonder_trade_in_flight)

    async def test_handle_passes_full_send_buffer(self):
        from unittest.mock import AsyncMock, MagicMock, patch

        ctx = _make_ctx()
        client = _make_client()
        client.wonder_trade_send = MagicMock()
        send_blob = bytes([25]) + bytes(range(1, 70))
        read = AsyncMock(side_effect=[[b"\xa5\x5a\xc3", b"\x01", send_blob, b"\x12\x34"], [b"\x00"]])
        with patch("worlds._bizhawk.read", read), \
                patch("worlds.pokemon_crystal.client_wonder_trade.Utils.async_start"):
            await client.handle_wonder_trade(ctx)
        self.assertEqual(client.wonder_trade_send.call_args.args[3], send_blob)
        self.assertIs(client.wonder_trade_send.call_args.args[4], client.wonder_trade_send_token)


class TestWonderTradeMalformedPool(unittest.IsolatedAsyncioTestCase):
    async def test_non_dict_pool_is_ignored(self):
        from unittest.mock import AsyncMock, patch

        client = _make_client()
        client.wonder_trade_in_flight = True
        ctx = _make_ctx()
        ctx.stored_data = {"pokemon_wonder_trades_0": ["garbage"]}
        read = AsyncMock(return_value=[b"\xa5\x5a\xc3", b"\x01", bytes(70), b"\x12\x34"])
        with patch("worlds._bizhawk.read", read):
            await client.handle_wonder_trade(ctx)
        ctx.send_msgs.assert_not_awaited()

    async def test_acquire_tolerates_original_value_without_lock(self):
        client = _make_client()
        ctx = _make_ctx()

        async def reply(msgs):
            msg = msgs[0]
            lock = msg["operations"][0]["value"]["_lock"]
            client.on_wonder_trade_reply({"uuid": msg["uuid"], "value": {"_lock": lock}, "original_value": {}})

        ctx.send_msgs.side_effect = reply
        result = await client.wonder_trade_acquire(ctx)
        self.assertIsNotNone(result)
        self.assertEqual(client.wonder_trade_cooldown, 5000)


    async def test_acquire_tolerates_non_numeric_original_lock(self):
        client = _make_client()
        ctx = _make_ctx()

        async def reply(msgs):
            msg = msgs[0]
            lock = msg["operations"][0]["value"]["_lock"]
            client.on_wonder_trade_reply({"uuid": msg["uuid"], "value": {"_lock": lock},
                                          "original_value": {"_lock": "x"}})

        ctx.send_msgs.side_effect = reply
        self.assertIsNotNone(await client.wonder_trade_acquire(ctx))

    async def test_acquire_rejects_non_dict_value(self):
        client = _make_client()
        ctx = _make_ctx()

        async def reply(msgs):
            client.on_wonder_trade_reply({"uuid": msgs[0]["uuid"], "value": ["_lock"], "original_value": []})

        ctx.send_msgs.side_effect = reply
        self.assertIsNone(await client.wonder_trade_acquire(ctx))


class TestWonderTradeReplyMatching(unittest.IsolatedAsyncioTestCase):
    async def test_other_clients_replies_do_not_resolve_ours(self):
        from unittest.mock import patch

        client = _make_client()
        ctx = _make_ctx()

        async def reply(msgs):
            for foreign in ({"uuid": "someone-else"}, {}, {"uuid": ["unhashable"]}, {"uuid": None}):
                client.on_wonder_trade_reply({**foreign, "value": {"_lock": 0}})
            self.assertEqual(len(client.wonder_trade_pending_replies), 1)
            client.on_wonder_trade_reply({"uuid": msgs[0]["uuid"], "value": {"_lock": 7}})
            client.on_wonder_trade_reply({"uuid": "someone-else", "value": {"_lock": 0}})

        ctx.send_msgs.side_effect = reply
        with patch("worlds.pokemon_crystal.client_wonder_trade.REPLY_TIMEOUT_S", 1):
            result = await client._request_pool_update(ctx, [])
        self.assertEqual(result["value"], {"_lock": 7})
        self.assertEqual(client.wonder_trade_pending_replies, {})


class TestWonderTradeBackgroundReceive(unittest.IsolatedAsyncioTestCase):
    def _eligible_pool(self):
        entry = TestEligibilityFilter()._make_pool_entry(slot=1)
        return {"pokemon_wonder_trades_0": {"_lock": 0, "0": entry}}

    async def test_watcher_spawns_receive_without_awaiting_it(self):
        from unittest.mock import AsyncMock, MagicMock, patch

        client = _make_client()
        client.wonder_trade_in_flight = True
        client.wonder_trade_receive = AsyncMock()
        ctx = _make_ctx()
        ctx.stored_data = self._eligible_pool()
        read = AsyncMock(return_value=[b"\xa5\x5a\xc3", b"\x01", bytes(70), b"\x12\x34"])
        with patch("worlds._bizhawk.read", read), \
                patch("worlds.pokemon_crystal.client_wonder_trade.Utils.async_start") as async_start:
            await client.handle_wonder_trade(ctx)
            await client.handle_wonder_trade(ctx)
        async_start.assert_called_once()
        async_start.call_args.args[0].close()
        client.wonder_trade_receive.assert_not_awaited()
        self.assertTrue(client.wonder_trade_receiving)

    def _receiving_client(self):
        from unittest.mock import AsyncMock

        client = _make_client()
        client.wonder_trade_in_flight = True
        client.wonder_trade_receiving = True
        client.wonder_trade_cooldown = 20000
        self.blob = TestEligibilityFilter()._make_pool_entry(slot=1)[1]
        self.offer = bytes(range(1, 70))
        self.send_blob = bytes([25]) + self.offer
        client.wonder_trade_receive = AsyncMock(return_value=self.blob)
        return client

    async def test_received_trade_is_written_to_sram_immediately(self):
        from unittest.mock import AsyncMock, patch
        from ..data import data

        client = self._receiving_client()
        guarded_write = AsyncMock(return_value=True)
        with patch("worlds._bizhawk.guarded_write", guarded_write):
            await client._receive_in_background(_make_ctx(), 0x1234, self.offer)

        _, writes, guards = guarded_write.await_args.args
        status_addr = data.sram_addresses["sArchipelagoWonderTradeStatus"]
        self.assertIn((status_addr, [3], "CartRAM"), writes)
        self.assertIn((status_addr, [1], "CartRAM"), guards)
        self.assertIn((data.sram_addresses["sArchipelagoWonderTradeMagic"], b"\xa5\x5a\xc3", "CartRAM"), guards)
        self.assertIn((data.sram_addresses["sArchipelagoWonderTradeSendBuffer"] + 1, self.offer, "CartRAM"), guards)
        self.assertIsNone(client.queued_received_trade)
        self.assertFalse(client.wonder_trade_in_flight)
        self.assertEqual(client.wonder_trade_cooldown, 5000)
        self.assertFalse(client.wonder_trade_receiving)

    async def test_unwritable_received_trade_is_queued_for_watcher(self):
        from unittest.mock import AsyncMock, patch
        import worlds._bizhawk as bizhawk

        for outcome in (AsyncMock(return_value=False), AsyncMock(side_effect=bizhawk.RequestFailedError)):
            with self.subTest(outcome=outcome):
                client = self._receiving_client()
                with patch("worlds._bizhawk.guarded_write", outcome):
                    await client._receive_in_background(_make_ctx(), 0x1234, self.offer)
                self.assertEqual(client.queued_received_trade, (self.blob, self.offer))
                self.assertTrue(client.wonder_trade_in_flight)
                self.assertFalse(client.wonder_trade_receiving)

    async def test_watcher_keeps_queued_trade_until_written(self):
        from unittest.mock import AsyncMock, patch

        client = self._receiving_client()
        client.wonder_trade_receiving = False
        client.queued_received_trade = (self.blob, self.offer)
        read = AsyncMock(return_value=[b"\xa5\x5a\xc3", b"\x01", self.send_blob, b"\x12\x34"])
        with patch("worlds._bizhawk.read", read), \
                patch("worlds._bizhawk.guarded_write", AsyncMock(return_value=False)):
            await client.handle_wonder_trade(_make_ctx())
        self.assertEqual(client.queued_received_trade, (self.blob, self.offer))
        self.assertTrue(client.wonder_trade_in_flight)

        with patch("worlds._bizhawk.read", read), \
                patch("worlds._bizhawk.guarded_write", AsyncMock(return_value=True)):
            await client.handle_wonder_trade(_make_ctx())
        self.assertIsNone(client.queued_received_trade)
        self.assertFalse(client.wonder_trade_in_flight)

    async def test_queued_trade_for_previous_offer_is_dropped_and_new_offer_posts(self):
        from unittest.mock import AsyncMock, MagicMock, patch

        client = self._receiving_client()
        client.wonder_trade_receiving = False
        client.wonder_trade_send = MagicMock()
        # The late write landed, the partner was collected, and the player offered a new mon.
        client.queued_received_trade = (self.blob, self.offer)
        new_send_blob = bytes([152]) + bytes(range(2, 71))
        read = AsyncMock(side_effect=[[b"\xa5\x5a\xc3", b"\x01", new_send_blob, b"\x12\x34"], [b"\x00"]])
        guarded_write = AsyncMock(return_value=True)
        with patch("worlds._bizhawk.read", read), patch("worlds._bizhawk.guarded_write", guarded_write), \
                patch("worlds.pokemon_crystal.client_wonder_trade.Utils.async_start"):
            await client.handle_wonder_trade(_make_ctx())
        guarded_write.assert_not_awaited()
        self.assertIsNone(client.queued_received_trade)
        self.assertEqual(client.wonder_trade_send.call_args.args[3], new_send_blob)
        self.assertTrue(client.wonder_trade_in_flight)

    async def test_failed_receive_backs_off(self):
        from unittest.mock import AsyncMock

        client = _make_client()
        client.wonder_trade_receiving = True
        client.wonder_trade_receive = AsyncMock(side_effect=RuntimeError("connection lost"))
        with self.assertRaises(RuntimeError):
            await client._receive_in_background(_make_ctx(), 0x1234, bytes(69))
        self.assertIsNone(client.queued_received_trade)
        self.assertEqual(client.wonder_trade_cooldown_timer, 5000)
        self.assertGreaterEqual(client.wonder_trade_cooldown, 10000)
        self.assertFalse(client.wonder_trade_receiving)

    async def test_disconnected_receive_does_not_pop(self):
        client = _make_client()
        ctx = _make_ctx(connected=False)
        entry = TestEligibilityFilter()._make_pool_entry(slot=1)

        async def fake_acquire(ctx, keep_trying=False):
            return {"value": {"_lock": 1, "0": entry}}

        client.wonder_trade_acquire = fake_acquire
        self.assertIsNone(await client.wonder_trade_receive(ctx, 0x1234))
        ctx.send_msgs.assert_not_awaited()

if __name__ == "__main__":
    unittest.main()

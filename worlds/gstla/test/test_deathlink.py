from __future__ import annotations

import unittest
from typing import TYPE_CHECKING

from worlds.gstla.deathlink import (
    FIELD_DEATH_NARRATION_COUNT_ADDR,
    FIELD_DEATH_NARRATION_LIST_ADDR,
    FIELD_DEATH_SURVIVOR_COUNT_ADDR,
    GAME_STATE_READS,
    IN_BATTLE_BIT,
    SYSTEM_EVENT_ADDR,
    SYSTEM_EVENT_FIELD_DEATH,
    CharacterIndex as Character,
    DeathDeliverer,
    DeathDeliveryState,
    GameState,
    MemoryWrite,
    _build_field_death_request_writes,
    _build_multi_zero_hp_writes,
    get_current_hp_address,
    get_current_hp_ratio_address,
)

if TYPE_CHECKING:
    from collections.abc import Sequence


def _little_endian_u16(value: int) -> bytes:
    return value.to_bytes(2, 'little')


def _recruited(*characters: Character) -> int:
    return sum(1 << character for character in characters)


def _hp_values(*dead: Character) -> tuple[int, ...]:
    return tuple(0 if character in dead else _LIVE_HP[character] for character in Character)


def _hp_reads(*dead: Character) -> list[bytes]:
    return [_little_endian_u16(hp) for hp in _hp_values(*dead)]


def _build_full_field_death_writes(*recruited: Character) -> list[MemoryWrite]:
    return _build_multi_zero_hp_writes(recruited) + _build_field_death_request_writes()


def _build_deliverer(state: DeathDeliveryState) -> DeathDeliverer:
    dd = DeathDeliverer()
    dd.state = state
    return dd


_LIVE_HP = (11, 22, 33, 44, 55, 66, 77, 88)  # just arbitry HP values corresponding to each char
_ZERO_BYTES = _little_endian_u16(0)
_ARMED_REQUEST_BYTES = _little_endian_u16(SYSTEM_EVENT_FIELD_DEATH)

_DEFAULT_PARTY_CHARS = (Character.FELIX, Character.SHEBA)
_DEFAULT_PARTY = _recruited(*_DEFAULT_PARTY_CHARS)
_EVERYONE = tuple(Character)
_NOBODY = _recruited()

_OTHER_SYSTEM_EVENT = 0x0001  # not a real value, only used for testing


def _game_state(
    recruitment: int,
    in_battle: int = 0x00,
    system_event: int = 0x00,
    survivor_count: int = 0,
    dead: Sequence[Character] = (),  # TODO: change "dead" to "zero_hp_chars" or something?
) -> GameState:
    return GameState(
        recruitment=recruitment,
        in_battle=in_battle,
        system_event=system_event,
        survivor_count=survivor_count,
        hp=_hp_values(*dead),
    )


class TestCharacterHPAddresses(unittest.TestCase):
    def test_current_hp(self):
        self.assertEqual(0x558, get_current_hp_address(Character.ISAAC))
        self.assertEqual(0xA88, get_current_hp_address(Character.FELIX))
        self.assertEqual(0xD20, get_current_hp_address(Character.SHEBA))

    def test_current_hp_ratio(self):
        self.assertEqual(0x534, get_current_hp_ratio_address(Character.ISAAC))
        self.assertEqual(0xA64, get_current_hp_ratio_address(Character.FELIX))
        self.assertEqual(0xCFC, get_current_hp_ratio_address(Character.SHEBA))

    def test_current_hp_to_ratio_address_offset(self):
        self.assertEqual(0x24, get_current_hp_address(Character.ISAAC) - get_current_hp_ratio_address(Character.ISAAC))


class TestRecruitedCharacters(unittest.TestCase):
    _NO_BITS_SET = 0x00
    _BITS_4_AND_6 = 0x50

    def test_nobody_recruited(self):
        self.assertEqual((), _game_state(recruitment=self._NO_BITS_SET).recruited_characters)

    def test_felix_and_sheba(self):
        self.assertEqual(
            (Character.FELIX, Character.SHEBA),
            _game_state(recruitment=self._BITS_4_AND_6).recruited_characters,
        )


class TestIsPartyWiped(unittest.TestCase):
    def test_nobody_recruited(self):
        self.assertFalse(_game_state(recruitment=_NOBODY).is_party_wiped)

    def test_nobody_recruited_all_zero(self):
        self.assertFalse(_game_state(recruitment=_NOBODY, dead=_EVERYONE).is_party_wiped)

    def test_wiped_unrecruited_alive(self):
        self.assertTrue(_game_state(recruitment=_DEFAULT_PARTY, dead=[Character.FELIX, Character.SHEBA]).is_party_wiped)

    def test_wiped_unrecruited_also_zero(self):
        self.assertTrue(_game_state(recruitment=_DEFAULT_PARTY, dead=_EVERYONE).is_party_wiped)

    def test_all_alive(self):
        self.assertFalse(_game_state(recruitment=_DEFAULT_PARTY).is_party_wiped)

    def test_benched_survivor(self):
        self.assertFalse(
            _game_state(
                recruitment=_recruited(*_DEFAULT_PARTY_CHARS, Character.PIERS),
                dead=_DEFAULT_PARTY_CHARS,
            ).is_party_wiped
        )

    def test_one_recruited_alive(self):
        self.assertFalse(_game_state(recruitment=_recruited(Character.FELIX)).is_party_wiped)

    def test_one_recruited_dead(self):
        self.assertTrue(_game_state(recruitment=_recruited(Character.FELIX), dead=[Character.FELIX]).is_party_wiped)


class TestIsInBattle(unittest.TestCase):
    CONTEXT_BYTES = (
        (0x00, False),  # world map, outdoor field
        (0x10, False),  # shop, dialogue, field death
        (0x50, False),  # interior field, main menu open
        (0x18, True),  # in battle
    )

    def test_only_battle_bit_valid(self):
        for context_byte, expected in self.CONTEXT_BYTES:
            with self.subTest(context_byte=hex(context_byte)):
                state = _game_state(recruitment=_DEFAULT_PARTY, in_battle=context_byte)
                self.assertEqual(expected, state.is_in_battle)


class TestIsDeathObserved(unittest.TestCase):
    @staticmethod
    def _observe(dead: Sequence[Character], **kwargs):
        return _game_state(recruitment=_DEFAULT_PARTY, dead=dead, **kwargs).is_death_observed

    def test_battle_wipe_is_death(self):
        self.assertTrue(self._observe([Character.FELIX, Character.SHEBA], in_battle=IN_BATTLE_BIT))

    def test_battle_with_survivor_is_not_death(self):
        self.assertFalse(self._observe([Character.FELIX], in_battle=IN_BATTLE_BIT))

    def test_field_wipe_is_death(self):
        self.assertTrue(
            self._observe(
                [Character.FELIX, Character.SHEBA],
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                survivor_count=0,
            )
        )

    def test_single_down_is_not_death(self):
        self.assertFalse(
            self._observe(
                [Character.FELIX],
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                survivor_count=1,
            )
        )

    def test_fully_downed_party_with_survivors_is_not_death(self):
        # should *theoretically* never happen unless we write some bogus (I think)
        self.assertFalse(
            self._observe(
                [Character.FELIX, Character.SHEBA],
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                survivor_count=1,
            )
        )

    def test_field_death_request_with_living_party_is_not_death(self):
        self.assertFalse(
            self._observe(
                [],
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                survivor_count=0,
            )
        )

    def test_all_zero_party_with_no_request_is_not_death(self):
        # All chars at zero HP and no field death request should not equate to death.
        # Happens when loading a save for example.
        self.assertFalse(self._observe([Character.FELIX, Character.SHEBA]))

    def test_another_system_event_is_not_death(self):
        map_and_menu_event = 0xFC83  # just some other valid value the request slot can have
        self.assertFalse(
            self._observe([Character.FELIX, Character.SHEBA], system_event=map_and_menu_event, survivor_count=0)
        )

    def test_nobody_recruited_is_not_death(self):
        # RECRUITMENT_ADDR reads 0x10 at the title screen while the character blocks are at their default.
        self.assertFalse(
            _game_state(
                recruitment=_NOBODY,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                survivor_count=0,
                dead=_EVERYONE,
            ).is_death_observed
        )


class TestGameStateReads(unittest.TestCase):
    def setUp(self):
        self.width_by_address = dict(GAME_STATE_READS)

    def test_every_address_is_read_once(self):
        self.assertEqual(len(GAME_STATE_READS), len(self.width_by_address))

    def test_every_character_hp_is_u16(self):
        for character in Character:
            with self.subTest(character=character.name):
                self.assertEqual(2, self.width_by_address[get_current_hp_address(character)])

    def test_reads_and_writes_width(self):
        writes = [
            *_build_multi_zero_hp_writes(_EVERYONE),
            *_build_field_death_request_writes(),
        ]
        overlapping = [write for write in writes if write.address in self.width_by_address]
        for write in overlapping:
            with self.subTest(address=hex(write.address)):
                self.assertEqual(self.width_by_address[write.address], len(write.data))


class TestGameStateFromReadResult(unittest.TestCase):
    BATTLE_BIT_CLEAR_BYTE = 0x10

    def test_field_death_with_real_data_is_death(self):
        state = GameState.from_read_result(
            [
                bytes([_DEFAULT_PARTY]),
                bytes([self.BATTLE_BIT_CLEAR_BYTE]),
                _ARMED_REQUEST_BYTES,
                _ZERO_BYTES,
                *_hp_reads(*_DEFAULT_PARTY_CHARS),
            ]
        )
        self.assertEqual(
            GameState(
                recruitment=_DEFAULT_PARTY,
                in_battle=self.BATTLE_BIT_CLEAR_BYTE,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                survivor_count=0,
                hp=_hp_values(*_DEFAULT_PARTY_CHARS),
            ),
            state,
        )
        self.assertTrue(state.is_death_observed)


class TestPartyWipeWrites(unittest.TestCase):
    def test_every_hp_zero_is_written_together_with_their_ratio(self):
        writes = _build_multi_zero_hp_writes((Character.FELIX, Character.SHEBA))
        self.assertEqual(
            {
                get_current_hp_address(Character.FELIX),
                get_current_hp_ratio_address(Character.FELIX),
                get_current_hp_address(Character.SHEBA),
                get_current_hp_ratio_address(Character.SHEBA),
            },
            {write.address for write in writes},
        )
        self.assertEqual([_ZERO_BYTES] * 4, [write.data for write in writes])


class TestFieldDeathRequestWrites(unittest.TestCase):
    def setUp(self):
        self.writes = _build_field_death_request_writes()
        self.by_address = {write.address: write.data for write in self.writes}

    def test_death_request_last_write(self):
        self.assertEqual(MemoryWrite(SYSTEM_EVENT_ADDR, _ARMED_REQUEST_BYTES), self.writes[-1])

    def test_narration_count_is_zero(self):
        self.assertEqual(_ZERO_BYTES, self.by_address[FIELD_DEATH_NARRATION_COUNT_ADDR])

    def test_survivor_count_is_zero(self):
        self.assertEqual(_ZERO_BYTES, self.by_address[FIELD_DEATH_SURVIVOR_COUNT_ADDR])

    def test_no_narration_is_written(self):
        for slot in range(len(Character)):
            with self.subTest(slot=slot):
                self.assertNotIn(FIELD_DEATH_NARRATION_LIST_ADDR + 2 * slot, self.by_address)


class TestIdle(unittest.TestCase):
    def test_idle_does_not_write(self):
        dd = DeathDeliverer()
        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, in_battle=IN_BATTLE_BIT)).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

    def test_only_accept_when_idle(self):
        for state in DeathDeliveryState:
            with self.subTest(state=state):
                dd = _build_deliverer(state)
                dd.queue_death()
                expected = DeathDeliveryState.PENDING if state is DeathDeliveryState.IDLE else state
                self.assertEqual(expected, dd.state)


class TestReset(unittest.TestCase):
    def test_reset_does_not_write(self):
        dd = DeathDeliverer()
        dd.queue_death()
        dd.reset()
        self.assertEqual([], dd.tick(_game_state(recruitment=_DEFAULT_PARTY)).writes)


class TestPendingOnField(unittest.TestCase):
    def test_kill_party_on_field(self):
        for party in (_DEFAULT_PARTY_CHARS, _EVERYONE):
            with self.subTest(recruited=party):
                dd = _build_deliverer(DeathDeliveryState.PENDING)
                writes = dd.tick(_game_state(recruitment=_recruited(*party))).writes
                self.assertEqual(_build_full_field_death_writes(*party), writes)
                self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

    def test_wait_for_empty_system_event(self):
        for event in (SYSTEM_EVENT_FIELD_DEATH, _OTHER_SYSTEM_EVENT):
            with self.subTest(queued=event):
                dd = _build_deliverer(DeathDeliveryState.PENDING)
                writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, system_event=event)).writes
                self.assertEqual([], writes)
                self.assertEqual(DeathDeliveryState.PENDING, dd.state)

    def test_wait_for_recruited_characters(self):
        # Not a 100% sure *when* exactly the recruitment byte is 0,
        # since even on the title screen it's at the 0x10 (Felix recruited) default.
        # But let's make sure no deathlink would trigger if we ever see a 0x00 state.
        # Also:
        # The game_watcher should never even try to run this if we don't have
        # a savefile loaded. But having a guard here nontheless is better than not.
        dd = DeathDeliverer()
        dd.queue_death()
        for poll in range(10):
            with self.subTest(poll=poll):
                writes = dd.tick(_game_state(recruitment=_NOBODY)).writes
                self.assertEqual([], writes)
                self.assertEqual(DeathDeliveryState.PENDING, dd.state)

        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY)).writes
        self.assertEqual(_build_full_field_death_writes(*_DEFAULT_PARTY_CHARS), writes)


class TestPendingInBattle(unittest.TestCase):
    def test_in_battle_does_not_trigger_event(self):
        dd = _build_deliverer(DeathDeliveryState.PENDING)
        writes = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                in_battle=IN_BATTLE_BIT,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
            )
        ).writes
        self.assertEqual(_build_multi_zero_hp_writes(_DEFAULT_PARTY_CHARS), writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)


class TestInFlight(unittest.TestCase):
    def test_waits_on_event_queued(self):
        for event in (SYSTEM_EVENT_FIELD_DEATH, _OTHER_SYSTEM_EVENT):
            with self.subTest(queued=event):
                dd = _build_deliverer(DeathDeliveryState.IN_FLIGHT)
                writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, system_event=event)).writes
                self.assertEqual([], writes)
                self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

    def test_respawn_resets_to_idle(self):
        dd = _build_deliverer(DeathDeliveryState.IN_FLIGHT)
        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

    def test_dodged_via_flee_retriggers_death(self):
        # only happens if "flee" is clicked before death is queued while still "in battle"
        dd = _build_deliverer(DeathDeliveryState.IN_FLIGHT)
        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=_DEFAULT_PARTY_CHARS)).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.PENDING, dd.state)

    def test_no_retrigger_on_field_if_event_still_set(self):
        # after the party dies on field, there's still the short window
        # where the textboxes show up. It's still IN_FLIGHT but we don't
        # want to re-trigger the writes
        dd = _build_deliverer(DeathDeliveryState.IN_FLIGHT)
        writes = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                dead=_DEFAULT_PARTY_CHARS,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
            )
        ).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

    def test_no_retrigger_in_battle_if_event_still_set(self):
        # see test_no_retrigger_on_field_if_event_still_set
        dd = _build_deliverer(DeathDeliveryState.IN_FLIGHT)
        writes = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                in_battle=IN_BATTLE_BIT,
                dead=_DEFAULT_PARTY_CHARS,
            )
        ).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

    def test_battle_start_while_in_flight_does_not_send_deathlink(self):
        # if we try to trigger a death on a field, there is a small
        # window where a battle could be started right after those writes land
        # but before the game triggers the death sequence.
        # We have to make sure that we don't mistake that for a normal wipe
        # so we don't send a an accidental deathlink.
        dd = DeathDeliverer()
        dd.queue_death()

        # write while we're on the field
        self.assertFalse(dd.tick(_game_state(recruitment=_DEFAULT_PARTY)).send_death)

        # at this point the party should be at 0 HP
        # but the game has not triggered the death event yet
        # and has triggered a battle. This then results in having
        # the system event set *plus* the in_battle bit.
        battle_started = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                in_battle=IN_BATTLE_BIT,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                dead=_DEFAULT_PARTY_CHARS,
            )
        )
        self.assertFalse(battle_started.send_death)
        self.assertTrue(dd.is_delivering)

        # Felix/leader is respawned
        self.assertFalse(dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))).send_death)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)


class TestFullDeliverySequences(unittest.TestCase):
    def test_field_death_e2e(self):
        dd = DeathDeliverer()
        dd.queue_death()
        self.assertEqual(DeathDeliveryState.PENDING, dd.state)

        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY)).writes
        self.assertEqual(_build_full_field_death_writes(*_DEFAULT_PARTY_CHARS), writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

        writes = dd.tick(
            _game_state(
                # this is when the narration/textboxes would be on screen
                recruitment=_DEFAULT_PARTY,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                dead=_DEFAULT_PARTY_CHARS,
            )
        ).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

        # respawned, Felix/leader at 1 HP again
        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

    def test_in_battle_death_e2e(self):
        dd = DeathDeliverer()
        dd.queue_death()

        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, in_battle=IN_BATTLE_BIT)).writes
        self.assertEqual(_build_multi_zero_hp_writes(_DEFAULT_PARTY_CHARS), writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

        writes = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                in_battle=IN_BATTLE_BIT,
                dead=_DEFAULT_PARTY_CHARS,
            )
        ).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IN_FLIGHT, dd.state)

        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

    def test_flee_from_battle_e2e(self):
        # when "flee" was selected before deaths were written but before battle ended
        dd = DeathDeliverer()
        dd.queue_death()

        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, in_battle=IN_BATTLE_BIT)).writes
        self.assertEqual(_build_multi_zero_hp_writes(_DEFAULT_PARTY_CHARS), writes)

        # escaped, full party at 0 HP on field
        escaped = _game_state(recruitment=_DEFAULT_PARTY, dead=_DEFAULT_PARTY_CHARS)
        writes = dd.tick(escaped).writes
        self.assertEqual([], writes)
        self.assertTrue(dd.is_delivering)

        # re-trigger deaths
        writes = dd.tick(escaped).writes
        self.assertEqual(_build_full_field_death_writes(*_DEFAULT_PARTY_CHARS), writes)

        writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))).writes
        self.assertEqual([], writes)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

    def test_deathlink_is_ignored_when_party_wiped_themselves(self):
        # We have to make sure we don't kill the party if they're already dead
        # through normal circumstances. Getting killed, respawned and
        # then killed again would be pretty annoying.
        dd = DeathDeliverer()
        dd.queue_death()

        narrating = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                dead=_DEFAULT_PARTY_CHARS,
            )
        )
        self.assertFalse(narrating.send_death)
        self.assertEqual([], narrating.writes)

        respawned = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,)))
        self.assertEqual([], respawned.writes)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

    def test_several_requests_collapse_into_one_death(self):
        # could happen if a player has some menu open for a longer period of time
        # and multiple deaths come in via deathlink in the meantime
        dd = DeathDeliverer()
        for _ in range(3):
            dd.queue_death()
        self.assertEqual(DeathDeliveryState.PENDING, dd.state)

        all_writes = dd.tick(_game_state(recruitment=_DEFAULT_PARTY)).writes
        all_writes += dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                dead=_DEFAULT_PARTY_CHARS,
            )
        ).writes
        all_writes += dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))).writes

        requests = [write for write in all_writes if write.address == SYSTEM_EVENT_ADDR]
        self.assertEqual(1, len(requests))
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)


class TestOutgoingDeathReporting(unittest.TestCase):
    def test_wipe_in_battle_reported_only_once(self):
        dd = DeathDeliverer()
        wiped = _game_state(recruitment=_DEFAULT_PARTY, in_battle=IN_BATTLE_BIT, dead=_DEFAULT_PARTY_CHARS)
        self.assertTrue(dd.tick(wiped).send_death)
        self.assertFalse(dd.tick(wiped).send_death)

    def test_second_later_wipe_is_reported_again(self):
        dd = DeathDeliverer()
        wiped = _game_state(recruitment=_DEFAULT_PARTY, in_battle=IN_BATTLE_BIT, dead=_DEFAULT_PARTY_CHARS)
        respawned = _game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,))
        self.assertTrue(dd.tick(wiped).send_death)
        self.assertFalse(dd.tick(respawned).send_death)
        self.assertTrue(dd.tick(wiped).send_death)

    def test_death_by_deathlink_does_not_trigger_outgoing_death(self):
        dd = DeathDeliverer()
        dd.queue_death()

        outcome = dd.tick(_game_state(recruitment=_DEFAULT_PARTY))
        self.assertEqual(_build_full_field_death_writes(*_DEFAULT_PARTY_CHARS), outcome.writes)
        self.assertFalse(outcome.send_death)

        narrating = dd.tick(
            _game_state(
                recruitment=_DEFAULT_PARTY,
                system_event=SYSTEM_EVENT_FIELD_DEATH,
                dead=_DEFAULT_PARTY_CHARS,
            )
        )
        self.assertFalse(narrating.send_death)

        respawned = dd.tick(_game_state(recruitment=_DEFAULT_PARTY, dead=(Character.SHEBA,)))
        self.assertFalse(respawned.send_death)
        self.assertEqual(DeathDeliveryState.IDLE, dd.state)

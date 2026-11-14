from __future__ import annotations

from enum import Enum, IntEnum, auto
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from collections.abc import Sequence

RECRUITMENT_ADDR = 0x40  # also BizClient.FLAG_START
CHARACTER_BLOCK_SIZE = 0x14C
CHARACTER_BLOCK_START = 0x520

IN_BATTLE_ADDR = 0x60
IN_BATTLE_BIT = 0x08

SYSTEM_EVENT_ADDR = 0x3016A
SYSTEM_EVENT_FIELD_DEATH = 0xFFFF

FIELD_DEATH_NARRATION_COUNT_ADDR = 0x3016C
FIELD_DEATH_SURVIVOR_COUNT_ADDR = 0x3016E
FIELD_DEATH_NARRATION_LIST_ADDR = 0x30170

HP_RATIO_OFFSET = 0x14
MAX_HP_OFFSET = 0x34
CURRENT_HP_OFFSET = 0x38

# TODO: Obsolete for deathlink, but maybe useful to store somewhere?
MAX_PP_RATIO_OFFSET = 0x16
MAX_PP_OFFSET = 0x36
CURRENT_PP_OFFSET = 0x3A
CHARACTER_STATUS_BYTE_OFFSET = 0x131  # 0 = none, 1 = poison, 2 = venom, ...


class CharacterIndex(IntEnum):
    ISAAC = 0
    GARET = 1
    IVAN = 2
    MIA = 3
    FELIX = 4
    JENNA = 5
    SHEBA = 6
    PIERS = 7


def get_character_block_address(character: CharacterIndex) -> int:
    return CHARACTER_BLOCK_START + character * CHARACTER_BLOCK_SIZE


def get_current_hp_address(character: CharacterIndex) -> int:
    return get_character_block_address(character) + CURRENT_HP_OFFSET


def get_current_hp_ratio_address(character: CharacterIndex) -> int:
    """
    The "HP ratio" here is very likely just the way the game draws the HP bar.
    For some reason, the devs decided that bar should also double as a check
    against a (intentional or accidental) HP manipulation.

    Current HP and ratio have always have to be in sync.
    Setting the current HP to 0 without changing the ratio might result in
    a mismatch the game then corrects by setting that character to max HP/PP.
    Writing to these addresses should therefore always be done together
    in one single operation. Having them even just a few frames apart while someone spams
    their way through the battle actions can introduce a sudden full-heal.
    """
    return get_character_block_address(character) + HP_RATIO_OFFSET


GAME_STATE_READS: tuple[tuple[int, int], ...] = (
    (RECRUITMENT_ADDR, 1),
    (IN_BATTLE_ADDR, 1),
    (SYSTEM_EVENT_ADDR, 2),
    (FIELD_DEATH_SURVIVOR_COUNT_ADDR, 2),
    *tuple((get_current_hp_address(character), 2) for character in CharacterIndex),
)


class GameState(NamedTuple):
    recruitment: int
    in_battle: int
    system_event: int
    survivor_count: int
    hp: tuple[int, ...]

    @classmethod
    def from_read_result(cls, results: Sequence[bytes]) -> GameState:
        values = {}
        for (address, _width), result in zip(GAME_STATE_READS, results, strict=True):
            values[address] = int.from_bytes(result, 'little')

        return cls(
            recruitment=values[RECRUITMENT_ADDR],
            in_battle=values[IN_BATTLE_ADDR],
            system_event=values[SYSTEM_EVENT_ADDR],
            survivor_count=values[FIELD_DEATH_SURVIVOR_COUNT_ADDR],
            hp=tuple(values[get_current_hp_address(character)] for character in CharacterIndex),
        )

    @property
    def recruited_characters(self) -> tuple[CharacterIndex, ...]:
        """
        The indexes of all currently recruited characters.

        The character blocks of unrecruited chars are not empty,
        they just have their default stats set and look like a
        fully healed character.
        So every HP read has to first go through this function.
        """
        return tuple(character for character in CharacterIndex if self.recruitment & (1 << character))

    @property
    def is_in_battle(self) -> bool:
        return bool(self.in_battle & IN_BATTLE_BIT)

    @property
    def is_field_death_armed(self) -> bool:
        return self.system_event == SYSTEM_EVENT_FIELD_DEATH

    @property
    def is_system_event_queued(self) -> bool:
        """
        True while the address holds an event the game has not yet executed.

        These events are checked every frame (few frames?) when on the field and when we're
        not "busy" with something like conversations, so they'll trigger immediately after
        we close out of a conversation/shop/menu/etc.

        Before we write to SYSTEM_EVENT_ADDR, we check if the game has already
        queued *something*. We should only ever write to SYSTEM_EVENT_ADDR if it is empty.
        """
        return self.system_event != 0

    @property
    def is_party_wiped(self) -> bool:
        """
        True when every recruited character is at 0 HP, False when nobody is recruited.
        Important: This does not automatically mean the full party died (yet).

        Note:
        This also returns True when the game has just booted up.
        In that case the recruitment byte is already 0x10 (Felix) while character HP is 0.
        So just relying on this to detect a wipe is not enough and
        a caller also has to check that a save is actually loaded.
        """
        recruited = self.recruited_characters
        return bool(recruited) and all(self.hp[character] == 0 for character in recruited)

    @property
    def is_field_death_in_progress(self) -> bool:
        """
        True when a field death is running and the game counts nobody as still standing.

        We trigger a field death by writing SYSTEM_EVENT_FIELD_DEATH into the system event slot,
        but just doing that alone does not automatically mean that we triggered a death.
        The game also writes that same SYSTEM_EVENT_FIELD_DEATH every time a character goes down
        on the field, like when they're poisoned and take their last step.
        But as long as the survivor count is not 0, it just shows the
        "character is exhausted" text and the game continues normally.

        Also note:
        Since we'll also be writing both of these values ourselves to wipe the party,
        just checking these values only tells us that a field death is happening,
        but not if it's caused by us or just dying "naturally" via poison or something.
        """
        return self.is_field_death_armed and self.survivor_count == 0

    @property
    def is_death_observed(self) -> bool:
        """
        True when every recruited character reads 0 HP *and* the game has acted on it,
        so this is an actual death and not just a party that happens to be at zero.

        This is an important distinction because "everyone at 0 HP" can occur in other places
        like booting up the game or when we write 0 HP ourselves to trigger the deathlink.

        How the proper confirmation looks like:
        - In battle:
          Relatively straight-forward. Since the game checks on every action/input,
          it'll just play the defeat dialogue after we've set the HP to 0.

        - On the field/overworld:
          There's no loop like the one in battle that checks for HP, so without any trigger
          we could just stay on the field forever. Only when we'd get into a battle,
          it would then check for HP and play the defeat dialogue.
          However, it does have a loop that is checking for registered events like a poison tick.
          Also see `is_field_death_in_progress`.
        """
        return self.is_party_wiped and (self.is_in_battle or self.is_field_death_in_progress)

    @property
    def write_guards(self) -> list[tuple[int, bytes]]:
        return [
            (SYSTEM_EVENT_ADDR, self.system_event.to_bytes(2, 'little')),
            (IN_BATTLE_ADDR, self.in_battle.to_bytes(1, 'little')),
        ]


class MemoryWrite(NamedTuple):
    address: int
    data: bytes

    @classmethod
    def u16(cls, address: int, value: int) -> MemoryWrite:
        return cls(address, value.to_bytes(2, 'little'))


def _build_zero_hp_writes(character: CharacterIndex) -> tuple[MemoryWrite, MemoryWrite]:
    """
    HP writes should *always* only happen together. If the game sees a mismatch
    between HP and HP ratio, it will try to correct it when it runs some kind of
    loop on that character. Just setting HP *can* theoretically work but
    it's extremely inconsistant.

    Example:
        1. Start a fight, click through enemy textboxes
        2. Write HP to 0 without the ratio
        3. Select the "Fight" option
        4. In *most* cases, this is when the loop runs and a characters HP (+PP) get corrected to max.
    """

    return (
        MemoryWrite.u16(get_current_hp_address(character), 0),
        MemoryWrite.u16(get_current_hp_ratio_address(character), 0),
    )


def _build_multi_zero_hp_writes(characters: Sequence[CharacterIndex]) -> list[MemoryWrite]:
    return [write for character in characters for write in _build_zero_hp_writes(character)]


def _build_field_death_request_writes() -> list[MemoryWrite]:
    """
    These writes just use the same ingame way of handling something like poison deaths.
    (Setting Survivors to 0 and SYSTEM_EVENT_ADDR to the field death event.)

    *But* setting the NARRATION_COUNT to 0 means that instead of having 8
    "XYZ is exhausted..." textboxes to click through we just get one saying
    "<leader>'s party has been annihilated...".
    This makes the wipe much faster. Yippie
    """
    return [
        MemoryWrite.u16(FIELD_DEATH_NARRATION_COUNT_ADDR, 0),
        MemoryWrite.u16(FIELD_DEATH_SURVIVOR_COUNT_ADDR, 0),
        MemoryWrite.u16(SYSTEM_EVENT_ADDR, SYSTEM_EVENT_FIELD_DEATH),
    ]


class DeathDeliveryState(Enum):
    IDLE = auto()  # default, no death has been sent by anyone (or we haven't received one yet)
    PENDING = auto()  # a death came in and was accepted, but the game has not been told about it yet
    IN_FLIGHT = auto()  # any kind of death is running but the game has not yet finished respawning the party


class DeathLinkInstruction(NamedTuple):
    writes: list[MemoryWrite]
    send_death: bool


class DeathDeliverer:
    """
    The DeathDeliverer™ handles incoming deathlinks.
    It differentiates between a normal death and a death-by-deathlink.
    It will also wait until the game is able to accept the death and only then
    trigger the actual death sequence.
    """

    def __init__(self) -> None:
        self._death_observed_last_tick = False
        self.state = DeathDeliveryState.IDLE

    def tick(self, game_state: GameState) -> DeathLinkInstruction:
        send_death = self._detect_new_death(game_state)
        return DeathLinkInstruction(writes=self._advance(game_state), send_death=send_death)

    def retry_delivery(self) -> None:
        if self.state is DeathDeliveryState.IN_FLIGHT:
            self.state = DeathDeliveryState.PENDING

    @property
    def is_delivering(self) -> bool:
        return self.state is not DeathDeliveryState.IDLE

    def queue_death(self) -> None:
        if self.state is DeathDeliveryState.IDLE:
            self.state = DeathDeliveryState.PENDING

    def reset(self) -> None:
        """
        Resets every state and instruction inbound & outbound.

        We don't write anything to the game here.
        Once we've written the system event for a death,
        there's no going back on it. Trying to reset the event by
        writing something else to SYSTEM_EVENT_ADDR would very likely
        land too late anyway.
        """
        self._death_observed_last_tick = False
        self.state = DeathDeliveryState.IDLE

    def _advance(self, game_state: GameState) -> list[MemoryWrite]:
        """The inbound part of tick()"""
        if self.state is DeathDeliveryState.PENDING:
            if game_state.is_death_observed:
                # party already wiped on their own, so we just ignore any incoming
                # deathlink here as dying after respawning is not a fun mechanic
                self.state = DeathDeliveryState.IN_FLIGHT
                return []
            return self._deliver(game_state)

        if self.state is DeathDeliveryState.IN_FLIGHT:
            self._check_for_arrival(game_state)

        return []

    def _detect_new_death(self, game_state: GameState) -> bool:
        """The outbound part of tick()"""
        death_observed = game_state.is_death_observed
        send_death = death_observed and not self._death_observed_last_tick and not self.is_delivering
        self._death_observed_last_tick = death_observed
        return send_death

    def _deliver(self, game_state: GameState) -> list[MemoryWrite]:
        """See `GameState.is_death_observed()` for an explanation of how this works"""
        recruited = game_state.recruited_characters
        if not recruited:
            # should only happen when there's no savefile loaded yet
            return []

        writes = _build_multi_zero_hp_writes(recruited)
        if not game_state.is_in_battle:
            if game_state.is_system_event_queued:
                # we don't want to overwrite anything the game itself wrote there
                return []
            writes += _build_field_death_request_writes()

        self.state = DeathDeliveryState.IN_FLIGHT
        return writes

    def _check_for_arrival(self, game_state: GameState) -> None:
        """
        This handles the following outcomes:

        Death-by-DeathLink was successfull:
         -> Felix (or the leader) is back at 1 HP (respawned in a sanctum)

        Death was dodged somehow:
         -> Should only happen if a player confirms "Flee" before we write the death in battle.
            Escaping does not trigger any HP check in the game, so the party's just at 0 HP on the
            field/overworld. We then have to re-apply the death through the field path.
            Note: There *might* be a better way to handle this (maybe through some hook directly
            in the ROM), but for now this works, too.

        A battle was started while the state was IN_FLIGHT:
         -> This just produces the normal death sequence directly at the start of the fight
            because we've already written the party-wide 0 HP.

        The party died through natural causes:
         -> Looks the same as killing them via deathlink. That also means that we should
            just drop/ignore the request, similar to what happens when multiple deathlinks come in.
            It'd be annoying to wipe, revive in sanctum and then get killed again.
        """
        if game_state.is_in_battle or game_state.is_system_event_queued:
            return

        self.state = DeathDeliveryState.PENDING if game_state.is_party_wiped else DeathDeliveryState.IDLE

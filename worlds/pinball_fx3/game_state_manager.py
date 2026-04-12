from typing import NamedTuple, Optional, Tuple

from pymem import Pymem
from pymem.process import close_handle

from .data.mapping_data import challenge_type_id_to_challenge_type, table_id_to_table
from .enums import PinballFX3ChallengeTypes, PinballFX3Contexts, PinballFX3Tables


class GameState(NamedTuple):
    context: PinballFX3Contexts = PinballFX3Contexts.INVALID
    table: Optional[PinballFX3Tables] = None
    current_score: Optional[int] = None
    challenge_type: Optional[PinballFX3ChallengeTypes] = None
    stars_obtained: Optional[int] = None
    target_score: Optional[int] = None
    previous_target_score: Optional[int] = None


class GameStateManager:
    process_name = "Pinball FX Classic.exe"

    process: Optional[Pymem]
    is_process_running: bool

    competition_handler_address: Optional[int]
    challenge_handler_address: Optional[int]

    last_seen_context: PinballFX3Contexts
    last_seen_score: int

    def __init__(self) -> None:
        self.process = None
        self.is_process_running = False

        self.competition_handler_address = None
        self.challenge_handler_address = None

        self.last_seen_context = PinballFX3Contexts.INVALID
        self.last_seen_score = -1

    @property
    def competition_handler_struct_address(self) -> Optional[int]:
        return self._resolve_address(0xE2DAA4, (0x38, 0x8, 0x4, 0x8, 0x0))

    @property
    def competition_table_id_address(self) -> Optional[int]:
        if self.competition_handler_address is None:
            return None

        return self.competition_handler_address + 0x80

    @property
    def competition_current_score_address(self) -> Optional[int]:
        if self.competition_handler_address is None:
            return None

        return self.competition_handler_address + 0x50  # 8 bytes

    @property
    def challenge_handler_struct_address(self) -> Optional[int]:
        return self._resolve_address(0xAC5E9C, (0x160, 0x4, 0x30))

    @property
    def challenge_table_id_address(self) -> Optional[int]:
        if self.challenge_handler_address is None:
            return None

        return self.challenge_handler_address + 0x140

    @property
    def challenge_type_address(self) -> Optional[int]:
        if self.challenge_handler_address is None:
            return None

        return self.challenge_handler_address + 0x38

    @property
    def challenge_stars_obtained_address(self) -> Optional[int]:
        if self.challenge_handler_address is None:
            return None

        return self.challenge_handler_address + 0x60

    @property
    def challenge_target_score_address(self) -> Optional[int]:
        if self.challenge_handler_address is None:
            return None

        return self.challenge_handler_address + 0x68  # 8 bytes

    @property
    def challenge_previous_target_score_address(self) -> Optional[int]:
        if self.challenge_handler_address is None:
            return None

        return self.challenge_handler_address + 0x70  # 8 bytes

    @property
    def challenge_current_score_address(self) -> Optional[int]:
        if self.challenge_handler_address is None:
            return None

        return self.challenge_handler_address + 0x78  # 8 bytes

    def open_process_handle(self) -> bool:
        try:
            self.process = Pymem(self.process_name)
            self.is_process_running = True

            self.competition_handler_address = self.competition_handler_struct_address
            self.challenge_handler_address = self.challenge_handler_struct_address
        except Exception:
            return False

        return True

    def close_process_handle(self) -> bool:
        if close_handle(self.process.process_handle):
            self.is_process_running = False
            self.process = None

            self.competition_handler_address = None
            self.challenge_handler_address = None

            self.last_seen_context = PinballFX3Contexts.INVALID
            self.last_seen_score = -1

            return True

        return False

    def is_process_still_running(self) -> bool:
        try:
            self.process.read_int(self.process.base_address)
        except Exception:
            self.is_process_running = False
            self.process = None

            self.competition_handler_address = None
            self.challenge_handler_address = None

            self.last_seen_context = PinballFX3Contexts.INVALID
            self.last_seen_score = -1

            return False

        return True

    def determine_game_state(self) -> GameState:
        # The methodology here will need some context.

        # When playing in Single-Player mode, only CompetitiveHandler matters and gets set
        # When playing in Challenge mode, ChallengeHandler is the one that matters, but CompetitionHandler also gets set

        # Haven't found a way to know where we are in-game (Menu, Single-Player, Challenge etc.)
        # So we need a heuristic to determine the current context

        # Once either Handler's pointers are set, they seem to never be zeroed out again
        # That said, the Table ID in ChallengeHandler seems to be set to 0 when leaving Challenge mode
        # This isn't the case for CompetitionHandler; the Table ID persists until overwritten with another one
        # This allows us to at least know for sure when we are NOT in Challenge mode

        # It also presents a problem, as we can't know which mode the CompetitiveHandler's struct data came from
        # For example, if we score 12345 points in Challenge mode and exit to menu, the only Handler with a valid Table
        # ID will be CompetitionHandler, and the score will be 12345 as well and still set. This could leave us wrongly
        # interpreting game state and thinking the player also just scored 12345 points in Single-Player mode

        # The current idea on how to determine context is to track the last seen context and score
        # If the context change but the score is identical, we can assume we just exited Challenge mode and report an
        # invalid context in our response instead. Once the score changes again, we can resume returning game state

        self.competition_handler_address = self.competition_handler_struct_address
        self.challenge_handler_address = self.challenge_handler_struct_address

        competition_table_id: int = 0
        challenge_table_id: int = 0

        try:
            competition_table_id = self.process.read_int(self.competition_table_id_address)
        except Exception:
            pass

        try:
            challenge_table_id = self.process.read_int(self.challenge_table_id_address)
        except Exception:
            pass

        if competition_table_id not in table_id_to_table and challenge_table_id not in table_id_to_table:
            return GameState(context=PinballFX3Contexts.INVALID)

        context: PinballFX3Contexts
        score: int

        if challenge_table_id in table_id_to_table:
            context = PinballFX3Contexts.CHALLENGE
            score = self.process.read_longlong(self.challenge_current_score_address)
        else:
            context = PinballFX3Contexts.SINGLE_PLAYER
            score = self.process.read_longlong(self.competition_current_score_address)

        if context != self.last_seen_context and score == self.last_seen_score:
            return GameState(context=PinballFX3Contexts.INVALID)

        self.last_seen_context = context
        self.last_seen_score = score

        if context == PinballFX3Contexts.SINGLE_PLAYER:
            return GameState(
                context=context,
                table=table_id_to_table[self.process.read_int(self.competition_table_id_address)],
                current_score=score,
            )
        elif context == PinballFX3Contexts.CHALLENGE:
            return GameState(
                context=context,
                table=table_id_to_table[self.process.read_int(self.challenge_table_id_address)],
                current_score=score,
                challenge_type=challenge_type_id_to_challenge_type.get(self.process.read_int(self.challenge_type_address), 1),
                stars_obtained=self.process.read_int(self.challenge_stars_obtained_address),
                target_score=self.process.read_longlong(self.challenge_target_score_address),
                previous_target_score=self.process.read_longlong(self.challenge_previous_target_score_address),
            )

    # Use readuint for 32-bit processes, readlonglong for 64-bit processes
    def _resolve_address(self, base_offset: int, offsets: Tuple[int, ...]) -> Optional[int]:
        address: int = self.process.read_uint(self.process.base_address + base_offset)

        for offset in offsets[:-1]:
            try:
                address = self.process.read_uint(address + offset)
            except Exception:
                return None

        return address + offsets[-1]

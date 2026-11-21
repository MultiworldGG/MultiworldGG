# TODO: Try to display messages using in-game hints (need to figure out how to do so without crashing the game)
import logging
from collections import deque
from time import monotonic_ns

from . import ClientComponent
from ..common import StaticFloat
from ..events import subscribe_event, OnGameWatcherTickEvent, OnUnhookFromGameEvent
from ..type_aliases import TCSContext
from .text_replacer import TextId


_DEBUG_LOGGER = logging.getLogger("TCS Debug")

# Float value in seconds. The text will begin to fade out towards the end.
# Note that values higher than 1.0 will flash more rapidly the higher the value.
_DOUBLE_SCORE_ZONE_TIMER_ADDRESS = StaticFloat(0x925060)

_WAIT_BETWEEN_MESSAGES_SECONDS = 2
_WAIT_BETWEEN_MESSAGES_NS = _WAIT_BETWEEN_MESSAGES_SECONDS * 1_000_000_000


class InGameTextDisplay(ClientComponent):
    next_allowed_message_time: int
    next_allowed_clean_time: int
    # If the last write to memory was a custom message.
    memory_dirty: bool = False

    message_queue: deque[str]

    def __init__(self):
        self.message_queue = deque()
        now = monotonic_ns()
        self.next_allowed_message_time = now
        self.next_allowed_clean_time = now

    def queue_message(self, message: str):
        self.message_queue.append(message)

    def priority_message(self, message: str):
        self.message_queue.appendleft(message)

    def priority_messages(self, *messages: str):
        # priority_messages appends the message to the front, so, to maintain order, the messages need to be appended in
        # reverse.
        for message in reversed(messages):
            self.priority_message(message)

    # A custom minimum duration of more than 4 seconds is irrelevant currently because the message fades out by that
    # point.
    def _display_message(self, ctx: TCSContext, message: str,
                         next_message_delay_ns: int = _WAIT_BETWEEN_MESSAGES_NS,
                         display_duration_s: float = 4.0):
        # Write the message into the allocated memory for message strings.
        _DEBUG_LOGGER.info("Text Display: Displaying in-game message '%s'", message)
        ctx.text_replacer.write_custom_string(TextId.DOUBLE_SCORE_ZONE, message)
        self.memory_dirty = True

        # Set the timer.
        _DOUBLE_SCORE_ZONE_TIMER_ADDRESS.set(ctx, display_duration_s)

        # Update for the next time that a new message can be displayed.
        now = monotonic_ns()
        self.next_allowed_message_time = now + next_message_delay_ns
        self.next_allowed_clean_time = max(now + int((display_duration_s + 1) * 1_000_000_000),
                                           self.next_allowed_message_time)

    @subscribe_event
    def on_unhook_game_process(self, _event: OnUnhookFromGameEvent) -> None:
        self.message_queue.clear()
        if self.memory_dirty:
            # The TCSContext's TextReplacer will restore all replaced texts back to their vanilla text.
            self.memory_dirty = False

    @subscribe_event
    async def update_game_state(self, event: OnGameWatcherTickEvent) -> None:
        now = monotonic_ns()
        if now < self.next_allowed_message_time:
            return

        ctx = event.context
        if not self.message_queue:
            if self.memory_dirty and now > self.next_allowed_clean_time:
                _DEBUG_LOGGER.info("Text Display: Clearing dirty memory")
                ctx.text_replacer.write_vanilla_string(TextId.DOUBLE_SCORE_ZONE)
                self.memory_dirty = False
        else:
            # Don't display a new message if the game is paused, in a cutscene, in a status screen, or tabbed out.
            if event.is_actively_playing:
                self._display_message(ctx, self.message_queue.popleft())

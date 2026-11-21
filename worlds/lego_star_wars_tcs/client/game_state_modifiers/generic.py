import logging
from typing import Mapping, Sequence, cast

from ..events import subscribe_event, OnReceiveSlotDataEvent
from ..type_aliases import TCSContext
from . import ItemReceiver

from ...data.extras import Extra
from ...data.items.generic_items import (
    NonDataItemName,
    GENERIC_DATA,
    GenericItemData,
    GENERIC_DATA_BY_NAME,
    EPISODE_UNLOCKS,
    CHAPTER_TO_CHAPTER_UNLOCK_ITEM,
)


_SEPARATELY_HANDLED_GENERIC = {
    NonDataItemName.SILVER_STUD,
    NonDataItemName.GOLD_STUD,
    NonDataItemName.BLUE_STUD,
    NonDataItemName.PURPLE_STUD,
    NonDataItemName.POWER_UP,
    NonDataItemName.MINIKIT,
    NonDataItemName.TWO_MINIKITS,
    NonDataItemName.FIVE_MINIKITS,
    NonDataItemName.TEN_MINIKITS,
}
_RECEIVABLE_GENERIC_BY_AP_ID: Mapping[int, GenericItemData] = cast(dict[int, GenericItemData], {
    item.code: item for item in GENERIC_DATA
    if item.is_sendable and item.name not in _SEPARATELY_HANDLED_GENERIC
})
_EPISODE_UNLOCK_AP_ID_TO_EPISODE_NUMBER: Mapping[int, int] = cast(dict[int, int], {
    GENERIC_DATA_BY_NAME[item_name].code: episode for episode, item_name in EPISODE_UNLOCKS.items()
})
_CHAPTER_UNLOCK_AP_IDS: set[int] = cast(set[int], {
    GENERIC_DATA_BY_NAME[item_name].code for item_name in CHAPTER_TO_CHAPTER_UNLOCK_ITEM.values()
})
_ALL_EPISODES_TOKEN: int = cast(int, GENERIC_DATA_BY_NAME[NonDataItemName.EPISODE_COMPLETION_TOKEN].code)
_PROGRESSIVE_SCORE_MULTIPLIER: int = cast(int, GENERIC_DATA_BY_NAME[NonDataItemName.PROGRESSIVE_SCORE_MULTIPLIER].code)
_KYBER_BRICK: int = cast(int, GENERIC_DATA_BY_NAME[NonDataItemName.KYBER_BRICK].code)
_SCORE_MULIPLIER_EXTRAS: Sequence[Extra] = (
    Extra.SCORE_X2,
    Extra.SCORE_X4,
    Extra.SCORE_X6,
    Extra.SCORE_X8,
    Extra.SCORE_X10,
)


_LOGGER = logging.getLogger("Client")


_COMBINED_SCORE_MULTIPLIERS: Sequence[int] = [
    1,
    2,
    2 * 4,  # 8
    2 * 4 * 6,  # 48
    2 * 4 * 6 * 8,  # 384
    2 * 4 * 6 * 8 * 10,  # 3840
]

# todo: This is an idea for the future for slower scaling score multipliers.
#  The score multiplier extras would want to be enabled/disabled automatically as progressive score multiplier items are
#  received.
# STEP_SCORE_MULTIPLIERS: Sequence[tuple[tuple[int, ...], int]] = [
#     ((), 1),
#     ((2,), 2),  # +1
#     ((4,), 4),  # +2
#     ((6,), 6),  # +2
#     ((8,), 8),  # ((2, 4), 8),  # +2
#     ((10,), 10),  # +2
#     ((2, 6), 12),  # +2
#     ((2, 8), 16),  # +4
#     ((2, 10), 20),  # +4
#     ((4, 6), 24),  # +4
#     ((4, 8), 32),  # +8
#     ((4, 10), 40),  # +8
#     ((6, 8), 48),  # ((2, 4, 6), 48),  # +8
#     ((6, 10), 60),  # Suggested to skip  # +12
#     ((2, 4, 8), 64),  # +4 (no skip) or +16 (skip)
#     ((8, 10), 80),  # ((2, 4, 10), 80),  # +16
#     ((2, 6, 8), 96),  # +16
#     ((2, 6, 10), 120),  # Suggested cutoff #1 at 16 multipliers with (6, 10) skipped.  # +24
#     ((2, 8, 10), 160),  # +40
#     ((4, 6, 8), 192),  # +32
#     ((4, 6, 10), 240),  # +48
#     ((4, 8, 10), 320),  # +80
#     ((2, 4, 6, 8), 384),  # +64
#     ((6, 8, 10), 480),  # ((2, 4, 6, 10), 480),  # +96
#     ((2, 4, 8, 10), 640),  # +160
#     ((2, 6, 8, 10), 960),  # +320
#     ((4, 6, 8, 10), 1920),  # +960
#     ((2, 4, 6, 8, 10), 3840),  # +1920
# ]


class AcquiredGeneric(ItemReceiver):
    receivable_ap_ids = _RECEIVABLE_GENERIC_BY_AP_ID

    received_episode_unlocks: set[int]
    # received_chapter_unlocks: set[str]
    episode_completion_token_count: int = 0
    progressive_score_count: int = 0
    kyber_brick_count: int = 0

    def __init__(self):
        self.received_episode_unlocks = set()
        # self.received_chapter_unlocks = set()

    @subscribe_event
    def init_from_slot_data(self, _event: OnReceiveSlotDataEvent) -> None:
        self.clear_received_items()

    def clear_received_items(self) -> None:
        self.received_episode_unlocks.clear()
        # self.received_chapter_unlocks.clear()
        self.episode_completion_token_count = 0
        self.progressive_score_count = 0
        self.kyber_brick_count = 0

    @property
    def current_score_multiplier(self):
        idx = min(self.progressive_score_count, len(_COMBINED_SCORE_MULTIPLIERS) - 1)
        return _COMBINED_SCORE_MULTIPLIERS[idx]

    def receive_generic(self, ctx: TCSContext, ap_item_id: int):
        # Progressive Score Multiplier
        if ap_item_id == _PROGRESSIVE_SCORE_MULTIPLIER:
            if self.progressive_score_count < len(_SCORE_MULIPLIER_EXTRAS):
                ctx.acquired_extras.unlock_extra(_SCORE_MULIPLIER_EXTRAS[self.progressive_score_count])
            self.progressive_score_count += 1
        # 'All Episodes' tokens
        elif ap_item_id == _ALL_EPISODES_TOKEN:
            self.episode_completion_token_count += 1
        # Episode Unlocks
        elif ap_item_id in _EPISODE_UNLOCK_AP_ID_TO_EPISODE_NUMBER:
            self.received_episode_unlocks.add(_EPISODE_UNLOCK_AP_ID_TO_EPISODE_NUMBER[ap_item_id])
            ctx.unlocked_chapter_manager.on_character_or_chapter_or_episode_unlocked(ctx, ap_item_id)
        # Chapter Unlocks
        elif ap_item_id in _CHAPTER_UNLOCK_AP_IDS:
            # self.received_chapter_unlocks.add(CHAPTER_UNLOCKS[ap_item_id])
            ctx.unlocked_chapter_manager.on_character_or_chapter_or_episode_unlocked(ctx, ap_item_id)
        # Kyber Brick goal items
        elif ap_item_id == _KYBER_BRICK:
            self.kyber_brick_count += 1
            ctx.goal_manager.tag_for_update("kyber brick")
        else:
            _LOGGER.error("Unhandled ap_item_id %s for generic item", ap_item_id)

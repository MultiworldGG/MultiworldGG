import logging
from typing import Mapping, cast

from ..events import subscribe_event, OnReceiveSlotDataEvent
from ..type_aliases import TCSContext
from . import ItemReceiver

from ...data.items import MinikitItemData
from ...data.items.generic_items import GENERIC_DATA

_MINIKIT_ITEM_CODE_TO_COUNT: Mapping[int, int] = cast(dict[int, int], {
    item.code: item.bundle_size for item in GENERIC_DATA if isinstance(item, MinikitItemData)
})

_LOGGER = logging.getLogger("Client")


class AcquiredMinikits(ItemReceiver):
    receivable_ap_ids = _MINIKIT_ITEM_CODE_TO_COUNT

    minikit_count: int

    def __init__(self):
        self.minikit_count = 0

    @subscribe_event
    def init_from_slot_data(self, _event: OnReceiveSlotDataEvent) -> None:
        self.clear_received_items()

    def clear_received_items(self) -> None:
        self.minikit_count = 0

    def receive_minikit(self, ctx: TCSContext, ap_item_id: int):
        # Minikits
        if ap_item_id in _MINIKIT_ITEM_CODE_TO_COUNT:
            self.minikit_count += _MINIKIT_ITEM_CODE_TO_COUNT[ap_item_id]
            ctx.goal_manager.tag_for_update("minikit")
        else:
            _LOGGER.error("Unhandled ap_item_id %s for generic item", ap_item_id)

import logging
from typing import Mapping, Sequence, cast

from ..common import StaticUChar
from ..common_addresses import ShopType, EXTRAS_SHOP_START, AREA_DATA_ID, CURRENT_P_AREA_DATA_ADDRESS
from ..custom_save_data import CustomSaveFlags2
from ..events import subscribe_event, OnReceiveSlotDataEvent, OnGameWatcherTickEvent, OnLevelChangeEvent
from ..type_aliases import ApItemId, BitMask, MemoryOffset, TCSContext
from . import ItemReceiver

from ...data.areas import Area
from ...data.extras import Extra
from ...data.items.extra_items import EXTRA_DATA
from ...data.levels import Level


_LOGGER = logging.getLogger("Client")
_DEBUG_LOGGER = logging.getLogger("TCS Debug")


_UNLOCKED_EXTRAS_ADDRESS = 0x86e4e8
"""Memory address of the array that stores which Extras are unlocked."""

# EXTRAS_SHOP_LENGTH_BYTES = 6  # 0xB8 to 0xBD
# Active slot in the shop, which displays its name and will be purchased if the player presses the use key
# Note: The previous 2 and next 2 shop indices are before/after this in memory (5 on screen at once).
_EXTRAS_SHOP_ACTIVE_INDEX_ADDRESS = StaticUChar(0x87bf2c)


_RECEIVABLE_EXTRAS_BY_AP_ID: Mapping[ApItemId, Extra] = cast(dict[ApItemId, Extra], {
    data.code: data.extra for data in EXTRA_DATA
})
_ALL_RECEIVABLE_EXTRAS: Sequence[Extra] = [
    extra for extra in Extra if extra.is_purchasable()
]

# All bytes in the UnlockedExtras
_MIN_RANDOMIZED_BYTE: MemoryOffset = min(extra.get_shop_slot_byte() for extra in _ALL_RECEIVABLE_EXTRAS)
_MAX_RANDOMIZED_BYTE: MemoryOffset = max(extra.get_shop_slot_byte() for extra in _ALL_RECEIVABLE_EXTRAS)
# Min and max are inclusive, so `+ 1` is needed.
_RANDOMIZED_BYTES_RANGE = range(_MIN_RANDOMIZED_BYTE, _MAX_RANDOMIZED_BYTE + 1)
_NUM_RANDOMIZED_BYTES = len(_RANDOMIZED_BYTES_RANGE)


def _make_extras_randomized_bits() -> tuple[dict[MemoryOffset, set[BitMask]], tuple[Extra, ...]]:
    # Initialize to all bits randomized, then update by removing non-randomized bits.
    non_randomized_bits_in_randomized_bytes: dict[MemoryOffset, set[BitMask]] = {
        i: {1, 2, 4, 8, 16, 32, 64, 128} for i in _RANDOMIZED_BYTES_RANGE
    }

    # Remove bits that are randomized.
    for extra in _ALL_RECEIVABLE_EXTRAS:
        non_randomized_bits_in_randomized_bytes[extra.get_shop_slot_byte()].remove(extra.get_shop_slot_mask())

    # Remove bytes with all bits randomized.
    non_randomized_bits_in_randomized_bytes = {i: bits for i, bits in non_randomized_bits_in_randomized_bytes.items()
                                               if bits}

    # The bytes that remain should be only those that are partially randomized. It is not expected for there to be any
    # bytes that are not randomized at all.
    randomized_extras_in_partially_randomized_bytes: tuple[Extra, ...] = tuple([
        extra for extra in _ALL_RECEIVABLE_EXTRAS
        if extra.get_shop_slot_byte() in non_randomized_bits_in_randomized_bytes
    ])

    return non_randomized_bits_in_randomized_bytes, randomized_extras_in_partially_randomized_bytes


_NON_RANDOMIZED_BITS_IN_RANDOMIZED_BYTES: dict[MemoryOffset, set[BitMask]]
_RANDOMIZED_EXTRAS_IN_PARTIALLY_RANDOMIZED_BYTES: tuple[Extra, ...]
_NON_RANDOMIZED_BITS_IN_RANDOMIZED_BYTES, _RANDOMIZED_EXTRAS_IN_PARTIALLY_RANDOMIZED_BYTES = (
    _make_extras_randomized_bits()
)

_START_ADDRESS = _UNLOCKED_EXTRAS_ADDRESS + _MIN_RANDOMIZED_BYTE
# 6 bytes are needed (44 // 8 = 5, 44 % 8 != 0)
_CUSTOM_SAVE_DATA_ENABLED_EXTRAS_LENGTH = 6
assert _CUSTOM_SAVE_DATA_ENABLED_EXTRAS_LENGTH == CustomSaveFlags2.enabled_extras_bits.size


class AcquiredExtras(ItemReceiver):
    receivable_ap_ids = _RECEIVABLE_EXTRAS_BY_AP_ID
    unlocked_extras: bytearray
    _restored_enabled_extras: bool = False

    def __init__(self):
        self.unlocked_extras = bytearray(_NUM_RANDOMIZED_BYTES)

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent) -> None:
        self.clear_received_items()

        # Restore enabled Extras from save data, but only once per new multiworld+slot connection.
        if not event.first_time_setup and not self._restored_enabled_extras:
            self.restore_enabled_extras_from_save_data(event.context)
        self._restored_enabled_extras = True

    @subscribe_event
    def on_level_change(self, event: OnLevelChangeEvent) -> None:
        # It was tried to save enabled Extras when the Area changes to Area.MAP (the Cantina), but it seems this can be
        # too late because the game is typically already done saving the save data to file at that point.
        # Instead, the enabled Extras are now saved when entering a Status level, which always precedes entering
        # Area.MAP.
        if event.new_level_id in Level and Level(event.new_level_id).is_status():
            self.save_enabled_extras_to_save_data(event.context)

    def clear_received_items(self) -> None:
        # Clearing unlocked extras is necessary because Score Multiplier unlocks are usually progressive. Additionally,
        # to give the player the correct number of studs when receiving a Stud item, the maximum active score
        # multiplier, at the time of receiving the Stud, must be known.
        self.unlocked_extras = bytearray(_NUM_RANDOMIZED_BYTES)

    # Here for reference.
    # def is_extra_unlocked(self, extra: ExtraData) -> bool:
    #     return (self.unlocked_extras[extra.shop_slot_byte + _MIN_RANDOMIZED_BYTE] & extra.shop_slot_bit_mask) != 0

    # Here for reference.
    # def lock_extra(self, extra: ExtraData):
    #     self.unlocked_extras[extra.shop_slot_byte + self._MIN_RANDOMIZED_BYTE] &= ~extra.shop_slot_bit_mask

    def unlock_extra(self, extra: Extra):
        _DEBUG_LOGGER.info("Unlocking extra %s", extra.name)
        byte_index = extra.get_shop_slot_byte() - _MIN_RANDOMIZED_BYTE
        self.unlocked_extras[byte_index] |= extra.get_shop_slot_mask()

    def receive_extra(self, ap_item_id: int):
        """Receive an Extra from AP, to be given to the player the next time the game state is updated."""
        if ap_item_id not in _RECEIVABLE_EXTRAS_BY_AP_ID:
            _LOGGER.warning("Tried to receive unknown extra with item ID %i", ap_item_id)
            return

        self.unlock_extra(_RECEIVABLE_EXTRAS_BY_AP_ID[ap_item_id])

    @staticmethod
    def restore_enabled_extras_from_save_data(ctx: TCSContext) -> None:
        # todo: In the future, there will also need to be a ban of some Extras in
        #  Challenges/Minikit Bonuses/Character Bonuses/Bounty Hunter Missions.
        # If the player is in LEGO City or similar, prevent enabling score multipliers and other extras that are
        #  banned from these levels.
        banned_extras = set()
        # fixme: The slot data event may fire before the current area address is updated. The current area should update
        #  whenever the client is connected to the game (before connecting to a server), and subscribers to the event
        #  should need to check if the slot data has been received and processed yet.
        current_p_area_data = CURRENT_P_AREA_DATA_ADDRESS.get(ctx)
        if current_p_area_data:
            current_area_id = AREA_DATA_ID.get(ctx, current_p_area_data)
            current_area = Area(current_area_id) if current_area_id in Area else None
            if current_area in (Area.BONUS, Area.BONUS2):
                banned_extras.update((
                    Extra.STUD_MAGNET,
                    Extra.CHARACTER_STUDS,
                    Extra.SCORE_X2,
                    Extra.SCORE_X4,
                    Extra.SCORE_X6,
                    Extra.SCORE_X8,
                    Extra.SCORE_X10,
                    Extra.POO_MONEY,
                ))

        base_addr = CustomSaveFlags2.get_addr(CustomSaveFlags2.enabled_extras_bits)
        extra_bits = ctx.read_bytes(base_addr, _CUSTOM_SAVE_DATA_ENABLED_EXTRAS_LENGTH)
        for extra in Extra:
            should_be_enabled = (
                    extra not in banned_extras
                    and extra_bits[extra.get_shop_slot_byte()] & extra.get_shop_slot_mask() != 0
            )
            to_write = 1 if should_be_enabled else 0
            ctx.write_byte(extra.get_enabled_address(), to_write)

    @staticmethod
    def save_enabled_extras_to_save_data(ctx: TCSContext) -> None:
        custom_save_data_array = bytearray(_CUSTOM_SAVE_DATA_ENABLED_EXTRAS_LENGTH)
        for extra in Extra:
            is_enabled = bool(ctx.read_uchar(extra.get_enabled_address()))
            if is_enabled:
                custom_save_data_array[extra.get_shop_slot_byte()] |= extra.get_shop_slot_mask()
        base_addr = CustomSaveFlags2.get_addr(CustomSaveFlags2.enabled_extras_bits)
        ctx.write_bytes(base_addr, bytes(custom_save_data_array), len(custom_save_data_array))

    @subscribe_event
    async def update_game_state(self, event: OnGameWatcherTickEvent):
        """
        Update the game memory that stores which Extras are unlocked, with all the currently unlocked/locked extras
        according to Archipelago.

        This is done constantly because the game has not been modified to prevent purchasing an Extra from the shop from
        unlocking that Extra. Purchased Extras also normally unlock themselves again when entering the Cantina.
        """
        ctx = event.context
        # Create a copy so that `self.unlocked_extras` always represents only what has been received from Archipelago.
        unlocked_extras_copy = self.unlocked_extras.copy()

        # Retrieve the current bytes so that non-randomized bits can be maintained.
        current_unlocked_extras = ctx.read_bytes(_START_ADDRESS, _NUM_RANDOMIZED_BYTES)

        # Set all bytes that are only partially randomized or are not randomized at all.
        for i in _NON_RANDOMIZED_BITS_IN_RANDOMIZED_BYTES.keys():
            byte_index = i - _MIN_RANDOMIZED_BYTE
            unlocked_extras_copy[byte_index] = current_unlocked_extras[byte_index]

        # Merge in all bits of partially randomized bytes.
        for extra in _RANDOMIZED_EXTRAS_IN_PARTIALLY_RANDOMIZED_BYTES:
            byte_index = extra.get_shop_slot_byte() - _MIN_RANDOMIZED_BYTE
            # If the bit is set:
            if self.unlocked_extras[byte_index] & extra.get_shop_slot_mask():
                # Set the bit in `unlocked_extras_copy`.
                unlocked_extras_copy[byte_index] |= extra.get_shop_slot_mask()
            else:
                # Clear the bit in `unlocked_extras_copy`.
                unlocked_extras_copy[byte_index] &= ~extra.get_shop_slot_mask()

        # If the player is in the Extras shop in the Cantina, temporarily disable the Extra that is currently active
        # in the Extras shop, so that it is possible to buy that extra, if it is unlocked, but not purchased.
        if ctx.is_in_shop(ShopType.EXTRAS):
            active_shop_index = _EXTRAS_SHOP_ACTIVE_INDEX_ADDRESS.get(ctx)
            extra_byte = active_shop_index // 8
            extra_bit_mask = 1 << (active_shop_index % 8)

            # Check if the Extra at the current shop slot is in the range of bytes for randomized Extras.
            if extra_byte in _RANDOMIZED_BYTES_RANGE:
                # Check if the Extra at the current shop slot is already unlocked.
                byte_index = extra_byte - _MIN_RANDOMIZED_BYTE
                if self.unlocked_extras[byte_index] & extra_bit_mask:
                    # Check if the Extra at the current shop slot has not been purchased.
                    extras_shop_byte = ctx.read_uchar(EXTRAS_SHOP_START + extra_byte)
                    if not (extras_shop_byte & extra_bit_mask):
                        # The Extra is unlocked, but not purchased yet, so lock it temporarily to allow the purchase.
                        unlocked_extras_copy[byte_index] &= ~extra_bit_mask

        # Write the updated extras array.
        ctx.write_bytes(_START_ADDRESS, bytes(unlocked_extras_copy), _NUM_RANDOMIZED_BYTES)

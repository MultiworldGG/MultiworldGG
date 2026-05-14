import logging
from typing import Mapping, Sequence

from ..common_addresses import ShopType, EXTRAS_SHOP_START
from ..events import subscribe_event, OnReceiveSlotDataEvent, OnGameWatcherTickEvent
from ..type_aliases import ApItemId, BitMask, MemoryOffset
from ...items import ExtraData, EXTRAS_BY_NAME
from . import ItemReceiver


logger = logging.getLogger("Client")
debug_logger = logging.getLogger("TCS Debug")


UNLOCKED_EXTRAS_ADDRESS = 0x86e4e8
"""Memory address of the array that stores which Extras are unlocked."""

# EXTRAS_SHOP_LENGTH_BYTES = 6  # 0xB8 to 0xBD
# Active slot in the shop, which displays its name and will be purchased if the player presses the use key
# Note: The previous 2 and next 2 shop indices are before/after this in memory (5 on screen at once).
EXTRAS_SHOP_ACTIVE_INDEX_ADDRESS = 0x87bf2c


RECEIVABLE_EXTRAS_BY_AP_ID: Mapping[ApItemId, ExtraData] = {
    extra.code: extra for extra in EXTRAS_BY_NAME.values() if extra.code != -1
}
ALL_RECEIVABLE_EXTRAS: Sequence[ExtraData] = [
    *RECEIVABLE_EXTRAS_BY_AP_ID.values(),
    # Score multipliers are applied progressively depending on the number of "Progressive Score Multiplier"
    # received, so are not receivable AP items currently.
    EXTRAS_BY_NAME["Score x2"],
    EXTRAS_BY_NAME["Score x4"],
    EXTRAS_BY_NAME["Score x6"],
    EXTRAS_BY_NAME["Score x8"],
    EXTRAS_BY_NAME["Score x10"],
]

# All bytes in the UnlockedExtras
MIN_RANDOMIZED_BYTE: MemoryOffset = min(extra.shop_slot_byte for extra in ALL_RECEIVABLE_EXTRAS)
MAX_RANDOMIZED_BYTE: MemoryOffset = max(extra.shop_slot_byte for extra in ALL_RECEIVABLE_EXTRAS)
# Min and max are inclusive, so `+ 1` is needed.
RANDOMIZED_BYTES_RANGE = range(MIN_RANDOMIZED_BYTE, MAX_RANDOMIZED_BYTE + 1)
NUM_RANDOMIZED_BYTES = len(RANDOMIZED_BYTES_RANGE)


def _make_extras_randomized_bits() -> tuple[dict[MemoryOffset, set[BitMask]], tuple[ExtraData, ...]]:
    # Initialize to all bits randomized, then update by removing non-randomized bits.
    non_randomized_bits_in_randomized_bytes: dict[MemoryOffset, set[BitMask]] = {
        i: {1, 2, 4, 8, 16, 32, 64, 128} for i in RANDOMIZED_BYTES_RANGE
    }

    # Remove bits that are randomized.
    for extra in ALL_RECEIVABLE_EXTRAS:
        non_randomized_bits_in_randomized_bytes[extra.shop_slot_byte].remove(extra.shop_slot_bit_mask)

    # Remove bytes with all bits randomized.
    non_randomized_bits_in_randomized_bytes = {i: bits for i, bits in non_randomized_bits_in_randomized_bytes.items()
                                               if bits}

    # The bytes that remain should be only those that are partially randomized. It is not expected for there to be any
    # bytes that are not randomized at all.
    randomized_extras_in_partially_randomized_bytes: tuple[ExtraData, ...] = tuple([
        extra for extra in ALL_RECEIVABLE_EXTRAS
        if extra.shop_slot_byte in non_randomized_bits_in_randomized_bytes
    ])

    return non_randomized_bits_in_randomized_bytes, randomized_extras_in_partially_randomized_bytes


NON_RANDOMIZED_BITS_IN_RANDOMIZED_BYTES: dict[MemoryOffset, set[BitMask]]
RANDOMIZED_EXTRAS_IN_PARTIALLY_RANDOMIZED_BYTES: tuple[ExtraData, ...]
NON_RANDOMIZED_BITS_IN_RANDOMIZED_BYTES, RANDOMIZED_EXTRAS_IN_PARTIALLY_RANDOMIZED_BYTES = (
    _make_extras_randomized_bits()
)

START_ADDRESS = UNLOCKED_EXTRAS_ADDRESS + MIN_RANDOMIZED_BYTE


class AcquiredExtras(ItemReceiver):
    receivable_ap_ids = RECEIVABLE_EXTRAS_BY_AP_ID
    unlocked_extras: bytearray

    def __init__(self):
        self.unlocked_extras = bytearray(NUM_RANDOMIZED_BYTES)

    @subscribe_event
    def init_from_slot_data(self, _event: OnReceiveSlotDataEvent) -> None:
        self.clear_received_items()

    def clear_received_items(self) -> None:
        # Clearing unlocked extras is necessary because Score Multiplier unlocks are usually progressive. Additionally,
        # to give the player the correct number of studs when receiving a Stud item, the maximum active score
        # multiplier, at the time of receiving the Stud, must be known.
        self.unlocked_extras = bytearray(NUM_RANDOMIZED_BYTES)

    # Here for reference.
    # def is_extra_unlocked(self, extra: ExtraData) -> bool:
    #     return (self.unlocked_extras[extra.shop_slot_byte + MIN_RANDOMIZED_BYTE] & extra.shop_slot_bit_mask) != 0

    # Here for reference.
    # def lock_extra(self, extra: ExtraData):
    #     self.unlocked_extras[extra.shop_slot_byte + self.MIN_RANDOMIZED_BYTE] &= ~extra.shop_slot_bit_mask

    def unlock_extra(self, extra: ExtraData):
        debug_logger.info("Unlocking extra %s", extra.name)
        byte_index = extra.shop_slot_byte - MIN_RANDOMIZED_BYTE
        self.unlocked_extras[byte_index] |= extra.shop_slot_bit_mask

    def receive_extra(self, ap_item_id: int):
        """Receive an Extra from AP, to be given to the player the next time the game state is updated."""
        if ap_item_id not in RECEIVABLE_EXTRAS_BY_AP_ID:
            logger.warning("Tried to receive unknown extra with item ID %i", ap_item_id)
            return

        self.unlock_extra(RECEIVABLE_EXTRAS_BY_AP_ID[ap_item_id])

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
        current_unlocked_extras = ctx.read_bytes(START_ADDRESS, NUM_RANDOMIZED_BYTES)

        # Set all bytes that are only partially randomized or are not randomized at all.
        for i in NON_RANDOMIZED_BITS_IN_RANDOMIZED_BYTES.keys():
            byte_index = i - MIN_RANDOMIZED_BYTE
            unlocked_extras_copy[byte_index] = current_unlocked_extras[byte_index]

        # Merge in all bits of partially randomized bytes.
        for extra in RANDOMIZED_EXTRAS_IN_PARTIALLY_RANDOMIZED_BYTES:
            byte_index = extra.shop_slot_byte - MIN_RANDOMIZED_BYTE
            # If the bit is set:
            if self.unlocked_extras[byte_index] & extra.shop_slot_bit_mask:
                # Set the bit in `unlocked_extras_copy`.
                unlocked_extras_copy[byte_index] |= extra.shop_slot_bit_mask
            else:
                # Clear the bit in `unlocked_extras_copy`.
                unlocked_extras_copy[byte_index] &= ~extra.shop_slot_bit_mask

        # If the player is in the Extras shop in the Cantina, temporarily disable the Extra that is currently active
        # in the Extras shop, so that it is possible to buy that extra, if it is unlocked, but not purchased.
        if ctx.is_in_shop(ShopType.EXTRAS):
            active_shop_index = ctx.read_uchar(EXTRAS_SHOP_ACTIVE_INDEX_ADDRESS)
            extra_byte = active_shop_index // 8
            extra_bit_mask = 1 << (active_shop_index % 8)

            # Check if the Extra at the current shop slot is in the range of bytes for randomized Extras.
            if extra_byte in RANDOMIZED_BYTES_RANGE:
                # Check if the Extra at the current shop slot is already unlocked.
                byte_index = extra_byte - MIN_RANDOMIZED_BYTE
                if self.unlocked_extras[byte_index] & extra_bit_mask:
                    # Check if the Extra at the current shop slot has not been purchased.
                    extras_shop_byte = ctx.read_uchar(EXTRAS_SHOP_START + extra_byte)
                    if not (extras_shop_byte & extra_bit_mask):
                        # The Extra is unlocked, but not purchased yet, so lock it temporarily to allow the purchase.
                        unlocked_extras_copy[byte_index] &= ~extra_bit_mask

        # Write the updated extras array.
        ctx.write_bytes(START_ADDRESS, bytes(unlocked_extras_copy), NUM_RANDOMIZED_BYTES)

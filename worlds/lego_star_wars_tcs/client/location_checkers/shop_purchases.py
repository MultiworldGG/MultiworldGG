import abc

from ..common_addresses import CHARACTERS_SHOP_START, EXTRAS_SHOP_START
from ..type_aliases import MemoryAddress, MemoryOffset, BitMask, ApLocationId, TCSContext

from ...data.extras import Extra
from ...data.locations import LOCATION_NAME_TO_ID
from ...data.shop import CHARACTER_SHOP_SLOTS


class _BasePurchasesChecker(abc.ABC):
    remaining_purchases: dict[MemoryOffset, dict[BitMask, ApLocationId]]
    starting_min_byte: int
    starting_max_byte: int

    @property
    @abc.abstractmethod
    def shop_address(self) -> MemoryAddress: ...

    @property
    @abc.abstractmethod
    def shop_offsets_to_ap_location_ids(self) -> dict[MemoryOffset, dict[BitMask, ApLocationId]]: ...

    def __init__(self):
        self.remaining_purchases = {byte_offset: bit_mask_to_ap_id.copy() for byte_offset, bit_mask_to_ap_id
                                    in self.shop_offsets_to_ap_location_ids.items()}
        self.starting_min_byte = min(self.remaining_purchases.keys())
        self.starting_max_byte = max(self.remaining_purchases.keys())

    async def check_extra_purchases(self, ctx: TCSContext, new_location_checks: list[int]):
        updated_remaining_purchases: dict[MemoryOffset, dict[BitMask, ApLocationId]] = {}
        collected_checks: dict[MemoryOffset, BitMask] = {}
        for byte_offset, bit_mask_to_ap_id in self.remaining_purchases.items():
            updated_bit_to_ap_id: dict[BitMask, ApLocationId] = {}
            for bit, ap_id in bit_mask_to_ap_id.items():
                if ctx.is_location_sendable(ap_id):
                    if ctx.is_location_unchecked(ap_id):
                        # The location has not been checked, so still needs to be read from memory to see if it has been
                        # completed in-game.
                        updated_bit_to_ap_id[bit] = ap_id
                    else:
                        # For !collect and same-slot co-op support, mark collected checks as purchased, even if the
                        # player has not purchased them.
                        if byte_offset in collected_checks:
                            collected_checks[byte_offset] |= bit
                        else:
                            collected_checks[byte_offset] = bit

            if updated_bit_to_ap_id:
                updated_remaining_purchases[byte_offset] = updated_bit_to_ap_id

        if updated_remaining_purchases or collected_checks:
            # Start the min and max as the most extreme opposite values.
            min_byte_offset = self.starting_max_byte
            max_byte_offset = self.starting_min_byte
            if updated_remaining_purchases:
                min_byte_offset = min(min_byte_offset, min(updated_remaining_purchases.keys()))
                max_byte_offset = max(max_byte_offset, max(updated_remaining_purchases.keys()))
            if collected_checks:
                min_byte_offset = min(min_byte_offset, min(collected_checks.keys()))
                max_byte_offset = max(max_byte_offset, max(collected_checks.keys()))
            num_bytes = max_byte_offset - min_byte_offset + 1

            # Pre-offset the byte offsets to reduce the time spent between reading the bytes and writing the modified
            # bytes back to the game.
            collected_checks_offset = {byte_offset - min_byte_offset: bit_mask
                                       for byte_offset, bit_mask in collected_checks.items()}
            characters_shop_bytes = ctx.read_bytes(self.shop_address + min_byte_offset, num_bytes)
            if collected_checks_offset:
                characters_shop_bytes_array = bytearray(characters_shop_bytes)
                for byte_offset, bit_mask in collected_checks_offset.items():
                    # Set the bits for collected shop locations.
                    characters_shop_bytes_array[byte_offset] |= bit_mask
                # Write the updated bytes back to the game as fast as possible to reduce the chance of someone buying
                # from the shop during the time between reading the bytes and writing the bytes.
                # If this is actually a problem, then checking for purchases could be disabled while the shop is open.
                # NOTE: Requires a reload of the Cantina to take effect.
                ctx.write_bytes(self.shop_address + min_byte_offset, bytes(characters_shop_bytes_array), num_bytes)

            # Read from the bytes to see if any new purchases have been made and need to send location checks to AP.
            for byte_offset, bit_mask_to_ap_id in updated_remaining_purchases.items():
                shop_byte = characters_shop_bytes[byte_offset - min_byte_offset]
                for bit_mask, ap_id in bit_mask_to_ap_id.items():
                    if shop_byte & bit_mask:
                        new_location_checks.append(ap_id)
        self.remaining_purchases = updated_remaining_purchases


def _characters_to_shop_address() -> dict[MemoryOffset, dict[BitMask, ApLocationId]]:
    per_byte: dict[MemoryOffset, dict[BitMask, ApLocationId]] = {}
    
    for i, character in enumerate(CHARACTER_SHOP_SLOTS):
        byte_offset = i // 8
        bit_mask = 1 << (i % 8)
        location_name = character.get_purchase_location_name()
        location_id = LOCATION_NAME_TO_ID[location_name]
        per_byte.setdefault(byte_offset, {})[bit_mask] = location_id
    return per_byte


def _extras_to_shop_address() -> dict[MemoryOffset, dict[BitMask, ApLocationId]]:
    """Purchase <extra> shop ID -> AP Location ID"""
    per_byte: dict[MemoryOffset, dict[BitMask, ApLocationId]] = {}

    for extra in Extra:
        cost = extra.purchase_cost
        if cost is None:
            continue
        byte_offset = extra.get_shop_slot_byte()
        bit_mask = extra.get_shop_slot_mask()
        location_name = extra.get_purchase_location_name()
        location_id = LOCATION_NAME_TO_ID[location_name]
        per_byte.setdefault(byte_offset, {})[bit_mask] = location_id
    return per_byte


class PurchasedCharactersChecker(_BasePurchasesChecker):
    shop_offsets_to_ap_location_ids = _characters_to_shop_address()
    shop_address = CHARACTERS_SHOP_START


# todo: Read from slot_data whether the non-power-brick Extras are enabled as checks, and only include them in
#  `shop_offsets_to_ap_location_ids` when they are. This would also require ..game_state_modifiers.extras to read the
#  same information, and not remove the non-power-bricks from the player's unlocked items (the generator would also need
#  to be modified to turn the non-power-brick Extras and their vanilla locations into events.
class PurchasedExtrasChecker(_BasePurchasesChecker):
    shop_offsets_to_ap_location_ids = _extras_to_shop_address()
    shop_address = EXTRAS_SHOP_START

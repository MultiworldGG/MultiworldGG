import logging
from typing import cast

from ..common import StaticUChar
from ..common_addresses import CHARACTERS_SHOP_START, ShopType
from ..events import subscribe_event, OnReceiveSlotDataEvent, OnGameWatcherTickEvent
from ..type_aliases import TCSContext, ApItemId
from . import ItemReceiver

from ...data.characters import Character, UnlockMethod
from ...data.items.all_character_items import SENDABLE_CHARACTER_TO_ITEM_DATA
from ...data.shop import CHARACTER_SHOP_SLOTS


_UNLOCKED_CHARACTERS_ADDRESS = 0x86e5e0
_CHARACTERS_SHOP_ACTIVE_INDEX_ADDRESS = StaticUChar(0x87be18)

# 0b01 controls whether the character shows in the Free Play character picker.
# 0b10's use is unknown, but seemingly all unlocked characters use both bits.
UNLOCKED = 0b11
LOCKED = 0b0


_RECEIVABLE_CHARACTERS_BY_AP_ID: dict[ApItemId, Character] = cast(dict[ApItemId, Character], {
    v.code: k for k, v in SENDABLE_CHARACTER_TO_ITEM_DATA.items()
})

_MIN_RANDOMIZED_BYTE: int = min(_RECEIVABLE_CHARACTERS_BY_AP_ID.values())
_MAX_RANDOMIZED_BYTE: int = max(_RECEIVABLE_CHARACTERS_BY_AP_ID.values())
# Min and max are inclusive, so `+ 1` is needed.
_RANDOMIZED_BYTES_RANGE: range = range(_MIN_RANDOMIZED_BYTE, _MAX_RANDOMIZED_BYTE + 1)
_NUM_RANDOMIZED_BYTES: int = len(_RANDOMIZED_BYTES_RANGE)
_START_ADDRESS: int = _UNLOCKED_CHARACTERS_ADDRESS + _MIN_RANDOMIZED_BYTE
# Each Character Shop index to the character index of the Character in that slot.
_SHOP_INDEX_TO_CHARACTER_INDEX: dict[int, Character] = dict(enumerate(CHARACTER_SHOP_SLOTS))

_SHOP_INDICES_UNLOCKED_WHEN_ALL_EPISODES_UNLOCKED: set[int] = {
    i for i, character in enumerate(CHARACTER_SHOP_SLOTS)
    if character.unlock_method is UnlockMethod.ALL_EPISODES_COMPLETE
}


logger = logging.getLogger("Client")


class AcquiredCharacters(ItemReceiver):
    receivable_ap_ids = _RECEIVABLE_CHARACTERS_BY_AP_ID

    # Buying a character from the shop unlocks a character even though it shouldn't because it is supposed to be a
    # randomized location check, so unlockable characters need to be reset occasionally.
    # Sometimes, unlocking a character will let the player immediately switch to that character while in Free Play, so
    # this game state modifier should be run even outside the Cantina.
    # Completing a story mode level will also probably unlock a character, maybe only if the story mode has not already
    # been completed, but this game state modifier will disable any characters unlocked this way that should not be
    # unlocked.
    unlocked_characters: set[Character]

    def __init__(self):
        self.unlocked_characters = set()

    @subscribe_event
    def init_from_slot_data(self, _event: OnReceiveSlotDataEvent) -> None:
        self.clear_received_items()

    def clear_received_items(self) -> None:
        # Characters are not progressive, so receiving a character again has no effect, but for consistency, clear them
        # anyway.
        self.unlocked_characters.clear()

    def unlock_character(self, character: Character):
        self.unlocked_characters.add(character)

    def receive_character(self, ap_item_id: int):
        """Receive a Character from AP, to be given to the player the next time the game state is updated."""
        if ap_item_id not in _RECEIVABLE_CHARACTERS_BY_AP_ID:
            logger.warning("Tried to receive unknown character with item ID %i", ap_item_id)
            return

        char = _RECEIVABLE_CHARACTERS_BY_AP_ID[ap_item_id]

        # While there are not normally duplicate characters, receiving duplicates does nothing.
        self.unlock_character(char)

    @staticmethod
    def is_all_episodes_character_selected_in_shop(ctx: TCSContext) -> bool:
        return (ctx.is_in_shop(ShopType.CHARACTERS)
                and _CHARACTERS_SHOP_ACTIVE_INDEX_ADDRESS.get(ctx) in _SHOP_INDICES_UNLOCKED_WHEN_ALL_EPISODES_UNLOCKED)

    @subscribe_event
    async def update_game_state(self, event: OnGameWatcherTickEvent) -> None:
        """
        Update the game memory that stores which Characters are unlocked, with all the currently unlocked/locked
        Characters according to Archipelago.

        This is done constantly because the game has not been modified to disable vanilla Character unlocks from Story
        completion, shop purchases and other means (see CHARS/COLLECTION.TXT in an unpacked game).

        At least already purchased Characters do not re-unlock themselves automatically like with already purchased
        Extras.
        """
        # todo: See if there is a performance hit to doing all 137 (or more once we add more vehicles) writes
        #  separately. It would technically be safer.
        ctx = event.context
        chars = ctx.read_bytes(_START_ADDRESS, _NUM_RANDOMIZED_BYTES)
        chars_array = bytearray(chars)

        for char in _RECEIVABLE_CHARACTERS_BY_AP_ID.values():
            byte_index = char - _MIN_RANDOMIZED_BYTE
            if char in self.unlocked_characters:
                # 0b01 controls whether the character shows in the Free Play character picker.
                # 0b10's use is unknown, but seemingly all unlocked characters use both bits.
                chars_array[byte_index] = UNLOCKED
            else:
                chars_array[byte_index] = LOCKED

        # If the player is in the Character Shop, temporarily lock the character they have selected for purchase if that
        # Character has already been unlocked through receiving that Character from Archipelago.
        if ctx.is_in_shop(ShopType.CHARACTERS):
            current_character_shop_slot_index = _CHARACTERS_SHOP_ACTIVE_INDEX_ADDRESS.get(ctx)
            slot_byte = current_character_shop_slot_index // 8
            slot_bit_mask = 1 << (current_character_shop_slot_index % 8)

            character_index_for_slot = _SHOP_INDEX_TO_CHARACTER_INDEX[current_character_shop_slot_index]

            # Check if the Character at the currents shop slot is in the range of bytes for randomized Characters.
            if character_index_for_slot in _RANDOMIZED_BYTES_RANGE:
                # Check if the Character at the current shop slot is already unlocked.
                byte_index = character_index_for_slot - _MIN_RANDOMIZED_BYTE
                if chars_array[byte_index] == UNLOCKED:
                    # Check if the Character at the current shop slot has not been purchased.
                    character_shop_byte = ctx.read_uchar(CHARACTERS_SHOP_START + slot_byte)
                    if not (character_shop_byte & slot_bit_mask):
                        # The Character is unlocked, but not purchased yet, so lock the character temporarily to allow
                        # purchase.
                        chars_array[byte_index] = LOCKED

        ctx.write_bytes(_START_ADDRESS, bytes(chars_array), _NUM_RANDOMIZED_BYTES)

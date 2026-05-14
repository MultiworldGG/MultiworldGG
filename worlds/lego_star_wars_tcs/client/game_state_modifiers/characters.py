import logging

from ..common_addresses import CHARACTERS_SHOP_START, ShopType
from ..events import subscribe_event, OnReceiveSlotDataEvent, OnGameWatcherTickEvent
from ..type_aliases import TCSContext, ApItemId
from ...items import CHARACTERS_AND_VEHICLES_BY_NAME, GenericCharacterData, CHARACTER_SHOP_SLOTS
from . import ItemReceiver


UNLOCKED_CHARACTERS_ADDRESS = 0x86e5e0
CHARACTERS_SHOP_ACTIVE_INDEX_ADDRESS = 0x87be18

# 0b01 controls whether the character shows in the Free Play character picker.
# 0b10's use is unknown, but seemingly all unlocked characters use both bits.
UNLOCKED = 0b11
LOCKED = 0b0


RECEIVABLE_CHARACTERS_BY_AP_ID: dict[ApItemId, GenericCharacterData] = {
    extra.code: extra for extra in CHARACTERS_AND_VEHICLES_BY_NAME.values() if extra.code != -1
}
MIN_RANDOMIZED_BYTE: int = min(char.character_index for char in RECEIVABLE_CHARACTERS_BY_AP_ID.values())
MAX_RANDOMIZED_BYTE: int = max(char.character_index for char in RECEIVABLE_CHARACTERS_BY_AP_ID.values())
# Min and max are inclusive, so `+ 1` is needed.
RANDOMIZED_BYTES_RANGE: range = range(MIN_RANDOMIZED_BYTE, MAX_RANDOMIZED_BYTE + 1)
NUM_RANDOMIZED_BYTES: int = len(RANDOMIZED_BYTES_RANGE)
START_ADDRESS: int = UNLOCKED_CHARACTERS_ADDRESS + MIN_RANDOMIZED_BYTE
CHARACTER_TO_SHOP_INDEX: dict[str, int] = {name: i for i, name in enumerate(CHARACTER_SHOP_SLOTS.keys())}
# Each Character Shop index to the character index of the Character in that slot.
SHOP_INDEX_TO_CHARACTER_INDEX: dict[int, int] = {
    i: CHARACTERS_AND_VEHICLES_BY_NAME[name].character_index for name, i in CHARACTER_TO_SHOP_INDEX.items()
}

SHOP_INDICES_UNLOCKED_WHEN_ALL_EPISODES_UNLOCKED: set[int] = {
    CHARACTER_TO_SHOP_INDEX[name] for name, (unlock_method, _studs_cost) in CHARACTER_SHOP_SLOTS.items()
    if unlock_method == "ALL_EPISODES"
}


logger = logging.getLogger("Client")


class AcquiredCharacters(ItemReceiver):
    receivable_ap_ids = RECEIVABLE_CHARACTERS_BY_AP_ID

    # Buying a character from the shop unlocks a character even though it shouldn't because it is supposed to be a
    # randomized location check, so unlockable characters need to be reset occasionally.
    # Sometimes, unlocking a character will let the player immediately switch to that character while in Free Play, so
    # this game state modifier should be run even outside the Cantina.
    # Completing a story mode level will also probably unlock a character, maybe only if the story mode has not already
    # been completed, but this game state modifier will disable any characters unlocked this way that should not be
    # unlocked.
    unlocked_characters: set[int]

    def __init__(self):
        self.unlocked_characters = set()

    @subscribe_event
    def init_from_slot_data(self, _event: OnReceiveSlotDataEvent) -> None:
        self.clear_received_items()

    def clear_received_items(self) -> None:
        # Characters are not progressive, so receiving a character again has no effect, but for consistency, clear them
        # anyway.
        self.unlocked_characters.clear()

    def unlock_character(self, character: GenericCharacterData):
        self.unlocked_characters.add(character.character_index)

    def receive_character(self, ap_item_id: int):
        """Receive a Character from AP, to be given to the player the next time the game state is updated."""
        if ap_item_id not in RECEIVABLE_CHARACTERS_BY_AP_ID:
            logger.warning("Tried to receive unknown character with item ID %i", ap_item_id)
            return

        char = RECEIVABLE_CHARACTERS_BY_AP_ID[ap_item_id]

        # While there are not normally duplicate characters, receiving duplicates does nothing.
        self.unlock_character(char)

    @staticmethod
    def is_all_episodes_character_selected_in_shop(ctx: TCSContext) -> bool:
        return (ctx.is_in_shop(ShopType.CHARACTERS)
                and ctx.read_uchar(
                    CHARACTERS_SHOP_ACTIVE_INDEX_ADDRESS) in SHOP_INDICES_UNLOCKED_WHEN_ALL_EPISODES_UNLOCKED)

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
        chars = ctx.read_bytes(START_ADDRESS, NUM_RANDOMIZED_BYTES)
        chars_array = bytearray(chars)

        for char in RECEIVABLE_CHARACTERS_BY_AP_ID.values():
            char_index = char.character_index
            byte_index = char_index - MIN_RANDOMIZED_BYTE
            if char_index in self.unlocked_characters:
                # 0b01 controls whether the character shows in the Free Play character picker.
                # 0b10's use is unknown, but seemingly all unlocked characters use both bits.
                chars_array[byte_index] = UNLOCKED
            else:
                chars_array[byte_index] = LOCKED

        # If the player is in the Character Shop, temporarily lock the character they have selected for purchase if that
        # Character has already been unlocked through receiving that Character from Archipelago.
        if ctx.is_in_shop(ShopType.CHARACTERS):
            current_character_shop_slot_index = ctx.read_uchar(CHARACTERS_SHOP_ACTIVE_INDEX_ADDRESS)
            slot_byte = current_character_shop_slot_index // 8
            slot_bit_mask = 1 << (current_character_shop_slot_index % 8)

            character_index_for_slot = SHOP_INDEX_TO_CHARACTER_INDEX[current_character_shop_slot_index]

            # Check if the Character at the currents shop slot is in the range of bytes for randomized Characters.
            if character_index_for_slot in RANDOMIZED_BYTES_RANGE:
                # Check if the Character at the current shop slot is already unlocked.
                byte_index = character_index_for_slot - MIN_RANDOMIZED_BYTE
                if chars_array[byte_index] == UNLOCKED:
                    # Check if the Character at the current shop slot has not been purchased.
                    character_shop_byte = ctx.read_uchar(CHARACTERS_SHOP_START + slot_byte)
                    if not (character_shop_byte & slot_bit_mask):
                        # The Character is unlocked, but not purchased yet, so lock the character temporarily to allow
                        # purchase.
                        chars_array[byte_index] = LOCKED

        ctx.write_bytes(START_ADDRESS, bytes(chars_array), NUM_RANDOMIZED_BYTES)

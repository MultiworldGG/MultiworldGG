import logging
from dataclasses import dataclass
from enum import IntEnum

from . import ClientComponent
from ..events import subscribe_event, OnGameWatcherTickEvent
from ..type_aliases import TCSContext


class TextId(IntEnum):
    DOUBLE_SCORE_ZONE = 87

    CHARACTER_NAME_R2_D2 = 103
    CHARACTER_NAME_C_3PO = 104

    # The names of each episode. These are always displayed by unlocked Episode doors in the Cantina.
    EPISODE_1_NAME = 561
    EPISODE_2_NAME = 1351
    EPISODE_3_NAME = 1360
    EPISODE_4_NAME = 501
    EPISODE_5_NAME = 521
    EPISODE_6_NAME = 541

    # Unlocked hints to mostly be used for information display, e.g. goal requirements.
    SHOP_UNLOCKED_HINT_1 = 630
    SHOP_UNLOCKED_HINT_2 = 631
    SHOP_UNLOCKED_HINT_3 = 632
    SHOP_UNLOCKED_HINT_4 = 633
    SHOP_UNLOCKED_HINT_5 = 634
    # Locked hints to probably be used for displaying in-game hints.
    SHOP_LOCKED_HINT_6 = 635
    SHOP_LOCKED_HINT_7 = 636
    SHOP_LOCKED_HINT_8 = 637
    SHOP_LOCKED_HINT_9 = 638
    SHOP_LOCKED_HINT_10 = 639
    SHOP_LOCKED_HINT_11 = 640
    SHOP_LOCKED_HINT_12 = 641
    SHOP_LOCKED_HINT_13 = 642
    SHOP_LOCKED_HINT_14 = 643

    SHOP_TYPE_HINTS = 660
    SHOP_TYPE_ENTER_CODE = 661

    # Auto-hints, could be used to display a variety of hints. Perhaps auto-hints related to a specific type of
    # character could give AP hints towards a character of that type.
    AUTO_HINT_1_HOW_TO_CHANGE_CHARACTER_FREE_PLAY = 600
    AUTO_HINT_2_HOW_TO_USE_FORCE = 601
    AUTO_HINT_3_HOW_TO_TAG_CHARACTERS = 602
    AUTO_HINT_4_HOW_TO_TAG_CHARACTERS2 = 603
    AUTO_HINT_5_HOW_TO_BUILD_LEGO = 604
    AUTO_HINT_6_HOW_TO_GET_INTO_VEHICLES = 605
    AUTO_HINT_7_HOW_TO_EXIT_VEHICLES = 606
    AUTO_HINT_8_HOW_TO_USE_DROID_PANELS = 607
    AUTO_HINT_9_HOW_TO_USE_IMPERIAL_PANELS = 608
    AUTO_HINT_10_HOW_TO_USE_BOUNTY_HUNTER_PANELS = 609
    AUTO_HINT_11_HOW_TO_USE_GRAPPLE_POINTS = 610
    AUTO_HINT_12_HOW_TO_RIDE_CREATURES = 611

    # The "Paused" text displayed below the name of the player that paused the game. Goal information is appended here.
    PAUSED = 705

    # Unused in the PC version. Being overwritten in locked_cantina_door_display.py.
    WII_MOTION_CONTROL_HINT_1 = 1675


logger = logging.getLogger("Client")
debug_logger = logging.getLogger("TCS Debug")

# char***
LOCALIZED_TEXT_ARRAY_POINTER = 0x926C20


@dataclass
class LocalizedStringData:
    address_of_pointer_to_vanilla_string: int
    pointer_to_vanilla_string: int
    vanilla_string: bytes
    pointer_to_allocated_string: int | None = None
    allocated_string_max_length: int | None = None
    last_set_allocated_string: bytes | None = None


EXPECTED_CHARACTER_NAME_R2_D2 = b"R2-D2\x00"
EXPECTED_CHARACTER_NAME_C_3PO = b"C-3PO\x00"

# As a safety measure, now more than this many bytes are ever allocated for a single string.
MAXIMUM_SAFE_ALLOCATE_SIZE = 1024


class TextReplacer(ClientComponent):
    localized_string_data: dict[int, LocalizedStringData]
    ctx: TCSContext

    _initialized: bool = False

    def __init__(self, ctx: TCSContext):
        self.localized_string_data = {}
        self.ctx = ctx

    def _ensure_localized_string_data(self, string_index: int) -> LocalizedStringData:
        if string_index in self.localized_string_data:
            return self.localized_string_data[string_index]
        ctx = self.ctx
        # char*** or the char** of the first string in the array.
        array_address = ctx.read_uint(LOCALIZED_TEXT_ARRAY_POINTER)
        # char**, the address of the pointer to the string
        address_of_pointer_to_vanilla_string = array_address + string_index * 4  # 4 bytes per pointer.
        # char*, the address of the first character in the string
        pointer_to_vanilla_string = ctx.read_uint(address_of_pointer_to_vanilla_string, raw=True)
        # The longest localized string looks to be one of the Russian strings, at 372 bytes. 512 should cover all
        # strings.
        vanilla_string_oversize = ctx.read_bytes(pointer_to_vanilla_string, 512, raw=True)
        vanilla_string = vanilla_string_oversize.partition(b"\x00")[0] + b"\x00"
        data = LocalizedStringData(address_of_pointer_to_vanilla_string, pointer_to_vanilla_string, vanilla_string)
        self.localized_string_data[string_index] = data
        return data

    # The notoriously long FFXIV meme item from ArchipIDLE is only 198 bytes.
    def _set_custom_bytes(self, string_index: int, replacement: bytes, minimum_allocate_size: int):
        # Sanity check minimum allocation size.
        if minimum_allocate_size > MAXIMUM_SAFE_ALLOCATE_SIZE:
            raise ValueError(f"minimum_allocate_size of {minimum_allocate_size} is too large. Maximum allowed is"
                             f" {MAXIMUM_SAFE_ALLOCATE_SIZE}")
        if minimum_allocate_size < 1:
            raise ValueError(f"minimum_allocate_size must be greater than zero, not {minimum_allocate_size}")

        # Sanity check replacement bytes.
        if len(replacement) > MAXIMUM_SAFE_ALLOCATE_SIZE:
            # Restrict the replacement to no larger than the maximum safe size.
            replacement = replacement[:MAXIMUM_SAFE_ALLOCATE_SIZE - 1] + b"\x00"

        vanilla_data = self._ensure_localized_string_data(string_index)

        pointer_to_allocated_string = vanilla_data.pointer_to_allocated_string
        minimum_allocate_size = max(len(replacement), minimum_allocate_size)
        if pointer_to_allocated_string is None:
            # This is the first custom allocation for this localized text string.
            pointer_to_allocated_string = self.ctx.allocate(minimum_allocate_size)
            vanilla_data.pointer_to_allocated_string = pointer_to_allocated_string
            vanilla_data.allocated_string_max_length = minimum_allocate_size
            # Replace where the vanilla pointer is found, with the pointer to the allocated data.
            self.ctx.write_uint(vanilla_data.address_of_pointer_to_vanilla_string,
                                pointer_to_allocated_string, raw=True)
        elif minimum_allocate_size > vanilla_data.allocated_string_max_length:
            # The new bytes won't fit in the old allocated memory, so re-allocate more memory and free the old memory.
            old_pointer_to_allocated_string = vanilla_data.pointer_to_allocated_string
            assert old_pointer_to_allocated_string is not None
            pointer_to_allocated_string = self.ctx.allocate(minimum_allocate_size)
            vanilla_data.pointer_to_allocated_string = pointer_to_allocated_string
            vanilla_data.allocated_string_max_length = minimum_allocate_size
            # Replace where the old pointer is found, with the pointer to the allocated data.
            self.ctx.write_uint(vanilla_data.address_of_pointer_to_vanilla_string,
                                pointer_to_allocated_string, raw=True)
            # Free the allocated memory for the old string.
            self.ctx.free(old_pointer_to_allocated_string)

        # Finally write the replacement bytes.
        if string_index in TextId:
            text_id = TextId(string_index)
            # debug_logger.info("Writing %s to %s", replacement, text_id.name)
        # else:
        #     debug_logger.info("Writing %s to Text ID %i", replacement, string_index)
        vanilla_data.last_set_allocated_string = replacement
        self.ctx.write_bytes(pointer_to_allocated_string, replacement, len(replacement), raw=True)

    def _get_custom_string(self, string_index: int) -> bytes | None:
        data = self.localized_string_data.get(string_index)
        if data is None:
            # No custom string has been set.
            return None
        else:
            return data.last_set_allocated_string

    def _get_vanilla_string(self, string_index: int) -> bytes:
        return self._ensure_localized_string_data(string_index).vanilla_string

    def _write_vanilla_string(self, string_index: int):
        data = self.localized_string_data.get(string_index)
        if data is None:
            # The string is already vanilla.
            return
        self._set_custom_bytes(string_index, data.vanilla_string, len(data.vanilla_string))

    # Public methods should always take TextId arguments if possible.

    def write_custom_string(self, string_index: TextId, replacement: str, minimum_allocate_size=256):
        replacement_bytes = replacement.encode("utf-8", "replace") + b"\x00"
        self._set_custom_bytes(string_index.value, replacement_bytes, minimum_allocate_size)

    def write_vanilla_string(self, string_index: TextId):
        self._write_vanilla_string(string_index.value)

    def write_raw_custom_string(self, localization_id: int, replacement: bytes, minimum_allocate_size=256):
        self._set_custom_bytes(localization_id, replacement, minimum_allocate_size)

    def write_raw_vanilla_string(self, localization_id: int):
        self._write_vanilla_string(localization_id)

    def suffix_custom_string(self, string_index: TextId, to_append: str, minimum_allocate_size=256):
        """Write a suffix string onto the end of the vanilla string."""
        self._set_custom_bytes(string_index.value,
                               self.get_vanilla_string(string_index).rstrip(b"\x00")
                               + to_append.encode("utf-8", "replace") + b"\x00",
                               minimum_allocate_size)

    def get_vanilla_string(self, string_index: TextId) -> bytes:
        return self._get_vanilla_string(string_index.value)

    @subscribe_event
    async def update_game_state(self, _event: OnGameWatcherTickEvent) -> None:
        # todo: This initialization check should be done when the client connects to the game.
        if not self._initialized:
            # Check that the R2-D2 and C-3PO strings match what is expected. These strings are the same in every
            # language.
            if self.get_vanilla_string(TextId.CHARACTER_NAME_R2_D2) != EXPECTED_CHARACTER_NAME_R2_D2:
                raise RuntimeError("Failed to access the localized text array. If you have mods installed for Lego Star"
                                   " Wars: The Complete Saga, please try uninstalling the mods and try again.")
            if self.get_vanilla_string(TextId.CHARACTER_NAME_C_3PO) != EXPECTED_CHARACTER_NAME_C_3PO:
                raise RuntimeError("Failed to access the localized text array. If you have mods installed for Lego Star"
                                   " Wars: The Complete Saga, please try uninstalling the mods and try again.")
            self._initialized = True

    def on_unhook_game_process(self):
        data = self.localized_string_data
        try:
            # Write the vanilla strings to the allocated memory first as a precaution.
            for k in data.keys():
                self._write_vanilla_string(k)
            # Restore the vanilla pointers second as a precaution.
            for v in data.values():
                self.ctx.write_uint(v.address_of_pointer_to_vanilla_string, v.pointer_to_vanilla_string, raw=True)
            # Finally free the allocated memory.
            for v in data.values():
                self.ctx.free(v.pointer_to_allocated_string)
        finally:
            self.localized_string_data = {}


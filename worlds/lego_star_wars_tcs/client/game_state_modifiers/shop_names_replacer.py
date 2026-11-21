import logging

from random import Random
from typing import NamedTuple

from BaseClasses import ItemClassification
from Utils import async_start

from . import ClientComponent
from ..common import StaticUint
from ..events import (
    subscribe_event,
    OnReceiveSlotDataEvent,
    OnLevelChangeEvent,
    OnGameWatcherTickEvent,
)
from ..client_text import ClientText, clean_string
from ..type_aliases import ApLocationId, TCSContext
from ...constants import GAME_NAME

from ...data.extras import Extra
from ...data.levels import Level
from ...data.locations import LOCATION_NAME_TO_ID
from ...data.shop import CHARACTER_SHOP_SLOTS


try:
    # Copy SA2B's fake item names for replacing traps, if it is available.
    # noinspection PyUnresolvedReferences
    from worlds.sa2b.AestheticData import totally_real_item_names as _sa2b_fake_items_dict

    # noinspection PyBroadException
    try:
        FAKE_TRAP_NAMES = {str(k): tuple(v) for k, v in _sa2b_fake_items_dict.items() if v}
    except Exception:
        FAKE_TRAP_NAMES = {}
    del _sa2b_fake_items_dict
except ImportError:
    FAKE_TRAP_NAMES = {}


SHOP_SLOT_NAME_MAX_BYTES = 64
"""64 bytes, including the null-terminator."""

P_CHARACTER_SHOP_SLOTS = StaticUint(0x880498)
P_EXTRAS_SHOP_SLOTS = StaticUint(0x8804a0)
SHOP_SLOT_SIZE_BYTES = 0x74


debug_logger = logging.getLogger("TCS Debug")


# If a game does not have any fake item names defined, then one of these could be picked as the fake item name.
VERY_FAKE_TCS_ITEM_NAMES = (
    "Not the droids you're looking for",
    "100 Minikits (real)",
    # Fake characters.
    "Anakin Skywalker (Jedi Master)",
    "Qui-Gon Jinn (Episode III)",
    "Clone (Episode I)",
    "Luke Skywalker (Episode III)",
    "Matt the Radar Technician",
)


# todo: TCS doesn't actually have any traps currently, so these won't be used.
# Some of these names could be real names in other Star Wars games, so the client won't use them if the other game
# doesn't have any fake item names defined.
FAKE_TRAP_NAMES[GAME_NAME] = VERY_FAKE_TCS_ITEM_NAMES + (
    # Fake characters.
    "Battle Droid (Sergeant)",
    "Clone (Episode III, Commander)",
    "Rebel Guard",
    "Rebel Spy",
    "Bothan Spy",
    "Bath Trooper",
    "Luke Skywalker (Yavin)",
    "Zuckuss",
    "TIE Defender",
    "B-Wing",
    "V-Wing",
    "IG-86",
    "Darth Plagueis",
    # "Royal Trooper",
    # Characters that go by a different name in-game.
    "Destroyer Droid",
    "Boba Fett (Child)",
    "Darth Sidious",
    "Obi-Wan Kenobi (Ghost)",
    "Darth Vader (Ghost)",
)


ShopSlotNumber = int
LocalizationId = int


CHARACTER_SLOTS_MAPPING: dict[ShopSlotNumber, ApLocationId] = {
    i: LOCATION_NAME_TO_ID[character.get_purchase_location_name()]
    for i, character in enumerate(CHARACTER_SHOP_SLOTS)
}
EXTRA_LOCALIZATION_ID_MAPPING: dict[Extra, ApLocationId] = {
    extra: LOCATION_NAME_TO_ID[extra.get_purchase_location_name()]
    for extra in Extra if extra.purchase_cost is not None
}


class ShopSlotData(NamedTuple):
    item_classification: ItemClassification
    name: bytes
    player: int


class ShopNamesReplacer(ClientComponent):
    _scout_locations: set[int]
    _enabled_character_slots: dict[ShopSlotNumber, ApLocationId]
    _enabled_extra_slots: dict[Extra, ApLocationId]

    _player_names_as_bytes: dict[int, bytes]
    _cached_ctx_player_names: dict[int, str]
    _cached_character_shop_slot_item_names: dict[ShopSlotNumber, ShopSlotData]
    _cached_character_shop_slot_names: dict[ShopSlotNumber, bytes]
    _cached_extras_shop_slot_item_names: dict[Extra, ShopSlotData]
    _cached_extras_shop_slot_names: dict[Extra, bytes]

    _got_scouts: bool = False
    _calculated_player_names: bool = False
    _calculated_item_names: bool = False
    _character_shop_slot_names_replaced: bool = False
    _calculated_shop_slot_names: bool = False

    _is_in_cantina: bool = False
    _is_in_shop: bool = False

    trap_as_fake_progression_chance: int = 50

    _client_colors: ClientText

    def __init__(self):
        super().__init__()
        self._scout_locations = set()
        self._enabled_character_slots = {}
        self._enabled_extra_slots = {}
        self._player_names_as_bytes = {-1: b"Unknown"}  # 0 is reserved for Archipelago, so use -1.
        self._cached_ctx_player_names = {}
        self._cached_character_shop_slot_item_names = {}
        self._cached_character_shop_slot_names = {}
        self._cached_extras_shop_slot_item_names = {}
        self._cached_extras_shop_slot_names = {}
        self._client_colors = ClientText()

    def _set_enabled_locations(self, enabled_locations: set[int]):
        self._enabled_character_slots = {k: v for k, v in CHARACTER_SLOTS_MAPPING.items() if v in enabled_locations}
        self._enabled_extra_slots = {k: v for k, v in EXTRA_LOCALIZATION_ID_MAPPING.items() if v in enabled_locations}

    def update_player_names(self, ctx: TCSContext):
        changed = False
        for player_number, aliased_name in ctx.player_names.items():
            if aliased_name == self._cached_ctx_player_names.get(player_number):
                continue
            self._cached_ctx_player_names[player_number] = aliased_name
            changed = True
            cleaned_name = clean_string(aliased_name)
            self._player_names_as_bytes[player_number] = cleaned_name.encode("utf-8", errors="replace")
        self._calculated_player_names = True
        if changed:
            self._calculated_shop_slot_names = False
            if self._got_scouts:
                self._calculate_shop_slot_names(ctx)

    def _calculate_shop_slot_item_names(self, ctx: TCSContext):
        # Copy for safety.
        locations_info = ctx.locations_info.copy()

        # Create a deterministic Random instance by hashing the NetworkItem instances.
        # todo: This is technically deterministic because it's not hashing strings, but this is brittle and should not
        #  be relied on.
        shop_seed = hash(tuple([locations_info.get(scout_id) for scout_id in sorted(self._scout_locations)]))
        shop_random = Random(shop_seed)

        characters_shop_names: dict[ShopSlotNumber, ShopSlotData] = {}
        extras_shop_names: dict[Extra, ShopSlotData] = {}
        slots_dict: dict[ShopSlotNumber, ApLocationId] | dict[Extra, ApLocationId]
        names_dict: dict[ShopSlotNumber, ShopSlotData] | dict[Extra, ShopSlotData]
        for slots_dict, names_dict in (
                (self._enabled_character_slots, characters_shop_names),
                (self._enabled_extra_slots, extras_shop_names),
        ):
            for character_slot_or_extra, location_id in slots_dict.items():
                info = locations_info.get(location_id)
                if info is None:
                    debug_logger.error("Missing location info for location ID %i", location_id)
                    names_dict[character_slot_or_extra] = ShopSlotData(ItemClassification.filler, b"Unknown", -1)
                else:
                    classification = ItemClassification(info.flags)
                    # Fake the names for items that are purely traps, and don't have any other classification(s).
                    if (classification == ItemClassification.trap
                            and shop_random.randint(0, 99) < self.trap_as_fake_progression_chance):
                        slot_info = ctx.slot_info.get(info.player)
                        # Change the classification to Progression.
                        classification = ItemClassification.progression
                        game = slot_info.game if slot_info else "unknown"
                        if game not in FAKE_TRAP_NAMES:
                            games = list(FAKE_TRAP_NAMES)
                            random_game = shop_random.choice(games)
                            if random_game == GAME_NAME:
                                # The item won't match the game it is for, so avoid any similar sounding item names, and
                                # only use more obviously fake item names.
                                items_to_pick_from = VERY_FAKE_TCS_ITEM_NAMES
                            else:
                                items_to_pick_from = FAKE_TRAP_NAMES[random_game]
                        else:
                            items_to_pick_from = FAKE_TRAP_NAMES[game]

                        fake_item_name = shop_random.choice(items_to_pick_from)
                        cleaned_item_name = clean_string(fake_item_name)
                    else:
                        # Get the name of the item.
                        item_name = ctx.item_names.lookup_in_slot(info.item, info.player)
                        cleaned_item_name = clean_string(item_name)
                    names_dict[character_slot_or_extra] = ShopSlotData(
                        classification, cleaned_item_name.encode("utf-8", errors="replace"), info.player)
        self._cached_character_shop_slot_item_names = characters_shop_names
        self._cached_extras_shop_slot_item_names = extras_shop_names
        self._calculated_item_names = True

    def _calculate_shop_slot_names(self, ctx: TCSContext):
        """Calculate the custom shop slot names by combining the item name and player name."""
        if not self._calculated_item_names:
            self._calculate_shop_slot_item_names(ctx)
        if not self._calculated_player_names:
            debug_logger.error("Player names are not calculated in _calculate_shop_slot_names")
            return

        player_name_parentheses_count = len(b"()")
        spaces_between_item_and_player = len(b" ")
        characters_for_item_color = len("~0~~".encode("utf-8"))  # example colour code.
        null_terminator_count = len(b"\x00")
        max_custom_bytes = (
                SHOP_SLOT_NAME_MAX_BYTES
                - player_name_parentheses_count
                - spaces_between_item_and_player
                - characters_for_item_color
                - null_terminator_count
        )
        input_dict: dict[ShopSlotNumber, ShopSlotData] | dict[Extra, ShopSlotData]
        output_dict: dict[ShopSlotNumber, bytes] | dict[Extra, bytes]
        for output_dict, input_dict in (
                (self._cached_character_shop_slot_names, self._cached_character_shop_slot_item_names),
                (self._cached_extras_shop_slot_names, self._cached_extras_shop_slot_item_names),
        ):
            for slot_or_localization_id, data in input_dict.items():
                player_name = self._player_names_as_bytes.get(data.player)
                if player_name is None:
                    player_name = b"Unknown player " + f"{data.player}".encode()
                player_name_length = len(player_name)

                item_name = data.name
                item_name_length = len(item_name)

                if (player_name_length + item_name_length) > max_custom_bytes:
                    character_count_to_drop = (player_name_length + item_name_length) - max_custom_bytes
                    dropped_count = 0
                    # todo: This can be more efficient because we know the minimum bytes per character is 1, so more
                    #  can be chopped off at the start, which would avoid performance issues with very long item
                    #  names.
                    # Convert back to strings so there isn't a need to constantly decode and then encode again just to
                    # remove a character from the end.
                    item_name_str = item_name.decode("utf-8")
                    player_name_str = player_name.decode("utf-8")
                    while dropped_count < character_count_to_drop:
                        if item_name_length > player_name_length:
                            assert item_name_length > 0
                            # Chop the last character off the item name.
                            item_name_str = item_name_str[:-1]
                            item_name = item_name_str.encode("utf-8")
                            dropped_count += item_name_length - len(item_name)
                            item_name_length = len(item_name)
                        else:
                            assert player_name_length > 0
                            # Chop the last character off the player name.
                            player_name_str = player_name_str[:-1]
                            player_name = player_name_str.encode("utf-8")
                            dropped_count += player_name_length - len(player_name)
                            player_name_length = len(player_name)
                full_shop_slot_name = (
                    self._client_colors.from_classification(data.item_classification, item_name)
                    + b" ("
                    + player_name
                    + b")\x00"
                )
                output_dict[slot_or_localization_id] = full_shop_slot_name
        self._calculated_shop_slot_names = True

    def update_character_shop_slot_names(self, ctx: TCSContext):
        """Update the Shop with the already calculated custom shop slot names."""
        if not self._calculated_shop_slot_names:
            debug_logger.warning("Tried to update shop slot names without ")
            raise RuntimeError("...")

        shop_slots_start = P_CHARACTER_SHOP_SLOTS.get(ctx)
        if shop_slots_start == 0:
            # Null pointer...
            return
        for slot_index, new_name in self._cached_character_shop_slot_names.items():
            ctx.write_bytes(shop_slots_start + slot_index * SHOP_SLOT_SIZE_BYTES, new_name, len(new_name), raw=True)
        self._character_shop_slot_names_replaced = True

    @subscribe_event
    def init_from_slot_data(self, event: OnReceiveSlotDataEvent):
        self.trap_as_fake_progression_chance = event.slot_data.shop_fake_trap_chance.value
        self._set_enabled_locations(event.context.server_locations)
        self._scout_locations = set().union(self._enabled_character_slots.values(), self._enabled_extra_slots.values())
        if not self._scout_locations:
            self._got_scouts = True
            self._calculated_shop_slot_names = True
            self._character_shop_slot_names_replaced = True
        else:
            self._got_scouts = False
            self._calculated_shop_slot_names = False
            self._character_shop_slot_names_replaced = False
            # Fire and forget.
            async_start(event.context.send_msgs([{"cmd": "LocationScouts", "locations": list(self._scout_locations)}]))
        self.update_player_names(event.context)
        self._client_colors = ClientText.from_slot_data(event.slot_data)

    def _are_scouts_received(self, ctx: TCSContext) -> bool:
        scouted_location_ids = set(ctx.locations_info.keys())
        return (
                set(self._enabled_character_slots.values()) <= scouted_location_ids
                and set(self._enabled_extra_slots.values()) <= scouted_location_ids
        )

    def _replace_extras_names_with_shop_checks(self, ctx: TCSContext):
        # Replace Extras names with what they unlock.
        text_replacer = ctx.text_replacer
        power_brick_checker = ctx.true_jedi_and_power_brick_and_minikit_brick_checker
        unfound_power_bricks_by_area = power_brick_checker.remaining_power_bricks_by_area
        for extra, name in self._cached_extras_shop_slot_names.items():
            area = extra.get_area()
            if area in unfound_power_bricks_by_area:
                # The shop slot for this Extra is not unlocked yet, so skip replacing the name of the Extra in the
                # shop. The shop says "Locked" for locked Extra purchases, but other parts of the game also display
                # the names of the Extras, so only changing the names of the unlocked slots means that information
                # about the locked slots cannot be leaked.
                continue
            text_replacer.write_raw_custom_string(extra.localization_id, name)

    def _restore_extras_names(self, ctx: TCSContext):
        # Restore Extras names to their defaults.
        text_replacer = ctx.text_replacer
        for extra in self._cached_extras_shop_slot_names.keys():
            text_replacer.write_raw_vanilla_string(extra.localization_id)

    @subscribe_event
    def on_tick(self, event: OnGameWatcherTickEvent):
        if not self._got_scouts:
            if event.tick_count % 10 != 0:
                # The scouts could take a bit to be received from the server, so there's no need to check super
                # frequently.
                return
            if self._are_scouts_received(event.context):
                self._got_scouts = True
                self._calculate_shop_slot_names(event.context)

        if self._got_scouts and self._is_in_cantina and self._calculated_shop_slot_names:
            if self._cached_extras_shop_slot_names:
                # Extras shop slots always show the name of the Extra itself, so the names of the Extras themselves have
                # to be changed.
                is_in_shop = event.context.is_in_shop()
                if is_in_shop != self._is_in_shop:
                    if is_in_shop:
                        self._replace_extras_names_with_shop_checks(event.context)
                    else:
                        self._restore_extras_names(event.context)
                    self._is_in_shop = is_in_shop

            # Character shop slots do not need to update with a high frequency.
            if event.tick_count % 10 == 0:
                if not self._character_shop_slot_names_replaced:
                    # The names have not been replaced, so replace them.
                    self.update_character_shop_slot_names(event.context)
                elif event.tick_count % 20 == 0:
                    # Check that the shop slots still have their names replaced.
                    # After loading into the Cantina, the game seems to reset the Shop a second time after loading it,
                    # which can reset the replaced names.
                    if self._cached_character_shop_slot_names:
                        character_shop_start = P_CHARACTER_SHOP_SLOTS.get(event.context)
                        if character_shop_start != 0:
                            index, expected_bytes = next(iter(self._cached_character_shop_slot_names.items()))
                            read_bytes = event.context.read_bytes(character_shop_start + index * SHOP_SLOT_SIZE_BYTES,
                                                                  len(expected_bytes),
                                                                  raw=True)
                            if read_bytes != expected_bytes:
                                # debug_logger.info("Character Shop names were overwritten by the game...")
                                self._character_shop_slot_names_replaced = False

    @subscribe_event
    def on_level_change(self, event: OnLevelChangeEvent):
        self._is_in_cantina = event.new_level_id == Level.MAP
        self._is_in_shop = False
        self._character_shop_slot_names_replaced = False

    def reset_persisted_client_data(self, ctx: TCSContext):
        # Restore Extras names to their defaults.
        # This is just some extra cleanup in-case the user disconnects
        text_replacer = ctx.text_replacer
        for extra in self._cached_extras_shop_slot_names.keys():
            text_replacer.write_raw_vanilla_string(extra.localization_id)


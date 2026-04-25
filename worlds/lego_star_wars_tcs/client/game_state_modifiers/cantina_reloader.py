import asyncio
import logging
import random  # For picking a random unlocked character to force the player into if they spawned as a locked character.

from . import ClientComponent
from ..common_addresses import GameState1, OPENED_MENU_DEPTH_ADDRESS
from ..events import (
    subscribe_event,
    OnPlayerCharacterIdChangeEvent,
    OnLevelChangeEvent,
    OnReceiveSlotDataEvent,
    OnGameWatcherTickEvent
)
from ...items import CHARACTERS_AND_VEHICLES_BY_NAME, AP_NON_VEHICLE_CHARACTER_INDICES


debug_logger = logging.getLogger("TCS Debug")


# These character IDs/indices update when swapping characters in the Cantina, and the game reads these values to
# determine what characters P1 and P2 should spawn into the Cantina as.
# By changing these values and then forcing a hard (reset) load into the Cantina, the client can change the player's
# characters to whatever the client needs.
P1_CANTINA_FREE_PLAY_SELECTION_CHARACTER_ID = 0x802bd8
P2_CANTINA_FREE_PLAY_SELECTION_CHARACTER_ID = 0x802bdc


LEVEL_ID_CANTINA = 325


ADDITIONAL_OK_IDS = {
    # Womp Rat is the backup character the client forces when the player does not have at least 2 unlocked non-vehicle
    # characters.
    CHARACTERS_AND_VEHICLES_BY_NAME["Womp Rat"].character_index,

    # This is the vehicle found in the outside area of the Cantina.
    # The client could probably check some flag of the character in memory to see if it is a ridable
    # vehicle, but the Cantina only contains this one vehicle, so checking for it individually is simpler.
    CHARACTERS_AND_VEHICLES_BY_NAME["mapcar"].character_index,
}


class CantinaReloader(ClientComponent):
    active: bool = False
    needs_reload_p1: bool = False
    needs_reload_p2: bool = False
    last_p1_character_id: int | None = None
    last_p2_character_id: int | None = None
    _waiting_for_reload: bool = False

    @subscribe_event
    def on_receive_slot_data(self, event: OnReceiveSlotDataEvent):
        # Initialise active state based on the current level ID.
        self.active = event.context.current_level_id == LEVEL_ID_CANTINA

        # todo: Is it necessary to check the current character IDs here?:
        # if self.active:
        #     # Check current character ids for whether the Cantina needs to be reloaded with different characters.
        #     pass

    @subscribe_event
    def on_level_change(self, event: OnLevelChangeEvent):
        self.active = event.new_level_id == LEVEL_ID_CANTINA

    @subscribe_event
    def on_player_character_id_change(self, event: OnPlayerCharacterIdChangeEvent):
        if not self.active:
            # Not in the Cantina, so ignore needing to reload.
            return

        ctx = event.context
        unlocked_characters = ctx.acquired_characters.unlocked_characters
        if not unlocked_characters:
            # If connected, there should always be at least 1 character unlocked, even if it is a vehicle character.
            return

        p1_id = event.new_p1_character_id
        self.last_p1_character_id = p1_id
        if p1_id is not None and p1_id not in unlocked_characters and p1_id not in ADDITIONAL_OK_IDS:
            debug_logger.info(f"Cantina needs to reload because P1's character ID is {p1_id}, which is not an unlocked"
                              f" character ID.")
            self.needs_reload_p1 = True
        else:
            self.needs_reload_p1 = False

        p2_id = event.new_p2_character_id
        self.last_p2_character_id = p2_id
        if p2_id is not None and p2_id not in unlocked_characters and p2_id not in ADDITIONAL_OK_IDS:
            debug_logger.info(f"Cantina needs to reload because P2's character ID is {p2_id}, which is not an unlocked"
                              f" character ID.")
            self.needs_reload_p2 = True
        else:
            self.needs_reload_p2 = False

    @subscribe_event
    async def on_tick(self, event: OnGameWatcherTickEvent):
        if not (self.needs_reload_p1 or self.needs_reload_p2):
            # Reload not required.
            return
        if not self.active:
            # Not in the Cantina, so ignore needing to reload
            return

        ctx = event.context

        # It is assumed the player is in-game.
        # if not ctx.is_in_game():
        #     return
        if not GameState1.PLAYING_OR_TRAILER_OR_CANTINA_LOAD_OR_CHAPTER_TITLE_CRAWL.is_set(ctx):
            return
        if ctx.read_uchar(OPENED_MENU_DEPTH_ADDRESS) != 0:
            # Reloading while a menu is open can cause issues like the menu being stuck on-screen after the reload.
            # This notably happens with the shop.
            return
        if self._waiting_for_reload:
            if ctx.reload_cantina(hard=True):
                # Wait for the reload to happen.
                await asyncio.sleep(1.0)
                self._waiting_for_reload = False
            return

        needed_replacements = self.needs_reload_p1 + self.needs_reload_p2

        unlocked_characters = ctx.acquired_characters.unlocked_characters
        replacements = self._get_valid_replacement_characters(unlocked_characters, needed_replacements)

        # Change the characters that P1 and P2 will spawn as when they reload into the Cantina.
        if self.needs_reload_p1:
            ctx.write_uint(P1_CANTINA_FREE_PLAY_SELECTION_CHARACTER_ID, replacements.pop(0))
        if self.needs_reload_p2:
            ctx.write_uint(P2_CANTINA_FREE_PLAY_SELECTION_CHARACTER_ID, replacements.pop(0))

        if ctx.reload_cantina(hard=True):
            # Wait for the reload to happen.
            await asyncio.sleep(1.0)
        else:
            # If the reload failed (e.g. the player is in the shop or the game is paused), try again.
            self._waiting_for_reload = True

    def _get_valid_replacement_characters(self, unlocked_characters: set[int], needed_count: int) -> list[int]:
        """
        Get 2 valid replacement characters, or a single 'Glup' replacement character if there are no valid replacement
        characters.
        """
        # Prioritise good characters.
        replacements = []
        needed_remaining = needed_count

        # Pick from unlocked characters, except Custom Characters, who are not allowed in the Cantina because that is
        # where they are edited.
        not_allowed = {
            CHARACTERS_AND_VEHICLES_BY_NAME["STRANGER 1"].character_index,
            CHARACTERS_AND_VEHICLES_BY_NAME["STRANGER 2"].character_index,
            # If either player is a valid character, do not allow setting both players as the same character.
            # If both players are the same character, then player 2 can pick a locked character when entering a chapter.
            self.last_p1_character_id,
            self.last_p2_character_id,
        }
        allowed_character_indices = unlocked_characters - not_allowed
        allowed_character_indices.intersection_update(AP_NON_VEHICLE_CHARACTER_INDICES)

        to_pick_from = sorted(allowed_character_indices)
        picks = random.sample(to_pick_from, min(needed_remaining, len(to_pick_from)))
        replacements.extend(picks)
        needed_remaining -= len(picks)

        if needed_remaining == 0:
            return replacements
        else:
            # Fill remaining spots with the "Womp Rat" "Extra Toggle" character.
            replacements.extend([CHARACTERS_AND_VEHICLES_BY_NAME["Womp Rat"].character_index] * needed_remaining)
            return replacements

import asyncio
import logging
from typing import Callable, Coroutine

from ...common_addresses import StaticBOOL
from ...type_aliases import TCSContext
from .free_play_character_categories import set_custom_character_categories
from .add_flags_to_characters import (
    set_ig88_and_4lom_as_protocol_droids,
    set_astromech_panel_users_as_tightrope_walk,
    set_droideka_as_tightrope_tilt,
    set_can_zap_characters_as_got_batarang,
    set_yodas_as_wall_jump,
)


logger = logging.getLogger("Client")


PERM_DATA_LOADED_ADDR = StaticBOOL(0x007fce84)

# This is the last flag in the last CHARCATEGORY in _LSW_CharCategory. The last element is intentionally empty to
# signify the end of the array, but the game appears to only check the name pointer in this last element, so the two
# flags are free game for storing whether game patches have been applied.
PATCHES_APPLIED_ADDR = StaticBOOL(0x7f2664)


MemoryPatch = Callable[[TCSContext], Coroutine[None, None, None]]
PATCHES: list[MemoryPatch] = [
    set_custom_character_categories,
    set_ig88_and_4lom_as_protocol_droids,
    set_astromech_panel_users_as_tightrope_walk,
    set_droideka_as_tightrope_tilt,
    set_can_zap_characters_as_got_batarang,
    set_yodas_as_wall_jump,
]


async def apply_game_patches(ctx: TCSContext):
    if not PATCHES_APPLIED_ADDR.get(ctx):
        while not PERM_DATA_LOADED_ADDR.get(ctx):
            logger.info("Waiting for game to fully load before trying to patch. Retrying in 1.0s.")
            await asyncio.sleep(1.0)
        for patch in PATCHES:
            await patch(ctx)
        PATCHES_APPLIED_ADDR.set(ctx, True)
        logger.info("Applied AP patches")
    else:
        logger.info("AP patches have already been applied this session")

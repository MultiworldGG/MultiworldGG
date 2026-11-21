import logging
from typing import Callable, Coroutine

from ...common_addresses import StaticBOOL
from ...type_aliases import TCSContext
from .free_play_character_categories import set_custom_character_categories, p_CHARCATEGORYCOUNT
from .add_flags_to_characters import (
    set_ig88_and_4lom_as_protocol_droids,
    set_astromech_panel_users_as_tightrope_walk,
    set_droideka_as_tightrope_tilt,
    set_can_remove_droideka_shields_characters_as_got_batarang,
    set_yodas_as_super_strength,
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
    set_can_remove_droideka_shields_characters_as_got_batarang,
    set_yodas_as_super_strength,
]


def perm_data_loaded(ctx: TCSContext) -> bool:
    # PERM_DATA_LOADED_ADDR starts as `TRUE`, gets set to `FALSE` once perm data loading begins, and then gets set back
    # to `TRUE` once perm data loading is complete.
    # CHARCATEGORYCOUNT starts as `0` and gets set to non-zero (should be 9) during perm data loading.
    # Using both of these global values, it is possible to determine when perm data has been loaded.
    # Because the client overwrites CHARCATEGORYCOUNT, checking against `== 9` instead of `!= 0` won't work.
    return PERM_DATA_LOADED_ADDR.get(ctx) and p_CHARCATEGORYCOUNT.get(ctx) != 0


async def apply_game_patches(ctx: TCSContext) -> bool:
    if not PATCHES_APPLIED_ADDR.get(ctx):
        if not perm_data_loaded(ctx):
            return False
        for patch in PATCHES:
            await patch(ctx)
        PATCHES_APPLIED_ADDR.set(ctx, True)
        logger.info("Applied AP patches")
    else:
        logger.info("AP patches have already been applied this session")
    return True

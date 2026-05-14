from bisect import bisect_right
from enum import IntEnum, IntFlag
from functools import cache

from .common import StaticUChar, StaticFloat, StaticUint, StaticBOOL, FloatField, UCharField
from .type_aliases import TCSContext
from ..levels import AREA_ID_TO_CHAPTER_AREA

# To use: Iterate to find the first key that the address-to-convert is less than, then add the offset value.
_GOG_TO_STEAM = {
    # Fully aligned all the way back to 0x00400000.
    0x006f1505: 0x0,
    0x006f47b0: -0x14,
    0x006f4f64: -0x10,
    0x006f5d56: -0x13,
    0x006f5d60: -0x19,
    0x006f5eb3: -0x18,
    # There are a bunch of other minor changes between these two addresses, all within `__write_nolock`.
    # For example:
    # - 0x006f64b2: -0x70,  # GOG uses AND (3 bytes), Steam uses MOV (2 bytes)
    # - 0x006f64ba: -0x71,  # GOG has some extra instructions
    0x006f65c0: -0x74,
    # The function starting at 0x007139af (__isindst_nolock apparently) has a couple of different instructions in GOG.
    0x007139d3: -0x80,
    # Instructions in a function or two differ before here, so alignment gets complete thrown off
    0x00713b15: -0x82,
    0x00714ca0: -0xa8,
    # There is some empty space that varies in length between Steam and GOG, and then the same functions are found, but
    # offset.
    0x00751000: -0xb0,
    # Prior to 0x00751450, data does not match completely, but matches overall, back to 0x00751000.
    0x0075e9e0: +0x0,
    0x0075ece0: +0x8,
    0x0075ed00: +0xC,
    0x007615e4: +0x10,
    0x007615e8: +0x14,
    0x0076a914: +0x18,
    0x0076aa20: +0x1c,
    # This offset occurs because the previous string in memory is the path to
    # [parent dir]/gameapi.saga/edtools/fileselect.c, where [parent dir] is different between when the GOG and Steam
    # versions were compiled.
    0x76af90: +0x20,
    0x76b038: +0x24,
    0x777cd0: +0x28,
    # GOG and Steam addresses sync up at 0x7ef000, a pointer to the "bad allocation" string. There is a variable amount
    # of empty space before this.
    0x007ef000: +0x30,
    0x00829c40: 0x0,
    0x00829d70: -0x8,
    0x00854724: -0x10,
    0x029ab000: -0x20,
    0xFFFFFFFF: 0,
}
_GOG_TO_STEAM_KEYS = tuple(_GOG_TO_STEAM.keys())
assert sorted(_GOG_TO_STEAM_KEYS) == list(_GOG_TO_STEAM_KEYS)

_STEAM_TO_GOG = {
    # Fully aligned all the way back to 0x00400000.
    0x006f14f1: 0x0,
    0x006f47a0: +0x14,
    0x006f4f51: +0x10,
    0x006f5d3d: +0x13,
    0x006f5d48: +0x19,
    0x006f5e9b: +0x18,
    0x006f6441: +0x70,
    0x006f6446: +0x71,
    0x006f6540: +0x74,
    0x00713951: +0x80,
    0x00713a6d: +0x82,
    0x00714bf0: +0xa8,
    0x00751000: +0xb0,
    # Prior to 0x00751450, data does not match completely, but matches overall, back to 0x00751000.
    0x0075e9e8: -0x0,
    0x0075ecec: -0x8,
    0x0075ed10: -0xc,
    0x007615f8: -0x10,
    0x007615ff: -0x14,
    0x0076a930: -0x18,
    0x0076aa40: -0x1c,
    0x0076afb4: -0x20,
    0x0076b060: -0x24,
    0x00777d00: -0x28,
    0x007ef000: -0x30,
    0x00829c38: +0x0,
    0x00829d60: +0x8,
    0x00854704: +0x10,
    0x029ab000: +0x20,
    0xFFFFFFFF: +0x0,
}
_STEAM_TO_GOG_KEYS = tuple(_STEAM_TO_GOG.keys())
assert sorted(_STEAM_TO_GOG_KEYS) == list(_STEAM_TO_GOG_KEYS)


@cache
def gog_to_steam(address: int):
    # On an exact match, we want the next value because the keys in the dicts are for addresses *less than* a key
    # address.
    index = bisect_right(_GOG_TO_STEAM_KEYS, address)
    if index < len(_GOG_TO_STEAM_KEYS):
        return address + _GOG_TO_STEAM[_GOG_TO_STEAM_KEYS[index]]
    else:
        raise Exception(f"Address {address} is too high for GOG -> Steam conversion.")


@cache
def steam_to_gog(address: int):
    index = bisect_right(_STEAM_TO_GOG_KEYS, address)
    if index < len(_STEAM_TO_GOG_KEYS):
        return address + _STEAM_TO_GOG[_STEAM_TO_GOG_KEYS[index]]
    else:
        raise Exception(f"Address {address} is too high for Steam -> GOG conversion.")


# There are two pointers here, which are NULL when the player is dropped out.
# The full array of all 8 'player' character pointers, that can be tagged, is found at 0x93d7f0
HUMAN_CONTROLLED_PLAYER_CHARACTER_POINTERS = 0x93d830


class CharacterFlags1(IntFlag):
    PLAYER_CONTROLLED = 0x80

    @classmethod
    def get(cls, ctx: TCSContext, character_address: int):
        return cls(ctx.read_uchar(character_address + 0x1fc, raw=True))


def player_character_entity_iter(ctx: TCSContext):
    for i in range(0, 2):
        character_address = ctx.read_uint(HUMAN_CONTROLLED_PLAYER_CHARACTER_POINTERS + i * 4)
        if character_address != 0:
            yield i + 1, character_address


# CharacterEntity to index: ((int)char_ent - (int)character_entities_0093d524) / 0x10d8 & 0xffff;


CHARACTER_POWER_UP_TIMER = FloatField(0xdec)


# It looks like AREA IDs tend to use 4 bytes, even though they only need 1 byte.
# This first address seems to be part of a larger struct in memory and is not referenced, by address, directly.
CURRENT_AREA_ADDRESS = StaticUChar(0x7fd2c1)
# This second address is referenced directly, so could be a better choice.
# CURRENT_AREA_ADDRESS = StaticUChar(0x803784)

# Technically, this is direct access of the WORLDINFO struct at 0x93d858, accessing field offset 0x12c.
CURRENT_P_AREA_DATA_ADDRESS = StaticUint(0x93d9a4)
# ID field of P_AREA_DATA.
AREA_DATA_ID = UCharField(0x7c)


CHARACTERS_SHOP_START = 0x86e4c8  # See CHARACTER_SHOP_SLOTS in items.py for the mapping
EXTRAS_SHOP_START = 0x86e4d8

# 0 when a menu is not open, 1 when a menu is open (pause screen, shop, custom character creator, select mode after
# entering a level door). Increases to 2 when opening a submenu in the pause screen.
OPENED_MENU_DEPTH_ADDRESS = 0x800944


# Byte
# 255: Cutscene
# 1: Playing, Indy trailer, loading into Cantina, Title crawl
# 2: In-level 'cutscene' where non-playable characters play an animation and the player has no control
# 6: Bounty Hunter missions select
# 7: In custom character creator
# 8: In Cantina shop
# 9: Minikits display on outside scrapyard
# There is another address at 0x925395
GAME_STATE_ADDRESS = 0x9253b4


# This is GameState1 because other address have been found that can be used to infer game state, so it is likely that
# there will be a GameState2 in the future.
class GameState1(IntEnum):
    CUTSCENE = 255
    PLAYING_OR_TRAILER_OR_CANTINA_LOAD_OR_CHAPTER_TITLE_CRAWL = 1
    IN_LEVEL_SOFT_CUTSCENE = 2
    UNKNOWN_3 = 3
    UNKNOWN_4 = 4
    UNKNOWN_5 = 5
    IN_BOUNTY_HUNTER_MISSION_SELECT = 6
    IN_CUSTOM_CHARACTER_CREATOR = 7
    IN_CANTINA_SHOP = 8
    IN_JUNKYARD_MINIKITS_DISPLAY = 9

    def is_set(self, ctx: TCSContext) -> bool:
        return ctx.read_uchar(GAME_STATE_ADDRESS) == self.value

    @classmethod
    def is_playing(cls, ctx: TCSContext) -> bool:
        state = ctx.read_uchar(GAME_STATE_ADDRESS)
        return (state == cls.PLAYING_OR_TRAILER_OR_CANTINA_LOAD_OR_CHAPTER_TITLE_CRAWL.value
                or state == cls.IN_LEVEL_SOFT_CUTSCENE.value)


# When enabled, character swapping is enabled, e.g. Free Play/Challenge/Minikit Bonus/Character Bonus/LEGO City/
# New Town.
# This can be forcefully enabled in Story, and potentially other modes, to allow character swapping, though may disable
# some Story-only events that usually get disabled in Free Play, e.g. TC-14 won't spawn if this is enabled before
# Negotiations_A loads.
IS_CHARACTER_SWAPPING_ENABLED = StaticBOOL(0x93b2c4)

# See ChapterDoorGameMode below.
CHAPTER_DOOR_GAME_MODE = StaticUint(0x87953c)


class ChapterDoorGameMode(IntEnum):
    """
    The current game mode when in a chapter door. Note: Entering non-chapter levels does not clear this value.

    The value sticks around while inside a chapter itself, so can be used as an imperfect way to detect what mode the
    player is currently in. Notably, this can give false positives for Bounty Hunter Missions and Superstory.

    Adjusting this value changes the currently selected option in the chapter door's menu.
    """
    STORY = 0
    FREE_PLAY = 1
    CHALLENGE = 2

    def is_set(self, ctx: TCSContext) -> bool:
        return CHAPTER_DOOR_GAME_MODE.get(ctx) == self.value

    def set(self, ctx: TCSContext):
        CHAPTER_DOOR_GAME_MODE.set(ctx, self.value)

    # @classmethod
    # def get(cls, ctx: TCSContext) -> "ChapterDoorGameMode | None":
    #     v = CHAPTER_DOOR_GAME_MODE.get(ctx)
    #     if v in ChapterDoorGameMode:
    #         return cls(v)
    #     else:
    #         return None


CHALLENGE_MODE_ADDRESS = StaticUint(0x856c28)


class ChallengeMode(IntEnum):
    NO_CHALLENGE = 0x0
    CHALLENGE_IN_PROGRESS = 0x1
    CHALLENGE_STOPPED = 0x2
    CHALLENGE_FAILED = 0x3

    def is_set(self, ctx: TCSContext) -> bool:
        return CHALLENGE_MODE_ADDRESS.get(ctx) == self.value


def is_in_chapter_free_play(ctx: TCSContext, area_id: int | None = None) -> bool:
    # The current area ID is often known in advance.
    if area_id is None:
        area_id = CURRENT_AREA_ADDRESS.get(ctx)

    if area_id not in AREA_ID_TO_CHAPTER_AREA:
        # This eliminates Bonuses that have Free Play.
        return False

    if not IS_CHARACTER_SWAPPING_ENABLED.get(ctx):
        # This eliminates Bounty Hunter Missions because they do not allow character swapping (only tagging).
        # This eliminates Superstory because it does not allow character swapping (only tagging).
        return False

    if not ChapterDoorGameMode.FREE_PLAY.is_set(ctx):
        # This eliminates chapters in Challenge mode.
        return False

    return True


class ShopType(IntEnum):
    NONE = 255  # -1 as a `signed char`
    HINTS = 0
    CHARACTERS = 1
    EXTRAS = 2
    ENTER_CODE = 3
    GOLD_BRICKS = 4
    STORY_CLIPS = 5


class CantinaRoom(IntEnum):
    UNKNOWN = -2
    NOT_IN_CANTINA = -1
    SHOP_ROOM = 0
    EPISODE_1 = 1
    EPISODE_2 = 2
    EPISODE_3 = 3
    EPISODE_4 = 4
    EPISODE_5 = 5
    EPISODE_6 = 6
    JUNKYARD = 7
    BONUSES = 8
    BOUNTY_HUNTER_MISSIONS = 9


_CUSTOM_SAVE_FLAGS_1_ADDRESS = 0x86e506


class CustomSaveFlags1(IntFlag):
    """
    There are two unused bytes in the save data after the byte that stores whether the Indiana Jones trailer has been
    watched.
    BYTE1_AFTER_INDIANA_JONES_TRAILER = 0x86e506
    BYTE2_AFTER_INDIANA_JONES_TRAILER = 0x86e507

    The client uses these two bytes for storing up to 16 flags.
    """
    MINIKIT_GOAL_COMPLETE = 0x1
    DEATH_LINK_ENABLED = 0x2
    AUTO_COLLECT_PICKUPS_ENABLED = 0x4
    AUTO_COLLECT_PICKUPS_VEHICLES_ONLY = 0x8
    FIELD_5 = 0x10  # Could be DEFEAT_BOSSES_GOAL_COMPLETE to reduce memory reading once the goal is complete.
    FIELD_6 = 0x20
    FIELD_7 = 0x40
    FIELD_8 = 0x80
    FIELD_9 = 0x100
    FIELD_10 = 0x200
    FIELD_11 = 0x400
    FIELD_12 = 0x800
    FIELD_13 = 0x1000
    FIELD_14 = 0x2000
    FIELD_15 = 0x4000
    FIELD_16 = 0x8000

    def is_set(self, ctx: TCSContext) -> bool:
        # noinspection PyTypeChecker
        v: int = self.value
        if v <= 0xFF:
            addr = _CUSTOM_SAVE_FLAGS_1_ADDRESS
        else:
            v = v >> 8
            addr = _CUSTOM_SAVE_FLAGS_1_ADDRESS + 1

        return (ctx.read_uchar(addr) & v) != 0

    def set(self, ctx: TCSContext):
        # noinspection PyTypeChecker
        v: int = self.value
        if v <= 0xFF:
            addr = _CUSTOM_SAVE_FLAGS_1_ADDRESS
        else:
            v = v >> 8
            addr = _CUSTOM_SAVE_FLAGS_1_ADDRESS + 1

        b = ctx.read_uchar(addr)
        if not (b & v):
            ctx.write_byte(_CUSTOM_SAVE_FLAGS_1_ADDRESS, b | v)

    def unset(self, ctx: TCSContext):
        # noinspection PyTypeChecker
        v: int = self.value
        if v <= 0xFF:
            addr = _CUSTOM_SAVE_FLAGS_1_ADDRESS
        else:
            v = v >> 8
            addr = _CUSTOM_SAVE_FLAGS_1_ADDRESS + 1

        b = ctx.read_uchar(addr)
        if b & v:
            ctx.write_byte(_CUSTOM_SAVE_FLAGS_1_ADDRESS, b & ~v)

    def set_bool(self, ctx: TCSContext, b: bool):
        if b:
            return self.set(ctx)
        else:
            return self.unset(ctx)

# Other potential unused sava-data bytes
# Some (most?) (all?) bonus levels have enough space reserved for all the Minikits/True Jedi/Power Brick bytes, which
# they don't use.
# The Extras shop uses 6 bytes, but appears to have 16 bytes allocated.
# The Hints shop uses 2 bytes, but appears to have 12 bytes allocated.
# The Characters shop uses 13 bytes, but appears to have 16 bytes allocated.


# -- Game state addresses.

# This value is slightly unstable and occasionally changes to 0 while playing. It is also set to 2 in Mos Espa Pod Race
# for some reason.
# Importantly, this value is *not* 0 when watching a Story cutscene, and is instead 1.
PAUSED_OR_STATUS_WHEN_0_ADDRESS = 0x9737f8
# This address is usually -1/255 while playing or paused, 1 while tabbed out and 0 while both paused and tabbed out.
# It is a more unstable than the previous value, while playing, however.
# Notably, if window focus is forced by setting 0x827610 to 1, thus allowing the game to run in the background, then
# this still correctly identifies whether the game is frozen.
TABBED_OUT_WHEN_1_ADDRESS = 0x9868e4

# 0 when playing, 1 when in a cutscene, same-level door transition, Indy trailer and title crawl.
# Rarely unstable and seen as -1 briefly while playing
IS_PLAYING_WHEN_0_ADDRESS = 0x297c0cc

# Set to > 0.0 during a screen wipe/transition. In-game hints only display when this is 0.0.
SCREEN_TRANSITION_TIMER_ADDRESS = StaticFloat(0x9507a0)


def is_actively_playing(ctx: TCSContext):
    """
    Return True if the player is actively playing the game.

    Returns False in cases like having a menu open, having the game paused, or having the game tabbed out.
    """
    return (
            # Handles pause and status screens.
            ctx.read_uchar(PAUSED_OR_STATUS_WHEN_0_ADDRESS) != 0
            # Handles tabbing out.
            and ctx.read_uchar(TABBED_OUT_WHEN_1_ADDRESS) != 1
            # Handles pause menu and other menus.
            and ctx.read_uchar(OPENED_MENU_DEPTH_ADDRESS) == 0
            # Handles same-level screen transitions.
            and ctx.read_uchar(IS_PLAYING_WHEN_0_ADDRESS) == 0
            # Handles screen/level transitions. Unlike most timer-like floats, this one actually gets set to 0.0.
            and SCREEN_TRANSITION_TIMER_ADDRESS.get(ctx) == 0.0
            and GameState1.is_playing(ctx)
    )

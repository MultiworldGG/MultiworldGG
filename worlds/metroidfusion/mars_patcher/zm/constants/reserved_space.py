from enum import IntEnum, auto

from typing_extensions import Self


class ReservedConstantsZM:
    """
    These are constants that are in the ROM's 'Reserved Space'; things that are intended to be
    modified by this patcher. Most of these are pointers at a hard-coded address that point to
    various pieces of data.
    """

    # Important addresses:
    # 0x760D38 - End of vanilla data (U region)
    # 0x7B0000 - Patcher data free space
    # 0x7D0000 - Randomizer data pointers
    # 0x7D8000 - NES Metroid data

    # Hardcoded address for the pointers listed below; see linker.ld (around line 12)
    RANDO_POINTERS_ADDR = 0x7D0000

    # Address for any additional data that the patcher may need to write
    PATCHER_FREE_SPACE_ADDR = 0x7B0000
    PATCHER_FREE_SPACE_END = RANDO_POINTERS_ADDR


class ReservedPointersZM(IntEnum):
    # These need to be kept in sync with the data pointers in the decomp, which can be found in
    # src/data/randomizer_pointers.c

    # Existing data
    ROOM_AREA_ENTRIES_PTR = 0
    """Pointer to the list of pointers to the room entries for each area."""
    TILESET_ENTRIES_PTR = auto()
    """Pointer to the list of tileset entries."""
    ANIM_TILESET_ENTRIES_PTR = auto()
    """Pointer to the list of animated tileset entries."""
    MINIMAPS_PTR = auto()
    """Pointer to a list of pointers to the minimap data for each area."""
    AREA_DOORS_PTR = auto()
    """Pointer to the list of pointers to the door entries for each area."""
    AREA_CONNECTIONS_PTR = auto()
    """Pointer to the list of area connections."""
    ANIM_PALETTE_ENTRIES_PTR = auto()
    """Pointer to the list of animated palette entries."""
    SPRITE_GRAPHICS_PTR = auto()
    """Pointer to the list of pointers to the graphics for each sprite."""
    SPRITE_PALETTES_PTR = auto()
    """Pointer to the list of pointers to the palette for each sprite."""
    GUNSHIP_FLASHING_PALETTE_PTR = auto()
    """Pointer to an extra palette used by the gunship sprite."""
    SPRITESET_PTR = auto()
    """Pointer to the list of pointers to spriteset entries."""
    SAMUS_PALETTES_PTR = auto()
    """Pointer to the start of all of Samus's palettes."""
    HELMET_CURSOR_PALETTES_PTR = auto()
    """Pointer to the palette used for the helmet cursor in menus."""
    BEAM_PALETTES_PTR = auto()
    """Pointer to the start of the beam palettes."""
    STATUES_CUTSCENE_PALETTE_PTR = auto()
    """Pointer to the palette of the boss statues near Tourian used during the cutscene."""
    MESSAGE_TEXT_PTR = auto()
    """Pointer to a table of pointers for each language that point to message text."""
    STORY_TEXT_PTR = auto()
    """Pointer to a table of pointers for each language that point to story text."""
    CHARACTER_WIDTHS_PTR = auto()
    """Pointer to the character widths table."""
    SOUND_DATA_PTR = auto()
    """Pointer to the list of sound data entries."""
    CHOZO_STATUE_TARGETS_PTR = auto()
    """Pointer to the list of Chozo statue targets."""
    CREDITS_PTR = auto()
    """Pointer to the credits text."""

    # Rando data
    INTRO_CUTSCENE_DATA_PTR = auto()
    """Pointer to the in-game cutscene data for the intro cutscene;
    needed for writing the starting area."""
    STARTING_INFO_PTR = auto()
    """Pointer to a struct containing the starting location and items."""
    MAJOR_LOCATIONS_PTR = auto()
    """Pointer to a list of major locations and the items they have."""
    MINOR_LOCATIONS_PTR = auto()
    """Pointer to a list of minor locations and the items they have."""
    TANK_INCREASE_AMOUNTS_PTR = auto()
    """Pointer to the amount of ammo each tank gives."""
    TITLE_TEXT_LINES_PTR = auto()
    """Pointer to the lines of text to display on the title screen."""
    SEED_HASH_PTR = auto()
    """Pointer to the seed hash text to display on the file select menu."""
    ROOM_NAMES_PTR = auto()
    """Pointer to a table of pointers for each area that point to room names."""

    # Rando options
    DIFFICULTY_OPTIONS_PTR = auto()
    DEFAULT_STEREO_PTR = auto()
    METROID_SPRITE_STATS_PTR = auto()
    BLACK_PIRATES_REQUIRE_PLASMA_PTR = auto()
    SKIP_DOOR_TRANSITIONS_PTR = auto()
    BALL_LAUNCHER_WITHOUT_BOMBS_PTR = auto()
    REVEAL_HIDDEN_TILES = auto()
    REMOVE_CUTSCENES_PTR = auto()
    FAST_ITEM_GRAB_PTR = auto()
    SKIP_SUITLESS_SEQUENCE_PTR = auto()

    def __new__(cls, offset: int) -> Self:
        obj = int.__new__(cls)
        obj._value_ = ReservedConstantsZM.RANDO_POINTERS_ADDR + (offset * 4)
        return obj

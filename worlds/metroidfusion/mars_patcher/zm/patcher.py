from collections.abc import Callable
from os import PathLike

from ..random_palettes import PaletteRandomizer, PaletteSettings
from ..rom import Rom
from ..room_names import write_room_names
from ..sounds import set_sounds
from ..text import write_seed_hash
from ..title_screen_text import write_title_text
from .auto_generated_types import MarsSchemaZM
from .constants.reserved_space import ReservedConstantsZM
from .credits import write_credits
from .hint_text import write_hint_text, write_intro_text
from .item_patcher import ItemPatcher, set_tank_increments
from .locations import LocationSettings
from .misc_patches import (
    apply_reveal_hidden_tiles,
    disable_music,
    disable_sound_effects,
    fast_item_grab,
    remove_cutscenes,
    skip_door_transitions,
    stereo_default,
)
from .starting import set_starting_items, set_starting_location


def patch_zm(
    rom: Rom,
    output_path: str | PathLike[str],
    patch_data: MarsSchemaZM,
    status_update: Callable[[str, float], None],
) -> None:
    """
    Creates a new randomized Zero Mission game, based off of an input path, an output path,
    a dictionary defining how the game should be randomized, and a status update function.

    Args:
        input_path: The path to an unmodified Metroid Zero Mission (U) ROM.
        output_path: The path where the randomized Zero Mission ROM should be saved to.
        patch_data: A dictionary defining how the game should be randomized.
            This function assumes that it satisfies the needed schema. To validate it, use
            validate_patch_data_zm().
        status_update: A function taking in a message (str) and a progress value (float).
    """

    # Apply base patch first
    # apply_base_patch(rom)

    # Randomize palettes - palettes are randomized first since the item
    # patcher needs to copy tilesets
    if "palettes" in patch_data:
        status_update("Randomizing palettes...", -1)
        pal_settings = PaletteSettings.from_json(patch_data["palettes"])
        pal_randomizer = PaletteRandomizer(rom, pal_settings)
        pal_randomizer.randomize()

    # Load locations and set assignments
    status_update("Writing item assignments...", -1)
    loc_settings = LocationSettings.initialize()
    loc_settings.set_assignments(patch_data["locations"])
    item_patcher = ItemPatcher(rom, loc_settings)
    item_patcher.write_items()

    # Music
    if "music_replacement" in patch_data:
        status_update("Writing music...", -1)
        set_sounds(rom, patch_data["music_replacement"])

    # Starting location
    if "starting_location" in patch_data:
        status_update("Writing starting location...", -1)
        set_starting_location(rom, patch_data["starting_location"])

    # Starting items
    if "starting_items" in patch_data:
        status_update("Writing starting items...", -1)
        set_starting_items(rom, patch_data["starting_items"])

    # Tank increments
    if "tank_increments" in patch_data:
        status_update("Writing tank increments...", -1)
        set_tank_increments(rom, patch_data["tank_increments"])

    # Elevator connections
    # conns = None
    # if "elevator_connections" in patch_data:
    #     status_update("Writing elevator connections...", -1)
    #     conns = Connections(rom)
    #     conns.set_elevator_connections(patch_data["elevator_connections"])

    # Room Names
    if room_names := patch_data.get("room_names", []):
        status_update("Writing room names...", -1)
        write_room_names(rom, room_names)

    # Intro text
    if intro_text := patch_data.get("intro_text", {}):
        status_update("Writing intro text...", -1)
        write_intro_text(rom, intro_text)

    # Hints
    if hint_text := patch_data.get("hint_text", {}):
        status_update("Writing hint text...", -1)
        write_hint_text(rom, hint_text)

    # Credits
    if credits_text := patch_data.get("credits_text", []):
        status_update("Writing credits text...", -1)
        write_credits(rom, credits_text)

    # Misc patches
    if patch_data.get("skip_door_transitions"):
        skip_door_transitions(rom)

    if patch_data.get("stereo_default", True):
        stereo_default(rom)

    if patch_data.get("disable_music"):
        disable_music(rom)

    if patch_data.get("disable_sound_effects"):
        disable_sound_effects(rom)

    if patch_data.get("remove_cutscenes"):
        remove_cutscenes(rom)

    if patch_data.get("fast_item_grab"):
        fast_item_grab(rom)

    # if patch_data.get("unexplored_map"):
    #     apply_unexplored_map(rom)

    #     if not patch_data.get("hide_doors_on_minimap", False):
    #         apply_reveal_unexplored_doors(rom)

    if patch_data.get("reveal_hidden_tiles"):
        apply_reveal_hidden_tiles(rom)

    # if "level_edits" in patch_data:
    #     apply_level_edits(rom, patch_data["level_edits"])

    # Apply base minimap edits
    # apply_base_minimap_edits(rom)

    # Apply JSON minimap edits
    # if "minimap_edits" in patch_data:
    #     apply_minimap_edits(rom, patch_data["minimap_edits"])

    # Door locks
    # if door_locks := patch_data.get("door_locks", []):
    #     status_update("Writing door locks...", -1)
    #     set_door_locks(rom, door_locks)

    write_seed_hash(rom, patch_data["seed_hash"])

    # Title screen text
    if title_screen_text := patch_data.get("title_text"):
        status_update("Writing title screen text...", -1)
        write_title_text(rom, title_screen_text)

    free_space_size = (
        ReservedConstantsZM.PATCHER_FREE_SPACE_END - ReservedConstantsZM.PATCHER_FREE_SPACE_ADDR
    )
    free_space_used = rom.free_space_addr - ReservedConstantsZM.PATCHER_FREE_SPACE_ADDR
    percent = free_space_used / free_space_size
    print(f"Free space used: {free_space_used:X}/{free_space_size:X} ({percent:.2%})")

    rom.save(output_path)
    status_update(f"Output written to {output_path}", -1)

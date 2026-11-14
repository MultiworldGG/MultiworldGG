import json
import pkgutil
from collections.abc import Callable
from os import PathLike

from ..level_edits import apply_level_edits
from .auto_generated_types import MarsSchemaMF
from .connections import Connections
from .credits import write_credits
from .data import get_relative_data_path
from .door_locks import set_door_locks
from .item_patcher import (
    ItemPatcher,
    set_required_metroid_count,
    set_tank_increments,
)
from .locations import LocationSettings
from .misc_patches import (
    apply_alternative_health_layout,
    apply_base_patch,
    apply_environmental_damage,
    apply_instant_unmorph_patch,
    apply_nerf_gerons,
    apply_reveal_hidden_tiles,
    apply_reveal_unexplored_doors,
    apply_rng_values,
    apply_toggle_for_secondary_weapon_selection,
    apply_unexplored_map,
    change_missile_limit,
    disable_demos,
    disable_music,
    disable_sound_effects,
    skip_door_transitions,
    stereo_default,
)
from .navigation_text import NavigationText
from .starting import set_starting_items, set_starting_location
from ..random_palettes import PaletteRandomizer, PaletteSettings
from ..rom import Rom
from ..room_names import write_room_names
from ..sounds import set_sounds
from ..text import write_seed_hash
from ..tilemap import apply_minimap_edits
from ..title_screen_text import write_title_text


def patch_mf(
    rom: Rom,
    output_path: str | PathLike[str],
    patch_data: MarsSchemaMF,
    status_update: Callable[[str, float], None],
) -> None:
    """
    Creates a new randomized Fusion game, based off of an input path, an output path,
    a dictionary defining how the game should be randomized, and a status update function.

    Args:
        rom: Rom object for an unmodified Metroid Fusion (U) ROM.
        output_path: The path where the randomized Fusion ROM should be saved to.
        patch_data: A dictionary defining how the game should be randomized.
            This function assumes that it satisfies the needed schema. To validate it, use
            validate_patch_data_mf().
        status_update: A function taking in a message (str) and a progress value (float).
    """

    # Apply base asm patch first
    apply_base_patch(rom)

    # Randomize palettes - palettes are randomized first in case the item
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

    # Required metroid count
    set_required_metroid_count(rom, patch_data["required_metroid_count"])

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
    conns = None
    if "elevator_connections" in patch_data:
        status_update("Writing elevator connections...", -1)
        conns = Connections(rom)
        conns.set_elevator_connections(patch_data["elevator_connections"])

    # Sector shortcuts
    if "sector_shortcuts" in patch_data:
        status_update("Writing sector shortcuts...", -1)
        if conns is None:
            conns = Connections(rom)
        conns.set_shortcut_connections(patch_data["sector_shortcuts"])

    # Hints
    if nav_text := patch_data.get("navigation_text", {}):
        status_update("Writing navigation text...", -1)
        navigation_text = NavigationText.from_json(nav_text)
        navigation_text.write(rom)

    if nav_locks := patch_data.get("nav_station_locks", {}):
        status_update("Writing navigation locks...", -1)
        NavigationText.apply_hint_security(rom, nav_locks)

    # Room Names
    if room_names := patch_data.get("room_names", []):
        status_update("Writing room names...", -1)
        write_room_names(rom, room_names)

    # Credits
    if credits_text := patch_data.get("credits_text", []):
        status_update("Writing credits text...", -1)
        write_credits(rom, credits_text)

    # Misc patches
    if patch_data.get("disable_demos"):
        disable_demos(rom)

    if patch_data.get("instant_unmorph"):
        apply_instant_unmorph_patch(rom)

    if patch_data.get("skip_door_transitions"):
        skip_door_transitions(rom)

    if patch_data.get("stereo_default", True):
        stereo_default(rom)

    if patch_data.get("disable_music"):
        disable_music(rom)

    if patch_data.get("disable_sound_effects"):
        disable_sound_effects(rom)

    if environmental_damage := patch_data.get("environmental_damage"):
        apply_environmental_damage(rom, environmental_damage)

    if "missile_limit" in patch_data:
        change_missile_limit(rom, patch_data["missile_limit"])

    if patch_data.get("nerf_gerons"):
        apply_nerf_gerons(rom)

    if patch_data.get("use_alternative_hud_health_layout"):
        apply_alternative_health_layout(rom)

    if patch_data.get("use_toggle_for_secondary_weapon_selection"):
        apply_toggle_for_secondary_weapon_selection(rom)

    if rng_dict := patch_data.get("rng"):
        apply_rng_values(rom, rng_dict)

    if patch_data.get("unexplored_map"):
        apply_unexplored_map(rom)

        if not patch_data.get("hide_doors_on_minimap", False):
            apply_reveal_unexplored_doors(rom)

    if patch_data.get("reveal_hidden_tiles"):
        apply_reveal_hidden_tiles(rom)

    if "level_edits" in patch_data:
        apply_level_edits(rom, patch_data["level_edits"])

    # Apply base minimap edits
    path = get_relative_data_path(__file__, "base_minimap_edits.json")
    edits_dict = json.loads(pkgutil.get_data(__name__, path).decode())
    apply_minimap_edits(rom, edits_dict)

    # Apply JSON minimap edits
    if "minimap_edits" in patch_data:
        apply_minimap_edits(rom, patch_data["minimap_edits"])

    # Door locks
    if door_locks := patch_data.get("door_locks", []):
        status_update("Writing door locks...", -1)
        set_door_locks(rom, door_locks)

    write_seed_hash(rom, patch_data["seed_hash"])

    # Title screen text
    if title_screen_text := patch_data.get("title_text"):
        status_update("Writing title screen text...", -1)
        write_title_text(rom, title_screen_text)

    rom.save(output_path)
    status_update(f"Output written to {output_path}", -1)

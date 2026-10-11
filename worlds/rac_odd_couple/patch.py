from __future__ import annotations

from worlds.Files import APPatchExtension, APProcedurePatch


class OddCouplePatchExtension(APPatchExtension):
    """The button-rewiring transform is a structural edit (by SWF tag/button ID),
    not a byte-offset diff, so it can be expressed as a procedure step that runs
    against whatever vanilla swf the player supplies - no reference copy needed
    on the generating machine."""
    game = "Ratchet & Clank: The Odd Couple"

    @staticmethod
    def apply_button_patch(caller: "OddCouplePatch", rom: bytes) -> bytes:
        from .swf_patch import patch_swf_bytes
        return patch_swf_bytes(rom)


class OddCouplePatch(APProcedurePatch):
    """
    Describes the button patch as a procedure rather than a binary diff, so
    generation never needs a copy of the (copyrighted) vanilla swf - only the
    player applying the patch does, via their own root_directory setting.
    """
    game: str = "Ratchet & Clank: The Odd Couple"
    patch_file_ending: str = ".apoddcouple"
    result_file_ending: str = ".swf"
    hash = None  # no single well-known release/MD5 to pin against
    procedure = [("apply_button_patch", [])]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_swf_bytes()


def get_base_swf_path() -> str:
    # Accessing a required settings.FilePath that doesn't exist automatically
    # opens a file-browse dialog and persists the chosen path to host.yaml -
    # no manual "does it exist" handling needed here.
    from .world import OddCoupleWorld
    return str(OddCoupleWorld.settings.swf_file)


def get_base_swf_bytes() -> bytes:
    base_swf_bytes = getattr(get_base_swf_bytes, "base_swf_bytes", None)
    if not base_swf_bytes:
        with open(get_base_swf_path(), "rb") as f:
            base_swf_bytes = f.read()
        get_base_swf_bytes.base_swf_bytes = base_swf_bytes
    return base_swf_bytes

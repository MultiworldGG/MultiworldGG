import os
import orjson
import shutil
import tempfile
from dataclasses import dataclass
from typing import Any, ClassVar, Dict, List, Optional
from worlds.Files import APProcedurePatch, AutoPatchExtensionRegister
from Patch import create_rom_file
from Utils import Version, tuplize_version
from settings import get_settings
from .Hints import sanitize
from .Items import item_table, APItem
from .Options import ALBWOptions, create_randomizer_settings
from albwrandomizer import ArchipelagoItem, ArchipelagoInfo, logging_on, randomize_pre_fill, set_custom_hints

class PatchItemInfo:
    name: str
    classification: int

    def __init__(self, name: str, classification: int):
        self.name = name
        self.classification = classification

class PatchInfo:
    version: str
    seed: int
    player_name: str
    options: ALBWOptions
    check_map: Dict[str, str]
    items: Dict[str, PatchItemInfo]
    hints: List[str]
    bow_of_light_hint: str

    cur_version: ClassVar[Version] = Version(0, 2, 1)
    min_compatible_version: ClassVar[Version] = Version(0, 2, 0)

    def __init__(
        self,
        version: str,
        seed: int,
        player_name: str,
        options: ALBWOptions,
        check_map: Dict[str, str],
        items: Dict[str, PatchItemInfo],
        hints: List[str],
        bow_of_light_hint: str,
    ):
        self.version = version
        self.seed = seed
        self.player_name = player_name
        self.options = options
        self.check_map = check_map
        self.items = items
        self.hints = hints
        self.bow_of_light_hint = bow_of_light_hint
    
    def to_json(self) -> str:
        return orjson.dumps({
            "version": self.version,
            "seed": self.seed,
            "player_name": self.player_name,
            "options": self.options.as_dict(*ALBWOptions.option_names()),
            "check_map": self.check_map,
            "items": {key: val.__dict__ for key, val in self.items.items()},
            "hints": self.hints,
            "bow_of_light_hint": self.bow_of_light_hint,
        })
    
def from_json(json: str) -> PatchInfo:
    info = orjson.loads(json)

    # Check patch version
    version = info["version"]
    if tuplize_version(version) > PatchInfo.cur_version:
        raise Exception(f"The patch file was generated on a newer version of the apworld. \
            Please update to version {version}.")
    elif tuplize_version(version) < PatchInfo.min_compatible_version:
        raise Exception(f"The patch file was generated on an older version of the apworld. \
            For compatibility, you must downgrade to version {version}.")

    options = {key: option.from_any(info["options"][key] if key in info["options"] else option.default)
        for key, option in ALBWOptions.type_hints.items() }

    return PatchInfo(
        info["version"],
        info["seed"],
        info["player_name"],
        ALBWOptions(**options),
        info["check_map"],
        {loc: PatchItemInfo(item["name"], item["classification"]) for loc, item in info["items"].items()},
        info["hints"],
        info["bow_of_light_hint"]
    )

class ALBWProcedurePatch(APProcedurePatch):
    game: str = "A Link Between Worlds"
    hash: Optional[str] = None
    patch_file_ending: str = ".apalbw"
    result_file_ending: str = ".zip"
    rom_file: str = ""

    procedure = [
        ("patch_albw", ["patch_info.json"])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        cls.rom_file = get_settings().albw_settings.rom_file
        logging_on()

        return b""

class ALBWPatchExtension(metaclass=AutoPatchExtensionRegister):
    game: str = "A Link Between Worlds"

    @staticmethod
    def patch_albw(caller: ALBWProcedurePatch, rom: bytes, patch_name: str) -> bytes:
        try:
            return patch_albw_inner(caller, rom, patch_name)
        except Exception as e:
            from tkinter.messagebox import showerror
            showerror(message=str(e))
            raise e

def patch_albw_inner(caller: ALBWProcedurePatch, rom: bytes, patch_name: str) -> bytes:
    GAME_ID = "00040000000EC300"

    # Load patch info from the json file
    patch_info = from_json(caller.get_file(patch_name))

    # Load Archipelago info from the patch info
    archipelago_info = ArchipelagoInfo()
    archipelago_info.name = patch_info.player_name
    archipelago_info.items = {sanitize(loc_name): ArchipelagoItem(sanitize(item.name), item.classification)
                                for loc_name, item in patch_info.items.items()}

    # Initialize seed info from the patch info
    settings = create_randomizer_settings(patch_info.options)
    seed_info = randomize_pre_fill(patch_info.seed, settings, archipelago_info)
    check_map = {loc_name: item_table[item_name].progress[0] if item_name != "AP Item" else APItem
        for loc_name, item_name in patch_info.check_map.items()}
    seed_info.build_layout(check_map)
    set_custom_hints(seed_info, patch_info.hints, patch_info.bow_of_light_hint)

    with tempfile.TemporaryDirectory() as output_directory:
        # Create the patch
        output_subdirectory = os.path.join(output_directory, f"tmp_apalbw_{caller.player}")
        os.mkdir(output_subdirectory)
        seed_info.patch(caller.rom_file, output_subdirectory)

        # Optionally install the patch
        mod_path = getattr(get_settings().albw_settings, "mod_path", "")
        if mod_path != "":
            if os.path.exists(mod_path):
                try:
                    albw_mod_path = os.path.join(mod_path, GAME_ID)
                    if os.path.exists(albw_mod_path):
                        shutil.rmtree(albw_mod_path)
                    tmp_mod_path = os.path.join(output_subdirectory, GAME_ID)
                    shutil.copytree(tmp_mod_path, albw_mod_path)
                except Exception as err:
                    print(f"Error installing mod: {err}")
            else:
                print(f"Could not install mod, path {mod_path} does not exist")

        # Put the patch in a zip file
        output_path = os.path.join(output_directory, f"tmp_apalbw_{caller.player}.zip")
        shutil.make_archive(output_subdirectory, "zip", output_subdirectory)

        # Output the contents of the zip file
        with open(output_path, "rb") as output_file:
            output = output_file.read()
        return output

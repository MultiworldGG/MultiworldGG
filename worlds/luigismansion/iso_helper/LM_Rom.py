from worlds.Files import APPatch, APPlayerContainer, AutoPatchRegister
from settings import get_settings, Settings
from NetUtils import convert_to_base_types
import Utils

from hashlib import md5
from typing import Any
import requests, ssl, certifi, urllib.request
from logging import Logger, getLogger
import json, sys, os, zipfile, tempfile, shutil

from ..client.constants import CLIENT_VERSION, RANDOMIZER_NAME, CLIENT_NAME, LM_GC_IDs

LM_USA_MD5 = 0x6e3d9ae0ed2fbd2f77fa1ca09a60c494

class InvalidCleanISOError(Exception):
    """
    Exception raised for when user has an issue with their provided Luigi's Mansion ISO.

    Attributes:
        message -- Explanation of the error
    """

    def __init__(self, message="Invalid Clean ISO provided"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidCleanISOError: {self.message}"

class LMPlayerContainer(APPlayerContainer):
    game = RANDOMIZER_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".aplm"

    def __init__(self, player_choices: dict, patch_path: str, player_name: str, player: int,
        server: str = ""):
        self.output_data = player_choices
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.aplm", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)

class LMUSAAPPatch(APPatch, metaclass=AutoPatchRegister):
    game = RANDOMIZER_NAME
    hash = LM_USA_MD5
    patch_file_ending = ".aplm"
    result_file_ending = ".iso"
    _client_logger: Logger = None

    procedure = ["custom"]

    def __init__(self, *args: Any, **kwargs: Any):
        super(LMUSAAPPatch, self).__init__(*args, **kwargs)
        self._client_logger = getLogger(CLIENT_NAME)

    def _get_archive_name(self) -> str:
        if not (Utils.is_linux or Utils.is_windows):
            message = f"Your OS is not supported with this randomizer {sys.platform}."
            self._client_logger.error(message)
            raise RuntimeError(message)

        lib_path = ""
        if Utils.is_windows:
            lib_path = "lib-windows"
        elif Utils.is_linux:
            lib_path = "lib-linux"

        self._client_logger.info(f"Dependency archive name to use: {lib_path}")
        return lib_path

    def patch(self, aplm_patch: str) -> str:
        # Get the AP Path for the base ROM
        lm_clean_iso = get_base_rom_path()
        self._client_logger.info(f"Provided {RANDOMIZER_NAME} ISO Path was: " + lm_clean_iso)

        base_path = os.path.splitext(aplm_patch)[0]
        output_file = base_path + self.result_file_ending

        try:
            self.create_iso(aplm_patch, output_file, lm_clean_iso, True)
        except ImportError as ex:
            self._client_logger.warning("Error while trying to import third party dependencies. Details: " + str(ex))
            self._client_logger.info("Speedups not detected, attempting to pull remote release.")
            self._get_remote_dependencies_and_create_iso(aplm_patch, output_file, lm_clean_iso)
        return output_file

    def read_contents(self, aplm_patch: str) -> dict[str, Any]:
        with zipfile.ZipFile(aplm_patch, "r") as zf:
            with zf.open("archipelago.json", "r") as f:
                manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        return manifest

    def verify_base_rom(self, lm_rom_path: str, throw_on_missing_speedups: bool = False):
        # Verifies we have a valid installation of Luigi's Mansion USA. There are some regional file differences.
        self._client_logger.info(f"Verifying if the provided ISO is a valid copy of {RANDOMIZER_NAME} USA edition.")
        self._client_logger.info("Checking GCLib and speedup libs.")
        # We try importing speedups (pyfastyaz0yay0) to make sure speedups is accessible.
        import pyfastyaz0yay0
        from gclib import fs_helpers as fs, yaz0_yay0
        self._client_logger.info(f"Using GCLib from path: {str(fs.__file__)}")
        self._client_logger.info(f"Using speedups from path: {str(pyfastyaz0yay0.__file__)}")
        self._client_logger.info(sys.modules["gclib.yaz0_yay0"])

        if yaz0_yay0.PY_FAST_YAZ0_YAY0_INSTALLED:
            self._client_logger.info("Speedups detected.")
        else:
            self._client_logger.info("Python module paths: %s", sys.path)
            if throw_on_missing_speedups:
                raise ImportError(f"Cannot continue patching {RANDOMIZER_NAME} due to missing libraries.")
            self._client_logger.info("Continuing patching without speedups.")

        base_md5 = md5()
        with open(lm_rom_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read the file in chunks.
                base_md5.update(chunk)

            # Grab the Magic Code and Game_ID with the file still open
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
            self._client_logger.info(f"LM Magic Code: {magic}; LM Game ID: {game_id}")

        # Verify that the file has the right has first, as the wrong file could have been loaded.
        md5_conv = int(base_md5.hexdigest(), 16)
        if md5_conv != LM_USA_MD5:
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your " +
                f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {LM_USA_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

        # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
        # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                                       "only supports ISOs in ISO format.")
        if game_id != LM_GC_IDs.USA_ID:
            if game_id and game_id.startswith("GLM"):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                    "Currently, only the North American version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError(f"Non-{RANDOMIZER_NAME} game detected. Please re-select the vanilla " +
                    f"{RANDOMIZER_NAME}'s ISO (North American version).")
        return


    def download_lib_zip(self, tmp_dir_path: str) -> None:
        self._client_logger.info("Getting missing dependencies for Luigi's Mansion from remote source.")

        from ..LMClient import CLIENT_VERSION
        from sys import version_info
        lib_path = self._get_archive_name()
        lib_path_base = f"https://github.com/BootsinSoots/Archipelago/releases/download/{CLIENT_VERSION}"
        download_path = f"{lib_path_base}/{lib_path}{version_info.major}-{version_info.minor}.zip"

        temp_zip_path = os.path.join(tmp_dir_path, "temp.zip")
        try:
            with requests.get(download_path, stream=True) as response:
                response.raise_for_status()
                with open(temp_zip_path, 'wb') as created_zip:
                    for chunk in response.iter_content(chunk_size=8192):
                        created_zip.write(chunk)
        except Exception as downloadEx:
            self._client_logger.error("While trying to download LM dependencies from the release page, an unexpected error " +
                f"occurred while using the requests library. Additional details: {str(downloadEx)}")
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(download_path, context=ssl_context) as response, \
                open(temp_zip_path, 'wb') as created_zip:
                created_zip.write(response.read())

        with zipfile.ZipFile(temp_zip_path) as z:
            z.extractall(tmp_dir_path)

        return

    def create_iso(self, patch_file_path: str, output_iso_path: str, vanilla_iso_path: str, throw_error: bool):
        # Verify we have a clean rom of the game first
        self.verify_base_rom(vanilla_iso_path, throw_error)

        # Use our randomize function to patch the file into an ISO.
        from .LM_Randomize_ISO import LuigisMansionRandomizer
        with zipfile.ZipFile(patch_file_path, "r") as zf:
            aplm_bytes = zf.read("patch.aplm")
        lm_rando: LuigisMansionRandomizer = LuigisMansionRandomizer(vanilla_iso_path, output_iso_path, aplm_bytes)
        lm_rando.create_randomized_iso()

    def _get_remote_dependencies_and_create_iso(self, aplm_patch: str, output_file: str, lm_clean_iso: str):
        local_dir_path: str = "N/A"
        try:
            local_dir_path = get_temp_folder_name()
            # If temp directory exists, and we failed to patch the ISO, we want to remove the directory
            #   and instead get a fresh installation.
            if os.path.isdir(local_dir_path):
                self._client_logger.info("Found temporary directory after unsuccessful attempt of generating seed, deleting %s.", local_dir_path)
                shutil.rmtree(local_dir_path)
            os.makedirs(local_dir_path, exist_ok=True)
            # Load the external dependencies based on OS
            self._client_logger.info("Temporary Directory created as: %s", local_dir_path)
            self.download_lib_zip(local_dir_path)

            self._client_logger.info(f"Appending the following to sys path to get dependencies correctly: {local_dir_path}")
            sys.path.insert(0, local_dir_path)

            self.create_iso(aplm_patch, output_file, lm_clean_iso, False)
        except PermissionError:
            self._client_logger.warning("Failed to cleanup temp folder, %s ignoring delete.", local_dir_path)


def get_temp_folder_name() -> str:
    """Gets a temp file based on the current OS, then a subdirectory for game, version, and libs."""
    temp_path = os.path.join(tempfile.gettempdir(), "luigis_mansion", CLIENT_VERSION, "libs")
    return temp_path


def get_base_rom_path() -> str:
    """Gets the base rom path from the host.yml settings."""
    options: Settings = get_settings()
    file_name = options["luigismansion_options"]["iso_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name
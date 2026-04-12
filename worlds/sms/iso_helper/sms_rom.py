from hashlib import md5
from typing import Any
import shutil
import json, logging, sys, os, zipfile, tempfile
import requests, ssl, certifi, urllib.request

from worlds.Files import APPatch, APPlayerContainer, AutoPatchRegister
from settings import get_settings, Settings
from NetUtils import convert_to_base_types
import Utils


logger = logging.getLogger()
MAIN_PKG_NAME = "worlds.supermariosunshine.SMSPatcher"

RANDOMIZER_NAME = "Super Mario Sunshine"
SMS_USA_MD5 = 0x0c6d2edae9fdf40dfc410ff1623e4119

class InvalidCleanISOError(Exception):
    """
    Exception raised for when user has an issue with their provided Super Mario Sunshine ISO.

    Attributes:
        message -- Explanation of error
    """

    def __init__(self, message="Invalid Clean ISO provided"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"InvalidCleanISOError: {self.message}"
    
class SMSPlayerContainer(APPlayerContainer):
    game = RANDOMIZER_NAME
    compression_method = zipfile.ZIP_DEFLATED
    patch_file_ending = ".apsms"

    def __init__(self, player_choices: dict, patch_path: str, player_name: str, player: int, server: str = ""):
        self.output_data = player_choices
        super().__init__(patch_path, player, player_name, server)

    def write_contents(self, opened_zipfile: zipfile.ZipFile) -> None:
        opened_zipfile.writestr("patch.apsms", json.dumps(self.output_data, indent=4, default=convert_to_base_types))
        super().write_contents(opened_zipfile)

class SMSPatch(APPatch, metaclass=AutoPatchRegister):
    game = RANDOMIZER_NAME
    hash = SMS_USA_MD5
    patch_file_ending = ".apsms"
    result_file_ending = ".iso"

    procedure = ["custom"]

    def __init__(self, *args: Any, **kwargs: Any):
        super(SMSPatch, self).__init__(*args, **kwargs)

    def __get_archive_name(self) -> str:
        if not (Utils.is_linux or Utils.is_windows):
            message = f"Your OS is not supported with this randomizer {sys.platform}."
            logger.error(message)
            raise RuntimeError(message)

        lib_path = ""
        if Utils.is_windows:
            lib_path = "lib-windows"
        elif Utils.is_linux:
            lib_path = "lib-linux"

        logger.info(f"Dependency archive name to use: {lib_path}")
        return lib_path

    def __get_temp_folder_name(self) -> str:
        CLIENT_VERSION = "0.5.0"
        # from ..SMSClient import CLIENT_VERSION
        temp_path = os.path.join(tempfile.gettempdir(), "super_mario_sunhine", CLIENT_VERSION, "libs")
        return temp_path

    def patch(self, apsms_patch: str) -> str:
        # Get the AP Path for the base ROM
        sms_clean_iso = self.get_base_rom_path()
        logger.info("Provided Super Mario Sunshine ISO Path was: " + sms_clean_iso)

        base_path = os.path.splitext(apsms_patch)[0]
        output_file = base_path + self.result_file_ending

        try:
            # Verify we have a clean rom of the game first
            self.verify_base_rom(sms_clean_iso, throw_on_missing_speedups=True)

            # Use our randomize function to patch the file into an ISO.
            from ..SMSPatcher import SuperMarioSunshineRandomizer
            with zipfile.ZipFile(apsms_patch, "r") as zf:
                apsms_bytes = zf.read("patch.apsms")
            SuperMarioSunshineRandomizer(sms_clean_iso, output_file, apsms_bytes)
        except ImportError:
            self.__get_remote_dependencies_and_create_iso(apsms_patch, output_file, sms_clean_iso)
        return output_file

    def read_contents(self, apsms_patch: str) -> dict[str, Any]:
        with zipfile.ZipFile(apsms_patch, "r") as zf:
            with zf.open("archipelago.json", "r") as f:
                manifest = json.load(f)
        if manifest["compatible_version"] > self.version:
            raise Exception(f"File (version: {manifest['compatible_version']}) too new "
                            f"for this handler (version: {self.version})")
        return manifest

    @classmethod
    def get_base_rom_path(cls) -> str:
        options: Settings = get_settings()
        file_name = options["sms_options"]["iso_file"]
        if not os.path.exists(file_name):
            file_name = Utils.user_path(file_name)
        return file_name

    @classmethod
    def verify_base_rom(cls, sms_rom_path: str, throw_on_missing_speedups: bool = False):
        # Verifies we have a valid installation of Super Mario Sunshine USA. There are some regional file differences.
        logger.info("Verifying if the provided ISO is a valid copy of Super Mario Sunshine USA edition.")
        logger.info("Checking GCLib and speedup libs.")
        # We try importing speedups (pyfastyaz0yay0) to make sure speedups is accessible.
        import pyfastyaz0yay0
        from gclib import fs_helpers as fs, yaz0_yay0
        logger.info("Using GCLib from path: %s.", fs.__file__)
        logger.info("Using speedups from path: %s.", pyfastyaz0yay0.__file__)
        logger.info(sys.modules["gclib.yaz0_yay0"])

        if yaz0_yay0.PY_FAST_YAZ0_YAY0_INSTALLED:
            logger.info("Speedups detected.")
        else:
            logger.info("Python module paths: %s", sys.path)
            if throw_on_missing_speedups:
                logger.info("Speedups not detected, attempting to pull remote release.")
                raise ImportError("Cannot continue patching Super Mario Sunshine due to missing libraries.")
            logger.info("Continuing patching without speedups.")

        base_md5 = md5()
        with open(sms_rom_path, "rb") as f:
            while chunk := f.read(1024 * 1024):  # Read the file in chunks.
                base_md5.update(chunk)

            # Grab the Magic Code and Game_ID with the file still open
            magic = fs.try_read_str(f, 0, 4)
            game_id = fs.try_read_str(f, 0, 6)
            logger.info(f"Magic Code: {magic}")
            logger.info(f"SMS Game ID: {game_id}")

        # Verify that the file has the right hash first, as the wrong file could have been loaded.
        md5_conv = int(base_md5.hexdigest(), 16)
        if md5_conv != SMS_USA_MD5:
            raise InvalidCleanISOError(f"Invalid vanilla {RANDOMIZER_NAME} ISO.\nYour ISO may be corrupted or your " +
                f"MD5 hashes do not match.\nCorrect ISO MD5 hash: {SMS_USA_MD5:x}\nYour ISO's MD5 hash: {md5_conv}")

        # Verify if the provided ISO file is a valid file extension and contains a valid Game ID.
        # Based on some similar code from (MIT License): https://github.com/LagoLunatic/wwrando
        if magic == "CISO":
            raise InvalidCleanISOError(f"The provided ISO is in CISO format. The {RANDOMIZER_NAME} randomizer " +
                                       "only supports ISOs in ISO format.")
        if game_id != "GMSE01":
            if game_id and game_id.startswith("GMS"):
                raise InvalidCleanISOError(f"Invalid version of {RANDOMIZER_NAME}. " +
                                           "Currently, only the North American version is supported by this randomizer.")
            else:
                raise InvalidCleanISOError("Invalid game given as the vanilla ISO. You must specify a " +
                                           f"{RANDOMIZER_NAME}'s ISO (North American version).")
        return


    def download_lib_zip(self, tmp_dir_path: str) -> None:
        logger.info("Getting missing dependencies for Super Mario Sunshine from remote source.")

        from ..SMSClient import CLIENT_VERSION
        from sys import version_info
        lib_path = self.__get_archive_name()
        lib_path_base = f"https://github.com/Joshark/archipelago-sms/releases/download/{CLIENT_VERSION}"
        download_path = f"{lib_path_base}/{lib_path}{version_info.major}-{version_info.minor}.zip"

        temp_zip_path = os.path.join(tmp_dir_path, "temp.zip")
        try:
            with requests.get(download_path, stream=True) as response:
                response.raise_for_status()
                with open(temp_zip_path, 'wb') as created_zip:
                    for chunk in response.iter_content(chunk_size=8192):
                        created_zip.write(chunk)
        except Exception as downloadEx:
            logger.error("While trying to download SMS dependencies from the release page, an unexpected error " +
                f"occurred while using the requests library. Additional details: {str(downloadEx)}")
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            with urllib.request.urlopen(download_path, context=ssl_context) as response, \
                open(temp_zip_path, 'wb') as created_zip:
                created_zip.write(response.read())

        with zipfile.ZipFile(temp_zip_path) as z:
            z.extractall(tmp_dir_path)

        return

    def create_iso(self, temp_dir_path: str, patch_file_path: str, output_iso_path: str, vanilla_iso_path: str):
        logger.info(f"Appending the following to sys path to get dependencies correctly: {temp_dir_path}")
        sys.path.insert(0, temp_dir_path)

        # Verify we have a clean rom of the game first
        self.verify_base_rom(vanilla_iso_path)

        # Use our randomize function to patch the file into an ISO.
        from ..SMSPatcher import SuperMarioSunshineRandomizer
        with zipfile.ZipFile(patch_file_path, "r") as zf:
            apsms_bytes = zf.read("patch.apsms")
        SuperMarioSunshineRandomizer(vanilla_iso_path, output_iso_path, apsms_bytes)

    def __get_remote_dependencies_and_create_iso(self, apsms_patch: str, output_file: str, sms_clean_iso: str):
        try:
            local_dir_path = self.__get_temp_folder_name()
            # If temp directory exists, and we failed to patch the ISO, we want to remove the directory
            #   and instead get a fresh installation.
            if os.path.isdir(local_dir_path):
                logger.info("Found temporary directory after unsuccessful attempt of generating seed, deleting %s.", local_dir_path)
                shutil.rmtree(local_dir_path)
            os.makedirs(local_dir_path, exist_ok=True)
            # Load the external dependencies based on OS
            logger.info("Temporary Directory created as: %s", local_dir_path)
            self.download_lib_zip(local_dir_path)
            self.create_iso(local_dir_path, apsms_patch, output_file, sms_clean_iso)
        except PermissionError:
            logger.warning("Failed to cleanup temp folder, %s ignoring delete.", local_dir_path)
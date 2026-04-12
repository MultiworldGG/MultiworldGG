""" Module for launching dolphin emulator """
import logging
import subprocess
import psutil
import settings
import Utils

from .luigismansion_settings import LuigisMansionSettings, EmulatorSettings
from .constants import AP_LOGGER_NAME

logger = logging.getLogger(AP_LOGGER_NAME)

class DolphinLauncher:
    """
    Manages interactions between the LMClient and the dolphin emulator.
    """
    emulator_settings: EmulatorSettings
    dolphin_process_name = "dolphin"
    exclusion_dolphin_process_name: list[str] = ["dolphinmemoryengine"]

    def __init__(self, luigismansion_settings: LuigisMansionSettings = None):
        if luigismansion_settings is None:
            self.emulator_settings: EmulatorSettings = settings.get_settings().luigismansion_options.dolphin_settings
        else:
            self.emulator_settings = luigismansion_settings.dolphin_settings

    async def launch_dolphin_async(self, rom: str):
        """
        Launches the emulator process if not already running.

        :param rom: The rom to load into emulator when starting the process,
            if 'None' the process won't load any rom.
        """
        if not self.emulator_settings.auto_start:
            logger.info("Host.yaml settings 'auto_start' is 'false', skipping.")
            return

        if _check_emulator_process_open(self):
            return

        path = self.emulator_settings.path
        if Utils.is_linux and path in [ "", "./" ]:
            raise ValueError("The emulator path is not set, please update the host.yaml file with the emulator path.")

        args = [ path ] + self.emulator_settings.additional_args

        logger.info("Attempting to open emulator with the following arguments:'%s'",  ' '.join(args))
        if rom:
            logger.info("Attempting to open emulator with rom path:%s", rom)
            args.append(f"--exec={rom}")

        subprocess.Popen(
            args,
            cwd=None,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

def _check_emulator_process_open(dl: DolphinLauncher) -> bool:
    for proc in psutil.process_iter():
        if (dl.dolphin_process_name in proc.name().lower() and not any(
            exclude_name for exclude_name in dl.exclusion_dolphin_process_name if exclude_name in proc.name().lower())):
            logger.info("Located existing Dolphin process: %s, skipping.", proc.name())
            return True
    logger.info("No existing Dolphin processes, continuing.")
    return False

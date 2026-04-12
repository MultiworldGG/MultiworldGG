import json
import os

from gclib.gcm import GCM
from gclib.dol import DOL
from gclib.rarc import RARC

import Utils
from CommonClient import logger
from .SMSClient import CLIENT_VERSION, AP_WORLD_VERSION_NAME
from .Helper_Functions import StringByteFunction as sbf
from .patch import update_dol_offsets

RANDOMIZER_NAME = "Super Mario Sunshine"

class SuperMarioSunshineRandomizer:
    def __init__(self, clean_iso_path: str, randomized_output_file_path: str, ap_output_data: bytes, debug_flag=False):
        self.debug = debug_flag
        self.clean_iso_path = clean_iso_path
        self.randomized_output_file_path = randomized_output_file_path

        try:
            if os.path.isfile(randomized_output_file_path):
                temp_file = open(randomized_output_file_path, "r+")
                temp_file.close()
        except IOError:
            raise Exception(f"{randomized_output_file_path} is currently in use by another program")

        self.output_data = json.loads(ap_output_data.decode("utf-8"))

        self.gcm = GCM(self.clean_iso_path)
        self.gcm.read_entire_disc()
        self.dol = DOL()

        self.seed = self.output_data["Seed"]

        self.save_randomized_iso()

    def _check_server_version(self, output_data):
        """
        Compares the version provided in the patch manifest against the client's version

        :param output_data: The manifest's output data which we attempt to acquire the generated version
        """
        ap_world_version = "<0.5.0"

        if AP_WORLD_VERSION_NAME in output_data:
            ap_world_version = output_data[AP_WORLD_VERSION_NAME]
        if ap_world_version != CLIENT_VERSION:
            raise Utils.VersionException("Error! Server was generated with a different Super Mario Sunshine " +
                    f"APWorld version.\nThe client version is {CLIENT_VERSION}!\nPlease verify you are using the " +
                    f"same APWorld as the generator, which is '{ap_world_version}'")

    def get_arc(self, arc_path):
        arc_path = arc_path.replace("\\", "/")
        arc = RARC(self.gcm.read_file_data(arc_path))
        arc.read()
        return arc

    def save_randomized_iso(self):
        bool_level_access: bool = bool(self.output_data["Options"]["level_access"])
        bool_coin_shines: bool = bool(self.output_data["Options"]["enable_coin_shines"])
        blue_coin_rando: int = int(self.output_data["Options"]["blue_coin_sanity"])
        starting_nozzle: int = int(self.output_data["Options"]["starting_nozzle"])
        player_name: str = str(self.output_data["Name"])
        all_shines_selectable: bool = bool(self.output_data["Options"]["all_shines_selectable"])

        logger.info("Updating all the main.dol offsets with their appropriate values.")
        self.gcm, self.dol = update_dol_offsets(self.gcm, self.dol, self.seed, player_name, starting_nozzle,
            bool_level_access, bool_coin_shines, blue_coin_rando, all_shines_selectable)

        for _, _ in self.export_files_from_memory():
            continue

    def export_files_from_memory(self):
        yield from self.gcm.export_disc_to_iso_with_changed_files(self.randomized_output_file_path)


if __name__ == '__main__':
    print("Run this from Launcher.py instead.")

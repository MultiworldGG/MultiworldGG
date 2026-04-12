# Python related imports.
import copy
import json, os
from logging import Logger, getLogger
from random import Random
from importlib.resources import read_text

# AP Related Imports
import Utils

# 3rd Party related imports
from gclib.gcm import GCM
from gclib.fs_helpers import read_str, write_str
from gcbrickwork import JMP

# Internal Related imports.
from .dol.DOL_Updater import update_dol_offsets
from .Events import EventChanges
from .jmp_changes.Randomize_JMP_Tables import RandomizeJMPTables
from .LM_Map_File import LMMapFile
from ..client.constants import CLIENT_VERSION, AP_WORLD_VERSION_NAME, RANDOMIZER_NAME, CLIENT_NAME, LM_GC_IDs
from .LM_GameUSA_Arc import LMGameUSAArc
from ..Helper_Functions import LMDynamicAddresses

class LuigisMansionRandomizer:

    # Output data related vars
    output_data: dict
    slot: int

    # GCLib related vars
    lm_gcm: GCM
    game_region_arc: LMGameUSAArc

    # Other Class Vars
    debug: bool
    clean_iso_path: str
    output_file_path: str
    map_files: dict[str, LMMapFile]
    jmp_names_json: dict
    empty_jmp_files: dict[str, JMP]
    client_logger: Logger
    _seed: str
    random: Random
    lm_dynamic_addr: LMDynamicAddresses

    def __init__(self, clean_iso_path: str, randomized_output_file_path: str, ap_output_data: bytes, debug_flag=False):
        self.debug = debug_flag
        self.clean_iso_path = clean_iso_path
        self.output_file_path = randomized_output_file_path
        self.output_data = json.loads(ap_output_data.decode('utf-8'))

        # Init the logger based on the existing client name.
        self.client_logger = getLogger(CLIENT_NAME)

        # Set the random's seed for use in other files.
        self._seed = self.output_data["Seed"]
        self.random = Random()
        self.random.seed(self._seed)

        self.slot = self.output_data["Slot"]
        self._get_jmp_name_list()
        self.map_files = {}
        self.empty_jmp_files = {}
        self.lm_dynamic_addr = LMDynamicAddresses()

    def _get_jmp_name_list(self):
        """Gets the jmp dictionary name list and re-maps it from a string to int."""
        name_list: dict = json.loads(read_text("worlds.luigismansion.data", "jmp_names.json"))
        for jmp_file_name in name_list.keys():
            hash_and_names: dict = name_list[jmp_file_name]
            name_list[jmp_file_name] = {int(key): value for key, value in hash_and_names.items()}
        self.jmp_names_json = name_list

    def create_randomized_iso(self):
        # Check if the file is in use and return an error if so.
        try:
            if os.path.isfile(self.output_file_path):
                temp_file = open(self.output_file_path, "r+")  # or "a+", whatever you need
                temp_file.close()
        except IOError:
            raise Exception(f"'{self.output_file_path}' is currently in use by another program.")

        # Make sure that the server and client versions match before attempting to patch ISO.
        self._check_server_version()

        # After verifying, this will also read the entire iso, including system files and their content
        self.lm_gcm = GCM(self.clean_iso_path)
        self.lm_gcm.read_entire_disc()

        # Change game ID so save files are different
        lm_regional_id: str = self._get_and_update_game_id()

        # Update the relevant Game RARC archive
        self._load_game_archive(lm_regional_id)

        # Update all of our items to have their dynamic values.
        self.lm_dynamic_addr.update_item_addresses()

        self.client_logger.info("Updating all the main.dol offsets with their appropriate values.")
        update_dol_offsets(self)

        self.client_logger.info("Updating all the in-game events with their appropriate triggers, hints, etc.")
        self._update_events()

        # Loads all the relevant map files and their JMP files into memory.
        self._load_map_files()

        # Updates all the JMP Tables to have their relevant changes
        jmp_tables: RandomizeJMPTables = RandomizeJMPTables(self)
        jmp_tables.randomize_jmp_tables()

        # Saves all the map files back to disc
        self._update_map_files()

        # Updates the game archive file
        self._update_game_archive()

        # Generator function to combine all necessary files into an ISO file.
        # Returned information is ignored.
        for _, _ in self._export_files_from_memory():
            continue


    def _check_server_version(self):
        """Compares the version provided in the patch manifest against the client's version."""

        ap_world_version: str = self.output_data.get(AP_WORLD_VERSION_NAME, "<0.5.6")
        if ap_world_version != CLIENT_VERSION:
            raise Utils.VersionException(f"Error! Server was generated with a different {RANDOMIZER_NAME} " +
                 f"APWorld version.\nThe client version is {CLIENT_VERSION}!\nPlease verify you are using the " +
                 f"same APWorld as the generator, which is '{ap_world_version}'")

    def _get_and_update_game_id(self) -> str:
        """
        Updates the ISO's game id to use AP's seed that was generated.
        This allows LM to have 3 brand new save files every time.
        """
        self.client_logger.info("Updating the ISO game id with the AP generated seed.")
        bin_data = self.lm_gcm.read_file_data("sys/boot.bin")
        regional_id: str = read_str(bin_data, 0x00, 6)
        write_str(bin_data, 0x01, str(self._seed), len(str(self._seed))+1)
        self.lm_gcm.changed_files["sys/boot.bin"] = bin_data

        return regional_id

    def _load_game_archive(self, regional_id: str):
        # Load game_usa and prepare those changes. Leaves wiggle room for support to other LM regions (potentially)
        match regional_id:
            case LM_GC_IDs.USA_ID:
                self.game_region_arc: LMGameUSAArc = LMGameUSAArc(self.client_logger, self.lm_gcm, "files/Game/game_usa.szp")
                self.game_region_arc.add_gold_ghost()

    def _load_map_files(self):
        """Loads all the map file data, including JMP files.
        Some maps do not have the same jmp files available, so empty map2 data is also loaded."""
        map2_jmp_list: list[str] = ["iteminfotable", "itemappeartable", "treasuretable", "furnitureinfo", "characterinfo",
            "eventinfo", "observerinfo", "keyinfo", "objinfo", "generatorinfo", "telesa", "teidenobserverinfo",
            "teidencharacterinfo", "iyapootable"]
        map1_jmp_list: list[str] = ["eventinfo"]
        map3_jmp_list: list[str] = ["eventinfo"]
        map6_jmp_list: list[str] = ["furnitureinfo"]


        if bool(self.output_data["Options"]["speedy_spirits"]) or int(self.output_data["Options"]["enemizer"]) > 0:
            map2_jmp_list.append("enemyinfo")
            map2_jmp_list.append("teidenenemyinfo")

        if self.output_data["Options"]["spookiness"] != 0:
            map2_jmp_list.append("roominfo")

        self.client_logger.info(f"Now loading map2.szp with the following jmp list: {'; '.join(map2_jmp_list)}")
        map2: LMMapFile = LMMapFile(self.lm_gcm, "files/Map/map2.szp")
        map2.load_jmp_files(map2_jmp_list)
        map2.update_jmp_names(self.jmp_names_json)
        self.map_files["map2"] = map2
        self.client_logger.info(f"Now creating empty jmp files based on map2...")
        self._get_empty_jmp_files()

        self.client_logger.info(f"Now loading map1.szp with the following jmp list: {'; '.join(map1_jmp_list)}")
        map1: LMMapFile = LMMapFile(self.lm_gcm, "files/Map/map1.szp")
        map1.load_jmp_files(map1_jmp_list)
        map1.update_jmp_names(self.jmp_names_json)
        self.map_files["map1"] = map1

        self.client_logger.info(f"Now loading map3.szp with the following jmp list: {'; '.join(map3_jmp_list)}")
        map3: LMMapFile = LMMapFile(self.lm_gcm, "files/Map/map3.szp")
        map3.load_jmp_files(map3_jmp_list)
        map3.update_jmp_names(self.jmp_names_json)
        self.map_files["map3"] = map3

        self.client_logger.info(f"Now loading map6.szp with the following jmp list: {'; '.join(map6_jmp_list)}")
        map6: LMMapFile = LMMapFile(self.lm_gcm, "files/Map/map6.szp")
        if bool(self.output_data["Options"]["WDYM_checks"]):
            map6.load_jmp_files(map6_jmp_list)
            map6.update_jmp_names(self.jmp_names_json)
        self.map_files["map6"] = map6

    def _get_empty_jmp_files(self):
        """Loads all jmp files from Map2, excepts removes any JMP entries and loads a default one that can
        be used/manipulated."""
        temp_map2: LMMapFile = copy.deepcopy(self.map_files["map2"])
        temp_map2.get_all_jmp_files()
        for jmp_name, jmp_entry in temp_map2.jmp_files.items():
            temp_map2.jmp_files[jmp_name].clear_data_entries()
        self.empty_jmp_files = temp_map2.jmp_files

    def _update_map_files(self):
        """Updates and saves all that map data back into the GCM."""
        for map_name, map_file in self.map_files.items():
            self.client_logger.info(f"Now saving map '{map_name}'s data...")
            map_file.update_and_save_map(self.lm_gcm)

    def _update_game_archive(self):
        """Updates the game archive file back into the GCM."""
        self.game_region_arc.update_game_usa()

    def _update_events(self):
        """Updates all the event files to include hint info, new triggers, etc."""
        event_changes: EventChanges = EventChanges(self)
        event_changes.update_in_game_events()

    def _export_files_from_memory(self):
        """Saves the files to export them into their expected output location."""
        yield from self.lm_gcm.export_disc_to_iso_with_changed_files(self.output_file_path)
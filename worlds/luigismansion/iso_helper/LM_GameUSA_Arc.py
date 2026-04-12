from enum import StrEnum
from logging import Logger

from gclib.gcm import GCM
from gclib.rarc import RARC, RARCFileEntry
from gclib.yaz0_yay0 import Yay0
from gcbrickwork.PRM import PRM

from ..Helper_Functions import get_arc, find_rarc_file_entry

class _ParamType(StrEnum):
    TH = "TH"
    CTP = "CTP"

class LMGameUSAArc:

    # GCLib related vars
    lm_gcm: GCM
    game_usa_arc: RARC
    _ctp_files: list[RARCFileEntry]
    _th_files: list[RARCFileEntry]

    # Other Class Vars
    _arc_path: str
    _client_logger: Logger
    ctp_params: dict[str, PRM]
    th_params: dict[str, PRM]

    def __init__(self, logger: Logger, user_gcm: GCM, arc_path: str):
        self.lm_gcm = user_gcm
        self._arc_path = arc_path
        self.game_usa_arc: RARC = get_arc(self.lm_gcm, arc_path)
        self._client_logger = logger
        self._ctp_files = self.game_usa_arc.get_node_by_path("param/ctp").files
        self._th_files = self.game_usa_arc.get_node_by_path("param/th").files
        self.ctp_params = {}
        self.th_params = {}

    def add_gold_ghost(self):
        """
        In order to trigger the Gold Ghost trap properly, we need to copy its file into the game_usa archive.
        However, since game_usa is very full, we must also delete and remove some unused files, otherwise game_usa
            is too large to load and will crash the emulator.
        """
        self._remove_unused_files()
        obake_copy = get_arc(self.lm_gcm, "files/model/obake01.szp")
        self._client_logger.info("Adding Gold Ghost image into the model folder")
        self.game_usa_arc.add_new_file("obake01.arc", obake_copy.data, self.game_usa_arc.get_node_by_path("model"))

    def _remove_unused_files(self):
        """
        In order to keep game_usa loadable, several un-used files such as sky boxes, textboxes, images, and param files
            will be removed in order to make space, so the emulator can properly load this file.
        """
        self._client_logger.info("Deleting Unused Skybox (vrbox) in iwamoto")
        vrbox_data = find_rarc_file_entry(self.game_usa_arc, "iwamoto", "vrbox")
        self.game_usa_arc.delete_directory(vrbox_data)

        self._client_logger.info("Deleting Unused Textbox in kawano")
        unused_window = find_rarc_file_entry(self.game_usa_arc, "dmman", "m_window3.bti")
        self.game_usa_arc.delete_file(unused_window)

        self._client_logger.info("Deleting Unused Image File in kawano")
        unused_image = find_rarc_file_entry(self.game_usa_arc, "base", "cgbk_v.tim")
        self.game_usa_arc.delete_file(unused_image)

        self._client_logger.info("Deleting Unused param files iyapoo21 through iyapoo25")
        unused_params: list[str] = ["iyapoo21.prm", "iyapoo22.prm", "iyapoo23.prm", "iyapoo24.prm", "iyapoo25.prm"]
        for unused_prm in unused_params:
            prm_file = find_rarc_file_entry(self.game_usa_arc, "ctp", unused_prm)
            self.game_usa_arc.delete_file(prm_file)

        self._client_logger.info("Deleting Unused Image File in kt_static")
        unused_second_image = find_rarc_file_entry(self.game_usa_arc, "kt_static", "test.bti")
        self.game_usa_arc.delete_file(unused_second_image)

        self._client_logger.info("Deleting Unused Image File in model")
        unused_model = find_rarc_file_entry(self.game_usa_arc, "model", "takara1.arc")
        self.game_usa_arc.delete_file(unused_model)

    def update_game_usa(self):
        """
        Updates the game_usa arc into the GCM
        """
        self._client_logger.info("Updating all parameter files...")
        self._update_parameters()
        self._client_logger.info("Overwriting game_uza.szp with the new re-created file...")
        self.game_usa_arc.save_changes()
        self._client_logger.info("game_uza.szp Yay0 check...")
        self.lm_gcm.changed_files[self._arc_path] = Yay0.compress(self.game_usa_arc.data)

    def load_ctp_list_parameters(self, ctp_params: list[str]):
        """
        Loads several parameter files in the "CTP" folder based on a user provided input list.
        """
        for ctp_param in ctp_params:
            self.ctp_params[ctp_param] = self._load_prm(_ParamType.CTP, ctp_param)

    def load_th_list_parameters(self, th_params: list[str]):
        """
        Loads several parameter files in the "TH" folder based on a user provided input list.
        """
        for th_param in th_params:
            self.th_params[th_param] = self._load_prm(_ParamType.TH, th_param)

    def load_ctp_parameter(self, ctp_param_name: str):
        """
        Loads a single parameter files from the "CTP" folder.
        """
        self.ctp_params[ctp_param_name] = self._load_prm(_ParamType.CTP, ctp_param_name)

    def load_th_parameter(self, th_param_name: str):
        """
        Loads a single parameter files from the "TH" folder.
        """
        self.th_params[th_param_name] = self._load_prm(_ParamType.TH, th_param_name)

    def _load_prm(self, param_folder: str, param_name: str) -> PRM:
        """
        Returns a PRM file if it is already loaded in memory, otherwise searches for the relevant file in the right folder
            and loads it as a PRM type.
        """
        match param_folder:
            case _ParamType.TH:
                if param_name in self.th_params:
                    return self.th_params[param_name]

                prm_file: RARCFileEntry = next(arc_prm for arc_prm in self._th_files if arc_prm.name == param_name)
                return PRM.load_prm(prm_file.data)
            case _ParamType.CTP:
                if param_name in self.ctp_params:
                    return self.ctp_params[param_name]

                prm_file: RARCFileEntry = next(arc_prm for arc_prm in self._ctp_files if arc_prm.name == param_name)
                return PRM.load_prm(prm_file.data)

            case _:
                raise Exception("Unknown type of PRM file provided: " + param_folder)

    def _update_parameters(self):
        """
        Updates all parameter files in both CTP and TH folders and re-add the data back into the GameUSA RARC.
        """
        for th_param in self._th_files:
            if not th_param.name in self.th_params:
                continue

            th_file: PRM = self.th_params[th_param.name]
            th_param.data = th_file.create_new_prm()

        for ctp_param in self._ctp_files:
            if not ctp_param.name in self.ctp_params:
                continue

            ctp_file: PRM = self.ctp_params[ctp_param.name]
            ctp_param.data = ctp_file.create_new_prm()
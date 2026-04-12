from io import BytesIO

from gcbrickwork import JMP
from gclib.gcm import GCM
from gclib.rarc import RARC, RARCFileEntry
from gclib.yaz0_yay0 import Yay0

from ..Helper_Functions import get_arc, find_rarc_file_entry


class LMMapFile:
    _arc_data: RARC
    _arc_path: str
    jmp_files: dict[str, JMP]

    def __init__(self, lm_gcm: GCM, map_rarc_path: str):
        """
        Creates an object representation of an LM Map file, which can contain several directories/files such as:
            JMP (JUMP) object tables, Path files (which describe literal paths characters take), and J3D effect/animation files.
        Automatically caches all JMP table RARCFileEntries to make it easier to query later.
        Automatically also decompresses from Yay0 format.
        """
        self._arc_path = map_rarc_path
        self._arc_data = get_arc(lm_gcm, map_rarc_path)
        self.jmp_files = {}

    def add_new_jmp_file(self, file_name: str, data: BytesIO):
        """Creates a new JMP file name with the provided name and BytesIO data."""
        self._arc_data.add_new_file(file_name, data, self._arc_data.get_node_by_path("jmp"))

    def get_all_jmp_files(self):
        """
        Loads all JMP files found within the arc file into self.jmp_files object.
        """
        bad_jmp_names: list[str] = [".", ".."]
        self.load_jmp_files([jmp.name for jmp in self._arc_data.get_node_by_path("jmp").files if not jmp.name in bad_jmp_names])

    def load_jmp_files(self, jmp_file_names: list[str]):
        """
        Loads one or more JMP files based on the provided list of JMP file names
        """
        for jmp_file_name in jmp_file_names:
            self.jmp_files[jmp_file_name] = self.get_jmp_file(jmp_file_name)

    def get_jmp_file(self, jmp_file_name: str) -> JMP:
        """
        Checks if a JMP file is already loaded in memory and returns that, otherwise searches the arc's jmp files.
        """
        if jmp_file_name in self.jmp_files:
            return self.jmp_files[jmp_file_name]

        jmp_file: RARCFileEntry = find_rarc_file_entry(self._arc_data, "jmp", jmp_file_name)
        if jmp_file is None:
            raise Exception(f"Unable to find the jmp file: '{jmp_file_name}'")

        jmp_file_data: JMP = JMP.load_jmp(jmp_file.data)
        return jmp_file_data

    def update_jmp_names(self, jmp_names: dict):
        for jmp_file_name in jmp_names.keys():
            if not jmp_file_name in self.jmp_files:
                continue

            self.jmp_files[jmp_file_name].map_hash_to_name(jmp_names[jmp_file_name])

    def _update_all_jmp_files(self):
        """
        Updates all jmp files data back into their arc file
        """
        for jmp_name, jmp_file in self.jmp_files.items():
            arc_jmp: RARCFileEntry = find_rarc_file_entry(self._arc_data, "jmp", jmp_name)
            if jmp_file is None:
                raise Exception(f"Unable to find the jmp file: '{jmp_name}'")

            arc_jmp.data = jmp_file.create_new_jmp()

    def update_and_save_map(self, lm_gcm: GCM):
        """
        Saves the map file and all related changes, then recompresses the map back into Yay0 format.
        """
        self._update_all_jmp_files()
        self._arc_data.save_changes()
        lm_gcm.changed_files[self._arc_path] = Yay0.compress(self._arc_data.data)
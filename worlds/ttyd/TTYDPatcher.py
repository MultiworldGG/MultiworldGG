import io
import os
import sys
import tempfile
import zipfile

import Utils
from typing import Dict
from settings import get_settings
from .Data import Rels


def setup_gclib_path():
    """Extracts gclib files from .apworld zip to temp directory if needed."""
    base_path = os.path.dirname(__file__)
    lib_path = os.path.join(base_path, "lib", "gclib")

    if ".apworld" in __file__:
        # Find the .apworld file path
        zip_file_path = __file__
        while not zip_file_path.lower().endswith(".apworld"):
            zip_file_path = os.path.dirname(zip_file_path)

        # Set up temporary extraction directory
        temp_base_dir = tempfile.gettempdir()
        target_dir_path = os.path.join(temp_base_dir, "ttyd_temp_gclib")
        temp_lib_path = os.path.join(target_dir_path, "ttyd", "lib", "gclib")

        # Clean and recreate directory
        if os.path.exists(target_dir_path):
            import shutil
            shutil.rmtree(target_dir_path)
        os.makedirs(target_dir_path, exist_ok=True)

        # Extract gclib files from .apworld zip
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            for member in zip_ref.namelist():
                if "gclib" in member:
                    zip_ref.extract(member, target_dir_path)

        # Add lib directory to Python path for imports
        lib_parent = os.path.join(target_dir_path, "ttyd", "lib")
        if lib_parent not in sys.path:
            sys.path.insert(0, lib_parent)

        return temp_lib_path
    else:
        # For non-apworld case, add the lib directory to path
        lib_parent = os.path.dirname(lib_path)
        if lib_parent not in sys.path:
            sys.path.insert(0, lib_parent)
        return lib_path


def _select_native_binary(pkg_dir: str) -> None:
    import platform
    import shutil
    system = platform.system()
    if system == "Linux":
        src = "_abi3_linux_x86_64.so"
    elif system == "Darwin":
        machine = platform.machine().lower()
        src = "_abi3_macos_arm64.so" if machine in ("arm64", "aarch64") else "_abi3_macos_x86_64.so"
    else:
        return
    src_path = os.path.join(pkg_dir, src)
    dest_path = os.path.join(pkg_dir, "_dolphin_memory_engine.abi3.so")
    if os.path.exists(src_path) and not os.path.exists(dest_path):
        shutil.copyfile(src_path, dest_path)


def setup_dme_path():
    base_path = os.path.dirname(__file__)
    lib_path = os.path.join(base_path, "lib")

    if ".apworld" in __file__:
        zip_file_path = __file__
        while not zip_file_path.lower().endswith(".apworld"):
            zip_file_path = os.path.dirname(zip_file_path)

        target_dir_path = os.path.join(tempfile.gettempdir(), "ttyd_temp_dme")
        lib_parent = os.path.join(target_dir_path, "ttyd", "lib")
        marker = os.path.join(lib_parent, "dolphin_memory_engine_ttyd", "__init__.py")

        if not os.path.exists(marker):
            os.makedirs(target_dir_path, exist_ok=True)
            with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
                for member in zip_ref.namelist():
                    if "dolphin_memory_engine" in member:
                        zip_ref.extract(member, target_dir_path)
    else:
        lib_parent = lib_path

    _select_native_binary(os.path.join(lib_parent, "dolphin_memory_engine_ttyd"))

    if lib_parent not in sys.path:
        sys.path.insert(0, lib_parent)

    pkg_dir = os.path.join(lib_parent, "dolphin_memory_engine_ttyd")
    if hasattr(os, "add_dll_directory") and os.path.isdir(pkg_dir):
        try:
            os.add_dll_directory(pkg_dir)
        except OSError:
            pass

    return lib_parent


dolphin = None


class TTYDPatcher:
    rels: Dict[Rels, io.BytesIO] = {}

    def __init__(self):
        setup_gclib_path()
        from gclib.gcm import GCM
        from gclib.dol import DOL

        self.iso = GCM(get_settings().ttyd_options.rom_file)
        self.iso.read_entire_disc()
        self.dol = DOL()
        self.dol.read(self.iso.read_file_data("sys/main.dol"))
        for rel in Rels:
            if rel == Rels.dol:
                continue
            path = get_rel_path(rel)
            self.rels[rel] = self.iso.read_file_data(path)


def get_rel_path(rel: Rels):
    return f'files/rel/{rel.value}.rel'

import atexit
import random
import os
import shutil
import sys
import tempfile
import zipfile
from Utils import local_path

albw_base_id = 6242624000

tmp_path = ""

def get_temp_path():
    global tmp_path
    return tmp_path

def setup_lib():
    global tmp_path

    # clean up old temp directories
    for directory in os.listdir(tempfile.gettempdir()):
        if directory.startswith("albwrandomizer"):
            path = os.path.join(tempfile.gettempdir(), directory)
            if os.path.exists(os.path.join(path, "cleanup-tag")):
                try:
                    shutil.rmtree(path)
                except:
                    pass

    apworld_path = os.path.dirname(os.path.dirname(__file__))
    if apworld_path.endswith(".apworld"):
        with zipfile.ZipFile(apworld_path, "r") as apworld:
            tmp_path = tempfile.mkdtemp(prefix="albwrandomizer")
            atexit.register(cleanup_lib)
            try:
                randomizer_path = os.path.join(tmp_path, "albwrandomizer")
                if not os.path.exists(randomizer_path):
                    os.mkdir(randomizer_path)
                for info in apworld.infolist():
                    if not info.is_dir() and info.filename.startswith("albw/albwrandomizer/"):
                        info.filename = os.path.basename(info.filename)
                        apworld.extract(info, randomizer_path)
            except Exception as e:
                from tkinter.messagebox import showerror
                showerror(message=str(e))
            if not tmp_path in sys.path:
                sys.path.append(tmp_path)
    else:
        path = os.path.join(os.path.dirname(__file__), "albwrandomizer")
        if not path in sys.path:
            sys.path.append(path)

def cleanup_lib():
    global tmp_path

    if os.path.exists(tmp_path):
        try:
            shutil.rmtree(tmp_path)
        except Exception:
            with open(os.path.join(tmp_path, "cleanup-tag"), "w") as file:
                pass

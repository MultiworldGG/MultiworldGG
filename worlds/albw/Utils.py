import hashlib
import orjson
import os
import shutil
import sys
import tempfile
import zipfile
from Utils import local_path

def setup_lib():
    # clean up any files from old versions of the apworld
    for path in [local_path("."), local_path("lib")]:
        if os.path.exists(path):
            for entry in os.scandir(path):
                if entry.name.startswith("albwrandomizer"):
                    fullpath = os.path.join(path, entry.name)
                    if entry.is_dir():
                        shutil.rmtree(fullpath)
                    else:
                        os.remove(fullpath)

    apworld_path = os.path.dirname(os.path.dirname(__file__))
    if apworld_path.endswith(".apworld"):
        with open(apworld_path, "rb") as apworld:
            digest = hashlib.file_digest(apworld, "sha256").hexdigest()
        with zipfile.ZipFile(apworld_path, "r") as apworld:
            with apworld.open("albw/archipelago.json", "r") as manifest_file:
                manifest = orjson.loads(manifest_file.read())
            version = manifest["world_version"]
            tmp_path = os.path.join(tempfile.gettempdir(), f"albwrandomizer_{version}")
            lock_path = os.path.join(tmp_path, "lock")
            try:
                if not os.path.exists(tmp_path):
                    os.mkdir(tmp_path)
                while os.path.exists(lock_path):
                    pass
                with open(lock_path, "w") as lockfile:
                    pass
                randomizer_path = os.path.join(tmp_path, "albwrandomizer")
                if not os.path.exists(randomizer_path):
                    os.mkdir(randomizer_path)
                hash_path = os.path.join(randomizer_path, "hash")
                hash_matches = False
                if os.path.exists(hash_path):
                    with open(hash_path, "r") as hashfile:
                        stored_digest = hashfile.read()
                    hash_matches = digest == stored_digest
                if not hash_matches:
                    shutil.rmtree(randomizer_path)
                    os.mkdir(randomizer_path)
                    for info in apworld.infolist():
                        if not info.is_dir() and info.filename.startswith("albw/albwrandomizer/"):
                            info.filename = os.path.basename(info.filename)
                            apworld.extract(info, randomizer_path)
                    with open(hash_path, "w") as hashfile:
                        hashfile.write(digest)
                if os.path.exists(lock_path):
                    os.remove(lock_path)
            except Exception as e:
                print(e)
                if os.path.exists(lock_path):
                    os.remove(lock_path)
            if not tmp_path in sys.path:
                sys.path.append(tmp_path)
    else:
        path = os.path.join(os.path.dirname(__file__), "albwrandomizer")
        if not path in sys.path:
            sys.path.append(path)

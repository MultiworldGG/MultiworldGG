import tarfile
import json
import requests
import os
import shutil
import Utils
from pathlib import Path
import logging
logger = logging.getLogger("SM64 Romhack")

tarpath = "https://api.github.com/repos/DNVIC/sm64hack-archipelago-jsons/tarball"
requestpath = "https://api.github.com/repos/DNVIC/sm64hack-archipelago-jsons/branches/main"
localpath = os.path.join(Utils.user_path(), "sm64hack_jsons", "downloaded_jsons.tar.gz")
tempfolderpath = os.path.join(Utils.user_path(), "sm64hack_jsons", "tempfolder") #should probably use tempfile library for this but cba
folderpath = os.path.join(Utils.user_path(), "sm64hack_jsons", "downloaded_jsons")
jsonpath = os.path.join(Utils.user_path(), "sm64hack_jsons", "last_updated.json")

def strip_members(tar):
    for member in tar.getmembers():
        member.path = os.path.relpath(member.path, Path(member.path).parts[0])
        yield member

def update_jsons():
    last_updated = requests.get(requestpath).json()
    try:
        assert last_updated.get("commit") is not None
        with open(jsonpath, 'r') as jsonfile:
            if json.load(jsonfile)["commit"]["commit"]["author"]["date"] == last_updated["commit"]["commit"]["author"]["date"] and \
                os.path.isdir(folderpath): #incase you delete the folder for some reason itll come back
                return #up to date
    except FileNotFoundError:
        pass #intended behavior
    except AssertionError:
        logger.warning("Could not update JSON list; JSONs used for generation may be outdated. API request returned this: %s", json.dumps(last_updated))
        return
    
    
    response = requests.get(tarpath)
    with open(localpath, 'wb') as file:
        file.write(response.content)
    with tarfile.open(localpath, "r:gz") as tf:
        tf.extractall(path=tempfolderpath, members=strip_members(tf))
    os.remove(localpath)

    returnval = False #need to still delete temporary folder if version file is outdated
    with open(os.path.join(tempfolderpath, "version.txt"), 'r') as versionfile:
        if versionfile.read() != "1.1.0":
            logger.warning("Outdated APWorld version - Please update if you want to use the lastest JSON files")
            returnval = True

    try:
        if(returnval):
            shutil.rmtree(tempfolderpath)
            return
        shutil.rmtree(folderpath)
    except FileNotFoundError: #intended behavior
        if(returnval): #just in case
            return
    os.rename(tempfolderpath, folderpath)

    with open(jsonpath, 'w') as jsonfile:
        json.dump(last_updated, jsonfile)

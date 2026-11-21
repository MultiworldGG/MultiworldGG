import shutil
import tempfile
import urllib.request
from pathlib import Path
from zipfile import ZipFile

import requests

VERSION = "0.14.1"
ASSET_NAME = "Randomizer.Patches.zip"
DESTINATION_ASSEMBLY_PATH = (
    Path(__file__)
    .parent.resolve()
    .joinpath("mars_patcher", "mf", "data", "patches", "mf_u", "asm")
)


release_url = f"https://api.github.com/repos/MetroidAdvRandomizerSystem/mars-fusion-asm/releases/tags/{VERSION}"
print(f"Fetching {release_url}")
response = requests.get(release_url).json()


for asset in response["assets"]:
    if asset["name"] != ASSET_NAME:
        continue

    print("Correct release found, initalizing download")
    with tempfile.TemporaryDirectory() as temp_ref:
        temp_dir = Path(temp_ref)
        temp_file = temp_dir.joinpath("cache.zip")
        urllib.request.urlretrieve(asset["browser_download_url"], temp_file)
        with ZipFile(temp_file, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        for file in list(temp_dir.joinpath("bin").iterdir()):
            print(f"Moving {file.name}")
            shutil.move(file, DESTINATION_ASSEMBLY_PATH.joinpath(file.name))

    break

print("Done.")
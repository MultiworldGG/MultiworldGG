import tempfile, os, subprocess, requests
import logging
from Utils import normalize_tag, tuplize_version, is_windows, is_linux, is_macos

GITHUB_OWNER = "MultiworldGG"
GITHUB_REPO  = "MultiworldGG"
GITHUB_API_LATEST = (
    f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
)

def select_installer_asset(assets: list[dict]) -> dict:
    if is_windows:
        release_assets = [a for a in assets if a["name"].lower().endswith(".exe")]
    elif is_linux: 
        release_assets = [a for a in assets if a["name"].lower().endswith(".appimage")]
    elif is_macos:
        release_assets = [a for a in assets if a["name"].lower().endswith(".dmg")]
    else:   
        raise RuntimeError("This platform is not supported.")

    if not release_assets:
        raise RuntimeError("No feasible installer found in latest release for this platform.")
    
    return release_assets[0]

def get_latest_release_info() -> tuple:
    resp = requests.get(GITHUB_API_LATEST, headers={"Accept":"application/vnd.github.v3+json"})
    resp.raise_for_status()
    data = resp.json()

    tag = normalize_tag(data["tag_name"])
    installer = select_installer_asset(data["assets"])
    download_url = installer["browser_download_url"]
    changelog = data.get("body") or "No changelog available."
    logging.info(f"latest release {tag} under url {download_url}")
    return tuplize_version(tag), download_url, changelog

def download_and_install_win(url: str):
    fd, path = tempfile.mkstemp(suffix=".exe")
    os.close(fd)
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(path, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
    subprocess.Popen([path, "/SILENT", "/SUPPRESSMSGBOXES", "/RESTARTAPPLICATIONS", "/TASKS=deletelib"], shell=False)
    os._exit(0)
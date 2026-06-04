from __future__ import annotations

import fnmatch
import hashlib
import json
import logging
import os
import plistlib
import shlex
import shutil
import stat
import subprocess
import sys
import tempfile
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

import requests

import Utils
from Utils import normalize_tag, tuplize_version


GITHUB_OWNER = "MultiworldGG"
GITHUB_REPO = "MultiworldGG"
ASSET_PATTERNS: dict[str, tuple[str, ...]] = {
    "windows": ("*.exe",),
    "linux": ("*.AppImage",),
    "macos": ("*.dmg",),
}

ProgressCallback = Callable[[int, int], None]


@dataclass(frozen=True)
class UpdateAsset:
    name: str
    download_url: str
    size: int | None = None
    checksum_url: str | None = None
    checksum: str | None = None


@dataclass(frozen=True)
class ReleaseInfo:
    version: Utils.Version
    asset: UpdateAsset
    changelog: str


def _platform_key() -> str:
    if Utils.is_windows:
        return "windows"
    if Utils.is_linux:
        return "linux"
    if Utils.is_macos:
        return "macos"
    raise RuntimeError("This platform is not supported.")


def _asset_matches(name: str, patterns: Sequence[str]) -> bool:
    lowered_name = name.lower()
    return any(fnmatch.fnmatchcase(lowered_name, pattern.lower()) for pattern in patterns)


def select_installer_asset(assets: list[dict], platform_key: str | None = None) -> dict:
    platform_key = platform_key or _platform_key()
    release_assets = [a for a in assets if _asset_matches(str(a.get("name", "")), ASSET_PATTERNS[platform_key])]

    if not release_assets:
        raise RuntimeError(f"No feasible installer found in latest release for {platform_key}.")

    return release_assets[0]


def _select_checksum_asset(assets: list[dict], installer_name: str) -> dict | None:
    checksum_asset_name = f"{installer_name}.sha256".lower()
    for asset in assets:
        name = str(asset.get("name", "")).lower()
        if name == checksum_asset_name:
            return asset
    return None


def _parse_checksum_manifest(text: str, installer_name: str) -> str | None:
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        checksum = line[:64].lower()
        if len(checksum) != 64 or not all(c in "0123456789abcdef" for c in checksum):
            continue
        filename = line[64:].strip()
        if filename.startswith("*"):
            filename = filename[1:].strip()
        if not filename or filename == installer_name or Path(filename).name == installer_name:
            return checksum
    return None


def _get_checksum_for_asset(checksum_asset: dict | None, installer_name: str) -> tuple[str | None, str | None]:
    if not checksum_asset:
        return None, None
    checksum_url = str(checksum_asset.get("browser_download_url") or "")
    if not checksum_url:
        return None, None
    try:
        resp = requests.get(checksum_url, timeout=30)
        resp.raise_for_status()
    except Exception as e:
        logging.warning("Failed to download update checksum manifest: %s", e)
        return checksum_url, None
    return checksum_url, _parse_checksum_manifest(resp.text, installer_name)


def get_latest_release_info() -> ReleaseInfo:
    latest_url = f"https://api.github.com/repos/{GITHUB_OWNER}/{GITHUB_REPO}/releases/latest"
    resp = requests.get(latest_url, headers={"Accept": "application/vnd.github.v3+json"}, timeout=30)
    resp.raise_for_status()
    data = resp.json()

    tag = normalize_tag(data["tag_name"])
    assets = data.get("assets") or []
    installer = select_installer_asset(assets)
    installer_name = str(installer["name"])
    checksum_url, checksum = _get_checksum_for_asset(_select_checksum_asset(assets, installer_name), installer_name)
    asset = UpdateAsset(
        name=installer_name,
        download_url=str(installer["browser_download_url"]),
        size=installer.get("size"),
        checksum_url=checksum_url,
        checksum=checksum,
    )
    changelog = data.get("body") or "No changelog available."
    logging.info("latest release %s under url %s", tag, asset.download_url)
    return ReleaseInfo(tuplize_version(tag), asset, changelog)


def _download_update_asset(asset: UpdateAsset, suffix: str, progress_callback: ProgressCallback | None = None) -> Path:
    fd, raw_path = tempfile.mkstemp(prefix="MultiworldGG-update-", suffix=suffix)
    os.close(fd)
    path = Path(raw_path)
    with requests.get(asset.download_url, stream=True, timeout=30) as r:
        r.raise_for_status()
        total = int(r.headers.get("Content-Length", asset.size or -1))
        downloaded = 0
        with path.open("wb") as f:
            for chunk in r.iter_content(1024 * 256):
                if not chunk:
                    continue
                f.write(chunk)
                downloaded += len(chunk)
                if progress_callback:
                    progress_callback(downloaded, total)
    return path


def _verify_checksum(path: Path, checksum: str | None) -> None:
    if not checksum:
        return
    hasher = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            hasher.update(chunk)
    if hasher.hexdigest().lower() != checksum.lower():
        raise RuntimeError("Downloaded update did not match the published checksum.")


def _write_helper_script(prefix: str, body: str) -> Path:
    fd, raw_path = tempfile.mkstemp(prefix=prefix, suffix=".sh")
    os.close(fd)
    path = Path(raw_path)
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def _render_helper_template(template_name: str, **values: str | int | Path) -> str:
    template_path = Path(Utils.local_path("data", "updater", template_name))
    template = template_path.read_text(encoding="utf-8")
    return template.format(**values)


def _shell_quote(path: str | Path) -> str:
    return shlex.quote(str(path))


def _applescript_string(value: str | Path) -> str:
    return json.dumps(str(value))


def _download_and_install_win(asset: UpdateAsset, progress_callback: ProgressCallback | None = None) -> None:
    path = _download_update_asset(asset, ".exe", progress_callback)
    _verify_checksum(path, asset.checksum)
    subprocess.Popen(
        [str(path), "/SILENT", "/SUPPRESSMSGBOXES", "/RESTARTAPPLICATIONS", "/TASKS=deletelib"],
        shell=False,
    )
    os._exit(0)


def _fallback_open_folder(path: Path) -> None:
    opener = shutil.which("open") if Utils.is_macos else (
        shutil.which("xdg-open") or shutil.which("gnome-open") or shutil.which("kde-open")
    )
    if opener:
        subprocess.Popen([opener, str(path)])


def _download_and_install_appimage(asset: UpdateAsset, progress_callback: ProgressCallback | None = None) -> None:
    current_appimage = os.environ.get("APPIMAGE")
    if not current_appimage:
        raise RuntimeError("Linux auto-update is only available when running from an AppImage.")
    if not _asset_matches(asset.name, ASSET_PATTERNS["linux"]):
        raise RuntimeError(f"Release asset {asset.name!r} does not match the configured AppImage pattern.")

    current_path = Path(current_appimage).resolve()
    target_dir = current_path.parent if os.access(current_path.parent, os.W_OK) else Path.home() / "Downloads"
    target_dir.mkdir(parents=True, exist_ok=True)
    download_path = target_dir / f".{asset.name}.download"

    temp_path = _download_update_asset(asset, ".AppImage", progress_callback)
    _verify_checksum(temp_path, asset.checksum)
    shutil.move(str(temp_path), download_path)
    download_path.chmod(0o755)

    if target_dir != current_path.parent:
        _fallback_open_folder(target_dir)
        raise RuntimeError(f"Downloaded update to {download_path}, but {current_path.parent} is not writable.")

    backup_path = current_path.with_suffix(current_path.suffix + ".old")
    helper = _write_helper_script(
        "MultiworldGG-appimage-update-",
        _render_helper_template(
            "appimage_update.sh.template",
            parent_pid=os.getpid(),
            backup_path=_shell_quote(backup_path),
            current_path=_shell_quote(current_path),
            download_path=_shell_quote(download_path),
        ),
    )
    subprocess.Popen([str(helper)], start_new_session=True)
    os._exit(0)


def _current_macos_bundle() -> Path:
    executable = Path(sys.executable).resolve()
    for parent in (executable, *executable.parents):
        if parent.suffix == ".app" and (parent / "Contents" / "MacOS").is_dir():
            return parent
    raise RuntimeError("Unable to find the current macOS .app bundle.")


def _mounted_volume_from_plist(plist_data: bytes) -> Path:
    data = plistlib.loads(plist_data)
    for entity in data.get("system-entities", []):
        mount_point = entity.get("mount-point")
        if mount_point:
            return Path(mount_point)
    raise RuntimeError("Unable to find mounted DMG volume.")


def _download_and_install_macos(asset: UpdateAsset, progress_callback: ProgressCallback | None = None) -> None:
    app_path = _current_macos_bundle()
    temp_dmg = _download_update_asset(asset, ".dmg", progress_callback)
    _verify_checksum(temp_dmg, asset.checksum)

    attach = subprocess.run(
        ["hdiutil", "attach", "-readonly", "-nobrowse", "-plist", str(temp_dmg)],
        check=True,
        capture_output=True,
    )
    volume = _mounted_volume_from_plist(attach.stdout)
    apps = sorted(volume.glob("*.app"), key=lambda path: path.name != app_path.name)
    if not apps:
        subprocess.run(["hdiutil", "detach", str(volume)], check=False)
        raise RuntimeError("No .app bundle found in downloaded DMG.")
    source_app = apps[0]
    stage_app = Path(str(app_path) + ".update")
    admin_script = (
        f"do shell script \"rm -rf \" & quoted form of {_applescript_string(stage_app)}"
        f" & \" && ditto \" & quoted form of {_applescript_string(source_app)}"
        f" & \" \" & quoted form of {_applescript_string(stage_app)}"
        f" & \" && rm -rf \" & quoted form of {_applescript_string(app_path)}"
        f" & \" && mv \" & quoted form of {_applescript_string(stage_app)}"
        f" & \" \" & quoted form of {_applescript_string(app_path)}"
        " with administrator privileges"
    )

    helper = _write_helper_script(
        "MultiworldGG-macos-update-",
        _render_helper_template(
            "macos_update.sh.template",
            parent_pid=os.getpid(),
            app_path=_shell_quote(app_path),
            source_app=_shell_quote(source_app),
            stage_app=_shell_quote(stage_app),
            volume=_shell_quote(volume),
            dmg_path=_shell_quote(temp_dmg),
            admin_script=_shell_quote(admin_script),
        ),
    )
    subprocess.Popen([str(helper)], start_new_session=True)
    os._exit(0)


def download_and_install_update(
    release_or_asset: ReleaseInfo | UpdateAsset | str,
    progress_callback: ProgressCallback | None = None,
) -> None:
    if isinstance(release_or_asset, ReleaseInfo):
        if release_or_asset.version <= Utils.version_tuple:
            raise RuntimeError("Downloaded release is not newer than the running version.")
        asset = release_or_asset.asset
    elif isinstance(release_or_asset, UpdateAsset):
        asset = release_or_asset
    else:
        asset = UpdateAsset(name=Path(release_or_asset).name, download_url=release_or_asset)

    if Utils.is_windows:
        _download_and_install_win(asset, progress_callback)
    elif Utils.is_linux:
        _download_and_install_appimage(asset, progress_callback)
    elif Utils.is_macos:
        _download_and_install_macos(asset, progress_callback)
    else:
        raise RuntimeError("This platform is not supported.")


def download_and_install_win(url: str, progress_callback: ProgressCallback | None = None) -> None:
    """Compatibility wrapper for existing callers."""
    download_and_install_update(UpdateAsset(name=Path(url).name, download_url=url), progress_callback)

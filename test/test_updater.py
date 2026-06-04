import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import Updater
import Utils


class _Response:
    def __init__(self, json_data=None, text="", headers=None):
        self._json_data = json_data
        self.text = text
        self.headers = headers or {}

    def json(self):
        return self._json_data

    def raise_for_status(self):
        return None


class TestUpdaterAssetSelection(unittest.TestCase):
    assets = [
        {"name": "MultiworldGG_0.7.252_macos.dmg", "browser_download_url": "https://example.invalid/mac"},
        {"name": "MultiworldGG_0.7.252_linux-x86_64.AppImage", "browser_download_url": "https://example.invalid/linux"},
        {"name": "Setup MultiworldGG 0.7.252.exe", "browser_download_url": "https://example.invalid/win"},
    ]

    def test_selects_windows_installer(self):
        asset = Updater.select_installer_asset(self.assets, "windows")
        self.assertEqual(asset["name"], "Setup MultiworldGG 0.7.252.exe")

    def test_selects_linux_appimage(self):
        asset = Updater.select_installer_asset(self.assets, "linux")
        self.assertEqual(asset["name"], "MultiworldGG_0.7.252_linux-x86_64.AppImage")

    def test_selects_macos_dmg(self):
        asset = Updater.select_installer_asset(self.assets, "macos")
        self.assertEqual(asset["name"], "MultiworldGG_0.7.252_macos.dmg")


class TestUpdaterReleaseInfo(unittest.TestCase):
    def test_get_latest_release_info_includes_asset_metadata_and_checksum(self):
        release_json = {
            "tag_name": "v0.7.252",
            "body": "Release notes",
            "assets": [
                {
                    "name": "MultiworldGG_0.7.252_linux-x86_64.AppImage",
                    "browser_download_url": "https://example.invalid/appimage",
                    "size": 1234,
                },
                {
                    "name": "MultiworldGG_0.7.252_linux-x86_64.AppImage.sha256",
                    "browser_download_url": "https://example.invalid/checksum",
                    "size": 64,
                },
            ],
        }
        checksum = "a" * 64

        with patch.object(Updater, "_platform_key", return_value="linux"), \
                patch.object(Updater.requests, "get", side_effect=[
                    _Response(json_data=release_json),
                    _Response(text=f"{checksum}  MultiworldGG_0.7.252_linux-x86_64.AppImage\n"),
                ]):
            release = Updater.get_latest_release_info()

        self.assertEqual(release.version.as_simple_string(), "0.7.252")
        self.assertEqual(release.asset.name, "MultiworldGG_0.7.252_linux-x86_64.AppImage")
        self.assertEqual(release.asset.size, 1234)
        self.assertEqual(release.asset.checksum, checksum)
        self.assertEqual(release.changelog, "Release notes")

    def test_checksum_verification_rejects_bad_hash(self):
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(b"not the expected payload")
            path = Path(f.name)
        self.addCleanup(path.unlink, missing_ok=True)

        with self.assertRaisesRegex(RuntimeError, "checksum"):
            Updater._verify_checksum(path, "0" * 64)

    def test_adjacent_checksum_asset_supports_filenames_with_spaces(self):
        checksum = "b" * 64
        manifest = f"{checksum}  Setup MultiworldGG 0.7.252.exe\n"

        self.assertEqual(
            Updater._parse_checksum_manifest(manifest, "Setup MultiworldGG 0.7.252.exe"),
            checksum,
        )

    def test_install_rejects_non_newer_release_info(self):
        release = Updater.ReleaseInfo(
            version=Utils.version_tuple,
            asset=Updater.UpdateAsset("MultiworldGG.AppImage", "https://example.invalid/appimage"),
            changelog="",
        )

        with self.assertRaisesRegex(RuntimeError, "not newer"):
            Updater.download_and_install_update(release)

    def test_appimage_helper_template_renders_script(self):
        script = Updater._render_helper_template(
            "appimage_update.sh.template",
            parent_pid=123,
            backup_path="'/tmp/current.AppImage.old'",
            current_path="'/tmp/current.AppImage'",
            download_path="'/tmp/new.AppImage.download'",
        )

        self.assertIn("while kill -0 123", script)
        self.assertIn("mv '/tmp/new.AppImage.download' '/tmp/current.AppImage'", script)

    def test_macos_helper_template_renders_script(self):
        script = Updater._render_helper_template(
            "macos_update.sh.template",
            parent_pid=456,
            app_path="'/Applications/MultiworldGG.app'",
            source_app="'/Volumes/MultiworldGG/MultiworldGG.app'",
            stage_app="'/Applications/MultiworldGG.app.update'",
            volume="'/Volumes/MultiworldGG'",
            dmg_path="'/tmp/MultiworldGG.dmg'",
            admin_script="'do shell script'",
        )

        self.assertIn("while kill -0 456", script)
        self.assertIn("osascript -e 'do shell script'", script)


if __name__ == "__main__":
    unittest.main()

import os
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import test  # noqa: F401
import worlds
from worlds import LauncherComponents


class TestLauncherCache(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.enterContext(patch.object(LauncherComponents, "_LAUNCHER_CACHE_PATH",
                                      str(Path(self.temp_dir.name) / "world_launcher_cache.json.gz")))
        self.enterContext(patch.object(LauncherComponents, "components", LauncherComponents.ComponentList()))
        self.enterContext(patch.object(worlds, "world_sources", []))
        self.enterContext(patch.object(worlds, "failed_world_loads", {}))
        self.enterContext(patch.object(worlds, "_worlds_loaded", False))
        self.enterContext(patch.object(worlds, "_worlds_loading", False))
        self.enterContext(patch.object(worlds, "_worlds_load_owner_thread_id", None))
        self.enterContext(patch.object(worlds, "_current_loading_world", None))
        self.enterContext(patch.object(worlds, "_build_network_data_packages"))
        self.enterContext(patch.object(worlds, "__path__", [*worlds.__path__, self.temp_dir.name]))

    def _write_minimal_cache(self, components=()) -> None:
        LauncherComponents._write_cache_payload({
            "schema": LauncherComponents._LAUNCHER_CACHE_SCHEMA,
            "components": [LauncherComponents._serialize_component(component) for component in components],
            "icon_paths": {},
            "world_sources": sorted(world_source.path for world_source in worlds.world_sources),
            "world_source_fingerprints": LauncherComponents._current_world_source_fingerprints(),
        })

    def _add_loose_world(self, name: str, code: str) -> None:
        folder = Path(self.temp_dir.name) / name
        folder.mkdir()
        (folder / "__init__.py").write_text(code, encoding="utf-8")
        worlds.world_sources.append(worlds.WorldSource(str(folder), relative=False))
        self.addCleanup(sys.modules.pop, f"worlds.{name}", None)
        self.addCleanup(worlds.__dict__.pop, name, None)

    def _add_apworld_source(self, name: str) -> worlds.WorldSource:
        path = Path(self.temp_dir.name) / f"{name}.apworld"
        path.write_bytes(b"first")
        source = worlds.WorldSource(str(path), is_zip=True, relative=False)
        worlds.world_sources.append(source)
        return source

    def test_same_path_changed_apworld_invalidates_cache(self) -> None:
        apworld_path = Path(self.temp_dir.name) / "example.apworld"
        apworld_path.write_bytes(b"first")
        worlds.world_sources = [worlds.WorldSource(str(apworld_path), is_zip=True, relative=False)]

        self._write_minimal_cache()
        self.assertIsNotNone(LauncherComponents._load_launcher_cache())

        apworld_path.write_bytes(b"second")
        changed_time = apworld_path.stat().st_mtime_ns + 1_000_000_000
        os.utime(apworld_path, ns=(changed_time, changed_time))

        self.assertIsNone(LauncherComponents._load_launcher_cache())

    def test_previous_schema_is_rejected_even_without_freshness_check(self) -> None:
        self._write_minimal_cache()
        payload = LauncherComponents._load_launcher_cache()
        payload["schema"] = 2
        LauncherComponents._write_cache_payload(payload)

        self.assertIsNone(LauncherComponents._load_launcher_cache())
        self.assertIsNone(LauncherComponents._load_launcher_cache(check_freshness=False))

    def test_cannot_write_cache_before_world_loading_finishes(self) -> None:
        LauncherComponents.write_launcher_cache()

        self.assertFalse(worlds.has_launcher_cache())
        self.assertFalse(Path(LauncherComponents._LAUNCHER_CACHE_PATH).exists())

    def test_failed_import_invalidates_cache_and_keeps_working_clients(self) -> None:
        self._add_loose_world("launcher_cache_healthy", (
            "from worlds.LauncherComponents import Component, components\n"
            "components.append(Component('Healthy Client', script_name='HealthyClient'))\n"
        ))
        self._add_loose_world("launcher_cache_broken", "raise ModuleNotFoundError('unavailable dependency')\n")
        self._write_minimal_cache()

        with self.assertLogs(level="ERROR"):
            worlds.ensure_worlds_loaded()

        self.assertIn("launcher_cache_broken", worlds.failed_world_loads)
        self.assertIn("Healthy Client", [component.display_name for component in LauncherComponents.components])
        self.assertFalse(worlds.has_launcher_cache())
        self.assertFalse(Path(LauncherComponents._LAUNCHER_CACHE_PATH).exists())

        # Explicit rebuilds must not restore a cache of the partial world state either.
        self._write_minimal_cache()
        worlds.rebuild_world_caches()
        self.assertFalse(worlds.has_launcher_cache())

    def test_interrupted_world_loading_invalidates_existing_cache(self) -> None:
        self._write_minimal_cache()
        with patch.object(worlds, "_load_loose_worlds", side_effect=OSError("missing mount")):
            with self.assertRaisesRegex(OSError, "missing mount"):
                worlds.ensure_worlds_loaded()

        self.assertFalse(worlds._worlds_loaded)
        self.assertFalse(worlds.has_launcher_cache())

    def test_successful_world_without_clients_can_be_cached(self) -> None:
        self._add_loose_world("launcher_cache_no_client", "pass\n")

        worlds.ensure_worlds_loaded()

        self.assertTrue(worlds.has_launcher_cache())
        self.assertEqual([], LauncherComponents._load_launcher_cache()["components"])

    def test_old_cache_is_rebuilt_after_successful_loading(self) -> None:
        self._add_loose_world("launcher_cache_rebuild", (
            "from worlds.LauncherComponents import Component, components\n"
            "components.append(Component('Rebuilt Client', script_name='RebuiltClient'))\n"
        ))
        self._write_minimal_cache()
        payload = LauncherComponents._load_launcher_cache()
        payload["schema"] = 2
        LauncherComponents._write_cache_payload(payload)

        worlds.ensure_worlds_loaded()

        payload = LauncherComponents._load_launcher_cache()
        self.assertIsNotNone(payload)
        self.assertEqual(["Rebuilt Client"], [component["display_name"] for component in payload["components"]])

    def test_world_loading_can_still_skip_cache_writes(self) -> None:
        worlds.ensure_worlds_loaded(write_launcher_cache=False)

        self.assertTrue(worlds._worlds_loaded)
        self.assertFalse(Path(LauncherComponents._LAUNCHER_CACHE_PATH).exists())

    def test_install_merge_preserves_complete_cache(self) -> None:
        self._add_apworld_source("existing")
        self._write_minimal_cache([LauncherComponents.Component("Existing Client")])
        installed = self._add_apworld_source("installed")

        LauncherComponents._merge_installed_world_components_into_cache(
            [LauncherComponents.Component("Installed Client")], installed.path)

        payload = LauncherComponents._load_launcher_cache()
        self.assertIsNotNone(payload)
        self.assertEqual(["Existing Client", "Installed Client"],
                         [component["display_name"] for component in payload["components"]])

    def test_install_without_clients_preserves_complete_cache(self) -> None:
        self._add_apworld_source("existing")
        self._write_minimal_cache()
        installed = self._add_apworld_source("installed")

        LauncherComponents._merge_installed_world_components_into_cache([], installed.path)

        self.assertTrue(worlds.has_launcher_cache())

    def test_install_merge_cannot_promote_invalid_cache(self) -> None:
        for invalidity in ("missing", "old_schema", "missing_fingerprints", "changed_source", "removed_source"):
            with self.subTest(invalidity=invalidity):
                worlds.world_sources = []
                existing = self._add_apworld_source("existing")
                self._write_minimal_cache()
                payload = LauncherComponents._load_launcher_cache()
                if invalidity == "missing":
                    Path(LauncherComponents._LAUNCHER_CACHE_PATH).unlink()
                elif invalidity == "old_schema":
                    payload["schema"] = 2
                    LauncherComponents._write_cache_payload(payload)
                elif invalidity == "missing_fingerprints":
                    del payload["world_source_fingerprints"]
                    LauncherComponents._write_cache_payload(payload)
                elif invalidity == "changed_source":
                    Path(existing.path).write_bytes(b"different source contents")
                else:
                    worlds.world_sources.remove(existing)
                installed = self._add_apworld_source("installed")

                LauncherComponents._merge_installed_world_components_into_cache(
                    [LauncherComponents.Component("Installed Client")], installed.path)

                self.assertFalse(worlds.has_launcher_cache())

    def test_old_schema_cache_invalidates_cache(self) -> None:
        apworld_path = Path(self.temp_dir.name) / "example.apworld"
        apworld_path.write_bytes(b"first")
        worlds.world_sources = [worlds.WorldSource(str(apworld_path), is_zip=True, relative=False)]
        LauncherComponents._write_cache_payload({
            "components": [],
            "icon_paths": {},
            "world_sources": sorted(world_source.path for world_source in worlds.world_sources),
        })

        self.assertIsNone(LauncherComponents._load_launcher_cache())

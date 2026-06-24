import os
import tempfile
import unittest
from pathlib import Path

import test  # noqa: F401
import worlds
from worlds import LauncherComponents


class TestLauncherCache(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_cache_path = LauncherComponents._LAUNCHER_CACHE_PATH
        self.original_world_sources = worlds.world_sources
        LauncherComponents._LAUNCHER_CACHE_PATH = str(Path(self.temp_dir.name) / "world_launcher_cache.json.gz")

    def tearDown(self) -> None:
        LauncherComponents._LAUNCHER_CACHE_PATH = self.original_cache_path
        worlds.world_sources = self.original_world_sources
        self.temp_dir.cleanup()

    def _write_minimal_cache(self) -> None:
        LauncherComponents._write_cache_payload({
            "schema": LauncherComponents._LAUNCHER_CACHE_SCHEMA,
            "components": [],
            "icon_paths": {},
            "world_sources": sorted(world_source.path for world_source in worlds.world_sources),
            "world_source_fingerprints": LauncherComponents._current_world_source_fingerprints(),
        })

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

import logging
import os
import subprocess
import sys
import textwrap
import unittest
from copy import deepcopy
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import Utils
from MultiServer import Context, process_client_cmd
from NetUtils import NetworkSlot, SlotType
from apmw.multiserver.gamespackagecache import GamesPackageCache


def make_packages():
    return {
        game: {
            "item_name_to_id": {f"{game} Item": item_id},
            "location_name_to_id": {f"{game} Location": item_id},
            "item_name_groups": {"Everything": [f"{game} Item"]},
            "location_name_groups": {"Everywhere": [f"{game} Location"]},
            "checksum": f"checksum-{game}",
        }
        for game, item_id in (("Archipelago", -1), ("Test Game", 1))
    }


def make_multidata(packages, options=None):
    return {
        "minimum_versions": {"server": Utils.version_tuple},
        "version": Utils.version_tuple,
        "slot_info": {1: NetworkSlot("Player", "Test Game", SlotType.player)},
        "seed_name": "Loading regression",
        "connect_names": {"Player": (0, 1)},
        "locations": {1: {1: (1, 1, 0)}},
        "slot_data": {1: {}},
        "er_hint_data": {},
        "precollected_items": {},
        "precollected_hints": {},
        "datapackage": deepcopy(packages),
        "server_options": options or {},
    }


def run_in_fresh_process(case, source):
    env = dict(os.environ, AP_TEST_WORLDS="apquest", KIVY_NO_ARGS="1")
    result = subprocess.run(
        [sys.executable, "-c", "import test\n" + textwrap.dedent(source)],
        cwd=Path(__file__).resolve().parents[2], env=env,
        capture_output=True, text=True, timeout=60,
    )
    case.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class TestContextLoading(unittest.TestCase):
    def test_existing_positional_options_and_logger(self):
        logger = logging.getLogger("positional-context")
        cache = GamesPackageCache()
        ctx = Context("", 0, "", "", 1, 40, True, "goal", "auto", "own",
                      "disabled", "enabled", 25, 60, 1, True, logger,
                      games_package_cache=cache)
        self.assertEqual((ctx.hint_mode, ctx.countdown_mode, ctx.remaining_mode),
                         ("own", "disabled", "enabled"))
        self.assertEqual((ctx.release_threshold, ctx.auto_shutdown, ctx.compatibility), (25, 60, 1))
        self.assertIs(ctx.logger, logger)
        self.assertIs(ctx.games_package_cache, cache)

    def test_load_populates_blacklists_before_using_embedded_packages(self):
        registry = {}
        fake_worlds = SimpleNamespace(AutoWorldRegister=SimpleNamespace(world_types=registry))

        def load_worlds():
            registry["Test Game"] = SimpleNamespace(hint_blacklist=frozenset({"Test Game Item"}))

        fake_worlds.ensure_worlds_loaded = load_worlds
        packages = make_packages()
        multidata = make_multidata(packages)
        ctx = Context("", 0, "", "", 1, 40, True)
        with patch.dict(sys.modules, worlds=fake_worlds):
            ctx._load(multidata, False)
        self.assertEqual(ctx.non_hintable_names["Test Game"], {"Test Game Item"})
        self.assertEqual(ctx.item_names["Test Game"][-1], "Archipelago Item")
        self.assertEqual(ctx.location_names["Test Game"][-1], "Archipelago Location")
        self.assertEqual(multidata["datapackage"], packages)

    def test_cold_server_load_initializes_worlds_only_when_needed(self):
        run_in_fresh_process(self, '''
            import tempfile
            from pathlib import Path
            from unittest.mock import patch
            from MultiServer import Context
            import worlds
            from worlds import LauncherComponents

            assert not worlds._worlds_loaded
            ctx = Context("", 0, "", "", 1, 40, True)
            assert not worlds._worlds_loaded
            with tempfile.TemporaryDirectory() as folder:
                with patch.object(LauncherComponents, "_LAUNCHER_CACHE_PATH", str(Path(folder) / "cache.gz")):
                    ctx._load_world_data()
                    assert worlds._worlds_loaded
                    assert "APQuest" in ctx.non_hintable_names
                    assert worlds.has_launcher_cache()
        ''')


class TestLegacyDataPackage(unittest.IsolatedAsyncioTestCase):
    async def test_requested_games_and_legacy_exclusions(self):
        ctx = Context("", 0, "", "", 1, 40, True)
        ctx.reduced_games_package = make_packages()
        ctx.send_msgs = AsyncMock()
        client = object()
        for args, expected in (
            ({}, {"Archipelago", "Test Game"}),
            ({"exclusions": ["Test Game"]}, {"Archipelago"}),
            ({"games": ["Test Game"]}, {"Test Game"}),
            ({"games": []}, set()),
            ({"games": ["Test Game"], "exclusions": ["Test Game"]}, {"Test Game"}),
        ):
            with self.subTest(args=args):
                await process_client_cmd(ctx, client, {"cmd": "GetDataPackage", **args})
                self.assertEqual(set(ctx.send_msgs.call_args.args[1][0]["data"]["games"]), expected)

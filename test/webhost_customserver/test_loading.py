import unittest

from test.multiserver.test_loading import run_in_fresh_process


class TestWebHostLoading(unittest.TestCase):
    def test_rooms_share_packages_without_importing_worlds(self):
        run_in_fresh_process(self, '''
            import asyncio
            import importlib.abc
            import logging
            import sys

            class RejectWorlds(importlib.abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname == "worlds" or fullname.startswith("worlds."):
                        raise AssertionError("Room worker imported " + fullname)

            assert "worlds" not in sys.modules
            sys.meta_path.insert(0, RejectWorlds())
            from WebHostLib.customserver import WebHostContext
            from apmw.webhost.customserver.gamespackagecache import DBGamesPackageCache
            from test.multiserver.test_loading import make_packages, make_multidata

            async def check():
                packages = make_packages()
                static = {"games_package": packages,
                          "non_hintable_names": {"Test Game": frozenset({"Test Game Item"})}}
                cache = DBGamesPackageCache(packages)
                contexts = []
                for i in range(2):
                    ctx = WebHostContext(static, cache, logging.getLogger("room"))
                    assert (ctx.release_mode, ctx.collect_mode, ctx.remaining_mode) == ("enabled",) * 3
                    assert (ctx.hint_mode, ctx.countdown_mode, ctx.release_threshold) == ("default", "auto", 0)
                    assert (ctx.auto_shutdown, ctx.compatibility) == (0, 2)
                    data = make_multidata(packages, {"hint_mode": "own", "countdown_mode": "disabled",
                                                    "remaining_mode": "goal", "release_threshold": 25})
                    data["datapackage"] = {game: {"checksum": package["checksum"]}
                                           for game, package in packages.items()}
                    ctx._load(data, True)
                    assert (ctx.hint_mode, ctx.countdown_mode, ctx.remaining_mode, ctx.release_threshold) == (
                        "own", "disabled", "goal", 25)
                    assert ctx.non_hintable_names["Test Game"] == {"Test Game Item"}
                    assert ctx.item_names["Test Game"][-1] == "Archipelago Item"
                    saved = ctx.get_save()
                    saved["game_options"].update(hint_mode="all", countdown_mode="auto", release_threshold=50)
                    ctx.set_save(saved)
                    assert (ctx.hint_mode, ctx.countdown_mode, ctx.release_threshold) == ("all", "auto", 50)
                    contexts.append(ctx)
                assert contexts[0].reduced_games_package["Test Game"] is contexts[1].reduced_games_package["Test Game"]
                assert packages == make_packages()
                assert "worlds" not in sys.modules

            asyncio.run(check())
        ''')

    def test_static_data_loads_registry_before_collecting_blacklists(self):
        run_in_fresh_process(self, '''
            from types import SimpleNamespace
            from unittest.mock import patch
            import sys
            from WebHostLib.customserver import get_static_server_data
            registry = {}
            fake_worlds = SimpleNamespace(AutoWorldRegister=SimpleNamespace(world_types=registry))
            def load_worlds():
                registry["Test Game"] = SimpleNamespace(hint_blacklist=frozenset({"Hidden Item"}))
                fake_worlds.network_data_package = {"games": {}}
            fake_worlds.ensure_worlds_loaded = load_worlds
            with patch.dict(sys.modules, worlds=fake_worlds):
                data = get_static_server_data()
            assert data["non_hintable_names"] == {"Test Game": frozenset({"Hidden Item"})}
        ''')

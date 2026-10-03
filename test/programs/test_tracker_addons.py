import sys
import unittest
from types import ModuleType
from unittest.mock import patch

from test.multiserver.test_loading import run_in_fresh_process


class TestTrackerAddons(unittest.TestCase):
    def test_registration_does_not_require_importable_tracker(self):
        run_in_fresh_process(self, '''
            import importlib.abc
            import sys

            class MissingTracker(importlib.abc.MetaPathFinder):
                def find_spec(self, fullname, path=None, target=None):
                    if fullname == "worlds.tracker" or fullname.startswith("worlds.tracker."):
                        raise ModuleNotFoundError("Tracker archive is not registered yet", name=fullname)

            assert "worlds.tracker" not in sys.modules
            sys.meta_path.insert(0, MissingTracker())
            from worlds import tracker_addons

            assert "next_progression" in tracker_addons.UT_FUNCTIONS
            extension = lambda processor: None
            tracker_addons.register_function("extension", extension)
            assert tracker_addons.UT_FUNCTIONS["extension"] is extension
            assert "worlds.tracker" not in sys.modules
        ''')

    def test_compatibility_is_checked_when_retrieving_commands(self):
        from worlds import tracker_addons

        tracker = ModuleType("worlds.tracker")
        with patch.dict(sys.modules, {"worlds.tracker": tracker}):
            for version in ((0, 3, 0), (0, 3, 1), (0, 3, 4)):
                with self.subTest(version=version):
                    tracker.UT_VERSION_TUPLE = version
                    if version < (0, 3, 1):
                        with self.assertRaisesRegex(ImportError, "missing compatible UT"):
                            tracker_addons.get_functions()
                    else:
                        self.assertIs(tracker_addons.get_functions(), tracker_addons.UT_FUNCTIONS)

    def test_client_checks_compatibility_and_supports_legacy_addons(self):
        run_in_fresh_process(self, '''
            from types import SimpleNamespace
            from unittest.mock import patch
            import worlds
            from worlds import tracker, tracker_addons
            from worlds.tracker.TrackerClient import TrackerCommandProcessor

            ctx = SimpleNamespace(stored_data={})
            for version in ((0, 3, 0), (0, 3, 1), (0, 3, 4)):
                with patch.object(tracker, "UT_VERSION_TUPLE", version), \\
                        patch.object(TrackerCommandProcessor, "commands", {}):
                    processor = TrackerCommandProcessor(ctx)
                    assert ("next_progression" in processor.commands) == (version >= (0, 3, 1))

            legacy_command = lambda processor: "legacy command result"
            legacy_addons = SimpleNamespace(UT_FUNCTIONS={"legacy": legacy_command})
            with patch.object(worlds, "tracker_addons", legacy_addons), \\
                    patch.object(TrackerCommandProcessor, "commands", {}):
                processor = TrackerCommandProcessor(ctx)
                assert processor.commands["legacy"](processor) == "legacy command result"
        ''')

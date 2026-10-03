import unittest

from ..client_tracker_events import BITFLAG_STORAGES


class TrackerEventsTest(unittest.TestCase):
    def test_bitflag_storages_fit_in_32_bits(self):
        for flag_list, _, _, key_suffix in BITFLAG_STORAGES:
            with self.subTest(key_suffix):
                self.assertLessEqual(len(flag_list), 32)

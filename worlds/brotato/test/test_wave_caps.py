import unittest

from ..options import NumWaveCaps
from ..wave_caps import get_wave_cap_info


class TestBrotatoWaveCaps(unittest.TestCase):
    def test_get_wave_cap_info_option_one(self):
        option = NumWaveCaps(1)
        expected_wave_access = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
        }
        num_items, wave_access = get_wave_cap_info(option)
        self.assertEqual(num_items, 0)
        self.assertDictEqual(wave_access, expected_wave_access)

    def test_get_wave_cap_info_option_two(self):
        option = NumWaveCaps(2)
        expected_wave_access = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 1,
            12: 1,
            13: 1,
            14: 1,
            15: 1,
            16: 1,
            17: 1,
            18: 1,
            19: 1,
            20: 1,
        }
        num_items, wave_access = get_wave_cap_info(option)
        self.assertEqual(num_items, 1)
        self.assertDictEqual(wave_access, expected_wave_access)

    def test_get_wave_cap_info_option_four(self):
        option = NumWaveCaps(4)
        expected_wave_access = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 1,
            7: 1,
            8: 1,
            9: 1,
            10: 1,
            11: 2,
            12: 2,
            13: 2,
            14: 2,
            15: 2,
            16: 3,
            17: 3,
            18: 3,
            19: 3,
            20: 3,
        }
        num_items, wave_access = get_wave_cap_info(option)
        self.assertEqual(num_items, 3)
        self.assertDictEqual(wave_access, expected_wave_access)

import unittest

from unittest.mock import patch, MagicMock
from ..client.dolphin_launcher import DolphinLauncher
from ..client.luigismansion_settings import LuigisMansionSettings, EmulatorSettings, EmulatorExecutable


class _TestSettings:
    luigismansion_options: LuigisMansionSettings = LuigisMansionSettings
    luigismansion_options.dolphin_settings = EmulatorSettings


class TestDolphinLauncher(unittest.TestCase):
    @patch('settings.get_settings')
    def test_init_settings_populate(self, mock_settings_get_settings):
        """ Verifies that the DolphinLauncher is able to resolve init args from the AP settings object if no arg is presented. """
        test_settings = _TestSettings()
        test_settings.luigismansion_options.dolphin_settings.path = EmulatorExecutable("this is a test path")
        test_settings.luigismansion_options.dolphin_settings.auto_start = False
        mock_settings_get_settings.return_value = test_settings

        dolphin_launcher = DolphinLauncher()

        self.assertFalse(dolphin_launcher.emulator_settings.auto_start)
        self.assertEqual(test_settings.luigismansion_options.dolphin_settings.path, dolphin_launcher.emulator_settings.path)
        self.assertEqual(1, mock_settings_get_settings.call_count)

    def test_init_override_auto_start_set(self):
        """ Verifies that the DolphinLauncher's init allows consumers to override settings value. """
        lm_settings = LuigisMansionSettings()
        lm_settings.dolphin_settings.auto_start = True
        lm_settings.dolphin_settings.path = EmulatorExecutable("this is a test path")

        dolphin_launcher = DolphinLauncher(lm_settings)

        self.assertTrue(dolphin_launcher.emulator_settings.auto_start)
        self.assertEqual(lm_settings.dolphin_settings.path, dolphin_launcher.emulator_settings.path)

class TestAsyncDolphinLauncher(unittest.IsolatedAsyncioTestCase):
    @patch('subprocess.Popen')
    async def test_launch_dolphin_async_no_process_if_one_exists(self, mock_Popen):
        """ Verifies that _check_emulator_process_open locating a matching process doesn't open a new instance of Dolphin emulator. """
        mock_process_check = MagicMock()
        mock_process_check.return_value = True
        with patch('worlds.luigismansion.client.dolphin_launcher._check_emulator_process_open', mock_process_check):
            lm_settings = LuigisMansionSettings()
            lm_settings.dolphin_settings.auto_start = True
            lm_settings.dolphin_settings.path = EmulatorExecutable("this is a test path")

            dolphin_launcher = DolphinLauncher(lm_settings)
            await dolphin_launcher.launch_dolphin_async("")

            self.assertEqual(0, mock_Popen.call_count)

    @patch('subprocess.Popen')
    async def test_launch_dolphin_async_starts_new_process(self, mock_subprocess_open):
        """ Verifies that when _check_emulator_process_open cannot locate a matching process, a new instance of Dolphin emulator is started. """
        mock_process_check = MagicMock()
        mock_process_check.return_value = False
        with patch('worlds.luigismansion.client.dolphin_launcher._check_emulator_process_open', mock_process_check):
            lm_settings = LuigisMansionSettings()
            lm_settings.dolphin_settings.auto_start = True
            lm_settings.dolphin_settings.path = EmulatorExecutable("this is a test path")

            dolphin_launcher = DolphinLauncher(lm_settings)
            await dolphin_launcher.launch_dolphin_async("")

            arg_list = mock_subprocess_open.call_args.args[0]
            self.assertEqual(1, mock_subprocess_open.call_count)
            self.assertEqual(1, len(arg_list))
            self.assertEqual(lm_settings.dolphin_settings.path, arg_list[0])

    @patch('subprocess.Popen')
    async def test_launch_dolphin_async_with_rom(self, mock_subprocess_open):
        """ Verifies that when a rom path is included when trying to launch Dolphin Emulator, the rom is included in the args. """
        mock_process_check = MagicMock()
        mock_process_check.return_value = False
        with patch('worlds.luigismansion.client.dolphin_launcher._check_emulator_process_open', mock_process_check):
            lm_settings = LuigisMansionSettings()
            lm_settings.dolphin_settings.auto_start = True
            lm_settings.dolphin_settings.path = EmulatorExecutable("this is a test path")

            rom_name = "luigis_mansion.rom"

            dolphin_launcher = DolphinLauncher(lm_settings)
            await dolphin_launcher.launch_dolphin_async(rom_name)

            arg_list = mock_subprocess_open.call_args.args[0]
            self.assertEqual(1, mock_subprocess_open.call_count)
            self.assertEqual(2, len(arg_list))
            self.assertEqual(lm_settings.dolphin_settings.path, arg_list[0])
            self.assertEqual(f"--exec={rom_name}", arg_list[1])

    @patch('subprocess.Popen')
    async def test_launch_dolphin_async_no_auto_start(self, mock_subprocess_open):
        """ Verifies that when auto_start_dolphin is False we don't try and launch the Dolphin emulator. """
        mock_process_check = MagicMock()
        mock_process_check.return_value = False
        with patch('worlds.luigismansion.client.dolphin_launcher._check_emulator_process_open', mock_process_check):
            lm_settings = LuigisMansionSettings()
            lm_settings.dolphin_settings.auto_start = False
            lm_settings.dolphin_settings.path = EmulatorExecutable("this is a test path")

            dolphin_launcher = DolphinLauncher(lm_settings)
            await dolphin_launcher.launch_dolphin_async("")

            self.assertEqual(0, mock_subprocess_open.call_count)
            self.assertEqual(0, mock_process_check.call_count)

import unittest
from unittest.mock import patch

import Utils


class TestRunInTerminal(unittest.TestCase):
    def test_windows_title_uses_instance_name(self):
        with patch.object(Utils, "is_windows", True), \
                patch.object(Utils, "instance_name", "MultiworldGG"), \
                patch.object(Utils.subprocess, "Popen") as popen:
            self.assertTrue(Utils.run_in_terminal(["client.exe", "argument with spaces"]))
            popen.assert_called_once_with(
                ["start", "Running MultiworldGG", "client.exe", "argument with spaces"], shell=True)

    def test_linux_prefers_configured_xdg_terminal(self):
        with patch.object(Utils, "is_windows", False), patch.object(Utils, "is_linux", True), \
                patch.object(Utils, "which", return_value="/usr/bin/xdg-terminal-exec") as which, \
                patch.object(Utils.subprocess, "Popen") as popen:
            self.assertTrue(Utils.run_in_terminal(["client", "argument with spaces"]))
            which.assert_called_once_with("xdg-terminal-exec")
            popen.assert_called_once_with(["/usr/bin/xdg-terminal-exec", "--", "client", "argument with spaces"])

    def test_linux_fallback_preserves_upstream_terminal_arguments(self):
        for terminal, flag in (("gnome-terminal", "--"), ("xterm", "-e")):
            with self.subTest(terminal=terminal), \
                    patch.object(Utils, "is_windows", False), patch.object(Utils, "is_linux", True), \
                    patch.object(Utils, "which", side_effect=lambda name: name if name == terminal else None), \
                    patch.object(Utils.subprocess, "Popen") as popen, \
                    patch.object(Utils, "env_cleared_lib_path", return_value={}), \
                    patch.dict(Utils.os.environ, {}, clear=True):
                self.assertTrue(Utils.run_in_terminal(["client", "argument with spaces"]))
                popen.assert_called_once_with(
                    [terminal, flag, "sh", "-c", "client 'argument with spaces'"], env={})

    def test_missing_terminal_returns_false(self):
        with patch.object(Utils, "is_windows", False), patch.object(Utils, "is_linux", True), \
                patch.object(Utils, "which", return_value=None), \
                patch.object(Utils.subprocess, "Popen") as popen:
            self.assertFalse(Utils.run_in_terminal(["client"]))
            popen.assert_not_called()

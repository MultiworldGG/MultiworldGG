# Tests for Generate.py (MultiworldGGGenerate.exe)

import unittest
import os
import os.path
import sys

from pathlib import Path
from tempfile import TemporaryDirectory

import Generate
import Main


class TestGenerateMain(unittest.TestCase):
    """This tests Generate.py (MultiworldGGGenerate.exe) main"""

    generate_dir = Path(Generate.__file__).parent
    run_dir = generate_dir / "test"  # reproducible cwd that's neither __file__ nor Generate.__file__
    abs_input_dir = Path(__file__).parent / 'data' / 'one_player'
    rel_input_dir = abs_input_dir.relative_to(run_dir)  # directly supplied relative paths are relative to cwd
    yaml_input_dir = abs_input_dir.relative_to(generate_dir)  # yaml paths are relative to user_path

    def assertOutput(self, output_dir: str):
        output_path = Path(output_dir)
        output_files = list(output_path.glob('*.zip'))
        if len(output_files) == 1:
            return True
        self.fail(f"Expected {output_dir} to contain one zip, but has {len(output_files)}: "
                  f"{list(output_path.glob('*'))}")

    def setUp(self):
        self.original_argv = sys.argv.copy()
        self.original_cwd = os.getcwd()
        self.original_local_path = Generate.Utils.local_path.cached_path
        self.original_user_path = Generate.Utils.user_path.cached_path

        # Force both user_path and local_path to a specific path. They have independent caches.
        Generate.Utils.user_path.cached_path = Generate.Utils.local_path.cached_path = str(self.generate_dir)
        os.chdir(self.run_dir)
        self.output_tempdir = TemporaryDirectory(prefix='AP_out_')

    def tearDown(self):
        self.output_tempdir.cleanup()
        os.chdir(self.original_cwd)
        sys.argv = self.original_argv
        Generate.Utils.local_path.cached_path = self.original_local_path
        Generate.Utils.user_path.cached_path = self.original_user_path

    def test_paths(self):
        self.assertTrue(os.path.exists(self.generate_dir))
        self.assertTrue(os.path.exists(self.run_dir))
        self.assertTrue(os.path.exists(self.abs_input_dir))
        self.assertTrue(os.path.exists(self.rel_input_dir))
        self.assertFalse(os.path.exists(self.yaml_input_dir))  # relative to user_path, not cwd

    def test_generate_absolute(self):
        sys.argv = [sys.argv[0], '--seed', '0',
                    '--player_files_path', str(self.abs_input_dir),
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}')
        Main.main(*Generate.main())

        self.assertOutput(self.output_tempdir.name)

    def test_generate_relative(self):
        sys.argv = [sys.argv[0], '--seed', '0',
                    '--player_files_path', str(self.rel_input_dir),
                    '--outputpath', self.output_tempdir.name]
        print(f'Testing Generate.py {sys.argv} in {os.getcwd()}')
        Main.main(*Generate.main())

        self.assertOutput(self.output_tempdir.name)

    def test_generate_yaml(self):
        # override host.yaml
        from settings import get_settings
        from Utils import user_path, local_path
        settings = get_settings()
        # NOTE: until/unless we override settings.Group's setattr, we have to upcast the input dir here
        settings.generator.player_files_path = settings.generator.PlayerFilesPath(self.yaml_input_dir)
        settings.generator.players = 0
        settings._filename = None  # don't write to disk
        user_path_backup = user_path.cached_path
        user_path.cached_path = local_path()  # test yaml is actually in local_path
        try:
            sys.argv = [sys.argv[0], '--seed', '0',
                        '--outputpath', self.output_tempdir.name]
            print(f'Testing Generate.py {sys.argv} in {os.getcwd()}, player_files_path={self.yaml_input_dir}')
            Main.main(*Generate.main())
        finally:
            user_path.cached_path = user_path_backup

        self.assertOutput(self.output_tempdir.name)


class TestGenerateWeights(TestGenerateMain):
    """Tests Generate.py using a weighted file to generate for multiple players."""

    # this test will probably break if something in generation is changed that affects the seed before the weights get processed
    # can be fixed by changing the expected_results dict
    generate_dir = TestGenerateMain.generate_dir
    run_dir = TestGenerateMain.run_dir
    abs_input_dir = Path(__file__).parent / "data" / "weights"
    rel_input_dir = abs_input_dir.relative_to(run_dir)  # directly supplied relative paths are relative to cwd
    yaml_input_dir = abs_input_dir.relative_to(generate_dir)  # yaml paths are relative to user_path

    # don't need to run these tests
    test_generate_absolute = None
    test_generate_relative = None

    def test_generate_yaml(self):
        from settings import get_settings
        from Utils import user_path, local_path
        settings = get_settings()
        settings.generator.player_files_path = settings.generator.PlayerFilesPath(self.yaml_input_dir)
        settings.generator.players = 5  # arbitrary number, should be enough
        settings._filename = None
        user_path_backup = user_path.cached_path
        user_path.cached_path = local_path()
        try:
            sys.argv = [sys.argv[0], "--seed", "1"]
            namespace, seed = Generate.main()
        finally:
            user_path.cached_path = user_path_backup

        # there's likely a better way to do this, but hardcode the results from seed 1 to ensure they're always this
        expected_results = {
            "accessibility": [0, 2, 0, 2, 2],
            "progression_balancing": [0, 50, 99, 0, 50],
        }

        self.assertEqual(seed, 1)
        for option_name, results in expected_results.items():
            for player, result in enumerate(results, 1):
                self.assertEqual(
                    result, getattr(namespace, option_name)[player].value,
                    "Generated results from weights file did not match expected value."
                )

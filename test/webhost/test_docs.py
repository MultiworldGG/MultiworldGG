import json
import os
import pathlib
import unittest

import Utils
from werkzeug.utils import secure_filename

import WebHost
from worlds.AutoWorld import AutoWorldRegister

class TestDocs(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        WebHost.copy_tutorials_files_to_static()

    def test_has_tutorial(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    tutorials = world_type.web.tutorials
                    self.assertGreater(len(tutorials), 0, msg=f"{game_name} has no setup tutorial.")

                    safe_name = secure_filename(game_name)
                    target_path = Utils.local_path("WebHostLib", "static", "generated", "docs", safe_name)
                    for tutorial in tutorials:
                        self.assertTrue(
                            os.path.isfile(Utils.local_path(target_path, secure_filename(tutorial.file_name))),
                            f'{game_name} missing tutorial file {tutorial.file_name}.'
                        )

    def test_has_game_author(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                with self.subTest(game_name):
                    # Check if world has author attribute set (old format)
                    if getattr(world_type, "author", None) is not None:
                        continue

                    # If no author attribute, check for authors in archipelago.json (new format)
                    world_dir = pathlib.Path(world_type.__file__).parent
                    archipelago_json_path = world_dir / "archipelago.json"

                    if archipelago_json_path.exists():
                        with open(archipelago_json_path, "r", encoding="utf-8") as f:
                            data = json.load(f)
                            if "authors" in data and isinstance(data["authors"], list) and len(data["authors"]) > 0:
                                continue

                    self.fail(f'{game_name} missing game author information.')
              
    def test_has_game_info(self):
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden:
                safe_name = secure_filename(game_name)
                target_path = Utils.local_path("WebHostLib", "static", "generated", "docs", safe_name)
                for game_info_lang in world_type.web.game_info_languages:
                    with self.subTest(game_name):
                        self.assertTrue(
                            os.path.isfile(Utils.local_path(target_path, f'{game_info_lang}_{safe_name}.md')),
                            f'{game_name} missing game info file for "{game_info_lang}" language.'
                        )

    def test_legacy_tutorial_links(self):
        """Test that tutorials with legacy link formats can be resolved correctly"""
        for game_name, world_type in AutoWorldRegister.world_types.items():
            if not world_type.hidden and hasattr(world_type.web, 'tutorials'):
                with self.subTest(game_name):
                    for tutorial in world_type.web.tutorials:
                        # Skip tutorials that don't have a proper legacy link format
                        if tutorial.link == "unused" or "/" not in tutorial.link:
                            continue
                        
                        # Test that the legacy link can be parsed correctly
                        link_parts = tutorial.link.split("/")
                        self.assertEqual(len(link_parts), 2, 
                                      f"Legacy link '{tutorial.link}' should be in format 'section/lang'")

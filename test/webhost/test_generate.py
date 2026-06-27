import zipfile
from io import BytesIO

from flask import url_for

from . import TestBase


class TestGenerate(TestBase):
    def test_generate_page_marks_race_mode_for_settings_cache(self) -> None:
        normal_response = self.client.get("/generate")
        self.assertEqual(normal_response.status_code, 200)
        self.assertIn('data-race="0"', normal_response.get_data(as_text=True))

        race_response = self.client.get("/generate/True")
        self.assertEqual(race_response.status_code, 200)
        self.assertIn('data-race="1"', race_response.get_data(as_text=True))

    def test_generate_js_caches_non_sensitive_settings(self) -> None:
        with open("WebHostLib/static/assets/generate.js", encoding="utf-8") as js_file:
            js_content = js_file.read()

        self.assertIn("generate_settings", js_content)
        self.assertIn("generate_race_settings", js_content)
        self.assertIn("readCookie", js_content)
        self.assertIn("saveStoredSettings", js_content)
        self.assertIn("server_password", js_content)
        self.assertIn("file-input", js_content)
        self.assertIn("form.submit()", js_content)

    def test_get_meta_release_threshold(self) -> None:
        from WebHostLib.generate import get_meta

        meta = get_meta({"release_threshold": "37"})
        self.assertEqual(meta["server_options"]["release_threshold"], 37)

    def test_get_meta_release_threshold_clamps_invalid_values(self) -> None:
        from WebHostLib.generate import get_meta

        self.assertEqual(get_meta({"release_threshold": "-5"})["server_options"]["release_threshold"], 0)
        self.assertEqual(get_meta({"release_threshold": "150"})["server_options"]["release_threshold"], 100)
        self.assertEqual(get_meta({"release_threshold": "bad"})["server_options"]["release_threshold"], 0)

    def test_valid_yaml(self) -> None:
        """
        Verify that posting a valid yaml will start generating a game.
        """
        with self.app.app_context(), self.app.test_request_context():
            yaml_data = """
            name: Player1
            game: MultiworldGG
            MultiworldGG: {}
            """
            response = self.client.post(url_for("generate"),
                                        data={"file": (BytesIO(yaml_data.encode("utf-8")), "test.yaml")},
                                        follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertTrue("/seed/" in response.request.path or
                            "/wait/" in response.request.path,
                            f"Response did not properly redirect ({response.request.path})")

    def test_empty_zip(self) -> None:
        """
        Verify that posting an empty zip will give an error.
        """
        with self.app.app_context(), self.app.test_request_context():
            zip_data = BytesIO()
            zipfile.ZipFile(zip_data, "w").close()
            zip_data.seek(0)
            self.assertGreater(len(zip_data.read()), 0)
            zip_data.seek(0)
            response = self.client.post(url_for("generate"),
                                        data={"file": (zip_data, "test.zip")},
                                        follow_redirects=True)
            self.assertIn("user-message", response.text,
                          "Request did not call flash()")
            self.assertIn("not find any valid files", response.text,
                          "Response shows unexpected error")
            self.assertIn("generate-game-form", response.text,
                          "Response did not get user back to the form")

    def test_too_many_players(self) -> None:
        """
        Verify that posting too many players will give an error.
        """
        max_roll = self.app.config["MAX_ROLL"]
        # validate that max roll has a sensible value, otherwise we probably changed how it works
        self.assertIsInstance(max_roll, int)
        self.assertGreater(max_roll, 1)
        self.assertLess(max_roll, 100)
        # create a yaml with max_roll+1 players and watch it fail
        with self.app.app_context(), self.app.test_request_context():
            yaml_data = "---\n".join([
                f"name: Player{n}\n"
                "game: MultiworldGG\n"
                "MultiworldGG: {}\n"
                for n in range(1, max_roll + 2)
            ])
            response = self.client.post(url_for("generate"),
                                        data={"file": (BytesIO(yaml_data.encode("utf-8")), "test.yaml")},
                                        follow_redirects=True)
            self.assertIn("user-message", response.text,
                          "Request did not call flash()")
            self.assertIn("limited to", response.text,
                          "Response shows unexpected error")
            self.assertIn("generate-game-form", response.text,
                          "Response did not get user back to the form")

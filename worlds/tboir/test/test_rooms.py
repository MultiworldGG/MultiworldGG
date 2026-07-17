from .bases import TboiTestBase


OPTIONAL_ROOM_LOCATIONS = (
    "Chapter 1 - Vault",
    "Chapter 1 - Crawl Space",
    "Chapter 1 - Planetarium",
    "Chapter 1 - Ultra Secret Room",
    "Chapter 1 - I AM ERROR",
)


class TestOptionalRoomsDisabled(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "rng_rooms": "none",
        "crawl_space": "none",
        "planetarium": "none",
        "ultra_secret_room": "none",
        "error_room": "none",
    }

    def test_disabled_optional_rooms_do_not_create_locations(self) -> None:
        location_names = self.location_names()
        for location_name in OPTIONAL_ROOM_LOCATIONS:
            with self.subTest(location=location_name):
                self.assertNotIn(location_name, location_names)


class TestOptionalRoomsNoProgression(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "rng_rooms": "no_progression",
        "crawl_space": "no_progression",
        "planetarium": "no_progression",
        "ultra_secret_room": "no_progression",
        "error_room": "no_progression",
    }

    def test_locations_exist_but_reject_progression(self) -> None:
        location_names = self.location_names()
        for location_name in OPTIONAL_ROOM_LOCATIONS:
            with self.subTest(location=location_name):
                self.assertIn(location_name, location_names)
                self.assert_location_accepts_progression(location_name, False)
                self.assert_location_accepts_filler(location_name)


class TestOptionalRoomsAny(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "rng_rooms": "any",
        "crawl_space": "any",
        "planetarium": "any",
        "ultra_secret_room": "any",
        "error_room": "any",
    }

    def test_locations_exist_and_accept_progression(self) -> None:
        location_names = self.location_names()
        for location_name in OPTIONAL_ROOM_LOCATIONS:
            with self.subTest(location=location_name):
                self.assertIn(location_name, location_names)
                self.assert_location_accepts_progression(location_name, True)


class TestShovelCrawlSpaceLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "crawl_space": "any_shovel_logic",
    }

    def test_crawl_space_requires_shovel(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - Crawl Space"],
            [["We Need To Go Deeper! Unlock"]],
            only_check_listed=True,
        )


class TestEhwazCrawlSpaceLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "crawl_space": "any_ehwaz_logic",
    }

    def test_crawl_space_requires_ehwaz(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - Crawl Space"],
            [["Ehwaz Unlock"]],
            only_check_listed=True,
        )


class TestPlanetariumLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "planetarium": "any_telescope_lense_logic",
    }

    def test_planetarium_requires_telescope_lens(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - Planetarium"],
            [["Telescope Lens Unlock"]],
            only_check_listed=True,
        )


class TestRedKeyUltraSecretLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "ultra_secret_room": "any_red_key_logic",
    }

    def test_ultra_secret_room_requires_red_key(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - Ultra Secret Room"],
            [["Red Key Unlock"]],
            only_check_listed=True,
        )


class TestSoulOfCainUltraSecretLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "ultra_secret_room": "any_soul_of_cain_logic",
    }

    def test_ultra_secret_room_requires_soul_of_cain(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - Ultra Secret Room"],
            [["Soul of Cain Unlock"]],
            only_check_listed=True,
        )

class TestCrackedKeyUltraSecretLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "ultra_secret_room": "any_cracked_key_logic",
    }

    def test_ultra_secret_room_requires_cracked_key(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - Ultra Secret Room"],
            [["Cracked Key Unlock"]],
            only_check_listed=True,
        )


class TestUndefinedErrorRoomLogic(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "error_room": "any_undefined_logic",
    }

    def test_error_room_requires_undefined(self) -> None:
        self.assertAccessDependency(
            ["Chapter 1 - I AM ERROR"],
            [["Undefined Unlock"]],
            only_check_listed=True,
        )


class TestChapterFourPlanetariumDisabled(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "planetarium": "any",
        "planetarium_chapter_four": False,
    }

    def test_chapter_four_planetarium_is_absent(self) -> None:
        self.assertNotIn("Chapter 4 - Planetarium", self.location_names())


class TestChapterFourPlanetariumEnabled(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "planetarium": "any",
        "planetarium_chapter_four": True,
    }

    def test_chapter_four_planetarium_is_present(self) -> None:
        self.assertIn("Chapter 4 - Planetarium", self.location_names())

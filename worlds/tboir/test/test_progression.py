from .bases import TboiTestBase


BASE_LOGIC_OPTIONS = {
    "goals": {"Mom"},
    "trapdoor_logic": False,
    "error_room_logic": False,
    "sacrifice_room_logic": False,
    "soul_of_cain_logic": False
}


class TestMainPathDependencies(TboiTestBase):
    options = BASE_LOGIC_OPTIONS

    def test_main_path_dependencies(self) -> None:
        dependencies = {
            "Womb - Boss Room": "Womb Unlock",
            "Cathedral - Boss Room": "Cathedral Unlock",
            "Sheol - Boss Room": "Sheol Unlock",
            "Chest - Boss Room": "The Polaroid Unlock",
            "Dark Room - Boss Room": "The Negative Unlock",
            "Mega Satan - Boss Room": "Key Pieces Unlock",
            "The Void - Boss Room": "Void Portal Unlock",
        }
        for location_name, item_name in dependencies.items():
            with self.subTest(location=location_name):
                self.assertAccessDependency(
                    [location_name],
                    [[item_name]],
                    only_check_listed=True,
                )

        self.assertAccessDependency(
            ["Home - Boss Room"],
            [
                ["Strange Door Unlock", "The Polaroid Unlock"],
                ["Strange Door Unlock", "The Negative Unlock"],
            ],
            only_check_listed=True,
        )

        self.assertAccessDependency(
            ["Corpse - Boss Room"],
            [
                ["Knife Pieces Unlock", "Downpour Unlock", "Mines Unlock"],
                ["Knife Pieces Unlock", "Downpour Unlock", "Ashpit Unlock"],
                ["Knife Pieces Unlock", "Dross Unlock", "Mines Unlock"],
                ["Knife Pieces Unlock", "Dross Unlock", "Ashpit Unlock"],
            ],
            only_check_listed=True,
        )


class TestShovelTrapdoorRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "trapdoor_logic": True,
        "crawl_space": "any_shovel_logic",
    }

    def test_shovel_is_an_alternative_to_native_unlocks(self) -> None:
        for location_name, native_unlock in (
            ("Womb - Boss Room", "Womb Unlock"),
            ("Sheol - Boss Room", "Sheol Unlock"),
        ):
            with self.subTest(location=location_name):
                self.assertAccessDependency(
                    [location_name],
                    [[native_unlock], ["We Need To Go Deeper! Unlock"]],
                    only_check_listed=True,
                )


class TestEhwazTrapdoorRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "trapdoor_logic": True,
        "crawl_space": "any_ehwaz_logic",
    }

    def test_ehwaz_is_an_alternative_to_native_unlocks(self) -> None:
        for location_name, native_unlock in (
            ("Womb - Boss Room", "Womb Unlock"),
            ("Sheol - Boss Room", "Sheol Unlock"),
        ):
            with self.subTest(location=location_name):
                self.assertAccessDependency(
                    [location_name],
                    [[native_unlock], ["Ehwaz Unlock"]],
                    only_check_listed=True,
                )


class TestDisabledEhwazTrapdoorRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "trapdoor_logic": False,
        "crawl_space": "any_ehwaz_logic",
    }

    def test_ehwaz_does_not_skip_unlocks_when_trapdoor_logic_is_off(self) -> None:

        self.collect_all_but(["Womb Unlock", "Sheol Unlock", "Ehwaz Unlock",])

        self.assertFalse(self.can_reach_location("Womb - Boss Room"))
        self.assertFalse(self.can_reach_location("Sheol - Boss Room"))

        self.collect_by_name("Ehwaz Unlock")

        self.assertFalse(self.can_reach_location("Womb - Boss Room"))
        self.assertFalse(self.can_reach_location("Sheol - Boss Room"))


class TestUndefinedErrorRoomRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "error_room_logic": True,
        "error_room": "any_undefined_logic",
        "ultra_secret_room": "no_progression",
    }

    def test_undefined_is_an_alternative_route(self) -> None:
        for location_name, native_unlock in (
            ("Womb - Boss Room", "Womb Unlock"),
            ("Cathedral - Boss Room", "Cathedral Unlock"),
            ("Sheol - Boss Room", "Sheol Unlock"),
            ("Chest - Boss Room", "The Polaroid Unlock"),
            ("Dark Room - Boss Room", "The Negative Unlock"),
        ):
            with self.subTest(location=location_name):
                self.assertAccessDependency(
                    [location_name],
                    [[native_unlock], ["Undefined Unlock"]],
                    only_check_listed=True,
                )


class TestRedKeyErrorRoomRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "error_room_logic": True,
        "error_room": "no_progression",
        "ultra_secret_room": "any_red_key_logic",
    }

    def test_red_key_is_an_alternative_route(self) -> None:
        for location_name, native_unlock in (
            ("Womb - Boss Room", "Womb Unlock"),
            ("Cathedral - Boss Room", "Cathedral Unlock"),
            ("Sheol - Boss Room", "Sheol Unlock"),
            ("Chest - Boss Room", "The Polaroid Unlock"),
            ("Dark Room - Boss Room", "The Negative Unlock"),
        ):
            with self.subTest(location=location_name):
                self.assertAccessDependency(
                    [location_name],
                    [[native_unlock], ["Red Key Unlock"]],
                    only_check_listed=True,
                )


class TestSacrificeRoomRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "sacrifice_room_logic": True,
    }

    def test_sacrifice_room_option_opens_dark_room_without_negative(self) -> None:
        self.assertTrue(
            self.can_reach_location("Dark Room - Boss Room")
        )

class TestSoulOfCainRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "soul_of_cain_logic": True,
        "ultra_secret_room": "any_soul_of_cain_logic"
    }
    
    def test_soul_of_cain_is_an_alternative_to_key_pieces(self) -> None:
        self.assertAccessDependency(
                    ["Mega Satan - Boss Room"],
                    [["Key Pieces Unlock"], ["Soul of Cain Unlock"]],
                    only_check_listed=True,
                )
    
    def test_soul_of_cain_is_an_alternative_to_knife_pieces(self) -> None:
        self.assertAccessDependency(
                    ["Corpse - Boss Room"],
                    [["Knife Pieces Unlock"], ["Soul of Cain Unlock"]],
                    only_check_listed=True,
                )
    
    def test_soul_of_cain_is_an_alternative_to_polaroid_negative(self) -> None:
        self.assertAccessDependency(
                    ["Home - Boss Room"],
                    [["The Polaroid Unlock", "The Negative Unlock"], ["Soul of Cain Unlock"]],
                    only_check_listed=True,
                )
        

class TestDisabledSoulOfCainRoute(TboiTestBase):
    options = {
        **BASE_LOGIC_OPTIONS,
        "soul_of_cain_logic": False,
        "ultra_secret_room": "any_soul_of_cain_logic"
    }
    
    def test_soul_of_cain_is_not_an_alternative_to_key_pieces(self) -> None:
        self.collect_all_but(["Key Pieces Unlock",])

        self.assertFalse(self.can_reach_location("Mega Satan - Boss Room"))

        self.collect_by_name("Soul of Cain Unlock")

        self.assertFalse(self.can_reach_location("Mega Satan - Boss Room"))
    
    def test_soul_of_cain_is_not_an_alternative_to_knife_pieces(self) -> None:
        self.collect_all_but(["Knife Pieces Unlock",])

        self.assertFalse(self.can_reach_location("Corpse - Boss Room"))

        self.collect_by_name("Soul of Cain Unlock")

        self.assertFalse(self.can_reach_location("Corpse - Boss Room"))
    
    def test_soul_of_cain_is_not_an_alternative_to_polaroid_negative(self) -> None:
        self.collect_all_but(["The Polaroid Unlock", "The Negative Unlock",])

        self.assertFalse(self.can_reach_location("Home - Boss Room"))

        self.collect_by_name("Soul of Cain Unlock")

        self.assertFalse(self.can_reach_location("Home - Boss Room"))
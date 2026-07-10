from BaseClasses import PlandoOptions
from Options import OptionError

from ..options import PikuColor
from ..world import PikunikuWorld
from .bases import PikunikuTestBase


def verify_color(text: str) -> PikuColor:
    # verify() is what Generate.py runs on every option; it validates and normalizes
    # the value. The test gen pipeline doesn't run it, so call it directly here.
    option = PikuColor.from_text(text)
    option.verify(PikunikuWorld, "Tester", PlandoOptions.none)
    return option


class TestPikuColorDefault(PikunikuTestBase):
    options = {}

    def test_defaults_to_off(self) -> None:
        self.assertEqual(self.world.options.piku_color, PikuColor.option_off)

    def test_slot_data_is_mode_name(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["piku_color"], "off")


class TestPikuColorRandomPerSeed(PikunikuTestBase):
    options = {
        "piku_color": "random_per_seed",
    }

    def test_slot_data_is_mode_name(self) -> None:
        self.assertEqual(self.world.fill_slot_data()["piku_color"], "random_per_seed")


class TestPikuColorVerification(PikunikuTestBase):
    options = {}

    def test_hex_is_normalized(self) -> None:
        # Lowercase and missing "#" should normalize to a canonical "#RRGGBB".
        self.assertEqual(verify_color("ff0000").value, "#FF0000")
        self.assertEqual(verify_color("#AbCdEf").current_key, "#ABCDEF")

    def test_named_modes_stay_ints(self) -> None:
        for mode in ("off", "random_per_screen", "random_per_seed"):
            self.assertEqual(verify_color(mode).current_key, mode)

    def test_invalid_values_raise(self) -> None:
        for bad in ("not-a-color", "#FFF", "12345", "GGGGGG", "#1234567"):
            with self.subTest(value=bad):
                self.assertRaises(OptionError, verify_color, bad)

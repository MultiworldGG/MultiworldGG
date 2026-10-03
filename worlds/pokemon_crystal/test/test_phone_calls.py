import pkgutil
from unittest import TestCase

import yaml

from ..data import PhoneScriptData
from ..phone_data import POKEMON_REGIONS, line_cmd, poke_cmd, player_cmd, rival_cmd, process_apostrophes, \
    data_to_script, script_line_to_blocks
from ..utils import convert_to_ingame_text


class PhoneCallsTest(TestCase):
    max_phone_trap_bytes = 1024
    max_line_length = 18

    def test_phone_call_characters_mappable(self):
        """Every character in every phone trap script must have an explicit in-game mapping."""
        question_mark_byte = convert_to_ingame_text("?")[0]

        phone_scripts = yaml.safe_load(
            pkgutil.get_data("worlds.pokemon_crystal", "data/phone_data.yaml").decode('utf-8-sig'))

        failures = []
        seen = set()
        for script_name, script_data in phone_scripts.items():
            script = data_to_script(PhoneScriptData(script_name, script_data.get("caller"), script_data.get("script")))

            for line in script.lines:
                for item in line.contents:
                    if not isinstance(item, str):
                        continue
                    for char in item:
                        if (char, script_name) in seen:
                            continue
                        byte = convert_to_ingame_text(char)[0]
                        if byte == question_mark_byte and char != "?":
                            failures.append(f"  '{char}' (U+{ord(char):04X}) in '{script_name}'")
                            seen.add((char, script_name))

        assert not failures, "Characters with no in-game mapping:\n" + "\n".join(failures)

    def test_remote_call_regions_mappable(self):
        """Every character in every remote call region name must have an explicit in-game mapping."""
        question_mark_byte = convert_to_ingame_text("?")[0]

        failures = []
        for game, region in POKEMON_REGIONS.items():
            for item in script_line_to_blocks(line_cmd, region):
                if not isinstance(item, str):
                    continue
                for char in item:
                    if convert_to_ingame_text(char)[0] == question_mark_byte and char != "?":
                        failures.append(f"  '{char}' (U+{ord(char):04X}) in '{game}'")

        assert not failures, "Characters with no in-game mapping:\n" + "\n".join(failures)

    def test_phone_calls(self):
        phone_scripts = yaml.safe_load(
            pkgutil.get_data("worlds.pokemon_crystal", "data/phone_data.yaml").decode('utf-8-sig'))

        for script_name, script_data in phone_scripts.items():
            script = data_to_script(PhoneScriptData(script_name, script_data.get("caller"), script_data.get("script")))

            assert len(script.get_script_bytes()) < self.max_phone_trap_bytes

            for line in script.lines:
                assert sum(
                    [(len(item) - process_apostrophes(item)) if isinstance(item, str) else 4 if item == poke_cmd else 7
                     for item in line.contents[1:]]) <= self.max_line_length, f"{line.contents[1:]} is too long."

from dataclasses import fields
from typing import Any, Iterator
import unittest

from ..game_data import data
from ..items import item_list
from ..locations import location_list
from ..options import (
    AdditionalItemLocationsPerStage,
    ItemWeights,
    JunkWeights,
    TboiOptions,
    TrapWeights,
)


class TestTboirData(unittest.TestCase):
    @staticmethod
    def _iter_rules(rule: dict[str, Any]) -> Iterator[dict[str, Any]]:
        yield rule
        for operator in ("and", "or"):
            for child in rule.get(operator, ()):
                yield from TestTboirData._iter_rules(child)

    run_default_tests = False
    
    def test_generated_item_and_location_names_are_unique(self) -> None:
        items = item_list()
        locations = location_list()

        self.assertEqual(len(items), len(set(items)), "Duplicate generated item name")
        self.assertEqual(
            len(locations),
            len(set(locations)),
            "Duplicate generated location name",
        )

    def test_region_room_connection_and_variant_references_exist(self) -> None:
        regions = set(data["regions"])
        rooms = set(data["rooms"])
        option_names = {field.name for field in fields(TboiOptions)}

        for region_name, region_data in data["regions"].items():
            for room_reference in region_data.get("rooms", ()):
                room_name, *conditions = room_reference.split("&")
                self.assertIn(
                    room_name,
                    rooms,
                    f"{region_name} references unknown room {room_name!r}",
                )
                for condition in conditions:
                    self.assertIn(
                        condition,
                        option_names,
                        f"{region_name}/{room_name} references unknown option {condition!r}",
                    )

            for connection_reference in region_data.get("connects_to", ()):
                target_name, *conditions = connection_reference.split("&")
                self.assertIn(
                    target_name,
                    regions,
                    f"{region_name} connects to unknown region {target_name!r}",
                )
                for condition in conditions:
                    self.assertIn(
                        condition,
                        option_names,
                        f"{region_name}->{target_name} references unknown option {condition!r}",
                    )

            variant_of = region_data.get("variant_of")
            if variant_of:
                self.assertIn(
                    variant_of,
                    regions,
                    f"{region_name} is a variant of unknown region {variant_of!r}",
                )

    def test_rule_references_exist(self) -> None:
        unlocks = set(data["unlocks"])
        regions = set(data["regions"])
        option_names = {field.name for field in fields(TboiOptions)}

        rules: list[tuple[str, dict[str, Any]]] = []
        for room_name, room_data in data["rooms"].items():
            if rule := room_data.get("requires"):
                rules.append((f"room {room_name}", rule))

        for region_name, region_data in data["regions"].items():
            if rule := region_data.get("requires"):
                rules.append((f"region {region_name}", rule))

        for owner, root_rule in rules:
            for rule in self._iter_rules(root_rule):
                if "has" in rule:
                    unlock_name, *conditions = rule["has"].split("&")
                    if unlock_name:
                        self.assertIn(
                            unlock_name,
                            unlocks,
                            f"{owner} references unknown unlock {unlock_name!r}",
                        )
                    for condition in conditions:
                        self.assertIn(
                            condition,
                            option_names,
                            f"{owner} references unknown option {condition!r}",
                        )

                if "hasIfOption" in rule:
                    conditional_rule = rule["hasIfOption"]
                    self.assertIn(
                        conditional_rule["has"],
                        unlocks,
                        f"{owner} references unknown unlock {conditional_rule['has']!r}",
                    )
                    for option_name, _value in conditional_rule["options"]:
                        self.assertIn(
                            option_name,
                            option_names,
                            f"{owner} references unknown option {option_name!r}",
                        )

                if "option" in rule:
                    option_name, _value = rule["option"]
                    self.assertIn(
                        option_name,
                        option_names,
                        f"{owner} references unknown option {option_name!r}",
                    )

                if "reach" in rule:
                    self.assertIn(
                        rule["reach"],
                        regions,
                        f"{owner} references unknown region {rule['reach']!r}",
                    )

    def test_boss_references_and_rewards_exist(self) -> None:
        referenced_bosses = {
            region_data["boss"]
            for region_data in data["regions"].values()
            if "boss" in region_data
        }

        self.assertEqual(referenced_bosses, set(data["boss_rewards"]))
        for boss_name, reward_data in data["boss_rewards"].items():
            reward_count = reward_data["amount"]
            self.assertIsInstance(reward_count, int, boss_name)
            self.assertGreater(reward_count, 0, boss_name)

    def test_weight_options_only_reference_real_items(self) -> None:
        items = set(data["items"])
        for option_type in (ItemWeights, JunkWeights, TrapWeights):
            with self.subTest(option=option_type.__name__):
                self.assertLessEqual(set(option_type.valid_keys), items)

    def test_additional_location_stages_reference_real_regions(self) -> None:
        self.assertLessEqual(
            set(AdditionalItemLocationsPerStage.valid_keys),
            set(data["regions"]),
        )

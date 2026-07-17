from .bases import TboiTestBase
from ..game_data import data


AREA_OPTION_TO_TYPE = {
    "Alt Path": "alt",
    "The Void": "void",
    "Ascend": "ascend",
    "Timed Areas": "timed",
}


class TestExcludedAreas(TboiTestBase):
    options = {
        "goals": {"Mother", "Delirium", "Beast", "Boss Rush"},
        "excluded_areas": set(AREA_OPTION_TO_TYPE.keys()),
    }

    def test_excluded_area_regions_unlocks_and_goals_are_removed(self) -> None:
        region_names = self.region_names()
        item_names = self.item_names()
        excluded_types = set(AREA_OPTION_TO_TYPE.values())

        for region_name, region_data in data["regions"].items():
            if region_data.get("type") in excluded_types:
                with self.subTest(region=region_name):
                    self.assertNotIn(region_name, region_names)

        for unlock_name, unlock_data in data["unlocks"].items():
            unlock_types = set(unlock_data.get("type", ()))
            if unlock_types & excluded_types:
                with self.subTest(item=unlock_name):
                    self.assertNotIn(f"{unlock_name} Unlock", item_names)

        self.assertEqual(self.world.goals, ["Mom"])
        location_names = self.location_names()
        for excluded_goal in ("Mother", "Delirium", "Beast", "Boss Rush"):
            with self.subTest(goal=excluded_goal):
                self.assertNotIn(f"Defeat {excluded_goal}", location_names)
        self.assertIn("Defeat Mom", location_names)


class TestFloorVariationsDisabled(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "floor_variations": False,
    }

    def test_variants_and_variant_unlocks_are_removed(self) -> None:
        region_names = self.region_names()
        item_names = self.item_names()

        for region_name, region_data in data["regions"].items():
            if region_data.get("variant_of"):
                with self.subTest(region=region_name):
                    self.assertNotIn(region_name, region_names)
                    if region_name in data["unlocks"]:
                        self.assertNotIn(f"{region_name} Unlock", item_names)
                    self.assertIn(region_data["variant_of"], region_names)


class TestAdditionalLocationsPerStage(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "additional_item_locations_per_stage": {
            "Basement": 3,
            "Caves": 1,
        },
    }

    def test_exact_numbered_location_counts(self) -> None:
        location_names = self.location_names()

        for index in range(1, 4):
            self.assertIn(f"Basement - Item #{index}", location_names)
        self.assertNotIn("Basement - Item #4", location_names)

        self.assertIn("Caves - Item #1", location_names)
        self.assertNotIn("Caves - Item #2", location_names)

        self.assertNotIn("Depths - Item #1", location_names)


class TestBossRewardsDisabled(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "additional_boss_rewards": False,
    }

    def test_boss_rewards_are_removed_but_goal_event_remains(self) -> None:
        location_names = self.location_names()
        self.assertNotIn("Mom Reward #1", location_names)
        self.assertIn("Defeat Mom", location_names)


class TestBossRewardsEnabled(TboiTestBase):
    options = {
        "goals": {"Mom"},
        "additional_boss_rewards": True,
    }

    def test_configured_boss_reward_counts_are_created(self) -> None:
        location_names = self.location_names()
        for boss_name in ("Mom", "Delirium"):
            reward_count = data["boss_rewards"][boss_name]["amount"]
            for index in range(1, reward_count + 1):
                with self.subTest(boss=boss_name, reward=index):
                    self.assertIn(
                        f"{boss_name} Reward #{index}",
                        location_names,
                    )
            self.assertNotIn(
                f"{boss_name} Reward #{reward_count + 1}",
                location_names,
            )

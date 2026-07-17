from collections import Counter

from .bases import TboiTestBase
from ..game_data import data


THREE_GOALS = {"Mom", "Isaac", "Satan"}


class TestExplicitGoals(TboiTestBase):
    options = {"goals": THREE_GOALS}

    def test_explicit_goals_are_created_once(self) -> None:
        self.assertEqual(set(self.world.goals), THREE_GOALS)
        self.assertEqual(len(self.world.goals), len(THREE_GOALS))
        for goal in THREE_GOALS:
            self.assertIn(f"Defeat {goal}", self.location_names())


class TestRandomGoals(TboiTestBase):
    options = {"goals": {"Random-3"}}

    def test_random_goals_are_distinct_and_valid(self) -> None:
        base_goals = [goal.split("|", 1)[0] for goal in self.world.goals]
        self.assertEqual(len(base_goals), 3)
        self.assertEqual(len(base_goals), len(set(base_goals)))
        self.assertLessEqual(set(base_goals), set(data["boss_rewards"]))


class TestExplicitAndRandomGoals(TboiTestBase):
    options = {"goals": {"Mom", "Random-3"}}

    def test_random_selection_does_not_duplicate_explicit_goal(self) -> None:
        base_goals = [goal.split("|", 1)[0] for goal in self.world.goals]
        self.assertEqual(len(base_goals), 4)
        self.assertEqual(len(base_goals), len(set(base_goals)))
        self.assertIn("Mom", base_goals)


class TestAllGoals(TboiTestBase):
    options = {"goals": {"All"}}

    def test_all_selects_every_available_boss(self) -> None:
        self.assertEqual(
            {goal.split("|", 1)[0] for goal in self.world.goals},
            set(data["boss_rewards"]),
        )


class TestGoalAmountTwo(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "goal_amount": 2,
    }

    def test_exactly_two_victory_conditions_are_required(self) -> None:
        self.multiworld.state.collect(self.world.create_event("Victory Condition"), True)
        self.assertFalse(self.multiworld.completion_condition[self.player](self.multiworld.state))

        self.multiworld.state.collect(self.world.create_event("Victory Condition"), True)
        self.assertTrue(self.multiworld.completion_condition[self.player](self.multiworld.state))


class TestGoalAmountZero(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "goal_amount": 0,
    }

    def test_zero_requires_all_selected_goals(self) -> None:
        for _ in range(len(THREE_GOALS) - 1):
            self.multiworld.state.collect(self.world.create_event("Victory Condition"), True)
        self.assertFalse(self.multiworld.completion_condition[self.player](self.multiworld.state))

        self.multiworld.state.collect(self.world.create_event("Victory Condition"), True)
        self.assertTrue(self.multiworld.completion_condition[self.player](self.multiworld.state))


class TestGoalAmountAboveGoalCount(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "goal_amount": 12,
    }

    def test_amount_above_goal_count_is_capped_to_all(self) -> None:
        for _ in range(len(THREE_GOALS) - 1):
            self.multiworld.state.collect(self.world.create_event("Victory Condition"), True)
        self.assertFalse(self.multiworld.completion_condition[self.player](self.multiworld.state))

        self.multiworld.state.collect(self.world.create_event("Victory Condition"), True)
        self.assertTrue(self.multiworld.completion_condition[self.player](self.multiworld.state))


class TestSingleCharacterGoals(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "character_goals": "single",
        "exclude_characters": {"Isaac", "Tainted"},
    }

    def test_each_goal_gets_one_allowed_character(self) -> None:
        for encoded_goal in self.world.goals:
            parts = encoded_goal.split("|")
            self.assertEqual(len(parts), 2)
            character = parts[1]
            self.assertNotEqual(character, "Isaac")
            self.assertFalse(character.startswith("Tainted "))
            self.assertIn(character, data["characters"])


class TestGroupedCharacterGoals(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "character_goals": "grouped",
        "exclude_characters": {"Isaac", "Tainted Isaac"},
    }

    def test_grouped_mode_assigns_every_allowed_character_once(self) -> None:
        assigned_characters = [
            character
            for encoded_goal in self.world.goals
            for character in encoded_goal.split("|")[1:]
        ]
        expected_characters = set(data["characters"]) - {"Isaac", "Tainted Isaac"}

        self.assertEqual(set(assigned_characters), expected_characters)
        self.assertEqual(
            Counter(assigned_characters),
            Counter(expected_characters),
        )
        self.assertTrue(
            all(len(encoded_goal.split("|")) > 1 for encoded_goal in self.world.goals)
        )


class TestOnlyTaintedCharacterGoals(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "character_goals": "single",
        "exclude_characters": {"Non-Tainted"},
    }

    def test_non_tainted_filter_leaves_only_tainted_characters(self) -> None:
        assigned = [goal.split("|")[1] for goal in self.world.goals]
        self.assertTrue(all(character.startswith("Tainted ") for character in assigned))


class TestOnlyNonTaintedCharacterGoals(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "character_goals": "single",
        "exclude_characters": {"Tainted"},
    }

    def test_tainted_filter_leaves_only_non_tainted_characters(self) -> None:
        assigned = [goal.split("|")[1] for goal in self.world.goals]
        self.assertTrue(all(not character.startswith("Tainted ") for character in assigned))


class TestCharacterFallback(TboiTestBase):
    options = {
        "goals": THREE_GOALS,
        "character_goals": "single",
        "exclude_characters": set(data["characters"]),
    }

    def test_empty_character_pool_falls_back_to_isaac(self) -> None:
        assigned = [goal.split("|")[1] for goal in self.world.goals]
        self.assertEqual(assigned, ["Isaac"] * len(THREE_GOALS))

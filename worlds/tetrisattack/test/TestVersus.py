from worlds.tetrisattack import VersusGoal
from worlds.tetrisattack.Options import StarterPack, PuzzleGoal, VersusMode
from worlds.tetrisattack.test import TetrisAttackTestBase


class TestVersusMinimumDifficulty(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_no_puzzle,
        "versus_goal": VersusGoal.option_very_hard,
        "starter_pack": StarterPack.option_vs_two_stages,
        "versus_mode": VersusMode.option_minimum_difficulty
    }


class TestVersusMinimumProgressive(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_no_puzzle,
        "versus_goal": VersusGoal.option_very_hard,
        "starter_pack": StarterPack.option_vs_two_stages,
        "versus_mode": VersusMode.option_minimum_progressive
    }


class TestVersusGoalDifficulty(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_no_puzzle,
        "versus_goal": VersusGoal.option_very_hard,
        "starter_pack": StarterPack.option_vs_two_stages,
        "versus_mode": VersusMode.option_goal_difficulty
    }


class TestVersusEasyProgressive(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_no_puzzle,
        "versus_goal": VersusGoal.option_easy,
        "starter_pack": StarterPack.option_vs_two_stages
    }


class TestVersusEasyBowser(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": False,
        "puzzle_goal": PuzzleGoal.option_no_puzzle,
        "versus_goal": VersusGoal.option_easy,
        "starter_pack": StarterPack.option_vs_two_stages,
        "versus_mode": VersusMode.option_goal_difficulty,
        "versus_easy_bowser": True
    }

    def test_stage_12(self) -> None:
        locations = ["LAST STAGE - Bowser!!!!"]
        items = [["Vs. Last Stage Unlock",
                  "Mt. Wickedness Gate"]]
        self.assertAccessDependency(locations, items, only_check_listed=True)

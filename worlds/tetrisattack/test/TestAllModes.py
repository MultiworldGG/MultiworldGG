from worlds.tetrisattack import PuzzleGoal, VersusGoal, StarterPack
from worlds.tetrisattack.test import TetrisAttackTestBase

class TestAllModes(TetrisAttackTestBase):
    options = {
        "stage_clear_goal": True,
        "puzzle_goal": PuzzleGoal.option_puzzle_and_extra_puzzle,
        "versus_goal": VersusGoal.option_no_vs,
        "versus_inclusion": True,
        "starter_pack": StarterPack.option_puzzle_level_1,  # TODO: Make test able to pass with other starter packs
        "special_stage_trap_count": 30,
        "shock_panel_checks": 100,
    }

    def test_unique_ids(self) -> None:
        for name in self.world.item_name_to_id:
            item_id = self.world.item_name_to_id[name]
            compare_name = self.world.item_id_to_name[item_id]
            assert compare_name == name, f"Item ID {item_id} has two conflicting names {name} and {compare_name}"
        for name in self.world.location_name_to_id:
            location_id = self.world.location_name_to_id[name]
            compare_name = self.world.location_id_to_name[location_id]
            assert compare_name == name, f"Location ID {location_id} has two conflicting names {name} and {compare_name}"

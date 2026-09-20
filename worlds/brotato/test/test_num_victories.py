from ..constants import BASE_GAME_CHARACTERS
from . import BrotatoTestBase


class TestBrotatoNumVictoriesOption(BrotatoTestBase):
    """Test edge cases related to the num_victories option."""

    def test_num_wins_needed_clamped_to_number_of_characters(self):
        """Test that the number of victories is not more than the number of included characters.

        This prevents unwinnable situations where there aren't enough characters to reach the goal with.

        We also check the output slot data to make sure the change, if made, propagates to it as well.
        """
        expected_final_num_victories_value = 10  # Arbitrary value that's less than the number of characters
        include_characters = BASE_GAME_CHARACTERS.characters[:10]
        num_victories_option_value = 25

        options = {
            "num_victories": num_victories_option_value,
            "include_base_game_characters": include_characters,
            "num_characters": expected_final_num_victories_value,
        }

        with self._run(options):
            generated_num_victories_value = self.world.num_wins_needed
            # Checking slot data here so we don't need to duplicate the test setup in multiple functions/files.
            slot_data_num_victories = self.world.fill_slot_data()["num_wins_needed"]

            self.assertEqual(expected_final_num_victories_value, generated_num_victories_value)
            self.assertEqual(expected_final_num_victories_value, slot_data_num_victories)

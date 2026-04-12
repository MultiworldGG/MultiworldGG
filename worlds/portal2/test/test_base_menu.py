from worlds.AutoWorld import call_all

from .bases import Portal2TestBase
from ..Options import GameModeOption
from ..mod_helpers.MapMenu import Menu
from ..Locations import all_locations_table

class FakeClient:
    item_list: list[str] = []
    location_id_to_name: dict[int, str] = {data.id: name for name, data in all_locations_table.items()}


class BaseMenuTests(Portal2TestBase):
    options = {
        "game_mode": GameModeOption.NORMAL
    }
    
    def setUp(self):
        super().setUp()
        self.client = FakeClient()
    
    def test_menu_generation(self) -> None:
        from Fill import distribute_items_restrictive
        
        with self.subTest("Game", game=self.game, seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
        
        slot_data = self.world.fill_slot_data()
        
        menu = Menu(slot_data["chapter_dict"], self.client, is_open_world=slot_data["game_mode"] == GameModeOption.OPEN_WORLD, logic_difficulty=slot_data["logic_difficulty"], wheatley_monitors=slot_data["wheatley_monitors"], ratman_dens=slot_data["ratman_dens"])
        menu.generate_menu()
        # Check menu is generated where the first map of each chapter says "command" and the rest say "command_deactivated"
        menu_string = str(menu)
        print(menu_string)
        self.assertGreater(menu_string.count('"command_deactivated"'), 0)
        self.assertEqual(menu_string.count('"command"'), 18)
    
    def test_menu_no_maps(self) -> None:
        menu = Menu({1: [], 2: [], 3: []}, self.client)
        menu.generate_menu()
        menu_string = str(menu)
        print(menu_string)
        # Check menu is generated where the first map of each chapter says "No Maps In This Chapter"
        self.assertEqual(menu_string.count("No Maps In This Chapter"), 3)
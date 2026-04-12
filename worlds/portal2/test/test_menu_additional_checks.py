from worlds.AutoWorld import call_all

from .test_base_menu import FakeClient
from .bases import Portal2TestBase
from ..Options import GameModeOption
from ..mod_helpers.MapMenu import Menu
from ..ItemNames import portal_gun_1, portal_gun_2, potatos
from ..mod_helpers.MapMenu import indicator_characters

class AdditionalChecksMenuTests(Portal2TestBase):
    options = {
        "game_mode": GameModeOption.NORMAL,
        "wheatley_monitors": True,
        "ratman_dens": True,
        "cutscene_levels": True,
    }
    
    def setUp(self):
        super().setUp()
        self.client = FakeClient()
    
    def test_title_generation(self) -> None:
        from Fill import distribute_items_restrictive
        
        with self.subTest("Game", game=self.game, seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
        
        slot_data = self.world.fill_slot_data()
        
        menu = Menu(slot_data["chapter_dict"], self.client, is_open_world=slot_data["game_mode"] == GameModeOption.OPEN_WORLD, logic_difficulty=slot_data["logic_difficulty"], wheatley_monitors=slot_data["wheatley_monitors"], ratman_dens=slot_data["ratman_dens"])
        menu.generate_menu()
        menu_string = str(menu)
        # Find map that includes Wheatley Monitors in the title and check it is correct
        self.assertTrue(f"M{indicator_characters["wheatley"]}{indicator_characters["wheatley"]}-Funnel Catch" in menu_string)
        self.assertTrue(f"M{indicator_characters["wheatley"]}--Laser Platform" in menu_string)
        self.assertTrue("MR--Laser Stairs" in menu_string)
        self.assertTrue("M---" in menu_string)
        self.assertTrue(f"M{indicator_characters[portal_gun_1]}--Portal Gun" in menu_string)
        self.assertTrue(f"M{indicator_characters[portal_gun_2]}--Incinerator" in menu_string)
        self.assertTrue(f"M{indicator_characters[potatos]}--PotatOS" in menu_string)
        
    def test_sub_location_completion(self) -> None:
        from Fill import distribute_items_restrictive
        
        with self.subTest("Game", game=self.game, seed=self.multiworld.seed):
            distribute_items_restrictive(self.multiworld)
            call_all(self.multiworld, "post_fill")
        
        slot_data = self.world.fill_slot_data()
        
        menu = Menu(slot_data["chapter_dict"], self.client, is_open_world=slot_data["game_mode"] == GameModeOption.OPEN_WORLD, logic_difficulty=slot_data["logic_difficulty"], wheatley_monitors=slot_data["wheatley_monitors"], ratman_dens=slot_data["ratman_dens"])
        menu.generate_menu()
        # Complete a map with a sub location and check the title updates
        menu.complete_map(slot_data["location_name_to_id"]["Portal Gun Completion"])
        menu_string = str(menu)
        self.assertTrue(f"✓{indicator_characters[portal_gun_1]}--Portal Gun" in menu_string)
        menu.complete_sub_location_check(portal_gun_1)
        menu_string = str(menu)
        self.assertTrue("✓✓--Portal Gun" in menu_string)
        
        
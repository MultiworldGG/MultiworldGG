from .bases import Portal2TestBase
from ..Options import GameModeOption
from ..ItemNames import portal_gun_2, potatos

class ItemChecks(Portal2TestBase):
    options = {
        "game_mode": GameModeOption.NORMAL,
    }
    
    def test_portal_gun_items_in_place(self) -> None:
        """Testing if when Upgraded Portal Gun and PotatOS are in their places they are also put into slot data"""
        self.world.get_location(portal_gun_2).item = self.world.create_item(portal_gun_2)
        self.world.get_location(potatos).item = self.world.create_item(potatos)
        
        slot_data = self.world.fill_slot_data()
        
        self.assertTrue("portal_gun_upgrade_inplace" in slot_data)
        self.assertTrue(slot_data["portal_gun_upgrade_inplace"] == True)
        self.assertTrue("potatos_inplace" in slot_data)
        self.assertTrue(slot_data["potatos_inplace"] == True)

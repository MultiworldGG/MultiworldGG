from BaseClasses import Location, Region

from .constants import GAME_NAME


class LegoStarWarsTCSLocation(Location):
    game = GAME_NAME


class LegoStarWarsTCSShopLocation(LegoStarWarsTCSLocation):
    studs_cost: int

    def __init__(self, player: int, name: str, address: int, parent: Region, studs_cost: int):
        super().__init__(player, name, address, parent)
        self.studs_cost = studs_cost

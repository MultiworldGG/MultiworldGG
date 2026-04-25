import math

from BaseClasses import ItemClassification, Region
from rule_builder.rules import CanReachRegion, Has
from worlds.AutoWorld import World

from .items import ITEM_NAME_TO_ID, TwoThousandAndFortyEightItem
from .locations import LOCATION_NAME_TO_ID, SCORE_THRESHOLDS, TwoThousandAndFortyEightLocation
from .web_world import TwoThousandAndFortyEightWebWorld


class TwoThousandAndFortyEightWorld(World):
    """
    2048 is a single-player sliding tile puzzle video game. The objective of the game is 
    to slide numbered tiles on a grid to combine them to create a tile with the number 2048.
    """
    game = "2048"
    web = TwoThousandAndFortyEightWebWorld()
    item_name_to_id = ITEM_NAME_TO_ID
    location_name_to_id = LOCATION_NAME_TO_ID

    def create_regions(self) -> None:
        region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions.append(region)
        score_50 = TwoThousandAndFortyEightLocation(self.player, "Reach 50 Points", 50, region)
        self.set_rule(score_50, Has("Merge 2s"))
        region.locations.append(score_50)
        score_100 = TwoThousandAndFortyEightLocation(self.player, "Reach 100 Points", 100, region)
        self.set_rule(score_100, Has("Merge 2s") & Has("Merge 4s"))
        region.locations.append(score_100)
        score_200 = TwoThousandAndFortyEightLocation(self.player, "Reach 200 Points", 200, region)
        self.set_rule(score_200, Has("Merge 2s") & Has("Merge 4s") & Has("Merge 8s"))
        region.locations.append(score_200)

        region_to_score = {
            16: 400,
            32: 800,
            64: 1500,
            128: 3000,
            256: 5000,
            512: 7500,
            1024: 10000,
            2048: 14000,
        }

        i = 1
        while i < 2048:
            i *= 2
            if i > 4:
                new_region = Region(str(i), self.player, self.multiworld)
                self.multiworld.regions.append(new_region)
                access_rule = Has(f"Merge {i // 2}s")
                if i == 16:
                    access_rule &= Has("Merge 2s")  # To not clog the board
                entrance = region.connect(new_region)
                self.set_rule(entrance, access_rule)
                region = new_region
            location = TwoThousandAndFortyEightLocation(self.player, f"Have a {i}", i, region)
            region.locations.append(location)

            if i in region_to_score:
                score = region_to_score[i]
                location = TwoThousandAndFortyEightLocation(self.player, f"Reach {score} Points", score, region)
                region.locations.append(location)

        self.set_completion_rule(CanReachRegion("2048"))

    def create_item(self, name: str) -> TwoThousandAndFortyEightItem:
        item_id = self.item_name_to_id[name]
        if math.log2(item_id).is_integer():
            classification = ItemClassification.progression
        elif "trap" in name:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        return TwoThousandAndFortyEightItem(name, classification, item_id, self.player)

    def create_items(self) -> None:
        i = 2
        while i < 2048:
            self.multiworld.itempool.append(self.create_item(f"Merge {i}s"))
            i *= 2

        for _ in range(len(SCORE_THRESHOLDS) + 1):
            self.multiworld.itempool.append(self.create_item(self.get_filler_item_name()))

    def get_filler_item_name(self) -> str:
        r = self.random.random()
        if r < 0.1:
            return f"{self.random.randint(66, 70)} trap"
        if r < 0.15:
            return "Shuffle Trap"
        if r < 0.65:
            return "Progressive Luck"

        return f"Merge {self.random.randint(419, 421)}s"

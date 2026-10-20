# from PMR: https://github.com/icebound777/PMR-SeedGenerator/blob/main/models/options/MysteryOptionSet.py
from .ItemList import item_table


# original items are, in order:
# mushroom, super shroom, fire flower, stone cap, dizzy dial, thunder rage, pebble
class MysteryOptions:
    def __init__(self):
        self.mystery_random_choice = 0
        self.mystery_random_pick = False
        self.mystery_itemA = 138
        self.mystery_itemB = 140
        self.mystery_itemC = 128
        self.mystery_itemD = 136
        self.mystery_itemE = 154
        self.mystery_itemF = 130
        self.mystery_itemG = 133

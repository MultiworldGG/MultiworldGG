from .itemInfo import ItemInfo
from .constants import *


class TunicFairy(ItemInfo):

    def __init__(self, index):
        self.index = index
        super().__init__(0x301)
        self.patch_room = self.room + index*3
        
    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x3e][0x3800 + self.patch_room] = CHEST_ITEMS[option]
        if multiworld:
            rom.banks[0x3e][0x3300 + self.patch_room] = multiworld

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.index)

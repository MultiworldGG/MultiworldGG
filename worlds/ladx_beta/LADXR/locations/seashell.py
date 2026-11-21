from .itemInfo import ItemInfo
from .droppedKey import DroppedKey
from .constants import *
from .items import *


class Seashell(DroppedKey):
    # Thanks to patches, a seashell is just a dropped key as far as the randomizer is concerned.

    def configure(self, options):
        if not options.seashells:
            self.OPTIONS = [SEASHELL]


class SeashellMansionBonus(ItemInfo):
    def __init__(self, index):
        self.index = index
        super().__init__(0x2E9)
        self.patch_room = self.room - 0x29 + index

    def patch(self, rom, option, *, multiworld=None):
        rom.banks[0x3e][0x3800 + self.patch_room] = CHEST_ITEMS[option]
        if multiworld:
            rom.banks[0x3e][0x3300 + self.patch_room] = multiworld

    def configure(self, options):
        if not options.seashells:
            self.OPTIONS = [SEASHELL]

    @property
    def nameId(self):
        return "0x%03X-%s" % (self.room, self.index)


class SeashellMansion(DroppedKey):
    pass

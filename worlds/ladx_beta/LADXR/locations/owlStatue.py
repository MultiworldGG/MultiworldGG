from .itemInfo import ItemInfo
from .constants import *


class OwlStatue(ItemInfo):
    def __init__(self, room):
        super().__init__(room)
        if self.room < 0x100: # overworld owl
            self.patch_room = (self.room + 0x01) & 0xFF
        elif self.room < 0x200:
            self.patch_room = 0x100 | (((self.room - 0x31) & 0xFF) ^ 0x75)
        elif self.room < 0x300:
            self.patch_room = 0x200 | ((self.room + 0x03) & 0xFF)
        else: 
            self.patch_room = 0x300 | ((self.room + 0x01) & 0xFF)

    def configure(self, options):
        if options.owlstatues == "both":
            return
        if options.owlstatues == "dungeon" and self.room >= 0x100:
            return
        if options.owlstatues == "overworld" and self.room < 0x100:
            return
        raise RuntimeError("Tried to configure an owlstatue that was not enabled")
        self.OPTIONS = [RUPEES_20]

    def patch(self, rom, option, *, multiworld=None):
        #if option.startswith(MAP) or option.startswith(COMPASS) or option.startswith(STONE_BEAK) or option.startswith(NIGHTMARE_KEY) or option.startswith(KEY):
        #    if self._location.dungeon == int(option[-1]) and multiworld is not None:
        #        option = option[:-1]
        rom.banks[0x3E][0x3800 + self.patch_room] = CHEST_ITEMS[option]
        if multiworld:
            rom.banks[0x3E][0x3300 + self.patch_room] = multiworld

    def __repr__(self):
        if self._location and self._location.dungeon:
            return "%s:%03x:%d" % (self.__class__.__name__, self.room, self._location.dungeon)
        else:
            return "%s:%03x" % (self.__class__.__name__, self.room)
    
    @property
    def nameId(self):
        return "0x%03X-Owl" % self.room

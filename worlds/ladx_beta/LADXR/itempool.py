import logging
from Options import OptionError
from .locations.items import *
FILLER = 'FILLER'

DEFAULT_ITEM_POOL = {
    SWORD: 2,
    FEATHER: 1,
    HOOKSHOT: 1,
    BOW: 1,
    BOMB: 1,
    MAGIC_POWDER: 1,
    MAGIC_ROD: 1,
    OCARINA: 1,
    PEGASUS_BOOTS: 1,
    POWER_BRACELET: 2,
    SHIELD: 2,
    SHOVEL: 1,
    ROOSTER: 1,
    TOADSTOOL: 1,
    BOOMERANG: 1,

    TAIL_KEY: 1, SLIME_KEY: 1, ANGLER_KEY: 1, FACE_KEY: 1, BIRD_KEY: 1,
    GOLD_LEAF: 5,

    FLIPPERS: 1,
    BOWWOW: 1,
    SONG1: 1, SONG2: 1, SONG3: 1,

    BLUE_TUNIC: 1, RED_TUNIC: 1,
    MAX_ARROWS_UPGRADE: 1, MAX_BOMBS_UPGRADE: 1, MAX_POWDER_UPGRADE: 1,

    HEART_CONTAINER: 8,
    HEART_PIECE: 12,

    RUPEES_100: 3,
    RUPEES_20: 6,
    RUPEES_200: 3,
    RUPEES_50: 19,

    SEASHELL: 26,
    MEDICINE: 3,
    GEL: 4,
    MESSAGE: 1,

    COMPASS1: 1, COMPASS2: 1, COMPASS3: 1, COMPASS4: 1,
    COMPASS5: 1, COMPASS6: 1, COMPASS7: 1, COMPASS8: 1, COMPASS9: 1,
    KEY1: 3, KEY2: 5, KEY3: 9, KEY4: 5, KEY5: 3, KEY6: 3, KEY7: 3, KEY8: 7, KEY9: 3,
    MAP1: 1, MAP2: 1, MAP3: 1, MAP4: 1, MAP5: 1, MAP6: 1, MAP7: 1, MAP8: 1, MAP9: 1,
    NIGHTMARE_KEY1: 1, NIGHTMARE_KEY2: 1, NIGHTMARE_KEY3: 1, NIGHTMARE_KEY4: 1,
    NIGHTMARE_KEY5: 1, NIGHTMARE_KEY6: 1, NIGHTMARE_KEY7: 1, NIGHTMARE_KEY8: 1, NIGHTMARE_KEY9: 1,
    STONE_BEAK1: 1, STONE_BEAK2: 1, STONE_BEAK3: 1, STONE_BEAK4: 1,
    STONE_BEAK5: 1, STONE_BEAK6: 1, STONE_BEAK7: 1, STONE_BEAK8: 1, STONE_BEAK9: 1,
    
    INSTRUMENT1: 1, INSTRUMENT2: 1, INSTRUMENT3: 1, INSTRUMENT4: 1,
    INSTRUMENT5: 1, INSTRUMENT6: 1, INSTRUMENT7: 1, INSTRUMENT8: 1,

    TRADING_ITEM_YOSHI_DOLL: 1,
    TRADING_ITEM_RIBBON: 1,
    TRADING_ITEM_DOG_FOOD: 1,
    TRADING_ITEM_BANANAS: 1,
    TRADING_ITEM_STICK: 1,
    TRADING_ITEM_HONEYCOMB: 1,
    TRADING_ITEM_PINEAPPLE: 1,
    TRADING_ITEM_HIBISCUS: 1,
    TRADING_ITEM_LETTER: 1,
    TRADING_ITEM_BROOM: 1,
    TRADING_ITEM_FISHING_HOOK: 1,
    TRADING_ITEM_NECKLACE: 1,
    TRADING_ITEM_SCALE: 1,
    TRADING_ITEM_MAGNIFYING_GLASS: 1,

    "MEDICINE2": 1, "RAFT": 1, "ANGLER_KEYHOLE": 1, "CASTLE_BUTTON": 1
}

logger = logging.getLogger("Link's Awakening Logger")

class ItemPool:    
    def __init__(self, world_setup, settings, precollected):
        self.min_rupees = 1970
        self.__pool = {}
        self.__setup(world_setup, settings, precollected)

    def add(self, item, count=1):
        self.__pool[item] = self.__pool.get(item, 0) + count

    def remove(self, item, count=1):
        if count < 0 or count > self.get(item):
            count = self.get(item)
        self.__pool[item] = self.__pool.get(item, 0) - count
        if self.__pool[item] == 0:
            del self.__pool[item]

    def replace(self, item, replacement, count=1):
        if count < 0 or count > self.get(item):
            count = self.get(item)
        self.add(replacement, count)
        self.remove(item, count)

    def get(self, item):
        return self.__pool.get(item, 0)

    def count(self):
        total = 0
        for count in self.__pool.values():
            total += count
        return total

    def removeRupees(self, count):
        for n in range(count):
            self.removeRupee()

    def removeRupee(self):
        for item in (RUPEES_20, RUPEES_50, RUPEES_100, RUPEES_200, RUPEES_500):
            if self.get(item) > 0:
                self.remove(item)
                break

    def balanceRupees(self):
        while self.countRupees() < self.min_rupees and self.get(RUPEES_20):
            self.replace(RUPEES_20, RUPEES_50)
        while self.countRupees() < self.min_rupees and self.get(RUPEES_50):
            self.replace(RUPEES_50, RUPEES_100)
        while self.countRupees() < self.min_rupees and self.get(RUPEES_100):
            self.replace(RUPEES_100, RUPEES_200)
        while self.countRupees() < self.min_rupees and self.get(RUPEES_200):
            self.replace(RUPEES_200, RUPEES_500)
        
        while self.countRupees() >= self.min_rupees + 300 and self.get(RUPEES_500):
            self.replace(RUPEES_500, RUPEES_200)
        while self.countRupees() >= self.min_rupees + 100 and self.get(RUPEES_200):
            self.replace(RUPEES_200, RUPEES_100)
        while self.countRupees() >= self.min_rupees + 50 and self.get(RUPEES_100):
            self.replace(RUPEES_100, RUPEES_50)
        while self.countRupees() >= self.min_rupees + 30 and self.get(RUPEES_50):
            self.replace(RUPEES_50, RUPEES_20)

        assert self.countRupees() >= self.min_rupees


    def countRupees(self):
        count = 0
        for value in [20, 50, 100, 200, 500]:
            count += self.get(f'RUPEES_{value}') * value
        return count

    def numberRupees(self):
        number = 0
        for value in [20, 50, 100, 200, 500]:
            number += self.get(f'RUPEES_{value}')
        return number

    def __setup(self, world_setup, settings, precollected):
        default_item_pool = DEFAULT_ITEM_POOL

        for item, count in default_item_pool.items():
            self.add(item, count)

        location_count = self.count()

        # overworld settings change overall item count
        if settings.overworld == "dungeondive":
            location_count -= 73
            self.min_rupees -= 400
            self.remove(SHOVEL)
            self.remove(TOADSTOOL)
            self.remove(SEASHELL, 26)
            self.remove(TAIL_KEY)
            self.remove(SLIME_KEY)
            self.remove(ANGLER_KEY)
            self.remove(FACE_KEY)
            self.remove(BIRD_KEY)
            self.remove(GOLD_LEAF, 5)
            self.remove(SONG2)
            self.remove(SONG3)
            self.remove(BOWWOW)
            self.remove(ROOSTER)
            self.remove("MEDICINE2")
            self.remove("RAFT")
            self.remove("ANGLER_KEYHOLE")
            self.remove("CASTLE_BUTTON")

        overworld_owl_statues = 9
        owl_statues_per_dungeon = (3, 3, 3, 3, 1, 2, 3, 3, 3)
        condensed_location_adjustment_per_dungeon = (7, 10, 11, 17, 13, 12, 14, 11, 18)
        excluded_filler_adjustment_per_dungeon = (2, 2, 3, 2, 2, 2, 2, 2, 2)
        for n in range(1, 10):
            if n in world_setup.condensed_dungeons:
                location_count -= condensed_location_adjustment_per_dungeon[n%9]
                self.remove("MAP%d" % (n))
                self.remove("COMPASS%d" % (n))
                self.remove("STONE_BEAK%d" % (n))
                self.remove("KEY%d" % (n), -1)
                self.remove("NIGHTMARE_KEY%d" % (n))
            elif settings.owlstatues in ('dungeon', 'both'):
                location_count += owl_statues_per_dungeon[n%9]
            if n in world_setup.excluded_dungeons and settings.shuffleinstruments in ('vanilla', 'originaldungeon'):
                self.remove("INSTRUMENT%d" % (n))
                self.add(FILLER, excluded_filler_adjustment_per_dungeon[n%9])

        if settings.owlstatues in ('overworld', 'both'):
            location_count += overworld_owl_statues

        if not settings.tradequest:
            location_count -= 14
            self.remove(TRADING_ITEM_YOSHI_DOLL)
            self.remove(TRADING_ITEM_RIBBON)
            self.remove(TRADING_ITEM_DOG_FOOD)
            self.remove(TRADING_ITEM_BANANAS)
            self.remove(TRADING_ITEM_STICK)
            self.remove(TRADING_ITEM_HONEYCOMB)
            self.remove(TRADING_ITEM_PINEAPPLE)
            self.remove(TRADING_ITEM_HIBISCUS)
            self.remove(TRADING_ITEM_LETTER)
            self.remove(TRADING_ITEM_BROOM)
            self.remove(TRADING_ITEM_FISHING_HOOK)
            self.remove(TRADING_ITEM_NECKLACE)
            self.remove(TRADING_ITEM_SCALE)
            self.remove(TRADING_ITEM_MAGNIFYING_GLASS)

        # goal adjustments
        goal = world_setup.goal
        if isinstance(goal, str) and goal.startswith('='):
            instruments_to_remove = [i for i in range(1, 9) if str(i) not in goal]
            for i in instruments_to_remove:
                self.remove(f"INSTRUMENT{i}")
        elif settings.goal == "seashells":
            location_count -= 2
            self.remove(SEASHELL, 2)
            for n in range(8):
                self.remove("INSTRUMENT%d" % (n + 1))
        elif settings.goal == "open":
            for n in range(8):
                self.remove("INSTRUMENT%d" % (n + 1))

        # reserve extra filler if desired
        self.add(FILLER, world_setup.reserve_filler)

        # pull out precollected items while correcting amounts based on pool
        for name, amount in precollected.items():
            amount = min(self.get(name), amount)
            self.remove(name, amount)

        # try some corrections if we're over on items
        diff = self.count() - location_count

        def clamp(low, mid, hi):
            return min(hi, max(mid, low))

        def try_remove_rupees(leaving=0):
            nonlocal diff
            if diff > 0:
                to_remove = clamp(0, self.numberRupees() - leaving, diff)
                self.removeRupees(to_remove)
                diff -= to_remove

        def try_remove(item, leaving=0):
            nonlocal diff
            if diff > 0:
                to_remove = clamp(0, self.get(item) - leaving, diff)
                self.remove(item, to_remove)
                diff -= to_remove

        try_remove_rupees(leaving=25)
        try_remove(MESSAGE)
        try_remove(GEL)
        try_remove(MEDICINE)
        try_remove(SEASHELL, leaving=24)
        while diff >= 3 and self.get(HEART_PIECE) >= 4:
            self.add(HEART_CONTAINER)
            self.remove(HEART_PIECE, 4)
            diff -= 3
        try_remove_rupees(leaving=20)
        if diff >= 3:
            self.remove(MAX_ARROWS_UPGRADE)
            self.remove(MAX_BOMBS_UPGRADE)
            self.remove(MAX_POWDER_UPGRADE)
            diff -= 3
        if diff >= 2:
            self.remove(BLUE_TUNIC)
            self.remove(RED_TUNIC)
            diff -= 2
        try_remove(BOWWOW)
        try_remove_rupees(leaving=15)
        try_remove(SEASHELL, leaving=22)
        try_remove_rupees(leaving=8)
        # getting into desperation removals
        if settings.overworld=="dungeondive":
            try_remove(SHIELD, leaving=1)
        if settings.overworld=="dungeondive" and 6 in world_setup.condensed_dungeons:
            try_remove(POWER_BRACELET, leaving=1)
        if settings.logic in ("glitched", "hell"):
            try_remove(SONG1)
        try_remove(SWORD, leaving=1)
        try_remove(BOOMERANG)
        # last hope removals
        try_remove(SEASHELL, leaving=20)
        try_remove_rupees(leaving=(self.min_rupees // 500) + 2)
        try_remove(FILLER) # pull filler back out if we reserved too much
        try_remove(HEART_CONTAINER)
        if diff > 0:
            raise OptionError(
                f"Not enough locations. Need {diff} more at bare minimum. " +
                "This is usually from combining dungeon_dive overworld with " +
                "too many condensed/excluded dungeons."
            )

        self.add(FILLER, location_count - self.count())
        self.balanceRupees()

    def toDict(self):
        return self.__pool.copy()

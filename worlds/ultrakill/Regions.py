from typing import List
from dataclasses import dataclass


@dataclass
class UKRegion:
    short_name: str
    full_name: str


@dataclass
class LevelRegion(UKRegion):
    level_id: int
    level_layer: int


@dataclass
class SecretRegion(UKRegion):
    level_layer: int
    parent_level: LevelRegion


@dataclass
class EncoreRegion(UKRegion):
    level_id: int


@dataclass
class PrimeRegion(UKRegion):
    level_id: int


class Regions:
    shop = UKRegion("shop", "Shop")
    museum = UKRegion("museum", "Developer Museum")

    l1 = LevelRegion("0-1", "0-1: INTO THE FIRE", 1, 0)
    l2 = LevelRegion("0-2", "0-2: THE MEATGRINDER", 2, 0)
    l3 = LevelRegion("0-3", "0-3: DOUBLE DOWN", 3, 0)
    l4 = LevelRegion("0-4", "0-4: A ONE-MACHINE ARMY", 4, 0)
    l5 = LevelRegion("0-5", "0-5: CERBERUS", 5, 0)
    s0 = SecretRegion("0-S", "0-S: SOMETHING WICKED", 0, l2)

    l6 = LevelRegion("1-1", "1-1: HEART OF THE SUNRISE", 6, 1)
    l7 = LevelRegion("1-2", "1-2: THE BURNING WORLD", 7, 1)
    l8 = LevelRegion("1-3", "1-3: HALLS OF SACRED REMAINS", 8, 1)
    l9 = LevelRegion("1-4", "1-4: CLAIR DE LUNE", 9, 1)
    s1 = SecretRegion("1-S", "1-S: THE WITLESS", 1, l6)

    l10 = LevelRegion("2-1", "2-1: BRIDGEBURNER", 10, 2)
    l11 = LevelRegion("2-2", "2-2: DEATH AT 20,000 VOLTS", 11, 2)
    l12 = LevelRegion("2-3", "2-3: SHEER HEART ATTACK", 12, 2)
    l13 = LevelRegion("2-4", "2-4: COURT OF THE CORPSE KING", 13, 2)
    s2 = SecretRegion("2-S", "2-S: ALL IMPERFECT LOVE SONG", 2, l12)

    l14 = LevelRegion("3-1", "3-1: BELLY OF THE BEAST", 14, 3)
    l15 = LevelRegion("3-2", "3-2: IN THE FLESH", 15, 3)

    l16 = LevelRegion("4-1", "4-1: SLAVES TO POWER", 16, 4)
    l17 = LevelRegion("4-2", "4-2: GOD DAMN THE SUN", 17, 4)
    l18 = LevelRegion("4-3", "4-3: A SHOT IN THE DARK", 18, 4)
    l19 = LevelRegion("4-4", "4-4: CLAIR DE SOLEIL", 19, 4)
    s4 = SecretRegion("4-S", "4-S: CLASH OF THE BRANDICOOT", 4, l17)

    l20 = LevelRegion("5-1", "5-1: IN THE WAKE OF POSEIDON", 20, 5)
    l21 = LevelRegion("5-2", "5-2: WAVES OF THE STARLESS SEA", 21, 5)
    l22 = LevelRegion("5-3", "5-3: SHIP OF FOOLS", 22, 5)
    l23 = LevelRegion("5-4", "5-4: LEVIATHAN", 23, 5)
    s5 = SecretRegion("5-S", "5-S: I ONLY SAY MORNING", 5, l20)

    l24 = LevelRegion("6-1", "6-1: CRY FOR THE WEEPER", 24, 6)
    l25 = LevelRegion("6-2", "6-2: AESTHETICS OF HATE", 25, 6)

    l26 = LevelRegion("7-1", "7-1: GARDEN OF FORKING PATHS", 26, 7)
    l27 = LevelRegion("7-2", "7-2: LIGHT UP THE NIGHT", 27, 7)
    l28 = LevelRegion("7-3", "7-3: NO SOUND, NO MEMORY", 28, 7)
    l29 = LevelRegion("7-4", "7-4: ...LIKE ANTENNAS TO HEAVEN", 29, 7)
    s7 = SecretRegion("7-S", "7-S: HELL BATH NO FURY", 7, l28)

    l30 = LevelRegion("8-1", "8-1: HURTBREAK WONDERLAND", 30, 8)
    l31 = LevelRegion("8-2", "8-2: THROUGH THE MIRROR", 31, 8)
    l32 = LevelRegion("8-3", "8-3: DISINTEGRATION LOOP", 32, 8)
    l33 = LevelRegion("8-4", "8-4: FINAL FLIGHT", 33, 8)

    e0 = EncoreRegion("0-E", "0-E: THIS HEAT, AN EVIL HEAT", 100)
    e1 = EncoreRegion("1-E", "1-E: ...THEN FELL THE ASHES", 101)

    p1 = PrimeRegion("P-1", "P-1: SOUL SURVIVOR", 666)
    p2 = PrimeRegion("P-2", "P-2: WAIT OF THE WORLD", 667)

    all_regions: List[UKRegion] = [
        shop, museum, l1, l2, l3, l4, l5, s0, l6, l7, l8, l9, s1, l10, l11, l12, l13, s2, l14, l15, l16, l17, l18, l19,
        s4, l20, l21, l22, l23, s5, l24, l25, l26, l27, l28, l29, l30, l31, l32, l33, s7, e0, e1, p1, p2
    ]


    @classmethod
    def get_from_short_name(cls, name: str) -> UKRegion:
        for region in cls.all_regions:
            if region.short_name == name:
                return region
        return None
    

    @classmethod
    def get_from_full_name(cls, name: str) -> UKRegion:
        for region in cls.all_regions:
            if region.full_name == name:
                return region
        return None
    

    @classmethod
    def get_from_id(cls, id: int) -> UKRegion:
        if id < 1:
            for region in [region for region in cls.all_regions if isinstance(region, SecretRegion)]:
                if region.level_layer * -1 == id:
                    return region
        else:
            for region in [region for region in cls.all_regions if isinstance(region, LevelRegion) or isinstance(region, PrimeRegion) or isinstance(region, EncoreRegion)]:
                if region.level_id == id:
                    return region
        return None

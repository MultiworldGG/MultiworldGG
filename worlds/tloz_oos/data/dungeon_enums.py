from enum import StrEnum


class BossName(StrEnum):
    d1_boss = "Aquamentus"
    d2_boss = "Dodongo"
    d3_boss = "Mothulla"
    d4_boss = "Gohma"
    d5_boss = "Digdogger"
    d6_boss = "Manhandala"
    d7_boss = "Gleeok"
    d8_boss = "Medusa"


class DungeonName(StrEnum):
    d0 = "Hero's Cave"
    d1 = "Gnarled Root Dungeon"
    d2 = "Snake's Remains"
    d3 = "Poison Moth's Lair"
    d4 = "Dancing Dragon Dungeon"
    d5 = "Unicorn's Cave"
    d6 = "Ancient Remains"
    d7 = "Explorers Crypt"
    d8 = "Sword & Shield Dungeon"
    d11 = "Linked Hero's Cave"


boss_name_to_dungeon_mapping = {
    BossName.d1_boss.value.lower(): 1,
    BossName.d2_boss.value.lower(): 2,
    BossName.d3_boss.value.lower(): 3,
    BossName.d4_boss.value.lower(): 4,
    BossName.d5_boss.value.lower(): 5,
    BossName.d6_boss.value.lower(): 6,
    BossName.d7_boss.value.lower(): 7,
    BossName.d8_boss.value.lower(): 8,
}

dungeon_name_to_dungeon_mapping = {
    DungeonName.d0.value.lower(): 0,
    DungeonName.d1.value.lower(): 1,
    DungeonName.d2.value.lower(): 2,
    DungeonName.d3.value.lower(): 3,
    DungeonName.d4.value.lower(): 4,
    DungeonName.d5.value.lower(): 5,
    DungeonName.d6.value.lower(): 6,
    DungeonName.d7.value.lower(): 7,
    DungeonName.d8.value.lower(): 8,
    DungeonName.d11.value.lower(): 11,
}

from collections.abc import Callable
from enum import StrEnum
from typing import TYPE_CHECKING, NamedTuple

from BaseClasses import Location
from .options import GoalConditions

if TYPE_CHECKING:
    from . import CandyBox2World


class CandyBox2LocationData(NamedTuple):
    id: int | None = None
    is_included: Callable[["CandyBox2World"], bool] = lambda _: True


class CandyBox2Location(Location):
    game: str = "Candy Box 2"


class CandyBox2LocationName(StrEnum):
    HP_BAR_UNLOCK = "Candy Box: HP Bar Unlock"
    DISAPPOINTED_EMOTE_CHOCOLATE_BAR = "Candy Box: Throw 1630 candies"
    VILLAGE_SHOP_TOP_LOLLIPOP = "Shop: Top Lollipop"
    VILLAGE_SHOP_CENTRE_LOLLIPOP = "Shop: Centre Lollipop"
    VILLAGE_SHOP_BOTTOM_LOLLIPOP = "Shop: Bottom Lollipop"
    VILLAGE_SHOP_CHOCOLATE_BAR = "Shop: Chocolate Bar"
    VILLAGE_SHOP_TIME_RING = "Shop: Time Ring"
    VILLAGE_SHOP_CANDY_MERCHANTS_HAT = "Shop: Candy Merchant's Hat"
    VILLAGE_SHOP_LEATHER_GLOVES = "Shop: Leather Gloves"
    VILLAGE_SHOP_LEATHER_BOOTS = "Shop: Leather Boots"
    VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF = "Fifth House: Lollipop on bookshelf"
    VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF = "Fifth House: Lollipop in bookshelf"
    VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG = "Fifth House: Lollipop under rug"
    CELLAR_QUEST_CLEARED = "Cellar Quest: Quest Cleared"
    DESERT_QUEST_CLEARED = "Desert Quest: Quest Cleared"
    DESERT_BIRD_FEATHER_ACQUIRED = "Desert Quest: Get Desert Bird Feather"
    TROLL_DEFEATED = "Bridge Quest: Troll Defeated"
    THE_TROLLS_BLUDGEON_ACQUIRED = "Bridge Quest: Get Troll's Bludgeon"
    CAVE_EXIT = "Cave: Exit"
    CAVE_CHOCOLATE_BAR = "Cave: Chocolate Bar"
    CAVE_HEART_PLUG = "Cave: Heart Plug"
    FOREST_QUEST_CLEARED = "Forest Quest: Quest Cleared"
    CASTLE_ENTRANCE_QUEST_CLEARED = "Castle Entrance Quest: Quest Cleared"
    KNIGHT_BODY_ARMOUR_ACQUIRED = "Castle Entrance Quest: Get Knight Body Armour"
    GIANT_NOUGAT_MONSTER_DEFEATED = "Nougat Monster Quest: Giant Nougat Monster Defeated"
    SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES = "Sorceress' Hut: Inconspicuous Lollipop"
    SORCERESS_HUT_BEGINNERS_GRIMOIRE = "Sorceress' Hut: Beginner's Grimoire"
    SORCERESS_HUT_ADVANCED_GRIMOIRE = "Sorceress' Hut: Advanced Grimoire"
    SORCERESS_HUT_CAULDRON = "Sorceress' Hut: Cauldron"
    SORCERESS_HUT_HAT = "Sorceress' Hut: Sorceress' Hat"
    OCTOPUS_KING_DEFEATED = "Octopus King Quest: Octopus King Defeated"
    MONKEY_WIZARD_DEFEATED = "Monkey Wizard Quest: Monkey Wizard Defeated"
    EGG_ROOM_QUEST_CLEARED = "Egg Room Quest: Chest Opened"
    DEVIL_DEFEATED = "Hell Quest: Devil Defeated"
    THE_DEVELOPER_DEFEATED = "Developer Quest: The Developer Defeated"
    SOLVE_CYCLOPS_PUZZLE = "Lighthouse: Solve Cyclops Puzzle"
    VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE = "Forge: Inconspicuous Lollipop"
    VILLAGE_FORGE_BUY_WOODEN_SWORD = "Forge: Wooden Sword"
    VILLAGE_FORGE_BUY_IRON_AXE = "Forge: Iron Axe"
    VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD = "Forge: Polished Silver Sword"
    VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR = "Forge: Lightweight Body Armour"
    VILLAGE_FORGE_BUY_SCYTHE = "Forge: Scythe"
    ENCHANT_RED_ENCHANTED_GLOVES = "Wishing Well: Red Enchanted Gloves"
    ENCHANT_PINK_ENCHANTED_GLOVES = "Wishing Well: Pink Enchanted Gloves"
    ENCHANT_SUMMONING_TRIBAL_SPEAR = "Wishing Well: Summoning Tribal Spear"
    ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF = "Wishing Well: Enchanted Monkey Wizard Staff"
    ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR = "Wishing Well: Enchanted Knight Body Armour"
    ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS = "Wishing Well: Octopus King Crown with Jaspers"
    ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN = "Wishing Well: Octopus King Crown with Obsidian"
    ENCHANT_GIANT_SPOON_OF_DOOM = "Wishing Well: Giant Spoon of Doom"
    THE_HOLE_TRIBAL_WARRIOR_DEFEATED = "Hole: Tribal Warrior Defeated"
    THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED = "Hole: Right Chest Opened"
    THE_HOLE_HEART_PENDANT_ACQUIRED = "Hole: Top Chest Opened"
    THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED = "Hole: Left Chest Opened"
    THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED = "Hole: Bottom Chest Opened"
    TEAPOT_DEFEATED = "Teapot Quest: Teapot Defeated"
    XINOPHERYDON_DEFEATED = "Xinopherydon Quest: Xinopherydon Defeated"
    XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED = "Xinopherydon Quest: Unicorn Horn Acquired"
    ROCKET_BOOTS_ACQUIRED = "Ledge Quest: Chest Opened"
    PITCHFORK_ACQUIRED = "Castle Dark Room: Get Pitchfork"
    THE_SQUIRRELS_FIRST_QUESTION = "A Tree: The Squirrel's first question"
    THE_SQUIRRELS_SECOND_QUESTION = "A Tree: The Squirrel's second question"
    THE_SQUIRRELS_THIRD_QUESTION = "A Tree: The Squirrel's third question"
    THE_SQUIRRELS_FOURTH_QUESTION = "A Tree: The Squirrel's fourth question"
    THE_SQUIRRELS_FIFTH_QUESTION = "A Tree: The Squirrel's fifth question"
    THE_SQUIRRELS_PUZZLE = "A Tree: The Squirrel's puzzle"
    THE_SPONGE_ACQUIRED = "The Sea: Get Sponge"
    THE_SHELL_POWDER_ACQUIRED = "The Sea: Get Shell Powder"
    THE_RED_FIN_ACQUIRED = "The Sea: Get Red Fin"
    THE_GREEN_FIN_ACQUIRED = "The Sea: Get Green Fin"
    THE_PURPLE_FIN_ACQUIRED = "The Sea: Get Purple Fin"
    X_MARKS_THE_SPOT = "Secret Treasure Spot: X marks the spot!"
    LOCKED_CANDY_BOX_ACQUIRED = "Lonely House: Locked Candy Box Acquired"
    YOURSELF_DEFEATED = "X Potion Quest: Yourself Defeated"
    BAKE_PAIN_AU_CHOCOLAT_1 = "Castle Bakehouse: Bake Pain au Chocolat 1"
    BAKE_PAIN_AU_CHOCOLAT_2 = "Castle Bakehouse: Bake Pain au Chocolat 2"
    BAKE_PAIN_AU_CHOCOLAT_3 = "Castle Bakehouse: Bake Pain au Chocolat 3"
    BAKE_PAIN_AU_CHOCOLAT_4 = "Castle Bakehouse: Bake Pain au Chocolat 4"
    BAKE_PAIN_AU_CHOCOLAT_5 = "Castle Bakehouse: Bake Pain au Chocolat 5"
    POGO_STICK = "The Mountains: Pogo Stick"
    TALKING_CANDY = "The Tower: Take the Talking Candy"

    # Message to future me and Aren: I am so sorry.
    LOLLIPOP_FARM_EXTRA_1 = "Lollipop Farm: Planted 1 Lollipops"
    LOLLIPOP_FARM_EXTRA_2 = "Lollipop Farm: Planted 2 Lollipops"
    LOLLIPOP_FARM_EXTRA_3 = "Lollipop Farm: Planted 3 Lollipops"
    LOLLIPOP_FARM_EXTRA_4 = "Lollipop Farm: Planted 4 Lollipops"
    LOLLIPOP_FARM_EXTRA_5 = "Lollipop Farm: Planted 5 Lollipops"
    LOLLIPOP_FARM_EXTRA_6 = "Lollipop Farm: Planted 6 Lollipops"
    LOLLIPOP_FARM_EXTRA_7 = "Lollipop Farm: Planted 7 Lollipops"
    LOLLIPOP_FARM_EXTRA_8 = "Lollipop Farm: Planted 8 Lollipops"
    LOLLIPOP_FARM_EXTRA_9 = "Lollipop Farm: Planted 9 Lollipops"
    LOLLIPOP_FARM_EXTRA_10 = "Lollipop Farm: Planted 10 Lollipops"
    LOLLIPOP_FARM_EXTRA_11 = "Lollipop Farm: Planted 11 Lollipops"
    LOLLIPOP_FARM_EXTRA_12 = "Lollipop Farm: Planted 12 Lollipops"
    LOLLIPOP_FARM_EXTRA_13 = "Lollipop Farm: Planted 13 Lollipops"
    LOLLIPOP_FARM_EXTRA_14 = "Lollipop Farm: Planted 14 Lollipops"
    LOLLIPOP_FARM_EXTRA_15 = "Lollipop Farm: Planted 15 Lollipops"
    LOLLIPOP_FARM_EXTRA_16 = "Lollipop Farm: Planted 16 Lollipops"
    LOLLIPOP_FARM_EXTRA_17 = "Lollipop Farm: Planted 17 Lollipops"
    LOLLIPOP_FARM_EXTRA_18 = "Lollipop Farm: Planted 18 Lollipops"
    LOLLIPOP_FARM_EXTRA_19 = "Lollipop Farm: Planted 19 Lollipops"
    LOLLIPOP_FARM_EXTRA_20 = "Lollipop Farm: Planted 20 Lollipops"
    LOLLIPOP_FARM_EXTRA_21 = "Lollipop Farm: Planted 21 Lollipops"
    LOLLIPOP_FARM_EXTRA_22 = "Lollipop Farm: Planted 22 Lollipops"
    LOLLIPOP_FARM_EXTRA_23 = "Lollipop Farm: Planted 23 Lollipops"
    LOLLIPOP_FARM_EXTRA_24 = "Lollipop Farm: Planted 24 Lollipops"
    LOLLIPOP_FARM_EXTRA_25 = "Lollipop Farm: Planted 25 Lollipops"
    LOLLIPOP_FARM_EXTRA_26 = "Lollipop Farm: Planted 26 Lollipops"
    LOLLIPOP_FARM_EXTRA_27 = "Lollipop Farm: Planted 27 Lollipops"
    LOLLIPOP_FARM_EXTRA_28 = "Lollipop Farm: Planted 28 Lollipops"
    LOLLIPOP_FARM_EXTRA_29 = "Lollipop Farm: Planted 29 Lollipops"
    LOLLIPOP_FARM_EXTRA_30 = "Lollipop Farm: Planted 30 Lollipops"
    LOLLIPOP_FARM_EXTRA_31 = "Lollipop Farm: Planted 31 Lollipops"
    LOLLIPOP_FARM_EXTRA_32 = "Lollipop Farm: Planted 32 Lollipops"
    LOLLIPOP_FARM_EXTRA_33 = "Lollipop Farm: Planted 33 Lollipops"
    LOLLIPOP_FARM_EXTRA_34 = "Lollipop Farm: Planted 34 Lollipops"
    LOLLIPOP_FARM_EXTRA_35 = "Lollipop Farm: Planted 35 Lollipops"
    LOLLIPOP_FARM_EXTRA_36 = "Lollipop Farm: Planted 36 Lollipops"
    LOLLIPOP_FARM_EXTRA_37 = "Lollipop Farm: Planted 37 Lollipops"
    LOLLIPOP_FARM_EXTRA_38 = "Lollipop Farm: Planted 38 Lollipops"
    LOLLIPOP_FARM_EXTRA_39 = "Lollipop Farm: Planted 39 Lollipops"
    LOLLIPOP_FARM_EXTRA_40 = "Lollipop Farm: Planted 40 Lollipops"
    LOLLIPOP_FARM_EXTRA_41 = "Lollipop Farm: Planted 41 Lollipops"
    LOLLIPOP_FARM_EXTRA_42 = "Lollipop Farm: Planted 42 Lollipops"
    LOLLIPOP_FARM_EXTRA_43 = "Lollipop Farm: Planted 43 Lollipops"
    LOLLIPOP_FARM_EXTRA_44 = "Lollipop Farm: Planted 44 Lollipops"
    LOLLIPOP_FARM_EXTRA_45 = "Lollipop Farm: Planted 45 Lollipops"
    LOLLIPOP_FARM_EXTRA_46 = "Lollipop Farm: Planted 46 Lollipops"
    LOLLIPOP_FARM_EXTRA_47 = "Lollipop Farm: Planted 47 Lollipops"
    LOLLIPOP_FARM_EXTRA_48 = "Lollipop Farm: Planted 48 Lollipops"
    LOLLIPOP_FARM_EXTRA_49 = "Lollipop Farm: Planted 49 Lollipops"
    LOLLIPOP_FARM_EXTRA_50 = "Lollipop Farm: Planted 50 Lollipops"
    LOLLIPOP_FARM_EXTRA_51 = "Lollipop Farm: Planted 51 Lollipops"
    LOLLIPOP_FARM_EXTRA_52 = "Lollipop Farm: Planted 52 Lollipops"
    LOLLIPOP_FARM_EXTRA_53 = "Lollipop Farm: Planted 53 Lollipops"
    LOLLIPOP_FARM_EXTRA_54 = "Lollipop Farm: Planted 54 Lollipops"
    LOLLIPOP_FARM_EXTRA_55 = "Lollipop Farm: Planted 55 Lollipops"
    LOLLIPOP_FARM_EXTRA_56 = "Lollipop Farm: Planted 56 Lollipops"
    LOLLIPOP_FARM_EXTRA_57 = "Lollipop Farm: Planted 57 Lollipops"
    LOLLIPOP_FARM_EXTRA_58 = "Lollipop Farm: Planted 58 Lollipops"
    LOLLIPOP_FARM_EXTRA_59 = "Lollipop Farm: Planted 59 Lollipops"
    LOLLIPOP_FARM_EXTRA_60 = "Lollipop Farm: Planted 60 Lollipops"
    LOLLIPOP_FARM_EXTRA_61 = "Lollipop Farm: Planted 61 Lollipops"
    LOLLIPOP_FARM_EXTRA_62 = "Lollipop Farm: Planted 62 Lollipops"
    LOLLIPOP_FARM_EXTRA_63 = "Lollipop Farm: Planted 63 Lollipops"
    LOLLIPOP_FARM_EXTRA_64 = "Lollipop Farm: Planted 64 Lollipops"
    LOLLIPOP_FARM_EXTRA_65 = "Lollipop Farm: Planted 65 Lollipops"
    LOLLIPOP_FARM_EXTRA_66 = "Lollipop Farm: Planted 66 Lollipops"
    LOLLIPOP_FARM_EXTRA_67 = "Lollipop Farm: Planted 67 Lollipops"
    LOLLIPOP_FARM_EXTRA_68 = "Lollipop Farm: Planted 68 Lollipops"
    LOLLIPOP_FARM_EXTRA_69 = "Lollipop Farm: Planted 69 Lollipops"
    LOLLIPOP_FARM_EXTRA_70 = "Lollipop Farm: Planted 70 Lollipops"
    LOLLIPOP_FARM_EXTRA_71 = "Lollipop Farm: Planted 71 Lollipops"
    LOLLIPOP_FARM_EXTRA_72 = "Lollipop Farm: Planted 72 Lollipops"
    LOLLIPOP_FARM_EXTRA_73 = "Lollipop Farm: Planted 73 Lollipops"
    LOLLIPOP_FARM_EXTRA_74 = "Lollipop Farm: Planted 74 Lollipops"
    LOLLIPOP_FARM_EXTRA_75 = "Lollipop Farm: Planted 75 Lollipops"
    LOLLIPOP_FARM_EXTRA_76 = "Lollipop Farm: Planted 76 Lollipops"
    LOLLIPOP_FARM_EXTRA_77 = "Lollipop Farm: Planted 77 Lollipops"
    LOLLIPOP_FARM_EXTRA_78 = "Lollipop Farm: Planted 78 Lollipops"
    LOLLIPOP_FARM_EXTRA_79 = "Lollipop Farm: Planted 79 Lollipops"
    LOLLIPOP_FARM_EXTRA_80 = "Lollipop Farm: Planted 80 Lollipops"
    LOLLIPOP_FARM_EXTRA_81 = "Lollipop Farm: Planted 81 Lollipops"
    LOLLIPOP_FARM_EXTRA_82 = "Lollipop Farm: Planted 82 Lollipops"
    LOLLIPOP_FARM_EXTRA_83 = "Lollipop Farm: Planted 83 Lollipops"
    LOLLIPOP_FARM_EXTRA_84 = "Lollipop Farm: Planted 84 Lollipops"
    LOLLIPOP_FARM_EXTRA_85 = "Lollipop Farm: Planted 85 Lollipops"
    LOLLIPOP_FARM_EXTRA_86 = "Lollipop Farm: Planted 86 Lollipops"
    LOLLIPOP_FARM_EXTRA_87 = "Lollipop Farm: Planted 87 Lollipops"
    LOLLIPOP_FARM_EXTRA_88 = "Lollipop Farm: Planted 88 Lollipops"
    LOLLIPOP_FARM_EXTRA_89 = "Lollipop Farm: Planted 89 Lollipops"
    LOLLIPOP_FARM_EXTRA_90 = "Lollipop Farm: Planted 90 Lollipops"
    LOLLIPOP_FARM_EXTRA_91 = "Lollipop Farm: Planted 91 Lollipops"
    LOLLIPOP_FARM_EXTRA_92 = "Lollipop Farm: Planted 92 Lollipops"
    LOLLIPOP_FARM_EXTRA_93 = "Lollipop Farm: Planted 93 Lollipops"
    LOLLIPOP_FARM_EXTRA_94 = "Lollipop Farm: Planted 94 Lollipops"
    LOLLIPOP_FARM_EXTRA_95 = "Lollipop Farm: Planted 95 Lollipops"
    LOLLIPOP_FARM_EXTRA_96 = "Lollipop Farm: Planted 96 Lollipops"
    LOLLIPOP_FARM_EXTRA_97 = "Lollipop Farm: Planted 97 Lollipops"
    LOLLIPOP_FARM_EXTRA_98 = "Lollipop Farm: Planted 98 Lollipops"
    LOLLIPOP_FARM_EXTRA_99 = "Lollipop Farm: Planted 99 Lollipops"
    LOLLIPOP_FARM_EXTRA_100 = "Lollipop Farm: Planted 100 Lollipops"
    LOLLIPOP_FARM_EXTRA_101 = "Lollipop Farm: Planted 1000 Lollipops"
    LOLLIPOP_FARM_EXTRA_102 = "Lollipop Farm: Planted 2000 Lollipops"
    LOLLIPOP_FARM_EXTRA_103 = "Lollipop Farm: Planted 3000 Lollipops"
    LOLLIPOP_FARM_EXTRA_104 = "Lollipop Farm: Planted 4000 Lollipops"
    LOLLIPOP_FARM_EXTRA_105 = "Lollipop Farm: Planted 5000 Lollipops"
    LOLLIPOP_FARM_EXTRA_106 = "Lollipop Farm: Planted 6000 Lollipops"
    LOLLIPOP_FARM_EXTRA_107 = "Lollipop Farm: Planted 7000 Lollipops"
    LOLLIPOP_FARM_EXTRA_108 = "Lollipop Farm: Planted 8000 Lollipops"
    LOLLIPOP_FARM_EXTRA_109 = "Lollipop Farm: Planted 9000 Lollipops"
    LOLLIPOP_FARM_EXTRA_110 = "Lollipop Farm: Planted 10000 Lollipops"
    LOLLIPOP_FARM_EXTRA_111 = "Lollipop Farm: Planted 11000 Lollipops"
    LOLLIPOP_FARM_EXTRA_112 = "Lollipop Farm: Planted 12000 Lollipops"
    LOLLIPOP_FARM_EXTRA_113 = "Lollipop Farm: Planted 13000 Lollipops"
    LOLLIPOP_FARM_EXTRA_114 = "Lollipop Farm: Planted 14000 Lollipops"
    LOLLIPOP_FARM_EXTRA_115 = "Lollipop Farm: Planted 15000 Lollipops"
    LOLLIPOP_FARM_EXTRA_116 = "Lollipop Farm: Planted 16000 Lollipops"
    LOLLIPOP_FARM_EXTRA_117 = "Lollipop Farm: Planted 17000 Lollipops"
    LOLLIPOP_FARM_EXTRA_118 = "Lollipop Farm: Planted 18000 Lollipops"
    LOLLIPOP_FARM_EXTRA_119 = "Lollipop Farm: Planted 19000 Lollipops"
    LOLLIPOP_FARM_EXTRA_120 = "Lollipop Farm: Planted 20000 Lollipops"
    LOLLIPOP_FARM_EXTRA_121 = "Lollipop Farm: Planted 21000 Lollipops"
    LOLLIPOP_FARM_EXTRA_122 = "Lollipop Farm: Planted 22000 Lollipops"
    LOLLIPOP_FARM_EXTRA_123 = "Lollipop Farm: Planted 23000 Lollipops"
    LOLLIPOP_FARM_EXTRA_124 = "Lollipop Farm: Planted 24000 Lollipops"
    LOLLIPOP_FARM_EXTRA_125 = "Lollipop Farm: Planted 25000 Lollipops"
    LOLLIPOP_FARM_EXTRA_126 = "Lollipop Farm: Planted 26000 Lollipops"
    LOLLIPOP_FARM_EXTRA_127 = "Lollipop Farm: Planted 27000 Lollipops"
    LOLLIPOP_FARM_EXTRA_128 = "Lollipop Farm: Planted 28000 Lollipops"
    LOLLIPOP_FARM_EXTRA_129 = "Lollipop Farm: Planted 29000 Lollipops"
    LOLLIPOP_FARM_EXTRA_130 = "Lollipop Farm: Planted 30000 Lollipops"
    LOLLIPOP_FARM_EXTRA_131 = "Lollipop Farm: Planted 31000 Lollipops"
    LOLLIPOP_FARM_EXTRA_132 = "Lollipop Farm: Planted 32000 Lollipops"
    LOLLIPOP_FARM_EXTRA_133 = "Lollipop Farm: Planted 33000 Lollipops"
    LOLLIPOP_FARM_EXTRA_134 = "Lollipop Farm: Planted 34000 Lollipops"
    LOLLIPOP_FARM_EXTRA_135 = "Lollipop Farm: Planted 35000 Lollipops"
    LOLLIPOP_FARM_EXTRA_136 = "Lollipop Farm: Planted 36000 Lollipops"
    LOLLIPOP_FARM_EXTRA_137 = "Lollipop Farm: Planted 37000 Lollipops"
    LOLLIPOP_FARM_EXTRA_138 = "Lollipop Farm: Planted 38000 Lollipops"
    LOLLIPOP_FARM_EXTRA_139 = "Lollipop Farm: Planted 39000 Lollipops"
    LOLLIPOP_FARM_EXTRA_140 = "Lollipop Farm: Planted 40000 Lollipops"
    LOLLIPOP_FARM_EXTRA_141 = "Lollipop Farm: Planted 41000 Lollipops"
    LOLLIPOP_FARM_EXTRA_142 = "Lollipop Farm: Planted 42000 Lollipops"
    LOLLIPOP_FARM_EXTRA_143 = "Lollipop Farm: Planted 43000 Lollipops"
    LOLLIPOP_FARM_EXTRA_144 = "Lollipop Farm: Planted 44000 Lollipops"
    LOLLIPOP_FARM_EXTRA_145 = "Lollipop Farm: Planted 45000 Lollipops"
    LOLLIPOP_FARM_EXTRA_146 = "Lollipop Farm: Planted 46000 Lollipops"
    LOLLIPOP_FARM_EXTRA_147 = "Lollipop Farm: Planted 47000 Lollipops"
    LOLLIPOP_FARM_EXTRA_148 = "Lollipop Farm: Planted 48000 Lollipops"
    LOLLIPOP_FARM_EXTRA_149 = "Lollipop Farm: Planted 49000 Lollipops"
    LOLLIPOP_FARM_EXTRA_150 = "Lollipop Farm: Planted 50000 Lollipops"
    LOLLIPOP_FARM_EXTRA_151 = "Lollipop Farm: Planted 51000 Lollipops"
    LOLLIPOP_FARM_EXTRA_152 = "Lollipop Farm: Planted 52000 Lollipops"
    LOLLIPOP_FARM_EXTRA_153 = "Lollipop Farm: Planted 53000 Lollipops"
    LOLLIPOP_FARM_EXTRA_154 = "Lollipop Farm: Planted 54000 Lollipops"
    LOLLIPOP_FARM_EXTRA_155 = "Lollipop Farm: Planted 55000 Lollipops"
    LOLLIPOP_FARM_EXTRA_156 = "Lollipop Farm: Planted 56000 Lollipops"
    LOLLIPOP_FARM_EXTRA_157 = "Lollipop Farm: Planted 57000 Lollipops"
    LOLLIPOP_FARM_EXTRA_158 = "Lollipop Farm: Planted 58000 Lollipops"
    LOLLIPOP_FARM_EXTRA_159 = "Lollipop Farm: Planted 59000 Lollipops"
    LOLLIPOP_FARM_EXTRA_160 = "Lollipop Farm: Planted 60000 Lollipops"
    LOLLIPOP_FARM_EXTRA_161 = "Lollipop Farm: Planted 61000 Lollipops"
    LOLLIPOP_FARM_EXTRA_162 = "Lollipop Farm: Planted 62000 Lollipops"
    LOLLIPOP_FARM_EXTRA_163 = "Lollipop Farm: Planted 63000 Lollipops"
    LOLLIPOP_FARM_EXTRA_164 = "Lollipop Farm: Planted 64000 Lollipops"
    LOLLIPOP_FARM_EXTRA_165 = "Lollipop Farm: Planted 65000 Lollipops"
    LOLLIPOP_FARM_EXTRA_166 = "Lollipop Farm: Planted 66000 Lollipops"
    LOLLIPOP_FARM_EXTRA_167 = "Lollipop Farm: Planted 67000 Lollipops"
    LOLLIPOP_FARM_EXTRA_168 = "Lollipop Farm: Planted 68000 Lollipops"
    LOLLIPOP_FARM_EXTRA_169 = "Lollipop Farm: Planted 69000 Lollipops"
    LOLLIPOP_FARM_EXTRA_170 = "Lollipop Farm: Planted 70000 Lollipops"
    LOLLIPOP_FARM_EXTRA_171 = "Lollipop Farm: Planted 71000 Lollipops"
    LOLLIPOP_FARM_EXTRA_172 = "Lollipop Farm: Planted 72000 Lollipops"
    LOLLIPOP_FARM_EXTRA_173 = "Lollipop Farm: Planted 73000 Lollipops"
    LOLLIPOP_FARM_EXTRA_174 = "Lollipop Farm: Planted 74000 Lollipops"
    LOLLIPOP_FARM_EXTRA_175 = "Lollipop Farm: Planted 75000 Lollipops"
    LOLLIPOP_FARM_EXTRA_176 = "Lollipop Farm: Planted 76000 Lollipops"
    LOLLIPOP_FARM_EXTRA_177 = "Lollipop Farm: Planted 77000 Lollipops"
    LOLLIPOP_FARM_EXTRA_178 = "Lollipop Farm: Planted 78000 Lollipops"
    LOLLIPOP_FARM_EXTRA_179 = "Lollipop Farm: Planted 79000 Lollipops"
    LOLLIPOP_FARM_EXTRA_180 = "Lollipop Farm: Planted 80000 Lollipops"
    LOLLIPOP_FARM_EXTRA_181 = "Lollipop Farm: Planted 81000 Lollipops"
    LOLLIPOP_FARM_EXTRA_182 = "Lollipop Farm: Planted 82000 Lollipops"
    LOLLIPOP_FARM_EXTRA_183 = "Lollipop Farm: Planted 83000 Lollipops"
    LOLLIPOP_FARM_EXTRA_184 = "Lollipop Farm: Planted 84000 Lollipops"
    LOLLIPOP_FARM_EXTRA_185 = "Lollipop Farm: Planted 85000 Lollipops"
    LOLLIPOP_FARM_EXTRA_186 = "Lollipop Farm: Planted 86000 Lollipops"
    LOLLIPOP_FARM_EXTRA_187 = "Lollipop Farm: Planted 87000 Lollipops"
    LOLLIPOP_FARM_EXTRA_188 = "Lollipop Farm: Planted 88000 Lollipops"
    LOLLIPOP_FARM_EXTRA_189 = "Lollipop Farm: Planted 89000 Lollipops"
    LOLLIPOP_FARM_EXTRA_190 = "Lollipop Farm: Planted 90000 Lollipops"
    LOLLIPOP_FARM_EXTRA_191 = "Lollipop Farm: Planted 91000 Lollipops"
    LOLLIPOP_FARM_EXTRA_192 = "Lollipop Farm: Planted 92000 Lollipops"
    LOLLIPOP_FARM_EXTRA_193 = "Lollipop Farm: Planted 93000 Lollipops"
    LOLLIPOP_FARM_EXTRA_194 = "Lollipop Farm: Planted 94000 Lollipops"
    LOLLIPOP_FARM_EXTRA_195 = "Lollipop Farm: Planted 95000 Lollipops"
    LOLLIPOP_FARM_EXTRA_196 = "Lollipop Farm: Planted 96000 Lollipops"
    LOLLIPOP_FARM_EXTRA_197 = "Lollipop Farm: Planted 97000 Lollipops"
    LOLLIPOP_FARM_EXTRA_198 = "Lollipop Farm: Planted 98000 Lollipops"
    LOLLIPOP_FARM_EXTRA_199 = "Lollipop Farm: Planted 99000 Lollipops"
    LOLLIPOP_FARM_EXTRA_200 = "Lollipop Farm: Planted 100000 Lollipops"
    THE_SEA_EXTRA_1 = "The Sea: Travel 50m"
    THE_SEA_EXTRA_2 = "The Sea: Travel 100m"
    THE_SEA_EXTRA_3 = "The Sea: Travel 150m"
    THE_SEA_EXTRA_4 = "The Sea: Travel 200m"
    THE_SEA_EXTRA_5 = "The Sea: Travel 250m"
    THE_SEA_EXTRA_6 = "The Sea: Travel 300m"
    THE_SEA_EXTRA_7 = "The Sea: Travel 350m"
    THE_SEA_EXTRA_8 = "The Sea: Travel 400m"
    THE_SEA_EXTRA_9 = "The Sea: Travel 450m"
    THE_SEA_EXTRA_10 = "The Sea: Travel 500m"
    THE_SEA_EXTRA_11 = "The Sea: Travel 550m"
    THE_SEA_EXTRA_12 = "The Sea: Travel 600m"
    THE_SEA_EXTRA_13 = "The Sea: Travel 650m"
    THE_SEA_EXTRA_14 = "The Sea: Travel 700m"
    THE_SEA_EXTRA_15 = "The Sea: Travel 750m"
    THE_SEA_EXTRA_16 = "The Sea: Travel 800m"
    THE_SEA_EXTRA_17 = "The Sea: Travel 850m"
    THE_SEA_EXTRA_18 = "The Sea: Travel 900m"
    THE_SEA_EXTRA_19 = "The Sea: Travel 950m"
    THE_SEA_EXTRA_20 = "The Sea: Travel 1000m"
    THE_SEA_EXTRA_21 = "The Sea: Travel 1050m"
    THE_SEA_EXTRA_22 = "The Sea: Travel 1100m"
    THE_SEA_EXTRA_23 = "The Sea: Travel 1150m"
    THE_SEA_EXTRA_24 = "The Sea: Travel 1200m"
    THE_SEA_EXTRA_25 = "The Sea: Travel 1250m"
    THE_SEA_EXTRA_26 = "The Sea: Travel 1300m"
    THE_SEA_EXTRA_27 = "The Sea: Travel 1350m"
    THE_SEA_EXTRA_28 = "The Sea: Travel 1400m"
    THE_SEA_EXTRA_29 = "The Sea: Travel 1450m"
    THE_SEA_EXTRA_30 = "The Sea: Travel 1500m"
    THE_SEA_EXTRA_31 = "The Sea: Travel 1550m"
    THE_SEA_EXTRA_32 = "The Sea: Travel 1600m"
    THE_SEA_EXTRA_33 = "The Sea: Travel 1650m"
    THE_SEA_EXTRA_34 = "The Sea: Travel 1700m"
    THE_SEA_EXTRA_35 = "The Sea: Travel 1750m"
    THE_SEA_EXTRA_36 = "The Sea: Travel 1800m"
    THE_SEA_EXTRA_37 = "The Sea: Travel 1850m"
    THE_SEA_EXTRA_38 = "The Sea: Travel 1900m"
    THE_SEA_EXTRA_39 = "The Sea: Travel 1950m"
    THE_SEA_EXTRA_40 = "The Sea: Travel 2000m"
    THE_SEA_EXTRA_41 = "The Sea: Travel 2050m"
    THE_SEA_EXTRA_42 = "The Sea: Travel 2100m"
    THE_SEA_EXTRA_43 = "The Sea: Travel 2150m"
    THE_SEA_EXTRA_44 = "The Sea: Travel 2200m"
    THE_SEA_EXTRA_45 = "The Sea: Travel 2250m"
    THE_SEA_EXTRA_46 = "The Sea: Travel 2300m"
    THE_SEA_EXTRA_47 = "The Sea: Travel 2350m"
    THE_SEA_EXTRA_48 = "The Sea: Travel 2400m"
    THE_SEA_EXTRA_49 = "The Sea: Travel 2450m"
    THE_SEA_EXTRA_50 = "The Sea: Travel 2500m"
    THE_SEA_EXTRA_51 = "The Sea: Travel 2550m"
    THE_SEA_EXTRA_52 = "The Sea: Travel 2600m"
    THE_SEA_EXTRA_53 = "The Sea: Travel 2650m"
    THE_SEA_EXTRA_54 = "The Sea: Travel 2700m"
    THE_SEA_EXTRA_55 = "The Sea: Travel 2750m"
    THE_SEA_EXTRA_56 = "The Sea: Travel 2800m"
    THE_SEA_EXTRA_57 = "The Sea: Travel 2850m"
    THE_SEA_EXTRA_58 = "The Sea: Travel 2900m"
    THE_SEA_EXTRA_59 = "The Sea: Travel 2950m"
    THE_SEA_EXTRA_60 = "The Sea: Travel 3000m"
    THE_SEA_EXTRA_61 = "The Sea: Travel 3050m"
    THE_SEA_EXTRA_62 = "The Sea: Travel 3100m"
    THE_SEA_EXTRA_63 = "The Sea: Travel 3150m"
    THE_SEA_EXTRA_64 = "The Sea: Travel 3200m"
    THE_SEA_EXTRA_65 = "The Sea: Travel 3250m"
    THE_SEA_EXTRA_66 = "The Sea: Travel 3300m"
    THE_SEA_EXTRA_67 = "The Sea: Travel 3350m"
    THE_SEA_EXTRA_68 = "The Sea: Travel 3400m"
    THE_SEA_EXTRA_69 = "The Sea: Travel 3450m"
    THE_SEA_EXTRA_70 = "The Sea: Travel 3500m"
    THE_SEA_EXTRA_71 = "The Sea: Travel 3550m"
    THE_SEA_EXTRA_72 = "The Sea: Travel 3600m"
    THE_SEA_EXTRA_73 = "The Sea: Travel 3650m"
    THE_SEA_EXTRA_74 = "The Sea: Travel 3700m"
    THE_SEA_EXTRA_75 = "The Sea: Travel 3750m"
    THE_SEA_EXTRA_76 = "The Sea: Travel 3800m"
    THE_SEA_EXTRA_77 = "The Sea: Travel 3850m"
    THE_SEA_EXTRA_78 = "The Sea: Travel 3900m"
    THE_SEA_EXTRA_79 = "The Sea: Travel 3950m"
    THE_SEA_EXTRA_80 = "The Sea: Travel 4000m"


location_descriptions: dict[CandyBox2LocationName, str] = {CandyBox2LocationName.HP_BAR_UNLOCK: ""}

locations: dict[CandyBox2LocationName, CandyBox2LocationData] = {
    CandyBox2LocationName.HP_BAR_UNLOCK: CandyBox2LocationData(1),
    CandyBox2LocationName.DISAPPOINTED_EMOTE_CHOCOLATE_BAR: CandyBox2LocationData(2),
    CandyBox2LocationName.VILLAGE_SHOP_TOP_LOLLIPOP: CandyBox2LocationData(100),
    CandyBox2LocationName.VILLAGE_SHOP_CENTRE_LOLLIPOP: CandyBox2LocationData(101),
    CandyBox2LocationName.VILLAGE_SHOP_BOTTOM_LOLLIPOP: CandyBox2LocationData(102),
    CandyBox2LocationName.VILLAGE_SHOP_CHOCOLATE_BAR: CandyBox2LocationData(103),
    CandyBox2LocationName.VILLAGE_SHOP_TIME_RING: CandyBox2LocationData(104),
    CandyBox2LocationName.VILLAGE_SHOP_CANDY_MERCHANTS_HAT: CandyBox2LocationData(105),
    CandyBox2LocationName.VILLAGE_SHOP_LEATHER_GLOVES: CandyBox2LocationData(106),
    CandyBox2LocationName.VILLAGE_SHOP_LEATHER_BOOTS: CandyBox2LocationData(107),
    CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF: CandyBox2LocationData(200),
    CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF: CandyBox2LocationData(201),
    CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG: CandyBox2LocationData(202),
    CandyBox2LocationName.CELLAR_QUEST_CLEARED: CandyBox2LocationData(300),
    CandyBox2LocationName.POGO_STICK: CandyBox2LocationData(500),
    CandyBox2LocationName.DESERT_QUEST_CLEARED: CandyBox2LocationData(1100),
    CandyBox2LocationName.DESERT_BIRD_FEATHER_ACQUIRED: CandyBox2LocationData(1101),
    CandyBox2LocationName.TROLL_DEFEATED: CandyBox2LocationData(1200),
    CandyBox2LocationName.THE_TROLLS_BLUDGEON_ACQUIRED: CandyBox2LocationData(1201),
    CandyBox2LocationName.CAVE_EXIT: CandyBox2LocationData(1300),
    CandyBox2LocationName.CAVE_CHOCOLATE_BAR: CandyBox2LocationData(1301),
    CandyBox2LocationName.CAVE_HEART_PLUG: CandyBox2LocationData(1302),
    CandyBox2LocationName.FOREST_QUEST_CLEARED: CandyBox2LocationData(1400),
    CandyBox2LocationName.CASTLE_ENTRANCE_QUEST_CLEARED: CandyBox2LocationData(1500),
    CandyBox2LocationName.KNIGHT_BODY_ARMOUR_ACQUIRED: CandyBox2LocationData(1501),
    CandyBox2LocationName.GIANT_NOUGAT_MONSTER_DEFEATED: CandyBox2LocationData(1600),
    CandyBox2LocationName.SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES: CandyBox2LocationData(1800),
    CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE: CandyBox2LocationData(1801),
    CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE: CandyBox2LocationData(1802),
    CandyBox2LocationName.SORCERESS_HUT_CAULDRON: CandyBox2LocationData(1803),
    CandyBox2LocationName.SORCERESS_HUT_HAT: CandyBox2LocationData(1804),
    CandyBox2LocationName.OCTOPUS_KING_DEFEATED: CandyBox2LocationData(1900),
    CandyBox2LocationName.MONKEY_WIZARD_DEFEATED: CandyBox2LocationData(2000),
    CandyBox2LocationName.EGG_ROOM_QUEST_CLEARED: CandyBox2LocationData(2100),
    CandyBox2LocationName.DEVIL_DEFEATED: CandyBox2LocationData(2300),
    CandyBox2LocationName.THE_DEVELOPER_DEFEATED: CandyBox2LocationData(2400),
    CandyBox2LocationName.SOLVE_CYCLOPS_PUZZLE: CandyBox2LocationData(2500),
    CandyBox2LocationName.VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE: CandyBox2LocationData(2600),
    CandyBox2LocationName.VILLAGE_FORGE_BUY_WOODEN_SWORD: CandyBox2LocationData(2601),
    CandyBox2LocationName.VILLAGE_FORGE_BUY_IRON_AXE: CandyBox2LocationData(2700),
    CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD: CandyBox2LocationData(2800),
    CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR: CandyBox2LocationData(2900),
    CandyBox2LocationName.VILLAGE_FORGE_BUY_SCYTHE: CandyBox2LocationData(3000),
    CandyBox2LocationName.ENCHANT_RED_ENCHANTED_GLOVES: CandyBox2LocationData(3100),
    CandyBox2LocationName.ENCHANT_PINK_ENCHANTED_GLOVES: CandyBox2LocationData(3101),
    CandyBox2LocationName.ENCHANT_SUMMONING_TRIBAL_SPEAR: CandyBox2LocationData(3200),
    CandyBox2LocationName.ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF: CandyBox2LocationData(3300),
    CandyBox2LocationName.ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR: CandyBox2LocationData(3400),
    CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS: CandyBox2LocationData(3500),
    CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN: CandyBox2LocationData(3501),
    CandyBox2LocationName.ENCHANT_GIANT_SPOON_OF_DOOM: CandyBox2LocationData(3600),
    CandyBox2LocationName.THE_HOLE_TRIBAL_WARRIOR_DEFEATED: CandyBox2LocationData(3700),
    CandyBox2LocationName.THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED: CandyBox2LocationData(3701),
    CandyBox2LocationName.THE_HOLE_HEART_PENDANT_ACQUIRED: CandyBox2LocationData(3702),
    CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED: CandyBox2LocationData(3703),
    CandyBox2LocationName.THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED: CandyBox2LocationData(3704),
    CandyBox2LocationName.TEAPOT_DEFEATED: CandyBox2LocationData(3900),
    CandyBox2LocationName.XINOPHERYDON_DEFEATED: CandyBox2LocationData(4000),
    CandyBox2LocationName.XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED: CandyBox2LocationData(4001),
    CandyBox2LocationName.ROCKET_BOOTS_ACQUIRED: CandyBox2LocationData(4100),
    CandyBox2LocationName.PITCHFORK_ACQUIRED: CandyBox2LocationData(4300),
    CandyBox2LocationName.THE_SQUIRRELS_FIRST_QUESTION: CandyBox2LocationData(4400),
    CandyBox2LocationName.THE_SQUIRRELS_SECOND_QUESTION: CandyBox2LocationData(4401),
    CandyBox2LocationName.THE_SQUIRRELS_THIRD_QUESTION: CandyBox2LocationData(4402),
    CandyBox2LocationName.THE_SQUIRRELS_FOURTH_QUESTION: CandyBox2LocationData(4403),
    CandyBox2LocationName.THE_SQUIRRELS_FIFTH_QUESTION: CandyBox2LocationData(4404),
    CandyBox2LocationName.THE_SQUIRRELS_PUZZLE: CandyBox2LocationData(4405),
    CandyBox2LocationName.THE_SPONGE_ACQUIRED: CandyBox2LocationData(4500),
    CandyBox2LocationName.THE_SHELL_POWDER_ACQUIRED: CandyBox2LocationData(4501),
    CandyBox2LocationName.THE_RED_FIN_ACQUIRED: CandyBox2LocationData(4502),
    CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED: CandyBox2LocationData(4503),
    CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED: CandyBox2LocationData(4504),
    CandyBox2LocationName.X_MARKS_THE_SPOT: CandyBox2LocationData(4600),
    CandyBox2LocationName.LOCKED_CANDY_BOX_ACQUIRED: CandyBox2LocationData(4700),
    CandyBox2LocationName.YOURSELF_DEFEATED: CandyBox2LocationData(4800),
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_1: CandyBox2LocationData(4900),
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_2: CandyBox2LocationData(4901),
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_3: CandyBox2LocationData(4902),
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_4: CandyBox2LocationData(4903),
    CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_5: CandyBox2LocationData(4904),
    CandyBox2LocationName.TALKING_CANDY: CandyBox2LocationData(5000),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_1: CandyBox2LocationData(100000),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_2: CandyBox2LocationData(100001),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_3: CandyBox2LocationData(100002),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_4: CandyBox2LocationData(100003),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_5: CandyBox2LocationData(100004),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_6: CandyBox2LocationData(100005),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_7: CandyBox2LocationData(100006),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_8: CandyBox2LocationData(100007),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_9: CandyBox2LocationData(100008),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_10: CandyBox2LocationData(100009),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_11: CandyBox2LocationData(100010),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_12: CandyBox2LocationData(100011),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_13: CandyBox2LocationData(100012),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_14: CandyBox2LocationData(100013),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_15: CandyBox2LocationData(100014),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_16: CandyBox2LocationData(100015),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_17: CandyBox2LocationData(100016),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_18: CandyBox2LocationData(100017),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_19: CandyBox2LocationData(100018),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_20: CandyBox2LocationData(100019),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_21: CandyBox2LocationData(100020),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_22: CandyBox2LocationData(100021),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_23: CandyBox2LocationData(100022),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_24: CandyBox2LocationData(100023),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_25: CandyBox2LocationData(100024),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_26: CandyBox2LocationData(100025),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_27: CandyBox2LocationData(100026),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_28: CandyBox2LocationData(100027),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_29: CandyBox2LocationData(100028),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_30: CandyBox2LocationData(100029),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_31: CandyBox2LocationData(100030),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_32: CandyBox2LocationData(100031),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_33: CandyBox2LocationData(100032),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_34: CandyBox2LocationData(100033),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_35: CandyBox2LocationData(100034),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_36: CandyBox2LocationData(100035),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_37: CandyBox2LocationData(100036),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_38: CandyBox2LocationData(100037),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_39: CandyBox2LocationData(100038),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_40: CandyBox2LocationData(100039),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_41: CandyBox2LocationData(100040),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_42: CandyBox2LocationData(100041),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_43: CandyBox2LocationData(100042),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_44: CandyBox2LocationData(100043),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_45: CandyBox2LocationData(100044),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_46: CandyBox2LocationData(100045),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_47: CandyBox2LocationData(100046),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_48: CandyBox2LocationData(100047),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_49: CandyBox2LocationData(100048),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_50: CandyBox2LocationData(100049),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_51: CandyBox2LocationData(100050),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_52: CandyBox2LocationData(100051),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_53: CandyBox2LocationData(100052),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_54: CandyBox2LocationData(100053),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_55: CandyBox2LocationData(100054),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_56: CandyBox2LocationData(100055),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_57: CandyBox2LocationData(100056),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_58: CandyBox2LocationData(100057),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_59: CandyBox2LocationData(100058),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_60: CandyBox2LocationData(100059),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_61: CandyBox2LocationData(100060),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_62: CandyBox2LocationData(100061),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_63: CandyBox2LocationData(100062),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_64: CandyBox2LocationData(100063),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_65: CandyBox2LocationData(100064),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_66: CandyBox2LocationData(100065),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_67: CandyBox2LocationData(100066),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_68: CandyBox2LocationData(100067),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_69: CandyBox2LocationData(100068),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_70: CandyBox2LocationData(100069),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_71: CandyBox2LocationData(100070),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_72: CandyBox2LocationData(100071),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_73: CandyBox2LocationData(100072),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_74: CandyBox2LocationData(100073),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_75: CandyBox2LocationData(100074),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_76: CandyBox2LocationData(100075),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_77: CandyBox2LocationData(100076),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_78: CandyBox2LocationData(100077),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_79: CandyBox2LocationData(100078),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_80: CandyBox2LocationData(100079),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_81: CandyBox2LocationData(100080),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_82: CandyBox2LocationData(100081),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_83: CandyBox2LocationData(100082),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_84: CandyBox2LocationData(100083),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_85: CandyBox2LocationData(100084),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_86: CandyBox2LocationData(100085),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_87: CandyBox2LocationData(100086),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_88: CandyBox2LocationData(100087),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_89: CandyBox2LocationData(100088),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_90: CandyBox2LocationData(100089),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_91: CandyBox2LocationData(100090),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_92: CandyBox2LocationData(100091),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_93: CandyBox2LocationData(100092),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_94: CandyBox2LocationData(100093),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_95: CandyBox2LocationData(100094),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_96: CandyBox2LocationData(100095),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_97: CandyBox2LocationData(100096),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_98: CandyBox2LocationData(100097),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_99: CandyBox2LocationData(100098),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_100: CandyBox2LocationData(100099),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_101: CandyBox2LocationData(100100),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_102: CandyBox2LocationData(100101),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_103: CandyBox2LocationData(100102),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_104: CandyBox2LocationData(100103),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_105: CandyBox2LocationData(100104),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_106: CandyBox2LocationData(100105),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_107: CandyBox2LocationData(100106),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_108: CandyBox2LocationData(100107),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_109: CandyBox2LocationData(100108),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_110: CandyBox2LocationData(100109),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_111: CandyBox2LocationData(100110),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_112: CandyBox2LocationData(100111),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_113: CandyBox2LocationData(100112),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_114: CandyBox2LocationData(100113),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_115: CandyBox2LocationData(100114),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_116: CandyBox2LocationData(100115),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_117: CandyBox2LocationData(100116),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_118: CandyBox2LocationData(100117),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_119: CandyBox2LocationData(100118),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_120: CandyBox2LocationData(100119),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_121: CandyBox2LocationData(100120),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_122: CandyBox2LocationData(100121),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_123: CandyBox2LocationData(100122),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_124: CandyBox2LocationData(100123),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_125: CandyBox2LocationData(100124),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_126: CandyBox2LocationData(100125),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_127: CandyBox2LocationData(100126),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_128: CandyBox2LocationData(100127),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_129: CandyBox2LocationData(100128),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_130: CandyBox2LocationData(100129),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_131: CandyBox2LocationData(100130),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_132: CandyBox2LocationData(100131),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_133: CandyBox2LocationData(100132),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_134: CandyBox2LocationData(100133),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_135: CandyBox2LocationData(100134),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_136: CandyBox2LocationData(100135),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_137: CandyBox2LocationData(100136),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_138: CandyBox2LocationData(100137),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_139: CandyBox2LocationData(100138),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_140: CandyBox2LocationData(100139),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_141: CandyBox2LocationData(100140),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_142: CandyBox2LocationData(100141),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_143: CandyBox2LocationData(100142),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_144: CandyBox2LocationData(100143),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_145: CandyBox2LocationData(100144),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_146: CandyBox2LocationData(100145),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_147: CandyBox2LocationData(100146),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_148: CandyBox2LocationData(100147),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_149: CandyBox2LocationData(100148),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_150: CandyBox2LocationData(100149),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_151: CandyBox2LocationData(100150),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_152: CandyBox2LocationData(100151),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_153: CandyBox2LocationData(100152),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_154: CandyBox2LocationData(100153),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_155: CandyBox2LocationData(100154),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_156: CandyBox2LocationData(100155),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_157: CandyBox2LocationData(100156),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_158: CandyBox2LocationData(100157),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_159: CandyBox2LocationData(100158),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_160: CandyBox2LocationData(100159),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_161: CandyBox2LocationData(100160),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_162: CandyBox2LocationData(100161),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_163: CandyBox2LocationData(100162),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_164: CandyBox2LocationData(100163),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_165: CandyBox2LocationData(100164),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_166: CandyBox2LocationData(100165),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_167: CandyBox2LocationData(100166),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_168: CandyBox2LocationData(100167),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_169: CandyBox2LocationData(100168),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_170: CandyBox2LocationData(100169),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_171: CandyBox2LocationData(100170),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_172: CandyBox2LocationData(100171),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_173: CandyBox2LocationData(100172),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_174: CandyBox2LocationData(100173),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_175: CandyBox2LocationData(100174),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_176: CandyBox2LocationData(100175),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_177: CandyBox2LocationData(100176),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_178: CandyBox2LocationData(100177),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_179: CandyBox2LocationData(100178),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_180: CandyBox2LocationData(100179),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_181: CandyBox2LocationData(100180),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_182: CandyBox2LocationData(100181),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_183: CandyBox2LocationData(100182),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_184: CandyBox2LocationData(100183),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_185: CandyBox2LocationData(100184),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_186: CandyBox2LocationData(100185),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_187: CandyBox2LocationData(100186),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_188: CandyBox2LocationData(100187),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_189: CandyBox2LocationData(100188),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_190: CandyBox2LocationData(100189),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_191: CandyBox2LocationData(100190),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_192: CandyBox2LocationData(100191),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_193: CandyBox2LocationData(100192),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_194: CandyBox2LocationData(100193),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_195: CandyBox2LocationData(100194),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_196: CandyBox2LocationData(100195),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_197: CandyBox2LocationData(100196),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_198: CandyBox2LocationData(100197),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_199: CandyBox2LocationData(100198),
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_200: CandyBox2LocationData(100199),
    CandyBox2LocationName.THE_SEA_EXTRA_1: CandyBox2LocationData(101000),
    CandyBox2LocationName.THE_SEA_EXTRA_2: CandyBox2LocationData(101001),
    CandyBox2LocationName.THE_SEA_EXTRA_3: CandyBox2LocationData(101002),
    CandyBox2LocationName.THE_SEA_EXTRA_4: CandyBox2LocationData(101003),
    CandyBox2LocationName.THE_SEA_EXTRA_5: CandyBox2LocationData(101004),
    CandyBox2LocationName.THE_SEA_EXTRA_6: CandyBox2LocationData(101005),
    CandyBox2LocationName.THE_SEA_EXTRA_7: CandyBox2LocationData(101006),
    CandyBox2LocationName.THE_SEA_EXTRA_8: CandyBox2LocationData(101007),
    CandyBox2LocationName.THE_SEA_EXTRA_9: CandyBox2LocationData(101008),
    CandyBox2LocationName.THE_SEA_EXTRA_10: CandyBox2LocationData(101009),
    CandyBox2LocationName.THE_SEA_EXTRA_11: CandyBox2LocationData(101010),
    CandyBox2LocationName.THE_SEA_EXTRA_12: CandyBox2LocationData(101011),
    CandyBox2LocationName.THE_SEA_EXTRA_13: CandyBox2LocationData(101012),
    CandyBox2LocationName.THE_SEA_EXTRA_14: CandyBox2LocationData(101013),
    CandyBox2LocationName.THE_SEA_EXTRA_15: CandyBox2LocationData(101014),
    CandyBox2LocationName.THE_SEA_EXTRA_16: CandyBox2LocationData(101015),
    CandyBox2LocationName.THE_SEA_EXTRA_17: CandyBox2LocationData(101016),
    CandyBox2LocationName.THE_SEA_EXTRA_18: CandyBox2LocationData(101017),
    CandyBox2LocationName.THE_SEA_EXTRA_19: CandyBox2LocationData(101018),
    CandyBox2LocationName.THE_SEA_EXTRA_20: CandyBox2LocationData(101019),
    CandyBox2LocationName.THE_SEA_EXTRA_21: CandyBox2LocationData(101020),
    CandyBox2LocationName.THE_SEA_EXTRA_22: CandyBox2LocationData(101021),
    CandyBox2LocationName.THE_SEA_EXTRA_23: CandyBox2LocationData(101022),
    CandyBox2LocationName.THE_SEA_EXTRA_24: CandyBox2LocationData(101023),
    CandyBox2LocationName.THE_SEA_EXTRA_25: CandyBox2LocationData(101024),
    CandyBox2LocationName.THE_SEA_EXTRA_26: CandyBox2LocationData(101025),
    CandyBox2LocationName.THE_SEA_EXTRA_27: CandyBox2LocationData(101026),
    CandyBox2LocationName.THE_SEA_EXTRA_28: CandyBox2LocationData(101027),
    CandyBox2LocationName.THE_SEA_EXTRA_29: CandyBox2LocationData(101028),
    CandyBox2LocationName.THE_SEA_EXTRA_30: CandyBox2LocationData(101029),
    CandyBox2LocationName.THE_SEA_EXTRA_31: CandyBox2LocationData(101030),
    CandyBox2LocationName.THE_SEA_EXTRA_32: CandyBox2LocationData(101031),
    CandyBox2LocationName.THE_SEA_EXTRA_33: CandyBox2LocationData(101032),
    CandyBox2LocationName.THE_SEA_EXTRA_34: CandyBox2LocationData(101033),
    CandyBox2LocationName.THE_SEA_EXTRA_35: CandyBox2LocationData(101034),
    CandyBox2LocationName.THE_SEA_EXTRA_36: CandyBox2LocationData(101035),
    CandyBox2LocationName.THE_SEA_EXTRA_37: CandyBox2LocationData(101036),
    CandyBox2LocationName.THE_SEA_EXTRA_38: CandyBox2LocationData(101037),
    CandyBox2LocationName.THE_SEA_EXTRA_39: CandyBox2LocationData(101038),
    CandyBox2LocationName.THE_SEA_EXTRA_40: CandyBox2LocationData(101039),
    CandyBox2LocationName.THE_SEA_EXTRA_41: CandyBox2LocationData(101040),
    CandyBox2LocationName.THE_SEA_EXTRA_42: CandyBox2LocationData(101041),
    CandyBox2LocationName.THE_SEA_EXTRA_43: CandyBox2LocationData(101042),
    CandyBox2LocationName.THE_SEA_EXTRA_44: CandyBox2LocationData(101043),
    CandyBox2LocationName.THE_SEA_EXTRA_45: CandyBox2LocationData(101044),
    CandyBox2LocationName.THE_SEA_EXTRA_46: CandyBox2LocationData(101045),
    CandyBox2LocationName.THE_SEA_EXTRA_47: CandyBox2LocationData(101046),
    CandyBox2LocationName.THE_SEA_EXTRA_48: CandyBox2LocationData(101047),
    CandyBox2LocationName.THE_SEA_EXTRA_49: CandyBox2LocationData(101048),
    CandyBox2LocationName.THE_SEA_EXTRA_50: CandyBox2LocationData(101049),
    CandyBox2LocationName.THE_SEA_EXTRA_51: CandyBox2LocationData(101050),
    CandyBox2LocationName.THE_SEA_EXTRA_52: CandyBox2LocationData(101051),
    CandyBox2LocationName.THE_SEA_EXTRA_53: CandyBox2LocationData(101052),
    CandyBox2LocationName.THE_SEA_EXTRA_54: CandyBox2LocationData(101053),
    CandyBox2LocationName.THE_SEA_EXTRA_55: CandyBox2LocationData(101054),
    CandyBox2LocationName.THE_SEA_EXTRA_56: CandyBox2LocationData(101055),
    CandyBox2LocationName.THE_SEA_EXTRA_57: CandyBox2LocationData(101056),
    CandyBox2LocationName.THE_SEA_EXTRA_58: CandyBox2LocationData(101057),
    CandyBox2LocationName.THE_SEA_EXTRA_59: CandyBox2LocationData(101058),
    CandyBox2LocationName.THE_SEA_EXTRA_60: CandyBox2LocationData(101059),
    CandyBox2LocationName.THE_SEA_EXTRA_61: CandyBox2LocationData(101060),
    CandyBox2LocationName.THE_SEA_EXTRA_62: CandyBox2LocationData(101061),
    CandyBox2LocationName.THE_SEA_EXTRA_63: CandyBox2LocationData(101062),
    CandyBox2LocationName.THE_SEA_EXTRA_64: CandyBox2LocationData(101063),
    CandyBox2LocationName.THE_SEA_EXTRA_65: CandyBox2LocationData(101064),
    CandyBox2LocationName.THE_SEA_EXTRA_66: CandyBox2LocationData(101065),
    CandyBox2LocationName.THE_SEA_EXTRA_67: CandyBox2LocationData(101066),
    CandyBox2LocationName.THE_SEA_EXTRA_68: CandyBox2LocationData(101067),
    CandyBox2LocationName.THE_SEA_EXTRA_69: CandyBox2LocationData(101068),
    CandyBox2LocationName.THE_SEA_EXTRA_70: CandyBox2LocationData(101069),
    CandyBox2LocationName.THE_SEA_EXTRA_71: CandyBox2LocationData(101070),
    CandyBox2LocationName.THE_SEA_EXTRA_72: CandyBox2LocationData(101071),
    CandyBox2LocationName.THE_SEA_EXTRA_73: CandyBox2LocationData(101072),
    CandyBox2LocationName.THE_SEA_EXTRA_74: CandyBox2LocationData(101073),
    CandyBox2LocationName.THE_SEA_EXTRA_75: CandyBox2LocationData(101074),
    CandyBox2LocationName.THE_SEA_EXTRA_76: CandyBox2LocationData(101075),
    CandyBox2LocationName.THE_SEA_EXTRA_77: CandyBox2LocationData(101076),
    CandyBox2LocationName.THE_SEA_EXTRA_78: CandyBox2LocationData(101077),
    CandyBox2LocationName.THE_SEA_EXTRA_79: CandyBox2LocationData(101078),
    CandyBox2LocationName.THE_SEA_EXTRA_80: CandyBox2LocationData(101079),
}

lollipop_farm_filler_locations = [
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_1,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_2,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_3,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_4,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_5,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_6,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_7,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_8,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_9,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_10,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_11,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_12,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_13,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_14,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_15,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_16,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_17,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_18,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_19,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_20,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_21,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_22,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_23,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_24,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_25,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_26,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_27,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_28,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_29,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_30,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_31,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_32,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_33,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_34,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_35,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_36,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_37,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_38,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_39,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_40,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_41,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_42,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_43,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_44,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_45,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_46,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_47,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_48,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_49,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_50,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_51,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_52,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_53,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_54,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_55,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_56,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_57,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_58,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_59,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_60,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_61,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_62,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_63,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_64,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_65,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_66,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_67,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_68,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_69,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_70,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_71,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_72,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_73,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_74,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_75,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_76,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_77,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_78,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_79,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_80,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_81,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_82,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_83,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_84,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_85,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_86,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_87,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_88,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_89,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_90,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_91,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_92,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_93,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_94,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_95,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_96,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_97,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_98,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_99,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_100,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_101,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_102,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_103,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_104,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_105,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_106,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_107,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_108,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_109,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_110,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_111,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_112,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_113,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_114,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_115,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_116,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_117,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_118,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_119,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_120,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_121,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_122,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_123,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_124,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_125,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_126,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_127,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_128,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_129,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_130,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_131,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_132,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_133,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_134,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_135,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_136,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_137,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_138,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_139,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_140,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_141,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_142,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_143,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_144,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_145,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_146,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_147,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_148,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_149,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_150,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_151,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_152,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_153,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_154,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_155,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_156,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_157,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_158,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_159,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_160,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_161,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_162,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_163,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_164,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_165,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_166,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_167,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_168,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_169,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_170,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_171,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_172,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_173,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_174,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_175,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_176,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_177,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_178,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_179,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_180,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_181,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_182,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_183,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_184,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_185,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_186,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_187,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_188,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_189,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_190,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_191,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_192,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_193,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_194,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_195,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_196,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_197,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_198,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_199,
    CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_200,
]

the_sea_filler_locations = [
    CandyBox2LocationName.THE_SEA_EXTRA_1,
    CandyBox2LocationName.THE_SEA_EXTRA_2,
    CandyBox2LocationName.THE_SEA_EXTRA_3,
    CandyBox2LocationName.THE_SEA_EXTRA_4,
    CandyBox2LocationName.THE_SEA_EXTRA_5,
    CandyBox2LocationName.THE_SEA_EXTRA_6,
    CandyBox2LocationName.THE_SEA_EXTRA_7,
    CandyBox2LocationName.THE_SEA_EXTRA_8,
    CandyBox2LocationName.THE_SEA_EXTRA_9,
    CandyBox2LocationName.THE_SEA_EXTRA_10,
    CandyBox2LocationName.THE_SEA_EXTRA_11,
    CandyBox2LocationName.THE_SEA_EXTRA_12,
    CandyBox2LocationName.THE_SEA_EXTRA_13,
    CandyBox2LocationName.THE_SEA_EXTRA_14,
    CandyBox2LocationName.THE_SEA_EXTRA_15,
    CandyBox2LocationName.THE_SEA_EXTRA_16,
    CandyBox2LocationName.THE_SEA_EXTRA_17,
    CandyBox2LocationName.THE_SEA_EXTRA_18,
    CandyBox2LocationName.THE_SEA_EXTRA_19,
    CandyBox2LocationName.THE_SEA_EXTRA_20,
    CandyBox2LocationName.THE_SEA_EXTRA_21,
    CandyBox2LocationName.THE_SEA_EXTRA_22,
    CandyBox2LocationName.THE_SEA_EXTRA_23,
    CandyBox2LocationName.THE_SEA_EXTRA_24,
    CandyBox2LocationName.THE_SEA_EXTRA_25,
    CandyBox2LocationName.THE_SEA_EXTRA_26,
    CandyBox2LocationName.THE_SEA_EXTRA_27,
    CandyBox2LocationName.THE_SEA_EXTRA_28,
    CandyBox2LocationName.THE_SEA_EXTRA_29,
    CandyBox2LocationName.THE_SEA_EXTRA_30,
    CandyBox2LocationName.THE_SEA_EXTRA_31,
    CandyBox2LocationName.THE_SEA_EXTRA_32,
    CandyBox2LocationName.THE_SEA_EXTRA_33,
    CandyBox2LocationName.THE_SEA_EXTRA_34,
    CandyBox2LocationName.THE_SEA_EXTRA_35,
    CandyBox2LocationName.THE_SEA_EXTRA_36,
    CandyBox2LocationName.THE_SEA_EXTRA_37,
    CandyBox2LocationName.THE_SEA_EXTRA_38,
    CandyBox2LocationName.THE_SEA_EXTRA_39,
    CandyBox2LocationName.THE_SEA_EXTRA_40,
    CandyBox2LocationName.THE_SEA_EXTRA_41,
    CandyBox2LocationName.THE_SEA_EXTRA_42,
    CandyBox2LocationName.THE_SEA_EXTRA_43,
    CandyBox2LocationName.THE_SEA_EXTRA_44,
    CandyBox2LocationName.THE_SEA_EXTRA_45,
    CandyBox2LocationName.THE_SEA_EXTRA_46,
    CandyBox2LocationName.THE_SEA_EXTRA_47,
    CandyBox2LocationName.THE_SEA_EXTRA_48,
    CandyBox2LocationName.THE_SEA_EXTRA_49,
    CandyBox2LocationName.THE_SEA_EXTRA_50,
    CandyBox2LocationName.THE_SEA_EXTRA_51,
    CandyBox2LocationName.THE_SEA_EXTRA_52,
    CandyBox2LocationName.THE_SEA_EXTRA_53,
    CandyBox2LocationName.THE_SEA_EXTRA_54,
    CandyBox2LocationName.THE_SEA_EXTRA_55,
    CandyBox2LocationName.THE_SEA_EXTRA_56,
    CandyBox2LocationName.THE_SEA_EXTRA_57,
    CandyBox2LocationName.THE_SEA_EXTRA_58,
    CandyBox2LocationName.THE_SEA_EXTRA_59,
    CandyBox2LocationName.THE_SEA_EXTRA_60,
    CandyBox2LocationName.THE_SEA_EXTRA_61,
    CandyBox2LocationName.THE_SEA_EXTRA_62,
    CandyBox2LocationName.THE_SEA_EXTRA_63,
    CandyBox2LocationName.THE_SEA_EXTRA_64,
    CandyBox2LocationName.THE_SEA_EXTRA_65,
    CandyBox2LocationName.THE_SEA_EXTRA_66,
    CandyBox2LocationName.THE_SEA_EXTRA_67,
    CandyBox2LocationName.THE_SEA_EXTRA_68,
    CandyBox2LocationName.THE_SEA_EXTRA_69,
    CandyBox2LocationName.THE_SEA_EXTRA_70,
    CandyBox2LocationName.THE_SEA_EXTRA_71,
    CandyBox2LocationName.THE_SEA_EXTRA_72,
    CandyBox2LocationName.THE_SEA_EXTRA_73,
    CandyBox2LocationName.THE_SEA_EXTRA_74,
    CandyBox2LocationName.THE_SEA_EXTRA_75,
    CandyBox2LocationName.THE_SEA_EXTRA_76,
    CandyBox2LocationName.THE_SEA_EXTRA_77,
    CandyBox2LocationName.THE_SEA_EXTRA_78,
    CandyBox2LocationName.THE_SEA_EXTRA_79,
    CandyBox2LocationName.THE_SEA_EXTRA_80,
]

filler_locations = [
    *lollipop_farm_filler_locations,
    *the_sea_filler_locations
]

def generate_filter_categories():
    lollipop_farm = lollipop_farm_filler_locations.copy()
    the_sea = the_sea_filler_locations.copy()

    return [
        # Make the lollipop farm more likely
        lollipop_farm,
        lollipop_farm,
        the_sea
    ]

def extra_location_count(world: "CandyBox2World"):
    extras = 0
    extras += world.font_traps

    if world.grimoires == 2:
        # Individual spells add extra locations for each extra spell that can be obtained
        extras += 4

    if world.options.goal_conditions.value[GoalConditions.PLAY_STONES] == 0:
        # We don't have the talking candy location, but we still have the item
        extras -= 1

    return extras

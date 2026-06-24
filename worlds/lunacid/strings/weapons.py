from typing import List


class Weapon:
    axe_of_harming = "Axe of Harming"
    battle_axe = "Battle Axe"
    blade_of_jusztina = "Blade of Jusztina"
    blade_of_ophelia = "Blade of Ophelia"
    blessed_wind = "Blessed Wind"
    broken_hilt = "Broken Hilt"
    broken_lance = "Broken Lance"
    corrupted_dagger = "Corrupted Dagger"
    dark_rapier = "Dark Rapier"
    elfen_bow = "Elfen Bow"
    elfen_sword = "Elfen Sword"
    fishing_spear = "Fishing Spear"
    marauder_black_flail = "Marauder Black Flail"
    halberd = "Halberd"
    iron_claw = "Iron Claw"
    moonlight = "Moonlight"
    obsidian_seal = "Obsidian Seal"
    replica_sword = "Replica Sword"
    ritual_dagger = "Ritual Dagger"
    rusted_sword = "Rusted Sword"
    serpent_fang = "Serpent Fang"
    shadow_blade = "Shadow Blade"
    steel_spear = "Steel Spear"
    stone_club = "Stone Club"
    torch = "Torch"
    twisted_staff = "Twisted Staff"
    vampire_hunter_sword = "Vampire Hunter Sword"
    wand_of_power = "Wand of Power"
    wolfram_greatsword = "Wolfram Greatsword"
    wooden_shield = "Wooden Shield"
    crossbow = "Crossbow"
    steel_needle = "Steel Needle"
    hammer_of_cruelty = "Hammer of Cruelty"
    lucid_blade = "Lucid Blade"

    jotunn_slayer = "Jotunn Slayer"
    rapier = "Rapier"
    privateer_musket = "Privateer Musket"

    brittle_arming_sword = "Brittle Arming Sword"
    golden_kopesh = "Golden Khopesh"
    golden_sickle = "Golden Sickle"
    ice_sickle = "Ice Sickle"
    jailor_candle = "Jailor's Candle"
    obsidian_cursebrand = "Obsidian Cursebrand"
    obsidian_poisonguard = "Obsidian Poisonguard"
    skeleton_axe = "Skeleton Axe"
    sucsarian_dagger = "Sucsarian Dagger"
    sucsarian_spear = "Sucsarian Spear"
    cursed_blade = "Cursed Blade"
    lyrian_longsword = "Lyrian Longsword"

    dark_greatsword = "Dark Greatsword"
    shining_blade = "Shining Blade"
    poison_claw = "Poison Claw"
    iron_club = "Iron Club"
    iron_torch = "Iron Torch"
    fire_sword = "Fire Sword"
    steel_lance = "Steel Lance"
    double_crossbow = "Double Crossbow"
    death_scythe = "Death Scythe"
    elfen_longsword = "Elfen Longsword"
    flail = "Flail"
    steel_claw = "Steel Claw"
    steel_club = "Steel Club"
    lyrian_greatsword = "Lyrian Greatsword"
    saint_ishii = "Saint Ishii"
    silver_rapier = "Silver Rapier"
    heritage_sword = "Heritage Sword"

    limbo = "Limbo"

    thorn = "Thorn"
    ghost_sword = "Ghost Sword"

    base_weapons = [replica_sword, torch, ritual_dagger, wooden_shield, stone_club, steel_spear, battle_axe,
                    broken_hilt, corrupted_dagger, dark_rapier, halberd, blade_of_jusztina,
                    twisted_staff, vampire_hunter_sword, elfen_bow, elfen_sword, wolfram_greatsword,
                    axe_of_harming, wand_of_power, blade_of_ophelia, marauder_black_flail,
                    blessed_wind, iron_claw, moonlight, broken_lance, fishing_spear, hammer_of_cruelty,
                    obsidian_seal, shadow_blade, serpent_fang, lucid_blade, thorn, ghost_sword
                    ]

    shop_weapons = [rapier, crossbow, jotunn_slayer, privateer_musket, steel_needle]

    drop_weapons = [rusted_sword, ice_sickle, skeleton_axe, cursed_blade, obsidian_cursebrand,
                    obsidian_poisonguard, golden_kopesh, golden_sickle, brittle_arming_sword,
                    jailor_candle, lyrian_longsword, sucsarian_spear, sucsarian_dagger,
                    ]

    quenchsanity_weapons = [dark_greatsword, silver_rapier, shining_blade, poison_claw, iron_club, iron_torch, fire_sword, steel_lance, double_crossbow,
                            elfen_longsword, steel_claw, steel_club, lyrian_greatsword, saint_ishii, heritage_sword]

    quenchable_weapons = [replica_sword, torch, stone_club, broken_hilt, elfen_sword, wolfram_greatsword,
                          iron_claw, broken_lance, obsidian_seal, shadow_blade, obsidian_cursebrand, obsidian_poisonguard, brittle_arming_sword,
                          lyrian_longsword, iron_club, steel_claw, rapier, crossbow, rusted_sword,
                          shining_blade,
                          ]

    long_weapons: List[str] = [axe_of_harming, blade_of_ophelia, blessed_wind, brittle_arming_sword, broken_lance, dark_greatsword, dark_rapier, elfen_longsword,
                    golden_kopesh, halberd, jotunn_slayer, lyrian_greatsword, marauder_black_flail, obsidian_cursebrand, shining_blade, silver_rapier,
                    skeleton_axe, steel_club, steel_lance, steel_needle, steel_spear, stone_club, sucsarian_spear, thorn, vampire_hunter_sword,
                    wolfram_greatsword]
    long_quenchable_weapon: List[str] = [iron_club, rapier, rusted_sword, shadow_blade, ]


class SpookyWeapon:
    cavalry_saber = "Cavalry Saber"

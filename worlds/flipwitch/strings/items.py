
class QuestItem:
    fairy_bubble = "Fairy Bubble"
    cowbell = "Belle's Cowbell"
    goblin_headshot = "Goblin Headshot"
    business_card = "Business Card"
    gobliana_luggage = "Gobliana's Luggage"
    summon_stone = "Summon Stone"
    delicious_milk = "Delicious Milk"
    belle_milkshake = "Belle's Milkshake"
    cherry_key = "Cherry Apartment Key"
    mono_password = "Momo Server Admin Password"
    clothes = "Bundle of Clothes"
    heavenly_daikon = "Heavenly Daikon"
    hellish_dango = "Hellish Dango"
    soul_fragment = "Soul Fragment"
    legendary_halo = "Legendary Halo"
    demonic_letter = "Demon Letter"
    angelic_letter = "Angel Letter"
    silky_slime = "Silky Slime"
    red_wine = "Red Wine"
    blue_jelly_mushroom = "Blue Jelly Mushroom"
    maid_contract = "Maid Contract"
    deed = "Deed to Fungal Forest"
    mimic_chest = "Mimic Chest Key"
    fungal = "Fungal Key"
    goblin_apartment = "Goblin Apartment Key"
    vip_key = "VIP Key"


class Power:
    bomb = "Goblin Bomb"
    frilly_panties = "Frilly Panties"
    disarming_bell = "Disarming Bell"
    ghost_form = "Ghost Form"
    slime_form = "Slime Form"
    harpy_feather = "Harpy Feather"
    magical_mushroom = "Magical Mushroom"
    slime_sentry = "Slime Sentry"
    ring_of_the_moon = "Ring Of The Moon"
    ring_of_the_sun = "Ring Of The Sun"
    haunted_scythe = "Haunted Scythe"
    demonic_cuff = "Demonic Cuff"


class Accessory:
    fortune_cat = "Fortune Cat"
    heart_necklace = "Heart Necklace"
    star_bracelet = "Star Bracelet"
    magnetic_hairpin = "Magnetic Hairpin"
    yellow_frog_talisman = "Yellow Frog Talisman"
    blue_frog_talisman = "Blue Frog Talisman"
    sacrificial_dagger = "Sacrificial Dagger"
    mind_mushroom = "Mind Mushroom"
    flutterknife_garter = "Flutterknife Garter"
    cursed_talisman = "Cursed Talisman"


class Upgrade:
    health = "Health Upgrade" #10 of these
    mana = "Mana Upgrade" #10 of these
    wand = "Wand Upgrade"
    barrier = "Protective Barrier Upgrade"
    peachy_peach = "Peachy Peach Charge"
    peachy_upgrade = "Peachy Peach Upgrade"
    bewitched_bubble = "Bewitched Bubble"
    # goblin_crystal = "Goblin Crystal"
    # portable_portal = "Portable Portal"
    demon_wings = "Demon Wings"
    angel_feathers = "Angel Feathers"
    mermaid_scale = "Mermaid Scale"
    rose_ribbon = "Rose Ribbon"  # Use Rose Cutters
    orb_of_avoidance = "Orb of Avoidance"  # Use Arcane Cannon


class Coin:
    lucky_coin = "Lucky Coin"
    animal_coin = "Animal Coin"
    bunny_coin = "Bunny Coin"
    angel_demon_coin = "Angel & Demon Coin"
    monster_coin = "Monster Coin"
    promotional_coin = "Promotional Coin"
    loose_change = "Loose Change"

    lucky_coins = [animal_coin, bunny_coin, angel_demon_coin, monster_coin, promotional_coin]


class Warp:
    sensei = "Sensei's Hut Teleport"
    witchy = "Witchy Woods Teleport"
    goblin = "Goblin Caves Teleport"
    spirit = "Spirit City Teleport"
    shady = "Shady Alley Teleport"
    ghost_entrance = "Ghost Castle Entrance Teleport"
    ghost_castle = "Ghost Castle Teleport"
    jigoku = "Jigoku Teleport"
    club_demon = "Club Demon Teleport"
    tengoku = "Tengoku Teleport"
    angelic_hallway = "Angelic Hallway Teleport"
    fungal_forest = "Fungal Forest Teleport"
    slime_citadel = "Slime Citadel Teleport"
    slimy_depths = "Slimy Depths Teleport"
    umi_umi = "Umi Umi Teleport"
    chaos_castle = "Chaos Castle Teleport"

    area_to_warp = {
        0: sensei,
        1: goblin,
        2: spirit,
        3: ghost_castle,
        4: jigoku,
        5: club_demon,
        6: tengoku,
        7: slime_citadel,
        8: umi_umi,
    }


class GachaItem:
    special_promotion = "Special Promotion Figure #1"
    animal_girl_1 = "Animal Girls Figure #1"
    animal_girl_2 = "Animal Girls Figure #2"
    animal_girl_3 = "Animal Girls Figure #3"
    animal_girl_4 = "Animal Girls Figure #4"
    animal_girl_5 = "Animal Girls Figure #5"
    animal_girl_6 = "Animal Girls Figure #6"
    animal_girl_7 = "Animal Girls Figure #7"
    animal_girl_8 = "Animal Girls Figure #8"
    animal_girl_9 = "Animal Girls Figure #9"
    animal_girl_10 = "Animal Girls Figure #10"
    bunny_girl_1 = "Bunny Girls Figure #1"
    bunny_girl_2 = "Bunny Girls Figure #2"
    bunny_girl_3 = "Bunny Girls Figure #3"
    bunny_girl_4 = "Bunny Girls Figure #4"
    bunny_girl_5 = "Bunny Girls Figure #5"
    bunny_girl_6 = "Bunny Girls Figure #6"
    bunny_girl_7 = "Bunny Girls Figure #7"
    bunny_girl_8 = "Bunny Girls Figure #8"
    bunny_girl_9 = "Bunny Girls Figure #9"
    bunny_girl_10 = "Bunny Girls Figure #10"
    angel_demon_1 = "Angels & Demons Figure #1"
    angel_demon_2 = "Angels & Demons Figure #2"
    angel_demon_3 = "Angels & Demons Figure #3"
    angel_demon_4 = "Angels & Demons Figure #4"
    angel_demon_5 = "Angels & Demons Figure #5"
    angel_demon_6 = "Angels & Demons Figure #6"
    angel_demon_7 = "Angels & Demons Figure #7"
    angel_demon_8 = "Angels & Demons Figure #8"
    angel_demon_9 = "Angels & Demons Figure #9"
    angel_demon_10 = "Angels & Demons Figure #10"
    monster_girl_1 = "Monster Girls Figure #1"
    monster_girl_2 = "Monster Girls Figure #2"
    monster_girl_3 = "Monster Girls Figure #3"
    monster_girl_4 = "Monster Girls Figure #4"
    monster_girl_5 = "Monster Girls Figure #5"
    monster_girl_6 = "Monster Girls Figure #6"
    monster_girl_7 = "Monster Girls Figure #7"
    monster_girl_8 = "Monster Girls Figure #8"
    monster_girl_9 = "Monster Girls Figure #9"
    monster_girl_10 = "Monster Girls Figure #10"


class Unlock:
    crystal_block = "Woods Crystal Blockade Removal"
    goblin_crystal_block = "City Crystal Blockade Removal"


class Custom:
    sex_experience = "Sexual Experience"
    hp_heal = "Healing Surge"
    mp_heal = "Mana Surge"
    peach_recharge = "Peachy Peach Recharge"


class Costume:
    navy = "Navy Witch Costume"
    # black_witch = "Black Witch Costume"
    red_wizard = "Red Wizard Costume"
    nun = "Nun Costume"
    priest = "Priest Costume"
    miko = "Miko Costume"
    farmer = "Farmer Costume"
    cat = "Cat Costume"
    goblin = "Goblin Costume"
    maid = "Maid Costume"
    pigman = "Pigman Costume"
    bunny = "Bunny Costume"
    rat = "Rat Costume"
    nurse = "Nurse Costume"
    angler = "Angler Costume"
    dominating = "Dominating Costume"
    postman = "Postman Costume"
    fairy = "Fairy Costume"
    alchemist = "Alchemist Costume"

    female_costumes = [navy, nun, miko, cat, maid, bunny, nurse, dominating, fairy]
    male_costumes = [red_wizard, priest, farmer, goblin, pigman, rat, angler, postman, alchemist]


class Key:
    rundown_house = "Rundown House Key"
    ghostly_castle = "Ghostly Castle Key"
    beast = "The Beast's Key"
    secret_club = "Secret Club Door Key"
    slime_citadel = "Slime Citadel Key"
    frog_boss = "Frog Boss Key"
    goblin_queen = "Goblin Queen Key"
    rose_garden = "Rose Garden Key"
    collapsed_temple = "Collapsed Temple Key"
    demon_boss = "Demon Boss Key"
    slimy_sub_boss = "Slimy Sub Boss Key"
    chaos_sanctum = "Chaos Sanctum Key"
    abandoned_apartment = "Abandoned Apartment Key"
    secret_garden = "Secret Garden Key"
    demon_club = "Demon Club Door Key"
    slime_boss = "Slime Boss Key"
    forgotten_fungal = "Forgotten Fungal Door Key"


class GoalItem:
    chaos_piece = "Chaos Key Piece"


class QuestEventItem:
    goblin_model_1 = "Given Photo"
    goblin_model_2 = "Given Card"
    goblin_model_3 = "Goblin Model Complete"
    queen_defeat = "Goblin Queen Defeated"
    gobliana_luggage_2 = "Got Gobliana's Luggage"

    # SpC
    rover_1 = "Dogs Out Complete"
    rover_3 = "Chewtoy Complete"
    belle_1 = "Cowbell Complete"
    belle_2_a = "Given Milkshake"
    belle_2_b = "Milkshake Complete"
    belle_3 = "Apartment Complete"
    cat_girls_3_a = "Told Ghost Off"
    cat_girls_3_b = "Haunted Bathroom Complete"
    bunny_1 = "Booze Bunny Complete"
    bunny_2 = "Help Wanted Complete"
    kyoni_1 = "Devilicious Complete"
    gobliana_luggage_1 = "Given Apartment Key"
    gobliana_luggage_3 = "Gobliana's Luggage Complete"
    tatil_1 = "Given Tatil Key"

    # GC
    cat_girls_1 = "Panty Raid Complete"

    # Jigoku
    cat_statue_start = "Cat Statue Started"
    cat_statue_1 = "Prayed At Statue 1"
    cat_statue_2 = "Prayed At Statue 2"
    cat_statue_3 = "Prayed At Statue 3"
    goat_guy = "Given Goat Guy Letter"

    # Tengoku
    angel_letter = "Angel Letter Item Given"
    gobliana_photographer = "Hired the Photographer"

    # Fungal Forest
    tatil_2 = "Given Deed"
    stone_start = "Summoning Stone Start"
    stone_1 = "Summoning Stone 1 Item"
    stone_2 = "Summoning Stone 2 Item"
    stone_3 = "Summoning Stone 3 Item"


class Trap:
    nothing = "Nothing"
    sexual_thoughts = "Sexual Thoughts"


hint_base_items = [Power.ghost_form, Power.slime_form, Upgrade.demon_wings, Upgrade.angel_feathers, Upgrade.mermaid_scale, Key.ghostly_castle, Key.secret_garden,
                   Unlock.goblin_crystal_block, Unlock.crystal_block]


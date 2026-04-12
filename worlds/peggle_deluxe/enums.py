import enum


class PeggleDeluxeAPGoals(enum.Enum):
    GOLD_PEGS_FINAL_LEVEL = 0
    GOLD_PEG_HUNT = 1


class PeggleDeluxeAPItems(enum.Enum):
    GOLD_PEG = "Gold Peg"
    BRITTLE_PEG = "Brittle Peg"
    CHIPPED_PEG = "Chipped Peg"
    DENTED_PEG = "Dented Peg"
    HOLLOW_PEG = "Hollow Peg"
    PROGRESSIVE_FEVER_METER = "Progressive Fever Meter Threshold"
    PROGRESSIVE_STARTING_BALL_INCREASE = "Progressive Starting Ball Increase"
    RUSTY_PEG = "Rusty Peg"
    CHARACTER_UNLOCK_BJORN = "Master Unlock: Bjorn"
    CHARACTER_UNLOCK_JIMMY_LIGHTNING = "Master Unlock: Jimmy Lightning"
    CHARACTER_UNLOCK_KAT_TUT = "Master Unlock: Kat Tut"
    CHARACTER_UNLOCK_SPLORK = "Master Unlock: Splork"
    CHARACTER_UNLOCK_CLAUDE = "Master Unlock: Claude"
    CHARACTER_UNLOCK_RENFIELD = "Master Unlock: Renfield"
    CHARACTER_UNLOCK_TULA = "Master Unlock: Tula"
    CHARACTER_UNLOCK_WARREN = "Master Unlock: Warren"
    CHARACTER_UNLOCK_LORD_CINDERBOTTOM = "Master Unlock: Lord Cinderbottom"
    CHARACTER_UNLOCK_MASTER_HU = "Master Unlock: Master Hu"


class PeggleDeluxeAPMasterSelectionModes(enum.Enum):
    SINGLE_MASTER = 0
    MULTIPLE_MASTERS = 1


class PeggleDeluxeAPRequirementModes(enum.Enum):
    SAME_FOR_ALL_LEVELS = 0
    RANDOM_PER_LEVEL = 1


class PeggleDeluxeAPTags(enum.Enum):
    BASEBALL_ITEM = "6-4 Baseball Item"
    BASEBALL_LOCATION = "6-4 Baseball Location"
    BEYOND_REASON_ITEM = "11-5 Beyond Reason Item"
    BEYOND_REASON_LOCATION = "11-5 Beyond Reason Location"
    BILLIONS_AND_BILLIONS_ITEM = "11-3 Billions & Billions Item"
    BILLIONS_AND_BILLIONS_LOCATION = "11-3 Billions & Billions Location"
    BIRDYS_CRIB_ITEM = "2-1 Birdy's Crib Item"
    BIRDYS_CRIB_LOCATION = "2-1 Birdy's Crib Location"
    BJORNS_GAZEBO_ITEM = "1-3 Bjorn's Gazebo Item"
    BJORNS_GAZEBO_LOCATION = "1-3 Bjorn's Gazebo Location"
    BLOCKERS_ITEM = "6-3 Blockers Item"
    BLOCKERS_LOCATION = "6-3 Blockers Location"
    BUFFALO_WINGS_ITEM = "2-2 Buffalo Wings Item"
    BUFFALO_WINGS_LOCATION = "2-2 Buffalo Wings Location"
    CHARACTER_UNLOCK_ITEM = "Character Unlock Item"
    CROCO_GATOR_PIT_ITEM = "3-4 Croco-Gator Pit Item"
    CROCO_GATOR_PIT_LOCATION = "3-4 Croco-Gator Pit Location"
    DAS_BUCKET_ITEM = "1-4 Das Bucket Item"
    DAS_BUCKET_LOCATION = "1-4 Das Bucket Location"
    DOG_PINBALL_ITEM = "8-2 Dog Pinball Item"
    DOG_PINBALL_LOCATION = "8-2 Dog Pinball Location"
    DONT_PANIC_ITEM = "11-4 Don't Panic Item"
    DONT_PANIC_LOCATION = "11-4 Don't Panic Location"
    DOOM_WITH_A_VIEW_ITEM = "9-2 Doom with a View Item"
    DOOM_WITH_A_VIEW_LOCATION = "9-2 Doom with a View Location"
    END_OF_TIME_ITEM = "11-2 End of Time Item"
    END_OF_TIME_LOCATION = "11-2 End of Time Location"
    FEVER_METER_LOCATION = "Fever Meter Location"
    FILLER_ITEM = "Filler Item"
    FIVE_OF_A_KIND_ITEM = "8-5 Five of a Kind Item"
    FIVE_OF_A_KIND_LOCATION = "8-5 Five of a Kind Location"
    FULL_CLEAR_LOCATION = "Full Clear Location"
    GETTING_THE_SPARE_ITEM = "4-5 Getting the Spare Item"
    GETTING_THE_SPARE_LOCATION = "4-5 Getting the Spare Location"
    GOAL_ITEM = "Goal Item"
    HOLLAND_OATS_ITEM = "7-1 Holland Oats Item"
    HOLLAND_OATS_LOCATION = "7-1 Holland Oats Location"
    INFINITE_CHEESE_ITEM = "3-2 Infinite Cheese Item"
    INFINITE_CHEESE_LOCATION = "3-2 Infinite Cheese Location"
    INSANE_AQUARIUM_ITEM = "5-2 Insane Aquarium Item"
    INSANE_AQUARIUM_LOCATION = "5-2 Insane Aquarium Location"
    I_HEART_FLOWERS_ITEM = "7-2 I Heart Flowers Item"
    I_HEART_FLOWERS_LOCATION = "7-2 I Heart Flowers Location"
    LEVEL_CLEAR_LOCATION = "Level Clear Location"
    LEVEL_UNLOCK_ITEM = "Level Unlock Item"
    LOVE_STORY_ITEM = "5-5 Love Story Item"
    LOVE_STORY_LOCATION = "5-5 Love Story Location"
    MAID_IN_SPACE_ITEM = "4-4 Maid in Space Item"
    MAID_IN_SPACE_LOCATION = "4-4 Maid in Space Location"
    MR_PEEPERS_ITEM = "2-5 Mr. Peepers Item"
    MR_PEEPERS_LOCATION = "2-5 Mr. Peepers Location"
    NINE_LUFT_BALLOONS_ITEM = "9-4 9 Luft Balloons Item"
    NINE_LUFT_BALLOONS_LOCATION = "9-4 9 Luft Balloons Location"
    ORANGE_PEG_COMBO_LOCATION = "Orange Peg Combo Location"
    OUR_FAVORITE_EEL_ITEM = "5-4 Our Favorite Eel Item"
    OUR_FAVORITE_EEL_LOCATION = "5-4 Our Favorite Eel Location"
    PAW_READER_ITEM = "11-1 Paw Reader Item"
    PAW_READER_LOCATION = "11-1 Paw Reader Location"
    PEARL_CLAM_ITEM = "5-1 Pearl Clam Item"
    PEARL_CLAM_LOCATION = "5-1 Pearl Clam Location"
    PEGGLELAND_ITEM = "1-1 Peggleland Item"
    PEGGLELAND_LOCATION = "1-1 Peggleland Location"
    PEG_COMBO_LOCATION = "Peg Combo Location"
    PROGRESSIVE_ITEM = "Progressive Item"
    RA_DEAL_ITEM = "3-3 Ra Deal Item"
    RA_DEAL_LOCATION = "3-3 Ra Deal Location"
    RHOMBI_ITEM = "9-3 Rhombi Item"
    RHOMBI_LOCATION = "9-3 Rhombi Location"
    ROLL_EM_ITEM = "8-4 Roll 'Em Item"
    ROLL_EM_LOCATION = "8-4 Roll 'Em Location"
    SCARAB_CRUNCH_ITEM = "3-1 Scarab Crunch Item"
    SCARAB_CRUNCH_LOCATION = "3-1 Scarab Crunch Location"
    SCORE_LOCATION = "Score Location"
    SEVENTY_AND_SUNNY_ITEM = "7-5 70 and Sunny Item"
    SEVENTY_AND_SUNNY_LOCATION = "7-5 70 and Sunny Location"
    SKATE_PARK_ITEM = "2-3 Skate Park Item"
    SKATE_PARK_LOCATION = "2-3 Skate Park Location"
    SLIP_AND_SLIDE_ITEM = "1-2 Slip and Slide Item"
    SLIP_AND_SLIDE_LOCATION = "1-2 Slip and Slide Location"
    SNOW_DAY_ITEM = "1-5 Snow Day Item"
    SNOW_DAY_LOCATION = "1-5 Snow Day Location"
    SPIDERWEB_ITEM = "6-2 Spiderweb Item"
    SPIDERWEB_LOCATION = "6-2 Spiderweb Location"
    SPIN_AGAIN_ITEM = "8-3 Spin Again Item"
    SPIN_AGAIN_LOCATION = "8-3 Spin Again Location"
    SPIN_CYCLE_ITEM = "10-1 Spin Cycle Item"
    SPIN_CYCLE_LOCATION = "10-1 Spin Cycle Location"
    SPIRAL_OF_DOOM_ITEM = "2-4 Spiral of Doom Item"
    SPIRAL_OF_DOOM_LOCATION = "2-4 Spiral of Doom Location"
    STYLE_SHOT_LOCATION = "Style Shot Location"
    TASTY_WAVES_ITEM = "5-3 Tasty Waves Item"
    TASTY_WAVES_LOCATION = "5-3 Tasty Waves Location"
    THE_AMOEBAN_ITEM = "4-1 The Amoeban Item"
    THE_AMOEBAN_LOCATION = "4-1 The Amoeban Location"
    THE_DUDE_ABIDES_ITEM = "10-2 The Dude Abides Item"
    THE_DUDE_ABIDES_LOCATION = "10-2 The Dude Abides Location"
    THE_FEVER_LEVEL_ITEM = "3-5 The Fever Level Item"
    THE_FEVER_LEVEL_LOCATION = "3-5 The Fever Level Location"
    THE_LAST_FLOWER_ITEM = "4-2 The Last Flower Item"
    THE_LAST_FLOWER_LOCATION = "4-2 The Last Flower Location"
    THE_LOVE_MOAT_ITEM = "9-1 The Love Moat Item"
    THE_LOVE_MOAT_LOCATION = "9-1 The Love Moat Location"
    TULAS_RIDE_ITEM = "7-4 Tula's Ride Item"
    TULAS_RIDE_LOCATION = "7-4 Tula's Ride Location"
    TWISTED_SISTERS_ITEM = "9-5 Twisted Sisters Item"
    TWISTED_SISTERS_LOCATION = "9-5 Twisted Sisters Location"
    USEFUL_ITEM = "Useful Item"
    VERMIN_ITEM = "6-5 Vermin Item"
    VERMIN_LOCATION = "6-5 Vermin Location"
    WAVES_ITEM = "6-1 Waves Item"
    WAVES_LOCATION = "6-1 Waves Location"
    WE_COME_IN_PEACE_ITEM = "4-3 We Come in Peace Item"
    WE_COME_IN_PEACE_LOCATION = "4-3 We Come in Peace Location"
    WHEN_PIGS_FLY_ITEM = "10-3 When Pigs Fly Item"
    WHEN_PIGS_FLY_LOCATION = "10-3 When Pigs Fly Location"
    WIN_A_MONKEY_ITEM = "8-1 Win a Monkey Item"
    WIN_A_MONKEY_LOCATION = "8-1 Win a Monkey Location"
    WORKIN_FROM_HOME_ITEM = "7-3 Workin from Home Item"
    WORKIN_FROM_HOME_LOCATION = "7-3 Workin from Home Location"
    YANG_YIN_ITEM = "10-4 Yang, Yin Item"
    YANG_YIN_LOCATION = "10-4 Yang, Yin Location"
    ZEN_FROG_ITEM = "10-5 Zen Frog Item"
    ZEN_FROG_LOCATION = "10-5 Zen Frog Location"


class PeggleDeluxeAPUsefulItems(enum.Enum):
    FEVER_METER_BONUS = "Fever Meter Permanent Bonus"
    FULL_CLEAR_DISCOUNT = "Full Clear Discount"
    SCORE_MULTIPLIER = "Score Multiplier"
    TARGET_SCORE_DISCOUNT = "Target Score Discount"


class PeggleDeluxeCharacters(enum.Enum):
    BJORN = "Bjorn"
    JIMMY_LIGHTNING = "Jimmy Lightning"
    KAT_TUT = "Kat Tut"
    SPLORK = "Splork"
    CLAUDE = "Claude"
    RENFIELD = "Renfield"
    TULA = "Tula"
    WARREN = "Warren"
    LORD_CINDERBOTTOM = "Lord Cinderbottom"
    MASTER_HU = "Master Hu"


class PeggleDeluxeContexts(enum.Enum):
    INVALID = 0
    VALID = 1


class PeggleDeluxeGameModes(enum.Enum):
    OTHER = 0
    ADVENTURE = 1
    QUICK_PLAY = 2
    DUEL = 3
    CHALLENGE = 4
    DEMO = 6


class PeggleDeluxeLevels(enum.Enum):
    PEGGLELAND = "1-1 Peggleland"
    SLIP_AND_SLIDE = "1-2 Slip and Slide"
    BJORNS_GAZEBO = "1-3 Bjorn's Gazebo"
    DAS_BUCKET = "1-4 Das Bucket"
    SNOW_DAY = "1-5 Snow Day"
    BIRDYS_CRIB = "2-1 Birdy's Crib"
    BUFFALO_WINGS = "2-2 Buffalo Wings"
    SKATE_PARK = "2-3 Skate Park"
    SPIRAL_OF_DOOM = "2-4 Spiral of Doom"
    MR_PEEPERS = "2-5 Mr. Peepers"
    SCARAB_CRUNCH = "3-1 Scarab Crunch"
    INFINITE_CHEESE = "3-2 Infinite Cheese"
    RA_DEAL = "3-3 Ra Deal"
    CROCO_GATOR_PIT = "3-4 Croco-Gator Pit"
    THE_FEVER_LEVEL = "3-5 The Fever Level"
    THE_AMOEBAN = "4-1 The Amoeban"
    THE_LAST_FLOWER = "4-2 The Last Flower"
    WE_COME_IN_PEACE = "4-3 We Come in Peace"
    MAID_IN_SPACE = "4-4 Maid in Space"
    GETTING_THE_SPARE = "4-5 Getting the Spare"
    PEARL_CLAM = "5-1 Pearl Clam"
    INSANE_AQUARIUM = "5-2 Insane Aquarium"
    TASTY_WAVES = "5-3 Tasty Waves"
    OUR_FAVORITE_EEL = "5-4 Our Favorite Eel"
    LOVE_STORY = "5-5 Love Story"
    WAVES = "6-1 Waves"
    SPIDERWEB = "6-2 Spiderweb"
    BLOCKERS = "6-3 Blockers"
    BASEBALL = "6-4 Baseball"
    VERMIN = "6-5 Vermin"
    HOLLAND_OATS = "7-1 Holland Oats"
    I_HEART_FLOWERS = "7-2 I Heart Flowers"
    WORKIN_FROM_HOME = "7-3 Workin from Home"
    TULAS_RIDE = "7-4 Tula's Ride"
    SEVENTY_AND_SUNNY = "7-5 70 and Sunny"
    WIN_A_MONKEY = "8-1 Win a Monkey"
    DOG_PINBALL = "8-2 Dog Pinball"
    SPIN_AGAIN = "8-3 Spin Again"
    ROLL_EM = "8-4 Roll 'Em"
    FIVE_OF_A_KIND = "8-5 Five of a Kind"
    THE_LOVE_MOAT = "9-1 The Love Moat"
    DOOM_WITH_A_VIEW = "9-2 Doom with a View"
    RHOMBI = "9-3 Rhombi"
    NINE_LUFT_BALLOONS = "9-4 9 Luft Balloons"
    TWISTED_SISTERS = "9-5 Twisted Sisters"
    SPIN_CYCLE = "10-1 Spin Cycle"
    THE_DUDE_ABIDES = "10-2 The Dude Abides"
    WHEN_PIGS_FLY = "10-3 When Pigs Fly"
    YANG_YIN = "10-4 Yang, Yin"
    ZEN_FROG = "10-5 Zen Frog"
    PAW_READER = "11-1 Paw Reader"
    END_OF_TIME = "11-2 End of Time"
    BILLIONS_AND_BILLIONS = "11-3 Billions & Billions"
    DONT_PANIC = "11-4 Don't Panic"
    BEYOND_REASON = "11-5 Beyond Reason"


class PeggleDeluxeLevelStates(enum.Enum):
    OTHER = 0
    BEFORE_SHOT = 1
    SHOT_ACTIVE = 2
    AFTER_SHOT = 3

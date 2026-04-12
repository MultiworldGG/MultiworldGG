import typing
from dataclasses import dataclass
from Options import Toggle, DefaultOnToggle, Option, Range, Choice, ItemDict, DeathLink, PerGameCommonOptions, OptionGroup

class GoalOptions():
    SORCERESS_ONE = 0
    EGG_FOR_SALE = 1
    SORCERESS_TWO = 2
    ALL_SKILLPOINTS = 3
    EPILOGUE = 4
    SPIKE = 5
    SCORCH = 6
    EGG_HUNT = 7

class LifeBottleOptions():
    OFF = 0
    NORMAL = 1
    HARD = 2

class MoneybagsOptions():
    VANILLA = 0
    COMPANIONSANITY = 1
    # Reserve 2 for shuffling moneybags prices on companions
    MONEYBAGSSANITY = 3

class PowerupLockOptions():
    VANILLA = 0
    TYPE = 1
    INDIVIDUAL = 2

class SparxUpgradeOptions():
    OFF = 0
    BLUE = 1
    GREEN = 2
    SPARXLESS = 3
    TRUE_SPARXLESS = 4

class SparxForGemsOptions():
    OFF = 0
    GREEN_SPARX = 1
    SPARX_FINDER = 2

class GemsanityOptions():
    OFF = 0
    PARTIAL = 1
    FULL_BUNDLES = 2
    FULL = 3
    FULL_GLOBAL = 4

class LevelLockOptions():
    VANILLA = 0
    KEYS = 1
    KEYS_AND_EGGS = 2
    RANDOM_REQS = 3
    ADD_REQS = 4
    ADD_GEM_REQS = 5


class GoalOption(Choice):
    """Lets the user choose the completion goal.
    Sorceress 1 - Beat the sorceress *and* obtain the specified number of eggs.
    Egg For Sale - Chase Moneybags after defeating the sorceress the first time.
    Sorceress 2 - Beat the sorceress in Super Bonus Round *and*
        obtain the specified number of eggs.
    All Skillpoints - Collect all 20 skill points in the game.
        Excluded locations are still required for this goal.
    Epilogue - Unlock the full epilogue by collecting all 20 skill points
        and defeating the sorceress. Excluded locations are still required for this goal.
    Spike - Beat Spike *and* obtain the specified number of eggs.
    Scorch - Beat Scorch *and* obtain the specified number of eggs.
    Egg Hunt - Find the specified number of eggs to win. Portal requirements are reduced."""
    display_name = "Completion Goal"
    default = GoalOptions.SORCERESS_ONE
    option_sorceress_1 = GoalOptions.SORCERESS_ONE
    option_egg_for_sale = GoalOptions.EGG_FOR_SALE
    option_sorceress_2 = GoalOptions.SORCERESS_TWO
    option_all_skillpoints = GoalOptions.ALL_SKILLPOINTS
    option_epilogue = GoalOptions.EPILOGUE
    option_spike = GoalOptions.SPIKE
    option_scorch = GoalOptions.SCORCH
    option_egg_hunt = GoalOptions.EGG_HUNT

class EggCount(Range):
    """The number of eggs needed to win when goal is Sorceress 1,
    Sorceress 2, Spike, Scorch, and Egg Hunt."""
    display_name = "Eggs to Win"
    range_start = 10
    range_end = 150
    default = 100

class PercentExtraEggs(Range):
    """The percentage of extra eggs in the pool for Egg Hunt.
    For example, if 50 eggs are needed and there are 20% extra eggs,
    60 eggs will be in the pool. The total number of available eggs
    caps at 150 regardless of this option. Rounds up."""
    display_name = "Percent Extra Egg Hunt Eggs"
    range_start = 0
    range_end = 50
    default = 25

class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

class OpenWorldOption(Toggle):
    """Grants access to all 4 homeworlds from the start.
    End of level and boss eggs are removed as checks.
    This removes 18 locations from the location pool,
    so you may need to enable additional locations to use this option.
    If Moneybags is Vanilla, companion unlocks will be free.
    Disables world keys."""
    display_name = "Open World Mode"

class LevelLockOption(Choice):
    """Determines the rules for entering levels.
    Sparx levels, companion levels, homeworlds, Super Bonus Round, and bosses
    are not affected by these settings.
    At least one Sunrise level will always start unlocked.
    Some settings give a free egg to ensure correct behavior.
    Some settings prevent non-companion levels from out of bounds.
    Vanilla: Levels have their vanilla unlock requirements.
    Keys: 20 Level Unlock items are added to the item pool.
    Randomize Requirements: Randomizes egg requirements for levels
        that normally require eggs to enter.
    Add Requirements: Any level can have an egg requirement added.
    Add Gem Requirements: Any level can have an egg OR gem requirement added.
        Only works when both Moneybagssanity and Gemsanity are on.
    """
    display_name = "Level Lock Options"
    default = LevelLockOptions.VANILLA
    option_vanilla = LevelLockOptions.VANILLA
    option_keys = LevelLockOptions.KEYS
    option_randomize_requirements = LevelLockOptions.RANDOM_REQS
    option_add_requirements = LevelLockOptions.ADD_REQS
    option_add_gem_requirements = LevelLockOptions.ADD_GEM_REQS

class StartingLevels(Range):
    """When Level Lock Options is not Vanilla or Randomize Requirements,
    determines how many non-companion levels start unlocked.
    The recommended value when Keys are in use is 2 or 3.
    One Sunrise level will always be unlocked."""
    display_name = "Number of Starting Levels"
    range_start = 1
    range_end = 20
    default = 2

class SorceressDoorRequirement(Range):
    """Determines how many eggs are required to open Sorceress' Lair
    in Midnight Mountain.
    NOTE: This only works if Duckstation is set to interpreter mode."""
    display_name = "Eggs to Open Sorceress Door"
    range_start = 1
    range_end = 100
    default = 100

class SBRDoorEggRequirement(Range):
    """Determines how many eggs are required to open Super Bonus Round.
    NOTE: This only works if Duckstation is set to interpreter mode."""
    display_name = "Eggs to Open Super Bonus Round"
    range_start = 1
    range_end = 149
    default = 149

class SBRDoorGemRequirement(Range):
    """Determines how many gems are required to open Super Bonus Round.
    Gem requirements within Super Bonus Round are based on this number.
    NOTE: This only works if Duckstation is set to interpreter mode.
    In game displays may have visual glitches."""
    display_name = "Gems to Open Super Bonus Round"
    range_start = 1
    range_end = 15000
    default = 15000

class Enable25PctGemChecksOption(Toggle):
    """Adds checks for getting 25% of the gems in a level"""
    display_name = "Enable 25% Gem Checks"

class Enable50PctGemChecksOption(Toggle):
    """Adds checks for getting 50% of the gems in a level"""
    display_name = "Enable 50% Gem Checks"

class Enable75PctGemChecksOption(Toggle):
    """Adds checks for getting 75% of the gems in a level"""
    display_name = "Enable 75% Gem Checks"

class EnableGemChecksOption(Toggle):
    """Adds checks for getting all gems in a level"""
    display_name = "Enable 100% Gem Checks"

class EnableTotalGemChecksOption(Toggle):
    """Adds checks for every 500 gems you collect total.
    Gems currently paid to Moneybags do not count towards your total.
    Logic assumes you pay Moneybags everywhere."""
    display_name = "Enable Total Gem Count Checks"

class MaxTotalGemCheckOption(Range):
    """The highest number of total gems that can be required for Total Gem Count checks.
    Has no effect if Enable Total Gem Count Checks is disabled."""
    display_name = "Max for Total Gem Count Checks"
    range_start = 500
    range_end = 20000
    default = 6000

class EnableGemsanityOption(Choice):
    """Adds checks for individual gems.
    If Moneybagssanity is off, Moneybags unlocks become free.
    WARNING: Full gemsanity requires the host to edit allow_full_gemsanity
        in their yaml file.
    Off: Individual gems are not checks.
    Partial: 200 random gems become checks. Adds items giving 50 or 100 gems
        for specific levels to the item pool.
    Full Bundles: Every gem is a check.  Adds items giving 50 or 100 gems
        for specific levels to the item pool.  Adds many filler items."""
    display_name = "Enable Gemsanity"
    default = GemsanityOptions.OFF
    option_off = GemsanityOptions.OFF
    option_partial = GemsanityOptions.PARTIAL
    option_full_bundles = GemsanityOptions.FULL_BUNDLES

class EnableSkillpointChecksOption(Toggle):
    """Adds checks for getting skill points"""
    display_name = "Enable Skillpoint Checks"

class EnableLifeBottleChecksOption(Choice):
    """Adds checks for breaking life bottles.
    Off: Life bottles are not checks.
    Normal: The 26 intended life bottles become checks.
    Hard: Adds the out-of-bounds life bottle in Fireworks Factory to the pool.
    This does not include the 3 bottles on the impossible island in Midnight Mountain."""
    display_name = "Enable Life Bottle Checks"
    default = LifeBottleOptions.OFF
    option_off = LifeBottleOptions.OFF
    option_normal = LifeBottleOptions.NORMAL
    option_hard = LifeBottleOptions.HARD

class SparxPowerSettings(Toggle):
    """Shuffles the Sparx abilities from completing Sparx levels into the item pool.
    Sparx's ability to break baskets becomes 2 progressive items.
    Having both allows atlas warp and breaking vases."""
    display_name = "Sparx Power-sanity Settings"

class EnableDeathLink(DeathLink):
    """Spyro will die when a DeathLink is received.
    Sends DeathLinks on his death.
    Some edge cases may not be handled."""
    display_name = "DeathLink"

class MoneybagsSettings(Choice):
    """Determines settings for Moneybags unlocks.
    Moneybags dialog has small visual errors.
    Defeating the Sorceress bypasses all requirements.
    Vanilla - Pay Moneybags to progress as usual
    Companionsanity - Unlock items replace payment for side characters.
    Moneybagssanity - Unlock items replace payment for Moneybags."""
    display_name = "Moneybags Settings"
    default = MoneybagsOptions.VANILLA
    option_vanilla = MoneybagsOptions.VANILLA
    option_companionsanity = MoneybagsOptions.COMPANIONSANITY
    option_moneybagssanity = MoneybagsOptions.MONEYBAGSSANITY

class PowerupLockSettings(Choice):
    """Powerup gates (such as superflame) require items to use.
    Does not affect the invincibility filler item.
    NOTE: The Sunrise Spring early level entry tricks assume
        you do not need the superfly powerup to complete them!
    Vanilla - Powerups are available at all times.
    Type - Superfly, Fireball, and Invincibility Powerup items are added to the pool.
        Fireworks Factory and Super Bonus Round's combo powerups
        require both Superfly and Fireball to unlock.
    Individual: Each level's powerups are unlocked by a specific item.
    """
    display_name = "Powerup Lock Settings"
    default = PowerupLockOptions.VANILLA
    option_vanilla = PowerupLockOptions.VANILLA
    option_type = PowerupLockOptions.TYPE
    option_individual = PowerupLockOptions.INDIVIDUAL

class EnableWorldKeys(Toggle):
    """Prevents moving to the next homeworld without enough World Key items.
    You must still complete the vanilla requirements to go to the next homeworld.
    Disabled in Open World mode."""
    display_name = "Enable World Keys"

class EnableFillerExtraLives(DefaultOnToggle):
    """Enables filler items that grant extra lives"""
    display_name = "Enable Extra Lives Filler"

class EnableFillerInvincibility(Toggle):
    """Enables filler items that grant temporary invincibility"""
    display_name = "Enable Temporary Invincibility Filler"

class EnableFillerColorChange(Toggle):
    """Enables filler items that change Spyro's color"""
    display_name = "Enable Changing Spyro's Color Filler"

class EnableFillerBigHeadMode(Toggle):
    """Enables filler items that turn on Big Head Mode and Flat Spyro Mode"""
    display_name = "Enable Big Head and Flat Spyro Filler"

class EnableFillerHealSparx(Toggle):
    """Enables filler items that heal Sparx. Can exceed max health."""
    display_name = "Enable (over)healing Sparx Filler"

class TrapFillerPercent(Range):
    """The percent chance that a filler items is a trap."""
    display_name = "Trap Percentage of Filler"
    range_start = 0
    range_end = 100
    default = 0

class EnableTrapDamageSparx(Toggle):
    """Enables traps that damage Sparx. Cannot directly kill Spyro."""
    display_name = "Enable Hurting Sparx Trap"

class EnableTrapSparxless(Toggle):
    """Enables traps that removes Sparx."""
    display_name = "Enable Sparxless Trap"

class EnableProgressiveSparxHealth(Choice):
    """Start the game with less max health.
    Add items to the pool to increase your max health.
    Heal Sparx items have no effect until all items are found.
    Off - The game behaves normally.
    Blue - Your max health starts at blue Sparx.
    Green - Your max health starts at green Sparx.
    Sparxless - Your max health starts at no Sparx.
    True Sparxless - Your max health is permanently Sparxless."""
    display_name = "Enable Progressive Sparx Health Upgrades"
    default = SparxUpgradeOptions.OFF
    option_off = SparxUpgradeOptions.OFF
    option_blue = SparxUpgradeOptions.BLUE
    option_green = SparxUpgradeOptions.GREEN
    option_sparxless = SparxUpgradeOptions.SPARXLESS
    option_true_sparxless = SparxUpgradeOptions.TRUE_SPARXLESS

class ProgressiveSparxHealthLogic(Toggle):
    """Certain Sparx health amounts are expected before
    you are required to enter different levels.
    Super Bonus Round, Crawdad Farm, and levels in Midday and later
    logically require green Sparx.
    Fireworks Factory, Charmed Ridge, and levels in Midnight and later
    logically require blue Sparx.
    Dino Mines and the Sorceress logically require
    gold Sparx.
    The Extra Health item/bonus from Starfish Reef is not considered for this logic.
    Note: This does nothing unless Enable Progressive Sparx
    Health Upgrades is set to blue, green, or Sparxless,"""
    display_name = "Enable Progressive Sparx Health Logic"

class RequireSparxForMaxGems(Choice):
    """Determines the logic for gemsanity and 100% gem checks.
    75% gem checks (100% in levels with no enemies) are always on.
    Off: Sparx max health and abilities do not affect gem logic.
    Green Sparx: Sparx is required.
    Sparx Finder: Sparx Gem Finder is required.
    NOTE: This option is ignored in True Sparxless mode,
    or in Sparxless mode if Progressive Sparx Health Logic is off."""
    display_name = "Require Sparx for Max Gems"
    default = SparxForGemsOptions.OFF
    option_off = SparxForGemsOptions.OFF
    option_green_sparx = SparxForGemsOptions.GREEN_SPARX
    option_sparx_finder = SparxForGemsOptions.SPARX_FINDER

class ZoeGivesHints(Range):
    """Some or all of the 13 Tutorial Zoes give hints.
    Which Zoes give hints are random.
    Hints include:
    - Difficult or slow locations
    - Progression items in your world
    - Joke hints"""
    display_name = "Number of Zoe Hints"
    range_start = 0
    range_end = 13
    default = 0

class EasySkateboardingLizards(Toggle):
    """The Sunny Villa lizard skateboarding challenges require only 1 lizard.
    Results in minor graphical glitches."""
    display_name = "Easy Skateboarding Lizards"

class EasySkateboardingPoints(Toggle):
    """Point-based skateboarding challenges in Sunny Villa
    and Enchanted Towers become much easier.
    Includes skill points."""
    display_name = "Easy Skateboarding Points"

class EasySkateboardingLostFleet(Toggle):
    """Your turbo cannot run out in the Lost Fleet skateboarding challenges."""
    display_name = "Easy Skateboarding Lost Fleet"

class EasySkateboardingSuperBonusRound(Toggle):
    """Your turbo cannot run out in the Super Bonus Round skateboarding challenge."""
    display_name = "Easy Skateboarding Super Bonus Round"

class EasySubs(Toggle):
    """The Lost Fleet submarine challenges require ony 1 sub.
    The HUD will incorrectly display 1/1."""
    display_name = "Easy Subs"

class EasyBoxing(Toggle):
    """The enemy yeti in Frozen Altars boxing has only 1 health."""
    display_name = "Easy Boxing"

class EasySheilaBombing(Toggle):
    """Rocks and mushrooms never respawn in Spooky Swamp's Sheila sub-area."""
    display_name = "Easy Spooky Sheila Missions"

class EasyBluto(Toggle):
    """Bluto in Seashell Shores has only 1 health."""
    display_name = "Easy Bluto"

class EasySleepyhead(Toggle):
    """Sleepyhead in Spooky Swamp has only 1 health."""
    display_name = "Easy Sleepyhead"

class EasyWhackAMole(Toggle):
    """The Bentley Whack-A-Mole challenge in Crystal Islands require only 1 mole."""
    display_name = "Easy Whack-a-Mole"

class EasySharkRiders(Toggle):
    """The Shark Riders challenge in Desert Ruins requires only 1 shark,
    which starts to the left of the building."""
    display_name = "Easy Shark Riders"

class EasyTanks(Toggle):
    """The Tanks challenges in Haunted Tomb will require only 1 tank each.
    Results in minor graphical glitches."""
    display_name = "Easy Tanks"

class EasyTunnels(Toggle):
    """Water tunnels in Seashell Shore and Dino Mines move slightly more slowly."""
    display_name = "Easy Tunnels"

class NoGreenRockets(Toggle):
    """Collecting a green rocket in Scorch will automatically convert to 50 red rockets instead."""
    display_name = "Convert Scorch Green Rockets to Red"

class LogicSunnySheilaEarly(Toggle):
    """Potentially require entering Sunny Villa's Sheila sub-area from out of bounds.
    NOTE: Entering this area from behind may crash the game if done incorrectly.
    This option only matters is Companionsanity or Moneybagssanity is turned on."""
    display_name = "Enter Sunny Villa Sheila Area Early"

class LogicCloudBackwards(Toggle):
    """Potentially require completing Cloud Spires backwards
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Cloud Spires Backwards"

class LogicMoltenEarly(Toggle):
    """Potentially require entering Molten Crater from out of bounds."""
    display_name = "Enter Molten Crater Early"

class LogicMoltenByrdEarly(Toggle):
    """Potentially require entering Molten Crater's Sgt. Byrd sub-area from out of bounds"""
    display_name = "Enter Molten Crater Sgt. Byrd Area Early"

class LogicMoltenThievesNoMoneybags(Toggle):
    """Potentially require entering Molten Crater's Thieves sub-area from out of bounds
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Enter Molten Crater Thieves without Moneybags"

class LogicSeashellEarly(Toggle):
    """Potentially require entering Seashell Shores from out of bounds."""
    display_name = "Enter Seashell Shores Early"

class LogicSeashellSheilaEarly(Toggle):
    """Potentially require entering Seashell Shores' Sheila sub-area from out of bounds."""
    display_name = "Enter Seashell Shores Sheila Area Early"

class LogicMushroomEarly(Toggle):
    """Potentially require entering Mushroom Speedway from out of bounds."""
    display_name = "Enter Mushroom Speedway Early"

class LogicSheilaEarly(Toggle):
    """Potentially require entering Sheila's Alp from out of bounds
    without paying Moneybags or beating the Sorceress.
    This option only matters if Companionsanity or Moneybagssanity is turned on."""
    display_name = "Enter Sheila's Alp Early"

class LogicSpookyEarly(Toggle):
    """Potentially require entering Spooky Swamp from out of bounds."""
    display_name = "Enter Spooky Swamp Early"

class LogicSpookyNoMoneybags(Toggle):
    """Potentially require getting to the end of Spooky Swamp
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Skip Moneybags in Spooky Swamp"

class LogicBambooEarly(Toggle):
    """Potentially require entering Bamboo Terrace from out of bounds."""
    display_name = "Enter Bamboo Terrace Early"

class LogicBambooBentleyEarly(Toggle):
    """Potentially require entering the Bamboo Terrace Bentley sub-area from out of bounds."""
    display_name = "Enter Bamboo Terrace Bentley Area Early"

class LogicCountryEarly(Toggle):
    """Potentially require entering Country Speedway from out of bounds."""
    display_name = "Enter Country Speedway Early"

class LogicByrdEarly(Toggle):
    """Potentially require entering Sgt. Byrd's Base from out of bounds
    without paying Moneybags or beating the Sorceress.
    This option only matters if Companionsanity or Moneybagssanity is turned on."""
    display_name = "Enter Sgt. Byrd's Base Early"

class LogicFrozenBentleyEarly(Toggle):
    """Potentially require entering the Frozen Altars Bentley sub-area from out of bounds.
    This option only matters if Companionsanity or Moneybagssaniity is turned on."""
    display_name = "Enter Frozen Altars Bentley Area Early"

class LogicFrozenCatHockeyNoMoneybags(Toggle):
    """Potentially require entering the Frozen Altars cat hockey minigame
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Enter Frozen Altars Cat Hockey Area without Moneybags"

class LogicFireworksEarly(Toggle):
    """Potentially require entering Fireworks Factory from out of bounds."""
    display_name = "Enter Fireworks Factory Early"

class LogicFireworksAgent9Early(Toggle):
    """Potentially require entering Fireworks Factory's Agent 9 sub-area
    out of bounds."""
    display_name = "Enter Fireworks Factory Agent 9 Area Early"

class LogicCharmedEarly(Toggle):
    """Potentially require entering Charmed Ridge from out of bounds."""
    display_name = "Enter Charmed Ridge Early"

class LogicCharmedNoMoneybags(Toggle):
    """Potentially require getting past the stairs in Charmed Ridge
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Pass Charmed Ridge Stairs without Moneybags"

class LogicHoneyEarly(Toggle):
    """Potentially require entering Honey Speedway from out of bounds."""
    display_name = "Enter Honey Speedway Early"

class LogicBentleyEarly(Toggle):
    """Potentially require entering Bentley's Outpost
    from out of bounds.
    This option only matters if Companionsanity or Moneybagssanity is turned on."""
    display_name = "Enter Bentley's Outpost Early"

class LogicCrystalNoMoneybags(Toggle):
    """Potentially require fully completing Crystal Islands
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Complete Crystal Islands without Moneybags"

class LogicDesertNoMoneybags(Toggle):
    """Potentially require fully completing Desert Ruins
    without paying Moneybags or beating the Sorceress.
    This option only matters if Moneybagssanity is turned on."""
    display_name = "Complete Desert Ruins without Moneybags"

class LogicDinoAgent9Early(Toggle):
    """Potentially require entering the Agent 9 sub-area
    of Dino Mines out of bounds."""
    display_name = "Enter Dino Mines Agent 9 Area Early"

class LogicSorceressEarly(Toggle):
    """Potentially require entering Sorceress' Lair out of bounds.
    Does not change the door or goal requirements."""
    display_name = "Enter Sorceress' Lair Early"


@dataclass
class Spyro3Option(PerGameCommonOptions):
    goal: GoalOption
    egg_count: EggCount
    percent_extra_eggs: PercentExtraEggs
    guaranteed_items: GuaranteedItemsOption
    open_world: OpenWorldOption
    level_lock_option: LevelLockOption
    starting_levels_count: StartingLevels
    sorceress_door_requirement: SorceressDoorRequirement
    sbr_door_egg_requirement: SBRDoorEggRequirement
    sbr_door_gem_requirement: SBRDoorGemRequirement
    enable_25_pct_gem_checks: Enable25PctGemChecksOption
    enable_50_pct_gem_checks: Enable50PctGemChecksOption
    enable_75_pct_gem_checks: Enable75PctGemChecksOption
    enable_gem_checks: EnableGemChecksOption
    enable_total_gem_checks: EnableTotalGemChecksOption
    max_total_gem_checks: MaxTotalGemCheckOption
    enable_gemsanity: EnableGemsanityOption
    enable_skillpoint_checks: EnableSkillpointChecksOption
    enable_life_bottle_checks: EnableLifeBottleChecksOption
    sparx_power_settings: SparxPowerSettings
    death_link: EnableDeathLink
    moneybags_settings: MoneybagsSettings
    powerup_lock_settings: PowerupLockSettings
    enable_world_keys: EnableWorldKeys
    enable_filler_extra_lives: EnableFillerExtraLives
    enable_filler_invincibility: EnableFillerInvincibility
    enable_filler_color_change: EnableFillerColorChange
    enable_filler_big_head_mode: EnableFillerBigHeadMode
    enable_filler_heal_sparx: EnableFillerHealSparx
    trap_filler_percent: TrapFillerPercent
    enable_trap_damage_sparx: EnableTrapDamageSparx
    enable_trap_sparxless: EnableTrapSparxless
    enable_progressive_sparx_health: EnableProgressiveSparxHealth
    enable_progressive_sparx_logic: ProgressiveSparxHealthLogic
    require_sparx_for_max_gems: RequireSparxForMaxGems
    zoe_gives_hints: ZoeGivesHints
    easy_skateboarding_lizards: EasySkateboardingLizards
    easy_skateboarding_points: EasySkateboardingPoints
    easy_skateboarding_lost_fleet: EasySkateboardingLostFleet
    easy_skateboarding_super_bonus_round: EasySkateboardingSuperBonusRound
    easy_boxing: EasyBoxing
    easy_sheila_bombing: EasySheilaBombing
    easy_tanks: EasyTanks
    easy_subs: EasySubs
    easy_bluto: EasyBluto
    easy_sleepyhead: EasySleepyhead
    easy_shark_riders: EasySharkRiders
    easy_whackamole: EasyWhackAMole
    easy_tunnels: EasyTunnels
    no_green_rockets: NoGreenRockets
    logic_sunny_sheila_early: LogicSunnySheilaEarly
    logic_cloud_backwards: LogicCloudBackwards
    logic_molten_early: LogicMoltenEarly
    logic_molten_byrd_early: LogicMoltenByrdEarly
    logic_molten_thieves_no_moneybags: LogicMoltenThievesNoMoneybags
    logic_seashell_early: LogicSeashellEarly
    logic_seashell_sheila_early: LogicSeashellSheilaEarly
    logic_mushroom_early: LogicMushroomEarly
    logic_sheila_early: LogicSheilaEarly
    logic_spooky_early: LogicSpookyEarly
    logic_spooky_no_moneybags: LogicSpookyNoMoneybags
    logic_bamboo_early: LogicBambooEarly
    logic_bamboo_bentley_early: LogicBambooBentleyEarly
    logic_country_early: LogicCountryEarly
    logic_byrd_early: LogicByrdEarly
    logic_frozen_bentley_early: LogicFrozenBentleyEarly
    logic_frozen_cat_hockey_no_moneybags: LogicFrozenCatHockeyNoMoneybags
    logic_fireworks_early: LogicFireworksEarly
    logic_fireworks_agent_9_early: LogicFireworksAgent9Early
    logic_charmed_early: LogicCharmedEarly
    logic_charmed_no_moneybags: LogicCharmedNoMoneybags
    logic_honey_early: LogicHoneyEarly
    logic_bentley_early: LogicBentleyEarly
    logic_crystal_no_moneybags: LogicCrystalNoMoneybags
    logic_desert_no_moneybags: LogicDesertNoMoneybags
    logic_dino_agent_9_early: LogicDinoAgent9Early
    logic_sorceress_early: LogicSorceressEarly


# Group logic/trick options together, especially for the local WebHost.
spyro_options_groups = [
    OptionGroup(
        "Enabled Locations",
        [
            Enable25PctGemChecksOption,
            Enable50PctGemChecksOption,
            Enable75PctGemChecksOption,
            EnableGemChecksOption,
            EnableTotalGemChecksOption,
            MaxTotalGemCheckOption,
            EnableGemsanityOption,
            EnableSkillpointChecksOption,
            EnableLifeBottleChecksOption
        ],
        False
    ),
    OptionGroup(
        "Game Progression",
        [
            OpenWorldOption,
            LevelLockOption,
            StartingLevels,
            SorceressDoorRequirement,
            SBRDoorEggRequirement,
            SBRDoorGemRequirement,
            MoneybagsSettings,
            PowerupLockSettings,
            EnableWorldKeys
        ],
        False
    ),
    OptionGroup(
        "Item Pool",
        [
            EnableFillerExtraLives,
            EnableFillerInvincibility,
            EnableFillerColorChange,
            EnableFillerBigHeadMode,
            EnableFillerHealSparx,
            TrapFillerPercent,
            EnableTrapDamageSparx,
            EnableTrapSparxless
        ],
        True
    ),
    OptionGroup(
        "Sparx Settings",
        [
            SparxPowerSettings,
            EnableProgressiveSparxHealth,
            ProgressiveSparxHealthLogic,
            RequireSparxForMaxGems
        ],
        True
    ),
    OptionGroup(
        "Game Difficulty",
        [
            ZoeGivesHints,
            EasySkateboardingLizards,
            EasySkateboardingPoints,
            EasySkateboardingLostFleet,
            EasySkateboardingSuperBonusRound,
            EasyBoxing,
            EasySheilaBombing,
            EasyTanks,
            EasySubs,
            EasyBluto,
            EasySleepyhead,
            EasySharkRiders,
            EasyWhackAMole,
            EasyTunnels,
            NoGreenRockets
        ],
        True
    ),
    OptionGroup(
        "Tricks",
        [
            LogicSunnySheilaEarly,
            LogicCloudBackwards,
            LogicMoltenEarly,
            LogicMoltenByrdEarly,
            LogicMoltenThievesNoMoneybags,
            LogicSeashellEarly,
            LogicSeashellSheilaEarly,
            LogicMushroomEarly,
            LogicSheilaEarly,
            LogicSpookyEarly,
            LogicSpookyNoMoneybags,
            LogicBambooEarly,
            LogicBambooBentleyEarly,
            LogicCountryEarly,
            LogicByrdEarly,
            LogicFrozenBentleyEarly,
            LogicFrozenCatHockeyNoMoneybags,
            LogicFireworksEarly,
            LogicFireworksAgent9Early,
            LogicCharmedEarly,
            LogicCharmedNoMoneybags,
            LogicHoneyEarly,
            LogicBentleyEarly,
            LogicCrystalNoMoneybags,
            LogicDesertNoMoneybags,
            LogicDinoAgent9Early,
            LogicSorceressEarly
        ],
        True
    ),
]

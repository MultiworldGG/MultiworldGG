from dataclasses import dataclass
from Options import (Toggle, Range, PerGameCommonOptions, StartInventoryPool,
                     OptionGroup, DefaultOnToggle, Choice, OptionSet)


class TrophiesRequired(Range):
    """How many Trophies need to be found to complete the seed."""
    display_name = "Trophies Required"
    range_start = 1
    range_end = 293
    default = 100


class TrophiesExtra(Range):
    """How many extra Trophies will be in the item pool. Total trophies cannot exceed 293."""
    display_name = "Extra Trophies"
    range_start = 0
    range_end = 293
    default = 50


class BonusSanity(Toggle):
    """Enables Bonuses as checks. Which bonuses are enabled can be tweaked."""
    display_name = "Bonus-sanity"


class EventSanity(Toggle):
    """Enables all Event match clears as checks. If this is disabled, events
        with major unlocks will still give checks."""
    display_name = "Eventsanity"


class RarePokemonChecks(Toggle):
    """Enables 2 checks for seeing Mew and Celebi as well as 2 related Bonus checks."""
    display_name = "Pokemon Bonus Checks"


class HardBonuses(Toggle):
    """Enables a few specific difficult Bonus checks. Does nothing with Bonus-sanity off, such as All Variations or bonuses which are easier with 2 human players."""
    display_name = "Hard Bonus Checks"


class ExtremeBonuses(Toggle):
    """Enables a few very difficult Bonus checks, such as Hammer Throw or No-Damage Clear. Does nothing with Bonus-sanity off."""
    display_name = "Extreme Bonus Checks"


class DiskunTrophyCheck(Toggle):
    """Enables a check on the Diskun trophy, which requires getting all 249 Bonuses."""
    display_name = "Diskun Check"


class MewtwoUnlockCheck(Toggle):
    """Enables a check on unlocking Mewtwo, which requires 1 total hour of VS play."""
    display_name = "Mewtwo Check"


class AnnoyingMultiMan(Toggle):
    """Enables checks on 15-Minute and Cruel Melee"""
    display_name = "Annoying Multi-Man Checks"


class VsCountChecks(Toggle):
    """Enables checks on VS match counts. WARNING. These are really high and will likely take a long time."""
    display_name = "VS Count Checks"


class LotteryPool(Choice):
    """Changes how the Lottery Trophy pool works.
       Vanilla: The lottery pool expands when meeting the vanilla requirement. The 200 VS trophies are unlocked with 5 matches instead.
       Progressive: The lottery pool will increase every time you get a Progressive Lottery Pool item.
       Non-progressive: The lottery pool has specific upgrade items"""
    display_name = "Lottery Pool Mode"
    option_vanilla = 0
    option_progressive = 1
    option_non_progressive = 2
    default = 1


class SoloCSmash(DefaultOnToggle):
    """Enables the use of Smash Attacks with the C-Stick during 1-Player modes."""
    display_name = "1-P C Smash"


class TargetSanity(Toggle):
    """Enables a check for every individual character's Target Test being cleared."""
    display_name = "Target Clear Checks"


class LongTargetChecks(Toggle):
    """Enables Target Test checks locked behind most or all characters."""
    display_name = "Long Target Test Checks"


class DisableTapJump(Toggle):
    """Removes the ability to jump by tapping Up on the control stick."""
    display_name = "Disable Tap Jump"


class HardModeClears(Toggle):
    """Enables checks for completing the main 1-P Modes on Hard or higher."""
    display_name = "Hard Mode Clears"


class StartingCharacter(Choice):
    """This is the character you will start with."""
    display_name = "Starting Character"
    option_dr_mario = 0
    option_mario = 1
    option_luigi = 2
    option_bowser = 3
    option_peach = 4
    option_yoshi = 5
    option_donkey_kong = 6
    option_captain_falcon = 7
    option_ganondorf = 8
    option_falco = 9
    option_fox = 10
    option_ness = 11
    option_ice_climbers = 12
    option_kirby = 13
    option_samus = 14
    option_zelda = 15
    option_link = 16
    option_young_link = 17
    option_pichu = 18
    option_pikachu = 19
    option_jigglypuff = 20
    option_mewtwo = 21
    option_mr_game_and_watch = 22
    option_marth = 23
    option_roy = 24
    default = "random"


class TenManSanity(Toggle):
    """Enables a check for every individual character clearing 10-Man Melee"""
    display_name = "Ten-Man Sanity"


class AutoLCancel(Toggle):
    """Automatically L-cancels aerial attacks."""
    display_name = "Automatic L-Cancel"


class GoalTriggers(OptionSet):
    """
    Set which goal triggers are active. You will need to complete ALL of the specified goals and collect the required amount of Trophies
    in order to complete the game. You can check your Goal Trigger progress in-game by using the command /check_goals in the client.

    Available Triggers: 
        Giga Bowser: Defeat Giga Bowser at the end of Adventure Mode
        Crazy Hand: Defeat Crazy Hand at the end of Classic Mode
        All Targets: Complete Target Test with every character
        Other Events: Complete Event Matches 1-49
        Event 50: Complete Event 50
        Event 51: Complete Event 51
    """
    display_name = "Goal Triggers"
    default = {"Giga Bowser"}
    valid_keys = {"Giga Bowser", "Crazy Hand", "Event 51", "All Targets", "All Events", "Other Events", "Event 50"}


class AdventureClearTrophies(DefaultOnToggle):
    """Enables checks on each character's Adventure clear trophy"""
    display_name = "Adventure Clear Trophies"


class ClassicClearTrophies(DefaultOnToggle):
    """Enables checks on each character's Classic clear trophy"""
    display_name = "Classic Clear Trophies"


class AllStarClearTrophies(DefaultOnToggle):
    """Enables checks on each character's All-Star clear trophy"""
    display_name = "All-Star Clear Trophies"


class RandomizeItems(Toggle):
    """Adds in-battle Items to the multiworld pool. The item will not spawn in any mode until you find it.
       (With the exception of All-Star Heart Containers)"""
    display_name = "Randomize Battle Items"


class Disable1PRandomTrophies(Toggle):
    """Removes the random 1P mode trophies from the locations pool."""
    display_name = "Remove 1P Trophies"


@dataclass
class SSBMOptions(PerGameCommonOptions):
    starting_character: StartingCharacter
    trophies_required: TrophiesRequired
    extra_trophies: TrophiesExtra
    bonus_checks: BonusSanity
    target_checks: TargetSanity
    ten_man_checks: TenManSanity
    enable_rare_pokemon_checks: RarePokemonChecks
    enable_hard_bonuses: HardBonuses
    enable_extreme_bonuses: ExtremeBonuses
    enable_annoying_multiman_checks: AnnoyingMultiMan
    diskun_trophy_check: DiskunTrophyCheck
    mewtwo_unlock_check: MewtwoUnlockCheck
    vs_count_checks: VsCountChecks
    hard_modes_clear: HardModeClears
    long_targettest_checks: LongTargetChecks
    lottery_pool_mode: LotteryPool
    event_checks: EventSanity
    goal_triggers: GoalTriggers
    solo_cstick_smash: SoloCSmash
    disable_tap_jump: DisableTapJump
    automatic_l_cancel: AutoLCancel
    start_inventory_from_pool: StartInventoryPool
    adventure_clear_trophies: AdventureClearTrophies
    classic_clear_trophies: ClassicClearTrophies
    all_star_clear_trophies: AllStarClearTrophies
    randomize_battle_items: RandomizeItems
    remove_random_1P_trophies: Disable1PRandomTrophies


ssbm_option_groups = [
    OptionGroup("Starting Options", [
        StartingCharacter
    ]),

    OptionGroup("Trophy Settings", [
        TrophiesRequired,
        TrophiesExtra,
    ]),

    OptionGroup("Check Settings", [
        AdventureClearTrophies,
        ClassicClearTrophies,
        AllStarClearTrophies,
        BonusSanity,
        EventSanity,
        TargetSanity,
        TenManSanity,
        Disable1PRandomTrophies
    ]),

    OptionGroup("Item Settings", [
        RandomizeItems
    ]),

    OptionGroup("Annoying Checks", [
        HardBonuses,
        RarePokemonChecks,
        ExtremeBonuses,
        AnnoyingMultiMan,
        VsCountChecks,
        DiskunTrophyCheck,
        MewtwoUnlockCheck,
        LongTargetChecks,
        HardModeClears
    ]),

    OptionGroup("Goal Settings", [
        GoalTriggers
    ]),

    OptionGroup("QOL Settings", [
        SoloCSmash,
        DisableTapJump,
        AutoLCancel
    ]),
]

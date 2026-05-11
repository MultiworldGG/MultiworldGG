### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Mapping
from typing import Any

from typing_extensions import override

from Options import Choice, FreeText, OptionSet, Range, Visibility

from .. import enums as e
from .optionbase import BDefaultOnToggle, BToggle, ChoiceEx, EnumOption, LaxRange, LevelDict
from .protocols import NamedOption

## Option classes

class BossGradeChecks(EnumOption[e.GradeCheckMode], ChoiceEx, NamedOption):
    """
    Enable grade checks for Boss Levels.
    NOTE: S Grade option will be treated as A+ Grade if Expert Mode is disabled.
    """
    name = "boss_grade_checks"
    display_name = "Boss Grade Checks"
    enum_type = e.GradeCheckMode
    option_disabled = 0
    option_a_minus_grade = 1
    option_a_grade = 2
    option_a_plus_grade = 3
    option_s_grade = 4
    default = 1


class BossSecretChecks(BToggle, NamedOption):
    """
    Also include beating the secret phases that certain bosses have as checks.
    The boss levels include: Botanic Panic, Pyramid Peril, Dramatic Fanatic, and Doggone Dogfight (DLC).
    The secret phases are generally more difficult than the normal fight.
    """
    name = "boss_secret_checks"
    display_name = "Boss Secret Checks"


class ContractGoalRequirements(Range, NamedOption):
    """
    Set the amount of contracts needed for goal.
    Note: Cannot be lower than Contract Requirements
    """
    name = "contract_goal_requirements"
    display_name = "Contract Goal Requirements"
    range_start = 3
    range_end = 17
    default = 17


class ContractRequirements(Range, NamedOption):
    """
    Set the amount of contracts needed to confront King Dice and, ultimately, the devil.
    The required contracts for the die houses are evenly distributed.
    """
    name = "contract_requirements"
    display_name = "Contract Requirements"
    range_start = 3
    range_end = 17
    default = 17


class DeathLink(BToggle, NamedOption):
    """
    Enable DeathLink. When you die, everyone dies. Of course the reverse is true too.
    In Cuphead, this only applies while you are in a level.
    """
    name = "deathlink"
    display_name = "Death Link"
    rich_text_doc = True


class DeathLinkGraceCount(LaxRange, NamedOption):
    """
    -REQUIRES DEATHLINK-
    Set DeathLink Grace Count. Each "Grace" grants you a free Death without triggering DeathLink.
    """
    name = "deathlink_grace_count"
    display_name = "Death Link Grace Count"
    range_start = 0
    range_end = 25
    hard_max = 1000
    default = 0


class DeathLinkMode(Choice, NamedOption):
    """
    -REQUIRES DEATHLINK-
    Set DeathLink Mode.

    Modes:
    - Lose: Both players dying triggers DeathLink. Same in reverse.
    - Per Player: Each player's death will trigger DeathLink. Receiving a DeathLink will kill a random player.

    NOTE: Per Player will behave like Lose if playing singleplayer.

    This option is ignored on older clients that don't support this feature
    """
    name = "deathlink_mode"
    display_name = "Death Link Mode"
    visibility = Visibility.spoiler
    option_lose = 1
    option_per_player = 2
    default = 1


class DeliciousLastCourse(BToggle, NamedOption):
    """
    Set whether or not to use Delicious Last Course content (Requires owning the DLC).
    """
    name = "use_dlc"
    display_name = "DLC"


class DicePalaceBossSanity(BToggle, NamedOption):
    """
    ---NOT YET IMPLEMENTED---
    Enable checks for beating the King Dice mini-bosses.
    There is an indicator for which mini-bosses you defeated.
    """
    name = "kingdice_bosssanity"
    display_name = "King Dice BossSanity"
    visibility = Visibility.spoiler | Visibility.template


class DlcBossChaliceChecks(EnumOption[e.ChaliceCheckMode], Choice, NamedOption):
    """
    -DLC ONLY-
    -REQUIRES CHALICE-
    Enable checks for defeating each boss as Ms. Chalice.
    Separate makes Chalice checks separate from level completion checks.
    Grade Required has the set grade check requirement for bosses.
    """
    name = "dlc_boss_chalice_checks"
    display_name = "[DLC] Boss Chalice Checks"
    enum_type = e.ChaliceCheckMode
    option_disabled = 0
    option_enabled = 1
    option_separate = 2
    option_grade_required = 4
    option_separate_grade_required = 6
    default = 0


class DlcCactusGirlQuest(BToggle, NamedOption):
    """
    -DLC ONLY-
    -REQUIRES CHALICE-
    Enable the Cactus Girl Quest (aka Ms. Chalice Quest) check.
    This means that you will have to beat EVERY boss as Ms. Chalice (tedious) for a single check.
    You can talk to the Cactus Girl to know which bosses you need to defeat still.
    """
    name = "dlc_cactusgirl_quest"
    display_name = "[DLC] Cactus Girl Quest"


class DlcChaliceCheckGrade(Choice, NamedOption):
    """
    -DLC ONLY-
    -REQUIRES CHALICE-
    --- NOT IMPLEMENTED ---
    [MISSINGDESCRIPTION]
    """
    name = "dlc_chalice_check_grade"
    display_name = "[DLC] Chalice Check Grade Requirement"
    option_disabled = 0
    option_a_minus_grade = 1
    option_a_grade = 2
    option_a_plus_grade = 3
    option_use_grade_check = 64
    default = 0


class DlcChaliceItemsSeparate(OptionSet, NamedOption):
    """
    ---NOT YET IMPLEMENTED---
    -DLC ONLY-
    Make certain items seperate for when playing as Ms. Chalice.
    Options:
    - Core Items: Core items like plane and supers.
    - Abilities: Abilities including parry.

    With parry for Ms. Chalice, the Parry item is replaced with Progressive Dash.
    Progressive Dash has two levels: 1. Dash only, 2. Dash with Parry.

    Note: Chalice Double Jump is randomized regardless of this option if Randomize Abilities is on.
    """
    name = "dlc_chalice_items_separate"
    display_name = "[DLC] Chalice Items Separate"
    #visibility = Visibility.complex_ui
    visibility = Visibility.spoiler
    valid_keys = frozenset({"core_items", "abilities"}) # TODO: Finish
    valid_keys_casefold = True
    _fvalue: int

    _key_ebits: Mapping[str, e.ItemGroups] = {
        "core_items": e.ItemGroups.CORE_ITEMS,
        #"weapon_ex": e.ItemGroups.WEAPON_EX,
        "abilities": e.ItemGroups.ABILITIES
    }

    @property
    def fvalue(self) -> e.ItemGroups:
        """flag value"""
        return e.ItemGroups(self._fvalue)

    @fvalue.setter
    def fvalue(self, value: e.ItemGroups | int):
        self._fvalue = int(value)

    def _get_separate_items_mode(self) -> e.ItemGroups:
        _set = self.value
        _val = e.ItemGroups.NONE

        for opt, item_group in self._key_ebits.items():
            if opt in _set:
                _val |= item_group

        return _val

    def _get_separate_items_set(self) -> set[str]:
        _val = self.fvalue

        _set: set[str] = {
            opt
            for opt, item_group in self._key_ebits.items()
            if (_val & item_group) == item_group
        }

        return _set

    @override
    def __setattr__(self, name: str, value: Any, /):
        super().__setattr__(name, value)
        if name == "value":
            self._value_set = True
            self.fvalue = self._get_separate_items_mode()
            self._value_set = False
        elif name == "evalue" and not self._value_set:
            self.value = self._get_separate_items_set()


class DlcChaliceMode(EnumOption[e.ChaliceMode], Choice, NamedOption):
    """
    -DLC ONLY-
    Enable Ms. Chalice and the Astral Cookie.
    Options:
    - Disabled: The cookie is disabled and cannot be obtained (Ms. Chalice is disabled).
    - Start: The cookie is available at the start of the game.
    - Vanilla: The cookie is obtained at the start of the DLC (Vanilla Behavior).
    - Randomized: The cookie is in the item pool. Starting the DLC is a check.
    """
    name = "dlc_chalice"
    display_name = "[DLC] Ms. Chalice"
    enum_type = e.ChaliceMode
    option_disabled = 0
    option_start = 1
    option_vanilla = 2
    option_randomized = 3
    #- Chalice Only: Play as only Ms. Chalice. Cookie is not considered an item.
    #option_chalice_only = 4
    default = 3


class DlcChessCastle(EnumOption[e.ChessCastleMode], Choice, NamedOption):
    """
    -DLC ONLY-
    Choose how to handle the locations of The King's Leap.
    Gauntlet is the run where you have to defeat all the King's Leap bosses in succession.
    """
    name = "dlc_kingsleap"
    display_name = "[DLC] The King's Leap"
    enum_type = e.ChessCastleMode
    option_exclude = 0
    option_exclude_gauntlet = 1
    option_include_all = 3
    default = 1


class DlcChessChaliceChecks(EnumOption[e.ChaliceCheckMode], Choice, NamedOption):
    """
    -DLC ONLY-
    -REQUIRES CHALICE-
    -REQUIRES THE KING'S LEAP-
    Enable checks for completing The King's Leap checks as Ms. Chalice.
    """
    name = "dlc_chess_chalice_checks"
    display_name = "[DLC] Chess Chalice Checks"
    enum_type = e.ChaliceCheckMode
    visibility = Visibility.template | Visibility.spoiler
    option_disabled = 0
    option_enabled = 1
    option_separate = 2
    default = 0


class DlcCurseMode(EnumOption[e.CurseMode], Choice, NamedOption):
    """
    -DLC ONLY-
    Set how the cursed and devine relic is handled.

    Modes:
    - Off: Broken Relic is removed from the game
    - Vanilla: Broken Relic is in pool. The graveyard and getting the devine relic is excluded from logic.
    """
    name = "dlc_curse_mode"
    display_name = "[DLC] Curse Mode"
    enum_type = e.CurseMode
    option_off = 0
    option_vanilla = 1
    #option_reverse = 2
    #option_always_on = 3
    #option_always_on_r = 4
    #option_always_on_1 = 5
    #option_always_on_2 = 6
    #option_always_on_3 = 7
    #option_always_on_4 = 8
    default = 0


class DlcDicePalaceChaliceChecks(EnumOption[e.ChaliceCheckMode], Choice, NamedOption):
    """
    --NOT YET IMPLEMENTED--
    -DLC ONLY-
    -REQUIRES CHALICE-
    -REQUIRES KING DICE BOSSSANITY-
    Enable checks for completing King Dice Bossanity checks as Ms. Chalice.
    """
    name = "dlc_kingdice_chalice_checks"
    display_name = "[DLC] King Dice Chalice Checks"
    enum_type = e.ChaliceCheckMode
    visibility = Visibility.template | Visibility.spoiler
    option_disabled = 0
    option_enabled = 1
    option_separate = 2
    default = 0


class DlcIngredientGoalRequirements(Range, NamedOption):
    """
    -DLC ONLY-
    Set the amount of ingredients needed for goal.
    Note: Cannot be lower than Ingredient Requirements
    """
    name = "dlc_ingredient_goal_requirements"
    display_name = "[DLC] Ingredient Goal Requirements"
    range_start = 1
    range_end = 5
    default = 5


class DlcIngredientRequirements(Range, NamedOption):
    """
    -DLC ONLY-
    Set the amount of ingredients needed to confront Saltbaker.
    """
    name = "dlc_ingredient_requirements"
    display_name = "[DLC] Ingredient Requirements"
    range_start = 1
    range_end = 5
    default = 5


class DlcRunGunChaliceChecks(EnumOption[e.ChaliceCheckMode], Choice, NamedOption):
    """
    -DLC ONLY-
    -REQUIRES CHALICE-
    Enable checks for completing each run n' gun as Ms. Chalice.
    Separate makes Chalice checks separate from level completion checks.
    Grade Required has the set grade check requirement for run n' guns.
    """
    name = "dlc_rungun_chalice_checks"
    display_name = "[DLC] Run n' Gun Chalice Checks"
    enum_type = e.ChaliceCheckMode
    option_disabled = 0
    option_enabled = 1
    option_separate = 2
    option_grade_required = 4
    option_separate_grade_required = 6
    default = 0


class DuckLockPlatDrop(BToggle, NamedOption):
    """
    Allow the dropping-down-platforms-without-duck-by-using-aim-lock exploit.
    This option re-enables that bug that the mod had before alpha02.
    This "feature" is purely client-side and does not affect logic.
    """
    name = "ducklock_platdrop"
    display_name = "DuckLock PlatDrop"
    visibility = Visibility.spoiler


class EarlyParry(BToggle, NamedOption):
    """
    Make Parry be placed early in the multiworld.
    This may prevent early BK.
    NOTE: This is on regardless in single player multiworlds.
    """
    name = "early_parry"
    display_name = "Early Parry"
    visibility = Visibility.spoiler | Visibility.template | Visibility.complex_ui


class ExpertMode(BToggle, NamedOption):
    """
    Set the boss difficulty to expert.
    """
    name = "expert_mode"
    display_name = "Expert Mode"


class ExtraCoins(LaxRange, NamedOption):
    """
    Set extra coins in the item pool.
    """
    name = "extra_coins"
    display_name = "Extra Coins"
    range_start = 0
    range_end = 10
    hard_max = 20
    default = 0


class FillerWeightExtraHealth(LaxRange, NamedOption):
    """
    Set Extra Health weight. Higher weight means it will more likely appear compared to other filler items.
    Set to 0 to disable this item.
    """
    name = "filler_weight_extrahealth"
    display_name = "Extra Health Weight"
    default = 3


class FillerWeightFastFire(LaxRange, NamedOption):
    """
    Set Fast Fire weight. Higher weight means it will more likely appear compared to other filler items.
    Set to 0 to disable this item.
    """
    name = "filler_weight_fastfire"
    display_name = "Fast Fire Weight"
    visibility = Visibility.none
    default = 0


class FillerWeightSuperRecharge(LaxRange, NamedOption):
    """
    Set Super Recharge weight. Higher weight means it will more likely appear compared to other filler items.
    Set to 0 to disable this item.
    """
    name = "filler_weight_supercharge"
    display_name = "Super Recharge Weight"
    default = 3


class FreeMoveIsles(BToggle, NamedOption):
    """
    Allow all the levels on each island to be freely accessible without completing a previous level first.
    """
    name = "freemove_isles"
    display_name = "Free Move Isles"


class GameMode(EnumOption[e.GameMode], ChoiceEx, NamedOption):
    """
    Set the mode of the randomizer which includes goal.
    NOTE: If DLC is not enabled, picking DLC modes will pick a random mode from the base game instead.
    """
    name = "mode"
    display_name = "Mode"
    enum_type = e.GameMode
    _no_isle_4 = 32
    _isle_4_only = 64
    option_beat_devil = 1
    option_collect_contracts = 2
    option_buy_out_shop = 4
    option_dlc_beat_saltbaker = 8
    option_dlc_beat_both = 9
    option_dlc_collect_ingredients = 16
    option_dlc_collect_both = 18
    #option_dlc_beat_devil_no_isle4 = 33
    #option_dlc_collect_contracts_no_isle4 = 34
    #option_dlc_buy_out_shop_no_isle4 = 36
    #option_dlc_collect_ingredients_no_isle4 = 48
    #option_dlc_beat_saltbaker_isle4_only = 72
    #option_dlc_collect_ingredients_isle4_only = 80
    default = 1


class LevelPlacements(LevelDict, NamedOption):
    """
    Define which levels will be placed in which spots when shuffling the levels.
    Note: Some levels cannot be shuffled, and some levels cannot be placed in specific spots.
    Key: original, Value: new
    """
    name = "level_placements"
    display_name = "Level Placements"
    visibility = Visibility.spoiler | Visibility.template | Visibility.complex_ui
    default: Mapping[str, str] = {}


class LevelShuffle(EnumOption[e.LevelShuffleMode], Choice, NamedOption):
    """
    Shuffle the Boss and Run n' Gun levels.
    Bosses and Run n' Guns are shuffled within their own group.
    Note: Be careful with this option! This can easily break generation if used with plando.
    """
    name = "level_shuffle"
    display_name = "Level Shuffle"
    enum_type = e.LevelShuffleMode
    option_disabled = 0
    option_enabled = 1
    option_plane_separate = 2
    default = 0


class LevelShuffleDicePalace(BDefaultOnToggle, NamedOption):
    """
    Shuffle the King Dice mini-bosses.
    This option is independent of Level Shuffle.
    """
    name = "level_shuffle_kingdice"
    display_name = "Shuffle King Dice Bosses"


class LevelShuffleSeed(FreeText, NamedOption):
    """
    Seed for Level Shuffle.
    Leave blank to use a seed based on the multiworld's seed.
    """
    name = "level_shuffle_seed"
    display_name = "Level Shuffle Seed"
    visibility = Visibility.spoiler
    default = ""


class LogicMode(EnumOption[e.LogicMode], Choice, NamedOption):
    """
    -HARD LOGIC WORKS, BUT IS INCOMPLETE-
    Set the logic mode.
    Hard: Use more difficult logic that may require more skillful actions without specific items.
    """
    name = "logic_mode"
    display_name = "Logic"
    enum_type = e.LogicMode
    option_normal = 0
    option_hard = 1
    default = 0


class MaxHealthUpgrades(Range, NamedOption):
    """
    Set number of max health upgrades in the pool.
    NOTE: Health cannot be any higher than 9, so health charms would be less useful at higher health amounts.
    """
    name = "maxhealth_upgrades"
    display_name = "Max Health Upgrades"
    range_start = 0
    range_end = 3
    default = 0


class MinimumFillerItems(Range, NamedOption):
    """
    Set the minimum amount of filler items that should exist in this world.
    NOTE: If there are not enough locations, some coins will be compressed into packs of 2 or 3 to make space.
    """
    name = "minimum_filler"
    display_name = "Minimum Filler Items"
    range_start = 0
    range_end = 10
    default = 0


class MusicShuffle(Choice, NamedOption):
    """
    ---NOT YET IMPLEMENTED ON CLIENT---
    Enable Shuffling Music.
    NOTE: This option will do nothing until the client is updated
    """
    name = "music_shuffle"
    display_name = "Music Shuffle"
    visibility = Visibility.spoiler
    option_disabled = 0
    option_level_music = 1
    option_map_music = 2
    option_level_and_map_music = 3
    #option_all_music = 255
    default = 0


class PacifistQuest(BToggle, NamedOption):
    """
    Enable the Pacifist Quest check.
    This means that you will have to beat all 6 Run n' Gun levels without beating any enemies (not easy).
    """
    name = "pacifist_quest"
    display_name = "Pacifist Quest"


class RandomizeAbilities(BDefaultOnToggle, NamedOption):
    """
    Randomize essential abilities like Crouch, Parry, Dash, etc.
    """
    name = "randomize_abilities"
    display_name = "Randomize Abilities"


class RunGunGradeChecks(EnumOption[e.GradeCheckMode], Choice, NamedOption):
    """
    Enable grade checks for Run n' Gun levels.
    Pacifist: Beat the level without killing any monsters (not easy).
    """
    name = "rungun_grade_checks"
    display_name = "Run n' Gun Grade Checks"
    enum_type = e.GradeCheckMode
    option_disabled = 0
    option_a_minus_grade = 1
    option_a_grade = 2
    option_a_plus_grade = 3
    option_p_grade = 5
    alias_pacifist = 5
    default = 1


class SilverworthQuest(BDefaultOnToggle, NamedOption):
    """
    Enable the Silverworth Quest check.
    This means that you will have to beat 15 levels with at least an A- Grade in order to get this check.
    """
    name = "silverworth_quest"
    display_name = "Silverworth Quest"


class StartMaxHealth(Range, NamedOption):
    """
    Set starting max health.
    NOTE: Health cannot be any higher than 9, so health charms would be less useful at higher health amounts.
    """
    name = "start_maxhealth"
    display_name = "Starting Max Health"
    range_start = 1
    range_end = 4
    default = 3


class StartMaxHealthP2(Range, NamedOption):
    """
    Set starting max health for Player 2. Set to 0 to use Player 1's max health.
    NOTE: Health cannot be any higher than 9, so health charms would be less useful at higher health amounts.
    """
    name = "start_maxhealth_p2"
    display_name = "Starting Max Health"
    range_start = 0
    range_end = 4
    default = 0


class StartWeapon(ChoiceEx, NamedOption):
    """
    Choose weapon to start with.
    NOTE: If DLC is not enabled, picking DLC weapons will pick a random base game weapon instead.
    """
    name = "start_weapon"
    display_name = "Start Weapon"
    option_random_weapon = -2
    option_peashooter = 0
    option_spread = 1
    option_chaser = 2
    option_lobber = 3
    option_charge = 4
    option_roundabout = 5
    option_dlc_crackshot = 6
    option_dlc_converge = 7
    option_dlc_twistup = 8
    option_none = 127
    default = -2

    def is_none(self) -> bool:
        return self.value == self.option_none

    @classmethod
    @override
    def from_text(cls, text: str) -> Choice:
        text = text.lower()
        if text == "none":
            cls.name_lookup[cls.option_none] = "None"
            return cls(cls.option_none)
        return super().from_text(text)


class TrapLoadoutAnyWeapon(BToggle, NamedOption):
    """
    For Loadout Mixup Trap:
    Allow Loadout Mixup to use any item including ones you do not currently have.
    """
    name = "trap_loadout_anyweapon"
    display_name = "Loadout Mixup Any Item"
    visibility = Visibility.spoiler


class TrapWeightFingerJam(LaxRange, NamedOption):
    """
    Set Finger Jam Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    name = "trap_weight_fingerjam"
    display_name = "Finger Jam Trap Weight"
    visibility = Visibility.none
    default = 5


class TrapWeightLoadout(LaxRange, NamedOption):
    """
    Set Loadout Mixup Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    name = "trap_weight_loadout"
    display_name = "Loadout Mixup Trap Weight"
    visibility = Visibility.none
    default = 5


class TrapWeightScreen(LaxRange, NamedOption):
    """
    Set Screen Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    name = "trap_weight_screen"
    display_name = "Screen Trap Weight"
    visibility = Visibility.none
    default = 3


class TrapWeightSlowFire(LaxRange, NamedOption):
    """
    Set Slow Fire Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    name = "trap_weight_slowfire"
    display_name = "Slow Fire Trap Weight"
    visibility = Visibility.none
    default = 5


class TrapWeightSuperDrain(LaxRange, NamedOption):
    """
    Set Super Drain Trap weight. Higher weight means it will more likely appear compared to other traps.
    Set to 0 to disable this trap.
    """
    name = "trap_weight_superdrain"
    display_name = "Super Drain Trap Weight"
    visibility = Visibility.none
    default = 5


class Traps(Range, NamedOption):
    """
    ---NOT YET IMPLEMENTED ON CLIENT---
    Set Trap percentage for filler items.
    """
    name = "traps"
    display_name = "Traps"
    visibility = Visibility.template | Visibility.spoiler
    range_start = 0
    range_end = 100
    default = 0


class WeaponMode(EnumOption[e.WeaponMode], Choice, NamedOption):
    """
    Set how the weapons are shuffled in the pool.
    Options:
    - Normal: EX is part of the weapon you receive (vanilla behavior).
    - Progressive: turns the weapons in the pool into progressive weapons (plane has a separate EX item).
    - EX Separate makes each weapon's EX ability a separate item.
    - ... Except Start: makes the start weapon have normal behavior.
    Notes:
    - "Progressive" means that weapon EX is unlocked from having two of the same weapon.
    - A weapon EX item without the base weapon will give you a weapon that only can do EX shots.
    """
    name = "weapon_mode"
    display_name = "Weapon Mode"
    enum_type = e.WeaponMode
    option_normal = 0
    option_progressive = 1
    option_progressive_except_start = 5
    option_ex_separate = 2
    option_ex_separate_except_start = 6
    default = 0

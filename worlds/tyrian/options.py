# Archipelago MultiWorld integration for Tyrian
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details.

from dataclasses import dataclass
from typing import TYPE_CHECKING

from Options import (
    Accessibility,
    Choice,
    DeathLink,
    DefaultOnToggle,
    ItemDict,
    NamedRange,
    OptionGroup,
    PerGameCommonOptions,
    ProgressionBalancing,
    Range,
    TextChoice,
    Toggle,
    Visibility,
)

if TYPE_CHECKING:
    from BaseClasses import PlandoOptions

    from worlds.AutoWorld import World


# =============
# === Goals ===
# =============


class EnableTyrian2000Support(Toggle):
    """Use data from Tyrian 2000 instead of Tyrian 2.1.

    Turning this on is mandatory if you want to do anything with Episode 5. All of Tyrian 2000's weapons and new items will also be added to the item pool.
    """
    display_name = "Enable Tyrian 2000 support"


class GoalEpisode1(Choice):
    """Add Episode 1 (Escape) levels to the pool. Adds 93 locations across 16 levels.

    If "goal" is chosen, you'll need to complete "ASSASSIN" (in addition to other episode goals) to win.
    """
    display_name = "Episode 1"
    option_goal = 2
    option_on = 1
    option_off = 0
    default = 2


class GoalEpisode2(Choice):
    """Add Episode 2 (Treachery) levels to the pool. Adds 75 locations across 12 levels.

    If "goal" is chosen, you'll need to complete "GRYPHON" (in addition to other episode goals) to win.
    """
    display_name = "Episode 2"
    option_goal = 2
    option_on = 1
    option_off = 0
    default = 2


class GoalEpisode3(Choice):
    """Add Episode 3 (Mission: Suicide) levels to the pool. Adds 81 locations across 12 levels.

    If "goal" is chosen, you'll need to complete "FLEET" (in addition to other episode goals) to win.
    """
    display_name = "Episode 3"
    option_goal = 2
    option_on = 1
    option_off = 0
    default = 2


class GoalEpisode4(Choice):
    """Add Episode 4 (An End to Fate) levels to the pool. Adds 100 locations across 18 levels.

    If "goal" is chosen, you'll need to complete "NOSE DRIP" (in addition to other episode goals) to win.
    """
    display_name = "Episode 4"
    option_goal = 2
    option_on = 1
    option_off = 0
    default = 0


class GoalEpisode5(Choice):
    """Add Episode 5 (Hazudra Fodder) levels to the pool. Adds 56 locations across 7 levels.

    This setting requires enabling Tyrian 2000 support to have any effect.
    If "goal" is chosen, you'll need to complete "FRUIT" (in addition to other episode goals) to win.
    """
    display_name = "Episode 5"
    option_goal = 2
    option_on = 1
    option_off = 0
    default = 0


class DataCubeHunt(Toggle):
    """If enabled, goal levels will not be in the item pool, but will be locked behind collecting a given amount of "Data Cube" items.

    See data_cubes_required, data_cubes_total_percent, and data_cubes_total for more information.
    """
    display_name = "Data Cube Hunt"


class DataCubesRequired(Range):
    """The amount of data cubes that must be collected to access goal levels in Data Cube Hunt mode."""
    display_name = "Data Cubes Required"
    range_start = 1
    range_end = 99
    default = 40


class DataCubesTotal(NamedRange):
    """How many data cubes should be added to the pool in Data Cube Hunt mode, as an absolute amount.

    You may specify 'percentage' to use the value from data_cubes_total_percent instead.
    """
    display_name = "Data Cubes Total"
    range_start = 1
    range_end = 400
    special_range_names = {
        "percentage": 0,
    }
    default = 0


class DataCubesTotalPercent(Range):
    """How many data cubes should be added to the pool in Data Cube Hunt mode, as a percentage of the required amount.

    100 adds in exactly the number of data cubes required, 200 adds in twice that amount, etc.
    """
    display_name = "Data Cubes Total %"
    visibility = Visibility.all ^ Visibility.spoiler  # Overrides above option if it takes effect
    range_start = 100
    range_end = 400
    default = 100


# =============================
# === Item Pool Adjustments ===
# =============================


class RemoveFromItemPool(ItemDict):
    """Allows customizing the item pool by removing unwanted items from it.

    Note: Items in starting inventory are automatically removed from the pool; you don't need to remove them here too.
    """
    display_name = "Remove From Item Pool"
    verify_item_name = True


class StartingMoney(Range):
    """Change the amount of money you start the seed with."""
    display_name = "Starting Money"
    range_start = 0
    range_end = 9999999
    default = 10000


class StartingMaxPower(Range):
    """Change the maximum power level you're allowed to upgrade weapons to when you start the seed.

    Increasing this can result in more varied seeds, and/or easier starts.
    """
    display_name = "Starting Maximum Power Level"
    range_start = 1
    range_end = 11
    default = 1


class RandomStartingWeapon(Toggle):
    """Choose whether you start with the default Pulse-Cannon, or some other random weapon.

    The weapon you receive depends on logic difficulty settings, among other things. In particular, adding generators to your start inventory may result in a better selection for lower logic difficulties.

    Note: If your start inventory contains a front weapon, you will not receive another starting weapon (and therefore, this option will be ignored).
    """
    display_name = "Random Starting Weapon"


class ProgressiveItems(DefaultOnToggle):
    """How items with multiple tiers (in this game, only generators) should be rewarded.

    If 'off', each item can be independently picked up, letting you skip tiers. Picking up an item of a lower tier after an item of a higher tier does nothing.
    If 'on', each "Progressive" item will move you up to the next tier, regardless of which one you find.
    """
    display_name = "Progressive Items"


class AddBonusGames(Toggle):
    """Add the three bonus games into the item pool as additional filler.

    If 'off', these bonus games will be available by default.
    If 'on', the items for each bonus game will need to be obtained to play them, just like any other level.
    """
    display_name = "Add Bonus Games"


class Specials(Choice):
    """Enable or disable specials (extra behaviors when starting to fire).

    If 'on', your ship will have a random special from the start.
    If 'as_items', specials will be added to the item pool, and can be freely chosen once acquired.
    If 'off', specials won't be available at all.
    """
    display_name = "Specials"
    option_on = 1
    option_as_items = 2
    option_off = 0
    alias_true = 1
    alias_false = 0
    default = 2


class Twiddles(Choice):
    """Enable or disable twiddles (Street Fighter-esque button combinations).

    If 'on', your ship will have up to three random twiddles. Their button combinations will be the same as in the original game; as will their use costs.
    If 'off', no twiddles will be available.

    The following option is not currently available but is planned in the future:
    If 'chaos', your ship will have up to three random twiddles with new inputs. They may have new, unique behaviors; and they may have different use costs.
    """
    display_name = "Twiddles"
    option_on = 1
    #option_chaos = 2
    option_off = 0
    alias_true = 1
    alias_false = 0
    default = 1


class LocalLevelPercent(Range):
    """Set some percentage of levels, chosen randomly, to be local to your own world.

    Increasing this may reduce the chance of being in BK mode (having no checks available), but may also result in less interaction with other worlds.
    """
    display_name = "Local Level %"
    range_start = 0
    range_end = 100
    default = 0


# =======================
# === Shops and Money ===
# =======================


class ShopMode(Choice):
    """Determine if shops exist and how they behave.

    If 'none', shops will not exist; credits will only be used to upgrade weapons.
    If 'standard', each level will contain a shop that is accessible after clearing it. The shop will contain anywhere from 1 to 5 additional checks for the multiworld.
    If 'hidden', shops will behave as above, but will not tell you what you're buying until after you spend credits.
    If 'shops_only', shops will be the only location checks available; items within levels will only contain varying amounts of money for yourself. Note that this mode is designed for "no logic", and is extremely restrictive; you may need to tweak your logic difficulty settings when playing solo.
    """
    display_name = "Shop Mode"
    option_none = 0
    option_standard = 1
    option_hidden = 2
    option_shops_only = 3
    alias_true = 1
    alias_false = 0
    default = 1


class ShopItemCount(NamedRange):
    """The number of shop location checks that will be added.

    All levels are guaranteed to have at least one shop item if there's more shop location checks than levels.
    You may also specify 'always_one', 'always_two', 'always_three', 'always_four', or 'always_five' to guarantee that shops will have exactly that many items.
    """
    display_name = "Shop Item Count"
    range_start = 1
    range_end = 325
    special_range_names = {
        "always_one":   -1,
        "always_two":   -2,
        "always_three": -3,
        "always_four":  -4,
        "always_five":  -5,
    }
    default = 100

    @property
    def current_option_name(self) -> str:
        if self.value <= -1:
            return ["Always One", "Always Two", "Always Three", "Always Four", "Always Five"][abs(self.value) - 1]
        return str(self.value)


class MoneyPoolScale(Range):
    """Change the amount of money in the pool, as a percentage.

    At 100 (100%), the total amount of money in the pool will be equal to the cost of upgrading the most expensive front weapon to the maximum level, plus the cost of purchasing all items from every shop.

    Note that this does not take into account money that you earn while playing levels, so it is safe to set this to a relatively low value.
    """
    display_name = "Money Pool Scaling"
    range_start = 10
    range_end = 200
    default = 80


class BaseWeaponCost(TextChoice):
    """Change the amount that weapons (and, in turn, weapon power upgrades) cost.

    If 'original', weapons will cost the same amount that they do in the original game.
    If 'balanced', prices will be changed around such that generally more powerful and typically used weapons (Laser, etc.) will cost more.
    If 'randomized', weapons will have random prices.

    You may also input a positive integer to force all base weapon prices to that amount.
    """
    display_name = "Base Weapon Cost"
    # This is intentionally not a named range. I want the options to be displayed on web/template.
    # Having a fixed integer value is the more obscure use case, the options are the common one.
    option_original = -1
    option_balanced = -2
    option_randomized = -3
    default = -1

    def verify(self, world: type["World"], player_name: str, plando_options: "PlandoOptions") -> None:
        if isinstance(self.value, int):
            return

        try:
            if int(self.value) >= 0:
                return
        except ValueError:
            pass  # Catch this error and return a more helpful KeyError

        raise KeyError(f"Could not find option '{self.value}' for '{self.__class__.__name__}', "
                       f"known options are {', '.join(self.options)}, <any positive integer>")


# =========================
# === Logic Adjustments ===
# =========================


class LogicDifficulty(Choice):
    """Select how difficult the logic will be.

    If 'beginner', most secret locations will be excluded by default, and additional leeway will be provided when calculating damage to ensure you can destroy things required to obtain checks.
    If 'standard', only a few incredibly obscure locations will be excluded by default. There will always logically be a weapon loadout you can use to obtain checks that your current generator can handle (shields notwithstanding).
    If 'expert', almost all locations will be in logic, and it will be expected that you can manage a weapon loadout that creates a power drain on your current generator.
    If 'master', all locations will always be in logic, and you will also be expected to know technical things like specific triggers for secrets and other minute details. You will be expected to use twiddles if available, and little to no leeway will be provided with damage calculation.
    If 'no_logic', all locations within a level will be assumed attainable if you can access that level at all, with zero regard for loadout or anything else. This is *extremely* dangerous and should be used with caution.
    """
    display_name = "Logic Difficulty"
    option_beginner = 1
    option_standard = 2
    option_expert = 3
    option_master = 4
    option_no_logic = 5
    default = 2


class LogicBossTimeout(Toggle):
    """If enabled, bosses that can be timed out may logically require you to do so; requiring you to dodge them until the level automatically completes to obtain items from a shop afterward."""
    display_name = "Boss Timeout in Logic"


# ===================================
# === Game Difficulty Adjustments ===
# ===================================


class GameDifficulty(NamedRange):
    """Select the base difficulty of the game.

    Anything beyond Impossible (4) is VERY STRONGLY not recommended unless you know what you're doing.
    """
    display_name = "Game Difficulty"
    range_start = 1
    range_end = 8
    special_range_names = {
        "easy": 1,  # 75% enemy health
        "normal": 2,  # 100% enemy health
        "hard": 3,  # 120% enemy health, aimed bullet speed +1
        "impossible": 4,  # 150% enemy health, fast firing, aimed bullet speed +2
        # Difficulty 5: 180% enemy health, fast firing, aimed bullet speed +3
        "suicide": 6,  # 200% enemy health, fast firing, aimed bullet speed +4
        # Difficulty 7: 300% enemy health, fast firing, aimed bullet speed +5
        "lord_of_game": 8,  # 400% enemy health, super fast firing, aimed bullet speed +6

        # Difficulty 9: 800% enemy health, super fast firing, aimed bullet speed +7
        # Playing on difficulty 9 is not feasible due to the insane enemy health, so we disallow it.
    }
    default = 2


class HardContact(Toggle):
    """Direct contact with an enemy or anything else will completely power down your shields and deal armor damage.

    Note that this makes the game significantly harder. Additional "Enemy approaching from behind" callouts will be given throughout the game if this is enabled.
    """
    display_name = "Contact Bypasses Shields"


class ExcessArmor(DefaultOnToggle):
    """Twiddles, pickups, etc. can cause your ship to have more armor than its maximum armor rating.

    Enabling this is vanilla behavior.
    If disabled, a red line over the Armor meter will show the maximum armor level that you are allowed to attain, if not already at maximum armor.
    """
    display_name = "Allow Excess Armor"


# ======================================
# === Visual tweaks and other things ===
# ======================================


class ForceGameSpeed(Choice):
    """Force the game to stay at a specific speed setting, or "off" to allow it to be freely chosen."""
    display_name = "Force Game Speed"
    option_off = 0
    option_slug_mode = 1
    option_slower = 2
    option_slow = 3
    option_normal = 4
    option_turbo = 5
#   option_unbounded = 6
    alias_true = 4
    alias_false = 0
    default = 0


class Christmas(Toggle):
    """Use the Christmas set of graphics and sound effects."""
    display_name = "Christmas Mode"
    # This option is purely visual and audio changes, and has no effect on the way the game plays, or on generation.
    # However, it cannot easily be toggled client-side, because it changes which set of data files are loaded.
    visibility = Visibility.all ^ Visibility.spoiler


class TyrianDeathLink(DeathLink):
    """When you die, everyone else with DeathLink enabled also dies. The reverse is also true.

    Can be toggled off in the Options menu, if enabled.
    """


# =============================================================================


@dataclass
class TyrianOptions(PerGameCommonOptions):
    # ----- Remove from Item Pool ---------------------------------------------
    # This is listed separately from others, so that it follows per-game common options.
    remove_from_item_pool: RemoveFromItemPool

    # ----- Version -----------------------------------------------------------
    enable_tyrian_2000_support: EnableTyrian2000Support

    # ----- Episodes and Goals ------------------------------------------------
    episode_1: GoalEpisode1
    episode_2: GoalEpisode2
    episode_3: GoalEpisode3
    episode_4: GoalEpisode4
    episode_5: GoalEpisode5
    data_cube_hunt: DataCubeHunt
    data_cubes_required: DataCubesRequired
    data_cubes_total: DataCubesTotal
    data_cubes_total_percent: DataCubesTotalPercent

    # ----- Difficulty Options ------------------------------------------------
    difficulty: GameDifficulty
    contact_bypasses_shields: HardContact
    allow_excess_armor: ExcessArmor
    logic_difficulty: LogicDifficulty
    logic_boss_timeout: LogicBossTimeout

    # ----- Other Options -----------------------------------------------------
    local_level_percent: LocalLevelPercent
    add_bonus_games: AddBonusGames
    progressive_items: ProgressiveItems
    specials: Specials
    twiddles: Twiddles
    random_starting_weapon: RandomStartingWeapon
    starting_max_power: StartingMaxPower
    starting_money: StartingMoney
    shop_mode: ShopMode
    shop_item_count: ShopItemCount
    money_pool_scale: MoneyPoolScale
    base_weapon_cost: BaseWeaponCost

    # ----- Visual Tweaks and Other Things ------------------------------------
    force_game_speed: ForceGameSpeed
    christmas_mode: Christmas
    death_link: TyrianDeathLink


tyrian_option_groups = [
    OptionGroup("Version", [
        EnableTyrian2000Support
    ]),
    OptionGroup("Episodes & Goals", [
        GoalEpisode1,
        GoalEpisode2,
        GoalEpisode3,
        GoalEpisode4,
        GoalEpisode5,
        DataCubeHunt,
        DataCubesRequired,
        DataCubesTotal,
        DataCubesTotalPercent
    ]),
    OptionGroup("Difficulty Options", [
        GameDifficulty,
        HardContact,
        ExcessArmor,
        LogicDifficulty,
        LogicBossTimeout
    ]),
    OptionGroup("Other Options", [
        ProgressionBalancing,
        Accessibility,
        LocalLevelPercent,
        AddBonusGames,
        ProgressiveItems,
        Specials,
        Twiddles,
        RandomStartingWeapon,
        StartingMaxPower,
        StartingMoney,
        ShopMode,
        ShopItemCount,
        MoneyPoolScale,
        BaseWeaponCost
    ]),
    OptionGroup("Visual Tweaks & Other Things", [
        ForceGameSpeed,
        Christmas,
        TyrianDeathLink
    ], start_collapsed=True),
    OptionGroup("Item & Location Options", [
        # Other options are automatically added.
        RemoveFromItemPool
    ], start_collapsed=True)
]

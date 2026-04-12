from Options import Range, StartInventoryPool, PerGameCommonOptions, Choice, FreeText, Toggle, DeathLink, \
    DefaultOnToggle, OptionList
from dataclasses import dataclass


class Goal(Choice):
    """
    This determines the goal of the game.
    shadow_queen: Defeat the Shadow Queen.
    crystal_stars: Collect a specified amount of Crystal Stars.
    bonetail: Defeat Bonetail.
    """
    display_name = "Goal"
    option_shadow_queen = 1
    option_crystal_stars = 2
    option_bonetail = 3
    default = 1


class GoalStars(Range):
    """
    This determines how many crystal stars are required to enter the Throne Room in the Palace of Shadow.
    This also determines how many stars are required to goal with the crystal_stars goal selected.
    """
    display_name = "Goal Crystal Stars"
    range_start = 1
    range_end = 7
    default = 7


class PalaceStars(Range):
    """
    This determines how many Crystal Stars are required to enter the Palace of Shadow.
    """
    display_name = "Palace Crystal Stars"
    range_start = 0
    range_end = 7
    default = 7


class RequiredStarsToggle(Toggle):
    """
    Toggles the Required Stars setting.
    This will force the stars selected in Required Stars to be needed to enter the Palace of Shadow.
    Leaving this off will cause the stars needed to be chosen randomly.
    """
    display_name = "Required Stars Selection"


class RequiredStars(OptionList):
    """
    Select which stars are required to enter the Palace of Shadow.
    If you do not toggle this option the stars will be chosen randomly.
    If this has more stars in it than goal stars required, it will use the ones that come first in the list.
    If this has fewer stars in it than goal stars required, it will fill the rest in randomly.
    """
    display_name = "Required Stars"
    valid_keys = ["Diamond Star", "Emerald Star", "Gold Star", "Ruby Star", "Sapphire Star", "Garnet Star", "Crystal Star"]
    default = valid_keys

    def verify(self, world, player_name: str, plando_options) -> None:
        super().verify(world, player_name, plando_options)
        seen = set()
        unique = []
        for star in self.value:
            if star not in seen:
                seen.add(star)
                unique.append(star)
        self.value = unique


class StarShuffle(Choice):
    """
    Crystal Stars will be added as items to the item pool.
    vanilla: Crystal Stars will remain in their original locations.
    stars_only: Crystal Stars will be shuffled into other crystal star locations.
    all: Crystal Stars will be shuffled into any location.
    """
    display_name = "Star Shuffle"
    option_vanilla = 1
    option_stars_only = 2
    option_all = 3
    default = 1


class PitItems(Choice):
    """
    This determines what type of items are in the Pit of 100 Trials.
    vanilla: The locations contain the same items as the original game, and the locations themselves will not be created.
    filler: The locations will be marked as excluded.
    all: The locations can contain any item.
    """
    display_name = "Pit Items"
    option_vanilla = 0
    option_filler = 1
    option_all = 2
    default = 1


class TattleSanityOption(Toggle):
    """
    Creates a location for every enemy being tattled.
    All key items can possibly be placed in these locations.
    """
    display_name = "Tattlesanity"


class Piecesanity(Choice):
    """
    Determines if Star Piece locations will be randomized.
    vanilla: Star Piece locations will remain in their original locations.
    nonpanel_only: Only Star Pieces that are not in panels will be randomized.
    all: All Star Pieces will be randomized.
    """
    display_name = "Star Piecesanity"
    option_vanilla = 0
    option_nonpanel_only = 1
    option_all = 2
    default = 1


class Shopsanity(DefaultOnToggle):
    """
    Shop items will be randomized.
    This includes only regular shops.
    """
    display_name = "Shopsanity"


class ShopPurchaseLimit(Choice):
    """
    This determines which items in the shop will be replenished infinitely when purchasing.
    infinite: All non-progression items in shops can be purchased infinitely.
    consumables_only: Only consumable items can be purchased infinitely.
    badges_only: Only badges can be purchased infinitely.
    limited: No items can be purchased infinitely.
    """
    display_name = "Shop Purchase Limit"
    option_infinite = 0
    option_consumables_only = 1
    option_badges_only = 2
    option_limited = 3
    default = 1


class Shinesanity(DefaultOnToggle):
    """
    Shine Sprites will be randomized.
    """
    display_name = "Shinesanity"


class Keysanity(DefaultOnToggle):
    """
    Chapter specific keys will be added to the item pool.
    Disabling this will place the keys in their own chapters dungeon.
    """
    display_name = "Keysanity"


class DazzleRewards(Choice):
    """
    This determines what type of items are given as rewards by Dazzle.
    vanilla: The rewards are the same as the original game.
    filler: The rewards will be non-progression items.
    all: The rewards can be any item.
    """
    display_name = "Dazzle Rewards"
    option_vanilla = 1
    option_filler = 2
    option_all = 3
    default = 3


class PartnerShuffle(Choice):
    """
    This determines how partners are shuffled.
    vanilla: Partners will be in their original locations.
    shuffled: Partners will be shuffled among each other, but not with other items.
    full_random: Partners can be shuffled into any location.
    """
    display_name = "Partner Shuffle"
    option_vanilla = 1
    option_shuffled = 2
    option_full_random = 3
    default = 1


class StartingPartner(Choice):
    """
    Choose the partner that you start with.
    This settings will not be applied if partner shuffle is set to Vanilla.
    """
    display_name = "Starting Partner"
    option_goombella = 1
    option_koops = 2
    option_bobbery = 3
    option_yoshi = 4
    option_flurrie = 5
    option_vivian = 6
    option_ms_mowz = 7
    default = 1


class LimitChapterLogic(Toggle):
    """
    Progression items will only appear in required chapters, and in common areas. You will not need to
    check the chapters that are out of logic whatsoever. You can still visit them for local items (badges, consumables, etc) if you want or need to.
    """
    display_name = "Limit Chapter Logic"


class LimitChapterEight(Toggle):
    """
    All chapter 8 keys items will be placed in vanilla locations.
    All other locations will have local non-progression items.
    """
    display_name = "Limit Chapter 8"


class BluePipeToggle(DefaultOnToggle):
    """
    Toggle whether the blue pipes in Rogueport Sewers are usable.
    Disabling this will remove the blue switches and the pipes will become inaccessible.
    """
    display_name = "Blue Pipe Warp"


class PalaceSkip(Toggle):
    """
    Entering the Thousand-Year door will take you straight to Grodus.
    """
    display_name = "Palace Skip"


class CutsceneSkip(Toggle):
    """
    Skips some of the longer cutscenes in the game,
    such as the Shadow Queen cutscene, Fahr Outpost Cannon etc.
    """
    display_name = "Skip Cutscenes"


class OpenWestside(Toggle):
    """
    Rogueport Westside is open from the start.
    """
    display_name = "Open West Side"


class GrubbaBribeDirection(Choice):
    """
    Sets how bribing grubba behaves in-game.
    Set if you want grubba to require coins for moving up or down the rankings respectively.
    up_rank_only: Grubba accepts coins to move up the rankings. (20 -> 1). Moving down is free.
    down_rank_only: Grubba accepts coins bribes to move down the rankings. (1 -> 20). Moving up is free.
    both_directions: Grubba accepts coins for moving both up and down the rankings.
    """
    display_name = "Grubba Bribe Direction"
    option_up_rank_only = 0
    option_down_rank_only = 1
    option_both_directions = 2
    default = 2


class GrubbaBribeCost(Range):
    """
    Sets the cost to bribe Grubba to move up the rankings.
    Grubba can be found in his office after your first battle in the glitz pit.
    """
    display_name = "Grubba Bribe Cost"
    range_start = 0
    range_end = 50
    default = 20


class EnemyRandomizer(Choice):
    """
    Toggles the randomization of enemies in battles.
    vanilla: Enemies will be the same as the original game.
    within_chapter: Enemy encounters will be shuffled with other encounters that appear in the same chapter.
    random: Enemy encounters will be shuffled with any other encounter in the game.
    """
    display_name = "Enemy Randomizer"
    option_vanilla = 0
    option_within_chapter = 1
    option_randomize = 2
    default = 0


class EncounterShuffleType(Choice):
    """
    This determines how enemies are grouped when randomizing.
    Enemy randomizer must be set to either within_chapter or random for this option to have an effect.
    vanilla_groups: Enemies will be grouped by encounter, and shuffled as a group.
    custom_groups: Enemies will be shuffled individually, and grouped into new encounters based on their new enemy count.
    """
    display_name = "Enemy Randomizer Grouping"
    option_vanilla_groups = 0
    option_custom_groups = 1
    default = 0


class EnemyStatScaling(Toggle):
    """
    Enemies will have their stats scaled based on the chapter they appear in.
    This option is independent of the Enemy Randomizer option, and will scale enemies even if they are not randomized.
    """
    display_name = "Enemy Stat Scaling"


class ShuffleChapterStats(Toggle):
    """
    Chapter stat scaling values will be shuffled between each other.
    EnemyStatScaling must be enabled for this option to have an effect.
    ie. Chapter 1 enemies could have scaled stats based on chapter 5,
    Chapter 2 enemies could have scaled stats based on chapter 3, etc.
    """
    display_name = "Shuffle Chapter Stats"


class PermanentPeekaboo(Toggle):
    """
    The Peekaboo badge is always active, even when not equipped.
    """
    display_name = "Permanent Peekaboo"


class FullRunBar(Toggle):
    """
    The run bar in battle always starts at 100 percent.
    """
    display_name = "Full Run Bar"


class DisableIntermissions(Toggle):
    """
    After obtaining a crystal star, mario will stay in the boss' room,
    and the sequence will be updated past the intermission.
    """
    display_name = "Disable Intermissions"


class FastTravel(Toggle):
    """
    Enable this to gain the ability to warp to any area you have visited from the map
    screen in the main menu. Press A on the destination to open the warp confirmation dialog.
    """
    display_name = "Fast Travel"


class AlwaysSucceedConditions(Toggle):
    """
    Enable this to make it so the battle condition in fights in the Glitz Pit
    will always be fulfilled, regardless of their actual fulfillment.
    """
    display_name = "Always Succeed Conditions"


class ZeroBPFirstAttack(Toggle):
    """
    The First Attack badge costs 0 BP, just like the remake.
    """
    display_name = "0 BP First Attack"


class BadgeBP(Choice):
    """
    Change the BP cost of all badges.
    This will not affect badges with unique costs such as First Attack, Power Bounce, etc.
    vanilla: All badges will have their normal BP cost.
    shuffled: All badges will have their BP cost shuffled among each other.
    random_costs: All badges will have a random BP cost between 0 and 6.
    """
    display_name = "Badge BP Cost"
    option_vanilla = 0
    option_shuffled = 1
    option_random_costs = 2
    default = 0


class BadgeFP(Choice):
    """
    Change the FP cost of all badges.
    This will not affect badges with unique costs such as Refresh, etc.
    vanilla: All badges will have their normal FP cost.
    shuffled: All badges will have their FP cost shuffled among each other.
    random_costs: All badges will have a random FP cost between 0 and 6.
    """
    display_name = "Badge FP Cost"
    option_vanilla = 0
    option_shuffled = 1
    option_random_costs = 2
    default = 0


class PartnerFP(Choice):
    """
    Change the FP cost of all partners.
    This will not affect partners with unique costs such as Vivian, etc.
    vanilla: All partner abilities will have their normal FP cost.
    shuffled: All partner abilities will have their FP cost shuffled among each other.
    random_costs: All partner abilities will have a random FP cost between 0 and 6.
    """
    display_name = "Partner FP Cost"
    option_vanilla = 0
    option_shuffled = 1
    option_random_costs = 2
    default = 0


class MusicSettings(Choice):
    """
    Choose in-game music settings.
    normal: Music will not change.
    silent: No music will play at all.
    randomized: Music will be randomized.
    """
    display_name = "Music Settings"
    option_normal = 0
    option_silent = 1
    option_randomized = 2
    default = 0


class BlockVisibility(Choice):
    """
    Choose how visible item blocks are.
    normal: All blocks will keep their vanilla visibility.
    all_visible: All blocks will be visible.
    """
    display_name = "Block Visibility"
    option_normal = 0
    option_all_visible = 1
    default = 1


class ExperienceMultiplier(Range):
    """
    Multiplies the experience you gain from battles.
    """
    display_name = "Experience Multiplier"
    range_start = 0
    range_end = 10
    default = 1


class StartingHP(Range):
    """
    How much health you start with.
    """
    display_name = "Starting HP"
    range_start = 1
    range_end = 100
    default = 10


class StartingFP(Range):
    """
    How much flower points you start with.
    """
    display_name = "Starting FP"
    range_start = 0
    range_end = 100
    default = 5


class StartingBP(Range):
    """
    How many badge points you start with.
    """
    display_name = "Starting BP"
    range_start = 0
    range_end = 99
    default = 3


class StartingLevel(Range):
    """
    What level you start at.
    """
    display_name = "Starting Level"
    range_start = 1
    range_end = 99
    default = 1


class StartingCoins(Range):
    """
    How many coins you start with.
    """
    display_name = "Starting Coins"
    range_start = 0
    range_end = 999
    default = 100


class YoshiColor(Choice):
    """
    Select the color of your Yoshi partner.
    """
    display_name = "Yoshi Color"
    option_green = 0
    option_red = 1
    option_blue = 2
    option_orange = 3
    option_pink = 4
    option_black = 5
    option_white = 6
    default = 0


class YoshiName(FreeText):
    """
    Set the name of your Yoshi partner.
    This has a maximum length of 8 characters.
    """
    display_name = "Yoshi Name"
    default = "Yoshi"


@dataclass
class TTYDOptions(PerGameCommonOptions):
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    goal_stars: GoalStars
    palace_stars: PalaceStars
    required_stars_toggle: RequiredStarsToggle
    required_stars: RequiredStars
    star_shuffle: StarShuffle
    tattlesanity: TattleSanityOption
    piecesanity: Piecesanity
    shopsanity: Shopsanity
    shop_purchase_limit: ShopPurchaseLimit
    shinesanity: Shinesanity
    keysanity: Keysanity
    dazzle_rewards: DazzleRewards
    pit_items: PitItems
    limit_chapter_logic: LimitChapterLogic
    limit_chapter_eight: LimitChapterEight
    blue_pipe_toggle: BluePipeToggle
    palace_skip: PalaceSkip
    #partner_shuffle: PartnerShuffle
    cutscene_skip: CutsceneSkip
    disable_intermissions: DisableIntermissions
    fast_travel: FastTravel
    succeed_conditions: AlwaysSucceedConditions
    open_westside: OpenWestside
    grubba_bribe_direction: GrubbaBribeDirection
    grubba_bribe_cost: GrubbaBribeCost
    enemy_randomizer: EnemyRandomizer
    encounter_shuffle_type: EncounterShuffleType
    enemy_stat_scaling: EnemyStatScaling
    shuffle_chapter_stats: ShuffleChapterStats
    permanent_peekaboo: PermanentPeekaboo
    full_run_bar: FullRunBar
    first_attack: ZeroBPFirstAttack
    badge_bp: BadgeBP
    badge_fp: BadgeFP
    partner_fp: PartnerFP
    music_settings: MusicSettings
    block_visibility: BlockVisibility
    experience_multiplier: ExperienceMultiplier
    starting_hp: StartingHP
    starting_fp: StartingFP
    starting_bp: StartingBP
    starting_coins: StartingCoins
    starting_level: StartingLevel
    starting_partner: StartingPartner
    yoshi_color: YoshiColor
    yoshi_name: YoshiName

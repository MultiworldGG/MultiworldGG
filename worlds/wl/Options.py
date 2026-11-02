import typing
from BaseClasses import MultiWorld
from dataclasses import dataclass
from Options import (
    Choice,
    Range,
    Option,
    Toggle,
    DeathLink,
    StartInventoryPool,
    PerGameCommonOptions,
)


def required_garlic_cloves(number: int, percentage: int) -> int:
    return (number * percentage + 99) // 100


class Goal(Choice):
    """
    Determines the goal of the seed
    Genie: Kill the required number of bosses followed by the Genie
    Garlic Hunt: Find a certain number of Garlic Cloves
    """

    display_name = "Goal"
    option_genie = 0
    option_garlic_hunt = 1
    default = 0


class BossesRequired(Range):
    """
    How many Bosses must be defeated in order to defeat the final boss
    """

    display_name = "Bosses Required"
    range_start = 0
    range_end = 6
    default = 6


class ProgressivePowerup(Toggle):
    """
    Whether powerups get unlocked in order or can be found directly as items.
    """

    display_name = "Progressive Powerups"
    default = True


class GetPreviousPowerups(Toggle):
    """
    If powerups are not progressive, if you find jet, all previous powerups will be acquired as well (e.g. garlic, bull, dragon).
    """

    display_name = "GetPreviousPowerups"
    default = False


class StartWithHJ(Toggle):
    """
    High-Jump is active from the start. For people who like going fast.
    """

    display_name = "Start with High-Jump"
    default = False


class RemoveAutoscrollers(Toggle):
    """
    Turn autoscrollers into normal scrolling stages.
    """

    display_name = "Remove Autoscrollers"
    default = False


class BossUnlocks(Toggle):
    """
    Whether boss levels need to be unlocked by items found in the multiworld.
    """

    display_name = "Locked Bosses"
    default = True


class WorldUnlocks(Toggle):
    """
    Whether overworld spots need to be unlocked by items found in the multiworld.
    In a single world multiworld, this is forced to unlock Parsley Woods from the start.
    """

    display_name = "Locked Worlds"
    default = False


class LevelUnlocks(Toggle):
    """
    Create Unlock Items for ordinary courses.
    Locked courses keep their dotted paths and are skipped over when walking.
    Unlocked courses get their white dots on the map.
    Boss courses use the Locked Bosses option.
    """

    display_name = "Locked Courses"
    default = False


class NumberOfGarlicCloves(Range):
    """
    How many Garlic Cloves are in the pool for Garlic Clove Hunt
    """

    display_name = "Total Number of Garlic Cloves"
    range_start = 1
    range_end = 30
    default = 15


class PercentageOfGarlicCloves(Range):
    """
    What Percentage of Garlic Cloves are required to finish Garlic Clove Hunt
    """

    display_name = "Required Percentage of Garlic Cloves"
    range_start = 1
    range_end = 100
    default = 100


class TreasureChecks(Toggle):
    """
    Whether collecting the treasure in levels will grant a check
    """

    display_name = "Treasure Checks"
    default = True


class Blocksanity(Toggle):
    """
    Whether blocks with a face sprite count as checks
    This does include hidden blocks and adds around 550 checks to the game
    For more info check the Blocksanity Tips in:
    https://github.com/randomcodegen/Archipelago_WL/blob/wl-dev/worlds/wl/docs/en_Wario_Land.md
    """

    display_name = "Blocksanity"
    default = False


# class LevelShuffle(Toggle):
#    """
#    Whether levels are shuffled
#    """
#    display_name = "Level Shuffle"
#    default = False


class TrapFillPercentage(Range):
    """
    Replace a percentage of junk items in the item pool with random traps
    """

    display_name = "Trap Fill Percentage"
    range_start = 0
    range_end = 100
    default = 10


class BaseTrapWeight(Choice):
    """
    Base Class for Trap Weights
    """

    option_none = 0
    option_low = 1
    option_medium = 2
    option_high = 4
    default = 2


class StunTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which briefly stuns Wario
    """

    display_name = "Stun Trap Weight"


class TimerTrapWeight(BaseTrapWeight):
    """
    Likelihood of a receiving a trap which causes the timer to get set to 100
    """

    display_name = "Timer Trap Weight"


class DeathTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a trap which causes the player to die
    """

    display_name = "Death Trap Weight"


class GreaseTrapWeight(BaseTrapWeight):
    """
    Likelihood of receiving a greasy trap
    """

    display_name = "Grease Trap Weight"


class MusicShuffle(Toggle):
    """
    Whether level music is shuffled or not.
    """

    display_name = "Music Shuffle"
    default = False


class UseDX(Toggle):
    """Use korxo's DX 1.2 colorization. Needs IPS file \"Wario Land - Super Mario Land 3 DX (World).ips\" """

    display_name = "DX Colorization"
    default = False


class StartingLifeCount(Range):
    """
    How many extra lives to start the game with
    """

    display_name = "Starting Life Count"
    range_start = 1
    range_end = 99
    default = 5


@dataclass
class WLOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    goal: Goal
    bosses_required: BossesRequired
    progressive_powerup: ProgressivePowerup
    get_previous_powerups: GetPreviousPowerups
    start_with_hj: StartWithHJ
    remove_autoscrollers: RemoveAutoscrollers
    boss_unlocks: BossUnlocks
    world_unlocks: WorldUnlocks
    level_unlocks: LevelUnlocks
    number_of_garlic_cloves: NumberOfGarlicCloves
    percentage_of_garlic_cloves: PercentageOfGarlicCloves
    treasure_checks: TreasureChecks
    blocksanity: Blocksanity
    # level_shuffle: LevelShuffle
    trap_fill_percentage: TrapFillPercentage
    stun_trap_weight: StunTrapWeight
    timer_trap_weight: TimerTrapWeight
    death_trap_weight: DeathTrapWeight
    grease_trap_weight: GreaseTrapWeight
    music_shuffle: MusicShuffle
    use_dx: UseDX
    starting_life_count: StartingLifeCount
    death_link: DeathLink

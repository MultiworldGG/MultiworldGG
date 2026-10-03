from dataclasses import dataclass

from Options import Choice, Range, Toggle, PerGameCommonOptions, StartInventoryPool, OptionSet

from .enums import Items
from .stage_data import microgame_data, game_data

class IncludedStages(OptionSet):
    """
    Which stages will be added in the location pool.
    Can be left empty.

    Valid stages:
        - "Introduction"
        - "Jimmy"
        - "Dribble"
        - "Mona"
        - "9-Volt"
        - "Remix 1"
        - "Orbulon"
        - "Dr. Crygor"
        - "Kat"
        - "Remix 2"
        - "Wario"
        - "Easy"
        - "Thrilling"
        - "Hard"
        - "Total Boss"
        - "Sheriff Stage"
        - "Dr. Wario"
        - "Fly Swatter"
        - "Pyoro"
        - "Pyoro 2"
        - "Jump Forever"
        - "Paper Plane Stage"
        - "Skating Board"
    """
    display_name = "Included Stages"
    valid_keys = [game.value for game in game_data.keys()]
    default = [game.value for game in game_data.keys()]


class StartingStage(OptionSet):
    """
    Which of the following stages will be chosen as a potential initial stage.
    The stage has to be in the pool in order to be chosen.
    Can be left empty.

    Valid stages:
        - "Introduction"
        - "Jimmy"
        - "Dribble"
        - "Mona"
        - "9-Volt"
        - "Remix 1"
        - "Orbulon"
        - "Dr. Crygor"
        - "Kat"
        - "Remix 2"
        - "Wario"
        - "Easy"
        - "Thrilling"
        - "Hard"
        - "Total Boss"
        - "Sheriff Stage"
        - "Dr. Wario"
        - "Fly Swatter"
        - "Pyoro"
        - "Pyoro 2"
        - "Jump Forever"
        - "Paper Plane Stage"
        - "Skating Board"
    """
    display_name = "Included Stages"
    valid_keys = [game.value for game in game_data.keys()]
    default = [game.value for game in game_data.keys()]


class StartingMicrogames(Range):
    """
    How many individual microgames will be unlocked by default at the start.
    """
    display_name = "Microgame Count"
    range_start = 4
    range_end = 18
    default = 4


class MicrogameUnlock(Choice):
    """
    How are microgames unlocked.
    * Bundles: Character bundles are added into the pool which unlocks the corresponding set of games
    * Individual: Unlocks for individual microgames are added into the pool
    """
    display_name = "Microgame Unlock"
    option_bundles = 0
    option_individual = 1
    default = 0


class MicrogameCount(Range):
    """
    How many microgames will be considered locations. Selected at random.
    Unselected microgames will not be unlocked.
    At least 2 microgames will be forced per stage and the selection will remain relatively equal across stages.
    """
    display_name = "Microgame Count"
    range_start = 18
    range_end = 213
    default = 36


class ExcludedMicrogames(OptionSet):
    """
    Which microgames will not be considered in the random selection of microgames for the current session.
    """
    display_name = "Excluded Microgames"
    default = []
    valid_keys = [microgame.value for microgame in microgame_data.keys()]

class Flowers(Range):
    """
    How many medals are placed in the item pool.
    Flowers are used to allow you to goal the game which is done by selecting the credits level.
    """
    display_name = "Flowers"
    range_start = 1
    range_end = 50
    default = 30


class FlowersRequired(Range):
    """
    Percentage of medals required to finish the game.
    Result is floored with a minimum of 1.
    """
    display_name = "Medals"
    range_start = 1
    range_end = 100
    default = 75


class MicrogameFlowers(Toggle):
    """
    Enable getting flowers (Hi-Scores) in microgames as valid locations.
    By default every microgame has a location when getting 5 or more score points.
    """
    display_name = "Microgame Flowers"


class StageHiScores(Toggle):
    """
    Enables additional Hi-Score locations for character games.
    These WILL require playing the game again after beating it! May be a nuisance.
    """
    display_name = "Stage Hi-Scores"




@dataclass
class WarioWareOptions(PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool
    included_stages: IncludedStages
    starting_stage: StartingStage
    microgame_unlock: MicrogameUnlock
    flowers: Flowers
    flowers_required: FlowersRequired
    starting_microgames: StartingMicrogames
    excluded_microgames: ExcludedMicrogames
    microgame_flowers: MicrogameFlowers
    microgame_count: MicrogameCount
    stage_hi_scores: StageHiScores
from dataclasses import dataclass
from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle, OptionGroup, StartInventoryPool, Range, Visibility
from .addresses import CAMERA_INVERSION_OPTION_INVERTED, CAMERA_INVERSION_OPTION_NORMAL


class GoalType(Choice):
    """
    Determines what is required to unlock The Rainbow Cloud where Mew (the Goal Condtion) lives.
    Note: If significantly lowering requirements, we recommend disabling the # pokemon and score cehcks
    - signs: What is used in Vanilla Pokemon Snap - spread accross the multiworlds. Can be adjusted.
    - pokemon_pictures: A number of Pokemon Pictures spread accross the multiworlds.  Can be adjusted.
    """
    display_name = "Goal Type"
    default = 1
    option_signs = 0
    option_pokemon_pictures = 1


class WonderfulMewRequired(Toggle):
    """
    Determines if submitting a "Good Technique" photo of Mew is required to win.
    Does nothing if "Good Technique" photos are disabled
    """
    display_name = "'Good Technique' Mew Required"


class SignsRequired(Range):
    """
    Determines the number of Sign Pictures required to unlock the Rainbow Cloud.
    Only matters if Goal Type is set to "Signs"
    """
    display_name = "Signs Required"
    range_start = 1
    range_end = 6
    default = 6


class ExtraSignPictures(Range):
    """
    Determines how many extra Sign Pictures to add to the pool.
    Only matters if Goal Type is set to "Signs"
    """
    display_name = "Extra Sign Pictures"
    default     = 0
    range_start = 0
    range_end   = 6


class PokemonRequired(Range):
    """
    Determines the number of Pokemon Pictures required to unlock the Rainbow Cloud.
    Only matters if Goal Type is set to "Pokemon"
    """
    display_name = "Pokemon Required"
    range_start = 1
    range_end = 63
    default = 50


class ExtraPokemonPictures(Range):
    """
    Determines how many extra Pokemon Pictures to add to the pool.
    Only matters if Goal Type is set to "Pokemon"
    """
    display_name = "Extra Pokemon Pictures"
    default     = 0
    range_start = 0
    range_end   = 20


class GoalItemNamingScheme(Choice):
    """
    Determines how the goal items are named.

    Generic: All goal items will be called "Pokemon Picture"/"Sign Picture"
    Specific: Items will be labeled to specific locations, e.g. "Pokemon Picture: Charmander"/"Sign Picture: Kingler Rock"
    """
    display_name = "Picture Names"
    default = 0
    option_generic = 0
    option_specific = 1


class FilmCapacityStart(Range):
    """
    Sets the amount of film available at the start of the game.
    """
    display_name = "Starting Film"
    range_start = 1
    range_end = 60
    default = 15


class FilmCapacityStep(Range):
    """
    Sets the amount of film granted by each "Film Capacity Upgrade" item.
    """
    display_name = "Film Upgrade Amount"
    range_start = 1
    range_end = 60
    default = 5


class FilmCapacityCap(Range):
    """
    Sets the maximum amount of film available.
    Making this number very small will increase the length of your playthrough.
    """
    display_name = "Maximum Film"
    range_start = 10
    range_end = 60
    default = 60


class ExtraFilmUpgrades(Range):
    """
    Adds the specified number of extra "Film Capacity Upgrade" items to the item pool.
    """
    display_name = "Extra Film Capacity Upgrades"
    range_start = 0
    range_end = 20
    default = 1


class PhotoScoring(Choice):
    """
    Determines how the photo score bonuses, "Good Technique" and "Multiple PKMN", are unlocked.
    - vanilla: Photo score bonuses are available from the start. "Multiple PKMN" score requires "Good Technique."
    - separate: Photo score bonuses are available from the start. "Multiple PKMN" can be scored *without* "Good Technique."
    - progressive_unlocks: Adds "Progressive Scoring" items that unlock "Good Technique" then "Multiple PKMN."
    - separate_unlocks: Adds items that unlock "Good Technique" and "Multiple PKMN" scoring separately.
    """
    display_name = "Photo Scoring"
    option_vanilla             = 0
    option_separate            = 1
    option_progressive_unlocks = 2
    option_separate_unlocks    = 3
    default = 0


class ExtraPhotoScoringItems(Range):
    """
    Adds the specified number of extra scoring bonus items to the pool, making it more likely
    to unlock "Good Technique" and "Multiple PKMN" bonuses earlier.
    
    If `photo_scoring` is set to `vanilla` or `separate`, this does nothing.
    """
    display_name = "Extra 'Photo Score Bonus' Items"
    range_start = 0
    range_end = 2
    default = 0


class MapFragments(Range):
    """
    Determines the number of items required to unlock a course.
    
    Examples:
    - If set to 1, finding the "Beach" item will unlock the Beach course.
    - If set to 2+, you will need that many "Beach: Map Fragment" items to unlock the Beach course.
    """
    display_name = "Map Fragments"
    range_end = 6
    range_start = 1
    default = 1


class UnlockItemsPerCourse(DefaultOnToggle):
    """
    Unlock the Apple, Pester Ball, and PokeFlute for each level separately, rather than every level at once.
    """
    display_name = "Per-Course Item Unlocks"


class FillerItemNamingScheme(Choice):
    """
    Determines how filler items are named. 

    Simple: all filler items will be called "Bad Picture"
    Flavorful: filler items will have flavorful names, e.g. "Faded Photo of Blastoise"
    """
    display_name = "Filler Item Names"
    default = 1
    option_simple = 0
    option_flavorful = 1


class AppleNamingScheme(Choice):
    """
    Determines what the "Apple-Shaped Pokemon Food" unlock is called in the AP world. Has no impact on gameplay.
    """
    display_name = "'Apple-shaped Pokemon Food' Item Name"
    default = 0
    option_apples = 0
    option_pokemon_food = 1


class PhotoBonusChecks(Choice):
    """
    Determines which photo bonuses to include as checks.
    - technique_and_multiple: adds "Good Technique" and "Multiple Pokemon" photos as checks 
    - technique_only: adds "Good Technique" photos as checks
    - none: only normal photos are checks
    """
    display_name = "Include photo bonuses"
    default = 2
    option_none = 0
    option_technique_only = 1
    option_technique_and_multiple = 2


class SpecialPoses(DefaultOnToggle):
    """
    Include the 11 "Special Pose" photos as checks. The special poses are:
    - Beach:   Surfing Pikachu, Pikachu on a Stump, Gust-Using Pidgey
    - Tunnel:  Pikachu on a Ball
    - Volcano: Fighting Magmar
    - River:   Speed Pikachu
    - Cave:    Balloon Pikachu, Flying Pikachu, Jigglypuff on Stage, Jigglypuff Trio on Stage
    - Valley:  Graveler's Group Dance
    """
    display_name = "Include special poses"


class PokemonSigns(DefaultOnToggle):
    """
    Include the 6 Pokemon Sign photos as checks (requires Pokemon Sign Detector).
    """
    display_name = "Include pokemon signs"


class SecretExits(DefaultOnToggle):
    """
    Include taking each of the 3 Secret Exits (Tunnel, River, and Valley) as checks. 
    """
    display_name = "Include secret exits"


class PokemonReportPhotoCount(DefaultOnToggle):
    """
    Include the three photo count rewards from Professor Oak as checks. 
    They are rewarded for having 6, 22, and 40 pictures in your PKMN Report.
    """
    display_name = "PKMN Report Photo Rewards"


class PokemonReportTotalScore(DefaultOnToggle):
    """
    Include the three PKMN Report score checkpoint rewards from Professor Oak as checks. 
    They are rewarded for having a score of 24,000, 72,500, and 130,000 in your PKMN Report.
    """
    display_name = "PKMN Report Score Rewards"


class PoseSanity(Range):
    """
    The number of Pokemon poses to include as checks.
    These are the poses that Oak has a line for, but do not give a "Special Pose" bonus.
    
    Setting this to a high number will make your playthrough much longer. See the Pose FAQ for a guide to each pose.
    Note that some poses are hard/RNG checks, so this number may be adjusted during generation if you do not have those enabled.
    """
    display_name = "Posesanity"
    range_start = 0
    range_end = 141
    default = 0


class DeprecatedIncludeRNGChecks(Toggle):
    """
    This option is deprecated. Please use `include_rng_photos` and/or `include_rng_poses`.
    
    Include the luck-heavy photos as checks. The photos are:
    - [Volcano] Arcanine: Multiple
    - [  River] Cloyster: Multiple and Psyduck: Multiple
    - [ Valley] Magikarp (Valley): Multiple and Dratini: Multiple

    Some regular poses are RNG checks. See the Pose FAQ for a list.
    """
    display_name = "[Deprecated] Include random checks"
    visibility = Visibility.none

class DeprecatedIncludeHardChecks(Toggle):
    """
    This option is deprecated. Please use `include_hard_photos` and/or `include_hard_poses`.
    
    Include the hard photos as checks. They are:
    - [ River] Pikachu (River): Good Technique
    - [  Cave] Zubat (Cave): Multiple, Magikarp (Cave): Wonderful, Balloon Pikachu, and Flying Pikachu
    - [Valley] Staryu: Multiple, Starmie: Multiple, and Goldeen: Good Technique

    Some regular poses are hard checks. See the Pose FAQ for a list.
    """
    display_name = "[Deprecated] Include hard checks"
    visibility = Visibility.none

class IncludeRNGPhotos(Toggle):
    """
    Include the luck-heavy photos as checks. The photos are:
    - [Volcano] Arcanine: Multiple
    - [  River] Cloyster: Multiple and Psyduck: Multiple
    - [ Valley] Magikarp (Valley): Multiple and Dratini: Multiple
    """
    display_name = "Include random photos"


class IncludeRNGPoses(Toggle):
    """
    Include the luck-heavy poses as checks.
    See the Pose FAQ for a list of what poses are considered lucky heavy (tagged "RNG").
    """
    display_name = "Include random poses"


class IncludeHardPhotos(Toggle):
    """
    Include the hard photos as checks. They are:
    - [ River] Pikachu (River): Good Technique
    - [  Cave] Zubat (Cave): Multiple, Magikarp (Cave): Wonderful, Balloon Pikachu, and Flying Pikachu
    - [Valley] Staryu: Multiple, Starmie: Multiple, and Goldeen: Good Technique
    """
    display_name = "Include hard photos"


class IncludeHardPoses(Toggle):
    """
    Include the hard poses as checks.
    See the Pose FAQ for a list of what poses are considered hard (tagged "HARD").
    """
    display_name = "Include hard poses"


class UseHardLogic(Toggle):
    """
    Enable hard logic.
    
    This puts more checks in-logic earlier, with potentially much more difficult requirements. 
    Only enable this option if you are experienced and want a challenge.
    """
    display_name = "Hard logic"


class StartWithDashEngine(DefaultOnToggle):
    """
    Start with the Dash Engine.

    This makes up to six more checks available from the beginning.
    """
    display_name = "Start with Dash Engine"


class PressLToStop(Choice):
    """
    Adds the ability to start/stop the Zero-One by pressing L.
    - start_with: start the game with this ability
    - in_item_pool: add the ability to the item pool
    - disabled: default
    """
    display_name = "Press L to start/stop"

    option_start_with   = 0
    option_in_item_pool = 1
    option_disabled     = 2

    default = 0


class DeprecatedPressLToStop(DefaultOnToggle):
    """
    Deprecated. Use the new option `left_bumper_to_start_stop` instead.
    """
    display_name = "[Deprecated] Press L to start/stop"
    visibility = Visibility.none


class CameraInversion(Choice):
    """
    Choose if the camera controls are Normal or Inverted.
    """
    display_name = "Camera Inversion"

    # DO NOT change these values, they match the values in the ROM
    default = CAMERA_INVERSION_OPTION_NORMAL
    option_inverted = CAMERA_INVERSION_OPTION_INVERTED
    option_normal = CAMERA_INVERSION_OPTION_NORMAL


@dataclass
class PokemonSnapOption(PerGameCommonOptions):
    goal_type: GoalType
    good_technique_mew_photo: WonderfulMewRequired
    signs_required: SignsRequired
    extra_sign_pictures: ExtraSignPictures
    pokemon_required: PokemonRequired
    extra_pokemon_pictures: ExtraPokemonPictures
    goal_item_names: GoalItemNamingScheme

    photo_scoring: PhotoScoring
    extra_photo_scoring_items: ExtraPhotoScoringItems
    starting_film: FilmCapacityStart
    maximum_film:  FilmCapacityCap
    film_upgrade_amount: FilmCapacityStep
    extra_film_upgrades: ExtraFilmUpgrades
    map_fragments: MapFragments
    per_course_items: UnlockItemsPerCourse
    filler_item_names: FillerItemNamingScheme
    pokemon_food_name: AppleNamingScheme

    photo_bonuses: PhotoBonusChecks
    special_poses: SpecialPoses
    pokemon_signs: PokemonSigns
    secret_exits:  SecretExits
    report_photo_count: PokemonReportPhotoCount
    report_score_total: PokemonReportTotalScore
    posesanity: PoseSanity

    rng_checks:  DeprecatedIncludeRNGChecks
    hard_checks: DeprecatedIncludeHardChecks
    include_rng_photos:  IncludeRNGPhotos
    include_rng_poses:   IncludeRNGPoses
    include_hard_photos: IncludeHardPhotos
    include_hard_poses:  IncludeHardPoses
    hard_logic:          UseHardLogic

    start_with_dash_engine: StartWithDashEngine
    left_bumper_to_start_stop: PressLToStop
    enable_left_bumper_to_start_stop: DeprecatedPressLToStop
    camera_inversion: CameraInversion
    start_inventory_from_pool: StartInventoryPool

pokemon_snap_option_groups = [
    OptionGroup("Goal Settings", [
        GoalType,
        WonderfulMewRequired,
        SignsRequired,
        ExtraSignPictures,
        PokemonRequired,
        ExtraPokemonPictures,
        GoalItemNamingScheme,
    ]),
    OptionGroup("Items", [
        PhotoScoring,
        ExtraPhotoScoringItems,
        FilmCapacityStart,
        FilmCapacityCap,
        FilmCapacityStep,
        ExtraFilmUpgrades,
        MapFragments,
        UnlockItemsPerCourse,
        FillerItemNamingScheme,
        AppleNamingScheme,
    ]),
    OptionGroup("Checks - Categories", [
        PhotoBonusChecks,
        SpecialPoses,
        PokemonSigns,
        SecretExits,
        PokemonReportPhotoCount,
        PokemonReportTotalScore,
        PoseSanity
    ]),
    OptionGroup("Checks - Difficulty Settings", [
        IncludeRNGPhotos,
        IncludeRNGPoses,
        IncludeHardPhotos,
        IncludeHardPoses,
        UseHardLogic
    ]),
    OptionGroup("Quality Of Life", [
        StartWithDashEngine,
        PressLToStop,
        CameraInversion,
    ]),
]
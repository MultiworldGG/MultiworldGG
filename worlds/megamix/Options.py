from Options import Toggle, Range, Choice, DeathLink, ItemSet, OptionSet, PerGameCommonOptions, FreeText, \
    Visibility, Removed, OptionGroup
from dataclasses import dataclass

from .MegaMixCollection import MegaMixCollections


class StartingSongs(Range):
    """The number of songs that will be automatically unlocked at the start of a run."""
    range_start = 3
    range_end = 10
    default = 5
    display_name = "Starting Song Count"


class AdditionalSongs(Range):
    """The total number of songs that will be placed in the randomisation pool.
    - This does not count any Starting Songs or the Goal Song.
    - The final song count may be lower due to other settings.

    Given the large range, "random" is not recommended. If you have a 500+ check seed, this is why.
    At a pace of 4 minutes per song (fails, death links, traps, etc.), expect to clear 15 songs/30 checks an hour.
    """
    range_start = 15
    range_end = 3900
    default = 40
    display_name = "Additional Song Count"


class DuplicateSongPercentage(Range):
    """
    After placing required items (Leeks and songs), the percentage of remaining filler slots to become duplicate song items.
    Duplicate songs are considered Useful thus out of logic and may speed up completion time.
    """
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Duplicate Song Percentage"


class AllowMegaMixDLCSongs(Toggle):
    """Whether Extra Song Pack DLC Songs can be chosen as randomised songs."""
    display_name = "Allow Extra Song Pack DLC Songs"


class AutoRemoveCleared(Toggle):
    """If true, automatically removes cleared songs from the song list on refresh.

    This can be done later manually with "/remove_cleared" or toggled with "/auto_remove" in the Client."""
    display_name = "Auto Remove Songs"


class DifficultyModeMin(Choice):
    """Minimum difficulty that a song can be selected from."""
    display_name = "Manual Difficulty Min"
    option_Easy = 0
    option_Normal = 1
    option_Hard = 2
    option_Extreme = 3
    option_ExExtreme = 4
    default = 0


class DifficultyModeMax(Choice):
    """Maximum difficulty that a song can be selected from."""
    display_name = "Manual Difficulty Max"
    option_Easy = 0
    option_Normal = 1
    option_Hard = 2
    option_Extreme = 3
    option_ExExtreme = 4
    default = 4


class DifficultyRatingMin(Choice):
    """Ensures that at least one of the song's available difficulties have this star rating or higher
    x5 = .5, Used since _5 causes issues"""
    display_name = "Manual Rating Min"
    option_one = 0
    option_1x5 = 1
    option_two = 2
    option_2x5 = 3
    option_three = 4
    option_3x5 = 5
    option_four = 6
    option_4x5 = 7
    option_five = 8
    option_5x5 = 9
    option_six = 10
    option_6x5 = 11
    option_seven = 12
    option_7x5 = 13
    option_eight = 14
    option_8x5 = 15
    option_nine = 16
    option_9x5 = 17
    option_ten = 18
    default = 0


class DifficultyRatingMax(Choice):
    """Ensures that at least one of the song's available difficulties have this star rating or lower
    x5 = .5, Used since _5 causes issues"""
    display_name = "Manual Rating Max"
    option_one = 0
    option_1x5 = 1
    option_two = 2
    option_2x5 = 3
    option_three = 4
    option_3x5 = 5
    option_four = 6
    option_4x5 = 7
    option_five = 8
    option_5x5 = 9
    option_six = 10
    option_6x5 = 11
    option_seven = 12
    option_7x5 = 13
    option_eight = 14
    option_8x5 = 15
    option_nine = 16
    option_9x5 = 17
    option_ten = 18
    default = 14


class ScoreGradeNeeded(Choice):
    """Completing a song will require a grade of this value or higher in order to unlock items.
    Accuracy required is based on the song's difficulty (Easy, Normal, Hard, etc.)
    A Perfect requires a full combo, regardless of accuracy.
    A Cheap is completing a song with less than a Standard clear.
    """
    display_name = "Grade Needed"
    option_Cheap = 1
    option_Standard = 2
    option_Great = 3
    option_Excellent = 4
    option_Perfect = 5
    default = 2


class TotalLeeksAvailable(Range):
    """The percentage of Leeks to add to the pool based on the total number of Starting and Additional Songs.
    A higher available Leek percentage leads to more consistent game lengths, but individual Leeks will be less important.

    Example: (5 Starting + 40 Additional Songs) * 20% Leeks Total = 9 Leeks will be available

    Recommended values are between 10 and 40.
    WARNING: Higher values, especially 100, are more suited for solo seeds to replicate the console progression experience.
    """
    range_start = 10
    range_end = 100 # As 100 is approached this greatly puts pressure on progression balancing and slows gen down.
    default = 20
    display_name = "Leek Percentage"


class LeeksRequiredPercentage(Range):
    """The percentage of available Leeks in the item pool that are needed to unlock the Goal Song.

    Example: (5 Starting + 40 Additional Songs) * 20% Leeks Total * 80% Leeks Needed = 7 out of 9 Leeks needed to goal"""
    range_start = 50
    range_end = 100
    default = 80
    display_name = "Leek Percentage Needed to Win"


class GoalSongs(ItemSet):
    """Guarantee one song listed here as the final Goal Song.
    - Difficulty options are ignored.
    - If a Goal Song is also in the Starting Inventory, it will not be chosen as a Goal Song.

    Use /item_groups in the Client for a list of available song groups."""
    display_name = "Goal Song"


class IncludeSongsPercentage(Range):
    """The percentage of the seed reserved for Include Songs.
    - At 50% a 100 song seed will reserve up to 50 Include Songs.
    - If all Include Songs can fit in the given percent they will all appear.
    - Non-Exclude Songs that are not selected stay in the song pool and can still appear.
    - Include and Exclude a song to remove it from the song pool completely if not selected."""
    range_start = 0
    range_end = 100
    default = 100
    display_name = "Include Songs Percentage"


class IncludeSongs(ItemSet):
    """Songs listed here will be guaranteed to be included as part of the seed.
    - Difficulty options are ignored for these songs.
    - If you want these songs immediately, use start_inventory instead.

    Use /item_groups in the Client for a list of available song groups."""
    display_name = "Include Songs"


class ExcludeSongs(ItemSet):
    """Songs listed here and not previously chosen as a Goal or Include will be excluded from being a part of the seed.
    This is recommended instead of exclude_locations which would allow songs to appear but with guaranteed filler checks.

    Use /item_groups in the Client for a list of available song groups."""
    display_name = "Exclude Songs"


class ModData(FreeText):
    """To play with mod songs, set the output of the Mega Mix JSON Generator here."""
    display_name = "MegaMixModData"
    default = ''
    visibility = Visibility.template | Visibility.spoiler


class DivaDeathLink(DeathLink):
    """When you die on your own or fail to reach Grade Needed (not both), everyone who enabled Death Link dies.

    Received Death Links subtract a percentage of total HP. Adjustable in the game mod's config file.
    WARNING: Non-lethal Death Link makes it harder to get Life Bonuses and may affect score by up to 2%.

    This can be toggled later in the Client with "/deathlink".
    """
    display_name = "Death Link"


class DeathLinkAmnesty(Range):
    """Amount of additional own deaths needed before sending one Death Link. 0 would be every death, 1 every other, etc.

    This can be adjusted later in the Client with "/deathlink #" and no upper limit.
    """
    display_name = "Death Link Amnesty"
    range_start = 0
    range_end = 10
    default = 0


class TrapsEnabled(OptionSet):
    """Control which Traps can be placed in the item pool.
    It is highly recommended to add these Traps to non_local_items."""
    display_name = "Traps Enabled"
    valid_keys = {trap for trap in MegaMixCollections.trap_items.keys()}
    default = valid_keys


class TrapPercentage(Range):
    """
    After placing required items and duplicate songs, the percentage of remaining filler slots to become traps.
    If Duplicate Song Percentage is at 100, this option has no effect.
    """
    display_name = "Trap Percentage"
    range_start = 0
    range_end = 100
    default = 0


class ProgressiveHP(Range):
    """
    Divide the HP bar into items and start with 1/X HP. The rest go into the item pool.
    - There may be less based on free space after adding Leeks and Songs.
    - Non-lethal Death Link applies to max available HP
    - For extras use start_inventory

    WARNING: Currently the only logic for this is needing full HP for the Goal Song.
    """
    range_start = 1
    range_end = 20
    default = 1
    display_name = "Progressive HP"


megamix_option_groups = [
    OptionGroup("Game Length", [
        StartingSongs,
        AdditionalSongs,
        DuplicateSongPercentage,
        TotalLeeksAvailable,
        LeeksRequiredPercentage,
    ]),
    OptionGroup("Song Choice", [
        AllowMegaMixDLCSongs,
        GoalSongs,
        IncludeSongsPercentage,
        IncludeSongs,
        ExcludeSongs,
        ModData, # hidden by visibility property
    ]),
    OptionGroup("Song Difficulty", [
        ScoreGradeNeeded,
        DifficultyModeMin,
        DifficultyModeMax,
        DifficultyRatingMin,
        DifficultyRatingMax,
    ]),
    OptionGroup("Game Modifiers", [
        DivaDeathLink,
        DeathLinkAmnesty,
        ProgressiveHP,
        TrapPercentage,
        TrapsEnabled,
    ]),
]


@dataclass
class MegaMixOptions(PerGameCommonOptions):
    allow_megamix_dlc_songs: AllowMegaMixDLCSongs
    auto_remove_songs: AutoRemoveCleared
    duplicate_song_percentage: DuplicateSongPercentage
    starting_song_count: StartingSongs
    additional_song_count: AdditionalSongs
    song_difficulty_min: DifficultyModeMin
    song_difficulty_max: DifficultyModeMax
    song_difficulty_rating_min: DifficultyRatingMin
    song_difficulty_rating_max: DifficultyRatingMax
    grade_needed: ScoreGradeNeeded
    leek_count_percentage: TotalLeeksAvailable
    leek_win_count_percentage: LeeksRequiredPercentage
    goal_song: GoalSongs
    include_songs_percentage: IncludeSongsPercentage
    include_songs: IncludeSongs
    exclude_songs: ExcludeSongs
    megamix_mod_data: ModData
    death_link: DivaDeathLink
    death_link_amnesty: DeathLinkAmnesty
    traps_enabled: TrapsEnabled
    trap_percentage: TrapPercentage
    progressive_hp: ProgressiveHP

    # Deprecated
    exclude_singers: Removed
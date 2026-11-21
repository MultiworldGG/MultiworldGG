import random
from collections import Counter
from dataclasses import dataclass
from enum import Enum, auto
from typing import Mapping, AbstractSet, Any, TypedDict, NotRequired

from Options import (
    PerGameCommonOptions,
    StartInventoryPool,
    Choice,
    Range,
    NamedRange,
    OptionSet,
    DefaultOnToggle,
    Toggle,
    OptionGroup,
    DeathLink,
    ItemDict,
    Removed,
    OptionCounter,
    Option,
)

from .data.areas import ALL_CHAPTER_AREAS, Area, VEHICLE_CHAPTERS, EPISODE_AREA_LOOKUP
from .data.bosses import Boss
from .data.characters import Character
from .data.extras import Extra
from .data.items.all_character_items import SENDABLE_CHARACTER_TO_ITEM_DATA
from .item_groups import ITEM_GROUPS


CHAPTER_OPTION_KEYS: Mapping[str, AbstractSet[Area]] = {
    "All": ALL_CHAPTER_AREAS,
    "Prequel Trilogy": {chapter for chapter in ALL_CHAPTER_AREAS if 1 <= chapter.get_chapter_episode() <= 3},
    "Original Trilogy": {chapter for chapter in ALL_CHAPTER_AREAS if 4 <= chapter.get_chapter_episode() <= 6},
    **{
        f"Episode {episode}": {chapter for chapter in ALL_CHAPTER_AREAS if chapter.get_chapter_episode() == episode}
        for episode in range(1, 7)
    },
    **{
        # todo?: Use get_long_name() instead? Note that some doc-comments will need updating.
        chapter.get_short_name(): {chapter}
        for chapter in sorted(ALL_CHAPTER_AREAS)
    },
}


# Variable names cannot use hyphens, so the options for specific levels are set programmatically.
# option_1-1 = 100
# option_1-2 = 101
# etc.
_CHAPTER_AREA_OPTIONS = {
    f"option_{chapter_area.get_chapter_episode()}-{chapter_area.get_chapter_number_in_episode()}": chapter_area.value
    for chapter_area in sorted(ALL_CHAPTER_AREAS)
}


_BOSS_KEY_TO_BOSS = {
    f"{boss.unique_name} ({boss.area.get_short_name()})": boss for boss in Boss if Boss is not boss.is_alt_boss
}


class ChapterOptionSet(OptionSet):
    valid_keys = list(CHAPTER_OPTION_KEYS.keys())

    @property
    def value_ungrouped(self) -> set[Area]:
        """Ungroup all grouped chapters in .value into a single set of individual chapters."""
        return set().union(*(CHAPTER_OPTION_KEYS[key] for key in self.value))


class ChoiceFromStringExtension(Choice):
    """
    Extends Choice to add a method to set the value from a string option name, similar to constructing a new Choice
    instance with Choice.from_text().
    """
    def set_from_string(self, s: str):
        for k, v in self.name_lookup.items():
            if s == v:
                self.value = k
                return
        raise ValueError(f"{s} is not a valid string for {type(self)}. Expected: {sorted(self.name_lookup.values())}")


class TextColorChoice(ChoiceFromStringExtension):
    _COMMON_DOC_SUFFIX = "\n\n``/color_test`` in the game's client will demonstrate each of the colors in-game."
    option_white_ffffff = 0xFFFFFF  # Location name default
    option_white_green_outline_ffffff = 0xFFFFFF01  # with a green outline
    option_white_red_outline_ffffff = 0xFFFFFF02  # with a red outline
    # option_overbrightened_white = 0xFFFFFF03  # with brighter outlines
    # option_black = 0x000000  # Black is basically unreadable.

    option_bright_red_ff0000 = 0xFF0000
    option_red_de0000 = 0xDE0000  # Trap default.
    option_dark_red_7e0000 = 0x7E0000
    option_darker_red_640000 = 0x640000

    option_red_pink_ff007e = 0xFF007E
    option_magenta_ff00ff = 0xFF00FF

    option_purple_6e00de = 0x6E00DE  # Progression default.
    option_light_blue_purple_7e7eff = 0x7E7EFF

    option_deep_blue_0000ff = 0x0000FF
    option_blue_007eff = 0x007EFF  # Useful default.
    option_dark_blue_00007e = 0x00007E

    option_cyan_00ffff = 0x00FFFF  # Filler default.
    option_dark_cyan_007e7e = 0x007E7E
    option_dark_sea_green_007e76 = 0x007E76
    option_mint_green_7effc0 = 0x7EFFC0  # Player name default.

    option_dark_green_007e00 = 0x007E00
    option_bright_green_00ff00 = 0x00FF00
    option_pea_green_80ff00 = 0x80FF00  # Location name default.

    option_near_white_yellow_feffea = 0xFEFFEA
    option_pale_yellow_ffff7e = 0xFFFF7E
    option_yellow_ffff00 = 0xFFFF00  # Progression + Useful default.
    option_dark_yellow_7e7e00 = 0x7E7E00
    option_orange_ffc000 = 0xFFC000
    option_dark_orange_ff7e00 = 0xFF7E00

    rich_text_doc = True

    def __init_subclass__(cls):
        super().__init_subclass__()
        # Append common docstring parts to the end of the subclass' docstring.
        if not cls.__doc__.endswith(cls._COMMON_DOC_SUFFIX):
            cls.__doc__ = cls.__doc__ + cls._COMMON_DOC_SUFFIX

    @staticmethod
    def colors_from_slot_data(colors_from_slot_data: list[int]) -> tuple[str, str, str, str, str, str, str]:
        default_colors = [
            ProgressionUsefulItemColor.default,
            ProgressionItemColor.default,
            UsefulItemColor.default,
            FillerItemColor.default,
            TrapItemColor.default,
            PlayerNameColor.default,
            LocationNameColor.default,
        ]

        # If the list of colours changes at some point, make sure that reading colors from slot_data is future-proofed.
        if len(colors_from_slot_data) < len(default_colors):
            colors_from_slot_data = colors_from_slot_data + default_colors[len(colors_from_slot_data):]
        elif len(colors_from_slot_data) > len(default_colors):
            colors_from_slot_data = colors_from_slot_data[:len(default_colors)]

        colors = []
        for i, value in enumerate(colors_from_slot_data):
            # Type variables cannot be used in ClassVars, but AP does anyway, so Mypy complains.
            if value in TextColorChoice.name_lookup:  # type: ignore
                color = TextColorChoice(value)
            else:
                color = TextColorChoice(default_colors[i])
            colors.append(color.current_key_no_hex_value)

        # The only reason a tuple of `colors` isn't returned directly, is to make type checkers happy.
        prog_useful, prog, useful, filler, trap, player, location = colors
        return prog_useful, prog, useful, filler, trap, player, location

    @staticmethod
    def colors_to_slot_data(options: "LegoStarWarsTCSOptions") -> tuple[int, int, int, int, int, int, int]:
        return (
            options.progression_useful_item_color.value,
            options.progression_item_color.value,
            options.useful_item_color.value,
            options.filler_item_color.value,
            options.trap_item_color.value,
            options.player_name_color.value,
            options.location_name_color.value,
        )

    @property
    def current_key_no_hex_value(self) -> str:
        return self.current_key[:-7]


class ChapterChoice(ChoiceFromStringExtension):
    """ChoiceFromStringExtension for picking Chapters"""
    # Variable names cannot use hyphens, so the options for specific chapters are set programmatically.
    locals().update(_CHAPTER_AREA_OPTIONS)
    option_random_chapter = -7
    option_random_non_vehicle = -8
    option_random_vehicle = -9
    option_random_episode_1 = -1
    option_random_episode_2 = -2
    option_random_episode_3 = -3
    option_random_episode_4 = -4
    option_random_episode_5 = -5
    option_random_episode_6 = -6

    def is_singular_chapter(self) -> bool:
        return self.value in Area

    def to_area_set(self) -> set[Area]:
        v = self.value
        if v == ChapterChoice.option_random_chapter:
            return set(ALL_CHAPTER_AREAS)
        elif v == ChapterChoice.option_random_non_vehicle:
            return set(ALL_CHAPTER_AREAS).difference(VEHICLE_CHAPTERS)
        elif v == ChapterChoice.option_random_vehicle:
            return set(VEHICLE_CHAPTERS)
        elif -6 <= v <= -1:
            return set(ALL_CHAPTER_AREAS).intersection(EPISODE_AREA_LOOKUP[-v].values())
        else:
            assert self.is_singular_chapter()
            return {Area(self.value)}

    def __bool__(self):
        raise Exception("__bool__ can be confusing with ChapterChoice options because Area.Negotiations (0) is falsey")


class MinikitGoalAmount(NamedRange):
    """
    Require that a number of Minikits must be acquired as part of your goal.

    Once the required number of Minikit items have been received/collected, the Minikit goal is completed according to
    the *Minikit Goal Completion Method* option (defaulting to interacting with the Minikits display in the outside
    junkyard area of the Cantina).

    The number of Minikits required to goal is shown in the Hints shop in the Cantina.

    Current progress towards the goal can be seen on the Pause screen.

    If set to zero, Minikits will not be part of the goal, and will not be included in the item pool.

    If set to non-zero, and Minikit locations are disabled, the *Minikit Bundle Size* will be forcefully set to 10.

    Each enabled episode chapter shuffles 10 Minikits into the item pool, which may be bundled to reduce the number
    Minikit items in the item pool.

    Setting this option to **Use Percentage Option** will use the *Minikit Goal Amount Percentage* option's value to
    determine how many Minikit's are required to goal.
    """
    display_name = "Goal Requires Minikits"
    rich_text_doc = True
    range_start = 0
    range_end = 360
    special_range_names = {
        "use_percentage_option": -1,
        "disabled": 0,
    }
    default = -1


class MinikitGoalAmountPercentage(Range):
    """
    The percentage of Minikits in the item pool that must be acquired as part of your goal.

    10 Minikits are added to the item pool for each enabled episode chapter, which may be bundled to reduce the number
    of individual items.

    This does nothing unless the *Minikit Goal Amount* option is set to *Use Percentage Option* instead of a number.

    The final number of Minikits required to goal is rounded to the nearest integer, but will always be at least 1.
    """
    display_name = "Minikit Goal Amount Percentage"
    rich_text_doc = True
    range_start = 1
    range_end = 100
    default = 75


class MinikitGoalCompletionMethod(ChoiceFromStringExtension):
    """
    Choose how the Minikit Goal is completed.

    **Instant:** The Minikit Goal is completed as soon as you have enough Minikit items to meet your goal. It is
    recommended to enable a Goal Chapter when the Minikit Goal Completion Method is set to Instant.

    **Junkyard Minikit Display:** Once you have enough Minikit items to meet your goal, the goal must be completed by
    using the Minikit Display in the outside Junkyard area of the Cantina.

    """
    display_name = "Minikit Goal Completion Method"
    rich_text_doc = True
    option_instant = 1
    option_junkyard_minikit_display = 2
    default = 2


# "Level" used here is as a user-facing term. The correct internal name is "Area". Internally, a "Level" refers to a
# separately loaded section of an "Area".
class CompleteLevelsGoalAmountPercentage(NamedRange):
    """
    Require that a percentage of enabled Chapters and Gold Brick Door Bonuses (if Bonuses are enabled) must be completed
    as part of your goal.

    The final number of levels that must be completed to goal is rounded to the nearest integer, but will always be at
    least 1 if the percentage is greater than 0.

    Current progress towards the goal can be seen on the Pause screen.
    """
    display_name = "Goal Requires Level Completion Percentage"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    special_range_names = {
        "disabled": 0,
    }
    default = 0


class GoalRequiresKyberBricks(Toggle):
    """
    Require that 7 Kyber Brick items must be acquired as part of your goal.

    The 7 Kyber Brick items only contribute to your goal and do nothing else. There are only 7 added to the item pool
    when this option is enabled.

    It is recommended to enable a Goal Chapter when the Kyber Bricks Goal is enabled.

    Current progress towards the goal can be seen on the Pause screen.
    """
    display_name = "Goal Requires 7 Kyber Bricks"
    rich_text_doc = True


class KyberBrickGoalCompletionMethod(ChoiceFromStringExtension):
    """
    Set how the Kyber Brick part of the Goal is completed.

    **Instant:** The Kyber Brick goal is completed as soon as 7 Kyber Brick items are acquired. It is recommended to
    enable a Goal Chapter when the Kyber Brick Goal Completion Method is set to Instant.

    """
    display_name = "Kyber Brick Goal Completion Method"
    rich_text_doc = True
    option_instant = 1
    default = 1


class GoalChapterLocationsMode(ChoiceFromStringExtension):
    """
    Choose how locations within the Goal Chapter are generated.

    **Removed:** Locations within the Goal Chapter are removed from the multiworld. Gold Bricks from the Goal Chapter
    will not be included in Gold Brick logic.

    **Excluded:** Locations within the Goal Chapter are marked as Excluded, disallowing Progression and Useful items
    being placed there. Gold Bricks from the Goal Chapter will not be included in Gold Brick logic. Locations accessible
    from both the Goal Chapter and from some other enabled Chapter, will also be marked as Excluded.

    **Normal:** No changes will be made to the locations in the Goal Chapter, or to Gold Brick logic. Not recommended
    unless playing without ``!release`` after goaling.

    """
    display_name = "Goal Chapter Locations Mode"
    rich_text_doc = True
    option_removed = 1
    option_excluded = 2
    option_normal = 3
    default = 1


class GoalChapter(ChoiceFromStringExtension):
    """Choose a Goal Chapter that must be completed as the final part of your goal.

    All other goal requirements must be completed to unlock the Goal Chapter, in addition to the Goal Chapter's usual
    unlock requirements.

    The Goal Chapter, when enabled, is picked separately from regular Chapters, ignoring the *Chapters To Pick From*
    option used when picking regular Chapters.

    The Goal Chapter is enabled in addition to your *Enabled Chapter Count*, when possible.

    The Goal Chapter does not contribute towards other goals, it does not add Minikit items to the item pool, and will
    never contain an enabled boss.

    Selecting ``Random Chapter`` will pick any chapter at random, as if you had used weights to set the weight of
    ``No Goal Chapter`` to zero and the weight of every other chapter to the same number greater than zero. It is
    recommended to use one of the special random options for the Starting Chapter when using ``Random Chapter``,
    otherwise there is a chance that the Goal Chapter can roll the same chapter as the Starting Chapter, which is not
    allowed.

    Selecting ``Random Enabled Chapter`` will pick one of your enabled chapters at random.

    Selecting ``Random Enabled Non Boss Chapter`` will pick one of your enabled chapters at random, excluding those that
    are allowed to contain an Enabled Boss for the Defeat Bosses Goal.

    """
    display_name = "Goal Requires a Goal Chapter"
    rich_text_doc = True
    option_no_goal_chapter = -1
    # Variable names cannot use hyphens, so the options for specific levels are set programmatically.
    locals().update(_CHAPTER_AREA_OPTIONS)
    option_random_chapter = -2
    option_random_enabled_chapter = -3
    option_random_enabled_non_boss_chapter = -4
    default = -1
    _random_chapter_picks = list(_CHAPTER_AREA_OPTIONS.values())

    class ToBeDetermined(Enum):
        RANDOM_ENABLED_TO_BE_DETERMINED = auto()
        RANDOM_ENABLED_NON_BOSS_TO_BE_DETERMINED = auto()

    def __init__(self, value: int):
        if value == GoalChapter.option_random_chapter:
            # Pick a random chapter instead.
            value = random.choice(self._random_chapter_picks)
        super().__init__(value)

    def to_area(self) -> Area | None | ToBeDetermined:
        if self.value == GoalChapter.option_no_goal_chapter:
            return None
        if self.value == GoalChapter.option_random_enabled_chapter:
            # to be determined.
            return self.ToBeDetermined.RANDOM_ENABLED_TO_BE_DETERMINED
        if self.value == GoalChapter.option_random_enabled_non_boss_chapter:
            # to be determined.
            return self.ToBeDetermined.RANDOM_ENABLED_NON_BOSS_TO_BE_DETERMINED
        if self.value == GoalChapter.option_random_chapter:
            raise AssertionError("Goal Chapter instances set to `random_chapter` should not be instantiable")
        return Area(self.value)

    @classmethod
    def from_area(cls, area: Area):
        return cls(area.value)


class DefeatBossesGoalAmount(NamedRange):
    """
    Choose how many bosses must be defeated as part of completing your goal.

    If set to disabled, bosses will not be part of the goal.

    **The Chapter a boss is in must be completed for defeating the boss to count.**

    The bosses that count towards your goal are shown in the Hints shop in the Cantina.

    Current progress towards the goal can be seen on the Pause screen. Individual progress within an Episode can be seen
    by standing in front of the door to that Episode once a Chapter within that Episode is unlocked.
    """
    display_name = "Goal Requires Bosses"
    rich_text_doc = True
    range_start = 0
    range_end = len(_BOSS_KEY_TO_BOSS)
    special_range_names = {
        "disabled": 0,
    }
    default = 0


class EnabledBossesCount(Range):
    """
    Choose the number of bosses that will be present in the world and count towards your goal.

    More chapters containing bosses than this count can end up in the generated world. If this happens, some of them
    will not count towards the goal.

    This will automatically be set at least as high as the number of bosses required to goal.

    This will automatically be set no higher than the maximum of the number of boss chapters in *Chapters To Pick From*.
    """
    display_name = "Bosses To Enable"
    rich_text_doc = True
    range_start = 0
    range_end = len(_BOSS_KEY_TO_BOSS)


class AllowedBosses(OptionSet):
    """
    Choose bosses that count towards the Defeat Bosses Goal.

    When bosses must be defeated as part of the goal, the Chapters for the bosses in this list will be added to the
    *Chapters To Pick From* list if they are not already in the *Chapters To Pick From* list.

    ::

        allowed_bosses:
        - Darth Maul (1-6) # Darth Maul
        - Zam Wesell (2-1) # Bounty Hunter Pursuit
        - Jango Fett (2-2) # Discovery On Kamino
        - Jango Fett (2-4) # Jedi Battle
        - Count Dooku (2-6) # Count Dooku
        - Count Dooku (3-2) # Chancellor In Peril
        - General Grievous (3-3) # General Grievous
        - Anakin Skywalker (3-6) # Darth Vader
        - Imperial Spy (4-3) # Mos Eisley Spaceport
        - Death Star (4-6) # Rebel Attack
        - Darth Vader (5-4) # Dagobah
        - Darth Vader (5-5) # Cloud City Trap
        - Boba Fett (5-6) # Betrayal Over Bespin
        - Rancor (6-1) # Jabba's Palace
        - Boba Fett (6-2) # The Great Pit Of Carkoon
        - Darth Sidious (6-5) # Jedi Destiny
        - Death Star II (6-6) # Into The Death Star
    """
    display_name = "Bosses To Pick From"
    rich_text_doc = True
    valid_keys = list(_BOSS_KEY_TO_BOSS.keys())
    default = list(_BOSS_KEY_TO_BOSS.keys())

    def to_areas(self) -> set[Area]:
        return {_BOSS_KEY_TO_BOSS[key].area for key in self.value}


class OnlyUniqueBossesCountTowardsGoal(ChoiceFromStringExtension):
    """
    When enabled, only unique boss characters will count towards your goal. Defeating the same boss character in two
    separate Chapters will only count as one boss kill.

    When unique bosses are enabled, the maximum number of bosses that can count towards the goal will be reduced to 13,
    or 12 when Anakin Skywalker counts as the same boss as Darth Vader.
    """
    display_name = "Only Count Unique Bosses"
    rich_text_doc = True
    option_disabled = 0
    option_enabled = 1
    option_enabled_and_count_anakin_as_vader = 2


class MinikitBundleSize(ChoiceFromStringExtension):
    """
    Minikit items in the item pool are bundled into items individually worth this number of Minikits.

    Low bundle sizes can cause generation times to increase and are more likely to result in generation failing with a
    FillError when generating Lego Star Wars: The Complete Saga on its own, or with other games that can struggle to
    place all items.

    Low bundle sizes also mean fewer filler items in the item pool.
    """
    display_name = "Minikit Bundle Size"
    rich_text_doc = True
    option_individual = 1
    alias_1 = 1
    option_2 = 2
    option_5 = 5
    option_10 = 10
    default = 5


class EnabledChaptersCount(Range):
    """Choose how many chapters will exist in your slot.

    Chapters, other than the Starting Chapter and Goal Chapter, if enabled, will be randomly picked from the Allowed
    Chapters list.

    If there are fewer *Chapters To Pick From* than the count to enable, all the *Chapters To Pick From* will be
    enabled, and the count will be reduced to the maximum possible.
    """
    display_name = "Chapters To Enable"
    rich_text_doc = True
    range_start = 1
    range_end = 36
    default = 18


class AllowedChapterTypes(ChoiceFromStringExtension):
    """Specify additional filtering of the chapters that can exist in your slot.

    **All:** No additional filtering, all chapters specified in the *Chapters To Pick From* option are allowed.

    **No Vehicles:** No vehicle chapters (1-4, 2-1, 2-5, 3-1, 4-6, 5-1, 5-3, 6-6) will be allowed to exist in your slot.
    """
    display_name = "Allowed Chapter Types"
    rich_text_doc = True
    option_all = 0
    option_no_vehicles = 1
    default = 0


class AllowedChapters(ChapterOptionSet):
    """Choose the chapter levels that are allowed to be picked when randomly choosing which chapters will exist in your
    slot.

    The Starting Chapter and Goal Chapter options ignore the allowed list of chapters when they are set to specific
    chapters.

    When your goal is set to require defeating bosses, all Allowed Boss Chapters will be added into the Allowed
    Chapters option.

    Individual chapters can be specified, e.g. "1-1", "5-4".

    Special values:

    - "All": All chapters will be allowed.
    - "Prequel Trilogy": All chapters in episodes 1, 2 and 3 will be allowed.
    - "Original Trilogy": All chapters in episode 4, 5 and 6 will be allowed.
    - "Episode {number}": e.g. "Episode 3" will allow all chapters in Episode 3, so 3-1 through to 3-6.

    Examples::

        # Enable only 1-1 (Negotiations)
        allowed_chapters:
          - 1-1

        # Enable all
        allowed_chapters:
          - All

        # A mix of values
        allowed_chapters:
          - Prequel Trilogy
          - Episode 4
          - 5-2
          - 5-3
          - 6-5
    """
    display_name = "Chapters To Pick From"
    rich_text_doc = True
    default = frozenset({"All"})


class PreferredChapters(ChapterOptionSet):
    """
    When the generator picks which chapters should exist in your slot, it will pick from these preferred chapters first.

    If a preferred chapter is not allowed to be picked because it is not included in the *Chapters To Pick From* option,
    it will not be picked.

    This option can be used to guarantee that certain chapters are present in a generated world.

    Individual chapters can be specified, e.g. "1-1", "5-4".

    Special values:

    - "Prequel Trilogy": All chapters in episodes 1, 2 and 3 will be preferred.
    - "Original Trilogy": All chapters in episode 4, 5 and 6 will be preferred.
    - "Episode {number}": e.g. "Episode 3" will make all chapters in Episode 3, so 3-1 through to 3-6, be preferred.

    Examples::

        # Prefer vehicle levels
        preferred_chapters:
          - 1-4
          - 2-2
          - 2-5
          - 3-1
          - 4-6
          - 5-1
          - 5-3
          - 6-6

        # A mix of values
        preferred_chapters:
          - Prequel Trilogy
          - Episode 4
          - 5-2
          - 5-3
          - 6-5
    """
    display_name = "Preferred Chapters"
    rich_text_doc = True
    # There is no point to using "All" for Preferred Chapters, so remove it from the valid_keys.
    valid_keys = [key for key in ChapterOptionSet.valid_keys if key != "All"]
    default = frozenset()


class PreferEntireEpisodes(Toggle):
    """
    When enabled, after the generator has picked a chapter to exist in your slot, out of the *Chapters To Pick From*, it
    will continue picking additional chapters from the same episode until it runs out of chapters to pick from that
    episode.

    For example, if the generator picks 3-2 as the first enabled chapter, its next picked chapters will be guaranteed to
    be picked from the *Chapters To Pick From* out of 3-1, 3-3, 3-4, 3-5 and 3-6.

    The Starting Chapter is always the first picked enabled chapter.

    With all chapters allowed to exist in your slot, and an Enabled Chapters Count set to a multiple of 6, this option
    will result in whole episodes being enabled.
    """
    display_name = "Prefer Entire Episodes"
    rich_text_doc = True


class EnableMinikitLocations(DefaultOnToggle):
    """
    Enable locations for collecting each Minikit in each Chapter that exists in your slot.

    If Minikit locations are not enabled, but the goal requires Minikit items, the Minikit Bundle Size will be
    forcefully set to 10.

    When Minikit locations are not enabled, Bonus levels will not consider the Gold Bricks, awarded for getting all 10
    Minikit locations in a Chapter, as part of Gold Brick logic.
    """
    display_name = "Minikit Locations"
    rich_text_doc = True


class EnableTrueJediLocations(DefaultOnToggle):
    """
    Enable locations for completing True Jedi in each Chapter that exists in your slot.

    Some True Jedi locations logically expect 1 Progressive Score Multiplier because they are otherwise too difficult or
    impossible with only the minimal characters to complete the Chapter:

    - 1-6
    - 2-6
    - 3-3
    - 3-5
    - 3-6
    - 5-1
    - 5-2
    - 5-6
    - 6-5

    The logic for difficult True Jedi is intended to be reworked in the future to account for additional characters
    giving access to more studs within a Chapter, therefore making True Jedi easier to complete.

    When True Jedi locations are not enabled, Bonus levels will not consider True Jedi Gold Bricks as part of Gold Brick
    logic.
    """
    display_name = "True Jedi Locations"
    rich_text_doc = True


class EnableStoryCharacterUnlockLocations(DefaultOnToggle):
    """
    Enable locations for unlocking Story mode characters that would normally unlock when completing a Chapter/Bonus in
    vanilla.

    In vanilla, completing any Chapter/Bonus with C-3PO as a playable Story mode character would unlock C-3PO. In
    vanilla, Chapters within an Episode unlock in order, so this would mean completing either 2-3, 4-1, 5-2, 6-1 or A
    New Hope. However, the AP randomizer allows for Chapters to be unlocked out-of-order, so, additionally, completing
    any of 4-2, 4-3, 4-4, 4-5, 5-6, 6-2 or 6-4, would also send the Story Character Unlock location for C-3PO.

    Only the first Chapter/Bonus completed that would unlock a Story mode character will send the Unlock location for
    that character.

    Because Story mode is skipped in the AP randomizer, these character unlock locations are sent when the Chapters are
    completed in Free Play, except the Pod Race and Gunship Cavalry bonus levels which only have Story mode.

    With all 36 Chapters enabled, this adds 56 locations.
    With all 36 Chapters and all Bonuses enabled, this adds 57 locations.
    """
    display_name = "Level Completion Character Unlocks"
    rich_text_doc = True


class EnableBonusLocations(Toggle):
    """
    The Bonuses Door in the Cantina has a number of levels that require Gold Bricks to access. When this option is
    enabled, completing each of these Bonus levels (in Free Play if they have Free Play) will be a location to
    check.

    Additionally, watching the Lego Indiana Jones trailer (it can be skipped once started), and purchasing Indiana Jones
    from the shop are added as locations to check.

    Gold Brick logic currently only counts Gold Bricks earned from Chapter completion, True Jedi, 10/10 Minikits in a
    Chapter, and the singular Gold Bricks awarded for completing other Bonus levels. The True Jedi and 10/10 Minikits
    Gold Bricks are not included in Gold Brick logic if the corresponding locations are disabled.

    Depending on other options, not all Chapters could exist in your slot, so if there are not enough Gold Bricks
    logically available for a Bonus level to be accessible, that Bonus level will not be included in the multiworld.

    With all Bonuses included in the multiworld, this adds 8 locations.
    """
    display_name = "Bonuses"
    rich_text_doc = True


class EnableAllEpisodesCharacterPurchaseLocations(Toggle):
    """
    Enable the expensive character purchase locations for *IG-88*, *Dengar*, *4-LOM*, *Ben Kenobi (Ghost)*,
    *Anakin Skywalker (Ghost)*, *Yoda (Ghost)* and *R2-Q5*.

    In vanilla, these locations unlock after completing Story mode for every chapter, but the AP randomizer changes
    these shop purchases to unlock according to the All Episodes Character Purchase Requirements option.

    Even when the locations are disabled, the vanilla characters, *IG-88*, *Dengar* etc. may still be added to the item
    pool.

    Attempting to purchase the vanilla characters from the shop while the locations are disabled will not unlock the
    vanilla characters.

    This adds 7 locations.
    """
    display_name = "'All Episodes' Character Purchases"
    rich_text_doc = True


class Ridesanity(Toggle):
    """
    Enable locations for riding each unique type of ridable 'character' (creature, vehicle, turret, crane control) in
    the game.

    This notably adds a few extra locations to the LEGO City and New Town bonus levels.

    If none of your enabled levels contain a specific ridable character, then the location riding for that character
    will not exist in the generated world.

    Ridesanity adds up to 28 locations.

    There are 28 unique ridable characters:

    - AT-AT (6-3)
    - AT-ST (4-3, 6-3, 6-4, LEGO City)
    - Bantha (4-2, LEGO City, New Town)
    - Basketball Cannon (New Town)
    - Big Skiff Cannon (6-2)
    - B'omarr Monk (6-1)
    - Cantina Car (Cantina)
    - Clone Walker (3-4, New Town)
    - Cloud Car (5-6, LEGO City, New Town) (the red car)
    - Crane Control (4-1, 4-4, 4-5, 5-5, 5-6) (also controls Magnets, Window Cleaners and Turbolasers)
    - Dewback (4-2, 4-3, LEGO City, New Town)
    - Ewok Catapult (6-4)
    - Firetruck (New Town)
    - Flash Speeder (1-5)
    - Landspeeder (4-2, 4-3, LEGO City, New Town)
    - Lifeboat (New Town)
    - Moon Car (4-1, LEGO City, New Town) (the orange car)
    - Mos Eisley Cannon (4-3) (used to get a Minikit)
    - Service Car (1-5, 1-6, 4-5) (the floating car with no wheels)
    - Skiff Cannon (6-2)
    - Speeder Bike (6-3)
    - Snowmobile (5-2)
    - STAP (1-1)
    - Stormtrooper Cannon (5-2, 5-5)
    - Tauntaun (5-2, LEGO City, New Town)
    - Town Car (4-1, LEGO City, New Town) (the white van-like car)
    - Tractor (5-4, 6-4, LEGO City, New Town)
    - Wookie Flyer (LEGO City)

    """
    display_name = "Ridesanity Locations"
    rich_text_doc = True


class EnableNonPowerBrickExtraLocations(DefaultOnToggle):
    """
    Enable locations for purchasing the Extras from the shop that do not require Power Bricks to unlock, and allow those
    Extras to be shuffled into the item pool.

    Adds 7 locations usually accessible from the start.

    These are:

    - Purchase Extra Toggle
    - Purchase Fertilizer
    - Purchase Disguise
    - Purchase Daisy Chains
    - Purchase Chewbacca Carrying C-3PO
    - Purchase Tow Death Star
    - Purchase Beep Beep

    They are all classified as Filler items, except Extra Toggle, which may be Useful or Progression depending on your
    logic options.

    If this option is not enabled, the locations will still exist in the multiworld, but will always contain their
    vanilla items.
    """
    display_name = "Non Power Brick Extra Purchases"
    rich_text_doc = True


# Not Implemented.
class EnableCompletionPointLocations(Toggle):
    """
    Enable locations for progressively increasing your total completion points. Completion points are how the game
    tracks your completion percentage. There are 816 completion points earned across many actions in the game:

    Episodes:

    - 6 points per chapter (see below)
    - Completing the Minikit bonus
    - Completing the Character bonus
    - Completing Superstory

    Chapters:

    - Completing a chapter in Story mode
    - Getting all 10 Minikits in a chapter
    - Completing True Jedi for a chapter (worth 2 points instead of 1)
    - Completing the Challenge for a chapter
    - Getting the Power Brick for a chapter

    Shop:

    -

    Other:

    - Completing a Bonus level
    """


class ChapterUnlockRequirement(ChoiceFromStringExtension):
    """Choose how Chapters within an Episode are unlocked.

    The requirements to access and complete your starting Chapter will be given to you at the start.

    The items you are missing to unlock a Chapter are shown in-game when standing in-front of a locked Chapter's door.

    **Vanilla Characters:** A Chapter unlocks once its Vanilla characters (those from Story mode, or optionally those
    that are available for Purchase after completing the Chapter in Vanilla) have been found/received. The count
    required to unlock the Chapter can be adjusted with a separate option.

    **Chapter Item:** A Chapter unlocks after receiving an unlock item specific to that Chapter, e.g. "Chapter 2-3
    Unlock".

    **Random Characters:** Each Chapter requires randomly chosen characters to unlock.

    **Open (not implemented):** All chapters within an Episode are unlocked as soon as the Episode is unlocked.

    """
    display_name = "Chapter Unlock Requirements"
    rich_text_doc = True
    alias_story_characters = 0  # Backwards compatibility.
    option_vanilla_characters = 0  # Partially implemented with overly restrictive logic. Needs a logic rewrite.
    option_chapter_item = 1  # Partially implemented with overly restrictive logic. Needs a logic rewrite.
    option_random_characters = 2  # Partially implemented with overly restrictive logic. Needs a logic rewrite.
    # option_open = 3  # Needs the ability to limit characters to only being usable within a specific episode/
    default = 0

    def is_characters(self):
        return self.value in (self.option_vanilla_characters, self.option_random_characters)


class ChapterUnlockCharactersMinRequiredCount(Range):
    """When Chapters are locked by needing specific Characters, choose the minimum number of Characters that are needed.

    If Chapters are set to require Vanilla Characters to unlock, the required count for a Chapter will never be more
    than the number of Vanilla Characters for that Chapter.

    The starting Chapter will always use this minimum required count.

    Most chapters have a maximum of around 3 to 5 Characters.
    The highest vanilla Story mode Characters requirement, is 7, for The Great Pit Of Carkoon (6-2).
    The highest vanilla Purchase Characters requirement, is 9, for Jedi Battle (2-4).

    This option does nothing if Chapters are not set to require Vanilla/Random Characters to unlock.
    """
    display_name = "Min Required Count"
    rich_text_doc = True
    range_start = 1
    range_end = 5
    default = 1


class ChapterUnlockCharactersMaxRequiredCount(Range):
    """When Chapters are set to unlock by needing specific Characters, choose the maximum number of Characters that are
    needed.

    If Chapters are set to require Vanilla Characters to unlock, the required count for a Chapter will never be more
    than the number of Vanilla Characters for that Chapter.

    The Goal Chapter, if enabled, will always use this maximum required count.

    Most chapters have a maximum of around 3 to 5 Characters.
    The highest vanilla Story mode Characters requirement, is 7, for The Great Pit Of Carkoon (6-2).
    The highest vanilla Purchase Characters requirement, is 9, for Jedi Battle (2-4).

    This option does nothing if Chapters are not set to require Vanilla/Random Characters to unlock.
    """
    display_name = "Max Required Count"
    rich_text_doc = True
    range_start = 1
    range_end = 9
    default = 5


class ChapterUnlockCharactersRequiredCountDistribution(ChoiceFromStringExtension):
    """When the Max Required Count is greater than the Min Required Count, choose how the generator randomly picks
    between the Min and the Max.

    **Uniform:** Pick between the Min and Max with equal chance.

    **Low:** More likely to pick lower values, similar to random-range-low-{min}-{max}.

    **Middle:** More likely to pick values in the middle of the range, similar to random-range-middle-{min}-{max}.

    **High:** More like to pick higher values, similar to random-range-high-{min}-{max}.

    """
    display_name = "Required Count Distribution"
    rich_text_doc = True
    option_uniform = 0
    option_low = 1
    option_middle = 2
    option_high = 3
    default = option_uniform


class ChapterUnlockRandomCharactersMinExtraPoolCount(Range):
    """When Chapters are set to unlock by needing randomly chosen Characters, increase the number of characters that
    contribute to unlocking a Chapter by at least this many.

    For example, if a Chapter rolls as requiring 4/4 Characters to unlock it, and this option is set to 1, an additional
    Character will be added to the Chapter's requirements, but the number of characters required will remain at 4, so
    any 4/5 of the Chapter's requirements will unlock the Chapter.

    The maximum number of Characters that can be included in a Chapter's unlock requirements is capped at 9 because
    the in-game text that displays what Characters unlock a Chapter becomes squished and difficult to read when there
    are many Characters.
    """
    display_name = "Min Additional Random Characters"
    rich_text_doc = True
    range_start = 0
    range_end = 3
    default = 0


class ChapterUnlockRandomCharactersMaxExtraPoolCount(Range):
    """When Chapters are set to unlock by needing randomly chosen Characters, increase the number of characters that
    contribute to unlocking a Chapter by up to this many.

    For example, if a Chapter rolls as requiring 4/4 Characters to unlock it, and this option is set to 1 (and the
    minimum extra is set to 0), there will be a 50% chance (0 or 1) that an additional Character will be added to the
    Chapter's requirements, but the number of characters required will remain at 4, so any 4/5 of the Chapter's
    requirements will unlock the Chapter.

    The maximum number of Characters that can be included in a Chapter's unlock requirements is capped at 9 because
    the in-game text that displays what Characters unlock a Chapter becomes squished and difficult to read when there
    are many Characters.
    """
    display_name = "Max Additional Random Characters"
    rich_text_doc = True
    range_start = 0
    range_end = 3
    default = 2


class ChapterUnlockRandomCharactersUniquePerChapter(Range):
    """When Chapters are set to unlock by needing randomly chosen Characters, choose how many unique characters can be
    randomly picked from to be used in Chapter unlock requirements. The option value is multiplied by the number of
    Chapters that exist in your slot.

    For example, if this option is set to 3, and you have 18 Chapters enabled, then the total number of unique
    Characters that Chapter unlock requirements will pick from will be 3 * 18 = 54 Characters.

    Lower values will result in characters more often being used in unlock requirements for many Chapters.

    Higher values will result in characters more often being used in unlock requirements for only 1 or 2 Chapters.

    The characters are picked at random, so it is possible that some unique characters won't get picked for a single
    Chapter.

    Comparing against setting chapters to require Vanilla Characters to unlock:

    - With all 36 Chapters enabled and set to require vanilla Story Characters to unlock, there would be 56 unique
      Characters total, averaging 1.555 unique Characters per Chapter, with Chapters averaging 3.361 unique Characters
      in their unlock requirements.
    - With all 36 Chapters enabled and set to require vanilla Purchase Characters, where possible, or Story Characters
      otherwise, there would be 102 unique Characters total, averaging 2.833 unique Characters per Chapter, with
      Chapters averaging 2.944 unique Characters in their unlock requirements.

    """
    display_name = "Unique Characters In Requirements, Per Chapter"
    rich_text_doc = True
    range_start = 1
    range_end = 6
    default = 2


class ChapterStoryUnlockCharactersNotRequired(OptionSet):
    """When the unlock requirement for Chapters is set to Story Characters, disable specific commonly required Story
    Characters from contributing towards unlocking Chapters.

    ``R2-D2``, ``C-3PO`` and ``Chewbacca`` are the only characters supported by this option because of the large number
    of Chapters they can each lock access to.

    Note that the ``{episode}-{chapter} Story Unlock Characters`` item groups will still include these characters, even
    if the characters are set to not be required.

    Example that disables all three::

    - R2-D2 # can lock up to 15 Chapters.
    - C-3PO # can lock up to 11 Chapters.
    - Chewbacca # can lock up to 9 Chapters.

    This option only affects Chapters that are set to require Story Characters to unlock.
    """
    display_name = "Remove Story Characters From Unlock Requirements"
    rich_text_doc = True
    _name_to_character = {c.readable_name: c for c in (Character.C_3PO, Character.R2_D2, Character.CHEWBACCA)}
    valid_keys = frozenset(_name_to_character.keys())
    default = frozenset()

    def to_character_set(self) -> set[Character]:
        return {self._name_to_character[name] for name in self.value}


class ChaptersThatCanRequirePurchaseCharacters(OptionSet):
    """When the unlock requirement for Chapters is set to Vanilla Characters, instead of requiring the Story Characters
    to unlock these Chapters, chapters can instead be set to require the Characters that would, in the vanilla game,
    become available for purchase from the Cantina Shop after completing the Chapter.

    A common use of this is to give some Chapters within the same Episode more varied unlock requirements because it is
    common for many Chapters within an Episode to require some of the same Story Characters.

    Not all Chapters, in the vanilla game, make Characters available for purchase from the Cantina Shop after completing
    the Chapter, so these chapters are not available for this option:

    - 1-5
    - 2-5
    - 2-6
    - 3-6
    - 4-5
    - 5-1
    - 5-4
    - 5-5
    - 6-3

    All other Chapters can be specified using their shorthand names, for example::

    - 1-2  # Change 1-2 to require Captain Tarpals and Boss Nass
    - 3-5  # Change 3-5 to require Mace Windu (Episode III) and Disguised Clone
    - 5-3  # Change 5-3 to require TIE Bomber and Imperial Shuttle

    This option does nothing if Chapters are not set to require Story Characters to unlock.
    """
    display_name = "Allow Requiring Purchase Characters"
    rich_text_doc = True
    REVERSE_LOOKUP: dict[str, Area] = {
        # todo?: Use get_long_name() instead?
        chapter.get_short_name(): chapter
        for chapter in sorted(ALL_CHAPTER_AREAS) if chapter.get_purchase_characters()
    }
    valid_keys = frozenset(REVERSE_LOOKUP.keys())
    default = sorted(valid_keys)

    def to_area_set(self) -> set[Area]:
        """Ungroup all grouped chapters in .value into a single set of individual chapters."""
        return {self.REVERSE_LOOKUP[v] for v in self.value}


class RequirePurchaseCharactersInsteadOfStoryCharactersChance(NamedRange):
    """Set the chance that a chapter rolls as requiring vanilla Purchase Characters to unlock instead of vanilla Story
    Characters.

    Only affects chapters that have been allowed to require vanilla Purchase Characters, instead of vanilla Story
    characters, to unlock."""
    display_name = "Require Purchase Characters Chance"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    special_range_names = {
        "use_custom_chance_per_chapter_option": -1,
    }
    default = 0


class RequirePurchaseCharactersInsteadOfStoryCharactersCustomChance(OptionCounter):
    """Individually set the chance that a chapter rolls as requiring Purchase Characters to unlock instead of Story
    Characters.

    Will not do anything unless Require Purchase Characters Chance is set to Use Custom Chance Per Chapter Option.

    A Chapter not being present in this option is the same as giving it a 0% chance.
    """
    display_name = "Require Purchase Characters Chance: Custom"
    rich_text_doc = True
    min = 0
    max = 100
    valid_keys = ChaptersThatCanRequirePurchaseCharacters.valid_keys
    default = dict.fromkeys(sorted(valid_keys), 50)

    def to_area_counter(self) -> Counter[Area]:
        return Counter({ChaptersThatCanRequirePurchaseCharacters.REVERSE_LOOKUP[k]: v for k, v in self.value.items()})


class EpisodeUnlockRequirement(ChoiceFromStringExtension):
    """Choose how Episodes are unlocked.

    The game client forces open all Episode doors in the Cantina, but all Chapters within an Episode will remain locked
    if an Episode unlock item is required to unlock the Episode.

    The Episode of your starting Chapter will always be unlocked from the start.

    **Open:** All Episodes will be unlocked from the start.

    **Episode Item:** Each Episode will unlock after receiving an unlock item for that Episode, e.g. "Episode 5 Unlock".
    Warning: Episode unlock items typically lock access to about 1/6 of your game each, which can result in long periods
    of not being able to do any checks when playing in multiworlds with other players.

    """
    display_name = "Episode Unlock Requirements"
    rich_text_doc = True
    option_open = 0
    option_episode_item = 1
    default = 0


class AllEpisodesCharacterPurchaseRequirements(ChoiceFromStringExtension):
    """The vanilla unlock requirements for purchasing IG-88, Dengar, 4-LOM, Ben Kenobi (Ghost), Anakin Skywalker
    (Ghost), Yoda (Ghost) and R2-Q5 from the shop, are completing every Story mode chapter. The randomizer changes this
    unlock condition because completing every Story mode chapter is unreasonable in most multiworlds and is impossible
    if not all chapters are enabled.

    **Episodes Unlocked:** The shop purchases will unlock when the "Episode # Unlock" item for each Episode with enabled
    Chapters has been received. If the Episode Unlock Requirement is set to Open or there is only 1 enabled Episode,
    this will be forcefully changed to "Episodes Tokens" instead.

    **Episodes Tokens:** 6 "Episode Completion Token" items need to be acquired to unlock the characters for purchase.
    The number of "Episode Completion Token" items in the item pool is equal to your number of enabled chapters divided
    by 6 and rounded to the nearest integer, but always at least 1. The remaining "Episode Completion Token" items will
    be added to your starting inventory. For example, if you have 28 chapters enabled, 28 / 6 = 4.666 -> 5 in the pool
    and 1 in your starting inventory.

    """
    display_name = "'All Episodes' Character Purchase Unlock Requirements"
    rich_text_doc = True
    option_episodes_unlocked = 1
    option_episodes_tokens = 2
    default = 2


class StartingChapter(ChapterChoice):
    """
    Choose the starting chapter.

    Items required to access and complete the starting chapter will be given to you from the start.
    """
    display_name = "Starting Chapter"
    rich_text_doc = True
    default = ChapterChoice.option_random_chapter


# Not Implemented. Todo: Remove all requirements from the starting chapter.
class RandomStartingLevelMaxStartingCharacters(Range):
    """Specify the maximum number of starting characters allowed when picking a random starting level.

    - 1 Character: 1-4, 2-1, 2-5, 5-1 (all vehicle levels)
    - 2 Characters: 1-6, 2-2, 3-1 (v), 3-3, 3-4, 3-5, 3-6, 4-6 (v), 5-3 (v), 5-5, 6-3, 6-5, 6-6 (v)
    - 3 Characters: 1-1, 1-2, 2-6
    - 4 Characters: 1-3, 2-3, 2-4, 3-2, 4-2, 5-2, 5-4, 5-6
    - 5 Characters: 4-1
    - 6 Characters: 1-5, 4-3, 4-4, 4-5, 6-1, 6-4
    - 7 Characters: 6-2"""
    display_name = "Random Starting Chapter Max Starting Characters",
    rich_text_doc = True
    range_start = 2
    range_end = 7
    default = 7


class PreferredCharacters(OptionSet):
    """
    Specify characters that the generator should try to always include in the item pool.

    When the number of enabled Chapters is reduced from the maximum, the number of items to add to the item pool is also
    reduced, so not all characters may get added to the item pool.

    The names of all items can be found by starting the Lego Star Wars: The Complete Saga client and entering the
    ``/items`` command.

    If no vehicle Chapters are enabled, no vehicle characters will be included in the item pool.
    """
    display_name = "Preferred Characters"
    rich_text_doc = True
    valid_keys = {char.name for char in SENDABLE_CHARACTER_TO_ITEM_DATA.values()}
    default = frozenset({
        # Highest base movement speed or non-Extra-Toggle characters, lots of glitches.
        "Droideka",
        # Lots of glitches, also a ghost.
        "Yoda (Ghost)",
        # High Jump + Triple jump glitch can get a lot of vertical height.
        # Grevous' Bodyguard can reach similar heights, and has higher movement speed, but has a super-high single jump
        # + slam double jump, so cannot get as much horizontal distance compared to General Grievous.
        "General Grievous",
    })


class PreferredExtras(OptionSet):
    """
    Specify Extras that the generator should try to always include in the item pool.

    When the number of enabled Chapters is reduced from the maximum, the number of items to add to the item pool is also
    reduced, so not all Extras may get added to the item pool.

    The names of all items can be found by starting the Lego Star Wars: The Complete Saga client and entering the
    ``/items`` command.

    Score Multipliers that are logically required, due to the Most Expensive Purchase With No Score Multiplier option,
    will always be included in the item pool.

    Preferring "Score x{number}" to be included in the item pool will try to ensure there are enough Progressive Score
    Multiplier items to unlock that score multiplier.
    """
    display_name = "Preferred Extras"
    rich_text_doc = True
    # Progressive Score Multiplier is an AP-specific item, and this option does not support specifying multiple of
    # an item, so the individual "Score x{number}" Extras are included as valid keys instead.
    valid_keys = {extra.readable_name for extra in Extra if extra.is_purchasable()}
    # todo: Use a default the maintains order.
    default = frozenset({
        # todo: Replace the string literals with Extra.<name>.readable_name
        # SITH access
        "Dark Side",
        # BOUNTY_HUNTER access (silver bricks only)
        "Exploding Blaster Bolts",
        # BLASTER access (grapple only)
        "Force Grapple Leap",
        # BOUNTY_HUNTER access (silver bricks only)
        "Self Destruct",
        # BOUNTY_HUNTER access (silver bricks only)
        "Super Ewok Catapult",
        # BLASTER, GRAPPLE and IMPERIAL access, also speeds up levels with Mouse Droids
        "Extra Toggle",

        # Speed up playing:
        # Useful for survivability/True Jedi, especially in vehicle chapters, and a few places where hostile NPCs can be
        # used to activate buttons.
        "Deflect Bolts",
        # Useful for survivability/True Jedi and a few places where NPCs can be used to activate buttons
        "Disarm Troopers",
        # Useful for speeding up playing through chapters
        "Fast Force",
        # Useful for speeding up playing through chapters
        "Fast Build",
        # Useful for speeding up playing through chapters
        "Infinite Torpedos",
        # Useful for survivability/True Jedi and a few places where hostile NPCs can be used to activate buttons.
        "Invincibility",
        # All score multipliers are useful for speeding up Studs farming and getting True Jedi
        "Score x2",
        "Score x4",
        "Score x6",
        "Score x8",
        "Score x10",
        # Useful for speeding up playing through chapters and getting True Jedi
        "Stud Magnet",
    })


class StartWithDetectors(DefaultOnToggle):
    """Start with the Minikit Detector and Power Brick Detector unlocked.

    When these Extras are enabled, the locations of Minikits and Power Bricks in the current level are shown with
    arrows."""
    display_name = "Start With Detector Extras"
    rich_text_doc = True


class FillerReserveCharacters(DefaultOnToggle):
    """
    When enabled, reserve space in the item pool for at least as many Characters as enabled locations that would
    normally unlock Characters in vanilla.

    When disabled, the only reserved space in the item pool for Characters will be the Characters needed to reach all
    locations. Additional Characters will only get added to the item pool through the Filler Weight: Characters option.
    """
    display_name = "Filler Reserve: Characters"
    rich_text_doc = True


class FillerReserveExtras(DefaultOnToggle):
    """
    When enabled, reserve space in the item pool for at least as many Extras as enabled locations that would normally
    unlock Extras in vanilla.

    When disabled, the only reserved space in the item pool for Extras will be the Extras needed to reach all locations.
    Additional Extras will only get added to the item pool through the Filler Weight: Extras option.
    """
    display_name = "Filler Reserve: Extras"
    rich_text_doc = True


class FillerWeightCharacters(Range):
    """
    This option controls the weight of characters when choosing which items to fill out the rest of the space in the
    item pool. A higher weight in comparison to the other Filler Weight options results in more characters in the item
    pool, compared to other items used to fill out the rest of the item pool.
    """
    # Many characters are just reskins of another character, and the generator already guarantees that the item pool
    # contains enough characters to reach every location. There are also often many character unlocks for each chapter
    # completed.
    display_name = "Filler Weight: Characters"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 10


class FillerWeightExtras(Range):
    """
    This option controls the weight of Extras when choosing which items to fill out the rest of the space in the
    item pool. A higher weight in comparison to the other Filler Weight options results in more Extras in the item
    pool, compared to other items used to fill out the rest of the item pool.
    """
    # There is only one Extra reserved in the item pool per chapter and Extras tend to have unique effects, so the
    # default weight is higher.
    display_name = "Filler Weight: Extras"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 30


class FillerWeightJunk(Range):
    """
    This option controls the weight of Studs, Power Ups and other junk filler Archipelago items when choosing which
    items to fill out the rest of the space in the item pool. A higher weight in comparison to the other Filler Weight
    options results in more Studs and other filler Archipelago items in the item pool, compared to other items used to
    fill out the rest of the item pool.

    The weight of each Junk Filler item can be controlled with the separate Junk Weights option.
    """
    display_name = "Filler Weight: Junk"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 30


class JunkWeights(ItemDict):
    """Control the weight of each Junk Filler item.

    If all weight are set to zero, all Junk will be Blue Studs.

    Purple Studs give 10000 Studs when received.
    Blue Studs give 1000 Studs when received.
    Gold Studs give 100 Studs when received.
    Silver Studs give 10 Studs when received.
    Received studs are multiplied by unlocked Score Multipliers and any active Power Up.

    Power Up items give 20 seconds of invincibility, 2x score multiplier and a number of other beneficial effects.
    Power Up items will not be used while in the Cantina, LEGO City, New Town or Battle Over Coruscant (3-1).
    Unused Power Up items do not carry over to the next play session.
    """
    display_name = "Junk Weights"
    rich_text_doc = True
    valid_keys = ITEM_GROUPS["Junk"]
    default = {
        "Power Up": 15,
        "Silver Stud": 1,
        "Gold Stud": 5,
        "Blue Stud": 50,
        "Purple Stud": 15,
    }


class UncapOriginalTrilogyHighJump(Toggle):
    """Original Trilogy Chapters, Bonuses and the Cantina cap High Jump height to about the same as a Jedi double jump
    because they were not designed for being able to High Jump.

    Enabling this option will remove the cap, restoring High Jump height to the same as seen in Prequel Trilogy
    Chapters.
    """
    display_name = "Uncap Original Trilogy High Jump"
    rich_text_doc = True


class EasierTrueJedi(Toggle):
    """When enabled, the True Jedi requirements in Free Play will be set to the Story True Jedi requirement, which is
    usually less.

    True Jedi in Free Play usually has higher requirements than True Jedi in Story and can be very difficult, if not
    impossible, with just the Story characters for that Chapter.

    Without this option enabled, the following Chapters will gain a logical requirement for Score x2 due to their
    difficulty/impossibility of achieving True Jedi in Free Play with just the Story characters for the Chapter:

    - 1-6
    - 2-6
    - 3-3
    - 3-5
    - 3-6
    - 5-1
    - 5-2
    - 5-6
    - 6-5
    """
    display_name = "Easier True Jedi"
    rich_text_doc = True


class ScaleTrueJediWithScoreMultipliers(Toggle):
    """Scale True Jedi requirements with the number of Progressive Score Multipliers acquired.

    If Easier True Jedi is not enabled, the True Jedi that logically require Score x2 will also scale but only with
    Score x4 and higher.

    The scaling is applied only when entering a Chapter and will not adjust dynamically if you receive/find additional
    Progressive Score Multiplier items while within the entered Chapter.

    Very high True Jedi requirements will visually break the True Jedi bar shown on screen, but progress towards True
    Jedi is still being counted.
    """
    display_name = "Scale True Jedi With Multipliers"
    rich_text_doc = True


# todo: Override random behaviour to be logarithmic, or just reject 'random' for this option because it will too often
#  pick way too high values.
class MostExpensivePurchaseWithNoScoreMultiplier(NamedRange):
    """
    The most expensive individual purchase the player can be expected to make without any score multipliers, *in
    thousands of Studs* (number of Blue Studs).

    For example, an option value of 100 means that purchases up to 100,000 studs in price can be expected to be
    purchased without any score multipliers.

    The logical requirements for expensive purchases will scale with this value. For example, if a purchase of up to
    100,000 Studs is expected with no score multipliers, then a purchase of 100,001 up to 200,000 Studs is expected with
    a score multiplier of 2x.

    "Score x2" costs 1.25 million studs (1250 * 1000) in vanilla, so, for a more vanilla experience with potentially
    more farming for Studs, set this option to 1250.

    The most expensive purchase is "Score x10", which costs 20 million studs (20000 * 1000). Setting this options to
    20000 means that all purchases are logically expected without score multipliers.
    """
    display_name = "Most Expensive Purchase Without Score Multipliers"
    rich_text_doc = True
    default = 100
    # Max purchase cost is 20_000_000
    # 5 * 1000 * 3840 = 19_200_000 -> 5 is too low
    # 6 * 1000 * 3840 = 23_040_000 -> 6 is the minimum allowed
    range_start = 6
    range_end = 20000
    special_range_names = {
        "minimum_(6000_studs)": 6,
        "10000_studs": 10,
        "25000_studs": 25,
        "50000_studs": 50,
        "75000_studs": 75,
        "default_(100000_studs)": 100,
        "250000_studs": 250,
        "500000_studs": 500,
        "750000_studs": 750,
        "1_million_studs": 1000,
        "vanilla_(1.25_million_studs)": 1250,
        "2.5_million_studs": 2500,
        "5_million_studs": 5000,
        "7.5_million_studs": 7500,
        "10_million_studs": 10000,
        "no_score_multipliers_expected": 20000,
    }


class CharacterMaxHealth(Range):
    """Set the max health for non-vehicle characters. The vanilla max health for all characters is 4."""
    display_name = "Character Max Health"
    rich_text_doc = True
    _VANILLA = 4
    range_start = 1
    range_end = 10
    default = _VANILLA


class VehicleMaxHealth(Range):
    """Set the max health for vehicle characters. The vanilla max health for all characters is 4."""
    display_name = "Vehicle Max Health"
    rich_text_doc = True
    _VANILLA = 4
    range_start = 1
    range_end = 10
    default = _VANILLA


class ReceivedItemMessages(ChoiceFromStringExtension):
    """
    Determines whether an in-game notification is displayed when receiving an item.

    Note: Dying while a message is displayed results in losing studs as normal, but the lost studs do not drop, so
    cannot be recovered.
    Note: Collecting studs while a message is displayed plays the audio for collecting Blue/Purple studs, but this has
    no effect on the received value of the studs collected.

    **All:** Every item shows a message.

    **None:** All items are received silently.

    """
    display_name = "Received Item Messages"
    rich_text_doc = True
    default = 1
    option_none = 0
    option_all = 1
    option_progression = 2


class CheckedLocationMessages(ChoiceFromStringExtension):
    """
    Determines whether an in-game notification is displayed when checking a location.

    Note: Dying while a message is displayed results in losing studs as normal, but the lost studs do not drop, so
    cannot be recovered.
    Note: Collecting studs while a message is displayed plays the audio for collecting Blue/Purple studs, but this has
    no effect on the received value of the studs collected.

    **All:** Every checked location shows a message

    **None:** No checked locations show a message

    """
    display_name = "Checked Location Messages"
    rich_text_doc = True
    default = 1
    option_none = 0
    option_all = 1


class ProgressionUsefulItemColor(TextColorChoice):
    """
    Choose the color used to display the names of items that have both the Progression classification and the Useful
    classification.
    These are typically the most powerful progression items for a game.
    """
    display_name = "Progression + Useful Item Color"
    default = TextColorChoice.option_yellow_ffff00


class ProgressionItemColor(TextColorChoice):
    """Choose the color used to display Progression classification item names."""
    display_name = "Progression Item Color"
    default = TextColorChoice.option_purple_6e00de


class UsefulItemColor(TextColorChoice):
    """Choose the color used to display Useful classification item names."""
    display_name = "Useful Item Color"
    default = TextColorChoice.option_blue_007eff


class FillerItemColor(TextColorChoice):
    """Choose the color used to display Filler classification item names."""
    display_name = "Filler Item Color"
    default = TextColorChoice.option_cyan_00ffff


class TrapItemColor(TextColorChoice):
    """Choose the color used to display Trap classification item names."""
    display_name = "Trap Item Color"
    default = TextColorChoice.option_red_de0000


class PlayerNameColor(TextColorChoice):
    """Choose the color used to display player names in Received Item and Checked Location messages."""
    display_name = "Player Name Color"
    default = TextColorChoice.option_mint_green_7effc0


class LocationNameColor(TextColorChoice):
    """Choose the color used to display location names in Received Item and Checked Location messages."""
    display_name = "Location Name Color"
    default = TextColorChoice.option_white_ffffff


class ShopTrapAsFakeProgressionChance(Range):
    """The chance that a Trap classification item in the shop instead shows as a fake Progression item.

    Items that are a mix of the Trap classification and another classification are unaffected."""
    display_name = "Shop Fake Trap Item Chance"
    rich_text_doc = True
    range_start = 0
    range_end = 100
    default = 50


class AutoCollectSpawnedPickups(ChoiceFromStringExtension):
    """Automatically collect pickups (studs and hearts) spawned by destroying objects/enemies, using the force on
    objects, or spawned by other means, such as from dying or from the Character Studs Extra.

    This option can be adjusted at any time in the client with ``/auto_collect_pickups <on/off/vehicles>``.

    Minikits, and other pickups that internally start off hidden, and get unhidden, rather than spawned in, are not
    affected.

    When enabled, Power Up pickups no longer spawn from destroyed/forced objects, an active Power Up will not double the
    value of spawned studs (though score multiplier Extras still work).

    Levels that already automatically collect spawned pickups, in the vanilla game, such as *Mos Espa Pod Race* and
    *LEGO City*, are unaffected by this option.

    **Disabled:** Spawned pickups must be collected as normal.

    **Enabled:** Spawned pickups will be automatically collected as soon as they spawn.

    **Vehicle Levels Only:** Spawned pickups will be automatically collected in vehicle levels, and must be collected as
    normal in other levels.
    """
    display_name = "Auto-collect Spawned Pickups"
    rich_text_doc = True
    option_disabled = 0
    option_enabled = 1
    option_vehicle_levels_only = 2
    default = option_disabled


# Expert/Super Expert text kept for future use.
# - Expert (not implemented):
#
#   - This difficulty, if implemented, will probably try to match Expert difficulty in ViolaGuy's standalone TCS
#     randomizer.
#
# - Super Expert (not implemented):
#
#   - This difficulty, if implemented, will probably try to match Super Expert difficulty in ViolaGuy's standalone TCS
#     randomizer.
class LogicDifficulty(ChoiceFromStringExtension):
    # noinspection LongLine
    """
        - **None** - Tries to match developer intended strategies, for players new to the game:

          - Includes some combat logic for avoidable/ignorable enemies.
          - Extras (except Score Multipliers for expensive purchases) are not included in logic.

        - **Normal** - No glitches expected, for players that have played most of the vanilla content:

          - Expects more platforming that probably wasn't developer intended, but is generally quite obvious and simple.
          - Logic expects the use of Extras, for example:

            - *Self Destruct*, *Exploding Blaster Bolts*, and *Super Ewok Catapult* can be expected for destroying Silver Brick objects.
            - *Force Grapple Leap* can be expected to use Grapple points.
            - *Dark Side* can be expected to use Sith Force.

          - 1P2C (1 Player, 2 Controllers) usage is limited to pressing only a single button on each controller simultaneously. E.g. 2-player Sith Force puzzles when *Dark Side* is unlocked, but no Sith are unlocked (e.g. the last Minikit in *Discovery On Kamino* (2-2)).
          - 1P2C can expect teleporting one player to the other through a drop-in, to activate buttons etc. where the AI won't follow you due to the AI only being able to use specific characters, and then dropping out again to let the AI continue as normal.

        - **Moderate** - Simpler glitches expected, for players that play the Archipelago randomizer often and are willing to learn simpler tricks:

          - Slam-jumps, e.g. Jedi-Triple-Jump, included in logic.
          - Expects more platforming off of terrain.
          - Easy 'oil glitches' (getting a Stormtrooper to activate an Imperial panel for you) that don't require coercing a Stormtrooper into position.
          - 1P2C (1 Player, 2 Controllers) usage additionally includes fully controlling only one character at a time, taking turns between controlling each character, e.g. button platforms in 2-2 and 2-6 when the AI won't follow you

        - **Hard** - More difficult jumps and tricks, for players starting to learn speedrun tricks (installing *BrickBench* to assist in learning tricks is recommended):

          - Some out-of-bounds tricks may be in logic (mostly Yoda Clips through ceilings). Full out-of-bounds movement, e.g. walking around under the level, is *not* included.
          - Yoda Grabs.
          - Drop-in warps (none are currently present in the logic).
          - TIE gate, and drag bomb wall, skips using loop drop-ins.
          - More difficult 'oil glitches' that require coercing a Stormtrooper into position.
          - 1P2C (1 Player, 2 Controllers) usage additionally includes fully controlling both characters simultaneously.
        """
    display_name = "Logic Difficulty"
    rich_text_doc = True
    # - Expert: Includes many out-of-bounds clips and more difficult 1P2C.
    # Comparable to Glitched logic in ViolaGuy's TCS randomizer.
    # - Super Expert: Super Jumps, DV3 Skip, CCT door clip and more. Comparable to Super Glitched logic in ViolaGuy's
    # standalone TCS randomizer.
    option_none = 0
    option_normal = 1
    option_moderate = 2
    option_hard = 3
    # option_expert = 4
    # option_super_expert = 5

    @property
    def normal_plus(self) -> bool:
        return self.value >= self.option_normal

    @property
    def moderate_plus(self) -> bool:
        return self.value >= self.option_moderate

    @property
    def hard_plus(self) -> bool:
        return self.value >= self.option_hard


class LogicExpectNonInfiniteTorpedoesPodRacer21(Toggle):
    """When enabled, logic can expect making progress in Bounty Hunter Pursuit (2-1) with only Pod Racers unlocked, by
    gathering Torpedoes from within the level. This can be much slower than in other vehicle levels.
    """
    display_name = "2-1 Expects Gathering Torpedoes With Pod Racers"
    rich_text_doc = True

# Not using DeathLinkMixin currently because the docstring needs to be different.
class LegoStarWarsTCSDeathLink(DeathLink):
    __doc__ = getattr(DeathLink, "__doc__", "") + """

    Death Link can be toggled on/off in the client with ``/toggle_death_link``.

    Known issues:

    - Studs are not dropped when receiving a death, however, you can use the Death Link Studs Loss option to cause a
      loss of studs when receiving a death.
    - Using the Self Destruct Extra counts as dying.
    """
    display_name = "Death Link"
    rich_text_doc = True


class DeathLinkAmnesty(Range):
    """The number of deaths allowed before the next death is sent through Death Link.

    0 means that every death will be sent through Death Link,
    1 means every other death will send through Death Link, etc.

    Applies to most Chapters and other levels (every level not covered by Vehicle Death Link Amnesty).
    """
    display_name = "Normal Death Link Amnesty"
    rich_text_doc = True
    range_start = 0
    range_end = 10
    default = 0


class VehicleDeathLinkAmnesty(Range):
    """The number of deaths allowed before the next death is sent through Death Link.

    \\*Applies to top-down vehicle levels and bonus vehicle levels that are easier to die in.

    Applies to:

    - 2-1 (Bounty Hunter Pursuit)
    - 2-5 (Gunship Cavalry)
    - 4-6 (Rebel Attack)
    - 5-1 (Hoth Battle)
    - 5-3 (Falcon Flight)
    - 6-6 (Into The Death Star)
    - Mos Espa Pod Race (Original)
    - Anakin's Flight
    - Gunship Cavalry (Original)

    Does not apply to:

    - 1-4 (Mos Espa Pod Race)
    - 3-1 (Battle Over Coruscant)

    """
    display_name = "Vehicle* Death Link Amnesty"
    rich_text_doc = True
    range_start = 0
    range_end = 10
    default = 3


class DeathLinkStudLoss(ChoiceFromStringExtension):
    """Choose how many studs are lost when receiving a death from Death Link.

    The studs will not spawn around you, and will be permanently lost.

    This is a temporary option while it is not possible for the client to perform a normal death that spawns studs."""
    display_name = "Death Link Studs Loss"
    rich_text_doc = True
    option_0 = 0
    option_1000 = 1000
    option_2000 = 2000
    option_3000 = 3000
    option_4000 = 4000
    option_5000 = 5000
    option_6000 = 6000
    option_7000 = 7000
    option_8000 = 8000
    option_9000 = 9000
    option_10000 = 10000
    default = 2000


class DeathLinkStudLossScaling(Toggle):
    """When enabled, the stud loss from receiving a death from Death Link is multiplied by your maximum combined score
    multiplier."""
    display_name = "Death Link Studs Loss Scaling"
    rich_text_doc = True


class SlotDataOptionMetaData(TypedDict):
    since: tuple[int, int, int]
    default_if_absent: NotRequired[Any]


def _since(major: int, minor: int, patch: int, default_if_absent=None) -> SlotDataOptionMetaData:
    if default_if_absent is not None:
        return {"since": (major, minor, patch), "default_if_absent": default_if_absent}
    else:
        return {"since": (major, minor, patch)}


# noinspection PyTypeChecker,LongLine
@dataclass
class TCSDirectSlotDataOptions:
    """Options that are put directly into slot data."""
    # Client.
    received_item_messages: ReceivedItemMessages
    checked_location_messages: CheckedLocationMessages
    shop_fake_trap_chance: ShopTrapAsFakeProgressionChance
    auto_collect_spawned_pickups: AutoCollectSpawnedPickups
    character_max_health: CharacterMaxHealth
    vehicle_max_health: VehicleMaxHealth

    # DeathLink.
    death_link_amnesty: DeathLinkAmnesty
    vehicle_death_link_amnesty: VehicleDeathLinkAmnesty
    death_link_studs_loss: DeathLinkStudLoss

    # Logic.
    # Logic knows the bundle size, so checks its counts against that known bundle size.
    minikit_bundle_size: MinikitBundleSize
    episode_unlock_requirement: EpisodeUnlockRequirement
    chapter_unlock_requirement: ChapterUnlockRequirement
    chapter_unlock_story_characters_not_required: ChapterStoryUnlockCharactersNotRequired  # todo make this optional
    all_episodes_character_purchase_requirements: AllEpisodesCharacterPurchaseRequirements

    # Logic difficulty.
    logic_difficulty: LogicDifficulty
    most_expensive_purchase_with_no_multiplier: MostExpensivePurchaseWithNoScoreMultiplier

    # Goal logic.
    defeat_bosses_goal_amount: DefeatBossesGoalAmount
    only_unique_bosses_count: OnlyUniqueBossesCountTowardsGoal

    # Other goal info.
    minikit_goal_completion_method: MinikitGoalCompletionMethod
    kyber_brick_goal_completion_method: KyberBrickGoalCompletionMethod

    # Locations.
    goal_chapter_locations_mode: GoalChapterLocationsMode


@dataclass
class LegoStarWarsTCSOptions(TCSDirectSlotDataOptions, PerGameCommonOptions):
    start_inventory_from_pool: StartInventoryPool

    # Goals.
    minikit_goal_amount: MinikitGoalAmount
    minikit_goal_amount_percentage: MinikitGoalAmountPercentage
    goal_requires_kyber_bricks: GoalRequiresKyberBricks

    enabled_bosses_count: EnabledBossesCount
    allowed_bosses: AllowedBosses

    complete_levels_goal_amount_percentage: CompleteLevelsGoalAmountPercentage

    goal_chapter: GoalChapter

    # Enabled/Available locations.
    # Chapters.
    enabled_chapters_count: EnabledChaptersCount
    allowed_chapters: AllowedChapters
    allowed_chapter_types: AllowedChapterTypes
    starting_chapter: StartingChapter
    preferred_chapters: PreferredChapters
    prefer_entire_episodes: PreferEntireEpisodes
    # Locations.
    enable_bonus_locations: EnableBonusLocations
    enable_story_character_unlock_locations: EnableStoryCharacterUnlockLocations
    enable_all_episodes_purchases: EnableAllEpisodesCharacterPurchaseLocations
    enable_minikit_locations: EnableMinikitLocations
    enable_true_jedi_locations: EnableTrueJediLocations
    ridesanity: Ridesanity
    enable_starting_extras_locations: EnableNonPowerBrickExtraLocations

    # Logic and Difficulty.
    #   Chapters locked by Characters.
    chapter_unlock_characters_min_count: ChapterUnlockCharactersMinRequiredCount
    chapter_unlock_characters_max_count: ChapterUnlockCharactersMaxRequiredCount
    chapter_unlock_characters_count_distribution: ChapterUnlockCharactersRequiredCountDistribution
    #   Chapters locked by Vanilla Characters (Story/Purchase).
    chapters_that_can_require_purchase_characters: ChaptersThatCanRequirePurchaseCharacters
    require_purchase_characters_chance: RequirePurchaseCharactersInsteadOfStoryCharactersChance
    require_purchase_characters_custom_chances: RequirePurchaseCharactersInsteadOfStoryCharactersCustomChance
    #   Chapters locked by Random Characters.
    chapter_unlock_random_characters_extra_min_count: ChapterUnlockRandomCharactersMinExtraPoolCount
    chapter_unlock_random_characters_extra_max_count: ChapterUnlockRandomCharactersMaxExtraPoolCount
    chapter_unlock_random_characters_unique_per_chapter: ChapterUnlockRandomCharactersUniquePerChapter
    #   General difficulty:
    uncap_original_trilogy_high_jump: UncapOriginalTrilogyHighJump
    expect_2_1_torpedo_gathering: LogicExpectNonInfiniteTorpedoesPodRacer21
    easier_true_jedi: EasierTrueJedi
    scale_true_jedi_with_score_multipliers: ScaleTrueJediWithScoreMultipliers

    # Items.
    preferred_characters: PreferredCharacters
    preferred_extras: PreferredExtras
    start_with_detectors: StartWithDetectors
    filler_reserve_characters: FillerReserveCharacters
    filler_reserve_extras: FillerReserveExtras
    filler_weight_characters: FillerWeightCharacters
    filler_weight_extras: FillerWeightExtras
    filler_weight_junk: FillerWeightJunk
    junk_weights: JunkWeights

    # DeathLink.
    death_link: LegoStarWarsTCSDeathLink
    death_link_studs_loss_scaling: DeathLinkStudLossScaling

    # Client behaviour.
    progression_useful_item_color: ProgressionUsefulItemColor
    progression_item_color: ProgressionItemColor
    useful_item_color: UsefulItemColor
    filler_item_color: FillerItemColor
    trap_item_color: TrapItemColor
    player_name_color: PlayerNameColor
    location_name_color: LocationNameColor

    # Future options, not implemented yet.
    # random_starting_level_max_starting_characters: RandomStartingLevelMaxStartingCharacters

    def item_colors_to_slot_data(self) -> tuple[int, int, int, int, int, int, int]:
        return TextColorChoice.colors_to_slot_data(self)


_OPTION_TYPE_TO_ATTRIBUTE: Mapping[type[Option[Any]], str] = {
    v: k for k, v in LegoStarWarsTCSOptions.type_hints.items()
}

def get_option_name(o: type[Option[Any]]) -> str:
    return _OPTION_TYPE_TO_ATTRIBUTE[o]


OPTION_GROUPS: list[OptionGroup] = [
    OptionGroup("Chapters", [
        EnabledChaptersCount,
        AllowedChapters,
        AllowedChapterTypes,
        StartingChapter,
        PreferredChapters,
        PreferEntireEpisodes,
    ]),
    OptionGroup("Goal Requirements",[
        MinikitGoalAmount,
        DefeatBossesGoalAmount,
        CompleteLevelsGoalAmountPercentage,
        GoalRequiresKyberBricks,
        GoalChapter,
    ]),
    OptionGroup("Minikit Goal Options", [
        MinikitGoalAmountPercentage,
        MinikitGoalCompletionMethod,
    ]),
    OptionGroup("Bosses Goal Options", [
        EnabledBossesCount,
        AllowedBosses,
        OnlyUniqueBossesCountTowardsGoal,
    ], True),
    OptionGroup("Goal Chapter Options", [
        GoalChapterLocationsMode,
    ], True),
    OptionGroup("Other Goal Options", [
        KyberBrickGoalCompletionMethod,
    ], True),
    OptionGroup("Enabled Locations", [
        EnableMinikitLocations,
        EnableTrueJediLocations,
        EnableStoryCharacterUnlockLocations,
        EnableBonusLocations,
        EnableAllEpisodesCharacterPurchaseLocations,
        EnableNonPowerBrickExtraLocations,
        Ridesanity,
    ]),
    OptionGroup("Unlock Requirements", [
        EpisodeUnlockRequirement,
        ChapterUnlockRequirement,
        AllEpisodesCharacterPurchaseRequirements,
    ]),
    OptionGroup("Logic and Difficulty", [
        LogicDifficulty,
        UncapOriginalTrilogyHighJump,
        EasierTrueJedi,
        ScaleTrueJediWithScoreMultipliers,
        MostExpensivePurchaseWithNoScoreMultiplier,
        LogicExpectNonInfiniteTorpedoesPodRacer21,
        CharacterMaxHealth,
        VehicleMaxHealth,
    ]),
    OptionGroup("Chapter Unlock Requirement: Characters (any)", [
        ChapterUnlockCharactersMinRequiredCount,
        ChapterUnlockCharactersMaxRequiredCount,
        ChapterUnlockCharactersRequiredCountDistribution,
    ]),
    OptionGroup("Chapter Unlock Requirement: Vanilla Characters", [
        ChapterStoryUnlockCharactersNotRequired,
        ChaptersThatCanRequirePurchaseCharacters,
        RequirePurchaseCharactersInsteadOfStoryCharactersChance,
        RequirePurchaseCharactersInsteadOfStoryCharactersCustomChance,
    ]),
    OptionGroup("Chapter Unlock Requirement: Random Characters", [
        ChapterUnlockRandomCharactersMinExtraPoolCount,
        ChapterUnlockRandomCharactersMaxExtraPoolCount,
        ChapterUnlockRandomCharactersUniquePerChapter,
    ], True),
    OptionGroup("Items", [
        MinikitBundleSize,
        StartWithDetectors,
        PreferredCharacters,
        PreferredExtras,
        FillerReserveCharacters,
        FillerReserveExtras,
        FillerWeightCharacters,
        FillerWeightExtras,
        FillerWeightJunk,
        JunkWeights,
    ]),
    OptionGroup("Client", [
        ReceivedItemMessages,
        CheckedLocationMessages,
        AutoCollectSpawnedPickups,
        ShopTrapAsFakeProgressionChance,
        ProgressionUsefulItemColor,
        ProgressionItemColor,
        UsefulItemColor,
        FillerItemColor,
        TrapItemColor,
        PlayerNameColor,
        LocationNameColor,
    ], True),
    OptionGroup("Death Link", [
        LegoStarWarsTCSDeathLink,
        DeathLinkAmnesty,
        VehicleDeathLinkAmnesty,
        DeathLinkStudLoss,
        DeathLinkStudLossScaling,
    ], True)
]

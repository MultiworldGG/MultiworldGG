from . import LegoStarWarsWorldTestBase
from ..options import (
    get_option_name,
    EnabledChaptersCount,
    LogicDifficulty,
    StartingChapter,
    DefeatBossesGoalAmount,
    EnableBonusLocations,
    GoalRequiresKyberBricks,
    CompleteLevelsGoalAmountPercentage,
    GoalChapter,
    Ridesanity,
    MinikitGoalAmountPercentage,
    EpisodeUnlockRequirement,
    ChapterUnlockRequirement,
    RequirePurchaseCharactersInsteadOfStoryCharactersChance,
)

_BASE_OPTIONS = {
    get_option_name(StartingChapter): StartingChapter.option_random_chapter,
    get_option_name(EnabledChaptersCount): EnabledChaptersCount.range_end,
}

_PARTIAL_ENABLED_CHAPTERS = {
    get_option_name(EnabledChaptersCount): f"random-range-12-{EnabledChaptersCount.range_end}",
}


class TestBaseLogicAllChapters(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(LogicDifficulty): LogicDifficulty.option_none,
    }

class TestNormalLogicAllChapters(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(LogicDifficulty): LogicDifficulty.option_normal,
    }

class TestModerateLogicAllChapters(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(LogicDifficulty): LogicDifficulty.option_moderate,
    }

class TestHardLogicAllChapters(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(LogicDifficulty): LogicDifficulty.option_hard,
    }

class TestPurchaseCharacterChapterLocks(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(ChapterUnlockRequirement): ChapterUnlockRequirement.option_vanilla_characters,
        get_option_name(RequirePurchaseCharactersInsteadOfStoryCharactersChance):
            RequirePurchaseCharactersInsteadOfStoryCharactersChance.range_end,
    }

class TestChapterItemChapterLocks(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(ChapterUnlockRequirement): ChapterUnlockRequirement.option_chapter_item,
    }

class TestRandomCharacterChapterLocks(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(ChapterUnlockRequirement): ChapterUnlockRequirement.option_random_characters,
    }

class TestAllsanityMaxGoals(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | {
        get_option_name(DefeatBossesGoalAmount): DefeatBossesGoalAmount.range_end,
        get_option_name(EnableBonusLocations): True,
        get_option_name(GoalRequiresKyberBricks): True,
        get_option_name(CompleteLevelsGoalAmountPercentage): CompleteLevelsGoalAmountPercentage.range_end,
        get_option_name(GoalChapter): "random",
        get_option_name(Ridesanity): True,
        get_option_name(MinikitGoalAmountPercentage): MinikitGoalAmountPercentage.range_end,
        get_option_name(EpisodeUnlockRequirement): EpisodeUnlockRequirement.option_episode_item,
    }

class TestAllsanityMaxGoalsPartialChapters(LegoStarWarsWorldTestBase):
    options = _BASE_OPTIONS | _PARTIAL_ENABLED_CHAPTERS | {
        get_option_name(DefeatBossesGoalAmount): DefeatBossesGoalAmount.range_end,
        get_option_name(EnableBonusLocations): True,
        get_option_name(GoalRequiresKyberBricks): True,
        get_option_name(CompleteLevelsGoalAmountPercentage): CompleteLevelsGoalAmountPercentage.range_end,
        get_option_name(GoalChapter): "random",
        get_option_name(Ridesanity): True,
        get_option_name(MinikitGoalAmountPercentage): MinikitGoalAmountPercentage.range_end,
        get_option_name(EpisodeUnlockRequirement): EpisodeUnlockRequirement.option_episode_item,
    }

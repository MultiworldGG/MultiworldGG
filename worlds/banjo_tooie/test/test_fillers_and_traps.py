from collections import defaultdict

from BaseClasses import ItemClassification

from ..Names import itemName
from . import BanjoTooieTestBase

BASE_FILLERS = 4

# ``ADD_687_FILLERS`` with nestsanity: filler + trap + useful Jiggy / 5-note / Doubloon from create_filler rolls.
ADD_687_NESTSANITY_ROLL_TOTAL = 731
# Same shortened world without nestsanity.
ADD_687_NO_NESTSANITY_ROLL_TOTAL = 258
# Clefs + signposts, notes on, BK moves fully randomized (no BK items as filler).
NOTES_SIGNPOSTS_NO_NEST_ROLL_TOTAL = 188

ALL_90_JIGGIES_AND_900_NOTES_PROGRESSION = {
    "world_requirements": "custom",
    "custom_worlds": "1,1,1,1,1,1,1,1,90",
    "randomize_notes": "false",
}

ADD_16_FILLERS_FROM_BK_MOVES = {
    "randomize_bk_moves": 0,
}

ADD_NO_FILLERS_FROM_BK_MOVES = {
    "randomize_bk_moves": 2,
}

ADD_687_FILLERS = {
    **ADD_16_FILLERS_FROM_BK_MOVES,
    # length config (adds 44)
    "world_requirements": "custom",
    "custom_worlds": "1,1,1,1,1,1,1,1,1",
    # nests config (adds 473)
    "nestsanity": "true",

    # notes config
    # there are actually no 5 notes in pool now.
    "randomize_notes": "true",

    # doesn't do anything, but allows extra doubloons in filler pool
    "randomize_doubloons": "true",

    # (adds 93)
    "extra_trebleclefs_count": 21,
    "bass_clef_amount": 30,

    # (adds 61)
    "randomize_signposts": "true",
}

ONLY_BIG_O_PANTS_FILLER = {
    "max_traps": 0,
    "feather_nests_weight": 0,
    "egg_nests_weight": 0,
    "extra_jiggies_weight": 0,
    "extra_notes_weight": 0,
    "extra_pages_weight": 0,
    "extra_doubloons_weight": 0,
    "big_o_pants_weight": 100,
}

ZERO_FILLERS_WEIGHT = {
    **ONLY_BIG_O_PANTS_FILLER,
    "big_o_pants_weight": 0,
}


class FillersTrapTestBase(BanjoTooieTestBase):
    """Fixed RNG so filler-weighted rolls are stable across CI runs."""

    filler_test_seed = 123456789

    def setUp(self) -> None:
        if self.auto_construct:
            self.world_setup(self.filler_test_seed)

    class Pool:
        def __init__(self):
            self.trap_distribution = defaultdict(int)
            self.filler_distribution = defaultdict(int)
            self.distribution = defaultdict(int)
            self.total_distribution = defaultdict(int)

    def useful_note_bundle_count(self) -> int:
        """Bundles from ``get_notes_in_pool`` are useful, not filler, and shrink the filler/trap pool."""
        return sum(
            1 for item in self.multiworld.itempool
            if item.name == itemName.NOTE and item.classification == ItemClassification.useful
        )

    def currency_useful_item_count(self) -> int:
        """Useful Jiggies, 5-note bundles, and Doubloons (including create_filler rolls)."""
        ip = self.multiworld.itempool
        return (
            self.useful_note_bundle_count()
            + sum(1 for item in ip if item.name == itemName.DOUBLOON and item.classification == ItemClassification.useful)
            + sum(1 for item in ip if item.name == itemName.JIGGY and item.classification == ItemClassification.useful)
        )

    def pool(self) -> Pool:
        pool = self.Pool()
        for item in self.world.multiworld.itempool:
            if item.trap:
                pool.trap_distribution[item.name] += 1
                pool.distribution[item.name] += 1
            if item.filler:
                pool.filler_distribution[item.name] += 1
                pool.distribution[item.name] += 1
            pool.total_distribution[item.name] += 1

        return pool


class TestMaxTrapsZero(FillersTrapTestBase):
    options = {
        "max_traps": 0,
        "nestsanity": "false",

        **ALL_90_JIGGIES_AND_900_NOTES_PROGRESSION,
        **ADD_16_FILLERS_FROM_BK_MOVES,
        "egg_nests_weight": 0,
        "feather_nests_weight": 0,
        "extra_jiggies_weight": 0,
        "big_o_pants_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.filler_distribution.values()) == 20
        assert sum(pool.trap_distribution.values()) == 0


class TestMaxTrapsNonZero(FillersTrapTestBase):
    options = {
        "max_traps": 100,
        "nestsanity": "false",

        **ALL_90_JIGGIES_AND_900_NOTES_PROGRESSION,
        **ADD_16_FILLERS_FROM_BK_MOVES,
        "egg_nests_weight": 0,
        "feather_nests_weight": 0,
        "extra_jiggies_weight": 0,
        "big_o_pants_weight": 0,
        "squish_trap_weight": 100,
        "tip_trap_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        fillers = sum(pool.filler_distribution.values())
        traps = sum(pool.trap_distribution.values())
        assert traps > 0
        assert fillers + traps == 20


class TestMaxTrapsZeroWithNestsanity(FillersTrapTestBase):
    options = {
        "max_traps": 0,
        "nestsanity": "true",

        **ALL_90_JIGGIES_AND_900_NOTES_PROGRESSION,
        **ADD_NO_FILLERS_FROM_BK_MOVES,
        "extra_jiggies_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.filler_distribution.values()) == 315 + 135 + 23 + BASE_FILLERS
        assert sum(pool.trap_distribution.values()) == 0


class TestFillersExtraClefs(FillersTrapTestBase):
    options = {
        "max_traps": 0,

        **ALL_90_JIGGIES_AND_900_NOTES_PROGRESSION,
        **ADD_NO_FILLERS_FROM_BK_MOVES,

        "randomize_notes": "true",
        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,
        "extra_jiggies_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        clef_filler_budget = 30 + 21 * 3 + BASE_FILLERS
        assert (
            sum(pool.filler_distribution.values())
            + sum(pool.trap_distribution.values())
            + self.useful_note_bundle_count()
            == clef_filler_budget
        )
        assert sum(pool.trap_distribution.values()) == 0


class TestAllWeightsZeroAddPants(FillersTrapTestBase):
    options = {
        **ADD_687_FILLERS,
        **ZERO_FILLERS_WEIGHT
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL


class TestAllFillerWeightsZeroAddRestPants(FillersTrapTestBase):
    options = {
        **ADD_687_FILLERS,
        **ZERO_FILLERS_WEIGHT,

        "max_traps": 87,
        "trip_trap_weight": 0,
        "slip_trap_weight": 0,
        "transform_trap_weight": 0,
        "golden_eggs_weight": 0,
        "squish_trap_weight": 100,
        "tip_trap_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert pool.distribution[itemName.SQTRAP] == 87
        filler_trap_only = ADD_687_NESTSANITY_ROLL_TOTAL - self.currency_useful_item_count()
        assert pool.distribution[itemName.NONE] == filler_trap_only - 87


class TestRespectDistribution(FillersTrapTestBase):
    options = {
        "max_traps": "unlimited",

        **ADD_687_FILLERS,

        # note to future editors, don't add more than 6 non-zero weights
        "extra_jiggies_weight": 0,
        "big_o_pants_weight": 0,
        "trip_trap_weight": 0,
        "slip_trap_weight": 0,
        "transform_trap_weight": 0,
        "golden_eggs_weight": 0,

        "extra_doubloons_weight": 10,
        "egg_nests_weight": 5,  # will be doubled
        "extra_notes_weight": 50,
        "feather_nests_weight": 25,  # will be doubled
        "squish_trap_weight": 100,
        "tip_trap_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL

        assert pool.distribution[itemName.JIGGY] == 0
        assert pool.distribution[itemName.NONE] == 0
        assert pool.distribution[itemName.TTRAP] == 0
        assert pool.distribution[itemName.STRAP] == 0
        assert pool.distribution[itemName.TRTRAP] == 0
        assert pool.distribution[itemName.GNEST] == 0
        assert 6 <= pool.total_distribution[itemName.DOUBLOON] <= 70
        assert 6 <= pool.distribution[itemName.ENEST] <= 38
        assert 75 <= pool.total_distribution[itemName.NOTE] <= 141
        assert 75 <= pool.distribution[itemName.FNEST] <= 141
        assert 174 <= pool.distribution[itemName.SQTRAP] <= 258
        assert 174 <= pool.distribution[itemName.TITRAP] <= 258


class TestRespectDistribution2(FillersTrapTestBase):
    options = {
        "max_traps": "unlimited",

        **ADD_687_FILLERS,

        # note to future editors, don't add more than 6 non-zero weights
        "extra_jiggies_weight": 10,
        "big_o_pants_weight": 10,
        "trip_trap_weight": 50,
        "slip_trap_weight": 50,
        "transform_trap_weight": 100,
        "golden_eggs_weight": 100,

        "extra_doubloons_weight": 0,
        "egg_nests_weight": 0,
        "extra_notes_weight": 0,
        "feather_nests_weight": 0,
        "squish_trap_weight": 0,
        "tip_trap_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL

        assert pool.distribution[itemName.DOUBLOON] == 0
        assert pool.distribution[itemName.ENEST] == 0
        assert pool.distribution[itemName.NOTE] == 0
        assert pool.distribution[itemName.FNEST] == 0
        assert pool.distribution[itemName.SQTRAP] == 0
        assert pool.distribution[itemName.TITRAP] == 0
        assert 6 <= pool.total_distribution[itemName.JIGGY] <= 80
        assert 6 <= pool.distribution[itemName.NONE] <= 35
        assert 75 <= pool.distribution[itemName.TTRAP] <= 141
        assert 75 <= pool.distribution[itemName.STRAP] <= 141
        assert 174 <= pool.distribution[itemName.TRTRAP] <= 258
        assert 174 <= pool.distribution[itemName.GNEST] <= 258


class TestRespectMaxTraps(FillersTrapTestBase):
    options = {
        **ZERO_FILLERS_WEIGHT,
        "max_traps": 30,
        "squish_trap_weight": 100,

        **ADD_687_FILLERS,

        "egg_nests_weight": 50,
        "feather_nests_weight": 50,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.trap_distribution.values()) == 30
        filler_trap_only = ADD_687_NESTSANITY_ROLL_TOTAL - self.currency_useful_item_count()
        assert sum(pool.filler_distribution.values()) == filler_trap_only - 30

        assert 270 <= pool.filler_distribution[itemName.ENEST] <= 375
        assert 270 <= pool.filler_distribution[itemName.FNEST] <= 375


class TestJiggiesHardLimit(FillersTrapTestBase):
    options = {
        **ZERO_FILLERS_WEIGHT,
        **ADD_687_FILLERS,

        "extra_jiggies_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL
        assert pool.total_distribution[itemName.JIGGY] == 249


class TestDoubloonsHardLimit(FillersTrapTestBase):
    options = {
        **ZERO_FILLERS_WEIGHT,
        **ADD_687_FILLERS,

        "extra_doubloons_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL
        assert pool.total_distribution[itemName.DOUBLOON] == 250


class TestNotesHardLimit(FillersTrapTestBase):
    options = {
        **ZERO_FILLERS_WEIGHT,
        **ADD_687_FILLERS,

        "extra_notes_weight": 100,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL
        assert pool.total_distribution[itemName.NOTE] == 250


class TestDefaultFillersWithNestsanityPlenty(FillersTrapTestBase):
    options = {
        **ADD_687_FILLERS,
        "nestsanity": "true",
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NESTSANITY_ROLL_TOTAL
        # adding reasonable expectations here

        useful_notes = sum(1 for item in self.world.multiworld.itempool
                             if item.name == itemName.NOTE and item.classification == ItemClassification.useful)
        useful_jiggies = sum(1 for item in self.world.multiworld.itempool
                             if item.name == itemName.JIGGY and item.classification == ItemClassification.useful)
        assert 0 <= useful_notes <= 120
        assert 20 <= useful_jiggies <= 135


class TestDefaultFillersWithoutNestsanityPlenty(FillersTrapTestBase):
    options = {
        **ADD_687_FILLERS,
        "nestsanity": "false",
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == ADD_687_NO_NESTSANITY_ROLL_TOTAL
        # adding reasonable expectations here
        useful_notes = sum(1 for item in self.world.multiworld.itempool
                             if item.name == itemName.NOTE and item.classification == ItemClassification.useful)
        useful_jiggies = sum(1 for item in self.world.multiworld.itempool
                             if item.name == itemName.JIGGY and item.classification == ItemClassification.useful)
        assert 0 <= useful_notes <= 120
        assert 20 <= useful_jiggies <= 100


class TestDefaultFillersWithoutNestsanityReasonable(FillersTrapTestBase):
    options = {
        "randomize_notes": "true",

        "extra_trebleclefs_count": 21,
        "bass_clef_amount": 30,

        "randomize_signposts": "true",
        "nestsanity": "false",
        # Matches ``ADD_NO_FILLERS_FROM_BK_MOVES``: 188 filler-or-useful currency rolls, not 204 with BK-as-filler.
        "randomize_bk_moves": 2,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert sum(pool.distribution.values()) + self.currency_useful_item_count() == NOTES_SIGNPOSTS_NO_NEST_ROLL_TOTAL
        # adding reasonable expectations here
        useful_notes = sum(1 for item in self.world.multiworld.itempool
                             if item.name == itemName.NOTE and item.classification == ItemClassification.useful)
        useful_jiggies = sum(1 for item in self.world.multiworld.itempool
                             if item.name == itemName.JIGGY and item.classification == ItemClassification.useful)
        assert 0 <= useful_notes <= 120
        assert 15 <= useful_jiggies <= 80


class TestNoReplaceExtraNotesAndJiggies(FillersTrapTestBase):
    options = {
        **ADD_16_FILLERS_FROM_BK_MOVES,

        # exactly 50 jiggies are progressive
        "jingaling_jiggy": "false",
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,50",

        # This also adds 9 filler
        "extra_trebleclefs_count": 2,
        "bass_clef_amount": 3,
        "randomize_notes": "true",

        "replace_extra_jiggies": "false",
        "replace_extra_notes": "false",
        "egg_nests_weight": 0,
        "feather_nests_weight": 0,
        "extra_jiggies_weight": 0,
        "big_o_pants_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert pool.total_distribution[itemName.BASS] == 3
        assert pool.total_distribution[itemName.TREBLE] == 9 + 2

        assert pool.total_distribution[itemName.NOTE] * 5 \
               + pool.total_distribution[itemName.BASS] * 10 \
               + pool.total_distribution[itemName.TREBLE] * 20 \
               == 900

        assert pool.total_distribution[itemName.JIGGY] == 90

        assert sum(pool.distribution.values()) == 29

        assert pool.filler_distribution[itemName.JIGGY] == 0
        assert pool.filler_distribution[itemName.NOTE] == 0
        note_bundles = [item for item in self.world.multiworld.itempool if item.name == itemName.NOTE]
        assert not any(item.filler for item in note_bundles)
        assert sum(1 for item in note_bundles if item.classification == ItemClassification.useful) == len(note_bundles) - sum(
            1 for item in note_bundles if item.advancement)


class TestNoReplaceExtraJiggiesMinimalRespectCount(FillersTrapTestBase):
    options = {
        **ADD_16_FILLERS_FROM_BK_MOVES,
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,1",

        "randomize_jinjos": "false",

        "replace_extra_jiggies": "false",
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert pool.total_distribution[itemName.JIGGY] == 90 - 9 - 1  # remove jinjos' and jingaling


class TestNoReplaceExtraJiggiesMaximalRespectCount(FillersTrapTestBase):
    options = {
        **ADD_16_FILLERS_FROM_BK_MOVES,
        "world_requirements": "custom",
        "custom_worlds": "1,1,1,1,1,1,1,1,90",

        "randomize_jinjos": "false",

        "replace_extra_jiggies": "false",
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert pool.total_distribution[itemName.JIGGY] == 90 - 9 - 1  # remove jinjos' and jingaling


class TestNoReplaceExtraNotesRespectCount(FillersTrapTestBase):
    options = {
        **ADD_16_FILLERS_FROM_BK_MOVES,

        # This also adds 9 filler
        "extra_trebleclefs_count": 15,
        "bass_clef_amount": 20,
        "randomize_notes": "true",

        "replace_extra_notes": "false",
        "egg_nests_weight": 0,
        "feather_nests_weight": 0,
        "extra_jiggies_weight": 0,
        "big_o_pants_weight": 0,
    }

    def test_fillers_and_traps_pool(self) -> None:
        pool = self.pool()

        assert pool.total_distribution[itemName.BASS] == 20
        assert pool.total_distribution[itemName.TREBLE] == 9 + 15

        assert pool.total_distribution[itemName.NOTE] * 5 \
               + pool.total_distribution[itemName.BASS] * 10 \
               + pool.total_distribution[itemName.TREBLE] * 20 \
               == 900

        assert sum(pool.distribution.values()) == 102

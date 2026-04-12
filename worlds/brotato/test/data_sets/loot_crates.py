"""Define test data for various Brotato unit tests.

Test data consists of a set of options to create the test World with, and various expected results.

Test classes can create subtests which run on each data set to check that generation works for different option
combinations.

Currently, the test data sets are focused on testing the crate drop region creation and access rules, but there's no
reason it couldn't be expanded to handle more in the future.
"""

from dataclasses import asdict, dataclass
from typing import Any

from ...constants import (
    BASE_GAME_CHARACTERS,
    MAX_LEGENDARY_CRATE_DROP_GROUPS,
    MAX_LEGENDARY_CRATE_DROPS,
    MAX_NORMAL_CRATE_DROP_GROUPS,
    MAX_NORMAL_CRATE_DROPS,
)
from ...loot_crates import BrotatoLootCrateGroup
from .base import BrotatoTestDataSet


@dataclass(frozen=True)
class BrotatoLootCrateTestOptions:
    """Subset of the full options that we want to control for the test, with defaults.

    This avoids needing to specify all the options for the dataclass, and makes using it in the tests slightly more
    concise.
    """

    num_common_crate_drops: int
    num_common_crate_drop_groups: int
    num_legendary_crate_drops: int
    num_legendary_crate_drop_groups: int
    num_victories: int = 30

    @property
    def options_dict(self) -> dict[str, Any]:
        options = asdict(self)
        # Set the number of characters to the number of wins required so the option is always what we expect.
        options["num_characters"] = self.num_victories
        return options


@dataclass(frozen=True)
class BrotatoLootCrateTestExpectedResults:
    # An int value means all regions have the same number of crates.
    # A tuple of ints means region "Crate Group {i}" has number of crates in index [i]
    num_common_crate_regions: int
    common_crates_per_region: int | tuple[int, ...]
    num_legendary_crate_regions: int
    legendary_crates_per_region: int | tuple[int, ...]
    wins_required_per_common_region: tuple[int, ...]
    wins_required_per_legendary_region: tuple[int, ...]

    def __post_init__(self):
        """Validate the expected results to make sure the fields are consistent.

        Currently, this just means checking that the expected number of regions matches the number of entries in the
        crates per region fields.
        """

        if isinstance(self.common_crates_per_region, tuple):
            num_common_crate_regions = len(self.common_crates_per_region)
            if num_common_crate_regions != self.num_common_crate_regions:
                raise ValueError(
                    f"common_crates_per_region has {num_common_crate_regions} entries, expected "
                    f"{self.num_common_crate_regions}."
                )

        if len(self.wins_required_per_common_region) != self.num_common_crate_regions:
            num_win_entries = len(self.wins_required_per_common_region)
            raise ValueError(
                f"wins_required_per_common_region has {num_win_entries} entries, expected "
                f"{self.num_common_crate_regions}."
            )

        if isinstance(self.legendary_crates_per_region, tuple):
            num_legendary_crate_regions = len(self.legendary_crates_per_region)
            if num_legendary_crate_regions != self.num_legendary_crate_regions:
                raise ValueError(
                    f"legendary_crates_per_region has {num_legendary_crate_regions} entries, expected "
                    f"{self.num_legendary_crate_regions}."
                )

        if len(self.wins_required_per_legendary_region) != self.num_legendary_crate_regions:
            num_win_entries = len(self.wins_required_per_legendary_region)
            raise ValueError(
                f"wins_required_per_legendary_region has {num_win_entries} entries, expected "
                f"{self.num_legendary_crate_regions}."
            )


@dataclass(frozen=True)
class BrotatoLootCrateTestDataSet(BrotatoTestDataSet):
    options: BrotatoLootCrateTestOptions
    expected_common_groups: list[BrotatoLootCrateGroup]
    expected_legendary_groups: list[BrotatoLootCrateGroup]
    description: str | None = None

    @property
    def test_name(self) -> str:
        options_str = ", ".join(
            [
                f"CD={self.options.num_common_crate_drops}",
                f"CG={self.options.num_common_crate_drop_groups}",
                f"LD={self.options.num_legendary_crate_drops}",
                f"LG={self.options.num_legendary_crate_drop_groups}",
                f"NV={self.options.num_victories}",
            ]
        )
        if self.description:
            name = f"{options_str} ({self.description})"
        else:
            name = options_str

        return name

    @property
    def options_dict(self) -> dict[str, Any]:
        return self.options.options_dict


LOOT_CRATE_GROUP_DATA_SETS: list[BrotatoLootCrateTestDataSet] = [
    BrotatoLootCrateTestDataSet(
        description="Easily divisible, common and legendary same (25 crates)",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=25,
            num_common_crate_drop_groups=5,
            num_legendary_crate_drops=25,
            num_legendary_crate_drop_groups=5,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 6),
            BrotatoLootCrateGroup(3, 5, 12),
            BrotatoLootCrateGroup(4, 5, 18),
            BrotatoLootCrateGroup(5, 5, 24),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 6),
            BrotatoLootCrateGroup(3, 5, 12),
            BrotatoLootCrateGroup(4, 5, 18),
            BrotatoLootCrateGroup(5, 5, 24),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Easily divisible, common and legendary same (30 crates)",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=30,
            num_common_crate_drop_groups=6,
            num_legendary_crate_drops=30,
            num_legendary_crate_drop_groups=6,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 5),
            BrotatoLootCrateGroup(3, 5, 10),
            BrotatoLootCrateGroup(4, 5, 15),
            BrotatoLootCrateGroup(5, 5, 20),
            BrotatoLootCrateGroup(6, 5, 25),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 5),
            BrotatoLootCrateGroup(3, 5, 10),
            BrotatoLootCrateGroup(4, 5, 15),
            BrotatoLootCrateGroup(5, 5, 20),
            BrotatoLootCrateGroup(6, 5, 25),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Easily divisible, common and legendary are different",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=20,
            num_common_crate_drop_groups=2,
            num_legendary_crate_drops=30,
            num_legendary_crate_drop_groups=6,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 10, 0),
            BrotatoLootCrateGroup(2, 10, 15),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 5),
            BrotatoLootCrateGroup(3, 5, 10),
            BrotatoLootCrateGroup(4, 5, 15),
            BrotatoLootCrateGroup(5, 5, 20),
            BrotatoLootCrateGroup(6, 5, 25),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Unequal groups",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=16,
            num_common_crate_drop_groups=3,
            num_legendary_crate_drops=16,
            num_legendary_crate_drop_groups=3,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 6, 0),
            BrotatoLootCrateGroup(2, 5, 10),
            BrotatoLootCrateGroup(3, 5, 20),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 6, 0),
            BrotatoLootCrateGroup(2, 5, 10),
            BrotatoLootCrateGroup(3, 5, 20),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Unequal groups, common and legendary are different",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=35,
            num_common_crate_drop_groups=15,
            num_legendary_crate_drops=25,
            num_legendary_crate_drop_groups=5,
        ),
        expected_common_groups=[
            # Five "3's" and ten "2's", because the drops don't evenly divide into the groups
            BrotatoLootCrateGroup(1, 3, 0),
            BrotatoLootCrateGroup(2, 3, 2),
            BrotatoLootCrateGroup(3, 3, 4),
            BrotatoLootCrateGroup(4, 3, 6),
            BrotatoLootCrateGroup(5, 3, 8),
            BrotatoLootCrateGroup(6, 2, 10),
            BrotatoLootCrateGroup(7, 2, 12),
            BrotatoLootCrateGroup(8, 2, 14),
            BrotatoLootCrateGroup(9, 2, 16),
            BrotatoLootCrateGroup(10, 2, 18),
            BrotatoLootCrateGroup(11, 2, 20),
            BrotatoLootCrateGroup(12, 2, 22),
            BrotatoLootCrateGroup(13, 2, 24),
            BrotatoLootCrateGroup(14, 2, 26),
            BrotatoLootCrateGroup(15, 2, 28),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 6),
            BrotatoLootCrateGroup(3, 5, 12),
            BrotatoLootCrateGroup(4, 5, 18),
            BrotatoLootCrateGroup(5, 5, 24),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Max possible groups and crates, more groups than req. wins, no DLC",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=MAX_NORMAL_CRATE_DROPS,
            num_common_crate_drop_groups=MAX_NORMAL_CRATE_DROP_GROUPS,
            num_legendary_crate_drops=MAX_LEGENDARY_CRATE_DROPS,
            num_legendary_crate_drop_groups=MAX_LEGENDARY_CRATE_DROP_GROUPS,
        ),
        expected_common_groups=[
            # The number of groups will be set to 30 (default # of wins) when generated.
            # Every win will unlock a new crate drop group.
            BrotatoLootCrateGroup(1, 2, 0),
            BrotatoLootCrateGroup(2, 2, 1),
            BrotatoLootCrateGroup(3, 2, 2),
            BrotatoLootCrateGroup(4, 2, 3),
            BrotatoLootCrateGroup(5, 2, 4),
            BrotatoLootCrateGroup(6, 2, 5),
            BrotatoLootCrateGroup(7, 2, 6),
            BrotatoLootCrateGroup(8, 2, 7),
            BrotatoLootCrateGroup(9, 2, 8),
            BrotatoLootCrateGroup(10, 2, 9),
            BrotatoLootCrateGroup(11, 2, 10),
            BrotatoLootCrateGroup(12, 2, 11),
            BrotatoLootCrateGroup(13, 2, 12),
            BrotatoLootCrateGroup(14, 2, 13),
            BrotatoLootCrateGroup(15, 2, 14),
            BrotatoLootCrateGroup(16, 2, 15),
            BrotatoLootCrateGroup(17, 2, 16),
            BrotatoLootCrateGroup(18, 2, 17),
            BrotatoLootCrateGroup(19, 2, 18),
            BrotatoLootCrateGroup(20, 2, 19),
            BrotatoLootCrateGroup(21, 1, 20),
            BrotatoLootCrateGroup(22, 1, 21),
            BrotatoLootCrateGroup(23, 1, 22),
            BrotatoLootCrateGroup(24, 1, 23),
            BrotatoLootCrateGroup(25, 1, 24),
            BrotatoLootCrateGroup(26, 1, 25),
            BrotatoLootCrateGroup(27, 1, 26),
            BrotatoLootCrateGroup(28, 1, 27),
            BrotatoLootCrateGroup(29, 1, 28),
            BrotatoLootCrateGroup(30, 1, 29),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 2, 0),
            BrotatoLootCrateGroup(2, 2, 1),
            BrotatoLootCrateGroup(3, 2, 2),
            BrotatoLootCrateGroup(4, 2, 3),
            BrotatoLootCrateGroup(5, 2, 4),
            BrotatoLootCrateGroup(6, 2, 5),
            BrotatoLootCrateGroup(7, 2, 6),
            BrotatoLootCrateGroup(8, 2, 7),
            BrotatoLootCrateGroup(9, 2, 8),
            BrotatoLootCrateGroup(10, 2, 9),
            BrotatoLootCrateGroup(11, 2, 10),
            BrotatoLootCrateGroup(12, 2, 11),
            BrotatoLootCrateGroup(13, 2, 12),
            BrotatoLootCrateGroup(14, 2, 13),
            BrotatoLootCrateGroup(15, 2, 14),
            BrotatoLootCrateGroup(16, 2, 15),
            BrotatoLootCrateGroup(17, 2, 16),
            BrotatoLootCrateGroup(18, 2, 17),
            BrotatoLootCrateGroup(19, 2, 18),
            BrotatoLootCrateGroup(20, 2, 19),
            BrotatoLootCrateGroup(21, 1, 20),
            BrotatoLootCrateGroup(22, 1, 21),
            BrotatoLootCrateGroup(23, 1, 22),
            BrotatoLootCrateGroup(24, 1, 23),
            BrotatoLootCrateGroup(25, 1, 24),
            BrotatoLootCrateGroup(26, 1, 25),
            BrotatoLootCrateGroup(27, 1, 26),
            BrotatoLootCrateGroup(28, 1, 27),
            BrotatoLootCrateGroup(29, 1, 28),
            BrotatoLootCrateGroup(30, 1, 29),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Max wins, one crate per character, one group per character, no DLC",
        options=BrotatoLootCrateTestOptions(
            num_victories=BASE_GAME_CHARACTERS.num_characters,
            num_common_crate_drops=BASE_GAME_CHARACTERS.num_characters,
            # Assign one group per character, so each win makes more crates accessible.
            num_common_crate_drop_groups=BASE_GAME_CHARACTERS.num_characters,
            num_legendary_crate_drops=BASE_GAME_CHARACTERS.num_characters,
            num_legendary_crate_drop_groups=BASE_GAME_CHARACTERS.num_characters,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 1, 0),
            BrotatoLootCrateGroup(2, 1, 1),
            BrotatoLootCrateGroup(3, 1, 2),
            BrotatoLootCrateGroup(4, 1, 3),
            BrotatoLootCrateGroup(5, 1, 4),
            BrotatoLootCrateGroup(6, 1, 5),
            BrotatoLootCrateGroup(7, 1, 6),
            BrotatoLootCrateGroup(8, 1, 7),
            BrotatoLootCrateGroup(9, 1, 8),
            BrotatoLootCrateGroup(10, 1, 9),
            BrotatoLootCrateGroup(11, 1, 10),
            BrotatoLootCrateGroup(12, 1, 11),
            BrotatoLootCrateGroup(13, 1, 12),
            BrotatoLootCrateGroup(14, 1, 13),
            BrotatoLootCrateGroup(15, 1, 14),
            BrotatoLootCrateGroup(16, 1, 15),
            BrotatoLootCrateGroup(17, 1, 16),
            BrotatoLootCrateGroup(18, 1, 17),
            BrotatoLootCrateGroup(19, 1, 18),
            BrotatoLootCrateGroup(20, 1, 19),
            BrotatoLootCrateGroup(21, 1, 20),
            BrotatoLootCrateGroup(22, 1, 21),
            BrotatoLootCrateGroup(23, 1, 22),
            BrotatoLootCrateGroup(24, 1, 23),
            BrotatoLootCrateGroup(25, 1, 24),
            BrotatoLootCrateGroup(26, 1, 25),
            BrotatoLootCrateGroup(27, 1, 26),
            BrotatoLootCrateGroup(28, 1, 27),
            BrotatoLootCrateGroup(29, 1, 28),
            BrotatoLootCrateGroup(30, 1, 29),
            BrotatoLootCrateGroup(31, 1, 30),
            BrotatoLootCrateGroup(32, 1, 31),
            BrotatoLootCrateGroup(33, 1, 32),
            BrotatoLootCrateGroup(34, 1, 33),
            BrotatoLootCrateGroup(35, 1, 34),
            BrotatoLootCrateGroup(36, 1, 35),
            BrotatoLootCrateGroup(37, 1, 36),
            BrotatoLootCrateGroup(38, 1, 37),
            BrotatoLootCrateGroup(39, 1, 38),
            BrotatoLootCrateGroup(40, 1, 39),
            BrotatoLootCrateGroup(41, 1, 40),
            BrotatoLootCrateGroup(42, 1, 41),
            BrotatoLootCrateGroup(43, 1, 42),
            BrotatoLootCrateGroup(44, 1, 43),
            BrotatoLootCrateGroup(45, 1, 44),
            BrotatoLootCrateGroup(46, 1, 45),
            BrotatoLootCrateGroup(47, 1, 46),
            BrotatoLootCrateGroup(48, 1, 47),
            BrotatoLootCrateGroup(49, 1, 48),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 1, 0),
            BrotatoLootCrateGroup(2, 1, 1),
            BrotatoLootCrateGroup(3, 1, 2),
            BrotatoLootCrateGroup(4, 1, 3),
            BrotatoLootCrateGroup(5, 1, 4),
            BrotatoLootCrateGroup(6, 1, 5),
            BrotatoLootCrateGroup(7, 1, 6),
            BrotatoLootCrateGroup(8, 1, 7),
            BrotatoLootCrateGroup(9, 1, 8),
            BrotatoLootCrateGroup(10, 1, 9),
            BrotatoLootCrateGroup(11, 1, 10),
            BrotatoLootCrateGroup(12, 1, 11),
            BrotatoLootCrateGroup(13, 1, 12),
            BrotatoLootCrateGroup(14, 1, 13),
            BrotatoLootCrateGroup(15, 1, 14),
            BrotatoLootCrateGroup(16, 1, 15),
            BrotatoLootCrateGroup(17, 1, 16),
            BrotatoLootCrateGroup(18, 1, 17),
            BrotatoLootCrateGroup(19, 1, 18),
            BrotatoLootCrateGroup(20, 1, 19),
            BrotatoLootCrateGroup(21, 1, 20),
            BrotatoLootCrateGroup(22, 1, 21),
            BrotatoLootCrateGroup(23, 1, 22),
            BrotatoLootCrateGroup(24, 1, 23),
            BrotatoLootCrateGroup(25, 1, 24),
            BrotatoLootCrateGroup(26, 1, 25),
            BrotatoLootCrateGroup(27, 1, 26),
            BrotatoLootCrateGroup(28, 1, 27),
            BrotatoLootCrateGroup(29, 1, 28),
            BrotatoLootCrateGroup(30, 1, 29),
            BrotatoLootCrateGroup(31, 1, 30),
            BrotatoLootCrateGroup(32, 1, 31),
            BrotatoLootCrateGroup(33, 1, 32),
            BrotatoLootCrateGroup(34, 1, 33),
            BrotatoLootCrateGroup(35, 1, 34),
            BrotatoLootCrateGroup(36, 1, 35),
            BrotatoLootCrateGroup(37, 1, 36),
            BrotatoLootCrateGroup(38, 1, 37),
            BrotatoLootCrateGroup(39, 1, 38),
            BrotatoLootCrateGroup(40, 1, 39),
            BrotatoLootCrateGroup(41, 1, 40),
            BrotatoLootCrateGroup(42, 1, 41),
            BrotatoLootCrateGroup(43, 1, 42),
            BrotatoLootCrateGroup(44, 1, 43),
            BrotatoLootCrateGroup(45, 1, 44),
            BrotatoLootCrateGroup(46, 1, 45),
            BrotatoLootCrateGroup(47, 1, 46),
            BrotatoLootCrateGroup(48, 1, 47),
            BrotatoLootCrateGroup(49, 1, 48),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Max number of crates, one group",
        options=BrotatoLootCrateTestOptions(
            num_victories=BASE_GAME_CHARACTERS.num_characters,
            num_common_crate_drops=MAX_NORMAL_CRATE_DROPS,
            num_common_crate_drop_groups=1,
            num_legendary_crate_drops=MAX_LEGENDARY_CRATE_DROPS,
            num_legendary_crate_drop_groups=1,
        ),
        # All the crates should be in the first group which is unlocked by default.
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 50, 0),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 50, 0),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="1 crate and 1 group",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=1,
            num_common_crate_drop_groups=1,
            num_legendary_crate_drops=1,
            num_legendary_crate_drop_groups=1,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 1, 0),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 1, 0),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="2 crates, 1 group",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=2,
            num_common_crate_drop_groups=1,
            num_legendary_crate_drops=2,
            num_legendary_crate_drop_groups=1,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 2, 0),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 2, 0),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Max number of crates, 1 common group, 2 legendary groups",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=MAX_LEGENDARY_CRATE_DROPS,
            num_common_crate_drop_groups=1,
            num_legendary_crate_drops=MAX_LEGENDARY_CRATE_DROPS,
            num_legendary_crate_drop_groups=2,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 50, 0),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 25, 0),
            BrotatoLootCrateGroup(2, 25, 15),
        ],
    ),
]

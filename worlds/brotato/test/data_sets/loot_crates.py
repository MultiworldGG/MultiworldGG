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
    MAX_LEGENDARY_CRATE_DROP_GROUPS,
    MAX_LEGENDARY_CRATE_DROPS,
    MAX_NORMAL_CRATE_DROP_GROUPS,
    MAX_NORMAL_CRATE_DROPS,
    MAX_REQUIRED_RUN_WINS,
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
    num_victories: int = 20

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
        description="Easily divisible, common and legendary same (10 crates)",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=10,
            num_common_crate_drop_groups=5,
            num_legendary_crate_drops=10,
            num_legendary_crate_drop_groups=5,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 2, 0),
            BrotatoLootCrateGroup(2, 2, 4),
            BrotatoLootCrateGroup(3, 2, 8),
            BrotatoLootCrateGroup(4, 2, 12),
            BrotatoLootCrateGroup(5, 2, 16),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 2, 0),
            BrotatoLootCrateGroup(2, 2, 4),
            BrotatoLootCrateGroup(3, 2, 8),
            BrotatoLootCrateGroup(4, 2, 12),
            BrotatoLootCrateGroup(5, 2, 16),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Easily divisible, common and legendary are different",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=20,
            num_common_crate_drop_groups=2,
            num_legendary_crate_drops=5,
            num_legendary_crate_drop_groups=5,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 10, 0),
            BrotatoLootCrateGroup(2, 10, 10),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 1, 0),
            BrotatoLootCrateGroup(2, 1, 4),
            BrotatoLootCrateGroup(3, 1, 8),
            BrotatoLootCrateGroup(4, 1, 12),
            BrotatoLootCrateGroup(5, 1, 16),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Unequal groups",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=16,
            num_common_crate_drop_groups=3,
            num_legendary_crate_drops=7,
            num_legendary_crate_drop_groups=3,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 6, 0),
            BrotatoLootCrateGroup(2, 5, 6),
            BrotatoLootCrateGroup(3, 5, 13),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 3, 0),
            BrotatoLootCrateGroup(2, 2, 6),
            BrotatoLootCrateGroup(3, 2, 13),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Unequal groups, common and legendary are different",
        options=BrotatoLootCrateTestOptions(
            num_common_crate_drops=20,
            num_common_crate_drop_groups=15,
            num_legendary_crate_drops=10,
            num_legendary_crate_drop_groups=8,
            num_victories=25,
        ),
        expected_common_groups=[
            # Five "3's" and ten "2's", because the drops don't evenly divide into the groups
            BrotatoLootCrateGroup(1, 2, 0),
            BrotatoLootCrateGroup(2, 2, 1),
            BrotatoLootCrateGroup(3, 2, 3),
            BrotatoLootCrateGroup(4, 2, 5),
            BrotatoLootCrateGroup(5, 2, 6),
            BrotatoLootCrateGroup(6, 1, 8),
            BrotatoLootCrateGroup(7, 1, 10),
            BrotatoLootCrateGroup(8, 1, 11),
            BrotatoLootCrateGroup(9, 1, 13),
            BrotatoLootCrateGroup(10, 1, 14),
            BrotatoLootCrateGroup(11, 1, 16),
            BrotatoLootCrateGroup(12, 1, 18),
            BrotatoLootCrateGroup(13, 1, 20),
            BrotatoLootCrateGroup(14, 1, 21),
            BrotatoLootCrateGroup(15, 1, 23),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 2, 0),
            BrotatoLootCrateGroup(2, 2, 3),
            BrotatoLootCrateGroup(3, 1, 6),
            BrotatoLootCrateGroup(4, 1, 9),
            BrotatoLootCrateGroup(5, 1, 12),
            BrotatoLootCrateGroup(6, 1, 15),
            BrotatoLootCrateGroup(7, 1, 18),
            BrotatoLootCrateGroup(8, 1, 21),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Max crates, groups, and wins",
        options=BrotatoLootCrateTestOptions(
            num_victories=MAX_REQUIRED_RUN_WINS,  # 25
            num_common_crate_drops=MAX_NORMAL_CRATE_DROPS,  # 25
            num_common_crate_drop_groups=MAX_NORMAL_CRATE_DROP_GROUPS,  # 25
            num_legendary_crate_drops=MAX_LEGENDARY_CRATE_DROP_GROUPS,  # 10
            num_legendary_crate_drop_groups=MAX_LEGENDARY_CRATE_DROP_GROUPS,  # 10
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
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 1, 0),
            BrotatoLootCrateGroup(2, 1, 2),
            BrotatoLootCrateGroup(3, 1, 5),
            BrotatoLootCrateGroup(4, 1, 7),
            BrotatoLootCrateGroup(5, 1, 10),
            BrotatoLootCrateGroup(6, 1, 12),
            BrotatoLootCrateGroup(7, 1, 15),
            BrotatoLootCrateGroup(8, 1, 17),
            BrotatoLootCrateGroup(9, 1, 20),
            BrotatoLootCrateGroup(10, 1, 22),
        ],
    ),
    BrotatoLootCrateTestDataSet(
        description="Max number of crates, one group",
        options=BrotatoLootCrateTestOptions(
            num_victories=MAX_REQUIRED_RUN_WINS,
            num_common_crate_drops=MAX_NORMAL_CRATE_DROPS,
            num_common_crate_drop_groups=1,
            num_legendary_crate_drops=MAX_LEGENDARY_CRATE_DROPS,
            num_legendary_crate_drop_groups=1,
        ),
        # All the crates should be in the first group which is unlocked by default.
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 25, 0),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 10, 0),
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
            num_common_crate_drops=MAX_NORMAL_CRATE_DROPS,
            num_common_crate_drop_groups=1,
            num_legendary_crate_drops=MAX_LEGENDARY_CRATE_DROPS,
            num_legendary_crate_drop_groups=2,
        ),
        expected_common_groups=[
            BrotatoLootCrateGroup(1, 25, 0),
        ],
        expected_legendary_groups=[
            BrotatoLootCrateGroup(1, 5, 0),
            BrotatoLootCrateGroup(2, 5, 10),
        ],
    ),
]

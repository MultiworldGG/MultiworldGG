from typing import Any, ClassVar

from BaseClasses import MultiWorld, Region
from test.bases import WorldTestBase

from .. import BrotatoWorld
from ..constants import (
    CHARACTER_REGION_TEMPLATE,
    CRATE_DROP_GROUP_REGION_TEMPLATE,
    CRATE_DROP_LOCATION_TEMPLATE,
    LEGENDARY_CRATE_DROP_GROUP_REGION_TEMPLATE,
    LEGENDARY_CRATE_DROP_LOCATION_TEMPLATE,
    RUN_COMPLETE_LOCATION_TEMPLATE,
    WAVE_COMPLETE_LOCATION_TEMPLATE,
)
from ..items import ItemName
from ..loot_crates import BrotatoLootCrateGroup
from ..regions import create_character_region, create_loot_crate_group_region, create_regions
from . import BrotatoTestBase


class TestBrotatoRegions(WorldTestBase):
    # Create the bare minimum test setup for our tests to work, for speed.
    def setUp(self):
        self.multiworld = MultiWorld(1)
        self.multiworld.game[1] = "Brotato"
        self.multiworld.player_name = {self.player: "Tester"}
        self.multiworld.worlds[1] = BrotatoWorld(self.multiworld, 1)

    def _create_region(self, name: str) -> Region:
        """Region factory to pass to the region creation functions."""
        return Region(name, self.multiworld.player_ids[0], self.multiworld)


class TestBrotatoCharacterRegions(TestBrotatoRegions):
    def test_create_character_region_has_correct_locations(self):
        waves_with_checks = [5, 10, 15, 20]
        # Create a region for a characters we deliberately did not include
        expected_location_names = [
            RUN_COMPLETE_LOCATION_TEMPLATE.format(char="Crazy"),
            WAVE_COMPLETE_LOCATION_TEMPLATE.format(char="Crazy", wave=5),
            WAVE_COMPLETE_LOCATION_TEMPLATE.format(char="Crazy", wave=10),
            WAVE_COMPLETE_LOCATION_TEMPLATE.format(char="Crazy", wave=15),
            WAVE_COMPLETE_LOCATION_TEMPLATE.format(char="Crazy", wave=20),
        ]
        region = create_character_region(self._create_region, "Crazy", waves_with_checks)
        region_location_names = [loc.name for loc in region.locations]

        self.assertListEqual(region_location_names, expected_location_names)

    def test_create_character_region_invalid_character_fails(self):
        with self.assertRaises(KeyError):
            create_character_region(self._create_region, "Ironclad", [3, 6, 9, 12, 15, 18])

    def test_create_character_region_invalid_waves_with_checks_fails(self):
        """Check that we don't create a region with invalid wave complete locations.

        Mostly a sanity check on creating the waves with checks, but this has historically been an error-prone part of
        the code, so it's worth a bit of redundant testing.
        """
        invalid_waves_with_checks_value: list[Any] = [[1, 2, 3, -1], [0, 5, 10, 15, 20]]
        for invalid_value in invalid_waves_with_checks_value:
            with self.subTest(
                f"Check that create_character_region fails when waves_with_checks={invalid_value}",
                invalid_value=invalid_value,
            ):
                with self.assertRaises(ValueError):
                    create_character_region(self._create_region, "Brawler", invalid_value)


class TestBrotatoLootCrateRegions(TestBrotatoRegions):
    def test_create_loot_crate_group_region_has_correct_locations(self):
        group = BrotatoLootCrateGroup(1, 5, 0)
        expected_locations = [
            CRATE_DROP_LOCATION_TEMPLATE.format(num=1),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=2),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=3),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=4),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=5),
        ]
        region = create_loot_crate_group_region(self._create_region, group, "common")
        location_names = [location.name for location in region.locations]
        self.assertListEqual(location_names, expected_locations)

    def test_create_loot_crate_group_region_custom_start_has_correct_locations(self):
        previous_crates = 10
        group = BrotatoLootCrateGroup(1, 7, 5)
        expected_locations = [
            CRATE_DROP_LOCATION_TEMPLATE.format(num=11),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=12),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=13),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=14),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=15),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=16),
            CRATE_DROP_LOCATION_TEMPLATE.format(num=17),
        ]
        region = create_loot_crate_group_region(
            self._create_region, group, "common", crate_count_start=previous_crates + 1
        )
        location_names = [location.name for location in region.locations]
        self.assertListEqual(location_names, expected_locations)


class TestBrotatoCreateRegions(TestBrotatoRegions):
    parent_region: Region
    regions: dict[str, Region]

    characters: list[str] = ("Brawler", "Crazy", "Mage", "Demon")
    common_loot_crate_groups: ClassVar[list[BrotatoLootCrateGroup]] = [
        BrotatoLootCrateGroup(1, 10, 0),
        BrotatoLootCrateGroup(2, 10, 5),
        BrotatoLootCrateGroup(3, 10, 10),
        BrotatoLootCrateGroup(4, 5, 15),
    ]
    legendary_loot_crate_groups: list[BrotatoLootCrateGroup] = (BrotatoLootCrateGroup(1, 5, 0),)
    waves_with_checks: list[int] = (5, 10, 15, 20)

    def setUp(self) -> None:
        super().setUp()
        regions = create_regions(
            self._create_region,
            self.characters,
            self.waves_with_checks,
            self.common_loot_crate_groups,
            self.legendary_loot_crate_groups,
        )
        self.regions = {region.name: region for region in regions}

    def test_common_loot_crate_group_regions_have_correct_locations(self):
        expected_locations_per_region: list[list[str]] = [
            [CRATE_DROP_LOCATION_TEMPLATE.format(num=i) for i in range(1, 11)],
            [CRATE_DROP_LOCATION_TEMPLATE.format(num=i) for i in range(11, 21)],
            [CRATE_DROP_LOCATION_TEMPLATE.format(num=i) for i in range(21, 31)],
            [CRATE_DROP_LOCATION_TEMPLATE.format(num=i) for i in range(31, 36)],
        ]
        for region_idx, expected_locations in enumerate(expected_locations_per_region, start=1):
            region_name: str = CRATE_DROP_GROUP_REGION_TEMPLATE.format(num=region_idx)
            region: Region = self.regions[region_name]
            region_locations: list[str] = [location.name for location in region.locations]
            self.assertListEqual(
                region_locations, expected_locations, f"Locations did not match for region '{region_name}'."
            )

    def test_legendary_loot_crate_group_regions_have_correct_locations(self):
        expected_locations_per_region: list[list[str]] = [
            [LEGENDARY_CRATE_DROP_LOCATION_TEMPLATE.format(num=i) for i in range(1, 6)]
        ]
        for region_idx, expected_locations in enumerate(expected_locations_per_region, start=1):
            region_name: str = LEGENDARY_CRATE_DROP_GROUP_REGION_TEMPLATE.format(num=region_idx)
            region: Region = self.regions[region_name]
            region_locations: list[str] = [location.name for location in region.locations]
            self.assertListEqual(
                region_locations, expected_locations, f"Locations did not match for region '{region_name}'."
            )

    def test_character_regions_are_correct(self):
        for char in self.characters:
            expected_locations_for_char: list[str] = [
                RUN_COMPLETE_LOCATION_TEMPLATE.format(char=char),
                WAVE_COMPLETE_LOCATION_TEMPLATE.format(char=char, wave=5),
                WAVE_COMPLETE_LOCATION_TEMPLATE.format(char=char, wave=10),
                WAVE_COMPLETE_LOCATION_TEMPLATE.format(char=char, wave=15),
                WAVE_COMPLETE_LOCATION_TEMPLATE.format(char=char, wave=20),
            ]
            char_region_name = CHARACTER_REGION_TEMPLATE.format(char=char)
            char_region: Region = self.regions[char_region_name]
            char_region_locations: list[str] = [location.name for location in char_region.locations]
            self.assertListEqual(
                char_region_locations,
                expected_locations_for_char,
                f"Locations did not match for region '{char_region_name}'",
            )


class TestBrotatoRegionAccessRules(BrotatoTestBase):
    run_default_tests = False  # type:ignore
    options: ClassVar[dict[str, Any]] = {
        "num_victories": 10,
        "num_characters": 10,
        # Number of characters should match
        "include_base_game_characters": [
            "Brawler",
            "Crazy",
            "Mage",
            "Mutant",
            "Generalist",
            "Engineer",
            "Streamer",
            "Cyborg",
            "Jack",
            "Demon",
        ],
        "waves_per_drop": 4,
        "num_common_crate_drops": 25,
        "num_common_crate_drop_groups": 5,
        "num_legendary_crate_drops": 5,
        "num_legendary_crate_drop_groups": 1,
    }

    def test_common_loot_crate_group_regions_have_correct_access_rules(self):
        # 10 wins and 5 groups means 2 wins to unlock each group
        wins_per_group = [0, 2, 4, 6, 8]
        wins_collected = 0
        victory_item = self.multiworld.create_item(ItemName.RUN_COMPLETE.value, self.player)
        # For whatever reason, self.assertAccessDependency doesn't work, so we do the collect and sweep manually.
        for group_idx, num_wins_needed in enumerate(wins_per_group, start=1):
            region_name: str = CRATE_DROP_GROUP_REGION_TEMPLATE.format(num=group_idx)
            region: Region = self.multiworld.regions.region_cache[self.player][region_name]
            region_locations = [location.name for location in region.locations]
            while wins_collected < num_wins_needed:
                self.assertFalse(
                    self.multiworld.state.can_reach_region(region_name, self.player),
                    f"Should not be able to reach region {region_name} without {num_wins_needed} wins, have {wins_collected}.",  # noqa
                )
                for location in region_locations:
                    self.assertFalse(self.multiworld.state.can_reach_location(location, self.player))
                self.multiworld.state.collect(victory_item, prevent_sweep=True)
                wins_collected += 1

            self.assertTrue(self.multiworld.state.can_reach_region(region_name, self.player))
            for location in region_locations:
                self.assertTrue(self.multiworld.state.can_reach_location(location, self.player))

    def test_character_regions_have_correct_access_rules(self):
        characters = self.options["include_base_game_characters"]
        for char in characters:
            region_name = CHARACTER_REGION_TEMPLATE.format(char=char)
            region = self.multiworld.regions.region_cache[self.player][region_name]
            region_locations = [location.name for location in region.locations]
            if self.multiworld.state.has(char, self.player):
                # The multiworld needs to start with some characters, so this will get hit at least some of the time.
                # We can't remove characters from state here because assertAccessDependency just creates a new state
                # internally.
                self.assertTrue(self.multiworld.state.can_reach_region(region_name, self.player))
            else:
                self.assertAccessDependency(region_locations, [[char]])

from typing import ClassVar

from test.param import classvar_matrix
from . import MegaMixTestBase

# WARNING: mm_collection.song_items is subject to available megamix_mod_data from Players YAMLs during all tests.
# When testing locally this may affect length checks.

class TestOptionIncludes(MegaMixTestBase):
    """Set include_songs and test the multiworld item pool for their inclusion."""
    options = {
        "allow_megamix_dlc_songs": True,
        "duplicate_song_percentage": 0,
        "starting_song_count": 3,
        "additional_song_count": 15,
        "include_songs": ["Love is War [1]", "Packaged [10]", "Senbonzakura [216]", "Teo [271]"],
    }

    def test_included(self):
        world = self.get_world()
        pool = {song.name for song in world.multiworld.itempool if song.code >= 10}
        pool.update(world.starting_songs)
        pool.add(world.victory_song_name)

        self.assertTrue(world.options.include_songs.value.issubset(pool))

class TestOptionIncludesExact(MegaMixTestBase):
    """Set include_songs to the match the minimum required and verify the entire pool consists of them."""
    options = {
        "allow_megamix_dlc_songs": True,
        "duplicate_song_percentage": 0,
        "starting_song_count": 3,
        "additional_song_count": 15,
        "include_songs": [ # 19 songs for a 19 song seed (3+15+goal)
            "Love is War [1]", "The World is Mine [2]", "That One Second in Slow Motion [3]", "Jaded [4]", "Melt [5]",
            "Far Away [6]", "Strobo Nights [7]", "Star Story [8]", "Last Night, Good Night [9]", "Packaged [10]",
            "Rain With A Chance of Sweet*Drops [11]", "Marginal [12]", "Grumpy Waltz [13]", "Miracle Paint [14]",
            "Dreaming Leaf [15]", "VOC@LOID in Love [16]", "A Song of Wastelands, Forests, and Magic [17]",
            "Song of Life [18]", "moon [20]"
        ],
    }

    def test_include_exact(self):
        world = self.get_world()
        pool = {item.name for item in world.multiworld.itempool if item.code >= 10}
        pool.update(world.starting_songs)
        pool.add(world.victory_song_name)

        self.assertTrue(pool.issubset(set(world.options.include_songs)))

class TestOptionIncludesOverflow(MegaMixTestBase):
    """Set include_songs to more than the itempool can handle and verify the entire pool consists of them."""
    options = {
        "allow_megamix_dlc_songs": True,
        "duplicate_song_percentage": 0,
        "starting_song_count": 3,
        "additional_song_count": 15,
        "include_songs": [ # 20 songs for a 19 song seed (3+15+goal)
            "Love is War [1]", "The World is Mine [2]", "That One Second in Slow Motion [3]", "Jaded [4]", "Melt [5]",
            "Far Away [6]", "Strobo Nights [7]", "Star Story [8]", "Last Night, Good Night [9]", "Packaged [10]",
            "Rain With A Chance of Sweet*Drops [11]", "Marginal [12]", "Grumpy Waltz [13]", "Miracle Paint [14]",
            "Dreaming Leaf [15]", "VOC@LOID in Love [16]", "A Song of Wastelands, Forests, and Magic [17]",
            "Song of Life [18]", "moon [20]", "Beware of the Miku Miku Germs [21]"
        ]
    }

    def test_include_overflow(self):
        world = self.get_world()
        pool = {item.name for item in world.multiworld.itempool if item.code >= 10}
        pool.update(world.starting_songs)
        pool.add(world.victory_song_name)

        self.assertTrue(pool.issubset(world.options.include_songs.value))


@classvar_matrix(percent=[10, 39, 99, 100])
class TestIncludesPercentage(MegaMixTestBase):
    """Set include_ and exclude_songs to an item group (MikuSongs) and verify the percentage of the seed for them.
    Excluding the same songs guarantees they cannot appear in the song pool again."""
    percent: ClassVar[int]
    options = {
        "allow_megamix_dlc_songs": True,
        "duplicate_song_percentage": 0,
        "starting_song_count": 10,
        "additional_song_count": 40,
    }

    def test_includes_percentage(self):
        group_miku = self.world.item_name_groups["MikuSongs"]
        self.options["include_songs_percentage"] = self.percent
        self.options["include_songs"] = group_miku
        self.options["exclude_songs"] = group_miku
        self.world_setup()

        pool = {song.name for song in self.world.multiworld.itempool if song.code >= 10}
        pool.update(self.world.starting_songs)
        pool.add(self.world.victory_song_name)

        match = {song for song in pool if song in group_miku}
        count = len(pool) * self.percent // 100

        self.assertEqual(len(match), count)


class TestOptionExcludes(MegaMixTestBase):
    """Set exclude_songs and test the multiworld item pool for their absence."""
    options = {
        "allow_megamix_dlc_songs": True,
        "duplicate_song_percentage": 0,
        "starting_song_count": 10,
        "additional_song_count": 251,
        "exclude_songs": ["Love is War [1]", "Packaged [10]", "Senbonzakura [216]", "Teo [271]"],
    }

    def test_excluded(self):
        world = self.get_world()
        pool = {song.name for song in world.multiworld.itempool if song.code >= 10}
        pool.update(world.starting_songs)
        pool.add(world.victory_song_name)

        self.assertEqual(len(pool), len(world.mm_collection.song_items) - len(world.options.exclude_songs.value))
        self.assertFalse(world.options.exclude_songs.value.issubset(pool))


@classvar_matrix(group=['MikuSongs', 'RinSongs', 'LenSongs', 'LukaSongs', 'KAITOSongs', 'MEIKOSongs', 'BaseSongs', 'DLCSongs', 'Grasssanity'])
class TestOptionExcludeItemGroups(MegaMixTestBase):
    """Set exclude_songs to an item group and test the multiworld item pool for their absence."""
    run_default_tests = False # Greatly speeds up testing time
    group: ClassVar[str]
    options = {
        "allow_megamix_dlc_songs": True,
        "additional_song_count": 251,
    }

    def test_exclude_group(self):
        group_songs = self.world.item_name_groups[self.group]
        self.options["exclude_songs"] = group_songs
        self.world_setup()

        pool = {song.name for song in self.world.multiworld.itempool if song.code >= 10}
        pool.update(self.world.starting_songs)
        pool.add(self.world.victory_song_name)

        intersect = pool.intersection(group_songs)
        self.assertEqual(0, len(intersect), f"0 songs from {self.group} expected, got {len(intersect)}: {intersect}")
        self.assertEqual(len(group_songs) + len(pool), len(self.world.mm_collection.song_items))


class TestTrapsFull(MegaMixTestBase):
    """Set trap settings to extremes."""
    options = {
        "duplicate_song_percentage": 0,
        "trap_percentage": 100,
    }


class TestOptionNoDLC(MegaMixTestBase):
    options = {
        "allow_megamix_dlc_songs": False,
        "additional_song_count": 251,
    }

    def test_no_dlc(self):
        pool = {song.name for song in self.world.multiworld.itempool if song.code >= 10}
        pool.update(self.world.starting_songs)
        pool.add(self.world.victory_song_name)
        dlc = {song for song in pool if self.world.mm_collection.song_items.get(song).DLC}

        self.assertEqual(0, len(dlc), f"DLC is disabled, got {len(dlc)} in the item pool.")

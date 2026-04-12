#AP
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, components, Type, launch_subprocess
from BaseClasses import Region, Item, ItemClassification, Tutorial
from Options import PerGameCommonOptions, OptionError
import settings

#Local
from .Options import MegaMixOptions, megamix_option_groups
from .Items import MegaMixSongItem, MegaMixFixedItem
from .Locations import MegaMixLocation
from .MegaMixCollection import MegaMixCollections
from .DataHandler import get_player_specific_ids

#Python
from typing import ClassVar, TextIO
from math import floor


def launch_client():
    from .Client import launch
    launch_subprocess(launch, name="MegaMixClient")


components.append(Component(
    "Mega Mix Client",
    func=launch_client,
    component_type=Type.CLIENT
))


def launch_json_generator():
    from .generator_megamix.generator import launch
    launch_subprocess(launch, name="MegaMixJSONGenerator")


components.append(Component(
    "Mega Mix JSON Generator",
    func=launch_json_generator,
    component_type=Type.ADJUSTER
))

class MegaMixSettings(settings.Group):
    class GameExe(settings.LocalFilePath):
        """
        Path to the HMPDMM+'s game exe. Usually ends with "DivaMegaMix.exe"
        Players (Mega Mix Clients) must have this set correctly in THEIR host.yaml.
        Generating and hosting do not rely on this.
        """
        description = "Hatsune Miku Project DIVA Mega Mix+ game executable"
        is_exe = True
        md5s = ["813e1befae1776d4fafdf907e509b28b"] # 1.03

    game_exe: GameExe = GameExe("C:/Program Files (x86)/Steam/steamapps/common/Hatsune Miku Project DIVA Mega Mix Plus/DivaMegaMix.exe")


class MegaMixWebWorld(WebWorld):
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="A guide to setting up the Megamix Randomizer for MultiworldGG multiworld games.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["Cynichill"]
        )
    ]
    theme = "ocean"
    bug_report_page = "https://github.com/Cynichill/DivaAPworld/issues"
    option_groups = megamix_option_groups

class MegaMixWorld(World):
    """Hatsune Miku: Project Diva Mega Mix+ is a rhythm game where you hit notes to the beat of one of 250+ songs.
    Play through a selection of randomly chosen songs, collecting leeks
    until you have enough to play and complete the goal song!"""

    # World Options
    game = "Hatsune Miku Project Diva Mega Mix+"

    settings: ClassVar[MegaMixSettings]
    options_dataclass: ClassVar[PerGameCommonOptions] = MegaMixOptions
    options: MegaMixOptions

    topology_present = False
    web = MegaMixWebWorld()
    ut_can_gen_without_yaml = True

    # Necessary Data
    mm_collection = MegaMixCollections()

    item_name_to_id = {name: code for name, code in mm_collection.item_names_to_id.items()}
    location_name_to_id = {name: code for name, code in mm_collection.location_names_to_id.items()}
    item_name_groups = mm_collection.get_item_name_groups()

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)
        # Working Data
        self.player_mod_data = {}
        self.player_mod_ids = {}
        self.player_mod_remap = {}
        self.victory_song_name: str = ""
        self.victory_song_id: int = 10
        self.starting_songs: list[str] = []
        self.included_songs: list[str] = []
        self.final_song_ids: set[int] = set()
        self.prog_hp_added: int = 0

    def generate_early(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            slot_data: dict[str, any] = re_gen_passthrough[self.game]

            self.options.progressive_hp.value = int(slot_data.get("progHP", 0)) + 1

            # Inject mod data, remap as needed
            from .SymbolFixer import format_song_name
            from .Items import SongData
            remap = slot_data.get("modRemap", {})
            for pack, items in slot_data.get("modData", {}).items():
                for item in items: # for name, song_id in items
                    # Temporary back-compat for testing on older world gens
                    name = "Modded Song" if isinstance(item, int) else item[0]
                    song_id = item if isinstance(item, int) else item[-1]

                    formatted_name = format_song_name(name, song_id)
                    item_id = remap.get(str(song_id), song_id * 10)

                    self.mm_collection.song_items[formatted_name] = SongData(item_id, song_id, set(), False, True, [])
                    for i in range(2):
                        self.mm_collection.song_locations[f"{formatted_name}-{i}"] = (item_id + i)
            self.item_id_to_name.update({data.code: name for name, data in self.mm_collection.song_items.items()})

            if "finalSongIDs" in slot_data:
                final = slot_data.get("finalSongIDs", [])
                self.included_songs = [key for key, song in self.mm_collection.song_items.items() if song.songID in final]
            return

        # Initial search criteria
        lower_rating_threshold, higher_rating_threshold = self.get_difficulty_range()
        lower_diff_threshold, higher_diff_threshold = self.get_available_difficulties(self.options.song_difficulty_min.value, self.options.song_difficulty_max.value)
        self.player_mod_data, self.player_mod_ids, self.player_mod_remap = get_player_specific_ids(self.options.megamix_mod_data.value, self.mm_collection.mod_remaps)

        while True:
            # In most cases this should only need to run once

            allowed_difficulties = list(range(lower_diff_threshold, higher_diff_threshold + 1))
            available_song_keys = self.mm_collection.get_songs_with_settings(bool(self.options.allow_megamix_dlc_songs.value), self.player_mod_ids, allowed_difficulties, lower_rating_threshold, higher_rating_threshold)

            available_song_keys = self.handle_plando(available_song_keys)
            #print(f"{lower_rating_threshold}~{higher_rating_threshold}* {allowed_difficulties}", len(available_song_keys))

            # The minimum amount of songs to make an ok rando would be Starting Songs + 10 interim songs + Goal song.
            # - Interim songs being equal to max starting song count.
            count_needed_for_start = max(0, self.options.starting_song_count.value - len(self.starting_songs)) + 11
            if len(available_song_keys) + len(self.included_songs) >= count_needed_for_start:
                final_song_list = available_song_keys
                break

            # If the above fails, we want to adjust the difficulty thresholds.
            # Easier first, then harder
            if lower_rating_threshold <= 1 and higher_rating_threshold >= 10 and len(allowed_difficulties) >= 5:
                raise OptionError("Failed to find enough songs, even with maximum difficulty thresholds.")
            elif lower_rating_threshold <= 1:
                if higher_rating_threshold > 10:
                    # Reset ratings, adjust diff. Maybe buff/nerf initial ratings when lowering/raising diff.
                    lower_rating_threshold, higher_rating_threshold = self.get_difficulty_range()

                    if lower_diff_threshold <= 0 and higher_diff_threshold < 4: higher_diff_threshold += 1
                    if lower_diff_threshold > 0: lower_diff_threshold -= 1

                    lower_diff_threshold, higher_diff_threshold = self.get_available_difficulties(lower_diff_threshold, higher_diff_threshold)
                else:
                    higher_rating_threshold += 0.5
            else:
                lower_rating_threshold -= 0.5

        self.create_song_pool(final_song_list)

        for song in self.starting_songs:
            self.multiworld.push_precollected(self.create_item(song))

    def handle_plando(self, available_song_keys: list[str]) -> list[str]:
        # The ModdedSongs group is shared across all players. Limit to own songs (base, DLC, modded).
        dlc = self.options.allow_megamix_dlc_songs.value
        song_items = {s for s, v in self.mm_collection.song_items.items() if
                      dlc or not v.DLC and not v.modded or v.songID in self.player_mod_ids}

        start_items = song_items & self.options.start_inventory.value.keys()
        goal_songs = song_items & self.options.goal_song.value - start_items
        include_songs = song_items & self.options.include_songs.value - start_items
        exclude_songs = self.options.exclude_songs.value

        if goal_songs:
            self.victory_song_name = self.random.choice(sorted(goal_songs))
            start_items.discard(self.victory_song_name)
            include_songs.discard(self.victory_song_name)
        self.starting_songs = sorted(start_items)

        # Incl songs, Incl%, and Excl. Minimal logic of create_song_pool.
        pool = set(available_song_keys) - start_items - include_songs - exclude_songs
        player_size = self.options.starting_song_count.value + self.options.additional_song_count.value
        pool_size = 1 + min(len(pool | start_items | include_songs), player_size)

        # Sample Incl%, add non-Incl+Excl back to pool.
        include_size = pool_size * self.options.include_songs_percentage.value // 100
        self.included_songs = self.random.sample(sorted(include_songs), k=min(len(include_songs), include_size))
        pool |= include_songs - set(self.included_songs) - exclude_songs

        return sorted(pool)

    def create_song_pool(self, available_song_keys: list[str]):
        starting_song_count = self.options.starting_song_count.value
        additional_song_count = self.options.additional_song_count.value
        self.random.shuffle(available_song_keys)

        # First, we must double-check if the player has included too many guaranteed songs
        included_song_count = len(self.included_songs)
        if included_song_count > additional_song_count:
            # If so, we want to thin the list, thus let's get starter songs while we are at it.
            self.random.shuffle(self.included_songs)
            if not self.victory_song_name:
                self.victory_song_name = self.included_songs.pop()
            while len(self.included_songs) > additional_song_count:
                next_song = self.included_songs.pop()
                if len(self.starting_songs) < starting_song_count:
                    self.starting_songs.append(next_song)
        elif not self.victory_song_name:
            # If not, choose a random victory song from the available songs
            chosen_song = self.random.randrange(0, len(available_song_keys) + included_song_count)
            if chosen_song < included_song_count:
                self.victory_song_name = self.included_songs[chosen_song]
                del self.included_songs[chosen_song]
            else:
                self.victory_song_name = available_song_keys[chosen_song - included_song_count]
                del available_song_keys[chosen_song - included_song_count]
        elif self.victory_song_name in available_song_keys:
            available_song_keys.remove(self.victory_song_name)

        # Next, make sure the starting songs are fulfilled
        if len(self.starting_songs) < starting_song_count:
            for _ in range(len(self.starting_songs), starting_song_count):
                if len(available_song_keys) > 0:
                    self.starting_songs.append(available_song_keys.pop())
                else:
                    self.starting_songs.append(self.included_songs.pop())

        # Then attempt to fulfill any remaining songs for interim songs
        if len(self.included_songs) < additional_song_count:
            for _ in range(len(self.included_songs), self.options.additional_song_count.value):
                if len(available_song_keys) <= 0:
                    break
                self.included_songs.append(available_song_keys.pop())

        victory_song = self.mm_collection.song_items.get(self.victory_song_name)
        self.victory_song_id = (victory_song.code // 10) * 10
        self.final_song_ids.add(victory_song.songID)

    def create_item(self, name: str) -> Item:

        if name == self.mm_collection.LEEK_NAME:
            return MegaMixFixedItem(name, ItemClassification.progression_skip_balancing, self.mm_collection.LEEK_CODE, self.player)

        elif name == self.mm_collection.FILLER_NAME:
            return MegaMixFixedItem(name, ItemClassification.filler, self.mm_collection.FILLER_CODE, self.player)

        elif name in self.mm_collection.trap_items:
            return MegaMixFixedItem(name, ItemClassification.trap, self.mm_collection.trap_items.get(name), self.player)

        elif name == "Progressive HP":
            return MegaMixFixedItem(name, ItemClassification.progression | ItemClassification.useful, 3, self.player)

        song = self.mm_collection.song_items.get(name)
        self.final_song_ids.add(song.songID)
        return MegaMixSongItem(name, self.player, song)

    def create_items(self) -> None:
        items_left = len(self.multiworld.get_unfilled_locations(self.player))

        for _ in range(0, self.get_leek_count()):
            self.multiworld.itempool.append(self.create_item(self.mm_collection.LEEK_NAME))

        self.multiworld.itempool.extend(self.create_item(song) for song in self.included_songs)

        items_left -= self.get_leek_count() + len(self.included_songs)
        if items_left <= 0:
            return

        # N-1 prog HP
        for _ in range(1, min(items_left, self.options.progressive_hp.value)):
            self.prog_hp_added += 1
            self.multiworld.itempool.append(self.create_item("Progressive HP"))
            items_left -= 1

        # Add duplicates based on user percentage
        dupe_count = items_left * self.options.duplicate_song_percentage // 100
        items_left -= dupe_count

        song_keys_in_pool = self.included_songs.copy()
        self.random.shuffle(song_keys_in_pool)
        for i in range(0, dupe_count):
            item = self.create_item(song_keys_in_pool[i % len(song_keys_in_pool) - 1])
            item.classification = ItemClassification.useful
            self.multiworld.itempool.append(item)

        # Add traps based on user percentage and unfilled by dupes
        trap_count = items_left * self.options.trap_percentage // 100
        enabled_traps = sorted(self.options.traps_enabled.value)

        if trap_count and enabled_traps:
            items_left -= trap_count
            for _ in range(0, trap_count):
                self.multiworld.itempool.append(self.create_item(self.random.choice(enabled_traps)))

        for _ in range(0, items_left):
            self.multiworld.itempool.append(self.create_item(self.mm_collection.FILLER_NAME))

    def create_regions(self) -> None:
        menu_region = Region("Menu", self.player, self.multiworld)
        self.multiworld.regions += [menu_region]

        all_selected_locations = self.starting_songs + self.included_songs

        # Adds 2 item locations per song to the menu region.
        for name in all_selected_locations:
            for j in range(2):
                loc = MegaMixLocation(self.player, f"{name}-{j}", self.mm_collection.song_locations[f"{name}-{j}"], menu_region)
                loc.access_rule = lambda state, item=name: state.has(item, self.player)
                menu_region.locations.append(loc)

    def set_rules(self) -> None:
        self.multiworld.completion_condition[self.player] = lambda state: \
            state.has(self.mm_collection.LEEK_NAME, self.player, self.get_leek_win_count()) \
            and state.has("Progressive HP", self.player, self.prog_hp_added)

    def get_leek_count(self) -> int:
        """Number of Leeks to be placed in the item pool based on user option and final song count."""
        multiplier = self.options.leek_count_percentage.value / 100.0
        song_count = len(self.starting_songs) + len(self.included_songs)
        return max(1, floor(song_count * multiplier))

    def get_leek_win_count(self) -> int:
        """Number of Leeks out of all in the item pool needed to goal."""
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            return re_gen_passthrough[self.game].get("leekWinCount")

        multiplier = self.options.leek_win_count_percentage.value / 100.0
        leek_count = self.get_leek_count()
        return max(1, floor(leek_count * multiplier))

    def get_difficulty_range(self) -> list[float]:

        # Generate the number_to_option_value dictionary using the formula
        number_to_option_value = {i: 1 + i * 0.5 if i % 2 != 0 else int(1 + i * 0.5) for i in range(19)}

        minimum_difficulty = number_to_option_value.get(self.options.song_difficulty_rating_min.value, None)
        maximum_difficulty = number_to_option_value.get(self.options.song_difficulty_rating_max.value, None)
        difficulty_bounds = [min(minimum_difficulty, maximum_difficulty), max(minimum_difficulty, maximum_difficulty)]

        return difficulty_bounds

    def write_spoiler_header(self, spoiler_handle: TextIO):
        spoiler_handle.write(f"Selected Goal Song:              {self.victory_song_name}\n")
        spoiler_handle.write(f"Final Progressive HP:            {self.prog_hp_added}\n")

    @staticmethod
    def get_available_difficulties(song_difficulty_min: int, song_difficulty_max: int) -> list[int]:
        min_diff = min(song_difficulty_min, song_difficulty_max)
        max_diff = max(song_difficulty_min, song_difficulty_max)

        return [min_diff, max_diff]

    @staticmethod
    def interpret_slot_data(slot_data: dict[str, any]) -> dict[str, any]:
        return slot_data

    def fill_slot_data(self):
        return {
            "victoryLocation": self.victory_song_name,
            "victoryID": self.victory_song_id,
            "finalSongIDs": self.final_song_ids,
            "leekWinCount": self.get_leek_win_count(),
            "scoreGradeNeeded": self.options.grade_needed.value,
            "autoRemove": bool(self.options.auto_remove_songs),
            "deathLink": self.options.death_link.value,
            "deathLink_Amnesty": self.options.death_link_amnesty.value,
            "modData": {pack: [[song[0], song[1]] for song in songs if song[1] in self.final_song_ids]
                        for pack, songs in self.player_mod_data.items()},
            "modRemap": self.player_mod_remap,
            "progHP": self.prog_hp_added,
        }

# Local
from .Items import SongData
from .SymbolFixer import format_song_name
from .MegaMixSongData import SONG_DATA, base_game_ids, dlc_ids
from .DataHandler import extract_mod_data_to_json

# Python
from collections import ChainMap
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class MegaMixCollections:
    """Contains all the data of MegaMix, loaded from songData.json"""

    LEEK_NAME: str = "Leek"
    LEEK_CODE: int = 1

    FILLER_NAME: str = "SAFE"
    FILLER_CODE: int = 2

    PROG_HP_NAME: str = "Progressive HP"
    PROG_HP_CODE: int = 3

    song_items: dict[str, SongData] = {}
    song_locations: dict[str, int] = {}

    # IDs 3-9 available. 10 is "Love is War [1]".
    trap_items: dict[str, int] = {
        "Hidden Trap": 4,
        "Sudden Trap": 5,
        # "High Speed Trap": 6,
        "Icon Trap": 9,
    }

    def __init__(self) -> None:
        self.item_names_to_id = ChainMap({self.LEEK_NAME: self.LEEK_CODE}, {self.FILLER_NAME: self.FILLER_CODE},
                                         {self.PROG_HP_NAME: self.PROG_HP_CODE}, self.song_items, self.trap_items)
        self.location_names_to_id = ChainMap(self.song_locations)

        self.song_items = SONG_DATA
        mod_data = extract_mod_data_to_json()

        self.mod_remaps: dict[int, dict[str, list]] = {}

        if mod_data:
            seen_mod_song_ids = set()
            seen_mod_item_ids = set()

            for data_dict in mod_data:
                for pack, songs in data_dict.items():
                    for song in songs:
                        if (
                            not isinstance(song, list)
                            or not list(map(type, song)) == [str, int, int]
                            or song[1] <= 0 or song[2] <= 0
                        ):
                            logger.warning(f"Skipping {pack} {song}")
                            continue

                        song_id = song[1]

                        if song_id in base_game_ids:
                            continue

                        song_name = format_song_name(song[0], song_id)
                        item_id = (song_id * 10)

                        if song_name in self.song_items:
                            logger.warning(f"{song_name} previously mapped to base ID, skipping")
                            continue

                        # Remap up to 4 ID conflicts using the 8 free slots (2-9) between item/loc IDs.
                        if song_id in seen_mod_song_ids:
                            if song_id in self.mod_remaps and song_name in self.mod_remaps[song_id]:
                                logger.warning(f"{song_name} already remapped to {self.mod_remaps[song_id][song_name]}")
                                continue

                            resolve = {i for i in range(item_id + 2, item_id + 10)}
                            resolve -= seen_mod_item_ids
                            new_slots = sorted(resolve)[0:2]

                            if len(new_slots) != 2:
                                raise Exception(f"Could not remap conflict of {song_name} (out of slots)\n"
                                                f"{self.mod_remaps[song_id]}")
                            logger.warning(f"Remapped {song_name} to {new_slots}")

                            item_id = new_slots[0]
                            seen_mod_item_ids.update(new_slots)

                            self.mod_remaps.setdefault(song_id, {})
                            self.mod_remaps[song_id][song_name] = new_slots
                        seen_mod_song_ids.add(song_id)

                        # Shift difficulty bitfields from modded data into [#,#,#,#,#]
                        diff_info = []
                        while len(diff_info) < 5:
                            diff = song[2] & 15
                            half = bool(song[2] >> 4 & 1)
                            # there might be a perf difference over time between this VS reversing after it's full, deque, etc
                            diff_info.insert(0, diff + (.5 if half else 0.0))
                            song[2] >>= 5

                        self.song_items[song_name] = SongData(item_id, song_id, set(), song_id in dlc_ids, True, diff_info)

        self.item_names_to_id.update({name: data.code for name, data in self.song_items.items()})

        for song_name, song_data in self.song_items.items():
            for i in range(2):
                self.song_locations[f"{song_name}-{i}"] = (song_data.code + i)

    def get_songs_with_settings(self, dlc: bool, mod_ids: list[int], allowed_diff: list[int], diff_lower: float, diff_higher: float) -> list[str]:
        """Gets a list of all songs that match the filter settings. Difficulty thresholds are inclusive."""
        filtered_list = []

        for songKey, songData in self.song_items.items():

            song_id = songData.songID

            # If song is DLC and DLC is disabled, skip song
            if songData.DLC and not dlc:
                continue

            # Skip modded song if not intended for this player
            if songData.modded and song_id not in mod_ids:
                continue

            # Do not give base game version if modded cover available for this player
            if not songData.modded and song_id in mod_ids:
                continue

            for diff in allowed_diff:
                if songData.difficulties[diff] > 0.0: # Has that difficulty
                    if diff_lower <= songData.difficulties[diff] <= diff_higher:
                        filtered_list.append(songKey)
                        break

        return filtered_list

    def get_item_name_groups(self) -> dict[str, set]:
        base_songs = {name: data for name, data in self.song_items.items() if not data.modded}
        groups = {
            "BaseSongs": {name for name, data in base_songs.items() if not data.DLC},
            "DLCSongs": {name for name, data in base_songs.items() if data.DLC},

            "MikuSongs": {name for name, data in base_songs.items() if "Hatsune Miku" in data.singers},
            "RinSongs": {name for name, data in base_songs.items() if "Kagamine Rin" in data.singers},
            "LenSongs": {name for name, data in base_songs.items() if "Kagamine Len" in data.singers},
            "LukaSongs": {name for name, data in base_songs.items() if "Megurine Luka" in data.singers},
            "KAITOSongs": {name for name, data in base_songs.items() if "KAITO" in data.singers},
            "MEIKOSongs": {name for name, data in base_songs.items() if "MEIKO" in data.singers},
        }

        # Experimental since all players share this group. Filtered in handle_plando.
        modded = {name for name, data in self.song_items.items() if data.modded}
        if modded: # test_groups::TestNameGroups::test_item_name_groups_not_empty
            groups.update({"ModdedSongs": modded})

        return groups

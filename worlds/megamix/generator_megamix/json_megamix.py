import json
import os.path
from pathlib import Path
import re

from ..SymbolFixer import fix_song_name
from ..MegaMixSongData import base_game_ids

class ConflictException(Exception):
    pass

def process_mods(mods_folder: str, mod_pv_dbs_path_list: list[str]) -> tuple[int, str]:
    """
    Accumulates song metadata across the provided mod_pv_dbs and returns JSON.

    mod_pv_dbs_path_list
      A list of paths to mod_pv_db.txt. Extracts the mod folder name too.
    """
    mod_song_collection = {}
    unique_seen_ids = {}

    for mod_path in mod_pv_dbs_path_list:
        mod_dir = Path(mod_path)#.parents[1]
        mod_folder = str(Path(mod_dir).relative_to(mods_folder))
        mod_folder = mod_folder.replace("'", "''")

        song_pack_ids, song_pack_list = process_single_mod(mod_path, str(mod_dir))

        # Beyond overkill, beyond useful.
        intersect_check = set(unique_seen_ids.keys()).intersection(song_pack_ids)
        if intersect_check:
            conflict_packs = [unique_seen_ids.get(song_id) for song_id in intersect_check] + [mod_folder]
            raise ConflictException(set(conflict_packs), sorted(intersect_check))

        unique_seen_ids |= {song_id: mod_folder for song_id in song_pack_ids}
        if song_pack_list:
            mod_song_collection[mod_folder] = song_pack_list

    return len(unique_seen_ids), finalize_json(mod_song_collection)

def process_single_mod(mod_pv_db_path: str, mod_dir: str) -> tuple[set[int], list[list[str,int,int]]]:
    difficulties = ["exextreme", "extreme", "hard", "normal", "easy"] # see shift_difficulty()
    songs = {}
    song_pack_ids = set()
    diff_lockout = {} # Well if it isn't the consequences of my own actions.

    dbs = []
    mod_pv_db = Path(mod_pv_db_path) / "rom" / "mod_pv_db.txt"
    mod_nc_pv_db = Path(mod_pv_db_path) / "rom" / "mod_nc_pv_db.txt"

    if mod_nc_pv_db.exists():
        dbs.append(mod_nc_pv_db)
    if mod_pv_db.exists():
        dbs.append(mod_pv_db)

    for pv_db_path in dbs:
        with open(pv_db_path, "r", encoding='utf-8') as input_file:
            mod_pv_db = input_file.read()
        mod_pv_db = set(re.findall(rf'^(?:#ARCH#)?pv_(\d+)\.(song_name(?:_en)?|difficulty)(?:\.([^.]+)\.(\d|length)\.?(level|script_file_name|attribute\.extra)?)?=(.*)$', mod_pv_db, re.MULTILINE))

        for line in sorted(mod_pv_db):
            song_id, song_prop, diff_rating, diff_index_length, diff_prop, value = line

            if int(song_id) in base_game_ids:
                continue

            songs.setdefault(song_id, ["", int(song_id), 0])
            diff_lockout.setdefault(song_id, [False] * 5)
            song_pack_ids.add(song_id)

            match song_prop:
                case "song_name_en":
                    songs[song_id][0] = fix_song_name(value).replace("'", "''")
                case "song_name":
                    if not songs[song_id][0]:
                        songs[song_id][0] = fix_song_name(value).replace("'", "''")
                case "difficulty" if not diff_rating == "encore":
                    extra_check = song_id, song_prop, diff_rating, '1', 'attribute.extra', '1'
                    diff_rating = "exextreme" if diff_index_length == "1" and diff_rating == "extreme" else diff_rating

                    # Sanity check for invalid extreme data (starts at 1 index/out of 0-2 range of length prop): check the extra attribute.
                    if diff_rating is "exextreme" and extra_check not in mod_pv_db:
                        print(f"{song_id} appears ExEx but lacks attribute, downgrade to Ex")
                        diff_rating = "extreme"

                    diff_index = difficulties.index(diff_rating)

                    if diff_index_length == "length" and value == "0":
                        diff_lockout[song_id][diff_index] = True
                        songs[song_id][2] = shift_difficulty(songs[song_id][2], diff_index, 31.0)

                    match diff_prop:
                        case "level" if not diff_lockout[song_id][diff_index]:
                            songs[song_id][2] = shift_difficulty(songs[song_id][2], diff_index, float(".".join(value.split("_")[2:4])))
                        case "script_file_name" if int(song_id) not in base_game_ids: # 99% covers. Good luck everyone.
                            # Verify DSC exists. Check parents for "modular" packs.
                            if not (Path(pv_db_path) / value).exists() \
                               and not (Path(pv_db_path).parents[1] / value).exists() \
                               and not (Path(pv_db_path).parents[2] / value).exists():
                                print(f"{song_id} No {difficulties[diff_index]} DSC at {value}")
                                diff_lockout[song_id][diff_index] = True
                                songs[song_id][2] = shift_difficulty(songs[song_id][2], diff_index, 31.0)

    return song_pack_ids, [songs[song] for song in songs if songs[song][2] > 0]

def shift_difficulty(current_diffs: int = 0, index: int = 0, level_float: float = 0.0) -> int:
    """
    Accumulates difficulties in a bitfield to save space in the export.
    Easy MSB (index 4) <- ExEx LSB (index 0) due to Ex/ExEx prevalence.
    Each diff is stored as 5 bits with MSB indicating the .5: 9.5 = 0b11001
    Masks off missing DSCs with NOT 31. Locking handled in caller.
    """

    level_int = (int(level_float) | (not level_float.is_integer()) << 4) << 5 * index
    current_diffs = current_diffs & ~level_int if level_float == 31 else current_diffs | level_int

    return current_diffs

def finalize_json(mod_song_collection: dict) -> str:
    output = json.dumps(mod_song_collection, separators=(',', ':'))
    return f"'{output}'" # Wrapped in ' for the YAML.

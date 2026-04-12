from dataclasses import dataclass
from Options import Toggle, Range, Choice, FreeText, PerGameCommonOptions, DeathLink, TextChoice, OptionGroup, StartInventoryPool, Visibility, OptionSet
import requests
import json
import os
import time
import logging
import re
import Utils

logger = logging.getLogger("SM64Hacks")


def _get_json_files_from_github():
    """Fetch list of JSON files from GitHub repository, with caching."""
    cache_path = os.path.join(Utils.user_path(), "sm64hack_jsons", "json_list_cache.json")
    cache_duration = 86400
    
    if os.path.exists(cache_path):
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
                if time.time() - cache_data.get('timestamp', 0) < cache_duration:
                    return cache_data.get('files', [])
        except Exception as e:
            logger.debug(f"Could not read cache: {e}")
    
    json_files = []
    api_base = "https://api.github.com/repos/DNVIC/sm64hack-archipelago-jsons/contents"
    
    try:
        root_response = requests.get(api_base, timeout=10)
        root_response.raise_for_status()
        folders = [item['name'] for item in root_response.json() if item.get('type') == 'dir']
        
        if not folders:
            logger.warning("No folders found in GitHub repository")
            return []
        
        for folder in folders:
            try:
                response = requests.get(f"{api_base}/{folder}", timeout=10)
                response.raise_for_status()
                for item in response.json():
                    if item.get('type') == 'file' and item.get('name', '').endswith('.json'):
                        json_files.append(item['name'])
            except requests.RequestException as e:
                logger.warning(f"Could not fetch {folder} folder from GitHub: {e}")
                continue
        
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)
        with open(cache_path, 'w') as f:
            json.dump({'timestamp': time.time(), 'files': json_files}, f)
        
        return json_files
    except Exception as e:
        logger.warning(f"Could not fetch JSON list from GitHub: {e}")
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r') as f:
                    return json.load(f).get('files', [])
            except Exception:
                pass
        return []


def _filename_to_option_name(filename: str) -> str:
    """Convert JSON filename to option attribute name."""
    name = filename.replace('.json', '').lower().replace('.', '_dot_')
    name = re.sub(r'[^a-z0-9_]', '_', name)
    name = re.sub(r'_+', '_', name).strip('_')
    return name


def _format_display_name(filename: str) -> str:
    """Format JSON filename for display, splitting before numbers, brackets, or uppercase letters."""
    display_name = filename.replace('.json', '')
    
    display_name = re.sub(r'(?<=[a-z])(?=[A-Z])', ' ', display_name)
    display_name = re.sub(r'(?<!^)(?<![0-9.])(?=\.?\d)', ' ', display_name)
    display_name = re.sub(r'(?<!^)(?=[\[\](){}])', ' ', display_name)
    display_name = re.sub(r'(?<=\d)(?=[A-Za-z])', ' ', display_name)
    display_name = re.sub(r'(?<=[\[\](){}])(?=[A-Za-z])', ' ', display_name)
    
    display_name = re.sub(r'\.\s+(\d)', r'.\1', display_name)
    display_name = re.sub(r'\(\s+', '(', display_name)
    display_name = re.sub(r'\s+\)', ')', display_name)
    display_name = re.sub(r'\s+', ' ', display_name).strip()
    
    if display_name:
        display_name = display_name[0].upper() + display_name[1:]
    
    display_name = re.sub(r'(?i)\b([Ss][Mm])(\d)', r'SM\2', display_name)
    display_name = re.sub(r'(?i)\b([Ss][Mm])\b', 'SM', display_name)
    
    return display_name


def _populate_json_file_options():
    """Dynamically populate JsonFile class with options from GitHub."""
    json_files = _get_json_files_from_github()

    if not json_files:
        logger.warning("No JSON files found from GitHub, using fallback list")
        json_files = [
            "Super Mario 64.json",
            "24 Hour Hack.json",
            "Aventure Alpha Redone.json",
            "Cursed Castles.json",
            "Despair Marios Gambit 64.json",
            "Eureka.json",
            "Grand Star.json",
            "Kaizo Mario 64.json",
            "Koopa Power.json",
            "Lugs Delightful Dioramas.json",
            "Marios New Earth.json",
            "Peachs Memory.json",
            "Phenomena.json",
            "Plutonium Mario 64.json",
            "Sapphire.json",
            "Shining Stars Repainted.json",
            "SM64 The Green Stars.json",
            "SM74 TYA.json",
            "Star Revenge 0.json",
            "Star Revenge 1.5.json",
            "Star Revenge 2 TTM.json",
            "Star Revenge 3.json",
            "Star Revenge 3.5.json",
            "Star Revenge 4.json",
            "Star Revenge 4.5.json",
            "Star Revenge 5.json",
            "Star Revenge 5.5.json",
            "Star Revenge 6.json",
            "Star Revenge 6.25.json",
            "Star Revenge 6.5.json",
            "Star Revenge 7.json",
            "Star Revenge 7.5.json",
            "Star Revenge 7.5 Expert.json",
            "Star Revenge 8.json",
            "Star Revenge 8 Advanced.json",
            "Super Donkey Kong 64.json",
            "Super Mario 74.json",
            "Super Mario Fantasy 64.json",
            "Super Mario Star Road.json",
            "Super Mario Treasure World.json",
            "Timeless Rendezvous.json",
            "Unoriginal Cringe Meme Hack.json",
            "Ztar Attack 2.json",
            "Ztar Attack Rebooted.json",
        ]

    option_value = 1
    new_options = {}
    new_name_lookup = {}
    for json_file in sorted(json_files):
        option_name = _filename_to_option_name(json_file)
        setattr(JsonFile, f"option_{option_name}", option_value)
        new_options[json_file.lower()] = option_value
        new_name_lookup[option_value] = json_file
        option_value += 1

    JsonFile.options.update(new_options)
    JsonFile.name_lookup.update(new_name_lookup)

    default_value = None
    for json_file in sorted(json_files):
        normalized = re.sub(r'[^a-z0-9]', '', json_file.lower().replace('.json', ''))
        if normalized == "supermario64" or "supermario64" in normalized:
            default_value = new_options.get(json_file.lower())
            break

    if default_value is not None:
        JsonFile.default = default_value
    elif option_value > 1:
        JsonFile.default = 1
        logger.warning("Could not find Super Mario 64, using first option as default")
    else:
        logger.error("No options were populated, cannot set default")

class JsonFile(TextChoice):
    """Name of the hack to use. Set to the JSON filename, e.g. 'Star Revenge 7.json'.
    For custom JSONs, place the file in data/sm64hacks/custom_jsons/ and use its filename here.
    Note that custom values are not supported in web generation."""
    auto_display_name = True
    display_name = "Hack to Use"
    default = 1  # Will be set by _populate_json_file_options()

    @classmethod
    def get_option_name(cls, value) -> str:
        if isinstance(value, str):
            return _format_display_name(value)
        return _format_display_name(cls.name_lookup[value])
    
# Populate JsonFile options from GitHub on module import
_populate_json_file_options()

class ProgressiveKeys(Choice):
    """Makes the keys progressive items

    Off - Keys are not progressive items

    On - Keys are progressive items, you get Key 1 first and then Key 2
    May make generation impossible if there's only Key 2
    
    Reverse - Keys are progressive items, you get Key 2 first, and then Key 1
    May make generation impossible if there's only Key 1
    
    JSON - Go with the recommended value for the hack you are playing in the JSON
    Will only work with newer JSONs"""
    display_name = "Make keys progressive"
    option_off = 0
    option_on = 1
    option_reverse = 2
    option_json = 3
    default = 3

class TrollStars(Choice):
    """Enables checks for grabbing troll stars, if the JSON supports it.
    Note: Each world has 1 check shared among all its troll stars, not one check per troll star.
    
    Off - Troll stars are not randomized
    
    On - Troll stars are randomized"""
    option_off = 0
    option_on = 1
    display_name = "Troll Stars"

class RandomizeMoat(Toggle):
    """Shuffles the moat as a check in logic. If off, the moat will instead be placed in the vanilla location."""

class FillerUsefulWeight(Range):
    """Decides what percent chance of filler items should be somewhat useful items, compared to other filler.
    
    0 - No junk can be generated as useful items
    
    100 - Maximum Weight"""

    display_name = "Filler Useful Weight"
    range_start = 0
    default = 20
    range_end = 100

class FillerJunkWeight(Range):
    """Decides what percent chance of filler items should be junk items, compared to other filler.
    
    0 - No junk can be generated as filler
    
    100 - Maximum Weight"""

    display_name = "Filler Junk Weight"
    range_start = 0
    default = 50
    range_end = 100

class FillerTrapWeight(Range):
    """Decides what percent chance of filler items should be traps, compared to other filler. 
    In asyncs, traps received while you are not playing will not be received all immediately but will activate randomly while you are playing the game
    
    0 - No traps can be generated as filler
    
    100 - Maximum Weight"""

    display_name = "Filler Trap Weight"
    range_start = 0
    default = 30
    range_end = 100

class NoSpinTrap(Toggle):
    """The spin trap causes the camera to spin around which might make some people nauseous, if you want you can enable this setting to remove it from the pool."""

class SignRandomization(Toggle):
    """There is 1 check per level (not per sign) for reading a sign inside it. If you are generating a solo game and it fails, the logic might be too restrictive; enabling this will ease up the logic a bit since there is usually a sign right next to the start"""

class LevelTickets(Toggle):
    """Generate level tickets for each level, excluding the overworlds and usually course 1. There is logic to account for the scenario of going through a different level to access a level."""

class MoveRandomization(Toggle):
    """Moves are now items and you will need them in order to use mario's moveset. 
    The moves randomized are 3 progressive jumps (single, double, triple), long jumps, backflips, sideflips, wallkicks, dives, ground pounding, kicking, punching, slidekicking, and riding a shell
    You will always start with a random choice of either one of the 3 jumps, long jumps, backflips, or sideflips, since otherwise you can easily run into generation issues. 
    If you put one of those in your starting items, however, you will always start with it."""

class ForceMoveRandomization(Toggle):
    """Moves will be randomized even if the hack you are playing does not have logic for it. Use at your own risk, depending on the hack and your starting jump option it can very likely lead to impossible seeds"""
    visibility = Visibility(0b0101)

class StartingJump(Choice):
    """Decides what jumps you start (or dont start) with.

    Jumps (default) - Start with a random jump (single jump, long jump, sideflip, and backflip), weighted towards single jump
    
    Single Jump - Always start with a single jump
    
    Rollout - Start with either slidekicks or dives to allow you to rollout from the start.

    Nothing - You will not start with a random jump. This may lead to significant generation issues with solo generations, especially with hacks with no levels you can enter without jumping, and if you're playing in a large multiworld, be prepared to do nothing for a long time. 
    Expect logic to be a little unintuitive without jumping.
    """
    option_jumps = 0
    option_single_jump = 1
    option_rollout = 2
    option_nothing = 3
    default = 0

class StartingTickets(Range):
    """If you have level tickets enabled, decides what percent of level tickets are given as starting items. Intended to ease up logic generation, especially in linear games"""
    range_start = 0
    default = 25
    range_end = 100
    

class LogicDifficulty(Choice):
    """Decides what the difficulty of the logic (compared to the hack itself) should be.
    
    Strict - Everything that could be considered the intended requirements will be required. This will require certain items even if its more likely that a casual would skip said items than actually use them to get the star, since the skip is either easier to find or easier to perform than the intended path.
    
    Reasonable - Every skip that a casual could reasonably find in normal gameplay is considered in logic, assuming it is not significantly more difficult than expected for the hack it is in.
    
    Obscure - Skips that may be hard to find on your own but not necessarily difficult to perform, compared to the hack's average difficulty, are considered in logic
    
    Hard - Any skips that are relatively hard to perform (and usually hard to find as a result), compared to the average difficulty of the hack, are considered in logic"""

    option_strict = 0
    option_reasonable = 1
    option_obscure = 2
    option_hard = 3
    default = 1

class LogicGlitches(OptionSet):
    """Decides what common glitches are considered in logic.
    Glitches considered: "Bomb Clips", "BLJs", "Chuckya Clips", "Bomb Walking", "Framewalks"
    Does nothing if logic is on strict (after all, using a glitch is almost certainly unintended)
    If in the rare instance a glitch is actually intended for a certain star in the hack you're playing, it will always be considered in-logic and this option won't matter."""
    valid_keys = ["Bomb Clips", "BLJs", "Chuckya Clips", "Bomb Walking", "Framewalks"]

class MajorSkips(Toggle):
    """If this is enabled, major skips (obviously unintended skips which may unlock one or more stages) will be considered in-logic"""

class HackSpecificOptions(OptionSet):
    """Any options specific to the hack you are playing should be put here. Check the wiki page (https://wiki.dnvic.com) for the hack you are playing to see which options exist in the hack you are playing"""

class StarBundles(Range):
    """Decides what percent of stars will be converted into star bundles, worth 2 stars each. 
    
    If there are more items than locations (from move/tickets) the generator will automatically convert Stars to Star Bundles to lower the number of items, regardless of this setting, but if you want there to be more filler items/traps this option will free up item slots for junk.
    Also, if there is an odd number of stars in the hack, it will still create 1 normal star, even at 100% star bundles, so that the star count remains the same."""
    range_start = 0
    default = 0
    range_end = 100

class RingLink(Choice):
    """
    Whether your coin counter is linked to other players.

    On - Normal RingLink. You only send coins to other players and can receive any amount of coins from other players.

    Hard RingLink (Not recommended) - Same as on, but allows the client to send negative rings upon leaving a level.
    """
    display_name = "Ring Link"
    option_off = 0
    option_on = 1
    option_hard_ringlink = 2


option_groups = [
    OptionGroup("Main Options", [
        JsonFile,
        ProgressiveKeys
    ]),
    OptionGroup("Extra Randomization", [
        TrollStars,
        SignRandomization,
        RandomizeMoat,
        LevelTickets,
        MoveRandomization
    ]),
    OptionGroup("Item Settings", [
        StartingJump,
        StartingTickets,
        StarBundles,
        FillerUsefulWeight,
        FillerJunkWeight,
        FillerTrapWeight,
        NoSpinTrap
    ]),
    OptionGroup("Logic Options", [
        LogicDifficulty,
        LogicGlitches,
        MajorSkips,
        HackSpecificOptions,
        ForceMoveRandomization
    ]),
    OptionGroup("Misc Options", [
        DeathLink,
        RingLink
    ])
]
@dataclass
class SM64HackOptions(PerGameCommonOptions):
    json_file: JsonFile
    progressive_keys: ProgressiveKeys
    troll_stars: TrollStars
    sign_randomization: SignRandomization
    randomize_moat: RandomizeMoat
    level_tickets: LevelTickets
    starting_tickets: StartingTickets
    star_bundles: StarBundles
    move_randomization: MoveRandomization
    force_move_randomization: ForceMoveRandomization
    starting_jump: StartingJump
    filler_trap_weight: FillerTrapWeight
    filler_junk_weight: FillerJunkWeight
    filler_useful_weight: FillerUsefulWeight
    no_spin_trap: NoSpinTrap
    logic_difficulty: LogicDifficulty
    glitches_in_logic: LogicGlitches
    major_skips: MajorSkips
    hack_specific_options: HackSpecificOptions
    death_link: DeathLink
    start_inventory_from_pool: StartInventoryPool
    ring_link: RingLink

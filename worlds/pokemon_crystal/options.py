import random
from collections.abc import Hashable
from dataclasses import dataclass
from typing import Type, override, Any

from schema import Schema, And, Optional, Use, Or, Regex

from BaseClasses import PlandoOptions, ItemClassification
from Options import Toggle, Choice, DefaultOnToggle, Range, PerGameCommonOptions, NamedRange, OptionSet, \
    StartInventoryPool, OptionDict, Visibility, DeathLink, OptionGroup, OptionList, FreeText, OptionError, \
    OptionCounter, PlandoConnections, TextChoice
from Utils import is_iterable_except_str
from .data import data, MapPalette, MiscOption, friendly_entrance_name, FRIENDLY_CONNECTION_NAMES, \
    OUTDOOR_WARP_MAP_FRIENDLY_NAMES, OUTDOOR_ENVIRONMENTS
from .maps import FLASH_MAP_GROUPS
from .pokemon_data import LEGENDARY_POKEMON, NON_LEGENDARY_POKEMON
from .entrance_rando import ENTRANCE_CATEGORIES
from ..AutoWorld import World


class EnhancedOptionSet(OptionSet):

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.valid_keys:
            keys = list(cls.valid_keys)
            for meta in ("_All", "_Random"):
                if meta not in keys:
                    keys.append(meta)
            cls.valid_keys = keys

    def __init__(self, value):
        if isinstance(value, list):
            value = [x.title() if x.title() in ('_All', '_Random') else x for x in value]

            if "_All" in value:
                value = [k for k in self.valid_keys if not k.startswith("_")]

            if "_Random" in value:
                value = [v for v in value if v != "_Random"]
                value += [k for k in sorted(self.valid_keys) if not k.startswith("_") and random.getrandbits(1)]

        super().__init__(set(value))


class PokemonSet(OptionSet):
    def __init_subclass__(cls, **kwargs):
        cls.__doc__ = cls.__doc__ + (
            "You can use _Legendaries or _Non-Legendaries as shortcuts, "
            "or _<Type> (e.g. _Fire, _Water) to include all Pokemon of that type."
        )

    type_shortcuts = sorted(f"_{"Psychic" if t == "PSYCHIC_TYPE" else t.title()}" for t in data.types)

    valid_keys = sorted(pokemon.friendly_name for pokemon in data.pokemon.values()) + [
        "_Legendaries", "_Non-Legendaries"
    ] + type_shortcuts

    def get_ids(self, world) -> set[str]:
        if not self.value: return set()

        pokemon = set(self.value)
        if "_Legendaries" in pokemon:
            pokemon.discard("_Legendaries")
            pokemon.update(LEGENDARY_POKEMON)
        if "_Non-Legendaries" in pokemon:
            pokemon.discard("_Non-Legendaries")
            pokemon.update(NON_LEGENDARY_POKEMON)
        for type_shortcut in self.type_shortcuts:
            if type_shortcut in pokemon:
                pokemon.discard(type_shortcut)
                type_name = type_shortcut[1:].upper()  # strip leading _, match internal type key casing
                if type_name == "PSYCHIC":
                    type_name = "PSYCHIC_TYPE"
                pokemon.update(
                    pkmn_data.friendly_name
                    for pkmn_data in world.generated_pokemon.values()
                    if type_name in pkmn_data.types
                )

        pokemon_ids = {pokemon_id for pokemon_id, pokemon_data in world.generated_pokemon.items() if
                       pokemon_data.friendly_name in pokemon}

        return pokemon_ids


class WeightedOptionDict(OptionDict):
    valid_values: set[str]

    def __init__(self, value):
        rolled = {}
        for k, v in value.items():
            if isinstance(v, dict):
                invalid = set(v.keys()) - self.valid_values
                if invalid:
                    raise OptionError(
                        f"Found unexpected value(s) {', '.join(sorted(invalid))} in {self.display_name}. "
                        f"Allowed values: {self.valid_values}."
                    )
                rolled[k] = random.choices(list(v.keys()), weights=list(v.values()))[0]
            else:
                rolled[k] = v
        super().__init__(rolled)

    def verify_keys(self) -> None:
        extra_keys = {str(k) for k in self.value.keys()} - self._valid_keys
        if extra_keys:
            raise OptionError(
                f"Found unexpected key {', '.join(extra_keys)} in {self.display_name}. "
                f"Allowed keys: {self._valid_keys}."
            )
        extra_values = set(self.value.values()) - self.valid_values
        if extra_values:
            raise OptionError(
                f"Found unexpected value {', '.join(extra_values)} in {self.display_name}. "
                f"Allowed values: {self.valid_values}."
            )


class Goal(EnhancedOptionSet):
    """
    Select one or more goals. All selected goals must be completed to win.

    - Elite Four: Defeat the Champion and enter the Hall of Fame
    - Red: Defeat Red in Mt. Silver
    - Diploma: Catch all logically available Pokemon and receive the diploma in Celadon City
    - Rival: Win all possible rival battles
    - Defeat Team Rocket: Vanquish Team Rocket in Slowpoke Well, Mahogany Town, Radio Tower and defeat the grunt
       on Route 24 (if Kanto is accessible)
    - Unown Hunt: Catch all 26 Unown forms that are attached to signs across the region(s) and show the completed Unown dex
       to the scientist in Ruins of Alph. In order to encounter the Unown you'll need to solve their corresponding tile puzzle.
       Each puzzle requires 16 pieces which must be found first.
    - Battle Tower: Beat all 10 Battle Tower tiers (7 trainers each).
    """
    display_name = "Goal"

    ELITE_FOUR = "Elite Four"
    RED = "Red"
    DIPLOMA = "Diploma"
    RIVAL = "Rival"
    DEFEAT_TEAM_ROCKET = "Defeat Team Rocket"
    UNOWN_HUNT = "Unown Hunt"
    BATTLE_TOWER = "Battle Tower"

    default = [ELITE_FOUR]
    valid_keys = [ELITE_FOUR, RED, DIPLOMA, RIVAL, DEFEAT_TEAM_ROCKET, UNOWN_HUNT, BATTLE_TOWER]


class VanillaEventChains(EnhancedOptionSet):
    """
    Restores the selected vanilla event chains instead of the streamlined Archipelago behaviour.

    Misty: Misty is not in her gym at the start. You must meet the Power Plant manager, witness the Rocket
     flee the Cerulean Gym, then find Misty on her date on Route 25 before she returns to her gym. The Cerulean Gym
     Machine Part cannot be picked up until the Power Plant manager step.

    Clair: Clair refuses to give you the Rising Badge until you prove your worth to the Elders in the
     Dragon's Den Shrine, which requires Whirlpool to access.

    Jasmine: the Cianwood Pharmacy only hands over the SecretPotion after you've visited Jasmine tending
     her sick Amphy atop the Olivine Lighthouse. (Curing Amphy to bring Jasmine back to her gym is always
     required; this just gates the SecretPotion behind meeting her first.)

    Copycat: the guy in the Vermilion Pokemon Fan Club only gives you the Lost Item after you've spoken to
     the Copycat in Saffron and learned she lost it.

    - _All includes all event chains
    - _Random has a 50% chance to include each event chain that is not already included
    """
    display_name = "Vanilla Event Chains"

    MISTY = "Misty"
    CLAIR = "Clair"
    JASMINE = "Jasmine"
    COPYCAT = "Copycat"

    valid_keys = [MISTY, CLAIR, JASMINE, COPYCAT]


class JohtoOnly(Choice):
    """
    Excludes Kanto and disables Kanto access. Include Silver Cave keeps Silver Cave and Mt. Silver available.

    - The Diploma goal is removed; the Red goal is also removed unless Silver Cave is included
      (Elite Four is used if no goals remain)
    - Gym count requirements are capped at 8 (7 for Radio Tower)
    - Badge count requirements are capped at 8 (7 for Radio Tower and Route 44) unless badges are completely
      random, in which case extra Kanto badges are added to the pool
    """
    display_name = "Johto Only"
    default = 0
    option_off = 0
    option_on = 1
    option_include_silver_cave = 2


class VictoryRoadRequirement(Choice):
    """
    Sets the requirement to pass the Victory Road badge check
    """
    display_name = "Victory Road Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1
    option_johto_badges = 2


class VictoryRoadCount(Range):
    """
    Sets the number of badges/gyms required to pass the Victory Road badge check

    This will be limited to 8 if the requirement is Johto Badges
    """
    display_name = "Victory Road Count"
    default = 8
    range_start = 0
    range_end = 16


class EliteFourRequirement(Choice):
    """
    Sets the requirement go between Indigo Pokecenter 1F and Will's room
    """
    display_name = "Elite Four Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1
    option_johto_badges = 2


class EliteFourCount(Range):
    """
    Sets the number of badges/gyms required to go between Indigo Pokecenter 1F and Will's room

    This will be limited to 8 if the requirement is Johto Badges
    """
    display_name = "Elite Four Count"
    default = 8
    range_start = 0
    range_end = 16


class RedRequirement(Choice):
    """
    Sets the requirement to battle Red
    """
    display_name = "Red Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class RedCount(Range):
    """
    Number of badges/gyms required to battle Red
    """
    display_name = "Red Count"
    default = 16
    range_start = 0
    range_end = 16


class MtSilverRequirement(Choice):
    """
    Sets the requirement to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class MtSilverCount(Range):
    """
    Number of badges/gyms required to access Mt. Silver and Silver Cave
    """
    display_name = "Mt. Silver Count"
    default = 16
    range_start = 0
    range_end = 16


class RadioTowerRequirement(Choice):
    """
    Sets the requirement for Team Rocket to take over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class RadioTowerCount(Range):
    """
    Number of badges/gyms at which Team Rocket takes over the Goldenrod Radio Tower
    """
    display_name = "Radio Tower Count"
    default = 7
    range_start = 0
    range_end = 16


class Route44AccessRequirement(Choice):
    """
    Sets the requirement to pass between Mahogany Town and Route 44
    """
    display_name = "Route 44 Access Requirement"
    default = 0
    option_badges = 0
    option_gyms = 1


class Route44AccessCount(Range):
    """
    Sets the number of badges/gyms required to pass between Mahogany Town and Route 44
    """
    display_name = "Route 44 Access Count"
    default = 7
    range_start = 0
    range_end = 16


class MagnetTrainAccess(Choice):
    """
    Sets the requirement to ride the Magnet Train

    - Pass requires only the Pass
    - Pass and Power requires the Pass and restoring power to Kanto by returning the Machine Part
    """
    display_name = "Magnet Train Access"
    default = 0
    option_pass = 0
    option_pass_and_power = 1


class RandomizeStartingTown(Toggle):
    """
    Randomly chooses a town to start in.
    Any Pokemon Center except Indigo Plateau, Cinnabar Island and Silver Cave can be chosen. The Pokemon Centers at Union Cave and Rock Tunnel can also be chosen.
    Lake of Rage will start you at its flypoint and cannot be chosen if gate entrances are randomized. Pallet Town will start you in front of Red's House.
    When Pokemon Center entrances are randomized, the Pokemon Centers of Cherrygrove City, Viridian City, and Mahogany Town will be vanilla when the starting town is New Bark Town, Pallet Town, or Lake of Rage respectively.

    Other settings may additionally restrict which Pokemon Centers can be chosen.

    WARNING: Some starting towns without level scaling may produce difficult starts.
    """
    display_name = "Randomize Starting Town"


class StartingTownBlocklist(OptionSet):
    """
    Specify places which cannot be chosen as a starting town. If you block every valid option, this list will do nothing.
    Indigo Plateau, Cinnabar Island and Silver Cave cannot be chosen as starting towns and are not valid options.
    "_Johto" and "_Kanto" are shortcuts for all Johto and Kanto towns respectively.
    "Union Cave" and "Rock Tunnel" are valid starting towns.
    """
    display_name = "Starting Town Blocklist"
    valid_keys = sorted(town.name for town in data.starting_towns) + ["_Johto", "_Kanto"]


class Route23Restored(Toggle):
    """
    Inserts a restored Route 23 (the cut Kanto area) between Victory Road's
    southern exit and Victory Road Gate. Adds new wild encounters, a berry
    tree, and two hidden items.
    """
    display_name = "Route 23 Restored"


class FloodedMine(Toggle):
    """
    Adds the Flooded Mine, a small cave connecting Cherrygrove City and
    Route 32, with new wild encounters, three hidden items, and a TM.
    """
    display_name = "Flooded Mine"


class RandomizeBadges(Choice):
    """
    Shuffles gym badge locations into the pool
    - Vanilla: Does not randomize gym badges
    - Shuffle: Randomizes gym badges between gym leaders
    - Completely Random: Randomizes badges with all other items
    """
    display_name = "Randomize Badges"
    default = 2
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class RandomizeHiddenItems(Toggle):
    """
    Shuffles hidden item locations into the pool
    """
    display_name = "Randomize Hidden Items"


class BattleTowerSanity(Choice):
    """
    Adds locations in the Battle Tower.

    - off: no Battle Tower locations.
    - tiers: 10 locations, one for completing each tier.
    - tiers_and_trainers: the 10 tier locations plus one location per Battle Tower trainer (70 extra).

    Tier N is logically gated behind access to N of the following: gyms, E4 and Red. Trainer locations share the gate
    of whichever tier they are shuffled into for the seed.

    WARNING: The Battle Tower is legit. Your team will be levelled down to match your tier, if needed. You cannot
    use items from your bag, held items must all be different and the trainers have the best possible AI. Bringing in Pokemon with >= 600 BST requires the Battle Tower
    Uber Pass, which will be shuffled into the item pool.
    """
    display_name = "Battle Tower Sanity"
    option_off = 0
    option_tiers = 1
    option_tiers_and_trainers = 2
    default = 0


class BattleTowerProgressiveTierUnlocks(Toggle):
    """
    Locks Battle Tower tiers behind progressive unlock items.
    Each item received unlocks the next tier in order; without them, all tiers
    are immediately accessible. Only takes effect when battle_tower_sanity is on
    or the Battle Tower goal is selected.
    """
    display_name = "Battle Tower Progressive Tier Unlocks"


class RequireItemfinder(Choice):
    """
    Hidden items require Itemfinder in logic

    - Not Required: Hidden items do not require the Itemfinder at all
    - Logically Required: Hidden items will expect you to have Itemfinder for logic but can be picked up without it
    - Hard Required: Hidden items cannot be picked up without the Itemfinder
    """
    display_name = "Require Itemfinder"
    default = 1
    option_not_required = 0
    option_logically_required = 1
    option_hard_required = 2


class ItemPoolFill(Choice):
    """
    Changes the weight of non-progression items in the pool.

    - Vanilla: weighted similarly to vanilla.
    - Balanced: all weighted equally.
    - Youngster: weighted to reflect a young trainer (weak items).
    - Cooltrainer: weighted to reflect a cooltrainer (strong items).
    - Shuckle: weighted to reflect a Shuckle (🐢).
    """
    display_name = "Item Pool Fill"
    default = 0
    option_vanilla = 0
    option_balanced = 1
    option_youngster = 2
    option_cooltrainer = 3
    option_shuckle = 4


class AddMissingUsefulItems(Toggle):
    """
    Adds useful items which are unobtainable to the pool, these replace filler
    """
    display_name = "Add Missing Useful Items"


class Route32Condition(Choice):
    """
    Sets the condition required to pass between the north and south parts of Route 32
    - Egg from aide: Collect the Egg from the aide in the Violet City Pokemon Center after beating Falkner
    - Any badge: Obtain any badge
    - Any gym: Beat any gym
    - Zephyr Badge: Obtain the Zephyr Badge
    - None: No requirement
    """
    display_name = "Route 32 Access Condition"
    default = 0
    option_egg_from_aide = 0
    option_any_badge = 1
    option_any_gym = 2
    option_zephyr_badge = 3
    option_none = 4


class Route22AccessRequirement(Choice):
    """
    Sets the requirement to pass between Victory Road gate and Kanto
    - Wake Snorlax: Wake the Snorlax outside of Diglett's Cave
    - Badges: Requires the number of badges specified by route_22_access_count
    - Gyms: Requires beating the number of gyms specified by route_22_access_count
    - Become Champion: Defeat Lance and enter the Hall of Fame

    This setting does nothing if Johto Only is enabled
    """
    display_name = "Route 22 Access Requirement"
    default = 0
    option_wake_snorlax = 0
    option_badges = 1
    option_gyms = 2
    option_become_champion = 3


class Route22AccessCount(Range):
    """
    Sets the number of badges/gyms required to pass between Victory Road gate and Kanto
    Only applies if Route 22 Access Requirement is set to badges or gyms
    """
    display_name = "Route 22 Access Count"
    default = 8
    range_start = 0
    range_end = 16


class DarkAreas(EnhancedOptionSet):
    """
    Sets which areas are dark until Flash is used

    - _All includes all areas
    - _Random has a 50% chance to include each area that is not already included
    """
    display_name = "Dark Areas"
    default = sorted(area for area, maps in FLASH_MAP_GROUPS.items() if data.maps[maps[0]].palette is MapPalette.Dark)
    valid_keys = sorted(area for area in FLASH_MAP_GROUPS.keys())

    __doc__ = __doc__ + "\nAllowed areas: " + ", ".join(valid_keys)


class RedGyaradosAccess(Choice):
    """
    Sets the access requirement for the red Gyarados
    - Vanilla requires Surf
    - Whirlpool requires Surf and Whirlpool
    - Shore requires nothing
    """
    display_name = "Red Gyarados Access"
    default = 0
    option_vanilla = 0
    option_whirlpool = 1
    option_shore = 2


class Route2Access(Choice):
    """
    Sets the roadblock for moving between the west of Route 2 and Diglett's cave
    - Vanilla: Cut is required
    - Ledge: A ledge is added north of Diglett's cave allowing east -> west access without Cut
    - Open: No requirement
    """
    display_name = "Route 2 Access"
    default = 1
    option_vanilla = 0
    option_ledge = 1
    option_open = 2


class Route3Access(Choice):
    """
    Sets the roadblock for moving between Pewter City and Route 3
    - Vanilla: No requirement
    - Boulder Badge: The Boulder Badge is required to pass
    """
    display_name = "Route 3 Access"
    default = 0
    option_vanilla = 0
    option_boulder_badge = 1


class BlackthornDarkCaveAccess(Choice):
    """
    Sets the roadblock for travelling from Route 31 to Blackthorn City through Dark Cave
    - Vanilla: Traversal is not possible
    - Waterfall: A waterfall is added to the Violet side of Dark Cave and a ledge is removed on the Blackthorn side,
    allowing passage with Flash, Surf and Waterfall
    """
    display_name = "Blackthorn Dark Cave Access"
    default = 0
    option_vanilla = 0
    option_waterfall = 1


class NationalParkAccess(Choice):
    """
    Sets the requirement to enter National Park
    - Vanilla: No requirement
    - Bicycle: The Bicycle is required
    """
    display_name = "National Park Access"
    default = 0
    option_vanilla = 0
    option_bicycle = 1


class Route42Access(Choice):
    """
    Sets the requirement to traverse the water on Route 42
    - Vanilla: Route 42 can be traversed with Surf
    - Whirlpool: Access to Central Route 42 is blocked by a whirlpool
    - Blocked: Access to Central Route 42 is completely blocked, requiring going through Mount Mortar instead.
    Mount Mortar 1F gets an extra map connection between the Inside and Central Outside
    - Whirlpool Open Mortar: Route 42 has whirlpools and Mount Mortar 1F has the extra map connection.
    """
    display_name = "Route 42 Access"
    default = 0
    option_vanilla = 0
    option_whirlpool = 1
    option_blocked = 2
    option_whirlpool_open_mortar = 3

    @property
    def requires_whirlpool(self) -> bool:
        """Central Route 42 is gated by a whirlpool."""
        return self.value in (self.option_whirlpool, self.option_whirlpool_open_mortar)

    @property
    def opens_mortar_connection(self) -> bool:
        """Mount Mortar 1F gets the extra Inside <-> Central Outside connection."""
        return self.value in (self.option_blocked, self.option_whirlpool_open_mortar)


class MountMortarAccess(Choice):
    """
    Sets the requirement to pass through Mount Mortar east <> west
    - Vanilla: No requirement
    - Rock Smash: Rock Smash is required
    """
    display_name = "Mount Mortar Access"
    default = 0
    option_vanilla = 0
    option_rock_smash = 1


class VictoryRoadStrength(Toggle):
    """
    If enabled, Strength is required to pass through Victory Road to Indigo Plateau.
    """
    display_name = "Victory Road Strength"


class Route12Access(Choice):
    """
    Sets the requirement to pass between the north and south parts of Route 12
    - Vanilla: No requirement
    - Weird Tree: Requires Squirtbottle, but can be bypassed with Surf
    - Weird Tree Surf Block: Requires Squirtbottle and adds boulders to prevent surfing around

    The roadblock is north of the path to Route 11
    """
    display_name = "Route 12 Access"
    default = 0
    option_vanilla = 0
    option_weird_tree = 1
    option_weird_tree_surf_block = 2


class SSAquaAccess(Choice):
    """
    Sets the requirement to sail on the S.S. Aqua
    - Vanilla: S.S. Ticket is required
    - Lighthouse and Ticket: Healing Amphy in the Olivine lighthouse and the S.S Ticket are required
    """
    display_name = "S.S. Aqua Access"
    default = 0
    option_vanilla = 0
    option_lighthouse_and_ticket = 1


class Route30Access(Choice):
    """
    Sets the requirement to end the Pokemon battle on Route 30
    - Mr. Pokemon: Visit Mr. Pokemon in his house
    - Mystery Egg: Return the Mystery Egg to Professor Elm
    """
    display_name = "Route 30 Access"
    default = 0
    option_mr_pokemon = 0
    option_mystery_egg = 1


class SouthKantoAccess(Choice):
    """
    Sets where the landslide that is normally south of Fuchsia City is located

    Both can only be used if the condition is power restored.
    """
    display_name = "South Kanto Access"
    default = 0
    option_route_19 = 0
    option_route_21 = 1
    option_neither = 2
    option_both = 3

    @property
    def blocks_route_19(self) -> bool:
        return self.value in (self.option_route_19, self.option_both)

    @property
    def blocks_route_21(self) -> bool:
        return self.value in (self.option_route_21, self.option_both)


class SouthKantoCondition(Choice):
    """
    Sets the condition which clears the south Kanto landslide
    """
    display_name = "South Kanto Condition"
    default = 0
    option_enter_south_kanto = 0
    option_power_restored = 1


class Route30Battle(Choice):
    """
    Sets which directions the battle on Route 30 blocks
    """
    display_name = "Route 30 Battle"
    default = 0
    option_blocks_northbound = 0
    option_blocks_both = 1


class JohtoTrainersanity(NamedRange):
    """
    Adds checks for defeating Johto trainers.

    You can turn trainers that have checks grayscale by setting the "trainersanity_indication" in-game option.

    Trainers are no longer missable. Each trainer will add a random filler item into the pool.
    """
    display_name = "Johto Trainersanity"
    default = 0
    range_start = 0
    range_end = len([loc_id for loc_id, loc_data in data.locations.items() if
                     "Trainersanity" in loc_data.tags and "Johto" in loc_data.tags])
    special_range_names = {
        "none": 0,
        "full": range_end
    }


class KantoTrainersanity(NamedRange):
    """
    Adds checks for defeating Kanto trainers.

    You can turn trainers that have checks grayscale by setting the "trainersanity_indication" in-game option.

    Trainers are no longer missable. Each trainer will add a random filler item into the pool.
    """
    display_name = "Kanto Trainersanity"
    default = 0
    range_start = 0
    range_end = len([loc_id for loc_id, loc_data in data.locations.items() if
                     "Trainersanity" in loc_data.tags and "Johto" not in loc_data.tags])
    special_range_names = {
        "none": 0,
        "full": range_end
    }


class KindaEarlySurf(Toggle):
    """
    Adds Surf as a logical requirement for: the Magnet Train, going east of Mahogany,
    fighting Jasmine, the Rocket takeover of the Radio Tower, entering Tin Tower,
    waking Snorlax, and entering the Kanto Gyms. Forced off if Randomize Starting Town,
    Johto Only, or Entrance Randomization is enabled.
    """
    display_name = "Kinda Early Surf"
    visibility = Visibility.none


class Rematchsanity(Toggle):
    """
    Adds the phone-trainer rematch fights as checks.

    Rematches unlock in order as you hit story milestones (visiting Goldenrod / Olivine /
    etc., clearing the Radio Tower, beating the Elite Four, restoring power to Kanto).
    All rematches need the Pokegear and a Phone Card.

    Picnicker Tiffany's rematches only count if Randomize Pokemon Requests is also on.

    Joey's HP Up is given after his last rematch.
    """
    display_name = "Rematchsanity"


class Dexsanity(NamedRange):
    """
    Adds checks for catching Pokemon
    Pokemon that cannot be logically obtained will never be included
    """
    display_name = "Dexsanity"
    default = 0
    range_start = 0
    range_end = 251
    special_range_names = {
        "none": default,
        "full": range_end
    }


class Dexcountsanity(NamedRange):
    """
    Adds checks for completing Pokedex milestones
    This setting specifies number of caught Pokemon on which you'll get your last check
    """
    display_name = "Dexcountsanity"
    default = 0
    range_start = 0
    range_end = 251
    special_range_names = {
        "none": default,
        "full": range_end
    }


class DexcountsanityStep(Range):
    """
    If Dexcountsanity is enabled, specifies the step interval at which your checks are placed.
    For example, if you have Dexcountsanity 50 and Dexcountsanity Step 10, you will have checks at
    10, 20, 30, 40 and 50 total Pokemon caught.
    """
    display_name = "Dexcountsanity Step"
    default = 1
    range_start = 1
    range_end = 251


class DexcountsanityLeniency(Range):
    """
    If Dexcountsanity is enabled, specifies the logic leniency for checks.
    For example, if you set Dexcountsanity Leniency to 5 and have a Dexcountsanity check at 10, you will not be
    logically required to obtain this check until you can obtain 15 Pokemon

    Checks that would go over the total number of logically available Pokemon will be clamped to that limit
    """
    display_name = "Dexcountsanity Leniency"
    default = 0
    range_start = 0
    range_end = 251


class DexsanityStarters(Choice):
    """
    Controls how Dexsanity treats starter Pokemon

    - Allow: Starter Pokemon will be allowed as Dexsanity checks
    - Block: Starter Pokemon will not be allowed as Dexsanity Checks
    - Available Early: Starter Pokemon will all be obtainable in the wild immediately, unless there is nowhere to obtain
    wild Pokemon immediately
    """
    display_name = "Dexsanity Starters"
    default = 0
    option_allow = 0
    option_block = 1
    option_available_early = 2


class WildEncounterMethodsRequired(EnhancedOptionSet):
    """
    Sets which wild encounter types may be logically required

    - Land: Pokemon encountered in grass and caves
    - Surfing: Pokemon encountered while surfing
    - Fishing: Pokemon encountered with any rod
    - Headbutt: Pokemon encountered by headbutting trees
    - Rock Smash: Pokemon encountered by smashing rocks
    - Bug Catching Contest: Pokemon encountered in the National Park contest
    - Swarm: Pokemon encountered during a swarm

    _Random has a 50% chance to include types which are not already included
    _All will include all types

    Swarm encounters require Randomize Phone Calls to be enabled.
    Roamers are NEVER in logic.
    """
    display_name = "Wild Encounter Methods Required"

    LAND = "Land"
    SURFING = "Surfing"
    FISHING = "Fishing"
    HEADBUTT = "Headbutt"
    ROCK_SMASH = "Rock Smash"
    BUG_CATCHING_CONTEST = "Bug Catching Contest"
    SWARM = "Swarm"

    valid_keys = [LAND, SURFING, FISHING, HEADBUTT, ROCK_SMASH, BUG_CATCHING_CONTEST, SWARM]
    default = [LAND, SURFING, FISHING, HEADBUTT, ROCK_SMASH, BUG_CATCHING_CONTEST]


class EnforceWildEncounterMethodsLogic(Toggle):
    """
    Sets whether the game will prevent capture of Pokemon found through disabled wild encounter methods
    Statics, roamers and contest encounters can always be caught

    You can always re-catch Pokemon you have already caught
    """
    display_name = "Enforce Wild Encounter Methods Logic"


class EvolutionMethodsRequired(EnhancedOptionSet):
    """
    Sets which types of evolutions may be logically required

    _Random has a 50% chance to include types which are not already included
    _All will include all types
    """
    display_name = "Evolution Methods Required"

    LEVEL = "Level"
    LEVEL_TYROGUE = "Level and Stat"
    USE_ITEM = "Use Item"
    HELD_ITEM = "Held Item"
    HAPPINESS = "Happiness"

    valid_keys = [LEVEL, LEVEL_TYROGUE, USE_ITEM, HELD_ITEM, HAPPINESS]
    default = [LEVEL, LEVEL_TYROGUE, USE_ITEM, HELD_ITEM, HAPPINESS]


class StaticPokemonRequired(DefaultOnToggle):
    """
    Sets whether static Pokemon may be logically required
    """
    display_name = "Static Pokemon Required"


class TradesRequired(Toggle):
    """
    Specifies if in-game trades may be logically required
    """
    display_name = "Trades Required"


class RandomizeLuckyNumberShow(Toggle):
    """
    Adds the Radio Tower Lucky Number Show as three locations.

    Three in-game trades are chosen at random; obtaining each traded Pokemon wins the
    matching prize (1st/2nd/3rd).
    """
    display_name = "Randomize Lucky Number Show"


class BreedingMethodsRequired(Choice):
    """
    Specifies which breeding methods may be logically required.
    """
    display_name = "Breeding Method Required"
    default = 1
    option_none = 0
    option_with_ditto = 1
    option_any = 2


class EnforceBreedingMethodsLogic(Toggle):
    """
    Sets whether the game will prevent the breeding of Pokemon that do not match the selected breeding logic
    """
    display_name = "Enforce Breeding Methods Logic"


class EvolutionGymLevels(Range):
    """
    Sets how many levels each accessible gym puts into logic for level (and Tyrogue) evolutions

    For example, if you set this to 4 and have access to 5 gyms, evolutions up to level 20 would be in logic.

    If Johto only is enabled the minimum for this setting is 8.
    """
    display_name = "Evolution Gym Levels"
    default = 8
    range_start = 4
    range_end = 69


class Shopsanity(EnhancedOptionSet):
    """
    Adds shop purchases as locations, items in shops are added to the item pool
    - Johto Marts: Adds Johto Poke Marts, including the Goldenrod Dept. Store.
    - Kanto Marts: Adds Kanto Poke Marts, including the Celadon Dept. Store.
    - Blue Card: Adds the Blue Card prize shop, accessing this shop requires the Blue Card and buying items requires
    points. Five Blue Card Points are added to the item pool. Points are not spent when purchasing.
    - Game Corners: The Game Corner TM shops are added.
    - Apricorns: Kurt's Apricorn Ball shop is added, each slot requires a different Apricorn. Apricorns are progression.
    - _All: Includes all valid options.
    - _Random: Each option that is not included has a 50% chance to be additionally included.

    IMPORTANT NOTE: There is a non-randomized shop on Pokecenter 2F, you can always buy Poke Balls and Escape Ropes there.
    """
    display_name = "Shopsanity"
    default = []

    JOHTO_MARTS = "Johto Marts"
    KANTO_MARTS = "Kanto Marts"
    BLUE_CARD = "Blue Card"
    APRICORNS = "Apricorns"
    GAME_CORNERS = "Game Corners"

    valid_keys = [JOHTO_MARTS, KANTO_MARTS, BLUE_CARD, APRICORNS, GAME_CORNERS]


class ShopsanityPrices(Choice):
    """
    Sets how shop item prices are determined when Shopsanity is enabled
    - Vanilla: Shop prices are unchanged
    - Item Price: Shop prices are determined by the value of the item being sold
    - Spheres: Shop prices are determined by sphere access
    - Classification: Shop prices are determined by item classifications (Progression, Useful, Filler/Trap)
    - Spheres and Classifications: Shop prices are determined by both sphere access and item classifications
    - Completely Random: Shop prices will be completely random
    """
    display_name = "Shopsanity Prices"
    default = 0
    option_vanilla = 0
    option_item_price = 1
    option_spheres = 2
    option_classification = 3
    option_spheres_and_classification = 4
    option_completely_random = 5


class MinimumShopsanityPrice(Range):
    """
    Sets the minimum cost of shop items when Shopsanity is enabled
    """
    display_name = "Minimum Shopsanity Price"
    default = 100
    range_start = 0
    range_end = 10000


class MaximumShopsanityPrice(Range):
    """
    Sets the maximum cost of shop items when Shopsanity is enabled
    """
    display_name = "Maximum Shopsanity Price"
    default = 3000
    range_start = 0
    range_end = 10000


class ProvideShopHints(Choice):
    """
    Sends out hints when a randomized shop is accessed
    """
    display_name = "Provide Shop Hints"
    default = 0
    option_off = 0
    option_progression = 1
    option_progression_and_useful = 2
    option_all = 3


class ShopsanityRestrictRareCandies(Toggle):
    """
    Makes Rare Candies in shops only purchasable once
    """
    display_name = "Shopsanity Restrict Rare Candies"


class ShopsanityXItems(Choice):
    """
    Determines how Shopsanity treats X Items
    - Anywhere: X Items will be shuffled into the multiworld pool
    - Any Shop: At least one of each X Item will be available for purchase in a local shop

    NOTE: You cannot purchase any shop item repeatedly when Remote Items is active
    """
    display_name = "Shopsanity X Items"
    default = 0
    option_anywhere = 0
    option_any_shop = 1


class RandomizePokegear(Toggle):
    """
    Shuffles the Pokegear and cards into the pool
    """
    display_name = "Randomize Pokegear"


class RandomizeBerryTrees(Toggle):
    """
    Shuffles berry tree locations into the pool
    """
    display_name = "Randomize Berry Trees"


class RandomizePokedex(Choice):
    """
    Sets whether the Pokedex is shuffled into the pool

    The Pokedex is required for Dexsanity, Dexcountsanity, trades and Pokemon request locations.
    """
    display_name = "Randomize Pokedex"
    default = 0
    option_vanilla = 0
    option_start_with = 1
    option_randomize = 2


class RandomizePokemonRequests(Choice):
    """
    Shuffles the items given by Bill's Grandpa after showing him specific Pokemon into the pool, as well as the reward
    for showing a Magikarp to the fisher in the house at Lake of Rage

    Optionally also randomizes the requested Pokemon, except the Magikarp

    Trainers which need you to show them a Pokemon to get their phone number require both this option and Randomize Phone Call Items to be enabled.
    """
    display_name = "Randomize Pokemon Requests"
    default = 0
    option_off = 0
    option_items = 1
    option_pokemon = 2
    option_items_and_pokemon = 3


class PokemonSourceLogic(EnhancedOptionSet):
    """Base class for options that restrict Pokemon pools by encounter source."""
    LAND = "Land"
    SURFING = "Surfing"
    FISHING = "Fishing"
    HEADBUTT = "Headbutt"
    ROCK_SMASH = "Rock Smash"
    BUG_CATCHING_CONTEST = "Bug Catching Contest"
    SWARM = "Swarm"
    STATICS = "Statics"
    EVOLUTION = "Evolution"
    BREEDING = "Breeding"
    TRADES = "Trades"

    valid_keys = [LAND, SURFING, FISHING, HEADBUTT, ROCK_SMASH, BUG_CATCHING_CONTEST, SWARM, STATICS, EVOLUTION,
                  BREEDING, TRADES]
    default = [LAND, SURFING, FISHING, HEADBUTT, ROCK_SMASH, BUG_CATCHING_CONTEST, SWARM, STATICS, EVOLUTION,
               BREEDING, TRADES]


class PokemonRequestLogic(PokemonSourceLogic):
    """
    Restricts which encounter sources may provide Pokemon for randomized requests and trades
    (Bill's Grandpa, phone call trainers, in-game trades, etc.)

    Only applies when Pokemon requests or trades are randomized.
    Selected sources are further restricted by their own logic settings (e.g. Wild Encounter Methods Required).
    If no Pokemon are available from the selected sources, falls back to the full logically available pool.

    _Random has a 50% chance to include types which are not already included
    _All will include all types
    """
    display_name = "Pokemon Request Logic"


class DexsanityLogic(PokemonSourceLogic):
    """
    Restricts which encounter sources may provide Pokemon for Dexsanity and Dexcountsanity locations.

    Only applies when Dexsanity or Dexcountsanity is enabled.
    Selected sources are further restricted by their own logic settings (e.g. Wild Encounter Methods Required).
    If no Pokemon are available from the selected sources, falls back to the full logically available pool.

    _Random has a 50% chance to include types which are not already included
    _All will include all types
    """
    display_name = "Dexsanity Logic"


class RandomizeFlyUnlocks(Choice):
    """
    Shuffles Fly destination unlocks into the pool
    """
    display_name = "Randomize Fly Unlocks"
    default = 0
    option_off = 0
    option_on = 1
    option_exclude_silver_cave = 2


class RandomizeFlyDestinations(Toggle):
    """
    Randomizes the destinations of the game's flypoints

    If Randomize Fly Unlocks is on "Exclude Silver Cave", Silver Cave / Route 28 are not included and the flypoint remains vanilla.
    """
    display_name = "Randomize Fly Destinations"


_VALID_FLY_DESTINATION_KEYS = sorted(
    friendly_name for conn, friendly_name in FRIENDLY_CONNECTION_NAMES.items()
    if conn in data.entrance_connections and
    data.maps[data.entrance_connections[conn].exit_warps[0].map_name].environment in OUTDOOR_ENVIRONMENTS
) + OUTDOOR_WARP_MAP_FRIENDLY_NAMES


class FlyDestinationBlocklist(OptionSet):
    """
    Prevents a specific warp or map from being selected as a random flypoint.

    You can find a complete list of accepted values at:
    https://github.com/gerbiljames/Archipelago-Crystal/blob/pokecrystal/worlds/pokemon_crystal/docs/fly_plando.md
    """
    display_name = "Fly Destination Blocklist"
    valid_keys = _VALID_FLY_DESTINATION_KEYS
    default = []


class FlyDestinationPlando(WeightedOptionDict):
    """
    Pins one or more fly unlock to a specific warp or map.

    You can find a guide to accepted values and formatting at:
    https://github.com/gerbiljames/Archipelago-Crystal/blob/pokecrystal/worlds/pokemon_crystal/docs/fly_plando.md
    """
    KEY_PREFIX = "Fly Destination "
    display_name = "Fly Destination Plando"
    valid_keys = sorted(f"Fly Destination {i}" for i in range(1, len(data.fly_regions) + 1))
    valid_values = frozenset(_VALID_FLY_DESTINATION_KEYS)
    default = {}


class RandomizeBugCatchingContest(Choice):
    """
    Shuffles the bug catching contest prizes into the pool
    - All: shuffles all prizes into the pool. WARNING: It can be very difficult to get second or third place.
    - Combine second and third: Combines second and third place into a single prize. Shuffles 1st, 2nd+3rd and 4th.
    - Participate: Shuffles a single participation award into the pool, which is obtained by completing the contest.
    """
    display_name = "Randomize Bug Catching Contest"
    default = 0
    option_off = 0
    option_all = 1
    option_combine_second_third = 2
    option_participate = 3


class RandomizePhoneCallItems(Toggle):
    """
    Shuffles gift items from phone trainers into the item pool.

    You need the Pokegear to register phone numbers and the Phone Card to make and receive calls.

    Trainers that ask to see a Pokemon to exchange numbers are only included if Randomize Pokemon Requests is also on.
    """
    display_name = "Randomize Phone Call Items"


class Momsanity(Toggle):
    """
    Adds 10 locations for the items Mom buys you at different money thresholds
    while she's saving your money.

    Logically requires access to Mom, and either giving the Mystery Egg to Elm or
    reaching Route 31 (where Mom calls you). Each item logically requires an
    increasing number of accessible gyms, starting at zero.

    Items that go in your bag will be deposited into the PC. Items which do not go
    in your bag will be in the BANK OF MOM collection box in the PC.

    You can deposit money into the BANK OF MOM by talking to Mom after giving Elm
    the Mystery Egg or her having called you on Route 31.
    """
    display_name = "Momsanity"


class PhoneCallMode(Choice):
    """
    Controls how in-game phone calls work.

    - Vanilla: Calling a trainer only does something useful at the right day and time of day.
      Trainers calling you is random. WARNING: triggering specific phone calls this way can
      require resetting the clock, toggling DST, and a lot of patience.

    - Simple: Calling any trainer always does something useful if available. Trainers calling
      you skip the random roll and offer their action directly.
    """
    display_name = "Phone Call Mode"
    default = 1
    option_vanilla = 0
    option_simple = 1


class RandomizeStarters(Choice):
    """
    Randomizes species of starter Pokemon
    """
    display_name = "Randomize Starters"
    default = 0
    option_vanilla = 0
    option_unevolved_only = 1
    option_completely_random = 2
    option_first_stage_can_evolve = 3
    option_base_stat_mode = 4


class StarterBlocklist(PokemonSet):
    """
    These Pokemon will not be chosen as starter Pokemon
    Does nothing if starter Pokemon are not randomized
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Starter Blocklist"


class StarterBST(NamedRange):
    """
    If you chose Base Stat Mode for your starters, what is the average base stat total you want your available starters to be?
    """
    display_name = "Starter BST Range"
    default = 310
    range_start = 195
    range_end = 680
    special_range_names = {
        "normal_starters": 310
    }


class RandomizeWilds(Choice):
    """
    Randomizes species of wild Pokemon

    - Base Forms: Ensures that at least every Pokemon that cannot be obtained through evolution is available in the wild
    - Evolution Lines: Ensures that at least one Pokemon from each evolutionary line can be obtained in the wild
    - Catch 'em All: Ensures that every Pokemon will be obtainable in the wild

    If this setting is anything other than vanilla, bug catching contest encounters will be completely random.
    """
    display_name = "Randomize Wilds"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_base_forms = 2
    option_evolution_lines = 3
    option_catch_em_all = 4


class SharedWildEncounters(Toggle):
    """
    Requires Wild Match Mode to be None, and has no effect otherwise or if wild Pokemon are not randomized.

    Wild and bug catching contest encounters are generated from the multiworld seed instead of your own slot,
    so every player who enables this will have identical wild encounters.

    For identical tables, players must also match on: Randomize Wilds, Wild Encounter Blocklist, Encounter Grouping,
    Time of Day Encounters, Encounter Slot Distribution and Dexsanity Starters,
    and all must have or lack the Unown Hunt goal.
    Unique Static Pokemon must be disabled, and type shortcuts in the blocklist require Randomize Types to be off.
    Pokemon required by a player's own logic (for example trade requests or Ditto) may still differ.
    """
    display_name = "Shared Wild Encounters"


class WildEncounterBlocklist(PokemonSet):
    """
    These Pokemon will not appear in the wild
    Does nothing if wild Pokemon are not randomized
    Blocklists are best effort, other constraints may cause them to be ignored
    This setting also applies to bug catching contest encounters
    """
    display_name = "Wild Encounter Blocklist"


class WildMatchMode(Choice):
    """
    Controls how randomized wild Pokemon are matched to the vanilla encounters they replace.

    - None: Wild Pokemon are replaced with no regard for the encounter they replace
    - Match Types: Wild Pokemon are replaced with Pokemon of the same type
    - Match Base Stats: Wild Pokemon are replaced with Pokemon of similar base stat totals
    - Match Types and Base Stats: Wild Pokemon are replaced with Pokemon of the same type and similar base stat totals

    This setting has no effect if wild Pokemon are not randomized.
    """
    display_name = "Wild Match Mode"
    default = 0
    option_none = 0
    option_match_types = 1
    option_match_base_stats = 2
    option_match_types_and_base_stats = 3
    alias_vanilla = 0

    @property
    def matches_types(self) -> bool:
        return self.value in (self.option_match_types, self.option_match_types_and_base_stats)

    @property
    def matches_base_stats(self) -> bool:
        return self.value in (self.option_match_base_stats, self.option_match_types_and_base_stats)


class EncounterGrouping(Choice):
    """
    Determines how randomized wild Pokemon are grouped in encounter tables.

    - All Split: Each encounter area will have each slot randomized separately. For example, grass areas will have seven
      randomized encounter slots.
    - One to One: Each encounter area will retain its vanilla slot grouping. For example, if an area has two encounters
      in vanilla, it will be randomized as two slots.
    - One per Method: Each encounter method on a route will be treated as a single slot. For example, the grass on a route
      will contain only a single encounter. Each rod is a separate encounter.

    This setting has no effect if wild Pokemon are not randomized.
    This setting does not affect the bug catching contest.
    """
    display_name = "Encounter Grouping"
    default = 0
    option_all_split = 0
    option_one_to_one = 1
    option_one_per_method = 2


class ForceFullyEvolved(NamedRange):
    """
    When an opponent uses a Pokemon of the specified level or higher, restricts the species to only fully evolved Pokemon.

    Evolution Level instead evolves each opponent Pokemon into the species it would naturally have become at its level,
    so a species is never used at or above the level it would evolve at. Species that do not evolve by level are
    unaffected.

    Only applies when trainer parties are randomized.
    """
    display_name = "Force Fully Evolved"
    range_start = 0
    range_end = 100
    default = 0
    special_evolution_level = -1
    special_range_names = {
        "disabled": 0,
        "evolution_level": special_evolution_level
    }


class TimeOfDayEncounters(Toggle):
    """
    When enabled, land encounters vary by time of day (morning/day/night), and
    fishing encounters that vary by time of day in vanilla vary by day/night.
    Each time period is randomized independently.

    When disabled, all time periods use the same encounters.
    """
    display_name = "Time of Day Encounters"


class UnlockableTimeOfDay(Toggle):
    """
    When enabled, the player must find Morn, Day and Nite items to access
    land and fishing encounters for those time periods. You start with one of these at random.

    Requires Time of Day Encounters to be enabled.

    Time of day can be adjusted using the Pokegear.
    """
    display_name = "Unlockable Time of Day"


class EncounterSlotDistribution(Choice):
    """
    Sets how the Pokemon encounter slots in an area are distributed.

    Remove 1%'s modifies grass/cave encounters to 30%/25%/20%/10%/5%/5%/5% and does not modify any others.
    Balanced sets the following:
        Grass/Cave: 20%/20%/15%/15%/10%/10%/10%
        Surf (unchanged): 60%/30%/10%
        Headbutt:  20%/20%/20%/15%/15%/10%
        Rock Smash: 70%/30%
        Fishing (unchanged):
            Old Rod: 70%/15%/15%
            Good Rod: 35%/35%/20%/10%
            Super Rod: 40%/30%/20%/10%
        Bug Catching Contest (unchanged): 20%/20%/10%/10%/10%/10%/5%/5%/5%/5%
    Equal sets all encounter slots to have (almost) equal probability.
    """
    display_name = "Encounter Slot Distribution"
    default = 1
    option_vanilla = 0
    option_remove_one_percents = 1
    option_balanced = 2
    option_equal = 3


class RandomizeStaticPokemon(Choice):
    """
    Randomizes species of static Pokemon encounters
    This includes overworld Pokemon, gift Pokemon and gift egg Pokemon

    Match Types: Pokemon are replaced with Pokemon of the same type
    Match Base Stats: Pokemon are replaced with Pokemon of similar base stat totals
    Match Types and Base Stats: Pokemon are replaced with Pokemon of the same type and similar base stat totals
    Completely Random: Pokemon are replaced with completely random Pokemon

    NOTE: If this setting is disabled, the Odd Egg will still be fixed to a single possible Pokemon
    """
    display_name = "Randomize Static Pokemon"
    default = 0
    option_vanilla = 0
    option_completely_random = 1
    option_match_types = 2
    option_match_base_stats = 3
    option_match_types_and_base_stats = 4

    @property
    def matches_types(self) -> bool:
        return self.value in (self.option_match_types, self.option_match_types_and_base_stats)

    @property
    def matches_base_stats(self) -> bool:
        return self.value in (self.option_match_base_stats, self.option_match_types_and_base_stats)


class StaticBlocklist(PokemonSet):
    """
    These Pokemon will not appear as static overworld encounters, gift eggs, gift Pokemon or received trade Pokemon
    Only applies to static Pokemon or received trade Pokemon that are randomized
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Static Blocklist"


class UniqueStaticPokemon(Choice):
    """
    Makes static encounter species globally unique. A species rolled into a static slot will not
    appear in another static slot, and will be excluded from wild encounters. If evolution methods
    are logically required, pre-evolutions of the static species (along logically-required evolution
    paths) are also excluded from wilds. If breeding methods are logically required, any Pokemon
    whose egg produces a static species is also excluded from wilds.

    Only applies to static slots that are in logic. Does nothing if static Pokemon are not randomized or not required.

    - Legendaries Only: only applies to the four legendary static slots (Suicune, Lugia, Ho-Oh, Celebi)
    - Legendaries and Uniques: the legendary slots plus the unique overworld encounters
    (Sudowoodo, Red Gyarados, Snorlax, Lapras)
    - All: applies to every static slot
    """
    display_name = "Unique Static Pokemon"
    default = 0
    option_disabled = 0
    option_legendaries_only = 1
    option_legendaries_and_uniques = 2
    option_all = 3


class RandomizeTrades(Choice):
    """
    Randomizes species of in-game trades
    Received species respect the Static Blocklist
    """
    display_name = "Randomize Trades"
    default = 0
    option_vanilla = 0
    option_received = 1
    option_requested = 2
    option_both = 3


class RandomizeTrainerParties(Choice):
    """
    Randomizes Pokemon in enemy trainer parties

    - Match Types: Pokemon are replaced with Pokemon of the same type
    - Match Base Stats: Pokemon are replaced with Pokemon of similar base stat totals
    - Match Types and Base Stats: Pokemon are replaced with Pokemon of the same type and similar base stat totals
    - Completely Random: Pokemon are replaced with completely random Pokemon
    """
    display_name = "Randomize Trainer Parties"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_completely_random = 2
    option_match_base_stats = 3
    option_match_types_and_base_stats = 4

    @property
    def matches_types(self) -> bool:
        return self.value in (self.option_match_types, self.option_match_types_and_base_stats)

    @property
    def matches_base_stats(self) -> bool:
        return self.value in (self.option_match_base_stats, self.option_match_types_and_base_stats)


class TrainerPartyBlocklist(PokemonSet):
    """
    These Pokemon will not appear in enemy trainer parties
    Does nothing if trainer parties are not randomized
    Blocklists are best effort, other constraints may cause them to be ignored
    """
    display_name = "Trainer Party Blocklist"


class LevelScaling(Choice):
    """
    Sets whether Trainer, Wild Pokemon and Static Pokemon levels are scaled based on sphere access.

    - Off: Vanilla levels are used.
    - Spheres: Levels are scaled based on sphere access only.
    - Spheres and Distance: Levels are scaled based on both sphere access and distance from starting town.
    """
    display_name = "Level Scaling"
    default = 0
    option_off = 0
    option_spheres = 1
    option_spheres_and_distance = 2


class LevelCurve(Choice):
    """
    When level scaling is enabled, use a custom level curve instead of deriving levels from vanilla data.
    The curve distributes levels from min to max across all scaled levels (trainers, statics, and wild encounters).

    - Vanilla: Use vanilla levels as the basis for scaling.
    - Linear: Levels increase at a constant rate from min to max.
    - Sqrt: Levels rise quickly early then taper off. Harder early game, compressed late game.
    - Quadratic: Levels stay low early then rise steeply. Easier early game, rapid late-game growth.
    - S Curve: Slow start, fast middle, slow finish.
    """
    display_name = "Level Curve"
    default = 0
    option_vanilla = 0
    option_linear = 1
    option_sqrt = 2
    option_quadratic = 3
    option_s_curve = 4


class LevelCurveMinLevel(Range):
    """
    The starting level for the custom level curve. Only used when Level Curve is not vanilla.
    """
    display_name = "Level Curve Min Level"
    default = 2
    range_start = 1
    range_end = 100


class LevelCurveMaxLevel(Range):
    """
    The ending level for the custom level curve. Only used when Level Curve is not vanilla.

    Red will be scaled so his lowest level matches this value. Wilds and statics will be scaled up to 2/3 of this value.

    NOTE: Trainers are scaled based on their lowest level party member, so they can have levels above this value.
    """
    display_name = "Level Curve Max Level"
    default = 73
    range_start = 1
    range_end = 100


class LockKantoGyms(Choice):
    """
    Logically lock entering all Kanto gyms, Mt. Moon and Trainer House behind access to a high level Pokemon, included locations:
    - Snorlax
    - Ho-oh
    - Lugia
    - Suicune
    - Silver Cave entrance
    - Victory Road

    You can still enter gyms, Mt. Moon and Trainer House without access to any of these.

    NOTE: This option is automatically disabled when Level Scaling is enabled.
    """
    display_name = "Lock Kanto Gyms"
    option_off = 0
    option_high_level_pokemon = 1


class BoostTrainerPokemonLevels(Choice):
    """
    Boost levels of every trainer's Pokemon. There are 2 different boost modes:
    Percentage Boost: Increases every trainer Pokemon's level by the boost percentage.
    Set Min Level: Trainer Pokemon will be the specified level or higher.
    """
    display_name = "Boost Trainer Pokemon Levels"
    default = 0
    option_vanilla = 0
    option_percentage_boost = 1
    option_set_min_level = 2


class TrainerLevelBoostValue(Range):
    """
    This Value only works if Boost Trainer Pokemon Levels is being used.
    The meaning of this value depends on Trainer Boost Mode.

    Percentage Boost: This value represents the boost amount percentage
    Set Min Level: Trainer Pokemon will never be lower than this level
    """
    display_name = "Trainer Level Boost Value"
    default = 1
    range_start = 1
    range_end = 100


class RandomizeLearnsets(Choice):
    """
    - Vanilla: Vanilla learnsets
    - Randomize: Random learnsets
    - Start With Four Moves: Random learnsets with 4 starting moves
    """
    display_name = "Randomize Learnsets"
    default = 0
    option_vanilla = 0
    option_randomize = 1
    option_start_with_four_moves = 2


class MetronomeOnly(Toggle):
    """
    Only Metronome is usable in battle, PP is infinite
    You can still teach HMs and useful TMs
    """
    display_name = "Metronome Only"


class LearnsetTypeBias(NamedRange):
    """
    This option will have an effect only if Randomize Learnset option is enabled.

    Percentage chance of each move in a Pokemon's learnset to match one of its types.
    Default value is none (-1). This means there will be no bias.
    The lowest possible type matching value is 0. This means there will be no STAB moves in a Pokemon's learnset.
    If set to 100 all moves that a Pokemon will learn by levelling up will match one of its types.
    """
    display_name = "Move Learnset Type Bias"
    default = -1
    range_start = -1
    range_end = 100
    special_range_names = {
        "none": -1,
    }

    @classmethod
    def from_text(cls, text: str) -> Range:
        if text == "vanilla":
            text = "none"
        return super().from_text(text)


class RandomizeMoves(EnhancedOptionSet):
    """
    Randomizes the properties of moves.

    The following options can be provided:
    - Power Restricted: Multiplies the power of each move by a random number between 0.5 and 1.5
    - PP Restricted: Adds or subtracts 0, 5 or 10 from original move PP. Base PP is limited to 5-40.
    - Power Full: Randomizes the power of each move in the range 20-150.
      Multi hit moves have their power divided by average hit count.
    - PP Full: Randomizes the PP of each move in the range 5-40.
    - Accuracy: Randomizes the accuracy of each move. Accuracy has a 70% chance to be 100% for each move,
      otherwise it is linearly distributed in the range 30-100.
    - Type: Randomizes the type of each move.
    - _All includes all options.
    - _Random has a 50% chance to include each option that is not already included.
    - _RandomExcludingAccuracy has a 50% chance to include each option except Accuracy.

    Full options override Restricted options.
    """
    display_name = "Randomize Moves"
    default = []

    POWER_RESTRICTED = "Power Restricted"
    POWER_FULL = "Power Full"
    PP_RESTRICTED = "PP Restricted"
    PP_FULL = "PP Full"
    ACCURACY = "Accuracy"
    TYPE = "Type"

    RANDOM_EXCLUDING_ACCURACY = "_RandomExcludingAccuracy"

    valid_keys = [POWER_RESTRICTED, POWER_FULL, PP_RESTRICTED, PP_FULL, ACCURACY, TYPE, RANDOM_EXCLUDING_ACCURACY]

    def __init__(self, value):
        if isinstance(value, list):
            value = [self.RANDOM_EXCLUDING_ACCURACY if x.lower() == "_randomexcludingaccuracy" else x for x in value]

            if self.RANDOM_EXCLUDING_ACCURACY in value:
                value = [v for v in value if v != self.RANDOM_EXCLUDING_ACCURACY]
                value += [k for k in sorted(self.valid_keys) if not k.startswith("_") and k != self.ACCURACY
                          and random.getrandbits(1)]

        super().__init__(value)

    @classmethod
    def from_any(cls, data: Any):
        key_map = {k.replace(" ", "_").lower(): k for k in cls.valid_keys}
        if isinstance(data, dict):
            return cls([key_map.get(k, k) for k, v in data.items() if v != 0])
        if is_iterable_except_str(data):
            return cls([key_map.get(item, item) for item in data])
        return cls.from_text(str(data))

    @classmethod
    def from_text(cls, text: str):
        if text in ("vanilla", "0"):
            return cls([])
        elif text in ("restricted", "1"):
            return cls([cls.POWER_RESTRICTED, cls.PP_RESTRICTED])
        elif text in ("full_exclude_accuracy", "2"):
            return cls([cls.POWER_FULL, cls.PP_FULL])
        elif text in ("full", "3"):
            return cls([cls.POWER_FULL, cls.PP_FULL, cls.ACCURACY])
        return super().from_text(text)


class RandomizeTypeChart(Choice):
    """
    Randomizes the type matchup chart
    - Vanilla: Type matchups are unchanged
    - Shuffle: Shuffles type matchups around, keeping the same number of each possible matchup
    - Completely Random: Generates a random matchup for each type pair. WARNING: This can result in a lot of immunities
    """
    display_name = "Randomize Type Chart"
    default = 0
    option_vanilla = 0
    option_shuffle = 1
    option_completely_random = 2


class PhysicalSpecialSplit(Choice):
    """
    Sets how moves are determined to be Physical or Special
    - Vanilla: Determined by move type, for example: all Fire moves are Special
    - Modern: Determined by the move, for example: Flame Wheel is Physical and Ember is Special
    - Random by type: Vanilla, but shuffled randomly for each type
    - Random by move: Modern, but shuffled randomly for each move
    """
    display_name = "Physical/Special Split"
    default = 0
    option_vanilla = 0
    option_modern = 1
    option_random_by_type = 2
    option_random_by_move = 3


class RandomizeTMMoves(Toggle):
    """
    Randomizes the moves available as TMs
    """
    display_name = "Randomize TM Moves"


_ignored_tm_moves = ("NO_MOVE", "STRUGGLE", "HEADBUTT", "ROCK_SMASH", "CUT", "FLY", "SURF", "STRENGTH", "FLASH",
                     "WHIRLPOOL", "WATERFALL")


class TMPlando(WeightedOptionDict):
    """
    Specify what move a TM will contain.
    TMs 02 and 08 can never be plandoed. This also means Headbutt and Rock Smash cannot be plandoed onto other TMs.
    If Dexsanity or Dexcountsanity are enabled, and Sweet Scent hasn't been plandoed, it will be forced to TM12.
    This option takes priority over the TM Blocklist and vanilla TMs, and is ignored in Metronome Only mode.

    A single move or a weighted dict of moves can be provided per TM:
    tm_plando:
      1: Dynamicpunch
      3: Curse
      10:
        Ice Beam: 50
        Blizzard: 50
    """
    display_name = "TM Plando"
    valid_keys = {str(i) for i in range(1, 51)} - {"2", "8"}

    valid_values = set(
        sorted(move.name.title() for id, move in data.moves.items() if id not in _ignored_tm_moves))

    def __init__(self, value):
        normalized = {int(k): v for k, v in sorted(value.items())}
        super().__init__(normalized)


class TMSameTypeCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each TM whose move type matches one of the Pokemon's types.
    Headbutt and Rock Smash are considered HMs when applying compatibility.
    """
    display_name = "TM Same Type Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "fully_compatible": 100
    }


class TMOtherTypeCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each TM whose move type does not match any of the Pokemon's types.
    Headbutt and Rock Smash are considered HMs when applying compatibility.
    """
    display_name = "TM Other Type Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "fully_compatible": 100
    }


class HMSameTypeCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each HM whose move type matches one of the Pokemon's types.
    Headbutt and Rock Smash are considered HMs when applying compatibility.

    You can look up HM compatible Pokemon in the Pokedex using the search function.
    """
    display_name = "HM Same Type Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "fully_compatible": 100
    }


class HMOtherTypeCompatibility(NamedRange):
    """
    Percent chance for Pokemon to be compatible with each HM whose move type does not match any of the Pokemon's types.
    Headbutt and Rock Smash are considered HMs when applying compatibility.

    You can look up HM compatible Pokemon in the Pokedex using the search function.
    """
    display_name = "HM Other Type Compatibility"
    default = -1
    range_start = 0
    range_end = 100
    special_range_names = {
        "vanilla": -1,
        "none": 0,
        "fully_compatible": 100
    }


class HMCompatibilityOverride(OptionDict):
    """
    Allows overriding compatibility percentage for specific HMs

    Uses the following format:
    hm_compatibility_override:
      Headbutt: 10
      Fly: 100
      Flash: 0

    Headbutt and Rock Smash are considered HMs for this setting.
    """
    display_name = "HM Compatibility Override"
    default = {}
    schema = Schema(
        {
            Optional(move.name.title()): And(Use(int), lambda n: 0 < n <= 100) for move in
            data.moves.values() if move.is_hm
        },
    )


class HMPowerCap(NamedRange):
    """
    Lowers the power of damaging HM moves that exceed the set power down to match it.
    Headbutt and Rock Smash are considered HMs for this setting.
    """
    display_name = "HM Power Cap"
    default = 255
    range_start = 20
    range_end = 255
    special_range_names = {
        "none": range_end
    }


class FieldMovesAlwaysUsable(Toggle):
    """
    Decouples TM/HM Compatibility for Battle Moves and Field Moves.
    If enabled, Field Moves will always be considered usable, regardless of TM or HM compatibility. Badge requirements still apply.
    """
    display_name = "Field Moves Always Usable"


class RandomizeBaseStats(Choice):
    """
    - Vanilla: Vanilla base stats
    - Keep BST: Random base stats, but base stat total is preserved
    - Completely Random: Base stats and BST are completely random
    """
    display_name = "Randomize Base Stats"
    default = 0
    option_vanilla = 0
    option_keep_bst = 1
    option_completely_random = 2

class BaseStatsMultiplesOfFive(Toggle):
    """
    When randomizing base stats, aim to make the new base stats multiples of 5.
    When using Keep BST, any remainder will be added to one stat.
    """
    display_name = "Make Random Base Stats Multiples of 5"


class BaseStatsEvolutionMode(Choice):
    """
    - Independent: Base stats are randomized separately for every Pokemon, so evolving can be a downgrade
    - Follow Evolutions: Pokemon inherit their pre-evolution's stat spread, and evolving always increases BST

    Has no effect when Randomize Evolution is enabled, as random evolutions already increase base stat total.
    """
    display_name = "Base Stats Evolution Mode"
    default = 0
    option_independent = 0
    option_follow_evolutions = 1


class RandomizeTypes(Choice):
    """
    - Vanilla: Vanilla Pokemon types
    - Follow Evolutions: Types are randomized but preserved when evolved
    - Completely Random: Types are completely random
    """
    display_name = "Randomize Types"
    default = 0
    option_vanilla = 0
    option_follow_evolutions = 1
    option_completely_random = 2


class SharedPrimaryType(Choice):
    """
    If types are randomized, all Pokemon will share this type
    """
    display_name = "Shared Primary Type"
    default = 0
    option_off = 0
    option_normal = 1
    option_fighting = 2
    option_flying = 3
    option_poison = 4
    option_ground = 5
    option_rock = 6
    option_bug = 8
    option_ghost = 9
    option_steel = 10
    option_fire = 21
    option_water = 22
    option_grass = 23
    option_electric = 24
    option_psychic = 25
    option_ice = 26
    option_dragon = 27
    option_dark = 28


class RandomizeEvolution(Choice):
    """
    - Vanilla: Pokemon evolve into the same Pokemon they do in vanilla
    - Match a Type: Pokemon evolve into a random Pokemon with a higher base stat total, that shares at least one type with it.
    - Increase BST: Pokemon evolve into a random Pokemon with a higher base stat total.

    Note: If random BST, random types, or the evolution blocklist cause a Pokemon to have no valid evolution within
    your chosen setting here, it will evolve into the closest available thing to a valid evolution.

    Note: All Pokemon will be standardized to the medium-fast EXP curve when any evolution randomization is enabled.
    """
    display_name = "Randomize Evolution"
    default = 0
    option_vanilla = 0
    option_match_a_type = 1
    option_increase_bst = 2


class ConvergentEvolution(Choice):
    """
    Random evolution can cause multiple Pokemon to evolve into the same Pokemon.
    - Avoid: Each Pokemon can only evolve from one Pokemon.
    - Allow: Multiple Pokemon can evolve into the same Pokemon.
    """
    display_name = "Convergent Evolution"
    default = 0
    option_avoid = 0
    option_allow = 1


class EvolutionBlocklist(PokemonSet):
    """
    No Pokemon will evolve into these Pokemon. Does nothing if evolution is not randomized.
    Blocklists are best effort, other constraints may cause them to be ignored.
    """
    display_name = "Evolution Blocklist"


class MaximumEvolutionLevel(NamedRange):
    """
    Reduces all level-based evolution levels to at most the specified level.
    """
    display_name = "Maximum Evolution Level"
    default = 100
    range_start = 1
    range_end = 100
    special_range_names = {
        "disabled": 100
    }


class RandomizeBreeding(Choice):
    """
    - Vanilla: Breeding is unchanged
    - Random Line Base: Each Pokemon will produce eggs for a random base Pokemon that evolves into it
    - Random Any Base: Each Pokemon will produce eggs for a random base Pokemon
    - Random Lower BST: Each Pokemon will produce eggs for a random Pokemon with equal or lower BST
    - Completely Random: Each Pokemon will produce eggs for a random Pokemon
    """
    display_name = "Randomize Breeding"
    default = 0
    option_vanilla = 0
    option_line_base = 1
    option_any_base = 2
    option_decrease_bst = 3
    option_completely_random = 4


class BreedingBlocklist(PokemonSet):
    """
    No Pokemon will produce eggs containing these Pokemon.
    Blocklists are best effort, other constraints may cause them to be ignored.
    """
    display_name = "Breeding Blocklist"


class ModifyPalettes(Choice):
    """
    - Vanilla: Vanilla Pokemon color palettes
    - Match Types: Color palettes match Pokemon Type
    - Randomize: Color palettes are completely random
    - Swap Shiny: Regular Pokemon use shiny palettes and vice versa
    - Gold and Silver: For the Pokemon whose palettes changed between Gold/Silver and Crystal, restores their old palette
    """
    display_name = "Modify Palettes"
    default = 0
    option_vanilla = 0
    option_match_types = 1
    option_randomize = 2
    option_swap_shiny = 3
    option_gold_and_silver = 4


class RandomizeMusic(Choice):
    """
    Randomize all music
    - Shuffle will map each music track to a new track
    - Completely Random will map each music area to a new track
    """
    display_name = "Randomize Music"
    default = 0
    option_off = 0
    option_shuffle = 1
    option_completely_random = 2


class FreeFlyLocation(Choice):
    """
    - Free Fly: Unlocks a random Fly destination when Fly is obtained.
    - Free Fly and Map Card: Additionally unlocks a random Fly destination after obtaining both the Pokegear and Map Card.
    - Map Card: Unlocks a single random Fly destination only after obtaining both the Pokegear and Map card.
    """
    display_name = "Free Fly Location"
    default = 0
    option_off = 0
    option_free_fly = 1
    option_free_fly_and_map_card = 2
    option_map_card = 3


class EarlyFly(Toggle):
    """
    HM02 Fly will be placed early in the game
    If this option is enabled, you will be able to Fly before being forced to use an item to progress
    Early Fly is a best effort setting, if Fly and its badge cannot be placed early, then they will be placed
        randomly
    """
    display_name = "Early Fly"


class HMBadgeRequirements(Choice):
    """
    - Vanilla: HMs require their vanilla badges
    - No Badges: HMs do not require a badge to use
    - Add Kanto: HMs can be used with the Johto or Kanto badge
    - Regional: HMs can be used in Johto with the Johto badge or in Kanto with the Kanto badge
        This does not apply to Fly which will accept either badge
        Routes 26, 27, 28 and Tohjo Falls are in Johto for HM purposes
    """
    display_name = "HM Badge Requirements"
    default = 0
    option_vanilla = 0
    option_no_badges = 1
    option_add_kanto = 2
    option_regional = 3


class RemoveBadgeRequirement(EnhancedOptionSet):
    """
    Specify which HMs do not require a badge to use. This overrides the HM Badge Requirements setting.

    _Random has a 50% chance to include HMs which are not already included
    _All will include all HMs

    HMs should be provided in the form: "Fly".
    """
    display_name = "Remove Badge Requirement"

    CUT = "Cut"
    FLY = "Fly"
    SURF = "Surf"
    STRENGTH = "Strength"
    FLASH = "Flash"
    WHIRLPOOL = "Whirlpool"
    WATERFALL = "Waterfall"

    valid_keys = [CUT, FLY, SURF, STRENGTH, FLASH, WHIRLPOOL, WATERFALL]


class RequireFlash(Choice):
    """
    Determines if the ability to use Flash is required to traverse dark areas

    - Not Required: Dark areas do not require Flash at all
    - Logically Required: Dark areas will expect you to be able to use Flash for logic, but you can traverse them without
    - Hard Required: You will not be able to traverse dark areas without the ability to use Flash there
    """
    display_name = "Require Flash"
    default = 1
    option_not_required = 0
    option_logically_required = 1
    option_hard_required = 2


class RemoveIlexCutTree(Toggle):
    """
    Removes the Cut tree in Ilex Forest
    """
    display_name = "Remove Ilex Forest Cut Tree"


class SaffronGatehouseTea(EnhancedOptionSet):
    """
    Sets which Saffron City gatehouses require Tea to pass. Obtaining the Tea will unlock them all.
    If any gatehouses are enabled, adds a new location in Celadon Mansion 1F and adds Tea to the item pool.
    Valid options are: North, East, South and West in any combination.
    _Random gives each gate that is not already included a 50% chance to be included.
    _All is shorthand for all valid options except _Random of course.
    """
    display_name = "Saffron Gatehouse Tea"

    NORTH = "North"
    EAST = "East"
    SOUTH = "South"
    WEST = "West"

    valid_keys = [NORTH, EAST, SOUTH, WEST]


class EastWestUnderground(Toggle):
    """
    Adds an Underground Pass between Route 7 and Route 8 in Kanto.
    """
    display_name = "East - West Underground"


class UndergroundsRequirePower(Choice):
    """
    Specifies which of the Kanto Underground Passes require the Machine Part to be returned to access.
    """
    display_name = "Undergrounds Require Power"
    default = 0
    option_both = 0
    option_north_south = 1
    option_east_west = 2
    option_neither = 3


class ReusableTMs(Toggle):
    """
    TMs can be used an infinite number of times
    """
    display_name = "Reusable TMs"


class MinimumCatchRate(Range):
    """
    Sets a minimum catch rate for wild Pokemon
    """
    display_name = "Minimum Catch Rate"
    default = 0
    range_start = 0
    range_end = 255


class SkipEliteFour(Toggle):
    """
    Go straight to Lance when challenging the Elite Four
    """
    display_name = "Skip Elite Four"


class LanceRequiresEliteFour(Toggle):
    """
    Lance's room kicks you out unless you have beaten all four Elite Four members.

    Has no effect if Skip Elite Four is enabled.
    """
    display_name = "Lance Requires Elite Four"


class BetterMarts(Toggle):
    """
    If this option is enabled then the Pokcenter 2F mart will not upgrade as you beat gyms.
    Instead, it will always be the final upgrade.
    """
    display_name = "Better Marts"


class BuildAMart(OptionList):
    """
    Create a custom shop in place of the final upgraded Pokecenter 2F mart.
    The first two shop items will always be Poke Ball and Escape Rope.
    Maximum of 14 items, any extra items will be discarded.
    
    Available items: Antidote, Awakening, Burn Heal, Calcium, Carbos, Dire Hit, Dragon Scale, Elixer, Ether,
    Fast Ball, Fire Stone, Fresh Water, Friend Ball, Full Heal, Full Restore, Great Ball, Guard Spec, Heavy Ball,
    HP Up, Hyper Potion, Ice Heal, Iron, Kings Rock, Leaf Stone, Lemonade, Level Ball, Link Cable, Love Ball,
    Lure Ball, Master Ball, Max Elixer, Max Ether, Max Potion, Max Repel, Max Revive, Metal Coat, Moon Ball,
    Moon Stone, Park Ball, Parlyz Heal, Potion, Protein, PP Up, Rare Candy, Repel, Revive, Soda Pop, Sun Stone,
    Super Potion, Super Repel, Thunderstone, Ultra Ball, Up-Grade, Water Stone, X Accuracy, X Attack, X Defend,
    X Special, X Speed.
    """
    display_name = "Build-a-Mart"
    valid_keys = sorted(item.label for item in data.items.values() if "CustomShop" in item.tags)


class GrowthRates(Choice):
    """
    Controls the experience growth rate curves for Pokemon.
    - Vanilla: Use the original growth rate for each Pokemon species.
    - Normalized: Legendary Pokemon use the Slow growth rate.
      All other Pokemon use Medium Fast.

    This option is ignored when evolution randomization is enabled;
    all Pokemon will use Medium Fast in that case.
    """
    display_name = "Growth Rates"
    default = 1
    option_vanilla = 0
    option_normalized = 1


class ExpModifier(NamedRange):
    """
    Scale the amount of Experience Points given in battle
    Default is 20, for double set to 40, for half set to 10, etc

    You can modify this value in-game, the CUSTOM option will use the value provided here.
    """
    display_name = "Experience Modifier"
    default = 20
    range_start = 1
    range_end = 255
    special_range_names = {
        "half": default // 2,
        "normal": default,
        "double": default * 2,
        "triple": default * 3,
        "quadruple": default * 4,
        "quintuple": default * 5,
        "sextuple": default * 6,
        "septuple": default * 7,
        "octuple": default * 8,
    }


class ExpShareType(Choice):
    """
    Sets which experience-sharing item is placed in the multiworld.

    - Exp Share: The vanilla Exp Share.
    - Exp All: A key item that toggles on/off. When on, all non-participating party Pokemon earn
    experience.
    """
    display_name = "Exp Share Type"
    option_exp_share = 0
    option_exp_all = 1
    default = 0


class StartingMoney(NamedRange):
    """
    Sets your starting money.
    """
    display_name = "Starting Money"
    default = 3000
    range_start = 0
    range_end = 999999
    special_range_names = {
        "vanilla": 3000
    }


class AllPokemonSeen(Toggle):
    """
    Start with all Pokemon seen in your Pokedex.
    This allows you to see where the Pokemon can be encountered in the wild.
    """
    display_name = "All Pokemon Seen"


class TrapWeight(Range):
    """
    Percentage chance each filler item is replaced with a trap

    If no traps have any weight, this option does nothing

    NOTE: This option has a maximum of 20 by default, this can be changed by setting maximum_filler_trap_percentage in host.yaml
    """
    display_name = "Filler Trap Percentage"
    default = 0
    range_start = 0
    range_end = 100


_trap_weight_min = 0
_trap_weight_max = 100


class TrapWeights(OptionCounter):
    """
    Specifies the weights at which traps become each trap type

    - Burn, Paralysis, Sleep, Poison and Freeze traps afflict the corresponding status on your party
    - Phone Traps trigger random Pokegear calls (NOTE: Phone Traps loop after you receive 32 of them)
    - Tutorial Traps trigger the catch tutorial
    - Teleport Traps use the move Teleport (both in battle and out of battle)
    - Whirlpool Traps spin you around in the overworld or trap you in Whirlpool for 99 turns in battle
    - Ice Traps make the overworld slippery for 40-60 steps
    - Explosion Traps faint a party member in the overworld or use Explosion in battle
    - Sandstorm Traps slow you in the overworld for 20-40 steps or activate Sandstorm for 99 turns in battle
    - Metronome Traps trigger a random other move trap in the overworld or use Metronome in battle
    - Shuffle Traps randomize the order of items in your Items and Balls pockets
    """
    min = _trap_weight_min
    max = _trap_weight_max
    default = {
        trap.label: 0 for trap in data.items.values() if trap.classification & ItemClassification.trap
    }
    schema = Schema(
        {
            Optional(trap): Or(int, "random", "default", "high", "low",
                               "random-low", "random-middle", "random-high",
                               Regex(r"^random-range-(?:low-|middle-|high-)?\d+-\d+$"))
            for trap in default.keys()
        }
    )

    class _TrapWeightsRange(Range):
        range_start = _trap_weight_min
        range_end = _trap_weight_max

    @classmethod
    def from_any(cls, data: dict[str, Any]) -> OptionCounter:
        resolved_data = {
            key: cls._TrapWeightsRange.from_any(value).value for key, value in sorted(data.items())
        }
        return super().from_any(resolved_data)


class TrapLink(Toggle):
    """
    Games that support traplink will all receive similar traps when a matching trap is sent from another traplink game

    This only applies to traps you have enabled
    """
    display_name = "Trap Link"


class WonderTrading(DefaultOnToggle):
    """
    Allows participation in wonder trading with other players in your current multiworld. Speak with the wonder trade receptionist on the second floor of any Pokemon Center.

    Wonder trading NEVER affects logic.

    Pokemon traded this way may come from other Pokemon games. Stat experience, DVs, and similar species-specific data may not survive the trip perfectly across generations.

    Received Pokemon are not marked as caught in your Pokedex.
    """
    display_name = "Wonder Trading"


class EnableMischief(Choice):
    """
    If I told you what this does, it would ruin the surprises :)
    """
    display_name = "Enable Mischief"
    default = 0
    option_off = 0
    alias_false = option_off  # For compatibility
    alias_no = option_off  # For compatibility
    option_mild = 1
    option_wild = 2
    alias_true = option_wild  # For compatibility
    alias_on = option_wild  # For compatibility
    alias_yes = option_wild  # For compatibility


class CustomMischiefPool(OptionSet):
    """Only allow specific Mischief options"""
    display_name = "Custom Mischief Pool"
    visibility = Visibility.none
    valid_keys = [misc_option.name for misc_option in list(MiscOption)] + ["_Mild", "_Wild"]


class MischiefLowerBound(Range):
    """
    Lower bound of selectable mischief, in percentage
    """
    display_name = "Mischief Lower Bound"
    visibility = Visibility.none
    default = 50
    range_start = 0
    range_end = 100


class MischiefUpperBound(Range):
    """
    Upper bound of selectable mischief, in percentage
    """
    display_name = "Mischief Upper Bound"
    visibility = Visibility.none
    default = 75
    range_start = 0
    range_end = 100


class MoveBlocklist(OptionSet):
    """
    Pokemon won't learn these moves via learnsets.
    Moves should be provided in the form: "Ice Beam"
    Does not apply to vanilla learnsets
    """
    display_name = "Move Blocklist"
    valid_keys = sorted(move.name.title() for id, move in data.moves.items() if id not in ("NO_MOVE", "STRUGGLE"))


class TMBlocklist(OptionSet):
    """
    No TM will contain these moves.
    Moves should be provided in the form: "Ice Beam"
    Does not apply to vanilla TMs
    """
    display_name = "TM Blocklist"
    valid_keys = sorted(move.name.title() for id, move in data.moves.items()
                        if id not in ("NO_MOVE", "STRUGGLE", "ROCK_SMASH", "HEADBUTT") and not move.is_hm)


class ModerniseMovesGeneration(NamedRange):
    """
    Selects the generation to update moves to.
    This affects power, PP and accuracy only and is applied before any randomization.
    """
    display_name = "Modernise Moves"
    default = 0
    range_start = 3
    range_end = 9
    special_range_names = {
        "disabled": 0,
        "newest": range_end
    }


class ModerniseMovesType(Choice):
    """
    Selects whether generational buffs, nerfs or both are applied to moves.
    Only has an effect if a generation is selected to modernise moves to.
    """
    display_name = "Modernise Moves Type"
    default = 0
    option_buffs_and_nerfs = 0
    option_buffs_only = 1
    option_nerfs_only = 2


class FlyLocationBlocklist(OptionSet):
    """
    These locations won't be given to you as fly locations, either as your free one or from receiving the map card.
    Locations should be provided in the form: "Ecruteak City"
    If you blocklist enough locations that there aren't enough locations left for your total number of free fly locations, the blocklist will simply do nothing
    "_Johto" and "_Kanto" are shortcuts for all Johto and Kanto towns respectively
    """
    display_name = "Fly Location Blocklist"
    valid_keys = sorted(region.name for region in data.fly_regions) + ["_Johto", "_Kanto"]


class RemoteItems(Toggle):
    """
    Instead of placing your own items directly into the ROM, all items are received from the server, including items you find for yourself.
    This enables co-op of a single slot and recovering more items after a lost save file (if you're so unlucky).
    But it changes pickup behavior slightly and requires connection to the server to receive any items.
    """
    display_name = "Remote Items"


class AlwaysUnlockFly(Toggle):
    """
    Always unlock Fly destinations when entering a town, even if Randomize Fly Unlocks is enabled.
    This does not work with Randomize Fly Destinations and is not considered by logic.
    """
    display_name = "Always Unlock Fly Destinations"


class TrainerGender(Choice):
    """
    Preset your trainer's gender, this skips the in-game prompt.
    """
    display_name = "Trainer Gender"
    default = 0
    option_vanilla = 0
    option_boy = 1
    option_girl = 2
    option_randomize = 3


class TrainerName(FreeText):
    """
    Preset your trainer name, this skips the name prompt.

    Only the first seven characters will be used, unsupported characters will be replaced with '?'.
    """
    display_name = "Trainer Name"


class RivalName(FreeText):
    """
    Preset your rival's name, this skips the name prompt in Elm's Lab.

    Only the first seven characters will be used, unsupported characters will be replaced with '?'.
    Alternatively (only at Multiworld generation), you can enter the values "random_player" and "random_crystal" to use the name of a random player in the multiworld, respectively from any game and from Pokemon Crystal specifically.
    """
    display_name = "Rival Name"


class StartTime(FreeText):
    """
    Preset the game's start time, this skips the introduction's prompt.

    Must have the format "HH:MM", with hours going from 0 to 23.
    Alternatively, you can enter the value "now", which will automatically use the multiworld generation time (or patch time when using option overrides)
    """
    display_name = "Start Time"


class GameOptions(OptionDict):
    """
    Presets in-game options. These can be changed in-game later. Any omitted options will use their default.

    Allowed options and values, with default first:

    ap_item_notification: popup_sound/popup/sound/none - Sets how items received from AP are announced (popup_sound shows the popup and plays the sound)
    auto_hms: off/on - HMs will be used automatically where possible, if their usage conditions are met
    auto_run: off/on - Sets whether run activates automatically, if on you can hold B to walk
    battle_always_run: off/on - Sets whether running from wild battles always succeeds, including through trapping moves like Mean Look and Wrap
    battle_animations: all/no_scene/no_bars/speedy - Sets which battle animations are played:
        all: All animations play, including entry and moves
        no_scene: Entry and move animations do not play
        no_bars: Entry, move and HP/EXP bar animations do not play
        speedy: No battle animations play and many delays are removed to make battles faster
    battle_move_stats: off/on - Sets whether or not to display power and accuracy of moves in battle
    battle_shift: shift/set - Sets whether you are asked to switch between trainer Pokemon
    bike_music: on/off - Sets whether the bike music will play
    blind_trainers: off/on - Sets whether trainers will see you without talking to them directly
    catch_exp: off/on - Sets whether or not you get EXP for catching a Pokemon
    dex_area_beep: off/on - Sets whether the Pokedex beeps for land and Surf encounters in the current area
    exp_distribution: gen2/gen6/gen8/no_exp - Sets the EXP distribution method:
        gen2: EXP is split evenly among battle participants, Exp All splits evenly between participants and non-participants
        gen6: Participants earn 100% of EXP, non-participants earn 50% of EXP when Exp All is enabled
        gen8: Participants earn 100% of EXP, non-participants earn 100% of EXP when Exp All is enabled
        no_exp: EXP is disabled
    fast_egg_hatch: off/on - Sets whether eggs take a single cycle to hatch
    fast_egg_make: off/on - Sets whether eggs are guaranteed after one cycle at the day care
    guaranteed_catch: off/on - Sets whether balls have a 100% success rate
    hms_require_teaching: on/off - Sets whether it is required to teach field moves to use them in the field
    local_item_notification: text/sound/none - Sets how Trainersanity, Dex(count)sanity and Grasssanity locations show item notifications
    low_hp_beep: on/off - Sets whether the low HP beep is played in battle
    menu_account: on/off - Sets whether extra information is shown on the Start menu
    more_uncaught_encounters: off/on - Sets whether wild encounters of Pokemon you have not caught are more likely
    music: on/off - Sets whether music will play
    poison_flicker: on/off - Sets whether the overworld poison flash effect is played
    rods_always_work: off/on - Sets whether the fishing rods always succeed
    scaling_exp: off/on - Sets whether EXP scales based on level difference as in Generation 5
    short_fanfares: off/on - Sets whether item receive fanfares are shortened
    skip_dex_registration: off/on - Sets whether the Pokedex registration screen is skipped
    skip_nicknames: off/on - Sets whether you are asked to nickname a Pokemon upon receiving it
    sound: mono/stereo - Sets the sound mode
    spinners: normal/rotators/heck/hell - Sets the overworld behaviour of trainers
        normal: Trainers will behave as they do in vanilla
        rotators: Trainers that spin randomly will rotate consistently
        heck: All trainers with vision rotate consistently, they have their original vision range but can spot you through obstacles
        hell: All trainers with vision will spin randomly, have max vision and can spot you through obstacles
    surf_music: on/off - Sets whether the surf music will play
    text_frame: 1-8 - Sets the textbox frame, "random" will pick a random frame
    text_speed: mid/slow/fast/instant - Sets the speed at which text advances
    time_of_day: auto/morn/day/nite - Sets a time of day override, auto follows the clock, "random" will pick a random time
    tracker_slot: 0-255 - Sets which tracker slot is used for map tracking, used for co-op seeds
    trainersanity_indication: off/on - Sets whether Trainersanity trainers have grayscale sprites until they are beaten
    turbo_button: none/a/b/a_or_b - Sets which buttons auto advance text when held
    """
    display_name = "Game Options"
    default = {
        "text_speed": "mid",
        "battle_shift": "shift",
        "battle_animations": "all",
        "sound": "mono",
        "menu_account": "on",
        "text_frame": 1,
        "bike_music": "on",
        "surf_music": "on",
        "skip_nicknames": "off",
        "auto_run": "off",
        "spinners": "normal",
        "fast_egg_hatch": "off",
        "fast_egg_make": "off",
        "rods_always_work": "off",
        "scaling_exp": "off",
        "exp_distribution": "gen2",
        "catch_exp": "off",
        "poison_flicker": "on",
        "turbo_button": "none",
        "low_hp_beep": "on",
        "time_of_day": "auto",
        "battle_move_stats": "off",
        "short_fanfares": "off",
        "dex_area_beep": "off",
        "skip_dex_registration": "off",
        "blind_trainers": "off",
        "guaranteed_catch": "off",
        "ap_item_notification": "popup_sound",
        "trainersanity_indication": "off",
        "more_uncaught_encounters": "off",
        "auto_hms": "off",
        "hms_require_teaching": "on",
        "local_item_notification": "text",
        "tracker_slot": 0,
        "music": "on",
        "battle_always_run": "off",
    }

    @override
    def verify(self, world: Type[World], player_name: str, plando_options: PlandoOptions) -> None:
        for key, value in self.value.items():
            if not isinstance(value, Hashable):
                raise OptionError(f"Invalid game option value for {key}: {value}")
            if key == "tracker_slot":
                if isinstance(value, bool) or not isinstance(value, int | str) or not str(value).isdigit() \
                        or not 0 <= int(value) <= 255:
                    raise OptionError(f"Invalid game option value for {key}: {value}. Must be 0-255.")
                continue
            setting = data.game_settings.get(key)
            if setting is None or key.startswith("_"):
                continue
            valid_values = list(setting.values)
            if key in ("text_frame", "time_of_day"):
                valid_values.append("random")
            if setting.normalize(value) not in valid_values:
                raise OptionError(f"Invalid game option value for {key}: {value}. "
                                  f"Valid values: {', '.join(valid_values)}")


class FieldMoveMenuOrder(OptionList):
    """
    Defines which order the entries of the Field Move Menu (accessible if hms_require_teaching is set to 'off') appear in.

    Provided values will appear on top of the menu in the given order.
    Omitted values will appear below in the following order: Cut, Fly, Surf, Strength, Flash, Whirlpool, Waterfall, Rock Smash, Headbutt, Dig, Teleport, Sweet Scent.
    Duplicates will be omitted.
    """
    display_name = "Field Move Menu Order"
    valid_keys = ["Cut", "Fly", "Surf", "Strength", "Flash", "Whirlpool", "Waterfall", "Rock Smash", "Headbutt",
                  "Dig", "Teleport", "Sweet Scent"]
    default = valid_keys

    def __init__(self, value):
        super(FieldMoveMenuOrder, self).__init__(value)
        self.value = list(dict.fromkeys(self.value))
        self.value += [key for key in self.valid_keys if key not in self.value]
        assert len(self.value) == len(self.valid_keys)

    def __bool__(self):
        return super(FieldMoveMenuOrder, self).__bool__() and self.value != self.default


class ExcludePostGoalLocations(DefaultOnToggle):
    """
    Excludes locations which require becoming champion when goal is becoming champion
    """
    display_name = "Exclude Post Goal Locations"


class RandomizeItemValues(Toggle):
    """
    Randomizes the base value of items, this affects sell price and can affect buy price depending on other options
    """
    display_name = "Randomize Item Values"


class MinimumItemValue(Range):
    """
    Sets the minimum value of items when Randomize Item Values is enabled
    """
    display_name = "Minimum Item Value"
    default = 0
    range_start = 0
    range_end = 10000


class MaximumItemValue(Range):
    """
    Sets the maximum value of items when Randomize Item Values is enabled
    """
    display_name = "Maximum Item Value"
    default = 10000
    range_start = 0
    range_end = 10000


class ItemValuePlando(OptionDict):
    """
    Specify the base value of individual items.
    This applies even when Randomize Item Values is off, and takes priority over randomized values.
    Values must be between 0 and 10000.

    A single value or a weighted dict of values can be provided per item:
    item_value_plando:
      Poke Ball: 150
      Rare Candy:
        5000: 50
        10000: 50
    """
    display_name = "Item Value Plando"
    valid_keys = set(item.label for item in data.items.values() if "INVALID" not in item.tags)

    def __init__(self, value):
        normalized = {}
        for k, v in sorted(value.items()):
            if isinstance(v, dict):
                normalized[k] = int(random.choices(list(v.keys()), weights=list(v.values()))[0])
            else:
                normalized[k] = int(v)
        super().__init__(normalized)

    def verify_keys(self) -> None:
        super().verify_keys()
        invalid_values = {v for v in self.value.values() if not 0 <= v <= 10000}
        if invalid_values:
            raise OptionError(
                f"Found out of range value(s) {', '.join(str(v) for v in sorted(invalid_values))} "
                f"in {self.display_name}. Values must be between 0 and 10000."
            )


class Grasssanity(Choice):
    """
    Adds Cutting grass tiles as locations, each one adds a Grass to the item pool, Grass smells good and sells for ¥1
    Long grass tiles in National Park must be Cut twice and as such contribute two locations

    - One Per Area: Selects a random grass tile in each Route or Area to be a location
    - Full: Every grass tile is a location

    WARNING: This option is dumb, it can add over 800 locations and over 800 useless filler items
    """
    display_name = "Grasssanity"
    default = 0
    option_off = 0
    option_one_per_area = 1
    option_full = 2


class DefaultPokedexMode(Choice):
    """
    Sets the default Pokedex mode
    """
    display_name = "Default Pokedex Mode"
    default = 0
    option_new = 0
    option_old = 1
    option_a_to_z = 2


class RequirePokegearForPhoneNumbers(DefaultOnToggle):
    """
    Sets whether the Pokegear is required to register trainer phone numbers and whether the Pokegear and Phone Card
    are required to receive calls

    The Pokegear and Phone Card will always be logically required for phone call locations
    """
    display_name = "Require Pokegear for Phone Numbers"


class TrainerPalette(TextChoice):
    """
    Sets the palette used for the player character.
    Can also be set to a hex color code (e.g. #FF8040) for a custom palette.
    """
    display_name = "Trainer Palette"
    default = 0
    option_vanilla = 0
    option_red = 1
    option_blue = 2
    option_green = 3
    option_brown = 4

    @classmethod
    def from_text(cls, text: str) -> "TrainerPalette":
        # Strip leading # if present, then check if it's a valid 6-char hex color
        cleaned = text.strip().lstrip("#")
        if len(cleaned) == 6:
            try:
                int(cleaned, 16)
                return cls(cleaned.upper())
            except ValueError:
                pass
        return super().from_text(text)


class ColoredItemBalls(Toggle):
    """
    Tints overworld item ball sprites by the AP classification of the item they hold:
    green for progression, blue for useful, red for filler, and a random one of the three
    for traps.
    Remote items are colored by their classification in the receiving slot's world.
    """
    display_name = "Colored Item Balls"


class ProgressiveRods(Toggle):
    """
    Sets whether fishing rods are always received in order (Old -> Good -> Super)
    """
    display_name = "Progressive Rods"


class PokemonCrystalDeathLink(DeathLink):
    __doc__ = DeathLink.__doc__ + "\n\n    In Pokemon Crystal, whiting out sends a death and receiving a death causes you to white out.\n\n    Being seen by a trainer when spinner heck or hell is enabled will send a deathlink."


class RandomizeEntrances(EnhancedOptionSet):
    """
    Categories of entrances to include in the entrance randomization pool.
    Leave empty (default) to disable entrance randomization.

    Categories:
    - Dungeon: Entrances to multi-floor areas with trainers/items (towers, caves, hideouts). Gyms excluded.
    - Dungeon Interior: Entrances between two interior regions of a dungeon (internal stairs/ladders/warps).
    - Gym: Entrances to gyms.
    - Gym Interior: Entrances between two interior regions of a gym (Blackthorn Gym and Saffron Gym).
    - Mart: Entrances to Pokemarts, department stores, and other shop-like buildings.
    - Mart Interior: Entrances between two interior regions of a department store (inter-floor stairs).
    - Building: Entrances to generic buildings.
    - Building Interior: Entrances between two interior regions of a building.
    - Gate: Entrances to route gates.
    - Pokecenter: Entrances to pokecenters.
    - Elevator: Entrances to elevators for each floor.
    - Pokemon League: Entrances involving Elite Four chambers.
    - One-Way: One-way entrances. Will not be shuffled with other entrances.

    _All includes all categories.
    _Random has a 50% chance to include each category not already included.
    """
    display_name = "Randomize Entrances"
    valid_keys = sorted(ENTRANCE_CATEGORIES)
    default = []


class MixEntrances(EnhancedOptionSet):
    """
    Categories that shuffle together in a single combined pool. Defaults to all
    categories (everything mixes). Any category removed from this set becomes
    its own isolated pool and shuffles only among itself.

    Has no effect on categories not also present in randomize_entrances.
    One-Ways are always isolated regardless of this setting.

    _All includes all categories (the default).
    """
    display_name = "Mix Entrances"
    valid_keys = sorted(ENTRANCE_CATEGORIES)
    default = sorted(ENTRANCE_CATEGORIES)


class CoupledEntrances(DefaultOnToggle):
    """
    If enabled, entrance randomization is coupled: if door A leads to location B,
    then the exit of location B leads back to door A. Recommended for navigation.
    If disabled, exits are randomized independently.

    Has no effect on one way entrances.
    """
    display_name = "Coupled Entrances"


class CrystalPlandoConnections(PlandoConnections):
    """
    Force specific entrance randomization pairings before randomization.
    Accepts friendly connection names (e.g. "Azalea Gym Entrance") or internal
    connection names of the form "REGION_A -> REGION_B" from entrance_data.json.

    The "entrance" is the door walked through. The "exit" is the connection at the
    arrival side: the player ends up on the far side of that door.

    Direction "both" forces the reverse pairing too; "entrance" forces only one direction.
    With coupled_entrances enabled every pairing is forced to "both", since coupling already
    makes the return trip mirror the way in.
    Requires randomize_entrances to include the relevant categories.

    Example (cafe door leads to the elevator room):
      plando_connections:
        - entrance: "Celadon Cafe Entrance"
          exit: "Celadon Dept. Store 1F Elevator Entrance"
          direction: both

    To pin an entrance to its vanilla destination, use the same connection name for
    both "entrance" and "exit":
      plando_connections:
        - entrance: "Silver Cave Entrance"
          exit: "Silver Cave Entrance"
          direction: both
    """
    entrances = set(data.entrance_connections.keys()) \
        | {friendly_entrance_name(name) for name in data.entrance_connections}
    exits = set(data.entrance_connections.keys()) \
        | {friendly_entrance_name(name) for name in data.entrance_connections}


@dataclass
class PokemonCrystalOptions(PerGameCommonOptions):
    goal: Goal
    vanilla_event_chains: VanillaEventChains
    johto_only: JohtoOnly
    victory_road_requirement: VictoryRoadRequirement
    victory_road_count: VictoryRoadCount
    elite_four_requirement: EliteFourRequirement
    elite_four_count: EliteFourCount
    red_requirement: RedRequirement
    red_count: RedCount
    mt_silver_requirement: MtSilverRequirement
    mt_silver_count: MtSilverCount
    radio_tower_requirement: RadioTowerRequirement
    radio_tower_count: RadioTowerCount
    route_44_access_requirement: Route44AccessRequirement
    route_44_access_count: Route44AccessCount
    magnet_train_access: MagnetTrainAccess
    route_23_restored: Route23Restored
    flooded_mine: FloodedMine
    randomize_starting_town: RandomizeStartingTown
    starting_town_blocklist: StartingTownBlocklist
    randomize_badges: RandomizeBadges
    randomize_hidden_items: RandomizeHiddenItems
    battle_tower_sanity: BattleTowerSanity
    battle_tower_progressive_tier_unlocks: BattleTowerProgressiveTierUnlocks
    require_itemfinder: RequireItemfinder
    item_pool_fill: ItemPoolFill
    add_missing_useful_items: AddMissingUsefulItems
    route_32_condition: Route32Condition
    dark_areas: DarkAreas
    victory_road_strength: VictoryRoadStrength
    route_22_access_requirement: Route22AccessRequirement
    route_22_access_count: Route22AccessCount
    red_gyarados_access: RedGyaradosAccess
    route_2_access: Route2Access
    route_3_access: Route3Access
    blackthorn_dark_cave_access: BlackthornDarkCaveAccess
    national_park_access: NationalParkAccess
    route_42_access: Route42Access
    mount_mortar_access: MountMortarAccess
    route_12_access: Route12Access
    ss_aqua_access: SSAquaAccess
    route_30_access: Route30Access
    route_30_battle: Route30Battle
    south_kanto_access: SouthKantoAccess
    south_kanto_condition: SouthKantoCondition
    johto_trainersanity: JohtoTrainersanity
    kanto_trainersanity: KantoTrainersanity
    rematchsanity: Rematchsanity
    kinda_early_surf: KindaEarlySurf
    randomize_wilds: RandomizeWilds
    shared_wild_encounters: SharedWildEncounters
    dexsanity: Dexsanity
    dexsanity_starters: DexsanityStarters
    dexsanity_logic: DexsanityLogic
    dexcountsanity: Dexcountsanity
    dexcountsanity_step: DexcountsanityStep
    dexcountsanity_leniency: DexcountsanityLeniency
    wild_encounter_methods_required: WildEncounterMethodsRequired
    enforce_wild_encounter_methods_logic: EnforceWildEncounterMethodsLogic
    trades_required: TradesRequired
    randomize_lucky_number_show: RandomizeLuckyNumberShow
    static_pokemon_required: StaticPokemonRequired
    evolution_methods_required: EvolutionMethodsRequired
    evolution_gym_levels: EvolutionGymLevels
    breeding_methods_required: BreedingMethodsRequired
    enforce_breeding_methods_logic: EnforceBreedingMethodsLogic
    shopsanity: Shopsanity
    shopsanity_prices: ShopsanityPrices
    shopsanity_minimum_price: MinimumShopsanityPrice
    shopsanity_maximum_price: MaximumShopsanityPrice
    provide_shop_hints: ProvideShopHints
    shopsanity_restrict_rare_candies: ShopsanityRestrictRareCandies
    shopsanity_x_items: ShopsanityXItems
    randomize_pokegear: RandomizePokegear
    randomize_berry_trees: RandomizeBerryTrees
    randomize_pokedex: RandomizePokedex
    randomize_pokemon_requests: RandomizePokemonRequests
    pokemon_request_logic: PokemonRequestLogic
    randomize_phone_call_items: RandomizePhoneCallItems
    momsanity: Momsanity
    phone_call_mode: PhoneCallMode
    randomize_fly_unlocks: RandomizeFlyUnlocks
    randomize_bug_catching_contest: RandomizeBugCatchingContest
    randomize_starters: RandomizeStarters
    starter_blocklist: StarterBlocklist
    starters_bst_average: StarterBST
    wild_encounter_blocklist: WildEncounterBlocklist
    wild_match_mode: WildMatchMode
    encounter_grouping: EncounterGrouping
    time_of_day_encounters: TimeOfDayEncounters
    unlockable_time_of_day: UnlockableTimeOfDay
    force_fully_evolved: ForceFullyEvolved
    encounter_slot_distribution: EncounterSlotDistribution
    randomize_static_pokemon: RandomizeStaticPokemon
    static_blocklist: StaticBlocklist
    unique_static_pokemon: UniqueStaticPokemon
    level_scaling: LevelScaling
    level_curve: LevelCurve
    level_curve_min_level: LevelCurveMinLevel
    level_curve_max_level: LevelCurveMaxLevel
    lock_kanto_gyms: LockKantoGyms
    randomize_trades: RandomizeTrades
    randomize_trainer_parties: RandomizeTrainerParties
    trainer_party_blocklist: TrainerPartyBlocklist
    boost_trainers: BoostTrainerPokemonLevels
    trainer_level_boost: TrainerLevelBoostValue
    randomize_learnsets: RandomizeLearnsets
    metronome_only: MetronomeOnly
    learnset_type_bias: LearnsetTypeBias
    randomize_moves: RandomizeMoves
    randomize_type_chart: RandomizeTypeChart
    physical_special_split: PhysicalSpecialSplit
    randomize_tm_moves: RandomizeTMMoves
    tm_plando: TMPlando
    tm_same_type_compatibility: TMSameTypeCompatibility
    tm_other_type_compatibility: TMOtherTypeCompatibility
    hm_same_type_compatibility: HMSameTypeCompatibility
    hm_other_type_compatibility: HMOtherTypeCompatibility
    hm_compatibility_override: HMCompatibilityOverride
    hm_power_cap: HMPowerCap
    field_moves_always_usable: FieldMovesAlwaysUsable
    randomize_base_stats: RandomizeBaseStats
    base_stats_multiples_of_five: BaseStatsMultiplesOfFive
    base_stats_evolution_mode: BaseStatsEvolutionMode
    randomize_types: RandomizeTypes
    shared_primary_type: SharedPrimaryType
    randomize_evolution: RandomizeEvolution
    convergent_evolution: ConvergentEvolution
    evolution_blocklist: EvolutionBlocklist
    maximum_evolution_level: MaximumEvolutionLevel
    randomize_breeding: RandomizeBreeding
    breeding_blocklist: BreedingBlocklist
    modify_palettes: ModifyPalettes
    randomize_music: RandomizeMusic
    move_blocklist: MoveBlocklist
    tm_blocklist: TMBlocklist
    free_fly_location: FreeFlyLocation
    free_fly_blocklist: FlyLocationBlocklist
    early_fly: EarlyFly
    require_flash: RequireFlash
    hm_badge_requirements: HMBadgeRequirements
    remove_badge_requirement: RemoveBadgeRequirement
    remove_ilex_cut_tree: RemoveIlexCutTree
    saffron_gatehouse_tea: SaffronGatehouseTea
    east_west_underground: EastWestUnderground
    undergrounds_require_power: UndergroundsRequirePower
    reusable_tms: ReusableTMs
    minimum_catch_rate: MinimumCatchRate
    skip_elite_four: SkipEliteFour
    lance_requires_elite_four: LanceRequiresEliteFour
    better_marts: BetterMarts
    build_a_mart: BuildAMart
    growth_rates: GrowthRates
    experience_modifier: ExpModifier
    exp_share_type: ExpShareType
    starting_money: StartingMoney
    all_pokemon_seen: AllPokemonSeen
    filler_trap_percentage: TrapWeight
    trap_weights: TrapWeights
    remote_items: RemoteItems
    game_options: GameOptions
    field_move_menu_order: FieldMoveMenuOrder
    trainer_gender: TrainerGender
    trainer_name: TrainerName
    rival_name: RivalName
    start_time: StartTime
    enable_mischief: EnableMischief
    custom_mischief_pool: CustomMischiefPool
    mischief_lower_bound: MischiefLowerBound
    mischief_upper_bound: MischiefUpperBound
    start_inventory_from_pool: StartInventoryPool
    death_link: PokemonCrystalDeathLink
    always_unlock_fly_destinations: AlwaysUnlockFly
    exclude_post_goal_locations: ExcludePostGoalLocations
    grasssanity: Grasssanity
    default_pokedex_mode: DefaultPokedexMode
    trap_link: TrapLink
    wonder_trading: WonderTrading
    require_pokegear_for_phone_numbers: RequirePokegearForPhoneNumbers
    trainer_palette: TrainerPalette
    colored_item_balls: ColoredItemBalls
    progressive_rods: ProgressiveRods
    randomize_item_values: RandomizeItemValues
    minimum_item_value: MinimumItemValue
    maximum_item_value: MaximumItemValue
    item_value_plando: ItemValuePlando
    modernise_moves_generation: ModerniseMovesGeneration
    modernise_moves_type: ModerniseMovesType
    randomize_entrances: RandomizeEntrances
    mix_entrances: MixEntrances
    coupled_entrances: CoupledEntrances
    plando_connections: CrystalPlandoConnections
    randomize_fly_destinations: RandomizeFlyDestinations
    fly_destination_blocklist: FlyDestinationBlocklist
    fly_destination_plando: FlyDestinationPlando


OPTION_GROUPS = [
    OptionGroup(
        "Map",
        [RandomizeStartingTown,
         StartingTownBlocklist,
         JohtoOnly,
         RandomizeEntrances,
         MixEntrances,
         CoupledEntrances,
         RandomizeFlyDestinations,
         FlyDestinationBlocklist,
         FlyDestinationPlando,
         CrystalPlandoConnections,
         FloodedMine,
         Route23Restored]
    ),
    OptionGroup(
        "Roadblocks",
        [VictoryRoadRequirement, VictoryRoadCount,
         VictoryRoadStrength,
         EliteFourRequirement, EliteFourCount,
         LanceRequiresEliteFour,
         RedRequirement, RedCount,
         DarkAreas,
         MagnetTrainAccess,
         SSAquaAccess,
         VanillaEventChains]
    ),
    OptionGroup(
        "Johto Roadblocks",
        [MtSilverRequirement, MtSilverCount,
         RadioTowerRequirement, RadioTowerCount,
         Route44AccessRequirement, Route44AccessCount,
         Route32Condition,
         Route42Access,
         MountMortarAccess,
         RedGyaradosAccess,
         BlackthornDarkCaveAccess,
         NationalParkAccess,
         RemoveIlexCutTree,
         Route30Access,
         Route30Battle]
    ),
    OptionGroup(
        "Kanto Roadblocks",
        [Route22AccessRequirement, Route22AccessCount,
         Route2Access,
         Route3Access,
         SaffronGatehouseTea,
         UndergroundsRequirePower,
         EastWestUnderground,
         Route12Access,
         SouthKantoAccess,
         SouthKantoCondition]
    ),
    OptionGroup(
        "Items",
        [RandomizeBadges,
         RandomizePokegear,
         RandomizeHiddenItems,
         RandomizeBerryTrees,
         RandomizePokedex,
         RandomizePokemonRequests,
         RandomizeFlyUnlocks,
         RandomizeBugCatchingContest,
         RandomizePhoneCallItems,
         Momsanity,
         RequireItemfinder,
         RemoteItems,
         ItemPoolFill,
         AddMissingUsefulItems,
         ExcludePostGoalLocations,
         Grasssanity,
         RandomizeItemValues,
         MinimumItemValue,
         MaximumItemValue,
         ItemValuePlando]
    ),
    OptionGroup(
        "Shopsanity",
        [Shopsanity,
         ShopsanityPrices,
         MinimumShopsanityPrice,
         MaximumShopsanityPrice,
         ProvideShopHints,
         ShopsanityRestrictRareCandies,
         ShopsanityXItems]
    ),
    OptionGroup(
        "HMs",
        [HMSameTypeCompatibility,
         HMOtherTypeCompatibility,
         HMCompatibilityOverride,
         HMBadgeRequirements,
         RemoveBadgeRequirement,
         RequireFlash,
         FieldMovesAlwaysUsable,
         FreeFlyLocation,
         FlyLocationBlocklist,
         EarlyFly]
    ),
    OptionGroup(
        "Pokemon",
        [RandomizeWilds,
         SharedWildEncounters,
         WildEncounterBlocklist,
         WildMatchMode,
         TimeOfDayEncounters,
         RandomizeStaticPokemon,
         StaticBlocklist,
         UniqueStaticPokemon,
         RandomizeBaseStats,
         BaseStatsMultiplesOfFive,
         BaseStatsEvolutionMode,
         RandomizeTypes,
         SharedPrimaryType,
         RandomizeEvolution,
         ConvergentEvolution,
         EvolutionBlocklist,
         MaximumEvolutionLevel,
         RandomizeBreeding,
         BreedingBlocklist,
         RandomizeTrades,
         EncounterGrouping,
         UnlockableTimeOfDay,
         EncounterSlotDistribution]
    ),
    OptionGroup(
        "Starters",
        [RandomizeStarters,
         StarterBST,
         StarterBlocklist]
    ),
    OptionGroup(
        "Moves",
        [RandomizeLearnsets,
         LearnsetTypeBias,
         MetronomeOnly,
         RandomizeMoves,
         RandomizeTypeChart,
         PhysicalSpecialSplit,
         HMPowerCap,
         RandomizeTMMoves,
         TMPlando,
         TMSameTypeCompatibility,
         TMOtherTypeCompatibility,
         ReusableTMs,
         MoveBlocklist,
         TMBlocklist,
         ModerniseMovesGeneration,
         ModerniseMovesType]
    ),
    OptionGroup(
        "Trainers",
        [RandomizeTrainerParties,
         TrainerPartyBlocklist,
         BoostTrainerPokemonLevels,
         TrainerLevelBoostValue,
         ForceFullyEvolved]
    ),
    OptionGroup(
        "Dexsanities",
        [Dexsanity,
         DexsanityLogic,
         Dexcountsanity,
         DexcountsanityStep,
         DexcountsanityLeniency,
         DexsanityStarters]
    ),
    OptionGroup(
        "Trainersanity",
        [JohtoTrainersanity,
         KantoTrainersanity,
         Rematchsanity]
    ),
    OptionGroup(
        "Battle Tower",
        [BattleTowerSanity,
         BattleTowerProgressiveTierUnlocks]
    ),
    OptionGroup(
        "Pokemon Logic",
        [WildEncounterMethodsRequired,
         EnforceWildEncounterMethodsLogic,
         StaticPokemonRequired,
         TradesRequired,
         RandomizeLuckyNumberShow,
         EvolutionMethodsRequired,
         EvolutionGymLevels,
         BreedingMethodsRequired,
         EnforceBreedingMethodsLogic,
         PokemonRequestLogic]
    ),
    OptionGroup(
        "Traps",
        [TrapWeight,
         TrapWeights,
         TrapLink]
    ),
    OptionGroup(
        "Quality of Life",
        [GameOptions,
         LevelScaling,
         LevelCurve,
         LevelCurveMinLevel,
         LevelCurveMaxLevel,
         LockKantoGyms,
         AllPokemonSeen,
         StartingMoney,
         BetterMarts,
         BuildAMart,
         GrowthRates,
         ExpModifier,
         ExpShareType,
         SkipEliteFour,
         MinimumCatchRate,
         AlwaysUnlockFly,
         FieldMoveMenuOrder,
         DefaultPokedexMode,
         ProgressiveRods,
         RequirePokegearForPhoneNumbers,
         PhoneCallMode,
         WonderTrading,
         PokemonCrystalDeathLink]
    ),
    OptionGroup(
        "Intro Presets",
        [TrainerGender,
         TrainerName,
         RivalName,
         StartTime]
    ),
    OptionGroup(
        "Cosmetic",
        [ModifyPalettes,
         RandomizeMusic,
         TrainerPalette,
         ColoredItemBalls]
    ),
    OptionGroup(
        ":3",
        [EnableMischief,
         CustomMischiefPool,
         MischiefLowerBound,
         MischiefUpperBound],
        False
    )
]

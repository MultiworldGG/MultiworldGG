import math
from typing import List, Union, ClassVar, Any, TYPE_CHECKING
import settings
from BaseClasses import Tutorial, Region, Location, LocationProgressType, Item, ItemClassification, Entrance
from Fill import fill_restrictive, FillError
from worlds.AutoWorld import WebWorld, World
from entrance_rando import randomize_entrances, bake_target_group_lookup, EntranceRandomizationError, disconnect_entrance_for_randomization
from .tracker.tracker_util import get_hidden_map_icons

from .Util import *
from .Options import *

from .data import LOCATIONS_DATA
from .data.Items import ITEMS
from .data.Constants import *
from .data.ModelLookups import all_lookups
from .data.Regions import REGIONS
from .data.LogicPredicates import *
from .data.Entrances import (ENTRANCES, entrance_id_to_region, entrance_id_to_entrance,
                             location_event_lookup, goal_event_lookup, boss_events, cargo_events)

from .Client import SpiritTracksClient  # Unused, but required to register with BizHawkClient
from .Subclasses import EntranceGroups, OPPOSITE_ENTRANCE_GROUPS, decode_recursive, decode_entrance_groups, \
    dungeon_to_enum

try:  # Backwards compatibility yay
    from rule_builder.cached_world import CachedRuleBuilderWorld as WorldParent
    from .LogicRB import create_connections
    # raise ModuleNotFoundError
except ModuleNotFoundError:
    print(f"Spirit Tracks is using legacy logic")
    WorldParent = World
    from .Logic import create_connections

if TYPE_CHECKING:
    from .Subclasses import STTransition


try:
    DEPRIORITIZED_SKIP_BALANCING_FALLBACK = ItemClassification.progression_deprioritized_skip_balancing
    DEPRIORITIZED_FALLBACK = ItemClassification.progression_deprioritized
except AttributeError:
    DEPRIORITIZED_SKIP_BALANCING_FALLBACK = ItemClassification.progression_skip_balancing
    DEPRIORITIZED_FALLBACK = ItemClassification.progression

# Adds a consistent count of items to pool, independent of how many are from locations
def add_items_from_filler(item_pool_dict: dict, filler_item_count: int, item: str, count: int):
    count_addable = count-item_pool_dict.setdefault(item,0)
    if filler_item_count >= count_addable:
        item_pool_dict[item] += count_addable
        filler_item_count = filler_item_count - count_addable
    else:
        item_pool_dict[item] += filler_item_count
        filler_item_count = 0
        print(f"Ran out of filler items! at {item}")

    return item_pool_dict, filler_item_count

class SpiritTracksWeb(WebWorld):
    theme = "grassFlowers"
    game = "Spirit Tracks"
    display_name = "The Legend of Zelda: Spirit Tracks"
    setup_en = Tutorial(
        tutorial_name="Multiworld Setup Guide",
        description="A guide to setting up Spirit Tracks for MultiworldGG on your computer.",
        language="English",
        file_name="setup.md",
        link="setup/en",
        authors=["DayKat", "Carrotinator"]
    )
    tricks_and_skips_en = Tutorial(
        tutorial_name="Tricks and Skips",
        description="A list of tricks and skips with their logic difficulty, and video links when available.",
        language="English",
        file_name="tricks_and_skips.md",
        link="tricks_and_skips/en",
        authors=["Carrotinator"]
    )

    tutorials = [setup_en]
    option_groups = st_option_groups

class SpiritTracksSettings(settings.Group):
    class STTrainSpeed(list[int]):
        """
        Train speed for each of the 4 gears, from lowest (reverse) to highest.
        defaults are -143, 0, 115, 193
        """
    class STTrainInstantStation(str):
        """
        Allows entering stations immediately on the stop gear, no matter your speed.
        """
    class STTrainSnapSpeed(str):
        """
        The train will instantly switch to the new speed when changing gears, no acceleration required.
        Does not apply to your stop gear.
        """
    class STUTConnectMaps(str):
        """
        UT will account for unlocked map warps with /get_logical_path.
        Turn off in case you want to see the normal path.
        """

    train_speed: STTrainSpeed = STTrainSpeed([-143, 0, 115, 193])
    train_snap_speed: Union[STTrainSnapSpeed, bool] = True
    train_quick_station: Union[STTrainInstantStation, bool] = True
    ut_connect_map_warps: Union[STUTConnectMaps, bool] = True

dev_prints = False

class SpiritTracksItem(Item):
    game = "Spirit Tracks"

def map_func(i):
    return i if i else 0

class SpiritTracksWorld(WorldParent):
    """
    The Legend of Zelda: Spirit Tracks is the train bound handheld sequel to Phantom Hourglass.
    """
    game = "Spirit Tracks"
    options_dataclass = SpiritTracksOptions
    options: SpiritTracksOptions
    settings: ClassVar[SpiritTracksSettings]
    required_client_version = (0, 6, 7)
    web = SpiritTracksWeb()
    topology_present = True

    settings_key = "tloz_st_options"

    # UT Attributes
    location_name_to_id = build_location_name_to_id_dict()
    item_name_to_id = build_item_name_to_id_dict()
    item_name_groups = ITEM_GROUPS
    location_name_groups = LOCATION_GROUPS
    origin_region_name = "menu"
    glitches_item_name = "_UT_Glitched_Logic"
    ut_can_gen_without_yaml = True
    tracker_world = {"map_page_folder": "tracker",
                     "map_page_maps": "maps/maps.json",
                     "map_page_settings_key": "{slot}_{team}_UT_MAP",
                     "map_page_locations": ["locations/overworld.json",
                                            "entrances/entrances.json"],
                     "map_page_index": map_func}
    found_entrances_datastorage_key = ["st_checked_entrances_{player}_{team}",
                                       "st_traversed_entrances_{player}_{team}",
                                       "st_redisconnected_entrances_{player}_{team}",
                                       "st_visited_scenes_{player}_{team}"]

    # Rule builder attributes
    item_mapping = ITEM_MAPPING

    def __init__(self, multiworld, player):
        super().__init__(multiworld, player)

        self.pre_fill_items: List[SpiritTracksItem] = []
        self.required_boss_locs = []
        self.non_required_dungeons = []
        self.non_required_sections = []
        self.dungeon_name_groups = {}
        self.locations_to_exclude = set()
        self.ut_locations_to_exclude = set()
        self.extra_filler_items = []
        self.excluded_dungeons = []
        self.active_rabbit_locations: list[str] = []
        self.rabbit_counts: list[int] = []
        self.rabbit_item_dict: dict[str, int] = {}
        self.rabbit_realm_items: dict[str, dict[str, int]] = {"Grass": {}, "Snow": {}}
        self.item_mapping_collect: dict[str, tuple[str, int]] = {}

        self.ut_checked_entrances: set[int] = set()
        self.ut_traversed_entrances: set[int] = set()
        self.ut_redisconnected_entrances: set[int] = set()
        self.ut_visited_scenes: set[int] = set()
        self.ut_pairings = {}
        self.ut_events = []
        self.is_ut = getattr(self.multiworld, "generation_is_fake", False)

        self.ut_map_page_hidden_entrances = {}
        self.ut_map_page_hidden_locations = {}

        self.er_placement_state = None
        self.valid_entrances: list["Entrance"] = []
        self.plando_pairings: dict[int, int] = {}  # int: int pairing
        self.tower_pairings = []  # zip object of entrance strings
        self.tower_section_lookup = {i:i for i in range(1, 7)}  # tower section lookup for logic
        self.exclude_tos_5 = 0
        self.shuffled_bosses: dict[str, str] = {}
        self.shuffled_dungeon_lookup: dict[str, str] = {}
        self.near_dungeon_lookup: dict[str, str] = {}  # loc: dung

        self.stamp_items = []
        self.stamp_pack_order = []
        self.model_lookup = {}
        self.sections_included: int = 6
        self.tears_included_big: int = 6
        self.tears_included_small: int = 16
        self.required_rupees = 0
        self.track_items = []
        self.raw_track_items = []

        self.starting_entrance: str = "Niko's House Exit"


    def generate_early(self):
        re_gen_passthrough = getattr(self.multiworld, "re_gen_passthrough", {})
        if re_gen_passthrough and self.game in re_gen_passthrough:
            # Get the passed through slot data from the real generation
            slot_data: dict[str, Any] = re_gen_passthrough[self.game]
            print(slot_data)
            # slot_options: dict[str, Any] = slot_data.get("options", {})
            # Set all your options here instead of getting them from the yaml
            for key, value in slot_data.items():
                opt = getattr(self.options, key, None)
                if opt is not None:
                    # You can also set .value directly but that won't work if you have OptionSets
                    setattr(self.options, key, opt.from_any(value))
            lookup = build_rabbit_location_id_to_name_dict()
            self.active_rabbit_locations = [lookup[i] for i in slot_data["active_rabbit_locs"]]
            self.required_boss_locs = [self.location_id_to_name[i] for i in slot_data["required_boss_locs"]]
            self.ut_pairings = slot_data["er_pairings"]
            self.tower_section_lookup = {int(k): v for k, v in slot_data["tower_section_lookup"].items()}
            self.non_required_dungeons = [d for d in DUNGEON_NAMES[2:] if
                                          DUNGEON_TO_BOSS_ITEM_LOCATION[d] not in self.required_boss_locs]
            self.pick_ut_events()
            self.ut_map_page_hidden_locations, self.ut_map_page_hidden_entrances = get_hidden_map_icons(self)
            self.starting_entrance = slot_data["starting_entrance"]
            self.exclude_tos_5 = slot_data["exclude_tos_5"]
            self.non_required_sections = [s for s in range(1, 7) if DUNGEON_TO_BOSS_ITEM_LOCATION[f"ToS {s}"] not in self.required_boss_locs]
        else:
            self.choose_starting_entrance()
            self.track_items = self.choose_track_items()
            self.choose_starting_tracks()

            self.required_boss_locs = self.pick_required_dungeons()
            self.non_required_sections = [s for s in range(1, 7) if DUNGEON_TO_BOSS_ITEM_LOCATION[f"ToS {s}"] not in self.required_boss_locs]
            # db_list = [(s, DUNGEON_TO_BOSS_ITEM_LOCATION[f"ToS {s}"], DUNGEON_TO_BOSS_ITEM_LOCATION[f"ToS {s}"] not in self.required_boss_locs) for s in range(1, 7)]
            # print(f"Req dungs {self.required_boss_locs} => {self.non_required_sections} {db_list}")
            if self.options.exclude_sections == "remove":
                self.sections_included = 6 - len(self.non_required_sections)
                self.tears_included_small = min(self.sections_included, 5)*3+1
                self.tears_included_big = min(self.sections_included, 5)+1
            # print(f"Required Dungeons: {self.required_boss_locs}")
            self.restrict_non_local_items()
            self.options.compass_shard_count.value = min(self.options.compass_shard_count.value, self.options.compass_shard_total.value)
            self.active_rabbit_locations = self.choose_rabbit_locations()
            self.rabbit_item_dict = self.choose_rabbit_items()
            self.choose_stamp_items()
            if self.options.shuffle_portals.value and self.options.portal_behavior.value == 2:
                self.options.portal_behavior.value = 1
            if self.options.shuffle_stations.value:  # Don't want to deal with this yet
                self.options.tos_unlock_base_item.value = 0
            # print(f"Rabbit items: {self.rabbit_item_dict}")
            if "all" in self.options.entrance_directionality.value:
                self.options.entrance_directionality.value = set(self.options.entrance_directionality.valid_keys)
            self.plando_tos_sections()
            # print(f"Tower Sections: {self.tower_section_lookup}")
            # Keyrings don't work with vanilla key locations
            if self.options.keysanity.value == 0:
                self.options.keyrings.value = min(self.options.keyrings.value, 1)
            if self.options.randomize_boss_keys.value <= 0:
                self.options.big_keyrings.value = 0
            if self.options.keyrings.value > 1 and self.options.big_keyrings and self.options.randomize_boss_keys > 0:
                self.options.randomize_boss_keys.value = self.options.keysanity.value

            # Starting Train
            # Tear conditions
            if self.options.randomize_tears.value <= 0:  # Vanilla/no tears
                self.options.tear_size.value = 0  # force small tears
                self.options.tear_sections.value = 0  # force per-section grouping when vanilla
            if self.options.tear_sections.value == 0:
                self.options.spirit_weapons.value = 0  # no spirit weapons if not progressive/all sections
            if self.options.tear_sections.value > 0 and self.options.randomize_tears == "in_own_section":
                self.options.randomize_tears.value = 2  # all sections/progressive can't be in own section, make in_tos
            if len(self.non_required_sections) == 6 and self.options.exclude_sections and self.options.randomize_tears.value not in [3, 0]:
                self.options.spirit_weapons.value = 0

            if self.tower_pairings:
                tos_summit_section = [EXIT_TO_TOS_SECTION[ex] for en, ex in self.tower_pairings
                                      if en == 'Tower of Spirits Summit Enter Altar'][0]
                tos_summit_boss = DUNGEON_TO_BOSS_ITEM_LOCATION[f"ToS {tos_summit_section}"]
            else:
                tos_summit_boss = "ToS 24F Final Chest"
            if all([
                self.options.exclude_sections.value,
                len(self.non_required_sections) == 5,
                self.options.randomize_tears.value in [1, 2],
                self.options.spirit_weapons.value,
                tos_summit_boss in self.required_boss_locs
            ]):
                self.options.spirit_weapons.value = 0
                # print(f"ToS Summit needs final spirit weapon. Turning off spirit weapons.")

            if self.options.starting_train == "random_train":
                self.options.starting_train.value = self.random.randint(0, 7)
            if "all" in self.options.shopsanity.value:
                self.options.shopsanity.value = self.options.shopsanity.valid_keys

            self.non_required_dungeons = [d for d in DUNGEON_NAMES[2:] if
                                          DUNGEON_TO_BOSS_ITEM_LOCATION[d] not in self.required_boss_locs]

        self.create_item_mappings()
        # print(f"non-reqs {self.non_required_dungeons} & {self.non_required_sections}/{self.required_boss_locs}")
        if 5 in self.non_required_sections and self.options.exclude_sections:
            self.exclude_tos_5 = 1
        self.required_rupees = self.get_required_rupees()

    def choose_starting_entrance(self):
        starting_entrances = self.options.randomize_start.value

        if "niko" in starting_entrances:
            starting_entrances.remove("niko")
            starting_entrances.add("Niko's House Exit")
        if "tos" in starting_entrances:
            starting_entrances.remove("tos")
            starting_entrances.update(["Tower of Spirits to Forest Realm", "Tower of Spirits to Snow Realm",
                                       "Tower of Spirits to Ocean Realm", "Tower of Spirits to Fire Realm",])
        if "towns" in starting_entrances:
            starting_entrances.remove("towns")
            starting_entrances.update(["Outset Board Train", "Mayscore Board Train",
                                       "Castle Town Board Train", "Anouki Village Board Train",
                                       "Papuzia Board Train", "Goron Village Board Train"])

        if "stations" in starting_entrances:
            stations = {n: e for n, e in ENTRANCES.items() if
                        e.direction == EntranceGroups.DOWN and e.category_group == EntranceGroups.STATION}
            starting_entrances.remove("stations")
            starting_entrances.update({s for s in stations})

        self.starting_entrance = self.random.choice(list(starting_entrances))
        # print(f"Starting entrance: {self.starting_entrance}")

    def plando_tos_sections(self):
        """Plando ToS Shuffle early so we can use the ordering in logic"""
        if not self.options.shuffle_tos_sections:
            if self.options.exclude_sections == "remove":
                # print(self.non_required_sections)
                sections = [s for s in range(1, 7) if s not in self.non_required_sections]
                self.tower_section_lookup = {s: i for i, s in enumerate(sections, start=1)}
                self.tower_section_lookup |= {s: 6 for s in self.non_required_sections}
                # print(self.tower_section_lookup)
            return
        elif self.options.shuffle_tos_sections.value > 1:
            # Randomly choose section lookup when sections are in mixed pools
            if self.options.exclude_sections == "remove":
                section_order = [s for s in range(1, 7) if s not in self.non_required_sections]
            else:
                section_order = list(range(1, 7))
            self.random.shuffle(section_order)
            self.tower_section_lookup = {r: s for r, s in zip(range(1, 7), section_order)}
            self.tower_section_lookup |= {s: 6 for s in range(1, 7) if s not in self.tower_section_lookup}
            return

        # Sophisticated shuffle to avoid loops
        entrances = list(ENTRANCE_TO_TOS_ORDER.keys())
        exits = list(EXIT_TO_TOS_SECTION.keys()) + ["ToS Summit Lower Exit"]
        banned_connections = {"Tower of Spirits Exit Staven": ["ToS 18F Exit"],
                              "Tower of Spirits Summit Enter Altar": ["ToS Summit Lower Exit"]}
        self.random.shuffle(exits)
        for entrance in entrances:
            if exits[0] in banned_connections.get(entrance, []):
                self.tower_pairings.append((entrance, exits.pop(1)))
            else:
                self.tower_pairings.append((entrance, exits.pop(0)))
            if entrance == "Tower of Spirits Exit Staven" and self.tower_pairings[0][1] == "ToS Summit Lower Exit":
                banned_connections["Tower of Spirits Summit Enter Altar"].append("ToS 18F Exit")
        self.plando_pairings |= {ENTRANCES[e1].id: ENTRANCES[e2].id for e1, e2 in self.tower_pairings}
        self.plando_pairings |= {e2: e1 for e1, e2 in self.plando_pairings.items()}

        # Get lookup table for logic progressive tear sections
        sort_filter = {}
        for pair, entr in self.tower_pairings:
            if entr in EXIT_TO_TOS_SECTION and pair in ENTRANCE_TO_TOS_ORDER:
                sort_filter[EXIT_TO_TOS_SECTION[entr]] = ENTRANCE_TO_TOS_ORDER[pair]

        to_sort = [i for i in sort_filter]
        old_sort = [i for i in sort_filter]
        add_excluded = []
        if self.options.exclude_sections == "remove":
            required = set(range(1, 7))-set(self.non_required_sections)
            add_excluded = self.non_required_sections
            for s in self.non_required_sections:
                to_sort.remove(s)

        to_sort.sort(key=lambda i: sort_filter[i])
        self.tower_section_lookup = {section: i + 1 for i, section in enumerate(to_sort)}
        self.tower_section_lookup |= {i: 6 for i in add_excluded}
        # print(f"Section lookup: {self.tower_section_lookup}")

    def get_required_rupees(self):
        required_rupees = 0
        options = self.options
        if "uniques" in options.shopsanity.value: required_rupees += 4500
        if "treasure" in options.shopsanity.value: required_rupees += 2400
        if "potions" in options.shopsanity.value: required_rupees += 1400
        if "shields" in options.shopsanity.value: required_rupees += 610
        if "postcards" in options.shopsanity.value: required_rupees += 500
        if "ammo" in options.shopsanity.value: required_rupees += 500
        if options.randomize_cargo == "vanilla":
            required_rupees += 650
        elif options.randomize_cargo:
            required_rupees += 550
        # print(f"Required Rupees (gen) {required_rupees}")
        return required_rupees

    def pick_ut_events(self):
        events = ["EVENT: Trading Post Give Regal Ring to Linebeck"]

        if self.options.goal.value == -1 and self.options.endgame_scope == "enter_dark_realm":
            events.append("GOAL: Enter Dark Realm")
        else:
            events.append(goal_event_lookup[self.options.goal.value])

        if self.options.randomize_cargo.value > 0:
            events += [
                "EVENT: Mountain Altar Visit Kagoron",
                "EVENT: Goron Village Bring Ice to Kagoron"]

        if self.options.goal == "defeat_malladus" and self.options.dark_realm_access in ["dungeons", "both"]:
            if self.options.dungeon_hints or not self.options.require_specific_dungeons:
                events += [location_event_lookup[loc] for loc in self.required_boss_locs]
            else:
                events += ["EVENT: Defeat Stagnox", "EVENT: Defeat Fraaz", "EVENT: Defeat Cactops", "EVENT: Defeat Vulcano", "EVENT: Defeat Capbone"]
                if self.options.tos_dungeon_options == "final_section":
                    events += ["EVENT: Defeat Staven"]
                elif self.options.tos_dungeon_options == "all_sections":
                    events += ["EVENT: Reach ToS 3F", "EVENT: Reach ToS 7F", "EVENT: Reach ToS 12F", "EVENT: Reach ToS 17F", "EVENT: Defeat Staven", "EVENT: Reach ToS 24F"]

        if not self.options.open_blue_warps.value and self.options.shuffle_warps.value and "warps" in self.options.extra_events.value:
            events += [
                "EVENT: Desert Temple Open Blue Warp",
                "EVENT: Mountain Temple Open Blue Warp",
                "EVENT: Marine Temple Open Blue Warp",
                "EVENT: Blizzard Temple Open Blue Warp",
                "EVENT: Wooded Temple Open Blue Warp"
            ]
        if self.options.shuffle_houses.value and self.options.randomize_passengers.value:
            events += ["EVENT: Anouki Village Drop Off Goron",
                       "EVENT: Outset Drop Off Ferrus"]

        if self.options.randomize_passengers.value and self.options.shuffle_caves.value:
            events += ["EVENT: Island Sanctuary Drop Off Carben"]

        if self.options.shuffle_portals.value and self.options.portal_behavior.value == 0 and "portals" in self.options.extra_events.value:
            events += [
                "EVENT: Unlock Forest Realm Cave Portal",
                "EVENT: Unlock Snow Bridge Portal",
                "EVENT: Unlock Anouki Village Portal",
                "EVENT: Unlock Icy Spring Portal",
                "EVENT: Unlock Forest Realm SE Portal",
                "EVENT: Unlock Ocean Portal",
                "EVENT: Unlock Desert Temple Portal",
                "EVENT: Unlock Sand Connection Portal"
            ]
        if self.options.shuffle_caves.value or self.options.shuffle_disorientation.value:
            events += ["EVENT: Disorientation Maze Find Chest"]

        if self.options.randomize_passengers.value and self.options.passenger_pickup.value == 1 and "visits" in self.options.extra_events.value:
            events += [
                "EVENT: Visit Outset",
                "EVENT: Visit Castle Town",
                "EVENT: Visit Rabbit Haven",
                "EVENT: Visit Anouki Village",
                "EVENT: Visit Icy Spring",
                "EVENT: Visit Trading Post",
                "EVENT: Visit Papuzia Village",
                "EVENT: Visit Marine Temple",
                "EVENT: Visit Goron Village",
            ]
        if self.options.randomize_stamps.value in [1, 4] and "stamps" in self.options.extra_events.value:
            events += [
                "EVENT: Outset Stamp Station",
                "EVENT: Mayscore Forest Stamp Station",
                "EVENT: Castle Town Stamp Station",
                "EVENT: Woodland Sanctuary Stamp Station",
                "EVENT: Anouki Village Stamp Station",
                "EVENT: Snowfall Sanctuary Stamp Station",
                "EVENT: Icy Spring Stamp Station",
                "EVENT: Trading Post Tunnel Stamp Station",
                "EVENT: Papuzia Archipelago Stamp Station",
                "EVENT: Island Sanctuary Stamp Station",
                "EVENT: Pirate Hideout Stamp Station",
                "EVENT: Goron Field Stamp Station",
                "EVENT: Valley Sanctuary Stamp Station",
                "EVENT: Dune Sanctuary Stamp Station",
                "EVENT: Tower of Spirits Summit Stamp Station"
            ]
          #  print(f"non-required dungeons: {self.non_required_dungeons}")
            events += [event for dungeon, event in zip(DUNGEON_NAMES[2:], [
                "EVENT: Wooded Temple Stamp Station",
                "EVENT: Blizzard Temple Stamp Station",
                "EVENT: Marine Temple Stamp Station",
                "EVENT: Mountain Temple Stamp Station",
                "EVENT: Desert Temple Stamp Station"
            ]) if dungeon not in self.non_required_dungeons]

        if self.options.shuffle_dungeon_rooms.value:
            if not ("Marine Temple" in self.non_required_dungeons and self.options.exclude_dungeons.value):
                events += ["EVENT: Marine Temple 6F Arena"]
                if self.options.randomize_stamps.value:
                    events += ["EVENT: Marine Temple Stamp Room Switch"]
                if not self.options.logic.value:
                    events += ["EVENT: Marine Temple 2F Boulders"]
            if not ("Blizzard Temple" in self.non_required_dungeons and self.options.exclude_dungeons.value) and not self.options.open_blizzard_temple.value:
                events += ["EVENT: Blizzard Temple 1F Bell Door 2"]

        if self.options.rabbitsanity.value in [3, 4] and "rabbits" in self.options.extra_events.value:
            events += [f"EVENT: {r}" for r in LOCATION_GROUPS["Unique Rabbits"]]

        if self.options.randomize_passengers.value == 1 and "passengers" in self.options.extra_events.value:
            events += [
                "EVENT: Castle Town Pick Up Alfonzo",
                "EVENT: Bridge Worker's Home Pick Up Kenzo",
                "EVENT: Trading Post Drop Off Kenzo",
                "EVENT: Trading Post Pick Up Kenzo",
                "EVENT: Anouki Village Pick Up Kofu",
                "EVENT: Anouki Village Pick Up Noko",
                "EVENT: Castle Town Pick Up Mona",
                "EVENT: Outset Pick Up Joe",
                "EVENT: Mayscore Pick Up Dovok",
                "EVENT: Papuzia Village Pick Up Carben",
                "EVENT: Pirate Hideout Pick Up Wadatsumi",
                "EVENT: Goron Village Pick Up Snow Goron",
                "EVENT: Goron Village Pick Up City Goron",
                "EVENT: Snow Realm Pick Up Ferrus",
                "EVENT: Fire Realm Pick Up Ferrus",
                "EVENT: Marine Temple Lobby Drop Off Ferrus",
            ]
            if self.options.randomize_cargo.value:
                events += ["EVENT: Icy Spring Drop Off Noko"]
            if self.options.randomize_stamps.value:
                events += ["EVENT: Dune Sanctuary Deliver Cuccos"]

        if self.options.randomize_cargo.value == 1 and "cargo" in self.options.extra_events.value:
            events += [
                "EVENT: Icy Spring Buy Mega Ice",
                "EVENT: Mayscore Buy Lumber",
                "EVENT: Castle Town Buy Cuccos",
                "EVENT: Papuzia Village Buy Fish",
                "EVENT: Papuzia Village Buy Vessel",
                "EVENT: Goron Field Buy Steel",
                "EVENT: Dark Ore Mine Buy Ore"
            ]

        if "shortcuts" in self.options.extra_events.value and getattr(self.multiworld, "enforce_deferred_connections", "off") == "on":
            events += ["EVENT: Wooded Temple 1F Shortcut",
                       "EVENT: Wooded Temple 2F Windmill",
                       "EVENT: Blizzard Temple B1 SE Windmill",
                       "EVENT: Blizzard Temple 1F NE Door",
                       "EVENT: Blizzard Temple 1F NW Door",
                       "EVENT: Marine Temple 3F South Branch",
                       "EVENT: Marine Temple 4F West Door",
                       "EVENT: Marine Temple 4F South Bridge",
                       "EVENT: Marine Temple 5F North Branches",
                       "EVENT: Marine Temple 5F SE Door",
                       "EVENT: Mountain Temple 1F SW Switch",
                       "EVENT: Mountain Temple 1F Main Door",
                       "EVENT: Mountain Temple 2F Heatoise Arena",
                       "EVENT: Mountain Temple B2 Stalfos Arena",
                       "EVENT: Mountain Temple B2 SE Torches",
                       "EVENT: Mountain Temple B2 W Branch",
                       "EVENT: Mountain Temple B1 Arena",
                       "EVENT: Desert Temple B1 Shortcut",
                       "EVENT: Tunnel to the Tower 2F Door",
                       "EVENT: Island Sanctuary Bridge",
                       "EVENT: Valley Sanctuary Door",
                       "EVENT: Desert Temple B1 Red Door"]
            if not self.options.open_blizzard_temple.value:
                events += [
                    "EVENT: Blizzard Temple 1F Bell Door 1",
                    "EVENT: Blizzard Temple 1F Bell Door 3"
                ]

        self.ut_events = events
        # self.ut_map_page_hidden_entrances["Overview"] += [e.name for e in ENTRANCES.values() if e.category_group == EntranceGroups.EVENT and e.name not in self.ut_events and not e.name.startswith("Unnamed")]
        print(f"UT Events: {events} hidden: {self.ut_map_page_hidden_entrances}")
        for e in events:
            event = ENTRANCES[e]
            self.ut_pairings[str(event.id)] = event.vanilla_reciprocal.id

    def create_item_mappings(self):
        self.item_mapping_collect = {
            i: [("Rupees", ITEMS[i].value), ("Treasure Rupees", ITEMS[i].value)] for i in ITEM_GROUPS["Rupee Items"]
        } | {
            r: ("Grass Rabbit", ITEMS[r].value) for r in grass_rabbits[1:]
        } | {
            r: ("Snow Rabbit", ITEMS[r].value) for r in snow_rabbits[1:]
        } | {
            r: ("Ocean Rabbit", ITEMS[r].value) for r in ocean_rabbits[1:]
        } | {
            r: ("Mountain Rabbit", ITEMS[r].value) for r in mountain_rabbits[1:]
        } | {
            r: ("Sand Rabbit", ITEMS[r].value) for r in sand_rabbits[1:]
        } | {
            t: [("Treasure", price), ("Treasure Rupees", price)] for t, price in TREASURE_PRICES.items()
        } | {
            i: ("Stamp", ITEMS[i].value) for i in ITEM_GROUPS["Stamp Packs"]
        } | {
            i: ("Stamp", 1) for i in ITEM_GROUPS["Stamps"]
        } | {

        # Events
            "_stamp_stand": ("Stamp", 1)
        }
        # print(f"Item mappings: {self.item_mapping_collect}")

    def pick_required_dungeons(self) -> list[str]:
        force_require = []
        if self.options.goal.value >= 0:
            self.options.dark_realm_access.value = 0
            force_require = [list(BOSS_LOCATION_TO_EVENT_REGION.keys())[self.options.goal.value]]

        # Choose dungeon entrance-dungeon pairing if applicable
        if self.options.shuffle_dungeon_entrances.value in [1, 6]:
            shuffled_dungeons = DUNGEON_NAMES[2:]
            self.random.shuffle(shuffled_dungeons)
            self.shuffled_dungeon_lookup = {o: n for o, n in zip(DUNGEON_NAMES[2:], shuffled_dungeons)}

        # Match boss to dungeon when bosses are shuffled to match them properly in plando
        pre_pick_boss_pairings = DUNGEON_TO_BOSS_ITEM_LOCATION
        if self.options.shuffle_bosses.value in [1, 6]:
            bosses = list(BOSS_LOCATION_TO_POST_LOCATIONS.keys())
            self.random.shuffle(bosses)
            self.shuffled_bosses = {dung: boss for dung, boss in zip(DUNGEON_NAMES[2:], bosses)}
            for dung, boss in pre_pick_boss_pairings.items():
                if dung not in self.shuffled_bosses:
                    continue
                new_boss = self.shuffled_bosses[dung]
                pre_pick_boss_pairings[dung] = new_boss
            # print(f"bosses: {self.shuffled_bosses} pre pick {pre_pick_boss_pairings}")

        if self.options.plando_dungeon_pool:
            if "all" in self.options.plando_dungeon_pool.value:
                self.options.plando_dungeon_pool.value = set(DUNGEON_TO_BOSS_ITEM_LOCATION.keys())
            case_compare = {k.lower(): v for k, v in pre_pick_boss_pairings.items()}
            required_dungeons = list({case_compare[dung.lower()] for dung in self.options.plando_dungeon_pool.value})
        else:
            required_dungeons = list(BOSS_LOCATION_TO_POST_LOCATIONS.keys())
            implemented_tos = ["ToS 3F Forest Rail Glyph", "ToS 7F Snow Rail Glyph",
                               "ToS 12F Ocean Rail Glyph", "ToS 17F Fire Rail Glyph",
                               "ToS 23F Defeat Staven", "ToS 24F Final Chest"]
            if self.options.tos_dungeon_options == "final_section":
                required_dungeons.append(implemented_tos[-1])
            elif self.options.tos_dungeon_options == "all_sections":
                required_dungeons += implemented_tos

        self.options.dungeons_required.value = min(self.options.dungeons_required.value, len(set(required_dungeons + force_require)))
        if (self.options.exclude_dungeons.value and 4 >= self.options.goal.value >= 0) or (self.options.exclude_sections.value and self.options.goal.value >= 5):
            self.options.dungeons_required.value = max(1, self.options.dungeons_required.value)
        if not self.options.require_specific_dungeons:
            return list(set(required_dungeons + force_require))

        required_dungeons = [i for i in required_dungeons if i not in force_require]
        self.random.shuffle(required_dungeons)
        required_dungeons = force_require + required_dungeons
        required_dungeons = required_dungeons[:self.options.dungeons_required.value]
        # print(f"Required dungeons: {required_dungeons}")

        if self.options.dungeon_hints:
            self.options.start_location_hints.value.update(required_dungeons)
        return required_dungeons

    def restrict_non_local_items(self):
        # Restrict non_local_items option in cases where it"s incompatible with other options that enforce items
        # to be placed locally (e.g. dungeon items with keysanity off)
        if not self.options.keysanity == "anywhere":
            self.options.non_local_items.value -= self.item_name_groups["Small Keys"]
            self.options.non_local_items.value -= self.item_name_groups["Boss Keys"]

    def create_location(self, region_name: str, location_name: str, local: bool):
        region = self.multiworld.get_region(region_name, self.player)
        location = Location(self.player, location_name, self.location_name_to_id[location_name], region)
        region.locations.append(location)

        if local:
            location.item_rule = lambda item: item.player == self.player

    def create_regions(self):
        # Create regions
        all_regions = set(REGIONS)
        if self.is_ut:
            all_regions.update(set(ENTRANCES.keys()))

        for region_name in all_regions:
            region = Region(region_name, self.player, self.multiworld)
            self.multiworld.regions.append(region)

        # Map post/pre dungeon items to their dungeons
        reverse_dungeon_lookup = {v: k for k, v in self.shuffled_dungeon_lookup.items()}
        for dung_name in DUNGEON_NAMES[2:]:
            if dung_name in self.shuffled_bosses:
                # print(f"Shuffled_bosses: {self.shuffled_bosses}")
                boss_loc = self.shuffled_bosses[dung_name]
                self.near_dungeon_lookup |= {loc: dung_name for loc in BOSS_LOCATION_TO_POST_LOCATIONS.get(boss_loc, [])}
            else:
                boss_dungeon = DUNGEON_TO_BOSS_ITEM_LOCATION.get(dung_name)
                self.near_dungeon_lookup |= {loc: dung_name for loc in BOSS_LOCATION_TO_POST_LOCATIONS.get(boss_dungeon, [])}
            if dung_name in reverse_dungeon_lookup:
                self.near_dungeon_lookup |= {loc: dung_name for loc in DUNGEON_NAME_TO_LOBBY_LOCATION.get(reverse_dungeon_lookup[dung_name], [])}
            else:
                self.near_dungeon_lookup |= {loc: dung_name for loc in DUNGEON_NAME_TO_LOBBY_LOCATION.get(dung_name, [])}
        # print(f"ndl: {self.near_dungeon_lookup}")

        # Create locations
        for location_name, location_data in LOCATIONS_DATA.items():
            if not self.location_is_active(location_name, location_data):
                continue

            is_local = "local" in location_data and location_data["local"] is True
            self.create_location(location_data['region_id'], location_name, is_local)

        self.create_events()
        self.exclude_locations_automatically()

    def create_event(self, region_name, event_item_name):
        region = self.get_region(region_name)
        location = Location(self.player, region_name + ".event", None, region)
        region.locations.append(location)
        location.place_locked_item(SpiritTracksItem(event_item_name, ItemClassification.progression, None, self.player))

    # When you want multiple copies of the same event in the same region
    def create_multiple_events(self, region_name, event_item_name, count):
        region = self.get_region(region_name)
        locations = [Location(self.player, region_name + f"{i}.event", None, region) for i in range(count)]
        for loc in locations:
            region.locations.append(loc)
            loc.place_locked_item(SpiritTracksItem(event_item_name, ItemClassification.progression, None, self.player))

    def location_is_active(self, location_name, location_data):
        if not location_data.get("conditional", False) and "rabbit" not in location_data and "dungeon" not in location_data and "tos_section" not in location_data and "post_dungeon" not in location_data:
            return True

        if "tos_section" in location_data:
            if "stamp" in location_data:
                return self.options.randomize_stamps.value in [1, 2, 3]
            bk = self.options.randomize_boss_keys.value if location_name.endswith("Boss Key") else True
            tears = self.options.randomize_tears.value != -1 if location_data.get("conditional", False) == "tears" else True
            return bk and tears and (location_data["tos_section"] not in self.non_required_sections or self.options.exclude_sections != "remove")
        if "dungeon" in location_data:
            stamp = self.options.randomize_stamps.value in [1, 2, 3] if "stamp" in location_data else True
            bk = self.options.randomize_boss_keys.value if location_name.endswith("Boss Key") else True
            # print(f"Location is active: {location_name}? {location_data['dungeon'] not in self.non_required_dungeons}")
            return stamp and bk and (self.options.exclude_dungeons != "remove" or location_data["dungeon"] not in self.non_required_dungeons)
        if location_name == "Marine Temple Lobby Ferrus Force Gem":
            return self.options.randomize_passengers.value
        if location_name in self.near_dungeon_lookup:
            if self.options.exclude_dungeons.value != 2:
                return True
            return self.near_dungeon_lookup[location_name] not in self.non_required_dungeons

        if location_name.startswith("Bonus Starting Item"):
            return location_data["value"] <= self.options.free_starting_items.value
        if "rabbit" in location_data:
            return location_name in self.active_rabbit_locations
        if "Portal" in location_name:
            return self.options.portal_checks
        if location_name in LOCATION_GROUPS["Rabbit Rewards"]:
            return self.options.rabbitsanity.value
        if "minigame" in location_data and self.options.randomize_minigames.value:
            if (location_name in ["Castle Town Take 'em All On Level 3",
                                 "Castle Town Take 'em All On Level 3 Capbone Chest"]
                    and "Castle Town Take 'em All On Level 3" in self.required_boss_locs):
                return True  # If plandoed dungeon include
            # print(f"Minigame {location_name} {self.options.randomize_minigames.value in location_data['minigame']}")
            if location_name in LOCATION_GROUPS["Ends of the Earth"] and self.options.shuffle_eote.value:
                return True
            return self.options.randomize_minigames.value in location_data["minigame"]
        if location_name in LOCATION_GROUPS["Stamp Stands"]:
            return self.options.randomize_stamps.value in [1, 2, 3]
        if location_name in LOCATION_GROUPS["Niko"]:
            # If dungeon stamp stands are excluded with vanilla stamps, niko has to give less items
            if self.options.exclude_dungeons.value and self.non_required_dungeons and self.options.randomize_stamps.value in [1, 2, 4]:
                if len(self.non_required_dungeons) > 5:
                    return location_name not in ["Outset Niko 15 Stamps Reward", "Outset Niko 20 Stamps Reward"]
                return location_name not in ["Outset Niko 20 Stamps Reward"]
            return self.options.randomize_stamps.value
        if self.options.shopsanity.value and location_name in LOCATION_GROUPS["Shop Locations"]:
            if location_name in LOCATION_GROUPS["Shop Restock Locations"]:
                if "uniques" in self.options.shopsanity.value:
                    return False
                if location_name == "Beedle Shop Purple Potion":
                    return "potions" in self.options.shopsanity.value
                if location_name == "Snowfall Supermarket Treasure":
                    return "treasure" in self.options.shopsanity.value
                if location_name == "Goron Shop Postcards":
                    return "postcards" in self.options.shopsanity.value
            if location_name in LOCATION_GROUPS["Shop Treasure Locations"]:
                return "treasure" in self.options.shopsanity.value
            if location_name in LOCATION_GROUPS["Shop Unique Locations"]:
                return "uniques" in self.options.shopsanity.value
            if location_name in LOCATION_GROUPS["Shop Potion Locations"]:
                return "potions" in self.options.shopsanity.value
            if location_name in LOCATION_GROUPS["Shop Shield Locations"]:
                return "shields" in self.options.shopsanity.value
            if location_name in LOCATION_GROUPS["Shop Postcard Locations"]:
                return "postcards" in self.options.shopsanity.value
            if location_name in LOCATION_GROUPS["Shop Ammo Locations"]:
                return "ammo" in self.options.shopsanity.value
        if location_name == "Anouki Village Repair Fence":
            return self.options.randomize_passengers.value or self.options.randomize_cargo.value
        if location_name == "Anouki Village Fence Progress Gift":
            return self.options.randomize_passengers.value and self.options.randomize_cargo.value
        if self.options.randomize_passengers.value and location_name in LOCATION_GROUPS["Passenger Locations"]:
            if "slot_data" in location_data:
                for option, values, *args in location_data["slot_data"]:
                    if option != "randomize_passengers":
                        continue
                    values = values if isinstance(values, list) else [values]
                    if self.options.randomize_passengers.value not in values:
                        return False
                return True
        if self.options.randomize_cargo.value and location_name in LOCATION_GROUPS["Cargo Locations"]:
            if "slot_data" in location_data:
                for option, values, *args in location_data["slot_data"]:
                    if option != "randomize_cargo":
                        continue
                    values = values if isinstance(values, list) else [values]
                    if self.options.randomize_cargo.value not in values:
                        return False
                return True
        return False

    def create_events(self):
        if self.options.goal == "defeat_malladus":
            self.create_event("malladus goal", "_beaten_game")
            if self.options.dark_realm_access in ["dungeons", "both"]:
                for loc in self.required_boss_locs:
                    self.create_event(BOSS_LOCATION_TO_EVENT_REGION[loc], "_dungeon_reward")
        else:
            goal_loc = list(BOSS_LOCATION_TO_EVENT_REGION.keys())[self.options.goal.value]
            goal_reg = BOSS_LOCATION_TO_EVENT_REGION[goal_loc]
            self.create_event(goal_reg, "_beaten_game")

        if self.options.rabbitsanity.value in [3, 4]:
            forest_regions = {"forest ocean shortcut rabbit": 1,
                              "e mayscore rabbits": 2,
                              "sw trading post rabbit": 1,
                              "wt rabbit": 1,
                              "s rabbit haven rabbits": 2,
                              "nr rabbit haven rabbit": 1,
                              "forest realm rabbits": 2}
            snow_regions = {"snow realm blizzard rabbits": 2,
                            "snow realm early blizzard rabbits": 3,
                            "blizzard temple tracks rabbits": 1,
                            "snow realm rabbits": 1,
                            "snowdrift station rabbit": 1,
                            "icyspring rabbits": 2}
            ocean_regions = {"ocean rabbits": 6,
                            "las rabbit": 1,
                            "ocean portal rabbits": 1,
                            "ocean source rabbits": 1,
                            "pirate rabbit": 1}
            mountain_regions = {"fire realm rabbits": 2,
                                "mountain rabbits": 4,
                                "fire source rabbits": 1,
                                "disorientation rabbits": 1,''
                                "eote rabbits": 1,
                                "s mountain temple rabbit": 1}
            sand_regions = {"sand realm rabbits": 4,
                            "sand restoration rabbits": 3,
                            "sand restoration south rabbits": 2,
                            "sand connection rabbit": 1}
            [self.create_multiple_events(reg, f"_caught_{realm}_rabbits", count)
             for regions, realm in zip([forest_regions, snow_regions, ocean_regions, mountain_regions, sand_regions], ["grass", "snow", "ocean", "mountain", "sand"])
             for reg, count in regions.items()]

        if self.options.randomize_stamps.value in [1, 4]:
            excluded_dungeons = self.non_required_dungeons if self.options.exclude_dungeons else []
            [self.create_event(LOCATIONS_DATA[loc]["region_id"].replace("station", "event"), "_stamp_stand") for loc in LOCATION_GROUPS["Stamp Stands"] if LOCATIONS_DATA[loc].get("dungeon") not in excluded_dungeons]

        # Create rupee farming events
        rupee_farming_regions = ["mayscore whip game", "mayscore leaves",
                                 "hyrule castle sword minigame", "pirate hideout minigame",
                                 "gtr"]
        [self.create_event(reg, "_rupee_farming_spot") for reg in rupee_farming_regions]
        # Passenger Events
        if self.options.randomize_passengers == "vanilla":
            self.create_event("pick up bridge worker event", "_kenzo_1")
            self.create_event("trading post pick up kenzo event", "_kenzo_2")
            self.create_event("av noko event", "_noko")
            self.create_event("castle town mona event", "_mona")
            self.create_event("outset joe event", "_joe")
            self.create_event("alfonzo event", "_picked_up_alfonzo")
            self.create_event("mayscore dovok event", "_dovok")
            self.create_event("pv carben event", "_carben")
            self.create_event("pirate wadatsumi event", "_wadatsumi")
            self.create_event("av kofu event", "_kofu")
            self.create_event("pick up snow goron event", "_snow_goron")
            self.create_event("pick up city goron event", "_city_goron")
            self.create_event("snow realm ferrus event", "_ferrus_1")
            self.create_event("fire realm ferrus event", "_ferrus_2")
            self.create_event("oct ferrus event", "_ferrus_3")
            self.create_event("icyspring", "_ferrus_backup")
        if self.options.randomize_cargo == "vanilla":
            self.create_event("mayscore lumber event", "_buy_lumber")
            self.create_event("icyspring ice event", "_buy_ice")
            self.create_event("castle town buy cuccos event", "_buy_cuccos")
            self.create_event("papuzia buy fish event", "_buy_fish")
            self.create_event("wise one buy vessel event", "_buy_vessel")
            self.create_event("dark ore mine ore event", "_buy_ore")
            self.create_event("goron steel event", "_buy_steel")
        # Logic Events
        # self.create_event("alfonzo event", "_picked_up_alfonzo")
        self.create_event("linebeck event", "_can_sell_treasure")
        self.create_event("goron ice event", "_goron_ice")  # Used for GTR
        self.create_event("kagoron event", "_visit_kagoron")
        self.create_event("papuzia village song statue", "_papuzia_sob")
        self.create_event("disorientation event", "_disorientation_chest")
        if self.options.randomize_passengers.value:
            self.create_event("outset delivered ferrus event", "_delivered_ferrus")
            self.create_event("av goron event", "_av_goron")
            self.create_event("carben event", "_deliver_carben")

        def create_blue_warp_events():
            self.create_event("wt warp event", "_wt_warp")
            self.create_event("bt warp event", "_bt_warp")
            self.create_event("oct warp event", "_oct_warp")
            self.create_event("mtt warp event", "_mtt_warp")
            self.create_event("dt warp event", "_dt_warp")

        # DER events. might add if statement later
        if "Blizzard Temple" not in self.non_required_dungeons or self.options.exclude_dungeons.value != 2:
            self.create_event("bt 1f torches", "_bt_torches")
            if not self.options.open_blizzard_temple.value:
                self.create_event("bt 1f ne bell event", "_bt_bell_2")
                self.create_event("bt 1f nw bell event", "_bt_bell_3")
        if "Marine Temple" not in self.non_required_dungeons or self.options.exclude_dungeons.value != 2:
            self.create_event("oct 2f boulders event", "_oct_boulders")
            self.create_event("oct boomerang switch event", "_oct_boomerang")
            self.create_event("oct 6f sw arena event", "_oct_6f_arena")
        if (not self.options.open_blue_warps.value
            and self.options.exclude_dungeons.value == 2
            and self.shuffled_dungeon_lookup
            and self.options.shuffle_warps.value in [0, 5]):
                if self.shuffled_dungeon_lookup["Wooded Temple"] not in self.non_required_dungeons:
                    self.create_event("wt warp event", "_wt_warp")
                if self.shuffled_dungeon_lookup["Blizzard Temple"] not in self.non_required_dungeons:
                    self.create_event("bt warp event", "_bt_warp")
                if self.shuffled_dungeon_lookup["Marine Temple"] not in self.non_required_dungeons:
                    self.create_event("oct warp event", "_oct_warp")
                if self.shuffled_dungeon_lookup["Mountain Temple"] not in self.non_required_dungeons:
                    self.create_event("mtt warp event", "_mtt_warp")
                if self.shuffled_dungeon_lookup["Desert Temple"] not in self.non_required_dungeons:
                    self.create_event("dt warp event", "_dt_warp")
        else:
            create_blue_warp_events()

        if self.options.randomize_passengers.value and self.options.passenger_pickup.value == 1:
            self.create_event("visit outset", "_visit_outset")
            self.create_event("visit castle town", "_visit_ct")
            self.create_event("visit rabbit haven", "_visit_rabbit")
            self.create_event("visit anouki village", "_visit_av")
            self.create_event("visit icyspring", "_visit_icyspring")
            self.create_event("visit trading post", "_visit_tp")
            self.create_event("visit papuzia", "_visit_papuzia")
            self.create_event("visit marine temple", "_visit_oct")
            self.create_event("visit goron village", "_visit_gv")

        # Train Portal events
        if self.options.portal_behavior.value == 0:
            self.create_event("cave portal event", "_cave_portal")
            self.create_event("trading post portal event", "_tp_portal")
            self.create_event("anouki portal event", "_sr_portal")
            self.create_event("snow bridge portal event", "_bridge_portal")
            self.create_event("icyspring portal event", "_icyspring_portal")
            self.create_event("ocean portal event", "_ocean_portal")
            self.create_event("sand restoration portal event", "_dt_portal")
            self.create_event("sand connection portal event", "_sand_portal")

        self.create_event("las loop event", "_las6")


    def exclude_locations_automatically(self):
        locations_to_exclude = set()

        self.ut_locations_to_exclude = locations_to_exclude.copy()
        self.locations_to_exclude = locations_to_exclude

        # Filter excluded dungeons, and account for dungeon/boss shuffle
        if self.options.exclude_dungeons == "exclude":
            self.locations_to_exclude.update([loc for loc, d in LOCATIONS_DATA.items() if
                                              "dungeon" in d and d["dungeon"] in self.non_required_dungeons])
            for loc_name, dung_name in self.near_dungeon_lookup.items():
                if dung_name in self.non_required_dungeons:
                    self.locations_to_exclude.add(loc_name)

            self.locations_to_exclude -= {"Marine Temple Lobby Ferrus Force Gem"}

        if self.options.exclude_sections == "exclude":
            self.locations_to_exclude.update([loc for loc, d in LOCATIONS_DATA.items() if "tos_section" in d and d["tos_section"] in self.non_required_sections])

        if self.options.randomize_passengers == "vanilla_abstract":
            self.locations_to_exclude.update(["Mayscore Pick Up Wood",
                                              "Mayscore Pick Up Mash",
                                              "Mayscore Pick Up Yamahiko",
                                              "Mayscore Pick Up Morris",
                                              "Castle Town Pick Up Teacher"])

        # Take item off goal + post goal location
        if self.options.goal.value >= 0:
            current_goal = list(BOSS_LOCATION_TO_EVENT_REGION.keys())[self.options.goal.value]
            self.locations_to_exclude.add(current_goal)
            for loc in BOSS_LOCATION_TO_POST_LOCATIONS.get(current_goal, []):
                self.locations_to_exclude.add(loc)

        for name in self.locations_to_exclude:
            # print(f"Excluded Location: {name}")
            try:
                self.multiworld.get_location(name, self.player).progress_type = LocationProgressType.EXCLUDED
            except KeyError:  # Would it be more efficient to check if location is in active locations first?
                pass

    def set_rules(self):
        create_connections(self, self.player, self.origin_region_name, self.options)

    def create_item(self, name: str) -> SpiritTracksItem:
        classification = ITEMS[name].classification
        if name in self.extra_filler_items:
            self.extra_filler_items.remove(name)
            classification = ItemClassification.filler
        if not self.options.shopsanity and name in ITEM_GROUPS["Uncommon Plus Treasure"]:
            # print(f"Changing classification for item {name}")
            classification = DEPRIORITIZED_SKIP_BALANCING_FALLBACK

        ap_code = self.item_name_to_id[name]
        return SpiritTracksItem(name, classification, ap_code, self.player)

    def build_item_pool_dict(self):
        removed_item_quantities = self.options.remove_items_from_pool.value.copy()
        item_pool_dict = {}
        filler_item_count = 0

        def pop_item_from_dict(item_dict, item):
            item_dict[item] -= 1
            if item_dict[item] <= 0:
                item_dict.pop(item)

        def pop_random_item_from_dict(item_dict):
            i_name = self.random.choice([i for i in item_dict])
            pop_item_from_dict(item_dict, i_name)
            return i_name

        for loc_name, loc_data in LOCATIONS_DATA.items():
            # print(f"New Location: {loc_name} {filler_item_count}")
            if not self.location_is_active(loc_name, loc_data):
                # print(f"{loc_name} is not active")
                continue
            # If no defined vanilla item, fill with filler
            if "vanilla_item" not in loc_data:
                # print(f"\t{loc_name} has no defined vanilla item")
                filler_item_count += 1
                continue

            item_name = loc_data.get("item_override", loc_data["vanilla_item"])
            if isinstance(item_name, list | set):
                item_name = self.random.choice(list(item_name))
            item_data = ITEMS[item_name]
            if item_name in removed_item_quantities and removed_item_quantities[item_name] > 0:
                # If item was put in the "remove_items_from_pool" option, replace it with a random filler item
                removed_item_quantities[item_name] -= 1
               # print(f"\triq")
                filler_item_count += 1
                continue

            if "rabbit" in item_data.tags:
                if self.options.rabbitsanity == "vanilla" and not hasattr(self.multiworld, "generation_is_fake"):  # Force vanilla rabbits randomly
                    realm = item_name.split()[0]
                    realm_pool = self.rabbit_realm_items[realm]
                    popped_item = pop_random_item_from_dict(realm_pool)
                    pop_item_from_dict(self.rabbit_item_dict, popped_item)

                    forced_item = self.create_item(popped_item)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
                # print(f"\trabbit")
                filler_item_count += 1
                continue
            if "Tear of Light" in item_name:
                if self.options.randomize_tears.value < 0:
                    forced_item = self.create_item(item_name)
                    self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                    continue
                # print(f"\ttear")
                filler_item_count += 1
                continue
            if "stamp" in loc_data and self.options.randomize_stamps.value == 2:
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                # print(f"Locking stamp item {item_name} to {loc_name}")
                continue
            if any([
                item_name in ["Filler Item", "Treasure", "Nothing!", "Compass of Light",
                              "Heart Container", "Tear of Light",
                              "Shield", "Prize Postcards (10)", "Sand Source"],
                item_name.startswith("Stamp"),
                item_name in ITEM_GROUPS["Basic Tracks"],
                item_name in ITEM_GROUPS["Main Items"],
                item_name in ITEM_GROUPS["All Treasures"],
                item_name in ITEM_GROUPS["Rupee Items"],
                self.options.randomize_cargo.value == 3 and item_name in ["Cargo: Cuccos", "Cargo: Mega Ice"],
                self.options.keyrings.value >= 1 and item_name == "Mountain Temple Snurglar Key",
                self.options.keyrings.value > 1 and item_name.startswith("Small Key ("),
                self.options.keyrings.value > 1 and self.options.big_keyrings and item_name.startswith("Boss Key (") and item_name != "Boss Key (ToS 3)"
                ]):
                # print(f"\tBig listicle {item_name}")
                filler_item_count += 1
                continue
            if any([
                "Small Key" in item_name and self.options.keysanity == "vanilla",
                loc_name.endswith("Boss Key") and self.options.randomize_boss_keys == "vanilla_abstract",
                "force_vanilla" in loc_data and loc_data["force_vanilla"],
                self.options.randomize_passengers == "vanilla_abstract" and item_name.startswith("Passenger:"),
                self.options.randomize_cargo == "vanilla_abstract" and item_name.startswith("Cargo:"),
                item_name == "Mountain Temple Snurglar Key" and self.options.keysanity == "vanilla"
            ]):
                # print(f"Forcing item {item_name} to location {loc_name}")
                forced_item = self.create_item(item_name)
                self.multiworld.get_location(loc_name, self.player).place_locked_item(forced_item)
                continue
            # if item_data.classification == ItemClassification.filler:  # Regen all filler items for now
            #     filler_item_count += 1
            #     continue

            item_pool_dict[item_name] = item_pool_dict.get(item_name, 0) + 1

        # add progression items first
        add_items = [("Repair Trading Post Bridge", 1), ("Treasure: Regal Ring", 1)]
        if self.options.progressive_equipment:
            add_items += [("Bombs (Progressive)", 3), ("Bow (Progressive)", 3)]
        else:
            add_items += [("Bomb Bag", 1), ("Bow", 1), ("Bomb Bag Upgrade", 2), ("Quiver Upgrade", 2)]
        if self.options.shields_in_pool:
            add_items += [("Shield", math.ceil(filler_item_count/60)), ("Ancient Shield", 1)]
        add_items += [(i, 1) for i in ITEM_GROUPS["Non-Progressive Main Items"]]
        if self.options.dark_realm_access.value in [2, 3] and self.options.compass_shard_total.value > 1:
            add_items += [("Compass of Light Shard", self.options.compass_shard_total.value)]
        else:
            add_items += [("Compass of Light", 1)]
        if self.options.rabbitsanity: add_items += [("Rabbit Net", 1)]
        if self.options.randomize_cargo: add_items += [("Wagon", 1)]
        if self.options.randomize_cargo.value == 3: add_items += [("Cargo: Mega Ice", 3), ("Cargo: Cuccos (5)", 3)]
        # if self.options.shopsanity: add_items += [("Treasure: Regal Ring", 1), ("Treasure: Priceless Stone", 2)]
        if self.options.randomize_stamps: add_items += self.stamp_items
        add_items += self.choose_tos_items()
        add_items += self.choose_key_items()
        add_items += self.track_items
        if self.options.portal_behavior.value == 2:
            add_items += [(i, 1) for i in ITEM_GROUPS["Portal Unlocks"]]
        add_items += self.choose_tear_items()
        add_items += [i for i in self.rabbit_item_dict.items()]
        add_items += [("Sword Beam Scroll", 1), ("Great Spin Scroll", 1), ("Heart Container", 13)]
        # Add items
        for i, count in add_items:
            # print(f"\t{i}: {count}")
            item_pool_dict, filler_item_count = add_items_from_filler(item_pool_dict, filler_item_count, i, count)

        # Calculate rupee items for logic, and make sure there are enough filler items for excluded locations
        item_pool_dict = self.choose_filler_items(filler_item_count, item_pool_dict)

        return item_pool_dict

    def choose_key_items(self):
        res: list[tuple[str, int]] = []
        if self.options.keyrings == 0:
            return res
        if self.options.keyrings == 1:
            res += [("Snurglar Keyring", 1)]
        elif self.options.keyrings >= 2:
            keyrings = ITEM_GROUPS["Keyrings"].copy()
            res += [("Small Key (Tunnel to ToS)", 1)]
            if self.options.exclude_dungeons == "remove":
                keyrings -= {f"Keyring ({i})" for i in self.non_required_dungeons}
            if self.options.exclude_sections == "remove":
                keyrings -= {f"Keyring (ToS {i})" for i in self.non_required_sections}
            if not self.options.big_keyrings and not self.options.exclude_sections == "remove" and "Blizzard Temple" not in self.non_required_dungeons:
                keyrings -= {"Keyring (Blizzard Temple)"}
                res += [("Small Key (Blizzard Temple)", 1)]

            if self.options.keyrings == 3:
                keyrings = list(keyrings)
                keyrings.sort()
                self.random.shuffle(keyrings)
                keyring_count = self.random.randint(0, len(keyrings))
                chosen_keyrings = keyrings[:keyring_count]
                # print(f"Chosen keys: {chosen_keyrings}")
                vanilla_keys = ["(" + i.split("(")[1] for i in keyrings[keyring_count:] if i != "Snurglar Keyring"]
                if "Snurglar Keyring" in keyrings[keyring_count:]:
                    res += [("Mountain Temple Snurglar Key", 3)]
                for dungeon in vanilla_keys:
                    key = f"Small Key {dungeon}"
                    res += [(key, KEY_COUNTS[key])]
                    if self.options.big_keyrings:
                        big_key = f"Boss Key {dungeon}"
                        if big_key not in ITEMS:
                            continue
                        res += [(big_key, 1)]
                keyrings = chosen_keyrings
            res += [(i, 1) for i in keyrings]

        # print(f"Key Items: {res}")
        return res

    def choose_track_items(self):
        option = self.options.track_pool
        track_items = set()
        if option == "vanilla":
            track_items = ITEM_GROUPS["Basic Tracks"]
        elif option == "major_minor":
            track_items = ITEM_GROUPS["Major Track Groupings"] | ITEM_GROUPS["Minor Track Groupings"]
        elif option == "completed_glyphs":
            track_items = ITEM_GROUPS["Completed Track Groupings"]
        elif option == "thematic":
            track_items =  ITEM_GROUPS["Thematic Track Groupings"]
        elif option.value < 0:  # Random mixed
            skip_pools = set()
            for pool_name, pool in ITEM_GROUPS.items():
                if not pool_name.startswith("Tracks:") or pool_name in skip_pools:
                    continue
                valid_choices = pool.copy()
                if option == "mixed_large":
                    valid_choices -= ITEM_GROUPS["Basic Tracks"]
                elif option == "mixed_small":
                    valid_choices -= ITEM_GROUPS["Completed Track Groupings"]
                new_track = self.random.choice(list(valid_choices))
                track_items.add(new_track)
                skip_pools.update([i for i in ITEMS[new_track].item_groups if i.startswith("Tracks:")])
        add_items = [(i, 1) for i in track_items]
        # print(len(add_items), add_items)
        self.raw_track_items = track_items

        return add_items

    def choose_starting_tracks(self):
        if not self.options.start_with_train.value:
            return
        pairings = {}
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id

        if self.starting_entrance == "Niko's House Exit" and not self.options.shuffle_houses:
            starting_entrance = ENTRANCES["Outset Board Train"]
        else:
            starting_entrance = ENTRANCES[self.starting_entrance]
        reciprocal = entrance_id_to_entrance[pairings.get(starting_entrance.id, starting_entrance.vanilla_reciprocal.id)]
        # print(f"Starting entrance {self.starting_entrance} | {starting_entrance}, reciprocal {reciprocal}")

        if reciprocal.required_groups:
            starting_tracks = set()
            for group in reciprocal.required_groups:
                if isinstance(group, tuple):
                    group = self.random.choice(group)
                valid_starting_tracks = [track for track in self.raw_track_items if track in ITEM_GROUPS[group]]
                # print(f"Valid starting tracks: {valid_starting_tracks} group {group}")
                starting_tracks.add(self.random.choice(valid_starting_tracks))
            self.options.start_inventory_from_pool.value.update({track: 1 for track in starting_tracks})

        if self.options.cannon_logic.value in [0, 1]:
            self.options.start_inventory_from_pool.value.update({"Cannon": 1})
        # print(self.options.start_inventory_from_pool.value)

    def choose_filler_items(self, filler_count, item_pool_dict):
        rupees_required = self.get_required_rupees()
        required_filler = len(self.locations_to_exclude)
        max_non_filler = filler_count - required_filler
        # print(f"Filler Count: {filler_count} | Excluded {required_filler} remaining {max_non_filler}")
        if max_non_filler <= 0:
            raise FillError(f"Not enough room in item pool for filler items, please adjust your settings.")

        # Start with 60% of the remaining filler pool as rupee items, and cascade down until you've got 3 times the required rupees.
        cascade = [99, 100, 150, 200, 300, 500, 2500]
        filler_values = [2500]*((max_non_filler*6)//10)
        total_rupees = rupees_required*2+2500
        # print(f"Need {rupees_required} rupees, starting with pool of {len(filler_values)} value {sum(filler_values)} for target {total_rupees}")
        if sum(filler_values) < total_rupees:
            filler_values += [2500]*math.ceil((total_rupees-sum(filler_values))/2400)
            print(f"Not enough room in filler pool for rupees, adding more regal rings")
        while sum(filler_values) > total_rupees:
            i = self.random.choice(filler_values)
            filler_values.remove(i)
            if i != 100:
                filler_values.append(cascade[cascade.index(i) - 1])

        # Create items for the corresponding values
        rupee_choices = {99: "Big Green Rupee (100)",
                         100: "Big Green Rupee (100)",
                         150: list(ITEM_GROUPS["Uncommon Treasures"]),
                         200: "Big Red Rupee (200)",
                         300: "Gold Rupee (300)",
                         500: list(ITEM_GROUPS["Rare Treasures"]),
                         2500: list(ITEM_GROUPS["Super Rare Treasures"])}
        # print(f"Rupee pool: {filler_values}")
        for i in filler_values:
            if isinstance(rupee_choices[i], str):
                item_pool_dict[rupee_choices[i]] = item_pool_dict.get(rupee_choices[i], 0) + 1
            else:
                choice = self.random.choice(rupee_choices[i])
                item_pool_dict[choice] = item_pool_dict.get(choice, 0) + 1
        filler_count -= len(filler_values)
        # print(f"Rupee item dict: {[(i, v) for i, v in item_pool_dict.items() if i in ITEM_GROUPS['Rupee Pool Items']]}")
        # Get filler items for the remaining items
        for _ in range(filler_count):
            random_filler_item = self.get_filler_item_name()
            item_pool_dict[random_filler_item] = item_pool_dict.get(random_filler_item, 0) + 1
        # print(f"Filler item dict: {[(i, v) for i, v in item_pool_dict.items() if i in ITEM_GROUPS['Filler Item Pool']]}")
        return item_pool_dict

    def choose_tos_items(self):
        res = []
        if self.options.tos_section_unlocks in ["progressive"]:
            prog_count = 4
            if self.options.tos_unlock_base_item:
                prog_count = 5
            res += [("Progressive ToS Section", prog_count)]
        elif self.options.tos_unlock_base_item:
            res += [("Tower of Spirits Base", 1)]

        return res

    def choose_rabbit_locations(self):
        if not self.options.rabbitsanity:
            return []
        rabbit_locations = []
        # Figure out rabbit counts for different pools
        max_count = self.options.rabbit_max_location_count.value
        rabbit_counts = [max_count]*5
        if self.options.rabbit_location_count_distribution.value == -1:
            rabbit_counts = [self.random.randint(1, max_count) for _ in range(5)]
        self.rabbit_counts = rabbit_counts

        def pick_random_locs(loc_lists):
            [self.random.shuffle(i) for i in loc_lists]
            return [loc for rl, c in zip(loc_lists, rabbit_counts) for loc in rl[:c]]

        # Figure out pools
        if self.options.rabbitsanity.value in [1, 2, 4]: # Vanilla or unique
            forest_rabbits = list(LOCATION_GROUPS["Unique Grass Rabbits"])
            snow_rabbits = list(LOCATION_GROUPS["Unique Snow Rabbits"])
            ocean_rabbits = list(LOCATION_GROUPS["Unique Ocean Rabbits"])
            mountain_rabbits = list(LOCATION_GROUPS["Unique Mountain Rabbits"])
            sand_rabbits = list(LOCATION_GROUPS["Unique Sand Rabbits"])
            rabbit_locations += pick_random_locs([forest_rabbits, snow_rabbits, ocean_rabbits, mountain_rabbits, sand_rabbits])

        if self.options.rabbitsanity.value in [3, 4]:  # total count
            forest_rabbits = list(LOCATION_GROUPS["Total Grass Rabbits"])
            snow_rabbits = list(LOCATION_GROUPS["Total Snow Rabbits"])
            ocean_rabbits = list(LOCATION_GROUPS["Total Ocean Rabbits"])
            mountain_rabbits = list(LOCATION_GROUPS["Total Mountain Rabbits"])
            sand_rabbits = list(LOCATION_GROUPS["Total Sand Rabbits"])
            sort_func = lambda loc: f"0{loc.split()[1]}"[-2:]  # wth python
            forest_rabbits.sort(key=sort_func)
            snow_rabbits.sort(key=sort_func)
            ocean_rabbits.sort(key=sort_func)
            mountain_rabbits.sort(key=sort_func)
            sand_rabbits.sort(key=sort_func)
            interval = self.options.rabbit_location_count_distribution.value
            rabbit_lists = [forest_rabbits, snow_rabbits, ocean_rabbits, mountain_rabbits, sand_rabbits]
            if interval >= 0:
                intervals = [interval]*5 if interval else [self.random.randint(1, 3) for _ in range(3)]
                for i, realm_locs in zip(intervals, rabbit_lists):
                    if i > max_count:
                        rabbit_locations.append(realm_locs[max_count-1])
                    else:
                        rabbit_locations += realm_locs[i-1:max_count:i]
                # print(f"Rabbit Locations: {rabbit_counts} {intervals} {rabbit_locations}")
                return rabbit_locations
            if self.options.rabbitsanity == "both":  # Randomize each pool count separately
                self.rabbit_counts = [self.random.randint(1, max_count) for _ in range(5)]
            rabbit_lists = [r[:max_count] for r in rabbit_lists]
            rabbit_locations += pick_random_locs(rabbit_lists)

        # print(f"Rabbit Locations: {rabbit_counts} {rabbit_locations}")
        return rabbit_locations

    def choose_rabbit_items(self):
        if not self.options.rabbitsanity:
            return {}

        def get_rabbit_pack_name(realm, count):
            if count == 1:
                return f"{realm} Rabbit"
            return f"{realm} Rabbits ({count})"

        def create_items_from_count_list(realm, clist):
            res = {}
            for count in clist:
                item_name = get_rabbit_pack_name(realm, count)
                res.setdefault(item_name, 0)
                res[item_name] += 1
            # print(f"Creating rabbit items: {res}")
            return res

        def fill_vanilla(realm, max_count):
            count_distr = [1]*max_count
            if max_count == 1:
                return {get_rabbit_pack_name(realm, 10): 1}

            res_counts = []
            # print(f"Filling vanilla rabbits {realm} {max_count}")
            while sum(count_distr) + sum(res_counts) < 10:
                randindex = self.random.randint(0, len(count_distr)-1)
                count_distr[randindex] += 1
                if count_distr[randindex] == 5:
                    res_counts.append(count_distr.pop(randindex))
            res_counts += count_distr
            res_counts += [1]*self.options.rabbit_extra_items.value  # Add bonus items
            return create_items_from_count_list(realm, res_counts)

        def fill_mixed(realm):
            res_counts = []
            while sum(res_counts) < 10:
                res_counts.append(round(self.random.triangular(0.5, 5.5, 2)))
            for i in range(self.options.rabbit_extra_items.value):
                res_counts.append(round(self.random.triangular(0.5, 5.5, 2)))
            return create_items_from_count_list(realm, res_counts)

        realms = rabbit_realms
        rabbit_items = {}
        if self.options.rabbitsanity.value == 1:  # Vanilla
            # print(f"Vanilla rabbits {self.rabbit_counts}")
            self.options.rabbit_pack_size.value = 1
            for r, c in zip(realms, self.rabbit_counts):
                vanilla_pool = fill_vanilla(r, c)
                rabbit_items |= vanilla_pool
                self.rabbit_realm_items[r] = vanilla_pool
            return rabbit_items

        if self.options.rabbit_pack_size == -1:  # random_mixed
            for r in realms:
                rabbit_items |= fill_mixed(r)
            return rabbit_items

        # Uniform packs
        if self.options.rabbit_pack_size == 0:  # Random uniform
            pack_sizes = [self.random.randint(1, 5), self.random.randint(1, 5)]
        else:
            pack_sizes = [self.options.rabbit_pack_size.value]*5
        # print(f"Uniform Packs {pack_sizes}")
        for r, s in zip(realms, pack_sizes):
            item_count = math.ceil(10 / s) + self.options.rabbit_extra_items.value
            rabbit_items |= create_items_from_count_list(r, [s]*item_count)
        # print(f"rabbit items: {rabbit_items}")
        return rabbit_items

    def choose_tear_items(self):
        size_index = self.options.tear_size.value
        spirit_weapon = self.options.spirit_weapons.value
        add_items = []

        if not spirit_weapon:
            if self.options.progressive_equipment:
                add_items += [("Sword (Progressive)", 2)]
            else:
                add_items += [("Sword", 1), ("Lokomo Sword", 1)]
            add_items += [("Bow of Light", 1)]
        else:
            add_items += [("Sword", 1)]

        if self.options.exclude_sections == "remove" and len(self.non_required_sections) == 6 and self.options.randomize_tears.value not in [3, 0]:
            return add_items

        if self.options.randomize_tears.value <= 0:
            return add_items

        size_str = ["", "Big "][size_index]
        sections = range(1, 6)
        if self.options.exclude_sections == "remove":
            sections = [s for s in sections if s not in self.non_required_sections]

        tear_sections = self.options.tear_sections.value
        count_normal = [3, 1][size_index]

        if tear_sections == 0 and self.options.randomize_tears not in ["no_tears", "vanilla"]:  # unique section
            add_items += [(f"{size_str}Tear of Light (ToS {section})", count_normal) for section in sections]
            if (self.options.randomize_tears == "in_own_section"
            and self.options.keysanity == "in_own_section"
            and self.options.tear_size == "small"
            and self.tower_section_lookup[6] < 6):
                add_items.pop(-1)
                add_items.append(("Big Tear of Light (ToS 6)", 1))
        elif tear_sections == 1:  # All Sections
            add_items += [(f"{size_str}Tear of Light (All Sections)", count_normal + spirit_weapon)]
        elif tear_sections == 2: # progressive
            section_count = min(self.sections_included, 5)
            count_prog = [section_count*3, section_count][size_index]
            add_items += [(f"{size_str}Tear of Light (Progressive)", count_prog + spirit_weapon)]

        # print(f"New Tear Items: {add_items}")
        return add_items

    def choose_stamp_items(self):
        if self.options.randomize_stamps.value == 0:
            return
        self.stamp_items = [("Stamp Book", 1)]
        if self.options.randomize_stamps.value in [1, 2, 4]:
            return
        if self.options.stamp_pack_sizes.value == 1:
            self.stamp_items += [(s, 1) for s in ITEM_GROUPS["Stamps"]]
            return

        self.stamp_pack_order = list(range(20))
        self.random.shuffle(self.stamp_pack_order)
        if self.options.stamp_pack_sizes.value > 1:
            item_count = math.ceil(20/self.options.stamp_pack_sizes.value)
            self.stamp_items += [(f"Stamp Pack ({self.options.stamp_pack_sizes.value})", item_count)]
        elif self.options.stamp_pack_sizes.value == -1:
            sizes = []
            while sum(sizes) < 20:
                sizes.append(math.floor(self.random.triangular(1, 6, 1)))
            stamp_value_lookup = {ITEMS[name].value: name for name in ITEM_GROUPS["Stamps"]}
            stamp_dict = {i: 0 for i in range(2, 6)}
            for s in sizes:
                if s == 1:
                    self.stamp_items.append((stamp_value_lookup[self.stamp_pack_order.pop()], 1))
                else:
                    stamp_dict[s] += 1
            self.stamp_items += [(f"Stamp Pack ({size})", count) for size, count in stamp_dict.items() if count > 0]


    def create_items(self):
        item_pool_dict = self.build_item_pool_dict()
        self.get_extra_filler_items(item_pool_dict)
        items = []
        for item_name, quantity in item_pool_dict.items():
            for _ in range(quantity):
                items.append(self.create_item(item_name))

        self.filter_confined_dungeon_items_from_pool(items)
        self.multiworld.itempool.extend(items)
        # print(self.multiworld.itempool)

    def get_extra_filler_items(self, item_pool_dict):
        # Create a random list of useful or currency items to turn into filler to satisfy all removed locations
        filler_count = 0
        extra_items_list = []
        for item, count in item_pool_dict.items():
            if 'backup_filler' in ITEMS[item].tags:
                extra_items_list.extend([item] * count)
            if ITEMS[item].classification in [ItemClassification.filler, ItemClassification.trap]:
                filler_count += count

        extra_item_count = len(self.locations_to_exclude) - filler_count + 20
        if extra_item_count > 0:
            self.random.shuffle(extra_items_list)
            self.extra_filler_items = extra_items_list[:extra_item_count]

    # Based on the messenger's plando connection by Aaron Wagner
    def connect_plando(self, plando_pairings) -> None:
        def remove_dangling_exit(region: Region, name: str) -> None:
            # find the disconnected exit and remove references to it
            for _exit in region.exits:
                if not _exit.connected_region and _exit.name == name:
                    break
            else:
                raise ValueError(f"Unable to find randomized transition for {region} {name}")
            # print(f"\tRemoving dangling exit from {region.name}: {_exit.name}")
            region.exits.remove(_exit)

        def remove_dangling_entrance(region: Region, name: str) -> None:
            # find the disconnected entrance and remove references to it
            for _entrance in region.entrances:
                if not _entrance.parent_region and _entrance.name == name:
                    break
            else:
                raise ValueError(f"Invalid target region for {region}")
            # print(f"\tRemoving dangling entr from {region.name}: {_entrance.name}")
            region.entrances.remove(_entrance)

        for entr_name, exit_name in plando_pairings:
            # get the connecting regions
            r1: "STTransition" = ENTRANCES[entr_name]
            reg1 = self.get_region(r1.entrance_region)

            remove_dangling_exit(reg1, entr_name)

            r2 = ENTRANCES[exit_name]
            reg2 = self.get_region(r2.entrance_region)
            remove_dangling_entrance(reg2, exit_name)
            # connect the regions
            reg1.connect(reg2)
            self.plando_pairings[r1.id] = r2.id
            if dev_prints:
                pass
            # print(f"Plando Connecting {r1} => {r2} with regions {reg1} => {reg2}")

            # pretend the user set the plando direction as "both" regardless of what they actually put on coupled
            if True:
                remove_dangling_exit(reg2, exit_name)
                remove_dangling_entrance(reg1, entr_name)
                reg2.connect(reg1)
                self.plando_pairings[r2.id] = r1.id
                if dev_prints:
                    print(f"Connecting backwards {r2} => {r1}")

    @staticmethod
    def in_pool(p, etype: int) -> int | None:
        # print(f"Pools: {p} etype {etype}")
        for i in range(4):
            if etype in p[i]:
                return i
        return None


    def create_er_target_groups(self, type_option_lookup, pools):
        unique_groups = {entrance.randomization_group for entrance in self.multiworld.get_entrances(self.player)
                         if entrance.parent_region and not entrance.connected_region}
        # print(f"Unique Groups: {decode_recursive(unique_groups)}")

        def get_target_groups(g: int) -> list[int]:
            direction = g & EntranceGroups.DIRECTION_MASK
            etype = (g & EntranceGroups.AREA_MASK) >> 3
            pool = self.in_pool(pools, etype)
            dungeon = (g & EntranceGroups.DUNGEON_MASK) >> 8
            # print(f"\t{direction}_{etype}_{pool}")

            # Choose target entrance types from pool options
            if pool is not None:
                target_etyps = pools[pool]
            else:
                target_etyps = [etype]

            # Choose target directions
            if (direction == 0
                or (pool is not None and pool_name_lookup[pool] not in self.options.entrance_directionality.value)
                or (pool is None and directionality_etype_lookup[etype] not in self.options.entrance_directionality.value)):
                target_directions = range(5)
            else:
                target_directions = [0, OPPOSITE_ENTRANCE_GROUPS[direction]]

            # choose target dungeon
            if pool == 3 and dungeon:
                target_dungeons = [0, dungeon]
            else:
                target_dungeons = range(12)

            res = []
            # print(f"\t\tTarget dirs: {target_directions}")
            # print(f"\t\tTarget etypes: {target_etyps}")
            # if dungeon:
                # print(f"\t\tTarget dungeons: {target_dungeons}")
            for d in target_directions:
                for t in target_etyps:
                    for dung in target_dungeons:
                        new_group = d | (t << 3) | (dung << 8)
                        # print(f"Try match: {decode_entrance_groups(new_group)}")
                        if new_group in unique_groups:
                            res.append(new_group)
            return res
        return bake_target_group_lookup(self, get_target_groups)

    def connect_entrances(self) -> None:
        starting_region = ENTRANCES[self.starting_entrance].entrance_region
        self.get_region("menu").connect(self.get_region(starting_region), "Warp to Start")
        # print(f"Starting entrance: {self.starting_entrance}")

        if self.is_ut:
            disconnect_ids = {int(i) for i in self.ut_pairings.keys()}
            las_ow = ENTRANCES["Lost at Sea Lobby Enter Dungeon One-Way"].id
            if las_ow in disconnect_ids:
                disconnect_ids.remove(las_ow)
            for e in self.valid_entrances:
                if ENTRANCES[e.name].id in disconnect_ids:
                    # print(f"Disconnecting {e.name}")
                    target_name = ENTRANCES[e.name].vanilla_reciprocal.name
                    disconnect_entrance_for_randomization(e, one_way_target_name=target_name)
            if getattr(self.multiworld, "enforce_deferred_connections", "default") == "off":
                # print(f"Reconnecting entrances {self.ut_pairings}")
                for i, pairing in self.ut_pairings.items():
                    try:
                        _exit: "Entrance" = self.get_entrance(entrance_id_to_entrance[int(i)].name)
                    except KeyError:
                        continue
                    entrance_region: "Region" = self.get_region(entrance_id_to_region[pairing])
                    _exit.connect(entrance_region)
            return

        # Choose entrances to shuffle based on settings
        type_option_lookup = {
            0: 0,  # Plando entrances
            1: self.options.shuffle_houses,
            2: self.options.shuffle_caves,
            3: self.options.shuffle_stations,
            4: self.options.shuffle_overworld,
            5: self.options.shuffle_dungeon_entrances,
            6: self.options.shuffle_bosses,
            7: self.options.shuffle_dungeon_rooms,
            8: self.options.shuffle_warps,
            9: self.options.shuffle_portals,
            11: self.options.shuffle_tos_sections,
            12: self.options.shuffle_train_transitions,
            14: self.options.shuffle_tos_staircase,
            15: self.options.shuffle_hyrule_castle,
            16: self.options.shuffle_disorientation,
            17: self.options.shuffle_eote,
            18: self.options.shuffle_las
        }
        none_option_types = {  # when assigning direction pairings to NONE-directional entrances, these are the directions for each etype
            0: [1, 2, 3, 4],
            1: [3, 4],
            2: [3, 4],
            3: [3, 4],
            4: [1, 2, 3, 4],
            5: [3, 4],
            6: [3, 4],
            7: [3, 4],
            8: [3, 4],
            9: [1, 2, 3, 4],
            11: [3, 4],
            12: [1, 2, 3, 4],
            14: [3, 4],
            15: [3, 4],
            16: [1, 2, 3, 4],
            17: [3, 4],
            18: [3, 4],
        }

        plando_disconnects: set[str] = set()

        # Change entrance groups for pre-chosen dungeon pairings
        for dung, boss in self.shuffled_bosses.items():
            if boss not in BOSS_LOCATION_TO_ENTRANCE:
                continue
            # Change dungeon for the boss' entrance randomization group to the newly shuffled one
            entrance = self.get_entrance(BOSS_LOCATION_TO_ENTRANCE[boss])
            entrance.randomization_group = (entrance.randomization_group & EntranceGroups.NON_DUNGEON_MASK) + \
                                           (dungeon_to_enum[dung] << 8)
            # print(f"New Target group: {entrance} {decode_entrance_groups(entrance.randomization_group)}")
        if self.shuffled_dungeon_lookup:
            # print(f"Shuffled dungeon lookup: {self.shuffled_dungeon_lookup}")
            for dung, entr in DUNGEON_LOBBY_ENTRANCES.items():
                for e in entr:
                    entrance = self.get_entrance(e)
                    entrance.randomization_group = (entrance.randomization_group & EntranceGroups.NON_DUNGEON_MASK) + \
                                                   (dungeon_to_enum[self.shuffled_dungeon_lookup[dung]] << 8)
                    # print(f"New Target group: {entrance} {decode_entrance_groups(entrance.randomization_group)}")
            if self.options.shuffle_warps.value == 0:
                plando_disconnects.update(DUNGEON_TO_WARP_ENTRANCE.values())
                plando_disconnects.update(DUNGEON_TO_WARP_EXIT.values())

        # Filter active entrances
        entrances_to_shuffle: list["Entrance"] = []
        directionless_entrances: list["Entrance"] = []
        for i in self.options.plando_transitions.value:
            plando_disconnects.add(i.entrance)
            plando_disconnects.add(ENTRANCES[i.entrance].vanilla_reciprocal.name)
            plando_disconnects.add(i.exit)
            plando_disconnects.add(ENTRANCES[i.exit].vanilla_reciprocal.name)
        for e in self.valid_entrances:
            if type_option_lookup.get((e.randomization_group & EntranceGroups.AREA_MASK) >> 3, False):
                entrances_to_shuffle.append(e)
                # print(f"ER: {e.name} {bin(e.randomization_group)} {(e.randomization_group & EntranceGroups.AREA_MASK) >> 3}")
                if e.randomization_group & 7 == 0 :
                    directionless_entrances.append(e)
            elif e.name in plando_disconnects:
                entrances_to_shuffle.append(e)
                e.randomization_group = 0
                directionless_entrances.append(e)
                # print(f"Plando ER: {e.name} {bin(e.randomization_group)} {(e.randomization_group & EntranceGroups.AREA_MASK) >> 3}")

        # print("no of entrances:", len(entrances_to_shuffle), entrances_to_shuffle)

        # Get pool data
        pools = [[], [], [], []]
        for a, option in type_option_lookup.items():
            if a == 0: continue
            pool_norm = option.value - 2
            if 0 <= pool_norm <= 3:
                pools[pool_norm].append(a)
            elif pool_norm == 4:  # the dungeon pool has 2 options
                pools[3].append(a)

        # Assign direction pairs do directionless entrances
        directional_pool_cache = {}
        # print(f"Directionless entrances: {directionless_entrances}")
        for i in range(len(directionless_entrances)//2):

            # Figure out what directions exist in their pool
            current_etype = (directionless_entrances[i*2].randomization_group & EntranceGroups.AREA_MASK) >> 3
            if current_etype in directional_pool_cache:
                if directional_pool_cache[current_etype] is None:
                    continue
                direction_choice = directional_pool_cache[current_etype]
            else:
                pool = self.in_pool(pools, current_etype)
                if pool is None:
                    if directionality_etype_lookup[current_etype] not in self.options.entrance_directionality.value:
                        directional_pool_cache[current_etype] = None
                        continue  # direction doesn't matter!
                    direction_choice = none_option_types[current_etype]
                    directional_pool_cache[current_etype] = direction_choice
                else:
                    if pool_name_lookup[pool] not in self.options.entrance_directionality.value:
                        directional_pool_cache[current_etype] = None
                        continue  # direction doesn't matter!
                    direction_choice = set()
                    for j in pools[pool]:
                        direction_choice |= set(none_option_types[j])
                    direction_choice = list(direction_choice)
                    directional_pool_cache[current_etype] = direction_choice

            new_direction = self.random.choice(direction_choice)
            directionless_entrances[i*2].randomization_group |= new_direction
            directionless_entrances[i*2+1].randomization_group |= OPPOSITE_ENTRANCE_GROUPS[new_direction]
            # print(f"Setting new group: {directionless_entrances[i*2]} => {decode_entrance_groups(directionless_entrances[i*2].randomization_group)} {direction_choice}")

        # Disconnect entrances to shuffle
        for entrance in entrances_to_shuffle:
            if dev_prints:
                print(f"Disconnecting {entrance.name}")
            target_name = ENTRANCES[entrance.name].vanilla_reciprocal.name
            disconnect_entrance_for_randomization(entrance, one_way_target_name=target_name)

        # Get target groups
        groups = self.create_er_target_groups(type_option_lookup, pools)
        # print(f"Shuffling Entrances {entrances_to_shuffle} with groups {decode_recursive(groups)}")

        # Entrance Plando
        plando_data: list[tuple[str, str]] = []
        if self.tower_pairings:
            plando_data += self.tower_pairings
        if self.options.plando_transitions.value:
            plando_data += [(e.entrance, e.exit) for e in self.options.plando_transitions]
        if self.options.shuffle_dungeon_entrances.value == 1:
            # print(f"Shuffled dungeons: {self.shuffled_dungeon_lookup}")
            plando_data += [(DUNGEON_TO_ENTRANCE[dung_old], DUNGEON_TO_EXIT[dung_new])
                           for dung_old, dung_new in self.shuffled_dungeon_lookup.items()]
        if self.shuffled_dungeon_lookup and self.options.shuffle_warps.value == 0:
            plando_data += [(DUNGEON_TO_WARP_ENTRANCE[dung_old], DUNGEON_TO_WARP_EXIT[dung_new])
                           for dung_old, dung_new in self.shuffled_dungeon_lookup.items()]
        if self.shuffled_bosses and self.options.shuffle_bosses.value == 1:
            plando_data += [(DUNGEON_TO_BOSS_STAIRCASE[dung], BOSS_LOCATION_TO_EXIT[boss]) for dung, boss in self.shuffled_bosses.items()]
        # print(f"Plando Data: {plando_data}")
        self.connect_plando(plando_data)

        # Randomize Entrances
        st_max_er_attempts = self.options.entrance_shuffle_retries.value
        coupled = not self.options.decouple_shuffled_entrances.value
        for i in range(st_max_er_attempts):
            try:
                self.er_placement_state = randomize_entrances(self, coupled, groups)
                # print(f"ER Placements: {self.er_placement_state.pairings}")
                break
            except EntranceRandomizationError as error:
                if st_max_er_attempts > 5 and i % 5 == 4:
                    print(f"Spirit tracks failed ER {i+1} time(s), retrying")
                if i >= st_max_er_attempts - 1:
                    raise EntranceRandomizationError(
                        f"Spirit Tracks: failed GER after {st_max_er_attempts} attempts.")
                # disconnect entrances again, but only if they got connected before
                for region in self.get_regions():
                    # print(f"\tRegion: {region} | exits {[e for e in region.get_exits()]}")
                    for _exit in region.get_exits():
                        if (_exit.parent_region
                                and _exit.connected_region
                                and _exit in entrances_to_shuffle):
                            # print(f"Disconnecting entrance {_exit} {_exit.randomization_group}")
                            target_name = ENTRANCES[_exit.name].vanilla_reciprocal.name
                            disconnect_entrance_for_randomization(_exit, one_way_target_name=target_name)

    def generate_basic(self) -> None:
        # Add bonus rules based on entrance placement
        pairings = {}
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id
        pairings |= self.plando_pairings
        pairings |= {int(k): v for k, v in self.ut_pairings.items()}

        # las triple entrance
        if ENTRANCES["Lost at Sea Lobby Enter Dungeon"].id in pairings:
            entering_entr = pairings.get(ENTRANCES["Lost at Sea Dungeon Reward Room Warp"].id, 0)
            if entering_entr:
                entr_name = entrance_id_to_entrance[entering_entr].name
                self.set_rule(self.get_entrance("Lost at Sea Lobby Enter Dungeon One-Way"), self.get_entrance(entr_name).access_rule)


    def redirect_boss_warps(self, pairings: dict[int, int]):
        # post shuffle force connections
        if self.options.shuffle_bosses.value or self.options.shuffle_dungeon_rooms.value or self.options.shuffle_dungeon_entrances.value:
            if self.options.shuffle_bosses.value:
                self.plando_pairings |= {ENTRANCES[boss_warp].id: pairings.get(ENTRANCES[boss_exit].id, ENTRANCES[boss_exit].vanilla_reciprocal.id)
                                         for boss_exit, boss_warp in BOSS_EXIT_TO_BOSS_WARP.items()}
            else:
                entrance_names = {boss_warp: ENTRANCES[boss_exit].vanilla_reciprocal.name
                                  for boss_exit, boss_warp in BOSS_EXIT_TO_BOSS_WARP.items()}
                self.plando_pairings |= {ENTRANCES[boss_warp].id: ENTRANCES[boss_exit].id
                                         for boss_warp, boss_exit in entrance_names.items()}

        # Lost at sea matching
        las_entrance = ENTRANCES["Lost at Sea Lobby Enter Dungeon"].id
        las_exit = ENTRANCES["Lost at Sea Dungeon Reward Room Warp"].id
        if las_entrance in pairings:
            self.plando_pairings[ENTRANCES["Lost at Sea Lobby Enter Dungeon One-Way"].id] = pairings[las_entrance]
            self.plando_pairings[pairings[las_exit]] = ENTRANCES["Lost at Sea Dungeon Plain Phantom Spawn"].id


    def get_pre_fill_items(self):
        return self.pre_fill_items

    def pre_fill(self) -> None:
        self.pre_fill_tos_sections()
        self.pre_fill_dungeon_items()

    def filter_confined_dungeon_items_from_pool(self, items: List[SpiritTracksItem]):
        confined_dungeon_items = []


        # Confine small keys and boss key to own dungeon if option is enabled
        if self.options.keysanity in ["in_own_dungeon", "in_own_section"]:
            confined_dungeon_items.extend([item for item in items if item.name.startswith("Small Key") or item.name.startswith("Keyring (")])

        if self.options.randomize_boss_keys in ["in_own_dungeon", "in_own_section"]:
            confined_dungeon_items.extend([item for item in items if item.name in ITEM_GROUPS["Boss Keys"]])

        if self.options.randomize_tears in ["in_own_section", "in_tos"]:
            confined_dungeon_items.extend([item for item in items if item.name in ITEM_GROUPS["Tears of Light"]])

        # Filter out starting inventory items, borrowed from EternalCode's Minish cap implementation
        start_inv = self.options.start_inventory_from_pool.value
        known_start_inv = {}
        def keep_item(s):
            known_start_inv[s] = known_start_inv.get(s, 0) + 1
            return s not in start_inv or known_start_inv[s] > start_inv[s]
        confined_dungeon_items = [i for i in confined_dungeon_items if keep_item(i.name)]

        for item in confined_dungeon_items:
            items.remove(item)

        self.pre_fill_items.extend(confined_dungeon_items)
        # print(f"Pre fill items {self.pre_fill_items}")

    def pre_fill_tos_sections(self):
        for section in range(1, 7):
            section_names = [name for name, loc in LOCATIONS_DATA.items()
                             if loc.get("tos_section", 0) == section]
            section_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in section_names and not loc.locked]

            section_items = []
            if self.options.keysanity == "in_own_section":
                section_items += [item for item in self.pre_fill_items if item.name == f"Small Key (ToS {section})" or item.name == f"Keyring (ToS {section})"]
            if self.options.randomize_boss_keys == "in_own_section":
                section_items += [item for item in self.pre_fill_items if item.name == f"Boss Key (ToS {section})"]
            if self.options.randomize_tears == "in_own_section":
                section_items += [item for item in self.pre_fill_items if item.name.endswith(f"Tear of Light (ToS {section})")]

            if len(section_locations) == 0:
                continue
            # print(f"Pre filling section {section}: {section_items}")
            # print(f"\tlocations {section_locations}")
            # Remove from the all_state the items we're about to place
            for item in section_items:
                self.pre_fill_items.remove(item)
            collection_state = self.multiworld.get_all_state(False)
            # Perform a prefill to place confined items inside locations of this dungeon
            self.random.shuffle(section_locations)
            # print(f"Pre filling section {section}: {section_items} to {section_locations}")
            fill_restrictive(self.multiworld, collection_state, section_locations, section_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def pre_fill_dungeon_items(self):
        # If keysanity is off, dungeon items can only be put inside local dungeon locations, and there are not so many
        # of those which makes them pretty crowded.
        # This usually ends up with generator not having anywhere to place a few small keys, making the seed unbeatable.
        # To circumvent this, we perform a restricted pre-fill here, placing only those dungeon items
        # before anything else.
        for dung_name in DUNGEON_NAMES:
            # Build a list of locations in this dungeon
            # print(f"Pre-filling {dung_name}")
            dungeon_location_names = [name for name, loc in LOCATIONS_DATA.items()
                                      if "dungeon" in loc and loc["dungeon"] == dung_name]
            dungeon_location_names += [name for name, dung in self.near_dungeon_lookup.items() if dung == dung_name]

            dungeon_locations = [loc for loc in self.multiworld.get_locations(self.player)
                                 if loc.name in dungeon_location_names and not loc.locked]

            # From the list of all dungeon items that needs to be placed restrictively, only filter the ones for the
            # dungeon we are currently processing.
            confined_dungeon_items = [item for item in self.pre_fill_items
                                      if item.name.endswith(f"({dung_name})")]
            if dung_name == "ToS":
                if self.options.keysanity == "in_own_dungeon":
                    confined_dungeon_items += [item for item in self.pre_fill_items
                                          if item.name.startswith("Small Key (ToS") or item.name.startswith("Keyring (ToS")]
                if self.options.randomize_boss_keys == "in_own_dungeon":
                    confined_dungeon_items += [item for item in self.pre_fill_items
                                          if item.name.startswith("Boss Key (ToS")]
                if self.options.randomize_tears == "in_tos":
                    confined_dungeon_items += [item for item in self.pre_fill_items
                                          if "Tear of Light" in item.name]
            # print(f"pre filling {dung_name}: {confined_dungeon_items}")
            # print(f"\tlocations {dungeon_location_names}")
            if len(confined_dungeon_items) == 0:
                continue  # This list might be empty with some keysanity options

            # Remove from the all_state the items we're about to place
            for item in confined_dungeon_items:
                self.pre_fill_items.remove(item)
            collection_state = self.multiworld.get_all_state(False)
            # Perform a prefill to place confined items inside locations of this dungeon
            self.random.shuffle(dungeon_locations)
            #print(f"{dungeon_locations}, {confined_dungeon_items}")
            fill_restrictive(self.multiworld, collection_state, dungeon_locations, confined_dungeon_items,
                             single_player_placement=True, lock=True, allow_excluded=True)

    def get_filler_item_name(self) -> str:
        filler_item_names = list(ITEM_GROUPS["Common Treasures"] |
                             # ITEM_GROUPS["Uncommon Treasures"] |
                             ITEM_GROUPS["Refill Items"] |
                             ITEM_GROUPS["Small Rupees"]
                             ) + ["Big Green Rupee (100)"]
        rare_filler_items = list(ITEM_GROUPS["Potions"])

        # 1/5 chance to roll a rare filler item
        if self.random.randint(1, 15) == 1:
            return self.random.choice(rare_filler_items)
        return self.random.choice(filler_item_names)

    def collect(self, state: CollectionState, item: SpiritTracksItem) -> bool:
        # Code borrowed from Ishigh's early Rule Builder implementation
        change = super().collect(state, item)
        if not change:
            return False

        mapping = self.item_mapping_collect.get(item.name, None)
        if mapping is not None:
            mapping = mapping if isinstance(mapping, list) else [mapping]
            # print(f"Mapping {mapping} {state.prog_items[self.player][mapping[0]]} for item {item.name}")
            for m in mapping:
                state.prog_items[self.player][m[0]] += m[1]

        return True

    def remove(self, state: CollectionState, item: SpiritTracksItem) -> bool:
        change = super().remove(state, item)
        if not change:
            return False

        mapping = self.item_mapping_collect.get(item.name, None)
        if mapping is not None:
            mapping = mapping if isinstance(mapping, list) else [mapping]
            for m in mapping:
                state.prog_items[self.player][m[0]] -= m[1]

        return True

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        player_hint_data = dict()

        pairings = dict()
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id
        pairings |= self.plando_pairings
        if not pairings:  # If not er, don't bother trying anything else
            return

        def create_hint_entrances(key):
            hint_entrances = loc_data[key]
            hint_entrances = [hint_entrances] if isinstance(hint_entrances, str) else hint_entrances
            hint_entrances_ids = [e.id for name, e in ENTRANCES.items() if name in hint_entrances]

            for entrance_id in hint_entrances_ids:
                reverse_id = reverse_pairings.get(entrance_id, None)
                if reverse_id is not None and (reverse_id not in dead_end_ids or self.options.decouple_shuffled_entrances.value):
                    entrance_list.add(entrance_id_to_entrance[reverse_id].name)

        reverse_pairings = {e2: int(e1) for e1, e2 in pairings.items()}
        dead_end_ids = [e.id for name, e in ENTRANCES.items() if name in DEAD_END_ENTRANCES]

        for loc, loc_data in LOCATIONS_DATA.items():
            if "hint_entrance" in loc_data:
                entrance_list = set()
                create_hint_entrances("hint_entrance")
                if not entrance_list and "hint_entrance_secondary" in loc_data:
                    create_hint_entrances("hint_entrance_secondary")
                if not entrance_list and "hint_entrance_tertiary" in loc_data:
                    create_hint_entrances("hint_entrance_tertiary")

                if entrance_list:
                    player_hint_data[loc_data["id"]] = ", ".join(entrance_list)

        hint_data[self.player] = player_hint_data

    def get_location_models(self):
        # get item placement models to send to client
        default_models = {
            2: [
                ITEM_MODEL_LOOKUP["Gold Rupee"].offset,
                ITEM_MODEL_LOOKUP["Blue Rupee"].offset,
                ITEM_MODEL_LOOKUP["Green Rupee"].offset
            ]
        }
        dmi = self.options.multiworld_item_default_models.value

        location_models = {}
        for loc in self.get_locations():
            item = loc.item
            if item is None: continue
            loc_data = LOCATIONS_DATA.get(loc.name, {})
            if not loc_data or 'stamp' in loc_data or 'no_model' in loc_data:
                continue
            if item.game in ["Spirit Tracks"]:
                if ITEMS[item.name].model is not None:
                    location_models[loc_data['id']] = ITEM_MODEL_LOOKUP[ITEMS[item.name].model].offset
                    continue
            elif self.options.multiworld_item_model_swaps and item.game in all_lookups:
                model = all_lookups[item.game].get(item.name, None)
                if model is not None:
                    location_models[loc_data['id']] = model
                    continue

            if dmi in [2]:
                if item.classification & ItemClassification.useful:
                    location_models[loc_data['id']] = default_models[dmi][1]
                elif item.classification & ItemClassification.filler:
                    location_models[loc_data['id']] = default_models[dmi][2]
            if item.classification & ItemClassification.trap:
                location_models[loc_data['id']] = ITEM_MODEL_LOOKUP["Stalfos Skull"].offset

        return location_models
        # print(f"Location Models: {location_models}")

    def fill_slot_data(self) -> dict:
        options = ["goal", "compass_shard_count",
                   "logic", "cannon_logic",
                   "exclude_dungeons", "exclude_sections", "require_specific_dungeons", "dungeon_hints",
                   "keysanity", "randomize_boss_keys",
                   "big_keyrings",
                   "randomize_minigames", "minigame_hints",
                   "rabbitsanity", # "rabbit_hints",
                   "randomize_passengers", "passenger_pickup", "randomize_cargo",
                   "exclude_locations",
                   "portal_behavior", "portal_checks",
                   "randomize_tears", "spirit_weapons", "tear_sections",
                   "dark_realm_access", "endgame_scope", "dungeons_required",
                   "starting_train", "multiworld_item_default_models",
                   "randomize_stamps", "open_blizzard_temple", "open_blue_warps",
                   "tos_section_unlocks", "tos_unlock_base_item", "shuffle_tos_sections", "tos_shortcuts",
                   "shopsanity", "shop_hints", "rupee_farming_logic", "excess_random_treasure",
                   "shuffle_houses", "shuffle_caves", "shuffle_disorientation",  # for map switching
                   "shuffle_stations", "shuffle_overworld",  # used to disable dynamic flags
                   "shuffle_hyrule_castle",  # prevent zelda warp
                   "shuffle_portals", "shuffle_eote",  # include eote locs if shuffled
                   "shuffle_train_transitions",  # for desert rocktite cannon logic lol
                   "shuffle_dungeon_rooms", "shuffle_warps", "shuffle_bosses", "shuffle_dungeon_entrances",
                   "decouple_shuffled_entrances",
                   "death_link", "enable_map_warp", "extra_events",
                   "free_starting_items",
                   "ut_blocked_entrances_behaviour"]
        slot_data = self.options.as_dict(*options)
        slot_data["active_rabbit_locs"] = [LOCATIONS_DATA[loc]["id"] for loc in self.active_rabbit_locations]
        slot_data["required_boss_locs"] = [self.location_name_to_id[i] for i in self.required_boss_locs]
        slot_data["stamp_pack_order"] = self.stamp_pack_order
        slot_data["model_lookup"] = self.get_location_models()
        slot_data["exclude_tos_5"] = self.exclude_tos_5
        slot_data["non_required_dungeons"] = self.non_required_dungeons
        slot_data["non_required_sections"] = self.non_required_sections
        slot_data["starting_entrance"] = self.starting_entrance
        pairings = {}
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id
        self.redirect_boss_warps(pairings)
        pairings |= self.plando_pairings
        slot_data["er_pairings"] = pairings
        slot_data["tower_section_lookup"] = self.tower_section_lookup
        slot_data["section_count"] = self.sections_included
        # print(f"ER Pairings: {pairings}")

        return slot_data

    def write_spoiler(self, spoiler_handle):
        if self.options.dark_realm_access in ["dungeons", "both"]:
            title_str = "Required Dungeons" if self.options.require_specific_dungeons else "Dungeon Locations"
            spoiler_handle.write(f"\n\n{title_str} ({self.multiworld.player_name[self.player]}):\n")
            for dung in self.required_boss_locs:
                spoiler_handle.write(f"\t- {dung}\n")

        pairings: dict[int, int] = {}
        if self.er_placement_state:
            for e1, e2 in self.er_placement_state.pairings:
                pairings[ENTRANCES[e1].id] = ENTRANCES[e2].id
        self.redirect_boss_warps(pairings)
        pairings |= self.plando_pairings
        if pairings:
            spoiler_handle.write(f"\n\nEntrance Randomization ({self.multiworld.player_name[self.player]}):\n")
            entrance_formatter: dict[int, list] = {}
            for e1, e2 in pairings.items():
                if e2 in entrance_formatter and entrance_formatter[e2][1] == entrance_id_to_entrance[e1].name:
                    entrance_formatter[e2][2] = True
                else:
                    entrance_formatter[e1] = [entrance_id_to_entrance[e1].name, entrance_id_to_entrance[e2].name, False]
            for e1, e2, two_way in entrance_formatter.values():
                arrow = "<=>" if two_way else "=>"
                spoiler_handle.write(f"\t{e1} {arrow} {e2}\n")

    # UT stuff
    @staticmethod
    def interpret_slot_data(slot_data: dict[str, Any]):
        return slot_data

    def ut_add_warp_connection(self, key, stored_data):
        """Create direct connections to map warp locations for glp"""
        if not self.options.enable_map_warp.value or not self.settings.get('ut_get_logical_path_shortcuts', True):
            print(f"Map warp shortcuts disabled.")
            return
        if "st_visited_scenes" in key:
            new_scenes = set(stored_data) - self.ut_visited_scenes
            self.ut_visited_scenes |= new_scenes
            for scene in new_scenes:
                reg = self.get_region(WARP_SCENES[scene].region)
                print(f"Connecting map warp: {reg}")
                self.get_region("menu").connect(reg, f"Map Warp to {reg.name}")


    def reconnect_found_entrances(self, key, stored_data):
        print(f"UT Tried to defer entrances! key {key}"
              f" {stored_data}")

        if not stored_data: return

        self.ut_add_warp_connection(key, stored_data)

        if getattr(self.multiworld, "enforce_deferred_connections", "default") == "off":
            print(f"Don't defer entrances when off")
            return

        def connect(connection):
            pairing = self.ut_pairings.get(str(connection), None)
            # print(f"Pairing {pairing} {entrance_id_to_entrance[i].name}")
            if pairing is not None:
                exit_name = entrance_id_to_entrance[connection].name
                try:
                    _exit: "Entrance" = self.get_entrance(exit_name)
                except KeyError:
                    return
                entrance_region: "Region" = self.get_region(entrance_id_to_region[pairing])
                print(f"Connecting: {_exit} => {entrance_region} | {connection}: {pairing}")
                _exit.connect(entrance_region)

                if exit_name == "EVENT: Goron Village Bring Ice to Kagoron":
                    self.get_region("goron village").connect(self.get_region("goron ice"))

                if exit_name in boss_events or exit_name in cargo_events:
                    print(f"Globally connecting outset village => {_exit.parent_region}")
                    self.get_region("menu").connect(_exit.parent_region)

                if "silent_event" in ENTRANCES[exit_name].extra_data:
                    from rule_builder.rules import True_
                    print(f"Setting blank rule for silent entrance {_exit} -> {entrance_region}")
                    self.set_rule(_exit, True_())
            else:
                entr = entrance_id_to_entrance[connection]
                if "silent_event" in entr.extra_data:
                    print(f"Connecting silent entrance: {entr.entrance_region} -> {entr.exit_region}")
                    self.get_region(entr.entrance_region).connect(self.get_region(entr.exit_region))

        def disconnect(connection):
            entr_id = connection
            if str(entr_id) not in self.ut_pairings or entr_id in self.ut_traversed_entrances:
                return
            e = self.get_entrance(entrance_id_to_entrance[entr_id].name)
            if (entr_id in stored_data and e.parent_region and e.connected_region
                    and entr_id in self.ut_checked_entrances
                    and entr_id not in self.ut_traversed_entrances):
                print(f"Disconnecting {e.name}")
                child_region = e.connected_region
                parent_region = e.parent_region

                # disconnect the edge
                child_region.entrances.remove(e)
                e.connected_region = None
                # Create target
                parent_region.create_er_target(e.name)

        if "st_traversed_entrances" in key:
            new_connections = set(stored_data) - self.ut_traversed_entrances
            self.ut_traversed_entrances.update(new_connections)
            for i in new_connections:
                connect(i)

        elif "st_redisconnected_entrances" in key:
            if not self.ut_traversed_entrances:
                return
            new_connections = set(stored_data) - self.ut_traversed_entrances
            self.ut_redisconnected_entrances.update(new_connections)
            for i in new_connections:
                disconnect(i)

        elif "st_checked_entrances" in key:
            new_connections = set(stored_data) - self.ut_checked_entrances
            self.ut_checked_entrances |= new_connections
            for i in new_connections:
                if i not in self.ut_redisconnected_entrances:
                    connect(i)

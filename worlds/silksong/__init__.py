from __future__ import annotations

from .options import get_silk_and_soul_points
from .eva import EVA_POINT_SOURCES

from copy import deepcopy
import random
from collections import Counter, deque
from typing import ClassVar, Union, Any

from BaseClasses import (
    CollectionState,
    Item,
    ItemClassification,
    Region,
    Tutorial,
)

from Options import OptionError
from rule_builder.rules import Has
from worlds.AutoWorld import WebWorld, World
from rule_builder.cached_world import CachedRuleBuilderWorld
from settings import FilePath, Group

from .act1_scope import (
    ACT_ONE_GOAL_KEY,
    get_act_one_excluded_location_names,
)
from .act2_scope import (
    ACT_THREE_ONLY_GOAL_LOCATION_NAMES,
    ACT_TWO_GOAL_KEY,
    CURSED_ENDING_GOAL_KEY,
    get_act_two_excluded_location_names,
)
from .enemy_souls import required_pool_items as enemy_soul_required_pool_items
from .alphabet_mode import (
    ALPHABET_ITEM_NAMES,
    SPELLING_BEE_GOAL_KEY,
    parse_spelling_bee_phrase,
)
from .category_fill import prefill_category_shuffles
from .display_names import FLEA_ITEM_NAMES
from .items import (
    ACT_TWO_START_WITH_MAP_ITEMS,
    AUTOMATIC_COMPASS_ITEM,
    OPTIONAL_START_REPLACEMENT_ITEM,
    POOL_ONLY_USEFUL_ITEM_NAMES,
    QUILL_ITEM,
    PROGRESSIVE_SWIFT_STEP_ITEM,
    START_WITH_MAP_ITEMS,
    STARTING_CREST_ITEM_BY_KEY,
    TRAP_ITEM_NAME_BY_WEIGHT_OPTION,
    TRAP_ITEM_NAMES,
    ItemPoolEntry,
    SilksongItem,
    build_item_pool_entries,
    get_act_one_start_with_map_items,
    get_configured_item_pool_size,
    get_dynamic_trap_capacity,
    get_vanilla_reward_name,
    item_data_table,
    item_name_groups,
    item_table,
)
from .locations import (
    INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES,
    LOCATION_NAMES_BY_CATEGORY,
    NEEDLE_UPGRADE_LOCATION_CATEGORY,
    PALE_OIL_LOCATION_CATEGORY,
    OBSERVATION_LOCATION_CATEGORIES,
    PAIRED_LOCATION_CATEGORIES,
    PINMASTER_OIL_QUEST_LOCATION,
    WISH_REWARD_LOCATION_BY_COMPLETION,
    RELIC_TURN_IN_LOCATION_CATEGORY,
    SCROUNGE_RELIC_ITEM_NAMES,
    VOLATILE_FLINTBEETLES_QUEST_LOCATION,
    SilksongLocation,
    canonicalize_location_name,
    wish_offer_display_name,
    location_data_table,
    location_name_groups,
    location_table,
)
from .minor_families import (
    MINOR_FAMILY_BY_LOCATION,
    MINOR_FAMILY_OPTION_BY_KEY,
    get_minor_family_category,
)
from .native_regions import (
    choose_location_anchor,
    connect_native_logic_regions,
    create_native_logic_region_map,
    native_source_requires_assumption,
)
from .options import (
    CATEGORY_OPTION_BY_LOCATION_CATEGORY,
    SilksongOptions,
    silksong_option_groups,
    get_aggregate_minor_mode_key,
    get_category_mode_key,
    get_minor_family_modes,
)
from .prices import (
    PRICE_CATEGORY_OPTION_NAMES,
    PRICE_MODE_KEYS,
    get_shell_shard_donation_tool_pouch_requirements,
    resolve_purchase_prices,
)
from .requirements import (
    CREST_SLOT_LOCATION_NAMES,
    CRAWFATHER_LOCATION,
    FLEA_HUNT_GOAL_KEY,
    JUDGE_BELL_ITEMS,
    JUNK_ONLY_LOCATIONS,
    BUGS_OF_PHARLOOM_REWARD_LOCATIONS,
    LOGIC_UNKNOWN_LOCATIONS,
    MAX_FLEA_HUNT_GOAL_COUNT,
    MEMORY_LOCKET_ITEM,
    MIN_FLEA_HUNT_GOAL_COUNT,
    OPTION_DEPENDENT_CREST_SLOT_ITEM_NAMES,
    POLLIP_HEART_COUNT,
    ROSARY_BANK_GATED_LOCATIONS,
    ROOM_CHECK_REQUIREMENTS,
    SIMPLE_KEY_GREEN_PRINCE,
    SIMPLE_KEY_ROSARY_BANK,
    THREEFOLD_MELODY_ITEMS,
    export_abstract_requirements,
    export_logic_item_dependencies,
    export_requirements,
    export_wish_logic_events,
    get_location_requirements,
    get_logic_item_references,
    get_mapper_option_quarantines,
    MAPPER_GRAPH_ENABLED,
    normalize_trails_end_requirement,
)
from .wish_events import (
    SILK_AND_SOUL_FULL_POINT_EVENTS,
    SILK_AND_SOUL_HALF_POINT_EVENTS,
    SILK_AND_SOUL_WISH_POINT_ITEM,
    SILK_AND_SOUL_WISH_HALF_POINT_ITEM,
    WISH_LOGIC_EVENTS,
    WISH_REGION_SOURCE_LOCATIONS,
)
from .rules import (
    enforce_global_shuffle_item_rules,
    finalize_crest_slot_memory_locket_logic,
    get_active_crest_slot_locations,
    get_crest_slot_memory_locket_count,
    get_crest_slot_progression_item_count,
    restore_global_shuffle_item_rules,
    set_silksong_rules,
    uses_crest_slot_locket_logic,
    uses_randomized_memory_lockets_for_crest_slots,
)
from .version import WORLD_VERSION
from .vog_hints import (
    build_vog_hint_plan,
    copy_vog_hint_plan,
    empty_vog_hint_plan,
)
from .tracker.mapping import ut_page_index, tracker_map_groups

__version__ = WORLD_VERSION

LOGIC_PAYLOAD_FIELDS = (
    "requirements",
    "abstract_requirements",
    "logic_item_dependencies",
    "logic_events",
)
LOGIC_UNKNOWN_REGION_NAME = "LogicUnknown"
TRACKER_OPTION_NAMES = tuple(
    name for name in SilksongOptions.__annotations__
    if name not in {"starting_crest", "vog_area_hints", "trap_percentage", "wish_plando", *TRAP_ITEM_NAME_BY_WEIGHT_OPTION}
) + ("start_inventory", "exclude_locations")

class SilksongSettings(Group):
    class UTPackPath(FilePath):
        required = False
        ut_dialog_name = "Select Data Pack"

    ut_pack_path: Union[str,UTPackPath] = UTPackPath()


class SilksongWebWorld(WebWorld):
    theme = "ocean"
    option_groups = silksong_option_groups
    tutorials = [
        Tutorial(
            tutorial_name="Multiworld Setup Guide",
            description="How to generate and connect a Hollow Knight: Silksong MultiworldGG seed.",
            language="English",
            file_name="setup_en.md",
            link="setup/en",
            authors=["BatAtVideoGames"],
        )
    ]


class SilksongWorld(CachedRuleBuilderWorld):
    """Hollow Knight: Silksong item randomizer support for the uploaded BepInEx client."""

    game = "Hollow Knight: Silksong"
    topology_present = True
    ut_can_gen_without_yaml = True
    author = "BatAtVideoGames"
    web = SilksongWebWorld()
    options_dataclass = SilksongOptions
    options: SilksongOptions
    settings: ClassVar[SilksongSettings]

    item_name_to_id = item_table
    from .enemy_souls import CATALOGUE as _enemy_catalogue
    location_name_to_id = {**location_table, **{'First Kill: ' + row['name']: row['location_id'] for row in _enemy_catalogue}}
    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    _tracker_world: ClassVar[dict[str, Any]] = {
        "external_pack_key": "ut_pack_path",
        "map_page_folder": "tracker",
        "map_page_maps":"maps.json",
        "map_page_locations":"locations.json",
        "map_page_index": ut_page_index,
        "map_page_setting_key": "Silksong:CurrentRoom:{team}:{player}",
        "map_page_groups": tracker_map_groups
    }

    required_client_version = (0, 6, 0)
    _resolved_content_scope: str | None = None
    _resolved_starting_crest: str | None = None
    _resolved_trap_counts: dict[str, int] | None = None
    _crest_slot_memory_locket_count: int | None = None
    _vog_hint_plan: dict[str, object] | None = None

    @classmethod
    def rule_from_dict(cls, data):
        from . import requirement_rules as _requirement_rules, silk_supply as _silk_supply

        del _requirement_rules, _silk_supply
        return super().rule_from_dict(data)

    def register_rule_dependencies(self, resolved_rule):
        from .requirement_rules import NativeSourceRule
        from .silk_supply import SilkSupplyRule

        if isinstance(resolved_rule, SilkSupplyRule.Resolved):
            return
        if isinstance(resolved_rule, NativeSourceRule.Resolved):
            resolved_rule = resolved_rule.child
        super().register_rule_dependencies(resolved_rule)

    def collect_item(self, state: CollectionState, item: Item, remove: bool = False):
        if item.name == PROGRESSIVE_SWIFT_STEP_ITEM and 'Dash' in self.get_directional_abilities():
            from .directional_abilities import progressive_steps
            steps = progressive_steps(self._swift_step_first_right)
            if remove:
                return next((name for name in reversed(steps) if state.has(name, self.player)), None)
            return next((name for name in steps if not state.has(name, self.player)), None)
        return super().collect_item(state, item, remove)

    def collect(self, state: CollectionState, item: Item) -> bool:
        collected_name = self.collect_item(state, item)
        changed = World.collect(self, state, item)
        if changed and collected_name != item.name and hasattr(self, '_silk_supply'):
            self._silk_supply.collect(state, collected_name)
        results = state.rule_builder_cache[self.player]
        if changed and results:
            for name in (item.name, collected_name, self.item_mapping.get(item.name, "")):
                for rule_id in self.rule_item_dependencies.get(name, ()):
                    if results.get(rule_id) is False:
                        del results[rule_id]
        return changed

    def reached_region(self, state: CollectionState, region: Region) -> None:
        dependencies = self.rule_region_dependencies.get(region.name)
        if dependencies:
            results = state.rule_builder_cache[self.player]
            for rule_id in dependencies:
                results.pop(rule_id, None)

    def _enable_silk_supply(self, supply):
        self._silk_supply = supply
        self.collect = self._collect_with_silk_supply
        self.remove = self._remove_with_silk_supply
        self.reached_region = self._reached_region_with_silk_supply

    def _collect_with_silk_supply(self, state: CollectionState, item: Item) -> bool:
        changed = SilksongWorld.collect(self, state, item)
        if changed:
            self._silk_supply.collect(state, item.name)
        return changed

    def _remove_with_silk_supply(self, state: CollectionState, item: Item) -> bool:
        changed = super().remove(state, item)
        if changed and hasattr(state, '_silksong_silk_supply'):
            state._silksong_silk_supply.pop(self.player, None)
        return changed

    def _reached_region_with_silk_supply(self, state: CollectionState, region: Region) -> None:
        SilksongWorld.reached_region(self, state, region)
        self._silk_supply.reached(state, region)

    @staticmethod
    def _tracker_silk_and_soul_points(slot_data):
        from .options import SilkAndSoulPoints
        from worlds.tracker import TrackerException
        points = slot_data.get("silk_and_soul_points", SilkAndSoulPoints.default)
        if type(points) is not int or not SilkAndSoulPoints.range_start <= points <= SilkAndSoulPoints.range_end:
            raise TrackerException(message="Invalid Silk and Soul point total in slot data.")
        return points

    @staticmethod
    def _tracker_native_sources(slot_data):
        if "native_source_mask" not in slot_data:
            return None
        from worlds.tracker import TrackerException
        encoded = slot_data["native_source_mask"]
        offset = min(location_table.values())
        width = max(location_table.values()) - offset + 1
        if (not isinstance(encoded, str) or not encoded or len(encoded) > (width + 3) // 4
                or any(char not in "0123456789abcdef" for char in encoded)):
            raise TrackerException(message="Invalid fixed item sources in slot data.")
        mask = int(encoded, 16)
        sources = frozenset(name for name, code in location_table.items()
                            if mask & (1 << (code - offset)))
        if mask.bit_count() != len(sources):
            raise TrackerException(message="Unknown fixed item source in slot data.")
        return sources

    def _native_source_mask(self):
        offset = min(location_table.values())
        return format(sum(1 << (location_table[name] - offset)
                          for name in self._silksong_native_assumed_source_locations), "x")

    @staticmethod
    def interpret_slot_data(slot_data):
        from .map_logic_data import load_base
        from .entrance_randomization import validate_pairs

        from worlds.tracker import TrackerException

        if slot_data.get("logic_base") != load_base()[0]:
            raise TrackerException(message="Tracker map logic does not match this seed. Use the matching APWorld.")
        slot_data = dict(slot_data)
        if type(slot_data.get("swift_step_first_right")) is not bool:
            raise TrackerException(message="Tracker slot data is missing the Swift Step upgrade order.")
        slot_data.setdefault("start_inventory_from_pool", {})
        slot_data.setdefault("npc_souls", False)
        from .npc_souls import validate_slot_data as validate_npc_souls
        validate_npc_souls(slot_data)
        slot_data.setdefault("enemy_souls", False)
        from .enemy_souls import validate_slot_data as validate_enemy_souls
        validate_enemy_souls(slot_data)
        silk_logic = slot_data.setdefault('enemy_soul_silk_logic', 0)
        if type(silk_logic) is not int or silk_logic not in (0, 1) or (silk_logic and not slot_data['enemy_souls']):
            raise TrackerException(message='Invalid Enemy Souls silk logic version.')
        slot_data.setdefault("boss_souls", False)
        from .boss_souls import validate_slot_data
        validate_slot_data(slot_data)
        missing = set(TRACKER_OPTION_NAMES) - slot_data.keys()
        if missing:
            raise TrackerException(message=f"Tracker slot data is missing options: {', '.join(sorted(missing))}.")
        option_types = SilksongOptions.type_hints
        for name in TRACKER_OPTION_NAMES:
            if name in slot_data:
                option_types[name].from_any(deepcopy(slot_data[name]))
        from .progression_shuffle import Assignments, SUPPORTED_WISH_IDS, SUPPORTED_BOSS_IDS
        assignment_data = slot_data.get("progression_shuffle")
        if not isinstance(assignment_data, dict):
            raise TrackerException(message="Tracker slot data is missing progression assignments.")
        wish_ids = frozenset(assignment_data.get("wishes", {}))
        if not wish_ids.issubset(SUPPORTED_WISH_IDS):
            raise TrackerException(message="Unknown shuffled wish identity.")
        wish_shuffle = option_types["shuffle_wish_offers"].from_any(slot_data["shuffle_wish_offers"])
        boss_mode = option_types["boss_sanity"].from_any(slot_data["boss_sanity"])
        if bool(wish_ids) != bool(wish_shuffle):
            raise TrackerException(message="Shuffle Wish Offers setting does not match its assignments.")
        boss_ids = frozenset(assignment_data.get("bosses", {}))
        if not boss_ids.issubset(SUPPORTED_BOSS_IDS) or (boss_ids and boss_mode.value == boss_mode.option_vanilla):
            raise TrackerException(message="Boss Sanity setting does not match its assignments.")
        Assignments.from_slot_data(assignment_data, wish_ids, boss_ids)
        SilksongWorld._tracker_native_sources(slot_data)
        SilksongWorld._tracker_silk_and_soul_points(slot_data)
        goal = slot_data["goal"]
        if goal in {FLEA_HUNT_GOAL_KEY, SPELLING_BEE_GOAL_KEY}:
            count = (
                slot_data["flea_hunt_count"] if goal == FLEA_HUNT_GOAL_KEY
                else len(parse_spelling_bee_phrase(slot_data["spelling_bee_phrase"])[1])
            )
            act = 1 if count <= 10 else 2 if count <= 20 else 3
            valid_scopes = {f"act_{act}", f"act_{min(act + 1, 3)}"}
        else:
            valid_scopes = {ACT_TWO_GOAL_KEY if goal == CURSED_ENDING_GOAL_KEY else goal}
        if slot_data.get("content_scope") not in valid_scopes:
            raise TrackerException(message="Invalid content scope in slot data.")
        if slot_data["starting_crest"] not in STARTING_CREST_ITEM_BY_KEY:
            raise TrackerException(message="Invalid starting crest in slot data.")
        if (slot_data["starting_crest"] == "naked") != bool(option_types["force_naked"].from_any(slot_data["force_naked"])):
            raise TrackerException(message="Force Naked does not match the starting crest in slot data.")
        if slot_data["entrance_randomization"] == "coupled":
            validate_pairs(
                slot_data.get("entrance_pairs"), slot_data["entrance_randomization_scope"],
                slot_data["content_scope"],
            )
        count = slot_data.get("crest_slot_memory_locket_count")
        if type(count) is not int or not 0 <= count <= len(CREST_SLOT_LOCATION_NAMES):
            raise TrackerException(message="Invalid Crest Slot Locket requirement in slot data.")
        for name in ("purchase_prices", "trap_counts"):
            values = slot_data.get(name)
            if not isinstance(values, dict) or any(type(value) is not int or value < 0 for value in values.values()):
                raise TrackerException(message=f"Invalid {name} in slot data.")
        return slot_data

    def resolve_starting_crest(self) -> str:
        if self._resolved_starting_crest is not None:
            return self._resolved_starting_crest

        if self.options.force_naked and self.get_category_mode('Crest') == 'vanilla':
            raise OptionError("Naked start requires Crest Randomization set to anywhere.")
        configured_crest = (
            'naked' if self.options.force_naked else (
                'hunter' if self.get_category_mode('Crest') == 'vanilla'
                else self.options.starting_crest.current_key
            )
        )
        if configured_crest not in STARTING_CREST_ITEM_BY_KEY:
            raise OptionError(
                f"Unknown Silksong starting crest option: "
                f"{configured_crest!r}"
            )

        self._resolved_starting_crest = configured_crest
        return configured_crest

    def get_starting_location_key(self) -> str:
        from .requirements import SUPPORTED_STARTING_LOCATIONS
        key = self.options.starting_location.current_key
        if key not in SUPPORTED_STARTING_LOCATIONS:
            raise OptionError(
                f"Unknown Silksong starting location: {key!r}"
            )
        return key

    def get_goal_key(self) -> str:
        goal_key = self.options.goal.current_key
        if (
            goal_key == SPELLING_BEE_GOAL_KEY
            and self.get_spelling_bee_phrase_data() is None
        ):
            return ACT_TWO_GOAL_KEY
        return goal_key

    def get_spelling_bee_phrase_data(
        self,
    ) -> tuple[str, tuple[str, ...]] | None:
        return parse_spelling_bee_phrase(
            self.options.spelling_bee_phrase.value
        )

    def get_spelling_bee_phrase(self) -> str:
        if self.options.goal.current_key != SPELLING_BEE_GOAL_KEY:
            return ""
        phrase_data = self.get_spelling_bee_phrase_data()
        return "" if phrase_data is None else phrase_data[0]

    def get_spelling_bee_required_item_names(self) -> tuple[str, ...]:
        phrase_data = self.get_spelling_bee_phrase_data()
        return () if phrase_data is None else phrase_data[1]

    def get_content_scope(self) -> str:
        if self._resolved_content_scope is None:
            goal = self.get_goal_key()
            if goal in {FLEA_HUNT_GOAL_KEY, SPELLING_BEE_GOAL_KEY}:
                count = (
                    self.get_flea_hunt_goal_count()
                    if goal == FLEA_HUNT_GOAL_KEY
                    else len(self.get_spelling_bee_required_item_names())
                )
                act = 1 if count <= 10 else 2 if count <= 20 else 3
                if act < 3 and self.random.randrange(5) == 0:
                    act += 1
                self._resolved_content_scope = f"act_{act}"
            else:
                self._resolved_content_scope = (
                    ACT_TWO_GOAL_KEY if goal == CURSED_ENDING_GOAL_KEY else goal
                )
        return self._resolved_content_scope

    def is_act_two_content_scope(self) -> bool:
        return self.get_content_scope() == ACT_TWO_GOAL_KEY

    def is_act_one_content_scope(self) -> bool:
        return self.get_content_scope() == ACT_ONE_GOAL_KEY

    def get_start_with_map_item_names(self) -> tuple[str, ...]:
        if not self.is_start_with_maps_enabled():
            return ()
        if self.is_act_one_content_scope():
            return get_act_one_start_with_map_items(
                self.get_goal_excluded_location_names()
            )
        return (
            ACT_TWO_START_WITH_MAP_ITEMS
            if self.is_act_two_content_scope()
            else START_WITH_MAP_ITEMS
        )

    def get_act_two_excluded_location_names(self) -> frozenset[str]:
        if not self.is_act_two_content_scope():
            return frozenset()
        excluded = get_act_two_excluded_location_names(
            STARTING_CREST_ITEM_BY_KEY[self.resolve_starting_crest()],
            self.get_category_mode('Skill'),
            self.get_goal_key() == CURSED_ENDING_GOAL_KEY,
            bool(self.options.silk_soar_begone),
            (*enemy_soul_required_pool_items(self),
             *(('Crest: Shaman',) if self.get_category_mode('Crest') == 'anywhere' else ())),
        )
        if self.get_category_mode('Soul') == 'vanilla':
            return excluded | {'Maiden Soul', 'Hermit Soul', 'Seeker Soul'}
        return excluded

    def get_goal_excluded_location_names(self) -> frozenset[str]:
        from .boss_journal import excluded_locations
        excluded = self._get_base_goal_excluded_location_names()
        return excluded | excluded_locations(excluded, int(self.get_content_scope().removeprefix("act_")))

    def _get_base_goal_excluded_location_names(self) -> frozenset[str]:
        from .game_modes import excluded_locations
        mode_exclusions = excluded_locations(self.is_steel_soul(), self.is_act_one_content_scope())
        goal_key = self.get_content_scope()
        act_three_only_location_names = (
            ACT_THREE_ONLY_GOAL_LOCATION_NAMES
            if goal_key in {
                ACT_ONE_GOAL_KEY,
                ACT_TWO_GOAL_KEY,
                CURSED_ENDING_GOAL_KEY,
            }
            else frozenset()
        )
        if self.is_act_one_content_scope():
            return (
                get_act_one_excluded_location_names(
                    self.get_category_mode('MajorKey'),
                    self.get_category_mode('Boss'),
                    self.get_act_one_donation_tool_pouch_requirements(),
                    starting_crest_item=(
                        STARTING_CREST_ITEM_BY_KEY[
                            self.resolve_starting_crest()
                        ]
                    ),
                )

                | act_three_only_location_names
                | mode_exclusions
            )
        return (
            self.get_act_two_excluded_location_names()

            | act_three_only_location_names
            | mode_exclusions
        )

    def get_act_one_donation_tool_pouch_requirements(self) -> dict[str, int]:
        if not self.is_act_one_content_scope():
            return {}
        return get_shell_shard_donation_tool_pouch_requirements(
            self.get_purchase_prices()
        )

    def get_logic_unknown_locations(self) -> frozenset[str]:
        cached = getattr(self, "_resolved_logic_unknown_locations", None)
        if cached is not None:
            return cached
        if not MAPPER_GRAPH_ENABLED:
            return LOGIC_UNKNOWN_LOCATIONS
        if not hasattr(self, '_mapper_option_quarantines'):
            unavailable_items = set()
            if self.is_act_one_content_scope():
                excluded = self.get_goal_excluded_location_names()
                retained_items = set()
                for name, data in location_data_table.items():
                    if data.category not in PAIRED_LOCATION_CATEGORIES:
                        continue
                    reward = get_vanilla_reward_name(name, data.category)
                    (unavailable_items if name in excluded else retained_items).add(reward)
                unavailable_items.difference_update(retained_items)
                unavailable_items.discard(
                    STARTING_CREST_ITEM_BY_KEY[self.resolve_starting_crest()]
                )
                unavailable_items.difference_update(
                    name for inventory in (self.options.start_inventory, self.options.start_inventory_from_pool)
                    for name, count in inventory.value.items() if count > 0
                )
            if self.is_act_two_content_scope() and (
                    self.get_category_mode('Skill') != 'anywhere' or self.options.silk_soar_begone):
                unavailable_items.add('Silk Soar')
            self._mapper_option_quarantines = get_mapper_option_quarantines(
                unavailable_items=frozenset(unavailable_items),
                split_dash_and_sprint=self.is_split_dash_and_sprint(),
                allow_bellways_before_bell_beast=self.allows_bellways_before_bell_beast(),
                proficient_combat=self.get_proficient_combat_mode(),
                platforming_capability=self.get_platforming_capability(),
                directional_abilities=self.get_directional_abilities(),
                damage_boost_tier=int(self.options.damage_boost_logic.value),
                flea_brew_jump_logic=self.is_flea_brew_jump_logic_enabled(),
                sharpdart_logic=self.is_sharpdart_logic_enabled(),
                red_tool_stall_tier=int(self.options.red_tool_stall_logic.value),
                crest_pogo_tier=int(self.options.crest_pogo_logic.value),
                needle_strike_tier=int(self.options.needle_strike_logic.value),
                enemy_pogo_tier=int(self.options.enemy_pogo_logic.value),
                drill_crystal_pogo_tier=int(self.options.drill_crystal_pogo_logic.value),
                heal_stall_tier=int(self.options.heal_stall_logic.value),
                hazard_respawn_tier=int(self.options.hazard_respawn_logic.value),
                scuttlebrace_tier=int(self.options.scuttlebrace_logic.value),
                bell_shrine_sanity=self.get_category_mode("BellShrine") != "vanilla",
                steel_soul=self.is_steel_soul(),
                steel_soul_sites=self._steel_soul_sites,
                silk_and_soul_points=get_silk_and_soul_points(self.options),
                randomized_crest_slots_enabled=self.get_category_mode('CrestSlot') != 'vanilla',
                starting_location=self.get_starting_location_key(),
                trails_end_requirement=self.get_trails_end_requirement_key(),
                scuttlebrace_logic_enabled=self.is_scuttlebrace_logic_enabled(),
                randomize_ledge_grab=self.is_ledgegrab_ability_rando_enabled(),
                randomize_swim=self.is_swim_ability_rando_enabled(),
                pollip_heart_count=POLLIP_HEART_COUNT if self.get_category_mode('PollipHeart') != 'vanilla' else 0,
            )
        unknown = LOGIC_UNKNOWN_LOCATIONS | self._mapper_option_quarantines
        if self.is_act_one_content_scope() or self.is_act_two_content_scope():
            unknown |= BUGS_OF_PHARLOOM_REWARD_LOCATIONS
        from .boss_journal import unknown_locations
        self._resolved_logic_unknown_locations = unknown | unknown_locations(
            unknown, self.get_goal_excluded_location_names(), int(self.get_content_scope().removeprefix("act_")))
        return self._resolved_logic_unknown_locations

    def generate_early(self) -> None:
        from .requirement_rules import build_requirements_rule

        build_requirements_rule.cache_clear()
        self._resolved_logic_unknown_locations = None
        self._crest_slot_memory_locket_count = None
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game)
        self._swift_step_first_right = (
            bool(passthrough['swift_step_first_right']) if passthrough is not None
            else bool(self.random.getrandbits(1)) if self.is_split_dash_and_sprint() and self.options.directional_swift_step
            else False
        )
        if passthrough is not None:
            passthrough = dict(passthrough)
            passthrough.setdefault("start_inventory_from_pool", {})
            option_types = SilksongOptions.type_hints
            for name in TRACKER_OPTION_NAMES:
                setattr(self.options, name, option_types[name].from_any(deepcopy(passthrough[name])))
            self._resolved_content_scope = passthrough["content_scope"]
            self._resolved_starting_crest = passthrough["starting_crest"]
            self.options.starting_crest = option_types["starting_crest"].from_any(
                "hunter" if self.options.force_naked else self._resolved_starting_crest
            )
            self._resolved_purchase_prices = dict(passthrough["purchase_prices"])
            self._resolved_trap_counts = dict(passthrough["trap_counts"])
            self._crest_slot_memory_locket_count = passthrough["crest_slot_memory_locket_count"]
        if self.options.directional_ledge_grab:
            self.options.ledgegrab_ability_rando.value = 1
        if self.get_goal_key() == "act_3":
            self.options.silk_and_soul_points.value = get_silk_and_soul_points(self.options)
        from .game_modes import choose_resting_sites, validate_resting_sites
        self._steel_soul_sites = validate_resting_sites(
            passthrough.get("steel_soul_sites", []) if passthrough is not None
            else choose_resting_sites(self.random) if self.is_steel_soul() else (),
            self.is_steel_soul(),
        )
        if (self.is_ledgegrab_ability_rando_enabled()
                and self.options.starting_location.current_key == 'vanilla'):
            self.options.starting_location.value = self.options.starting_location.option_bone_bottom
        if self.get_starting_location_key() == 'songclave' and self.is_act_one_content_scope():
            raise OptionError("Songclave start requires an Act 2 or later goal.")
        self._vog_hint_plan = None
        if self.is_alphabet_mode_enabled():
            self.options.alphabet_mode.value = 1
        if self.options.silk_soar_begone and any(
            inventory.value.get("Silk Soar", 0) > 0
            for inventory in (self.options.start_inventory, self.options.start_inventory_from_pool)
        ):
            raise OptionError("Silk Soar Begone cannot be combined with starting Silk Soar.")
        starting_crest = self.resolve_starting_crest()
        category_modes = self.get_category_modes()
        goal_key = self.get_goal_key()
        opening_pool = build_item_pool_entries(
            STARTING_CREST_ITEM_BY_KEY[starting_crest],
            self.resolve_trap_counts(),
            self.is_split_dash_and_sprint(),
            category_modes,
            self.is_start_with_maps_enabled(),
            self.is_automatic_compass_enabled(),
            individual_relic_turn_ins=(
                self.is_individual_relic_turn_ins_enabled()
            ),
            act_two_only=self.is_act_two_content_scope(),
            start_fully_mapped=self.is_start_fully_mapped_enabled(),
            act_one_only=self.is_act_one_content_scope(),

            retain_green_prince_key=(goal_key == ACT_TWO_GOAL_KEY),
            alphabet_mode=self.is_alphabet_mode_enabled(),
            act_one_donation_tool_pouch_requirements=(
                self.get_act_one_donation_tool_pouch_requirements()
            ),
            randomize_ledge_grab=(
                self.is_ledgegrab_ability_rando_enabled()
            ),
            randomize_swim=self.is_swim_ability_rando_enabled(),
            directional_abilities=self.get_directional_abilities(),
            randomize_diving_bell_key=bool(self.options.diving_bell_key_randomization.value),
            cursed_ending=(self.get_goal_key() == CURSED_ENDING_GOAL_KEY),
            steel_soul=self.is_steel_soul(),
            required_goal_items=enemy_soul_required_pool_items(self),
            silk_soar_begone=bool(self.options.silk_soar_begone),
            soul_pool_entries=self._soul_pool_entries(),
        )
        if self.is_early_sprint_enabled():
            player_early_items = self.multiworld.local_early_items[
                self.player
            ]
            early_item_name = (
                PROGRESSIVE_SWIFT_STEP_ITEM
                if self.is_split_dash_and_sprint()
                else "Swift Step"
            )
            if self.options.directional_swift_step and not self.is_split_dash_and_sprint():
                early_item_name = 'Swift Step (Left)'
                right = early_item_name.replace('(Left)', '(Right)')
                player_early_items[right] = player_early_items.get(right, 0) + 1
            player_early_items[early_item_name] = (
                player_early_items.get(early_item_name, 0)
                + 1
            )

        self.options.non_local_items.value.difference_update(
            entry.name for entry in opening_pool if entry.placement_category is not None
        )

    def get_directional_abilities(self):
        from .directional_abilities import selected
        return selected(self.options, self.get_category_mode('Skill') == 'anywhere')

    def is_steel_soul(self) -> bool:
        return self.options.game_mode.current_key == "steel_soul"

    def is_split_dash_and_sprint(self) -> bool:
        return (
            bool(self.options.split_dash_and_sprint.value)
            and self.get_category_mode('Skill') == 'anywhere'
        )

    def is_early_sprint_enabled(self) -> bool:
        return (
            bool(self.options.early_sprint.value)
            and self.get_category_mode('Skill') == 'anywhere'
        )

    def is_ledgegrab_ability_rando_enabled(self) -> bool:
        return bool(self.options.ledgegrab_ability_rando.value)

    def is_swim_ability_rando_enabled(self) -> bool:
        return bool(self.options.swim_ability_rando.value)

    def is_vanilla_flea_hunt_check(self, location_name: str) -> bool:
        return (
            self.get_goal_key() == FLEA_HUNT_GOAL_KEY
            and self.get_category_mode('Flea') == 'vanilla'
            and location_name in LOCATION_NAMES_BY_CATEGORY['Flea']
        )

    def is_individual_relic_turn_ins_enabled(self) -> bool:
        return bool(self.options.individual_relic_turn_ins.value)

    def get_proficient_combat_mode(self) -> int:
        return self.options.proficient_combat.value

    def get_platforming_capability(self) -> int:
        return int(self.options.platforming_capability.value)

    def is_flea_brew_jump_logic_enabled(self) -> bool:
        return bool(getattr(getattr(self.options, "flea_brew_jump_logic", None), "value", 0))

    def is_sharpdart_logic_enabled(self) -> bool:
        return bool(self.options.sharpdart_logic.value)

    def is_scuttlebrace_logic_enabled(self) -> bool:
        return bool(self.options.scuttlebrace_logic.value)

    def get_flea_hunt_goal_count(self) -> int:
        count = int(self.options.flea_hunt_count.value)
        if not (
            MIN_FLEA_HUNT_GOAL_COUNT
            <= count
            <= MAX_FLEA_HUNT_GOAL_COUNT
        ):
            raise OptionError(
                "flea_hunt_count must be between "
                f"{MIN_FLEA_HUNT_GOAL_COUNT} and "
                f"{MAX_FLEA_HUNT_GOAL_COUNT} but received {count!r}."
            )
        return count

    def is_needle_upgrade_randomization_enabled(self) -> bool:
        return self.get_category_mode(NEEDLE_UPGRADE_LOCATION_CATEGORY) != 'vanilla'

    def is_pale_oil_randomization_enabled(self) -> bool:
        return self.get_category_mode(PALE_OIL_LOCATION_CATEGORY) != 'vanilla'

    def is_alphabet_mode_enabled(self) -> bool:
        return bool(self.options.alphabet_mode.value) or (
            self.get_goal_key() == SPELLING_BEE_GOAL_KEY
        )

    def is_start_with_maps_enabled(self) -> bool:
        return bool(self.options.start_with_maps.value)

    def is_start_fully_mapped_enabled(self) -> bool:
        return bool(self.options.start_fully_mapped.value)

    def is_automatic_compass_enabled(self) -> bool:
        return bool(self.options.automatic_compass.value)

    def get_bellway_access_key(self) -> str:
        key = self.options.bellway_access.current_key
        if key not in {
            "bell_beast_required",
            "randomized_stations",
        }:
            raise OptionError(
                f"Unknown Bellway access mode: {key!r}"
            )
        return key

    def allows_bellways_before_bell_beast(self) -> bool:
        return self.get_bellway_access_key() == "randomized_stations"

    def get_trails_end_requirement_key(self) -> str:
        return normalize_trails_end_requirement(
            self.options.trails_end_requirement.current_key
        )

    def get_location_map_markers_key(self) -> str:
        key = self.options.location_map_markers.current_key
        if key not in {"off", "mapped_rooms", "owned_maps", "all"}:
            raise OptionError(
                f"Unknown location map marker mode: {key!r}"
            )
        return key

    def uses_randomized_bell_markers(self) -> bool:
        return bool(self.options.randomized_bell_markers.value)

    def uses_randomized_melody_markers(self) -> bool:
        return bool(self.options.randomized_melody_markers.value)

    def get_randomized_item_marker_locations(self) -> dict[str, str]:
        item_names = set()
        if self.uses_randomized_bell_markers():
            item_names.update(JUDGE_BELL_ITEMS)
        if self.uses_randomized_melody_markers():
            item_names.update(THREEFOLD_MELODY_ITEMS)
        if not item_names:
            return {}

        return {
            location.item.name: location.name
            for location in sorted(
                self.multiworld.get_filled_locations(),
                key=lambda candidate: (candidate.player, candidate.name),
            )
            if (
                location.player == self.player
                and location.address is not None
                and location.item is not None
                and location.item.player == self.player
                and location.item.name in item_names
            )
        }

    def get_enemy_rosary_multiplier_key(self) -> str:
        key = self.options.enemy_rosary_multiplier.current_key
        if key not in {"x1", "x1_5", "x2", "x3", "x5", "x10"}:
            raise OptionError(
                f"Unknown enemy Rosary multiplier: {key!r}"
            )
        return key

    def get_enemy_shard_multiplier_key(self) -> str:
        key = self.options.enemy_shard_multiplier.current_key
        if key not in {"x1", "x1_5", "x2", "x3", "x5", "x10"}:
            raise OptionError(
                f"Unknown enemy Shell Shard multiplier: {key!r}"
            )
        return key

    def get_purchase_price_modes(self) -> dict[str, str]:
        modes: dict[str, str] = {}
        for category, option_name in PRICE_CATEGORY_OPTION_NAMES.items():
            key = getattr(self.options, option_name).current_key
            if key not in PRICE_MODE_KEYS:
                raise OptionError(
                    f"Unknown {option_name} mode: {key!r}"
                )
            modes[category] = key
        return modes

    def get_purchase_prices(self) -> dict[str, int]:
        cached = getattr(self, "_resolved_purchase_prices", None)
        if cached is None:
            pouch_count = sum(
                data.category == 'ToolPouch' and (
                    self.get_category_mode('ToolPouch') != 'vanilla'
                    or name not in LOGIC_UNKNOWN_LOCATIONS
                )
                for name, data in location_data_table.items()
            )
            cached = resolve_purchase_prices(
                getattr(self, "random", None) or random.Random(0),
                self.get_purchase_price_modes(),
                tool_pouch_count=pouch_count,
            )
            self._resolved_purchase_prices = cached
        return dict(cached)

    def is_faster_dialogue_enabled(self) -> bool:
        return bool(self.options.faster_dialogue.value)

    def is_death_link_enabled(self) -> bool:
        return bool(self.options.death_link.value)

    def get_death_link_cocoon_key(self) -> str:
        key = self.options.death_link_cocoon.current_key
        if key not in {"vanilla", "cocoonless", "cocoon"}:
            raise OptionError(
                f"Unknown Death Link cocoon mode: {key!r}"
            )
        return key

    def is_silk_link_enabled(self) -> bool:
        return bool(self.options.silk_link.value)

    def is_rosary_link_enabled(self) -> bool:
        return bool(self.options.rosary_link.value)

    def is_shell_shard_link_enabled(self) -> bool:
        return bool(self.options.shell_shard_link.value)

    def get_vog_area_hint_count(self) -> int:
        return self.options.vog_area_hints.value

    def get_vog_hint_plan(self) -> dict[str, object]:
        plan = getattr(self, "_vog_hint_plan", None)
        if plan is None:
            plan = self.build_vog_hint_plan()
        return copy_vog_hint_plan(plan)

    def build_vog_hint_plan(self) -> dict[str, object]:
        self._vog_hint_plan = build_vog_hint_plan(self)
        return copy_vog_hint_plan(self._vog_hint_plan)

    def is_wish_sanity_enabled(self) -> bool:
        return self.get_category_mode('Quest') != 'vanilla'

    def get_category_mode(self, category: str) -> str:
        return get_category_mode_key(self.options, category)

    def get_minor_family_modes(self) -> dict[str, str]:
        return get_minor_family_modes(self.options)

    def get_location_randomization_mode(
        self,
        location_name: str,
        category: str,
    ) -> str:
        if category != "Resource":
            return self.get_category_mode(category)
        try:
            family_key = MINOR_FAMILY_BY_LOCATION[location_name]
        except KeyError as exc:
            raise OptionError(
                f"No minor pickup family for {location_name!r}."
            ) from exc
        return self.get_minor_family_modes()[family_key]



    def get_category_modes(self) -> dict[str, str]:
        modes = {
            category: self.get_category_mode(category)
            for category in CATEGORY_OPTION_BY_LOCATION_CATEGORY
        }
        modes["Resource"] = get_aggregate_minor_mode_key(self.options)
        modes.update(
            {
                get_minor_family_category(family_key): mode
                for family_key, mode in
                self.get_minor_family_modes().items()
            }
        )
        return modes

    def _minimum_pool_lockets(self) -> int:
        if not uses_crest_slot_locket_logic(self):
            return 0
        excluded = self.get_goal_excluded_location_names()
        active_count = len(set(CREST_SLOT_LOCATION_NAMES) - excluded)
        native_count = 0
        if self.get_category_mode('MemoryLocket') == 'vanilla':
            native_count = len(
                set(LOCATION_NAMES_BY_CATEGORY['MemoryLocket'])
                - excluded - self.get_logic_unknown_locations()
            )
        starting_count = max(
            self.options.start_inventory.value.get(MEMORY_LOCKET_ITEM, 0),
            sum(item.name == MEMORY_LOCKET_ITEM
                for item in self.multiworld.precollected_items[self.player])
            - self.options.start_inventory_from_pool.value.get(MEMORY_LOCKET_ITEM, 0),
        )
        return max(0, active_count - native_count - starting_count)

    def _soul_pool_entries(self):
        from .boss_souls import pool_entries as boss_entries
        from .npc_souls import pool_entries as npc_entries
        return (*boss_entries(self), *npc_entries(self))

    def resolve_trap_counts(self) -> dict[str, int]:
        if self._resolved_trap_counts is not None:
            return dict(self._resolved_trap_counts)

        percentage = int(self.options.trap_percentage.value)
        trap_capacity = get_dynamic_trap_capacity(
            self.get_category_modes(),
            self.is_split_dash_and_sprint(),
            STARTING_CREST_ITEM_BY_KEY[self.resolve_starting_crest()],
            self.is_start_with_maps_enabled(),
            self.is_automatic_compass_enabled(),
            self.is_individual_relic_turn_ins_enabled(),
            self.is_act_two_content_scope(),
            self.is_start_fully_mapped_enabled(),
            act_one_only=self.is_act_one_content_scope(),

            retain_green_prince_key=(
                self.get_goal_key() == ACT_TWO_GOAL_KEY
            ),
            alphabet_mode=self.is_alphabet_mode_enabled(),
            act_one_donation_tool_pouch_requirements=(
                self.get_act_one_donation_tool_pouch_requirements()
            ),
            randomize_ledge_grab=(
                self.is_ledgegrab_ability_rando_enabled()
            ),
            randomize_swim=self.is_swim_ability_rando_enabled(),
            directional_abilities=self.get_directional_abilities(),
            randomize_diving_bell_key=bool(self.options.diving_bell_key_randomization.value),
            cursed_ending=(self.get_goal_key() == CURSED_ENDING_GOAL_KEY),
            steel_soul=self.is_steel_soul(),
            silk_soar_begone=bool(self.options.silk_soar_begone),
            minimum_memory_lockets=self._minimum_pool_lockets(),
            required_goal_items=enemy_soul_required_pool_items(self),
            soul_pool_entries=self._soul_pool_entries(),
        )
        total_traps = (trap_capacity * percentage + 50) // 100
        weights = {
            item_name: int(getattr(self.options, option_name).value)
            for option_name, item_name
            in TRAP_ITEM_NAME_BY_WEIGHT_OPTION.items()
        }
        total_weight = sum(weights.values())
        counts = {item_name: 0 for item_name in TRAP_ITEM_NAMES}
        if total_traps > 0 and total_weight > 0:
            remainders: dict[int, list[str]] = {}
            assigned = 0
            for item_name, weight in weights.items():
                count, remainder = divmod(
                    total_traps * weight,
                    total_weight,
                )
                counts[item_name] = count
                assigned += count
                if weight > 0:
                    remainders.setdefault(remainder, []).append(item_name)

            remaining = total_traps - assigned
            for remainder in sorted(remainders, reverse=True):
                tied_names = remainders[remainder]
                if len(tied_names) > 1:
                    self.random.shuffle(tied_names)
                for item_name in tied_names:
                    if remaining == 0:
                        break
                    counts[item_name] += 1
                    remaining -= 1
                if remaining == 0:
                    break

        self._resolved_trap_counts = counts
        return dict(counts)

    def create_item(
        self,
        name: str,
        placement_category: str | None = None,
    ) -> Item:
        data = item_data_table[name]
        classification = data.classification
        if data.category == 'MaskShard' and self.options.proficient_combat.value == 2:
            classification = ItemClassification.useful
        if name == 'Sylphsong':
            from .silk_economy import enabled as silk_enabled
            if silk_enabled(self):
                classification = ItemClassification.progression
        if (
            name in ALPHABET_ITEM_NAMES
            and getattr(self, "options", None) is not None
            and (
                self.get_goal_key() != SPELLING_BEE_GOAL_KEY
                or name not in self.get_spelling_bee_required_item_names()
            )
        ):
            classification = ItemClassification.useful
        if (
            name == SIMPLE_KEY_ROSARY_BANK
            and not self.is_rosary_bank_key_progression_enabled()
        ):
            classification = ItemClassification.useful
        if (
            name == 'Scuttlebrace'
            and not self.is_scuttlebrace_logic_enabled()
        ):
            classification = ItemClassification.useful
        if (
            name == SIMPLE_KEY_GREEN_PRINCE
            and self.get_content_scope() != "act_3"
        ):
            classification = ItemClassification.useful
        if name in OPTION_DEPENDENT_CREST_SLOT_ITEM_NAMES:
            crest_slot_mode = self.get_category_mode('CrestSlot')
            if crest_slot_mode == 'vanilla':
                classification = ItemClassification.useful
        if (
            self.get_category_mode('CrestSlot') != 'vanilla'
            and any(slot == name for _, _, slot in EVA_POINT_SOURCES)
        ):
            classification = ItemClassification.progression
        if (
            name in SCROUNGE_RELIC_ITEM_NAMES
            or (
                name in INDIVIDUAL_RELIC_TURN_IN_ITEM_NAMES
                and self.is_individual_relic_turn_ins_enabled()
            )
        ):
            classification = ItemClassification.progression
        if (
            name == MEMORY_LOCKET_ITEM
            and uses_crest_slot_locket_logic(self)
        ):
            # These consumable logic keys must stay where restrictive fill
            # proved them reachable. Core progression balancing otherwise
            # has permission to move progression after the shared Crest Slot
            # requirement has been frozen.
            classification |= ItemClassification.skip_balancing
        return SilksongItem(
            name,
            classification,
            data.code,
            self.player,
            placement_category,
        )

    def create_filler(self) -> Item:
        lanes = getattr(self, "_start_inventory_pool_filler_lanes", None)
        return self.create_item(self.get_filler_item_name(), lanes.popleft() if lanes else None)

    def _prepare_start_inventory_pool(self) -> None:
        remaining = Counter(self.options.start_inventory_from_pool.value)
        lanes = deque()
        for item in self.multiworld.itempool:
            if item.player == self.player and remaining[item.name] > 0:
                remaining[item.name] -= 1
                lanes.append(getattr(item, "silksong_placement_category", None))
        missing = {name: count for name, count in remaining.items() if count > 0}
        if missing:
            raise OptionError(
                f"Start Inventory from Pool requests unavailable copies: {missing}. "
                "Choose items in the randomized pool; vanilla, out-of-scope and already-starting items cannot be removed."
            )
        self._start_inventory_pool_filler_lanes = lanes

    def get_filler_item_name(self) -> str:
        return OPTIONAL_START_REPLACEMENT_ITEM

    def is_rosary_bank_key_progression_enabled(self) -> bool:
        return True

    def create_event(self, name: str) -> Item:
        return SilksongItem(
            name,
            ItemClassification.progression,
            None,
            self.player,
        )

    def create_items(self) -> None:
        starting_crest = self.resolve_starting_crest()
        starting_crest_item = STARTING_CREST_ITEM_BY_KEY[starting_crest]
        category_modes = self.get_category_modes()
        precollected_option_items = {
            *self.get_start_with_map_item_names(),
        }
        option_replaced_item_names = {
            *precollected_option_items,
            *((QUILL_ITEM,) if self.is_start_fully_mapped_enabled() else ()),
            *(
                (AUTOMATIC_COMPASS_ITEM,)
                if self.is_automatic_compass_enabled()
                else ()
            ),
        }

        def place_fixed_reward(
            location_name: str,
            reward_name: str,
        ) -> None:
            effective_reward_name = (
                OPTIONAL_START_REPLACEMENT_ITEM
                if reward_name in option_replaced_item_names
                else reward_name
            )
            effective_reward = self.create_item(effective_reward_name)
            location = self.multiworld.get_location(location_name, self.player)
            location.place_locked_item(effective_reward)

        if (self.options.silk_soar_begone and self.get_content_scope() == "act_3"
                and category_modes['Skill'] != 'vanilla'):
            place_fixed_reward('Silk Soar', 'Silk Soar')

        if category_modes['Crest'] != 'vanilla' and starting_crest_item is not None:
            place_fixed_reward('Crest: Hunter', starting_crest_item)

        for category in PAIRED_LOCATION_CATEGORIES:
            for location_name in LOCATION_NAMES_BY_CATEGORY[category]:
                if (
                    location_name
                    in self.get_goal_excluded_location_names()
                ):
                    continue
                mode = self.get_location_randomization_mode(
                    location_name,
                    category,
                )
                if mode == 'vanilla' and location_name not in self.get_logic_unknown_locations():
                    reward_name = get_vanilla_reward_name(
                        location_name,
                        category,
                    )
                    place_fixed_reward(
                        location_name,
                        reward_name,
                    )
        for item_name in sorted(precollected_option_items):
            self.multiworld.push_precollected(self.create_item(item_name))

        get_locations = getattr(self.multiworld, 'get_locations', None)
        addressed_unfilled_locations = (
            [
                location
                for location in get_locations()
                if (
                    location.player == self.player
                    and location.address is not None
                    and location.item is None
                )
            ]
            if callable(get_locations)
            else []
        )
        nonadvancement_demand_by_lane = Counter(
            getattr(
                location,
                'silksong_placement_category',
                None,
            )
            for location in addressed_unfilled_locations
            if (
                location.name
                in (self.get_logic_unknown_locations() | JUNK_ONLY_LOCATIONS)
            )
        )

        pool_entries = list(build_item_pool_entries(
            starting_crest_item,
            self.resolve_trap_counts(),
            self.is_split_dash_and_sprint(),
            category_modes,
            self.is_start_with_maps_enabled(),
            self.is_automatic_compass_enabled(),
            getattr(self, 'random', None),
            self.is_individual_relic_turn_ins_enabled(),
            self.is_act_two_content_scope(),
            self.is_start_fully_mapped_enabled(),
            act_one_only=self.is_act_one_content_scope(),

            retain_green_prince_key=(
                self.get_goal_key() == ACT_TWO_GOAL_KEY
            ),
            alphabet_mode=self.is_alphabet_mode_enabled(),
            act_one_donation_tool_pouch_requirements=(
                self.get_act_one_donation_tool_pouch_requirements()
            ),
            randomize_ledge_grab=(
                self.is_ledgegrab_ability_rando_enabled()
            ),
            randomize_swim=self.is_swim_ability_rando_enabled(),
            directional_abilities=self.get_directional_abilities(),
            randomize_diving_bell_key=bool(self.options.diving_bell_key_randomization.value),
            cursed_ending=(self.get_goal_key() == CURSED_ENDING_GOAL_KEY),
            steel_soul=self.is_steel_soul(),
            silk_soar_begone=bool(self.options.silk_soar_begone),
            alphabet_nonadvancement_demand_by_placement_category=(
                nonadvancement_demand_by_lane
            ),
            alphabet_item_is_advancement=(
                lambda item_name: self.create_item(item_name).advancement
            ),
            minimum_memory_lockets=self._minimum_pool_lockets(),
            required_goal_items=enemy_soul_required_pool_items(self),
            soul_pool_entries=self._soul_pool_entries(),
        ))

        from .enemy_souls import add_souls_to_pool as add_enemy_souls
        add_enemy_souls(self, pool_entries)

        location_lane_counts = Counter(
            getattr(
                location,
                'silksong_placement_category',
                None,
            )
            for location in addressed_unfilled_locations
        )
        original_pool_size = len(pool_entries)
        original_pool_lane_counts = Counter(
            entry.placement_category
            for entry in pool_entries
        )
        if (
            callable(get_locations)
            and location_lane_counts != original_pool_lane_counts
        ):
            raise AssertionError(
                "Silksong location and item placement lanes are unbalanced: "
                f"{location_lane_counts!r} != {original_pool_lane_counts!r}."
            )

        for placement_category, nonadvancement_demand in (
            nonadvancement_demand_by_lane.items()
        ):
            matching_indices = [
                index
                for index, entry in enumerate(pool_entries)
                if entry.placement_category == placement_category
            ]
            nonadvancement_count = sum(
                not self.create_item(pool_entries[index].name).advancement
                for index in matching_indices
            )
            shortage = nonadvancement_demand - nonadvancement_count
            if shortage <= 0:
                continue

            raise OptionError(
                f"{placement_category or 'Anywhere'} needs {shortage} more "
                "non-progression items for checks with incomplete logic. "
                "Use more anywhere categories or disable the affected checks."
            )

        if len(pool_entries) != original_pool_size:
            raise AssertionError(
                "Non-advancement placement safety changed the item-pool "
                "size."
            )
        if Counter(
            entry.placement_category
            for entry in pool_entries
        ) != original_pool_lane_counts:
            raise AssertionError(
                "Non-advancement placement safety changed placement lanes."
            )
        for placement_category, nonadvancement_demand in (
            nonadvancement_demand_by_lane.items()
        ):
            nonadvancement_count = sum(
                not self.create_item(entry.name).advancement
                for entry in pool_entries
                if entry.placement_category == placement_category
            )
            if nonadvancement_count < nonadvancement_demand:
                raise AssertionError(
                    "Non-advancement placement safety left too few "
                    f"non-advancement items in lane {placement_category!r}."
                )

        pool_entries = tuple(pool_entries)
        if (self.is_act_two_content_scope() and not self.options.silk_soar_begone
                and (any(entry.name == "Grey Memento" for entry in pool_entries)
                     or (self.get_category_mode('Skill') == 'anywhere'
                         and self.options.accessibility == 'full'))
                and not any(entry.name == "Silk Soar" for entry in pool_entries)
                and not any(item.name == "Silk Soar"
                            for item in self.multiworld.precollected_items[self.player])):
            raise OptionError(
                "The selected Act 2 settings need room for Silk Soar. "
                "Enable a category with filler items in Anywhere mode or start with Silk Soar."
            )

        self.multiworld.itempool.extend(
            self.create_item(entry.name, entry.placement_category)
            for entry in pool_entries
        )

    def _finalize_progression_shuffle(self) -> None:
        from .progression_shuffle import finalize_world
        finalize_world(self)
        self._configure_tracker_map()
        state = self.multiworld.get_all_state()
        if self.get_goal_key() == "act_3":
            available = (
                state.count(SILK_AND_SOUL_WISH_POINT_ITEM, self.player)
                + state.count(SILK_AND_SOUL_WISH_HALF_POINT_ITEM, self.player) // 2
            )
            required = get_silk_and_soul_points(self.options)
            if available < required:
                raise OptionError(
                    f"Silk and Soul requires {required} points, but verified wish logic "
                    f"supports only {available} with these settings. "
                    "Unresolved wishes cannot contribute progression points."
                )
        for name in tuple(self._silksong_active_wish_logic_events):
            location = self.multiworld.get_location(name, self.player)
            if not location.can_reach(state):
                location.parent_region.locations.remove(location)
                del self._silksong_active_wish_logic_events[name]
                self._silksong_wish_logic_event_anchors.pop(name, None)

    @property
    def found_entrances_datastorage_key(self):
        keys = ["Silksong:Warps:{team}:{player}"]
        if self.options.entrance_randomization:
            keys.append("Silksong:Entrances:{team}:{player}")
        return keys

    def reconnect_found_entrances(self, found_key, data_storage_value):
        from .entrance_randomization import reconnect_found, reconnect_warps
        if found_key.startswith("Silksong:Warps:"):
            reconnect_warps(self, data_storage_value)
        elif found_key.startswith("Silksong:Entrances:"):
            reconnect_found(self, data_storage_value)

    def get_pre_fill_items(self):
        return [*super().get_pre_fill_items(), *getattr(self, "_entrance_construction_items", ())]

    def connect_entrances(self) -> None:
        from .boss_souls import prepare_start
        prepare_start(self)
        from .entrance_randomization import connect_exits
        connect_exits(self)
        if getattr(self, '_silk_supply', None) is not None:
            self.explicit_indirect_conditions = False

    def explain_path(self, entrance, state):
        from rule_builder.rules import Or
        label = getattr(entrance, "display_name", None)
        if isinstance(entrance.access_rule, Or.Resolved):
            j_return: list = [{"type":"color","color":"blue","text": (label if label is not None else entrance.name)}]
            for child in entrance.access_rule.children:
                j_return.append({"type":"text","text":"\n"})
                if child(state):
                    j_return.append({"type":"color","text":"TRUE","color":"green"})
                else:
                    j_return.append({"type":"color","text":"FALSE","color":"red"})
                j_return.append({"type":"text","text":": "})
                j_return.extend(child.explain_json(state))
            return j_return
        elif label is None:
            return [] # Default behaviour
        result = [{'type': 'color', 'color': 'blue', 'text': label}]
        if hasattr(entrance.access_rule, 'explain_json'):
            result.append({'type': 'text', 'text': ':\n    '})
            result.extend(entrance.access_rule.explain_json(state))
        return result
    
    def explain_spot(self, location, state):
        from rule_builder.rules import Or
        label = getattr(location, "display_name", None)
        if isinstance(location.access_rule, Or.Resolved):
            j_return: list = [{"type":"color","color":"green","text": (label if label is not None else location.name)}]
            for child in location.access_rule.children:
                j_return.append({"type":"text","text":"\n"})
                if child(state):
                    j_return.append({"type":"color","text":"TRUE","color":"green"})
                else:
                    j_return.append({"type":"color","text":"FALSE","color":"red"})
                j_return.append({"type":"text","text":": "})
                j_return.extend(child.explain_json(state))
            return j_return
        elif label is None:
            return [] # Default behaviour
        result = [{'type': 'color', 'color': 'green', 'text': label}]
        if hasattr(location.access_rule, 'explain_json'):
            result.append({'type': 'text', 'text': ':\n    '})
            result.extend(location.access_rule.explain_json(state))
        return result

    def create_regions(self) -> None:
        from .progression_shuffle import world_location_requirements
        self._active_crest_slot_locations = None
        self._entrance_construction_items = ()
        menu = Region("Menu", self.player, self.multiworld)
        pharloom = Region("Pharloom", self.player, self.multiworld)
        logic_unknown = Region(
            LOGIC_UNKNOWN_REGION_NAME,
            self.player,
            self.multiworld,
        )
        self.multiworld.regions += [menu, pharloom, logic_unknown]
        from .enemy_souls import create_locations as create_enemy_locations
        create_enemy_locations(self, pharloom)
        if not self.options.diving_bell_key_randomization.value:
            vanilla_key = SilksongLocation(self.player, "Vanilla Diving Bell Key", None, menu)
            vanilla_key.show_in_spoiler = False
            vanilla_key.place_locked_item(self.create_event("Diving Bell Key"))
            menu.locations.append(vanilla_key)

        native_regions = create_native_logic_region_map(self)
        abstract_names = self._silksong_native_region_names
        self._silksong_native_location_anchors = {}
        self._silksong_native_assumed_source_locations = set()
        passthrough = getattr(self.multiworld, "re_gen_passthrough", {}).get(self.game)
        restored_sources = self._tracker_native_sources(passthrough) if passthrough else None
        menu.connect(pharloom)
        self.create_entrance(
            pharloom,
            logic_unknown,
            Has("Victory"),
            "Silksong Logic: LogicUnknown",
        )
        connect_native_logic_regions(self, menu, native_regions)
        from .scene_exits import create_exits
        create_exits(self, native_regions)
        randomize_needle_upgrades = (
            self.is_needle_upgrade_randomization_enabled()
        )
        pollip_heart_count = (
            POLLIP_HEART_COUNT
            if self.get_category_mode("PollipHeart") != "vanilla"
            else 0
        )
        logic_item_references = get_logic_item_references()

        source_rule_dependencies = {}
        for name, data in location_data_table.items():
            if (
                name in self.get_goal_excluded_location_names()
            ):
                continue
            if (
                data.category == RELIC_TURN_IN_LOCATION_CATEGORY
                and not self.is_individual_relic_turn_ins_enabled()
            ):
                continue
            if name in WISH_REWARD_LOCATION_BY_COMPLETION:
                continue
            mode = (
                self.get_location_randomization_mode(
                    name,
                    data.category,
                )
                if (
                    data.category == "Resource"
                    or data.category in CATEGORY_OPTION_BY_LOCATION_CATEGORY
                )
                else 'anywhere'
            )
            if (
                data.category in OBSERVATION_LOCATION_CATEGORIES
                and mode == 'vanilla'
            ):
                continue

            address = (
                None
                if (
                    data.category in PAIRED_LOCATION_CATEGORIES
                    and mode == 'vanilla'
                    and not self.is_vanilla_flea_hunt_check(name)
                    and not (
                        self.is_start_with_maps_enabled()
                        and data.category == 'Map'
                    )
                    and not (
                        self.is_automatic_compass_enabled()
                        and data.category == 'Compass'
                        and get_vanilla_reward_name(
                            name,
                            data.category,
                        ) == AUTOMATIC_COMPASS_ITEM
                    )
                    and not (
                        self.is_start_fully_mapped_enabled()
                        and data.category == 'Quill'
                        and get_vanilla_reward_name(
                            name,
                            data.category,
                        ) == QUILL_ITEM
                    )
                )
                else data.code
            )
            if address is None and name in self.get_logic_unknown_locations():
                continue
            anchor = None
            if (
                name != "Goal"
                and data.category != "Journal"
                and name != CRAWFATHER_LOCATION
                and name not in self.get_logic_unknown_locations()
            ):
                anchor = choose_location_anchor(
                    world_location_requirements(
                        self, name,
                        pollip_heart_count=pollip_heart_count,
                    ),
                    abstract_names,
                )
            reward_name = (
                get_vanilla_reward_name(name, data.category)
                if mode == "vanilla"
                else ""
            )
            uses_native_source = (
                reward_name in logic_item_references
                and name not in self._progression_location_rules
                and (name in restored_sources if restored_sources is not None else
                     native_source_requires_assumption(
                         self, name, reward_name, pollip_heart_count, anchor,
                         source_rule_dependencies))
            )
            if uses_native_source:
                self._silksong_native_assumed_source_locations.add(name)
            parent_anchor = None if uses_native_source else anchor
            parent_region = (
                logic_unknown
                if name in self.get_logic_unknown_locations()
                else (
                    native_regions[parent_anchor]
                    if parent_anchor is not None
                    else pharloom
                )
            )
            self._silksong_native_location_anchors[name] = anchor
            location = SilksongLocation(
                self.player,
                name,
                address,
                parent_region,
            )
            location.silksong_randomization_category = data.category
            if data.category == 'Key' and mode == 'shuffle':
                location.silksong_placement_category = 'Key'
            parent_region.locations.append(location)

        # Wish events use their verified source region and rule when available.
        # Otherwise they are placed directly in the completion region.
        self._silksong_active_wish_logic_events = {}
        self._silksong_wish_logic_event_anchors = {}
        excluded_location_names = self.get_goal_excluded_location_names()
        for event in WISH_LOGIC_EVENTS:
            if event.location_name.startswith('Eva Logic: ') and (
                self.get_category_mode('CrestSlot') == 'vanilla'
            ):
                continue
            if (
                (self.is_act_one_content_scope() or (
                    self.is_act_two_content_scope() and self.get_category_mode('Soul') == 'vanilla'
                ))
                and event in (
                    *SILK_AND_SOUL_FULL_POINT_EVENTS,
                    *SILK_AND_SOUL_HALF_POINT_EVENTS,
                )
            ):
                continue
            if event.source_region:
                if (
                    WISH_REGION_SOURCE_LOCATIONS.get(event.source_region)
                    in excluded_location_names
                ):
                    continue
                parent_region = native_regions.get(event.source_region)
                if parent_region is None:
                    continue
                anchor = event.source_region
            else:
                source_name = canonicalize_location_name(
                    event.source_location
                )
                if (
                    source_name in excluded_location_names
                    or source_name in self.get_logic_unknown_locations()
                    or (MAPPER_GRAPH_ENABLED and not ROOM_CHECK_REQUIREMENTS.get(source_name))
                ):
                    continue
                if (
                    source_name == VOLATILE_FLINTBEETLES_QUEST_LOCATION
                    and self.get_category_mode('MemoryLocket') != 'vanilla'
                ):
                    # The option removes this quest source entirely, so it
                    # cannot contribute a Silk and Soul score point.
                    continue
                try:
                    self.multiworld.get_location(
                        source_name,
                        self.player,
                    )
                except (KeyError, StopIteration):
                    # Vanilla observation categories do not create AP reward
                    # locations. Rebuild their exact declarative source under
                    # the same native anchor instead of treating them as free.
                    anchor = choose_location_anchor(
                        world_location_requirements(
                            self, source_name,
                            pollip_heart_count=pollip_heart_count,
                        ),
                        abstract_names,
                    )
                    parent_region = (
                        native_regions[anchor]
                        if anchor is not None
                        else pharloom
                    )
                else:
                    anchor = self._silksong_native_location_anchors.get(
                        source_name
                    )
                    parent_region = (
                        native_regions[anchor]
                        if anchor is not None
                        else pharloom
                    )
            location = SilksongLocation(
                self.player,
                event.location_name,
                None,
                parent_region,
            )
            location.show_in_spoiler = False
            parent_region.locations.append(location)
            self._silksong_active_wish_logic_events[
                event.location_name
            ] = event
            self._silksong_wish_logic_event_anchors[
                event.location_name
            ] = anchor

    def extend_hint_information(self, hint_data) -> None:
        from .entrance_randomization import extend_hints

        extend_hints(self, hint_data)

    def write_spoiler(self, spoiler_handle) -> None:
        assignments = getattr(self, "_progression_assignments", None)
        if assignments is not None:
            if assignments.wishes:
                spoiler_handle.write("\nWish offers:\n")
                for source, target in assignments.wishes:
                    source_name = wish_offer_display_name(source)
                    target_name = wish_offer_display_name(target)
                    spoiler_handle.write(f"  {source_name} -> {target_name}\n")
        if self.get_goal_key() in {FLEA_HUNT_GOAL_KEY, SPELLING_BEE_GOAL_KEY}:
            scope = self.get_content_scope().replace("_", " ").title()
            spoiler_handle.write(f"Content scope: {scope}\n")
        hidden = {
            str(location) for location in self.get_locations()
            if not location.show_in_spoiler
        }
        spoiler = self.multiworld.spoiler
        for sphere in spoiler.playthrough.values():
            if isinstance(sphere, dict):
                for name in hidden:
                    sphere.pop(name, None)
        for name in hidden:
            spoiler.paths.pop(name, None)

    def set_rules(self) -> None:
        self._active_crest_slot_locations = get_active_crest_slot_locations(self)
        set_silksong_rules(self)
        from .enemy_souls import set_rules as set_enemy_rules
        set_enemy_rules(self)
        self._configure_tracker_map()

    def _configure_tracker_map(self) -> None:
        from .tracker import install_marker_status
        from .tracker.wishes import location_mapping
        self.tracker_world = {**self._tracker_world, "poptracker_name_mapping": location_mapping(self)}
        if getattr(self.multiworld, 'generation_is_fake', False):
            install_marker_status()

    @classmethod
    def stage_pre_fill(cls, multiworld) -> None:
        from .requirement_rules import _enable_native_source_memo

        _enable_native_source_memo(multiworld, frozenset(
            world.player for world in multiworld.get_game_worlds(cls.game)
            if world.game == cls.game
        ))
        scope = getattr(
            multiworld,
            "_silksong_shuffle_item_rule_scope",
            None,
        )
        try:
            point_items = Counter((item.player, item.name) for item in multiworld.get_items())
            for world in multiworld.get_game_worlds(cls.game):
                if world.get_goal_key() != "act_3":
                    continue
                available_halves = (
                    2 * point_items[world.player, SILK_AND_SOUL_WISH_POINT_ITEM]
                    + point_items[world.player, SILK_AND_SOUL_WISH_HALF_POINT_ITEM]
                )
                required = get_silk_and_soul_points(world.options)
                if 2 * required > available_halves:
                    raise OptionError(
                        f"Player {world.player}: Silk and Soul requires {required} points, "
                        f"but this configuration contains at most {available_halves / 2:g}. "
                        "Lower Silk and Soul Points."
                    )
            prefill_category_shuffles(multiworld, cls.game)
        finally:
            restore_global_shuffle_item_rules(scope)
            if hasattr(
                multiworld,
                "_silksong_shuffle_item_rule_scope",
            ):
                delattr(
                    multiworld,
                    "_silksong_shuffle_item_rule_scope",
                )
        for world in multiworld.get_game_worlds(cls.game):
            if world.game == cls.game:
                world._finalize_progression_shuffle()
        alphabet_mode_enabled = any(
            getattr(world, "game", None) == cls.game
            and getattr(
                world, "is_alphabet_mode_enabled", lambda: False
            )()
            for world in multiworld.get_game_worlds(cls.game)
        )
        progression_items = tuple(
            item for item in multiworld.itempool if item.advancement
        )
        if not progression_items:
            return
        unfilled_locations = tuple(
            multiworld.get_unfilled_locations()
        )
        progression_location_count = 0
        for location in unfilled_locations:
            if not any(
                location.can_fill(
                    multiworld.state,
                    item,
                    check_access=False,
                )
                for item in progression_items
            ):
                continue
            progression_location_count += 1
            if len(progression_items) <= progression_location_count:
                return
        non_progression_item_count = (
            len(multiworld.itempool) - len(progression_items)
        )
        non_progression_location_count = (
            len(unfilled_locations) - progression_location_count
        )
        advice = (
            "Disable Alphabet Mode, set Crest Slot Randomization to vanilla "
            "or randomize Memory Lockets."
            if alphabet_mode_enabled
            else "Change a restrictive randomization setting or remove "
            "conflicting exclusion, locality or plando settings."
        )
        raise OptionError(
            f"The selected options leave {len(progression_items)} "
            f"progression items for {progression_location_count} "
            "progression-legal locations after category shuffles "
            f"({non_progression_location_count} locations require "
            "non-progression items, but only "
            f"{non_progression_item_count} remain). {advice}"
        )

    @classmethod
    def stage_generate_basic(cls, multiworld) -> None:
        for world in multiworld.get_game_worlds(cls.game):
            world._prepare_start_inventory_pool()
        multiworld._silksong_shuffle_item_rule_scope = (
            enforce_global_shuffle_item_rules(multiworld)
        )

    def fill_hook(self, progitempool, usefulitempool, filleritempool, fill_locations):
        indices = [index for index, item in enumerate(progitempool) if item.player == self.player]
        ordered = sorted((progitempool[index] for index in indices),
                         key=lambda item: item.name in FLEA_ITEM_NAMES)
        for index, item in zip(indices, ordered):
            progitempool[index] = item
        if uses_crest_slot_locket_logic(self):
            if self.options.accessibility == "minimal":
                from rule_builder.rules import Has

                available_items = {
                    id(item): item
                    for item in (
                        *self.multiworld.get_items(),
                        *self.multiworld.precollected_items[self.player],
                    )
                    if item.player == self.player and item.name == MEMORY_LOCKET_ITEM
                }
                budget = min(
                    len(get_active_crest_slot_locations(self)),
                    len(available_items),
                    self.multiworld.get_all_state().count(MEMORY_LOCKET_ITEM, self.player),
                )
                self.set_completion_rule(
                    Has("Victory") & Has(MEMORY_LOCKET_ITEM, budget)
                )
                self._crest_slot_fill_completion_guard = True
            indices = [
                index for index, item in enumerate(progitempool)
                if item.player == self.player
            ]
            # Restrictive fill places from the end. Place Lockets before movement.
            ordered = sorted(
                (progitempool[index] for index in indices),
                key=lambda item: item.name == MEMORY_LOCKET_ITEM,
            )
            for index, item in zip(indices, ordered):
                progitempool[index] = item

        from .category_fill import fill_solo_progression

        fill_solo_progression(self, progitempool, fill_locations)

    @classmethod
    def _build_crest_slot_budget_state(cls, multiworld, excluded_slots, base_state=None):
        state = base_state.copy() if base_state is not None else CollectionState(multiworld)
        remaining_slots = set(excluded_slots)
        filled_locations = tuple(
            location for location in multiworld.get_filled_locations()
            if location.advancement and location not in state.advancements
        )
        while True:
            state.sweep_for_advancements(
                locations=(
                    location for location in filled_locations
                    if location not in remaining_slots
                )
            )
            funded_slots = {
                location
                for world in multiworld.get_game_worlds(cls.game)
                if world.game == cls.game
                and state.count(MEMORY_LOCKET_ITEM, world.player)
                >= get_crest_slot_memory_locket_count(world)
                for location in get_active_crest_slot_locations(world)
            } & remaining_slots
            if not funded_slots:
                return state
            remaining_slots.difference_update(funded_slots)

    @classmethod
    def _repair_crest_slot_locket_budget(
        cls,
        multiworld,
        world,
        excluded_slots,
        slotless_state,
    ):
        non_slot_locations = tuple(
            location
            for location in multiworld.get_filled_locations()
            if location not in excluded_slots
        )
        while True:
            required_count = get_crest_slot_memory_locket_count(world)
            reachable_count = slotless_state.count(
                MEMORY_LOCKET_ITEM,
                world.player,
            )
            if reachable_count >= required_count:
                return slotless_state

            progression_slots = sorted(
                excluded_slots,
                key=lambda location: (location.player, location.name),
            )
            progression_slots = [
                location
                for location in progression_slots
                if (
                    location.item is not None
                    and location.item.advancement
                    and not location.locked
                    and location not in slotless_state.advancements
                )
            ]
            replacement_locations = sorted(
                (
                    location
                    for location in multiworld.get_filled_locations()
                    if (
                        location not in excluded_slots
                        and location.address is not None
                        and location.item is not None
                        and not location.item.advancement
                        and not location.locked
                        and location.can_reach(slotless_state)
                    )
                ),
                key=lambda location: (location.player, location.name),
            )
            if not progression_slots:
                return slotless_state

            from Fill import swap_location_item

            improved_state = None
            fallback_swap = None
            fallback_state = None
            for slot_location in progression_slots:
                for replacement_location in replacement_locations:
                    if not (
                        replacement_location.can_fill(
                            slotless_state,
                            slot_location.item,
                            False,
                        )
                        and slot_location.can_fill(
                            slotless_state,
                            replacement_location.item,
                            False,
                        )
                    ):
                        continue

                    swap_location_item(slot_location, replacement_location)
                    candidate_state = cls._build_crest_slot_budget_state(
                        multiworld, excluded_slots, slotless_state,
                    )
                    candidate_count = candidate_state.count(
                        MEMORY_LOCKET_ITEM,
                        world.player,
                    )
                    if candidate_count > reachable_count:
                        improved_state = candidate_state
                        break
                    if (
                        fallback_swap is None
                        and candidate_state.prog_items != slotless_state.prog_items
                    ):
                        fallback_swap = (
                            slot_location,
                            replacement_location,
                        )
                        fallback_state = candidate_state
                    swap_location_item(slot_location, replacement_location)
                    break
                if improved_state is not None:
                    break

            if improved_state is None:
                if fallback_swap is None:
                    # Tiny pools can have nothing but progression left to swap.
                    for slot_location in progression_slots:
                        for replacement in sorted(non_slot_locations, key=lambda loc: (loc.player, loc.name)):
                            if (replacement.address is None or replacement.locked or replacement.item is None
                                    or not replacement.can_reach(slotless_state)
                                    or not replacement.can_fill(slotless_state, slot_location.item, False)
                                    or not slot_location.can_fill(slotless_state, replacement.item, False)):
                                continue
                            swap_location_item(slot_location, replacement)
                            candidate = cls._build_crest_slot_budget_state(multiworld, excluded_slots)
                            if (candidate.count(MEMORY_LOCKET_ITEM, world.player)
                                    >= get_crest_slot_memory_locket_count(world)
                                    and all(candidate.prog_items[player] >= counts
                                            for player, counts in slotless_state.prog_items.items())):
                                return candidate
                            swap_location_item(slot_location, replacement)
                    return slotless_state
                swap_location_item(*fallback_swap)
                improved_state = fallback_state
            slotless_state = improved_state

    @classmethod
    def stage_post_fill(cls, multiworld) -> None:
        combined_worlds = [
            multiworld.worlds[player]
            for player in multiworld.player_ids
            if (
                multiworld.worlds[player].game == cls.game
                and uses_crest_slot_locket_logic(
                    multiworld.worlds[player]
                )
            )
        ]
        if not combined_worlds:
            return

        for world in combined_worlds:
            if getattr(world, "_crest_slot_fill_completion_guard", False):
                world.set_completion_rule(
                    world._silksong_rule_builder_rules["Completion"]
                )
                world._crest_slot_fill_completion_guard = False

        excluded_slots = set()
        for world in combined_worlds:
            excluded_slots.update(get_active_crest_slot_locations(world))

        from .requirements import CRAFTMETAL_PURCHASE_LOCATIONS

        silksong_players = {world.player for world in multiworld.get_game_worlds(cls.game)}
        placements = tuple((location, location.item) for location in multiworld.get_filled_locations())
        base_state = CollectionState(multiworld)
        base_state.sweep_for_advancements(locations=(
            location for location, _ in placements
            if location not in excluded_slots
            and not (location.player in silksong_players and location.name in CRAFTMETAL_PURCHASE_LOCATIONS)
        ))

        # First move only as much progression out of Crest Slots as needed
        # for the available independent Lockets plus the two-Locket buffer.
        slotless_state = cls._build_crest_slot_budget_state(
            multiworld,
            excluded_slots,
            base_state,
        )
        for world in combined_worlds:
            slotless_state = cls._repair_crest_slot_locket_budget(
                multiworld,
                world,
                excluded_slots,
                slotless_state,
            )

        from .craftmetal import audit_craftmetal_spending

        if any(location.item is not item for location, item in placements):
            base_state = None

        audit_craftmetal_spending(multiworld, [
            multiworld.worlds[player] for player in multiworld.player_ids
            if multiworld.worlds[player].game == cls.game
        ], finalized=False, base_state=base_state)

        if any(location.item is not item for location, item in placements):
            base_state = None

        # Freeze the resulting count before core progression balancing. The
        # slot placements are locked so that balancing cannot change it.
        for world in combined_worlds:
            finalize_crest_slot_memory_locket_logic(world)

        # Move only the progression needed to keep two Lockets in reserve.
        slotless_state = cls._build_crest_slot_budget_state(
            multiworld,
            excluded_slots,
            base_state,
        )
        for world in combined_worlds:
            progression_count = get_crest_slot_progression_item_count(
                world
            )
            required_count = get_crest_slot_memory_locket_count(world)
            reachable_count = slotless_state.count(
                MEMORY_LOCKET_ITEM,
                world.player,
            )
            require_all_slots = (
                world.options.accessibility.value
                != world.options.accessibility.option_minimal
            )
            if (progression_count or require_all_slots) and reachable_count < required_count:
                from Fill import FillError

                if not require_all_slots:
                    try:
                        if multiworld.fulfills_accessibility():
                            continue
                    except FillError:
                        pass
                raise FillError(
                    f"{multiworld.player_name[world.player]}'s Crest Slot "
                    "checks require more Lockets. Only "
                    f"{reachable_count} of the required {required_count} "
                    "Memory Lockets are reachable without Crest Slot "
                    "rewards. Check forced placements, exclusions and "
                    "category settings.",
                    multiworld=multiworld,
                )

    @classmethod
    def stage_finalize_multiworld(cls, multiworld) -> None:
        worlds = [
            multiworld.worlds[player]
            for player in multiworld.player_ids
            if multiworld.worlds[player].game == cls.game
        ]
        if not worlds:
            return

        from .requirement_rules import _enable_native_source_memo

        _enable_native_source_memo(multiworld, frozenset(world.player for world in worlds))
        from .craftmetal import audit_craftmetal_spending

        audit_craftmetal_spending(multiworld, worlds)
        for world in worlds:
            world.build_vog_hint_plan()

    def fill_slot_data(self) -> dict[str, object]:
        from .entrance_randomization import (
            enabled as entrances_enabled,
            node_overrides as entrance_node_overrides,
            slot_entrances,
        )
        goal_key = self.get_goal_key()
        flea_hunt_count = self.get_flea_hunt_goal_count()
        category_modes = self.get_category_modes()
        minor_family_modes = self.get_minor_family_modes()
        purchase_price_modes = self.get_purchase_price_modes()
        purchase_prices = self.get_purchase_prices()
        bone_bottom_statue_tool_pouch_count = (
            get_shell_shard_donation_tool_pouch_requirements(
                purchase_prices
            )['Wish: An Icon of Hope']
        )
        exported_requirements = export_requirements(
            goal_key,
            flea_hunt_count,
            self.allows_bellways_before_bell_beast(),
            (
                get_crest_slot_memory_locket_count(self)
                if uses_crest_slot_locket_logic(self)
                else 0
            ),
            (
                POLLIP_HEART_COUNT
                if self.get_category_mode('PollipHeart') != 'vanilla'
                else 0
            ),
            bone_bottom_statue_tool_pouch_count,
            directional_abilities=self.get_directional_abilities(),
            randomize_needle_upgrades=(
                self.is_needle_upgrade_randomization_enabled()
            ),
            randomize_pale_oils=(
                self.is_pale_oil_randomization_enabled()
            ),
            scuttlebrace_logic_enabled=(
                self.is_scuttlebrace_logic_enabled()
            ),
            spelling_bee_item_names=(
                self.get_spelling_bee_required_item_names()
            ),
            randomized_relics=(
                self.get_category_mode('Relic') != 'vanilla'
            ),
        )
        for name in (self.get_logic_unknown_locations() - LOGIC_UNKNOWN_LOCATIONS
                     - self.get_goal_excluded_location_names()):
            exported_requirements[name] = {'alternatives': [], 'logic_unknown': True}
        slot_data = {
            **self.options.as_dict("accessibility", "start_inventory", "start_inventory_from_pool", "exclude_locations"),
            "world_version": WORLD_VERSION,
            "game_mode": self.options.game_mode.current_key,
            "steel_soul_sites": list(self._steel_soul_sites),
            "native_source_mask": self._native_source_mask(),
            "silk_and_soul_points": get_silk_and_soul_points(self.options),
            "goal": goal_key,
            "content_scope": self.get_content_scope(),
            "spelling_bee_phrase": self.get_spelling_bee_phrase(),
            "flea_hunt_count": flea_hunt_count,
            "starting_location": self.get_starting_location_key(),
            "starting_crest": self.resolve_starting_crest(),
            "force_naked": bool(self.options.force_naked.value),
            "early_sprint": self.is_early_sprint_enabled(),
            "split_dash_and_sprint": self.is_split_dash_and_sprint(),
            "directional_cling_grip": 'Cling Grip' in self.get_directional_abilities(),
            "directional_clawline": 'Clawline' in self.get_directional_abilities(),
            "directional_swift_step": bool({'Swift Step', 'Dash'} & set(self.get_directional_abilities())),
            "swift_step_first_right": self._swift_step_first_right,
            "directional_ledge_grab": 'Ledge Grab' in self.get_directional_abilities(),
            "silk_heart_logic": bool(self.options.silk_heart_logic.value),
            "ledgegrab_ability_rando": (
                self.is_ledgegrab_ability_rando_enabled()
            ),
            "swim_ability_rando": (
                self.is_swim_ability_rando_enabled()
            ),
            "alphabet_mode": self.is_alphabet_mode_enabled(),
            "silk_soar_begone": bool(self.options.silk_soar_begone),
            "crest_slot_memory_locket_count": (
                get_crest_slot_memory_locket_count(self)
                if uses_crest_slot_locket_logic(self)
                else 0
            ),
            "crest_slot_item_flags": {
                location.name: int(location.item.classification)
                for location in get_active_crest_slot_locations(self)
                if location.item is not None
                and location.item.name != MEMORY_LOCKET_ITEM
            },
            "shuffle_wish_offers": bool(self.options.shuffle_wish_offers),
            "individual_relic_turn_ins":
                self.is_individual_relic_turn_ins_enabled(),
            "proficient_combat": self.get_proficient_combat_mode(),
            "platforming_capability": self.get_platforming_capability(),
            "damage_boost_logic": int(self.options.damage_boost_logic.value),
            "flea_brew_jump_logic": self.is_flea_brew_jump_logic_enabled(),
            "sharpdart_logic": self.is_sharpdart_logic_enabled(),
            "scuttlebrace_logic": int(self.options.scuttlebrace_logic.value),
            "heal_stall_logic": int(self.options.heal_stall_logic.value),
            "red_tool_stall_logic": int(self.options.red_tool_stall_logic.value),
            "crest_pogo_logic": int(self.options.crest_pogo_logic.value),
            "needle_strike_logic": int(self.options.needle_strike_logic.value),
            "enemy_pogo_logic": int(self.options.enemy_pogo_logic.value),
            "drill_crystal_pogo_logic": int(self.options.drill_crystal_pogo_logic.value),
            "hazard_respawn_logic": int(self.options.hazard_respawn_logic.value),
            "start_with_maps": self.is_start_with_maps_enabled(),
            "start_fully_mapped":
                self.is_start_fully_mapped_enabled(),
            "automatic_compass": self.is_automatic_compass_enabled(),
            "location_map_markers": self.get_location_map_markers_key(),
            "randomized_bell_markers":
                self.uses_randomized_bell_markers(),
            "randomized_melody_markers":
                self.uses_randomized_melody_markers(),
            "randomized_item_marker_locations":
                self.get_randomized_item_marker_locations(),
            "vog_hints": self.get_vog_hint_plan(),
            "bellway_access": self.get_bellway_access_key(),
            "trails_end_requirement":
                self.get_trails_end_requirement_key(),
            "enemy_rosary_multiplier":
                self.get_enemy_rosary_multiplier_key(),
            "enemy_shard_multiplier":
                self.get_enemy_shard_multiplier_key(),
            "purchase_prices": purchase_prices,
            "faster_dialogue": self.is_faster_dialogue_enabled(),
            "faster_silkheart_animation":
                bool(self.options.faster_silkheart_animation.value),
            "death_link": self.is_death_link_enabled(),
            "death_link_cocoon": self.get_death_link_cocoon_key(),
            "silk_link": self.is_silk_link_enabled(),
            "rosary_link": self.is_rosary_link_enabled(),
            "shell_shard_link": self.is_shell_shard_link_enabled(),
            "knockback_link": bool(self.options.knockback_link.value),
            "trap_disguises": bool(self.options.trap_disguises.value),
            "diving_bell_key_randomization": bool(self.options.diving_bell_key_randomization.value),
            "trap_counts": self.resolve_trap_counts(),
            "requirements": exported_requirements,
            "abstract_requirements": export_abstract_requirements(
                self.allows_bellways_before_bell_beast(),
                self.get_category_mode('CrestSlot') != 'vanilla',
                self.get_starting_location_key(),
                self.get_trails_end_requirement_key(),
                self.is_scuttlebrace_logic_enabled(),
                (
                    POLLIP_HEART_COUNT
                    if self.get_category_mode('PollipHeart') != 'vanilla'
                    else 0
                ),
                entrance_randomizer=entrances_enabled(self),
                randomize_ledge_grab=(
                    self.is_ledgegrab_ability_rando_enabled()
                ),
                randomize_swim=(
                    self.is_swim_ability_rando_enabled()
                ),
                proficient_combat=self.get_proficient_combat_mode(),
                platforming_capability=self.get_platforming_capability(),
                directional_abilities=self.get_directional_abilities(),
                damage_boost_tier=int(self.options.damage_boost_logic.value),
                flea_brew_jump_logic=self.is_flea_brew_jump_logic_enabled(),
                sharpdart_logic=self.is_sharpdart_logic_enabled(),
                red_tool_stall_tier=int(self.options.red_tool_stall_logic.value),
                crest_pogo_tier=int(self.options.crest_pogo_logic.value),
                needle_strike_tier=int(self.options.needle_strike_logic.value),
                enemy_pogo_tier=int(self.options.enemy_pogo_logic.value),
                drill_crystal_pogo_tier=int(self.options.drill_crystal_pogo_logic.value),
                heal_stall_tier=int(self.options.heal_stall_logic.value),
                hazard_respawn_tier=int(self.options.hazard_respawn_logic.value),
                scuttlebrace_tier=int(self.options.scuttlebrace_logic.value),
                bell_shrine_sanity=self.get_category_mode("BellShrine") != "vanilla",
                steel_soul=self.is_steel_soul(),
                steel_soul_sites=self._steel_soul_sites,
                silk_and_soul_points=get_silk_and_soul_points(self.options),
                donation_tool_pouch_requirements=get_shell_shard_donation_tool_pouch_requirements(self.get_purchase_prices()),
                room_node_overrides=entrance_node_overrides(self, connected=True),
            ),
            "logic_item_dependencies": export_logic_item_dependencies(
                self.is_split_dash_and_sprint(),
                silk_heart_logic=bool(self.options.silk_heart_logic.value)
            ),
            "logic_events": export_wish_logic_events(
                exported_requirements,
                getattr(
                    self,
                    "_silksong_active_wish_logic_events",
                    {},
                ),
            ),
        }
        slot_data.update(
            {
                option_name: category_modes[category]
                for category, option_name
                in CATEGORY_OPTION_BY_LOCATION_CATEGORY.items()
            }
        )
        slot_data.update(slot_entrances(self))
        slot_data["minor_pickup_randomization"] = category_modes["Resource"]
        slot_data.update(
            {
                option_name: minor_family_modes[family_key]
                for family_key, option_name
                in MINOR_FAMILY_OPTION_BY_KEY.items()
            }
        )
        slot_data.update(
            {
                option_name: purchase_price_modes[category]
                for category, option_name
                in PRICE_CATEGORY_OPTION_NAMES.items()
            }
        )
        from .progression_shuffle import export_world
        export_world(self, slot_data)
        from .boss_souls import export_world as export_boss_souls
        export_boss_souls(self, slot_data)
        from .npc_souls import export_world as export_npc_souls
        export_npc_souls(self, slot_data)
        from .enemy_souls import export_world as export_enemy_souls
        export_enemy_souls(self, slot_data)
        from .silk_economy import export_world as export_silk_economy
        export_silk_economy(self, slot_data)
        unknown = self.get_logic_unknown_locations()
        for location in self.get_locations():
            if location.address is not None and location.name in unknown:
                slot_data["requirements"][location.name] = {
                    "alternatives": [{"all_of": ["Victory"]}], "logic_unknown": True,
                }
        return slot_data

    def modify_multidata(self, multidata: dict) -> None:
        slot_data = multidata["slot_data"][self.player]
        logic_payload = {
            key: slot_data.pop(key)
            for key in LOGIC_PAYLOAD_FIELDS
        }
        from .map_logic_data import encode
        slot_data.update(encode(logic_payload, slot_data))

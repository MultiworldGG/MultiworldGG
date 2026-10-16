from __future__ import annotations

import dataclasses
from functools import lru_cache
from typing import TYPE_CHECKING, Iterable

from BaseClasses import CollectionState, Item
from NetUtils import JSONMessagePart
from rule_builder.rules import (
    And,
    CanReachLocation,
    CanReachRegion,
    False_,
    Has,
    HasAll,
    HasAllCounts,
    HasAny,
    HasAnyCount,
    HasFromList,
    HasFromListUnique,
    HasGroup,
    HasGroupUnique,
    Or,
    Rule,
    True_,
)

from .display_names import clean_item_display_name
from .room_graph_logic import native_region_name
from .items import get_vanilla_reward_name
from .locations import canonicalize_location_name
from .requirements import (
    CREST_ITEMS,
    ABSTRACT_REQUIREMENTS,
    CLOAK_REQUIRED_SKILL_ITEMS,
    REQUIREMENTS,
    DEFAULT_FLEA_HUNT_GOAL_COUNT,
    MEMORY_LOCKET_ITEM,
    NON_ARCHITECT_CREST_ITEMS,
    PROGRESSIVE_SWIFT_STEP_ITEM,
    STARTING_LOCATION_VANILLA,
    SWIFT_STEP_ITEM,
    TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    USABLE_SCUTTLEBRACE_REQUIREMENT,
    ItemCountRequirement,
    LocationRequirement,
    _has_named_requirement,
    get_abstract_requirements,
    get_goal_requirements,
    get_location_requirements,
    get_logic_item_dependencies,
    get_logic_item_references,
    is_logic_unknown_location,
)

if TYPE_CHECKING:
    from worlds.AutoWorld import World


GAME_NAME = "Hollow Knight: Silksong"


@dataclasses.dataclass()
class NativeRegionRule(Rule, game=GAME_NAME):
    name: str

    def _instantiate(self, world):
        if self.name in getattr(world, '_silksong_unreachable_abstract_names', ()):
            return False_().resolve(world)
        return CanReachRegion(native_region_name(self.name)).resolve(world)


@dataclasses.dataclass()
class AbstractRequirementRule(Rule, game=GAME_NAME):
    """Evaluate one named node in Silksong's cyclic route graph.

    The route graph is solved as a least fixed point by requirements.py. Item
    and count gates outside that graph remain ordinary RuleBuilder leaves, so
    explanations show those requirements directly instead of hiding an entire
    location behind one callable.
    """

    requirement_name: str = ""
    split_dash_and_sprint: bool = False
    allow_bellways_before_bell_beast: bool = False
    skips_tier: int = 0
    randomized_crest_slots_enabled: bool = True
    starting_location: str = STARTING_LOCATION_VANILLA
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK
    scuttlebrace_logic_enabled: bool = True
    randomize_ledge_grab: bool = False
    randomize_swim: bool = False
    pollip_heart_count: int = 0
    proficient_combat: int = 0
    proficient_movement: bool = False
    flea_brew_jump_logic: bool = False
    sharpdart_logic: bool = True
    red_tool_stall_tier: int = 0
    crest_pogo_tier: int = 0
    needle_strike_tier: int = 0
    enemy_pogo_tier: int = 0
    drill_crystal_pogo_tier: int = 0
    heal_stall_tier: int = 0
    hazard_respawn_tier: int = 0
    scuttlebrace_tier: int = 0
    bell_shrine_sanity: bool = False
    steel_soul: bool = False
    steel_soul_sites: tuple[str, ...] = ()
    silk_and_soul_points: int = 17
    silk_heart_logic: bool = False

    def __post_init__(self) -> None:
        super().__post_init__()
        self.steel_soul_sites = tuple(self.steel_soul_sites)

    def _instantiate(self, world: World) -> Rule.Resolved:
        return self.Resolved(
            self.requirement_name,
            self.split_dash_and_sprint,
            self.allow_bellways_before_bell_beast,
            self.skips_tier,
            self.randomized_crest_slots_enabled,
            self.starting_location,
            self.trails_end_requirement,
            self.scuttlebrace_logic_enabled,
            self.randomize_ledge_grab,
            self.randomize_swim,
            self.pollip_heart_count,
            self.proficient_combat,
            self.proficient_movement,
            self.flea_brew_jump_logic,
            self.sharpdart_logic,
            self.red_tool_stall_tier,
            self.crest_pogo_tier,
            self.needle_strike_tier,
            self.enemy_pogo_tier,
            self.drill_crystal_pogo_tier,
            self.heal_stall_tier,
            self.hazard_respawn_tier,
            self.scuttlebrace_tier,
            self.bell_shrine_sanity,
            self.steel_soul,
            self.steel_soul_sites,
            self.silk_and_soul_points,
            self.silk_heart_logic,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        force_recalculate = True
        requirement_name: str
        split_dash_and_sprint: bool
        allow_bellways_before_bell_beast: bool
        skips_tier: int
        randomized_crest_slots_enabled: bool
        starting_location: str
        trails_end_requirement: str
        scuttlebrace_logic_enabled: bool
        randomize_ledge_grab: bool
        randomize_swim: bool
        pollip_heart_count: int
        proficient_combat: int
        proficient_movement: bool
        flea_brew_jump_logic: bool
        sharpdart_logic: bool
        red_tool_stall_tier: int
        crest_pogo_tier: int
        needle_strike_tier: int
        enemy_pogo_tier: int
        drill_crystal_pogo_tier: int
        heal_stall_tier: int
        hazard_respawn_tier: int
        scuttlebrace_tier: int
        bell_shrine_sanity: bool
        steel_soul: bool
        steel_soul_sites: tuple[str, ...]
        silk_and_soul_points: int
        silk_heart_logic: bool

        def _evaluate(self, state: CollectionState) -> bool:
            return _has_named_requirement(
                self.requirement_name,
                state,
                self.player,
                split_dash_and_sprint=self.split_dash_and_sprint,
                allow_bellways_before_bell_beast=(
                    self.allow_bellways_before_bell_beast
                ),
                skips_tier=self.skips_tier,
                randomized_crest_slots_enabled=(
                    self.randomized_crest_slots_enabled
                ),
                starting_location=self.starting_location,
                trails_end_requirement=self.trails_end_requirement,
                scuttlebrace_logic_enabled=(
                    self.scuttlebrace_logic_enabled
                ),
                randomize_ledge_grab=self.randomize_ledge_grab,
                randomize_swim=self.randomize_swim,
                pollip_heart_count=self.pollip_heart_count,
                proficient_combat=self.proficient_combat,
                proficient_movement=self.proficient_movement,
                flea_brew_jump_logic=self.flea_brew_jump_logic,
                sharpdart_logic=self.sharpdart_logic,
                red_tool_stall_tier=self.red_tool_stall_tier,
                crest_pogo_tier=self.crest_pogo_tier,
                needle_strike_tier=self.needle_strike_tier,
                enemy_pogo_tier=self.enemy_pogo_tier,
                drill_crystal_pogo_tier=self.drill_crystal_pogo_tier,
                heal_stall_tier=self.heal_stall_tier,
                hazard_respawn_tier=self.hazard_respawn_tier,
                scuttlebrace_tier=self.scuttlebrace_tier,
                bell_shrine_sanity=self.bell_shrine_sanity,
                steel_soul=self.steel_soul,
                steel_soul_sites=self.steel_soul_sites,
                silk_and_soul_points=self.silk_and_soul_points,
                silk_heart_logic=self.silk_heart_logic,
            )

        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                item_name: {id(self)}
                for item_name in get_logic_item_references()
            }

        def explain_json(
            self,
            state: CollectionState | None = None,
        ) -> list[JSONMessagePart]:
            if state is None:
                prefix = "Can satisfy "
                color = "yellow"
            elif self(state):
                prefix = "Satisfied "
                color = "green"
            else:
                prefix = "Cannot satisfy "
                color = "salmon"
            return [
                {"type": "text", "text": prefix},
                {
                    "type": "color",
                    "color": color,
                    "text": native_region_name(self.requirement_name),
                },
            ]

        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Satisfied" if self(state) else "Cannot satisfy"
            return f"{prefix} {native_region_name(self.requirement_name)}"

        def __str__(self) -> str:
            return f"Can satisfy {native_region_name(self.requirement_name)}"


NativeSourceInventoryKey = tuple[
    int,
    frozenset[tuple[str, int]],
    bool,
]
NativeSourceMemoKey = tuple[int, NativeSourceInventoryKey, int | None]


def sweep_native_pool(base_state, itempool=(), locations=None):
    state = base_state.copy()
    for item in itempool:
        state.collect(item, True)
    sweep_native_sources(state, locations if locations is not None else state.multiworld.get_filled_locations())
    return state


def sweep_native_sources(state, locations):
    pending = [location for location in locations
               if location not in state.advancements
               and location.item is not None and location.item.advancement]
    while pending:
        reachable = []
        for location in pending:
            rule = location.access_rule
            if isinstance(rule, NativeSourceRule.Resolved):
                accessible = (
                    location.parent_region.can_reach(state)
                    and (rule.anchor_requirement_name is None or state.can_reach_region(
                        native_region_name(rule.anchor_requirement_name), rule.player))
                    and rule.child(state)
                )
            else:
                accessible = location.can_reach(state)
            if accessible:
                reachable.append(location)
        if not reachable:
            order = getattr(state.multiworld, "_native_sweep_order", None)
            if order is None:
                order = state.multiworld._native_sweep_order = {}
            for location in sorted(pending, key=lambda loc: order.get(loc, len(order))):
                if location.can_reach(state):
                    reachable.append(location)
                    order.setdefault(location, len(order))
                    break
            if not reachable:
                break
        for location in reachable:
            state.advancements.add(location)
            state.collect(location.item, True, location)
        pending = [location for location in pending if location not in state.advancements]


def _enable_native_source_memo(multiworld, players: frozenset[int] | None = None) -> None:
    from .rules import uses_crest_slot_locket_logic

    slot_players = frozenset(
        player for player in (players or ())
        if multiworld.worlds[player].options.accessibility == "minimal"
        and uses_crest_slot_locket_logic(multiworld.worlds[player])
    )
    setattr(
        multiworld,
        "_silksong_native_source_memo",
        {
            "inventory_keys": {},
            "results": {},
            "slot_players": slot_players,
            **({"players": players} if players is not None else {}),
        },
    )


def _invalidate_native_source_player(multiworld, player: int) -> None:
    memo = getattr(multiworld, "_silksong_native_source_memo", None)
    if memo is None:
        return
    memo["results"] = {key: value for key, value in memo["results"].items() if key[1][0] != player}
    for name in ("inventory_keys", "inventory_counts", "reachable_bounds", "unreachable_bounds"):
        if name in memo:
            memo[name] = {key: value for key, value in memo[name].items() if key[0] != player}


def _lookup_native_source_memo(
    rule: Rule.Resolved,
    state: CollectionState,
) -> tuple[
    dict[NativeSourceMemoKey, bool],
    NativeSourceMemoKey,
    bool | None,
] | None:
    memo = getattr(
        state.multiworld,
        "_silksong_native_source_memo",
        None,
    )
    if memo is None or ("players" in memo and rule.player not in memo["players"]):
        return None
    if "players" in memo and max(len(memo["results"]), len(memo["inventory_keys"])) >= 16384:
        memo.update(inventory_keys={}, results={}, inventory_counts={})

    snapshots = getattr(state, "_silksong_native_inventory_keys", None)
    if snapshots is None:
        snapshots = state._silksong_native_inventory_keys = {}
    inventory = state.prog_items[rule.player]
    snapshot = snapshots.get(rule.player)
    if snapshot is None or inventory != snapshot[0]:
        snapshot = (dict(inventory), frozenset(inventory.items()))
        snapshots[rule.player] = snapshot

    inventory_key: NativeSourceInventoryKey = (
        rule.player,
        snapshot[1],
        state.allow_partial_entrances,
    )
    canonical_inventory_key = memo["inventory_keys"].setdefault(
        inventory_key,
        inventory_key,
    )
    budget = None
    if rule.player in memo["slot_players"]:
        from .rules import get_crest_slot_memory_locket_count

        budget = get_crest_slot_memory_locket_count(state.multiworld.worlds[rule.player])
    key: NativeSourceMemoKey = (id(rule), canonical_inventory_key, budget)
    results = memo["results"]
    cached = results.get(key)
    if cached is None and "players" in memo:
        bound_key = (rule.player, id(rule), budget, state.allow_partial_entrances)
        lower = memo.get("reachable_bounds", {}).get(bound_key)
        if lower is not None and all(
            state.prog_items[rule.player].get(name, 0) >= count for name, count in lower.items()
        ):
            results[key] = True
            return results, key, True
        bound = memo.get("unreachable_bounds", {}).get(bound_key)
        if bound is not None and all(
            count <= bound.get(name, 0) for name, count in state.prog_items[rule.player].items()
        ):
            results[key] = False
            cached = False
    return results, key, cached


def _remember_native_source_result(state, memo_entry, result):
    results, key, _ = memo_entry
    results[key] = result
    memo = state.multiworld._silksong_native_source_memo
    if "players" in memo and memo["results"] is results:
        inventory = memo.setdefault("inventory_counts", {}).setdefault(key[1], dict(key[1][1]))
        bound_key = (key[1][0], key[0], key[2], key[1][2])
        bounds = "reachable_bounds" if result else "unreachable_bounds"
        memo.setdefault(bounds, {})[bound_key] = inventory


@lru_cache(maxsize=1)
def _native_source_item_references():
    return get_logic_item_references()


def _native_item_requirement(rule):
    if type(rule) in {
        Has.Resolved, HasAll.Resolved, HasAny.Resolved, HasAllCounts.Resolved,
        HasAnyCount.Resolved, HasFromList.Resolved, HasFromListUnique.Resolved,
        HasGroup.Resolved, HasGroupUnique.Resolved, False_.Resolved,
    }:
        return rule
    if type(rule) is And.Resolved:
        children = tuple(child for entry in rule.children
                         if (child := _native_item_requirement(entry)) is not None)
        return And.Resolved(children, player=rule.player) if children else None
    if type(rule) is Or.Resolved:
        children = tuple(_native_item_requirement(entry) for entry in rule.children)
        return None if any(child is None for child in children) else Or.Resolved(children, player=rule.player)
    return None


@dataclasses.dataclass()
class NativeSourceRule(Rule, game=GAME_NAME):
    """Preserve the vanilla-source self-reward assumption.

    RuleBuilder's built-in item rules read ``prog_items`` directly. A custom
    rule is required here because the temporary native reward intentionally
    exists only while evaluating its own addressless source.
    """

    location_name: str = ""
    reward_name: str = ""
    split_dash_and_sprint: bool = False
    allow_bellways_before_bell_beast: bool = False
    skips_tier: int = 0
    randomized_crest_slots_enabled: bool = True
    starting_location: str = STARTING_LOCATION_VANILLA
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK
    scuttlebrace_logic_enabled: bool = True
    pollip_heart_count: int = 0
    anchor_requirement_name: str | None = None
    randomize_ledge_grab: bool = False
    randomize_swim: bool = False
    proficient_combat: int = 0
    proficient_movement: bool = False
    flea_brew_jump_logic: bool = False
    sharpdart_logic: bool = True
    red_tool_stall_tier: int = 0
    crest_pogo_tier: int = 0
    needle_strike_tier: int = 0
    enemy_pogo_tier: int = 0
    drill_crystal_pogo_tier: int = 0
    heal_stall_tier: int = 0
    hazard_respawn_tier: int = 0
    scuttlebrace_tier: int = 0
    bell_shrine_sanity: bool = False
    steel_soul: bool = False
    steel_soul_sites: tuple[str, ...] = ()
    silk_and_soul_points: int = 17
    silk_heart_logic: bool = False

    def __post_init__(self) -> None:
        super().__post_init__()
        self.steel_soul_sites = tuple(self.steel_soul_sites)

    def _instantiate(self, world: World) -> Rule.Resolved:
        child_rule = build_location_rule(
            self.location_name,
            split_dash_and_sprint=self.split_dash_and_sprint,
            allow_bellways_before_bell_beast=(
                self.allow_bellways_before_bell_beast
            ),
            skips_tier=self.skips_tier,
            randomized_crest_slots_enabled=(
                self.randomized_crest_slots_enabled
            ),
            starting_location=self.starting_location,
            trails_end_requirement=self.trails_end_requirement,
            scuttlebrace_logic_enabled=self.scuttlebrace_logic_enabled,
            pollip_heart_count=self.pollip_heart_count,
            native_abstract_regions=True,
            anchor_requirement_name=self.anchor_requirement_name,
            randomize_ledge_grab=self.randomize_ledge_grab,
            randomize_swim=self.randomize_swim,
            proficient_combat=self.proficient_combat,
            proficient_movement=self.proficient_movement,
            flea_brew_jump_logic=self.flea_brew_jump_logic,
            sharpdart_logic=self.sharpdart_logic,
            red_tool_stall_tier=self.red_tool_stall_tier,
            crest_pogo_tier=self.crest_pogo_tier,
            needle_strike_tier=self.needle_strike_tier,
            enemy_pogo_tier=self.enemy_pogo_tier,
            drill_crystal_pogo_tier=self.drill_crystal_pogo_tier,
            heal_stall_tier=self.heal_stall_tier,
            hazard_respawn_tier=self.hazard_respawn_tier,
            scuttlebrace_tier=self.scuttlebrace_tier,
            bell_shrine_sanity=self.bell_shrine_sanity,
            steel_soul=self.steel_soul,
            steel_soul_sites=self.steel_soul_sites,
            silk_and_soul_points=self.silk_and_soul_points,
            silk_heart_logic=self.silk_heart_logic,
        )
        return self.Resolved(
            self.location_name,
            self.reward_name,
            self.anchor_requirement_name,
            child_rule.resolve(world),
            world.create_item(self.reward_name),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        force_recalculate = True
        location_name: str
        reward_name: str
        anchor_requirement_name: str | None
        child: Rule.Resolved
        assumed_item: Item
        _item_rule: Rule.Resolved | None = dataclasses.field(init=False, repr=False)

        def __post_init__(self) -> None:
            object.__setattr__(
                self,
                "force_recalculate",
                self.force_recalculate or self.child.force_recalculate,
            )
            super().__post_init__()
            object.__setattr__(self, "_item_rule", _native_item_requirement(self.child))

        def _evaluate(self, state: CollectionState) -> bool:
            if (
                (self.anchor_requirement_name is None
                 or state.can_reach_region(
                     native_region_name(self.anchor_requirement_name), self.player))
                and self.child(state)
            ):
                return True

            memo_entry = _lookup_native_source_memo(self, state)
            if memo_entry is not None:
                results, key, cached_result = memo_entry
                if cached_result is not None:
                    return cached_result

            assumed_state = CollectionState(
                state.multiworld, state.allow_partial_entrances
            )
            assumed_state.prog_items[self.player] = state.prog_items[self.player].copy()
            assumed_state.reachable_regions[self.player] = (
                state.reachable_regions[self.player].copy()
            )
            assumed_state.blocked_connections[self.player] = (
                state.blocked_connections[self.player].copy()
            )
            assumed_state.rule_builder_cache[self.player] = state.rule_builder_cache[self.player].copy()
            from .silk_supply import copy_silk_supply
            copy_silk_supply(state, assumed_state, self.player)
            assumed_state.collect(self.assumed_item, True)
            if self._item_rule is not None and not self._item_rule(assumed_state):
                result = False
            elif (
                self.anchor_requirement_name is not None
                and not assumed_state.can_reach_region(
                    native_region_name(self.anchor_requirement_name),
                    self.player,
                )
            ):
                result = False
            else:
                result = self.child(assumed_state)
            if memo_entry is not None:
                _remember_native_source_result(state, memo_entry, result)
            return result

        def item_dependencies(self) -> dict[str, set[int]]:
            dependencies = {name: {id(self)} for name in _native_source_item_references()}
            for name, rules in self.child.item_dependencies().items():
                dependencies.setdefault(name, set()).update(rules)
            return dependencies

        def region_dependencies(self) -> dict[str, set[int]]:
            dependencies = self.child.region_dependencies()
            if self.anchor_requirement_name is not None:
                name = native_region_name(self.anchor_requirement_name)
                dependencies.setdefault(name, set()).add(id(self))
            return dependencies

        def location_dependencies(self) -> dict[str, set[int]]:
            return self.child.location_dependencies()

        def entrance_dependencies(self) -> dict[str, set[int]]:
            return self.child.entrance_dependencies()

        def explain_json(
            self,
            state: CollectionState | None = None,
        ) -> list[JSONMessagePart]:
            if state is None:
                color = "yellow"
                prefix = "Can reach native source "
            elif self(state):
                color = "green"
                prefix = "Reached native source "
            else:
                color = "salmon"
                prefix = "Cannot reach native source "
            return [
                {"type": "text", "text": prefix},
                {
                    "type": "color",
                    "color": color,
                    "text": self.location_name,
                },
                {
                    "type": "text",
                    "text": f" (assumes its {self.reward_name} reward)",
                },
            ]

        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                prefix = "Can reach"
            else:
                prefix = "Reached" if self(state) else "Cannot reach"
            return (
                f"{prefix} native source {self.location_name} "
                f"(assumes its {self.reward_name} reward)"
            )

        def __str__(self) -> str:
            return (
                f"Can reach native source {self.location_name} "
                f"(assumes its {self.reward_name} reward)"
            )


@dataclasses.dataclass()
class CrestSlotMemoryLocketRule(Rule, game=GAME_NAME):
    """Require the world's frozen randomized Crest Slot Locket budget."""

    def _instantiate(self, world: World) -> Rule.Resolved:
        return self.Resolved(
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        force_recalculate = True

        def _required_count(self, state: CollectionState) -> int:
            from .rules import get_crest_slot_memory_locket_count

            world = state.multiworld.worlds[self.player]
            return get_crest_slot_memory_locket_count(world)

        def _evaluate(self, state: CollectionState) -> bool:
            return state.count(
                MEMORY_LOCKET_ITEM,
                self.player,
            ) >= self._required_count(state)

        def item_dependencies(self) -> dict[str, set[int]]:
            return {MEMORY_LOCKET_ITEM: {id(self)}}

        def explain_json(
            self,
            state: CollectionState | None = None,
        ) -> list[JSONMessagePart]:
            if state is None:
                return [
                    {"type": "text", "text": "Has the required "},
                    {
                        "type": "item_name",
                        "flags": 0b001,
                        "text": MEMORY_LOCKET_ITEM,
                        "player": self.player,
                    },
                    {"type": "text", "text": " count for Crest Slots"},
                ]
            required = self._required_count(state)
            found = state.count(MEMORY_LOCKET_ITEM, self.player)
            color = "green" if found >= required else "salmon"
            return [
                {"type": "text", "text": "Has "},
                {
                    "type": "color",
                    "color": color,
                    "text": f"{found}/{required}",
                },
                {"type": "text", "text": f" {MEMORY_LOCKET_ITEM}"},
            ]

        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            required = self._required_count(state)
            found = state.count(MEMORY_LOCKET_ITEM, self.player)
            return f"Has {found}/{required} {MEMORY_LOCKET_ITEM}"

        def __str__(self) -> str:
            return f"Has the required {MEMORY_LOCKET_ITEM} count for Crest Slots"


def _and_rules(rules: Iterable[Rule]) -> Rule:
    children = tuple(rules)
    if not children:
        return True_()
    if len(children) == 1:
        return children[0]
    return And(*children)


def _or_rules(rules: Iterable[Rule]) -> Rule:
    children = tuple(rules)
    if not children:
        return False_()
    if len(children) == 1:
        return children[0]
    return Or(*children)


def _compile_item_count(count_requirement: ItemCountRequirement) -> Rule:
    item_names = tuple(
        clean_item_display_name(item_name)
        for item_name in count_requirement.item_names
    )
    if len(item_names) == 1:
        return Has(item_names[0], count_requirement.minimum)
    return HasFromList(*item_names, count=count_requirement.minimum)


def _compile_named_requirement(
    requirement_name: str,
    *,
    abstract_requirement_names: frozenset[str],
    split_dash_and_sprint: bool,
    allow_bellways_before_bell_beast: bool,
    skips_tier: int,
    randomized_crest_slots_enabled: bool,
    starting_location: str,
    trails_end_requirement: str,
    scuttlebrace_logic_enabled: bool,
    randomize_ledge_grab: bool,
    randomize_swim: bool,
    pollip_heart_count: int,
    native_abstract_regions: bool = False,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> Rule:
    if (
        not scuttlebrace_logic_enabled
        and requirement_name == USABLE_SCUTTLEBRACE_REQUIREMENT
    ):
        return False_()
    if requirement_name in abstract_requirement_names:
        if native_abstract_regions:
            return NativeRegionRule(requirement_name)
        return AbstractRequirementRule(
            requirement_name=requirement_name,
            split_dash_and_sprint=split_dash_and_sprint,
            allow_bellways_before_bell_beast=(
                allow_bellways_before_bell_beast
            ),
            skips_tier=skips_tier,
            randomized_crest_slots_enabled=(
                randomized_crest_slots_enabled
            ),
            starting_location=starting_location,
            trails_end_requirement=trails_end_requirement,
            scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            pollip_heart_count=pollip_heart_count,
            proficient_combat=proficient_combat,
            proficient_movement=proficient_movement,
            flea_brew_jump_logic=flea_brew_jump_logic,
            sharpdart_logic=sharpdart_logic,
            red_tool_stall_tier=red_tool_stall_tier,
            crest_pogo_tier=crest_pogo_tier,
            needle_strike_tier=needle_strike_tier,
            enemy_pogo_tier=enemy_pogo_tier,
            drill_crystal_pogo_tier=drill_crystal_pogo_tier,
            heal_stall_tier=heal_stall_tier,
            hazard_respawn_tier=hazard_respawn_tier,
            scuttlebrace_tier=scuttlebrace_tier,
            bell_shrine_sanity=bell_shrine_sanity,
            steel_soul=steel_soul,
            steel_soul_sites=steel_soul_sites,
            silk_and_soul_points=silk_and_soul_points,
            silk_heart_logic=silk_heart_logic,
        )

    item_name = clean_item_display_name(requirement_name)
    if split_dash_and_sprint and item_name == SWIFT_STEP_ITEM:
        return Has(PROGRESSIVE_SWIFT_STEP_ITEM, 2)

    dependencies = get_logic_item_dependencies(
        split_dash_and_sprint,
        silk_heart_logic=silk_heart_logic,
    ).get(item_name, ())
    item_rules: list[Rule] = [Has(item_name)]
    if item_name in CLOAK_REQUIRED_SKILL_ITEMS:
        item_rules.append(HasAny(*sorted(CREST_ITEMS)))
    for dependency_name in sorted(set(dependencies)):
        item_rules.append(
            Has(
                clean_item_display_name(dependency_name),
                dependencies.count(dependency_name),
            )
        )
    return _and_rules(item_rules)


def _compile_requirement(
    requirement: LocationRequirement,
    *,
    abstract_requirement_names: frozenset[str],
    split_dash_and_sprint: bool,
    allow_bellways_before_bell_beast: bool,
    skips_tier: int,
    randomized_crest_slots_enabled: bool,
    starting_location: str,
    trails_end_requirement: str,
    scuttlebrace_logic_enabled: bool,
    randomize_ledge_grab: bool,
    randomize_swim: bool,
    pollip_heart_count: int,
    native_abstract_regions: bool = False,
    anchor_requirement_name: str | None = None,
    required_location_stack: tuple[str, ...] = (),
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> Rule:
    if requirement.minimum_skip_tier > skips_tier:
        return False_()

    def compile_named(name: str) -> Rule:
        return _compile_named_requirement(
            name,
            abstract_requirement_names=abstract_requirement_names,
            split_dash_and_sprint=split_dash_and_sprint,
            allow_bellways_before_bell_beast=(
                allow_bellways_before_bell_beast
            ),
            skips_tier=skips_tier,
            randomized_crest_slots_enabled=(
                randomized_crest_slots_enabled
            ),
            starting_location=starting_location,
            trails_end_requirement=trails_end_requirement,
            scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            pollip_heart_count=pollip_heart_count,
            native_abstract_regions=native_abstract_regions,
            proficient_combat=proficient_combat,
            proficient_movement=proficient_movement,
            flea_brew_jump_logic=flea_brew_jump_logic,
            sharpdart_logic=sharpdart_logic,
            red_tool_stall_tier=red_tool_stall_tier,
            crest_pogo_tier=crest_pogo_tier,
            needle_strike_tier=needle_strike_tier,
            enemy_pogo_tier=enemy_pogo_tier,
            drill_crystal_pogo_tier=drill_crystal_pogo_tier,
            heal_stall_tier=heal_stall_tier,
            hazard_respawn_tier=hazard_respawn_tier,
            scuttlebrace_tier=scuttlebrace_tier,
            bell_shrine_sanity=bell_shrine_sanity,
            steel_soul=steel_soul,
            steel_soul_sites=steel_soul_sites,
            silk_and_soul_points=silk_and_soul_points,
            silk_heart_logic=silk_heart_logic,
        )

    def compile_required_location(location_name: str) -> Rule:
        if not native_abstract_regions:
            return CanReachLocation(location_name)
        canonical_name = canonicalize_location_name(location_name)
        if is_logic_unknown_location(canonical_name):
            return True_()
        if canonical_name in required_location_stack:
            return False_()
        alternatives = REQUIREMENTS.get(canonical_name)
        if not alternatives:
            return False_()
        next_stack = (*required_location_stack, canonical_name)
        return _or_rules(
            _compile_requirement(
                alternative,
                abstract_requirement_names=abstract_requirement_names,
                split_dash_and_sprint=split_dash_and_sprint,
                allow_bellways_before_bell_beast=(
                    allow_bellways_before_bell_beast
                ),
                skips_tier=skips_tier,
                randomized_crest_slots_enabled=(
                    randomized_crest_slots_enabled
                ),
                starting_location=starting_location,
                trails_end_requirement=trails_end_requirement,
                scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
                randomize_ledge_grab=randomize_ledge_grab,
                randomize_swim=randomize_swim,
                pollip_heart_count=pollip_heart_count,
                native_abstract_regions=True,
                required_location_stack=next_stack,
                proficient_combat=proficient_combat,
                proficient_movement=proficient_movement,
                flea_brew_jump_logic=flea_brew_jump_logic,
                sharpdart_logic=sharpdart_logic,
                red_tool_stall_tier=red_tool_stall_tier,
                crest_pogo_tier=crest_pogo_tier,
                needle_strike_tier=needle_strike_tier,
                enemy_pogo_tier=enemy_pogo_tier,
                drill_crystal_pogo_tier=drill_crystal_pogo_tier,
                heal_stall_tier=heal_stall_tier,
                hazard_respawn_tier=hazard_respawn_tier,
                scuttlebrace_tier=scuttlebrace_tier,
                bell_shrine_sanity=bell_shrine_sanity,
                steel_soul=steel_soul,
                steel_soul_sites=steel_soul_sites,
                silk_and_soul_points=silk_and_soul_points,
                silk_heart_logic=silk_heart_logic,
            )
            for alternative in alternatives
        )

    if anchor_requirement_name in requirement.all_of:
        requirement = dataclasses.replace(
            requirement,
            all_of=tuple(
                name
                for name in requirement.all_of
                if name != anchor_requirement_name
            ),
        )

    rules: list[Rule] = []
    if requirement.require_any_crest:
        rules.append(HasAny(*sorted(CREST_ITEMS)))
    if requirement.require_silk_spear:
        rules.extend(
            (
                Has("Silkspear"),
                HasAny(*sorted(NON_ARCHITECT_CREST_ITEMS)),
            )
        )
    rules.extend(compile_named(name) for name in requirement.all_of)
    if requirement.any_of:
        rules.append(
            _or_rules(compile_named(name) for name in requirement.any_of)
        )
    rules.extend(
        _compile_item_count(count_requirement)
        for count_requirement in requirement.item_counts
    )
    rules.extend(
        compile_required_location(location_name)
        for location_name in requirement.required_locations
    )
    return _and_rules(rules)


@lru_cache(maxsize=32)
def _abstract_names(revision, *args, **kwargs):
    return frozenset(get_abstract_requirements(*args, **kwargs))


@lru_cache(maxsize=32)
def _combined_names(base, extra):
    return base | extra


@lru_cache(maxsize=8192)
def build_requirements_rule(
    requirements: tuple[LocationRequirement, ...],
    *,
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    native_abstract_regions: bool = False,
    anchor_requirement_name: str | None = None,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    extra_abstract_requirement_names: frozenset[str] = frozenset(),
    silk_heart_logic: bool = False,
) -> Rule:
    """Compile declarative Silksong requirements into a RuleBuilder tree."""

    if extra_abstract_requirement_names and not native_abstract_regions:
        raise ValueError("Seed-specific events require native abstract regions.")

    abstract_requirement_names = _abstract_names(
        ABSTRACT_REQUIREMENTS.revision,
        allow_bellways_before_bell_beast,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        pollip_heart_count,
        randomize_ledge_grab=randomize_ledge_grab,
        randomize_swim=randomize_swim,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
    )
    abstract_requirement_names = _combined_names(abstract_requirement_names, extra_abstract_requirement_names)
    return _or_rules(
        _compile_requirement(
            requirement,
            abstract_requirement_names=abstract_requirement_names,
            split_dash_and_sprint=split_dash_and_sprint,
            allow_bellways_before_bell_beast=(
                allow_bellways_before_bell_beast
            ),
            skips_tier=skips_tier,
            randomized_crest_slots_enabled=(
                randomized_crest_slots_enabled
            ),
            starting_location=starting_location,
            trails_end_requirement=trails_end_requirement,
            scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
            randomize_ledge_grab=randomize_ledge_grab,
            randomize_swim=randomize_swim,
            pollip_heart_count=pollip_heart_count,
            native_abstract_regions=native_abstract_regions,
            anchor_requirement_name=anchor_requirement_name,
            proficient_combat=proficient_combat,
            proficient_movement=proficient_movement,
            flea_brew_jump_logic=flea_brew_jump_logic,
            sharpdart_logic=sharpdart_logic,
            red_tool_stall_tier=red_tool_stall_tier,
            crest_pogo_tier=crest_pogo_tier,
            needle_strike_tier=needle_strike_tier,
            enemy_pogo_tier=enemy_pogo_tier,
            drill_crystal_pogo_tier=drill_crystal_pogo_tier,
            heal_stall_tier=heal_stall_tier,
            hazard_respawn_tier=hazard_respawn_tier,
            scuttlebrace_tier=scuttlebrace_tier,
            bell_shrine_sanity=bell_shrine_sanity,
            steel_soul=steel_soul,
            steel_soul_sites=steel_soul_sites,
            silk_and_soul_points=silk_and_soul_points,
            silk_heart_logic=silk_heart_logic,
        )
        for requirement in requirements
    )


def build_location_rule(
    location_name: str,
    *,
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    pollip_heart_count: int = 0,
    native_abstract_regions: bool = False,
    anchor_requirement_name: str | None = None,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> Rule:
    if is_logic_unknown_location(location_name):
        return True_()
    return build_requirements_rule(
        get_location_requirements(
            location_name,
            pollip_heart_count=pollip_heart_count,
        ),
        split_dash_and_sprint=split_dash_and_sprint,
        allow_bellways_before_bell_beast=allow_bellways_before_bell_beast,
        skips_tier=skips_tier,
        randomized_crest_slots_enabled=randomized_crest_slots_enabled,
        starting_location=starting_location,
        trails_end_requirement=trails_end_requirement,
        scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
        randomize_ledge_grab=randomize_ledge_grab,
        randomize_swim=randomize_swim,
        pollip_heart_count=pollip_heart_count,
        native_abstract_regions=native_abstract_regions,
        anchor_requirement_name=anchor_requirement_name,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
        silk_heart_logic=silk_heart_logic,
    )


def build_goal_rule(
    goal_key: str,
    *,
    split_dash_and_sprint: bool = False,
    flea_hunt_count: int = DEFAULT_FLEA_HUNT_GOAL_COUNT,
    pollip_heart_count: int = 0,
    spelling_bee_item_names: tuple[str, ...] | None = None,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    native_abstract_regions: bool = False,
    anchor_requirement_name: str | None = None,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> Rule:
    return build_requirements_rule(
        get_goal_requirements(
            goal_key,
            flea_hunt_count,
            pollip_heart_count,
            spelling_bee_item_names,
        ),
        split_dash_and_sprint=split_dash_and_sprint,
        allow_bellways_before_bell_beast=allow_bellways_before_bell_beast,
        skips_tier=skips_tier,
        randomized_crest_slots_enabled=randomized_crest_slots_enabled,
        starting_location=starting_location,
        trails_end_requirement=trails_end_requirement,
        scuttlebrace_logic_enabled=scuttlebrace_logic_enabled,
        randomize_ledge_grab=randomize_ledge_grab,
        randomize_swim=randomize_swim,
        pollip_heart_count=pollip_heart_count,
        native_abstract_regions=native_abstract_regions,
        anchor_requirement_name=anchor_requirement_name,
        proficient_combat=proficient_combat,
        proficient_movement=proficient_movement,
        flea_brew_jump_logic=flea_brew_jump_logic,
        sharpdart_logic=sharpdart_logic,
        red_tool_stall_tier=red_tool_stall_tier,
        crest_pogo_tier=crest_pogo_tier,
        needle_strike_tier=needle_strike_tier,
        enemy_pogo_tier=enemy_pogo_tier,
        drill_crystal_pogo_tier=drill_crystal_pogo_tier,
        heal_stall_tier=heal_stall_tier,
        hazard_respawn_tier=hazard_respawn_tier,
        scuttlebrace_tier=scuttlebrace_tier,
        bell_shrine_sanity=bell_shrine_sanity,
        steel_soul=steel_soul,
        steel_soul_sites=steel_soul_sites,
        silk_and_soul_points=silk_and_soul_points,
        silk_heart_logic=silk_heart_logic,
    )


def build_native_source_rule(
    location_name: str,
    category: str,
    *,
    split_dash_and_sprint: bool = False,
    allow_bellways_before_bell_beast: bool = False,
    skips_tier: int = 0,
    randomized_crest_slots_enabled: bool = True,
    starting_location: str = STARTING_LOCATION_VANILLA,
    trails_end_requirement: str = TRAILS_END_REQUIREMENT_SHAKRA_STOCK,
    scuttlebrace_logic_enabled: bool = True,
    pollip_heart_count: int = 0,
    anchor_requirement_name: str | None = None,
    randomize_ledge_grab: bool = False,
    randomize_swim: bool = False,
    proficient_combat: int = 0,
    proficient_movement: bool = False,
    flea_brew_jump_logic: bool = False,
    sharpdart_logic: bool = True,
    red_tool_stall_tier: int = 0,
    crest_pogo_tier: int = 0,
    needle_strike_tier: int = 0,
    enemy_pogo_tier: int = 0,
    drill_crystal_pogo_tier: int = 0,
    heal_stall_tier: int = 0,
    hazard_respawn_tier: int = 0,
    scuttlebrace_tier: int = 0,
    bell_shrine_sanity: bool = False,
    steel_soul: bool = False,
    steel_soul_sites: tuple[str, ...] = (),
    silk_and_soul_points: int = 17,
    silk_heart_logic: bool = False,
) -> Rule:
    if is_logic_unknown_location(location_name):
        return True_()
    return NativeSourceRule(
        location_name,
        get_vanilla_reward_name(location_name, category),
        split_dash_and_sprint,
        allow_bellways_before_bell_beast,
        skips_tier,
        randomized_crest_slots_enabled,
        starting_location,
        trails_end_requirement,
        scuttlebrace_logic_enabled,
        pollip_heart_count,
        anchor_requirement_name,
        randomize_ledge_grab,
        randomize_swim,
        proficient_combat,
        proficient_movement,
        flea_brew_jump_logic,
        sharpdart_logic,
        red_tool_stall_tier,
        crest_pogo_tier,
        needle_strike_tier,
        enemy_pogo_tier,
        drill_crystal_pogo_tier,
        heal_stall_tier,
        hazard_respawn_tier,
        scuttlebrace_tier,
        bell_shrine_sanity,
        steel_soul,
        steel_soul_sites,
        silk_and_soul_points,
        silk_heart_logic=silk_heart_logic,
    )

from __future__ import annotations

from .options import get_silk_and_soul_points

from BaseClasses import Item, ItemClassification
from Options import OptionError
from rule_builder.rules import Has, HasAny, True_
from worlds.generic.Rules import add_item_rule

from .items import (
    PROGRESSIVE_NEEDLE_UPGRADE_ITEM,
    PROGRESSION_ITEMS,
    item_data_table,
)
from .locations import (
    COURIER_DELIVERY_WISH_LOCATION_NAMES,
    OBSERVATION_LOCATION_CATEGORIES,
    PINMASTER_OIL_QUEST_LOCATION,
    WISH_REWARD_LOCATION_BY_COMPLETION,
    RELIC_TURN_IN_LOCATION_CATEGORY,
    SCROUNGE_RELIC_ITEM_NAMES,
    VOLATILE_FLINTBEETLES_QUEST_LOCATION,
    canonicalize_location_name,
    location_data_table,
)
from .options import CATEGORY_OPTION_BY_LOCATION_CATEGORY
from .prices import get_shell_shard_donation_tool_pouch_requirements
from .requirements import (
    CREST_SLOT_LOCATION_NAMES,
    JUNK_ONLY_LOCATIONS,
    LOGIC_UNKNOWN_LOCATIONS,
    MAPPER_GRAPH_ENABLED,
    MEMORY_LOCKET_ITEM,
    POLLIP_HEART_COUNT,
    ROSARY_BANK_GATED_LOCATIONS,
    SIMPLE_KEY_ROSARY_BANK,
    UNVERIFIED_PROGRESSION_LOCATIONS,
    get_crawfather_requirements,
    get_pinmaster_oil_requirements,
    validate_requirements,
)
from .requirement_rules import (
    CrestSlotMemoryLocketRule,
    build_goal_rule,
    build_location_rule,
    build_native_source_rule,
    build_requirements_rule,
)

PROGRESSIVE_TOOL_POUCH_ITEM = 'Progressive Tool Pouch'
RESTORATION_OF_BELLHART_QUEST_LOCATION = (
    'Wish: Restoration of Bellhart'
)
CRAWFATHER_LOCATION = 'Boss: Crawfather'
CREST_SLOT_MEMORY_LOCKET_BUFFER = 2


def _is_not_progression_item(item: Item) -> bool:
    return not item.advancement


def _is_not_memory_locket(item: Item) -> bool:
    return item.name != MEMORY_LOCKET_ITEM


def _is_not_rosary_bank_key(item: Item) -> bool:
    return item.name != SIMPLE_KEY_ROSARY_BANK


def uses_crest_slot_locket_logic(world) -> bool:
    return world.get_category_mode('CrestSlot') != 'vanilla'


def uses_randomized_memory_lockets_for_crest_slots(world) -> bool:
    memory_locket_mode = world.get_category_mode('MemoryLocket')
    crest_slot_mode = world.get_category_mode('CrestSlot')
    return (
        memory_locket_mode != 'vanilla'
        and crest_slot_mode != 'vanilla'
    )


def get_crest_slot_progression_item_count(world) -> int:
    return sum(
        bool(
            getattr(location, "item", None) is not None
            and getattr(location.item, "advancement", False)
        )
        for location in get_active_crest_slot_locations(world)
    )


def get_active_crest_slot_locations(world) -> tuple:
    cached = getattr(world, "_active_crest_slot_locations", None)
    if cached is not None:
        return cached
    get_location = getattr(world.multiworld, "get_location", None)
    if not callable(get_location):
        return ()

    locations = []
    for location_name in CREST_SLOT_LOCATION_NAMES:
        try:
            location = get_location(location_name, world.player)
        except (KeyError, StopIteration):
            continue
        locations.append(location)
    return tuple(locations)


def get_crest_slot_memory_locket_count(world) -> int:
    """Return the shared consumable budget for randomized Crest Slots.

    Full accessibility must keep every physical slot collectable, so it
    conservatively requires one Locket for every active slot.  Minimal only
    needs the progression-bearing slots for completion. Two spare Lockets
    preserve the established buffer for an optional purchase or mistake.
    """

    frozen_count = getattr(
        world,
        "_crest_slot_memory_locket_count",
        None,
    )
    if frozen_count is not None:
        return int(frozen_count)

    active_count = len(get_active_crest_slot_locations(world))
    if active_count == 0:
        return 0

    accessibility = getattr(world.options, "accessibility", None)
    accessibility_value = getattr(accessibility, "value", accessibility)
    minimal_value = getattr(accessibility, "option_minimal", 2)
    if accessibility is None or accessibility_value != minimal_value:
        return active_count

    return min(
        active_count,
        max(
            1,
            get_crest_slot_progression_item_count(world)
            + CREST_SLOT_MEMORY_LOCKET_BUFFER,
        ),
    )


def finalize_crest_slot_memory_locket_logic(world) -> None:
    if not uses_crest_slot_locket_logic(world):
        world._crest_slot_memory_locket_count = None
        return

    world._crest_slot_memory_locket_count = (
        get_crest_slot_memory_locket_count(world)
    )
    apply_crest_slot_memory_locket_rules(world)
    for location_name in CREST_SLOT_LOCATION_NAMES:
        try:
            location = world.multiworld.get_location(
                location_name,
                world.player,
            )
        except (KeyError, StopIteration):
            continue
        if getattr(location, "item", None) is not None:
            # Progression balancing must not change the number after the
            # access rules and client slot data have agreed on it.
            location.locked = True


def apply_crest_slot_memory_locket_rules(world) -> None:
    count = world._crest_slot_memory_locket_count
    if count is None:
        return
    for name, base_rule in world._crest_slot_base_rules.items():
        rule = base_rule & Has(MEMORY_LOCKET_ITEM, count)
        world._silksong_rule_builder_rules[name] = rule
        world.set_rule(world.multiworld.get_location(name, world.player), rule)


def _is_matching_shuffle_item(category: str, player: int):
    def item_rule(item: Item) -> bool:
        return (
            getattr(
                item,
                "silksong_placement_category",
                None,
            )
            == category
            and item.player == player
        )

    return item_rule


def enforce_global_shuffle_item_rules(multiworld):
    itempool = getattr(multiworld, "itempool", None)
    if itempool is not None and not any(
        getattr(item, "silksong_placement_category", None) is not None
        for item in itempool
    ):
        return None
    enabled = [True]
    installed_rules = []
    for location in multiworld.get_locations():
        target_category = getattr(
            location,
            "silksong_placement_category",
            None,
        )
        target_game = getattr(location, "game", None)
        target_player = location.player

        def item_rule(
            item: Item,
            target_category: str | None = target_category,
            target_game: str | None = target_game,
            target_player: int = target_player,
            enabled: list[bool] = enabled,
        ) -> bool:
            if not enabled[0]:
                return True
            item_category = getattr(
                item,
                "silksong_placement_category",
                None,
            )
            if item_category is None:
                return True
            if (
                target_game != "Hollow Knight: Silksong"
                or target_category != item_category
                or target_player != item.player
            ):
                return False
            return True

        previous_rule = location.item_rule
        add_item_rule(location, item_rule)
        installed_rules.append(
            (location, previous_rule, location.item_rule)
        )
    return enabled, installed_rules


def restore_global_shuffle_item_rules(scope) -> None:
    if scope is None:
        return
    enabled, installed_rules = scope
    enabled[0] = False
    for location, previous_rule, installed_rule in installed_rules:
        if location.item_rule is installed_rule:
            location.item_rule = previous_rule


def set_silksong_rules(world) -> None:
    validate_requirements(
        location_data_table.keys() | COURIER_DELIVERY_WISH_LOCATION_NAMES,
        item_data_table.keys(),
        PROGRESSION_ITEMS,
        check_vanilla_self_locks=False,
    )
    logic_unknown_locations = getattr(world, 'get_logic_unknown_locations', lambda: LOGIC_UNKNOWN_LOCATIONS)()
    protected = (logic_unknown_locations | JUNK_ONLY_LOCATIONS
                 | (UNVERIFIED_PROGRESSION_LOCATIONS - CREST_SLOT_LOCATION_NAMES))
    blocked_priorities = sorted(
        location.name for location in world.multiworld.get_unfilled_locations(world.player)
        if location.address is not None and location.name in protected
        and location.name in world.options.priority_locations.value
    )
    if blocked_priorities:
        raise OptionError(
            f"{world.multiworld.get_player_name(world.player)}: priority_locations requires progression, "
            "but these locations cannot hold it because they are missable or their logic is unverified: "
            + ", ".join(blocked_priorities)
            + ". Remove them from priority_locations, including any groups that contain them."
        )
    split_dash_and_sprint = world.is_split_dash_and_sprint()
    randomize_ledge_grab = world.is_ledgegrab_ability_rando_enabled()
    randomize_swim = world.is_swim_ability_rando_enabled()
    randomize_needle_upgrades = world.is_needle_upgrade_randomization_enabled()
    randomize_pale_oils = world.is_pale_oil_randomization_enabled()
    allow_bellways_before_bell_beast = (
        world.allows_bellways_before_bell_beast()
    )
    skips_tier = 0
    proficient_combat = world.get_proficient_combat_mode()
    proficient_movement = bool(getattr(getattr(world.options, "proficient_movement", None), "value", 0))
    flea_brew_jump_logic = bool(getattr(getattr(world.options, "flea_brew_jump_logic", None), "value", 0))
    sharpdart_logic = bool(getattr(getattr(world.options, "sharpdart_logic", None), "value", 0))
    red_tool_stall_tier = int(world.options.red_tool_stall_logic.value)
    crest_pogo_tier = int(world.options.crest_pogo_logic.value)
    needle_strike_tier = int(world.options.needle_strike_logic.value)
    enemy_pogo_tier = int(world.options.enemy_pogo_logic.value)
    drill_crystal_pogo_tier = int(world.options.drill_crystal_pogo_logic.value)
    heal_stall_tier = int(world.options.heal_stall_logic.value)
    hazard_respawn_tier = int(world.options.hazard_respawn_logic.value)
    scuttlebrace_tier = int(world.options.scuttlebrace_logic.value)
    bell_shrine_sanity = world.get_category_mode("BellShrine") != "vanilla"
    scuttlebrace_logic_enabled = (
        world.is_scuttlebrace_logic_enabled()
    )
    individual_relic_turn_ins = bool(
        world.options.individual_relic_turn_ins.value
    )
    relic_mode = world.get_category_mode('Relic')
    memory_locket_mode = world.get_category_mode('MemoryLocket')
    crest_slot_mode = world.get_category_mode('CrestSlot')
    pollip_heart_mode = world.get_category_mode('PollipHeart')
    pollip_heart_count = (
        POLLIP_HEART_COUNT
        if pollip_heart_mode != 'vanilla'
        else 0
    )
    crest_slot_locket_logic = uses_crest_slot_locket_logic(world)
    randomized_crest_slots_enabled = crest_slot_mode != 'vanilla'
    starting_location = world.get_starting_location_key()
    trails_end_requirement = world.get_trails_end_requirement_key()
    shell_shard_donation_pouch_requirements = (
        get_shell_shard_donation_tool_pouch_requirements(
            world.get_purchase_prices()
        )
    )
    # The Bone Bottom fossil does not exist until the statue donation is
    # completed. Inherit that donation's randomized hard-capacity gate so a
    # downstream item cannot be considered reachable before Hornet can carry
    # enough Shell Shards to construct the statue.
    shell_shard_donation_pouch_requirements[
        'Bone Bottom - Shell Shard Cache'
    ] = shell_shard_donation_pouch_requirements.get(
        'Wish: An Icon of Hope',
        0,
    )
    excluded_location_names = world.get_goal_excluded_location_names()
    world._silksong_rule_builder_rules = {}
    world._crest_slot_base_rules = {}

    for location_name, location_data in location_data_table.items():
        if location_name == "Goal":
            continue
        if location_name in excluded_location_names:
            continue
        if (
            location_data.category == RELIC_TURN_IN_LOCATION_CATEGORY
            and not individual_relic_turn_ins
        ):
            continue
        if location_name in WISH_REWARD_LOCATION_BY_COMPLETION:
            continue
        mode = (
            world.get_location_randomization_mode(
                location_name,
                location_data.category,
            )
            if location_data.category
            in {*CATEGORY_OPTION_BY_LOCATION_CATEGORY, "Resource"}
            else "anywhere"
        )
        if (
            location_data.category in OBSERVATION_LOCATION_CATEGORIES
            and mode == "vanilla"
        ):
            continue

        location = world.multiworld.get_location(location_name, world.player)
        shuffled_requirements = getattr(world, "_progression_location_rules", {}).get(location_name)
        if shuffled_requirements is not None:
            from .native_regions import native_rule_options
            location_rule = build_requirements_rule(
                shuffled_requirements,
                anchor_requirement_name=world._silksong_native_location_anchors.get(location_name),
                extra_abstract_requirement_names=world._silksong_native_abstract_names,
                **native_rule_options(world),
            )
        elif location_name in getattr(
            world,
            "_silksong_native_assumed_source_locations",
            (),
        ):
            location_rule = build_native_source_rule(
                location_name,
                location_data.category,
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
                scuttlebrace_logic_enabled=(
                    scuttlebrace_logic_enabled
                ),
                randomize_ledge_grab=randomize_ledge_grab,
                randomize_swim=randomize_swim,
                pollip_heart_count=pollip_heart_count,
                anchor_requirement_name=(
                    world._silksong_native_location_anchors.get(
                        location_name
                    )
                ),
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
                silk_and_soul_points=get_silk_and_soul_points(world.options),
                silk_heart_logic=bool(world.options.silk_heart_logic.value),
            )
        else:
            location_rule = build_location_rule(
                location_name,
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
                scuttlebrace_logic_enabled=(
                    scuttlebrace_logic_enabled
                ),
                randomize_ledge_grab=randomize_ledge_grab,
                randomize_swim=randomize_swim,
                pollip_heart_count=pollip_heart_count,
                native_abstract_regions=True,
                anchor_requirement_name=(
                    world._silksong_native_location_anchors.get(
                        location_name
                    )
                ),
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
                silk_and_soul_points=get_silk_and_soul_points(world.options),
                silk_heart_logic=bool(world.options.silk_heart_logic.value),
            )
            if location_name == CRAWFATHER_LOCATION:
                location_rule = build_requirements_rule(
                    get_crawfather_requirements(
                        randomize_needle_upgrades,
                        randomize_pale_oils,
                    ),
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
                    scuttlebrace_logic_enabled=(
                        scuttlebrace_logic_enabled
                    ),
                    randomize_ledge_grab=randomize_ledge_grab,
                    randomize_swim=randomize_swim,
                    pollip_heart_count=pollip_heart_count,
                    native_abstract_regions=True,
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
                    silk_and_soul_points=get_silk_and_soul_points(world.options),
                    silk_heart_logic=bool(world.options.silk_heart_logic.value),
                )
        if location_name == PINMASTER_OIL_QUEST_LOCATION:
            location_rule = build_requirements_rule(
                get_pinmaster_oil_requirements(randomize_pale_oils),
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
                scuttlebrace_logic_enabled=(
                    scuttlebrace_logic_enabled
                ),
                randomize_ledge_grab=randomize_ledge_grab,
                randomize_swim=randomize_swim,
                pollip_heart_count=pollip_heart_count,
                native_abstract_regions=True,
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
                silk_and_soul_points=get_silk_and_soul_points(world.options),
                silk_heart_logic=bool(world.options.silk_heart_logic.value),
            )

        required_tool_pouch_count = (
            shell_shard_donation_pouch_requirements.get(location_name, 0)
        )
        if required_tool_pouch_count > 0:
            location_rule = location_rule & Has(
                PROGRESSIVE_TOOL_POUCH_ITEM,
                required_tool_pouch_count,
            )
        if (
            randomize_needle_upgrades
            and location_name == RESTORATION_OF_BELLHART_QUEST_LOCATION
        ):
            # FullQuestBase Belltown House Start requires nailUpgrades > 0.
            # The client mirrors received Progressive Needle Upgrades into
            # that native field, so this is the shuffled-mode gate.
            location_rule = location_rule & Has(
                PROGRESSIVE_NEEDLE_UPGRADE_ITEM
            )

        if (
            relic_mode != 'vanilla'
            and location_name == RESTORATION_OF_BELLHART_QUEST_LOCATION
        ):
            # BelltownRelicDealerGaveRelic is set only when Scrounge takes at
            # least one deposited relic. In vanilla mode the free Moss Grotto
            # Commandment supplies it. Shuffled modes need an actual received
            # Scrounge-compatible relic before this Wish can appear.
            location_rule = location_rule & HasAny(
                *SCROUNGE_RELIC_ITEM_NAMES
            )

        if location_name in logic_unknown_locations and (
            MAPPER_GRAPH_ENABLED or location_name not in LOGIC_UNKNOWN_LOCATIONS
        ):
            location_rule = True_()

        if (
            crest_slot_locket_logic
            and location_name in CREST_SLOT_LOCATION_NAMES
            and location_name not in logic_unknown_locations
        ):
            world._crest_slot_base_rules[location_name] = location_rule
            count = world._crest_slot_memory_locket_count
            if count is None and world.options.accessibility != "minimal":
                count = get_crest_slot_memory_locket_count(world)
            location_rule = location_rule & (
                CrestSlotMemoryLocketRule() if count is None
                else Has(MEMORY_LOCKET_ITEM, count)
            )
        from .npc_souls import location_gate
        npc_gate = location_gate(world, location_name)
        if npc_gate is not None:
            location_rule = location_rule & npc_gate
        world._silksong_rule_builder_rules[location_name] = location_rule
        world.set_rule(location, location_rule)

        if getattr(location, "item", None) is not None:
            continue

        if location_data.category == "Key" and mode == "shuffle":
            add_item_rule(location, _is_matching_shuffle_item("Key", world.player))

        if location_name in ROSARY_BANK_GATED_LOCATIONS:
            # The door's own key is excluded from these locations. Its
            # classification is option-dependent: useful when every bank
            # reward is vanilla and progression whenever at least one becomes
            # an AP check.
            add_item_rule(location, _is_not_rosary_bank_key)

        if (
            location_name in logic_unknown_locations
            or location_name in JUNK_ONLY_LOCATIONS
        ):
            add_item_rule(location, _is_not_progression_item)
        elif location_name in CREST_SLOT_LOCATION_NAMES:
            add_item_rule(location, _is_not_memory_locket)
        elif location_name in UNVERIFIED_PROGRESSION_LOCATIONS:
            add_item_rule(location, _is_not_progression_item)

    for event in getattr(
        world,
        "_silksong_active_wish_logic_events",
        {},
    ).values():
        event_location = world.multiworld.get_location(
            event.location_name,
            world.player,
        )
        if event.source_location:
            source_name = canonicalize_location_name(
                event.source_location
            )
            event_rule = world._silksong_rule_builder_rules.get(source_name)
            if event_rule is None and source_name in getattr(world, "_progression_location_rules", {}):
                from .native_regions import native_rule_options
                event_rule = build_requirements_rule(
                    world._progression_location_rules[source_name],
                    anchor_requirement_name=world._silksong_wish_logic_event_anchors.get(event.location_name),
                    extra_abstract_requirement_names=world._silksong_native_abstract_names,
                    **native_rule_options(world),
                )
            if event_rule is None:
                # Vanilla observation categories deliberately omit their AP
                # reward location.  The native Wish still exists, so rebuild
                # the same declarative, anchor-relative rule for this hidden
                # completion event instead of treating the source as free.
                event_rule = build_location_rule(
                    source_name,
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
                    scuttlebrace_logic_enabled=(
                        scuttlebrace_logic_enabled
                    ),
                    randomize_ledge_grab=randomize_ledge_grab,
                    randomize_swim=randomize_swim,
                    pollip_heart_count=pollip_heart_count,
                    native_abstract_regions=True,
                    anchor_requirement_name=(
                        world._silksong_wish_logic_event_anchors.get(
                            event.location_name
                        )
                    ),
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
                    silk_and_soul_points=get_silk_and_soul_points(world.options),
                    silk_heart_logic=bool(world.options.silk_heart_logic.value),
                )
                required_tool_pouch_count = (
                    shell_shard_donation_pouch_requirements.get(
                        source_name,
                        0,
                    )
                )
                if required_tool_pouch_count > 0:
                    event_rule = event_rule & Has(
                        PROGRESSIVE_TOOL_POUCH_ITEM,
                        required_tool_pouch_count,
                    )
                if (
                    randomize_needle_upgrades
                    and source_name
                    == RESTORATION_OF_BELLHART_QUEST_LOCATION
                ):
                    event_rule = event_rule & Has(
                        PROGRESSIVE_NEEDLE_UPGRADE_ITEM
                    )
                if (
                    relic_mode != 'vanilla'
                    and source_name
                    == RESTORATION_OF_BELLHART_QUEST_LOCATION
                ):
                    event_rule = event_rule & HasAny(
                        *SCROUNGE_RELIC_ITEM_NAMES
                    )
            world._silksong_rule_builder_rules[
                event.location_name
            ] = event_rule
            world.set_rule(event_location, event_rule)
        event_location.place_locked_item(
            world.create_event(event.item_name)
        )

    goal_key = world.get_goal_key()
    flea_hunt_count = world.get_flea_hunt_goal_count()
    goal = world.multiworld.get_location("Goal", world.player)
    goal_rule = build_goal_rule(
        goal_key,
        split_dash_and_sprint=split_dash_and_sprint,
        flea_hunt_count=flea_hunt_count,
        pollip_heart_count=pollip_heart_count,
        spelling_bee_item_names=(
            world.get_spelling_bee_required_item_names()
        ),
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
        native_abstract_regions=True,
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
        silk_and_soul_points=get_silk_and_soul_points(world.options),
        silk_heart_logic=bool(world.options.silk_heart_logic.value),
    )
    world._silksong_rule_builder_rules["Goal"] = goal_rule
    world.set_rule(
        goal,
        goal_rule,
    )
    goal.place_locked_item(world.create_event("Victory"))
    completion_rule = Has("Victory")
    world._silksong_rule_builder_rules["Completion"] = completion_rule
    world.set_completion_rule(completion_rule)

from typing import Any, cast, override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from Options import CommonOptions, Option
from rule_builder import rules
from rule_builder.options import OPERATORS, REVERSE_OPERATORS, Operator

from .glitched_rules import LogicState, evaluate_rule, get_indentation, get_logic_color, get_out_of_logic_suffix

from ..bases import RabiRibiWorldBase
from ..constants import GAME_NAME
from ..items import item_groups, recruit_table, recruit_table_irisu
from ..names import ItemName
from ..options import *


@dataclass()
class KnowledgeRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player has an knowledge level set or if the rule should be evaluated when out of logic."""
    value: int

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        if world.options.knowledge >= self.value:
            return rules.True_().resolve(world)

        if getattr(world.multiworld, "generation_is_fake", False):
            return self.Resolved(
                self.value,
                player=world.player,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

        return rules.False_().resolve(world)

    class Resolved(rules.Rule.Resolved):
        value: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(ItemName.glitched_logic, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            deps.setdefault(ItemName.glitched_logic, set()).add(id(self))
            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            name = Knowledge.get_option_name(self.value)
            indent = get_indentation(depth)
            verb = "Has" if result != LogicState.CannotReach else "Lacks"
            color = get_logic_color(result)
            return [
                {"type": "text", "text": f"{indent}{verb} "},
                {"type": "color", "color": color, "text": name},
                {"type": "text", "text": f" knowledge"},
                *get_out_of_logic_suffix(result)
            ]

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            name = Knowledge.get_option_name(self.value)
            messages: list[JSONMessagePart] = [
                {"type": "color", "color": "yellow", "text": name},
            ]
            return messages


@dataclass()
class TrickDifficultyRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player has an trick difficulty set or if the rule should be evaluated when out of logic."""
    value: int

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        if world.options.trick_difficulty >= self.value:
            return rules.True_().resolve(world)

        if getattr(world.multiworld, "generation_is_fake", False):
            return self.Resolved(
                self.value,
                player=world.player,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

        return rules.False_().resolve(world)

    class Resolved(rules.Rule.Resolved):
        value: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(ItemName.glitched_logic, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            deps.setdefault(ItemName.glitched_logic, set()).add(id(self))
            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            name = TrickDifficulty.get_option_name(self.value)
            indent = get_indentation(depth)
            verb = "Can do" if result != LogicState.CannotReach else "Cannot do"
            color = get_logic_color(result)
            return [
                {"type": "text", "text": f"{indent}{verb} "},
                {"type": "color", "color": color, "text": name},
                {"type": "text", "text": f" tricks"},
                *get_out_of_logic_suffix(result)
            ]

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            name = TrickDifficulty.get_option_name(self.value)
            messages: list[JSONMessagePart] = [
                {"type": "color", "color": "yellow", "text": name},
            ]
            return messages


@dataclass()
class OutOfLogicOptionRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player has an option set or if the rule should be evaluated when out of logic."""
    name: str
    option: type[Option[Any]]
    value: Any
    operator: Operator = "eq"

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        if self.check(world.options):
            return rules.True_().resolve(world)

        if getattr(world.multiworld, "generation_is_fake", False):
            return self.Resolved(
                self.name,
                player=world.player,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )

        return rules.False_().resolve(world)

    def check(self, options: CommonOptions) -> bool:
        """Tests the given options dataclass to see if it passes this option filter"""
        option_name = next(
            (name for name, cls in options.__class__.type_hints.items()
             if cls is self.option),
            None,
        )
        if option_name is None:
            raise ValueError(
                f"Cannot find option {self.option.__name__} in options class {options.__class__.__name__}")
        opt = cast(Option[Any] | None, getattr(options, option_name, None))
        if opt is None:
            raise ValueError(f"Invalid option: {option_name}")

        fn = OPERATORS[self.operator]
        return fn(self.value, opt) if self.operator in REVERSE_OPERATORS else fn(opt, self.value)

    class Resolved(rules.Rule.Resolved):
        name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(ItemName.glitched_logic, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            deps.setdefault(ItemName.glitched_logic, set()).add(id(self))
            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            indent = get_indentation(depth)
            verb = "Can" if result != LogicState.CannotReach else "Cannot"
            color = get_logic_color(result)
            return [
                {"type": "text", "text": f"{indent}{verb} "},
                {"type": "color", "color": color, "text": self.name},
                *get_out_of_logic_suffix(result)
            ]

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = [
                {"type": "color", "color": "yellow", "text": self.name},
            ]
            return messages


@dataclass
class MagicTypesRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player can use enough magic types."""
    num_magic_types: int

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        return self.Resolved(
            self.num_magic_types,
            bool(world.options.rainbow_shot_in_logic.value),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(rules.Rule.Resolved):
        num_magic_types: int
        rainbow_shot_in_logic_enabled: bool

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            curr_magic_types = self._count_magic_types(state)
            return curr_magic_types >= self.num_magic_types

        def _count_magic_types(self, state: CollectionState) -> int:
            # Add 1 for default Ribbon magic
            curr_magic_types = state.count_group_unique("Magic", self.player) + 1
            if self._rainbow_shot_in_logic(state):
                curr_magic_types += 1
            return curr_magic_types

        def _rainbow_shot_in_logic(self, state: CollectionState) -> bool:
            """Player has Rainbow Shot and it's not out of logic by options"""
            return (
                (
                    self.rainbow_shot_in_logic_enabled
                    or state.has(ItemName.glitched_logic, self.player)
                )
                and state.has(ItemName.easter_egg, self.player, count=5)
            )

        def _rainbow_shot_out_of_logic(self, state: CollectionState) -> bool:
            return (
                not self.rainbow_shot_in_logic_enabled
                and state.has(ItemName.glitched_logic, self.player)
                and state.has(ItemName.easter_egg, self.player, count=5)
            )

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            for recruit in recruit_table:
                deps.setdefault(recruit, set()).add(id(self))
            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            indent = get_indentation(depth)
            messages: list[JSONMessagePart] = []
            if result == LogicState.Explain:
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {"type": "color", "color": "cyan",
                        "text": str(self.num_magic_types)},
                    {"type": "text", "text": " Magic Types"},
                ]
            else:
                assert state is not None
                assert glitched_state is not None
                curr_magic_types = self._count_magic_types(state)
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {
                        "type": "color",
                        "color": get_logic_color(result),
                        "text": f"{curr_magic_types}/{self.num_magic_types}",
                    },
                    {"type": "text", "text": " Magic Types"},
                    *get_out_of_logic_suffix(result)
                ]
            return messages

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan",
                        "text": str(self.num_magic_types)},
                    {"type": "text", "text": " Magic Types"},
                ]
            else:
                curr_magic_types = self._count_magic_types(state)
                color = (
                    "green" if curr_magic_types > self.num_magic_types
                    else "yellow" if curr_magic_types == self.num_magic_types and self._rainbow_shot_out_of_logic(state)
                    else "salmon"
                )
                messages = [
                    {"type": "text", "text": "Has "},
                    {
                        "type": "color",
                        "color": color,
                        "text": f"{curr_magic_types}/{self.num_magic_types}",
                    },
                    {"type": "text", "text": " Magic Types"},
                ]
            return messages


@dataclass
class TownMemberCountRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player can reach enough town members for an event."""
    num_town_members: int

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        return self.Resolved(
            self.num_town_members,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(rules.Rule.Resolved):
        num_town_members: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has_from_list_unique(recruit_table, self.player, self.num_town_members)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            for recruit in recruit_table:
                deps.setdefault(recruit, set()).add(id(self))
            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            indent = get_indentation(depth)
            messages: list[JSONMessagePart] = []
            if result == LogicState.Explain:
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {"type": "color", "color": "cyan",
                        "text": str(self.num_town_members)},
                    {"type": "text", "text": " Town Members"},
                ]
            else:
                assert state is not None
                assert glitched_state is not None
                if result == LogicState.OutOfLogic:
                    curr_town_members = glitched_state.count_from_list_unique(
                        recruit_table, self.player)
                else:
                    curr_town_members = state.count_from_list_unique(
                        recruit_table, self.player)
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {
                        "type": "color",
                        "color": get_logic_color(result),
                        "text": f"{curr_town_members}/{self.num_town_members}",
                    },
                    {"type": "text", "text": " Town Members"},
                    *get_out_of_logic_suffix(result)
                ]
            return messages

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan",
                        "text": str(self.num_town_members)},
                    {"type": "text", "text": " Town Members"},
                ]
            else:
                curr_town_members = state.count_from_list_unique(
                    recruit_table, self.player)
                color = "green" if curr_town_members >= self.num_town_members else "salmon"
                messages = [
                    {"type": "text", "text": "Has "},
                    {
                        "type": "color",
                        "color": color,
                        "text": f"{curr_town_members}/{self.num_town_members}",
                    },
                    {"type": "text", "text": " Town Members"},
                ]
            return messages


@dataclass
class TownMemberCountIrisuRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player can reach enough town members to fight Irisu."""
    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        return self.Resolved(
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(rules.Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has_from_list_unique(recruit_table_irisu, self.player, 15)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            for recruit in recruit_table_irisu:
                deps.setdefault(recruit, set()).add(id(self))
            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            indent = get_indentation(depth)
            messages: list[JSONMessagePart] = []
            if result == LogicState.Explain:
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {"type": "color", "color": "cyan", "text": "15"},
                    {"type": "text", "text": " Main Game Town Members"},
                ]
            else:
                assert state is not None
                assert glitched_state is not None
                if result == LogicState.OutOfLogic:
                    curr_town_members = glitched_state.count_from_list_unique(
                        recruit_table, self.player)
                else:
                    curr_town_members = state.count_from_list_unique(
                        recruit_table, self.player)
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {
                        "type": "color",
                        "color": get_logic_color(result),
                        "text": f"{curr_town_members}/15",
                    },
                    {"type": "text", "text": " Main Game Town Members"},
                    *get_out_of_logic_suffix(result)
                ]
            return messages

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": "15"},
                    {"type": "text", "text": " Main Game Town Members"},
                ]
            else:
                curr_town_members = state.count_from_list_unique(
                    recruit_table_irisu, self.player)
                color = "green" if curr_town_members >= 15 else "salmon"
                messages = [
                    {"type": "text", "text": "Has "},
                    {
                        "type": "color",
                        "color": color,
                        "text": f"{curr_town_members}/{15}",
                    },
                    {"type": "text", "text": " Main Game Town Members"},
                ]
            return messages


@dataclass()
class HasEnoughAmuletFoodRule(rules.Rule[RabiRibiWorldBase], game=GAME_NAME):
    """Rule to check if the player can utilize enough items to perform a trick."""
    num_amulet_food: int

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        has_advanced_knowledge = world.options.knowledge.value >= Knowledge.option_advanced
        rainbow_shot_in_logic_enabled = bool(
            world.options.rainbow_shot_in_logic.value)
        return self.Resolved(
            self.num_amulet_food,
            has_advanced_knowledge,
            rainbow_shot_in_logic_enabled,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(rules.Rule.Resolved):
        num_amulet_food: int
        has_advanced_knowledge: bool
        rainbow_shot_in_logic_enabled: bool

        def _count_amulet_food(self, state):
            amulet = self._count_amulet_charges(state)
            food = 0

            if self._has_item_menu(state):
                if state.has(ItemName.rumi_donut, self.player) or state.has("Shop Reachable", self.player):
                    food = 1
                    # Eating a Rumi Donut gives an amulet charge
                    if self._can_bunny_amulet(state):
                        amulet += 1
                    food += self._count_normal_consumable_items(state)
                    # Kotri's buff can save enough amulet charge for an additional amulet use
                    if amulet >= 4 and state.has(ItemName.kotri_recruit, self.player) and \
                            state.has_from_list_unique(recruit_table, self.player, 3):
                        amulet += 1
            return (amulet + food)

        def _count_amulet_charges(self, state: CollectionState) -> int:
            """Counts the number of amulet charges the player has"""
            if state.has(ItemName.bunny_amulet, self.player) or state.has("Chapter 2", self.player):
                if state.has(ItemName.rumi_recruit, self.player):
                    return 4
                if state.has("Shop Reachable", self.player) or state.has("Chapter 4", self.player):
                    return 3
                if state.has("Chapter 3", self.player):
                    return 2
                return 1
            return 0

        def _count_normal_consumable_items(self, state: CollectionState) -> int:
            """Counts which normal consumable items the player can reach, either from locations or purchases."""
            consumables = 0
            if state.has(ItemName.rumi_cake, self.player) or state.has("Shop Reachable", self.player):
                consumables += 1
            if state.has(ItemName.cocoa_bomb, self.player) or self._can_purchase_cocoa_bomb(state):
                consumables += 1
            if state.has(ItemName.gold_carrot, self.player):
                consumables += 1
            return consumables

        def _can_purchase_cocoa_bomb(self, state: CollectionState) -> bool:
            """Player can purchase cocoa bomb"""
            return state.has("Chapter 1", self.player) and \
                state.has(ItemName.cocoa_recruit, self.player) and \
                state.has_from_list_unique(recruit_table, self.player, 3)

        def _can_bunny_amulet(self, state: CollectionState) -> bool:
            """Player can use the bunny amulet"""
            return state.has(ItemName.rumi_cake, self.player) or state.has("Shop Reachable", self.player)

        def _has_item_menu(self, state: CollectionState) -> bool:
            """Player has access to the item menu"""
            return state.has("Chapter 1", self.player) or \
                (self._is_at_least_advanced_knowledge(
                    state) and self._has_3_magic_types(state))

        def _has_3_magic_types(self, state: CollectionState) -> bool:
            """Player has at least 3 types of magic"""
            # If playing with more than 5 Easter Eggs, Rainbow Shot could be used as a magic type
            return state.has_group_unique("Magic", self.player, 2) or \
                (self._rainbow_shot_in_logic(state)
                 and state.has_group_unique("Magic", self.player, 1))

        def _is_at_least_advanced_knowledge(self, state: CollectionState) -> bool:
            """Knowledge is at least advanced"""
            return self.has_advanced_knowledge or state.has(ItemName.glitched_logic, self.player)

        def _rainbow_shot_in_logic(self, state: CollectionState) -> bool:
            """Player has Rainbow Shot and it's not out of logic by options"""
            return (self.rainbow_shot_in_logic_enabled or state.has(ItemName.glitched_logic, self.player)) and \
                state.has(ItemName.easter_egg, self.player, count=5)

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            curr_amulet_food = self._count_amulet_food(state)
            return curr_amulet_food >= self.num_amulet_food

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            deps = super().item_dependencies()
            deps.setdefault(ItemName.bunny_amulet, set()).add(id(self))
            deps.setdefault(ItemName.easter_egg, set()).add(id(self))
            deps.setdefault(ItemName.glitched_logic, set()).add(id(self))

            deps.setdefault("Chapter 1", set()).add(id(self))
            deps.setdefault("Chapter 2", set()).add(id(self))
            deps.setdefault("Chapter 3", set()).add(id(self))
            deps.setdefault("Chapter 4", set()).add(id(self))
            deps.setdefault("Shop Reachable", set()).add(id(self))

            for consumable in item_groups["Consumables"]:
                deps.setdefault(consumable, set()).add(id(self))
            for recruit in recruit_table:
                deps.setdefault(recruit, set()).add(id(self))
            for magic in item_groups["Magic"]:
                deps.setdefault(magic, set()).add(id(self))

            return deps

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            indent = get_indentation(depth)
            messages: list[JSONMessagePart] = []
            if result == LogicState.Explain:
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {"type": "color", "color": "cyan",
                        "text": str(self.num_amulet_food)},
                    {"type": "text", "text": " Amulet/Food"},
                ]
            else:
                assert state is not None
                assert glitched_state is not None
                if result == LogicState.OutOfLogic:
                    curr_amulet_food = self._count_amulet_food(glitched_state)
                else:
                    curr_amulet_food = self._count_amulet_food(state)
                messages = [
                    {"type": "text", "text": f"{indent}Has "},
                    {
                        "type": "color",
                        "color": get_logic_color(result),
                        "text": f"{curr_amulet_food}/{self.num_amulet_food}",
                    },
                    {"type": "text", "text": " Amulet/Food"},
                    *get_out_of_logic_suffix(result)
                ]
            return messages

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            messages: list[JSONMessagePart] = []
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan",
                        "text": str(self.num_amulet_food)},
                    {"type": "text", "text": " Amulet/Food"},
                ]
            else:
                curr_amulet_food = self._count_amulet_food(state)
                color = "green" if self(state) else "salmon"
                messages = [
                    {"type": "text", "text": "Has "},
                    {
                        "type": "color",
                        "color": color,
                        "text": f"{curr_amulet_food}/{self.num_amulet_food}",
                    },
                    {"type": "text", "text": " Amulet/Food"},
                ]
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = ""
            if state is not None:
                suffix = " ✓" if self(state) else " ✕"
            return f"Has {self.num_amulet_food} Amulet/Food{suffix}"

        @override
        def __str__(self) -> str:
            return f"Has {self.num_amulet_food} Amulet/Food"


def from_option(option: type[Option], value: Any, operator: Operator = "eq") -> rules.Rule[RabiRibiWorldBase]:
    return rules.True_(options=[rules.OptionFilter(option, value, operator)])


@dataclass()
class Macro(rules.WrapperRule[RabiRibiWorldBase], game=GAME_NAME):
    name: str
    description: str = ""
    verb_true: str = "Can"
    verb_false: str = "Cannot"

    @override
    def _instantiate(self, world: RabiRibiWorldBase) -> rules.Rule.Resolved:
        if rule := world.rule_macros.get(self.name):
            return rule
        rule = self.Resolved(
            self.child.resolve(world),
            self.name,
            self.description,
            self.verb_true,
            self.verb_false,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )
        world.rule_macros[self.name] = rule
        return rule

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(rules.WrapperRule.Resolved):
        name: str
        description: str
        verb_true: str
        verb_false: str

        def explain_rule_glitched(self, state: CollectionState | None, glitched_state: CollectionState | None, depth: int) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, glitched_state)
            indent = get_indentation(depth)
            verb = self.verb_false if result == LogicState.CannotReach else self.verb_true
            color = get_logic_color(result)
            return [
                {"type": "text", "text": f"{indent}{verb} "},
                {"type": "color", "color": color, "text": str(self)},
                *get_out_of_logic_suffix(result)
            ]

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            result = evaluate_rule(self, state, None)
            verb = self.verb_false if result == LogicState.CannotReach else self.verb_true
            color = get_logic_color(result)
            return [
                {"type": "text", "text": f"{verb} "},
                {"type": "color", "color": color, "text": str(self)},
                *get_out_of_logic_suffix(result)
            ]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            result = evaluate_rule(self, state, None)
            suffix = " ✕" if result == LogicState.CannotReach else " ✓"
            return f"{self.name}{suffix}"

        @override
        def __str__(self) -> str:
            return self.name

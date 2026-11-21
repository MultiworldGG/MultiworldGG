import dataclasses
from typing import TYPE_CHECKING, Protocol, TypeVar

from rule_builder.rules import Or, Rule, Has, And
from rule_builder.field_resolvers import FieldResolver

from .rules import (
    InLevelRule,
    HasAbility,
    HasAbilityCombination,
    HasAnyAbilities,
    HasAllAbilities,
    HasAbilityExceptCharacters,
    HasSingleJumpDistance,
)
from .rule_replacement import (
    RuleReplacer,
    Difficulty,
    NestedOptimizerRuleReplacer,
    NestedAndInLevelRuleSimplifierRuleReplacer,
)
from ..extras import Extra
from ...character_ability import CharacterAbility
from ...data.items.character_items import NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA


if TYPE_CHECKING:
    from .types import LogicArea
else:
    LogicArea = object


@dataclasses.dataclass
class RuleData(Protocol):
    @property
    def rule(self) -> Rule:
        return ...

    @property
    def er_rule(self) -> Rule | None:
        return ...


TRuleData = TypeVar("TRuleData", bound=RuleData)


@dataclasses.dataclass
class ExtraTogglePrepare:
    rule: Rule
    """The rule that can alternatively be met if the player has Extra Toggle."""
    extra_and_rule: Rule | None = None
    """An additional rule that must be satisfied for the playing having Extra Toggle to satisfy `self.rule`."""

    def make_replacement_rule(self, new_rule_first: bool = False) -> Rule:
        return ExtraToggleRuleReplacer.or_extra_toggle(self.rule, self.extra_and_rule, new_rule_first)


PRE_RULE_OPTIMIZER = NestedOptimizerRuleReplacer()


class ExtraToggleRuleReplacer(RuleReplacer):
    logic_area: LogicArea
    extra_toggle_abilities_union: CharacterAbility
    extra_toggle_abilities_unique_combinations: set[CharacterAbility]
    extra_toggle_name_to_abilities: dict[str, CharacterAbility]
    adding_extra_toggle_rules: bool = False
    shared_replacer: NestedAndInLevelRuleSimplifierRuleReplacer

    def __init__(self, logic_area: LogicArea, shared_replacer: NestedAndInLevelRuleSimplifierRuleReplacer):
        super().__init__()
        extra_toggle_abilities_union = CharacterAbility.NONE
        extra_toggle_abilities_unique_combinations: set[CharacterAbility] = set()
        extra_toggle_name_to_abilities: dict[str, CharacterAbility] = {}
        extra_toggle_characters = logic_area.area.get_extra_toggle_characters()
        if extra_toggle_characters:
            for character in extra_toggle_characters:
                character_data = NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA[character]
                extra_toggle_abilities_union |= character_data.abilities
                extra_toggle_abilities_unique_combinations.add(character_data.abilities)
                extra_toggle_name_to_abilities[character_data.name] = character_data.abilities
        self.extra_toggle_abilities_union = extra_toggle_abilities_union
        self.extra_toggle_abilities_unique_combinations = extra_toggle_abilities_unique_combinations
        self.extra_toggle_name_to_abilities = extra_toggle_name_to_abilities
        self.logic_area = logic_area
        self.shared_replacer = shared_replacer

    def start_replace(self, rule: Rule, difficulty: Difficulty) -> Rule:
        if difficulty == "base":
            return self.shared_replacer.start_replace(rule, difficulty)
        else:
            # Un-nest rules so that an Or(Or(Or(...), ...), ...) collapses into a single Or()
            base = PRE_RULE_OPTIMIZER.start_replace(rule, difficulty)
            # Apply Extra Toggle rules, the previous un-nesting is important so that if a single rule within the Or()
            # can be satisfied with Extra Toggle, the Extra Toggle rule can be added as a new child of the Or() instead
            # of applying to each child that can be satisfied with Extra Toggle.
            extra_toggle_applied = super().start_replace(base, difficulty)
            # Simplify rules that had to be kept in more complex forms to determine if Extra Toggle can satisfy them,
            # and then un-nest again, since the simpler forms often use Or or And rules.
            return self.shared_replacer.start_replace(extra_toggle_applied, difficulty)

    @staticmethod
    def or_extra_toggle(rule: Rule, extra_and_rule: Rule | None = None, new_rule_first: bool = False) -> Rule:
        if extra_and_rule is None:
            if new_rule_first:
                return Extra.EXTRA_TOGGLE.has() | rule
            else:
                return rule | Extra.EXTRA_TOGGLE.has()
        else:
            if new_rule_first:
                return (extra_and_rule & Extra.EXTRA_TOGGLE.has()) | rule
            else:
                return rule | (extra_and_rule & Extra.EXTRA_TOGGLE.has())

    def _handle(self, rule: Rule) -> Rule:
        # Base logic rules never consider Extras.
        if self.current_difficulty_path == "base" or not isinstance(rule, InLevelRule):
            return super()._handle(rule)

        result = super()._handle(rule)
        if isinstance(result, InLevelRule):
            added = self._add_extra_toggle(result)
            if added is not result:
                self.current_found_difficulty = self.current_difficulty_path
                return added
        return result

    def _add_extra_toggle(self, rule: InLevelRule) -> Rule:
        prepare = self._add_extra_toggle_prepare(rule)
        if prepare is None:
            return rule
        return prepare.make_replacement_rule()

    def _add_extra_toggle_prepare(self, rule: InLevelRule) -> ExtraTogglePrepare | None:
        if isinstance(rule, HasAbility):
            if isinstance(rule.ability, CharacterAbility):
                if rule.ability in self.extra_toggle_abilities_union:
                    return ExtraTogglePrepare(rule)
                else:
                    return None
            else:
                raise Exception("FieldResolver support is not implemented.")

        if isinstance(rule, HasAnyAbilities):
            if isinstance(rule.abilities, CharacterAbility):
                if (rule.abilities & self.extra_toggle_abilities_union) != 0:
                    # There is an Extra Toggle character that provides one of the abilities.
                    return ExtraTogglePrepare(rule)
                else:
                    return None
            else:
                raise Exception("FieldResolver support is not implemented.")

        if isinstance(rule, HasAllAbilities):
            if isinstance(rule.abilities, CharacterAbility):
                if rule.abilities in self.extra_toggle_abilities_union:
                    # There is an Extra Toggle character that provides all the abilities.
                    return ExtraTogglePrepare(rule)
                elif (rule.abilities & self.extra_toggle_abilities_union) != 0:
                    # There is an Extra Toggle character that provides *some* of the abilities.
                    # Find the abilities that are not provided by Extra Toggle characters, but still need to be
                    # provided for the rule to return True.
                    missing_abilities = rule.abilities & ~self.extra_toggle_abilities_union
                    return ExtraTogglePrepare(rule, HasAllAbilities(missing_abilities))
                else:
                    return None
            else:
                raise Exception("FieldResolver support is not implemented.")

        if isinstance(rule, HasAbilityCombination):
            if isinstance(rule.ability_combinations, tuple):
                for combination in rule.ability_combinations:
                    if any(combination in extra_toggle_combination for extra_toggle_combination in
                           self.extra_toggle_abilities_unique_combinations):
                        # There is an Extra Toggle character that provides one of the ability combinations the rule
                        # is checking for.
                        return ExtraTogglePrepare(rule)
                else:
                    return None
            else:
                raise Exception("FieldResolver support is not implemented.")

        if isinstance(rule, HasAbilityExceptCharacters):
            if isinstance(rule.ability, CharacterAbility) and not isinstance(rule.except_characters, FieldResolver):
                for extra_toggle_character, character_abilities in self.extra_toggle_name_to_abilities.items():
                    if (
                            (rule.ability is CharacterAbility.NONE or rule.ability in character_abilities)
                            and extra_toggle_character not in rule.except_characters
                    ):
                        # There is a character with the required ability that is not excluded.
                        return ExtraTogglePrepare(rule)
                else:
                    # No break, so no extra toggle character could satisfy the rule.
                    return None
            else:
                raise Exception("FieldResolver support is not implemented.")

        if isinstance(rule, HasSingleJumpDistance):
            if (CharacterAbility.HOVER | CharacterAbility.CAN_DOUBLE_JUMP) & self.extra_toggle_abilities_union != 0:
                # A character that can hover or double jump can jump further than the best single-jump distance.
                return ExtraTogglePrepare(rule)
            else:
                required_distance = rule.distance
                for character in self.logic_area.area.get_extra_toggle_characters():
                    character_data = NON_VEHICLE_EXTRA_CHARACTER_TO_ITEM_DATA[character]
                    if character_data.single_jump_distance >= required_distance:
                        # Found a character that can jump the required distance.
                        return ExtraTogglePrepare(rule)
                else:
                    # No extra toggle character was found that could satisfy the rule.
                    return None

        raise ValueError(f"Unexpected InLevelRule {rule}")

    def add_extra_toggle_rules(self, rule_data: TRuleData) -> TRuleData:
        assert dataclasses.is_dataclass(rule_data)
        rule = self.replace_top_level_rule(rule_data.rule)
        er_rule = None if rule_data.er_rule is None else self.replace_top_level_rule(rule_data.er_rule)
        if rule is not rule_data.rule or er_rule is not rule_data.er_rule:
            return dataclasses.replace(rule_data, rule=rule, er_rule=er_rule)
        else:
            return rule_data

    def _handle_or(self, rule: Or) -> Rule:
        """Scan for any rule within the Or that would get `| Has("Extra toggle")` applied, and instead add
        `Has("Extra Toggle")` as a new child within the Or."""
        other_rules: list[Rule] = []
        partial_rules: list[ExtraTogglePrepare] = []
        for child in rule.children:
            if isinstance(child, InLevelRule) and (prepare := self._add_extra_toggle_prepare(child)) is not None:
                if prepare.extra_and_rule is None:
                    # This child can alternatively be satisfied by having "Extra Toggle", so the entire `Or` can
                    # alternatively be satisfied by having "Extra Toggle".
                    return Or(*rule.children, Has(Extra.EXTRA_TOGGLE.readable_name),
                              options=rule.options, filtered_resolution=rule.filtered_resolution)
                else:
                    # This child is partially satisfied by having "Extra Toggle", so some reduced version of this child,
                    # in addition to having "Extra Toggle", would be an alternative to satisfy this child.
                    partial_rules.append(prepare)
        if partial_rules:
            # Combine the partial rules together as
            #  Or(
            #     super()._handle_or(Or(*rule.children)),
            #     And(
            #         Has("Extra Toggle"),
            #         Or(*partial_reduced_rules),  # Any one of these satisfies the original rule with Extra Toggle.
            #     )
            #  )
            partial_and_rule = And(
                Has(Extra.EXTRA_TOGGLE.readable_name),
                Or(*[partial.extra_and_rule for partial in partial_rules]),
                options=rule.options,
                filtered_resolution=rule.filtered_resolution,
            )
            return super()._handle_or(rule) | partial_and_rule
        else:
            return super()._handle_or(rule)


    def _handle_and(self, rule: And) -> Rule:
        """
        Find rules within the And that would get `| Has("Extra toggle")` applied, and instead replace the child rules
        with `Has("Extra Toggle") | And(*child_rules)` as a new child within the And.

        For rules that are only partiall satisfied by having Extra Toggle, those rules are replaced by a single child of
        `And(*original_rules) | And(Has("Extra Toggle"), *reduced_original_rules)`
        """
        children_that_can_or_extra_toggle: list[Rule] = []
        children_that_can_partial_or_extra_toggle: list[ExtraTogglePrepare] = []
        other_children: list[Rule] = []
        for child in rule.children:
            if isinstance(child, InLevelRule) and (prepare := self._add_extra_toggle_prepare(child)) is not None:
                if prepare.extra_and_rule is None:
                    children_that_can_or_extra_toggle.append(child)
                else:
                    children_that_can_partial_or_extra_toggle.append(prepare)
            else:
                other_children.append(child)

        if len(other_children) == len(rule.children):
            return super()._handle_and(rule)

        base_rule = And(*other_children, options=rule.options, filtered_resolution=rule.filtered_resolution)
        base_rule = super()._handle_and(base_rule)

        new_children: list[Rule] = []

        if children_that_can_or_extra_toggle:
            if len(children_that_can_or_extra_toggle) == 1:
                children_that_can_or_extra_toggle_rule = children_that_can_or_extra_toggle[0]
            else:
                children_that_can_or_extra_toggle_rule = And(*children_that_can_or_extra_toggle)
            new_children.append(ExtraTogglePrepare(children_that_can_or_extra_toggle_rule).make_replacement_rule())

        if children_that_can_partial_or_extra_toggle:
            if len(children_that_can_partial_or_extra_toggle) == 1:
                partial_rule = children_that_can_partial_or_extra_toggle[0].make_replacement_rule()
            else:
                original_rules = [prepare.rule for prepare in children_that_can_partial_or_extra_toggle]
                alt_rules = [prepare.extra_and_rule for prepare in children_that_can_partial_or_extra_toggle]
                partial_rule = And(*original_rules) | And(Has(Extra.EXTRA_TOGGLE.readable_name), *alt_rules)
            new_children.append(partial_rule)

        return base_rule & And(*new_children, options=rule.options, filtered_resolution=rule.filtered_resolution)
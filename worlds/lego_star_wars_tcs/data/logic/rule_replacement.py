import dataclasses
from typing import Literal, TypeVar, Protocol, Sequence

from rule_builder.field_resolvers import FieldResolver
from rule_builder.rules import Rule, And, Or, WrapperRule, Filtered, False_, True_

from .option_filters import LogicOptions, UTGlitchesRule
from .rules import HasAbility, HasAnyAbilities, HasAllAbilities, InLevelRule
from ...character_ability import CharacterAbility, IMPLIED_ABILITIES, IMPLIED_BY_ABILITIES

Difficulty = Literal["base", "normal", "moderate", "hard"]


class RuleData(Protocol):
    @property
    def rule(self) -> Rule:
        return ...

    @property
    def er_rule(self) -> Rule | None:
        return ...


TRuleData = TypeVar("TRuleData", bound=RuleData)


def rule_children_are_the_same(rule1_children: Sequence[Rule], rule2_children: Sequence[Rule]):
    if len(rule1_children) != len(rule2_children):
        return False
    # First check that the type of each rule is the same, this is a fairly fast check.
    for rule1_child, rule2_child in zip(rule1_children, rule2_children):
        # The type check eliminates cases where a complex rule's .to_dict() reduces itself to a simpler rule and calls
        # .to_dict() on that simpler rule.
        if type(rule1_child) is not type(rule2_child):
            return False
    # Now check that the rules are the same by comparing their .to_dict(). This is much slower than the type check, so
    # is in its own loop.
    for rule1_child, rule2_child in zip(rule1_children, rule2_children):
        if rule1_child.to_dict() != rule2_child.to_dict():
            return False
    return True


class RuleReplacer:
    current_difficulty_path: Difficulty
    current_found_difficulty: Difficulty | None = None
    replaced_rules_memodict: dict[tuple[int, Difficulty | None], tuple[Rule, Rule]]

    def __init__(self, dispatch_overrides: dict | None = None) -> None:
        self._handlers = {
            Filtered: self._handle_filtered,
            WrapperRule: self._handle_wrapper_rule,
            LogicOptions: self._handle_logic_options,
            UTGlitchesRule: self._handle_ut_glitches_rule,
            Or: self._handle_or,
            And: self._handle_and,
        }
        if dispatch_overrides:
            self._handlers |= dispatch_overrides
        self.replaced_rules_memodict = {}

    def purge_memodict(self):
        """Clear the contents of the memodict. This allows the contents of the memodict to be garbage collected if the
        replacer is a module-level global."""
        self.replaced_rules_memodict.clear()

    def replace_each_difficulty(
            self,
            base: Rule,
            normal: Rule,
            moderate: Rule,
            hard: Rule,
    ) -> Rule | None:
        # If any of base/normal/moderate/hard contain a LogicOptions rule, replace that with the
        # base/normal/moderate/hard rule.
        base_rule = self.start_replace(base, "base")
        normal_rule = self.start_replace(normal, "normal")
        moderate_rule = self.start_replace(moderate, "moderate")
        hard_rule = self.start_replace(hard, "hard")

        assert isinstance(base_rule, Rule)
        if hard_rule is moderate_rule and hard_rule is normal_rule and hard_rule is base_rule:
            # All the rules are the same.
            return base_rule
        else:
            assert isinstance(normal_rule, Rule)
            assert isinstance(moderate_rule, Rule)
            assert isinstance(hard_rule, Rule)

            if base_rule is base and normal_rule is normal and moderate_rule is moderate and hard_rule is hard:
                # No changes.
                return None

            return LogicOptions(base_rule, normal_rule, moderate_rule, hard_rule)

    def replace_top_level_rule(self, rule: Rule) -> Rule:
        if isinstance(rule, LogicOptions):
            un_nested = self.replace_each_difficulty(
                base=rule.base,
                normal=rule.normal,
                moderate=rule.moderate,
                hard=rule.hard,
            )
        else:
            un_nested = self.replace_each_difficulty(
                base=rule,
                normal=rule,
                moderate=rule,
                hard=rule,
            )
        if un_nested is not None:
            return un_nested
        else:
            return rule

    def replace_rule_data(self, rule_data: TRuleData) -> TRuleData:
        rule = self.replace_top_level_rule(rule_data.rule)
        er_rule = None if rule_data.er_rule is None else self.replace_top_level_rule(rule_data.er_rule)
        if rule is not rule_data.rule or er_rule is not rule_data.er_rule:
            return dataclasses.replace(rule_data, rule=rule, er_rule=er_rule)
        else:
            return rule_data

    def start_replace(self, rule: Rule, difficulty: Difficulty) -> Rule:
        if self.current_found_difficulty is not None:
            raise Exception("Error: Replacement is already ongoing.")
        try:
            self.current_difficulty_path = difficulty
            replaced = self.replace(rule)
        finally:
            self.current_found_difficulty = None
        return replaced


    def replace(self, rule: Rule) -> Rule:
        key = (id(rule), self.current_difficulty_path)
        already_handled = self.replaced_rules_memodict.get(key)
        if already_handled is not None:
            return already_handled[0]
        to_return = self._handle(rule)
        # Need to store the rule to prevent garbage collection.
        self.replaced_rules_memodict[key] = to_return, rule
        return to_return

    def _handle(self, rule: Rule) -> Rule:
        rule_class = type(rule)
        if rule_class in self._handlers:
            return self._handlers[rule_class](rule)
        else:
            return rule

    def _handle_wrapper_rule_subclass(self, rule: WrapperRule) -> WrapperRule:
        replaced = self.replace(rule.child)
        if replaced is not rule.child:
            return dataclasses.replace(rule, child=replaced)
        else:
            return rule

    def _handle_filtered(self, rule: Filtered) -> Rule:
        return self._handle_wrapper_rule_subclass(rule)

    def _handle_wrapper_rule(self, rule: WrapperRule) -> Rule:
        return self._handle_wrapper_rule_subclass(rule)

    def _handle_ut_glitches_rule(self, rule: UTGlitchesRule) -> Rule:
        replaced = self.replace(rule.child)
        replaced_glitches = self.replace(rule.glitches)
        replaced_all_glitches = self.replace(rule.all_glitches)
        if (replaced is not rule.child
                or replaced_glitches is not rule.glitches
                or replaced_all_glitches is not rule.all_glitches):
            return dataclasses.replace(rule,
                                       child=replaced, glitches=replaced_glitches, all_glitches=replaced_all_glitches)
        else:
            return rule

    def _handle_logic_options(self, rule: LogicOptions) -> Rule:
        if rule.options:
            # OptionFilters would probably be annoying to combine correctly, especially if filtered_resolution
            # differs between the LogicOptions and the rule being getattr-ed.
            raise Exception("LogicOptions should not use OptionFilters, filter the individual rules instead.")
        # Mark that we are now processing difficulty-specific rules.
        self.current_found_difficulty = self.current_difficulty_path
        return self.replace(getattr(rule, self.current_difficulty_path))

    def _handle_or(self, rule: Or) -> Rule:
        if not rule.children:
            return False_()

        if len(rule.children) == 1:
            return self.replace(rule.children[0])

        changed = False
        new_children = []
        for child in rule.children:
            replaced = self.replace(child)
            if replaced is not child:
                changed = True
            new_children.append(replaced)

        if changed:
            if len(new_children) == 1:
                child = new_children[0]
                if child.options == rule.options and child.filtered_resolution == rule.filtered_resolution:
                    return child
                else:
                    return Filtered(child, options=rule.options, filtered_resolution=rule.filtered_resolution)
            return Or(*new_children, options=rule.options, filtered_resolution=rule.filtered_resolution)
        else:
            return rule

    def _handle_and(self, rule: And) -> Rule:
        if not rule.children:
            return True_()

        if len(rule.children) == 1:
            return self.replace(rule.children[0])

        changed = False
        new_children = []
        for child in rule.children:
            replaced = self.replace(child)
            if replaced is not child:
                changed = True
            new_children.append(replaced)

        if changed:
            if len(new_children) == 1:
                child = new_children[0]
                if child.options == rule.options and child.filtered_resolution == rule.filtered_resolution:
                    return child
                else:
                    return Filtered(child, options=rule.options, filtered_resolution=rule.filtered_resolution)
            return And(*new_children, options=rule.options, filtered_resolution=rule.filtered_resolution)
        else:
            return rule

class NestedOptimizerRuleReplacer(RuleReplacer):
    def _handle_or(self, rule: Or) -> Rule:
        if not rule.children:
            return False_()

        if len(rule.children) == 1:
            return self.replace(rule.children[0])

        changed = False
        initial_new_children = []
        for child in rule.children:
            replaced = self.replace(child)
            if replaced is not child:
                changed = True
            if isinstance(replaced, Or) and replaced.options == rule.options:
                initial_new_children.extend(replaced.children)
            else:
                initial_new_children.append(replaced)

        # todo: When extending this to also apply to nested rule, this will have some potential issues with how the
        #  memodict is used, because a rule could be handle differently depending on what nested rules we are within.
        # Some early basic ability rule combinations.
        final_new_children: list[Rule] = []
        any_abilities = CharacterAbility.NONE
        all_abilities_set: set[CharacterAbility] = set()
        for child in initial_new_children:
            if child.options == rule.options:
                if isinstance(child, HasAbility) and not isinstance(child.ability, FieldResolver):
                    any_abilities |= child.ability
                elif isinstance(child, HasAnyAbilities) and not isinstance(child.abilities, FieldResolver):
                    any_abilities |= child.abilities
                elif isinstance(child, HasAllAbilities) and not isinstance(child.abilities, FieldResolver):
                    all_abilities_set.add(child.abilities)
                else:
                    final_new_children.append(child)
            else:
                # todo: Abilities with .options set can be optimised based on the other abilities rules.
                final_new_children.append(child)
        any_abilities_simplified = any_abilities.simplify_or()
        if not changed and any_abilities_simplified is not any_abilities:
            changed = True
        if any_abilities_simplified is not CharacterAbility.NONE and all_abilities_set:
            # Any one of these abilities allows the Or rule to return True, so a HasAllAbilities containing any of these
            # abilities is pointless.
            delete_rule_if_found_in_all_abilities = any_abilities | any_abilities_simplified
            for ability in delete_rule_if_found_in_all_abilities:
                # Having an ability that implies any of these abilities would also allow the Or rule to return True, so
                # these abilities can be removed too.
                # Or(
                #    HasAbility(CAN_DOUBLE_JUMP),
                #    HasAllAbilities(JEDI | ASTROMECH_PANEL),
                # )
                # can be reduced to just HasAbility(CAN_DOUBLE_JUMP).
                # Merge in all abilities that are implied by `ability`. E.g. if CAN_DOUBLE_JUMP is one of the already
                # found abilities, then JEDI can also be removed because CAN_DOUBLE_JUMP is implied by JEDI.
                for implied_by_abilities in IMPLIED_BY_ABILITIES[ability]:
                    delete_rule_if_found_in_all_abilities |= implied_by_abilities

            pointless_removed_all_abilities_set = {
                all_abilities for all_abilities in all_abilities_set
                if (all_abilities & delete_rule_if_found_in_all_abilities) == 0
            }
            if not changed and pointless_removed_all_abilities_set != all_abilities_set:
                changed = True
            all_abilities_set = pointless_removed_all_abilities_set

        # Or(
        #    [...],
        #    HasAllAbilities(JEDI | ASTROMECH_PANEL),
        #    HasAllAbilities(JEDI | ASTROMECH_PANEL | BLASTER),
        # )
        # can be reduced to:
        # Or(
        #    [...],
        #    HasAllAbilities(JEDI | ASTROMECH_PANEL),
        # )
        # Sort largest bit counts to the top of the stack because these are most likely to contain all the abilities
        # of another HasAllAbilities rule, where that other rule would always be satisfied first.
        all_abilities_stack = sorted(all_abilities_set, key=CharacterAbility.bit_count)
        all_abilities_list = []
        while all_abilities_stack:
            abilities = all_abilities_stack.pop()
            # Iterate in reverse to get the abilities with smallest bits first, since those are most likely to be
            # contained within `abilities`.
            for other_ability in reversed(all_abilities_stack):
                if other_ability in abilities:
                    # `abilities` is pointless because it contains `other_ability`.
                    changed = True
                    break
            else:
                # No break, try the abilities in the list next.
                for other_ability in reversed(all_abilities_list):
                    if other_ability in abilities:
                        # `abilities` is pointless because it contains `other_ability`.
                        changed = True
                        break
                else:
                    # The ability/abilities are relevant.
                    all_abilities_list.append(abilities)

        # todo: Make sure the easiest to satisfy rules are put towards the front of the children.
        for all_abilities in all_abilities_list:
            if all_abilities.bit_count() == 1:
                # The HasAllAbilities has reduced to a HasAbility, which can be combined into a HasAnyAbilities.
                any_abilities_simplified |= all_abilities
            else:
                # Insert at the front.
                final_new_children.insert(0, HasAllAbilities(all_abilities))

        if any_abilities_simplified is not CharacterAbility.NONE:
            changed = True
            # Insert the new HasAnyAbilities at the front because it is a fast rule.
            if any_abilities_simplified.bit_count() == 1:
                new_has_any_abilities = HasAbility(any_abilities_simplified)
            else:
                new_has_any_abilities = HasAnyAbilities(any_abilities_simplified)
            final_new_children.insert(0, new_has_any_abilities)

        # There could be either zero or one 'any abilities rule' and/or either zero or one 'all abilities rule' that,
        # when processed, produces the same rules as before. In that case, the original rule can be returned instead,
        # reducing memory usage.
        if changed and rule_children_are_the_same(rule.children, final_new_children):
            changed = False

        if changed:
            if len(final_new_children) == 1:
                child = final_new_children[0]
                if child.options == rule.options and child.filtered_resolution == rule.filtered_resolution:
                    return child
                else:
                    return Filtered(child, options=rule.options, filtered_resolution=rule.filtered_resolution)
            return Or(*final_new_children, options=rule.options, filtered_resolution=rule.filtered_resolution)
        else:
            return rule

    def _handle_and(self, rule: And) -> Rule:
        if not rule.children:
            return True_()

        if len(rule.children) == 1:
            return self.replace(rule.children[0])

        changed = False
        initial_new_children = []
        for child in rule.children:
            replaced = self.replace(child)
            if replaced is not child:
                changed = True
            if isinstance(replaced, And) and replaced.options == rule.options:
                initial_new_children.extend(replaced.children)
            else:
                initial_new_children.append(replaced)

        # Some early basic ability rule combinations.
        final_new_children: list[Rule] = []
        all_abilities = CharacterAbility.NONE
        any_abilities_set: set[CharacterAbility] = set()
        for child in initial_new_children:
            if child.options == rule.options:
                if isinstance(child, HasAbility) and not isinstance(child.ability, FieldResolver):
                    all_abilities |= child.ability
                elif isinstance(child, HasAllAbilities) and not isinstance(child.abilities, FieldResolver):
                    all_abilities |= child.abilities
                elif isinstance(child, HasAnyAbilities) and not isinstance(child.abilities, FieldResolver):
                    any_abilities_set.add(child.abilities)
                else:
                    final_new_children.append(child)
            else:
                # todo: Abilities with .options set can be optimised based on the other abilities rules.
                final_new_children.append(child)
        all_abilities_simplified = all_abilities.simplify_and()
        if not changed and all_abilities_simplified is not all_abilities:
            changed = True
        if all_abilities_simplified is not CharacterAbility.NONE and any_abilities_set:
            # Every one of these abilities is required for the And rule to return True, so a HasAnyAbilities containing
            # one of these abilities is pointless.
            delete_rule_if_found_in_any_abilities = all_abilities_simplified
            for ability in delete_rule_if_found_in_any_abilities:
                # An ability that is implied by any one of these abilities
                # And(
                #     HasAbility(JEDI),
                #     HasAnyAbilities(CAN_DOUBLE_JUMP | ASTROMECH_PANEL),
                # )
                # can be reduced to just HasAbility(JEDI).
                # Merge in all abilities that `ability` implies. E.g. if JEDI is one of the already found abilities,
                # then CAN_DOUBLE_JUMP can also be removed because JEDI implies CAN_DOUBLE_JUMP.
                for implied_abilities in IMPLIED_ABILITIES[ability]:
                    delete_rule_if_found_in_any_abilities |= implied_abilities

            # Update any_abilities_set to remove pointless rules.
            pointless_removed_any_abilities_set = {
                any_abilities for any_abilities in any_abilities_set
                if (any_abilities & delete_rule_if_found_in_any_abilities) == 0
            }
            if not changed and pointless_removed_any_abilities_set != any_abilities_set:
                changed = True
            any_abilities_set = pointless_removed_any_abilities_set

        # And(
        #     [...],
        #     HasAnyAbilities(CAN_DOUBLE_JUMP | ASTROMECH_PANEL),
        #     HasAnyAbilities(CAN_DOUBLE_JUMP | ASTROMECH_PANEL | BLASTER),
        # )
        # can be reduced to:
        # And(
        #     [...],
        #     HasAnyAbilities(CAN_DOUBLE_JUMP | ASTROMECH_PANEL),
        # )
        # Sort largest bit counts to the top of the stack because these are most likely to contain all the abilities
        # of another HasAllAbilities rule, where that other rule would always be satisfied first.
        any_abilities_stack = sorted(any_abilities_set, key=CharacterAbility.bit_count)
        any_abilities_list = []
        while any_abilities_stack:
            abilities = any_abilities_stack.pop()
            # Iterate in reverse to get the abilities with smallest bits first, since those are most likely to be
            # contained within `abilities`.
            for other_ability in reversed(any_abilities_stack):
                if other_ability in abilities:
                    # `abilities` is pointless because it contains `other_ability`.
                    changed = True
                    break
            else:
                # No break, try the abilities in the lust next.
                for other_ability in reversed(any_abilities_list):
                    if other_ability in abilities:
                        # `abilities` is pointless because it contains `other_ability`.
                        changed = True
                        break
                else:
                    # The ability/abilities are relevant.
                    any_abilities_list.append(abilities)

        # todo: Make sure the hardest to satisfy rules are put towards the front of the children.
        for any_abilities in any_abilities_list:
            if any_abilities.bit_count() == 1:
                # The HasAnyAbilities has reduced to a HasAbility, which can be combined into a HasAllAbilities.
                all_abilities_simplified |= any_abilities
            else:
                # Insert at the front.
                final_new_children.insert(0, HasAnyAbilities(any_abilities))

        if all_abilities_simplified is not CharacterAbility.NONE:
            changed = True
            # Insert the new HasAnyAbilities at the front because it is a fast rule.
            if all_abilities_simplified.bit_count() == 1:
                new_has_all_abilities = HasAbility(all_abilities_simplified)
            else:
                new_has_all_abilities = HasAllAbilities(all_abilities_simplified)
            final_new_children.insert(0, new_has_all_abilities)

        # There could be either zero or one 'all abilities rule' and/or either zero or one 'any abilities rule' that,
        # when processed, produces the same rules as before. In that case, the original rule can be returned instead,
        # reducing memory usage.
        if changed and rule_children_are_the_same(rule.children, final_new_children):
            changed = False

        if changed:
            if len(final_new_children) == 1:
                child = final_new_children[0]
                if child.options == rule.options and child.filtered_resolution == rule.filtered_resolution:
                    return child
                else:
                    return Filtered(child, options=rule.options, filtered_resolution=rule.filtered_resolution)
            return And(*final_new_children, options=rule.options, filtered_resolution=rule.filtered_resolution)
        else:
            return rule

class NestedAndInLevelRuleSimplifierRuleReplacer(NestedOptimizerRuleReplacer):
    def _handle(self, rule: Rule) -> Rule:
        if isinstance(rule, InLevelRule):
            return super()._handle(rule.make_simpler_rule())
        else:
            return super()._handle(rule)
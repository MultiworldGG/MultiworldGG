import functools
import operator
from collections import Counter
from random import Random
from typing import TypeVar, Iterable, ClassVar
from unittest import TestCase

from rule_builder.rules import (
    Rule,
    And,
    Or,
    Has,
    HasAll,
    HasAny,
    HasFromListUnique,
    HasGroup,
    HasAnyCount,
    HasGroupUnique,
    HasAllCounts,
    HasFromList,
    WrapperRule,
    True_,
)

from ..character_ability import CharacterAbility
from ..data.logic.extraction import AbilityRequirements, ItemRequirementsExtractor
from ..data.logic.rules import HasAbility, HasAllAbilities, HasAnyAbilities


_COMMON_ARGS = dict(
    player=1,
    caching_enabled=False,
)


_T = TypeVar("_T")


class TestAbilityExtraction(TestCase):
    r: Random
    extractor: AbilityRequirements

    def setUp(self):
        self.r = Random(1)
        # Override all costs to be the same to induce more randomness.
        self.extractor = AbilityRequirements(self.r, ability_cost_overrides=dict.fromkeys(CharacterAbility, 0))

    def tearDown(self):
        # Allow garbage collection. Notably, the extractor maintains a memodict.
        del self.r
        del self.extractor

    def _random_unique_abilities_gen(self,
                                     min_size: int = 1,
                                     min_excluded: int = 0,
                                     ) -> Iterable[list[CharacterAbility]]:
        all_abilities: list[CharacterAbility] = list(CharacterAbility)
        for i in range(min_size, len(all_abilities) + 1 - min_excluded):
            yield self.r.sample(all_abilities, k=i)

    def _split_into_random_batches(self,
                                   min_batch_size: int,
                                   max_initial_batch_size: int,
                                   elements: list[_T],
                                   ) -> list[list[_T]]:
        if min_batch_size > len(elements):
            raise ValueError(f"min_batch_size ({min_batch_size}) must be <= len(elements) ({len(elements)})")
        stack = elements.copy()
        batches: list[list[_T]] = []
        while stack:
            if len(stack) < min_batch_size:
                # The remaining number is too small for another random batch, so add the remaining to existing batches.
                self.r.choice(batches).append(stack.pop())
            else:
                pop_count = self.r.randint(min_batch_size, min(max_initial_batch_size, len(stack)))
                popped = [stack.pop() for _ in range(pop_count)]
                batches.append(popped)
        return batches

    def _extract_abilities(self,
                           rule: Rule.Resolved,
                           required: CharacterAbility = CharacterAbility.NONE,
                           optional: CharacterAbility = CharacterAbility.NONE,
                           ) -> tuple[CharacterAbility, CharacterAbility, bool]:
        return AbilityRequirements(self.r).extract_ability_requirements(rule, required, optional)

    def test_extract_has_ability(self) -> None:
        """Test that the ability of a HasAbility.Resolved rule is extracted as 'required'."""
        for ability in CharacterAbility:
            rule = HasAbility.Resolved(ability, **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            self.assertIs(requirements[0], ability)
            self.assertIs(requirements[1], CharacterAbility.NONE)
            self.assertFalse(requirements[2])

    def test_extract_has_ability_existing_required(self) -> None:
        """Test that existing required/optional abilities are preserved."""
        for ability in CharacterAbility:
            rule = HasAbility.Resolved(ability, **_COMMON_ARGS)
            existing_optional = ~ability
            requirements = self._extract_abilities(rule, optional=existing_optional)
            self.assertIs(requirements[0], ability)
            self.assertIs(requirements[1], existing_optional)
            self.assertFalse(requirements[2])

    def test_extract_has_all_abilities(self) -> None:
        """Test that all abilities of a HasAllAbilities.Resolved rule are extracted as 'required'."""
        for picks in self._random_unique_abilities_gen():
            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = HasAllAbilities.Resolved(abilities, **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            self.assertIs(requirements[0], abilities)
            self.assertIs(requirements[1], CharacterAbility.NONE)
            self.assertFalse(requirements[2])

    def test_extract_has_any_abilities(self) -> None:
        """Test that one ability of a HasAnyAbilities.Resolved rule is extracted as 'required', and the remaining
        abilities are extracted as 'optional'."""
        for picks in self._random_unique_abilities_gen():
            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = HasAnyAbilities.Resolved(abilities, **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            required, optional, has_other_requirements = requirements
            self.assertEqual(required.bit_count(), 1, "The required abilities should be a single ability.")
            self.assertIs(required | optional, abilities,
                          "The required and optional abilities should equal the input abilities.")
            self.assertIs(required & optional, CharacterAbility.NONE,
                          "There should be no abilities in common between the required and optional abilities.")
            self.assertFalse(has_other_requirements)

    def test_extract_has_any_abilities_fixed_costs(self) -> None:
        """Test that ability costs determine"""
        rule = HasAnyAbilities.Resolved(~CharacterAbility.NONE, **_COMMON_ARGS)
        all_same_costs = dict.fromkeys(CharacterAbility, 1)
        for ability in CharacterAbility:
            extractor = AbilityRequirements(self.r, ability_cost_overrides=all_same_costs | {ability: 0})
            requirements = extractor.extract_ability_requirements(rule)
            required, optional, has_other_requirements = requirements
            self.assertIs(required, ability)
            self.assertIs(optional, ~ability)
            self.assertFalse(has_other_requirements)

    def test_extract_has_any_abilities_existing_required_intersection(self) -> None:
        """Test that if any of the abilities, of a HasAnyAbilities.Resolved rule, are already required, then that
        ability remains required, and all other abilities become optional."""
        for picks in self._random_unique_abilities_gen():
            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = HasAnyAbilities.Resolved(abilities, **_COMMON_ARGS)
            # Pick an ability to mark as already required.
            already_required = self.r.choice(picks)
            requirements = self._extract_abilities(rule, required=already_required)
            required, optional, has_other_requirements = requirements
            self.assertIs(required, already_required,
                          "The required abilities should match the abilities that were already required.")
            self.assertIs(optional, abilities & ~already_required)
            self.assertIs(required | optional, abilities,
                          "The required and optional abilities should equal the input abilities.")
            self.assertIs(required & optional, CharacterAbility.NONE,
                          "There should be no abilities in common between the required and optional abilities.")
            self.assertFalse(has_other_requirements)

    def test_extract_has_any_abilities_existing_required_no_intersection(self) -> None:
        """Test that if any of the abilities, of a HasAnyAbilities.Resolved rule, are already required, then that
        ability remains required, and all other abilities become optional."""
        # Leave at least one ability free, so that there is always an unused ability to pick to mark as
        # already_required.
        for picks in self._random_unique_abilities_gen(min_excluded=1):
            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = HasAnyAbilities.Resolved(abilities, **_COMMON_ARGS)
            # Pick an ability not in `abilities` to mark as already required.
            already_required = self.r.choice(list(~abilities))
            requirements = self._extract_abilities(rule, required=already_required)
            required, optional, has_other_requirements = requirements
            self.assertEqual(required.bit_count(), 2, "The required abilities should be two abilities.")
            self.assertIs(required | optional, abilities | already_required,
                          "The required and optional abilities should equal the input abilities.")
            self.assertIs(required & optional, CharacterAbility.NONE,
                          "There should be no abilities in common between the required and optional abilities.")
            self.assertFalse(has_other_requirements)

    def test_extract_or_simple(self) -> None:
        for picks in self._random_unique_abilities_gen():
            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = Or.Resolved(tuple(HasAbility.Resolved(pick, **_COMMON_ARGS) for pick in abilities), **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            required, optional, has_other_requirements = requirements
            self.assertEqual(required.bit_count(), 1, "The required abilities should be a single ability.")
            self.assertIs(required | optional, abilities,
                          "The required and optional abilities should equal the input abilities.")
            self.assertIs(required & optional, CharacterAbility.NONE,
                          "There should be no abilities in common between the required and optional abilities.")
            self.assertFalse(has_other_requirements)

    def test_extract_and_simple(self) -> None:
        for picks in self._random_unique_abilities_gen():
            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = And.Resolved(tuple(HasAbility.Resolved(pick, **_COMMON_ARGS) for pick in abilities), **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            self.assertIs(requirements[0], abilities)
            self.assertIs(requirements[1], CharacterAbility.NONE)
            self.assertFalse(requirements[2])

    def test_extract_and_nested_and(self):
        min_batch_size = 2
        max_batch_size = 5
        for picks in self._random_unique_abilities_gen(min_size=min_batch_size):

            # Split the picks up into batches of abilities that will go into separate And.Resolved rules.
            batches = self._split_into_random_batches(min_batch_size, max_batch_size, picks)
            and_rules = [
                And.Resolved(
                    tuple(HasAbility.Resolved(ability, **_COMMON_ARGS) for ability in batch),
                    **_COMMON_ARGS
                )
                for batch in batches
            ]

            # Each element is a unique bit, so we can just sum them.
            abilities = CharacterAbility(sum(picks))
            rule = And.Resolved(tuple(and_rules), **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            self.assertIs(requirements[0], abilities)
            self.assertIs(requirements[1], CharacterAbility.NONE)
            self.assertFalse(requirements[2])

    def test_extract_or_nested_and(self):
        min_batch_size = 2
        max_batch_size = 5
        for picks in self._random_unique_abilities_gen(min_batch_size):
            # Split the picks up into batches of abilities that will go into separate And.Resolved rules.
            batches = self._split_into_random_batches(min_batch_size, max_batch_size, picks)
            and_rules = [
                And.Resolved(
                    tuple(HasAbility.Resolved(ability, **_COMMON_ARGS) for ability in batch),
                    **_COMMON_ARGS
                )
                for batch in batches
            ]

            # Construct the rule.
            rule = Or.Resolved(tuple(and_rules), **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            required, optional, has_other_requirements = requirements

            possible_required_abilities = {functools.reduce(operator.or_, batch) for batch in batches}
            self.assertEqual(len(batches), len(possible_required_abilities))

            # Each element is a unique bit, so we can just sum them to find all the abilities contained within the rule.
            abilities = CharacterAbility(sum(picks))

            self.assertIn(required, possible_required_abilities,
                          "The required abilities should be from a single batch.")
            self.assertIs(required | optional, abilities,
                          "The required and optional abilities should equal the input abilities.")
            self.assertIs(required & optional, CharacterAbility.NONE,
                          "There should be no abilities in common between the required and optional abilities.")
            self.assertFalse(has_other_requirements)

    def test_extract_or_nested_and_already_required(self):
        min_batch_size = 2
        max_batch_size = 5
        for picks in self._random_unique_abilities_gen(min_batch_size):
            # Split the picks up into batches of abilities that will go into separate And.Resolved rules.
            batches = self._split_into_random_batches(min_batch_size, max_batch_size, picks)
            and_rules = [
                And.Resolved(
                    tuple(HasAbility.Resolved(ability, **_COMMON_ARGS) for ability in batch),
                    **_COMMON_ARGS
                )
                for batch in batches
            ]

            already_required = functools.reduce(operator.or_, self.r.choice(batches))

            # Construct the rule.
            rule = Or.Resolved(tuple(and_rules), **_COMMON_ARGS)
            requirements = self._extract_abilities(rule, required=already_required)
            required, optional, has_other_requirements = requirements

            possible_required_abilities = {functools.reduce(operator.or_, batch) for batch in batches}
            self.assertEqual(len(batches), len(possible_required_abilities))

            # Each element is a unique bit, so we can just sum them to find all the abilities contained within the rule.
            abilities = CharacterAbility(sum(picks))

            self.assertIs(required, already_required,
                          "The required abilities should match the already_required abilities.")
            self.assertIs(required | optional, abilities,
                          "The required and optional abilities should equal the input abilities.")
            self.assertIs(required & optional, CharacterAbility.NONE,
                          "There should be no abilities in common between the required and optional abilities.")
            self.assertFalse(has_other_requirements)

    def test_extract_or_has_ability_and_has(self) -> None:
        for ability in CharacterAbility:
            rule1 = HasAbility.Resolved(ability, **_COMMON_ARGS)
            rule2 = Has.Resolved("item", **_COMMON_ARGS)
            rule = Or.Resolved((rule1, rule2), **_COMMON_ARGS)
            requirements = self._extract_abilities(rule)
            self.assertIs(requirements[0], ability)
            self.assertIs(requirements[1], CharacterAbility.NONE)
            self.assertFalse(requirements[2])

    def test_extract_or_no_abilities(self) -> None:
        rule1 = Has.Resolved("item", **_COMMON_ARGS)
        rule2 = Has.Resolved("other item", **_COMMON_ARGS)
        rule = Or.Resolved((rule1, rule2), **_COMMON_ARGS)
        requirements = self._extract_abilities(rule)
        self.assertIs(requirements[0], CharacterAbility.NONE)
        self.assertIs(requirements[1], CharacterAbility.NONE)
        self.assertTrue(requirements[2])

    # TODO: Test And.Resolved containing Has.Resolved.
    # TODO: Test Or.Resolved containing Has.Resolved, where `required`/`optional` are already set.
    # TODO: Test And.Resolved containing Has.Resolved, where `required`/`optional` are already set.

class TestItemExtraction(TestCase):
    extractor: ClassVar[ItemRequirementsExtractor]

    item: ClassVar[str] = "item"

    item_counts: ClassVar[tuple[tuple[str, int], ...]] = tuple((f"item{i}", i) for i in range(1, 6))
    item_counts_counter: ClassVar[Counter[str]] = Counter(dict(item_counts))

    item_names: ClassVar[tuple[str, ...]] = tuple(f"item{i}" for i in range(1, 6))
    item_names_counter: ClassVar[Counter[str]] = Counter(item_names)

    group: ClassVar[str] = "group"

    item_counts2: ClassVar[tuple[tuple[str, int], ...]] = tuple((f"item{i}", i * 2) for i in range(3, 8))
    item_counts2_counter: ClassVar[Counter[str]] = Counter(dict(item_counts2))

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.extractor = ItemRequirementsExtractor()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        # Allow garbage collection.
        del cls.extractor

    def extract(self, rule: Rule.Resolved) -> Counter[str]:
        return self.extractor.extract_item_requirements(rule)

    def test_has(self):
        for i in range(1, 6):
            rule = Has.Resolved(item_name="item", count=i, **_COMMON_ARGS)
            extracted = self.extract(rule)
            self.assertEqual(extracted, Counter({"item": i}))

    def _test_item_counts(self, rule: Rule.Resolved):
        extracted = self.extract(rule)
        self.assertEqual(extracted, self.item_counts_counter)

    def test_has_all_counts(self):
        self._test_item_counts(HasAllCounts.Resolved(self.item_counts, **_COMMON_ARGS))

    def test_has_any_count(self):
        self._test_item_counts(HasAnyCount.Resolved(self.item_counts, **_COMMON_ARGS))

    def _test_item_names_count(self, rule: Rule.Resolved, count: int):
        extracted = self.extract(rule)
        expected = Counter({k: v * count for k, v in self.item_names_counter.items()})
        self.assertEqual(extracted, expected)

    def test_has_from_list(self):
        for i in range(1, 6):
            self._test_item_names_count(HasFromList.Resolved(self.item_names, count=i, **_COMMON_ARGS), i)

    def test_has_group(self):
        for i in range(1, 6):
            self._test_item_names_count(HasGroup.Resolved(self.group, self.item_names, count=i, **_COMMON_ARGS), i)

    def _test_item_names(self, rule: Rule.Resolved):
        extracted = self.extract(rule)
        self.assertEqual(extracted, self.item_names_counter)

    def test_has_any(self):
        self._test_item_names(HasAny.Resolved(self.item_names, **_COMMON_ARGS))

    def test_has_all(self):
        self._test_item_names(HasAll.Resolved(self.item_names, **_COMMON_ARGS))

    def test_has_from_list_unique(self):
        for i in range(1, 6):
            self._test_item_names(HasFromListUnique.Resolved(self.item_names, count=i, **_COMMON_ARGS))

    def test_has_group_unique(self):
        for i in range(1, 6):
            self._test_item_names(HasGroupUnique.Resolved(self.group, self.item_names, count=i, **_COMMON_ARGS))

    def test_wrapper_rule(self):
        for i in range(1, 6):
            rule = WrapperRule.Resolved(Has.Resolved(item_name="item", count=i, **_COMMON_ARGS), **_COMMON_ARGS)
            extracted = self.extract(rule)
            self.assertEqual(extracted, Counter({"item": i}))

        self._test_item_names(WrapperRule.Resolved(HasAny.Resolved(self.item_names, **_COMMON_ARGS), **_COMMON_ARGS))

        for i in range(1, 6):
            self._test_item_names(
                WrapperRule.Resolved(
                    HasFromListUnique.Resolved(self.item_names, count=i, **_COMMON_ARGS),
                    **_COMMON_ARGS,
                )
            )

    def _test_nested(self, rule_cls: type[And.Resolved] | type[Or.Resolved]):
        r1 = Has.Resolved(item_name="item2", count=17, **_COMMON_ARGS)
        r1_counter = Counter({"item2": 17})
        r2 = HasAllCounts.Resolved(self.item_counts, **_COMMON_ARGS)
        r2_counter = self.item_counts_counter
        r3 = HasAnyCount.Resolved(self.item_counts2, **_COMMON_ARGS)
        r3_counter = self.item_counts2_counter

        rule = rule_cls(children=(r1, r2, r3), **_COMMON_ARGS)

        keys = set().union(r1_counter.keys(), r2_counter.keys(), r3_counter.keys())
        combined_counts = Counter()
        for k in keys:
            combined_counts[k] = max(r1_counter[k], r2_counter[k], r3_counter[k])

        extracted = self.extract(rule)
        self.assertEqual(extracted, combined_counts)

    def test_or(self):
        self._test_nested(Or.Resolved)

    def test_and(self):
        self._test_nested(And.Resolved)

    def test_non_item_rule(self):
        rule = True_.Resolved(**_COMMON_ARGS)
        extracted = self.extract(rule)
        self.assertEqual(extracted, Counter())

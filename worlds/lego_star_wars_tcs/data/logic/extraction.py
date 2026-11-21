from dataclasses import dataclass, field
from collections import Counter
from random import Random

from BaseClasses import CollectionState
from rule_builder.rules import (
    Rule,
    Or,
    And,
    True_,
    WrapperRule,
    Has,
    HasAll,
    HasAny,
    HasFromListUnique,
    HasGroup,
    HasAnyCount,
    HasFromList,
    HasAllCounts,
    HasGroupUnique,
    CanReachRegion,
)

from .rules import InLevelRule, HasAbility, HasAnyAbilities, HasAllAbilities
from .rule_replacement import RuleReplacer
from ..items.character_items import NORMAL_CHARACTER_DATA
from ..items.vehicle_items import VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from ...character_ability import CharacterAbility


class ExtractionRuleReplacer(RuleReplacer):
    def __init__(self):
        super().__init__({})

    def _handle(self, rule: Rule) -> Rule:
        if isinstance(rule, InLevelRule):
            simpler = rule.make_simpler_rule()
            # If the rule cannot be simplified, then it may return itself.
            if simpler is not rule:
                return self.replace(simpler)
            else:
                return rule
        return super()._handle(rule)


def _make_default_ability_costs() -> dict[CharacterAbility, int]:
    """Make ability costs based on ability frequency. Vehicle and non-vehicle abilities are calculated separately."""
    non_vehicle_abilities_counter = Counter()
    for character_data in NORMAL_CHARACTER_DATA:
        non_vehicle_abilities_counter.update(character_data.abilities)
    non_vehicle_abilities_max = max(non_vehicle_abilities_counter.values())

    vehicle_abilities_counter = Counter()
    for character_data in VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA.values():
        vehicle_abilities_counter.update(character_data.abilities)
    # All vehicles are...vehicles, which is an irrelevant cost to consider.
    del vehicle_abilities_counter[CharacterAbility.IS_A_VEHICLE]
    vehicle_abilities_max = max(vehicle_abilities_counter.values())

    return {
        # ** 2 so that the cost increases more as abilities get rarer.
        # + 1 so that the lowest cost is 1 instead of zero
        **{k: non_vehicle_abilities_max - v ** 2 + 1 for k, v in non_vehicle_abilities_counter.items()},
        **{k: vehicle_abilities_max - v ** 2 + 1 for k, v in vehicle_abilities_counter.items()},
        # Re-add the removed IS_A_VEHICLE ability with a cost of zero.
        CharacterAbility.IS_A_VEHICLE: 0,
    }


DEFAULT_ABILITY_COSTS = _make_default_ability_costs()
# The below comment may be out-of-date, but is enough to give a rough overview.
# DEFAULT_ABILITY_COSTS: dict[CharacterAbility, int] = {
#     # Vehicle abilities are calculated separately.
#     VEHICLE_TOW: 257,
#     VEHICLE_TIE: 226,
#     VEHICLE_BLASTER: 1,
#     IS_A_VEHICLE: 0,
#
#     # 2 Characters
#     JETPACK: 13925,
#     CAN_HIGH_JUMP_SLAM: 13925,
#     WEAPON_EWOK: 13925,
#
#     # 3 Characters
#     ASTROMECH_DROID: 13690,
#
#     # 4 Characters
#     SITH: 13457,
#     PROTOCOL_PANEL: 13457,
#     HIGH_JUMP: 13457,
#
#     # 5 Characters
#     HOVER: 13226,
#     ASTROMECH_PANEL: 13226,
#
#     # 6 Characters
#     WEAPON_ZAPPER: 12997,
#     SHORTIE: 12997,
#
#     # 8 Characters
#     BOUNTY_HUNTER: 12545,
#
#     # 15 Characters
#     CAN_WEAR_HAT_AND_DOUBLE_JUMP: 11026,
#     CAN_SELF_DESTRUCT: 11026,
#
#     IMPERIAL: 10202,
#     IS_NON_GHOST_JEDI: 9217,
#     CAN_TRIPLE_JUMP_GREAT_DISTANCE: 8837,
#     JEDI: 8650,
#     CAN_WEAR_HAT_AND_GRAPPLE: 8465,
#     CAN_DEFLECT_BOLTS: 8282,
#     CAN_DOUBLE_JUMP: 7922,
#     CAN_FLOP_JUMP: 6890,
#     CAN_WEAR_HAT: 5477,
#     GRAPPLE: 3026,
#     BLASTER: 2305,
#     CAN_JUMP_DISTANCE_0_92: 1765,
#     CAN_JUMP_0_44: 1445,
#     CAN_MELEE: 1445,
#     CAN_JUMP_DISTANCE_0_84: 362,
#     RUN_SPEED_1_18_OR_HIGHER: 290,
#     CAN_PULL_LEVERS: 145,
#     CAN_BUILD_BRICKS: 122,
#     # All characters that can push objects also can ride vehicles, and vice-versa, so these use the same flag for better
#     # performance.
#     CAN_RIDE_VEHICLES: 65,
#     # CAN_PUSH_OBJECTS: 65,
#     CAN_AGGRAVATE_ENEMIES: 65,
#     CAN_JUMP_HEIGHT_0_37: 26,
#     CAN_JUMP_DISTANCE_0_69: 26,
#     CAN_BARELY_JUMP: 5,
#     RUN_SPEED_0_9_OR_HIGHER: 1,
# }


AbilityRequirementsKey = tuple[Rule.Resolved, CharacterAbility, bool]
AbilityRequirementsValue = tuple[CharacterAbility, CharacterAbility, bool]


# todo: can `required` abilities and `optional` abilities always get combined, and then do `optional &= ~required` at
#  the and?
@dataclass
class AbilityRequirements:
    random: Random
    ability_cost_overrides: dict[CharacterAbility, int] = field(default_factory=dict)
    abilities_memodict: dict[AbilityRequirementsKey, AbilityRequirementsValue] = field(default_factory=dict)
    ability_costs: dict[CharacterAbility, int] = field(init=False)
    
    def __post_init__(self):
        # Ensure there is a default cost for every ability and then merge in any overrides.
        self.ability_costs = DEFAULT_ABILITY_COSTS | self.ability_cost_overrides

    def _memoize(self,
                 key: AbilityRequirementsKey,
                 result: AbilityRequirementsValue,
                 ) -> AbilityRequirementsValue:
        self.abilities_memodict[key] = result
        return result
    
    def _get_ability_cost(self, abilities: CharacterAbility):
        if abilities in self.ability_costs:
            return self.ability_costs[abilities]
        # Individual abilities are guaranteed to be present.
        cost = sum(map(self.ability_costs.__getitem__, abilities))
        self.ability_costs[abilities] = cost
        return cost

    # todo: Is the `optional` argument even necessary? It is only ever combined with currently, so would not be
    #  necessary.
    def extract_ability_requirements(
            self,
            rule: Rule.Resolved,
            required: CharacterAbility = CharacterAbility.NONE,
            optional: CharacterAbility = CharacterAbility.NONE,
            has_other_requirements: bool = False,
    ) -> AbilityRequirementsValue:
        # Resolved rules are singletons, so if a resolved rule is used in multiple places, it is the same instance.
        key = rule, required, has_other_requirements
        if key in self.abilities_memodict:
            return self.abilities_memodict[key]

        if isinstance(rule, Or.Resolved):
            # Explicit type hint to work around bugs in PyCharm's type checker.
            rule: Or.Resolved

            # Any one rule must be required.
            # First try to find if there is any rule whose required abilities are already satisfied. If so, then all
            # abilities used by the child rules are optional, besides those that are already in `required`.
            found_requirements: list[AbilityRequirementsValue] = []
            child_iter = iter(rule.children)
            for child in child_iter:
                requirements = self.extract_ability_requirements(child, required, optional, has_other_requirements)
                if not has_other_requirements and requirements[2]:
                    # The caller does not have non-ability requirements, but this child does.
                    # Even if this child's abilities are already satisfied, there is no way to tell if the full child
                    # rule is already satisfied.
                    found_requirements.append(requirements)
                elif requirements[0] in required:
                    # This child is already satisfied by the required abilities, so the whole rule is satisfied by
                    # the abilities.
                    # Mark everything as optional.
                    optional |= requirements[1]
                    # And the requirements from already processed children.
                    for required_for_child_but_optional_for_parent, optional_requirement, _ in found_requirements:
                        optional |= required_for_child_but_optional_for_parent | optional_requirement
                    # And the requirements from the remaining children.
                    for remaining_child in child_iter:
                        # todo: Does it matter that `optional` has already been modified?
                        requirements = self.extract_ability_requirements(remaining_child, required, optional, has_other_requirements)
                        optional |= requirements[0] | requirements[1]
                    # Remove required abilities from optional abilities before returning.
                    return self._memoize(key, (required, optional & ~required, has_other_requirements))
                else:
                    found_requirements.append(requirements)
            if not found_requirements:
                raise Exception("Or() rule is empty.")
            # Find the child with the lowest 'cost', preferring children that can be satisfied by only abilities.
            # Shuffle first, so that, if there is a tie, the tie is resolved randomly.
            self.random.shuffle(found_requirements)
            if not has_other_requirements:
                # Prefer rules without non-ability requirements.
                found_requirements.sort(key=lambda t: (t[2], self._get_ability_cost(t[0] & ~required)))
            else:
                found_requirements.sort(key=lambda t: self._get_ability_cost(t[0] & ~required))
            first = found_requirements[0]
            required |= first[0]
            optional |= first[1]
            or_has_other_requirements = first[2]
            for required_for_child_but_optional_for_parent, optional_requirement, _ in found_requirements[1:]:
                optional |= required_for_child_but_optional_for_parent | optional_requirement
            return self._memoize(
                key, (required, optional & ~required, has_other_requirements or or_has_other_requirements))

        if isinstance(rule, And.Resolved):
            rule: And.Resolved

            and_has_other_requirements = False
            for child in rule.children:
                requirements = self.extract_ability_requirements(child, required, optional, has_other_requirements)
                # Union the abilities.
                required |= requirements[0]
                optional |= requirements[1]
                if requirements[2]:
                    and_has_other_requirements = True
            # Remove all required abilities from the optional abilities before returning.
            return self._memoize(
                key, (required, optional & ~required, has_other_requirements or and_has_other_requirements))

        if isinstance(rule, HasAbility.Resolved):
            rule: HasAbility.Resolved

            return self._memoize(key, (required | CharacterAbility(rule.ability_as_int), optional, has_other_requirements))

        if isinstance(rule, HasAnyAbilities.Resolved):
            rule: HasAnyAbilities.Resolved

            abilities = CharacterAbility(rule.abilities_as_int)
            intersection = abilities & required
            if intersection is not CharacterAbility.NONE:
                # This rule would already be satisfied by the currently required abilities.
                # Find other abilities present in this rule that are not already required, and mark them as optional.
                other_abilities = abilities & ~required
                return self._memoize(key, (required, optional | other_abilities, has_other_requirements))
            else:
                # This rule would not already be satisfied by the currently required abilities.
                # todo: Should we prefer picking an ability that is already in `optional` to promote to `required`, or
                #  prefer an ability that is in neither `optional` nor `required`?
                # Pick the lowest cost ability used by this rule.
                # Shuffle first for randomness in any tie breaks.
                abilities_list = list(abilities)
                self.random.shuffle(abilities_list)
                # Individual abilities are guaranteed to exist in .ability_costs, so access it directly.
                picked_ability: CharacterAbility = min(abilities, key=self.ability_costs.__getitem__)
                # Remove the picked ability from the other abilities.
                other_abilities = abilities & ~picked_ability
                # Remove the picked ability from the optional abilities (if present)
                optional &= ~picked_ability
                return self._memoize(
                    key, (required | picked_ability, optional | other_abilities, has_other_requirements))

        if isinstance(rule, HasAllAbilities.Resolved):
            rule: HasAllAbilities.Resolved

            # All abilities are required.
            return self._memoize(
                key, (CharacterAbility(required | rule.abilities_as_int), optional, has_other_requirements))

        if isinstance(rule, True_.Resolved):
            return self._memoize(key, (required, optional, has_other_requirements))

        if isinstance(rule, WrapperRule.Resolved):
            rule: WrapperRule.Resolved

            return self._memoize(
                key, (self.extract_ability_requirements(rule.child, required, optional, has_other_requirements)))

        # This rule does not have ability requirements, e.g. it is a Has("Exploding Blaster Bolts"), or a
        # CanReachRegion("region name") or similar.
        # Note that it is not expected to see a False_ rule within an And or Or rule, only on its own.
        return self._memoize(key, (required, optional, True))


@dataclass
class ItemRequirementsExtractor:
    """Extract the maximum logically relevant counts of item names from resolved rules."""

    items_memodict: dict[Rule.Resolved, Counter[str]] = field(default_factory=dict)

    def _memoize(self, rule: Rule.Resolved, counts: Counter[str]) -> Counter[str]:
        # Resolved rules are singletons, so an individual resolved rule only needs to be processed at most once.
        self.items_memodict[rule] = counts
        return counts

    def extract_item_requirements(self, rule: Rule.Resolved) -> Counter[str]:
        """Extract the maximum logically relevant counts of item names used by a resolved rule."""
        existing = self.items_memodict.get(rule)
        if existing is not None:
            return existing

        if isinstance(rule, Has.Resolved):
            rule: Has.Resolved
            return self._memoize(rule, Counter({rule.item_name: rule.count}))

        if isinstance(rule, (HasAllCounts.Resolved, HasAnyCount.Resolved)):
            rule: HasAllCounts.Resolved | HasAnyCount.Resolved
            return self._memoize(rule, Counter(dict(rule.item_counts)))

        if isinstance(rule, (HasFromList.Resolved, HasGroup.Resolved)):
            rule: HasFromList.Resolved | HasGroup.Resolved
            # While it is likely that a player could achieve a count of 4 items through 2 of item A and 2 of item B,
            # up to 4 of item A would still be logically relevant.
            # The return value from this function could be changed to a tuple[Counter[str], Counter[str]], or similar,
            # where one Counter specifies the maximum, and the other Counter specifies the minimum.
            if rule.count == 1:
                return self._memoize(rule, Counter(rule.item_names))
            else:
                return self._memoize(rule, Counter(dict.fromkeys(rule.item_names, rule.count)))

        if isinstance(rule, (HasAny.Resolved, HasAll.Resolved, HasFromListUnique.Resolved, HasGroupUnique.Resolved)):
            rule: HasAny.Resolved | HasAll.Resolved | HasFromListUnique.Resolved | HasGroupUnique.Resolved
            return self._memoize(rule, Counter(rule.item_names))

        if isinstance(rule, (And.Resolved, Or.Resolved)):
            rule: And.Resolved | Or.Resolved
            requirements = Counter()
            # todo?: Might there be some cases where Or.Resolved should be using `min(A[key], B[key])`?
            for child in rule.children:
                # Union of counters A and B performs element-wise `result[key] = max(A[key], B[key])`.
                child_requirements = self.extract_item_requirements(child)
                requirements |= child_requirements
            return self._memoize(rule, requirements)

        if isinstance(rule, WrapperRule.Resolved):
            rule: WrapperRule.Resolved
            return self._memoize(rule, self.extract_item_requirements(rule.child))


        return self._memoize(rule, Counter())


@dataclass
class DNFAbilityRequirementsExtractor:
    """Extract requirements in `Or(*HasAllAbilities(?) for ? in ?)` form."""
    cnf_extractor: "CNFAbilityRequirementsExtractor"
    abilities_memodict: dict[Rule.Resolved, set[CharacterAbility] | None]
    ignore_can_reach_region: bool

    def __init__(self, ignore_can_reach_region: bool, cnf_extractor: "CNFAbilityRequirementsExtractor | None" = None):
        self.ignore_can_reach_region = ignore_can_reach_region
        self.abilities_memodict = {}
        if cnf_extractor is None:
            self.cnf_extractor = CNFAbilityRequirementsExtractor(ignore_can_reach_region, self)
        else:
            self.cnf_extractor = cnf_extractor

    def _memoize(self,
                 rule: Rule.Resolved,
                 and_has_any_abilities: set[CharacterAbility] | None
                 ) -> set[CharacterAbility] | None:
        # Resolved rules are singletons, so an individual resolved rule only needs to be processed at most once.
        self.abilities_memodict[rule] = and_has_any_abilities
        return and_has_any_abilities

    def extract_ability_requirements(self, rule: Rule.Resolved) -> set[CharacterAbility] | None:
        existing = self.abilities_memodict.get(rule)
        if existing is not None:
            return existing

        if isinstance(rule, Or.Resolved):
            # Explicit type hint to work around bugs in PyCharm's type checker.
            rule: Or.Resolved

            or_has_all_requirements: set[CharacterAbility] = set()
            found = False
            for child in rule.children:
                requirements = self.extract_ability_requirements(child)
                if requirements is not None:
                    found = True
                    or_has_all_requirements.update(requirements)
            if not or_has_all_requirements and not found:
                return self._memoize(rule, None)

            return self._memoize(rule, CharacterAbility.optimize_or_has_all_abilities(or_has_all_requirements))

        if isinstance(rule, And.Resolved):
            rule: And.Resolved

            and_has_any_requirements: set[CharacterAbility] = set()
            for child in rule.children:
                cnf_requirements = self.cnf_extractor.extract_ability_requirements(child)
                if cnf_requirements is None:
                    # This And rule cannot be satisfied with abilities alone.
                    return self._memoize(rule, None)
                and_has_any_requirements.update(and_has_any_requirements)
            return self._memoize(rule, CharacterAbility.convert_and_has_any_to_or_has_all(*and_has_any_requirements))

        if isinstance(rule, HasAbility.Resolved):
            rule: HasAbility.Resolved

            return self._memoize(rule, {CharacterAbility(rule.ability_as_int)})

        if isinstance(rule, HasAnyAbilities.Resolved):
            rule: HasAnyAbilities.Resolved

            abilities = CharacterAbility(rule.abilities_as_int)
            as_or_has_all_abilities = CharacterAbility.convert_and_has_any_to_or_has_all(abilities)

            return self._memoize(rule, as_or_has_all_abilities)

        if isinstance(rule, HasAllAbilities.Resolved):
            rule: HasAllAbilities.Resolved

            # All abilities are required.
            # HasAbilities(abilities) is the same as Or(HasAbilities(abilities)).
            return self._memoize(rule, {CharacterAbility(rule.abilities_as_int)})

        if isinstance(rule, True_.Resolved):
            return self._memoize(rule, set())

        if isinstance(rule, WrapperRule.Resolved):
            rule: WrapperRule.Resolved

            return self._memoize(rule, self.extract_ability_requirements(rule.child))

        if self.ignore_can_reach_region and isinstance(rule, CanReachRegion.Resolved):
            return self._memoize(rule, set())

        # This rule does not have ability requirements, e.g. it is a Has("Exploding Blaster Bolts"), or a
        # CanReachRegion("region name") or similar.
        return self._memoize(rule, None)



class CNFAbilityRequirementsExtractor:
    """Extract requirements in `And(*HasAnyAbilities(?) for ? in ?)` form."""
    dnf_extractor: DNFAbilityRequirementsExtractor
    abilities_memodict: dict[Rule.Resolved, set[CharacterAbility] | None]
    ignore_can_reach_region: bool

    def __init__(self, ignore_can_reach_region: bool, dnf_extractor: DNFAbilityRequirementsExtractor | None = None):
        self.ignore_can_reach_region = ignore_can_reach_region
        self.abilities_memodict = {}
        if dnf_extractor is None:
            self.dnf_extractor = DNFAbilityRequirementsExtractor(ignore_can_reach_region, self)
        else:
            self.dnf_extractor = dnf_extractor


    def _memoize(self,
                 rule: Rule.Resolved,
                 and_has_any_abilities: set[CharacterAbility] | None
                 ) -> set[CharacterAbility] | None:
        # Resolved rules are singletons, so an individual resolved rule only needs to be processed at most once.
        self.abilities_memodict[rule] = and_has_any_abilities
        return and_has_any_abilities

    def extract_ability_requirements(self, rule: Rule.Resolved) -> set[CharacterAbility] | None:
        existing = self.abilities_memodict.get(rule)
        if existing is not None:
            return existing

        if isinstance(rule, Or.Resolved):
            # Explicit type hint to work around bugs in PyCharm's type checker.
            rule: Or.Resolved

            or_has_any_requirements: set[CharacterAbility] = set()
            found = False
            for child in rule.children:
                cnf_requirements = self.dnf_extractor.extract_ability_requirements(child)
                if cnf_requirements is not None:
                    or_has_any_requirements.update(cnf_requirements)
                    # The requirements may be empty signifying that the rule is true without abilities. This needs to be
                    # tracked because an empty Or() returns false, like `any([])`
                    found = True
            if not or_has_any_requirements and not found:
                return self._memoize(rule, None)
            return self._memoize(rule, CharacterAbility.convert_or_has_all_to_and_has_any(*or_has_any_requirements))

        if isinstance(rule, And.Resolved):
            rule: And.Resolved

            and_has_any_requirements: set[CharacterAbility] = set()
            for child in rule.children:
                requirements = self.extract_ability_requirements(child)
                if requirements is None:
                    # This And rule cannot be satisfied with abilities alone.
                    return self._memoize(rule, None)
                and_has_any_requirements.update(requirements)
            return self._memoize(rule, CharacterAbility.optimize_and_has_any_abilities(and_has_any_requirements))

        if isinstance(rule, HasAbility.Resolved):
            rule: HasAbility.Resolved

            return self._memoize(rule, {CharacterAbility(rule.ability_as_int)})

        if isinstance(rule, HasAnyAbilities.Resolved):
            rule: HasAnyAbilities.Resolved

            # HasAnyAbilities(abilities) is the same as And(HasAnyAbilities(abilities)).
            return self._memoize(rule, {CharacterAbility(rule.abilities_as_int)})

        if isinstance(rule, HasAllAbilities.Resolved):
            rule: HasAllAbilities.Resolved

            abilities = CharacterAbility(rule.abilities_as_int)
            as_and_has_any_abilities = CharacterAbility.convert_or_has_all_to_and_has_any(abilities)

            return self._memoize(rule, as_and_has_any_abilities)

        if isinstance(rule, True_.Resolved):
            return self._memoize(rule, set())

        if isinstance(rule, WrapperRule.Resolved):
            rule: WrapperRule.Resolved

            return self._memoize(rule, self.extract_ability_requirements(rule.child))

        if self.ignore_can_reach_region and isinstance(rule, CanReachRegion.Resolved):
            return self._memoize(rule, set())

        # This rule does not have ability requirements, e.g. it is a Has("Exploding Blaster Bolts"), or a
        # CanReachRegion("region name") or similar.
        return self._memoize(rule, None)


@dataclass
class LogicalRequirementsExtractor:
    """Extract the maximum logically relevant counts of item names, and logically relevant abilities, from resolved
     rules.

    When given an initial state, this will reduce maximum logically relevant counts by the items already collected by
    the state.
    """

    @dataclass(frozen=True)
    class Requirements:
        item_counts: Counter[str] = field(default_factory=Counter)
        abilities: CharacterAbility = CharacterAbility.NONE

        def __bool__(self):
            return bool(self.item_counts) and bool(self.abilities)

        def __or__(self, 
                   other: "LogicalRequirementsExtractor.Requirements"
                   ) -> "LogicalRequirementsExtractor.Requirements":
            return LogicalRequirementsExtractor.Requirements(
                self.item_counts | other.item_counts, self.abilities | other.abilities)


    initial_state: CollectionState | None = None
    memodict: dict[Rule.Resolved, Requirements] = field(default_factory=dict)

    def _memoize(self, rule: Rule.Resolved, requirements: Requirements) -> Requirements:
        # Resolved rules are singletons, so an individual resolved rule only needs to be processed at most once.
        self.memodict[rule] = requirements
        return requirements

    def extract_requirements(self, rule: Rule.Resolved) -> Requirements:
        existing = self.memodict.get(rule)
        if existing is not None:
            return existing

        state = self.initial_state

        if state is not None and rule(state):
            # The rule is satisfied by the state, so there are no missing requirements.
            return self._memoize(rule, LogicalRequirementsExtractor.Requirements())

        if isinstance(rule, HasAbility.Resolved):
            rule: HasAbility.Resolved

            return self._memoize(
                rule, LogicalRequirementsExtractor.Requirements(abilities=CharacterAbility(rule.ability_as_int)))

        if isinstance(rule, HasAnyAbilities.Resolved):
            rule: HasAnyAbilities.Resolved

            return self._memoize(
                rule, LogicalRequirementsExtractor.Requirements(abilities=CharacterAbility(rule.abilities_as_int)))

        if isinstance(rule, HasAllAbilities.Resolved):
            rule: HasAllAbilities.Resolved

            abilities = CharacterAbility(rule.abilities_as_int)
            if state is not None:
                state_abilities = CharacterAbility(state.count("COMBINED_ABILITIES", rule.player))
                abilities = abilities & ~state_abilities

            return self._memoize(rule, LogicalRequirementsExtractor.Requirements(abilities=abilities))

        if isinstance(rule, Has.Resolved):
            rule: Has.Resolved
            if state is not None:
                missing_count = rule.count - state.count(rule.item_name, rule.player)
                counts = {rule.item_name: missing_count}
            else:
                counts = {rule.item_name: rule.count}
            return self._memoize(rule, LogicalRequirementsExtractor.Requirements(item_counts=Counter(counts)))

        if isinstance(rule, (HasAllCounts.Resolved, HasAnyCount.Resolved)):
            rule: HasAllCounts.Resolved | HasAnyCount.Resolved
            if state is not None:
                counts = {
                    item: count - state.count(item, rule.player) for item, count in rule.item_counts
                }
            else:
                counts = dict(rule.item_counts)
            return self._memoize(rule, LogicalRequirementsExtractor.Requirements(item_counts=Counter(counts)))

        if isinstance(rule, (HasFromList.Resolved, HasGroup.Resolved)):
            rule: HasFromList.Resolved | HasGroup.Resolved
            # While it is likely that a player could achieve a count of 4 items through 2 of item A and 2 of item B,
            # up to 4 of item A would still be logically relevant.
            if rule.count == 1:
                # The `state` can be ignored because if any one item was present, the rule would have returned True
                # given `state`.
                return self._memoize(
                    rule, LogicalRequirementsExtractor.Requirements(item_counts=Counter(rule.item_names)))
            else:
                if state is not None:
                    counts = {
                        item: rule.count - state.count(item, rule.player) for item in rule.item_names
                    }
                else:
                    counts = dict.fromkeys(rule.item_names, rule.count)
                return self._memoize(rule, LogicalRequirementsExtractor.Requirements(item_counts=Counter(counts)))

        if isinstance(rule, (HasAny.Resolved, HasAll.Resolved, HasFromListUnique.Resolved, HasGroupUnique.Resolved)):
            rule: HasAny.Resolved | HasAll.Resolved | HasFromListUnique.Resolved | HasGroupUnique.Resolved
            # If a HasAny rule was not satisfied, then the state must have none of the items.
            if state is not None and not isinstance(rule, HasAny.Resolved):
                item_names = [item for item in rule.item_names if not state.has(item, rule.player)]
            else:
                item_names = rule.item_names
            return self._memoize(rule, LogicalRequirementsExtractor.Requirements(item_counts=Counter(item_names)))

        if isinstance(rule, (And.Resolved, Or.Resolved)):
            rule: And.Resolved | Or.Resolved
            requirements = LogicalRequirementsExtractor.Requirements()
            # todo?: Might there be some cases where Or.Resolved should be using `min(A[key], B[key])`?
            for child in rule.children:
                child_requirements = self.extract_requirements(child)
                requirements |= child_requirements
            return self._memoize(rule, requirements)

        if isinstance(rule, WrapperRule.Resolved):
            rule: WrapperRule.Resolved
            return self._memoize(rule, self.extract_requirements(rule.child))

        return self._memoize(rule, LogicalRequirementsExtractor.Requirements())

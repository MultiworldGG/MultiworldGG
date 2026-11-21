import dataclasses
from functools import reduce
from operator import or_
from typing import ClassVar, Iterable, TYPE_CHECKING, Any, Self, AbstractSet
from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.field_resolvers import FieldResolver, resolve_field
from rule_builder.options import OptionFilter
from rule_builder.rules import (
    False_,
    Filtered,
    HasAll,
    HasAny,
    Rule,
    True_,
    TWorld,
    And,
    Or,
)

from ..characters import Character
from ..items.all_character_items import (
    CHARACTER_TO_ITEM_DATA,
    EXTRA_TOGGLE_CHARACTER_TO_ITEM_DATA,
    NORMAL_CHARACTER_TO_ITEM_DATA,
)
from ..items.character_items import NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA, SORTED_SINGLE_JUMP_DISTANCE_TO_CHARACTERS
from ..items.vehicle_items import VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
from ...character_ability import CharacterAbility, IMPLIED_BY_ABILITIES
from ...constants import GAME_NAME


if TYPE_CHECKING:
    from ... import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = TWorld


def _caching_enabled(world: LegoStarWarsTCSWorld):
    # Caching support is not implemented currently.
    return False
    # return getattr(world, "rule_caching_enabled", False)


def _common_rule_args(world: LegoStarWarsTCSWorld):
    return dict(player=world.player, caching_enabled=_caching_enabled(world))


@dataclasses.dataclass
class InLevelRule(Rule[LegoStarWarsTCSWorld], game=GAME_NAME):
    """Denotes that a rule can be used within a level, so may need combining with Extra Toggle rules."""
    def prepare_for_or_extra_toggle(self) -> Self:
        """
        Prepare this rule for OR-ing with and Extra Toggle rule, by creating a copy with default options and default
        filtered_resolution.
        """
        return dataclasses.replace(self, options=(), filtered_resolution=False)

    def make_simpler_rule(self) -> Rule:
        """Return a simpler version of this rule, intended to make it easier to extract logic for use in external
        software. Often times, this will just return the current rule, or will return the combination of rules that this
        rule will resolve to."""
        return self


@dataclasses.dataclass
class HasAbility(InLevelRule, game=GAME_NAME):
    """A rule that checks if the player has a given character ability."""

    ability: CharacterAbility | FieldResolver
    """The ability to check for."""

    def __post_init__(self):
        super().__post_init__()
        if isinstance(self.ability, CharacterAbility):
            assert self.ability.bit_count() == 1, f"Expected a single bit, but got {self.ability!r}"

    def _instantiate(self, world: LegoStarWarsTCSWorld) -> Rule.Resolved:
        resolved: int = resolve_field(self.ability, world, CharacterAbility).value

        if resolved.bit_count() == 0:
            return True_().resolve(world)

        assert resolved.bit_count() == 1
        return self.Resolved(
            resolved,
            **_common_rule_args(world)
        )

    class Resolved(Rule.Resolved):
        ability_as_int: int
        skip_cache: ClassVar[bool] = True

        @property
        def _ability_name(self) -> str:
            return CharacterAbility(self.ability_as_int).name

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # != 0 is faster than calling bool().
            return state.prog_items[self.player]["COMBINED_ABILITIES"] & self.ability_as_int != 0

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            verb = "Missing Ability " if state and not self(state) else "Has Ability "
            messages: list[JSONMessagePart] = [{"type": "text", "text": verb}]
            if state:
                color = "green" if self(state) else "salmon"
                messages.append({"type": "color", "color": color, "text": self._ability_name})
            else:
                messages.append({"type": "item_name", "flags": 0b001, "text": self._ability_name, "player": self.player})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            prefix = "Has Ability" if self(state) else "Missing Ability"
            return f"{prefix} {self._ability_name}"

        @override
        def __str__(self) -> str:
            return f"Has Ability {self._ability_name}"


@dataclasses.dataclass
class HasAllAbilities(InLevelRule, game=GAME_NAME):
    """A rule that checks if the player has all the given character abilities."""

    abilities: CharacterAbility | FieldResolver
    """The abilities to check for."""

    def _instantiate(self, world: LegoStarWarsTCSWorld) -> Rule.Resolved:
        resolved_abilities = resolve_field(self.abilities, world, CharacterAbility)

        # Simplify within this rule only.
        simplified = resolved_abilities.simplify_and()

        if simplified.bit_count() == 0:
            return True_().resolve(world)
        if simplified.bit_count() == 1:
            return HasAbility(simplified).resolve(world)
        return self.Resolved(
            simplified,
            **_common_rule_args(world)
        )

    class Resolved(Rule.Resolved):
        abilities_as_int: int
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.prog_items[self.player]["COMBINED_ABILITIES"] & self.abilities_as_int == self.abilities_as_int

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            abilities = CharacterAbility(self.abilities_as_int)
            messages: list[JSONMessagePart]
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": "all"},
                    {"type": "text", "text": " of abilities ("},
                ]
                for i, ability in enumerate(abilities):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "item_name", "flags": 0b001, "text": ability.name, "player": self.player})
                messages.append({"type": "text", "text": ")"})
                return messages

            state_abilities = CharacterAbility(state.prog_items[self.player]["COMBINED_ABILITIES"])
            found = abilities & state_abilities
            missing = abilities & ~state_abilities
            messages = [
                {"type": "text", "text": "Has " if not missing else "Missing "},
                {"type": "color", "color": "cyan", "text": "all" if not missing else "some"},
                {"type": "text", "text": " Abilities ("},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, ability in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "green", "text": ability.name})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, ability in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": ability.name})
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            abilities = CharacterAbility(self.abilities_as_int)
            state_abilities = CharacterAbility(state.prog_items[self.player]["COMBINED_ABILITIES"])
            found = abilities & state_abilities
            missing = abilities & ~state_abilities
            prefix = "Has all Abilities" if self(state) else "Missing some Abilities"
            found_str = f"Found: {found.to_readable_list()}" if found else ""
            missing_str = f"Missing: {missing.to_readable_list()}" if missing else ""
            infix = "; " if found and missing else ""
            return f"{prefix} of ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            return f"Has all Abilities ({CharacterAbility(self.abilities_as_int).to_readable_list()})"

    def __and__(self, other: "Rule[Any] | Iterable[OptionFilter] | OptionFilter") -> "Rule[TWorld]":
        if isinstance(other, OptionFilter):
            other = (other,)
        if isinstance(other, Iterable):
            if not other:
                return self
            return Filtered(self, options=other)
        if self.options == other.options:
            if isinstance(other, HasAllAbilities):
                if other.abilities in self.abilities:
                    return self
                elif self.abilities in other.abilities:
                    return other
                else:
                    return HasAllAbilities(other.abilities | self.abilities)
            if isinstance(other, HasAbility):
                if other.ability in self.abilities:
                    return self
                else:
                    return HasAllAbilities(other.ability | self.abilities)
        return super().__and__(other)


@dataclasses.dataclass
class HasAnyAbilities(InLevelRule, game=GAME_NAME):
    """A rule that checks if the player has any of the given character abilities."""

    abilities: CharacterAbility | FieldResolver
    """The abilities to check for."""

    def _instantiate(self, world: LegoStarWarsTCSWorld) -> Rule.Resolved:
        resolved_abilities = resolve_field(self.abilities, world, CharacterAbility)

        # Simplify within this rule only.
        simplified = resolved_abilities.simplify_or()

        if simplified.bit_count() == 0:
            return True_().resolve(world)
        if simplified.bit_count() == 1:
            return HasAbility(simplified).resolve(world)
        return self.Resolved(
            simplified,
            **_common_rule_args(world)
        )

    class Resolved(Rule.Resolved):
        abilities_as_int: int
        skip_cache: ClassVar[bool] = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.prog_items[self.player]["COMBINED_ABILITIES"] & self.abilities_as_int != 0

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            abilities = CharacterAbility(self.abilities_as_int)
            messages: list[JSONMessagePart]
            if state is None:
                messages = [
                    {"type": "text", "text": "Has "},
                    {"type": "color", "color": "cyan", "text": "any"},
                    {"type": "text", "text": " Ability ("},
                ]
                for i, ability in enumerate(abilities):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "item_name", "flags": 0b001, "text": ability.name, "player": self.player})
                messages.append({"type": "text", "text": ")"})
                return messages

            state_abilities = CharacterAbility(state.prog_items[self.player]["COMBINED_ABILITIES"])
            found = abilities & state_abilities
            missing = abilities & ~state_abilities
            messages = [
                {"type": "text", "text": "Has " if found else "Missing "},
                {"type": "color", "color": "cyan", "text": "any"},
                {"type": "text", "text": " Ability (" if found else " "},
            ]
            if found:
                messages.append({"type": "text", "text": "Found: "})
                for i, ability in enumerate(found):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "green", "text": ability.name})
                if missing:
                    messages.append({"type": "text", "text": "; "})

            if missing:
                messages.append({"type": "text", "text": "Missing: "})
                for i, ability in enumerate(missing):
                    if i > 0:
                        messages.append({"type": "text", "text": ", "})
                    messages.append({"type": "color", "color": "salmon", "text": ability.name})
            messages.append({"type": "text", "text": ")"})
            return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            abilities = CharacterAbility(self.abilities_as_int)
            state_abilities = CharacterAbility(state.prog_items[self.player]["COMBINED_ABILITIES"])
            found = abilities & state_abilities
            missing = abilities & ~state_abilities
            prefix = "Has any Ability" if self(state) else "Missing any Ability"
            found_str = f"Found: {found.to_readable_list()}" if found else ""
            missing_str = f"Missing: {missing.to_readable_list()}" if missing else ""
            infix = "; " if found and missing else ""
            return f"{prefix} of ({found_str}{infix}{missing_str})"

        @override
        def __str__(self) -> str:
            return f"Has any Ability ({CharacterAbility(self.abilities_as_int).to_readable_list()})"


@dataclasses.dataclass
class HasSingleJumpDistance(InLevelRule, game=GAME_NAME):
    """A rule that checks if the player has any character with the specified jump distance, or greater, up to the
    maximum single-jump distance of 0.92."""
    distance: float

    def __post_init__(self):
        super().__post_init__()
        if self.distance <= 0:
            raise ValueError("distance must be greater than 0")
        if self.distance > 0.92:
            raise ValueError("distance must be less than or equal to 0.92")

    def _instantiate(self, world: LegoStarWarsTCSWorld) -> Rule.Resolved:
        return self.make_simpler_rule().resolve(world)

    def make_simpler_rule(self) -> Rule:
        return self.static_make_simpler_rule(
            self.distance, options=self.options, filtered_resolution=self.filtered_resolution)

    @staticmethod
    def static_make_simpler_rule(distance: float, *, options=(), filtered_resolution=False) -> Rule:
        if distance <= NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA[Character.BOBA_FETT_BOY].single_jump_distance:
            return HasAbility(CharacterAbility.CAN_BARELY_JUMP)
        if distance <= 0.69:
            base_ability = CharacterAbility.CAN_JUMP_DISTANCE_0_69
            max_distance_exclusive = 0.69
        elif distance <= 0.84:
            base_ability = CharacterAbility.CAN_JUMP_DISTANCE_0_84
            max_distance_exclusive = 0.84
        elif distance <= 0.92:
            base_ability = CharacterAbility.CAN_JUMP_DISTANCE_0_92
            max_distance_exclusive = 0.92
        else:
            raise ValueError(
                f"Tried to create rule for distance greater than 0.92, but the furthest regular single-jump is"
                f" 0.92. Use ")

        all_characters = []
        for jump_distance, characters in SORTED_SINGLE_JUMP_DISTANCE_TO_CHARACTERS.items():
            if jump_distance >= max_distance_exclusive:
                # The `base_ability` covers all other characters that can jump this distance.
                break
            if jump_distance >= distance:
                all_characters.extend(characters)

        if all_characters:
            return Or(
                HasAbility(base_ability),
                Character.has_any(*all_characters),
                options=options,
                filtered_resolution=filtered_resolution,
            )
        else:
            return HasAbility(base_ability, options=options, filtered_resolution=filtered_resolution)


@dataclasses.dataclass
class HasAbilityCombination(InLevelRule, game=GAME_NAME):
    """A rule that checks if the player has any character with any of the given combinations of abilities.

    Typically only a single ability combination will be needed, but multiple can be provided.

    This is often an expensive rule, but is rarely used rule for cases where it is not worth defining a new ability just
    for a specific use case."""
    ability_combinations: tuple[CharacterAbility, ...] | FieldResolver

    def __init__(self,
                 *ability_combinations: CharacterAbility | FieldResolver,
                 options: Iterable[OptionFilter] = (),
                 filtered_resolution: bool = False
                 ):
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        found_resolver = False
        found_abilities = False
        for v in ability_combinations:
            if isinstance(v, FieldResolver):
                if found_resolver:
                    raise ValueError("Only specify at most one FieldResolver")
                found_resolver = True
            if isinstance(v, CharacterAbility):
                found_abilities = True
        if found_abilities and found_resolver:
            raise ValueError("Cannot specify abilities and field resolvers simultaneously.")

        if found_resolver:
            self.ability_combinations = ability_combinations[0]
        else:
            self.ability_combinations = ability_combinations

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        abilities = resolve_field(self.ability_combinations, world, tuple)

        return self.static_make_simpler_rule(*abilities).resolve(world)

    @override
    def make_simpler_rule(self) -> Rule:
        if isinstance(self.ability_combinations, FieldResolver):
            return self
        else:
            return self.static_make_simpler_rule(*self.ability_combinations)

    @staticmethod
    def simplify_contained_combinations(combinations: list[CharacterAbility]):
        """
        HasAbilityCombination(HIGH_JUMP | JEDI, HIGH_JUMP | JEDI | SITH)
        can be reduced to HasAbilityCombination(HIGH_JUMP | JEDI)
        :param combinations:
        :return:
        """
        if len(combinations) <= 1:
            # Nothing to do.
            return combinations
        simplified_combinations = []
        while combinations:
            combination = combinations.pop()
            for other_combinations in (simplified_combinations, combinations):
                for other_combination in other_combinations:
                    if other_combination in combination:
                        break
                else:
                    continue
                # Propagate the inner break.
                break
            else:
                # No inner break, so no other combination is present in `combination`
                simplified_combinations.append(combination)
        return simplified_combinations

    @staticmethod
    def static_make_simpler_rule(*combinations: CharacterAbility) -> Rule:
        if not combinations:
            return False_()

        simplified_combinations = HasAbilityCombination.simplify_contained_combinations(list(combinations))

        # Remove abilities implied by another ability that is requested in that combination.
        # e.g. (JEDI | CAN_MELEE) can be reduced to just (JEDI)
        simplified_combinations = [combination.simplify_combination() for combination in simplified_combinations]

        # Simplify contained combinations again.
        simplified_combinations = HasAbilityCombination.simplify_contained_combinations(simplified_combinations)

        reduced_to_single_bit = []
        still_multiple_bits = []
        for combination in simplified_combinations:
            if combination.bit_count() > 1:
                still_multiple_bits.append(combination)
            else:
                reduced_to_single_bit.append(combination)

        any_rules = []

        if reduced_to_single_bit:
            if len(reduced_to_single_bit) == 1:
                any_rules.append(HasAbility(reduced_to_single_bit[0]))
            else:
                any_rules.append(HasAnyAbilities(reduce(or_, reduced_to_single_bit)))

        if still_multiple_bits:
            def get_rough_rule_cost(rule: Rule) -> float:
                if isinstance(rule, HasAny):
                    return len(rule.item_names) * 0.5
                elif isinstance(rule, HasAll):
                    return len(rule.item_names) * 0.75
                elif isinstance(rule, Or):
                    return sum(map(get_rough_rule_cost, rule.children)) * 0.5
                elif isinstance(rule, And):
                    return sum(map(get_rough_rule_cost, rule.children)) * 0.75
                else:
                    return 1

            # First try rules based on HasAbilityExceptCharacters
            best_ability_except_rules = []
            for combination in still_multiple_bits:
                ability_except_rule_attemps: list[Rule] = []
                main_ability: CharacterAbility
                for main_ability in combination:
                    other_abilities = combination & ~main_ability
                    excluded_characters: set[Character] = set()
                    # Make sure to include Extra Toggle characters in the exclusions.
                    for character_data in CHARACTER_TO_ITEM_DATA.values():
                        if main_ability in character_data.abilities and other_abilities not in character_data.abilities:
                            excluded_characters.add(character_data.character)
                    ability_except_rule = HasAbilityExceptCharacters.static_make_rule(main_ability, excluded_characters)
                    ability_except_rule_attemps.append(ability_except_rule)

                # todo: I think these rules might always be the same due to optimisations HasAbilityExceptCharacters
                #  already does..
                best_rule = ability_except_rule_attemps[0]
                best_rule_cost = get_rough_rule_cost(best_rule)
                for rule in ability_except_rule_attemps[1:]:
                    rule_cost = get_rough_rule_cost(rule)
                    if rule_cost < best_rule_cost:
                        best_rule = rule
                        best_rule_cost = rule_cost
                best_ability_except_rules.append(best_rule)

            if len(best_ability_except_rules) == 1:
                best_ability_except_rule = best_ability_except_rules[0]
            else:
                best_ability_except_rule = Or(*best_ability_except_rules)

            # Try a different kind of rule that can encompass all supplied combinations.
            all_matching_characters: set[str] = set()
            common_abilities_for_each_combination: list[CharacterAbility] = []
            for combination in still_multiple_bits:
                common_abilities = ~CharacterAbility.NONE
                # Find all characters with this ability combination.
                # Extra Toggle characters are ignored because they are never collected into a state.
                for character in NORMAL_CHARACTER_TO_ITEM_DATA.values():
                    if combination in character.abilities:
                        # If there are some single bits to check for, then all characters with those single bits can be
                        # ignored because that single bit would match before needing to check for the character being in
                        # the state.
                        if not reduced_to_single_bit or not any(single_bit for single_bit in reduced_to_single_bit):
                            all_matching_characters.add(character.name)
                            common_abilities &= character.abilities
                if common_abilities is not ~CharacterAbility.NONE:
                    common_abilities_for_each_combination.append(common_abilities)

            # todo: Create a False_() rule when no matching characters.
            characters_rule = HasAny(*all_matching_characters)

            # If there are lots of characters that match this, check for having any of the common abilities of each
            # set of characters that have one of the combinations of abilities.
            # characters
            # because that is a faster check.
            if len(all_matching_characters) >= 8 and common_abilities_for_each_combination:
                abilities_rules = []
                for common_abilities_for_combination in common_abilities_for_each_combination:
                    abilities_rules.append(HasAllAbilities(common_abilities_for_combination))
                if abilities_rules:
                    characters_rule = And(Or(*abilities_rules), characters_rule)

            if get_rough_rule_cost(best_ability_except_rule) < get_rough_rule_cost(characters_rule):
                any_rules.append(best_ability_except_rule)
            else:
                any_rules.append(characters_rule)
        return Or(*any_rules) if len(any_rules) != 1 else any_rules[0]


@dataclasses.dataclass
class HasAbilityExceptCharacters(InLevelRule, game=GAME_NAME):
    """A rule that checks if the player has any character with the given ability, except the given characters.

    This is an expensive, but rarely used rule for cases where specific characters cannot use their abilities in
    specific cases, where adding a new CharacterAbility to represent this difference in ability is not worth it.
    """
    ability: CharacterAbility | FieldResolver
    """The ability to check for. CharacterAbility.NONE is allowed."""

    except_characters: AbstractSet[Character] | FieldResolver
    """The characters excluded from this rule."""

    def __init__(
            self,
            ability: CharacterAbility | FieldResolver,
            *except_characters: Character,
            options: Iterable[OptionFilter] = (),
            filtered_resolution: bool = False,
    ):
        super().__init__(options=options, filtered_resolution=filtered_resolution)
        self.ability = ability
        for character in except_characters:
            if character not in CHARACTER_TO_ITEM_DATA:
                raise Exception(f"Item data for Character '{character!r}' does not exist.")
        self.except_characters = set(except_characters)

    @override
    def make_simpler_rule(self) -> Rule:
        if isinstance(self.ability, FieldResolver) or isinstance(self.except_characters, FieldResolver):
            return self
        return self.static_make_rule(self.ability, self.except_characters)

    @override
    def prepare_for_or_extra_toggle(self) -> "HasAbilityExceptCharacters":
        if isinstance(self.except_characters, FieldResolver):
            raise Exception(f"Fields Resolvers are not supported by prepare_for_or_extra_toggle. FieldResolver"
                            f" {self.except_characters} on {self}")
        return HasAbilityExceptCharacters(self.ability, *self.except_characters)

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        required_ability = resolve_field(self.ability, world, CharacterAbility)
        if required_ability.bit_count() == 0:
            # This would otherwise mean any character except certain characters.
            raise Exception("An ability must be required.")
        if required_ability.bit_count() > 1:
            raise Exception(f"Only a single ability should be required, but got {self.ability.name}")

        except_characters = set(resolve_field(self.except_characters, world, Iterable))

        return self.static_make_rule(required_ability, except_characters).resolve(world)

    @override
    def to_dict(self) -> dict[str, Any]:
        if isinstance(self.except_characters, FieldResolver) or isinstance(self.ability, FieldResolver):
            return super().to_dict()
        else:
            return self.static_make_rule(self.ability, self.except_characters).to_dict()
            # data = super().to_dict()
            # # sets are not allowed.
            # data["args"]["except_characters"] = list(data["args"]["except_characters"])
            # return data

    @staticmethod
    def static_make_rule(required_ability: CharacterAbility, except_characters: AbstractSet[Character]) -> Rule:
        if not except_characters:
            return HasAbility(required_ability)

        except_characters_abilities: CharacterAbility = CharacterAbility.NONE
        for character in except_characters:
            # Extra Toggle characters are allowed in the exclusions to make sure they cannot be allowed due to their
            # abilities when automatically adding Extra Toggle rules, but they otherwise do not need to be considered by
            # the rule.
            if character in NORMAL_CHARACTER_TO_ITEM_DATA:
                except_characters_abilities |= NORMAL_CHARACTER_TO_ITEM_DATA[character].abilities
            elif character not in EXTRA_TOGGLE_CHARACTER_TO_ITEM_DATA:
                raise KeyError(f"No item data found for Character {character!r} found.")
        if (CharacterAbility.ALL_VEHICLE_ABILITIES & except_characters_abilities
                and (~CharacterAbility.ALL_VEHICLE_ABILITIES) & except_characters_abilities):
            raise ValueError(f"The characters to except from the rule cannot be both vehicle and non-vehicle"
                             f" characters, but got {sorted(except_characters)}")

        usable_implied_by_abilities_to_characters: dict[CharacterAbility, set[Character]]
        include_characters: set[Character] = set()
        if required_ability is CharacterAbility.NONE:
            if CharacterAbility.IS_A_VEHICLE in except_characters_abilities:
                all_abilities = CharacterAbility.ALL_VEHICLE_ABILITIES
                character_data_collection = VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA
            else:
                all_abilities = ~CharacterAbility.ALL_VEHICLE_ABILITIES
                character_data_collection = NON_VEHICLE_NORMAL_CHARACTER_TO_ITEM_DATA

            usable_abilities = ~except_characters_abilities & all_abilities

            usable_implied_by_abilities_to_characters = {
                ability: set() for ability in usable_abilities
            }
            include_characters_abilities = ~CharacterAbility.NONE
            for character_data in character_data_collection.values():
                if character_data.character not in except_characters:
                    include_characters_abilities &= character_data.abilities
                    include_characters.add(character_data.character)
                    for ability in (character_data.abilities & usable_abilities):
                        usable_implied_by_abilities_to_characters[ability].add(character_data.character)
        else:
            usable_implied_by_abilities = CharacterAbility.NONE
            for ability in IMPLIED_BY_ABILITIES.get(required_ability, ()):
                if ability not in except_characters_abilities:
                    usable_implied_by_abilities |= ability

            usable_implied_by_abilities_to_characters = {
                ability: set() for ability in usable_implied_by_abilities
            }
            include_characters_abilities = ~CharacterAbility.NONE
            for character_data in NORMAL_CHARACTER_TO_ITEM_DATA.values():
                if required_ability in character_data.abilities and character_data.character not in except_characters:
                    include_characters_abilities &= character_data.abilities
                    include_characters.add(character_data.character)
                    for ability in (character_data.abilities & usable_implied_by_abilities):
                        usable_implied_by_abilities_to_characters[ability].add(character_data.character)

        if not include_characters:
            return False_()

        if len(include_characters) == 1:
            return next(iter(include_characters)).has()

        # todo: I don't know if this is useful, it hasn't managed to do anything so far.
        # abilities_included_characters_all_have_but_except_characters_do_not = (
        #         include_characters_abilities & ~include_characters_abilities
        # )
        #
        # if abilities_included_characters_all_have_but_except_characters_do_not is not CharacterAbility.NONE:
        #     all_shared_unique = abilities_included_characters_all_have_but_except_characters_do_not | required_ability
        #     simplified = all_shared_unique.simplify_combination()
        #     if simplified.bit_count() == 1:
        #         raise Exception("actually did something")
        #         return HasAbility(simplified)
        #
        #     if abilities_included_characters_all_have_but_except_characters_do_not.bit_count() > 1:
        #         # Try simplifying pairs of abilities.
        #         for included_ability in abilities_included_characters_all_have_but_except_characters_do_not:
        #             pair = included_ability | required_ability
        #             simplified = pair.simplify_combination()
        #             if simplified.bit_count() == 1:
        #                 raise Exception("actually did something 2")
        #                 return HasAbility(simplified)

        has_any_implied_by_abilities = CharacterAbility.NONE
        if any(usable_implied_by_abilities_to_characters.values()):
            # Some characters can be replaced with HasAnyAbilities instead of including them each in a HasAny.
            most_common_last: list[tuple[CharacterAbility, set[Character]]]
            most_common_last = sorted(usable_implied_by_abilities_to_characters.items(), key=lambda t: len(t[1]))
            while True:
                most_common_ability, characters_with_ability = most_common_last.pop()
                has_any_implied_by_abilities |= most_common_ability
                # Remove these character from needing to be checked individually in a HasAny
                include_characters.difference_update(characters_with_ability)

                # Remove characters that are now accounted for by an ability.
                for t in most_common_last:
                    t[1].difference_update(characters_with_ability)
                most_common_last = sorted((t for t in most_common_last if t[1]), key=lambda t: len(t[1]))
                if not most_common_last:
                    break

            if has_any_implied_by_abilities.bit_count() == 1:
                any_abilities_rule = HasAbility(has_any_implied_by_abilities)
            else:
                any_abilities_rule = HasAnyAbilities(has_any_implied_by_abilities)

            if not include_characters:
                # All included characters could be specified using only abilities that the excluded characters don't
                # have.
                return any_abilities_rule
            else:
                if len(include_characters) >= 8 and required_ability is not CharacterAbility.NONE:
                    return HasAbility(required_ability) & (any_abilities_rule | Character.has_any(*include_characters))
                else:
                    return any_abilities_rule | Character.has_any(*include_characters)
        else:
            if len(include_characters) >= 8 and required_ability is not CharacterAbility.NONE:
                # If there are lots of characters that match this, check for having all the required abilities first
                # because that is a faster check.
                return HasAbility(required_ability) & Character.has_any(*include_characters)
            else:
                return Character.has_any(*include_characters)


@dataclasses.dataclass
class HasAnyCharacterExcept(HasAbilityExceptCharacters, game=GAME_NAME):
    def __init__(
            self,
            *except_characters: Character,
            options: Iterable[OptionFilter] = (),
            filtered_resolution: bool = False,
    ):
        super().__init__(
            CharacterAbility.NONE,
            *except_characters,
            options=options,
            filtered_resolution=filtered_resolution
        )

    @override
    def prepare_for_or_extra_toggle(self) -> "HasAnyCharacterExcept":
        if isinstance(self.except_characters, FieldResolver):
            raise Exception(f"Unexpected field resolver for .except_characters on {self}")
        return HasAnyCharacterExcept(*self.except_characters)

    @override
    def _instantiate(self, world: TWorld) -> Rule.Resolved:
        if self.ability is not CharacterAbility.NONE:
            raise Exception(f"Ability should always be CharacterAbility.NONE, but got {self.ability!r}")

        except_characters = set(resolve_field(self.except_characters, world, Iterable))

        return self.static_make_rule(CharacterAbility.NONE, except_characters).resolve(world)



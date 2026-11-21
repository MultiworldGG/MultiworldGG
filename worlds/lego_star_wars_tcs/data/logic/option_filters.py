from dataclasses import dataclass
from operator import and_, or_
from typing import TYPE_CHECKING, Literal, Any
from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Rule, TWorld, Or, WrapperRule
from rule_builder.options import OptionFilter

from ...constants import GAME_NAME
from ...options import LogicDifficulty, UncapOriginalTrilogyHighJump


if TYPE_CHECKING:
    from ... import LegoStarWarsTCSWorld
else:
    LegoStarWarsTCSWorld = TWorld


OT_HIGH_JUMP_ENABLED = OptionFilter(UncapOriginalTrilogyHighJump, True)
OT_HIGH_JUMP_DISABLED = OptionFilter(UncapOriginalTrilogyHighJump, False)


def ot_high_jump_ternary(uncapped: Rule, capped: Rule) -> Rule:
    return Or(
        uncapped & OT_HIGH_JUMP_ENABLED,
        capped & OT_HIGH_JUMP_DISABLED,
    )


DifficultySpecifier = Literal[
    "base",
    "base+",
    "normal",
    "normal+",
    "moderate",
    "moderate+",
    "hard",
    "hard+",
]

_DIFFICULTIES = (
    "base",
    "normal",
    "moderate",
    "hard",
)

_PLUS_DIFFICULTY_TO_SLICE = {
    "base+": slice(0, None),
    "normal+": slice(1, None),
    "moderate+": slice(2, None),
    "hard+": slice(3, None),
}


@dataclass
class UTGlitchesRule(WrapperRule[LegoStarWarsTCSWorld], game=GAME_NAME):
    glitches: Rule
    all_glitches: Rule = None

    def __post_init__(self):
        super().__post_init__()
        if self.all_glitches is None:
            self.all_glitches = self.glitches

    def _instantiate(self, world: LegoStarWarsTCSWorld) -> Rule.Resolved:
        if not world.is_universal_tracker():
            return self.child.resolve(world)
        return self.Resolved(
            child=self.child.resolve(world),
            glitches=self.glitches.resolve(world),
            all_glitches=self.all_glitches.resolve(world),
            glitches_item_name=world.glitches_item_name,
            all_glitches_item_name=world.glitches_all_item_name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(WrapperRule.Resolved):
        """This class should only ever be instantiated when generation is occurring under Universal Tracker."""
        glitches: Rule.Resolved
        all_glitches: Rule.Resolved
        glitches_item_name: str
        all_glitches_item_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            # When the glitches item is collected, all previously accessible locations should still be accessible (if
            # not, then there is a logic bug).
            # Lower logic difficulties may require a certain item to reach a region, so locations within that region,
            # that require that item, do not need to require that certain item. However, in higher logic difficulties,
            # that certain item may not be required to reach the region, so the locations within the region have to have
            # rules set to require that certain item.
            # This means that when the glitches item is in the state, logic must not be allowed to use the logic rules
            # from a lower logic difficulty.
            if state.has(self.glitches_item_name, self.player):
                if state.has(self.all_glitches_item_name, self.player):
                    return self.all_glitches(state)
                else:
                    return self.glitches(state)
            else:
                return self.child(state)

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return self.child.explain_json()
            else:
                messages: list[JSONMessagePart]
                messages = self.child.explain_json(state).copy()
                if self.glitches is not self.child:
                    messages.append({"type": "text", "text": "\nWith "})
                    messages.append({"type": "color", "text": "Glitches", "color": "yellow"})
                    messages.append({"type": "text", "text": ": "})
                    messages.append({"type": "color", "text": "(", "color": "yellow"})
                    messages.extend(self.glitches.explain_json(state))
                    messages.append({"type": "color", "text": ")", "color": "yellow"})
                if self.all_glitches is not self.glitches and state.has(self.all_glitches_item_name, self.player):
                    messages.append({"type": "text", "text": "\nWith "})
                    messages.append({"type": "color", "text": "All Glitches", "color": "yellow"})
                    messages.append({"type": "text", "text": ": "})
                    messages.append({"type": "color", "text": "(", "color": "yellow"})
                    messages.extend(self.all_glitches.explain_json(state))
                    messages.append({"type": "color", "text": ")", "color": "yellow"})
                return messages

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return self.child.explain_str()
            else:
                s = f"({self.child.explain_str(state)})"
                # Include either self.all_glitches or self.glitches depending on whether all_glitches_item_name is in
                # the state.
                if state.has(self.all_glitches_item_name, self.player):
                    if self.all_glitches is not self.child:
                        s += f" | AllGlitches({self.all_glitches.explain_str(state)})"
                else:
                    if self.glitches is not self.child:
                        return s + f" | Glitches({self.glitches.explain_str(state)})"
                return s

        @override
        def __str__(self):
            s = f"({self.child})"
            if self.glitches is not self.child:
                s += f" | Glitches({self.glitches})"
            if self.all_glitches is not self.glitches:
                s += f" | AllGlitches({self.all_glitches})"
            return s


def ut_glitched_rule(normal_rule: Rule, glitched_rule: Rule):
    """This small helper function gives kwargs that are easier to understand, rather than 'child' being used for the
    normal rule when instantiating a UTGlitchesRule directly. This also hides the `all_glitches` rule argument, which is
    currently only relevant for Logic Difficulty rules."""
    return UTGlitchesRule(normal_rule, glitched_rule)


@dataclass
class LogicOptions(Rule[LegoStarWarsTCSWorld], game=GAME_NAME):
    base: Rule[TWorld]
    normal: Rule[TWorld]
    moderate: Rule[TWorld]
    hard: Rule[TWorld]

    @override
    def _instantiate(self, world: LegoStarWarsTCSWorld) -> Rule.Resolved:
        logic_difficulty = world.options.logic_difficulty
        # Universal Tracker glitched logic is currently enabled in an awkward way because a lower logic difficulty may
        # not be able to reach a region without a certain item, meaning that some locations within that region do not
        # need a rule assigned, but a higher logic difficulty may be able to reach that region without that item, so in
        # higher logic some locations within that region do need rules assigned. UT glitched logic was taking the most
        # logically open of both, and ignoring the fact that lower logic locations should only be accessible when lower
        # logic entrances have been used.
        if logic_difficulty == LogicDifficulty.option_none:
            if world.is_universal_tracker() and (self.base is not self.normal or self.base is not self.hard):
                return UTGlitchesRule(self.base, self.normal, self.hard).resolve(world)
            rule = self.base
        elif logic_difficulty == LogicDifficulty.option_normal:
            if world.is_universal_tracker() and (self.normal is not self.moderate or self.normal is not self.hard):
                return UTGlitchesRule(self.normal, self.moderate, self.hard).resolve(world)
            rule = self.normal
        elif logic_difficulty == LogicDifficulty.option_moderate:
            if world.is_universal_tracker() and self.moderate is not self.hard:
                return UTGlitchesRule(self.moderate, self.hard).resolve(world)
            rule = self.moderate
        elif logic_difficulty == LogicDifficulty.option_hard:
            # Hard is the maximum logic difficulty currently.
            rule = self.hard
        else:
            raise Exception(f"Unrecognised logic difficulty {logic_difficulty}")
        return rule.resolve(world)

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        del data["args"]
        data["base"] = self.base.to_dict()
        data["normal"] = self.normal.to_dict()
        data["moderate"] = self.moderate.to_dict()
        data["hard"] = self.hard.to_dict()
        return data

    def _apply_rule_op(self,
                       rule: Rule,
                       op: Literal[and_, or_],
                       apply_to: DifficultySpecifier | None = None,
                       reverse_order: bool = False) -> "LogicOptions":
        if apply_to is None:
            # Not a necessary optimisation, but saves having to create extra intermediary LogicOptions instances.
            if isinstance(rule, LogicOptions):
                if reverse_order:
                    first_args = (rule.base, rule.normal, rule.moderate, rule.hard)
                    second_args = (self.base, self.normal, self.moderate, self.hard)
                else:
                    first_args = (self.base, self.normal, self.moderate, self.hard)
                    second_args = (rule.base, rule.normal, rule.moderate, rule.hard)
                applied = []
                last_first_arg = None
                last_second_arg = None
                last_applied = None
                for first_arg, second_arg in zip(first_args, second_args):
                    # If the arguments have not changed, use the previous result.
                    if first_arg is not last_first_arg or second_arg is not last_second_arg:
                        last_applied = op(first_arg, second_arg)
                    applied.append(last_applied)
                    last_first_arg = first_arg
                    last_second_arg = second_arg
                return LogicOptions(*applied)
            else:
                # Apply to all.
                apply_to = "base+"

        if apply_to.endswith("+"):
            # TODO: When either argument is LogicOptions, try to deduplicate when `base is normal` etc.
            slice_to_use = _PLUS_DIFFICULTY_TO_SLICE[apply_to]
            difficulty_names = _DIFFICULTIES[slice_to_use]
            logic = self
            for difficulty_name in difficulty_names:
                logic = logic._apply_rule_op(rule, op, difficulty_name, reverse_order)
            return logic

        if isinstance(rule, LogicOptions):
            rule = getattr(rule, apply_to)

        if apply_to == "base":
            return LogicOptions(
                op(rule, self.base) if reverse_order else op(self.base, rule),
                self.normal,
                self.moderate,
                self.hard,
            )
        elif apply_to == "normal":
            return LogicOptions(
                self.base,
                op(rule, self.normal) if reverse_order else op(self.normal, rule),
                self.moderate,
                self.hard,
            )
        elif apply_to == "moderate":
            return LogicOptions(
                self.base,
                self.normal,
                op(rule, self.moderate) if reverse_order else op(self.moderate, rule),
                self.hard,
            )
        elif apply_to == "hard":
            return LogicOptions(
                self.base,
                self.normal,
                self.moderate,
                op(rule, self.hard) if reverse_order else op(self.hard, rule),
            )
        raise ValueError(f"Unexpected apply_to {apply_to}")

    def and_rule(self,
                 rule: Rule,
                 apply_to: DifficultySpecifier | None = None) -> "LogicOptions":
        return self._apply_rule_op(rule, and_, apply_to)

    def rand_rule(self,
                  rule: Rule,
                  apply_to: DifficultySpecifier | None = None) -> "LogicOptions":
        return self._apply_rule_op(rule, and_, apply_to, reverse_order=True)

    def or_rule(self,
                rule: Rule,
                apply_to: DifficultySpecifier | None = None) -> "LogicOptions":
        return self._apply_rule_op(rule, or_, apply_to)

    def ror_rule(self,
                 rule: Rule,
                 apply_to: DifficultySpecifier | None = None) -> "LogicOptions":
        return self._apply_rule_op(rule, or_, apply_to, reverse_order=True)

    # I'm not sure if pre-applying __and__/__or__ like this helps with performance when initialising rules.
    # def __and__(self, other):
    #     return self.and_rule(other)
    #
    # def __or__(self, other):
    #     return self.or_rule(other)


def logic_options(
        base: Rule[TWorld],
        normal: Rule[TWorld] | None = None,
        moderate: Rule[TWorld] | None = None,
        hard: Rule[TWorld] | None = None,
        *, strict: bool = True,
) -> LogicOptions[TWorld]:
    base_rule = base

    if normal is None:
        normal = base
        normal_rule = base
    else:
        normal_rule = normal

    if moderate is None:
        moderate = normal
        moderate_rule = normal
    else:
        moderate_rule = moderate

    if hard is None:
        # hard = moderate
        hard_rule = moderate
    else:
        hard_rule = hard

    if strict and hard_rule is moderate_rule and hard_rule is normal_rule and hard_rule is base_rule:
        # This is not really a problem, but it could indicate an issue elsewhere if all the provided rules are the same.
        raise Exception("All rules are the same. Maybe don't use logic_options.")

    assert isinstance(base_rule, Rule)
    assert isinstance(normal_rule, Rule)
    assert isinstance(moderate_rule, Rule)
    assert isinstance(hard_rule, Rule)

    return LogicOptions(base_rule, normal_rule, moderate_rule, hard_rule)

import math
from typing import TYPE_CHECKING, Callable, Union

from BaseClasses import CollectionState

if TYPE_CHECKING:
    from . import D3DWorld


class Rule(object):
    def __call__(self, state: CollectionState) -> bool:
        raise NotImplementedError

    def __or__(self, other: "Rule") -> "Rule":
        # short circuit
        if isinstance(other, RuleTrue):
            return other
        if isinstance(other, RuleFalse):
            return self
        return LambdaRule(lambda state: self(state) or other(state))

    def __and__(self, other: "Rule") -> "Rule":
        # short circuit
        if isinstance(other, RuleTrue):
            return self
        if isinstance(other, RuleFalse):
            return other
        return LambdaRule(lambda state: self(state) and other(state))


RULETYPE = Union[Rule, Callable[[CollectionState], bool]]


class LambdaRule(Rule):
    def __init__(self, func):
        self._func = func

    def __call__(self, state: dict) -> bool:
        return self._func(state)


class RuleTrue(Rule):
    def __call__(self, state: CollectionState) -> bool:
        return True

    def __or__(self, other: "Rule") -> "Rule":
        return self

    def __and__(self, other: "Rule") -> "Rule":
        return other


class RuleFalse(Rule):
    def __call__(self, state: CollectionState) -> bool:
        return False

    def __or__(self, other: "Rule") -> "Rule":
        return other

    def __and__(self, other: "Rule") -> "Rule":
        return self


class Rules(object):
    def __init__(self, world: "D3DWorld"):
        player = world.player

        self.true = RuleTrue()
        self.false = RuleFalse()

        class HasRule(Rule):
            def __init__(self, prop: str):
                self.prop = prop

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has(self.prop, player)

        self.has = HasRule

        class HasGroupRule(Rule):
            def __init__(self, prop: str):
                self.prop = prop

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has_group(self.prop, player)

        self.has_group = HasGroupRule

        class CountRule(Rule):
            def __init__(self, prop: str, count: int):
                self.prop = prop
                self.count = count

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has(self.prop, player, self.count)

        self.count = CountRule

        class CountGroupRule(Rule):
            def __init__(self, prop: str, count: int):
                self.prop = prop
                self.count = count

            def __call__(self, state: CollectionState) -> bool:
                # something based on world, whatever
                return state.has_group(self.prop, player, self.count)

        self.count_group = CountGroupRule

        if world.options.unlock_abilities:
            self.can_jump = HasRule("Jump")
            self.can_crouch = HasRule("Crouch")
            self.can_dive = HasRule("Dive") | HasGroupRule("Scuba Gear")
            self.can_sprint = HasRule("Sprint")
        else:
            self.can_jump = self.true
            self.can_crouch = self.true
            self.can_sprint = self.true
            self.can_dive = self.true
        if world.options.unlock_interact:
            self.can_open = HasRule("Open")
            self.can_use = HasRule("Use")
        else:
            self.can_open = self.true
            self.can_use = self.true
        self.can_shrink = (
            self.true
        )  # Might make this an ability at some point, a bit narrow in scope

        class CanJetPack(Rule):
            def __init__(self, fuel: int):
                self.fuel = fuel
                self.required = math.ceil(
                    self.fuel / float(world.fuel_per_pickup["Jetpack"])
                )

            def __call__(self, state: CollectionState) -> bool:
                return state.has_group("Jetpack", player) and state.has_group(
                    "Jetpack Capacity", player, self.required
                )

        self.jetpack = CanJetPack

        self.jump = self.can_jump | self.jetpack(50)
        """Any simple jump sequence that doesn't consume a lot of jetpack"""

        class CanDiveTo(Rule):
            def __init__(self, fuel: int):
                self.fuel = fuel
                self.required = math.ceil(
                    self.fuel / float(world.fuel_per_pickup["Scuba Gear"])
                )

            def __call__(self, state: CollectionState) -> bool:
                return state.has_group("Scuba Gear Capacity", player, self.required)

        if world.options.unlock_abilities:
            self.dive = lambda fuel: self.can_dive & CanDiveTo(fuel)
            """For chained sequences of dives, where scuba capacity matters for accessibility"""
        else:
            self.dive = lambda x: self.true

        self.steroids = HasGroupRule("Steroids")
        # Steroids act as an alternative source for sprinting
        self.sprint = self.can_sprint | self.steroids
        self.fast_sprint = self.can_sprint & self.steroids

        difficulty_map = {"easy": 0, "medium": 1, "hard": 2, "extreme": 3}
        self.difficulty = lambda difficulty: (
            self.true
            if difficulty_map.get(difficulty, 0) <= world.options.logic_difficulty
            else self.false
        )

        self.sr50 = self.sprint | self.difficulty("hard")

        self.explosives = self.has_group("Explosives")
        # This is technically not correct because some of them provide more capacity, so this is stricter than it
        # needs to be for now, ToDo
        self.explosives_count = lambda count: self.count_group("Explosives", count)

        # Glitched logic stuff
        if world.options.glitch_logic:
            self.glitched = RuleTrue()
        else:
            self.glitched = RuleFalse()
        # Most clips require run speed
        self.crouch_jump = self.glitched & self.can_jump & self.can_crouch & self.sprint
        self.fast_crouch_jump = (
            self.glitched
            & self.can_jump
            & self.can_crouch
            & self.can_sprint
            & self.steroids
        )
        # Kicks can activate walls with a lotag set, which is the case for multi-part doors. This allows bypassing
        # some lock checks
        # Kicks still require Use to activate switches
        self.glitch_kick = self.glitched & self.can_use

        # Some simplifications for progressive items
        self.rpg = self.has_group("RPG")
        self.pipebomb = self.has_group("Pipebomb")
        self.devastator = self.has_group("Devastator")
        self.tripmine = self.has_group("Tripmine")

        # General Stuff
        self.level = lambda level_cls: HasRule(level_cls.unlock)

        # Boss kill logic, difficulty dependant
        self.can_kill_boss_1 = self.rpg  # Enough RPG Ammo for a kill in the room
        self.can_kill_boss_2 = (
            self.rpg & self.devastator
        )  # Should have enough ammo in the room, I think?
        # can jump on goal post and have boss suicide on splash damage, or blimp spawns enough ammo
        self.can_kill_boss_3 = (
            self.rpg
            | self.devastator
            | (
                self.difficulty("medium")
                & ((self.can_jump & self.sprint) | self.jetpack(50))
            )
        )
        # 30 RPG Ammo required. Giving the player some scuba gear requirement for this check as air can be tight
        # Also requiring devastator access. Will need to figure out ammo later as the fight doesn't provide any
        self.can_kill_boss_4 = self.dive(400) & self.rpg & self.devastator

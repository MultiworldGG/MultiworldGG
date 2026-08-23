from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import CanReachRegion, Has, HasFromList, Rule, And, HasAll

from . import items
from .items import GOAL_LEVEL
from .locations import LOCATION_DATA, get_excluded_locations, is_minigame_location, level_item_name
from .options import RankCheckDifficulty


if TYPE_CHECKING:
    from .world import UncannyCatWorld

@dataclass
class OutOfLogic(Rule["UncannyCatWorld"], game="Uncanny Cat Golf"):
    description: str

    class Resolved(Rule.Resolved):
        glitches_item_name: str
        player: int
        description: str
        skip_cache = True

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return state.has(self.glitches_item_name, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.glitches_item_name: {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [{"text": f"Glitch: {self.description}", "color": "magenta"}]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            return f"Glitch: {self.description}"

    @override
    def _instantiate(self, world: "UncannyCatWorld") -> "OutOfLogic.Resolved":
        return OutOfLogic.Resolved(
            glitches_item_name=world.glitches_item_name,
            player=world.player,
            description=self.description,
        )

def set_all_rules(world: UncannyCatWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def gimmick_rule(requirements: list[str]) -> Rule[UncannyCatWorld] | None:
    """Turn a requirement list into one rule. "A|B is just an OR."""
    all_of = [req for req in requirements if "|" not in req]
    either_of = [HasFromList(*req.split("|")) for req in requirements if "|" in req]
    if not all_of and not either_of:
        return None
    return And(HasAll(*all_of), *either_of)


def location_rule(world: UncannyCatWorld, location_name: str) -> Rule[UncannyCatWorld] | None:
    _loc_id, requirements = LOCATION_DATA[location_name]
    parts: list[Rule[UncannyCatWorld]] = []

    if is_minigame_location(location_name):
        # A minigame's own unlock always gates it. It isn't a gimmick, so gimmick_lock doesn't apply.
        return HasAll(*requirements)

    unlock = items.unlock_item_name(world, level_item_name(location_name))
    if unlock is not None:
        parts.append(Has(unlock))
    if world.options.gimmick_lock:
        gimmicks = gimmick_rule(requirements)
        if gimmicks is not None:
            parts.append(gimmicks)

    return And(*parts) if parts else None


def set_all_location_rules(world: UncannyCatWorld) -> None:
    for location_name in LOCATION_DATA:
        rule = location_rule(world, location_name)
        if rule is None:
            continue
        try:
            location = world.get_location(location_name)
        except KeyError:
            continue  
        world.set_rule(location, rule)

    set_location_rule_exceptions(world)


def set_location_rule_exceptions(world: UncannyCatWorld) -> None:
    """Glitched logic stuff goes here"""
    def rule(name: str, r: Rule[UncannyCatWorld]) -> None:
        try:
            world.set_rule(world.get_location(name), r)
        except KeyError:
            return

# Prisms a single level pays out, by the best rank you can actually get in it.
PEAK_PRISMS = 5
GOOD_PRISMS = 4
OK_PRISMS = 3
COMPLETE_PRISMS = 2
"""What a level is worth when you can finish it but can't rank up, because a gimmick it needs is missing."""


GimmickRequirement = tuple[tuple[str, ...], ...]
"""Gimmick requirements needed to beat specific levels."""

PrismTier = tuple[int, GimmickRequirement]
"""What a rank pays out, and the gimmicks needed to reach it."""


def rank_check_prisms(world: UncannyCatWorld) -> int:
    """What the always-on rank check is worth, i.e. how high a rank the player signed up to hit."""
    if world.options.rank_check_difficulty == RankCheckDifficulty.option_good:
        return GOOD_PRISMS
    return OK_PRISMS


def prism_tiers(world: UncannyCatWorld, include_peak: bool) -> list[tuple[int, str]]:
    """(prisms, rank location suffix) from the best rank down. The first tier you can reach is what you bank."""
    tiers: list[tuple[int, str]] = []
    if include_peak:
        tiers.append((PEAK_PRISMS, " Peak Rank"))
    tiers.append((rank_check_prisms(world), " Good Rank"))
    return tiers


def gimmick_alternatives(requirements: list[str]) -> GimmickRequirement:
    """["Keys", "Portals|Jump Pads"] -> one tuple of alternatives per requirement"""
    return tuple(tuple(requirement.split("|")) for requirement in requirements)


def seed_levels(world: UncannyCatWorld) -> list[tuple[str, str | None]]:
    """(level, unlock item) for every level in the seed. World 0 has no unlock item, so it is always playable."""
    excluded = get_excluded_locations(world)
    levels: list[tuple[str, str | None]] = []
    seen: list[str] = []
    for location_name in LOCATION_DATA:
        if is_minigame_location(location_name):
            continue  # minigames aren't levels, no prisms attached
        level = level_item_name(location_name)
        if level in seen:
            continue
        seen.append(level)
        if f"{level} Complete" in excluded:
            continue
        levels.append((level, items.unlock_item_name(world, level)))
    return levels


def max_obtainable_prisms(world: UncannyCatWorld) -> int:
    """Every level in the seed unlocked and ranked as high as logic expects. The cap for the goal amount."""
    best_rank_prisms = prism_tiers(world, bool(world.options.peak_checks))[0][0]
    return len(seed_levels(world)) * best_rank_prisms


@dataclass
class HasEnoughPrisms(Rule["UncannyCatWorld"], game="Uncanny Cat Golf"):
    """
    Enough prisms banked to unlock the goal level.

    Each unlocked level pays out for the highest rank you can actually reach in it: the first tier whose
    gimmicks you hold, or `COMPLETE_PRISMS` if you can only finish the level. `include_peak` adds the
    peak tier on top, which is what logic assumes when peak checks are on.
    """

    include_peak: bool

    class Resolved(Rule.Resolved):
        required: int
        free_prisms: int
        levels: tuple[tuple[str | None, tuple[PrismTier, ...]], ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            total = self.free_prisms
            for unlock, tiers in self.levels:
                if unlock is not None and not state.has(unlock, self.player):
                    continue
                total += self.level_prisms(state, tiers)
                if total >= self.required:
                    return True
            return total >= self.required

        def level_prisms(self, state: CollectionState, tiers: tuple[PrismTier, ...]) -> int:
            """The best rank you can reach in one unlocked level."""
            for prisms, gimmicks in tiers:
                if all(
                    any(state.has(gimmick, self.player) for gimmick in alternatives)
                    for alternatives in gimmicks
                ):
                    return prisms
            return COMPLETE_PRISMS

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            dependencies: dict[str, set[int]] = {}
            for unlock, tiers in self.levels:
                names = [unlock] if unlock is not None else []
                names += [g for _prisms, gimmicks in tiers for alternatives in gimmicks for g in alternatives]
                for name in names:
                    dependencies.setdefault(name, set()).add(id(self))
            return dependencies

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            ranks = ", ".join(str(prisms) for prisms, _gimmicks in self.levels[0][1]) if self.levels else ""
            return f"{self.required} prisms ({ranks} per ranked level, {COMPLETE_PRISMS} if you can only complete it)"

    @override
    def _instantiate(self, world: "UncannyCatWorld") -> "HasEnoughPrisms.Resolved":
        tiers = prism_tiers(world, self.include_peak)
        free_prisms = 0
        levels: list[tuple[str | None, tuple[PrismTier, ...]]] = []
        for level, unlock in seed_levels(world):
            level_tiers = tuple(
                (prisms, gimmick_alternatives(LOCATION_DATA[f"{level}{suffix}"][1]) if world.options.gimmick_lock else ())
                for prisms, suffix in tiers
            )
            if unlock is None and not level_tiers[0][1]:
                # Playable from the start and nothing gates its best rank, so its payout is a constant.
                free_prisms += level_tiers[0][0]
                continue
            levels.append((unlock, level_tiers))
        return HasEnoughPrisms.Resolved(
            required=world.options.prism_unlock_amount.value,
            free_prisms=free_prisms,
            levels=tuple(levels),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )


def has_enough_prisms(world: UncannyCatWorld) -> Rule[UncannyCatWorld]:
    peak_checks_on = bool(world.options.peak_checks)
    in_logic = HasEnoughPrisms(include_peak=peak_checks_on)
    if peak_checks_on:
        return in_logic

    # You can go out of logic and get higher ranks and goal early, this tries to account for that in UT
    return in_logic | (
        OutOfLogic(f"Peak levels for {PEAK_PRISMS} prisms each instead of {rank_check_prisms(world)}")
        & HasEnoughPrisms(include_peak=True)
    )


def set_completion_condition(world: UncannyCatWorld) -> None:
    goal = GOAL_LEVEL[world.options.goal_level.value]
    parts: list[Rule[UncannyCatWorld]] = []

    if world.options.gimmick_lock:
        gimmicks = gimmick_rule(LOCATION_DATA[f"{goal} Complete"][1])
        if gimmicks is not None:
            parts.append(gimmicks)

    parts.append(has_enough_prisms(world))

    world.set_rule(world.get_location("Victory"), And(*parts))
    world.set_completion_rule(Has("Victory"))

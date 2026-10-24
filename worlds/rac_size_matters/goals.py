"""Goal selection shared by generation, Universal Tracker and the client."""

from rule_builder.rules import And, CanReachRegion, Rule

from Options import OptionError

from .constants import Rac5Planets
from .data.models import RACItem, RACLocation
from .locations import MENU_REGION
from .locations.quodrona import VICTORY_RULE
from .locations.shared import required_clank_challenges, required_skill_points
from .options import ClankChallenges, Goal, PickAndMixGoals, SkillPoints
from .rules._helpers import CanReachAllClankChallenges, CanReachAllSkillPoints

GOAL_EVENTS: dict[int, str] = {
    Goal.option_defeat_otto: "Quodrona Completed",
    Goal.option_all_skill_points: "All Skill Points Completed",
    Goal.option_all_clank_challenges: "All Clank Challenges Completed",
    Goal.option_pick_and_mix: "Pick and Mix Completed",
}


def selected_goals(goal: int, pick_and_mix_goals) -> tuple[int, ...]:
    """Every goal that must be completed: the chosen goal, or each Pick and Mix selection."""
    if goal != Goal.option_pick_and_mix:
        return (goal,)
    return tuple(sorted(Goal.from_any(name).value for name in pick_and_mix_goals))


def validate_goals(world) -> None:
    options = world.options
    player_name = world.multiworld.get_player_name(world.player)
    goals = selected_goals(options.goal.value, options.pick_and_mix_goals.value)
    if not goals:
        raise OptionError(
            f"{player_name}'s RAC Size Matters: {Goal.display_name} Pick and Mix requires at least one "
            f"{PickAndMixGoals.display_name} selection."
        )
    if Goal.option_all_skill_points in goals and not required_skill_points(options):
        raise OptionError(
            f"{player_name}'s RAC Size Matters: the All Skill Points goal requires {SkillPoints.display_name} "
            "to be Easy or Hard."
        )
    if Goal.option_all_clank_challenges in goals and not required_clank_challenges(options):
        raise OptionError(
            f"{player_name}'s RAC Size Matters: the All Clank Challenges goal requires {ClankChallenges.display_name} "
            "to be on with at least one Clank Challenge Group selected."
        )


def _goal_condition(goal: int) -> tuple[str, Rule]:
    """(region, rule) for a single goal."""
    if goal == Goal.option_defeat_otto:
        return Rac5Planets.QUODRONA, VICTORY_RULE
    if goal == Goal.option_all_skill_points:
        return MENU_REGION, CanReachAllSkillPoints()
    return MENU_REGION, CanReachAllClankChallenges()


def create_victory(world, regions) -> None:
    goal = world.options.goal.value
    goals = selected_goals(goal, world.options.pick_and_mix_goals.value)
    if goal == Goal.option_pick_and_mix:
        conditions = [_goal_condition(selected) for selected in goals]
        region = MENU_REGION
        rule = And(*(CanReachRegion(parent) & condition for parent, condition in conditions))
    else:
        region, rule = _goal_condition(goal)
    regions[region].add_event(GOAL_EVENTS[goal], "Victory", rule, location_type=RACLocation, item_type=RACItem)

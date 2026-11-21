from dataclasses import dataclass, field
from typing import Iterable, TypedDict, NotRequired, ClassVar

from rule_builder.rules import (
    Rule,
    True_,
    CanReachRegion,
    CanReachLocation,
    CanReachEntrance,
)

from .extra_toggle import ExtraToggleRuleReplacer
from .rule_replacement import NestedAndInLevelRuleSimplifierRuleReplacer, RuleReplacer
from ..areas import Area
from ..characters import Character
from ..levels import Level


RULE_OPTIMIZER = NestedAndInLevelRuleSimplifierRuleReplacer()


@dataclass(frozen=True)
class LocationData:
    region: str
    rule: Rule = field(default_factory=True_)
    er_rule: Rule | None = None
    """While ER is not implemented, comparing generation using the slower ER rules vs pre-optimised normal rules can
    identify issues in the logic if their two sets of rules don't produce identical results.
    If `er_rule` is None, use `rule` instead."""


@dataclass(frozen=True)
class StudsEventData(LocationData):
    stud_total: int = 0

    def __post_init__(self):
        if self.stud_total < 0:
            raise Exception(f"Invalid stud_total {self.stud_total}. stud_total must be greater than zero.")


@dataclass(frozen=True)
class MinikitData(LocationData):
    # Minikits that can be achieved by performing actions in multiple orders sometimes have different names depending on
    # which was the last action performed. This also allowed for minikit 'duplication' in vanilla, though the minikits
    # collected are technically unique, so it's not actually duplication. For randomizer purposes, these unique minikits
    # are considered the same AP location.
    pickup_names: tuple[str, ...] = ()

    def __post_init__(self):
        if not self.pickup_names:
            raise Exception("No pickup names provided")
        for name in self.pickup_names:
            # Minikit pickup names are null-terminated strings of up to 8 bytes, so only 7 bytes can be used when
            # including the null-terminator.
            byte_size = len(name.encode())
            if byte_size > 7:
                raise Exception(f"Invalid pickup name {name} encodes to {byte_size} bytes, but the max is 7.")


def minikit_data(region: str, rule: Rule | None = None, *, er_rule: Rule | None = None, pickup_name: str) -> MinikitData:
    """Helper for defining minikit data with a single pickup name."""
    if rule is None:
        return MinikitData(region, er_rule=er_rule, pickup_names=(pickup_name,))
    else:
        return MinikitData(region, rule, er_rule, (pickup_name,))


@dataclass(frozen=True)
class ExitData:
    to_region: str
    rule: Rule = field(default_factory=True_)
    er_rule: Rule | None = None
    name: str | None = None
    new_level: Level | None = None


# FIXME: Move chapter names into the Area type.
@dataclass(frozen=True)
class RegionData:
    name: str
    exits: tuple[ExitData, ...]

    def __init__(self, name: str, *exits: ExitData):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "exits", tuple(exits))


class IntendedCompletionPath(TypedDict):
    base: NotRequired[tuple[str, ...]]
    normal: NotRequired[tuple[str, ...]]
    moderate: NotRequired[tuple[str, ...]]
    hard: NotRequired[tuple[str, ...]]


@dataclass
class ChapterHelper:
    area: Area
    start_region: str
    _regions_used_in_can_reach: set[str] = field(default_factory=set, init=False)

    def can_reach_region(self, region_name: str):
        self._regions_used_in_can_reach.add(region_name)
        return CanReachRegion(f"{self.area.readable_name} - {region_name}")

    def can_reach_location(self, location_name: str):
        return CanReachLocation(f"{self.area.readable_name} - {location_name}")

    def can_reach_entrance(self, entrance_name: str):
        return CanReachEntrance(f"{self.area.readable_name} - {entrance_name}")

    def make_chapter(
            self,
            regions: dict[str, tuple[ExitData, ...]],
            minikits: dict[str, MinikitData],
            power_brick: LocationData,
            # TODO: Add wip_true_jedi_rule
            ridables: dict[Character, LocationData | tuple[LocationData, ...]] | None = None,
            extra_entrance_rules: Rule | None = None,
            intended_completion_path: IntendedCompletionPath | None = None,
    ):
        if ridables is None:
            ridables = {}
        if extra_entrance_rules is None:
            extra_entrance_rules = True_()
        if intended_completion_path is None:
            intended_completion_path = {}
        return Chapter(
            area=self.area,
            start_region=self.start_region,
            regions=regions,
            minikits=minikits,
            power_brick=power_brick,
            ridables=ridables,
            extra_entrance_rules=extra_entrance_rules,
            regions_in_can_reach=self._regions_used_in_can_reach,
            intended_completion_path=intended_completion_path,
        )


@dataclass(frozen=True, kw_only=True)
class LogicArea:
    COMPLETION_REGION_NAME: ClassVar[str] = "Level Completion"
    area: Area
    start_region: str
    regions: dict[str, tuple[ExitData, ...]]
    intended_completion_path: IntendedCompletionPath = field(default_factory=dict)
    """The intended traversal route through the chapter. This is used to determine what abilities are required to
    complete the chapter, based on extracting abilities from the entrance rules, and any extra_entrance_rules.
    
    The start region and Chapter Completion region are implicit."""
    ridables: dict[Character, LocationData | tuple[LocationData, ...]] = field(default_factory=dict)
    extra_entrance_rules: Rule = field(default_factory=True_)
    regions_in_can_reach: Iterable[str] = ()
    name: str = field(init=False)
    start_level: Level = field(init=False)
    region_to_level: dict[str, Level] = field(init=False, default_factory=dict)

    def __post_init__(self):
        # Get the name from the Area.
        name = self.area.readable_name
        object.__setattr__(self, "name", name)

        start_level = self.area.get_first_playable_level()
        if start_level is None:
            raise Exception(f"First playable level for {self.name} is None")
        object.__setattr__(self, "start_level", start_level)

        # TODO: Defer rule optimisation until generation time
        if self.area.get_extra_toggle_characters():
            # Add `| Has("Extra Toggle")` to rules that can be satisfied by having Extra Toggle.
            # It's important that replacements go in the following order:
            # 1) Un-nest rules, so that Extra Toggle rules can efficiently apply to And/Or rules.
            # 2) Add Extra Toggle Rules. Special InLevelRules that can be simplified must still be untouched so that it
            #    is possible to tell whether Extra Toggle is a suitable alternative for the rule.
            # 3) Simplify special InLevelRules and un-nest any that become And/Or rules, including combining
            #    HasAny/AllAbilities where appropriate.
            rule_optimizer = ExtraToggleRuleReplacer(self, RULE_OPTIMIZER)
        else:
            rule_optimizer = RULE_OPTIMIZER

        self._post_init_optimize_rules(rule_optimizer)

        # Automatically add in the Completion region because it is the same for each type of playable area.
        self.regions[self.COMPLETION_REGION_NAME] = ()

        # FIFO queue Depth-First-Search. DFS vs BFS doesn't matter here, only that every region is visited, and every
        # exit is tried.
        region_queue: list[tuple[str, Level]] = [(self.start_region, self.start_level)]
        region_to_level = self.region_to_level
        while region_queue:
            region_name, region_level = region_queue.pop()

            if region_name in region_to_level:
                # Check that an alternative route has not propagated a different level name.
                # The COMPLETION_REGION_NAME region's level is set automatically, so is ignored by this check.
                if region_to_level[region_name] != region_level and region_name != self.COMPLETION_REGION_NAME:
                    raise Exception(f"Already found that {region_name} is in level {region_to_level[region_name]}, but"
                                    f"now also found it in {region_level}.")
                continue
            else:
                region_to_level[region_name] = region_level
                for exit_data in self.regions[region_name]:
                    if exit_data.new_level:
                        # Traversing this exit loads a new level.
                        region_queue.append((exit_data.to_region, exit_data.new_level))
                    else:
                        # Traversing this exit continues within the current level.
                        region_queue.append((exit_data.to_region, region_level))

        # Automatically set the Level of the Chapter Completion region to the status level of this area.
        region_to_level[self.COMPLETION_REGION_NAME] = self.area.get_status_level()

        # Check that there exists a path to each region from self.start_region.
        for region_name in self.regions:
            if region_name not in region_to_level:
                raise Exception(f"No path to the {region_name} region was found.")

    def _post_init_optimize_rules(self, rule_optimizer: RuleReplacer):
        for region_name, exits in self.regions.items():
            self.regions[region_name] = tuple(
                rule_optimizer.replace_rule_data(exit_) for exit_ in exits
            )
        for ridable_character, ridable_data in self.ridables.items():
            if isinstance(ridable_data, tuple):
                self.ridables[ridable_character] = tuple(
                    rule_optimizer.replace_rule_data(ridable_datum) for ridable_datum in ridable_data
                )
            else:
                self.ridables[ridable_character] = rule_optimizer.replace_rule_data(ridable_data)

    @property
    def all_in_level_location_data(self) -> Iterable[LocationData]:
        """Yield all unique location data for locations found in this playable area.

        Does not include locations that become accessible once the area is completed (these are always in the
        COMPLETION_REGION_NAME region of the level, and most of the data for these locations is defined elsewhere)."""
        for ridable_data in self.ridables.values():
            if isinstance(ridable_data, tuple):
                yield from ridable_data
            else:
                yield ridable_data


@dataclass(frozen=True, kw_only=True)
class GoldBrickBonus(LogicArea):
    gold_brick_requirement: int

    @property
    def rewards_gold_brick(self) -> bool:
        return self.gold_brick_requirement > 0


@dataclass(frozen=True, kw_only=True)
class Chapter(LogicArea):
    COMPLETION_REGION_NAME = "Chapter Completion"
    minikits: dict[str, MinikitData]
    power_brick: LocationData
    level_minikits: dict[Level, dict[str, MinikitData]] = field(init=False, default_factory=dict)

    def _post_init_optimize_rules(self, rule_optimizer: RuleReplacer):
        super()._post_init_optimize_rules(rule_optimizer)

        for minikit_name, minikit_data in self.minikits.items():
            self.minikits[minikit_name] = rule_optimizer.replace_rule_data(minikit_data)

        replaced_power_brick_data = rule_optimizer.replace_rule_data(self.power_brick)
        object.__setattr__(self, "power_brick", replaced_power_brick_data)

    def __post_init__(self):
        super().__post_init__()

        for location_name, minikit in self.minikits.items():
            level = self.region_to_level[minikit.region]
            if level in self.level_minikits:
                minikits_dict = self.level_minikits[level]
            else:
                minikits_dict = {}
                self.level_minikits[level] = minikits_dict
            minikits_dict[location_name] = minikit

    @property
    def all_in_level_location_data(self) -> Iterable[LocationData]:
        yield from super().all_in_level_location_data
        yield from self.minikits.values()
        yield self.power_brick

    @property
    def short_name(self) -> str:
        return self.area.get_short_name()

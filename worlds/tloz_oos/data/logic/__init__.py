from ...core.rule_builder.rule_import import Rule
from ...data.regions import RegionName
from ..transition_type import TransitionType

LogicLine = tuple[RegionName, RegionName, TransitionType, Rule]

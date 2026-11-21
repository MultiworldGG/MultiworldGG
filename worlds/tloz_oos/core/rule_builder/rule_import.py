try:
    from rule_builder.rules import (
        And,
        AtLeast,
        CanReachRegion,
        False_,
        Has,
        HasAll,
        HasFromList,
        HasGroup,
        NestedRule,
        Or,
        True_,
    )
    from rule_builder.rules import Rule as CoreRule

    from ...world import OracleOfSeasonsWorld

    Rule = CoreRule[OracleOfSeasonsWorld]

    # RB needs to implement the NestedRule accepting resolved we are expecting
    # and implementing the optimization tied to it
    if CoreRule.Resolved not in NestedRule.__annotations__["children"].__args__[0].__args__:
        raise ImportError("#6542 is missing")
except ImportError:
    from .rules import And, AtLeast, CanReachRegion, False_, Has, HasAll, HasFromList, HasGroup, Or, Rule, True_

__all__ = [
    "And",
    "AtLeast",
    "CanReachRegion",
    "False_",
    "Has",
    "HasAll",
    "HasFromList",
    "HasGroup",
    "Or",
    "Rule",
    "True_",
]

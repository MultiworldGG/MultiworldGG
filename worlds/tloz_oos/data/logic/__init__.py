from rule_builder.rules import Rule as BaseRule
from worlds.tloz_oos import OracleOfSeasonsWorld

Rule = BaseRule[OracleOfSeasonsWorld]

LogicLine = tuple[str, str, bool, Rule | None] | tuple[str, str, bool, Rule | None, bool]

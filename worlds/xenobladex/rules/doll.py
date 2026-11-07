from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, Rule, HasGroup
from .level import LogicLevelResolv
from ..Options import LogicLevelSteps

skell_lvls: dict[int, list[str]] = {
    15: [
        "SKF: AS0115 Formula XT"
    ],
    20: [
        "SKF: US0220 Urban ST",
    ],
    30: [
        "SKF: AS0130 Formula ST",
        "SKF: US0230 Urban ST",
        "SKF: AS0330 Verus ST",
        "SKF: AS0430 Lailah ST",
        "SKF: AS0530 Inferno ST",
        "SKF: XS0630 Mastema ST",
        "SKF: XS0730 Amdusias ST",
        "SKF: US0232 Police_1",
        "SKF: US0830 Dozer_1",
        "SKF: US0232 Police_2",
        "SKF: US0830 Dozer_2",
    ],
    50: [
        "SKF: AS0150 Formula ST",
        "SKF: US0250 Urban ST",
        "SKF: AS0350 Verus ST",
        "SKF: AS0450 Lailah ST",
        "SKF: AS0550 Inferno ST",
        "SKF: XS0650 Mastema ST",
        "SKF: XS0750 Amdusias ST",
    ],
    60: [
        "SKF: Formula Zero",
        "SKF: Urban Lincoln",
        "SKF: Verus Cain",
        "SKF: Lailah Queen",
        "SKF: Inferno Skydon",
        "SKF: Mastema White Reaper",
        "SKF: Amdusias Hades",
        "SKF: Ares 70",
        "SKF: Ares 90",
        "SKF: US0860 Excavator_1",
        "SKF: US0860 Excavator_2",
    ],
}

skell_15_rule = Has("KEY: Level", count=LogicLevelResolv(15), options=[OptionFilter(LogicLevelSteps, 0, operator="ne")],
                    filtered_resolution=True) & HasAny(*skell_lvls[15])
skell_20_rule = Has("KEY: Level", count=LogicLevelResolv(20), options=[OptionFilter(LogicLevelSteps, 0, operator="ne")],
                    filtered_resolution=True) & HasAny(*skell_lvls[20])
skell_30_rule = Has("KEY: Level", count=LogicLevelResolv(30), options=[OptionFilter(LogicLevelSteps, 0, operator="ne")],
                    filtered_resolution=True) & HasAny(*skell_lvls[30])
skell_50_rule = Has("KEY: Level", count=LogicLevelResolv(50), options=[OptionFilter(LogicLevelSteps, 0, operator="ne")],
                    filtered_resolution=True) & HasAny(*skell_lvls[50])
skell_60_rule = Has("KEY: Level", count=LogicLevelResolv(60), options=[OptionFilter(LogicLevelSteps, 0, operator="ne")],
                    filtered_resolution=True) & HasAny(*skell_lvls[60])
skell_rule = skell_15_rule | skell_20_rule | skell_30_rule | skell_50_rule | skell_60_rule

doll_rules: dict[str, Rule] = {
    "Blade License": Has("KEY: Progressive License"),
    "Skell License": Has("KEY: Progressive License", 2) & skell_rule,
    "Flight Module": Has("KEY: Progressive License", 3) & skell_rule,
    "Skell Frame": HasGroup("SKF"),
}

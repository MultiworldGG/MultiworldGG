from rule_builder.rules import Has, HasAll, HasAny, Rule

quest_rules: dict[str, Rule] = {
    "Quest Probe-fessional": Has("DP: Mining Probe G1", 3) & HasAll("DP: Research Probe G1", "KEY: FNet"),
    "Quest Skell License": HasAny("WPN: Trial Knife", "WPN: Trial Sword", "WPN: Trial Assault Rifle"),
    "Quest Weaponized": Has("WPN: Ramjet Rifle_1"),
    "Quest Thats Incredible": HasAll("WPN: Hyde Dyads", "WPN: Diagonal Twins"),
    "Quest The Little Rich Girl": Has("WPN: Scrap Duo"),
}

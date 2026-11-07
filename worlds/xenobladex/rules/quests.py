from rule_builder.rules import Has, HasAll, HasAny, Rule
from .importantItems import important_item_rules as impit_rules

pip_squeak_rule = (
    impit_rules["Frozen Pizza"]
    & impit_rules["Hot Dog"]
    & impit_rules["Hamburger"]
    & impit_rules["Aganeba Alloy"]
)
handy_manon_rule = impit_rules["Windshield Glass"]
thats_incredible_rule = HasAll("WPN: Hyde Dyads", "WPN: Diagonal Twins")

quest_rules: dict[str, Rule] = {
    "Quest Probe-fessional": Has("DP: Mining Probe G1", 3) & HasAll("DP: Research Probe G1", "KEY: FNet"),
    "Quest Skell License": (
        HasAny("WPN: Trial Knife", "WPN: Trial Sword", "WPN: Trial Assault Rifle")
        & (pip_squeak_rule | handy_manon_rule | thats_incredible_rule)
    ),
    "Quest Weaponized": Has("WPN: Ramjet Rifle_1"),
    "Quest Thats Incredible": thats_incredible_rule,
}

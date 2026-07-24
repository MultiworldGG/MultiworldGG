from rule_builder.rules import Has, HasAll, Rule

shop_rules: dict[str, Rule] = {
    "Shop Mia": HasAll("AMR: Combat Bodywear_1", "WPN: Iron Blades_1"),
    "Shop Bodyguard": HasAll("WPN: Warrior Assault Rifle_1", "WPN: Iron Sword_1", "WPN: Titanium Shield_1"),
    "Shop Cooking Schooled": Has("WPN: Chrome Sword_1"),
    "Shop Lend an Ear": Has("WPN: Chrome Knife_1"),
    "Shop Boot Camp": Has("WPN: Soldier Assault Rifle_1"),
    "Shop Ovah and Out": Has("WPN: Savage Ziyse"),
}

from rule_builder.rules import Has, HasAll, Rule, HasGroup

doll_rules: dict[str, Rule] = {
    "Blade License": Has("KEY: Blade License"),
    "Skell License": HasAll("KEY: Blade License", "KEY: Skell License") & HasGroup("SKF"),
    "Flight Module": HasAll("KEY: Blade License", "KEY: Skell License", "KEY: Flight Module") & HasGroup("SKF"),
}

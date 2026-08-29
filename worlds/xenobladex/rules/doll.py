from rule_builder.rules import Has, Rule, HasGroup

doll_rules: dict[str, Rule] = {
    "Blade License": Has("KEY: Progressive License"),
    "Skell License": Has("KEY: Progressive License", 2) & HasGroup("SKF"),
    "Flight Module": Has("KEY: Progressive License", 3) & HasGroup("SKF"),
}

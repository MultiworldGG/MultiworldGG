from rule_builder.rules import Has, Rule, True_

field_skill_rules: dict[str, Rule] = {
    "Mechanical 1": True_(),
    "Mechanical 2": Has("FLDSK: Mechanical", 1),
    "Mechanical 3": Has("FLDSK: Mechanical", 2),
    "Mechanical 4": Has("FLDSK: Mechanical", 3),
    "Mechanical 5": Has("FLDSK: Mechanical", 4),
    "Biological 1": True_(),
    "Biological 2": Has("FLDSK: Biological", 1),
    "Biological 3": Has("FLDSK: Biological", 2),
    "Biological 4": Has("FLDSK: Biological", 3),
    "Biological 5": Has("FLDSK: Biological", 4),
    "Archeological 1": True_(),
    "Archeological 2": Has("FLDSK: Archeological", 1),
    "Archeological 3": Has("FLDSK: Archeological", 2),
    "Archeological 4": Has("FLDSK: Archeological", 3),
    "Archeological 5": Has("FLDSK: Archeological", 4),
}

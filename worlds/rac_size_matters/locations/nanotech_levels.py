from rule_builder.rules import And, True_

from ..rules._helpers import HasChallengeMode, HasGoodExpPlanet, HasExpAccess


def access_rule(world, *, level, categories=frozenset()):
    rules = [HasExpAccess()]
    if level > 20 and world.options.nanotech_experience_multiplier.value <= 8:
        rules.append(HasGoodExpPlanet())
    if "challenge_mode_nanotech_level" in categories:
        rules.append(HasChallengeMode(world, 1))
    if not rules:
        return True_()
    return rules[0] if len(rules) == 1 else And(*rules)

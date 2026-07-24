from rule_builder.rules import Has, Rule


def generate_friend_rule(friend: str) -> dict[str, Rule]:
    return {f"{friend} {i}": Has(f"FRD: {friend}", i) for i in range(1, 6)}


friends_rules: dict[str, Rule] = {
    **generate_friend_rule("Nagi"),
    **generate_friend_rule("L"),
    **generate_friend_rule("Lao"),
    **generate_friend_rule("HB"),
    **generate_friend_rule("Gwin"),
    **generate_friend_rule("Frye"),
    **generate_friend_rule("Doug"),
    **generate_friend_rule("Yelv"),
    **generate_friend_rule("Boze"),
    **generate_friend_rule("Phog"),
    **generate_friend_rule("Elma"),
    **generate_friend_rule("Lin"),
    **generate_friend_rule("Celica"),
    **generate_friend_rule("Irina"),
    **generate_friend_rule("Murderess"),
    **generate_friend_rule("Alexa"),
    **generate_friend_rule("Hope"),
    **generate_friend_rule("Mia")
}

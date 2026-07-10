from __future__ import annotations

from functools import reduce
from typing import TYPE_CHECKING

from rule_builder.rules import Has, Rule

from . import locations, regions

if TYPE_CHECKING:
    from .world import PikunikuWorld


def build_rule(world: PikunikuWorld, requirements: tuple[str, ...], location_name: str | None = None) -> Rule | None:
    """Convert a requirement tuple from the logic sheet into a Rule Builder rule.

    "Apple x3" means three Apple items. "Coins" is only a logical requirement when
    coinsanity is enabled (otherwise coins are freely farmable in-game), and resolves
    to enough "5 Coins" items to afford the shop purchase at location_name.
    Returns None when there is no requirement.
    """
    rules: list[Rule] = []
    for requirement in requirements:
        if requirement == "Apple x3":
            rules.append(Has("Apple", count=3))
        elif requirement == "Coins":
            if world.options.coinsanity:
                rules.append(Has("5 Coins", count=locations.get_required_five_coins(location_name)))
        elif requirement == "Sunglasses": # Sunglasses and X-Ray Glasses are interchangeable
            rules.append(Has("Sunglasses") | Has("X-Ray Glasses"))
        else:
            rules.append(Has(requirement))

    if not rules:
        return None
    return reduce(lambda a, b: a & b, rules)


def set_all_rules(world: PikunikuWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: PikunikuWorld) -> None:
    for region_name in regions.get_active_region_names(world):
        rule = build_rule(world, regions.REGION_ENTRY_REQUIREMENTS[region_name])
        if rule is not None:
            world.set_rule(world.get_entrance(f"The Valley -> {region_name}"), rule)


def set_all_location_rules(world: PikunikuWorld) -> None:
    for location_data in locations.get_active_location_data(world):
        rule = build_rule(world, location_data.requirements, location_data.name)
        if rule is not None:
            world.set_rule(world.get_location(location_data.name), rule)


def set_completion_condition(world: PikunikuWorld) -> None:
    victory_rule = build_rule(world, locations.VICTORY_REQUIREMENTS)
    assert victory_rule is not None
    world.set_rule(world.get_location(locations.VICTORY_EVENT_LOCATION), victory_rule)

    world.set_completion_rule(Has("Victory"))

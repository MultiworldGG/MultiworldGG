"""Seed-specific vendor access rules shared by generation and the client.

The wire format contains only resolved item predicates, never executable code.
Unsupported rules fail generation instead of silently weakening vendor gates.
"""
from collections.abc import Mapping

from rule_builder.rules import And, Or, Has, HasAll, HasAny, HasAllCounts, HasAnyCount, Rule

from .locations import LOCATIONS, MENU_REGION

VENDOR_CATEGORIES = frozenset({
    "weapon_vendor", "gadget_vendor", "weapon_titan_vendor", "weapon_mod_vendor",
})


VERSION = 2


def encode_rule(rule):
    """Encode as ``["all"|"any", *children]`` / ``["has", item, count]`` so each operator adds one
    level of JSON nesting; Archipelago rejects packets nested deeper than 16."""
    if not isinstance(rule, Rule.Resolved):
        raise TypeError(f"Vendor access requires a rule-builder rule, got {rule!r}")
    if rule.always_true:
        return ["true"]
    if rule.always_false:
        return ["false"]
    if type(rule) in (And.Resolved, Or.Resolved):
        return ["all" if type(rule) is And.Resolved else "any", *(encode_rule(child) for child in rule.children)]
    if type(rule) is Has.Resolved:
        return ["has", rule.item_name, rule.count]
    if type(rule) in (HasAll.Resolved, HasAny.Resolved):
        return ["all" if type(rule) is HasAll.Resolved else "any", *(["has", name, 1] for name in rule.item_names)]
    if type(rule) in (HasAllCounts.Resolved, HasAnyCount.Resolved):
        return ["all" if type(rule) is HasAllCounts.Resolved else "any",
                *(["has", name, count] for name, count in rule.item_counts)]
    raise TypeError(f"Unsupported vendor access rule: {type(rule).__qualname__}")


def evaluate_rule(rule, items: Mapping[str, int]) -> bool:
    op = rule[0]
    if op == "true":
        return True
    if op == "false":
        return False
    if op == "has":
        return items.get(rule[1], 0) >= rule[2]
    if op == "all":
        return all(evaluate_rule(child, items) for child in rule[1:])
    if op == "any":
        return any(evaluate_rule(child, items) for child in rule[1:])
    raise ValueError(f"Unknown vendor rule operation: {op!r}")


def reachable_regions(regions: Mapping[str, list], items: Mapping[str, int]) -> set[str]:
    """Fixed-point region sweep over the exported entrance table, mirroring CollectionState."""
    reached = {MENU_REGION}
    changed = True
    while changed:
        changed = False
        for region, entrances in regions.items():
            if region not in reached and any(
                parent in reached and evaluate_rule(rule, items) for parent, rule in entrances
            ):
                reached.add(region)
                changed = True
    return reached


def location_accessible(data, location: str, items: Mapping[str, int], reached: set[str] | None = None) -> bool:
    entry = data["locations"].get(location)
    if entry is None:
        return False
    region, rule = entry
    if reached is None:
        reached = reachable_regions(data["regions"], items)
    return region in reached and evaluate_rule(rule, items)


def build_vendor_rules(world):
    """Export the region graph once as a flat entrance table rather than inlining it per location."""
    regions = {}
    pending = []
    locations = {}
    for definition in LOCATIONS:
        if not definition.categories & VENDOR_CATEGORIES or not definition.available(world.options):
            continue
        location = world.multiworld.get_location(definition.name, world.player)
        locations[definition.name] = [location.parent_region.name, encode_rule(location.access_rule)]
        pending.append(location.parent_region)
    while pending:
        region = pending.pop()
        if region.name == MENU_REGION or region.name in regions:
            continue
        regions[region.name] = [[entrance.parent_region.name, encode_rule(entrance.access_rule)]
                                for entrance in region.entrances]
        pending.extend(entrance.parent_region for entrance in region.entrances)
    return {"version": VERSION, "regions": regions, "locations": locations}

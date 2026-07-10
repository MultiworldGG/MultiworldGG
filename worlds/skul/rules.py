from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.rules import Has

if TYPE_CHECKING:
    from .world import SkulWorld


def set_all_rules(world: SkulWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_location_rules(world: SkulWorld) -> None:
    # Castle Repair checks require the Death Knight NPC to be unlocked.
    for i in range(1, 5):
        world.set_rule(
            world.multiworld.get_location(f"Castle Repair {i}", world.player),
            Has("Death Knight NPC"),
        )

    # Witch tree tiers — each tier requires one more Progressive Tree item than the last.
    # Skull tree: Marrow Transplant (tier 0), Quick Dislocation (1), Nutrition Supply (2), Exoskeleton Reinforcement (3)
    for tier, name in enumerate(["Marrow Transplant", "Quick Dislocation", "Nutrition Supply", "Exoskeleton Reinforcement"]):
        if tier > 0:
            max_i = 10 if name in ("Marrow Transplant", "Quick Dislocation") else 2
            rule = Has("Progressive Skull Tree", count=tier)
            for i in range(1, max_i + 1):
                world.set_rule(world.multiworld.get_location(f"{name} {i}", world.player), rule)

    # Body tree: Thick Bone (tier 0), Fracture Prevention (1), Heavy Frame (2), Reassemble (3)
    for tier, name in enumerate(["Thick Bone", "Fracture Prevention", "Heavy Frame", "Reassemble"]):
        if tier > 0:
            max_i = 10 if name in ("Thick Bone", "Fracture Prevention") else 2
            rule = Has("Progressive Bone Tree", count=tier)
            for i in range(1, max_i + 1):
                world.set_rule(world.multiworld.get_location(f"{name} {i}", world.player), rule)

    # Soul tree: Fatal Mind (tier 0), Ancestral Fortitude (1), Spirit Acceleration (2), Ancient Alchemy (3)
    for tier, name in enumerate(["Fatal Mind", "Ancestral Fortitude", "Spirit Acceleration", "Ancient Alchemy"]):
        if tier > 0:
            max_i = 10 if name == "Ancestral Fortitude" else 2
            rule = Has("Progressive Spirit Tree", count=tier)
            for i in range(1, max_i + 1):
                world.set_rule(world.multiworld.get_location(f"{name} {i}", world.player), rule)

    # Mini boss and boss checks require the Progressive Stage for their area.
    for area, count in [
        ("Forest of Harmony", 1),
        ("Grand Hall",        2),
        ("The Black Lab",     3),
        ("Fortress of Fate",  4),
    ]:
        rule = Has("Progressive Stage", count=count)
        world.set_rule(world.multiworld.get_location(f"{area} Mini Boss Defeated", world.player), rule)
        world.set_rule(world.multiworld.get_location(f"{area} Boss Defeated",      world.player), rule)


def set_completion_condition(world: SkulWorld) -> None:
    world.set_completion_rule(Has("Victory"))

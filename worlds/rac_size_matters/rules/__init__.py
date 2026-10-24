from typing import TYPE_CHECKING

from rule_builder.rules import Has

if TYPE_CHECKING:
    from ..world import RACSizeMatterWorld


def set_rules(world: "RACSizeMatterWorld") -> None:
    # locations/* import rules._helpers, so importing locations at module level here would be circular.
    from ..locations import ALL_LOCATIONS, Rac5Categories

    # Set completions need all four pieces, so progression placed there lets fill
    # lock a missing piece behind its own set and dead-end the seed.
    no_progression_categories = frozenset((Rac5Categories.ARMOUR_SET_CHECK,))

    world.set_completion_rule(Has("Victory"))
    for location in world.get_locations():
        definition = ALL_LOCATIONS.get(location.name)
        if definition is None:
            continue
        world.set_rule(location, definition.rule)
        if definition.categories & no_progression_categories:
            location.item_rule = lambda item: not item.advancement

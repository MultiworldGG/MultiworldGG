from .entrances import set_entrance_rules


# Set completions need all four pieces, so progression placed there lets fill
# lock a missing piece behind its own set and dead-end the seed.
_NO_PROGRESSION_CATEGORIES = frozenset(("armour_set_check",))


def set_rules(world) -> None:
    from ..locations import LOCATIONS

    no_progression_locations = {
        definition.name for definition in LOCATIONS
        if definition.categories & _NO_PROGRESSION_CATEGORIES
    }
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)
    set_entrance_rules(world)
    for location in world.multiworld.get_locations(world.player):
        world.set_rule(location, location.rule_factory(world))
        if location.name in no_progression_locations:
            location.item_rule = lambda item: not item.advancement

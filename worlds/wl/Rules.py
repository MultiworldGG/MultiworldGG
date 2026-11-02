from BaseClasses import MultiWorld
from .Names import LocationName, ItemName
from .Options import required_garlic_cloves
from worlds.generic.Rules import add_rule


def set_rules(world: MultiWorld, options, player: int):
    if options.goal == "garlic_hunt":
        required = required_garlic_cloves(
            options.number_of_garlic_cloves.value,
            options.percentage_of_garlic_cloves.value,
        )
        add_rule(
            world.get_location(LocationName.garlic_goal, player),
            lambda state: state.has(
                ItemName.garlic_clove, player, required
            ),
        )
    world.completion_condition[player] = lambda state: state.has(
        ItemName.victory, player
    )

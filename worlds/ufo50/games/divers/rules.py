from typing import TYPE_CHECKING

from BaseClasses import Region
from worlds.generic.Rules import set_rule


if TYPE_CHECKING:
    from ... import UFO50World


def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:
    player = world.player
    bomb = "Divers - Bomb"
    brelic = "Divers - B Relic"
    menu = regions["Menu"]
    shallows = regions["Shallows"]
    ruins = regions["Ruins"]
    depths = regions["Depths"]
    boss = regions["Boss"]
    menu.connect(shallows)

    if not world.options.divers_lever_check:
        shallows.connect(ruins)
    else:
        shallows.connect(ruins,
                         rule=lambda state: state.has("Divers - Ruins Gate", player))
    ruins.connect(depths,
                  rule=lambda state: state.has_group("Divers - Weapons", player, 3)
                  and state.has_group("Divers - Potions", player))

    if not world.options.divers_lever_check:
        depths.connect(boss, rule=lambda state: state.has("Divers - Mist Orb", player))
    else:
        depths.connect(boss,
                       rule=lambda state: state.has("Divers - Mist Orb", player)
                       and state.has_all(("Divers - Ruins Gate", "Divers - Boss Gate 1", "Divers - Boss Gate 2"), player))

    set_rule(world.get_location("Divers - Shallows Bomb Blocked Chest 1"),
             rule=lambda state: state.has(bomb, player))
    set_rule(world.get_location("Divers - Shallows Bomb Blocked Chest 2"),
             rule=lambda state: state.has(bomb, player))
    set_rule(world.get_location("Divers - Piranha Cave Bomb Blocked Chest"),
             rule=lambda state: state.has(bomb, player))
    set_rule(world.get_location("Divers - Holy Potion Store"),
             rule=lambda state: state.has(brelic, player))

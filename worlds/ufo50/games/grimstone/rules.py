from typing import TYPE_CHECKING

from BaseClasses import Region, CollectionState
from worlds.generic.Rules import set_rule


if TYPE_CHECKING:
    from ... import UFO50World


def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:
    player = world.player
    menu = regions["Menu"]
    pleasant = regions["Pleasant"]
    heston = regions["Heston"]
    auster = regions["Auster"]
    basement = regions["Basement"]
    pasaje = regions["Pasaje"]
    serpent = regions["Serpent"]
    lawbuck = regions["Lawbuck"]
    tower = regions["Tower"]
    boss = regions["Boss"]
    abyss = "Grimstone - ABYSSIDIAN"
    menu.connect(pleasant)
    pleasant.connect(heston,
                     rule=lambda state: state.has("Grimstone - TOOLBOX", player))
    heston.connect(auster,
                   rule=lambda state: state.has("Grimstone - PASS", player))
    auster.connect(basement,
                   rule=lambda state: state.has("Grimstone - M. MIRROR", player))
    auster.connect(pasaje,
                   rule=lambda state: state.has("Grimstone - RUSTY KEY", player))
    auster.connect(serpent,
                   rule=lambda state: state.has("Grimstone - DETONATOR", player))
    serpent.connect(lawbuck,
                    rule=lambda state: state.has("Grimstone - DEVIL HORN", player))
    lawbuck.connect(tower,
                    rule=lambda state: state.has("Grimstone - HORSESHOE", player))
    tower.connect(boss,
                  rule=lambda state: state.has("Grimstone - HAMMER", player))
    pleasant.connect(regions["Pleasantshop"])
    heston.connect(regions["Hestonshop"])
    auster.connect(regions["Austershop"])
    lawbuck.connect(regions["Lawbuckshop"])
    tower.connect(regions["Agarthashop"])
    set_rule(world.get_location("Grimstone - Calamity Location"),
             rule=lambda state: state.has(abyss, player))

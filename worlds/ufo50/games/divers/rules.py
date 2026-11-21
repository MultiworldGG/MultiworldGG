from typing import TYPE_CHECKING, Any

from BaseClasses import Region, CollectionState
from rule_builder import rules


if TYPE_CHECKING:
    from ... import UFO50World


def create_rules(world: "UFO50World", regions: dict[str, Region]) -> None:
    bomb = "Divers - Bomb"
    brelic = "Divers - B relic"

    menu = regions["Menu"]
    shallows = regions["Shallows"]
    ruins = regions["Ruins"]
    slime = regions["Slime"]
    spider = regions["Spider"]
    jelly = regions["Jelly"]
    boss = regions["Boss"]
    sticks = regions["Sticks"]
    mallets = regions["Mallets"]
    lids = regions["Lids"]
    potions = regions["Potions"]
    bombs = regions["Bombs"]

    hasweapons = rules.HasGroup("Divers - Weapons", count=3)
    haspotion = rules.HasGroup("Divers - Potions")
    hasbomb = rules.Has(bomb)
    hasbrelic = rules.Has(brelic)
    malletrule = rules.Has("Divers - Mallets Store Page") & hasweapons
    lidrule = rules.Has("Divers - Lids Store Page") & hasweapons
    potionrule = rules.Has("Divers - Potions Store Page") & hasweapons
    bombrule = rules.Has("Divers - Bombs Store Page") & hasweapons
    hasemblems = (rules.Has("Divers - Mooncat Emblem") & rules.Has("Divers - Barbuta Emblem")
                  & rules.Has("Divers - Divers Emblem"))

    slimegate = rules.Has("Divers - Slime Cave Gate")
    northgate = rules.Has("Divers - Ruins North Gate")
    northeastgate = rules.Has("Divers - Ruins Northeast Gate")
    southeastgate = rules.Has("Divers - Ruins Northwest Gate")
    southwestgate = rules.Has("Divers - Ruins Southwest Gate")
    jellygate = northeastgate | southeastgate
    bossgate = (rules.Has("Divers - Boss Gate 1") & rules.Has("Divers - Boss Gate 2") & rules.Has("Divers - Mist Orb")
                & haspotion & hasweapons)

    menu.connect(shallows)
    shallows.connect(slime, rule=slimegate)
    shallows.connect(ruins, rule=northgate)
    ruins.connect(spider, rule=southwestgate)
    ruins.connect(jelly, rule=jellygate)
    jelly.connect(boss, rule=bossgate)
    menu.connect(sticks, rule=hasweapons)
    sticks.connect(mallets, rule=malletrule)
    sticks.connect(lids, rule=lidrule)
    sticks.connect(potions, rule=potionrule)
    sticks.connect(bombs, rule=bombrule)

    if "Divers" in world.options.cherry_allowed_games:
        world.set_rule(world.get_location("Divers - Cherry"), hasemblems)

    slimerule = slimegate & hasweapons
    ingotrule = northgate & hasweapons
    crossrule = northgate & southwestgate & hasweapons

    world.set_rule(world.get_location("Divers - Shallows Bomb Blocked Chest 1"), hasbomb)
    world.set_rule(world.get_location("Divers - Shallows Bomb Blocked Chest 2"), hasbomb)
    world.set_rule(world.get_location("Divers - Piranha Cave Bomb Blocked Chest"), hasbomb)
    world.set_rule(world.get_location("Divers - Holy Potion Store"), hasbrelic)
    world.set_rule(world.get_location("Divers - Mist Orb Store"), hasweapons & haspotion & northgate)

    shop_rules: dict[str, rules.Rule[Any]] = {
        "Slime Lance": slimerule,
        "Slime Trident": slimerule & crossrule,
        "Shell Lance": slimerule,
        "Shell Trident": crossrule,
        "Elec Lance": ingotrule,
        "Elec Trident": crossrule,
        "Slime Sledge": slimerule & ingotrule,
        "Shell Sledge": ingotrule,
        "Elec Sledge": crossrule,
        "Slime Buckler": slimerule,
        "Slime Tower": slimerule & crossrule,
        "Shell Tower": crossrule,
        "Elec Tower": crossrule,
        "Holy Potion": crossrule,
        "Egg": ingotrule
    }

    for slot, rule in shop_rules.items():
        for i in range(world.options.divers_store_depth.value):
            if i == 0:
                number = ""
            else:
                number = f" {i + 1}"
            world.set_rule(world.get_location(f"Divers - {slot} Store{number}"), rule)

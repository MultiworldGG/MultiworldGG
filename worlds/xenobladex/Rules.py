from functools import reduce
import operator
from typing import TYPE_CHECKING
from BaseClasses import Entrance
from rule_builder.rules import Has, Rule, True_

if TYPE_CHECKING:
    from . import XenobladeXWorld

from . import Items
from .rules.doll import doll_rules
from .rules.fieldSkills import field_skill_rules
from .rules.fnet import fnet_rules
from .rules.friends import friends_rules
from .rules.importantItems import important_item_rules
from .rules.level import level_rules
from .rules.quests import quest_rules
from .rules.shop import shop_rules
from .rules.zones import zone_rules


xenobladeXRules: dict[str, Rule["XenobladeXWorld"]] = {
    **doll_rules,
    **field_skill_rules,
    **fnet_rules,
    **friends_rules,
    **important_item_rules,
    **level_rules,
    **quest_rules,
    **shop_rules,
    **zone_rules,
}


def connect_with_rule(world: "XenobladeXWorld", source: str, target: str, rule: Rule["XenobladeXWorld"]) -> None:
    source_region = world.get_region(source)
    target_region = world.get_region(target)

    connection = Entrance(world.player, target, source_region)
    source_region.exits.append(connection)
    connection.connect(target_region)

    world.set_rule(connection, rule)


def set_rules(world: "XenobladeXWorld") -> None:
    """Setting all the rules for region connections and region->item connections"""
    for region in world.get_regions():
        if region.name == "Menu":
            continue
        rule_names = region.name.split("+")
        rules = [xenobladeXRules[rule] for rule in rule_names]
        if not rules:
            rules = [True_()]
        new_rule = reduce(operator.iand, rules)
        connect_with_rule(world, "Menu", region.name, new_rule)

    world.get_location("EBK: Lao Boss - Chp 12: Story").place_locked_item(Items.create_item(world, "KEY: Victory"))
    world.set_completion_rule(Has("KEY: Victory"))

from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule

if TYPE_CHECKING:
    from .world import BuildJetpackWorld

def set_all_rules(world: BuildJetpackWorld) -> None:
    set_all_location_rules(world)
    set_completion_condition(world)

def set_shop_tier_rules(tier: int, access: Rule, world: BuildJetpackWorld):
    stringtier = str(tier)
    world.set_rule(world.get_location("Diving Suit "+stringtier), access)
    world.set_rule(world.get_location("Oxygen Mask "+stringtier), access)
    world.set_rule(world.get_location("Magnet "+stringtier), access)
    if (tier < 8):
        world.set_rule(world.get_location("Backpack "+stringtier), access)
        world.set_rule(world.get_location("Fins "+stringtier), access)

def set_all_location_rules(world: BuildJetpackWorld) -> None:
    # jetpack is really overpowered.
    # it's single-handedly a viable option for getting earlier upgrades, but starts getting unrealistic at level 7 (still feasible!)
    can_buy_l2_upgrades: Rule = (Has("Diving Suit", count=1) & Has("Oxygen Mask", count=1)) | Has("Jetpack", count=1)
    can_buy_l3_upgrades: Rule = (Has("Diving Suit", count=2) & Has("Oxygen Mask", count=2)) | Has("Jetpack", count=2)
    can_buy_l4_upgrades: Rule = (Has("Diving Suit", count=3) & Has("Oxygen Mask", count=3)) | Has("Jetpack", count=2)
    can_buy_l5_upgrades: Rule = (Has("Diving Suit", count=4) & Has("Oxygen Mask", count=4)) | Has("Jetpack", count=2)
    can_buy_l6_upgrades: Rule = (Has("Diving Suit", count=5) & Has("Oxygen Mask", count=5)) | Has("Jetpack", count=3)
    can_buy_l7_upgrades: Rule = Has("Diving Suit", count=6) & Has("Oxygen Mask", count=6)
    can_buy_l8_upgrades: Rule = Has("Diving Suit", count=7) & Has("Oxygen Mask", count=6)

    set_shop_tier_rules(2, can_buy_l2_upgrades, world)
    set_shop_tier_rules(3, can_buy_l3_upgrades, world)
    set_shop_tier_rules(4, can_buy_l4_upgrades, world)
    set_shop_tier_rules(5, can_buy_l5_upgrades, world)
    set_shop_tier_rules(6, can_buy_l6_upgrades, world)
    set_shop_tier_rules(7, can_buy_l7_upgrades, world)
    set_shop_tier_rules(8, can_buy_l8_upgrades, world)

    world.set_rule(world.get_location("Raft Expansion 1"), Has("Rock"))
    world.set_rule(world.get_location("Raft Expansion 2"), Has("Rock"))
    world.set_rule(world.get_location("Raft Expansion 3"), Has("More Rock"))
    world.set_rule(world.get_location("Jetpack 1"), Has("More Rock") & Has("Raft Expansion", count=1))
    world.set_rule(world.get_location("Jetpack 2"), Has("More Rock") & Has("Raft Expansion", count=1))
    world.set_rule(world.get_location("Jetpack 3"), Has("More Gold") & Has("Raft Expansion", count=1))
    world.set_rule(world.get_location("Radar 1"), Has("Strings") & Has("Raft Expansion", count=2))
    world.set_rule(world.get_location("Radar 2"), Has("Strings") & Has("Raft Expansion", count=2))
    world.set_rule(world.get_location("Radar 3"), Has("Rock") & Has("Raft Expansion", count=2))
    world.set_rule(world.get_location("Radar 4"), Has("Gold") & Has("Raft Expansion", count=2))
    world.set_rule(world.get_location("Radar 5"), Has("Gold") & Has("Raft Expansion", count=2))
    world.set_rule(world.get_location("Gold Statue"), Has("More Gold") & Has("Raft Expansion", count=3))


def set_completion_condition(world: BuildJetpackWorld) -> None:
    world.set_completion_rule(Has("Victory"))
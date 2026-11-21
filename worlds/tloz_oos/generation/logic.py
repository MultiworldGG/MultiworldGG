from typing import cast

from BaseClasses import CollectionState, Item, Region
from Options import Accessibility

from ..core.rule_builder.rule_import import And, Or
from ..data.constants import DUNGEON_NAMES
from ..data.logic.logic_predicates import (
    oos_can_jump_1_wide_pit,
    oos_can_jump_5_wide_pit,
    oos_can_kill_magunesu,
    oos_can_kill_normal_enemy,
    oos_can_kill_stalfos,
    oos_has_feather,
    oos_has_flippers,
    oos_has_magnet_gloves,
    oos_has_small_keys,
    oos_option_hard_logic,
    oos_option_medium_logic,
)
from ..data.logic.rulebuilder import OoSCanReachRegion, Rule
from ..world import OracleOfSeasonsWorld


class AlwaysAllowRule:
    def __init__(self, world: OracleOfSeasonsWorld, rule: Rule, *item_names: str):
        self.rule = rule.resolve(world)
        self.item_names = item_names
        self.player = world.player

    def __call__(self, state: CollectionState, item: Item):
        return item.player == self.player and item.name in self.item_names and self.rule(state)


def apply_self_locking_rules(world: OracleOfSeasonsWorld):
    if world.options.accessibility == Accessibility.option_full:
        return

    # Process self-locking keys first
    key_rules = {
        "Hero's Cave: Final Chest": AlwaysAllowRule(
            world, OoSCanReachRegion("enter d0"), f"Small Key ({DUNGEON_NAMES[0]})", f"Master Key ({DUNGEON_NAMES[0]})"
        ),
        "Gnarled Root Dungeon: Item in Basement": AlwaysAllowRule(
            world, OoSCanReachRegion("d1 railway chest"), f"Small Key ({DUNGEON_NAMES[1]})"
        ),
        "Poison Moth's Lair (1F): Chest in Mimics Room": AlwaysAllowRule(
            world,
            And(OoSCanReachRegion("d3 water room"), oos_can_kill_normal_enemy()),
            f"Small Key ({DUNGEON_NAMES[3]})",
        ),
        "Dancing Dragon Dungeon (1F): Crumbling Room Chest": AlwaysAllowRule(
            world, OoSCanReachRegion("d4 final minecart"), f"Small Key ({DUNGEON_NAMES[4]})"
        ),
        "Dancing Dragon Dungeon (1F): Eye Diving Spot Item": AlwaysAllowRule(
            world, And(OoSCanReachRegion("d4 final minecart"), oos_has_flippers()), f"Small Key ({DUNGEON_NAMES[4]})"
        ),
        "Unicorn's Cave: Magnet Gloves Chest": AlwaysAllowRule(
            world, OoSCanReachRegion("enter d5"), f"Small Key ({DUNGEON_NAMES[5]})"
        ),
        "Unicorn's Cave: Treadmills Basement Item": AlwaysAllowRule(
            world,
            And(
                OoSCanReachRegion("enter d5"),
                oos_has_small_keys(5, 3),
                OoSCanReachRegion("d5 drop ball"),
                oos_has_magnet_gloves(),
                Or(oos_can_kill_magunesu(), And(oos_option_medium_logic(), oos_has_feather())),
            ),
            f"Small Key ({DUNGEON_NAMES[5]})",
        ),
        "Explorer's Crypt (B1F): Chest in Jumping Stalfos Room": AlwaysAllowRule(
            world,
            And(
                OoSCanReachRegion("enter d7"),
                oos_has_small_keys(7, 4),
                Or(oos_can_jump_5_wide_pit(), And(oos_option_hard_logic(), oos_can_jump_1_wide_pit(False))),
                oos_can_kill_stalfos(),
            ),
            f"Small Key ({DUNGEON_NAMES[7]})",
        ),
        "Explorer's Crypt (1F): Chest Right of Entrance": AlwaysAllowRule(
            world,
            And(
                OoSCanReachRegion("enter d7"),
                oos_can_kill_normal_enemy(),
                oos_has_small_keys(7, 1),
            ),
            f"Small Key ({DUNGEON_NAMES[7]})",
        ),
    }

    for location_name, key_rule in key_rules.items():
        location = world.get_location(location_name)
        location.always_allow = key_rule

    # Process other self-locking items
    OTHER_SELF_LOCKING_ITEMS = {
        "Sunken City: Master's Plaque Trade": "Master's Plaque",
        "Subrosia: Market #1": "Star Ore",
    }
    if world.options.trade_sequence:
        OTHER_SELF_LOCKING_ITEMS.update(
            {
                "North Horon: Malon Trade": "Cuccodex",
                "Maple Trade": "Lon Lon Egg",
                "Holodrum Plain: Mrs. Ruul Trade": "Ghastly Doll",
                "Subrosia: Subrosian Chef Trade": "Iron Pot",
                "Sunken City: Ingo Trade": "Goron Vase",
                "North Horon: Yelling Old Man Trade": "Fish",
                "Horon Village: Tick Tock Trade": "Wooden Bird",
                "Eastern Suburbs: Guru-Guru Trade": "Engine Grease",
                "Subrosia: Smithy Hard Ore Reforge": "Hard Ore",
                "Subrosia: Smithy Rusty Bell Reforge": "Rusty Bell",
            }
        )
        if not world.options.secret_locations:
            OTHER_SELF_LOCKING_ITEMS["Goron Mountain: Biggoron Trade"] = "Lava Soup"

    for loc_name, item_name in OTHER_SELF_LOCKING_ITEMS.items():
        location = world.get_location(loc_name)
        region = cast(Region, location.parent_region)
        parent_region = cast(Region, region.entrances[0].parent_region)
        location.always_allow = AlwaysAllowRule(world, OoSCanReachRegion(parent_region.name), item_name)

    # Great Furnace special case
    location = world.get_location("Subrosia: Item Smelted in Great Furnace")
    location.always_allow = AlwaysAllowRule(world, OoSCanReachRegion("great furnace"), "Red Ore", "Blue Ore")


def apply_rule_forbiddance(world: OracleOfSeasonsWorld):
    rupee_shops = [
        "Horon Village: Shop #1",
        "Horon Village: Shop #2",
        "Horon Village: Shop #3",
        "Horon Village: Member's Shop #1",
        "Horon Village: Member's Shop #2",
        "Horon Village: Member's Shop #3",
    ]
    if world.options.advance_shop:
        rupee_shops.extend(
            [
                "Horon Village: Advance Shop #1",
                "Horon Village: Advance Shop #2",
                "Horon Village: Advance Shop #3",
            ]
        )
    if world.options.trade_sequence:
        rupee_shops.extend(
            [
                "Sunken City: Syrup Shop #1",
                "Sunken City: Syrup Shop #2",
                "Sunken City: Syrup Shop #3",
            ]
        )

    def rupee_rule(item: Item):
        return item.player != world.player or not item.code or ((item.code & 0xFF00) != 0x2800)  # 28 being rupees

    for rupee_shop in rupee_shops:
        location = world.get_location(rupee_shop)
        location.item_rule = rupee_rule

    def ore_rule(item: Item):
        return item.player != world.player or not item.code or ((item.code & 0xFF00) != 0x3700)  # 37 being ores

    for ore_shop in ["Subrosia: Market #2", "Subrosia: Market #3", "Subrosia: Market #4", "Subrosia: Market #5"]:
        location = world.get_location(ore_shop)
        location.item_rule = ore_rule

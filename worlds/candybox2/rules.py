import dataclasses
from enum import IntEnum
from json import JSONEncoder
from typing import TYPE_CHECKING, override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Has, Rule, True_, CanReachLocation, False_, CanReachRegion

from .expected_client_version import EXPECTED_CLIENT_VERSION
from .items import CandyBox2ItemName, candy_box_2_base_id, items
from .locations import CandyBox2Location, CandyBox2LocationData, CandyBox2LocationName, locations, filler_locations, \
    extra_location_count, lollipop_farm_filler_locations, the_sea_filler_locations, \
    generate_filter_categories
from .options import GoalCondition, GoalConditions
from .regions import CandyBox2Region, CandyBox2RoomRegion
from .rooms import CandyBox2Room, entrance_friendly_names

if TYPE_CHECKING:
    from . import CandyBox2World


weapons = [
    CandyBox2ItemName.NOTHING_WEAPON,
    CandyBox2ItemName.WOODEN_SWORD,
    CandyBox2ItemName.IRON_AXE,
    CandyBox2ItemName.POLISHED_SILVER_SWORD,
    CandyBox2ItemName.TROLLS_BLUDGEON,
    CandyBox2ItemName.MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.TRIBAL_SPEAR,
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR,
    CandyBox2ItemName.GIANT_SPOON,
    CandyBox2ItemName.SCYTHE,
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM,
]

weapon_strength = [
    CandyBox2ItemName.NOTHING_WEAPON,
    CandyBox2ItemName.WOODEN_SWORD,
    CandyBox2ItemName.IRON_AXE,
    CandyBox2ItemName.TRIBAL_SPEAR,
    CandyBox2ItemName.MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.POLISHED_SILVER_SWORD,
    CandyBox2ItemName.TROLLS_BLUDGEON,
    CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR,
    CandyBox2ItemName.GIANT_SPOON,
    CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF,
    CandyBox2ItemName.GIANT_SPOON_OF_DOOM,
    CandyBox2ItemName.SCYTHE,
]

armors = [
    CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR,
    CandyBox2ItemName.KNIGHT_BODY_ARMOUR,
    CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR,
]

room_parents = {
    CandyBox2Room.CASTLE: "MENU",
    CandyBox2Room.TOWER: CandyBox2Room.CASTLE.value,
    CandyBox2Room.VILLAGE_SHOP: "MENU",
    CandyBox2Room.VILLAGE_FURNISHED_HOUSE: "MENU",
    CandyBox2Room.VILLAGE_QUEST_HOUSE: "MENU",
    CandyBox2Room.QUEST_THE_CELLAR: CandyBox2Room.VILLAGE_QUEST_HOUSE.value,
    CandyBox2Room.VILLAGE_FORGE: "MENU",
    CandyBox2Room.VILLAGE_MINIGAME: "MENU",
    CandyBox2Room.SQUIRREL_TREE: "MENU",
    CandyBox2Room.LONELY_HOUSE: "MENU",
    CandyBox2Room.QUEST_THE_DESERT: "MENU",
    CandyBox2Room.POGO_STICK_SPOT: "MENU",
    CandyBox2Room.LOLLIPOP_FARM: "MENU",
    CandyBox2Room.WISHING_WELL: "MENU",
    CandyBox2Room.CAVE: "MENU",
    CandyBox2Room.QUEST_THE_OCTOPUS_KING: CandyBox2Room.CAVE.value,
    CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD: CandyBox2Room.CAVE.value,
    CandyBox2Room.DIG_SPOT: "MENU",
    CandyBox2Room.QUEST_THE_BRIDGE: "MENU",
    CandyBox2Room.SORCERESS_HUT: "MENU",
    CandyBox2Room.PIER: "MENU",
    CandyBox2Room.QUEST_THE_SEA: CandyBox2Room.PIER.value,
    CandyBox2Room.LIGHTHOUSE: CandyBox2Room.PIER.value,
    CandyBox2Room.QUEST_THE_FOREST: "MENU",
    CandyBox2Room.HOLE: "MENU",
    CandyBox2Room.QUEST_THE_HOLE: CandyBox2Room.HOLE.value,
    CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE: "MENU",
    CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER: CandyBox2Room.CASTLE.value,
    CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM: CandyBox2Room.CASTLE.value,
    CandyBox2Room.CASTLE_DARK_ROOM: CandyBox2Room.CASTLE.value,
    CandyBox2Room.CASTLE_BAKEHOUSE: CandyBox2Room.CASTLE.value,
    CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM: CandyBox2Room.CASTLE.value,
    CandyBox2Room.DRAGON: CandyBox2Room.CASTLE.value,
    CandyBox2Room.QUEST_HELL: CandyBox2Room.DRAGON.value,
    CandyBox2Room.QUEST_THE_DEVELOPER: CandyBox2Room.DRAGON.value,
    CandyBox2Room.DESERT_FORTRESS: "MENU",
    CandyBox2Room.QUEST_THE_XINOPHERYDON: CandyBox2Room.DESERT_FORTRESS.value,
    CandyBox2Room.QUEST_THE_TEAPOT: CandyBox2Room.DESERT_FORTRESS.value,
    CandyBox2Room.QUEST_THE_LEDGE_ROOM: CandyBox2Room.DESERT_FORTRESS.value,
    CandyBox2Room.QUEST_THE_X_POTION: "MENU",
}

@dataclasses.dataclass()
class HasStartWeapon(Rule["CandyBox2World"], game="Candy Box 2"):
    weapon: "CandyBox2ItemName"

    @override
    def _instantiate(self, world: "CandyBox2World") -> Rule.Resolved:
        return self.Resolved(weapon=self.weapon, starting_weapon=world.starting_weapon, player=world.player, caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        weapon: "CandyBox2ItemName"
        starting_weapon: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            for item in items:
                if items[item].code - candy_box_2_base_id == self.starting_weapon and item == self.weapon:
                    return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {self.weapon: {id(self)}}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            # this method can be overridden to display custom explanations
            return [
                {"type": "text", "text": "Has start weapon "},
                {"type": "color", "color": "green", "text": str(self.weapon)},
            ]

class RuleCountInequality(IntEnum):
    LESS_THAN = 0
    LESS_THAN_OR_EQUAL_TO = 1
    EQUAL_TO = 2
    GREATER_THAN_OR_EQUAL_TO = 3
    GREATER_THAN = 4

@dataclasses.dataclass()
class HasCount(Rule["CandyBox2World"], game="Candy Box 2"):
    item: str
    required: int
    inequality: RuleCountInequality

    @override
    def _instantiate(self, world: "CandyBox2World") -> Rule.Resolved:
        return self.Resolved(item=self.item, required=self.required, inequality=self.inequality, player=world.player,
                             caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        item: str
        required: int
        inequality: RuleCountInequality

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            if self.inequality == RuleCountInequality.EQUAL_TO:
                return self.item_count(state, self.player) == self.required
            if self.inequality == RuleCountInequality.LESS_THAN:
                return self.item_count(state, self.player) < self.required
            if self.inequality == RuleCountInequality.LESS_THAN_OR_EQUAL_TO:
                return self.item_count(state, self.player) <= self.required
            if self.inequality == RuleCountInequality.GREATER_THAN:
                return self.item_count(state, self.player) > self.required
            if self.inequality == RuleCountInequality.GREATER_THAN_OR_EQUAL_TO:
                return self.item_count(state, self.player) >= self.required
            raise Exception("Tried to evaluate a count expression with invalid inequality operator")

        def item_count(self, state: CollectionState, player: int):
            if self.item == "chocolate":
                return (
                    state.count(CandyBox2ItemName.CHOCOLATE_BAR, player)
                    + (4 * state.count(CandyBox2ItemName.FOUR_CHOCOLATE_BARS, player))
                    + (3 * state.count(CandyBox2ItemName.THREE_CHOCOLATE_BARS, player))
                )
            if self.item == "lollipop":
                return state.count(CandyBox2ItemName.THREE_LOLLIPOPS, player) * 3 + state.count(
                    CandyBox2ItemName.LOLLIPOP, player
                )
            raise Exception("Tried to evaluate a count expression with invalid item name")

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                CandyBox2ItemName.CHOCOLATE_BAR: {id(self)},
                CandyBox2ItemName.FOUR_CHOCOLATE_BARS: {id(self)},
                CandyBox2ItemName.THREE_CHOCOLATE_BARS: {id(self)},
                CandyBox2ItemName.THREE_LOLLIPOPS: {id(self)},
                CandyBox2ItemName.LOLLIPOP: {id(self)},
            }

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [
                {"type": "text", "text": "Has "},
                self.json_ineq(),
                {"type": "color", "color": "salmon", "text": str(self.required)},
                {"type": "text", "text": " "},
                {"type": "color", "color": "blue", "text": self.item},
            ]

        def json_ineq(self) -> JSONMessagePart:
            match self.inequality:
                case RuleCountInequality.LESS_THAN:
                    return {"type": "text", "color": "green", "text": "less than "}
                case RuleCountInequality.LESS_THAN_OR_EQUAL_TO:
                    return {"type": "text", "color": "green", "text": "less than or equal to "}
                case RuleCountInequality.GREATER_THAN:
                    return {"type": "text", "color": "green", "text": "greater than "}
                case RuleCountInequality.GREATER_THAN_OR_EQUAL_TO:
                    return {"type": "text", "color": "green", "text": "greater than or equal to "}
                case RuleCountInequality.EQUAL_TO:
                    return {"type": "text", "color": "green", "text": "exactly "}

class CandyBox2RulesPackage(JSONEncoder):
    expected_client_version: str
    locations: dict["CandyBox2LocationName", "CandyBox2LocationData"]
    location_rules: dict["CandyBox2LocationName", Rule]
    room_rules: dict["CandyBox2Room", Rule]
    location_parents: dict["CandyBox2LocationName", CandyBox2Room]
    room_exits: dict["CandyBox2Room", list["CandyBox2Room"]]
    items: dict[str, str]
    regions: dict[str, str]
    goal_rules: dict[str, Rule]

    def __init__(
        self,
        expected_client_version: str = "",
        *,
        skipkeys=False,
        ensure_ascii=True,
        check_circular=True,
        allow_nan=True,
        sort_keys=False,
        indent=None,
        separators=None,
        default=None,
    ):
        super().__init__(
            skipkeys=skipkeys,
            ensure_ascii=ensure_ascii,
            check_circular=check_circular,
            allow_nan=allow_nan,
            sort_keys=sort_keys,
            indent=indent,
            separators=separators,
            default=default,
        )
        self.expected_client_version = expected_client_version
        self.locations = locations
        self.location_rules = {}
        self.room_rules = {}
        self.location_parents = {}
        self.room_exits = {}
        self.items = {}
        self.regions = {}
        self.goal_rules = {}

    def set_goal_rule(self, rule_name: str, goal_rule: Rule):
        self.goal_rules[rule_name] = goal_rule

    def add_location_rule(
        self,
        location: "CandyBox2LocationName",
        rule: Rule | None,
        parent: CandyBox2Room | None,
    ):
        if rule is not None:
            self.location_rules[location] = rule
        self.location_parents[location] = parent

    def add_room_rule(self, room: "CandyBox2Room", rule: Rule):
        self.room_rules[room] = rule

    def assign_room_exits(self, room: "CandyBox2Room", exits: list["CandyBox2Room"]):
        self.room_exits[room] = exits

    def default(self, o):
        return {
            "expectedClientVersion": o.expected_client_version,
            "locations": {location.id: name for name, location in o.locations.items()},
            "locationParents": {
                o.locations[location].id: room.value
                for location, room in o.location_parents.items()
                if room is not None
            },
            "roomExits": {room.value: [exit.value for exit in exits] for room, exits in o.room_exits.items()},
            "rules": {
                "locations": {o.locations[location].id: rule.to_dict() for location, rule in o.location_rules.items()},
                "rooms": {room: rule.to_dict() for room, rule in o.room_rules.items()},
            },
            "goal": {rule_name: rule.to_dict() for rule_name, rule in o.goal_rules.items()},
            "items": o.items,
            "regions": o.regions,
        }

    def apply_location_rules(self, world: "CandyBox2World", player: int):
        for target, rule in self.location_rules.items():
            try:
                world.set_rule(
                    world.get_location(target),
                    rule,
                )
            except KeyError:
                pass

    def apply_room_rules(self, rooms: dict[str, CandyBox2Region], world: "CandyBox2World", player: int):
        generated_entrances = []
        selected_filler_locations = []

        # Add filler locations
        extra_location_num = extra_location_count(world)
        if extra_location_num > 0:
            current_filter_categories = generate_filter_categories()

            for i in range(extra_location_num):
                non_empty_filler_categories = [category for category in current_filter_categories if len(category) > 0]
                if len(non_empty_filler_categories) == 0:
                    world.raise_error("Not enough filler locations available. Please raise a bug in the Candy Box 2 channel. Include the YAML file for this player.")

                # Select a random category
                selected_filter_category = world.random.choice(non_empty_filler_categories)
                selected_location = world.random.choice(selected_filter_category)
                selected_filter_category.remove(selected_location)
                selected_filler_locations.append(selected_location)

        for target, region in rooms.items():
            rule = self.room_rules.get(target)
            if rule is None:
                rule = True_()

            region.locations += [
                CandyBox2Location(player, location_name.value, self.locations[location_name].id, region)
                for location_name in [
                    location
                    for location, room in self.location_parents.items()
                    if room == (None if target == "MENU" else target)
                ]
                if location_name in selected_filler_locations or (self.locations[location_name].is_included(world) and location_name not in filler_locations)
            ]

            parent = room_parents.get("MENU" if target is None else target)
            if parent is not None:
                entrance = rooms[parent].connect(
                    region,
                    None,
                )
                world.set_rule(entrance, rule)
                if type(region) is CandyBox2RoomRegion:
                    generated_entrances.append(entrance)
                # if rule is not None:
                #     for indirect_region in rule.indirection_required():
                #         world.multiworld.register_indirect_condition(rooms[indirect_region], entrance)

        return generated_entrances


class CandyBox2Castable(IntEnum):
    ACID_RAIN = 0
    FIREBALL = 1
    TELEPORT = 2
    ERASE_MAGIC = 3
    THORNS_SHIELD = 4
    OBSIDIAN_WALL = 5
    BLACK_DEMONS = 6
    BLACK_HOLE = 7


def rule_item(item: "CandyBox2ItemName", count: int = 1):
    return Has(item.value, count)


def rule_room(room: "CandyBox2Room"):
    return CanReachRegion(entrance_friendly_names[room])


def rule_location(location: "CandyBox2LocationName"):
    return CanReachLocation(location.value)


def no_conditions() -> Rule:
    return True_()


def has_weapon(weapon: CandyBox2ItemName):
    return (
        rule_item(weapon)
        | rule_item(CandyBox2ItemName.PROGRESSIVE_WEAPON, weapons.index(weapon))
        | HasStartWeapon(weapon=weapon)
    )


def weapon_is_at_least(minimum_weapon: CandyBox2ItemName):
    condition: Rule = False_()
    for weapon in weapon_strength[weapon_strength.index(minimum_weapon) :]:
        condition = condition | has_weapon(weapon)
    return condition


def armor_is_at_least(minimum_armor: CandyBox2ItemName):
    condition: Rule = False_()
    for armor in armors[armors.index(minimum_armor) :]:
        condition = condition | rule_item(armor)
    return condition


def can_cast(castable: CandyBox2Castable):
    match castable:
        case CandyBox2Castable.ACID_RAIN:
            return (
                rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
                | rule_item(CandyBox2ItemName.ACID_RAIN_SPELL)
            )
        case CandyBox2Castable.FIREBALL:
            return (
                rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
                | rule_item(CandyBox2ItemName.FIREBALL_SPELL)
            )
        case CandyBox2Castable.TELEPORT:
            return (
                rule_item(CandyBox2ItemName.BEGINNERS_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 1)
                | rule_item(CandyBox2ItemName.TELEPORT_SPELL)
            )
        case CandyBox2Castable.ERASE_MAGIC:
            return (
                rule_item(CandyBox2ItemName.ADVANCED_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 2)
                | rule_item(CandyBox2ItemName.ERASE_MAGIC_SPELL)
            )
        case CandyBox2Castable.THORNS_SHIELD:
            return (
                rule_item(CandyBox2ItemName.ADVANCED_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 2)
                | rule_item(CandyBox2ItemName.THORNS_SHIELD_SPELL)
            )
        case CandyBox2Castable.OBSIDIAN_WALL:
            return (
                rule_item(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 3)
                | rule_item(CandyBox2ItemName.OBSIDIAN_WALL_SPELL)
            )
        case CandyBox2Castable.BLACK_DEMONS:
            return (
                rule_item(CandyBox2ItemName.BLACK_MAGIC_GRIMOIRE)
                | rule_item(CandyBox2ItemName.PROGRESSIVE_GRIMOIRE, 3)
                | rule_item(CandyBox2ItemName.BLACK_DEMONS_SPELL)
            )
        case CandyBox2Castable.BLACK_HOLE:
            return rule_item(CandyBox2ItemName.PURPLE_FIN)
    return None


def has_at_least_chocolates(chocolates: int):
    return HasCount(
        "chocolate", chocolates, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO
    )


def has_all_chocolates():
    return has_at_least_chocolates(13)


# Allows the player to plant enough lollipops at the farm for 1/minute
def can_grow_lollipops():
    return (
        HasCount(
            "lollipop", 9, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO
        )
        & rule_room(CandyBox2Room.LOLLIPOP_FARM)
    )


def can_farm_lollipops():
    return (
        can_grow_lollipops()
        & rule_item(CandyBox2ItemName.PITCHFORK)
        & rule_item(CandyBox2ItemName.SHELL_POWDER)
        & rule_item(CandyBox2ItemName.GREEN_FIN)
    )


# Ideally allows the player to stumble upon a quest they can use to farm candies
def can_farm_candies():
    return can_farm_lollipops()


def has_projectiles():
    return (
        rule_item(CandyBox2ItemName.RED_ENCHANTED_GLOVES)
        | rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        | rule_item(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
    )


def can_jump():
    return (
        (rule_item(CandyBox2ItemName.ROCKET_BOOTS) | rule_item(CandyBox2ItemName.DESERT_BIRD_FEATHER))
        & rule_item(CandyBox2ItemName.POGO_STICK)
    ) | rule_item(CandyBox2ItemName.PROGRESSIVE_JUMP, 2)


def can_fly():
    return (rule_item(CandyBox2ItemName.ROCKET_BOOTS) & rule_item(CandyBox2ItemName.POGO_STICK)) | rule_item(
        CandyBox2ItemName.PROGRESSIVE_JUMP, 3
    )


def can_escape_hole():
    return can_fly() | can_cast(CandyBox2Castable.TELEPORT)


def can_brew(also_require_lollipops: bool):
    if also_require_lollipops:
        return rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & can_farm_candies() & can_farm_lollipops()

    return rule_item(CandyBox2ItemName.SORCERESS_CAULDRON) & can_farm_candies()


def can_heal():
    return can_brew(False) | rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)


def sea_entrance():
    return (
        weapon_is_at_least(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
        & has_projectiles()
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)
        & can_heal()
    )


def can_beat_sharks():
    return sea_entrance() & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)


def generate_rules_package():
    rules_package = CandyBox2RulesPackage(EXPECTED_CLIENT_VERSION)
    generate_rules_package_location_rules(rules_package)
    generate_rules_package_room_rules(rules_package)
    generate_rules_package_exits(rules_package)
    generate_rules_package_constants(rules_package)

    for condition in GoalConditions:
        rules_package.set_goal_rule(condition.name, generate_rules_package_rule_segment(condition))

    return rules_package


def generate_rules_package_location_rules(rules_package: CandyBox2RulesPackage):
    rules_package.add_location_rule(CandyBox2LocationName.DISAPPOINTED_EMOTE_CHOCOLATE_BAR, can_farm_candies(), None)
    rules_package.add_location_rule(CandyBox2LocationName.HP_BAR_UNLOCK, no_conditions(), None)
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_LOLLIPOP_ON_EXHAUST_CHUTE, no_conditions(), CandyBox2Room.VILLAGE_FORGE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_WOODEN_SWORD, no_conditions(), CandyBox2Room.VILLAGE_FORGE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_IRON_AXE,
        rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_WOODEN_SWORD),
        CandyBox2Room.VILLAGE_FORGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD,
        can_farm_candies() & rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_IRON_AXE),
        CandyBox2Room.VILLAGE_FORGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR,
        can_farm_candies()
        & rule_location(CandyBox2LocationName.CAVE_EXIT)
        & rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_POLISHED_SILVER_SWORD),
        CandyBox2Room.VILLAGE_FORGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_FORGE_BUY_SCYTHE,
        can_farm_candies()
        & rule_room(CandyBox2Room.DRAGON)
        & rule_location(CandyBox2LocationName.VILLAGE_FORGE_BUY_LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.VILLAGE_FORGE,
    )

    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_ON_THE_BOOKSHELF,
        no_conditions(),
        CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_IN_THE_BOOKSHELF,
        no_conditions(),
        CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_HOUSE_LOLLIPOP_UNDER_THE_RUG,
        no_conditions(),
        CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
    )

    # Cellar rules
    rules_package.add_location_rule(
        CandyBox2LocationName.CELLAR_QUEST_CLEARED, no_conditions(), CandyBox2Room.QUEST_THE_CELLAR
    )

    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_FIRST_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_SECOND_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_THIRD_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_FOURTH_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_FIFTH_QUESTION, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SQUIRRELS_PUZZLE, no_conditions(), CandyBox2Room.SQUIRREL_TREE
    )
    rules_package.add_location_rule(CandyBox2LocationName.X_MARKS_THE_SPOT, no_conditions(), CandyBox2Room.DIG_SPOT)
    rules_package.add_location_rule(
        CandyBox2LocationName.LOCKED_CANDY_BOX_ACQUIRED, no_conditions(), CandyBox2Room.LONELY_HOUSE
    )

    # Desert rules
    rules_package.add_location_rule(
        CandyBox2LocationName.DESERT_QUEST_CLEARED,
        weapon_is_at_least(CandyBox2ItemName.IRON_AXE),
        CandyBox2Room.QUEST_THE_DESERT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.DESERT_BIRD_FEATHER_ACQUIRED,
        weapon_is_at_least(CandyBox2ItemName.IRON_AXE) & has_projectiles(),
        CandyBox2Room.QUEST_THE_DESERT,
    )

    rules_package.add_location_rule(CandyBox2LocationName.POGO_STICK, no_conditions(), CandyBox2Room.POGO_STICK_SPOT)

    # Wishing Well rules
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_RED_ENCHANTED_GLOVES,
        rule_item(CandyBox2ItemName.LEATHER_GLOVES) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_PINK_ENCHANTED_GLOVES,
        rule_item(CandyBox2ItemName.LEATHER_GLOVES) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_SUMMONING_TRIBAL_SPEAR,
        has_weapon(CandyBox2ItemName.TRIBAL_SPEAR) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_ENCHANTED_MONKEY_WIZARD_STAFF,
        has_weapon(CandyBox2ItemName.MONKEY_WIZARD_STAFF) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_ENCHANTED_KNIGHT_BODY_ARMOUR,
        rule_item(CandyBox2ItemName.KNIGHT_BODY_ARMOUR) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_JASPERS,
        rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_OCTOPUS_KING_CROWN_WITH_OBSIDIAN,
        rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ENCHANT_GIANT_SPOON_OF_DOOM,
        has_weapon(CandyBox2ItemName.GIANT_SPOON) & has_all_chocolates(),
        CandyBox2Room.WISHING_WELL,
    )

    # Bridge rules
    rules_package.add_location_rule(
        CandyBox2LocationName.TROLL_DEFEATED,
        weapon_is_at_least(CandyBox2ItemName.POLISHED_SILVER_SWORD) | rule_item(CandyBox2ItemName.PURPLE_FIN),
        CandyBox2Room.QUEST_THE_BRIDGE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_TROLLS_BLUDGEON_ACQUIRED,
        weapon_is_at_least(CandyBox2ItemName.POLISHED_SILVER_SWORD) | rule_item(CandyBox2ItemName.PURPLE_FIN),
        CandyBox2Room.QUEST_THE_BRIDGE,
    )

    # Cave rules
    rules_package.add_location_rule(CandyBox2LocationName.CAVE_CHOCOLATE_BAR, no_conditions(), CandyBox2Room.CAVE)
    rules_package.add_location_rule(CandyBox2LocationName.CAVE_HEART_PLUG, no_conditions(), CandyBox2Room.CAVE)
    rules_package.add_location_rule(CandyBox2LocationName.CAVE_EXIT, no_conditions(), CandyBox2Room.CAVE)
    rules_package.add_location_rule(
        CandyBox2LocationName.OCTOPUS_KING_DEFEATED,
        (rule_item(CandyBox2ItemName.SORCERESS_CAULDRON)
        & weapon_is_at_least(CandyBox2ItemName.TROLLS_BLUDGEON)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR) | rule_item(CandyBox2ItemName.PURPLE_FIN)),
        CandyBox2Room.QUEST_THE_OCTOPUS_KING,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.MONKEY_WIZARD_DEFEATED,
        (rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
        & can_cast(CandyBox2Castable.TELEPORT)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & weapon_is_at_least(CandyBox2ItemName.TROLLS_BLUDGEON)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR) | rule_item(CandyBox2ItemName.PURPLE_FIN)),
        CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD,
    )

    # The Hole rules
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_HEART_PENDANT_ACQUIRED, can_jump(), CandyBox2Room.QUEST_THE_HOLE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_BLACK_MAGIC_GRIMOIRE_ACQUIRED,
        can_escape_hole() & rule_item(CandyBox2ItemName.SPONGE),
        CandyBox2Room.QUEST_THE_HOLE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_DESERT_FORTRESS_KEY_ACQUIRED,
        can_escape_hole() & (can_fly() | (can_brew(False) & rule_item(CandyBox2ItemName.SPONGE))),
        CandyBox2Room.QUEST_THE_HOLE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_TRIBAL_WARRIOR_DEFEATED,
        can_escape_hole()
        & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_HOLE,
    )

    # TODO: possibly fly over?
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_HOLE_FOUR_CHOCOLATE_BARS_ACQUIRED,
        can_escape_hole()
        & weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_HOLE,
    )

    # The Forest rules
    rules_package.add_location_rule(
        CandyBox2LocationName.FOREST_QUEST_CLEARED,
        weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_FOREST,
    )

    # Castle Entrance rules
    rules_package.add_location_rule(
        CandyBox2LocationName.CASTLE_ENTRANCE_QUEST_CLEARED,
        can_fly()
        | (
            weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
            & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
            & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR)
        ),
        CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.KNIGHT_BODY_ARMOUR_ACQUIRED,
        weapon_is_at_least(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & armor_is_at_least(CandyBox2ItemName.LIGHTWEIGHT_BODY_ARMOUR),
        CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
    )

    # Castle rules
    rules_package.add_location_rule(
        CandyBox2LocationName.PITCHFORK_ACQUIRED, no_conditions(), CandyBox2Room.CASTLE_DARK_ROOM
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.GIANT_NOUGAT_MONSTER_DEFEATED,
        can_cast(CandyBox2Castable.BLACK_HOLE)
        & weapon_is_at_least(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
        & rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN),
        CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER,
    )

    # Egg Room
    rules_package.add_location_rule(
        CandyBox2LocationName.EGG_ROOM_QUEST_CLEARED,
        can_fly() | has_weapon(CandyBox2ItemName.NOTHING_WEAPON),
        CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM,
    )

    # The Tower
    rules_package.add_location_rule(
        CandyBox2LocationName.TALKING_CANDY,
        rule_item(CandyBox2ItemName.P_STONE) &
            rule_item(CandyBox2ItemName.L_STONE) &
            rule_item(CandyBox2ItemName.A_STONE) &
            rule_item(CandyBox2ItemName.Y_STONE),
        CandyBox2Room.TOWER,
    )

    # The Desert Fortress
    rules_package.add_location_rule(
        CandyBox2LocationName.XINOPHERYDON_DEFEATED,
        (can_fly() | (can_brew(False) & can_jump()))
        & (
            has_weapon(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF)
            | rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        ),
        CandyBox2Room.QUEST_THE_XINOPHERYDON,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.XINOPHERYDON_QUEST_UNICORN_HORN_ACQUIRED,
        can_fly() | (can_brew(False) & can_jump()),
        CandyBox2Room.QUEST_THE_XINOPHERYDON,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.TEAPOT_DEFEATED,
        weapon_is_at_least(CandyBox2ItemName.SCYTHE)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN)
        & rule_item(CandyBox2ItemName.SORCERESS_CAULDRON)
        & rule_item(CandyBox2ItemName.XINOPHERYDON_CLAW),
        CandyBox2Room.QUEST_THE_TEAPOT,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.ROCKET_BOOTS_ACQUIRED,
        can_fly()
        | (
            rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
            & can_jump()
            & can_cast(CandyBox2Castable.TELEPORT)
            & (
                rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_OBSIDIAN)
                | has_weapon(CandyBox2ItemName.SUMMONING_TRIBAL_SPEAR)
            )
        ),
        CandyBox2Room.QUEST_THE_LEDGE_ROOM,
    )

    # Lollipop Farm rules
    for location in lollipop_farm_filler_locations:
        match location:
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_1:
                rules_package.add_location_rule(location, HasCount("lollipop", 1, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_2:
                rules_package.add_location_rule(location, HasCount("lollipop", 2, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_3:
                rules_package.add_location_rule(location, HasCount("lollipop", 3, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_4:
                rules_package.add_location_rule(location, HasCount("lollipop", 4, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_5:
                rules_package.add_location_rule(location, HasCount("lollipop", 5, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_6:
                rules_package.add_location_rule(location, HasCount("lollipop", 6, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_7:
                rules_package.add_location_rule(location, HasCount("lollipop", 7, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_8:
                rules_package.add_location_rule(location, HasCount("lollipop", 8, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_9:
                rules_package.add_location_rule(location, HasCount("lollipop", 9, RuleCountInequality.GREATER_THAN_OR_EQUAL_TO), CandyBox2Room.LOLLIPOP_FARM)
            case _:
                if lollipop_farm_filler_locations.index(location) < lollipop_farm_filler_locations.index(CandyBox2LocationName.LOLLIPOP_FARM_EXTRA_100):
                    rules_package.add_location_rule(location, can_grow_lollipops(), CandyBox2Room.LOLLIPOP_FARM)
                else:
                    rules_package.add_location_rule(location, can_farm_lollipops(), CandyBox2Room.LOLLIPOP_FARM)

    # Hell rules
    rules_package.add_location_rule(
        CandyBox2LocationName.DEVIL_DEFEATED,
        can_cast(CandyBox2Castable.BLACK_DEMONS)
        & rule_item(CandyBox2ItemName.UNICORN_HORN)
        & rule_item(CandyBox2ItemName.BOOTS_OF_INTROSPECTION)
        & armor_is_at_least(CandyBox2ItemName.ENCHANTED_KNIGHT_BODY_ARMOUR)
        & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)
        & has_weapon(CandyBox2ItemName.ENCHANTED_MONKEY_WIZARD_STAFF),
        CandyBox2Room.QUEST_HELL,
    )

    # Developer rules
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_DEVELOPER_DEFEATED,
        can_farm_candies() & can_cast(CandyBox2Castable.BLACK_HOLE) & can_cast(CandyBox2Castable.TELEPORT),
        CandyBox2Room.QUEST_THE_DEVELOPER,
    )

    # The Sea rules
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SPONGE_ACQUIRED, sea_entrance(), CandyBox2Room.QUEST_THE_SEA
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_SHELL_POWDER_ACQUIRED, sea_entrance(), CandyBox2Room.QUEST_THE_SEA
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_RED_FIN_ACQUIRED,
        can_beat_sharks() & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS),
        CandyBox2Room.QUEST_THE_SEA,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED,
        can_beat_sharks()
        & can_cast(CandyBox2Castable.ERASE_MAGIC)
        & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS),
        CandyBox2Room.QUEST_THE_SEA,
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED,
        can_beat_sharks()
        & rule_item(CandyBox2ItemName.HEART_PENDANT)
        & rule_item(CandyBox2ItemName.HEART_PLUG)
        & can_cast(CandyBox2Castable.ERASE_MAGIC)
        & rule_item(CandyBox2ItemName.PINK_ENCHANTED_GLOVES)
        & rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN_WITH_JASPERS)
        & rule_item(CandyBox2ItemName.UNICORN_HORN)
        & rule_item(CandyBox2ItemName.SPONGE),
        CandyBox2Room.QUEST_THE_SEA,
    )

    # Based off an initial distance of 1000m
    # Red fin appears at about 150m
    red_fin_appears_at = the_sea_filler_locations.index(CandyBox2LocationName.THE_SEA_EXTRA_22)
    # Green fin appears at about 700m
    green_fin_appears_at = the_sea_filler_locations.index(CandyBox2LocationName.THE_SEA_EXTRA_33)
    # Purple fin appears at about 2500m
    purple_fin_appears_at = the_sea_filler_locations.index(CandyBox2LocationName.THE_SEA_EXTRA_69)
    for location in the_sea_filler_locations:
        index = the_sea_filler_locations.index(location)
        if index > (purple_fin_appears_at - green_fin_appears_at) / 2:
            rules_package.add_location_rule(location, rule_location(CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED), CandyBox2Room.QUEST_THE_SEA)
        elif index > (green_fin_appears_at - red_fin_appears_at) / 2:
            rules_package.add_location_rule(location, rule_location(CandyBox2LocationName.THE_GREEN_FIN_ACQUIRED), CandyBox2Room.QUEST_THE_SEA)
        elif index > red_fin_appears_at / 2:
            rules_package.add_location_rule(location, rule_location(CandyBox2LocationName.THE_RED_FIN_ACQUIRED), CandyBox2Room.QUEST_THE_SEA)
        else:
            rules_package.add_location_rule(location, sea_entrance(), CandyBox2Room.QUEST_THE_SEA)

    # Cyclops Puzzle
    rules_package.add_location_rule(
        CandyBox2LocationName.SOLVE_CYCLOPS_PUZZLE, rule_room(CandyBox2Room.DRAGON), CandyBox2Room.LIGHTHOUSE
    )

    # X Potion
    rules_package.add_location_rule(
        CandyBox2LocationName.YOURSELF_DEFEATED,
        rule_item(CandyBox2ItemName.OCTOPUS_KING_CROWN),
        CandyBox2Room.QUEST_THE_X_POTION,
    )

    # Cooking
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_1, has_at_least_chocolates(9), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_2, has_at_least_chocolates(10), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_3, has_at_least_chocolates(11), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_4, has_at_least_chocolates(12), CandyBox2Room.CASTLE_BAKEHOUSE
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.BAKE_PAIN_AU_CHOCOLAT_5, has_all_chocolates(), CandyBox2Room.CASTLE_BAKEHOUSE
    )

    # Sorceress items
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_BEGINNERS_GRIMOIRE, can_grow_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_ADVANCED_GRIMOIRE, can_grow_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_HAT, can_farm_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_CAULDRON, can_grow_lollipops(), CandyBox2Room.SORCERESS_HUT
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.SORCERESS_HUT_LOLLIPOP_ON_THE_SHELVES, no_conditions(), CandyBox2Room.SORCERESS_HUT
    )

    # Merchant items
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_TOP_LOLLIPOP, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_CENTRE_LOLLIPOP, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_BOTTOM_LOLLIPOP, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_TIME_RING, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_LEATHER_BOOTS, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_LEATHER_GLOVES, no_conditions(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_CHOCOLATE_BAR, can_farm_candies(), CandyBox2Room.VILLAGE_SHOP
    )
    rules_package.add_location_rule(
        CandyBox2LocationName.VILLAGE_SHOP_CANDY_MERCHANTS_HAT, can_farm_candies(), CandyBox2Room.VILLAGE_SHOP
    )


def generate_rules_package_room_rules(rules_package: CandyBox2RulesPackage):
    rules_package.add_room_rule(CandyBox2Room.SQUIRREL_TREE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1))
    rules_package.add_room_rule(CandyBox2Room.LONELY_HOUSE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1))
    rules_package.add_room_rule(
        CandyBox2Room.DIG_SPOT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1) & rule_room(CandyBox2Room.CAVE)
    )
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_DESERT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1))
    rules_package.add_room_rule(CandyBox2Room.LOLLIPOP_FARM, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_BRIDGE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.WISHING_WELL, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.POGO_STICK_SPOT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.CAVE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 2))
    rules_package.add_room_rule(CandyBox2Room.SORCERESS_HUT, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 3))
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_FOREST, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 4))
    rules_package.add_room_rule(CandyBox2Room.PIER, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 4))
    rules_package.add_room_rule(CandyBox2Room.HOLE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 5))
    rules_package.add_room_rule(
        CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 5)
    )
    rules_package.add_room_rule(CandyBox2Room.CASTLE, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 6))
    rules_package.add_room_rule(CandyBox2Room.TOWER, rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 7))
    rules_package.add_room_rule(CandyBox2Room.VILLAGE_MINIGAME, rule_item(CandyBox2ItemName.THIRD_HOUSE_KEY))
    rules_package.add_room_rule(
        CandyBox2Room.DESERT_FORTRESS,
        rule_item(CandyBox2ItemName.DESERT_FORTRESS_KEY) & rule_item(CandyBox2ItemName.PROGRESSIVE_WORLD_MAP, 1),
    )
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_CELLAR, weapon_is_at_least(CandyBox2ItemName.WOODEN_SWORD))
    rules_package.add_room_rule(CandyBox2Room.QUEST_THE_X_POTION, can_brew(True))


def generate_rules_package_exits(rules_package: CandyBox2RulesPackage):
    rules_package.assign_room_exits(
        CandyBox2Room.VILLAGE,
        [
            CandyBox2Room.VILLAGE_SHOP,
            CandyBox2Room.VILLAGE_FORGE,
            CandyBox2Room.VILLAGE_MINIGAME,
            CandyBox2Room.VILLAGE_QUEST_HOUSE,
            CandyBox2Room.VILLAGE_FURNISHED_HOUSE,
            CandyBox2Room.QUEST_THE_X_POTION,
        ],
    )
    rules_package.assign_room_exits(CandyBox2Room.VILLAGE_QUEST_HOUSE, [CandyBox2Room.QUEST_THE_CELLAR])
    rules_package.assign_room_exits(
        CandyBox2Room.WORLD_MAP,
        [
            CandyBox2Room.SQUIRREL_TREE,
            CandyBox2Room.LONELY_HOUSE,
            CandyBox2Room.DIG_SPOT,
            CandyBox2Room.QUEST_THE_DESERT,
            CandyBox2Room.DESERT_FORTRESS,
            CandyBox2Room.LOLLIPOP_FARM,
            CandyBox2Room.WISHING_WELL,
            CandyBox2Room.POGO_STICK_SPOT,
            CandyBox2Room.QUEST_THE_BRIDGE,
            CandyBox2Room.SORCERESS_HUT,
            CandyBox2Room.CAVE,
            CandyBox2Room.PIER,
            CandyBox2Room.QUEST_THE_FOREST,
            CandyBox2Room.HOLE,
            CandyBox2Room.QUEST_THE_CASTLE_ENTRANCE,
            CandyBox2Room.CASTLE,
        ],
    )
    rules_package.assign_room_exits(
        CandyBox2Room.DESERT_FORTRESS,
        [CandyBox2Room.QUEST_THE_LEDGE_ROOM, CandyBox2Room.QUEST_THE_XINOPHERYDON, CandyBox2Room.QUEST_THE_TEAPOT],
    )
    rules_package.assign_room_exits(
        CandyBox2Room.CAVE, [CandyBox2Room.QUEST_THE_NAKED_MONKEY_WIZARD, CandyBox2Room.QUEST_THE_OCTOPUS_KING]
    )
    rules_package.assign_room_exits(CandyBox2Room.PIER, [CandyBox2Room.QUEST_THE_SEA, CandyBox2Room.LIGHTHOUSE])
    rules_package.assign_room_exits(CandyBox2Room.HOLE, [CandyBox2Room.QUEST_THE_HOLE])
    rules_package.assign_room_exits(
        CandyBox2Room.CASTLE,
        [
            CandyBox2Room.CASTLE_DARK_ROOM,
            CandyBox2Room.CASTLE_BAKEHOUSE,
            CandyBox2Room.QUEST_THE_CASTLE_EGG_ROOM,
            CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM,
            CandyBox2Room.QUEST_THE_GIANT_NOUGAT_MONSTER,
            CandyBox2Room.DRAGON,
            CandyBox2Room.TOWER,
        ],
    )
    rules_package.assign_room_exits(CandyBox2Room.DRAGON, [CandyBox2Room.QUEST_THE_DEVELOPER, CandyBox2Room.QUEST_HELL])

def generate_rules_package_goal_rule(world: "CandyBox2World | None"):
    goal_rule = True_()

    goal_conditions = GoalCondition(GoalCondition.default)

    if world is not None:
        goal_conditions = world.options.goal_conditions

    for condition in GoalConditions:
        if goal_conditions.value[condition.value] == 1:
            goal_rule &= generate_rules_package_rule_segment(condition)

    return goal_rule

def generate_rules_package_rule_segment(rule_segment: GoalConditions):
    match rule_segment:
        case GoalConditions.PLAY_STONES:
            return rule_item(CandyBox2ItemName.TALKING_CANDY) & \
                rule_item(CandyBox2ItemName.LOCKED_CANDY_BOX)
        case GoalConditions.DIE_TO_CASTLE_TRAP_ROOM:
            return rule_room(CandyBox2Room.QUEST_THE_CASTLE_TRAP_ROOM) & \
                rule_item(CandyBox2ItemName.LOCKED_CANDY_BOX)
        case GoalConditions.SWIM_3000_METERS:
            return rule_room(CandyBox2Room.QUEST_THE_SEA) & \
                rule_location(CandyBox2LocationName.THE_PURPLE_FIN_ACQUIRED) & \
                rule_item(CandyBox2ItemName.LOCKED_CANDY_BOX)

def generate_rules_package_constants(rules_package: CandyBox2RulesPackage):
    rules_package.items = {item_data.code: item for item, item_data in items.items()}
    rules_package.regions = {code: name for code, name in entrance_friendly_names.items()}

from dataclasses import dataclass
from typing_extensions import override
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WaffleWorld

from .Options import EnemyShuffle, InventoryYoshiLogic, GameLogicDifficulty, Goal
from .Levels import level_info_dict, hard_gameplay_levels, very_hard_gameplay_levels, possible_starting_regions
from .Tricks import logic_tricks

from .enums import Locations, Regions, Items

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAnyCount, HasAll, Rule, True_, CanReachRegion, WrapperRule
from rule_builder.field_resolvers import FromOption, FromWorldAttr
from BaseClasses import CollectionState, Entrance, Location
from NetUtils import JSONMessagePart

GAME_NAME = "SMW: Spicy Mycena Waffles"

@dataclass()
class Macro(WrapperRule["WaffleWorld"], game=GAME_NAME):
    name: str
    description: str = ""

    @override
    def _instantiate(self, world: "WaffleWorld") -> Rule.Resolved:
        if rule := world.rule_macros.get(self.name):
            return rule
        rule = self.Resolved(
            self.child.resolve(world),
            self.name,
            self.description,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )
        world.rule_macros[self.name] = rule
        return rule

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str
        description: str = ""

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return [{"type": "color", "color": "green" if self(state) else "salmon", "text": str(self)}]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = ""
            if state is not None:
                suffix = " ✓" if self(state) else " ✕"
            return f"{self.name}{suffix}"

        @override
        def __str__(self) -> str:
            return self.name
        
CanCarry: Rule = Has(Items.carry)
CanRun: Macro = Macro(
    HasAny(Items.run, Items.progressive_run),
    "Can run",
    "Can run freely",
)
CanWallRun: Macro = Macro(
    HasAnyCount({Items.run: 1, Items.progressive_run: 2}),
    "Can wall run anywhere",
    "Can perform a wall run anywhere",
)
CanSwim: Macro = Macro(
    HasAny(Items.swim, Items.progressive_swim),
    "Can swim",
    "Can swim freely underwater"
)
CanClimb: Rule = Has(Items.climb)
CanSpinJump: Rule = Has(Items.spin_jump)

HasMushroom: Macro = Macro(
    Has(Items.progressive_powerup, 1),
    "Has mushrooms",
    "Can be Big Mario",
)
HasFireFlower: Macro = Macro(
    Has(Items.progressive_powerup, 2),
    "Has fire flowers",
    "Can throw fireballs at enemies",
)
HasFeather: Macro = Macro(
    Has(Items.progressive_powerup, 3),
    "Has feathers",
    "Has a cape",
)
HasSuperStar: Macro = Macro(
    Has(Items.super_star_active, 2),
    "Has super star",
    "Can be invincible for a period of time",
)
HasPBalloon: Rule = Has(Items.p_balloon)
HasPSwitch: Rule = Has(Items.p_switch)

HasYSP: Rule = Has(Items.yellow_switch_palace)
HasGSP: Rule = Has(Items.green_switch_palace)
HasRSP: Rule = Has(Items.red_switch_palace)
HasBSP: Rule = Has(Items.blue_switch_palace)

HasMidway: Rule = Has(Items.midway_point)
HasItemBox: Rule = Has(Items.item_box)
HasExtraDefense: Rule = Has(Items.extra_defense)

CanBreakTurnBlocks: Macro = Macro(
    HasAll(Items.progressive_powerup, Items.spin_jump),
    "Can break turn blocks",
    "Can break yellow blocks as Big Mario"
)
CanCapeFly: Macro = Macro(
    HasFeather & CanRun,
    "Can cape fly",
    "Can fly with a cape",
)

CanGetGreenYoshi: Macro = Macro(
        CanReachRegion(Regions.donut_plains_top_secret) |
        CanReachRegion(Regions.yoshis_island_2_region) |
        CanReachRegion(Regions.yoshis_island_3_region) |
        CanReachRegion(Regions.donut_plains_1_region) |
        CanReachRegion(Regions.donut_plains_4_region) |
        CanReachRegion(Regions.vanilla_dome_3_region) |
        CanReachRegion(Regions.vanilla_secret_2_region) |
        (CanReachRegion(Regions.butter_bridge_2_region) & CanCarry) |
        (CanReachRegion(Regions.cookie_mountain_region) & HasRSP) |
        CanReachRegion(Regions.forest_of_illusion_1_region) |
        CanReachRegion(Regions.forest_of_illusion_3_region) |
        CanReachRegion(Regions.chocolate_island_1_region) |
        CanReachRegion(Regions.chocolate_island_2_region) |
        (CanReachRegion(Regions.valley_of_bowser_4_region) & CanClimb) |
        CanReachRegion(Regions.special_zone_5_region) |
        #CanReachRegion(Regions.special_zone_7_region) |
        (CanReachRegion(Regions.special_zone_8_region) & HasPSwitch & CanCarry),
    "Can get Green Yoshi",
    "Can get a Green Yoshi in any level",
    options=[OptionFilter(InventoryYoshiLogic, 0)],
    filtered_resolution=True,
)

CanGetRedYoshi: Macro = Macro(
        (CanReachRegion(Regions.star_road_1_region) & CanBreakTurnBlocks) |
        CanReachRegion(Regions.star_road_4_region),
    "Can get Red Yoshi",
    "Can get a Red Yoshi in any level",
    options=[OptionFilter(InventoryYoshiLogic, 0)],
    filtered_resolution=True,
)

CanGetYellowYoshi: Macro = Macro(
        CanReachRegion(Regions.star_road_3_region) |
        (CanReachRegion(Regions.star_road_5_region) & CanCapeFly | HasPSwitch),
    "Can get Yellow Yoshi",
    "Can get a Yellow Yoshi in any level",
    options=[OptionFilter(InventoryYoshiLogic, 0)],
    filtered_resolution=True,
)

CanGetBlueYoshi: Macro = Macro(
        CanReachRegion(Regions.star_road_2_region) | (
            (CanGetGreenYoshi | CanGetRedYoshi | CanGetYellowYoshi) & (
                    CanReachRegion(Regions.cheese_bridge_region) | 
                    CanReachRegion(Regions.special_zone_3_region) | 
                    CanReachRegion(Regions.valley_of_bowser_2_region)
            )
        ),
    "Can get Blue Yoshi",
    "Can get a Blue Yoshi in any level",
    options=[OptionFilter(InventoryYoshiLogic, 0)],
    filtered_resolution=True,
)

CanGetAnyYoshi: Macro = Macro(
    (
        CanGetGreenYoshi | CanGetRedYoshi | CanGetBlueYoshi | CanGetYellowYoshi
    ),
    "Can get Yoshi",
    "Can get a Yoshi of any color in any levels"
)

CanYoshiCarry: Macro = Macro(
    HasAnyCount({Items.yoshi: 1, Items.progressive_yoshi: 2}) & (
        CanGetGreenYoshi | CanGetBlueYoshi | CanGetYellowYoshi
    ),
    "Can carry with Yoshi",
    "Can maintain any item in Yoshi's mouth"
)

CanCarryOrYoshiTongue: Macro = Macro(
    CanCarry | CanYoshiCarry,
    "Can carry or use Yoshi's tongue",
    "Can carry objects with Mario's hands or Yoshi's tongue"
)

CanYoshiFly: Macro = Macro(
    CanYoshiCarry & CanGetBlueYoshi,
    "Can Yoshi fly",
    "Can fly with Yoshi",
)

CanFly: Macro = Macro(
    CanCapeFly | CanYoshiFly,
    "Can fly",
    "Can fly with either Yoshi or Cape",
)

CanCapeSpinFly: Macro = Macro(
    CanCapeFly & CanSpinJump,
    "Can spin fly",
    "Can fly with Cape while spinning",
)

HasYoshi: Macro = Macro(
    HasAny(Items.yoshi, Items.progressive_yoshi) & CanGetAnyYoshi,
    "Has Yoshi",
    "Can get a Yoshi from either a level or the inventory (if that setting is enabled)"
)


class WaffleRules:
    player: int
    world: "WaffleWorld"
    carryless_exit_rules: dict[str, Rule]
    connection_rules: dict[str, Rule]
    region_rules: dict[str, Rule]
    location_rules: dict[str, Rule]
    enemy_shuffle: int
    required_egg_count: int
    inventory_yoshi_logic: int

    def __init__(self, world: "WaffleWorld") -> None:
        self.player = world.player
        self.world = world
        self.enemy_shuffle = world.options.enemy_shuffle.value
        self.required_egg_count = world.required_egg_count
        self.inventory_yoshi_logic = world.options.inventory_yoshi_logic.value

        options = self.world.options.alternate_logic.value
        self.alternate_logic(self, options)

        if self.world.is_ut:
            options = [trick for trick in logic_tricks if trick not in options]
            self.alternate_logic(self, options, True)

    def set_smw_rules(self) -> None:
        world = self.world
        multiworld = self.world.multiworld

        if self.world.is_ut:
            CanBeatHardLevel: Macro = Macro(
                (OptionFilter(GameLogicDifficulty, 0) & HasMushroom & (HasItemBox | HasMidway)) |
                (OptionFilter(GameLogicDifficulty, 1) & HasMushroom) |
                OptionFilter(GameLogicDifficulty, 2) |
                Has(Items.glitched),
                "Can clear hard levels",
                "Can clear hard levels depending on game_logic_difficulty",
            )

            CanBeatVeryHardLevel: Macro = Macro(
                (OptionFilter(GameLogicDifficulty, 0) & HasFireFlower & (HasMidway | HasItemBox | HasExtraDefense)) |
                (OptionFilter(GameLogicDifficulty, 1) & HasMushroom & (HasItemBox | HasMidway)) |
                OptionFilter(GameLogicDifficulty, 2) |
                Has(Items.glitched),
                "Can clear very hard levels",
                "Can clear very hard levels depending on game_logic_difficulty",
            )
        else:
            CanBeatHardLevel: Macro = Macro(
                (OptionFilter(GameLogicDifficulty, 0) & HasMushroom & (HasItemBox | HasMidway)) |
                (OptionFilter(GameLogicDifficulty, 1) & HasMushroom) |
                OptionFilter(GameLogicDifficulty, 2),
                "Can clear hard levels",
                "Can clear hard levels depending on game_logic_difficulty",
            )

            CanBeatVeryHardLevel: Macro = Macro(
                (OptionFilter(GameLogicDifficulty, 0) & HasFireFlower & (HasMidway | HasItemBox | HasExtraDefense)) |
                (OptionFilter(GameLogicDifficulty, 1) & HasMushroom & (HasItemBox | HasMidway)) |
                OptionFilter(GameLogicDifficulty, 2),
                "Can clear very hard levels",
                "Can clear very hard levels depending on game_logic_difficulty",
            )

        # Swap exit rules & use carryless rules if needed
        for level_id, level_info in level_info_dict.items():
            # Process carryless first
            if level_id in world.carryless_exits:
                level_name = level_info.levelName
                entrance = f"{level_name} -> {level_name} - Secret Exit"
                self.connection_rules[entrance] = self.carryless_exit_rules[entrance]

            # Process swapped locations later
            if level_id in world.swapped_exits:
                level_name = level_info.levelName
                entrance_1 = f"{level_name} -> {level_name} - Normal Exit"
                entrance_2 = f"{level_name} -> {level_name} - Secret Exit"
                entrance_1_data = self.connection_rules[entrance_1]
                entrance_2_data = self.connection_rules[entrance_2]
                self.connection_rules[entrance_1] = entrance_2_data
                self.connection_rules[entrance_2] = entrance_1_data

        # Build glitched entrances
        if self.world.is_ut and world.multiworld.enforce_deferred_connections in ("on", "default"):
            for entrance in multiworld.get_entrances(self.player):
                if entrance.name.endswith("(Glitched)"):
                    self.world.set_rule(entrance, Has(Items.glitched))

        # Build entrance rules
        starting_region = possible_starting_regions[world.options.starting_location.value]
        for entrance_name, rule in self.connection_rules.items():
            entrance: Entrance = self.world.get_entrance(entrance_name)
            if entrance.parent_region.name in hard_gameplay_levels:
                rule = rule & CanBeatHardLevel
            elif entrance.parent_region.name in very_hard_gameplay_levels:
                rule = rule & CanBeatVeryHardLevel
            self.world.set_rule(entrance, rule)
            try:
                location_name = entrance_name.split("-> ")[1]
                location: Location = self.world.get_location(location_name)
                self.world.set_rule(location, rule)
                if self.world.is_ut:
                    # Apply exit rules to 
                    if len(entrance.connected_region.exits) != 0:
                        # Do all of this to fix an issue where rules aren't being applied to an entrance that connects to the origin level
                        for exit in entrance.connected_region.exits:
                            if "Transition" in exit.name:
                                destination = exit.connected_region.exits[0].connected_region.exits[0].connected_region
                                if destination.name == starting_region:
                                    break
                        else:
                            continue
                    glitched_entrance = self.world.get_entrance(f"{entrance_name} (Glitched)")
                    self.world.set_rule(glitched_entrance, rule)
            except KeyError:
                continue

        # Build location rules
        for loc in multiworld.get_locations(self.player):
            rule = True_()
            if loc.name in self.location_rules:
                rule = self.location_rules[loc.name]
            
            if loc.parent_region.name in hard_gameplay_levels:
                rule = rule & CanBeatHardLevel
            elif loc.parent_region.name in very_hard_gameplay_levels:
                rule = rule & CanBeatVeryHardLevel
            # Add generic rules for valid locations
            if "- Midway Point" in loc.name:
                rule = rule & HasMidway
            elif " - Green Switch Palace Block" in loc.name:
                rule = rule & HasGSP
            elif " - Yellow Switch Palace Block" in loc.name:
                rule = rule & HasYSP

            self.world.set_rule(loc, rule)

        # Handle goals
        self.world.set_completion_rule(Has(Items.victory))
        if self.world.options.goal == Goal.option_yoshi_house:
            self.world.set_rule(self.world.get_location(Locations.yoshis_house), Has(Items.yoshi_egg, count=FromWorldAttr("required_egg_count")))
        elif self.world.options.goal == Goal.option_bowser:
            self.world.set_rule(self.world.get_location(Locations.bowser), Has(Items.yoshi_egg, count=FromWorldAttr("required_egg_count")))

    
    def alternate_logic(self) -> None:
        return


class WaffleBasicRules(WaffleRules):
    def __init__(self, world: "WaffleWorld") -> None:
        self.connection_rules = {
            f"{Regions.yoshis_island_1_region} -> {Locations.yoshis_island_1_exit_1}": 
                True_(),
            f"{Regions.yoshis_island_2_region} -> {Locations.yoshis_island_2_exit_1}": 
                True_(),
            f"{Regions.yoshis_island_3_region} -> {Locations.yoshis_island_3_exit_1}": 
                True_(),
            f"{Regions.yoshis_island_4_region} -> {Locations.yoshis_island_4_exit_1}": 
                True_(),
            f"{Regions.yoshis_island_castle_region} -> {Locations.yoshis_island_castle}": 
                CanClimb,
                
            f"{Regions.donut_plains_1_region} -> {Locations.donut_plains_1_exit_1}": 
                True_(),
            f"{Regions.donut_plains_1_region} -> {Locations.donut_plains_1_exit_2}": 
                (
                    CanCarry & (
                        HasGSP |
                        CanCapeFly
                    )
                ) | CanYoshiCarry,
            f"{Regions.donut_plains_2_region} -> {Locations.donut_plains_2_exit_1}": 
                True_(),
            f"{Regions.donut_plains_2_region} -> {Locations.donut_plains_2_exit_2}": 
                CanYoshiCarry | (CanClimb & (
                    (CanCarry & CanBreakTurnBlocks) | HasYoshi)
                ),
            f"{Regions.donut_plains_3_region} -> {Locations.donut_plains_3_exit_1}": 
                True_(),
            f"{Regions.donut_plains_4_region} -> {Locations.donut_plains_4_exit_1}": 
                True_(),
            f"{Regions.donut_secret_1_region} -> {Locations.donut_secret_1_exit_1}": 
                CanSwim,
            f"{Regions.donut_secret_1_region} -> {Locations.donut_secret_1_exit_2}": 
                CanSwim & CanCarryOrYoshiTongue & HasPSwitch,
            f"{Regions.donut_secret_2_region} -> {Locations.donut_secret_2_exit_1}": 
                True_(),
            f"{Regions.donut_ghost_house_region} -> {Locations.donut_ghost_house_exit_1}": 
                CanCapeFly,
            f"{Regions.donut_ghost_house_region} -> {Locations.donut_ghost_house_exit_2}": 
                CanClimb | CanCapeFly,
            f"{Regions.donut_secret_house_region} -> {Locations.donut_secret_house_exit_1}": 
                HasPSwitch,
            f"{Regions.donut_secret_house_region} -> {Locations.donut_secret_house_exit_2}": 
                HasPSwitch & CanCarry & (
                    CanClimb | CanCapeFly
                ),
            f"{Regions.donut_plains_castle_region} -> {Locations.donut_plains_castle}": 
                True_(),

            f"{Regions.vanilla_dome_1_region} -> {Locations.vanilla_dome_1_exit_1}": 
                CanRun & (HasSuperStar | HasMushroom),
            f"{Regions.vanilla_dome_1_region} -> {Locations.vanilla_dome_1_exit_2}": 
                CanClimb & CanCarry & (
                    HasYoshi | HasRSP
                ),
            f"{Regions.vanilla_dome_2_region} -> {Locations.vanilla_dome_2_exit_1}": 
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            f"{Regions.vanilla_dome_2_region} -> {Locations.vanilla_dome_2_exit_2}": 
                CanSwim & CanCarry & HasPSwitch & (
                    CanClimb | HasYoshi
                ),
            f"{Regions.vanilla_dome_3_region} -> {Locations.vanilla_dome_3_exit_1}": 
                True_(),
            f"{Regions.vanilla_dome_4_region} -> {Locations.vanilla_dome_4_exit_1}": 
                True_(),
            f"{Regions.vanilla_secret_1_region} -> {Locations.vanilla_secret_1_exit_1}": 
                CanClimb,
            f"{Regions.vanilla_secret_1_region} -> {Locations.vanilla_secret_1_exit_2}": 
                CanClimb & CanCarry & HasBSP,
            f"{Regions.vanilla_secret_2_region} -> {Locations.vanilla_secret_2_exit_1}": 
                True_(),
            f"{Regions.vanilla_secret_3_region} -> {Locations.vanilla_secret_3_exit_1}": 
                CanSwim,
            f"{Regions.vanilla_ghost_house_region} -> {Locations.vanilla_ghost_house_exit_1}": 
                HasPSwitch,
            f"{Regions.vanilla_fortress_region} -> {Locations.vanilla_fortress}": 
                CanSwim,
            f"{Regions.vanilla_dome_castle_region} -> {Locations.vanilla_dome_castle}": 
                True_(),

            f"{Regions.butter_bridge_1_region} -> {Locations.butter_bridge_1_exit_1}": 
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            f"{Regions.butter_bridge_2_region} -> {Locations.butter_bridge_2_exit_1}": 
                True_(),
            f"{Regions.cheese_bridge_region} -> {Locations.cheese_bridge_exit_1}": 
                CanClimb | HasYoshi,
            f"{Regions.cheese_bridge_region} -> {Locations.cheese_bridge_exit_2}": 
                CanCapeFly,
            f"{Regions.soda_lake_region} -> {Locations.soda_lake_exit_1}": 
                CanSwim,
            f"{Regions.cookie_mountain_region} -> {Locations.cookie_mountain_exit_1}": 
                True_(),
            f"{Regions.twin_bridges_castle_region} -> {Locations.twin_bridges_castle}": 
                CanRun & CanClimb,

            f"{Regions.forest_of_illusion_1_region} -> {Locations.forest_of_illusion_1_exit_1}": 
                True_(),
            f"{Regions.forest_of_illusion_1_region} -> {Locations.forest_of_illusion_1_exit_2}": 
                CanCarry & HasPBalloon,
            f"{Regions.forest_of_illusion_2_region} -> {Locations.forest_of_illusion_2_exit_1}": 
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            f"{Regions.forest_of_illusion_2_region} -> {Locations.forest_of_illusion_2_exit_2}": 
                CanCarryOrYoshiTongue & CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_1}": 
                CanCarry | HasYoshi,
            f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_2}": 
                (CanCarry | HasYoshi) & CanCarryOrYoshiTongue & CanBreakTurnBlocks,
            f"{Regions.forest_of_illusion_4_region} -> {Locations.forest_of_illusion_4_exit_1}": 
                True_(),
            f"{Regions.forest_of_illusion_4_region} -> {Locations.forest_of_illusion_4_exit_2}":
                True_(),
            f"{Regions.forest_ghost_house_region} -> {Locations.forest_ghost_house_exit_1}": 
                HasPSwitch,
            f"{Regions.forest_ghost_house_region} -> {Locations.forest_ghost_house_exit_2}": 
                HasPSwitch,
            f"{Regions.forest_secret_region} -> {Locations.forest_secret_exit_1}": 
                True_(),
            f"{Regions.forest_fortress_region} -> {Locations.forest_fortress}": 
                True_(),
            f"{Regions.forest_castle_region} -> {Locations.forest_castle}": 
                True_(),

            f"{Regions.chocolate_island_1_region} -> {Locations.chocolate_island_1_exit_1}": 
                HasPSwitch | HasYoshi,
            f"{Regions.chocolate_island_2_region} -> {Locations.chocolate_island_2_exit_1}": 
                True_(),
            f"{Regions.chocolate_island_2_region} -> {Locations.chocolate_island_2_exit_2}": 
                CanCarryOrYoshiTongue,
            f"{Regions.chocolate_island_3_region} -> {Locations.chocolate_island_3_exit_1}": 
                CanClimb | HasYoshi,
            f"{Regions.chocolate_island_3_region} -> {Locations.chocolate_island_3_exit_2}": 
                CanFly,
            f"{Regions.chocolate_island_4_region} -> {Locations.chocolate_island_4_exit_1}": 
                True_(),
            f"{Regions.chocolate_island_5_region} -> {Locations.chocolate_island_5_exit_1}": 
                True_(),
            f"{Regions.chocolate_ghost_house_region} -> {Locations.chocolate_ghost_house_exit_1}": 
                True_(),
            f"{Regions.chocolate_fortress_region} -> {Locations.chocolate_fortress}": 
                True_(),
            f"{Regions.chocolate_secret_region} -> {Locations.chocolate_secret_exit_1}": 
                True_(),
            f"{Regions.chocolate_castle_region} -> {Locations.chocolate_castle}": 
                True_(),
            f"{Regions.sunken_ghost_ship_region} -> {Locations.sunken_ghost_ship}": 
                CanSwim,

            f"{Regions.valley_of_bowser_1_region} -> {Locations.valley_of_bowser_1_exit_1}": 
                True_(),
            f"{Regions.valley_of_bowser_2_region} -> {Locations.valley_of_bowser_2_exit_1}": 
                True_(),
            f"{Regions.valley_of_bowser_2_region} -> {Locations.valley_of_bowser_2_exit_2}": 
                CanCarry,
            f"{Regions.valley_of_bowser_3_region} -> {Locations.valley_of_bowser_3_exit_1}": 
                True_(),
            f"{Regions.valley_of_bowser_4_region} -> {Locations.valley_of_bowser_4_exit_1}": 
                CanClimb,
            f"{Regions.valley_of_bowser_4_region} -> {Locations.valley_of_bowser_4_exit_2}": 
                CanYoshiCarry & CanClimb,
            f"{Regions.valley_ghost_house_region} -> {Locations.valley_ghost_house_exit_1}": 
                HasPSwitch,
            f"{Regions.valley_ghost_house_region} -> {Locations.valley_ghost_house_exit_2}": 
                HasPSwitch & CanCarry & CanRun,
            f"{Regions.valley_fortress_region} -> {Locations.valley_fortress}": 
                True_(),
            f"{Regions.valley_castle_region} -> {Locations.valley_castle}": 
                True_(),
            f"{Locations.front_door} -> {Regions.bowser_region}": 
                CanCarry & CanClimb & CanRun & CanSwim,
            f"{Locations.back_door} -> {Regions.bowser_region}": 
                CanCarry,

            f"{Regions.star_road_1_region} -> {Locations.star_road_1_exit_1}": 
                CanBreakTurnBlocks,
            f"{Regions.star_road_1_region} -> {Locations.star_road_1_exit_2}": 
                CanBreakTurnBlocks & CanCarryOrYoshiTongue,
            f"{Regions.star_road_2_region} -> {Locations.star_road_2_exit_1}": 
                CanSwim,
            f"{Regions.star_road_2_region} -> {Locations.star_road_2_exit_2}": 
                CanSwim & CanCarryOrYoshiTongue,
            f"{Regions.star_road_3_region} -> {Locations.star_road_3_exit_1}": 
                True_(),
            f"{Regions.star_road_3_region} -> {Locations.star_road_3_exit_2}": 
                CanCarry | (HasFireFlower & CanYoshiCarry),
            f"{Regions.star_road_4_region} -> {Locations.star_road_4_exit_1}": 
                True_(),
            f"{Regions.star_road_4_region} -> {Locations.star_road_4_exit_2}": 
                CanYoshiFly | (CanCarry & (HasFeather | (HasGSP & HasRSP))),
            f"{Regions.star_road_5_region} -> {Locations.star_road_5_exit_1}": 
                HasPSwitch | CanFly,
            f"{Regions.star_road_5_region} -> {Locations.star_road_5_exit_2}": 
                CanYoshiFly | (
                    CanCarry & CanClimb & HasPSwitch & 
                    HasYSP & HasGSP & HasRSP & HasBSP
                ) | (
                    CanFly & CanCarry
                ),
            f"{Regions.special_zone_1_region} -> {Locations.special_zone_1_exit_1}": 
                CanClimb & (
                    HasPSwitch | CanCapeFly
                ),
            f"{Regions.special_zone_2_region} -> {Locations.special_zone_2_exit_1}": 
                HasPBalloon,
            f"{Regions.special_zone_3_region} -> {Locations.special_zone_3_exit_1}": 
                CanClimb | HasYoshi,
            f"{Regions.special_zone_4_region} -> {Locations.special_zone_4_exit_1}": 
                (CanCarry | HasPSwitch) & HasSuperStar,
            f"{Regions.special_zone_5_region} -> {Locations.special_zone_5_exit_1}": 
                True_(),
            f"{Regions.special_zone_6_region} -> {Locations.special_zone_6_exit_1}": 
                True_(),
            f"{Regions.special_zone_7_region} -> {Locations.special_zone_7_exit_1}": 
                CanCarryOrYoshiTongue,
            f"{Regions.special_zone_8_region} -> {Locations.special_zone_8_exit_1}": 
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
        }
    
    
        self.carryless_exit_rules = {
            f"{Regions.donut_plains_1_region} -> {Locations.donut_plains_1_exit_2}": 
                HasGSP | CanCapeFly | CanYoshiCarry,
            f"{Regions.donut_plains_2_region} -> {Locations.donut_plains_2_exit_2}": 
                CanYoshiCarry | (CanClimb & (
                    (CanCarry & CanBreakTurnBlocks) | HasYoshi)
                ),
            f"{Regions.donut_secret_1_region} -> {Locations.donut_secret_1_exit_2}": 
                CanSwim,

            f"{Regions.vanilla_dome_1_region} -> {Locations.vanilla_dome_1_exit_2}": 
                CanClimb & (
                    HasYoshi | HasRSP
                ),
            f"{Regions.vanilla_dome_2_region} -> {Locations.vanilla_dome_2_exit_2}": 
                CanSwim & CanCarry & HasPSwitch & (
                    CanClimb | HasYoshi
                ),

            f"{Regions.forest_of_illusion_1_region} -> {Locations.forest_of_illusion_1_exit_2}": 
                HasPBalloon,
            f"{Regions.forest_of_illusion_2_region} -> {Locations.forest_of_illusion_2_exit_2}": 
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_2}": 
                (CanCarry | HasYoshi) & CanCarryOrYoshiTongue & CanBreakTurnBlocks,
            f"{Regions.forest_of_illusion_4_region} -> {Locations.forest_of_illusion_4_exit_2}":
                True_(),

            f"{Regions.chocolate_island_2_region} -> {Locations.chocolate_island_2_exit_2}": 
                True_(),

            f"{Regions.valley_of_bowser_2_region} -> {Locations.valley_of_bowser_2_exit_2}": 
                True_(),
            f"{Regions.valley_of_bowser_4_region} -> {Locations.valley_of_bowser_4_exit_2}": 
                CanClimb,
            f"{Regions.valley_ghost_house_region} -> {Locations.valley_ghost_house_exit_2}": 
                HasPSwitch & CanCarry & CanRun,

            f"{Regions.star_road_1_region} -> {Locations.star_road_1_exit_2}": 
                CanBreakTurnBlocks,
            f"{Regions.star_road_2_region} -> {Locations.star_road_2_exit_2}": 
                CanSwim,
            f"{Regions.star_road_3_region} -> {Locations.star_road_3_exit_2}": 
                CanCarry | HasFireFlower,
            f"{Regions.star_road_4_region} -> {Locations.star_road_4_exit_2}": 
                CanYoshiFly | HasFeather | (HasGSP & HasRSP),
            f"{Regions.star_road_5_region} -> {Locations.star_road_5_exit_2}": 
                CanYoshiFly | (
                    CanClimb & HasPSwitch & 
                    HasYSP & HasGSP & HasRSP & HasBSP
                ) | (
                    CanFly & CanSpinJump
                ),
        }
    
        self.location_rules = {
            Locations.yoshis_island_1_dragon:
                CanBreakTurnBlocks,
            Locations.yoshis_island_1_moon:
                CanCapeFly,
            Locations.yoshis_island_1_midway:
                True_(),
            Locations.yoshis_island_1_flying_block_1:
                True_(),
            Locations.yoshis_island_1_yellow_block_1:
                True_(),
            Locations.yoshis_island_1_life_block_1:
                True_(),
            Locations.yoshis_island_1_powerup_block_1:
                True_(),
            Locations.yoshis_island_1_room_2:
                CanBreakTurnBlocks,

            Locations.yoshis_island_2_dragon:
                HasYoshi | CanClimb,
            Locations.yoshis_island_2_midway:
                True_(),
            Locations.yoshis_island_2_flying_block_1:
                CanCarry | HasYoshi,
            Locations.yoshis_island_2_flying_block_2:
                CanCarry | HasYoshi,
            Locations.yoshis_island_2_flying_block_3:
                CanCarry | HasYoshi,
            Locations.yoshis_island_2_flying_block_4:
                CanCarry | HasYoshi,
            Locations.yoshis_island_2_flying_block_5:
                CanCarry | HasYoshi,
            Locations.yoshis_island_2_flying_block_6:
                CanCarry | HasYoshi,
            Locations.yoshis_island_2_coin_block_1:
                True_(),
            Locations.yoshis_island_2_yellow_block_1:
                True_(),
            Locations.yoshis_island_2_coin_block_2:
                True_(),
            Locations.yoshis_island_2_coin_block_3:
                True_(),
            Locations.yoshis_island_2_yoshi_block_1:
                True_(),
            Locations.yoshis_island_2_coin_block_4:
                True_(),
            Locations.yoshis_island_2_yoshi_block_2:
                True_(),
            Locations.yoshis_island_2_coin_block_5:
                True_(),
            Locations.yoshis_island_2_vine_block_1:
                True_(),
            Locations.yoshis_island_2_yellow_block_2:
                True_(),

            Locations.yoshis_island_3_dragon:
                HasPSwitch,
            Locations.yoshis_island_3_prize:
                True_(),
            Locations.yoshis_island_3_midway:
                True_(),
            Locations.yoshis_island_3_yellow_block_1:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_2:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_3:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_4:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_5:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_6:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_7:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_8:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_9:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_10:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_11:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_12:
                True_(),
            Locations.yoshis_island_3_yellow_block_13:
                True_(),
            Locations.yoshis_island_3_yellow_block_14:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_15:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_16:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_17:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_18:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_19:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_20:
                CanCarry | HasYoshi,
            Locations.yoshis_island_3_yellow_block_21:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_22:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_23:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_24:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_25:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_26:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_27:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_28:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_29:
                CanYoshiFly,
            Locations.yoshis_island_3_coin_block_1:
                True_(),
            Locations.yoshis_island_3_yoshi_block_1:
                True_(),
            Locations.yoshis_island_3_yellow_block_30:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_31:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_32:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_33:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_34:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_35:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_36:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_37:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_38:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_39:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_40:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_41:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_42:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_43:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_44:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_45:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_46:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_47:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_48:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_49:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_50:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_51:
                CanYoshiFly,
            Locations.yoshis_island_3_coin_block_2:
                True_(),
            Locations.yoshis_island_3_powerup_block_1:
                True_(),
            Locations.yoshis_island_3_yellow_block_52:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_53:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_54:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_55:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_56:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_57:
                True_(),
            Locations.yoshis_island_3_yellow_block_58:
                True_(),
            Locations.yoshis_island_3_yellow_block_59:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_60:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_61:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_62:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_63:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_64:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_65:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_66:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_67:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_68:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_69:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_70:
                True_(),
            Locations.yoshis_island_3_yellow_block_71:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_72:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_73:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_74:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_75:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_76:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_77:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_78:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_79:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_80:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_81:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_82:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_83:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_84:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_85:
                CanYoshiFly,
            Locations.yoshis_island_3_yellow_block_86:
                CanYoshiFly,

            Locations.yoshis_island_4_dragon:
                HasYoshi | CanSwim | HasPSwitch,
            Locations.yoshis_island_4_hidden_1up:
                HasYoshi | CanCapeFly,
            Locations.yoshis_island_4_yellow_block_1:
                True_(),
            Locations.yoshis_island_4_powerup_block_1:
                True_(),
            Locations.yoshis_island_4_multi_coin_block_1:
                True_(),
            Locations.yoshis_island_4_star_block_1:
                True_(),
                
            Locations.yoshis_island_castle_midway:
                CanClimb,
            Locations.yoshis_island_castle_coin_block_1:
                CanCarry | CanClimb,
            Locations.yoshis_island_castle_coin_block_2:
                CanCarry | CanClimb,
            Locations.yoshis_island_castle_powerup_block_1:
                CanCarry | CanClimb,
            Locations.yoshis_island_castle_coin_block_3:
                CanCarry | CanClimb,
            Locations.yoshis_island_castle_coin_block_4:
                CanCarry | CanClimb,
            Locations.yoshis_island_castle_flying_block_1:
                CanClimb,
            Locations.yoshis_island_castle_room_2:
                CanClimb,

            Locations.yellow_switch_palace:
                True_(),

            Locations.donut_plains_1_dragon:
                CanClimb | HasYoshi | CanCapeFly,
            Locations.donut_plains_1_hidden_1up:
                True_(),
            Locations.donut_plains_1_midway:
                True_(),
            Locations.donut_plains_1_coin_block_1:
                True_(),
            Locations.donut_plains_1_coin_block_2:
                True_(),
            Locations.donut_plains_1_yoshi_block_1:
                True_(),
            Locations.donut_plains_1_vine_block_1:
                True_(),
            Locations.donut_plains_1_green_block_1:
                HasFeather,
            Locations.donut_plains_1_green_block_2:
                HasFeather,
            Locations.donut_plains_1_green_block_3:
                HasFeather,
            Locations.donut_plains_1_green_block_4:
                HasFeather,
            Locations.donut_plains_1_green_block_5:
                HasFeather,
            Locations.donut_plains_1_green_block_6:
                HasFeather,
            Locations.donut_plains_1_green_block_7:
                HasFeather,
            Locations.donut_plains_1_green_block_8:
                HasFeather,
            Locations.donut_plains_1_green_block_9:
                HasFeather,
            Locations.donut_plains_1_green_block_10:
                HasFeather,
            Locations.donut_plains_1_green_block_11:
                HasFeather,
            Locations.donut_plains_1_green_block_12:
                HasFeather,
            Locations.donut_plains_1_green_block_13:
                HasFeather,
            Locations.donut_plains_1_green_block_14:
                HasFeather,
            Locations.donut_plains_1_green_block_15:
                HasFeather,
            Locations.donut_plains_1_green_block_16:
                HasFeather,
            Locations.donut_plains_1_yellow_block_1:
                True_(),
            Locations.donut_plains_1_yellow_block_2:
                True_(),
            Locations.donut_plains_1_yellow_block_3:
                True_(),
            Locations.donut_plains_1_room_2:
                HasYSP,

            Locations.donut_plains_2_dragon:
                True_(),
            Locations.donut_plains_2_coin_block_1:
                True_(),
            Locations.donut_plains_2_coin_block_2:
                True_(),
            Locations.donut_plains_2_coin_block_3:
                True_(),
            Locations.donut_plains_2_yellow_block_1:
                True_(),
            Locations.donut_plains_2_powerup_block_1:
                True_(),
            Locations.donut_plains_2_multi_coin_block_1:
                True_(),
            Locations.donut_plains_2_flying_block_1:
                True_(),
            Locations.donut_plains_2_green_block_1:
                True_(),
            Locations.donut_plains_2_yellow_block_2:
                True_(),
            Locations.donut_plains_2_vine_block_1:
                (CanBreakTurnBlocks & CanCarry) | HasYoshi,

            Locations.donut_plains_3_dragon:
                (CanBreakTurnBlocks & CanClimb) | HasYoshi |
                    CanCapeFly,
            Locations.donut_plains_3_prize:
                (CanBreakTurnBlocks & CanClimb) | HasYoshi |
                    CanCapeFly,
            Locations.donut_plains_3_midway:
                True_(),
            Locations.donut_plains_3_green_block_1:
                True_(),
            Locations.donut_plains_3_coin_block_1:
                True_(),
            Locations.donut_plains_3_coin_block_2:
                True_(),
            Locations.donut_plains_3_vine_block_1:
                CanBreakTurnBlocks,
            Locations.donut_plains_3_powerup_block_1:
                True_(),

            Locations.donut_plains_4_dragon:
                True_(),
            Locations.donut_plains_4_moon:
                CanCapeFly,
            Locations.donut_plains_4_hidden_1up:
                CanCapeFly,
            Locations.donut_plains_4_midway:
                True_(),
            Locations.donut_plains_4_coin_block_1:
                True_(),
            Locations.donut_plains_4_powerup_block_1:
                True_(),
            Locations.donut_plains_4_coin_block_2:
                True_(),
            Locations.donut_plains_4_yoshi_block_1:
                True_(),

            Locations.donut_secret_1_dragon:
                CanSwim,
            Locations.donut_secret_1_coin_block_1:
                CanSwim,
            Locations.donut_secret_1_coin_block_2:
                CanSwim,
            Locations.donut_secret_1_powerup_block_1:
                CanSwim,
            Locations.donut_secret_1_coin_block_3:
                CanSwim,
            Locations.donut_secret_1_powerup_block_2:
                CanSwim,
            Locations.donut_secret_1_powerup_block_3:
                CanSwim & HasPBalloon,
            Locations.donut_secret_1_life_block_1:
                CanSwim & HasPBalloon,
            Locations.donut_secret_1_powerup_block_4:
                CanSwim & HasPBalloon,
            Locations.donut_secret_1_powerup_block_5:
                CanSwim,
            Locations.donut_secret_1_key_block_1:
                CanSwim & CanCarry & HasPSwitch,
            Locations.donut_secret_1_room_2:
                CanSwim,

            Locations.donut_secret_2_dragon:
                CanClimb | HasYoshi,
            Locations.donut_secret_2_directional_coin_block_1:
                True_(),
            Locations.donut_secret_2_vine_block_1:
                True_(),
            Locations.donut_secret_2_star_block_1:
                CanClimb | HasYoshi,
            Locations.donut_secret_2_powerup_block_1:
                True_(),
            Locations.donut_secret_2_star_block_2:
                True_(),

            Locations.donut_ghost_house_vine_block_1:
                True_(),
            Locations.donut_ghost_house_directional_coin_block_1:
                HasPSwitch,
            Locations.donut_ghost_house_life_block_1:
                CanCapeFly,
            Locations.donut_ghost_house_life_block_2:
                CanCapeFly,
            Locations.donut_ghost_house_life_block_3:
                CanCapeFly,
            Locations.donut_ghost_house_life_block_4:
                CanCapeFly,
            Locations.donut_ghost_house_room_2:
                CanCapeFly,
            Locations.donut_ghost_house_room_5:
                HasPSwitch,
            Locations.donut_ghost_house_room_6:
                CanClimb,

            Locations.donut_secret_house_powerup_block_1:
                True_(),
            Locations.donut_secret_house_multi_coin_block_1:
                True_(),
            Locations.donut_secret_house_life_block_1:
                HasPSwitch,
            Locations.donut_secret_house_vine_block_1:
                HasPSwitch,
            Locations.donut_secret_house_directional_coin_block_1:
                HasPSwitch,
            Locations.donut_secret_house_room_3:
                HasPSwitch,
            Locations.donut_secret_house_room_4:
                HasPSwitch,
            Locations.donut_secret_house_room_5:
                HasPSwitch & (
                    CanClimb | CanCapeFly
                ),

            Locations.donut_plains_castle_hidden_1up:
                True_(),
            Locations.donut_plains_castle_yellow_block_1:
                True_(),
            Locations.donut_plains_castle_coin_block_1:
                True_(),
            Locations.donut_plains_castle_powerup_block_1:
                True_(),
            Locations.donut_plains_castle_coin_block_2:
                True_(),
            Locations.donut_plains_castle_vine_block_1:
                True_(),
            Locations.donut_plains_castle_invis_life_block_1:
                CanClimb,
            Locations.donut_plains_castle_coin_block_3:
                True_(),
            Locations.donut_plains_castle_coin_block_4:
                True_(),
            Locations.donut_plains_castle_coin_block_5:
                True_(),
            Locations.donut_plains_castle_green_block_1:
                True_(),
            Locations.donut_plains_castle_room_2:
                CanCapeFly,

            Locations.green_switch_palace:
                True_(),

            Locations.vanilla_dome_1_dragon:
                CanCarry & CanRun & (HasSuperStar | HasMushroom),
            Locations.vanilla_dome_1_midway:
                CanRun & (HasSuperStar | HasMushroom),
            Locations.vanilla_dome_1_flying_block_1:
                True_(),
            Locations.vanilla_dome_1_powerup_block_1:
                True_(),
            Locations.vanilla_dome_1_powerup_block_2:
                True_(),
            Locations.vanilla_dome_1_coin_block_1:
                True_(),
            Locations.vanilla_dome_1_life_block_1:
                True_(),
            Locations.vanilla_dome_1_powerup_block_3:
                True_(),
            Locations.vanilla_dome_1_vine_block_1:
                HasRSP | CanCarry | HasYoshi,
            Locations.vanilla_dome_1_star_block_1:
                True_(),
            Locations.vanilla_dome_1_powerup_block_4:
                CanRun & (HasSuperStar | HasMushroom),
            Locations.vanilla_dome_1_coin_block_2:
                CanRun & (HasSuperStar | HasMushroom),

            Locations.vanilla_dome_2_dragon:
                CanSwim & HasPSwitch & CanCarry & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_midway:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_coin_block_1:
                CanSwim,
            Locations.vanilla_dome_2_powerup_block_1:
                CanSwim,
            Locations.vanilla_dome_2_coin_block_2:
                CanSwim,
            Locations.vanilla_dome_2_coin_block_3:
                CanSwim,
            Locations.vanilla_dome_2_vine_block_1:
                CanSwim,
            Locations.vanilla_dome_2_invis_life_block_1:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_coin_block_4:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_coin_block_5:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_powerup_block_2:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_powerup_block_3:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_powerup_block_4:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_powerup_block_5:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_multi_coin_block_1:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_multi_coin_block_2:
                CanSwim & (
                    CanClimb | HasYoshi
                ),
            Locations.vanilla_dome_2_room_2:
                CanSwim & (
                    CanClimb | HasYoshi
                ),

            Locations.vanilla_dome_3_dragon:
                True_(),
            Locations.vanilla_dome_3_moon:
                CanCapeFly,
            Locations.vanilla_dome_3_midway:
                True_(),
            Locations.vanilla_dome_3_coin_block_1:
                True_(),
            Locations.vanilla_dome_3_flying_block_1:
                True_(),
            Locations.vanilla_dome_3_flying_block_2:
                True_(),
            Locations.vanilla_dome_3_powerup_block_1:
                True_(),
            Locations.vanilla_dome_3_flying_block_3:
                True_(),
            Locations.vanilla_dome_3_invis_coin_block_1:
                True_(),
            Locations.vanilla_dome_3_powerup_block_2:
                True_(),
            Locations.vanilla_dome_3_multi_coin_block_1:
                True_(),
            Locations.vanilla_dome_3_powerup_block_3:
                True_(),
            Locations.vanilla_dome_3_yoshi_block_1:
                CanCarry | HasYoshi,
            Locations.vanilla_dome_3_powerup_block_4:
                True_(),
            Locations.vanilla_dome_3_pswitch_coin_block_1:
                CanCapeFly & HasPSwitch,
            Locations.vanilla_dome_3_pswitch_coin_block_2:
                CanCapeFly & HasPSwitch,
            Locations.vanilla_dome_3_pswitch_coin_block_3:
                CanCapeFly & HasPSwitch,
            Locations.vanilla_dome_3_pswitch_coin_block_4:
                CanCapeFly & HasPSwitch,
            Locations.vanilla_dome_3_pswitch_coin_block_5:
                CanCapeFly & HasPSwitch,
            Locations.vanilla_dome_3_pswitch_coin_block_6:
                CanCapeFly & HasPSwitch,
            Locations.vanilla_dome_3_room_2:
                CanCapeFly,

            Locations.vanilla_dome_4_dragon:
                True_(),
            Locations.vanilla_dome_4_hidden_1up:
                True_(),
            Locations.vanilla_dome_4_powerup_block_1:
                True_(),
            Locations.vanilla_dome_4_powerup_block_2:
                True_(),
            Locations.vanilla_dome_4_coin_block_1:
                True_(),
            Locations.vanilla_dome_4_coin_block_2:
                True_(),
            Locations.vanilla_dome_4_coin_block_3:
                True_(),
            Locations.vanilla_dome_4_life_block_1:
                True_(),
            Locations.vanilla_dome_4_coin_block_4:
                True_(),
            Locations.vanilla_dome_4_coin_block_5:
                True_(),
            Locations.vanilla_dome_4_coin_block_6:
                True_(),
            Locations.vanilla_dome_4_coin_block_7:
                True_(),
            Locations.vanilla_dome_4_coin_block_8:
                CanCarry,

            Locations.vanilla_secret_1_dragon:
                CanClimb & CanCarry,
            Locations.vanilla_secret_1_coin_block_1:
                True_(),
            Locations.vanilla_secret_1_powerup_block_1:
                True_(),
            Locations.vanilla_secret_1_multi_coin_block_1:
                True_(),
            Locations.vanilla_secret_1_vine_block_1:
                True_(),
            Locations.vanilla_secret_1_vine_block_2:
                CanClimb,
            Locations.vanilla_secret_1_coin_block_2:
                CanClimb,
            Locations.vanilla_secret_1_coin_block_3:
                CanClimb,
            Locations.vanilla_secret_1_powerup_block_2:
                CanClimb,
            Locations.vanilla_secret_1_room_2:
                CanClimb,
            Locations.vanilla_secret_1_room_3:
                CanClimb & CanCarry & HasBSP,

            Locations.vanilla_secret_2_dragon:
                CanCapeFly,
            Locations.vanilla_secret_2_yoshi_block_1:
                True_(),
            Locations.vanilla_secret_2_green_block_1:
                True_(),
            Locations.vanilla_secret_2_powerup_block_1:
                True_(),
            Locations.vanilla_secret_2_powerup_block_2:
                True_(),
            Locations.vanilla_secret_2_multi_coin_block_1:
                True_(),
            Locations.vanilla_secret_2_gray_pow_block_1:
                True_(),
            Locations.vanilla_secret_2_coin_block_1:
                True_(),
            Locations.vanilla_secret_2_coin_block_2:
                True_(),
            Locations.vanilla_secret_2_coin_block_3:
                True_(),
            Locations.vanilla_secret_2_coin_block_4:
                True_(),
            Locations.vanilla_secret_2_coin_block_5:
                True_(),
            Locations.vanilla_secret_2_coin_block_6:
                True_(),

            Locations.vanilla_secret_3_dragon:
                CanSwim,
            Locations.vanilla_secret_3_powerup_block_1:
                CanSwim,
            Locations.vanilla_secret_3_powerup_block_2:
                CanSwim,
            Locations.vanilla_secret_3_room_2:
                CanSwim,

            Locations.vanilla_ghost_house_dragon:
                CanClimb,
            Locations.vanilla_ghost_house_hidden_1up:
                True_(),
            Locations.vanilla_ghost_house_powerup_block_1:
                True_(),
            Locations.vanilla_ghost_house_vine_block_1:
                True_(),
            Locations.vanilla_ghost_house_powerup_block_2:
                True_(),
            Locations.vanilla_ghost_house_multi_coin_block_1:
                True_(),
            Locations.vanilla_ghost_house_blue_pow_block_1:
                True_(),
            Locations.vanilla_ghost_house_room_3:
                HasPSwitch,
                
            Locations.vanilla_fortress_hidden_1up:
                CanSwim,
            Locations.vanilla_fortress_powerup_block_1:
                CanSwim,
            Locations.vanilla_fortress_powerup_block_2:
                CanSwim,
            Locations.vanilla_fortress_yellow_block_1:
                CanSwim,
            Locations.vanilla_fortress_room_2:
                CanSwim,

            Locations.vanilla_dome_castle_life_block_1:
                HasMushroom,
            Locations.vanilla_dome_castle_life_block_2:
                HasMushroom,
            Locations.vanilla_dome_castle_powerup_block_1:
                True_(),
            Locations.vanilla_dome_castle_life_block_3:
                HasPSwitch,
            Locations.vanilla_dome_castle_midway:
                HasPSwitch,
            Locations.vanilla_dome_castle_room_2:
                HasPSwitch,

            Locations.red_switch_palace:
                True_(),

            Locations.butter_bridge_1_dragon:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_prize:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_powerup_block_1:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_multi_coin_block_1:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_multi_coin_block_2:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_multi_coin_block_3:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_life_block_1:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),
            Locations.butter_bridge_1_room_2:
                True_(options=[OptionFilter(EnemyShuffle, 0)]) | 
                Has(Items.red_switch_palace, options=[OptionFilter(EnemyShuffle, 1)]),

            Locations.butter_bridge_2_dragon:
                CanFly,
            Locations.butter_bridge_2_powerup_block_1:
                CanCarry,
            Locations.butter_bridge_2_green_block_1:
                True_(),
            Locations.butter_bridge_2_yoshi_block_1:
                CanCarry,

            Locations.cheese_bridge_dragon:
                CanClimb | HasYoshi,
            Locations.cheese_bridge_moon:
                CanCapeFly,
            Locations.cheese_bridge_powerup_block_1:
                True_(),
            Locations.cheese_bridge_powerup_block_2:
                True_(),
            Locations.cheese_bridge_wings_block_1:
                True_(),
            Locations.cheese_bridge_powerup_block_3:
                True_(),
            Locations.cheese_bridge_room_3:
                HasYoshi,

            Locations.cookie_mountain_dragon:
                CanClimb | HasYoshi,
            Locations.cookie_mountain_hidden_1up:
                CanSwim | CanWallRun,
            Locations.cookie_mountain_coin_block_1:
                True_(),
            Locations.cookie_mountain_coin_block_2:
                True_(),
            Locations.cookie_mountain_coin_block_3:
                True_(),
            Locations.cookie_mountain_coin_block_4:
                True_(),
            Locations.cookie_mountain_coin_block_5:
                True_(),
            Locations.cookie_mountain_coin_block_6:
                True_(),
            Locations.cookie_mountain_coin_block_7:
                True_(),
            Locations.cookie_mountain_coin_block_8:
                True_(),
            Locations.cookie_mountain_coin_block_9:
                True_(),
            Locations.cookie_mountain_powerup_block_1:
                True_(),
            Locations.cookie_mountain_life_block_1:
                CanClimb,
            Locations.cookie_mountain_vine_block_1:
                True_(),
            Locations.cookie_mountain_yoshi_block_1:
                HasRSP,
            Locations.cookie_mountain_coin_block_10:
                True_(),
            Locations.cookie_mountain_coin_block_11:
                True_(),
            Locations.cookie_mountain_powerup_block_2:
                True_(),
            Locations.cookie_mountain_coin_block_12:
                True_(),
            Locations.cookie_mountain_coin_block_13:
                True_(),
            Locations.cookie_mountain_coin_block_14:
                True_(),
            Locations.cookie_mountain_coin_block_15:
                True_(),
            Locations.cookie_mountain_coin_block_16:
                True_(),
            Locations.cookie_mountain_coin_block_17:
                True_(),
            Locations.cookie_mountain_coin_block_18:
                True_(),
            Locations.cookie_mountain_coin_block_19:
                True_(),
            Locations.cookie_mountain_coin_block_20:
                True_(),
            Locations.cookie_mountain_coin_block_21:
                True_(),
            Locations.cookie_mountain_coin_block_22:
                True_(),
            Locations.cookie_mountain_coin_block_23:
                True_(),
            Locations.cookie_mountain_coin_block_24:
                True_(),
            Locations.cookie_mountain_coin_block_25:
                True_(),
            Locations.cookie_mountain_coin_block_26:
                True_(),
            Locations.cookie_mountain_coin_block_27:
                True_(),
            Locations.cookie_mountain_coin_block_28:
                True_(),
            Locations.cookie_mountain_coin_block_29:
                True_(),
            Locations.cookie_mountain_coin_block_30:
                True_(),

            Locations.soda_lake_dragon:
                CanSwim,
            Locations.soda_lake_powerup_block_1:
                CanSwim,
            Locations.soda_lake_room_2:
                CanSwim,

            Locations.twin_bridges_castle_powerup_block_1:
                CanRun & CanClimb,

            Locations.forest_of_illusion_1_powerup_block_1:
                True_(),
            Locations.forest_of_illusion_1_yoshi_block_1:
                True_(),
            Locations.forest_of_illusion_1_powerup_block_2:
                True_(),
            Locations.forest_of_illusion_1_key_block_1:
                HasPBalloon,
            Locations.forest_of_illusion_1_life_block_1:
                True_(),

            Locations.forest_of_illusion_2_dragon:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_green_block_1:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_powerup_block_1:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_invis_coin_block_1:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_invis_coin_block_2:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_invis_life_block_1:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_invis_coin_block_3:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),
            Locations.forest_of_illusion_2_yellow_block_1:
                CanSwim & 
                Has(Items.super_star_active, 3, options=[OptionFilter(EnemyShuffle, 1)], filtered_resolution=True),

            Locations.forest_of_illusion_3_dragon:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_hidden_1up:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_yoshi_block_1:
                True_(),
            Locations.forest_of_illusion_3_coin_block_1:
                True_(),
            Locations.forest_of_illusion_3_multi_coin_block_1:
                True_(),
            Locations.forest_of_illusion_3_coin_block_2:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_multi_coin_block_2:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_3:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_4:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_5:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_6:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_7:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_8:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_9:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_10:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_11:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_12:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_13:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_14:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_15:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_16:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_17:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_18:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_19:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_20:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_21:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_22:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_23:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_coin_block_24:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_midway:
                CanCarry | HasYoshi,
            Locations.forest_of_illusion_3_room_1:
                True_(),
            Locations.forest_of_illusion_3_room_2:
                True_(),
            Locations.forest_of_illusion_3_room_3:
                CanCarry | HasYoshi,

            Locations.forest_of_illusion_4_dragon:
                HasYoshi | CanCarry | HasPSwitch | HasFireFlower,
            Locations.forest_of_illusion_4_multi_coin_block_1:
                True_(),
            Locations.forest_of_illusion_4_coin_block_1:
                True_(),
            Locations.forest_of_illusion_4_coin_block_2:
                True_(),
            Locations.forest_of_illusion_4_coin_block_3:
                True_(),
            Locations.forest_of_illusion_4_coin_block_4:
                True_(),
            Locations.forest_of_illusion_4_powerup_block_1:
                True_(),
            Locations.forest_of_illusion_4_coin_block_5:
                True_(),
            Locations.forest_of_illusion_4_coin_block_6:
                True_(),
            Locations.forest_of_illusion_4_coin_block_7:
                True_(),
            Locations.forest_of_illusion_4_powerup_block_2:
                True_(),
            Locations.forest_of_illusion_4_coin_block_8:
                True_(),
            Locations.forest_of_illusion_4_coin_block_9:
                True_(),
            Locations.forest_of_illusion_4_coin_block_10:
                True_(),
            Locations.forest_of_illusion_4_room_2:
                True_(),

            Locations.forest_ghost_house_dragon:
                HasPSwitch,
            Locations.forest_ghost_house_moon:
                HasPSwitch,
            Locations.forest_ghost_house_coin_block_1:
                True_(),
            Locations.forest_ghost_house_powerup_block_1:
                True_(),
            Locations.forest_ghost_house_flying_block_1:
                True_(),
            Locations.forest_ghost_house_powerup_block_2:
                True_(),
            Locations.forest_ghost_house_life_block_1:
                True_(),
            Locations.forest_ghost_house_room_3:
                HasPSwitch,
            Locations.forest_ghost_house_room_4:
                HasPSwitch,

            Locations.forest_secret_dragon:
                True_(),
            Locations.forest_secret_powerup_block_1:
                True_(),
            Locations.forest_secret_powerup_block_2:
                True_(),
            Locations.forest_secret_life_block_1:
                HasBSP,

            Locations.forest_fortress_yellow_block_1:
                True_(),
            Locations.forest_fortress_powerup_block_1:
                True_(),
            Locations.forest_fortress_life_block_1:
                CanCapeFly,
            Locations.forest_fortress_life_block_2:
                CanCapeFly,
            Locations.forest_fortress_life_block_3:
                CanCapeFly,
            Locations.forest_fortress_life_block_4:
                CanCapeFly,
            Locations.forest_fortress_life_block_5:
                CanCapeFly,
            Locations.forest_fortress_life_block_6:
                CanCapeFly,
            Locations.forest_fortress_life_block_7:
                CanCapeFly,
            Locations.forest_fortress_life_block_8:
                CanCapeFly,
            Locations.forest_fortress_life_block_9:
                CanCapeFly,

            Locations.forest_castle_dragon:
                True_(),
            Locations.forest_castle_green_block_1:
                True_(),

            Locations.blue_switch_palace:
                True_(),

            Locations.chocolate_island_1_dragon:
                HasPSwitch | HasYoshi,
            Locations.chocolate_island_1_moon:
                CanCapeFly,
            Locations.chocolate_island_1_flying_block_1:
                True_(),
            Locations.chocolate_island_1_flying_block_2:
                HasPSwitch | HasYoshi,
            Locations.chocolate_island_1_yoshi_block_1:
                HasPSwitch | HasYoshi,
            Locations.chocolate_island_1_green_block_1:
                (HasPSwitch | HasYoshi) & (
                    (HasGSP & HasBSP) |
                    (HasYSP & HasBSP)
                ),
            Locations.chocolate_island_1_life_block_1:
                HasPSwitch | HasYoshi,
            Locations.chocolate_island_1_room_2:
                HasPSwitch | HasYoshi,
                
            Locations.chocolate_island_2_dragon:
                HasBSP & (
                    HasPSwitch | HasGSP | HasYoshi | (
                        HasYSP & HasRSP
                    )),
            Locations.chocolate_island_2_hidden_1up:
                True_(),
            Locations.chocolate_island_2_multi_coin_block_1:
                True_(),
            Locations.chocolate_island_2_invis_coin_block_1:
                True_(),
            Locations.chocolate_island_2_yoshi_block_1:
                True_(),
            Locations.chocolate_island_2_coin_block_1:
                True_(),
            Locations.chocolate_island_2_coin_block_2:
                True_(),
            Locations.chocolate_island_2_multi_coin_block_2:
                True_(),
            Locations.chocolate_island_2_powerup_block_1:
                True_(),
            Locations.chocolate_island_2_blue_pow_block_1:
                True_(),
            Locations.chocolate_island_2_yellow_block_1:
                True_(),
            Locations.chocolate_island_2_yellow_block_2:
                True_(),
            Locations.chocolate_island_2_green_block_1:
                True_(),
            Locations.chocolate_island_2_green_block_2:
                True_(),
            Locations.chocolate_island_2_green_block_3:
                True_(),
            Locations.chocolate_island_2_green_block_4:
                True_(),
            Locations.chocolate_island_2_green_block_5:
                True_(),
            Locations.chocolate_island_2_green_block_6:
                True_(),

            Locations.chocolate_island_3_dragon:
                True_(),
            Locations.chocolate_island_3_prize:
                True_(),
            Locations.chocolate_island_3_powerup_block_1:
                True_(),
            Locations.chocolate_island_3_powerup_block_2:
                True_(),
            Locations.chocolate_island_3_powerup_block_3:
                True_(),
            Locations.chocolate_island_3_green_block_1:
                True_(),
            Locations.chocolate_island_3_vine_block_1:
                True_(),
            Locations.chocolate_island_3_life_block_1:
                CanFly,
            Locations.chocolate_island_3_life_block_2:
                CanFly,
            Locations.chocolate_island_3_life_block_3:
                CanFly,

            Locations.chocolate_island_4_dragon:
                HasPSwitch & HasFeather,
            Locations.chocolate_island_4_yellow_block_1:
                HasBSP,
            Locations.chocolate_island_4_blue_pow_block_1:
                True_(),
            Locations.chocolate_island_4_powerup_block_1:
                True_(),
            Locations.chocolate_island_4_room_2:
                HasPSwitch,

            Locations.chocolate_island_5_dragon:
                True_(),
            Locations.chocolate_island_5_yoshi_block_1:
                True_(),
            Locations.chocolate_island_5_powerup_block_1:
                HasPSwitch,
            Locations.chocolate_island_5_life_block_1:
                HasPSwitch & (CanCarry | HasFeather),
            Locations.chocolate_island_5_yellow_block_1:
                HasPSwitch,
            Locations.chocolate_island_5_room_2:
                HasPSwitch,

            Locations.chocolate_ghost_house_powerup_block_1:
                True_(),
            Locations.chocolate_ghost_house_powerup_block_2:
                True_(),
            Locations.chocolate_ghost_house_life_block_1:
                True_(),

            Locations.chocolate_secret_powerup_block_1:
                True_(),
            Locations.chocolate_secret_powerup_block_2:
                True_(),
            Locations.chocolate_secret_room_5:
                True_(),
                
            Locations.chocolate_fortress_powerup_block_1:
                True_(),
            Locations.chocolate_fortress_powerup_block_2:
                True_(),
            Locations.chocolate_fortress_coin_block_1:
                True_(),
            Locations.chocolate_fortress_coin_block_2:
                True_(),
            Locations.chocolate_fortress_green_block_1:
                True_(),

            Locations.chocolate_castle_hidden_1up:
                True_(),
            Locations.chocolate_castle_yellow_block_1:
                True_(),
            Locations.chocolate_castle_yellow_block_2:
                True_(),
            Locations.chocolate_castle_green_block_1:
                True_(),

            Locations.sunken_ghost_ship_dragon:
                CanSwim,
            Locations.sunken_ghost_ship_powerup_block_1:
                CanSwim,
            Locations.sunken_ghost_ship_star_block_1:
                CanSwim,
            Locations.sunken_ghost_ship_room_2:
                CanSwim,
            Locations.sunken_ghost_ship_room_3:
                CanSwim,

            Locations.valley_of_bowser_1_dragon:
                True_(),
            Locations.valley_of_bowser_1_moon:
                True_(),
            Locations.valley_of_bowser_1_green_block_1:
                True_(),
            Locations.valley_of_bowser_1_invis_coin_block_1:
                True_(),
            Locations.valley_of_bowser_1_invis_coin_block_2:
                True_(),
            Locations.valley_of_bowser_1_invis_coin_block_3:
                True_(),
            Locations.valley_of_bowser_1_yellow_block_1:
                HasFeather,
            Locations.valley_of_bowser_1_yellow_block_2:
                HasFeather,
            Locations.valley_of_bowser_1_yellow_block_3:
                HasFeather,
            Locations.valley_of_bowser_1_yellow_block_4:
                HasFeather,
            Locations.valley_of_bowser_1_vine_block_1:
                True_(),
            Locations.valley_of_bowser_1_room_2:
                CanClimb,

            Locations.valley_of_bowser_2_dragon:
                HasYoshi,
            Locations.valley_of_bowser_2_hidden_1up:
                True_(),
            Locations.valley_of_bowser_2_powerup_block_1:
                True_(),
            Locations.valley_of_bowser_2_yellow_block_1:
                True_(),
            Locations.valley_of_bowser_2_powerup_block_2:
                True_(),
            Locations.valley_of_bowser_2_wings_block_1:
                True_(),

            Locations.valley_of_bowser_3_dragon:
                True_(),
            Locations.valley_of_bowser_3_powerup_block_1:
                True_(),
            Locations.valley_of_bowser_3_powerup_block_2:
                CanCarry,

            Locations.valley_of_bowser_4_yellow_block_1:
                True_(),
            Locations.valley_of_bowser_4_powerup_block_1:
                True_(),
            Locations.valley_of_bowser_4_vine_block_1:
                True_(),
            Locations.valley_of_bowser_4_yoshi_block_1:
                CanClimb,
            Locations.valley_of_bowser_4_life_block_1:
                CanClimb & CanBreakTurnBlocks,
            Locations.valley_of_bowser_4_powerup_block_2:
                CanClimb & HasYSP,
            Locations.valley_of_bowser_4_midway:
                CanClimb,

            Locations.valley_ghost_house_dragon:
                HasPSwitch,
            Locations.valley_ghost_house_pswitch_coin_block_1:
                HasPSwitch,
            Locations.valley_ghost_house_multi_coin_block_1:
                HasPSwitch,
            Locations.valley_ghost_house_powerup_block_1:
                True_(),
            Locations.valley_ghost_house_directional_coin_block_1:
                HasPSwitch,
            Locations.valley_ghost_house_room_3:
                HasPSwitch,
            Locations.valley_ghost_house_room_4:
                HasPSwitch,

            Locations.valley_fortress_green_block_1:
                True_(),
            Locations.valley_fortress_yellow_block_1:
                True_(),
                
            Locations.valley_castle_dragon:
                True_(),
            Locations.valley_castle_hidden_1up:
                True_(),
            Locations.valley_castle_yellow_block_1:
                True_(),
            Locations.valley_castle_yellow_block_2:
                True_(),
            Locations.valley_castle_green_block_1:
                True_(),

            Locations.star_road_1_dragon:
                CanBreakTurnBlocks,
            Locations.star_road_1_room_2:
                CanBreakTurnBlocks,

            Locations.star_road_2_star_block_1:
                CanSwim,
            Locations.star_road_2_room_2:
                CanSwim,

            Locations.star_road_3_key_block_1:
                CanCarry | HasFireFlower,

            Locations.star_road_4_powerup_block_1:
                True_(),
            Locations.star_road_4_green_block_1:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_green_block_2:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_green_block_3:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_green_block_4:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_green_block_5:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_green_block_6:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_green_block_7:
                CanYoshiFly | CanCapeSpinFly,
            Locations.star_road_4_key_block_1:
                CanYoshiFly | HasFeather | (CanCarry & HasGSP & HasRSP),

            Locations.star_road_5_directional_coin_block_1:
                True_(),
            Locations.star_road_5_life_block_1:
                HasPSwitch,
            Locations.star_road_5_vine_block_1:
                CanFly,
            Locations.star_road_5_yellow_block_1:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_2:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_3:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_4:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_5:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_6:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_7:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_8:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_9:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_10:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_11:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_12:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_13:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_14:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_15:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_16:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_17:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_18:
                CanYoshiFly,
            Locations.star_road_5_yellow_block_19:
                CanYoshiFly & HasGSP,
            Locations.star_road_5_yellow_block_20:
                CanYoshiFly & HasGSP,
            Locations.star_road_5_green_block_1:
                CanYoshiFly,
            Locations.star_road_5_green_block_2:
                CanYoshiFly,
            Locations.star_road_5_green_block_3:
                CanYoshiFly,
            Locations.star_road_5_green_block_4:
                CanYoshiFly,
            Locations.star_road_5_green_block_5:
                CanYoshiFly,
            Locations.star_road_5_green_block_6:
                CanYoshiFly,
            Locations.star_road_5_green_block_7:
                CanYoshiFly,
            Locations.star_road_5_green_block_8:
                CanYoshiFly,
            Locations.star_road_5_green_block_9:
                CanYoshiFly,
            Locations.star_road_5_green_block_10:
                CanYoshiFly,
            Locations.star_road_5_green_block_11:
                CanYoshiFly,
            Locations.star_road_5_green_block_12:
                CanYoshiFly,
            Locations.star_road_5_green_block_13:
                CanYoshiFly,
            Locations.star_road_5_green_block_14:
                CanYoshiFly,
            Locations.star_road_5_green_block_15:
                CanYoshiFly,
            Locations.star_road_5_green_block_16:
                CanYoshiFly,
            Locations.star_road_5_green_block_17:
                CanYoshiFly,
            Locations.star_road_5_green_block_18:
                CanYoshiFly,
            Locations.star_road_5_green_block_19:
                CanYoshiFly,
            Locations.star_road_5_green_block_20:
                CanYoshiFly,


            Locations.special_zone_1_dragon:
                CanClimb,
            Locations.special_zone_1_hidden_1up:
                CanClimb,
            Locations.special_zone_1_vine_block_1:
                True_(),
            Locations.special_zone_1_vine_block_2:
                True_(),
            Locations.special_zone_1_vine_block_3:
                True_(),
            Locations.special_zone_1_vine_block_4:
                True_(),
            Locations.special_zone_1_life_block_1:
                CanClimb,
            Locations.special_zone_1_vine_block_5:
                CanClimb,
            Locations.special_zone_1_blue_pow_block_1:
                CanClimb,
            Locations.special_zone_1_vine_block_6:
                CanClimb,
            Locations.special_zone_1_powerup_block_1:
                CanClimb,
            Locations.special_zone_1_pswitch_coin_block_1:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_2:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_3:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_4:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_5:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_6:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_7:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_8:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_9:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_10:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_11:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_12:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_pswitch_coin_block_13:
                CanClimb & HasPSwitch & HasFeather,
            Locations.special_zone_1_room_2:
                CanClimb,

            Locations.special_zone_2_dragon:
                HasPBalloon,
            Locations.special_zone_2_powerup_block_1:
                True_(),
            Locations.special_zone_2_coin_block_1:
                HasPBalloon,
            Locations.special_zone_2_coin_block_2:
                HasPBalloon,
            Locations.special_zone_2_powerup_block_2:
                HasPBalloon,
            Locations.special_zone_2_coin_block_3:
                HasPBalloon,
            Locations.special_zone_2_coin_block_4:
                HasPBalloon,
            Locations.special_zone_2_powerup_block_3:
                HasPBalloon,
            Locations.special_zone_2_multi_coin_block_1:
                HasPBalloon,
            Locations.special_zone_2_coin_block_5:
                HasPBalloon,
            Locations.special_zone_2_coin_block_6:
                HasPBalloon,

            Locations.special_zone_3_dragon:
                HasYoshi,
            Locations.special_zone_3_powerup_block_1:
                True_(),
            Locations.special_zone_3_yoshi_block_1:
                True_(),
            Locations.special_zone_3_wings_block_1:
                True_(),
            Locations.special_zone_3_room_3:
                HasYoshi,

            Locations.special_zone_4_dragon:
                (CanCarry | HasPSwitch) & HasSuperStar,
            Locations.special_zone_4_star_block_1:
                CanCarry | HasPSwitch,

            Locations.special_zone_5_dragon:
                True_(),
            Locations.special_zone_5_yoshi_block_1:
                True_(),

            Locations.special_zone_6_dragon:
                CanSwim,
            Locations.special_zone_6_powerup_block_1:
                CanSwim,
            Locations.special_zone_6_coin_block_1:
                CanSwim,
            Locations.special_zone_6_coin_block_2:
                CanSwim,
            Locations.special_zone_6_yoshi_block_1:
                CanSwim,
            Locations.special_zone_6_life_block_1:
                CanSwim,
            Locations.special_zone_6_multi_coin_block_1:
                CanSwim,
            Locations.special_zone_6_coin_block_3:
                CanSwim,
            Locations.special_zone_6_coin_block_4:
                CanSwim,
            Locations.special_zone_6_coin_block_5:
                CanSwim,
            Locations.special_zone_6_coin_block_6:
                CanSwim,
            Locations.special_zone_6_coin_block_7:
                CanSwim,
            Locations.special_zone_6_coin_block_8:
                CanSwim,
            Locations.special_zone_6_coin_block_9:
                CanSwim,
            Locations.special_zone_6_coin_block_10:
                CanSwim,
            Locations.special_zone_6_coin_block_11:
                CanSwim,
            Locations.special_zone_6_coin_block_12:
                CanSwim,
            Locations.special_zone_6_coin_block_13:
                CanSwim,
            Locations.special_zone_6_coin_block_14:
                CanSwim,
            Locations.special_zone_6_coin_block_15:
                CanSwim,
            Locations.special_zone_6_coin_block_16:
                CanSwim,
            Locations.special_zone_6_coin_block_17:
                CanSwim,
            Locations.special_zone_6_coin_block_18:
                CanSwim,
            Locations.special_zone_6_coin_block_19:
                CanSwim,
            Locations.special_zone_6_coin_block_20:
                CanSwim,
            Locations.special_zone_6_coin_block_21:
                CanSwim,
            Locations.special_zone_6_coin_block_22:
                CanSwim,
            Locations.special_zone_6_coin_block_23:
                CanSwim,
            Locations.special_zone_6_coin_block_24:
                CanSwim,
            Locations.special_zone_6_coin_block_25:
                CanSwim,
            Locations.special_zone_6_coin_block_26:
                CanSwim,
            Locations.special_zone_6_coin_block_27:
                CanSwim,
            Locations.special_zone_6_coin_block_28:
                CanSwim,
            Locations.special_zone_6_powerup_block_2:
                CanSwim,
            Locations.special_zone_6_coin_block_29:
                CanSwim,
            Locations.special_zone_6_coin_block_30:
                CanSwim,
            Locations.special_zone_6_coin_block_31:
                CanSwim,
            Locations.special_zone_6_coin_block_32:
                CanSwim,
            Locations.special_zone_6_coin_block_33:
                CanSwim,
            Locations.special_zone_6_room_2:
                CanSwim,
            Locations.special_zone_6_room_3:
                CanSwim,

            Locations.special_zone_7_dragon:
                CanCarryOrYoshiTongue,
            Locations.special_zone_7_powerup_block_1:
                True_(),
            Locations.special_zone_7_yoshi_block_1:
                CanCarryOrYoshiTongue,
            Locations.special_zone_7_coin_block_1:
                CanCarryOrYoshiTongue,
            Locations.special_zone_7_powerup_block_2:
                CanCarryOrYoshiTongue,
            Locations.special_zone_7_coin_block_2:
                CanCarryOrYoshiTongue,

            Locations.special_zone_8_dragon:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_yoshi_block_1:
                CanCarry | HasYoshi,
            Locations.special_zone_8_coin_block_1:
                True_(),
            Locations.special_zone_8_coin_block_2:
                True_(),
            Locations.special_zone_8_coin_block_3:
                True_(),
            Locations.special_zone_8_coin_block_4:
                True_(),
            Locations.special_zone_8_coin_block_5:
                True_(),
            Locations.special_zone_8_blue_pow_block_1:
                True_(),
            Locations.special_zone_8_powerup_block_1:
                True_(),
            Locations.special_zone_8_star_block_1:
                True_(),
            Locations.special_zone_8_coin_block_6:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_7:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_8:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_9:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_10:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_11:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_12:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_13:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_14:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_15:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_16:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_17:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_18:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_multi_coin_block_1:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_19:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_20:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_21:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_22:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_coin_block_23:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_powerup_block_2:
                CanBreakTurnBlocks | HasFeather | HasYoshi | CanCarry,
            Locations.special_zone_8_flying_block_1:
                CanCarry | HasYoshi,
        }

        super().__init__(world)


    def alternate_logic(self, world: "WaffleWorld", options: list[str] = [], is_glitched: bool = False) -> None:
        if "Mondo - Swimless" in options:
            connection_rules = {
                f"{Regions.special_zone_6_region} -> {Locations.special_zone_6_exit_1}": 
                    True_(),
            }
            location_rules = {
                Locations.special_zone_6_dragon:
                    True_(),
                Locations.special_zone_6_powerup_block_1:
                    True_(),
                Locations.special_zone_6_coin_block_1:
                    True_(),
                Locations.special_zone_6_coin_block_2:
                    True_(),
                Locations.special_zone_6_yoshi_block_1:
                    True_(),
                Locations.special_zone_6_multi_coin_block_1:
                    True_(),
                Locations.special_zone_6_coin_block_3:
                    True_(),
                Locations.special_zone_6_coin_block_4:
                    True_(),
                Locations.special_zone_6_coin_block_5:
                    True_(),
                Locations.special_zone_6_coin_block_6:
                    True_(),
                Locations.special_zone_6_coin_block_7:
                    True_(),
                Locations.special_zone_6_coin_block_8:
                    True_(),
                Locations.special_zone_6_coin_block_9:
                    True_(),
                Locations.special_zone_6_coin_block_10:
                    True_(),
                Locations.special_zone_6_coin_block_11:
                    True_(),
                Locations.special_zone_6_coin_block_12:
                    True_(),
                Locations.special_zone_6_coin_block_13:
                    True_(),
                Locations.special_zone_6_coin_block_14:
                    True_(),
                Locations.special_zone_6_coin_block_15:
                    True_(),
                Locations.special_zone_6_coin_block_16:
                    True_(),
                Locations.special_zone_6_coin_block_17:
                    True_(),
                Locations.special_zone_6_coin_block_18:
                    True_(),
                Locations.special_zone_6_coin_block_19:
                    True_(),
                Locations.special_zone_6_coin_block_20:
                    True_(),
                Locations.special_zone_6_coin_block_21:
                    True_(),
                Locations.special_zone_6_coin_block_22:
                    True_(),
                Locations.special_zone_6_coin_block_23:
                    True_(),
                Locations.special_zone_6_coin_block_24:
                    True_(),
                Locations.special_zone_6_coin_block_25:
                    True_(),
                Locations.special_zone_6_coin_block_26:
                    True_(),
                Locations.special_zone_6_coin_block_27:
                    True_(),
                Locations.special_zone_6_coin_block_28:
                    True_(),
                Locations.special_zone_6_powerup_block_2:
                    True_(),
                Locations.special_zone_6_coin_block_29:
                    True_(),
                Locations.special_zone_6_coin_block_30:
                    True_(),
                Locations.special_zone_6_coin_block_31:
                    True_(),
                Locations.special_zone_6_coin_block_32:
                    True_(),
                Locations.special_zone_6_coin_block_33:
                    True_(),
                Locations.special_zone_6_room_2:
                    True_(),
                Locations.special_zone_6_room_3:
                    True_(),
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)

        if "Vanilla Dome 1 - Itemless Sinking Platform" in options:
            connection_rules = {
                f"{Regions.vanilla_dome_1_region} -> {Locations.vanilla_dome_1_exit_1}": 
                    True_(),
            }
            location_rules = {
                Locations.vanilla_dome_1_dragon:
                    CanCarry,
                Locations.vanilla_dome_1_midway:
                    True_(),
                Locations.vanilla_dome_1_powerup_block_4:
                    True_(),
                Locations.vanilla_dome_1_coin_block_2:
                    True_(),
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)

        if "Vanilla Secret 1 - Wall Running" in options:
            connection_rules = {
                f"{Regions.vanilla_secret_1_region} -> {Locations.vanilla_secret_1_exit_1}": 
                    CanClimb | CanWallRun,
                f"{Regions.vanilla_secret_1_region} -> {Locations.vanilla_secret_1_exit_2}": 
                    (CanClimb | CanWallRun) & CanCarry & HasBSP,
            }
            location_rules = {
                Locations.vanilla_secret_1_dragon:
                    (CanClimb | CanWallRun) & CanCarry,
                Locations.vanilla_secret_1_vine_block_2:
                    CanClimb | CanWallRun,
                Locations.vanilla_secret_1_coin_block_2:
                    CanClimb | CanWallRun,
                Locations.vanilla_secret_1_coin_block_3:
                    CanClimb | CanWallRun,
                Locations.vanilla_secret_1_powerup_block_2:
                    CanClimb | CanWallRun,
                Locations.vanilla_secret_1_room_2:
                    CanClimb | CanWallRun,
                Locations.vanilla_secret_1_room_3:
                    (CanClimb | CanWallRun) & CanCarry & HasBSP,
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)

        if "Vanilla Secret 3 - Swimless" in options:
            connection_rules = {
                f"{Regions.vanilla_secret_3_region} -> {Locations.vanilla_secret_3_exit_1}": 
                    True_(),
            }
            location_rules = {
                Locations.vanilla_secret_3_dragon:
                    True_(),
                Locations.vanilla_secret_3_powerup_block_1:
                    True_(),
                Locations.vanilla_secret_3_powerup_block_2:
                    True_(),
                Locations.vanilla_secret_3_room_2:
                    True_(),
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)


        if "Cheese Bridge Area - Secret Exit with Yoshi" in options:
            connection_rules = {
                f"{Regions.cheese_bridge_region} -> {Locations.cheese_bridge_exit_2}": 
                    CanCapeFly | HasYoshi,
            }
            location_rules = {
                Locations.cheese_bridge_moon:
                    CanCapeFly | HasYoshi,
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)


        if "Vanilla Dome 4 - Sacrifice for Coin Block #8" in options:
            location_rules = {
                Locations.vanilla_dome_4_coin_block_8:
                    CanCarry | HasFeather | HasYoshi,
            }
            self.update_rules(is_glitched, location_rules=location_rules)


        if "Ludwig's Castle - Runless" in options:
            connection_rules = {
                f"{Regions.twin_bridges_castle_region} -> {Locations.twin_bridges_castle}": 
                    CanClimb,
            }
            location_rules = {
                Locations.twin_bridges_castle_powerup_block_1:
                    CanClimb,
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)


        if "Ludwig's Castle - Climbless" in options:
            connection_rules = {
                f"{Regions.twin_bridges_castle_region} -> {Locations.twin_bridges_castle}": 
                    CanWallRun,
            }
            location_rules = {
                Locations.twin_bridges_castle_powerup_block_1:
                    CanWallRun,
            }
            self.update_rules(is_glitched, location_rules=location_rules)


        if "Forest of Illusion 1 - Secret Exit with Yoshi" in options:
            connection_rules = {
                f"{Regions.forest_of_illusion_1_region} -> {Locations.forest_of_illusion_1_exit_2}": 
                    CanCarry & (HasYoshi | HasPBalloon),
            }
            carryless_exit_rules = {
                f"{Regions.forest_of_illusion_1_region} -> {Locations.forest_of_illusion_1_exit_2}": 
                    HasYoshi | HasPBalloon,
            }
            location_rules = {
                Locations.forest_of_illusion_1_key_block_1:
                    HasYoshi | HasPBalloon,
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, 
                              carryless_exit_rules=carryless_exit_rules,
                              location_rules=location_rules)


        if "Forest of Illusion 3 - Can pass big pipe itemless" in options:
            connection_rules = {
                f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_1}": 
                    True_(),
                f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_2}": 
                    CanCarryOrYoshiTongue & CanBreakTurnBlocks,
            }
            carryless_exit_rules = {
                f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_2}": 
                    CanCarryOrYoshiTongue & CanBreakTurnBlocks,
            }
            location_rules = {
                Locations.forest_of_illusion_3_dragon:
                    True_(),
                Locations.forest_of_illusion_3_hidden_1up:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_2:
                    True_(),
                Locations.forest_of_illusion_3_multi_coin_block_2:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_3:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_4:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_5:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_6:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_7:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_8:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_9:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_10:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_11:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_12:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_13:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_14:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_15:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_16:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_17:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_18:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_19:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_20:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_21:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_22:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_23:
                    True_(),
                Locations.forest_of_illusion_3_coin_block_24:
                    True_(),
                Locations.forest_of_illusion_3_midway:
                    True_(),
                Locations.forest_of_illusion_3_room_3:
                    True_(),
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, 
                              carryless_exit_rules=carryless_exit_rules,
                              location_rules=location_rules)


        if "Forest of Illusion 3 - Secret Exit with Yoshi" in options:
            self.add_connection_rule(is_glitched,
                                     f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_2}", 
                                     CanYoshiCarry, "or")
            self.add_carryless_rule(is_glitched,
                                    f"{Regions.forest_of_illusion_3_region} -> {Locations.forest_of_illusion_3_exit_2}", 
                                    CanYoshiCarry, "or")


        if "Forest Ghost House - Skip second room" in options:
            connection_rules = {
                f"{Regions.forest_ghost_house_region} -> {Locations.forest_ghost_house_exit_1}": 
                    HasPSwitch | CanWallRun | CanCapeFly,
                f"{Regions.forest_ghost_house_region} -> {Locations.forest_ghost_house_exit_2}": 
                    HasPSwitch | CanWallRun | CanCapeFly,
            }
            location_rules = {
                Locations.forest_ghost_house_dragon:
                    HasPSwitch | CanWallRun | CanCapeFly,
                Locations.forest_ghost_house_moon:
                    HasPSwitch | CanWallRun | CanCapeFly,
                Locations.forest_ghost_house_room_3:
                    HasPSwitch | CanWallRun | CanCapeFly,
                Locations.forest_ghost_house_room_4:
                    HasPSwitch | CanWallRun | CanCapeFly,
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)


        if "Valley of Bowser 4 - Yoshi Climb" in options:
            connection_rules = {
                f"{Regions.valley_of_bowser_4_region} -> {Locations.valley_of_bowser_4_exit_1}": 
                    CanClimb | HasYoshi,
                f"{Regions.valley_of_bowser_4_region} -> {Locations.valley_of_bowser_4_exit_2}": 
                    CanYoshiCarry & (CanClimb | HasYoshi),
            }
            carryless_exit_rules = {
                f"{Regions.valley_of_bowser_4_region} -> {Locations.valley_of_bowser_4_exit_2}": 
                    CanClimb | HasYoshi,
            }
            location_rules = {
                Locations.valley_of_bowser_4_yoshi_block_1:
                    CanClimb | HasYoshi,
                Locations.valley_of_bowser_4_life_block_1:
                    (CanClimb | HasYoshi) & CanBreakTurnBlocks,
                Locations.valley_of_bowser_4_powerup_block_2:
                    (CanClimb | HasYoshi) & HasYSP,
                Locations.valley_of_bowser_4_midway:
                    CanClimb | HasYoshi,
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, 
                              carryless_exit_rules=carryless_exit_rules,
                              location_rules=location_rules)


        if "Awesome - Itemless" in options:
            connection_rules = {
                f"{Regions.special_zone_4_region} -> {Locations.special_zone_4_exit_1}": 
                    True_(),
            }
            location_rules = {
                Locations.special_zone_4_dragon:
                    True_(),
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)


        if "Forest Secret Area - Itemless 1-Up block" in options:
            location_rules = {
                Locations.forest_secret_life_block_1:
                    True_(),
            }
            self.update_rules(is_glitched, location_rules=location_rules)


        if "Valley of Bowser 3 - Itemless Powerup block" in options:
            location_rules = {
                Locations.valley_of_bowser_3_powerup_block_2:
                    True_(),
            }
            self.update_rules(is_glitched, location_rules=location_rules)


        if "Outrageous - Wall Run pipe" in options:
            connection_rules = {
                f"{Regions.special_zone_7_region} -> {Locations.special_zone_7_exit_1}": 
                    CanCarryOrYoshiTongue | (CanWallRun & HasSuperStar),
            }
            location_rules = {
                Locations.special_zone_7_dragon:
                    CanCarryOrYoshiTongue | (CanWallRun & HasSuperStar),
                Locations.special_zone_7_yoshi_block_1:
                    CanCarryOrYoshiTongue | (CanWallRun & HasSuperStar),
                Locations.special_zone_7_coin_block_1:
                    CanCarryOrYoshiTongue | (CanWallRun & HasSuperStar),
                Locations.special_zone_7_powerup_block_2:
                    CanCarryOrYoshiTongue | (CanWallRun & HasSuperStar),
                Locations.special_zone_7_coin_block_2:
                    CanCarryOrYoshiTongue | (CanWallRun & HasSuperStar),
            }
            self.update_rules(is_glitched, connection_rules=connection_rules, location_rules=location_rules)


        if "Lemmy's Castle - Itemless 1-Up blocks" in options:
            location_rules = {
                Locations.vanilla_dome_castle_life_block_1:
                    True_(),
                Locations.vanilla_dome_castle_life_block_2:
                    True_(),
            }
            self.update_rules(is_glitched, location_rules=location_rules)


        if "Star World 3 - Top area with a Star" in options:
            self.add_carryless_rule(is_glitched, 
                                    f"{Regions.star_road_3_region} -> {Locations.star_road_3_exit_2}",
                                    Has(Items.super_star_active, 1), 
                                    union="or")
            self.add_location_rule(is_glitched, 
                                    Locations.star_road_3_key_block_1,
                                    Has(Items.super_star_active, 1), 
                                    union="or")

        if "Star World 4 - Carryless exit with wingless Yoshi" in options:
            carryless_exit_rules = {
                f"{Regions.star_road_4_region} -> {Locations.star_road_4_exit_2}": 
                    HasYoshi | HasFeather | (HasGSP & HasRSP),
            }
            self.update_rules(is_glitched,carryless_exit_rules=carryless_exit_rules)

        if "Valley Ghost House - True Carryless Secret Exit" in options:
            carryless_exit_rules = {
                f"{Regions.valley_ghost_house_region} -> {Locations.valley_ghost_house_exit_2}": 
                    HasPSwitch & CanRun,
            }
            self.update_rules(is_glitched, carryless_exit_rules=carryless_exit_rules)


        super().alternate_logic()


    def update_rules(self, 
                     is_glitched: bool,
                     connection_rules: dict[str, Rule] = None, 
                     carryless_exit_rules: dict[str, Rule] = None, 
                     location_rules: dict[str, Rule] = None) -> None:
        if is_glitched:
            if carryless_exit_rules is not None:
                for connection, rule in carryless_exit_rules.items():
                    self.add_carryless_rule(is_glitched, connection, rule, union="or")
            if connection_rules is not None:
                for connection, rule in connection_rules.items():
                    self.add_connection_rule(is_glitched, connection, rule, union="or")
            if location_rules is not None:
                for location, rule in location_rules.items():
                    self.add_location_rule(is_glitched, location, rule, union="or")
        else:
            if carryless_exit_rules is not None:
                self.carryless_exit_rules.update(carryless_exit_rules)
            if connection_rules is not None:
                self.connection_rules.update(connection_rules)
            if location_rules is not None:
                self.location_rules.update(location_rules)

    def add_connection_rule(self, is_glitched, connection, rule, union = "and"):
        if is_glitched:
            union = "or"
            rule = rule & Has(Items.glitched)
        original_rule = self.connection_rules[connection]
        if union == "and":
            modified_rule = original_rule & rule
        else:
            modified_rule = original_rule | rule
        self.connection_rules[connection] = modified_rule

    def add_location_rule(self, is_glitched, location, rule, union = "and"):
        if is_glitched:
            union = "or"
            rule = rule & Has(Items.glitched)
        original_rule = self.location_rules[location]
        if union == "and":
            modified_rule = original_rule & rule
        else:
            modified_rule = original_rule | rule
        self.location_rules[location] = modified_rule

    def add_carryless_rule(self, is_glitched, connection, rule, union = "and"):
        if is_glitched:
            union = "or"
            rule = rule & Has(Items.glitched)
        original_rule = self.carryless_exit_rules[connection]
        if union == "and":
            modified_rule = original_rule & rule
        else:
            modified_rule = original_rule | rule
        self.carryless_exit_rules[connection] = modified_rule


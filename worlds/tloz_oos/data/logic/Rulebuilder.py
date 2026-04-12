import dataclasses
from typing import Any, override

from BaseClasses import CollectionState
from Options import Option, Accessibility
from rule_builder.options import OptionFilter, Operator
from rule_builder.rules import Rule, HasFromList, HasGroup, HasAll, False_, True_, Has
from ..Constants import SEASON_CHAOTIC, SEASON_ITEMS, MARKET_LOCATIONS
from ...World import OracleOfSeasonsWorld
from ...Options import OracleOfSeasonsGoldenOreSpotsShuffle


@dataclasses.dataclass
class Season(Rule[OracleOfSeasonsWorld], game=OracleOfSeasonsWorld.game):
    area_name: str
    season: int
    excluded: bool = False

    @override
    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        if (world.default_seasons[self.area_name] == self.season) == self.excluded:
            return True_().resolve(world)
        else:
            return False_().resolve(world)


class HasGroupOption(HasGroup, game=OracleOfSeasonsWorld.game):
    option_name: str

    def __init__(self, item_name: str, option_name: str):
        self.option_name = option_name
        super().__init__(item_name)

    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        self.count = getattr(world.options, self.option_name).value
        return super()._instantiate(world)


class HasFromListOption(HasFromList, game=OracleOfSeasonsWorld.game):
    option_name: str

    def __init__(self, *item_names: str, option_name: str):
        self.option_name = option_name
        super().__init__(*item_names)

    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        self.count = getattr(world.options, self.option_name).value
        return super()._instantiate(world)


@dataclasses.dataclass
class LostWoods(HasAll, game=OracleOfSeasonsWorld.game):
    is_main_sequence: bool
    allow_default: bool

    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        if self.is_main_sequence:
            sequence = world.lost_woods_main_sequence
        else:
            sequence = world.lost_woods_item_sequence

        if self.allow_default:
            current_season = world.default_seasons["LOST_WOODS"]
        else:
            current_season = SEASON_CHAOTIC

        needed_seasons = set()
        for item in sequence:
            season = item[1]
            if season != current_season:
                current_season = SEASON_CHAOTIC
                needed_seasons.add(SEASON_ITEMS[season])

        self.item_names = tuple(needed_seasons)
        return super()._instantiate(world)


@dataclasses.dataclass
class CanReachNumRegions(Rule[OracleOfSeasonsWorld], game=OracleOfSeasonsWorld.game):
    """A rule that checks if the given region is reachable by the current player"""

    region_names: list[str]
    """The name of the regions to test access to"""

    region_need: int
    """The number of regions that need to be reached"""

    @override
    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        if self.region_need == 0:
            return True_().resolve(world)
        return self.Resolved(
            tuple(self.region_names),
            self.region_need,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    @override
    def __str__(self) -> str:
        options = f", options={self.options}" if self.options else ""
        return f"{self.__class__.__name__}({self.region_names}{options})"

    class Resolved(Rule.Resolved):
        region_names: tuple[str]
        region_need: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            reachables = 0
            for region_name in self.region_names:
                if state.can_reach_region(region_name, self.player):
                    reachables += 1
                    if reachables >= self.region_need:
                        return True
            return False

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {
                region_name: {id(self)} for region_name in self.region_names
            }

        @override
        def __str__(self) -> str:
            items = ", ".join(self.region_names)
            return f"Can reach {self.region_need} regions ({items})"


@dataclasses.dataclass
class HasRupeesForShop(Rule[OracleOfSeasonsWorld], game=OracleOfSeasonsWorld.game):
    shop_name: str

    @override
    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        amount = world.shop_rupee_requirements.get(self.shop_name, 0)
        if amount == 0:
            return True_().resolve(world)
        from .LogicPredicates import oos_can_farm_rupees
        return (oos_can_farm_rupees() & Has("Rupees", amount // 2)).resolve(world)


class HasOresForShop(Rule[OracleOfSeasonsWorld], game=OracleOfSeasonsWorld.game):
    @override
    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        amount = sum([world.shop_prices[loc] for loc in MARKET_LOCATIONS])
        if amount == 0:
            return True_().resolve(world)
        from .LogicPredicates import oos_can_farm_ore_chunks
        if world.options.shuffle_golden_ore_spots == OracleOfSeasonsGoldenOreSpotsShuffle.option_false:
            return oos_can_farm_ore_chunks().resolve(world)
        return (oos_can_farm_ore_chunks() & Has("Ore Chunks", amount // 2)).resolve(world)


@dataclasses.dataclass
class ItemInLocation(Rule[OracleOfSeasonsWorld], game=OracleOfSeasonsWorld.game):
    location_name: str
    item_name: str

    @override
    def _instantiate(self, world: OracleOfSeasonsWorld) -> Rule.Resolved:
        if world.options.accessibility == Accessibility.option_full:
            return False_().resolve(world)
        return self.Resolved(
            self.location_name,
            self.item_name,
            player=world.player,
        )

    class Resolved(Rule.Resolved):
        location_name: str
        item_name: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            item = state.multiworld.get_location(self.location_name, self.player).item
            return item is not None and item.name == self.item_name and item.player == self.player

        @override
        def __str__(self) -> str:
            return f"{self.item_name} in {self.location_name}"


def from_bool(condition: bool) -> Rule:
    return True_() if condition else False_()


def from_option(option: type[Option], value: Any, operator: Operator = "eq") -> Rule:
    return True_(options=[OptionFilter(option, value, operator)])

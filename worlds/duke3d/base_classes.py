from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Set, Union

from BaseClasses import Entrance, Item, Location, Region

from .rules import RULETYPE, LambdaRule, Rule, Rules, RuleTrue

if TYPE_CHECKING:
    from ..duke3d import D3DWorld


class D3DItem(Item):
    game = "Duke3D"


class D3DLocation(Location):
    game = "Duke3D"

    def __init__(
        self,
        player: int,
        name: str = "",
        address: Optional[int] = None,
        parent: Optional[Region] = None,
    ):
        super().__init__(player, name, address, parent)
        if address is None:
            self.event = True


@dataclass(frozen=True)
class LocationDef:
    name: str
    type: str  # "exit", "sprite", "sector
    game_id: int  # Sprite number, sector number or exit lotag
    sprite_type: str = ""  # additional data for sprites
    density: int = 0  # defines what density settings it appears in. Higher values require more locations enabled
    x: int = 0
    y: int = 0
    z: int = 0


# Density levels:
# 0: Iconic locations - Always included
# 1: Balanced with secrets - Default density with location checks at secret areas. Handpicked for interesting places to
#    visit.
# 2: Balanced without secrets - Default density with no checks at secret areas. Includes additional pickups in (most)
#    secret areas to account for missing checks from the area itself
# 3: Dense - More checks, including some nearby duplicates
# 4: All - All single player locations, can sometimes have big clusters in single spot
# 5: MP Only - Additional items that normally only spawn in MP only deathmatch locations


@dataclass(frozen=True)
class ItemDef:
    name: str
    ap_id: int  # The id for the item
    type: str  # The type of item
    props: Dict[str, Any]  # Additional type specific properties
    unique: bool = False  # Can only have one of these
    persistent: bool = False  # These are persisted in the game save
    progression: bool = False  # Marks an item as being a progression item. Persistent non-progression are marked useful
    silent: bool = False  # These are acquired but not notified to the player


class D3DLevel(object):
    name: str
    levelnum: int
    volumenum: int
    location_defs: List[dict]
    keys: List[str]
    events: List[str] = []
    must_dive: bool = False  # If the level has locations locked behind diving. Determines progression status for Scuba
    has_boss: bool = (
        False  # If the level awards a boss token in the appropriate goal settings
    )

    def __init__(self):
        self.world: Optional["D3DWorld"] = None
        self.prefix = f"E{self.volumenum + 1}L{self.levelnum + 1}"
        self.locations: Dict[str, LocationDef] = self._make_locations()
        self.used_locations: Set[
            str
        ] = set()  # locations actually filled in make_region

    def _make_locations(self) -> Dict[str, LocationDef]:
        ret = {}
        for loc_def in self.location_defs:
            loc_name = f'{self.prefix} {loc_def["name"]}'
            ret[loc_name] = LocationDef(
                name=loc_name,
                type=loc_def["type"],
                game_id=loc_def["id"],
                density=loc_def.get("density", 0),
                sprite_type=loc_def.get("sprite_type"),
            )
        return ret

    def create_region(self, world: "D3DWorld") -> Region:
        self.world = world
        self.used_locations = set()
        ret = self.main_region()
        self.world = None
        return ret

    def main_region(self) -> Region:
        """
        To be implemented by each level
        """
        # Default implementations: everything available in the start region
        # This is wildly incorrect logically, but helps play the levels for configuring the logic
        ret = self.region(self.name)
        self.add_locations([x["name"] for x in self.location_defs], ret)
        return ret

    def region(
        self,
        name: str,
        locations: Optional[List[str]] = None,
        hint: Optional[str] = None,
    ) -> Region:
        ret = Region(
            f"{self.prefix} {name}", self.world.player, self.world.multiworld, hint
        )
        if locations:
            self.add_locations(locations, ret)
        return ret

    def add_location(self, name: str, region: Region):
        location = f"{self.prefix} {name}"
        if name in self.events:
            region.locations.append(
                D3DLocation(
                    self.world.player,
                    location,
                    None,
                    region,
                )
            )
        elif self.world.use_location(self.locations.get(location)):
            region.locations.append(
                D3DLocation(
                    self.world.player,
                    location,
                    self.world.location_name_to_id[location],
                    region,
                )
            )
            self.used_locations.add(location)

    def add_locations(self, locations: List[str], region: Region):
        for loc in locations:
            self.add_location(loc, region)

    def get_location(self, name) -> Optional[Location]:
        try:
            return self.world.multiworld.get_location(
                f"{self.prefix} {name}", self.world.player
            )
        except KeyError:
            return None

    @staticmethod
    def _resolve_rule_type(
        rules: Optional[Union[RULETYPE, List[RULETYPE]]] = None
    ) -> Optional[Rule]:
        if rules is None:
            return RuleTrue()
        if not isinstance(rules, List):
            rules = [rules]
        if not rules:
            return None
        rule = rules[0]
        if not isinstance(rule, Rule):
            rule = LambdaRule(rule)
        for other_rule in rules[1:]:
            if not isinstance(other_rule, Rule):
                other_rule = LambdaRule(other_rule)
            rule |= other_rule
        return rule

    def connect(
        self,
        start: Region,
        end: Region,
        rules: Optional[Union[RULETYPE, List[RULETYPE]]] = None,
    ):
        start.connect(end, None, self._resolve_rule_type(rules))

    def restrict(
        self,
        spot: Optional[Union[Location, Entrance, str]],
        rules: Union[RULETYPE, List[RULETYPE]],
    ):
        if isinstance(spot, str):
            return self.restrict(self.get_location(spot), rules)
        if spot is not None:
            spot.access_rule = self._resolve_rule_type(rules)

    @property
    def red_key(self) -> Rule:
        return self.world.rules.can_use & self.world.rules.has(
            f"{self.prefix} Red Key Card"
        )

    @property
    def blue_key(self) -> Rule:
        return self.world.rules.can_use & self.world.rules.has(
            f"{self.prefix} Blue Key Card"
        )

    @property
    def yellow_key(self) -> Rule:
        return self.world.rules.can_use & self.world.rules.has(
            f"{self.prefix} Yellow Key Card"
        )

    @property
    def unlock(self) -> str:
        return f"{self.prefix} Unlock"

    @property
    def rules(self) -> Rules:
        return self.world.rules

    @property
    def items(self) -> List[str]:
        ret = []
        for color in ("Red", "Blue", "Yellow"):
            if color in self.keys:
                ret.append(f"{self.prefix} {color} Key Card")
        return ret

    @property
    def map(self) -> str:
        return f"{self.prefix} Automap"

    def event(self, name: str) -> Rule:
        return self.world.rules.has(f"{self.prefix} {name}")


class D3DEpisode(object):
    name: str
    volumenum: int
    levels: List[D3DLevel]
    maxlevel: int
    bosslevel: int

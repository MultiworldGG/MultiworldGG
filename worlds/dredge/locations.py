from __future__ import annotations

import json
import pkgutil

from typing import Dict, Set, TYPE_CHECKING, Literal, Sequence, Union

from BaseClasses import Location, Region
from BaseClasses import LocationProgressType as LPT

from dataclasses import dataclass, field

from .options import DREDGEOptions

if TYPE_CHECKING:
    from .world import DREDGEWorld

class DREDGELocation(Location):
    game: str = "DREDGE"

CatchType = Literal["Coastal", "Shallow", "Oceanic", "Abyssal", "Hadal", "Mangrove", "Volcanic", "Ice", "Crab"]
IronRigPhase = Literal[0,1,2,3,4,5]

@dataclass(frozen=True)
class ItemsReq:
    type: Literal["items"] = "items"
    any_of: Sequence[str] = field(default_factory=list)
    all_of: Sequence[str] = field(default_factory=list)

@dataclass(frozen=True)
class ResearchReq:
    type: Literal["research"] = "research"
    cost: int = 0

@dataclass(frozen=True)
class CatchTypeReq:
    type: Literal["catch_type"] = "catch_type"
    value: CatchType = "Coastal"

@dataclass(frozen=True)
class IronRigPhaseReq:
    type: Literal["iron_rig_phase"] = "iron_rig_phase"
    value:IronRigPhase = 0

Requirement = Union[ItemsReq, ResearchReq, CatchTypeReq, IronRigPhaseReq]

@dataclass
class DREDGELocationData:
    base_id_offset: int
    region: str
    location_group: str
    expansion: str
    requirements: list[Requirement] = field(default_factory=list)
    can_catch_rod: bool = True
    can_catch_net: bool = False
    progress_type: LPT = LPT.DEFAULT
    is_aberration: bool = False


location_base_id = 3459028911689314

def load_data_file(*args) -> dict:
    fname = "/".join(["data", *args])
    return json.loads(pkgutil.get_data(__name__, fname).decode())

def parse_requirement(obj: dict) -> Requirement:
    t = obj["type"]  # required
    if t == "items":
        return ItemsReq(
            any_of=obj.get("any_of", []),
            all_of=obj.get("all_of", []),
        )
    if t == "research":
        cost = obj.get("cost", 0)
        if not isinstance(cost, int) or cost < 0:
            raise ValueError(f"Invalid research cost: {cost!r}")
        return ResearchReq(cost=cost)
    if t == "catch_type":
        return CatchTypeReq(value=obj["value"])
    if t == "iron_rig_phase":
        value = obj["value"]
        if value not in (0, 1, 2, 3, 4, 5):
            raise ValueError(f"Invalid iron_rig_phase value: {value!r}")
        return IronRigPhaseReq(value=value)
    raise ValueError(f"Unknown requirement type: {t!r} ({obj})")


def parse_requirements(raw) -> list[Requirement]:
    # If you want to allow omission of the key:
    if raw is None:
        return []

    if not isinstance(raw, list):
        raise TypeError(
            f"`requirement` must be a list of objects, got {type(raw).__name__}: {raw!r}"
        )

    return [parse_requirement(r) for r in raw]

location_table = {
    name: DREDGELocationData(
        base_id_offset=entry["base_id_offset"],
        region=entry["region"],
        location_group=entry["location_group"],
        expansion=entry["expansion"],
        requirements=parse_requirements(entry.get("requirements")),
        can_catch_rod=entry.get("can_catch_rod", True),
        can_catch_net=entry.get("can_catch_net", False),
        progress_type=entry.get("progress_type", LPT.DEFAULT),
        is_aberration=entry.get("is_aberration", False)
    )
    for name, entry in load_data_file("locations.json").items()
}

LOCATION_NAME_TO_ID: Dict[str, int] = {name: location_base_id + data.base_id_offset for name, data in location_table.items()}




def get_player_location_table(options: DREDGEOptions) -> list[str]:
    all_locations: list[str] = []
    base_locations = {name for (name, location)
                      in location_table.items() if location.expansion == "Base"}
    iron_rig_locations = {name for (name, location)
                      in location_table.items() if location.expansion == "IronRig"}
    pale_reach_locations = {name for (name, location)
                      in location_table.items() if location.expansion == "PaleReach"}
    both_dlc_locations = {name for (name, location)
                      in location_table.items() if location.expansion == "Both"}

    all_locations.extend(base_locations)

    if options.include_iron_rig_dlc:
        all_locations.extend(iron_rig_locations)
    if options.include_pale_reach_dlc:
        all_locations.extend(pale_reach_locations)
    if options.include_pale_reach_dlc and options.include_iron_rig_dlc:
        all_locations.extend(both_dlc_locations)

    all_locations = list(filter(exclude_groups, all_locations))

    return all_locations

def exclude_groups(location_name):
    # removing these checks while waiting for fix from mod
    excluded_groups = {"Shop", "Pursuit", "World", "Relic"}
    dredge_location = location_table[location_name]
    return not (dredge_location.location_group in excluded_groups)

LOCATION_NAME_GROUPS: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    if loc_data.location_group:
        LOCATION_NAME_GROUPS.setdefault(loc_data.location_group, set()).add(loc_name)

def create_all_locations(world: DREDGEWorld) -> None:
    create_locations(world)

def create_locations(world: DREDGEWorld) -> None:
    for location_name in get_player_location_table(world.options):
        region = world.get_region(location_table[location_name].region)
        location_id = LOCATION_NAME_TO_ID[location_name]
        dredge_location = location_table[location_name]
        location = DREDGELocation(world.player, location_name, location_id, region)
        if dredge_location.is_aberration and not world.options.include_aberrations:
            location.progress_type = LPT.EXCLUDED
        region.locations.append(location)
        if location_table[location_name].location_group == "Research Unlock":
            add_research_unlock_item(world, location)

def add_research_unlock_item(world: DREDGEWorld, location: DREDGELocation) -> None:
    research_unlock_item = world.create_item(location.name)
    location.place_locked_item(research_unlock_item)
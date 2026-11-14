# This file was generated using jinja2 from a template. If this file needs
# to be changed, either change the template, or the code leveraging the template.
from collections.abc import Callable
from typing import TYPE_CHECKING, NotRequired, TypedDict

from typing_extensions import Unpack

import worlds.gstla.gen.internal_location_data as LocationLists  # noqa: N812
from BaseClasses import MultiWorld
from .internal_location_data import InternalLocationData, LocationRestriction, LocationType
from .location_names import loc_names_by_id

if TYPE_CHECKING:
    base = InternalLocationData
else:
    base = object


class LocationDataDict(TypedDict):
    rando_flag: NotRequired[int]
    flag: NotRequired[int]
    id: NotRequired[int | None]
    ap_id: NotRequired[int]
    addresses: NotRequired[list[int]]
    event_type: NotRequired[int]
    vanilla_contents: NotRequired[int]
    is_key: NotRequired[bool]
    is_major: NotRequired[bool]
    loc_type: NotRequired[LocationType]
    restrictions: NotRequired[LocationRestriction]
    event: NotRequired[bool]
    included: NotRequired[Callable[[MultiWorld, int], bool]]


class LocationData(base):
    def __init__(self, location: InternalLocationData, **kwargs: Unpack[LocationDataDict]):
        self._loc = location
        self._kwargs = kwargs

    def __getattr__(self, name):
        if name in self._kwargs:
            return self._kwargs[name]  # type: ignore
        return getattr(self._loc, name)


_overrides: dict[int, LocationDataDict] = {}


def _wrap_loc(loc: InternalLocationData) -> LocationData:
    if loc.ap_id in _overrides:
        return LocationData(loc, **_overrides[loc.ap_id])
    return LocationData(loc)


def _convert_locs(data: list[InternalLocationData]) -> list[LocationData]:
    return [_wrap_loc(x) for x in data]


djinn_locations = _convert_locs(LocationLists.djinn_locations)

summon_tablets = _convert_locs(LocationLists.summon_tablets)

psyenergy_locations = _convert_locs(LocationLists.psyenergy_locations)

events = _convert_locs(LocationLists.events)

the_rest = _convert_locs(LocationLists.the_rest)


def create_loctype_to_datamapping() -> dict[str, list[LocationData]]:
    """Creates a dictionary mapping LocationType to a list of all locations
    of that type
    """
    types: dict[str, list[LocationData]] = {}
    for idx, data in enumerate(all_locations):
        if data.loc_type not in types:
            types[data.loc_type] = []
        types[data.loc_type].append(data)
    return types


all_locations: list[LocationData] = djinn_locations + psyenergy_locations + summon_tablets + events + the_rest
location_name_to_data: dict[str, LocationData] = {
    loc_names_by_id[location.ap_id]: location for location in all_locations if location.loc_type != LocationType.Event
}
location_id_to_data: dict[int, LocationData] = {
    location.ap_id: location for location in all_locations if location.loc_type != LocationType.Event
}
event_name_to_data: dict[str, LocationData] = {
    loc_names_by_id[location.ap_id]: location for location in all_locations if location.loc_type == LocationType.Event
}
event_id_to_name: dict[int, str] = {
    location.ap_id: loc_names_by_id[location.ap_id]
    for location in all_locations
    if location.loc_type == LocationType.Event
}
assert len(all_locations) == len(location_id_to_data) + len(events)
location_type_to_data: dict[str, list[LocationData]] = create_loctype_to_datamapping()

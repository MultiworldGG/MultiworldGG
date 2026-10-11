from ...locations.model import LocationView
from ...locations.shared import LOCATIONS
from ..address_maps import PLANET_MISSION_ADDRESSES

_MISSIONS = tuple(
    sorted(
        (location for location in LOCATIONS if location.completed.source == "missions"),
        key=lambda location: location.check_order,
    )
)
STORY_MISSION_MAP = LocationView(
    _MISSIONS,
    lambda location: "cutscene" not in location.categories,
    key=lambda location: (location.completed.key, location.completed.mask),
    value=lambda location: location.name,
)
CUTSCENE_MAP = LocationView(
    _MISSIONS,
    lambda location: "cutscene" in location.categories,
    key=lambda location: (location.completed.key, location.completed.mask),
    value=lambda location: location.name,
)
MISSION_COMPLETE_MAP = LocationView(
    _MISSIONS,
    key=lambda location: (location.completed.key, location.completed.mask),
    value=lambda location: location.name,
)
VALIDATED_MISSION_MAP = MISSION_COMPLETE_MAP
LOCATION_TO_PLANET_ID = LocationView(_MISSIONS, value=lambda location: location.completed.planet_id)
PLANET_BY_ADDR = {address: name for name, address in PLANET_MISSION_ADDRESSES.items()}

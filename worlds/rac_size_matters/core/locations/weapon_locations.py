from ...constants import Rac5Gadgets, Rac5Planets
from ...locations import shared
from ...locations.model import LocationView

_SLOT_TO_UNLOCK_ATTR = {
    "mod_slot_one": "mod_unlock_one",
    "mod_slot_two": "mod_unlock_two",
    "mod_slot_three": "mod_unlock_three",
}
MOD_UNLOCK_EXTRA_GADGETS = {Rac5Planets.CHALLAX: (Rac5Gadgets.SHRINK_RAY, Rac5Gadgets.POLARIZER)}


VENDOR_WEAPON_LOC = shared.VENDOR_WEAPON_LOC
VENDOR_GADGET_LOC = shared.VENDOR_GADGET_LOC
WEAPON_TO_LOCATION = shared.WEAPON_TO_LOCATION
GADGET_TO_LOCATION = shared.GADGET_TO_LOCATION
MOD_TO_LOCATION = shared.MOD_TO_LOCATION
TITAN_TO_LOCATION = shared.TITAN_TO_LOCATION
_MOD_LOC = LocationView(
    shared.LOCATIONS,
    lambda location: location.mod_slot is not None,
    value=lambda location: (location.weapon, location.mod_slot),
)
_TITAN_LOC = shared.VENDOR_TITAN_LOC
MOD_UNLOCK_PLANET = LocationView(
    shared.LOCATIONS,
    lambda location: location.mod_slot is not None,
    key=lambda location: (location.weapon, _SLOT_TO_UNLOCK_ATTR[location.mod_slot]),
    value=lambda location: location.planet,
)

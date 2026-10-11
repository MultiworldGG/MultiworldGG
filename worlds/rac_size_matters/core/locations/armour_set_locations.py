from ...locations.model import ArmourSetCompletion as ArmourSetCheck, LocationView
from ...locations.shared import LOCATIONS

__all__ = ["ArmourSetCheck", "ARMOUR_SET_CHECKS"]

ARMOUR_SET_CHECKS = LocationView(
    LOCATIONS, lambda location: "armour_set_check" in location.categories, value=lambda location: location.completed
)

"""This module provides a list of Excluded locations for the Rac3 apworld"""

from Options import ExcludeLocations


class RAC3ExcludeLocations(ExcludeLocations):
    """Prevent these locations from having an important item."""
    default = frozenset()

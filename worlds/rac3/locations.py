"""This module provides handling of location objects"""

from typing import TYPE_CHECKING

from worlds.rac3.constants.data.location import RAC3_LOCATION_DATA_TABLE
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.region import RAC3REGION

if TYPE_CHECKING:
    from worlds.rac3.world import RaC3World


def get_total_locations(world: "RaC3World") -> int:
    """Returns the total number of locations in the apworld"""
    locations = [loc for loc in world.multiworld.get_locations() if loc.player == world.player]
    return len(locations)


def get_location_names() -> dict[str, int]:
    """Returns a dictionary mapping location names to their apcodes"""
    return {name: data.AP_CODE for name, data in RAC3_LOCATION_DATA_TABLE.items()}


def get_from_tag(tag) -> set[str]:
    """Return a set of location names that match the given tag"""
    return {loc for loc in RAC3_LOCATION_DATA_TABLE.keys() if tag in RAC3_LOCATION_DATA_TABLE[loc].TAGS}


# class EventData(NamedTuple):
#     ap_code: None
#     region: Optional[str]
#
#
# rac3_events = {  # Events have no ap_code
#     "Cleared Veldin": EventData(None, RAC3REGION.VELDIN),
#     "Cleared Florana": EventData(None, RAC3REGION.FLORANA),
#     "Cleared Marcadia": EventData(None, RAC3REGION.MARCADIA),
#     "Cleared Annihilation Nation 1": EventData(None, RAC3REGION.ANNIHILATION_NATION),
#     "Cleared Annihilation Nation 2": EventData(None, RAC3REGION.ANNIHILATION_NATION_2),
#     "Cleared Aquatos": EventData(None, RAC3REGION.AQUATOS),
#     "Cleared Tyhrranosis": EventData(None, RAC3REGION.TYHRRANOSIS),
#     "Cleared Daxx": EventData(None, RAC3REGION.DAXX),
# }


all_tags: list[str] = [
    RAC3TAG.SKILLPOINT,
    RAC3TAG.T_BOLT,
    RAC3TAG.SEWER,
    RAC3TAG.VIDCOMIC,
    RAC3TAG.TROPHY,
    RAC3TAG.LONG_TROPHY,
    RAC3TAG.RANGERS,
    RAC3TAG.ARENA,
    RAC3TAG.NANOTECH,
    RAC3TAG.UNSTABLE,
    RAC3TAG.WEAPONS,
    RAC3TAG.ARMOR,
    RAC3TAG.SHIP,
    RAC3TAG.GADGETS,
    RAC3TAG.INFOBOT,
    RAC3TAG.VR,
    RAC3TAG.ONE_HP_UNSTABLE,
    RAC3TAG.NGPLUS,
    RAC3TAG.WEAPON_LEVEL,
]

location_groups: dict[str, set[str]] = {
    RAC3REGION.VELDIN: get_from_tag(RAC3REGION.VELDIN),
    RAC3REGION.FLORANA: get_from_tag(RAC3REGION.FLORANA),
    RAC3REGION.STARSHIP_PHOENIX: get_from_tag(RAC3REGION.STARSHIP_PHOENIX),
    RAC3REGION.MARCADIA: get_from_tag(RAC3REGION.MARCADIA),
    RAC3REGION.ANNIHILATION_NATION: get_from_tag(RAC3REGION.ANNIHILATION_NATION),
    RAC3REGION.AQUATOS: get_from_tag(RAC3REGION.AQUATOS),
    RAC3REGION.TYHRRANOSIS: get_from_tag(RAC3REGION.TYHRRANOSIS),
    RAC3REGION.DAXX: get_from_tag(RAC3REGION.DAXX),
    RAC3REGION.OBANI_GEMINI: get_from_tag(RAC3REGION.OBANI_GEMINI),
    RAC3REGION.BLACKWATER_CITY: get_from_tag(RAC3REGION.BLACKWATER_CITY),
    RAC3REGION.HOLOSTAR_STUDIOS: get_from_tag(RAC3REGION.HOLOSTAR_STUDIOS),
    RAC3REGION.OBANI_DRACO: get_from_tag(RAC3REGION.OBANI_DRACO),
    RAC3REGION.ZELDRIN_STARPORT: get_from_tag(RAC3REGION.ZELDRIN_STARPORT),
    RAC3REGION.METROPOLIS: get_from_tag(RAC3REGION.METROPOLIS),
    RAC3REGION.CRASH_SITE: get_from_tag(RAC3REGION.CRASH_SITE),
    RAC3REGION.ARIDIA: get_from_tag(RAC3REGION.ARIDIA),
    RAC3REGION.QWARKS_HIDEOUT: get_from_tag(RAC3REGION.QWARKS_HIDEOUT),
    RAC3REGION.KOROS: get_from_tag(RAC3REGION.KOROS),
    RAC3REGION.COMMAND_CENTER: get_from_tag(RAC3REGION.COMMAND_CENTER),
    RAC3TAG.SKILLPOINT: get_from_tag(RAC3TAG.SKILLPOINT),
    RAC3TAG.T_BOLT: get_from_tag(RAC3TAG.T_BOLT),
    RAC3TAG.SEWER: get_from_tag(RAC3TAG.SEWER),
    RAC3TAG.VIDCOMIC: get_from_tag(RAC3TAG.VIDCOMIC),
    RAC3TAG.TROPHY: get_from_tag(RAC3TAG.TROPHY),  # All trophies including long term
    RAC3TAG.LONG_TROPHY: get_from_tag(RAC3TAG.LONG_TROPHY),  # Long Term trophies only
    RAC3TAG.RANGERS: get_from_tag(RAC3TAG.RANGERS),
    RAC3TAG.ARENA: get_from_tag(RAC3TAG.ARENA),
    RAC3TAG.NANOTECH: get_from_tag(RAC3TAG.NANOTECH),
    RAC3TAG.UNSTABLE: get_from_tag(RAC3TAG.UNSTABLE),
    RAC3TAG.WEAPONS: get_from_tag(RAC3TAG.WEAPONS),
    RAC3TAG.ARMOR: get_from_tag(RAC3TAG.ARMOR),
    RAC3TAG.SHIP: get_from_tag(RAC3TAG.SHIP),
    RAC3TAG.GADGETS: get_from_tag(RAC3TAG.GADGETS),
    RAC3TAG.INFOBOT: get_from_tag(RAC3TAG.INFOBOT),
    RAC3TAG.ONE_HP_UNSTABLE: get_from_tag(RAC3TAG.ONE_HP_UNSTABLE),
    RAC3TAG.NGPLUS: get_from_tag(RAC3TAG.NGPLUS),
    RAC3TAG.VR: get_from_tag(RAC3TAG.VR),
    RAC3TAG.WEAPON_LEVEL: get_from_tag(RAC3TAG.WEAPON_LEVEL),
}


def get_region_locations(region: str) -> set[str]:
    """Returns a set of location names for a given region"""
    return set(level[0] for level in get_region_location_data(region))


def get_region_location_data(region: str) -> filter:
    """Returns the location data table filtered to a specific region"""
    return filter(lambda level: level[1].REGION == region, RAC3_LOCATION_DATA_TABLE.items())

from typing import TYPE_CHECKING

from BaseClasses import Location, Region

# TODO: revert
from worlds.gstla.gen.location_data import LocationData, LocationType, all_locations as all_gen_locations
from worlds.gstla.gen.location_names import LocationName, loc_names_by_id
from .game_data import ItemType

if TYPE_CHECKING:
    from .items import GSTLAItem


def allow_djinn(_, item: 'GSTLAItem') -> bool:
    return item.item_data.type == ItemType.Djinn


class GSTLALocation(Location):
    game: str = 'Golden Sun The Lost Age'
    location_data: LocationData
    item: 'GSTLAItem'

    def __init__(self, player: int, name: str, location: LocationData, region: Region):
        # Yes, calling str(name) because it's secretly an enum, and pickling does terrible things in MultiServer
        super().__init__(player, str(name), location.ap_id, region)
        self.location_data = location

    @staticmethod
    def create_djinn_location(player: int, name: str, location: LocationData, region: Region) -> 'GSTLALocation':
        ret = GSTLALocation(player, name, location, region)
        ret.always_allow = allow_djinn
        return ret

    @staticmethod
    def create_event_location(player: int, name: str, location: LocationData, region: Region):
        ret = GSTLALocation(player, name, location, region)
        ret.address = None
        return ret


def create_loctype_to_datamapping() -> dict[LocationType, list[LocationData]]:
    """Creates a dictionary mapping LocationType to a list of all locations
    of that type
    """
    types: dict[LocationType, list[LocationData]] = {}
    for idx, data in enumerate(all_locations):
        if data.loc_type not in types:
            types[data.loc_type] = []
        types[data.loc_type].append(data)
    return types


all_locations: list[LocationData] = all_gen_locations
location_name_to_id: dict[str, LocationData] = {loc_names_by_id[location.ap_id]: location for location in all_locations}
location_type_to_data: dict[LocationType, list[LocationData]] = create_loctype_to_datamapping()

remote_blacklist: set[int] = {
    location_name_to_id[name].ap_id
    for name in [
        LocationName.Idejima_Jenna,
        LocationName.Idejima_Growth,
        LocationName.Idejima_Shamans_Rod,
        LocationName.Idejima_Whirlwind,
        LocationName.Idejima_Mind_Read,
        LocationName.Kibombo_Douse_Drop,
        LocationName.Kibombo_Frost_Jewel,
        LocationName.Contigo_Orb_of_Force,
        LocationName.Contigo_Lifting_Gem,
        LocationName.Contigo_Catch_Beads,
        LocationName.Contigo_Carry_Stone,
    ]
}
"""Locations that cannot have remote items"""

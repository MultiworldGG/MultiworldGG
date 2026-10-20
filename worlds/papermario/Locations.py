from typing import List

from BaseClasses import Location
from .data.LocationsList import location_table

"""Paper Mario came out August 11th, 2000 (in Japan)"""
location_id_prefix = 8112000000
location_name_to_id = {
    name: (location_id_prefix + index)
    for (index, name) in enumerate(location_table.keys())
}


# Special location class for paper mario that specifies paper mario specific
# info for locations
class PMLocation(Location):
    game: str = "Paper Mario"

    def __init__(
        self,
        player,
        name='',
        code=None,
        identifier=None,
        source_type=None,
        area_id=None,
        map_id=None,
        index=None,
        vanilla_item=None,
        keyname=None,
        price_keyname=None,
        vanilla_price=None,
        price_index=None,
        parent=None,
        internal=False,
        event=None,
        event_name=None,
    ):
        super(PMLocation, self).__init__(player, name, code, parent)
        self.identifier = identifier
        self.source_type = source_type
        self.area_id = area_id
        self.map_id = map_id
        self.index = index
        self.vanilla_item = vanilla_item
        self.keyname = keyname
        self.price_keyname = price_keyname
        self.vanilla_price = vanilla_price
        self.price_index = price_index
        self.never = False
        self.disabled = False
        self.event = event
        self.event_name = event_name
        self.internal = internal


# used when loading regions from json to create location objects
def location_factory(locations, player: int) -> PMLocation | List[PMLocation]:
    ret = []
    singleton = False

    # make sure location is a tuple and not a singleton for parsing purposes
    if isinstance(locations, str):
        locations = [locations]
        singleton = True

    # grab location info from location_table and create the PMLocation object
    # using that info
    for location in locations:
        if location in location_table:
            match_location = location
        else:
            match_location = next(
                filter(
                    lambda k: k.lower() == location.lower(),
                    location_table
                ),
                None
            )
        if match_location:
            (
                identifier,
                source_type,
                area_id,
                map_id,
                index,
                vanilla_item,
                keyname,
                price_keyname,
                vanilla_price,
                price_index
            ) = location_table[match_location]
            ret.append(PMLocation(
                player,
                match_location,
                location_name_to_id.get(match_location, None),
                identifier,
                source_type,
                area_id,
                map_id,
                index,
                vanilla_item,
                keyname,
                price_keyname,
                vanilla_price,
                price_index
            ))
        else:
            raise KeyError("Unknown Location", Location)

    # if it was a singleton originally, we need to return it as such
    if singleton:
        return ret[0]
    return ret

from __future__ import annotations

import typing

from BaseClasses import Location

base_id = 3_870_100


class OddCoupleLocation(Location):
    game: str = "Ratchet & Clank: The Odd Couple"


class LocationData(typing.NamedTuple):
    code: int
    item: typing.Optional[str]  # the item that must be held to access this location, or None if always accessible


# "The Odd Couple Intro" has no item requirement - it's always accessible, and
# the client checks it immediately on connecting. That's what actually seeds
# the very first item, rather than precollecting one into starting inventory.
INTRO_LOCATION = "The Odd Couple Intro"

location_table: typing.Dict[str, LocationData] = {
    INTRO_LOCATION: LocationData(base_id + 8, None),
    "Stereo": LocationData(base_id + 0, "Stereo"),
    "Fruit Bowl: Taxi Driver!": LocationData(base_id + 1, "Taxi Driver"),
    "Is That Captan Qwark?: Scene 1": LocationData(base_id + 2, "Gimp"),
    "Is That Captan Qwark?: Scene 2": LocationData(base_id + 3, "Gimp"),
    "Is That Captan Qwark?: Scene 3": LocationData(base_id + 4, "Gimp"),
    "Join The Darkside: Phonecall": LocationData(base_id + 5, "Phonecall"),
    "Snip Snip: Scissors": LocationData(base_id + 6, "Scissors"),
    "A link to the past: TV": LocationData(base_id + 7, "TV"),
}

lookup_id_to_name: typing.Dict[int, str] = {data.code: name for name, data in location_table.items()}

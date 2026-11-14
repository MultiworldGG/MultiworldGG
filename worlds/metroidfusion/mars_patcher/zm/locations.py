import json
from typing import TypeAlias

from typing_extensions import Self

from ..item_messages import ItemMessages
from .auto_generated_types import (
    MarsschemazmLocations,
    MarsschemazmLocationsMajorLocationsItem,
    MarsschemazmLocationsMinorLocationsItem,
)
from .constants.items import (
    ITEM_TO_SPRITE,
    HintLocation,
    ItemJingle,
    ItemSprite,
    ItemType,
    MajorSource,
)
from .data import get_data_path

MarsSchemaZmLocation: TypeAlias = (
    MarsschemazmLocationsMajorLocationsItem | MarsschemazmLocationsMinorLocationsItem
)


class Location:
    def __init__(
        self,
        area: int,
        room: int,
        orig_item: ItemType,
        new_item: ItemType = ItemType.UNDEFINED,
        item_sprite: ItemSprite = ItemSprite.DEFAULT,
        item_messages: ItemMessages | None = None,
        item_jingle: ItemJingle = ItemJingle.DEFAULT,
        hinted_by: HintLocation = HintLocation.NONE,
    ):
        if type(self) is Location:
            raise TypeError()
        self.area = area
        self.room = room
        self.orig_item = orig_item
        self.new_item = new_item
        self.item_sprite = item_sprite
        self.item_messages = item_messages
        self.item_jingle = item_jingle
        self.hinted_by = hinted_by

    def __str__(self) -> str:
        item_str = self.orig_item.name
        item_str += "/" + self.new_item.name
        return f"{self.area},0x{self.room:02X}: {item_str}"

    @property
    def actual_item_sprite(self) -> ItemSprite:
        if self.item_sprite == ItemSprite.DEFAULT:
            return ITEM_TO_SPRITE[self.new_item]
        return self.item_sprite

    @property
    def hint_value(self) -> int:
        return 0xFF if self.hinted_by == HintLocation.NONE else self.hinted_by.value


class MajorLocation(Location):
    def __init__(
        self,
        area: int,
        room: int,
        map_x: int,
        map_y: int,
        major_src: MajorSource,
        orig_item: ItemType,
        new_item: ItemType = ItemType.UNDEFINED,
        item_sprite: ItemSprite = ItemSprite.DEFAULT,
        item_messages: ItemMessages | None = None,
        item_jingle: ItemJingle = ItemJingle.DEFAULT,
        hinted_by: HintLocation = HintLocation.NONE,
    ):
        super().__init__(
            area, room, orig_item, new_item, item_sprite, item_messages, item_jingle, hinted_by
        )
        self.map_x = map_x
        self.map_y = map_y
        self.major_src = major_src


class MinorLocation(Location):
    def __init__(
        self,
        area: int,
        room: int,
        block_x: int,
        block_y: int,
        hidden: bool,
        orig_item: ItemType,
        new_item: ItemType = ItemType.UNDEFINED,
        item_sprite: ItemSprite = ItemSprite.DEFAULT,
        item_messages: ItemMessages | None = None,
        item_jingle: ItemJingle = ItemJingle.DEFAULT,
        hinted_by: HintLocation = HintLocation.NONE,
    ):
        super().__init__(
            area, room, orig_item, new_item, item_sprite, item_messages, item_jingle, hinted_by
        )
        self.block_x = block_x
        self.block_y = block_y
        self.hidden = hidden

    @property
    def key(self) -> int:
        # See MINOR_LOC_KEY macro in include/randomizer.h
        return (self.area << 24) | (self.room << 16) | (self.block_y << 8) | self.block_x


class LocationSettings:
    def __init__(self, major_locs: list[MajorLocation], minor_locs: list[MinorLocation]):
        self.major_locs = major_locs
        self.minor_locs = minor_locs

    @classmethod
    def initialize(cls) -> Self:
        with open(get_data_path("locations.json")) as f:
            data = json.load(f)

        major_locs = []
        for entry in data["major_locations"]:
            major_loc = MajorLocation(
                entry["area"],
                entry["room"],
                entry["map_x"],
                entry["map_y"],
                MajorSource[entry["source"]],
                ItemType[entry["original"]],
            )
            major_locs.append(major_loc)

        minor_locs = []
        for entry in data["minor_locations"]:
            minor_loc = MinorLocation(
                entry["area"],
                entry["room"],
                entry["block_x"],
                entry["block_y"],
                entry["hidden"],
                ItemType[entry["original"]],
            )
            minor_locs.append(minor_loc)

        return cls(major_locs, minor_locs)

    def set_assignments(self, data: MarsschemazmLocations) -> None:
        for maj_loc_entry in data["major_locations"]:
            source = MajorSource[maj_loc_entry["source"]]
            # Find location with this source
            try:
                maj_loc = next(m for m in self.major_locs if m.major_src == source)
            except StopIteration:
                raise ValueError(f"Invalid major location: Source {source}")
            LocationSettings.set_location_data(maj_loc, maj_loc_entry)

        for min_loc_entry in data["minor_locations"]:
            # Get area, room, block X, block Y
            area = min_loc_entry["area"]
            room = min_loc_entry["room"]
            block_x = min_loc_entry["block_x"]
            block_y = min_loc_entry["block_y"]
            # Find location with this area, room, and position
            try:
                min_loc = next(
                    m
                    for m in self.minor_locs
                    if m.area == area
                    and m.room == room
                    and m.block_x == block_x
                    and m.block_y == block_y
                )
            except StopIteration:
                raise ValueError(
                    f"Invalid minor location: Area {area}, Room {room}, X {block_x}, Y {block_y}"
                )
            LocationSettings.set_location_data(min_loc, min_loc_entry)

    @classmethod
    def set_location_data(cls, loc_obj: Location, loc_entry: MarsSchemaZmLocation) -> None:
        """Sets item, item sprite, custom message (if any), jingle, and hint
        on a major or minor location."""
        loc_obj.new_item = ItemType[loc_entry["item"]]

        if "item_sprite" in loc_entry:
            loc_obj.item_sprite = ItemSprite[loc_entry["item_sprite"]]

        if "jingle" in loc_entry:
            loc_obj.item_jingle = ItemJingle[loc_entry["jingle"]]
        else:
            loc_obj.item_jingle = ItemJingle.DEFAULT

        if "hinted_by" in loc_entry:
            loc_obj.hinted_by = HintLocation[loc_entry["hinted_by"]]
        else:
            loc_obj.hinted_by = HintLocation.NONE

        if "item_messages" in loc_entry:
            loc_obj.item_messages = ItemMessages.from_json(loc_entry["item_messages"])

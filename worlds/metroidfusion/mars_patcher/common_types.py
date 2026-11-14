from typing import Annotated, TypeAlias

from .mf import auto_generated_types as types_mf
from .zm import auto_generated_types as types_zm

BytesLike: TypeAlias = bytes | bytearray

TypeU8: TypeAlias = types_mf.TypeU8 | types_zm.TypeU8

AreaId: TypeAlias = types_mf.AreaId | types_zm.AreaId
RoomId: TypeAlias = TypeU8

AreaRoomPair = tuple[AreaId, RoomId]

MinimapId: TypeAlias = Annotated[int, "0 <= value < 10"]

RoomNamesItem: TypeAlias = types_mf.MarsschemamfRoomNamesItem | types_zm.MarsschemazmRoomNamesItem

ItemMessagesType: TypeAlias = types_mf.ItemMessages | types_zm.ItemMessages

MusicMapping: TypeAlias = types_mf.MusicMapping | types_zm.MusicMapping

from enum import IntFlag, auto


class TransitionType(IntFlag):
    _TWO_WAY_FLAG = auto()
    _DUNGEON_FLAG = auto()
    _PORTAL_FLAG = auto()

    BASIC_ONE_WAY = 0
    BASIC_TWO_WAY = _TWO_WAY_FLAG
    DUNGEON = _TWO_WAY_FLAG | _DUNGEON_FLAG
    PORTAL = _TWO_WAY_FLAG | _PORTAL_FLAG

    def is_two_way(self) -> bool:
        return bool(TransitionType._TWO_WAY_FLAG & self)

    def is_dungeon_entrance(self) -> bool:
        return bool(TransitionType._DUNGEON_FLAG & self)

    def is_portal_entrance(self) -> bool:
        return bool(TransitionType._PORTAL_FLAG & self)

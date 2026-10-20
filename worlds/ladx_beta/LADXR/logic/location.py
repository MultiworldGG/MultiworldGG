import typing
from .requirements import hasConsumableRequirement, OR
from ..locations.itemInfo import ItemInfo


class Location:
    def __init__(self, name=None, dungeon=None):
        self.name = name
        self.items = []  # type: typing.List[ItemInfo]
        self.dungeon = dungeon
        self.__connected_to = set()
        self.connections = []

    def add(self, *item_infos):
        for ii in item_infos:
            assert isinstance(ii, ItemInfo)
            ii.setLocation(self)
            self.items.append(ii)
        return self

    def connect(self, other, req, *, one_way=False):
        assert isinstance(other, Location), type(other)

        if isinstance(req, bool):
            if req:
                self.connect(other, None, one_way=one_way)
            return

        if other in self.__connected_to:
            for idx, data in enumerate(self.connections):
                if data[0] == other:
                    if req is None or data[1] is None:
                        self.connections[idx] = (other, None)
                    else:
                        self.connections[idx] = (other, OR(req, data[1]))
                    break
        else:
            self.__connected_to.add(other)
            self.connections.append((other, req))
        if not one_way:
            other.connect(self, req, one_way=True)
        return self

    def __repr__(self):
        return "<%s:%s:%d:%d>" % (self.__class__.__name__, self.dungeon, len(self.items), len(self.connections))

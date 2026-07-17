from collections import OrderedDict
from BaseClasses import Location, MultiWorld
from Options import Option
from dataclasses import dataclass, field, replace
from typing import Generator, Optional


from .Options import XenobladeXOptions
from .Regions import add_region_location, init_region, trim_regions


@dataclass(frozen=True)
class Loc:
    name: str
    valid: bool = True
    regions: list[str] = field(default_factory=lambda: ['Menu'])
    depends: list[str] = field(default_factory=lambda: [])
    type: Optional[int] = None
    id: Optional[int] = None
    prefix: Optional[str] = None
    required: bool = False

    def get_location(self):
        return f"{self.prefix}: {self.name}"

    def get_region(self):
        return "+".join(sorted(self.regions))


from .locations.collepedia import collepedia_data  # noqa: E402
from .locations.enemies import enemies_data  # noqa: E402
from .locations.fnNodes import fn_nodes_data  # noqa: E402
from .locations.locations import locations_data  # noqa: E402
from .locations.segments import segments_data  # noqa: E402
# from .locations.quests import quests_data  # noqa: E402
# from .locations.shops import shops_data  # noqa: E402


class XenobladeXLocation(Location):
    game: str = "Xenoblade X"


game_type_location_to_offset: OrderedDict[int, int] = OrderedDict()


class _Locs:
    table_size = 0
    last_table_size = 0

    @staticmethod
    def gen(prefix: str, type: int, data: list[Loc]) -> Generator[Loc, None, None]:
        _Locs.table_size += _Locs.last_table_size
        game_type_location_to_offset[type] = _Locs.table_size
        _Locs.last_table_size = len(data)
        return (replace(e, type=type, id=_Locs.table_size + i + 1, prefix=prefix)
                for i, e in enumerate(data) if e.valid)


xenobladeXLocations = [
    *_Locs.gen("CLP", 0, collepedia_data),
    *_Locs.gen("EBK", 1, enemies_data),
    *_Locs.gen("FNO", 2, fn_nodes_data),
    *_Locs.gen("SEG", 3, segments_data),
    *_Locs.gen("LOC", 4, locations_data),
    # *_Locs.gen("QST", 5, quests_data),
    # *_Locs.gen("SHP", 6, shops_data),
]


def _resolve_dependencies() -> None:
    dependency_lookup: dict[str, int] = {}
    for i, loc in enumerate(xenobladeXLocations):
        dependency = loc.name.split(" - ")[0]
        if dependency not in loc.depends:
            dependency_lookup[dependency] = i

    for loc_i in range(len(xenobladeXLocations)):
        loc = xenobladeXLocations[loc_i]
        dependencies = loc.depends.copy()
        regions: list[str] = loc.regions.copy()
        while True:
            if len(dependencies) < 1:
                break
            dependency = dependencies.pop()
            dep_loc = xenobladeXLocations[dependency_lookup[dependency]]
            dependencies += dep_loc.depends
            regions += dep_loc.regions
        xenobladeXLocations[loc_i] = replace(loc, regions=trim_regions(set(regions)), depends=[])


_resolve_dependencies()


def create_location(world: MultiWorld, region_name: str, location_name: str, player: int, abs_id: Optional[int]):
    region_name = init_region(world, player, region_name)
    return add_region_location(world, player, region_name,
                               XenobladeXLocation(player, location_name, abs_id, world.get_region(region_name, player)))


def create_locations(world: MultiWorld, options: XenobladeXOptions, player: int, base_id: int):
    for location in xenobladeXLocations:
        if location.prefix is None or location.id is None:
            continue
        location_option: Optional[Option] = getattr(options, location.prefix.lower(), None)
        if location.required or location_option is None or location_option.value:
            create_location(world, location.get_region(), location.get_location(), player, base_id + location.id)

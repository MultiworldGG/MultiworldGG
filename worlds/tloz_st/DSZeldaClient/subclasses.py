from enum import IntEnum
from typing import TYPE_CHECKING, Iterable
import worlds._bizhawk as bizhawk
from math import ceil

if TYPE_CHECKING:
    try:
        from ..Client import PhantomHourglassClient
        from worlds._bizhawk.context import BizHawkClientContext
    except ImportError:
        pass

print_debug: list[str] = []

def hex_f(i):
    """hex() but can handle all datatype exceptions recursively"""
    if isinstance(i, int):
        return hex(i)
    if isinstance(i, dict):
        return {hex_f(k): hex_f(v) for k, v in i.items()}
    if isinstance(i, Iterable) and not isinstance(i, str):
        return [hex_f(j) for j in i]
    return i

def printl(s, silent=False) -> None:
    """Prints to console, but also saves print output in case the client asks for it."""
    s = str(s)
    s = s.replace("\t", "  ")
    if not silent:
        print(s)
    print_debug.append(s)

async def read_multiple(ctx, addresses, signed=False, keys=None, offset=0) -> dict["Address", int] or dict[str, int]:
    # print(f"\t reading {list(addresses)}")
    read_list = [a.get_inner_read_list() for a in addresses]
    if offset:
        read_list = [(a+offset, *args) for a, *args in read_list]
    reads = []
    chunk_size = 128
    for i in range(ceil(len(read_list)/chunk_size)):
        reads += await bizhawk.read(ctx.bizhawk_ctx, read_list[chunk_size*i:chunk_size*(i+1)])

    # reads = await bizhawk.read(ctx.bizhawk_ctx, read_list)
    reads = [int.from_bytes(r, "little", signed=signed) for r in reads]
    if keys:
        return {k: r for k, r in zip(keys, reads)}
    return {a: r for a, r in zip(addresses, reads)}

async def write_multiple(ctx, addresses: Iterable["Address"], values: Iterable[int]):
    writes = [a.get_inner_write_list(v) for a, v in zip(addresses, values)]
    # print(f"Writing: {hex_f(writes)}")
    await bizhawk.write(ctx.bizhawk_ctx, writes)


# Get address from pointer
async def get_address_from_heap(ctx, pointer, offset=0, size=4) -> "Address":
    """
    Reads a pointer, and follows that pointer with an offset
    :param size: how many bytes
    :param ctx:
    :param pointer:
    :param offset:
    :return:
    """
    m_course = 0
    while m_course == 0:
        m_course = await pointer.read(ctx)
    m_course = Address.from_pointer(m_course, size=3)
    read = await m_course.read(ctx)
    print(f"Got map address @ {hex(read + offset)}")
    return Address.from_pointer(read + offset, size=size)

def storage_key(ctx, key: str):
    return f"{key}_{ctx.slot}_{ctx.team}"

def get_stored_data(ctx: "BizHawkClientContext", key, default=None):
    ctx.set_notify(storage_key(ctx, key))
    store = ctx.stored_data.get(storage_key(ctx, key), default)
    store = store if store is not None else default
    return store

# Split up large values to write into smaller chunks
def split_bits(value, size):
    ret = []
    f = 0xFFFFFFFFFFFFFF00
    for _ in range(size):
        ret.append(value & 0xFF)
        value = (value & f) >> 8
    return ret

class Address:
    addr_eu: int
    addr_us: int
    addr: int
    current_region: int
    domain: str
    size: int
    offset: int
    name: str

    def __init__(self, addr_eu, addr_us=None, size=1, domain="Main RAM", name=""):
        self.addr_eu = addr_eu
        self.addr_us = addr_us if addr_us else None
        self.addr_lookup = [self.addr_eu, self.addr_us]
        self.addr = self.addr_eu

        self.current_region = 0
        self.domain = domain
        self.size = size
        self.name = name

        if self.addr:
            self.validate()

    def set_addr(self, value):
        self.addr = value
        self.addr_eu = value
        self.addr_lookup[0] = value

    def get_address(self, region=None):
        if region is not None:
            region = self._region_int(region)
            return self.addr_lookup[region]
        return self.addr

    def validate(self):
        if self.domain == "Main RAM":
            if not 0 < self.addr_eu < 0x400000:
                self.set_addr(0)

    def set_region(self, region: str or int):
        self.current_region = self._region_int(region)
        self.addr = self.addr_lookup[self.current_region]

    @staticmethod
    def _region_int(region: str or int):
        if isinstance(region, str):
            assert region.lower() in ["eu", "us"]
            region = ["eu", "us"].index(region.lower())
        assert region in [0, 1]
        return region

    def get_read_list(self):
        return [self.get_inner_read_list()]

    def get_inner_read_list(self) -> tuple:
        return self.addr, self.size, self.domain

    def get_write_list(self, value:int or list):
        return [self.get_inner_write_list(value)]

    def get_inner_write_list(self, value: int or list, offset: int=0, size: int=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        size = self.size if not size else size
        return self.addr+offset, value[:size], self.domain

    async def read(self, ctx, signed=False, silent=False):
        read_result = await self.read_bytes(ctx)
        res = sum([int.from_bytes(b, "little", signed=signed)<<(8*i) for i, b in enumerate(read_result)])
        if not silent:
            printl(f"\tReading address {self}, got value {hex_f(res)}")
        return res

    async def read_bytes(self, ctx):
        return await bizhawk.read(ctx.bizhawk_ctx, [(self.addr, self.size, self.domain)])

    async def overwrite(self, ctx, value, silent=False, offset=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        if not silent:
            printl(f"\tWriting to address {self} with value {hex_f(value)}")
        return await bizhawk.write(ctx.bizhawk_ctx, [(self.addr+offset, value, self.domain)])

    async def add(self, ctx, value: int, silent=False, offset=0):
        silent=False
        prev = await self.read(ctx, silent=silent)
        return await self.overwrite(ctx, prev + value, silent=silent, offset=offset)

    async def set_bits(self, ctx, value: int or list, silent=False, offset=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        prev = split_bits(await self.read(ctx, silent=silent), self.size)
        # print(f"Setting bits {self} {prev} {value} {[p | v for p, v in zip(prev, value)]}")
        return await self.overwrite(ctx, [p | v for p, v in zip(prev, value)], silent=silent, offset=offset)

    async def unset_bits(self, ctx, value: int or list, silent=False, offset=0):
        if isinstance(value, int):
            value = split_bits(value, self.size)
        prev = split_bits(await Address.from_pointer(self + offset, self.size).read(ctx, silent=silent), self.size)
        # print(f"Setting bits {self} {prev} {value} {[p | v for p, v in zip(prev, value)]}")
        return await self.overwrite(ctx, [p & (~v) for p, v in zip(prev, value)], silent=silent, offset=offset)


    def __repr__(self, region="eu"):
        return f"Address Object {hex_f(self.get_address(region))} {self.name}"

    def __str__(self):
        name = f"{self.name}: " if self.name else ""
        return f"{name}{hex(self.get_address())}"

    def __add__(self, other):
        return self.addr + other

    def __sub__(self, other):
        if isinstance(other, Address):
            return self.addr - other.addr
        return self.addr - other

    def __eq__(self, other):
        return self.addr == other

    def __ne__(self, other):
        return self.addr != other

    def __bool__(self):
        return bool(self.addr)

    def __hash__(self):
        return self.addr

    def __gt__(self, other):
        return self.addr > other

    def __lt__(self, other):
        return self.addr < other

    def __ge__(self, other):
        return self.addr >= other

    def __le__(self, other):
        return self.addr <= other

    def __int__(self):
        return self.addr

    @classmethod
    def pointer(cls, addr, name=""):
        """Pointer from Data TCM"""
        return cls(addr, addr, 4, "Data TCM", name)

    @classmethod
    def from_pointer(cls, addr, size=1, domain="Main RAM", name=""):
        """When addresses are grabbed from pointers, the address is the same in all versions"""
        return cls(addr, addr, size, domain, name)

class DTCM(Address):
    def __init__(self, addr):
        super().__init__(addr, addr, 3, "Data TCM")

class AddressLoader(Address):
    """
    Address who's first argument is a dtcm address, that needs to be loaded before it can be used as an address
    """
    dtcm_addr: "Address"
    load_offset: int

    def __init__(self, dtcm_addr, size=1, load_offset=0, domain="Main RAM", name=""):
        self.dtcm_addr = dtcm_addr
        self.load_offset = load_offset
        super().__init__(None, None, size, domain, name)

    async def load(self, ctx):
        self.set_addr(await self.dtcm_addr.read(ctx) + self.load_offset)

    async def read_bytes(self, ctx):
        if not self.addr:
            await self.load(ctx)
        return await super().read_bytes(ctx)

class DoubleAddressLoader(AddressLoader):

    async def load(self, ctx):
        pointer = Address.from_pointer(await self.dtcm_addr.read(ctx), size=3)
        self.set_addr(await pointer.read(ctx) + self.load_offset)

async def load_multi(ctx, loader_list: list["AddressLoader"]):
    """Load multiple address loaders"""
    read_list: list = [addr.dtcm_addr for addr in loader_list]
    read_res = await read_multiple(ctx, read_list)
    for loader in read_list:
        loader.set_addr(read_res[loader.dtcm_addr] + loader.load_offset)


class SRAM(Address):
    """
    Saveram also has slot data to care about.
    """

    def __init__(self, addr_eu_1, addr_eu_2=None, addr_us_1=None, addr_us_2=None, name=""):
        super().__init__(addr_eu_1, addr_us_1, size=1, domain="SRAM", name=name)
        self.slot = 0
        self.addr_lookup = [(addr_eu_1, addr_eu_2), (addr_us_1, addr_us_2)]


    async def read(self, ctx, signed=False, silent=False, slot=0):
        addr = self.addr_lookup[self.current_region][self.slot]
        read_result = await bizhawk.read(ctx.bizhawk_ctx, [(addr, self.size, self.domain)])
        res = int.from_bytes(read_result[0], "little", signed=signed)
        if not silent:
            print(f"\tReading address {self}, got value {hex(res)}")
        return res

class DSTransition:
    """
    Datastructures for dealing with Transitions on the client side.
    Not to be confused with PHEntrances, that deals with entrance objects during ER placement.
    """
    entrance_groups: IntEnum | None = None  # set these in game instance or
    opposite_entrance_groups: dict[IntEnum, IntEnum] | None = None
    y_margin: int = 2000

    def __init__(self, name, data):
        self.data = data

        self.name: str = name
        self.id: int = data.get("id", None)
        assert self.id is not None

        self.entrance: tuple = data.get("entrance", None)
        self.exit: tuple = data.get("exit", None)
        self.entrance_region: str = data["entrance_region"]
        self.exit_region: str = data["exit_region"]
        self.two_way: bool = data.get("two_way", True)
        self.category_group = data["type"]
        self.direction = data["direction"]
        self.island = data.get("island", self.entrance_groups.NONE if self.entrance_groups else None)
        self.coords: tuple | None = data.get("coords", None)
        self.extra_data: dict = data.get("extra_data", {})

        self.stage, self.room, _ = self.entrance if self.entrance else (None, None, None)
        self.scene: int = self.get_scene()
        self.exit_scene: int = self.get_exit_scene()
        self.exit_stage = self.exit[0] if self.exit else None
        self.y = self.coords[1] if self.coords else None

        self.vanilla_reciprocal: DSTransition | None = None  # Paired location

        self.copy_number = 0


    def get_scene(self):
        if self.room:
            return self.stage * 0x100 + self.room
        else:
            return self.stage << 8

    def get_exit_scene(self):
        if self.exit:
            return self.exit[0] * 0x100 + self.exit[1]
        else:
            return None

    def is_pairing(self, r1, r2) -> bool:
        return r1 == self.entrance_region and r2 == self.exit_region

    def get_y(self):
        return self.coords[1] if self.coords else None

    def detect_exit_simple(self, stage, room, entrance):
        return self.exit == (stage, room, entrance)

    def detect_exit_scene(self, scene, entrance):
        return self.exit_scene == scene and entrance == self.exit[2]

    def detect_exit(self, scene, entrance, coords, y_offest):
        if self.detect_exit_scene(scene, entrance):
            if entrance < 0xF0 and not hasattr(self, "extra_data"):
                return True
            # Continuous entrance check
            x_max = self.extra_data.get("x_max", 0x8FFFFFFF)
            x_min = self.extra_data.get("x_min", -0x8FFFFFFF)
            z_max = self.extra_data.get("z_max", 0x8FFFFFFF)
            z_min = self.extra_data.get("z_min", -0x8FFFFFFF)
            y = self.coords[1] if self.coords else self.extra_data.get("y", coords["y"]) - y_offest
            printl(f"Checking entrance {self.name}")
            printl(f"\tx: {x_max} > {coords['x']} > {x_min}")
            printl(f"\ty: {y + self.y_margin} > {coords['y'] - y_offest} > {y}")
            printl(f"\tz: {z_max} > {coords['z']} > {z_min}")
            if (y + self.y_margin > coords["y"] - y_offest >= y
                    and x_max > coords["x"] > x_min
                    and z_max > coords["z"] > z_min):
                printl(f"\tMatch!")
                return True
        return False

    def set_stage(self, new_stage):
        self.stage = new_stage
        self.scene = self.get_scene()
        self.entrance = tuple([new_stage] + list(self.entrance[1:]))

    def set_exit_stage(self, new_stage):
        self.exit = tuple([new_stage] + list(self.exit[1:]))
        self.exit_scene = self.get_exit_scene()
        self.exit_stage = self.exit[0]

    def set_exit_room(self, new_room):
        self.exit = tuple([self.exit[0], new_room, self.exit[2]])
        self.exit_scene = self.get_exit_scene()

    def copy(self):
        res = DSTransition(f"{self.name}{self.copy_number+1}", self.data)
        res.copy_number = self.copy_number + 1
        return res

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__} {self.name} {hex_f(self.entrance)} => {hex_f(self.exit)} | {self.extra_data}"

    def debug_print(self):
        printl(f"Debug print for entrance {self.name}")
        printl(f"\tentrance {self.entrance}")
        printl(f"\texit {self.exit}")
        printl(f"\tcoords {self.coords}")
        printl(f"\textra_data {self.extra_data}")

    @classmethod
    def from_data(cls, entrance_data):
        res = dict()
        counter = {}
        ident = 0
        for name, data in entrance_data.items():
            data["id"] = ident
            res[name] = cls(name, data)
            # print(f"{i} {ENTRANCES[name].entrance_region} -> {ENTRANCES[name].exit_region}")
            ident += 1
            point = data["entrance_region"] + "<=>" + data["exit_region"]
            counter.setdefault(point, 0)
            counter[point] += 1
            if "one_way_data" in data:
                res[name].extra_data |= data["one_way_data"]

            if data.get("two_way", True):
                two_way = True
            else:
                two_way = False
            reverse_name = data.get("return_name", f"Unnamed Entrance {ident}")
            reverse_data = {
                "entrance_region": data.get("reverse_exit_region", data["exit_region"]),
                "exit_region": data.get("reverse_entrance_region", data["entrance_region"]),
                "id": ident,
                "entrance": data.get("exit", data.get("entrance", None)),
                "exit": data["entrance"],
                "two_way": two_way,
                "type": data["type"],
                "island": data.get("return_island", data.get("island", cls.entrance_groups.NONE)),
                "direction": cls.opposite_entrance_groups[data["direction"]],
                "coords": data.get("coords", None),

            }
            if "extra_data" in data:
                reverse_data["extra_data"] = data["extra_data"]
            if "reverse_one_way_data" in data:
                reverse_data.setdefault("extra_data", {})
                reverse_data["extra_data"] = data["reverse_one_way_data"]
            if reverse_name in res:
                print(f"DUPLICATE ENTRANCE!!! {reverse_name}")
            res[reverse_name] = cls(reverse_name, reverse_data)

            res[name].vanilla_reciprocal = res[reverse_name]
            res[reverse_name].vanilla_reciprocal = res[name]

            # print(f"{i} {ENTRANCES[reverse_name].entrance_region} -> {ENTRANCES[reverse_name].exit_region}")
            ident += 1
            point: str = reverse_data["entrance_region"] + "<=>" + reverse_data["exit_region"]
            counter.setdefault(point, 0)
            counter[point] += 1
        return res


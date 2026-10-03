from .subclasses import Address, printl
from dataclasses import dataclass
from typing import Iterable, Any, Callable

@dataclass
class DSLocation:
    name: str
    id: int
    scenes: Iterable[int] | int | None = None
    region: str | None = None
    from_entrances: list[int] | int | None = None

    vanilla_item: str | Iterable[str] | None = None
    item_override: str | None = None
    location_groups: list[str] = None
    local: bool = False  # Always have items from own world

    y: int | None = None
    x_max: int | None = None
    x_min: int | None = None
    z_max: int | None = None
    z_min: int | None = None
    from_coords: dict[str, int] | None = None

    address: Address | None = None
    value: int = 1
    chest_offset: int | None = None
    gift_addr: Address | str | list[Address] | None = None
    shop_model: bool = False  # gift_addr for shop models are set during actor loop
    exact_read: bool = False
    do_special: str | dict = ""
    read_object: bool = False  # read the chest opening instead of normal triggers
    set_bit: list[Iterable] | None = None
    ut_connect: str = ""

    delay_reset: bool = False  # don't reset vanilla item from this location until getting another location or changing scene
    delay_pickup: str | list[str] | None = None
    conditional: Callable | None = None
    farmable: bool | str = False
    has_slot_data: list[Iterable] | None = None
    any_slot_data: list[Iterable] | None = None
    reload_chests: bool = False
    force_vanilla: bool = False
    persistent: bool = False  # don't remove from local locations in scene after triggering
    always_exist: bool = False
    restock: str = ""  # the category it's restocked behind, allowing it out early when applicable
    dig_spot: bool = False
    priority: int = -1
    no_model: bool = False

    hidden_vanilla_item: list[str] | None = None  # For shops that don't want to change model early

    dungeon: str = ""  # for in_own_dungeon gen and dungeon exclusion
    tos_section: int | str = 0
    boss_room: str = ""
    post_dungeon: str = ""
    boss_reward_location: bool = False
    island_shop: bool = False
    stamp: int | None = None
    minigame: list[int] = None
    goal: str = ""
    rabbit: bool = False
    realm: str = ""
    count: int = 0

    hint_entrance: str | list[str] = ""
    hint_entrance_secondary: str | list[str] = ""
    hint_entrance_tertiary: str | list[str] = ""

    sram_addr: Address | None = None
    sram_value: int | None = None

    def __post_init__(self):
        if isinstance(self.scenes, int):
            self.scenes = {self.scenes}
        if self.shop_model:
            self.exact_read = True
            self.delay_reset = True
        if isinstance(self.from_entrances, int):
            self.from_entrances = [self.from_entrances]

    # def __init__(self, name, **kwargs):
    #     self.name = name
    #
    #     for key, value in kwargs.items():
    #         if key not in self.__annotations__:
    #             print(f"Unknown location attribute: {key}: {value}")
    #         setattr(self, key, value)

    def compare(self, comp_value):
        return comp_value == self.value if self.exact_read else comp_value & self.value

    def check_coords(self, link_coords):
        printl(
            f"\tx: {self.get('x_max', 0x8FFFFFFF)} > {link_coords['x']} > {self.get('x_min', -0x8FFFFFFF)}")
        printl(
            f"\ty: {self.get('y', link_coords['y']) + 1000} > {link_coords['y']} >= {self.get('y', link_coords['y'])}")
        printl(
            f"\tz: {self.get('z_max', 0x8FFFFFFF)} > {link_coords['z']} > {self.get('z_min', -0x8FFFFFFF)}")

        return (self.get("x_max", 0x8FFFFFFF) > link_coords["x"] > self.get("x_min", -0x8FFFFFFF) and
                        self.get("z_max", 0x8FFFFFFF) > link_coords["z"] > self.get("z_min", -0x8FFFFFFF) and
                        self.get("y", link_coords["y"]) + 1000 > link_coords["y"] >= self.get("y", link_coords["y"]))

    def get(self, attribute, default:Any=False):
        res = getattr(self, attribute, default)
        if res is None:
            return default
        return res

    def __contains__(self, item):
        return self.get(item)

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        return setattr(self, key, value)
from typing import NamedTuple

TAG_REQUIRES_BOOST = "*Requires Boost"
TAG_CHAIN_CHOMP = "*Requires Chain Chomp"
TAG_REQUIRES_STAR = "*Requires Star"
TAG_NO_SLOW_KARTS = "*Requires 100cc"


class Line(NamedTuple):
    x1: float
    z1: float
    x2: float
    z2: float

    def get_p1(self) -> tuple[float, float]:
        return (self.x1, self.z1)
    
    def get_p2(self) -> tuple[float, float]:
        return (self.x2, self.z2)


class RouteLocation(NamedTuple):
    """Defines a route by expecting the player to cross 2 lines within a time window."""
    name: str
    start: Line
    end: Line
    time_limit: float
    void_height: float = -10000
    tags: set[str] = set() 


def get_loc_name_route(course: str, route: RouteLocation) -> str:
    """Returns route's location name."""
    return f"{course} - {route.name}"


def lines_intersect(l1: Line, l2: Line) -> bool:
    def ccw(a: tuple, b: tuple, c: tuple):
        return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])

    return (
        ccw(l1.get_p1(), l2.get_p1(), l2.get_p2()) != ccw(l1.get_p2(), l2.get_p1(), l2.get_p2()) and
        ccw(l1.get_p1(), l1.get_p2(), l2.get_p1()) != ccw(l1.get_p1(), l1.get_p2(), l2.get_p2())
    )

ROUTE_LOCATIONS: dict[str, list[RouteLocation]] = {
    "Dry Dry Desert": [
        RouteLocation("Survive Sand Pit", Line(18600, -7800, 17800, -7800), Line(19100, -7000, 17000, -7000), 1, void_height=3400, tags={TAG_REQUIRES_STAR}),
        RouteLocation("Last Sign Shortcut", Line(-18500, 9000, -15500, 6000), Line(-20000, 7300, -17000, 4600), 3, tags={TAG_REQUIRES_BOOST}),
    ],
    "Mushroom Bridge": [
        RouteLocation("Toad House Shortcut", Line(12000, -6300, 12100, -11600), Line(7700, -3800, 4800, -5700), 2, tags={TAG_REQUIRES_BOOST}),
    ],
    "Mario Circuit": [
        RouteLocation("Chain Chomp Shortcut", Line(5600, 17700, 2900, 19500), Line(9000, 22800, 6700, 24900), 2.2, tags={TAG_REQUIRES_BOOST, TAG_CHAIN_CHOMP}),
    ],
    "Daisy Cruiser": [
        RouteLocation("Pool Shortcut", Line(-22160, -2680, -21240, -3120), Line(-26000, -4610, -26000, -5840), 3),
    ],
    "Waluigi Stadium": [
        RouteLocation("Pond Shortcut", Line(-14500, -2900, -17100, -4600), Line(-17100, -200, -20000, -1800), 1.3, tags={TAG_REQUIRES_BOOST}),
    ],
    "Sherbet Land": [
        RouteLocation("Last Turn Shortcut", Line(-900, 22200, 1900, 20400), Line(-4400, 19100, -900, 19100), 4),
    ],
    "Mushroom City": [
        RouteLocation("Bridge Shortcut", Line(-3600, 1700, -3600, 2400), Line(6300, 1700, 6300, 2400), 4, tags={TAG_REQUIRES_BOOST}),
    ],
    "Yoshi Circuit": [
        RouteLocation("Arc Shortcut", Line(-8800, 13300, -5800, 12600), Line(-9700, 11700, -6700, 10400), 3, void_height=12900, tags={TAG_REQUIRES_BOOST, TAG_CHAIN_CHOMP, TAG_NO_SLOW_KARTS}),
        RouteLocation("Tunnel Shortcut", Line(3400, -18200, 2700, -16700), Line(5800, -15400, 4000, -14900), 3, void_height=12200, tags={TAG_REQUIRES_BOOST, TAG_CHAIN_CHOMP, TAG_NO_SLOW_KARTS}),
    ],
    "DK Mountain": [
        RouteLocation("Hairpin Turn Shortcut", Line(-11600, -25200, -9500, -22600), Line(-12100, -25100, -11400, -21200), 2, void_height=7400),
    ],
    "Dino Dino Jungle": [
        RouteLocation("Bridge Shortcut", Line(-18500, 8100, -18500, 7000), Line(-29200, 6500, -28300, 5640), 5, void_height=8100),
        RouteLocation("Cave Shortcut", Line(-20700, -14500, -20700, -12500), Line(-17300, -14700, -17300, -10800), 5, void_height=11000, tags={TAG_REQUIRES_BOOST, TAG_CHAIN_CHOMP, TAG_NO_SLOW_KARTS}),
    ],
    "Bowser's Castle": [
        RouteLocation("Cannon Room Shortcut", Line(-26580, 22600, -27550, 20900), Line(-29600, 22800, -32200, 22800), 3, void_height=8000),
    ],
}

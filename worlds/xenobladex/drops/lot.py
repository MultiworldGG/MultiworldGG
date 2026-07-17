# from https://xenoblade.github.io/xbx/bdat/common_local_us/DRP_AffixSlotTable.html
from typing import NamedTuple
class DropLot(NamedTuple):
    lot1Prob: int
    lot2Prob: int
    lot3Prob: int


DL = DropLot

# flake8: noqa
dropLotData: list[DropLot] = [
DL(0, 0, 0),  # add artifical empty for lookup
DL(100, 30, 5),
DL(100, 70, 30),
DL(100, 10, 0),
DL(100, 20, 0),
DL(100, 60, 0),
DL(100, 75, 0),
DL(100, 90, 0),
DL(100, 100, 0),
DL(100, 100, 0),
DL(100, 100, 100),
DL(100, 100, 100),
DL(100, 100, 100),
DL(100, 0, 0),
DL(100, 15, 0),
DL(100, 30, 0),
DL(100, 70, 0),
DL(100, 85, 0),
DL(100, 100, 0),
DL(100, 100, 0),
DL(100, 100, 100),
DL(100, 100, 100),
DL(100, 100, 100),
DL(10, 0, 0),
DL(30, 0, 0),
DL(30, 5, 1),
DL(30, 15, 3),
DL(10, 5, 0),
DL(20, 10, 0),
DL(60, 15, 0),
DL(70, 20, 0),
DL(80, 25, 0),
DL(50, 0, 0),
DL(50, 0, 0),
DL(100, 20, 3),
DL(100, 20, 2),
DL(100, 20, 1),
DL(0, 0, 0),
DL(10, 0, 0),
DL(20, 0, 0),
DL(40, 0, 0),
DL(80, 0, 0),
DL(100, 0, 0),
DL(100, 0, 0),
DL(100, 0, 0),
DL(100, 0, 0),
DL(100, 0, 0),
]
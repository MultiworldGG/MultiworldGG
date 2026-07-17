from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
doll_regions: List[Rule] = [
Rule("Menu"),
Rule("Blade License", {Req("KEY: Blade License")}),
Rule("Skell License", {Req("KEY: Skell License"), Req("SKF")}),
Rule("Flight Module", {Req("KEY: Flight Module")}),
]

key_fnet_regions: List[Rule] = [
Rule("Menu"),
Rule("FNet", {Req("KEY: FNet")}),
]

key_regions: List[Rule] = [
    *doll_regions,
    *key_fnet_regions
]

from typing import List
from ..Regions import Requirement as Req, Rule


fnet_precious_ressources_regions: List[Rule] = [
    Rule("Menu"),
    # all others
    Rule("FNet Resource", {Req("KEY: FNet")}),
    # Boiled-Egg Ore, Ouroboros Crystal, Parhelion Platinum, Marine Rutile
    Rule("FNet Resource 2", {Req("FLDSK: Mechanical", 1)})
]

fnet_miranium_regions: List[Rule] = [
    Rule("Menu"),
    # Anything < 6k: 700, 750, 900, 1200, 1800, 2400, 2500, 3600, 4000, 4200, 5500, 5700
    Rule("Miranium", {Req("KEY: FNet")}),
    Rule("Miranium 7", {Req("DP: Storage Probe", 1)}),
    Rule("Miranium 9.3", {Req("MIRANIUM", 9)}),
    Rule("Miranium 10", {Req("MIRANIUM", 10)}),
    Rule("Miranium 12", {Req("MIRANIUM", 12)}),
    Rule("Miranium 15", {Req("MIRANIUM", 15)}),
    Rule("Miranium 20", {Req("MIRANIUM", 20)}),
    Rule("Miranium 30", {Req("MIRANIUM", 30)}),
    Rule("Miranium 40", {Req("MIRANIUM", 40)}),
    Rule("Miranium 50", {Req("MIRANIUM", 50)}),  # Ares 70
    Rule("Miranium 100", {Req("MIRANIUM", 100)}),  # Ares 90
]

fnet_credits_regions: List[Rule] = [
    Rule("Menu"),
    # 3k just unlock all default mech 1 probes
    Rule("Credits", {Req("KEY: FNet")}),
    Rule("Credits 15", {Req("CREDITS", 15)}),
    Rule("Credits 70", {Req("CREDITS", 70)}),
    Rule("Credits 130", {Req("CREDITS", 130)}),
]

fnet_regions: List[Rule] = [
    *fnet_precious_ressources_regions,
    *fnet_miranium_regions,
    *fnet_credits_regions,
]

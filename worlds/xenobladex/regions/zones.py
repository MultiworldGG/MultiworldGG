from typing import List
from ..Regions import Requirement as Req, Rule


# 693 Segments
zones_mira_regions: List[Rule] = [
    Rule("Menu"),
    Rule("Mira 10", {Req("MIRA", 70)}),
    Rule("Mira 18", {Req("MIRA", 125)}),
    Rule("Mira 20", {Req("MIRA", 139)}),
    Rule("Mira 40", {Req("MIRA", 278)}),
    Rule("Mira 50", {Req("MIRA", 347)}),
    Rule("Mira 60", {Req("MIRA", 416)}),
    Rule("Mira 80", {Req("MIRA", 555)}),
]

# 87 Segments
zones_prim_regions: List[Rule] = [
    Rule("Menu"),
    Rule("Prim 15", {Req("PRIM", 14)}),
    Rule("Prim 50", {Req("PRIM", 44)})
]

# 77 Segments
zones_noct_regions: List[Rule] = [
    Rule("Menu"),
    Rule("Noct 15", {Req("NOCT", 12)}),
    Rule("Noct 20", {Req("NOCT", 16)}),
    Rule("Noct 25", {Req("NOCT", 20)}),
    Rule("Noct 30", {Req("NOCT", 24)}),
    Rule("Noct 45", {Req("NOCT", 35)}),
    Rule("Noct 85", {Req("NOCT", 66)}),
]

# 95 Segments
zones_obli_regions: List[Rule] = [
    Rule("Menu"),
    Rule("Obli 25", {Req("OBLI", 24)}),
    Rule("Obli 30", {Req("OBLI", 29)}),
    Rule("Obli 40", {Req("OBLI", 38)}),
    Rule("Obli 50", {Req("OBLI", 48)}),
    Rule("Obli 70", {Req("OBLI", 67)}),
]

# 92 Segments
zones_sylv_regions: List[Rule] = [
    Rule("Menu"),
    Rule("Sylv 15", {Req("SYLV", 14)}),
]

# 75 Segments
zones_caul_regions: List[Rule] = [
    Rule("Menu"),
    Rule("Caul 10", {Req("CAUL", 8)}),
    Rule("Caul 50", {Req("CAUL", 38)}),
    Rule("Caul 65", {Req("CAUL", 49)}),
]

zones_regions: List[Rule] = [
    *zones_mira_regions,
    *zones_prim_regions,
    *zones_noct_regions,
    *zones_obli_regions,
    *zones_sylv_regions,
    *zones_caul_regions
]

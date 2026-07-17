from typing import List
from ..Regions import Requirement as Req, Rule

# flake8: noqa
chapter_regions: List[Rule] = [
Rule("Menu"),
Rule("Chapter 0", {Req("LVL", 4)}),
Rule("Chapter 1"),
Rule("Chapter 2", {Req("LVL", 5)}),
Rule("Chapter 3", {Req("LVL", 10)}),
Rule("Chapter 4", {Req("KEY: Blade License"), Req("DP: Mining Probe G1", 3), Req("DP: Research Probe G1"), Req("KEY: FNet"), Req("PRIM", 14), Req("LVL", 16)}),
Rule("Chapter 5", {Req("LVL", 20)}),
Rule("Chapter 6", {Req("NOCT", 16), Req("LVL", 24)}),
Rule("Chapter 7", {Req("OBLI", 24), Req("LVL", 28)}),
Rule("Chapter 8", {Req("FRD: Lao"), Req("MIRA", 70), Req("LVL", 31)}),
Rule("Chapter 9", {Req("LVL", 34)}),
Rule("Chapter 10", {Req("SYLV", 14), Req("LVL", 39)}),
Rule("Chapter 11", {Req("FRD: Gwin"), Req("CAUL", 8), Req("WPN: Soldier Assault Rifle_1"), Req("LVL", 45)}),
Rule("Chapter 12", {Req("KEY: Skell License"), Req("SKF"), Req("LVL", 50)}), # TAJ Talon Rock
]

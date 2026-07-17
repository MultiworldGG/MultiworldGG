from ..Regions import Requirement as Req, Rule

# flake8: noqa
# Probe-fessional
quest_probe_fessional_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest Probe-fessional", {Req("DP: Mining Probe G1", 3), Req("DP: Research Probe G1"), Req("KEY: FNet")}),
]

# The Skell License
quest_skell_license_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest Skell License", {Req("WPN: Trial Knife")}), # could be trial assault rifle or trial sword as well, but 1 is enough
]

# Weaponized
quest_weaponized_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest Weaponized", {Req("WPN: Ramjet Rifle_1")}),
]

# Weaponized
quest_thats_incredible_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest Thats Incredible", {Req("WPN: Hyde Dyads"), Req("WPN: Diagonal Twins")}),
]

# Scrap Duo
quest_little_rich_girl_regions: list[Rule] = [
Rule("Menu"),
Rule("Quest The Little Rich Girl", {Req("WPN: Scrap Duo")}),
]

quest_regions: list[Rule] = [
    *quest_probe_fessional_regions,
    *quest_skell_license_regions,
    *quest_weaponized_regions,
    *quest_thats_incredible_regions,
    *quest_little_rich_girl_regions,
]

from enum import IntEnum
from typing import Optional, NamedTuple, Dict
from dataclasses import dataclass

from rule_builder.rules import Rule, True_, Has, HasAll, HasAny, OptionFilter, And, HasGroup, CanReachRegion, Or
from .Options import FogwallSanity, BossFogwallSanity, CanWarpWithoutLordvessel, LogicToAccessCatacombs, LogicToAccessTotG, LogicToAccessFirelinkAltar

@dataclass
class DsrEntranceRule():
    source: str
    rule: Rule

@dataclass
class DsrLocationRule():
    loc_name: str
    rule: Rule

# can_teleport = Has("Lordvessel" options=[OptionFilter(CanWarpWithoutLordvessel, CanWarpWithoutLordvessel.option_true)], filtered_resolution=True)

bossfogwall_sanity_off = [OptionFilter(BossFogwallSanity, BossFogwallSanity.option_false)]
fogwall_sanity_off = [OptionFilter(FogwallSanity, FogwallSanity.option_false)]

bossfogwall_sanity_on = [OptionFilter(BossFogwallSanity, BossFogwallSanity.option_true)]
fogwall_sanity_on = [OptionFilter(FogwallSanity, FogwallSanity.option_true)]

# Special location rules
location_rules_table = [
  DsrLocationRule("UP: Bell of Awakening #1 rung", Has("Bell Gargoyles Defeated")),
  DsrLocationRule("NL: Key to the Seal", Has("Lordvessel")),
  DsrLocationRule("FA: Lordvessel Placed", Has("Lordvessel")),
  # DLC access
  DsrLocationRule("DA: Broken Pendant", Has("Princess Dusk Rescued")),
  # Demon ruins checks that require the lava-walking ring
  DsrLocationRule("DR: Large Soul of a Proud Knight - First Jump over the Lava", Has("Orange Charred Ring")),
  DsrLocationRule("DR: Chaos Flame Ember", Has("Orange Charred Ring")),
  # Fogs that do not affect region accessibility
  DsrLocationRule("DE: Fog Wall - Depths Rat Room", Has("Fog Wall Key - Depths Rat Room") | fogwall_sanity_off),
  DsrLocationRule("TC: Fog Wall - Catacombs", Has("Fog Wall Key - Catacombs") | fogwall_sanity_off),
  DsrLocationRule("NL: Fog Wall - New Londo (Lower)", Has("Fog Wall Key - New Londo (Lower)") | fogwall_sanity_off),
]

# All region rules
region_rules_table: dict[str, list[DsrEntranceRule]] = {
  "Undead Asylum Cell": [
    DsrEntranceRule("Menu", True_())
  ],
  "Undead Asylum Cell Door": [
    DsrEntranceRule("Undead Asylum Cell", True_()), # Has("Dungeon Cell Key")), => Always true
  ],
  "Northern Undead Asylum": [
    DsrEntranceRule("Undead Asylum Cell Door", True_()),
  ],
  "Northern Undead Asylum - After Fog": [
    DsrEntranceRule("Northern Undead Asylum", True_()),
  ],
  "Northern Undead Asylum - F2 East Door": [
    DsrEntranceRule("Northern Undead Asylum - After Fog", True_()), # Has("Undead Asylum F2 East Key")), => Always true
  ],
  "Northern Undead Asylum - After F2 East Door": [
    DsrEntranceRule("Northern Undead Asylum - F2 East Door", True_()),
  ],
  "Northern Undead Asylum - Big Pilgrim Door": [
    DsrEntranceRule("Northern Undead Asylum - After F2 East Door", True_()), # Has("Big Pilgrim's Key")), => Always true
  ],
  "Firelink Shrine": [
    DsrEntranceRule("Northern Undead Asylum - Big Pilgrim Door", True_()),
    DsrEntranceRule("The Catacombs", True_()),
    DsrEntranceRule("Upper Undead Burg - Before Fog", True_()),
    DsrEntranceRule("Upper New Londo Ruins", True_()),
    DsrEntranceRule("Firelink Shrine - After Undead Parish Elevator", True_()),
  ],

  "Firelink Shrine - Trusty Patches": [
    DsrEntranceRule("Firelink Shrine", Has("Gravelord Nito Defeated")), # vanilla
  ],
  "Firelink Shrine - Griggs of Vinheim": [
    DsrEntranceRule("Firelink Shrine", CanReachRegion("Lower Undead Burg - After Residence Key")), # vanilla
  ],
  "Firelink Shrine - Griggs of Vinheim, After Logan Leaves": [
    DsrEntranceRule("Firelink Shrine - Griggs of Vinheim", 
      CanReachRegion("Sen's Fortress - After Cage Key") & CanReachRegion("The Duke's Archives - Out of Cell")), # Can rescue Logan, and easily get him to leave Firelink
  ],
  "Firelink Shrine - Laurentius of the Great Swamp": [
    DsrEntranceRule("Firelink Shrine", CanReachRegion("Depths")), # vanilla
  ],
  "Firelink Shrine - Petrus of Thorolund": [
    DsrEntranceRule("Firelink Shrine", True_()), # vanilla
  ],
  "Firelink Shrine - Rhea of Thorolund": [ # need more info about her shop inventory and when each part becomes available
    DsrEntranceRule("Firelink Shrine", CanReachRegion("Tomb of the Giants")), # vanilla tomb rescue spot
  ],
  "Upper Undead Burg - Before Fog": [
    DsrEntranceRule("Firelink Shrine", True_()),
    DsrEntranceRule("Upper Undead Burg - Fog", True_()),
  ],
  "Upper Undead Burg - Fog": [
    DsrEntranceRule("Upper Undead Burg - Before Fog", Has("Fog Wall Key - Undead Burg") | fogwall_sanity_off),
    DsrEntranceRule("Upper Undead Burg", Has("Fog Wall Key - Undead Burg") | fogwall_sanity_off),
  ],
  "Upper Undead Burg": [
    DsrEntranceRule("Upper Undead Burg - Fog", True_()),
    DsrEntranceRule("Upper Undead Burg - Hellkite Bridge", True_()), # bonfire ladder
    DsrEntranceRule("Lower Undead Burg", True_()),
    DsrEntranceRule("Watchtower Basement", True_()),
  ],
  "Upper Undead Burg - Male Undead Merchant": [
    DsrEntranceRule("Upper Undead Burg", True_()), # vanilla
  ],
  "Upper Undead Burg - Pine Resin Chest": [
    DsrEntranceRule("Upper Undead Burg", HasAny("Residence Key", "Master Key")),
  ],
  "Upper Undead Burg - Taurus Demon": [
    DsrEntranceRule("Upper Undead Burg", Has("Boss Fog Wall Key - Taurus Demon") | bossfogwall_sanity_off),
  ],
  "Upper Undead Burg - Hellkite Bridge": [
    DsrEntranceRule("Upper Undead Burg - Taurus Demon", True_()), # Has("Taurus Demon Defeated")), => Always true
    DsrEntranceRule("Undead Parish - Before Fog", True_()),
    # DsrEntranceRule("Undead Burg Basement Door", True_()),
  ],
  "Undead Parish - Before Fog": [
    DsrEntranceRule("Upper Undead Burg - Hellkite Bridge", True_()),
    DsrEntranceRule("Undead Parish - Fog", True_()),
    DsrEntranceRule("Undead Parish", True_()), # Lever->Gate, or drop near fog
  ],
  "Undead Parish - Fog": [
    DsrEntranceRule("Undead Parish - Before Fog", Has("Fog Wall Key - Undead Parish") | fogwall_sanity_off),
    DsrEntranceRule("Undead Parish", Has("Fog Wall Key - Undead Parish") | fogwall_sanity_off),
  ],
  "Undead Parish": [
    DsrEntranceRule("Undead Parish - Fog", True_()),
    DsrEntranceRule("Darkroot Garden - Before Fog", True_()),
  ],
  "Undead Parish - Andre of Astora": [
    DsrEntranceRule("Undead Parish", True_()),
  ],
  "Undead Parish - Bell Gargoyles": [
    DsrEntranceRule("Undead Parish", Has("Boss Fog Wall Key - Bell Gargoyles") | bossfogwall_sanity_off),
  ],
  "Undead Parish - Oswald of Carim": [
    DsrEntranceRule("Undead Parish - Bell Gargoyles", True_()),
  ],
  "Firelink Shrine - After Undead Parish Elevator": [
    DsrEntranceRule("Undead Parish", True_()),
  ],
  "Northern Undead Asylum Second Visit": [
    DsrEntranceRule("Firelink Shrine - After Undead Parish Elevator", True_()),
  ],
  "Northern Undead Asylum Second Visit - F2 West Door": [
    DsrEntranceRule("Northern Undead Asylum Second Visit", Has("Undead Asylum F2 West Key")),
  ],
  "Northern Undead Asylum Second Visit - Behind F2 West Door": [
    DsrEntranceRule("Northern Undead Asylum Second Visit - F2 West Door", True_()),
  ],
  # "Northern Undead Asylum Second Visit - Snuggly Trades": [ # none yet
  # ],
  "Undead Burg Basement Door": [
    DsrEntranceRule("Upper Undead Burg - Hellkite Bridge", Has("Basement Key")),
    # DsrEntranceRule("Lower Undead Burg", Has("Basement Key")),
  ],
  "Lower Undead Burg": [
    DsrEntranceRule("Undead Burg Basement Door", True_()),
  ],
  "Lower Undead Burg - After Residence Key": [
    DsrEntranceRule("Lower Undead Burg", Has("Residence Key")),
  ],
  "Lower Undead Burg - Capra Demon": [
    DsrEntranceRule("Lower Undead Burg", Has("Boss Fog Wall Key - Capra Demon") | bossfogwall_sanity_off),
  ],
  "Lower Undead Burg - After Capra Demon": [
    DsrEntranceRule("Lower Undead Burg - Capra Demon", True_()), # Has("Capra Demon Defeated")),
  ],
  "Lower Undead Burg - Female Undead Merchant": [
    DsrEntranceRule("Lower Undead Burg", True_()),
  ],
  "Watchtower Basement": [
    DsrEntranceRule("Upper Undead Burg", HasAny("Watchtower Basement Key", "Master Key")),
    DsrEntranceRule("Darkroot Basin", HasAny("Watchtower Basement Key", "Master Key")),
  ],
  "Depths": [
    DsrEntranceRule("Lower Undead Burg", Has("Key to Depths")),
  ],
  # "Depths - After Sewer Chamber Key": [
  #   DsrEntranceRule("Depths", Has("Sewer Chamber Key")), # temporarily ignored - no checks here
  # ],
  "Depths - Gaping Dragon": [
    DsrEntranceRule("Depths", Has("Boss Fog Wall Key - Gaping Dragon") | bossfogwall_sanity_off),
  ],
  "Depths - After Gaping Dragon": [
    DsrEntranceRule("Depths - Gaping Dragon", True_()), # Has("Gaping Dragon Defeated")),
  ],
  "Firelink Shrine - Domhnall of Zena": [
    DsrEntranceRule("Firelink Shrine", CanReachRegion("Depths") & HasAll("Bell of Awakening #1", "Bell of Awakening #2")), # vanilla, but his inventory is more complicated due to flags
  ],
  # "Firelink Shrine - Domhnall of Zena - Post Iron Golem": [
  #   DsrEntranceRule("Firelink Shrine - Domhnall of Zena", Has("Iron Golem Defeated")), 
  # ],
  # "Firelink Shrine - Domhnall of Zena - Post O+S": [
  #   DsrEntranceRule("Firelink Shrine - Domhnall of Zena", Has("Ornstein and Smough Defeated")), #vanilla, but his inventory is more complicated due to flags
  # ],
  # "Firelink Shrine - Domhnall of Zena - Post Gwyndolin": [
  #   DsrEntranceRule("Firelink Shrine - Domhnall of Zena", Has("Gwyndolin Defeated")), #vanilla, but his inventory is more complicated due to flags
  # ],
  # "Firelink Shrine - Domhnall of Zena - Post Artorias": [
  #   DsrEntranceRule("Firelink Shrine - Domhnall of Zena", Has("Artorias the Abysswalker Defeated")), #vanilla, but his inventory is more complicated due to flags
  # ],
  "Depths to Blighttown Door": [
    DsrEntranceRule("Depths", Has("Blighttown Key")),
  ],
  "Upper Blighttown Depths Side": [
    DsrEntranceRule("Depths to Blighttown Door", True_()),
    DsrEntranceRule("Lower Blighttown - Fog", True_()),
  ],
  "Upper Blighttown VotD Side": [
    DsrEntranceRule("Valley of the Drakes", True_()),
    DsrEntranceRule("Lower Blighttown", True_()),
  ],
  "Lower Blighttown - Fog": [
    DsrEntranceRule("Lower Blighttown", Has("Fog Wall Key - Lower Blighttown Entrance") | fogwall_sanity_off),
    DsrEntranceRule("Upper Blighttown Depths Side", Has("Fog Wall Key - Lower Blighttown Entrance") | fogwall_sanity_off),
  ],
  "Lower Blighttown": [
    DsrEntranceRule("Upper Blighttown VotD Side", True_()),
    DsrEntranceRule("Lower Blighttown - Fog", True_()),
    # Don't expect player to jump down past fog if they can't teleport
    DsrEntranceRule("Upper Blighttown Depths Side", Has("Lordvessel", options=[OptionFilter(CanWarpWithoutLordvessel, CanWarpWithoutLordvessel.option_false)], filtered_resolution=True)),
  ],
  "Lower Blighttown - Shiva of the East": [
    DsrEntranceRule("Lower Blighttown", CanReachRegion("Darkroot Garden - Behind Artorias Door")),
  ],
  "Lower Blighttown - Quelana of Izalith": [
    DsrEntranceRule("Lower Blighttown", CanReachRegion("Firelink Shrine - Laurentius of the Great Swamp")), # normal way to reach; could also reach via Eingyi
  ],
  "Lower Blighttown - Quelaag": [
    DsrEntranceRule("Lower Blighttown", Has("Boss Fog Wall Key - Quelaag") | bossfogwall_sanity_off),
  ],
  "Lower Blighttown - After Quelaag": [
    DsrEntranceRule("Lower Blighttown - Quelaag", True_()), # Has("Chaos Witch Quelaag Defeated")),
    DsrEntranceRule("Demon Ruins - Early", True_()),
  ],
  "Lower Blighttown - Eingyi": [
    DsrEntranceRule("Lower Blighttown - After Quelaag",  True_()),
  ],
  "Valley of the Drakes": [
    DsrEntranceRule("Upper Blighttown VotD Side", True_()),
    DsrEntranceRule("Lower New Londo Ruins", True_()), # flood gates opened
    DsrEntranceRule("Darkroot Basin", True_()),
    DsrEntranceRule("Door between Upper New Londo and Valley of the Drakes", True_()),
  ],
  "Valley of the Drakes - After Defeating Four Kings": [
    DsrEntranceRule("Valley of the Drakes", CanReachRegion("The Abyss - After Four Kings")),
  ],
  "Door between Upper New Londo and Valley of the Drakes": [
    DsrEntranceRule("Upper New Londo Ruins", HasAny("Key to New Londo Ruins", "Master Key")),
    DsrEntranceRule("Valley of the Drakes", HasAny("Key to New Londo Ruins", "Master Key")),
  ],
  "Darkroot Basin": [
    DsrEntranceRule("Darkroot Garden - Before Fog", True_()),
    DsrEntranceRule("Valley of the Drakes", True_()),
    DsrEntranceRule("Watchtower Basement", True_()),
  ],
  "Darkroot Basin - Princess Dusk": [
    DsrEntranceRule("Darkroot Basin", Has("Princess Dusk Rescued")),
    DsrEntranceRule("Oolacile Sanctuary - Elizabeth", True_()),
  ],
  "Darkroot Garden - Before Fog": [
    DsrEntranceRule("Darkroot Basin", True_()),
    DsrEntranceRule("Undead Parish", True_()),
  ],
  "Darkroot Garden": [
    DsrEntranceRule("Darkroot Garden - Before Fog", Has("Fog Wall Key - Darkroot Garden") | fogwall_sanity_off),
  ],
  "Darkroot Garden - Behind Artorias Door": [
    DsrEntranceRule("Darkroot Garden - Before Fog", Has("Crest of Artorias")),
  ],
  "Darkroot Garden - Moonlight Butterfly": [
    DsrEntranceRule("Darkroot Garden", Has("Boss Fog Wall Key - Moonlight Butterfly") | bossfogwall_sanity_off),
  ],
  "Darkroot Garden - After Moonlight Butterfly": [
    DsrEntranceRule("Darkroot Garden - Moonlight Butterfly", True_()), # Has("Moonlight Butterfly Defeated")),
  ],
  "The Great Hollow": [
    DsrEntranceRule("Lower Blighttown", Has("Lordvessel") | fogwall_sanity_on | bossfogwall_sanity_on), # Add slight logic for the no-fog-sanity people,
  ],
  "Ash Lake": [
    DsrEntranceRule("The Great Hollow", Has("Fog Wall Key - Ash Lake Entrance") | fogwall_sanity_off),
  ],
  "Sen's Fortress": [
    DsrEntranceRule("Undead Parish", HasAll("Bell of Awakening #1", "Bell of Awakening #2")),
  ],
  "Sen's Fortress - After First Fog": [
    DsrEntranceRule("Sen's Fortress", Has("Fog Wall Key - Sen's Fortress #1 (Outside Stairs)") | fogwall_sanity_off),
  ],
  "Sen's Fortress - After Second Fog": [
    DsrEntranceRule("Sen's Fortress - After First Fog", Has("Fog Wall Key - Sen's Fortress #2 (Upper Entrance)") | fogwall_sanity_off),
  ],
  "Sen's Fortress - Crestfallen Merchant": [
    DsrEntranceRule("Sen's Fortress - After Second Fog", True_()),
  ],
  "Sen's Fortress - After Cage Key": [
    DsrEntranceRule("Sen's Fortress - After First Fog", HasAny("Cage Key", "Master Key")),
  ],
  "Sen's Fortress - Iron Golem": [
    DsrEntranceRule("Sen's Fortress - After Second Fog", Has("Boss Fog Wall Key - Iron Golem") | bossfogwall_sanity_off),
  ],
  "Sen's Fortress - After Iron Golem": [
    DsrEntranceRule("Sen's Fortress - Iron Golem", True_()), # Has("Iron Golem Defeated")),
  ],
  "Anor Londo": [
    DsrEntranceRule("Sen's Fortress - After Iron Golem", True_()),
  ],
  "Anor Londo - After First Fog": [
    DsrEntranceRule("Anor Londo", Has("Fog Wall Key - Anor Londo #1 (Rafters)") | fogwall_sanity_off),
  ],  
  "Anor Londo - Painting Room": [
    DsrEntranceRule("Anor Londo - After First Fog", True_()),
  ],
  "Anor Londo - After Second Fog": [
    DsrEntranceRule("Anor Londo - After First Fog", Has("Fog Wall Key - Anor Londo #2 (Archers)") | fogwall_sanity_off),
  ],
  "Anor Londo - Ornstein and Smough": [
    DsrEntranceRule("Anor Londo - After Second Fog", Has("Boss Fog Wall Key - Ornstein and Smough") | bossfogwall_sanity_off),
  ],
  "Anor Londo - Giant Blacksmith": [
    DsrEntranceRule("Anor Londo - After Second Fog", True_()),
  ],
  "Anor Londo - After Ornstein and Smough": [
    DsrEntranceRule("Anor Londo - Ornstein and Smough", True_()), # Has("Ornstein and Smough Defeated")),
  ],
  "Anor Londo - Gwyndolin": [
    # attacking the illusion -> no ring needed
    DsrEntranceRule("Anor Londo - After Ornstein and Smough", Has("Boss Fog Wall Key - Gwyndolin") | bossfogwall_sanity_off), 
  ],
  "Anor Londo - After Gwyndolin": [
    DsrEntranceRule("Anor Londo - Gwyndolin", True_()), # Has("Gwyndolin Defeated")),
  ],
  "Painted World of Ariamis": [
    DsrEntranceRule("Anor Londo - Painting Room", Has("Peculiar Doll")),
  ],
  "Painted World of Ariamis - After Fog": [
    DsrEntranceRule("Painted World of Ariamis", Has("Fog Wall Key - Painted World") | fogwall_sanity_off),
  ],
  "Painted World of Ariamis - After Annex Key": [
    DsrEntranceRule("Painted World of Ariamis - After Fog", Has("Annex Key")),
  ],
  "Painted World of Ariamis - Crossbreed Priscilla": [
    DsrEntranceRule("Painted World of Ariamis - After Fog", Has("Boss Fog Wall Key - Crossbreed Priscilla") | bossfogwall_sanity_off),
  ],
  "Upper New Londo Ruins": [
    DsrEntranceRule("Firelink Shrine", True_()),
    DsrEntranceRule("Door between Upper New Londo and Valley of the Drakes", True_()),
  ],
  "Upper New Londo Ruins - Rickert of Vinheim": [
    DsrEntranceRule("Upper New Londo Ruins", True_()),
  ],
  "Upper New Londo Ruins - After Fog": [
    DsrEntranceRule("Upper New Londo Ruins", Has("Fog Wall Key - New Londo (Upper)") | fogwall_sanity_off),
  ],
  "Upper New Londo Ruins - Ingward": [
    DsrEntranceRule("Upper New Londo Ruins - After Fog", True_()),
  ],
  "New Londo Ruins Door to the Seal": [
    DsrEntranceRule("Upper New Londo Ruins - After Fog", Has("Key to the Seal") 
      & (CanReachRegion("Anor Londo - After Ornstein and Smough") | fogwall_sanity_on | bossfogwall_sanity_on)), # Add slight logic for the no-fog-sanity people
  ],
  "Lower New Londo Ruins": [
    DsrEntranceRule("New Londo Ruins Door to the Seal", True_()),
  ],
  "The Abyss": [
    DsrEntranceRule("Lower New Londo Ruins", Has("Covenant of Artorias") & (Has("Boss Fog Wall Key - Four Kings") | bossfogwall_sanity_off)),
  ],
  "The Abyss - After Four Kings": [
    DsrEntranceRule("The Abyss", True_()), # Has("Four Kings Defeated")),
  ],
  "The Duke's Archives": [
    DsrEntranceRule("Anor Londo", Has("Lordvessel Placed")),
  ],
  "The Duke's Archives - After First Seath Encounter": [
    DsrEntranceRule("The Duke's Archives", Has("Boss Fog Wall Key - Seath First Encounter") | bossfogwall_sanity_off),
  ],
  "The Duke's Archives - After Archive Tower Cell Key": [
    DsrEntranceRule("The Duke's Archives - After First Seath Encounter", Has("Archive Tower Cell Key")),
  ],
  "The Duke's Archives - After Archive Prison Extra Key": [
    DsrEntranceRule("The Duke's Archives - After First Seath Encounter", Has("Archive Prison Extra Key")),
  ],
  "The Duke's Archives - Out of Cell": [
    DsrEntranceRule("The Duke's Archives - After Archive Prison Extra Key", True_()),
    DsrEntranceRule("The Duke's Archives - After Archive Tower Cell Key", True_()),
  ],
  "The Duke's Archives - After Archive Tower Giant Door Key": [
    DsrEntranceRule("The Duke's Archives - Out of Cell", Has("Archive Tower Giant Door Key")),
  ],
  "The Duke's Archives - Courtyard": [
    DsrEntranceRule("The Duke's Archives - After Archive Tower Giant Door Key", Has("Fog Wall Key - Duke's Archives Courtyard Entrance") | fogwall_sanity_off),
  ],
  "The Duke's Archives - Giant Cell": [
    DsrEntranceRule("The Duke's Archives - Out of Cell", Has("Archive Tower Giant Cell Key")),
  ],
  "Crystal Cave": [
    DsrEntranceRule("The Duke's Archives - Courtyard", True_()),
  ],
  "Crystal Cave - After Seath": [
    DsrEntranceRule("Crystal Cave", True_()), # Has("Seath the Scaleless Defeated")),
  ],
  "The Duke's Archives - First Arena after Seath's Death": [
    DsrEntranceRule("The Duke's Archives", CanReachRegion("Crystal Cave - After Seath")),
  ],
  "The Duke's Archives - Big Hat Logan": [ # Logan in book room = when he is guaranteed
    DsrEntranceRule("The Duke's Archives - After Archive Tower Giant Door Key",
     CanReachRegion("Sen's Fortress - After Cage Key") & CanReachRegion("The Duke's Archives - Giant Cell") & CanReachRegion("Crystal Cave - After Seath"))
  ],
  "Demon Ruins - Early": [
    DsrEntranceRule("Lower Blighttown - After Quelaag", True_()),
  ],
  "Demon Ruins - Ceaseless Discharge": [
    DsrEntranceRule("Demon Ruins - Early", Has("Boss Fog Wall Key - Ceaseless Discharge") | bossfogwall_sanity_off),
  ],
  "Demon Ruins": [
    DsrEntranceRule("Demon Ruins - Early", CanReachRegion("Demon Ruins - Ceaseless Discharge")), # Has("Ceaseless Discharge Defeated")),
  ],
  "Demon Ruins - Demon Firesage": [
    DsrEntranceRule("Demon Ruins", Has("Lordvessel Placed") & (Has("Boss Fog Wall Key - Demon Firesage") | bossfogwall_sanity_off)),
  ],
  "Demon Ruins - After Demon Firesage": [
    DsrEntranceRule("Demon Ruins - Demon Firesage", True_()), # Has("Demon Firesage Defeated")),
  ],
  "Demon Ruins - Centipede Demon": [
    DsrEntranceRule("Demon Ruins - After Demon Firesage", Has("Boss Fog Wall Key - Centipede Demon") | bossfogwall_sanity_off),
  ],
  "Demon Ruins Shortcut": [
    DsrEntranceRule("Lost Izalith", True_()), # opens from the back for free
  ],
  "Lost Izalith": [
    DsrEntranceRule("Demon Ruins - Centipede Demon", Has("Orange Charred Ring")),
  ],
  "Lost Izalith - Bed of Chaos": [
    DsrEntranceRule("Lost Izalith", Has("Boss Fog Wall Key - Bed of Chaos") | bossfogwall_sanity_off),
  ],
  "The Catacombs": [
    # Firelink access is either immediate (if option = "no logic"), or has one of the requirements below
    DsrEntranceRule("Firelink Shrine", 
        Has("Male Undead Merchant Access", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_undead_merchant)], filtered_resolution=True)
      & Has("Andre of Astora Access", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_andre)], filtered_resolution=True)
      & HasAny("Andre of Astora Access", "Male Undead Merchant Access", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_andre_or_undead_merchant)], filtered_resolution=True)
      & CanReachRegion("Anor Londo - After Ornstein and Smough", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_ornstein_and_smough)], filtered_resolution=True)
      )
  ],
  "The Catacombs - Door 1": [
    DsrEntranceRule("The Catacombs", True_()),
  ],
  "The Catacombs - After Door 1": [
    DsrEntranceRule("The Catacombs - Door 1", True_()),
  ],
  "The Catacombs - Vamos": [
    DsrEntranceRule("The Catacombs - After Door 1", True_()),
  ],
  "The Catacombs - Pinwheel": [
    DsrEntranceRule("The Catacombs - After Door 1", Has("Boss Fog Wall Key - Pinwheel") | bossfogwall_sanity_off),
  ],
  "The Catacombs - After Pinwheel": [
    DsrEntranceRule("The Catacombs - Pinwheel", True_()), # Has("Pinwheel Defeated")),
  ],
  "Tomb of the Giants": [
    DsrEntranceRule("The Catacombs - After Pinwheel",
      Has("Skull Lantern", options=[OptionFilter(LogicToAccessTotG, LogicToAccessTotG.option_skull_lantern)], filtered_resolution=True) &
      Has("Sunlight Maggot", options=[OptionFilter(LogicToAccessTotG, LogicToAccessTotG.option_sunlight_maggot)], filtered_resolution=True)
    )
  ],
  "Tomb of the Giants - After White Fog": [
    DsrEntranceRule("Tomb of the Giants", Has("Fog Wall Key - Tomb of the Giants") | fogwall_sanity_off),
  ],
  "Tomb of the Giants - Behind Golden Fog Wall": [
    DsrEntranceRule("Tomb of the Giants - After White Fog", Has("Lordvessel Placed")),
  ],
  "Tomb of the Giants - Nito": [
    DsrEntranceRule("Tomb of the Giants - Behind Golden Fog Wall", Has("Boss Fog Wall Key - Nito") | bossfogwall_sanity_off),
  ],
  "Tomb of the Giants - After Nito": [
    DsrEntranceRule("Tomb of the Giants - Nito", True_()), # Has("Gravelord Nito Defeated")),
  ],
  "Firelink Altar": [
    # Access via kaathe if it's "kaathe" or "either_serpent"
    DsrEntranceRule("The Abyss - After Four Kings", True_(options=[OptionFilter(LogicToAccessFirelinkAltar, [LogicToAccessFirelinkAltar.option_kaathe, LogicToAccessFirelinkAltar.option_either_serpent], operator="in")])),
    # Access via frampt if it's "frampt", or "either_serpent", or ["both_serpents" and also has kaathe access]
    DsrEntranceRule("Firelink Shrine", HasAll("Bell of Awakening #1", "Bell of Awakening #2") & (
      CanReachRegion("The Abyss - After Four Kings",options=[OptionFilter(LogicToAccessFirelinkAltar, LogicToAccessFirelinkAltar.option_both_serpents)]) |
      True_(options=[OptionFilter(LogicToAccessFirelinkAltar, [LogicToAccessFirelinkAltar.option_frampt, LogicToAccessFirelinkAltar.option_either_serpent], operator="in")])
      )),
  ],
  "Kiln of the First Flame": [
    DsrEntranceRule("Firelink Altar", HasAll("Lord Soul (Bed of Chaos)", "Lord Soul (Nito)", "Bequeathed Lord Soul Shard (Four Kings)", "Bequeathed Lord Soul Shard (Seath)", "Lordvessel")),
  ],
  "Kiln of the First Flame - Gwyn": [
    DsrEntranceRule("Kiln of the First Flame", Has("Boss Fog Wall Key - Gwyn") | bossfogwall_sanity_off),
  ],
  "Sanctuary Garden": [
    DsrEntranceRule("Darkroot Basin", Has("Broken Pendant")),
  ],
  "Sanctuary Garden - Sanctuary Guardian": [
    DsrEntranceRule("Sanctuary Garden", Has("Boss Fog Wall Key - Sanctuary Guardian") | bossfogwall_sanity_off),
  ],
  "Oolacile Sanctuary": [
    DsrEntranceRule("Sanctuary Garden - Sanctuary Guardian", True_()), # Has("Sanctuary Guardian Defeated")),
  ],
  "Oolacile Sanctuary - Elizabeth": [
    DsrEntranceRule("Oolacile Sanctuary", True_()),
  ],
  "Royal Wood": [
    DsrEntranceRule("Oolacile Sanctuary", True_()),
  ],
  "Royal Wood - Marvelous Chester": [
    DsrEntranceRule("Royal Wood", True_()),
  ],
  "Royal Wood - Artorias": [
    DsrEntranceRule("Royal Wood", Has("Boss Fog Wall Key - Artorias") | bossfogwall_sanity_off),
  ],
  "Royal Wood - Hawkeye Gough": [
    DsrEntranceRule("Oolacile Township", Has("Crest Key")),
  ],
  "Royal Wood - After Hawkeye Gough": [
    DsrEntranceRule("Royal Wood - Hawkeye Gough", True_()), # depends on being able to reach kalameet arena, technically, but until fog rando that will always be in logic
  ],
  "Oolacile Township": [
    DsrEntranceRule("Royal Wood - Artorias", True_()), # Has("Artorias the Abysswalker Defeated")),
    DsrEntranceRule("Chasm of the Abyss", True_()),
  ],
  "Oolacile Township - Behind Light-Dispelled Walls": [
    DsrEntranceRule("Oolacile Township", HasAny("Skull Lantern", "Sunlight Maggot")),
  ],
  "Chasm of the Abyss": [
    DsrEntranceRule("Oolacile Township", True_()),
  ],
  "Chasm of the Abyss - Manus": [
    DsrEntranceRule("Chasm of the Abyss", Has("Boss Fog Wall Key - Manus") | bossfogwall_sanity_off),
  ],
  "2 Merchants - Bottomless Box": [
    DsrEntranceRule("Upper Undead Burg - Male Undead Merchant", True_()),
    DsrEntranceRule("Firelink Shrine - Domhnall of Zena", True_()),
  ],
  "4 Merchants - Repairbox": [
    DsrEntranceRule("Anor Londo - Giant Blacksmith", True_()),
    DsrEntranceRule("Upper Undead Burg - Male Undead Merchant", True_()),
    DsrEntranceRule("Undead Parish - Andre of Astora", True_()),
    DsrEntranceRule("The Catacombs - Vamos", True_()),
  ],
  "3 Blacksmiths - Smithboxen": [
    DsrEntranceRule("Anor Londo - Giant Blacksmith", True_()),
    DsrEntranceRule("Undead Parish - Andre of Astora", True_()),
    DsrEntranceRule("The Catacombs - Vamos", True_()),
  ],
}

from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from rule_builder.rules import Rule, True_, Has, HasAll, HasAny, OptionFilter
from .Options import FogwallSanity, BossFogwallSanity, CanWarpWithoutLordvessel, LogicToAccessCatacombs

class DsrEntranceRule(NamedTuple):
    source: str
    rule: Rule
class DsrLocationRule(NamedTuple):
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
  DsrLocationRule("DA: Broken Pendant", Has("Dusk Rescued")),
  # Demon ruins checks that require the lava-walking ring
  DsrLocationRule("DR: Large Soul of a Proud Knight - First Jump over the Lava", Has("Orange Charred Ring")),
  DsrLocationRule("DR: Chaos Flame Ember", Has("Orange Charred Ring")),
  # Fogs that do not affect 
  DsrLocationRule("DE: Fog Wall - Depths Rat Room", Has("Fog Wall Key - Depths Rat Room") | fogwall_sanity_off),
  DsrLocationRule("TC: Fog Wall - Catacombs", Has("Fog Wall Key - Catacombs") | fogwall_sanity_off),
  DsrLocationRule("NL: Fog Wall - New Londo (Lower)", Has("Fog Wall Key - New Londo (Lower)") | fogwall_sanity_off),
]

# All region rules
region_rules_table = {
  "Undead Asylum Cell": [
    DsrEntranceRule("Menu", True_())
  ],
  "Undead Asylum Cell Door": [
    DsrEntranceRule("Undead Asylum Cell", Has("Dungeon Cell Key")),
  ],
  "Northern Undead Asylum": [
    DsrEntranceRule("Undead Asylum Cell Door", True_()),
  ],
  "Northern Undead Asylum - After Fog": [
    DsrEntranceRule("Northern Undead Asylum", True_()),
  ],
  "Northern Undead Asylum - F2 East Door": [
    DsrEntranceRule("Northern Undead Asylum - After Fog", Has("Undead Asylum F2 East Key")),
  ],
  "Northern Undead Asylum - After F2 East Door": [
    DsrEntranceRule("Northern Undead Asylum - F2 East Door", True_()),
  ],
  "Northern Undead Asylum - Big Pilgrim Door": [
    DsrEntranceRule("Northern Undead Asylum - After F2 East Door", Has("Big Pilgrim's Key")),
  ],
  "Firelink Shrine": [
    DsrEntranceRule("Northern Undead Asylum - Big Pilgrim Door", True_()),
    DsrEntranceRule("The Catacombs", True_()),
    DsrEntranceRule("Upper Undead Burg - Before Fog", True_()),
    DsrEntranceRule("Upper New Londo Ruins", True_()),
    DsrEntranceRule("Firelink Shrine - After Undead Parish Elevator", True_()),
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
  ],
  "Upper Undead Burg - Pine Resin Chest": [
    DsrEntranceRule("Upper Undead Burg", HasAny("Residence Key", "Master Key")),
  ],
  "Upper Undead Burg - Taurus Demon": [
    DsrEntranceRule("Upper Undead Burg", Has("Boss Fog Wall Key - Taurus Demon") | bossfogwall_sanity_off),
  ],
  "Upper Undead Burg - Hellkite Bridge": [
    DsrEntranceRule("Upper Undead Burg - Taurus Demon", Has("Taurus Demon Defeated")),
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
  "Undead Parish - Bell Gargoyles": [
    DsrEntranceRule("Undead Parish", Has("Boss Fog Wall Key - Bell Gargoyles") | bossfogwall_sanity_off),
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
  "Northern Undead Asylum Second Visit - Snuggly Trades": [ # none yet
  ],
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
    DsrEntranceRule("Lower Undead Burg - Capra Demon", Has("Capra Demon Defeated")),
  ],
  "Watchtower Basement": [
    DsrEntranceRule("Upper Undead Burg", HasAny("Watchtower Basement Key", "Master Key")),
    DsrEntranceRule("Darkroot Basin", HasAny("Watchtower Basement Key", "Master Key")),
  ],
  "Depths": [
    DsrEntranceRule("Lower Undead Burg", Has("Key to Depths")),
  ],
  "Depths - After Sewer Chamber Key": [
    DsrEntranceRule("Depths", Has("Sewer Chamber Key")),
  ],
  "Depths - Gaping Dragon": [
    DsrEntranceRule("Depths", Has("Boss Fog Wall Key - Gaping Dragon") | bossfogwall_sanity_off),
  ],
  "Depths - After Gaping Dragon": [
    DsrEntranceRule("Depths - Gaping Dragon", Has("Gaping Dragon Defeated")),
  ],
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
  "Lower Blighttown - Quelaag": [
    DsrEntranceRule("Lower Blighttown", Has("Boss Fog Wall Key - Quelaag") | bossfogwall_sanity_off),
  ],
  "Lower Blighttown - After Quelaag": [
    DsrEntranceRule("Lower Blighttown", Has("Chaos Witch Quelaag Defeated")),
  ],
  "Valley of the Drakes": [
    DsrEntranceRule("Upper Blighttown VotD Side", True_()),
    DsrEntranceRule("Lower New Londo Ruins", True_()),
    DsrEntranceRule("Darkroot Basin", True_()),
    DsrEntranceRule("Door between Upper New Londo and Valley of the Drakes", True_()),
  ],
  "Valley of the Drakes - After Defeating Four Kings": [
    DsrEntranceRule("Valley of the Drakes", Has("Four Kings Defeated")),
  ],
  "Door between Upper New Londo and Valley of the Drakes": [
    DsrEntranceRule("Upper New Londo Ruins", HasAny("Key to New Londo Ruins", "Master Key")),
    DsrEntranceRule("Valley of the Drakes", HasAny("Key to New Londo Ruins", "Master Key")),
  ],
  "Darkroot Basin": [
    DsrEntranceRule("Valley of the Drakes", True_()),
    DsrEntranceRule("Darkroot Garden - Before Fog", True_()),
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
    DsrEntranceRule("Darkroot Garden - Moonlight Butterfly", Has("Moonlight Butterfly Defeated")),
  ],
  "The Great Hollow": [
    DsrEntranceRule("Lower Blighttown", (Has("Lordvessel")| fogwall_sanity_on | bossfogwall_sanity_on)), # Add slight logic for the no-fog-sanity people,
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
  "Sen's Fortress - After Cage Key": [
    DsrEntranceRule("Sen's Fortress - After First Fog", HasAny("Cage Key", "Master Key")),
  ],
  "Sen's Fortress - Iron Golem": [
    DsrEntranceRule("Sen's Fortress - After Second Fog", Has("Boss Fog Wall Key - Iron Golem") | bossfogwall_sanity_off),
  ],
  "Sen's Fortress - After Iron Golem": [
    DsrEntranceRule("Sen's Fortress - Iron Golem", Has("Iron Golem Defeated")),
  ],
  "Anor Londo": [
    DsrEntranceRule("Sen's Fortress - After Iron Golem", True_()),
  ],
  "Anor Londo - After First Fog": [
    DsrEntranceRule("Anor Londo", Has("Fog Wall Key - Anor Londo #1 (Rafters)") | fogwall_sanity_off),
  ],
  "Anor Londo - After Second Fog": [
    DsrEntranceRule("Anor Londo - After First Fog", Has("Fog Wall Key - Anor Londo #2 (Archers)") | fogwall_sanity_off),
  ],
  "Anor Londo - Ornstein and Smough": [
    DsrEntranceRule("Anor Londo - After Second Fog", Has("Boss Fog Wall Key - Ornstein and Smough") | bossfogwall_sanity_off),
  ],
  "Anor Londo - After Ornstein and Smough": [
    DsrEntranceRule("Anor Londo - Ornstein and Smough", Has("Ornstein and Smough Defeated")),
  ],
  "Anor Londo - Gwyndolin": [
    # attacking the illusion -> no ring needed
    DsrEntranceRule("Anor Londo - After Ornstein and Smough", Has("Boss Fog Wall Key - Gwyndolin") | bossfogwall_sanity_off), 
  ],
  "Anor Londo - After Gwyndolin": [
    DsrEntranceRule("Anor Londo - Gwyndolin", Has("Gwyndolin Defeated")),
  ],
  "Painted World of Ariamis": [
    DsrEntranceRule("Anor Londo - After First Fog", Has("Peculiar Doll")),
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
  "Upper New Londo Ruins - After Fog": [
    DsrEntranceRule("Upper New Londo Ruins", Has("Fog Wall Key - New Londo (Upper)") | fogwall_sanity_off),
  ],
  "New Londo Ruins Door to the Seal": [
    DsrEntranceRule("Upper New Londo Ruins - After Fog", Has("Key to the Seal") 
      & (Has("Ornstein and Smough Defeated") | fogwall_sanity_on | bossfogwall_sanity_on)), # Add slight logic for the no-fog-sanity people
  ],
  "Lower New Londo Ruins": [
    DsrEntranceRule("New Londo Ruins Door to the Seal", True_()),
  ],
  "The Abyss": [
    DsrEntranceRule("Lower New Londo Ruins", (Has("Covenant of Artorias") & Has("Boss Fog Wall Key - Crossbreed Priscilla") | bossfogwall_sanity_off)),
  ],
  "The Abyss - After Four Kings": [
    DsrEntranceRule("The Abyss", Has("Four Kings Defeated")),
  ],
  "The Duke's Archives": [
    DsrEntranceRule("Anor Londo", Has("Lordvessel Placed")),
  ],
  "The Duke's Archives - After First Seath Encounter": [
    DsrEntranceRule("The Duke's Archives", Has("Boss Fog Wall Key - Seath First Encounter") | bossfogwall_sanity_off),
  ],
  "The Duke's Archives - After Archive Tower Cell Key": [
    DsrEntranceRule("The Duke's Archives", Has("Archive Tower Cell Key")),
  ],
  "The Duke's Archives - After Archive Prison Extra Key": [
    DsrEntranceRule("The Duke's Archives", Has("Archive Prison Extra Key")),
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
    DsrEntranceRule("Crystal Cave", Has("Seath the Scaleless Defeated")),
  ],
  "The Duke's Archives - First Arena after Seath's Death": [
    DsrEntranceRule("Crystal Cave", Has("Seath the Scaleless Defeated")),
  ],
  "Demon Ruins - Early": [
    DsrEntranceRule("Lower Blighttown - After Quelaag", True_()),
  ],
  "Demon Ruins - Ceaseless Discharge": [
    DsrEntranceRule("Demon Ruins - Early", Has("Boss Fog Wall Key - Ceaseless Discharge") | bossfogwall_sanity_off),
  ],
  "Demon Ruins": [
    DsrEntranceRule("Demon Ruins - Early", Has("Ceaseless Discharge Defeated")),
  ],
  "Demon Ruins - Demon Firesage": [
    DsrEntranceRule("Demon Ruins", Has("Lordvessel Placed") & Has("Boss Fog Wall Key - Ceaseless Discharge") | bossfogwall_sanity_off),
  ],
  "Demon Ruins - After Demon Firesage": [
    DsrEntranceRule("Demon Ruins - Demon Firesage", Has("Demon Firesage Defeated")),
  ],
  "Demon Ruins - Centipede Demon": [
    DsrEntranceRule("Demon Ruins - After Demon Firesage", Has("Boss Fog Wall Key - Centipede Demon") | bossfogwall_sanity_off),
  ],
  "Demon Ruins Shortcut": [
    DsrEntranceRule("Lost Izalith", True_()), # opens from the back for free
  ],
  "Lost Izalith": [
    DsrEntranceRule("Demon Ruins - Centipede Demon", HasAll("Orange Charred Ring", "Centipede Demon Defeated")),
  ],
  "Lost Izalith - Bed of Chaos": [
    DsrEntranceRule("Lost Izalith", Has("Boss Fog Wall Key - Bed of Chaos") | bossfogwall_sanity_off),
  ],
  "The Catacombs": [
    # Firelink access is either immediate (if option = "no logic"), or has one of the requirements below
    DsrEntranceRule("Firelink Shrine", 
        Has("Undead Merchant Access", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_undead_merchant)], filtered_resolution=True)
      & Has("Andre Access", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_andre)], filtered_resolution=True)
      & HasAny("Andre Access", "Undead Merchant Access", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_andre_or_undead_merchant)], filtered_resolution=True)
      & Has("Ornstein and Smough Defeated", options=[OptionFilter(LogicToAccessCatacombs, LogicToAccessCatacombs.option_ornstein_and_smough)], filtered_resolution=True)
      )
  ],
  "The Catacombs - Door 1": [
    DsrEntranceRule("The Catacombs", True_()),
  ],
  "The Catacombs - After Door 1": [
    DsrEntranceRule("The Catacombs - Door 1", True_()),
  ],
  "The Catacombs - Pinwheel": [
    DsrEntranceRule("The Catacombs - After Door 1", Has("Boss Fog Wall Key - Pinwheel") | bossfogwall_sanity_off),
  ],
  "The Catacombs - After Pinwheel": [
    DsrEntranceRule("The Catacombs - Pinwheel", Has("Pinwheel Defeated")),
  ],
  "Tomb of the Giants": [
    DsrEntranceRule("The Catacombs - After Pinwheel", Has("Skull Lantern")),
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
    DsrEntranceRule("Tomb of the Giants - Nito", Has("Gravelord Nito Defeated")),
  ],
  "Firelink Altar": [
    DsrEntranceRule("The Abyss - After Four Kings", True_()),
    DsrEntranceRule("Firelink Shrine", HasAll("Bell of Awakening #1", "Bell of Awakening #2")),
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
    DsrEntranceRule("Sanctuary Garden - Sanctuary Guardian", Has("Sanctuary Guardian Defeated")),
  ],
  "Royal Wood": [
    DsrEntranceRule("Oolacile Sanctuary", True_()),
  ],
  "Royal Wood - Artorias": [
    DsrEntranceRule("Royal Wood", Has("Boss Fog Wall Key - Artorias") | bossfogwall_sanity_off),
  ],
  "Royal Wood - After Hawkeye Gough": [
    DsrEntranceRule("Oolacile Township - After Crest Key", True_()),
  ],
  "Oolacile Township": [
    DsrEntranceRule("Royal Wood - Artorias", Has("Artorias the Abysswalker Defeated")),
  ],
  "Oolacile Township - Behind Light-Dispelled Walls": [
    DsrEntranceRule("Oolacile Township", Has("Skull Lantern")),
  ],
  "Oolacile Township - After Crest Key": [
    DsrEntranceRule("Oolacile Township", Has("Crest Key")),
  ],
  "Chasm of the Abyss": [
    DsrEntranceRule("Oolacile Township", True_()),
  ],
  "Chasm of the Abyss - Manus": [
    DsrEntranceRule("Chasm of the Abyss", Has("Boss Fog Wall Key - Manus") | bossfogwall_sanity_off),
  ],
}



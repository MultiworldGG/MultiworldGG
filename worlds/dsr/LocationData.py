from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from rule_builder.rules import Rule, True_

# class DSRRule(IntEnum):
#     ALWAYS = 0,
#     ITEM = 1,


class DSREntrance(NamedTuple):
    source: str
    rule: Rule

region_rules_table = {
  "Firelink Shrine": [
    DSREntrance("Northern Undead Asylum - Big Pilgrim Door", True_()),
    DSREntrance("The Catacombs", True_()),
    DSREntrance("Upper Undead Burg - Before Fog", True_()),
    DSREntrance("Upper New Londo Ruins", True_()),
    DSREntrance("Firelink Shrine - After Undead Parish Elevator", True_())
  ]
}



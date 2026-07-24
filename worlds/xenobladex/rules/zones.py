import dataclasses
from typing import TYPE_CHECKING
from typing_extensions import override
from BaseClasses import CollectionState
from rule_builder.rules import Rule
from ..Locations import xenobladeXSegmentLookup

if TYPE_CHECKING:
    from .. import XenobladeXWorld


@dataclasses.dataclass()
class HasZoneCount(Rule["XenobladeXWorld"], game="Xenoblade X"):
    zone: str
    target: int

    def _instantiate(self, world: "XenobladeXWorld") -> Rule.Resolved:
        return self.Resolved(self.zone, self.target, player=world.player,
                             caching_enabled=getattr(world, "rule_caching_enabled", False))

    class Resolved(Rule.Resolved):
        zone: str
        target: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            count = 0
            for reg, reg_count in xenobladeXSegmentLookup[self.zone].items():
                if state.can_reach_region(reg, self.player):
                    count += reg_count
                    if count >= self.target:
                        return True
            return False

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {reg: {id(self)} for reg in xenobladeXSegmentLookup[self.zone].keys()}


zone_rules: dict[str, Rule["XenobladeXWorld"]] = {
    # 693 Segments
    "Mira 10": HasZoneCount("Mira", 70),
    "Mira 18": HasZoneCount("Mira", 125),
    "Mira 20": HasZoneCount("Mira", 139),
    "Mira 40": HasZoneCount("Mira", 278),
    "Mira 50": HasZoneCount("Mira", 347),
    "Mira 60": HasZoneCount("Mira", 416),
    "Mira 80": HasZoneCount("Mira", 555),
    # 87 Segments
    "Prim 15": HasZoneCount("Prim", 14),
    "Prim 50": HasZoneCount("Prim", 44),
    # 77 Segments
    "Noct 15": HasZoneCount("Noct", 12),
    "Noct 20": HasZoneCount("Noct", 16),
    "Noct 25": HasZoneCount("Noct", 20),
    "Noct 30": HasZoneCount("Noct", 24),
    "Noct 45": HasZoneCount("Noct", 35),
    "Noct 85": HasZoneCount("Noct", 66),
    # 95 Segments
    "Obli 25": HasZoneCount("Obli", 24),
    "Obli 30": HasZoneCount("Obli", 29),
    "Obli 40": HasZoneCount("Obli", 38),
    "Obli 50": HasZoneCount("Obli", 48),
    "Obli 70": HasZoneCount("Obli", 67),
    # 92 Segments
    "Sylv 15": HasZoneCount("Sylv", 14),
    # 75 Segments
    "Caul 10": HasZoneCount("Caul", 8),
    "Caul 50": HasZoneCount("Caul", 38),
    "Caul 65": HasZoneCount("Caul", 49),
}

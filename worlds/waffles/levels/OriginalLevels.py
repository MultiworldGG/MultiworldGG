from .Types import SMWLocation, SMWLevel, SMWLevelPack
from ..Names import LocationName, ItemName
from ..Constants import *
from rule_builder.rules import Rule, Has, HasAll

EASY_LEVELS = 0xFFFE
HARD_LEVELS = 0xFFFF

CanSpinJump: Rule = Has(ItemName.spin_jump) & Has(ItemName.progressive_powerup, 1)

levels = {
    LocationName.yoshis_island_1_region: SMWLevel(
        LocationName.yoshis_island_1_region,
        EASY_LEVELS,
        [
            SMWLocation(DRAGON_COINS | YI1, LocationName.yoshis_island_1_dragon, CanSpinJump),
            SMWLocation(MOON | YI1, LocationName.yoshis_island_1_moon, CanSpinJump),
        ]

    )
}
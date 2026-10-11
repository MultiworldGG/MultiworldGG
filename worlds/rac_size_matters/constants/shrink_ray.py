"""This module contains string constants for Shrink Ray puzzle-gate locations"""

from dataclasses import dataclass
from enum import IntFlag


@dataclass(frozen=True)
class Rac5ShrinkRayGrindrail:
    """String constants for Shrink Ray puzzle-gate locations"""

    KALIDON_ENTER_FACTORY = "Kalidon: Shrink Ray Enter the Factory"
    KALIDON_INSIDE_FACTORY = "Kalidon: Shrink Ray Inside the Factory"
    CHALLAX_GRINDRAIL = "Challax: Shrink Ray Grindrail"
    DAYNI_MOON_TITANIUM_BOLT_ENTRANCE = "Dayni Moon: Shrink Ray Titanium bolt entrance"
    INSIDE_CLANK_GRINDRAIL = "Inside Clank: Shrink Ray Grindrail"
    QUODRONA_ENTRANCE = "Quodrona: Shrink Ray Entrance"
    QUODRONA_CLONE_TRAINING_ROOM = "Quodrona: Shrink Ray Clone Training Room"
    OUTPOST_OMEGA_GRINDRAIL = "Outpost Omega: Shrink Ray Grindrail"
    CHALLAX_SECOND_PUZZLE = "Challax: Shrink Ray Second Puzzle"
    OUTPOST_OMEGA_SECOND_GRINDRAIL = "Outpost Omega: Shrink Ray Second Grindrail"


class ShrinkRayPuzzleBit(IntFlag):
    KALIDON_ENTER_FACTORY = 0x0001
    KALIDON_INSIDE_FACTORY = 0x0002
    CHALLAX_GRINDRAIL = 0x0010
    DAYNI_MOON_TITANIUM_BOLT_ENTRANCE = 0x0040
    INSIDE_CLANK_GRINDRAIL = 0x0080
    QUODRONA_ENTRANCE = 0x0200
    QUODRONA_CLONE_TRAINING_ROOM = 0x0400
    OUTPOST_OMEGA_GRINDRAIL = 0x0004
    CHALLAX_SECOND_PUZZLE = 0x0020
    OUTPOST_OMEGA_SECOND_GRINDRAIL = 0x0008


OUTPOST_OMEGA_GRINDRAIL_BIT: ShrinkRayPuzzleBit = ShrinkRayPuzzleBit.OUTPOST_OMEGA_GRINDRAIL

SHRINK_RAY_PUZZLE_BITS: dict[str, ShrinkRayPuzzleBit] = {
    Rac5ShrinkRayGrindrail.KALIDON_ENTER_FACTORY: ShrinkRayPuzzleBit.KALIDON_ENTER_FACTORY,
    Rac5ShrinkRayGrindrail.KALIDON_INSIDE_FACTORY: ShrinkRayPuzzleBit.KALIDON_INSIDE_FACTORY,
    Rac5ShrinkRayGrindrail.CHALLAX_GRINDRAIL: ShrinkRayPuzzleBit.CHALLAX_GRINDRAIL,
    Rac5ShrinkRayGrindrail.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE: ShrinkRayPuzzleBit.DAYNI_MOON_TITANIUM_BOLT_ENTRANCE,
    Rac5ShrinkRayGrindrail.INSIDE_CLANK_GRINDRAIL: ShrinkRayPuzzleBit.INSIDE_CLANK_GRINDRAIL,
    Rac5ShrinkRayGrindrail.QUODRONA_ENTRANCE: ShrinkRayPuzzleBit.QUODRONA_ENTRANCE,
    Rac5ShrinkRayGrindrail.QUODRONA_CLONE_TRAINING_ROOM: ShrinkRayPuzzleBit.QUODRONA_CLONE_TRAINING_ROOM,
    Rac5ShrinkRayGrindrail.OUTPOST_OMEGA_GRINDRAIL: ShrinkRayPuzzleBit.OUTPOST_OMEGA_GRINDRAIL,
    Rac5ShrinkRayGrindrail.CHALLAX_SECOND_PUZZLE: ShrinkRayPuzzleBit.CHALLAX_SECOND_PUZZLE,
    Rac5ShrinkRayGrindrail.OUTPOST_OMEGA_SECOND_GRINDRAIL: ShrinkRayPuzzleBit.OUTPOST_OMEGA_SECOND_GRINDRAIL,
}

SHRINK_RAY_LOCATION_PLANETS = dict(zip(SHRINK_RAY_PUZZLE_BITS, (3, 3, 7, 8, 9, 10, 10, 6, 7, 6)))

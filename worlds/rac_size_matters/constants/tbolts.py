"""This module contains string constants for Titanium Bolt locations"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5TBolts:
    """String constants for Titanium Bolt locations"""

    POKITARU_ZIPLINE = "Pokitaru: T-Bolt: Above Zipline"
    POKITARU_HUT = "Pokitaru: T-Bolt: Behind Hut"

    RYLLUS_WALL = "Ryllus: T-Bolt: After the Wall"
    RYLLUS_CLIFF = "Ryllus: T-Bolt: Down The Cliff"

    KALIDON_SHIP = "Kalidon: T-Bolt: Behind Ship"
    KALIDON_RAMP = "Kalidon: T-Bolt: Grav-Ramps"
    KALIDON_FACTORY = "Kalidon: T-Bolt: Side of Mechanoid Factory"

    METALIS_DOOR = "Metalis: T-Bolt: Behind the Polarized Door"

    DREAMTIME_CRAB = "Dreamtime: T-Bolt: Apparition of the Scuttle Crab"
    DREAMTIME_HAT = "Dreamtime: T-Bolt: Atop the floating hat"
    DREAMTIME_GARAGE = "Dreamtime: T-Bolt: To the left of Ratchet's Garage"

    OUTPOST_OMEGA_DREAM = "Outpost Omega: T-Bolt: Near the Entrance to DreamTime"

    CHALLAX_MECH_PAD = "Challax: T-Bolt: Beside The Ultra Mech Pad"
    CHALLAX_ROOM = "Challax: T-Bolt: Hidden Room"
    CHALLAX_PLANT = "Challax: T-Bolt: Mimic Plant Lob"

    DAYNI_MOON_MIMIC = "Dayni Moon: T-Bolt: Bounce on the Blue mimic"
    DAYNI_MOON_BARN = "Dayni Moon: T-Bolt: Planting at the Barnyard"

    INSIDE_CLANK_LADDER = "Inside Clank: T-Bolt: Walk behind the ladder"
    INSIDE_CLANK_WALL = "Inside Clank: T-Bolt: Wall jumping Technomite"

    QUODRONA_DUMMIES = "Quodrona: T-Bolt: Ratchet Clones and Dummies"

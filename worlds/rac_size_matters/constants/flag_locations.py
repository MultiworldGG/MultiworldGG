"""This module contains string constants for each flag related location"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5FlagLocations:
    """String constants for flag locations"""

    RYLLUS_BUZZING = "Ryllus: Buzzing Cameras"
    KALIDON_EXPLORE = "Kalidon: Explore the planet"
    METALIS_CLANK = "Metalis: Start Giant Clank"
    OUTPOST_OMEGA = "Outpost Omega: Escape from facility pt 1"
    DAYNI_MOON_FIGHT1 = "Dayni Moon: Luna fight chased by the tractor"
    DAYNI_MOON_FIGHT2 = "Dayni Moon: Luna fight falling rocks"
    QUODRONA_CLONE = "Quodrona: Clone Wars (Fight the Ratchet Clones)"
    QUODRONA_CHASE = "Quodrona: Runnnn from Otto"
    QUODRONA_MECHA = "Quodrona: Defeat Mecha Otto"

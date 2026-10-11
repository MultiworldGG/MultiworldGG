"""This module contains string constants for Skyboard Challenge locations"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5SkyboardChallenges:
    """String constants for Skyboard Challenge locations"""

    KALIDON_LEARNER = "Kalidon: Skyboard Challenge: Learner's Challenge"
    KALIDON_MASTER = "Kalidon: Skyboard Challenge: Master's Challenge"
    KALIDON_TICKET = "Kalidon: Skyboard Challenge: Speeding Ticket"
    KALIDON_TRICKY = "Kalidon: Skyboard Challenge: Tricky Air"

    OUTPOST_OMEGA_DANGER = "Outpost Omega: Skyboard Challenge: Danger, High Voltage"
    OUTPOST_OMEGA_INTERIOR = "Outpost Omega: Skyboard Challenge: Interior Decorating"
    OUTPOST_OMEGA_VERTIGO = "Outpost Omega: Skyboard Challenge: Vertigo"
    OUTPOST_OMEGA_VORTEX = "Outpost Omega: Skyboard Challenge: The Vortex"

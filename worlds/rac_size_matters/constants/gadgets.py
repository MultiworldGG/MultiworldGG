"""This module contains string constants for each gadget in Rac5."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5Gadgets:
    """A class containing all the gadgets in Rac5, for use in rules and logic."""

    HYPERSHOT = "Hypershot"
    SPROUT_O_MATIC = "Sprout-O-Matic"
    POLARIZER = "Polarizer"
    PDA = "PDA"
    SHRINK_RAY = "Shrink Ray"
    BOLT_GRABBER = "Bolt Grabber"
    MAP_O_MATIC = "Map-O-Matic"
    BOX_BREAKER = "Box Breaker"

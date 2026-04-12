from typing import NamedTuple

from .options import Difficulty
from .rules import *


# Eventually, the goal is to allow opting in and out of certain tricks rather than the all-or-nothing system we have now


class TrickData(NamedTuple):
    rule: Requirement | None
    # TODO: Categories, difficulties?


def trick(name: str):
    rule = trick_table[name].rule
    if rule is None:
        return advanced_logic()
    return advanced_logic() & rule


trick_table = {
    # Throw an enemy into the ceiling and enter with Puffy Wario
    "MJ CD box with grab": TrickData(has("Grab")),

    # Throw the Yeti at the block.
    "40BF CD box with heavy grab": TrickData(has("Heavy Grab")),

    # Ground pound the switches in the maze puzzle room by getting a running start and stomp jumping on the glass ball
    # right after the glass bird spits it out.
    "40BF glass ball stomp jump": TrickData(has_all(["Stomp Jump", "Ground Pound"])),

    # Lure the Ringosuki toward the water and grab the apple in midair.
    "TTL transformation puzzle without heavy grab": TrickData(None),

    # Throw one of the lower pinballs at the ones on the ledges.
    "PZ fruit room without ground pound": TrickData(None),

    # Carry a Ringosuki to the top of the room to move the pinballs using Fat Wario jumps.
    "PZ jungle room with Fat Wario": TrickData(has("Heavy Grab")),

    # Throw a Toy Car at the gray blocks.
    "DW gray square room with grab": TrickData(not_difficulty(Difficulty.option_normal) & has("Grab")),

    # Ground pound from the top of the room to knock down a toy car, then stomp-jump it for the diamond
    # Superceded by the damage boost trick below
    # "DR toy car tower diamond without grab": TrickData(has_all(["Super Ground Pound", "Head Smash"])),

    # Go up the left path, take damage from the spikes, break the leftmost block, then collect the diamond from above.
    "DR toy car tower diamond damage boost": TrickData(None),

    # Break the blocks with a toy car or your head before starting the escape.
    # Superceded by the escape with only swim trick below
    # "DR escape without ground pound": TrickData(has_any(["Grab", "Head Smash"])),

    # Break the blocks with shoulder bashes, using invulnerability frames to hit the second one through the spikes.
    "DR escape with only swim": TrickData(None),

    # Drop off the top of the ladder and immediately start a ground pound
    "DR switch room block no dash attack": TrickData(has("Super Ground Pound")),

    # Break the wooden boxes by throwing the mummy enemies.
    "AN Onomi room with grab": TrickData(has("Grab")),

    # Access the switch on hard by throwing the Marumen upward, stomping it in midair, and starting a ground pound.
    "HH escape minion jump": TrickData(
        difficulty(Difficulty.option_hard) & has_all(["Grab", "Stomp Jump", "Super Ground Pound"])
    ),

    # To jump off the waves, start walking before you jump. When the waves start oscillating, jump at the apex.
    "Catbat without stomp jump": TrickData(None),

    # Repeatedly jump out of the river with good timing.
    "GP current room skip": TrickData(None),

    # Use the jewel piece box as a platform to escape the area with the blue block. You can safely collect the item
    # after breaking the blocks below the blue block.
    # NOTE: This trick isn't relevant in practice yet: reaching Golden Passage always requires ground pound because of
    # Cractus and Catbat
    "GP Keyzer puzzle without ground pound": TrickData(has("Grab")),
}

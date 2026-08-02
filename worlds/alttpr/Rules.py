from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .World import ALttPRWorld


def set_all_rules(world: ALttPRWorld) -> None:
    # The rules are taken from Door Randomizer while we're generating the regions and locations,
    # in Regions.py. The only thing left is setting how to win.
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Triforce", world.player)

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING

from . import itembase

if TYPE_CHECKING:
    from ... import CupheadWorld

def get_filler_item_name(world: "CupheadWorld") -> str:
    item_weights = world.options.filler_item_weights.value
    if item_weights:
        return itembase.weighted_item_choice(item_weights, world.random)

    # Item-link synthetic players can skip Cuphead option resolution and end up with empty weights.
    from . import itemdefs as idef
    return world.random.choice(list(idef.item_filler.keys()))

"""Signature-checked native patches for the US PS2 executable."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class PatchOptions:
    """Native patch switches; dependent UI hooks also require vendor and skin hooks."""

    ship_menu: bool = True
    vendor: bool = True
    vendor_presentation: bool = True
    shrink_ray: bool = True
    skins: bool = True
    multiplayer_skins: bool = True
    item_toast: bool = True
    connection_warning: bool = True
    armour_pickup: bool = True
    pokitaru_ship: bool = True
    sprout_pickup: bool = True
    inside_clank_exit: bool = True
    balance_patch: bool = False

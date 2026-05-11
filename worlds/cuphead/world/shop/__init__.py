### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING, Self

from ..names import locationnames, regionnames

if TYPE_CHECKING:
    from ..options import CupheadOptions


shop_weapons = [
    locationnames.loc_shop_weapon1,
    locationnames.loc_shop_weapon2,
    locationnames.loc_shop_weapon3,
    locationnames.loc_shop_weapon4,
    locationnames.loc_shop_weapon5,
    locationnames.loc_shop_dlc_weapon6,
    locationnames.loc_shop_dlc_weapon7,
    locationnames.loc_shop_dlc_weapon8
]
shop_charms = [
    locationnames.loc_shop_charm1,
    locationnames.loc_shop_charm2,
    locationnames.loc_shop_charm3,
    locationnames.loc_shop_charm4,
    locationnames.loc_shop_charm5,
    locationnames.loc_shop_charm6,
    locationnames.loc_shop_dlc_charm7,
    locationnames.loc_shop_dlc_charm8
]

class ShopData:
    shop_map: list[tuple[int, int]]
    shop_locations: dict[str, list[str]]

    def __init__(self, shop_map: list[tuple[int, int]]):
        shop_locations: dict[str, list[str]] = {}

        weapon_index = 0
        charm_index = 0
        for i in range(4):
            shop_region: list[str] = []
            if (i == 3):
                shop_region += shop_weapons[weapon_index:]+shop_charms[charm_index:]
            else:
                wcount = min(shop_map[i][0], len(shop_weapons)-weapon_index)
                ccount = min(shop_map[i][1], len(shop_charms)-charm_index)
                shop_region += shop_weapons[weapon_index:(weapon_index+wcount)]
                shop_region += shop_charms[charm_index:(charm_index+ccount)]
                weapon_index+=wcount
                charm_index+=ccount
            shop_locations[regionnames.shop_sets[i]] = shop_region

        self.shop_map = shop_map
        self.shop_locations = shop_locations

    @classmethod
    def create_from_options(cls, options: "CupheadOptions") -> Self:
        return cls(options.shop_map.value)

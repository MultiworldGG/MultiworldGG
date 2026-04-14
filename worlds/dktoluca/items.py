import typing

from BaseClasses import Item, ItemClassification
from .enums import Items
from .constants import *

class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classsification: ItemClassification
    quantity: int = 1

class DKC3Item(Item):
    game = GAME_NAME

# Item tables
worlds_table = {
    Items.lake_orangatanga:      ItemData(FLAG | 0x020, ItemClassification.progression | ItemClassification.useful),
    Items.kremwood_forest:       ItemData(FLAG | 0x021, ItemClassification.progression | ItemClassification.useful),
    Items.cotton_top_cove:       ItemData(FLAG | 0x022, ItemClassification.progression | ItemClassification.useful),
    Items.mekanos:               ItemData(FLAG | 0x023, ItemClassification.progression | ItemClassification.useful),
    Items.k3:                    ItemData(FLAG | 0x024, ItemClassification.progression | ItemClassification.useful),
    Items.razor_ridge:           ItemData(FLAG | 0x025, ItemClassification.progression | ItemClassification.useful),
    Items.kaos_kore:             ItemData(FLAG | 0x026, ItemClassification.progression | ItemClassification.useful),
    Items.krematoa:              ItemData(FLAG | 0x027, ItemClassification.progression | ItemClassification.useful),
}

mcmuffin_table = {
    Items.banana_bird:           ItemData(COUNT | WRAM | 0x05CD, ItemClassification.progression_deprioritized_skip_balancing),
    Items.cog:                   ItemData(COUNT | WRAM | 0x05D1, ItemClassification.progression_deprioritized_skip_balancing),
    Items.bonus_coin:            ItemData(COUNT | WRAM | 0x05CB, ItemClassification.progression_deprioritized_skip_balancing),
}

progression_table = {
    Items.dixie:                 ItemData(DIXIE | 0x000, ItemClassification.progression | ItemClassification.useful),
    Items.kiddy:                 ItemData(KIDDY | 0x000, ItemClassification.progression | ItemClassification.useful),
    Items.vehicle:               ItemData(VEHICLE | 0x034, ItemClassification.progression | ItemClassification.useful),
    Items.carry:                 ItemData(FLAG | 0x001, ItemClassification.progression),
    Items.spin:                  ItemData(FLAG | 0x002, ItemClassification.progression),
    Items.climb:                 ItemData(FLAG | 0x003, ItemClassification.progression),
    Items.team_attack:           ItemData(FLAG | 0x004, ItemClassification.progression),
    Items.helicopter_spin:       ItemData(FLAG | 0x005, ItemClassification.progression),
    Items.water_bounce:          ItemData(FLAG | 0x006, ItemClassification.progression_deprioritized),
    Items.swim:                  ItemData(FLAG | 0x007, ItemClassification.progression),
    Items.ellie:                 ItemData(FLAG | 0x008, ItemClassification.progression),
    Items.enguarde:              ItemData(FLAG | 0x009, ItemClassification.progression),
    Items.squawks:               ItemData(FLAG | 0x00A, ItemClassification.progression),
    Items.squitter:              ItemData(FLAG | 0x00B, ItemClassification.progression),
    Items.parry:                 ItemData(FLAG | 0x00C, ItemClassification.progression_deprioritized),
    Items.barrel_cannon:         ItemData(FLAG | 0x010, ItemClassification.progression),
    Items.barrel_rocket:         ItemData(FLAG | 0x011, ItemClassification.progression_deprioritized),
    Items.barrel_tracker:        ItemData(FLAG | 0x012, ItemClassification.progression_deprioritized),
    Items.barrel_ghost:          ItemData(FLAG | 0x013, ItemClassification.progression_deprioritized),
    Items.barrel_warp:           ItemData(FLAG | 0x014, ItemClassification.useful),
    Items.barrel_invincible:     ItemData(FLAG | 0x015, ItemClassification.progression_deprioritized),
    Items.barrel_switch:         ItemData(FLAG | 0x016, ItemClassification.progression_deprioritized),
    Items.barrel_shield:         ItemData(FLAG | 0x017, ItemClassification.progression_deprioritized),
    Items.barrel_waterfall:      ItemData(FLAG | 0x018, ItemClassification.progression_deprioritized),
}

misc_table = {
    Items.dk_barrel:             ItemData(COUNT | 0x030, ItemClassification.filler),
    Items.bear_coin:             ItemData(COUNT | WRAM | 0x5C9, ItemClassification.filler),
    Items.dk_coin:               ItemData(COUNT | WRAM | 0x5CF, ItemClassification.filler),
    Items.balloon:               ItemData(COUNT | WRAM | 0x5D5, ItemClassification.filler),
}

extra_table = {
    Items.extractinator:         ItemData(COUNT | 0x032, ItemClassification.useful),
    Items.radar:                 ItemData(FLAG | 0x00F, ItemClassification.useful),
    Items.glitched:              ItemData(None, ItemClassification.progression_skip_balancing),
}

item_groups = {
    "Worlds": {
        #Items.lake_orangatanga,
        Items.kremwood_forest.value,
        Items.cotton_top_cove.value,
        Items.mekanos.value,
        Items.k3.value,
        Items.razor_ridge.value,
        #Items.kaos_kore.value,
        Items.krematoa.value,
    },
    "Abilities": {
        Items.carry.value,
        Items.climb.value,
        Items.swim.value,
        Items.spin.value,
        Items.helicopter_spin.value,
        Items.team_attack.value,
        Items.water_bounce.value,
    },
    "Animals": {
        Items.enguarde.value,
        Items.squawks.value,
        Items.squitter.value,
        Items.parry.value,
        Items.ellie.value,
    },
    "Barrels": {
        Items.barrel_cannon.value,
        Items.barrel_rocket.value,
        Items.barrel_tracker.value,
        Items.barrel_ghost.value,
        Items.barrel_warp.value,
        Items.barrel_invincible.value,
        Items.barrel_switch.value,
        Items.barrel_shield.value,
        Items.barrel_waterfall.value,
    }
}

item_table = {
    **mcmuffin_table,
    **worlds_table,
    **progression_table,
    **misc_table,
    **extra_table,
}

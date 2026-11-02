import typing

from BaseClasses import Item, ItemClassification
from .Names import ItemName
from .Levels import full_level_list, level_info_dict

boss_course_numbers = {5, 13, 19, 25, 30, 36, 40}
course_unlock_names = {
    level_id: f"{level_info_dict[level_id].levelName} - Unlock"
    for number, level_id in enumerate(full_level_list, 1) if number not in boss_course_numbers
}


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    progression: bool
    trap: bool = False
    quantity: int = 1


class WLItem(Item):
    game: str = "Wario Land"


powerup_order = (ItemName.wario_garlic, ItemName.wario_bull,
                 ItemName.wario_dragon, ItemName.wario_jet)


# Uh oh
junk_table = {
    ItemName.stinky_1up: ItemData(0xA80900, False),
    ItemName.garlic_breath: ItemData(0xA80000, False),
    ItemName.garlic_tea: ItemData(0xA80001, False),
    ItemName.garlic_bread: ItemData(0xA80002, False),
    ItemName.noxious: ItemData(0xA80003, False),
    ItemName.garlic_cheesecake: ItemData(0xA80004, False),
    ItemName.garlic_pesto: ItemData(0xA80005, False),
    ItemName.garlic_sandwich: ItemData(0xA80006, False),
    ItemName.garlic_burger: ItemData(0xA80007, False),
    ItemName.garlic_cookie: ItemData(0xA80008, False),
    ItemName.garlic_soda: ItemData(0xA80009, False),
    ItemName.nothing: ItemData(0xA800F0, False),
    ItemName.heart: ItemData(0xA80800, False),
    ItemName.coin: ItemData(0xA80700, False),
}

upgrade_table = {
    ItemName.wario_garlic: ItemData(0xA40000, True),
    ItemName.wario_bull: ItemData(0xA40100, True),
    ItemName.wario_jet: ItemData(0xA40200, True),
    ItemName.wario_dragon: ItemData(0xA40300, True),
    ItemName.wario_dash: ItemData(0xA40400, True),
    ItemName.wario_highjump: ItemData(0xA40500, True),
    ItemName.wario_createcoin: ItemData(0xA40600, True),
    ItemName.wario_climb: ItemData(0xA40700, True),
    ItemName.wario_duck: ItemData(0xA40800, True),
    # ItemName.wario_grow:            ItemData(0xA41000, True),    # This is set when upgrades are received
    ItemName.progressive_powerup: ItemData(0xA41100, True),
}

world_unlock_table = {
    ItemName.ricebeach: ItemData(0xA40900, True),
    ItemName.mtteapot: ItemData(0xA40A00, True),
    ItemName.stovecanyon: ItemData(0xA40B00, True),
    ItemName.parsleywoods: ItemData(0xA40C00, True),
    ItemName.ssteacup: ItemData(0xA40D00, True),
    ItemName.sherbetland: ItemData(0xA40E00, True),
    ItemName.syrupcastle: ItemData(0xA40F00, True),
}

boss_unlock_table = {
    ItemName.ricebeach_bossunlock: ItemData(0xA42100, True),
    ItemName.mtteapot_bossunlock: ItemData(0xA42200, True),
    ItemName.stovecanyon_bossunlock: ItemData(0xA42300, True),
    ItemName.parsleywoods_bossunlock: ItemData(0xA42400, True),
    ItemName.ssteacup_bossunlock: ItemData(0xA42500, True),
    ItemName.sherbetland_bossunlock: ItemData(0xA42600, True),
    # ItemName.syrupcastle_bossunlock:   ItemData(0xA42700, True),
}

trap_table = {
    ItemName.wario_stun_trap: ItemData(0xA38400, False, True),
    ItemName.wario_timer_trap: ItemData(0xA96400, False, True),
    ItemName.wario_death_trap: ItemData(0xA91A00, False, True),
    ItemName.wario_grease_trap: ItemData(0xA61C00, False, True),
}

collectable_table = {
    ItemName.garlic_clove: ItemData(0xA42800, True),
}

# It's "free" real estate
event_table = {
    ItemName.victory: ItemData(None, True),
    ItemName.boss_token: ItemData(0xA41200, True),
}

# Complete item table.
course_unlock_table = {name: ItemData((0xA4B0 + level_id) << 8, True)
                       for level_id, name in course_unlock_names.items()}

item_table = {
    **course_unlock_table,
    **junk_table,
    **collectable_table,
    **upgrade_table,
    **trap_table,
    **event_table,
    **boss_unlock_table,
    **world_unlock_table,
}

lookup_id_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in item_table.items() if data.code
}

# Generate Client Lookup Tables
lookup_junkid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in junk_table.items() if data.code
}
lookup_collectableid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in collectable_table.items() if data.code
}
lookup_upgradeid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in upgrade_table.items() if data.code
}
lookup_trapid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in trap_table.items() if data.code
}
lookup_eventid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in event_table.items() if data.code
}
lookup_worldunlockid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in world_unlock_table.items() if data.code
}
lookup_bossunlockid_to_name: typing.Dict[int, str] = {
    data.code: item_name for item_name, data in boss_unlock_table.items() if data.code
}

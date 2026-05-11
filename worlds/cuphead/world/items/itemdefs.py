### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

# Prefer things to be on one line than scrunched, so ignore length issues with linting.
# ruff: noqa: E501

from BaseClasses import ItemClassification

from ..names import itemnames
from .itembase import ItemData

# Items
# Next ids: 22005, 10016001
item_generic: dict[str, ItemData] = {
    itemnames.item_level_generic: ItemData(1000, ItemClassification.filler, 0),
}
item_filler: dict[str, ItemData] = {
    itemnames.item_level_extrahealth: ItemData(2000, ItemClassification.filler, 0),
    itemnames.item_level_supercharge: ItemData(2001, ItemClassification.filler, 0),
    itemnames.item_level_fastfire: ItemData(2002, ItemClassification.filler, 0),
    #itemnames.item_level_4: ItemData(2003, ItemClassification.filler, 0),
}

item_essential: dict[str, ItemData] = {
    itemnames.item_coin: ItemData(4000, ItemClassification.progression_deprioritized_skip_balancing, 0),
    itemnames.item_coin2: ItemData(4001, ItemClassification.progression_deprioritized_skip_balancing, 0),
    itemnames.item_coin3: ItemData(4002, ItemClassification.progression_deprioritized_skip_balancing, 0),
    itemnames.item_contract: ItemData(4003, ItemClassification.progression_skip_balancing, 17),
    itemnames.item_plane_gun: ItemData(4004, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_plane_ex: ItemData(4005, ItemClassification.progression | ItemClassification.useful, 0),
    itemnames.item_plane_bombs: ItemData(4006, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_healthupgrade: ItemData(4007, ItemClassification.useful, 0)
}
item_dlc_essential: dict[str, ItemData] = {
    itemnames.item_dlc_boat: ItemData(10000000, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_dlc_ingredient: ItemData(10000001, ItemClassification.progression_deprioritized_skip_balancing, 5),
}
item_dlc_chalice_essential: dict[str, ItemData] = {
    itemnames.item_dlc_cplane_gun: ItemData(10002000, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_dlc_cplane_ex: ItemData(10002001, ItemClassification.progression | ItemClassification.useful, 0),
    itemnames.item_dlc_cplane_bombs: ItemData(10002002, ItemClassification.progression | ItemClassification.useful),
}
item_all_essential = {**item_essential, **item_dlc_essential, **item_dlc_chalice_essential}

item_weapons: dict[str, ItemData] = {
    itemnames.item_weapon_peashooter: ItemData(6000, ItemClassification.useful),
    itemnames.item_weapon_spread: ItemData(6001, ItemClassification.useful),
    itemnames.item_weapon_chaser: ItemData(6002, ItemClassification.useful),
    itemnames.item_weapon_lobber: ItemData(6003, ItemClassification.useful),
    itemnames.item_weapon_charge: ItemData(6004, ItemClassification.useful),
    itemnames.item_weapon_roundabout: ItemData(6005, ItemClassification.useful),
}
item_dlc_weapons: dict[str, ItemData] = {
    itemnames.item_weapon_dlc_crackshot: ItemData(10004000, ItemClassification.useful),
    itemnames.item_weapon_dlc_converge: ItemData(10004001, ItemClassification.useful),
    itemnames.item_weapon_dlc_twistup: ItemData(10004002, ItemClassification.useful),
}
item_all_weapons: dict[str, ItemData] = {**item_weapons, **item_dlc_weapons}

item_weapon_ex: dict[str, ItemData] = {
    itemnames.item_weapon_peashooter_ex: ItemData(8000, ItemClassification.useful),
    itemnames.item_weapon_spread_ex: ItemData(8001, ItemClassification.useful),
    itemnames.item_weapon_chaser_ex: ItemData(8002, ItemClassification.useful),
    itemnames.item_weapon_lobber_ex: ItemData(8003, ItemClassification.useful),
    itemnames.item_weapon_charge_ex: ItemData(8004, ItemClassification.useful),
    itemnames.item_weapon_roundabout_ex: ItemData(8005, ItemClassification.useful),
}
item_dlc_weapon_ex: dict[str, ItemData] = {
    itemnames.item_weapon_dlc_crackshot_ex: ItemData(10006000, ItemClassification.useful),
    itemnames.item_weapon_dlc_converge_ex: ItemData(10006001, ItemClassification.useful),
    itemnames.item_weapon_dlc_twistup_ex: ItemData(10006002, ItemClassification.useful),
}
item_all_weapon_ex: dict[str, ItemData] = {**item_weapon_ex, **item_dlc_weapon_ex}

item_p_weapons: dict[str, ItemData] = {
    itemnames.item_p_weapon_peashooter: ItemData(10000, ItemClassification.useful),
    itemnames.item_p_weapon_spread: ItemData(10001, ItemClassification.useful),
    itemnames.item_p_weapon_chaser: ItemData(10002, ItemClassification.useful),
    itemnames.item_p_weapon_lobber: ItemData(10003, ItemClassification.useful),
    itemnames.item_p_weapon_charge: ItemData(10004, ItemClassification.useful),
    itemnames.item_p_weapon_roundabout: ItemData(10005, ItemClassification.useful),
}
item_dlc_p_weapons: dict[str, ItemData] = {
    itemnames.item_p_weapon_dlc_crackshot: ItemData(10008000, ItemClassification.useful),
    itemnames.item_p_weapon_dlc_converge: ItemData(10008001, ItemClassification.useful),
    itemnames.item_p_weapon_dlc_twistup: ItemData(10008002, ItemClassification.useful),
}
item_all_p_weapons: dict[str, ItemData] = {**item_p_weapons, **item_dlc_p_weapons}

item_charms: dict[str, ItemData] = {
    itemnames.item_charm_heart: ItemData(12000, ItemClassification.useful),
    itemnames.item_charm_smokebomb: ItemData(12001, ItemClassification.useful),
    itemnames.item_charm_psugar: ItemData(12002, ItemClassification.useful),
    itemnames.item_charm_coffee: ItemData(12003, ItemClassification.useful),
    itemnames.item_charm_twinheart: ItemData(12004, ItemClassification.useful),
    itemnames.item_charm_whetstone: ItemData(12005, ItemClassification.useful),
}
item_dlc_charms: dict[str, ItemData] = {
    itemnames.item_charm_dlc_heartring: ItemData(10010000, ItemClassification.useful),
    itemnames.item_charm_dlc_broken_relic: ItemData(10010001, ItemClassification.useful, 0), # Sequence will not be in logic
}
item_all_charms: dict[str, ItemData] = {**item_charms, **item_dlc_charms}

item_super: dict[str, ItemData] = {
    itemnames.item_super_i: ItemData(14000, ItemClassification.useful),
    itemnames.item_super_ii: ItemData(14001, ItemClassification.useful),
    itemnames.item_super_iii: ItemData(14002, ItemClassification.useful),
    itemnames.item_plane_super: ItemData(14003, ItemClassification.useful),
}
item_dlc_chalice_super: dict[str, ItemData] = {
    itemnames.item_super_dlc_c_i: ItemData(10012000, ItemClassification.useful),
    itemnames.item_super_dlc_c_ii: ItemData(10012001, ItemClassification.useful),
    itemnames.item_super_dlc_c_iii: ItemData(10012002, ItemClassification.useful),
    itemnames.item_dlc_cplane_super: ItemData(10012003, ItemClassification.useful),
}
item_all_super: dict[str, ItemData] = {**item_super, **item_dlc_chalice_super}

item_abilities: dict[str, ItemData] = {
    itemnames.item_ability_crouch: ItemData(16000, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dash: ItemData(16001, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_parry: ItemData(16002, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_plane_parry: ItemData(16003, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_plane_shrink: ItemData(16004, ItemClassification.useful),
}
item_dlc_chalice_abilities: dict[str, ItemData] = {
    itemnames.item_ability_dlc_ccrouch: ItemData(10014000, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_p_cdash: ItemData(10014001, ItemClassification.progression | ItemClassification.useful, 2),
    itemnames.item_ability_dlc_cdoublejump: ItemData(10014002, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_cplane_parry: ItemData(10014003, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_cplane_shrink: ItemData(10014004, ItemClassification.useful),
}
item_all_abilities: dict[str, ItemData] = {**item_abilities, **item_dlc_chalice_abilities}

item_abilities_aim: dict[str, ItemData] = {
    itemnames.item_ability_aim_left: ItemData(18000, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_right: ItemData(18001, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_up: ItemData(18002, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_down: ItemData(18003, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_upleft: ItemData(18004, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_upright: ItemData(18005, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_downleft: ItemData(18006, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_aim_downright: ItemData(18007, ItemClassification.progression | ItemClassification.useful),
}
item_dlc_chalice_abilities_aim: dict[str, ItemData] = {
    itemnames.item_ability_dlc_c_aim_left: ItemData(20000, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_right: ItemData(20001, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_up: ItemData(20002, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_down: ItemData(20003, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_upleft: ItemData(20004, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_upright: ItemData(20005, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_downleft: ItemData(20006, ItemClassification.progression | ItemClassification.useful),
    itemnames.item_ability_dlc_c_aim_downright: ItemData(20007, ItemClassification.progression | ItemClassification.useful),
}
item_all_abilities_aim: dict[str, ItemData] = {**item_abilities_aim, **item_dlc_chalice_abilities_aim}

item_trap: dict[str, ItemData] = {
    itemnames.item_level_trap_fingerjam: ItemData(22000, ItemClassification.trap, 0),
    itemnames.item_level_trap_slowfire: ItemData(22001, ItemClassification.trap, 0),
    itemnames.item_level_trap_superdrain: ItemData(22002, ItemClassification.trap, 0),
    itemnames.item_level_trap_loadout: ItemData(22003, ItemClassification.trap, 0),
    itemnames.item_level_trap_screen: ItemData(22004, ItemClassification.trap, 0),
}

item_special: dict[str, ItemData] = {
    itemnames.item_event_boss_defeated: ItemData(None, ItemClassification.progression_skip_balancing, 0),
    itemnames.item_event_isle1_secret_prereq: ItemData(None, ItemClassification.progression_deprioritized_skip_balancing, 0),
    itemnames.item_event_isle2_shortcut: ItemData(None, ItemClassification.progression_deprioritized, 0),
    itemnames.item_event_quest_4mel_4th: ItemData(None, ItemClassification.progression_deprioritized, 0),
    itemnames.item_event_agrade: ItemData(None, ItemClassification.progression_deprioritized_skip_balancing, 0),
    itemnames.item_event_pacifist: ItemData(None, ItemClassification.progression_deprioritized_skip_balancing, 0),
    itemnames.item_event_ludwig: ItemData(None, ItemClassification.progression_deprioritized, 0),
    itemnames.item_event_wolfgang: ItemData(None, ItemClassification.progression_deprioritized, 0),
    #itemnames.item_event_music: ItemData(None, ItemClassification.progression_deprioritized, 0),
}
item_dlc_special: dict[str, ItemData] = {
    itemnames.item_charm_dlc_cookie: ItemData(10016000, ItemClassification.useful, 0),
    itemnames.item_event_mausoleum: ItemData(None, ItemClassification.progression, 0),
    itemnames.item_event_dlc_boataccess: ItemData(None, ItemClassification.progression, 0),
    itemnames.item_event_dlc_start: ItemData(None, ItemClassification.progression, 0),
    itemnames.item_event_dlc_boss_chaliced: ItemData(None, ItemClassification.progression_deprioritized_skip_balancing, 0),
}
item_all_special: dict[str, ItemData] = {**item_special, **item_dlc_special}

item_goal: dict[str, ItemData] = {
    itemnames.item_event_goal_devilko: ItemData(None, ItemClassification.progression, 0),
}
item_dlc_goal: dict[str, ItemData] = {
    itemnames.item_event_goal_dlc_saltbakerko: ItemData(None, ItemClassification.progression, 0),
}

items_all_weapons: dict[str, ItemData] = {
    **item_all_weapons,
    **item_all_weapon_ex,
    **item_all_p_weapons
}

items_base: dict[str, ItemData] = {
    **item_generic,
    **item_filler,
    **item_essential,
    **item_charms,
    **item_super,
    **item_special,
    **item_goal
}
items_dlc: dict[str, ItemData] = {
    **item_dlc_essential,
    **item_dlc_charms,
    **item_dlc_special,
    **item_dlc_goal,
}

items_all: dict[str, ItemData] = {
    **items_base,
    **items_dlc,
    **items_all_weapons,
    **item_dlc_chalice_essential,
    **item_dlc_chalice_super,
    **item_abilities,
    **item_dlc_chalice_abilities,
    #**item_abilities_aim,
    #**item_dlc_chalice_abilities_aim,
    **item_trap,
}

name_to_id = {name: data.id for name, data in items_all.items() if data.id}

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from . import locationnames as ln
from . import regionnames as rn

## Item Names

# Prefixes
_item_event_ = "Event "
_item_progressive = "Progressive "

# Groups
item_group_weapon = "Weapon"
item_group_weapon_ex = "Weapon EX"
item_group_charm = "Charm"
item_group_super = "Super"
item_group_ability = "Ability"
item_group_aim_ability = "Aim Ability"

# Junk
item_level_generic = "Present"
item_level_extrahealth = "+1 Health"
item_level_supercharge = "Super Charge"
item_level_fastfire = "Fast Fire"
item_level_4 = "Item Id 4"

# Weapons
item_weapon = "Weapon"
item_weapon_peashooter = "Peashooter"
item_weapon_spread = "Spread"
item_weapon_chaser = "Chaser"
item_weapon_lobber = "Lobber"
item_weapon_charge = "Charge"
item_weapon_roundabout = "Roundabout"
item_dlc_weapon = "DLC Weapon"
item_weapon_dlc_crackshot = "Crackshot"
item_weapon_dlc_converge = "Converge"
item_weapon_dlc_twistup = "Twist-Up"

# Weapon EX
_weapon_ex = " EX"
item_weapon_ex = item_weapon + _weapon_ex
item_weapon_peashooter_ex = item_weapon_peashooter + _weapon_ex
item_weapon_spread_ex = item_weapon_spread + _weapon_ex
item_weapon_chaser_ex = item_weapon_chaser + _weapon_ex
item_weapon_lobber_ex = item_weapon_lobber + _weapon_ex
item_weapon_charge_ex = item_weapon_charge + _weapon_ex
item_weapon_roundabout_ex = item_weapon_roundabout + _weapon_ex
item_dlc_weapon_ex = item_dlc_weapon + _weapon_ex
item_weapon_dlc_crackshot_ex = item_weapon_dlc_crackshot + _weapon_ex
item_weapon_dlc_converge_ex = item_weapon_dlc_converge + _weapon_ex
item_weapon_dlc_twistup_ex = item_weapon_dlc_twistup + _weapon_ex

# Progressive Weapon
item_p_weapon = _item_progressive + "Weapon"
item_p_weapon_peashooter = _item_progressive + "Peashooter"
item_p_weapon_spread = _item_progressive + "Spread"
item_p_weapon_chaser = _item_progressive + "Chaser"
item_p_weapon_lobber = _item_progressive + "Lobber"
item_p_weapon_charge = _item_progressive + "Charge"
item_p_weapon_roundabout = _item_progressive + "Roundabout"
item_p_dlc_weapon = _item_progressive + "DLC Weapon"
item_p_weapon_dlc_crackshot = _item_progressive + "Crackshot"
item_p_weapon_dlc_converge = _item_progressive + "Converge"
item_p_weapon_dlc_twistup = _item_progressive + "Twist-Up"

# Charms
item_charm = "Charm"
item_charm_heart = "Heart"
item_charm_smokebomb = "Smoke Bomb"
item_charm_psugar = "P. Sugar"
item_charm_coffee = "Coffee"
item_charm_twinheart = "Twin Heart"
item_charm_whetstone = "Whetstone"
item_dlc_charm = "DLC Charm"
item_charm_dlc_heartring = "Heart Ring"
item_charm_dlc_broken_relic = "Broken Relic"
item_charm_dlc_cookie = "Astral Cookie"

# Super
item_super_i = "Super Art I"
item_super_ii = "Super Art II"
item_super_iii = "Super Art III"

item_super_dlc_c_i = "Chalice Super Art I"
item_super_dlc_c_ii = "Chalice Super Art II"
item_super_dlc_c_iii = "Chalice Super Art III"

# Abilities
item_ability_parry = "Parry"
item_ability_dash = "Dash"
item_ability_crouch = "Crouch"
item_ability_crouch_a = "Duck"
item_ability_plane_shrink = "Plane Shrink"
item_ability_plane_parry = "Plane Parry"

item_ability_dlc_cparry = "Chalice Parry"
item_ability_dlc_cdash = "Chalice Dash"
item_ability_dlc_p_cdash = _item_progressive + "Chalice Dash"
item_ability_dlc_cdoublejump = "Chalice Double Jump"
item_ability_dlc_ccrouch = "Chalice Crouch"
item_ability_dlc_ccrouch_a = "Chalice Duck"
item_ability_dlc_cplane_shrink = "Chalice Plane Shrink"
item_ability_dlc_cplane_parry = "Chalice Plane Parry"

item_ability_aim_left = "Aim Left"
item_ability_aim_right = "Aim Right"
item_ability_aim_up = "Aim Up"
item_ability_aim_down = "Aim Down"
item_ability_aim_upleft = "Aim Up-Left"
item_ability_aim_upright = "Aim Up-Right"
item_ability_aim_downleft = "Aim Down-Left"
item_ability_aim_downright = "Aim Down-Right"

item_ability_dlc_c_aim_left = "Chalice Aim Left"
item_ability_dlc_c_aim_right = "Chalice Aim Right"
item_ability_dlc_c_aim_up = "Chalice Aim Up"
item_ability_dlc_c_aim_down = "Chalice Aim Down"
item_ability_dlc_c_aim_upleft = "Chalice Aim Up-Left"
item_ability_dlc_c_aim_upright = "Chalice Aim Up-Right"
item_ability_dlc_c_aim_downleft = "Chalice Aim Down-Left"
item_ability_dlc_c_aim_downright = "Chalice Aim Down-Right"

# Essential
item_coin = "Coin"
item_coin2 = "2 Coins"
item_coin3 = "3 Coins"
item_progressive_plane = _item_progressive + "Plane"
item_plane = "Plane"
item_plane_gun = "Plane Peashooter"
item_plane_gun_a = "Plane Gun"
item_plane_ex = "Plane EX"
item_plane_bombs = "Plane Bombs"
item_plane_super = "Plane Super"
item_contract = "Soul Contract"
item_contract_a = "Contract"
item_healthupgrade = "+1 Max Health"
item_dlc_boat = "Boat"
item_dlc_ingredient = "Ingredient"
item_dlc_cplane_gun = "Chalice Plane Peashooter"
item_dlc_cplane_gun_a = "Chalice Plane Gun"
item_dlc_cplane_ex = "Chalice Plane EX"
item_dlc_cplane_bombs = "Chalice Plane Bombs"
item_dlc_cplane_super = "Chalice Plane Super"

# Traps
item_level_trap_fingerjam = "Finger Jam"
item_level_trap_slowfire = "Slow Fire"
item_level_trap_superdrain = "Super Drain"
item_level_trap_loadout = "Loadout Mixup"
item_level_trap_screen = "Screen Trap"

# Events
item_event_null = "null"
item_event_boss_defeated = _item_event_ + "Boss Defeated"
item_event_mausoleum = _item_event_ + "Mausoleum"
item_event_isle1_secret_prereq = _item_event_ + rn.world_inkwell_1 + " Secret Coin Prerequisite"
item_event_isle2_shortcut = _item_event_ + ln.loc_event_isle2_shortcut + " Accessed"
item_event_quest_4mel_4th = _item_event_ + ln.loc_event_quest_4mel_4th
item_event_agrade = _item_event_ + "A Grade"
item_event_pacifist = _item_event_ + "P Grade"
item_event_ludwig = _item_event_ + "Lugwig"
item_event_wolfgang = _item_event_ + "Wolfgang"
item_event_music = _item_event_ + "Music Changed"
item_event_dlc_start = _item_event_ + "DLC Start"
item_event_charm_dlc_cookie = _item_event_ + item_charm_dlc_cookie
item_event_dlc_boataccess = _item_event_ + "Boat Access"
item_event_dlc_boss_chaliced = _item_event_ + "Boss Chalice Defeated"

# Goals
item_event_goal_devilko = "The Devil's Surrender"
item_event_goal_dlc_saltbakerko = "Chef Saltbaker's Surrender"

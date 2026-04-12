from dataclasses import dataclass
from typing import List
from BaseClasses import ItemClassification

from ..strings.items import GenericItem, UniqueItem, Alchemy, Coins, Creation, Progressives, RareDrops, \
    Voucher, Trap, Switch, Door, CustomItem, Upgrade, SpookyItem, Stat
from ..strings.weapons import Weapon, SpookyWeapon
from ..strings.spells import Spell, MobSpell, SpookySpell, CrimpusSpell


@dataclass(frozen=True)
class LunacidItemData:
    code: int
    name: str
    classification: ItemClassification

    def __repr__(self):
        return f"{self.code} {self.name} (Classification: {self.classification})"


all_items: List[LunacidItemData] = []


def create_item(code: int, name: str, classification: ItemClassification):
    item = LunacidItemData(code, name, classification)
    all_items.append(item)

    return item

# ID - Classification Data


# Uses a structure of BASE ITEM + type offset + pseudo value.  The base item ID will eventually be deprecated in favor of starting at 1.
ITEM_CODE_START = 0
base_start_id = 0

core_items = [
    create_item(ITEM_CODE_START + base_start_id + 1, Creation.health_vial, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 2, Creation.mana_vial, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 3, Creation.antidote, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 4, GenericItem.blood_wine, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 5, Creation.crystal_shard, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 6, UniqueItem.ocean_elixir, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 7, UniqueItem.earth_elixir, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 8, Creation.poison_throwing_knife, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 9, UniqueItem.black_book, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 10, Creation.holy_water, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 11, Creation.fairy_moss, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 12, GenericItem.light_urn, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 13, Alchemy.ashes, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 14, GenericItem.cloth_bandage, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 15, Creation.moonlight_vial, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 16, Creation.spectral_candle, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 17, GenericItem.dark_urn, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 18, Creation.wisp_heart, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 19, Creation.staff_of_osiris, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 20, UniqueItem.white_tape, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 21, UniqueItem.vhs_tape, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 22, UniqueItem.corrupted_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 23, UniqueItem.skull_of_josiah, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 24, Progressives.vampiric_symbol, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 27, UniqueItem.crystal_lantern, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 28, UniqueItem.terminus_prison_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 29, UniqueItem.enchanted_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 30, UniqueItem.survey_banner, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 31, Alchemy.ectoplasm, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 32, Alchemy.snowflake_obsidian, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 33, Alchemy.moon_petal, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 34, Alchemy.fractured_life, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 35, Alchemy.fractured_death, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 36, Alchemy.broken_sword, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 37, UniqueItem.water_talisman, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 38, UniqueItem.earth_talisman, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 39, Coins.strange_coin, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 40, UniqueItem.oil_lantern, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 41, Creation.bomb, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 42, Creation.poison_urn, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 43, Coins.silver, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 44, UniqueItem.skeleton_egg, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 45, UniqueItem.dried_rat, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 46, UniqueItem.dusty_crystal_orb, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 47, UniqueItem.skeleton_rattle, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 48, RareDrops.shrimp, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 49, RareDrops.angel_feather, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 50, Alchemy.fire_opal, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 51, Alchemy.lotus_seed_pod, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 52, Alchemy.onyx, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 53, Alchemy.destroying_angel_mushroom, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 54, Alchemy.ocean_bone_shard, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 55, Alchemy.ocean_bone_shell, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 56, Alchemy.yellow_morel, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 57, Alchemy.bloodweed, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 58, Alchemy.opal, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 59, Alchemy.obsidian, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 60, Alchemy.ikurrilb_root, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 61, RareDrops.fools_gold, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 62, Voucher.sheryl_initial_voucher, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 63, Voucher.sheryl_golden_voucher, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 64, Voucher.sheryl_dreamer_voucher, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 65, Voucher.patchouli_simp_discount, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 66, Alchemy.fiddlehead, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 67, Alchemy.fire_coral, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 68, Alchemy.bones, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 69, Alchemy.vampiric_ashes, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 70, Creation.throwing_knife, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 71, CustomItem.experience, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 72, Upgrade.drop_chance, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 73, CustomItem.bestial_mastery, ItemClassification.useful),
    create_item(ITEM_CODE_START + base_start_id + 74, GenericItem.nothing, ItemClassification.filler),
    create_item(ITEM_CODE_START + base_start_id + 75, UniqueItem.vampiric_symbol_w, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 76, UniqueItem.vampiric_symbol_a, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 77, UniqueItem.vampiric_symbol_e, ItemClassification.progression),
    create_item(ITEM_CODE_START + base_start_id + 78, GenericItem.demi_gift, ItemClassification.filler),
    ]

trap_start_id = 100

trap_items = [
    create_item(ITEM_CODE_START + trap_start_id + 1, Trap.health_viai, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 2, Trap.poison_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 3, Trap.blindness_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 4, Trap.slowness_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 5, Trap.mana_drain_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 6, Trap.xp_drain_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 7, Trap.curse_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 8, Trap.bleed_trap, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 9, Trap.rat, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 10, Trap.timeout, ItemClassification.trap),
    create_item(ITEM_CODE_START + trap_start_id + 11, GenericItem.patchouli_gift, ItemClassification.trap),
]

all_traps = {trap.name: trap for trap in trap_items}

weapon_start_id = 150
base_weapons = [
    create_item(ITEM_CODE_START + weapon_start_id + 1, Weapon.axe_of_harming, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 2, Weapon.battle_axe, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 3, Weapon.blade_of_jusztina, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 4, Weapon.blade_of_ophelia, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 5, Weapon.blessed_wind, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 6, Weapon.broken_hilt, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 7, Weapon.broken_lance, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 8, Weapon.corrupted_dagger, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 9, Weapon.dark_rapier, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 10, Weapon.elfen_bow, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 11, Weapon.elfen_sword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 12, Weapon.fishing_spear, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 13, Weapon.marauder_black_flail, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 14, Weapon.halberd, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 15, Weapon.iron_claw, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 16, Weapon.moonlight, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 17, Weapon.obsidian_seal, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 18, Weapon.replica_sword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 19, Weapon.ritual_dagger, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 20, Weapon.serpent_fang, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 21, Weapon.shadow_blade, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 22, Weapon.steel_spear, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 23, Weapon.stone_club, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 24, Weapon.torch, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 25, Weapon.twisted_staff, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 26, Weapon.vampire_hunter_sword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 27, Weapon.wand_of_power, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 28, Weapon.wolfram_greatsword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 29, Weapon.wooden_shield, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 30, Weapon.crossbow,  ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 31, Weapon.steel_needle, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 32, Weapon.lucid_blade, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 33, Weapon.hammer_of_cruelty, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 34, Weapon.thorn, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 35, Weapon.ghost_sword, ItemClassification.useful),
]

shop_weapons = [
    create_item(ITEM_CODE_START + weapon_start_id + 36, Weapon.jotunn_slayer, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 37, Weapon.rapier, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 38, Weapon.privateer_musket, ItemClassification.progression),
]

drop_weapons = [
    create_item(ITEM_CODE_START + weapon_start_id + 39, Weapon.rusted_sword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 40, Weapon.ice_sickle, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 41, Weapon.skeleton_axe, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 42, Weapon.cursed_blade, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 43, Weapon.brittle_arming_sword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 44, Weapon.obsidian_cursebrand, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 45, Weapon.obsidian_poisonguard, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 46, Weapon.golden_kopesh, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 47, Weapon.golden_sickle, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 48, Weapon.jailor_candle, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 49, Weapon.sucsarian_dagger, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 50, Weapon.sucsarian_spear, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 51, Weapon.lyrian_longsword, ItemClassification.useful),
]

quench_weapons = [
    create_item(ITEM_CODE_START + weapon_start_id + 52, Weapon.lyrian_greatsword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 53, Weapon.dark_greatsword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 54, Weapon.shining_blade, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 55, Weapon.poison_claw, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 56, Weapon.iron_club, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 57, Weapon.iron_torch, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 58, Weapon.fire_sword, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 59, Weapon.steel_lance, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 60, Weapon.double_crossbow, ItemClassification.progression),
    create_item(ITEM_CODE_START + weapon_start_id + 61, Weapon.death_scythe, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 62, Weapon.elfen_longsword, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 63, Weapon.steel_claw, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 64, Weapon.steel_club, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 65, Weapon.saint_ishii, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 66, Weapon.silver_rapier, ItemClassification.useful),
    create_item(ITEM_CODE_START + weapon_start_id + 67, Weapon.heritage_sword, ItemClassification.useful),
]

alchemy_weapons = [
    create_item(ITEM_CODE_START + weapon_start_id + 68, Weapon.limbo, ItemClassification.useful),
]

spell_start_id = 250
base_spells = [
    create_item(ITEM_CODE_START + spell_start_id + 1, Spell.barrier, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 2, Spell.bestial_communion, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 3, Spell.blood_drain, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 4, Spell.blood_strike, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 5, Spell.blue_flame_arc, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 6, Spell.coffin, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 7, Spell.corpse_transformation, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 8, Spell.earth_strike, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 9, Spell.earth_thorn, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 10, Spell.fire_worm, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 11, Spell.flame_flare, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 12, Spell.flame_spear, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 13, Spell.ghost_light, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 14, Spell.holy_warmth, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 15, Spell.icarian_flight, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 16, Spell.ice_spear, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 17, Spell.ice_tear, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 18, Spell.ignis_calor, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 19, Spell.lava_chasm, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 20, Spell.light_reveal, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 21, Spell.lightning, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 22, Spell.lithomancy, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 23, Spell.moon_beam, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 24, Spell.poison_mist, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 25, Spell.rock_bridge, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 26, Spell.slime_orb, ItemClassification.useful),
    # create_item(ITEM_CODE_START + spell_start_id + 27, Spell.spirit_warp, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 28, Spell.summon_fairy, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 29, Spell.summon_ice_sword, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 30, Spell.wind_dash, ItemClassification.progression),
    create_item(ITEM_CODE_START + spell_start_id + 31, Spell.wind_slicer, ItemClassification.useful),
]

drop_spells = [
    create_item(ITEM_CODE_START + spell_start_id + 33, MobSpell.summon_snail, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 34, MobSpell.dark_skull, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 35, MobSpell.summon_kodama, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 36, MobSpell.tornado, ItemClassification.useful),
    create_item(ITEM_CODE_START + spell_start_id + 37, MobSpell.quick_stride, ItemClassification.useful),
]

switch_start_id = 300
switches = [
    create_item(ITEM_CODE_START + switch_start_id + 1, Switch.hollow_basin_switch_near_demi, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 2, Switch.temple_switch, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 3, Switch.fetid_mire_switch, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 4, Switch.tomb_switches, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 5, Switch.tomb_light_switches, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 6, Switch.archives_switch, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 7, Switch.archives_elevator_switches, ItemClassification.progression),
    create_item(ITEM_CODE_START + switch_start_id + 8, Switch.ballroom_switch, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 9, Switch.grotto_valves_switches, ItemClassification.progression),
    create_item(ITEM_CODE_START + switch_start_id + 10, Switch.grotto_switches, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 11, Switch.prison_shortcut_switch, ItemClassification.progression),
    create_item(ITEM_CODE_START + switch_start_id + 12, Switch.prison_arena_switch, ItemClassification.progression),
    create_item(ITEM_CODE_START + switch_start_id + 13, Switch.arena_water_switch, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 14, Switch.arena_earth_switch, ItemClassification.useful),
    create_item(ITEM_CODE_START + switch_start_id + 15, Switch.ash_switch, ItemClassification.useful),
]

door_start_id = 350
doors = [
    create_item(ITEM_CODE_START + door_start_id + 1, Door.basin_broken_steps, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 2, Door.basin_rickety_bridge, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 3, Door.basin_temple_sewers, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 4, Door.forest_door_in_trees, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 5, Door.forest_patchouli, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 6, Door.sea_westward, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 7, Door.sea_eastward, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 8, Door.sea_double_doors, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 9, Door.archives_sealed_door, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 10, Door.chasm_surface_door, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 11, Door.ballroom_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 12, Door.throne_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 13, Door.prison_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 14, Door.forlorn_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 15, Door.burning_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 16, Door.ash_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 17, Door.sucsarian_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 18, Door.sleeper_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 19, Door.ballroom_rooms_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 20, Door.tower_key, ItemClassification.progression | ItemClassification.useful),
    create_item(ITEM_CODE_START + door_start_id + 21, Door.musical_key, ItemClassification.progression | ItemClassification.useful),
]

holiday_start_id = 400
holiday = [
    create_item(ITEM_CODE_START + holiday_start_id + 1, SpookyItem.soul_candy, ItemClassification.progression),
    create_item(ITEM_CODE_START + holiday_start_id + 2, SpookySpell.pumpkin_pop, ItemClassification.useful),
    create_item(ITEM_CODE_START + holiday_start_id + 3, SpookyWeapon.cavalry_saber, ItemClassification.useful),
    create_item(ITEM_CODE_START + holiday_start_id + 4, CrimpusSpell.jingle_bells, ItemClassification.useful),
    create_item(ITEM_CODE_START + holiday_start_id + 5, Trap.eggnog, ItemClassification.trap),
    create_item(ITEM_CODE_START + holiday_start_id + 6, Trap.coal, ItemClassification.trap)
]

extra_start_id = 450
extras = [
    create_item(ITEM_CODE_START + extra_start_id + 1, Upgrade.flippers, ItemClassification.progression),
    create_item(ITEM_CODE_START + extra_start_id + 2, Upgrade.boots_of_leaping, ItemClassification.progression),
    create_item(ITEM_CODE_START + extra_start_id + 3, Upgrade.earring_of_speed, ItemClassification.progression),
    create_item(ITEM_CODE_START + extra_start_id + 4, CustomItem.lucky_bangle, ItemClassification.progression | ItemClassification.useful)
]

# Item Groups

# Starting Weapons
starting_weapon = [
    Weapon.replica_sword, Weapon.battle_axe, Weapon.stone_club,
    Weapon.ritual_dagger, Weapon.torch, Weapon.steel_spear,
    Weapon.wooden_shield, Weapon.broken_hilt, Weapon.elfen_bow,
    Weapon.elfen_sword, Spell.flame_spear, Spell.ice_spear,
    Spell.wind_slicer, Spell.slime_orb, Spell.earth_strike
    ]
shop_starting_weapons = [
    Weapon.crossbow, Weapon.rapier, Weapon.steel_needle
]
drop_starting_weapons = [
    Weapon.skeleton_axe, Weapon.rusted_sword, Weapon.ice_sickle,
    MobSpell.dark_skull
]

quench_starting_weapons = [
    Weapon.heritage_sword, Weapon.iron_torch, Weapon.iron_club, Weapon.steel_club, Weapon.elfen_longsword, Weapon.fire_sword
]

# Item Data used for generation
base_unique_items = [
    UniqueItem.vhs_tape, UniqueItem.corrupted_key, UniqueItem.white_tape,
    UniqueItem.skull_of_josiah, Alchemy.fractured_life, UniqueItem.earth_talisman,
    UniqueItem.enchanted_key, UniqueItem.terminus_prison_key, Alchemy.broken_sword,
    Alchemy.fractured_death, UniqueItem.water_talisman, UniqueItem.skeleton_egg,
    UniqueItem.dried_rat, UniqueItem.dusty_crystal_orb, UniqueItem.skeleton_rattle,
    UniqueItem.crystal_lantern
]

base_special_item_counts = {
    UniqueItem.ocean_elixir: 7,
    UniqueItem.earth_elixir: 10,
    UniqueItem.black_book: 3,
}

shop_unique_items = [
    UniqueItem.oil_lantern, UniqueItem.enchanted_key
]

shop_item_count = {
    UniqueItem.ocean_elixir: 2
}

# Items for Rules
blood_spells = [Spell.blood_drain, Spell.blood_strike]

base_light_sources = [
    UniqueItem.crystal_lantern, Weapon.torch, Spell.ghost_light, Weapon.broken_hilt,
    Weapon.twisted_staff, Weapon.moonlight, Spell.flame_flare, Weapon.wand_of_power
]

shop_light_sources = [
    UniqueItem.oil_lantern
]

drop_light_sources = [
    Weapon.jailor_candle
]

quench_light_sources = [
    Weapon.fire_sword, Weapon.iron_torch, Weapon.shining_blade
]

drop_spell_names = [drop.name for drop in drop_spells]


all_item_data_by_name = {item.name: item for item in all_items}
all_filler_items = [item.name for item in all_items if item.classification == ItemClassification.filler]
all_basic_materials = [item.name for item in all_items if item.name in Alchemy.all_basic_items]

default_filler_weights = {
    Coins.silver: 8,
    Creation.health_vial: 3,
    Creation.mana_vial: 3,
    Creation.antidote: 3,
    GenericItem.blood_wine: 3,
    Creation.crystal_shard: 3,
    Creation.holy_water: 3,
    Creation.fairy_moss: 3,
    GenericItem.cloth_bandage: 3,
    Creation.throwing_knife: 3,
    Creation.poison_throwing_knife: 3,
    Creation.poison_urn: 2,
    GenericItem.light_urn: 2,
    Creation.moonlight_vial: 2,
    Creation.spectral_candle: 2,
    GenericItem.dark_urn: 2,
    Creation.wisp_heart: 2,
    Creation.staff_of_osiris: 2,
    UniqueItem.survey_banner: 2,
    RareDrops.shrimp: 2,
    Alchemy.ashes: 2,
    Alchemy.ectoplasm: 2,
    Alchemy.snowflake_obsidian: 2,
    Alchemy.moon_petal: 2,
    Alchemy.fire_opal: 2,
    Alchemy.lotus_seed_pod: 2,
    Alchemy.onyx: 2,
    Alchemy.destroying_angel_mushroom: 2,
    Alchemy.ocean_bone_shard: 2,
    Alchemy.ocean_bone_shell: 2,
    Alchemy.yellow_morel: 2,
    Alchemy.bloodweed: 2,
    Alchemy.opal: 2,
    Alchemy.obsidian: 2,
    Alchemy.ikurrilb_root: 2,
    RareDrops.fools_gold: 2,
    Alchemy.fiddlehead: 2,
    Alchemy.fire_coral: 2,
    Alchemy.bones: 2,
    Alchemy.vampiric_ashes: 2,
    CustomItem.experience: 1,
    Creation.bomb: 1,
    RareDrops.angel_feather: 1,
    GenericItem.nothing: 0,
    GenericItem.demi_gift: 0,
}

default_trap_weights = {
    Trap.health_viai: 4,
    Trap.blindness_trap: 2,
    Trap.slowness_trap: 2,
    Trap.mana_drain_trap: 2,
    Trap.xp_drain_trap: 2,
    Trap.curse_trap: 2,
    Trap.poison_trap: 2,
    Trap.bleed_trap: 2,
    Trap.rat: 1,
    Trap.timeout: 0,
    Trap.eggnog: 4,
    Trap.coal: 4,
    GenericItem.patchouli_gift: 0,
}

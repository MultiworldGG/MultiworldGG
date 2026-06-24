import dataclasses

from BaseClasses import CollectionState
from typing import Dict, List, TYPE_CHECKING, Any, override

from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from rule_builder.rules import False_, True_, Rule, HasAll, HasAny, CanReachRegion, Has, CanReachLocation
from .data.enemy_positions import immovable_enemies
from .strings.enemies import Enemy
from .strings.properties import Elements

from .data.spell_info import ranged_spells, support_spells
from .data.weapon_info import ranged_weapons
from .data.item_data import base_light_sources, shop_light_sources, blood_spells, drop_light_sources, quench_light_sources
from .data.enemy_data import all_enemy_data_by_name
from .data.plant_data import all_alchemy_plant_data
from .Options import DoorLocks, SwitchLocks, SecretDoorLock, Levelsanity
from .strings.custom_features import JumpHeight, Glitch
from .strings.regions_entrances import LunacidEntrance, LunacidRegion, region_to_level_value
from .strings.spells import Spell, MobSpell
from .strings.items import UniqueItem, Progressives, Switch, Alchemy, Door, Coins, Voucher, SpookyItem, CustomItem
from .strings.locations import BaseLocation, ShopLocation, all_drops_by_enemy, DropLocation, Quench, AlchemyLocation, SpookyLocation, LevelLocation, LoreLocation, \
    GrassLocation, BreakLocation
from .strings.weapons import Weapon, SpookyWeapon
from .strings.options import Endings

if TYPE_CHECKING:
    from . import LunacidWorld


class LunacidRules:
    player: int
    world: "LunacidWorld"
    entrance_rules: Dict[str, Rule[Any]]
    location_rules: Dict[str, Rule[Any]]
    lightless: Rule[Any]
    rock_bridge: Rule[Any]
    surface: Rule[Any]
    barrier: Rule[Any]
    not_shopsanity: Rule[Any]

    def __init__(self, world: "LunacidWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options
        self.level = world.level
        self.lightless = False_()
        if "Lightless" in self.world.options.tricks_and_glitches.value:
            self.lightless = True_()
        self.rock_bridge = False_()
        if "Rock Bridge Skip" in self.world.options.tricks_and_glitches.value:
            self.rock_bridge = True_()
        self.surface = False_()
        if "Early Surface" in self.world.options.tricks_and_glitches.value:
            self.surface = True_()
        self.barrier = False_()
        if "Barrier Skip" in self.world.options.tricks_and_glitches.value:
            self.barrier = True_()
        self.not_shopsanity = True_()
        if self.world.options.shopsanity:
            self.not_shopsanity = False_()

        self.entrance_rules = {
            LunacidEntrance.basin_to_temple_path: self.not_shopsanity | self.has_keys_for_basin_or_canopy(),
            LunacidEntrance.basin_to_archives_2f: self.has_door_key(Door.basin_broken_steps) & self.can_jump_given_height(JumpHeight.low),
            LunacidEntrance.basin_to_surface: self.can_jump_given_height(JumpHeight.high) | self.surface,

            LunacidEntrance.temple_path_to_basin: self.not_shopsanity | self.has_keys_for_basin_or_canopy(),
            LunacidEntrance.temple_path_to_temple_front: self.has_light_source(),

            LunacidEntrance.temple_front_to_temple_back: self.has_switch_key(Switch.temple_switch),
            LunacidEntrance.temple_front_to_temple_sewers: self.has_switch_key(Switch.temple_switch),
            LunacidEntrance.temple_front_to_temple_front_secret: self.has_crystal_orb() & self.can_jump_given_height(JumpHeight.high),
            LunacidEntrance.temple_front_to_locked_spot: self.has_switch_key(Switch.temple_switch),

            LunacidEntrance.temple_sewers_to_mire: self.has_door_key(Door.basin_temple_sewers),
            LunacidEntrance.temple_sewers_to_sewers_secret: self.has_crystal_orb(),


            LunacidEntrance.temple_back_to_temple_secret: self.has_crystal_orb(),

            LunacidEntrance.temple_lower_to_temple_back: self.has_light_source(),

            LunacidEntrance.temple_lower_to_forest: self.has_door_key(Door.basin_rickety_bridge),

            LunacidEntrance.rest_to_surface: self.can_jump_given_height(JumpHeight.high) | self.surface,

            LunacidEntrance.archives_2f_to_basin: self.has_door_key(Door.basin_broken_steps),
            LunacidEntrance.archives_2f_to_2f_secret: self.has_crystal_orb(),

            LunacidEntrance.archives_2f_to_3f: self.can_jump_given_height(JumpHeight.high) | self.has_switch_key(Switch.archives_elevator_switches),
            LunacidEntrance.archives_1f_front_to_3f: self.can_jump_given_height(JumpHeight.high) | self.has_switch_key(Switch.archives_elevator_switches),
            LunacidEntrance.archives_1f_back_to_2f: self.can_jump_given_height(JumpHeight.high) | self.has_switch_key(Switch.archives_elevator_switches),

            LunacidEntrance.archives_3f_to_secret: self.has_crystal_orb(),
            LunacidEntrance.archives_1f_to_1f_secret: self.has_crystal_orb(),
            LunacidEntrance.archives_3f_to_vampire: Has(Progressives.vampiric_symbol, 2) | Has(UniqueItem.vampiric_symbol_a),

            LunacidEntrance.archives_vampire_to_3f: Has(Progressives.vampiric_symbol, 2) | Has(UniqueItem.vampiric_symbol_a),
            LunacidEntrance.archives_vampire_to_chasm: self.has_door_key(Door.archives_sealed_door),

            LunacidEntrance.chasm_to_archives_vampire: self.has_door_key(Door.archives_sealed_door),
            LunacidEntrance.chasm_to_chasm_upper: self.can_jump_given_height(JumpHeight.low),
            LunacidEntrance.chasm_upper_to_lower: self.can_jump_given_height(JumpHeight.high),

            LunacidEntrance.chasm_upper_to_surface: self.has_door_key(Door.chasm_surface_door),
            LunacidEntrance.chasm_upper_to_secret: self.has_crystal_orb(),

            LunacidEntrance.surface_to_chasm_upper: self.has_door_key(Door.chasm_surface_door),

            LunacidEntrance.mire_to_temple_sewers: self.has_door_key(Door.basin_temple_sewers),
            LunacidEntrance.mire_to_mire_upper_secret: self.has_crystal_orb() | self.can_jump_given_height(JumpHeight.high),
            LunacidEntrance.mire_to_mire_lower_secrets: self.has_crystal_orb(),
            LunacidEntrance.mire_to_sea: self.has_door_key(Door.sea_westward),

            LunacidEntrance.forest_to_temple_lower: self.has_door_key(Door.basin_rickety_bridge),
            LunacidEntrance.forest_to_canopy_path: self.has_keys_for_basin_or_canopy(),

            LunacidEntrance.canopy_path_to_forest: self.has_keys_for_basin_or_canopy(),
            LunacidEntrance.canopy_path_to_canopy: self.has_door_key(Door.forest_door_in_trees),

            LunacidEntrance.lower_forest_secret: self.has_crystal_orb(),

            LunacidEntrance.tomb_to_lower_forest: self.can_jump_given_height(JumpHeight.high),
            LunacidEntrance.forest_tomb_to_accursed_tomb: self.has_door_key(Door.forest_patchouli) & self.has_light_source(),

            LunacidEntrance.sea_to_mire: self.has_door_key(Door.sea_westward),
            LunacidEntrance.sea_to_castle_entrance: self.has_door_key(Door.sea_double_doors),
            LunacidEntrance.sea_to_accursed_tomb: self.has_door_key(Door.sea_eastward) & self.has_light_source(),

            LunacidEntrance.accursed_tomb_to_forest_tomb: self.has_door_key(Door.forest_patchouli),

            LunacidEntrance.accursed_tomb_to_platform: self.can_jump_given_height(JumpHeight.high),
            LunacidEntrance.accursed_well_to_accursed: self.has_light_source(),
            LunacidEntrance.accursed_to_vampire: self.has_element_access(Elements.light_options) | Has(Weapon.wand_of_power),
            LunacidEntrance.accursed_to_mausoleum: self.has_element_access(Elements.light_options) | Has(Weapon.wand_of_power),
            LunacidEntrance.accursed_tomb_to_sea: self.has_door_key(Door.sea_eastward),
            LunacidEntrance.accursed_tomb_to_secrets: self.has_crystal_orb(),
            LunacidEntrance.vampire_tomb_to_secret: self.has_crystal_orb(),
            LunacidEntrance.accursed_to_accursed_well: self.can_jump_given_height(JumpHeight.high),

            LunacidEntrance.castle_entrance_to_sea: self.has_door_key(Door.sea_double_doors),
            LunacidEntrance.castle_to_cattle: self.is_vampire() | self.has_blood_spell_access() | self.can_rock_bridge_skip(),
            LunacidEntrance.castle_entrance_to_main_halls: self.is_vampire() | Has(Progressives.vampiric_symbol, 1) | self.can_rock_bridge_skip() |
                                                                         Has(UniqueItem.vampiric_symbol_w),

            LunacidEntrance.cattle_to_deeper: self.is_vampire() | self.has_blood_spell_access(),
            LunacidEntrance.cattle_to_secret: self.has_crystal_orb(),

            LunacidEntrance.castle_main_halls_to_entrance: self.is_vampire() | Has(Progressives.vampiric_symbol, 1) |
                                                                         Has(UniqueItem.vampiric_symbol_w),
            LunacidEntrance.castle_main_halls_to_queen_path: Has(Progressives.vampiric_symbol, 3) | Has(UniqueItem.vampiric_symbol_e),
            LunacidEntrance.castle_main_halls_to_upstairs: Has(Progressives.vampiric_symbol, 2) | Has(UniqueItem.vampiric_symbol_a),

            LunacidEntrance.castle_upstairs_to_main_halls: Has(Progressives.vampiric_symbol, 2) | Has(UniqueItem.vampiric_symbol_a),
            LunacidEntrance.castle_upstairs_to_tape_room: self.has_crystal_orb(),
            LunacidEntrance.castle_upstairs_to_forbidden: CanReachRegion(LunacidRegion.castle_le_fanu_entrance) &
                                                                        (self.has_ranged_element_access(
                        [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison,
                         Elements.ice_and_poison]) | self.can_melee_window()),
            LunacidEntrance.castle_upstairs_to_queen_rest: Has(Progressives.vampiric_symbol, 3) | Has(UniqueItem.vampiric_symbol_e),

            LunacidEntrance.castle_cattle_back_to_boiling_grotto: self.has_door_key(Door.burning_key),

            LunacidEntrance.castle_queen_path_to_main_halls: Has(Progressives.vampiric_symbol, 3) | Has(UniqueItem.vampiric_symbol_e),
            LunacidEntrance.castle_queen_path_to_throne_room: self.has_door_key(Door.throne_key),

            LunacidEntrance.rock_castle_le_fanu_cattle_deeper_skip: self.can_rock_bridge_skip(),
            LunacidEntrance.rock_castle_le_fanu_queen_door: self.can_rock_bridge_skip(),
            LunacidEntrance.rock_castle_le_fanu_past_door: self.can_rock_bridge_skip(),
            LunacidEntrance.rock_castle_le_fanu_secret_skips: self.can_rock_bridge_skip(),
            LunacidEntrance.rock_castle_le_fanu_upper_bridge: self.can_rock_bridge_skip(),
            LunacidEntrance.rock_castle_le_fanu_spell_skip: self.can_rock_bridge_skip(),

            LunacidEntrance.throne_room_to_prison: self.has_door_key(Door.prison_key),
            LunacidEntrance.throne_from_main_to_front: self.can_defeat_the_prince(),
            LunacidEntrance.throne_from_main_to_back: self.can_defeat_the_prince(),
            LunacidEntrance.throne_room_to_castle_queen_path: self.has_door_key(Door.throne_key),

            LunacidEntrance.castle_forbidden_to_upstairs: CanReachRegion(LunacidRegion.castle_le_fanu_entrance) &
                                                                        (self.has_ranged_element_access(
                        [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison,
                         Elements.ice_and_poison]) | self.can_melee_window()),
            LunacidEntrance.castle_forbidden_to_sealed_ballroom: self.has_door_key(Door.ballroom_key),

            LunacidEntrance.sealed_ballroom_to_forbidden_entry: self.has_door_key(Door.ballroom_key),
            LunacidEntrance.sealed_ballroom_to_rooms: self.has_door_key(Door.ballroom_rooms_key),
            LunacidEntrance.sealed_ballroom_to_secrets: self.has_crystal_orb(),

            LunacidEntrance.sealed_ballroom_rooms_to_cave: self.has_crystal_orb(),
            LunacidEntrance.sealed_ballroom_secret_room: self.has_door_key(Door.ballroom_rooms_key),

            LunacidEntrance.boiling_grotto_to_castle_cattle_back: self.has_door_key(Door.burning_key),
            LunacidEntrance.boiling_grotto_to_secret: self.has_crystal_orb(),
            LunacidEntrance.boiling_grotto_to_coffin_room: self.has_crystal_orb(),
            LunacidEntrance.boiling_grotto_to_sand_temple: self.has_switch_key(Switch.grotto_valves_switches),

            LunacidEntrance.boiling_grotto_coffin_room_to_boiling_grotto: self.has_crystal_orb(),

            LunacidEntrance.sand_temple_to_deep_snake_pit: self.can_jump_given_height(JumpHeight.high) |
                                                                         Has(Spell.wind_dash),
            LunacidEntrance.sand_temple_secret_snake_pit_escape: self.has_crystal_orb() |
                                                                               self.can_jump_given_height(JumpHeight.high),

            LunacidEntrance.abyss_to_5f: self.has_door_key(Door.tower_key),
            LunacidEntrance.abyss_5f_to_10f: self.has_ranged_element_access(Elements.all_elements) | HasAny(*tuple(ranged_weapons)),
            LunacidEntrance.abyss_15f_to_20f: self.has_light_source() & self.can_level_reasonably(),

            LunacidEntrance.terminus_prison_1f_to_arena: CanReachRegion(LunacidRegion.terminus_prison_4f) &
                                                                       self.has_switch_key(Switch.prison_arena_switch) &
                                                                       self.has_door_key(Door.forlorn_key),
            LunacidEntrance.terminus_prison_1f_to_secrets: self.has_crystal_orb(),
            LunacidEntrance.terminus_prison_1f_to_2f: self.can_jump_given_height(JumpHeight.medium),
            LunacidEntrance.terminus_prison_1f_to_3f: self.has_switch_key(Switch.prison_shortcut_switch),
            LunacidEntrance.terminus_prison_2f_doors: Has(UniqueItem.terminus_prison_key),
            LunacidEntrance.terminus_prison_2f_to_3f: self.can_jump_given_height(JumpHeight.high),
            LunacidEntrance.terminus_prison_2f_to_1f: self.has_light_source(),
            LunacidEntrance.terminus_prison_3f_doors: Has(UniqueItem.terminus_prison_key),
            LunacidEntrance.terminus_prison_3f_to_4f: Has(UniqueItem.terminus_prison_key),
            LunacidEntrance.terminus_prison_3f_to_throne_room: self.has_door_key(Door.prison_key),
            LunacidEntrance.terminus_prison_4f_secret_walls: self.has_crystal_orb(),
            LunacidEntrance.terminus_prison_basement_to_ash: self.has_door_key(Door.ash_key),

            LunacidEntrance.labyrinth_of_ash_to_terminus_prison: self.has_door_key(Door.ash_key) & self.has_light_source(),
            LunacidEntrance.labyrinth_of_ash_to_interior: self.has_door_key(Door.musical_key),
            LunacidEntrance.labyrinth_of_ash_to_holy_seat: self.has_door_key(Door.musical_key),
            LunacidEntrance.labyrinth_interior_to_secret: self.has_crystal_orb(),
            LunacidEntrance.holy_seat_to_secret: self.has_crystal_orb(),

            LunacidEntrance.forlorn_arena_to_terminus_prison: self.has_door_key(Door.forlorn_key) & self.has_light_source(),
            LunacidEntrance.forlorn_arena_to_path_to_sucsarius: Has(UniqueItem.water_talisman) &
                                                                              Has(UniqueItem.earth_talisman) | self.barrier,
            LunacidEntrance.forlorn_arena_to_water_temple: self.can_jump_given_height(JumpHeight.high) |
                                                                         Has(Spell.wind_dash),
            LunacidEntrance.temple_of_earth_to_secrets: self.has_crystal_orb(),
            LunacidEntrance.temple_of_water_lower_to_secrets: self.has_crystal_orb(),
            LunacidEntrance.forlorn_path_to_chamber: self.has_door_key(Door.sucsarian_key),

            LunacidEntrance.chamber_to_grave: self.has_door_key(Door.sleeper_key) & Has(Weapon.lucid_blade),
        }

        self.location_rules = {
            "Throne of Prince Crilall Fanu": self.can_defeat_the_prince(),
            BaseLocation.wings_rest_demi_orb: CanReachRegion(LunacidRegion.grave_of_the_sleeper),
            BaseLocation.wings_rest_ocean_elixir: self.can_jump_given_height(JumpHeight.low),
            BaseLocation.temple_small_pillar: self.can_jump_given_height(JumpHeight.low) | Has(Spell.wind_dash),
            BaseLocation.temple_blood_altar: self.has_blood_spell_access(),
            BaseLocation.temple_sewer_puzzle: Has(UniqueItem.vhs_tape) &
                                                            CanReachRegion(LunacidRegion.vampire_tomb_tape_room) &
                                                            self.has_ranged_element_access(Elements.all_elements),
            BaseLocation.archives_daedalus_one: Has(UniqueItem.black_book, 1),
            BaseLocation.archives_daedalus_two: Has(UniqueItem.black_book, 2),
            BaseLocation.archives_daedalus_third: Has(UniqueItem.black_book, 3),
            BaseLocation.sea_pillar: HasAny(*(Spell.icarian_flight, Spell.rock_bridge,)),
            BaseLocation.chasm_hidden_chest: self.has_crystal_orb(),
            BaseLocation.chasm_invisible_cliffside: HasAny(*(Spell.coffin, Spell.icarian_flight,)),
            BaseLocation.catacombs_restore_vampire: self.has_blood_spell_access(),
            BaseLocation.mausoleum_upper_table: self.can_jump_given_height(JumpHeight.medium),
            BaseLocation.mausoleum_hidden_chest: self.has_crystal_orb(),
            BaseLocation.mausoleum_kill_death: HasAll(*(Alchemy.fractured_life, Alchemy.fractured_death, Alchemy.broken_sword,)),
            BaseLocation.corrupted_room: Has(UniqueItem.corrupted_key),
            BaseLocation.yosei_hanging_in_trees: HasAny(*tuple(ranged_weapons)),
            BaseLocation.yosei_hidden_chest: self.has_crystal_orb(),
            BaseLocation.yosei_room_defended_by_blood_plant: self.has_blood_spell_access(),
            BaseLocation.yosei_patchouli_quest: Has(UniqueItem.skull_of_josiah),
            BaseLocation.sea_kill_jotunn: self.can_buy_jotunn(),
            BaseLocation.yosei_blood_plant_insides: self.has_blood_spell_access(),
            BaseLocation.yosei_rusted_sword: self.has_blood_spell_access(),
            BaseLocation.castle_cell_center: self.has_element_access(Elements.fire),
            BaseLocation.castle_upper_floor_coffin_double: self.has_crystal_orb(),
            BaseLocation.throne_book: self.can_defeat_the_prince(),
            BaseLocation.grotto_slab_of_bridge: self.can_jump_given_height(JumpHeight.low),
            BaseLocation.grotto_hidden_chest: self.has_crystal_orb(),
            BaseLocation.grotto_triple_secret_chest: self.has_crystal_orb(),
            BaseLocation.sand_basement_snake_pit: self.has_crystal_orb(),
            BaseLocation.sand_hidden_sarcophagus: self.has_crystal_orb(),
            BaseLocation.sand_chest_overlooking_crypt: self.can_jump_given_height(JumpHeight.high),
            BaseLocation.arena_earth_earthen_temple: self.can_jump_given_height(JumpHeight.high),
            BaseLocation.arena_rock_parkour: self.can_jump_given_height(JumpHeight.low),
            BaseLocation.prison_b2_egg_resting_place: Has(UniqueItem.skeleton_egg),
            BaseLocation.prison_f1_hidden_cell: self.has_crystal_orb(),
            BaseLocation.prison_f1_hidden_debris_room: self.has_crystal_orb(),
            BaseLocation.prison_f4_hidden_beds: self.has_crystal_orb(),
            BaseLocation.prison_f4_maledictus_secret: self.has_crystal_orb(),
            BaseLocation.prison_f3_locked_left: Has(UniqueItem.terminus_prison_key),
            BaseLocation.prison_f3_locked_right: Has(UniqueItem.terminus_prison_key),
            BaseLocation.prison_f3_locked_south: Has(UniqueItem.terminus_prison_key),
            "Free Sir Hicket": Has(Spell.ignis_calor),
            BaseLocation.ash_path_maze: self.has_crystal_orb(),
            BaseLocation.ash_hidden_chest: self.has_crystal_orb(),

            # Shop Location Runes
            ShopLocation.buy_enchanted_key: Has(Voucher.sheryl_initial_voucher),
            ShopLocation.buy_steel_needle: Has(Voucher.sheryl_initial_voucher),
            ShopLocation.buy_crossbow: Has(Voucher.sheryl_initial_voucher),
            ShopLocation.buy_rapier: Has(Voucher.sheryl_initial_voucher),
            ShopLocation.buy_privateer_musket: self.can_purchase_item() & Has(Voucher.sheryl_golden_voucher),
            ShopLocation.buy_oil_lantern: self.can_purchase_item() & Has(Voucher.sheryl_golden_voucher),
            ShopLocation.buy_jotunn_slayer: CanReachLocation(BaseLocation.fate_lucid_blade) & Has(Voucher.sheryl_dreamer_voucher),
            ShopLocation.buy_ocean_elixir_patchouli: Has(Voucher.patchouli_simp_discount),

            # All Drop Location Rules Yikes
            DropLocation.snail_2c: self.can_reach_and_hurt_enemy(Enemy.snail),
            DropLocation.snail_10c: self.can_reach_and_hurt_enemy(Enemy.snail),
            DropLocation.snail_ocean: self.can_reach_and_hurt_enemy(Enemy.snail),
            DropLocation.snail: self.can_reach_and_hurt_enemy(Enemy.snail),
            DropLocation.milk_5c: self.can_reach_and_hurt_enemy(Enemy.milk_snail),
            DropLocation.milk_10c: self.can_reach_and_hurt_enemy(Enemy.milk_snail),
            DropLocation.milk_ocean: self.can_reach_and_hurt_enemy(Enemy.milk_snail),
            DropLocation.milk_snail: self.can_reach_and_hurt_enemy(Enemy.milk_snail),
            DropLocation.shulker_obsidian: self.can_reach_and_hurt_enemy(Enemy.shulker),
            DropLocation.shulker_onyx: self.can_reach_and_hurt_enemy(Enemy.shulker),
            DropLocation.mummy_knight_onyx: self.can_reach_and_hurt_enemy(Enemy.mummy_knight),
            DropLocation.mummy_knight_10c: self.can_reach_and_hurt_enemy(Enemy.mummy_knight),
            DropLocation.mummy_knight_5c: self.can_reach_and_hurt_enemy(Enemy.mummy_knight),
            DropLocation.mummy_knight: self.can_reach_and_hurt_enemy(Enemy.mummy_knight),
            DropLocation.mummy_mana_vial: self.can_reach_and_hurt_enemy(Enemy.mummy),
            DropLocation.mummy_onyx: self.can_reach_and_hurt_enemy(Enemy.mummy),
            DropLocation.mummy_2c: self.can_reach_and_hurt_enemy(Enemy.mummy),
            DropLocation.mummy_10c: self.can_reach_and_hurt_enemy(Enemy.mummy_knight),
            DropLocation.necronomicon_fire_opal: self.can_reach_and_hurt_enemy(Enemy.necronomicon),
            DropLocation.necronomicon_5c: self.can_reach_and_hurt_enemy(Enemy.necronomicon),
            DropLocation.necronomicon_10c: self.can_reach_and_hurt_enemy(Enemy.necronomicon),
            DropLocation.necronomicon_mana_vial: self.can_reach_and_hurt_enemy(Enemy.necronomicon),
            DropLocation.chimera_light_urn: self.can_reach_and_hurt_enemy(Enemy.chimera),
            DropLocation.chimera_holy_water: self.can_reach_and_hurt_enemy(Enemy.chimera),
            DropLocation.chimera_drop: self.can_reach_and_hurt_enemy(Enemy.chimera),
            DropLocation.enlightened_mana_vial: self.can_reach_and_hurt_enemy(Enemy.enlightened_one),
            DropLocation.enlightened_ocean_bone_shell: self.can_reach_and_hurt_enemy(Enemy.enlightened_one),
            DropLocation.slime_skeleton: self.can_reach_and_hurt_enemy(Enemy.slime_skeleton),
            DropLocation.skeleton_10c: self.can_reach_and_hurt_enemy(Enemy.skeleton) | self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon),
            DropLocation.skeleton_mana_vial: self.can_reach_and_hurt_enemy(Enemy.skeleton) | self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon),
            DropLocation.skeleton_onyx: self.can_reach_and_hurt_enemy(Enemy.skeleton) | self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon),
            DropLocation.skeleton_bones: self.can_reach_and_hurt_enemy(Enemy.skeleton) | self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon),
            DropLocation.skeleton_2c: self.can_reach_and_hurt_enemy(Enemy.skeleton),
            DropLocation.skeleton_spell: self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon),
            DropLocation.skeleton_weapon: self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon),
            DropLocation.rat_king_10c: self.can_reach_and_hurt_enemy(Enemy.rat_king),
            DropLocation.rat_king_lotus_seed: self.can_reach_and_hurt_enemy(Enemy.rat_king),
            DropLocation.rat: self.can_reach_and_hurt_enemy(Enemy.rat),
            DropLocation.kodama_drop: self.can_reach_and_hurt_enemy(Enemy.kodama),
            DropLocation.kodama_2c: self.can_reach_and_hurt_enemy(Enemy.kodama),
            DropLocation.kodama_10c: self.can_reach_and_hurt_enemy(Enemy.kodama),
            DropLocation.kodama_opal: self.can_reach_and_hurt_enemy(Enemy.kodama),
            DropLocation.yakul_10c: self.can_reach_and_hurt_enemy(Enemy.yakul),
            DropLocation.yakul_fire_opal: self.can_reach_and_hurt_enemy(Enemy.yakul),
            DropLocation.yakul_opal: self.can_reach_and_hurt_enemy(Enemy.yakul),
            DropLocation.yakul_health_vial: self.can_reach_and_hurt_enemy(Enemy.yakul),
            DropLocation.venus_10c: self.can_reach_and_hurt_enemy(Enemy.venus),
            DropLocation.venus_yellow_morel: self.can_reach_and_hurt_enemy(Enemy.venus),
            DropLocation.venus_dest_angel: self.can_reach_and_hurt_enemy(Enemy.venus),
            DropLocation.neptune_10c: self.can_reach_and_hurt_enemy(Enemy.neptune),
            DropLocation.neptune_yellow_morel: self.can_reach_and_hurt_enemy(Enemy.neptune),
            DropLocation.neptune_dest_angel: self.can_reach_and_hurt_enemy(Enemy.neptune),
            DropLocation.unilateralis_10c: self.can_reach_and_hurt_enemy(Enemy.unilateralis),
            DropLocation.unilateralis_yellow_morel: self.can_reach_and_hurt_enemy(Enemy.unilateralis),
            DropLocation.unilateralis_dest_angel: self.can_reach_and_hurt_enemy(Enemy.unilateralis),
            DropLocation.hemalith_health_vial: self.can_reach_and_hurt_enemy(Enemy.hemalith),
            DropLocation.hemalith_shrimp: self.can_reach_and_hurt_enemy(Enemy.hemalith),
            DropLocation.hemallith_bloodweed: self.can_reach_and_hurt_enemy(Enemy.hemalith),
            DropLocation.mi_go_ocean_bone_shell: self.can_reach_and_hurt_enemy(Enemy.mi_go),
            DropLocation.mi_go_10c: self.can_reach_and_hurt_enemy(Enemy.mi_go),
            DropLocation.mi_go_snowflake_obsidian: self.can_reach_and_hurt_enemy(Enemy.mi_go),
            DropLocation.mare_10c: self.can_reach_and_hurt_enemy(Enemy.mare),
            DropLocation.mare_obsidian: self.can_reach_and_hurt_enemy(Enemy.mare),
            DropLocation.mare_onyx: self.can_reach_and_hurt_enemy(Enemy.mare),
            DropLocation.painting_fire_opal: self.can_reach_and_hurt_enemy(Enemy.cursed_painting),
            DropLocation.painting_10c: self.can_reach_and_hurt_enemy(Enemy.cursed_painting),
            DropLocation.painting_mana_vial: self.can_reach_and_hurt_enemy(Enemy.cursed_painting),
            DropLocation.painting_20c: self.can_reach_and_hurt_enemy(Enemy.cursed_painting),
            DropLocation.phantom_10c: self.can_reach_and_hurt_enemy(Enemy.phantom),
            DropLocation.phantom_holy_water: self.can_reach_and_hurt_enemy(Enemy.phantom),
            DropLocation.phantom_moon_vial: self.can_reach_and_hurt_enemy(Enemy.phantom),
            DropLocation.phantom: self.can_reach_and_hurt_enemy(Enemy.phantom),
            DropLocation.phantom_ectoplasm: self.can_reach_and_hurt_enemy(Enemy.phantom),
            DropLocation.vampire_5c: self.can_reach_and_hurt_enemy(Enemy.vampire),
            DropLocation.vampire_vampiric_ashes: self.can_reach_and_hurt_enemy(Enemy.vampire),
            DropLocation.vampire_bandage: self.can_reach_and_hurt_enemy(Enemy.vampire),
            DropLocation.vampire_page_ashes: self.can_reach_and_hurt_enemy(Enemy.vampire_page),
            DropLocation.vampire_page_20c: self.can_reach_and_hurt_enemy(Enemy.vampire_page),
            DropLocation.vampire_drop: self.can_reach_and_hurt_enemy(Enemy.vampire_page),
            DropLocation.malformed_vampiric_ashes: self.can_reach_and_hurt_enemy(Enemy.malformed),
            DropLocation.great_bat_health_vial: self.can_reach_and_hurt_enemy(Enemy.great_bat),
            DropLocation.great_bat_obsidian: self.can_reach_and_hurt_enemy(Enemy.great_bat),
            DropLocation.great_bat_10c: self.can_reach_and_hurt_enemy(Enemy.great_bat),
            DropLocation.poltergeist_10c: self.can_reach_and_hurt_enemy(Enemy.poltergeist),
            DropLocation.poltergeist_ectoplasm: self.can_reach_and_hurt_enemy(Enemy.poltergeist),
            DropLocation.horse_10c: self.can_reach_and_hurt_enemy(Enemy.malformed_horse),
            DropLocation.horse_mana_vial: self.can_reach_and_hurt_enemy(Enemy.malformed_horse),
            DropLocation.horse_drop: self.can_reach_and_hurt_enemy(Enemy.malformed_horse),
            DropLocation.hallowed_husk_10c: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk),
            DropLocation.hallowed_husk_bones: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk),
            DropLocation.hallowed_husk_bandage: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk),
            DropLocation.hallowed_husk_light_urn: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk),
            DropLocation.hallowed_husk_goldeness: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk),
            DropLocation.hallowed_husk_holy_water: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk),
            DropLocation.ikkurilb_root: self.can_reach_and_hurt_enemy(Enemy.ikurrilb),
            DropLocation.ikkurilb_10c: self.can_reach_and_hurt_enemy(Enemy.ikurrilb),
            DropLocation.ikkurilb_snowflake_obsidian: self.can_reach_and_hurt_enemy(Enemy.ikurrilb),
            DropLocation.mimic_moon_vial: self.can_reach_and_hurt_enemy(Enemy.mimic),
            DropLocation.mimic_obsidian: self.can_reach_and_hurt_enemy(Enemy.mimic),
            DropLocation.mimic_fools_gold: self.can_reach_and_hurt_enemy(Enemy.mimic),
            DropLocation.obsidian_skeleton_10c: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton),
            DropLocation.obsidian_skeleton_bones: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton),
            DropLocation.obsidian_skeleton_mana_vial: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton),
            DropLocation.obsidian_skeleton_obsidian: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton),
            DropLocation.obsidian_skeleton_drop_1: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton),
            DropLocation.obsidian_skeleton_drop_2: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton),
            DropLocation.anpu_10c: self.can_reach_and_hurt_enemy(Enemy.anpu) | self.can_reach_and_hurt_enemy(Enemy.anpu_sword),
            DropLocation.anpu_fire_opal: self.can_reach_and_hurt_enemy(Enemy.anpu) | self.can_reach_and_hurt_enemy(Enemy.anpu_sword),
            DropLocation.anpu_drop_1: self.can_reach_and_hurt_enemy(Enemy.anpu_sword),
            DropLocation.anpu_drop_2: self.can_reach_and_hurt_enemy(Enemy.anpu),
            DropLocation.serpent_antidote: self.can_reach_and_hurt_enemy(Enemy.serpent),
            DropLocation.serpent_5c: self.can_reach_and_hurt_enemy(Enemy.serpent),
            DropLocation.embalmed_bandage: self.can_reach_and_hurt_enemy(Enemy.embalmed),
            DropLocation.embalmed_ashes: self.can_reach_and_hurt_enemy(Enemy.embalmed),
            DropLocation.embalmed_bones: self.can_reach_and_hurt_enemy(Enemy.embalmed),
            DropLocation.jailor_drop: self.can_reach_and_hurt_enemy(Enemy.jailor),
            DropLocation.jailor_10c: self.can_reach_and_hurt_enemy(Enemy.jailor),
            DropLocation.jailor_candle: self.can_reach_and_hurt_enemy(Enemy.jailor),
            DropLocation.jailor_bandage: self.can_reach_and_hurt_enemy(Enemy.jailor),
            DropLocation.jailor_health_vial: self.can_reach_and_hurt_enemy(Enemy.jailor),
            DropLocation.jailor_angel: self.can_reach_and_hurt_enemy(Enemy.jailor),
            DropLocation.lunam_ectoplasm: self.can_reach_and_hurt_enemy(Enemy.lunam),
            DropLocation.lunam_10c: self.can_reach_and_hurt_enemy(Enemy.lunam),
            DropLocation.lunam_snowflake_obsidian: self.can_reach_and_hurt_enemy(Enemy.lunam),
            DropLocation.giant_spell: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton),
            DropLocation.giant_dark_urn: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton),
            DropLocation.giant_bones: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton),
            DropLocation.giant_mana_vial: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton),
            DropLocation.giant_onyx: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton),
            DropLocation.lupine_spell: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton),
            DropLocation.lupine_bones: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton),
            DropLocation.lupine_onyx: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton),
            DropLocation.lupine_10c: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton),
            DropLocation.infested_antidote: self.can_reach_and_hurt_enemy(Enemy.infested_corpse),
            DropLocation.infested_bones: self.can_reach_and_hurt_enemy(Enemy.infested_corpse),
            DropLocation.sucsarian_drop_1: self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger),
            DropLocation.sucsarian_drop_2: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear),
            DropLocation.sucsarian_10c: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear) | self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger),
            DropLocation.sucsarian_obsidian: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear) | self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger),
            DropLocation.sucsarian_snowflake_obsidian: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear) | self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger),
            DropLocation.sucsarian_throwing_knife: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear) | self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger),
            DropLocation.vesta_fairy_moss: self.can_reach_and_hurt_enemy(Enemy.vesta),
            DropLocation.vesta_yellow_morel: self.can_reach_and_hurt_enemy(Enemy.vesta),
            DropLocation.vesta_dest_angel: self.can_reach_and_hurt_enemy(Enemy.vesta),
            DropLocation.ceres_fairy_moss: self.can_reach_and_hurt_enemy(Enemy.ceres),
            DropLocation.ceres_yellow_morel: self.can_reach_and_hurt_enemy(Enemy.ceres),
            DropLocation.ceres_dest_angel: self.can_reach_and_hurt_enemy(Enemy.ceres),
            DropLocation.gloom_fairy_moss: self.can_reach_and_hurt_enemy(Enemy.gloom_wood),
            DropLocation.gloom_health_vial: self.can_reach_and_hurt_enemy(Enemy.gloom_wood),
            DropLocation.gloom_dest_angel: self.can_reach_and_hurt_enemy(Enemy.gloom_wood),
            DropLocation.cetea_drop: self.can_reach_and_hurt_enemy(Enemy.cetea),
            DropLocation.cetea_10c: self.can_reach_and_hurt_enemy(Enemy.cetea),
            DropLocation.cetea_ocean_bone_shell: self.can_reach_and_hurt_enemy(Enemy.cetea),
            DropLocation.sea_demon: self.can_reach_any_region(immovable_enemies[Enemy.demon]),
            DropLocation.sanguis_book: self.can_reach_and_hurt_enemy("Sanguis Umbra"),

            # All Quenchsanity Rules
            Quench.rapier: self.can_get_weapon(Weapon.rapier),
            Quench.shadow_blade: self.can_get_weapon(Weapon.shadow_blade),
            Quench.shining_blade: self.can_get_weapon(Weapon.shining_blade),
            Quench.rusted_sword: self.can_get_weapon(Weapon.rusted_sword),
            Quench.torch: self.can_get_weapon(Weapon.torch),
            Quench.replica_sword: self.can_get_weapon(Weapon.replica_sword),
            Quench.obsidian_poisonguard: self.can_get_weapon(Weapon.obsidian_poisonguard),
            Quench.obsidian_cursebrand: self.can_get_weapon(Weapon.obsidian_cursebrand),
            Quench.lyrian_longsword: self.can_get_weapon(Weapon.lyrian_longsword),
            Quench.elfen_sword: self.can_get_weapon(Weapon.elfen_sword),
            Quench.crossbow: self.can_get_weapon(Weapon.crossbow),
            Quench.broken_lance: self.can_get_weapon(Weapon.broken_lance),
            Quench.broken_hilt: self.can_get_weapon(Weapon.broken_hilt),
            Quench.brittle_arming_sword: self.can_get_weapon(Weapon.brittle_arming_sword),
            Quench.stone_club: self.can_get_weapon(Weapon.stone_club),
            Quench.iron_club: self.can_get_weapon(Weapon.iron_club),
            Quench.iron_claw: self.can_get_weapon(Weapon.iron_claw),
            Quench.steel_claw: self.can_get_weapon(Weapon.steel_claw),
            Quench.obsidian_seal: self.can_get_weapon(Weapon.obsidian_seal),
            Quench.scythe: self.can_kill_death(),

            # All Etna's Pupil Rules
            AlchemyLocation.explosives: self.can_obtain_all_alchemy_items([Alchemy.ashes, Alchemy.fire_opal]),
            AlchemyLocation.knife: self.can_obtain_alchemy_item(Alchemy.ocean_bone_shard),
            AlchemyLocation.health: self.can_obtain_all_alchemy_items([Alchemy.opal, Alchemy.yellow_morel, Alchemy.lotus_seed_pod]),
            AlchemyLocation.mana: self.can_obtain_all_alchemy_items([Alchemy.opal, Alchemy.onyx, Alchemy.lotus_seed_pod]),
            AlchemyLocation.moonlight: self.can_obtain_all_alchemy_items([Alchemy.ashes, Alchemy.moon_petal, Alchemy.obsidian]),
            AlchemyLocation.spectral: self.can_obtain_all_alchemy_items([Alchemy.ectoplasm, Alchemy.ikurrilb_root, Alchemy.fire_opal]),
            AlchemyLocation.poison_knife: self.can_obtain_all_alchemy_items([Alchemy.destroying_angel_mushroom, Alchemy.ocean_bone_shell]),
            AlchemyLocation.staff_of_osiris: self.can_obtain_all_alchemy_items([Alchemy.onyx, Alchemy.ikurrilb_root, Alchemy.bones]),
            AlchemyLocation.poison_urn: self.can_obtain_all_alchemy_items([Alchemy.destroying_angel_mushroom, Alchemy.ocean_bone_shard,
                                                                                         Alchemy.bloodweed]),
            AlchemyLocation.fairy_moss: self.can_obtain_all_alchemy_items([Alchemy.moon_petal, Alchemy.bloodweed, Alchemy.yellow_morel]),
            AlchemyLocation.antidote: self.can_obtain_all_alchemy_items([Alchemy.destroying_angel_mushroom, Alchemy.lotus_seed_pod]),
            AlchemyLocation.banner: self.can_obtain_all_alchemy_items([Alchemy.ashes, Alchemy.bones]),
            AlchemyLocation.holy: self.can_obtain_all_alchemy_items([Alchemy.moon_petal, Alchemy.opal]),
            AlchemyLocation.warp: self.can_obtain_all_alchemy_items([Alchemy.snowflake_obsidian, Alchemy.onyx, Alchemy.obsidian]),
            AlchemyLocation.wisp: self.can_obtain_all_alchemy_items([Alchemy.snowflake_obsidian, Alchemy.ectoplasm, Alchemy.moon_petal]),
            AlchemyLocation.limbo: HasAll(*(Alchemy.broken_sword, Alchemy.fractured_life, Alchemy.fractured_death,)),

            SpookyLocation.spooky_spell: Has(SpookyItem.soul_candy, 35),
            SpookyLocation.headless_horseman: self.has_element_access(Elements.fire) & self.can_level_reasonably(),

            LevelLocation.level_2: self.can_reach_level_in_levelsanity(2),
            LevelLocation.level_3: self.can_reach_level_in_levelsanity(3),
            LevelLocation.level_4: self.can_reach_level_in_levelsanity(4),
            LevelLocation.level_5: self.can_reach_level_in_levelsanity(5),
            LevelLocation.level_6: self.can_reach_level_in_levelsanity(6),
            LevelLocation.level_7: self.can_reach_level_in_levelsanity(7),
            LevelLocation.level_8: self.can_reach_level_in_levelsanity(8),
            LevelLocation.level_9: self.can_reach_level_in_levelsanity(9),
            LevelLocation.level_10: self.can_reach_level_in_levelsanity(10),
            LevelLocation.level_11: self.can_reach_level_in_levelsanity(11),
            LevelLocation.level_12: self.can_reach_level_in_levelsanity(12),
            LevelLocation.level_13: self.can_reach_level_in_levelsanity(13),
            LevelLocation.level_14: self.can_reach_level_in_levelsanity(14),
            LevelLocation.level_15: self.can_reach_level_in_levelsanity(15),
            LevelLocation.level_16: self.can_reach_level_in_levelsanity(16),
            LevelLocation.level_17: self.can_reach_level_in_levelsanity(17),
            LevelLocation.level_18: self.can_reach_level_in_levelsanity(18),
            LevelLocation.level_19: self.can_reach_level_in_levelsanity(19),
            LevelLocation.level_20: self.can_reach_level_in_levelsanity(20),
            LevelLocation.level_21: self.can_reach_level_in_levelsanity(21),
            LevelLocation.level_22: self.can_reach_level_in_levelsanity(22),
            LevelLocation.level_23: self.can_reach_level_in_levelsanity(23),
            LevelLocation.level_24: self.can_reach_level_in_levelsanity(24),
            LevelLocation.level_25: self.can_reach_level_in_levelsanity(25),
            LevelLocation.level_26: self.can_reach_level_in_levelsanity(26),
            LevelLocation.level_27: self.can_reach_level_in_levelsanity(27),
            LevelLocation.level_28: self.can_reach_level_in_levelsanity(28),
            LevelLocation.level_29: self.can_reach_level_in_levelsanity(29),
            LevelLocation.level_30: self.can_reach_level_in_levelsanity(30),
            LevelLocation.level_31: self.can_reach_level_in_levelsanity(31),
            LevelLocation.level_32: self.can_reach_level_in_levelsanity(32),
            LevelLocation.level_33: self.can_reach_level_in_levelsanity(33),
            LevelLocation.level_34: self.can_reach_level_in_levelsanity(34),
            LevelLocation.level_35: self.can_reach_level_in_levelsanity(35),
            LevelLocation.level_36: self.can_reach_level_in_levelsanity(36),
            LevelLocation.level_37: self.can_reach_level_in_levelsanity(37),
            LevelLocation.level_38: self.can_reach_level_in_levelsanity(38),
            LevelLocation.level_39: self.can_reach_level_in_levelsanity(39),
            LevelLocation.level_40: self.can_reach_level_in_levelsanity(40),
            LevelLocation.level_41: self.can_reach_level_in_levelsanity(41),
            LevelLocation.level_42: self.can_reach_level_in_levelsanity(42),
            LevelLocation.level_43: self.can_reach_level_in_levelsanity(43),
            LevelLocation.level_44: self.can_reach_level_in_levelsanity(44),
            LevelLocation.level_45: self.can_reach_level_in_levelsanity(45),
            LevelLocation.level_46: self.can_reach_level_in_levelsanity(46),
            LevelLocation.level_47: self.can_reach_level_in_levelsanity(47),
            LevelLocation.level_48: self.can_reach_level_in_levelsanity(48),
            LevelLocation.level_49: self.can_reach_level_in_levelsanity(49),
            LevelLocation.level_50: self.can_reach_level_in_levelsanity(50),
            LevelLocation.level_51: self.can_reach_level_in_levelsanity(51),
            LevelLocation.level_52: self.can_reach_level_in_levelsanity(52),
            LevelLocation.level_53: self.can_reach_level_in_levelsanity(53),
            LevelLocation.level_54: self.can_reach_level_in_levelsanity(54),
            LevelLocation.level_55: self.can_reach_level_in_levelsanity(55),
            LevelLocation.level_56: self.can_reach_level_in_levelsanity(56),
            LevelLocation.level_57: self.can_reach_level_in_levelsanity(57),
            LevelLocation.level_58: self.can_reach_level_in_levelsanity(58),
            LevelLocation.level_59: self.can_reach_level_in_levelsanity(59),
            LevelLocation.level_60: self.can_reach_level_in_levelsanity(60),
            LevelLocation.level_61: self.can_reach_level_in_levelsanity(61),
            LevelLocation.level_62: self.can_reach_level_in_levelsanity(62),
            LevelLocation.level_63: self.can_reach_level_in_levelsanity(63),
            LevelLocation.level_64: self.can_reach_level_in_levelsanity(64),
            LevelLocation.level_65: self.can_reach_level_in_levelsanity(65),
            LevelLocation.level_66: self.can_reach_level_in_levelsanity(66),
            LevelLocation.level_67: self.can_reach_level_in_levelsanity(67),
            LevelLocation.level_68: self.can_reach_level_in_levelsanity(68),
            LevelLocation.level_69: self.can_reach_level_in_levelsanity(69),
            LevelLocation.level_70: self.can_reach_level_in_levelsanity(70),
            LevelLocation.level_71: self.can_reach_level_in_levelsanity(71),
            LevelLocation.level_72: self.can_reach_level_in_levelsanity(72),
            LevelLocation.level_73: self.can_reach_level_in_levelsanity(73),
            LevelLocation.level_74: self.can_reach_level_in_levelsanity(74),
            LevelLocation.level_75: self.can_reach_level_in_levelsanity(75),
            LevelLocation.level_76: self.can_reach_level_in_levelsanity(76),
            LevelLocation.level_77: self.can_reach_level_in_levelsanity(77),
            LevelLocation.level_78: self.can_reach_level_in_levelsanity(78),
            LevelLocation.level_79: self.can_reach_level_in_levelsanity(79),
            LevelLocation.level_80: self.can_reach_level_in_levelsanity(80),
            LevelLocation.level_81: self.can_reach_level_in_levelsanity(81),
            LevelLocation.level_82: self.can_reach_level_in_levelsanity(82),
            LevelLocation.level_83: self.can_reach_level_in_levelsanity(83),
            LevelLocation.level_84: self.can_reach_level_in_levelsanity(84),
            LevelLocation.level_85: self.can_reach_level_in_levelsanity(85),
            LevelLocation.level_86: self.can_reach_level_in_levelsanity(86),
            LevelLocation.level_87: self.can_reach_level_in_levelsanity(87),
            LevelLocation.level_88: self.can_reach_level_in_levelsanity(88),
            LevelLocation.level_89: self.can_reach_level_in_levelsanity(89),
            LevelLocation.level_90: self.can_reach_level_in_levelsanity(90),
            LevelLocation.level_91: self.can_reach_level_in_levelsanity(91),
            LevelLocation.level_92: self.can_reach_level_in_levelsanity(92),
            LevelLocation.level_93: self.can_reach_level_in_levelsanity(93),
            LevelLocation.level_94: self.can_reach_level_in_levelsanity(94),
            LevelLocation.level_95: self.can_reach_level_in_levelsanity(95),
            LevelLocation.level_96: self.can_reach_level_in_levelsanity(96),
            LevelLocation.level_97: self.can_reach_level_in_levelsanity(97),
            LevelLocation.level_98: self.can_reach_level_in_levelsanity(98),
            LevelLocation.level_99: self.can_reach_level_in_levelsanity(99),
            LevelLocation.level_100: self.can_reach_level_in_levelsanity(100),

            LoreLocation.golden_plea: self.has_element_access(Elements.fire_options),

            GrassLocation.yf_mushroom_48: self.has_blood_spell_access(),
            GrassLocation.yf_mushroom_34:  self.has_blood_spell_access(),
            BreakLocation.hb_vase_105: self.can_jump_given_height(JumpHeight.low),
            BreakLocation.hb_vase_39: self.can_jump_given_height(JumpHeight.low),
            BreakLocation.hb_vase_65: self.can_jump_given_height(JumpHeight.low),
            GrassLocation.fla_fiddlehead_14: self.can_jump_given_height(JumpHeight.high),
            GrassLocation.fla_fiddlehead_27: self.can_jump_given_height(JumpHeight.high),
            GrassLocation.fla_fiddlehead_11: self.can_jump_given_height(JumpHeight.high),
            GrassLocation.fla_fiddlehead_22: self.can_jump_given_height(JumpHeight.high),
            GrassLocation.fla_lotus_15: self.can_jump_given_height(JumpHeight.high),
            GrassLocation.fla_lotus_18: self.can_jump_given_height(JumpHeight.high),

            Endings.wake_dreamer: self.can_wake_dreamer(),
            Endings.open_door: self.can_open_evil_door(),
            "The Dreamer or the Door": self.can_wake_dreamer() | self.can_open_evil_door(),
        }

    def can_reach_and_hurt_enemy(self, name: str) -> Rule[Any]:
        if name in self.world.enemy_regions:
            region_rule = self.can_reach_any_region(self.world.enemy_regions[name])
        else:
            region_rule = self.can_reach_any_region(immovable_enemies[name])
        if name not in all_enemy_data_by_name:
            attack_rule = True_()
        else:
            possible_weapons = [weapon for weapon in self.world.weapon_elements if
                                self.world.weapon_elements[weapon] not in all_enemy_data_by_name[name].immune and weapon not in support_spells]
            attack_rule = HasAny(*tuple(possible_weapons))
        return region_rule & attack_rule

    def has_aoe_spell(self) -> Rule[Any]:
        level_rule = True_()
        if self.world.options.levelsanity:
            level_rule = self.can_reach_level_in_levelsanity(30)
        aoe_spells = [Spell.ice_tear, Spell.moon_beam, Spell.blue_flame_arc, Spell.lava_chasm]

        return HasAny(*tuple(aoe_spells)) & level_rule

    def is_vampire(self) -> Rule[Any]:
        vampire = False_()
        if self.world.options.starting_class == self.world.options.starting_class.option_vampire:
            vampire = True_()
        return vampire

    def can_reach_any_region(self, spots: List[str]) -> Rule[Any]:
        region_rule = False_()
        for spot in spots:
            region_rule = region_rule | CanReachRegion(spot)
        return region_rule

    def can_reach_all_regions(self, spots: List[str]) -> Rule[Any]:
        all_rule = True_()
        for spot in spots:
            all_rule = all_rule & CanReachRegion(spot)
        return all_rule

    def can_jump_given_height(self, height: str) -> Rule[Any]:
        if height == JumpHeight.low:
            level_rule = Has(CustomItem.experience, 10, options=[OptionFilter(Levelsanity, Levelsanity.option_true)], filtered_resolution=True)
            return level_rule | Has(Glitch.item)
        elif height == JumpHeight.medium:
            medium_spells = [Spell.barrier, Spell.icarian_flight, Spell.coffin, Spell.rock_bridge]
            if self.world.options.dropsanity:
                medium_spells.append(MobSpell.summon_snail)
            return HasAny(*tuple(medium_spells)) | Has(Glitch.item)
        else:
            high_spells = (Spell.barrier, Spell.rock_bridge,)
            return HasAny(*high_spells) | Has(Spell.icarian_flight)

    def has_door_key(self, key: str) -> Rule[Any]:
        return Has(key, options=[OptionFilter(DoorLocks, DoorLocks.option_true)], filtered_resolution=True)

    def has_light_source(self) -> Rule[Any]:
        if self.world.options.starting_area == self.world.options.starting_area.option_tomb:
            return True_()
        sources = base_light_sources.copy()
        sources.extend(source for source in shop_light_sources)
        sources.extend(source for source in drop_light_sources)
        sources.extend(source for source in quench_light_sources)
        if self.world.options.quenchsanity:
            sources.remove(Weapon.broken_hilt)
        if self.world.options.etnas_pupil:
            limbo_rule = Has(Weapon.limbo)
        else:
            limbo_rule = HasAll(*(Alchemy.broken_sword, Alchemy.fractured_life, Alchemy.fractured_death,))
        return HasAny(*tuple(sources)) | limbo_rule | Has(Glitch.item) | self.lightless

    # Needs a complete rework; add events to this game to figure out when an area is reachable to farm it appropriately.
    def can_reach_level_in_levelsanity(self, level: int) -> Rule[Any]:
        if level <= 10:
            return Has(CustomItem.experience, max(level - self.level, 0)) | Has(Glitch.item)
        has_bangle = True_()
        if level >= 50:
            has_bangle = Has(CustomItem.lucky_bangle)
        cap_rule = self.IsLevelBelowLevelCapBasedOnWorldAreas(level)
        return (Has(CustomItem.experience, max(level - self.level, 0)) & has_bangle & cap_rule) | Has(Glitch.item)

    def can_level_reasonably(self) -> Rule[Any]:
        if self.world.options.levelsanity:
            return Has(CustomItem.experience, 40) | Has(Glitch.item)
        if self.world.options.starting_area != self.world.options.starting_area.option_basin:
            level_rule = True_()
        else:
            # The player should be able to find SOME place to run off to in order to level.
            # Writing it like this avoids a region check.
            can_escape_basin_start_in_all_directions = (self.has_light_source() & self.has_keys_for_basin_or_canopy() &
                                                        self.has_door_key(Door.basin_broken_steps) &
                                                        self.has_switch_key(Switch.temple_switch) &
                                                        self.can_jump_given_height(JumpHeight.high))
            level_rule = can_escape_basin_start_in_all_directions
        return level_rule | Has(Glitch.item)

    def has_spell(self, spell: str) -> Rule[Any]:
        return Has(spell)

    def has_all_spells(self, spells: List[str]) -> Rule[Any]:
        has_spells = True_()
        for spell in spells:
            has_spell = Has(spell)
            has_spells = has_spells & has_spell
        return has_spells

    def can_melee_window(self) -> Rule[Any]:
        if "Melee Window" not in self.world.options.tricks_and_glitches:
            return False_()
        return Has(Spell.rock_bridge) & self.HasWeaponOfGivenElementForWindow(Elements.poison_or_dark, self.world.weapon_elements)


    def has_every_spell(self, starting_weapon: str = None) -> Rule[Any]:
        if self.world.options.dropsanity == self.world.options.dropsanity.option_off:
            every_spell = Spell.base_spells.copy()
        else:
            every_spell = list(set.union(set(Spell.base_spells), set(MobSpell.drop_spells)))
        if starting_weapon in every_spell:
            every_spell.remove(starting_weapon)
        if self.world.options.dropsanity == self.world.options.dropsanity.option_off:
            return self.has_all_spells(every_spell) & self.can_reach_every_necessary_mob_for_spells()
        else:
            return self.has_all_spells(every_spell)

    def can_reach_every_necessary_mob_for_spells(self) -> Rule[Any]:
        return (self.can_reach_monster(Enemy.chimera) & self.can_reach_monster(Enemy.kodama) & self.can_reach_monster(Enemy.skeleton) &
                self.can_reach_monster(Enemy.skeleton_weapon) & (self.can_reach_monster(Enemy.lupine_skeleton) |
                self.can_reach_monster(Enemy.giant_skeleton)) & self.can_reach_monster(Enemy.cetea) & self.can_reach_monster(Enemy.snail))

    def can_purchase_item(self) -> Rule[Any]:
        if self.world.options.shopsanity == self.world.options.shopsanity.option_false:
            return True_()
        return ((CanReachRegion(LunacidRegion.boiling_grotto) & Has(Spell.ignis_calor)) |
                CanReachLocation(BaseLocation.fate_lucid_blade))

    def has_blood_spell_access(self) -> Rule[Any]:
        return HasAny(*tuple(blood_spells))

    def has_keys_for_basin_or_canopy(self) -> Rule[Any]:
        if self.world.options.shopsanity == self.world.options.shopsanity.option_false:
            return Has(UniqueItem.enchanted_key)
        return Has(UniqueItem.enchanted_key, 2)

    def has_switch_key(self, key: str) -> Rule[Any]:
        return Has(key, options=[OptionFilter(SwitchLocks, SwitchLocks.option_true)], filtered_resolution=True)

    def has_crystal_orb(self) -> Rule[Any]:
        return Has(UniqueItem.dusty_crystal_orb, options=[OptionFilter(SecretDoorLock, SecretDoorLock.option_true)], filtered_resolution=True)

    def has_element_access(self, element: str | List[str]) -> Rule[Any]:
        if isinstance(element, str):
            element = [element]
        element_options = [item for item in self.world.weapon_elements if self.world.weapon_elements[item] in element]
        return HasAny(*tuple(element_options)) | Has(Weapon.wand_of_power) | Has(Spell.ignis_calor)

    def has_ranged_element_access(self, element: str | List[str]) -> Rule[Any]:
        if isinstance(element, str):
            element = [element]
        ranged_options = [item for item in ranged_weapons]
        ranged_options.extend([item for item in ranged_spells])
        element_options = [item for item in self.world.weapon_elements if self.world.weapon_elements[item] in element and item in ranged_options]
        return HasAny(*tuple(element_options)) | Has(Weapon.wand_of_power)

    def has_coins_for_door(self) -> Rule[Any]:
        return Has(Coins.strange_coin, self.world.options.required_strange_coin.value)

    def can_buy_jotunn(self) -> Rule[Any]:
        if self.world.options.shopsanity:
            return Has(Weapon.jotunn_slayer)
        return (CanReachLocation(BaseLocation.fate_lucid_blade)
                & (Has(Voucher.sheryl_dreamer_voucher) | Has(Glitch.item)))

    def can_defeat_the_prince(self) -> Rule[Any]:
        return (self.has_element_access(Elements.light_options) & self.can_level_reasonably()) | Has(Glitch.item)

    def can_reach_monster(self, enemy: str) -> Rule[Any]:
        locations = self.world.enemy_regions[enemy]
        return self.can_reach_any_region(locations)

    def can_get_weapon(self, weapon: str) -> Rule[Any]:
        if self.world.starting_weapon.name == weapon:
            return True_()
        if weapon in Weapon.base_weapons:
            return Has(weapon)
        elif weapon in Weapon.shop_weapons:
            if self.world.options.shopsanity:
                return Has(weapon)
            return Has(Voucher.sheryl_initial_voucher) | Has(Glitch.item)
        elif weapon in Weapon.drop_weapons:
            if self.world.options.dropsanity:
                return Has(weapon)
            for enemy in all_drops_by_enemy:
                if weapon in all_drops_by_enemy[enemy]:
                    return self.can_reach_any_region(self.world.enemy_regions[enemy])
        elif weapon in Weapon.quenchsanity_weapons:
            return Has(weapon)
        return False_()

    def can_kill_death(self) -> Rule[Any]:
        if self.world.options.etnas_pupil:
            return Has(Weapon.limbo) & CanReachRegion(LunacidRegion.mausoleum)

        return HasAll(*(Alchemy.fractured_life, Alchemy.fractured_death, Alchemy.broken_sword,)) & CanReachRegion(LunacidRegion.mausoleum)

    def can_obtain_alchemy_item(self, alchemy_item: str) -> Rule[Any]:
        if self.world.options.etnas_pupil and self.world.options.dropsanity == self.world.options.dropsanity.option_randomized:
            return Has(alchemy_item)
        acceptable_regions = []
        for enemy in all_drops_by_enemy:
            if alchemy_item in all_drops_by_enemy[enemy]:
                for region in self.world.enemy_regions[enemy]:
                    if region not in acceptable_regions:
                        acceptable_regions.append(region)
        for plant in all_alchemy_plant_data:
            if alchemy_item == plant.drop:
                for region in plant.regions:
                    if region not in acceptable_regions:
                        acceptable_regions.append(region)
        region_rule = self.can_reach_any_region(acceptable_regions)
        return region_rule

    def can_obtain_all_alchemy_items(self, alchemy_items: List[str]) -> Rule[Any]:
        alchemy_rule = True_()
        for item in alchemy_items:
            alchemy_rule = alchemy_rule & self.can_obtain_alchemy_item(item)
        return alchemy_rule

    def can_rock_bridge_skip(self) -> Rule[Any]:
        return self.barrier & Has(Spell.rock_bridge)

    def can_wake_dreamer(self) -> Rule[Any]:
        can_wake = True_()
        if self.world.options.ending == self.world.options.ending.option_ending_e:
            can_wake = self.has_every_spell(self.world.starting_weapon.name) & Has(UniqueItem.white_tape)
        if self.world.options.ending == self.world.options.ending.option_any_ending:
            can_wake = CanReachRegion(LunacidRegion.grave_of_the_sleeper)
        return can_wake

    def can_open_evil_door(self) -> Rule[Any]:
        door_rule = self.has_coins_for_door()
        if self.world.options.ending == self.world.options.ending.option_any_ending:
            door_rule = door_rule & CanReachRegion(LunacidRegion.holy_seat_of_gold)
        return door_rule


    @dataclasses.dataclass()
    class IsLevelBelowLevelCapBasedOnWorldAreas(Rule["LunacidWorld"], game="Lunacid"):

        level: int

        @override
        def _instantiate(self, world: "LunacidWorld") -> Rule.Resolved:
            # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
            return self.Resolved(self.level, player=world.player)

        class Resolved(Rule.Resolved):
            level: int

            @override
            def _evaluate(self, state: CollectionState) -> bool:
                level_cap = 0
                for region in region_to_level_value:
                    if state.can_reach_region(region, self.player):
                        level_cap += region_to_level_value[region]
                level_cap *= 10

                return level_cap >= self.level

            @override
            def item_dependencies(self) -> dict[str, set[int]]:
                # this function is only required if you have caching enabled
                return {"Deep Knowledge": {id(self)}}

            def region_dependencies(self) -> dict[str, set[int]]:
                rule_dict = {}
                for region in region_to_level_value:
                    rule_dict[region] = {id(self)}
                return rule_dict

            @override
            def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
                # this method can be overridden to display custom explanations
                return [
                    {"type": "text", "text": "Can Reach Level "},
                    {"type": "color", "color": "green" if state and self(state) else "salmon", "text": str(self.level)},
                ]


    @dataclasses.dataclass()
    class HasWeaponOfGivenElementForWindow(Rule["LunacidWorld"], game="Lunacid"):

        element: List[str]
        element_lookup: Dict[str, str]

        @override
        def _instantiate(self, world: "LunacidWorld") -> Rule.Resolved:
            # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
            return self.Resolved(self.element, self.element_lookup, player=world.player)

        class Resolved(Rule.Resolved):
            element: List[str]
            element_lookup: Dict[str, str]

            @override
            def _evaluate(self, state: CollectionState) -> bool:
                rule = False_()
                for weapon in Weapon.long_weapons:
                    if self.element_lookup[weapon] in self.element:
                        rule = rule | Has(weapon)
                for weapon in Weapon.long_quenchable_weapon:
                    if self.element_lookup[weapon] in self.element:
                        rule = rule | Has(weapon)
                if self.element_lookup[SpookyWeapon.cavalry_saber] in self.element:
                    rule = rule | Has(SpookyWeapon.cavalry_saber)
                return rule

            @override
            def item_dependencies(self) -> dict[str, set[int]]:
                item_lookup = {}
                for weapon in Weapon.long_weapons:
                    if self.element_lookup[weapon] in self.element:
                        item_lookup[weapon] = {id(self)}
                for weapon in Weapon.long_quenchable_weapon:
                    if self.element_lookup[weapon] in self.element:
                        item_lookup[weapon] = {id(self)}
                if self.element_lookup[SpookyWeapon.cavalry_saber] in self.element:
                    item_lookup[SpookyWeapon.cavalry_saber] = {id(self)}
                # this function is only required if you have caching enabled
                return item_lookup

            @override
            def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
                # this method can be overridden to display custom explanations
                return [
                    {"type": "color", "color": "green" if state and self(state) else "salmon", "text": "Melee Weapon Obtained Can Hit Castle Le Fanu Window"},
                ]

    def set_lunacid_rules(self) -> None:
        multiworld = self.world.multiworld
        for region in multiworld.get_regions(self.player):
            for entrance in region.entrances:
                if entrance.name in self.entrance_rules:
                    self.world.set_rule(entrance, self.entrance_rules[entrance.name])
            for loc in region.locations:
                if loc.name in self.location_rules:
                    self.world.set_rule(loc, self.location_rules[loc.name])

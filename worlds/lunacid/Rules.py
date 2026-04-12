from BaseClasses import CollectionState
from typing import Dict, List, TYPE_CHECKING

from .data.enemy_positions import immovable_enemies
from .strings.enemies import Enemy
from .strings.properties import Elements
from worlds.generic.Rules import CollectionRule

from .data.spell_info import ranged_spells, support_spells
from .data.weapon_info import ranged_weapons
from .data.item_data import base_light_sources, shop_light_sources, blood_spells, drop_light_sources, quench_light_sources
from .data.enemy_data import all_enemy_data_by_name
from .data.plant_data import all_alchemy_plant_data
from .Options import LunacidOptions
from .strings.custom_features import JumpHeight, Glitch
from .strings.regions_entrances import LunacidEntrance, LunacidRegion, region_to_level_value, indirect_entrances
from .strings.spells import Spell, MobSpell
from .strings.items import UniqueItem, Progressives, Switch, Alchemy, Door, Coins, Voucher, SpookyItem, CustomItem
from .strings.locations import BaseLocation, ShopLocation, all_drops_by_enemy, DropLocation, Quench, AlchemyLocation, SpookyLocation, LevelLocation, LoreLocation, \
    GrassLocation, BreakLocation
from .strings.weapons import Weapon

if TYPE_CHECKING:
    from . import LunacidWorld


class LunacidRules:
    player: int
    world: "LunacidWorld"
    region_rules: Dict[str, CollectionRule]
    entrance_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]
    elements: Dict[str, str]
    enemy_regions: Dict[str, List[str]]
    lightless: bool
    rock_bridge: bool
    surface: bool
    barrier: bool

    def __init__(self, world: "LunacidWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options
        self.level = world.level
        self.enemy_regions = self.world.enemy_regions
        self.lightless = "Lightless" in self.world.options.tricks_and_glitches.value
        self.rock_bridge = "Rock Bridge Skip" in self.world.options.tricks_and_glitches.value
        self.surface = "Early Surface" in self.world.options.tricks_and_glitches.value
        self.barrier = "Barrier Skip" in self.world.options.tricks_and_glitches.value

        self.region_rules = {
            LunacidRegion.accursed_tomb: lambda state: self.has_light_source(state, self.world.options),
            LunacidRegion.chamber_of_fate: lambda state: state.has_all({UniqueItem.earth_talisman, UniqueItem.water_talisman}, self.player),
            LunacidRegion.terminus_prison_1f: lambda state: self.has_light_source(state, self.world.options),
            LunacidRegion.terminus_prison_4f: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            LunacidRegion.terminus_prison_basement: lambda state: self.has_light_source(state, self.world.options),
            LunacidRegion.throne_chamber: lambda state: self.can_defeat_the_prince(state, self.world.options),
        }

        self.entrance_rules = {
            LunacidEntrance.basin_to_temple_path: lambda state: not self.world.options.shopsanity or
                                                                self.has_keys_for_basin_or_canopy(state, self.world.options),
            LunacidEntrance.basin_to_archives_2f: lambda state: self.has_door_key(Door.basin_broken_steps, state, self.world.options) and
                                                                self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            LunacidEntrance.basin_to_surface: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or self.surface,

            LunacidEntrance.temple_path_to_basin: lambda state: not self.world.options.shopsanity or
                                                                self.has_keys_for_basin_or_canopy(state, self.world.options),
            LunacidEntrance.temple_path_to_temple_front: lambda state: self.has_light_source(state, self.world.options),

            LunacidEntrance.temple_front_to_temple_back: lambda state: self.has_switch_key(Switch.temple_switch, state, self.world.options),
            LunacidEntrance.temple_front_to_temple_sewers: lambda state: self.has_switch_key(Switch.temple_switch, state, self.world.options),
            LunacidEntrance.temple_front_to_temple_front_secret: lambda state: self.has_crystal_orb(state, self.world.options) and
                                                                               self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            LunacidEntrance.temple_front_to_locked_spot: lambda state: self.has_switch_key(Switch.temple_switch, state, self.world.options),

            LunacidEntrance.temple_sewers_to_mire: lambda state: self.has_door_key(Door.basin_temple_sewers, state, self.world.options),
            LunacidEntrance.temple_sewers_to_sewers_secret: lambda state: self.has_crystal_orb(state, self.world.options),


            LunacidEntrance.temple_back_to_temple_secret: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.temple_lower_to_temple_back: lambda state: self.has_light_source(state, self.world.options),

            LunacidEntrance.temple_lower_to_forest: lambda state: self.has_door_key(Door.basin_rickety_bridge, state, self.world.options),

            LunacidEntrance.rest_to_surface: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or self.surface,

            LunacidEntrance.archives_2f_to_basin: lambda state: self.has_door_key(Door.basin_broken_steps, state, self.world.options),
            LunacidEntrance.archives_2f_to_2f_secret: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.archives_2f_to_3f: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or
                                                             self.has_switch_key(Switch.archives_elevator_switches, state, self.world.options),
            LunacidEntrance.archives_1f_front_to_3f: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or
                                                                   self.has_switch_key(Switch.archives_elevator_switches, state, self.world.options),
            LunacidEntrance.archives_1f_back_to_2f: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or
                                                                  self.has_switch_key(Switch.archives_elevator_switches, state, self.world.options),

            LunacidEntrance.archives_3f_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.archives_1f_to_1f_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.archives_3f_to_vampire: lambda state: state.has(Progressives.vampiric_symbol, self.player, 2) or state.has(UniqueItem.vampiric_symbol_a, self.player),

            LunacidEntrance.archives_vampire_to_3f: lambda state: state.has(Progressives.vampiric_symbol, self.player, 2) or state.has(UniqueItem.vampiric_symbol_a, self.player),
            LunacidEntrance.archives_vampire_to_chasm: lambda state: self.has_door_key(Door.archives_sealed_door, state, self.world.options),

            LunacidEntrance.chasm_to_archives_vampire: lambda state: self.has_door_key(Door.archives_sealed_door, state, self.world.options),
            LunacidEntrance.chasm_to_chasm_upper: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            LunacidEntrance.chasm_upper_to_lower: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),

            LunacidEntrance.chasm_upper_to_surface: lambda state: self.has_door_key(Door.chasm_surface_door, state, self.world.options),
            LunacidEntrance.chasm_upper_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.surface_to_chasm_upper: lambda state: self.has_door_key(Door.chasm_surface_door, state, self.world.options),

            LunacidEntrance.mire_to_temple_sewers: lambda state: self.has_door_key(Door.basin_temple_sewers, state, self.world.options),
            LunacidEntrance.mire_to_mire_upper_secret: lambda state: self.has_crystal_orb(state, self.world.options) or
                                                                     self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            LunacidEntrance.mire_to_mire_lower_secrets: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.mire_to_sea: lambda state: self.has_door_key(Door.sea_westward, state, self.world.options),

            LunacidEntrance.forest_to_temple_lower: lambda state: self.has_door_key(Door.basin_rickety_bridge, state, self.world.options),
            LunacidEntrance.forest_to_canopy_path: lambda state: self.has_keys_for_basin_or_canopy(state, self.world.options),

            LunacidEntrance.canopy_path_to_forest: lambda state: self.has_keys_for_basin_or_canopy(state, self.world.options),
            LunacidEntrance.canopy_path_to_canopy: lambda state: self.has_door_key(Door.forest_door_in_trees, state, self.world.options),

            LunacidEntrance.lower_forest_secret: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.tomb_to_lower_forest: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            LunacidEntrance.forest_tomb_to_accursed_tomb: lambda state: self.has_door_key(Door.forest_patchouli, state, self.world.options),

            LunacidEntrance.sea_to_mire: lambda state: self.has_door_key(Door.sea_westward, state, self.world.options),
            LunacidEntrance.sea_to_castle_entrance: lambda state: self.has_door_key(Door.sea_double_doors, state, self.world.options),
            LunacidEntrance.sea_to_accursed_tomb: lambda state: self.has_door_key(Door.sea_eastward, state, self.world.options),

            LunacidEntrance.accursed_tomb_to_forest_tomb: lambda state: self.has_door_key(Door.forest_patchouli, state, self.world.options),

            LunacidEntrance.accursed_tomb_to_platform: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            LunacidEntrance.accursed_well_to_accursed: lambda state: self.has_light_source(state, self.world.options),
            LunacidEntrance.accursed_to_vampire: lambda state: self.has_element_access(Elements.light_options, state) or state.has(Weapon.wand_of_power, self.player),
            LunacidEntrance.accursed_to_mausoleum: lambda state: self.has_element_access(Elements.light_options, state) or state.has(Weapon.wand_of_power, self.player),
            LunacidEntrance.accursed_tomb_to_sea: lambda state: self.has_door_key(Door.sea_eastward, state, self.world.options),
            LunacidEntrance.accursed_tomb_to_secrets: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.vampire_tomb_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.accursed_to_accursed_well: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),

            LunacidEntrance.castle_entrance_to_sea: lambda state: self.has_door_key(Door.sea_double_doors, state, self.world.options),
            LunacidEntrance.castle_to_cattle: lambda state: self.is_vampire(self.world.options) or self.has_blood_spell_access(state) or self.can_rock_bridge_skip(state),
            LunacidEntrance.castle_entrance_to_main_halls: lambda state: self.is_vampire(self.world.options) or
                                                                         state.has(Progressives.vampiric_symbol, self.player, 1) or self.can_rock_bridge_skip(state) or
                                                                         state.has(UniqueItem.vampiric_symbol_w, self.player),

            LunacidEntrance.cattle_to_deeper: lambda state: self.is_vampire(self.world.options) or self.has_blood_spell_access(state),
            LunacidEntrance.cattle_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.castle_main_halls_to_entrance: lambda state: self.is_vampire(self.world.options) or state.has(Progressives.vampiric_symbol, self.player, 1) or
                                                                         state.has(UniqueItem.vampiric_symbol_w, self.player),
            LunacidEntrance.castle_main_halls_to_queen_path: lambda state: state.has(Progressives.vampiric_symbol, self.player, 3) or state.has(UniqueItem.vampiric_symbol_e, self.player),
            LunacidEntrance.castle_main_halls_to_upstairs: lambda state: state.has(Progressives.vampiric_symbol, self.player, 2) or state.has(UniqueItem.vampiric_symbol_a, self.player),

            LunacidEntrance.castle_upstairs_to_main_halls: lambda state: state.has(Progressives.vampiric_symbol, self.player, 2) or state.has(UniqueItem.vampiric_symbol_a, self.player),
            LunacidEntrance.castle_upstairs_to_tape_room: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.castle_upstairs_to_forbidden: lambda state: state.can_reach_region(LunacidRegion.castle_le_fanu_entrance, self.player) and (
                    self.has_ranged_element_access(
                        [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison,
                         Elements.ice_and_poison], state) or
                    (self.has_element_access(
                        [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison,
                         Elements.ice_and_poison], state) and state.has(Spell.rock_bridge, self.player))),
            LunacidEntrance.castle_upstairs_to_queen_rest: lambda state: state.has(Progressives.vampiric_symbol, self.player, 3) or state.has(UniqueItem.vampiric_symbol_e, self.player),

            LunacidEntrance.castle_cattle_back_to_boiling_grotto: lambda state: self.has_door_key(Door.burning_key, state, self.world.options),

            LunacidEntrance.castle_queen_path_to_main_halls: lambda state: state.has(Progressives.vampiric_symbol, self.player, 3) or state.has(UniqueItem.vampiric_symbol_e, self.player),
            LunacidEntrance.castle_queen_path_to_throne_room: lambda state: self.has_door_key(Door.throne_key, state, self.world.options),

            LunacidEntrance.rock_castle_le_fanu_cattle_deeper_skip: lambda state: self.can_rock_bridge_skip(state),
            LunacidEntrance.rock_castle_le_fanu_queen_door: lambda state: self.can_rock_bridge_skip(state),
            LunacidEntrance.rock_castle_le_fanu_past_door: lambda state: self.can_rock_bridge_skip(state),
            LunacidEntrance.rock_castle_le_fanu_secret_skips: lambda state: self.can_rock_bridge_skip(state),
            LunacidEntrance.rock_castle_le_fanu_upper_bridge: lambda state: self.can_rock_bridge_skip(state),
            LunacidEntrance.rock_castle_le_fanu_spell_skip: lambda state: self.can_rock_bridge_skip(state),

            LunacidEntrance.throne_room_to_prison: lambda state: self.has_door_key(Door.prison_key, state, self.world.options),
            LunacidEntrance.throne_room_to_castle_queen_path: lambda state: self.has_door_key(Door.throne_key, state, self.world.options),

            LunacidEntrance.castle_forbidden_to_upstairs: lambda state: state.can_reach_region(LunacidRegion.castle_le_fanu_entrance, self.player) and (
                    self.has_ranged_element_access(
                        [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison,
                         Elements.ice_and_poison], state) or
                    (self.has_element_access(
                        [Elements.dark, Elements.dark_and_fire, Elements.dark_and_light, Elements.poison,
                         Elements.ice_and_poison], state) and state.has(Spell.rock_bridge, self.player))),
            LunacidEntrance.castle_forbidden_to_sealed_ballroom: lambda state: self.has_door_key(Door.ballroom_key, state, self.world.options),

            LunacidEntrance.sealed_ballroom_to_forbidden_entry: lambda state: self.has_door_key(Door.ballroom_key, state, self.world.options),
            LunacidEntrance.sealed_ballroom_to_rooms: lambda state: self.has_door_key(Door.ballroom_rooms_key, state, self.world.options),
            LunacidEntrance.sealed_ballroom_to_secrets: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.sealed_ballroom_rooms_to_cave: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.sealed_ballroom_secret_room: lambda state: self.has_door_key(Door.ballroom_rooms_key, state, self.world.options),

            LunacidEntrance.boiling_grotto_to_castle_cattle_back: lambda state: self.has_door_key(Door.burning_key, state, self.world.options),
            LunacidEntrance.boiling_grotto_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.boiling_grotto_to_coffin_room: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.boiling_grotto_to_sand_temple: lambda state: self.has_switch_key(Switch.grotto_valves_switches, state, self.world.options),

            LunacidEntrance.boiling_grotto_coffin_room_to_boiling_grotto: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.sand_temple_to_deep_snake_pit: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or
                                                                         state.has(Spell.wind_dash, self.player),
            LunacidEntrance.sand_temple_secret_snake_pit_escape: lambda state: self.has_crystal_orb(state, self.world.options) or
                                                                               self.can_jump_given_height(JumpHeight.high, state, self.world.options),

            LunacidEntrance.abyss_to_5f: lambda state: self.has_door_key(Door.tower_key, state, self.world.options),
            LunacidEntrance.abyss_5f_to_10f: lambda state: self.has_ranged_element_access(Elements.all_elements, state) or state.has_any(ranged_weapons, self.player),
            LunacidEntrance.abyss_15f_to_20f: lambda state: self.has_light_source(state, self.world.options) and self.can_level_reasonably(state, self.world.options),

            LunacidEntrance.terminus_prison_1f_to_arena: lambda state: state.can_reach_region(LunacidRegion.terminus_prison_4f, self.player) and
                                                                       self.has_switch_key(Switch.prison_arena_switch, state, self.world.options) and
                                                                       self.has_door_key(Door.forlorn_key, state, self.world.options),
            LunacidEntrance.terminus_prison_1f_to_secrets: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.terminus_prison_1f_to_2f: lambda state: self.can_jump_given_height(JumpHeight.medium, state, self.world.options),
            LunacidEntrance.terminus_prison_1f_to_3f: lambda state: self.has_switch_key(Switch.prison_shortcut_switch, state, self.world.options),
            LunacidEntrance.terminus_prison_2f_doors: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            LunacidEntrance.terminus_prison_2f_to_3f: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            LunacidEntrance.terminus_prison_2f_to_1f: lambda state: self.has_light_source(state, self.world.options),
            LunacidEntrance.terminus_prison_3f_doors: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            LunacidEntrance.terminus_prison_3f_to_4f: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            LunacidEntrance.terminus_prison_3f_to_throne_room: lambda state: self.has_door_key(Door.prison_key, state, self.world.options),
            LunacidEntrance.terminus_prison_4f_secret_walls: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.terminus_prison_basement_to_ash: lambda state: self.has_door_key(Door.ash_key, state, self.world.options),

            LunacidEntrance.labyrinth_of_ash_to_terminus_prison: lambda state: self.has_door_key(Door.ash_key, state, self.world.options),
            LunacidEntrance.labyrinth_of_ash_to_interior: lambda state: self.has_door_key(Door.musical_key, state, self.world.options),
            LunacidEntrance.labyrinth_of_ash_to_holy_seat: lambda state: self.has_door_key(Door.musical_key, state, self.world.options),
            LunacidEntrance.labyrinth_interior_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.holy_seat_to_secret: lambda state: self.has_crystal_orb(state, self.world.options),

            LunacidEntrance.forlorn_arena_to_terminus_prison: lambda state: self.has_door_key(Door.forlorn_key, state, self.world.options),
            LunacidEntrance.forlorn_arena_to_path_to_sucsarius: lambda state: state.has(UniqueItem.water_talisman, self.player) and
                                                                              state.has(UniqueItem.earth_talisman, self.player) or self.barrier,
            LunacidEntrance.forlorn_arena_to_water_temple: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options) or
                                                                         state.has(Spell.wind_dash, self.player),
            LunacidEntrance.temple_of_earth_to_secrets: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.temple_of_water_lower_to_secrets: lambda state: self.has_crystal_orb(state, self.world.options),
            LunacidEntrance.forlorn_path_to_chamber: lambda state: self.has_door_key(Door.sucsarian_key, state, self.world.options),

            LunacidEntrance.chamber_to_grave: lambda state: self.has_door_key(Door.sleeper_key, state, self.world.options) and state.has(Weapon.lucid_blade, self.player),
        }

        self.location_rules = {
            "Throne of Prince Crilall Fanu": lambda state: self.can_defeat_the_prince(state, self.world.options),
            BaseLocation.wings_rest_demi_orb: lambda state: state.can_reach_region(LunacidRegion.grave_of_the_sleeper, self.player),
            BaseLocation.wings_rest_ocean_elixir: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            BaseLocation.temple_small_pillar: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options) or state.has(Spell.wind_dash,
                                                                                                                                               self.player),
            BaseLocation.temple_blood_altar: self.has_blood_spell_access,
            BaseLocation.temple_sewer_puzzle: lambda state: state.has(UniqueItem.vhs_tape, self.player) and
                                                            state.can_reach_region(LunacidRegion.vampire_tomb_tape_room, self.player),
            BaseLocation.archives_daedalus_one: lambda state: state.has(UniqueItem.black_book, self.player, 1),
            BaseLocation.archives_daedalus_two: lambda state: state.has(UniqueItem.black_book, self.player, 2),
            BaseLocation.archives_daedalus_third: lambda state: state.has(UniqueItem.black_book, self.player, 3),
            BaseLocation.sea_pillar: lambda state: state.has_any({Spell.icarian_flight, Spell.rock_bridge}, self.player),
            BaseLocation.chasm_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.chasm_invisible_cliffside: lambda state: state.has_any([Spell.coffin, Spell.icarian_flight], self.player),
            BaseLocation.catacombs_restore_vampire: lambda state: self.has_blood_spell_access(state),
            BaseLocation.mausoleum_upper_table: lambda state: self.can_jump_given_height(JumpHeight.medium, state, self.world.options),
            BaseLocation.mausoleum_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.mausoleum_kill_death: lambda state: state.has_all({Alchemy.fractured_life, Alchemy.fractured_death, Alchemy.broken_sword},
                                                                           self.player),
            BaseLocation.corrupted_room: lambda state: state.has(UniqueItem.corrupted_key, self.player),
            BaseLocation.yosei_hanging_in_trees: lambda state: state.has_any(ranged_weapons, self.player),
            BaseLocation.yosei_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.yosei_room_defended_by_blood_plant: lambda state: self.has_blood_spell_access(state),
            BaseLocation.yosei_patchouli_quest: lambda state: state.has(UniqueItem.skull_of_josiah, self.player),
            BaseLocation.sea_kill_jotunn: lambda state: self.can_buy_jotunn(self.world.options, state),
            BaseLocation.yosei_blood_plant_insides: lambda state: self.has_blood_spell_access(state),
            BaseLocation.yosei_rusted_sword: lambda state: self.has_blood_spell_access(state),
            BaseLocation.castle_cell_center: lambda state: self.has_element_access(Elements.fire, state),
            BaseLocation.castle_upper_floor_coffin_double: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.grotto_slab_of_bridge: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            BaseLocation.grotto_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.grotto_triple_secret_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.sand_basement_snake_pit: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.sand_hidden_sarcophagus: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.sand_chest_overlooking_crypt: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            BaseLocation.arena_earth_earthen_temple: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            BaseLocation.arena_rock_parkour: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            BaseLocation.prison_b2_egg_resting_place: lambda state: state.has(UniqueItem.skeleton_egg, self.player),
            BaseLocation.prison_f1_hidden_cell: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f1_hidden_debris_room: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f4_hidden_beds: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f4_maledictus_secret: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.prison_f3_locked_left: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            BaseLocation.prison_f3_locked_right: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            BaseLocation.prison_f3_locked_south: lambda state: state.has(UniqueItem.terminus_prison_key, self.player),
            "Free Sir Hicket": lambda state: state.has(Spell.ignis_calor, self.player),
            BaseLocation.ash_path_maze: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.ash_hidden_chest: lambda state: self.has_crystal_orb(state, self.world.options),
            BaseLocation.fate_lucid_blade: lambda state: state.has(Weapon.lucid_blade, self.player) or
                                                         self.world.multiworld.get_location(BaseLocation.fate_lucid_blade, self.player).item == Weapon.lucid_blade,

            # Shop Location Runes
            ShopLocation.buy_steel_needle: lambda state: state.has(Voucher.sheryl_initial_voucher, self.player),
            ShopLocation.buy_crossbow: lambda state: state.has(Voucher.sheryl_initial_voucher, self.player),
            ShopLocation.buy_rapier: lambda state: state.has(Voucher.sheryl_initial_voucher, self.player),
            ShopLocation.buy_privateer_musket: lambda state: self.can_purchase_item(state, self.world.options) and
                                                             state.has(Voucher.sheryl_golden_voucher, self.player),
            ShopLocation.buy_oil_lantern: lambda state: self.can_purchase_item(state, self.world.options) and
                                                        state.has(Voucher.sheryl_golden_voucher, self.player),
            ShopLocation.buy_jotunn_slayer: lambda state: self.can_reach_location(state, BaseLocation.fate_lucid_blade)
                                                          and state.has(Voucher.sheryl_dreamer_voucher, self.player),
            ShopLocation.buy_ocean_elixir_patchouli: lambda state: state.has(Voucher.patchouli_simp_discount, self.player),

            # All Drop Location Rules Yikes
            DropLocation.snail_2c: lambda state: self.can_reach_and_hurt_enemy(Enemy.snail, state),
            DropLocation.snail_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.snail, state),
            DropLocation.snail_ocean: lambda state: self.can_reach_and_hurt_enemy(Enemy.snail, state),
            DropLocation.snail: lambda state: self.can_reach_and_hurt_enemy(Enemy.snail, state),
            DropLocation.milk_5c: lambda state: self.can_reach_and_hurt_enemy(Enemy.milk_snail, state),
            DropLocation.milk_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.milk_snail, state),
            DropLocation.milk_ocean: lambda state: self.can_reach_and_hurt_enemy(Enemy.milk_snail, state),
            DropLocation.milk_snail: lambda state: self.can_reach_and_hurt_enemy(Enemy.milk_snail, state),
            DropLocation.shulker_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.shulker, state),
            DropLocation.shulker_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.shulker, state),
            DropLocation.mummy_knight_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy_knight, state),
            DropLocation.mummy_knight_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy_knight, state),
            DropLocation.mummy_knight_5c: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy_knight, state),
            DropLocation.mummy_knight: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy_knight, state),
            DropLocation.mummy_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy, state),
            DropLocation.mummy_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy, state),
            DropLocation.mummy_2c: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy, state),
            DropLocation.mummy_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.mummy_knight, state),
            DropLocation.necronomicon_fire_opal: lambda state: self.can_reach_and_hurt_enemy(Enemy.necronomicon, state),
            DropLocation.necronomicon_5c: lambda state: self.can_reach_and_hurt_enemy(Enemy.necronomicon, state),
            DropLocation.necronomicon_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.necronomicon, state),
            DropLocation.necronomicon_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.necronomicon, state),
            DropLocation.chimera_light_urn: lambda state: self.can_reach_and_hurt_enemy(Enemy.chimera, state),
            DropLocation.chimera_holy_water: lambda state: self.can_reach_and_hurt_enemy(Enemy.chimera, state),
            DropLocation.chimera_drop: lambda state: self.can_reach_and_hurt_enemy(Enemy.chimera, state),
            DropLocation.enlightened_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.enlightened_one, state),
            DropLocation.enlightened_ocean_bone_shell: lambda state: self.can_reach_and_hurt_enemy(Enemy.enlightened_one, state),
            DropLocation.slime_skeleton: lambda state: self.can_reach_and_hurt_enemy(Enemy.slime_skeleton, state),
            DropLocation.skeleton_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton, state) or self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon, state),
            DropLocation.skeleton_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton, state) or self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon, state),
            DropLocation.skeleton_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton, state) or self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon, state),
            DropLocation.skeleton_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton, state) or self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon, state),
            DropLocation.skeleton_2c: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton, state),
            DropLocation.skeleton_spell: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon, state),
            DropLocation.skeleton_weapon: lambda state: self.can_reach_and_hurt_enemy(Enemy.skeleton_weapon, state),
            DropLocation.rat_king_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.rat_king, state),
            DropLocation.rat_king_lotus_seed: lambda state: self.can_reach_and_hurt_enemy(Enemy.rat_king, state),
            DropLocation.rat: lambda state: self.can_reach_and_hurt_enemy(Enemy.rat, state),
            DropLocation.kodama_drop: lambda state: self.can_reach_and_hurt_enemy(Enemy.kodama, state),
            DropLocation.kodama_2c: lambda state: self.can_reach_and_hurt_enemy(Enemy.kodama, state),
            DropLocation.kodama_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.kodama, state),
            DropLocation.kodama_opal: lambda state: self.can_reach_and_hurt_enemy(Enemy.kodama, state),
            DropLocation.yakul_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.yakul, state),
            DropLocation.yakul_fire_opal: lambda state: self.can_reach_and_hurt_enemy(Enemy.yakul, state),
            DropLocation.yakul_opal: lambda state: self.can_reach_and_hurt_enemy(Enemy.yakul, state),
            DropLocation.yakul_health_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.yakul, state),
            DropLocation.venus_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.venus, state),
            DropLocation.venus_yellow_morel: lambda state: self.can_reach_and_hurt_enemy(Enemy.venus, state),
            DropLocation.venus_dest_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.venus, state),
            DropLocation.neptune_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.neptune, state),
            DropLocation.neptune_yellow_morel: lambda state: self.can_reach_and_hurt_enemy(Enemy.neptune, state),
            DropLocation.neptune_dest_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.neptune, state),
            DropLocation.unilateralis_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.unilateralis, state),
            DropLocation.unilateralis_yellow_morel: lambda state: self.can_reach_and_hurt_enemy(Enemy.unilateralis, state),
            DropLocation.unilateralis_dest_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.unilateralis, state),
            DropLocation.hemalith_health_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.hemalith, state),
            DropLocation.hemalith_shrimp: lambda state: self.can_reach_and_hurt_enemy(Enemy.hemalith, state),
            DropLocation.hemallith_bloodweed: lambda state: self.can_reach_and_hurt_enemy(Enemy.hemalith, state),
            DropLocation.mi_go_ocean_bone_shell: lambda state: self.can_reach_and_hurt_enemy(Enemy.mi_go, state),
            DropLocation.mi_go_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.mi_go, state),
            DropLocation.mi_go_snowflake_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.mi_go, state),
            DropLocation.mare_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.mare, state),
            DropLocation.mare_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.mare, state),
            DropLocation.mare_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.mare, state),
            DropLocation.painting_fire_opal: lambda state: self.can_reach_and_hurt_enemy(Enemy.cursed_painting, state),
            DropLocation.painting_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.cursed_painting, state),
            DropLocation.painting_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.cursed_painting, state),
            DropLocation.painting_20c: lambda state: self.can_reach_and_hurt_enemy(Enemy.cursed_painting, state),
            DropLocation.phantom_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.phantom, state),
            DropLocation.phantom_holy_water: lambda state: self.can_reach_and_hurt_enemy(Enemy.phantom, state),
            DropLocation.phantom_moon_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.phantom, state),
            DropLocation.phantom: lambda state: self.can_reach_and_hurt_enemy(Enemy.phantom, state),
            DropLocation.phantom_ectoplasm: lambda state: self.can_reach_and_hurt_enemy(Enemy.phantom, state),
            DropLocation.vampire_5c: lambda state: self.can_reach_and_hurt_enemy(Enemy.vampire, state),
            DropLocation.vampire_vampiric_ashes: lambda state: self.can_reach_and_hurt_enemy(Enemy.vampire, state),
            DropLocation.vampire_bandage: lambda state: self.can_reach_and_hurt_enemy(Enemy.vampire, state),
            DropLocation.vampire_page_ashes: lambda state: self.can_reach_and_hurt_enemy(Enemy.vampire_page, state),
            DropLocation.vampire_page_20c: lambda state: self.can_reach_and_hurt_enemy(Enemy.vampire_page, state),
            DropLocation.vampire_drop: lambda state: self.can_reach_and_hurt_enemy(Enemy.vampire_page, state),
            DropLocation.malformed_vampiric_ashes: lambda state: self.can_reach_and_hurt_enemy(Enemy.malformed, state),
            DropLocation.great_bat_health_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.great_bat, state),
            DropLocation.great_bat_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.great_bat, state),
            DropLocation.great_bat_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.great_bat, state),
            DropLocation.poltergeist_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.poltergeist, state),
            DropLocation.poltergeist_ectoplasm: lambda state: self.can_reach_and_hurt_enemy(Enemy.poltergeist, state),
            DropLocation.horse_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.malformed_horse, state),
            DropLocation.horse_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.malformed_horse, state),
            DropLocation.horse_drop: lambda state: self.can_reach_and_hurt_enemy(Enemy.malformed_horse, state),
            DropLocation.hallowed_husk_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk, state),
            DropLocation.hallowed_husk_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk, state),
            DropLocation.hallowed_husk_bandage: lambda state: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk, state),
            DropLocation.hallowed_husk_light_urn: lambda state: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk, state),
            DropLocation.hallowed_husk_goldeness: lambda state: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk, state),
            DropLocation.hallowed_husk_holy_water: lambda state: self.can_reach_and_hurt_enemy(Enemy.hallowed_husk, state),
            DropLocation.ikkurilb_root: lambda state: self.can_reach_and_hurt_enemy(Enemy.ikurrilb, state),
            DropLocation.ikkurilb_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.ikurrilb, state),
            DropLocation.ikkurilb_snowflake_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.ikurrilb, state),
            DropLocation.mimic_moon_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.mimic, state),
            DropLocation.mimic_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.mimic, state),
            DropLocation.mimic_fools_gold: lambda state: self.can_reach_and_hurt_enemy(Enemy.mimic, state),
            DropLocation.obsidian_skeleton_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton, state),
            DropLocation.obsidian_skeleton_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton, state),
            DropLocation.obsidian_skeleton_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton, state),
            DropLocation.obsidian_skeleton_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton, state),
            DropLocation.obsidian_skeleton_drop_1: lambda state: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton, state),
            DropLocation.obsidian_skeleton_drop_2: lambda state: self.can_reach_and_hurt_enemy(Enemy.obsidian_skeleton, state),
            DropLocation.anpu_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.anpu, state) or self.can_reach_and_hurt_enemy(Enemy.anpu_sword, state),
            DropLocation.anpu_fire_opal: lambda state: self.can_reach_and_hurt_enemy(Enemy.anpu, state) or self.can_reach_and_hurt_enemy(Enemy.anpu_sword, state),
            DropLocation.anpu_drop_1: lambda state: self.can_reach_and_hurt_enemy(Enemy.anpu_sword, state),
            DropLocation.anpu_drop_2: lambda state: self.can_reach_and_hurt_enemy(Enemy.anpu, state),
            DropLocation.serpent_antidote: lambda state: self.can_reach_and_hurt_enemy(Enemy.serpent, state),
            DropLocation.serpent_5c: lambda state: self.can_reach_and_hurt_enemy(Enemy.serpent, state),
            DropLocation.embalmed_bandage: lambda state: self.can_reach_and_hurt_enemy(Enemy.embalmed, state),
            DropLocation.embalmed_ashes: lambda state: self.can_reach_and_hurt_enemy(Enemy.embalmed, state),
            DropLocation.embalmed_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.embalmed, state),
            DropLocation.jailor_drop: lambda state: self.can_reach_and_hurt_enemy(Enemy.jailor, state),
            DropLocation.jailor_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.jailor, state),
            DropLocation.jailor_candle: lambda state: self.can_reach_and_hurt_enemy(Enemy.jailor, state),
            DropLocation.jailor_bandage: lambda state: self.can_reach_and_hurt_enemy(Enemy.jailor, state),
            DropLocation.jailor_health_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.jailor, state),
            DropLocation.jailor_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.jailor, state),
            DropLocation.lunam_ectoplasm: lambda state: self.can_reach_and_hurt_enemy(Enemy.lunam, state),
            DropLocation.lunam_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.lunam, state),
            DropLocation.lunam_snowflake_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.lunam, state),
            DropLocation.giant_spell: lambda state: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton, state),
            DropLocation.giant_dark_urn: lambda state: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton, state),
            DropLocation.giant_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton, state),
            DropLocation.giant_mana_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton, state),
            DropLocation.giant_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.giant_skeleton, state),
            DropLocation.lupine_spell: lambda state: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton, state),
            DropLocation.lupine_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton, state),
            DropLocation.lupine_onyx: lambda state: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton, state),
            DropLocation.lupine_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.lupine_skeleton, state),
            DropLocation.infested_antidote: lambda state: self.can_reach_and_hurt_enemy(Enemy.infested_corpse, state),
            DropLocation.infested_bones: lambda state: self.can_reach_and_hurt_enemy(Enemy.infested_corpse, state),
            DropLocation.sucsarian_drop_1: lambda state: self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger, state),
            DropLocation.sucsarian_drop_2: lambda state: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear, state),
            DropLocation.sucsarian_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear, state) or self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger, state),
            DropLocation.sucsarian_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear, state) or self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger, state),
            DropLocation.sucsarian_snowflake_obsidian: lambda state: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear, state) or self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger, state),
            DropLocation.sucsarian_throwing_knife: lambda state: self.can_reach_and_hurt_enemy(Enemy.sucsarian_spear, state) or self.can_reach_and_hurt_enemy(Enemy.sucsarian_dagger, state),
            DropLocation.vesta_fairy_moss: lambda state: self.can_reach_and_hurt_enemy(Enemy.vesta, state),
            DropLocation.vesta_yellow_morel: lambda state: self.can_reach_and_hurt_enemy(Enemy.vesta, state),
            DropLocation.vesta_dest_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.vesta, state),
            DropLocation.ceres_fairy_moss: lambda state: self.can_reach_and_hurt_enemy(Enemy.ceres, state),
            DropLocation.ceres_yellow_morel: lambda state: self.can_reach_and_hurt_enemy(Enemy.ceres, state),
            DropLocation.ceres_dest_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.ceres, state),
            DropLocation.gloom_fairy_moss: lambda state: self.can_reach_and_hurt_enemy(Enemy.gloom_wood, state),
            DropLocation.gloom_health_vial: lambda state: self.can_reach_and_hurt_enemy(Enemy.gloom_wood, state),
            DropLocation.gloom_dest_angel: lambda state: self.can_reach_and_hurt_enemy(Enemy.gloom_wood, state),
            DropLocation.cetea_drop: lambda state: self.can_reach_and_hurt_enemy(Enemy.cetea, state),
            DropLocation.cetea_10c: lambda state: self.can_reach_and_hurt_enemy(Enemy.cetea, state),
            DropLocation.cetea_ocean_bone_shell: lambda state: self.can_reach_and_hurt_enemy(Enemy.cetea, state),
            DropLocation.sea_demon: lambda state: self.can_reach_any_region(state, immovable_enemies[Enemy.demon]),
            DropLocation.sanguis_book: lambda state: self.can_reach_and_hurt_enemy("Sanguis Umbra", state),

            # All Quenchsanity Rules
            Quench.rapier: lambda state: self.can_get_weapon(state, Weapon.rapier, self.world.options),
            Quench.shadow_blade: lambda state: self.can_get_weapon(state, Weapon.shadow_blade, self.world.options),
            Quench.shining_blade: lambda state: self.can_get_weapon(state, Weapon.shining_blade, self.world.options),
            Quench.rusted_sword: lambda state: self.can_get_weapon(state, Weapon.rusted_sword, self.world.options),
            Quench.torch: lambda state: self.can_get_weapon(state, Weapon.torch, self.world.options),
            Quench.replica_sword: lambda state: self.can_get_weapon(state, Weapon.replica_sword, self.world.options),
            Quench.obsidian_poisonguard: lambda state: self.can_get_weapon(state, Weapon.obsidian_poisonguard, self.world.options),
            Quench.obsidian_cursebrand: lambda state: self.can_get_weapon(state, Weapon.obsidian_cursebrand, self.world.options),
            Quench.lyrian_longsword: lambda state: self.can_get_weapon(state, Weapon.lyrian_longsword, self.world.options),
            Quench.elfen_sword: lambda state: self.can_get_weapon(state, Weapon.elfen_sword, self.world.options),
            Quench.crossbow: lambda state: self.can_get_weapon(state, Weapon.crossbow, self.world.options),
            Quench.broken_lance: lambda state: self.can_get_weapon(state, Weapon.broken_lance, self.world.options),
            Quench.broken_hilt: lambda state: self.can_get_weapon(state, Weapon.broken_hilt, self.world.options),
            Quench.brittle_arming_sword: lambda state: self.can_get_weapon(state, Weapon.brittle_arming_sword, self.world.options),
            Quench.stone_club: lambda state: self.can_get_weapon(state, Weapon.stone_club, self.world.options),
            Quench.iron_club: lambda state: self.can_get_weapon(state, Weapon.iron_club, self.world.options),
            Quench.iron_claw: lambda state: self.can_get_weapon(state, Weapon.iron_claw, self.world.options),
            Quench.steel_claw: lambda state: self.can_get_weapon(state, Weapon.steel_claw, self.world.options),
            Quench.obsidian_seal: lambda state: self.can_get_weapon(state, Weapon.obsidian_seal, self.world.options),
            Quench.scythe: lambda state: self.can_kill_death(state, self.world.options),

            # All Etna's Pupil Rules
            AlchemyLocation.explosives: lambda state: self.can_obtain_all_alchemy_items([Alchemy.ashes, Alchemy.fire_opal], state, self.world.options),
            AlchemyLocation.knife: lambda state: self.can_obtain_alchemy_item(Alchemy.ocean_bone_shard, state, self.world.options),
            AlchemyLocation.health: lambda state: self.can_obtain_all_alchemy_items([Alchemy.opal, Alchemy.yellow_morel, Alchemy.lotus_seed_pod],
                                                                                    state, self.world.options),
            AlchemyLocation.mana: lambda state: self.can_obtain_all_alchemy_items([Alchemy.opal, Alchemy.onyx, Alchemy.lotus_seed_pod], state,
                                                                                  self.world.options),
            AlchemyLocation.moonlight: lambda state: self.can_obtain_all_alchemy_items([Alchemy.ashes, Alchemy.moon_petal, Alchemy.obsidian], state,
                                                                                       self.world.options),
            AlchemyLocation.spectral: lambda state: self.can_obtain_all_alchemy_items([Alchemy.ectoplasm, Alchemy.ikurrilb_root, Alchemy.fire_opal], state,
                                                                                      self.world.options),
            AlchemyLocation.poison_knife: lambda state: self.can_obtain_all_alchemy_items([Alchemy.destroying_angel_mushroom, Alchemy.ocean_bone_shell], state,
                                                                                          self.world.options),
            AlchemyLocation.staff_of_osiris: lambda state: self.can_obtain_all_alchemy_items([Alchemy.onyx, Alchemy.ikurrilb_root, Alchemy.bones], state,
                                                                                             self.world.options),
            AlchemyLocation.poison_urn: lambda state: self.can_obtain_all_alchemy_items([Alchemy.destroying_angel_mushroom, Alchemy.ocean_bone_shard,
                                                                                         Alchemy.bloodweed], state, self.world.options),
            AlchemyLocation.fairy_moss: lambda state: self.can_obtain_all_alchemy_items([Alchemy.moon_petal, Alchemy.bloodweed, Alchemy.yellow_morel], state,
                                                                                        self.world.options),
            AlchemyLocation.antidote: lambda state: self.can_obtain_all_alchemy_items([Alchemy.destroying_angel_mushroom, Alchemy.lotus_seed_pod], state,
                                                                                      self.world.options),
            AlchemyLocation.banner: lambda state: self.can_obtain_all_alchemy_items([Alchemy.ashes, Alchemy.bones], state,
                                                                                    self.world.options),
            AlchemyLocation.holy: lambda state: self.can_obtain_all_alchemy_items([Alchemy.moon_petal, Alchemy.opal], state,
                                                                                  self.world.options),
            AlchemyLocation.warp: lambda state: self.can_obtain_all_alchemy_items([Alchemy.snowflake_obsidian, Alchemy.onyx, Alchemy.obsidian], state,
                                                                                  self.world.options),
            AlchemyLocation.wisp: lambda state: self.can_obtain_all_alchemy_items([Alchemy.snowflake_obsidian, Alchemy.ectoplasm, Alchemy.moon_petal], state,
                                                                                  self.world.options),
            AlchemyLocation.limbo: lambda state: state.has_all([Alchemy.broken_sword, Alchemy.fractured_life, Alchemy.fractured_death], self.player),

            SpookyLocation.spooky_spell: lambda state: state.has(SpookyItem.soul_candy, self.player, 35),
            SpookyLocation.headless_horseman: lambda state: self.has_element_access(Elements.fire, state) and
                                                            self.can_level_reasonably(state, self.world.options),

            LevelLocation.level_2: lambda state: self.can_reach_level_in_levelsanity(2, state),
            LevelLocation.level_3: lambda state: self.can_reach_level_in_levelsanity(3, state),
            LevelLocation.level_4: lambda state: self.can_reach_level_in_levelsanity(4, state),
            LevelLocation.level_5: lambda state: self.can_reach_level_in_levelsanity(5, state),
            LevelLocation.level_6: lambda state: self.can_reach_level_in_levelsanity(6, state),
            LevelLocation.level_7: lambda state: self.can_reach_level_in_levelsanity(7, state),
            LevelLocation.level_8: lambda state: self.can_reach_level_in_levelsanity(8, state),
            LevelLocation.level_9: lambda state: self.can_reach_level_in_levelsanity(9, state),
            LevelLocation.level_10: lambda state: self.can_reach_level_in_levelsanity(10, state),
            LevelLocation.level_11: lambda state: self.can_reach_level_in_levelsanity(11, state),
            LevelLocation.level_12: lambda state: self.can_reach_level_in_levelsanity(12, state),
            LevelLocation.level_13: lambda state: self.can_reach_level_in_levelsanity(13, state),
            LevelLocation.level_14: lambda state: self.can_reach_level_in_levelsanity(14, state),
            LevelLocation.level_15: lambda state: self.can_reach_level_in_levelsanity(15, state),
            LevelLocation.level_16: lambda state: self.can_reach_level_in_levelsanity(16, state),
            LevelLocation.level_17: lambda state: self.can_reach_level_in_levelsanity(17, state),
            LevelLocation.level_18: lambda state: self.can_reach_level_in_levelsanity(18, state),
            LevelLocation.level_19: lambda state: self.can_reach_level_in_levelsanity(19, state),
            LevelLocation.level_20: lambda state: self.can_reach_level_in_levelsanity(20, state),
            LevelLocation.level_21: lambda state: self.can_reach_level_in_levelsanity(21, state),
            LevelLocation.level_22: lambda state: self.can_reach_level_in_levelsanity(22, state),
            LevelLocation.level_23: lambda state: self.can_reach_level_in_levelsanity(23, state),
            LevelLocation.level_24: lambda state: self.can_reach_level_in_levelsanity(24, state),
            LevelLocation.level_25: lambda state: self.can_reach_level_in_levelsanity(25, state),
            LevelLocation.level_26: lambda state: self.can_reach_level_in_levelsanity(26, state),
            LevelLocation.level_27: lambda state: self.can_reach_level_in_levelsanity(27, state),
            LevelLocation.level_28: lambda state: self.can_reach_level_in_levelsanity(28, state),
            LevelLocation.level_29: lambda state: self.can_reach_level_in_levelsanity(29, state),
            LevelLocation.level_30: lambda state: self.can_reach_level_in_levelsanity(30, state),
            LevelLocation.level_31: lambda state: self.can_reach_level_in_levelsanity(31, state),
            LevelLocation.level_32: lambda state: self.can_reach_level_in_levelsanity(32, state),
            LevelLocation.level_33: lambda state: self.can_reach_level_in_levelsanity(33, state),
            LevelLocation.level_34: lambda state: self.can_reach_level_in_levelsanity(34, state),
            LevelLocation.level_35: lambda state: self.can_reach_level_in_levelsanity(35, state),
            LevelLocation.level_36: lambda state: self.can_reach_level_in_levelsanity(36, state),
            LevelLocation.level_37: lambda state: self.can_reach_level_in_levelsanity(37, state),
            LevelLocation.level_38: lambda state: self.can_reach_level_in_levelsanity(38, state),
            LevelLocation.level_39: lambda state: self.can_reach_level_in_levelsanity(39, state),
            LevelLocation.level_40: lambda state: self.can_reach_level_in_levelsanity(40, state),
            LevelLocation.level_41: lambda state: self.can_reach_level_in_levelsanity(41, state),
            LevelLocation.level_42: lambda state: self.can_reach_level_in_levelsanity(42, state),
            LevelLocation.level_43: lambda state: self.can_reach_level_in_levelsanity(43, state),
            LevelLocation.level_44: lambda state: self.can_reach_level_in_levelsanity(44, state),
            LevelLocation.level_45: lambda state: self.can_reach_level_in_levelsanity(45, state),
            LevelLocation.level_46: lambda state: self.can_reach_level_in_levelsanity(46, state),
            LevelLocation.level_47: lambda state: self.can_reach_level_in_levelsanity(47, state),
            LevelLocation.level_48: lambda state: self.can_reach_level_in_levelsanity(48, state),
            LevelLocation.level_49: lambda state: self.can_reach_level_in_levelsanity(49, state),
            LevelLocation.level_50: lambda state: self.can_reach_level_in_levelsanity(50, state),
            LevelLocation.level_51: lambda state: self.can_reach_level_in_levelsanity(51, state),
            LevelLocation.level_52: lambda state: self.can_reach_level_in_levelsanity(52, state),
            LevelLocation.level_53: lambda state: self.can_reach_level_in_levelsanity(53, state),
            LevelLocation.level_54: lambda state: self.can_reach_level_in_levelsanity(54, state),
            LevelLocation.level_55: lambda state: self.can_reach_level_in_levelsanity(55, state),
            LevelLocation.level_56: lambda state: self.can_reach_level_in_levelsanity(56, state),
            LevelLocation.level_57: lambda state: self.can_reach_level_in_levelsanity(57, state),
            LevelLocation.level_58: lambda state: self.can_reach_level_in_levelsanity(58, state),
            LevelLocation.level_59: lambda state: self.can_reach_level_in_levelsanity(59, state),
            LevelLocation.level_60: lambda state: self.can_reach_level_in_levelsanity(60, state),
            LevelLocation.level_61: lambda state: self.can_reach_level_in_levelsanity(61, state),
            LevelLocation.level_62: lambda state: self.can_reach_level_in_levelsanity(62, state),
            LevelLocation.level_63: lambda state: self.can_reach_level_in_levelsanity(63, state),
            LevelLocation.level_64: lambda state: self.can_reach_level_in_levelsanity(64, state),
            LevelLocation.level_65: lambda state: self.can_reach_level_in_levelsanity(65, state),
            LevelLocation.level_66: lambda state: self.can_reach_level_in_levelsanity(66, state),
            LevelLocation.level_67: lambda state: self.can_reach_level_in_levelsanity(67, state),
            LevelLocation.level_68: lambda state: self.can_reach_level_in_levelsanity(68, state),
            LevelLocation.level_69: lambda state: self.can_reach_level_in_levelsanity(69, state),
            LevelLocation.level_70: lambda state: self.can_reach_level_in_levelsanity(70, state),
            LevelLocation.level_71: lambda state: self.can_reach_level_in_levelsanity(71, state),
            LevelLocation.level_72: lambda state: self.can_reach_level_in_levelsanity(72, state),
            LevelLocation.level_73: lambda state: self.can_reach_level_in_levelsanity(73, state),
            LevelLocation.level_74: lambda state: self.can_reach_level_in_levelsanity(74, state),
            LevelLocation.level_75: lambda state: self.can_reach_level_in_levelsanity(75, state),
            LevelLocation.level_76: lambda state: self.can_reach_level_in_levelsanity(76, state),
            LevelLocation.level_77: lambda state: self.can_reach_level_in_levelsanity(77, state),
            LevelLocation.level_78: lambda state: self.can_reach_level_in_levelsanity(78, state),
            LevelLocation.level_79: lambda state: self.can_reach_level_in_levelsanity(79, state),
            LevelLocation.level_80: lambda state: self.can_reach_level_in_levelsanity(80, state),
            LevelLocation.level_81: lambda state: self.can_reach_level_in_levelsanity(81, state),
            LevelLocation.level_82: lambda state: self.can_reach_level_in_levelsanity(82, state),
            LevelLocation.level_83: lambda state: self.can_reach_level_in_levelsanity(83, state),
            LevelLocation.level_84: lambda state: self.can_reach_level_in_levelsanity(84, state),
            LevelLocation.level_85: lambda state: self.can_reach_level_in_levelsanity(85, state),
            LevelLocation.level_86: lambda state: self.can_reach_level_in_levelsanity(86, state),
            LevelLocation.level_87: lambda state: self.can_reach_level_in_levelsanity(87, state),
            LevelLocation.level_88: lambda state: self.can_reach_level_in_levelsanity(88, state),
            LevelLocation.level_89: lambda state: self.can_reach_level_in_levelsanity(89, state),
            LevelLocation.level_90: lambda state: self.can_reach_level_in_levelsanity(90, state),
            LevelLocation.level_91: lambda state: self.can_reach_level_in_levelsanity(91, state),
            LevelLocation.level_92: lambda state: self.can_reach_level_in_levelsanity(92, state),
            LevelLocation.level_93: lambda state: self.can_reach_level_in_levelsanity(93, state),
            LevelLocation.level_94: lambda state: self.can_reach_level_in_levelsanity(94, state),
            LevelLocation.level_95: lambda state: self.can_reach_level_in_levelsanity(95, state),
            LevelLocation.level_96: lambda state: self.can_reach_level_in_levelsanity(96, state),
            LevelLocation.level_97: lambda state: self.can_reach_level_in_levelsanity(97, state),
            LevelLocation.level_98: lambda state: self.can_reach_level_in_levelsanity(98, state),
            LevelLocation.level_99: lambda state: self.can_reach_level_in_levelsanity(99, state),
            LevelLocation.level_100: lambda state: self.can_reach_level_in_levelsanity(100, state),

            LoreLocation.golden_plea: lambda state: self.has_element_access(Elements.fire_options, state),

            GrassLocation.yf_mushroom_48: lambda state: self.has_blood_spell_access(state),
            GrassLocation.yf_mushroom_34: lambda state:  self.has_blood_spell_access(state),
            BreakLocation.hb_vase_105: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            BreakLocation.hb_vase_39: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            BreakLocation.hb_vase_65: lambda state: self.can_jump_given_height(JumpHeight.low, state, self.world.options),
            GrassLocation.fla_fiddlehead_14: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            GrassLocation.fla_fiddlehead_27: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            GrassLocation.fla_fiddlehead_11: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            GrassLocation.fla_fiddlehead_22: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            GrassLocation.fla_lotus_15: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
            GrassLocation.fla_lotus_18: lambda state: self.can_jump_given_height(JumpHeight.high, state, self.world.options),
        }

    def can_reach_and_hurt_enemy(self, name: str, state: CollectionState):
        if name in self.enemy_regions:
            region_rule = self.can_reach_any_region(state, self.enemy_regions[name])
        else:
            region_rule = self.can_reach_any_region(state, immovable_enemies[name])
        if name not in all_enemy_data_by_name:
            attack_rule = True
        else:
            possible_weapons = [weapon for weapon in self.elements if self.elements[weapon] not in all_enemy_data_by_name[name].immune and weapon not in support_spells]
            attack_rule = state.has_any(possible_weapons, self.player)
        return region_rule and attack_rule

    def has_aoe_spell(self, state: CollectionState, options: LunacidOptions):
        level_rule = True
        if options.levelsanity:
            level_rule = self.can_reach_level_in_levelsanity(30, state)
        aoe_spells = [Spell.ice_tear, Spell.moon_beam, Spell.blue_flame_arc, Spell.lava_chasm]

        return state.has_any(aoe_spells, self.player) and level_rule

    @staticmethod
    def is_vampire(options: LunacidOptions) -> bool:
        return options.starting_class == options.starting_class.option_vampire

    def can_reach_any_region(self, state: CollectionState, spots: List[str]) -> bool:
        for spot in spots:
            if state.can_reach_region(spot, self.player):
                return True
        return False

    def can_reach_all_regions(self, state: CollectionState, spots: List[str]) -> bool:
        all_rule = True
        for spot in spots:
            all_rule = all_rule and state.can_reach_region(spot, self.player)
        return all_rule

    def can_reach_location(self, state: CollectionState, spot: str) -> bool:
        return state.can_reach(spot, "Location", self.player)

    def can_jump_given_height(self, height: str, state: CollectionState, options: LunacidOptions) -> bool:
        if height == JumpHeight.low:
            level_rule = not options.levelsanity or state.has(CustomItem.experience, self.player, 10)
            return level_rule or state.has(Glitch.item, self.player)
        elif height == JumpHeight.medium:
            medium_spells = {Spell.barrier, Spell.icarian_flight, Spell.coffin, Spell.rock_bridge}
            if options.dropsanity:
                medium_spells.add(MobSpell.summon_snail)
            return state.has_any(medium_spells, self.player) or state.has(Glitch.item, self.player)
        else:
            high_spells = {Spell.barrier, Spell.rock_bridge}
            return state.has_any(high_spells, self.player) or state.has(Spell.icarian_flight, self.player)

    def has_door_key(self, key: str, state: CollectionState, options: LunacidOptions) -> bool:
        return not options.door_locks or state.has(key, self.player)

    def has_light_source(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.starting_area == options.starting_area.option_tomb:
            return True
        sources = base_light_sources.copy()
        sources.extend(source for source in shop_light_sources)
        sources.extend(source for source in drop_light_sources)
        sources.extend(source for source in quench_light_sources)
        if options.quenchsanity:
            sources.remove(Weapon.broken_hilt)
        if options.etnas_pupil:
            limbo_rule = state.has(Weapon.limbo, self.player)
        else:
            limbo_rule = state.has_all([Alchemy.broken_sword, Alchemy.fractured_life, Alchemy.fractured_death], self.player)
        return state.has_any(sources, self.player) or limbo_rule or state.has(Glitch.item, self.player) or self.lightless

    def can_reach_level_in_levelsanity(self, level: int, state: CollectionState):

        if level <= 10:
            return state.has(CustomItem.experience, self.player, max(level - self.level, 0)) or state.has(Glitch.item, self.player)
        has_bangle = True
        level_cap = 0
        for region in region_to_level_value:
            if state.can_reach_region(region, self.player):
                level_cap += region_to_level_value[region]
        level_cap *= 10
        if level >= 50:
            has_bangle = state.has(CustomItem.lucky_bangle, self.player)
        return (state.has(CustomItem.experience, self.player, max(level - self.level, 0)) and has_bangle and level_cap >= level) or state.has(Glitch.item, self.player)

    def can_level_reasonably(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.levelsanity:
            return state.has(CustomItem.experience, self.player, 40) or state.has(Glitch.item, self.player)
        can_you = options.starting_area != options.starting_area.option_basin
        if not can_you:
            # The player should be able to find SOME place to run off to in order to level.
            # Writing it like this avoids a region check.
            can_escape_basin_start_in_all_directions = (self.has_light_source(state, options) and self.has_keys_for_basin_or_canopy(state, options) and
                                                        self.has_door_key(Door.basin_broken_steps, state, options) and
                                                        self.has_switch_key(Switch.temple_switch, state, options) and
                                                        self.can_jump_given_height(JumpHeight.high, state, options))
            can_you = can_escape_basin_start_in_all_directions
        return can_you or state.has(Glitch.item, self.player)

    def has_spell(self, spell: str, state: CollectionState) -> bool:
        return state.has(spell, self.player)

    def has_all_spells(self, spells: List[str], state: CollectionState) -> bool:
        has_spells = True
        for spell in spells:
            has_spell = state.has(spell, self.player)
            has_spells = has_spells and has_spell
        return has_spells

    def has_every_spell(self, state: CollectionState, options: LunacidOptions, starting_weapon: str = None) -> bool:
        every_spell = []
        if options.dropsanity == options.dropsanity.option_off:
            every_spell = Spell.base_spells.copy()
        else:
            every_spell = list(set.union(set(Spell.base_spells), set(MobSpell.drop_spells)))
        if starting_weapon in every_spell:
            every_spell.remove(starting_weapon)
        if options.dropsanity == options.dropsanity.option_off:
            return self.has_all_spells(every_spell, state) and self.can_reach_every_necessary_mob_for_spells(state)
        else:
            return self.has_all_spells(every_spell, state)

    def can_reach_every_necessary_mob_for_spells(self, state: CollectionState):
        return (self.can_reach_monster(Enemy.chimera, state) and self.can_reach_monster(Enemy.kodama, state) and self.can_reach_monster(Enemy.skeleton, state) and
                self.can_reach_monster(Enemy.skeleton_weapon, state) and (self.can_reach_monster(Enemy.lupine_skeleton, state) or
                self.can_reach_monster(Enemy.giant_skeleton, state)) and self.can_reach_monster(Enemy.cetea, state) and self.can_reach_monster(Enemy.snail, state))

    def can_purchase_item(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.shopsanity == options.shopsanity.option_false:
            return True
        return ((state.can_reach_region(LunacidRegion.boiling_grotto, self.player) and state.has(Spell.ignis_calor, self.player)) or
                self.can_reach_location(state, BaseLocation.fate_lucid_blade))

    def has_blood_spell_access(self, state: CollectionState) -> bool:
        return state.has_any(blood_spells, self.player)

    def has_keys_for_basin_or_canopy(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.shopsanity == options.shopsanity.option_false:
            return state.has(UniqueItem.enchanted_key, self.player)
        return state.has(UniqueItem.enchanted_key, self.player, 2)

    def has_switch_key(self, key: str, state: CollectionState, options: LunacidOptions) -> bool:
        return not options.switch_locks or state.has(key, self.player)

    def has_crystal_orb(self, state: CollectionState, options: LunacidOptions) -> bool:
        if not options.secret_door_lock:
            return True
        return state.has(UniqueItem.dusty_crystal_orb, self.player)

    def has_element_access(self, element: str | List[str], state: CollectionState) -> bool:
        if isinstance(element, str):
            element = [element]
        element_options = [item for item in self.elements if self.elements[item] in element]
        return state.has_any(element_options, self.player) or state.has(Weapon.wand_of_power, self.player)

    def has_ranged_element_access(self, element: str | List[str], state: CollectionState) -> bool:
        if isinstance(element, str):
            element = [element]
        ranged_options = [item for item in ranged_weapons]
        ranged_options.extend([item for item in ranged_spells])
        element_options = [item for item in self.elements if self.elements[item] in element and item in ranged_options]
        return state.has_any(element_options, self.player)

    def has_coins_for_door(self, options: LunacidOptions, state: CollectionState) -> bool:
        return state.has(Coins.strange_coin, self.player, options.required_strange_coin.value)

    def can_buy_jotunn(self, options: LunacidOptions, state: CollectionState) -> bool:
        if options.shopsanity:
            return state.has(Weapon.jotunn_slayer, self.player)
        return (self.can_reach_location(state, BaseLocation.fate_lucid_blade)
                and (state.has(Voucher.sheryl_dreamer_voucher, self.player) or state.has(Glitch.item, self.player)))

    def can_defeat_the_prince(self, state: CollectionState, options: LunacidOptions) -> bool:
        return (self.has_element_access(Elements.light_options, state) and self.can_level_reasonably(state, options)) or state.has(Glitch.item, self.player)

    def can_reach_monster(self, enemy: str, state: CollectionState) -> bool:
        locations = self.enemy_regions[enemy]
        return self.can_reach_any_region(state, locations)

    def can_get_weapon(self, state: CollectionState, weapon: str, options: LunacidOptions) -> bool:
        if self.world.starting_weapon.name == weapon:
            return True
        if weapon in Weapon.base_weapons:
            return state.has(weapon, self.player)
        elif weapon in Weapon.shop_weapons:
            if options.shopsanity:
                return state.has(weapon, self.player)
            return state.has(Voucher.sheryl_initial_voucher, self.player)
        elif weapon in Weapon.drop_weapons:
            if options.dropsanity:
                return state.has(weapon, self.player)
            for enemy in all_drops_by_enemy:
                if weapon in all_drops_by_enemy[enemy]:
                    return self.can_reach_any_region(state, self.enemy_regions[enemy])
        elif weapon in Weapon.quenchsanity_weapons:
            return state.has(weapon, self.player)
        return False

    def can_kill_death(self, state: CollectionState, options: LunacidOptions) -> bool:
        if options.etnas_pupil:
            return state.has(Weapon.limbo, self.player) and state.can_reach_region(LunacidRegion.mausoleum, self.player)

        return state.has_all({Alchemy.fractured_life, Alchemy.fractured_death, Alchemy.broken_sword},
                             self.player) and state.can_reach_region(LunacidRegion.mausoleum, self.player)

    def can_obtain_alchemy_item(self, alchemy_item: str, state: CollectionState, options: LunacidOptions) -> bool:
        if options.etnas_pupil and options.dropsanity == options.dropsanity.option_randomized:
            return state.has(alchemy_item, self.player)
        acceptable_regions = []
        for enemy in all_drops_by_enemy:
            if alchemy_item in all_drops_by_enemy[enemy]:
                for region in self.enemy_regions[enemy]:
                    if region not in acceptable_regions:
                        acceptable_regions.append(region)
        for plant in all_alchemy_plant_data:
            if alchemy_item == plant.drop:
                for region in plant.regions:
                    if region not in acceptable_regions:
                        acceptable_regions.append(region)
        region_rule = self.can_reach_any_region(state, acceptable_regions)
        return region_rule

    def can_obtain_all_alchemy_items(self, alchemy_items: List[str], state: CollectionState, options: LunacidOptions) -> bool:
        alchemy_rule = True
        for item in alchemy_items:
            alchemy_rule = alchemy_rule and self.can_obtain_alchemy_item(item, state, options)
        return alchemy_rule

    def can_rock_bridge_skip(self, state: CollectionState):
        return self.barrier and state.has(Spell.rock_bridge, self.player)

    def set_lunacid_rules(self, world_elements: Dict[str, str], enemy_regions: Dict[str, List[str]]) -> None:
        multiworld = self.world.multiworld
        self.elements = world_elements
        self.enemy_regions = enemy_regions
        for region in self.world.get_regions():
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
                for location in region.locations:
                    location.access_rule = self.region_rules[region.name]
            for entrance in region.entrances:
                if entrance.name in self.entrance_rules:
                    entrance.access_rule = entrance.access_rule and self.entrance_rules[entrance.name]
                if entrance.name in indirect_entrances:
                    indirect_region = self.world.get_region(indirect_entrances[entrance.name])
                    multiworld.register_indirect_condition(indirect_region, entrance)
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = loc.access_rule and self.location_rules[loc.name]

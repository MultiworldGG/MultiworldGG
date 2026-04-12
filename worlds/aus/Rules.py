from typing import Dict, TYPE_CHECKING
from worlds.AutoWorld import LogicMixin
from worlds.generic.Rules import CollectionRule, set_rule, add_rule, add_item_rule
from BaseClasses import MultiWorld, CollectionState
from . import Options
from .Names import *

if TYPE_CHECKING:
    from . import AUSWorld


class AUSRules:
    player: int
    world: "AUSWorld"
    region_rules: Dict[str, CollectionRule]
    location_rules: Dict[str, CollectionRule]
    boss_drop_values: Dict[str, int]
    maximum_price: int
    required_seals: int 

    def __init__(self, world: "AUSWorld") -> None:
        self.player = world.player
        self.world = world

        self.region_rules = {
            A_NIGHTCLIMB: lambda state: self.jump_height_min(state, 5) and self.has_fire(state) and self.double_jump_min(state, 1),
            A_DEEPDIVE: lambda state: self.jump_height(state) + (self.can_duck(state) and self.has_red_energy(state)) * 2 >= 8 and
                                      self.can_divebomb(state) and (self.hatched(state) or (world.options.hard_logic and self.jump_height_min(state, 8))),
            A_FIRECAGE: lambda state: self.can_stick(state) and self.has_red_energy(state) and self.single_jump_min(state, 2) and (self.can_shoot(state) or world.options.hard_logic),
            A_MOUNTSIDE: lambda state: self.jump_height(state) + self.can_duck(state) * 2 >= 8 and
                                       self.has_red_energy(state) and (self.hatched(state) or (world.options.hard_logic and self.jump_height_min(state, 8))),
            A_THE_CURTAIN: lambda state: self.jump_height_min(state, 8) and self.can_slide(state) and
                                         state.has_all({I_YELLOW_ENERGY, I_SHOOT_ICE}, self.player),
            A_SKYSAND: lambda state: self.single_jump_min(state, 2) and self.double_jump_min(state, 2) and self.can_slide(state) and
                                     state.has_all({I_RED_ENERGY, I_SHOOT_FIRE, I_SHOOT_ICE}, self.player),
            A_DARK_GROTTO: lambda state: self.has_ice(state) and self.can_divebomb(state),
            A_FARFALL: lambda state: self.jump_height_min(state, 4) and state.has_all({I_RED_ENERGY, I_DIVE_BOMB}, self.player),
            A_STRANGECASTLE: lambda state: self.hatched(state) and (((self.jump_height(state) + self.can_stick(state)) >= 7)
                                                                or (world.options.hard_logic and self.can_stick(state) and (self.single_jump_min(state, 3) or self.double_jump_min(state, 1)) and (self.jump_height_min(state, 6) or self.can_slide(state)))),
            A_THE_BOTTOM: lambda state: self.jump_height_min(state, 6.5) and self.can_slide(state) and self.hatched(state),
            A_BLANCLAND: lambda state: self.jump_height_min(state, 8) and state.has(I_AIR_UPGRADE, self.player),
            R_DEEPDIVE_RIGHT: lambda state: self.jump_height_min(state, 7) and (self.single_jump_min(state, 3) or self.can_slide(state)),
            A_BLACKCASTLE: lambda state: state.has(I_GOLD_ORB, self.player, world.options.gold_orbs_required) and self.single_jump_min(state, 3) and
                                         self.double_jump_min(state, 2) and self.can_divebomb(state) and self.can_slide(state) and self.has_red_energy(state) and self.has_fire(state),
        }

        arcade_location_rules = {
            L_SKY_TOWN_ASTROCRASH: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 1400) and self.hatched(state),
            L_SKY_TOWN_JUMPBOX: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 1600) and self.hatched(state),
            L_SKY_TOWN_KEEPGOING: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 1800) and self.hatched(state),
        }

        blackcastle_location_rules = {
            L_BLACKCASTLE_BOSS: true,
            L_BLACKCASTLE_FLOWER: true,
            L_BLACKCASTLE_REDBLOCKS: true
        }

        blancland_location_rules = {
            L_BLANCLAND_FREEZE: lambda state: self.has_red_energy(state) and self.has_ice(state),
            L_BLANCLAND_KILL: lambda state: self.has_red_energy(state) and self.has_fire(state) and self.can_slide(state),
            L_BLANCLAND_POSTBOSS: lambda state: self.has_red_energy(state) and self.has_fire(state),
            L_BLANCLAND_BOSS: lambda state: self.has_red_energy(state) and self.has_fire(state),
            L_BLANCLAND_FLOWER: true
        }

        bonus_location_rules = {
            L_BONUS_1: true,
            L_BONUS_2: true,
        }

        bottom_location_rules = {
            L_THE_BOTTOM_CLOUD: true,
            L_THE_BOTTOM_FLOWER: true,
        }

        cloudrun_location_rules = {
            L_CLOUDRUN_FLOWER: true,
            L_CLOUDRUN_UNDER: lambda state: self.jump_height_min(state, 7),
            L_CLOUDRUN_MIDDLE: lambda state: self.jump_height_min(state, 7) and self.has_fire(state),
            L_CLOUDRUN_BOSS: lambda state: self.jump_height_min(state, 7) and self.has_fire(state) and self.has_ice(
                state),
            L_CLOUDRUN_POSTBOSS: lambda state: self.jump_height_min(state, 7) and self.has_fire(state) and self.has_ice(
                state),
            L_CLOUDRUN_FARRIGHT: lambda state: self.jump_height_min(state, 7) and self.has_fire(
                state) and self.has_ice(state),
        }

        coldkeep_location_rules = {
            L_COLDKEEP_CANNON: lambda state: self.has_ice(state) and (self.jump_height_min(state, 5) or (world.options.closed_end_logic and self.jump_height_min(state, 4))),
            L_COLDKEEP_BOSS: lambda state: self.jump_height_min(state, 5) or (world.options.hard_logic and self.jump_height_min(state, 4) and (self.can_divebomb(state) or self.has_ice(state))),
            L_COLDKEEP_POSTBOSS: lambda state: self.jump_height_min(state, 5) or (world.options.hard_logic and self.jump_height_min(state, 4) and (self.can_divebomb(state) or self.has_ice(state))),
            L_COLDKEEP_UPPER: lambda state: self.jump_height_min(state, 4),
            L_COLDKEEP_LOWER: lambda state: self.jump_height_min(state, 4),
        }

        the_curtain_location_rules = {
            L_THE_CURTAIN_FLOWER: lambda state: self.has_yellow_energy(state) and (self.double_jump_min(state, 3) or (
                        self.can_slide(state) and self.double_jump_min(state, 2))) and self.has_ice(state),
            L_THE_CURTAIN_KILL: true,
            L_THE_CURTAIN_BREAKABLE: lambda state: self.can_divebomb(state),
            L_THE_CURTAIN_BOSS: true,
            L_THE_CURTAIN_POSTBOSS: true,
        }

        dark_grotto_location_rules = {
            L_DARK_GROTTO_UPPER: lambda state: self.has_yellow_energy(state) and self.jump_height_min(state, 7),
            L_DARK_GROTTO_CAMPSITE: true,
            L_DARK_GROTTO_BOSS: true,
            L_DARK_GROTTO_POSTBOSS: true,
            L_DARK_GROTTO_TORCHES: true,
            L_DARK_GROTTO_FLOWER: true,
        }

        deepdive_location_rules = {
            L_DEEPDIVE_LEFT: lambda state: self.double_jump_min(state, 3),
            L_DEEPDIVE_CHEST: lambda state: self.double_jump_min(state, 3),
            L_DEEPDIVE_LEFTCEILING: lambda state: self.double_jump_min(state, 3),
            L_DEEPDIVE_TOP: true,
            L_DEEPDIVE_LEFTFISHNOOK: lambda state: (self.has_ice(state) or self.jump_height_min(state, 8)),
            L_DEEPDIVE_1FISHROOM: lambda state: self.has_ice(state) and self.jump_height_min(state,
                                                                                             6.5) and state.has(
                I_AIR_UPGRADE, self.player),
            L_DEEPDIVE_MIDDLEROOM: true,
            L_DEEPDIVE_BOTTOM: lambda state: self.jump_height_min(state, 8) and state.has(I_AIR_UPGRADE,
                                                                                          self.player, 2),
            L_DEEPDIVE_CARGO: lambda state: self.jump_height_min(state, 7),
            L_DEEPDIVE_BOSS: true,
            L_DEEPDIVE_INBLOCK: true,
            L_DEEPDIVE_RIGHTFISHNOOK: lambda state: self.has_ice(state),
            L_DEEPDIVE_FLOWER: true,
            L_DEEPDIVE_POSTBOSS: true,
            L_DEEPDIVE_SPIKEPATH: true,
        }

        deeptower_location_rules = {
            L_DEEPTOWER_DOOR: true,
            L_DEEPTOWER_BOSS: lambda state: self.jump_height_min(state, 4),
            L_DEEPTOWER_POSTBOSS: lambda state: self.jump_height_min(state, 4),
            L_DEEPTOWER_SPIKES: lambda state: self.jump_height_min(state, 4) and (self.double_jump_height(state) + self.can_slide(state)),
        }

        farfall_location_rules = {
            L_FARFALL_KILL: lambda state: self.double_jump_min(state, 1) and (self.jump_height_min(state, 5) or (world.options.hard_logic and self.jump_height_min(state, 4))),    #considered part of stonecastle
            L_FARFALL_CHEST: lambda state: self.jump_height_min(state, 4),    #considered part of stonecastle
            L_FARFALL_5BALLOONS: lambda state: (self.jump_height_min(state, 7) or (world.options.hard_logic and self.jump_height_min(state, 6))) and self.hatched(state),
            L_FARFALL_SPECIALBALLOON: true,    #considered part of the bottom
            L_FARFALL_PITDOOR: lambda state: self.jump_height_min(state, 5) and self.double_jump_min(state,
                                                                                                     1) and self.can_divebomb(
                state) and self.has_red_energy(state),
            L_FARFALL_FLOWER: lambda state: self.jump_height_min(state, 5) and self.double_jump_min(state,
                                                                                                    1) and self.can_divebomb(
                state) and self.has_red_energy(state),
            L_FARFALL_PITEND: lambda state: self.jump_height_min(state, 5) and self.double_jump_min(state,
                                                                                                    1) and self.can_divebomb(
                state) and self.has_red_energy(state),
            L_FARFALL_YELLOWDOOR: lambda state: self.jump_height_min(state, 5) and self.double_jump_min(state,
                                                                                                        1) and self.can_divebomb(
                state) and self.has_red_energy(state) and (self.has_yellow_energy(state) or (world.options.hard_logic and self.single_jump_min(state, 3) and self.can_slide(state))),
            L_FARFALL_BOSS: true,    #considered part of strangecastle
            L_FARFALL_POSTBOSS: true,    #considered part of strangecastle
        }

        final_climb_location_rules = {
            VICTORY: true
        }

        firecage_location_rules = {
            L_FIRECAGE_TOLL: lambda state: self.hatched(state) and (self.can_slide(state) or self.has_fire(state)),
            L_FIRECAGE_LEFTSAVE: true,
            L_FIRECAGE_CRUSHERS: lambda state: self.can_shoot(state),
            L_FIRECAGE_UPPERDOOR: true,
            L_FIRECAGE_MIDDLE: lambda state: self.jump_height_min(state, 8) and (self.has_yellow_energy(state) or world.options.closed_end_logic),
            L_FIRECAGE_LOWERDOOR: lambda state: self.jump_height_min(state, 6.5) and (self.has_yellow_energy(state) or world.options.closed_end_logic),
            L_FIRECAGE_RIGHTSAVE: lambda state: self.jump_height_min(state, 6.5) and self.can_slide(state) and self.has_yellow_energy(state),
            L_FIRECAGE_POSTBOSS: lambda state: self.jump_height_min(state, 6.5) and (self.has_yellow_energy(state) or world.options.closed_end_logic) and self.hatched(state),
            L_FIRECAGE_BOSS: lambda state: self.jump_height_min(state, 6.5) and (self.has_yellow_energy(state) or world.options.closed_end_logic) and self.hatched(state),
        }

        grotto_location_rules = {
            L_GROTTO_POSTBOSS: lambda state: self.jump_height_min(state, 4) or (world.options.closed_end_logic and self.jump_height_min(state, 3)),
            L_GROTTO_BOSS: lambda state: self.jump_height_min(state, 4) or (world.options.closed_end_logic and self.jump_height_min(state, 3)),
            L_GROTTO_FLOWER: lambda state: (self.jump_height(state) + (
                    self.can_duck(state) and self.has_red_energy(state)) * 2 >= 8) and (self.hatched(state) or (world.options.hard_logic and self.jump_height_min(state, 8))),
            L_GROTTO_MURAL: lambda state: self.jump_height_min(state, 4) and
                                          (self.double_jump_min(state, 2) or (world.options.hard_logic and self.double_jump_min(state, 1) and self.can_stick(state))),
            L_GROTTO_POSTBOSS2: true,
            L_GROTTO_BOSS2: true,
        }

        highlands_location_rules = {
            L_HIGHLANDS_PLATFORM: lambda state: self.has_yellow_energy(state) and (self.double_jump_min(state, 3) or (
                        self.double_jump_min(state, 2) and self.can_slide(state))) and self.has_ice(state),
        }

        icecastle_location_rules = {
            L_ICECASTLE_LEFTOUTER: true,
            L_ICECASTLE_ENTRYDOOR: true,
            L_ICECASTLE_SPIKEFUNNEL: true,
            L_ICECASTLE_FLOWER: true,
            L_ICECASTLE_YELLOWDOOR: true,
            L_ICECASTLE_UNDERSIDE: lambda state: self.can_divebomb(state),
            L_ICECASTLE_TINYDOOR: true,
            L_ICECASTLE_CANNONDOOR: true,
            L_ICECASTLE_SPIKEFLOOR: true,
            L_ICECASTLE_POSTBOSS: lambda state: self.can_divebomb(state),
            L_ICECASTLE_BOSS: lambda state: self.can_divebomb(state),
            L_ICECASTLE_TOPRIGHT: true,
        }

        library_location_rules = {
            L_LIBRARY_UPPER: true,
            L_LIBRARY_FLOWER: true,
        }

        longbeach_location_rules = {
            L_LONGBEACH_FLOWER: lambda state: (state.can_reach(R_DEEPDIVE_RIGHT, "Region",
                                                               self.player) or state.can_reach(
                A_DARK_GROTTO, "Region", self.player)) and self.double_jump_min(state, 3) and self.can_slide(state),
        }

        mountside_location_rules = {
            L_MOUNTSIDE_FLOWER: lambda state: self.double_jump_min(state, 3) or world.options.closed_end_logic,
            L_MOUNTSIDE_DOOR: true,
        }

        nightclimb_location_rules = {
            L_NIGHTCLIMB_BOSS: true,
            L_NIGHTCLIMB_CANNONS: true,
            L_NIGHTCLIMB_TOP: true,
            L_NIGHTCLIMB_DUCK: lambda state: self.can_duck(state) and self.hatched(state),
            L_NIGHTCLIMB_UPPERSAVE: true,
            L_NIGHTCLIMB_FLOWER: true,
            L_NIGHTCLIMB_RIGHT: lambda state: self.jump_height_min(state, 5) and self.has_fire(state),
            L_NIGHTCLIMB_CHEST: lambda state: self.jump_height_min(state, 5) and self.has_fire(state),
        }

        nightwalk_location_rules = {
            L_NIGHTWALK_UPPEREND: true,
            L_NIGHTWALK_NESTFLOWER: true,
            L_NIGHTWALK_LOWERFLOWER: lambda state: self.jump_height_min(state, 5) or (world.options.hard_logic and self.jump_height_min(state, 4) and self.double_jump_min(state, 1)),
            L_NIGHTWALK_SKYRED: lambda state: (self.can_duck(state) and self.jump_height_min(state, 6) and (self.has_red_energy(state) and (
                        self.double_jump_min(state, 2) or self.can_slide(state)) or (world.options.hard_logic and self.double_jump_min(state, 3) and self.can_slide(state)))) or state.can_reach(A_THE_CURTAIN,
                                                                                                     "Region",
                                                                                                     self.player),
            L_NIGHTWALK_FIRST: true,
            L_NIGHTWALK_BREAKABLE: lambda state: self.can_divebomb(state) and (
                        self.jump_height_min(state, 2) or self.double_jump_min(state, 1)),
            L_NIGHTWALK_CHEST: true,
            L_NIGHTWALK_SKYTEMPLE: lambda state: (self.can_duck(state) and self.jump_height_min(state,
                                                                                                6) and self.double_jump_min(
                state, 1)) or state.can_reach(A_THE_CURTAIN, "Region", self.player),
            L_NIGHTWALK_GROUNDTEMPLE: lambda state: self.jump_height_min(state, 2.5),
            L_NIGHTWALK_TORCHES: lambda state: self.jump_height_min(state, 2.5) and self.can_light_torches(
                state),
            L_NIGHTWALK_UPPERFLOWER: true,
        }

        rainbowdive_location_rules = {
            L_RAINBOWDIVE_4TH: true,
            L_RAINBOWDIVE_3RD: true,
            L_RAINBOWDIVE_2ND: true,
            L_RAINBOWDIVE_1ST: lambda state: self.has_fire(state),
        }

        skylands_location_rules = {
            L_SKYLANDS_CHEST: true,
            L_SKYLANDS_TOLL: lambda state: self.hatched(state),
            L_SKYLANDS_DUCK: lambda state: self.can_divebomb(state) and self.can_duck(state) and self.hatched(state),
            L_SKYLANDS_BALLOONS: lambda state: self.can_divebomb(state) and (self.has_range(state) or world.options.hard_logic),
            L_SKYLANDS_PORTAL: true,
            L_SKYLANDS_DOOR: lambda state: self.can_divebomb(state),
            L_SKYLANDS_TOPRIGHT: lambda state: self.can_divebomb(state),
        }

        skysand_location_rules = {
            L_SKYSAND_LEFTSTATUE: true,
            L_SKYSAND_FLOWER: true,
            L_SKYSAND_BOTTOMSAVE: lambda state: self.has_ice(state) and (
                        self.has_red_energy(state) or self.jump_height_min(state, 8)) and self.can_stick(state),
            L_SKYSAND_POSTBOSS: true,
            L_SKYSAND_BOSS: true,
            L_SKYSAND_UPPERDOOR: true,
            L_SKYSAND_YELLOW: lambda state: self.has_yellow_energy(state) and self.double_jump_min(state, 3),
            L_SKYSAND_LOWERDOOR: true,
            L_SKYSAND_CHEST: true,
        }

        sky_town_location_rules = {
            L_SKY_TOWN_YELLOW: lambda state: self.jump_height_min(state, 4) and self.has_yellow_energy(state),
            L_SKY_TOWN_RED: lambda state: (self.jump_height_min(state, 4) and self.has_red_energy(state)) or (
                    state.can_reach(A_NIGHTCLIMB, "Region", self.player) and self.has_ice(state)),
            L_SKY_TOWN_SHOP1: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 100),
            L_SKY_TOWN_SHOP2: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 100),
            L_SKY_TOWN_SHOP3: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 100),
            L_SKY_TOWN_SHOP4: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 500),
            L_SKY_TOWN_SHOP5: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 500),
            L_SKY_TOWN_SHOP6: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 500),
            L_SKY_TOWN_SHOP7: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 500),
            L_SKY_TOWN_SHOP8: lambda state: self.jump_height_min(state, 4) and self.total_money(state, 1000),
            L_SKY_TOWN_TOWER: true,
            L_SKY_TOWN_FLOWER: lambda state: self.jump_height_min(state, 4),
            L_SKY_TOWN_PITLEFT: lambda state: self.jump_height_min(state, 5) and self.has_fire(state),
            # ST_PIT: lambda state: self.jump_height_min(state, 4),
            L_SKY_TOWN_PITRIGHT: lambda state: (self.jump_height_min(state, 4) and self.can_slide(
                state)) or self.double_jump_min(state, 2),
        }

        staircase_location_rules = {
            L_STAIRCASE_5FLOWERS: lambda state: state.has(I_FLOWER, self.player, 5),
            L_STAIRCASE_10FLOWERS: lambda state: state.has(I_FLOWER, self.player, 10),
            L_STAIRCASE_15FLOWERS: lambda state: state.has(I_FLOWER, self.player, 15),
            L_STAIRCASE_20FLOWERS: lambda state: state.has(I_FLOWER, self.player, 20),
        }

        stonecastle_location_rules = {
            L_STONECASTLE_FLOWER: lambda state: self.jump_height_min(state, 5) or (self.jump_height_min(state, 4) and self.double_jump_min(state, 1) and self.can_slide(state)),
            L_STONECASTLE_UPPER: lambda state: (self.jump_height_min(state, 8) or (world.options.hard_logic and self.single_jump_min(state, 3) and self.double_jump_min(state, 2)))
                and self.has_red_energy(state) and self.has_yellow_energy(state),
            L_STONECASTLE_DOOR: lambda state: self.jump_height_min(state, 4),
            L_STONECASTLE_HIDDEN: lambda state: self.jump_height_min(state, 4),
            L_STONECASTLE_BOSS: lambda state: ((self.jump_height_min(state, 4) and self.double_jump_min(state,
                                                                                                        1)) or self.jump_height_min(
                state, 5)) and self.has_red_energy(state),
            L_STONECASTLE_BOSS2: lambda state: (self.jump_height_min(state, 8) or (world.options.hard_logic and self.single_jump_min(state, 3) and self.double_jump_min(state, 2)))
                and self.has_red_energy(state) and self.has_yellow_energy(state) and self.can_slide(state) and self.can_divebomb(state),
            L_STONECASTLE_POSTBOSS: lambda state: ((self.jump_height_min(state, 4) and self.double_jump_min(state,
                                                                                                            1)) or self.jump_height_min(
                state, 5)) and (self.can_divebomb(state) or world.options.closed_end_logic) and self.has_red_energy(state),
            L_STONECASTLE_POSTBOSS2: lambda state: (self.jump_height_min(state, 8) or (world.options.hard_logic and self.single_jump_min(state, 3) and self.double_jump_min(state, 2)))
                and self.has_red_energy(state) and self.has_yellow_energy(state) and self.can_slide(state) and self.can_divebomb(state),
        }

        strangecastle_location_rules = {
            L_STRANGECASTLE_END: lambda state: self.jump_height_min(state, 6) and self.single_jump_min(state, 2) and self.has_fire(state),
            L_STRANGECASTLE_DOOR: lambda state: self.jump_height_min(state, 6) and self.single_jump_min(state, 2) and self.has_fire(state),
        }

        undertomb_location_rules = {
            L_UNDERTOMB_LEFT: lambda state: self.can_divebomb(state),
            L_UNDERTOMB_LEFTDOOR: lambda state: self.can_divebomb(state),
            L_UNDERTOMB_RIGHTDOOR: lambda state: self.can_divebomb(state),
        }

        self.location_rules = {
            **blackcastle_location_rules,
            **blancland_location_rules,
            **bonus_location_rules,
            **bottom_location_rules,
            **cloudrun_location_rules,
            **coldkeep_location_rules,
            **the_curtain_location_rules,
            **dark_grotto_location_rules,
            **deepdive_location_rules,
            **deeptower_location_rules,
            **farfall_location_rules,
            **firecage_location_rules,
            **grotto_location_rules,
            **highlands_location_rules,
            **icecastle_location_rules,
            **library_location_rules,
            **longbeach_location_rules,
            **mountside_location_rules,
            **nightclimb_location_rules,
            **nightwalk_location_rules,
            **rainbowdive_location_rules,
            **skylands_location_rules,
            **skysand_location_rules,
            **sky_town_location_rules,
            **staircase_location_rules,
            **stonecastle_location_rules,
            **strangecastle_location_rules,
            **undertomb_location_rules,
            **arcade_location_rules,

            # Must go at the end for Reasons.
            **final_climb_location_rules,
        }

        self.boss_drop_values = {
            # 10, 25 and 35 are marked as filler and thus not progression items
            "50 Crystals": 50,
            "75 Crystals": 75,
            "110 Crystals": 110,
            "65 Crystals": 65,
            "125 Crystals": 125,
            "180 Crystals": 180,
            "270 Crystals": 270,
            "150 Crystals": 150,
            "200 Crystals": 200,
            "235 Crystals": 235,
            "245 Crystals": 245,
            "400 Crystals": 400,
            "300 Crystals": 300,
            "100 Crystals": 100,
        }

    def total_money(self, state: CollectionState, amount: int) -> int:
        money: int = 0
        for key, value in self.boss_drop_values.items():
            money += state.count(key, self.player) * value
        return money >= amount

    def jump_height(self, state: CollectionState) -> int:
        count: int
        if state.count(I_JUMP_UPGRADE, self.player) == 3 and state.count(I_DOUBLE_JUMP, self.player) == 1:
            count = 6.5
        else:
            count = state.count(I_JUMP_UPGRADE, self.player) + state.count(I_DOUBLE_JUMP, self.player) + 2
        return count
    
    def jump_height_min(self, state: CollectionState, amount: int) -> bool:
        count = self.jump_height(state)
        return count >= amount

    def single_jump_min(self, state: CollectionState, amount: int) -> bool:
        return state.count(I_JUMP_UPGRADE, self.player) >= amount

    def double_jump_height(self, state: CollectionState) -> int:
        return state.count(I_DOUBLE_JUMP, self.player)

    def double_jump_min(self, state: CollectionState, amount: int) -> bool:
        return state.count(I_DOUBLE_JUMP, self.player) >= amount

    def has_red_energy(self, state: CollectionState) -> bool:
        return state.has(I_RED_ENERGY, self.player)

    def has_yellow_energy(self, state: CollectionState) -> bool:
        return state.has(I_YELLOW_ENERGY, self.player)

    def can_duck(self, state: CollectionState) -> bool:
        return state.has(I_DUCKING, self.player)

    def can_stick(self, state: CollectionState) -> bool:
        return state.has(I_STICKING, self.player)
    
    def can_slide(self, state: CollectionState) -> bool:
        return state.has(I_STICKING, self.player, 2)

    def can_divebomb(self, state: CollectionState) -> bool:
        return state.has(I_DIVE_BOMB, self.player)
    
    def has_fire(self, state: CollectionState) -> bool:
        return state.has(I_SHOOT_FIRE, self.player)
    
    def has_range(self, state: CollectionState) -> bool:
        return state.has(I_SHOOT_FIRE, self.player, 2)
    
    def has_ice(self, state: CollectionState) -> bool:
        return state.has(I_SHOOT_ICE, self.player)
    
    def can_shoot(self, state: CollectionState) -> bool:
        return self.has_fire(state) or self.has_ice(state)
    
    def can_light_torches(self, state: CollectionState) -> bool:
        return self.has_fire(state) or self.can_divebomb(state)
    
    def hatched(self, state: CollectionState) -> bool:
        return state.has(I_HATCH, self.player)



    def set_aus_rules(self) -> None:
        multiworld = self.world.multiworld

        for region in multiworld.get_regions(self.player):
            if region.name in self.region_rules:
                for entrance in region.entrances:
                    entrance.access_rule = self.region_rules[region.name]
            for loc in region.locations:
                if loc.name in self.location_rules:
                    loc.access_rule = self.location_rules[loc.name]

        multiworld.completion_condition[self.player] = lambda state: state.has(VICTORY, self.player)

def true(state: CollectionState) -> bool:
    """Hi Messenger!"""
    return True

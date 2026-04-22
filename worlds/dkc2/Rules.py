from typing import TYPE_CHECKING, override

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAll, Rule, True_, False_
from NetUtils import JSONMessagePart

if TYPE_CHECKING:
    from . import DKC2World

from BaseClasses import CollectionState, Location
from .Options import Logic, Goal, FlyingKrockTokens
from .Names import LocationName, ItemName, RegionName, EventName
import dataclasses

GAME_NAME = "Donkey Kong Country 2"

HasDiddy: Rule = Has(ItemName.diddy)
HasDixie: Rule = Has(ItemName.dixie)
HasBothKongs: Rule = HasAll(ItemName.diddy, ItemName.dixie)
CanTeamAttack: Rule = HasBothKongs & Has(ItemName.team_attack)
CanClimb: Rule = Has(ItemName.climb)
CanHover: Rule = HasAll(ItemName.dixie, ItemName.helicopter_spin)
CanCarry: Rule = Has(ItemName.carry)
CanCling: Rule = Has(ItemName.cling)
CanCartwheel: Rule = Has(ItemName.cartwheel)
CanSwim: Rule = Has(ItemName.swim)
HasRambi: Rule = Has(ItemName.rambi)
HasSquawks: Rule = Has(ItemName.squawks)
HasEnguarde: Rule = Has(ItemName.enguarde)
HasSquitter: Rule = Has(ItemName.squitter)
HasRattly: Rule = Has(ItemName.rattly)
HasClapper: Rule = Has(ItemName.clapper)
HasGlimmer: Rule = Has(ItemName.glimmer)
CanRideSkullKart: Rule = Has(ItemName.skull_kart)
CanUseKannons: Rule = Has(ItemName.barrel_kannons)
CanBeInvincible: Rule = Has(ItemName.barrel_exclamation)
CanUseControllableBarrels: Rule = Has(ItemName.barrel_control)
CanUseDiddyBarrels: Rule = HasAll(ItemName.diddy, ItemName.barrel_kong)
CanUseDixieBarrels: Rule = HasAll(ItemName.dixie, ItemName.barrel_kong)
CanUseWarpBarrels: Rule = Has(ItemName.barrel_warp)

CanAccessGalleon: Rule = Has(ItemName.gangplank_galleon)
CanAccessCauldron: Rule = Has(ItemName.crocodile_cauldron)
CanAccessQuay: Rule = Has(ItemName.krem_quay)
CanAccessKremland: Rule = Has(ItemName.krazy_kremland)
CanAccessGulch: Rule = Has(ItemName.gloomy_gulch)
CanAccessKeep: Rule = Has(ItemName.krools_keep)
CanAccessLostWorldCauldron: Rule = Has(ItemName.lost_world_cauldron)
CanAccessLostWorldQuay: Rule = Has(ItemName.lost_world_quay)
CanAccessLostWorldKremland: Rule = Has(ItemName.lost_world_kremland)
CanAccessLostWorldGulch: Rule = Has(ItemName.lost_world_gulch)
CanAccessLostWorldKeep: Rule = Has(ItemName.lost_world_keep)

class DKC2Rules:
    world: "DKC2World"
    connection_rules: dict[str, Rule]
    region_rules: dict[str, Rule]
    location_rules: dict[str, Rule]

    def __init__(self, world: "DKC2World") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            f"{RegionName.crocodile_isle} -> {RegionName.gangplank_galleon}":
                CanAccessGalleon,
            f"{RegionName.crocodile_isle} -> {RegionName.crocodile_cauldron}":
                CanAccessCauldron,
            f"{RegionName.crocodile_isle} -> {RegionName.krem_quay}":
                CanAccessQuay,
            f"{RegionName.crocodile_isle} -> {RegionName.krazy_kremland}":
                CanAccessKremland,
            f"{RegionName.crocodile_isle} -> {RegionName.gloomy_gulch}":
                CanAccessGulch,
            f"{RegionName.crocodile_isle} -> {RegionName.krools_keep}":
                CanAccessKeep,
            f"{RegionName.crocodile_isle} -> {RegionName.the_flying_krock}":
                (OptionFilter(FlyingKrockTokens, 0) & Has(ItemName.the_flying_krock)) | \
                (OptionFilter(FlyingKrockTokens, 0, operator="ne") & Has(ItemName.boss_token, self.world.options.krock_boss_tokens.value)),
            f"{RegionName.crocodile_cauldron} -> {RegionName.lost_world_cauldron}":
                CanAccessLostWorldCauldron,
            f"{RegionName.krem_quay} -> {RegionName.lost_world_quay}":
                CanAccessLostWorldQuay,
            f"{RegionName.krazy_kremland} -> {RegionName.lost_world_kremland}":
                CanAccessLostWorldKremland,
            f"{RegionName.gloomy_gulch} -> {RegionName.lost_world_gulch}":
                CanAccessLostWorldGulch,
            f"{RegionName.krools_keep} -> {RegionName.lost_world_keep}":
                CanAccessLostWorldKeep,
            f"{RegionName.gangplank_galleon} -> {RegionName.krows_nest_map}":
                Has(EventName.galleon_level, self.world.options.required_galleon_levels.value),
            f"{RegionName.crocodile_cauldron} -> {RegionName.kleevers_kiln_map}":
                Has(EventName.cauldron_level, self.world.options.required_cauldron_levels.value),
            f"{RegionName.krem_quay} -> {RegionName.kudgels_kontest_map}":
                Has(EventName.quay_level, self.world.options.required_quay_levels.value),
            f"{RegionName.krazy_kremland} -> {RegionName.king_zing_sting_map}":
                Has(EventName.kremland_level, self.world.options.required_kremland_levels.value),
            f"{RegionName.gloomy_gulch} -> {RegionName.kreepy_krow_map}":
                Has(EventName.gulch_level, self.world.options.required_gulch_levels.value),
            f"{RegionName.krools_keep} -> {RegionName.stronghold_showdown_map}":
                Has(EventName.keep_level, self.world.options.required_keep_levels.value),
            f"{RegionName.the_flying_krock} -> {RegionName.k_rool_duel_map}":
                Has(EventName.krock_level, self.world.options.required_krock_levels.value),
        }

        if world.options.goal != Goal.option_flying_krock:
            self.connection_rules.update(
                {
                    f"{RegionName.lost_world_cauldron} -> {RegionName.krocodile_core_map}":
                        Has(ItemName.lost_world_rock, self.world.options.lost_world_rocks.value),
                    f"{RegionName.lost_world_quay} -> {RegionName.krocodile_core_map}":
                        Has(ItemName.lost_world_rock, self.world.options.lost_world_rocks.value),
                    f"{RegionName.lost_world_kremland} -> {RegionName.krocodile_core_map}":
                        Has(ItemName.lost_world_rock, self.world.options.lost_world_rocks.value),
                    f"{RegionName.lost_world_gulch} -> {RegionName.krocodile_core_map}":
                        Has(ItemName.lost_world_rock, self.world.options.lost_world_rocks.value),
                    f"{RegionName.lost_world_keep} -> {RegionName.krocodile_core_map}":
                        Has(ItemName.lost_world_rock, self.world.options.lost_world_rocks.value),
                }
            )


    def set_dkc2_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            try:
                entrance = multiworld.get_entrance(entrance_name, self.player)
                self.world.set_rule(entrance, rule)
            except KeyError:
                continue

        for loc in multiworld.get_locations(self.player):
            # Skip events so we don't have to type duplicate entries...
            if "(Map Event)" in loc.name:
                continue
            if loc.name in self.location_rules:
                rule = self.location_rules[loc.name]
                self.world.set_rule(self.world.get_location(loc.name), rule)
                # Set event rules at the same time as the real location
                if "- Clear" in loc.name:
                    try:
                        map_event: Location = multiworld.get_location(f"{loc.name} (Map Event)", self.player)
                        self.world.set_rule(map_event, rule)
                    except KeyError:
                        # Filter out missing locations
                        continue

        if self.world.options.goal == Goal.option_flying_krock:
            self.world.set_completion_rule(Has(EventName.k_rool_duel_clear))
        elif self.world.options.goal.value == Goal.option_lost_world:
            self.world.set_completion_rule(Has(EventName.krocodile_core_clear))
        else:
            self.world.set_completion_rule(HasAll(EventName.k_rool_duel_clear, EventName.krocodile_core_clear))


    def set_dkc2_glitched_rules(self, non_glitched_rules: dict[str, Rule]) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            # Skip events so we don't have to type duplicate entries...
            if "(Map Event)" in loc.name:
                continue
            # The second condition looks absolutely hideous, Rule Builder makes it possible LOL
            if loc.name in self.location_rules and not (non_glitched_rules[loc.name] == (self.location_rules[loc.name])):
                glitched_rule = non_glitched_rules[loc.name] | (self.location_rules[loc.name] & Has(ItemName.glitched))
                self.world.set_rule(self.world.get_location(loc.name), glitched_rule)
                # Set event rules at the same time as the real location
                if "- Clear" in loc.name:
                    try:
                        map_event: Location = multiworld.get_location(f"{loc.name} (Map Event)", self.player)
                        self.world.set_rule(map_event, glitched_rule)
                    except KeyError:
                        # Filter out missing locations
                        continue



class DKC2StrictRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                CanCarry | HasRambi,
            LocationName.pirate_panic_banana_coin_1:
                CanTeamAttack,
            LocationName.pirate_panic_banana_bunch_1:
                True_(),
            LocationName.pirate_panic_red_balloon:
                True_(),
            LocationName.pirate_panic_banana_coin_2:
                CanTeamAttack,
            LocationName.pirate_panic_banana_coin_3:
                True_(),
            LocationName.pirate_panic_green_balloon:
                HasRambi,


            LocationName.mainbrace_mayhem_clear:
                CanClimb,
            LocationName.mainbrace_mayhem_kong:
                CanClimb,
            LocationName.mainbrace_mayhem_dk_coin:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_bonus_1:
                CanClimb & (
                    CanHover | CanCartwheel
                ),
            LocationName.mainbrace_mayhem_bonus_2:
                CanClimb & CanCarry,
            LocationName.mainbrace_mayhem_bonus_3:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_bunch_1:
                CanClimb & (
                    CanHover | CanCartwheel
                ),
            LocationName.mainbrace_mayhem_banana_coin_1:
                CanClimb,
            LocationName.mainbrace_mayhem_banana_coin_2:
                CanClimb,
            LocationName.mainbrace_mayhem_green_balloon:
                CanClimb,
            LocationName.mainbrace_mayhem_banana_bunch_2:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_coin_3:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_bunch_3:
                CanClimb & CanTeamAttack,


            LocationName.gangplank_galley_clear:
                CanCling,
            LocationName.gangplank_galley_kong:
                CanCling & CanCarry & CanTeamAttack & 
                    CanUseKannons,
            LocationName.gangplank_galley_dk_coin:
                CanCling & (
                    CanHover | (HasDiddy & CanCartwheel)
                ),
            LocationName.gangplank_galley_bonus_1:
                CanCarry,
            LocationName.gangplank_galley_bonus_2:
                CanCling & CanBeInvincible,
            LocationName.gangplank_galley_banana_bunch_1:
                CanCling & (
                    CanHover | (HasDiddy & CanCartwheel)
                ),
            LocationName.gangplank_galley_banana_bunch_2:
                CanCarry,
            LocationName.gangplank_galley_red_balloon_1:
                CanCarry,
            LocationName.gangplank_galley_banana_bunch_3:
                CanCling & CanTeamAttack & CanUseKannons,
            LocationName.gangplank_galley_banana_coin_1:
                CanCarry,
            LocationName.gangplank_galley_banana_bunch_4:
                CanCling & CanUseKannons & (
                    CanHover | CanCartwheel
                ),
            LocationName.gangplank_galley_banana_coin_2:
                CanCling & CanUseKannons & (
                    CanHover | CanCartwheel
                ),
            LocationName.gangplank_galley_banana_bunch_5:
                CanCling & CanUseKannons & (
                    CanHover | CanCartwheel
                ),
            LocationName.gangplank_galley_banana_bunch_6:
                CanCling & CanCarry,
            LocationName.gangplank_galley_banana_bunch_7:
                CanCling,
            LocationName.gangplank_galley_red_balloon_2:
                 CanCling & CanBeInvincible & CanCarry,


            LocationName.lockjaws_locker_clear:
                CanSwim,
            LocationName.lockjaws_locker_kong:
                CanSwim,
            LocationName.lockjaws_locker_dk_coin:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_bonus_1:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_banana_coin_1:
                True_(),
            LocationName.lockjaws_locker_banana_bunch_1:
                True_(),
            LocationName.lockjaws_locker_banana_coin_2:
                True_(),
            LocationName.lockjaws_locker_banana_bunch_2:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_3:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_4:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_5:
                CanSwim,
            LocationName.lockjaws_locker_banana_bunch_3:
                CanSwim,
            LocationName.lockjaws_locker_red_balloon:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_banana_coin_6:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_banana_coin_7:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_banana_coin_8:
                CanSwim,
            LocationName.lockjaws_locker_banana_bunch_4:
                CanSwim & HasEnguarde,


            LocationName.topsail_trouble_clear:
                CanClimb & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_kong:
                CanClimb & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_dk_coin:
                CanClimb & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_bonus_1:
                HasRattly | (
                    CanTeamAttack & CanCling
                ),
            LocationName.topsail_trouble_bonus_2:
                CanClimb & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_red_balloon_1:
                HasRattly | (CanTeamAttack & CanCling),
            LocationName.topsail_trouble_red_balloon_2:
                CanCarry & (HasRattly | (CanTeamAttack & CanCling)),
            LocationName.topsail_trouble_banana_bunch_1:
                CanClimb & CanCarry & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_banana_bunch_2:
                HasRattly | (CanTeamAttack & CanCling),
            LocationName.topsail_trouble_banana_coin_1:
                HasRattly | (CanTeamAttack & CanCling),
            LocationName.topsail_trouble_banana_coin_2:
                HasRattly,
            LocationName.topsail_trouble_banana_bunch_3:
                CanClimb & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_banana_coin_3:
                CanClimb & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_banana_coin_4:
                CanClimb & CanCarry & (
                    CanTeamAttack | 
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_blue_balloon:
                CanClimb & CanTeamAttack,


            LocationName.krows_nest_clear:
                CanCarry & HasBothKongs,
            LocationName.krow_defeated:
                CanCarry & HasBothKongs,
            LocationName.krows_nest_banana_coin_1:
                CanTeamAttack,
            LocationName.krows_nest_banana_coin_2:
                CanTeamAttack,


            LocationName.hot_head_hop_clear:
                CanUseKannons,
            LocationName.hot_head_hop_kong:
                CanCarry & (
                    CanTeamAttack | 
                    HasSquitter
                ),
            LocationName.hot_head_hop_dk_coin:
                HasSquitter,
            LocationName.hot_head_hop_bonus_1:
                CanCarry,
            LocationName.hot_head_hop_bonus_2:
                HasSquitter,
            LocationName.hot_head_hop_bonus_3:
                HasSquitter & CanUseKannons,
            LocationName.hot_head_hop_green_balloon:
                CanCarry & CanTeamAttack,
            LocationName.hot_head_hop_banana_coin_1:
                CanCarry,
            LocationName.hot_head_hop_banana_bunch_1:
                CanCarry,
            LocationName.hot_head_hop_banana_coin_2:
                HasSquitter | CanTeamAttack,
            LocationName.hot_head_hop_banana_bunch_2:
                HasSquitter,
            LocationName.hot_head_hop_banana_bunch_3:
                HasSquitter,
            LocationName.hot_head_hop_banana_coin_3:
                HasSquitter,
            LocationName.hot_head_hop_banana_coin_4:
                HasSquitter,
            LocationName.hot_head_hop_red_balloon:
                HasSquitter & CanUseKannons,


            LocationName.kannons_klaim_clear:
                CanCarry & CanUseKannons,
            LocationName.kannons_klaim_kong:
                CanCarry & CanUseKannons,
            LocationName.kannons_klaim_dk_coin:
                CanHover,
            LocationName.kannons_klaim_bonus_1:
                CanUseDiddyBarrels & CanUseDixieBarrels & 
                    CanHover,
            LocationName.kannons_klaim_bonus_2:
                CanCarry & CanTeamAttack & CanUseKannons,
            LocationName.kannons_klaim_bonus_3:
                CanCarry & CanUseKannons & CanHover,
            LocationName.kannons_klaim_banana_bunch_1:
                CanUseKannons & CanCling & CanHover,
            LocationName.kannons_klaim_banana_coin_1:
                CanCarry & CanUseKannons,
            LocationName.kannons_klaim_banana_coin_2:
                CanCarry & CanUseKannons & CanHover,
            LocationName.kannons_klaim_banana_coin_3:
                CanCarry & CanUseKannons & CanUseDiddyBarrels,


            LocationName.lava_lagoon_clear:
                CanSwim & HasClapper & CanBeInvincible & 
                    CanUseKannons & HasEnguarde,
            LocationName.lava_lagoon_kong:
                CanSwim & HasClapper & CanBeInvincible & 
                    CanUseKannons & HasEnguarde,
            LocationName.lava_lagoon_dk_coin:
                CanSwim & HasClapper & CanBeInvincible & 
                    CanUseKannons & HasEnguarde,
            LocationName.lava_lagoon_bonus_1:
                CanSwim & HasClapper & CanBeInvincible & 
                    CanUseKannons & HasEnguarde & CanCarry,
            LocationName.lava_lagoon_banana_coin_1:
                CanSwim & HasClapper,
            LocationName.lava_lagoon_banana_coin_2:
                CanSwim & HasClapper,
            LocationName.lava_lagoon_banana_bunch_1:
                CanSwim & HasClapper,
            LocationName.lava_lagoon_banana_coin_3:
                CanSwim & HasClapper,
            LocationName.lava_lagoon_banana_bunch_2:
                CanSwim & HasClapper,
            LocationName.lava_lagoon_banana_coin_4:
                CanSwim & HasClapper & CanUseKannons,
            LocationName.lava_lagoon_banana_coin_5:
                CanSwim & HasClapper & 
                    CanUseKannons & CanBeInvincible,
            LocationName.lava_lagoon_banana_bunch_3:
                CanSwim & HasClapper & 
                    CanUseKannons & CanBeInvincible,
            LocationName.lava_lagoon_banana_coin_6:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde,
            LocationName.lava_lagoon_banana_coin_7:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde,
            LocationName.lava_lagoon_red_balloon_1:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde,
            LocationName.lava_lagoon_banana_bunch_4:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde & CanCarry,
            LocationName.lava_lagoon_banana_bunch_5:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde,
            LocationName.lava_lagoon_banana_coin_8:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde,
            LocationName.lava_lagoon_banana_coin_9:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde,
            LocationName.lava_lagoon_banana_coin_10:
                CanSwim & HasClapper & CanUseKannons & 
                    CanBeInvincible & HasEnguarde & CanTeamAttack,


            LocationName.red_hot_ride_clear:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_kong:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_dk_coin:
                CanCarry & HasRambi & CanTeamAttack,
            LocationName.red_hot_ride_bonus_1:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_bonus_2:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_banana_bunch_1:
                True_(),
            LocationName.red_hot_ride_banana_coin_1:
                CanTeamAttack,
            LocationName.red_hot_ride_banana_coin_2:
                CanTeamAttack,
            LocationName.red_hot_ride_banana_bunch_2:
                CanCarry,
            LocationName.red_hot_ride_banana_coin_3:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_banana_bunch_3:
                (CanCarry | CanTeamAttack) & HasRambi,
            LocationName.red_hot_ride_banana_coin_4:
                (CanCarry | CanTeamAttack) & HasRambi,
            LocationName.red_hot_ride_banana_coin_5:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_banana_coin_6:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_banana_bunch_4:
                CanCarry & HasRambi,


            LocationName.squawks_shaft_clear:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_kong:
                CanUseKannons & CanCarry & HasSquawks,
            LocationName.squawks_shaft_dk_coin:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_bonus_1:
                CanUseKannons & CanCarry & (
                    CanCartwheel | 
                    CanHover
                ),
            LocationName.squawks_shaft_bonus_2:
                CanUseKannons & CanTeamAttack,
            LocationName.squawks_shaft_bonus_3:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_1:
                CanCartwheel,
            LocationName.squawks_shaft_banana_bunch_1:
                CanUseKannons,
            LocationName.squawks_shaft_banana_coin_2:
                CanUseKannons & CanCarry & (
                    CanCartwheel | 
                    CanHover
                ),
            LocationName.squawks_shaft_banana_bunch_2:
                CanUseKannons,
            LocationName.squawks_shaft_red_balloon_1:
                CanUseKannons & CanCarry & CanCartwheel, 
            LocationName.squawks_shaft_banana_coin_3:
                CanUseKannons & CanUseDixieBarrels,
            LocationName.squawks_shaft_banana_coin_4:
                CanUseKannons & CanUseDixieBarrels,
            LocationName.squawks_shaft_banana_coin_5:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_6:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_7:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_bunch_3:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_bunch_4:
                CanUseKannons & HasSquawks,


            LocationName.kleevers_kiln_clear:
                CanCling & CanCarry & HasBothKongs,
            LocationName.kleever_defeated:
                CanCling & CanCarry & HasBothKongs,
            LocationName.kleevers_kiln_banana_coin_1:
                CanCling & CanCarry & HasBothKongs & 
                    CanHover,
            LocationName.kleevers_kiln_banana_coin_2:
                CanCling & CanCarry & HasBothKongs & 
                    CanHover,


            LocationName.barrel_bayou_clear:
                CanUseControllableBarrels & CanUseKannons,
            LocationName.barrel_bayou_kong:
                CanUseControllableBarrels & CanUseKannons & CanCartwheel,
            LocationName.barrel_bayou_dk_coin:
                CanUseControllableBarrels & HasRambi,
            LocationName.barrel_bayou_bonus_1:
                CanUseControllableBarrels & CanCarry,
            LocationName.barrel_bayou_bonus_2:
                CanUseControllableBarrels & CanUseKannons & CanTeamAttack,
            LocationName.barrel_bayou_banana_bunch_1:
                CanTeamAttack,
            LocationName.barrel_bayou_banana_coin_1:
                CanUseControllableBarrels & HasRambi,
            LocationName.barrel_bayou_banana_bunch_2:
                CanUseControllableBarrels,
            LocationName.barrel_bayou_green_balloon:
                CanUseControllableBarrels & CanCarry & CanUseKannons,
            LocationName.barrel_bayou_banana_coin_2:
                CanUseControllableBarrels & CanUseKannons,
            LocationName.barrel_bayou_banana_bunch_3:
                CanUseControllableBarrels & CanUseKannons & CanTeamAttack,


            LocationName.glimmers_galleon_clear:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_kong:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_dk_coin:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_bonus_1:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_bonus_2:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_1:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_2:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_1:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_2:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_3:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_red_balloon:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_4:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_3:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_5:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_4:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_6:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_7:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_5:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_8:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_6:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_9:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_10:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_11:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_12:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_7:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_8:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_13:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_9:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_bunch_14:
                CanSwim & HasGlimmer,
            LocationName.glimmers_galleon_banana_coin_10:
                CanSwim & HasGlimmer,


            LocationName.krockhead_klamber_clear:
                CanClimb & CanUseKannons & CanCarry,
            LocationName.krockhead_klamber_kong:
                CanClimb & CanUseKannons & CanCarry,
            LocationName.krockhead_klamber_dk_coin:
                CanTeamAttack & CanCarry & CanCartwheel,
            LocationName.krockhead_klamber_bonus_1:
                CanClimb & CanTeamAttack & CanUseKannons & 
                    HasSquitter,
            LocationName.krockhead_klamber_red_balloon_1:
                CanTeamAttack & CanCarry,
            LocationName.krockhead_klamber_banana_coin_1:
                CanTeamAttack & CanCartwheel,
            LocationName.krockhead_klamber_banana_coin_2:
                CanClimb,
            LocationName.krockhead_klamber_red_balloon_2:
                CanClimb & CanTeamAttack & CanUseKannons & 
                    HasSquitter,
            LocationName.krockhead_klamber_banana_coin_3:
                CanClimb & CanUseKannons,


            LocationName.rattle_battle_clear:
                HasRattly,
            LocationName.rattle_battle_kong:
                HasRattly,
            LocationName.rattle_battle_dk_coin:
                HasRattly & CanUseKannons,
            LocationName.rattle_battle_bonus_1:
                CanTeamAttack & CanHover,
            LocationName.rattle_battle_bonus_2:
                HasRattly,
            LocationName.rattle_battle_bonus_3:
                HasRattly,
            LocationName.rattle_battle_banana_coin_1:
                True_(),
            LocationName.rattle_battle_banana_bunch_1:
                True_(),
            LocationName.rattle_battle_banana_bunch_2:
                HasRattly,
            LocationName.rattle_battle_banana_coin_2:
                HasRattly,
            LocationName.rattle_battle_banana_coin_3:
                HasRattly,
            LocationName.rattle_battle_banana_bunch_3:
                HasRattly,
            LocationName.rattle_battle_banana_bunch_4:
                HasRattly,


            LocationName.slime_climb_clear:
                CanClimb & CanSwim & CanCarry & 
                    CanUseKannons & CanHover,
            LocationName.slime_climb_kong:
                CanClimb & CanSwim & CanCarry & 
                    CanCartwheel & CanHover,
            LocationName.slime_climb_dk_coin:
                CanClimb & CanSwim & CanCarry & 
                    CanTeamAttack & CanBeInvincible & CanHover,
            LocationName.slime_climb_bonus_1:
                CanClimb & CanSwim & CanCarry & 
                    CanBeInvincible & CanCling & CanCartwheel & CanHover,
            LocationName.slime_climb_bonus_2:
                CanClimb & CanSwim & CanCarry & CanHover,
            LocationName.slime_climb_banana_coin_1:
                CanCartwheel,
            LocationName.slime_climb_banana_coin_2:
                CanClimb & CanCarry & CanSwim & 
                    CanCartwheel,
            LocationName.slime_climb_banana_bunch_1:
                CanClimb & CanCarry & CanSwim & 
                    CanCartwheel,
            LocationName.slime_climb_banana_bunch_2:
                CanClimb & CanCarry & CanSwim,
            LocationName.slime_climb_banana_coin_3:
                CanClimb & CanCarry & CanSwim & 
                    CanCartwheel,
            LocationName.slime_climb_banana_bunch_3:
                CanClimb & CanCarry & CanSwim & 
                    CanCartwheel & CanHover,
            LocationName.slime_climb_banana_bunch_4:
                CanClimb & CanCarry & CanSwim & 
                    CanCartwheel & CanHover,


            LocationName.bramble_blast_clear:
                CanUseKannons,
            LocationName.bramble_blast_kong:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_dk_coin:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_bonus_1:
                CanUseKannons,
            LocationName.bramble_blast_bonus_2:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_1:
                CanTeamAttack,
            LocationName.bramble_blast_banana_bunch_2:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_3:
                CanUseKannons,
            LocationName.bramble_blast_banana_coin_1:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_4:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_5:
                CanUseKannons,
            LocationName.bramble_blast_banana_coin_2:
                CanUseKannons,
            LocationName.bramble_blast_red_balloon:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_6:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_7:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_8:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_9:
                CanUseKannons & HasSquawks,


            LocationName.kudgels_kontest_clear:
                CanCarry & CanCartwheel & CanHover & HasDiddy,
            LocationName.kudgel_defeated:
                CanCarry & CanCartwheel & CanHover & HasDiddy,


            LocationName.hornet_hole_clear:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_kong:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_dk_coin:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_bonus_1:
                CanTeamAttack & CanCling & CanCarry,
            LocationName.hornet_hole_bonus_2:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_bonus_3:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_banana_bunch_1:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_banana_coin_1:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_banana_bunch_2:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_banana_coin_2:
                True_(),
            LocationName.hornet_hole_green_balloon_1:
                CanCarry,
            LocationName.hornet_hole_banana_coin_3:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_banana_bunch_3:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_banana_coin_4:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_banana_bunch_4:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_banana_bunch_5:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,
            LocationName.hornet_hole_red_balloon_1:
                CanHover & CanTeamAttack & HasSquitter & 
                    CanUseKannons & CanCling,


            LocationName.target_terror_clear:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_kong:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_dk_coin:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_bonus_1:
                CanUseKannons & CanRideSkullKart & HasSquawks,
            LocationName.target_terror_bonus_2:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_banana_bunch_1:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_banana_bunch_2:
                CanUseKannons & CanRideSkullKart & HasSquawks,
            LocationName.target_terror_red_balloon:
                CanUseKannons & CanRideSkullKart,


            LocationName.bramble_scramble_clear:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_kong:
                CanHover & CanClimb & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_dk_coin:
                CanHover & CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_bonus_1:
                CanHover & CanClimb & CanTeamAttack & 
                    CanBeInvincible & CanUseKannons & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_1:
                CanUseKannons,
            LocationName.bramble_scramble_banana_bunch_2:
                 CanCarry & HasBothKongs & CanClimb,
            LocationName.bramble_scramble_banana_coin_1:
                CanHover & CanClimb & CanTeamAttack & 
                    CanBeInvincible & CanUseKannons,
            LocationName.bramble_scramble_banana_coin_2:
                CanHover & CanClimb & CanTeamAttack & 
                    CanBeInvincible & CanUseKannons & HasSquawks,
            LocationName.bramble_scramble_banana_coin_3:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_3:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_4:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_4:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_5:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_5:
                CanHover & CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_6:
                CanHover & CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_banana_coin_7:
                CanHover & CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_banana_coin_8:
                CanHover & CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_blue_balloon:
                CanHover & CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_red_balloon:
                CanHover & CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,


            LocationName.rickety_race_clear:
                CanRideSkullKart,
            LocationName.rickety_race_kong:
                CanRideSkullKart,
            LocationName.rickety_race_dk_coin:
                CanRideSkullKart,
            LocationName.rickety_race_bonus_1:
                CanRideSkullKart & CanTeamAttack & CanHover,
            LocationName.rickety_race_banana_coin:
                CanRideSkullKart,


            LocationName.mudhole_marsh_clear:
                CanClimb & CanCling & CanBeInvincible,
            LocationName.mudhole_marsh_kong:
                CanClimb & CanCling & CanBeInvincible & 
                    CanCarry & CanTeamAttack,
            LocationName.mudhole_marsh_dk_coin:
                CanClimb & CanCling & CanBeInvincible & 
                    CanHover,
            LocationName.mudhole_marsh_bonus_1:
                CanCling & CanBeInvincible & 
                    CanCarry & CanTeamAttack,
            LocationName.mudhole_marsh_bonus_2:
                CanClimb & CanCling & CanBeInvincible & 
                    CanCarry,
            LocationName.mudhole_marsh_banana_coin_1:
                True_(),
            LocationName.mudhole_marsh_banana_bunch_1:
                CanCling & CanCarry,
            LocationName.mudhole_marsh_banana_coin_2:
                CanCling & CanCarry & CanTeamAttack & 
                    CanBeInvincible,
            LocationName.mudhole_marsh_banana_coin_3:
                CanCling & CanCarry & CanTeamAttack & 
                    CanBeInvincible & CanClimb,
            LocationName.mudhole_marsh_banana_coin_4:
                CanCling & CanCarry & CanTeamAttack & 
                    CanBeInvincible & CanClimb & CanCartwheel,
            LocationName.mudhole_marsh_banana_coin_5:
                CanCling & CanCarry & CanTeamAttack & 
                    CanBeInvincible & CanClimb,


            LocationName.rambi_rumble_clear:
                CanCling & CanUseKannons & HasRambi & CanHover,
            LocationName.rambi_rumble_kong:
                CanCling & CanUseKannons & HasRambi & 
                    CanCartwheel & CanHover,
            LocationName.rambi_rumble_dk_coin:
                CanCling & CanUseKannons & CanHover,
            LocationName.rambi_rumble_bonus_1:
                CanCling & CanUseKannons & CanTeamAttack & CanHover,
            LocationName.rambi_rumble_bonus_2:
                CanCling & CanUseKannons & HasRambi & CanHover,
            LocationName.rambi_rumble_banana_coin_1:
                CanHover,
            LocationName.rambi_rumble_banana_bunch_1:
                CanHover,
            LocationName.rambi_rumble_banana_bunch_2:
                CanCling & CanUseKannons & 
                    CanHover,
            LocationName.rambi_rumble_banana_coin_2:
                CanCling & CanUseKannons & 
                    CanHover & CanTeamAttack,
            LocationName.rambi_rumble_banana_bunch_3:
                CanCling & CanUseKannons & 
                    CanHover & HasRambi,


            LocationName.king_zing_sting_clear:
                HasSquawks & HasBothKongs,
            LocationName.king_zing_defeated:
                HasSquawks & HasBothKongs,
            LocationName.king_zing_sting_banana_coin_1:
                True_(),
            LocationName.king_zing_sting_banana_coin_2:
                True_(),


            LocationName.ghostly_grove_clear:
                CanClimb,
            LocationName.ghostly_grove_kong:
                CanClimb & CanCarry,
            LocationName.ghostly_grove_dk_coin:
                CanClimb & CanUseKannons & (
                    CanCartwheel | CanHover
                ),
            LocationName.ghostly_grove_bonus_1:
                CanClimb & CanCarry,
            LocationName.ghostly_grove_bonus_2:
                CanClimb,
            LocationName.ghostly_grove_banana_bunch_1:
                True_(),
            LocationName.ghostly_grove_red_balloon:
                CanCarry,
            LocationName.ghostly_grove_banana_bunch_2:
                True_(),
            LocationName.ghostly_grove_banana_coin_1:
                CanClimb & CanCartwheel,
            LocationName.ghostly_grove_banana_bunch_3:
                CanClimb,
            LocationName.ghostly_grove_banana_bunch_4:
                CanClimb,
            LocationName.ghostly_grove_banana_coin_2:
                CanClimb,


            LocationName.haunted_hall_clear:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_kong:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_dk_coin:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_bonus_1:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_bonus_2:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_bonus_3:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_banana_bunch_1:
                True_(),
            LocationName.haunted_hall_banana_bunch_2:
                True_(),
            LocationName.haunted_hall_banana_coin_1:
                CanCartwheel,
            LocationName.haunted_hall_banana_coin_2:
                CanCling & CanRideSkullKart,
            LocationName.haunted_hall_banana_coin_3:
                CanCling & CanRideSkullKart,


            LocationName.gusty_glade_clear:
                CanCling & CanUseKannons & CanCartwheel,
            LocationName.gusty_glade_kong:
                CanCling & CanUseKannons & CanCarry & 
                    CanCartwheel,
            LocationName.gusty_glade_dk_coin:
                CanCling & CanUseKannons & CanHover,
            LocationName.gusty_glade_bonus_1:
                CanTeamAttack & (CanCling | HasRattly),
            LocationName.gusty_glade_bonus_2:
                CanCling & CanCarry & CanUseKannons,
            LocationName.gusty_glade_banana_coin_1:
                CanTeamAttack,
            LocationName.gusty_glade_banana_coin_2:
                CanCartwheel,
            LocationName.gusty_glade_blue_balloon:
                CanTeamAttack & HasRattly,
            LocationName.gusty_glade_banana_coin_3:
                CanCling & CanUseKannons & CanCartwheel,


            LocationName.parrot_chute_panic_clear:
                HasSquawks,
            LocationName.parrot_chute_panic_kong:
                HasSquawks,
            LocationName.parrot_chute_panic_dk_coin:
                CanHover,
            LocationName.parrot_chute_panic_bonus_1:
                HasSquawks,
            LocationName.parrot_chute_panic_bonus_2:
                HasSquawks & CanHover & CanCarry,
            LocationName.parrot_chute_panic_banana_coin_1:
                HasSquawks & CanCarry,
            LocationName.parrot_chute_panic_banana_coin_2:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_bunch_1:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_3:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_bunch_2:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_4:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_5:
                HasSquawks & CanUseControllableBarrels & CanTeamAttack,


            LocationName.web_woods_clear:
                HasSquitter,
            LocationName.web_woods_kong:
                HasSquitter & CanTeamAttack,
            LocationName.web_woods_dk_coin:
                HasSquitter & CanUseKannons,
            LocationName.web_woods_bonus_1:
                HasSquitter,
            LocationName.web_woods_bonus_2:
                HasSquitter,
            LocationName.web_woods_banana_coin_1:
                CanTeamAttack,
            LocationName.web_woods_banana_coin_2:
                CanTeamAttack & CanCarry,
            LocationName.web_woods_green_balloon_1:
                CanTeamAttack & CanCarry & CanUseKannons,
            LocationName.web_woods_banana_bunch_1:
                CanCartwheel,
            LocationName.web_woods_banana_bunch_2:
                CanCarry,
            LocationName.web_woods_banana_bunch_3:
                HasSquitter,
            LocationName.web_woods_banana_coin_3:
                HasSquitter,
            LocationName.web_woods_banana_coin_4:
                HasSquitter,
            LocationName.web_woods_banana_coin_5:
                HasSquitter,
            LocationName.web_woods_green_balloon_2:
                HasSquitter & CanTeamAttack,


            LocationName.kreepy_krow_clear:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry & HasBothKongs,
            LocationName.kreepy_krow_defeated:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry & HasBothKongs,
            LocationName.kreepy_krow_banana_coin_1:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry & HasBothKongs,
            LocationName.kreepy_krow_banana_coin_2:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry & HasBothKongs,


            LocationName.arctic_abyss_clear:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_kong:
                CanSwim & HasEnguarde & (
                    (HasDiddy & CanCartwheel) | CanHover
                ),
            LocationName.arctic_abyss_dk_coin:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_bonus_1:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_bonus_2:
                CanSwim & HasEnguarde & CanCarry,
            LocationName.arctic_abyss_banana_coin_1:
                CanTeamAttack & (CanCartwheel | CanHover),
            LocationName.arctic_abyss_banana_bunch_1:
                CanTeamAttack & (CanCartwheel | CanHover),
            LocationName.arctic_abyss_banana_bunch_2:
                CanTeamAttack & (CanCartwheel | CanHover),
            LocationName.arctic_abyss_banana_bunch_3:
                CanTeamAttack & (CanCartwheel | CanHover),
            LocationName.arctic_abyss_banana_bunch_4:
                CanSwim,
            LocationName.arctic_abyss_banana_coin_2:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_coin_3:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_coin_4:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_bunch_5:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_coin_5:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_bunch_6:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_bunch_7:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_red_balloon_1:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_red_balloon_2:
                CanSwim & HasEnguarde,


            LocationName.windy_well_clear:
                CanUseKannons & CanCling & HasBothKongs & CanCarry,
            LocationName.windy_well_kong:
                CanUseKannons & CanCling & HasBothKongs & CanCarry,
            LocationName.windy_well_dk_coin:
                CanUseKannons & CanCling & HasBothKongs & CanCarry,
            LocationName.windy_well_bonus_1:
                CanCling & CanCarry,
            LocationName.windy_well_bonus_2:
                CanUseKannons & CanCling & CanCarry & 
                    HasSquawks & HasBothKongs,
            LocationName.windy_well_banana_coin_1:
                CanCarry,
            LocationName.windy_well_banana_coin_2:
                CanCling & CanCarry,
            LocationName.windy_well_banana_coin_3:
                CanCling & CanCarry,
            LocationName.windy_well_banana_bunch_1:
                CanUseKannons & CanCling & CanCarry & 
                    CanCartwheel,
            LocationName.windy_well_banana_bunch_2:
                CanUseKannons & CanCling & CanCarry & 
                    CanCartwheel,
            LocationName.windy_well_banana_coin_4:
                CanUseKannons & CanCling & CanCarry,
            LocationName.windy_well_banana_bunch_3:
                CanUseKannons & CanCling & CanCarry,
            LocationName.windy_well_red_balloon:
                CanUseKannons & CanCling & CanCarry & 
                    HasBothKongs,
            LocationName.windy_well_banana_bunch_4:
                CanUseKannons & CanCling & CanCarry & 
                    HasBothKongs & HasSquawks,


            LocationName.castle_crush_clear:
                HasRambi & CanCartwheel & CanCarry & HasBothKongs,
            LocationName.castle_crush_kong:
                HasRambi & CanCartwheel & CanCarry & HasBothKongs,
            LocationName.castle_crush_dk_coin:
                HasRambi & CanCartwheel & CanCarry & 
                    HasSquawks & HasBothKongs,
            LocationName.castle_crush_bonus_1:
                HasRambi & CanCarry & HasBothKongs,
            LocationName.castle_crush_bonus_2:
                HasRambi & CanCartwheel & CanCarry & 
                    HasSquawks & HasBothKongs,
            LocationName.castle_crush_banana_coin_1:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_bunch_1:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_bunch_2:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_coin_2:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_bunch_3:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_bunch_4:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_bunch_5:
                HasRambi & CanCarry & 
                    HasBothKongs & CanCartwheel & HasSquawks,
            LocationName.castle_crush_banana_coin_3:
                HasRambi & CanCarry & 
                    HasBothKongs & CanCartwheel,
            LocationName.castle_crush_banana_bunch_6:
                HasRambi & CanCarry & 
                    HasBothKongs & CanCartwheel,


            LocationName.clappers_cavern_clear:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde & CanCling & CanCarry,
            LocationName.clappers_cavern_kong:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde & CanCling & CanCarry & 
                    CanTeamAttack & CanHover,
            LocationName.clappers_cavern_dk_coin:
                CanTeamAttack & CanCling & CanCartwheel,
            LocationName.clappers_cavern_bonus_1:
                CanTeamAttack & CanCling & CanCartwheel,
            LocationName.clappers_cavern_bonus_2:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_coin_1:
                HasClapper,
            LocationName.clappers_cavern_banana_bunch_1:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_bunch_2:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_bunch_3:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_coin_2:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_bunch_4:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_coin_3:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde & CanTeamAttack & CanBeInvincible,
            LocationName.clappers_cavern_banana_coin_4:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde & CanTeamAttack & CanBeInvincible,
            LocationName.clappers_cavern_banana_coin_5:
                HasClapper & CanSwim & CanUseKannons & 
                    HasEnguarde & CanTeamAttack & CanBeInvincible,


            LocationName.chain_link_chamber_clear:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,
            LocationName.chain_link_chamber_kong:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,
            LocationName.chain_link_chamber_dk_coin:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,
            LocationName.chain_link_chamber_bonus_1:
                CanClimb & CanCling & CanCarry,
            LocationName.chain_link_chamber_bonus_2:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels & CanCartwheel,
            LocationName.chain_link_chamber_banana_coin_1:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_1:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_2:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_3:
                CanClimb & CanCarry,
            LocationName.chain_link_chamber_banana_coin_2:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,
            LocationName.chain_link_chamber_banana_bunch_4:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,
            LocationName.chain_link_chamber_banana_coin_3:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,
            LocationName.chain_link_chamber_banana_coin_4:
                CanClimb & CanCling & CanUseKannons & 
                    CanUseControllableBarrels,


            LocationName.toxic_tower_clear:
                HasRattly & HasSquawks & HasSquitter & 
                    CanUseKannons,
            LocationName.toxic_tower_kong:
                HasRattly & HasSquawks & HasSquitter & 
                    CanUseKannons,
            LocationName.toxic_tower_dk_coin:
                HasRattly & CanUseKannons,
            LocationName.toxic_tower_bonus_1:
                HasRattly & HasSquawks & HasSquitter & 
                    CanUseKannons,
            LocationName.toxic_tower_banana_bunch_1:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_2:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_3:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_4:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_5:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_6:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_7:
                HasRattly,
            LocationName.toxic_tower_banana_coin_1:
                HasRattly,
            LocationName.toxic_tower_banana_coin_2:
                HasRattly,
            LocationName.toxic_tower_banana_coin_3:
                HasRattly,
            LocationName.toxic_tower_banana_coin_4:
                HasRattly & HasSquawks & CanUseKannons,
            LocationName.toxic_tower_banana_coin_5:
                HasRattly & HasSquawks & CanUseKannons,
            LocationName.toxic_tower_banana_bunch_8:
                HasRattly & HasSquawks & CanUseKannons,
            LocationName.toxic_tower_banana_bunch_9:
                HasRattly & HasSquawks & CanUseKannons,
            LocationName.toxic_tower_green_balloon:
                HasRattly & HasSquawks & CanUseKannons & HasSquitter,


            LocationName.stronghold_showdown_clear:
                True_(),
            LocationName.stronghold_showdown_banana_coin_1:
                CanTeamAttack,
            LocationName.stronghold_showdown_red_balloon:
                CanTeamAttack,
            LocationName.stronghold_showdown_banana_coin_2:
                CanTeamAttack,


            LocationName.screechs_sprint_clear:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_kong:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_dk_coin:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_bonus_1:
                CanClimb & CanTeamAttack & CanCarry & 
                    CanCartwheel & CanHover,
            LocationName.screechs_sprint_banana_coin_1:
                CanCartwheel,
            LocationName.screechs_sprint_banana_bunch_1:
                CanClimb & CanCarry & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_2:
                CanClimb & CanCarry & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_3:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_red_balloon:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_bunch_2:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_bunch_3:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_4:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_5:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_6:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_7:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_coin_8:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_bunch_4:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_bunch_5:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),
            LocationName.screechs_sprint_banana_bunch_6:
                CanClimb & CanCarry & HasSquawks & (HasDiddy & CanCartwheel),


            LocationName.k_rool_duel_clear:
                CanCarry & CanHover & HasDiddy,


            LocationName.jungle_jinx_clear:
                CanCartwheel & CanUseKannons,
            LocationName.jungle_jinx_kong:
                CanCartwheel & CanUseKannons & CanCarry,
            LocationName.jungle_jinx_dk_coin:
                CanCartwheel & CanTeamAttack,
            LocationName.jungle_jinx_banana_bunch_1:
                True_(),
            LocationName.jungle_jinx_banana_bunch_2:
                True_(),
            LocationName.jungle_jinx_banana_coin_1:
                CanHover,
            LocationName.jungle_jinx_banana_coin_2:
                CanCartwheel,
            LocationName.jungle_jinx_banana_coin_3:
                CanCartwheel & CanUseKannons,
            LocationName.jungle_jinx_banana_coin_4:
                CanCartwheel & CanUseKannons & CanTeamAttack,
            LocationName.jungle_jinx_banana_coin_5:
                CanCartwheel & CanUseKannons,


            LocationName.black_ice_battle_clear:
                True_(),
            LocationName.black_ice_battle_kong:
                CanCarry,
            LocationName.black_ice_battle_dk_coin:
                CanCarry,
            LocationName.black_ice_battle_banana_bunch_1:
                CanHover & CanCartwheel,
            LocationName.black_ice_battle_red_balloon_1:
                True_(),
            LocationName.black_ice_battle_red_balloon_2:
                True_(),
            LocationName.black_ice_battle_red_balloon_3:
                CanCarry,
            LocationName.black_ice_battle_banana_bunch_2:
                True_(),
            LocationName.black_ice_battle_banana_coin_1:
                True_(),
            LocationName.black_ice_battle_banana_bunch_3:
                CanCarry,


            LocationName.klobber_karnage_clear:
                CanCarry & CanUseControllableBarrels & 
                    CanUseKannons & CanUseDiddyBarrels & 
                    CanUseDixieBarrels,
            LocationName.klobber_karnage_kong:
                CanCarry & CanUseControllableBarrels & 
                    CanUseKannons & CanUseDiddyBarrels & 
                    CanUseDixieBarrels,
            LocationName.klobber_karnage_dk_coin:
                CanCarry & CanUseKannons & CanBeInvincible & 
                    CanUseDiddyBarrels & CanUseDixieBarrels & 
                    CanUseControllableBarrels,
            LocationName.klobber_karnage_banana_coin_1:
                True_(),
            LocationName.klobber_karnage_banana_bunch_1:
                CanCartwheel,
            LocationName.klobber_karnage_banana_bunch_2:
                CanCartwheel,
            LocationName.klobber_karnage_banana_coin_2:
                CanCartwheel,
            LocationName.klobber_karnage_banana_bunch_3:
                CanCartwheel,
            LocationName.klobber_karnage_banana_coin_3:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseControllableBarrels,
            LocationName.klobber_karnage_banana_bunch_4:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels,
            LocationName.klobber_karnage_banana_bunch_5:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_banana_bunch_6:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_banana_bunch_7:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_banana_coin_4:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_red_balloon:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,


            LocationName.fiery_furnace_clear:
                CanUseControllableBarrels & CanCartwheel
                    & CanTeamAttack,
            LocationName.fiery_furnace_kong:
                CanUseControllableBarrels & CanCartwheel
                    & CanTeamAttack,
            LocationName.fiery_furnace_dk_coin:
                CanUseControllableBarrels & CanCartwheel
                    & CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_1:
                CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_2:
                CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_3:
                CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_4:
                CanUseControllableBarrels & CanTeamAttack,
            LocationName.fiery_furnace_banana_coin_1:
                CanUseControllableBarrels & CanTeamAttack & 
                    CanCartwheel,
            LocationName.fiery_furnace_banana_coin_2:
                CanUseControllableBarrels & CanTeamAttack & 
                    CanCartwheel,
            LocationName.fiery_furnace_banana_bunch_5:
                CanUseControllableBarrels & CanTeamAttack & 
                    CanCartwheel,


            LocationName.animal_antics_clear:
                HasBothKongs & HasRambi & HasEnguarde & HasSquitter & 
                    HasSquawks & HasRattly & CanSwim & 
                    CanUseKannons,
            LocationName.animal_antics_kong:
                HasBothKongs & HasRambi & HasEnguarde & HasSquitter & 
                    HasSquawks & HasRattly & CanSwim & 
                    CanUseKannons,
            LocationName.animal_antics_dk_coin:
                HasBothKongs & HasRambi & HasEnguarde & HasSquitter & 
                    HasSquawks & CanSwim,
            LocationName.animal_antics_banana_bunch_1:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim,
            LocationName.animal_antics_banana_bunch_2:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter,
            LocationName.animal_antics_banana_coin_1:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter,
            LocationName.animal_antics_banana_coin_2:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_bunch_3:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_bunch_4:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_coin_3:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_coin_4:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_red_balloon:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_coin_5:
                HasBothKongs & HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks  & CanUseKannons & HasRattly,
    

            LocationName.krocodile_core_clear:
                CanCarry & CanHover & HasDiddy,
        }


class DKC2LooseRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                CanCarry | HasRambi,
            LocationName.pirate_panic_banana_coin_1:
                CanTeamAttack,
            LocationName.pirate_panic_banana_bunch_1:
                True_(),
            LocationName.pirate_panic_red_balloon:
                True_(),
            LocationName.pirate_panic_banana_coin_2:
                CanTeamAttack,
            LocationName.pirate_panic_banana_coin_3:
                True_(),
            LocationName.pirate_panic_green_balloon:
                HasRambi,


            LocationName.mainbrace_mayhem_clear:
                CanClimb,
            LocationName.mainbrace_mayhem_kong:
                CanClimb,
            LocationName.mainbrace_mayhem_dk_coin:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_bonus_1:
                CanClimb & (
                    CanHover | CanCartwheel
                ),
            LocationName.mainbrace_mayhem_bonus_2:
                CanClimb & CanCarry,
            LocationName.mainbrace_mayhem_bonus_3:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_bunch_1:
                CanClimb & (
                    CanHover | CanCartwheel
                ),
            LocationName.mainbrace_mayhem_banana_coin_1:
                CanClimb,
            LocationName.mainbrace_mayhem_banana_coin_2:
                CanClimb,
            LocationName.mainbrace_mayhem_green_balloon: 
                CanClimb,
            LocationName.mainbrace_mayhem_banana_bunch_2:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_coin_3:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_bunch_3:
                CanClimb & CanTeamAttack,


            LocationName.gangplank_galley_clear:
                CanCling,
            LocationName.gangplank_galley_kong:
                CanCling & CanCarry & CanTeamAttack,
            LocationName.gangplank_galley_dk_coin:
                CanCling & (
                    CanHover | (CanCartwheel & CanCartwheel)
                ),
            LocationName.gangplank_galley_bonus_1:
                CanCarry,
            LocationName.gangplank_galley_bonus_2:
                CanCling & CanBeInvincible,
            LocationName.gangplank_galley_banana_bunch_1:
                CanCling & (
                    CanHover | (CanCartwheel & CanCartwheel)
                ),
            LocationName.gangplank_galley_banana_bunch_2:
                CanCarry,
            LocationName.gangplank_galley_red_balloon_1:
                CanCarry,
            LocationName.gangplank_galley_banana_bunch_3:
                CanTeamAttack & CanUseKannons,
            LocationName.gangplank_galley_banana_coin_1:
                CanCarry,
            LocationName.gangplank_galley_banana_bunch_4:
                CanCling & CanUseKannons,
            LocationName.gangplank_galley_banana_coin_2:
                CanCling & CanUseKannons,
            LocationName.gangplank_galley_banana_bunch_5:
                CanCling & CanUseKannons,
            LocationName.gangplank_galley_banana_bunch_6:
                CanCarry & (CanCling | CanHover | CanCartwheel) ,
            LocationName.gangplank_galley_banana_bunch_7:
                CanHover | CanCling,
            LocationName.gangplank_galley_red_balloon_2:
                 CanCling & CanCarry & (CanTeamAttack | CanBeInvincible) ,


            LocationName.lockjaws_locker_clear:
                CanSwim,
            LocationName.lockjaws_locker_kong:
                CanSwim,
            LocationName.lockjaws_locker_dk_coin:
                CanSwim,
            LocationName.lockjaws_locker_bonus_1:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_banana_coin_1:
                True_(),
            LocationName.lockjaws_locker_banana_bunch_1:
                True_(),
            LocationName.lockjaws_locker_banana_coin_2:
                True_(),
            LocationName.lockjaws_locker_banana_bunch_2:
                CanSwim | CanHover | CanCartwheel,
            LocationName.lockjaws_locker_banana_coin_3:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_4:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_5:
                CanSwim,
            LocationName.lockjaws_locker_banana_bunch_3:
                CanSwim,
            LocationName.lockjaws_locker_red_balloon:
                CanSwim & HasEnguarde,
            LocationName.lockjaws_locker_banana_coin_6:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_7:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_8:
                CanSwim,
            LocationName.lockjaws_locker_banana_bunch_4:
                CanSwim & HasEnguarde,


            LocationName.topsail_trouble_clear:
                CanClimb & (
                    (CanTeamAttack | HasRattly)
                ),
            LocationName.topsail_trouble_kong:
                CanClimb & (
                    (CanTeamAttack | HasRattly)
                ),
            LocationName.topsail_trouble_dk_coin:
                CanClimb & (
                    (CanTeamAttack | HasRattly)
                ),
            LocationName.topsail_trouble_bonus_1:
                CanTeamAttack | HasRattly,
            LocationName.topsail_trouble_bonus_2:
                CanClimb & (
                    (CanTeamAttack | HasRattly)
                ),
            LocationName.topsail_trouble_red_balloon_1:
                HasRattly | CanTeamAttack | CanCling,
            LocationName.topsail_trouble_red_balloon_2:
                CanCarry & (
                    HasRattly | CanTeamAttack | CanCling
                ),
            LocationName.topsail_trouble_banana_bunch_1:
                CanTeamAttack |
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ,
            LocationName.topsail_trouble_banana_bunch_2:
                HasRattly | CanTeamAttack,
            LocationName.topsail_trouble_banana_coin_1:
                HasRattly | CanTeamAttack,
            LocationName.topsail_trouble_banana_coin_2:
                HasRattly,
            LocationName.topsail_trouble_banana_bunch_3:
                CanClimb & (
                    CanTeamAttack |
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_banana_coin_3:
                CanClimb & (
                    CanTeamAttack |
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_banana_coin_4:
                CanClimb & CanCarry & (
                    CanTeamAttack |
                    HasRattly | 
                    (CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_blue_balloon:
                CanClimb & CanTeamAttack ,


            LocationName.krows_nest_clear:
                CanCarry,
            LocationName.krow_defeated:
                CanCarry,
            LocationName.krows_nest_banana_coin_1:
                CanTeamAttack,
            LocationName.krows_nest_banana_coin_2:
                CanTeamAttack,


            LocationName.hot_head_hop_clear:
                CanUseKannons | HasSquitter,
            LocationName.hot_head_hop_kong:
                CanCarry & (
                    CanTeamAttack |
                    HasSquitter
                ),
            LocationName.hot_head_hop_dk_coin:
                HasSquitter,
            LocationName.hot_head_hop_bonus_1:
                CanCarry,
            LocationName.hot_head_hop_bonus_2:
                HasSquitter,
            LocationName.hot_head_hop_bonus_3:
                HasSquitter,
            LocationName.hot_head_hop_green_balloon:
                CanCarry & CanTeamAttack,
            LocationName.hot_head_hop_banana_coin_1:
                CanCarry,
            LocationName.hot_head_hop_banana_bunch_1:
                CanCarry,
            LocationName.hot_head_hop_banana_coin_2:
                HasSquitter | CanTeamAttack,
            LocationName.hot_head_hop_banana_bunch_2:
                HasSquitter,
            LocationName.hot_head_hop_banana_bunch_3:
                HasSquitter,
            LocationName.hot_head_hop_banana_coin_3:
                HasSquitter,
            LocationName.hot_head_hop_banana_coin_4:
                HasSquitter,
            LocationName.hot_head_hop_red_balloon:
                HasSquitter,


            LocationName.kannons_klaim_clear:
                CanUseKannons,
            LocationName.kannons_klaim_kong:
                CanUseKannons & CanCarry,
            LocationName.kannons_klaim_dk_coin:
                CanHover | CanCartwheel,
            LocationName.kannons_klaim_bonus_1:
                CanUseDiddyBarrels & CanUseDixieBarrels & (
                    CanHover | CanCartwheel
                ),
            LocationName.kannons_klaim_bonus_2:
                CanUseKannons,
            LocationName.kannons_klaim_bonus_3:
                CanUseKannons,
            LocationName.kannons_klaim_banana_bunch_1:
                CanUseKannons | CanTeamAttack,
            LocationName.kannons_klaim_banana_coin_1:
                CanUseKannons,
            LocationName.kannons_klaim_banana_coin_2:
                CanUseKannons & (CanCartwheel | CanHover),
            LocationName.kannons_klaim_banana_coin_3:
                CanUseKannons & CanUseDiddyBarrels,


            LocationName.lava_lagoon_clear:
                CanSwim & HasGlimmer & CanUseKannons & 
                    HasEnguarde,
            LocationName.lava_lagoon_kong:
                CanSwim & HasGlimmer & CanUseKannons & 
                    HasEnguarde,
            LocationName.lava_lagoon_dk_coin:
                CanSwim & HasGlimmer & CanUseKannons & 
                    HasEnguarde,
            LocationName.lava_lagoon_bonus_1:
                CanSwim & HasGlimmer & CanUseKannons & 
                    HasEnguarde & CanCarry,
            LocationName.lava_lagoon_banana_coin_1:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_banana_coin_2:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_banana_bunch_1:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_banana_coin_3:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_banana_bunch_2:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_banana_coin_4:
                CanSwim & HasGlimmer & CanUseKannons,
            LocationName.lava_lagoon_banana_coin_5:
                CanSwim & HasGlimmer & 
                    CanUseKannons & CanBeInvincible,
            LocationName.lava_lagoon_banana_bunch_3:
                CanSwim & HasGlimmer & 
                    CanUseKannons,
            LocationName.lava_lagoon_banana_coin_6:
                CanSwim & HasGlimmer & CanUseKannons,
            LocationName.lava_lagoon_banana_coin_7:
                CanSwim & HasGlimmer & CanUseKannons,
            LocationName.lava_lagoon_red_balloon_1:
                CanSwim & HasGlimmer & CanUseKannons & HasEnguarde,
            LocationName.lava_lagoon_banana_bunch_4:
                CanSwim & HasGlimmer & CanUseKannons & CanCarry & HasEnguarde,
            LocationName.lava_lagoon_banana_bunch_5:
                CanSwim & HasGlimmer & CanUseKannons,
            LocationName.lava_lagoon_banana_coin_8:
                CanSwim & HasGlimmer & CanUseKannons,
            LocationName.lava_lagoon_banana_coin_9:
                CanSwim & HasGlimmer & CanUseKannons,
            LocationName.lava_lagoon_banana_coin_10:
                CanSwim & HasGlimmer & CanUseKannons & 
                    CanTeamAttack,


            LocationName.red_hot_ride_clear:
                True_(),
            LocationName.red_hot_ride_kong:
                CanCarry,
            LocationName.red_hot_ride_dk_coin:
                CanCarry & CanTeamAttack,
            LocationName.red_hot_ride_bonus_1:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_bonus_2:
                True_(),
            LocationName.red_hot_ride_banana_bunch_1:
                True_(),
            LocationName.red_hot_ride_banana_coin_1:
                True_(),
            LocationName.red_hot_ride_banana_coin_2:
                True_(),
            LocationName.red_hot_ride_banana_bunch_2:
                CanCarry,
            LocationName.red_hot_ride_banana_coin_3:
                CanCarry | HasRambi,
            LocationName.red_hot_ride_banana_bunch_3:
                True_(),
            LocationName.red_hot_ride_banana_coin_4:
                True_(),
            LocationName.red_hot_ride_banana_coin_5:
                CanCarry & HasRambi,
            LocationName.red_hot_ride_banana_coin_6:
                CanCarry,
            LocationName.red_hot_ride_banana_bunch_4:
                True_(),


            LocationName.squawks_shaft_clear:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_kong:
                CanUseKannons & CanCarry & HasSquawks,
            LocationName.squawks_shaft_dk_coin:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_bonus_1:
                CanUseKannons & CanCarry & (
                    CanCartwheel | 
                    CanHover
                ),
            LocationName.squawks_shaft_bonus_2:
                CanUseKannons & CanTeamAttack,
            LocationName.squawks_shaft_bonus_3:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_1:
                CanCartwheel,
            LocationName.squawks_shaft_banana_bunch_1:
                CanUseKannons,
            LocationName.squawks_shaft_banana_coin_2:
                CanUseKannons & CanCarry & (
                    CanCartwheel | 
                    CanHover
                ),
            LocationName.squawks_shaft_banana_bunch_2:
                CanUseKannons,
            LocationName.squawks_shaft_red_balloon_1:
                CanUseKannons & CanCarry & CanCartwheel, 
            LocationName.squawks_shaft_banana_coin_3:
                CanUseKannons & CanUseDixieBarrels,
            LocationName.squawks_shaft_banana_coin_4:
                CanUseKannons & CanUseDixieBarrels,
            LocationName.squawks_shaft_banana_coin_5:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_6:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_7:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_bunch_3:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_bunch_4:
                CanUseKannons & HasSquawks,


            LocationName.kleevers_kiln_clear:
                CanCling & CanCarry,
            LocationName.kleever_defeated:
                CanCling & CanCarry,
            LocationName.kleevers_kiln_banana_coin_1:
                CanCling & CanCarry & 
                    CanHover,
            LocationName.kleevers_kiln_banana_coin_2:
                CanCling & CanCarry & 
                    CanHover,


            LocationName.barrel_bayou_clear:
                CanUseControllableBarrels & CanUseKannons,
            LocationName.barrel_bayou_kong:
                CanUseControllableBarrels & CanUseKannons & 
                    CanCartwheel,
            LocationName.barrel_bayou_dk_coin:
                CanUseControllableBarrels & HasRambi,
            LocationName.barrel_bayou_bonus_1:
                CanUseControllableBarrels & CanCarry,
            LocationName.barrel_bayou_bonus_2:
                CanUseControllableBarrels  &
                    CanUseKannons & CanTeamAttack,
            LocationName.barrel_bayou_banana_bunch_1:
                CanTeamAttack,
            LocationName.barrel_bayou_banana_coin_1:
                CanUseControllableBarrels & HasRambi,
            LocationName.barrel_bayou_banana_bunch_2:
                CanUseControllableBarrels,
            LocationName.barrel_bayou_green_balloon:
                CanUseControllableBarrels & CanCarry & CanUseKannons,
            LocationName.barrel_bayou_banana_coin_2:
                CanUseControllableBarrels & CanUseKannons,
            LocationName.barrel_bayou_banana_bunch_3:
                CanUseControllableBarrels & 
                    CanUseKannons & CanTeamAttack,


            LocationName.glimmers_galleon_clear:
                CanSwim,
            LocationName.glimmers_galleon_kong:
                CanSwim,
            LocationName.glimmers_galleon_dk_coin:
                CanSwim,
            LocationName.glimmers_galleon_bonus_1:
                CanSwim,
            LocationName.glimmers_galleon_bonus_2:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_1:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_2:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_1:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_2:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_3:
                CanSwim,
            LocationName.glimmers_galleon_red_balloon:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_4:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_3:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_5:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_4:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_6:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_7:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_5:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_8:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_6:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_9:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_10:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_11:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_12:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_7:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_8:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_13:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_9:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_14:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_10:
                CanSwim,


            LocationName.krockhead_klamber_clear:
                CanClimb & CanUseKannons,
            LocationName.krockhead_klamber_kong:
                CanClimb & CanUseKannons,
            LocationName.krockhead_klamber_dk_coin:
                CanTeamAttack & CanCarry & CanCartwheel,
            LocationName.krockhead_klamber_bonus_1:
                CanClimb & CanTeamAttack & HasSquitter,
            LocationName.krockhead_klamber_red_balloon_1:
                CanTeamAttack & CanCarry,
            LocationName.krockhead_klamber_banana_coin_1:
                CanTeamAttack & CanCartwheel,
            LocationName.krockhead_klamber_banana_coin_2:
                CanClimb,
            LocationName.krockhead_klamber_red_balloon_2:
                CanClimb & CanTeamAttack & HasSquitter,
            LocationName.krockhead_klamber_banana_coin_3:
                CanClimb,


            LocationName.rattle_battle_clear:
                HasRattly,
            LocationName.rattle_battle_kong:
                HasRattly,
            LocationName.rattle_battle_dk_coin:
                HasRattly & CanUseKannons,
            LocationName.rattle_battle_bonus_1:
                CanTeamAttack  &
                    (CanHover | CanCartwheel),
            LocationName.rattle_battle_bonus_2:
                HasRattly,
            LocationName.rattle_battle_bonus_3:
                HasRattly,
            LocationName.rattle_battle_banana_coin_1:
                True_(),
            LocationName.rattle_battle_banana_bunch_1:
                True_(),
            LocationName.rattle_battle_banana_bunch_2:
                HasRattly,
            LocationName.rattle_battle_banana_coin_2:
                HasRattly,
            LocationName.rattle_battle_banana_coin_3:
                HasRattly,
            LocationName.rattle_battle_banana_bunch_3:
                HasRattly,
            LocationName.rattle_battle_banana_bunch_4:
                HasRattly,


            LocationName.slime_climb_clear:
                CanClimb & CanSwim & CanUseKannons,
            LocationName.slime_climb_kong:
                CanClimb & CanSwim &  
                    (CanCartwheel | CanHover),
            LocationName.slime_climb_dk_coin:
                CanClimb & CanSwim & CanTeamAttack & 
                    CanBeInvincible,
            LocationName.slime_climb_bonus_1:
                CanClimb & CanSwim & CanBeInvincible & 
                    CanCling & CanCartwheel,
            LocationName.slime_climb_bonus_2:
                CanClimb & CanSwim & CanCarry,
            LocationName.slime_climb_banana_coin_1:
                CanCartwheel,
            LocationName.slime_climb_banana_coin_2:
                CanClimb & CanSwim & 
                    CanCartwheel,
            LocationName.slime_climb_banana_bunch_1:
                CanClimb & CanSwim & 
                    CanCartwheel,
            LocationName.slime_climb_banana_bunch_2:
                CanClimb & CanSwim,
            LocationName.slime_climb_banana_coin_3:
                CanClimb & CanSwim & 
                    CanCartwheel,
            LocationName.slime_climb_banana_bunch_3:
                CanClimb & CanSwim & 
                    CanCartwheel & CanHover,
            LocationName.slime_climb_banana_bunch_4:
                CanClimb & CanSwim & 
                    CanCartwheel & CanHover,


            LocationName.bramble_blast_clear:
                CanUseKannons,
            LocationName.bramble_blast_kong:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_dk_coin:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_bonus_1:
                CanUseKannons,
            LocationName.bramble_blast_bonus_2:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_1:
                CanTeamAttack,
            LocationName.bramble_blast_banana_bunch_2:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_3:
                CanUseKannons,
            LocationName.bramble_blast_banana_coin_1:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_4:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_5:
                CanUseKannons,
            LocationName.bramble_blast_banana_coin_2:
                CanUseKannons,
            LocationName.bramble_blast_red_balloon:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_6:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_7:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_8:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_9:
                CanUseKannons & HasSquawks,


            LocationName.kudgels_kontest_clear:
                CanCarry,
            LocationName.kudgel_defeated:
                CanCarry,


            LocationName.hornet_hole_clear:
                CanCling,
            LocationName.hornet_hole_kong:
                CanCling,
            LocationName.hornet_hole_dk_coin:
                CanCling & HasSquitter & CanTeamAttack,
            LocationName.hornet_hole_bonus_1:
                CanTeamAttack & CanCling & CanCarry,
            LocationName.hornet_hole_bonus_2:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_bonus_3:
                CanCling & HasSquitter & CanTeamAttack,
            LocationName.hornet_hole_banana_bunch_1:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_banana_coin_1:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_banana_bunch_2:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_banana_coin_2:
                True_(),
            LocationName.hornet_hole_green_balloon_1:
                CanCarry,
            LocationName.hornet_hole_banana_coin_3:
                True_(),
            LocationName.hornet_hole_banana_bunch_3:
                CanTeamAttack & HasSquitter & 
                    CanCling,
            LocationName.hornet_hole_banana_coin_4:
                CanTeamAttack & HasSquitter & 
                    CanCling,
            LocationName.hornet_hole_banana_bunch_4:
                CanTeamAttack & HasSquitter & 
                    CanCling,
            LocationName.hornet_hole_banana_bunch_5:
                CanTeamAttack & CanCling,
            LocationName.hornet_hole_red_balloon_1:
                CanTeamAttack & HasSquitter & 
                    CanCling,


            LocationName.target_terror_clear:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_kong:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_dk_coin:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_bonus_1:
                CanUseKannons & CanRideSkullKart & HasSquawks,
            LocationName.target_terror_bonus_2:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_banana_bunch_1:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_banana_bunch_2:
                CanUseKannons & CanRideSkullKart & HasSquawks,
            LocationName.target_terror_red_balloon:
                CanUseKannons & CanRideSkullKart,


            LocationName.bramble_scramble_clear:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_kong:
                CanClimb & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_dk_coin:
                CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_bonus_1:
                CanClimb & CanTeamAttack  &
                    CanBeInvincible & CanUseKannons & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_1:
                True_(),
            LocationName.bramble_scramble_banana_bunch_2:
                CanCarry & HasBothKongs & CanClimb,
            LocationName.bramble_scramble_banana_coin_1:
                CanClimb & CanTeamAttack  &
                    CanBeInvincible & CanUseKannons,
            LocationName.bramble_scramble_banana_coin_2:
                CanClimb & CanTeamAttack  &
                    CanBeInvincible & CanUseKannons & HasSquawks,
            LocationName.bramble_scramble_banana_coin_3:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_3:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_4:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_4:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_5:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_5:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_6:
                CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks,
            LocationName.bramble_scramble_banana_coin_7:
                CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks,
            LocationName.bramble_scramble_banana_coin_8:
                CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks,
            LocationName.bramble_scramble_blue_balloon:
                CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks,
            LocationName.bramble_scramble_red_balloon:
                CanCartwheel & CanClimb & 
                    HasSquitter & HasSquawks,


            LocationName.rickety_race_clear:
                CanRideSkullKart,
            LocationName.rickety_race_kong:
                CanRideSkullKart,
            LocationName.rickety_race_dk_coin:
                CanRideSkullKart,
            LocationName.rickety_race_bonus_1:
                CanRideSkullKart & CanTeamAttack & (
                    CanHover | 
                    (CanCartwheel & CanCartwheel)
                ),
            LocationName.rickety_race_banana_coin:
                CanRideSkullKart,


            LocationName.mudhole_marsh_clear:
                CanClimb & CanCling,
            LocationName.mudhole_marsh_kong:
                CanClimb & CanCling & CanCarry & 
                    CanTeamAttack,
            LocationName.mudhole_marsh_dk_coin:
                CanClimb & CanCling & CanHover,
            LocationName.mudhole_marsh_bonus_1:
                CanCling & CanCarry & 
                    CanTeamAttack,
            LocationName.mudhole_marsh_bonus_2:
                CanClimb & CanCling & CanCarry,
            LocationName.mudhole_marsh_banana_coin_1:
                True_(),
            LocationName.mudhole_marsh_banana_bunch_1:
                CanCling & CanCarry,
            LocationName.mudhole_marsh_banana_coin_2:
                CanCling & CanCarry & CanTeamAttack & 
                    CanBeInvincible,
            LocationName.mudhole_marsh_banana_coin_3:
                CanCling & CanCarry & CanTeamAttack & 
                    CanClimb,
            LocationName.mudhole_marsh_banana_coin_4:
                CanCling & CanCarry & CanTeamAttack & 
                    CanClimb & CanCartwheel,
            LocationName.mudhole_marsh_banana_coin_5:
                CanCling & CanCarry & CanTeamAttack & 
                    CanClimb,


            LocationName.rambi_rumble_clear:
                CanCling & CanUseKannons & HasRambi,
            LocationName.rambi_rumble_kong:
                CanCling & CanUseKannons & HasRambi & 
                    CanCartwheel,
            LocationName.rambi_rumble_dk_coin:
                CanCling & CanUseKannons,
            LocationName.rambi_rumble_bonus_1:
                CanCling & CanUseKannons & CanTeamAttack,
            LocationName.rambi_rumble_bonus_2:
                CanCling & CanUseKannons & HasRambi,
            LocationName.rambi_rumble_banana_coin_1:
                True_(),
            LocationName.rambi_rumble_banana_bunch_1:
                CanHover | CanCartwheel,
            LocationName.rambi_rumble_banana_bunch_2:
                CanCling & CanUseKannons,
            LocationName.rambi_rumble_banana_coin_2:
                CanCling & CanUseKannons & CanTeamAttack,
            LocationName.rambi_rumble_banana_bunch_3:
                CanCling & CanUseKannons & 
                    HasRambi,


            LocationName.king_zing_sting_clear:
                HasSquawks,
            LocationName.king_zing_defeated:
                HasSquawks,
            LocationName.king_zing_sting_banana_coin_1:
                True_(),
            LocationName.king_zing_sting_banana_coin_2:
                True_(),


            LocationName.ghostly_grove_clear:
                CanClimb,
            LocationName.ghostly_grove_kong:
                CanClimb & CanCarry,
            LocationName.ghostly_grove_dk_coin:
                CanClimb & CanUseKannons & (
                    CanCartwheel | CanHover
                ),
            LocationName.ghostly_grove_bonus_1:
                CanClimb & CanCarry,
            LocationName.ghostly_grove_bonus_2:
                CanClimb,
            LocationName.ghostly_grove_banana_bunch_1:
                True_(),
            LocationName.ghostly_grove_red_balloon:
                CanCarry,
            LocationName.ghostly_grove_banana_bunch_2:
                True_(),
            LocationName.ghostly_grove_banana_coin_1:
                CanClimb & CanCartwheel,
            LocationName.ghostly_grove_banana_bunch_3:
                CanClimb,
            LocationName.ghostly_grove_banana_bunch_4:
                CanClimb,
            LocationName.ghostly_grove_banana_coin_2:
                CanClimb,


            LocationName.haunted_hall_clear:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_kong:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_dk_coin:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_bonus_1:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_bonus_2:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_bonus_3:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_banana_bunch_1:
                True_(),
            LocationName.haunted_hall_banana_bunch_2:
                True_(),
            LocationName.haunted_hall_banana_coin_1:
                CanCartwheel,
            LocationName.haunted_hall_banana_coin_2:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),
            LocationName.haunted_hall_banana_coin_3:
                CanRideSkullKart & (
                    CanCartwheel | CanHover | CanCling | 
                    CanTeamAttack
                ),


            LocationName.gusty_glade_clear:
                CanCling & CanUseKannons,
            LocationName.gusty_glade_kong:
                CanCling & CanUseKannons & CanCarry  &
                    CanCartwheel,
            LocationName.gusty_glade_dk_coin:
                CanCling & CanUseKannons & CanHover,
            LocationName.gusty_glade_bonus_1:
                CanTeamAttack & (CanCling | HasRattly),
            LocationName.gusty_glade_bonus_2:
                CanCling & CanCarry & CanUseKannons,
            LocationName.gusty_glade_banana_coin_1:
                CanTeamAttack,
            LocationName.gusty_glade_banana_coin_2:
                CanCartwheel,
            LocationName.gusty_glade_blue_balloon:
                CanTeamAttack & HasRattly,
            LocationName.gusty_glade_banana_coin_3:
                CanCling & CanUseKannons & CanCartwheel,


            LocationName.parrot_chute_panic_clear:
                HasSquawks,
            LocationName.parrot_chute_panic_kong:
                HasSquawks,
            LocationName.parrot_chute_panic_dk_coin:
                CanCartwheel | CanHover,
            LocationName.parrot_chute_panic_bonus_1:
                HasSquawks,
            LocationName.parrot_chute_panic_bonus_2:
                HasSquawks & CanCartwheel & CanCarry,
            LocationName.parrot_chute_panic_banana_coin_1:
                HasSquawks & CanCarry,
            LocationName.parrot_chute_panic_banana_coin_2:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_bunch_1:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_3:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_bunch_2:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_4:
                HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_5:
                HasSquawks & CanUseControllableBarrels
                    & (CanTeamAttack | CanCartwheel),


            LocationName.web_woods_clear:
                HasSquitter,
            LocationName.web_woods_kong:
                HasSquitter & CanTeamAttack,
            LocationName.web_woods_dk_coin:
                HasSquitter & (CanTeamAttack | CanUseKannons),
            LocationName.web_woods_bonus_1:
                HasSquitter,
            LocationName.web_woods_bonus_2:
                HasSquitter,
            LocationName.web_woods_banana_coin_1:
                CanTeamAttack,
            LocationName.web_woods_banana_coin_2:
                CanTeamAttack & CanCarry,
            LocationName.web_woods_green_balloon_1:
                CanTeamAttack & CanCarry & CanUseKannons,
            LocationName.web_woods_banana_bunch_1:
                CanTeamAttack | CanCartwheel,
            LocationName.web_woods_banana_bunch_2:
                CanCarry,
            LocationName.web_woods_banana_bunch_3:
                HasSquitter,
            LocationName.web_woods_banana_coin_3:
                HasSquitter,
            LocationName.web_woods_banana_coin_4:
                HasSquitter,
            LocationName.web_woods_banana_coin_5:
                HasSquitter,
            LocationName.web_woods_green_balloon_2:
                HasSquitter & CanTeamAttack,


            LocationName.kreepy_krow_clear:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry,
            LocationName.kreepy_krow_defeated:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry,
            LocationName.kreepy_krow_banana_coin_1:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry,
            LocationName.kreepy_krow_banana_coin_2:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry,


            LocationName.arctic_abyss_clear:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_kong:
                CanSwim & HasEnguarde & (
                    CanCartwheel | CanHover
                ),
            LocationName.arctic_abyss_dk_coin:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_bonus_1:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_bonus_2:
                CanSwim & HasEnguarde & CanCarry,
            LocationName.arctic_abyss_banana_coin_1:
                CanHover | (CanCartwheel & CanCartwheel),
            LocationName.arctic_abyss_banana_bunch_1:
                CanHover | (CanCartwheel & CanCartwheel),
            LocationName.arctic_abyss_banana_bunch_2:
                CanHover | (CanCartwheel & CanCartwheel),
            LocationName.arctic_abyss_banana_bunch_3:
                CanHover | (CanCartwheel & CanCartwheel),
            LocationName.arctic_abyss_banana_bunch_4:
                CanSwim,
            LocationName.arctic_abyss_banana_coin_2:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_coin_3:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_coin_4:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_bunch_5:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_coin_5:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_bunch_6:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_banana_bunch_7:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_red_balloon_1:
                CanSwim & HasEnguarde,
            LocationName.arctic_abyss_red_balloon_2:
                CanSwim & HasEnguarde,


            LocationName.windy_well_clear:
                CanUseKannons & CanCling,
            LocationName.windy_well_kong:
                CanUseKannons & CanCling,
            LocationName.windy_well_dk_coin:
                CanUseKannons & CanCling,
            LocationName.windy_well_bonus_1:
                CanCling,
            LocationName.windy_well_bonus_2:
                CanUseKannons & CanCling & CanCarry & 
                    HasSquawks,
            LocationName.windy_well_banana_coin_1:
                True_(),
            LocationName.windy_well_banana_coin_2:
                CanCling,
            LocationName.windy_well_banana_coin_3:
                CanCling,
            LocationName.windy_well_banana_bunch_1:
                CanUseKannons & CanCling & CanCarry,
            LocationName.windy_well_banana_bunch_2:
                CanUseKannons & CanCling & CanCarry,
            LocationName.windy_well_banana_coin_4:
                CanCling & CanCarry,
            LocationName.windy_well_banana_bunch_3:
                CanCling & CanCarry,
            LocationName.windy_well_red_balloon:
                CanCling & CanCarry,
            LocationName.windy_well_banana_bunch_4:
                CanCling & CanCarry & 
                    HasSquawks,


            LocationName.castle_crush_clear:
                CanCartwheel | (HasRambi & CanCarry & HasBothKongs),
            LocationName.castle_crush_kong:
                CanCartwheel | (HasRambi & CanCarry & HasBothKongs),
            LocationName.castle_crush_dk_coin:
                CanCartwheel & HasSquawks,
            LocationName.castle_crush_bonus_1:
                HasRambi & CanCarry & HasBothKongs,
            LocationName.castle_crush_bonus_2:
                CanCartwheel & CanCarry & HasSquawks & HasBothKongs,
            LocationName.castle_crush_banana_coin_1:
                True_(),
            LocationName.castle_crush_banana_bunch_1:
                True_(),
            LocationName.castle_crush_banana_bunch_2:
                True_(),
            LocationName.castle_crush_banana_coin_2:
                True_(),
            LocationName.castle_crush_banana_bunch_3:
                HasRambi & CanCarry & 
                    HasBothKongs,
            LocationName.castle_crush_banana_bunch_4:
                True_(),
            LocationName.castle_crush_banana_bunch_5:
                CanCartwheel & HasSquawks,
            LocationName.castle_crush_banana_coin_3:
                CanCarry & 
                    HasBothKongs & CanCartwheel,
            LocationName.castle_crush_banana_bunch_6:
                CanCarry & 
                    HasBothKongs & CanCartwheel,


            LocationName.clappers_cavern_clear:
                HasGlimmer & CanSwim & CanUseKannons & 
                    CanCling,
            LocationName.clappers_cavern_kong:
                HasGlimmer & CanSwim & CanUseKannons & 
                    CanCling,
            LocationName.clappers_cavern_dk_coin:
                CanTeamAttack & CanCling,
            LocationName.clappers_cavern_bonus_1:
                CanTeamAttack & CanCling,
            LocationName.clappers_cavern_bonus_2:
                HasGlimmer & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_coin_1:
                HasGlimmer,
            LocationName.clappers_cavern_banana_bunch_1:
                HasGlimmer & CanSwim & CanUseKannons,
            LocationName.clappers_cavern_banana_bunch_2:
                HasGlimmer & CanSwim & CanUseKannons,
            LocationName.clappers_cavern_banana_bunch_3:
                HasGlimmer & CanSwim & CanUseKannons,
            LocationName.clappers_cavern_banana_coin_2:
                HasGlimmer & CanSwim & CanUseKannons,
            LocationName.clappers_cavern_banana_bunch_4:
                HasGlimmer & CanSwim & CanUseKannons & 
                    HasEnguarde,
            LocationName.clappers_cavern_banana_coin_3:
                HasGlimmer & CanSwim & CanUseKannons & 
                    CanTeamAttack & CanBeInvincible,
            LocationName.clappers_cavern_banana_coin_4:
                HasGlimmer & CanSwim & CanUseKannons & 
                    CanTeamAttack & CanBeInvincible,
            LocationName.clappers_cavern_banana_coin_5:
                HasGlimmer & CanSwim & CanUseKannons & 
                    CanTeamAttack & CanBeInvincible,


            LocationName.chain_link_chamber_clear:
                CanClimb & (
                    CanCling | 
                    (CanUseControllableBarrels & CanUseKannons)
                ),
            LocationName.chain_link_chamber_kong:
                CanClimb & (
                    CanCling | 
                    (CanUseControllableBarrels & CanUseKannons)
                ),
            LocationName.chain_link_chamber_dk_coin:
                CanClimb & (
                    CanCling | 
                    (CanUseControllableBarrels & CanUseKannons)
                ),
            LocationName.chain_link_chamber_bonus_1:
                CanClimb & CanCling & CanCarry,
            LocationName.chain_link_chamber_bonus_2:
                CanClimb & CanUseControllableBarrels & (
                    (CanCling | CanUseKannons) & 
                    (CanCartwheel | CanTeamAttack)
                ),
            LocationName.chain_link_chamber_banana_coin_1:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_1:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_2:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_3:
                CanClimb & CanCarry,
            LocationName.chain_link_chamber_banana_coin_2:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            LocationName.chain_link_chamber_banana_bunch_4:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            LocationName.chain_link_chamber_banana_coin_3:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            LocationName.chain_link_chamber_banana_coin_4:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            

            LocationName.toxic_tower_clear:
                HasRattly & HasSquawks & HasSquitter & 
                    CanUseKannons,
            LocationName.toxic_tower_kong:
                HasRattly & HasSquawks & HasSquitter & 
                    CanUseKannons,
            LocationName.toxic_tower_dk_coin:
                HasRattly & CanUseKannons,
            LocationName.toxic_tower_bonus_1:
                HasRattly & HasSquawks & HasSquitter & 
                    CanUseKannons,
            LocationName.toxic_tower_banana_bunch_1:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_2:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_3:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_4:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_5:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_6:
                HasRattly,
            LocationName.toxic_tower_banana_bunch_7:
                HasRattly,
            LocationName.toxic_tower_banana_coin_1:
                HasRattly,
            LocationName.toxic_tower_banana_coin_2:
                HasRattly,
            LocationName.toxic_tower_banana_coin_3:
                HasRattly,
            LocationName.toxic_tower_banana_coin_4:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_coin_5:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_bunch_8:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_bunch_9:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_green_balloon:
                HasRattly & HasSquawks & (CanCartwheel | CanClimb),


            LocationName.stronghold_showdown_clear:
                True_(),
            LocationName.stronghold_showdown_banana_coin_1:
                CanTeamAttack,
            LocationName.stronghold_showdown_red_balloon:
                CanTeamAttack,
            LocationName.stronghold_showdown_banana_coin_2:
                CanTeamAttack,


            LocationName.screechs_sprint_clear:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_kong:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_dk_coin:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_bonus_1:
                CanClimb & CanTeamAttack & CanCarry & 
                    CanCartwheel & CanHover,
            LocationName.screechs_sprint_banana_coin_1:
                CanCartwheel,
            LocationName.screechs_sprint_banana_bunch_1:
                CanClimb & CanCarry & CanCartwheel,
            LocationName.screechs_sprint_banana_coin_2:
                CanClimb & CanCarry & CanCartwheel,
            LocationName.screechs_sprint_banana_coin_3:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_red_balloon:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_bunch_2:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_bunch_3:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_coin_4:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_coin_5:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_coin_6:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_coin_7:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_coin_8:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_bunch_4:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_bunch_5:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),
            LocationName.screechs_sprint_banana_bunch_6:
                CanClimb & HasSquawks & (
                    (CanCartwheel & CanCartwheel) | CanHover
                ),


            LocationName.k_rool_duel_clear:
                CanCarry,


            LocationName.jungle_jinx_clear:
                CanCartwheel & CanUseKannons,
            LocationName.jungle_jinx_kong:
                CanCartwheel & CanUseKannons & CanCarry,
            LocationName.jungle_jinx_dk_coin:
                CanCartwheel & CanTeamAttack,
            LocationName.jungle_jinx_banana_bunch_1:
                True_(),
            LocationName.jungle_jinx_banana_bunch_2:
                True_(),
            LocationName.jungle_jinx_banana_coin_1:
                CanHover,
            LocationName.jungle_jinx_banana_coin_2:
                CanCartwheel,
            LocationName.jungle_jinx_banana_coin_3:
                CanCartwheel & CanUseKannons,
            LocationName.jungle_jinx_banana_coin_4:
                CanCartwheel & CanUseKannons & CanTeamAttack,
            LocationName.jungle_jinx_banana_coin_5:
                CanCartwheel & CanUseKannons,

            LocationName.black_ice_battle_clear:
                True_(),
            LocationName.black_ice_battle_kong:
                CanCarry,
            LocationName.black_ice_battle_dk_coin:
                CanCarry,
            LocationName.black_ice_battle_banana_bunch_1:
                CanCartwheel,
            LocationName.black_ice_battle_red_balloon_1:
                True_(),
            LocationName.black_ice_battle_red_balloon_2:
                True_(),
            LocationName.black_ice_battle_red_balloon_3:
                CanCarry,
            LocationName.black_ice_battle_banana_bunch_2:
                True_(),
            LocationName.black_ice_battle_banana_coin_1:
                True_(),
            LocationName.black_ice_battle_banana_bunch_3:
                CanCarry,


            LocationName.klobber_karnage_clear:
                CanCarry & CanUseControllableBarrels & 
                    CanUseKannons & CanUseDiddyBarrels & 
                    CanUseDixieBarrels,
            LocationName.klobber_karnage_kong:
                CanCarry & CanUseControllableBarrels & 
                    CanUseKannons & CanUseDiddyBarrels & 
                    CanUseDixieBarrels,
            LocationName.klobber_karnage_dk_coin:
                CanCarry & CanUseKannons & CanBeInvincible & 
                    CanUseDiddyBarrels & CanUseDixieBarrels & 
                    CanUseControllableBarrels,
            LocationName.klobber_karnage_banana_coin_1:
                True_(),
            LocationName.klobber_karnage_banana_bunch_1:
                CanCartwheel,
            LocationName.klobber_karnage_banana_bunch_2:
                CanCartwheel,
            LocationName.klobber_karnage_banana_coin_2:
                CanCartwheel,
            LocationName.klobber_karnage_banana_bunch_3:
                CanCartwheel,
            LocationName.klobber_karnage_banana_coin_3:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseControllableBarrels,
            LocationName.klobber_karnage_banana_bunch_4:
                (CanCartwheel & CanCartwheel | CanHover),
            LocationName.klobber_karnage_banana_bunch_5:
                (CanCartwheel & CanCartwheel | CanHover & CanUseKannons),
            LocationName.klobber_karnage_banana_bunch_6:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_banana_bunch_7:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_banana_coin_4:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,
            LocationName.klobber_karnage_red_balloon:
                CanCartwheel & CanUseDiddyBarrels & 
                    CanUseDixieBarrels & CanUseControllableBarrels & 
                    CanUseKannons,


            LocationName.fiery_furnace_clear:
                CanUseControllableBarrels & CanCartwheel,
            LocationName.fiery_furnace_kong:
                CanUseControllableBarrels & CanCartwheel
                    & CanTeamAttack,
            LocationName.fiery_furnace_dk_coin:
                CanUseControllableBarrels & CanCartwheel
                    & CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_1:
                CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_2:
                CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_3:
                CanTeamAttack,
            LocationName.fiery_furnace_banana_bunch_4:
                CanUseControllableBarrels,
            LocationName.fiery_furnace_banana_coin_1:
                CanUseControllableBarrels & CanCartwheel,
            LocationName.fiery_furnace_banana_coin_2:
                CanUseControllableBarrels & CanCartwheel,
            LocationName.fiery_furnace_banana_bunch_5:
                CanUseControllableBarrels & CanCartwheel,


            LocationName.animal_antics_clear:
                HasRambi & HasEnguarde & HasSquitter & 
                    HasSquawks & HasRattly & CanSwim & 
                    CanUseKannons,
            LocationName.animal_antics_kong:
                HasRambi & HasEnguarde & HasSquitter & 
                    HasSquawks & HasRattly & CanSwim & 
                    CanUseKannons,
            LocationName.animal_antics_dk_coin:
                HasRambi & HasEnguarde & HasSquitter & 
                    HasSquawks & CanSwim,
            LocationName.animal_antics_banana_bunch_1:
                HasRambi & 
                    HasEnguarde & CanSwim,
            LocationName.animal_antics_banana_bunch_2:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter,
            LocationName.animal_antics_banana_coin_1:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter,
            LocationName.animal_antics_banana_coin_2:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_bunch_3:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_bunch_4:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_coin_3:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_coin_4:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_red_balloon:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks & CanUseKannons,
            LocationName.animal_antics_banana_coin_5:
                HasRambi & 
                    HasEnguarde & CanSwim & HasSquitter & 
                    HasSquawks  & CanUseKannons & HasRattly,


            LocationName.krocodile_core_clear:
                CanCarry,
        }


class DKC2ExpertRules(DKC2Rules):
    def __init__(self, world: "DKC2World") -> None:
        super().__init__(world)

        self.location_rules = {
            LocationName.pirate_panic_bonus_2: 
                CanCarry | HasRambi,
            LocationName.pirate_panic_banana_coin_1:
                CanTeamAttack,
            LocationName.pirate_panic_banana_bunch_1:
                True_(),
            LocationName.pirate_panic_red_balloon:
                True_(),
            LocationName.pirate_panic_banana_coin_2:
                CanTeamAttack | CanCarry | HasRambi,
            LocationName.pirate_panic_banana_coin_3:
                True_(),
            LocationName.pirate_panic_green_balloon:
                HasRambi,


            LocationName.mainbrace_mayhem_clear:
                CanClimb,
            LocationName.mainbrace_mayhem_kong:
                CanClimb,
            LocationName.mainbrace_mayhem_dk_coin:
                CanClimb & CanTeamAttack, 
            LocationName.mainbrace_mayhem_bonus_1:
                CanClimb & (
                    CanHover | CanCartwheel),
            LocationName.mainbrace_mayhem_bonus_2:
                CanCarry & CanClimb,
            LocationName.mainbrace_mayhem_bonus_3:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_bunch_1:
                CanCartwheel,
            LocationName.mainbrace_mayhem_banana_coin_1:
                CanClimb | CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_coin_2:
                CanClimb | CanTeamAttack,
            LocationName.mainbrace_mayhem_green_balloon:
                CanClimb,
            LocationName.mainbrace_mayhem_banana_bunch_2:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_coin_3:
                CanClimb & CanTeamAttack,
            LocationName.mainbrace_mayhem_banana_bunch_3:
                CanClimb & CanTeamAttack,


            LocationName.gangplank_galley_clear:
                CanCling | (
                    CanTeamAttack & CanHover
                    ),
            LocationName.gangplank_galley_kong:
                CanCarry & CanTeamAttack & (
                    CanCling | CanHover
                ),
            LocationName.gangplank_galley_dk_coin:
                CanCartwheel & (
                    CanCling | CanHover
                    ) | (CanTeamAttack & CanCling
                ),
            LocationName.gangplank_galley_bonus_1:
                CanCarry,
            LocationName.gangplank_galley_bonus_2:
                CanCling,
            LocationName.gangplank_galley_banana_bunch_1:
                CanHover | (
                    CanCling & (
                        (CanCartwheel & CanCartwheel) 
                        | CanTeamAttack)
                    ),
            LocationName.gangplank_galley_banana_bunch_2:
                CanCarry,
            LocationName.gangplank_galley_red_balloon_1:
                CanCarry,
            LocationName.gangplank_galley_banana_bunch_3:
                CanTeamAttack,
            LocationName.gangplank_galley_banana_coin_1:
                CanCarry,
            LocationName.gangplank_galley_banana_bunch_4:
                CanHover | CanUseKannons,
            LocationName.gangplank_galley_banana_coin_2:
                CanUseKannons,
            LocationName.gangplank_galley_banana_bunch_5:
                CanHover | CanUseKannons,
            LocationName.gangplank_galley_banana_bunch_6:
                CanCarry & (CanHover | CanCartwheel | CanCling),
            LocationName.gangplank_galley_banana_bunch_7:
                CanHover | CanCling,
            LocationName.gangplank_galley_red_balloon_2:
                CanCarry & (CanHover | CanCling),


            LocationName.lockjaws_locker_clear:
                CanSwim,
            LocationName.lockjaws_locker_kong:
                CanSwim,
            LocationName.lockjaws_locker_dk_coin:
                CanSwim,
            LocationName.lockjaws_locker_bonus_1:
                HasEnguarde & (CanSwim 
                    | (CanTeamAttack & CanHover)),
            LocationName.lockjaws_locker_banana_coin_1:
                True_(),
            LocationName.lockjaws_locker_banana_bunch_1:
                True_(),
            LocationName.lockjaws_locker_banana_coin_2:
                True_(),
            LocationName.lockjaws_locker_banana_bunch_2:
                CanSwim | CanHover | CanCartwheel,
            LocationName.lockjaws_locker_banana_coin_3:
                CanSwim | CanTeamAttack,
            LocationName.lockjaws_locker_banana_coin_4:
                CanSwim | (
                    HasEnguarde & CanTeamAttack & CanHover
                ),
            LocationName.lockjaws_locker_banana_coin_5:
                CanSwim | (
                    HasEnguarde & CanTeamAttack & CanHover
                ),
            LocationName.lockjaws_locker_banana_bunch_3:
                CanSwim | (
                    HasEnguarde & CanTeamAttack & CanHover
                ),
            LocationName.lockjaws_locker_red_balloon:
                HasEnguarde & (
                    CanSwim | (CanTeamAttack & CanHover)
                ),
            LocationName.lockjaws_locker_banana_coin_6:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_7:
                CanSwim,
            LocationName.lockjaws_locker_banana_coin_8:
                CanSwim,
            LocationName.lockjaws_locker_banana_bunch_4:
                HasEnguarde & CanSwim,


            LocationName.topsail_trouble_clear:
                CanClimb & (
                    CanTeamAttack | 
                     HasRattly | (
                        CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_kong:
                CanClimb & (
                    CanTeamAttack | 
                     HasRattly | (
                        CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_dk_coin:
                CanClimb & (
                    CanTeamAttack | 
                     HasRattly | (
                        CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_bonus_1:
                CanTeamAttack | HasRattly,

            LocationName.topsail_trouble_bonus_2:
                CanClimb & (
                    CanTeamAttack | 
                     HasRattly | (
                        CanCling & CanUseKannons)
                ),
            LocationName.topsail_trouble_red_balloon_1:
                HasRattly | CanTeamAttack | CanCling,
            LocationName.topsail_trouble_red_balloon_2:
                CanCarry & (
                    HasRattly | CanTeamAttack | CanCling
                ),
            LocationName.topsail_trouble_banana_bunch_1:
                HasRattly | CanTeamAttack | (
                    CanCling & CanUseKannons
                ),
            LocationName.topsail_trouble_banana_bunch_2:
                HasRattly | CanTeamAttack,
            LocationName.topsail_trouble_banana_coin_1:
                HasRattly | CanTeamAttack,
            LocationName.topsail_trouble_banana_coin_2:
                HasRattly,
            LocationName.topsail_trouble_banana_bunch_3:
                CanClimb & (
                    HasRattly | CanTeamAttack | (
                        CanCling & CanUseKannons)
                    ),
            LocationName.topsail_trouble_banana_coin_3:
                CanClimb & (
                    HasRattly | CanTeamAttack | (
                        CanCling & CanUseKannons)
                    ),
            LocationName.topsail_trouble_banana_coin_4:
                CanClimb & (
                    HasRattly | CanTeamAttack | (
                        CanCling & CanUseKannons)
                    ),
            LocationName.topsail_trouble_blue_balloon:
                CanClimb & (CanTeamAttack | 
                    (HasBothKongs & CanHover & 
                        (HasRattly | (CanCling & CanUseKannons)))
                    ),


            LocationName.krows_nest_clear:
                CanCarry,
            LocationName.krow_defeated:
                CanCarry,
            LocationName.krows_nest_banana_coin_1:
                True_(),
            LocationName.krows_nest_banana_coin_2:
                True_(),


            LocationName.hot_head_hop_clear:
                CanUseKannons | HasSquitter | (
                        CanTeamAttack & CanHover
                    ),
            LocationName.hot_head_hop_kong:
                CanCarry,
            LocationName.hot_head_hop_dk_coin:
                HasSquitter,
            LocationName.hot_head_hop_bonus_1:
                CanCarry,
            LocationName.hot_head_hop_bonus_2:
                HasSquitter,
            LocationName.hot_head_hop_bonus_3:
                HasSquitter,
            LocationName.hot_head_hop_green_balloon:
                CanCarry,
            LocationName.hot_head_hop_banana_coin_1:
                CanCarry,
            LocationName.hot_head_hop_banana_bunch_1:
                CanCarry,
            LocationName.hot_head_hop_banana_coin_2:
                HasSquitter | CanTeamAttack | CanCarry,
            LocationName.hot_head_hop_banana_bunch_2:
                HasSquitter,
            LocationName.hot_head_hop_banana_bunch_3:
                HasSquitter,
            LocationName.hot_head_hop_banana_coin_3:
                HasSquitter | CanHover | HasBothKongs,
            LocationName.hot_head_hop_banana_coin_4:
                HasSquitter | CanHover | (
                    CanUseKannons & (HasBothKongs | CanCartwheel)),
            LocationName.hot_head_hop_red_balloon:
                HasSquitter,


            LocationName.kannons_klaim_clear:
                CanUseKannons,
            LocationName.kannons_klaim_kong:
                CanUseKannons & CanCarry,
            LocationName.kannons_klaim_dk_coin:
                CanHover | CanCartwheel,
            LocationName.kannons_klaim_bonus_1:
                CanUseDiddyBarrels & CanUseDixieBarrels & (
                    CanHover | CanCartwheel
                ),
            LocationName.kannons_klaim_bonus_2:
                CanUseKannons,
            LocationName.kannons_klaim_bonus_3:
                CanUseKannons,
            LocationName.kannons_klaim_banana_bunch_1:
                CanUseKannons | CanTeamAttack,
            LocationName.kannons_klaim_banana_coin_1:
                CanUseKannons,
            LocationName.kannons_klaim_banana_coin_2:
                CanUseKannons & (CanTeamAttack | CanCartwheel),
            LocationName.kannons_klaim_banana_coin_3:
                CanUseKannons,


            LocationName.lava_lagoon_clear:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_kong:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_dk_coin:
                CanSwim & HasGlimmer,
            LocationName.lava_lagoon_bonus_1:
                CanSwim & 
                    HasGlimmer & 
                    CanCarry  &
                    HasEnguarde,
            LocationName.lava_lagoon_banana_coin_1:
                HasGlimmer | HasBothKongs,
            LocationName.lava_lagoon_banana_coin_2:
                HasGlimmer | HasBothKongs,
            LocationName.lava_lagoon_banana_bunch_1:
                HasGlimmer | HasBothKongs,
            LocationName.lava_lagoon_banana_coin_3:
                HasGlimmer & (CanSwim | HasBothKongs),
            LocationName.lava_lagoon_banana_bunch_2:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_4:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_5:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_bunch_3:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_6:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_7:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_red_balloon_1:
                HasGlimmer & CanSwim & HasEnguarde,
            LocationName.lava_lagoon_banana_bunch_4:
                HasGlimmer & CanSwim & HasEnguarde & CanCarry,
            LocationName.lava_lagoon_banana_bunch_5:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_8:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_9:
                HasGlimmer & CanSwim,
            LocationName.lava_lagoon_banana_coin_10:
                HasGlimmer & CanSwim,


            
            LocationName.red_hot_ride_kong:
                CanCarry | HasBothKongs,
            LocationName.red_hot_ride_dk_coin:
                HasBothKongs | (CanCarry & CanCartwheel),
            LocationName.red_hot_ride_bonus_1:
                CanCarry | HasRambi,
            LocationName.red_hot_ride_banana_bunch_1:
                True_(),
            LocationName.red_hot_ride_banana_coin_1:
                True_(),
            LocationName.red_hot_ride_banana_coin_2:
                True_(),
            LocationName.red_hot_ride_banana_bunch_2:
                True_(),
            LocationName.red_hot_ride_banana_coin_3:
                True_(),
            LocationName.red_hot_ride_banana_bunch_3:
                True_(),
            LocationName.red_hot_ride_banana_coin_4:
                True_(),
            LocationName.red_hot_ride_banana_coin_5:
                HasRambi,
            LocationName.red_hot_ride_banana_coin_6:
                True_(),
            LocationName.red_hot_ride_banana_bunch_4:
                True_(),


            LocationName.squawks_shaft_clear:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_kong:
                CanUseKannons & CanCarry & HasSquawks,
            LocationName.squawks_shaft_dk_coin:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_bonus_1:
                CanUseKannons & CanCarry,
            LocationName.squawks_shaft_bonus_2:
                CanUseKannons & (
                    CanTeamAttack |  (
                        CanCartwheel | CanHover
                    )
                ),
            LocationName.squawks_shaft_bonus_3:
                CanUseKannons & HasSquawks,
            LocationName.squawks_shaft_banana_coin_1:
                True_(),
            LocationName.squawks_shaft_banana_bunch_1:
                CanTeamAttack | CanUseKannons,
            LocationName.squawks_shaft_banana_coin_2:
                CanCarry & CanUseKannons,
            LocationName.squawks_shaft_banana_bunch_2:
                CanUseKannons,
            LocationName.squawks_shaft_red_balloon_1:
                CanCarry & CanUseKannons,
            LocationName.squawks_shaft_banana_coin_3:
                CanUseKannons,
            LocationName.squawks_shaft_banana_coin_4:
                CanUseKannons,
            LocationName.squawks_shaft_banana_coin_5:
                HasSquawks & CanUseKannons,
            LocationName.squawks_shaft_banana_coin_6:
                HasSquawks & CanUseKannons,
            LocationName.squawks_shaft_banana_coin_7:
                HasSquawks & CanUseKannons,
            LocationName.squawks_shaft_banana_bunch_3:
                HasSquawks & CanUseKannons,
            LocationName.squawks_shaft_banana_bunch_4:
                HasSquawks & CanUseKannons,


            LocationName.kleevers_kiln_clear:
                CanCling & CanCarry,
            LocationName.kleever_defeated:
                CanCling & CanCarry,
            LocationName.kleevers_kiln_banana_coin_1:
                CanCling & CanHover & CanCarry,
            LocationName.kleevers_kiln_banana_coin_2:
                CanCling & CanHover & CanCarry,


            LocationName.barrel_bayou_clear:
                (CanUseControllableBarrels | (CanHover & CanCartwheel & HasRambi)) 
                    & (CanUseKannons | (CanHover & CanTeamAttack)
                ),
            LocationName.barrel_bayou_kong:
                CanUseControllableBarrels & CanUseKannons & (
                    CanTeamAttack | CanCartwheel
                ),
            LocationName.barrel_bayou_dk_coin:
                HasRambi & CanUseControllableBarrels,
            LocationName.barrel_bayou_bonus_1:
                CanCarry & (
                    CanUseControllableBarrels | (CanHover & CanCartwheel & HasRambi)
                ),
            LocationName.barrel_bayou_bonus_2:
                CanUseControllableBarrels & 
                    (CanUseKannons | (CanHover & CanTeamAttack)
                ),
            LocationName.barrel_bayou_banana_bunch_1:
                CanTeamAttack | HasBothKongs,
            LocationName.barrel_bayou_banana_coin_1:
                CanUseControllableBarrels | 
                    (CanHover & CanCartwheel & HasRambi
                ),
            LocationName.barrel_bayou_banana_bunch_2:
                CanUseControllableBarrels | 
                    (CanHover & CanCartwheel & HasRambi
                ),
            LocationName.barrel_bayou_green_balloon:
                (CanUseControllableBarrels | (CanHover & CanCartwheel & HasRambi))
                    & CanCarry & (
                    CanUseKannons | CanHover
                ),
            LocationName.barrel_bayou_banana_coin_2:
                (CanUseControllableBarrels | (CanHover & CanCartwheel & HasRambi)) 
                    & (CanUseKannons | (CanHover & CanTeamAttack)
                ),
            LocationName.barrel_bayou_banana_bunch_3:
                (CanUseControllableBarrels | (CanHover & CanCartwheel & HasRambi)) 
                    & (CanUseKannons | (CanHover & CanTeamAttack)
                ),


            LocationName.glimmers_galleon_clear:
                CanSwim,
            LocationName.glimmers_galleon_kong:
                CanSwim,
            LocationName.glimmers_galleon_dk_coin:
                CanSwim,
            LocationName.glimmers_galleon_bonus_1:
                CanSwim,
            LocationName.glimmers_galleon_bonus_2:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_1:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_2:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_1:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_2:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_3:
                CanSwim,
            LocationName.glimmers_galleon_red_balloon:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_4:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_3:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_5:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_4:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_6:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_7:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_5:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_8:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_6:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_9:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_10:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_11:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_12:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_7:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_8:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_13:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_9:
                CanSwim,
            LocationName.glimmers_galleon_banana_bunch_14:
                CanSwim,
            LocationName.glimmers_galleon_banana_coin_10:
                CanSwim,
                

            LocationName.krockhead_klamber_clear:
                CanClimb,
            LocationName.krockhead_klamber_kong:
                CanClimb,
            LocationName.krockhead_klamber_dk_coin:
                CanCarry & CanCartwheel & HasBothKongs,
            LocationName.krockhead_klamber_bonus_1:
                CanClimb & 
                CanTeamAttack & 
                HasSquitter,
            LocationName.krockhead_klamber_red_balloon_1:
                HasBothKongs & CanCarry,
            LocationName.krockhead_klamber_banana_coin_1:
                CanCarry & CanCartwheel & HasBothKongs,
            LocationName.krockhead_klamber_banana_coin_2:
                (CanCartwheel & CanHover & HasBothKongs) | CanClimb,
            LocationName.krockhead_klamber_red_balloon_2:
                CanClimb & CanTeamAttack & HasSquitter,
            LocationName.krockhead_klamber_banana_coin_3:
                CanClimb,


            LocationName.rattle_battle_clear:
                HasRattly,
            LocationName.rattle_battle_kong:
                HasRattly,
            LocationName.rattle_battle_dk_coin:
                HasRattly & CanUseKannons,
            LocationName.rattle_battle_bonus_1:
                CanTeamAttack & (CanHover | CanCartwheel),
            LocationName.rattle_battle_bonus_2:
                HasRattly,
            LocationName.rattle_battle_bonus_3:
                HasRattly,
            LocationName.rattle_battle_banana_coin_1:
                True_(),
            LocationName.rattle_battle_banana_bunch_1:
                True_(),
            LocationName.rattle_battle_banana_bunch_2:
                HasRattly,
            LocationName.rattle_battle_banana_coin_2:
                HasRattly,
            LocationName.rattle_battle_banana_coin_3:
                HasRattly,
            LocationName.rattle_battle_banana_bunch_3:
                HasRattly,
            LocationName.rattle_battle_banana_bunch_4:
                HasRattly,


            LocationName.slime_climb_clear:
                CanClimb & CanUseKannons,
            LocationName.slime_climb_kong:
                CanClimb & CanSwim,
            LocationName.slime_climb_dk_coin:
                CanClimb & CanSwim & HasBothKongs,
            LocationName.slime_climb_bonus_1:
                CanClimb,
            LocationName.slime_climb_bonus_2:
                CanClimb & CanCarry,
            LocationName.slime_climb_banana_coin_1:
                True_(),
            LocationName.slime_climb_banana_coin_2:
                CanClimb,
            LocationName.slime_climb_banana_bunch_1:
                CanClimb,
            LocationName.slime_climb_banana_bunch_2:
                CanClimb,
            LocationName.slime_climb_banana_coin_3:
                CanClimb,
            LocationName.slime_climb_banana_bunch_3:
                CanClimb & (HasBothKongs | CanSwim),
            LocationName.slime_climb_banana_bunch_4:
                CanClimb & (HasBothKongs | CanSwim),


            LocationName.bramble_blast_clear:
                CanUseKannons,
            LocationName.bramble_blast_kong:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_dk_coin:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_bonus_1:
                CanUseKannons,
            LocationName.bramble_blast_bonus_2:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_1:
                CanTeamAttack,
            LocationName.bramble_blast_banana_bunch_2:
                HasBothKongs | CanUseKannons,
            LocationName.bramble_blast_banana_bunch_3:
                CanUseKannons,
            LocationName.bramble_blast_banana_coin_1:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_4:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_5:
                CanUseKannons,
            LocationName.bramble_blast_banana_coin_2:
                CanUseKannons,
            LocationName.bramble_blast_red_balloon:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_6:
                CanUseKannons,
            LocationName.bramble_blast_banana_bunch_7:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_8:
                CanUseKannons & HasSquawks,
            LocationName.bramble_blast_banana_bunch_9:
                CanUseKannons & HasSquawks,


            LocationName.kudgels_kontest_clear:
                CanCarry,
            LocationName.kudgel_defeated:
                CanCarry,


            LocationName.hornet_hole_clear:
                CanCling | (CanTeamAttack & HasSquitter),
            LocationName.hornet_hole_kong:
                CanCling | (CanTeamAttack & HasSquitter),
            LocationName.hornet_hole_dk_coin:
                HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack
                    ),
            LocationName.hornet_hole_bonus_1:
                CanCarry & ((CanTeamAttack & CanCling) | (HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack))
                ),
            LocationName.hornet_hole_bonus_2:
                (CanTeamAttack & CanCling) | (HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack)
                    ),
            LocationName.hornet_hole_bonus_3:
                HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack
                    ),
            LocationName.hornet_hole_banana_bunch_1:
                (CanTeamAttack & CanCling) | (HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack)
                    ),
            LocationName.hornet_hole_banana_coin_1:
                (CanTeamAttack & CanCling) | (HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack)
                    ),
            LocationName.hornet_hole_banana_bunch_2:
                (CanTeamAttack & CanCling) | (HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack)
                    ),
            LocationName.hornet_hole_banana_coin_2:
                True_(),
            LocationName.hornet_hole_green_balloon_1:
                CanCarry,
            LocationName.hornet_hole_banana_coin_3:
                True_(),
            LocationName.hornet_hole_banana_bunch_3:
                HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack
                    ),
            LocationName.hornet_hole_banana_coin_4:
                HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack
                    ),
            LocationName.hornet_hole_banana_bunch_4:
                HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack
                    ),
            LocationName.hornet_hole_banana_bunch_5:
                CanTeamAttack | HasBothKongs | (HasSquitter & (
                    (HasBothKongs & CanCling))
                    ),
            LocationName.hornet_hole_red_balloon_1:
                HasSquitter & (
                    (HasBothKongs & CanCling) | CanTeamAttack
                    ),


            LocationName.target_terror_clear:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_kong:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_dk_coin:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_bonus_1:
                CanUseKannons & CanRideSkullKart & HasSquawks,
            LocationName.target_terror_bonus_2:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_banana_bunch_1:
                CanUseKannons & CanRideSkullKart,
            LocationName.target_terror_banana_bunch_2:
                CanUseKannons & CanRideSkullKart & HasSquawks,
            LocationName.target_terror_red_balloon:
                CanUseKannons & CanRideSkullKart,


            LocationName.bramble_scramble_clear:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_kong:
                CanClimb & HasSquawks & CanUseKannons,
            LocationName.bramble_scramble_dk_coin:
                CanClimb & HasSquawks & (
                    HasBothKongs | (CanCartwheel & HasSquitter)
                ),
            LocationName.bramble_scramble_bonus_1:
                CanClimb & HasSquawks & ((
                    CanTeamAttack & CanBeInvincible
                    ) | (
                    CanHover & CanUseKannons & HasBothKongs
                    )
                ),
            LocationName.bramble_scramble_banana_bunch_1:
                True_(),
            LocationName.bramble_scramble_banana_bunch_2:
                HasBothKongs,
            LocationName.bramble_scramble_banana_coin_1:
                CanClimb & CanUseKannons & ((
                    CanTeamAttack & CanBeInvincible
                    ) | (
                    (CanHover | CanCartwheel) & HasBothKongs
                    )
                ),
            LocationName.bramble_scramble_banana_coin_2:
                CanClimb & HasSquawks & ((
                    CanTeamAttack & CanBeInvincible
                    ) | (
                    (CanHover | CanCartwheel) & CanUseKannons & HasBothKongs
                    )
                ),
            LocationName.bramble_scramble_banana_coin_3:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_3:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_4:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_4:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_5:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_bunch_5:
                CanClimb & HasSquawks,
            LocationName.bramble_scramble_banana_coin_6:
                CanClimb & HasSquawks & (
                    HasBothKongs | (CanCartwheel & HasSquitter)
                ),
            LocationName.bramble_scramble_banana_coin_7:
                CanClimb & HasSquawks & (
                    HasBothKongs | (CanCartwheel & HasSquitter)
                ),
            LocationName.bramble_scramble_banana_coin_8:
                CanClimb & HasSquawks & (
                    HasBothKongs | (CanCartwheel & HasSquitter)
                ),
            LocationName.bramble_scramble_blue_balloon:
                CanClimb & HasSquawks & (
                    HasBothKongs | (CanCartwheel & HasSquitter)
                ),
            LocationName.bramble_scramble_red_balloon:
                CanClimb & HasSquawks & (
                    HasBothKongs | (CanCartwheel & HasSquitter)
                ),


            LocationName.rickety_race_clear:
                CanRideSkullKart,
            LocationName.rickety_race_kong:
                CanRideSkullKart,
            LocationName.rickety_race_dk_coin:
                CanRideSkullKart,
            LocationName.rickety_race_bonus_1:
                CanRideSkullKart & 
                    CanTeamAttack 
                    & CanHover,
            LocationName.rickety_race_banana_coin:
                CanRideSkullKart,


            LocationName.mudhole_marsh_clear:
                (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack
                        & HasBothKongs & CanCartwheel
                ),
            LocationName.mudhole_marsh_kong:
                CanCarry & (
                    (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack
                        & HasBothKongs & CanCartwheel)
                ),
            LocationName.mudhole_marsh_dk_coin:
                (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack
                        & HasBothKongs & CanCartwheel
                ),
            LocationName.mudhole_marsh_bonus_1:
                CanTeamAttack & ((CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & HasBothKongs & CanCartwheel)
                ),
            LocationName.mudhole_marsh_bonus_2:
                CanCarry & (
                    (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack
                        & HasBothKongs & CanCartwheel)
                ),
            LocationName.mudhole_marsh_banana_coin_1:
                True_(),
            LocationName.mudhole_marsh_banana_bunch_1:
                CanCarry & (
                    (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack & HasBothKongs)
                ),
            LocationName.mudhole_marsh_banana_coin_2:
                CanCarry & (
                    (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack
                        & HasBothKongs & CanCartwheel)
                ),
            LocationName.mudhole_marsh_banana_coin_3:
                 (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack 
                        & HasBothKongs & CanCartwheel
                ),
            LocationName.mudhole_marsh_banana_coin_4:
                (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack 
                        & HasBothKongs & CanCartwheel
                ),
            LocationName.mudhole_marsh_banana_coin_5:
                (CanCling & 
                    (CanClimb | CanHover))
                    | (CanHover & CanTeamAttack 
                        & HasBothKongs & CanCartwheel
                ),


            LocationName.rambi_rumble_clear:
                (CanCling | (CanCartwheel & CanCartwheel))  & CanUseKannons & HasRambi,
            LocationName.rambi_rumble_kong:
                (CanCling | (CanCartwheel & CanCartwheel)) & CanUseKannons & HasRambi & ( 
                    CanCartwheel | CanTeamAttack),
            LocationName.rambi_rumble_dk_coin:
                CanUseKannons & (CanCling | CanTeamAttack),
            LocationName.rambi_rumble_bonus_1:
                CanCling & CanUseKannons,
            LocationName.rambi_rumble_bonus_2:
                (CanCling | (CanCartwheel & CanCartwheel)) & CanUseKannons & HasRambi,
            LocationName.rambi_rumble_banana_coin_1:
                True_(),
            LocationName.rambi_rumble_banana_bunch_1:
                True_(),
            LocationName.rambi_rumble_banana_bunch_2:
                (CanCartwheel & CanCartwheel) | (CanCling & CanUseKannons),
            LocationName.rambi_rumble_banana_coin_2:
                CanUseKannons & (
                        CanCling | (CanCartwheel & CanCartwheel & CanHover)
                    ),
            LocationName.rambi_rumble_banana_bunch_3:
                (CanCling | (CanCartwheel & CanCartwheel)) & CanUseKannons & HasRambi,


            LocationName.king_zing_sting_clear:
                HasSquawks,
            LocationName.king_zing_defeated:
                HasSquawks,
            LocationName.king_zing_sting_banana_coin_1:
                True_(),
            LocationName.king_zing_sting_banana_coin_2:
                True_(),


             LocationName.ghostly_grove_clear:
                CanClimb,
            LocationName.ghostly_grove_kong:
                CanClimb & CanCarry,
            LocationName.ghostly_grove_dk_coin:
                 (CanClimb & (
                    (CanCartwheel & CanCartwheel) | CanHover)
                    ) | ((CanTeamAttack | HasBothKongs) & CanHover
                ),
            LocationName.ghostly_grove_bonus_1:
            CanCarry & 
                    (CanClimb | ((CanTeamAttack | HasBothKongs) & CanHover)
                ),
            LocationName.ghostly_grove_bonus_2:
                CanClimb,
            LocationName.ghostly_grove_banana_bunch_1:
                True_(),
            LocationName.ghostly_grove_red_balloon:
                CanCarry,
            LocationName.ghostly_grove_banana_bunch_2:
                True_(),
            LocationName.ghostly_grove_banana_coin_1:
                (CanClimb | (
                    (CanTeamAttack | HasBothKongs) & CanHover)
                ),
            LocationName.ghostly_grove_banana_bunch_3:
                CanClimb,
            LocationName.ghostly_grove_banana_bunch_4:
                CanClimb | (
                    CanTeamAttack & CanHover
                ),
            LocationName.ghostly_grove_banana_coin_2:
                CanClimb,


            LocationName.haunted_hall_clear:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_kong:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_dk_coin:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_bonus_1:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_bonus_2:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_bonus_3:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_banana_bunch_1:
                True_(),
            LocationName.haunted_hall_banana_bunch_2:
                True_(),
            LocationName.haunted_hall_banana_coin_1:
                True_(),
            LocationName.haunted_hall_banana_coin_2:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),
            LocationName.haunted_hall_banana_coin_3:
                CanRideSkullKart & (
                    CanCartwheel | (HasDixie 
                        & (CanHover | CanCartwheel)
                        )),


            LocationName.gusty_glade_clear:
                CanCling & CanUseKannons,
            LocationName.gusty_glade_kong:
                CanCling & CanUseKannons & CanCarry  &
                    CanCartwheel,
            LocationName.gusty_glade_dk_coin:
                CanCling & CanUseKannons,
            LocationName.gusty_glade_bonus_1:
                CanTeamAttack & (CanCling | HasRattly),
            LocationName.gusty_glade_bonus_2:
                CanCling & CanCarry & CanUseKannons,
            LocationName.gusty_glade_banana_coin_1:
                CanTeamAttack,
            LocationName.gusty_glade_banana_coin_2:
                True_(),
            LocationName.gusty_glade_blue_balloon:
                CanTeamAttack & HasRattly,
            LocationName.gusty_glade_banana_coin_3:
                CanCling & CanUseKannons,


            LocationName.parrot_chute_panic_clear:
                (HasBothKongs & CanHover & CanCarry) | HasSquawks,
            LocationName.parrot_chute_panic_kong:
                (HasBothKongs & CanHover & CanCarry) | HasSquawks,
            LocationName.parrot_chute_panic_dk_coin:
                CanHover | CanCartwheel,
            LocationName.parrot_chute_panic_bonus_1:
                HasSquawks | (
                    CanTeamAttack & CanHover),
            LocationName.parrot_chute_panic_bonus_2:
                HasSquawks & (
                    CanCartwheel | 
                    CanHover |
                    HasBothKongs
                ),
            LocationName.parrot_chute_panic_banana_coin_1:
                CanCarry | CanTeamAttack,
            LocationName.parrot_chute_panic_banana_coin_2:
                (HasBothKongs & CanHover) | HasSquawks,
            LocationName.parrot_chute_panic_banana_bunch_1:
                (HasBothKongs & CanHover) | HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_3:
                (HasBothKongs & CanHover & CanCarry) | HasSquawks,
            LocationName.parrot_chute_panic_banana_bunch_2:
                (HasBothKongs & CanHover & CanCarry) | HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_4:
                (HasBothKongs & CanHover & CanCarry) | HasSquawks,
            LocationName.parrot_chute_panic_banana_coin_5:
                ((HasBothKongs & CanHover & CanCarry) | HasSquawks) 
                & CanUseControllableBarrels
                    & (CanTeamAttack | CanCartwheel),


            LocationName.web_woods_clear:
                HasSquitter,
            LocationName.web_woods_kong:
                HasSquitter & (
                    CanTeamAttack | (CanHover | (
                        CanCartwheel & CanCartwheel)
                    )),
            LocationName.web_woods_dk_coin:
                HasSquitter,
            LocationName.web_woods_bonus_1:
                HasSquitter,
            LocationName.web_woods_bonus_2:
                HasSquitter,
            LocationName.web_woods_banana_coin_1:
                CanTeamAttack | 
                    (CanCartwheel & CanCartwheel) |
                    (HasDixie & CanHover),
            LocationName.web_woods_banana_coin_2:
                CanCarry & 
                    (CanTeamAttack | 
                    (CanCartwheel & CanCartwheel) |
                    (HasDixie & CanHover)
                ),
            LocationName.web_woods_green_balloon_1:
                CanCarry & (CanTeamAttack | CanUseKannons),
            LocationName.web_woods_banana_bunch_1:
                True_(),
            LocationName.web_woods_banana_bunch_2:
                True_(),
            LocationName.web_woods_banana_bunch_3:
                HasSquitter,
            LocationName.web_woods_banana_coin_3:
                HasSquitter,
            LocationName.web_woods_banana_coin_4:
                HasSquitter,
            LocationName.web_woods_banana_coin_5:
                HasSquitter,
            LocationName.web_woods_green_balloon_2:
                HasSquitter & CanTeamAttack,


            LocationName.kreepy_krow_clear:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry,
            LocationName.kreepy_krow_defeated:
                CanUseKannons & CanClimb & CanCling & 
                    CanCarry,
            LocationName.kreepy_krow_banana_coin_1:
                CanCling & CanClimb & CanUseKannons & CanCarry,
            LocationName.kreepy_krow_banana_coin_2:
                CanCling & CanClimb & CanUseKannons & CanCarry,


            LocationName.arctic_abyss_clear:
                CanSwim | (
                    HasEnguarde & (
                        (CanCartwheel & CanCartwheel) | CanHover
                    )
                ),
            LocationName.arctic_abyss_kong:
                (
                    (CanSwim | HasEnguarde)  &
                    ( (CanCartwheel & CanCartwheel) | CanHover)
                ),
            LocationName.arctic_abyss_dk_coin:
                CanSwim | (
                    HasEnguarde & (
                         (CanCartwheel & CanCartwheel) | CanHover
                    )
                ),
            LocationName.arctic_abyss_bonus_1:
                HasEnguarde & ( 
                    CanSwim | (
                         (CanCartwheel & CanCartwheel) | CanHover
                    )
                ),
            LocationName.arctic_abyss_bonus_2:
                
                CanCarry & (
                    CanSwim | (
                        HasEnguarde & (
                             (CanCartwheel & CanCartwheel) | CanHover
                        )
                    )
                ),
            LocationName.arctic_abyss_banana_coin_1:
                (CanCartwheel & CanCartwheel) | 
                    (HasDixie & CanHover),
            LocationName.arctic_abyss_banana_bunch_1:
                (CanCartwheel & CanCartwheel) | 
                    (HasDixie & CanHover),
            LocationName.arctic_abyss_banana_bunch_2:
                (CanCartwheel & CanCartwheel) | 
                    (HasDixie & CanHover),
            LocationName.arctic_abyss_banana_bunch_3:
                (CanCartwheel & CanCartwheel) | 
                    (HasDixie & CanHover),
            LocationName.arctic_abyss_banana_bunch_4:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_coin_2:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_coin_3:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_coin_4:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_bunch_5:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_coin_5:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_bunch_6:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_banana_bunch_7:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),
            LocationName.arctic_abyss_red_balloon_1:
                HasEnguarde & 
                    (CanSwim | (
                        (CanCartwheel & CanCartwheel) | 
                            (HasDixie & CanHover)
                        )
                    ),
            LocationName.arctic_abyss_red_balloon_2:
                CanSwim | 
                    (HasEnguarde & 
                        ((CanCartwheel & CanCartwheel) | 
                        (HasDixie & CanHover))
                    ),


            LocationName.windy_well_clear:
                CanCling,
            LocationName.windy_well_kong:
                CanUseKannons & CanCling,
            LocationName.windy_well_dk_coin:
                CanCling,
            LocationName.windy_well_bonus_1:
                CanCling,
            LocationName.windy_well_bonus_2:
                CanCarry & CanCling & HasSquawks,
            LocationName.windy_well_banana_coin_1:
                True_(),
            LocationName.windy_well_banana_coin_2:
                CanCling,
            LocationName.windy_well_banana_coin_3:
                CanCling,
            LocationName.windy_well_banana_bunch_1:
                CanCling & 
                    (CanUseKannons | CanTeamAttack),
            LocationName.windy_well_banana_bunch_2:
                CanCling & 
                    (CanUseKannons | CanTeamAttack),
            LocationName.windy_well_banana_coin_4:
                CanCling,
            LocationName.windy_well_banana_bunch_3:
                CanCling,
            LocationName.windy_well_red_balloon:
                CanCling,
            LocationName.windy_well_banana_bunch_4:
                CanCling & HasSquawks & CanCarry,


            LocationName.castle_crush_clear:
                (CanHover | CanCartwheel) | HasBothKongs,
            LocationName.castle_crush_kong:
                CanHover | (CanCartwheel | HasBothKongs),
            LocationName.castle_crush_dk_coin:
                HasSquawks & (CanHover | (CanCartwheel | HasBothKongs)),
            LocationName.castle_crush_bonus_1:
                HasRambi & (HasBothKongs | CanTeamAttack),
            LocationName.castle_crush_bonus_2:
                CanCarry & HasSquawks & (
                    HasBothKongs | 
                    (CanHover | CanCartwheel)
                ),
            LocationName.castle_crush_banana_coin_1:
                True_(),
            LocationName.castle_crush_banana_bunch_1:
                True_(),
            LocationName.castle_crush_banana_bunch_2:
                True_(),
            LocationName.castle_crush_banana_coin_2:
                True_(),
            LocationName.castle_crush_banana_bunch_3:
                HasRambi & HasBothKongs &  CanCarry,
            LocationName.castle_crush_banana_bunch_4:
                True_(),
            LocationName.castle_crush_banana_bunch_5:
                HasBothKongs | 
                    (CanHover | CanCartwheel),
            LocationName.castle_crush_banana_coin_3:
                CanCarry & (
                    HasBothKongs | 
                        (CanHover | CanCartwheel)
                    ),
            LocationName.castle_crush_banana_bunch_6:
                CanCarry & (
                    HasBothKongs | 
                        (CanHover | CanCartwheel)
                    ),


            LocationName.clappers_cavern_clear:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim & HasBothKongs)) & ((
                    CanCling & 
                        (HasEnguarde | CanSwim)
                    ) | (
                        CanSwim & CanBeInvincible
                    )
                ),
            LocationName.clappers_cavern_kong:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim & HasBothKongs)) & ((
                    CanCling & 
                        (HasEnguarde | CanSwim)
                    ) | (
                        CanSwim & CanBeInvincible & CanTeamAttack
                    )
                ),
            LocationName.clappers_cavern_dk_coin:
                CanTeamAttack & 
                    (CanCling | HasGlimmer | (CanHover & CanSwim)),
            LocationName.clappers_cavern_bonus_1:
                CanCling & CanTeamAttack,
            LocationName.clappers_cavern_bonus_2:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & HasEnguarde,
            LocationName.clappers_cavern_banana_coin_1:
                HasGlimmer | (CanHover & CanSwim),
            LocationName.clappers_cavern_banana_bunch_1:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & 
                    (CanSwim | HasEnguarde),
            LocationName.clappers_cavern_banana_bunch_2:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & 
                    (CanSwim | HasEnguarde),
            LocationName.clappers_cavern_banana_bunch_3:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & 
                    (CanSwim | HasEnguarde),
            LocationName.clappers_cavern_banana_coin_2:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & 
                    (CanSwim | HasEnguarde),
            LocationName.clappers_cavern_banana_bunch_4:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & HasEnguarde,
            LocationName.clappers_cavern_banana_coin_3:
                CanUseKannons & (HasGlimmer | (CanHover & CanSwim)) & 
                    (CanSwim | HasEnguarde) & (
                        (CanTeamAttack & CanBeInvincible) | HasBothKongs),
            LocationName.clappers_cavern_banana_coin_4:
                CanUseKannons & HasGlimmer & 
                    (CanSwim | HasEnguarde) & (
                        (CanTeamAttack & CanBeInvincible) | HasBothKongs),
            LocationName.clappers_cavern_banana_coin_5:
                CanUseKannons & HasGlimmer & 
                    (CanSwim | HasEnguarde) & (
                        (CanTeamAttack & CanBeInvincible) | HasBothKongs),


            LocationName.chain_link_chamber_clear:
                CanClimb & (
                    CanCling | (CanUseKannons & CanUseControllableBarrels)
                ),
            LocationName.chain_link_chamber_kong:
                CanClimb & (
                    CanCling | (CanUseKannons & CanUseControllableBarrels)
                ),
            LocationName.chain_link_chamber_dk_coin:
                CanClimb & (
                    CanCling | (CanUseKannons & CanUseControllableBarrels)
                ),
            LocationName.chain_link_chamber_bonus_1:
                CanClimb & CanCling & CanCarry,
            LocationName.chain_link_chamber_bonus_2:
                CanClimb & 
                CanUseControllableBarrels & (
                    CanCling | CanUseKannons
                ) & (
                    CanCartwheel | CanTeamAttack | HasBothKongs
                ),
            LocationName.chain_link_chamber_banana_coin_1:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_1:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_2:
                CanClimb,
            LocationName.chain_link_chamber_banana_bunch_3:
                CanClimb & CanCarry,
            LocationName.chain_link_chamber_banana_coin_2:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            LocationName.chain_link_chamber_banana_bunch_4:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            LocationName.chain_link_chamber_banana_coin_3:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),
            LocationName.chain_link_chamber_banana_coin_4:
                CanClimb & 
                    (CanCling | (CanUseKannons & 
                    CanUseControllableBarrels)),


            LocationName.toxic_tower_clear:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_kong:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_dk_coin:
                HasRattly,
            LocationName.toxic_tower_bonus_1:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_bunch_1:
                HasRattly | CanTeamAttack,
            LocationName.toxic_tower_banana_bunch_2:
                HasRattly | CanTeamAttack,
            LocationName.toxic_tower_banana_bunch_3:
                HasRattly | CanTeamAttack,
            LocationName.toxic_tower_banana_bunch_4:
                HasRattly | CanTeamAttack,
            LocationName.toxic_tower_banana_bunch_5:
                HasRattly | CanTeamAttack,
            LocationName.toxic_tower_banana_bunch_6:
                HasRattly | CanTeamAttack,
            LocationName.toxic_tower_banana_bunch_7:
                HasRattly,
            LocationName.toxic_tower_banana_coin_1:
                HasRattly,
            LocationName.toxic_tower_banana_coin_2:
                HasRattly,
            LocationName.toxic_tower_banana_coin_3:
                HasRattly,
            LocationName.toxic_tower_banana_coin_4:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_coin_5:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_bunch_8:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_banana_bunch_9:
                HasRattly & HasSquawks,
            LocationName.toxic_tower_green_balloon:
                HasRattly & HasSquawks & (CanCartwheel | CanClimb),


            LocationName.stronghold_showdown_banana_coin_1:
                CanTeamAttack,
            LocationName.stronghold_showdown_red_balloon:
                CanTeamAttack,
            LocationName.stronghold_showdown_banana_coin_2:
                CanTeamAttack,


            LocationName.screechs_sprint_clear:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | HasBothKongs
                ),
            LocationName.screechs_sprint_kong:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | HasBothKongs
                ),
            LocationName.screechs_sprint_dk_coin:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | HasBothKongs
                ),
            LocationName.screechs_sprint_bonus_1:
                CanClimb & CanTeamAttack & CanCartwheel & CanCarry,
            LocationName.screechs_sprint_banana_coin_1:
                True_(),
            LocationName.screechs_sprint_banana_bunch_1:
                CanCarry,
            LocationName.screechs_sprint_banana_coin_2:
                CanClimb,
            LocationName.screechs_sprint_banana_coin_3:
                CanClimb & (
                    ((HasSquawks | HasBothKongs) & (
                    CanHover | CanCartwheel)
                    ) | CanTeamAttack
                ),
            LocationName.screechs_sprint_red_balloon:
                CanClimb & (
                    ((HasSquawks | HasBothKongs) & (
                    CanHover | CanCartwheel)
                    ) | CanTeamAttack
                ),
            LocationName.screechs_sprint_banana_bunch_2:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_bunch_3:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_coin_4:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_coin_5:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_coin_6:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_coin_7:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_coin_8:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_bunch_4:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_bunch_5:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),
            LocationName.screechs_sprint_banana_bunch_6:
                CanClimb & HasSquawks & (
                    CanTeamAttack | CanCartwheel | CanHover | HasBothKongs
                ),


            LocationName.k_rool_duel_clear:
                CanCarry,


            LocationName.jungle_jinx_clear:
                CanUseKannons | CanHover, 
            
            LocationName.jungle_jinx_kong:
                (CanHover | (CanCartwheel & CanUseKannons)) & (
                    CanCarry | HasBothKongs 
                ), 
            LocationName.jungle_jinx_dk_coin:
                CanTeamAttack  & (
                    CanCartwheel | CanHover
                ), 
            LocationName.jungle_jinx_banana_bunch_1:
                True_(),
            LocationName.jungle_jinx_banana_bunch_2:
                True_(),
            LocationName.jungle_jinx_banana_coin_1:
                True_(),
            LocationName.jungle_jinx_banana_coin_2:
                True_(),
            LocationName.jungle_jinx_banana_coin_3:
                CanHover | CanUseKannons,
            LocationName.jungle_jinx_banana_coin_4:
                CanHover | CanUseKannons,
            LocationName.jungle_jinx_banana_coin_5:
                CanHover | CanUseKannons,

            LocationName.black_ice_battle_clear:
                True_(),
            LocationName.black_ice_battle_kong:
                CanCarry | HasBothKongs,
            LocationName.black_ice_battle_dk_coin:
                CanCarry | HasBothKongs,
            LocationName.black_ice_battle_banana_bunch_1:
                CanHover | HasBothKongs | CanCarry | CanCartwheel,
            LocationName.black_ice_battle_red_balloon_1:
                True_(),
            LocationName.black_ice_battle_red_balloon_2:
                True_(),
            LocationName.black_ice_battle_red_balloon_3:
                CanCarry,
            LocationName.black_ice_battle_banana_bunch_2:
                True_(),
            LocationName.black_ice_battle_banana_coin_1:
                True_(),
            LocationName.black_ice_battle_banana_bunch_3:
                CanCarry | HasBothKongs,


            LocationName.klobber_karnage_clear:
                CanUseDiddyBarrels & 
                    CanUseDixieBarrels  &
                    CanUseControllableBarrels  &
                    CanUseKannons & (
                        CanCarry | CanTeamAttack
                    ),
            LocationName.klobber_karnage_kong:
                CanUseDiddyBarrels & 
                    CanUseDixieBarrels  &
                    CanUseControllableBarrels  &
                    CanUseKannons & (
                        CanCarry | CanTeamAttack
                    ),
            LocationName.klobber_karnage_dk_coin:
                CanBeInvincible  &
                    CanUseDiddyBarrels & 
                    CanUseDixieBarrels  &
                    CanUseControllableBarrels  &
                    CanUseKannons & (
                        CanCarry | CanTeamAttack
                    ),
            LocationName.klobber_karnage_banana_coin_1:
                True_(),
            LocationName.klobber_karnage_banana_bunch_1:
                True_(),
            LocationName.klobber_karnage_banana_bunch_2:
                True_(),
            LocationName.klobber_karnage_banana_coin_2:
                True_(),
            LocationName.klobber_karnage_banana_bunch_3:
                True_(),
            LocationName.klobber_karnage_banana_coin_3:
                (CanCartwheel & (CanUseDixieBarrels & CanUseDiddyBarrels))
                               | (CanTeamAttack & CanUseControllableBarrels
                ),
            LocationName.klobber_karnage_banana_bunch_4:
                CanUseControllableBarrels,
            LocationName.klobber_karnage_banana_bunch_5:
                CanUseControllableBarrels & 
                    (HasBothKongs | (CanUseDixieBarrels & CanUseDiddyBarrels)
                ),
            LocationName.klobber_karnage_banana_bunch_6:
                CanUseControllableBarrels & 
                    (HasBothKongs | (CanUseDixieBarrels & CanUseDiddyBarrels)
                ),
            LocationName.klobber_karnage_banana_bunch_7:
                CanUseControllableBarrels & 
                    (HasBothKongs | (CanUseDixieBarrels & CanUseDiddyBarrels)
                ),
            LocationName.klobber_karnage_banana_coin_4:
                CanUseControllableBarrels & 
                    (HasBothKongs | (CanUseDixieBarrels & CanUseDiddyBarrels)
                ),
            LocationName.klobber_karnage_red_balloon:
                CanUseControllableBarrels & (CanCartwheel | CanHover)  &
                    (HasBothKongs | (CanUseDixieBarrels & CanUseDiddyBarrels)
                ),


            LocationName.fiery_furnace_clear:
                (
                    CanUseControllableBarrels & (
                        CanCartwheel |
                        HasBothKongs
                    )
                ),
            LocationName.fiery_furnace_kong:
                (
                    CanUseControllableBarrels & (
                        CanCartwheel |
                        HasBothKongs
                    )
                ),
            LocationName.fiery_furnace_dk_coin:
                (
                    CanUseControllableBarrels & (
                        CanCartwheel |
                        HasBothKongs
                    )
                ),
            LocationName.fiery_furnace_banana_bunch_1:
                CanTeamAttack | (CanCartwheel & CanHover),
            LocationName.fiery_furnace_banana_bunch_2:
                CanTeamAttack | (CanCartwheel & CanHover),
            LocationName.fiery_furnace_banana_bunch_3:
                CanTeamAttack | (CanCartwheel & CanHover),
            LocationName.fiery_furnace_banana_bunch_4:
                CanCartwheel | CanHover | CanUseControllableBarrels,
            LocationName.fiery_furnace_banana_coin_1:
                CanUseControllableBarrels,
            LocationName.fiery_furnace_banana_coin_2:
                CanUseControllableBarrels,
            LocationName.fiery_furnace_banana_bunch_5:
                CanUseControllableBarrels & (CanCartwheel | CanHover),


            LocationName.animal_antics_clear:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_kong:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_dk_coin:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_bunch_1:
                CanSwim & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_bunch_2:
                CanSwim & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_coin_1:
                CanSwim & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_coin_2:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_bunch_3:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_bunch_4:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_coin_3:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_coin_4:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_red_balloon:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),
            LocationName.animal_antics_banana_coin_5:
                CanSwim & CanUseKannons & HasEnguarde & (
                        HasRambi | (
                            CanHover & CanTeamAttack
                        )
                    ),


            LocationName.krocodile_core_clear:
                CanCarry,
        }

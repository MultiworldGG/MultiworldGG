from dataclasses import dataclass
from typing import TYPE_CHECKING, override
if TYPE_CHECKING:
    from . import DKC3World

from .enums import Items, Locations, Events, Regions
from .constants import *
from . import options

from BaseClasses import CollectionState, Entrance, Location
from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAnyCount, HasAll, Rule, True_, CanReachRegion, CanReachLocation, WrapperRule
from rule_builder.field_resolvers import FromOption, FromWorldAttr

@dataclass()
class Macro(WrapperRule["DKC3World"], game=GAME_NAME):
    name: str
    description: str = ""

    @override
    def _instantiate(self, world: "DKC3World") -> Rule.Resolved:
        if rule := world.rule_macros.get(self.name):
            return rule
        rule = self.Resolved(
            self.child.resolve(world),
            self.name,
            self.description,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )
        world.rule_macros[self.name] = rule
        return rule

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str
        description: str = ""

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            return [{"type": "color", "color": "green" if self(state) else "salmon", "text": str(self)}]

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            suffix = ""
            if state is not None:
                suffix = " ✓" if self(state) else " ✕"
            return f"{self.name}{suffix}"

        @override
        def __str__(self) -> str:
            return self.name
      
HasDixie: Rule = Has(Items.dixie)
HasKiddy: Rule = Has(Items.kiddy)
CanClimb: Rule = Has(Items.climb)
CanCarry: Rule = Has(Items.carry)
CanSpin: Rule = Has(Items.spin)
CanSwim: Rule = Has(Items.swim)
HasEllie: Rule = Has(Items.ellie)
HasEnguarde: Rule = Has(Items.enguarde)
HasSquawks: Rule = Has(Items.squawks)
HasSquitter: Rule = Has(Items.squitter)
HasParry: Rule = Has(Items.parry)
HasBarrelCannon: Rule = Has(Items.barrel_cannon)
HasBarrelRocket: Rule = Has(Items.barrel_rocket)
HasBarrelGhost: Rule = Has(Items.barrel_ghost)
HasBarrelTracker: Rule = Has(Items.barrel_tracker)
HasBarrelWarp: Rule = Has(Items.barrel_warp)
HasBarrelInvincible: Rule = Has(Items.barrel_invincible)
HasBarrelSwitch: Rule = Has(Items.barrel_switch)
HasBarrelShield: Rule = Has(Items.barrel_shield)
HasBarrelWaterfall: Rule = Has(Items.barrel_waterfall)

HasBothKongs = Macro(
    HasAll(Items.dixie, Items.kiddy),
    "Has both kongs",
    "Can use Dixie and Kiddy",
)

CanTeamAttack = Macro(
    HasBothKongs & Has(Items.team_attack),
    "Can use team attack",
    "Can perform a team attack with both kongs"
)

CanHover = Macro(
    HasAll(Items.helicopter_spin, Items.dixie),
    "Can hover",
    "Can hover with Dixie",
)

CanWaterBounce = Macro(
    HasAll(Items.water_bounce, Items.kiddy, Items.spin),
    "Can water bounce",
    "Can bounce in water with Kiddy"
)

HasHovercraft = Macro(
    Has(Items.vehicle, 1),
    "Has hovercraft",
    "Can rent hovercraft from Funky's Rentals",
)  
HasTurboSki = Macro(
    Has(Items.vehicle, 2),
    "Has turbo ski",
    "Can rent turbo ski from Funky's Rentals",
)  
HasGyrocopter = Macro(
    Has(Items.vehicle, 3),
    "Has gyrocopter",
    "Can rent gyrocopter from Funky's Rentals",
)

CanOpenKnautilus = Macro(
    Has(Items.cog, 5),
    "Can open Knautilus",
    "Can give cogs to Boomer to reveal Knautilus",
)

class DKC3Rules:
    player: int
    world: "DKC3World"
    connection_rules: dict[str, Rule]
    region_rules: dict[str, Rule]
    location_rules: dict[str, Rule]

    def __init__(self, world: "DKC3World") -> None:
        self.player = world.player
        self.world = world

        self.connection_rules = {
            # Vehicle rules
            f"{Regions.northern_kremisphere_south} -> {Regions.northern_kremisphere_center}":
                HasHovercraft,
            f"{Regions.northern_kremisphere_center} -> {Regions.northern_kremisphere_north}":
                HasTurboSki,
            f"{Regions.northern_kremisphere_north} -> {Regions.northern_kremisphere_kore}":
                True_(),
            f"{Regions.northern_kremisphere_south} -> {Regions.northern_kremisphere_flying}":
                HasGyrocopter,
            f"{Regions.northern_kremisphere_flying} -> {Regions.northern_kremisphere_kore}":
                True_(),

            # World access
            f"{Regions.northern_kremisphere_south} -> {Regions.lake_orangatanga}":
                Has(Items.lake_orangatanga),
            f"{Regions.northern_kremisphere_south} -> {Regions.kremwood_forest}":
                Has(Items.kremwood_forest),
            f"{Regions.northern_kremisphere_center} -> {Regions.cotton_top_cove}":
                Has(Items.cotton_top_cove),
            f"{Regions.northern_kremisphere_center} -> {Regions.mekanos}":
                Has(Items.mekanos),
            f"{Regions.northern_kremisphere_north} -> {Regions.k3}":
                Has(Items.k3),
            f"{Regions.northern_kremisphere_north} -> {Regions.razor_ridge}":
                Has(Items.razor_ridge),
            f"{Regions.northern_kremisphere_kore} -> {Regions.kaos_kore}":
                Has(Items.banana_bird, count=FromOption(options.RequiredBirds), options=[OptionFilter(options.RequiredBirds, 0, operator="ne")]) | 
                Has(Items.kaos_kore, options=[OptionFilter(options.RequiredBirds, 0)]),
            f"{Regions.northern_kremisphere_center} -> {Regions.krematoa}":
                Has(Items.krematoa),

            # Boss entrances
            f"{Regions.lake_orangatanga} -> {Regions.belchas_barn_map}":
                Has(Events.lake_level, count=FromOption(options.RequiredLakeLevels)),
            f"{Regions.kremwood_forest} -> {Regions.arichs_ambush_map}":
                Has(Events.forest_level, count=FromOption(options.RequiredForestLevels)),
            f"{Regions.cotton_top_cove} -> {Regions.squirt_showdown_map}":
                Has(Events.cove_level, count=FromOption(options.RequiredCoveLevels)),
            f"{Regions.mekanos} -> {Regions.kaos_karnage_map}":
                Has(Events.mekanos_level, count=FromOption(options.RequiredMekanosLevels)),
            f"{Regions.k3} -> {Regions.bleaks_house_map}":
                Has(Events.k3_level, count=FromOption(options.RequiredK3Levels)),
            f"{Regions.razor_ridge} -> {Regions.barbos_barrier_map}":
                Has(Events.ridge_level, count=FromOption(options.RequiredRidgeLevels)),
            f"{Regions.kaos_kore} -> {Regions.kastle_kaos_map}":
                Has(Events.kore_level, count=FromOption(options.RequiredKoreLevels)),
            f"{Regions.krematoa} -> {Regions.knautilus_map}":
                Has(Events.krematoa_level, count=FromOption(options.RequiredKrematoaLevels)) & CanOpenKnautilus,

            # Krematoa special casing
            f"{Regions.krematoa} -> {Regions.stampede_sprint_map}":
                Has(Items.bonus_coin, 1) | CanOpenKnautilus,
            f"{Regions.krematoa} -> {Regions.criss_kross_cliffs_map}":
                Has(Items.bonus_coin, 2) | CanOpenKnautilus,
            f"{Regions.krematoa} -> {Regions.tyrant_twin_tussle_map}":
                Has(Items.bonus_coin, 3) | CanOpenKnautilus,
            f"{Regions.krematoa} -> {Regions.swoopy_salvo_map}":
                Has(Items.bonus_coin, 4) | CanOpenKnautilus,
            f"{Regions.krematoa} -> {Regions.rocket_rush_map}":
                Has(Items.bonus_coin, 5) | CanOpenKnautilus,
        }

        self.bird_rules = {
            Locations.bird_bounty_beach:
                True_(),
            Locations.bird_kong_cave:
                True_(),
            Locations.bird_undercover_cove:
                True_(),
            Locations.bird_belchas_burrow:
                True_(),
            Locations.bird_ks_kache:
                True_(),
            Locations.bird_hill_top_hoard:
                True_(),
            Locations.bird_smugglers_cove:
                True_(),
            Locations.bird_arichs_hoard:
                True_(),
                #CanReachLocation(Locations.riverside_race_clear),
            Locations.bird_bounty_bay:
                True_(),
            #Locations.bird_sky_high_secret:
            #    CanReachRegion(Regions.k3) & CanReachRegion(Regions.cotton_top_cove),
            Locations.bird_glacial_grotto:
                True_(),
            #Locations.bird_clifftop_cache:
            #    True_(), # this is an unholy rule i don't want to write yet
            Locations.bird_sewer_stockpile:
                True_(),
        }

    def set_dkc3_rules(self) -> None:
        multiworld = self.world.multiworld

        for entrance_name, rule in self.connection_rules.items():
            try:
                entrance = multiworld.get_entrance(entrance_name, self.player)
                self.world.set_rule(entrance, rule)
            except KeyError:
                continue

        for loc in multiworld.get_locations(self.player):
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
            
            if loc.name in self.bird_rules:
                rule = self.bird_rules[loc.name]
                self.world.set_rule(self.world.get_location(loc.name), rule)


        if self.world.options.goal == options.Goal.option_kore:
            self.world.set_completion_rule(Has(Events.k_rool_at_kore))
        elif self.world.options.goal == options.Goal.option_krematoa:
            self.world.set_completion_rule(Has(Events.k_rool_at_knautilus))
        else:
            self.world.set_completion_rule(HasAll(Events.k_rool_at_kore, Events.k_rool_at_knautilus))
            

    def set_dkc3_glitched_rules(self, non_glitched_rules: dict[str, Rule]) -> None:
        multiworld = self.world.multiworld

        for loc in multiworld.get_locations(self.player):
            # Skip events so we don't have to type duplicate entries...
            if "(Map Event)" in loc.name:
                continue
            # The second condition looks absolutely hideous, Rule Builder makes it possible LOL
            if loc.name in self.location_rules and not (non_glitched_rules[loc.name] == (self.location_rules[loc.name])):
                glitched_rule = non_glitched_rules[loc.name] | (self.location_rules[loc.name] & Has(Items.glitched))
                self.world.set_rule(self.world.get_location(loc.name), glitched_rule)
                # Set event rules at the same time as the real location
                if "- Clear" in loc.name:
                    try:
                        map_event: Location = multiworld.get_location(f"{loc.name} (Map Event)", self.player)
                        self.world.set_rule(map_event, glitched_rule)
                    except KeyError:
                        # Filter out missing locations
                        continue


class DKC3StrictRules(DKC3Rules):
    def __init__(self, world: "DKC3World") -> None:
        super().__init__(world)

        self.location_rules = {
        
            Locations.lakeside_limbo_clear:
                CanSwim,
            Locations.lakeside_limbo_bonus_1:
                CanClimb & CanTeamAttack,
            Locations.lakeside_limbo_bonus_2:
                CanClimb & CanSwim,
            Locations.lakeside_limbo_dk_coin:
                CanCarry,
            Locations.lakeside_limbo_kong:
                CanSwim,
            Locations.lakeside_limbo_balloon_1:
                CanTeamAttack,
            Locations.lakeside_limbo_balloon_2:
                CanTeamAttack,
            Locations.lakeside_limbo_bananas_1:
                True_(),
            Locations.lakeside_limbo_coin_1:
                ( CanClimb & CanHover ) | CanTeamAttack,
            Locations.lakeside_limbo_balloon_3:
                ( CanClimb & CanHover ) | CanTeamAttack,
            Locations.lakeside_limbo_coin_2:
                ( CanClimb & CanHover ) | CanTeamAttack,
            Locations.lakeside_limbo_bananas_2:
                CanSwim,
            Locations.lakeside_limbo_balloon_4:
                CanSwim,
            Locations.lakeside_limbo_balloon_5:
                CanSwim & ( CanTeamAttack | HasEllie ),
            Locations.lakeside_limbo_coin_3:
                CanSwim & HasEllie,
            Locations.lakeside_limbo_coin_4:
                CanSwim & CanTeamAttack,
            Locations.lakeside_limbo_bananas_3:
                CanSwim & CanTeamAttack,
            Locations.lakeside_limbo_bananas_4:
                CanSwim,

            Locations.doorstop_dash_clear:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bonus_1:
                CanHover & CanTeamAttack,
            Locations.doorstop_dash_bonus_2:
                CanClimb & HasBarrelCannon & CanHover,
            Locations.doorstop_dash_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.doorstop_dash_kong:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bananas_1:
                True_(),
            Locations.doorstop_dash_coin_1:
                CanTeamAttack | CanHover | CanSpin,
            Locations.doorstop_dash_balloon_1:
                CanHover & CanTeamAttack,
            Locations.doorstop_dash_balloon_2:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bananas_2:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_coin_2:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_balloon_3:
                CanClimb & HasBarrelCannon & CanSpin & CanHover,
            Locations.doorstop_dash_balloon_4:
                CanClimb & HasBarrelCannon & CanHover,

            Locations.tidal_trouble_clear:
                CanSwim,
            Locations.tidal_trouble_bonus_1:
                CanSwim & HasEnguarde,
            Locations.tidal_trouble_bonus_2:
                CanSwim & CanWaterBounce & CanClimb,
            Locations.tidal_trouble_dk_coin:
                CanCarry & CanTeamAttack,
            Locations.tidal_trouble_kong:
                CanSwim,
            Locations.tidal_trouble_bananas_1:
                CanSwim,
            Locations.tidal_trouble_bananas_2:
                CanSwim & HasEnguarde,
            Locations.tidal_trouble_coin_1:
                CanSwim & CanHover,
            Locations.tidal_trouble_coin_2:
                CanSwim,
            Locations.tidal_trouble_balloon_1:
                CanSwim & CanTeamAttack,

            Locations.skiddas_row_clear:
                True_(),
            Locations.skiddas_row_bonus_1:
                True_(),
            Locations.skiddas_row_bonus_2:
                True_(),
            Locations.skiddas_row_dk_coin:
                CanCarry,
            Locations.skiddas_row_kong:
                True_(),
            Locations.skiddas_row_coin_1:
                True_(),
            Locations.skiddas_row_coin_2:
                True_(),
            Locations.skiddas_row_coin_3:
                True_(),
            Locations.skiddas_row_bananas_1:
                True_(),
            Locations.skiddas_row_balloon_1:
                True_(),

            Locations.murky_mill_clear:
                True_(),
            Locations.murky_mill_bonus_1:
                HasEllie | CanCarry,
            Locations.murky_mill_bonus_2:
                HasEllie & HasBarrelCannon,
            Locations.murky_mill_dk_coin:
                HasEllie | CanCarry,
            Locations.murky_mill_kong:
                True_(),
            Locations.murky_mill_bananas_1:
                True_(),
            Locations.murky_mill_bananas_2:
                True_(),
            Locations.murky_mill_coin_1:
                True_(),
            Locations.murky_mill_coin_2:
                True_(),
            Locations.murky_mill_coin_3:
                HasEllie,
            Locations.murky_mill_balloon_1:
                True_(),
                
            Locations.belchas_barn_clear:
                HasBothKongs & CanCarry,
            Locations.defeated_belcha:
                HasBothKongs & CanCarry,

            Locations.barrel_shield_bust_up_clear:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_bonus_1:
                CanClimb & HasBarrelShield & CanCarry,
            Locations.barrel_shield_bust_up_bonus_2:
                CanClimb & HasBarrelShield & CanHover & CanCarry,
            Locations.barrel_shield_bust_up_dk_coin:
                CanClimb & HasBarrelShield & CanCarry & CanTeamAttack,
            Locations.barrel_shield_bust_up_kong:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_bananas_1:
                CanCarry & HasBothKongs,
            Locations.barrel_shield_bust_up_bananas_2:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_coin_1:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_coin_2:
                CanClimb & HasBarrelShield,

            Locations.riverside_race_clear:
                CanSwim,
            Locations.riverside_race_bonus_1:
                CanSwim & CanWaterBounce,
            Locations.riverside_race_bonus_2:
                CanSwim & HasBarrelInvincible,
            Locations.riverside_race_dk_coin:
                CanSwim & CanWaterBounce & CanCarry,
            Locations.riverside_race_kong:
                CanSwim,
            Locations.riverside_race_bananas_1:
                True_(),
            Locations.riverside_race_coin_1:
                CanSwim,
            Locations.riverside_race_coin_2:
                CanSwim,
            Locations.riverside_race_bananas_2:
                CanSwim,
            Locations.riverside_race_balloon_1:
                CanSwim,
            Locations.riverside_race_bananas_3:
                CanSwim,
            Locations.riverside_race_bananas_4:
                CanSwim,
            Locations.riverside_race_bananas_5:
                CanSwim,
            Locations.riverside_race_coin_2:
                CanSwim,
            Locations.riverside_race_bananas_6:
                CanSwim,
            Locations.riverside_race_coin_3:
                CanSwim,
            Locations.riverside_race_coin_4:
                CanSwim,

            Locations.squeals_on_wheels_clear:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_bonus_1:
                CanCarry & CanClimb & CanHover,
            Locations.squeals_on_wheels_bonus_2:
                CanCarry & CanClimb & CanHover & CanTeamAttack,
            Locations.squeals_on_wheels_dk_coin:
                CanCarry & CanClimb & CanTeamAttack,
            Locations.squeals_on_wheels_kong:
                CanCarry & CanClimb & HasBarrelCannon & HasParry,
            Locations.squeals_on_wheels_bananas_1:
                True_(),
            Locations.squeals_on_wheels_bananas_2:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_3:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_4:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_5:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_6:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_7:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_coin_1:
                CanCarry & CanClimb & HasBarrelCannon & ( HasParry | CanTeamAttack ),
            Locations.squeals_on_wheels_balloon_1:
                CanCarry & CanClimb & HasBarrelCannon & HasParry,

            Locations.springing_spiders_clear:
                True_(),
            Locations.springing_spiders_bonus_1:
                HasSquawks,
            Locations.springing_spiders_bonus_2:
                CanHover,
            Locations.springing_spiders_dk_coin:
                CanCarry & CanTeamAttack,
            Locations.springing_spiders_kong:
                HasSquawks | CanTeamAttack,
            Locations.springing_spiders_coin_1:
                CanSpin,
            Locations.springing_spiders_balloon_1:
                CanTeamAttack,
            Locations.springing_spiders_bananas_1:
                CanTeamAttack,
            Locations.springing_spiders_coin_2:
                CanCarry,
            Locations.springing_spiders_coin_3:
                HasSquawks,
            Locations.springing_spiders_coin_4:
                HasSquawks,
            Locations.springing_spiders_bananas_2:
                HasSquawks,
            Locations.springing_spiders_coin_5:
                HasSquawks,
            Locations.springing_spiders_coin_6:
                True_(),
            Locations.springing_spiders_bananas_3:
                True_(),
            Locations.springing_spiders_bananas_4:
                True_(),
            Locations.springing_spiders_balloon_2:
                True_(),
            Locations.springing_spiders_balloon_3:
                True_(),
            Locations.springing_spiders_bananas_5:
                True_(),
            Locations.springing_spiders_bananas_6:
                True_(),
            Locations.springing_spiders_coin_7:
                True_(),

            Locations.bobbing_barrel_brawl_clear:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_bonus_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_bonus_2:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_dk_coin:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_kong:
                HasBarrelCannon & HasEllie & CanTeamAttack,
            Locations.bobbing_barrel_brawl_balloon_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_2:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_bananas_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_3:
                HasBarrelCannon & HasEllie & CanTeamAttack,
                
            Locations.arichs_ambush_clear:
                HasBothKongs & CanCarry,
            Locations.defeated_arich:
                HasBothKongs & CanCarry,

            Locations.bazzas_blockade_clear:
                CanSwim,
            Locations.bazzas_blockade_bonus_1:
                CanSwim,
            Locations.bazzas_blockade_bonus_2:
                CanSwim & HasEnguarde,
            Locations.bazzas_blockade_dk_coin:
                CanSwim & CanCarry,
            Locations.bazzas_blockade_kong:
                CanSwim & HasEnguarde,
            Locations.bazzas_blockade_bananas_1:
                CanSwim,
            Locations.bazzas_blockade_bananas_2:
                CanSwim,
            Locations.bazzas_blockade_coin_1:
                CanSwim,
            Locations.bazzas_blockade_coin_2:
                CanSwim,
            Locations.bazzas_blockade_coin_3:
                CanSwim,
            Locations.bazzas_blockade_coin_4:
                CanSwim & HasEnguarde,

            Locations.rocket_barrel_ride_clear:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bonus_1:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bonus_2:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_dk_coin:
                HasBarrelRocket & HasBarrelCannon & CanCarry,
            Locations.rocket_barrel_ride_kong:
                HasBarrelRocket & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.rocket_barrel_ride_bananas_1:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_bananas_2:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_1:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_2:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_bananas_3:
                HasBarrelRocket & CanHover,
            Locations.rocket_barrel_ride_coin_3:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_4:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_4:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_5:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_5:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_coin_6:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_6:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_7:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_balloon_1:
                HasBarrelRocket & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.rocket_barrel_ride_balloon_2:
                HasBarrelRocket & HasBarrelCannon & HasParry,

            Locations.kreeping_klasps_clear:
                CanClimb & CanHover,
            Locations.kreeping_klasps_bonus_1:
                CanClimb & CanHover,
            Locations.kreeping_klasps_bonus_2:
                CanClimb & CanHover & HasBarrelCannon,
            Locations.kreeping_klasps_dk_coin:
                CanClimb & CanHover & CanCarry,
            Locations.kreeping_klasps_kong:
                CanClimb & CanHover,
            Locations.kreeping_klasps_balloon_1:
                CanTeamAttack,
            Locations.kreeping_klasps_coin_1:
                CanTeamAttack & ( CanSwim | HasBarrelCannon ),
            Locations.kreeping_klasps_bananas_1:
                CanClimb & CanHover,
            Locations.kreeping_klasps_balloon_2:
                CanClimb & CanHover,
            Locations.kreeping_klasps_bananas_2:
                CanClimb & CanHover,
            Locations.kreeping_klasps_coin_2:
                CanClimb & CanHover,

            Locations.tracker_barrel_trek_clear:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_bonus_1:
                HasBarrelTracker & HasBarrelCannon & CanHover,
            Locations.tracker_barrel_trek_bonus_2:
                HasBarrelTracker & HasBarrelCannon & HasEllie,
            Locations.tracker_barrel_trek_dk_coin:
                HasBarrelTracker & HasBarrelCannon & HasEllie & CanCarry,
            Locations.tracker_barrel_trek_kong:
                HasBarrelTracker & HasBarrelCannon & CanSpin,
            Locations.tracker_barrel_trek_coin_1:
                True_(),
            Locations.tracker_barrel_trek_coin_2:
                HasBarrelTracker & HasKiddy,
            Locations.tracker_barrel_trek_bananas_1:
                HasBarrelTracker,
            Locations.tracker_barrel_trek_balloon_1:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_3:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_4:
                HasBarrelTracker & HasBarrelCannon,

            Locations.fish_food_frenzy_clear:
                CanSwim,
            Locations.fish_food_frenzy_bonus_1:
                CanSwim,
            Locations.fish_food_frenzy_bonus_2:
                CanSwim,
            Locations.fish_food_frenzy_dk_coin:
                CanSwim & CanTeamAttack & CanCarry,
            Locations.fish_food_frenzy_kong:
                CanSwim,
            Locations.fish_food_frenzy_coin_1:
                CanSwim,
            Locations.fish_food_frenzy_bananas_1:
                CanSwim,
            Locations.fish_food_frenzy_coin_2:
                CanSwim,
                
            Locations.squirt_showdown_clear:
                HasEllie,
            Locations.defeated_squirt:
                HasEllie,

            Locations.fireball_frenzy_clear:
                CanClimb,
            Locations.fireball_frenzy_bonus_1:
                CanClimb & HasSquitter & ( CanHover | CanSpin ),
            Locations.fireball_frenzy_bonus_2:
                CanClimb & CanTeamAttack,
            Locations.fireball_frenzy_dk_coin:
                CanClimb & CanCarry,
            Locations.fireball_frenzy_kong:
                CanClimb,
            Locations.fireball_frenzy_coin_1:
                True_(),
            Locations.fireball_frenzy_coin_2:
                CanTeamAttack,
            Locations.fireball_frenzy_bananas_1:
                CanClimb,
            Locations.fireball_frenzy_coin_3:
                CanClimb,
            Locations.fireball_frenzy_bananas_2:
                CanClimb,
            Locations.fireball_frenzy_coin_4:
                CanClimb & HasSquitter,
            Locations.fireball_frenzy_coin_5:
                CanClimb,
            Locations.fireball_frenzy_bananas_3:
                CanClimb,

            Locations.demolition_drain_pipe_clear:
                HasBarrelCannon,
            Locations.demolition_drain_pipe_bonus_1:
                True_(),
            Locations.demolition_drain_pipe_bonus_2:
                HasBarrelCannon,
            Locations.demolition_drain_pipe_dk_coin:
                HasBarrelCannon & CanCarry,
            Locations.demolition_drain_pipe_kong:
                True_(),
            Locations.demolition_drain_pipe_coin_1:
                True_(),
            Locations.demolition_drain_pipe_bananas_1:
                True_(),
            Locations.demolition_drain_pipe_coin_2:
                True_(),
            Locations.demolition_drain_pipe_bananas_2:
                True_(),
            Locations.demolition_drain_pipe_coin_3:
                True_(),
            Locations.demolition_drain_pipe_bananas_3:
                True_(),
            Locations.demolition_drain_pipe_coin_4:
                True_(),
            Locations.demolition_drain_pipe_bananas_4:
                True_(),
            Locations.demolition_drain_pipe_bananas_5:
                True_(),
            Locations.demolition_drain_pipe_bananas_6:
                True_(),
            Locations.demolition_drain_pipe_coin_5:
                True_(),
            Locations.demolition_drain_pipe_coin_6:
                True_(),
            Locations.demolition_drain_pipe_coin_7:
                True_(),
            Locations.demolition_drain_pipe_bananas_7:
                True_(),

            Locations.ripsaw_rage_clear:
                True_(),
            Locations.ripsaw_rage_bonus_1:
                CanCarry,
            Locations.ripsaw_rage_bonus_2:
                CanCarry & HasBarrelInvincible,
            Locations.ripsaw_rage_dk_coin:
                CanCarry & HasBarrelInvincible & HasBarrelCannon,
            Locations.ripsaw_rage_kong:
                True_(),
            Locations.ripsaw_rage_coin_1:
                CanCarry & HasBothKongs,
            Locations.ripsaw_rage_bananas_1:
                True_(),
            Locations.ripsaw_rage_coin_2:
                True_(),
            Locations.ripsaw_rage_bananas_2:
                True_(),
            Locations.ripsaw_rage_coin_3:
                CanSpin,
            Locations.ripsaw_rage_bananas_3:
                True_(),
            #Locations.ripsaw_rage_coin_4:
            #    True_(),
            Locations.ripsaw_rage_bananas_4:
                True_(),

            Locations.blazing_bazukas_clear:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_bonus_1:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_bonus_2:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ) & CanHover,
            Locations.blazing_bazukas_dk_coin:
                HasBarrelCannon & CanClimb & HasSquitter & HasBarrelSwitch,
            Locations.blazing_bazukas_kong:
                HasBarrelCannon & CanClimb & ( HasSquitter | CanTeamAttack & HasBarrelSwitch ),
            Locations.blazing_bazukas_coin_1:
                HasBarrelCannon & CanClimb,
            Locations.blazing_bazukas_coin_2:
                HasBarrelCannon & CanClimb,
            Locations.blazing_bazukas_bananas_1:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_coin_3:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_bananas_2:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_bananas_3:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_coin_4:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_balloon_1:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),

            Locations.low_g_labyrinth_clear:
                HasSquawks,
            Locations.low_g_labyrinth_bonus_1:
                HasSquawks | CanTeamAttack,
            Locations.low_g_labyrinth_bonus_2:
                HasSquawks,
            Locations.low_g_labyrinth_dk_coin:
                HasSquawks & CanCarry,
            Locations.low_g_labyrinth_kong:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_1:
                True_(),
            Locations.low_g_labyrinth_coin_1:
                True_(),
            Locations.low_g_labyrinth_bananas_2:
                True_(),
            Locations.low_g_labyrinth_coin_2:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_3:
                HasSquawks,
            Locations.low_g_labyrinth_balloon_1:
                HasSquawks,
            Locations.low_g_labyrinth_coin_3:
                HasSquawks,
            Locations.low_g_labyrinth_coin_4:
                HasSquawks,
            Locations.low_g_labyrinth_coin_5:
                HasSquawks,
            Locations.low_g_labyrinth_coin_6:
                HasSquawks,
            Locations.low_g_labyrinth_coin_7:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_4:
                HasSquawks,
                
            Locations.kaos_karnage_clear:
                HasBothKongs,
            Locations.defeated_kaos:
                HasBothKongs,

            Locations.krevice_kreepers_clear:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bonus_1:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bonus_2:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_dk_coin:
                CanClimb & CanCarry,
            Locations.krevice_kreepers_kong:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_1:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_2:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_3:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_coin_1:
                CanClimb,
            Locations.krevice_kreepers_bananas_4:
                CanClimb,
            Locations.krevice_kreepers_coin_2:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_balloon_1:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_coin_3:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_coin_5:
                CanClimb & HasBarrelCannon & CanTeamAttack,
            Locations.krevice_kreepers_coin_6:
                CanClimb & HasBarrelCannon & CanTeamAttack,

            Locations.tearaway_toboggan_clear:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bonus_1:
                HasBarrelCannon & CanTeamAttack,
            Locations.tearaway_toboggan_bonus_2:
                HasBarrelCannon,
            Locations.tearaway_toboggan_dk_coin:
                HasBarrelCannon & CanCarry,
            Locations.tearaway_toboggan_kong:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_1:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_1:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_2:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_3:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_2:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_4:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_3:
                HasBarrelCannon,
            Locations.tearaway_toboggan_balloon_1:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_5:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_6:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_4:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_5:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_6:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_7:
                HasBarrelCannon & ( CanCarry | CanHover | CanTeamAttack ),
            Locations.tearaway_toboggan_balloon_2:
                HasBarrelCannon & CanTeamAttack,

            Locations.barrel_drop_bounce_clear:
                HasBarrelWaterfall & HasBarrelCannon & CanHover,
            Locations.barrel_drop_bounce_bonus_1:
                HasBarrelWaterfall & HasBarrelCannon,
            Locations.barrel_drop_bounce_bonus_2:
                HasBarrelWaterfall & HasBarrelCannon & CanHover,
            Locations.barrel_drop_bounce_dk_coin:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & CanCarry,
            Locations.barrel_drop_bounce_kong:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & ( CanCarry | CanTeamAttack ),
            Locations.barrel_drop_bounce_coin_1:
                HasBarrelWaterfall | CanTeamAttack,
            Locations.barrel_drop_bounce_coin_2:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & HasParry,
            Locations.barrel_drop_bounce_balloon_1:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & HasParry,

            Locations.krackshot_krock_clear:
                HasSquitter,
            Locations.krackshot_krock_bonus_1:
                HasSquitter,
            Locations.krackshot_krock_bonus_2:
                HasSquitter,
            Locations.krackshot_krock_dk_coin:
                HasSquitter & CanCarry,
            Locations.krackshot_krock_kong:
                HasSquitter,
            Locations.krackshot_krock_coin_1:
                CanTeamAttack,
            Locations.krackshot_krock_coin_2:
                CanTeamAttack,
            Locations.krackshot_krock_balloon_1:
                HasSquitter,
            Locations.krackshot_krock_bananas_1:
                HasSquitter,
            Locations.krackshot_krock_bananas_2:
                HasSquitter,
            Locations.krackshot_krock_coin_3:
                HasSquitter,
            Locations.krackshot_krock_bananas_3:
                HasSquitter,
            Locations.krackshot_krock_coin_4:
                HasSquitter,
            Locations.krackshot_krock_coin_5:
                HasSquitter,
            Locations.krackshot_krock_bananas_3:
                HasSquitter,
            Locations.krackshot_krock_bananas_4:
                HasSquitter,
            Locations.krackshot_krock_bananas_5:
                HasSquitter,

            Locations.lemguin_lunge_clear:
                True_(),
            Locations.lemguin_lunge_bonus_1:
                CanTeamAttack,
            Locations.lemguin_lunge_bonus_2:
                CanSpin,
            Locations.lemguin_lunge_dk_coin:
                CanCarry,
            Locations.lemguin_lunge_kong:
                True_(),
            Locations.lemguin_lunge_coin_1:
                CanSpin,
            Locations.lemguin_lunge_bananas_1:
                True_(),
            Locations.lemguin_lunge_coin_2:
                True_(),
                
            Locations.bleaks_house_clear:
                HasBothKongs,
            Locations.defeated_bleak:
                HasBothKongs,

            Locations.buzzer_barrage_clear:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bonus_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bonus_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_dk_coin:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_kong:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_1:
                CanTeamAttack,
            Locations.buzzer_barrage_coin_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_4:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_5:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_6:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_7:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_4:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_5:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_6:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_7:
                CanTeamAttack & HasSquawks,

            Locations.kongfused_cliffs_clear:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bonus_1:
                CanClimb & CanHover & HasBarrelCannon,
            Locations.kongfused_cliffs_bonus_2:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.kongfused_cliffs_kong:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_1:
                CanClimb & CanHover,
            Locations.kongfused_cliffs_coin_2:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_3:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_5:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bananas_1:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bananas_2:
                CanClimb & HasBarrelCannon,

            Locations.floodlit_fish_clear:
                CanSwim & HasEnguarde & HasBarrelCannon,
            Locations.floodlit_fish_bonus_1:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bonus_2:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_dk_coin:
                CanSwim & HasEnguarde & HasBarrelCannon & CanCarry,
            Locations.floodlit_fish_kong:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_1:
                CanSwim,
            Locations.floodlit_fish_bananas_2:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_1:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_3:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_4:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_2:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_5:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_6:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_3:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_7:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_8:
                CanSwim & HasEnguarde,

            Locations.pot_hole_panic_clear:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack ) & HasBarrelCannon,
            Locations.pot_hole_panic_bonus_1:
                HasSquawks & CanSwim & HasEllie,
            Locations.pot_hole_panic_bonus_2:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack ) & HasBarrelCannon & HasSquitter,
            Locations.pot_hole_panic_dk_coin:
                HasSquawks & CanSwim & CanTeamAttack & HasBarrelCannon & CanCarry,
            Locations.pot_hole_panic_kong:
                HasSquawks & CanSwim & HasEllie & HasBarrelCannon & ( HasSquitter | CanHover ),
            Locations.pot_hole_panic_bananas_1:
                HasSquawks,
            Locations.pot_hole_panic_bananas_2:
                HasSquawks,
            Locations.pot_hole_panic_coin_1:
                HasSquawks,
            Locations.pot_hole_panic_bananas_3:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_4:
                HasSquawks & CanSwim & HasEnguarde,
            Locations.pot_hole_panic_bananas_5:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_6:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_7:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_8:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_coin_2:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_coin_3:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_9:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_coin_4:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_10:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack ) & HasBarrelCannon,
            Locations.pot_hole_panic_bananas_11:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack ) & HasBarrelCannon & HasSquitter,

            Locations.ropey_rumpus_clear:
                CanClimb,
            Locations.ropey_rumpus_bonus_1:
                CanClimb & CanCarry,
            Locations.ropey_rumpus_bonus_2:
                CanClimb & HasParry,
            Locations.ropey_rumpus_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.ropey_rumpus_kong:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_coin_1:
                CanTeamAttack,
            Locations.ropey_rumpus_coin_2:
                CanTeamAttack,
            Locations.ropey_rumpus_bananas_1:
                CanClimb & CanCarry,
            Locations.ropey_rumpus_coin_3:
                CanClimb,
            Locations.ropey_rumpus_bananas_2:
                CanClimb,
            Locations.ropey_rumpus_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.ropey_rumpus_coin_5:
                CanClimb & HasBarrelCannon,
            Locations.ropey_rumpus_bananas_3:
                CanClimb,
            Locations.ropey_rumpus_coin_6:
                CanClimb,
            Locations.ropey_rumpus_coin_7:
                CanClimb,
            Locations.ropey_rumpus_bananas_4:
                CanClimb,
            Locations.ropey_rumpus_balloon_1:
                CanClimb,
            Locations.ropey_rumpus_bananas_5:
                CanClimb,
            Locations.ropey_rumpus_bananas_6:
                CanClimb,
            Locations.ropey_rumpus_bananas_7:
                CanClimb,
            Locations.ropey_rumpus_bananas_8:
                CanClimb,
            Locations.ropey_rumpus_bananas_9:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_balloon_2:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_coin_8:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_bananas_10:
                CanClimb & HasParry,
                
            Locations.barbos_barrier_clear:
                HasBothKongs & CanSwim & HasEnguarde,
            Locations.defeated_barbos:
                HasBothKongs & CanSwim & HasEnguarde,

            Locations.konveyor_rope_klash_clear:
                CanClimb,
            Locations.konveyor_rope_klash_bonus_1:
                CanClimb,
            Locations.konveyor_rope_klash_bonus_2:
                CanClimb,
            Locations.konveyor_rope_klash_dk_coin:
                CanClimb & CanCarry,
            Locations.konveyor_rope_klash_kong:
                CanClimb,
            Locations.konveyor_rope_klash_coin_1:
                CanClimb | CanTeamAttack,
            Locations.konveyor_rope_klash_coin_2:
                CanClimb,
            Locations.konveyor_rope_klash_coin_3:
                CanClimb & CanTeamAttack,
            Locations.konveyor_rope_klash_balloon_1:
                CanClimb,
            Locations.konveyor_rope_klash_balloon_2:
                CanClimb & CanTeamAttack,

            Locations.creepy_caverns_clear:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_bonus_1:
                HasBarrelGhost & HasBarrelCannon & CanSpin & CanTeamAttack,
            Locations.creepy_caverns_bonus_2:
                HasBarrelGhost & HasBarrelCannon & CanCarry & CanTeamAttack & HasSquitter,
            Locations.creepy_caverns_dk_coin:
                HasBarrelGhost & HasBarrelCannon & CanCarry,
            Locations.creepy_caverns_kong:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_bananas_1:
                CanCarry | CanTeamAttack,
            Locations.creepy_caverns_coin_1:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_coin_2:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_coin_3:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_bananas_2:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_coin_4:
                HasBarrelGhost & HasBarrelCannon & CanCarry & CanTeamAttack & HasSquitter,
            Locations.creepy_caverns_coin_5:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_coin_6:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_balloon_1:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,

            Locations.lightning_look_out_clear:
                CanCarry & CanSwim,
            Locations.lightning_look_out_bonus_1:
                CanCarry & CanSwim,
            Locations.lightning_look_out_bonus_2:
                CanCarry & CanSwim & CanTeamAttack,
            Locations.lightning_look_out_dk_coin:
                CanCarry & ( CanSwim | CanHover ),
            Locations.lightning_look_out_kong:
                CanCarry & CanSwim,
            Locations.lightning_look_out_balloon_1:
                CanTeamAttack,
            Locations.lightning_look_out_coin_1:
                CanTeamAttack,
            Locations.lightning_look_out_coin_2:
                CanTeamAttack,
            Locations.lightning_look_out_bananas_1:
                CanCarry,
            Locations.lightning_look_out_coin_3:
                CanCarry & ( CanSwim | CanHover ) & CanTeamAttack,
            Locations.lightning_look_out_balloon_2:
                CanCarry & CanSwim & CanTeamAttack,

            Locations.koindozer_klamber_clear:
                CanHover & CanClimb,
            Locations.koindozer_klamber_bonus_1:
                CanHover & CanClimb,
            Locations.koindozer_klamber_bonus_2:
                CanHover & CanClimb & CanTeamAttack,
            Locations.koindozer_klamber_dk_coin:
                CanHover & CanClimb & HasBarrelSwitch,
            Locations.koindozer_klamber_kong:
                CanHover & CanClimb,
            Locations.koindozer_klamber_coin_1:
                CanHover & CanClimb,
            Locations.koindozer_klamber_coin_2:
                CanHover & CanClimb & CanTeamAttack,
            Locations.koindozer_klamber_coin_3:
                CanHover & CanClimb,
            Locations.koindozer_klamber_bananas_1:
                CanHover & CanClimb,
            Locations.koindozer_klamber_balloon_1:
                CanHover & CanClimb & CanTeamAttack,

            Locations.poisonous_pipeline_clear:
                CanSwim,
            Locations.poisonous_pipeline_bonus_1:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_bonus_2:
                CanSwim,
            Locations.poisonous_pipeline_dk_coin:
                CanSwim & CanCarry,
            Locations.poisonous_pipeline_kong:
                CanSwim,
            Locations.poisonous_pipeline_coin_1:
                CanSwim,
            Locations.poisonous_pipeline_bananas_1:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_bananas_2:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_coin_2:
                CanSwim,
            Locations.poisonous_pipeline_balloon_1:
                CanSwim & HasEnguarde,
                
            Locations.kastle_kaos_clear:
                HasBothKongs & CanCarry,
            Locations.defeated_krool_castle:
                HasBothKongs & CanCarry,

            Locations.stampede_sprint_clear:
                CanHover & HasEllie & HasBarrelCannon,
            Locations.stampede_sprint_bonus_1:
                CanTeamAttack & HasSquitter,
            Locations.stampede_sprint_bonus_2:
                CanTeamAttack & HasSquawks,
            Locations.stampede_sprint_bonus_3:
                CanHover & HasEllie & HasBarrelCannon & HasParry,
            Locations.stampede_sprint_dk_coin:
                CanHover & HasEllie & HasBarrelCannon & CanCarry,
            Locations.stampede_sprint_kong:
                CanHover & HasEllie & HasBarrelCannon & CanTeamAttack & HasSquitter,
            Locations.stampede_sprint_coin_1:
                CanHover & HasEllie & HasBarrelCannon & HasParry,
            Locations.stampede_sprint_coin_2:
                CanHover & HasEllie & HasBarrelCannon & HasParry,

            Locations.criss_kross_cliffs_clear:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_bonus_1:
                True_(),
            Locations.criss_kross_cliffs_bonus_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_dk_coin:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanCarry,
            Locations.criss_kross_cliffs_kong:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_bananas_1:
                True_(),
            Locations.criss_kross_cliffs_coin_1:
                HasBarrelSwitch & HasBarrelCannon,
            Locations.criss_kross_cliffs_bananas_2:
                HasBarrelSwitch & HasBarrelCannon,
            Locations.criss_kross_cliffs_coin_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_coin_3:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_coin_4:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_bananas_3:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_balloon_1:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_balloon_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,

            Locations.tyrant_twin_tussle_clear:
                True_(),
            Locations.tyrant_twin_tussle_bonus_1:
                CanTeamAttack &  ( HasSquitter | CanHover ),
            Locations.tyrant_twin_tussle_bonus_2:
                CanTeamAttack & HasBarrelCannon & CanCarry & CanHover,
            Locations.tyrant_twin_tussle_bonus_3:
                CanHover,
            Locations.tyrant_twin_tussle_dk_coin:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_kong:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_coin_1:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_balloon_1:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_balloon_2:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_coin_2:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_bananas_1:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_coin_3:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_coin_4:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_bananas_2:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_coin_5:
                HasBarrelCannon,
            Locations.tyrant_twin_tussle_coin_6:
                HasBarrelCannon,
            Locations.tyrant_twin_tussle_bananas_3:
                HasBarrelCannon,

            Locations.swoopy_salvo_clear:
                HasSquawks & HasBarrelCannon & CanClimb,
            Locations.swoopy_salvo_bonus_1:
                HasSquawks & HasBarrelCannon & (CanSpin | CanHover),
            Locations.swoopy_salvo_bonus_2:
                HasSquawks,
            Locations.swoopy_salvo_bonus_3:
                HasSquawks & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.swoopy_salvo_dk_coin:
                HasSquawks & CanCarry,
            Locations.swoopy_salvo_kong:
                HasSquawks & HasBarrelCannon & CanClimb,
            Locations.swoopy_salvo_bananas_1:
                HasSquawks,
            Locations.swoopy_salvo_coin_1:
                HasSquawks,
            Locations.swoopy_salvo_bananas_2:
                HasSquawks,

            Locations.rocket_rush_clear:
                True_(),
            Locations.rocket_rush_dk_coin:
                CanCarry,
            Locations.rocket_rush_bananas_1:
                True_(),
            Locations.rocket_rush_coin_1:
                True_(),
            Locations.rocket_rush_bananas_2:
                True_(),
            Locations.rocket_rush_bananas_3:
                True_(),
            Locations.rocket_rush_coin_2:
                True_(),
            Locations.rocket_rush_coin_3:
                True_(),
            Locations.rocket_rush_coin_4:
                True_(),
                
            Locations.knautilus_clear:
                HasBothKongs & CanCarry,
            Locations.defeated_krool_knautilus:
                HasBothKongs & CanCarry,
            
        }

class DKC3LooseRules(DKC3Rules):
    def __init__(self, world: "DKC3World") -> None:
        super().__init__(world)

        self.location_rules = {
        
            Locations.lakeside_limbo_clear:
                CanSwim,
            Locations.lakeside_limbo_bonus_1:
                CanClimb & CanTeamAttack,
            Locations.lakeside_limbo_bonus_2:
                CanClimb & CanSwim,
            Locations.lakeside_limbo_dk_coin:
                CanCarry,
            Locations.lakeside_limbo_kong:
                CanSwim,
            Locations.lakeside_limbo_balloon_1:
                CanTeamAttack,
            Locations.lakeside_limbo_balloon_2:
                CanTeamAttack,
            Locations.lakeside_limbo_bananas_1:
                True_(),
            Locations.lakeside_limbo_coin_1:
                ( CanClimb & CanHover ) | CanTeamAttack,
            Locations.lakeside_limbo_balloon_3:
                ( CanClimb & CanHover ) | CanTeamAttack,
            Locations.lakeside_limbo_coin_2:
                ( CanClimb & CanHover ) | CanTeamAttack,
            Locations.lakeside_limbo_bananas_2:
                CanSwim,
            Locations.lakeside_limbo_balloon_4:
                CanSwim,
            Locations.lakeside_limbo_balloon_5:
                ( CanSwim | CanHover ) & ( CanTeamAttack | HasEllie ),
            Locations.lakeside_limbo_coin_3:
                ( CanSwim | CanHover ) & HasEllie,
            Locations.lakeside_limbo_coin_4:
                ( CanSwim | CanHover ) & CanTeamAttack,
            Locations.lakeside_limbo_bananas_3:
                ( CanSwim | CanHover ) & CanTeamAttack,
            Locations.lakeside_limbo_bananas_4:
                CanSwim | CanHover,

            Locations.doorstop_dash_clear:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bonus_1:
                CanHover & CanTeamAttack,
            Locations.doorstop_dash_bonus_2:
                CanClimb & HasBarrelCannon & CanHover,
            Locations.doorstop_dash_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.doorstop_dash_kong:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bananas_1:
                True_(),
            Locations.doorstop_dash_coin_1:
                CanTeamAttack | CanHover | CanSpin,
            Locations.doorstop_dash_balloon_1:
                CanHover & CanTeamAttack,
            Locations.doorstop_dash_balloon_2:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bananas_2:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_coin_2:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_balloon_3:
                CanClimb & HasBarrelCannon & CanSpin & CanHover,
            Locations.doorstop_dash_balloon_4:
                CanClimb & HasBarrelCannon & CanHover,

            Locations.tidal_trouble_clear:
                CanSwim,
            Locations.tidal_trouble_bonus_1:
                CanSwim & HasEnguarde,
            Locations.tidal_trouble_bonus_2:
                CanSwim & CanWaterBounce & CanClimb,
            Locations.tidal_trouble_dk_coin:
                CanCarry & CanTeamAttack,
            Locations.tidal_trouble_kong:
                CanSwim,
            Locations.tidal_trouble_bananas_1:
                CanSwim,
            Locations.tidal_trouble_bananas_2:
                CanSwim & HasEnguarde,
            Locations.tidal_trouble_coin_1:
                CanSwim & CanHover,
            Locations.tidal_trouble_coin_2:
                CanSwim,
            Locations.tidal_trouble_balloon_1:
                CanSwim & CanTeamAttack,

            Locations.skiddas_row_clear:
                True_(),
            Locations.skiddas_row_bonus_1:
                True_(),
            Locations.skiddas_row_bonus_2:
                True_(),
            Locations.skiddas_row_dk_coin:
                CanCarry,
            Locations.skiddas_row_kong:
                True_(),
            Locations.skiddas_row_coin_1:
                True_(),
            Locations.skiddas_row_coin_2:
                True_(),
            Locations.skiddas_row_coin_3:
                True_(),
            Locations.skiddas_row_bananas_1:
                True_(),
            Locations.skiddas_row_balloon_1:
                True_(),

            Locations.murky_mill_clear:
                True_(),
            Locations.murky_mill_bonus_1:
                HasEllie | CanCarry,
            Locations.murky_mill_bonus_2:
                ( HasEllie | CanCarry ) & HasBarrelCannon,
            Locations.murky_mill_dk_coin:
                HasEllie | CanCarry,
            Locations.murky_mill_kong:
                True_(),
            Locations.murky_mill_bananas_1:
                True_(),
            Locations.murky_mill_bananas_2:
                True_(),
            Locations.murky_mill_coin_1:
                True_(),
            Locations.murky_mill_coin_2:
                True_(),
            Locations.murky_mill_coin_3:
                HasEllie,
            Locations.murky_mill_balloon_1:
                True_(),
                
            Locations.belchas_barn_clear:
                CanCarry,
            Locations.defeated_belcha:
                CanCarry,

            Locations.barrel_shield_bust_up_clear:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_bonus_1:
                CanClimb & HasBarrelShield & CanCarry,
            Locations.barrel_shield_bust_up_bonus_2:
                CanClimb & HasBarrelShield & CanHover & CanCarry,
            Locations.barrel_shield_bust_up_dk_coin:
                CanClimb & HasBarrelShield & CanCarry & CanTeamAttack,
            Locations.barrel_shield_bust_up_kong:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_bananas_1:
                CanCarry & HasBothKongs,
            Locations.barrel_shield_bust_up_bananas_2:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_coin_1:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_coin_2:
                CanClimb & HasBarrelShield,

            Locations.riverside_race_clear:
                CanSwim,
            Locations.riverside_race_bonus_1:
                CanSwim & CanWaterBounce,
            Locations.riverside_race_bonus_2:
                CanSwim & HasBarrelInvincible,
            Locations.riverside_race_dk_coin:
                CanSwim & CanWaterBounce & CanCarry,
            Locations.riverside_race_kong:
                CanSwim,
            Locations.riverside_race_bananas_1:
                True_(),
            Locations.riverside_race_coin_1:
                ( CanSwim | CanHover ),
            Locations.riverside_race_coin_2:
                CanSwim,
            Locations.riverside_race_bananas_2:
                CanSwim,
            Locations.riverside_race_balloon_1:
                CanSwim,
            Locations.riverside_race_bananas_3:
                CanSwim,
            Locations.riverside_race_bananas_4:
                CanSwim,
            Locations.riverside_race_bananas_5:
                CanSwim,
            Locations.riverside_race_coin_2:
                CanSwim,
            Locations.riverside_race_bananas_6:
                CanSwim,
            Locations.riverside_race_coin_3:
                CanSwim,
            Locations.riverside_race_coin_4:
                CanSwim,

            Locations.squeals_on_wheels_clear:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_bonus_1:
                CanCarry & CanClimb & CanHover,
            Locations.squeals_on_wheels_bonus_2:
                CanCarry & CanClimb & CanHover & CanTeamAttack,
            Locations.squeals_on_wheels_dk_coin:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_kong:
                CanCarry & CanClimb & HasBarrelCannon & HasParry,
            Locations.squeals_on_wheels_bananas_1:
                True_(),
            Locations.squeals_on_wheels_bananas_2:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_3:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_4:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_5:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_6:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_7:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_coin_1:
                CanCarry & CanClimb & HasBarrelCannon & HasParry,
            Locations.squeals_on_wheels_balloon_1:
                CanCarry & CanClimb & HasBarrelCannon & HasParry,

            Locations.springing_spiders_clear:
                True_(),
            Locations.springing_spiders_bonus_1:
                HasSquawks,
            Locations.springing_spiders_bonus_2:
                True_(),
            Locations.springing_spiders_dk_coin:
                CanCarry & CanTeamAttack,
            Locations.springing_spiders_kong:
                HasSquawks | CanTeamAttack,
            Locations.springing_spiders_coin_1:
                CanSpin,
            Locations.springing_spiders_balloon_1:
                CanTeamAttack,
            Locations.springing_spiders_bananas_1:
                CanTeamAttack,
            Locations.springing_spiders_coin_2:
                CanCarry,
            Locations.springing_spiders_coin_3:
                HasSquawks,
            Locations.springing_spiders_coin_4:
                HasSquawks,
            Locations.springing_spiders_bananas_2:
                HasSquawks,
            Locations.springing_spiders_coin_5:
                HasSquawks,
            Locations.springing_spiders_coin_6:
                True_(),
            Locations.springing_spiders_bananas_3:
                True_(),
            Locations.springing_spiders_bananas_4:
                True_(),
            Locations.springing_spiders_balloon_2:
                True_(),
            Locations.springing_spiders_balloon_3:
                True_(),
            Locations.springing_spiders_bananas_5:
                True_(),
            Locations.springing_spiders_bananas_6:
                True_(),
            Locations.springing_spiders_coin_7:
                True_(),

            Locations.bobbing_barrel_brawl_clear:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_bonus_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_bonus_2:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_dk_coin:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_kong:
                HasBarrelCannon & HasEllie & CanTeamAttack,
            Locations.bobbing_barrel_brawl_balloon_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_2:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_bananas_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_3:
                HasBarrelCannon & HasEllie & CanTeamAttack,
                
            Locations.arichs_ambush_clear:
                CanCarry,
            Locations.defeated_arich:
                CanCarry,

            Locations.bazzas_blockade_clear:
                CanSwim,
            Locations.bazzas_blockade_bonus_1:
                CanSwim,
            Locations.bazzas_blockade_bonus_2:
                CanSwim & HasEnguarde,
            Locations.bazzas_blockade_dk_coin:
                CanSwim & CanCarry,
            Locations.bazzas_blockade_kong:
                CanSwim & HasEnguarde,
            Locations.bazzas_blockade_bananas_1:
                CanSwim,
            Locations.bazzas_blockade_bananas_2:
                CanSwim,
            Locations.bazzas_blockade_coin_1:
                CanSwim,
            Locations.bazzas_blockade_coin_2:
                CanSwim,
            Locations.bazzas_blockade_coin_3:
                CanSwim,
            Locations.bazzas_blockade_coin_4:
                CanSwim & HasEnguarde,

            Locations.rocket_barrel_ride_clear:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bonus_1:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bonus_2:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_dk_coin:
                HasBarrelRocket & HasBarrelCannon & CanCarry,
            Locations.rocket_barrel_ride_kong:
                HasBarrelRocket & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.rocket_barrel_ride_bananas_1:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_bananas_2:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_1:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_2:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_bananas_3:
                HasBarrelRocket & CanHover,
            Locations.rocket_barrel_ride_coin_3:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_4:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_4:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_5:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_5:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_coin_6:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_6:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_7:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_balloon_1:
                HasBarrelRocket & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.rocket_barrel_ride_balloon_2:
                HasBarrelRocket & HasBarrelCannon & HasParry,

            Locations.kreeping_klasps_clear:
                CanClimb,
            Locations.kreeping_klasps_bonus_1:
                CanClimb,
            Locations.kreeping_klasps_bonus_2:
                CanClimb & HasBarrelCannon,
            Locations.kreeping_klasps_dk_coin:
                CanClimb & CanCarry,
            Locations.kreeping_klasps_kong:
                CanClimb,
            Locations.kreeping_klasps_balloon_1:
                CanTeamAttack,
            Locations.kreeping_klasps_coin_1:
                CanTeamAttack & ( CanSwim | HasBarrelCannon ),
            Locations.kreeping_klasps_bananas_1:
                CanClimb,
            Locations.kreeping_klasps_balloon_2:
                CanClimb,
            Locations.kreeping_klasps_bananas_2:
                CanClimb,
            Locations.kreeping_klasps_coin_2:
                CanClimb & CanHover,

            Locations.tracker_barrel_trek_clear:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_bonus_1:
                HasBarrelTracker & HasBarrelCannon & CanHover,
            Locations.tracker_barrel_trek_bonus_2:
                HasBarrelTracker & HasBarrelCannon & HasEllie,
            Locations.tracker_barrel_trek_dk_coin:
                HasBarrelTracker & HasBarrelCannon & HasEllie & CanCarry,
            Locations.tracker_barrel_trek_kong:
                HasBarrelTracker & HasBarrelCannon & CanSpin,
            Locations.tracker_barrel_trek_coin_1:
                True_(),
            Locations.tracker_barrel_trek_coin_2:
                HasBarrelTracker | CanHover,
            Locations.tracker_barrel_trek_bananas_1:
                HasBarrelTracker,
            Locations.tracker_barrel_trek_balloon_1:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_3:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_4:
                HasBarrelTracker & HasBarrelCannon,

            Locations.fish_food_frenzy_clear:
                CanSwim,
            Locations.fish_food_frenzy_bonus_1:
                CanSwim,
            Locations.fish_food_frenzy_bonus_2:
                CanSwim,
            Locations.fish_food_frenzy_dk_coin:
                CanSwim & CanTeamAttack & CanCarry,
            Locations.fish_food_frenzy_kong:
                CanSwim,
            Locations.fish_food_frenzy_coin_1:
                CanSwim,
            Locations.fish_food_frenzy_bananas_1:
                CanSwim,
            Locations.fish_food_frenzy_coin_2:
                CanSwim,
                
            Locations.squirt_showdown_clear:
                HasEllie,
            Locations.defeated_squirt:
                HasEllie,

            Locations.fireball_frenzy_clear:
                CanClimb,
            Locations.fireball_frenzy_bonus_1:
                CanClimb & HasSquitter & ( CanHover | CanSpin ),
            Locations.fireball_frenzy_bonus_2:
                CanClimb & CanTeamAttack,
            Locations.fireball_frenzy_dk_coin:
                CanClimb & CanCarry,
            Locations.fireball_frenzy_kong:
                CanClimb,
            Locations.fireball_frenzy_coin_1:
                True_(),
            Locations.fireball_frenzy_coin_2:
                CanTeamAttack,
            Locations.fireball_frenzy_bananas_1:
                CanClimb,
            Locations.fireball_frenzy_coin_3:
                CanClimb,
            Locations.fireball_frenzy_bananas_2:
                CanClimb,
            Locations.fireball_frenzy_coin_4:
                CanClimb & HasSquitter,
            Locations.fireball_frenzy_coin_5:
                CanClimb,
            Locations.fireball_frenzy_bananas_3:
                CanClimb,

            Locations.demolition_drain_pipe_clear:
                HasBarrelCannon,
            Locations.demolition_drain_pipe_bonus_1:
                True_(),
            Locations.demolition_drain_pipe_bonus_2:
                HasBarrelCannon,
            Locations.demolition_drain_pipe_dk_coin:
                HasBarrelCannon & CanCarry,
            Locations.demolition_drain_pipe_kong:
                True_(),
            Locations.demolition_drain_pipe_coin_1:
                True_(),
            Locations.demolition_drain_pipe_bananas_1:
                True_(),
            Locations.demolition_drain_pipe_coin_2:
                True_(),
            Locations.demolition_drain_pipe_bananas_2:
                True_(),
            Locations.demolition_drain_pipe_coin_3:
                True_(),
            Locations.demolition_drain_pipe_bananas_3:
                True_(),
            Locations.demolition_drain_pipe_coin_4:
                True_(),
            Locations.demolition_drain_pipe_bananas_4:
                True_(),
            Locations.demolition_drain_pipe_bananas_5:
                True_(),
            Locations.demolition_drain_pipe_bananas_6:
                True_(),
            Locations.demolition_drain_pipe_coin_5:
                True_(),
            Locations.demolition_drain_pipe_coin_6:
                True_(),
            Locations.demolition_drain_pipe_coin_7:
                True_(),
            Locations.demolition_drain_pipe_bananas_7:
                True_(),

            Locations.ripsaw_rage_clear:
                True_(),
            Locations.ripsaw_rage_bonus_1:
                CanCarry,
            Locations.ripsaw_rage_bonus_2:
                CanCarry & HasBarrelInvincible,
            Locations.ripsaw_rage_dk_coin:
                CanCarry & HasBarrelInvincible & HasBarrelCannon,
            Locations.ripsaw_rage_kong:
                True_(),
            Locations.ripsaw_rage_coin_1:
                CanCarry & HasBothKongs,
            Locations.ripsaw_rage_bananas_1:
                True_(),
            Locations.ripsaw_rage_coin_2:
                True_(),
            Locations.ripsaw_rage_bananas_2:
                True_(),
            Locations.ripsaw_rage_coin_3:
                CanSpin,
            Locations.ripsaw_rage_bananas_3:
                True_(),
            #Locations.ripsaw_rage_coin_4:
            #    True_(),
            Locations.ripsaw_rage_bananas_4:
                True_(),

            Locations.blazing_bazukas_clear:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_bonus_1:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_bonus_2:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ) & CanHover,
            Locations.blazing_bazukas_dk_coin:
                HasBarrelCannon & CanClimb & HasSquitter & HasBarrelSwitch,
            Locations.blazing_bazukas_kong:
                HasBarrelCannon & CanClimb & ( HasSquitter | CanTeamAttack & HasBarrelSwitch ),
            Locations.blazing_bazukas_coin_1:
                HasBarrelCannon & CanClimb,
            Locations.blazing_bazukas_coin_2:
                HasBarrelCannon & CanClimb,
            Locations.blazing_bazukas_bananas_1:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_coin_3:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_bananas_2:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_bananas_3:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_coin_4:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),
            Locations.blazing_bazukas_balloon_1:
                HasBarrelCannon & CanClimb & ( HasSquitter | HasBarrelSwitch ),

            Locations.low_g_labyrinth_clear:
                HasSquawks,
            Locations.low_g_labyrinth_bonus_1:
                HasSquawks | CanTeamAttack,
            Locations.low_g_labyrinth_bonus_2:
                HasSquawks,
            Locations.low_g_labyrinth_dk_coin:
                HasSquawks & CanCarry,
            Locations.low_g_labyrinth_kong:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_1:
                True_(),
            Locations.low_g_labyrinth_coin_1:
                True_(),
            Locations.low_g_labyrinth_bananas_2:
                True_(),
            Locations.low_g_labyrinth_coin_2:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_3:
                HasSquawks,
            Locations.low_g_labyrinth_balloon_1:
                HasSquawks,
            Locations.low_g_labyrinth_coin_3:
                HasSquawks,
            Locations.low_g_labyrinth_coin_4:
                HasSquawks,
            Locations.low_g_labyrinth_coin_5:
                HasSquawks,
            Locations.low_g_labyrinth_coin_6:
                HasSquawks,
            Locations.low_g_labyrinth_coin_7:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_4:
                HasSquawks,
                
            Locations.kaos_karnage_clear:
                True_(),
            Locations.defeated_kaos:
                True_(),

            Locations.krevice_kreepers_clear:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bonus_1:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bonus_2:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_dk_coin:
                CanClimb & CanCarry,
            Locations.krevice_kreepers_kong:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_1:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_2:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_3:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_coin_1:
                CanClimb,
            Locations.krevice_kreepers_bananas_4:
                CanClimb,
            Locations.krevice_kreepers_coin_2:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_balloon_1:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_coin_3:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_coin_5:
                CanClimb & HasBarrelCannon & CanTeamAttack,
            Locations.krevice_kreepers_coin_6:
                CanClimb & HasBarrelCannon & CanTeamAttack,

            Locations.tearaway_toboggan_clear:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bonus_1:
                HasBarrelCannon & CanTeamAttack,
            Locations.tearaway_toboggan_bonus_2:
                HasBarrelCannon,
            Locations.tearaway_toboggan_dk_coin:
                HasBarrelCannon & CanCarry,
            Locations.tearaway_toboggan_kong:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_1:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_1:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_2:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_3:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_2:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_4:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_3:
                HasBarrelCannon,
            Locations.tearaway_toboggan_balloon_1:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_5:
                HasBarrelCannon,
            Locations.tearaway_toboggan_coin_6:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_4:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_5:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_6:
                HasBarrelCannon,
            Locations.tearaway_toboggan_bananas_7:
                HasBarrelCannon & ( CanCarry | CanHover | CanTeamAttack ),
            Locations.tearaway_toboggan_balloon_2:
                HasBarrelCannon & CanTeamAttack,

            Locations.barrel_drop_bounce_clear:
                HasBarrelWaterfall & HasBarrelCannon & CanHover,
            Locations.barrel_drop_bounce_bonus_1:
                HasBarrelWaterfall & HasBarrelCannon,
            Locations.barrel_drop_bounce_bonus_2:
                HasBarrelWaterfall & HasBarrelCannon & CanHover,
            Locations.barrel_drop_bounce_dk_coin:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & CanCarry,
            Locations.barrel_drop_bounce_kong:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & ( CanCarry | CanTeamAttack ),
            Locations.barrel_drop_bounce_coin_1:
                HasBarrelWaterfall | CanTeamAttack,
            Locations.barrel_drop_bounce_coin_2:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & HasParry,
            Locations.barrel_drop_bounce_balloon_1:
                HasBarrelWaterfall & HasBarrelCannon & CanHover & HasParry,

            Locations.krackshot_krock_clear:
                HasSquitter,
            Locations.krackshot_krock_bonus_1:
                HasSquitter,
            Locations.krackshot_krock_bonus_2:
                HasSquitter,
            Locations.krackshot_krock_dk_coin:
                HasSquitter & CanCarry,
            Locations.krackshot_krock_kong:
                HasSquitter,
            Locations.krackshot_krock_coin_1:
                CanTeamAttack,
            Locations.krackshot_krock_coin_2:
                CanTeamAttack,
            Locations.krackshot_krock_balloon_1:
                HasSquitter,
            Locations.krackshot_krock_bananas_1:
                HasSquitter,
            Locations.krackshot_krock_bananas_2:
                HasSquitter,
            Locations.krackshot_krock_coin_3:
                HasSquitter,
            Locations.krackshot_krock_bananas_3:
                HasSquitter,
            Locations.krackshot_krock_coin_4:
                HasSquitter,
            Locations.krackshot_krock_coin_5:
                HasSquitter,
            Locations.krackshot_krock_bananas_3:
                HasSquitter,
            Locations.krackshot_krock_bananas_4:
                HasSquitter,
            Locations.krackshot_krock_bananas_5:
                HasSquitter,

            Locations.lemguin_lunge_clear:
                True_(),
            Locations.lemguin_lunge_bonus_1:
                CanTeamAttack,
            Locations.lemguin_lunge_bonus_2:
                True_(),
            Locations.lemguin_lunge_dk_coin:
                CanCarry,
            Locations.lemguin_lunge_kong:
                True_(),
            Locations.lemguin_lunge_coin_1:
                True_(),
            Locations.lemguin_lunge_bananas_1:
                True_(),
            Locations.lemguin_lunge_coin_2:
                True_(),
                
            Locations.bleaks_house_clear:
                True_(),
            Locations.defeated_bleak:
                True_(),

            Locations.buzzer_barrage_clear:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bonus_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bonus_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_dk_coin:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_kong:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_1:
                CanTeamAttack,
            Locations.buzzer_barrage_coin_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_4:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_5:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_6:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_7:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_4:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_5:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_6:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_7:
                CanTeamAttack & HasSquawks,

            Locations.kongfused_cliffs_clear:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bonus_1:
                CanClimb & CanHover & HasBarrelCannon,
            Locations.kongfused_cliffs_bonus_2:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.kongfused_cliffs_kong:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_1:
                CanClimb & CanHover,
            Locations.kongfused_cliffs_coin_2:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_3:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_coin_5:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bananas_1:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bananas_2:
                CanClimb & HasBarrelCannon,

            Locations.floodlit_fish_clear:
                CanSwim & HasEnguarde & HasBarrelCannon,
            Locations.floodlit_fish_bonus_1:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bonus_2:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_dk_coin:
                CanSwim & HasEnguarde & HasBarrelCannon & CanCarry,
            Locations.floodlit_fish_kong:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_1:
                CanSwim,
            Locations.floodlit_fish_bananas_2:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_1:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_3:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_4:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_2:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_5:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_6:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_3:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_7:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_8:
                CanSwim & HasEnguarde,

            Locations.pot_hole_panic_clear:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack | CanSpin ) & HasBarrelCannon,
            Locations.pot_hole_panic_bonus_1:
                HasSquawks & CanSwim & HasEllie,
            Locations.pot_hole_panic_bonus_2:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack | CanSpin ) & HasBarrelCannon & HasSquitter,
            Locations.pot_hole_panic_dk_coin:
                HasSquawks & CanSwim & CanTeamAttack & HasBarrelCannon & CanCarry,
            Locations.pot_hole_panic_kong:
                HasSquawks & CanSwim & HasEllie & HasBarrelCannon & ( HasSquitter | CanHover | CanSpin ),
            Locations.pot_hole_panic_bananas_1:
                HasSquawks,
            Locations.pot_hole_panic_bananas_2:
                HasSquawks,
            Locations.pot_hole_panic_coin_1:
                HasSquawks,
            Locations.pot_hole_panic_bananas_3:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_4:
                HasSquawks & CanSwim & HasEnguarde,
            Locations.pot_hole_panic_bananas_5:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_6:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_7:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_8:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_coin_2:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_coin_3:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_9:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_coin_4:
                HasSquawks & CanSwim,
            Locations.pot_hole_panic_bananas_10:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack | CanSpin ) & HasBarrelCannon,
            Locations.pot_hole_panic_bananas_11:
                HasSquawks & CanSwim & ( HasEllie | CanTeamAttack | CanSpin ) & HasBarrelCannon & HasSquitter,

            Locations.ropey_rumpus_clear:
                CanClimb,
            Locations.ropey_rumpus_bonus_1:
                CanClimb & CanCarry,
            Locations.ropey_rumpus_bonus_2:
                CanClimb & HasParry,
            Locations.ropey_rumpus_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.ropey_rumpus_kong:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_coin_1:
                CanTeamAttack,
            Locations.ropey_rumpus_coin_2:
                CanTeamAttack,
            Locations.ropey_rumpus_bananas_1:
                CanClimb & CanCarry,
            Locations.ropey_rumpus_coin_3:
                CanClimb,
            Locations.ropey_rumpus_bananas_2:
                CanClimb,
            Locations.ropey_rumpus_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.ropey_rumpus_coin_5:
                CanClimb & HasBarrelCannon,
            Locations.ropey_rumpus_bananas_3:
                CanClimb,
            Locations.ropey_rumpus_coin_6:
                CanClimb,
            Locations.ropey_rumpus_coin_7:
                CanClimb,
            Locations.ropey_rumpus_bananas_4:
                CanClimb,
            Locations.ropey_rumpus_balloon_1:
                CanClimb,
            Locations.ropey_rumpus_bananas_5:
                CanClimb,
            Locations.ropey_rumpus_bananas_6:
                CanClimb,
            Locations.ropey_rumpus_bananas_7:
                CanClimb,
            Locations.ropey_rumpus_bananas_8:
                CanClimb,
            Locations.ropey_rumpus_bananas_9:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_balloon_2:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_coin_8:
                CanClimb & HasBarrelCannon & ( CanTeamAttack | HasParry ),
            Locations.ropey_rumpus_bananas_10:
                CanClimb & HasParry,
                
            Locations.barbos_barrier_clear:
                CanSwim & HasEnguarde,
            Locations.defeated_barbos:
                CanSwim & HasEnguarde,

            Locations.konveyor_rope_klash_clear:
                CanClimb,
            Locations.konveyor_rope_klash_bonus_1:
                CanClimb,
            Locations.konveyor_rope_klash_bonus_2:
                CanClimb,
            Locations.konveyor_rope_klash_dk_coin:
                CanClimb & CanCarry,
            Locations.konveyor_rope_klash_kong:
                CanClimb,
            Locations.konveyor_rope_klash_coin_1:
                CanClimb | CanTeamAttack,
            Locations.konveyor_rope_klash_coin_2:
                CanClimb,
            Locations.konveyor_rope_klash_coin_3:
                CanClimb & CanTeamAttack,
            Locations.konveyor_rope_klash_balloon_1:
                CanClimb,
            Locations.konveyor_rope_klash_balloon_2:
                CanClimb & CanTeamAttack,

            Locations.creepy_caverns_clear:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_bonus_1:
                HasBarrelGhost & HasBarrelCannon & CanSpin & CanTeamAttack,
            Locations.creepy_caverns_bonus_2:
                HasBarrelGhost & HasBarrelCannon & CanCarry & CanTeamAttack & HasSquitter,
            Locations.creepy_caverns_dk_coin:
                HasBarrelGhost & HasBarrelCannon & CanCarry,
            Locations.creepy_caverns_kong:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_bananas_1:
                CanCarry | CanTeamAttack,
            Locations.creepy_caverns_coin_1:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_coin_2:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_coin_3:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_bananas_2:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_coin_4:
                HasBarrelGhost & HasBarrelCannon & CanCarry & CanTeamAttack & HasSquitter,
            Locations.creepy_caverns_coin_5:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_coin_6:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_balloon_1:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,

            Locations.lightning_look_out_clear:
                CanCarry & CanSwim,
            Locations.lightning_look_out_bonus_1:
                CanCarry & CanSwim,
            Locations.lightning_look_out_bonus_2:
                CanCarry & CanSwim & CanTeamAttack,
            Locations.lightning_look_out_dk_coin:
                CanCarry & ( CanSwim | CanHover ),
            Locations.lightning_look_out_kong:
                CanCarry & CanSwim,
            Locations.lightning_look_out_balloon_1:
                CanTeamAttack,
            Locations.lightning_look_out_coin_1:
                CanTeamAttack,
            Locations.lightning_look_out_coin_2:
                CanTeamAttack,
            Locations.lightning_look_out_bananas_1:
                CanCarry,
            Locations.lightning_look_out_coin_3:
                CanCarry & ( CanSwim | CanHover ) & CanTeamAttack,
            Locations.lightning_look_out_balloon_2:
                CanCarry & CanSwim & CanTeamAttack,

            Locations.koindozer_klamber_clear:
                CanClimb,
            Locations.koindozer_klamber_bonus_1:
                CanClimb,
            Locations.koindozer_klamber_bonus_2:
                CanClimb & CanTeamAttack,
            Locations.koindozer_klamber_dk_coin:
                CanClimb & HasBarrelSwitch,
            Locations.koindozer_klamber_kong:
                CanClimb,
            Locations.koindozer_klamber_coin_1:
                CanClimb,
            Locations.koindozer_klamber_coin_2:
                CanClimb & CanTeamAttack,
            Locations.koindozer_klamber_coin_3:
                CanClimb,
            Locations.koindozer_klamber_bananas_1:
                CanClimb,
            Locations.koindozer_klamber_balloon_1:
                CanClimb & CanTeamAttack,

            Locations.poisonous_pipeline_clear:
                CanSwim,
            Locations.poisonous_pipeline_bonus_1:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_bonus_2:
                CanSwim,
            Locations.poisonous_pipeline_dk_coin:
                CanSwim & CanCarry,
            Locations.poisonous_pipeline_kong:
                CanSwim,
            Locations.poisonous_pipeline_coin_1:
                CanSwim,
            Locations.poisonous_pipeline_bananas_1:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_bananas_2:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_coin_2:
                CanSwim,
            Locations.poisonous_pipeline_balloon_1:
                CanSwim & HasEnguarde,
                
            Locations.kastle_kaos_clear:
                CanCarry,
            Locations.defeated_krool_castle:
                CanCarry,

            Locations.stampede_sprint_clear:
                CanHover & HasEllie & HasBarrelCannon,
            Locations.stampede_sprint_bonus_1:
                CanTeamAttack & HasSquitter,
            Locations.stampede_sprint_bonus_2:
                CanTeamAttack & HasSquawks,
            Locations.stampede_sprint_bonus_3:
                CanHover & HasEllie & HasBarrelCannon & HasParry,
            Locations.stampede_sprint_dk_coin:
                CanHover & HasEllie & HasBarrelCannon & CanCarry,
            Locations.stampede_sprint_kong:
                CanHover & HasEllie & HasBarrelCannon & CanTeamAttack & HasSquitter,
            Locations.stampede_sprint_coin_1:
                CanHover & HasEllie & HasBarrelCannon & HasParry,
            Locations.stampede_sprint_coin_2:
                CanHover & HasEllie & HasBarrelCannon & HasParry,

            Locations.criss_kross_cliffs_clear:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_bonus_1:
                True_(),
            Locations.criss_kross_cliffs_bonus_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_dk_coin:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanCarry,
            Locations.criss_kross_cliffs_kong:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_bananas_1:
                True_(),
            Locations.criss_kross_cliffs_coin_1:
                HasBarrelSwitch & HasBarrelCannon,
            Locations.criss_kross_cliffs_bananas_2:
                HasBarrelSwitch & HasBarrelCannon,
            Locations.criss_kross_cliffs_coin_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_coin_3:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_coin_4:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.criss_kross_cliffs_bananas_3:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_balloon_1:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_balloon_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,

            Locations.tyrant_twin_tussle_clear:
                True_(),
            Locations.tyrant_twin_tussle_bonus_1:
                CanTeamAttack &  ( HasSquitter | CanHover ),
            Locations.tyrant_twin_tussle_bonus_2:
                CanTeamAttack & HasBarrelCannon & CanCarry & CanHover,
            Locations.tyrant_twin_tussle_bonus_3:
                CanHover,
            Locations.tyrant_twin_tussle_dk_coin:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_kong:
                True_(),
            Locations.tyrant_twin_tussle_coin_1:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_balloon_1:
                CanTeamAttack | CanSpin,
            Locations.tyrant_twin_tussle_balloon_2:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_coin_2:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_bananas_1:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_coin_3:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_coin_4:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_bananas_2:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_coin_5:
                HasBarrelCannon,
            Locations.tyrant_twin_tussle_coin_6:
                HasBarrelCannon,
            Locations.tyrant_twin_tussle_bananas_3:
                HasBarrelCannon,

            Locations.swoopy_salvo_clear:
                HasSquawks & HasBarrelCannon & CanClimb,
            Locations.swoopy_salvo_bonus_1:
                HasSquawks & HasBarrelCannon & CanSpin,
            Locations.swoopy_salvo_bonus_2:
                HasSquawks,
            Locations.swoopy_salvo_bonus_3:
                HasSquawks & HasBarrelCannon & CanClimb & CanTeamAttack,
            Locations.swoopy_salvo_dk_coin:
                HasSquawks & CanCarry,
            Locations.swoopy_salvo_kong:
                HasSquawks & HasBarrelCannon & CanClimb,
            Locations.swoopy_salvo_bananas_1:
                HasSquawks,
            Locations.swoopy_salvo_coin_1:
                HasSquawks,
            Locations.swoopy_salvo_bananas_2:
                HasSquawks,

            Locations.rocket_rush_clear:
                True_(),
            Locations.rocket_rush_dk_coin:
                CanCarry,
            Locations.rocket_rush_bananas_1:
                True_(),
            Locations.rocket_rush_coin_1:
                True_(),
            Locations.rocket_rush_bananas_2:
                True_(),
            Locations.rocket_rush_bananas_3:
                True_(),
            Locations.rocket_rush_coin_2:
                True_(),
            Locations.rocket_rush_coin_3:
                True_(),
            Locations.rocket_rush_coin_4:
                True_(),
                
            Locations.knautilus_clear:
                CanCarry,
            Locations.defeated_krool_knautilus:
                CanCarry,
            
        }

    def set_dkc3_rules(self) -> None:
        super().set_dkc3_rules()


class DKC3ExpertRules(DKC3Rules):
    def __init__(self, world: "DKC3World") -> None:
        super().__init__(world)

    
        self.location_rules = {
            Locations.lakeside_limbo_clear:
                CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin))),
            Locations.lakeside_limbo_bonus_1:
                CanTeamAttack,
            Locations.lakeside_limbo_bonus_2:
                (CanSwim & (CanTeamAttack | CanClimb)) | ((CanWaterBounce | CanHover | CanCarry) & CanTeamAttack & HasEllie),
            Locations.lakeside_limbo_dk_coin:
                CanCarry | ((CanSwim | CanWaterBounce | CanHover | CanCarry) & CanTeamAttack & HasEllie),
            Locations.lakeside_limbo_kong:
                CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin))),
            Locations.lakeside_limbo_balloon_1:
                CanTeamAttack,
            Locations.lakeside_limbo_balloon_2:
                CanTeamAttack,
            Locations.lakeside_limbo_bananas_1:
                True_(),
            Locations.lakeside_limbo_coin_1:
                CanTeamAttack | (CanClimb & CanHover),
            Locations.lakeside_limbo_balloon_3:
                CanTeamAttack,
            Locations.lakeside_limbo_coin_2:
                CanTeamAttack,
            Locations.lakeside_limbo_bananas_2:
                True_(),
            Locations.lakeside_limbo_balloon_4:
                CanSwim | (CanTeamAttack & HasEllie),
            Locations.lakeside_limbo_balloon_5:
                (CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin)))) & (HasEllie | CanSpin | CanTeamAttack),
            Locations.lakeside_limbo_coin_3:
                HasEllie & (CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin)))),
            Locations.lakeside_limbo_coin_4:
                CanTeamAttack & (CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin)))),
            Locations.lakeside_limbo_bananas_3:
                CanTeamAttack & (CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin)))),
            Locations.lakeside_limbo_bananas_4:
                CanSwim | CanWaterBounce | CanHover | (CanCarry & (HasDixie | (HasKiddy & CanSpin))),

            Locations.doorstop_dash_clear:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bonus_1:
                CanTeamAttack,
            Locations.doorstop_dash_bonus_2:
                CanClimb & CanHover & (HasBarrelCannon | CanTeamAttack),
            Locations.doorstop_dash_dk_coin:
                CanClimb & HasBarrelCannon & CanCarry,
            Locations.doorstop_dash_kong:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_bananas_1:
                True_(),
            Locations.doorstop_dash_coin_1:
                CanTeamAttack | CanHover | CanSpin | HasBothKongs,
            Locations.doorstop_dash_balloon_1:
                CanTeamAttack,
            Locations.doorstop_dash_balloon_2:
                CanClimb & (HasBarrelCannon | CanTeamAttack),
            Locations.doorstop_dash_bananas_2:
                CanClimb & (HasBarrelCannon | CanTeamAttack),
            Locations.doorstop_dash_coin_2:
                CanClimb & (HasBarrelCannon | CanTeamAttack),
            Locations.doorstop_dash_balloon_3:
                CanClimb & HasBarrelCannon,
            Locations.doorstop_dash_balloon_4:
                CanClimb & HasBarrelCannon,


            Locations.tidal_trouble_clear:
                CanSwim,
            Locations.tidal_trouble_bonus_1:
                (CanSwim & (HasBothKongs | (HasEnguarde))) | (CanHover & HasEnguarde),
            Locations.tidal_trouble_bonus_2:
                CanSwim & ((CanWaterBounce & CanClimb) | CanHover),
            Locations.tidal_trouble_dk_coin:
                CanCarry & CanTeamAttack,
            Locations.tidal_trouble_kong:
                CanSwim,
            Locations.tidal_trouble_bananas_1:
                 CanSwim | (CanHover & HasBothKongs),
            Locations.tidal_trouble_bananas_2:
                HasEnguarde & (CanSwim | CanHover),
            Locations.tidal_trouble_coin_1:
                CanSwim,
            Locations.tidal_trouble_coin_2:
                CanSwim,
            Locations.tidal_trouble_balloon_1:
                CanSwim & CanTeamAttack,

            Locations.skiddas_row_clear:
                True_(),
            Locations.skiddas_row_bonus_1:
                True_(),
            Locations.skiddas_row_bonus_2:
                True_(),
            Locations.skiddas_row_dk_coin:
                CanCarry,
            Locations.skiddas_row_kong:
                True_(),
            Locations.skiddas_row_coin_1:
                True_(),
            Locations.skiddas_row_coin_2:
                True_(),
            Locations.skiddas_row_coin_3:
                True_(),
            Locations.skiddas_row_bananas_1:
                True_(),
            Locations.skiddas_row_balloon_1:
                True_(),

            Locations.murky_mill_clear:
                True_(),
            Locations.murky_mill_bonus_1:
                HasEllie | CanCarry,
            Locations.murky_mill_bonus_2:
                ( HasEllie | CanCarry | HasBothKongs) & HasBarrelCannon,
            Locations.murky_mill_dk_coin:
                HasEllie | CanCarry,
            Locations.murky_mill_kong:
                True_(),
            Locations.murky_mill_bananas_1:
                True_(),
            Locations.murky_mill_bananas_2:
                True_(),
            Locations.murky_mill_coin_1:
                True_(),
            Locations.murky_mill_coin_2:
                True_(),
            Locations.murky_mill_coin_3:
                HasEllie,
            Locations.murky_mill_balloon_1:
                True_(),
                
            Locations.belchas_barn_clear:
                CanCarry,
            Locations.defeated_belcha:
                CanCarry,

            Locations.barrel_shield_bust_up_clear:
                CanClimb & (HasBarrelShield | CanHover),
            Locations.barrel_shield_bust_up_bonus_1:
                CanClimb & CanCarry & (HasBarrelShield | HasDixie),
            Locations.barrel_shield_bust_up_bonus_2:
                CanClimb & (HasBarrelShield | CanHover) & (CanTeamAttack | (CanCarry & (CanSpin | CanHover))),
            Locations.barrel_shield_bust_up_dk_coin:
                CanClimb & CanCarry & CanTeamAttack & (HasBarrelShield | CanHover),
            Locations.barrel_shield_bust_up_kong:
                CanClimb & (HasBarrelShield | CanHover),
            Locations.barrel_shield_bust_up_bananas_1:
                CanCarry | HasBothKongs,
            Locations.barrel_shield_bust_up_bananas_2:
                CanClimb & (HasBarrelShield | HasDixie),
            Locations.barrel_shield_bust_up_coin_1:
                CanClimb & HasBarrelShield,
            Locations.barrel_shield_bust_up_coin_2:
                CanClimb & (HasBarrelShield | CanHover),


            Locations.riverside_race_clear:
                CanSwim,
            Locations.riverside_race_bonus_1:
                CanSwim & (CanWaterBounce | HasBothKongs),
            Locations.riverside_race_bonus_2:
                CanSwim & (HasBarrelInvincible | HasBothKongs),
            Locations.riverside_race_dk_coin:
                CanSwim & CanCarry & (CanWaterBounce | HasBothKongs) ,
            Locations.riverside_race_kong:
                CanSwim,
            Locations.riverside_race_bananas_1:
                True_(),
            Locations.riverside_race_coin_1:
                CanSwim | CanHover | CanWaterBounce,
            Locations.riverside_race_coin_2:
                CanSwim | CanHover | CanWaterBounce,
            Locations.riverside_race_bananas_2:
                CanSwim | CanHover | CanWaterBounce,
            Locations.riverside_race_balloon_1:
                CanSwim,
            Locations.riverside_race_bananas_3:
                CanSwim,
            Locations.riverside_race_bananas_4:
                CanSwim,
            Locations.riverside_race_bananas_5:
                CanSwim,
            Locations.riverside_race_coin_2:
                CanSwim,
            Locations.riverside_race_bananas_6:
                CanSwim,
            Locations.riverside_race_coin_3:
                CanSwim,
            Locations.riverside_race_coin_4:
                CanSwim,

            Locations.squeals_on_wheels_clear:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_bonus_1:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bonus_2:
                CanCarry & CanClimb & CanTeamAttack,
            Locations.squeals_on_wheels_dk_coin:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_kong:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_bananas_1:
                True_(),
            Locations.squeals_on_wheels_bananas_2:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_3:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_4:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_5:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_6:
                CanCarry & CanClimb,
            Locations.squeals_on_wheels_bananas_7:
                CanCarry & CanClimb & HasBarrelCannon,
            Locations.squeals_on_wheels_coin_1:
                CanCarry & CanClimb & HasBarrelCannon & ( HasParry | CanTeamAttack ),
            Locations.squeals_on_wheels_balloon_1:
                CanCarry & CanClimb & HasBarrelCannon & HasParry,

            Locations.springing_spiders_clear:
                True_(),
            Locations.springing_spiders_bonus_1:
                HasSquawks,
            Locations.springing_spiders_bonus_2:
                True_(),
            Locations.springing_spiders_dk_coin:
                CanCarry & CanTeamAttack,
            Locations.springing_spiders_kong:
                HasSquawks | CanTeamAttack | HasBothKongs,
            Locations.springing_spiders_coin_1:
                True_(),
            Locations.springing_spiders_balloon_1:
                CanTeamAttack | HasBothKongs,
            Locations.springing_spiders_bananas_1:
                True_(),
            Locations.springing_spiders_coin_2:
                CanCarry | HasBothKongs | CanTeamAttack,
            Locations.springing_spiders_coin_3:
                HasSquawks | CanCarry | HasBothKongs,
            Locations.springing_spiders_coin_4:
                HasSquawks | CanCarry | HasBothKongs,
            Locations.springing_spiders_bananas_2:
                HasSquawks | CanCarry | HasBothKongs,
            Locations.springing_spiders_coin_5:
                HasSquawks,
            Locations.springing_spiders_coin_6:
                True_(),
            Locations.springing_spiders_bananas_3:
                True_(),
            Locations.springing_spiders_bananas_4:
                True_(),
            Locations.springing_spiders_balloon_2:
                True_(),
            Locations.springing_spiders_balloon_3:
                True_(),
            Locations.springing_spiders_bananas_5:
                True_(),
            Locations.springing_spiders_bananas_6:
                True_(),
            Locations.springing_spiders_coin_7:
                True_(),

            Locations.bobbing_barrel_brawl_clear:
                HasBarrelCannon & (HasEllie | CanHover),
            Locations.bobbing_barrel_brawl_bonus_1:
                HasBarrelCannon & (HasEllie | CanTeamAttack | CanHover | CanSwim),
            Locations.bobbing_barrel_brawl_bonus_2:
                HasBarrelCannon & (HasEllie | CanHover | CanSwim),
            Locations.bobbing_barrel_brawl_dk_coin:
                HasBarrelCannon & (HasEllie | (CanCarry & (CanTeamAttack | CanHover | CanSwim))),
            Locations.bobbing_barrel_brawl_kong:
                HasBarrelCannon & (HasEllie | CanHover),
            Locations.bobbing_barrel_brawl_balloon_1:
                HasBarrelCannon & (HasEllie | (CanCarry & (CanTeamAttack | CanHover))),
            Locations.bobbing_barrel_brawl_coin_1:
                HasBarrelCannon & (HasEllie | (CanCarry & (CanTeamAttack | CanHover))),
            Locations.bobbing_barrel_brawl_coin_2:
                HasBarrelCannon & (HasEllie | CanHover),
            Locations.bobbing_barrel_brawl_bananas_1:
                HasBarrelCannon & HasEllie,
            Locations.bobbing_barrel_brawl_coin_3:
                HasBarrelCannon & CanTeamAttack & (HasEllie | CanHover | (CanSwim & CanCarry)),
                
            Locations.arichs_ambush_clear:
                CanCarry,
            Locations.defeated_arich:
                CanCarry,

            Locations.bazzas_blockade_clear:
                CanSwim,
            Locations.bazzas_blockade_bonus_1:
                CanSwim,
            Locations.bazzas_blockade_bonus_2:
                CanSwim & HasEnguarde,
            Locations.bazzas_blockade_dk_coin:
                CanSwim & CanCarry,
            Locations.bazzas_blockade_kong:
                CanSwim & HasEnguarde,
            Locations.bazzas_blockade_bananas_1:
                CanSwim,
            Locations.bazzas_blockade_bananas_2:
                CanSwim,
            Locations.bazzas_blockade_coin_1:
                CanSwim,
            Locations.bazzas_blockade_coin_2:
                CanSwim,
            Locations.bazzas_blockade_coin_3:
                CanSwim,
            Locations.bazzas_blockade_coin_4:
                CanSwim & HasEnguarde,

            Locations.rocket_barrel_ride_clear:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bonus_1:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bonus_2:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_dk_coin:
                HasBarrelRocket & HasBarrelCannon & CanCarry,
            Locations.rocket_barrel_ride_kong:
                HasBarrelRocket & HasBarrelCannon & (CanTeamAttack | HasParry | CanSpin),
            Locations.rocket_barrel_ride_bananas_1:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_bananas_2:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_1:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_2:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_bananas_3:
                HasBarrelRocket & CanHover,
            Locations.rocket_barrel_ride_coin_3:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_4:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_4:
                HasBarrelRocket,
            Locations.rocket_barrel_ride_coin_5:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_5:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_coin_6:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_6:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_bananas_7:
                HasBarrelRocket & HasBarrelCannon,
            Locations.rocket_barrel_ride_balloon_1:
                HasBarrelRocket & HasBarrelCannon & ( CanTeamAttack | HasParry | CanSpin),
            Locations.rocket_barrel_ride_balloon_2:
                HasBarrelRocket & HasBarrelCannon & HasParry,

            Locations.kreeping_klasps_clear:
                CanSwim | CanClimb,
            Locations.kreeping_klasps_bonus_1:
                CanClimb,
            Locations.kreeping_klasps_bonus_2:
                CanSwim | (CanClimb & HasBarrelCannon),
            Locations.kreeping_klasps_dk_coin:
                (CanSwim | CanClimb) & CanCarry,
            Locations.kreeping_klasps_kong:
                CanClimb | (HasBothKongs & CanTeamAttack),
            Locations.kreeping_klasps_balloon_1:
                CanTeamAttack | CanSpin,
            Locations.kreeping_klasps_coin_1:
                CanTeamAttack,
            Locations.kreeping_klasps_bananas_1:
                CanSwim | CanClimb,
            Locations.kreeping_klasps_balloon_2:
                CanClimb | (CanSwim & HasBothKongs),
            Locations.kreeping_klasps_bananas_2:
                CanSwim | CanClimb,
            Locations.kreeping_klasps_coin_2:
                CanClimb & CanHover,

            Locations.tracker_barrel_trek_clear:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_bonus_1:
                HasBarrelTracker & HasBarrelCannon & CanHover,
            Locations.tracker_barrel_trek_bonus_2:
                HasBarrelTracker & HasBarrelCannon & (HasEllie | HasBothKongs),
            Locations.tracker_barrel_trek_dk_coin:
                HasBarrelTracker & HasBarrelCannon & HasEllie & CanCarry,
            Locations.tracker_barrel_trek_kong:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_1:
                True_(),
            Locations.tracker_barrel_trek_coin_2:
                HasBarrelTracker | CanHover | CanSpin,
            Locations.tracker_barrel_trek_bananas_1:
                HasBarrelTracker | (HasBarrelCannon & (CanHover | (CanSpin & HasBothKongs))),
            Locations.tracker_barrel_trek_balloon_1:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_3:
                HasBarrelTracker & HasBarrelCannon,
            Locations.tracker_barrel_trek_coin_4:
                HasBarrelTracker & HasBarrelCannon,

            Locations.fish_food_frenzy_clear:
                CanSwim,
            Locations.fish_food_frenzy_bonus_1:
                CanSwim,
            Locations.fish_food_frenzy_bonus_2:
                CanSwim,
            Locations.fish_food_frenzy_dk_coin:
                CanSwim & CanTeamAttack & CanCarry,
            Locations.fish_food_frenzy_kong:
                CanSwim,
            Locations.fish_food_frenzy_coin_1:
                True_(),
            Locations.fish_food_frenzy_bananas_1:
                CanSwim,
            Locations.fish_food_frenzy_coin_2:
                CanSwim,
                
            Locations.squirt_showdown_clear:
                HasEllie,
            Locations.defeated_squirt:
                HasEllie,

            Locations.fireball_frenzy_clear:
                CanClimb,
            Locations.fireball_frenzy_bonus_1:
                CanClimb & HasSquitter,
            Locations.fireball_frenzy_bonus_2:
                CanClimb & (CanTeamAttack | HasBothKongs),
            Locations.fireball_frenzy_dk_coin:
                CanClimb & CanCarry,
            Locations.fireball_frenzy_kong:
                CanClimb,
            Locations.fireball_frenzy_coin_1:
                True_(),
            Locations.fireball_frenzy_coin_2:
                CanTeamAttack | HasSquitter,
            Locations.fireball_frenzy_bananas_1:
                CanClimb,
            Locations.fireball_frenzy_coin_3:
                CanClimb,
            Locations.fireball_frenzy_bananas_2:
                CanClimb,
            Locations.fireball_frenzy_coin_4:
                CanClimb & HasSquitter,
            Locations.fireball_frenzy_coin_5:
                CanClimb,
            Locations.fireball_frenzy_bananas_3:
                CanClimb,

            Locations.demolition_drain_pipe_clear:
                HasBarrelCannon,
            Locations.demolition_drain_pipe_bonus_1:
                True_(),
            Locations.demolition_drain_pipe_bonus_2:
                HasBarrelCannon,
            Locations.demolition_drain_pipe_dk_coin:
                HasBarrelCannon & CanCarry,
            Locations.demolition_drain_pipe_kong:
                True_(),
            Locations.demolition_drain_pipe_coin_1:
                True_(),
            Locations.demolition_drain_pipe_bananas_1:
                True_(),
            Locations.demolition_drain_pipe_coin_2:
                True_(),
            Locations.demolition_drain_pipe_bananas_2:
                True_(),
            Locations.demolition_drain_pipe_coin_3:
                True_(),
            Locations.demolition_drain_pipe_bananas_3:
                True_(),
            Locations.demolition_drain_pipe_coin_4:
                True_(),
            Locations.demolition_drain_pipe_bananas_4:
                True_(),
            Locations.demolition_drain_pipe_bananas_5:
                True_(),
            Locations.demolition_drain_pipe_bananas_6:
                True_(),
            Locations.demolition_drain_pipe_coin_5:
                True_(),
            Locations.demolition_drain_pipe_coin_6:
                True_(),
            Locations.demolition_drain_pipe_coin_7:
                True_(),
            Locations.demolition_drain_pipe_bananas_7:
                True_(),

            Locations.ripsaw_rage_clear:
                True_(),
            Locations.ripsaw_rage_bonus_1:
                CanCarry | HasBothKongs,
            Locations.ripsaw_rage_bonus_2:
                CanCarry & HasBarrelInvincible,
            Locations.ripsaw_rage_dk_coin:
                CanCarry & HasBarrelInvincible & HasBarrelCannon,
            Locations.ripsaw_rage_kong:
                True_(),
            Locations.ripsaw_rage_coin_1:
                CanCarry | HasBothKongs,
            Locations.ripsaw_rage_bananas_1:
                True_(),
            Locations.ripsaw_rage_coin_2:
                True_(),
            Locations.ripsaw_rage_bananas_2:
                True_(),
            Locations.ripsaw_rage_coin_3:
                CanSpin | HasBothKongs,
            Locations.ripsaw_rage_bananas_3:
                True_(),
            #Locations.ripsaw_rage_coin_4:
            #    True_(),
            Locations.ripsaw_rage_bananas_4:
                True_(),

            Locations.blazing_bazukas_clear:
                HasBarrelCannon & CanClimb & (HasSquitter | HasBarrelSwitch | CanTeamAttack | CanHover),
            Locations.blazing_bazukas_bonus_1:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_bonus_2:
                HasBarrelCannon & CanClimb & (HasSquitter | HasBarrelSwitch | CanTeamAttack) & CanHover,
            Locations.blazing_bazukas_dk_coin:
                HasBarrelCannon & CanClimb & HasBarrelSwitch & (HasSquitter | CanHover),
            Locations.blazing_bazukas_kong:
                HasBarrelCannon & CanClimb & (HasSquitter | CanTeamAttack),
            Locations.blazing_bazukas_coin_1:
                HasBarrelCannon & CanClimb,
            Locations.blazing_bazukas_coin_2:
                HasBarrelCannon & CanClimb,
            Locations.blazing_bazukas_bananas_1:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_coin_3:
                HasBarrelCannon & CanClimb & HasSquitter,
            Locations.blazing_bazukas_bananas_2:
                HasBarrelCannon & CanClimb & (HasSquitter | HasBarrelSwitch | CanHover | CanTeamAttack),
            Locations.blazing_bazukas_bananas_3:
                HasBarrelCannon & CanClimb & (HasSquitter | HasBarrelSwitch | CanHover | CanTeamAttack),
            Locations.blazing_bazukas_coin_4:
                HasBarrelCannon & CanClimb & (HasSquitter | HasBarrelSwitch | CanHover | CanTeamAttack),
            Locations.blazing_bazukas_balloon_1:
                HasBarrelCannon & CanClimb & (HasSquitter | HasBarrelSwitch | CanHover | CanTeamAttack),

            Locations.low_g_labyrinth_clear:
                HasSquawks,
            Locations.low_g_labyrinth_bonus_1:
                HasSquawks | CanTeamAttack | HasBothKongs,
            Locations.low_g_labyrinth_bonus_2:
                HasSquawks,
            Locations.low_g_labyrinth_dk_coin:
                HasSquawks & CanCarry,
            Locations.low_g_labyrinth_kong:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_1:
                True_(),
            Locations.low_g_labyrinth_coin_1:
                True_(),
            Locations.low_g_labyrinth_bananas_2:
                True_(),
            Locations.low_g_labyrinth_coin_2:
                HasSquawks | HasBothKongs,
            Locations.low_g_labyrinth_bananas_3:
                HasSquawks,
            Locations.low_g_labyrinth_balloon_1:
                HasSquawks,
            Locations.low_g_labyrinth_coin_3:
                HasSquawks,
            Locations.low_g_labyrinth_coin_4:
                HasSquawks,
            Locations.low_g_labyrinth_coin_5:
                HasSquawks,
            Locations.low_g_labyrinth_coin_6:
                HasSquawks,
            Locations.low_g_labyrinth_coin_7:
                HasSquawks,
            Locations.low_g_labyrinth_bananas_4:
                HasSquawks,
                
            Locations.kaos_karnage_clear:
                True_(),
            Locations.defeated_kaos:
                True_(),

            Locations.krevice_kreepers_clear:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bonus_1:
                CanClimb & (HasBarrelCannon | HasBothKongs),
            Locations.krevice_kreepers_bonus_2:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_dk_coin:
                CanClimb & CanCarry,
            Locations.krevice_kreepers_kong:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_1:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_2:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_bananas_3:
                CanClimb & CanTeamAttack & HasBarrelCannon,
            Locations.krevice_kreepers_coin_1:
                CanClimb,
            Locations.krevice_kreepers_bananas_4:
                CanClimb,
            Locations.krevice_kreepers_coin_2:
                CanClimb & CanTeamAttack,
            Locations.krevice_kreepers_balloon_1:
                CanClimb,
            Locations.krevice_kreepers_coin_3:
                CanClimb & (CanTeamAttack | CanCarry),
            Locations.krevice_kreepers_coin_4:
                CanClimb & HasBarrelCannon,
            Locations.krevice_kreepers_coin_5:
                CanClimb & HasBarrelCannon & CanTeamAttack,
            Locations.krevice_kreepers_coin_6:
                CanClimb & HasBarrelCannon & CanTeamAttack,

            Locations.tearaway_toboggan_clear:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bonus_1:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bonus_2:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_dk_coin:
                (HasBarrelCannon | CanHover) & CanCarry,
            Locations.tearaway_toboggan_kong:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_coin_1:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_1:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_coin_2:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_coin_3:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_2:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_coin_4:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_3:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_balloon_1:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_coin_5:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_coin_6:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_4:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_5:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_6:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_bananas_7:
                HasBarrelCannon | CanHover,
            Locations.tearaway_toboggan_balloon_2:
                (HasBarrelCannon | CanHover) & (CanTeamAttack | CanSpin),

            Locations.barrel_drop_bounce_clear:
                HasBarrelWaterfall & HasBarrelCannon,
            Locations.barrel_drop_bounce_bonus_1:
                HasBarrelWaterfall & HasBarrelCannon,
            Locations.barrel_drop_bounce_bonus_2:
                HasBarrelWaterfall & HasBarrelCannon & CanHover,
            Locations.barrel_drop_bounce_dk_coin:
                CanCarry & (CanHover | (HasBarrelCannon & (CanSpin | HasBarrelWaterfall | CanTeamAttack))),
            Locations.barrel_drop_bounce_kong:
                HasBarrelWaterfall & HasBarrelCannon & (CanCarry | CanTeamAttack),
            Locations.barrel_drop_bounce_coin_1:
                HasBarrelWaterfall | CanTeamAttack,
            Locations.barrel_drop_bounce_coin_2:
                HasBarrelWaterfall & HasBarrelCannon & (CanHover | CanSpin),
            Locations.barrel_drop_bounce_balloon_1:
                HasBarrelWaterfall & HasBarrelCannon & HasParry,

            Locations.krackshot_krock_clear:
                HasSquitter,
            Locations.krackshot_krock_bonus_1:
                HasSquitter,
            Locations.krackshot_krock_bonus_2:
                HasSquitter,
            Locations.krackshot_krock_dk_coin:
                HasSquitter & CanCarry,
            Locations.krackshot_krock_kong:
                HasSquitter,
            Locations.krackshot_krock_coin_1:
                CanTeamAttack | HasSquitter,
            Locations.krackshot_krock_coin_2:
                CanTeamAttack | HasSquitter,
            Locations.krackshot_krock_balloon_1:
                HasSquitter | (CanTeamAttack & (CanHover | CanSpin)),
            Locations.krackshot_krock_bananas_1:
                HasSquitter,
            Locations.krackshot_krock_bananas_2:
                HasSquitter,
            Locations.krackshot_krock_coin_3:
                HasSquitter,
            Locations.krackshot_krock_bananas_3:
                HasSquitter,
            Locations.krackshot_krock_coin_4:
                HasSquitter,
            Locations.krackshot_krock_coin_5:
                HasSquitter,
            Locations.krackshot_krock_bananas_3:
                HasSquitter,
            Locations.krackshot_krock_bananas_4:
                HasSquitter,
            Locations.krackshot_krock_bananas_5:
                HasSquitter,

            Locations.lemguin_lunge_clear:
                True_(),
            Locations.lemguin_lunge_bonus_1:
                CanTeamAttack,
            Locations.lemguin_lunge_bonus_2:
                True_(),
            Locations.lemguin_lunge_dk_coin:
                CanCarry,
            Locations.lemguin_lunge_kong:
                True_(),
            Locations.lemguin_lunge_coin_1:
                True_(),
            Locations.lemguin_lunge_bananas_1:
                True_(),
            Locations.lemguin_lunge_coin_2:
                True_(),
                
            Locations.bleaks_house_clear:
                True_(),
            Locations.defeated_bleak:
                True_(),

            Locations.buzzer_barrage_clear:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bonus_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bonus_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_dk_coin:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_kong:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_1:
                CanTeamAttack,
            Locations.buzzer_barrage_coin_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_1:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_4:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_5:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_6:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_bananas_7:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_4:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_5:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_2:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_balloon_3:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_6:
                CanTeamAttack & HasSquawks,
            Locations.buzzer_barrage_coin_7:
                CanTeamAttack & HasSquawks,

            Locations.kongfused_cliffs_clear:
                CanClimb & (HasBarrelCannon | (HasBothKongs & CanHover)),
            Locations.kongfused_cliffs_bonus_1:
                CanClimb & HasBarrelCannon,
            Locations.kongfused_cliffs_bonus_2:
                CanClimb & (HasBarrelCannon | (HasBothKongs & CanHover)),
            Locations.kongfused_cliffs_dk_coin:
                CanClimb & CanCarry & (HasBarrelCannon | (HasBothKongs & CanHover)),
            Locations.kongfused_cliffs_kong:
                CanClimb & (HasBarrelCannon | (HasBothKongs & CanHover)),
            Locations.kongfused_cliffs_coin_1:
                CanClimb,
            Locations.kongfused_cliffs_coin_2:
                CanClimb,
            Locations.kongfused_cliffs_coin_3:
                CanClimb,
            Locations.kongfused_cliffs_coin_4:
                CanClimb & (HasBarrelCannon | (HasBothKongs & (CanHover | CanSpin))),
            Locations.kongfused_cliffs_coin_5:
                CanClimb & (HasBarrelCannon | (HasBothKongs & (CanHover | CanSpin))),
            Locations.kongfused_cliffs_bananas_1:
                CanClimb & (HasBarrelCannon | (HasBothKongs & CanHover)),
            Locations.kongfused_cliffs_bananas_2:
                CanClimb & (HasBarrelCannon | (HasBothKongs & CanHover)),

            Locations.floodlit_fish_clear:
                (CanSwim | HasEnguarde) & HasBarrelCannon,
            Locations.floodlit_fish_bonus_1:
                CanSwim | HasEnguarde,
            Locations.floodlit_fish_bonus_2:
                (CanSwim & HasBothKongs) | HasEnguarde,
            Locations.floodlit_fish_dk_coin:
                (CanSwim | HasEnguarde) & HasBarrelCannon & CanCarry,
            Locations.floodlit_fish_kong:
                HasEnguarde,
            Locations.floodlit_fish_bananas_1:
                CanSwim | HasEnguarde,
            Locations.floodlit_fish_bananas_2:
                CanSwim | HasEnguarde,
            Locations.floodlit_fish_coin_1:
                CanSwim | HasEnguarde,
            Locations.floodlit_fish_bananas_3:
                CanSwim | HasEnguarde,
            Locations.floodlit_fish_bananas_4:
                CanSwim | HasEnguarde,
            Locations.floodlit_fish_coin_2:
                HasEnguarde,
            Locations.floodlit_fish_bananas_5:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_6:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_coin_3:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_7:
                CanSwim & HasEnguarde,
            Locations.floodlit_fish_bananas_8:
                HasEnguarde,

            Locations.pot_hole_panic_clear:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim & (HasEllie | CanTeamAttack | CanSpin) & HasBarrelCannon,
            Locations.pot_hole_panic_bonus_1:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim & HasEllie,
            Locations.pot_hole_panic_bonus_2:
               (HasSquawks | (CanSpin & CanHover)) & CanSwim & (HasEllie | CanTeamAttack | CanSpin) & HasBarrelCannon & HasSquitter,
            Locations.pot_hole_panic_dk_coin:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim & CanTeamAttack & HasBarrelCannon & CanCarry,
            Locations.pot_hole_panic_kong:
                (HasSquawks | ((CanSpin & CanHover) & CanTeamAttack)) & CanSwim & HasEllie & HasBarrelCannon,
            Locations.pot_hole_panic_bananas_1:
                (HasSquawks | (CanSpin & CanHover & CanTeamAttack)),
            Locations.pot_hole_panic_bananas_2:
                (HasSquawks | (CanSpin & CanHover & CanTeamAttack)),
            Locations.pot_hole_panic_coin_1:
                (HasSquawks | (CanSpin & CanHover)),
            Locations.pot_hole_panic_bananas_3:
                (HasSquawks | (CanSpin & CanHover)),
            Locations.pot_hole_panic_bananas_4:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim & HasEnguarde,
            Locations.pot_hole_panic_bananas_5:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_bananas_6:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_bananas_7:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_bananas_8:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_coin_2:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_coin_3:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_bananas_9:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_coin_4:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim,
            Locations.pot_hole_panic_bananas_10:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim & (HasEllie | CanTeamAttack | CanSpin) & HasBarrelCannon,
            Locations.pot_hole_panic_bananas_11:
                (HasSquawks | (CanSpin & CanHover)) & CanSwim & (HasEllie | CanTeamAttack | CanSpin) & HasBarrelCannon & HasSquitter,

            Locations.ropey_rumpus_clear:
                CanClimb,
            Locations.ropey_rumpus_bonus_1:
                CanClimb & CanCarry,
            Locations.ropey_rumpus_bonus_2:
                CanClimb & HasParry,
            Locations.ropey_rumpus_dk_coin:
                CanClimb & CanCarry,
            Locations.ropey_rumpus_kong:
                CanClimb,
            Locations.ropey_rumpus_coin_1:
                CanTeamAttack,
            Locations.ropey_rumpus_coin_2:
                CanTeamAttack,
            Locations.ropey_rumpus_bananas_1:
                (CanClimb | ((CanSpin | CanHover) & CanTeamAttack)) & CanCarry,
            Locations.ropey_rumpus_coin_3:
                CanClimb,
            Locations.ropey_rumpus_bananas_2:
                CanClimb,
            Locations.ropey_rumpus_coin_4:
                CanClimb,
            Locations.ropey_rumpus_coin_5:
                CanClimb,
            Locations.ropey_rumpus_bananas_3:
                CanClimb,
            Locations.ropey_rumpus_coin_6:
                CanClimb,
            Locations.ropey_rumpus_coin_7:
                CanClimb,
            Locations.ropey_rumpus_bananas_4:
                CanClimb,
            Locations.ropey_rumpus_balloon_1:
                CanClimb,
            Locations.ropey_rumpus_bananas_5:
                CanClimb,
            Locations.ropey_rumpus_bananas_6:
                CanClimb,
            Locations.ropey_rumpus_bananas_7:
                CanClimb,
            Locations.ropey_rumpus_bananas_8:
                CanClimb,
            Locations.ropey_rumpus_bananas_9:
                CanClimb & HasBarrelCannon & (CanTeamAttack | HasParry),
            Locations.ropey_rumpus_balloon_2:
                CanClimb & HasBarrelCannon & (CanTeamAttack | HasParry),
            Locations.ropey_rumpus_coin_8:
                CanClimb & HasBarrelCannon & (CanTeamAttack | HasParry),
            Locations.ropey_rumpus_bananas_10:
                CanClimb & (HasParry | HasBothKongs),
                
            Locations.barbos_barrier_clear:
                CanSwim & HasEnguarde,
            Locations.defeated_barbos:
                CanSwim & HasEnguarde,

            Locations.konveyor_rope_klash_clear:
                CanClimb,
            Locations.konveyor_rope_klash_bonus_1:
                CanClimb,
            Locations.konveyor_rope_klash_bonus_2:
                CanClimb,
            Locations.konveyor_rope_klash_dk_coin:
                CanClimb & CanCarry,
            Locations.konveyor_rope_klash_kong:
                CanClimb,
            Locations.konveyor_rope_klash_coin_1:
                CanClimb | CanTeamAttack,
            Locations.konveyor_rope_klash_coin_2:
                CanClimb | (HasBothKongs & CanHover),
            Locations.konveyor_rope_klash_coin_3:
                CanClimb | (HasBothKongs & CanHover & CanCarry),
            Locations.konveyor_rope_klash_balloon_1:
                CanClimb,
            Locations.konveyor_rope_klash_balloon_2:
                CanClimb & CanTeamAttack,

            Locations.creepy_caverns_clear:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_bonus_1:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_bonus_2:
                HasBarrelGhost & HasBarrelCannon & ((CanCarry & CanTeamAttack) | HasBothKongs) & HasSquitter,
            Locations.creepy_caverns_dk_coin:
                HasBarrelGhost & HasBarrelCannon & CanCarry,
            Locations.creepy_caverns_kong:
                HasBarrelGhost & HasBarrelCannon,

            Locations.creepy_caverns_bananas_1:
                True_(),
            Locations.creepy_caverns_coin_1:
                ((HasBarrelGhost & HasBarrelCannon) | (CanCarry)) & CanTeamAttack,
            Locations.creepy_caverns_coin_2:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_coin_3:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,
            Locations.creepy_caverns_bananas_2:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_coin_4:
                HasBarrelGhost & HasBarrelCannon & ((CanCarry & CanTeamAttack) | HasBothKongs) & HasSquitter,
            Locations.creepy_caverns_coin_5:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_coin_6:
                HasBarrelGhost & HasBarrelCannon,
            Locations.creepy_caverns_balloon_1:
                HasBarrelGhost & HasBarrelCannon & CanTeamAttack,

            Locations.lightning_look_out_clear:
                CanSwim | (HasBothKongs & CanCarry),
            Locations.lightning_look_out_bonus_1:
                CanSwim,
            Locations.lightning_look_out_bonus_2:
                CanCarry & (CanSwim | HasBothKongs),
            Locations.lightning_look_out_dk_coin:
                CanCarry & (CanSwim | CanHover | CanWaterBounce),
            Locations.lightning_look_out_kong:
                CanSwim | (HasBothKongs & CanCarry),
            Locations.lightning_look_out_balloon_1:
                CanTeamAttack | HasBothKongs,
            Locations.lightning_look_out_coin_1:
                CanTeamAttack,
            Locations.lightning_look_out_coin_2:
                CanTeamAttack | HasBothKongs,
            Locations.lightning_look_out_bananas_1:
                True_(),
            Locations.lightning_look_out_coin_3:
                (CanSwim | CanHover | CanWaterBounce) & (CanTeamAttack | HasBothKongs),
            Locations.lightning_look_out_balloon_2:
                CanSwim | (HasBothKongs & CanCarry) & CanTeamAttack,

            Locations.koindozer_klamber_clear:
                CanClimb | CanHover | CanSpin,
            Locations.koindozer_klamber_bonus_1:
                CanClimb | ((CanHover | CanSpin) & CanTeamAttack),
            Locations.koindozer_klamber_bonus_2:
                CanClimb | CanHover | CanSpin,
            Locations.koindozer_klamber_dk_coin:
                CanClimb & HasBarrelSwitch,
            Locations.koindozer_klamber_kong:
                CanClimb | ((CanHover | CanSpin) & CanTeamAttack),
            Locations.koindozer_klamber_coin_1:
                CanClimb | CanHover | CanSpin,
            Locations.koindozer_klamber_coin_2:
                (CanClimb | CanHover | CanSpin) & CanTeamAttack,
            Locations.koindozer_klamber_coin_3:
                (CanClimb | CanHover | CanSpin),
            Locations.koindozer_klamber_bananas_1:
                CanClimb | CanHover | CanSpin,
            Locations.koindozer_klamber_balloon_1:
                (CanClimb | CanHover | CanSpin) & CanTeamAttack,

            Locations.poisonous_pipeline_clear:
                CanSwim,
            Locations.poisonous_pipeline_bonus_1:
                CanSwim & HasEnguarde,
            Locations.poisonous_pipeline_bonus_2:
                CanSwim,
            Locations.poisonous_pipeline_dk_coin:
                CanSwim & CanCarry,
            Locations.poisonous_pipeline_kong:
                CanSwim,
            Locations.poisonous_pipeline_coin_1:
                CanSwim,
            Locations.poisonous_pipeline_bananas_1:
                CanSwim,
            Locations.poisonous_pipeline_bananas_2:
                CanSwim,
            Locations.poisonous_pipeline_coin_2:
                CanSwim,
            Locations.poisonous_pipeline_balloon_1:
                CanSwim & HasEnguarde,
                
            Locations.kastle_kaos_clear:
                CanCarry,
            Locations.defeated_krool_castle:
                CanCarry,

            Locations.stampede_sprint_clear:
                CanHover & HasEllie & HasBarrelCannon,
            Locations.stampede_sprint_bonus_1:
                CanTeamAttack & HasSquitter,
            Locations.stampede_sprint_bonus_2:
                CanTeamAttack & HasSquawks,
            Locations.stampede_sprint_bonus_3:
                CanHover & HasEllie & HasBarrelCannon & HasParry,
            Locations.stampede_sprint_dk_coin:
                CanHover & HasEllie & HasBarrelCannon & CanCarry,
            Locations.stampede_sprint_kong:
                CanHover & HasEllie & HasBarrelCannon & CanTeamAttack & HasSquitter,
            Locations.stampede_sprint_coin_1:
                CanHover & HasEllie & HasBarrelCannon & HasParry,
            Locations.stampede_sprint_coin_2:
                CanHover & HasEllie & HasBarrelCannon & (HasParry | CanTeamAttack),

            Locations.criss_kross_cliffs_clear:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_bonus_1:
                True_(),
            Locations.criss_kross_cliffs_bonus_2:
                HasBarrelSwitch & CanTeamAttack & (HasBarrelCannon | CanClimb),
            Locations.criss_kross_cliffs_dk_coin:
                HasBarrelSwitch & (HasBarrelCannon | (CanTeamAttack & CanClimb)),
            Locations.criss_kross_cliffs_kong:
                CanTeamAttack & HasBarrelSwitch & (HasBarrelCannon | CanClimb),
            Locations.criss_kross_cliffs_bananas_1:
                True_(),
            Locations.criss_kross_cliffs_coin_1:
                HasBarrelSwitch & (HasBarrelCannon | CanTeamAttack),
            Locations.criss_kross_cliffs_bananas_2:
                HasBarrelSwitch & (HasBarrelCannon | CanTeamAttack),
            Locations.criss_kross_cliffs_coin_2:
                HasBarrelSwitch & (HasBarrelCannon | (CanTeamAttack & CanClimb)),
            Locations.criss_kross_cliffs_coin_3:
                HasBarrelSwitch & CanTeamAttack & (HasBarrelCannon | CanClimb),
            Locations.criss_kross_cliffs_coin_4:
                HasBarrelSwitch & CanTeamAttack & (HasBarrelCannon | CanClimb),
            Locations.criss_kross_cliffs_bananas_3:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_balloon_1:
                HasBarrelSwitch & HasBarrelCannon & CanClimb,
            Locations.criss_kross_cliffs_balloon_2:
                HasBarrelSwitch & HasBarrelCannon & CanClimb & CanTeamAttack,

            Locations.tyrant_twin_tussle_clear:
                True_(),
            Locations.tyrant_twin_tussle_bonus_1:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_bonus_2:
                CanTeamAttack & HasBarrelCannon,
            Locations.tyrant_twin_tussle_bonus_3:
                True_(),
            Locations.tyrant_twin_tussle_dk_coin:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_kong:
                True_(),

            Locations.tyrant_twin_tussle_coin_1:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_balloon_1:
                CanSpin | HasBothKongs,
            Locations.tyrant_twin_tussle_balloon_2:
                CanTeamAttack,
            Locations.tyrant_twin_tussle_coin_2:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_bananas_1:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_coin_3:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_coin_4:
                CanTeamAttack & HasSquitter,
            Locations.tyrant_twin_tussle_bananas_2:
                CanTeamAttack | HasBothKongs,
            Locations.tyrant_twin_tussle_coin_5:
                HasBarrelCannon,
            Locations.tyrant_twin_tussle_coin_6:
                HasBarrelCannon,
            Locations.tyrant_twin_tussle_bananas_3:
                HasBarrelCannon,


            Locations.swoopy_salvo_clear:
                HasSquawks & (HasBarrelCannon | CanTeamAttack) & CanClimb,
            Locations.swoopy_salvo_bonus_1:
                HasSquawks & ((HasBarrelCannon & (CanSpin | CanHover)) | CanTeamAttack),
            Locations.swoopy_salvo_bonus_2:
                HasSquawks,
            Locations.swoopy_salvo_bonus_3:
                HasSquawks & (HasBarrelCannon | CanTeamAttack) & CanClimb,
            Locations.swoopy_salvo_dk_coin:
                HasSquawks & CanCarry,
            Locations.swoopy_salvo_kong:
                HasSquawks & (HasBarrelCannon | CanTeamAttack) & CanClimb,
            Locations.swoopy_salvo_bananas_1:
                HasSquawks,
            Locations.swoopy_salvo_coin_1:
                HasSquawks,
            Locations.swoopy_salvo_bananas_2:
                HasSquawks,

            Locations.rocket_rush_clear:
                True_(),
            Locations.rocket_rush_dk_coin:
                CanCarry,
            Locations.rocket_rush_bananas_1:
                True_(),
            Locations.rocket_rush_coin_1:
                True_(),
            Locations.rocket_rush_bananas_2:
                True_(),
            Locations.rocket_rush_bananas_3:
                True_(),
            Locations.rocket_rush_coin_2:
                True_(),
            Locations.rocket_rush_coin_3:
                True_(),
            Locations.rocket_rush_coin_4:
                True_(),
                
            Locations.knautilus_clear:
                CanCarry,
            Locations.defeated_krool_knautilus:
                CanCarry,
            
        }


    def set_dkc3_rules(self) -> None:
        super().set_dkc3_rules()

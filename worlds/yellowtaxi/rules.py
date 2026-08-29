from __future__ import annotations

import math
from typing import TYPE_CHECKING, Callable, Mapping, Union, override, ClassVar

from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from .data_loader import regions_json_data
from BaseClasses import CollectionState, MultiWorld
from worlds.generic.Rules import add_rule, set_rule
from rule_builder.rules import Rule, True_, False_, Has, CanReachRegion, CanReachLocation
from .options import ShuffleFullGame, PizzaWheels, ShuffleGlide, IncludeOutOfBounds, LockedMoriosLab, \
    LockedMoriosWardrobe, OpenGrannysIsland

if TYPE_CHECKING:
    from .world import YellowTaxiWorld


def set_all_rules(world: YellowTaxiWorld) -> None:
    # In order for AP to generate an item layout that is actually possible for the player to complete,
    # we need to define rules for our Entrances and Locations.
    # Note: Regions do not have rules, the Entrances connecting them do!
    # We'll do entrances first, then locations, and then finally we set our victory condition.
    rf = RuleFactory(world)
    set_all_entrance_location_rules(world, rf)
    set_completion_condition(world)


def set_all_entrance_location_rules(world: YellowTaxiWorld, rf: RuleFactory) -> None:
    for region in world.get_regions():
        region_name = region.name
        if region_name == "Menu": # Menu doesn't have json data or any rules
            continue
        reg = regions_json_data[region_name]

        if world.options.shuffle_flip_o_will.value == world.options.shuffle_flip_o_will.option_per_level:
            if reg["level"] == "Crash Test Industries":
                rf.move_prefix = ""
            else:
                rf.move_prefix = "Progressive "

            if reg["level"].endswith("!"):
                rf.move_suffix = " (Time Trials)"
            else:
                rf.move_suffix = f" ({reg["level"]})"

        # Basic connections
        if "connections" in reg.keys():
            for connect, rule in reg["connections"].items():
                if rule:
                    rf.assign_connection_rule(region_name, connect, rule)

        # Subwarps
        if "subwarps" in reg.keys():
            for subwarp, connect_and_rule in reg["subwarps"].items():
                rule = connect_and_rule[1]
                if rule:
                    rf.assign_entrance_rule(subwarp, rule)

        # Warps
        if "warps" in reg.keys():
            for warp, connect_and_rule in reg["warps"].items():
                rule = connect_and_rule[1]
                if rule:
                    rf.assign_entrance_rule(warp, rule)

        # Mori-O-Trons. Only need rules on UT, as they aren't added at all unless important
        if world.using_ut and "moriotrons" in reg.keys():
            for moriotron in reg["moriotrons"].keys():
                rf.assign_entrance_rule(moriotron, "X2")

        # Cheeses
        if world.options.cheesesanity and "cheeses" in reg.keys():
            for cheese in reg["cheeses"]:
                try:
                    cheese_loc = world.get_location(cheese)
                    world.set_rule(cheese_loc, Has("Michele"))
                except KeyError:
                    break # If cheese doesn't exist here, region has no items

        # Special rules
        if "specialrules" in reg.keys():
            for location, rule in reg["specialrules"].items():
                rf.assign_location_rule(location, rule)

def set_completion_condition(world: YellowTaxiWorld) -> None:
    world.multiworld.completion_condition[world.player] = lambda state: state.has("Victory", world.player)


# Shamelessly copying SM64's rule factory implementation
class RuleFactory:
    world: YellowTaxiWorld

    class YTGVLogicException(Exception):
        pass

    def __init__(self, world: YellowTaxiWorld):
        self.world = world
        self.move_prefix = "Progressive "
        self.move_suffix = ""
        self.skip_unnecessary_rule_calculations = not self.world.using_ut
        self.cached_complex_rules : dict[str, Rule] = {}

    def assign_location_rule(self, target_name: str, rule_expr: str):
        try:
            target = self.world.get_location(target_name)
        except KeyError:
            return
        try:
            rule = self.build_rule(rule_expr)
        except RuleFactory.YTGVLogicException as exception:
            raise RuleFactory.YTGVLogicException(
                f"Error generating rule for {target_name} using rule expression {rule_expr}: {exception}")
        if rule is not None:
            self.world.set_rule(target, rule)

    def assign_connection_rule(self, region_from: str, region_to: str, rule_expr: str):
        self.assign_entrance_rule(f"{region_from} -> {region_to}", rule_expr)

    def assign_entrance_rule(self, entrance_name: str, rule_expr: str):
        if rule_expr is None or rule_expr == "":
            return
        try:
            target = self.world.get_entrance(entrance_name)
        except KeyError:
            return
        try:
            rule = self.build_rule(rule_expr)
        except RuleFactory.YTGVLogicException as exception:
            raise RuleFactory.YTGVLogicException(
                f"Error generating rule for {entrance_name} using rule expression {rule_expr}: {exception}")
        if rule is not None:
            self.world.set_rule(target, rule)

    def build_rule(self, rule_expr: str) -> Rule:
        expressions = rule_expr.split(" | ") if len(rule_expr) > 0 else []
        rule: Union[Rule | None] = None
        for expression in expressions:
            or_clause = self.combine_and_clauses(expression)
            if self.skip_unnecessary_rule_calculations and or_clause.Resolved.always_true:
                return True_()
            if rule is None:
                rule = or_clause
            else:
                rule |= or_clause
        if rule is None:
            return True_()
        return rule

    def combine_and_clauses(self, rule_expr: str) -> Rule:
        expressions = rule_expr.split(" & ")
        rule: Union[Rule | None] = None
        for expression in expressions:
            and_clause = self.evaluate_subclause(expression)
            if self.skip_unnecessary_rule_calculations and and_clause.Resolved.always_false:
                return False_()
            if rule is None:
                rule = and_clause
            else:
                rule &= and_clause
        if rule is None:
            return True_()
        return rule

    def evaluate_subclause(self, expression: str) -> Rule:
        if '+' in expression:
            tokens = expression.split('+')
            rule: Union[Rule | None] = None
            for token in tokens:
                and_clause = self.parse_token(token)
                if self.skip_unnecessary_rule_calculations and and_clause.Resolved.always_false:
                    return False_()
                if rule is None:
                    rule = and_clause
                else:
                    rule &= and_clause
            if rule is None:
                return True_()
            return rule
        if '/' in expression:
            tokens = expression.split('/')
            rule: Union[Rule | None] = None
            for token in tokens:
                or_clause = self.parse_token(token)
                if self.skip_unnecessary_rule_calculations and or_clause.Resolved.always_true:
                    return True_()
                if rule is None:
                    rule = or_clause
                else:
                    rule |= or_clause
            if rule is None:
                return True_()
            return rule
        if '{{' in expression:
            return CanReachLocation(expression[2:-2])
        if '{' in expression:
            return CanReachRegion(expression[1:-1])
        return self.parse_token(expression)

    def parse_token(self, token: str) -> Rule:
        if token == "B1":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has(f"{self.move_prefix}Boost{self.move_suffix}")
        if token == "B2":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has(f"{self.move_prefix}Boost{self.move_suffix}", 2)
        if token == "PMB": # Pac-man boost, overhead sections
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has(f"{self.move_prefix}Boost{self.move_suffix}")
        if token == "J1":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has(f"{self.move_prefix}Jump{self.move_suffix}")
        if token == "J2":
            if self.world.options.shuffle_flip_o_will == 0:
                return True_()
            return Has(f"{self.move_prefix}Jump{self.move_suffix}", 2)
        if token == "PMJ":
            if self.world.options.allow_top_down_jumps:
                return Has(f"{self.move_prefix}Jump{self.move_suffix}")
            return False_()
        if token == "GL":
            return Has("Glide",
                       options=[OptionFilter(ShuffleGlide, ShuffleGlide.option_true)],
                       filtered_resolution=True)
        if token == "SP":
            if not self.world.options.shuffle_spin_attack:
                return True_()
            return Has("Spin Attack")
        if token == "GS":
            if self.skip_unnecessary_rule_calculations and not self.world.has_golden_spring_access:
                return False_()
            return Has("Golden Spring Blueprints")
        if token == "GST":
            if self.world.options.shuffle_golden_spring == 0:
                return True_()
            return Has("Golden Spring Blueprints")
        if token == "Spike":
            if self.skip_unnecessary_rule_calculations and not self.world.has_spike_traversal:
                return False_()
            return Has("Golden Spring Blueprints") | Has("Pizza Wheels",
                                                     options=[
                                                         OptionFilter(PizzaWheels, PizzaWheels.option_progression)
                                                     ])
        if token == "SpikeT":
            if self.world.options.shuffle_golden_spring == 0:
                return True_()
            return Has("Golden Spring Blueprints") | Has("Pizza Wheels",
                                                     options=[
                                                         OptionFilter(PizzaWheels, PizzaWheels.option_progression)
                                                     ])
        if token == "PW":
            return Has("Pizza Wheels",
                       options=[OptionFilter(PizzaWheels, PizzaWheels.option_progression)])
        if token == "NOS":
            if self.world.has_orange_switch_access:
                return False_()
            return True_()
        # Non-shuffled orange switch, used to prevent impossible access rules
        if token == "NSOS":
            if self.world.options.shuffle_orange_switch:
                return False_()
            return True_()
        if token == "OS":
            if self.skip_unnecessary_rule_calculations and not self.world.has_orange_switch_access:
                return False_()
            return Has("Orange Switch")
        if token == "NGP":
            if not self.world.has_golden_propeller_access:
                return True_()
            return False_()
        if token == "GP":
            if self.skip_unnecessary_rule_calculations and not self.world.has_golden_propeller_access:
                return False_()
            return Has("Golden Propeller Blueprints")
        if token == "FGU":
            return Has("Full Game Unlock",
                       options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                       filtered_resolution=True)
        if token == "GelaToni":
            return Has("Gela-Toni")
        if token == "PizzaKing":
            return Has("Pizza King")
        if token == "Doggo":
            match self.world.options.fecal_matters_unlock_condition:
                case self.world.options.fecal_matters_unlock_condition.option_open:
                    return True_()
                case self.world.options.fecal_matters_unlock_condition.option_full_game:
                    return Has("Full Game Unlock",
                               options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                               filtered_resolution=True)
                case self.world.options.fecal_matters_unlock_condition.option_vanilla |\
                     self.world.options.fecal_matters_unlock_condition.option_shuffle_doggo:
                    return Has("Doggo")
                case self.world.options.fecal_matters_unlock_condition.option_exclude:
                    return False_()
        if token == "Password":
            if self.skip_unnecessary_rule_calculations and not self.world.has_password_access:
                return False_()
            return Has("Morio's Password")
        if token == "Rocket":
            if self.skip_unnecessary_rule_calculations and not self.world.has_rocket_access:
                return False_()
            if (self.world.options.rocket_unlock_condition.value ==
                    self.world.options.rocket_unlock_condition.option_open):
                return True_()
            return Has("Mosk's Rocket")
        if token == "PsychoTaxi":
            if (self.world.options.psycho_taxi_unlock_condition.value ==
                    self.world.options.psycho_taxi_unlock_condition.option_open):
                return True_()
            if (self.world.options.psycho_taxi_unlock_condition.value ==
                    self.world.options.psycho_taxi_unlock_condition.option_exclude):
                return False_()
            return Has("Psycho Taxi Cartridge")
        if token == "MorioHat":
            return Has("Morio Hat") | Has("Morio's Brain Hat")
        if token == "EmployeeHat":
            return Has("Tosla Employee Hat")
        if token == "MoskHat":
            return Has("Alien Mosk (Good) Hat") | Has("Bunny Hat")
        # Portals. TODO: Allow variable portal costs beyond just final portal
        if token == "PortalMorioHome":
            if (self.world.options.goal == self.world.options.goal.option_bombeach_boss
                    and self.world.level_order[0] == "Bombeach"):
                return Has("Gear", self.world.final_portal_cost)
            return Has("Gear", 3)
        if token == "PortalBombeach":
            if (self.world.options.goal == self.world.options.goal.option_bombeach_boss
                    and self.world.level_order[1] == "Bombeach"):
                return Has("Gear", self.world.final_portal_cost)
            return Has("Gear", 6)
        if token == "PortalArcadePanik":
            if self.world.options.demo_portal_mode != self.world.options.demo_portal_mode.option_basic:
                return Has("Gear", 18)
            return (Has("Gear", 18) &
                    Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True))
        if token == "PortalPizzaTime":
            if (self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_influencers or
                self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open):
                return Has("Gear", 32)
            return (Has("Gear", 32) &
                    Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True))
        if token == "PortalToslaOffices":
            if self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open:
                return Has("Gear", 50 if self.world.options.goal != self.world.options.goal.option_tosla_offices_boss
                           else self.world.final_portal_cost)
            return (Has("Gear", 50 if self.world.options.goal != self.world.options.goal.option_tosla_offices_boss
                        else self.world.final_portal_cost) &
                    Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True))
        if token == "PortalGymGears":
            return True_()
        if token == "PortalFecalMatters":
            return True_()
        if token == "PortalFlushedAway":
            return True_()
        if token == "PortalMauriziosCity":
            if self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open:
                return Has("Gear", 65 if self.world.options.goal != self.world.options.goal.option_help_maurizio
                           else self.world.final_portal_cost)
            return (Has("Gear", 65 if self.world.options.goal != self.world.options.goal.option_help_maurizio
                        else self.world.final_portal_cost) &
                    Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True))
        if token == "PortalCrashTestIndustries":
            if self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open:
                return Has("Gear", 80)
            return (Has("Gear", 80) &
                    Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True))
        if token == "PortalMoriosMind":
            if self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open:
                return True_()
            return Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True)
        if token == "PortalRuinedObservatory":
            if self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open:
                return True_()
            return Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True)
        if token == "PortalToslaHQ":
            if self.world.options.demo_portal_mode == self.world.options.demo_portal_mode.option_open:
                return Has("Gear", 130 if self.world.options.goal != 3 # self.world.options.goal.option_moon_boss
                           else self.world.final_portal_cost)
            return (Has("Gear", 130 if self.world.options.goal != 3 # self.world.options.goal.option_moon_boss
                        else self.world.final_portal_cost) &
                    Has("Full Game Unlock",
                        options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                        filtered_resolution=True))
        if token == "NPR":
            # No Portal randomization. Placeholder rule for now.
            return True_()
        if token == "NSAR":
            # No Subarea randomization. Placeholder rule for now.
            return True_()
        if token == "SAR":
            # Subarea randomization. Placeholder rule for now.
            return False_()
        # No Golden Propeller Smuggling
        if token == "NGPS":
            if not self.world.has_golden_propeller_access:
                return True_()
            # TODO: Golden propeller smuggling will not work on full ER!
            return False_()
        if token == "NHPR":
            # No Hub Portal randomization. Placeholder rule for now.
            # Hub portals launch you upwards when declining entry, making them logical access rules in some cases.
            if self.world.using_ut:
                return HubPortalBounce()
            return True_()
        if token == "OGI":
            if self.world.options.open_grannys_island:
                return True_()
            return False_()
        if token == "OOB": # Out-of-bounds
            if not self.world.options.include_out_of_bounds == self.world.options.include_out_of_bounds.option_full:
                return False_()
            # Fancy UT rule for printing purposes. Can skip as an optimization on actual gen
            if self.world.using_ut:
                return OutOfBounds()
            return True_()
        if token == "SCOOB": # Standard clip out-of-bounds. Requires less items on higher expert levels
            scoob_rule = False_()
            if f"SCOOB{self.move_suffix}" in self.cached_complex_rules:
                scoob_rule = self.cached_complex_rules[f"SCOOB{self.move_suffix}"]
            else:
                if (not self.world.options.include_out_of_bounds == self.world.options.include_out_of_bounds.option_full
                        or (not self.world.using_ut and self.world.options.expert_level <= 0)):
                    return False_()
                elif self.world.options.shuffle_flip_o_will == 0:
                    if self.world.options.expert_level <= 0:
                        scoob_rule = Has(self.world.glitches_item_name)
                    else:
                        scoob_rule = True_()
                else:
                    match self.world.options.expert_level:
                        case 0:
                            scoob_rule = False_()
                        case 1:
                            scoob_rule = (Has(f"{self.move_prefix}Boost{self.move_suffix}", 2) &
                                          Has(f"{self.move_prefix}Jump{self.move_suffix}"))
                        case 2:
                            scoob_rule = (Has(f"{self.move_prefix}Boost{self.move_suffix}") &
                                          Has(f"{self.move_prefix}Jump{self.move_suffix}"))
                        case _:
                            scoob_rule = (Has(f"{self.move_prefix}Boost{self.move_suffix}") |
                                          Has(f"{self.move_prefix}Jump{self.move_suffix}"))
                    if self.world.using_ut and self.world.options.expert_level < 3:
                        if self.world.options.expert_level <= 0:
                            scoob_rule |= (Has(f"{self.move_prefix}Boost{self.move_suffix}", 2) &
                                           Has(f"{self.move_prefix}Jump{self.move_suffix}") &
                                           Has(self.world.glitches_item_name))
                        if self.world.options.expert_level <= 1:
                            scoob_rule |= (Has(f"{self.move_prefix}Boost{self.move_suffix}") &
                                           Has(f"{self.move_prefix}Jump{self.move_suffix}") &
                                           Has(self.world.glitches_item_name, 2 - self.world.options.expert_level))
                        if self.world.options.expert_level <= 2:
                            scoob_rule |= ((Has(f"{self.move_prefix}Boost{self.move_suffix}") |
                                           Has(f"{self.move_prefix}Jump{self.move_suffix}")) &
                                           Has(self.world.glitches_item_name, 3 - self.world.options.expert_level))
                self.cached_complex_rules[f"SCOOB{self.move_suffix}"] = scoob_rule
            # Fancy UT rule for printing purposes. Can skip as an optimization on actual gen
            if self.world.using_ut:
                return scoob_rule & OutOfBounds()
            return scoob_rule
        if token == "LabKey":
            return Has("Lab Key",
                       options=[OptionFilter(LockedMoriosLab, LockedMoriosLab.option_true)],
                       filtered_resolution=True)
        if token == "WardrobeKey":
            return Has("Morio's Wardrobe",
                       options=[OptionFilter(LockedMoriosWardrobe, LockedMoriosWardrobe.option_true)],
                       filtered_resolution=True)
        if token == "GymKey":
            match self.world.options.gym_gears_unlock_condition:
                case self.world.options.gym_gears_unlock_condition.option_open:
                    return True_()
                case self.world.options.gym_gears_unlock_condition.option_full_game:
                    return Has("Full Game Unlock",
                               options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                               filtered_resolution=True)
                case self.world.options.gym_gears_unlock_condition.option_shuffle_gym_membership:
                    return Has("Gym Membership")
                case self.world.options.gym_gears_unlock_condition.option_exclude:
                    return False_()
        if token == "HatMembership":
            return True_()
        if token == "SewerKey":
            match self.world.options.flushed_away_unlock_condition:
                case self.world.options.flushed_away_unlock_condition.option_open:
                    return True_()
                case self.world.options.flushed_away_unlock_condition.option_full_game:
                    return Has("Full Game Unlock",
                               options=[OptionFilter(ShuffleFullGame, ShuffleFullGame.option_true)],
                               filtered_resolution=True)
                case self.world.options.flushed_away_unlock_condition.option_shuffle_sewer_key:
                    return Has("Sewer Key")
                case self.world.options.flushed_away_unlock_condition.option_exclude:
                    return False_()
        if token == "EarlySewer":
            if self.world.early_sewer_island:
                return True_()
            return False_()
        if token == "TT1":
            match self.world.options.locked_time_trials:
                case self.world.options.locked_time_trials.option_open:
                    return True_()
                case self.world.options.locked_time_trials.option_single_item:
                    return Has("Time Trial Remote")
                case self.world.options.locked_time_trials.option_split_items:
                    return Has("Time Trial Remote (Baby Steps!)")
                case self.world.options.locked_time_trials.option_progressive_items:
                    return Has("Progressive Time Trial Remote")
        if token == "TT2":
            match self.world.options.locked_time_trials:
                case self.world.options.locked_time_trials.option_open:
                    return True_()
                case self.world.options.locked_time_trials.option_single_item:
                    return Has("Time Trial Remote")
                case self.world.options.locked_time_trials.option_split_items:
                    return Has("Time Trial Remote (Getting Gud!)")
                case self.world.options.locked_time_trials.option_progressive_items:
                    return Has("Progressive Time Trial Remote", 2)
        if token == "TT3":
            match self.world.options.locked_time_trials:
                case self.world.options.locked_time_trials.option_open:
                    return True_()
                case self.world.options.locked_time_trials.option_single_item:
                    return Has("Time Trial Remote")
                case self.world.options.locked_time_trials.option_split_items:
                    return Has("Time Trial Remote (Pro Tricks!)")
                case self.world.options.locked_time_trials.option_progressive_items:
                    return Has("Progressive Time Trial Remote", 3)
        if token == "NHS":
            if self.world.options.hatsanity == 0:
                return True_()
            return False_()
        if token == "HS":
            if self.world.options.hatsanity != 0:
                return True_()
            return False_()
        if token.startswith("Bunny-"):
            bunny_level : str = token[len("Bunny-"):]
            if bunny_level == "Hub":
                hub_bunnies = 3
                if self.world.options.extra_demo_collectables:
                    hub_bunnies += 2
                if self.world.exclude_spike_bunny:
                    hub_bunnies -= 1
                if self.world.exclude_top_bunny:
                    hub_bunnies -= 1
                return Has("Bunny (Morio's Lab)", hub_bunnies)
            else:
                adjusted_bunny_level : str = bunny_level
                match bunny_level:
                    case "MH":
                        adjusted_bunny_level = "Morio's Home"
                    case "BB":
                        adjusted_bunny_level = "Bombeach"
                    case "AP":
                        adjusted_bunny_level = "Arcade Panik"
                    case "PT":
                        adjusted_bunny_level = "Pizza Time"
                    case "TO":
                        adjusted_bunny_level = "Tosla's Offices"
                    case "GG":
                        adjusted_bunny_level = "Gym Gears"
                    case "FM":
                        adjusted_bunny_level = "Fecal Matters"
                    case "FA":
                        adjusted_bunny_level = "Flushed Away"
                    case "MC":
                        adjusted_bunny_level = "Maurizio's City"
                    case "CTI":
                        adjusted_bunny_level = "Crash Test Industries"
                return Has(f"Bunny ({adjusted_bunny_level})", 3)
        if token.startswith("X"):
            expert_level = int(token[1:])
            if self.world.using_ut and self.world.options.expert_level < expert_level:
                return Has(self.world.glitches_item_name, expert_level - self.world.options.expert_level)
            if self.world.options.expert_level >= expert_level:
                return True_()
            return False_()

        raise Exception(f"Invalid token: '{token}'")

# Used for out-of-bounds stuff, really just to explain things better in UT
class OutOfBounds(Rule["YellowTaxiWorld"], game="Yellow Taxi Goes Vroom"):
    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return True

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [{"type": "color", "color": "green", "text": "Include Out-of-Bounds"}]

        @override
        def __str__(self) -> str:
            return "Include Out-of-Bounds"

# Used hub portal bounces, really just to explain things better in UT
class HubPortalBounce(Rule["YellowTaxiWorld"], game="Yellow Taxi Goes Vroom"):
    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return True

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            return [{"type": "color", "color": "green", "text": "Hub Portal Bounce"}]

        @override
        def __str__(self) -> str:
            return "Hub Portal Bounce"
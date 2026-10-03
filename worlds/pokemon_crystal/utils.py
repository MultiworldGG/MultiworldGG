import logging
from collections import defaultdict
from collections.abc import Mapping
from math import ceil
from typing import TYPE_CHECKING

from Options import OptionError, Toggle
from .data import data, StartingTown, RegionData, EncounterKey, EncounterType, LogicalAccess
from .item_data import START_INVENTORY_ENTRIES
from .items import item_const_name_to_label
from .mart_data import CUSTOM_MART_SLOT_NAMES
from .options import JohtoOnly, RandomizeBadges, UndergroundsRequirePower, Route3Access, VictoryRoadRequirement, \
    EliteFourRequirement, Goal, Route44AccessRequirement, BlackthornDarkCaveAccess, RedRequirement, \
    MtSilverRequirement, HMBadgeRequirements, RedGyaradosAccess, EarlyFly, RadioTowerRequirement, \
    BreedingMethodsRequired, Shopsanity, KantoTrainersanity, JohtoTrainersanity, RandomizePokemonRequests, \
    RandomizeTypes, RandomizeEvolution, RandomizeTrades, TradesRequired, MagnetTrainAccess, \
    Dexsanity, EncounterGrouping, SouthKantoAccess, SouthKantoCondition, LevelScaling, LockKantoGyms, \
    WildEncounterMethodsRequired, RemoveBadgeRequirement, SaffronGatehouseTea, PokemonSourceLogic, \
    RandomizePokedex, RandomizeLuckyNumberShow, VanillaEventChains, EvolutionMethodsRequired
from ..Files import APTokenTypes

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


def adjust_options(world: "PokemonCrystalWorld"):
    __adjust_option_problems(world)


def __adjust_option_problems(world: "PokemonCrystalWorld"):
    __adjust_options_randomize_entrances(world)
    __adjust_options_radio_tower_and_route_44(world)
    __adjust_options_victory_road_badges(world)
    __adjust_options_elite_four_badges(world)
    __adjust_options_goal(world)
    __adjust_options_johto_only(world)
    __adjust_options_restrictive_region_travel(world)
    __adjust_options_gyarados(world)
    __adjust_options_early_fly(world)
    __adjust_options_encounters_and_breeding(world)
    __adjust_options_race_mode(world)
    __adjust_options_pokemon_requests(world)
    __adjust_options_trades(world)
    __adjust_options_dark_areas(world)
    __adjust_options_randomize_types(world)
    __adjust_options_tm_plando(world)
    __adjust_options_traps(world)
    __adjust_options_mischief_bounds(world)
    __adjust_options_level_scaling(world)
    __adjust_options_level_curve_bounds(world)
    __adjust_options_fly_destination_rando(world)
    __adjust_options_start_time(world)
    __adjust_options_kinda_early_surf(world)
    __adjust_options_south_kanto_access(world)
    __adjust_options_lance_requires_elite_four(world)
    __adjust_options_vanilla_misty_chain(world)
    __adjust_options_coupled_plando_direction(world)


def __adjust_options_vanilla_misty_chain(world: "PokemonCrystalWorld"):
    # With vanilla badges the Cascade badge is Misty's own event, and regional HM badges make
    # Kanto Cut require it. The vanilla Misty chain then hides Misty behind the Power Plant/Cerulean
    # Rocket quest, whose approaches are Kanto-Cut-gated, so the Cascade badge would be required to
    # obtain itself. Drop the Misty chain to break the cycle.
    if (VanillaEventChains.MISTY in world.options.vanilla_event_chains.value
            and world.options.randomize_badges.value == RandomizeBadges.option_vanilla
            and world.options.hm_badge_requirements.value == HMBadgeRequirements.option_regional):
        world.options.vanilla_event_chains.value.discard(VanillaEventChains.MISTY)
        logging.warning(
            "Pokemon Crystal: The vanilla Misty event chain is incompatible with vanilla badges and "
            "regional HM badge requirements. Disabling the Misty event chain for player %s.",
            world.player_name)


def __adjust_options_coupled_plando_direction(world: "PokemonCrystalWorld"):
    # Coupling forces the return trip to mirror the way in, so a one-directional pairing has
    # no valid placement: the target left behind at the source can never be paired (its reverse
    # exit is already connected), and neither can the exit whose target the pairing consumed.
    if not (world.options.coupled_entrances and world.options.plando_connections):
        return
    one_way = [conn for conn in world.options.plando_connections.value if conn.direction != "both"]
    if not one_way:
        return
    world.options.plando_connections.value = [
        conn._replace(direction="both") for conn in world.options.plando_connections.value]
    logging.warning(
        "Pokemon Crystal: plando_connections direction '%s' is incompatible with Coupled Entrances. "
        "Forcing direction 'both' for %d pairing(s) for player %s.",
        one_way[0].direction, len(one_way), world.player_name)


def __adjust_options_lance_requires_elite_four(world: "PokemonCrystalWorld"):
    if world.options.lance_requires_elite_four and world.options.skip_elite_four:
        world.options.lance_requires_elite_four.value = 0
        logging.warning(
            "Pokemon Crystal: Lance Requires Elite Four is incompatible with Skip Elite Four. "
            "Disabling for player %s.",
            world.player_name)


def __adjust_options_south_kanto_access(world: "PokemonCrystalWorld"):
    if (world.options.south_kanto_access == SouthKantoAccess.option_both
            and world.options.south_kanto_condition != SouthKantoCondition.option_power_restored):
        world.options.south_kanto_access.value = SouthKantoAccess.option_route_19
        logging.warning(
            "Pokemon Crystal: South Kanto Access 'Both' requires South Kanto Condition 'Power Restored'. "
            "Changing South Kanto Access to Route 19 for player %s.",
            world.player_name)


def __adjust_options_randomize_entrances(world: "PokemonCrystalWorld"):
    if (world.options.randomize_entrances
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random):
        world.options.randomize_badges.value = RandomizeBadges.option_completely_random
        logging.warning(
            f"Pokemon Crystal: Entrance Randomization requires completely random badges. "
            f"Changing Randomize Badges to completely random for player {world.player} ({world.player_name}).")


def __adjust_options_kinda_early_surf(world: "PokemonCrystalWorld"):
    if world.options.kinda_early_surf and (
            world.options.randomize_starting_town
            or world.options.johto_only
            or world.options.randomize_entrances.value):
        world.options.kinda_early_surf.value = 0
        logging.warning(
            "Pokemon Crystal: Kinda Early Surf is incompatible with Randomize Starting Town, "
            "Johto Only, and Entrance Randomization. Disabling for player %s.",
            world.player_name)


def __adjust_options_radio_tower_and_route_44(world: "PokemonCrystalWorld"):
    if (world.options.randomize_badges.value != RandomizeBadges.option_completely_random
            and world.options.radio_tower_count.value > (7 if world.options.johto_only else 15)):
        world.options.radio_tower_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Radio Tower Count >%d incompatible with vanilla or shuffled badges. "
            "Changing Radio Tower Count to %d for player %s.",
            world.options.radio_tower_count.value,
            world.options.radio_tower_count.value,
            world.player_name)

    if (world.options.route_44_access_count.value > (7 if world.options.johto_only else 15)
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random):
        world.options.route_44_access_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Route 44 Access Count >%d incompatible with vanilla or shuffled badges. "
            "Changing Route 44 Access Count to %d for player %s.",
            world.options.route_44_access_count.value,
            world.options.route_44_access_count.value,
            world.player_name)

    if (world.options.route_44_access_requirement.value == Route44AccessRequirement.option_gyms
            and world.options.blackthorn_dark_cave_access.value == BlackthornDarkCaveAccess.option_vanilla
            and world.options.route_44_access_count.value > (7 if world.options.johto_only else 15)):
        world.options.route_44_access_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Route 44 Access Gyms >%d incompatible with vanilla Dark Cave. "
            "Changing Route 44 Access Gyms to %d for player %s.",
            world.options.route_44_access_count.value,
            world.options.route_44_access_count.value,
            world.player_name)

    if (world.options.radio_tower_requirement.value == RadioTowerRequirement.option_gyms
            and world.options.radio_tower_count.value > (7 if world.options.johto_only else 15)):
        world.options.radio_tower_count.value = 7 if world.options.johto_only else 15
        logging.warning(
            "Pokemon Crystal: Radio Tower Gyms >%d is impossible. "
            "Changing Radio Tower Gyms to %d for player %s.",
            world.options.radio_tower_count.value,
            world.options.radio_tower_count.value,
            world.player_name)


def __adjust_options_victory_road_badges(world: "PokemonCrystalWorld"):
    if (world.options.victory_road_requirement == VictoryRoadRequirement.option_johto_badges
            and world.options.victory_road_count > 8):
        world.options.victory_road_count.value = 8
        logging.warning(
            "Pokemon Crystal: Victory Road count cannot be greater than 8 if Victory Road requirement is Johto Badges. "
            "Changing Victory Road Count to 8 for player %s.",
            world.player_name)


def __adjust_options_elite_four_badges(world: "PokemonCrystalWorld"):
    if (world.options.elite_four_requirement == EliteFourRequirement.option_johto_badges
            and world.options.elite_four_count > 8):
        world.options.elite_four_count.value = 8
        logging.warning(
            "Pokemon Crystal: Elite Four count cannot be greater than 8 if Elite Four requirement is Johto Badges. "
            "Changing Elite Four Count to 8 for player %s.",
            world.player_name)


def __adjust_options_goal(world: "PokemonCrystalWorld"):
    if not world.options.goal.value:
        world.options.goal.value = set(world.options.goal.default)
        logging.warning(
            "Pokemon Crystal: No goal selected. Defaulting to Elite Four for player %s.",
            world.player_name)


def __adjust_options_johto_only(world: "PokemonCrystalWorld"):
    if world.options.johto_only:

        if Goal.RED in world.options.goal and world.options.johto_only == JohtoOnly.option_on:
            world.options.goal.value.discard(Goal.RED)
            logging.warning(
                "Pokemon Crystal: Red goal is incompatible with Johto Only "
                "without Silver Cave. Removing Red goal for player %s.",
                world.player_name)
            if not world.options.goal.value:
                world.options.goal.value.add(Goal.ELITE_FOUR)

        if Goal.DIPLOMA in world.options.goal and world.options.johto_only != JohtoOnly.option_off:
            world.options.goal.value.discard(Goal.DIPLOMA)
            logging.warning(
                "Pokemon Crystal: Diploma goal is incompatible with Johto Only. "
                "Removing Diploma goal for player %s.",
                world.player_name)
            if not world.options.goal.value:
                world.options.goal.value.add(Goal.ELITE_FOUR)

        if (world.options.victory_road_requirement.value == VictoryRoadRequirement.option_gyms
                and world.options.victory_road_count.value > 8):
            world.options.victory_road_count.value = 8
            logging.warning(
                "Pokemon Crystal: Victory Road Gyms >8 incompatible with Johto Only. "
                "Changing Victory Road Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.elite_four_requirement.value == EliteFourRequirement.option_gyms
                and world.options.elite_four_count.value > 8):
            world.options.elite_four_count.value = 8
            logging.warning(
                "Pokemon Crystal: Elite Four Gyms >8 incompatible with Johto Only. "
                "Changing Elite Four Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.red_requirement.value == RedRequirement.option_gyms
                and world.options.red_count.value > 8):
            world.options.red_count.value = 8
            logging.warning(
                "Pokemon Crystal: Red Gyms >8 incompatible with Johto Only. "
                "Changing Red Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.mt_silver_requirement.value == MtSilverRequirement.option_gyms
                and world.options.mt_silver_count.value > 8):
            world.options.mt_silver_count.value = 8
            logging.warning(
                "Pokemon Crystal: Mt. Silver Gyms >8 incompatible with Johto Only. "
                "Changing Mt. Silver Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.route_44_access_requirement.value == Route44AccessRequirement.option_gyms
                and world.options.route_44_access_count.value > 8):
            world.options.route_44_access_count.value = 8
            logging.warning(
                "Pokemon Crystal: Route 44 Access Gyms >8 incompatible with Johto Only. "
                "Changing Route 44 Access Gyms to 8 for player %s.",
                world.player_name)

        if (world.options.radio_tower_requirement.value == RadioTowerRequirement.option_gyms
                and world.options.radio_tower_count.value > 7):
            world.options.radio_tower_count.value = 7
            logging.warning(
                "Pokemon Crystal: Radio Tower Gyms >7 incompatible with Johto Only. "
                "Changing Radio Tower Gyms to 7 for player %s.",
                world.player_name)

        if world.options.evolution_gym_levels.value < 8:
            world.options.evolution_gym_levels.value = 8
            logging.warning(
                "Pokemon Crystal: Evolution Gym Levels <8 incompatible with Johto Only. "
                "Changing Evolution Gym Levels to 8 for player %s.",
                world.player_name)

        if world.options.randomize_badges != RandomizeBadges.option_completely_random:
            if world.options.red_count.value > 8 and world.options.red_requirement == RedRequirement.option_badges:
                world.options.red_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Red Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Red Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.victory_road_count.value > 8 and
                    world.options.victory_road_requirement.value == VictoryRoadRequirement.option_badges):
                world.options.victory_road_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Victory Road Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Victory Road Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.elite_four_count.value > 8 and
                    world.options.elite_four_requirement.value == EliteFourRequirement.option_badges):
                world.options.elite_four_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Elite Four Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Elite Four Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.radio_tower_count.value > 8
                    and world.options.radio_tower_requirement.value == RadioTowerRequirement.option_badges):
                world.options.radio_tower_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Radio Tower Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Radio Tower Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.mt_silver_count.value > 8 and
                    world.options.mt_silver_requirement.value == MtSilverRequirement.option_badges):
                world.options.mt_silver_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Mt. Silver Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Mt. Silver Badges to 8 for player %s.",
                    world.player_name)

            if (world.options.route_44_access_count.value > 8 and
                    world.options.route_44_access_requirement.value == Route44AccessRequirement.option_badges):
                world.options.route_44_access_count.value = 8
                logging.warning(
                    "Pokemon Crystal: Route 44 Access Badges >8 incompatible with Johto Only "
                    "if badges are not completely random. Changing Route 44 Access Badges to 8 for player %s.",
                    world.player_name)


def __adjust_options_restrictive_region_travel(world: "PokemonCrystalWorld") -> None:
    if world.options.randomize_badges != RandomizeBadges.option_completely_random:
        if world.options.magnet_train_access == MagnetTrainAccess.option_pass_and_power:
            world.options.magnet_train_access.value = MagnetTrainAccess.option_pass
            logging.warning("Pokemon Crystal: Magnet Train requires power not compatible with badges in gyms. "
                            "Changing Magnet Train Access to Pass for player %s.",
                            world.player_name)


def __adjust_options_gyarados(world: "PokemonCrystalWorld"):
    if (world.options.red_gyarados_access
            and world.options.randomize_badges.value == RandomizeBadges.option_vanilla
            and world.options.hm_badge_requirements != HMBadgeRequirements.option_no_badges
            and RemoveBadgeRequirement.WHIRLPOOL not in world.options.remove_badge_requirement):
        world.options.red_gyarados_access.value = RedGyaradosAccess.option_vanilla
        logging.warning("Pokemon Crystal: Red Gyarados access requires Whirlpool and Vanilla Badges are not "
                        "compatible, setting Red Gyarados access to vanilla for player %s.",
                        world.player_name)


def __adjust_options_early_fly(world: "PokemonCrystalWorld"):
    if (world.options.early_fly
            and world.options.randomize_starting_town
            and world.options.randomize_badges.value != RandomizeBadges.option_completely_random
            and RemoveBadgeRequirement.FLY not in world.options.remove_badge_requirement
            and world.options.hm_badge_requirements != HMBadgeRequirements.option_no_badges):
        world.options.early_fly.value = EarlyFly.option_false
        logging.warning("Pokemon Crystal: Early fly is not compatible with Random Starting Town if Badges are "
                        "not completely random. Disabling Early Fly for player %s",
                        world.player_name)


def __adjust_options_encounters_and_breeding(world: "PokemonCrystalWorld"):
    if (world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto
            and "Ditto" in world.options.wild_encounter_blocklist):
        world.options.breeding_methods_required.value = BreedingMethodsRequired.option_none
        logging.warning(
            "Pokemon Crystal: Ditto cannot be blocklisted while Ditto only breeding is enabled. "
            "Disabling breeding logic for player %s.",
            world.player_name)

    if WildEncounterMethodsRequired.LAND not in world.options.wild_encounter_methods_required and WildEncounterMethodsRequired.FISHING not in world.options.wild_encounter_methods_required:
        world.options.wild_encounter_methods_required.value.add(world.random.choice((WildEncounterMethodsRequired.LAND, WildEncounterMethodsRequired.FISHING)))
        logging.warning(
            "Pokemon Crystal: At least one of Land or Fishing must be enabled in wild encounter methods required. "
            "Adding one at random for player %s.",
            world.player_name)

    if (not world.options.randomize_wilds and
            world.options.breeding_methods_required == BreedingMethodsRequired.option_with_ditto
            and WildEncounterMethodsRequired.LAND not in world.options.wild_encounter_methods_required):
        world.options.breeding_methods_required.value = BreedingMethodsRequired.option_none
        logging.warning(
            "Pokemon Crystal: Ditto only breeding is not available for vanilla wilds with no Land encounters. "
            "Disabling breeding logic for player %s.",
            world.player_name)


def __adjust_options_race_mode(world: "PokemonCrystalWorld"):
    # In race mode we don't patch any item location information into the ROM
    if not world.multiworld.is_race:
        return
    if not world.options.remote_items:
        logging.warning("Pokemon Crystal: Forcing Player %s (%s) to use remote items due to race mode.",
                        world.player, world.player_name)
        world.options.remote_items.value = Toggle.option_true


def __adjust_options_pokemon_requests(world: "PokemonCrystalWorld"):
    if world.options.randomize_pokemon_requests == RandomizePokemonRequests.option_items and not world.options.randomize_wilds:
        logging.warning("Pokemon Crystal: Randomize Pokemon Requests items only is not compatible with vanilla wilds. "
                        "Disabling Randomize Pokemon Requests for player %s (%s).", world.player, world.player_name)
        world.options.randomize_pokemon_requests.value = RandomizePokemonRequests.option_off


def __adjust_options_trades(world: "PokemonCrystalWorld"):
    if world.options.randomize_trades.value not in (RandomizeTrades.option_vanilla, RandomizeTrades.option_received):
        return
    if not (world.options.trades_required or world.options.randomize_lucky_number_show):
        return

    wild_methods = set(world.options.wild_encounter_methods_required.value)
    request_logic = set(world.options.pokemon_request_logic.value)

    if world.options.randomize_wilds:
        wild_sources = {PokemonSourceLogic.LAND, PokemonSourceLogic.SURFING, PokemonSourceLogic.FISHING,
                        PokemonSourceLogic.HEADBUTT, PokemonSourceLogic.ROCK_SMASH, PokemonSourceLogic.SWARM,
                        PokemonSourceLogic.BUG_CATCHING_CONTEST}
        inlogic_wild_sources = wild_sources & wild_methods
        if inlogic_wild_sources and inlogic_wild_sources <= request_logic:
            return
    elif __vanilla_trade_requests_obtainable(world, wild_methods, request_logic):
        return

    if world.options.trades_required:
        logging.warning("Pokemon Crystal: Vanilla/received trade requests can't be made obtainable under the "
                        "chosen wild and request logic options. Disabling Trades Required for player %s (%s).",
                        world.player, world.player_name)
        world.options.trades_required.value = TradesRequired.option_false
    if world.options.randomize_lucky_number_show:
        logging.warning("Pokemon Crystal: Vanilla/received trade requests can't be made obtainable under the "
                        "chosen wild and request logic options. Disabling Lucky Number Show for player %s (%s).",
                        world.player, world.player_name)
        world.options.randomize_lucky_number_show.value = RandomizeLuckyNumberShow.option_false


def __vanilla_trade_requests_obtainable(world: "PokemonCrystalWorld", wild_methods: set[str],
                                        request_logic: set[str]) -> bool:
    def usable(source: str) -> bool:
        return source in wild_methods and source in request_logic

    dratini_in_logic = (PokemonSourceLogic.SURFING in wild_methods
                        or (world.options.static_pokemon_required and not world.options.randomize_static_pokemon))
    dragonair_obtainable = usable(PokemonSourceLogic.FISHING) or (
            PokemonSourceLogic.EVOLUTION in request_logic
            and not world.options.randomize_evolution
            and EvolutionMethodsRequired.LEVEL in world.options.evolution_methods_required.value
            and dratini_in_logic)
    # Kanto's Haunter trade: Gastly and Haunter are night-only
    haunter_obtainable = world.options.johto_only != JohtoOnly.option_off or world.options.time_of_day_encounters
    return usable(PokemonSourceLogic.LAND) and dragonair_obtainable and haunter_obtainable


def __adjust_options_dark_areas(world: "PokemonCrystalWorld"):
    if (sorted(world.options.dark_areas.value) != world.options.dark_areas.default
            and world.options.randomize_badges != RandomizeBadges.option_completely_random):
        logging.warning(
            "Pokemon Crystal: Non-vanilla dark areas are not compatible with badges that are not completely random. "
            "Resetting dark areas to vanilla for %s (%s).", world.player, world.player_name)
        world.options.dark_areas.value = world.options.dark_areas.default


def __adjust_options_randomize_types(world: "PokemonCrystalWorld"):
    if (world.options.randomize_types == RandomizeTypes.option_follow_evolutions and
            world.options.randomize_evolution == RandomizeEvolution.option_match_a_type):
        logging.warning(
            "Pokemon Crystal: Types follow evolutions and evolutions follow types are incompatible. "
            "Setting Randomize Types to completely random for %s (%s).", world.player, world.player_name)
        world.options.randomize_types.value = RandomizeTypes.option_completely_random


def __adjust_options_tm_plando(world: "PokemonCrystalWorld"):
    if 12 in world.options.tm_plando.value and "Sweet Scent" not in world.options.tm_plando.value.values() \
            and (world.options.dexsanity or world.options.dexcountsanity):
        logging.warning(
            "Pokemon Crystal: A Sweet Scent TM must exist if Dexsanity or Dexcountsanity are enabled. "
            "Resetting TM12 to vanilla for Player %s (%s).", world.player, world.player_name)
        world.options.tm_plando.value.pop(12)


def __adjust_options_traps(world: "PokemonCrystalWorld"):
    if world.options.filler_trap_percentage > world.settings.maximum_filler_trap_percentage:
        maximum_trap_weight = world.settings.maximum_filler_trap_percentage
        logging.warning(
            "Pokemon Crystal: Trap Weight is greater than allowed maximum. "
            f"Reducing filler trap percentage to {maximum_trap_weight} for Player %s (%s).",
            world.player,
            world.player_name
        )
        world.options.filler_trap_percentage.value = maximum_trap_weight


def __adjust_options_mischief_bounds(world: "PokemonCrystalWorld"):
    if world.options.enable_mischief and \
            world.options.mischief_lower_bound.value > world.options.mischief_upper_bound.value:
        world.options.mischief_upper_bound.value = world.options.mischief_lower_bound.value
        logging.warning("Pokemon Crystal: Adjusted mischief bounds for player %s (%s) :3",
                        world.player,
                        world.player_name
                        )


def __adjust_options_level_scaling(world: "PokemonCrystalWorld"):
    if (world.options.level_scaling != LevelScaling.option_off
            and world.options.lock_kanto_gyms != LockKantoGyms.option_off):
        world.options.lock_kanto_gyms.value = LockKantoGyms.option_off
        logging.warning(
            "Pokemon Crystal: Lock Kanto Gyms is incompatible with Level Scaling. "
            "Disabling Lock Kanto Gyms for player %s.",
            world.player_name)


def __adjust_options_level_curve_bounds(world: "PokemonCrystalWorld"):
    min_level = world.options.level_curve_min_level
    max_level = world.options.level_curve_max_level
    if min_level.value > max_level.value:
        min_level.value, max_level.value = max_level.value, min_level.value
        logging.warning("Pokemon Crystal: Swapped level curve min and max levels for player %s (%s)",
                        world.player,
                        world.player_name
                        )


def __adjust_options_fly_destination_rando(world: "PokemonCrystalWorld"):
    if world.options.randomize_fly_destinations and world.options.always_unlock_fly_destinations:
        world.options.always_unlock_fly_destinations.value = False
        logging.warning("Pokemon Crystal: Always Unlock Fly Destinations is incompatible with Fly Destination Rando. "
                        "Disabling Always Unlock Fly Destinations for player %s.",
                        world.player_name)

    if world.options.randomize_fly_destinations and any(world.options.free_fly_blocklist.value):
        world.options.free_fly_blocklist.value.clear()
        logging.warning("Pokemon Crystal: Free Fly Blocklist is incompatible with Fly Destination Randomization. "
                        "Disabling Free Fly Blocklist for player %s.",
                        world.player_name)


def __adjust_options_start_time(world: "PokemonCrystalWorld"):
    if parse_time(world.options.start_time.value) is None:
        logging.warning("Pokemon Crystal: %s is not a valid time string. "
                        "Resetting Start Time to vanilla for player %s.",
                        world.options.start_time.value, world.player_name)
        world.options.start_time.value = ""


def start_inventory_problems(world: "PokemonCrystalWorld", counts: Mapping[str, int]) -> list[str]:
    """The ROM writes the start inventory into a fixed size table, and the game silently drops
    anything that does not fit in the table or in the pocket the item belongs to."""
    table_entries = 0
    pocket_entries = defaultdict[str, int](int)
    oversized_tms = []
    for item_name, quantity in counts.items():
        item = data.items[world.item_name_to_id[item_name]]
        stacks = ceil(quantity / data.max_item_stack)
        table_entries += stacks
        if item.pocket == "KEY_ITEM":
            # duplicate key items are absorbed rather than taking another slot
            pocket_entries[item.pocket] += 1
        elif item.pocket == "TM_HM":
            # the TM pocket has a slot per TM, but a slot only counts to 99
            if stacks > 1:
                oversized_tms.append(item_name)
        elif item.pocket is not None:
            pocket_entries[item.pocket] += stacks

    problems = []
    if table_entries > START_INVENTORY_ENTRIES:
        problems.append(f"the game only has room for {START_INVENTORY_ENTRIES} starting stacks of items, "
                        f"but this slot needs {table_entries}")
    for pocket, size in data.pocket_sizes.items():
        if pocket_entries[pocket] > size:
            problems.append(f"the {pocket.replace('_', ' ').title()} pocket only holds {size} stacks, "
                            f"but this slot starts with {pocket_entries[pocket]}")
    if oversized_tms:
        problems.append(f"no more than {data.max_item_stack} of a TM or HM can be held, "
                        f"but this slot starts with more of {', '.join(sorted(oversized_tms))}")
    return problems


def validate_start_inventory(world: "PokemonCrystalWorld"):
    counts = defaultdict[str, int](int)
    for item in world.multiworld.precollected_items[world.player]:
        counts[item.name] += 1
    for option in (world.options.start_inventory, world.options.start_inventory_from_pool):
        for item_name, quantity in option.value.items():
            counts[item_name] += quantity
    if world.options.randomize_pokedex == RandomizePokedex.option_start_with:
        counts[item_const_name_to_label("POKEDEX")] += 1

    problems = start_inventory_problems(world, counts)
    if problems:
        raise OptionError(
            f"start_inventory: {'. '.join(problems)}. Each item takes a stack, plus another for every "
            f"{data.max_item_stack} extra copies of it, and items granted by other options count too. "
            f"Remove items or reduce quantities in start_inventory or start_inventory_from_pool."
        )


def should_include_region(region: RegionData, world: "PokemonCrystalWorld"):
    # check if region should be included
    if region.east_west_underground and not world.options.east_west_underground:
        return False
    if region.route_23_restored and not world.options.route_23_restored:
        return False
    if region.flooded_mine and not world.options.flooded_mine:
        return False
    if region.name == "REGION_MOUNT_MORTAR_1F_OUTSIDE:WATERFALL_ISLAND" \
            and not world.options.route_42_access.opens_mortar_connection:
        return False
    return (region.johto
            or world.options.johto_only.value == JohtoOnly.option_off
            or (region.silver_cave and world.options.johto_only == JohtoOnly.option_include_silver_cave)) and (
            not world.options.skip_elite_four or not region.elite_4
    )


def randomize_starting_town(world: "PokemonCrystalWorld"):
    if world.is_universal_tracker or not world.options.randomize_starting_town: return

    location_pool = data.starting_towns[:]
    location_pool = [loc for loc in location_pool if _starting_town_valid(world, loc)]

    blocklist = set(world.options.starting_town_blocklist.value)
    if "_Johto" in blocklist:
        blocklist.remove("_Johto")
        blocklist.update(town.name for town in data.starting_towns if town.johto)
    if "_Kanto" in blocklist:
        blocklist.remove("_Kanto")
        blocklist.update(town.name for town in data.starting_towns if not town.johto)

    filtered_pool = [loc for loc in location_pool if loc.name not in blocklist]
    if not filtered_pool:
        logging.warning("Pokemon Crystal: All valid starting town locations blocked for player %s (%s). "
                        "Using global list instead.", world.player, world.player_name)
        filtered_pool = location_pool

    world.random.shuffle(filtered_pool)
    world.starting_town = filtered_pool.pop()
    logging.debug(f"Starting town({world.player_name}): {world.starting_town.name}")

    if world.starting_town.name == "Cianwood City":
        world.multiworld.early_items[world.player]["HM03 Surf"] = 1


def _starting_town_valid(world: "PokemonCrystalWorld", starting_town: StartingTown):
    if world.options.johto_only and not starting_town.johto: return False
    if world.options.randomize_entrances and not starting_town.pokecenter_region: return False
    if world.options.randomize_badges != RandomizeBadges.option_completely_random and starting_town.restrictive_start:
        return False

    immediate_hiddens = world.options.randomize_hidden_items and not world.options.require_itemfinder
    full_johto_trainersanity = world.options.johto_trainersanity == JohtoTrainersanity.range_end
    full_kanto_trainersanity = world.options.kanto_trainersanity == KantoTrainersanity.range_end
    johto_shopsanity = Shopsanity.JOHTO_MARTS in world.options.shopsanity.value
    kanto_shopsanity = Shopsanity.KANTO_MARTS in world.options.shopsanity.value
    full_dexsanity = (world.options.dexsanity == Dexsanity.range_end
                      or (world.options.dexcountsanity >= 10 and world.options.dexcountsanity_step == 1))
    immediate_wilds = (WildEncounterMethodsRequired.LAND in world.options.wild_encounter_methods_required.value
                       and world.options.encounter_grouping != EncounterGrouping.option_one_per_method
                       and PokemonSourceLogic.LAND in world.options.dexsanity_logic.value)
    immediate_dexsanity = full_dexsanity and immediate_wilds

    if starting_town.name == "Cianwood City":
        return world.options.static_pokemon_required and (
                (full_johto_trainersanity and immediate_hiddens) or johto_shopsanity)

    if starting_town.name in ("Lake of Rage", "Mahogany Town"):
        # Lake of Rage only reaches Mahogany's pokecenter through the Route 43 gate
        if starting_town.name == "Lake of Rage" and "Gate" in world.options.randomize_entrances.value:
            return False
        if world.options.randomize_entrances:
            return johto_shopsanity or full_johto_trainersanity
        return ((not world.options.mount_mortar_access and "Mount Mortar" not in world.options.dark_areas)
                or johto_shopsanity or full_johto_trainersanity)

    if starting_town.name == "Azalea Town":
        return ("Slowpoke Well" not in world.options.dark_areas
                or "Union Cave" not in world.options.dark_areas or immediate_dexsanity)

    if starting_town.name in ("Pallet Town", "Viridian City", "Pewter City"):
        west_kanto_escapable = (world.options.randomize_pokegear or not world.options.lock_kanto_gyms
                                or not world.options.south_kanto_access.blocks_route_21)
        return (immediate_hiddens or world.options.route_3_access == Route3Access.option_vanilla or kanto_shopsanity
                or world.options.randomize_berry_trees or immediate_dexsanity) and west_kanto_escapable

    if starting_town.name == "Rock Tunnel":
        rock_tunnel_traversable = ("Rock Tunnel" not in world.options.dark_areas.value
                                    and not any(c in world.options.randomize_entrances.value for c in
                                                ("Dungeon", "Dungeon Interior", "Gym Interior", "Mart Interior",
                                                 "Building Interior", "Pokemon League")))
        return full_kanto_trainersanity or immediate_dexsanity or rock_tunnel_traversable

    if starting_town.name == "Vermilion City":
        return (SaffronGatehouseTea.SOUTH not in world.options.saffron_gatehouse_tea or world.options.undergrounds_require_power not in (
            UndergroundsRequirePower.option_both, UndergroundsRequirePower.option_north_south) or kanto_shopsanity
                or immediate_dexsanity)

    if starting_town.name == "Cerulean City":
        return (SaffronGatehouseTea.NORTH not in world.options.saffron_gatehouse_tea or immediate_hiddens or kanto_shopsanity
                or full_kanto_trainersanity or immediate_dexsanity)

    if starting_town.name == "Celadon City":
        return (SaffronGatehouseTea.WEST not in world.options.saffron_gatehouse_tea or immediate_hiddens or kanto_shopsanity
                or immediate_dexsanity)

    if starting_town.name == "Lavender Town":
        return (SaffronGatehouseTea.EAST not in world.options.saffron_gatehouse_tea or full_kanto_trainersanity or kanto_shopsanity
                or (immediate_dexsanity and "Rock Tunnel" not in world.options.dark_areas.value) or (
                        not world.options.route_12_access and immediate_hiddens and world.options.randomize_berry_trees))

    if starting_town.name == "Fuchsia City":
        return (SaffronGatehouseTea.EAST not in world.options.saffron_gatehouse_tea and not world.options.route_12_access) or (
                immediate_hiddens and world.options.randomize_berry_trees) or immediate_dexsanity or (
                not world.options.route_12_access and kanto_shopsanity) or full_kanto_trainersanity

    return True


def get_mart_slot_location_name(mart: str, index: int):
    if mart in CUSTOM_MART_SLOT_NAMES:
        return CUSTOM_MART_SLOT_NAMES[mart][index]
    else:
        return f"Shop Item {index + 1}"


def parse_time(time_str: str) -> tuple[int, int] | None:
    if time_str == "": return (10, 0xff)

    if time_str.lower() == "now":
        from time import localtime
        try:
            now = localtime()
        except:
            return None
        return (now.tm_hour, now.tm_min)

    split = time_str.split(":")
    if len(split) != 2: return None
    try:
        hours = int(split[0])
        minutes = int(split[1])
    except:
        return None
    if hours not in range(24): return None
    if minutes not in range(60): return None
    return (hours, minutes)


def randomize_rival(world: "PokemonCrystalWorld"):
    if world.options.rival_name.value not in ("random_player", "random_crystal") or world.is_universal_tracker:
        return
    
    if world.options.rival_name.value == "random_crystal":
        other_crystal_players = [player for player, game in world.multiworld.game.items()
                                 if player != world.player and game == world.game]
        if other_crystal_players:
            world.generated_rival = world.random.choice(other_crystal_players)
            return
        logging.warning(f"Pokemon Crystal: No other {world.game} players exist in this Multiworld. "
                     f"Attempting to set Rival Name to Random Player for player {world.player} ({world.player_name})")

    other_players = [player for player in world.multiworld.player_ids if player != world.player]
    if not other_players:
        logging.warning("Pokemon Crystal: This is a solo Multiworld. Setting Rival Name to vanilla.")
        world.options.rival_name.value = ""
        return
    world.generated_rival = world.random.choice(other_players)


def pretty_region_name(region_id: str) -> str:
    return region_id.removeprefix("REGION_").replace(":", " ").replace("_", " ").title().replace(" Of ", " of ")


def dexsanity_wild_in_logic(world: "PokemonCrystalWorld", key: EncounterKey) -> bool:
    if world.logic.wild_regions[key] is not LogicalAccess.InLogic:
        return False
    type_to_source_method = {
        EncounterType.Grass: PokemonSourceLogic.LAND,
        EncounterType.Water: PokemonSourceLogic.SURFING,
        EncounterType.Fish: PokemonSourceLogic.FISHING,
        EncounterType.Tree: PokemonSourceLogic.HEADBUTT,
        EncounterType.RockSmash: PokemonSourceLogic.ROCK_SMASH,
        EncounterType.Swarm: PokemonSourceLogic.SWARM
    }
    return type_to_source_method[key.encounter_type] in world.options.dexsanity_logic.value


def dexsanity_contest_in_logic(world: "PokemonCrystalWorld") -> bool:
    return WildEncounterMethodsRequired.BUG_CATCHING_CONTEST in world.options.wild_encounter_methods_required.value \
            and PokemonSourceLogic.BUG_CATCHING_CONTEST in world.options.dexsanity_logic.value


def dexsanity_statics_in_logic(world: "PokemonCrystalWorld") -> bool:
    return world.options.static_pokemon_required and PokemonSourceLogic.STATICS in world.options.dexsanity_logic.value


def dexsanity_breeding_in_logic(world: "PokemonCrystalWorld") -> bool:
    return world.options.breeding_methods_required and \
            PokemonSourceLogic.BREEDING in world.options.dexsanity_logic.value


def dexsanity_trades_in_logic(world: "PokemonCrystalWorld") -> bool:
    return world.options.trades_required and PokemonSourceLogic.TRADES in world.options.dexsanity_logic.value


def convert_to_ingame_text(text: str, string_terminator: bool = False) -> list[int]:
    charmap = {
        "…": 0x75, " ": 0x7f, "A": 0x80, "B": 0x81, "C": 0x82, "D": 0x83, "E": 0x84, "F": 0x85, "G": 0x86, "H": 0x87,
        "I": 0x88, "J": 0x89, "K": 0x8a, "L": 0x8b, "M": 0x8c, "N": 0x8d, "O": 0x8e, "P": 0x8f, "Q": 0x90, "R": 0x91,
        "S": 0x92, "T": 0x93, "U": 0x94, "V": 0x95, "W": 0x96, "X": 0x97, "Y": 0x98, "Z": 0x99, "(": 0x9a, ")": 0x9b,
        ":": 0x9c, ";": 0x9d, "[": 0x9e, "]": 0x9f, "a": 0xa0, "b": 0xa1, "c": 0xa2, "d": 0xa3, "e": 0xa4, "f": 0xa5,
        "g": 0xa6, "h": 0xa7, "i": 0xa8, "j": 0xa9, "k": 0xaa, "l": 0xab, "m": 0xac, "n": 0xad, "o": 0xae, "p": 0xaf,
        "q": 0xb0, "r": 0xb1, "s": 0xb2, "t": 0xb3, "u": 0xb4, "v": 0xb5, "w": 0xb6, "x": 0xb7, "y": 0xb8, "z": 0xb9,
        "Ä": 0xc0, "Ö": 0xc1, "Ü": 0xc2, "ä": 0xc3, "ö": 0xc4, "ü": 0xc5, "'": 0xe0, "-": 0xe3, "+": 0xe4,
        "?": 0xe6, "!": 0xe7, ".": 0xe8, "&": 0xe9, "é": 0xea, "→": 0xeb, "▷": 0xec, "▶": 0xed, "▼": 0xee,
        "♂": 0xef, "¥": 0xf0, "/": 0xf3, ",": 0xf4, "0": 0xf6, "1": 0xf7, "2": 0xf8, "3": 0xf9, "4": 0xfa,
        "5": 0xfb, "6": 0xfc, "7": 0xfd, "8": 0xfe, "9": 0xff, "_": 0xe3, "♀": 0xf5, "$": 0xf0, "£": 0xf0,
        "€": 0xf0, "É": 0xea,
    }
    apostrophe_specials = {
        "d": 0xd0, "l": 0xd1, "m": 0xd2, "r": 0xd3, "s": 0xd4, "t": 0xd5, "v": 0xd6
    }
    current_char = 0
    ingame_string = []
    while current_char < len(text):
        if text[current_char] == "'" and current_char < len(text) - 1 and text[current_char + 1] in apostrophe_specials:
            current_char += 1
            ingame_string.append(apostrophe_specials[text[current_char]])
        else:
            ingame_string.append(charmap.get(text[current_char], charmap["?"]))
        current_char += 1
    if string_terminator:
        ingame_string.append(0x50)
    return ingame_string


def bound(value: int, lower_bound: int, upper_bound: int) -> int:
    return max(min(value, upper_bound), lower_bound)


def rom_offset_to_address(offset: int) -> tuple[int, int]:
    if offset < 0x4000: return 0, offset
    bank = offset // 0x4000
    address = offset - (bank - 1) * 0x4000
    return bank, address


def replace_map_tiles(patch, map_name: str, x: int, y: int, tiles):
    # x and y are 0 indexed
    tile_index = (y * data.maps[map_name].width) + x
    base_address = data.rom_addresses[f"{map_name}_Blocks"]

    logging.debug(f"Writing {len(tiles)} new tile(s) to map {map_name} at {x},{y}")
    write_appp_tokens(patch, tiles, base_address + tile_index)


def write_appp_tokens(patch, byte_array, address):
    patch.write_token(
        APTokenTypes.WRITE,
        address,
        bytes(byte_array)
    )


def write_rom_bytes(rom, byte_array, address):
    rom[address:address + len(byte_array)] = bytes(byte_array)

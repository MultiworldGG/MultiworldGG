import logging
from collections import defaultdict
from typing import TYPE_CHECKING

from BaseClasses import Region, ItemClassification
from entrance_rando import EntranceType
from .data import data, RegionData, EncounterMon, StaticPokemon, LogicalAccess, EncounterKey, FishingRodType, \
    TreeRarity, EncounterType
from .fly import flypoint_arrival_connections, get_fly_regions, fly_flag_index
from .items import PokemonCrystalItem
from .locations import PokemonCrystalLocation
from .options import FreeFlyLocation, JohtoOnly, BlackthornDarkCaveAccess, Goal, Route42Access, LevelCurve, \
    WildEncounterMethodsRequired
from .pokemon_data import SWARM_REGISTRATIONS
from .entrance_rando import build_er_group_lookup, base_category, connection_er_group
from .utils import should_include_region

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld

# Rematches
MAP_LOCKED = [
    "BUG_CATCHER_ARNIE_BLACKTHORN", "BUG_CATCHER_ARNIE_LAKE",
    "BUG_CATCHER_WADE_GOLDENROD", "BUG_CATCHER_WADE_MAHOGANY",
    "CAMPER_TODD_BLACKTHORN", "CAMPER_TODD_CIANWOOD",
    "FISHER_RALPH_ECRUTEAK", "FISHER_RALPH_LAKE",
    "HIKER_ANTHONY_OLIVINE", "LASS_DANA_CIANWOOD",
    "PICNICKER_GINA_MAHOGANY", "PICNICKER_LIZ_ECRUTEAK",
    "SCHOOLBOY_ALAN_BLACKTHORN",
    "SCHOOLBOY_ALAN_OLIVINE", "SCHOOLBOY_CHAD_MAHOGANY",
    "SCHOOLBOY_JACK_OLIVINE", "YOUNGSTER_JOEY_GOLDENROD",
    "YOUNGSTER_JOEY_OLIVINE"
]

ROCKETHQ_LOCKED = [
    "FISHER_TULLY_ROCKETHQ", "PICNICKER_LIZ_ROCKETHQ",
    "POKEMANIAC_BRENT_ROCKETHQ"
]

RADIO_LOCKED = [
    "BUG_CATCHER_WADE_RADIO", "HIKER_ANTHONY_RADIO",
    "LASS_DANA_RADIO", "PICNICKER_GINA_RADIO",
    "PICNICKER_LIZ_RADIO", "PICNICKER_TIFFANY_RADIO",
    "SAILOR_HUEY_RADIO", "SCHOOLBOY_CHAD_RADIO",
    "SCHOOLBOY_JACK_RADIO", "YOUNGSTER_JOEY_RADIO"
]

CHAMPION_LOCKED = [
    "BIRD_KEEPER_JOSE_CHAMPION", "BIRD_KEEPER_VANCE_CHAMPION",
    "BUG_CATCHER_ARNIE_CHAMPION", "BUG_CATCHER_WADE_CHAMPION",
    "CAMPER_TODD_CHAMPION", "COOLTRAINERF_BETH_CHAMPION",
    "COOLTRAINERF_REENA_CHAMPION", "COOLTRAINERM_GAVEN_CHAMPION",
    "FISHER_RALPH_CHAMPION", "FISHER_TULLY_CHAMPION",
    "FISHER_WILTON_CHAMPION", "HIKER_ANTHONY_CHAMPION",
    "HIKER_PARRY_CHAMPION", "LASS_DANA_CHAMPION",
    "PICNICKER_ERIN_CHAMPION", "PICNICKER_GINA_CHAMPION",
    "PICNICKER_TIFFANY_CHAMPION", "POKEMANIAC_BRENT_CHAMPION",
    "SAILOR_HUEY_CHAMPION", "SCHOOLBOY_ALAN_CHAMPION",
    "SCHOOLBOY_CHAD_CHAMPION", "SCHOOLBOY_JACK_CHAMPION",
    "YOUNGSTER_JOEY_CHAMPION", "PICNICKER_LIZ_CHAMPION"
]

KANTO_LOCKED = [
    "BIRD_KEEPER_JOSE_POWER", "BIRD_KEEPER_VANCE_POWER",
    "BUG_CATCHER_ARNIE_POWER", "CAMPER_TODD_POWER",
    "COOLTRAINERF_BETH_POWER", "COOLTRAINERF_REENA_POWER",
    "COOLTRAINERM_GAVEN_POWER", "FISHER_RALPH_POWER",
    "FISHER_TULLY_POWER", "FISHER_WILTON_POWER",
    "HIKER_ANTHONY_POWER", "HIKER_PARRY_POWER",
    "LASS_DANA_POWER", "PICNICKER_ERIN_POWER",
    "PICNICKER_GINA_POWER", "PICNICKER_TIFFANY_POWER",
    "POKEMANIAC_BRENT_POWER", "SAILOR_HUEY_POWER",
    "SCHOOLBOY_ALAN_POWER", "SCHOOLBOY_CHAD_POWER",
    "SCHOOLBOY_JACK_POWER"
]

LOGIC_EXCLUDE_STATICS = [
    "Raikou", "Entei", "CatchTutorial1", "CatchTutorial2", "CatchTutorial3"
]

E4_LOCKED = list(set(CHAMPION_LOCKED + KANTO_LOCKED))
REMATCHES = list(set(MAP_LOCKED + ROCKETHQ_LOCKED + RADIO_LOCKED + E4_LOCKED + KANTO_LOCKED))


def _generate_curve_levels(n: int, min_level: int, max_level: int, shape: int) -> list[int]:
    if n == 0:
        return []
    if n == 1:
        return [min_level]
    span = max_level - min_level
    levels = []
    for i in range(n):
        t = i / (n - 1)
        if shape == LevelCurve.option_sqrt:
            t = t ** 0.5
        elif shape == LevelCurve.option_quadratic:
            t = t ** 2
        elif shape == LevelCurve.option_s_curve:
            t = t * t * (3 - 2 * t)  # smoothstep
        levels.append(round(min_level + span * t))
    return levels


def create_regions(world: "PokemonCrystalWorld") -> dict[str, Region]:
    regions: dict[str, Region] = {}
    connections: list[tuple[str, str, str]] = []
    johto_only = world.options.johto_only.value
    rematches = world.options.rematchsanity or world.options.randomize_phone_call_items

    wild_name_level_list: list[tuple[str, list[int]]] = []
    trainer_name_level_list: list[tuple[str, int]] = []
    static_name_level_list: list[tuple[str, int]] = []

    wild_scaling_locations: set[str] = set()
    seen_scaling_keys: set[str] = set()

    grass_keys_by_region = defaultdict(list)
    fish_keys_by_region_rod: dict[tuple[str, FishingRodType], list[EncounterKey]] = defaultdict(list)
    for k in world.generated_wild:
        if k.encounter_type is EncounterType.Grass:
            grass_keys_by_region[k.region_id].append(k)
        elif k.encounter_type is EncounterType.Fish:
            fish_keys_by_region_rod[(k.region_id, k.fishing_rod)].append(k)

    def exclude_scaling(trainer: str):
        if not rematches and (trainer in REMATCHES):
            return True
        elif johto_only != JohtoOnly.option_off and trainer in KANTO_LOCKED:
            return True
        elif world.options.goal.value == {Goal.ELITE_FOUR} and trainer in E4_LOCKED:
            return True
        else:
            return False

    def create_scaling_location(parent_region: Region, wild_key: EncounterKey):
        if not (world.options.level_scaling and wild_key.encounter_type in [
            EncounterType.Grass, EncounterType.Water, EncounterType.Swarm,
            EncounterType.Fish, EncounterType.Tree, EncounterType.RockSmash,
        ]):
            return

        key_name = wild_key.region_name()
        if key_name not in seen_scaling_keys:
            seen_scaling_keys.add(key_name)
            wild_name_level_list.append((
                key_name,
                [slot.level for slot in world.generated_wild[wild_key]]
            ))

        location_name = (f"{key_name} ({parent_region.name})"
                         if key_name in wild_scaling_locations else key_name)
        scaling_event = PokemonCrystalLocation(
            world.player, location_name, parent_region, None, None, None,
            frozenset({"wilds scaling"}))
        scaling_event.show_in_spoiler = False
        scaling_event.place_locked_item(PokemonCrystalItem(
            "Wild Pokemon", ItemClassification.filler, None, world.player))
        scaling_event.encounter_key = wild_key
        parent_region.locations.append(scaling_event)
        wild_scaling_locations.add(scaling_event.name)

    def create_wild_region(parent_region: Region, wild_key: EncounterKey, wilds: list[EncounterMon | StaticPokemon],
                           tags: set[str] | None = None):
        region_name = wild_key.region_name()
        if region_name not in regions:
            wild_region = Region(region_name, world.player, world.multiworld)
            wild_region.key = wild_key
            regions[region_name] = wild_region

            # We place a slot for each encounter here, but we don't care about what they are yet
            for i in range(len(wilds)):
                location = PokemonCrystalLocation(
                    world.player,
                    f"{region_name}_{i + 1}",
                    wild_region,
                    tags=frozenset(tags | {"wild encounter"} if tags else {"wild encounter"})
                )
                location.show_in_spoiler = False
                wild_region.locations.append(location)
        else:
            wild_region = regions[region_name]
        parent_region.connect(wild_region)

    def setup_wild_regions(parent_region: Region, wild_region_data: RegionData):

        if wild_region_data.wild_encounters:
            if wild_region_data.wild_encounters.grass:
                grass_name = wild_region_data.wild_encounters.grass
                grass_keys = grass_keys_by_region[grass_name]
                for encounter_key in grass_keys:
                    create_scaling_location(parent_region, encounter_key)
                    if WildEncounterMethodsRequired.LAND in world.options.wild_encounter_methods_required:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                    else:
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.surfing:
                encounter_key = EncounterKey.water(wild_region_data.wild_encounters.surfing)
                create_scaling_location(parent_region, encounter_key)
                if WildEncounterMethodsRequired.SURFING in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.fishing:
                fishing_name = wild_region_data.wild_encounters.fishing
                for fishing_rod in (FishingRodType.Old, FishingRodType.Good, FishingRodType.Super):
                    fish_keys = fish_keys_by_region_rod[(fishing_name, fishing_rod)]
                    for encounter_key in fish_keys:
                        create_scaling_location(parent_region, encounter_key)
                        if WildEncounterMethodsRequired.FISHING in world.options.wild_encounter_methods_required:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                        else:
                            if not world.options.enforce_wild_encounter_methods_logic:
                                world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                            if world.is_universal_tracker:
                                create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.headbutt:
                for rarity in (TreeRarity.Common, TreeRarity.Rare):
                    encounter_key = EncounterKey.tree(wild_region_data.wild_encounters.headbutt, rarity)
                    create_scaling_location(parent_region, encounter_key)
                    if WildEncounterMethodsRequired.HEADBUTT in world.options.wild_encounter_methods_required:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                    else:
                        if not world.options.enforce_wild_encounter_methods_logic:
                            world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                        if world.is_universal_tracker:
                            create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            if wild_region_data.wild_encounters.rock_smash:
                encounter_key = EncounterKey.rock_smash()
                create_scaling_location(parent_region, encounter_key)
                if WildEncounterMethodsRequired.ROCK_SMASH in world.options.wild_encounter_methods_required:
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

            swarms_qualify = WildEncounterMethodsRequired.SWARM in world.options.wild_encounter_methods_required

            for swarm_region_id, cfg in SWARM_REGISTRATIONS.items():
                if not ((cfg["grass_host"] is not None and wild_region_data.wild_encounters.grass == cfg["grass_host"])
                        or wild_region_data.name == cfg["fishing_region"]):
                    continue
                encounter_key = EncounterKey.swarm(swarm_region_id)
                if encounter_key not in world.generated_wild:
                    continue
                if swarms_qualify:
                    create_scaling_location(parent_region, encounter_key)
                    world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                    create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])
                else:
                    if not world.options.enforce_wild_encounter_methods_logic:
                        world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                    if world.is_universal_tracker:
                        create_scaling_location(parent_region, encounter_key)
                        create_wild_region(parent_region, encounter_key, world.generated_wild[encounter_key])

        for static_id in wild_region_data.statics:
            static_encounter = world.generated_static[static_id]
            encounter_key = EncounterKey.static(static_encounter.name)
            if (world.options.static_pokemon_required
                    and static_encounter.name not in LOGIC_EXCLUDE_STATICS):
                world.logic.wild_regions[encounter_key] = LogicalAccess.InLogic
                create_wild_region(parent_region, encounter_key, [static_encounter])
            else:
                world.logic.wild_regions[encounter_key] = LogicalAccess.OutOfLogic
                if world.is_universal_tracker:
                    create_wild_region(parent_region, encounter_key, [static_encounter])

    def setup_mart_regions(parent_region: Region, region_data: RegionData):
        for mart in region_data.marts:
            mart_data = data.marts[mart]
            if mart_data.category in world.options.shopsanity.value:
                region_name = f"REGION_{mart}"
                new_region = Region(region_name, world.player, world.multiworld)
                regions[region_name] = new_region
                parent_region.connect(new_region)

    for region_name, region_data in data.regions.items():
        if should_include_region(region_data, world):
            new_region = Region(region_name, world.player, world.multiworld)

            regions[region_name] = new_region

            for event_data in region_data.events:
                event_location = PokemonCrystalLocation(world.player, event_data.name, new_region)
                event_location.show_in_spoiler = False
                event_location.place_locked_item(world.create_event(event_data.name))
                new_region.locations.append(event_location)

            setup_wild_regions(new_region, region_data)
            if world.options.shopsanity:
                setup_mart_regions(new_region, region_data)

            # Level Scaling
            if world.options.level_scaling and not world.is_universal_tracker:
                # Create plando locations for the trainers in their regions.
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        logging.debug(
                            f"Excluding %s from level scaling for %s", trainer.name, world.player_name)
                        continue
                    scaling_event = PokemonCrystalLocation(
                        world.player, trainer.name, new_region, None, None, None, frozenset({"trainer scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Trainer Party", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                # Create plando locations for the statics in their regions.
                for static in region_data.statics:
                    scaling_event = PokemonCrystalLocation(
                        world.player, world.generated_static[static].name, new_region, None, None, None,
                        frozenset({"static scaling"}))
                    scaling_event.show_in_spoiler = False
                    scaling_event.place_locked_item(PokemonCrystalItem(
                        "Static Pokemon", ItemClassification.filler, None, world.player))
                    new_region.locations.append(scaling_event)

                # Create a new list of all the Trainer Pokemon and their levels
                for trainer in region_data.trainers:
                    if exclude_scaling(trainer.name):
                        continue
                    min_level = 100
                    for pokemon in trainer.pokemon:
                        min_level = min(min_level, pokemon.level)
                    # We grab the level and add it to our custom list.
                    trainer_name_level_list.append((trainer.name, min_level))
                    world.trainer_name_level_dict[trainer.name] = min_level

                # Now we do the same for statics.
                for static_id in region_data.statics:
                    static = world.generated_static[static_id]
                    static_name_level_list.append((static.name, static.level))

            if world.options.grasssanity and region_name in data.grass_tiles:
                grass_region = Region(f"{region_name}:GRASS", world.player, world.multiworld)
                regions[grass_region.name] = grass_region
                new_region.connect(grass_region)

            for region_exit in region_data.exits:
                connections.append((f"{region_name} -> {region_exit}", region_name, region_exit))

    randomize = world.options.randomize_entrances.value  # frozenset of category strings
    mix = world.options.mix_entrances.value              # frozenset of category strings
    # connect_entrances reassigns every group before ER runs; this is just the initial one.
    _, group_map = build_er_group_lookup(set(randomize), set(mix))

    # Pin certain pokecenter entrances to vanilla so the player always has pokecenter access.
    vanilla_pokecenter: set[str] = set()
    if "Pokecenter" in randomize:
        if world.options.randomize_starting_town:
            starting_town = world.starting_town
        else:
            starting_town = next(t for t in data.starting_towns if t.region_id == "REGION_NEW_BARK_TOWN")

        # The pokecenter interior has a _1F suffix; every Pokecenter connection has
        # exactly one such side, so the other one is the town region.
        town = starting_town.pokecenter_region
        if town and "POKECENTER_1F" not in town:
            vanilla_pokecenter = {name for name, conn in data.entrance_connections.items()
                                  if base_category(conn.category) == "Pokecenter"
                                  and town in (conn.entrance_region, conn.exit_region)}

    bypassed_vanilla_edges: set[str] = set()
    if world.options.route_23_restored:
        bypassed_vanilla_edges = {
            "REGION_VICTORY_ROAD:1F:ENTRANCE -> REGION_VICTORY_ROAD_GATE:NORTH",
            "REGION_VICTORY_ROAD_GATE:NORTH -> REGION_VICTORY_ROAD:1F:ENTRANCE",
        }

    if world.options.skip_elite_four:
        connections.append(("REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE -> REGION_LANCES_ROOM",
                            "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE", "REGION_LANCES_ROOM"))
        if randomize:
            connections.append(("REGION_LANCES_ROOM -> REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE",
                                "REGION_LANCES_ROOM", "REGION_INDIGO_PLATEAU_POKECENTER_1F:E4_GATE"))

    for name, source, dest in connections:
        if name in bypassed_vanilla_edges:
            continue
        if should_include_region(data.regions[source], world) and should_include_region(data.regions[dest], world):
            entrance = regions[source].connect(regions[dest], name)
            # Disconnect for ER if this connection's category is in the randomization pool
            conn = data.entrance_connections.get(name)
            if (conn
                    and base_category(conn.category) in randomize
                    and name not in vanilla_pokecenter):
                if conn.one_way:
                    entrance.randomization_type = EntranceType.ONE_WAY
                else:
                    entrance.randomization_type = EntranceType.TWO_WAY
                entrance.randomization_group = connection_er_group(group_map, name, conn.category)
                world.er_entrances.append((entrance, regions[dest]))

    regions["Menu"] = Region("Menu", world.player, world.multiworld)
    if world.options.randomize_starting_town:
        regions["Menu"].connect(regions[world.starting_town.region_id])
    elif world.options.randomize_entrances:
        regions["Menu"].connect(regions["REGION_NEW_BARK_TOWN"], "Start Game")
    else:
        regions["Menu"].connect(regions["REGION_PLAYERS_HOUSE_2F"], "Start Game")

    # Fly

    regions["Menu"].connect(regions["REGION_FLY"], "Fly")

    for fr in data.fly_regions:
        if fr.unlock_region == fr.exit_region or fr.exit_region not in regions:
            continue
        fly_unlock = Region(fr.unlock_region, world.player, world.multiworld)
        regions[fr.unlock_region] = fly_unlock
        event_name = f"EVENT_VISITED_{fr.base_identifier}"
        event_location = PokemonCrystalLocation(world.player, event_name, fly_unlock)
        event_location.show_in_spoiler = False
        event_location.place_locked_item(world.create_event(event_name))
        fly_unlock.locations.append(event_location)
        regions[fr.exit_region].connect(fly_unlock, f"{fr.exit_region} -> {fr.unlock_region}")

    for fr in data.fly_regions:
        if fr.unlock_region not in regions:
            continue
        for src in fr.unlock_sources:
            if src in regions:
                regions[src].connect(regions[fr.unlock_region], f"{src} -> {fr.unlock_region}")

    fly_region = regions["REGION_FLY"]
    if world.options.randomize_fly_destinations:
        for i, flypoint in enumerate(world.fly_destinations, start=1):
            dest_region = flypoint_arrival_connections(flypoint)[0].entrance_region
            fly_region.connect(regions[dest_region], f"Fly Destination {i}")
    else:
        for region in get_fly_regions(world):
            fly_region.connect(regions[region.exit_region])

    if world.options.blackthorn_dark_cave_access == BlackthornDarkCaveAccess.option_waterfall:
        regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:SOUTHWEST"].connect(
            regions["REGION_DARK_CAVE_BLACKTHORN_ENTRANCE:NORTHWEST"])

    if world.options.route_42_access != Route42Access.option_blocked:
        regions["REGION_ROUTE_42:WEST"].connect(regions["REGION_ROUTE_42:CENTER"])
        regions["REGION_ROUTE_42:CENTER"].connect(regions["REGION_ROUTE_42:WEST"])
        regions["REGION_ROUTE_42:EAST"].connect(regions["REGION_ROUTE_42:CENTER"])
        regions["REGION_ROUTE_42:CENTER"].connect(regions["REGION_ROUTE_42:EAST"])

    if world.options.dexsanity or world.options.dexcountsanity:
        pokedex_region = Region("Pokedex", world.player, world.multiworld)
        regions["Pokedex"] = pokedex_region
        regions["Menu"].connect(regions["Pokedex"])
    if world.options.battle_tower_sanity or Goal.BATTLE_TOWER in world.options.goal:
        battle_tower_region = Region("Battle Tower", world.player, world.multiworld)
        regions["Battle Tower"] = battle_tower_region
        regions["REGION_BATTLE_TOWER_1F"].connect(regions["Battle Tower"])
        # Per-tier sub-regions so the sanity location and the logical event share
        # the same access rule (set on the parent → child entrance in rules.py).
        for tier_idx in range(10):
            tier_region = Region(f"Battle Tower Tier {tier_idx + 1}", world.player, world.multiworld)
            regions[tier_region.name] = tier_region
            battle_tower_region.connect(tier_region)
            if Goal.BATTLE_TOWER in world.options.goal:
                event_name = f"EVENT_BATTLE_TOWER_TIER_{tier_idx + 1}_BEATEN"
                loc = PokemonCrystalLocation(world.player, event_name, tier_region)
                loc.show_in_spoiler = False
                loc.place_locked_item(world.create_event(event_name))
                tier_region.locations.append(loc)
        if Goal.BATTLE_TOWER in world.options.goal:
            goal_event = "EVENT_BEAT_ALL_BATTLE_TOWER_TIERS"
            loc = PokemonCrystalLocation(world.player, goal_event, battle_tower_region)
            loc.show_in_spoiler = False
            loc.place_locked_item(world.create_event(goal_event))
            battle_tower_region.locations.append(loc)
    if world.options.evolution_methods_required or world.is_universal_tracker:
        evolution_region = Region("Evolutions", world.player, world.multiworld)
        regions["Evolutions"] = evolution_region
        regions["Menu"].connect(regions["Evolutions"])
    if world.options.breeding_methods_required or world.is_universal_tracker:
        breeding_region = Region("Breeding", world.player, world.multiworld)
        regions["Breeding"] = breeding_region
        regions["Menu"].connect(regions["Breeding"])

    if world.options.level_scaling and not world.is_universal_tracker:
        trainer_name_level_list.sort(key=lambda i: i[1])
        world.trainer_name_list = [i[0] for i in trainer_name_level_list]
        static_name_level_list.sort(key=lambda i: i[1])
        world.static_name_list = [i[0] for i in static_name_level_list]
        wild_name_level_list.sort(key=lambda i: max(i[1]))
        world.encounter_region_name_list = [i[0] for i in wild_name_level_list]
        flat_wild_levels = [j for i in wild_name_level_list for j in i[1]]
        flat_wild_levels.sort()

        if world.options.level_curve != LevelCurve.option_vanilla:
            min_level = world.options.level_curve_min_level.value
            max_level = world.options.level_curve_max_level.value
            shape = world.options.level_curve.value
            wild_static_max = max(min_level, round(max_level * 2 / 3))
            world.trainer_level_list = _generate_curve_levels(len(trainer_name_level_list), min_level, max_level, shape)
            world.static_level_list = _generate_curve_levels(len(static_name_level_list), min_level, wild_static_max, shape)
            world.encounter_region_levels_list = _generate_curve_levels(len(flat_wild_levels), min_level, wild_static_max, shape)
        else:
            world.trainer_level_list = [i[1] for i in trainer_name_level_list]
            world.static_level_list = [i[1] for i in static_name_level_list]
            world.encounter_region_levels_list = flat_wild_levels
    return regions


def _get_fly_dest_region(world: "PokemonCrystalWorld", fly_location: "FlyRegion") -> str:
    if world.options.randomize_fly_destinations:
        flypoint = world.fly_destinations[fly_flag_index(world, fly_location)]
        return flypoint_arrival_connections(flypoint)[0].entrance_region
    return fly_location.exit_region


def setup_free_fly_regions(world: "PokemonCrystalWorld"):
    fly = world.get_region("REGION_FLY")
    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly,
                                                 FreeFlyLocation.option_free_fly_and_map_card):
        free_fly_location = world.free_fly_location
        dest_region = _get_fly_dest_region(world, free_fly_location)
        fly_region = world.get_region(dest_region)
        fly.connect(fly_region, f"Free Fly {dest_region}")

    if world.options.free_fly_location.value in (FreeFlyLocation.option_free_fly_and_map_card,
                                                 FreeFlyLocation.option_map_card):
        map_card_fly_location = world.map_card_fly_location
        dest_region = _get_fly_dest_region(world, map_card_fly_location)
        map_card_region = world.get_region(dest_region)
        fly.connect(map_card_region, f"Free Fly {dest_region}")

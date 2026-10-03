from collections.abc import Sequence
from typing import TYPE_CHECKING

from BaseClasses import Location, Region, LocationProgressType
from .battle_tower_data import BATTLE_TOWER_TRAINERS, BATTLE_TOWER_TIER_OFFSET, BATTLE_TOWER_NUM_TIERS, \
    BATTLE_TOWER_TRAINER_OFFSET, BATTLE_TOWER_TRAINERS_PER_TIER
from .data import data, LogicalAccess, GrassTile
from .evolution import evolution_location_name
from .fly import get_fly_regions, SILVER_CAVE_FLY_INDEX
from .item_data import POKEDEX_OFFSET, POKEDEX_COUNT_OFFSET, GRASS_OFFSET, FLAG_ITEM_OFFSET, CANONICAL_ITEM_ID_MASK
from .items import item_const_name_to_id
from .options import Goal, DexsanityStarters, Grasssanity, RandomizeBugCatchingContest, WildEncounterMethodsRequired, \
    PokemonSourceLogic, BattleTowerSanity, VanillaEventChains, RandomizeFlyUnlocks, JohtoOnly, Shopsanity
from .pokemon import get_priority_dexsanity, get_excluded_dexsanity
from .rematch_trainer_data import (
    all_rematch_locations
)
from .utils import get_mart_slot_location_name

if TYPE_CHECKING:
    from . import PokemonCrystalWorld


class PokemonCrystalLocation(Location):
    game: str = data.manifest.game
    rom_addresses: list[int]
    default_item_code: int | None
    flag: int | None
    tags: frozenset[str]

    def __init__(
            self,
            player: int,
            name: str,
            parent: Region | None = None,
            flag: int | None = None,
            rom_addresses: list[int] | None = None,
            default_item_value: int | None = None,
            tags: frozenset[str] = frozenset(),
            progress_type: LocationProgressType = LocationProgressType.DEFAULT
    ) -> None:
        super().__init__(player, name, flag, parent)
        self.default_item_code = default_item_value
        self.rom_addresses = rom_addresses or []
        self.tags = tags
        self.progress_type = progress_type


def create_locations(world: "PokemonCrystalWorld", regions: dict[str, Region]) -> None:
    exclude = set()
    if not world.options.randomize_hidden_items:
        exclude.add("Hidden")
    if not world.options.randomize_pokegear and not world.options.remote_items:
        exclude.add("Pokegear")
    if not world.options.randomize_badges:
        exclude.add("Badge")
    remote_apricorn_trees_only = (world.options.remote_items and not world.options.randomize_berry_trees
                                  and Shopsanity.APRICORNS in world.options.shopsanity.value)
    if not world.options.randomize_berry_trees and not remote_apricorn_trees_only:
        exclude.add("BerryTree")
    if not world.options.saffron_gatehouse_tea:
        exclude.add("RequiresSaffronGatehouses")
    if VanillaEventChains.CLAIR in world.options.vanilla_event_chains.value:
        exclude.add("VanillaClairOff")
    else:
        exclude.add("VanillaClairOn")
    if not world.options.randomize_pokemon_requests:
        exclude.add("BillsGrandpa")
        exclude.add("PokemonRequest")
    if not world.options.johto_trainersanity and not world.options.kanto_trainersanity:
        exclude.add("Trainersanity")
    if not world.options.randomize_phone_call_items:
        exclude.add("Phone Calls")
    if not world.options.momsanity:
        exclude.add("Momsanity")
    if not world.options.randomize_pokedex:
        exclude.add("Pokedex")
    if not world.options.randomize_lucky_number_show:
        exclude.add("Lucky Number Show")

    exclude.add("Contest")

    always_include = {"KeyItem"}

    if world.options.randomize_bug_catching_contest == RandomizeBugCatchingContest.option_all:
        always_include.add("ContestAll")
    elif world.options.randomize_bug_catching_contest == RandomizeBugCatchingContest.option_combine_second_third:
        always_include.add("ContestCombineSecondThird")
    elif world.options.randomize_bug_catching_contest == RandomizeBugCatchingContest.option_participate:
        always_include.add("ContestParticipate")

    def is_vanilla_berry_tree(loc: str) -> bool:
        return (remote_apricorn_trees_only and "BerryTree" in data.locations[loc].tags
                and "Apricorn" not in data.items[data.locations[loc].default_item].tags)

    for region_name, region_data in data.regions.items():
        if region_name in regions:
            region = regions[region_name]
            filtered_locations = [loc for loc in region_data.locations if
                                  (always_include.intersection(set(data.locations[loc].tags)) or
                                   not exclude.intersection(set(data.locations[loc].tags)))
                                  and not is_vanilla_berry_tree(loc)]
            for location_name in filtered_locations:
                location_data = data.locations[location_name]
                progress_type = LocationProgressType.EXCLUDED \
                    if (world.options.goal.value == {Goal.ELITE_FOUR}
                        and "PostE4" in location_data.tags
                        and world.options.exclude_post_goal_locations) else LocationProgressType.DEFAULT
                location = PokemonCrystalLocation(
                    world.player,
                    location_data.label,
                    region,
                    location_data.flag,
                    location_data.rom_addresses,
                    location_data.default_item,
                    location_data.tags,
                    progress_type,
                )
                region.locations.append(location)

            if world.options.trades_required or world.is_universal_tracker:
                for trade in region_data.trades:
                    location = PokemonCrystalLocation(
                        world.player,
                        trade,
                        region,
                    )
                    location.show_in_spoiler = False
                    region.locations.append(location)

            if Goal.UNOWN_HUNT in world.options.goal:
                for sign in region_data.signs:
                    if sign not in world.generated_unown_signs: continue
                    location = PokemonCrystalLocation(
                        world.player,
                        f"{sign}_Encounter",
                        region
                    )
                    location.show_in_spoiler = False
                    location.place_locked_item(world.create_event("UNOWN", source=PokemonSourceLogic.STATICS))
                    region.locations.append(location)

                    location = PokemonCrystalLocation(
                        world.player,
                        sign,
                        region
                    )
                    location.show_in_spoiler = False
                    location.place_locked_item(world.create_event(world.generated_unown_signs[sign]))
                    region.locations.append(location)

    if world.options.randomize_lucky_number_show:
        trade_region = {t: rn for rn, rd in data.regions.items() for t in rd.trades}
        for i, trade_id in enumerate(world.generated_lucky_number_trades):
            region = regions[trade_region[trade_id]]
            location = PokemonCrystalLocation(world.player, f"Lucky Number Trade {i + 1}", region)
            location.show_in_spoiler = False
            location.place_locked_item(world.create_event(f"Lucky Number Trade {i + 1}"))
            region.locations.append(location)

    if world.options.dexsanity:
        if not world.is_universal_tracker:
            pokemon_items = sorted(world.pokemon_pool.get_filtered(world.options.dexsanity_logic))
            priority_pokemon = sorted(get_priority_dexsanity(world))
            excluded_pokemon = get_excluded_dexsanity(world)

            if world.options.dexsanity_starters.value == DexsanityStarters.option_block:
                excluded_pokemon.update(starter[0] for starter in world.generated_starters)
            pokemon_items = [pokemon_id for pokemon_id in pokemon_items if pokemon_id not in excluded_pokemon]
            world.random.shuffle(pokemon_items)
            world.random.shuffle(priority_pokemon)
            for _ in range(min(world.options.dexsanity.value, len(pokemon_items))):
                if priority_pokemon:
                    pokemon = priority_pokemon.pop()
                    if pokemon in pokemon_items:
                        world.generated_dexsanity.add(pokemon)
                        pokemon_items.remove(pokemon)
                        continue
                world.generated_dexsanity.add(pokemon_items.pop())

        pokedex_region = regions["Pokedex"]

        for pokemon_id in sorted(world.generated_dexsanity):
            pokemon_data = world.generated_pokemon[pokemon_id]
            new_location = PokemonCrystalLocation(
                world.player,
                f"Pokedex - {pokemon_data.friendly_name}",
                pokedex_region,
                rom_addresses=[pokemon_data.id],
                flag=POKEDEX_OFFSET + pokemon_data.id,
                tags=frozenset({"dexsanity"})
            )
            pokedex_region.locations.append(new_location)

    if world.options.battle_tower_sanity:
        vitamins = ["HP_UP", "PROTEIN", "IRON", "CARBOS", "CALCIUM"]
        for tier_idx in range(BATTLE_TOWER_NUM_TIERS):
            tier_region = regions[f"Battle Tower Tier {tier_idx + 1}"]
            new_location = PokemonCrystalLocation(
                world.player,
                f"Battle Tower - Tier {tier_idx + 1} Complete",
                tier_region,
                rom_addresses=[data.rom_addresses[f"AP_BattleTowerTierReward_{tier_idx + 1}"]],
                flag=BATTLE_TOWER_TIER_OFFSET + tier_idx,
                default_item_value=item_const_name_to_id(world.random.choice(vitamins)),
                tags=frozenset({"Battle Tower Tier"})
            )
            tier_region.locations.append(new_location)

        if world.options.battle_tower_sanity == BattleTowerSanity.option_tiers_and_trainers:
            trainer_rewards_base = data.rom_addresses["AP_BattleTowerTrainerRewards"]
            for canonical_idx, (cls, name) in enumerate(BATTLE_TOWER_TRAINERS):
                shuffled_pos = world.battle_tower_trainer_permutation.index(canonical_idx)
                tier_idx = shuffled_pos // BATTLE_TOWER_TRAINERS_PER_TIER
                tier_region = regions[f"Battle Tower Tier {tier_idx + 1}"]
                new_location = PokemonCrystalLocation(
                    world.player,
                    f"Battle Tower - {cls} {name}",
                    tier_region,
                    rom_addresses=[trainer_rewards_base + canonical_idx],
                    flag=BATTLE_TOWER_TRAINER_OFFSET + canonical_idx,
                    default_item_value=item_const_name_to_id("NO_ITEM"),
                    tags=frozenset({"Battle Tower Trainer"})
                )
                tier_region.locations.append(new_location)

    if world.options.rematchsanity:
        rewards_base = data.rom_addresses["AP_RematchTrainerRewards"]
        johto_only = bool(world.options.johto_only)
        pokemon_requests = bool(world.options.randomize_pokemon_requests)
        for label, ap_id, trainer, idx in all_rematch_locations():
            gate = trainer.tier_gates[idx]
            # KANTO-tier rematches are unreachable in a johto-only seed
            # (EVENT_RESTORED_POWER_TO_KANTO never fires); skip them so fill
            # can't place items behind permanently unreachable locations.
            if johto_only and gate == "EVENT_RESTORED_POWER_TO_KANTO":
                continue
            if trainer.pokemon_request_slot is not None and not pokemon_requests:
                continue
            parent_region = regions.get(trainer.region)
            if parent_region is None:
                continue
            canonical_idx = trainer.base_index + idx
            new_location = PokemonCrystalLocation(
                world.player,
                label,
                parent_region,
                rom_addresses=[rewards_base + canonical_idx],
                flag=ap_id,
                default_item_value=item_const_name_to_id("NO_ITEM"),
                tags=frozenset({"Rematchsanity"})
            )
            parent_region.locations.append(new_location)

    if world.options.dexcountsanity:
        if not world.is_universal_tracker:
            total_pokemon = len(world.pokemon_pool.get_filtered(world.options.dexsanity_logic))
            dexcountsanity_total = min(world.options.dexcountsanity.value, total_pokemon)
            dexcountsanity_step = world.options.dexcountsanity_step.value

            world.generated_dexcountsanity = [i for i in
                                              range(dexcountsanity_step, dexcountsanity_total, dexcountsanity_step)]

            if dexcountsanity_total not in world.generated_dexcountsanity:
                world.generated_dexcountsanity.append(dexcountsanity_total)

        pokedex_region = regions["Pokedex"]

        for dexcountsanity_count in world.generated_dexcountsanity[:-1]:
            new_location = PokemonCrystalLocation(
                world.player,
                f"Pokedex - Catch {dexcountsanity_count} Pokemon",
                pokedex_region,
                rom_addresses=[dexcountsanity_count],
                flag=POKEDEX_COUNT_OFFSET + dexcountsanity_count,
                tags=frozenset({"dexcountsanity"})
            )
            pokedex_region.locations.append(new_location)

        assert world.generated_dexcountsanity[-1]

        new_location = PokemonCrystalLocation(
            world.player,
            "Pokedex - Final Catch",
            pokedex_region,
            rom_addresses=[world.generated_dexcountsanity[-1]],
            flag=POKEDEX_COUNT_OFFSET + len(data.pokemon),
            tags=frozenset({"dexcountsanity"})
        )
        pokedex_region.locations.append(new_location)

    if world.options.evolution_methods_required or world.is_universal_tracker:
        evolution_region = regions["Evolutions"]
        created_locations = set()
        for pokemon_id, evos_access in sorted(world.logic.evolution.items(), key=lambda x: x[0]):
            for evolution, access in evos_access:
                if access is LogicalAccess.OutOfLogic and not world.is_universal_tracker: continue
                location_name = evolution_location_name(world, pokemon_id, evolution.pokemon)
                if location_name in created_locations: continue
                new_location = PokemonCrystalLocation(
                    world.player,
                    location_name,
                    evolution_region,
                    tags=frozenset({"evolution"})
                )
                new_location.show_in_spoiler = False
                new_location.place_locked_item(
                    world.create_event(evolution.pokemon, source=PokemonSourceLogic.EVOLUTION)
                )
                evolution_region.locations.append(new_location)
                created_locations.add(location_name)

    if world.options.breeding_methods_required or world.is_universal_tracker:
        breeding_region = regions["Breeding"]
        for pokemon_id, children_access in sorted(world.logic.breeding.items(), key=lambda x: x[0]):
            accesses = [access for _, access, _ in children_access]
            if LogicalAccess.InLogic not in accesses and not world.is_universal_tracker: continue
            new_location = PokemonCrystalLocation(
                world.player,
                f"Hatch {world.generated_pokemon[pokemon_id].friendly_name}",
                breeding_region,
                tags=frozenset({"breeding"})
            )
            new_location.show_in_spoiler = False
            new_location.place_locked_item(
                world.create_event(pokemon_id, source=PokemonSourceLogic.BREEDING)
            )
            breeding_region.locations.append(new_location)

    if world.options.shopsanity:
        for mart, mart_data in sorted(data.marts.items(), key=lambda x: x[0]):
            region_name = f"REGION_{mart}"
            if region_name in regions:
                region = regions[region_name]

                for i, item in enumerate(mart_data.items):
                    progress_type = LocationProgressType.EXCLUDED \
                        if (world.options.goal.value == {Goal.ELITE_FOUR}
                            and mart == "MART_ROOFTOP_SALE"
                            and world.options.exclude_post_goal_locations) else LocationProgressType.DEFAULT
                    new_location = PokemonCrystalLocation(
                        world.player,
                        f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}",
                        region,
                        tags=frozenset({"shopsanity"}),
                        flag=item.flag,
                        rom_addresses=[item.address],
                        default_item_value=item_const_name_to_id(item.item),
                        progress_type=progress_type
                    )
                    new_location.price = item.price
                    region.locations.append(new_location)

    if world.options.randomize_fly_unlocks:

        if world.options.randomize_fly_destinations:
            default_fly_item = lambda idx, fr: ((CANONICAL_ITEM_ID_MASK + 1) | (FLAG_ITEM_OFFSET + idx)
                    if fr.id != SILVER_CAVE_FLY_INDEX or
                        (world.options.randomize_fly_unlocks.value != RandomizeFlyUnlocks.option_exclude_silver_cave
                         and world.options.johto_only.value != JohtoOnly.option_on)
                    else FLAG_ITEM_OFFSET + fr.id)
        else:
            default_fly_item = lambda _, fr: FLAG_ITEM_OFFSET + fr.id

        for i, fly_region in enumerate(get_fly_regions(world)):
            parent_region = regions[fly_region.unlock_region]

            location = PokemonCrystalLocation(
                world.player,
                f"Visit {fly_region.name}",
                parent_region,
                tags=frozenset({"fly"}),
                flag=data.event_flags[f"EVENT_VISITED_{fly_region.base_identifier}"],
                rom_addresses=[data.rom_addresses[f"AP_FlyUnlock_{fly_region.base_identifier}"]],
                default_item_value=default_fly_item(i+1, fly_region)
            )

            parent_region.locations.append(location)

    # NB: the EVENT_VISITED_X events are placed in regions.json on the
    # appropriate city region (or :FLY sub-region), so randomize_fly_destinations
    # no longer needs to inject them separately.

    if world.options.grasssanity == Grasssanity.option_full:
        for region_id, grass in sorted(data.grass_tiles.items(), key=lambda x: x[0]):
            if region_id not in regions: continue
            grass_region = regions[f"{region_id}:GRASS"]

            for grass_tile in grass:
                grass_region.locations.append(
                    PokemonCrystalLocation(
                        player=world.player,
                        name=grass_tile.name,
                        parent=grass_region,
                        rom_addresses=[grass_tile.rom_address],
                        flag=grass_tile.flag,
                        tags=frozenset({"grass"}),
                    )
                )
    elif world.options.grasssanity == Grasssanity.option_one_per_area:
        for location_name, grass_regions in sorted(data.grass_regions.items(), key=lambda x: x[0]):
            region_grass = list[tuple[GrassTile, str]]()

            for region in grass_regions:
                if region not in regions: continue
                region_grass.extend((tile, region) for tile in data.grass_tiles[region])

            if not region_grass: continue

            if world.is_universal_tracker:
                region_tile, region_id = next(
                    (tile, id) for tile, id in region_grass if str(tile.flag) in world.grass_location_mapping)
            else:
                region_tile, region_id = world.random.choice(region_grass)

            flag = world.location_name_to_id[location_name]
            world.grass_location_mapping[str(region_tile.flag)] = flag
            grass_region = regions[f"{region_id}:GRASS"]
            location = PokemonCrystalLocation(
                player=world.player,
                name=location_name,
                parent=grass_region,
                flag=flag,
                rom_addresses=[region_tile.rom_address],
                tags=frozenset({"grass"}),
            )
            location.original_grass_flag = region_tile.flag
            grass_region.locations.append(location)
            location.item_rule = lambda item: item.name != "Grass"

    # Delete trainersanity locations if there are more than the amount specified in the settings
    def remove_excess_trainersanity(trainer_locations: Sequence[PokemonCrystalLocation], locs_to_remove: int):
        if locs_to_remove:
            priority_trainer_locations = [loc for loc in trainer_locations
                                          if loc.name in world.options.priority_locations.value]
            non_priority_trainer_locations = [loc for loc in trainer_locations
                                              if loc.name not in world.options.priority_locations.value]
            world.random.shuffle(priority_trainer_locations)
            world.random.shuffle(non_priority_trainer_locations)
            trainer_locations = non_priority_trainer_locations + priority_trainer_locations
            for location in trainer_locations:
                region = location.parent_region
                region.locations.remove(location)
                locs_to_remove -= 1
                if locs_to_remove <= 0:
                    break

    if (world.options.johto_trainersanity or world.options.kanto_trainersanity) and not world.is_universal_tracker:
        trainer_locations = [loc for loc in world.get_locations() if
                             "Trainersanity" in loc.tags and "Johto" in loc.tags]
        locs_to_remove = len(trainer_locations) - world.options.johto_trainersanity.value
        remove_excess_trainersanity(trainer_locations, locs_to_remove)

        trainer_locations = [loc for loc in world.get_locations() if
                             "Trainersanity" in loc.tags and "Johto" not in loc.tags]
        locs_to_remove = len(trainer_locations) - world.options.kanto_trainersanity.value
        remove_excess_trainersanity(trainer_locations, locs_to_remove)

    if WildEncounterMethodsRequired.BUG_CATCHING_CONTEST in world.options.wild_encounter_methods_required or world.is_universal_tracker:
        region = regions["REGION_NATIONAL_PARK:CONTEST"]

        for i in range(len(world.generated_contest)):
            location = PokemonCrystalLocation(
                player=world.player,
                name=f"Bug Catching Contest Slot {i + 1}",
                parent=region,
            )
            location.show_in_spoiler = False
            region.locations.append(location)


def create_location_label_to_id_map() -> dict[str, int]:
    """
    Creates a map from location labels to their AP location id (address)
    """

    next_grass_index = 1

    label_to_id_map: dict[str, int] = {}
    for region_data in data.regions.values():
        for location_name in region_data.locations:
            location_data = data.locations[location_name]
            label_to_id_map[location_data.label] = location_data.flag

        if region_data.name in data.grass_tiles:
            for tile in data.grass_tiles[region_data.name]:
                label_to_id_map[tile.name] = tile.flag
                next_grass_index += 1

    for mart, mart_data in data.marts.items():
        for i, item in enumerate(mart_data.items):
            if item.flag:
                label_to_id_map[f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}"] = item.flag

    for pokemon in data.pokemon.values():
        label_to_id_map[f"Pokedex - {pokemon.friendly_name}"] = pokemon.id + POKEDEX_OFFSET

    for i in range(1, len(data.pokemon)):
        label_to_id_map[f"Pokedex - Catch {i} Pokemon"] = i + POKEDEX_COUNT_OFFSET

    label_to_id_map["Pokedex - Final Catch"] = len(data.pokemon) + POKEDEX_COUNT_OFFSET

    for fly_region in data.fly_regions:
        label_to_id_map[f"Visit {fly_region.name}"] = data.event_flags[f"EVENT_VISITED_{fly_region.base_identifier}"]

    for index, region in enumerate(data.grass_regions.keys()):
        label_to_id_map[region] = index + GRASS_OFFSET + next_grass_index

    for tier_idx in range(BATTLE_TOWER_NUM_TIERS):
        label_to_id_map[f"Battle Tower - Tier {tier_idx + 1} Complete"] = BATTLE_TOWER_TIER_OFFSET + tier_idx

    for canonical_idx, (cls, name) in enumerate(BATTLE_TOWER_TRAINERS):
        label_to_id_map[f"Battle Tower - {cls} {name}"] = BATTLE_TOWER_TRAINER_OFFSET + canonical_idx

    for label, ap_id, _trainer, _idx in all_rematch_locations():
        label_to_id_map[label] = ap_id

    return label_to_id_map


DEXSANITY_LOCATIONS = {f"Pokedex - {pokemon.friendly_name}" for pokemon in data.pokemon.values()}
DEXCOUNTSANITY_LOCATIONS = {f"Pokedex - Catch {i + 1} Pokemon" for i in range(len(data.pokemon) - 1)} | {
    "Pokedex - Final Catch"}
BATTLE_TOWER_SANITY_LOCATIONS = {f"Battle Tower - Tier {n} Complete" for n in range(1, BATTLE_TOWER_NUM_TIERS + 1)}
BATTLE_TOWER_TRAINER_LOCATIONS = {f"Battle Tower - {cls} {name}" for cls, name in BATTLE_TOWER_TRAINERS}
REMATCH_LOCATIONS = {label for label, _id, _t, _i in all_rematch_locations()}

LOCATION_GROUPS: dict[str, set[str]] = {
    "Dexsanity": DEXSANITY_LOCATIONS,
    "Dexcountsanity": DEXCOUNTSANITY_LOCATIONS,
    "Dex": DEXSANITY_LOCATIONS | DEXCOUNTSANITY_LOCATIONS,
    "Battle Tower Tier": BATTLE_TOWER_SANITY_LOCATIONS,
    "Battle Tower Trainer": BATTLE_TOWER_TRAINER_LOCATIONS,
    "Battle Tower": BATTLE_TOWER_SANITY_LOCATIONS | BATTLE_TOWER_TRAINER_LOCATIONS,
    "Rematchsanity": REMATCH_LOCATIONS,
    "Shopsanity": {f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}" for mart, mart_data in
                   data.marts.items() for i, item in
                   enumerate(mart_data.items) if item.flag},
    "Fly Unlocks": {f"Visit {region.name}" for region in data.fly_regions},
    "Grass": {grass.name for region in data.grass_tiles.values() for grass in region}
             | {region for region in data.grass_regions.keys()}
}

excluded_location_tags = ("VanillaClairOn", "VanillaClairOff", "RequiresSaffronGatehouses", "Badge", "NPCGift",
                          "Hidden", "KeyItem", "HM", "BillsGrandpa", "BerryTree", "ContestAll",
                          "ContestCombineSecondThird", "PokemonRequest")

for location in data.locations.values():
    for tag in location.tags:
        if tag in excluded_location_tags:
            continue
        if tag not in LOCATION_GROUPS:
            LOCATION_GROUPS[tag] = set()
        LOCATION_GROUPS[tag].add(location.label)


def _area_group(region_name: str) -> str:
    region = data.regions[region_name]
    return "Johto" if region.johto or region.silver_cave else "Kanto"


_mart_regions = {mart: region_name for region_name, region in data.regions.items() for mart in region.marts}
for mart, mart_data in data.marts.items():
    LOCATION_GROUPS[_area_group(_mart_regions[mart])].update(
        f"{mart_data.friendly_name} - {get_mart_slot_location_name(mart, i)}"
        for i, item in enumerate(mart_data.items) if item.flag)

for fly_region in data.fly_regions:
    johto = fly_region.johto or fly_region.id == SILVER_CAVE_FLY_INDEX
    LOCATION_GROUPS["Johto" if johto else "Kanto"].add(f"Visit {fly_region.name}")

for region_name, grass in data.grass_tiles.items():
    LOCATION_GROUPS[_area_group(region_name)].update(tile.name for tile in grass)

for location_name, grass_regions in data.grass_regions.items():
    LOCATION_GROUPS[_area_group(grass_regions[0])].add(location_name)

for label, _id, trainer, _i in all_rematch_locations():
    LOCATION_GROUPS[_area_group(trainer.region)].add(label)

LOCATION_GROUPS["Johto"].update(BATTLE_TOWER_SANITY_LOCATIONS | BATTLE_TOWER_TRAINER_LOCATIONS)

for pokemon in data.pokemon.values():
    location = f"Pokedex - {pokemon.friendly_name}"
    if location in DEXSANITY_LOCATIONS:
        LOCATION_GROUPS[pokemon.friendly_name] = {location}

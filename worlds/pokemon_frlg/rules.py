"""
Logic rule definitions for Pokémon FireRed and LeafGreen
"""
import re
from collections import defaultdict
from typing import TYPE_CHECKING, Dict, List, Set, Tuple, cast, Iterable

from BaseClasses import CollectionRule, CollectionState
from rule_builder.rules import CanReachRegion, False_, Has, HasAll, HasAny, HasFromListUnique, OptionFilter, Rule, True_

from .data import data, NAME_TO_SPECIES_ID, EvolutionMethodEnum, LocationCategory
from .items import PokemonFRLGGlitchedToken
from .locations import PokemonFRLGLocation
from .logic import (CanBuyCoins, CanCut, CanFlash, CanFly, CanLeavePewter, CanLeaveViridian, CanPushMansionSwitch,
                    CanRockSmash, CanShowSelphyPokemon, CanStopSeafoamB3FCurrent, CanStopSeafoamB4FCurrent, CanStrength,
                    CanSurf, CanWaterfall, HasBadgeRequirement, HasCardKey, HasCeruleanCaveRequirement,
                    HasE4Requirements, HasE4RematchRequirements, HasIslandPass, HasNGyms, HasNPokemon, HasPokemon,
                    HasPokemonForEvolution, HasTradePokemon, HasRoute22GateRequirements, HasRoute23GuardRequirements,
                    HasViridianGymRequirements, HasWildPokemon, JumpDownLedge, JumpUpLedge, NotRandomizingEntrances,
                    PostGameFame, TrainerRematch, TwoIslandStallExpansion)
from .options import (BlockPokemonTower, BlockUndergroundPaths, BlockVermilionSailing, CardKey, DiglettsCaveRoadblock,
                      ElevatorsCondition, ExtraKeyItems, FameCheckerRequired, FlashRequired, Goal, GymKeys,
                      IslandPasses, ItemfinderRequired, OpenSilphCo, RemoveCeruleanCityRoadblocks, RemoveSaffronRockets,
                      Route9Roadblock, Route10Waterfall, Route12Boulders, Route12Rocks, Route16Rock, Route23Trees,
                      Route23Waterfall, VictoryRoadRocks)
from .pokemon import add_hm_compatability
from .util import HM_TO_COMPATIBILITY_ID, int_to_bool_array

if TYPE_CHECKING:
    from .world import PokemonFRLGWorld

EVO_METHODS_LEVEL = {
    EvolutionMethodEnum.LEVEL,
    EvolutionMethodEnum.LEVEL_NINJASK,
    EvolutionMethodEnum.LEVEL_SHEDINJA
}

EVO_METHODS_TYROGUE_LEVEL = {
    EvolutionMethodEnum.LEVEL_ATK_LT_DEF,
    EvolutionMethodEnum.LEVEL_ATK_EQ_DEF,
    EvolutionMethodEnum.LEVEL_ATK_GT_DEF
}

EVO_METHODS_WURMPLE_LEVEL = {
    EvolutionMethodEnum.LEVEL_SILCOON,
    EvolutionMethodEnum.LEVEL_CASCOON
}

EVO_METHODS_LEVEL_ANY = {*EVO_METHODS_LEVEL, *EVO_METHODS_TYROGUE_LEVEL, *EVO_METHODS_WURMPLE_LEVEL}

EVO_METHODS_ITEM = {
    EvolutionMethodEnum.ITEM
}

EVO_METHODS_HELD_ITEM = {
    EvolutionMethodEnum.ITEM_HELD
}

EVO_METHODS_FRIENDSHIP = {
    EvolutionMethodEnum.FRIENDSHIP
}

CARD_KEYS_PER_FLOOR = {floor: ("Card Key", f"Card Key {floor}F") for floor in range(2, 12)}


class PokemonFRLGLogic:
    player: int
    compatible_hm_pokemon: Dict[str, List[str]]
    evo_methods_required: Set[EvolutionMethodEnum]
    required_trade_pokemon: Dict[str, str]
    resort_gorgeous_pokemon: int
    card_keys: Dict[int, str]
    island_passes: Dict[int, Tuple[str, int]]
    wild_pokemon: List[str]
    static_pokemon: List[str]
    evolved_pokemon: List[str]
    world_item_id_map: Dict[int, str]
    dexsanity_requires_evos: bool
    hms_require_evos: bool
    oaks_aides_require_evos: bool
    randomizing_entrances: bool
    guaranteed_hm_access: bool
    bicycle_requires_jumping_shoes: bool
    acrobatic_bicycle: bool
    rematches_require_gyms: bool
    dexsanity_state_item_names_lookup: Dict[str, Tuple[str, ...]]
    oaks_aides_species_item_names: List[Tuple[str, ...]]
    pokemon_hm_use: Dict[str, List[str]]
    evolution_state_item_names_lookup: Dict[str, List[str]]

    def __init__(self, player: int, item_id_to_name: Dict[int, str]) -> None:
        self.player = player
        self.compatible_hm_pokemon = defaultdict(list)
        self.evo_methods_required = set()
        self.required_trade_pokemon = {}
        self.resort_gorgeous_pokemon = data.constants["SPECIES_PIKACHU"]
        self.island_passes = {}
        self.wild_pokemon = []
        self.static_pokemon = []
        self.evolved_pokemon = []
        self.world_item_id_map = item_id_to_name
        self.dexsanity_requires_evos = False
        self.hms_require_evos = False
        self.oaks_aides_require_evos = False
        self.randomizing_entrances = False
        self.guaranteed_hm_access = False
        self.bicycle_requires_jumping_shoes = True
        self.acrobatic_bicycle = False
        self.rematches_require_gyms = True
        self.dexsanity_state_item_names_lookup = {}
        self.oaks_aides_species_item_names = []
        self.evolution_state_item_names_lookup = {}

    def update_hm_compatible_pokemon(self):
        pokemon_hm_use = defaultdict(list)
        for hm, species_list in self.compatible_hm_pokemon.items():
            hm_logic_name = f"Teach {hm}"
            for species in species_list:
                pokemon_hm_use[species].append(hm_logic_name)
                if self.hms_require_evos:
                    pokemon_hm_use[f"Evolved {species}"].append(hm_logic_name)
        self.pokemon_hm_use = pokemon_hm_use

    def add_hm_compatible_pokemon(self, hm: str, species: str):
        self.compatible_hm_pokemon[hm].append(species)
        hm_logic_name = f"Teach {hm}"
        self.pokemon_hm_use.setdefault(species, []).append(hm_logic_name)
        if self.hms_require_evos:
            self.pokemon_hm_use.setdefault(f"Evolved {species}", []).append(hm_logic_name)

    def has_pokemon(self, state: CollectionState, pokemon: str) -> bool:
        return state.has_any(self.dexsanity_state_item_names_lookup[pokemon], self.player)

    def has_pokemon_for_evolution(self, state: CollectionState, pokemon: str) -> bool:
        return state.has_any(self.evolution_state_item_names_lookup[pokemon], self.player)

    def has_n_pokemon(self, state: CollectionState, n: int) -> bool:
        if n <= 0:
            return True
        player = self.player
        for species_item_names in self.oaks_aides_species_item_names:
            # There are multiple item names for a species that can provide Pokédex progress for that species.
            if state.has_any(species_item_names, player):
                # Subtraction is used to make use of a common programming performance 'trick' where, comparing two
                # variables, e.g. `if count == n`, can be replaced with comparing a variable and a constant, e.g.
                # `if n == 0`.
                n -= 1
                # Further minor optimization of `if n == 0` -> `if not n`
                if not n:
                    return True
        return False

    def has_trade_pokemon(self, state: CollectionState, location_name: str) -> bool:
        return state.has(self.required_trade_pokemon[location_name], self.player)

    def can_show_selphy_pokemon(self, state: CollectionState) -> bool:
        return state.has_all(("Rescue Selphy", data.species[self.resort_gorgeous_pokemon].name), self.player)

    def update_species(self, world: "PokemonFRLGWorld"):
        """
        Update available species items used in logic for oak's aide, dexsanity and Pokémon request locations, for the
        wild/static/legendary/evolution Pokémon events that exist in the world.
        """
        pokemon_event_categories = {
            LocationCategory.EVENT_WILD_POKEMON,
            LocationCategory.EVENT_STATIC_POKEMON,
            LocationCategory.EVENT_LEGENDARY_POKEMON,
            LocationCategory.EVENT_EVOLUTION_POKEMON,
        }

        pokemon_events_that_exist = [location for location
                                     in cast(Iterable[PokemonFRLGLocation], world.get_locations())
                                     if location.category in pokemon_event_categories and location.advancement]
        assert pokemon_events_that_exist

        if not self.oaks_aides_require_evos:
            # Filter out evolutions.
            evolution_category = LocationCategory.EVENT_EVOLUTION_POKEMON
            oaks_aide_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist
                                                      if location.category is not evolution_category}
        else:
            oaks_aide_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist}

        if not self.dexsanity_requires_evos:
            # Filter out evolutions.
            evolution_category = LocationCategory.EVENT_EVOLUTION_POKEMON
            dexsanity_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist
                                                      if location.category is not evolution_category}
        else:
            dexsanity_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist}

        evolution_relevant_pokemon_event_names = {location.item.name for location in pokemon_events_that_exist}

        oaks_aides_species_item_names = []
        dexsanity_state_item_names = {}
        evolution_state_item_names = {}
        for species in data.species.values():
            species_name = species.name
            static_species_name = f"Static {species_name}"
            evolved_species_name = f"Evolved {species_name}"

            oaks_aide_item_names = []
            dexsanity_item_names = []
            for name in (species_name, static_species_name, evolved_species_name):
                if name in oaks_aide_relevant_pokemon_event_names:
                    oaks_aide_item_names.append(name)
                if name in dexsanity_relevant_pokemon_event_names:
                    dexsanity_item_names.append(name)

            if oaks_aide_item_names:
                oaks_aides_species_item_names.append(tuple(oaks_aide_item_names))

            dexsanity_state_item_names[species_name] = tuple(dexsanity_item_names)

            evolution_item_names = []
            for name in (species_name, evolved_species_name):
                if name in evolution_relevant_pokemon_event_names:
                    evolution_item_names.append(name)

            evolution_state_item_names[species_name] = tuple(evolution_item_names)

        self.oaks_aides_species_item_names[:] = oaks_aides_species_item_names
        self.dexsanity_state_item_names_lookup.update(dexsanity_state_item_names)
        self.evolution_state_item_names_lookup.update(evolution_state_item_names)


def set_logic_options(world: "PokemonFRLGWorld") -> None:
    logic = world.logic

    if world.options.card_key.value == CardKey.option_vanilla:
        logic.card_keys = {floor: "Card Key" for floor in range(2, 12)}
    elif world.options.card_key.value in {CardKey.option_split, CardKey.option_progressive}:
        logic.card_keys = {floor: f"Card Key {floor}F" for floor in range(2, 12)}

    if world.options.island_passes.value in {IslandPasses.option_vanilla, IslandPasses.option_progressive}:
        logic.island_passes[1] = ("Tri Pass", 1)
        logic.island_passes[2] = ("Tri Pass", 1)
        logic.island_passes[3] = ("Tri Pass", 1)
        logic.island_passes[4] = ("Rainbow Pass", 2)
        logic.island_passes[5] = ("Rainbow Pass", 2)
        logic.island_passes[6] = ("Rainbow Pass", 2)
        logic.island_passes[7] = ("Rainbow Pass", 2)
    elif world.options.island_passes.value in {IslandPasses.option_split, IslandPasses.option_progressive_split}:
        logic.island_passes[1] = ("One Pass", 1)
        logic.island_passes[2] = ("Two Pass", 2)
        logic.island_passes[3] = ("Three Pass", 3)
        logic.island_passes[4] = ("Four Pass", 4)
        logic.island_passes[5] = ("Five Pass", 5)
        logic.island_passes[6] = ("Six Pass", 6)
        logic.island_passes[7] = ("Seven Pass", 7)

    logic.dexsanity_requires_evos = "Dexsanity" in world.options.evolutions_required.value
    logic.hms_require_evos = "HM Requirement" in world.options.evolutions_required.value
    logic.oaks_aides_require_evos = "Oak's Aides" in world.options.evolutions_required.value
    logic.bicycle_requires_jumping_shoes = bool(world.options.bicycle_requires_jumping_shoes.value)
    logic.acrobatic_bicycle = bool(world.options.acrobatic_bicycle.value)
    logic.rematches_require_gyms = bool(world.options.rematch_requirements)

    # Until locations have been created, assume all Pokémon species are present in the world.
    dexsanity_state_item_names = {}
    oaks_aides_species_item_names = []
    evolution_state_item_names = {}
    for species in data.species.values():
        species_name = species.name

        if logic.dexsanity_requires_evos and species.pre_evolution is not None:
            state_item_names = (species_name, f"Static {species_name}", f"Evolved {species_name}")
        else:
            state_item_names = (species_name, f"Static {species_name}")
        dexsanity_state_item_names[species_name] = state_item_names

        if logic.oaks_aides_require_evos and species.pre_evolution is not None:
            oaks_aide_item_names = (species_name, f"Static {species_name}", f"Evolved {species_name}")
        else:
            oaks_aide_item_names = (species_name, f"Static {species_name}")
        oaks_aides_species_item_names.append(oaks_aide_item_names)

        evolution_item_names = (species_name, f"Evolved {species_name}")
        evolution_state_item_names[species_name] = evolution_item_names

    logic.dexsanity_state_item_names_lookup.update(dexsanity_state_item_names)
    logic.oaks_aides_species_item_names[:] = oaks_aides_species_item_names
    logic.evolution_state_item_names_lookup.update(evolution_state_item_names)

    if "Level" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_LEVEL)
    if "Level Tyrogue" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_TYROGUE_LEVEL)
    if "Level Wurmple" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_WURMPLE_LEVEL)
    if "Evo Item" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_ITEM)
    if "Evo & Held Item" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_HELD_ITEM)
    if "Friendship" in world.options.evolution_methods_required.value:
        logic.evo_methods_required.update(EVO_METHODS_FRIENDSHIP)


def _get_evolution_rule(world: "PokemonFRLGWorld", location: PokemonFRLGLocation) -> Rule:
    pokemon = location.name.split(" - ")[1].strip()
    pokemon_species_name = re.sub(r' \d+', '', pokemon)
    evo_data = data.evolutions[pokemon]
    evo_method = evo_data.method
    logic = world.logic
    if evo_method in EVO_METHODS_ITEM:
        use_item = logic.world_item_id_map[evo_data.param]
        return HasPokemonForEvolution(pokemon_species_name) & Has(use_item)
    elif evo_method in EVO_METHODS_HELD_ITEM:
        items = (logic.world_item_id_map[evo_data.param], logic.world_item_id_map[evo_data.param2])
        return HasPokemonForEvolution(pokemon_species_name) & HasAll(*items)
    elif evo_method in EVO_METHODS_LEVEL_ANY:
        gyms_requirement = evo_data.param // 7
        return HasPokemonForEvolution(pokemon_species_name) & HasNGyms(gyms_requirement)
    elif evo_method in EVO_METHODS_FRIENDSHIP:
        return HasPokemonForEvolution(pokemon_species_name)
    else:
        raise RuntimeError(f"Unexpected evo method: {evo_method}")


def set_rules(world: "PokemonFRLGWorld") -> None:
    entrance_rules: defaultdict[str, Rule] = defaultdict(True_)
    location_rules: defaultdict[str, Rule] = defaultdict(True_)

    world.set_completion_rule(
        Has("Defeat Champion", options=[OptionFilter(Goal, Goal.option_champion)]) |
        Has("Defeat Champion (Rematch)", options=[OptionFilter(Goal, Goal.option_champion_rematch)])
    )

    if world.options.pokemon_request_locations and not world.options.kanto_only:
        if not world.is_universal_tracker:
            world.logic.resort_gorgeous_pokemon = NAME_TO_SPECIES_ID[world.random.choice(world.logic.wild_pokemon)]
        else:
            world.logic.resort_gorgeous_pokemon = world.ut_slot_data["resort_gorgeous_pokemon"]

    # Sky
    entrance_rules["Flying"] = CanFly()
    entrance_rules["Pallet Town Fly Destination"] = Has("Fly Unlock (Pallet Town)")
    entrance_rules["Viridian City Fly Destination"] = Has("Fly Unlock (Viridian City)")
    entrance_rules["Pewter City Fly Destination"] = Has("Fly Unlock (Pewter City)")
    entrance_rules["Route 4 Fly Destination"] = Has("Fly Unlock (Route 4)")
    entrance_rules["Cerulean City Fly Destination"] = Has("Fly Unlock (Cerulean City)")
    entrance_rules["Vermilion City Fly Destination"] = Has("Fly Unlock (Vermilion City)")
    entrance_rules["Route 10 Fly Destination"] = Has("Fly Unlock (Route 10)")
    entrance_rules["Lavender Town Fly Destination"] = Has("Fly Unlock (Lavender Town)")
    entrance_rules["Celadon City Fly Destination"] = Has("Fly Unlock (Celadon City)")
    entrance_rules["Fuchsia City Fly Destination"] = Has("Fly Unlock (Fuchsia City)")
    entrance_rules["Saffron City Fly Destination"] = Has("Fly Unlock (Saffron City)")
    entrance_rules["Cinnabar Island Fly Destination"] = Has("Fly Unlock (Cinnabar Island)")
    entrance_rules["Indigo Plateau Fly Destination"] = Has("Fly Unlock (Indigo Plateau)")
    entrance_rules["One Island Fly Destination"] = Has("Fly Unlock (One Island)")
    entrance_rules["Two Island Fly Destination"] = Has("Fly Unlock (Two Island)")
    entrance_rules["Three Island Fly Destination"] = Has("Fly Unlock (Three Island)")
    entrance_rules["Four Island Fly Destination"] = Has("Fly Unlock (Four Island)")
    entrance_rules["Five Island Fly Destination"] = Has("Fly Unlock (Five Island)")
    entrance_rules["Six Island Fly Destination"] = Has("Fly Unlock (Six Island)")
    entrance_rules["Seven Island Fly Destination"] = Has("Fly Unlock (Seven Island)")

    # Seagallop
    entrance_rules["Depart Seagallop (Vermilion City)"] = (
        Has(
            "S.S. Ticket",
            options=[OptionFilter(BlockVermilionSailing, BlockVermilionSailing.option_true)],
            filtered_resolution=True
        )
    )
    entrance_rules["Depart Seagallop (One Island)"] = HasIslandPass(1)
    entrance_rules["Depart Seagallop (Two Island)"] = HasIslandPass(2)
    entrance_rules["Depart Seagallop (Three Island)"] = HasIslandPass(3)
    entrance_rules["Depart Seagallop (Four Island)"] = HasIslandPass(4)
    entrance_rules["Depart Seagallop (Five Island)"] = HasIslandPass(5)
    entrance_rules["Depart Seagallop (Six Island)"] = HasIslandPass(6)
    entrance_rules["Depart Seagallop (Seven Island)"] = HasIslandPass(7)
    entrance_rules["Depart Seagallop (Navel Rock)"] = (
        Has("Mystic Ticket") &
        (
            CanReachRegion("Vermilion City") | CanReachRegion("Vermilion City (Near Harbor)")
        )
    )
    entrance_rules["Depart Seagallop (Birth Island)"] = (
        Has("Aurora Ticket") &
        (
            CanReachRegion("Vermilion City") | CanReachRegion("Vermilion City (Near Harbor)")
        )
    )

    # Pallet Town
    location_rules["Rival's House - Daisy Gift"] = Has("Deliver Oak's Parcel")
    location_rules["Professor Oak's Lab - Oak's Delivery"] = Has("Oak's Parcel")
    location_rules["Professor Oak's Lab - Oak Gift 1 (Deliver Parcel)"] = Has("Oak's Parcel")
    location_rules["Professor Oak's Lab - Oak Gift 2 (Deliver Parcel)"] = Has("Oak's Parcel")
    location_rules["Professor Oak's Lab - Oak Info"] = Has("Oak's Parcel")
    location_rules["Professor Oak's Lab - Oak Gift (Post Route 22 Rival)"] = Has("Defeat Route 22 Rival")
    location_rules["Professor Oak's Lab - Oak's Aide M Info (Right)"] = PostGameFame()
    location_rules["Professor Oak's Lab - Oak's Aide M Info (Left)"] = PostGameFame()

    entrance_rules["Pallet Town Surfing Spot"] = CanSurf()

    # Viridian City
    location_rules["Viridian City - Tutorial Man Gift"] = CanLeaveViridian()
    location_rules["Viridian City - Old Man Gift"] = HasViridianGymRequirements()
    location_rules["Viridian Gym - Hidden Item Under Giovanni"] = Has("Itemfinder")
    location_rules["Viridian Gym - Gym Guy Info"] = Has("Defeat Giovanni")

    entrance_rules["Viridian City Roadblock (Bottom)"] = CanLeaveViridian()
    entrance_rules["Viridian City Roadblock (Top)"] = CanLeaveViridian()
    entrance_rules["Viridian City Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Viridian City Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Viridian City Cuttable Tree (Left)"] = CanCut()
    entrance_rules["Viridian City Cuttable Tree (Right)"] = CanCut()
    entrance_rules["Viridian City Surfing Spot"] = CanSurf()
    entrance_rules["Viridian Gym Entrance"] = (
        HasViridianGymRequirements() &
        Has("Viridian Key", options=[OptionFilter(GymKeys, GymKeys.option_true)], filtered_resolution=True)
    )

    # Route 22
    location_rules["Route 22 - Early Rival Battle"] = Has("Deliver Oak's Parcel")
    location_rules["Route 22 - Early Rival Reward"] = Has("Deliver Oak's Parcel")
    location_rules["Route 22 Early Rival Scaling"] = Has("Deliver Oak's Parcel")
    location_rules["Route 22 - Late Rival Reward"] = HasAll("Defeat Route 22 Rival", "Defeat Giovanni")
    location_rules["Route 22 - Late Rival Scaling"] = HasAll("Defeat Route 22 Rival", "Defeat Giovanni")

    entrance_rules["Route 22 North Ledge"] = JumpDownLedge()
    entrance_rules["Route 22 South Ledge"] = JumpDownLedge()
    entrance_rules["Route 22 Surfing Spot (East)"] = CanSurf()
    entrance_rules["Route 22 Surfing Spot (West)"] = CanSurf()
    entrance_rules["Route 22 Gate North Exit"] = HasRoute22GateRequirements()

    # Route 2
    location_rules["Route 2 Gate - Oak's Aide Gift (Pokedex Progress)"] = (
        HasNPokemon(world.options.oaks_aide_route_2.value) & Has("Pokedex")
    )
    location_rules["Route 2 Trade House - Trade Pokemon"] = (
        HasTradePokemon("Route 2 Trade House - Trade Pokemon") & Has("Pokedex")
    )

    entrance_rules["Route 2 South Cuttable Trees (Left)"] = CanCut()
    entrance_rules["Route 2 South Cuttable Trees (Right)"] = CanCut()
    entrance_rules["Route 2 North Cuttable Tree (Top)"] = (
        CanCut() & OptionFilter(DiglettsCaveRoadblock, DiglettsCaveRoadblock.option_vanilla)
    )
    entrance_rules["Route 2 North Cuttable Tree (Bottom)"] = (
        CanCut() & OptionFilter(DiglettsCaveRoadblock, DiglettsCaveRoadblock.option_vanilla)
    )
    entrance_rules["Route 2 Smashable Rock (Top)"] = (
        CanRockSmash() & OptionFilter(DiglettsCaveRoadblock, DiglettsCaveRoadblock.option_rock_smash)
    )
    entrance_rules["Route 2 Smashable Rock (Bottom)"] = (
        CanRockSmash() & OptionFilter(DiglettsCaveRoadblock, DiglettsCaveRoadblock.option_rock_smash)
    )
    entrance_rules["Route 2 Center Cuttable Tree (Top)"] = CanCut()
    entrance_rules["Route 2 Center Cuttable Tree (Bottom)"] = CanCut()

    # Pewter City
    location_rules["Pewter City - Gift from Mom"] = Has("Defeat Brock")

    entrance_rules["Pewter City Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Pewter City Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Pewter City Cuttable Tree (Right)"] = CanCut()
    entrance_rules["Pewter City Cuttable Tree (Left)"] = CanCut()
    entrance_rules["Pewter City Roadblock (Left)"] = CanLeavePewter()
    entrance_rules["Pewter City Roadblock (Right)"] = CanLeavePewter()
    entrance_rules["Pewter Gym Entrance"] = Has(
        "Pewter Key", options=[OptionFilter(GymKeys, GymKeys.option_true)], filtered_resolution=True
    )

    # Route 3
    location_rules["Route 3 - Lass Janice Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 3 - Lass Janice Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 3 - Bug Catcher Colton Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 3 - Bug Catcher Colton Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 3 - Bug Catcher Colton Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 3 - Youngster Ben Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 3 - Youngster Ben Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 3 - Youngster Ben Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Route 3 Ledge"] = JumpDownLedge()

    # Route 4
    entrance_rules["Route 4 Southeast Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Route 4 Northeast Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Route 4 Southeast Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Route 4 Northeast Ledge (Top)"] = JumpDownLedge()

    # Cerulean City
    location_rules["Cerulean Trade House - Trade Pokemon"] = (
        HasTradePokemon("Cerulean Trade House - Trade Pokemon") & Has("Pokedex")
    )
    location_rules["Cerulean Pokemon Center 1F - Bookshelf Info"] = PostGameFame()
    location_rules["Cerulean Gym - Hidden Item in Water"] = CanSurf() & Has("Itemfinder")
    location_rules["Bike Shop - Bicycle Purchase"] = Has("Bike Voucher")
    location_rules["Berry Powder Man's House - Berry Powder Man Gift"] = Has("Berry Pouch")

    entrance_rules["Cerulean City Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Cerulean City Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Cerulean City Cuttable Tree (Top)"] = (
        CanCut() &
        Has(
            "Help Bill",
            options=[OptionFilter(RemoveCeruleanCityRoadblocks, RemoveCeruleanCityRoadblocks.option_false)],
            filtered_resolution=True
        )
    )
    entrance_rules["Cerulean City Cuttable Tree (Bottom)"] = (
        CanCut() &
        Has(
            "Help Bill",
            options=[OptionFilter(RemoveCeruleanCityRoadblocks, RemoveCeruleanCityRoadblocks.option_false)],
            filtered_resolution=True
        )
    )
    entrance_rules["Robbed House Front Entrance"] = (
        Has(
            "Help Bill",
            options=[OptionFilter(RemoveCeruleanCityRoadblocks, RemoveCeruleanCityRoadblocks.option_false)],
            filtered_resolution=True
        )
    )
    entrance_rules["Cerulean Gym Entrance"] = Has(
        "Cerulean Key", options=[OptionFilter(GymKeys, GymKeys.option_true)], filtered_resolution=True
    )
    entrance_rules["Cerulean City East Exit"] = (
        (CanCut() & OptionFilter(Route9Roadblock, Route9Roadblock.option_vanilla)) |
        (CanRockSmash() & OptionFilter(Route9Roadblock, Route9Roadblock.option_rock_smash))
    )
    entrance_rules["Cerulean City Surfing Spot"] = CanSurf()
    entrance_rules["Cerulean Cave Entrance"] = HasCeruleanCaveRequirement()

    # Route 24
    location_rules["Route 24 - Youngster Timmy Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 24 - Youngster Timmy Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 24 - Youngster Timmy Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 24 - Lass Reli Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 24 - Lass Reli Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)

    entrance_rules["Route 24 Surfing Spot"] = CanSurf()

    # Route 25
    location_rules["Route 25 - Hiker Franklin Rematch Reward (2 Badges/Gyms)"] = TrainerRematch(2)
    location_rules["Route 25 - Picnicker Kelsey Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 25 - Picnicker Kelsey Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 25 - Picnicker Kelsey Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 25 - Item Near Bush"] = CanCut()
    location_rules["Route 25 - Youngster Chad Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 25 - Youngster Chad Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 25 - Youngster Chad Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Route 25 Surfing Spot"] = CanSurf()

    # Route 5
    entrance_rules["Route 5 North Ledge"] = JumpDownLedge()
    entrance_rules["Route 5 Center Ledge"] = JumpDownLedge()
    entrance_rules["Route 5 South Ledge"] = JumpDownLedge()
    entrance_rules["Route 5 Open Path (Top)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 5 Open Path (Bottom)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 5 Smashable Rocks (Top)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 5 Smashable Rocks (Bottom)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 5 Gate Guard Checkpoint (Top)"] = HasAny("Tea", "Blue Tea")
    entrance_rules["Route 5 Gate Guard Checkpoint (Bottom)"] = HasAny("Tea", "Blue Tea")

    # Underground Path North-South Tunnel
    location_rules["Underground Path North Entrance - Trade Pokemon"] = (
        HasTradePokemon("Underground Path North Entrance - Trade Pokemon") & Has("Pokedex")
    )

    # Route 6
    location_rules["Route 6 - Camper Ricky Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 6 - Camper Ricky Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 6 - Camper Ricky Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 6 - Picnicker Isabelle Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 6 - Picnicker Isabelle Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 6 - Picnicker Isabelle Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 6 - Camper Jeff Rematch Reward"] = TrainerRematch(0)
    location_rules["Route 6 - Camper Jeff Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 6 - Camper Jeff Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    entrance_rules["Route 6 Open Path (Bottom)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 6 Open Path (Top)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 6 Smashable Rocks (Bottom)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 6 Smashable Rocks (Top)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 6 Surfing Spot"] = CanSurf()
    entrance_rules["Route 6 Gate Guard Checkpoint (Bottom)"] = HasAny("Tea", "Red Tea")
    entrance_rules["Route 6 Gate Guard Checkpoint (Top)"] = HasAny("Tea", "Red Tea")

    # Vermilion City
    location_rules["Vermilion Pokemon Center 1F - Bookshelf Info"] = Has("Defeat Lt. Surge")
    location_rules["Pokemon Fan Club - Worker Info"] = PostGameFame()
    location_rules["Vermilion Trade House - Trade Pokemon"] = (
        HasTradePokemon("Vermilion Trade House - Trade Pokemon") & Has("Pokedex")
    )

    entrance_rules["Vermilion City Cuttable Tree (Top)"] = CanCut()
    entrance_rules["Vermilion City Cuttable Tree (Bottom)"] = CanCut()
    entrance_rules["Vermilion City Checkpoint (Top)"] = Has("S.S. Ticket")
    entrance_rules["Vermilion City Checkpoint (Bottom)"] = Has("S.S. Ticket")
    entrance_rules["Vermilion City Surfing Spot"] = CanSurf()
    entrance_rules["Vermilion City Surfing Spot (Near Gym)"] = CanSurf()
    entrance_rules["Vermilion Gym Entrance"] = (
        Has("Vermilion Key", options=[OptionFilter(GymKeys, GymKeys.option_true)], filtered_resolution=True)
    )
    entrance_rules["Board Seagallop (Vermilion Harbor)"] = (
        HasIslandPass(1) | HasIslandPass(2) | HasIslandPass(3) | HasIslandPass(4) | HasIslandPass(5) |
        HasIslandPass(6) | HasIslandPass(7) | HasAny("Mystic Ticket", "Aurora Ticket")
    )

    # S.S. Anne
    entrance_rules["S.S. Anne Exterior Surfing Spot"] = CanSurf()

    # Route 11
    location_rules["Route 11 - Engineer Bernie Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 11 - Youngster Yasu Rematch Reward (2 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 11 - Youngster Yasu Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 11 - Gamer Darian Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 11 Gate 2F - Oak's Aide Gift (Pokedex Progress)"] = (
        HasNPokemon(world.options.oaks_aide_route_11.value) & Has("Pokedex")
    )
    location_rules["Route 11 Gate 2F - Trade Pokemon"] = (
        HasTradePokemon("Route 11 Gate 2F - Trade Pokemon") & Has("Pokedex")
    )

    entrance_rules["Route 11 Surfing Spot"] = CanSurf()
    entrance_rules["Route 11 East Exit"] = (
        True_(options=[OptionFilter(Route12Boulders, Route12Boulders.option_false)]) |
        (CanStrength() & OptionFilter(Route12Boulders, Route12Boulders.option_true))
    )

    # Route 9
    location_rules["Route 9 - Picnicker Alicia Rematch Reward (2 Badges/Gyms)"] = TrainerRematch(2)
    location_rules["Route 9 - Picnicker Alicia Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 9 - Picnicker Alicia Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 9 - Hiker Jeremy Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 9 - Camper Chris Rematch Reward (2 Badges/Gyms)"] = TrainerRematch(2)
    location_rules["Route 9 - Camper Chris Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 9 - Camper Chris Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    entrance_rules["Route 9 West Exit"] = (
            (CanCut() & OptionFilter(Route9Roadblock, Route9Roadblock.option_vanilla)) |
            (CanRockSmash() & OptionFilter(Route9Roadblock, Route9Roadblock.option_rock_smash))
    )
    entrance_rules["Route 9 Southwest Ledge"] = JumpDownLedge()
    entrance_rules["Route 9 Northwest Ledge"] = JumpDownLedge()
    entrance_rules["Route 9 Northeast Ledge"] = JumpDownLedge()
    entrance_rules["Route 9 Southeast Ledge"] = JumpDownLedge()

    # Route 10
    location_rules["Route 10 - Hidden Item Behind Cuttable Tree"] = CanCut()
    location_rules["Route 10 - PokeManiac Herman Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 10 - PokeManiac Herman Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 10 - Hiker Trent Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 10 - PokeManiac Mark Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 10 - PokeManiac Mark Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 10 Pokemon Center 1F - Oak's Aide Gift (Pokedex Progress)"] = (
        HasNPokemon(world.options.oaks_aide_route_10.value) & Has("Pokedex")
    )

    entrance_rules["Route 10 Surfing Spot (North)"] = CanSurf()
    entrance_rules["Route 10 Surfing Spot (South)"] = (
        CanSurf() & OptionFilter(Route10Waterfall, Route10Waterfall.option_true)
    )
    entrance_rules["Route 10 Landing Spot (South)"] = (
        True_(options=[OptionFilter(Route10Waterfall, Route10Waterfall.option_true)])
    )
    entrance_rules["Route 10 Fishing Battle (South)"] = (
        True_(options=[OptionFilter(Route10Waterfall, Route10Waterfall.option_true)])
    )
    entrance_rules["Route 10 Waterfall (Drop)"] = CanWaterfall()
    entrance_rules["Route 10 Waterfall (Climb)"] = CanWaterfall()
    entrance_rules["Route 10 Surfing Spot (Near Power Plant)"] = CanSurf()
    entrance_rules["Power Plant Front Entrance"] = (
        Has("Machine Part", options=[OptionFilter(ExtraKeyItems, ExtraKeyItems.option_true)], filtered_resolution=True)
    )
    entrance_rules["Route 10 Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Route 10 Ledge (Top)"] = JumpDownLedge()

    # Lavender Town
    location_rules["Lavender Pokemon Center 1F - Balding Man Info"] = PostGameFame()
    location_rules["Volunteer Pokemon House - Mr. Fuji Gift"] = Has("Rescue Mr. Fuji")

    entrance_rules["Lavender Town South Exit"] = (
        True_(options=[OptionFilter(Route12Boulders, Route12Boulders.option_false)]) |
        (CanStrength() & OptionFilter(Route12Boulders, Route12Boulders.option_true))
    )

    # Route 8
    location_rules["Route 8 - Gamer Rich Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 8 - Super Nerd Glenn Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 8 - Twins Eli & Anne Reward"] = HasWildPokemon()
    location_rules["Route 8 - Twins Eli & Anne Rematch Reward (4 Badges/Gyms)"] = (
            HasWildPokemon() & TrainerRematch(4)
    )
    location_rules["Route 8 - Lass Megan Rematch Reward (2 Badges/Gyms)"] = TrainerRematch(2)
    location_rules["Route 8 - Lass Megan Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 8 - Biker Jaren Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)

    entrance_rules["Route 8 Cuttable Trees"] = CanCut()
    entrance_rules["Route 8 Open Path (Bottom)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 8 Open Path (Top)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 8 Smashable Rocks (Bottom)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 8 Smashable Rocks (Top)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 8 Gate Guard Checkpoint (Right)"] = HasAny("Tea", "Purple Tea")
    entrance_rules["Route 8 Gate Guard Checkpoint (Left)"] = HasAny("Tea", "Purple Tea")

    # Route 7
    entrance_rules["Route 7 Open Path (Top Right)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 7 Open Path (Bottom Left)"] = (
        True_(options=[OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_false)])
    )
    entrance_rules["Route 7 Smashable Rocks (Top Right)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 7 Smashable Rocks (Bottom Left)"] = (
        (CanRockSmash() & OptionFilter(BlockUndergroundPaths, BlockUndergroundPaths.option_true))
    )
    entrance_rules["Route 7 Gate Guard Checkpoint (Left)"] = HasAny("Tea", "Green Tea")
    entrance_rules["Route 7 Gate Guard Checkpoint (Right)"] = HasAny("Tea", "Green Tea")

    # Celadon City
    location_rules["Celadon Game Corner - Fisherman Gift"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Scientist Gift"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Gentleman Gift"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Northwest Hidden Item"] = Has("Coin Case")
    location_rules["Celadon Game Corner - North Hidden Item (Left)"] = Has("Coin Case")
    location_rules["Celadon Game Corner - North Hidden Item (Right)"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Northeast Hidden Item"] = Has("Coin Case")
    location_rules["Celadon Game Corner - West Hidden Item"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Center Hidden Item"] = Has("Coin Case")
    location_rules["Celadon Game Corner - East Hidden Item (Left)"] = Has("Coin Case")
    location_rules["Celadon Game Corner - East Hidden Item (Right)"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Southwest Hidden Item"] = Has("Coin Case")
    location_rules["Celadon Game Corner - South Hidden Item (Left)"] = Has("Coin Case")
    location_rules["Celadon Game Corner - South Hidden Item (Right)"] = Has("Coin Case")
    location_rules["Celadon Game Corner - Southeast Hidden Item"] = Has("Coin Case")
    location_rules["Celadon Game Corner Prize Room - Prize Item 1"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Item 2"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Item 3"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Item 4"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Item 5"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize TM 1"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize TM 2"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize TM 3"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize TM 4"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize TM 5"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Pokemon 1"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Pokemon 2"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Pokemon 3"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Pokemon 4"] = CanBuyCoins()
    location_rules["Celadon Game Corner Prize Room - Prize Pokemon 5"] = CanBuyCoins()
    location_rules["Prize Pokemon 1 Scaling"] = CanBuyCoins()
    location_rules["Prize Pokemon 2 Scaling"] = CanBuyCoins()
    location_rules["Prize Pokemon 3 Scaling"] = CanBuyCoins()
    location_rules["Prize Pokemon 4 Scaling"] = CanBuyCoins()
    location_rules["Prize Pokemon 5 Scaling"] = CanBuyCoins()
    location_rules["Celadon Department Store 2F - Woman Info"] = PostGameFame()
    location_rules["Celadon Department Store Roof - Thirsty Girl Gift (Give Fresh Water)"] = Has("Fresh Water")
    location_rules["Celadon Department Store Roof - Thirsty Girl Gift (Give Soda Pop)"] = Has("Soda Pop")
    location_rules["Celadon Department Store Roof - Thirsty Girl Gift (Give Lemonade)"] = Has("Lemonade")
    location_rules["Celadon Condominiums 1F - Brock Gift"] = Has("Defeat Brock")
    location_rules["Celadon Condominiums 1F - Misty Gift"] = Has("Defeat Misty")
    location_rules["Celadon Condominiums 1F - Erika Gift"] = Has("Defeat Erika")
    location_rules["Celadon Condominiums 1F - Tea Woman Info"] = PostGameFame()
    location_rules["Celadon Condominiums 2F - Bookshelf Info"] = Has("Defeat Erika")

    entrance_rules["Celadon City Cuttable Tree (Top)"] = CanCut()
    entrance_rules["Celadon City Cuttable Tree (Bottom)"] = CanCut()
    entrance_rules["Celadon City Surfing Spot"] = CanSurf()
    entrance_rules["Celadon Gym Entrance"] = (
        Has("Celadon Key", options=[OptionFilter(GymKeys, GymKeys.option_true)], filtered_resolution=True)
    )
    entrance_rules["Rocket Hideout Entrance"] = (
        Has("Hideout Key", options=[OptionFilter(ExtraKeyItems, ExtraKeyItems.option_true)], filtered_resolution=True)
    )
    entrance_rules["Celadon Department Store Elevator 1F Stop"] = (
        True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
        Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
        False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Celadon Department Store Elevator 2F Stop"] = (
        True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
        Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
        False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Celadon Department Store Elevator 3F Stop"] = (
        True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
        Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
        False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Celadon Department Store Elevator 4F Stop"] = (
        True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
        Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
        False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Celadon Department Store Elevator 5F Stop"] = (
        True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
        Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
        False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Celadon Gym Cuttable Trees"] = CanCut()

    # Rocket Hideout
    entrance_rules["Rocket Hideout Elevator B1F Stop"] = Has("Lift Key")
    entrance_rules["Rocket Hideout Elevator B2F Stop"] = Has("Lift Key")
    entrance_rules["Rocket Hideout Elevator B4F Stop"] = Has("Lift Key")

    # Pokemon Tower
    location_rules["Static Marowak Scaling"] = Has("Silph Scope")
    location_rules["Pokemon Tower 7F - Hidden Item Under Mr. Fuji"] = Has("Itemfinder")

    pokemon_tower_battles = [
        "Pokemon Tower 3F Land Battle", "Pokemon Tower 4F Land Battle", "Pokemon Tower 5F Land Battle",
        "Pokemon Tower 6F Land Battle", "Pokemon Tower 6F Land Battle", "Pokemon Tower 6F Land Battle (Near Stairs)",
        "Pokemon Tower 7F Land Battle"
    ]
    for battle in pokemon_tower_battles:
        entrance_rules[battle] = Has("Silph Scope")
    entrance_rules["Pokemon Tower 1F Open Path (Left)"] = (
        True_(options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_false)])
    )
    entrance_rules["Pokemon Tower 1F Open Path (Right)"] = (
        True_(options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_false)])
    )
    entrance_rules["Pokemon Tower 1F Reveal Ghost (Left)"] = (
        Has("Silph Scope", options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_true)])
    )
    entrance_rules["Pokemon Tower 1F Reveal Ghost (Right)"] = (
        Has("Silph Scope", options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_true)])
    )
    entrance_rules["Pokemon Tower 6F Open Path (Top)"] = (
        True_(options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_true)])
    )
    entrance_rules["Pokemon Tower 6F Open Path (Bottom)"] = (
        True_(options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_true)])
    )
    entrance_rules["Pokemon Tower 6F Reveal Ghost (Top)"] = (
        Has("Silph Scope", options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_false)])
    )
    entrance_rules["Pokemon Tower 6F Reveal Ghost (Bottom)"] = (
        Has("Silph Scope", options=[OptionFilter(BlockPokemonTower, BlockPokemonTower.option_false)])
    )
    entrance_rules["Follow Mr. Fuji"] = Has("Rescue Mr. Fuji") & NotRandomizingEntrances()

    # Route 12
    location_rules["Route 12 - Fisherman Elliot Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 12 - Young Couple Gia & Jes Reward"] = HasWildPokemon()
    location_rules["Route 12 - Young Couple Gia & Jes Rematch Reward (4 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(4)
    )
    location_rules["Route 12 - Young Couple Gia & Jes Rematch Reward (8 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(8)
    )
    location_rules["Route 12 - Hidden Item Under Snorlax"] = Has("Itemfinder")
    location_rules["Route 12 - Rocker Luca Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 12 Fishing House - Fishing Guru Gift (Show Magikarp)"] = (
        Has("Magikarp") & Has("Pokedex")
    )

    entrance_rules["Route 12 West Exit"] = (
        True_(options=[OptionFilter(Route12Boulders, Route12Boulders.option_false)]) |
        (CanStrength() & OptionFilter(Route12Boulders, Route12Boulders.option_true))
    )
    entrance_rules["Route 12 Play Poke Flute (Left)"] = Has("Poke Flute")
    entrance_rules["Route 12 North Exit"] = (
        True_(options=[OptionFilter(Route12Boulders, Route12Boulders.option_false)]) |
        (CanStrength() & OptionFilter(Route12Boulders, Route12Boulders.option_true))
    )
    entrance_rules["Route 12 Surfing Spot (North)"] = CanSurf()
    entrance_rules["Route 12 Play Poke Flute (Top)"] = Has("Poke Flute")
    entrance_rules["Route 12 Surfing Spot (Center)"] = CanSurf()
    entrance_rules["Route 12 Play Poke Flute (Bottom)"] = Has("Poke Flute")
    entrance_rules["Route 12 Open Path (Top)"] = (
        True_(options=[OptionFilter(Route12Rocks, Route12Rocks.option_false)])
    )
    entrance_rules["Route 12 Open Path (Bottom)"] = (
        True_(options=[OptionFilter(Route12Rocks, Route12Rocks.option_false)])
    )
    entrance_rules["Route 12 Surfing Spot (South)"] = CanSurf()
    entrance_rules["Route 12 North Cuttable Tree"] = CanCut()
    entrance_rules["Route 12 South Cuttable Tree"] = CanCut()
    entrance_rules["Route 12 South Exit"] = (
        True_(options=[OptionFilter(Route12Boulders, Route12Boulders.option_false)]) |
        (CanStrength() & OptionFilter(Route12Boulders, Route12Boulders.option_true))
    )

    # Route 13
    location_rules["Route 13 - Picnicker Susie Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 13 - Picnicker Susie Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 13 - Picnicker Susie Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 13 - Beauty Sheila Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 13 - Bird Keeper Robert Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 13 - Bird Keeper Robert Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Route 13 North Exit"] = (
        True_(options=[OptionFilter(Route12Boulders, Route12Boulders.option_false)]) |
        (CanStrength() & OptionFilter(Route12Boulders, Route12Boulders.option_true))
    )
    entrance_rules["Route 13 Surfing Spot"] = CanSurf()
    entrance_rules["Route 13 Cuttable Tree"] = CanCut()

    # Route 14
    location_rules["Route 14 - Bird Keeper Marlon Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 14 - Bird Keeper Marlon Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 14 - Bird Keeper Benny Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 14 - Bird Keeper Benny Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 14 - Twins Kiri & Jan Reward"] = HasWildPokemon()
    location_rules["Route 14 - Biker Lukas Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Route 14 Ledge"] = JumpUpLedge()
    entrance_rules["Route 14 North Cuttable Tree"] = CanCut()
    entrance_rules["Route 14 South Cuttable Tree"] = CanCut()

    # Route 15
    location_rules["Route 15 - Beauty Grace Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 15 - Bird Keeper Chester Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 15 - Bird Keeper Chester Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 15 - Picnicker Becky Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 15 - Picnicker Becky Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 15 - Picnicker Becky Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 15 - Crush Kin Ron & Mya Reward"] = HasWildPokemon()
    location_rules["Route 15 - Crush Kin Ron & Mya Rematch Reward (4 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(4)
    )
    location_rules["Route 15 - Crush Kin Ron & Mya Rematch Reward (6 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(6)
    )
    location_rules["Route 15 - Crush Kin Ron & Mya Rematch Reward (8 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(8)
    )
    location_rules["Route 15 Gate 2F - Oak's Aide Gift (Pokedex Progress)"] = (
        HasNPokemon(world.options.oaks_aide_route_15.value) & Has("Pokedex")
    )

    entrance_rules["Route 15 Ledge"] = JumpUpLedge()

    # Route 16
    location_rules["Route 16 - Young Couple Lea & Jed Reward"] = HasWildPokemon()
    location_rules["Route 16 - Hidden Item Under Snorlax"] = Has("Itemfinder")
    location_rules["Route 16 - Biker Ruben Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 16 - Cue Ball Camron Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 16 Gate 2F - Oak's Aide Gift (Pokedex Progress)"] = (
        HasNPokemon(world.options.oaks_aide_route_16.value) & Has("Pokedex")
    )

    # Route 16
    entrance_rules["Route 16 Cuttable Tree (Bottom)"] = CanCut()
    entrance_rules["Route 16 Cuttable Tree (Top)"] = CanCut()
    entrance_rules["Route 16 Play Poke Flute (Right)"] = Has("Poke Flute")
    entrance_rules["Route 16 Smashable Rock (Top)"] = (
        CanRockSmash() & OptionFilter(Route16Rock, Route16Rock.option_true)
    )
    entrance_rules["Route 16 Smashable Rock (Bottom)"] = (
            CanRockSmash() & OptionFilter(Route16Rock, Route16Rock.option_true)
    )
    entrance_rules["Route 16 Play Poke Flute (Left)"] = Has("Poke Flute")

    # Route 17
    location_rules["Route 17 - Cue Ball Isaiah Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 17 - Cue Ball Corey Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 17 - Biker Jaxon Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    # Route 18
    location_rules["Route 18 - Bird Keeper Jacob Rematch Reward (4 Badges/Gyms)"] = TrainerRematch(4)
    location_rules["Route 18 - Bird Keeper Jacob Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 18 Gate 2F - Trade Pokemon"] = (
        HasTradePokemon("Route 18 Gate 2F - Trade Pokemon") & Has("Pokedex")
    )

    # Fuchsia City
    location_rules["Fuchsia City - Koga's Daughter Info"] = PostGameFame()
    location_rules["Safari Zone Warden's House - Warden Gift (Return Teeth)"] = Has("Gold Teeth")
    location_rules["Safari Zone Warden's House - Item"] = CanStrength()
    location_rules["Safari Zone Warden's House - Bookshelf Info"] = Has("Defeat Koga")

    entrance_rules["Fuchsia Gym Entrance"] = (
        Has("Fuchsia Key", options=[OptionFilter(GymKeys, GymKeys.option_true)], filtered_resolution=True)
    )
    entrance_rules["Fuchsia City Surfing Spot"] = CanSurf()
    entrance_rules["Safari Zone Entrance"] = (
        Has("Safari Pass", options=[OptionFilter(ExtraKeyItems, ExtraKeyItems.option_true)], filtered_resolution=True)
    )

    # Safari Zone
    entrance_rules["Safari Zone Center Area Surfing Spot (South)"] = CanSurf()
    entrance_rules["Safari Zone Center Area Surfing Spot (Northwest)"] = CanSurf()
    entrance_rules["Safari Zone Center Area Surfing Spot (Northeast)"] = CanSurf()
    entrance_rules["Safari Zone East Area Surfing Spot"] = CanSurf()
    entrance_rules["Safari Zone North Area Surfing Spot"] = CanSurf()
    entrance_rules["Safari Zone West Area Surfing Spot (North)"] = CanSurf()
    entrance_rules["Safari Zone West Area Surfing Spot (South)"] = CanSurf()

    # Saffron City
    location_rules["Saffron City - Battle Girl Info"] = PostGameFame()
    location_rules["Pokemon Trainer Fan Club - Bookshelf Info"] = PostGameFame()
    location_rules["Saffron Pokemon Center 1F - Bookshelf Info"] = Has("Defeat Sabrina")

    # Saffron City
    entrance_rules["Silph Co. Entrance"] = (
        Has(
            "Rescue Mr. Fuji",
            options=[OptionFilter(OpenSilphCo, OpenSilphCo.option_false)],
            filtered_resolution=True
        ) |
        Has(
            "Liberate Silph Co.",
            options=[OptionFilter(RemoveSaffronRockets, RemoveSaffronRockets.option_false)],
            filtered_resolution=True
        )
    )
    entrance_rules["Copycat's House Entrance"] = (
        Has(
            "Liberate Silph Co.",
            options=[OptionFilter(RemoveSaffronRockets, RemoveSaffronRockets.option_false)],
            filtered_resolution=True
        )
    )
    entrance_rules["Saffron Gym Entrance"] = (
        Has(
            "Liberate Silph Co.",
            options=[OptionFilter(RemoveSaffronRockets, RemoveSaffronRockets.option_false)],
            filtered_resolution=True
        ) &
        Has("Saffron Key", options=[(OptionFilter(GymKeys, GymKeys.option_true))], filtered_resolution=True)
    )
    entrance_rules["Saffron Pidgey House Entrance"] = (
        Has(
            "Liberate Silph Co.",
            options=[OptionFilter(RemoveSaffronRockets, RemoveSaffronRockets.option_false)],
            filtered_resolution=True
        )
    )

    # Silph Co.
    entrance_rules["Silph Co. 2F Northwest Barrier (Bottom)"] = HasCardKey(2)
    entrance_rules["Silph Co. 2F Northwest Barrier (Top)"] = HasCardKey(2)
    entrance_rules["Silph Co. 2F Southwest Barrier (Top)"] = HasCardKey(2)
    entrance_rules["Silph Co. 2F Southwest Barrier (Bottom)"] = HasCardKey(2)
    entrance_rules["Silph Co. 3F Center Barrier (Right)"] = HasCardKey(3)
    entrance_rules["Silph Co. 3F Center Barrier (Left)"] = HasCardKey(3)
    entrance_rules["Silph Co. 3F West Barrier (Right)"] = HasCardKey(3)
    entrance_rules["Silph Co. 3F West Barrier (Left)"] = HasCardKey(3)
    entrance_rules["Silph Co. 4F West Barrier (Bottom)"] = HasCardKey(4)
    entrance_rules["Silph Co. 4F Center Barrier (Bottom)"] = HasCardKey(4)
    entrance_rules["Silph Co. 4F Center Barrier (Top)"] = HasCardKey(4)
    entrance_rules["Silph Co. 5F Northwest Barrier (Right)"] = HasCardKey(5)
    entrance_rules["Silph Co. 5F Center Barrier (Right)"] = HasCardKey(5)
    entrance_rules["Silph Co. 5F Southwest Barrier (Right)"] = HasCardKey(5)
    entrance_rules["Silph Co. 5F Southwest Barrier (Left)"] = HasCardKey(5)
    entrance_rules["Silph Co. 6F Barrier (Right)"] = HasCardKey(6)
    entrance_rules["Silph Co. 7F Center Barrier (Top)"] = HasCardKey(7)
    entrance_rules["Silph Co. 7F Northeast Barrier (Top)"] = HasCardKey(7)
    entrance_rules["Silph Co. 7F Northeast Barrier (Bottom)"] = HasCardKey(7)
    entrance_rules["Silph Co. 7F Southeast Barrier (Top)"] = HasCardKey(7)
    entrance_rules["Silph Co. 7F Southeast Barrier (Bottom)"] = HasCardKey(7)
    entrance_rules["Silph Co. 8F Barrier (Right)"] = HasCardKey(8)
    entrance_rules["Silph Co. 8F Barrier (Left)"] = HasCardKey(8)
    entrance_rules["Silph Co. 9F South Barrier (Right)"] = HasCardKey(9)
    entrance_rules["Silph Co. 9F South Barrier (Left)"] = HasCardKey(9)
    entrance_rules["Silph Co. 9F West Barrier (Left)"] = HasCardKey(9)
    entrance_rules["Silph Co. 9F West Barrier (Right)"] = HasCardKey(9)
    entrance_rules["Silph Co. 10F Barrier (Top)"] = HasCardKey(10)
    entrance_rules["Silph Co. 10F Barrier (Bottom)"] = HasCardKey(10)
    entrance_rules["Silph Co. 11F Barrier (Bottom)"] = HasCardKey(11)
    entrance_rules["Silph Co. Elevator 1F Stop"] = (
        True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
        Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
        False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 2F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 3F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 4F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 5F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 6F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 7F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 8F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 9F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 10F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )
    entrance_rules["Silph Co. Elevator 11F Stop"] = (
            True_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_open)]) |
            Has("Lift Key", options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_locked)]) |
            False_(options=[OptionFilter(ElevatorsCondition, ElevatorsCondition.option_disabled)])
    )

    # Route 19
    location_rules["Route 19 - Swimmer Tony Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 19 - Swimmer Matthew Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 19 - Sis and Bro Lia & Luc Reward"] = HasWildPokemon()
    location_rules["Route 19 - Swimmer Alice Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Route 19 Surfing Spot"] = CanSurf()

    # Route 20
    location_rules["Route 20 - Swimmer Darrin Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Route 20 - Swimmer Melissa Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 20 - Picnicker Missy Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 20 - Picnicker Missy Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    entrance_rules["Route 20 Surfing Spot (Near North Cave)"] = CanSurf()
    entrance_rules["Route 20 Surfing Spot (Near South Cave)"] = CanSurf()

    # Seafoam Islands
    entrance_rules["Seafoam Islands B3F South Surfing Spot (West)"] = CanSurf() & CanStopSeafoamB3FCurrent()
    entrance_rules["Seafoam Islands B3F Northwest Surfing Spot"] = CanSurf()
    entrance_rules["Seafoam Islands B3F South Landing Spot (West)"] = CanStopSeafoamB3FCurrent()
    entrance_rules["Seafoam Islands B3F Water Battle (South Water)"] = CanStopSeafoamB3FCurrent()
    entrance_rules["Seafoam Islands B3F Fishing Battle (South Water)"] = CanStopSeafoamB3FCurrent()
    entrance_rules["Seafoam Islands B3F South Landing Spot (East)"] = CanStopSeafoamB3FCurrent()
    entrance_rules["Seafoam Islands B3F South Surfing Spot (East)"] = CanSurf() & CanStopSeafoamB3FCurrent()
    entrance_rules["Seafoam Islands B3F Northeast Surfing Spot"] = CanSurf()
    entrance_rules["Seafoam Islands B3F Northeast Waterfall (Climb)"] = CanWaterfall()
    entrance_rules["Seafoam Islands B4F East Surfing Spot"] = CanSurf()
    entrance_rules["Seafoam Islands B4F West Surfing Spot"] = CanSurf() & CanStopSeafoamB4FCurrent()
    entrance_rules["Seafoam Islands B4F West Landing Spot (Near Articuno)"] = CanStopSeafoamB4FCurrent()
    entrance_rules["Seafoam Islands B4F Water Battle (West Water)"] = CanStopSeafoamB4FCurrent()
    entrance_rules["Seafoam Islands B4F Fishing Battle (West Water)"] = CanStopSeafoamB4FCurrent()
    entrance_rules["Seafoam Islands B4F Fishing Battle (Near Articuno)"] = CanStopSeafoamB4FCurrent()

    # Cinnabar Island
    location_rules["Pokemon Lab Lounge - Trade Pokemon 1"] = (
        HasTradePokemon("Pokemon Lab Lounge - Trade Pokemon 1") & Has("Pokedex")
    )
    location_rules["Pokemon Lab Lounge - Trade Pokemon 2"] = (
        HasTradePokemon("Pokemon Lab Lounge - Trade Pokemon 2") & Has("Pokedex")
    )
    location_rules["Pokemon Lab Experiment Room - Fossil"] = (
        Has("Miguel Takes Fossil") &
        HasFromListUnique("Dome Fossil", "Helix Fossil", "Old Amber", count=world.options.fossil_count.value)
    )
    location_rules["Pokemon Lab Experiment Room - Trade Pokemon"] = (
        HasTradePokemon("Pokemon Lab Experiment Room - Trade Pokemon") & Has("Pokedex")
    )
    location_rules["Pokemon Lab Experiment Room - Revive Helix Fossil"] = Has("Helix Fossil")
    location_rules["Gift Omanyte Scaling"] = Has("Helix Fossil")
    location_rules["Pokemon Lab Experiment Room - Revive Dome Fossil"] = Has("Dome Fossil")
    location_rules["Gift Kabuto Scaling"] = Has("Dome Fossil")
    location_rules["Pokemon Lab Experiment Room - Revive Old Amber"] = Has("Old Amber")
    location_rules["Gift Aerodactyl Scaling"] = Has("Old Amber")
    location_rules["Cinnabar Pokemon Center 1F - Bill Gift"] = Has("Defeat Blaine")
    location_rules["Cinnabar Pokemon Center 1F - Bookshelf Info"] = PostGameFame()

    entrance_rules["Cinnabar Island Surfing Spot"] = CanSurf()
    entrance_rules["Pokemon Mansion Entrance"] = (
        Has("Letter", options=[OptionFilter(ExtraKeyItems, ExtraKeyItems.option_true)], filtered_resolution=True)
    )
    entrance_rules["Cinnabar Gym Entrance"] = (
        Has("Secret Key", options=[OptionFilter(GymKeys, GymKeys.option_false)]) |
        Has("Cinnabar Key", options=[OptionFilter(GymKeys, GymKeys.option_true)])
    )
    entrance_rules["Follow Bill"] = Has("Defeat Blaine") & NotRandomizingEntrances()

    # Pokemon Mansion
    entrance_rules["Pokemon Mansion 1F East Exit"] = NotRandomizingEntrances()
    entrance_rules["Pokemon Mansion 1F South Barrier"] = CanPushMansionSwitch()
    entrance_rules["Pokemon Mansion 1F Southeast Barrier"] = CanPushMansionSwitch()
    entrance_rules["Pokemon Mansion 2F Center Barrier (Top)"] = CanPushMansionSwitch()
    entrance_rules["Pokemon Mansion 2F Center Barrier (Bottom)"] = CanPushMansionSwitch()
    entrance_rules["Pokemon Mansion 3F Barrier (Top)"] = CanPushMansionSwitch()
    entrance_rules["Pokemon Mansion 3F Barrier (Bottom)"] = CanPushMansionSwitch()

    # Route 21
    location_rules["Route 21 - Fisherman Wade Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Route 21 - Sis and Bro Lil & Ian Reward"] = HasWildPokemon()
    location_rules["Route 21 - Sis and Bro Lil & Ian Rematch Reward (6 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(6)
    )
    location_rules["Route 21 - Sis and Bro Lil & Ian Rematch Reward (8 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(8)
    )
    location_rules["Route 21 - Swimmer Jack Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Route 21 Surfing Spot"] = CanSurf()

    # Route 23
    entrance_rules["Route 23 Surfing Spot (South)"] = CanSurf()
    entrance_rules["Route 23 South Open Path (Bottom)"] = (
        True_(options=[OptionFilter(Route23Waterfall, Route23Waterfall.option_false)])
    )
    entrance_rules["Route 23 South Open Path (Top)"] = (
        True_(options=[OptionFilter(Route23Waterfall, Route23Waterfall.option_false)])
    )
    entrance_rules["Route 23 Waterfall (Climb)"] = (
        CanWaterfall() & OptionFilter(Route23Waterfall, Route23Waterfall.option_true)
    )
    entrance_rules["Route 23 Waterfall (Drop)"] = (
            CanWaterfall() & OptionFilter(Route23Waterfall, Route23Waterfall.option_true)
    )
    entrance_rules["Route 23 Surfing Spot (Near Water)"] = CanSurf()
    entrance_rules["Route 23 North Open Path (Bottom)"] = (
        True_(options=[OptionFilter(Route23Trees, Route23Trees.option_false)])
    )
    entrance_rules["Route 23 North Open Path (Top)"] = (
        True_(options=[OptionFilter(Route23Trees, Route23Trees.option_false)])
    )
    entrance_rules["Route 23 Cuttable Trees (Bottom)"] = (
        CanCut() & OptionFilter(Route23Trees, Route23Trees.option_true)
    )
    entrance_rules["Route 23 Cuttable Trees (Top)"] = (
            CanCut() & OptionFilter(Route23Trees, Route23Trees.option_true)
    )
    entrance_rules["Route 23 Guard Checkpoint (Bottom)"] = HasRoute23GuardRequirements()
    entrance_rules["Route 23 Guard Checkpoint (Top)"] = HasRoute23GuardRequirements()

    # Victory Road
    location_rules["Victory Road 1F - North Item (Left)"] = CanStrength()
    location_rules["Victory Road 1F - North Item (Right)"] = CanStrength()
    # location_rules["Victory Road 3F - Cool Couple Ray & Tyra Reward"] = HasWildPokemon()

    entrance_rules["Victory Road 1F Rock Barrier (Left)"] = (
        CanStrength() & (CanRockSmash() | OptionFilter(VictoryRoadRocks, VictoryRoadRocks.option_false))
    )
    entrance_rules["Victory Road 1F Strength Boulder (Top)"] = CanStrength()
    entrance_rules["Victory Road 2F West Rock Barrier (Left)"] = (
        CanStrength() & (CanRockSmash() | OptionFilter(VictoryRoadRocks, VictoryRoadRocks.option_false))
    )
    entrance_rules["Victory Road 2F Southeast Rock Barrier (Left)"] = (
        CanStrength() & CanReachRegion("Victory Road 3F (Southwest)")
    )
    entrance_rules["Victory Road 2F Northwest Strength Boulder (Top)"] = CanStrength()
    entrance_rules["Victory Road 3F Rock Barrier (Right)"] = (
        CanStrength() & (CanRockSmash() | OptionFilter(VictoryRoadRocks, VictoryRoadRocks.option_false))
    )
    entrance_rules["Victory Road 3F West Strength Boulder (Bottom)"] = CanStrength()
    entrance_rules["Victory Road 3F East Strength Boulder (Right)"] = CanStrength()

    # Indigo Plateau
    location_rules["Lorelei's Room - Elite Four Lorelei Rematch Reward"] = HasE4RematchRequirements()
    location_rules["Bruno's Room - Elite Four Bruno Rematch Reward"] = HasE4RematchRequirements()
    location_rules["Agatha's Room - Elite Four Agatha Rematch Reward"] = HasE4RematchRequirements()
    location_rules["Lance's Room - Elite Four Lance Rematch Reward"] = HasE4RematchRequirements()
    location_rules["Champion's Room - Champion Rematch Battle"] = HasE4RematchRequirements()
    location_rules["Champion's Room - Champion Rematch Reward"] = HasE4RematchRequirements()
    location_rules["Elite Four Rematch Scaling"] = HasE4RematchRequirements()
    location_rules["Champion Rematch Scaling"] = HasE4RematchRequirements()
    location_rules["Indigo Plateau Pokemon Center 1F - Black Belt Info 1"] = PostGameFame()
    location_rules["Indigo Plateau Pokemon Center 1F - Black Belt Info 2"] = PostGameFame()
    location_rules["Indigo Plateau Pokemon Center 1F - Cooltrainer Info"] = PostGameFame()
    location_rules["Indigo Plateau Pokemon Center 1F - Bookshelf Info"] = PostGameFame()

    entrance_rules["Pokemon League Entrance"] = HasE4Requirements()

    # One Island Town
    location_rules["One Island Pokemon Center 1F - Celio Gift (Deliver Ruby)"] = HasAll("Deliver Meteorite", "Ruby")
    location_rules["One Island Pokemon Center 1F - Help Celio"] = (
        HasAll("Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire")
    )
    location_rules["One Island Pokemon Center 1F - Celio Gift (Deliver Sapphire)"] = (
        HasAll("Deliver Meteorite", "Ruby", "Free Captured Pokemon", "Sapphire")
    )
    location_rules["One Island Pokemon Center 1F - Celio Info 1"] = Has("Restore Pokemon Network Machine")
    location_rules["One Island Pokemon Center 1F - Celio Info 2"] = Has("Restore Pokemon Network Machine")
    location_rules["One Island Pokemon Center 1F - Celio Info 3"] = Has("Restore Pokemon Network Machine")

    entrance_rules["One Island Town Surfing Spot"] = CanSurf()

    # Kindle Road
    location_rules["Kindle Road - Plateau Item"] = CanRockSmash()
    location_rules["Kindle Road - Item Behind Smashable Rock"] = CanRockSmash()
    location_rules["Kindle Road - Crush Girl Tanya Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Kindle Road - Crush Girl Tanya Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Kindle Road - Crush Kin Mik & Kia Reward"] = HasWildPokemon()
    location_rules["Kindle Road - Crush Kin Mik & Kia Rematch Reward (6 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(6)
    )
    location_rules["Kindle Road - Crush Kin Mik & Kia Rematch Reward (8 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(8)
    )
    location_rules["Kindle Road - Black Belt Hugh Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Kindle Road - Black Belt Hugh Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Kindle Road - Black Belt Shea Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Kindle Road - Black Belt Shea Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Kindle Road - Crush Girl Sharon Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)
    location_rules["Kindle Road - Crush Girl Sharon Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Kindle Road - Swimmer Finn Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Kindle Road South Surfing Spot (South)"] = CanSurf()
    entrance_rules["Kindle Road South Surfing Spot (Center)"] = CanSurf()
    entrance_rules["Kindle Road North Surfing Spot (Center)"] = CanSurf()
    entrance_rules["Kindle Road North Surfing Spot (North)"] = CanSurf()

    # Ember Spa
    location_rules["Ember Spa - Black Belt Info"] = PostGameFame()

    # Mt. Ember
    location_rules["Mt. Ember Exterior - Eavesdrop on Team Rocket Grunts"] = Has("Deliver Meteorite")
    location_rules["Mt. Ember Exterior - Team Rocket Grunt Reward (Left)"] = Has("Deliver Meteorite")
    location_rules["Mt. Ember Exterior - Team Rocket Grunt Reward (Right)"] = Has("Deliver Meteorite")
    location_rules["Team Rocket Grunt 43 Scaling"] = Has("Deliver Meteorite")
    location_rules["Team Rocket Grunt 44 Scaling"] = Has("Deliver Meteorite")
    location_rules["Mt. Ember Exterior - Item Near Summit"] = CanStrength() & (CanRockSmash() | JumpUpLedge())
    location_rules["Mt. Ember Summit - Legendary Pokemon"] = CanStrength()
    location_rules["Legendary Moltres Scaling"] = CanStrength()

    entrance_rules["Mt. Ember Exterior South Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Mt. Ember Exterior South Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Mt. Ember Exterior Strength Boulders (Right)"] = CanStrength()
    entrance_rules["Mt. Ember Exterior Strength Boulders (Left)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path Entrance"] = Has("Deliver Meteorite")
    entrance_rules["Mt. Ember Exterior Center Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Mt. Ember Exterior Center Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Mt. Ember Ruby Path 1F Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Mt. Ember Ruby Path 1F Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Mt. Ember Ruby Path B2F Strength Boulders (Left)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B2F Strength Boulders (Right)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B3F Northwest Strength Boulder (Left)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B3F Northwest Strength Boulder (Right)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B3F Southwest Strength Boulder (Right)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B3F Southwest Strength Boulder (Left)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B3F Southeast Strength Boulder (Top)"] = CanStrength()
    entrance_rules["Mt. Ember Ruby Path B3F Southeast Strength Boulder (Bottom)"] = CanStrength()

    # Two Island Town
    location_rules["Two Island Town - Item Behind Cuttable Tree"] = CanCut()
    location_rules["Two Island Town - Market Stall Item 2"] = TwoIslandStallExpansion(1)
    location_rules["Two Island Town - Market Stall Item 3"] = TwoIslandStallExpansion(3)
    location_rules["Two Island Town - Market Stall Item 4"] = TwoIslandStallExpansion(3)
    location_rules["Two Island Town - Market Stall Item 5"] = TwoIslandStallExpansion(2)
    location_rules["Two Island Town - Market Stall Item 6"] = TwoIslandStallExpansion(1)
    location_rules["Two Island Town - Market Stall Item 8"] = TwoIslandStallExpansion(2)
    location_rules["Two Island Town - Market Stall Item 9"] = TwoIslandStallExpansion(3)
    location_rules["Two Island Town - Beauty Info"] = TwoIslandStallExpansion(2)
    location_rules["Two Island Game Corner - Lostelle's Dad Gift (Deliver Meteorite)"] = (
        HasAll("Rescue Lostelle", "Meteorite")
    )
    location_rules["Two Island Game Corner - Lostelle's Dad's Delivery"] = HasAll("Rescue Lostelle", "Meteorite")

    # Cape Brink
    location_rules["Cape Brink - Hidden Item Across Pond"] = Has("Itemfinder")

    entrance_rules["Cape Brink Surfing Spot"] = CanSurf()

    # Three Island Town
    location_rules["Three Island Town - Item Behind East Fence"] = CanCut()
    location_rules["Three Island Town - Hidden Item Behind West Fence"] = CanCut()
    location_rules["Lostelle's House - Lostelle Gift"] = Has("Deliver Meteorite")

    # Bond Bridge
    location_rules["Bond Bridge - Twins Joy & Meg Reward"] = HasWildPokemon()
    location_rules["Bond Bridge - Twins Joy & Meg Rematch Reward (6 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(6)
    )
    location_rules["Bond Bridge - Tuber Amira Rematch Reward (6 Badges/Gyms)"] = TrainerRematch(6)

    entrance_rules["Bond Bridge Surfing Spot"] = CanSurf()

    # Berry Forest
    location_rules["Berry Forest - Item Near North Pond"] = JumpDownLedge()
    location_rules["Berry Forest - Item Past Southwest Pond"] = CanCut()

    entrance_rules["Berry Forest Surfing Spot"] = CanSurf()
    entrance_rules["Follow Lostelle"] = Has("Rescue Lostelle") & NotRandomizingEntrances()

    # Four Island Town
    location_rules["Four Island Town - Beach Item"] = CanRockSmash()
    location_rules["Four Island Town - Old Woman Info"] = Has("Restore Pokemon Network Machine")

    entrance_rules["Four Island Town Surfing Spot"] = CanSurf()
    entrance_rules["Four Island Town Surfing Spot (Near Cave)"] = CanSurf()

    # Icefall Cave
    entrance_rules["Icefall Cave Front Surfing Spot (South)"] = CanSurf()
    entrance_rules["Icefall Cave Front Waterfall (Climb)"] = CanWaterfall()
    entrance_rules["Icefall Cave Front Waterfall (Drop)"] = CanWaterfall()
    entrance_rules["Icefall Cave Front Surfing Spot (Center)"] = CanSurf()
    entrance_rules["Icefall Cave Front Surfing Spot (North)"] = CanSurf()
    entrance_rules["Icefall Cave 1F East Ledge (Left)"] = JumpUpLedge()
    entrance_rules["Icefall Cave 1F East Ledge (Right)"] = JumpDownLedge()
    entrance_rules["Icefall Cave 1F Southeast Ledge (Left)"] = JumpUpLedge()
    entrance_rules["Icefall Cave 1F Southeast Ledge (Right)"] = JumpDownLedge()
    entrance_rules["Icefall Cave 1F West Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Icefall Cave 1F West Ledge (Top)"] = JumpDownLedge()
    entrance_rules["Icefall Cave Back Surfing Spot"] = CanSurf()

    # Five Island Town
    location_rules["Five Island Pokemon Center 1F - Bookshelf Info"] = PostGameFame()

    entrance_rules["Five Island Town Surfing Spot"] = CanSurf()

    # Five Isle Meadow
    location_rules["Five Isle Meadow - Item Behind Cuttable Tree"] = CanCut()

    entrance_rules["Five Isle Meadow Surfing Spot"] = CanSurf()
    entrance_rules["Rocket Warehouse Entrance"] = HasAll("Learn Goldeen Need Log", "Learn Yes Nah Chansey")

    # Rocket Warehouse
    location_rules["Rocket Warehouse - Scientist Gideon Info"] = Has("Restore Pokemon Network Machine")

    # Memorial Pillar
    location_rules["Memorial Pillar - Bird Keeper Milo Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Memorial Pillar - Bird Keeper Chaz Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Memorial Pillar - Bird Keeper Harold Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Memorial Pillar - Memorial Man Gift"] = Has("Lemonade")

    # Water Labyrinth
    location_rules["Water Labyrinth - Gentleman Info"] = (
        (Has("Togepi") | Has("Togetic")) & Has("Pokedex")
    )
    location_rules["Water Labyrinth - Pokemon Breeder Alize Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    # Resort Gorgeous
    location_rules["Resort Gorgeous - Painter Rayna Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Resort Gorgeous - Youngster Destin Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Selphy's House - Selphy Gift (Show Pokemon)"] = (
        CanShowSelphyPokemon() & Has("Pokedex")
    )

    entrance_rules["Resort Gorgeous Surfing Spot (Near Resort)"] = CanSurf()
    entrance_rules["Resort Gorgeous Surfing Spot (Near Cave)"] = CanSurf()

    # Lost Cave
    entrance_rules["Follow Selphy"] = Has("Rescue Selphy") & NotRandomizingEntrances()

    # Water Path
    location_rules["Water Path - Hiker Earl Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Water Path - Swimmer Samir Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Water Path - Twins Miu & Mia Reward"] = HasWildPokemon()
    location_rules["Water Path Heracross Woman's House - Woman Gift (Show Heracross)"] = (
        Has("Heracross") & Has("Pokedex")
    )

    entrance_rules["Water Path South Surfing Spot (South)"] = CanSurf()
    entrance_rules["Water Path South Surfing Spot (North)"] = CanSurf()
    entrance_rules["Water Path North Surfing Spot"] = CanSurf()

    # Ruin Valley
    location_rules["Ruin Valley - Plateau Item"] = CanStrength()
    location_rules["Ruin Valley - Southwest Item"] = CanStrength()
    location_rules["Ruin Valley - Southeast Item"] = CanStrength()
    location_rules["Ruin Valley - PokeManiac Hector Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Ruin Valley - Ruin Maniac Larry Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    entrance_rules["Ruin Valley Surfing Spot"] = CanSurf()
    entrance_rules["Dotted Hole Entrance"] = Has("Help Lorelei") & CanCut()

    # Dotted Hole
    location_rules["Dotted Hole 1F - Dropped Item"] = Has("Learn Yes Nah Chansey")

    entrance_rules["Dotted Hole 1F Ledge (Bottom)"] = JumpUpLedge()
    entrance_rules["Dotted Hole 1F Ledge (Top)"] = JumpDownLedge()

    # Green Path
    location_rules["Green Path - Psychic Jaclyn Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    entrance_rules["Green Path Surfing Spot"] = CanSurf()

    # Outcast Island
    location_rules["Outcast Island - Swimmer Nicole Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Outcast Island - Sis and Bro Ava & Geb Reward"] = HasWildPokemon()

    entrance_rules["Outcast Island Surfing Spot"] = CanSurf()

    # Seven Island Town
    location_rules["Seven Island Town - Scientist Gift 1 (Trade Scanner)"] = Has("Scanner")
    location_rules["Seven Island Town - Scientist Gift 2 (Trade Scanner)"] = Has("Scanner")
    location_rules["Seven Island Pokemon Center 1F - Bookshelf Info"] = PostGameFame()

    # Canyon Entrance
    location_rules["Canyon Entrance - Juggler Mason Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Canyon Entrance - Pokemon Ranger Nicolas Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Canyon Entrance - Pokemon Ranger Madeline Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Canyon Entrance - Young Couple Eve & Jon Reward"] = HasWildPokemon()

    # Sevault Canyon
    location_rules["Sevault Canyon - Cool Couple Lex & Nya Reward"] = HasWildPokemon()
    location_rules["Sevault Canyon - Cool Couple Lex & Nya Rematch Reward (8 Badges/Gyms)"] = (
        HasWildPokemon() & TrainerRematch(8)
    )
    location_rules["Sevault Canyon - Tamer Evan Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Sevault Canyon - Pokemon Ranger Jackson Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Sevault Canyon - Pokemon Ranger Katelyn Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Sevault Canyon - Crush Girl Cyndy Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Sevault Canyon - Item Behind Smashable Rocks"] = CanStrength() & CanRockSmash()
    location_rules["Sevault Canyon - Cooltrainer Leroy Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Sevault Canyon - Cooltrainer Michelle Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    # Tanoby Key
    location_rules["Tanoby Key - Solve Puzzle"] = CanStrength()

    # Tanoby Ruins
    location_rules["Tanoby Ruins - Island Item"] = Has("Unlock Ruins")

    entrance_rules["Tanoby Ruins Surfing Spot"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Monean Island)"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Liptoo Island)"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Weepth Island)"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Dilford Island)"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Scufib Island)"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Rixy Island)"] = CanSurf()
    entrance_rules["Tanoby Ruins Surfing Spot (Viapois Island)"] = CanSurf()

    # Monean Chamber
    entrance_rules["Monean Chamber Land Battle"] = Has("Unlock Ruins")

    # Liptoo Chamber
    entrance_rules["Liptoo Chamber Land Battle"] = Has("Unlock Ruins")

    # Weepth Chamber
    entrance_rules["Weepth Chamber Land Battle"] = Has("Unlock Ruins")

    # Dilford Chamber
    entrance_rules["Dilford Chamber Land Battle"] = Has("Unlock Ruins")

    # Scufib Chamber
    entrance_rules["Scufib Chamber Land Battle"] = Has("Unlock Ruins")

    # Rixy Chamber
    entrance_rules["Rixy Chamber Land Battle"] = Has("Unlock Ruins")

    # Viapois Chamber
    entrance_rules["Viapois Chamber Land Battle"] = Has("Unlock Ruins")

    # Trainer Tower Exterior
    location_rules["Trainer Tower Exterior - Psychic Rodette Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)
    location_rules["Trainer Tower Exterior - Psychic Dario Rematch Reward (8 Badges/Gyms)"] = TrainerRematch(8)

    entrance_rules["Trainer Tower Exterior Surfing Spot (South)"] = CanSurf()
    entrance_rules["Trainer Tower Exterior Surfing Spot (North)"] = CanSurf()

    # Cerulean Cave
    location_rules["Cerulean Cave 2F - East Item"] = CanRockSmash()
    location_rules["Cerulean Cave 2F - West Item"] = CanRockSmash()
    location_rules["Cerulean Cave 2F - Center Item"] = CanRockSmash()

    entrance_rules["Cerulean Cave 1F Surfing Spot (Southeast)"] = CanSurf()
    entrance_rules["Cerulean Cave 1F Surfing Spot (Northeast)"] = CanSurf()
    entrance_rules["Cerulean Cave 1F Surfing Spot (Center)"] = CanSurf()
    entrance_rules["Cerulean Cave B1F Surfing Spot"] = CanSurf()

    # Navel Rock
    location_rules["Navel Rock Summit - Hidden Item Near Ho-Oh"] = Has("Itemfinder")

    entrance_rules["Board Seagallop (Navel Rock)"] = (
        Has(
            "S.S. Ticket",
            options=[OptionFilter(BlockVermilionSailing, BlockVermilionSailing.option_true)],
            filtered_resolution=True
        )
    )

    # Birth Island
    entrance_rules["Board Seagallop (Birth Island)"] = (
        Has(
            "S.S. Ticket",
            options=[OptionFilter(BlockVermilionSailing, BlockVermilionSailing.option_true)],
            filtered_resolution=True
        )
    )

    # Add rules that are the same for specific location categories
    hidden_rule = (
        True_(options=[OptionFilter(ItemfinderRequired, ItemfinderRequired.option_off)]) |
        Has(
            "Itemfinder",
            options=[OptionFilter(ItemfinderRequired, ItemfinderRequired.option_logic)],
            filtered_resolution=False
        ) |
        Has(
            "Itemfinder",
            options=[OptionFilter(ItemfinderRequired, ItemfinderRequired.option_required)],
            filtered_resolution=False
        )
    )
    fame_rule = Has(
        "Fame Checker",
        options=[OptionFilter(FameCheckerRequired, FameCheckerRequired.option_true)],
        filtered_resolution=True
    )
    if world.is_universal_tracker:
        hidden_rule |= Has(
            PokemonFRLGGlitchedToken.TOKEN_NAME,
            options=[OptionFilter(ItemfinderRequired, ItemfinderRequired.option_logic)],
            filtered_resolution=False
        )

    for location in world.get_locations():
        assert isinstance(location, PokemonFRLGLocation)
        if location.category == LocationCategory.HIDDEN_ITEM:
            location_rules[location.name] &= hidden_rule
        if location.category == LocationCategory.FAME_ENTRY:
            location_rules[location.name] &= fame_rule
        if location.category == LocationCategory.POKEDEX:
            pokemon = location.name.split(" - ")[1].strip()
            location_rules[location.name] &= HasPokemon(pokemon) & Has("Pokedex")
        if location.category == LocationCategory.EVENT_EVOLUTION_POKEMON:
            location_rules[location.name] &= _get_evolution_rule(world, location)

    # Add dark cave logic
    dark_cave_regions = []
    dark_cave_regions.extend(["Rock Tunnel 1F (Northeast)", "Rock Tunnel 1F (Northwest)", "Rock Tunnel 1F (South)",
                              "Rock Tunnel B1F (Southeast)", "Rock Tunnel B1F (Northwest)",
                              "Rock Tunnel 1F (Land Encounters)",
                              "Rock Tunnel B1F (Land Encounters)"])
    if "Mt. Moon" in world.options.additional_dark_caves.value:
        dark_cave_regions.extend(["Mt. Moon 1F", "Mt. Moon B1F (First Tunnel)", "Mt. Moon B1F (Second Tunnel)",
                                  "Mt. Moon B1F (Third Tunnel)", "Mt. Moon B1F (Fourth Tunnel)",
                                  "Mt. Moon B2F (South)", "Mt. Moon B2F (Northeast)", "Mt. Moon B2F",
                                  "Mt. Moon 1F (Land Encounters)", "Mt. Moon B1F (Land Encounters)",
                                  "Mt. Moon B2F (Land Encounters)"])
    if "Diglett's Cave" in world.options.additional_dark_caves.value:
        dark_cave_regions.extend(["Diglett's Cave B1F", "Diglett's Cave B1F (Land Encounters)"])
    if "Victory Road" in world.options.additional_dark_caves.value:
        dark_cave_regions.extend(["Victory Road 1F (South)", "Victory Road 1F (North)",
                                  "Victory Road 2F (Southwest)", "Victory Road 2F (Center)",
                                  "Victory Road 2F (Northwest)", "Victory Road 2F (Southeast)",
                                  "Victory Road 2F (East)", "Victory Road 3F (North)",
                                  "Victory Road 3F (Southwest)", "Victory Road 3F (Southeast)",
                                  "Victory Road 1F (Land Encounters)", "Victory Road 2F (Land Encounters)",
                                  "Victory Road 3F (Land Encounters)"])
    dark_cave_rule = (
        True_(options=[OptionFilter(FlashRequired, FlashRequired.option_off)]) |
        (
                CanFlash() & OptionFilter(FlashRequired, FlashRequired.option_logic)
        ) |
        (
                CanFlash() & OptionFilter(FlashRequired, FlashRequired.option_required)
        )
    )
    if world.is_universal_tracker:
        dark_cave_rule |= Has(
            PokemonFRLGGlitchedToken.TOKEN_NAME,
            options=[OptionFilter(FlashRequired, FlashRequired.option_logic)],
            filtered_resolution=False
        )

    for region in dark_cave_regions:
        for exit in world.get_region(region).exits:
            entrance_rules[exit.name] &= dark_cave_rule
        for location in world.get_region(region).locations:
            location_rules[location.name] &= dark_cave_rule

    # Add bicycle logic
    cycling_road_regions = ["Route 16 (Southwest)", "Route 17", "Route 18 (West)"]

    for region in cycling_road_regions:
        for exit in world.get_region(region).exits:
            entrance_rules[exit.name] &= Has("Bicycle")
        for location in world.get_region(region).locations:
            location_rules[location.name] &= Has("Bicycle")

    for name, rule in entrance_rules.items():
        try:
            entrance = world.get_entrance(name)
            world.set_rule(entrance, rule)
        except KeyError:
            continue

    for name, rule in location_rules.items():
        try:
            location = world.get_location(name)
            world.set_rule(location, rule)
        except KeyError:
            continue


def set_hm_compatible_pokemon(world: "PokemonFRLGWorld") -> None:
    logic = world.logic
    hms = frozenset({"Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"})
    for hm in hms:
        for species in world.modified_species.values():
            combatibility_array = int_to_bool_array(species.tm_hm_compatibility)
            if combatibility_array[HM_TO_COMPATIBILITY_ID[hm]] == 1:
                logic.compatible_hm_pokemon[hm].append(species.name)
    logic.update_hm_compatible_pokemon()


def verify_hm_accessibility(world: "PokemonFRLGWorld") -> None:
    if world.is_universal_tracker:
        return

    logic = world.logic
    hm_rules: Dict[str, CollectionRule] = {
        "Cut": CanCut().resolve(world),
        "Fly": CanFly().resolve(world),
        "Surf": CanSurf().resolve(world),
        "Strength": CanStrength().resolve(world),
        "Flash": CanFlash().resolve(world),
        "Rock Smash": CanRockSmash().resolve(world),
        "Waterfall": CanWaterfall().resolve(world)
    }
    badge_rules: Dict[str, CollectionRule] = {
        "Cut": HasBadgeRequirement("Cut").resolve(world),
        "Fly": HasBadgeRequirement("Fly").resolve(world),
        "Surf": HasBadgeRequirement("Surf").resolve(world),
        "Strength": HasBadgeRequirement("Strength").resolve(world),
        "Flash": HasBadgeRequirement("Flash").resolve(world),
        "Rock Smash": HasBadgeRequirement("Rock Smash").resolve(world),
        "Waterfall": HasBadgeRequirement("Waterfall").resolve(world),
    }

    def can_use_hm(state: CollectionState, hm: str) -> bool:
        rule = hm_rules[hm]
        return rule(state) if rule is not None else False

    def has_badge_requirement(state: CollectionState, hm: str) -> bool:
        rule = badge_rules[hm]
        return rule(state) if rule is not None else False

    hms: List[str] = ["Cut", "Fly", "Surf", "Strength", "Flash", "Rock Smash", "Waterfall"]
    world.random.shuffle(hms)
    last_hm_verified = None
    while len(hms) > 0:
        hm_to_verify = hms[0]
        state = world.get_world_collection_state()
        if not can_use_hm(state, hm_to_verify) and has_badge_requirement(state, hm_to_verify):
            if hm_to_verify == last_hm_verified:
                raise Exception(f"Failed to ensure access to {hm_to_verify} for player {world.player}")
            last_hm_verified = hm_to_verify
            valid_pokemon = [mon for mon in logic.wild_pokemon if state.has(mon, world.player)
                             and mon not in logic.compatible_hm_pokemon[hm_to_verify]]
            pokemon = world.random.choice(valid_pokemon)
            add_hm_compatability(world, pokemon, hm_to_verify)
            logic.add_hm_compatible_pokemon(hm_to_verify, pokemon)
        else:
            hms.pop(0)
    logic.update_hm_compatible_pokemon()

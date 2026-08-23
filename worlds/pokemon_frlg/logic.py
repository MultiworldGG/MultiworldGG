import dataclasses
from typing import Dict, List, TYPE_CHECKING
from typing_extensions import override

from BaseClasses import CollectionState
from rule_builder.rules import (CanReachRegion, False_, Has, HasAll, HasAny, HasFromListUnique, HasGroupUnique,
                                OptionFilter, Rule, True_)

from .data import data
from .options import (CeruleanCaveRequirement, EarlyGossipers, EliteFourRequirement, EliteFourRematchRequirement,
                      PewterCityRoadblock, RematchRequirements, Route22GateRequirement, Route23GuardRequirement,
                      ViridianGymRequirement, ViridianCityRoadblock)

if TYPE_CHECKING:
    from . import PokemonFRLGWorld

GAME = data.get_game()
GYMS: List[str] = [
    "Defeat Brock", "Defeat Misty", "Defeat Lt. Surge", "Defeat Erika", "Defeat Koga", "Defeat Sabrina",
    "Defeat Blaine", "Defeat Giovanni"]
BADGE_REQUIREMENTS: Dict[str, str] = {
    "Cut": "Cascade Badge",
    "Fly": "Thunder Badge",
    "Surf": "Soul Badge",
    "Strength": "Rainbow Badge",
    "Flash": "Boulder Badge",
    "Rock Smash": "Marsh Badge",
    "Waterfall": "Volcano Badge"
}


@dataclasses.dataclass
class NotRandomizingEntrances(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return self.Resolved(
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            world = state.multiworld.worlds[self.player]
            return not world.logic.randomizing_entrances


@dataclasses.dataclass
class HasNBadges(Rule["PokemonFRLGWorld"], game=GAME):
    count: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return HasGroupUnique("Badges", self.count).resolve(world)


@dataclasses.dataclass
class HasNGyms(Rule["PokemonFRLGWorld"], game=GAME):
    count: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return HasFromListUnique(*GYMS, count=self.count).resolve(world)


@dataclasses.dataclass
class HasPokemon(Rule["PokemonFRLGWorld"], game=GAME):
    pokemon: str

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return self.Resolved(
            self.pokemon,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(Rule.Resolved):
        pokemon: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            world = state.multiworld.worlds[self.player]
            return state.has_any(world.logic.dexsanity_state_item_names_lookup[self.pokemon], self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                self.pokemon: {id(self)},
                f"Static {self.pokemon}": {id(self)},
                f"Evolved {self.pokemon}": {id(self)}
            }


@dataclasses.dataclass
class HasWildPokemon(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return self.Resolved(
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(Rule.Resolved):
        @override
        def _evaluate(self, state: CollectionState) -> bool:
            world = state.multiworld.worlds[self.player]
            return state.has_any(world.logic.wild_pokemon, self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            dependencies: dict[str, set[int]] = {}
            for species in data.species.values():
                dependencies[species.name] = {id(self)}
            return dependencies


@dataclasses.dataclass
class HasPokemonForEvolution(Rule["PokemonFRLGWorld"], game=GAME):
    pokemon: str

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return self.Resolved(
            self.pokemon,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(Rule.Resolved):
        pokemon: str

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            world = state.multiworld.worlds[self.player]
            return state.has_any(world.logic.evolution_state_item_names_lookup[self.pokemon], self.player)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {
                self.pokemon: {id(self)},
                f"Evolved {self.pokemon}": {id(self)}
            }


@dataclasses.dataclass
class HasNPokemon(Rule["PokemonFRLGWorld"], game=GAME):
    count: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return self.Resolved(
            self.count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False)
        )

    class Resolved(Rule.Resolved):
        count: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            world = state.multiworld.worlds[self.player]
            count = self.count
            if count <= 0:
                return True
            for species_item_names in world.logic.oaks_aides_species_item_names:
                # There are multiple item names for a species that can provide Pokédex progress for that species.
                if state.has_any(species_item_names, self.player):
                    # Subtraction is used to make use of a common programming performance 'trick' where, comparing two
                    # variables, e.g. `if count == n`, can be replaced with comparing a variable and a constant, e.g.
                    # `if n == 0`.
                    count -= 1
                    # Further minor optimization of `if n == 0` -> `if not n`
                    if not count:
                        return True
            return False

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            dependencies: dict[str, set[int]] = {}
            for species in data.species.values():
                dependencies[species.name] = {id(self)}
            return dependencies


@dataclasses.dataclass
class HasTradePokemon(Rule["PokemonFRLGWorld"], game=GAME):
    trade: str

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return Has(world.logic.required_trade_pokemon[self.trade]).resolve(world)


@dataclasses.dataclass
class CanShowSelphyPokemon(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return HasAll("Rescue Selphy", data.species[world.logic.resort_gorgeous_pokemon].name).resolve(world)


@dataclasses.dataclass
class HasBadgeRequirement(Rule["PokemonFRLGWorld"], game=GAME):
    hm: str

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if self.hm in world.options.remove_badge_requirement.value:
            return True_().resolve(world)
        return Has(BADGE_REQUIREMENTS[self.hm]).resolve(world)


@dataclasses.dataclass
class CanCut(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM01 Cut", "TM Case", "Teach Cut")
        return (rule & HasBadgeRequirement("Cut")).resolve(world)


@dataclasses.dataclass
class CanFly(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM02 Fly", "TM Case", "Teach Fly")
        return (rule & HasBadgeRequirement("Fly")).resolve(world)


@dataclasses.dataclass
class CanSurf(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM03 Surf", "TM Case", "Teach Surf")
        return (rule & HasBadgeRequirement("Surf")).resolve(world)


@dataclasses.dataclass
class CanStrength(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM04 Strength", "TM Case", "Teach Strength")
        return (rule & HasBadgeRequirement("Strength")).resolve(world)


@dataclasses.dataclass
class CanFlash(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM05 Flash", "TM Case", "Teach Flash")
        return (rule & HasBadgeRequirement("Flash")).resolve(world)


@dataclasses.dataclass
class CanRockSmash(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM06 Rock Smash", "TM Case", "Teach Rock Smash")
        return (rule & HasBadgeRequirement("Rock Smash")).resolve(world)


@dataclasses.dataclass
class CanWaterfall(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = HasAll("HM07 Waterfall", "TM Case", "Teach Waterfall")
        return (rule & HasBadgeRequirement("Waterfall")).resolve(world)


@dataclasses.dataclass
class JumpDownLedge(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.bicycle_requires_jumping_shoes:
            return Has("Jumping Shoes").resolve(world)
        return HasAny("Jumping Shoes", "Bicycle").resolve(world)


@dataclasses.dataclass
class JumpUpLedge(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.acrobatic_bicycle:
            if world.options.bicycle_requires_jumping_shoes:
                return HasAll("Jumping Shoes", "Bicycle").resolve(world)
            return Has("Bicycle").resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class HasOldRod(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (Has("Old Rod") | Has("Progressive Rod", 1)).resolve(world)


@dataclasses.dataclass
class HasGoodRod(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (Has("Good Rod") | Has("Progressive Rod", 2)).resolve(world)


@dataclasses.dataclass
class HasSuperRod(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (Has("Super Rod") | Has("Progressive Rod", 3)).resolve(world)


@dataclasses.dataclass
class HasCardKey(Rule["PokemonFRLGWorld"], game=GAME):
    floor: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (
                Has(world.logic.card_keys[self.floor]) |
                Has("Progressive Card Key", self.floor - 1)
        ).resolve(world)


@dataclasses.dataclass
class HasIslandPass(Rule["PokemonFRLGWorld"], game=GAME):
    island: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (
                Has(world.logic.island_passes[self.island][0]) |
                Has("Progressive Pass", world.logic.island_passes[self.island][1])
        ).resolve(world)


@dataclasses.dataclass
class PostGameFame(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return Has(
            "Defeat Champion",
            options=[OptionFilter(EarlyGossipers, EarlyGossipers.option_false)],
            filtered_resolution=True
        ).resolve(world)


@dataclasses.dataclass
class TrainerRematch(Rule["PokemonFRLGWorld"], game=GAME):
    count: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = False_()
        if world.options.rematch_requirements.value == RematchRequirements.option_badges:
            rule = HasNBadges(self.count)
        elif world.options.rematch_requirements.value == RematchRequirements.option_gyms:
            rule = HasNGyms(self.count)
        return (rule & Has("Vs. Seeker")).resolve(world)


@dataclasses.dataclass
class CanLeaveViridian(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.viridian_city_roadblock.value == ViridianCityRoadblock.option_open:
            return True_().resolve(world)
        return Has("Deliver Oak's Parcel").resolve(world)


@dataclasses.dataclass
class HasViridianGymRequirements(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.viridian_gym_requirement.value == ViridianGymRequirement.option_badges:
            return HasNBadges(world.options.viridian_gym_count.value).resolve(world)
        elif world.options.viridian_gym_requirement.value == ViridianGymRequirement.option_gyms:
            return HasNGyms(world.options.viridian_gym_count.value).resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class HasRoute22GateRequirements(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.route22_gate_requirement.value == Route22GateRequirement.option_badges:
            return HasNBadges(world.options.route22_gate_count.value).resolve(world)
        elif world.options.route22_gate_requirement.value == Route22GateRequirement.option_gyms:
            return HasNGyms(world.options.route22_gate_count.value).resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class CanLeavePewter(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.pewter_city_roadblock.value == PewterCityRoadblock.option_brock:
            return Has("Defeat Brock").resolve(world)
        elif world.options.pewter_city_roadblock.value == PewterCityRoadblock.option_boulder_badge:
            return Has("Boulder Badge").resolve(world)
        elif world.options.pewter_city_roadblock.value == PewterCityRoadblock.option_any_gym:
            return HasNGyms(1).resolve(world)
        elif world.options.pewter_city_roadblock.value == PewterCityRoadblock.option_any_badge:
            return HasNBadges(1).resolve(world)
        elif world.options.pewter_city_roadblock.value == PewterCityRoadblock.option_open:
            return True_().resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class HasCeruleanCaveRequirement(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_vanilla:
            return HasAll("Defeat Champion", "Restore Pokemon Network Machine").resolve(world)
        elif world.options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_champion:
            return Has("Defeat Champion").resolve(world)
        elif world.options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_restore_network:
            return Has("Restore Pokemon Network Machine").resolve(world)
        elif world.options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_badges:
            return HasNBadges(world.options.cerulean_cave_count.value).resolve(world)
        elif world.options.cerulean_cave_requirement.value == CeruleanCaveRequirement.option_gyms:
            return HasNGyms(world.options.cerulean_cave_count.value).resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class CanBuyCoins(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (Has("Coin Case") & CanReachRegion("Celadon Game Corner")).resolve(world)


@dataclasses.dataclass
class CanStopSeafoamB3FCurrent(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (
            CanStrength() &
            CanReachRegion("Seafoam Islands 1F") &
            CanReachRegion("Seafoam Islands B1F (West)") &
            CanReachRegion("Seafoam Islands B1F (Northeast)") &
            CanReachRegion("Seafoam Islands B2F (Northwest)") &
            CanReachRegion("Seafoam Islands B2F (Northeast)")
        ).resolve(world)


@dataclasses.dataclass
class CanStopSeafoamB4FCurrent(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (
            CanStrength() &
            CanReachRegion("Seafoam Islands B3F (West)")
        ).resolve(world)


@dataclasses.dataclass
class CanPushMansionSwitch(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        return (
            CanReachRegion("Pokemon Mansion 1F") |
            CanReachRegion("Pokemon Mansion 2F") |
            CanReachRegion("Pokemon Mansion 3F (North)") |
            CanReachRegion("Pokemon Mansion B1F")
        ).resolve(world)


@dataclasses.dataclass
class HasRoute23GuardRequirements(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.route23_guard_requirement == Route23GuardRequirement.option_badges:
            return HasNBadges(world.options.route23_guard_count.value).resolve(world)
        elif world.options.route23_guard_requirement == Route23GuardRequirement.option_gyms:
            return HasNGyms(world.options.route23_guard_count.value).resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class HasE4Requirements(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if world.options.elite_four_requirement == EliteFourRequirement.option_badges:
            return HasNBadges(world.options.elite_four_count.value).resolve(world)
        elif world.options.elite_four_requirement == EliteFourRequirement.option_gyms:
            return HasNGyms(world.options.elite_four_count.value).resolve(world)
        return False_().resolve(world)


@dataclasses.dataclass
class HasE4RematchRequirements(Rule["PokemonFRLGWorld"], game=GAME):
    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        rule = False_()
        if world.options.elite_four_rematch_requirement == EliteFourRematchRequirement.option_badges:
            rule = HasNBadges(world.options.elite_four_rematch_count.value)
        elif world.options.elite_four_rematch_requirement == EliteFourRematchRequirement.option_gyms:
            rule = HasNGyms(world.options.elite_four_rematch_count.value)
        return (rule & HasAll("Defeat Champion", "Restore Pokemon Network Machine")).resolve(world)


@dataclasses.dataclass
class TwoIslandStallExpansion(Rule["PokemonFRLGWorld"], game=GAME):
    level: int

    @override
    def _instantiate(self, world: "PokemonFRLGWorld") -> Rule.Resolved:
        if self.level == 1:
            return Has("Rescue Lostelle").resolve(world)
        elif self.level == 2:
            return HasAll("Rescue Lostelle", "Defeat Champion").resolve(world)
        elif self.level == 3:
            return HasAll("Rescue Lostelle", "Defeat Champion", "Restore Pokemon Network Machine").resolve(world)
        return False_().resolve(world)

import dataclasses
from typing import TYPE_CHECKING, Dict, List, Any, override, Set, Tuple

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.rules import Has, Rule, False_, HasAll, True_
from .strings.locations import HarpyPath, Spell, ShadyWell, DarkForest, ForestOfLight, LightGarden, MagicTown, \
    SatanVilla, AncientRuins, School, \
    AncientVillage, DragonAreas, Bestiary, LookoutMountain, SageMountain, Bazaar
from .strings.region_entrances import MadouEntrance
from .strings.items import Tool, Custom, Special, Souvenir, EventItem, Gem, SpellItem, FlightUnlocks
from .options import MadouOptions

if TYPE_CHECKING:
    from . import MadouWorld


class MadouRules:
    world: "MadouWorld"
    region_rules: Dict[str, Rule[Any]]
    entrance_rules: Dict[str, Rule[Any]]
    location_rules: Dict[str, Rule[Any]]

    def __init__(self, world: "MadouWorld") -> None:
        self.player = world.player
        self.world = world
        self.world.options = world.options
        self.starting_magic = tuple(world.options.starting_magic.value)
        self.fairy_search = False_()
        if self.world.options.skip_fairy_search:
            self.fairy_search = True_()

        self.region_rules = {

        }

        self.entrance_rules = {
            MadouEntrance.village_to_nw_cave: Has(Tool.ribbit_boots),
            MadouEntrance.nw_cave_to_village: Has(Tool.ribbit_boots),
            MadouEntrance.forest_to_frog: Has(Tool.ribbit_boots),
            MadouEntrance.frog_to_forest: Has(Tool.ribbit_boots),
            MadouEntrance.ruins_to_ancient_ruins: Has(Tool.magic_bracelet),
            MadouEntrance.rain_forest_to_ancient_village: Has(Tool.hammer),
            MadouEntrance.ancient_to_zoh: Has(Special.elephant_head),
            MadouEntrance.nw_cave_to_smoky: Has(Custom.bomb),
            MadouEntrance.smoky_to_bazaar: Has(Tool.ribbit_boots),
            MadouEntrance.death_to_bazaar: Has(Special.bazaar_pass) & Has(Tool.ribbit_boots),
            MadouEntrance.smoky_left_to_right: Has(Tool.ribbit_boots),
            MadouEntrance.magic_village_to_tower: self.HasGoodEnoughCombatLevel(5, self.starting_magic) &
                                                                Has("Final Exam Certificate"),
            MadouEntrance.headmaster_to_school_maze: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            MadouEntrance.smoky_to_graveyard: Has(Special.dark_flower) & Has(Special.leaf),
            MadouEntrance.dark_forest_to_well: Has(Tool.ribbit_boots),
            MadouEntrance.dark_forest_to_satan: Has(Tool.ribbit_boots) & Has(Special.secret_stone, 3),
            MadouEntrance.dark_forest_to_maze: Has(Tool.ribbit_boots),
            MadouEntrance.dark_forest_to_dark_orb: Has(Tool.ribbit_boots),
            MadouEntrance.wolf_to_sage: Has(Tool.ribbit_boots),
            MadouEntrance.sage_to_wolf: Has(Tool.ribbit_boots),
            MadouEntrance.sage_to_summit: Has(Tool.ribbit_boots),
            # TODO: find a way to make the game accept a flight path even if you only have one; this isn't very intuitive.
            MadouEntrance.flight_magic_to_ruins: Has(FlightUnlocks.ruins_town) & self.has_any_flight_path_other_than(FlightUnlocks.ruins_town),
            MadouEntrance.flight_magic_to_wolf: Has(FlightUnlocks.wolf_town) & self.has_any_flight_path_other_than(FlightUnlocks.wolf_town),
            MadouEntrance.flight_magic_to_ancient: Has(FlightUnlocks.ancient_village) & self.has_any_flight_path_other_than(FlightUnlocks.ancient_village),
            MadouEntrance.flight_magic_to_sage: Has(FlightUnlocks.sage_mountain) & self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain),
            MadouEntrance.flight_ruins_to_magic: Has(FlightUnlocks.magic_village) & self.has_any_flight_path_other_than(FlightUnlocks.magic_village),
            MadouEntrance.flight_ruins_to_ancient: Has(FlightUnlocks.ancient_village) & self.has_any_flight_path_other_than(FlightUnlocks.ancient_village),
            MadouEntrance.flight_ruins_to_wolf: Has(FlightUnlocks.wolf_town) & self.has_any_flight_path_other_than(FlightUnlocks.wolf_town),
            MadouEntrance.flight_ruins_to_sage: Has(FlightUnlocks.sage_mountain) & self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain),
            MadouEntrance.flight_wolf_to_magic: Has(FlightUnlocks.magic_village) & self.has_any_flight_path_other_than(FlightUnlocks.magic_village),
            MadouEntrance.flight_wolf_to_ruins: Has(FlightUnlocks.ruins_town) & self.has_any_flight_path_other_than(FlightUnlocks.ruins_town),
            MadouEntrance.flight_wolf_to_ancient: Has(FlightUnlocks.ancient_village) & self.has_any_flight_path_other_than(FlightUnlocks.ancient_village),
            MadouEntrance.flight_wolf_to_sage: Has(FlightUnlocks.sage_mountain) & self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain),
            MadouEntrance.flight_ancient_to_magic: Has(FlightUnlocks.magic_village) & self.has_any_flight_path_other_than(FlightUnlocks.magic_village),
            MadouEntrance.flight_ancient_to_ruins: Has(FlightUnlocks.ruins_town) & self.has_any_flight_path_other_than(FlightUnlocks.ruins_town),
            MadouEntrance.flight_ancient_to_wolf: Has(FlightUnlocks.wolf_town) & self.has_any_flight_path_other_than(FlightUnlocks.wolf_town),
            MadouEntrance.flight_ancient_to_sage: Has(FlightUnlocks.sage_mountain) & self.has_any_flight_path_other_than(FlightUnlocks.sage_mountain),
            MadouEntrance.flight_sage_to_magic: Has(FlightUnlocks.magic_village) & self.has_any_flight_path_other_than(FlightUnlocks.magic_village),
            MadouEntrance.flight_sage_to_ruins: Has(FlightUnlocks.ruins_town) & self.has_any_flight_path_other_than(FlightUnlocks.ruins_town),
            MadouEntrance.flight_sage_to_wolf: Has(FlightUnlocks.wolf_town) & self.has_any_flight_path_other_than(FlightUnlocks.wolf_town),
            MadouEntrance.flight_sage_to_ancient: Has(FlightUnlocks.ancient_village) & self.has_any_flight_path_other_than(FlightUnlocks.ancient_village),
        }

        self.location_rules = {
            "Chest on Sage Mountain": Has(Special.secret_stone, self.world.options.required_secret_stones.value) & (self.fairy_search | Has(Special.dark_orb)),

            MagicTown.magic_bracelet: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            SatanVilla.satan: Has(Special.secret_stone, 3),
            ForestOfLight.sukiyapodes_2: Has(Special.light_orb) & Has(Tool.ribbit_boots),
            Spell.thunder_dark_forest: Has(Tool.ribbit_boots),
            Spell.diacute_dark_forest: Has(Tool.ribbit_boots),
            DarkForest.green_gem: Has(Tool.ribbit_boots),
            DarkForest.dark_flower: Has(Special.dark_orb),
            LightGarden.purple_orb: Has(Tool.toy_elephant),
            LightGarden.bouquet: Has(Special.leaf) & Has(Special.dark_flower) & Has(EventItem.unpetrify),
            ShadyWell.lofu: Has(Tool.toy_elephant),
            SageMountain.cyan_orb: Has(Tool.toy_elephant) & Has(Tool.ribbit_boots),
            DarkForest.rele: Has(Tool.toy_elephant),
            MagicTown.white_gem: self.has_souvenirs(),
            LookoutMountain.red_gem: Has(Tool.ribbit_boots),
            #  Gold Tablets
            Spell.fire_school: Has(Tool.magical_dictionary),
            Spell.fire_library: HasAll(*Gem.gems) & Has(Tool.magical_dictionary),
            Spell.ice_storm_underground: Has(Tool.magical_dictionary),
            Spell.ice_storm_library: HasAll(*Gem.gems) & Has(Tool.magical_dictionary),
            Spell.thunder_northwestern: Has(Tool.magic_ribbon) & Has(Tool.magical_dictionary),
            Spell.thunder_library: HasAll(*Gem.gems) & Has(Tool.magical_dictionary),
            Spell.diacute_library: HasAll(*Gem.gems) & Has(Tool.magical_dictionary),
            #  Combat Rules
            ForestOfLight.orb: self.HasGoodEnoughCombatLevel(1, self.starting_magic) & Has(Tool.ribbit_boots),
            ForestOfLight.ribbit_boots: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            ForestOfLight.sukiyapodes_1: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            AncientRuins.zoh_daimaoh: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            HarpyPath.bag: Has(Tool.panotty_flute) & self.HasGoodEnoughCombatLevel(2, self.starting_magic) & Has(Tool.ribbit_boots),
            ShadyWell.arachne: Has(Special.ripe_cucumber) & self.HasGoodEnoughCombatLevel(2, self.starting_magic),
            School.magical_dictionary: self.HasGoodEnoughCombatLevel(2, self.starting_magic),
            AncientVillage.elder: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            AncientVillage.villager_1: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            AncientVillage.villager_2: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            AncientVillage.villager_3: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            AncientVillage.villager_4: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            AncientVillage.villager_5: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            AncientVillage.villager_6: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            DragonAreas.firefly_egg: Has(Special.bouquet) & self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            DragonAreas.stone: self.HasGoodEnoughCombatLevel(4, self.starting_magic) & Has(Special.firefly_egg, 2),
            MagicTown.suketoudara: Has(Special.secret_stone, 7) & self.HasGoodEnoughCombatLevel(4, self.starting_magic),
            Bestiary.flea: Has(Tool.toy_elephant),
            DarkForest.ribbon: self.HasGoodEnoughCombatLevel(2, self.starting_magic),
            # Boss checks require that you can actually defeat them
            Bestiary.owlbear: Has(Special.secret_stone, 8) & Has(Special.dark_orb) & self.HasGoodEnoughCombatLevel(4, self.starting_magic),
            Bestiary.sukiyapodes: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Bestiary.mini_zombie: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Bestiary.zoh: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Bestiary.arachne: self.HasGoodEnoughCombatLevel(2, self.starting_magic) & Has(Special.ripe_cucumber),
            Bestiary.headmaster: self.HasGoodEnoughCombatLevel(2, self.starting_magic),
            Bestiary.harpy: self.HasGoodEnoughCombatLevel(2, self.starting_magic) & Has(Tool.panotty_flute) & Has(Tool.ribbit_boots),
            Bestiary.skeleton_d: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            Bestiary.skeleton_t: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
            Bestiary.nasu_grave: self.HasGoodEnoughCombatLevel(2, self.starting_magic),
            Bestiary.leviathan: self.HasGoodEnoughCombatLevel(4, self.starting_magic) & Has(Special.firefly_egg, 2),
            # Shop locations require combat to farm money.
            Souvenir.dragon_nail: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.magic_king_foot: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.magic_king_tusk: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.magic_king_picture: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.magic_king_statue: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.waterfall_vase: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.wolf_tail: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Souvenir.dark_jug: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Bazaar.bazaar_pass: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            Bazaar.elephant: self.HasGoodEnoughCombatLevel(1, self.starting_magic),
            # Firefly egg is really expensive, so push it a bit later.
            Bazaar.firefly_egg: self.HasGoodEnoughCombatLevel(3, self.starting_magic),
        }

    def has_souvenirs(self):
        if self.world.options.souvenir_hunt:
            return HasAll(*Souvenir.souvenirs)
        return HasAll(*EventItem.shops)

    def has_any_flight_path_other_than(self, exception: str):
        flights = [FlightUnlocks.magic_village, FlightUnlocks.ancient_village, FlightUnlocks.wolf_town, FlightUnlocks.ruins_town, FlightUnlocks.sage_mountain]
        flights.remove(exception)
        has_path = False_()
        for flight in flights:
            has_path = has_path | Has(flight)
        return has_path
    
    
    @dataclasses.dataclass()
    class HasGoodEnoughCombatLevel(Rule["MadouWorld"], game="Madou Monogatari Hanamaru Daiyouchienji"):

        level: int
        starting_spells: Tuple[str]

        @override
        def _instantiate(self, world: "MadouWorld") -> Rule.Resolved:
            # caching_enabled only needs to be passed in when your world inherits from CachedRuleBuilderWorld
            return self.Resolved(self.level, self.starting_spells, player=world.player)

        class Resolved(Rule.Resolved):
            level: int
            starting_spells: Tuple[str]

            @override
            def _evaluate(self, state: CollectionState) -> bool:
                total_combat_spell_items = state.count_from_list(SpellItem.combat_spells, self.player)
                if total_combat_spell_items == 0:
                    return False
                stun_rule = True
                diacute_count = max(0, self.level - 1)
                if "Fire" in self.starting_spells:
                    total_combat_spell_items += 1
                if "Ice Storm" in self.starting_spells:
                    total_combat_spell_items += 1
                if "Thunder" in self.starting_spells:
                    total_combat_spell_items += 1
                average_count = total_combat_spell_items // 3
                if self.level > 1:
                    stun_rule = state.has(SpellItem.bayoen, self.player)
                return (state.has(SpellItem.diacute, self.player, diacute_count) and stun_rule and average_count >= min(
                    4, self.level)) or state.has(EventItem.glitch, self.player)

            @override
            def item_dependencies(self) -> dict[str, set[int]]:
                # this function is only required if you have caching enabled
                return {"Fire": {id(self)},
                        "Ice Storm": {id(self)},
                        "Thunder": {id(self)},
                        "Diacute": {id(self)},}

            @override
            def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
                # this method can be overridden to display custom explanations
                return [
                    {"type": "text", "text": "Has Effective Combat Level "},
                    {"type": "color", "color": "green" if state and self(state) else "salmon", "text": str(self.level)},
                ]
    

    def set_madou_rules(self) -> None:
        for region in self.world.get_regions():
            for entrance in region.entrances:
                if entrance.name in self.entrance_rules:
                    self.world.set_rule(entrance, self.entrance_rules[entrance.name])
            for loc in region.locations:
                if loc.name in self.location_rules:
                    self.world.set_rule(loc, self.location_rules[loc.name])

from typing import TYPE_CHECKING, override
from dataclasses import dataclass

from rule_builder.rules import Rule, True_, False_, And, Or, Has, HasGroup, CanReachLocation, CollectionState, OptionFilter
from .locations import wonderful, multiple, secret_exit, course, bonus, species_data_tables, \
    PokemonSnapLocationCategory as Category, RNG_LOCATIONS, HARD_LOCATIONS, POKEMON_IN_MULTIPLE_LEVELS
from .constants import *
from .items import PokemonSnapItemCategory as ItemCategory, fragment, course as course_item
from .options import GoalType, PhotoScoring, IncludeRNGChecks, UseHardLogic
if TYPE_CHECKING:
    from . import PokemonSnapWorld

try:
    from rule_builder.rules import AtLeast # Added in 0.6.8
except ImportError:
    from .future_rules import AtLeast

_NO_ITEMS   = True_()

_SEPARATE_SCORING = OptionFilter(PhotoScoring, [PhotoScoring.option_separate, PhotoScoring.option_separate_unlocks], operator="in")
_RNG_LOCATIONS_ON = OptionFilter(IncludeRNGChecks, IncludeRNGChecks.option_true)
_HARD_LOGIC_ON    = OptionFilter(UseHardLogic, UseHardLogic.option_true)

REPORT_EXCLUSIONS = RNG_LOCATIONS + HARD_LOCATIONS

_identity = lambda s: s

location_name_functions = {
    Category.NORMAL_PHOTO:    _identity,
    Category.WONDERFUL_PHOTO: wonderful,
    Category.MULTIPLE_PHOTO:  multiple,
    Category.SPECIAL_POSE:    _identity,
    Category.POKEMON_SIGN:    _identity,
    Category.SECRET_EXIT:     secret_exit,
    Category.PHOTO_COUNT:     _identity,
    Category.REPORT_SCORE:    _identity,
}


def location_name(name: str, category: Category):
    return location_name_functions[category](name)


def set_location_rule(world: "PokemonSnapWorld", name: str, category: Category, rule: Rule):
    try:
        base_name = location_name(name, category)
        world.set_rule(world.get_location(base_name), rule)
        # Make sure the bonus locations also have the same rules
        world.set_rule(world.get_location(bonus(base_name)), rule)
    except KeyError:
        # The location wasn't added, so skip the logic for it
        # TODO: this is hacky, let's do it better eventually
        pass


def wonderful_requirement(world: "PokemonSnapWorld"):
    if world.options.photo_scoring == PhotoScoring.option_progressive_unlocks:
        return Has(PROG_SCORING, 1)
    elif world.options.photo_scoring == PhotoScoring.option_separate_unlocks:
        return Has(WDFL_SCORING)
    
    return _NO_ITEMS


def multiple_requirement(world: "PokemonSnapWorld"):
    if world.options.photo_scoring == PhotoScoring.option_progressive_unlocks:
        return Has(PROG_SCORING, 2)
    elif world.options.photo_scoring == PhotoScoring.option_separate_unlocks:
        return Has(MULT_SCORING)

    return _NO_ITEMS


def has(item_name: str, course_name: str):
    if item_name == POKEMON_FOOD:
        return Has(POKEMON_FOOD) | Has(course_item(POKEMON_FOOD, course_name)) | Has(APPLE) | Has(course_item(APPLE, course_name))
    return Has(item_name) | Has(course_item(item_name, course_name))


def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))

    for level in [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY]:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {level}'), Has(level) | Has(fragment(level), world.options.map_fragments.value))

    if world.options.goal_type == GoalType.option_signs:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'),
                       HasGroup(ItemCategory.SIGN_PIC.value, world.options.signs_required.value))
    elif world.options.goal_type == GoalType.option_pokemon_pictures:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'),
                       HasGroup(ItemCategory.POKEMON_PIC.value, world.options.pokemon_required.value))

    # World location rules
    for name, categories in LOCATION_RULES.items():
        for category, rule in categories.items():
            if category == Category.WONDERFUL_PHOTO:
                rule = And(wonderful_requirement(world), rule)
            if category == Category.MULTIPLE_PHOTO:
                rule = And(multiple_requirement(world), rule)
            
            set_location_rule(world, name, category, rule)


@dataclass()
class ReportScoreAchievable(Rule["PokemonSnapWorld"], game="Pokemon Snap"):
    """
    This is hacky at best, but works for now. 

    In _instantiate, for each pokemon, we create a list of location rules
    that are independent of the world options (otherwise wonderful/multiple 
    would be inaccessible). This list is passed to the Resolved rule. This
    will probably need to be revisited when we add progressive lenses.

    In the resolved rule, we heuristically estimate an upper bound for
    the achievable score given the current game state, based on some
    crude estimates for each line on the score sheet. Notably, we are
    ignoring special poses. This is potentially a To-Do, but I think
    the logic will actually be nicer without it.
    """
    score_goal: int

    @override
    def _instantiate(self, world: "PokemonSnapWorld") -> Rule.Resolved:
        all_pokemon_rules = [
            (self.build_rules_triplet(world, pokemon_name), ) # 1-tuple for pokemon only in one course
            for pokemon_name in ALL_INGAME_POKEMON
            if pokemon_name not in POKEMON_IN_MULTIPLE_LEVELS
        ]

        for pokemon_name in POKEMON_IN_MULTIPLE_LEVELS:
            this_pokemon_rules = []
            for level_name in ALL_MAIN_LEVELS:
                location_name = course(pokemon_name, level_name)
                if location_name not in LOCATION_RULES: continue

                this_pokemon_rules.append(self.build_rules_triplet(world, location_name))
            all_pokemon_rules.append(tuple(this_pokemon_rules))

        return self.Resolved(self.score_goal, tuple(all_pokemon_rules), player=world.player)

    def build_rules_triplet(self, world: "PokemonSnapWorld", location: str):
        species_data = [species_data for region in species_data_tables for species_data in species_data_tables[region] if species_data.name == location][0]
        
        normal_rule = CanReachLocation(location_name(location, Category.NORMAL_PHOTO))

        wonderful_rule = False_()
        if species_data.wonderful and wonderful(location) not in REPORT_EXCLUSIONS:
            if (location not in LOCATION_RULES or Category.WONDERFUL_PHOTO not in LOCATION_RULES[location]):
                wonderful_rule = normal_rule
            else:
                wonderful_rule = And(normal_rule, LOCATION_RULES[location][Category.WONDERFUL_PHOTO], wonderful_requirement(world))

        multiple_rule = False_()
        if species_data.multiple and multiple(location) not in REPORT_EXCLUSIONS:
            access_requirement = wonderful_rule | (normal_rule & _SEPARATE_SCORING)
            if (location not in LOCATION_RULES or Category.MULTIPLE_PHOTO not in LOCATION_RULES[location]):
                multiple_rule = access_requirement
            else:
                multiple_rule = And(access_requirement, LOCATION_RULES[location][Category.MULTIPLE_PHOTO], multiple_requirement(world))

        return normal_rule.resolve(world), wonderful_rule.resolve(world), multiple_rule.resolve(world)

    class Resolved(Rule.Resolved):
        score_goal: int
        all_pokemon_rules: tuple[tuple[tuple[Rule.Resolved, Rule.Resolved, Rule.Resolved]]]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            achievable_score_total = 0
            for rule_set in self.all_pokemon_rules:
                achievable_score_total += max((self.achievable_score(state, *rule_tuple) for rule_tuple in rule_set), default=0)
                if achievable_score_total >= self.score_goal: return True
            return False

        def achievable_score(self, state: CollectionState, normal_rule: Rule.Resolved, wonderful_rule: Rule.Resolved, multiple_rule: Rule.Resolved):
            # This is a heuristic, as it can change drastically between pokemon
            if not normal_rule(state): return 0

            score = 200
            if wonderful_rule(state):
                score += 900 # 150 more for size, and 750 more for pose
                score *= 2
            if multiple_rule(state):
                score += 150

            return score


@dataclass()
class HasFilm(Rule["PokemonSnapWorld"], game="Pokemon Snap"):
    film_requirement: int

    @override
    def _instantiate(self, world: "PokemonSnapWorld") -> Rule.Resolved:
        return self.Resolved(self.film_requirement,
                             world.options.starting_film.value,
                             world.options.film_upgrade_amount.value,
                             world.options.maximum_film.value,
                             player=world.player)

    class Resolved(Rule.Resolved):
        film_requirement: int
        film_start: int
        film_step: int
        film_cap: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            upgrade_count = state.count(FILM_UPGRADE, self.player)
            total_film = min(self.film_cap, self.film_start + upgrade_count * self.film_step)
            return total_film >= self.film_requirement


_CAN_REACH_ALL_POKEMON = [
    CanReachLocation(pokemon_name)
    for pokemon_name in ALL_INGAME_POKEMON
    if pokemon_name not in POKEMON_IN_MULTIPLE_LEVELS
] + [
    Or(*[
        CanReachLocation(course(pokemon_name, level))
        for level in levels
    ])
    for pokemon_name, levels in POKEMON_IN_MULTIPLE_LEVELS.items()
]


LOCATION_RULES = {
    # Beach
    BUTTERFREE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    PIDGEY: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    MEOWTH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    DODUO: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    CHANSEY: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
    },
    KANGASKHAN: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
    },
    SCYTHER: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_BEACH),
    },
    LAPRAS: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON),
        Category.MULTIPLE_PHOTO:  HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON),
    },
    EEVEE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SNORLAX: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_BEACH) | has(POKEFLUTE, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_BEACH) | has(POKEFLUTE, LVL_BEACH),
    },
    course(PIKACHU, LVL_BEACH): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_BEACH),
    },
    course(MAGIKARP, LVL_BEACH): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
    },
    SURFING_PIKACHU:    { Category.SPECIAL_POSE: has(POKEMON_FOOD, LVL_BEACH) },
    PIKACHU_ON_A_STUMP: { Category.SPECIAL_POSE: has(PESTER_BALL, LVL_BEACH) },
    GUST_USING_PIDGEY:  { Category.SPECIAL_POSE: _NO_ITEMS },
    BEACH_SIGN:         { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },


    # Tunnel
    KAKUNA: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL) | Has(DASH_ENGINE)) | _SEPARATE_SCORING | _HARD_LOGIC_ON,
    },
    DIGLETT: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    DUGTRIO: {
        Category.NORMAL_PHOTO:    HasFilm(5) | (HasFilm(4) & _HARD_LOGIC_ON),
        Category.WONDERFUL_PHOTO: HasFilm(5) | (HasFilm(4) & _HARD_LOGIC_ON),
        Category.MULTIPLE_PHOTO:  HasFilm(7) | (HasFilm(5) & _HARD_LOGIC_ON),
    },
    MAGNEMITE: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_TUNNEL),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_TUNNEL),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_TUNNEL),
    },
    MAGNETON: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_TUNNEL),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_TUNNEL),
    },
    HAUNTER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    ELECTRODE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    ELECTABUZZ: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        # Without Zapdos you have to ignore the first Buzz and throw at the second - spoiler in doc
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL)
    },
    ZAPDOS: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_TUNNEL) & has(POKEFLUTE, LVL_TUNNEL),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_TUNNEL) & has(POKEFLUTE, LVL_TUNNEL),
    },
    course(ZUBAT, LVL_TUNNEL): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(MAGIKARP, LVL_TUNNEL): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(PIKACHU, LVL_TUNNEL): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    PIKACHU_ON_A_BALL: { Category.SPECIAL_POSE: HasFilm(5) | (HasFilm(3) & _HARD_LOGIC_ON) },
    TUNNEL_SIGN:       { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) & has(POKEMON_FOOD, LVL_TUNNEL) & has(POKEFLUTE, LVL_TUNNEL) },
    LVL_TUNNEL:        { Category.SECRET_EXIT: has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL) },


    # Volcano
    CHARMANDER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VOLCANO) | [_SEPARATE_SCORING, _RNG_LOCATIONS_ON] | _HARD_LOGIC_ON,
    },
    CHARMELEON: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    CHARIZARD: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    VULPIX: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VOLCANO) | _SEPARATE_SCORING | (Has(DASH_ENGINE) & _HARD_LOGIC_ON),
    },
    GROWLITHE: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VOLCANO),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_VOLCANO) & has(PESTER_BALL, LVL_VOLCANO)) | (has(PESTER_BALL, LVL_VOLCANO) & _SEPARATE_SCORING),
    },
    ARCANINE: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VOLCANO),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_VOLCANO) & has(PESTER_BALL, LVL_VOLCANO)) | (has(PESTER_BALL, LVL_VOLCANO) & _SEPARATE_SCORING),
    },
    RAPIDASH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    MAGMAR: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        # This _might_ be possible without moving the Moltres egg, but I don't think you can get close enough
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    MOLTRES: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    course(MAGIKARP, LVL_VOLCANO): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    FIGHTING_MAGMAR: { Category.SPECIAL_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    VOLCANO_SIGN:    { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) & has(PESTER_BALL, LVL_VOLCANO) },


    # River
    METAPOD: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_RIVER) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_RIVER) | _SEPARATE_SCORING | _HARD_LOGIC_ON,
    },
    VILEPLUME: {
        Category.NORMAL_PHOTO:    has(POKEFLUTE, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(POKEFLUTE, LVL_RIVER),
    },
    PSYDUCK: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
    },
    POLIWAG: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) | _HARD_LOGIC_ON,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
    },
    SLOWPOKE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SLOWBRO: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER),
    },
    SHELLDER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: Has(DASH_ENGINE) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  Has(DASH_ENGINE) | _HARD_LOGIC_ON,
    },
    CLOYSTER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    PORYGON: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_RIVER),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_RIVER) & has(PESTER_BALL, LVL_RIVER)) | (has(PESTER_BALL, LVL_RIVER) & _SEPARATE_SCORING & _RNG_LOCATIONS_ON),
    },
    course(BULBASAUR, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER)
    },
    course(MAGIKARP, LVL_RIVER): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
    },
    course(PIKACHU, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SPEED_PIKACHU: { Category.SPECIAL_POSE: HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON) | has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    RIVER_SIGN:    { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) & has(POKEFLUTE, LVL_RIVER) },
    LVL_RIVER:     { Category.SECRET_EXIT: has(PESTER_BALL, LVL_RIVER) },


    # Cave
    JIGGLYPUFF: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
    },
    WEEPINBELL: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    VICTREEBEL: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
    },
    GRIMER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON),
    },
    MUK: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_CAVE) & (HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON)),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_CAVE) & (HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON)),
    },
    JYNX: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEFLUTE, LVL_CAVE),
    },
    DITTO: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_CAVE),
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_CAVE),
    },
    ARTICUNO: {
        Category.NORMAL_PHOTO:    has(POKEFLUTE, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(POKEFLUTE, LVL_CAVE),
    },
    KOFFING: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(BULBASAUR, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    course(MAGIKARP, LVL_CAVE): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
    },
    course(PIKACHU, LVL_CAVE): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) | _HARD_LOGIC_ON,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) | _HARD_LOGIC_ON,
    },
    course(ZUBAT, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    BALLOON_PIKACHU:     { Category.SPECIAL_POSE:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    FLYING_PIKACHU:      { Category.SPECIAL_POSE: (has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE)) & has(POKEFLUTE, LVL_CAVE) },
    JIGGLYPUFF_ON_STAGE: { Category.SPECIAL_POSE:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    JIGGLYPUFF_TRIO:     { Category.SPECIAL_POSE:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    CAVE_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },


    # Valley
    SQUIRTLE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_VALLEY) | (Has(DASH_ENGINE) & _HARD_LOGIC_ON),
    },
    SANDSHREW: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_VALLEY) & has(PESTER_BALL, LVL_VALLEY)),
    },
    SANDSLASH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: Has(DASH_ENGINE) | has(PESTER_BALL, LVL_VALLEY),
    },
    MANKEY: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    GEODUDE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    GRAVELER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY) | has(POKEFLUTE, LVL_VALLEY) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  has(POKEFLUTE, LVL_VALLEY) | _HARD_LOGIC_ON,
    },
    GOLDEEN: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
    },
    STARYU: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    STARMIE: {
        Category.NORMAL_PHOTO:    HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON),
        Category.WONDERFUL_PHOTO: HasFilm(7) | (HasFilm(2) & _HARD_LOGIC_ON),
        Category.MULTIPLE_PHOTO:  HasFilm(9) | (HasFilm(3) & _HARD_LOGIC_ON),
    },
    GYARADOS: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY),
    },
    DRATINI: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
    },
    DRAGONITE: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY),
    },
    course(MAGIKARP, LVL_VALLEY): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY) | Has(DASH_ENGINE),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
    },
    GRAVELERS_GROUP_DANCE: { Category.SPECIAL_POSE: has(POKEFLUTE, LVL_VALLEY) },
    VALLEY_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    LVL_VALLEY:            { Category.SECRET_EXIT:  has(PESTER_BALL, LVL_VALLEY) },

    # Cloud
    # Rainbow Cloud
    MEW: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CLOUD) | has(PESTER_BALL, LVL_CLOUD),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CLOUD) | has(PESTER_BALL, LVL_CLOUD),
    },

    # Oak Rewards
    POKEMON_TOTAL_6:  { Category.PHOTO_COUNT: AtLeast(6,  *_CAN_REACH_ALL_POKEMON) },
    POKEMON_TOTAL_22: { Category.PHOTO_COUNT: AtLeast(22, *_CAN_REACH_ALL_POKEMON) },
    POKEMON_TOTAL_40: { Category.PHOTO_COUNT: AtLeast(40, *_CAN_REACH_ALL_POKEMON) },

    REPORT_SCORE_24_000:  { Category.REPORT_SCORE: ReportScoreAchievable( 24_000) },
    REPORT_SCORE_72_500:  { Category.REPORT_SCORE: ReportScoreAchievable( 72_500) },
    REPORT_SCORE_130_000: { Category.REPORT_SCORE: ReportScoreAchievable(130_000) },
}

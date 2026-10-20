import typing
from enum import StrEnum
from math import ceil
from itertools import product
from typing import NamedTuple
from .constants import *
from .options import GoalType, PhotoScoring, PressLToStop, GoalItemNamingScheme, FillerItemNamingScheme, AppleNamingScheme

from BaseClasses import Item

if typing.TYPE_CHECKING:
    from worlds.pokemon_snap import PokemonSnapWorld


class PokemonSnapItemCategory(StrEnum):
    VICTORY = "Victory"
    TOOL = "Tools"
    PHOTO_SCORING = "Scoring"
    AREA = "Courses"
    MAP_FRAGMENT = "Fragments"
    MISC = "Miscellaneous"
    POKEMON_PIC = "Pokemon Pictures"
    SIGN_PIC = "Sign Pictures"
    TRASH_CUSTOM  = "Special Garbage"
    TRASH_PICTURE = "Garbage Photos"
    TRASH_SIMPLE  = "Simple Garbage"


class PokemonSnapItemData(NamedTuple):
    name: str
    ps_code: int
    category: PokemonSnapItemCategory


class PokemonSnapItem(Item):
    game: str = "Pokemon Snap"

    @staticmethod
    def get_name_to_id() -> dict:
        return {item_data.name: item_data.ps_code for item_data in _all_items}

fragment   = lambda s: f'{s}: Map Fragment'
unfragment = lambda s: s[:-len(': Map Fragment')]

key_item_names = {
    VICTORY_ITEM_NAME,

    LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD,
    *map(fragment, [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD]),

    POKEMON_FOOD, APPLE, PESTER_BALL, POKEFLUTE, DASH_ENGINE, SIGN_DETECTOR,
    *(course(POKEMON_FOOD, c) for c in ALL_LEVELS),
    *(course(APPLE, c)        for c in ALL_LEVELS),
    *(course(PESTER_BALL, c)  for c in ALL_LEVELS),
    *(course(POKEFLUTE, c)    for c in ALL_MAIN_LEVELS),

    PROG_SCORING, WDFL_SCORING, MULT_SCORING
}

pokemon_pics = [
    PokemonSnapItemData(f"{POKEMON_PIC_NAME}: {name}", 5000 + i, PokemonSnapItemCategory.POKEMON_PIC)
    for i, name in enumerate(ALL_INGAME_POKEMON)
]
POKEMON_PIC_NAMES = {item.name for item in pokemon_pics} | {POKEMON_PIC_NAME}

sign_pics = [
    PokemonSnapItemData(f"{SIGN_PIC_NAME}: {name}", 6000 + i, PokemonSnapItemCategory.SIGN_PIC)
    for i, name in enumerate(ALL_SIGNS)
]
SIGN_PIC_NAMES = {item.name for item in sign_pics} | {SIGN_PIC_NAME}

useful_item_names = {
    FILM_UPGRADE, L_TO_STOP, *POKEMON_PIC_NAMES, *SIGN_PIC_NAMES
}

# We're doing this weirdness so that each adjective/pokemon combo has its own ID.
# This way, when a tracker connects, it knows exactly which trash item you got.
# This also removes the mismatched checksum warning from Universal Tracker.
trash_pokemon_pics = {
    pokemon_name: [
        PokemonSnapItemData(
            f"{adjective} Photo of {pokemon_name}",
            10000 + i*len(TRASH_PIC_ADJECTIVES) + j, 
            PokemonSnapItemCategory.TRASH_PICTURE
        )
        for j, adjective in enumerate(TRASH_PIC_ADJECTIVES)
    ]
    for i, pokemon_name in enumerate(ORIGINAL_151)
    if pokemon_name not in ALL_INGAME_POKEMON
}

_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [
    (VICTORY_ITEM_NAME, VICTORY_ITEM_ID, PokemonSnapItemCategory.VICTORY),

    (POKEMON_PIC_NAME, 5500, PokemonSnapItemCategory.POKEMON_PIC),
    (SIGN_PIC_NAME,    6500, PokemonSnapItemCategory.SIGN_PIC),

    (POKEMON_FOOD,  1000, PokemonSnapItemCategory.TOOL),
    (PESTER_BALL,   1001, PokemonSnapItemCategory.TOOL),
    (APPLE,         1101, PokemonSnapItemCategory.TOOL),
    (POKEFLUTE,     1002, PokemonSnapItemCategory.TOOL),
    (DASH_ENGINE,   1003, PokemonSnapItemCategory.TOOL),
    (SIGN_DETECTOR, 1004, PokemonSnapItemCategory.TOOL),
    (L_TO_STOP,     1005, PokemonSnapItemCategory.TOOL),

    *((course(POKEMON_FOOD, c), 1000 + 10*(i+1), PokemonSnapItemCategory.TOOL) for i, c in enumerate(ALL_LEVELS)),
    *((course(APPLE,        c), 1100 + 10*(i+1), PokemonSnapItemCategory.TOOL) for i, c in enumerate(ALL_LEVELS)),
    *((course(PESTER_BALL,  c), 1001 + 10*(i+1), PokemonSnapItemCategory.TOOL) for i, c in enumerate(ALL_LEVELS)),
    *((course(POKEFLUTE,    c), 1002 + 10*(i+1), PokemonSnapItemCategory.TOOL) for i, c in enumerate(ALL_LEVELS)),

    (WDFL_SCORING,  1500, PokemonSnapItemCategory.PHOTO_SCORING),
    (MULT_SCORING,  1501, PokemonSnapItemCategory.PHOTO_SCORING),
    (PROG_SCORING,  1502, PokemonSnapItemCategory.PHOTO_SCORING),

    (LVL_BEACH,   2000, PokemonSnapItemCategory.AREA),
    (LVL_TUNNEL,  2001, PokemonSnapItemCategory.AREA),
    (LVL_VOLCANO, 2002, PokemonSnapItemCategory.AREA),
    (LVL_RIVER,   2003, PokemonSnapItemCategory.AREA),
    (LVL_CAVE,    2004, PokemonSnapItemCategory.AREA),
    (LVL_VALLEY,  2005, PokemonSnapItemCategory.AREA),

    (fragment(LVL_BEACH),   2100, PokemonSnapItemCategory.MAP_FRAGMENT),
    (fragment(LVL_TUNNEL),  2101, PokemonSnapItemCategory.MAP_FRAGMENT),
    (fragment(LVL_VOLCANO), 2102, PokemonSnapItemCategory.MAP_FRAGMENT),
    (fragment(LVL_RIVER),   2103, PokemonSnapItemCategory.MAP_FRAGMENT),
    (fragment(LVL_CAVE),    2104, PokemonSnapItemCategory.MAP_FRAGMENT),
    (fragment(LVL_VALLEY),  2105, PokemonSnapItemCategory.MAP_FRAGMENT),

    (FILM_UPGRADE, 3000, PokemonSnapItemCategory.MISC),

    ("ArsonAssassin's pokemon card collection", 4000, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Used reel of film", 4001, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Reminder to remove the lens cap", 4002, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Nothing, literally nothing at all", 4003, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Several decades worth of nostalgia", 4004, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Burger King voucher", 4005, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Super close-up of a thumb", 4006, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Futuristic Photo of Mareep", 4007, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Full Art Swinub Card", 4008, PokemonSnapItemCategory.TRASH_CUSTOM),

    (SIMPLE_TRASH_ITEM_NAME, 4100, PokemonSnapItemCategory.TRASH_SIMPLE),

]] + pokemon_pics + sign_pics + [pic for pics in trash_pokemon_pics.values() for pic in pics]

filler_item_names = [item.name for item in _all_items if item.category is PokemonSnapItemCategory.TRASH_CUSTOM]

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def build_required_item_pool(world: "PokemonSnapWorld") -> list[PokemonSnapItemData]:
    item_pool = []

    item_pool.extend(item for item in _all_items if item.name in [DASH_ENGINE, SIGN_DETECTOR, L_TO_STOP])

    pokemon_pic_count = len(ALL_INGAME_POKEMON)
    sign_pic_count = len(ALL_SIGNS)
    if world.options.goal_type == GoalType.option_pokemon_pictures:
        pokemon_pic_count += world.options.extra_pokemon_pictures.value
    elif world.options.goal_type == GoalType.option_signs:
        sign_pic_count += world.options.extra_sign_pictures.value

    if world.options.goal_item_names == GoalItemNamingScheme.option_specific:
        extra_pokemon_pics = pokemon_pics[:]
        extra_sign_pics = sign_pics[:]
        world.random.shuffle(extra_pokemon_pics)
        world.random.shuffle(extra_sign_pics)
        item_pool.extend((pokemon_pics + extra_pokemon_pics)[:pokemon_pic_count])
        item_pool.extend((sign_pics + extra_sign_pics)[:sign_pic_count])
    else:
        item_pool.extend([item_dictionary[POKEMON_PIC_NAME]] * pokemon_pic_count)
        item_pool.extend([item_dictionary[SIGN_PIC_NAME]]    * sign_pic_count)

    pokemon_food_choice = APPLE if (world.options.pokemon_food_name == AppleNamingScheme.option_apples) else POKEMON_FOOD
    if world.options.per_course_items:
        item_pool.extend(item_dictionary[course(name, c)] for name, c in product([pokemon_food_choice, PESTER_BALL, POKEFLUTE], ALL_LEVELS))
    else:
        item_pool.extend(item for item in _all_items if item.name in [pokemon_food_choice, PESTER_BALL, POKEFLUTE])

    if world.options.map_fragments.value == 1:
        item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.AREA and item.name != world.start_area.name)
    else:
        for item in _all_items:
            if item.category is PokemonSnapItemCategory.MAP_FRAGMENT and item.name != fragment(world.start_area.name):
                item_pool.extend([item] * world.options.map_fragments.value)

    film_upgrade_count = (
        ceil((world.options.maximum_film - world.options.starting_film) / world.options.film_upgrade_amount) +
        world.options.extra_film_upgrades
    )
    item_pool.extend([item_dictionary[FILM_UPGRADE]] * film_upgrade_count)

    # Remove items depending on options
    if world.options.start_with_dash_engine: item_pool.remove(item_dictionary[DASH_ENGINE])
    if not world.options.pokemon_signs:      item_pool.remove(item_dictionary[SIGN_DETECTOR])
    if world.options.left_bumper_to_start_stop != PressLToStop.option_in_item_pool:
        item_pool.remove(item_dictionary[L_TO_STOP])

    if world.options.photo_scoring == PhotoScoring.option_separate_unlocks:
        count = world.options.extra_photo_scoring_items.value + 1
        item_pool.extend([item_dictionary[WDFL_SCORING], item_dictionary[MULT_SCORING]] * count)
    elif world.options.photo_scoring == PhotoScoring.option_progressive_unlocks:
        count = world.options.extra_photo_scoring_items.value + 2
        item_pool.extend([item_dictionary[PROG_SCORING]] * count)

    return item_pool

def build_item_pool(world: "PokemonSnapWorld") -> list[PokemonSnapItemData]:
    item_pool = build_required_item_pool(world)

    def unfilled_count():
        return len(world.multiworld.get_unfilled_locations(world.player)) - len(item_pool)

    if world.options.filler_item_names == FillerItemNamingScheme.option_flavorful:
        ## Fill with one of each custom trash item, then one of each trash pokemon pic, then random pokemon pics
        trash_items = [item for item in _all_items if item.category is PokemonSnapItemCategory.TRASH_CUSTOM]

        trash_pics = list(trash_pokemon_pics.values())
        while len(trash_items) < unfilled_count():
            for pictures in trash_pics:
                trash_items.append(world.random.choice(pictures))
            world.random.shuffle(trash_pics)
        item_pool.extend(trash_items[:unfilled_count()])
    else:
        item_pool.extend([item_dictionary[SIMPLE_TRASH_ITEM_NAME]] * unfilled_count())

    return item_pool


item_name_groups: typing.Dict[str, typing.Set[str]] = {}
for item in _all_items:
    category = f"{item.category}"
    if category not in item_name_groups.keys():
        item_name_groups[category] = set()
    item_name_groups[category].add(item.name)


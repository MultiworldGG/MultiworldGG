import logging
from random import Random
from typing import TYPE_CHECKING, Dict, Set

from BaseClasses import Item, ItemClassification
from .data import data
from .options import Shopsanity, ItemPoolFill, ShopsanityXItems, FreeFlyLocation

if TYPE_CHECKING:
    from .world import PokemonCrystalWorld


class PokemonCrystalItem(Item):
    game: str = data.manifest.game
    tags: frozenset[str]
    flag_index: int | None

    def __init__(self,
                 name: str,
                 classification: ItemClassification,
                 code: int | None,
                 player: int,
                 flag_index: int | None = None) -> None:

        super().__init__(name, classification, code, player)

        self.flag_index = flag_index

        if code is None:
            self.tags = frozenset(["Event"])
        else:
            item = data.items[code]
            self.tags = item.tags


class PokemonCrystalGlitchedToken(Item):
    game: str = data.manifest.game
    TOKEN_NAME = "GLITCHED_TOKEN"

    def __init__(self, player) -> None:
        super().__init__(name=self.TOKEN_NAME, classification=ItemClassification.progression, code=None, player=player)


def create_item_label_to_code_map() -> dict[str, int]:
    """
    Creates a map from item labels to their AP item id (code)
    """
    return {attributes.label: item_value for item_value, attributes in data.items.items() if
            "INVALID" not in attributes.tags}


CONST_NAME_TO_ID = {item_data.item_const: item_id for item_id, item_data in data.items.items()}
CONST_NAME_TO_LABEL = {item_data.item_const: item_data.label for item_data in data.items.values()}


def item_const_name_to_id(const_name) -> int:
    return CONST_NAME_TO_ID.get(const_name, 0)


def item_const_name_to_label(const_name):
    return CONST_NAME_TO_LABEL.get(const_name, "Poke Ball")


def get_random_filler_item(world: "PokemonCrystalWorld") -> str:
    option = world.options.item_pool_fill
    if not hasattr(option, "weighted_pool"):
        if option == ItemPoolFill.option_balanced:
            option.weighted_pool = [["RARE_CANDY", "ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY",
                                     "WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE",
                                     "MOON_STONE", "ESCAPE_ROPE", "NUGGET", "STAR_PIECE", "STARDUST", "PEARL",
                                     "BIG_PEARL", "POKE_BALL", "GREAT_BALL", "ULTRA_BALL", "POTION", "SUPER_POTION",
                                     "ENERGY_ROOT", "ENERGYPOWDER", "HYPER_POTION", "FULL_RESTORE", "REPEL",
                                     "SUPER_REPEL", "MAX_REPEL", "REVIVE", "REVIVAL_HERB", "MAX_REVIVE", "HP_UP",
                                     "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON", "GUARD_SPEC", "DIRE_HIT",
                                     "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL", "HEAL_POWDER", "BURN_HEAL",
                                     "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING", "FULL_HEAL"]]
        elif option == ItemPoolFill.option_youngster:
            option.weighted_pool = [["RARE_CANDY", "ESCAPE_ROPE"] * 11,
                                    ["ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 9,
                                    ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE",
                                     "MOON_STONE"] * 2,
                                    ["GREAT_BALL"] * 1, ["POTION", "POKE_BALL", "REPEL"] * 12,
                                    ["SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER", "SUPER_REPEL"] * 2,
                                    ["HYPER_POTION", "FULL_RESTORE"] * 1, ["MAX_REPEL"] * 1,
                                    ["REVIVE", "REVIVAL_HERB"] * 5 + ["MAX_REVIVE"] * 1,
                                    ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 1,
                                    ["HEAL_POWDER", "BURN_HEAL", "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING",
                                     "FULL_HEAL"] * 2]
        elif option == ItemPoolFill.option_cooltrainer:
            option.weighted_pool = [["RARE_CANDY", "ESCAPE_ROPE"] * 11,
                                    ["MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 9,
                                    ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE",
                                     "MOON_STONE"] * 5,
                                    ["SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER", "SUPER_REPEL", "FULL_HEAL"] * 1,
                                    ["NUGGET", "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL"] * 5,
                                    ["GUARD_SPEC", "DIRE_HIT", "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL"] * 10,
                                    ["HYPER_POTION", "FULL_RESTORE", "MAX_REPEL"] * 10,
                                    ["REVIVE", "REVIVAL_HERB"] * 5 + ["MAX_REVIVE"] * 10,
                                    ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 10,
                                    ["TWISTEDSPOON", "MYSTIC_WATER", "LEFTOVERS", "CHARCOAL", "BRIGHTPOWDER", "MAGNET",
                                     "SCOPE_LENS", "DRAGON_FANG", "NEVERMELTICE", "SMOKE_BALL"] * 2]
        elif option == ItemPoolFill.option_vanilla:
            # weights are roughly based on vanilla occurrence
            option.weighted_pool = [["RARE_CANDY"] * 3,
                                    ["ETHER", "ELIXER", "MAX_ETHER", "MAX_ELIXER", "MYSTERYBERRY"] * 5,
                                    ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE",
                                     "MOON_STONE"] * 2,
                                    ["ESCAPE_ROPE"] * 3,
                                    ["NUGGET", "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL"] * 2,
                                    ["POKE_BALL", "GREAT_BALL", "ULTRA_BALL"] * 5,
                                    ["POTION", "SUPER_POTION", "ENERGY_ROOT", "ENERGYPOWDER"] * 12,
                                    ["HYPER_POTION", "FULL_RESTORE"] * 2, ["REPEL", "SUPER_REPEL", "MAX_REPEL"] * 3,
                                    ["REVIVE", "REVIVAL_HERB"] * 4 + ["MAX_REVIVE"] * 2,
                                    ["HP_UP", "PP_UP", "PROTEIN", "CARBOS", "CALCIUM", "IRON"] * 5,
                                    ["GUARD_SPEC", "DIRE_HIT", "X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL"] * 2,
                                    ["HEAL_POWDER", "BURN_HEAL", "PARLYZ_HEAL", "ICE_HEAL", "ANTIDOTE", "AWAKENING",
                                     "FULL_HEAL"] * 5]
        elif option == ItemPoolFill.option_shuckle:
            option.weighted_pool = [
                ["WATER_STONE", "FIRE_STONE", "THUNDERSTONE", "LEAF_STONE", "SUN_STONE", "MOON_STONE"] * 2,
                ["ESCAPE_ROPE"] * 3, ["NUGGET", "STAR_PIECE", "STARDUST", "PEARL", "BIG_PEARL"] * 2,
                ["PSNCUREBERRY", "PRZCUREBERRY", "BURNT_BERRY", "ICE_BERRY", "BITTER_BERRY", "MINT_BERRY"] * 5,
                ["MIRACLEBERRY", "BERRY_JUICE", "MYSTERYBERRY", "BERRY"] * 5, ["POKE_BALL"] * 2]
        else:
            # oops :)
            option.weighted_pool = [["NUGGET"] * 100]
    group = world.random.choice(option.weighted_pool)
    return world.random.choice(group)


def get_random_ball(random: Random):
    balls = ("POKE_BALL", "GREAT_BALL", "ULTRA_BALL", "FRIEND_BALL", "HEAVY_BALL", "LOVE_BALL", "LEVEL_BALL",
             "LURE_BALL", "FAST_BALL")
    ball_weights = (50, 30, 20, 1, 1, 1, 1, 1, 1)
    return random.choices(balls, weights=ball_weights)[0]


def adjust_item_classifications(world: "PokemonCrystalWorld"):
    all_items = world.itempool + world.pre_fill_items + world.multiworld.precollected_items[world.player]

    if Shopsanity.blue_card not in world.options.shopsanity.value:
        for item in all_items:
            if item.name == "Blue Card":
                item.classification = ItemClassification.useful

    if Shopsanity.apricorns not in world.options.shopsanity.value:
        for item in all_items:
            if "Apricorn" in item.tags:
                item.classification = ItemClassification.filler

    if not world.options.require_itemfinder:
        for item in all_items:
            if item.name == "Itemfinder":
                item.classification = ItemClassification.useful

    if world.options.free_fly_location < FreeFlyLocation.option_free_fly_and_map_card:
        for item in all_items:
            if item.name == "Map Card":
                item.classification = ItemClassification.useful

    if not world.options.randomize_phone_call_items:
        for item in all_items:
            if item.name == "Phone Card":
                item.classification = ItemClassification.useful

    if world.options.johto_only:
        for item in all_items:
            if item.name == "Radio Card":
                item.classification = ItemClassification.useful

    if (world.options.johto_only and not world.options.randomize_phone_call_items
            and world.options.free_fly_location < FreeFlyLocation.option_free_fly_and_map_card):
        for item in all_items:
            if item.name == "Pokegear":
                item.classification = ItemClassification.useful

    if world.options.johto_only and not world.options.national_park_access:
        for item in all_items:
            if item.name == "Bicycle":
                item.classification = ItemClassification.useful


def place_x_items(world: "PokemonCrystalWorld") -> list[str]:
    if world.options.shopsanity_x_items != ShopsanityXItems.option_any_shop: return []

    exclude_shops = ("REGION_MART_BLUE_CARD", "REGION_MART_GOLDENROD_GAME_CORNER",
                     "REGION_MART_CELADON_GAME_CORNER_PRIZE_ROOM", "REGION_MART_KURTS_BALLS")
    shop_locations = [loc for loc in world.get_locations() if
                      "shopsanity" in loc.tags and loc.parent_region.name not in exclude_shops and not loc.item]

    if not shop_locations: return []
    world.random.shuffle(shop_locations)

    x_items = ["X_ATTACK", "X_DEFEND", "X_SPEED", "X_SPECIAL", "X_ACCURACY", "DIRE_HIT", "GUARD_SPEC"]

    placed_x_items = []

    while x_items and shop_locations:
        loc = shop_locations.pop(0)
        x_item_const = x_items.pop(0)
        x_item = world.create_item_by_const_name(x_item_const)

        loc.place_locked_item(x_item)
        placed_x_items.append(x_item.name)

    return placed_x_items


def randomize_item_values(world: "PokemonCrystalWorld"):
    if not world.options.randomize_item_values: return

    min_item_value = world.options.minimum_item_value
    max_item_value = world.options.maximum_item_value
    if world.options.minimum_item_value > world.options.maximum_item_value:
        logging.info("Pokemon Crystal: Minimum Item Value for player %s (%s)"
                     " is greater than Maximum Item Value.",
                     world.player, world.player_name)
        min_item_value = world.options.maximum_item_value.value
        max_item_value = world.options.minimum_item_value.value

    world.generated_item_values = {code: world.random.randint(min_item_value, max_item_value) for code in
                                   sorted(world.generated_item_values.keys())}


ITEM_GROUPS: Dict[str, Set[str]] = {}

excluded_item_tags = ("INVALID", "Tracker", "Fly", "Badge", "HM", "Trap", "JohtoBadge", "KantoBadge", "TM", "Rod",
                      "Apricorn", "KeyItem", "Ball", "CustomShop")

for item in data.items.values():
    for tag in item.tags:
        if tag in excluded_item_tags:
            continue
        if tag not in ITEM_GROUPS:
            ITEM_GROUPS[tag] = set()
        ITEM_GROUPS[tag].add(item.label)

EXTENDED_TRAPLINK_MAPPING = {
    "Literature Trap": item_const_name_to_id("PHONE_TRAP"),
    "Exposition Trap": item_const_name_to_id("PHONE_TRAP"),
    "Frozen Trap": item_const_name_to_id("FRZ_TRAP"),
    "Fire Trap": item_const_name_to_id("BRN_TRAP"),
    "Electrocution Trap": item_const_name_to_id("PAR_TRAP"),
    "Cutscene Trap": item_const_name_to_id("PHONE_TRAP"),
    "Paralyze Trap": item_const_name_to_id("PAR_TRAP"),
    "Slow Trap": item_const_name_to_id("SANDSTORM_TRAP"),
    "Slowness Trap": item_const_name_to_id("SANDSTORM_TRAP"),
    "Stun Trap": item_const_name_to_id("PAR_TRAP"),
    "Ice Floor Trap": item_const_name_to_id("ICE_TRAP"),
    "Text Trap": item_const_name_to_id("PHONE_TRAP"),
    "Frost Trap": item_const_name_to_id("FRZ_TRAP"),
    "Slip Trap": item_const_name_to_id("ICE_TRAP"),
    "Instant Death Trap": item_const_name_to_id("EXPLOSION_TRAP"),
    "Spam Trap": item_const_name_to_id("PHONE_TRAP"),
}

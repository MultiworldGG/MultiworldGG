from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, Toggle, OptionSet, Visibility, Choice


class starting_pairs(Range):
    """number of pairs you start unlocked"""
    display_name = "Pairs Unlocked"
    range_start = 1
    range_end = 24
    default = 1


class starting_girls(Range):
    """number of girls you start unlocked Note will prioritise fulfilling the amount of starting pairs so may be higher then set"""
    display_name = "Girls Unlocked"
    range_start = 2
    range_end = 12
    default = 3


class starting_seed_blue(Range):
    """number of blue note seeds given at start"""
    display_name = "starting blue note seeds"
    range_start = 0
    range_end = 999
    default = 25


class starting_seed_green(Range):
    """number of green star seeds given at start"""
    display_name = "starting green star seeds"
    range_start = 0
    range_end = 999
    default = 25


class starting_seed_orange(Range):
    """number of orange moon seeds given at start"""
    display_name = "starting orange moon seeds"
    range_start = 0
    range_end = 999
    default = 25


class starting_seed_red(Range):
    """number of red flame seeds given at start"""
    display_name = "starting red flame seeds"
    range_start = 0
    range_end = 999
    default = 25

class shop_items(Range):
    """number of archipelago items in the shop Note if there is not enough locations for items it will add shop locations to satisfy the locations needed, MAX is 494 so total locations isn't over 1000"""
    display_name = "shop items"
    range_start = 0
    range_end = 494
    default = 0

class exclude_shop_items(Range):
    """shop items after the number set will be excluded from having progression items in them. will do nothing if set higher than the number of shop items, 
    NOTE will cause world generation to fail if number is set too low as there will be not enough location slots for progression items"""
    display_name = "shop location exclude start"
    range_start = 0
    range_end = 495
    default = 20

class hide_shop_item_details(Toggle):
    """hide shop item id and item progression category"""
    display_name = "hide shop item details"
    default = False

class enable_question_locations(Toggle):
    """enable having items locked behind asking girls their favourite stuff Note if there is not enough locations for items it will add shop locations to satisfy the locations needed"""
    display_name = "fav questions have items"
    default = True

class disable_outfits(Toggle):
    """disable having outfits as locations/items"""
    display_name = "outfits disabled"
    default = False

class disable_baggage(Toggle):
    """disable baggage completely"""
    display_name = "disable baggage"
    default = False

class lovers_instead_wings(Toggle):
    """require player to get all available pairs to lovers instead of collecting wings"""
    display_name = "lovers instead of wings"
    default = False

class enabled_girls(OptionSet):
    """girls enabled to be accessed"""
    display_name = "enabled girls"
    valid_keys = [
        "lola",
        "jessie",
        "lillian",
        "zoey",
        "sarah",
        "lailani",
        "candace",
        "nora",
        "brooke",
        "ashley",
        "abia",
        "polly"
    ]
    default = valid_keys.copy()

class randomise_girl_token(Toggle):
    """randomise tokens girls like/dislike"""
    display_name = "randomise girl token"
    default = True

class randomise_girl_baggage(Toggle):
    """randomise girls baggage"""
    display_name = "randomise girl baggage"
    default = False

class randomise_girl_gifts(Toggle):
    """randomise unique/shoe gifts for each girl"""
    display_name = "randomise girl gifts"
    default = False

class puzzle_goal_start(Range):
    """Starting affection goal for date puzzles"""
    display_name = "goal start"
    range_start = 1
    range_end = 9999
    default = 200

class puzzle_goal_add(Range):
    """affection added to the starting goal based on how many pairs you have taken on dates"""
    display_name = "goal addition"
    range_start = 1
    range_end = 999
    default = 25

class puzzle_goal_boss(Range):
    """affection goal for boss puzzles"""
    display_name = "goal boss"
    range_start = 1
    range_end = 9999
    default = 5000

class puzzle_moves(Range):
    """moves you start a puzzle with (EASY MODE=30, NORMAL MODE=25, HARD MODE=20) NOTE: boss fight will start with 4x this number caped at 999"""
    display_name = "puzzle moves"
    range_start = 10
    range_end = 999
    default = 25

class filler_item(Range):
    """how the filler item is handled by making them all either:
    1:nothing items,
    2:random seed item,
    3:random date gift"""
    display_name = "filler item"
    range_start = 1
    range_end = 3
    default = 3

class outfits_require_date_completion(Toggle):
    """require date to be successfully completed before outfit can be unlocked"""
    display_name = "outfit require date completion"
    default = False

class boss_wings_requirement(Range):
    """number of wings required to access the boss
    NOTE: Asking Kyu about the wings will show you the amount of wings needed"""
    display_name = "boss wing requirement"
    range_start = 1
    range_end = 24
    default = 24

class player_gender(Choice):
    """sets the players gender in game"""
    display_name = "player gender"
    option_male = 0
    option_female = 1
    default = 0

class polly_gender(Choice):
    """sets pollys gender in game"""
    display_name = "polly gender"
    option_innie = 0
    option_outie = 1
    default = 0

class game_difficulty(Choice):
    """sets the client game difficulty"""
    display_name = "game client difficulty"
    option_chad = 0
    option_average_guy = 1
    option_incel = 2
    default = 1


@dataclass
class HP2Options(PerGameCommonOptions):
    number_of_starting_girls: starting_girls
    number_of_starting_pairs: starting_pairs
    number_blue_seed: starting_seed_blue
    number_green_seed: starting_seed_green
    number_orange_seed: starting_seed_orange
    number_red_seed: starting_seed_red
    number_shop_items: shop_items
    enable_questions: enable_question_locations
    disable_baggage: disable_baggage
    enabled_girls: enabled_girls
    randomise_girl_token:randomise_girl_token
    randomise_girl_baggage:randomise_girl_baggage
    randomise_girl_gifts:randomise_girl_gifts
    lovers_instead_wings: lovers_instead_wings
    puzzle_goal_start: puzzle_goal_start
    puzzle_goal_add: puzzle_goal_add
    puzzle_goal_boss: puzzle_goal_boss
    disable_outfits: disable_outfits
    puzzle_moves: puzzle_moves
    filler_item: filler_item
    exclude_shop_items: exclude_shop_items
    hide_shop_item_details: hide_shop_item_details
    outfits_require_date_completion: outfits_require_date_completion
    boss_wings_requirement: boss_wings_requirement
    player_gender:player_gender
    polly_gender:polly_gender
    game_difficulty:game_difficulty
from dataclasses import dataclass

from Options import PerGameCommonOptions, Range, OptionSet, Toggle, Choice
from worlds.huniepop.CustomOption import DictRange
from worlds.huniepop.Data import gift_ids


class enabled_girls(OptionSet):
    """girls enabled to be accessed NOTE if goal is to give in panties kyu will be enabled no matter this setting"""
    display_name = "enabled girls"
    valid_keys = [
        "tiffany",
        "aiko",
        "kyanna",
        "audrey",
        "lola",
        "nikki",
        "jessie",
        "beli",
        "kyu",
        "momo",
        "celeste",
        "venus"
    ]
    default = valid_keys.copy()

class goal(Choice):
    """set the goal
    panties: give kyu all available girls panties
    sex: have sex with all available girls"""
    display_name = "goal"
    option_sex = 0
    option_panties = 1
    default = 1

class starting_girls(Range):
    """number of girls you start unlocked"""
    display_name = "Girls Unlocked"
    range_start = 2
    range_end = 12
    default = 3

#class randomize_girl_gifts(Toggle):
#    """randomize the gifts each girl wants"""
#    display_name = "Girls Gifts"
#    default = True
class randomize_girl_gifts(Choice):
    """randomize the gifts each girl wants
    vanilla: will make the gifts each girl want the same as vanilla hunie pop
    balanced: will randomize the gifts each girl want while balancing the amount of each gift in the multiworld slot
    full: will randomize the gifts each girl want"""
    display_name = "goal"
    option_vanilla = 0
    option_balanced = 1
    option_full = 2
    default = 2


class randomize_girl_trait(Toggle):
    """randomize the traits each girl likes/hates"""
    display_name = "Girls Traits"
    default = True

class puzzle_moves(Range):
    """number of moves you start the puzzles with"""
    display_name = "puzzle moves"
    range_start = 10
    range_end = 99
    default = 20

class puzzle_affection_base(Range):
    """the base affection you start the puzzles with"""
    display_name = "puzzle affection base"
    range_start = 1
    range_end = 5000
    default = 200

class puzzle_affection_add(Range):
    """affection added to base affection after every successful date capped at 999999"""
    display_name = "puzzle affection add"
    range_start = 10
    range_end = 500
    default = 100

class shop_items(Range):
    """number of archipelago items in the shop Note if there is not enough locations for items it will add shop locations to satisfy the locations needed"""
    display_name = "shop items"
    range_start = 0
    range_end = 500
    default = 0

class exclude_shop_items(Range):
    """shop items after the number set will be excluded from having progression items in them. will do nothing if set higher than the number of shop items,
    NOTE will cause world generation to fail if number is set too low as there will be not enough location slots for progression items"""
    display_name = "shop location exclude start"
    range_start = 0
    range_end = 480
    default = 20

#class shop_item_cost(Range):
#    """the cost of each arch item location in the shop"""
#    display_name = "shop arch item cost"
#    range_start = 100
#    range_end = 50000
#    default = 1000

class shop_item_cost(DictRange):
    """sets the cost for Arch Items in the shop

    <value>,<min>,<max> can be any number between 100 and 50000
    <min> must be smaller than <max>
    Possible options
    "single-<value>" will make all Arch Items cost the same <value>
    "single-random", will make all Arch Items cost the same but get a random value from 100-50000
    "single-random-low", will make all Arch Items cost the same but get a random value from 100-50000 with lower numbers more likely
    "single-random-high",  will make all Arch Items cost the same but get a random value from 100-50000 with higher numbers more likely
    "single-random-range-<min>-<max>", will make all Arch Items cost the same but get a random value from <min>-<max>
    "single-random-range-low-<min>-<max>", will make all Arch Items cost the same but get a random value from <min>-<max> with lower numbers more likely
    "single-random-range-high-<min>-<max>", will make all Arch Items cost the same but get a random value from <min>-<max> with higher numbers more likely

    "random", will make each Arch Item cost a random value from 100-50000
    "random-low", will make each Arch Item cost a random value from 100-50000 with lower numbers more likely
    "random-high",  will make each Arch Item cost a random value from 100-50000 with higher numbers more likely
    "random-range-<min>-<max>", will make each Arch Item cost a random value from <min>-<max>
    "random-range-low-<min>-<max>", will make each Arch Item cost a random value from <min>-<max> with lower numbers more likely
    "random-range-high-<min>-<max>", will make each Arch Item cost a random value from <min>-<max> with higher numbers more likely
    """
    display_name = "shop arch item cost"
    #arch item shop ids
    keys = [f"shop{x+1}" for x in range(500)]
    range_min = 100
    range_max = 50000
    default = "single-1000"

#class shop_gift_cost(Range):
#    """the cost of each gift item in the shop"""
#    display_name = "shop gift item cost"
#    range_start = 100
#    range_end = 50000
#    default = 2500
class shop_gift_cost(DictRange):
    """sets the cost of each gift item in the shop

    <value>,<min>,<max> can be any number between 100 and 50000
    <min> must be smaller than <max>
    Possible options
    "single-<value>" will make all gift items cost the same <value>
    "single-random", will make all gift items cost the same but get a random value from 100-50000
    "single-random-low", will make all gift items cost the same but get a random value from 100-50000 with lower numbers more likely
    "single-random-high",  will make all gift items cost the same but get a random value from 100-50000 with higher numbers more likely
    "single-random-range-<min>-<max>", will make all gift items cost the same but get a random value from <min>-<max>
    "single-random-range-low-<min>-<max>", will make all gift items cost the same but get a random value from <min>-<max> with lower numbers more likely
    "single-random-range-high-<min>-<max>", will make all gift items cost the same but get a random value from <min>-<max> with higher numbers more likely

    "random", will make each gift item cost a random value from 100-50000
    "random-low", will make each gift item cost a random value from 100-50000 with lower numbers more likely
    "random-high",  will make each gift item cost a random value from 100-50000 with higher numbers more likely
    "random-range-<min>-<max>", will make each gift item cost a random value from <min>-<max>
    "random-range-low-<min>-<max>", will make each gift item cost a random value from <min>-<max> with lower numbers more likely
    "random-range-high-<min>-<max>", will make each gift item cost a random value from <min>-<max> with higher numbers more likely
    """
    display_name = "shop gift item cost"
    #girl gift ids
    keys = [*gift_ids]
    range_min = 100
    range_max = 50000
    default = "single-2500"


#class shop_date_gift_cost(Range):
#    """the cost of each date gift item in the shop"""
#    display_name = "shop date gift item cost"
#    range_start = 100
#    range_end = 50000
#    default = 500

class shop_date_gift_cost(DictRange):
    """sets the cost of each date gift item in the shop

    <value>,<min>,<max> can be any number between 100 and 50000
    <min> must be smaller than <max>
    Possible options
    "single-<value>" will make all date gifts cost the same <value>
    "single-random", will make all date gifts cost the same but get a random value from 100-50000
    "single-random-low", will make all date gifts cost the same but get a random value from 100-50000 with lower numbers more likely
    "single-random-high",  will make all date gifts cost the same but get a random value from 100-50000 with higher numbers more likely
    "single-random-range-<min>-<max>", will make all date gifts cost the same but get a random value from <min>-<max>
    "single-random-range-low-<min>-<max>", will make all date gifts cost the same but get a random value from <min>-<max> with lower numbers more likely
    "single-random-range-high-<min>-<max>", will make all date gifts cost the same but get a random value from <min>-<max> with higher numbers more likely

    "random", will make each date gift cost a random value from 100-50000
    "random-low", will make each date gift cost a random value from 100-50000 with lower numbers more likely
    "random-high",  will make each date gift cost a random value from 100-50000 with higher numbers more likely
    "random-range-<min>-<max>", will make each date gift cost a random value from <min>-<max>
    "random-range-low-<min>-<max>", will make each date gift cost a random value from <min>-<max> with lower numbers more likely
    "random-range-high-<min>-<max>", will make each date gift cost a random value from <min>-<max> with higher numbers more likely
    """
    display_name = "shop date gift item cost"
    #date gift ids
    keys = [121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156,]
    range_min = 100
    range_max = 50000
    default = "single-500"

#class hunie_gift_cost(Range):
#    """the cost of each gift item when buying using hunie"""
#    display_name = "hunie item cost"
#    range_start = 1000
#    range_end = 99999
#    default = 10000
class hunie_gift_cost(DictRange):
    """sets the cost of each gift item when buying using hunie

    <value>,<min>,<max> can be any number between 1000 and 99999
    <min> must be smaller than <max>
    Possible options
    "single-<value>" will make all gift items cost the same <value>
    "single-random", will make all gift items cost the same but get a random value from 1000-99999
    "single-random-low", will make all gift items cost the same but get a random value from 1000-99999 with lower numbers more likely
    "single-random-high",  will make all gift items cost the same but get a random value from 1000-99999 with higher numbers more likely
    "single-random-range-<min>-<max>", will make all gift items cost the same but get a random value from <min>-<max>
    "single-random-range-low-<min>-<max>", will make all gift items cost the same but get a random value from <min>-<max> with lower numbers more likely
    "single-random-range-high-<min>-<max>", will make all gift items cost the same but get a random value from <min>-<max> with higher numbers more likely

    "random", will make each gift item cost a random value from 1000-99999
    "random-low", will make each gift item cost a random value from 1000-99999 with lower numbers more likely
    "random-high",  will make each gift item cost a random value from 1000-99999 with higher numbers more likely
    "random-range-<min>-<max>", will make each gift item cost a random value from <min>-<max>
    "random-range-low-<min>-<max>", will make each gift item cost a random value from <min>-<max> with lower numbers more likely
    "random-range-high-<min>-<max>", will make each gift item cost a random value from <min>-<max> with higher numbers more likely
    """
    display_name = "hunie item cost"
    #girl gift ids
    keys = [*gift_ids]
    range_min = 1000
    range_max = 99999
    default = "single-10000"


class filler_item(Choice):
    """how the filler item is handled by making them all either:
    nothing: "nothing" items,
    filler: random non progression items (date gifts, food, drink) + "nothing" items"""
    display_name = "filler item"
    option_nothing = 0
    option_filler = 1
    default = 1

class deathlink(Choice):
    """enables/disables deathlink

    "disable": disable deathlink
    "send": send deathlink on date fails but don't receive deaths
    "limited": send deathlink on date fails and receive deaths but do nothing if death is received outside a date
    "full": send deathlink on date fails and receive deaths, if death is received outside a date it will wait until you are in a date then kill you
    """
    display_name = "deathlink"
    option_disable = 0
    option_send = 1
    option_limited = 2
    option_full = 3
    default = 0


@dataclass
class HPOptions(PerGameCommonOptions):
    enabled_girls: enabled_girls
    number_of_starting_girls: starting_girls
    randomize_girl_gifts:randomize_girl_gifts
    randomize_girl_trait:randomize_girl_trait
    number_shop_items: shop_items
    exclude_shop_items: exclude_shop_items
    shop_item_cost: shop_item_cost
    shop_gift_cost: shop_gift_cost
    shop_date_gift_cost: shop_date_gift_cost
    hunie_gift_cost: hunie_gift_cost
    puzzle_moves: puzzle_moves
    puzzle_affection_base: puzzle_affection_base
    puzzle_affection_add: puzzle_affection_add
    filler_item:filler_item
    goal: goal
    deathlink:deathlink

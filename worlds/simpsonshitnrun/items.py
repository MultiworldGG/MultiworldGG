from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from BaseClasses import Item, ItemClassification
import re

from . import rules
from Options import OptionSet

if TYPE_CHECKING:
    from .world import SimpsonsHitNRunWorld

@dataclass
class ItemDef:
    # Item info
    id: int
    type: ItemClassification
    # Info needed if the item is a car
    is_car: bool = False
    level: list[int] = field(default_factory=list)
    size: str = ""
    internal_id: str = ""
    # Added to make creating items easier
    always_exists: bool = True

ITEM_DEFS = {
    "Homer - Casual": ItemDef(121789, ItemClassification.filler),
    "Homer - Muumuu": ItemDef(121790, ItemClassification.filler),
    "Homer - Chosen One": ItemDef(121791, ItemClassification.filler),
    "Bart - Tall": ItemDef(121792, ItemClassification.filler),
    "Bart - Football": ItemDef(121793, ItemClassification.filler),
    "Bart - Ninja": ItemDef(121794, ItemClassification.filler),
    "Lisa - Cool": ItemDef(121795, ItemClassification.progression),
    "Lisa - Floreda": ItemDef(121796, ItemClassification.filler),
    "Lisa - Hockey": ItemDef(121797, ItemClassification.filler),
    "Marge - Classy": ItemDef(121798, ItemClassification.filler),
    "Marge - Inmate": ItemDef(121799, ItemClassification.progression),
    "Marge - Police": ItemDef(121800, ItemClassification.progression),
    "Apu - American": ItemDef(121801, ItemClassification.progression),
    "Apu - Army": ItemDef(121802, ItemClassification.filler),
    "Apu - B-sharps": ItemDef(121803, ItemClassification.filler),
    "Bart - Hugo": ItemDef(121804, ItemClassification.filler),
    "Bart - Cadet": ItemDef(121805, ItemClassification.filler),
    "Bart - Bartman": ItemDef(121806, ItemClassification.filler),
    "Homer - Dirty": ItemDef(121807, ItemClassification.filler),
    "Homer - Evil": ItemDef(121808, ItemClassification.filler),
    "Homer - Donut": ItemDef(121809, ItemClassification.filler),

    "Family Sedan": ItemDef(121810, ItemClassification.progression_skip_balancing, True, [1], "Small", "famil_v"),
    "Plow King": ItemDef(121811, ItemClassification.progression, True, [1], "Large", "plowk_v"),
    "Duff Truck": ItemDef(121812, ItemClassification.progression_skip_balancing, True, [1], "Large", "cDuff"),
    "Surveillance Van": ItemDef(121813, ItemClassification.progression_skip_balancing, True, [1], "Medium", "cVan"),
    "Pickup Truck": ItemDef(121814, ItemClassification.progression_skip_balancing, True, [1], "Medium", "cletu_v"),
    "Electaurus": ItemDef(121815, ItemClassification.progression_skip_balancing, True, [1], "Small", "elect_v"),

    "Mr. Plow": ItemDef(121816, ItemClassification.progression, True, [2], "Medium", "mrplo_v"),
    "Limo": ItemDef(121817, ItemClassification.progression_skip_balancing, True, [2], "Small", "cLimo"),
    "Fire Truck": ItemDef(121818, ItemClassification.progression_skip_balancing, True, [2], "Large", "cFire_v"),
    "WWII Vehicle": ItemDef(121819, ItemClassification.progression_skip_balancing, True, [2], "Medium", "gramp_v"),
    "Moe's Sedan": ItemDef(121820, ItemClassification.progression_skip_balancing, True, [2], "Small", "moe_v"),

    "School Bus": ItemDef(121821, ItemClassification.progression, True, [3], "Large", "otto_v"),
    "Donut Truck": ItemDef(121822, ItemClassification.progression_skip_balancing, True, [3], "Medium", "cDonut"),
    "Nerd Car": ItemDef(121823, ItemClassification.progression_skip_balancing, True, [3], "Small", "cNerd"),
    "Skinner's Sedan": ItemDef(121824, ItemClassification.progression_skip_balancing, True, [3], "Medium", "skinn_v"),
    "Book Burning Van": ItemDef(121825, ItemClassification.progression_skip_balancing, True, [3], "Medium", "bookb_v"),

    "Tractor": ItemDef(121826, ItemClassification.progression_skip_balancing, True, [4], "Medium", "willi_v"),
    "Curator": ItemDef(121827, ItemClassification.progression_skip_balancing, True, [4], "Small", "cCurator"),
    "Krusty's Limo": ItemDef(121828, ItemClassification.progression_skip_balancing, True, [4], "Small", "cKlimo"),
    "Kremlin": ItemDef(121829, ItemClassification.progression_skip_balancing, True, [4], "Small", "comic_v"),
    "Clown Car": ItemDef(121830, ItemClassification.progression_skip_balancing, True, [4], "Small", "krust_v"),

    "Car Built For Homer": ItemDef(121831, ItemClassification.progression, True, [5], "Small", "carhom_v"),
    "Cola Truck": ItemDef(121832, ItemClassification.progression_skip_balancing, True, [5], "Large", "cCola"),
    "Police Car": ItemDef(121833, ItemClassification.progression_skip_balancing, True, [5], "Small", "wiggu_v"),
    "Hover Car": ItemDef(121834, ItemClassification.progression_skip_balancing, True, [5], "Small", "frink_v"),
    "El Carro Loco": ItemDef(121835, ItemClassification.progression_skip_balancing, True, [5], "Small", "bbman_v"),

    "Globex Super Villain Car": ItemDef(121836, ItemClassification.progression, True, [6], "Small", "scorp_v"),
    "Armored Truck": ItemDef(121837, ItemClassification.progression_skip_balancing, True, [6], "Large", "cArmor"),
    "Chase Sedan": ItemDef(121838, ItemClassification.progression_skip_balancing, True, [6], "Small", "cSedan"),
    "Bandit": ItemDef(121839, ItemClassification.progression_skip_balancing, True, [6], "Small", "snake_v"),
    "36 Stutz Bearcat": ItemDef(121840, ItemClassification.progression_skip_balancing, True, [6], "Small", "burns_v"),

    "Zombie Car": ItemDef(121841, ItemClassification.progression, True, [7], "Small", "zombi_v"),
    "Hearse": ItemDef(121842, ItemClassification.progression_skip_balancing, True, [7], "Small", "cHears"),
    "Mr. Burns' Limo": ItemDef(121843, ItemClassification.progression_skip_balancing, True, [7], "Medium", "smith_v"),
    "Hover Bike": ItemDef(121844, ItemClassification.progression_skip_balancing, True, [7], "Small", "hbike_v"),
    "Open Wheel Race Car": ItemDef(121845, ItemClassification.progression_skip_balancing, True, [7], "Small", "fone_v"),

    "Honor Roller": ItemDef(121846, ItemClassification.progression_skip_balancing, True, [2], "Small", "honor_v"),
    "Malibu Stacy Car": ItemDef(121847, ItemClassification.progression_skip_balancing, True, [3], "Small", "lisa_v"),
    "Canyonero": ItemDef(121848, ItemClassification.progression_skip_balancing, True, [4], "Medium", "marge_v"),
    "Longhorn": ItemDef(121849, ItemClassification.progression_skip_balancing, True, [5], "Small", "apu_v"),
    "Ferrini - Red": ItemDef(121850, ItemClassification.progression_skip_balancing, True, [6], "Small", "bart_v"),
    "70's Sports Car": ItemDef(121851, ItemClassification.progression_skip_balancing, True, [7], "Small", "homer_v"),

    "Launch": ItemDef(121852, ItemClassification.trap, always_exists=False),
    "Level 1": ItemDef(121853, ItemClassification.progression, always_exists=False),
    "Level 2": ItemDef(121854, ItemClassification.progression, always_exists=False),
    "Level 3": ItemDef(121855, ItemClassification.progression, always_exists=False),
    "Level 4": ItemDef(121856, ItemClassification.progression, always_exists=False),
    "Level 5": ItemDef(121857, ItemClassification.progression, always_exists=False),
    "Level 6": ItemDef(121858, ItemClassification.progression, always_exists=False),
    "Level 7": ItemDef(121859, ItemClassification.progression, always_exists=False),

    "Homer Attack": ItemDef(121860, ItemClassification.progression, always_exists=False),
    "Bart Attack": ItemDef(121861, ItemClassification.progression, always_exists=False),
    "Lisa Attack": ItemDef(121862, ItemClassification.progression, always_exists=False),
    "Marge Attack": ItemDef(121863, ItemClassification.progression, always_exists=False),
    "Apu Attack": ItemDef(121864, ItemClassification.progression, always_exists=False),

    "Homer Progressive Jump": ItemDef(121865, ItemClassification.progression, always_exists=False),
    "Bart Progressive Jump": ItemDef(121866, ItemClassification.progression, always_exists=False),
    "Lisa Progressive Jump": ItemDef(121867, ItemClassification.progression, always_exists=False),
    "Marge Progressive Jump": ItemDef(121868, ItemClassification.progression, always_exists=False),
    "Apu Progressive Jump": ItemDef(121869, ItemClassification.progression, always_exists=False),

    "Homer E-Brake": ItemDef(121870, ItemClassification.progression, always_exists=False),
    "Bart E-Brake": ItemDef(121871, ItemClassification.progression, always_exists=False),
    "Lisa E-Brake": ItemDef(121872, ItemClassification.progression, always_exists=False),
    "Marge E-Brake": ItemDef(121873, ItemClassification.progression, always_exists=False),
    "Apu E-Brake": ItemDef(121874, ItemClassification.progression, always_exists=False),

    "Wrench": ItemDef(121875, ItemClassification.filler),
    "Hit N Run Reset": ItemDef(121876, ItemClassification.filler),
    "10 Coins": ItemDef(121877, ItemClassification.filler),
    "Hit N Run": ItemDef(121878, ItemClassification.trap, always_exists=False),
    "Duff Trap": ItemDef(121879, ItemClassification.trap, always_exists=False),

    "Speed Rocket": ItemDef(121880, ItemClassification.progression_skip_balancing, True, [1], "Small", "rocke_v"),
    "Monorail Car": ItemDef(121881, ItemClassification.progression_skip_balancing, True, [2], "Medium", "mono_v"),
    "Knight Boat": ItemDef(121882, ItemClassification.progression_skip_balancing, True, [3], "Small", "knigh_v"),
    "ATV": ItemDef(121883, ItemClassification.progression_skip_balancing, True, [4], "Small", "atv_v"),
    "Obliteratatron Big Wheel Truck": ItemDef(121884, ItemClassification.progression_skip_balancing, True, [5], "Extra Large", "oblit_v"),
    "Planet Hype 50's Car": ItemDef(121885, ItemClassification.progression_skip_balancing, True, [6], "Small", "hype_v"),
    "R/C Buggy": ItemDef(121886, ItemClassification.progression_skip_balancing, True, [7], "Extra Small", "dune_v"),

    "Progressive Wallet Upgrade": ItemDef(121887, ItemClassification.progression, always_exists=False),
    "Progressive Level": ItemDef(121888, ItemClassification.progression, always_exists=False),

    "Eject": ItemDef(121889, ItemClassification.trap, always_exists=False),

    "Homer Checkered Flag": ItemDef(121890, ItemClassification.progression, always_exists=False),
    "Bart Checkered Flag": ItemDef(121891, ItemClassification.progression, always_exists=False),
    "Lisa Checkered Flag": ItemDef(121892, ItemClassification.progression, always_exists=False),
    "Marge Checkered Flag": ItemDef(121893, ItemClassification.progression, always_exists=False),
    "Apu Checkered Flag": ItemDef(121894, ItemClassification.progression, always_exists=False),

    "Homer Gagfinder": ItemDef(121895, ItemClassification.progression, always_exists=False),
    "Bart Gagfinder": ItemDef(121896, ItemClassification.progression, always_exists=False),
    "Lisa Gagfinder": ItemDef(121897, ItemClassification.progression, always_exists=False),
    "Marge Gagfinder": ItemDef(121898, ItemClassification.progression, always_exists=False),
    "Apu Gagfinder": ItemDef(121899, ItemClassification.progression, always_exists=False),

    "Mini School Bus": ItemDef(121900, ItemClassification.progression_skip_balancing, True, [1], "Large", "schoolbu"),
    "Glass Truck": ItemDef(121901, ItemClassification.progression_skip_balancing, True, [1], "Medium", "glastruc"),
    "Minivan": ItemDef(121902, ItemClassification.progression_skip_balancing, True, [1], "Medium", "minivanA"),
    "Pizza Van": ItemDef(121903, ItemClassification.progression_skip_balancing, True, [2], "Medium", "pizza"),
    "Taxi": ItemDef(121904, ItemClassification.progression_skip_balancing, True, [2], "Small", "taxiA"),
    "Sedan B": ItemDef(121905, ItemClassification.progression_skip_balancing, True, [2], "Small", "sedanB"),
    "Fish Van": ItemDef(121906, ItemClassification.progression_skip_balancing, True, [3], "Medium", "fishtruc"),
    "Garbage Truck": ItemDef(121907, ItemClassification.progression_skip_balancing, True, [4], "Large", "garbage"),
    "Nuclear Waste Truck": ItemDef(121908, ItemClassification.progression_skip_balancing, True, [4], "Medium", "nuctruck"),
    "Pickup": ItemDef(121909, ItemClassification.progression_skip_balancing, True, [1, 3, 6], "Medium", "pickupA"),
    "Sports Car A": ItemDef(121910, ItemClassification.progression_skip_balancing, True, [3], "Small", "sportsA"),
    "Compact Car": ItemDef(121911, ItemClassification.progression_skip_balancing, True, [3, 4, 6], "Small", "compactA"),
    "SUV": ItemDef(121912, ItemClassification.progression_skip_balancing, True, [4, 5], "Small", "SUVA"),
    "Hallo Hearse": ItemDef(121913, ItemClassification.progression_skip_balancing, True, [7], "Small", "hallo"),
    "Coffin Car": ItemDef(121914, ItemClassification.progression_skip_balancing, True, [7], "Small", "coffin"),
    "Ghost Ship": ItemDef(121915, ItemClassification.progression_skip_balancing, True, [7], "Small", "ship"),
    "Witch Broom": ItemDef(121916, ItemClassification.progression_skip_balancing, True, [7], "Small", "witchcar"),
    "Sedan A": ItemDef(121917, ItemClassification.progression_skip_balancing, True, [8], "Small", "sedanA"),
    "Station Wagon": ItemDef(121918, ItemClassification.progression_skip_balancing, True, [8], "Small", "wagonA"),
    "Ice Cream Truck": ItemDef(121919, ItemClassification.progression_skip_balancing, True, [8], "Large", "icecream"),
    "Bonestorm Truck": ItemDef(121920, ItemClassification.progression_skip_balancing, True, [8], "Large", "cBone"),
    "Cell Phone Car": ItemDef(121921, ItemClassification.progression_skip_balancing, True, [8], "Small", f"cCellA"),
    "Milk Truck": ItemDef(121922, ItemClassification.progression_skip_balancing, True, [8], "Large", "cMilk"),
    "Nonuplets Minivan": ItemDef(121923, ItemClassification.progression_skip_balancing, True, [8], "Medium", "cNonup"),
    "Ferrini - Black": ItemDef(121924, ItemClassification.progression_skip_balancing, True, [8], "Small", "cBlbart"),

    "Homer Frink-o-Matic Wasp Bumper": ItemDef(121925, ItemClassification.progression, always_exists=False),
    "Bart Frink-o-Matic Wasp Bumper": ItemDef(121926, ItemClassification.progression, always_exists=False),
    "Lisa Frink-o-Matic Wasp Bumper": ItemDef(121927, ItemClassification.progression, always_exists=False),
    "Marge Frink-o-Matic Wasp Bumper": ItemDef(121928, ItemClassification.progression, always_exists=False),
    "Apu Frink-o-Matic Wasp Bumper": ItemDef(121929, ItemClassification.progression, always_exists=False),

    "Traffic Trap": ItemDef(121930, ItemClassification.trap, always_exists=False),
    "Cube Van": ItemDef(121931, ItemClassification.progression_skip_balancing, True, [8], "Large", "cCube"),
    "WWII Vehicle W\\ Rocket": ItemDef(121932, ItemClassification.progression_skip_balancing, True, [7], "Medium", "gramR_v"),
    "Audi TT": ItemDef(121933, ItemClassification.progression_skip_balancing, True, [8], "Small", "tt"),
    "Vote Quimby Truck": ItemDef(121934, ItemClassification.progression_skip_balancing, True, [5], "Large", "votetruc"),
    "Ambulance": ItemDef(121935, ItemClassification.progression_skip_balancing, True, [5], "Large", "ambul"),
    "Sports Car B": ItemDef(121936, ItemClassification.progression_skip_balancing, True, [2, 5], "Small", "sportsB"),
    "Itchy and Scratchy Movie Truck": ItemDef(121937, ItemClassification.progression, True, [6], "Large", "IStruck"),
    "Burns Armored Truck": ItemDef(121938, ItemClassification.progression_skip_balancing, True, [6], "Large", "burnsarm"),

    "Homer Forward": ItemDef(121939, ItemClassification.progression, always_exists=False),
    "Bart Forward": ItemDef(121940, ItemClassification.progression, always_exists=False),
    "Lisa Forward": ItemDef(121941, ItemClassification.progression, always_exists=False),
    "Marge Forward": ItemDef(121942, ItemClassification.progression, always_exists=False),
    "Apu Forward": ItemDef(121943, ItemClassification.progression, always_exists=False),
}


ITEM_NAME_TO_ID = {name: item.id for name, item in ITEM_DEFS.items()}
DEFAULT_ITEM_CLASSIFICATIONS = {name: item.type for name, item in ITEM_DEFS.items()}

car_name_to_internal_id = {name: item.internal_id for name, item in ITEM_DEFS.items() if item.is_car}

item_name_groups = {
    "Cars": {name for name, item in ITEM_DEFS.items() if item.is_car},
    "Traps": {name for name, item in ITEM_DEFS.items() if item.type == ItemClassification.trap},
    "Progression": {name for name, item in ITEM_DEFS.items() if item.type == ItemClassification.progression or item.type == ItemClassification.progression_skip_balancing},
    **{
        f"{character} Costumes": {
            name for name in ITEM_DEFS
            if f"{character} - " in name
        }
        for character in ["Homer", "Bart", "Lisa", "Marge", "Apu"]
    },
    **{
        f"{character} Unlocks": {
            name for name in ITEM_DEFS
            if name.startswith(character) and f"{character} - " not in name
        }
        for character in ["Homer", "Bart", "Lisa", "Marge", "Apu"]
    },
    "Jumps": {name for name in ITEM_DEFS if "Jump" in name},
    "Attacks": {name for name in ITEM_DEFS if "Attack" in name},
    "Bumpers": {name for name in ITEM_DEFS if "Bumper" in name},
    "Gagfinders": {name for name in ITEM_DEFS if "Gagfinder" in name},
    "Flags": {name for name in ITEM_DEFS if "Flag" in name},
    "E-Brakes": {name for name in ITEM_DEFS if "E-Brake" in name},
    "Forwards": {name for name in ITEM_DEFS if "Forward" in name},
}

class SimpsonsHitNRunItem(Item):
    game = "Simpsons Hit and Run"

def get_random_filler_item_name(world: SimpsonsHitNRunWorld) -> str:
    trap_option_map = {
        "Eject": world.options.Enable_Eject_Traps,
        "Duff Trap": world.options.Enable_Duff_Traps,
        "Launch": world.options.Enable_Launch_Traps,
        "Hit N Run": world.options.Enable_HitNRun_Traps,
        "Traffic Trap": world.options.Enable_Traffic_Traps,
    }

    trap_items = [name for name, item in ITEM_DEFS.items() if item.type == ItemClassification.trap and trap_option_map.get(name, True)]
    filler_items = ["Wrench", "Hit N Run Reset", "10 Coins"]
    if world.random.randint(0, 99) < world.options.Filler_Traps and trap_items:
        return world.random.choice(trap_items)
    else:
        return world.random.choice(filler_items)

def create_item_with_correct_classification(world: SimpsonsHitNRunWorld, name: str, make_prog: bool = False) -> SimpsonsHitNRunItem:
    classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    if make_prog:
        classification = ItemClassification.progression

    return SimpsonsHitNRunItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: SimpsonsHitNRunWorld) -> None:
    characters = ["Homer", "Bart", "Lisa", "Marge", "Apu"]

    def add_per_options(item_name: str, option: OptionSet, itempool: list[Item], count: int = 1, start_count: int = 0, always_add: bool = True):
        # Create the item if and only if the character has it shuffled,
        # optionally add start_count amount to start inventory for things
        # like jump where you may start with 1 and still have 1 in the pool
        if "None" in option:
            shuffled = []
        elif "All" in option:
            shuffled = sorted(characters)
        else:
            shuffled = sorted(option.value)
        unshuffled = [c for c in characters if c not in shuffled]

        for c in shuffled:
            for _ in range(count - start_count):
                itempool.append(world.create_item(f"{c} {item_name}"))
            for _ in range(start_count):
                world.push_precollected(world.create_item(f"{c} {item_name}"))

        for c in unshuffled:
            if always_add:
                for _ in range(count):
                    world.push_precollected(world.create_item(f"{c} {item_name}"))

    # Choose 1 car from each level and make it progression
    for i in range(1, 8):
        cars = [name for name, item in ITEM_DEFS.items() if item.is_car and (i in item.level or 8 in item.level)]
        world.prog_cars.append(world.random.choice(cars))
    # Choose 1 car of each size and make it progression
    for size in ("Small", "Medium", "Large"):
        cars = [name for name, item in ITEM_DEFS.items() if item.is_car and item.size == size]
        world.prog_cars.append(world.random.choice(cars))

    # Now, hopefully prog_cars is a list of cars that altogether will logically reach all checks
    # *and* encourage different cars to be important in different playthroughs

    # Missionlocks
    if not hasattr(world.multiworld, "generation_is_fake"):
        num_locks = int(49 * (world.options.Mission_Locks / 100))
        pattern = re.compile(r'^\(L([1-7])M([1-7])\)\s+.+')
        mission_locked = world.random.sample([loc.name for loc in world.get_locations() if pattern.match(loc.name)], num_locks)
        chosen_cars = world.random.sample(rules.any_car, num_locks)
        for mission, car in zip(mission_locked, chosen_cars):
            world.missionlockdict[mission] = car
            world.prog_cars.append(car)

    itempool: list[Item] = []

    add_per_options("Progressive Jump", world.options.Shuffle_Jump, itempool, 2, world.options.Start_Jump_Level)
    add_per_options("Attack", world.options.Shuffle_Attack, itempool)
    add_per_options("Gagfinder", world.options.Shuffle_Gagfinder, itempool)
    add_per_options("Checkered Flag", world.options.Shuffle_Checkered_Flags, itempool)
    add_per_options("E-Brake", world.options.Shuffle_EBrakes, itempool)
    add_per_options("Forward", world.options.Shuffle_Forward, itempool)
    add_per_options("Frink-o-Matic Wasp Bumper", world.options.Shuffle_Bumpers, itempool, 1, 1 if world.options.Start_With_Bumpers else 0, False)

    if world.options.Shuffle_Levels:
        start_level = world.random.randint(1,7)
        world.push_precollected(world.create_item(f"Level {start_level}"))
        for i in range(1, 8):
            if i != start_level:
                itempool.append(world.create_item(f"Level {i}"))
    else:
        start_level = 1
        world.push_precollected(world.create_item("Progressive Level"))
        for _ in range(6):
            itempool.append(world.create_item("Progressive Level"))

    if world.options.Starting_Car_Shuffle:
        cars = [name for name, item in ITEM_DEFS.items() if item.is_car and (start_level in item.level or 8 in item.level)]
        start_car = world.create_item(world.random.choice(cars), True)
        world.push_precollected(start_car)
    else:
        start_cars = ["Family Sedan", "Honor Roller", "Malibu Stacy Car", "Canyonero", "Longhorn", "Ferrini - Red", "70's Sports Car"]
        start_car = world.create_item(start_cars[start_level - 1], True)
        world.push_precollected(start_car)

    for i in range(1, 8):
        if i <= world.options.Start_Wallet_Level:
            world.push_precollected(world.create_item("Progressive Wallet Upgrade"))
        else:
            itempool.append(world.create_item("Progressive Wallet Upgrade"))

    trap_option_map = {
        "Eject": world.options.Enable_Eject_Traps,
        "Duff Trap": world.options.Enable_Duff_Traps,
        "Launch": world.options.Enable_Launch_Traps,
        "Hit N Run": world.options.Enable_HitNRun_Traps,
        "Traffic Trap": world.options.Enable_Traffic_Traps,
    }

    for item, option in trap_option_map.items():
        if option:
            for _ in range(10):
                itempool.append(world.create_item(item))

    # add items to itempool, make sure there's at least one car for each level and of each size marked prog, only add moves if they're shuffled
    for name, item_def in ITEM_DEFS.items():
        if name == start_car.name:
            # this car already exists
            continue

        if (name in world.prog_cars) or (world.options.Itchy_And_Scratchy_Ticket_Requirement == 3 and item_def.is_car):
            itempool.append(world.create_item(name, True))
        else:
            if item_def.always_exists:
                itempool.append(world.create_item(name))

    num_items = len(itempool)

    num_unfilled_locs = len(world.multiworld.get_unfilled_locations(world.player))

    needed_filler = num_unfilled_locs - num_items
    itempool += [world.create_filler() for _ in range(needed_filler)]
    world.multiworld.itempool += itempool

    early = set(world.options.Early_Forward)

    if "All" in early:
        characters = ["Homer", "Bart", "Lisa", "Marge", "Apu"]
    elif "None" in early:
        characters = []
    else:
        characters = early

    for character in characters:
        world.multiworld.early_items[world.player][f"{character} Forward"] = 1

    if world.options.Early_Level:
        levels = ["1", "2", "3", "4", "5", "6", "7"] if "All" in world.options.Required_Mission_Levels else list(world.options.Required_Mission_Levels)
        level = world.random.choice(levels)
        world.multiworld.early_items[world.player][f"Level {level}"] = 1

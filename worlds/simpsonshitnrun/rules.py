from __future__ import annotations

from typing import TYPE_CHECKING, Callable

from BaseClasses import CollectionState
from worlds.generic.Rules import add_rule, set_rule

if TYPE_CHECKING:
    from .world import SimpsonsHitNRunWorld

# RC Car excluded because it can't be used for hitting wasps reliably and is too small to consider for jumps
# Obliteratatron excluded because its wheels make it impossible to use for spawning on top of car strats, and it'd be too complicated to consider in logic (for now anyway)
small_cars = ["Family Sedan", "Electaurus", "Honor Roller", "Moe's Sedan", "Limo", "Malibu Stacy Car", "Nerd Car", "Clown Car", "Kremlin", "Krusty's Limo", "Curator",
              "Longhorn", "El Carro Loco", "Hover Car", "Car Built For Homer", "Police Car", "Ferrini - Red", "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car",
              "Chase Sedan", "70's Sports Car", "Open Wheel Race Car", "Zombie Car", "Hover Bike", "Hearse", "Speed Rocket", "Knight Boat", "ATV", "Planet Hype 50's Car",
              "Taxi", "Sedan B", "Sports Car B", "Sports Car A", "Compact Car", "SUV", "Hallo Hearse", "Coffin Car", "Witch Broom", "Ghost Ship", "Sedan A", "Station Wagon",
              "Cell Phone Car", "Ferrini - Black"]
medium_cars = ["Pickup Truck", "Surveillance Van", "WWII Vehicle", "Mr. Plow", "Book Burning Van", "Skinner's Sedan", "Donut Truck", "Canyonero", "Tractor", "Mr. Burns' Limo",
               "Monorail Car", "Glass Truck", "Minivan", "Pizza Van", "Fish Van", "Nuclear Waste Truck", "Pickup", "Nonuplets Minivan", "WWII Vehicle W\\ Rocket"]
large_cars = ["Plow King", "Duff Truck", "Fire Truck", "School Bus", "Cola Truck", "Armored Truck", "Mini School Bus", "Garbage Truck", "Vote Quimby Truck", "Ambulance",
              "Itchy and Scratchy Movie Truck", "Burns Armored Truck", "Ice Cream Truck", "Bonestorm Truck", "Cube Van", "Milk Truck"]

# Name: driving height, standing height if 1 jump, standing height if 2 jump, needs wall for 1 jump, needs 2 jump to stand on
cars_with_height = {
    "Audi TT": [0.88904362916946, 0.00, 0.00, False, False],
    "R/C Buggy": [0.1420596987009, 0.55, 0.55, False, False],
    "Knight Boat": [0.38586622476578, 1.05, 1.05, False, False],
    "ATV": [0.84600263834, 1.15, 1.15, False, False],
    "Ghost Ship": [0.43597140908241, 1.15, 1.15, False, False],
    "Ferrini - Black": [1.0352524518967, 1.22, 1.22, False, False],
    "Open Wheel Race Car": [1.0246151685715, 1.27, 1.27, False, False],
    "36 Stutz Bearcat": [0.95322567224503, 1.32, 1.32, False, False],
    "Malibu Stacy Car": [0.71360820531845, 1.44, 1.44, False, False],
    "Ferrini - Red": [1.0352524518967, 1.51, 1.51, False, False],
    "Sports Car A": [1.2352250814438, 1.53, 1.53, False, False],
    "Sports Car B": [1.1229319572449, 1.53, 1.53, False, False],
    "70's Sports Car": [1.0239123106003, 1.57, 1.57, False, False],
    "Coffin Car": [0.63846975564957, 1.59, 1.59, False, False],
    "Planet Hype 50's Car": [0.39757785201073, 1.59, 1.59, False, False],
    "Longhorn": [1.1072555780411, 1.60, 1.60, False, False],
    "Curator": [1.0599981546402, 1.66, 1.66, False, False],
    "Family Sedan": [0.38035726547241, 1.69, 1.69, False, False],
    "Chase Sedan": [1.1364763975143, 1.70, 1.70, False, False],
    "Tractor": [1.144605755806, 1.70, 1.70, False, False],
    "Cell Phone Car": [1.033905506134, 1.71, 1.71, False, False],
    "Clown Car": [1.0350135564804, 1.72, 1.72, False, False],
    "Moe's Sedan": [1.0493868589401, 1.72, 1.72, False, False],
    "Compact Car": [1.0163091421127, 1.74, 1.74, False, False],
    "Hover Bike": [0.42122980952263, 1.74, 1.74, False, False],
    "Witch Broom": [0.49036625027657, 1.74, 1.74, False, False],
    "Electraurus": [1.0801006555557, 1.75, 1.75, False, False],
    "Bandit": [0.9866349697113, 1.76, 1.76, False, False],
    "Taxi": [1.1277488470078, 1.76, 1.76, False, False],
    "Globex Super Villain Car": [1.2801865339279, 1.77, 1.77, False, False],
    "Station Wagon": [1.0978087186813, 1.77, 1.77, False, False],
    "Limo": [1.1383023262024, 1.79, 1.79, False, False],
    "Nerd Car": [1.1229592561722, 1.79, 1.79, False, False],
    "Sedan B": [1.1040531396866, 1.80, 1.80, False, False],
    "Krusty's Limo": [0.40398040413857, 1.81, 1.81, False, False],
    "Skinner's Sedan": [0.96899342536926, 1.81, 1.81, False, False],
    "Police Car": [1.1692904233932, 1.83, 1.83, False, False],
    "El Carro Loco": [1.0693520307541, 1.85, 1.85, False, False],
    "Hallo Hearse": [0.99800789356232, 1.87, 1.87, False, False],
    "Mr. Burns' Limo": [1.2676959037781, 1.90, 1.90, False, False],
    "Kremlin": [1.1578575372696, 1.92, 1.92, False, False],
    "Minivan": [1.0423936843872, 1.99, 1.99, False, False],
    "Milk Truck": [1.2454595565796, 2.00, 2.00, False, False],
    "Pickup": [1.0575177669525, 2.02, 2.02, False, False],
    "Nonuplets Minivan": [1.0423936843872, 2.04, 2.04, False, False],
    "Nuclear Waste Truck": [1.0625860691071, 2.04, 2.04, False, False],
    "Hover Car": [1.2529621124268, 2.05, 2.05, False, False],
    "Honor Roller": [1.118599653244, 2.06, 2.06, False, False],
    "Car Built For Homer": [1.1477473974228, 2.07, 2.07, False, False],
    "Hearse": [0.45504277944565, 2.07, 2.07, False, False],
    "WWII Vehicle": [0.92515879869461, 2.12, 2.12, False, False],
    "WWII Vehicle W\\ Rocket": [0.92515879869461, 2.16, 2.16, False, False],
    "SUV": [1.1111797094345, 2.30, 2.30, False, False],
    "Pickup Truck": [1.0315010547638, 2.32, 2.32, False, False],
    "Fish Van": [1.0472620725632, 2.34, 2.34, True, False],
    "Donut Truck": [1.1898299455643, 2.35, 4.74, True, False],
    "Canyonero": [1.1241983175278, 2.41, 2.41, False, False],
    "Book Burning Van": [1.1568940877914, 2.48, 2.48, False, False],
    "Mr. Plow": [1.0322655439377, 2.58, 2.58, False, False],
    "Bonestorm Truck": [1.3887873888016, 2.62, 2.62, False, False],
    "Ice Cream Truck": [1.2766793966293, 2.63, 5.32, False, False],
    "Ambulance": [1.1065303087234, 2.67, 2.67, True, False],
    "Cube Van": [1.3887873888016, 2.70, 2.70, False, False],
    "Zombie Car": [1.4054447412491, 2.71, 2.71, False, False],
    "Speed Rocket": [1.4913637638092, 2.72, 2.72, False, False],
    "Armored Truck": [0.8586203455925, 2.75, 2.75, False, False],
    "Burns Armored Truck": [1.3873634338379, 2.82, 2.82, False, False],
    "Glass Truck": [1.4860532283783, 2.82, 2.82, False, False],
    "School Bus": [1.0493761301041, 2.86, 2.86, False, False],
    "Pizza Van": [1.0861008167267, 2.97, 2.97, False, False],
    "Duff Truck": [1.5190999507904, 3.23, 3.23, False, False],
    "Mini School Bus": [1.4455015659332, 3.25, 3.25, True, False],
    "Monorail Car": [0.6708989739418, 3.25, 3.25, False, False],
    "Vote Quimby Truck": [1.3887873888016, 3.27, 3.27, True, False],
    "Plow King": [1.3482452630997, 3.32, 3.32, False, False],
    "Cola Truck": [1.4344767332077, 3.33, 3.33, False, False],
    "Fire Truck": [1.3768050670624, 3.34, 3.34, False, False],
    "Obliteratatron Big Wheel Truck": [1.8496829271317, 3.52, 3.52, False, True],
    "Surveillance Van": [0.93560719490051, 3.60, 3.60, False, False],
    "Garbage Truck": [1.39524269104, 3.75, 3.75, True, False],
    "Itchy and Scratchy Movie Truck": [1.3887873888016, 4.88, 4.88, False, False]
}

cars_by_driving_height = sorted(cars_with_height.items(), key=lambda item: item[1][0])
cars_by_single_jump_height = sorted([item for item in cars_with_height.items() if not item[1][3] and not item[1][4]], key=lambda item: item[1][1])
cars_by_single_jump_height_with_wall = sorted([item for item in cars_with_height.items() if not item[1][4]], key=lambda item: item[1][1])
cars_by_double_jump_height = sorted(cars_with_height.items(), key=lambda item: item[1][2])

car_names_by_driving_height = [name for name, _ in cars_by_driving_height]
car_names_by_single_jump_height = [name for name, _ in cars_by_single_jump_height]
car_names_by_single_jump_height_with_wall = [name for name, _ in cars_by_single_jump_height_with_wall]
car_names_by_double_jump_height = [name for name, _ in cars_by_double_jump_height]


any_car = small_cars + medium_cars + large_cars #[car for car in cars_with_height.keys()]
any_car_wasps = [car for car in any_car if car not in ("Witch Broom", "Audi TT")]  # These can't reliably hit wasps
any_car_wasps.append("Obliteratatron Big Wheel Truck") # These can hit wasps, but can't be jumped on (just Obliteratatron for now)

def set_rule_if_location_exists(world, location_name: str, rule: Callable):
    try:
        location = world.get_location(location_name)
    except KeyError:
        return

    set_rule(location, rule)

def set_all_rules(world: SimpsonsHitNRunWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: SimpsonsHitNRunWorld) -> None:
    # These are set in regions.py for now
    pass

def set_all_location_rules(world: SimpsonsHitNRunWorld) -> None:
    # Missions
    set_rule(world.get_location("(L1M2) Petty Theft Homer"), lambda state: state.has_any(("Homer Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player))
    set_rule(world.get_location("(L1M3) Office Spaced"), lambda state: state.has("Plow King", world.player))
    #set_rule(world.get_location("(L1M4) Blind Big Brother"), lambda state: state.has("Homer Progressive Jump", world.player)) will remove entirely after some more feedback
    set_rule(world.get_location("(L2M6) Monkey See Monkey D'oh"), lambda state: state.has("Mr. Plow", world.player) and \
                                                                                state.has_any(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player))
    set_rule(world.get_location("(L3M4) Operation Hellfish"), lambda state: state.has("School Bus", world.player))
    set_rule(world.get_location("(L3M5) Slithery Sleuthing"), lambda state: state.has("Lisa - Cool", world.player))
    set_rule(world.get_location("(L3M7) The Old Pirate and the Sea"), lambda state: state.has_any(("Family Sedan", "Electaurus", "Pickup Truck", "Plow King", "Duff Truck",
                                                                                                 "Surveillance Van", "Honor Roller", "Moe's Sedan", "WWII Vehicle", "Mr. Plow",
                                                                                                 "Limo", "Fire Truck", "Malibu Stacy Car", "Book Burning Van", "Skinner's Sedan",
                                                                                                 "School Bus", "Donut Truck", "Nerd Car", "Canyonero", "Clown Car", "Kremlin",
                                                                                                 "Tractor", "Krusty's Limo", "Curator", "Longhorn", "El Carro Loco", "Hover Car",
                                                                                                 "Car Built For Homer", "Police Car", "Cola Truck", "Ferrini - Red",
                                                                                                 "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car", "Chase Sedan",
                                                                                                 "70's Sports Car", "Open Wheel Race Car", "Mr. Burns' Limo", "Zombie Car",
                                                                                                 "Hover Bike", "Hearse", "Speed Rocket", "Monorail Car", "Knight Boat", "ATV",
                                                                                                 "Obliteratatron Big Wheel Truck", "Planet Hype 50's Car", "Mini School Bus",
                                                                                                 "Glass Truck", "Minivan", "Pizza Van", "Taxi", "Sedan B", "Fish Van",
                                                                                                 "Nuclear Waste Truck", "Ambulance", "Sports Car B",
                                                                                                 "Itchy and Scratchy Movie Truck", "Sports Car A", "Compact Car", "SUV",
                                                                                                 "Hallo Hearse", "Coffin Car", "Ghost Ship", "Sedan A", "Station Wagon",
                                                                                                 "Ice Cream Truck", "Cell Phone Car", "Cube Van", "Milk Truck",
                                                                                                 "Nonuplets Minivan", "WWII Vehicle W\\ Rocket", "Ferrini - Black"), world.player))
    set_rule(world.get_location("(L4M3) Ketchup Logic"), lambda state: state.has("Marge - Inmate", world.player))
    set_rule(world.get_location("(L4M6) The Cola Wars"), lambda state: state.has_all(("Marge - Police", "Marge Progressive Jump"), world.player))
    set_rule(world.get_location("(L4BM) Beached Love"), lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule(world.get_location("(L5M3) Eight is Too Much"), lambda state: state.has("Car Built For Homer", world.player))
    set_rule(world.get_location("(L5M4) This Little Piggy"), lambda state: state.has("Apu - American", world.player))
    set_rule(world.get_location("(L5M5) Never Trust a Snake"), lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule(world.get_location("(L6M4) Duff for Me, Duff for You"), lambda state: state.has_any(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player))
    set_rule(world.get_location("(L6M6) Set to Kill"), lambda state: state.has("Globex Super Villain Car", world.player))
    set_rule(world.get_location("(L7M1) Rigor Motors"), lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule(world.get_location("(L7M2) Long Black Probes"), lambda state: state.has("Zombie Car", world.player))
    set_rule(world.get_location("(L7M4) There's Something About Monty"), lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule(world.get_location("(L7M5) Alien \"Auto\"topsy Part 1"), lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule(world.get_location("(L7BM) Flaming Tires"), lambda state: state.has("Homer Progressive Jump", world.player))

    # Mission Locks
    for mission, car in world.missionlockdict.items():
        add_rule(world.get_location(mission), lambda state, locked_car=car: state.has(locked_car, world.player))

    # Gags
    set_rule(world.get_location("(LVL 1) GAG - Tank in Front of Power Plant"), lambda state: state.has("Homer Progressive Jump", world.player) or\
                                                                                             state.has_any((medium_cars + large_cars), world.player))
    set_rule(world.get_location("(LVL 2) GAG - Rat's Milk Machine atop Legitimate Businessman's Roof"), lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule(world.get_location("(LVL 4) GAG - Tank in Front of Power Plant"), lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                             state.has_any((medium_cars + large_cars), world.player))
    set_rule(world.get_location("(LVL 4) GAG - Krusty Lamp (Bart's Room)"), lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule(world.get_location("(LVL 7) GAG - Krusty Lamp (Bart's Room)"), lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule(world.get_location("(LVL 7) GAG - Clown Bed (Bart's Room)"), lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule(world.get_location("(LVL 7) GAG - Tank in Front of Power Plant"), lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                             state.has_any((medium_cars + large_cars) , world.player))

    # Wasps
    # L1
    set_rule(world.get_location("(LVL 1) WASP - Small Park Next to Simpsons House"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Flanders Backyard"), lambda state: state.has("Homer Attack", world.player))
    set_rule(world.get_location("(LVL 1) WASP - Wiggum's Backyard"), lambda state: (state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player) or \
                                                                                   (state.has_any(medium_cars + large_cars, world.player) and \
                                                                                    state.has("Homer Attack", world.player))))
    set_rule(world.get_location("(LVL 1) WASP - Kwik-E-Mart Roof"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Gas Pump Roof"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Lard Lad's Roof"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - School Yard Bus"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - School Roof 1"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - School Roof 2"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Top of Tower Before Broken Bridge"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Trailer Park 2"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Atop of Bridge Framework 1"), lambda state: state.has_all((["Homer Progressive Jump", "Homer Attack"]), world.player) and\
                                                                                            state.has_any(large_cars, world.player) or \
                                                                                            state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 1) WASP - Atop of Bridge Framework 2"), lambda state: state.has_all((["Homer Progressive Jump", "Homer Attack"]), world.player) and\
                                                                                            state.has_any(large_cars, world.player) or \
                                                                                            state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))

    set_rule(world.get_location("(LVL 1) WASP - Simpson's Neighbor's House"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 1) WASP - Back Door of School"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                        ["Honor Roller", "Malibu Stacy Car", "Ferrini - Red",
                                                                                                         "Bandit", "Open Wheel Race Car", "Ferrini - Black"], 0))
    set_rule(world.get_location("(LVL 1) WASP - StoneCutter's Table 1"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, []))
    set_rule(world.get_location("(LVL 1) WASP - StoneCutter's Table 2"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, []))
    set_rule(world.get_location("(LVL 1) WASP - Rocket Car"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, ["ATV", "Obliteratatron Big Wheel Truck"], 0))
    set_rule(world.get_location("(LVL 1) WASP - Barn Haystack"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                 ["Family Sedan", "Malibu Stacy Car", "Nerd Car",
                                                                                                            "Open Wheel Race Car", "Hover Bike", "Coffin Car"]))
    set_rule(world.get_location("(LVL 1) WASP - Trailer Park 1"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                   ["Nerd Car", "70's Sports Car", "Open Wheel Race Car"], 0))

    # L2
    set_rule(world.get_location("(LVL 2) WASP - Roof Across Monkey Building"), lambda state: state.has("Bart Attack", world.player) and \
                                                                                             state.has_any(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Monorail Stairs"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Upstairs Beside Monorail"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player) or \
                                                                                         (state.has("Bart Attack", world.player) and \
                                                                                          state.has_any(medium_cars + large_cars, world.player)))
    set_rule(world.get_location("(LVL 2) WASP - Monorail Building"), lambda state: state.has_all_counts({"Bart Attack" : 1, "Bart Progressive Jump" : 2}, world.player))
    set_rule(world.get_location("(LVL 2) WASP - Stairs Leading atop Trains"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Across Moving Train"), lambda state: state.has_all_counts({"Bart Attack" : 1, "Bart Progressive Jump" : 2}, world.player))
    set_rule(world.get_location("(LVL 2) WASP - On Train Past Water Tank"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Legitimate Businessman's Rooftop 1"), lambda state: (state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player) and \
                                                                                                     state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                     state.has_all_counts({"Bart Attack" : 1, "Bart Progressive Jump" : 2}, world.player))
    set_rule(world.get_location("(LVL 2) WASP - Legitimate Businessman's Rooftop 2"), lambda state: (state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player) and \
                                                                                                     state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                    state.has_all_counts({"Bart Attack": 1, "Bart Progressive Jump": 2}, world.player))

    set_rule(world.get_location("(LVL 2) WASP - Roof Next to Moe's"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Lard Lads Roof"), lambda state: (state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player) and \
                                                                                 state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                state.has_all_counts({"Bart Progressive Jump": 2, "Bart Attack": 1}, world.player))

    set_rule(world.get_location("(LVL 2) WASP - Courthouse Steps"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                     ["Family Sedan", "Moe's Sedan", "Malibu Stacy Car", "Nerd Car",
                                                                                                                "Krusty's Limo", "36 Stutz Bearcat", "Bandit", "Hover Bike"], 0))
    set_rule(world.get_location("(LVL 2) WASP - Gazebo Between Museum and Courthouse"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                     ["Honor Roller", "Moe's Sedan", "Malibu Stacy Car", "Clown Car",
                                                                                                      "Krusty's Limo", "Longhorn", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                      "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car",
                                                                                                      "Hover Bike", "Hearse", "Ghost Ship", "Ferrini - Black"], 0))
    set_rule(world.get_location("(LVL 2) WASP - Museum Steps"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                 ["Moe's Sedan", "Malibu Stacy Car", "Nerd Car", "Kremlin", "El Carro Loco",
                                                                                            "Ferrini - Red", "36 Stutz Bearcat", "Globex Super Villain Car", "70's Sports Car",
                                                                                            "Open Wheel Race Car", "Zombie Car", "Hover Bike", "Knight Boat", "ATV", "Planet Hype 50's Car",
                                                                                            "Taxi", "Sedan B", "Sports Car A", "Compact Car", "Coffin Car", "Ghost Ship", "Sedan A",
                                                                                            "Ferrini - Black", "Obliteratatron Big Wheel Truck"],
                                                                                    0))
    set_rule(world.get_location("(LVL 2) WASP - Hospital Front Yard"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                        ["Family Sedan", "Electaurus", "Honor Roller", "Moe's Sedan", "Malibu Stacy Car", "Nerd Car",
                                                                                                  "Longhorn", "El Carro Loco", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                                  "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car",
                                                                                                  "Hover Bike", "Compact Car", "Coffin Car", "Ferrini - Black"], 0))

    set_rule(world.get_location("(LVL 2) WASP - Town Hall (Front)"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                     ["Family Sedan", "Honor Roller", "Malibu Stacy Car", "Clown Car",
                                                                                                                "Krusty's Limo", "Bandit", "Open Wheel Race Car", "Hover Bike",
                                                                                                                "Hearse", "Ghost Ship"], 0))
    set_rule(world.get_location("(LVL 2) WASP - Town Hall (Back)"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                      ["Family Sedan", "Honor Roller", "Malibu Stacy Car", "Clown Car",
                                                                                                       "Krusty's Limo", "Bandit", "Open Wheel Race Car", "Hover Bike",
                                                                                                       "Hearse", "Ghost Ship"], 0))
    set_rule(world.get_location("(LVL 2) WASP - Behind Downtown Krusty Burger"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                     ["Open Wheel Race Car", "Knight Boat",
                                                                                                                "ATV", "Coffin Car", "Obliteratatron Big Wheel Truck"], 0))
    set_rule(world.get_location("(LVL 2) WASP - Inside Trainyard Shortcut"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 2) WASP - Car Wash"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                             ["Family Sedan", "Moe's Sedan", "Longhorn", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                        "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car", "Zombie Car",
                                                                                                        "Hover Bike", "Knight Boat", "Coffin Car", "Ghost Ship", "Ferrini - Black"], 0))

    # L3
    set_rule(world.get_location("(LVL 3) WASP - Observatory"), lambda state: state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Planet Hype"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Broken Railing Below Dam"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Broken Railing Above Dam (Exit)"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Kamp Krusty Well"), lambda state: state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Kamp Krusty Near Stage"), lambda state: state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Krusty Studio Left"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Krusty Studio Right"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Bowlarama Rooftop"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player) or \
                                                                                state.has_any(large_cars, world.player) and state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Comic Book Guy Rooftop"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))

    set_rule(world.get_location("(LVL 3) WASP - Exit of Kamp Krusty's Well"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps, ["ATV"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Motel near Observatory"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
                                                                                                  ["Limo", "Fire Truck", "Longhorn", "36 Stutz Bearcat", "ATV", "Garbage Truck",
                                                                                                            "Itchy and Scratchy Movie Truck", "Coffin Car"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Duff Brewery Behind Krusty Glass"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps, ["Coffin Car"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Duff Blimp 1"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps, ["ATV", "Coffin Car"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Duff Blimp 2"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps, ["ATV", "Coffin Car"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Globex Ship Front End"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
                                                                                       ["Garbage Truck", "Vote Quimby Truck", "Burns Armored Truck", "Bonestorm Truck"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Globex Ship Next to the Crane"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
                                                                                               ["Hover Bike", "Garbage Truck", "Vote Quimby Truck",
                                                                                                          "Burns Armored Truck", "Bonestorm Truck"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Globex Ship Stairs"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
                                                                                    ["Skinner's Sedan", "nerd Car", "Curator", "Longhorn", "El Carro Loco",
                                                                                               "Ferrini - Red", "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car",
                                                                                               "70's Sports Car", "Open Wheel Race Car", "Hover Bike", "Garbage Truck",
                                                                                               "Vote Quimby Truck", "Burns Armored Truck", "Ferrini - Black"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Lighthouse"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
                                                                            ["Family Sedan", "Honor Roller", "Moe's Sedan", "WWII Vehicle",
                                                                                       "Limo", "Malibu Stacy Car", "Nerd Car", "Krusty's Limo", "Curator",
                                                                                       "Longhorn", "El Carro Loco", "Police Car", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                       "Bandit", "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car",
                                                                                       "Zombie Car", "Hover Bike"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Beach"), lambda state:  can_break_wasp(world, state, "Lisa", any_car_wasps,
                                                                                                       ["Family Sedan", "Electaurus", "Pickup Truck", "Surveillance Van",
                                                                                                                  "Honor Roller", "Moe's Sedan", "WWII Vehicle", "Limo", "Malibu Stacy Car",
                                                                                                                  "Nerd Car", "Krusty's Limo", "Curator", "Longhorn", "El Carro Loco",
                                                                                                                  "Police Car", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                                                  "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car",
                                                                                                                  "Mr. Burns' Limo", "Zombie Car", "Hover Bike", "Hearse", "Knight Boat", "ATV",
                                                                                                                  "Planet Hype 50's Car", "Taxi", "Sedan B", "Nuclear Waste Truck", "Sports Car B",
                                                                                                                  "Sports Car A", "Compact Car", "SUV", "Hallo Hearse", "Coffin Car", "Ghost Ship",
                                                                                                                  "Sedan A", "Station Wagon", "Cell Phone Car", "Milk Truck", "WWII Vehicle W\\ Rocket",
                                                                                                                  "Ferrini - Black", "Obliteratatron Big Wheel Truck"], 0))


    # L4
    set_rule(world.get_location("(LVL 4) WASP - Flander's Backyard"), lambda state: state.has("Marge Attack", world.player))
    set_rule(world.get_location("(LVL 4) WASP - Wiggum's Backyard 1"), lambda state: (state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player) or \
                                                                                     (state.has_any(medium_cars + large_cars, world.player) and \
                                                                                      state.has("Marge Attack", world.player))))
    set_rule(world.get_location("(LVL 4) WASP - Wiggum's Backyard 2"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Kwik-E-Mart Rooftop"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Gas Station Rooftop"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Atop Gasoline Pump"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Atop Trailer Park"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Barn"), lambda state: (state.has_all_counts({"Marge Progressive Jump" : 1, "Marge Attack" : 1}, world.player)))
    set_rule(world.get_location("(LVL 4) WASP - School Rooftop 1"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - School Rooftop 2"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Atop Tower Before Broken Bridge"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))
    set_rule(world.get_location("(LVL 4) WASP - Outside of Homer's Workstation"), lambda state: state.has("Marge Attack", world.player))

    set_rule(world.get_location("(LVL 4) WASP - Blue House Before Krusty Glass 1"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                     ["Malibu Stacy Car", "Nerd Car", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                                                "Bandit", "Open Wheel Race Car", "Hover Bike", "Ferrini - Black"],
                                                                                                                     0))
    set_rule(world.get_location("(LVL 4) WASP - Blue House Before Krusty Glass 2"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                     ["Malibu Stacy Car", "Nerd Car", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                                                "Bandit", "Open Wheel Race Car", "Hover Bike", "Ferrini - Black"],
                                                                                                                     0))
    set_rule(world.get_location("(LVL 4) WASP - Burns Mansion Giant Chessboard 1"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 4) WASP - Burns Mansion Giant Chessboard 2"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 4) WASP - Burns Mansion Staircase"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                     ["Electaurus", "Pickup Truck", "Plow King", "Duff Truck", "Surveillance Van",
                                                                                                                                "Honor Roller", "Limo", "Book Burning Van", "School Bus", "Donut Truck",
                                                                                                                                "Nerd Car", "Canyonero", "Kremlin", "Tractor", "Krusty's Limo", "Curator",
                                                                                                                                "Longhorn", "El Carro Loco", "Hover Car", "Car Built For Homer", "Police Car",
                                                                                                                                "Cola Truck", "Globex Super Villain Car", "Armored Truck", "Chase Sedan",
                                                                                                                                "Mr. Burns' Limo", "Zombie Car", "Hearse", "Speed Rocket", "Monorail Car",
                                                                                                                                "Obliteratatron Big Wheel Truck", "Planet Hype 50's Car", "Mini School Bus",
                                                                                                                                "Glass Truck", "Minivan", "Pizza Van", "Taxi", "Sedan B", "Fish Van",
                                                                                                                                "Garbage Truck", "Nuclear Waste Truck", "Vote Quimby Truck", "Ambulance",
                                                                                                                                "Sports Car B", "Itchy and Scratchy Movie Truck", "Burns Armored Truck",
                                                                                                                                "Pickup", "Sports Car A", "Compact Car", "SUV", "Hallo Hearse", "Sedan A",
                                                                                                                                "Station Wagon", "Ice Cream Truck", "Cell Phone Car", "Cube Van", "Bonestorm Truck",
                                                                                                                                "Milk Truck", "Nonuplets Minivan", "Obliteratatron Big Wheel Truck"],
                                                                                                                     0))
    set_rule(world.get_location("(LVL 4) WASP - Burns Mansion Library"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                        ["Electaurus", "Pickup Truck", "Plow King", "Duff Truck", "Surveillance Van",
                                                                                                         "Honor Roller", "Limo", "Book Burning Van", "School Bus", "Donut Truck",
                                                                                                         "Nerd Car", "Canyonero", "Kremlin", "Tractor", "Krusty's Limo", "Curator",
                                                                                                         "Longhorn", "El Carro Loco", "Hover Car", "Car Built For Homer", "Police Car",
                                                                                                         "Cola Truck", "Globex Super Villain Car", "Armored Truck", "Chase Sedan",
                                                                                                         "Mr. Burns' Limo", "Zombie Car", "Hearse", "Speed Rocket", "Monorail Car",
                                                                                                         "Obliteratatron Big Wheel Truck", "Planet Hype 50's Car", "Mini School Bus",
                                                                                                         "Glass Truck", "Minivan", "Pizza Van", "Taxi", "Sedan B", "Fish Van",
                                                                                                         "Garbage Truck", "Nuclear Waste Truck", "Vote Quimby Truck", "Ambulance",
                                                                                                         "Sports Car B", "Itchy and Scratchy Movie Truck", "Burns Armored Truck",
                                                                                                         "Pickup", "Sports Car A", "Compact Car", "SUV", "Hallo Hearse", "Sedan A",
                                                                                                         "Station Wagon", "Ice Cream Truck", "Cell Phone Car", "Cube Van", "Bonestorm Truck",
                                                                                                         "Milk Truck", "Nonuplets Minivan", "Obliteratatron Big Wheel Truck"],
                                                                                                        0))
    set_rule(world.get_location("(LVL 4) WASP - In Trailer Park"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps, ["Open Wheel Race Car"], 0))
    set_rule(world.get_location("(LVL 4) WASP - Behind School Steps"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                   ["ATV"], 0))

    # L5
    set_rule(world.get_location("(LVL 5) WASP - Rooftop Next to Moe's"), lambda state: (state.has_all_counts({"Apu Progressive Jump": 1, "Apu Attack": 1}, world.player) and \
                                                                                      state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                      state.has_all_counts({"Apu Progressive Jump": 2, "Apu Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Legitimate Businessman's Rooftop 1"), lambda state: (state.has_all_counts({"Apu Progressive Jump": 1, "Apu Attack": 1}, world.player) and \
                                                                                                    state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                    state.has_all_counts({"Apu Progressive Jump": 2, "Apu Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Legitimate Businessman's Rooftop 2"), lambda state: (state.has_all_counts({"Apu Progressive Jump": 1, "Apu Attack": 1}, world.player) and \
                                                                                                     state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                    state.has_all_counts({"Apu Progressive Jump": 2, "Apu Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Trainyard Stairs"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    set_rule(world.get_location("(LVL 5) WASP - Other Side of Moving Train"), lambda state: state.has_all_counts({"Apu Progressive Jump": 2, "Apu Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Watertower 1"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    set_rule(world.get_location("(LVL 5) WASP - Watertower 2"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    set_rule(world.get_location("(LVL 5) WASP - Monorail Stairs"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    set_rule(world.get_location("(LVL 5) WASP - Monorail"), lambda state: state.has_all_counts({"Apu Progressive Jump" : 2, "Apu Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Monorail Building 1"), lambda state: state.has_all_counts({"Apu Progressive Jump" : 2, "Apu Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Monorail Building 2"), lambda state: state.has_all_counts({"Apu Progressive Jump" : 2, "Apu Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Fountain Near Stadium"), lambda state: (state.has_all_counts({"Apu Progressive Jump": 1, "Apu Attack": 1}, world.player) and \
                                                                                                     state.has_any(large_cars, world.player)) or \
                                                                                                    state.has_all_counts({"Apu Progressive Jump": 2, "Apu Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Alleyway Rooftop"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))

    set_rule(world.get_location("(LVL 5) WASP - Hospital Front Yard"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                                     ["Family Sedan", "Electaurus", "Pickup Truck", "Duff Truck",
                                                                                                                      "Surveillance Van", "Honor Roller", "Moe's Sedan", "WWII Vehicle",
                                                                                                                      "Mr. Plow", "Limo", "Malibu Stacy Car", "Nerd Car", "Clown Car",
                                                                                                                      "Krusty's Limo", "Curator", "Longhorn", "El Carro Loco", "Hover Car",
                                                                                                                      "Car Built For Homer", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                                                      "Globex Super Villain Car", "Chase Sedan", "70's Sports Car",
                                                                                                                      "Open Wheel Race Car", "Zombie Car", "Hover Bike", "ATV",
                                                                                                                      "Planet Hype 50's Car", "Compact Car", "Coffin Car", "Ferrini - Black"],
                                                                                                                     1))
    set_rule(world.get_location("(LVL 5) WASP - Gazebo Between Museum & Court House"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                              ["Family Sedan", "Electaurus", "Honor Roller", "WWII Vehicle",
                                                                                                               "Malibu Stacy Car", "Nerd Car", "Curator", "Longhorn", "Ferrini - Red",
                                                                                                               "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car", "70's Sports Car",
                                                                                                               "Open Wheel Race Car", "Hover Bike", "ATV", "Planet Hype 50's Car", "Compact Car",
                                                                                                               "Coffin Car", "Ghost Ship", "WWII Vehicle W\\ Rocket", "Ferrini - Black"],
                                                                                                              0))
    set_rule(world.get_location("(LVL 5) WASP - Steps of Town Hall"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                       ["Malibu Stacy Car", "Curator", "Longhorn", "Ferrini - Red",
                                                                                                       "36 Stutz Bearcat", "Open Wheel Race Car", "Zombie Car", "Hover Bike",
                                                                                                        "ATV", "Vote Quimby Truck", "Itchy and Scratchy Movie Truck", "Compact Car",
                                                                                                        "Ghost Ship", "Station Wagon", "Ferrini - Black"],
                                                                                                       0))
    set_rule(world.get_location("(LVL 5) WASP - Museum Steps"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                 ["Family Sedan", "Electaurus", "Pickup Truck", "Duff Truck",
                                                                                                 "Surveillance Van", "Honor Roller", "Moe's Sedan", "WWII Vehicle", "Mr. Plow",
                                                                                                 "Limo", "Malibu Stacy Car", "Skinner's Sedan", "Donut Truck", "Nerd Car", "Canyonero",
                                                                                                 "Clown Car", "Kremlin", "Krusty's Limo", "Curator", "Longhorn", "El Carro Loco",
                                                                                                  "Car Built For Homer", "Police Car", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                                  "Globex Super Villain Car", "Chase Sedan", "70's Sports Car", "Open Wheel Race Car",
                                                                                                  "Mr. Burns' Limo", "Zombie Car", "Hover Bike", "Hearse", "Speed Rocket", "Monorail Car",
                                                                                                  "Knight Boat", "ATV", "Planet Hype 50's Car", "Vote Quimby Truck", "Sports Car B",
                                                                                                  "Sports Car A", "Compact Car", "Coffin Car", "Ghost Ship", "Station Wagon", "Cell Phone Car",
                                                                                                  "WWII Vehicle W\\ Rocket", "Ferrini - Black"],
                                                                                                 1))
    set_rule(world.get_location("(LVL 5) WASP - Police Station Steps"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                       ["WWII Vehicle", "Malibu Stacy Car", "Donut Truck", "Nerd Car",
                                                                                                        "Clown Car", "Tractor", "Curator", "36 Stutz Bearcat", "70's Sports Car",
                                                                                                        "Zombie Car", "Hover Bike", "ATV", "Planet Hype 50's Car", "Mini School Bus",
                                                                                                        "Vote Quimby Truck", "Coffin Car", "Ghost Ship", "WWII Vehicle W\\ Rocket", "Ferrini - Black"],
                                                                                                       0))
    set_rule(world.get_location("(LVL 5) WASP - Sit 'n' Rotate 1"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                         ["Electaurus", "Malibu Stacy Car", "Curator", "Longhorn", "El Carro Loco",
                                                                                                          "Ferrini - Red", "Globex Super Villain Car", "ATV", "Open Wheel Race Car", "Hover Bike",
                                                                                                          "ATV", "Compact Car", "Ferrini - Black"],
                                                                                                         1))
    set_rule(world.get_location("(LVL 5) WASP - Sit 'n' Rotate 2"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                               ["Electaurus", "Malibu Stacy Car", "Curator", "Longhorn", "El Carro Loco",
                                                                                                                "Ferrini - Red", "Globex Super Villain Car", "ATV", "Open Wheel Race Car", "Hover Bike",
                                                                                                                "ATV", "Compact Car", "Ferrini - Black"],
                                                                                                               1))

    # L6
    set_rule(world.get_location("(LVL 6) WASP - Observatory 1"), lambda state: state.has("Bart Attack", world.player))
    set_rule(world.get_location("(LVL 6) WASP - Observatory 2"), lambda state: state.has("Bart Attack", world.player))
    set_rule(world.get_location("(LVL 6) WASP - Kamp Krusty 1"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Kamp Krusty 2"), lambda state: state.has("Bart Attack", world.player))
    set_rule(world.get_location("(LVL 6) WASP - Broken Railing Below Dam"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Broken Railing Exit"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Krusty Studio Left"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Krusty Studio Right"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Krusty Studio Balcony"), lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                        state.has_any(large_cars, world.player) or \
                                                                                        state.has("Bart Progressive Jump", world.player, 2)) and \
                                                                                        state.has("Bart Attack", world.player))
    set_rule(world.get_location("(LVL 6) WASP - Planet Hype Rooftop"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Bowlarama Rooftop"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Comic Book Guy Rooftop 1"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Comic Book Guy Rooftop 2"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))

    set_rule(world.get_location("(LVL 6) WASP - Motel by Observatory"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                          ["Family Sedan", "Electaurus", "Surveillance Van", "Honor Roller", "Moe's Sedan",
                                                                                          "WWII Vehicle", "Limo", "Fire Truck", "Malibu Stacy Car", "Nerd Car", "Clown Car", "Curator",
                                                                                          "Longhorn", "El Carro Loco", "Cola Truck", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                           "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car", "Zombie Car", "Hover Bike",
                                                                                           "ATV", "Obliteratatron Big Wheel Truck", "Planet Hype 50's Car", "Taxi", "Garbage Truck",
                                                                                           "Vote Quimby Truck", "Itchy and Scratchy Movie Truck", "Compact Car", "Coffin Car",
                                                                                           "Ghost Ship", "Ferrini - Black", "Obliteratatron Big Wheel Truck"],
                                                                                          0))
    set_rule(world.get_location("(LVL 6) WASP - Duff Brewery Krusty Glass"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                          ["Family Sedan", "Electaurus", "Honor Roller", "Moe's Sedan", "Malibu Stacy Car",
                                                                                           "Nerd Car", "Curator", "Longhorn", "El Carro Loco", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                           "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car", "Hover Bike",
                                                                                           "ATV", "Ferrini - Black"],
                                                                                          0))
    set_rule(world.get_location("(LVL 6) WASP - Under Duff Blimp"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                     ["Family Sedan", "Electaurus", "Honor Roller", "Surveillance Van", "Moe's Sedan",
                                                                                                      "WWII Vehicle", "Malibu Stacy Car", "Nerd Car", "Clown Car", "Krusty's Limo", "Curator",
                                                                                                      "Longhorn", "El Carro Loco", "Car Built For Homer", "Police Car", "Ferrini - Red",
                                                                                                      "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car", "Chase Sedan", "70's Sports Car",
                                                                                                      "Open Wheel Race Car", "Mr. Burns' Limo", "Zombie Car", "Hover Bike", "Hearse", "ATV",
                                                                                                     "Sports Car A", "Coffin Car", "Ghost Ship", "WWII Vehicle W\\ Rocket", "Ferrini - Black"],
                                                                                                     0))
    set_rule(world.get_location("(LVL 6) WASP - Globex Ship Crane"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                      ["Moe's Sedan", "Malibu Stacy Car", "Open Wheel Race Car", "Hover Bike",
                                                                                                      "ATV", "Garbage Truck", "Vote Quimby Truck", "Burns Armored Truck", "Bonestorm Truck"],
                                                                                                      0))
    set_rule(world.get_location("(LVL 6) WASP - Globex Ship Staircase 1"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                            ["Honor Roller", "Moe's Sedan", "Limo", "Malibu Stacy Car", "Nerd Car", "Longhorn",
                                                                                                             "El Carro Loco", "36 Stutz Bearcat", "Globex Super Villain Car", "Open Wheel Race Car",
                                                                                                             "Hover Bike", "ATV", "Garbage Truck", "Vote Quimby Truck", "Burns Armored Truck",
                                                                                                             "Bonestorm Truck"],
                                                                                                            0))
    set_rule(world.get_location("(LVL 6) WASP - Globex Ship Staircase 2"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                                            ["Honor Roller", "Moe's Sedan", "Limo", "Malibu Stacy Car", "Nerd Car", "Longhorn",
                                                                                                             "El Carro Loco", "36 Stutz Bearcat", "Globex Super Villain Car", "Open Wheel Race Car",
                                                                                                             "Hover Bike", "ATV", "Garbage Truck", "Vote Quimby Truck", "Burns Armored Truck",
                                                                                                             "Bonestorm Truck"],
                                                                                                            0))
    set_rule(world.get_location("(LVL 6) WASP - Lighthouse"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                               ["Family Sedan", "Electaurus", "Surveillance Van", "Honor Roller", "Moe's Sedan",
                                                                                                "WWII Vehicle", "Limo", "Malibu Stacy Car", "Nerd Car", "Clown Car", "Kremlin", "Krusty's Limo",
                                                                                                "Longhorn", "El Carro Loco", "Hover Car", "Car Built For Homer", "Police Car", "Ferrini - Red",
                                                                                                "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car", "Chase Sedan", "70's Sports Car",
                                                                                                "Open Wheel Race Car", "Mr. Burns' Limo", "Zombie Car", "Hearse", "ATV", "Ghost Ship",
                                                                                                "WWII Vehicle W\\ Rocket", "Ferrini - Black"],
                                                                                               0))

    # L7
    set_rule(world.get_location("(LVL 7) WASP - Blue House Haunted Playground"), lambda state: state.has_all(("Homer Attack", "Homer Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - Simpsons' Backyard"), lambda state: (state.has("Homer Attack", world.player) and state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                     state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - Flanders' Backyard"), lambda state: state.has("Homer Attack", world.player))
    set_rule(world.get_location("(LVL 7) WASP - Wiggum's Backyard"), lambda state: (state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player) or \
                                                                                   (state.has_any(medium_cars + large_cars, world.player) and \
                                                                                    state.has("Homer Attack", world.player))))
    set_rule(world.get_location("(LVL 7) WASP - Atop of Kwik-E-Mart"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - Atop of Gasoline"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - Lard Lad Rooftop"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - Krusty Burger Rooftop"), lambda state: state.has("Homer Attack", world.player))
    set_rule(world.get_location("(LVL 7) WASP - School Playground"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - The One Being Abducted"), lambda state: state.has("Homer Attack", world.player))
    set_rule(world.get_location("(LVL 7) WASP - School Roof 1"), lambda state: state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - School Roof 2"), lambda state: state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - Bridge Frame by Cletus"), lambda state: state.has_all((["Homer Progressive Jump", "Homer Attack"]), world.player) and\
                                                                                               state.has_any(large_cars, world.player) or \
                                                                                               state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - Trailer Park 1"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - Trailer Park 2"), lambda state: (state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player) and \
                                                                                     state.has_any(large_cars, world.player)) or \
                                                                                     state.has_all_counts({"Homer Progressive Jump" : 2, "Homer Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - Barn Silo"), lambda state: state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - Mr. Burns Office"), lambda state: state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))

    set_rule(world.get_location("(LVL 7) WASP - Blue House Backyard"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                                  ["Family Sedan", "Honor Roller", "Moe's Sedan", "Malibu Stacy Car", "Nerd Car",
                                                                                                                   "Curator", "Longhorn", "El Carro Loco", "Car Built For Homer", "Ferrini - Red",
                                                                                                                   "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car", "70's Sports Car",
                                                                                                                   "Open Wheel Race Car", "Zombie Car", "Hover Bike", "Knight Boat", "ATV",
                                                                                                                   "Ferrini - Black"],
                                                                                                                  1))
    set_rule(world.get_location("(LVL 7) WASP - Bridge Barricade"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                                  ["Family Sedan", "Electaurus", "Surveillance Van", "Honor Roller", "Moe's Sedan",
                                                                                                                   "WWII Vehicle", "Limo", "Malibu Stacy Car", "Book Burning Van", "Skinner's Sedan",
                                                                                                                   "Donut Truck", "Nerd Car", "Clown Car", "Kremlin", "Tractor", "Krusty's Limo"
                                                                                                                   "Curator", "Longhorn", "El Carro Loco", "Hover Car", "Car Built For Homer",
                                                                                                                   "Police Car", "Ferrini - Red", "36 Stutz Bearcat", "Bandit", "Globex Super Villain Car",
                                                                                                                   "Chase Sedan", "70's Sports Car", "Open Wheel Race Car", "Mr. Burn's' Limo", "Zombie Car",
                                                                                                                   "Hover Bike", "Hearse", "Speed Rocket", "Monorail Car", "Knight Boat", "ATV", "Planet Hype 50's Car",
                                                                                                                   "Taxi", "Sedan B", "Sports Car B", "Sports Car A", "Compact Car", "SUV", "Ghost Ship", "Sedan A",
                                                                                                                   "Station Wagon", "Cell Phone Car", "WWII Vehicle W\\ Rocket", "Ferrini - Black"],
                                                                                                                  1))
    set_rule(world.get_location("(LVL 7) WASP - Power Plant Parking lot"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                     ["Family Sedan", "Electaurus", "Surveillance Van", "Honor Roller", "Moe's Sedan",
                                                                                                      "Limo", "Malibu Stacy Car", "Nerd Car", "Kremlin", "Tractor", "Curator", "Longhorn",
                                                                                                      "El Carro Loco", "Car Built For Homer", "Ferrini - Red", "36 Stutz Bearcat", "Bandit",
                                                                                                      "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car", "Mr. Burn's' Limo", "Zombie Car",
                                                                                                      "Hover Bike", "Hearse", "Speed Rocket", "Monorail Car", "Knight Boat", "ATV",
                                                                                                      "Planet Hype 50's Car", "Sedan B", "Sports Car B", "Sports Car A", "Compact Car", "Hallo Hearse",
                                                                                                      "Ghost Ship", "Sedan A", "Station Wagon", "Ferrini - Black"],
                                                                                                     1))
    # Cards
    # L1
    set_rule_if_location_exists(world, "(LVL 1) CARD - Simpsons' Backyard", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Kwik-E-Mart Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Wiggum's Backyard", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above StoneCutters Table", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Highest Platform in Power Plant", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Trailer Park", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                     state.has("Homer Progressive Jump", world.player) or \
                                                                                     state.has("Homer Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Neighbor's Carport", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Kwik-E-Mart's Dumpster", lambda state: state.has_any(get_cars_by_height("Krusty's Limo", 1, False, False), world.player) or \
                                                                                                     state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Krusty Burger's Dumpster", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                 state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Gas Station Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Street Between Simpsons' House and Kwik-E-Mart", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                                                                          state.has("Homer Progressive Jump", world.player) or \
                                                                                                                                          state.has("Homer Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Retirement Castle", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                       state.has("Vote Quimby Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Church Dumpster", lambda state: state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) or \
                                                                                                   state.has("Obliteratatron Big Wheel Truck", world.player) or \
                                                                                                   state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Dumpster Behind Krusty Burger Near School", lambda state: state.has_any(get_cars_by_height("Armored Truck", 1, False, False), world.player) or \
                                                                                                                        state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Back of School Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Grocery Store's Dumpster", lambda state: state.has_any(get_cars_by_height("WWII Vehicle", 1, False, False), world.player) or \
                                                                                                state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - House Across From Simpsons' House 1", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                           state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Wiggum's", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Cletus' House", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                    state.has_any(get_cars_by_height("SUV", 1, False, False), world.player)) or \
                                                                                                    state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Big Bridge", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                   state.has("Homer Progressive Jump", world.player)) or \
                                                                                  state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Trailer Park", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                        state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Street Near Barn", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                                            state.has("Homer Progressive Jump", world.player)) or \
                                                                                                            state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Power Plant Parking Lot 1", lambda state: state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player) or \
                                                                                                 (state.has_any(get_cars_by_height("Armored Truck", 1, False, False), world.player) and \
                                                                                                  state.has("Homer Progressive Jump", world.player)) or \
                                                                                                 state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Street Near Simpsons' House", lambda state: (state.has_any(["Surveillance Van", "Itchy and Scratchy Movie Truck"], world.player) and \
                                                                                                          state.has("Homer Progressive Jump", world.player)) or \
                                                                                                         state.has_any(get_cars_by_height("Vote Quimby Truck", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Nuclear Waste Bridge", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                  state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Roof Across of House Across From Gold Mansion", lambda state: state.has("Homer Progressive Jump", world.player, 2) or \
                                                                                                                                   state.has_any(["Knight Boat", "ATV", "Ghost Ship", "Ferrini - Black",
                                                                                                                                                  "Open Wheel Race Car", "36 Stutz Bearcat", "Malibu Stacy Car",
                                                                                                                                                  "Ferrini - Red", "Sports Car A", "Sports Car B", "70's Sports Car",
                                                                                                                                                  "Coffin Car", "Planet Hype 50's Car", "Longhorn", "Curator", "Family Sedan",
                                                                                                                                                  "Chase Sedan", "Tractor", "Cell Phone Car", "Clown Car", "Moe's Sedan",
                                                                                                                                                  "Compact Car", "Hover Bike", "Witch Broom", "Electaurus", "Bandit", "Taxi",
                                                                                                                                                  "Globex Super Villain Car", "Station Wagon", "Limo", "Nerd Car", "Sedan A", "Sedan B",
                                                                                                                                                  "Krusty's Limo", "Skinner's Sedan", "Police Car", "El Carro Loco", "Hallo Hearse",
                                                                                                                                                  "Mr. Burns' Limo", "Kremlin", "Minivan", "Milk Truck", "Pickup", "Nonuplets Minivan",
                                                                                                                                                  "Nuclear Waste Truck", "Hover Car", "Honor Roller", "Car Built For Homer", "Hearse",
                                                                                                                                                  "WWII Vehicle", "WWII Vehicle w/ Rocket", "SUV", "Fish Van", "Donut Truck", "Canyonero",
                                                                                                                                                  "Book Burning Van", "Mr. Plow", "Bonestorm Truck", "Cube Van", "Zombie Car", "Speed Rocket",
                                                                                                                                                  "Burns Armored Truck", "Glass Truck", "Pizza Van", "Duff Truck", "Cola Truck", "Fire Truck",
                                                                                                                                                  "Surveillance Van"], world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Outside Burns Mansion Gate", lambda state: state.has_any(any_car, world.player) and \
                                                                                                  state.has("Homer Progressive Jump", world.player) or \
                                                                                                  state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Rocket Car", lambda state: state.has_any(large_cars, world.player) or state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Top of Krusty Burger Near Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player))

    # L2
    set_rule_if_location_exists(world, "(LVL 2) CARD - Jebediah Statue", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Jebediah Statue", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                     state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Roof Across Monkey Building", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                  state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                  state.has("Bert Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Legitimate Businessman's Roof", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                    state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                    state.has("Bert Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Car Wash", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                               state.has_any(large_cars, world.player) or \
                                                                                               state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Train Wagon", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - DMV Light Pole", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Fountain At Stadium", lambda state: state.has_all(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player) or \
                                                                                                         state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Light Pole by Court House", lambda state: (state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player) and \
                                                                                                                state.has("Bart Progressive Jump", world.player)) or \
                                                                                                                state.has_any(get_cars_by_height("Armored Truck", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Lion Statue", lambda state: state.has_any(["Vote Quimby Truck", "Ambulance", "Burns Armored Truck", "Canyonero", "Car Built For Homer", "Cell Phone Car",
                                                                                                               "Clown Car", "Cola Truck", "Compact Car", "Donut Truck", "El Carro Loco", "Fish Van", "Garbage Truck", "Glass Truck",
                                                                                                               "Hallo Hearse", "Hover Car", "Ice Cream Truck", "Itchy & Scratchy Movie Truck", "Kremlin", "Milk Truck", "Mini School Bus",
                                                                                                               "Minivan", "Moe's Sedan", "Monorail Car", "Mr. Plow", "Nerd Car", "Nonuplets Minivan", "Nuclear Waste Truck", "Obliteratatron Big Wheel Truck",
                                                                                                               "Pickup", "Pickup Truck", "Pizza Van", "Plow King", "School Bus", "Sedan A", "Sedan B", "Skinner's Sedan", "Station Wagon", "Surveillance Van",
                                                                                                               "SUV", "Taxi"], world.player) or \
                                                                                                 state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Hospital Parking Lot", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                             state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                             state.has_any(get_cars_by_height("SUV", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Stadium Behind Duff Mascot", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                state.has_any(["Garbage Truck", "Itchy and Scratchy Movie Truck"], world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Tree By Krusty Burger Downtown", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                     state.has_any(get_cars_by_height("36 Stutz Bearcat", 1, False, False))) or \
                                                                                                                     state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Monorail", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Corner of Monorail Station", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Downtown Krusty Float", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                              state.has_any(get_cars_by_height("Ferrini - Black", 1, False, False), world.player)) or\
                                                                                                                              state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                                                              state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Downtown Highway Exit", lambda state: (state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                                  state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                 (state.has("Bart Progressive Jump", world.player, 1) and \
                                                                                                                  state.has_any(get_cars_by_height("Chase Sedan", 1, False, False), world.player)) or \
                                                                                                                  state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Helter Shelter", lambda state: state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                                                      (state.has("Bart Progressive Jump", world.player, 1) and \
                                                                                                                      state.has_any(get_cars_by_height("Chase Sedan", 1, False, False), world.player)) or \
                                                                                                                      state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Tree By Krusty Burger Downtown", lambda state: state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                                    state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Between DMV and Trainyard", lambda state: state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                                                     (state.has("Bart Progressive Jump", world.player, 1) and \
                                                                                                                     state.has_any(get_cars_by_height("Malibu Stacy Car", 1, False, False), world.player)) or \
                                                                                                                     state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Train Crossing", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Car Wash", lambda state: (state.has("Bart Progressive Jump", world.player, 1) and \
                                                                                                                 state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                 state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - On Top of Gas Station at Car Wash", lambda state: (state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                                        state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                       (state.has("Bart Progressive Jump", world.player, 1) and \
                                                                                                                        state.has_any(get_cars_by_height("Chase Sedan", 1, False, False), world.player)) or \
                                                                                                                        state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Lexicon Bookstore Roof", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Legitimate Businessman's Roof 2", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                     state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                                     state.has("Bert Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Glen's Grocery Roof", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                         state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                         state.has("Bert Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Street Near Construction", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Hospital Sign", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                    state.has_any(get_cars_by_height("Audi TT", 1, False, False), world.player)) or \
                                                                                                    state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Tree Outside Police Station", lambda state: state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                                         (state.has_any(get_cars_by_height("WWII Vehicle W\\ Rocket", 1, False, False), world.player) and \
                                                                                                          state.has("Bart Progressive Jump", world.player, 1)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Stop Sign Across From Moe's", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                 state.has_any(get_cars_by_height("Plow King", 1, False, False), world.player))


    # L3
    set_rule_if_location_exists(world, "(LVL 3) CARD - Android's Dungeon Rooftop", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Above Bowlarama", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Atop Lighthouse", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Krusty Studio Balcony", lambda state: state.has("Lisa Progressive Jump", world.player, 2) or \
                                                                                                           state.has_any(get_cars_by_height("Hallo Hearse", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Beside Broken Bridge", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Edge of Globex Ship", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Planet Hype Outdoor Seating", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Barrels Near Gil", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                      state.has_any(["Vote Quimby Truck", "Bonestorm Truck", "Burns Armored Truck", "Canyonero", "Cola Truck", "Cube Van", "Donut Truck",
                                                                                                                     "Duff Truck", "Garbage Truck", "Hallo Hearse", "Hover Bike", "Hover Car", "Ice Cream Truck", "Itchy & Scratchy Movie Truck",
                                                                                                                     "Monorail Car", "Longhorn", "Mr. Plow", "Nuclear Waste Truck", "Obliteratatron Big Wheel Truck", "Pickup Truck", "Pizza Van",
                                                                                                                     "Plow King", "School Bus", "Speed Rocket", "SUV", "WWII Vehicle", "WWII Vehicle w/ Rocket", "Ambulance", "Armored Truck",
                                                                                                                     "Car Built For Homer", "Compact Car", "Curator", "El Carro Loco", "Electaurus", "Fire Truck", "Fish Van", "Glass Truck", "Hearse",
                                                                                                                     "Kremlin", "Krusty's Limo", "Limo", "Milk Truck", "Mini School Bus", "Minivan", "Moe's Sedan", "Nerd Car", "Nonuplets Minivan",
                                                                                                                     "Pickup", "Police Car", "Sedan A", "Sedan B", "Skinner's Sedan", "Sports Car A", "Station Wagon", "Surveillance Van", "Taxi"], world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Boulevard Near Krusty and Friends Billboard", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                                 state.has_any("Obliteratatron Big Wheel Truck, Garbage Truck, Itchy and Scratchy Movie Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Concrete Mixer at Gas Station", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                   state.has_any(["Knight Boat", "ATV", "Open Wheel Race Car", "36 Stutz Bearcat", "Malibu Stacy Car",
                                                                                                                                "70's Sports Car", "Planet Hype 50's Car", "Longhorn", "Curator", "Chase Sedan",
                                                                                                                                "Tractor", "Cell Phone Car A", "Cell Phone Car B", "Cell Phone Car C",
                                                                                                                                "Cell Phone Car D", "Clown Car", "Moe's Sedan", "Hover Bike", "Bandit",
                                                                                                                                "Globex Super Villain Car", "Nerd Car", "Skinner's Sedan", "Police Car",
                                                                                                                                "El Carro Loco", "Hallo Hearse", "Mr. Burns' Limo", "Kremlin", "Hover Car",
                                                                                                                                "Car Built For Homer", "Hearse", "WWII Vehicle w/ Rocket", "SUV", "Fish Van",
                                                                                                                                "Donut Truck", "Canyonero", "Book Burning Van", "Mr. Plow", "Zombie Car",
                                                                                                                                "Speed Rocket", "Pizza Van", "School Bus", "Vote Quimby Truck", "Garbage Truck",
                                                                                                                                "Itchy & Scratchy Movie Truck"], world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Lumber King Billboard", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                           state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Box Near Gil", lambda state: state.has("Lisa Progressive Jump", world.player, 2)  or \
                                                                                                  state.has_any([c for c in get_cars_by_height("Mini School Bus", 0, False, False) if c != "Monorail Car"], world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Davey Jones Hamper", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                        state.has_any(get_cars_by_height("Burns Armored Truck", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Globex Ship Crane", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Globex Ship Inside Cargo Container", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - KrustyLu Studios Sign", lambda state: state.has("Lisa Progressive Jump", world.player, 2) or \
                                                                                                           (state.has_any("Garbage Truck, Itchy and Scratchy Movie Truck", world.player) and \
                                                                                                            state.has("Lisa Progressive Jump", world.player)))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Behind KrustyLu Studios Sign", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                  state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Motel Awning", lambda state: state.has("Lisa Progressive Jump", world.player, 2) or \
                                                                                                           state.has_any(get_cars_by_height("Monorail Car", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Observatory 1", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Observatory 2", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                   state.has_any(["R/C Buggy", "ATV", "Hover Bike", "Witch Broom", "Coffin Car"], world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Kamp Krusty Weight Loss Center", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Boar's Head at Kamp Krusty", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Dam", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Parking Spot Across From Android's Dungeon", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                                state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Above Road Near Drain Pipe", lambda state: state.has("Lisa Progressive Jump", world.player, 2) or \
                                                                                                                state.has_any(get_cars_by_height("Hallo Hearse", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Captain Chum 'N' Stuff", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                     state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Upper Casino Entrance", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                           state.has_any(get_cars_by_height("Pickup Truck", 0, False, False), world.player) or \
                                                                                                           state.has("Obliteratatron Big Wheel Truck"))

    # L4
    set_rule_if_location_exists(world, "(LVL 4) CARD - Between Gas Station and Lard Lad's", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Burns Mansion Secret", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Big Bridge", lambda state: (state.has("Marge Progressive Jump", world.player, 2)) or \
                                                                                                 state.has_any(get_cars_by_height("SUV", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Atop Tower Before Broken Bridge", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Simpsons' Tree House", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                   state.has_any(["R/C Buggy", "ATV", "Hover Bike", "Witch Broom", "Coffin Car"], world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - End of Trailer Park", lambda state: (state.has("Marge Progressive Jump", world.player, 2))  or \
                                                                                                 state.has_any(get_cars_by_height("Ferrini - Red", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Road Near Drain Pipe", lambda state: ((state.has("Marge Progressive Jump", world.player) and \
                                                                                                                 state.has_any(large_cars, world.player)) or \
                                                                                                                 state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Kwik-E-Mart", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Kwik-E-Mart's Dumpster", lambda state: state.has_any(get_cars_by_height("Krusty's Limo", 1, False, False), world.player) or \
                                                                                                            state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Krusty Burger Dumpster", lambda state: state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                            state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Gas Station Roof 2", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Street Between Simpsons' House and Kwik-E-Mart", lambda state: (state.has_any(get_cars_by_height("Malibu Stacy Car", 1, False, False), world.player) and \
                                                                                                                                           state.has("Marge Progressive Jump", world.player) or \
                                                                                                                                           state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Retirement Castle", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                       state.has("Vote Quimby Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Church Dumpster", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                     state.has_any(get_cars_by_height("SUV", 0, False, False), world.player) or \
                                                                                                     state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Dumpster Behind Krusty Burger Near School", lambda state: state.has_any(get_cars_by_height("Armored Truck", 1, False, False), world.player) or \
                                                                                                                               state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Back of School Roof", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Grocery Store Dumpster", lambda state: state.has_any(get_cars_by_height("WWII Vehicle", 0, False, False), world.player) or \
                                                                                                            state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Wiggum's", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Cletus' House", lambda state: state.has("Marge Progressive Jump", world.player, 2) or \
                                                                                                   (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                                    state.has("Marge Progressive Jump", world.player)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Big Bridge 2", lambda state: state.has("Marge Progressive Jump", world.player, 2) or \
                                                                                                  state.has_any(get_cars_by_height("SUV", 1, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Trailer Park", lambda state:  state.has("Marge Progressive Jump", world.player) or \
                                                                                                         state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Street Near Barn", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                                            state.has("Marge Progressive Jump", world.player)) or \
                                                                                                            state.has("Marge Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Power Plant Parking Lot 1", lambda state: state.has_any(get_cars_by_height("Armored Truck", 0, False, False), world.player) or \
                                                                                                               state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Street Near Simpsons' House", lambda state: (state.has("Marge Progressive Jump", world.player) and \
                                                                                                                        state.has_any(["Surveilance Van", "Itchy & Scratchy Movie Truck"], world.player) or \
                                                                                                                       (state.has("Marge Progressive Jump", world.player, 2) and \
                                                                                                                        state.has_any(get_cars_by_height("Vote Quimby Truck", 2, False, False), world.player))))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Nuclear Waste Bridge", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Outside Burns Mansion Gate", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Rocket Car", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Chessboard", lambda state: state.has_any(["Vote Quimby Truck", "Armored Truck", "Bonestorm Truck", "Burns Armored Truck", "Canyonero", "Cola Truck",
                                                                                                               "Compact Car", "Cube Van", "Duff Truck", "Fire Truck", "Fish Van", "Garbage Truck", "Glass Truck", "Hover Car",
                                                                                                               "Ice Cream Truck", "Itchy & Scratchy Movie Truck", "Milk Truck", "Mini School Bus", "Monorail Car", "Mr. Plow",
                                                                                                               "Nonuplets Minivan", "Nuclear Waste Truck", "Obliteratatron Big Wheel Truck", "Pickup Truck", "Pizza Van", "Plow King",
                                                                                                               "School Bus", "Speed Rocket", "SUV"], world.player) or\
                                                                                                state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Top of Krusty Burger Near Kwik-E-Mart", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Roof Across of House Across From Gold Mansion", lambda state: state.has("Marge Progressive Jump", world.player, 2) or \
                                                                                                                                   state.has_any(["Knight Boat", "ATV", "Ghost Ship", "Ferrini - Black",
                                                                                                                                                  "Open Wheel Race Car", "36 Stutz Bearcat", "Malibu Stacy Car",
                                                                                                                                                  "Ferrini - Red", "Sports Car A", "Sports Car B", "70's Sports Car",
                                                                                                                                                  "Coffin Car", "Planet Hype 50's Car", "Longhorn", "Curator", "Family Sedan",
                                                                                                                                                  "Chase Sedan", "Tractor", "Cell Phone Car", "Clown Car", "Moe's Sedan",
                                                                                                                                                  "Compact Car", "Hover Bike", "Witch Broom", "Electaurus", "Bandit", "Taxi",
                                                                                                                                                  "Globex Super Villain Car", "Station Wagon", "Limo", "Nerd Car", "Sedan A", "Sedan B",
                                                                                                                                                  "Krusty's Limo", "Skinner's Sedan", "Police Car", "El Carro Loco", "Hallo Hearse",
                                                                                                                                                  "Mr. Burns' Limo", "Kremlin", "Minivan", "Milk Truck", "Pickup", "Nonuplets Minivan",
                                                                                                                                                  "Nuclear Waste Truck", "Hover Car", "Honor Roller", "Car Built For Homer", "Hearse",
                                                                                                                                                  "WWII Vehicle", "WWII Vehicle w/ Rocket", "SUV", "Fish Van", "Donut Truck", "Canyonero",
                                                                                                                                                  "Book Burning Van", "Mr. Plow", "Bonestorm Truck", "Cube Van", "Zombie Car", "Speed Rocket",
                                                                                                                                                  "Burns Armored Truck", "Glass Truck", "Pizza Van", "Duff Truck", "Cola Truck", "Fire Truck",
                                                                                                                                                  "Surveillance Van"], world.player))

    # L5
    set_rule_if_location_exists(world, "(LVL 5) CARD - Construction Crane Platforming", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Moe's Roof", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - On Top of Train Across Water Tower", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Downtown Billboard Platforming", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Monorail Track", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Light Pole by Court House", lambda state: state.has_any(get_cars_by_height("Armored Truck", 0, False, False), world.player) or \
                                                                                                               state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Lion Statue", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Hospital Parking Lot", lambda state: (state.has("Apu Progressive Jump", world.player) or \
                                                                                                                             state.has_any(get_cars_by_height("SUV", 0, False, False), world.player)))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Stadium Behind Duff Mascot", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                state.has_any(["Garbage Truck", "Itchy and Scratchy Movie Truck"], world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Tree By Krusty Burger Downtown", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                     state.has_any(get_cars_by_height("36 Stutz Bearcat", 1, False, False), world.player)) or \
                                                                                                                     state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Monorail", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Corner of Monorail Station", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Downtown Krusty Float", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                              state.has_any(get_cars_by_height("Ferrini - Black", 1, False, False), world.player)) or\
                                                                                                                              state.has("Apu Progressive Jump", world.player, 2) or \
                                                                                                                              state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Downtown Highway Exit", lambda state: state.has("Apu Progressive Jump", world.player) or \
                                                                                                                 state.has_any(get_cars_by_height("Chase Sedan ", 1, False, False), world.player) or \
                                                                                                                 state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Helter Shelter", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                       state.has_any(get_cars_by_height("36 Stutz Bearcat", 1, False, False), world.player)) or \
                                                                                                                       state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Between DMV and Trainyard", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                            state.has_any(get_cars_by_height("Malibu Stacy Car", 1, False, False), world.player)) or \
                                                                                                                            state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Train Crossing", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Car Wash", lambda state: (state.has("Apu Progressive Jump", world.player, 1) or \
                                                                                                         state.has("Obliteratatron Big Wheel Truck", world.player)))
    set_rule_if_location_exists(world, "(LVL 5) CARD - On Top of Gas Station at Car Wash", lambda state: ((state.has("Apu Progressive Jump", world.player, 2) and \
                                                                                                                        state.has_any(get_cars_by_height("Zombie Car", 2, False, False), world.player))) or \
                                                                                                                       ((state.has("Apu Progressive Jump", world.player, 1) and \
                                                                                                                         state.has_any(get_cars_by_height("Surveillance Van", 1, False, False), world.player))))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Lexicon Bookstore Roof", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Legitimate Businessman's Roof 2", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Glen's Grocery Roof", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Stop Sign Across From Moe's", lambda state: state.has("Apu Progressive Jump", world.player) or  state.has("Armored Truck", world.player) or \
                                                                                                                 state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Under Construction Building Between Krusty Burger and Lard Lad's", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Gazebo Between Museum & Court House", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Hospital Sign", lambda state: state.has("Apu Progressive Jump", world.player) or \
                                                                                                   state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Police Station", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                     state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                     state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Tree Outside Police Station", lambda state: state.has("Apu Progressive Jump", world.player, 2) or \
                                                                                                         (state.has_any(get_cars_by_height("WWII Vehicle W\\ Rocket", 1, False, False), world.player) and \
                                                                                                          state.has("Apu Progressive Jump", world.player, 1)))
    set_rule_if_location_exists(world, "(LVL 5) CARD - King Toot's Music Store Roof", lambda state: state.has("Apu Progressive Jump", world.player))

    # L6
    set_rule_if_location_exists(world, "(LVL 6) CARD - Above Street by Ball Pit Gag", lambda state: (state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                                   state.has_any(get_cars_by_height("WWII Vehicle W\\ Rocket", 2, False, False), world.player)) or \
                                                                                                                   state.has_all(("Bart Progressive Jump", "Itchy and Scratchy Truck"), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Planet Hype Sign", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Atop Front of Boat", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Hidden in Bush Next to Kamp Krusty Well Exit", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Planet Hype Outdoor Seating", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Boulevard Near Krusty and Friends Billboard", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                                 state.has_any("Obliteratatron Big Wheel Truck, Garbage Truck, Itchy and Scratchy Movie Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Lumber King Billboard", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                           state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Box Near Gil", lambda state: lambda state: state.has("Bart Progressive Jump", world.player, 2)  or \
                                                                                                  state.has_any(get_cars_by_height("Mini School Bus", 0, False, False).remove("Monorail Car"), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Davey Jones Hamper", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                        state.has_any(get_cars_by_height("Burns Armored Truck", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Globex Ship Crane", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Globex Ship Inside Cargo Container", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 6) CARD - KrustyLu Studios Sign", lambda state: state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                                           (state.has_any("Garbage Truck, Itchy and Scratchy Movie Truck", world.player) and \
                                                                                                            state.has("Bart Progressive Jump", world.player)))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Behind KrustyLu Studios Sign", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                  state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Motel Awning", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Observatory 1", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Observatory 2", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                   state.has_any(["R/C Buggy", "ATV", "Hover Bike", "Witch Broom", "Coffin Car"], world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Kamp Krusty Weight Loss Center", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Boar's Head at Kamp Krusty", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Dam", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Parking Spot Across From Android's Dungeon", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                                state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Above Road Near Drain Pipe", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Captain Chum 'N' Stuff", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                     state.has_any(get_cars_by_height("Plow King", 0, False, False), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Upper Casino Entrance", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                           state.has_any(get_cars_by_height("Pickup Truck", 0, False, False), world.player) or \
                                                                                                           state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Duff Blimp", lambda state: state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                        (state.has("Bart Progressive Jump", world.player, 1) and \
                                                                                         state.has_any(get_cars_by_height("Zombie Car", 1, False, False), world.player)))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Barrels Near Gil", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                    state.has_any(
                                                                                                        ["Vote Quimby Truck", "Bonestorm Truck", "Burns Armored Truck", "Canyonero", "Cola Truck", "Cube Van",
                                                                                                         "Donut Truck",
                                                                                                         "Duff Truck", "Garbage Truck", "Hallo Hearse", "Hover Bike", "Hover Car", "Ice Cream Truck",
                                                                                                         "Itchy & Scratchy Movie Truck",
                                                                                                         "Monorail Car", "Longhorn", "Mr. Plow", "Nuclear Waste Truck", "Obliteratatron Big Wheel Truck",
                                                                                                         "Pickup Truck", "Pizza Van",
                                                                                                         "Plow King", "School Bus", "Speed Rocket", "SUV", "WWII Vehicle", "WWII Vehicle w/ Rocket", "Ambulance",
                                                                                                         "Armored Truck",
                                                                                                         "Car Built For Homer", "Compact Car", "Curator", "El Carro Loco", "Electaurus", "Fire Truck", "Fish Van",
                                                                                                         "Glass Truck", "Hearse",
                                                                                                         "Kremlin", "Krusty's Limo", "Limo", "Milk Truck", "Mini School Bus", "Minivan", "Moe's Sedan", "Nerd Car",
                                                                                                         "Nonuplets Minivan",
                                                                                                         "Pickup", "Police Car", "Sedan A", "Sedan B", "Skinner's Sedan", "Sports Car A", "Station Wagon",
                                                                                                         "Surveillance Van", "Taxi"], world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Concrete Mixer at Gas Station", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                     state.has_any(["Knight Boat", "ATV", "Open Wheel Race Car", "36 Stutz Bearcat", "Malibu Stacy Car",
                                                                                                                    "70's Sports Car", "Planet Hype 50's Car", "Longhorn", "Curator", "Chase Sedan",
                                                                                                                    "Tractor", "Cell Phone Car A", "Cell Phone Car B", "Cell Phone Car C",
                                                                                                                    "Cell Phone Car D", "Clown Car", "Moe's Sedan", "Hover Bike", "Bandit",
                                                                                                                    "Globex Super Villain Car", "Nerd Car", "Skinner's Sedan", "Police Car",
                                                                                                                    "El Carro Loco", "Hallo Hearse", "Mr. Burns' Limo", "Kremlin", "Hover Car",
                                                                                                                    "Car Built For Homer", "Hearse", "WWII Vehicle w/ Rocket", "SUV", "Fish Van",
                                                                                                                    "Donut Truck", "Canyonero", "Book Burning Van", "Mr. Plow", "Zombie Car",
                                                                                                                    "Speed Rocket", "Pizza Van", "School Bus", "Vote Quimby Truck", "Garbage Truck",
                                                                                                                    "Itchy & Scratchy Movie Truck"], world.player))

    # L7
    set_rule_if_location_exists(world, "(LVL 7) CARD - Flanders Bomb Shelter", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Blue House Haunted Playground",lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                                  state.has_any(get_cars_by_height("Longhorn", 1, False, False), world.player)) or \
                                                                                                                  state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - School Playground", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                       state.has_any(get_cars_by_height("Longhorn", 1, False, False), world.player)) or \
                                                                                                       state.has("Homer Progressive Jump", world.player, 2) or \
                                                                                                       state.has_any(["Itchy and Scratchy Movie Truck", "Garbage Truck", "Obliteratatron Big Wheel Truck"], world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Atop of Lard Lad", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Barn Silo", lambda state: state.has("Homer Progressive Jump", world.player, 2) or \
                                                                                                    (state.has("Itchy and Scratchy Movie Truck", world.player) and \
                                                                                                     state.has("Homer Progressive Jump", world.player)))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Mr. Burns Office", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Kwik-E-Mart's Dumpster", lambda state: state.has_any(get_cars_by_height("Krusty's Limo", 1, False, False), world.player) or \
                                                                                                            state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Krusty Burger's Dumpster", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                              state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Gas Station Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Street Between Simpsons' House and Kwik-E-Mart", lambda state: (state.has_any(get_cars_by_height("Malibu Stacy Car", 1, False, False), world.player) and \
                                                                                                                                           state.has("Homer Progressive Jump", world.player) or \
                                                                                                                                           state.has("Homer Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Retirement Castle", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                       state.has("Vote Quimby Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Church Dumpster", lambda state: state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) or \
                                                                                                   state.has("Obliteratatron Big Wheel Truck", world.player) or \
                                                                                                   state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Dumpster Behind Krusty Burger Near School", lambda state: state.has_any(get_cars_by_height("Armored Truck", 1, False, False), world.player) or \
                                                                                                                        state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Back of School Roof", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Grocery Store's Dumpster", lambda state: state.has_any(get_cars_by_height("WWII Vehicle", 1, False, False), world.player) or \
                                                                                                state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Wiggum's", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Cletus' House", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                    state.has_any(get_cars_by_height("SUV", 1, False, False), world.player)) or \
                                                                                                    state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Big Bridge", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                                 state.has("Homer Progressive Jump", world.player)) or \
                                                                                                 state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Trailer Park", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                        state.has("Obliteratatron Big Wheel Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Street Near Barn", lambda state: (state.has_any(get_cars_by_height("SUV", 1, False, False), world.player) and \
                                                                                                            state.has("Homer Progressive Jump", world.player)) or \
                                                                                                            state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Parking Lot 1", lambda state: (state.has_any(get_cars_by_height("Car Built For Homer", 1, False, False), world.player) and \
                                                                                                                state.has("Homer Progressive Jump", world.player)) or \
                                                                                                                state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Wreckage 1", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Wreckage 2", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Wreckage 3", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Burns' Office Chair", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Cemetery Crypt", lambda state: (state.has_any(get_cars_by_height("Ferrini - Red", 1, False, False), world.player) and \
                                                                                                     state.has("Homer Progressive Jump", world.player)) or \
                                                                                                     state.has("Homer Progressive Jump", world.player, 2) or \
                                                                                                     state.has("Garbage Truck", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Cemetery Tree", lambda state: state.has("Homer Progressive Jump", world.player, 2) and \
                                                                                                   state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Ghost", lambda state: state.has("Homer Progressive Jump", world.player, 2) and \
                                                                                            state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Top of Krusty Burger Near Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player))



def set_completion_condition(world: SimpsonsHitNRunWorld) -> None:
    wasps = world.options.Wasp_Amount
    cards = world.options.Card_Amount
    cars = world.options.Car_Amount

    if world.options.Itchy_And_Scratchy_Ticket_Requirement == 0:
        # all missions or story missions
        world.multiworld.completion_condition[world.player] = lambda state: can_reach_type_count(world, state, "WASP") >= wasps and \
                                                                            can_reach_type_count(world, state, "CARD") >= cards and \
                                                                            can_reach_missions(world, state)
    elif world.options.Itchy_And_Scratchy_Ticket_Requirement == 2:
        # final mission
        world.multiworld.completion_condition[world.player] = lambda state: can_reach_type_count(world, state, "WASP") >= wasps and \
                                                                            can_reach_type_count(world, state, "CARD") >= cards and \
                                                                            state.can_reach_region(f"Level 7 Missions", world.player)
    elif world.options.Itchy_And_Scratchy_Ticket_Requirement == 3:
        # num cars
        world.multiworld.completion_condition[world.player] = lambda state: can_reach_type_count(world, state, "WASP") >= wasps and \
                                                                            can_reach_type_count(world, state, "CARD") >= cards and \
                                                                            state.has_group("Cars", world.player, cars)

def can_reach_type_count(world: SimpsonsHitNRunWorld, state: CollectionState, type: str) -> int:
    count = 0
    for region in world.get_regions():
        for loc in list(region.locations):
            if f"{type} - " in loc.name and state.can_reach_location(loc.name, world.player):
                count += 1
    return count

def can_reach_missions(world: SimpsonsHitNRunWorld, state: CollectionState) -> bool:
    if "All" in world.options.Required_Mission_Levels:
        levels = range(1, 8)
    else:
        levels = world.options.Required_Mission_Levels

    for i in levels:
        for loc in world.get_region(f"Level {i} Missions").locations:
            name = loc.name
            if not world.options.Bonus_Mission_Required and "BM)" in name:
                continue

            if not world.options.Race_Mission_Required and "Race" in name:
                continue

            if not state.can_reach_location(loc.name, world.player):
                return False

    return True

def can_break_wasp(world: SimpsonsHitNRunWorld, state: CollectionState, character: str, any_car_wasps: list[str], bad_cars: list[str], jumps: int = 1) -> bool:
    return (state.has(f"{character} Progressive Jump", world.player, jumps) and state.has(f"{character} Attack", world.player)) or \
           (state.has(f"{character} Frink-o-Matic Wasp Bumper", world.player) and \
            state.has_any([car for car in any_car_wasps if car not in bad_cars],
            world.player))

def get_cars_by_height(car: str, jumps: int, driving: bool, wall: bool):
    #print(car)

    if driving:
        cars = car_names_by_driving_height
    elif jumps == 1 or jumps == 0:
        #if not wall:
        #    cars = car_names_by_single_jump_height
        #else:
            cars = car_names_by_single_jump_height_with_wall
    elif jumps == 2:
        cars = car_names_by_double_jump_height


    for i, name in enumerate(cars):
        if name == car:
            #print(cars[i:])
            return cars[i:]

    #print(cars)
    #print(car + " failed")
    return []






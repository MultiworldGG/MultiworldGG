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
any_car = small_cars + medium_cars + large_cars
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
                                                                                                 "School Bus", "Donut Truck", "Nerd Car", "Canyonero", "Clown Car", "Kermlin",
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
    set_rule(world.get_location("(LVL 1) WASP - Lard Lads Roof"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - School Yard Bus"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - School Roof 1"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - School Roof 2"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Top of Tower Before Broken Bridge"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Trailer Park 2"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 1) WASP - Atop of Bridge Framework 1"), lambda state: state.has_all((["Homer Progressive Jump", "Homer Attack"] + large_cars), world.player) or \
                                                                                            state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 1) WASP - Atop of Bridge Framework 2"), lambda state: state.has_all((["Homer Progressive Jump", "Homer Attack"] + large_cars), world.player) or \
                                                                                            state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))

    #if "All" in world.options.Shuffle_Bumpers or "Homer" in world.options.Shuffle_Bumpers:
    set_rule(world.get_location("(LVL 1) WASP - Next to the Blue House Besides Simpsons House"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 1) WASP - Back Door of School"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                        ["Honor Roller", "Malibu Stacy Car", "Ferrini - Red",
                                                                                                         "Bandit", "Open Wheel Race Car", "Ferrini - Black"], 0))
    set_rule(world.get_location("(LVL 1) WASP - StoneCutters Table 1"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, []))
    set_rule(world.get_location("(LVL 1) WASP - StoneCutters Table 2"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, []))
    set_rule(world.get_location("(LVL 1) WASP - Rocket Car"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps, ["ATV", "Obliteratatron Big Wheel Truck"], 0))
    set_rule(world.get_location("(LVL 1) WASP - Barn Haystack"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                 ["Family Sedan", "Malibu Stacy Car", "Nerd Car",
                                                                                                            "Open Wheel Race Car", "Hover Bike", "Coffin Car"]))
    set_rule(world.get_location("(LVL 1) WASP - Trailer Park 1"), lambda state: can_break_wasp(world, state, "Homer", any_car_wasps,
                                                                                                   ["Nerd Car", "70's Sports Car", "Open Wheel Race Car"], 0))
    #else:
    #    set_rule(world.get_location("(LVL 1) WASP - Next to the Blue House Besides Simpsons House"), lambda state: state.has("Homer Attack", world.player))
    #    set_rule(world.get_location("(LVL 1) WASP - Back Door of School"), lambda state: state.has("Homer Attack", world.player))
    #    set_rule(world.get_location("(LVL 1) WASP - Rocket Car"), lambda state: state.has("Homer Attack", world.player))
    #    set_rule(world.get_location("(LVL 1) WASP - StoneCutters Table 1"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    #    set_rule(world.get_location("(LVL 1) WASP - StoneCutters Table 2"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    #    set_rule(world.get_location("(LVL 1) WASP - Barn Haystack"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    #    set_rule(world.get_location("(LVL 1) WASP - Trailer Park 1"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))

    # L2
    set_rule(world.get_location("(LVL 2) WASP - Roof Across Monkey Building"), lambda state: state.has("Bart Attack", world.player) and \
                                                                                             state.has_any(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Monorail Stairs"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 2) WASP - Upstair Beside Monorail"), lambda state: state.has_all(("Bart Attack", "Bart Progressive Jump"), world.player) or \
                                                                                         (state.has("Bart Attack", world.player) and \
                                                                                          state.has_any(medium_cars + large_cars, world.player)))
    set_rule(world.get_location("(LVL 2) WASP - Roof Across Monorail"), lambda state: state.has_all_counts({"Bart Attack" : 1, "Bart Progressive Jump" : 2}, world.player))
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

    #if "All" in world.options.Shuffle_Bumpers or "Bart" in world.options.Shuffle_Bumpers:
    set_rule(world.get_location("(LVL 2) WASP - CourtHouse Steps"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
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
    set_rule(world.get_location("(LVL 2) WASP - Inside Trainyard Parking Spot"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 2) WASP - Car Wash"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
                                                                                             ["Family Sedan", "Moe's Sedan", "Longhorn", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                        "Globex Super Villain Car", "70's Sports Car", "Open Wheel Race Car", "Zombie Car",
                                                                                                        "Hover Bike", "Knight Boat", "Coffin Car", "Ghost Ship", "Ferrini - Black"], 0))
    #else:
    #    set_rule(world.get_location("(LVL 2) WASP - CourtHouse Steps"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Gazebo Between Museum and Courthouse"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Museum Steps"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Hospital Front Yard"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Town Hall (Front)"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Town Hall (Back)"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Behind Downtown Krusty Burger"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Inside Trainyard Parking Spot"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 2) WASP - Car Wash"), lambda state: state.has("Bart Attack", world.player))

    # L3
    set_rule(world.get_location("(LVL 3) WASP - Observatory"), lambda state: state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Planet Hype"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Broken Railing Below Dam"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Broken Railing Above Dam (Exit)"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Kamp Krusty Well"), lambda state: state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Kamp Krusty Near Stage"), lambda state: state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Krusty Studio Left"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Krusty Studio Right"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    set_rule(world.get_location("(LVL 3) WASP - Bowling Rooftop"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player) or \
                                                                                state.has_any(large_cars, world.player) and state.has("Lisa Attack", world.player))
    set_rule(world.get_location("(LVL 3) WASP - Comic Book Guy Rooftop"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))

    #if "All" in world.options.Shuffle_Bumpers or "Lisa" in world.options.Shuffle_Bumpers:
    set_rule(world.get_location("(LVL 3) WASP - Exit of Kamp Krusty's Well"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps, ["ATV"], 0))
    set_rule(world.get_location("(LVL 3) WASP - Motel Complex"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
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
    set_rule(world.get_location("(LVL 3) WASP - LightHouse"), lambda state: can_break_wasp(world, state, "Lisa", any_car_wasps,
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


    #else:
    #    set_rule(world.get_location("(LVL 3) WASP - Exit of Kamp Krusty's Well"), lambda state: state.has("Lisa Attack", world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Motel Complex"), lambda state: state.has("Lisa Attack", world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Duff Brewery Behind Krusty Glass"), lambda state: state.has("Lisa Attack", world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Duff Blimp 1"), lambda state: state.has("Lisa Attack", world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Duff Blimp 2"), lambda state: state.has("Lisa Attack", world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Globex Ship Front End"), lambda state: state.has("Lisa Attack", world.player) and state.has_any(any_car_wasps, world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Globex Ship Next to the Crane"), lambda state: state.has("Lisa Attack", world.player) and state.has_any(any_car_wasps, world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Globex Ship Stairs"), lambda state: state.has("Lisa Attack", world.player) and state.has_any(any_car_wasps, world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - LightHouse"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))
    #    set_rule(world.get_location("(LVL 3) WASP - Beach"), lambda state: state.has_all(("Lisa Attack", "Lisa Progressive Jump"), world.player))

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
    set_rule(world.get_location("(LVL 4) WASP - Outside of Homer's Workstation"), lambda state: state.has_all(("Marge Progressive Jump", "Marge Attack"), world.player))

    #if "All" in world.options.Shuffle_Bumpers or "Marge" in world.options.Shuffle_Bumpers:
    set_rule(world.get_location("(LVL 4) WASP - Blue House Before Krusty Glass 1"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                     ["Malibu Stacy Car", "Nerd Car", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                                                "Bandit", "Open Wheel Race Car", "Hover Bike", "Ferrini - Black"],
                                                                                                                     0))
    set_rule(world.get_location("(LVL 4) WASP - Blue House Before Krusty Glass 2"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                     ["Malibu Stacy Car", "Nerd Car", "Ferrini - Red", "36 Stutz Bearcat",
                                                                                                                                "Bandit", "Open Wheel Race Car", "Hover Bike", "Ferrini - Black"],
                                                                                                                     0))
    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns Giant ChessBoard 1"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns Giant ChessBoard 2"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps, [], 0))
    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns StairCase"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
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
                                                                                                                                "Station Wagon", "Ice Cream Truck", "Cell Phone Car", "Cube Van",
                                                                                                                                "Milk Truck", "Nonuplets Minivan", "Obliteratatron Big Wheel Truck"],
                                                                                                                     0))
    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns Library"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
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
                                                                                                         "Station Wagon", "Ice Cream Truck", "Cell Phone Car", "Cube Van",
                                                                                                         "Milk Truck", "Nonuplets Minivan", "Obliteratatron Big Wheel Truck"],
                                                                                                        0))
    set_rule(world.get_location("(LVL 4) WASP - In Trailer Park"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps, ["Open Wheel Race Car"], 0))
    set_rule(world.get_location("(LVL 4) WASP - Behind School Steps"), lambda state: can_break_wasp(world, state, "Marge", any_car_wasps,
                                                                                                                   ["ATV"], 0))
    #else:
    #    set_rule(world.get_location("(LVL 4) WASP - Blue House Before Krusty Glass 1"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Blue House Before Krusty Glass 2"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns Giant ChessBoard 1"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns Giant ChessBoard 2"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns StairCase"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Mr. Burns Library"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Outside of Homer's Workstation"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - In Trailer Park"), lambda state: state.has("Marge Attack", world.player))
    #    set_rule(world.get_location("(LVL 4) WASP - Behind School Steps"), lambda state: state.has("Marge Attack", world.player))

    # L5
    set_rule(world.get_location("(LVL 5) WASP - Rooftop Next to Moes"), lambda state: (state.has_all_counts({"Apu Progressive Jump": 1, "Apu Attack": 1}, world.player) and \
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
    set_rule(world.get_location("(LVL 5) WASP - Otherside of Monorail 1"), lambda state: state.has_all_counts({"Apu Progressive Jump" : 2, "Apu Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Otherside of Monorail 2"), lambda state: state.has_all_counts({"Apu Progressive Jump" : 2, "Apu Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Fountain Near Stadium"), lambda state: (state.has_all_counts({"Apu Progressive Jump": 1, "Apu Attack": 1}, world.player) and \
                                                                                                     state.has_any(large_cars, world.player)) or \
                                                                                                    state.has_all_counts({"Apu Progressive Jump": 2, "Apu Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 5) WASP - Alleyway Rooftop"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))

    #if "All" in world.options.Shuffle_Bumpers or "Apu" in world.options.Shuffle_Bumpers:
    set_rule(world.get_location("(LVL 5) WASP - Front of Hospital"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
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
    set_rule(world.get_location("(LVL 5) WASP - Under Giant Purple Beams 1"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                         ["Electaurus", "Malibu Stacy Car", "Curator", "Longhorn", "El Carro Loco",
                                                                                                          "Ferrini - Red", "Globex Super Villain Car", "ATV", "Open Wheel Race Car", "Hover Bike",
                                                                                                          "ATV", "Compact Car", "Ferrini - Black"],
                                                                                                         1))
    set_rule(world.get_location("(LVL 5) WASP - Under Giant Purple Beams 2"), lambda state: can_break_wasp(world, state, "Apu", any_car_wasps,
                                                                                                               ["Electaurus", "Malibu Stacy Car", "Curator", "Longhorn", "El Carro Loco",
                                                                                                                "Ferrini - Red", "Globex Super Villain Car", "ATV", "Open Wheel Race Car", "Hover Bike",
                                                                                                                "ATV", "Compact Car", "Ferrini - Black"],
                                                                                                               1))

    #else:
    #    set_rule(world.get_location("(LVL 5) WASP - Front of Hospital"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Gazebo Between Museum & Court House"), lambda state: state.has("Apu Attack", world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Steps of Town Hall"), lambda state: state.has("Apu Attack", world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Museum Steps"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Police Station Steps"), lambda state: state.has("Apu Attack", world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Under Giant Purple Beams 1"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Under Giant Purple Beams 2"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))
    #    set_rule(world.get_location("(LVL 5) WASP - Alleyway Rooftop"), lambda state: state.has_all(("Apu Progressive Jump", "Apu Attack"), world.player))

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
    set_rule(world.get_location("(LVL 6) WASP - Bowling Rooftop"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Comic Book Guy Rooftop 1"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))
    set_rule(world.get_location("(LVL 6) WASP - Comic Book Guy Rooftop 2"), lambda state: state.has_all(("Bart Progressive Jump", "Bart Attack"), world.player))

    #if "All" in world.options.Shuffle_Bumpers or "Bart" in world.options.Shuffle_Bumpers:
    set_rule(world.get_location("(LVL 6) WASP - Motel"), lambda state: can_break_wasp(world, state, "Bart", any_car_wasps,
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


    #else:
    #    set_rule(world.get_location("(LVL 6) WASP - Motel"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 6) WASP - Duff Brewery Krusty Glass"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 6) WASP - Under Duff Blimp"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 6) WASP - Globex Ship Crane"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 6) WASP - Globex Ship Staircase 1"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 6) WASP - Globex Ship Staircase 2"), lambda state: state.has("Bart Attack", world.player))
    #    set_rule(world.get_location("(LVL 6) WASP - Lighthouse"), lambda state: state.has("Bart Attack", world.player))

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
    set_rule(world.get_location("(LVL 7) WASP - Bridge Frame by Cletus"), lambda state: state.has_all((["Homer Progressive Jump", "Homer Attack"] + large_cars), world.player) or \
                                                                                        state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - TrailerPark 1"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
    set_rule(world.get_location("(LVL 7) WASP - TrailerPark 2"), lambda state: (state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player) and \
                                                                                     state.has_any(large_cars, world.player)) or \
                                                                                     state.has_all_counts({"Homer Progressive Jump" : 2, "Homer Attack" : 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - Barn Silo"), lambda state: state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))
    set_rule(world.get_location("(LVL 7) WASP - Mr. Burns Office"), lambda state: state.has_all_counts({"Homer Progressive Jump": 2, "Homer Attack": 1}, world.player))

    #if "All" in world.options.Shuffle_Bumpers or "Homer" in world.options.Shuffle_Bumpers:
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
    #else:
        #set_rule(world.get_location("(LVL 7) WASP - Blue House Haunted Playground"), lambda state: state.has_all(("Homer Progressive Jump", "Homer Attack"), world.player))
        #set_rule(world.get_location("(LVL 7) WASP - Bridge Barricade"), lambda state: state.has("Homer Attack", world.player))
        #set_rule(world.get_location("(LVL 7) WASP - Power Plant Parking lot"), lambda state: state.has("Homer Attack", world.player))

    # Cards
    # L1
    set_rule_if_location_exists(world, "(LVL 1) CARD - Simpsons' Backyard", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Kwik-E-Mart Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Wiggum's Backyard", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above StoneCutters Table", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Highest Platform in Power Plant", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Trailer Park", lambda state: (state.has("Homer Progressive Jump", world.player)))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Neighbor's Carport", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Kwik-E-Mart", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                        state.has_any(large_cars, world.player)) or \
                                                                                                        state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Kwik-E-Mart's Dumpster", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                             state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                             state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Krusty Burger's Dumpster", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                                state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                                state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Gas Station Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Street Between Simpsons' House and Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player, 2) and \
                                                                                                                                          state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Retirement Castle", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                       state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Church Dumpster", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                     state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Dumpster Behind Krusty Burger Near School", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                                               state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Back of School Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Grocery Store's Dumpster", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                              state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - House Across From Simpsons' House 1", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                                         state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Wiggum's", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                    state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Cletus' House", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                    state.has_any(large_cars, world.player)) or \
                                                                                                    state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Big Bridge", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Trailer Park", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                        state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Street Near Barn", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                            state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Power Plant Parking Lot 1", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                               state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Street Near Simpsons' House", lambda state: state.has("Homer Progressive Jump", world.player, 2) and \
                                                                                                                       state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Above Nuclear Waste Bridge", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                                 state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Roof Across of House Across From Gold Mansion", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Outside Burns Mansion Gate", lambda state: state.has_any(large_cars, world.player) or \
                                                                                                                state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 1) CARD - Rocket Car", lambda state: state.has_any(large_cars, world.player) or state.has("Homer Progressive Jump", world.player))

    # L2
    set_rule_if_location_exists(world, "(LVL 2) CARD - Statue", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Roof Across Monkey Building", lambda state: state.has_any(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Legitimate Businessman's Roof", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Car Wash", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                               state.has_any(large_cars, world.player) or \
                                                                                               state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Train Wagon", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Fountain At Stadium", lambda state: state.has_all(("Bart Progressive Jump", "Itchy and Scratchy Movie Truck"), world.player) or \
                                                                                                         state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Light Pole by Court House", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                                state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Lion Statue", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Hospital Parking Lot", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                             state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                                             state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Town Hall (Stadium Side)", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Stadium Behind Duff Mascot", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                         state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                         state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Tree By Krusty Burger Downtown", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                     state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                                     state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Monorail", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Corner of Monorail Station", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Downtown Krusty Float", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                                              state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                                              state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Downtown Highway Exit", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Helter Shelter", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Tree By Krusty Burger Downtown", lambda state: state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                                    state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Between DMV and Trainyard", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Train Crossing", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Above Street Near Car Wash", lambda state: state.has("Bart Progressive Jump", world.player) and \
                                                                                                                state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - On Top of Gas Station at Car Wash", lambda state: state.has_all_counts({"Bart Progressive Jump" : 2,
                                                                                                                            "Itchy and Scratchy Movie Truck" : 1}, world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Lexicon Bookstore Roof", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Legitimate Businessman's Roof 2", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Glen's Grocery Roof", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Street Near Construction", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Hospital Sign", lambda state: (state.has("Bart Progressive Jump", world.player) and \
                                                                                                    state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                    state.has("Bart Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 2) CARD - Tree Outside Police Station", lambda state: state.has("Bart Progressive Jump", world.player))

    # L3
    set_rule_if_location_exists(world, "(LVL 3) CARD - Comic Book Guy's Rooftop", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Above Bowling", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Atop Lighthouse", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Krusty Studio Balcony", lambda state: (state.has("Lisa Progressive Jump", world.player) and \
                                                                                                               state.has_any(large_cars, world.player) or \
                                                                                                               state.has("Lisa Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Beside Broken Bridge", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Edge of Globex Ship", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Planet Hype Outdoor Seating", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Deck by Squidport Pedestrian Entrance 1", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                             state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Deck by Squidport Pedestrian Entrance 2", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                             state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Gated Houses Near Aztec Theater", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                     state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Boulevard Near Krusty and Friends Billboard", lambda state: (state.has("Lisa Progressive Jump", world.player) and \
                                                                                                                                  state.has_any(large_cars, world.player) or \
                                                                                                                                  state.has("Lisa Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Concrete Mixer at Gas Station", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Lumber King Billboard", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Box Near Gil", lambda state: state.has("Lisa Progressive Jump", world.player, 2) and \
                                                                                                  state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Squidport Undercover Police Dumpster", lambda state: (state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                           state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                                           state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Davey Jones Hamper", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Globex Ship Crane", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Globex Ship Inside Cargo Container", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 2) CARD - KrustyLu Studios Sign", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Behind KrustyLu Studios Sign", lambda state: state.has("Lisa Progressive Jump", world.player) or \
                                                                                                                  state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Motel Awning", lambda state: state.has("Lisa Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Observatory 1", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Observatory 2", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Kamp Krusty Weight Loss Center", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Boar's Head at Kamp Krusty", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Dam", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Parking Spot Across From Android's Dungeon", lambda state: (state.has("Lisa Progressive Jump", world.player) and \
                                                                                                                                 state.has_any(large_cars, world.player) or \
                                                                                                                                 state.has("Lisa Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Above Road Near Drain Pipe", lambda state: (state.has("Lisa Progressive Jump", world.player) and \
                                                                                                                 state.has_any(large_cars, world.player) or \
                                                                                                                 state.has("Lisa Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Captain Chum 'N' Stuff", lambda state: state.has("Lisa Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 3) CARD - Upper Casino Entrance", lambda state: state.has("Lisa Progressive Jump", world.player))

    # L4
    set_rule_if_location_exists(world, "(LVL 4) CARD - Gas Station Roof 1", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Burns Mansion Secret", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Big Bridge", lambda state: ((state.has("Marge Progressive Jump", world.player) and \
                                                                                                 state.has_any(large_cars, world.player)) or \
                                                                                                 state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Atop Tower Before Broken Bridge", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Roof of House Across From Gold Mansion", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Simpsons' Tree House", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - End of Trailer Park", lambda state: ((state.has("Marge Progressive Jump", world.player) and \
                                                                                                          state.has_any(large_cars, world.player)) or \
                                                                                                          state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Road Near Drain Pipe", lambda state: ((state.has("Marge Progressive Jump", world.player) and \
                                                                                                                 state.has_any(large_cars, world.player)) or \
                                                                                                                 state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Kwik-E-Mart's Dumpster", lambda state: state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                      state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Krusty Burger Dumpster", lambda state: state.has_any(medium_cars + large_cars, world.player) or\
                                                                                                            state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Gas Station Roof 2", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Street Between Simpson's House and Kwik-E-Mart", lambda state: (state.has("Marge Progressive Jump", world.player) and \
                                                                                                                                           state.has_any(large_cars, world.player) or \
                                                                                                                                           state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Retirement Castle", lambda state: (state.has("Marge Progressive Jump", world.player) and \
                                                                                                         state.has_any(large_cars, world.player) or \
                                                                                                         state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Church Dumpster", lambda state: (state.has("Marge Progressive Jump", world.player) and \
                                                                                                      state.has_any(large_cars, world.player) or \
                                                                                                      state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Dumpster Behind Krusty Burger Near School", lambda state: (state.has("Marge Progressive Jump", world.player) and \
                                                                                                                                state.has_any(large_cars, world.player) or \
                                                                                                                                state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Back of School Roof", lambda state: state.has("Marge Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Grocery Store Dumpster", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                            state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Wiggum's", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                    state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Cletus' House", lambda state: (state.has("Marge Progressive Jump", world.player) and \
                                                                                                    state.has_any(large_cars, world.player) or \
                                                                                                    state.has("Marge Progressive Jump", world.player, 2)))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Big Bridge 2", lambda state: state.has("Marge Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Trailer Park", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                        state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Street Near Barn", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                            state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Power Plant Parking Lot 1", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                               state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Street Near Simpsons' House", lambda state: state.has("Marge Progressive Jump", world.player, 2) and \
                                                                                                                       state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Above Nuclear Waste Bridge", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                                state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Outside Burns Mansion Gate", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                                state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Rocket Car", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 4) CARD - Chessboard", lambda state: state.has("Marge Progressive Jump", world.player) or \
                                                                                                state.has_any(large_cars, world.player))

    # L5
    set_rule_if_location_exists(world, "(LVL 5) CARD - Construction Crane Platforming", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Moe's Roof", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - On Top of Train Across Water Tower", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Downtown Billboard Platforming", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Monorail Track", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Courthouse Light Pole", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                            state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                            state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Lion Statue", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Hospital Parking Lot", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                             state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                                             state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Stadium Behind Duff Mascot", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                 state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                                 state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Tree By Krusty Burger Downtown", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                     state.has_any(medium_cars, world.player)) or\
                                                                                                                     state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Monorail", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Corner of Monorail Station", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Downtown Krusty Float", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Downtown Highway Exit", lambda state: state.has("Apu Progressive Jump", world.player) or \
                                                                                                                 state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Helter Shelter", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Between DMV and Trainyard", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Train Crossing", lambda state: state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Above Street Near Car Wash", lambda state: state.has("Apu Progressive Jump", world.player) or \
                                                                                                                state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - On Top of Gas Station at Car Wash", lambda state: state.has_all_counts({"Apu Progressive Jump" : 2,
                                                                                                                         "Itchy and Scratchy Movie Truck" : 1}, world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Lexicon Bookstore Roof", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Legitimate Businessman's Roof 2", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Glen's Grocery Roof", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Stop Sign Across From Moe's", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Under Construction Building Between Krusty Burger and Lard Lad's", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Gazebo Between Museum & Court House", lambda state: state.has("Apu Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Hospital Sign", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                    state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                    state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Police Station", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                     state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                     state.has("Apu Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 5) CARD - Tree Outside Police Station", lambda state: (state.has("Apu Progressive Jump", world.player) and \
                                                                                                                  state.has_any(medium_cars + large_cars, world.player)) or\
                                                                                                                  state.has("Apu Progressive Jump", world.player, 2))

    # L6
    set_rule_if_location_exists(world, "(LVL 6) CARD - Above Street BallPit House", lambda state: (state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                                state.has_any(large_cars, world.player)) or \
                                                                                                                state.has_all(("Bart Progressive Jump", "Itchy and Scratchy Truck"), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Planet Hype Sign", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Atop Front of Boat", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Hidden in Bush Next to Kamp Krusty Well Exit", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Planet Hype Outdoor Seating", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Deck by Squidport Pedestrian Entrance 1", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                             state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Deck by Squidport Pedestrian Entrance 2", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                             state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Gated Houses Near Aztec Theater", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                     state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Boulevard Near Krusty and Friends Billboard", lambda state: state.has("Bart Progressive Jump", world.player, 2) or \
                                                                                                                                 state.has_all(("Bart Progressive Jump", "Itchy and Scratchy Truck"), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Lumber King Billboard", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Box Near Gil", lambda state: state.has("Bart Progressive Jump", world.player, 2) and \
                                                                                                  state.has_any(medium_cars + large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Squidport Undercover Police Dumpster", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                          state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Davey Jones Hamper", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Globex Ship Crane", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Globex Ship Inside Cargo Container", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - KrustyLu Studios Sign", lambda state: state.has("Bart Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Behind KrustyLu Studios Sign", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                  state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Motel Awning", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Observatory 1", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Observatory 2", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Kamp Krusty Weight Loss Center", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Boar's Head at Kamp Krusty", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Dam", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Parking Spot Across From Android's Dungeon", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                                state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Above Road Near Drain Pipe", lambda state: state.has("Bart Progressive Jump", world.player) or \
                                                                                                                state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Captain Chum 'N' Stuff", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Upper Casino Entrance", lambda state: state.has("Bart Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 6) CARD - Duff Blimp", lambda state: state.has("Bart Progressive Jump", world.player, 2))

    # L7
    set_rule_if_location_exists(world, "(LVL 7) CARD - Flanders Bomb Shelter", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Blue House Haunted Playground", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                        state.has_any(medium_cars + large_cars, world.player)) or \
                                                                                                        state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - School Playground", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                        state.has_any(large_cars, world.player)) or \
                                                                                                        state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Atop of Lard Lad", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Barn Silo", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Mr. Burns Office", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                   state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Kwik-E-Mart's Dumpster", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                            state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Krusty Burger's Dumpster", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                              state.has_any((medium_cars + large_cars), world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Gas Station Roof", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Street Between Simpsons' House and Kwik-E-Mart", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                                                          state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Retirement Castle", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                       state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Church Dumpster", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                     state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Dumpster Behind Krusty Burger Near School", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                                               state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Back of School Roof", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Grocery Store's Dumpster", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                              state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Wiggum's", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                    state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Cletus' House", lambda state: (state.has("Homer Progressive Jump", world.player) and \
                                                                                                    state.has_any(large_cars, world.player)) or \
                                                                                                    state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Big Bridge", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Trailer Park", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                        state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Above Street Near Barn", lambda state: state.has("Homer Progressive Jump", world.player) or \
                                                                                                            state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Parking Lot 1", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Parking Lot 2", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Wreckage 1", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Wreckage 2", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Power Plant Wreckage 3", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Burns' Office Chair", lambda state: state.has("Homer Progressive Jump", world.player, 2))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Cemetery Crypt", lambda state: state.has("Homer Progressive Jump", world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Cemetery Tree", lambda state: state.has("Homer Progressive Jump", world.player, 2) and \
                                                                                                   state.has_any(large_cars, world.player))
    set_rule_if_location_exists(world, "(LVL 7) CARD - Ghost", lambda state: state.has("Homer Progressive Jump", world.player, 2) and \
                                                                                            state.has_any(large_cars, world.player))



def set_completion_condition(world: SimpsonsHitNRunWorld) -> None:
    wasps = world.options.Wasp_Amount
    cards = world.options.Card_Amount
    cars = world.options.Car_Amount

    if world.options.Itchy_And_Scratchy_Ticket_Requirement == 0 or world.options.Itchy_And_Scratchy_Ticket_Requirement == 1:
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
            if not state.can_reach_location(loc.name, world.player):
                return False

    return True

def can_break_wasp(world: SimpsonsHitNRunWorld, state: CollectionState, character: str, any_car_wasps: list[str], bad_cars: list[str], jumps: int = 1) -> bool:
    return (state.has(f"{character} Progressive Jump", world.player, jumps) and state.has(f"{character} Attack", world.player)) or \
           (state.has(f"{character} Frink-o-Matic Wasp Bumper", world.player) and \
            state.has_any([car for car in any_car_wasps if car not in bad_cars],
            world.player))


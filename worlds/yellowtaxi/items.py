from __future__ import annotations

import math
from typing import TYPE_CHECKING, List

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
    from .world import YellowTaxiWorld

ITEM_NAME_TO_ID = {
    "Gear": 1,
    "Bunny (Morio's Lab)": 2_00,
    "Bunny (Bombeach)": 2_01,
    "Bunny (Pizza Time)": 2_02,
    "Bunny (Morio's Home)": 2_03,
    "Bunny (Arcade Panik)": 2_04,
    "Bunny (Tosla's Offices)": 2_05,
    "Bunny (Gym Gears)": 2_06,
    "Bunny (Fecal Matters)": 2_07,
    "Bunny (Flushed Away)": 2_08,
    "Bunny (Maurizio's City)": 2_09,
    "Bunny (Crash Test Industries)": 2_10,
    # "Bunny (Demo)": 2_11,
    "Bunny (Morio's Mind)": 2_12,
    "Bunny (Ruined Observatory)": 2_13,
    "Bunny (Tosla HQ)": 2_14,
    "Bunny (Moon)": 2_15,
    "1 Coin": 3,
    "10 Coins": 4,
    "25 Coins": 5,
    "100 Coins": 6,
    # Hats reserve 7_00
    "No Hat": 7_00,
    "Propeller Cap": 7_01,
    "Top Hat": 7_02,
    "Morio Hat": 7_03,
    "Taxi Stack Hat": 7_04,
    "Bomb Hat": 7_05,
    "Drink Hat": 7_06,
    "Chef Hat": 7_07,
    "Spaghetti Hat": 7_08,
    "Pot Hat": 7_09,
    "Lasagna Hat": 7_10,
    "Joystick Hat": 7_11,
    "Slot Machine Hat": 7_12,
    "Gelatin Hat": 7_13,
    "Mug Hat": 7_14,
    "Tosla Employee Hat": 7_15,
    "Flexing Hat": 7_16,
    "Syringe Hat": 7_17,
    "Poop Hat": 7_18,
    "Dog Bowl Hat": 7_19,
    "Toilet Hat": 7_20,
    "Bone Fish Hat": 7_21,
    "Spoiler": 7_22,
    "Police Lights": 7_23,
    "Captain Abs-urd Hat": 7_24,
    "Roid-Man Hat": 7_25,
    "Buzzsaw Hat": 7_26,
    "Crusher Hat": 7_27,
    "Morio's Brain Hat": 7_28,
    "Heart Hat": 7_29,
    "Moon Globe Hat": 7_30,
    "Tower Hat": 7_31,
    "Alien Mosk (Evil) Hat": 7_32,
    "Skeleton Taxi Skin": 7_33,
    "Golden Taxi Skin": 7_34,
    "Orbit Hat": 7_35,
    "Satellite Dish Hat": 7_36,
    "Alien Mosk (Good) Hat": 7_37,
    "Crash Test Dummy Hat": 7_38,
    "Dentures Hat": 7_39,
    "Mushroom Cloud Hat": 7_40,
    "Gym Bros Hat": 7_41,
    "Banana Hat": 7_42,
    "Bunny Hat": 7_43,
    "Inception Top Hat": 7_44,
    "Pizza Man Hat": 7_45,
    "Toilet Paper Hat": 7_46,
    "Pod Hat": 7_47,
    "Paper Boat Hat": 7_48,
    "Prototype Taxi Skin": 7_49,
    "Glitched Taxi Skin": 7_50,
    "TV Hat": 7_51,
    "Burger Hat": 7_52,
    #"Flip-O-Will": 8_0_0, # Not actually adding this at the moment, not interesting standalone
    "Progressive Jump": 8_0_1,
    "Progressive Boost": 8_0_2,
    "Spin Attack": 8_0_3,
    "Glide": 8_0_4,
    "Golden Spring Blueprints": 8_1_0,
    "Golden Propeller Blueprints": 8_2_0,
    "Pizza Wheels": 8_9_9,
    "Lab Key": 10_00,
    "Gym Membership": 10_06,
    "Doggo": 10_07,
    "Sewer Key": 10_08,
    "Mosk's Rocket": 10_16,
    "Time Trial Remote (Baby Steps!)": 10_17,
    "Time Trial Remote (Getting Gud!)": 10_18,
    "Time Trial Remote (Pro Tricks!)": 10_19,
    "Hat World Membership": 10_99,
    "Morio's Wardrobe": 11_00,
    "Gela-Toni": 11_01,
    "Pizza King": 11_02,
    "Orange Switch": 11_10,
    "Full Game Unlock": 11_11,
    "Morio's Password": 11_12,
    "Time Trial Remote": 11_17,
    "Progressive Time Trial Remote": 11_18,
    "Psycho Taxi Cartridge": 20_01,
    "Michele": 20_02,
    # Traps
    "Burger Hat Trap": 666_000,
    "Cutscene Trap": 666_001,
    "Explosion Trap": 666_002,
    "Fast Trap": 666_003,
    "Invisible Trap": 666_004,
    "Literature Trap": 666_005,
    "No Hat Trap": 666_006,
    "Phone Trap": 666_007,
    "Pixelate Trap": 666_008,
    "Screen Flip Trap": 666_009,
    "Slip Trap": 666_010,
    "Slow Trap": 666_011,
    "Spam Trap": 666_012,
    "Stun Trap": 666_013,
    "Timer Trap": 666_014,
    "Whirlpool Trap": 666_015,

    "Progressive Jump (Hub)": 777_00_0_1,
    "Progressive Boost (Hub)": 777_00_0_2,
    "Progressive Jump (Bombeach)": 777_01_0_1,
    "Progressive Boost (Bombeach)": 777_01_0_2,
    "Progressive Jump (Pizza Time)": 777_02_0_1,
    "Progressive Boost (Pizza Time)": 777_02_0_2,
    "Progressive Jump (Morio's Home)": 777_03_0_1,
    "Progressive Boost (Morio's Home)": 777_03_0_2,
    "Progressive Jump (Arcade Panik)": 777_04_0_1,
    "Progressive Boost (Arcade Panik)": 777_04_0_2,
    "Progressive Jump (Tosla's Offices)": 777_05_0_1,
    "Progressive Boost (Tosla's Offices)": 777_05_0_2,
    "Progressive Jump (Gym Gears)": 777_06_0_1,
    "Progressive Boost (Gym Gears)": 777_06_0_2,
    "Progressive Jump (Fecal Matters)": 777_07_0_1,
    "Progressive Boost (Fecal Matters)": 777_07_0_2,
    "Progressive Jump (Flushed Away)": 777_08_0_1,
    "Progressive Boost (Flushed Away)": 777_08_0_2,
    "Progressive Jump (Maurizio's City)": 777_09_0_1,
    "Progressive Boost (Maurizio's City)": 777_09_0_2,
    "Jump (Crash Test Industries)": 777_10_0_1,
    "Boost (Crash Test Industries)": 777_10_0_2,
    "Progressive Jump (Morio's Mind)": 777_12_0_1,
    "Progressive Boost (Morio's Mind)": 777_12_0_2,
    "Progressive Jump (Ruined Observatory)": 777_13_0_1,
    "Progressive Boost (Ruined Observatory)": 777_13_0_2,
    "Progressive Jump (Tosla HQ)": 777_14_0_1,
    "Progressive Boost (Tosla HQ)": 777_14_0_2,
    "Progressive Jump (The Moon)": 777_15_0_1,
    "Progressive Boost (The Moon)": 777_15_0_2,
    "Progressive Jump (Mosk's Rocket)": 777_16_0_1,
    "Progressive Boost (Mosk's Rocket)": 777_16_0_2,
    "Progressive Jump (Psycho Taxi)": 777_20_0_1,
    "Progressive Boost (Psycho Taxi)": 777_20_0_2,
    "Progressive Jump (Time Trials)": 777_21_0_1,
    "Progressive Boost (Time Trials)": 777_21_0_2,

    # Universal Tracker Only
    "Additional Expert Logic Level": 666_999
}

DEFAULT_ITEM_CLASSIFICATIONS = {
    "Gear": ItemClassification.progression_deprioritized_skip_balancing,
    "Bunny (Morio's Lab)": ItemClassification.progression_deprioritized,
    "Bunny (Bombeach)": ItemClassification.progression_deprioritized,
    "Bunny (Pizza Time)": ItemClassification.progression_deprioritized,
    "Bunny (Morio's Home)": ItemClassification.progression_deprioritized,
    "Bunny (Arcade Panik)": ItemClassification.progression_deprioritized,
    "Bunny (Tosla's Offices)": ItemClassification.progression_deprioritized,
    "Bunny (Gym Gears)": ItemClassification.progression_deprioritized,
    "Bunny (Fecal Matters)": ItemClassification.progression_deprioritized,
    "Bunny (Flushed Away)": ItemClassification.progression_deprioritized,
    "Bunny (Maurizio's City)": ItemClassification.progression_deprioritized,
    "Bunny (Crash Test Industries)": ItemClassification.progression_deprioritized,
    # "Bunny (Demo)": ItemClassification.progression_deprioritized,
    "Bunny (Morio's Mind)": ItemClassification.progression_deprioritized,
    "Bunny (Ruined Observatory)": ItemClassification.progression_deprioritized,
    "Bunny (Tosla HQ)": ItemClassification.progression_deprioritized,
    "Bunny (Moon)": ItemClassification.progression_deprioritized,
    "1 Coin": ItemClassification.filler,
    "10 Coins": ItemClassification.filler,
    "25 Coins": ItemClassification.filler,
    "100 Coins": ItemClassification.filler,
    # Hats reserve 7_00
    "No Hat": ItemClassification.filler,
    "Propeller Cap": ItemClassification.filler,
    "Top Hat": ItemClassification.filler,
    "Morio Hat": ItemClassification.progression,
    "Taxi Stack Hat": ItemClassification.filler,
    "Bomb Hat": ItemClassification.filler,
    "Drink Hat": ItemClassification.filler,
    "Chef Hat": ItemClassification.filler,
    "Spaghetti Hat": ItemClassification.filler,
    "Pot Hat": ItemClassification.filler,
    "Lasagna Hat": ItemClassification.filler,
    "Joystick Hat": ItemClassification.filler,
    "Slot Machine Hat": ItemClassification.filler,
    "Gelatin Hat": ItemClassification.filler,
    "Mug Hat": ItemClassification.filler,
    "Tosla Employee Hat": ItemClassification.filler,
    "Flexing Hat": ItemClassification.filler,
    "Syringe Hat": ItemClassification.filler,
    "Poop Hat": ItemClassification.filler,
    "Dog Bowl Hat": ItemClassification.filler,
    "Toilet Hat": ItemClassification.filler,
    "Bone Fish Hat": ItemClassification.filler,
    "Spoiler": ItemClassification.filler,
    "Police Lights": ItemClassification.filler,
    "Captain Abs-urd Hat": ItemClassification.filler,
    "Roid-Man Hat": ItemClassification.filler,
    "Buzzsaw Hat": ItemClassification.filler,
    "Crusher Hat": ItemClassification.filler,
    "Morio's Brain Hat": ItemClassification.progression,
    "Heart Hat": ItemClassification.filler,
    "Moon Globe Hat": ItemClassification.filler,
    "Tower Hat": ItemClassification.filler,
    "Alien Mosk (Evil) Hat": ItemClassification.filler,
    "Skeleton Taxi Skin": ItemClassification.filler,
    "Golden Taxi Skin": ItemClassification.filler,
    "Orbit Hat": ItemClassification.filler,
    "Satellite Dish Hat": ItemClassification.filler,
    "Alien Mosk (Good) Hat": ItemClassification.filler,
    "Crash Test Dummy Hat": ItemClassification.filler,
    "Dentures Hat": ItemClassification.filler,
    "Mushroom Cloud Hat": ItemClassification.filler,
    "Gym Bros Hat": ItemClassification.filler,
    "Banana Hat": ItemClassification.filler,
    "Bunny Hat": ItemClassification.filler,
    "Inception Top Hat": ItemClassification.filler,
    "Pizza Man Hat": ItemClassification.filler,
    "Toilet Paper Hat": ItemClassification.filler,
    "Pod Hat": ItemClassification.filler,
    "Paper Boat Hat": ItemClassification.filler,
    "Prototype Taxi Skin": ItemClassification.filler,
    "Glitched Taxi Skin": ItemClassification.filler,
    "TV Hat": ItemClassification.filler,
    "Burger Hat": ItemClassification.trap,
    "Flip-O-Will": ItemClassification.progression | ItemClassification.useful,
    "Progressive Jump": ItemClassification.progression | ItemClassification.useful,
    "Progressive Boost": ItemClassification.progression | ItemClassification.useful,
    "Spin Attack": ItemClassification.progression | ItemClassification.useful,
    "Glide": ItemClassification.useful,
    "Golden Spring Blueprints": ItemClassification.progression | ItemClassification.useful,
    "Golden Propeller Blueprints": ItemClassification.progression | ItemClassification.useful,
    "Pizza Wheels": ItemClassification.filler,
    "Lab Key": ItemClassification.progression,
    "Gym Membership": ItemClassification.progression,
    "Doggo": ItemClassification.progression,
    "Sewer Key": ItemClassification.progression,
    "Mosk's Rocket": ItemClassification.progression,
    "Time Trial Remote (Baby Steps!)": ItemClassification.progression,
    "Time Trial Remote (Getting Gud!)": ItemClassification.progression,
    "Time Trial Remote (Pro Tricks!)": ItemClassification.progression,
    "Hat World Membership": ItemClassification.progression,
    "Morio's Wardrobe": ItemClassification.progression,
    "Gela-Toni": ItemClassification.progression,
    "Pizza King": ItemClassification.progression,
    "Orange Switch": ItemClassification.progression,
    "Full Game Unlock": ItemClassification.progression,
    "Morio's Password": ItemClassification.progression,
    "Time Trial Remote": ItemClassification.progression,
    "Progressive Time Trial Remote": ItemClassification.progression,
    "Psycho Taxi Cartridge": ItemClassification.filler,
    "Michele": ItemClassification.useful,

    # Universal Tracker Only
    "Additional Expert Logic Level": ItemClassification.progression,
}

HATS = [
    "Propeller Cap",
    "Top Hat",
    "Morio Hat",
    "Taxi Stack Hat",
    "Bomb Hat",
    "Drink Hat",
    "Chef Hat",
    "Spaghetti Hat",
    "Pot Hat",
    "Lasagna Hat",
    "Joystick Hat",
    "Slot Machine Hat",
    "Gelatin Hat",
    "Mug Hat",
    "Tosla Employee Hat",
    "Flexing Hat",
    "Syringe Hat",
    "Poop Hat",
    "Dog Bowl Hat",
    "Toilet Hat",
    "Bone Fish Hat",
    "Spoiler",
    "Police Lights",
    "Captain Abs-urd Hat",
    "Roid-Man Hat",
    "Buzzsaw Hat",
    "Crusher Hat",
    "Morio's Brain Hat",
    "Heart Hat",
    "Moon Globe Hat",
    "Tower Hat",
    "Alien Mosk (Evil) Hat",
    "Skeleton Taxi Skin",
    "Golden Taxi Skin",
    "Orbit Hat",
    "Satellite Dish Hat",
    "Alien Mosk (Good) Hat",
    "Crash Test Dummy Hat",
    "Dentures Hat",
    "Mushroom Cloud Hat",
    "Gym Bros Hat",
    "Banana Hat",
    "Bunny Hat",
    "Inception Top Hat",
    "Pizza Man Hat",
    "Toilet Paper Hat",
    "Pod Hat",
    "Paper Boat Hat",
    "Prototype Taxi Skin",
    "Glitched Taxi Skin",
    "TV Hat",
    "Burger Hat"
]

TRAPS = [
    "Burger Hat Trap",
    "Cutscene Trap",
    "Explosion Trap",
    "Fast Trap",
    "Invisible Trap",
    "Literature Trap",
    "No Hat Trap",
    "Phone Trap",
    "Pixelate Trap",
    "Screen Flip Trap",
    "Slip Trap",
    "Slow Trap",
    "Spam Trap",
    "Stun Trap",
    "Timer Trap",
    "Whirlpool Trap",
]

class YellowTaxiItem(Item):
    game = "Yellow Taxi Goes Vroom"

def get_random_filler_item_name(world: YellowTaxiWorld) -> str:
    return get_random_filler_item_names(world, 1)[0]

def get_random_filler_item_names(world: YellowTaxiWorld, count: int) -> List[str]:
    filler = []
    weights = []
    if world.options.safesanity and world.options.hatsanity != world.options.hatsanity.option_disabled:
        filler += ["100 Coins"]
        weights += [3]
    elif world.options.hatsanity != world.options.hatsanity.option_disabled:
        filler += ["100 Coins"]
        weights += [2]
    elif world.options.safesanity:
        filler += ["100 Coins"]
        weights += [1]
    if world.options.chestsanity or world.options.cheesesanity:
        filler += ["25 Coins"]
        weights += [5]
    if world.options.coinbagsanity or world.options.cheesesanity or world.options.checkpointsanity:
        filler += ["10 Coins"]
        weights += [10]
    if world.options.coinsanity:
        filler += ["1 Coin"]
        weights += [world.options.coinsanity_percent]
    elif world.options.checkpointsanity:
        filler += ["1 Coin"]
        weights += [20]
    if len(filler) == 0:
        filler = ["25 Coins", "10 Coins"]
        weights = [1, 5]
    return world.random.choices(filler, weights, k=count)

def get_random_trap_names(world: YellowTaxiWorld, count:int) -> List[str]:
    return world.random.choices(sorted(world.options.enabled_traps.value), k=count)


def create_item_with_correct_classification(world: YellowTaxiWorld, name: str) -> YellowTaxiItem:
    if name in TRAPS:
        classification = ItemClassification.trap
    elif "Jump (" in name or "Boost (" in name:
        classification = ItemClassification.progression | ItemClassification.useful
    else:
        classification = DEFAULT_ITEM_CLASSIFICATIONS[name]

    # Don't skip balancing on required gears
    #if name == "Gear" and world.required_gears > 0:
    #    classification = ItemClassification.progression_deprioritized
    #    world.required_gears -= 1

    # Rat is progression if Cheesesanity is on
    if name == "Michele" and world.options.cheesesanity:
        classification = ItemClassification.progression

    if (name == "Police Lights" and
            ("Maurizio's City" in world.included_levels or "Maurizio's City" in world.goal_levels)):
        classification = ItemClassification.useful  # Makes cop cars not attack you
    if (name == "Alien Mosk (Good) Hat" or name == "Bunny Hat") and "Ruined Observatory" in world.included_levels:
        classification = ItemClassification.useful  # No actual items locked behind this, but make it useful
    if name == "Tosla Employee Hat" and "Tosla's Offices" in world.included_levels:
        classification = ItemClassification.progression # Allows access to employees-only room of Tosla Offices

    if name == "Psycho Taxi Cartridge" and world.options.shuffle_psycho_taxi_entrance:
        classification = ItemClassification.progression # Leads to an actual level, presumedly

    if name == "Pizza Wheels":
        if world.options.pizza_wheels == world.options.pizza_wheels.option_useful:
            classification = ItemClassification.useful
        if world.options.pizza_wheels == world.options.pizza_wheels.option_progression:
            classification = ItemClassification.progression

    return YellowTaxiItem(name, classification, ITEM_NAME_TO_ID[name], world.player)

def create_all_items(world: YellowTaxiWorld) -> None:
    gear_count = world.num_gears
    if world.using_ut:
        gear_count = world.ut_true_num_gears

    itempool : list[Item] = [world.create_item("Gear") for _ in range(gear_count)]

    # Add Bunnies to the pool if needed
    if world.options.bunnysanity and "Mosk's Rocket" in world.included_levels:
        hub_bunnies = 3
        if world.options.extra_demo_collectables:
            hub_bunnies += 2
        if world.exclude_top_bunny:
            hub_bunnies -= 1
        if world.exclude_spike_bunny:
            hub_bunnies -= 1
        itempool += [world.create_item("Bunny (Morio's Lab)") for _ in range(hub_bunnies)]
        for level in world.included_levels:
            if level not in ["Hub", "Mosk's Rocket", "Psycho Taxi"] and not level.endswith("!"):
                itempool += [world.create_item(f"Bunny ({level})") for _ in range(3)]

    if world.options.shuffle_gela_toni:
        itempool.append(world.create_item("Gela-Toni"))

    if world.options.shuffle_pizza_king:
        itempool.append(world.create_item("Pizza King"))

    if world.options.locked_morios_lab:
        itempool.append(world.create_item("Lab Key"))

    if (world.options.fecal_matters_unlock_condition ==
            world.options.fecal_matters_unlock_condition.option_shuffle_doggo):
        itempool.append(world.create_item("Doggo"))

    if (world.options.gym_gears_unlock_condition ==
            world.options.gym_gears_unlock_condition.option_shuffle_gym_membership):
        itempool.append(world.create_item("Gym Membership"))

    if (world.options.flushed_away_unlock_condition ==
            world.options.flushed_away_unlock_condition.option_shuffle_sewer_key):
        itempool.append(world.create_item("Sewer Key"))

    if world.options.shuffle_morios_password:
        itempool.append(world.create_item("Morio's Password"))

    if world.options.rocket_unlock_condition == world.options.rocket_unlock_condition.option_shuffle_rocket:
        itempool.append(world.create_item("Mosk's Rocket"))

    if world.options.shuffle_flip_o_will.value == world.options.shuffle_flip_o_will.option_global:
        itempool += [world.create_item("Progressive Boost") for _ in range(2)]
        itempool += [world.create_item("Progressive Jump") for _ in range(2)]
    elif world.options.shuffle_flip_o_will.value == world.options.shuffle_flip_o_will.option_per_level:
        created_time_trial_moves : bool = False
        true_included_levels : set[str] = set(list(world.included_levels) + list(world.goal_levels))
        for level in sorted(true_included_levels):
            if level == "Crash Test Industries":
                itempool += [world.create_item("Boost (Crash Test Industries)")]
                if world.options.allow_top_down_jumps:
                    itempool += [world.create_item("Jump (Crash Test Industries)")]
            elif level.endswith("!"):
                if not created_time_trial_moves:
                    itempool += [world.create_item("Progressive Boost (Time Trials)") for _ in range(2)]
                    itempool += [world.create_item("Progressive Jump (Time Trials)") for _ in range(2)]
                    created_time_trial_moves = True
            elif level != "Psycho Taxi":
                itempool += [world.create_item(f"Progressive Boost ({level})") for _ in range(2)]
                itempool += [world.create_item(f"Progressive Jump ({level})") for _ in range(2)]

    if world.options.shuffle_spin_attack:
        itempool.append(world.create_item("Spin Attack"))

    if world.options.shuffle_glide:
        itempool.append(world.create_item("Glide"))

    if world.options.shuffle_golden_spring:
        itempool.append(world.create_item("Golden Spring Blueprints"))

    if world.options.shuffle_golden_propeller:
        itempool.append(world.create_item("Golden Propeller Blueprints"))

    if world.options.shuffle_orange_switch:
        itempool.append(world.create_item("Orange Switch"))

    if world.options.pizza_wheels != world.options.pizza_wheels.option_off:
        itempool += [world.create_item("Pizza Wheels")]

    if world.options.shuffle_full_game:
        itempool.append(world.create_item("Full Game Unlock"))

    if world.options.shuffle_rat:
        itempool.append(world.create_item("Michele"))

    if (world.options.psycho_taxi_unlock_condition ==
            world.options.psycho_taxi_unlock_condition.option_shuffle_cartridge):
        itempool.append(world.create_item("Psycho Taxi Cartridge"))

    if world.options.locked_morios_wardrobe:
        itempool.append(world.create_item("Morio's Wardrobe"))

    if world.options.locked_time_trials == world.options.locked_time_trials.option_single_item:
        itempool.append(world.create_item("Time Trial Remote"))
    elif world.options.locked_time_trials == world.options.locked_time_trials.option_split_items:
        itempool.append(world.create_item("Time Trial Remote (Baby Steps!)"))
        itempool.append(world.create_item("Time Trial Remote (Getting Gud!)"))
        itempool.append(world.create_item("Time Trial Remote (Pro Tricks!)"))
    elif world.options.locked_time_trials == world.options.locked_time_trials.option_progressive_items:
        itempool += [world.create_item("Progressive Time Trial Remote") for _ in range(3)]

    # Add included hats
    for hat in sorted(world.included_hats):
        itempool.append(world.create_item(hat))

    # Create filler
    if world.using_ut:
        # Make one of everything for UT. No RNG to prevent item creation failures.
        itempool += [world.create_item("No Hat")]
        for hat in HATS:
            if hat not in world.included_hats:
                itempool.append(world.create_item(hat))
        for trap in TRAPS:
            itempool.append(world.create_item(trap))
        itempool += [world.create_item("1 Coin")]
        itempool += [world.create_item("10 Coins")]
        itempool += [world.create_item("25 Coins")]
        itempool += [world.create_item("100 Coins")]
    else: # Determine what actually needs to be added for real generation
        number_of_items = len(itempool)

        number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

        needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

        # Add hats to fill remaining hat locations, or remaining filler locations, depending
        if world.options.hatsanity != world.options.hatsanity.option_disabled:
            # Hatsanity only makes one location per hat
            if world.options.hatsanity == world.options.hatsanity.option_hatsanity:
                world.hat_location_count = len(world.included_hats)

            # If there are more hat locations than hat items, add "bonus" hats that do not have in-game locations
            extra_hats : int = min(world.hat_location_count - len(world.included_hats), needed_number_of_filler_items)

            if world.options.hatsanity_filler_hats:
                extra_hats = min(len(HATS) - len(world.included_hats), needed_number_of_filler_items)

            # If funny faces is enabled, special handling is performed for the TV Hat
            if world.options.funny_faces != "":
                if extra_hats > 0 and world.options.hatsanity == world.options.hatsanity.option_shopsanity:
                    itempool.append(world.create_item("No Hat"))
                    extra_hats -= 1
                    needed_number_of_filler_items -= 1
                world.included_hats.add("TV Hat") # TV Hat is always available when funny faces is enabled. Handled specially.

            # Next, add "Alien Mosk (Good)" hat, which has a minor in-game use (allows access to a ruined observatory area, no checks in it though)
            if extra_hats > 0 and "Ruined Observatory" in world.included_levels and "Alien Mosk (Good) Hat" not in world.included_hats:
                itempool.append(world.create_item("Alien Mosk (Good) Hat"))
                extra_hats -= 1
                needed_number_of_filler_items -= 1
                world.included_hats.add("Alien Mosk (Good) Hat")

            # Now add random hats as needed
            if extra_hats > 0:
                hats : list[str] = []
                hats.extend(HATS)
                world.random.shuffle(hats)
                for hat in hats:
                    if extra_hats == 0:
                        break
                    if hat in world.included_hats:
                        continue
                    itempool.append(world.create_item(hat))
                    extra_hats -= 1
                    needed_number_of_filler_items -= 1
                    # No need to add to included hats, last place they're needed

        # Add traps
        if world.options.trap_fill_percent > 0 and len(world.options.enabled_traps.value) > 0:
            needed_number_of_traps = math.floor((needed_number_of_filler_items * world.options.trap_fill_percent) / 100)

            itempool += [world.create_item(trap) for trap
                         in get_random_trap_names(world, needed_number_of_traps)]

            needed_number_of_filler_items -= needed_number_of_traps

        itempool += [world.create_item(filler) for filler
                     in get_random_filler_item_names(world, needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

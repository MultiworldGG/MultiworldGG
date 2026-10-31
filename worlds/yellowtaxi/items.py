from __future__ import annotations

import math
from typing import TYPE_CHECKING, List

from BaseClasses import Item, ItemClassification
from . import data_loader
from .names import ItemNames

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
    "Bunny (The Moon)": 2_15,
    "1 Coin": 3,
    "10 Coins": 4,
    "25 Coins": 5,
    "100 Coins": 6,
    # Hats reserve 7_00
    ItemNames.no_hat: 7_00,
    ItemNames.propeller_cap: 7_01,
    ItemNames.top_hat: 7_02,
    ItemNames.morio_hat: 7_03,
    ItemNames.taxi_stack_hat: 7_04,
    ItemNames.bomb_hat: 7_05,
    ItemNames.drink_hat: 7_06,
    ItemNames.chef_hat: 7_07,
    ItemNames.spaghetti_hat: 7_08,
    ItemNames.pot_hat: 7_09,
    ItemNames.lasagna_hat: 7_10,
    ItemNames.joystick_hat: 7_11,
    ItemNames.slot_machine_hat: 7_12,
    ItemNames.gelatin_hat: 7_13,
    ItemNames.mug_hat: 7_14,
    ItemNames.tosla_employee_hat: 7_15,
    ItemNames.flexing_hat: 7_16,
    ItemNames.syringe_hat: 7_17,
    ItemNames.poop_hat: 7_18,
    ItemNames.dog_bowl_hat: 7_19,
    ItemNames.toilet_hat: 7_20,
    ItemNames.bone_fish_hat: 7_21,
    ItemNames.spoiler: 7_22,
    ItemNames.police_lights: 7_23,
    ItemNames.captain_absurd_hat: 7_24,
    ItemNames.roidman_hat: 7_25,
    ItemNames.buzzsaw_hat: 7_26,
    ItemNames.crusher_hat: 7_27,
    ItemNames.morios_brain_hat: 7_28,
    ItemNames.heart_hat: 7_29,
    ItemNames.moon_globe_hat: 7_30,
    ItemNames.tower_hat: 7_31,
    ItemNames.alien_mosk_evil_hat: 7_32,
    ItemNames.skeleton_taxi_skin: 7_33,
    ItemNames.golden_taxi_skin: 7_34,
    ItemNames.orbit_hat: 7_35,
    ItemNames.satellite_dish_hat: 7_36,
    ItemNames.alien_mosk_good_hat: 7_37,
    ItemNames.crash_test_dummy_hat: 7_38,
    ItemNames.dentures_hat: 7_39,
    ItemNames.mushroom_cloud_hat: 7_40,
    ItemNames.gym_bros_hat: 7_41,
    ItemNames.banana_hat: 7_42,
    ItemNames.bunny_hat: 7_43,
    ItemNames.inception_top_hat: 7_44,
    ItemNames.pizza_man_hat: 7_45,
    ItemNames.toilet_paper_hat: 7_46,
    ItemNames.pod_hat: 7_47,
    ItemNames.paper_boat_hat: 7_48,
    ItemNames.prototype_taxi_skin: 7_49,
    ItemNames.glitched_taxi_skin: 7_50,
    ItemNames.tv_hat: 7_51,
    ItemNames.burger_hat: 7_52,
    #"Flip-O-Will": 8_0_0, # Not actually adding this at the moment, not interesting standalone
    "Progressive Jump": 8_0_1,
    "Progressive Boost": 8_0_2,
    "Spin Attack": 8_0_3,
    "Glide": 8_0_4,
    "Progressive Spin Attack": 8_0_5,
    "World Map Unlock": 8_0_6,
    "Golden Spring Blueprints": 8_1_0,
    "Golden Propeller Blueprints": 8_2_0,
    "Pizza Wheels": 8_9_9,
    "Lab Key": 10_00,
    "Gym Membership": 10_06,
    "Doggo": 10_07,
    "Sewer Key": 10_08,
    "Dream Machine": 10_12,
    "Mosk's Rocket": 10_16,
    "Time Attack Remote (Baby Steps!)": 10_17,
    "Time Attack Remote (Getting Gud!)": 10_18,
    "Time Attack Remote (Pro Tricks!)": 10_19,
    "Hat World Membership": 10_99,
    "Morio's Wardrobe": 11_00,
    "Gela-Toni": 11_01,
    "Pizza King": 11_02,
    "Orange Switch": 11_10,
    "Full Game Unlock": 11_11,
    "Morio's Password": 11_12,
    "Time Attack Remote": 11_17,
    "Progressive Time Attack Remote": 11_18,
    "Corrupted Pizza Slice": 12_02,
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
    "Debug Level Trap": 666_016,

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
    "Progressive Jump (Time Attacks)": 777_21_0_1,
    "Progressive Boost (Time Attacks)": 777_21_0_2,

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
    "Bunny (The Moon)": ItemClassification.progression_deprioritized,
    # Hats reserve 7_00
    ItemNames.morio_hat: ItemClassification.progression,
    ItemNames.morios_brain_hat: ItemClassification.progression,
    ItemNames.burger_hat: ItemClassification.trap,
    "Flip-O-Will": ItemClassification.progression | ItemClassification.useful,
    "Progressive Jump": ItemClassification.progression | ItemClassification.useful,
    "Progressive Boost": ItemClassification.progression | ItemClassification.useful,
    "Spin Attack": ItemClassification.progression | ItemClassification.useful,
    "Glide": ItemClassification.useful,
    "Progressive Spin Attack": ItemClassification.progression | ItemClassification.useful,
    "World Map Unlock": ItemClassification.useful,
    "Golden Spring Blueprints": ItemClassification.progression | ItemClassification.useful,
    "Golden Propeller Blueprints": ItemClassification.progression | ItemClassification.useful,
    "Lab Key": ItemClassification.progression,
    "Gym Membership": ItemClassification.progression,
    "Doggo": ItemClassification.progression,
    "Sewer Key": ItemClassification.progression,
    "Dream Machine": ItemClassification.progression,
    "Mosk's Rocket": ItemClassification.progression,
    "Time Attack Remote (Baby Steps!)": ItemClassification.progression,
    "Time Attack Remote (Getting Gud!)": ItemClassification.progression,
    "Time Attack Remote (Pro Tricks!)": ItemClassification.progression,
    "Hat World Membership": ItemClassification.progression,
    "Morio's Wardrobe": ItemClassification.progression,
    "Gela-Toni": ItemClassification.progression,
    "Pizza King": ItemClassification.progression,
    "Orange Switch": ItemClassification.progression,
    "Full Game Unlock": ItemClassification.progression,
    "Morio's Password": ItemClassification.progression,
    "Time Attack Remote": ItemClassification.progression,
    "Progressive Time Attack Remote": ItemClassification.progression,
    "Corrupted Pizza Slice": ItemClassification.progression,
    "Michele": ItemClassification.useful,

    # Universal Tracker Only
    "Additional Expert Logic Level": ItemClassification.progression,
}

HATS = [
    ItemNames.no_hat,
    ItemNames.propeller_cap,
    ItemNames.top_hat,
    ItemNames.morio_hat,
    ItemNames.taxi_stack_hat,
    ItemNames.bomb_hat,
    ItemNames.drink_hat,
    ItemNames.chef_hat,
    ItemNames.spaghetti_hat,
    ItemNames.pot_hat,
    ItemNames.lasagna_hat,
    ItemNames.joystick_hat,
    ItemNames.slot_machine_hat,
    ItemNames.gelatin_hat,
    ItemNames.mug_hat,
    ItemNames.tosla_employee_hat,
    ItemNames.flexing_hat,
    ItemNames.syringe_hat,
    ItemNames.poop_hat,
    ItemNames.dog_bowl_hat,
    ItemNames.toilet_hat,
    ItemNames.bone_fish_hat,
    ItemNames.spoiler,
    ItemNames.police_lights,
    ItemNames.captain_absurd_hat,
    ItemNames.roidman_hat,
    ItemNames.buzzsaw_hat,
    ItemNames.crusher_hat,
    ItemNames.morios_brain_hat,
    ItemNames.heart_hat,
    ItemNames.moon_globe_hat,
    ItemNames.tower_hat,
    ItemNames.alien_mosk_evil_hat,
    ItemNames.skeleton_taxi_skin,
    ItemNames.golden_taxi_skin,
    ItemNames.orbit_hat,
    ItemNames.satellite_dish_hat,
    ItemNames.alien_mosk_good_hat,
    ItemNames.crash_test_dummy_hat,
    ItemNames.dentures_hat,
    ItemNames.mushroom_cloud_hat,
    ItemNames.gym_bros_hat,
    ItemNames.banana_hat,
    ItemNames.bunny_hat,
    ItemNames.inception_top_hat,
    ItemNames.pizza_man_hat,
    ItemNames.toilet_paper_hat,
    ItemNames.pod_hat,
    ItemNames.paper_boat_hat,
    ItemNames.prototype_taxi_skin,
    ItemNames.glitched_taxi_skin,
    ItemNames.tv_hat,
    ItemNames.burger_hat,
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
    "Debug Level Trap",
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
    if len(filler) == 0 or world.options.extra_gear_percentage < 75:
        filler += ["100 Coins", "25 Coins", "10 Coins", "1 Coin"]
        weights += [1, 20, 15, 10]
    return world.random.choices(filler, weights, k=count)

def get_random_trap_names(world: YellowTaxiWorld, count:int) -> List[str]:
    traps = []
    weights = []
    for trap in world.options.trap_distribution.value:
        if world.options.trap_distribution.value[trap] > 0:
            traps += [trap]
            weights += [world.options.trap_distribution.value[trap]]

    return world.random.choices(traps, weights, k=count)


def create_item_with_correct_classification(world: YellowTaxiWorld, name: str) -> YellowTaxiItem:
    if name in TRAPS:
        classification = ItemClassification.trap
    elif "Jump (" in name or "Boost (" in name:
        classification = ItemClassification.progression | ItemClassification.useful
    elif name in DEFAULT_ITEM_CLASSIFICATIONS:
        classification = DEFAULT_ITEM_CLASSIFICATIONS[name]
    else:
        classification = ItemClassification.filler

    # Don't skip balancing on required gears
    #if name == "Gear" and world.required_gears > 0:
    #    classification = ItemClassification.progression_deprioritized
    #    world.required_gears -= 1

    # Rat is progression if Cheesesanity is on
    if name == "Michele" and world.options.cheesesanity:
        classification = ItemClassification.progression
    elif (name == ItemNames.police_lights and
            ("Maurizio's City" in world.included_levels or "Maurizio's City" in world.goal_levels)):
        classification = ItemClassification.useful  # Makes cop cars not attack you
    elif (name == ItemNames.alien_mosk_good_hat or name == ItemNames.bunny_hat) and "Ruined Observatory" in world.included_levels:
        classification = ItemClassification.useful  # No actual items locked behind this, but make it useful
    elif name == ItemNames.tosla_employee_hat and "Tosla's Offices" in world.included_levels:
        classification = ItemClassification.progression # Allows access to employees-only room of Tosla Offices
    elif (name == ItemNames.inception_top_hat and "Morio's Mind" in world.included_levels and
            world.options.morios_mind_laser_behavior.value in
            [
                world.options.morios_mind_laser_behavior.option_inception_top_hat,
                world.options.morios_mind_laser_behavior.option_morios_brain_or_inception_top_hat
            ]):
        classification = ItemClassification.progression
    elif name == "Psycho Taxi Cartridge" and world.options.shuffle_psycho_taxi_entrance:
        classification = ItemClassification.progression # Leads to an actual level, presumedly
    elif name == "Pizza Wheels":
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
        itempool += [world.create_item("Bunny (Morio's Lab)") for _ in range(world.hub_bunnies)]
        world.num_bunnies = world.hub_bunnies
        bunny_level_list : list[str] = world.included_levels.copy()
        if world.options.bunnysanity_includes_all_bunnies:
            bunny_level_list = data_loader.original_portal_level_order + data_loader.grannys_island_level_order
        for level in bunny_level_list:
            if level not in ["Hub", "Mosk's Rocket", "Psycho Taxi"] and not level.endswith("!"):
                itempool += [world.create_item(f"Bunny ({level})") for _ in range(3)]
                world.num_bunnies += 3

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

    if (world.options.dream_machine_unlock_condition ==
            world.options.dream_machine_unlock_condition.option_shuffle_dream_machine
            and not "Morio's Lab - Dream Machine" in world.excluded_regions):
        itempool.append(world.create_item("Dream Machine"))

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
                    itempool += [world.create_item("Progressive Boost (Time Attacks)") for _ in range(2)]
                    itempool += [world.create_item("Progressive Jump (Time Attacks)") for _ in range(2)]
                    created_time_trial_moves = True
            elif level != "Psycho Taxi":
                itempool += [world.create_item(f"Progressive Boost ({level})") for _ in range(2)]
                itempool += [world.create_item(f"Progressive Jump ({level})") for _ in range(2)]

    if world.options.shuffle_spin_attack.value == world.options.shuffle_spin_attack.option_shuffle:
        itempool.append(world.create_item("Spin Attack"))
    elif world.options.shuffle_spin_attack.value == world.options.shuffle_spin_attack.option_progressive:
        itempool += [world.create_item("Progressive Spin Attack") for _ in range(2)]

    if world.options.shuffle_glide:
        itempool.append(world.create_item("Glide"))

    if world.options.shuffle_world_map:
        itempool.append(world.create_item("World Map Unlock"))

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

    if world.options.hat_world_membership:
        itempool.append(world.create_item("Hat World Membership"))

    if (world.options.psycho_taxi_unlock_condition ==
            world.options.psycho_taxi_unlock_condition.option_shuffle_cartridge):
        itempool.append(world.create_item("Psycho Taxi Cartridge"))

    if world.options.locked_morios_wardrobe:
        itempool.append(world.create_item("Morio's Wardrobe"))

    if world.options.locked_time_trials == world.options.locked_time_trials.option_single_item:
        itempool.append(world.create_item("Time Attack Remote"))
    elif world.options.locked_time_trials == world.options.locked_time_trials.option_split_items:
        itempool.append(world.create_item("Time Attack Remote (Baby Steps!)"))
        itempool.append(world.create_item("Time Attack Remote (Getting Gud!)"))
        itempool.append(world.create_item("Time Attack Remote (Pro Tricks!)"))
    elif world.options.locked_time_trials == world.options.locked_time_trials.option_progressive_items:
        itempool += [world.create_item("Progressive Time Attack Remote") for _ in range(3)]

    if world.options.pizzasanity and "Pizza Time" in world.included_levels:
        itempool += [world.create_item("Corrupted Pizza Slice") for _ in range(world.options.pizzasanity_count.value)]

    # Add included hats
    for hat in sorted(world.included_hats):
        itempool.append(world.create_item(hat))

    # Create filler
    if world.using_ut:
        # Make one of everything for UT. No RNG to prevent item creation failures.
        itempool += [world.create_item(ItemNames.no_hat)]
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
                    itempool.append(world.create_item(ItemNames.no_hat))
                    extra_hats -= 1
                    needed_number_of_filler_items -= 1
                world.included_hats.add(ItemNames.tv_hat) # TV Hat is always available when funny faces is enabled. Handled specially.

            # Next, add "Alien Mosk (Good)" hat, which has a minor in-game use (allows access to a ruined observatory area, no checks in it though)
            if extra_hats > 0 and "Ruined Observatory" in world.included_levels and ItemNames.alien_mosk_good_hat not in world.included_hats:
                itempool.append(world.create_item(ItemNames.alien_mosk_good_hat))
                extra_hats -= 1
                needed_number_of_filler_items -= 1
                world.included_hats.add(ItemNames.alien_mosk_good_hat)

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
        if world.options.trap_fill_percent > 0:
            any_traps_enabled : bool = False
            for trap in world.options.trap_distribution.value:
                if world.options.trap_distribution.value[trap] > 0:
                    any_traps_enabled = True
                    break

            if any_traps_enabled:
                needed_number_of_traps = math.floor((needed_number_of_filler_items * world.options.trap_fill_percent) / 100)

                itempool += [world.create_item(trap) for trap
                             in get_random_trap_names(world, needed_number_of_traps)]

                needed_number_of_filler_items -= needed_number_of_traps

        itempool += [world.create_item(filler) for filler
                     in get_random_filler_item_names(world, needed_number_of_filler_items)]

    world.multiworld.itempool += itempool

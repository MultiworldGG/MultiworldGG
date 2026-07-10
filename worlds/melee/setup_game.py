import logging
from .Rules import adventure_trophies, classic_trophies, allstar_trophies


def setup_gamevars(world) -> None:
    character_selection = ["Dr. Mario", "Mario", "Luigi", "Bowser", "Peach",
                           "Yoshi", "Donkey Kong", "Captain Falcon", "Ganondorf", "Falco",
                           "Fox", "Ness", "Ice Climbers", "Kirby", "Samus",
                           "Zelda", "Link", "Young Link", "Pichu", "Pikachu",
                           "Jigglypuff", "Mewtwo", "Mr. Game & Watch", "Marth", "Roy"]

    world.starting_character = character_selection[world.options.starting_character]
    world.multiworld.push_precollected(world.create_item(world.starting_character))

    world.total_trophy_count = world.options.trophies_required + world.options.extra_trophies
    if world.total_trophy_count > 293:
        logging.warning(f"""Warning: {world.multiworld.get_player_name(world.player)}'s generated Trophy Count is too high.
                Required: {world.options.trophies_required} | Extra: {world.options.extra_trophies}. This will be automatically capped to 293.""")
        world.total_trophy_count = 293
        world.options.extra_trophies.value = 293 - world.options.trophies_required

    world.total_trophy_count = max(0, world.total_trophy_count)
    for i in range(world.total_trophy_count):
        if not world.all_trophies:
            break
        else:
            trophy = world.random.choice(world.all_trophies)
            world.all_trophies.remove(trophy)
            world.picked_trophies.add(trophy)

    if world.options.lottery_pool_mode:
        world.required_item_count += 4

    if world.options.target_checks:
        world.location_count += 25

    if world.options.ten_man_checks:
        world.location_count += 25

    if world.options.event_checks:
        world.location_count += 45

    if world.options.enable_rare_pokemon_checks:
        world.location_count += 2

    if world.options.diskun_trophy_check:
        world.location_count += 1

    if world.options.mewtwo_unlock_check:
        world.location_count += 1

    if world.options.vs_count_checks:
        world.location_count += 7

    if world.options.hard_modes_clear:
        world.location_count += 3

    if world.options.enable_annoying_multiman_checks:
        world.location_count += 2

    if world.options.long_targettest_checks:
        world.location_count += 3

    if world.options.adventure_clear_trophies:
        world.location_count += 26

    if world.options.classic_clear_trophies:
        world.location_count += 26

    if world.options.all_star_clear_trophies:
        world.location_count += 26

    if not world.options.remove_random_1P_trophies:
        world.location_count += 27

    if world.options.bonus_checks:
        world.location_count += 223
        
        if world.options.enable_rare_pokemon_checks:
            world.location_count += 2  # Pokemon bonuses

        if world.options.enable_hard_bonuses:
            world.location_count += 13

        if world.options.enable_extreme_bonuses:
            world.location_count += 7
        
        if world.options.hard_modes_clear:
            world.location_count += 1

    if not world.options.randomize_battle_items:
        world.multiworld.push_precollected(world.create_item("Capsule"))
        world.multiworld.push_precollected(world.create_item("Crate"))
        world.multiworld.push_precollected(world.create_item("Barrel"))
        world.multiworld.push_precollected(world.create_item("Egg"))
        world.multiworld.push_precollected(world.create_item("Party Ball"))
        world.multiworld.push_precollected(world.create_item("Barrel Cannon"))
        world.multiworld.push_precollected(world.create_item("Bob-omb"))
        world.multiworld.push_precollected(world.create_item("Mr. Saturn"))
        world.multiworld.push_precollected(world.create_item("Heart Container"))
        world.multiworld.push_precollected(world.create_item("Maxim Tomato"))
        world.multiworld.push_precollected(world.create_item("Starman"))
        world.multiworld.push_precollected(world.create_item("Home-Run Bat"))
        world.multiworld.push_precollected(world.create_item("Beam Sword"))
        world.multiworld.push_precollected(world.create_item("Parasol"))
        world.multiworld.push_precollected(world.create_item("Green Shell"))
        world.multiworld.push_precollected(world.create_item("Red Shell"))
        world.multiworld.push_precollected(world.create_item("Ray Gun"))
        world.multiworld.push_precollected(world.create_item("Freezie"))
        world.multiworld.push_precollected(world.create_item("Food"))
        world.multiworld.push_precollected(world.create_item("Motion-Sensor Bomb"))
        world.multiworld.push_precollected(world.create_item("Flipper"))
        world.multiworld.push_precollected(world.create_item("Super Scope"))
        world.multiworld.push_precollected(world.create_item("Star Rod"))
        world.multiworld.push_precollected(world.create_item("Lip's Stick"))
        world.multiworld.push_precollected(world.create_item("Fan"))
        world.multiworld.push_precollected(world.create_item("Fire Flower"))
        world.multiworld.push_precollected(world.create_item("Super Mushroom"))
        world.multiworld.push_precollected(world.create_item("Poison Mushroom"))
        world.multiworld.push_precollected(world.create_item("Hammer"))
        world.multiworld.push_precollected(world.create_item("Warp Star"))
        world.multiworld.push_precollected(world.create_item("Screw Attack"))
        world.multiworld.push_precollected(world.create_item("Bunny Hood"))
        world.multiworld.push_precollected(world.create_item("Metal Box"))
        world.multiworld.push_precollected(world.create_item("Cloaking Device"))
        world.multiworld.push_precollected(world.create_item("Poké Ball"))
    else:
        world.required_item_count += 35


def place_static_items(world):
    world.get_location("Trophy Room - Admire Collection").place_locked_item(world.create_item("Sense of Accomplishment"))

    if "Giga Bowser" in world.options.goal_triggers:
        world.get_location("Goal: Giga Bowser Defeated").place_locked_item(world.create_item("Sense of Accomplishment"))

    if "Crazy Hand" in world.options.goal_triggers:
        world.get_location("Goal: Crazy Hand Defeated").place_locked_item(world.create_item("Sense of Accomplishment"))

    if "Event 51" in world.options.goal_triggers:
        world.get_location("Goal: Event 51").place_locked_item(world.create_item("Sense of Accomplishment"))

    if "Other Events" in world.options.goal_triggers:
        world.get_location("Goal: Other Events Clear").place_locked_item(world.create_item("Sense of Accomplishment"))

    if "All Targets" in world.options.goal_triggers:
        world.get_location("Goal: All Targets Clear").place_locked_item(world.create_item("Sense of Accomplishment"))

    if "Event 50" in world.options.goal_triggers:
        world.get_location("Goal: Event 50").place_locked_item(world.create_item("Sense of Accomplishment"))


def calculate_trophy_based_locations(world):
    if adventure_trophies.issubset(world.picked_trophies):
        world.all_adventure_trophies = True
    else:
        world.all_adventure_trophies = False

    if classic_trophies.issubset(world.picked_trophies):
        world.all_classic_trophies = True
    else:
        world.all_classic_trophies = False

    if allstar_trophies.issubset(world.picked_trophies):
        world.all_allstar_trophies = True
    else:
        world.all_allstar_trophies = False

    if len(world.picked_trophies) >= 250 or world.options.lottery_pool_mode:
        world.use_250_trophy_pool = True
    else:
        world.use_250_trophy_pool = False

from .Options import SoulsanityLevel, SoulRandomizer, MineCondition, GardenCondition, MenaceCondition
from .in_game_data import warp_room_regions, warp_room_table
from .modules.bullet_wall_randomizer import set_souls_for_walls
from .modules.synthesis_randomizer import randomize_synthesis
from .modules.boss_randomizer import randomize_bosses
from .modules.seal_shuffle import set_seals
from .modules.set_goals import set_goal_triggers
from logging import warning


def setup_game(world):
    from .generator_main import create_progress_event
    if world.player_name == "ironsoul":
        world.iron_mode = True

    if world.iron_mode:
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 1"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 2"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 3"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 4"))
        world.multiworld.push_precollected(create_progress_event(world, "Magic Seal 5"))
        world.multiworld.local_early_items[world.player]["Malphas Soul"] = 1

    world.extra_soul_slots = 99  # Locations that can be filled by guaranteed souls

    world.mine_status = None
    world.garden_chamber_available = True
    world.mine_requisites = None

    if world.options.mine_condition == MineCondition.option_garden:
        if world.options.garden_condition == GardenCondition.option_throne_room:
            world.mine_requisites = "Throne Room"
        else:
            world.mine_requisites = "Garden"
    elif world.options.mine_condition == MineCondition.option_throne_room:
        world.mine_requisites = "Throne Room"

    if not world.options.goal:
        if world.options.mine_condition == MineCondition.option_throne_room or ( 
                    world.options.mine_condition == MineCondition.option_garden and 
                    world.options.garden_condition == GardenCondition.option_throne_room):
            world.mine_status = "Disabled"  # Make sure we don't generate Mine checks if the Mine is unreachable.

        if world.options.menace_condition == MenaceCondition.option_throne_room or (
                world.options.menace_condition == MenaceCondition.option_garden and world.options.garden_condition == GardenCondition.option_throne_room):
            world.options.menace_condition.value = MenaceCondition.option_none  # This would be impossible so we switch it to no condition
            
        if world.options.garden_condition == GardenCondition.option_throne_room:
            world.garden_chamber_available = False

    if not world.mine_status:  # If we didn't just disable it, set the status here
        if world.options.mine_condition != MineCondition.option_none:
            world.mine_status = "Locked"
        else:
            world.mine_status = "Open"

    if world.options.early_seal_1:
        world.multiworld.local_early_items[world.player]["Magic Seal 1"] = 1

    if world.starting_warp_room is None:  # UT will have already grabbed it
        if world.options.shuffle_starting_warp_room:
            world.starting_warp_room = world.random.choice(warp_room_table)
        else:
            world.starting_warp_room = "Lost Village"

    world.starting_warp_region = warp_room_regions[world.starting_warp_room]

    if not world.magic_seal_table:  # If not doing UT passthrough
        set_seals(world)
    set_souls_for_walls(world)
    randomize_synthesis(world)

    if world.options.boss_shuffle:
        randomize_bosses(world)

    world.menace_triggers = set_goal_triggers(world, world.options.menace_condition.current_key, "Menace")
    world.garden_triggers = set_goal_triggers(world, world.options.garden_condition.current_key, "Garden")
    world.mine_triggers = set_goal_triggers(world, world.options.mine_condition.current_key, "Mine")


def place_static_items(world):
    world.get_location("Lost Village: Moat Drain Switch").place_locked_item(world.create_item("Moat Drained"))
    world.get_location("Abyss Center").place_locked_item(world.create_item("Menace Defeated"))
    # Place boss kill checks
    world.get_location("Lost Village: Boss Room").place_locked_item(world.create_item("Village Boss Clear"))
    world.get_location("Wizardry Lab: Boss Room").place_locked_item(world.create_item("Lab Boss Clear"))
    world.get_location("Dark Chapel: Boss Room").place_locked_item(world.create_item("Chapel Boss Clear"))
    world.get_location("Dark Chapel: Inner Chapel Boss Room").place_locked_item(world.create_item("Inner Chapel Boss Clear"))
    world.get_location("Garden of Madness: Boss Room").place_locked_item(world.create_item("Garden Boss Clear"))
    world.get_location("Demon Guest House: Boss Room").place_locked_item(world.create_item("Guest House Boss Clear"))
    world.get_location("Subterranean Hell: Boss Room").place_locked_item(world.create_item("Subterranean Hell Boss Clear"))
    world.get_location("Condemned Tower: Boss Room").place_locked_item(world.create_item("Tower Boss Clear"))
    world.get_location("Cursed Clock Tower: Boss Room").place_locked_item(world.create_item("Clock Tower Boss Clear"))
    world.get_location("Silenced Ruins: Boss Room").place_locked_item(world.create_item("Ruins Boss Clear"))
    world.get_location("Upper Guest House: Boss Room").place_locked_item(world.create_item("Upper Guest House Boss Clear"))

    if world.options.goal:
        world.get_location("The Pinnacle: Throne Room").place_locked_item(world.create_item("Aguni Defeated"))

    if world.mine_status != "Disabled":
        world.get_location("The Abyss: Boss Room").place_locked_item(world.create_item("Abyss Boss Clear"))
        world.get_location("Mine of Judgment: Boss Room").place_locked_item(world.create_item("Mine Boss Clear"))

    if world.garden_chamber_available:
        world.get_location("Garden of Madness: Central Chamber").place_locked_item(world.create_item("Power of Darkness"))


def setup_souls(world):
    world.options.guaranteed_souls.value = {soul.title() for soul in world.options.guaranteed_souls.value}
    world.important_souls.update(sorted(world.red_soul_walls))
    if world.options.soulsanity_level == SoulsanityLevel.option_rare and world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.important_souls.add("Imp Soul")

    if world.mine_status != "Disabled":
        world.common_souls.update(["Slogra Soul", "Black Panther Soul"])
        world.uncommon_souls.update(["Ripper Soul", "Mud Demon Soul", "Gaibon Soul", "Malacoda Soul"])
        world.rare_souls.update(["Giant Slug Soul", "Stolas Soul", "Arc Demon Soul"])
    # Conver this to proper casing
    if "Common" in world.options.guaranteed_souls:
        for soul in world.common_souls:
            if soul not in world.options.guaranteed_souls.value:
                world.options.guaranteed_souls.value.add(soul)
        world.options.guaranteed_souls.value.remove("Common")

    if "Uncommon" in world.options.guaranteed_souls.value:
        for soul in world.uncommon_souls:
            if soul not in world.options.guaranteed_souls.value:
                world.options.guaranteed_souls.value.add(soul)
        world.options.guaranteed_souls.value.remove("Uncommon")

    if "Rare" in world.options.guaranteed_souls.value:
        for soul in world.rare_souls:
            if soul not in world.options.guaranteed_souls.value:
                world.options.guaranteed_souls.value.add(soul)
        world.options.guaranteed_souls.value.remove("Rare")

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.important_souls.update(["Mandragora Soul", "Rycuda Soul", "Waiter Skeleton Soul"])  # Always required for sanity

    if world.options.soul_randomizer != SoulRandomizer.option_soulsanity:
        if world.mine_status == "Disabled":
            goal_locked_enemies = {"Malacoda Soul", "Slogra Soul", "Ripper Soul"}  # These enemies are inacessible if Mine is removed
            world.excluded_static_souls.update(goal_locked_enemies)

    world.options.guaranteed_souls.value = {item.title() for item in world.options.guaranteed_souls.value}
    if world.options.no_logical_grinding:
        world.excluded_static_souls.update(world.important_souls)  # Do this so they don't get forced vanilla


def place_souls(world, pool):
    soul_location_count = 0
    extra_souls = 0
    souls_added = 0

    if world.mine_status != "Disabled":
        world.extra_soul_slots += 4  # Mine checks count

    if world.options.gate_items == 1:
        world.extra_soul_slots -= 4  # We need space for the keys

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        world.extra_soul_slots += len(world.common_souls)

        if world.options.soulsanity_level:
            world.extra_soul_slots += len(world.uncommon_souls)

        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            world.extra_soul_slots += len(world.rare_souls)

    if world.options.no_logical_grinding:
        world.extra_soul_slots -= len(world.important_souls)

    for soul in sorted(world.options.guaranteed_souls):
        world.extra_soul_slots -= 1
        if not world.extra_soul_slots:
            warning("WARNING: More Guranteed Souls exist than can be placed, no more Guaranteed Souls will be placed.")
            break  # Bail if we're out of room for more souls
        else:
            pool.append(world.create_item(soul))
            update_soul_pool(world, soul)
            souls_added += 1

    if world.options.no_logical_grinding and world.options.soul_randomizer != SoulRandomizer.option_soulsanity:
        for soul in sorted(world.important_souls):
            if world.create_item(soul) not in pool:
                pool.append(world.create_item(soul))
                update_soul_pool(world, soul)

    if world.options.soul_randomizer == SoulRandomizer.option_soulsanity:
        # These items are only important on Rare tier
        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            world.good_armor_table.remove("Soul Eater Ring")  # Don't generate a filler copy since hard guarantees one
            pool.append(world.create_item("Soul Eater Ring"))  # Guarantee we get a Soul Eater Ring for rare's

        for soul in sorted(world.important_souls):
            if world.create_item(soul) not in pool:  # First we need to create the souls that are always in
                extra_souls += 1
                update_soul_pool(world, soul)
                pool.append(world.create_item(soul))

        soul_location_count += (len(world.common_souls) - extra_souls)

        if world.options.soulsanity_level:
            soul_location_count += len(world.uncommon_souls)

        if world.options.soulsanity_level == SoulsanityLevel.option_rare:
            soul_location_count += len(world.rare_souls)

        for i in range(soul_location_count - souls_added):
            soul = world.random.choice(world.filler_souls)
            pool.append(world.create_item(soul))
            update_soul_pool(world, soul)
    else:
        place_inaccessible_souls = False
        if world.mine_status == "Disabled":
            place_inaccessible_souls = True
        elif world.mine_status == "Locked":
            if "Upper Guest House Boss Clear" in world.mine_triggers:
                place_inaccessible_souls = True
            elif world.options.mine_condition == MineCondition.option_garden and world.garden_triggers:
                # Place these if we need to reach garden and garden is bosses
                if "Upper Guest House Boss Clear" in world.garden_triggers:
                    place_inaccessible_souls = True

        if place_inaccessible_souls and not world.options.no_logical_grinding:
            goal_locked_enemies = {"Malacoda Soul", "Slogra Soul", "Ripper Soul"}  # These enemies are inacessible if Mine is removed
            for soul in (item for item in world.red_soul_walls if item in goal_locked_enemies):
                pool.append(world.create_item(soul))


def place_static_souls(world):
    from .generator_main import create_static_soul
    for soul in sorted(world.important_souls):
        if soul not in world.excluded_static_souls:
            world.get_location(soul).place_locked_item(create_static_soul(world, soul))


def update_soul_pool(world, soul):
    from .in_game_data import unleveled_standard_souls
    # Remove leveled souls from the Filler pool of souls
    if soul in unleveled_standard_souls and soul in world.filler_souls:
        world.filler_souls.remove(soul)  # If the soul is present, remove it

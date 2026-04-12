from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, add_rule, forbid_item
from .Locations import EOS_location_table, EOSLocation, location_Dict_by_id
from .RomTypeDefinitions import subX_table

if TYPE_CHECKING:
    from . import EOSWorld


def set_rules(world: "EOSWorld", excluded):
    player = world.player
    options = world.options

    special_episodes_rules(world, player)
    subx_rules(world, player)
    dungeon_locations_behind_items(world, player)
    mission_rules(world, player)
    forbid_items_behind_locations(world, player)
    spinda_drink_events(world, player)

    if world.options.goal.value == 0:
        set_rule(
            world.multiworld.get_location("Final Boss", player),
            lambda state: state.has("Temporal Tower", player) and has_relic_shards(state, player, world),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Final Boss", player), lambda state: state.has("Main Game Unlock", player)
            )

        # set_rule(world.multiworld.get_location("Dark Crater", player),
        # lambda state: state.has("Dark Crater", player) and ready_for_late_game(state, player, world))

    elif world.options.goal.value == 1:
        set_rule(
            world.multiworld.get_location("Final Boss", player), lambda state: ready_for_darkrai(state, player, world)
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Final Boss", player), lambda state: state.has("Main Game Unlock", player)
            )
        set_rule(
            world.multiworld.get_location("Dark Crater", player), lambda state: ready_for_darkrai(state, player, world)
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Dark Crater", player),
                lambda state: state.has("Main Game Unlock", player),
            )
        set_rule(
            world.multiworld.get_location("The Nightmare", player),
            lambda state: state.can_reach_location("Mt. Bristle", player)
            and state.has("The Nightmare", player)
            and ready_for_late_game(state, player, world),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("The Nightmare", player),
                lambda state: state.has("Main Game Unlock", player),
            )

    set_rule(
        world.multiworld.get_entrance("Late Game Door", player), lambda state: ready_for_late_game(state, player, world)
    )

    set_rule(world.multiworld.get_location("Hidden Land", player), lambda state: has_relic_shards(state, player, world))
    if special_episode_sanity_no_exclusion(world, player):
        add_rule(
            world.multiworld.get_location("Hidden Land", player), lambda state: state.has("Main Game Unlock", player)
        )

    set_rule(
        world.multiworld.get_location("Temporal Tower", player),
        lambda state: state.has("Temporal Tower", player) and has_relic_shards(state, player, world),
    )
    if special_episode_sanity_no_exclusion(world, player):
        add_rule(
            world.multiworld.get_location("Temporal Tower", player), lambda state: state.has("Main Game Unlock", player)
        )


def has_relic_shards(state, player, world):
    return state.has("Relic Fragment Shard", player, world.options.required_fragments.value)


def ready_for_late_game(state, player, world):
    return (
        state.has_group("EarlyDungeons", player, 10)
        and state.has("Relic Fragment Shard", player, world.options.required_fragments.value)
        and state.has("Temporal Tower", player)
    )


def spinda_drink_events(world, player):
    de_amount = world.options.drink_events.value
    sdrinks_amount = world.options.spinda_drinks.value
    for i in range(de_amount):
        set_rule(
            world.multiworld.get_location("Spinda Drink Event " + str(i + 1), player),
            lambda state: state.has("Bag Upgrade", player, 3),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Spinda Drink Event " + str(i + 1), player),
                lambda state: state.has("Main Game Unlock", player)
                or state.has("Bidoof's Wish", player)
                or state.has('Today\'s "Oh My Gosh"', player),
            )
    for i in range(sdrinks_amount):
        set_rule(
            world.multiworld.get_location("Spinda Drink " + str(i + 1), player),
            lambda state: state.has("Bag Upgrade", player),
        )
        if special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location("Spinda Drink " + str(i + 1), player),
                lambda state: state.has("Main Game Unlock", player)
                or state.has("Bidoof's Wish", player)
                or state.has('Today\'s "Oh My Gosh"', player),
            )


def forbid_items_behind_locations(world, player):
    forbid_item(world.multiworld.get_location("Hidden Land", player), "Relic Fragment Shard", player)
    forbid_item(world.multiworld.get_location("Temporal Tower", player), "Relic Fragment Shard", player)
    if world.options.goal.value == 1 and world.options.sky_peak_type == 1:
        forbid_item(world.multiworld.get_location("1st Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("2nd Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("3rd Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("4th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("5th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("6th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("7th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("8th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("9th Station Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("Sky Peak Summit Pass", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("5th Station Clearing", player), "Progressive Sky Peak", player)
        forbid_item(world.multiworld.get_location("Sky Peak Summit", player), "Progressive Sky Peak", player)
        # if world.options.goal.value == 1:
        for i in range(111, 120):
            location = location_Dict_by_id[i]
            for j in range(world.options.late_mission_checks.value):
                forbid_item(
                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                    "Progressive Sky Peak",
                    player,
                )
            for j in range(world.options.late_outlaw_checks.value):
                forbid_item(
                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                    "Progressive Sky Peak",
                    player,
                )


def special_episodes_rules(world, player):
    if not world.options.exclude_special.value:
        # Bidoof Special Episode Checks
        set_rule(
            world.multiworld.get_location("SE Deep Star Cave", player), lambda state: state.has("Bidoof's Wish", player)
        )
        set_rule(
            world.multiworld.get_location("SE Star Cave Pit", player), lambda state: state.has("Bidoof's Wish", player)
        )

        # Igglybuff Special Episode checks
        set_rule(
            world.multiworld.get_location("SE Murky Forest", player),
            lambda state: state.has("Igglybuff the Prodigy", player),
        )
        set_rule(
            world.multiworld.get_location("SE Eastern Cave", player),
            lambda state: state.has("Igglybuff the Prodigy", player),
        )
        set_rule(
            world.multiworld.get_location("SE Fortune Ravine", player),
            lambda state: state.has("Igglybuff the Prodigy", player),
        )

        # Grovyle and Dusknoir Special Episode Checks
        set_rule(
            world.multiworld.get_location("In the Future of Darkness Location", player),
            lambda state: has_relic_shards(state, player, world),
        )
        set_rule(
            world.multiworld.get_location("SE Barren Valley", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Dark Wasteland", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Temporal Tower", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Dusk Forest", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Spacial Cliffs", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Dark Ice Mountain", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Icicle Forest", player),
            lambda state: state.has("In the Future of Darkness", player),
        )
        set_rule(
            world.multiworld.get_location("SE Vast Ice Mountain", player),
            lambda state: state.has("In the Future of Darkness", player),
        )

        # Team Charm Special Episode Checks
        set_rule(
            world.multiworld.get_location("SE Southern Jungle", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Boulder Quarry", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Right Cave Path", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Left Cave Path", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )
        set_rule(
            world.multiworld.get_location("SE Limestone Cavern", player),
            lambda state: state.has("Here Comes Team Charm!", player),
        )

        # Sunflora Special Episode Checks
        set_rule(
            world.multiworld.get_location("SE Upper Spring Cave", player),
            lambda state: state.has('Today\'s "Oh My Gosh"', player),
        )
        set_rule(
            world.multiworld.get_location("SE Middle Spring Cave", player),
            lambda state: state.has('Today\'s "Oh My Gosh"', player),
        )
        set_rule(
            world.multiworld.get_location("SE Spring Cave Pit", player),
            lambda state: state.has('Today\'s "Oh My Gosh"', player),
        )


def ready_for_darkrai(state, player, world):
    return (
        state.has("Relic Fragment Shard", player, world.options.required_fragments.value)
        and state.has("Temporal Tower", player)
        and state.has_group("Instrument", player, world.options.req_instruments.value)
        and state.has_group("LateDungeons", player, 10)
    )


def dungeon_locations_behind_items(world, player):
    for location in EOS_location_table:
        if location.name == "Beach Cave":
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
            continue
        elif "Early" in location.group:
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
        elif "Dojo" in location.group:
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player)
                    or state.has("Bidoof's Wish", player)
                    or state.has('Today\'s "Oh My Gosh"', player),
                )
        elif "Station" in location.group and world.options.goal.value == 1:
            if world.options.sky_peak_type.value == 1:  # progressive
                if location.name == "Sky Peak Summit":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Progressive Sky Peak", player, 10)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.name == "5th Station Clearing":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Progressive Sky Peak", player, 5)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                else:
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state, req_num=(location.id - 110): state.has("Progressive Sky Peak", player, req_num)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )

            elif world.options.sky_peak_type.value == 2:  # all random
                if location.name == "Sky Peak Summit":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Sky Peak Summit Pass", player)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.name == "5th Station Clearing":
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("5th Station Pass", player)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                else:
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state, ln=location.name: state.has(ln, player)
                        and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )

            elif world.options.sky_peak_type.value == 3:  # all open from 1st station pass
                set_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("1st Station Pass", player) and ready_for_late_game(state, player, world),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
        elif "Aegis" in location.group and world.options.goal.value == 1:
            if world.options.cursed_aegis_cave.value == 0:
                if location.id in [54]:
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player) and ready_for_late_game(state, player, world),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.id in [55, 56]:  # Regice Chamber
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player)
                        and ready_for_late_game(state, player, world)
                        and state.has("Progressive Seal", player, 1),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.id in [57, 58]:  # Regirock Chamber
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player)
                        and ready_for_late_game(state, player, world)
                        and state.has("Progressive Seal", player, 2),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )
                elif location.id in [59, 60, 61]:  # Registeel Chamber
                    set_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Ice Aegis Cave", player)
                        and ready_for_late_game(state, player, world)
                        and state.has("Progressive Seal", player, 3),
                    )
                    if special_episode_sanity_no_exclusion(world, player):
                        add_rule(
                            world.multiworld.get_location(location.name, player),
                            lambda state: state.has("Main Game Unlock", player),
                        )

            else:
                set_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Ice Aegis Cave", player) and ready_for_late_game(state, player, world),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(location.name, player),
                        lambda state: state.has("Main Game Unlock", player),
                    )

        elif "Late" in location.group and world.options.goal.value == 1:
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player, world),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
        elif "Rule" in location.group and world.options.goal.value == 1:
            if world.options.long_location == 0:
                continue
            set_rule(
                world.multiworld.get_location(location.name, player),
                lambda state, ln=location.name: state.has(ln, player) and ready_for_late_game(state, player, world),
            )
            if special_episode_sanity_no_exclusion(world, player):
                add_rule(
                    world.multiworld.get_location(location.name, player),
                    lambda state: state.has("Main Game Unlock", player),
                )
        elif "Special" in location.group:
            continue


def mission_rules(world, player):
    for i, location in enumerate(EOS_location_table):
        if "Mission" not in location.group:
            continue

        if location.name == "Beach Cave":
            if special_episode_sanity_no_exclusion(world, player):
                for j in range(world.options.early_mission_checks.value):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
                for j in range(world.options.early_outlaw_checks.value):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
            continue

        elif location.classification == "EarlyDungeonComplete":
            for j in range(world.options.early_mission_checks.value):
                set_rule(
                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                    lambda state, ln=location.name, p=player: state.has(ln, p),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )
            for j in range(world.options.early_outlaw_checks.value):
                set_rule(
                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                    lambda state, ln=location.name, p=player: state.has(ln, p),
                )
                if special_episode_sanity_no_exclusion(world, player):
                    add_rule(
                        world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                        lambda state: state.has("Main Game Unlock", player),
                    )

        elif location.classification in ["LateDungeonComplete", "BossDungeonComplete"]:
            if world.options.goal.value == 1:
                if "Station" in location.group:
                    if world.options.sky_peak_type == 1:
                        for j in range(world.options.late_mission_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state, ln="Progressive Sky Peak", num=(location.id - 110), p=player: state.has(
                                    ln, p, num
                                )
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state, ln="Progressive Sky Peak", num=(location.id - 110), p=player: state.has(
                                    ln, p, num
                                )
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )

                    elif world.options.sky_peak_type == 2:
                        for j in range(world.options.late_mission_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state, ln=location.name, p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state, ln=location.name, p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )

                    elif world.options.sky_peak_type == 3:
                        for j in range(world.options.late_mission_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state, ln="1st Station Pass", p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )
                        for j in range(world.options.late_outlaw_checks.value):
                            set_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state, ln="1st Station Pass", p=player: state.has(ln, p)
                                and ready_for_late_game(state, player, world),
                            )
                            if special_episode_sanity_no_exclusion(world, player):
                                add_rule(
                                    world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                    lambda state: state.has("Main Game Unlock", player),
                                )

                elif location.name == "Hidden Land":
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                elif location.name == "The Nightmare":
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world)
                            and state.can_reach_location("Mt. Bristle", p)
                            and state.has(ln, p),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                            lambda state, ln=location.name, p=player: ready_for_late_game(state, p, world)
                            and state.can_reach_location("Mt. Bristle", p)
                            and state.has(ln, p),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                else:
                    for j in range(world.options.late_mission_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                            lambda state, ln=location.name, p=player: state.has(ln, p)
                            and ready_for_late_game(state, player, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Mission {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )

                    for j in range(world.options.late_outlaw_checks.value):
                        set_rule(
                            world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                            lambda state, ln=location.name, p=player: state.has(ln, p)
                            and ready_for_late_game(state, player, world),
                        )
                        if special_episode_sanity_no_exclusion(world, player):
                            add_rule(
                                world.multiworld.get_location(f"{location.name} Outlaw {j + 1}", player),
                                lambda state: state.has("Main Game Unlock", player),
                            )


def subx_rules(world, player):
    for item in subX_table:
        if item.flag_definition == "Unused" or item.default_item == "ignore":
            continue
        if world.options.goal.value == 0 and item.classification in [
            "Manaphy",
            "LateSubX",
            "Legendary",
            "Instrument",
            "SecretRank",
        ]:
            continue
        if world.options.goal.value == 0 and item.flag_definition in [
            "Recycle Shop Dungeon #4",
            "Recycle Shop Dungeon #5",
        ]:
            continue
        if world.options.goal.value == 0 and item.flag_definition == "Bag Upgrade 5":
            continue
        # if world.options.long_location.value == 0 and item.classification in ["OptionalSubX"]:
        #   continue
        if item.classification == "Rank":
            rank_toid_dict = {
                "Bronze Rank": 1,
                "Silver Rank": 2,
                "Gold Rank": 3,
                "Diamond Rank": 4,
                "Super Rank": 5,
                "Ultra Rank": 6,
                "Hyper Rank": 7,
                "Master Rank": 8,
                "Master ★ Rank": 9,
                "Master ★★ Rank": 10,
                "Master ★★★ Rank": 11,
                "Guildmaster Rank": 12,
            }
            if rank_toid_dict[item.flag_definition] > world.options.max_rank:
                continue
            # if dialga is the goal, we can't add master star rank+
            if world.options.goal.value == 0 and rank_toid_dict[item.flag_definition] > 8:
                continue
        if (
            (special_episode_sanity_no_exclusion(world, player))
            and item.classification in ["Free", "ShopItem"]
            and "Main Game" not in item.prerequisites
        ):
            add_rule(
                world.multiworld.get_location(item.flag_definition, player),
                lambda state: state.has("Main Game Unlock", player)
                or state.has("Bidoof's Wish", player)
                or state.has('Today\'s "Oh My Gosh"', player),
            )
        elif special_episode_sanity_no_exclusion(world, player):
            add_rule(
                world.multiworld.get_location(item.flag_definition, player),
                lambda state: state.has("Main Game Unlock", player),
            )
        # if (item.flag_definition == "Manaphy's Discovery") and world.options.goal.value == 0:
        # continue
        for requirement in item.prerequisites:
            if requirement == "Defeat Dialga":
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state: ready_for_late_game(state, player, world),
                )
            elif requirement == "Sky Peak Summit Pass":
                if world.options.sky_peak_type == 1:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="Progressive Sky Peak": ready_for_late_game(state, player, world)
                        and state.has(req, player, 10),
                    )
                elif world.options.sky_peak_type == 2:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="Sky Peak Summit Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
                elif world.options.sky_peak_type == 3:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="1st Station Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
            elif requirement == "7th Station Pass":
                if world.options.sky_peak_type == 1:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="Progressive Sky Peak": ready_for_late_game(state, player, world)
                        and state.has(req, player, 7),
                    )
                elif world.options.sky_peak_type == 2:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="7th Station Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
                elif world.options.sky_peak_type == 3:
                    add_rule(
                        world.multiworld.get_location(item.flag_definition, player),
                        lambda state, req="1st Station Pass": ready_for_late_game(state, player, world)
                        and state.has(req, player),
                    )
            elif requirement in ["ProgressiveBag1", "ProgressiveBag2", "ProgressiveBag3"]:
                bag_num_str = requirement[-1]
                bag_num = int(bag_num_str)
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Bag Upgrade", p=player, num=bag_num: state.has(req, p, num),
                )

            elif requirement in ["3 Early", "5 Early", "10 Early"]:
                dungeon_num_str = requirement[0:2]
                dungeon_num = int(dungeon_num_str)
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="EarlyDungeons", p=player, num=dungeon_num: state.has_group(req, p, num),
                )

            elif requirement == "Hidden Land":
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state,
                    req="Relic Fragment Shard",
                    p=player,
                    num=world.options.required_fragments.value: state.has(req, p, num),
                )
            elif requirement == "Ice Seal" and world.options.cursed_aegis_cave.value == 0:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Progressive Seal", p=player, num=1: state.has(req, p, num),
                )

            elif requirement == "Rock Seal" and world.options.cursed_aegis_cave.value == 0:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Progressive Seal", p=player, num=2: state.has(req, p, num),
                )

            elif requirement == "Steel Seal" and world.options.cursed_aegis_cave.value == 0:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Progressive Seal", p=player, num=3: state.has(req, p, num),
                )

            elif requirement == "All Mazes":
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req="Dojo Dungeons", p=player: state.has_group(req, p, 10),
                )
            elif requirement == "Bidoof's Wish":
                if world.options.exclude_special.value:
                    continue
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req=requirement, p=player: state.has(req, p),
                )
            elif requirement == "Main Game":
                continue
            else:
                add_rule(
                    world.multiworld.get_location(item.flag_definition, player),
                    lambda state, req=requirement, p=player: state.has(req, p),
                )


def special_episode_sanity_no_exclusion(world, player) -> bool:
    if world.options.special_episode_sanity.value == 1 and not world.options.exclude_special.value:
        return True
    else:
        return False

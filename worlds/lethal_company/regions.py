from BaseClasses import MultiWorld, Region, Location, ItemClassification
from .locations import generate_bestiary_moons, generate_scrap_moons, locations, generate_scrap_moons_alt
from .rules import check_item_accessible, can_buy
from .options import LCOptions
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import LethalCompanyWorld


def create_regions(options: LCOptions, world: "LethalCompanyWorld"):
    multiworld: MultiWorld = world.multiworld
    player: int = world.player

    menu: Region = Region("Menu", player, multiworld)
    multiworld.regions.append(menu)
    ship: Region = Region("Ship", player, multiworld)
    multiworld.regions.append(ship)
    starting_moon: Region = Region(world.initial_world, player, multiworld)
    multiworld.regions.append(starting_moon)
    terminal: Region = Region("Terminal", player, multiworld)
    multiworld.regions.append(terminal)
    logs: list[Region] = []
    bestiary: list[Region] = []
    scrap: list[Region] = []
    moon_regions: list[Region] = []
    company_building: Region = Region("Company Building", player, multiworld)
    multiworld.regions.append(company_building)
    quotas: Region = Region("Quotas", player, multiworld)
    multiworld.regions.append(quotas)
    victory: Region = Region("Victory", player, multiworld)
    multiworld.regions.append(victory)

    if options.game_mode.value == 2:
        company_building.connect(victory,
                                 rule=lambda state: (state.has("Company Credit", player,
                                                               count=world.required_credit_count)))
    elif options.game_mode.value == 0:
        company_building.connect(victory, rule=lambda state: (state.has_all(world.slot_item_data.moons, player)))

    menu.connect(ship, rule=lambda state: True)
    ship.connect(starting_moon, rule=lambda state: True)
    ship.connect(terminal, rule=lambda state: state.has("Terminal", player) or options.randomize_terminal.value == 0)
    for moon in world.slot_item_data.moons:
        if not moon == world.initial_world:
            moon_regions.append(Region(moon, player, multiworld))
            multiworld.regions.append(moon_regions[-1])
            terminal.connect(moon_regions[-1], rule=lambda state, m=moon: state.has(m, player))

    terminal.connect(company_building, rule=lambda state: (state.has("Company Building", player)
                                                           or options.randomize_company_building == 0))
    company_building.connect(quotas, rule=lambda state: (state.has("Inventory Slot", player, 3)
                                                         and state.has("Stamina Bar", player, 2)))

    bestiary_moons = generate_bestiary_moons(world, options.min_monster_chance.value/100.0)
    scrap_moons = generate_scrap_moons(world, options.min_scrap_chance.value/100.0) if options.modify_scrap_spawns.value == 0 \
        else generate_scrap_moons_alt(world)


    if options.game_mode.value == 1:
        # get a list of all scrap that isn't common or excluded and randomly pick out scrap to be part of the goal
        # when picking scrap, try to ensure that the player must visit at least 1/3 of their moons to find them all
        # keep selecting until we've met the requirement

        import logging
        random_scrap_required = options.collectathon_random_scrap.value
        target_unique_moons = min(len(world.slot_item_data.moons) // 3, random_scrap_required - 1)
        scrap_choices = {k: v for k,v in scrap_moons.items() if "excluded" not in v and "Common" not in v and 
                         "AP Apparatus" not in k and "Archipelago Chest" not in k}
        # ap_apparati = {k: v for k,v in scrap_moons.items() if "AP Apparatus" in v}

        if options.exclude_egg.value: scrap_choices.pop("Sapsucker Egg")
        if options.exclude_hive.value: scrap_choices.pop("Hive")
        if options.exclude_killing.value: 
            scrap_choices.pop("Shotgun")
            scrap_choices.pop("Kitchen knife")

        max_moons = max(len(world.slot_item_data.moons) // 4, 1)
        filtered_choices = dict(filter(lambda s, m=max_moons: len(s[1]) <= m, scrap_choices.items()))
        while len(filtered_choices) < 1 and len(scrap_choices) > 0:
            max_moons += 1
            filtered_choices = dict(filter(lambda s, m=max_moons: len(s[1]) <= m, scrap_choices.items()))

        selected_scrap = []
        seen_moons = []
        selected_scrap_count = 0

        # randomly pick scrap to be part of the goal until we have enough or run out
        # only add the scrap to the goal if one of the following conditions is true:
        #   we don't need any more scrap from unique moons
        #   the selected scrap doesn't spawn on the same moons as any chosen scrap
        #   the only way to get enough random scrap for the goal is to pick EVERY remaining scrap
        #
        # to avoid the third condition as much as possible, filter the list for scrap that only spawn on a few (less than max_moons) moons and gradually increase max_moons over time
        while selected_scrap_count < random_scrap_required and len(scrap_choices) > 0:
            scrap_choice = list(filtered_choices.keys())[world.random.randint(0, len(filtered_choices) - 1)]
            if selected_scrap_count >= target_unique_moons or \
                        len(set(seen_moons).intersection(set(filtered_choices[scrap_choice]))) == 0 or \
                        len(scrap_choices) <= random_scrap_required - selected_scrap_count:
                selected_scrap.append(scrap_choice)
                seen_moons.extend(set(scrap_choices[scrap_choice]).difference(set(seen_moons)))
                selected_scrap_count += 1
            scrap_choices.pop(scrap_choice)
            if selected_scrap_count >= target_unique_moons and max_moons < len(world.slot_item_data.moons):
                max_moons = len(world.slot_item_data.moons)
                filtered_choices = dict(filter(lambda s, m=max_moons: len(s[1]) <= m, scrap_choices.items()))
            elif len(filtered_choices) <= 1:
                max_moons += 2
                filtered_choices = dict(filter(lambda s, m=max_moons: len(s[1]) <= m, scrap_choices.items()))
                while len(filtered_choices) < 1 and len(scrap_choices) > 0:
                    max_moons += 1
                    filtered_choices = dict(filter(lambda s, m=max_moons: len(s[1]) <= m, scrap_choices.items()))
            else:
                filtered_choices.pop(scrap_choice)

        logging.info(f"Selected scrap: {selected_scrap}\nSeen moons: {seen_moons}")

        if selected_scrap_count < random_scrap_required: raise AssertionError(f"Not enough valid scrap for {world.player_name}'s Collectathon goal. Consider lowering collectathon_random_scrap or min_scrap_chance")

        world.spoiler_text += f"\n{world.player_name}'s Required Collectathon scrap: {selected_scrap}"

        # for each required scrap, have at least one of the moons it spawns on
        company_building.connect(victory, rule=lambda state: {
            (state.has_any((moon for moon in scrap_moons[scrap] if "excluded" not in moon), player)) 
                for scrap in selected_scrap
        })

        world.required_collectathon_scrap = selected_scrap


    for monster in world.bestiary_names:
        bestiary.append(Region(monster, player, multiworld))
        multiworld.regions.append(bestiary[-1])
        can_spawn = bestiary_moons[monster]
        for moon in can_spawn:
            if moon != "excluded":
                multiworld.get_region(moon, player).connect(multiworld.get_region(monster, player),
                                                            rule=lambda state: (state.has("Scanner", player)
                                                                                or options.randomize_scanner.value == 0))

    if options.scrapsanity.value == 1:
        for scrap_name in world.scrap_names:
            scrap.append(Region(scrap_name, player, multiworld))
            multiworld.regions.append(scrap[-1])

        for scrap_name in scrap_moons.keys():
            for moon in scrap_moons[scrap_name]:
                if moon == "Common":
                    for r_moon in world.slot_item_data.moons:
                        multiworld.get_region(r_moon, player).connect(multiworld.get_region(scrap_name, player),
                                                                      rule=lambda state, s_name=scrap_name:
                                                                      (state.has("Stamina Bar", player)
                                                                        and ((check_item_accessible(state, "Shovel",
                                                                                                  player, options)
                                                                                and (state.has("Stamina Bar", player, 3)
                                                                                    or (s_name != "Sapsucker Egg")))
                                                                            or (s_name != "Shotgun"
                                                                                and s_name != "Kitchen knife"
                                                                                and s_name != "Sapsucker Egg"))))
                elif moon != "excluded":
                    multiworld.get_region(moon, player).connect(multiworld.get_region(scrap_name, player),
                                                                rule=lambda state, s_name=scrap_name:
                                                                (state.has("Stamina Bar", player)
                                                                    and ((check_item_accessible(state, "Shovel",
                                                                                                player, options)
                                                                            and (state.has("Stamina Bar", player, 3)
                                                                                or (s_name != "Sapsucker Egg")))
                                                                        or (s_name != "Shotgun"
                                                                            and s_name != "Kitchen knife"
                                                                            and s_name != "Sapsucker Egg"))))

    logs.append(Region("Behind the Wall", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("March", player).connect(logs[0])
    logs.append(Region("Mummy", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Assurance", player).connect(logs[1])
    logs.append(Region("Swing of Things", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Experimentation", player).connect(logs[2])
    logs.append(Region("Autopilot", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Experimentation", player).connect(logs[3], rule=lambda state: state.has("Stamina Bar", player))
    logs.append(Region("Golden Planet", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Rend", player).connect(logs[4])
    logs.append(Region("Goodbye", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Offense", player).connect(logs[5])
    logs.append(Region("Screams", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Assurance", player).connect(logs[6], rule=lambda state: state.has("Stamina Bar", player))
    logs.append(Region("Idea", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Adamance", player).connect(logs[7])
    logs.append(Region("Nonsense", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Rend", player).connect(logs[8])
    logs.append(Region("Hiding", player, multiworld))
    multiworld.regions.append(logs[-1])
    company_building.connect(logs[9])
    logs.append(Region("Real Job", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Vow", player).connect(logs[10])
    logs.append(Region("Desmond", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Dine", player).connect(logs[11], rule=lambda state: state.has("Stamina Bar", player))
    logs.append(Region("Team Synergy", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Adamance", player).connect(logs[12])
    logs.append(Region("Letter of Resignation", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Titan", player).connect(logs[13], rule=lambda state: state.has("Stamina Bar", player))
    logs.append(Region("Work", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("Artifice", player).connect(logs[14])

    # Generate locations
    for i in range(options.grade_locations_per_moon.value):
        for moon in world.slot_item_data.moons:
            
            add_location(player, f"{moon} Grade Location {i+1}", multiworld.get_region(moon, player))
            multiworld.get_location(f"{moon} Grade Location {i+1}", player).access_rule = (lambda state:
                                                                                        (state.has("Stamina Bar", player)
                                                                                            or options.starting_stamina_bars > 0)
                                                                                        and state.has("Inventory Slot", player, 2))

    for i in range(options.num_quotas.value):
        add_location(player, f"Quota Location {i+1}", quotas)

    for log in world.log_names:
        add_location(player, f"Log - {log}", multiworld.get_region(log, player))

    for monster in world.bestiary_names:
        if len(bestiary_moons[monster]) < 1:
            import logging
            logging.warning(f"Cannot find any moon that spawns Monster - {monster} for player {world.player_name}. This monster may not be scannable.")
        #else:
        add_location(player, f"Bestiary Entry - {monster}", multiworld.get_region(monster, player))
        if len(bestiary_moons[monster]) < 1 or (len(bestiary_moons[monster]) <= 2 and bestiary_moons[monster][-1] == 'excluded'):
            multiworld.get_location(f"Bestiary Entry - {monster}", player).item_rule = lambda item: \
                    (item.classification == ItemClassification.filler or
                     item.classification == ItemClassification.trap)

    if options.scrapsanity.value == 1:
        for scrap_name in world.scrap_names:
            if scrap_name not in scrap_moons: 
                continue
            if len(scrap_moons[scrap_name]) < 1:
                import logging
                logging.warning(f"Cannot find any moon that spawns Scrap - {scrap_name} for player {world.player_name}. This scrap may not be obtainable.")
            #else:
            add_location(player, f"Scrap - {scrap_name}", multiworld.get_region(scrap_name, player))

            if len(scrap_moons[scrap_name]) < 1 or (len(scrap_moons[scrap_name]) <= 2 and scrap_moons[scrap_name][-1] == 'excluded'):
                multiworld.get_location(f"Scrap - {scrap_name}", player).item_rule = lambda item: \
                    (item.classification == ItemClassification.filler or
                     item.classification == ItemClassification.trap)


def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location]))
    region.locations[-1].parent_region = region

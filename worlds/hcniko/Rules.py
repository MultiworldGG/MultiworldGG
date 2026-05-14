from BaseClasses import CollectionState

TICKETS = ["Hairball City Ticket", "Turbine Town Ticket", "Salmon Creek Forest Ticket", "Public Pool Ticket",
           "Bathhouse Ticket", "Tadpole HQ Ticket", "Gary's Garden Ticket"]


def is_employee(state: CollectionState, player):
    return state.has("Coin", player, 76)


def has_enough_coins(state: CollectionState, player, count: int):
    return state.has("Coin", player, count)


def has_enough_cassettes(state: CollectionState, player, count: int):
    return state.has("Cassette", player, count * 5)


def has_all_tickets(state: CollectionState, player):
    return (state.has("Hairball City Ticket", player)
            and state.has("Turbine Town Ticket", player)
            and state.has("Salmon Creek Forest Ticket", player)
            and state.has("Public Pool Ticket", player)
            and state.has("Bathhouse Ticket", player)
            and state.has("Tadpole HQ Ticket", player))


def has_tickets(state: CollectionState, player, required_tickets):
    ticket_count = sum(1 for ticket in TICKETS if state.has(ticket, player))
    return ticket_count >= required_tickets


def has_textbox(state: CollectionState, player, world, level):
    textbox = world.options.textbox.value
    if textbox == 1:
        return state.has("Textbox", player)
    elif textbox == 2:
        if level == "Gary's Garden" and not world.options.shuffle_garys_garden.value:
            return True
        return state.has(f"{level} Textbox", player)
    else:
        return True


def has_access_garden(state: CollectionState, player, world):
    access_option = world.options.access_garys_garden.value
    if access_option == 1:
        return (state.has("Gary's Garden Ticket", player)
                and state.has("Tadpole HQ Ticket", player)
                and (has_textbox(state, player, world, "Tadpole HQ"))
                and (world.options.swimming.value != 1 or state.has("Swim Course", player)))
    elif access_option == 2:
        return (state.has("Gary's Garden Ticket", player)
                and (has_textbox(state, player, world, "Gary's Garden")))
    else:
        return (state.has("Tadpole HQ Ticket", player)
                and (has_textbox(state, player, world, "Tadpole HQ"))
                and (world.options.swimming.value != 1 or state.has("Swim Course", player)))


def has_party_ticket(state: CollectionState, player, world):
    if world.options.textbox.value != 0 and world.options.chatsanity.value == 1:
        return state.has("Party Invitation", player) and (state.has("Textbox", player) or state.has("Home Textbox", player))
    elif world.options.chatsanity.value == 1:
        return state.has("Party Invitation", player)
    else:
        return state.can_reach_region("Home", player)


def has_enough_seeds(state: CollectionState, player, world, count: int):
    if world.options.goal_completion.value == 3:
        return state.has("Gary's Garden Seed", player, count)
    else:
        return True


def has_helped_everyone(state: CollectionState, player, world):
    if world.options.goal_completion.value == 4:
        return (state.can_reach_location("Home - Give High Frog Lunchbox", player)
                and state.can_reach_location("Hairball City - BIG VOLLEY", player)
                and state.can_reach_location("Hairball City - Dustan on Lighthouse", player)
                and state.can_reach_location("Hairball City - Gunter on Skyscraper", player)
                and state.can_reach_location("Hairball City - Nina", player)
                and state.can_reach_location("Hairball City - Moomy", player)
                and state.can_reach_location("Hairball City - Fish with Fischer", player)
                and state.can_reach_location("Hairball City - Game Kid", player)
                and state.can_reach_location("Hairball City - Blippy Dog", player)
                and state.can_reach_location("Hairball City - Blippy", player)
                and state.can_reach_location("Hairball City - Serschel & Louist", player)
                and state.can_reach_location("Hairball City - Little Gabi's Flowers", player)
                and state.can_reach_location("Hairball City - Blessley", player)
                and state.can_reach_location("Turbine Town - Blippy Dog", player)
                and state.can_reach_location("Turbine Town - Blippy", player)
                and state.can_reach_location("Turbine Town - Serschel & Louist", player)
                and state.can_reach_location("Turbine Town - Dustan on Wind Turbine", player)
                and state.can_reach_location("Turbine Town - Little Gabi's Flowers", player)
                and state.can_reach_location("Turbine Town - Blessley", player)
                and state.can_reach_location("Turbine Town - AIR VOLLEY", player)
                and state.can_reach_location("Turbine Town - Pelly the Engineer", player)
                and state.can_reach_location("Turbine Town - Fish with Fischer", player)
                and state.can_reach_location("Salmon Creek Forest - Dustan on Mountain", player)
                and state.can_reach_location("Salmon Creek Forest - Nina", player)
                and state.can_reach_location("Salmon Creek Forest - Stijn & Melissa", player)
                and state.can_reach_location("Salmon Creek Forest - Treeman", player)
                and state.can_reach_location("Salmon Creek Forest - Blessley", player)
                and state.can_reach_location("Salmon Creek Forest - Little Gabi's Flowers", player)
                and state.can_reach_location("Salmon Creek Forest - Game Kid", player)
                and state.can_reach_location("Salmon Creek Forest - Blippy", player)
                and state.can_reach_location("Salmon Creek Forest - Serschel & Louist", player)
                and state.can_reach_location("Salmon Creek Forest - Blippy Dog", player)
                and state.can_reach_location("Salmon Creek Forest - Fish with Fischer", player)
                and state.can_reach_location("Salmon Creek Forest - SPORTVIVAL", player)
                and state.can_reach_location("Salmon Creek Forest - Moomy", player)
                and state.can_reach_location("Public Pool - Blippy", player)
                and state.can_reach_location("Public Pool - Frogtective", player)
                and state.can_reach_location("Public Pool - Blippy Dog", player)
                and state.can_reach_location("Public Pool - Little Gabi's Flowers", player)
                and state.can_reach_location("Public Pool - Blessley", player)
                and state.can_reach_location("Public Pool - SPORTVIVAL VOLLEY", player)
                and state.can_reach_location("Public Pool - Fish with Fischer", player)
                and state.can_reach_location("Bathhouse - Poppy", player)
                and state.can_reach_location("Bathhouse - Fish with Fischer", player)
                and state.can_reach_location("Bathhouse - Blessley", player)
                and state.can_reach_location("Bathhouse - Little Gabi's Flowers", player)
                and state.can_reach_location("Bathhouse - Blippy Dog", player)
                and state.can_reach_location("Bathhouse - Blippy", player)
                and state.can_reach_location("Bathhouse - Dustan on Bathhouse", player)
                and state.can_reach_location("Bathhouse - Game Kid", player)
                and state.can_reach_location("Bathhouse - LONG VOLLEY", player)
                and state.can_reach_location("Bathhouse - Nina", player)
                and state.can_reach_location("Bathhouse - Serschel & Louist", player)
                and state.can_reach_location("Bathhouse - Moomy", player)
                and state.can_reach_location("Tadpole HQ - Blippy", player)
                and state.can_reach_location("Tadpole HQ - Little Gabi's Flowers", player)
                and state.can_reach_location("Tadpole HQ - Blippy Dog", player)
                and state.can_reach_location("Tadpole HQ - Blessley", player)
                and state.can_reach_location("Tadpole HQ - Serschel & Louist", player)
                and state.can_reach_location("Tadpole HQ - Frog King", player)
                and state.can_reach_location("Tadpole HQ - HUGE VOLLEY", player)
                and state.can_reach_location("Tadpole HQ - Fish with Fischer", player)
                and state.can_reach_location("Gary's Garden - Gunter & Little Gabi", player)
                and state.can_reach_location("Hairball City - Mitch", player)
                and state.can_reach_location("Hairball City - Mai", player)
                and state.can_reach_location("Turbine Town - Mitch", player)
                and state.can_reach_location("Turbine Town - Mai", player)
                and state.can_reach_location("Salmon Creek Forest - Mai", player)
                and state.can_reach_location("Salmon Creek Forest - Mitch", player)
                and state.can_reach_location("Public Pool - Mitch", player)
                and state.can_reach_location("Public Pool - Mai", player)
                and state.can_reach_location("Bathhouse - Mitch", player)
                and state.can_reach_location("Bathhouse - Mai", player)
                and state.can_reach_location("Tadpole HQ - Mai", player)
                and state.can_reach_location("Tadpole HQ - Mitch", player)
                and state.can_reach_location("Gary's Garden - Mai", player)
                and state.can_reach_location("Gary's Garden - Mitch", player))
    else:
        return True


def has_access_to(state: CollectionState, player, location):
    return state.can_reach_location(location, player)


def get_region_rules(player, world):
    options = world.options
    if options.min_elevator_cost.value == options.max_elevator_cost.value:
        world.kiosk_cost["Elevator"] = options.max_elevator_cost.value
    else:
        world.kiosk_cost["Elevator"] = world.random.randint(options.min_elevator_cost.value,
                                                            options.max_elevator_cost.value)
    return {
        "Home -> Hairball City":
            lambda state: state.has("Hairball City Ticket", player),
        "Home -> Turbine Town":
            lambda state: state.has("Turbine Town Ticket", player),
        "Home -> Salmon Creek Forest":
            lambda state: state.has("Salmon Creek Forest Ticket", player),
        "Home -> Public Pool":
            lambda state: state.has("Public Pool Ticket", player),
        "Home -> Bathhouse":
            lambda state: state.has("Bathhouse Ticket", player),
        "Home -> Tadpole HQ":
            lambda state: state.has("Tadpole HQ Ticket", player),
        "Home -> Gary's Garden":
            lambda state: has_access_garden(state, player, world),
        "Tadpole HQ -> Home Party":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Home -> ChatHome":
            lambda state: has_textbox(state, player, world, "Home"),
        "Home -> ChatParty":
            lambda state: has_party_ticket(state, player, world),
        #"Home -> Chatsanity":
        #    lambda state: has_textbox(state, player, world, "Home"),
        "Hairball City -> ChatHC":
            lambda state: has_textbox(state, player, world, "Hairball City"),
        "Turbine Town -> ChatTT":
            lambda state: has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest -> ChatSCF":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool -> ChatPP":
            lambda state: has_textbox(state, player, world, "Public Pool"),
        "Bathhouse -> ChatBath":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Tadpole HQ -> ChatHQ":
            lambda state: has_textbox(state, player, world, "Tadpole HQ"),
        "Gary's Garden -> ChatGarden":
            lambda state: has_textbox(state, player, world, "Gary's Garden"),
        "Hairball City -> BugsHC":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Turbine Town -> BugsTT":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Salmon Creek Forest -> BugsSCF":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Public Pool -> BugsPP":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Bathhouse -> BugsBath":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Tadpole HQ -> BugsHQ":
            lambda state: (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Hairball City -> ApplesHC":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Turbine Town -> ApplesTT":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Salmon Creek Forest -> ApplesSCF":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Public Pool -> ApplesPP":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Bathhouse -> ApplesBath":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
        "Tadpole HQ -> ApplesHQ":
            lambda state: (options.applebasket.value != 1 or state.has("Apple Basket", player)),
    }


def get_location_rules(player, world):
    options = world.options
    lowest_cost: int = options.min_kiosk_cost.value
    highest_cost: int = options.max_kiosk_cost.value
    cost_increment: int = (highest_cost - lowest_cost) // len(world.kiosk_cost)
    min_difference = 4
    last_cost = 0

    kiosk_names = list(world.kiosk_cost.keys())
    kiosk_names.remove("Elevator")
    if options.shuffle_kiosk_reward.value == 1:
        world.random.shuffle(kiosk_names)

    if options.shuffle_kiosk_reward.value == 0:
        for i, kiosk_name in enumerate(kiosk_names):
            if i >= 3:
                cost = 1 + 5 + (5 * i)
            else:
                cost = 1 + (5 * i)
            world.kiosk_cost[kiosk_name] = cost
    else:
        for i, kiosk_name in enumerate(kiosk_names):
            min_range: int = lowest_cost + (cost_increment * i)
            if min_range >= highest_cost:
                min_range = highest_cost - 1

            value: int = world.random.randint(min_range,
                                              min(highest_cost, max(lowest_cost, last_cost + cost_increment)))
            cost = world.random.randint(value, min(value + cost_increment, highest_cost))
            if i >= 1:
                if last_cost + min_difference > cost:
                    cost = last_cost + min_difference

            cost = min(cost, highest_cost)
            world.kiosk_cost[kiosk_name] = cost
            last_cost = cost

    # Don't count Gary's Garden locations when they are disabled
    cassette_locations = list(world.cassette_cost.keys())
    if not options.shuffle_garys_garden.value:
        cassette_locations = [
            loc for loc in cassette_locations
            if not loc.startswith("Gary's Garden")
        ]
    cassette_location_count = len(cassette_locations)
    cassette_values = list(range(1, cassette_location_count + 1))

    if options.cassette_logic.value == 2:
        world.random.shuffle(cassette_values)
        for i, location_name in enumerate(cassette_locations):
            world.cassette_cost[location_name] = cassette_values[i]
    elif options.cassette_logic.value == 0:
        cassette_locations = list(world.cassette_cost.keys())
        for i, location_name in enumerate(cassette_locations):
            if "Mitch" in location_name:
                world.cassette_cost[location_name] = 5
            elif "Mai" in location_name:
                world.cassette_cost[location_name] = 10
    else:
        for i, location_name in enumerate(cassette_locations):
            world.cassette_cost[location_name] = cassette_values[i]

    if options.min_custom_goal_cost.value == options.max_custom_goal_cost.value:
        world.custom_goal_required = options.max_custom_goal_cost.value
    else:
        world.custom_goal_required = world.random.randint(options.min_custom_goal_cost.value, options.max_custom_goal_cost.value)

    return {
        # Victory
        "Best Employee!":
            lambda state: is_employee(state, player),
        "Coin Collector!":
            lambda state: has_enough_coins(state, player, world.custom_goal_required),
        "Restored Gary's Garden!":
            lambda state: has_enough_seeds(state, player, world, 10),
        "Helped Everyone!":
            lambda state: has_helped_everyone(state, player, world),

        "Home - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Home"]))
                          and has_textbox(state, player, world, "Home"),
        "Hairball City - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Hairball City"]))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Turbine Town"]))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Salmon Creek Forest"]))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Public Pool"]))
                          and has_textbox(state, player, world, "Public Pool"),
        "Bathhouse - Kiosk":
            lambda state: (state.has("Coin", player, world.kiosk_cost["Kiosk Bathhouse"]))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Achievement - Employee Of The Month!":
            lambda state: is_employee(state, player),
        "Achievement - Bottled Up":
            lambda state: state.has("Hairball City Ticket", player)
                          and state.has("Turbine Town Ticket", player)
                          and state.has("Salmon Creek Forest Ticket", player)
                          and (state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player))
                          and state.has("Public Pool Ticket", player)
                          and state.has("Bathhouse Ticket", player)
                          and state.has("Tadpole HQ Ticket", player)
                          and has_enough_coins(state, player, world.kiosk_cost["Elevator"])
                          and (options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Achievement - Hopeless Romantic":
            lambda state: state.has("Hairball City Ticket", player)
                          and state.has("Turbine Town Ticket", player)
                          and state.has("Salmon Creek Forest Ticket", player)
                          and state.has("Public Pool Ticket", player)
                          and state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Hairball City")
                          and has_textbox(state, player, world, "Turbine Town")
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and has_textbox(state, player, world, "Public Pool")
                          and has_textbox(state, player, world, "Bathhouse"),
        "Achievement - Volley Dreams":
            lambda state: has_all_tickets(state, player)
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.swimming.value != 1
                          or options.precisejumps.value == 1
                          or state.has("Swim Course", player)),
        "Achievement - Snail Fashion Show":
            lambda state: has_all_tickets(state, player),
        "Turbine Town - Dustan on Wind Turbine":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Turbine Town Key", player))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Public Pool - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Public Pool Key", player))
                          and has_textbox(state, player, world, "Public Pool")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Poppy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2))
                          and has_textbox(state, player, world, "Bathhouse")
                          and (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Tadpole HQ - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Tadpole HQ Key", player))
                          and has_textbox(state, player, world, "Tadpole HQ")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Above Frog Statue":
            lambda state: state.has("Key", player, 7)
                          or state.has("Hairball City Key", player)
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Salmon Creek Forest - Inside Locked Cave":
            lambda state: state.has("Key", player, 7)
                          or state.has("Salmon Creek Forest Key", player),
        "Bathhouse - Mahjong Hideout":
            lambda state: state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2),
        "Salmon Creek Forest - Fish with Fischer":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                           and (options.fishsanity.value != 2 or state.has("Salmon Creek Forest Fish", player, 5))
                           and has_textbox(state, player, world, "Salmon Creek Forest")
                           and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - SPORTVIVAL":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Hairball City - Nina":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Moomy":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.seedsanity.value != 2 or state.has("Hairball City Seed", player, 10))
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Game Kid":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Blippy Dog":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.bonesanity.value != 2 or state.has("Hairball City Bone", player, 5))
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Hairball City - Blippy":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Hairball City - Serschel & Louist":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Blippy Dog":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.bonesanity.value != 2 or state.has("Turbine Town Bone", player, 5))
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Blippy":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Turbine Town - Serschel & Louist":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Turbine Town")
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Salmon Creek Forest - Game Kid":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Blippy":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Serschel & Louist":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool - SPORTVIVAL VOLLEY":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Public Pool")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Blessley":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Public Pool")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Public Pool - Little Gabi's Flowers":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.flowersanity.value != 2 or state.has("Public Pool Flower", player, 3))
                          and has_textbox(state, player, world, "Public Pool"),
        "Bathhouse - Fish with Fischer":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                           and (options.fishsanity.value != 2 or state.has("Bathhouse Fish", player, 5))
                          and has_textbox(state, player, world, "Bathhouse")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Blessley":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and has_textbox(state, player, world, "Bathhouse")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player)),
        "Bathhouse - Little Gabi's Flowers":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.flowersanity.value != 2 or state.has("Bathhouse Flower", player, 3))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Blippy Dog":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.bonesanity.value != 2 or state.has("Bathhouse Bone", player, 5))
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Bathhouse - Blippy":
            lambda state: (state.has("Key", player, 7)
                          or state.has("Bathhouse Key", player, 2)) and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Dustan - Meeting First Time":
            lambda state: (has_access_to(state, player, "Hairball City - Dustan on Lighthouse")
                           or has_access_to(state, player, "Turbine Town - Dustan on Wind Turbine")
                           or has_access_to(state, player, "Salmon Creek Forest - Dustan on Mountain")
                           or has_access_to(state, player, "Bathhouse - Dustan on Bathhouse"))
                          and (has_textbox(state, player, world, "Hairball City")
                           or has_textbox(state, player, world, "Turbine Town")
                           or has_textbox(state, player, world, "Salmon Creek Forest")
                           or has_textbox(state, player, world, "Bathhouse")),
        # Cassette
        "Hairball City - Mitch":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Hairball City - Mitch"])
                               or state.has("Hairball City Cassette", player, world.cassette_cost["Hairball City - Mitch"])))
                          and has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Mai":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Hairball City - Mai"])
                               or state.has("Hairball City Cassette", player, world.cassette_cost["Hairball City - Mai"])))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Mitch":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Turbine Town - Mitch"])
                               or state.has("Turbine Town Cassette", player, world.cassette_cost["Turbine Town - Mitch"])))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Turbine Town - Mai":
            lambda state: ((state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Turbine Town - Mai"])
                               or state.has("Turbine Town Cassette", player, world.cassette_cost["Turbine Town - Mai"])))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest - Mai":
            lambda state: ((has_enough_cassettes(state, player, world.cassette_cost["Salmon Creek Forest - Mai"])
                               or state.has("Salmon Creek Forest Cassette", player, world.cassette_cost["Salmon Creek Forest - Mai"]))
                          and (state.has("Key", player, 7)
                               or state.has("Salmon Creek Forest Key", player))
                          and (state.has("Contact List 1", player)
                               or state.has("Progressive Contact List", player, 1)))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Salmon Creek Forest - Mitch"])
                               or state.has("Salmon Creek Forest Cassette", player, world.cassette_cost["Salmon Creek Forest - Mitch"]))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Public Pool - Mitch":
            lambda state: ((state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (has_enough_cassettes(state, player, world.cassette_cost["Public Pool - Mitch"])
                               or state.has("Public Pool Cassette", player, world.cassette_cost["Public Pool - Mitch"])))
                          and has_textbox(state, player, world, "Public Pool"),
        "Public Pool - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Public Pool - Mai"])
                               or state.has("Public Pool Cassette", player, world.cassette_cost["Public Pool - Mai"]))
                          and has_textbox(state, player, world, "Public Pool"),
        "Bathhouse - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Bathhouse - Mitch"])
                               or state.has("Bathhouse Cassette", player, world.cassette_cost["Bathhouse - Mitch"]))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Bathhouse - Mai"])
                               or state.has("Bathhouse Cassette", player, world.cassette_cost["Bathhouse - Mai"]))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Tadpole HQ - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Tadpole HQ - Mai"])
                               or state.has("Tadpole HQ Cassette", player, world.cassette_cost["Tadpole HQ - Mai"]))
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Tadpole HQ - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Tadpole HQ - Mitch"])
                               or state.has("Tadpole HQ Cassette", player, world.cassette_cost["Tadpole HQ - Mitch"]))
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Gary's Garden - Mai":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Gary's Garden - Mai"])
                               or state.has("Gary's Garden Cassette", player, world.cassette_cost["Gary's Garden - Mai"]))
                          and has_textbox(state, player, world, "Gary's Garden"),
        "Gary's Garden - Mitch":
            lambda state: (has_enough_cassettes(state, player, world.cassette_cost["Gary's Garden - Mitch"])
                               or state.has("Gary's Garden Cassette", player, world.cassette_cost["Gary's Garden - Mitch"]))
                          and has_textbox(state, player, world, "Gary's Garden"),
        # Fish
        "Salmon Creek Forest - Bass":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Catfish":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Pike":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Salmon":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Trout":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Anglerfish":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Clione":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Little Wiggly Guy":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Jellyfish":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Pufferfish":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Hairball City Fish", player, 5))
                          and has_textbox(state, player, world, "Hairball City")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Turbine Town Fish", player, 5))
                          and has_textbox(state, player, world, "Turbine Town")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Public Pool Fish", player, 5))
                          and has_textbox(state, player, world, "Public Pool")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Fish with Fischer":
            lambda state: (options.fishsanity.value != 2 or state.has("Tadpole HQ Fish", player, 5))
                          and has_textbox(state, player, world, "Tadpole HQ")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        # Snail Shop
        "Snail Shop - Bowtie":
            lambda state: has_tickets(state, player, 4),  # 10000$
        "Snail Shop - Motorcycle":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Sunglasses":
            lambda state: has_tickets(state, player, 3),  # 2000$
        "Snail Shop - Mahjong":
            lambda state: has_tickets(state, player, 1),  # 100$
        "Snail Shop - Cap":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - King Staff":
            lambda state: has_tickets(state, player, 4),  # 10000$
        "Snail Shop - Mouse":
            lambda state: has_tickets(state, player, 3),  # 1000$
        "Snail Shop - Clown Face":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Cat":
            lambda state: has_tickets(state, player, 3),  # 1000$
        "Snail Shop - Bandanna":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Stars":
            lambda state: has_tickets(state, player, 2),  # 500$
        "Snail Shop - Sword":
            lambda state: has_tickets(state, player, 3),  # 3000$
        "Snail Shop - Top hat":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Snail Shop - Glasses":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Snail Shop - Flower":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Snail Shop - Small Hat":
            lambda state: has_tickets(state, player, 1),  # 50$
        "Tadpole HQ - Ledge Above Elevator":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        # Seedsanity
        "Hairball City - Seed By Nina":
            lambda state: state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Upper Flowerbed":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed On Top Of Lighthouse":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed On Top Of Palm Tree":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Train":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Wood Posts In Water":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Frog Of Destruction":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Frog Statue":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Mitch":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Hairball City - Seed By Turbine":
            lambda state: state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1),
        "Salmon Creek Forest - Moomy":
            lambda state: (options.seedsanity.value != 2 or state.has("Salmon Creek Forest Seed", player, 10))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Bathhouse - Moomy":
            lambda state: (options.seedsanity.value != 2 or state.has("Bathhouse Seed", player, 10))
                          and has_textbox(state, player, world, "Bathhouse"),
        # Flowersanity
        "Public Pool - Left Flowerbed":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Public Pool - Middle Flowerbed":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Public Pool - Right Flowerbed":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Bathhouse - Flowerbed By Gabi":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Bathhouse - Flowerbed By Axolotl Family":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Bathhouse - Flowerbed Above Axolotl Family":
            lambda state: state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2),
        "Hairball City - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Hairball City Flower", player, 3))
                          and has_textbox(state, player, world, "Hairball City"),
        "Turbine Town - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Turbine Town Flower", player, 3))
                          and has_textbox(state, player, world, "Turbine Town"),
        "Salmon Creek Forest - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Salmon Creek Forest Flower", player, 6))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Tadpole HQ - Little Gabi's Flowers":
            lambda state: (options.flowersanity.value != 2 or state.has("Tadpole HQ Flower", player, 4))
                          and has_textbox(state, player, world, "Tadpole HQ"),
        # Progressive Cassette Logic
        "Mitch/Mai - 1":
            lambda state: (has_enough_cassettes(state, player, 1)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 2":
            lambda state: (has_enough_cassettes(state, player, 2)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 3":
            lambda state: (has_enough_cassettes(state, player, 3)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 4":
            lambda state: (has_enough_cassettes(state, player, 4)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 5":
            lambda state: (has_enough_cassettes(state, player, 5)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 6":
            lambda state: (has_enough_cassettes(state, player, 6)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 7":
            lambda state: (has_enough_cassettes(state, player, 7)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 8":
            lambda state: (has_enough_cassettes(state, player, 8)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 9":
            lambda state: (has_enough_cassettes(state, player, 9)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 10":
            lambda state: (has_enough_cassettes(state, player, 10)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 11":
            lambda state: (has_enough_cassettes(state, player, 11)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 12":
            lambda state: (has_enough_cassettes(state, player, 12)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 13":
            lambda state: (has_enough_cassettes(state, player, 13)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),
        "Mitch/Mai - 14":
            lambda state: (has_enough_cassettes(state, player, 14)
                          and ((state.has("Hairball City Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Hairball City Textbox", player))
                          or (state.has("Turbine Town Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and options.textbox.value != 2 or state.has("Turbine Town Textbox", player))
                          or (state.has("Salmon Creek Forest Ticket", player)
                               and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1))
                               and (state.has("Key", player, 7) or state.has("Salmon Creek Forest Key", player))
                               and options.textbox.value != 2 or state.has("Salmon Creek Forest Textbox", player))
                          or (state.has("Public Pool Ticket", player)
                               and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                               and options.textbox.value != 2 or state.has("Public Pool Textbox", player))
                          or (state.has("Bathhouse Ticket", player)
                               and options.textbox.value != 2 or state.has("Bathhouse Textbox", player))
                          or (state.has("Tadpole HQ Ticket", player)
                               and options.textbox.value != 2 or state.has("Tadpole HQ Textbox", player))
                          or (state.has("Gary's Garden Ticket", player))
                               and options.textbox.value != 2 or state.has("Gary's Garden Textbox", player)))
                          and (options.textbox.value != 1 or state.has("Textbox", player)),

        "Hairball City - Apple On Frog Statue Island Pier 1":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 2":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 3":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 4":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Apple On Frog Statue Island Pier 5":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug On Frog Statue Island 1":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug On Frog Statue Island 2":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug On Frog Statue Island 4":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug On Frog Statue Island 5":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bug On Frog Statue Island 3":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),

        "Salmon Creek Forest - Blippy Dog":
            lambda state: (options.bonesanity.value != 2 or state.has("Salmon Creek Forest Bone", player, 5))
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Blippy Dog":
            lambda state: (options.bonesanity.value != 2 or state.has("Public Pool Bone", player, 5))
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Tadpole HQ - Blippy Dog":
            lambda state: (options.bonesanity.value != 2 or state.has("Tadpole HQ Bone", player, 5))
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Tadpole HQ - Blessley":
            lambda state: (has_textbox(state, player, world, "Tadpole HQ")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Hairball City - Blessley":
            lambda state: (has_textbox(state, player, world, "Hairball City")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Turbine Town - Blessley":
            lambda state: (has_textbox(state, player, world, "Turbine Town")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Salmon Creek Forest - Blessley":
            lambda state: (has_textbox(state, player, world, "Salmon Creek Forest")
                          and (options.bug_catching.value != 1 or state.has("Bug Net", player))),
        "Turbine Town - Shipping Container With Breakable Boxes":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Bathhouse - Breakable Box Inside Bathhouse Box":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Hairball City - Breakable Boxes Near Frog Of Destruction":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Salmon Creek Forest - Inside Boxes (Waterfall Cave)":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Breakable Boxes Near Frogtective":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Above Small Island":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player))
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Tadpole HQ - Breakable Boxes near Blessley":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),

        "Hairball City - Big Umbrella":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Stone Pillar Behind Wind Turbine":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Bug On Stone Pillar Behind Wind Turbine 1":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Turbine Town - Bug On Stone Pillar Behind Wind Turbine 2":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 3":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 4":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 5":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Third Rock Cluster Near Building Submerged In Ocean 6":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),

        "Public Pool - Far Away Island":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Far Away Island Left Side":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Public Pool - Far Away Island Right Side":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Niko & 2D (Thought)":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 1":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 2":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 3":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 4":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 5":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 6":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 7":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 8":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 9":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 10":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 11":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 12":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 13":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 14":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 15":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 16":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 17":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 18":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 19":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 20":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 21":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 22":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 23":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Public Pool - Apple On Far Away Island 24":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Tadpole HQ - Big Tree Next To Louist":
            lambda state: (options.soda_cans.value != 1 or state.has("Soda Repair", player)),

        "Turbine Town - Near Fishing Containers":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Niko is a ninja (Thought)":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Fan to Fan":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 8":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 1":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 7":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 6":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 5":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 4":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 3":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Apple Near Dustan 2":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Seed On Lamp Near Office":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Seed In Office":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Bathhouse - Seed By Serschel & Louist":
            lambda state: (options.ac_repair.value != 1 or state.has("AC Repair", player)),

        "Achievement - Lost at Sea":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Behind The Train":
            lambda state: (options.swimming.value != 1
                          or options.precisejumps.value == 1
                          or state.has("Swim Course", player)),
        "Home - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Frog Statue Crown":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Moorish Idol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Not Nemo":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Eel":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Flying Fish":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Orange Fish":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Bone In Bush Ring":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Bone In Breakable Boxes On Left Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Bone On Back Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Bone On Right Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Bone Between Middle Buildings":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Bone Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Kappa (Chatsanity)":
            lambda state: (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Dog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Dog 2 (Chatsanity)":
            lambda state: (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Niko admires a Frog Statue (Thought)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Nervous Frog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Hairball City - Next to Breakable Boxes Under Ramp":
            lambda state: (options.swimming.value != 1
                          or options.precisejumps.value == 1
                          or state.has("Swim Course", player)),

        "Turbine Town - Albino Corydoras":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Axolotl":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Prianha":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Mantaray":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Sand Shrimp":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Turbine Town - Bone Above Big Parasol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and(state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Bone On Edge Of Pig Parasol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and(state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Bone Under Big Parasol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and(state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Bone Above Back Parasol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and(state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Bone Above Right Parasol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and(state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Bone Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 1", player) or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Dog 2 (Chatsanity)":
            lambda state: (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)),
        "Turbine Town - Kappa (Chatsanity)":
            lambda state: (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Turbine Town - Dog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2))
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Turbine Town - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),

        "Salmon Creek Forest - Beneath Pond":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone On Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone Above Parasol":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player)),
        "Salmon Creek Forest - Bone On Left Of Bone Dog":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone On Right Of Bone Dog":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone On Back Of Rock":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Woodisch (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Divin' Doe (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Niko & a rock (Thought)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 1":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 2":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Apple On Second Rock Cluster Near Building Submerged In Ocean 3":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug On Second Rock Cluster Near Submerged Building In Ocean":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug On Fourth Rock Cluster Near Submerged Building In Ocean":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug Around Lower Pond 6":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug Below Treehouse In Bushes 2":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bug On Third Rock Cluster Near Submerged Building In Ocean":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Salmon Creek Forest - Bone Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),

        "Public Pool - Inside BIG Pool":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Inside Pool":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Bone In Breakable Boxes 1":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone In Breakable Boxes 2":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone In Breakable Boxes 3":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone In Breakable Boxes 4":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Bone In Breakable Boxes 5":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Public Pool - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Shark":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Squid":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Turtle":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Gramma Loreto":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Baby Crocodile":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Bone Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Public Pool - Britney (Chatsanity)":
            lambda state: (options.swimming.value != 1
                          or options.precisejumps.value == 1
                          or state.has("Swim Course", player)),
        "Public Pool - Niko, Pink Frog & King Frog (Thought)":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),

        "Bathhouse - Bone Above Middle Bathhouse":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone In Middle Bathhouse":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone Above Right Bathhouse":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone In Water In Left Bathhouse":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Bone On Right Bathhouse":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Bone Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (state.has("Contact List 2", player) or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Hut in Water":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),

        "Tadpole HQ - Bone On Wood Board On Side Of Right Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bone Above Right Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bone On Small Building Behind Big Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bone In Breakable Boxes On Middle Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Tadpole HQ - Bone On Net Near Left Building":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Blue Fairy Shrimp":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Bluestreak Cleaner Wrasse":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Honey Gourami":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Loach":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Neon Tetra":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Hasselhop (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Blippy (Chatsanity)":
            lambda state: (state.has("Key", player, 7) or state.has("Tadpole HQ Key", player)),
        "Tadpole HQ - Bone Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Tadpole HQ - Dog (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player))
                          and (state.has("Key", player, 7) or state.has("Tadpole HQ Key", player)),

        "Home - Give High Frog Lunchbox":
            lambda state: has_textbox(state, player, world, "Home"),
        "Hairball City - BIG VOLLEY":
            lambda state: has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Dustan on Lighthouse":
            lambda state: (has_textbox(state, player, world, "Hairball City")
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))),
        "Hairball City - Gunter on Skyscraper":
            lambda state: has_textbox(state, player, world, "Hairball City"),
        "Hairball City - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Hairball City"),

        "Turbine Town - AIR VOLLEY":
            lambda state: has_textbox(state, player, world, "Turbine Town"),
        "Turbine Town - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Turbine Town"),
        "Turbine Town - Pelly the Engineer":
            lambda state: has_textbox(state, player, world, "Turbine Town"),

        "Salmon Creek Forest - Dustan on Mountain":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Nina":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Stijn & Melissa":
            lambda state: has_textbox(state, player, world, "Salmon Creek Forest"),
        "Salmon Creek Forest - Treeman":
            lambda state: (has_textbox(state, player, world, "Salmon Creek Forest")
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player))),

        "Public Pool - Frogtective":
            lambda state: has_textbox(state, player, world, "Public Pool"),
        "Public Pool - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Public Pool"),

        "Bathhouse - Dustan on Bathhouse":
            lambda state: (has_textbox(state, player, world, "Bathhouse")
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player))),
        "Bathhouse - Game Kid":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Handsome Frog":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - LONG VOLLEY":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Nina":
            lambda state: has_textbox(state, player, world, "Bathhouse"),
        "Bathhouse - Serschel & Louist":
            lambda state: has_textbox(state, player, world, "Bathhouse"),

        "Tadpole HQ - Dojo Guy":
            lambda state: (has_textbox(state, player, world, "Tadpole HQ")
                          and (options.applebasket.value != 1 or state.has("Apple Basket", player))),
        "Tadpole HQ - Serschel & Louist":
            lambda state: (has_textbox(state, player, world, "Tadpole HQ")
                          and (options.parasols.value != 1 or state.has("Parasol Repair", player))),
        "Tadpole HQ - Frog King":
            lambda state: has_textbox(state, player, world, "Tadpole HQ"),
        "Tadpole HQ - HUGE VOLLEY":
            lambda state: has_textbox(state, player, world, "Tadpole HQ"),

        "Hairball City - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Blippy Dog (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Game Kid (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Hairball City - Louist (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Serschel & Louist"),
        "Hairball City - Serschel (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Serschel & Louist"),
        "Hairball City - Nina (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Melissa (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Hairball City - Nina"),
        "Hairball City - Mitch (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Mai (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Moomy (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1)),
        "Hairball City - Dustan (Chatsanity)":
            lambda state: (options.parasols.value != 1 or state.has("Parasol Repair", player)),

        "Turbine Town - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Turbine Town - Blippy Dog (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Serschel (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Serschel & Louist"),
        "Turbine Town - Louist (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Serschel & Louist"),
        "Turbine Town - Mitch (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Mai (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Turbine Town - Dustan (Chatsanity)":
            lambda state: has_access_to(state, player, "Turbine Town - Dustan on Wind Turbine"),
        "Turbine Town - Melissa & Stijn (Chatsanity)":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa"),

        "Salmon Creek Forest - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Fischer (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Salmon Creek Forest - Mai (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                           or state.has("Progressive Contact List", player, 1))
                          and (state.has("Key", player, 7)
                           or state.has("Salmon Creek Forest Key", player)),
        "Salmon Creek Forest - Serschel (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Louist (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                          or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Trixie (Chatsanity)":
            lambda state: (state.has("Contact List 1", player)
                          or state.has("Progressive Contact List", player, 1)),
        "Salmon Creek Forest - Game Kid (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Salmon Creek Forest - Clint (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Clover (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Coco (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Culley (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - David D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Flippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Jippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Marry D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Salmon Creek Forest - Mippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Paul (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Poppy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Tippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Skippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Salmon Creek Forest - Pine Frog (Chatsanity)":
            lambda state: (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),

        "Public Pool - Blessley (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Mitch (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (state.has("Key", player, 7)
                           or state.has("Public Pool Key", player)),
        "Public Pool - Little Gabi (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Trixie (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Vlog Frog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Public Pool - Poppy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Paul (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Flippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Jippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Mippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Skippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Public Pool - Tippy (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),

        "Bathhouse - Blessley (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Vlog Frog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Fischer (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Little Gabi (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Blippy (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Blippy Dog (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2)),
        "Bathhouse - Gashadokuro (Chatsanity)":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Bathhouse - Mahjong Frogs (Chatsanity)":
            lambda state: (state.has("Contact List 2", player)
                           or state.has("Progressive Contact List", player, 2))
                          and (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Penny (Chatsanity)":
            lambda state: (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Poppy (Chatsanity)":
            lambda state: (state.has("Key", player, 7)
                           or state.has("Bathhouse Key", player, 2)),
        "Bathhouse - Clint (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Coco (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Culley (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Clover (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Marry D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - David D. Carota (Chatsanity)":
            lambda state: has_access_to(state, player, "Public Pool - Frogtective"),
        "Bathhouse - Dustan (Chatsanity)":
            lambda state: has_access_to(state, player, "Bathhouse - Dustan on Bathhouse"),

        # Chatsanity Global
        "Chatsanity - (Ex) Employee of the month":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - AC Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Accountant Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Alice":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Assistant Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Baby Gull (PP)":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Baby Gull (TT)":
            lambda state: (state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town")),
        "Chatsanity - Big Bro Stag":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Biki":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Bird":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 4),
        "Chatsanity - Blessley":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Blippy":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and (state.has("Key", player,7)
                                   or state.has("Tadpole HQ Key", player))
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Blippy Dog":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Bobby":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Borbie":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Britney":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (options.swimming.value != 1
                                   or options.precisejumps.value == 1
                                   or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Public Pool Ticket", player)
                              and (options.swimming.value != 1
                                   or options.precisejumps.value == 1
                                   or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Public Pool")),
        "Chatsanity - Brooklyn Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Button Bird":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Carl":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Carrot":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Clint":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool")
                          and (options.swimming.value != 1 or state.has("Swim Course", player)),
        "Chatsanity - Clover":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Coco":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Code Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Coffee Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Conspiracy Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 2),
        "Chatsanity - Culley":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Culture Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Dance Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 8),
        "Chatsanity - Danger Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 5),
        "Chatsanity - David D. Carota":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Dirk":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Divin' Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Doe of Darkness":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Dream Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 3)
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Chatsanity - Dustan":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or has_access_to(state, player, "Dustan - Meeting First Time"),
        "Chatsanity - Elizabeth IV":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Fear Deer":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Fear Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 7),
        "Chatsanity - Fischer":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Fix Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Fizzy the Frog":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Flippy":
            lambda state: ((state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                           or (state.has("Salmon Creek Forest Ticket", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Flower Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 1),
        "Chatsanity - Flowery Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Friendly Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Frog (Frogbucks)":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Frog King":
            lambda state: (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Frog of Destruction":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Frogtective":
            lambda state: (state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Frogucus the Green":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Fry Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Fry loving Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Game Kid":
            lambda state: (state.has("Hairball City Ticket", player)
                           and (state.has("Contact List 2", player)
                                or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Gamedev Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Gary":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Gashadokuro":
            lambda state: state.has("Bathhouse Ticket", player)
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Gull Friend":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Gull Friend 2":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Gunter":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or has_access_garden(state, player, world),
        "Chatsanity - HUD Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Handsome Frog":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (has_access_garden(state, player, world)
                              and has_enough_seeds(state, player, world, 2)),
        "Chatsanity - Hasselhop":
            lambda state: (options.swimming.value != 1 or state.has("Swim Course", player))
                          or (has_access_garden(state, player, world)
                              and has_enough_seeds(state, player, world, 10)),
        "Chatsanity - Hat Kid":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Hungry Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 9)
                          and (options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Chatsanity - Impatient Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Jess":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Jiji":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Jippy":
            lambda state: ((state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                           or (state.has("Salmon Creek Forest Ticket", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Knowledgeable Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Lil' Sis Doe":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Little Gabi":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Lock Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Loud Stag":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Louist":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Maggie":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mahjong Frog":
            lambda state: (state.has("Bathhouse Ticket", player)
                           and (state.has("Key", player, 7)
                                or state.has("Bathhouse Key", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mai":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and state.has("Key", player, 7)
                                   or state.has("Salmon Creek Forest Key", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Marry D. Carota":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Master":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Melissa":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa")
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or has_access_to(state, player, "Hairball City - Nina")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mickey":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Miki":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Minoes":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mippy":
            lambda state: ((state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"))
                           or (state.has("Salmon Creek Forest Ticket", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Mitch":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Moe":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Mom Gull (PP)":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Mom Gull (TT)":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Monty":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Moomy":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Mysterious Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Mythology Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Nervous Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Niko a0.45":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Nina":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Noah":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Paul":
            lambda state: (state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Pelly the Engineer":
            lambda state: (state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Penny":
            lambda state: has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Pine Frog":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest")
                          and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player)),
        "Chatsanity - Poppy":
            lambda state: (state.has("Party Invitation", player)
                          and has_textbox(state, player, world, "Home"))
                          or has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - R&D Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - R&D Frog 2":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - R&D Frog 3":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Ricky":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Robo Fr0g":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Salty Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Scare Frog":
            lambda state: (state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest")),
        "Chatsanity - Serschel":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Shovelin' Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Simon":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Skippy":
            lambda state: ((state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                           or (state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool")))
                          and has_access_to(state, player, "Bathhouse - Poppy"),
        "Chatsanity - Slack Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Small Talk Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Snip Frog":
            lambda state: has_access_garden(state, player, world),
        "Chatsanity - Snow Frog Frog":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Steamy Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Steamy Frog":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Stijn":
            lambda state: has_access_to(state, player, "Salmon Creek Forest - Stijn & Melissa")
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or has_access_to(state, player, "Hairball City - Nina")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Stijn's Dad":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Stijn's Mom":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Superstitious Gull":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Sushi Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Swimming Doe":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Tax Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Tip Frog":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Tippy":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Tough Frog":
            lambda state: state.has("Hairball City Ticket", player)
                          and has_textbox(state, player, world, "Hairball City"),
        "Chatsanity - Tourist Frog":
            lambda state: has_access_garden(state, player, world)
                          and has_enough_seeds(state, player, world, 6),
        "Chatsanity - Train Frog":
            lambda state: state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City")
                          or state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town")
                          or state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest")
                          or state.has("Public Pool Ticket", player)
                              and has_textbox(state, player, world, "Public Pool")
                          or state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse")
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Travis":
            lambda state: (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Bathhouse Ticket", player)
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ"))
                          or (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home")),
        "Chatsanity - Treeman":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Turbine Stag":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Chatsanity - Trixie":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Public Pool")),
        "Chatsanity - VR Frog":
            lambda state: state.has("Tadpole HQ Ticket", player)
                          and has_textbox(state, player, world, "Tadpole HQ"),
        "Chatsanity - Vlog Frog":
            lambda state: (state.has("Party Invitation", player)
                              and has_textbox(state, player, world, "Home"))
                          or (state.has("Hairball City Ticket", player)
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Vacation Frog":
            lambda state: state.has("Public Pool Ticket", player)
                          and has_textbox(state, player, world, "Public Pool"),
        "Chatsanity - Wess":
            lambda state: state.has("Bathhouse Ticket", player)
                          and has_textbox(state, player, world, "Bathhouse"),
        "Chatsanity - Wind Dragon":
            lambda state: state.has("Turbine Town Ticket", player)
                          and has_textbox(state, player, world, "Turbine Town"),
        "Chatsanity - Woodisch":
            lambda state: state.has("Salmon Creek Forest Ticket", player)
                          and (options.swimming.value != 1 or state.has("Swim Course", player))
                          and has_textbox(state, player, world, "Salmon Creek Forest"),
        "Turbine Town - Inside Partially Sunken Shipping Container":
            lambda state: (options.swimming.value != 1
                          or options.precisejumps.value == 1
                          or state.has("Swim Course", player)),
        "Turbine Town - Above Partially Sunken Shipping Container":
            lambda state: (options.swimming.value != 1
                          or options.precisejumps.value == 1
                          or state.has("Swim Course", player)),
        "Turbine Town - Bug By Sunken Container 4":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug By Sunken Container 2":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug By Sunken Container 3":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug By Sunken Container 1":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug By Sunken Container 5":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        "Turbine Town - Bug On Top Of Wind Turbine":
            lambda state: state.has("Key", player, 7)
                          or state.has("Turbine Town Key", player),
        "Tadpole HQ - Borbie (Chatsanity)":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Tadpole HQ - Pepper (Chatsanity)":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Chatsanity - Bone Dog":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 1", player)
                                   or state.has("Progressive Contact List", player, 1))
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Salmon Creek Forest Ticket", player)
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Salmon Creek Forest"))
                          or (state.has("Public Pool Ticket", player)
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Public Pool"))
                          or (state.has("Bathhouse Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Bathhouse"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Kappa":
            lambda state:(state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Turbine Town")),
        "Chatsanity - Dog":
            lambda state: (state.has("Hairball City Ticket", player)
                              and (state.has("Contact List 2", player)
                                or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and (options.ac_repair.value != 1 or state.has("AC Repair", player))
                              and has_textbox(state, player, world, "Turbine Town"))
                          or (state.has("Tadpole HQ Ticket", player)
                              and (options.swimming.value != 1 or state.has("Swim Course", player))
                              and (options.bonk_permit.value != 1 or state.has("Safety Helmet", player))
                              and (state.has("Key", player, 7) or state.has("Tadpole HQ Key", player))
                              and has_textbox(state, player, world, "Tadpole HQ")),
        "Chatsanity - Dog 2":
            lambda state: (state.has("Hairball City Ticket", player)
                           and (state.has("Contact List 2", player)
                                or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Hairball City"))
                          or (state.has("Turbine Town Ticket", player)
                              and (state.has("Contact List 2", player)
                                   or state.has("Progressive Contact List", player, 2))
                              and has_textbox(state, player, world, "Turbine Town")),
        "Tadpole HQ - Niko has nightmares (Thought)":
            lambda state: has_enough_coins(state, player, world.kiosk_cost["Elevator"]),
        "Tadpole HQ - Inbetween Four Skyscrapers":
            lambda state: (options.swimming.value != 1
                           or options.precisejumps.value == 1
                           or state.has("Swim Course", player)),
        # Gary's Garden Seeds
        "Gary's Garden - Seed 2":
            lambda state: state.has("Gary's Garden Seed", player, 1),
        "Gary's Garden - Seed 3":
            lambda state: state.has("Gary's Garden Seed", player, 2),
        "Gary's Garden - Seed 4":
            lambda state: state.has("Gary's Garden Seed", player, 3)
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Gary's Garden - Seed 5":
            lambda state: state.has("Gary's Garden Seed", player, 4),
        "Gary's Garden - Seed 6":
            lambda state: state.has("Gary's Garden Seed", player, 5),
        "Gary's Garden - Seed 7":
            lambda state: state.has("Gary's Garden Seed", player, 6),
        "Gary's Garden - Seed 8":
            lambda state: state.has("Gary's Garden Seed", player, 7),
        "Gary's Garden - Seed 9":
            lambda state: state.has("Gary's Garden Seed", player, 8),
        "Gary's Garden - Seed 10":
            lambda state: state.has("Gary's Garden Seed", player, 9)
                          and (options.soda_cans.value != 1 or state.has("Soda Repair", player)),

        "Gary's Garden - Flower Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 1),
        "Gary's Garden - Small Rocks In Water":
            lambda state: has_enough_seeds(state, player, world, 1),
        "Gary's Garden - Handsome Frog":
            lambda state: has_enough_seeds(state, player, world, 2),
        "Gary's Garden - Handsome Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 2),
        "Gary's Garden - Conspiracy Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 2),
        "Gary's Garden - Dream Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 3)
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Gary's Garden - Behind Large Rock":
            lambda state: has_enough_seeds(state, player, world, 3)
                          and (options.ac_repair.value != 1 or state.has("AC Repair", player)),
        "Gary's Garden - Bird (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 4),
        "Gary's Garden - On Tree Branch":
            lambda state: has_enough_seeds(state, player, world, 4),
        "Gary's Garden - Danger Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 5),
        "Gary's Garden - Next To Smaller Tree":
            lambda state: has_enough_seeds(state, player, world, 5),
        "Gary's Garden - Tourist Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 6),
        "Gary's Garden - Next Garden Seed On Rocks":
            lambda state: has_enough_seeds(state, player, world, 6),
        "Gary's Garden - Fear Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 7),
        "Gary's Garden - Beginning Of Giant Gold Scissor":
            lambda state: has_enough_seeds(state, player, world, 7),
        "Gary's Garden - Near End Of Giant Gold Scissor":
            lambda state: has_enough_seeds(state, player, world, 7),
        "Gary's Garden - Dance Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 8),
        "Gary's Garden - Tree Branch Near Gold Scissor Row":
            lambda state: has_enough_seeds(state, player, world, 8),
        "Gary's Garden - Hungry Frog (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 9)
                          and (options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Gary's Garden - Tree Branch Near The Top":
            lambda state: has_enough_seeds(state, player, world, 9)
                          and (options.soda_cans.value != 1 or state.has("Soda Repair", player)),
        "Gary's Garden - Gunter (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 10),
        "Gary's Garden - Hasselhop (Chatsanity)":
            lambda state: has_enough_seeds(state, player, world, 10),
    }

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
    else:
        company_building.connect(victory, rule=lambda state: (state.has_all(world.slot_item_data.shop_items, player)
                                                              and state.has_all(world.slot_item_data.moons, player)))

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
    company_building.connect(quotas, rule=lambda state: ((state.has("Inventory Slot", player, 2 - options.starting_inventory_slots.value)
                                                          or options.starting_inventory_slots.value >= 2)
                                                         and (state.has("Stamina Bar", player)
                                                              or options.starting_stamina_bars.value > 0)))

    bestiary_moons = generate_bestiary_moons(world, options.min_monster_chance.value/100.0)
    scrap_moons = generate_scrap_moons(world, options.min_scrap_chance.value/100.0) if options.modify_scrap_spawns.value == 0 \
        else generate_scrap_moons_alt(world)

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
                                                                      ((state.has("Stamina Bar", player)
                                                                        or options.starting_stamina_bars.value > 0)
                                                                        and ((check_item_accessible(state, "Shovel",
                                                                                                  player, options)
                                                                                and (state.has("Stamina Bar", player, 3 - options.starting_stamina_bars.value)    # we eventually need to put 4 stamina and 4 slots in the item pool and grant them as starting items so we don't have to do this jank
                                                                                    or options.starting_stamina_bars.value >= 3
                                                                                    or (s_name != "Sapsucker Egg")))
                                                                            or (s_name != "Shotgun"
                                                                                and s_name != "Kitchen knife"
                                                                                and s_name != "Sapsucker Egg"))))
                elif moon != "excluded":
                    multiworld.get_region(moon, player).connect(multiworld.get_region(scrap_name, player),
                                                                rule=lambda state, s_name=scrap_name:
                                                                ((state.has("Stamina Bar", player)
                                                                    or options.starting_stamina_bars.value > 0)
                                                                    and ((check_item_accessible(state, "Shovel",
                                                                                                player, options)
                                                                            and (state.has("Stamina Bar", player, 3 - options.starting_stamina_bars.value)
                                                                                or options.starting_stamina_bars.value >= 3
                                                                                or (s_name != "Sapsucker Egg")))
                                                                        or (s_name != "Shotgun"
                                                                            and s_name != "Kitchen knife"
                                                                            and s_name != "Sapsucker Egg"))))

    logs.append(Region("Behind the Wall", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("61 March", player).connect(logs[0])
    logs.append(Region("Mummy", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("220 Assurance", player).connect(logs[1])
    logs.append(Region("Swing of Things", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("41 Experimentation", player).connect(logs[2])
    logs.append(Region("Autopilot", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("41 Experimentation", player).connect(logs[3],
                                                             rule=lambda state: (state.has("Stamina Bar", player)
                                                                                 or options.starting_stamina_bars > 0))
    logs.append(Region("Golden Planet", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("85 Rend", player).connect(logs[4])
    logs.append(Region("Goodbye", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("21 Offense", player).connect(logs[5])
    logs.append(Region("Screams", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("220 Assurance", player).connect(logs[6],
                                                             rule=lambda state: (state.has("Stamina Bar", player)
                                                                                 or options.starting_stamina_bars > 0))
    logs.append(Region("Idea", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("20 Adamance", player).connect(logs[7])
    logs.append(Region("Nonsense", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("85 Rend", player).connect(logs[8])
    logs.append(Region("Hiding", player, multiworld))
    multiworld.regions.append(logs[-1])
    company_building.connect(logs[9])
    logs.append(Region("Real Job", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("56 Vow", player).connect(logs[10])
    logs.append(Region("Desmond", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("7 Dine", player).connect(logs[11],
                                                   rule=lambda state:
                                                   (state.has("Stamina Bar", player)
                                                        or options.starting_stamina_bars > 0))
    logs.append(Region("Team Synergy", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("20 Adamance", player).connect(logs[12])
    logs.append(Region("Letter of Resignation", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("8 Titan", player).connect(logs[13],
                                                   rule=lambda state:
                                                   (state.has("Stamina Bar", player)
                                                        or options.starting_stamina_bars > 0))
    logs.append(Region("Work", player, multiworld))
    multiworld.regions.append(logs[-1])
    multiworld.get_region("68 Artifice", player).connect(logs[14])

    # Generate locations
    for i in range(options.checks_per_moon.value):
        for moon in world.slot_item_data.moons:
            add_location(player, f"{moon} check {i+1}", multiworld.get_region(moon, player))

    for i in range(options.num_quotas.value):
        add_location(player, f"Quota check {i+1}", quotas)

    for log in world.log_names:
        add_location(player, f"Log - {log}", multiworld.get_region(log, player))

    for monster in world.bestiary_names:
        if len(bestiary_moons[monster]) < 1:
            import logging
            logging.warning(f"Cannot find any moon that spawns Monster - {monster} for player {world.player_name}. This monster may not be scannable.")
        #else:
        add_location(player, f"Bestiary Entry - {monster}", multiworld.get_region(monster, player))
        if len(bestiary_moons[monster]) < 1 or (len(bestiary_moons[monster]) <= 2 and bestiary_moons[monster][-1] == 'excluded'):
            multiworld.get_location(f"Bestiary Entry - {monster}", player).item_rule = lambda item: not \
                    (item.classification == ItemClassification.progression or
                     item.classification == ItemClassification.useful)

    if options.scrapsanity.value == 1:
        for scrap_name in world.scrap_names:
            if len(scrap_moons[scrap_name]) < 1:
                import logging
                logging.warning(f"Cannot find any moon that spawns Scrap - {scrap_name} for player {world.player_name}. This scrap may not be obtainable.")
            #else:
            add_location(player, f"Scrap - {scrap_name}", multiworld.get_region(scrap_name, player))

            if len(scrap_moons[scrap_name]) < 1 or (len(scrap_moons[scrap_name]) <= 2 and scrap_moons[scrap_name][-1] == 'excluded'):
                multiworld.get_location(f"Scrap - {scrap_name}", player).item_rule = lambda item: not \
                    (item.classification == ItemClassification.progression or
                     item.classification == ItemClassification.useful)


def add_location(player: int, location: str, region: Region):
    region.locations.append(Location(player, location, locations[location]))
    region.locations[-1].parent_region = region

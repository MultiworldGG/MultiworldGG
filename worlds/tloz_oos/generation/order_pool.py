from typing import cast

from BaseClasses import Item, MultiWorld

from ..data.Constants import SEASON_WINTER
from ..options import OracleOfSeasonsStartingPosition
from ..world import OracleOfSeasonsWorld


def order_pool(multiworld: MultiWorld, progitempool: list[Item]):
    players = multiworld.get_game_players(OracleOfSeasonsWorld.game)
    if not players:
        return
    weight_dict = {}
    for player in players:
        world: OracleOfSeasonsWorld = cast(OracleOfSeasonsWorld, multiworld.worlds[player])
        bush_breakers = [["Progressive Sword"], ["Biggoron's Sword"]]

        if multiworld.random.random() < 0.5:
            bush_breakers.append(["Progressive Boomerang", "Progressive Boomerang"])
        if world.options.animal_companion == "ricky":
            bush_breakers.append(["Ricky's Flute"])
        else:
            bush_breakers.append(["Moosh's Flute"])

        if world.options.logic_difficulty > 0:
            if multiworld.random.random() < 0.5:
                bush_breakers.append(["Bomb Upgrade"])
            if world.options.default_seed == "gale":
                bush_breakers.append(["Progressive Slingshot"])
                if world.options.cross_items:
                    bush_breakers.append(["Seed Shooter"])

        if world.options.cross_items:
            bush_breakers.append(["Switch Hook"])

        bad_portals = {"spool swamp portal", "horon village portal", "eyeglass lake portal", "temple remains lower portal", "d8 entrance portal"}

        if world.options.start_position == OracleOfSeasonsStartingPosition.option_horon_village:
            possible_items = [["Flippers", "Bush Breaker"], ["Power Bracelet"]]
            portal_connections = {world.portal_connections[key]: key for key in world.portal_connections}
            portal_connections.update(world.portal_connections)

            if portal_connections["temple remains lower portal"] in bad_portals:
                bad_portals.add("temple remains upper portal")

            if portal_connections["horon village portal"] not in bad_portals:
                possible_items.append(["Progressive Boomerang", "Progressive Boomerang"])

            if portal_connections["eyeglass lake portal"] not in bad_portals and world.options.default_seed == "pegasus":
                items = ["Progressive Feather", "Progressive Feather", "Seed Satchel", "Bush Breaker"]
                if world.default_seasons["EYEGLASS_LAKE"] != SEASON_WINTER:
                    items.append("Rod of Seasons (Winter)")
                possible_items.append(items)

            if world.options.default_seed == "ember":
                possible_items.append(["Seed Satchel"])
                possible_items.append(["Progressive Slingshot"])
                if world.options.cross_items:
                    possible_items.append(["Seed Shooter"])

            if world.options.animal_companion == "dimitri":
                possible_items.append(["Dimitri's Flute"])

            if not world.options.remove_d0_alt_entrance:
                if world.dungeon_entrances["d2 entrance"] == "enter d0" \
                        or world.dungeon_entrances["d5 entrance"] == "enter d0" \
                        or world.dungeon_entrances["d7 entrance"] == "enter d0" \
                        or (world.dungeon_entrances["d8 entrance"] == "enter d0"
                            and portal_connections["d8 entrance portal"] not in bad_portals):
                    possible_items.append(["Bush Breaker"])
        elif world.options.start_position == OracleOfSeasonsStartingPosition.option_sunken_city:
            possible_items = [["Flippers"], ["Progressive Feather"], ["Bomb Upgrade"]]

            if world.options.animal_companion == "dimitri":
                possible_items.append(["Dimitri's Flute"])
        elif (world.options.start_position == OracleOfSeasonsStartingPosition.option_temple_of_seasons
              or world.options.start_position == OracleOfSeasonsStartingPosition.option_samasa_desert):
            possible_items = [["Bush Breaker"]]
        elif world.options.start_position == OracleOfSeasonsStartingPosition.option_tarm_entrance:
            possible_items = [[]] # That one is pretty restrictive but has 2 starting items
        else:
            raise NotImplementedError

        items = multiworld.random.choice(possible_items)
        if "Bush Breaker" in items:
            items.remove("Bush Breaker")
            items.extend(multiworld.random.choice(bush_breakers))
        for item in multiworld.precollected_items[player]:
            if item.name in items:
                items.remove(item.name)
        weight_dict[player] = items

    indexes = {player: [] for player in players}
    for i in range(len(progitempool)):
        item = progitempool[i]
        player = item.player
        if player not in players:
            continue

        if len(indexes[player]) < len(weight_dict[player]):
            indexes[player].append(i)
        if item.name not in weight_dict[player]:
            continue
        other_index = indexes[player].pop()
        progitempool[i], progitempool[other_index] = progitempool[other_index], progitempool[i]
        weight_dict[player].remove(item.name)
        for player in players:
            if len(weight_dict[player]) > 0:
                break
        else:
            break

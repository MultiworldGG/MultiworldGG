import itertools
from typing import TYPE_CHECKING

from BaseClasses import Region, CollectionRule, Entrance
from entrance_rando import EntranceType, randomize_entrances
from .connections import RANDOMIZED_CONNECTIONS, TRANSITIONS
from .options import ShuffleTransitions, TransitionPlando

if TYPE_CHECKING:
    from . import MessengerWorld


def disconnect_entrances(world: "MessengerWorld") -> None:
    for region_exit, vanilla_connected_region in RANDOMIZED_CONNECTIONS.items():
        entrance = world.get_entrance(region_exit)
        entrance.randomization_type = EntranceType.ONE_WAY if region_exit in ONE_WAY_EXITS else EntranceType.TWO_WAY
        disconnect_entrance_for_randomization(entrance, one_way_target_name=vanilla_connected_region)


def connect_plando(world: "MessengerWorld", plando_connections: TransitionPlando, keep_logic: bool = False) -> list[Entrance]:
    def remove_dangling_exit(region: Region) -> CollectionRule:
        # find the disconnected exit and remove references to it
        for _exit in region.exits:
            if not _exit.connected_region:
                break
        else:
            raise ValueError(f"Unable to find randomized transition for {plando_connection}")
        return _exit

    def remove_dangling_entrance(region: Region) -> None:
        """Find the disconnected entrance and remove references to it."""
        for _entrance in region.entrances:
            if not _entrance.parent_region:
                break
        else:
            raise ValueError(f"Invalid target region for {plando_connection}")
        region.entrances.remove(_entrance)

    plando_entrances = []
    for plando_connection in plando_connections:
        plando_entrance = world.get_entrance(plando_connection.entrance)
        destination = world.get_region(plando_connection.exit)

        reg2 = world.get_region(plando_connection.exit)
        remove_dangling_entrance(reg2)
        # connect the regions
        new_exit1 = reg1.connect(reg2)
        if keep_logic:
            new_exit1.access_rule = access_rule
        if plando_connection.entrance == "Artificer":
            new_exit1.name = "Artificer's Portal"
        elif plando_connection.entrance == "Tower HQ":
            new_exit1.name = "Artificer's Challenge"

        plando_entrances.append(new_exit1)

        # pretend the user set the plando direction as "both" regardless of what they actually put on coupled
        if ((world.options.shuffle_transitions == ShuffleTransitions.option_coupled
             or plando_connection.direction == "both")
                and plando_connection.exit in RANDOMIZED_CONNECTIONS
                and plando_connection.exit != "Glacial Peak - Left"):
            access_rule = remove_dangling_exit(reg2)
            remove_dangling_entrance(reg1)
            new_exit2 = reg2.connect(reg1)
            if keep_logic:
                new_exit2.access_rule = access_rule
            plando_entrances.append(new_exit2)

    return plando_entrances


def shuffle_transitions(world: "MessengerWorld") -> None:
    coupled = world.options.shuffle_transitions == ShuffleTransitions.option_coupled

    plando = world.options.plando_connections
    if plando:
        plando_entrances = connect_plando(world, plando, keep_logic)
    else:
        plando_entrances = []

    er_result = randomize_entrances(world, coupled, {0: [0]})

    world.transitions = sorted(itertools.chain(result.placements, plando_entrances),
                               key=lambda entrance: (TRANSITIONS.index(entrance.parent_region.name), entrance.name))

    for transition in world.transitions:
        if "->" not in transition.name:
            continue
        transition.parent_region.exits.remove(transition)
        transition.name = f"{transition.parent_region.name} -> {transition.connected_region.name}"
        transition.parent_region.exits.append(transition)

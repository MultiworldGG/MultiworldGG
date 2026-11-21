import itertools
from collections.abc import Mapping

from entrance_rando import randomize_entrances

from ..data.constants import DUNGEON_CONNECTIONS, PORTAL_CONNECTIONS, OracleOfSeasonsConnectionType
from ..data.regions import RegionName
from ..options import OracleOfSeasonsPortalShuffle
from ..world import OracleOfSeasonsWorld


def list_entrances_for_patch(
    pairing_dict: dict[str, str], prefix: str, vanilla_entrances: Mapping[RegionName, RegionName]
):
    seen_entrances = set()
    connections = {}
    for entrance1 in itertools.chain(
        vanilla_entrances, vanilla_entrances.values()
    ):  # Do them in order overworld then subrosia
        if entrance1 in seen_entrances:
            continue
        seen_entrances.add(entrance1)
        entrance2 = pairing_dict[f"{prefix}{entrance1}"].removeprefix(prefix)
        seen_entrances.add(entrance2)
        connections[entrance1] = entrance2
    return connections


def oos_randomize_entrances(world: OracleOfSeasonsWorld) -> None:
    target_group_lookup = {
        OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD: [OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA],
        OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA: [OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD],
        OracleOfSeasonsConnectionType.CONNECT_DUNGEON_OVERWORLD: [OracleOfSeasonsConnectionType.CONNECT_DUNGEON_INSIDE],
        OracleOfSeasonsConnectionType.CONNECT_DUNGEON_INSIDE: [OracleOfSeasonsConnectionType.CONNECT_DUNGEON_OVERWORLD],
    }
    if world.options.shuffle_portals == OracleOfSeasonsPortalShuffle.option_shuffle:
        target_group_lookup[OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD].append(
            OracleOfSeasonsConnectionType.CONNECT_PORTAL_OVERWORLD
        )
        target_group_lookup[OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA].append(
            OracleOfSeasonsConnectionType.CONNECT_PORTAL_SUBROSIA
        )

    placement_state = randomize_entrances(world, True, target_group_lookup)
    pairing_dict = dict(placement_state.pairings)
    if world.options.shuffle_portals:
        world.portal_connections = list_entrances_for_patch(pairing_dict, "enter ", PORTAL_CONNECTIONS)
    if world.options.shuffle_dungeons:
        dungeon_entrances = dict(DUNGEON_CONNECTIONS)
        if world.options.linked_heros_cave.is_samasa:
            dungeon_entrances[RegionName.d11_entrance] = RegionName.enter_d11
        world.dungeon_entrances = list_entrances_for_patch(pairing_dict, "", dungeon_entrances)
    elif world.options.linked_heros_cave.is_samasa:
        dungeon_entrances = dict(DUNGEON_CONNECTIONS)
        dungeon_entrances[RegionName.d11_entrance] = RegionName.enter_d11
        world.dungeon_entrances = dungeon_entrances

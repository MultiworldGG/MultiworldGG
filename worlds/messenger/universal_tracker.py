import logging
from collections import defaultdict
from collections.abc import Callable, Collection, Iterable
from typing import TYPE_CHECKING

from BaseClasses import Entrance, Location, Region
from Options import PlandoConnection
from rule_builder.rules import Has

from .connections import ONE_WAY_EXITS, RANDOMIZED_CONNECTIONS
from .options import ShuffleTransitions
from .portals import CHECKPOINTS, PORTALS, REGION_ORDER, SHOP_POINTS
from .rules import MessengerHardRules, MessengerRules
from .shop import FIGURINES, SHOP_ITEMS
from .transitions import TRANSITIONS

if TYPE_CHECKING:
    from . import MessengerWorld

logger = logging.getLogger(__name__)

REVERSED_RANDOMIZED_CONNECTIONS = {v: k for k, v in RANDOMIZED_CONNECTIONS.items()}
REVERSED_SHOP_ITEMS = {v.internal_name: k for k, v in (SHOP_ITEMS | FIGURINES).items()}
GLITCHED_ITEM = "Glitched Item"

TRACKER_ONE_WAY_DEFERRED_EXITS = [
    exit_name if exit_name.endswith("exit") else "HQ - " + exit_name for exit_name in ONE_WAY_EXITS
] + ["HQ - " + portal_name + " Portal" for portal_name in PORTALS]


def handle_auto_tabbing(data: str) -> int:
    match data:
        case "Level_01_NinjaVillage":
            return 1
        case "Level_02_AutumnHills":
            return 2
        case "Level_03_ForlornTemple":
            return 3
        case "Level_04_Catacombs":
            return 4
        case "Level_04_C_RiviereTurquoise":
            return 13
        case "Level_05_A_HowlingGrotto":
            return 6
        case "Level_05_B_SunkenShrine":
            return 14
        case "Level_06_A_BambooCreek":
            return 5
        case "Level_07_QuillshroomMarsh":
            return 7
        case "Level_08_SearingCrags":
            return 8
        case "Level_09_A_GlacialPeak":
            return 9
        case "Level_09_B_ElementalSkylands":
            return 15
        case "Level_10_A_TowerOfTime":
            return 10
        case "Level_11_A_CloudRuins":
            return 11
        case "Level_12_UnderWorld":
            return 12
        case _:
            return 0


TRACKER_PACK_CONFIG = {
    "external_pack_key": "ut_pack_path",
    "map_page_folder": "tracker",
    "map_page_maps": "maps/maps.json",
    "map_page_locations": [
        "locations/AutumnHills.json",
        "locations/BambooCreek.json",
        "locations/Catacombs.json",
        "locations/CloudRuins.json",
        "locations/CorruptedFuture.json",
        "locations/DarkCave.json",
        "locations/ElementalSkylands.json",
        "locations/ForlornTemple.json",
        "locations/GlacialPeak.json",
        "locations/HowlingGrotto.json",
        "locations/MusicBox.json",
        "locations/NinjaVillage.json",
        "locations/QuillshroomMarsh.json",
        "locations/RiviereTurquoise.json",
        "locations/SearingCrags.json",
        "locations/SunkenShrine.json",
        "locations/TheShop.json",
        "locations/TowerOfTime.json",
        "locations/Underworld.json",
    ],
    "map_page_setting_key": "Slot:{player}:CurrentRegion",
    "map_page_index": handle_auto_tabbing,
}


def find_spot(portal_key: int) -> str:
    """finds the spot associated with the portal key"""
    parent = REGION_ORDER[portal_key // 100]
    if portal_key % 100 == 0:
        return f"{parent} Portal"
    if portal_key % 100 // 10 == 1:
        return SHOP_POINTS[parent][portal_key % 10]
    return CHECKPOINTS[parent][portal_key % 10]


def reverse_portal_exits_into_portal_plando(portal_exits: list[int]) -> list[PlandoConnection]:
    return [
        PlandoConnection("Autumn Hills", find_spot(portal_exits[0]), "both"),
        PlandoConnection("Riviere Turquoise", find_spot(portal_exits[1]), "both"),
        PlandoConnection("Howling Grotto", find_spot(portal_exits[2]), "both"),
        PlandoConnection("Sunken Shrine", find_spot(portal_exits[3]), "both"),
        PlandoConnection("Searing Crags", find_spot(portal_exits[4]), "both"),
        PlandoConnection("Glacial Peak", find_spot(portal_exits[5]), "both"),
    ]

def reverse_shop_prices(
    shop_prices: dict[str, int], figures_prices: dict[str, int]
) -> tuple[dict[str, int], dict[str, int]]:
    return (
        {REVERSED_SHOP_ITEMS[item_internal_name]: price for item_internal_name, price in shop_prices.items()},
        {REVERSED_SHOP_ITEMS[item_internal_name]: price for item_internal_name, price in figures_prices.items()},
    )


def reverse_transitions_into_plando_connections(shuffle_transitions: ShuffleTransitions,
                                                transitions: list[list[int]]) -> list[PlandoConnection]:
    plando_connections = []

    for connection in [
        PlandoConnection(REVERSED_RANDOMIZED_CONNECTIONS[TRANSITIONS[transition[0]]], TRANSITIONS[transition[1]], "entrance")
        for transition in transitions
    ]:
        if shuffle_transitions == ShuffleTransitions.option_coupled and connection.exit in {con.entrance for con in plando_connections}:
            continue
        plando_connections.append(connection)

    return plando_connections


class MessengerGlitchedRules(MessengerRules):
    def __init__(self, world: "MessengerWorld") -> None:
        super().__init__(world)

        hard_logic = MessengerHardRules(world)
        has_glitched = Has(GLITCHED_ITEM)

        for connection in hard_logic.connection_rules.keys():
            hard_rule = hard_logic.connection_rules[connection]
            normal_rule = self.connection_rules[connection]
            if normal_rule != hard_rule:
                self.connection_rules[connection] = (has_glitched & hard_rule) | normal_rule

        for location in hard_logic.location_rules.keys():
            hard_rule = hard_logic.location_rules[location]
            normal_rule = self.location_rules[location]
            if normal_rule != hard_rule:
                self.location_rules[location] = (has_glitched & hard_rule) | normal_rule


def disconnect_deferred_exits(
    should_disconnect_level_exits: bool,
    should_disconnect_portal_exists: bool,
    starting_portals: Collection[str],
    get_entrance: Callable[[str], Entrance],
    get_location: Callable[[str], Location],
) -> tuple[dict[str, str], dict[str, list[str]], dict[str, list[str]]]:
    """Disconnect the exits, but save their destinations in a map to reconnect when it is visited."""

    deferred_connections = {}
    connections_to_hide = defaultdict(list)
    events_to_hide = defaultdict(list)

    def disconnect_exit(transition: Entrance, tracker_name_override: str | None) -> None:
        if tracker_name_override is not None:
            transition.name = tracker_name_override

        deferred_connections[transition.name] = transition.connected_region.name
        transition.connected_region.entrances.remove(transition)
        transition.connected_region = None

    if should_disconnect_level_exits:
        for exit_name in RANDOMIZED_CONNECTIONS.keys():
            exit_ = get_entrance(exit_name)

            if exit_.parent_region.name == "Tower HQ":
                name_override = "HQ - " + exit_.name
            else:
                name_override = None

            disconnect_exit(exit_, name_override)
    else:
        connections_to_hide |= hide_all_level_exits()

    for portal in PORTALS:
        actual_exit = get_entrance(f"ToTHQ {portal} Portal")
        tracker_exit_name = f"HQ - {portal} Portal"
        if should_disconnect_portal_exists:
            disconnect_exit(actual_exit, tracker_exit_name)
        else:
            connections_to_hide["Overworld"].append(tracker_exit_name)

        event_name = f"{portal} Portal"
        unlock_event = get_location(event_name)

        hq = actual_exit.parent_region
        tracker_event_name = f"{portal} - Portal unlock"
        if event_name in starting_portals:
            unlock_event.parent_region.locations.remove(unlock_event)
            hq.locations.append(unlock_event)
            unlock_event.parent_region = hq
            events_to_hide[portal].append(tracker_event_name)

        unlock_event.name = tracker_event_name
        unlock_event.access_rule = lambda _: False

    return deferred_connections, connections_to_hide, events_to_hide


def hide_all_entrances_and_events() -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    connections_to_hide: dict[str, list[str]] = hide_all_level_exits()
    events_to_hide: dict[str, list[str]] = defaultdict(list)

    for portal in PORTALS:
        connections_to_hide[portal].append(f"HQ - {portal} Portal")
        events_to_hide[portal].append(f"{portal} - Portal unlock")

    return connections_to_hide, events_to_hide


def hide_all_level_exits() -> dict[str, list[str]]:
    exits_by_map = defaultdict(list)

    for e in RANDOMIZED_CONNECTIONS:
        try:
            map_name = e[: e.index(" - ")]
        except ValueError:
            map_name = "Overworld"
        exits_by_map[map_name].append(e)

    exits_by_map["Overworld"] += exits_by_map["Dark Cave"]

    return exits_by_map


def connect_visited_entrances(
    connections_map: dict[str, str],
    visited_exits: list[str],
    get_region: Callable[[str], Region],
    get_entrance: Callable[[str], Entrance],
    decoupled: bool = False,
) -> None:
    def connect_exit_to_destination(visited_exit: str) -> tuple[Entrance, Region]:
        _transition = get_entrance(visited_exit)
        _destination = get_region(connections_map[visited_exit])
        _transition.connect(_destination)
        return _transition, _destination

    for e in visited_exits:
        try:
            transition, destination = connect_exit_to_destination(e)
            if not decoupled and transition.name not in TRACKER_ONE_WAY_DEFERRED_EXITS:
                coupled_exit = f"{destination.name} exit"
                connect_exit_to_destination(coupled_exit)
        except KeyError:
            logger.warning(f"Unable to find region/entrance for visited exit {e}, skipping connection.")
            continue


def unlock_portals(unlocked_portals: Iterable[str], get_location: Callable[[str], Location]) -> None:
    for p in unlocked_portals:
        event_name = p.replace(" Portal", " - Portal unlock")
        unlock_event = get_location(event_name)
        # This assumes the events have no requirements in itself. If an item is required, it's handled by the region.
        unlock_event.access_rule = lambda _: True

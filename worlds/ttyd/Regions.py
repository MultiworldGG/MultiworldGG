import typing

from BaseClasses import Region
from .Locations import (TTYDLocation, shadow_queen, LocationData)
from . import StateLogic, get_locations_by_tags

if typing.TYPE_CHECKING:
    from . import TTYDWorld


def get_regions_dict() -> dict[str, list[LocationData]]:
    """
    Returns a dictionary mapping region names to their corresponding location data lists.
    """
    return {
        "Rogueport": get_locations_by_tags("rogueport"),
        "Rogueport (Westside)": get_locations_by_tags("rogueport_westside"),
        "Rogueport Sewers": get_locations_by_tags("sewers"),
        "Rogueport Sewers Westside": get_locations_by_tags("sewers_westside"),
        "Rogueport Sewers Westside Ground": get_locations_by_tags("sewers_westside_ground"),
        "Petal Meadows (Left)": get_locations_by_tags("petal_left"),
        "Petal Meadows (Right)": get_locations_by_tags("petal_right"),
        "Hooktail's Castle": get_locations_by_tags("hooktails_castle"),
        "Boggly Woods": get_locations_by_tags("boggly_woods"),
        "Great Tree": get_locations_by_tags("great_tree"),
        "Glitzville": get_locations_by_tags("glitzville"),
        "Twilight Town": get_locations_by_tags("twilight_town"),
        "Twilight Trail": get_locations_by_tags("twilight_trail"),
        "Creepy Steeple": get_locations_by_tags("creepy_steeple"),
        "Keelhaul Key": get_locations_by_tags("keelhaul_key"),
        "Pirate's Grotto": get_locations_by_tags("pirates_grotto"),
        "Excess Express": get_locations_by_tags("excess_express"),
        "Riverside Station": get_locations_by_tags("riverside"),
        "Poshley Heights": get_locations_by_tags("poshley_heights"),
        "Fahr Outpost": get_locations_by_tags("fahr_outpost"),
        "X-Naut Fortress": get_locations_by_tags("xnaut_fortress"),
        "Palace of Shadow": get_locations_by_tags("palace"),
        "Palace of Shadow (Post-Riddle Tower)": get_locations_by_tags("riddle_tower"),
        "Pit of 100 Trials": get_locations_by_tags("pit"),
        "Shadow Queen": shadow_queen,
        "Tattlesanity": get_locations_by_tags("tattle")
    }


def get_region_connections_dict(world: "TTYDWorld") -> dict[tuple[str, str], typing.Optional[typing.Callable]]:
    """
    Returns a dictionary mapping region connections (source, target) to their access rules.
    If a rule is None, the connection is always available.
    """
    connections = {
        ("Menu", "Rogueport"): None,
        ("Menu", "Rogueport (Westside)"): None,
        ("Menu", "Tattlesanity"): None,
        ("Rogueport", "Rogueport Sewers"): None,
        ("Rogueport", "Rogueport Sewers Westside"):
            lambda state: StateLogic.sewer_westside(state, world.player),
        ("Rogueport Sewers Westside", "Twilight Town"):
            lambda state: state.has("Yoshi", world.player),
        ("Rogueport", "Rogueport Sewers Westside Ground"):
            lambda state: StateLogic.sewer_westside_ground(state, world.player),
        ("Rogueport Sewers Westside Ground", "Pit of 100 Trials"):
            lambda state: StateLogic.pit_westside_ground(state, world.player),
        ("Rogueport Sewers Westside Ground", "Rogueport (Westside)"): None,
        ("Rogueport Sewers Westside Ground", "Twilight Town"):
            lambda state: StateLogic.ultra_boots(state, world.player),
        ("Rogueport Sewers", "Pit of 100 Trials"):
            lambda state: StateLogic.pit(state, world.player),
        ("Rogueport", "Shadow Queen"):
            lambda state, star_shuffle=world.options.star_shuffle.value: StateLogic.palace(state, world.player, world.options.goal_stars.value, star_shuffle),
        ("Rogueport", "Palace of Shadow"):
            lambda state, star_shuffle=world.options.star_shuffle.value: StateLogic.palace(state, world.player, world.options.palace_stars.value, star_shuffle),
        ("Palace of Shadow", "Palace of Shadow (Post-Riddle Tower)"):
            lambda state: StateLogic.riddle_tower(state, world.player),
        ("Palace of Shadow (Post-Riddle Tower)", "Shadow Queen"):
            lambda state: state.can_reach("Palace of Shadow Final Staircase: Ultra Shroom", "Location", world.player) and state.has("stars", world.player, world.options.goal_stars.value),
        ("Rogueport", "Fahr Outpost"):
            lambda state: StateLogic.fahr_outpost(state, world.player),
        ("Rogueport", "Keelhaul Key"):
            lambda state: StateLogic.keelhaul_key(state, world.player),
        ("Keelhaul Key", "Pirate's Grotto"):
            lambda state: StateLogic.pirates_grotto(state, world.player),
        ("Rogueport", "Rogueport (Westside)"):
            lambda state: StateLogic.westside(state, world.player),
        ("Rogueport (Westside)", "Glitzville"):
            lambda state: StateLogic.glitzville(state, world.player),
        ("Rogueport (Westside)", "Rogueport Sewers Westside"):
            lambda state: state.has("Paper Mode", world.player),
        ("Rogueport (Westside)", "Excess Express"):
            lambda state: StateLogic.excess_express(state, world.player),
        ("Excess Express", "Riverside Station"):
            lambda state: StateLogic.riverside(state, world.player),
        ("Riverside Station", "Poshley Heights"):
            lambda state: StateLogic.poshley_heights(state, world.player),
        ("Rogueport Sewers", "Petal Meadows (Left)"):
            lambda state: StateLogic.petal_left(state, world.player),
        ("Rogueport Sewers", "Boggly Woods"):
            lambda state: StateLogic.boggly_woods(state, world.player),
        ("Twilight Town", "Twilight Trail"):
            lambda state: StateLogic.twilight_trail(state, world.player),
        ("Twilight Trail", "Creepy Steeple"):
            lambda state: StateLogic.steeple(state, world.player),
        ("Petal Meadows (Left)", "Petal Meadows (Right)"): None,
        ("Petal Meadows (Left)", "Hooktail's Castle"):
            lambda state: StateLogic.hooktails_castle(state, world.player),
        ("Boggly Woods", "Great Tree"):
            lambda state: StateLogic.great_tree(state, world.player),
        ("Fahr Outpost", "X-Naut Fortress"):
            lambda state: StateLogic.moon(state, world.player)
    }

    if world.options.blue_pipe_toggle:
        connections[("Rogueport Sewers", "Petal Meadows (Right)")] = lambda state: StateLogic.super_blue_pipes(state, world.player)
        connections[("Rogueport Sewers", "Boggly Woods")] = lambda state: StateLogic.super_blue_pipes(state, world.player)
        connections[("Rogueport Sewers", "Keelhaul Key")] = lambda state: StateLogic.ultra_blue_pipes(state, world.player)
        connections[("Rogueport Sewers", "Poshley Heights")] = lambda state: StateLogic.ultra_blue_pipes(state, world.player)

    return connections



def create_regions(world: "TTYDWorld"):
    # Create menu region (always included)
    menu_region = Region("Menu", world.player, world.multiworld)
    world.multiworld.regions.append(menu_region)

    # Create other regions from dictionary, excluding any in excluded_regions
    regions_dict = get_regions_dict()
    for name, locations in regions_dict.items():
        if name not in world.excluded_regions:
            create_region(world, name, locations)
        else:
            world.disabled_locations.update([loc.name for loc in locations if loc.name not in world.disabled_locations])


def connect_regions(world: "TTYDWorld"):


    connections_dict = get_region_connections_dict(world)
    names: typing.Dict[str, int] = {}

    # Connect regions based on the connections dictionary, excluding any with excluded regions
    for (source, target), rule in connections_dict.items():
        # Skip connections where either the source or target is in excluded_regions
        if source in world.excluded_regions or target in world.excluded_regions:
            continue
        if source == "Rogueport" and target == "Shadow Queen" and not world.options.palace_skip:
            continue
        if source == "Menu" and target == "Rogueport (Westside)" and not world.options.open_westside:
            continue

        # Verify that both regions exist before trying to connect them
        try:
            world.multiworld.get_region(source, world.player)
            world.multiworld.get_region(target, world.player)
            connect(world, names, source, target, rule)
        except Exception:
            continue


def register_indirect_connections(world: "TTYDWorld"):
    world.multiworld.register_indirect_condition(world.get_region("Rogueport Sewers Westside Ground"),
                                                 world.get_entrance("Fahr Outpost"))
    world.multiworld.register_indirect_condition(world.get_region("Rogueport Sewers Westside"),
                                                 world.get_entrance("Fahr Outpost"))


def create_region(world: "TTYDWorld", name: str, locations: list[LocationData]):
    """Create a region with the given name and locations."""
    reg = Region(name, world.player, world.multiworld)
    reg.add_locations({loc.name: loc.id for loc in locations if loc.name not in world.disabled_locations}, TTYDLocation)
    world.multiworld.regions.append(reg)


def connect(world: "TTYDWorld",
            used_names: typing.Dict[str, int],
            source: str,
            target: str,
            rule: typing.Optional[typing.Callable] = None):
    """Connect two regions with an optional access rule."""
    source_region = world.multiworld.get_region(source, world.player)
    target_region = world.multiworld.get_region(target, world.player)

    if target not in used_names:
        used_names[target] = 1
        name = target
    else:
        used_names[target] += 1
        name = target + (" " * used_names[target])

    source_region.connect(target_region, name, rule)

"""Generator to create the door connections in entrance randomization."""

from __future__ import annotations

from enum import IntEnum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from . import WotWWorld

from .generated_data.DoorData import doors_map

class Groups(IntEnum):
    # Main room
    MAIN = 0
    OW_1O_2 = 1
    MOKI_HUT = 2
    OW_3 = 3
    RIDGE = 4
    # Non dead-ends
    WILLOW = 5
    IW_1 = 6  # First floor of Inner Wellspring
    # Dead-ends
    WOODS_HUT = 7
    IW_2 = 8
    RUINS = 9
    DEAD = 10

group_lookup: dict[str, Groups] = {
    "GladesTown.TwillenHome (Door)": Groups.MOKI_HUT,
    "GladesTown.KeyMokiHutInside (Door)": Groups.DEAD,
    "GladesTown.MotayHutDoor (Door)": Groups.MAIN,
    "GladesTown.MotayHutInside (Door)": Groups.DEAD,
    "GladesTown.UpperWest (Door)": Groups.MAIN,
    "GladesTown.InsideThirdHut (Door)": Groups.DEAD,
    "GladesTown.AcornMoki (Door)": Groups.MAIN,
    "GladesTown.AcornCave (Door)": Groups.DEAD,
    "GladesTown.AboveOpher (Door)": Groups.MAIN,
    "GladesTown.StorageHut (Door)": Groups.DEAD,
    "GladesTown.LupoHouse (Door)": Groups.MAIN,
    "GladesTown.InsideLupoHouse (Door)": Groups.DEAD,
    "GladesTown.HoleHutEntrance (Door)": Groups.MAIN,
    "GladesTown.InsideHoleHut (Door)": Groups.DEAD,
    "OuterWellspring.EntranceDoor (Door)": Groups.MAIN,
    "OuterWellspring.WestDoor (Door)": Groups.OW_1O_2,
    "OuterWellspring.EastDoor (Door)": Groups.OW_1O_2,
    "OuterWellspring.TopDoor (Door)": Groups.OW_3,
    "InnerWellspring.EntranceDoor (Door)": Groups.IW_1,
    "InnerWellspring.WestDoor (Door)": Groups.IW_1,
    "InnerWellspring.EastDoor (Door)": Groups.IW_2,
    "InnerWellspring.Teleporter (Door)": Groups.DEAD,
    "WoodsEntry.FamilyHut (Door)": Groups.MAIN,
    "WoodsEntry.FamilyHutInside (Door)": Groups.WOODS_HUT,
    "UpperReach.TreeRoom (Door)": Groups.MAIN,
    "UpperReach.SeedHut (Door)": Groups.DEAD,
    "UpperWastes.OutsideRuins (Door)": Groups.MAIN,
    "WindtornRuins.UpperRuinsDoor (Door)": Groups.RUINS,
    "WeepingRidge.WillowEntranceLedge (Door)": Groups.RIDGE,
    "WillowsEnd.Entry (Door)": Groups.WILLOW,
    "WillowsEnd.Upper (Door)": Groups.WILLOW,
    "WillowsEnd.ShriekArena (Door)": Groups.DEAD
}

# Rules to prevent a group to connect to a door in the listed group.
forbidden_conn_lookup: dict[Groups, list[Groups]] = {
    ### Main rooms (groups 0 to 3)
    Groups.MAIN: [],
    # Don't connect the doors opened by the lever in Inner Wellspring 1 to this room
    Groups.OW_1O_2: [Groups.IW_1],
    # Don't connect the Key Moki Hut to the Doll location in the woods hut (as it is required to enter)
    Groups.MOKI_HUT: [Groups.WOODS_HUT, Groups.WILLOW, Groups.IW_1],
    # Entering the 3rd room in Wellspring requires removing the corruption from Inner Wellspring 2
    Groups.OW_3: [Groups.IW_2, Groups.WILLOW, Groups.IW_1],
    # Accessing the Weeping Ridge door requires Seir from the Ruins (without glitches)
    Groups.RIDGE: [Groups.RUINS, Groups.WILLOW, Groups.IW_1],
    ### Other rooms that are not dead ends (groups 4, 5): don't connect them to restricted groups or themselves
    # Example: WeepingRidge-InnerWellspringEntrance + InnerWellspringWest-WindtornRuins must be prevented
    Groups.WILLOW: [
        Groups.MOKI_HUT, Groups.OW_3, Groups.RIDGE, Groups.WOODS_HUT, Groups.IW_2, Groups.RUINS, Groups.WILLOW
    ],
    # No connection with the OW_1O_2 doors
    Groups.IW_1: [
        Groups.OW_1O_2,
        Groups.MOKI_HUT,
        Groups.OW_3,
        Groups.RIDGE,
        Groups.WOODS_HUT,
        Groups.IW_2,
        Groups.RUINS,
        Groups.IW_1,
    ],
    ### Dead ends: don't connect these to themselves to not lock the generator (groups 6 to 8)
    # No connection with the Key Moki hut
    Groups.WOODS_HUT: [
        Groups.MOKI_HUT, Groups.WOODS_HUT, Groups.IW_2, Groups.RUINS, Groups.DEAD, Groups.WILLOW, Groups.IW_1
    ],
    # No connection with the top door of Outer Wellspring
    Groups.IW_2: [Groups.OW_3, Groups.WOODS_HUT, Groups.IW_2, Groups.RUINS, Groups.DEAD, Groups.WILLOW, Groups.IW_1],
    # No connection with Weeping Ridge
    Groups.RUINS: [Groups.RIDGE, Groups.WOODS_HUT, Groups.IW_2, Groups.RUINS, Groups.DEAD, Groups.WILLOW, Groups.IW_1],
    Groups.DEAD: [Groups.WOODS_HUT, Groups.IW_2, Groups.RUINS, Groups.DEAD],
}

groups: dict[Groups, list[str]] = {
    Groups.MAIN: [
        "GladesTown.HoleHutEntrance (Door)",
        "GladesTown.MotayHutDoor (Door)",
        "GladesTown.UpperWest (Door)",
        "GladesTown.AcornMoki (Door)",
        "GladesTown.AboveOpher (Door)",
        "GladesTown.LupoHouse (Door)",
        "OuterWellspring.EntranceDoor (Door)",
        "WoodsEntry.FamilyHut (Door)",
        "UpperReach.TreeRoom (Door)",
        "UpperWastes.OutsideRuins (Door)",
    ],
    Groups.OW_1O_2: [
        "OuterWellspring.WestDoor (Door)",
        "OuterWellspring.EastDoor (Door)",
    ],
    Groups.MOKI_HUT: [
        "GladesTown.TwillenHome (Door)",
    ],
    Groups.OW_3: [
        "OuterWellspring.TopDoor (Door)",
    ],
    Groups.RIDGE: [
        "WeepingRidge.WillowEntranceLedge (Door)",
    ],
    Groups.WILLOW: [
        "WillowsEnd.Entry (Door)",
        "WillowsEnd.Upper (Door)",
    ],
    Groups.IW_1: [
        "InnerWellspring.EntranceDoor (Door)",
        "InnerWellspring.WestDoor (Door)",
    ],
    Groups.WOODS_HUT: [
        "WoodsEntry.FamilyHutInside (Door)",
    ],
    Groups.IW_2: [
        "InnerWellspring.EastDoor (Door)",
    ],
    Groups.RUINS: [
        "WindtornRuins.UpperRuinsDoor (Door)",
    ],
    Groups.DEAD: [
        "GladesTown.KeyMokiHutInside (Door)",
        "GladesTown.MotayHutInside (Door)",
        "GladesTown.InsideThirdHut (Door)",
        "GladesTown.AcornCave (Door)",
        "GladesTown.StorageHut (Door)",
        "GladesTown.InsideLupoHouse (Door)",
        "GladesTown.InsideHoleHut (Door)",
        "InnerWellspring.Teleporter (Door)",
        "UpperReach.SeedHut (Door)",
        "WillowsEnd.ShriekArena (Door)",
    ],
}


class ERGeneratorWotW:
    """
    Generator for door randomization.

    The algorithm ignores logic for the placements, and only rely on the map structure. The restrictions between the
    groups prevent the placements that would make some doors unreachable once logic is applied.
    It starts from a random door in the main area, and connect it to a random door from a new group. If all doors are
    already reachable, make connections between these.
    """

    # In coupled mode, the door exits and entrances are similar, since the reverse connection is also made.

    # Door exits that are not linked yet.
    unlinked_doors: list[str] = []

    # Door entrances that cannot be reached yet.
    unaccessible_doors: list[str] = []

    # Doors entrances that can be reached (ignoring the logic rules), and not linked yet.
    accessible_doors: list[str] = []

    # 1 to 1 mapping of door connections.
    # In coupled mode, it has 16 pairings at the end (key <-> item) ; and 32 pairings for decoupled (key -> item).
    placements: dict[str, str] = {}

    def __init__(self):
        self.placements = {}
        # Start the randomization from the main group.
        self.accessible_doors = (
            groups[Groups.MAIN]
            + groups[Groups.OW_1O_2]
            + groups[Groups.MOKI_HUT]
            + groups[Groups.OW_3]
            + groups[Groups.RIDGE]
        )
        self.unlinked_doors = list(group_lookup.keys())
        self.unaccessible_doors = list(group_lookup.keys())
        for door in self.accessible_doors:
            try:
                self.unaccessible_doors.remove(door)
            except ValueError:
                print(door)
                print(
                    f"Error\n\n"
                    f"placements: {self.placements}\n\n"
                    f"unlinked_doors: {self.unlinked_doors}\n\n"
                    f"unaccessible_doors: {self.unaccessible_doors}\n\n"
                    f"accessible_doors: {self.accessible_doors}"
                )

    def create_connection(self, world: WotWWorld, coupled: bool) -> bool:
        """Attempt to make a door connection. Return False if the connection failed."""
        # Target in priority the doors that cannot be reached yet.
        if self.unaccessible_doors:
            flag_new_group = True  # Flag that tracks if a new group will get reached.
            target_doors = list.copy(self.unaccessible_doors)
        else:  # All doors can already be reached
            flag_new_group = False
            target_doors = list.copy(self.unlinked_doors)
        world.random.shuffle(self.accessible_doors)
        world.random.shuffle(target_doors)

        # Loop for all combinations of origin to target door and check that the connection in allowed
        for target in target_doors:
            for origin in self.accessible_doors:
                origin_group: Groups = group_lookup[origin]
                target_group: Groups = group_lookup[target]
                if target_group not in forbidden_conn_lookup[origin_group] and origin != target:
                    # Found a connection: register it
                    self.placements.setdefault(origin, target)

                    # Update the ER state
                    if coupled:  # Origin door is linked only in coupled mode
                        self.unlinked_doors.remove(origin)
                    self.unlinked_doors.remove(target)
                    self.accessible_doors.remove(origin)

                    if flag_new_group:
                        # A new group is reached: the other doors from the group become accessible (except dead-ends).
                        if target_group != Groups.DEAD:
                            self.accessible_doors += groups[target_group]
                            if coupled:
                                self.accessible_doors.remove(target)
                            for new_door in groups[target_group]:
                                self.unaccessible_doors.remove(new_door)
                        else:  # Added a dead-end, only remove this one from the unaccessible doors.
                            self.unaccessible_doors.remove(target)
                            if not coupled:  # In decoupled, the new door is not linked yet
                                self.accessible_doors.append(target)

                    elif coupled:  # unaccessible_doors is empty, so no new doors are accessible.
                        self.accessible_doors.remove(target)  # Target door is linked only in coupled mode

                    return True  # Connection successful

        return False  # Failure: no valid pairing


def generate_er_connections(world: WotWWorld, coupled: bool) -> list[int]:
    """Randomize and create the entrances between the doors. Return the pairing data to send through slot_data."""
    max_attempts = 5
    current_attempt = 1
    result = True  # Track success of the entrance connection

    while current_attempt <= max_attempts:
        er_gen = ERGeneratorWotW()
        while er_gen.unlinked_doors:
            result = er_gen.create_connection(world=world, coupled=coupled)
            if not result:
                current_attempt += 1
                break  # Go to the next attempt

        if result:  # Exit the while loop if the generation was successful
            break

    if current_attempt > max_attempts:
        raise RuntimeError(
            f"Entrance Randomization failed {max_attempts} times: no valid connection is possible.\nCurrent state:\n\n"
            f"placements: {er_gen.placements}\n\n"
            f"unlinked_doors: {er_gen.unlinked_doors}\n\n"
            f"unaccessible_doors: {er_gen.unaccessible_doors}\n\n"
            f"accessible_doors: {er_gen.accessible_doors}"
        )

    er_pairings = er_gen.placements

    # Connect the entrances
    for entry, target in er_pairings.items():
        # For the exit door, connect to the base region and not the door one (thus remove ` (Door)` from the name,
        # hence the [:-7]) This matters in decoupled mode, since you cannot always reenter the door you just exited.
        world.get_region(entry).connect(world.get_region(target[:-7]))
        if coupled:
            world.get_region(target).connect(world.get_region(entry[:-7]))

    expected_connections = 16 if coupled else 32
    if len(er_pairings) != expected_connections:
        mode = "coupled" if coupled else "decoupled"
        raise RuntimeError(
            f"er_pairings have {len(er_pairings)} connections in {mode} mode, expected {expected_connections}.\n"
            "Something went really wrong, please report this issue to the dev.\n\n"
            "Generator state:\n\n"
            f"placements: {er_gen.placements}\n\n"
            f"unlinked_doors: {er_gen.unlinked_doors}\n\n"
            f"unaccessible_doors: {er_gen.unaccessible_doors}\n\n"
            f"accessible_doors: {er_gen.accessible_doors}"
        )

    # Create the data list of the pairings to give to slot_data.
    er_door_ids = [0] * 32
    for source_exit, target_entrance in er_pairings.items():
        er_door_ids[doors_map[source_exit] - 1] = doors_map[target_entrance]
        if coupled:  # Reverse mapping only made in coupled mode
            er_door_ids[doors_map[target_entrance] - 1] = doors_map[source_exit]

    return er_door_ids

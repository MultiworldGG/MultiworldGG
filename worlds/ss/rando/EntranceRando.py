from typing import TYPE_CHECKING
from copy import deepcopy

from Options import OptionError

from ..Entrances import *
from ..Locations import LOCATION_TABLE
from ..Options import SSOptions
from ..Constants import *

from ..logic.Requirements import ALL_REQUIREMENTS, exit_requirements

if TYPE_CHECKING:
    from .. import SSWorld


class EntranceRando:
    """
    Class handles dungeon entrance rando and trial rando.
    """

    def __init__(self, world: "SSWorld"):
        self.world = world
        self.multiworld = world.multiworld

        self.regions: dict[str, dict] = {}
        for reg in ALL_REQUIREMENTS.keys():
            self.regions[reg] = {
                "accessed": True if reg == self.world.origin_region_name else False,
                "exits": [],
                "entrances": [],
            }
        self.entrances: list = []
        self.exits: list = []

        self.placed_entrances = []
        self.placed_exits = []

        self.entrance_mapping = SSEntranceMapping(self.world)
        self.exit_requirements = exit_requirements

        self.scanned_placeable_exits = set()
        self.scanned_reachable_regions = set()
        self.scanned_exits = set()
        self.reachable_exits: set[SSExit] = set()

        self.dungeon_exits_to_place = {
            "Skyview": [],
            "Earth Temple": [],
            "Lanayru Mining Facility": [],
            "Ancient Cistern": [],
            "Sandship": [],
            "Fire Sanctuary": [],
            "Sky Keep": [],
        }

        self.dungeon_connections: dict = {}
        self.dungeons: list[str] = list(VANILLA_DUNGEON_CONNECTIONS.keys())
        self.dungeon_entrances: list[str] = list(VANILLA_DUNGEON_CONNECTIONS.values())
        self.trial_connections: dict = {}
        self.trials: list[str] = list(VANILLA_TRIAL_CONNECTIONS.keys())
        self.trial_gates: list[str] = list(VANILLA_TRIAL_CONNECTIONS.values())

        self.starting_entrance: dict = {}
        self.starting_statues: dict[str, tuple] = {}

    def randomize_entrances(self) -> None:
        """
        Docstring for randomize_entrances
        
        :param self: Description
        """

        # Place plando entrances first
        self.place_plando_entrances()

        print("----- Building path to sealed temple")
        self.build_path(self.world.origin_region_name)

        req_dun_regions = [reg for dun, reg in DUNGEON_INITIAL_REGIONS.items() if dun in self.world.dungeons.required_dungeons]
        non_req_dun_regions = [reg for dun, reg in DUNGEON_INITIAL_REGIONS.items() if dun not in self.world.dungeons.required_dungeons and dun != "Sky Keep"]
        if self.world.dungeons.sky_keep_required:
            req_dun_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])
        else:
            non_req_dun_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])

        for dun in req_dun_regions:
            dun_name = [name for name, reg in DUNGEON_INITIAL_REGIONS.items() if reg == dun].pop()
            print(f"----- Building path to dungeon: {dun}")
            self.build_dungeon_paths(dun, self.world.origin_region_name)
            ent = [en for ex, en, x in self.entrance_mapping.mapping if ex == SSExit(dun, "Dungeon Exit")].pop()
            for ex in self.dungeon_exits_to_place[dun_name]:
                SSExit(ex.region, ex.name, world=self.world).link(ent, reversible=False, plando=True)
        
        for dun in non_req_dun_regions:
            dun_name = [name for name, reg in DUNGEON_INITIAL_REGIONS.items() if reg == dun].pop()
            print(f"----- Building path to dungeon: {dun}")
            self.build_dungeon_paths(dun, self.world.origin_region_name)
            ent = [en for ex, en, x in self.entrance_mapping.mapping if ex == SSExit(dun, "Dungeon Exit")].pop()
            for ex in self.dungeon_exits_to_place[dun_name]:
                if self.world.options.empty_unrequired_dungeons:
                    SSExit(ex.region, ex.name, world=self.world).link(ent, reversible=False, plando=True, no_logic=True)
                else:
                    SSExit(ex.region, ex.name, world=self.world).link(ent, reversible=False, plando=True)

        for reg, data in ALL_REQUIREMENTS.items():
            if len(data["exits"].keys()) == 1 and SSExit(reg, list(data["exits"].keys())[0]) not in self.entrance_mapping.exits:
                print(f"----- Building path to dead end region: {reg}")
                self.build_dead_end_paths(reg, self.world.origin_region_name)

        # Now, place remaining entrances
        print("----- Connecting remaining entrances")
        self.finalize_entrance_placements(dead_ends=True, new_regions_only=False)

    def place_plando_entrances(self) -> None:
        """
        Docstring for place_plando_entrances
        
        :param self: Description
        """
        bed_region_entrances = []
        for reg, data in ALL_REQUIREMENTS.items():
            if reg not in BED_REGIONS:
                continue
            for ent in data["exits"].keys():
                if SSEntrance(reg, ent, world=self.world) not in self.entrance_mapping.entrances:
                    bed_region_entrances.append(SSEntrance(reg, ent, world=self.world))

        # First, make sure skyloft is connected to a bed region
        placeable_skyloft_exits = [SSExit("Upper Skyloft", ent, world=self.world) for ent, req in ALL_REQUIREMENTS["Upper Skyloft"]["exits"].items() if req == "Nothing"]
        placeable_skyloft_exits.extend([SSExit("Central Skyloft", ent, world=self.world) for ent, req in ALL_REQUIREMENTS["Central Skyloft"]["exits"].items() if req == "Nothing" and not "Bazaar" in ent])
        placeable_skyloft_exits.extend([SSExit("Skyloft Village", ent, world=self.world) for ent, req in ALL_REQUIREMENTS["Skyloft Village"]["exits"].items() if req == "Nothing"])

        self.world.random.shuffle(placeable_skyloft_exits)

        ent_placed = False
        for ex in placeable_skyloft_exits:
            if ex not in self.entrance_mapping.exits:
                ent = self.world.random.choice(bed_region_entrances)
                bed_region_entrances.remove(ent)

                print(ex)
                print(ent)
                ex.link(ent, reversible=True, plando=False)
                ent_placed = True
                break

        if not ent_placed:
            raise Exception("Error during SS exit/entrance plando placement")
        
        night_needed_regions = {
            # Regions that need direct access to either a region with a bed or night skyloft
            "Upper Skyloft - Sparring Hall": [
                "Door",
            ],
            "Central Skyloft - Under Waterfall": [
                "Cave Entrance",
            ],
            "Sky - Lumpy Pumpkin - Outside": [
                "South Door",
                "North Door",
            ],
        }

        placeable_skyloft_exits.extend([SSExit("Upper Skyloft - Knight Academy", ent, world=self.world) for ent, req in ALL_REQUIREMENTS["Upper Skyloft - Knight Academy"]["exits"].items() if req == "Nothing"])
        placeable_skyloft_exits.extend([SSExit("Sky - Lumpy Pumpkin - Inside", ent, world=self.world) for ent, req in ALL_REQUIREMENTS["Sky - Lumpy Pumpkin - Inside"]["exits"].items() if req == "Nothing"])

        for reg, region_entrances in night_needed_regions.items():
            ent = self.world.random.choice([SSEntrance(reg, ent, world=self.world) for ent in region_entrances if SSEntrance(reg, ent, world=self.world) not in self.entrance_mapping.entrances])
            
            ex = self.world.random.choice([ex for ex in placeable_skyloft_exits if ex not in self.entrance_mapping.exits])
            if ex.region == "Upper Skyloft - Knight Academy":
                for entr, req in ALL_REQUIREMENTS["Upper Skyloft - Knight Academy"]["exits"].items():
                    if SSExit("Upper Skyloft - Knight Academy", entr, world=self.world) in placeable_skyloft_exits:
                        placeable_skyloft_exits.remove(SSExit("Upper Skyloft - Knight Academy", entr, world=self.world))
            if ex.region == "Sky - Lumpy Pumpkin - Inside":
                for entr, req in ALL_REQUIREMENTS["Sky - Lumpy Pumpkin - Inside"]["exits"].items():
                    if SSExit("Sky - Lumpy Pumpkin - Inside", entr, world=self.world) in placeable_skyloft_exits:
                        placeable_skyloft_exits.remove(SSExit("Sky - Lumpy Pumpkin - Inside", entr, world=self.world))
            
            print(f"{ex} ---> {ent}")
            ex.link(ent, reversible=True, plando=False)
            

    def build_path(self, region) -> None:
        """
        Start by building a path to sealed temple
        
        :param self: SSWorld Entrance class
        :param region: Name of the region
        """

        if region == "Sealed Grounds - Sealed Temple":
            return
        
        self.find_reachable_region_exits(self.world.origin_region_name)
        ex = self.world.random.choice(list(self.reachable_exits))
        entrance_to_place = self.find_entrance_pairing(ex, dungeons=False, dead_ends=False, banned=set([ogex.toEntrance() for ogex in self.reachable_exits]))
        print(f"{ex} ---> {entrance_to_place}")
        reversible = ex.reversible and entrance_to_place.reversible
        if not reversible:
            if ex.reversible:
                # In this case, exit is reversible but entrance is not
                # Since this entrance will be inaccessible, lets remove it
                self.regions[ex.region]["entrances"].remove(SSEntrance(ex.region, ex.name, world=self.world))
            if entrance_to_place.reversible:
                # In this case, entrance is reversible but exit is not
                # Since the entrance can be traveled back through but we have no where to send
                # the player, let's just send them back to the starting entrance
                entrance_to_place.toExit().link_to_start()
        ex.link(entrance_to_place, reversible=reversible)

        self.build_path(entrance_to_place.region)

    def build_dungeon_paths(self, dun, region):
        """
        Docstring for build_dungeon_paths
        
        :param self: Description
        :param region: Description
        """

        if region == dun:
            return
        
        self.find_reachable_region_exits(self.world.origin_region_name)
        ex = self.world.random.choice(list(self.reachable_exits))
        entrance_to_place = self.find_entrance_pairing(ex, dungeons=[dun], dead_ends=False, banned=set([ogex.toEntrance() for ogex in self.reachable_exits]))
        print(f"{ex} ---> {entrance_to_place}")

        if self.world.options.empty_unrequired_dungeons and entrance_to_place.region == dun:
            if dun == "Sky Keep":
                if self.world.dungeons.sky_keep_required:
                    no_logic = False
                else:
                    no_logic = True
            else:
                if dun in self.world.dungeons.banned_dungeons:
                    no_logic = True
                else:
                    no_logic = False
        else:
            no_logic = False

        reversible = ex.reversible and entrance_to_place.reversible
        if not reversible:
            if ex.reversible:
                # In this case, exit is reversible but entrance is not
                # Since this entrance will be inaccessible, lets remove it
                self.regions[ex.region]["entrances"].remove(SSEntrance(ex.region, ex.name, world=self.world))
            if entrance_to_place.reversible:
                # In this case, entrance is reversible but exit is not
                # Since the entrance can be traveled back through but we have no where to send
                # the player, let's just send them back to the starting entrance
                entrance_to_place.toExit().link_to_start(no_logic=no_logic)
        ex.link(entrance_to_place, reversible=reversible, no_logic=no_logic)

        self.build_dungeon_paths(dun, entrance_to_place.region)

    def build_dead_end_paths(self, de, region) -> None:
        """
        Docstring for build_dead_end_paths
        
        :param self: Description
        """
        if region == de:
            return
        
        self.find_reachable_region_exits(self.world.origin_region_name)
        ex = self.world.random.choice(list(self.reachable_exits))
        entrance_to_place = self.find_entrance_pairing(ex, dungeons=True, dead_ends=True, banned=set([ogex.toEntrance() for ogex in self.reachable_exits]))
        print(f"{ex} ---> {entrance_to_place}")
        reversible = ex.reversible and entrance_to_place.reversible
        if not reversible:
            if ex.reversible:
                # In this case, exit is reversible but entrance is not
                # Since this entrance will be inaccessible, lets remove it
                self.regions[ex.region]["entrances"].remove(SSEntrance(ex.region, ex.name, world=self.world))
            if entrance_to_place.reversible:
                # In this case, entrance is reversible but exit is not
                # Since the entrance can be traveled back through but we have no where to send
                # the player, let's just send them back to the starting entrance
                entrance_to_place.toExit().link_to_start()
        ex.link(entrance_to_place, reversible=reversible)

        self.build_dead_end_paths(de, entrance_to_place.region)

    def finalize_entrance_placements(self, dead_ends: bool = False, new_regions_only: bool = False) -> None:
        """
        Docstring for finalize_entrance_placements
        
        :param self: Description
        :param dead_ends: Description
        :type dead_ends: bool
        """
        self.find_reachable_region_exits(self.world.origin_region_name)
        currently_reachable_exits = [ex for ex in self.reachable_exits]
        if len(self.reachable_exits) == 0:
            return
        
        if len(self.reachable_exits) == 2 and any([not ex.reversible for ex in self.reachable_exits]):
            # This is a special case
            ex = [ex for ex in self.reachable_exits if not ex.reversible].pop()
        else:
            ex = self.world.random.choice(currently_reachable_exits)
        entrance_to_place = self.find_entrance_pairing(ex, dungeons=dead_ends, dead_ends=dead_ends)
        while not entrance_to_place:
            new_ex = self.world.random.choice([r_ex for r_ex in currently_reachable_exits if r_ex != ex])
            entrance_to_place = self.find_entrance_pairing(new_ex, dungeons=dead_ends, dead_ends=dead_ends)
        print(f"{ex} ---> {entrance_to_place}")
        reversible = ex.reversible and entrance_to_place.reversible
        if not reversible:
            if ex.reversible:
                # In this case, exit is reversible but entrance is not
                # Since this entrance will be inaccessible, lets remove it
                self.regions[ex.region]["entrances"].remove(SSEntrance(ex.region, ex.name, world=self.world))
            if entrance_to_place.reversible:
                # In this case, entrance is reversible but exit is not
                # Since the entrance can be traveled back through but we have no where to send
                # the player, let's just send them back to the starting entrance
                entrance_to_place.toExit().link_to_start()
        ex.link(entrance_to_place, reversible=reversible)

        
        self.finalize_entrance_placements(dead_ends=dead_ends, new_regions_only=new_regions_only)

    def find_reachable_region_exits(self, region) -> None:
        """
        Find all reachable exits starting in a given region that have not yet been placed.
        
        :param self: The SSWorld EntranceRando class.
        :param region: The starting region name.
        """

        region_exits = [SSExit(region, ex, world=self.world) for ex in ALL_REQUIREMENTS[region]["exits"].keys()]
        for ex in region_exits:
            self.init_follow_exit_chain(ex)
            self.reachable_exits |= self.scanned_placeable_exits
            for reg in self.scanned_reachable_regions:
                self.regions[reg]["accessed"] = True

        self.reachable_exits -= set(self.entrance_mapping.exits)

        # Couple edge cases to account for
        if self.regions["Faron Woods - Outside Top of Great Tree"]["accessed"] == False and self.world.options.open_lake_floria != "open":
            # Unless open, make sure yerbal is reachable prior to lake floria exit access
            ex = SSExit("Faron Woods - In the Woods", "Jump into Lake")
            if ex in self.reachable_exits:
                self.reachable_exits.remove(ex)

        if SSEntrance("Faron Woods - In the Woods", "Shortcut to Floria Waterfall") not in self.entrance_mapping.entrances:
            # Cannot place this as an exit unless it can be accessed as an entrance
            ex = SSExit("Faron Woods - In the Woods", "Shortcut to Floria Waterfall")
            if ex in self.reachable_exits:
                self.reachable_exits.remove(ex)

        if self.world.options.open_lmf == "nodes":
            if self.regions["Lanayru Desert - Fire Node"]["accessed"] == False or self.regions["Lanayru Desert - Lightning Node"]["accessed"] == False:
                # Unless open/main node Make sure both nodes are accessed before lanayru dungeon exit access
                ex = SSExit("Lanayru Desert - North Desert", "Dungeon Entrance in Lanayru Desert")
                if ex in self.reachable_exits:
                    self.reachable_exits.remove(ex)

        if self.regions["Lanayru Sand Sea - Pirate Stronghold - Inside"]["accessed"] == False:
            # Require access to inside of PS prior to placing under jaw exit
            ex = SSExit("Lanayru Sand Sea - Pirate Stronghold - Under Jaw", "Door under Jaw")
            if ex in self.reachable_exits:
                self.reachable_exits.remove(ex)

    def find_entrance_pairing(self, ex: SSExit, dungeons: list | bool = False, dead_ends: bool = False, banned: set | None = None) -> SSEntrance | None:
        """
        Find valid entrance pairings for a given shuffled exit.

        :param self: The SSWorld EntranceRando class.
        :param ex: The SSExit object that is being shuffled.
        :param dungeons: Determines which dungeons, if any, are allowed to be selected as a valid entrance.
                         Give a list of valid dungeons, or True for all dungeons / False for no dungeons.
        :param dead_ends: Bool which determines if dead ends can be placed at this point.
        :param banned: A set of entrances that cannot be selected, or None if any entrances can be picked.
        """
        placeable_entrances = set()
        all_entrances = []
        for reg, data in self.regions.items():
            all_entrances.extend([ent for ent in data["entrances"]])
            placeable_entrances.update(set([ent for ent in data["entrances"] if ent != ex.toEntrance()]))

        #print([str(ent) for ent in all_entrances])

        if banned:
            if len(placeable_entrances - banned) > 0:
                placeable_entrances -= banned

        # Couple edge cases to account for
        if SSExit("Thunderhead - Isle of Songs - Outside", "Crawlspace after Bridge Puzzle") not in self.entrance_mapping.exits:
            # Make sure the exit is placed first, otherwise the bridge won't be done
            ent = SSEntrance("Thunderhead - Isle of Songs - Outside", "Crawlspace after Bridge Puzzle")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if self.regions["Sealed Grounds - Spiral"]["accessed"] == False:
            # Cannot access statue area from temple door, so require access before placing as entrance
            ent = SSEntrance("Sealed Grounds - Spiral", "Sealed Temple")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if SSEntrance("Volcano Summit - Before First Frog", "Path across from First Frog") not in self.entrance_mapping.entrances:
            # Since this part of summit is not traversable backwards
            ent = SSEntrance("Volcano Summit - After Second Frog", "Dungeon Entrance in Volcano Summit")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if self.regions["Eldin Volcano - Hot Cave"]["accessed"] == False:
            # Cannot call Fi, so require access to prevent softlocks
            ent = SSEntrance("Eldin Volcano - Hot Cave", "Upper Path out of Hot Cave")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if self.regions["Lanayru Mine - Ending"]["accessed"] == False:
            # Assume non-traversable backwards until accessed due to bomb rock
            ent = SSEntrance("Lanayru Mine - Ending", "Minecart Ride out of Mine")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if self.regions["Lanayru Sand Sea - Shipyard - Outside"]["accessed"] == False:
            # Not traversable backwards
            ent = SSEntrance("Lanayru Sand Sea - Shipyard - Past Roller Coaster", "Door")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if SSEntrance("Lanayru Sand Sea - Shipyard - Construction Bay", "Upper Door") not in self.entrance_mapping.entrances:
            # Make sure the upper entrance to construction bay is placed before the lower
            ent = SSEntrance("Lanayru Sand Sea - Shipyard - Construction Bay", "Lower Door")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if self.regions["Lanayru Sand Sea - Pirate Stronghold - Inside"]["accessed"] == False:
            # Require access to inside of PS prior to placing under jaw entrance
            ent = SSEntrance("Lanayru Sand Sea - Pirate Stronghold - Under Jaw", "Door under Jaw")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        if (
            SSEntrance("Lanayru Caves - Caves", "North Exit") not in self.entrance_mapping.entrances
            and SSEntrance("Lanayru Caves - Caves", "East Exit") not in self.entrance_mapping.entrances
            and SSEntrance("Lanayru Caves - Past Crawlspace", "Path away from Crawlspace") not in self.entrance_mapping.entrances
            and (self.world.options.lanayru_caves_small_key == "caves" or self.world.options.lanayru_caves_small_key == "lanayru")
        ):
            # If caves key is in cave, make sure behind locked door is not placed first
            ent = SSEntrance("Lanayru Caves - Past Locked Door", "Path away from Door")
            if ent in placeable_entrances:
                placeable_entrances.remove(ent)

        #print([str(ent) for ent in placeable_entrances])

        if len(placeable_entrances) == 0:
            if len(all_entrances) < 2:
                raise Exception("Tried to pick an entrance but less than 2 exist")
            return None

        if dead_ends:
            return self.world.random.choice(list(placeable_entrances))

        # In this case, we cannot yet place any dead ends
        placeable_entrances_non_dead_end = []
        for ent in placeable_entrances:
            if dungeons == True:
                if ent.region in DUNGEON_INITIAL_REGIONS.values():
                    placeable_entrances_non_dead_end.append(ent)
                    continue
            elif isinstance(dungeons, list):
                if ent.region in dungeons:
                    placeable_entrances_non_dead_end.append(ent)
                    continue
                elif ent.region in DUNGEON_INITIAL_REGIONS.values():
                    continue
            else:
                if ent.region in DUNGEON_INITIAL_REGIONS.values():
                    continue
            region_exits =  [ex for ex in ALL_REQUIREMENTS[ent.region]["exits"].keys() if ex != ent.name]
            if len(region_exits) == 0:
                continue
            
            temp = False
            for ex in region_exits:
                if self.init_follow_exit_chain(SSExit(ent.region, ex, world=self.world)):
                    temp = True
                    break
                else:
                    continue
            
            if temp:
                placeable_entrances_non_dead_end.append(ent)

        return self.world.random.choice(placeable_entrances_non_dead_end)
    

    def init_follow_exit_chain(self, ex: SSExit) -> bool:
        """
        Initializes the follow_exit_chain method. See the docstring for the follow_exit_chain
        method for more info.

        :param self: The SSWorld EntranceRando class.
        :param ex: The starting exit, as an SSExit object.
        """
        self.scanned_placeable_exits.clear()
        self.scanned_reachable_regions.clear()
        self.scanned_exits.clear()

        return self.follow_exit_chain(ex)
                

    def follow_exit_chain(self, chain_ex: SSExit) -> bool:
        """
        To run an exit chain, please use method self.init_follow_exit_chain().

        Follows the current exit chain from a given starting SSExit object.
        Begins by checking if the given exit is not yet placed. If not, return true.
        Otherwise, find the connected entrance and check exits from that point. If it is a dead end, return False.
        If not a dead end, go through all exits from that entrance and call this function recursively.

        Ensure that before calling this function first, set self.scanned_placeable_exits to an empty set or clear it.
        Ensure that before calling this function first, set self.scanned_exits to an empty set or clear it.
        By calling init_follow_exit_chain(), these sets will automatically be cleared.
        All unplaced exits that are found will be added to self.scanned_placeable_exits.
        
        :param self: The SSWorld EntranceRando class
        :param chain_ex: SSExit object of the current chain exit
        :return: Returns true at the end of the chain if there are available exits to place.
        Otherwise, returns false at the end of the chain.
        """
        self.scanned_exits.add(chain_ex)
        self.scanned_reachable_regions.add(chain_ex.region)
        if chain_ex not in self.entrance_mapping.exits:
            # If not placed, then return true
            self.scanned_placeable_exits.add(chain_ex)
            return True
        
        ent = None
        for mapex, mapent, x in self.entrance_mapping.mapping:
            # Find the entrance where this exit maps to
            if chain_ex == mapex:
                ent = mapent
                break
        if not ent:
            raise Exception(f"Exit chain failed at exit {chain_ex.region} ({chain_ex.name})")
        
        # Find the exits out of the new region, but not the entrance we came through
        chain_region_exits = [crex for crex in ALL_REQUIREMENTS[ent.region]["exits"].keys() if crex != ent.name]
        if len(chain_region_exits) == 0:
            # If no further exits, then entrance leads to a dead end, return false
            self.scanned_reachable_regions.add(ent.region)
            return False

        # Now, continue the exit chain for the exits in this new region
        if any([self.follow_exit_chain(SSExit(ent.region, crex, world=self.world)) for crex in deepcopy(chain_region_exits) if SSExit(ent.region, crex, world=self.world) not in self.scanned_exits]):
            # In this case, the chain found placeable exits, so return true
            return True
        else:
            # In this case, the chain did find any more placeable exits, so return false
            return False

    def randomize_dungeon_entrances_only(self) -> None:
        """
        Randomize dungeon entrances based on the player's options.
        """

        duns_to_place = deepcopy(self.dungeons)
        randomized_dungeon_entrances = deepcopy(self.dungeon_entrances)

        if self.world.options.randomize_entrances == "required_dungeons_only":
            for dun in self.world.dungeons.banned_dungeons:
                self.dungeon_connections[dun] = VANILLA_DUNGEON_CONNECTIONS[dun]
                duns_to_place.remove(dun)
                randomized_dungeon_entrances.remove(VANILLA_DUNGEON_CONNECTIONS[dun])

            if not self.world.dungeons.sky_keep_required:
                self.dungeon_connections["Sky Keep"] = VANILLA_DUNGEON_CONNECTIONS["Sky Keep"]
                duns_to_place.remove("Sky Keep")
                randomized_dungeon_entrances.remove(VANILLA_DUNGEON_CONNECTIONS["Sky Keep"])

        self.world.random.shuffle(randomized_dungeon_entrances)
        self.dungeon_connections.update(dict(zip(duns_to_place, randomized_dungeon_entrances)))

        req_duns = [dun for dun, reg in DUNGEON_INITIAL_REGIONS.items() if dun in self.world.dungeons.required_dungeons]
        req_dun_regions = [reg for dun, reg in DUNGEON_INITIAL_REGIONS.items() if dun in self.world.dungeons.required_dungeons]
        non_req_duns = [dun for dun, reg in DUNGEON_INITIAL_REGIONS.items() if dun not in self.world.dungeons.required_dungeons and dun != "Sky Keep"]
        non_req_dun_regions = [reg for dun, reg in DUNGEON_INITIAL_REGIONS.items() if dun not in self.world.dungeons.required_dungeons and dun != "Sky Keep"]
        if self.world.dungeons.sky_keep_required:
            req_duns.append("Sky Keep")
            req_dun_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])
        else:
            non_req_duns.append("Sky Keep")
            non_req_dun_regions.append(DUNGEON_INITIAL_REGIONS["Sky Keep"])

        for dun, ent in self.dungeon_connections.items():
            dun_region = DUNGEON_INITIAL_REGIONS[dun]
            ent_region = DUNGEON_ENTRANCE_REGIONS[ent]
            if self.world.options.empty_unrequired_dungeons and dun in non_req_duns:
                no_logic = True
            else:
                no_logic = False
            SSExit(dun_region, "Dungeon Exit", world=self.world).link(SSEntrance(ent_region, ent, world=self.world), reversible=True, no_logic=no_logic)

        for dun in req_dun_regions:
            dun_name = [name for name, reg in DUNGEON_INITIAL_REGIONS.items() if reg == dun].pop()
            ent = [en for ex, en, x in self.entrance_mapping.mapping if ex == SSExit(dun, "Dungeon Exit")].pop()
            for ex in self.dungeon_exits_to_place[dun_name]:
                SSExit(ex.region, ex.name, world=self.world).link(ent, reversible=False, plando=True)
        
        for dun in non_req_dun_regions:
            dun_name = [name for name, reg in DUNGEON_INITIAL_REGIONS.items() if reg == dun].pop()
            ent = [en for ex, en, x in self.entrance_mapping.mapping if ex == SSExit(dun, "Dungeon Exit")].pop()
            for ex in self.dungeon_exits_to_place[dun_name]:
                if self.world.options.empty_unrequired_dungeons:
                    SSExit(ex.region, ex.name, world=self.world).link(ent, reversible=False, plando=True, no_logic=True)
                else:
                    SSExit(ex.region, ex.name, world=self.world).link(ent, reversible=False, plando=True)


    def randomize_trial_gates(self) -> None:
        """
        Randomize the trials connected to each trial gate based on the player's options.
        """

        if self.world.options.randomize_trials:
            randomized_trial_gates = deepcopy(self.trial_gates)
            self.world.random.shuffle(randomized_trial_gates)
            self.trial_connections = dict(zip(self.trials, randomized_trial_gates))
        else:
            for trl in self.trials:
                self.trial_connections[trl] = VANILLA_TRIAL_CONNECTIONS[trl]

        for trl, gate in self.trial_connections.items():
            gate_region = TRIAL_GATE_REGIONS[gate]
            SSExit(trl, "Trial Gate", world=self.world).link(SSEntrance(gate_region, "Entrance from Trial", world=self.world), reversible=False, plando=True)
            SSExit(gate_region, gate, world=self.world).link(SSEntrance(trl, "Trial Gate Entrance", world=self.world), reversible=False, plando=True)

    def randomize_starting_statues(self) -> None:
        """
        Randomize the starting statues for each province based on the player's options.
        """

        possible_starting_statues = {}
        if self.world.options.random_start_statues:
            for prov in ["Faron Province", "Eldin Province", "Lanayru Province"]:
                possible_starting_statues[prov] = [
                    ent for ent in GAME_ENTRANCE_TABLE
                    if ent.type == "Statue"
                    and ent.statue_name != "Inside the Volcano"
                    and ent.province == prov
                ]
            if self.world.options.lanayru_caves_small_key == "caves":
                # Account for this edge case where caves key is in caves
                # We must block sand sea from being the starting region
                possible_starting_statues["Lanayru Province"] = [
                    ent for ent in possible_starting_statues["Lanayru Province"]
                    if ent.flag_space != "Lanayru Sand Sea"
                ]
        else:
            for prov in ["Faron Province", "Eldin Province", "Lanayru Province"]:
                possible_starting_statues[prov] = [
                    ent for ent in GAME_ENTRANCE_TABLE
                    if ent.type == "Statue"
                    and ent.vanilla_statue
                    and ent.province == prov
                ]

        for prov, statues in possible_starting_statues.items():
            statue = self.world.random.choice(statues)
            self.starting_statues[prov] = (
                statue.name,
                {
                    "type": "entrance",
                    "subtype": "bird-statue-entrance",
                    "province": statue.province,
                    "statue-name": statue.statue_name,
                    "stage": statue.stage,
                    "room": statue.room,
                    "layer": statue.layer,
                    "entrance": statue.entrance,
                    "tod": statue.tod,
                    "flag-space": statue.flag_space,
                    "flag": statue.flag,
                    "vanilla-start-statue": statue.vanilla_statue,
                    "hint_region": ALL_REQUIREMENTS[statue.apregion]["hint_region"],
                    "apregion": statue.apregion,
                },
            )

    def randomize_starting_entrance(self) -> None:
        """
        Randomize the starting spawn based on the player's options.
        """
        ser = self.world.options.random_start_entrance
        #limit_ser = self.world.options.limit_start_entrance

        if ser == "vanilla":
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE if ent.type == "Vanilla"]
        elif ser == "bird_statues":
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE if ent.type == "Statue" or ent.type == "Vanilla"]
        elif ser == "any_surface_region":
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE if ent.province != "The Sky" or ent.type == "Vanilla"]
        else:
            possible_starting_entrances = [ent for ent in GAME_ENTRANCE_TABLE]
        
        starting_entrance = self.world.random.choice(possible_starting_entrances)

        self.starting_entrance = {
            "statue-name": starting_entrance.statue_name if starting_entrance.statue_name is not None else starting_entrance.name,
            "stage": starting_entrance.stage,
            "room": starting_entrance.room,
            "layer": starting_entrance.layer,
            "entrance": starting_entrance.entrance,
            "day-night": starting_entrance.tod,
            "apregion": starting_entrance.apregion,
        }
    
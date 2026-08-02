from collections import deque
import logging
from typing import Any, Callable, Optional

from BaseClasses import CollectionState
from .ALttPDoorRandomizer.BaseClasses import CrystalBarrier, Door, Entrance, Location, World as DoorRandoWorld


dungeon_portals = {
    "Hyrule Castle": ["Hyrule Castle South Portal", "Hyrule Castle West Portal", "Hyrule Castle East Portal", "Sanctuary Portal", "Sewer Drop"],
    "Eastern Palace": ["Eastern Portal"],
    "Desert Palace": ["Desert South Portal", "Desert East Portal", "Desert West Portal", "Desert Back Portal"],
    "Tower of Hera": ["Hera Portal"],
    "Agahnims Tower": ["Agahnims Tower Portal"],
    "Palace of Darkness": ["Palace of Darkness Portal"],
    "Swamp Palace": ["Swamp Portal"],
    "Skull Woods": ["Skull 1 Portal", "Skull 2 West Portal", "Skull 2 East Portal", "Skull 3 Portal", "Skull Pinball",
                    "Skull Pot Circle", "Skull Left Drop", "Skull Back Drop"],
    "Thieves Town": ["Thieves Town Portal"],
    "Ice Palace": ["Ice Portal"],
    "Misery Mire": ["Mire Portal"],
    "Turtle Rock": ["Turtle Rock Main Portal", "Turtle Rock Lazy Eyes Portal", "Turtle Rock Chest Portal", "Turtle Rock Eye Bridge Portal"],
    "Ganons Tower": ["Ganons Tower Portal"],
}


logger = logging.getLogger("alttpr")

class StateAdapter:
    ###############################################
    # Wraps Archipelago's CollectionState to provide DoorRandomizer-compatible state methods.
    #
    # This allows DoorRandomizer access_rule functions to work without modification by intercepting
    # calls to methods that don't exist on CollectionState, and translating them to equivalent
    # Archipelago item checks. In other words, we get to reuse the DR lambda's that define logical
    # access to different regions and locations, by passing in StateAdapter instead of AP's CollectionState.
    ###############################################
    _checked_crystal_regions = set()
    @property
    def checked_crystal_regions(self):
        return type(self)._checked_crystal_regions


    def __init__(self, state: CollectionState, world: DoorRandoWorld, player: int, crystal_paths):
        self.crystal_paths = crystal_paths
        self.state = state
        self.placing_items = None  # Used inside Door Randomizer
        self.player = player
        self.world = world


    def __getattr__(self, name: str) -> Any:
        # Forward attribute access to the wrapped state if the attribute exists there.
        # This allows direct access to standard CollectionState methods/properties.
        return getattr(self.state, name)

    # NOTE: Every method takes an argument "player", which Door Randomizer uses for
    # multiworld logic. We ignore the argument and use AP's player value to check AP's state.

    # Core generic item checking methods
    def can_reach(self, location, location_type: Optional[str]=None, player=None) -> bool:
        name = location if isinstance(location, str) else location.name

        if isinstance(location, Door) or isinstance(location, Entrance):
            location_type = "Entrance"
        elif isinstance(location, Location):
            location_type = "Location"

        return self.state.can_reach(name, location_type, self.player)


    def has(self, item: str, player: int, count: int = 1) -> bool:
        if item.endswith("Sword"):
            sword_count = {"Fighter Sword": 1, "Master Sword": 2, "Tempered Sword": 3, "Golden Sword": 4, "Progressive Sword": count}
            item = "Progressive Sword"
            count = sword_count[item]
        elif item == "Bow":
            item = "Progressive Bow"
        elif item == "Silver Arrows":
            item = "Progressive Bow"
            count = 2
        elif item == "Cape":
            # TODO: I don't know why I thought changing the name of "Cape" was a good idea, I should undo that
            item = "Magic Cape"

        return self.state.has(item, self.player, count)


    def has_item(self, item: str, count: int = 1) -> bool:
        # A wrapper for has() that doesn't require the useless player argument
        return self.has(item, self.player, count)


    def item_count(self, item: str, player):
        return self.count(item, self.player)


    # More specific item checking methods
    def bottle_count(self, player) -> int:
        return self.count_group("Bottles", self.player)


    def can_avoid_lasers(self, player) -> bool:
        return self.has_item("Progressive Shield", 3) or self.has_item("Cane of Byrna") or self.has_item("Magic Cape")


    def can_buy_unlimited(self, item, player):
        for shop in self.world.shops[1]:
            if shop.has_unlimited(item) and self.can_reach(shop.region.name):
                return True
        return False


    def can_collect_bonkdrops(self, player):
        return self.has_Boots(player) or (self.has_sword(player) and self.has_item('Quake'))


    def can_extend_magic(self, player, smallmagic=16, fullrefill=False) -> bool:
        # Check if the player has enough magic. smallmagic is the total amount needed,
        # with a full magic meter being 8 magic.
        # TODO: Check for hard/expert mode
        basemagic = 8 if not self.has_item("Magic Upgrade (1/2)") else 16
        if self.can_buy_unlimited('Green Potion', player) or self.can_buy_unlimited('Blue Potion', player):
            basemagic = basemagic + basemagic * self.bottle_count(player)
        return smallmagic <= basemagic


    def can_farm_rupees(self, player):
        # Bushes can always drop a green rupee at the bare minimum.
        # OWR has the event item "Farmable Rupees" for access to less awful farming locations, such as
        # bush crabs or a tree pull, but that would be a pain to implement correctly for an incredibly
        # niche situation.
        # (entrance shuffle with no rupee farming locations, no rupees from tree pulls/bush crabs, enemy shuffle with no killable
        # enemies dropping rupees, item on Zora)
        return True


    def can_farm_bombs(self, player):
        # Both the light and dark worlds have at least one bush that can drop bombs.
        # South of dig spot or near bombable hut for LW, and next to brewery for DW.
        # OWR has the event item "Farmable Bombs" for access to less awful farming locations, such as
        # bush crabs or a tree pull, but that would be a pain to implement correctly.
        # Might be required for overworld shuffle??
        return True


    def can_flute(self, player) -> bool:
        if self.world.mode[1] == 'standard' and not self.has_item('Zelda Delivered'):
            return False  # can't flute in rain state
        return self.has_item("Ocarina (Activated)")


    def can_hit_crystal(self, player) -> bool:
        return (self.can_use_bombs(self.player)
                or self.can_shoot_arrows(self.player)
                or self.has_blunt_weapon(self.player)
                or self.has('Blue Boomerang', self.player)
                or self.has('Red Boomerang', self.player)
                or self.has('Hookshot', self.player)
                or self.has('Fire Rod', self.player)
                or self.has('Ice Rod', self.player)
                or self.has('Cane of Somaria', self.player)
                or self.has('Cane of Byrna', self.player))


    def can_hit_crystal_through_barrier(self, player) -> bool:
        return (self.can_use_bombs(self.player)
                or self.can_shoot_arrows(self.player)
                or self.has('Blue Boomerang', self.player)
                or self.has('Red Boomerang', self.player)
                or self.has('Fire Rod', self.player)
                or self.has('Ice Rod', self.player)
                or self.has('Cane of Somaria', self.player))


    def can_kill_most_things(self, player, enemies=5) -> bool:
        return (self.has_blunt_weapon(self.player)
                or self.has_item('Cane of Somaria')
                or (self.has_item('Cane of Byrna') and (enemies < 6 or self.can_extend_magic(player)))
                or self.can_shoot_arrows(self.player)
                or self.has_item('Fire Rod')
                )


    def can_lift_heavy_rocks(self, player) -> bool:
        return self.has_item('Progressive Glove', 2)


    def can_lift_rocks(self, player) -> bool:
        return self.has_item('Progressive Glove', 1)


    def can_melt_things(self, player) -> bool:
        return self.has_item('Fire Rod') or self.has_item('Bombos')


    def can_reach_blue(self, region, player) -> bool:
        if self.world.doorShuffle[1] == "vanilla":
            # This will be the simple version for non-door rando. In general, if you can reach
            # blue blocks you can also reach a crystal switch.
            # TODO: Bomb bag also breaks this assumption for back of Mire
            extra_condition = True
            if region.name.startswith("Swamp "):
                extra_condition = self.has_item("Small Key (Swamp Palace)", 6)
            elif region.name in ["Ice Backwards Room", "Ice Crystal Left", "Ice Crystal Right"]:
                extra_condition = self.has_item("Small Key (Ice Palace)", 6)
            elif region.name.startswith("Mire") and region.name != "Mire Crystal Mid":  # If not in the back of Mire
                extra_condition = self.has_item("Small Key (Misery Mire)", 3)

            return self.can_hit_crystal(player) and extra_condition
        else:
            if self.alttpr_stale_crystal_regions[self.player]:
                self.update_reachable_crystal_regions()
            return region.name in self.state.alttpr_reachable_crystal_regions[self.player] and self.state.alttpr_reachable_crystal_regions[self.player][region.name] in [CrystalBarrier.Blue, CrystalBarrier.Either]


    def can_reach_orange(self, region, player) -> bool:
        if self.world.doorShuffle[1] == "vanilla":
            return True
        else:
            if self.alttpr_stale_crystal_regions[self.player]:
                self.update_reachable_crystal_regions()
            return region.name in self.state.alttpr_reachable_crystal_regions[self.player] and self.state.alttpr_reachable_crystal_regions[self.player][region.name] in [CrystalBarrier.Orange, CrystalBarrier.Either]


    def can_shoot_arrows(self, player) -> bool:
        # TODO: Retro
        return self.has('Progressive Bow', player) or self.has("Bow", player)


    def can_stun_enemies(self, player) -> bool:
        return self.has_item("Blue Boomerang") or self.has_item("Red Boomerang") or self.has_item("Hookshot")


    def can_take_damage(self) -> bool:
        # TODO: Needed for OHKO mode
        return True


    def can_use_bombs(self, player) -> bool:
        # TODO: Bomb bag
        return True


    def everything(self, player, all_except=0) -> bool:
        locations = self.state.multiworld.get_locations(self.player)
        return len([location for location in locations if not location.is_event and not location.can_reach(self.state)]) - all_except <= 0


    def has_beam_sword(self, player) -> bool:
        return self.has_item("Progressive Sword", 2)


    def has_beaten_aga(self, player) -> bool:
        return self.has_item("Beat Agahnim 1") and (self.world.mode[1] != "standard" or self.has_item("Zelda Delivered"))


    def has_blunt_weapon(self, player) -> bool:
        return self.has_item("Hammer") or self.has_item("Progressive Sword")


    def has_bottle(self, player) -> bool:
        return self.state.has_group("Bottles", self.player)


    def has_Boots(self, player) -> bool:
        return self.has_item('Pegasus Boots')


    def has_crystals(self, count: int, player) -> bool:
        # TODO: Make the crystals a group of event items
        num_crystals = 0
        for i in range(1, 8):
            if self.has_item(f'Crystal {i}'):
                num_crystals += 1
        return num_crystals >= count


    def has_fire_source(self, player) -> bool:
        return self.has_item('Fire Rod') or self.has_item('Lamp')


    def has_hearts(self, player, count: int) -> bool:
        # TODO: I really don't want to make a heart container a progression item.
        # Might make the sanc heart container progression later, not sure.
        return False


    def has_Mirror(self, player) -> bool:
        return self.has_item('Magic Mirror')


    def has_misery_mire_medallion(self, player) -> bool:
        return self.has_item(self.world.required_medallions[player][0])


    def has_Pearl(self, player) -> bool:
        return self.has_item('Moon Pearl')


    def has_sm_key(self, small_key_name, player, number=1):
        return self.has_item(small_key_name, number)


    def has_sword(self, player) -> bool:
        return self.has_item("Progressive Sword")


    def has_turtle_rock_medallion(self, player) -> bool:
        return self.has_item(self.world.required_medallions[player][1])


    def is_door_open(self, door_name: str, player) -> bool:
        # Force the key logic to be handled
        return False


    def is_not_bunny(self, region, player) -> bool:
        if self.has_item('Moon Pearl'):
            return True
        return not region.can_cause_bunny(1) # Overwriting this function to also track what crystal state (orange/blue blocks down) each region can be reached in.


    ########################################
    # Support methods
    ########################################
    def update_reachable_crystal_regions(self):
        # Mostly copy/pasted from CollectionState, but with some added code to track what the crystal state
        # (orange/blue blocks) is when a region can be reached
        self.state.alttpr_stale_crystal_regions[self.player] = False
        world = self.multiworld.worlds[self.player]
        blocked_crystal_connections = self.state.alttpr_blocked_crystal_connections[self.player]
        reachable_crystal_regions = self.state.alttpr_reachable_crystal_regions[self.player]
        queue = deque([(connector, reachable_crystal_regions[connector.parent_region.name]) for connector in blocked_crystal_connections])

        # init on first call - this can't be done on construction since the regions don't exist yet
        for portals in dungeon_portals.values():
            for portal in portals:
                if portal not in reachable_crystal_regions:
                    reachable_crystal_regions[portal] = CrystalBarrier.Orange
                    exits = world.get_region(portal).exits
                    blocked_crystal_connections.extend(exits)
                    queue.extend([(exit, CrystalBarrier.Orange) for exit in exits])

        # run BFS on all connections, and keep track of those blocked by missing items
        while queue:
            connection, crystal_color = queue.popleft()
            new_region = connection.connected_region
            if not new_region.is_in_dungeon or (new_region.name in reachable_crystal_regions and
                                                (reachable_crystal_regions[new_region.name] == CrystalBarrier.Either or
                                                 reachable_crystal_regions[new_region.name] == crystal_color)):
                blocked_crystal_connections.remove(connection)
                continue

            if connection.crystal in [CrystalBarrier.Blue, CrystalBarrier.Orange]:
                # This connection is across orange or blue blocks
                can_access = crystal_color == CrystalBarrier.Either or crystal_color == connection.crystal
                crystal_color = connection.crystal
            else:
                can_access = connection.access_rule(self.state)

            if can_access:
                if self.allow_partial_entrances and not new_region:
                    continue
                assert new_region, f"tried to search through an Entrance \"{connection}\" with no connected Region"
                if new_region.has_crystal_switch or (new_region.name in reachable_crystal_regions and reachable_crystal_regions[new_region.name] != crystal_color):
                    crystal_color = CrystalBarrier.Either
                reachable_crystal_regions[new_region.name] = crystal_color
                blocked_crystal_connections.remove(connection)
                blocked_crystal_connections.extend(new_region.exits)

                for exit in new_region.exits:
                    if new_region.is_in_dungeon:
                        if new_region.has_crystal_switch:
                            queue.append((exit, CrystalBarrier.Either))
                        elif connection.crystal:
                            queue.append((exit, connection.crystal))
                        else:
                            queue.append((exit, crystal_color))
                    else:
                        queue.append((exit, CrystalBarrier.Orange))


def adapt_door_rando_rule(rule_func: Callable[[StateAdapter], bool], world: DoorRandoWorld, player: int, crystal_paths) -> Callable[[CollectionState], bool]:
    # Convert a DoorRandomizer rule function to work with Archipelago's CollectionState.
    def adapted_rule(state: CollectionState) -> bool:
        try:
            return rule_func(StateAdapter(state, world, player, crystal_paths))
        except Exception as e:
            logger.warning(f"Error evaluating adapted DoorRandomizer rule for player {player}: {e}")
            raise e

    return adapted_rule

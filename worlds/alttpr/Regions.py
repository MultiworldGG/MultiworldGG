from __future__ import annotations

import logging
from typing import Callable, TYPE_CHECKING

from BaseClasses import Entrance, Location, Region

from .ALttPDoorRandomizer.BaseClasses import CrystalBarrier, PotItem, PotFlags, RegionType
from .ALttPDoorRandomizer.source.dungeon import EnemyList
from .ALttPDoorRandomizer import PotShuffle
from .ALttPDoorRandomizer import Regions as DoorRandomizerRegions
from .ALttPDoorRandomizer.source.rom import DataTables
from .RomAddresses import location_table_pot_items, location_table_sprite_items
from .StateAdapter import adapt_door_rando_rule

if TYPE_CHECKING:
    from .World import ALttPRWorld


location_name_to_id = {}
lookup_id_to_name = {}
lookup_name_to_id = {}
logger = logging.getLogger("alttpr")


class ALttPRRegion(Region):
    game = "The Legend of Zelda: A Link to the Past"
    has_crystal_switch = False
    is_in_dungeon = False
    type = RegionType.Menu

    def get_connecting_entrances(self, checked_regions: list[str]) -> Entrance:
        if self.name in checked_regions:
            return []

        checked_regions.append(self.name)
        outdoor_entrances = []
        for entrance in self.entrances:
            if entrance.parent_region.type == RegionType.LightWorld or entrance.parent_region.type == RegionType.DarkWorld:
                outdoor_entrances.append(entrance.name)
            else:
                outdoor_entrances.extend(entrance.parent_region.get_connecting_entrances(checked_regions))

        return outdoor_entrances


class ALttPRLocation(Location):
    game = "The Legend of Zelda: A Link to the Past"


class ALttPREntrance(Entrance):
    game = "The Legend of Zelda: A Link to the Past"
    blocked = False
    crystal = CrystalBarrier.Null


class ALttPRCrystalPath:
    def __init__(self, color: CrystalBarrier, crystal_switch_region: ALttPRRegion, path: list[ALttPREntrance]):
        self.color = color
        self.crystal_switch_region = crystal_switch_region.name  # The name of a region with a crystal switch
        self.path = [entrance.name for entrance in path]  # The path of entrances leading from the crystal switch to a particular region
        # NOTE: Names of regions/entrances are used instead of the Region/Entrance objects because Regions have a
        # reference to the multiworld, which gets manually cleaned up after generation, causing a memory leak


    def similar_path(self, other) -> bool:
        if not isinstance(other, ALttPRCrystalPath):
            return False

        return self.crystal_switch_region == other.crystal_switch_region and \
               self.color == other.color and \
               (set(self.path).issubset(other.path) or set(other.path).issubset(self.path))


    def issubset(self, other) -> bool:
        if not isinstance(other, ALttPRCrystalPath) or not self.similar_path(other):
            return False

        return set(self.path).issubset(set(other.path))


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


def create_and_connect_regions(world: ALttPRWorld) -> None:
    # First define every region, then loop through a second time to connect them.
    # Otherwise we're trying to connect to regions that don't exist yet.
    ap_regions = {}
    crystal_switches = {dungeon: [] for dungeon in world.door_rando_world.dungeons}
    event_locations = get_event_locations(world)

    for region in world.door_rando_world.regions:
        ap_region = ALttPRRegion(region.name, world.player, world.multiworld)
        ap_region.type = region.type
        ap_region.is_in_dungeon = region.type == RegionType.Dungeon
        if region.crystal_switch:
            ap_region.has_crystal_switch = region.crystal_switch
            crystal_switches[region.dungeon].append(ap_region)

        for location in region.locations:
            # Skip all locations that aren't randomized with the user's options
            if ("Shop - " in location.name or "Upgrade - " in location.name) and not world.options.shopsanity:
                continue
            elif " Item " in location.name:
                # TODO: Retro
                continue
            elif location.item and "Farmable" in location.item.name:
                # These are in logic to see if the player can farm rupees or bombs.
                # TODO: Overworld shuffle
                continue
            else:
                # The dungeon prize locations aren't in lookup_name_to_id (not sure how they're removed?),
                # so they won't have an ID, which is how an event location is defined.
                id = lookup_name_to_id.get(location.name, None)
                if not id and \
                   " - Prize" not in location.name and \
                   location.name not in event_locations:
                    raise Exception(f"Found unknown location {location.name} in region {region.name}.")

                if world.is_excluded_key_drop_location(location) or location.name in event_locations:
                    id = None

                ap_location = ALttPRLocation(
                    world.player, location.name, id, ap_region
                )
                ap_location.access_rule = adapt_door_rando_rule(location.access_rule, world.door_rando_world, world.player, world.crystal_paths)
                ap_region.locations.append(ap_location)

        ap_regions[region.name] = ap_region

    # Now make all the connections
    for region in world.door_rando_world.regions:
        ap_region = ap_regions[region.name]
        for exit in region.exits:
            if exit.connected_region is None:
                continue

            # Need to check for always impassible doors, other door logic like keys is handled in access_rule
            blocked = False if not exit.door else exit.door.blocked

            ap_entrance = ALttPREntrance(world.player, exit.name, parent=ap_region)
            ap_entrance.access_rule = adapt_door_rando_rule(exit.access_rule if not blocked else lambda state: False, world.door_rando_world, world.player, world.crystal_paths)
            if exit.door:
                ap_entrance.blocked = blocked
                ap_entrance.crystal = exit.door.crystal
            ap_region.exits.append(ap_entrance)
            ap_entrance.connect(ap_regions[exit.connected_region.name])

    world.multiworld.regions += list(ap_regions.values())
    handle_ice_cross(world)
    handle_big_bomb_logic(world)


def handle_ice_cross(world: ALttPRWorld) -> None:
    # The "Ice Cross" room in Ice Palace, north of Pengator room, is a confusing pain logic-wise with door rando.
    # Let's just make our own entrances to help AP find the right path...
    def make_ice_cross_entrance(entrance_name: str, parent_region: ALttPRRegion, exit: ALttPREntrance):
        new_entrance = ALttPREntrance(world.player, entrance_name, parent=parent_region)
        new_entrance.access_rule = exit.access_rule
        new_entrance.blocked = exit.blocked
        new_entrance.crystal = exit.crystal
        parent_region.exits.append(new_entrance)
        new_entrance.connect(exit.connected_region)

    ice_cross_left_region = world.get_region("Ice Cross Left")
    ice_cross_right_region = world.get_region("Ice Cross Right")
    ice_cross_top_region = world.get_region("Ice Cross Top")
    ice_cross_bottom_region = world.get_region("Ice Cross Bottom")
    ice_cross_left_exit = world.get_entrance("Ice Cross Left WS")
    ice_cross_right_exit = world.get_entrance("Ice Cross Right ES")
    ice_cross_top_exit = world.get_entrance("Ice Cross Top NE")
    ice_cross_bottom_exit = world.get_entrance("Ice Cross Bottom SE")

    make_ice_cross_entrance("Ice Cross Left to Bottom", ice_cross_left_region, ice_cross_bottom_exit)
    make_ice_cross_entrance("Ice Cross Bottom to Left", ice_cross_bottom_region, ice_cross_left_exit)
    make_ice_cross_entrance("Ice Cross Bottom to Right", ice_cross_bottom_region, ice_cross_right_exit)
    make_ice_cross_entrance("Ice Cross Right to Bottom", ice_cross_right_region, ice_cross_bottom_exit)
    make_ice_cross_entrance("Ice Cross Right to Top", ice_cross_right_region, ice_cross_top_exit)
    make_ice_cross_entrance("Ice Cross Top to Left", ice_cross_top_region, ice_cross_left_exit)
    make_ice_cross_entrance("Ice Cross Top to Right", ice_cross_top_region, ice_cross_right_exit)


def handle_big_bomb_logic(world: ALttPRWorld) -> None:
    # TODO: Everything about this code is awful, it desperately needs a rewrite, and I haven't even finished writing it <_< (but also this is taking too long as is)
    # Picking up the Big Bomb already requires reaching the bomb shop and having the red crystals
    bomb_shop_entrance = world.get_region("Big Bomb Shop").entrances[-1].name
    pyramid_crack = world.get_location("Pyramid Crack")

    crossed_entrances = world.options.entrance_shuffle == "crossed"
    flute_shuffle = world.options.flute_shuffle != "vanilla"
    inverted = world.options.world_mode == "inverted"

    district = [district for district in world.door_rando_world.districts[1].values() if bomb_shop_entrance in district.entrances][0]
    flute_spots = world.door_rando_world.owflutespots[1]
    player = world.player
    pyramid_crack_rule = None

    if not crossed_entrances and not inverted:
        pyramid_crack_rule = lambda state: (state.has("Hammer", player) and state.has("Moon Pearl", player)) or \
                                                  (state.has("Magic Mirror", player) and state.has("Beat Agahnim 1", player))
    elif not crossed_entrances and inverted:
        flute_spots = world.door_rando_world.owflutespots
        if not flute_shuffle or [True for flute_spot in [0x1b, 0x1e, 0x25, 0x2e, 0x2f] if flute_spot in flute_spots]:
            # To deliver the big bomb without the Hammer or Flute, you need Light World access + Mirror to reach the Pyramid with the bomb
            pyramid_crack_rule = lambda state: state.has("Hammer", player) or \
                                                      state.has("Ocarina (Activated)", player) or \
                                                      (state.has("Magic Mirror", player) and state.has("Progressive Glove", player, 2) and state.has("Moon Pearl", player))
        elif [True for flute_spot in [0x15, 0x16] if flute_spot in flute_spots]:  # Flute to dark potion shop but not east dark world
            pyramid_crack_rule = lambda state: state.has("Hammer", player) or \
                                                      (state.has("Ocarina (Activated)", player) and state.has("Progressive Glove", player)) or \
                                                      (state.has("Magic Mirror", player) and state.has("Progressive Glove", player, 2) and state.has("Moon Pearl", player))
        elif [True for flute_spot in [0x0f, 0x17] if flute_spot in flute_spots]:  # Flute to Catfish but not east dark world
            pyramid_crack_rule = lambda state: state.has("Hammer", player) or \
                                                      (state.has("Ocarina (Activated)", player) and state.has("Progressive Glove", player)) or \
                                                      (state.has("Magic Mirror", player) and state.has("Progressive Glove", player, 2) and state.has("Moon Pearl", player))
        else:  # Cannot Flute to anywhere in east dark world
            pyramid_crack_rule = lambda state: state.has("Hammer", player) or \
                                               (state.has("Magic Mirror", player) and state.has("Progressive Glove", player, 2) and state.has("Moon Pearl", player))
    elif crossed_entrances and not inverted:
        # NOTE: King's Tomb is special because you could Mirror without Mitts, you need Mitts or Flute to deliver it
        if bomb_shop_entrance in ["Desert Palace Entrance (South)", "Desert Palace Entrance (West)",
                                  "Desert Palace Entrance (East)", "Desert Palace Entrance (North)"]:
            # Differs based on whether you got here using connector to Mire + Mirror, or a direct connector
            world.multiworld.register_indirect_condition(world.get_region("Mire Area"), world.get_entrance(bomb_shop_entrance))
            pyramid_crack_rule = lambda state: (
                state.has("Ocarina (Activated)", player) or (state.has("Magic Mirror", player) and state.can_reach_region("Mire Area", player))
            ) and (state.has("Beat Agahnim 1", player) or (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player)))
        elif bomb_shop_entrance == "Kings Grave":
            # Whether you reach it with Mitts or DW + Mirror, you have a way to be in the general Light World.
            # You could leave a Mirror Portal at HC, but that hard requires Mitts.
            pyramid_crack_rule = lambda state: state.has("Beat Agahnim 1", player) or \
               (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player)) or \
               (state.has("Magic Mirror", player) and state.has("Progressive Glove", player, 2))
        elif bomb_shop_entrance == "Dark Potion Shop":
            pyramid_crack_rule = lambda state: (state.has("Moon Pearl", player) and (state.has("Progressive Glove", player) or state.has("Hammer", player))) or \
               (state.has("Magic Mirror", player) and state.has("Beat Agahnim 1", player))
        elif bomb_shop_entrance in ["Hyrule Castle Entrance (West)", "Hyrule Castle Entrance (East)", "Agahnims Tower"]:
            # Can Mirror from Pyramid or Flute to a Dark World portal
            pyramid_crack_rule = lambda state: state.has("Magic Mirror", player) or \
                (state.has("Ocarina (Activated)", player) and
                 (state.has("Beat Agahnim 1", player) or
                 (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player))
                )
            )
        elif bomb_shop_entrance == "Capacity Upgrade":
            # A Mirror portal at Pyramid can be used, but only with Flippers, otherwise you have to Flute away
            # TODO: Overworld glitches
            pyramid_crack_rule = lambda state: (state.has("Magic Mirror", player) and state.has("Flippers", player)) or \
               (state.has("Ocarina (Activated)", player) and
                (state.has("Beat Agahnim 1", player) or
                (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player))
                )
               )
        elif district.name == "The Mire" or bomb_shop_entrance in ["Checkerboard Cave", "Red Shield Shop", "Dark Lake Hylia Ledge Fairy",
                                                                   "Dark Lake Hylia Ledge Spike Cave", "Dark Lake Hylia Ledge Hint",
                                                                   "Skull Woods Final Section", "Skull Woods Second Section Door (West)"]:
            # Mirror is hard required, but you can walk through LW to another DW portal
            pyramid_crack_rule = lambda state: state.has("Magic Mirror", player) and \
                (state.has("Beat Agahnim 1", player) or (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player)))
        elif district.name == "Dark Death Mountain" or bomb_shop_entrance in ["Ice Palace", "Bumper Cave (Top)"]:
            pyramid_crack_rule = lambda state: state.has("Magic Mirror", player) and state.has("Ocarina (Activated)", player) and \
                                                      (state.has("Beat Agahnim 1", player) or
                                                      (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player)))
        elif district.name == "South Dark World" or bomb_shop_entrance in ["Cave 45", "Two Brothers (West)"]:
            pyramid_crack_rule = lambda state: state.has("Hammer", player) or state.has("Magic Mirror", player) and state.has("Beat Agahnim 1", player)
        elif district.name == "Northwest Dark World" or bomb_shop_entrance == "Graveyard Cave":
            # You can walk there with Mitts + Hammer + Mearl, or Mirror to Light World and get back into the Dark World near Pyramid
            pyramid_crack_rule = lambda state: (
                    (state.has("Magic Mirror", player) and
                     (state.has("Beat Agahnim 1", player) or
                      (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has(
                          "Moon Pearl", player)))
                     ) or (state.has("Progressive Glove", player, 2) and state.has("Hammer", player) and state.has(
                "Moon Pearl", player)))
        elif district.name in ["Eastern Hyrule", "Lake Hylia", "Central Hyrule", "Desert", "Kakariko", "Northwest Hyrule"]:
            # Only Mirror is needed because if we're checking the Pyramid Crack, then you can get to Pyramid, leave a
            # mirror portal outside Hyrule Castle, then walk there with the Big Bomb from most of Light World.
            pyramid_crack_rule = lambda state: state.has("Beat Agahnim 1", player) or \
                state.has("Magic Mirror", player) or \
                (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player))
        elif district.name == "Death Mountain" or bomb_shop_entrance == "Death Mountain Return Cave (West)":
            # Must Flute away, extra requirements or Mirror shenanigans are possible depending on the exact entrance and Flute spots
            # TODO: For my own sanity, it is out of logic to both use a Mirror Portal near Hyrule Castle and take a
            # connector to the Bomb Shop. Otherwise you get nonsense like leaving a Mirror, then using a connector to go
            # through Turtle Rock to reach the Bomb Shop, but only if the connector doesn't touch the Dark World or
            # require a Save and Quit. Please, no.

            # Optional rule for leaving a Mirror portal at HC and Fluting to DM.
            # Assume we already have the Flute because it's always needed for DM
            mirror_and_flute_rule = lambda state: False
            if 0x03 in flute_spots:  # Vanilla Flute spot for DM
                if bomb_shop_entrance in ["Old Man Cave (East)", "Old Man House (Bottom)", "Old Man House (Top)",
                                          "Death Mountain Return Cave (East)", "Spectacle Rock Cave",
                                          "Spectacle Rock Cave Peak", "Spectacle Rock Cave (Bottom)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player)
                elif bomb_shop_entrance in ["Spiral Cave (Bottom)", "Hookshot Fairy", "Paradox Cave (Bottom)", "Paradox Cave (Middle)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player) and state.has("Hookshot", player)
                elif bomb_shop_entrance in ["Fairy Ascension Cave (Bottom)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player) and state.has("Hookshot", player) and state.has("Progressive Glove", player, 2)
            elif 0x05 in flute_spots:  # Flute to southeast DM
                if bomb_shop_entrance in ["Spiral Cave (Bottom)", "Hookshot Fairy", "Paradox Cave (Bottom)", "Paradox Cave (Middle)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player)
                elif bomb_shop_entrance in ["Old Man Cave (East)", "Old Man House (Bottom)", "Old Man House (Top)",
                                          "Death Mountain Return Cave (East)", "Spectacle Rock Cave",
                                          "Spectacle Rock Cave Peak", "Spectacle Rock Cave (Bottom)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player) and state.has("Hookshot", player)
                elif bomb_shop_entrance in ["Fairy Ascension Cave (Bottom)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player) and state.has("Progressive Glove", player, 2)
            elif 0x07 in flute_spots:  # Flute to top-right of DM
                if bomb_shop_entrance in ["Spiral Cave (Bottom)", "Hookshot Fairy", "Paradox Cave (Bottom)", "Paradox Cave (Middle)",
                                          "Paradox Cave (Top)", "Spiral Cave", "Fairy Ascension Cave (Top)", "Fairy Ascension Cave (Bottom)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player)
                elif bomb_shop_entrance in ["Old Man Cave (East)", "Old Man House (Bottom)", "Old Man House (Top)",
                                            "Death Mountain Return Cave (East)", "Spectacle Rock Cave",
                                            "Spectacle Rock Cave Peak", "Spectacle Rock Cave (Bottom)"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player) and (state.has("Hookshot", player) or state.has("Hammer", player))
                elif bomb_shop_entrance in ["Tower of Hera"]:
                    mirror_and_flute_rule = lambda state: state.has("Magic Mirror", player) and state.has("Hammer", player, 2)

            pyramid_crack_rule = lambda state: state.has("Ocarina (Activated)", player) and \
              (state.has("Beat Agahnim 1", player) or
              (state.has("Progressive Glove", player) and state.has("Hammer", player) and state.has("Moon Pearl", player))) or \
              mirror_and_flute_rule(state)
        elif district.name == "East Dark World":
            pyramid_crack_rule = lambda state: True
        else:
            pyramid_crack_rule = lambda state: True

    elif crossed_entrances and inverted:
        can_reach_from_north_dark_world = lambda state: state.has("Progressive Glove", player, 2) and state.has("Hammer", player)

        # Create a rule for using the Flute to reach the Pyramid, based on Flute Shuffle results
        can_reach_with_flute = None
        if world.options.flute_shuffle == "vanilla" or any([True for flute_spot in flute_spots if flute_spot in [0x1b, 0x1e, 0x25, 0x2e, 0x2f]]):
            can_reach_with_flute = lambda state: state.has("Ocarina (Activated)", player)
        elif 0x15 in flute_spots or 0x16 in flute_spots:  # Can't Flute to the East but can Flute near Dark Potion Shop
            can_reach_with_flute = lambda state: state.has("Ocarina (Activated)", player) and (state.has("Progressive Glove", player) or state.has("Hammer", player))
        else:
            can_use_glove = False
            can_use_hammer = False
            if 0x0f in flute_spots or 0x17 in flute_spots:
                # Only Flute spots in the East are near Catfish
                can_use_glove = True
            if any([True for flute_spot in flute_spots if flute_spot in [0x28, 0x2a, 0x2b, 0x2c, 0x2d, 0x32, 0x33, 0x34, 0x3a, 0x3b, 0x3c]]):
                # Can Flute to South Dark World
                can_use_hammer = True

            if can_use_glove and can_use_hammer:
                can_reach_with_flute = lambda state: state.has("Ocarina (Activated)", player) and (state.has("Progressive Glove", player) or state.has("Hammer", player))
            elif can_use_glove and not can_use_hammer:
                can_reach_with_flute = lambda state: state.has("Ocarina (Activated)", player) and state.has("Progressive Glove", player)
            elif not can_use_glove and can_use_hammer:
                can_reach_with_flute = lambda state: state.has("Ocarina (Activated)", player) and state.has("Hammer", player)
            else:
                # The only usable Flute spots are in northwest Dark World
                can_reach_with_flute = lambda state: state.has("Ocarina (Activated)", player) and can_reach_from_north_dark_world(state)

        must_flute_entrances = ["Ice Palace", "Bumper Cave (Top)"]
        must_flute_or_mirror_entrances = ["Dark Lake Hylia Ledge Fairy", "Dark Lake Hylia Ledge Hint", "Dark Lake Hylia Ledge Spike Cave",
                                     "Skull Woods Final Section", "Skull Woods Second Section Door (West)", "Red Shield Shop"]
        must_flute_and_mirror_entrances = ["Desert Palace Entrance (South)", "Desert Palace Entrance (East)", "Desert Palace Entrance (West)",
                                           "Desert Palace Entrance (North)", "Death Mountain Return Cave (West)", "Capacity Upgrade", "Waterfall of Wishing"]

        if bomb_shop_entrance == "Dark Potion Shop":
            pyramid_crack_rule = lambda state: state.has("Progressive Glove", player) or state.has("Hammer", player) or can_reach_with_flute(state)
        elif bomb_shop_entrance in must_flute_or_mirror_entrances or district.name == "The Mire":
            # Can Flute or do Mirror shenanigans from almost anywhere in the Light World
            world.multiworld.register_indirect_condition(world.get_region("Kakariko Village"), world.get_entrance("Pyramid Crack"))
            pyramid_crack_rule = lambda state: can_reach_with_flute(state) or (state.can_reach_region("Kakariko Village", player) and state.has("Magic Mirror", player))
        elif bomb_shop_entrance in must_flute_entrances or district.name == "Dark Death Mountain":
            pyramid_crack_rule = can_reach_with_flute
        elif bomb_shop_entrance in must_flute_and_mirror_entrances or district.name == "Death Mountain":
            pyramid_crack_rule = lambda state: state.has("Magic Mirror", player) and can_reach_with_flute(state)
        elif district.name == "East Dark World":
            pyramid_crack_rule = lambda state: True
        elif district.name == "South Dark World":
            pyramid_crack_rule = lambda state: state.has("Hammer", player) or can_reach_with_flute(state)
        elif district.name == "Northwest Dark World":
            pyramid_crack_rule = lambda state: can_reach_from_north_dark_world(state) or can_reach_with_flute(state)
        elif district.name in ["Northwest Hyrule", "Kakariko", "Central Hyrule", "Eastern Hyrule", "Lake Hylia", "Desert"]:
            pyramid_crack_rule = lambda state: state.has("Magic Mirror", player)
        # TODO: Overworld glitches, what if bomb shop at brothers west

    pyramid_crack.access_rule = lambda state: state.has("Pick Up Big Bomb", player) and pyramid_crack_rule(state)


def get_event_locations(world: ALttPRWorld):
    # TODO: I feel like most of these aren't needed until door randomizer is added, and some of them still seem unnecessary (e.g. Skull Star Tile).
    # It's fine if it doesn't affect anything for players, but if it shows up in the player log or Poptracker than that could be an annoyance.
    # TODO: Maybe get these directly from OWR?
    event_locations = {
        "Ganon": "Triforce",
        "Agahnim 1": "Beat Agahnim 1",
        "Agahnim 2": "Beat Agahnim 2",
        "Lost Old Man": "Escort Old Man",
        "Old Man Drop Off": "Return Old Man",
        "Locksmith": "Sign Vandalized",
        "Kiki": "Pick Up Kiki",
        "Kiki Assistance": "Dark Palace Opened",
        "Frog": "Get Frog",
        "Missing Smith": "Return Smith",
        "Dark Blacksmith Ruins": "Pick Up Purple Chest",
        "Middle Aged Man": "Deliver Purple Chest",
        "Big Bomb": "Pick Up Big Bomb",
        "Pyramid Crack": "Detonate Big Bomb",
        "Floodgate": "Open Floodgate",
        "Trench 1 Switch": "Trench 1 Filled",
        "Trench 2 Switch": "Trench 2 Filled",
        "Swamp Drain": "Drained Swamp",
        "Attic Cracked Floor": "Shining Light",
        "Suspicious Maiden": "Maiden Rescued",
        "Revealing Light": "Maiden Unmasked",
        "Ice Block Drop": "Convenient Block",
        "Skull Star Tile": "Hidden Pits",
        "Turtle Medallion Pad": "Turtle Opened",
        'Eastern Palace - Boss Kill': 'Beat Boss',
        "Desert Palace - Boss Kill": "Beat Boss",
        "Tower of Hera - Boss Kill": "Beat Boss",
        "Palace of Darkness - Boss Kill": "Beat Boss",
        "Swamp Palace - Boss Kill": "Beat Boss",
        "Skull Woods - Boss Kill": "Beat Boss",
        "Thieves\' Town - Boss Kill": "Beat Boss",
        "Ice Palace - Boss Kill": "Beat Boss",
        "Misery Mire - Boss Kill": "Beat Boss",
        "Turtle Rock - Boss Kill": "Beat Boss",
        "Zelda Pickup": "Zelda Herself",
        "Zelda Drop Off": "Zelda Delivered",
        # Some events are only created in certain modes
        # "Master Sword Pedestal": "Triforce",
        # "Murahdahla": "Triforce",
        # "Flute Activation": "Ocarina (Activated)",
    }

    goal = world.options.goal
    if goal == "triforcehunt":
        event_locations["Ganon"] = "Nothing"
    if goal == "triforcehunt" or goal == "trinity":
        event_locations["Murahdahla"] = "Triforce"
    if goal == "pedestal" or goal == "trinity":
        event_locations["Master Sword Pedestal"] = "Triforce"
    if world.options.world_mode.current_key != "inverted" and not world.options.pre_activated_flute.value:
        event_locations["Flute Activation"] = "Ocarina (Activated)"

    return event_locations



# Add info on all locations to lookup_id_to_name and lookup_name_to_id.
# This is used by the client to send items we pick up.
def init_lookups():
    global lookup_id_to_name
    global lookup_name_to_id

    lookup_id_to_name = {x: y for x, y in DoorRandomizerRegions.lookup_id_to_name.items()}
    lookup_name_to_id = {x: y for x, y in DoorRandomizerRegions.lookup_name_to_id.items()}

    for event in DoorRandomizerRegions.location_events:
        lookup_name_to_id[event] = None

    for super_tile, pot_list in PotShuffle.vanilla_pots.items():
        for pot_index, pot in enumerate(pot_list):
            if pot.item != PotItem.Hole:
                if pot.item == PotItem.Key:
                    loc_name = next(loc for loc, datum in PotShuffle.key_drop_data.items()
                                    if datum[1] == super_tile)
                else:
                    descriptor = 'Large Block' if pot.flags & PotFlags.Block else f'Pot #{pot_index+1}'
                    loc_name = f'{pot.room} {descriptor}'
                location_table_pot_items[loc_name] = (2 * super_tile, 0x8000 >> pot_index)
                location_id = DoorRandomizerRegions.pot_address(pot_index, super_tile)
                lookup_name_to_id[loc_name] = location_id
                lookup_id_to_name[location_id] = loc_name
    uw_table = DataTables.get_uw_enemy_table()
    key_drop_data = {(v[1][1], v[1][2]): k for k, v in PotShuffle.key_drop_data.items() if v[0] == 'Drop'}
    for super_tile, enemy_list in uw_table.room_map.items():
        index_adj = 0
        for index, sprite in enumerate(enemy_list):
            if sprite.sub_type == 0x07:  # overlord
                index_adj += 1
                continue
            if (super_tile, index) in key_drop_data:
                loc_name = key_drop_data[(super_tile, index)]
                location_id = PotShuffle.key_drop_data[loc_name][1][0]
            else:
                loc_name = f'{sprite.region} Enemy #{index+1}'
                location_id = EnemyList.drop_address(index, super_tile)
            # if index < index_adj:
            #     logging.info(f'Problem at {hex(super_tile)} {loc_name}')
            location_table_sprite_items[loc_name] = (2 * super_tile, 0x8000 >> (index-index_adj))
            lookup_name_to_id[loc_name] = location_id
            lookup_id_to_name[location_id] = loc_name

init_lookups()
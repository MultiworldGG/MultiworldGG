"""
Helper functions to deliver entrance/exit/region sets to OWG rules.
"""

from .BaseClasses import Entrance, Region
from .OWEdges import OWTileRegions

# Cave regions that superbunny can get through - but only with a sword.
sword_required_superbunny_mirror_regions = ["Spiral Cave (Top)"]

# Cave regions that superbunny can get through - but only with boots.
boots_required_superbunny_mirror_regions = ["Two Brothers House"]

# Cave locations that superbunny can access - but only with boots.
boots_required_superbunny_mirror_locations = [
    "Sahasrahla's Hut - Left",
    "Sahasrahla's Hut - Middle",
    "Sahasrahla's Hut - Right",
]

# Entrances that can't be superbunny-mirrored into.
invalid_mirror_bunny_entrances = [
    "Hype Cave",
    "Bonk Fairy (Dark)",
    "Thieves Town",
    "Hammer Peg Cave",
    "Brewery",
    "Hookshot Cave",
    "Dark Lake Hylia Ledge Fairy",
    "Dark Lake Hylia Ledge Spike Cave",
    "Palace of Darkness",
    "Misery Mire",
    "Turtle Rock",
    "Bonk Rock Cave",
    "Bonk Fairy (Light)",
    "50 Rupee Cave",
    "20 Rupee Cave",
    "Checkerboard Cave",
    "Light Hype Fairy",
    "Waterfall of Wishing",
    "Light World Bomb Hut",
    "Mini Moldorm Cave",
    "Ice Rod Cave",
    "Sanctuary Grave",
    "Kings Grave",
    "Sanctuary Grave",
    "Hyrule Castle Secret Entrance Drop",
    "Skull Woods Second Section Hole",
    "Skull Woods First Section Hole (North)",
]

# Interior locations that can be accessed with superbunny state.
superbunny_accessible_locations = [
    "Waterfall of Wishing - Left",
    "Waterfall of Wishing - Right",
    "King's Tomb",
    "Floodgate",
    "Floodgate Chest",
    "Cave 45",
    "Bonk Rock Cave",
    "Brewery",
    "C-Shaped House",
    "Chest Game",
    "Mire Shed - Left",
    "Mire Shed - Right",
    "Secret Passage",
    "Ice Rod Cave",
    "Pyramid Fairy - Left",
    "Pyramid Fairy - Right",
    "Superbunny Cave - Top",
    "Superbunny Cave - Bottom",
    "Blind's Hideout - Left",
    "Blind's Hideout - Right",
    "Blind's Hideout - Far Left",
    "Blind's Hideout - Far Right",
    "Kakariko Well - Left",
    "Kakariko Well - Middle",
    "Kakariko Well - Right",
    "Kakariko Well - Bottom",
    "Kakariko Tavern",
    "Library",
    "Spiral Cave",
] + boots_required_superbunny_mirror_locations

    # TODO: Add pottery locations


def get_non_mandatory_exits(world, player):
    """
    Entrances that can be reached with full equipment using overworld glitches and don't need to be an exit.
    The following are still be mandatory exits:

    Open:
    Turtle Rock Isolated Ledge Entrance
    Skull Woods Second Section Door (West) (or Skull Woods Final Section)

    Inverted:
    Two Brothers House (West)
    Desert Palace Entrance (East)
    """

    yield 'Bumper Cave (Top)'
    yield 'Death Mountain Return Cave (West)'
    yield 'Hookshot Cave Back Entrance'

    if world.is_tile_swapped(0x30, player):
        yield 'Desert Palace Entrance (North)'
        yield 'Desert Palace Entrance (West)'
    else:
        yield 'Desert Palace Entrance (East)'

    if world.is_tile_swapped(0x1b, player):
        yield 'Agahnims Tower'
        yield 'Hyrule Castle Entrance (West)'
        yield 'Hyrule Castle Entrance (East)'

    if not world.is_tile_swapped(0x05, player):
        yield 'Dark Death Mountain Ledge (West)'
        yield 'Dark Death Mountain Ledge (East)'
        #yield 'Mimic Cave' #TODO: This was here, I don't think this is true


def get_boots_clip_exits_lw(world, player):
    """
    Special Light World region exits that require boots clips.
    """

    for name, parent_region, target_region in boots_clips_local:
        if world.is_tile_lw_like(OWTileRegions[parent_region], player):
            yield(name, parent_region, target_region)

    for names, parent_regions, target_regions in boots_clips:
        region_pair = get_world_pair(world, player, get_region_pairs(world, player, names, parent_regions, target_regions), True)
        if region_pair and region_pair[2]:
            assert region_pair[0], f'Exit name missing in OWG pairing from {region_pair[1]} to {region_pair[2]}'
            yield(region_pair[0], region_pair[1], region_pair[2])


def get_boots_clip_exits_dw(world, player):
    """
    Special Dark World region exits that require boots clips.
    """

    for name, parent_region, target_region in boots_clips_local:
        if not world.is_tile_lw_like(OWTileRegions[parent_region], player):
            yield(name, parent_region, target_region)

    for names, parent_regions, target_regions in boots_clips:
        region_pair = get_world_pair(world, player, get_region_pairs(world, player, names, parent_regions, target_regions), False)
        if region_pair and region_pair[2]:
            assert region_pair[0], f'Exit name missing in OWG pairing from {region_pair[1]} to {region_pair[2]}'
            yield(region_pair[0], region_pair[1], region_pair[2])


def get_glitched_speed_drops_lw(world, player):
    """
    Light World drop-down ledges that require glitched speed.
    """

def get_glitched_speed_drops_dw(world, player):
    """
    Dark World drop-down ledges that require glitched speed.
    """


def get_mirror_clip_spots(world, player):
    """
    Out of bounds transitions using the mirror
    """

    for name, parent_region, target_region in mirror_clips_local:
        if not world.is_tile_lw_like(OWTileRegions[parent_region], player):
            yield(name, parent_region, target_region)

    for names, parent_regions, target_regions in mirror_clips:
        region_pair = get_world_pair(world, player, get_region_pairs(world, player, names, parent_regions, target_regions), False)
        if region_pair and region_pair[2] and not world.is_tile_lw_like(OWTileRegions[region_pair[1]], player):
            assert region_pair[0], f'Exit name missing in OWG pairing from {region_pair[1]} to {region_pair[2]}'
            yield(region_pair[0], region_pair[1], region_pair[2])


def get_mirror_offset_spots(world, player):
    """
    Mirror shenanigans placing a mirror portal with a broken camera
    """

    # TODO: These really should check to see if there is a mirrorless path to the mirror portal
    # but being that OWG is very very open, it's very unlikely there isn't a path, but possible
    for names, parent_regions, target_regions, path_to in mirror_offsets:
        region_pair = get_world_pair(world, player, get_region_pairs(world, player, names, parent_regions, target_regions, path_to), False)
        if region_pair and region_pair[2] and not world.is_tile_lw_like(OWTileRegions[region_pair[1]], player):
            assert region_pair[0], f'Exit name missing in OWG pairing from {region_pair[1]} to {region_pair[2]}'
            yield(region_pair[0], region_pair[1], region_pair[2], region_pair[3])


def get_swapped_status(world, player, parents, targets):
    if parents[0]:
        parent_swapped = world.is_tile_swapped(OWTileRegions[parents[0]], player)
    else:
        parent_swapped = world.is_tile_swapped(OWTileRegions[parents[1]], player)
    
    if targets[0] and targets[0] in (glitch_regions[0] + glitch_regions[1]):
        target_swapped = targets[0] in glitch_regions[1]
    else:
        if targets[0]:
            target_swapped = world.is_tile_swapped(OWTileRegions[targets[0]], player)
        else:
            target_swapped = world.is_tile_swapped(OWTileRegions[targets[1]], player)

    return parent_swapped, target_swapped


def get_region_pairs(world, player, names, parent_regions, target_regions, path_regions=None):
    # this pairs the source region to the proper destination
    region_pairs = [None, None]
    parent_swapped, target_swapped = get_swapped_status(world, player, parent_regions, target_regions)
    if parent_regions[0]:
        region_pairs[0] = [names[0], parent_regions[0]]
        if parent_swapped == target_swapped:
            region_pairs[0].append(target_regions[0])
            if path_regions:
                region_pairs[0].append(path_regions[0])
        else:
            region_pairs[0].append(target_regions[1])
            if path_regions:
                region_pairs[0].append(path_regions[1])
    if parent_regions[1]:
        region_pairs[1] = [names[1], parent_regions[1]]
        if parent_swapped == target_swapped:
            region_pairs[1].append(target_regions[1])
            if path_regions:
                region_pairs[1].append(path_regions[1])
        else:
            region_pairs[1].append(target_regions[0])
            if path_regions:
                region_pairs[1].append(path_regions[0])
    return region_pairs


def get_world_pair(world, player, region_pairs, get_light_world):
    # this chooses the region pair that is in the right world
    if region_pairs[0]:
        is_lw = world.is_tile_lw_like(OWTileRegions[region_pairs[0][1]], player)
    else:
        is_lw = not world.is_tile_lw_like(OWTileRegions[region_pairs[1][1]], player)
    
    if is_lw == get_light_world:
        return region_pairs[0]
    else:
        return region_pairs[1]


def create_owg_connections(world, player):
    """
    Add OWG transitions to player's world without logic
    """
    create_no_logic_connections(player, world, get_boots_clip_exits_lw(world, player))
    create_no_logic_connections(player, world, get_boots_clip_exits_dw(world, player))

    # Glitched speed drops.
    #create_no_logic_connections(player, world, get_glitched_speed_drops_lw(world, player))
    #create_no_logic_connections(player, world, get_glitched_speed_drops_dw(world, player))

    # Mirror clip spots.
    create_no_logic_connections(player, world, get_mirror_clip_spots(world, player))
    
    # Mirror offset spots.
    for data in get_mirror_offset_spots(world, player):
        create_no_logic_connections(player, world, [data[0:3]])


def overworld_glitches_rules(world, player):
    # Boots-accessible locations.
    set_owg_rules(player, world, get_boots_clip_exits_lw(world, player), lambda state: state.can_boots_clip_lw(player))
    set_owg_rules(player, world, get_boots_clip_exits_dw(world, player), lambda state: state.can_boots_clip_dw(player))

    # Glitched speed drops.
    #set_owg_rules(player, world, get_glitched_speed_drops_lw(world, player), lambda state: state.can_get_glitched_speed_lw(player))
    #set_owg_rules(player, world, get_glitched_speed_drops_dw(world, player), lambda state: state.can_get_glitched_speed_dw(player))

    # Mirror clip spots.
    # TODO: Should this also require can_boots_clip
    set_owg_rules(player, world, get_mirror_clip_spots(world, player), lambda state: state.has_Mirror(player))

    # Mirror offset spots.
    for data in get_mirror_offset_spots(world, player):
        set_owg_rules(player, world, [data[0:3]], lambda state: state.has_Mirror(player) and state.can_boots_clip_lw(player) and state.can_reach(data[3], None, player))

    # Regions that require the boots and some other stuff.
    # TODO: Revisit below when we can guarantee water walk
    # if world.mode[player] != 'inverted':
    #     add_alternate_rule(world.get_entrance('Waterfall of Wishing Cave Entry', player), lambda state: state.has_Pearl(player) or state.has_Boots(player))
    # else:
    #     add_alternate_rule(world.get_entrance('Waterfall of Wishing Cave Entry', player), lambda state: state.has_Pearl(player))

    # Zora's Ledge via waterwalk setup.
    #add_alternate_rule(world.get_location('Zora\'s Ledge', player), lambda state: state.has_Boots(player)) #revisit when we can guarantee water walk

    # Adding additional item requirements to OWG Clips
    if world.is_tile_swapped(0x18, player) != world.is_tile_swapped(0x28, player):
        add_additional_rule(world.get_entrance('Kakariko To Dig Game Hook Clip', player), lambda state: state.has('Hookshot', player))
    else:
        add_additional_rule(world.get_entrance('VoO To Dig Game Hook Clip', player), lambda state: state.has('Hookshot', player))
    add_additional_rule(world.get_entrance('Tree Line Water Clip', player), lambda state: state.has('Flippers', player))
    add_additional_rule(world.get_entrance('Dark Tree Line Water Clip', player), lambda state: state.has('Flippers', player))

    # Bunny pocket
    if not world.is_tile_swapped(0x00, player):
        add_alternate_rule(world.get_entrance("Skull Woods Final Section", player), lambda state: state.can_bunny_pocket(player) and state.has("Fire Rod", player))
    if world.is_tile_swapped(0x05, player):
        add_alternate_rule(world.get_entrance("DM Hammer Bridge (West)", player), lambda state: state.can_bunny_pocket(player) and state.has("Hammer", player))
        add_alternate_rule(world.get_entrance("DM Hammer Bridge (East)", player), lambda state: state.can_bunny_pocket(player) and state.has("Hammer", player))
    if not world.is_tile_swapped(0x18, player):
        add_alternate_rule(world.get_entrance("Bush Yard Pegs (Inner)", player), lambda state: state.can_bunny_pocket(player) and state.has("Hammer", player))
        add_alternate_rule(world.get_entrance("Bush Yard Pegs (Outer)", player), lambda state: state.can_bunny_pocket(player) and state.has("Hammer", player))
    if world.is_tile_swapped(0x22, player):
        add_alternate_rule(world.get_entrance("Blacksmith Ledge Peg (West)", player), lambda state: state.can_bunny_pocket(player) and state.has("Hammer", player))


def add_alternate_rule(entrance, rule):
    old_rule = entrance.access_rule
    entrance.access_rule = lambda state: old_rule(state) or rule(state)


def add_additional_rule(entrance, rule):
    old_rule = entrance.access_rule
    entrance.access_rule = lambda state: old_rule(state) and rule(state)


def create_no_logic_connections(player, world, connections, connect_external=False):
    for entrance, parent_region, target_region, *_ in connections:
        parent = world.get_region(parent_region, player)

        if isinstance(target_region, Region):
            target_region = target_region.name
            
        if connect_external and target_region.endswith(" Portal"):
            target = world.get_portal(target_region[:-7], player).find_portal_entrance().parent_region
        else:
            target = world.get_region(target_region, player)

        connection = Entrance(player, entrance, parent)
        connection.spot_type = 'OWG'
        parent.exits.append(connection)
        connection.connect(target)


def set_owg_rules(player, world, connections, default_rule):
    for entrance, _, _, *rule_override in connections:
        connection = world.get_entrance(entrance, player)
        rule = rule_override[0] if len(rule_override) > 0 else default_rule
        connection.access_rule = rule


glitch_regions = (['Central Cliffs', 'Eastern Cliff', 'Desert Northern Cliffs'],
                  ['Dark Central Cliffs', 'Darkness Cliff', 'Mire Northern Cliffs'])

# same screen clips, no Tile Flip OWR implications
boots_clips_local = [ # (name, from_region, to_region)
    ('Hera Ascent Clip', 'West Death Mountain (Bottom)', 'West Death Mountain (Top)'), #cannot guarantee camera correction, but a bomb clip exists
    ('WDDM Bomb Clip', 'West Dark Death Mountain (Bottom)', 'West Dark Death Mountain (Top)'), #cannot guarantee camera correction, but a bomb clip exists
    ('Ganons Tower Screen Wrap Clip', 'West Dark Death Mountain (Bottom)', 'GT Stairs'),  # This only gets you to the GT entrance
    ('Spectacle Rock Ledge Clip', 'West Death Mountain (Top)', 'Spectacle Rock Ledge'),
    
    ('Floating Island Clip', 'East Death Mountain (Top East)', 'Death Mountain Floating Island'),
    ('Floating Island Return Clip', 'Death Mountain Floating Island', 'East Death Mountain (Top East)'),
    #('DW Floating Island Clip', 'East Dark Death Mountain (Bottom)', 'Death Mountain Floating Island'), #cannot guarantee camera correction
    ('EDM East Dropdown Clip', 'East Death Mountain (Top East)', 'East Death Mountain (Bottom Left)'),
    ('EDM Hammer Bypass Teleport', 'East Death Mountain (Top West)', 'East Death Mountain (Top East)'),
    ('EDDM West Dropdown Clip', 'East Dark Death Mountain (Top)', 'East Dark Death Mountain (Bottom Left)'),
    ('WDM To EDM Bottom Clip', 'East Death Mountain (Bottom Left)', 'East Death Mountain (Bottom)'),
    ('WDDM To EDDM Bottom Clip', 'East Dark Death Mountain (Bottom Left)', 'East Dark Death Mountain (Bottom)'),
    ('TR Bridge Clip', 'East Dark Death Mountain (Top)', 'Dark Death Mountain Ledge'),
    
    ('TR Pegs Ledge Clip', 'Death Mountain TR Pegs Area', 'Death Mountain TR Pegs Ledge'),
    ('TR Pegs Ledge Descent Clip', 'Death Mountain TR Pegs Ledge', 'Death Mountain TR Pegs Area'), # inverted only, but doesn't hurt to exist always
    ('Turtle Rock Ledge Clip', 'Turtle Rock Area', 'Turtle Rock Ledge'),
    
    ('Mountain Pass To Ledge Clip', 'Mountain Pass Area', 'Mountain Pass Ledge'),
    ('Bumper Cave Ledge Clip', 'Bumper Cave Area', 'Bumper Cave Ledge'),
    ('Mountain Ledge Drop Clip', 'Mountain Pass Ledge', 'Mountain Pass Entry'),
    ('Bumper Cave Ledge Drop Clip', 'Bumper Cave Ledge', 'Bumper Cave Entry'),

    ('Potion Shop Northbound Rock Bypass Clip', 'Potion Shop Area', 'Potion Shop Northeast'),
    ('Potion Shop Southbound Rock Bypass Clip', 'Potion Shop Northeast', 'Potion Shop Area'),
    ('Dark Witch Northbound Rock Bypass Clip', 'Dark Witch Area', 'Dark Witch Northeast'),
    ('Dark Witch Southbound Rock Bypass Clip', 'Dark Witch Northeast', 'Dark Witch Area'),
    
    ('Hyrule Castle To Water Clip', 'Hyrule Castle Area', 'Hyrule Castle Water'), #fake flipper

    #('Bat Cave River Clip Spot', 'Blacksmith Area', 'Blacksmith Ledge'), #TODO: This should be added in MG (screenwrap transition)

    ('Maze Race Item Get Ledge Clip', 'Maze Race Area', 'Maze Race Prize'),

    #('Hobo Water Clip', 'Stone Bridge South Area', 'Stone Bridge Water'), # TODO: Doesn't work with OW Free Terrain
    
    ('Tree Line Water Clip', 'Tree Line Area', 'Tree Line Water'), #requires flippers
    ('Dark Tree Line Water Clip', 'Dark Tree Line Area', 'Dark Tree Line Water'), #requires flippers

    ('Desert To Teleporter Clip', 'Desert Area', 'Desert Teleporter Ledge'),
    ('Mire To Teleporter Clip', 'Mire Area', 'Mire Teleporter Ledge'),
    ('Desert To Bombos Tablet Clip', 'Desert Area', 'Bombos Tablet Ledge'),

    ('Lake Hylia To Shore Clip', 'Lake Hylia Northwest Bank', 'Lake Hylia South Shore'),
    ('Ice Lake To Shore Clip', 'Ice Lake Northwest Bank', 'Ice Lake Southwest Ledge')

    #('Desert Pass To Zora Clip', 'Desert Pass Area', 'Zoras Domain', ) #revisit when Zora is shuffled
]

# Common structure for cross-screen connections:
# (name, from_region, to_region) <- each three consists of [LW, DW]
# This is so Tile Flip OWR can properly connect both connections, and simultaneously be aware of which one requires pearl
# Note: Some clips have no way to reach the OOB area, and others have no way to get from the OOB area
# to a proper destination, these are marked with 'None'; these connections will not be made
boots_clips = [
    (['Lumberjack DMA Clip', 'Dark Lumberjack DMA Clip'], ['Lumberjack Area', 'Dark Lumberjack Area'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)']),

    (['Lumberjack DMD Clip', None], ['West Death Mountain (Top)', None], ['Lumberjack Area', 'Dark Lumberjack Area']),
    (['DM Glitched Bridge Clip', 'DDM Glitched Bridge Clip'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)'], ['East Death Mountain (Top East)', 'East Dark Death Mountain (Top)']),
    (['WDM to EDM Top Clip', 'WDDM to EDDM Top Clip'], ['West Death Mountain (Top)', 'West Dark Death Mountain (Top)'], ['East Death Mountain (Top West)', None]),
    (['Sanctuary DMD Clip', 'Chapel DMD Clip'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)'], ['Sanctuary Area', 'Dark Chapel Area']),
    (['Graveyard Ledge DMD Clip', 'Dark Graveyard DMD Clip', ], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)'], ['Graveyard Ledge', 'Dark Graveyard North']),
    (['Kings Grave DMD Clip', 'Dark Kings Grave DMD Clip'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)'], ['Kings Grave Area', None]),

    (['EDM to WDM Top Clip', 'EDDM To WDDM Clip'], ['East Death Mountain (Top West)', 'East Dark Death Mountain (Top)'], ['West Death Mountain (Top)', 'West Dark Death Mountain (Top)']),
    (['EDM To TR Pegs Clip', 'EDDM To TR Clip'], ['East Death Mountain (Top East)', 'East Dark Death Mountain (Top)'], ['Death Mountain TR Pegs Area', None]),
    (['EDM DMD FAWT Clip', 'Dark Witch DMD FAWT Clip'], ['East Death Mountain (Bottom)', 'East Dark Death Mountain (Bottom)'], ['Potion Shop Area', 'Dark Witch Area']),
    (['WDM DMD To River Bend Clip', 'WDDM DMD To Qirn Jump Clip'], ['East Death Mountain (Bottom Left)', 'East Dark Death Mountain (Bottom Left)'], ['River Bend Area', 'Qirn Jump Area']),
    (['EDM DMD To River Bend Clip', 'EDDM DMD To Qirn Jump Clip'], ['East Death Mountain (Bottom)', 'East Dark Death Mountain (Bottom)'], ['River Bend Area', 'Qirn Jump Area']),

    (['TR Pegs To EDM Clip', 'TR To EDDM Clip'], ['Death Mountain TR Pegs Area', 'Turtle Rock Area'], ['East Death Mountain (Top East)', 'East Dark Death Mountain (Top)']),
    (['Zora DMD Clip', 'Catfish DMD Clip'], ['Death Mountain TR Pegs Area', 'Turtle Rock Area'], ['Zora Waterfall Area', 'Catfish Area']),

    (['Mountain Pass To Pond Clip', 'Bumper Cave To Pond Clip'], ['Mountain Pass Area', 'Bumper Cave Area'], ['Kakariko Pond Area', 'Outcast Pond Area']),

    (['Zora Waterfall Ledge Clip', 'Catfish Ledge Clip'], ['Zora Waterfall Area', 'Catfish Area'], ['Zora Approach Area', 'Catfish Approach Area']),

    #(['Pond DMA Clip', 'Dark Pond DMA Clip'], ['Kakariko Pond Area', 'Outcast Pond Area'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)']), #cannot guarantee camera correction
    (['Pond To Mountain Pass Clip', 'Pond To Bumper Cave Clip'], ['Kakariko Pond Area', 'Outcast Pond Area'], ['Mountain Pass Area', 'Bumper Cave Area']),
    (['Pond To Bonk Rocks Clip', 'Pond To Chapel Clip'], ['Kakariko Pond Area', 'Outcast Pond Area'], ['Bonk Rock Ledge', 'Dark Chapel Area']),

    (['River Bend To Potion Shop Clip', 'Qirn Jump To Dark Witch Clip'], ['River Bend East Bank', 'Qirn Jump East Bank'], ['Potion Shop Area', 'Dark Witch Area']),
    (['River Bend To Wooden Bridge Clip', 'Qirn Jump To Broken Bridge North Clip'], ['River Bend East Bank', 'Qirn Jump East Bank'], ['Wooden Bridge Area', 'Broken Bridge Northeast']),
    (['River Bend To Broken Bridge Clip', 'Qirn Jump To Broken Bridge Clip'], ['River Bend East Bank', 'Qirn Jump East Bank'], [None, 'Broken Bridge Area']),

    (['Potion Shop To EP Clip', 'Dark Witch To PoD Clip'], ['Potion Shop Area', 'Dark Witch Area'], ['Eastern Palace Area', 'Palace of Darkness Area']),
    (['Potion Shop To River Bend Clip', 'Dark Witch To Qirn Jump Clip'], ['Potion Shop Area', 'Dark Witch Area'], ['River Bend East Bank', 'Qirn Jump East Bank']),
    (['Potion Shop To Zora Approach Clip', 'Dark Witch To Catfish Approach Clip'], ['Potion Shop Northeast', 'Dark Witch Northeast'], ['Zora Approach Area', 'Catfish Approach Area']),

    (['Zora Approach To Potion Shop Clip', 'Catfish Approach To Dark Witch Clip'], ['Zora Approach Area', 'Catfish Approach Area'], ['Potion Shop Area', 'Dark Witch Area']),
    (['Zora Approach To PoD Clip', 'Catfish Approach To PoD Clip'], ['Zora Approach Area', 'Catfish Approach Area'], [None, 'Palace of Darkness Area']),

    (['Kakariko Bomb Hut Clip', 'VoO To Dig Game Clip'], ['Kakariko Southwest', 'Village of Outcasts'], ['Maze Race Area', 'Dig Game Area']),
    (['Kakariko To Dig Game Hook Clip', 'VoO To Dig Game Hook Clip'], ['Kakariko Southwest', 'Village of Outcasts'], [None, 'Dig Game Ledge']), #requires hookshot

    (['Forgotten Forest To Blacksmith Clip', None], ['Forgotten Forest Area', None], ['Hyrule Castle Water', 'Pyramid Water']), #fake flipper

    (['Wooden Bridge To Dunes Clip', 'Broken Bridge To Dunes Clip'], ['Wooden Bridge Area', 'Broken Bridge West'], ['Sand Dunes Area', 'Dark Dunes Area']),
    (['Wooden Bridge To Water Clip', 'Broken Bridge To Water Clip'], ['Wooden Bridge Area', 'Broken Bridge West'], [None, 'Pyramid Water']), #fake flipper

    (['Eastern Palace To Zora Approach Clip', None], ['Eastern Palace Area', None], ['Zora Approach Area', 'Catfish Approach Area']),
    (['Eastern Palace To Nook Clip', None], ['Eastern Palace Area', None], ['Eastern Nook Area', 'Darkness Nook Area']),
    (['Eastern Palace To Cliff Clip', 'PoD To Cliff Clip'], ['Eastern Palace Area', 'Palace of Darkness Area'], ['Eastern Cliff', 'Darkness Cliff']),

    (['Sand Dunes To Cliff Clip', 'Dark Dunes To Cliff Clip'], ['Sand Dunes Area', 'Dark Dunes Area'], ['Eastern Cliff', 'Darkness Cliff']),
    (['Sand Dunes To Water Clip', 'Dark Dunes To Water Clip'], ['Sand Dunes Area', 'Dark Dunes Area'], [None, 'Pyramid Water']), #fake flipper

    (['Maze Race To Desert Ledge Clip', 'Dig Game To Mire Clip'], ['Maze Race Area', 'Dig Game Area'], ['Desert Ledge', 'Mire Area']),
    (['Maze Race To Desert Boss Clip', 'Dig Game To Desert Boss Clip'], ['Maze Race Area', 'Dig Game Area'], ['Desert Ledge Keep', None]),
    (['Suburb To Cliff Clip', 'Archery Game To Cliff Clip'], ['Kakariko Suburb Area', 'Archery Game Area'], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),
    (['Central Bonk Rocks To Cliff Clip', 'Dark Bonk Rocks To Cliff Clip'], ['Central Bonk Rocks Area', 'Dark Bonk Rocks Area'], ['Central Cliffs', 'Dark Central Cliffs']),
    (['Links House To Cliff Clip', 'Bomb Shop To Cliff Clip'], ['Links House Area', 'Big Bomb Shop Area'], ['Central Cliffs', 'Dark Central Cliffs']),
    (['Stone Bridge To Cliff Clip', 'Hammer Bridge To Cliff Clip'], ['Stone Bridge South Area', 'Hammer Bridge South Area'], ['Central Cliffs', 'Dark Central Cliffs']),
    (['Eastern Nook To Eastern Clip', None], ['Eastern Nook Area', None], ['Eastern Palace Area', 'Palace of Darkness Area']),
    (['Eastern Nook To Ice Cave FAWT Clip', 'PoD Nook To Shopping Mall FAWT Clip'], ['Eastern Nook Area', 'Darkness Nook Area'], ['Ice Cave Area', 'Shopping Mall Area']),

    (['Links To Bridge FAWT Clip', 'Bomb Shop To Hammer Bridge FAWT Clip'], ['Links House Area', 'Big Bomb Shop Area'], ['Stone Bridge North Area', 'Hammer Bridge North Area']), #fake flipper

    (['Stone Bridge To Water Clip', 'Hammer Bridge To Water Clip'], ['Stone Bridge North Area', 'Hammer Bridge North Area'], [None, 'Pyramid Water']), #fake flipper

    (['Desert To Maze Race Clip', None], ['Desert Ledge', None], ['Maze Race Area', 'Dig Game Area']),
    (['Desert To Cliff Clip', 'Mire To Cliff Clip'], ['Desert Area', 'Mire Area'], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),

    (['Flute Boy To Cliff Clip', 'Stumpy To Cliff Clip'], ['Flute Boy Approach Area', 'Stumpy Approach Area'], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),
    (['Cave 45 To Cliff Clip', None], ['Cave 45 Ledge', None], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),

    (['C Whirlpool To Cliff Clip', 'Dark C Whirlpool To Cliff Clip'], ['C Whirlpool Area', 'Dark C Whirlpool Area'], ['Central Cliffs', 'Dark Central Cliffs']),
    (['C Whirlpool Outer To Cliff Clip', 'Dark C Whirlpool Outer To Cliff Clip'], ['C Whirlpool Outer Area', 'Dark C Whirlpool Outer Area'], ['Central Cliffs', 'Dark Central Cliffs']),
    (['C Whirlpool Portal Bomb Clip', 'Dark C Whirlpool Portal Bomb Clip'], ['C Whirlpool Portal Area', 'Dark C Whirlpool Portal Area'], ['Central Cliffs', 'Dark Central Cliffs']), # bomb TODO: bombbag not considered

    (['Statues To Cliff Clip', 'Hype To Cliff Clip'], ['Statues Area', 'Hype Cave Area'], ['Central Cliffs', 'Dark Central Cliffs']),

    (['Lake Hylia To Statues Clip', 'Ice Lake To Hype Clip'], ['Lake Hylia Northwest Bank', 'Ice Lake Northwest Bank'], ['Statues Area', 'Hype Cave Area']),
    (['Lake Hylia To South Pass Clip', 'Ice Lake To South Pass Clip'], ['Lake Hylia Northwest Bank', 'Ice Lake Northwest Bank'], ['South Pass Area', 'Dark South Pass Area']),

    (['Desert Pass To Cliff Clip', 'Swamp Nook To Cliff Clip'], ['Desert Pass Area', 'Swamp Nook Area'], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),
    (['Desert Pass Southeast To Cliff Clip', None], ['Desert Pass Southeast', None], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),

    (['Dam To Cliff Clip', 'Swamp To Cliff Clip'], ['Dam Area', 'Swamp Area'], ['Desert Northern Cliffs', 'Mire Northern Cliffs']),
    (['Dam To Desert Pass Southeast Clip', 'Swamp To Desert Pass Southeast Clip'], ['Dam Area', 'Swamp Area'], ['Desert Pass Southeast', None]),

    (['South Pass To Lake Hylia Clip', 'South Pass To Ice Lake Clip'], ['South Pass Area', 'Dark South Pass Area'], ['Lake Hylia Northwest Bank', 'Ice Lake Northwest Bank']),
    (['South Pass To Shore Clip', 'South Pass To Dark Shore Clip'], ['South Pass Area', 'Dark South Pass Area'], ['Lake Hylia South Shore', 'Ice Lake Southwest Ledge']),
    #(['Octoballoon To Shore Clip', 'Bomber Corner To Shore Clip'], ['Octoballoon Area', 'Bomber Corner Area'], ['Lake Hylia South Shore', 'Ice Lake Southeast Ledge']), #map wrap hardlock risk

    (['HC Water To Blacksmith Clip', 'Pyramid Water To Hammerpegs Clip'], ['Hyrule Castle Water', 'Pyramid Water'], ['Blacksmith Area', 'Hammer Pegs Area']), #TODO: THIS IS NOT A BOOTS CLIP, this is a normal connection that needs to occur somewhere
    ([None, 'Pyramid Water To Bomb Shop Clip'], [None, 'Pyramid Water'], ['Links House Area', 'Big Bomb Shop Area']) #TODO: THIS IS NOT A BOOTS CLIP, this is a normal connection that needs to occur somewhere
]

mirror_clips_local = [
    ('Desert East Mirror Clip', 'Mire Area', 'Desert Mouth'),
    ('EDDM Mirror Clip', 'East Dark Death Mountain (Bottom Left)', 'East Dark Death Mountain (Bottom)'),
    ('EDDM Mirror Clip', 'East Dark Death Mountain (Top)', 'Dark Death Mountain Ledge')
]

mirror_clips = [
    ([None, 'Qirn Jump Bunny DMD Clip'], [None, 'East Dark Death Mountain (Bottom Left)'], ['River Bend Area', 'Qirn Jump Area'])
]

mirror_offsets = [
    (['DM Offset Mirror', 'DDM Offset Mirror'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)'], ['Hyrule Castle Courtyard Northeast', 'Pyramid Crack'], ['Pyramid Area', 'Hyrule Castle Courtyard']),
    (['DM To HC Ledge Offset Mirror', 'DDM To Pyramid Offset Mirror'], ['West Death Mountain (Bottom)', 'West Dark Death Mountain (Bottom)'], ['Hyrule Castle Ledge', 'Pyramid Area'], ['Pyramid Area', 'Hyrule Castle Area'])
]
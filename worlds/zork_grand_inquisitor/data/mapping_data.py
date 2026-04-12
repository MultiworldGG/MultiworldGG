from typing import Dict, Optional, Tuple, Union

from ..enums import (
    ZorkGrandInquisitorClientSeedInformation,
    ZorkGrandInquisitorCraftableSpellBehaviors,
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorEntranceRandomizer,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorHotspots,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLandmarksanity,
    ZorkGrandInquisitorRegions,
    ZorkGrandInquisitorStartingLocations,
)


death_cause_labels: Dict[int, str] = {
    1: "PLAYER got their noggin smitten in twain",
    3: "PLAYER decided to jump into a bottomless pit",
    4: "PLAYER decided to step into the infinite",
    5: "PLAYER became an evil spawn's plaything",
    6: "PLAYER started a career as a talking manhole cover",
    7: "PLAYER got sucked into a starship's tractor beam",
    8: "PLAYER became a paperweight",
    9: "PLAYER rolled into the airless expanse of the cosmos",
    10: "PLAYER got their head bitten off",
    11: "PLAYER was swallowed whole by a dragon",
    13: "PLAYER decided to spend an eternity staring at scenic vistas",
    18: "PLAYER was eaten by a grue",
    19: "PLAYER was vaporized by Zork Rocks",
    20: "PLAYER got stung by a thousand quelbees",
    21: "PLAYER broke curfew",
    22: "PLAYER lost their soul to a scratch-and-win card",
    29: "PLAYER was outsmarted by bees",
    30: "PLAYER got pureed by a six-armed invisible guard",
    32: "PLAYER's head exploded",
    33: "PLAYER died of arteriosclerosis",
    34: "PLAYER decided to ignore the sign and THROCK the grass",
    37: "PLAYER lost a game of strip grue, fire, water",
}

# Avoid spells in early items to prevent clash with craftable spells
early_items_for_starting_location: Dict[
    ZorkGrandInquisitorStartingLocations, Optional[Tuple[Tuple[ZorkGrandInquisitorItems, ...], ...]]
] = {
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: (
        (
            ZorkGrandInquisitorItems.WELL_ROPE,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.CROSSROADS: None,
    ZorkGrandInquisitorStartingLocations.DM_LAIR: None,
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: None,
    ZorkGrandInquisitorStartingLocations.GUE_TECH: None,
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: None,
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: None,
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: None,
    ZorkGrandInquisitorStartingLocations.MONASTERY: None,
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: None,
}

endgame_connecting_regions_for_goal: Dict[
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorRegions,
] = {
    ZorkGrandInquisitorGoals.THREE_ARTIFACTS: ZorkGrandInquisitorRegions.MENU,
    ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT: ZorkGrandInquisitorRegions.WALKING_CASTLE,
    ZorkGrandInquisitorGoals.SPELL_HEIST: ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
    ZorkGrandInquisitorGoals.ZORK_TOUR: ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
    ZorkGrandInquisitorGoals.GRIM_JOURNEY: (
        ZorkGrandInquisitorRegions.HADES_BEYOND_GATES
    ),
}

entrance_names: Dict[
    Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions],
    str,
] = {
    (
        ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL,
        ZorkGrandInquisitorRegions.CROSSROADS
    ): "Down the Dragon Staircase",
    (
        ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL
    ): "Teleport Up the Well",
    (
        ZorkGrandInquisitorRegions.CROSSROADS,
        ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL
    ): "Up the Dragon Staircase",
    (
        ZorkGrandInquisitorRegions.CROSSROADS,
        ZorkGrandInquisitorRegions.DM_LAIR
    ): "Through the Overgrown Door",
    (
        ZorkGrandInquisitorRegions.CROSSROADS,
        ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE
    ): "Through the 'In Magic We Trust' Door",
    (
        ZorkGrandInquisitorRegions.CROSSROADS,
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS
    ): "Through the Subway Turnstile",
    (
        ZorkGrandInquisitorRegions.CROSSROADS,
        ZorkGrandInquisitorRegions.TELEPORTER
    ): "At the Crossroads Teleportation Station",
    (
        ZorkGrandInquisitorRegions.DM_LAIR,
        ZorkGrandInquisitorRegions.CROSSROADS
    ): "Exit Through the Overgrown Door",
    (
        ZorkGrandInquisitorRegions.DM_LAIR,
        ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR
    ): "Through Sloshed Harry",
    (
        ZorkGrandInquisitorRegions.DM_LAIR,
        ZorkGrandInquisitorRegions.TELEPORTER
    ): "At the Dungeon Master's Lair Teleportation Station",
    (
        ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        ZorkGrandInquisitorRegions.DM_LAIR
    ): "Exit Through Sloshed Harry",
    (
        ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        ZorkGrandInquisitorRegions.WALKING_CASTLE
    ): "Through the Walking Castle Porticullis",
    (
        ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
        ZorkGrandInquisitorRegions.WHITE_HOUSE
    ): "Through the White House Time Tunnel",
    (
        ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
        ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON
    ): "Towards the Dragon",
    (
        ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
        ZorkGrandInquisitorRegions.HADES_BEYOND_GATES
    ): "Exit Through the Dragon Archipelago Time Tunnel",
    (
        ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
        ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO
    ): "Towards the Dragon Archipelago Time Tunnel",
    (
        ZorkGrandInquisitorRegions.GUE_TECH,
        ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE
    ): "Through the Right Window",
    (
        ZorkGrandInquisitorRegions.GUE_TECH,
        ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY
    ): "To the (Infinite) Corridor",
    (
        ZorkGrandInquisitorRegions.GUE_TECH,
        ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE
    ): "Through the Entrance Door",
    (
        ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
        ZorkGrandInquisitorRegions.CROSSROADS
    ): "Exit Through the 'In Magic We Trust' Door",
    (
        ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
        ZorkGrandInquisitorRegions.GUE_TECH
    ): "Through the 3rd Pillar's Window",
    (
        ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        ZorkGrandInquisitorRegions.GUE_TECH
    ): "To the Lobby",
    (
        ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
        ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE
    ): "Through the Student ID Door",
    (
        ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
        ZorkGrandInquisitorRegions.GUE_TECH
    ): "Through the Pillar's Window",
    (
        ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
        ZorkGrandInquisitorRegions.TELEPORTER
    ): "At the GUE Tech Teleportation Station",
    (
        ZorkGrandInquisitorRegions.HADES,
        ZorkGrandInquisitorRegions.HADES_BEYOND_GATES
    ): "Through the Gates of Hell",
    (
        ZorkGrandInquisitorRegions.HADES,
        ZorkGrandInquisitorRegions.HADES_SHORE
    ): "Return Across the River Styx",
    (
        ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
        ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO
    ): "Through the Dragon Archipelago Time Tunnel",
    (
        ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
        ZorkGrandInquisitorRegions.HADES
    ): "Exit Through the Gates of Hell",
    (
        ZorkGrandInquisitorRegions.HADES_SHORE,
        ZorkGrandInquisitorRegions.HADES
    ): "Across the River Styx",
    (
        ZorkGrandInquisitorRegions.HADES_SHORE,
        ZorkGrandInquisitorRegions.SUBWAY_HADES
    ): "Exit to the Subway Station",
    (
        ZorkGrandInquisitorRegions.HADES_SHORE,
        ZorkGrandInquisitorRegions.TELEPORTER
    ): "At the Hades Teleportation Station",
    (
        ZorkGrandInquisitorRegions.MONASTERY,
        ZorkGrandInquisitorRegions.HADES_SHORE
    ): "Through the Totemizer Set to 'Straight to Hell'",
    (
        ZorkGrandInquisitorRegions.MONASTERY,
        ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT
    ): "Through the Totemizer Set to 'Hall of Inquisition'",
    (
        ZorkGrandInquisitorRegions.MONASTERY,
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY
    ): "Down the Hatch",
    (
        ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        ZorkGrandInquisitorRegions.MONASTERY
    ): "To the Totemizer",
    (
        ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
        ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST
    ): "Through the Past Port Foozle Time Tunnel",
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST
    ): "Along the Path Down the Hill",
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ
    ): "Along the Path Up the Hill",
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL
    ): "Along the Path Into the Woods",
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
        ZorkGrandInquisitorRegions.PORT_FOOZLE
    ): "Along the Path Towards Port Foozle",
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL,
        ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL
    ): "Down the Well",
    (
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST
    ): "Along the Path Out of the Woods",
    (
        ZorkGrandInquisitorRegions.PORT_FOOZLE,
        ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST
    ): "Along the Path Out of Port Foozle",
    (
        ZorkGrandInquisitorRegions.PORT_FOOZLE,
        ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP
    ): "Through Jack's Door",
    (
        ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP,
        ZorkGrandInquisitorRegions.PORT_FOOZLE
    ): "Exit Through Jack's Door",
    (
        ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT
    ): "Exit Through the Past Port Foozle Time Tunnel",
    (
        ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
        ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN
    ): "Through the Tavern Door",
    (
        ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
        ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST
    ): "Exit Through the Tavern Door",
    (
        ZorkGrandInquisitorRegions.SPELL_LAB,
        ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE
    ): "Return Across the Bridge",
    (
        ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY
    ): "Exit through the Student ID Door",
    (
        ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        ZorkGrandInquisitorRegions.SPELL_LAB
    ): "Across the Bridge",
    (
        ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
        ZorkGrandInquisitorRegions.TELEPORTER
    ): "At the Spell Lab Teleportation Station",
    (
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        ZorkGrandInquisitorRegions.CROSSROADS
    ): "Up the Escalator",
    (
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM
    ): "Subway Ride from Crossroads to FCD #3",
    (
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        ZorkGrandInquisitorRegions.SUBWAY_HADES
    ): "Subway Ride from Crossroads to Hades",
    (
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY
    ): "Subway Ride from Crossroads to Monastery",
    (
        ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS
    ): "Subway Ride from FCD #3 to Crossroads",
    (
        ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        ZorkGrandInquisitorRegions.SUBWAY_HADES
    ): "Subway Ride from FCD #3 to Hades",
    (
        ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY
    ): "Subway Ride from FCD #3 to Monastery",
    (
        ZorkGrandInquisitorRegions.SUBWAY_HADES,
        ZorkGrandInquisitorRegions.HADES_SHORE
    ): "Towards the Hades Shore",
    (
        ZorkGrandInquisitorRegions.SUBWAY_HADES,
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS
    ): "Subway Ride from Hades to Crossroads",
    (
        ZorkGrandInquisitorRegions.SUBWAY_HADES,
        ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM
    ): "Subway Ride from Hades to FCD #3",
    (
        ZorkGrandInquisitorRegions.SUBWAY_HADES,
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY
    ): "Subway Ride from Hades to Monastery",
    (
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        ZorkGrandInquisitorRegions.MONASTERY
    ): "Climb up the Rope",
    (
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS
    ): "Subway Ride from Monastery to Crossroads",
    (
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM
    ): "Subway Ride from Monastery to FCD #3",
    (
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        ZorkGrandInquisitorRegions.SUBWAY_HADES
    ): "Subway Ride from Monastery to Hades",
    (
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
        ZorkGrandInquisitorRegions.TELEPORTER
    ): "At the Monastery Teleportation Station",
    (
        ZorkGrandInquisitorRegions.TELEPORTER,
        ZorkGrandInquisitorRegions.CROSSROADS
    ): "Teleport to Crossroads",
    (
        ZorkGrandInquisitorRegions.TELEPORTER,
        ZorkGrandInquisitorRegions.DM_LAIR
    ): "Teleport to Dungeon Master's Lair",
    (
        ZorkGrandInquisitorRegions.TELEPORTER,
        ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE
    ): "Teleport to GUE Tech",
    (
        ZorkGrandInquisitorRegions.TELEPORTER,
        ZorkGrandInquisitorRegions.HADES_SHORE
    ): "Teleport to Hades",
    (
        ZorkGrandInquisitorRegions.TELEPORTER,
        ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE
    ): "Teleport to Spell Lab",
    (
        ZorkGrandInquisitorRegions.TELEPORTER,
        ZorkGrandInquisitorRegions.SUBWAY_MONASTERY
    ): "Teleport to Monastery",
    (
        ZorkGrandInquisitorRegions.WALKING_CASTLE,
        ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR
    ): "Exit Through the Walking Castle Porticullis",
    (
        ZorkGrandInquisitorRegions.WHITE_HOUSE,
        ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR
    ): "Exit Through the White House Time Tunnel",
    (
        ZorkGrandInquisitorRegions.WHITE_HOUSE,
        ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR
    ): "Through the White House Front Door",
    (
        ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
        ZorkGrandInquisitorRegions.WHITE_HOUSE
    ): "Exit Through the White House Front Door",
}

entrance_names_reverse: Dict[str, Tuple[ZorkGrandInquisitorRegions, ZorkGrandInquisitorRegions]] = {
    name: entrance for entrance, name in entrance_names.items()
}

game_location_to_region: Dict[
    str,
    ZorkGrandInquisitorRegions,
] = {
    "cd20": ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO_DRAGON,
    "cd60": ZorkGrandInquisitorRegions.DRAGON_ARCHIPELAGO,
    "dc10": ZorkGrandInquisitorRegions.WALKING_CASTLE,
    "dg10": ZorkGrandInquisitorRegions.DM_LAIR,
    "dg30": ZorkGrandInquisitorRegions.DM_LAIR,
    "dg40": ZorkGrandInquisitorRegions.DM_LAIR,
    "dv10": ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
    "hp10": ZorkGrandInquisitorRegions.HADES_SHORE,
    "hp40": ZorkGrandInquisitorRegions.HADES,
    "hp50": ZorkGrandInquisitorRegions.HADES,
    "hp60": ZorkGrandInquisitorRegions.HADES_BEYOND_GATES,
    "me10": ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
    "me20": ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
    "mt10": ZorkGrandInquisitorRegions.MONASTERY,
    "mt20": ZorkGrandInquisitorRegions.MONASTERY,
    "mt30": ZorkGrandInquisitorRegions.MONASTERY,
    "pc10": ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL,
    "pe10": ZorkGrandInquisitorRegions.PORT_FOOZLE,
    "pp10": ZorkGrandInquisitorRegions.PORT_FOOZLE_JACKS_SHOP,
    "ps10": ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
    "ps20": ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_WELL,
    "px10": ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_INQUISITION_HQ,
    "qb10": ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST_TAVERN,
    "qe10": ZorkGrandInquisitorRegions.PORT_FOOZLE_PAST,
    "sg10": ZorkGrandInquisitorRegions.WHITE_HOUSE_INTERIOR,
    "sw40": ZorkGrandInquisitorRegions.WHITE_HOUSE,
    "te10": ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
    "te30": ZorkGrandInquisitorRegions.GUE_TECH_ENTRANCE,
    "te40": ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
    "te50": ZorkGrandInquisitorRegions.GUE_TECH_OUTSIDE,
    "th10": ZorkGrandInquisitorRegions.GUE_TECH,
    "th30": ZorkGrandInquisitorRegions.GUE_TECH_HALLWAY,
    "tp10": ZorkGrandInquisitorRegions.SPELL_LAB_BRIDGE,
    "tp20": ZorkGrandInquisitorRegions.SPELL_LAB,
    "tr10": ZorkGrandInquisitorRegions.GUE_TECH,
    "tr20": ZorkGrandInquisitorRegions.GUE_TECH,
    "uc10": ZorkGrandInquisitorRegions.CROSSROADS,
    "uc30": ZorkGrandInquisitorRegions.CROSSROADS,
    "uc40": ZorkGrandInquisitorRegions.CROSSROADS,
    "uc50": ZorkGrandInquisitorRegions.CROSSROADS,
    "uc60": ZorkGrandInquisitorRegions.CROSSROADS,
    "ue10": ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
    "ue20": ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
    "uh10": ZorkGrandInquisitorRegions.SUBWAY_HADES,
    "uh20": ZorkGrandInquisitorRegions.SUBWAY_HADES,
    "um10": ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
    "um20": ZorkGrandInquisitorRegions.SUBWAY_MONASTERY,
    "us10": ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
    "us20": ZorkGrandInquisitorRegions.SUBWAY_CROSSROADS,
    "uw10": ZorkGrandInquisitorRegions.BOTTOM_OF_THE_WELL,
}

hotspot_to_regional_hotspot: Dict[ZorkGrandInquisitorItems, ZorkGrandInquisitorItems] = {
    ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES
    ),
    ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST
    ),
    ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB
    ),
    ZorkGrandInquisitorItems.HOTSPOT_BLINDS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_BUCKET: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY
    ),
    ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY
    ),
    ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS
    ),
    ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_HOUSE_EXIT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HARRY: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS
    ),
    ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MIRROR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM
    ),
    ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST
    ),
    ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR
    ),
    ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH
    ),
    ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS
    ),
    ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST
    ),
    ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY
    ),
    ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS: (
        ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY
    ),
}

hotspots_for_regional_hotspot: Dict[ZorkGrandInquisitorItems, Tuple[ZorkGrandInquisitorItems, ...]] = {
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_CROSSROADS: (
        ZorkGrandInquisitorItems.HOTSPOT_BUCKET,
        ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
        ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE,
        ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR,
        ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DM_LAIR: (
        ZorkGrandInquisitorItems.HOTSPOT_BLINDS,
        ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
        ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_HOUSE_EXIT,
        ZorkGrandInquisitorItems.HOTSPOT_HARRY,
        ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY,
        ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH,
        ZorkGrandInquisitorItems.HOTSPOT_MIRROR,
        ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE,
        ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON,
        ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_DRAGON_ARCHIPELAGO: (
        ZorkGrandInquisitorItems.HOTSPOT_DRAGON_CLAW,
        ZorkGrandInquisitorItems.HOTSPOT_DRAGON_NOSTRILS,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_FLOOD_CONTROL_DAM: (
        ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS,
        ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS,
        ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE,
        ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_GUE_TECH: (
        ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS,
        ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT,
        ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT,
        ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT,
        ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER,
        ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND,
        ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT,
        ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS,
        ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR,
        ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_GRASS,
        ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS,
        ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
        ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS,
        ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT,
        ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_HADES: (
        ZorkGrandInquisitorItems.HOTSPOT_666_MAILBOX,
        ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
        ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_MONASTERY: (
        ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT,
        ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER,
        ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
        ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE: (
        ZorkGrandInquisitorItems.HOTSPOT_DOCK_WINCH,
        ZorkGrandInquisitorItems.HOTSPOT_GRAND_INQUISITOR_DOLL,
        ZorkGrandInquisitorItems.HOTSPOT_JACKS_DOOR,
        ZorkGrandInquisitorItems.HOTSPOT_LOUDSPEAKER_VOLUME_BUTTONS,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_PORT_FOOZLE_PAST: (
        ZorkGrandInquisitorItems.HOTSPOT_ALPINES_QUANDRY_CARD_SLOTS,
        ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR,
        ZorkGrandInquisitorItems.HOTSPOT_TAVERN_FLY,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_SPELL_LAB: (
        ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX,
        ZorkGrandInquisitorItems.HOTSPOT_ROPE_BRIDGE,
        ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER,
        ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT,
        ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_CHASM,
    ),
    ZorkGrandInquisitorItems.HOTSPOT_REGIONAL_WHITE_HOUSE: (
        ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT,
        ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR,
        ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG,
        ZorkGrandInquisitorItems.HOTSPOT_SKULL_CAGE,
    ),
}

labels_for_enum_items: Dict[
    Union[
        ZorkGrandInquisitorCraftableSpellBehaviors,
        ZorkGrandInquisitorDeathsanity,
        ZorkGrandInquisitorEntranceRandomizer,
        ZorkGrandInquisitorGoals,
        ZorkGrandInquisitorHotspots,
        ZorkGrandInquisitorLandmarksanity,
        ZorkGrandInquisitorStartingLocations,
    ],
    str
] = {
    ZorkGrandInquisitorClientSeedInformation.REVEAL_NOTHING: "Reveal Nothing",
    ZorkGrandInquisitorClientSeedInformation.REVEAL_GOAL: "Reveal Goal",
    ZorkGrandInquisitorClientSeedInformation.REVEAL_GOAL_AND_OPTIONS: "Reveal Goal and Options",
    ZorkGrandInquisitorCraftableSpellBehaviors.VANILLA: "Vanilla",
    ZorkGrandInquisitorCraftableSpellBehaviors.ANY_SPELL: "Any Spell",
    ZorkGrandInquisitorCraftableSpellBehaviors.ANYTHING: "Anything",
    ZorkGrandInquisitorDeathsanity.OFF: "Off",
    ZorkGrandInquisitorDeathsanity.ON: "On",
    ZorkGrandInquisitorEntranceRandomizer.DISABLED: "Disabled",
    ZorkGrandInquisitorEntranceRandomizer.COUPLED: "Enabled (Coupled Entrances)",
    ZorkGrandInquisitorEntranceRandomizer.UNCOUPLED: "Enabled (Uncoupled Entrances)",
    ZorkGrandInquisitorGoals.THREE_ARTIFACTS: "Three Artifacts",
    ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT: "Artifact of Magic Hunt",
    ZorkGrandInquisitorGoals.SPELL_HEIST: "Spell Heist",
    ZorkGrandInquisitorGoals.ZORK_TOUR: "Zork Tour",
    ZorkGrandInquisitorGoals.GRIM_JOURNEY: "Grim Journey",
    ZorkGrandInquisitorHotspots.ENABLED: "Enabled",
    ZorkGrandInquisitorHotspots.REQUIRE_ITEM_PER_REGION: "Require Item Per Region",
    ZorkGrandInquisitorHotspots.REQUIRE_ITEM_PER_HOTSPOT: "Require Item Per Hotspot",
    ZorkGrandInquisitorLandmarksanity.OFF: "Off",
    ZorkGrandInquisitorLandmarksanity.ON: "On",
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: "Port Foozle",
    ZorkGrandInquisitorStartingLocations.CROSSROADS: "Crossroads",
    ZorkGrandInquisitorStartingLocations.DM_LAIR: "Dungeon Master's Lair",
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: "Dungeon Master's House",
    ZorkGrandInquisitorStartingLocations.GUE_TECH: "GUE Tech",
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: "Spell Lab",
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: "Hades Shore",
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: "Flood Control Dam #3",
    ZorkGrandInquisitorStartingLocations.MONASTERY: "Monastery Totemizer",
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: "Monastery Exhibit",
}

starter_kit_for_entrance_randomizer: Tuple[ZorkGrandInquisitorItems, ...] = (
    ZorkGrandInquisitorItems.HAMMER,
    ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
    ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
    ZorkGrandInquisitorItems.SPELL_IGRAM,
    ZorkGrandInquisitorItems.SPELL_REZROV,
    ZorkGrandInquisitorItems.SPELL_THROCK,
    ZorkGrandInquisitorItems.SWORD,
)

starter_kits_for_starting_location: Dict[
    ZorkGrandInquisitorStartingLocations, Optional[Tuple[Tuple[ZorkGrandInquisitorItems, ...], ...]]
] = {
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_BUCKET,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.CROSSROADS: (
        (
            ZorkGrandInquisitorItems.WELL_ROPE,
            ZorkGrandInquisitorItems.HOTSPOT_BUCKET,
        ),
        (
            ZorkGrandInquisitorItems.SPELL_BEBURTT,
            ZorkGrandInquisitorItems.SUBWAY_TOKEN,
            ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
        ),
        (
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.HOTSPOT_IN_MAGIC_WE_TRUST_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS,
        ),
        (
            ZorkGrandInquisitorItems.HAMMER,
            ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE,
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
            ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM,
            ZorkGrandInquisitorItems.SPELL_THROCK,
        ),
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.DM_LAIR: (
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_HARRY,
            ZorkGrandInquisitorItems.HUNGUS_LARD,
            ZorkGrandInquisitorItems.HOTSPOT_QUELBEE_HIVE,
            ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
        ),
        (
            ZorkGrandInquisitorItems.HAMMER,
            ZorkGrandInquisitorItems.SPELL_THROCK,
            ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON,
            ZorkGrandInquisitorItems.SNAPDRAGON,
            ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM,
        ),
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_HARRY,
            ZorkGrandInquisitorItems.CIGAR,
            ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
        ),
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_HARRY,
            ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
            ZorkGrandInquisitorItems.SHOVEL,
            ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND,
        ),
        (
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.HOTSPOT_HARRY,
            ZorkGrandInquisitorItems.CIGAR,
            ZorkGrandInquisitorItems.HOTSPOT_HARRYS_ASHTRAY,
            ZorkGrandInquisitorItems.MEAD_LIGHT,
            ZorkGrandInquisitorItems.ZIMDOR_SCROLL,
            ZorkGrandInquisitorItems.HOTSPOT_HARRYS_BIRD_BATH,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_BLINDS,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.SPELL_OBIDIL,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_MIRROR,
            ZorkGrandInquisitorItems.SCROLL_FRAGMENT_ANS,
            ZorkGrandInquisitorItems.SCROLL_FRAGMENT_GIV,
            ZorkGrandInquisitorItems.COCOA_INGREDIENTS,
            ZorkGrandInquisitorItems.HUNGUS_LARD,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
            ZorkGrandInquisitorItems.TOTEM_GRIFF,
            ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG,
            ZorkGrandInquisitorItems.HOTSPOT_MIRROR,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
            ZorkGrandInquisitorItems.TOTEM_LUCY,
            ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_FLAG,
            ZorkGrandInquisitorItems.HOTSPOT_MAILBOX_DOOR,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_CLOSET_DOOR,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
            ZorkGrandInquisitorItems.TOTEM_BROG,
            ZorkGrandInquisitorItems.BROGS_FLICKERING_TORCH,
            ZorkGrandInquisitorItems.BROGS_GRUE_EGG,
            ZorkGrandInquisitorItems.HOTSPOT_COOKING_POT,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.GUE_TECH: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_DOOR,
            ZorkGrandInquisitorItems.HOTSPOT_DIRT_MOUND,
            ZorkGrandInquisitorItems.SHOVEL,
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS,
        ),
        (
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
            ZorkGrandInquisitorItems.HOTSPOT_CHANGE_MACHINE_SLOT,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS,
        ),
        (
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_VACUUM_SLOT,
            ZorkGrandInquisitorItems.PERMA_SUCK_MACHINE,
            ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.ZORK_ROCKS,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_FROZEN_TREAT_MACHINE_DOORS,
        ),
        (
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_CANDY_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
        ),
        (
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_BUTTONS,
            ZorkGrandInquisitorItems.HOTSPOT_SODA_MACHINE_COIN_SLOT,
            ZorkGrandInquisitorItems.ZORK_ROCKS,
            ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
            ZorkGrandInquisitorItems.HOTSPOT_DENTED_LOCKER,
            ZorkGrandInquisitorItems.HOTSPOT_STUDENT_ID_MACHINE,
            ZorkGrandInquisitorItems.STUDENT_ID,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER,
            ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX,
            ZorkGrandInquisitorItems.SANDWITCH_WRAPPER,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.MONASTERY_ROPE,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER,
            ZorkGrandInquisitorItems.SANDWITCH_WRAPPER,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.SWORD,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER,
            ZorkGrandInquisitorItems.HOTSPOT_BLANK_SCROLL_BOX,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_CHECKER,
            ZorkGrandInquisitorItems.SANDWITCH_WRAPPER,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_SPELL_LAB_BRIDGE_EXIT,
            ZorkGrandInquisitorItems.HOTSPOT_PURPLE_WORDS,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.SPELL_SNAVIG,
            ZorkGrandInquisitorItems.TOTEM_BROG,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.SPELL_OBIDIL,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,
            ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
        ),
        (
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
            ZorkGrandInquisitorItems.SPELL_KENDALL,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.SWORD,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.MONASTERY_ROPE,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL,
        ),
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
            ZorkGrandInquisitorItems.HOTSPOT_GLASS_CASE,
            ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON,
            ZorkGrandInquisitorItems.HOTSPOT_SPRING_MUSHROOM,
            ZorkGrandInquisitorItems.HAMMER,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_DOORS,
            ZorkGrandInquisitorItems.HOTSPOT_FLOOD_CONTROL_BUTTONS,
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ),
        (
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
        ),
        (
            ZorkGrandInquisitorItems.SPELL_THROCK,
            ZorkGrandInquisitorItems.HOTSPOT_MOSSY_GRATE,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
            ZorkGrandInquisitorItems.HOTSPOT_SNAPDRAGON,
        ),
        (
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_GUE_TECH,
            ZorkGrandInquisitorItems.HOTSPOT_GUE_TECH_WINDOWS,
        ),
        (
            ZorkGrandInquisitorItems.POUCH_OF_ZORKMIDS,
            ZorkGrandInquisitorItems.HOTSPOT_SOUVENIR_COIN_SLOT,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_RECEIVER,
            ZorkGrandInquisitorItems.HOTSPOT_HADES_PHONE_BUTTONS,
            ZorkGrandInquisitorItems.SWORD,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.MONASTERY: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_HALL_OF_INQUISITION,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER,
            ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_STRAIGHT_TO_HELL,
            ZorkGrandInquisitorItems.OLD_SCRATCH_CARD,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.SUBWAY_TOKEN,
            ZorkGrandInquisitorItems.HOTSPOT_SUBWAY_TOKEN_SLOT,
        ),
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
            ZorkGrandInquisitorItems.SPELL_REZROV,
        ),
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
            ZorkGrandInquisitorItems.HOTSPOT_HARRY,
            ZorkGrandInquisitorItems.HOTSPOT_DUNGEON_MASTERS_LAIR_ENTRANCE,
            ZorkGrandInquisitorItems.SWORD,
        ),
    ),
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: (
        (
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_HAMMER_SLOT,
            ZorkGrandInquisitorItems.HOTSPOT_CLOSING_THE_TIME_TUNNELS_LEVER,
            ZorkGrandInquisitorItems.LARGE_TELEGRAPH_HAMMER,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
            ZorkGrandInquisitorItems.TOTEM_GRIFF,
            ZorkGrandInquisitorItems.HOTSPOT_PORT_FOOZLE_PAST_TAVERN_DOOR,
        ),
        (
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,
        ),
        (
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,
        ),
        (
            ZorkGrandInquisitorItems.MAP,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS,
        ),
        (
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_WHEELS,
            ZorkGrandInquisitorItems.HOTSPOT_TOTEMIZER_SWITCH,
        ),
    ),
}

starting_location_to_region: Dict[
    ZorkGrandInquisitorStartingLocations, ZorkGrandInquisitorRegions
] = {
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: ZorkGrandInquisitorRegions.OUTSIDE_PORT_FOOZLE_SIGNPOST,
    ZorkGrandInquisitorStartingLocations.CROSSROADS: ZorkGrandInquisitorRegions.CROSSROADS,
    ZorkGrandInquisitorStartingLocations.DM_LAIR: ZorkGrandInquisitorRegions.DM_LAIR,
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: ZorkGrandInquisitorRegions.DM_LAIR_INTERIOR,
    ZorkGrandInquisitorStartingLocations.GUE_TECH: ZorkGrandInquisitorRegions.GUE_TECH,
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: ZorkGrandInquisitorRegions.SPELL_LAB,
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: ZorkGrandInquisitorRegions.SUBWAY_HADES,
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: ZorkGrandInquisitorRegions.SUBWAY_FLOOD_CONTROL_DAM,
    ZorkGrandInquisitorStartingLocations.MONASTERY: ZorkGrandInquisitorRegions.MONASTERY,
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: ZorkGrandInquisitorRegions.MONASTERY_EXHIBIT,
}

voxam_cast_game_locations: Dict[
    ZorkGrandInquisitorStartingLocations,
    Tuple[Tuple[str, int], ...]
] = {
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: (
        ("px1j", 0),
        ("ps20", 1),
        ("pe20", 1),
        ("pe2j", 0),
        ("pe30", 1),
        ("pe40", 1),
        ("pe50", 1),
        ("pe5e", 0),
        ("pe5f", 0),
        ("pe6e", 0),
    ),
    ZorkGrandInquisitorStartingLocations.CROSSROADS: (
        ("uc10", 1),
        ("uc20", 1),
        ("uc30", 1),
        ("uc3e", 0),
        ("uc40", 1),
        ("uc4e", 0),
        ("uc50", 1),
        ("uc6e", 0),
    ),
    ZorkGrandInquisitorStartingLocations.DM_LAIR: (
        ("dg10", 1),
        ("dg20", 1),
        ("dg4f", 0),
        ("dg30", 1),
        ("dg3e", 0),
    ),
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: (
        ("dv10", 1),
        ("dv1j", 0),
        ("dw10", 1),
        ("dw1g", 0),
    ),
    ZorkGrandInquisitorStartingLocations.GUE_TECH: (
        ("tr20", 1),
        ("tr1k", 0),
        ("tr1g", 0),
        ("tr2g", 0),
        ("tr50", 1),
        ("tr5e", 0),
        ("tr5f", 0),
        ("tr5g", 0),
        ("tr4g", 0),
        ("tr4f", 0),
        ("th30", 1),
        ("th50", 1),
        ("th60", 1),
        ("th40", 1),
    ),
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: (
        ("tp20", 1),
        ("tp50", 1),
        ("tp10", 1),
        ("tp2f", 0),
        ("tp2g", 0),
        ("tp2e", 0),
        ("tp30", 1),
        ("tp3f", 0),
        ("tp3e", 0),
        ("tp4f", 0),
        ("tp4e", 0),
    ),
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: (
        ("uh10", 1),
        ("uh20", 1),
        ("uh2f", 0),
        ("uh2e", 0),
    ),
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: (
        ("ue10", 1),
        ("ue20", 1),
        ("ue2g", 0),
        ("ue2e", 0),
        ("ue2j", 0),
        ("ue2k", 0),
        ("ue2f", 0),
    ),
    ZorkGrandInquisitorStartingLocations.MONASTERY: (
        ("mt20", 1),
        ("mt1e", 0),
        ("mt1f", 0),
        ("mt2g", 0),
        ("mt2e", 0),
        ("mt30", 1),
    ),
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: (
        ("me10", 1),
        ("me1f", 0),
        ("me1h", 0),
        ("me1g", 0),
        ("me20", 1),
        ("me2h", 0),
        ("me2j", 0),
        ("me5f", 0),
        ("me2m", 0),
    ),
}

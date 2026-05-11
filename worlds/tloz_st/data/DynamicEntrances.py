from .Entrances import ENTRANCES
from .Items import ITEM_GROUPS

# For adding entrances that change based on items, locations, slot_data etc.
# uses all the same conditions as dynamic flags
# "entrance: str name of the STTransition to enter
# "destination": str name of the STTransition to warp to if conditions are true
DYNAMIC_ENTRANCES = {
    # ToS Bounce
    "Exit ToS to snow without source": {
        "entrance": "Tower of Spirits to Snow Realm",
        "destination": "Tower of Spirits to Snow Realm",
        "not_has_groups": ["Tracks: Snow Source"],
        "message": "You don't have the snow source!"
    },
    "Exit ToS to ocean without source": {
        "entrance": "Tower of Spirits to Ocean Realm",
        "destination": "Tower of Spirits to Ocean Realm",
        "not_has_groups": ["Tracks: Ocean Source"],
        "message": "You don't have the Ocean source!"
    },
    "Exit ToS to fire without source": {
        "entrance": "Tower of Spirits to Fire Realm",
        "destination": "Tower of Spirits to Fire Realm",
        "not_has_groups": ["Tracks: Fire Source"],
        "message": "You don't have the Fire source!"
    },

    "Bounce ToS from forest without base prog": {
        "entrance": "Forest Realm to Tower of Spirits",
        "destination": "Forest Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", 2], ["tos_unlock_base_item", 1]],
        "has_items": [("Progressive ToS Section", 0)],
        "message": "You need 1 Progressive ToS Section to enter!"
    },
    "Bounce ToS from forest without base": {
        "entrance": "Forest Realm to Tower of Spirits",
        "destination": "Forest Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", [0, 1]], ["tos_unlock_base_item", 1]],
        "has_items": [("Tower of Spirits Base", 0)],
        "message": "You need the Tower of Spirits Base to enter!"
    },
    "Bounce ToS from snow without base prog": {
        "entrance": "Snow Realm to Tower of Spirits",
        "destination": "Snow Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", 2], ["tos_unlock_base_item", 1]],
        "has_items": [("Progressive ToS Section", 0)],
        "message": "You need 1 Progressive ToS Section to enter!"
    },
    "Bounce ToS from snow without base": {
        "entrance": "Snow Realm to Tower of Spirits",
        "destination": "Snow Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", [0, 1]], ["tos_unlock_base_item", 1]],
        "has_items": [("Tower of Spirits Base", 0)],
        "message": "You need the Tower of Spirits Base to enter!"
    },
    "Bounce ToS from ocean without base prog": {
        "entrance": "Ocean Realm to Tower of Spirits",
        "destination": "Ocean Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", 2], ["tos_unlock_base_item", 1]],
        "has_items": [("Progressive ToS Section", 0)],
        "message": "You need 1 Progressive ToS Section to enter!"
    },
    "Bounce ToS from Ocean without base": {
        "entrance": "Ocean Realm to Tower of Spirits",
        "destination": "Ocean Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", [0, 1]], ["tos_unlock_base_item", 1]],
        "has_items": [("Tower of Spirits Base", 0)],
        "message": "You need the Tower of Spirits Base to enter!"
    },
    "Bounce ToS from Fire without base prog": {
        "entrance": "Fire Realm to Tower of Spirits",
        "destination": "Fire Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", 2], ["tos_unlock_base_item", 1]],
        "has_items": [("Progressive ToS Section", 0)],
        "message": "You need 1 Progressive ToS Section to enter!"
    },
    "Bounce ToS from Fire without base": {
        "entrance": "Fire Realm to Tower of Spirits",
        "destination": "Fire Realm to Tower of Spirits",
        "has_slot_data": [["tos_section_unlocks", [0, 1]], ["tos_unlock_base_item", 1]],
        "has_items": [("Tower of Spirits Base", 0)],
        "message": "You need the Tower of Spirits Base to enter!"
    },

    # Outset pre-glyph bounce
    "Bounce Outset without cannon": {
        "entrance": "Outset to Forest Realm",
        "destination": "Outset to Forest Realm",
        "has_items": [("Cannon", 0)],
        "has_slot_data": [("cannon_logic", 0)],
        "message": "You need Forest Glyph and Cannon to board the train here"
    },
    "Bounce Outset without glyph cannonless": {
        "entrance": "Outset to Forest Realm",
        "destination": "Outset to Forest Realm",
        "not_has_groups": ["Tracks: Forest Glyph"],
        "message": "You need Forest Glyph to board the train here"
    },
    "Bounce Tutorial cannon": {
        "entrance": "Outset to Tutorial",
        "destination": "Outset to Tutorial",
        "has_items": [("Cannon", 0)],
        "has_slot_data": [("cannon_logic", 0)],
        "message": "You need Forest Glyph and Cannon to board the train here"
    },
    "Bounce Tutorial cannonless": {
        "entrance": "Outset to Tutorial",
        "destination": "Outset to Tutorial",
        "not_has_groups": ["Tracks: Forest Glyph"],
        "message": "You need Forest Glyph to board the train here"
    },
    "Bounce Tutorial to rail cannon": {
        "entrance": "Outset to Tutorial",
        "destination": "Forest Realm to Outset",
        "has_slot_data": [("cannon_logic", 0)],
        "has_items": [("Cannon", 1)],
        "has_groups": ["Tracks: Forest Glyph"],
    },
    "Bounce Tutorial to rail cannonless": {
        "entrance": "Outset to Tutorial",
        "destination": "Forest Realm to Outset",
        "has_groups": ["Tracks: Forest Glyph"],
        "has_slot_data": [("cannon_logic", [1, 2, 3])],
    },

    # Portal Bounces
    "Bounce forest portal north": {
        "entrance": "Forest Realm North Portal",
        "destination": "Forest Realm North Portal",
        "not_has_groups": ["Tracks: Snow Glyph"],
        "message": "You don't have the Snow Glyph!"
    },
    "Bounce forest portal north item portal": {
        "entrance": "Forest Realm North Portal",
        "destination": "Forest Realm North Portal",
        "has_items": [("Portal Unlock: Hyrule Castle to Anouki Village", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce forest portal south": {
        "entrance": "Forest Realm South Portal",
        "destination": "Forest Realm South Portal",
        "not_has_groups": ["Tracks: Blizzard Temple Tracks"],
        "message": "You don't have the Blizzard Temple Tracks!"
    },
    "Bounce forest portal south item": {
        "entrance": "Forest Realm South Portal",
        "destination": "Forest Realm South Portal",
        "has_items": [("Portal Unlock: Trading Post to E Snow Realm", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce snow portal east": {
        "entrance": "Snow Realm East Portal",
        "destination": "Snow Realm East Portal",
        "not_has_groups": ["Tracks: Forest Realm SE Portal"],
        "message": "You don't have the Forest Realm SE Portal Tracks!"
    },
    "Bounce snow portal east item": {
        "entrance": "Snow Realm East Portal",
        "destination": "Snow Realm East Portal",
        "has_items": [("Portal Unlock: Trading Post to E Snow Realm", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce sand portal sanc": {
        "entrance": "Sand Realm Sanctuary Portal",
        "destination": "Sand Realm Sanctuary Portal",
        "not_has_groups": ["Tracks: Desert Temple Tracks"],
        "message": "You don't have the Desert Temple Tracks!"
    },
    "Bounce sand portal sanc item": {
        "entrance": "Sand Realm Sanctuary Portal",
        "destination": "Sand Realm Sanctuary Portal",
        "has_items": [("Portal Unlock: Desert Temple to Sand Realm", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce sand portal temple": {
        "entrance": "Sand Realm Temple Portal",
        "destination": "Sand Realm Temple Portal",
        "not_has_groups": ["Tracks: Sand Realm"],
        "message": "You don't have the Sand Realm Tracks!"
    },
    "Bounce sand portal temple item": {
        "entrance": "Sand Realm Temple Portal",
        "destination": "Sand Realm Temple Portal",
        "has_items": [("Portal Unlock: Desert Temple to Sand Realm", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce sand fire portal": {
        "entrance": "Fire Realm Sand Portal",
        "destination": "Fire Realm Sand Portal",
        "not_has_groups": ["Tracks: Marine Temple Tracks"],
        "message": "You don't have the Marine Temple Tracks!"
    },
    "Bounce sand fire portal item": {
        "entrance": "Fire Realm Sand Portal",
        "destination": "Fire Realm Sand Portal",
        "has_items": [("Portal Unlock: Sand Valley to Marine Temple", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce marine temple portal": {
        "entrance": "Ocean Realm Temple Portal",
        "destination": "Ocean Realm Temple Portal",
        "not_has_groups": ["Tracks: Fire Realm Sand Portal"],
        "message": "You don't have the Fire Realm Sand Portal Tracks!"
    },
    "Bounce marine temple portal item": {
        "entrance": "Ocean Realm Temple Portal",
        "destination": "Ocean Realm Temple Portal",
        "has_items": [("Portal Unlock: Sand Valley to Marine Temple", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce snow portal west item": {  # No need for other bounce condition, unlocked with forest glyph
        "entrance": "Snow Realm West Portal",
        "destination": "Snow Realm West Portal",
        "has_slot_data": [["portal_behavior", 2]],
        "has_items": [("Portal Unlock: Hyrule Castle to Anouki Village", 0)],
        "message": "You don't have access to this portal!"
    },
    "Bounce snow portal west tracks": {  # No need for other bounce condition, unlocked with forest glyph
        "entrance": "Snow Realm West Portal",
        "destination": "Snow Realm West Portal",
        "not_has_groups": ["Tracks: Forest Glyph"],
        "message": "You don't have the Forest Glyph!"
    },

    "Bounce icyspring portal": {
        "entrance": "Snow Realm North Portal",
        "destination": "Snow Realm North Portal",
        "not_has_groups": ["Tracks: Mountain Temple Tracks"],
        "message": "You don't have the Mountain Temple Tracks!"
    },
    "Bounce icyspring item": {
        "entrance": "Snow Realm North Portal",
        "destination": "Snow Realm North Portal",
        "has_items": [("Portal Unlock: Icy Spring to Mountain Temple", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce snow portal bridge": {
        "entrance": "Snow Realm Bridge Portal",
        "destination": "Snow Realm Bridge Portal",
        "not_has_groups": ["Tracks: Marine Temple Tracks"],
        "message": "You don't have the Marine Temple Tracks!"
    },
    "Bounce snow bridge portal item": {
        "entrance": "Snow Realm Bridge Portal",
        "destination": "Snow Realm Bridge Portal",
        "has_items": [("Portal Unlock: Snow Bridge to Island Sanctuary", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce island sanc portal": {
        "entrance": "Ocean Realm South Portal",
        "destination": "Ocean Realm South Portal",
        "not_has_groups": ["Tracks: Snow Realm Bridge"],
        "message": "You don't have the Snow Realm Bridge Tracks!"
    },
    "Bounce island sanc portal item": {
        "entrance": "Ocean Realm South Portal",
        "destination": "Ocean Realm South Portal",
        "has_items": [("Portal Unlock: Snow Bridge to Island Sanctuary", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce ocean west portal": {
        "entrance": "Ocean Realm West Portal",
        "destination": "Ocean Realm West Portal",
        "not_has_groups": ["Tracks: Ocean Glyph"],
        "message": "You don't have the Ocean Glyph!"
    },
    "Bounce ocean west portal item": {
        "entrance": "Ocean Realm West Portal",
        "destination": "Ocean Realm West Portal",
        "has_items": [("Portal Unlock: Mayscore to Ocean Portal Tracks", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce mayscore portal": {
        "entrance": "Forest Realm Mayscore Portal",
        "destination": "Forest Realm Mayscore Portal",
        "not_has_groups": ["Tracks: Ocean Portal"],
        "message": "You don't have the Ocean Portal Tracks!"
    },
    "Bounce mayscore portal item": {
        "entrance": "Forest Realm Mayscore Portal",
        "destination": "Forest Realm Mayscore Portal",
        "has_items": [("Portal Unlock: Mayscore to Ocean Portal Tracks", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce mountain portal": {
        "entrance": "Mountain Portal",
        "destination": "Mountain Portal",
        "not_has_groups": ["Tracks: N Icy Spring"],
        "message": "You don't have the N Icy Spring Tracks!"
    },
    "Bounce mountain item": {
        "entrance": "Mountain Portal",
        "destination": "Mountain Portal",
        "has_items": [("Portal Unlock: Icy Spring to Mountain Temple", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce Cave portal": {
        "entrance": "Forest Realm Cave Portal",
        "destination": "Forest Realm Cave Portal",
        "not_has_groups": ["Tracks: Fire Glyph"],
        "message": "You don't have the Fire Glyph!"
    },
    "Bounce Cave portal item": {
        "entrance": "Forest Realm Cave Portal",
        "destination": "Forest Realm Cave Portal",
        "has_items": [("Portal Unlock: Forest Cave to Goron Village", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },

    "Bounce goron portal": {
        "entrance": "Fire Realm Portal",
        "destination": "Fire Realm Portal",
        "not_has_groups": ["Tracks: Forest Realm SW Cave"],
        "message": "You don't have the Forest Realm SW Cave Tracks!"
    },
    "Bounce goron portal item": {
        "entrance": "Fire Realm Portal",
        "destination": "Fire Realm Portal",
        "has_items": [("Portal Unlock: Forest Cave to Goron Village", 0)],
        "has_slot_data": [["portal_behavior", 2]],
        "message": "You don't have access to this portal!"
    },


    # Dark realm options
    "Bounce Dark realm missing endgame requirements": {
        "entrance": "Enter Dark Realm Portal",
        "destination": "Enter Dark Realm Portal",
        "message": "You are missing dark realm requirements",
        "dungeons": False
    },
    "Dark realm Skip dark trains": {
        "entrance": "Enter Dark Realm Portal",
        "destination": "Enter Demon Train",
        "has_slot_data": [["endgame_scope", 1]],
        "dungeons": True
    },
    "Dark realm Skip demon train": {
        "entrance": "Enter Dark Realm Portal",
        "destination": "Enter Cole Fight",
        "has_slot_data": [["endgame_scope", 2]],
        "dungeons": True
    },
    "Dark realm Skip Cole": {
        "entrance": "Enter Dark Realm Portal",
        "destination": "Enter Malladus 1",
        "has_slot_data": [["endgame_scope", 3]],
        "dungeons": True
    },
    "Dark realm Skip Malladus 1": {
        "entrance": "Enter Dark Realm Portal",
        "destination": "Enter Malladus 2",
        "has_slot_data": [["endgame_scope", 4]],
        "dungeons": True
    },

    # ToS Bounces
    "Bounce ToS Section 2": {
        "entrance": "Tower of Spirits Enter Section 2",
        "destination": "Tower of Spirits Enter Section 2",
        "not_has_groups": ["Tracks: Forest Source"],
        "has_slot_data": [["tos_section_unlocks", 1]],
        "message": "You need the Forest Source to enter this section!"
    },
    "Bounce ToS Section 3": {
        "entrance": "Tower of Spirits Enter Section 3",
        "destination": "Tower of Spirits Enter Section 3",
        "not_has_groups": ["Tracks: Snow Source"],
        "has_slot_data": [["tos_section_unlocks", 1]],
        "message": "You need the Snow Source to enter this section!"
    },
    "Bounce ToS Section 4": {
        "entrance": "Tower of Spirits Enter Section 4",
        "destination": "Tower of Spirits Enter Section 4",
        "not_has_groups": ["Tracks: Ocean Source"],
        "has_slot_data": [["tos_section_unlocks", 1]],
        "message": "You need the Ocean Source to enter this section!"
    },
    "Bounce ToS Section 5": {
        "entrance": "Tower of Spirits Enter Section 5",
        "destination": "Tower of Spirits Enter Section 5",
        "not_has_groups": ["Tracks: Fire Source"],
        "has_slot_data": [["tos_section_unlocks", 1]],
        "message": "You need the Fire Source to enter this section!"
    },
    "Bounce OCT 7F cause crash": {
        "entrance": "Marine Temple 7F Exit",
        "destination": "Marine Temple 7F Exit",
        "has_locations": ["Marine Temple 6F Boss Key"],
        "message": "Oops you can't do that, it crashes for some reason"
    },

    # ToS Blue Warp shortcuts
    "Exit ToS 3F": {
        "entrance": "ToS 3F Blue Portal",
        "destination": "_connected_dungeon_entrance",
    },
    "Exit ToS 7F": {
        "entrance": "ToS 7F Blue Portal",
        "destination": "_connected_dungeon_entrance",
    },
    "Exit ToS 12F": {
        "entrance": "ToS 12F Blue Portal",
        "destination": "_connected_dungeon_entrance",
    },
    "Exit ToS 17F": {
        "entrance": "ToS 17F Blue Portal",
        "destination": "_connected_dungeon_entrance",
    },
    "Exit ToS 24F": {
        "entrance": "ToS 24F Blue Portal",
        "destination": "_connected_dungeon_entrance",
    },
    "Exit ToS 23F": {
        "entrance": "ToS 23F Blue Warp Before Staven",
        "destination": "_connected_dungeon_entrance",
    },
    "Skeldritch avoid post fight stuffs": {
        "entrance": "Desert Temple Enter Post-Fight",
        "destination": "Skeldritch Exit",
        "not_has_locations": ["Desert Temple Dungeon Reward"],
    },
    "Fire realm bounce snow realm without btt": {
        "entrance": "Fire Realm East Tower",
        "destination": "Fire Realm East Tower",
        "not_has_groups": ["Tracks: Blizzard Temple Tracks"],
        "message": "The game crashes here without the blizzard temple tracks. Sorry!"
    },
    "Prevent softlock in papuzia south": {
        "entrance": "South Papuzia North",
        "destination": "Papuzia NW House"
    },
    "Prevent softlock in icy spring with ferrus": {
        "entrance": "Icy Spring Train",
        "destination": "Fire Realm Goron Village",
        "not_has_groups": ["Tracks: Blizzard Temple Tracks"],
        "message": "You got here with Ferrus, putting you somewhere safe"
    },
    # ToS Shortcuts: Open
    "ToS Staircase shortcut open": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 5",
        "has_slot_data": [("tos_section_unlocks", 0), ("tos_shortcuts", 1)],
    },
    # ToS Shortcuts: Sources
    "ToS Staircase shortcut fire source": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 5",
        "has_slot_data": [("tos_section_unlocks", 1), ("tos_shortcuts", 1)],
        "has_groups": ["Tracks: Fire Source"]
    },
    "ToS Staircase shortcut ocean source": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 4",
        "has_slot_data": [("tos_section_unlocks", 1), ("tos_shortcuts", 1)],
        "not_has_groups": ["Tracks: Fire Source"],
        "has_groups": ["Tracks: Ocean Source"],
    },
    "ToS Staircase shortcut snow source": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 3",
        "has_slot_data": [("tos_section_unlocks", 1), ("tos_shortcuts", 1)],
        "not_has_groups": ["Tracks: Fire Source", "Tracks: Ocean Source"],
        "has_groups": ["Tracks: Snow Source"],
    },
    "ToS Staircase shortcut forest source": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 2",
        "has_slot_data": [("tos_section_unlocks", 1), ("tos_shortcuts", 1)],
        "not_has_groups": ["Tracks: Fire Source", "Tracks: Ocean Source", "Tracks: Snow Source"],
        "has_groups": ["Tracks: Forest Source"],
    },
    "ToS Staircase shortcut no source": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 1",
        "has_slot_data": [("tos_section_unlocks", 1), ("tos_shortcuts", 1)],
        "not_has_groups": ["Tracks: Fire Source", "Tracks: Ocean Source",
                           "Tracks: Snow Source", "Tracks: Forest Source"],
    },
    # ToS Shortcuts: Progressive no base
    "ToS Staircase shortcut progressive nb 4": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 5",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 0), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 4, "has_exact")],
    },
    "ToS Staircase shortcut progressive nb 3": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 4",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 0), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 3, "has_exact")],
    },
    "ToS Staircase shortcut progressive nb 2": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 3",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 0), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 2, "has_exact")],
    },
    "ToS Staircase shortcut progressive nb 1": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 2",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 0), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 1, "has_exact")],
    },
    "ToS Staircase shortcut progressive nb 0": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 1",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 0), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 0)],
    },
    # ToS Shortcuts: Progressive base
    "ToS Staircase shortcut progressive 5": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 5",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 1), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 5, "has_exact")],
    },
    "ToS Staircase shortcut progressive 4": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 4",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 1), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 4, "has_exact")],
    },
    "ToS Staircase shortcut progressive 3": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 3",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 1), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 3, "has_exact")],
    },
    "ToS Staircase shortcut progressive 2": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 2",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 1), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 2, "has_exact")],
    },
    "ToS Staircase shortcut progressive 1": {
        "entrance": "ToS Staircase Exit",
        "destination": "Tower of Spirits Enter Section 1",
        "has_slot_data": [("tos_section_unlocks", 2), ("tos_unlock_base_item", 1), ("tos_shortcuts", 1)],
        "has_items": [("Progressive ToS Section", 1, "has_exact")],
    },
}

# Reorganize above data to the form {scene: data} or something
# DYNAMIC_ENTRANCES_BY_SCENE = {}
# for name, data in DYNAMIC_ENTRANCES.items():
#     data["name"] = name
#     entrance_data = ENTRANCES[data["entrance"]]
#     if data["destination"] == "_connected_dungeon_entrance":
#         destination_data = None
#     else:
#         destination_data = ENTRANCES[data["destination"]]
#
#     entrance_scene = entrance_data.scene
#
#     # Save er_in_scene values in data
#     data["detect_data"] = entrance_data
#     data["exit_data"] = destination_data
#     DYNAMIC_ENTRANCES_BY_SCENE.setdefault(entrance_scene, {})
#     DYNAMIC_ENTRANCES_BY_SCENE[entrance_scene][name] = data
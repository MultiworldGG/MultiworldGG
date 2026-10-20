from __future__ import annotations

from collections import Counter

from .location_display_names import location_first_name


# Native CollectableItemPickup identities. Alternate Flea Festival state
# copies share the same scene, asset and position and therefore represent one
# physical source apiece.
MINOR_PICKUP_SOURCE: tuple[tuple[str, str, str, float, float], ...] = (
    ("Hunter's March - Rosary Necklace", 'ant_04_left', 'Rosary_Set_Medium', 85.02, 26.99),
    ('Putrified Ducts - Frayed Rosary String', 'aqueduct_01', 'Rosary_Set_Frayed', 256.19, 14.67),
    ('Fleatopia - Rosary Necklace', 'aqueduct_05_festival', 'Rosary_Set_Medium', 152.783, 16.2396),
    ('Fleatopia - Rosary String', 'aqueduct_05_festival', 'Rosary_Set_Small', 154.043, 15.9796),
    ('Memorium - Shard Bundle', 'arborium_11', 'Shard Pouch', 211.22, 10.27),
    ('The Marrow (Flea Caravan Passage) - Frayed Rosary String', 'bone_10', 'Rosary_Set_Frayed', 98.9849, 41.3206),
    ('Deep Docks - Frayed Rosary String', 'bone_east_04b', 'Rosary_Set_Frayed', 6.462, 87.1857),
    ('Far Fields - Rosary String', 'bone_east_14', 'Rosary_Set_Small', 13.82, 7.461),
    ('Far Fields - Pale Rosary Necklace', 'bone_east_24', 'Rosary_Set_Huge_White', 248.93, 67.4),
    ('Cogwork Core - Pristine Core', 'cog_07', 'Pristine Core', 0.0, 0.0),
    ('Cogwork Core - Shard Bundle', 'cog_10', 'Shard Pouch', 6.78, 44.67),
    ('Blasted Steps - Frayed Rosary String', 'coral_03', 'Rosary_Set_Frayed', 38.64, 5.53),
    ('Blasted Steps - Beast Shard', 'coral_36', 'Great Shard', 20.0542, 48.5738),
    ('Wormways - Frayed Rosary String', 'crawl_02', 'Rosary_Set_Frayed', 3.14, 142.3655),
    ('Deep Docks - Shard Bundle #1', 'dock_02', 'Shard Pouch', 38.79, 3.5175),
    ('Deep Docks - Beast Shard', 'dock_11', 'Great Shard', 100.63, 6.28),
    ("Sinner's Road - Frayed Rosary String", 'dust_01', 'Rosary_Set_Frayed', 76.43, 2.7178),
    ("Sinner's Road - Shard Bundle", 'dust_06', 'Shard Pouch', 26.11, 96.25),
    ('Greymor - totally free to take shell shard cache at the top', 'greymoor_05', 'Shard Pouch', 59.01, 62.74),
    ('Greymoor that shard bundle i hate at the left side of the room', 'greymoor_12', 'Shard Pouch', 61.29, 14.4),
    ('Greymoor - Frayed Rosary String from dead bug guarded by rat', 'greymoor_15', 'Rosary_Set_Frayed', 64.41, 24.21),
    ('Greymoor - Frayed Rosary String in tiny ass hole above left lower entrance', 'greymoor_15b', 'Rosary_Set_Frayed', 91.86, 35.26),
    ('High Halls - Pale Rosary Necklace', 'hang_06_bank', 'Rosary_Set_Huge_White', 73.41, 35.3895),
    ('High Halls - Frayed Rosary String', 'hang_16', 'Rosary_Set_Frayed', 68.15, 6.38),
    ('Whispering Vaults - Heavy Rosary Necklace', 'library_02', 'Rosary_Set_Large', 76.437, 48.02),
    ('Songclave - Heavy Rosary Necklace', 'library_09', 'Rosary_Set_Large', 14.08, 36.42),
    ('Whispering Vaults - Shard Bundle', 'library_12', 'Shard Pouch', 126.39, 24.4143),
    ('Bone Bottom (Silkspear Passage) - Frayed Rosary String', 'mosstown_02', 'Rosary_Set_Frayed', 35.32, 40.27),
    ('Deep Docks - Shard Bundle #2', 'room_forge', 'Shard Pouch', 5.08, 37.38),
    ('Bilewater - Frayed Rosary String', 'shadow_02', 'Rosary_Set_Frayed', 49.21, 161.48),
    ('Shellwood - Frayed Rosary String', 'shellwood_01', 'Rosary_Set_Frayed', 48.99, 23.27),
    ('Shellwood - Rosary String #1', 'shellwood_01b', 'Rosary_Set_Small', 33.13, 72.38),
    ('Shellwood - Shard Bundle', 'shellwood_13', 'Shard Pouch', 82.2928, 67.2101),
    ('Shellwood - Rosary String #2', 'shellwood_25', 'Rosary_Set_Small', 83.3, 25.4172),
    ('The Slab - Frayed Rosary String #1', 'slab_02', 'Rosary_Set_Frayed', 53.4572, 21.2107),
    ('The Slab - Shard Bundle', 'slab_04', 'Shard Pouch', 9.4863, 15.6907),
    ('The Slab - Frayed Rosary String #2', 'slab_18', 'Rosary_Set_Frayed', 17.2344, 21.2003),
    ('The Slab - Frayed Rosary String #3', 'slab_22', 'Rosary_Set_Frayed', 28.3, 30.39),
    ('Choral Chambers - Heavy Rosary Necklace', 'song_04', 'Rosary_Set_Large', 121.49, 37.57),
    ('Choral Chambers - Rosary Necklace #1', 'song_07', 'Rosary_Set_Medium', 3.83, 4.91),
    ('Choral Chambers - Rosary Necklace #2', 'song_09', 'Rosary_Set_Medium', 39.38, 8.2749),
    ('Moss Grotto - Frayed Rosary String', 'tut_01', 'Rosary_Set_Frayed', 43.96, 20.43),
    ('Underworks - Shard Bundle #1', 'under_03', 'Shard Pouch', 4.5876, 6.2287),
    ('Underworks - Frayed Rosary String #1', 'under_07c', 'Rosary_Set_Frayed', 75.57, 76.08),
    ('Underworks - Frayed Rosary String #2', 'under_12', 'Rosary_Set_Frayed', 33.13, 10.29),
    ('Underworks - Pristine Core', 'under_17', 'Pristine Core', 75.44, 23.37),
    ('Underworks - Shard Bundle #2', 'under_18', 'Shard Pouch', 34.14, 34.3),
    ('Wisp Thicket - Rosary Necklace', 'wisp_02', 'Rosary_Set_Medium', 111.32, 37.99),
    ('Greymoor - Yanarby stash with a Frayed Rosary', 'wisp_03', 'Rosary_Set_Frayed', 62.89, 35.37),
)

MINOR_PICKUP_REWARD_BY_ASSET: dict[str, str] = {
    'Rosary_Set_Frayed': 'Frayed Rosary String',
    'Rosary_Set_Small': 'Rosary String',
    'Rosary_Set_Medium': 'Rosary Necklace',
    'Rosary_Set_Large': 'Heavy Rosary Necklace',
    'Rosary_Set_Huge_White': 'Pale Rosary Necklace',
    'Shard Pouch': 'Shard Bundle',
    'Great Shard': 'Beast Shard',
    'Pristine Core': 'Pristine Core',
}


WISH_CURRENCY_REWARDS: dict[str, str] = {
    'Wish: Fine Pins': 'Heavy Rosary Necklace',
    'Wish: Garb of the Pilgrims': 'Rosary Necklace',
    'Wish: Silver Bells': 'Rosary Necklace',
    'Wish: The Terrible Tyrant': 'Heavy Rosary Necklace',
    'Wish: Cloaks of the Choir': 'Heavy Rosary Necklace',
}

SCRIPTED_MINOR_REWARDS: dict[str, str] = {
    **WISH_CURRENCY_REWARDS,
    'Loddie - Heavy Rosary Necklace': 'Heavy Rosary Necklace',
}


MINOR_PICKUP_LOCATION_NAMES: tuple[str, ...] = tuple(
    location_first_name(location_name)
    for location_name, *_identity in MINOR_PICKUP_SOURCE
)
ACTIVE_MINOR_PICKUP_LOCATION_NAMES: tuple[str, ...] = tuple(
    name for name in MINOR_PICKUP_LOCATION_NAMES
    if name != "Whispering Vaults - Heavy Rosary Necklace"
)
MINOR_PICKUP_REWARD_BY_LOCATION: dict[str, str] = {
    location_first_name(location_name):
        MINOR_PICKUP_REWARD_BY_ASSET[asset_name]
    for location_name, _scene, asset_name, _x, _y in MINOR_PICKUP_SOURCE
    if location_name in ACTIVE_MINOR_PICKUP_LOCATION_NAMES
}
MINOR_PICKUP_REWARD_COUNTS: dict[str, int] = dict(
    Counter(MINOR_PICKUP_REWARD_BY_LOCATION.values())
)

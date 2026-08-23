from enum import IntEnum
from typing import TYPE_CHECKING, Dict, List, Tuple
from BaseClasses import Entrance, EntranceType, Region
from entrance_rando import (ERPlacementState, EntranceRandomizationError, disconnect_entrance_for_randomization,
                            randomize_entrances)

from .data import data
from .options import (ShuffleBuildingEntrances, ShuffleDropdowns, ShuffleDungeonEntrances, ShuffleWarpTiles)
from .universal_tracker import ut_set_entrances

if TYPE_CHECKING:
    from .world import PokemonFRLGWorld

MAX_GER_ATTEMPTS = 40

POKEMON_CENTER_ENTRANCES = [
    "Player's House Entrance", "Viridian Pokemon Center Entrance", "Pewter Pokemon Center Entrance",
    "Route 4 Pokemon Center Entrance", "Cerulean Pokemon Center Entrance", "Vermilion Pokemon Center Entrance",
    "Route 10 Pokemon Center Entrance", "Lavender Pokemon Center Entrance", "Celadon Pokemon Center Entrance",
    "Fuchsia Pokemon Center Entrance", "Saffron Pokemon Center Entrance", "Cinnabar Pokemon Center Entrance",
    "Indigo Plateau Pokemon Center Entrance", "One Island Pokemon Center Entrance",
    "Two Island Pokemon Center Entrance", "Three Island Pokemon Center Entrance", "Four Island Pokemon Center Entrance",
    "Five Island Pokemon Center Entrance", "Six Island Pokemon Center Entrance", "Seven Island Pokemon Center Entrance"
]

POKEMON_CENTER_EXITS = [
    "Player's House 1F Exit", "Viridian Pokemon Center 1F Exit", "Pewter Pokemon Center 1F Exit",
    "Route 4 Pokemon Center 1F Exit", "Cerulean Pokemon Center 1F Exit", "Vermilion Pokemon Center 1F Exit",
    "Route 10 Pokemon Center 1F Exit", "Lavender Pokemon Center 1F Exit", "Celadon Pokemon Center 1F Exit",
    "Fuchsia Pokemon Center 1F Exit", "Saffron Pokemon Center 1F Exit", "Cinnabar Pokemon Center 1F Exit",
    "Indigo Plateau Pokemon Center 1F Exit", "One Island Pokemon Center 1F Exit", "Two Island Pokemon Center 1F Exit",
    "Three Island Pokemon Center 1F Exit", "Four Island Pokemon Center 1F Exit", "Five Island Pokemon Center 1F Exit",
    "Six Island Pokemon Center 1F Exit", "Seven Island Pokemon Center 1F Exit"
]

GYM_ENTRANCES = [
    "Viridian Gym Entrance", "Pewter Gym Entrance", "Cerulean Gym Entrance", "Vermilion Gym Entrance",
    "Celadon Gym Entrance", "Fuchsia Gym Entrance", "Saffron Gym Entrance", "Cinnabar Gym Entrance"
]

GYM_EXITS = [
    "Viridian Gym Exit", "Pewter Gym Exit", "Cerulean Gym Exit", "Vermilion Gym Exit", "Celadon Gym Exit",
    "Fuchsia Gym Exit", "Saffron Gym Exit", "Cinnabar Gym Exit"
]

MART_ENTRANCES = [
    "Viridian Poke Mart Entrance", "Pewter Poke Mart Entrance", "Cerulean Poke Mart Entrance",
    "Vermilion Poke Mart Entrance", "Lavender Poke Mart Entrance", "Fuchsia Poke Mart Entrance",
    "Saffron Poke Mart Entrance", "Cinnabar Poke Mart Entrance", "Three Island Poke Mart Entrance",
    "Four Island Poke Mart Entrance", "Six Island Poke Mart Entrance", "Seven Island Poke Mart Entrance"
]

MART_EXITS = [
    "Viridian Poke Mart Exit", "Pewter Poke Mart Exit", "Cerulean Poke Mart Exit", "Vermilion Poke Mart Exit",
    "Lavender Poke Mart Exit", "Fuchsia Poke Mart Exit", "Saffron Poke Mart Exit", "Cinnabar Poke Mart Exit",
    "Three Island Poke Mart Exit", "Four Island Poke Mart Exit", "Six Island Poke Mart Exit",
    "Seven Island Poke Mart Exit"
]

HARBOR_ENTRANCES = [
    "One Island Harbor Entrance", "Two Island Harbor Entrance", "Three Island Harbor Entrance",
    "Four Island Harbor Entrance", "Five Island Harbor Entrance", "Six Island Harbor Entrance",
    "Seven Island Harbor Entrance", "Navel Rock Harbor Entrance", "Birth Island Harbor Entrance"
]

HARBOR_EXITS = [
    "One Island Harbor Exit", "Two Island Harbor Exit", "Three Island Harbor Exit", "Four Island Harbor Exit",
    "Five Island Harbor Exit", "Six Island Harbor Exit", "Seven Island Harbor Exit", "Navel Rock Harbor Exit",
    "Birth Island Harbor Exit"
]

SINGLE_BUILDING_ENTRANCES = [
    "Rival's House Entrance", "Professor Oak's Lab Entrance", "Viridian Nickname House Entrance",
    "Viridian School Entrance", "Route 2 Trade House Entrance", "Pewter Museum West Entrance",
    "Pewter Museum East Entrance", "Pewter Nidoran House Entrance", "Pewter Info House Entrance",
    "Cerulean Trade House Entrance", "Bike Shop Entrance", "Wonder News House Entrance",
    "Berry Powder Man's House Entrance", "Sea Cottage Entrance", "Route 5 Pokemon Day Care Entrance",
    "Vermilion Fishing House Entrance", "Pokemon Fan Club Entrance", "Vermilion Trade House Entrance",
    "Vermilion Pidgey House Entrance", "Volunteer Pokemon House Entrance", "Lavender Cubone House Entrance",
    "Name Rater's House Entrance", "Celadon Game Corner Entrance", "Celadon Condominiums Front Entrance",
    "Celadon Condominiums Back Entrance", "Celadon Game Corner Prize Room Entrance", "Celadon Restaurant Entrance",
    "Celadon Rocket House Entrance", "Celadon Hotel Entrance", "Route 12 Fishing House Entrance",
    "Route 16 Fly House Entrance", "Safari Zone Warden's House Entrance", "Safari Zone Office Entrance",
    "Bill's Grandpa's House Entrance", "Move Deleter's House Entrance", "Copycat's House Entrance",
    "Saffron Dojo Entrance", "Saffron Pidgey House Entrance", "Mr. Psychic's House Entrance",
    "Pokemon Trainer Fan Club Entrance", "Pokemon Lab Entrance", "One Island Old Couple's House Entrance",
    "One Island Lass' House Entrance", "Ember Spa Entrance", "Two Island Game Corner Entrance",
    "Move Maniac's House Entrance", "Starter Tutor's House Entrance", "Lostelle's House Entrance",
    "Sabrina Fan's House Entrance", "Three Island Beauty's House Entrance",
    "Three Island Worried Father's House Entrance", "Lostelle's Friend's House Entrance",
    "Four Island Pokemon Day Care Entrance", "Move Tutor's House Entrance", "Lorelei's House Entrance",
    "Sticker Man's House Entrance", "Five Island Couple's House Entrance", "Five Island Old Man's House Entrance",
    "Selphy's House Entrance", "Six Island Old Man's House Entrance", "Water Path Heracross Woman's House Entrance",
    "Water Path Man's House Entrance", "Seven Island Trainer Battle House Entrance", "Tanoby Key Entrance",
    "Sevault Canyon Chansey House Entrance", "Trainer Tower Entrance"
]

SINGLE_BUILDING_EXITS = [
    "Rival's House Exit", "Professor Oak's Lab Exit", "Viridian Nickname House Exit", "Viridian School Exit",
    "Route 2 Trade House Exit", "Pewter Museum 1F West Exit", "Pewter Museum 1F East Exit",
    "Pewter Nidoran House Exit", "Pewter Info House Exit", "Cerulean Trade House Exit", "Bike Shop Exit",
    "Wonder News House Exit", "Berry Powder Man's House Exit", "Sea Cottage Exit", "Route 5 Pokemon Day Care Exit",
    "Vermilion Fishing House Exit", "Pokemon Fan Club Exit", "Vermilion Trade House Exit",
    "Vermilion Pidgey House Exit", "Volunteer Pokemon House Exit", "Lavender Cubone House Exit",
    "Name Rater's House Exit", "Celadon Game Corner Exit", "Celadon Condominiums 1F Front Exit",
    "Celadon Condominiums 1F Back Exit", "Celadon Game Corner Prize Room Exit", "Celadon Restaurant Exit",
    "Celadon Rocket House Exit", "Celadon Hotel Exit", "Route 12 Fishing House Exit", "Route 16 Fly House Exit",
    "Safari Zone Warden's House Exit", "Safari Zone Office Exit", "Bill's Grandpa's House Exit",
    "Move Deleter's House Exit", "Copycat's House 1F Exit", "Saffron Dojo Exit", "Saffron Pidgey House Exit",
    "Mr. Psychic's House Exit", "Pokemon Trainer Fan Club Exit", "Pokemon Lab Exit",
    "One Island Old Couple's House Exit", "One Island Lass' House Exit", "Ember Spa Exit",
    "Two Island Game Corner Exit", "Move Maniac's House Exit", "Starter Tutor's House Exit", "Lostelle's House Exit",
    "Sabrina Fan's House Exit", "Three Island Beauty's House Exit", "Three Island Worried Father's House Exit",
    "Lostelle's Friend's House Exit", "Four Island Pokemon Day Care Exit", "Move Tutor's House Exit",
    "Lorelei's House Exit", "Sticker Man's House Exit", "Five Island Couple's House Exit",
    "Five Island Old Man's House Exit", "Selphy's House Exit", "Six Island Old Man's House Exit",
    "Water Path Heracross Woman's House Exit", "Water Path Man's House Exit", "Seven Island Trainer Battle House Exit",
    "Tanoby Key Exit", "Sevault Canyon Chansey House Exit", "Trainer Tower Lobby Exit"
]

MULTI_BUILDING_ENTRANCES = [
    "Route 22 Gate South Entrance", "Route 22 Gate North Entrance", "Viridian Forest South Gate Entrance",
    "Viridian Forest North Gate Entrance", "Route 2 Gate North Entrance", "Route 2 Gate South Entrance",
    "Badge Guy's House Front Entrance", "Badge Guy's House Back Entrance", "Robbed House Front Entrance",
    "Robbed House Back Entrance", "Route 5 Gate North Entrance", "Route 5 Gate South Entrance",
    "Underground Path North Entrance", "Underground Path South Entrance", "Route 6 Gate South Entrance",
    "Route 6 Gate North Entrance", "Route 11 Gate West Entrance", "Route 11 Gate East Entrance",
    "Route 8 Gate East Entrance", "Route 8 Gate West Entrance", "Underground Path East Entrance",
    "Underground Path West Entrance", "Route 7 Gate West Entrance", "Route 7 Gate East Entrance",
    "Celadon Department Store West Entrance", "Celadon Department Store East Entrance", "Route 12 Gate North Entrance",
    "Route 12 Gate South Entrance", "Route 15 Gate East Entrance", "Route 15 Gate West Entrance",
    "Route 16 Gate Northeast Entrance", "Route 16 Gate Northwest Entrance", "Route 16 Gate Southeast Entrance",
    "Route 16 Gate Southwest Entrance", "Route 18 Gate West Entrance", "Route 18 Gate East Entrance",
    "Fuchsia Fishing House Front Entrance", "Fuchsia Fishing House Back Entrance", "Three Isle Path West Entrance",
    "Three Isle Path East Entrance"
]

MULTI_BUILDING_EXITS = [
    "Route 22 Gate South Exit", "Route 22 Gate North Exit", "Viridian Forest South Gate South Exit",
    "Viridian Forest North Gate North Exit", "Route 2 Gate North Exit", "Route 2 Gate South Exit",
    "Badge Guy's House Front Exit", "Badge Guy's House Back Exit", "Robbed House Front Exit", "Robbed House Back Exit",
    "Route 5 Gate North Exit", "Route 5 Gate South Exit", "Underground Path 1F North Exit",
    "Underground Path 1F South Exit", "Route 6 Gate South Exit", "Route 6 Gate North Exit",
    "Route 11 Gate 1F West Exit", "Route 11 Gate 1F East Exit", "Route 8 Gate East Exit", "Route 8 Gate West Exit",
    "Underground Path 1F East Exit", "Underground Path 1F West Exit", "Route 7 Gate West Exit",
    "Route 7 Gate East Exit", "Celadon Department Store 1F West Exit", "Celadon Department Store 1F East Exit",
    "Route 12 Gate 1F North Exit", "Route 12 Gate 1F South Exit", "Route 15 Gate 1F East Exit",
    "Route 15 Gate 1F West Exit", "Route 16 Gate 1F Northeast Exit", "Route 16 Gate 1F Northwest Exit",
    "Route 16 Gate 1F Southeast Exit", "Route 16 Gate 1F Southwest Exit", "Route 18 Gate 1F West Exit",
    "Route 18 Gate 1F East Exit", "Fuchsia Fishing House Front Exit", "Fuchsia Fishing House Back Exit",
    "Three Isle Path West Exit", "Three Isle Path East Exit"
]

SINGLE_DUNGEON_ENTRANCES = [
    "Vermilion Harbor Entrance", "Pokemon Tower Entrance", "Rocket Hideout Entrance", "Safari Zone Lobby Entrance",
    "Silph Co. Entrance", "Pokemon Mansion Entrance", "Cerulean Cave Entrance", "Navel Rock Entrance",
    "Mt. Ember Entrance", "Berry Forest Entrance", "Icefall Cave Entrance", "Rocket Warehouse Entrance",
    "Lost Cave Entrance", "Dotted Hole Entrance", "Altering Cave Entrance", "Viapois Chamber Entrance",
    "Rixy Chamber Entrance", "Scufib Chamber Entrance", "Dilford Chamber Entrance", "Weepth Chamber Entrance",
    "Liptoo Chamber Entrance", "Monean Chamber Entrance"
]

SINGLE_DUNGEON_EXITS = [
    "S.S. Anne Exterior Exit", "Pokemon Tower 1F Exit", "Rocket Hideout B1F Northwest Stairs",
    "Safari Zone Lobby Exit", "Silph Co. 1F Exit", "Pokemon Mansion 1F West Exit", "Cerulean Cave 1F Exit",
    "Navel Rock 1F Exit", "Mt. Ember Exterior Exit", "Berry Forest Exit", "Icefall Cave Front South Exit",
    "Rocket Warehouse Exit", "Lost Cave 1F Exit", "Dotted Hole 1F Exit", "Altering Cave Exit", "Viapois Chamber Exit",
    "Rixy Chamber Exit", "Scufib Chamber Exit", "Dilford Chamber Exit", "Weepth Chamber Exit", "Liptoo Chamber Exit",
    "Monean Chamber Exit"
]

MULTI_DUNGEON_ENTRANCES = [
    "Viridian Forest South Gate North Exit", "Viridian Forest North Gate South Exit", "Mt. Moon West Entrance",
    "Mt. Moon East Entrance", "Diglett's Cave North Entrance", "Diglett's Cave South Entrance",
    "Rock Tunnel North Entrance", "Rock Tunnel South Entrance", "Power Plant Front Entrance",
    "Power Plant Back Entrance", "Seafoam Islands North Entrance", "Seafoam Islands South Entrance",
    "Victory Road West Entrance", "Victory Road East Entrance", "Pattern Bush West Entrance",
    "Pattern Bush East Entrance"
]

MULTI_DUNGEON_EXITS = [
    "Viridian Forest South Exit", "Viridian Forest North Exit", "Mt. Moon 1F Exit",
    "Mt. Moon B1F East Ladder (Fourth Tunnel)", "Diglett's Cave 1F North Exit", "Diglett's Cave 1F South Exit",
    "Rock Tunnel 1F North Ladder", "Rock Tunnel 1F Exit", "Power Plant Front Exit", "Power Plant Back Exit",
    "Seafoam Islands 1F West Exit", "Seafoam Islands 1F East Exit", "Victory Road 1F Exit", "Victory Road 2F Exit",
    "Pattern Bush West Exit", "Pattern Bush East Exit"
]

INTERIOR_WARPS = [
    "Pewter Museum 1F Stairs", "Pewter Museum 2F Stairs", "Mt. Moon 1F Northwest Ladder",
    "Mt. Moon 1F Center Ladder (Left)", "Mt. Moon 1F Center Ladder (Right)",
    "Mt. Moon B1F Northeast Ladder (First Tunnel)", "Mt. Moon B1F Southwest Ladder (First Tunnel)",
    "Mt. Moon B1F East Ladder (Second Tunnel)", "Mt. Moon B1F West Ladder (Second Tunnel)",
    "Mt. Moon B1F Northwest Ladder (Third Tunnel)", "Mt. Moon B1F Southeast Ladder (Third Tunnel)",
    "Mt. Moon B1F West Ladder (Fourth Tunnel)", "Mt. Moon B2F South Ladder", "Mt. Moon B2F Northeast Ladder",
    "Mt. Moon B2F Center Ladder", "Mt. Moon B2F Northwest Ladder", "Underground Path 1F North Stairs",
    "Underground Path B1F North Stairs", "Underground Path B1F South Stairs", "Underground Path 1F South Stairs",
    "S.S. Anne Entrance", "S.S. Anne 1F Corridor Northwest Stairs", "S.S. Anne Kitchen Entrance", "S.S. Anne Exit",
    "S.S. Anne 1F Corridor Southeast Stairs", "S.S. Anne 1F Room 1 Entrance", "S.S. Anne 1F Room 2 Entrance",
    "S.S. Anne 1F Room 3 Entrance", "S.S. Anne 1F Room 4 Entrance", "S.S. Anne 1F Room 5 Entrance",
    "S.S. Anne 1F Room 7 Entrance", "S.S. Anne 1F Room 6 Entrance", "S.S. Anne Kitchen Exit",
    "S.S. Anne 1F Room 1 Exit", "S.S. Anne 1F Room 2 Exit", "S.S. Anne 1F Room 3 Exit", "S.S. Anne 1F Room 4 Exit",
    "S.S. Anne 1F Room 5 Exit", "S.S. Anne 1F Room 6 Exit", "S.S. Anne 1F Room 7 Exit", "S.S. Anne B1F Corridor Stairs",
    "S.S. Anne B1F Room 1 Entrance", "S.S. Anne B1F Room 2 Entrance", "S.S. Anne B1F Room 3 Entrance",
    "S.S. Anne B1F Room 4 Entrance", "S.S. Anne B1F Room 5 Entrance", "S.S. Anne B1F Room 1 Exit",
    "S.S. Anne B1F Room 2 Exit", "S.S. Anne B1F Room 3 Exit", "S.S. Anne B1F Room 4 Exit", "S.S. Anne B1F Room 5 Exit",
    "S.S. Anne 2F Corridor Northwest Stairs", "S.S. Anne 2F Corridor Southwest Stairs",
    "S.S. Anne 2F Corridor Northeast Stairs", "S.S. Anne 2F Room 1 Entrance", "S.S. Anne 2F Room 2 Entrance",
    "S.S. Anne 2F Room 3 Entrance", "S.S. Anne 2F Room 4 Entrance", "S.S. Anne 2F Room 5 Entrance",
    "S.S. Anne 2F Room 6 Entrance", "S.S. Anne 2F Room 1 Exit", "S.S. Anne 2F Room 2 Exit", "S.S. Anne 2F Room 3 Exit",
    "S.S. Anne 2F Room 4 Exit", "S.S. Anne 2F Room 5 Exit", "S.S. Anne 2F Room 6 Exit", "S.S. Anne 3F Corridor Exit",
    "S.S. Anne 3F Corridor Stairs", "S.S. Anne Deck Exit", "S.S. Anne Captain's Office Stairs",
    "Diglett's Cave 1F South Ladder", "Diglett's Cave B1F Northwest Ladder", "Diglett's Cave B1F Southeast Ladder",
    "Diglett's Cave 1F North Ladder", "Route 11 Gate 1F Stairs", "Route 11 Gate 2F Stairs",
    "Rock Tunnel 1F Northeast Ladder", "Rock Tunnel 1F Northwest Ladder", "Rock Tunnel 1F Center Ladder",
    "Rock Tunnel 1F East Ladder", "Rock Tunnel B1F Southeast Ladder", "Rock Tunnel B1F Northeast Ladder",
    "Rock Tunnel B1F Center Ladder", "Rock Tunnel B1F Northwest Ladder", "Underground Path 1F East Stairs",
    "Underground Path B1F East Stairs", "Underground Path B1F West Stairs", "Underground Path 1F West Stairs",
    "Celadon Department Store 1F Stairs", "Celadon Department Store 2F West Stairs",
    "Celadon Department Store 2F East Stairs", "Celadon Department Store 3F East Stairs",
    "Celadon Department Store 3F West Stairs", "Celadon Department Store 4F West Stairs",
    "Celadon Department Store 4F East Stairs", "Celadon Department Store 5F East Stairs",
    "Celadon Department Store 5F West Stairs", "Celadon Department Store Roof Exit",
    "Celadon Condominiums 1F Northeast Stairs", "Celadon Condominiums 1F Northwest Stairs",
    "Celadon Condominiums 2F Northeast Stairs (Left)", "Celadon Condominiums 2F Northeast Stairs (Right)",
    "Celadon Condominiums 2F Northwest Stairs (Right)", "Celadon Condominiums 2F Northwest Stairs (Left)",
    "Celadon Condominiums 3F Northeast Stairs (Right)", "Celadon Condominiums 3F Northeast Stairs (Left)",
    "Celadon Condominiums 3F Northwest Stairs (Left)", "Celadon Condominiums 3F Northwest Stairs (Right)",
    "Celadon Condominiums Roof Northeast Stairs", "Celadon Condominiums Roof Northwest Stairs",
    "Celadon Condominiums Roof Room Entrance", "Celadon Condominiums Roof Room Exit",
    "Rocket Hideout B1F Northeast Stairs", "Rocket Hideout B1F South Stairs",
    "Rocket Hideout B2F Northeast Stairs (Left)", "Rocket Hideout B2F Northeast Stairs (Right)",
    "Rocket Hideout B2F Southeast Stairs", "Rocket Hideout B3F North Stairs", "Rocket Hideout B3F South Stairs",
    "Rocket Hideout B4F Stairs", "Pokemon Tower 1F Stairs", "Pokemon Tower 2F West Stairs",
    "Pokemon Tower 2F East Stairs", "Pokemon Tower 3F West Stairs", "Pokemon Tower 3F East Stairs",
    "Pokemon Tower 4F West Stairs", "Pokemon Tower 4F East Stairs", "Pokemon Tower 5F West Stairs",
    "Pokemon Tower 5F East Stairs", "Pokemon Tower 6F East Stairs", "Pokemon Tower 6F South Stairs",
    "Pokemon Tower 7F Stairs", "Route 12 Gate 1F Stairs", "Route 12 Gate 2F Stairs",
    "Route 15 Gate 1F Stairs", "Route 15 Gate 2F Stairs", "Route 16 Gate 1F Stairs", "Route 16 Gate 2F Stairs",
    "Route 18 Gate 1F Stairs", "Route 18 Gate 2F Stairs", "Safari Zone Center Area Rest House Entrance",
    "Safari Zone Center Area East Exit", "Safari Zone Center Area North Exit", "Safari Zone Center Area West Exit",
    "Safari Zone East Area Northwest Exit", "Safari Zone East Area Southwest Exit",
    "Safari Zone East Area Rest House Entrance", "Safari Zone North Area Southwest Exit",
    "Safari Zone North Area South Exit", "Safari Zone North Area East Exit", "Safari Zone North Area Southeast Exit",
    "Safari Zone North Area Rest House Entrance", "Safari Zone West Area Northeast Exit",
    "Safari Zone West Area East Exit", "Safari Zone West Area Rest House Entrance",
    "Safari Zone West Area Northwest Exit", "Safari Zone Secret House Entrance",
    "Safari Zone Center Area Rest House Exit", "Safari Zone East Area Rest House Exit",
    "Safari Zone North Area Rest House Exit", "Safari Zone West Area Rest House Exit", "Safari Zone Secret House Exit",
    "Silph Co. 1F Stairs", "Silph Co. 2F Northeast Stairs (Left)", "Silph Co. 2F Northeast Stairs (Right)",
    "Silph Co. 3F Northeast Stairs (Left)", "Silph Co. 3F Northeast Stairs (Right)",
    "Silph Co. 4F Northeast Stairs (Left)", "Silph Co. 4F Northeast Stairs (Right)",
    "Silph Co. 5F Northeast Stairs (Left)", "Silph Co. 5F Northeast Stairs (Right)", "Silph Co. 6F Northwest Stairs",
    "Silph Co. 6F Northeast Stairs", "Silph Co. 7F Northwest Stairs", "Silph Co. 7F Northeast Stairs",
    "Silph Co. 8F Northwest Stairs", "Silph Co. 8F Northeast Stairs", "Silph Co. 9F North Stairs (Left)",
    "Silph Co. 9F North Stairs (Right)", "Silph Co. 10F North Stairs (Left)", "Silph Co. 10F North Stairs (Right)",
    "Silph Co. 11F Stairs", "Copycat's House 1F Stairs", "Copycat's House 2F Stairs",
    "Seafoam Islands 1F Northwest Ladder", "Seafoam Islands 1F Northeast Ladder", "Seafoam Islands 1F Southeast Ladder",
    "Seafoam Islands B1F Northwest Ladder (Bottom)", "Seafoam Islands B1F Northwest Ladder (Top)",
    "Seafoam Islands B1F Center Ladder", "Seafoam Islands B1F South Ladder", "Seafoam Islands B1F Northeast Ladder",
    "Seafoam Islands B1F Southeast Ladder (Bottom Left)", "Seafoam Islands B1F Southeast Ladder (Top Right)",
    "Seafoam Islands B2F Northwest Ladder", "Seafoam Islands B2F Southwest Ladder", "Seafoam Islands B2F Center Ladder",
    "Seafoam Islands B2F South Ladder", "Seafoam Islands B2F Northeast Ladder",
    "Seafoam Islands B2F Southeast Ladder (Bottom)", "Seafoam Islands B2F Southeast Ladder (Top)",
    "Seafoam Islands B3F Southwest Ladder", "Seafoam Islands B3F West Ladder",
    "Seafoam Islands B3F Northeast Ladder (Right)", "Seafoam Islands B3F Northeast Ladder (Left)",
    "Seafoam Islands B3F Southeast Ladder", "Seafoam Islands B4F Center Ladder", "Seafoam Islands B4F Northeast Ladder",
    "Pokemon Lab Lounge Entrance", "Pokemon Lab Research Room Entrance", "Pokemon Lab Experiment Room Entrance",
    "Pokemon Lab Lounge Exit", "Pokemon Lab Research Room Exit", "Pokemon Lab Experiment Room Exit",
    "Pokemon Mansion 1F West Stairs", "Pokemon Mansion 1F South Stairs", "Pokemon Mansion 2F Northwest Stairs",
    "Pokemon Mansion 2F West Stairs (Left)", "Pokemon Mansion 2F West Stairs (Right)", "Pokemon Mansion 2F East Stairs",
    "Pokemon Mansion 3F Southwest Stairs", "Pokemon Mansion 3F Northwest Stairs", "Pokemon Mansion 3F Southeast Stairs",
    "Pokemon Mansion B1F Stairs", "Victory Road 1F Ladder", "Victory Road 2F West Ladder",
    "Victory Road 2F Center Ladder", "Victory Road 2F Northwest Ladder", "Victory Road 2F Southeast Ladder",
    "Victory Road 2F East Ladder", "Victory Road 3F Northwest Ladder", "Victory Road 3F Northeast Ladder",
    "Victory Road 3F Southeast Ladder (Top)", "Victory Road 3F Southeast Ladder (Bottom)",
    "Mt. Ember Ruby Path Entrance", "Mt. Ember Summit Path Bottom Entrance", "Mt. Ember Summit Path Top Entrance",
    "Mt. Ember Summit Entrance", "Mt. Ember Summit Path 1F South Exit", "Mt. Ember Summit Path 1F North Exit",
    "Mt. Ember Summit Path 2F South Exit", "Mt. Ember Summit Path 2F North Exit", "Mt. Ember Summit Path 3F West Exit",
    "Mt. Ember Summit Path 3F East Exit", "Mt. Ember Summit Exit", "Mt. Ember Ruby Path 1F Exit",
    "Mt. Ember Ruby Path 1F Northwest Ladder", "Mt. Ember Ruby Path 1F Northeast Ladder",
    "Mt. Ember Ruby Path B1F South Ladder", "Mt. Ember Ruby Path B1F North Ladder",
    "Mt. Ember Ruby Path B1F Return Northeast Ladder", "Mt. Ember Ruby Path B1F Return Southwest Ladder",
    "Mt. Ember Ruby Path B2F West Ladder", "Mt. Ember Ruby Path B2F East Ladder",
    "Mt. Ember Ruby Path B2F Return Northeast Ladder", "Mt. Ember Ruby Path B2F Return Southwest Ladder",
    "Mt. Ember Ruby Path B3F Northwest Ladder", "Mt. Ember Ruby Path B3F Southwest Ladder",
    "Mt. Ember Ruby Path B3F Southeast Ladder", "Mt. Ember Ruby Path B4F Southeast Ladder",
    "Mt. Ember Ruby Path B4F Northwest Ladder", "Mt. Ember Ruby Path B5F Ladder", "Icefall Cave Front North Exit",
    "Icefall Cave Front Ladder", "Icefall Cave 1F South Exit", "Icefall Cave 1F East Ladder",
    "Icefall Cave 1F Northeast Ladder", "Icefall Cave 1F Southeast Ladder", "Icefall Cave 1F Northwest Ladder",
    "Icefall Cave 1F North Exit", "Icefall Cave B1F West Ladder", "Icefall Cave B1F North Ladder",
    "Icefall Cave B1F South Ladder", "Icefall Cave Back Exit", "Lost Cave 1F Ladder", "Lost Cave B1F Room 1 Ladder",
    "Dotted Hole 1F Ladder", "Dotted Hole Sapphire Room Ladder", "Cerulean Cave 1F Northeast Ladder",
    "Cerulean Cave 1F North Ladder", "Cerulean Cave 1F Southwest Ladder", "Cerulean Cave 1F East Ladder",
    "Cerulean Cave 1F Center Ladder", "Cerulean Cave 1F Northwest Ladder (Bottom)",
    "Cerulean Cave 1F Northwest Ladder (Top)", "Cerulean Cave 2F Northeast Ladder", "Cerulean Cave 2F North Ladder",
    "Cerulean Cave 2F West Ladder", "Cerulean Cave 2F East Ladder", "Cerulean Cave 2F Center Ladder",
    "Cerulean Cave 2F Northwest Ladder", "Cerulean Cave B1F Ladder", "Navel Rock 1F Ladder",
    "Navel Rock B1F Northwest Ladder", "Navel Rock B1F Southeast Ladder", "Navel Rock Fork South Ladder",
    "Navel Rock Fork Northwest Ladder", "Navel Rock Fork Northeast Ladder",
    "Navel Rock Summit Path 2F Southeast Ladder", "Navel Rock Summit Path 2F Northwest Ladder",
    "Navel Rock Summit Path 3F Northwest Ladder", "Navel Rock Summit Path 3F Southeast Ladder",
    "Navel Rock Summit Path 4F Southeast Ladder", "Navel Rock Summit Path 4F Northwest Ladder",
    "Navel Rock Summit Path 5F Northwest Ladder", "Navel Rock Summit Path 5F Southeast Ladder",
    "Navel Rock Summit Ladder", "Navel Rock Base Path B1F Northwest Ladder",
    "Navel Rock Base Path B1F Southeast Ladder", "Navel Rock Base Path B2F Southeast Ladder",
    "Navel Rock Base Path B2F Northwest Ladder", "Navel Rock Base Path B3F Northwest Ladder",
    "Navel Rock Base Path B3F Southeast Ladder", "Navel Rock Base Path B4F Southeast Ladder",
    "Navel Rock Base Path B4F Northwest Ladder", "Navel Rock Base Path B5F Northwest Ladder",
    "Navel Rock Base Path B5F Southeast Ladder", "Navel Rock Base Path B6F Southeast Ladder",
    "Navel Rock Base Path B6F Northwest Ladder", "Navel Rock Base Path B7F Northwest Ladder",
    "Navel Rock Base Path B7F Southeast Ladder", "Navel Rock Base Path B8F Southeast Ladder",
    "Navel Rock Base Path B8F Northwest Ladder", "Navel Rock Base Path B9F Northwest Ladder",
    "Navel Rock Base Path B9F Southeast Ladder", "Navel Rock Base Path B10F Southeast Ladder",
    "Navel Rock Base Path B10F Northwest Ladder", "Navel Rock Base Path B11F Northwest Ladder",
    "Navel Rock Base Path B11F Southeast Ladder", "Navel Rock Base Ladder"
]

SILPH_CO_WARP_TILES = [
    "Silph Co. 2F North Warp Tile", "Silph Co. 2F Southeast Warp Tile", "Silph Co. 2F Northwest Warp Tile",
    "Silph Co. 2F Southwest Warp Tile", "Silph Co. 3F Northwest Warp Tile", "Silph Co. 3F Southwest Warp Tile",
    "Silph Co. 3F East Warp Tile", "Silph Co. 3F Southeast Warp Tile", "Silph Co. 3F Northeast Warp Tile",
    "Silph Co. 3F Center Warp Tile", "Silph Co. 3F West Warp Tile", "Silph Co. 4F Southwest Warp Tile",
    "Silph Co. 4F Center Warp Tile", "Silph Co. 4F North Warp Tile (Right)", "Silph Co. 4F North Warp Tile (Left)",
    "Silph Co. 5F North Warp Tile", "Silph Co. 5F South Warp Tile", "Silph Co. 5F Northeast Warp Tile",
    "Silph Co. 5F Southwest Warp Tile", "Silph Co. 6F Northeast Warp Tile",  "Silph Co. 6F Northwest Warp Tile",
    "Silph Co. 7F Southeast Warp Tile", "Silph Co. 7F Northwest Warp Tile (Bottom)",
    "Silph Co. 7F Northwest Warp Tile (Top)",  "Silph Co. 8F Center Warp Tile", "Silph Co. 8F North Warp Tile",
    "Silph Co. 8F Southwest Warp Tile", "Silph Co. 8F West Warp Tile", "Silph Co. 9F Southeast Warp Tile",
    "Silph Co. 9F Northwest Warp Tile", "Silph Co. 10F East Warp Tile", "Silph Co. 10F Southeast Warp Tile (Top Left)",
    "Silph Co. 10F Southeast Warp Tile (Bottom Right)", "Silph Co. 11F Warp Tile"
]

SAFFRON_GYM_WARP_TILES = [
    "Saffron Gym South Warp Tile", "Saffron Gym Southeast Warp Tile (Top Left)",
    "Saffron Gym Southeast Warp Tile (Bottom Left)", "Saffron Gym Southeast Warp Tile (Top Right)",
    "Saffron Gym Southeast Warp Tile (Bottom Right)", "Saffron Gym Southwest Warp Tile (Top Left)",
    "Saffron Gym Southwest Warp Tile (Bottom Left)", "Saffron Gym Southwest Warp Tile (Top Right)",
    "Saffron Gym Southwest Warp Tile (Bottom Right)", "Saffron Gym East Warp Tile (Top Left)",
    "Saffron Gym East Warp Tile (Bottom Left)", "Saffron Gym East Warp Tile (Top Right)",
    "Saffron Gym East Warp Tile (Bottom Right)", "Saffron Gym West Warp Tile (Top Left)",
    "Saffron Gym West Warp Tile (Bottom Left)", "Saffron Gym West Warp Tile (Top Right)",
    "Saffron Gym West Warp Tile (Bottom Right)", "Saffron Gym Northeast Warp Tile (Top Left)",
    "Saffron Gym Northeast Warp Tile (Bottom Left)", "Saffron Gym Northeast Warp Tile (Top Right)",
    "Saffron Gym Northeast Warp Tile (Bottom Right)", "Saffron Gym North Warp Tile (Top Left)",
    "Saffron Gym North Warp Tile (Bottom Left)", "Saffron Gym North Warp Tile (Top Right)",
    "Saffron Gym North Warp Tile (Bottom Right)", "Saffron Gym Northwest Warp Tile (Top Left)",
    "Saffron Gym Northwest Warp Tile (Bottom Left)", "Saffron Gym Northwest Warp Tile (Top Right)",
    "Saffron Gym Northwest Warp Tile (Bottom Right)", "Saffron Gym Center Warp Tile"
]

SEAFOAM_ISLANDS_DROPS = [
    "Seafoam Islands 1F Drop (Left)", "Seafoam Islands 1F Drop (Right)", "Seafoam Islands B1F Drop (Left)",
    "Seafoam Islands B1F Drop (Right)", "Seafoam Islands B2F Drop (Left)", "Seafoam Islands B2F Drop (Right)",
    "Seafoam Islands B3F Drop (Left)", "Seafoam Islands B3F Drop (Right)"
]

POKEMON_MANSION_DROPS = [
    "Pokemon Mansion 3F Drop (Left)", "Pokemon Mansion 3F Drop (Right)"
]

VICTORY_ROAD_DROPS = [
    "Victory Road 3F Drop"
]

DOTTED_HOLE_DROPS = [
    "Dotted Hole 1F Drop", "Dotted Hole B1F Drop (Top)", "Dotted Hole B2F Drop (Left)", "Dotted Hole B3F Drop (Right)",
    "Dotted Hole B4F Drop (Bottom)"
]

BUILDING_ENTRANCE_PAIRS = {
    "Route 22 Gate South Entrance": "Route 22 Gate North Entrance",
    "Viridian Forest South Gate Entrance": "Viridian Forest North Gate Entrance",
    "Route 2 Gate North Entrance": "Route 2 Gate South Entrance",
    "Badge Guy's House Front Entrance": "Badge Guy's House Back Entrance",
    "Robbed House Front Entrance": "Robbed House Back Entrance",
    "Route 5 Gate North Entrance": "Route 5 Gate South Entrance",
    "Underground Path North Entrance": "Underground Path South Entrance",
    "Route 6 Gate South Entrance": "Route 6 Gate North Entrance",
    "Route 11 Gate West Entrance": "Route 11 Gate East Entrance",
    "Route 8 Gate East Entrance": "Route 8 Gate West Entrance",
    "Underground Path East Entrance": "Underground Path West Entrance",
    "Route 7 Gate West Entrance": "Route 7 Gate East Entrance",
    "Celadon Department Store West Entrance": "Celadon Department Store East Entrance",
    "Route 12 Gate North Entrance": "Route 12 Gate South Entrance",
    "Route 15 Gate East Entrance": "Route 15 Gate West Entrance",
    "Route 16 Gate Northeast Entrance": "Route 16 Gate Northwest Entrance",
    "Route 16 Gate Southeast Entrance": "Route 16 Gate Southwest Entrance",
    "Route 18 Gate West Entrance": "Route 18 Gate East Entrance",
    "Fuchsia Fishing House Front Entrance": "Fuchsia Fishing House Back Entrance",
    "Three Isle Path West Entrance": "Three Isle Path East Entrance",
    "Route 22 Gate South Exit": "Route 22 Gate North Exit",
    "Viridian Forest South Gate South Exit": "Viridian Forest North Gate North Exit",
    "Route 2 Gate North Exit": "Route 2 Gate South Exit",
    "Badge Guy's House Front Exit": "Badge Guy's House Back Exit",
    "Robbed House Front Exit": "Robbed House Back Exit",
    "Route 5 Gate North Exit": "Route 5 Gate South Exit",
    "Underground Path 1F North Exit": "Underground Path 1F South Exit",
    "Route 6 Gate South Exit": "Route 6 Gate North Exit",
    "Route 11 Gate 1F West Exit": "Route 11 Gate 1F East Exit",
    "Route 8 Gate East Exit": "Route 8 Gate West Exit",
    "Underground Path 1F East Exit": "Underground Path 1F West Exit",
    "Route 7 Gate West Exit": "Route 7 Gate East Exit",
    "Celadon Department Store 1F West Exit": "Celadon Department Store 1F East Exit",
    "Route 12 Gate 1F North Exit": "Route 12 Gate 1F South Exit",
    "Route 15 Gate 1F East Exit": "Route 15 Gate 1F West Exit",
    "Route 16 Gate 1F Northeast Exit": "Route 16 Gate 1F Northwest Exit",
    "Route 16 Gate 1F Southeast Exit": "Route 16 Gate 1F Southwest Exit",
    "Route 18 Gate 1F West Exit": "Route 18 Gate 1F East Exit",
    "Fuchsia Fishing House Front Exit": "Fuchsia Fishing House Back Exit",
    "Three Isle Path West Exit": "Three Isle Path East Exit",
}
DUNGEON_ENTRANCE_PAIRS = {
    "Viridian Forest South Gate North Exit": "Viridian Forest North Gate South Exit",
    "Mt. Moon West Entrance": "Mt. Moon East Entrance",
    "Diglett's Cave North Entrance": "Diglett's Cave South Entrance",
    "Rock Tunnel North Entrance": "Rock Tunnel South Entrance",
    "Power Plant Front Entrance": "Power Plant Back Entrance",
    "Seafoam Islands North Entrance": "Seafoam Islands South Entrance",
    "Victory Road West Entrance": "Victory Road East Entrance",
    "Pattern Bush West Entrance": "Pattern Bush East Entrance",
    "Viridian Forest South Exit": "Viridian Forest North Exit",
    "Mt. Moon 1F Exit": "Mt. Moon B1F East Ladder (Fourth Tunnel)",
    "Diglett's Cave 1F North Exit": "Diglett's Cave 1F South Exit",
    "Rock Tunnel 1F North Ladder": "Rock Tunnel 1F Exit",
    "Power Plant Front Exit": "Power Plant Back Exit",
    "Seafoam Islands 1F West Exit": "Seafoam Islands 1F East Exit",
    "Victory Road 1F Exit": "Victory Road 2F Exit",
    "Pattern Bush West Exit": "Pattern Bush East Exit"
}
BUILDING_ENTRANCE_PAIRS_REVERSE = {k: v for v, k in BUILDING_ENTRANCE_PAIRS.items()}
BUILDING_PAIRS = BUILDING_ENTRANCE_PAIRS | BUILDING_ENTRANCE_PAIRS_REVERSE
DUNGEON_ENTRANCE_PAIRS_REVERSE = {k: v for v, k in DUNGEON_ENTRANCE_PAIRS.items()}
DUNGEON_PAIRS = DUNGEON_ENTRANCE_PAIRS | DUNGEON_ENTRANCE_PAIRS_REVERSE
MULTI_PAIRS = BUILDING_PAIRS | DUNGEON_PAIRS

OUTDOOR_REGIONS = [
    "Title Screen", "Player's PC", "Pokedex", "Evolutions", "Sky", "Pallet Town (Visit)", "Pallet Town",
    "Pallet Town (Water)", "Viridian City (Visit)", "Viridian City (South)", "Viridian City (North)",
    "Viridian City (Water)", "Pewter City (Visit)", "Pewter City", "Pewter City (Near Roadblock)",
    "Pewter City (Near Museum)", "Cerulean City (Visit)", "Cerulean City", "Cerulean City (Backyard)",
    "Cerulean City (Outskirts)", "Cerulean City (Water)", "Cerulean City (Near Cave)", "Vermilion City (Visit)",
    "Vermilion City", "Vermilion City (Near Gym)", "Vermilion City (Near Harbor)", "Vermilion City (Near Sign)",
    "Vermilion City (Water)", "Lavender Town (Visit)", "Lavender Town", "Celadon City (Visit)", "Celadon City",
    "Celadon City (Near Gym)", "Celadon City (Water)", "Fuchsia City (Visit)", "Fuchsia City",
    "Fuchsia City (Backyard)", "Fuchsia City (Water)", "Saffron City (Visit)", "Saffron City",
    "Cinnabar Island (Visit)", "Cinnabar Island", "Cinnabar Island (Water)", "Indigo Plateau (Visit)",
    "Indigo Plateau", "One Island Town (Visit)", "One Island Town", "One Island Town (Water)", "Treasure Beach (Water)",
    "Treasure Beach", "Kindle Road (South)", "Kindle Road (South Water)", "Kindle Road (Center)",
    "Kindle Road (North Water)", "Kindle Road (North)", "Two Island Town (Visit)", "Two Island Town", "Cape Brink",
    "Cape Brink (Water)", "Three Isle Port (West)", "Three Isle Port (East)", "Three Island Town (Visit)",
    "Three Island Town (South)", "Three Island Town (North)", "Bond Bridge", "Bond Bridge (Water)",
    "Four Island Town (Visit)", "Four Island Town", "Four Island Town (Water)", "Four Island Town (Near Cave)",
    "Five Island Town (Visit)", "Five Island Town", "Five Island Town (Water)", "Five Isle Meadow",
    "Five Isle Meadow (Water)", "Memorial Pillar (Water)", "Memorial Pillar", "Water Labyrinth (Water)",
    "Water Labyrinth", "Resort Gorgeous (Water)", "Resort Gorgeous (Near Resort)", "Resort Gorgeous (Near Cave)",
    "Six Island Town (Visit)", "Six Island Town", "Water Path (South)", "Water Path (South Water)",
    "Water Path (North)", "Water Path (North Water)", "Ruin Valley", "Ruin Valley (Water)", "Green Path (East)",
    "Green Path (West)", "Green Path (Water)", "Outcast Island (Water)", "Outcast Island", "Seven Island Town (Visit)",
    "Seven Island Town", "Canyon Entrance", "Sevault Canyon", "Tanoby Ruins", "Tanoby Ruins (Water)",
    "Tanoby Ruins (Monean Island)", "Tanoby Ruins (Liptoo Island)", "Tanoby Ruins (Weepth Island)",
    "Tanoby Ruins (Dilford Island)", "Tanoby Ruins (Scufib Island)", "Tanoby Ruins (Rixy Island)",
    "Tanoby Ruins (Viapois Island)", "Trainer Tower Exterior (South)", "Trainer Tower Exterior (Water)",
    "Trainer Tower Exterior (North)", "Navel Rock Exterior", "Birth Island Exterior", "Route 1", "Route 2 (Southwest)",
    "Route 2 (Northwest)", "Route 2 (Northeast)", "Route 2 (East)", "Route 2 (Southeast)", "Route 3",
    "Route 3 (Between Ledges)", "Route 4 (West)", "Route 4 (East)", "Route 4 (Southeast)", "Route 4 (Water)",
    "Route 4 (Northeast)", "Route 5", "Route 5 (Center)", "Route 5 (Near Daycare)", "Route 5 (Near Underground)",
    "Route 6", "Route 6 (Near Underground)", "Route 6 (Water)", "Route 7", "Route 7 (Near Underground)", "Route 8",
    "Route 8 (Behind Trees)", "Route 8 (Near Underground)", "Route 9 (West)", "Route 9", "Route 9 (East)",
    "Route 10 (North)", "Route 10 (South)", "Route 10 (North Water)", "Route 10 (South Water)",
    "Route 10 (Near Power Plant)", "Route 10 (Near Power Plant Back)", "Route 11 (West)", "Route 11 (East)",
    "Route 11 (Water)", "Route 12 (West)", "Route 12 (North)", "Route 12 (North Water)", "Route 12 (Center)",
    "Route 12 (Center Water)", "Route 12 (Snorlax Area)", "Route 12 (South)", "Route 12 (South Water)",
    "Route 12 (Behind North Tree)", "Route 12 (Behind South Tree)", "Route 13", "Route 13 (Behind Tree)",
    "Route 13 (Water)", "Route 14", "Route 14 (Behind Tree)", "Route 15 (South)", "Route 15 (North)",
    "Route 15 (Southwest)", "Route 16 (Southeast)", "Route 16 (Northeast)", "Route 16 (Northwest)",
    "Route 16 (Snorlax Area)", "Route 16 (Center)", "Route 16 (Southwest)", "Route 17", "Route 18 (West)",
    "Route 18 (East)", "Route 19", "Route 19 (Water)", "Route 20 (East)", "Route 20 (Near North Cave)",
    "Route 20 (Near South Cave)", "Route 20 (West)", "Route 21", "Route 21 (Water)", "Route 22 (East)",
    "Route 22 (West)", "Route 22 (Water)", "Route 23 (South)", "Route 23 (South Water)", "Route 23 (North Water)",
    "Route 23 (Near Water)", "Route 23 (Center)", "Route 23 (Near Cave)", "Route 23 (North)", "Route 24",
    "Route 24 (Water)", "Route 25", "Route 25 (Water)"
]


class EntranceGroup(IntEnum):
    UNSHUFFLED = 0
    POKEMON_CENTER_ENTRANCE = 1
    POKEMON_CENTER_EXIT = 2
    GYM_ENTRANCE = 3
    GYM_EXIT = 4
    MART_ENTRANCE = 5
    MART_EXIT = 6
    HARBOR_ENTRANCE = 7
    HARBOR_EXIT = 8
    SINGLE_BUILDING_ENTRANCE = 9
    SINGLE_BUILDING_EXIT = 10
    MULTI_BUILDING_ENTRANCE = 11
    MULTI_BUILDING_EXIT = 12
    SINGLE_DUNGEON_ENTRANCE = 13
    SINGLE_DUNGEON_EXIT = 14
    MULTI_DUNGEON_ENTRANCE = 15
    MULTI_DUNGEON_EXIT = 16
    INTERIOR_WARP = 17
    SILPH_CO_WARP_TILE = 18
    SAFFRON_GYM_WARP_TILE = 19
    SEAFOAM_ISLANDS_DROP = 20
    POKEMON_MANSION_DROP = 21
    VICTORY_ROAD_DROP = 22
    DOTTED_HOLE_DROP = 23


ENTRANCE_GROUPS: Dict[str, EntranceGroup] = {}
for entrance_name in POKEMON_CENTER_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.POKEMON_CENTER_ENTRANCE
for entrance_name in POKEMON_CENTER_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.POKEMON_CENTER_EXIT
for entrance_name in GYM_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.GYM_ENTRANCE
for entrance_name in GYM_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.GYM_EXIT
for entrance_name in MART_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.MART_ENTRANCE
for entrance_name in MART_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.MART_EXIT
for entrance_name in HARBOR_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.HARBOR_ENTRANCE
for entrance_name in HARBOR_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.HARBOR_EXIT
for entrance_name in SINGLE_BUILDING_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SINGLE_BUILDING_ENTRANCE
for entrance_name in SINGLE_BUILDING_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SINGLE_BUILDING_EXIT
for entrance_name in MULTI_BUILDING_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.MULTI_BUILDING_ENTRANCE
for entrance_name in MULTI_BUILDING_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.MULTI_BUILDING_EXIT
for entrance_name in SINGLE_DUNGEON_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SINGLE_DUNGEON_ENTRANCE
for entrance_name in SINGLE_DUNGEON_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SINGLE_DUNGEON_EXIT
for entrance_name in MULTI_DUNGEON_ENTRANCES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.MULTI_DUNGEON_ENTRANCE
for entrance_name in MULTI_DUNGEON_EXITS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.MULTI_DUNGEON_EXIT
for entrance_name in INTERIOR_WARPS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.INTERIOR_WARP
for entrance_name in SILPH_CO_WARP_TILES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SILPH_CO_WARP_TILE
for entrance_name in SAFFRON_GYM_WARP_TILES:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SAFFRON_GYM_WARP_TILE
for entrance_name in SEAFOAM_ISLANDS_DROPS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.SEAFOAM_ISLANDS_DROP
for entrance_name in POKEMON_MANSION_DROPS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.POKEMON_MANSION_DROP
for entrance_name in VICTORY_ROAD_DROPS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.VICTORY_ROAD_DROP
for entrance_name in DOTTED_HOLE_DROPS:
    ENTRANCE_GROUPS[entrance_name] = EntranceGroup.DOTTED_HOLE_DROP

POKEMON_CENTER_GROUPS = [EntranceGroup.POKEMON_CENTER_ENTRANCE, EntranceGroup.POKEMON_CENTER_EXIT]

GYM_GROUPS = [EntranceGroup.GYM_ENTRANCE, EntranceGroup.GYM_EXIT]

MART_GROUPS = [EntranceGroup.MART_ENTRANCE, EntranceGroup.MART_EXIT]

HARBOR_GROUPS = [EntranceGroup.HARBOR_ENTRANCE, EntranceGroup.HARBOR_EXIT]

SINGLE_BUILDING_GROUPS = [EntranceGroup.SINGLE_BUILDING_ENTRANCE, EntranceGroup.SINGLE_BUILDING_EXIT]

MULTI_BUILDING_GROUPS = [EntranceGroup.MULTI_BUILDING_ENTRANCE, EntranceGroup.MULTI_BUILDING_EXIT]

BUILDING_ENTRANCE_GROUPS = [EntranceGroup.SINGLE_BUILDING_ENTRANCE, EntranceGroup.MULTI_BUILDING_ENTRANCE]

BUILDING_EXIT_GROUPS = [EntranceGroup.SINGLE_BUILDING_EXIT, EntranceGroup.MULTI_BUILDING_EXIT]

SINGLE_DUNGEON_GROUPS = [EntranceGroup.SINGLE_DUNGEON_ENTRANCE, EntranceGroup.SINGLE_DUNGEON_EXIT]

MULTI_DUNGEON_GROUPS = [EntranceGroup.MULTI_DUNGEON_ENTRANCE, EntranceGroup.MULTI_DUNGEON_EXIT]

DUNGEON_ENTRANCE_GROUPS = [EntranceGroup.SINGLE_DUNGEON_ENTRANCE, EntranceGroup.MULTI_DUNGEON_ENTRANCE]

DUNGEON_EXIT_GROUPS = [EntranceGroup.SINGLE_DUNGEON_EXIT, EntranceGroup.MULTI_DUNGEON_EXIT]

RESTRICTED_MULTI_ENTRANCE_GROUPS = [EntranceGroup.MULTI_BUILDING_ENTRANCE, EntranceGroup.MULTI_DUNGEON_ENTRANCE]

RESTRICTED_MULTI_EXIT_GROUPS = [EntranceGroup.MULTI_BUILDING_EXIT, EntranceGroup.MULTI_DUNGEON_EXIT]

WARP_TILE_GROUPS = [EntranceGroup.SILPH_CO_WARP_TILE, EntranceGroup.SAFFRON_GYM_WARP_TILE]

DROPDOWN_GROUPS = [EntranceGroup.SEAFOAM_ISLANDS_DROP, EntranceGroup.POKEMON_MANSION_DROP,
                   EntranceGroup.VICTORY_ROAD_DROP, EntranceGroup.DOTTED_HOLE_DROP]


def _set_seafoam_entrances(world: "PokemonFRLGWorld") -> None:
    seafoam_reverse_entrances = {
        "Seafoam Islands North Entrance": "Seafoam Islands 1F (Southeast)",
        "Seafoam Islands South Entrance": "Seafoam Islands 1F",
        "Seafoam Islands 1F West Exit": "Route 20 (Near South Cave)",
        "Seafoam Islands 1F East Exit": "Route 20 (Near North Cave)"
    }

    for entrance_name, region_name in seafoam_reverse_entrances.items():
        entrance = world.get_entrance(entrance_name)
        region = world.get_region(region_name)
        entrance.connected_region.entrances.remove(entrance)
        entrance.connected_region = region
        region.entrances.append(entrance)


def _set_starting_pokemon_center(world: "PokemonFRLGWorld") -> List[str]:
    spawn_map = {
        "SPAWN_PALLET_TOWN": "Player's House Entrance",
        "SPAWN_VIRIDIAN_CITY": "Viridian Pokemon Center Entrance",
        "SPAWN_PEWTER_CITY": "Pewter Pokemon Center Entrance",
        "SPAWN_CERULEAN_CITY": "Cerulean Pokemon Center Entrance",
        "SPAWN_LAVENDER_TOWN": "Lavender Pokemon Center Entrance",
        "SPAWN_VERMILION_CITY": "Vermilion Pokemon Center Entrance",
        "SPAWN_CELADON_CITY": "Celadon Pokemon Center Entrance",
        "SPAWN_FUCHSIA_CITY": "Fuchsia Pokemon Center Entrance",
        "SPAWN_CINNABAR_ISLAND": "Cinnabar Pokemon Center Entrance",
        "SPAWN_INDIGO_PLATEAU": "Indigo Plateau Pokemon Center Entrance",
        "SPAWN_SAFFRON_CITY": "Saffron Pokemon Center Entrance",
        "SPAWN_ROUTE4": "Route 4 Pokemon Center Entrance",
        "SPAWN_ROUTE10": "Route 10 Pokemon Center Entrance",
        "SPAWN_ONE_ISLAND": "One Island Pokemon Center Entrance",
        "SPAWN_TWO_ISLAND": "Two Island Pokemon Center Entrance",
        "SPAWN_THREE_ISLAND": "Three Island Pokemon Center Entrance",
        "SPAWN_FOUR_ISLAND": "Four Island Pokemon Center Entrance",
        "SPAWN_FIVE_ISLAND": "Five Island Pokemon Center Entrance",
        "SPAWN_SEVEN_ISLAND": "Seven Island Pokemon Center Entrance",
        "SPAWN_SIX_ISLAND": "Six Island Pokemon Center Entrance"
    }
    kanto_respawn_map = {
        "Viridian Pokemon Center 1F Exit": "SPAWN_VIRIDIAN_CITY",
        "Pewter Pokemon Center 1F Exit": "SPAWN_PEWTER_CITY",
        "Cerulean Pokemon Center 1F Exit": "SPAWN_CERULEAN_CITY",
        "Lavender Pokemon Center 1F Exit": "SPAWN_LAVENDER_TOWN",
        "Vermilion Pokemon Center 1F Exit": "SPAWN_VERMILION_CITY",
        "Celadon Pokemon Center 1F Exit": "SPAWN_CELADON_CITY",
        "Fuchsia Pokemon Center 1F Exit": "SPAWN_FUCHSIA_CITY",
        "Cinnabar Pokemon Center 1F Exit": "SPAWN_CINNABAR_ISLAND",
        "Indigo Plateau Pokemon Center 1F Exit": "SPAWN_INDIGO_PLATEAU",
        "Saffron Pokemon Center 1F Exit": "SPAWN_SAFFRON_CITY",
        "Route 4 Pokemon Center 1F Exit": "SPAWN_ROUTE4",
        "Route 10 Pokemon Center 1F Exit": "SPAWN_ROUTE10",
    }
    respawn_map = kanto_respawn_map.copy()
    respawn_map.update({
        "One Island Pokemon Center 1F Exit": "SPAWN_ONE_ISLAND",
        "Two Island Pokemon Center 1F Exit": "SPAWN_TWO_ISLAND",
        "Three Island Pokemon Center 1F Exit": "SPAWN_THREE_ISLAND",
        "Four Island Pokemon Center 1F Exit": "SPAWN_FOUR_ISLAND",
        "Five Island Pokemon Center 1F Exit": "SPAWN_FIVE_ISLAND",
        "Seven Island Pokemon Center 1F Exit": "SPAWN_SEVEN_ISLAND",
        "Six Island Pokemon Center 1F Exit": "SPAWN_SIX_ISLAND"
    })
    plando_entrances: List[str] = []

    if world.options.shuffle_pokemon_centers:
        starting_center_entrance = world.get_entrance(spawn_map[world.starting_town])
        if world.options.kanto_only:
            starting_center_exit = world.get_entrance(world.random.choice(list(kanto_respawn_map.keys())))
        else:
            starting_center_exit = world.get_entrance(world.random.choice(list(respawn_map.keys())))

        entrance_region = starting_center_entrance.parent_region
        exit_region = starting_center_exit.parent_region
        starting_center_entrance.connected_region.entrances.remove(starting_center_entrance)
        starting_center_entrance.connect(exit_region)
        plando_entrances.append(starting_center_entrance.name)
        world.er_pairings.append((starting_center_entrance.name, starting_center_exit.name))
        starting_center_exit.connected_region.entrances.remove(starting_center_exit)
        starting_center_exit.connect(entrance_region)
        plando_entrances.append(starting_center_exit.name)
        world.er_pairings.append((starting_center_exit.name, starting_center_entrance.name))
        world.starting_respawn = respawn_map[starting_center_exit.name]

    return plando_entrances


def _disconnect_shuffled_entrances(world: "PokemonFRLGWorld") -> None:
    def get_entrance_type(entrance_name: str) -> EntranceType:
        if (entrance_name in SEAFOAM_ISLANDS_DROPS
                or entrance_name in POKEMON_MANSION_DROPS
                or entrance_name in VICTORY_ROAD_DROPS
                or entrance_name in DOTTED_HOLE_DROPS):
            return EntranceType.ONE_WAY
        return EntranceType.TWO_WAY

    shuffled_entrances: List[str] = []

    if world.options.shuffle_pokemon_centers:
        shuffled_entrances.extend(POKEMON_CENTER_ENTRANCES)
        shuffled_entrances.extend(POKEMON_CENTER_EXITS)

    if world.options.shuffle_gyms:
        shuffled_entrances.extend(GYM_ENTRANCES)
        shuffled_entrances.extend(GYM_EXITS)

    if world.options.shuffle_marts:
        shuffled_entrances.extend(MART_ENTRANCES)
        shuffled_entrances.extend(MART_EXITS)

    if world.options.shuffle_harbors:
        shuffled_entrances.extend(HARBOR_ENTRANCES)
        shuffled_entrances.extend(HARBOR_EXITS)

    if world.options.shuffle_buildings != ShuffleBuildingEntrances.option_off:
        shuffled_entrances.extend(SINGLE_BUILDING_ENTRANCES)
        shuffled_entrances.extend(SINGLE_BUILDING_EXITS)
        shuffled_entrances.extend(MULTI_BUILDING_ENTRANCES)
        shuffled_entrances.extend(MULTI_BUILDING_EXITS)

    if (world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_off
            and world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_seafoam):
        shuffled_entrances.extend(SINGLE_DUNGEON_ENTRANCES)
        shuffled_entrances.extend(SINGLE_DUNGEON_EXITS)
        shuffled_entrances.extend(MULTI_DUNGEON_ENTRANCES)
        shuffled_entrances.extend(MULTI_DUNGEON_EXITS)

    if world.options.shuffle_interiors:
        shuffled_entrances.extend(INTERIOR_WARPS)

    if world.options.shuffle_warp_tiles != ShuffleWarpTiles.option_off:
        shuffled_entrances.extend(SILPH_CO_WARP_TILES)
        shuffled_entrances.extend(SAFFRON_GYM_WARP_TILES)

    if world.options.shuffle_dropdowns != ShuffleDropdowns.option_off:
        shuffled_entrances.extend(SEAFOAM_ISLANDS_DROPS)
        shuffled_entrances.extend(POKEMON_MANSION_DROPS)
        shuffled_entrances.extend(VICTORY_ROAD_DROPS)
        shuffled_entrances.extend(DOTTED_HOLE_DROPS)

    plando_entrances = _set_starting_pokemon_center(world)

    for entrance_name in shuffled_entrances:
        if entrance_name in plando_entrances:
            continue
        try:
            entrance = world.get_entrance(entrance_name)
            entrance.randomization_group = ENTRANCE_GROUPS[entrance_name]
            entrance.randomization_type = get_entrance_type(entrance_name)
            if entrance.randomization_type == EntranceType.ONE_WAY:
                target_name = f"!{entrance.name}"
            else:
                target_name = None
            world.er_entrances.append((entrance, entrance.connected_region))
            disconnect_entrance_for_randomization(entrance, entrance.randomization_group, target_name)
        except KeyError:
            continue


def _create_entrance_group_lookup(world: "PokemonFRLGWorld") -> Dict[EntranceGroup, List[EntranceGroup]]:
    entrance_group_lookup = {}
    mixed_entrance_group = []
    mixed_exit_group = []
    unrestricted_entrances = False
    restricted_entrances_mixed = False

    if ("Buildings" in world.options.mix_entrance_warp_pools.value
            and "Dungeons" in world.options.mix_entrance_warp_pools.value
            and ((world.options.shuffle_buildings == ShuffleBuildingEntrances.option_simple
                  and world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_simple)
                 or (world.options.shuffle_buildings == ShuffleBuildingEntrances.option_restricted
                     and world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_restricted))):
        restricted_entrances_mixed = True

    # Create the mixed entrance/exit groups. If interiors/warp tiles/dropdowns are included in the mixed pool then the
    # restriction that entrances -> exits and vice versa can be ignored. Any warp in the mixed pool can go to any other
    # warp.
    if "Interiors" in world.options.mix_entrance_warp_pools.value and world.options.shuffle_interiors:
        mixed_entrance_group.append(EntranceGroup.INTERIOR_WARP)
        mixed_exit_group.append(EntranceGroup.INTERIOR_WARP)
        unrestricted_entrances = True

    if ("Warp Tiles" in world.options.mix_entrance_warp_pools.value
            and world.options.shuffle_warp_tiles == ShuffleWarpTiles.option_full):
        mixed_entrance_group.extend(WARP_TILE_GROUPS)
        mixed_exit_group.extend(WARP_TILE_GROUPS)
        unrestricted_entrances = True

    if ("Dropdowns" in world.options.mix_entrance_warp_pools.value
            and world.options.shuffle_dropdowns == ShuffleDropdowns.option_full
            and world.options.decouple_entrances_warps):
        mixed_entrance_group.extend(DROPDOWN_GROUPS)
        mixed_exit_group.extend(DROPDOWN_GROUPS)
        unrestricted_entrances = True

    if "Pokemon Centers" in world.options.mix_entrance_warp_pools.value:
        if unrestricted_entrances:
            mixed_entrance_group.extend(POKEMON_CENTER_GROUPS)
            mixed_exit_group.extend(POKEMON_CENTER_GROUPS)
        else:
            mixed_entrance_group.append(EntranceGroup.POKEMON_CENTER_EXIT)
            mixed_exit_group.append(EntranceGroup.POKEMON_CENTER_ENTRANCE)

    if "Gyms" in world.options.mix_entrance_warp_pools.value and world.options.shuffle_gyms:
        if unrestricted_entrances:
            mixed_entrance_group.extend(GYM_GROUPS)
            mixed_exit_group.extend(GYM_GROUPS)
        else:
            mixed_entrance_group.append(EntranceGroup.GYM_EXIT)
            mixed_exit_group.append(EntranceGroup.GYM_ENTRANCE)

    if "Marts" in world.options.mix_entrance_warp_pools.value and world.options.shuffle_marts:
        if unrestricted_entrances:
            mixed_entrance_group.extend(MART_GROUPS)
            mixed_exit_group.extend(MART_GROUPS)
        else:
            mixed_entrance_group.append(EntranceGroup.MART_EXIT)
            mixed_exit_group.append(EntranceGroup.MART_ENTRANCE)

    if "Harbors" in world.options.mix_entrance_warp_pools.value and world.options.shuffle_harbors:
        if unrestricted_entrances:
            mixed_entrance_group.extend(HARBOR_GROUPS)
            mixed_exit_group.extend(HARBOR_GROUPS)
        else:
            mixed_entrance_group.append(EntranceGroup.HARBOR_EXIT)
            mixed_exit_group.append(EntranceGroup.HARBOR_ENTRANCE)

    # If buildings or dungeons are mixed then single entrance buildings are always added to the mixed pool. Multi
    # entrance buildings are only added to the mixed pool if the shuffle option is set to full.
    if ("Buildings" in world.options.mix_entrance_warp_pools.value
            and world.options.shuffle_buildings != ShuffleBuildingEntrances.option_off):
        if unrestricted_entrances:
            mixed_entrance_group.extend(SINGLE_BUILDING_GROUPS)
            mixed_exit_group.extend(SINGLE_BUILDING_GROUPS)
            if world.options.shuffle_buildings == ShuffleBuildingEntrances.option_full:
                mixed_entrance_group.extend(MULTI_BUILDING_GROUPS)
                mixed_exit_group.extend(MULTI_BUILDING_GROUPS)
        else:
            mixed_entrance_group.append(EntranceGroup.SINGLE_BUILDING_EXIT)
            mixed_exit_group.append(EntranceGroup.SINGLE_BUILDING_ENTRANCE)
            if world.options.shuffle_buildings == ShuffleBuildingEntrances.option_full:
                mixed_entrance_group.append(EntranceGroup.MULTI_BUILDING_EXIT)
                mixed_exit_group.append(EntranceGroup.MULTI_BUILDING_ENTRANCE)

    if ("Dungeons" in world.options.mix_entrance_warp_pools.value
            and world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_off):
        if unrestricted_entrances:
            mixed_entrance_group.extend(SINGLE_DUNGEON_GROUPS)
            mixed_exit_group.extend(SINGLE_DUNGEON_GROUPS)
            if world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_full:
                mixed_entrance_group.extend(MULTI_DUNGEON_GROUPS)
                mixed_exit_group.extend(MULTI_DUNGEON_GROUPS)
        else:
            mixed_entrance_group.append(EntranceGroup.SINGLE_DUNGEON_EXIT)
            mixed_exit_group.append(EntranceGroup.SINGLE_DUNGEON_ENTRANCE)
            if world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_full:
                mixed_entrance_group.append(EntranceGroup.MULTI_DUNGEON_EXIT)
                mixed_exit_group.append(EntranceGroup.MULTI_DUNGEON_ENTRANCE)

    # Set the entrance groups that an entrance/exit can shuffle with
    if world.options.shuffle_pokemon_centers:
        if "Pokemon Centers" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.POKEMON_CENTER_ENTRANCE] = mixed_entrance_group
            entrance_group_lookup[EntranceGroup.POKEMON_CENTER_EXIT] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.POKEMON_CENTER_ENTRANCE] = [EntranceGroup.POKEMON_CENTER_EXIT]
            entrance_group_lookup[EntranceGroup.POKEMON_CENTER_EXIT] = [EntranceGroup.POKEMON_CENTER_ENTRANCE]

    if world.options.shuffle_gyms:
        if "Gyms" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.GYM_ENTRANCE] = mixed_entrance_group
            entrance_group_lookup[EntranceGroup.GYM_EXIT] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.GYM_ENTRANCE] = [EntranceGroup.GYM_EXIT]
            entrance_group_lookup[EntranceGroup.GYM_EXIT] = [EntranceGroup.GYM_ENTRANCE]

    if world.options.shuffle_marts:
        if "Marts" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.MART_ENTRANCE] = mixed_entrance_group
            entrance_group_lookup[EntranceGroup.MART_EXIT] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.MART_ENTRANCE] = [EntranceGroup.MART_EXIT]
            entrance_group_lookup[EntranceGroup.MART_EXIT] = [EntranceGroup.MART_ENTRANCE]

    if world.options.shuffle_harbors:
        if "Harbors" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.HARBOR_ENTRANCE] = mixed_entrance_group
            entrance_group_lookup[EntranceGroup.HARBOR_EXIT] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.HARBOR_ENTRANCE] = [EntranceGroup.HARBOR_EXIT]
            entrance_group_lookup[EntranceGroup.HARBOR_EXIT] = [EntranceGroup.HARBOR_ENTRANCE]

    # If buildings/dungeons are in the mixed pool, set single entrances/exits so they can connect to any other mixed
    # entrance/exit. Only set multi entrances/exits to be in the mixed pool if the shuffle option is full. Otherwise,
    # set multi exntrances/exits to be mixed with all building/dungeon multi entrances/exits if their shuffle options
    # are the same
    if world.options.shuffle_buildings != ShuffleBuildingEntrances.option_off:
        if "Buildings" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.SINGLE_BUILDING_ENTRANCE] = mixed_entrance_group
            entrance_group_lookup[EntranceGroup.SINGLE_BUILDING_EXIT] = mixed_exit_group
            if world.options.shuffle_buildings == ShuffleBuildingEntrances.option_full:
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_ENTRANCE] = mixed_entrance_group
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_EXIT] = mixed_exit_group
            elif restricted_entrances_mixed:
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_ENTRANCE] = RESTRICTED_MULTI_EXIT_GROUPS
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_EXIT] = RESTRICTED_MULTI_ENTRANCE_GROUPS
            else:
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_ENTRANCE] = [EntranceGroup.MULTI_BUILDING_EXIT]
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_EXIT] = [EntranceGroup.MULTI_BUILDING_ENTRANCE]
        else:
            if world.options.shuffle_buildings == ShuffleBuildingEntrances.option_full:
                entrance_group_lookup[EntranceGroup.SINGLE_BUILDING_ENTRANCE] = BUILDING_EXIT_GROUPS
                entrance_group_lookup[EntranceGroup.SINGLE_BUILDING_EXIT] = BUILDING_ENTRANCE_GROUPS
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_ENTRANCE] = BUILDING_EXIT_GROUPS
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_EXIT] = BUILDING_ENTRANCE_GROUPS
            else:
                entrance_group_lookup[EntranceGroup.SINGLE_BUILDING_ENTRANCE] = [EntranceGroup.SINGLE_BUILDING_EXIT]
                entrance_group_lookup[EntranceGroup.SINGLE_BUILDING_EXIT] = [EntranceGroup.SINGLE_BUILDING_ENTRANCE]
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_ENTRANCE] = [EntranceGroup.MULTI_BUILDING_EXIT]
                entrance_group_lookup[EntranceGroup.MULTI_BUILDING_EXIT] = [EntranceGroup.MULTI_BUILDING_ENTRANCE]

    if world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_off:
        if "Dungeons" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.SINGLE_DUNGEON_ENTRANCE] = mixed_entrance_group
            entrance_group_lookup[EntranceGroup.SINGLE_DUNGEON_EXIT] = mixed_exit_group
            if world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_full:
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_ENTRANCE] = mixed_entrance_group
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_EXIT] = mixed_exit_group
            elif restricted_entrances_mixed:
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_ENTRANCE] = RESTRICTED_MULTI_EXIT_GROUPS
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_EXIT] = RESTRICTED_MULTI_ENTRANCE_GROUPS
            else:
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_ENTRANCE] = [EntranceGroup.MULTI_DUNGEON_EXIT]
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_EXIT] = [EntranceGroup.MULTI_DUNGEON_ENTRANCE]
        else:
            if world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_full:
                entrance_group_lookup[EntranceGroup.SINGLE_DUNGEON_ENTRANCE] = DUNGEON_EXIT_GROUPS
                entrance_group_lookup[EntranceGroup.SINGLE_DUNGEON_EXIT] = DUNGEON_ENTRANCE_GROUPS
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_ENTRANCE] = DUNGEON_EXIT_GROUPS
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_EXIT] = DUNGEON_ENTRANCE_GROUPS
            else:
                entrance_group_lookup[EntranceGroup.SINGLE_DUNGEON_ENTRANCE] = [EntranceGroup.SINGLE_DUNGEON_EXIT]
                entrance_group_lookup[EntranceGroup.SINGLE_DUNGEON_EXIT] = [EntranceGroup.SINGLE_DUNGEON_ENTRANCE]
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_ENTRANCE] = [EntranceGroup.MULTI_DUNGEON_EXIT]
                entrance_group_lookup[EntranceGroup.MULTI_DUNGEON_EXIT] = [EntranceGroup.MULTI_DUNGEON_ENTRANCE]

    if world.options.shuffle_interiors:
        if "Interiors" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.INTERIOR_WARP] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.INTERIOR_WARP] = [EntranceGroup.INTERIOR_WARP]

    if world.options.shuffle_warp_tiles == ShuffleWarpTiles.option_full:
        if "Warp Tiles" in world.options.mix_entrance_warp_pools.value:
            entrance_group_lookup[EntranceGroup.SILPH_CO_WARP_TILE] = mixed_exit_group
            entrance_group_lookup[EntranceGroup.SAFFRON_GYM_WARP_TILE] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.SILPH_CO_WARP_TILE] = WARP_TILE_GROUPS
            entrance_group_lookup[EntranceGroup.SAFFRON_GYM_WARP_TILE] = WARP_TILE_GROUPS
    elif world.options.shuffle_warp_tiles == ShuffleWarpTiles.option_simple:
        entrance_group_lookup[EntranceGroup.SILPH_CO_WARP_TILE] = [EntranceGroup.SILPH_CO_WARP_TILE]
        entrance_group_lookup[EntranceGroup.SAFFRON_GYM_WARP_TILE] = [EntranceGroup.SAFFRON_GYM_WARP_TILE]

    if world.options.shuffle_dropdowns == ShuffleDropdowns.option_full:
        if "Dropdowns" in world.options.mix_entrance_warp_pools.value and world.options.decouple_entrances_warps:
            entrance_group_lookup[EntranceGroup.SEAFOAM_ISLANDS_DROP] = mixed_exit_group
            entrance_group_lookup[EntranceGroup.POKEMON_MANSION_DROP] = mixed_exit_group
            entrance_group_lookup[EntranceGroup.VICTORY_ROAD_DROP] = mixed_exit_group
            entrance_group_lookup[EntranceGroup.DOTTED_HOLE_DROP] = mixed_exit_group
        else:
            entrance_group_lookup[EntranceGroup.SEAFOAM_ISLANDS_DROP] = DROPDOWN_GROUPS
            entrance_group_lookup[EntranceGroup.POKEMON_MANSION_DROP] = DROPDOWN_GROUPS
            entrance_group_lookup[EntranceGroup.VICTORY_ROAD_DROP] = DROPDOWN_GROUPS
            entrance_group_lookup[EntranceGroup.DOTTED_HOLE_DROP] = DROPDOWN_GROUPS
    elif world.options.shuffle_dropdowns == ShuffleDropdowns.option_simple:
        entrance_group_lookup[EntranceGroup.SEAFOAM_ISLANDS_DROP] = [EntranceGroup.SEAFOAM_ISLANDS_DROP]
        entrance_group_lookup[EntranceGroup.POKEMON_MANSION_DROP] = [EntranceGroup.POKEMON_MANSION_DROP]
        entrance_group_lookup[EntranceGroup.VICTORY_ROAD_DROP] = [EntranceGroup.VICTORY_ROAD_DROP]
        entrance_group_lookup[EntranceGroup.DOTTED_HOLE_DROP] = [EntranceGroup.DOTTED_HOLE_DROP]

    return entrance_group_lookup


def _set_pokemon_mansion_exit(world: "PokemonFRLGWorld") -> None:
    cinnabar_region = world.get_region("Cinnabar Island")
    mansion_shuffled_entrance = world.get_entrance("Pokemon Mansion 1F West Exit")
    mansion_other_entrance = world.get_entrance("Pokemon Mansion 1F East Exit")
    cinnabar_region.entrances.remove(mansion_other_entrance)
    mansion_other_entrance.connect(mansion_shuffled_entrance.connected_region)
    for source, dest in world.er_pairings:
        if source == "Pokemon Mansion 1F West Exit":
            world.er_pairings.append((mansion_other_entrance.name, dest))
            break


def _randomize_entrances(world: "PokemonFRLGWorld",
                         entrance_group_lookup: Dict[EntranceGroup, List[EntranceGroup]]) -> None:
    if world.options.decouple_entrances_warps:
        coupled = False
    else:
        coupled = True

    for i in range(MAX_GER_ATTEMPTS):
        try:
            if (world.options.shuffle_buildings != ShuffleBuildingEntrances.option_simple
                    and world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_simple):
                er_placement_state = randomize_entrances(world, coupled, entrance_group_lookup)
            else:
                er_placement_state = randomize_entrances(world, coupled, entrance_group_lookup,
                                                         on_connect=connect_simple_entrances)
            world.er_pairings.extend(er_placement_state.pairings)
            world.logic.guaranteed_hm_access = False
            world.logic.randomizing_entrances = False
            if (world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_off
                    and world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_seafoam):
                _set_pokemon_mansion_exit(world)
            break
        except EntranceRandomizationError as error:
            if i >= MAX_GER_ATTEMPTS - 1:
                raise EntranceRandomizationError(f"Pokemon FRLG: GER failed for player {world.player} "
                                                 f"({world.player_name}) after {MAX_GER_ATTEMPTS} attempts. Final "
                                                 f"error here: \n\n{error}")
            if i > 1:
                world.logic.guaranteed_hm_access = True
            for entrance, vanilla_connected_region in world.er_entrances:
                if entrance.connected_region:
                    entrance.connected_region.entrances.remove(entrance)
                entrance.connected_region = vanilla_connected_region
                if entrance.randomization_type == EntranceType.TWO_WAY:
                    parent_region = entrance.parent_region
                    for parent_entrance in parent_region.entrances:
                        if parent_entrance.name == entrance.name:
                            parent_region.entrances.remove(parent_entrance)
                            break
                    entrance.connected_region = None
                    target = parent_region.create_er_target(entrance.name)
                    target.randomization_group = entrance.randomization_group
                    target.randomization_type = entrance.randomization_type
                else:
                    child_region = entrance.connected_region
                    for child_entrance in child_region.entrances:
                        if child_entrance.name == f"!{entrance.name}":
                            child_region.entrances.remove(child_entrance)
                            break
                    entrance.connected_region = None
                    target = child_region.create_er_target(f"!{entrance.name}")
                    target.randomization_group = entrance.randomization_group
                    target.randomization_type = entrance.randomization_type


def shuffle_entrances(world: "PokemonFRLGWorld") -> bool:
    if world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_seafoam:
        _set_seafoam_entrances(world)
    if world.is_universal_tracker:
        ut_set_entrances(world)
        return False

    entrance_rando = entrances_randomized(world)

    if entrance_rando:
        world.er_pairings = []
        _disconnect_shuffled_entrances(world)
        entrance_group_lookup = _create_entrance_group_lookup(world)
        world.logic.randomizing_entrances = True
        _randomize_entrances(world, entrance_group_lookup)
        return True

    return False


def connect_simple_entrances(er_state: ERPlacementState,
                             placed_exits: List[Entrance],
                             paired_entrances: List[Entrance]):
    if ("Buildings" in er_state.world.options.mix_entrance_warp_pools.value
            and "Dungeons" in er_state.world.options.mix_entrance_warp_pools.value
            and er_state.world.options.shuffle_buildings == ShuffleBuildingEntrances.option_simple
            and er_state.world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_simple
            and placed_exits[0].name in MULTI_PAIRS
            and paired_entrances[0].name in MULTI_PAIRS):
        entrance = er_state.world.get_entrance(MULTI_PAIRS[placed_exits[0].name])
        exit = er_state.entrance_lookup.find_target(MULTI_PAIRS[paired_entrances[0].name])
        er_state.connect(entrance, exit)
        return True
    if (er_state.world.options.shuffle_buildings == ShuffleBuildingEntrances.option_simple
            and placed_exits[0].name in BUILDING_PAIRS
            and paired_entrances[0].name in BUILDING_PAIRS):
        entrance = er_state.world.get_entrance(BUILDING_PAIRS[placed_exits[0].name])
        exit = er_state.entrance_lookup.find_target(BUILDING_PAIRS[paired_entrances[0].name])
        er_state.connect(entrance, exit)
        return True
    elif (er_state.world.options.shuffle_dungeons == ShuffleDungeonEntrances.option_simple
          and placed_exits[0].name in DUNGEON_PAIRS
          and paired_entrances[0].name in DUNGEON_PAIRS):
        entrance = er_state.world.get_entrance(DUNGEON_PAIRS[placed_exits[0].name])
        exit = er_state.entrance_lookup.find_target(DUNGEON_PAIRS[paired_entrances[0].name])
        er_state.connect(entrance, exit)
        return True
    return False


def set_hint_entrances(world: "PokemonFRLGWorld") -> None:
    real_regions = [region.name for region in data.regions.values()]
    for region in world.get_regions():
        checked_regions = {region}
        entrance_hints = set()

        def check_region(region_to_check: Region) -> bool | None:
            if region_to_check.name in OUTDOOR_REGIONS:
                return True
            for entrance in region_to_check.entrances:
                if entrance.parent_region not in checked_regions:
                    checked_regions.add(entrance.parent_region)
                    is_outdoors = check_region(entrance.parent_region)
                    if is_outdoors:
                        entrance_hints.add(entrance.name)
                    elif is_outdoors is not None:
                        return is_outdoors
            return None

        if region.name not in OUTDOOR_REGIONS and region.name in real_regions:
            check_region(region)
            region.entrance_hints = entrance_hints


def entrances_randomized(world: "PokemonFRLGWorld") -> bool:
    if world.options.shuffle_pokemon_centers:
        return True
    elif world.options.shuffle_gyms:
        return True
    elif world.options.shuffle_marts:
        return True
    elif world.options.shuffle_harbors:
        return True
    elif world.options.shuffle_buildings != ShuffleBuildingEntrances.option_off:
        return True
    elif (world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_off
          and world.options.shuffle_dungeons != ShuffleDungeonEntrances.option_seafoam):
        return True
    elif world.options.shuffle_interiors:
        return True
    elif world.options.shuffle_warp_tiles != ShuffleWarpTiles.option_off:
        return True
    elif world.options.shuffle_dropdowns != ShuffleDropdowns.option_off:
        return True
    return False

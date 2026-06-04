from typing import Dict, NamedTuple, List, TYPE_CHECKING
from BaseClasses import Location, LocationProgressType

if TYPE_CHECKING:
    from . import ChainedEchoesWorld


class ChainedEchoesLocation(NamedTuple):
    id: int
    location_type: str  # Type of the location (e.g., Chest, Boss, Emblem, etc.)
    user_friendly_name: str  # Human-readable name
    game_id: str  # Game-specific ID (not used in APWorld, just for reference)
    classification: str  # Missable or Not Missable
    region: str  # The region where the location is found


# Location data will be parsed from a text file
location_data_table: List[ChainedEchoesLocation] = []

# Example text data for locations
locations_txt = '''
// Location Type,User Friendly Name,ID,Classification,Region
Chest,Sternenritt (Chest) #1,sr_1,Missable,Prologue
Chest,Sternenritt (Chest) #2,sr_2,Missable,Prologue
Chest,Sternenritt (Chest) #3,sr_3,Missable,Prologue
Chest,Battlefield (Chest) #1,bf1_3,Missable,Prologue
Chest,Battlefield (Chest) #2,bf1_1,Missable,Prologue
Chest,Battlefield (Chest) #3,bf1_2,Missable,Prologue
Chest,Battlefield (Chest) #4,bf3_1,Missable,Prologue
Boss,Wywyan (Boss) #1,wywyan0,Not Missable,Prologue
Boss,Wywyan (Boss) #2,wywyan1,Not Missable,Prologue
Boss,Wywyan (Boss) #3,wywyan2,Not Missable,Prologue
Chest,Farnsport Peak (Chest) #1,fp_peak_1,Missable,Sandworm
Chest,Farnsport Peak (Chest) #2,fp_peak_2,Missable,Sandworm
Chest,Farnsport Peak (Shiny) #1,fpsparking_peak_3,Missable,Sandworm
Chest,Farnsport Peak (Shiny) #2,fpsparking_peak_4,Missable,Sandworm
Chest,Farnsport Peak (Shiny) #3,fpsparking_peak_5,Missable,Sandworm
Chest,Rohlan Fields S (Chest) #1,rf_2_3_5,Not Missable,Sandworm
Chest,Rohlan Fields S (Chest) #2,rf_2_3_4,Not Missable,Sandworm
Chest,Rohlan Fields S (Chest) #3,rf_2_3_3,Not Missable,Sandworm
Chest,Rohlan Fields S (Chest) #4,rf_2_3_7,Not Missable,Sandworm
Chest,Rohlan Fields S (Chest) #5,rf_2_3_6,Not Missable,Sandworm
Chest,Termina Caves (Chest) #1,trm_3,Not Missable,Sandworm
Chest,Termina Caves (Chest) #2,trm_2,Not Missable,Sandworm
Chest,Termina Caves (Chest) #3,trm_6,Not Missable,Sandworm
Chest,Termina Caves (Chest) #4,trm_1,Not Missable,Sandworm
Chest,Termina Caves (Chest) #5,trm_4,Not Missable,Sandworm
Chest,Termina Caves (Chest) #6,trm_5,Not Missable,Sandworm
Boss,Sandworm (Boss) #1,robber0,Not Missable,Sandworm
Boss,Sandworm (Boss) #2,robber1,Not Missable,Sandworm
Boss,Sandworm (Boss) #3,robber2,Not Missable,Sandworm
Chest,Farnsport Festival (Chest) #1,fpp_fest_1,Missable,Krachan
Chest,Farnsport Festival (Chest) #2,fpp_fest_2,Missable,Krachan
Chest,Narslene Sewers (Chest) #1,ns_south_2,Missable,Krachan
Chest,Narslene Sewers (Chest) #2,ns_south_4,Missable,Krachan
Chest,Narslene Sewers (Chest) #3,ns_south_3,Missable,Krachan
Chest,Narslene Sewers (Chest) #4,ns_south_1,Missable,Krachan
Chest,Narslene Sewers (Chest) #5,ns_south_5,Missable,Krachan
Chest,Narslene Sewers (Chest) #6,ns_south_7,Missable,Krachan
Chest,Narslene Sewers (Chest) #7,ns_south_6,Missable,Krachan
Boss,Krachan (Boss) #1,krachan_tentacle10,Not Missable,Krachan
Boss,Krachan (Boss) #2,krachan_tentacle11,Not Missable,Krachan
Boss,Krachan (Boss) #3,krachan_tentacle12,Not Missable,Krachan
Chest,Farnsport Storeroom (Chest) #1,fpp_storeRoom_2,Missable,Flame Mantis
Chest,Farnsport Storeroom (Chest) #2,fpp_storeRoom_1,Missable,Flame Mantis
Chest,Farnsport Storeroom (Chest) #3,fpp_storeRoom_3,Missable,Flame Mantis
Chest,Farnsport Storeroom (Chest) #4,fpp_storeRoom_5,Missable,Flame Mantis
Chest,Farnsport Storeroom (Chest) #5,fpp_storeRoom_4,Missable,Flame Mantis
Chest,Fleeing Farnsport (Chest) #1,fpp_fleeing_3,Missable,Flame Mantis
Chest,Fleeing Farnsport (Chest) #2,fpp_fleeing_2,Missable,Flame Mantis
Chest,Fleeing Farnsport (Chest) #3,fpp_fleeing_1,Missable,Flame Mantis
Boss,Flame Mantis (Boss) #1,flameMantis0,Not Missable,Flame Mantis
Boss,Flame Mantis (Boss) #2,flameMantis1,Not Missable,Flame Mantis
Boss,Flame Mantis (Boss) #3,flameMantis2,Not Missable,Flame Mantis
Chest,Narslene Sewers (Chest) #8,ns_west_2,Not Missable,Lich
Chest,Narslene Sewers (Chest) #9,ns_west_1,Not Missable,Lich
Chest,Narslene Sewers (Chest) #10,ns_west_4,Not Missable,Lich
Chest,Narslene Sewers (Chest) #11,ns_west_3,Not Missable,Lich
Emblem,Cleric (Emblem),Cleric,Not Missable,Lich
Deal,Starter Pack (Deal),Starter Pack,Not Missable,Lich
Chest,Farnsport Road (Chest) #1,fp_road_2,Not Missable,Lich
Chest,Farnsport Road (Chest) #2,fp_road_1,Not Missable,Lich
Chest,Farnsport Road (Chest) #3,fp_road_3,Not Missable,Lich
Chest,Rohlan Fields E (Buried),rfburied_3_2,Not Missable,Lich
Chest,Rohlan Fields E (Chest) #1,rf_3_2_7,Not Missable,Lich
Chest,Farnsport Bazaar (Chest) #1,fp_bazaar_5,Not Missable,Lich
Chest,Farnsport Bazaar (Shiny) #1,fpsparking_bazaar_3,Not Missable,Lich
Chest,Farnsport Bazaar (Shiny) #2,fpsparking_bazaar_2,Not Missable,Lich
Chest,Farnsport Bazaar (Chest) #2,fp_bazaar_4,Not Missable,Lich
Chest,Farnsport Bazaar (Chest) #3,fp_bazaar_1,Not Missable,Lich
Chest,Farnsport Phyon Oasisrt (Chest) #1,fp_port_2,Not Missable,Lich
Chest,Farnsport Phyon Oasisrt (Chest) #2,fp_port_3,Not Missable,Lich
Chest,Farnsport Phyon Oasisrt (Chest) #3,fp_port_1,Not Missable,Lich
Chest,Rohlan Fields SE (Chest) #1,rf_3_3_1,Not Missable,Lich
Chest,Rohlan Fields E (Chest) #2,rf_3_2_4,Not Missable,Lich
Chest,Rohlan Fields E (Chest) #3,rf_3_2_6,Not Missable,Lich
Chest,Rohlan Fields E (Chest) #4,rf_3_2_1,Not Missable,Lich
Chest,Rohlan Fields C (Chest) #1,rf_2_2_4,Not Missable,Lich
Chest,Rohlan Fields C (Chest) #2,rf_2_2_1,Not Missable,Lich
Chest,Rohlan Fields C (Buried),rfburied_2_2,Not Missable,Lich
Chest,Rohlan Fields C (Chest) #3,rf_2_2_3,Not Missable,Lich
Chest,Rohlan Fields C (Chest) #4,rf_2_2_2,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #1,rfrfshiny_2_3_3,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #2,rfrfshiny_2_3_2,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #3,rfrfshiny_2_3_4,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #4,rfrfshiny_2_3_5,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #5,rfrfshiny_2_3_6,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #6,rfrfshiny_2_3_8,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #7,rfrfshiny_2_3_7,Not Missable,Lich
Chest,Rohlan Fields S (Shiny) #8,rfrfshiny_2_3_1,Not Missable,Lich
Board,Step into Farnsport (Board),Board44,Not Missable,Lich
Board,Find chests in Farnsport (Board),Board45,Not Missable,Lich
Board,Find a Class Emblem in Farnsport (Board),Board46,Missable,Lich
Board,Explore Farnsport (Board),Board65,Not Missable,Lich
ChainBoard,Reward Board (Chain) 4,Chain4,Not Missable,Lich
Board,Defeat 5 Pigears (Board),Board23,Not Missable,Lich
Board,Find 5 Collectibles in Rohlan Fields (Board),Board42,Not Missable,Lich
Board,Step into Rohlan Fields (Board),Board61,Not Missable,Lich
Board,Defeat a Building (Board),Board60,Not Missable,Lich
Emblem,Warrior (Emblem),Warrior,Not Missable,Lich
Board,Defeat 3 Slorses (Board),Board62,Not Missable,Lich
Board,Kill a Slorse by Poison (Board),Board83,Not Missable,Lich
Board,Find a Class Emblem in Rohlan Fields (Board),Board4,Not Missable,Lich
Chest,Termina Caves (Chest) #7,trm_7,Not Missable,Lich
Chest,Rohlan Fields SW (Chest) #1,rf_1_3_2,Not Missable,Lich
Chest,Rohlan Fields SW (Shiny) #1,rfshiny_1_3_3,Not Missable,Lich
Chest,Rohlan Fields SW (Shiny) #2,rfshiny_1_3_4,Not Missable,Lich
Chest,Rohlan Fields SW (Chest) #2,rf_1_3_3,Not Missable,Lich
Chest,Rohlan Fields SW (Chest) #3,rf_1_3_1,Not Missable,Lich
Chest,Rohlan Fields W (Chest) #1,rf_1_2_1,Not Missable,Lich
Chest,Rohlan Fields W (Chest) #2,rf_1_2_14,Not Missable,Lich
Chest,Rohlan Fields W (Chest) #3,rf_1_2_2,Not Missable,Lich
Chest,Rohlan Fields W (Shiny) #1,rfrfshiny_1_2_10,Not Missable,Lich
Chest,Rohlan Fields W (Chest) #4,rf_1_2_4,Not Missable,Lich
Chest,Rohlan Fields W (Chest) #5,rf_1_2_3,Not Missable,Lich
Board,Defeat 6 Wool Turtles (Board),Board43,Not Missable,Lich
Board,Find 10 Collectibles in Rohlan Fields (Board),Board82,Not Missable,Lich
Board,Find the Phioran couple (Board),Board84,Missable,Lich
Deal,Packs of Snacks (Deal),Packs of Snacks,Not Missable,Lich
Deal,... (Deal),…,Not Missable,Lich
Chest,Ograne Grottos SW (Chest) #1,og_1_3_3,Not Missable,Lich
Chest,Rohlan Fields NE (Chest) #1,rf_3_1_4,Not Missable,Lich
Chest,Rohlan Fields NE (Chest) #2,rf_3_1_3,Not Missable,Lich
Chest,Rohlan Fields NE (Buried),rfburied_3_1,Not Missable,Lich
Chest,Rohlan Fields NE (Chest) #3,rf_3_1_1,Not Missable,Lich
Chest,Rohlan Fields N (Chest) #1,rf_2_1_1,Not Missable,Lich
Board,Buy 3 Deals (Board),Board47,Not Missable,Lich
Board,Step into Ograne Grottos (Board),Board107,Not Missable,Lich
Chest,Rohlan Fields N (Chest) #2,rf_2_1_3,Not Missable,Lich
Chest,Rohlan Fields N (Chest) #3,rf_2_1_2,Not Missable,Lich
Chest,Rohlan Fields NW (Buried),rfburied_1_1,Not Missable,Lich
Chest,Rohlan Fields NW (Chest) #1,rf_1_1_2,Not Missable,Lich
Chest,Rohlan Fields NW (Chest) #2,rf_1_1_1,Not Missable,Lich
Board,Find 10 Collectibles in Ograne Grottos (Board),Board128,Not Missable,Lich
Board,Find 5 Collectibles in Ograne Grottos (Board),Board106,Not Missable,Lich
Board,Find chests in Rohlan Fields (Board),Board5,Not Missable,Lich
Board,Explore Rohlan Fields (Board),Board3,Not Missable,Lich
Board,Defeat 3 Saliva (Board),Board1,Not Missable,Lich
Board,Find hidden caves in Rohlan Fields (Board),Board0,Not Missable,Lich
Board,Find buried treasures in Rohlan Fields (Board),Board102,Not Missable,Lich
ChainBoard,Reward Board (Chain) 8,Chain8,Not Missable,Lich
ChainBoard,Reward Board (Chain) 16,Chain16,Not Missable,Lich
Board,Win against Crabs with Glenn (Board),Board2,Not Missable,Lich
Board,Unique: Leaping the Frog (Board),Board40,Not Missable,Lich
Deal,Sun & Moon (Deal),Sun & Moon,Not Missable,Lich
Deal,Robe 3 (Deal),Robe 3,Not Missable,Lich
Board,Unique: Tak the Yak (Board),Board80,Not Missable,Lich
Deal,Greatsword 3 (Deal),Greatsword 3,Not Missable,Lich
Deal,Light Armor 3 (Deal),Light Armor 3,Not Missable,Lich
Deal,Rapier 3 (Deal),Rapier 3,Not Missable,Lich
Chest,Rohlan Fields W (Shiny) #2,rfrfshiny_1_2_8,Not Missable,Lich
Chest,Rohlan Fields W (Shiny) #3,rfrfshiny_1_2_9,Not Missable,Lich
Chest,Rohlan Fields W (Shiny) #4,rfrfshiny_1_2_7,Not Missable,Lich
Chest,Rohlan Fields W (Chest) #6,rf_1_2_6,Not Missable,Lich
Chest,Rohlan Fields SW (Shiny) #3,rfshiny_1_3_6,Not Missable,Lich
Chest,Rohlan Fields SW (Shiny) #4,rfshiny_1_3_5,Not Missable,Lich
Board,Quest: The Pass to Kortara (Board),Board85,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #1,tpf_1_4,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #2,tpf_1_3,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #3,tpf_1_5,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #4,tpf_1_6,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #5,tpf_1_7,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #6,tpf_1_8,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #7,tpf_1_10,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #8,tpf_1_9,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #9,tpf_1_1,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #10,tpf_1_11,Not Missable,Lich
Chest,Purple Flame Temple (Chest) #11,tpf_1_2,Not Missable,Lich
ChainBoard,Reward Board (Chain) 24,Chain24,Not Missable,Lich
Boss,Lich (Boss) #1,lich0,Not Missable,Lich
Boss,Lich (Boss) #2,lich1,Not Missable,Lich
Boss,Lich (Boss) #3,lich2,Not Missable,Lich
Chest,Purple Flame Temple (Shiny) #1,tpf_2shiny_1,Not Missable,Mines
Chest,Purple Flame Temple (Shiny) #2,tpf_2shiny_2,Not Missable,Mines
Board,Step Into Kortara (Board),Board124,Not Missable,Mines
Chest,Kortara Mountan Range SW (Chest) #1,kmr_1_3_6,Not Missable,Mines
Chest,Kortara Mountan Range S (Chest) #1,kmr_2_3_1,Not Missable,Mines
Board,Find 5 Collectibles in Kortara (Board),Board142,Not Missable,Mines
Board,Win an encounter against Medusaen Vipers without using any skill (Board),Board162,Not Missable,Mines
Chest,Kortara Mountan Range S (Chest) #4,kmr_2_3_4,Not Missable,Mines
Chest,Kortara Mountan Range S (Buried) #1,kmrburied_2_3_1,Not Missable,Mines
Board,Defeat 10 Horn Lizards (Board),Board104,Not Missable,Mines
Board,Find 10 Collectibles in Kortara (Board),Board125,Not Missable,Mines
Board,Win an encounter against Horn Lizards without taking any damage (Board),Board146,Not Missable,Mines
Deal,Uncommon Material Pack (Deal),Uncommon Material Pack,Not Missable,Mines
Deal,Common Material Pack (Deal),Common Material Pack,Not Missable,Mines
Deal,Rare Material Pack (Deal),Rare Material Pack,Not Missable,Mines
Deal,Sword 3 (Deal),Sword 3,Not Missable,Mines
Deal,Bow 3 (Deal),Bow 3,Not Missable,Mines
Boss,Row (Boss) #1,row (1)0,Not Missable,Mines
Boss,Row (Boss) #2,row (1)1,Not Missable,Mines
Boss,Row (Boss) #3,row (1)2,Not Missable,Mines
Chest,Kortara Mountan Range SW (Chest) #3,kmr_1_3_1,Missable,Drill Breaker
Chest,Kortara Mountan Range SW (Chest) #4,kmr_1_3_3,Missable,Drill Breaker
Chest,Kortara Mountan Range SW (Chest) #5,kmr_1_3_2,Missable,Drill Breaker
Chest,Kortara Mountan Range SW (Chest) #6,kmr_1_3_5,Missable,Drill Breaker
Chest,Kortara Mountan Range SW (Chest) #7,kmr_1_3_4,Missable,Drill Breaker
Chest,Kortara Mountan Range (Chest)?,kmr_foridden1,Missable,Drill Breaker
Chest,Kortara Mountan Range SE (Chest) #1,kmr_3_3_4,Not Missable,Drill Breaker
Chest,Kortara Mountan Range SE (Buried),kmrburied_3_3,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Shiny) #1,kmrshiny_3_2_3,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Chest) #2,kmr_3_2_1,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Shiny) #2,kmrshiny_3_2_2,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Shiny) #3,kmrshiny_3_2_1,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Chest) #3,kmr_3_2_2,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Chest) #4,kmr_3_2_4,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Chest) #5,kmr_3_2_3,Not Missable,Drill Breaker
Chest,Kortara Mountan Range E (Chest) #6,kmr_3_2_5,Not Missable,Drill Breaker
Chest,Kortara Mountan Range NE (Chest) #1,kmr_3_1_3,Not Missable,Drill Breaker
Chest,Wygrand Mines (Chest) #1,wm_1_1,Missable,Drill Breaker
Chest,Wygrand Mines (Chest) #2,wm_2_1,Missable,Drill Breaker
Chest,Wygrand Mines (Chest) #3,wm_2_2,Missable,Drill Breaker
Boss,Drill Breaker (Boss) #1,drillBreaker0,Not Missable,Drill Breaker
Boss,Drill Breaker (Boss) #2,drillBreaker1,Not Missable,Drill Breaker
Boss,Drill Breaker (Boss) #3,drillBreaker2,Not Missable,Drill Breaker
Deal,Heavy Armor 3 (Deal),Heavy Armor 3,Not Missable,Arlette
Chest,Kortara Mountan Range N (Chest) #1,kmr_2_1_1,Not Missable,Arlette
Chest,Kortara Mountan Range N (Chest) #2,kmr_2_1_3,Not Missable,Arlette
Chest,Kortara Mountan Range N (Chest) #3,kmr_2_1_2,Not Missable,Arlette
Board,Defeat 10 Mountain Bibi (Board),Board122,Not Missable,Arlette
Chest,White Rose Inn (Chest) #1,wr_house_1,Not Missable,Arlette
Board,Step Into Fiorwoods (Board),Board51,Not Missable,Arlette
Chest,Fiorwoods S (Chest) #3,fw_2_3_2,Not Missable,Arlette
Chest,Fiorwoods SE (Buried),fwburied_3_3,Not Missable,Arlette
Board,Find 5 Collectibles in Fiorwoods (Board),Board50,Not Missable,Arlette
Chest,Fiorwoods SE (Chest) #1,fw_3_3_3,Not Missable,Arlette
Chest,Fiorwoods SE (Chest) #2,fw_3_3_2,Not Missable,Arlette
Chest,Fiorwoods SE (Shiny) #1,fwshiny_3_3_7,Not Missable,Arlette
Chest,Fiorwoods SE (Shiny) #2,fwshiny_3_3_8,Not Missable,Arlette
Chest,Fiorwoods SE (Chest) #3,fw_3_3_5,Not Missable,Arlette
Chest,Fiorwoods SE (Shiny) #3,fwshiny_3_3_6,Not Missable,Arlette
Chest,Fiorwoods SE (Chest) #4,fw_3_3_4,Not Missable,Arlette
Chest,Fiorwoods SE (Chest) #5,fw_3_3_1,Not Missable,Arlette
Chest,Fiorwoods SE (Shiny) #4,fwshiny_3_3_9,Not Missable,Arlette
Board,Defeat 6 Alpha Wolves (Board),Board52,Not Missable,Arlette
Board,Find 10 Collectibles in Fiorwoods (Board),Board53,Not Missable,Arlette
Deal,Bangle (Deal),Bangle,Not Missable,Arlette
Deal,Super Rare Material Pack (Deal),Super Rare Material Pack,Not Missable,Arlette
Deal,Gauntlets (Deal),Gauntlets,Not Missable,Arlette
Chest,White Rose Inn (Chest) #2,wr_dungeon_3,Not Missable,Arlette
Chest,White Rose Inn (Chest) #3,wr_dungeon_2,Not Missable,Arlette
Chest,White Rose Inn (Chest) #4,wr_dungeon_1,Not Missable,Arlette
Boss,Arlette (Boss) #1,arlette0,Not Missable,Arlette
Boss,Arlette (Boss) #2,arlette1,Not Missable,Arlette
Boss,Arlette (Boss) #3,arlette2,Not Missable,Arlette
Chest,Fiorwoods E (Chest) #5,fw_3_2_3,Not Missable,Puppeteer
Board,Defeat Vins without going into Overdrive (Board),Board28,Not Missable,Puppeteer
Chest,Fiorwoods C (Chest) #1,fw_2_2_3,Not Missable,Puppeteer
Chest,Fiorwoods S (Chest) #1,fw_2_3_1,Not Missable,Puppeteer
Board,Defeat a Gazer while switching every turn (Board),Board31,Not Missable,Puppeteer
Chest,Fiorwoods C (Chest) #2,fw_2_2_1,Not Missable,Puppeteer
Chest,Fiorwoods W (Chest) #1,fw_1_2_4,Not Missable,Puppeteer
Chest,Fiorwoods W (Chest) #2,fw_1_2_1,Not Missable,Puppeteer
Chest,Fiorwoods C (Buried),fwburied_2_2,Not Missable,Puppeteer
Chest,Fiorwoods C (Chest) #3,fw_2_2_5,Not Missable,Puppeteer
Chest,Fiorwoods C (Chest) #4,fw_2_2_4,Not Missable,Puppeteer
Chest,Fiorwoods N (Chest) #1,fw_2_1_1,Not Missable,Puppeteer
Chest,Fiorwoods N (Chest) #2,fw_2_1_3,Not Missable,Puppeteer
Chest,Fiorwoods N (Chest) #3,fw_2_1_6,Not Missable,Puppeteer
Chest,Fiorwoods N (Chest) #4,fw_2_1_4,Not Missable,Puppeteer
Chest,Fiorwoods N (Chest) #5,fw_2_1_5,Not Missable,Puppeteer
Chest,Fiorwoods N (Chest) #6,fw_2_1_2,Not Missable,Puppeteer
Deal,Heavenly Ring (Deal),Heavenly Ring,Not Missable,Puppeteer
Board,Defeat 8 Vins (Board),Board48,Not Missable,Puppeteer
ChainBoard,Reward Board (Chain) 32,Chain32,Not Missable,Puppeteer
Chest,Tormund Center (Chest) #1,tm_Center_2,Not Missable,Puppeteer
Chest,Tormund Center (Shiny) #1,tmsparking_Center_3,Not Missable,Puppeteer
Chest,Tormund Center (Shiny) #2,tmsparking_Center_6,Not Missable,Puppeteer
Chest,Tormund Center (Chest) #2,tm_Center_1,Not Missable,Puppeteer
Chest,Tormund Center (Shiny) #3,tmsparking_Center_5,Not Missable,Puppeteer
Chest,Tormund (Shiny)Center_4,tmsparking_Center_4,Not Missable,Puppeteer
Chest,Tormund West (Chest) #1,tm_West_1,Not Missable,Puppeteer
Chest,Tormund West (Chest) #2,tm_West_2,Not Missable,Puppeteer
Chest,Tormund Downtown (Shiny) #1,tmsparking_downtown_4,Not Missable,Puppeteer
Chest,Tormund East (Chest) #2,tm_East_1,Not Missable,Puppeteer
Chest,Tormund East (Chest) #3,tm_East_2,Not Missable,Puppeteer
Chest,Tormund Downtown (Chest) #2,tm_downtown_2,Not Missable,Puppeteer
Chest,Tormund East (Chest) #1,tm_East_3,Not Missable,Puppeteer
Chest,Tormund Downtown (Chest) #1,tm_downtown_1,Not Missable,Puppeteer
Board,Join the Adventurer’s Guild (Board),Board26,Not Missable,Puppeteer
Board,Explore Tormund (Board),Board93,Not Missable,Puppeteer
Board,Step into Tormund (Board),Board113,Not Missable,Puppeteer
Board,Find chests in Tormund (Board),Board73,Not Missable,Puppeteer
Chest,Tormund Downtown (Shiny) #2,tmsparking_downtown_3,Not Missable,Puppeteer
Chest,Tormund Castle (Chest) #1,tc_2_1,Not Missable,Puppeteer
Chest,Inner Sactum (Chest) #1,is_2,Not Missable,Puppeteer
Chest,Fiorwoods NW (Chest) #1,fw_1_1_2,Not Missable,Puppeteer
Chest,Fiorwoods NW (Chest) #2,fw_1_1_1,Not Missable,Puppeteer
Board,Explore Fiorwoods (Board),Board11,Not Missable,Puppeteer
Chest,Fiorwoods SW (Chest) #1,fw_1_3_1,Not Missable,Puppeteer
Chest,Fiorwoods SW (Chest) #2,fw_1_3_2,Not Missable,Puppeteer
Emblem,Vampire (Emblem),Vampire,Not Missable,Puppeteer
Board,Find a Class Emblem in Fiorwoods (Board),Board49,Missable,Puppeteer
ChainBoard,Reward Board (Chain) 40,Chain40,Not Missable,Puppeteer
Board,Paralyze the same enemy four times (Board),Board114,Not Missable,Puppeteer
Chest,Fiorwoods NE (Chest) #1,fw_3_1_4,Not Missable,Puppeteer
Chest,Fiorwoods NE (Chest) #2,fw_3_1_6,Not Missable,Puppeteer
Board,Find hidden caves in Fiorwoods (Board),Board13,Not Missable,Puppeteer
Chest,Fiorwoods NE (Chest) #3,fw_3_1_5,Not Missable,Puppeteer
Chest,Fiorwoods NE (Chest) #4,fw_3_1_3,Not Missable,Puppeteer
Chest,Fiorwoods NE (Chest) #5,fw_3_1_2,Not Missable,Puppeteer
Chest,Fiorwoods NE (Chest) #6,fw_3_1_1,Not Missable,Puppeteer
Chest,Fiorwoods E (Buried),fwburied_3_2,Not Missable,Puppeteer
Board,Find buried treasures in Fiorwoods (Board),Board8,Not Missable,Puppeteer
Chest,Fiorwoods C (Chest) #5,fw_2_2_6,Not Missable,Puppeteer
Chest,Fiorwoods E (Chest) #1,fw_3_2_1,Not Missable,Puppeteer
Chest,Fiorwoods E (Chest) #2,fw_3_2_2,Not Missable,Puppeteer
Chest,Fiorwoods E (Chest) #3,fw_3_2_4,Not Missable,Puppeteer
Chest,Fiorwoods E (Chest) #4,fw_3_2_5,Not Missable,Puppeteer
Board,Step Into Perpetua (Board),Board54,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Chest) #1,ffp_1_2_2,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Chest) #2,ffp_1_2_3,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Buried),ffpburied_1_2,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #1,ffp_2_2_4,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #2,ffp_2_2_3,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Chest) #3,ffp_1_2_4,Not Missable,Puppeteer
Board,Win an encounter without using any healing skill (Board),Board97,Not Missable,Puppeteer
Board,Win an encounter without allowing the enemies to take more than 4 actions (Board),Board77,Not Missable,Puppeteer
Board,Find 5 Collectibles in Perpetua (Board),Board57,Not Missable,Puppeteer
Board,Unique: Ekskalibur (Board),Board69,Not Missable,Puppeteer
Board,Win an encounter with an all girls team (Board),Board58,Not Missable,Puppeteer
Board,Win an encounter against scorpion with only 8 actions (Board),Board35,Not Missable,Puppeteer
Emblem,Shaman (Emblem),Shaman,Not Missable,Puppeteer
Board,Defeat 6 King Owl (Board),Board15,Not Missable,Puppeteer
Board,Find a Class Emblem in Perpetua (Board),Board16,Not Missable,Puppeteer
Board,Obtain 4 Class Emblems anywhere (Board),Board133,Missable,Puppeteer
ChainBoard,Reward Board (Chain) 48,Chain48,Not Missable,Puppeteer
Board,Defeat 5 Spore Men (Board),Board56,Not Missable,Puppeteer
Board,Defeat 8 Scorpions (Board),Board55,Not Missable,Puppeteer
ChainBoard,Reward Board (Chain) 56,Chain56,Not Missable,Puppeteer
Board,Defeat 4 Forest Wyrms (Board),Board12,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Chest) #4,ffp_1_2_5,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Chest) #5,ffp_1_2_6,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua NW (Chest) #3,ffp_1_1_1,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua NW (Chest) #4,ffp_1_1_5,Not Missable,Puppeteer
Board,Find 10 Collectibles in Perpetua (Board),Board59,Not Missable,Puppeteer
Deal,Trove of Gold (Deal),Trove of Gold,Not Missable,Puppeteer
Deal,Sword & Greatsword 4 (Deal),Sword & Greatsword 4,Not Missable,Puppeteer
Deal,Trove of Midas (Deal),Trove of Midas,Not Missable,Puppeteer
Board,Get 3 Herbal Collars (Board),Board96,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua NW (Chest) #5,ffp_1_1_4,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua NW (Chest) #6,ffp_1_1_3,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua NW (Chest) #7,ffp_1_1_6,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua NW (Chest) #8,ffp_1_1_2,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #3,ffp_2_2_5,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #4,ffp_2_2_7,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #5,ffp_2_2_6,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #6,ffp_2_2_8,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #7,ffp_2_2_2,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Chest) #8,ffp_2_2_1,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua C (Buried),ffpburied_2_2,Not Missable,Puppeteer
Boss,Puppeteer (Boss) #1,puppeteer0,Not Missable,Puppeteer
Boss,Puppeteer (Boss) #2,puppeteer1,Not Missable,Puppeteer
Boss,Puppeteer (Boss) #3,puppeteer2,Not Missable,Puppeteer
Chest,Flower Fields of Perpetua W (Chest) #6,ffp_1_2_1,Not Missable,Gin
Chest,Leviathan Trench (Chest) #1,lt_1_6,Not Missable,Gin
Chest,Leviathan Trench (Chest) #2,lt_1_3,Not Missable,Gin
Chest,Leviathan Trench (Chest) #3,lt_1_4,Not Missable,Gin
Chest,Leviathan Trench (Chest) #4,lt_1_1,Not Missable,Gin
Chest,Leviathan Trench (Chest) #5,lt_1_2,Not Missable,Gin
Chest,Leviathan Trench (Chest) #6,lt_1_5,Not Missable,Gin
Deal,Clothes & Robes 4 (Deal),Clothes & Robes 4,Not Missable,Gin
Deal,Light & Heavy Armor 4 (Deal),Light & Heavy Armor 4,Not Missable,Gin
Boss,Gin (Boss) #1,gin0,Not Missable,Gin
Boss,Gin (Boss) #2,gin1,Not Missable,Gin
Boss,Gin (Boss) #3,gin2,Not Missable,Gin
Chest,Kindreld Monastery (Chest) #1,km_f1_inner_1,Not Missable,Kondor
Chest,Kindreld Monastery (Chest) #2,km_f1_1,Not Missable,Kondor
Chest,Kindreld Monastery (Chest) #3,km_f1_inner_3,Not Missable,Kondor
Chest,Kindreld Monastery (Chest) #4,km_f1_inner_2,Not Missable,Kondor
Chest,Kindreld Monastery (Chest) #5,km_b1_1,Not Missable,Kondor
Emblem,Monk (Emblem),Monk,Not Missable,Kondor
Chest,Kindreld Monastery (Chest) #6,km_f1_2,Not Missable,Kondor
Chest,Aurora U5 (Chest) #1,as_aurora_U5_2,Missable,Kondor
Chest,Aurora U5 (Chest) #2,as_aurora_U5_3,Missable,Kondor
Chest,Aurora U5 (Chest) #3,as_aurora_U5_1,Missable,Kondor
Chest,Aurora U5 (Chest) #4,as_aurora_U5_east_2,Missable,Kondor
Chest,Aurora U4 (Chest) #1,as_aurora_U4_2,Missable,Kondor
Chest,Aurora U4 (Chest) #2,as_aurora_U4_1,Missable,Kondor
Chest,Aurora U4 (Chest) #3,as_aurora_U4_3,Missable,Kondor
// MECH
Chest,Aurora U5 (Chest) #5,as_aurora_U5_east_7,Not Missable,Kondor
Chest,Aurora U5 (Chest) #6,as_aurora_U5_east_5,Not Missable,Kondor
Chest,Aurora U5 (Chest) #7,as_aurora_U5_east_4,Not Missable,Kondor
Chest,Aurora U5 (Chest) #8,as_aurora_U5_east_3,Not Missable,Kondor
Chest,Aurora U5 (Chest) #9,as_aurora_U5_east_6,Not Missable,Kondor
Chest,Aurora U5 (Chest) #10,as_aurora_U5_east_1,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #1,kmr_1_2_3,Not Missable,Kondor
Chest,Kortara Mountan Range W (Shiny) #1,kmrshiny_1_2_1,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #2,kmr_1_2_8,Not Missable,Kondor
Board,Find hidden caves in Kortara (Board),Board121,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #3,kmr_1_2_2,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #4,kmr_1_2_1,Not Missable,Kondor
Chest,Kortara Mountan Range W (Shiny) #2,kmrshiny_1_2_2,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #5,kmr_1_2_4,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #6,kmr_1_2_5,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #7,kmr_1_2_9,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #8,kmr_1_2_6,Not Missable,Kondor
Chest,Kortara Mountan Range W (Chest) #9,kmr_1_2_7,Not Missable,Kondor
Chest,Mount Rydell (Chest) #1,mr_1_4,Not Missable,Kondor
Chest,Mount Rydell (Chest) #2,mr_1_1,Not Missable,Kondor
Chest,Mount Rydell (Chest) #3,mr_1_5,Not Missable,Kondor
Chest,Mount Rydell (Chest) #4,mr_1_2,Not Missable,Kondor
Chest,Mount Rydell (Chest) #5,mr_1_3,Not Missable,Kondor
Chest,Mount Rydell (Chest) #6,mr_2_1,Not Missable,Kondor
Chest,Mount Rydell (Chest) #7,mr_2_4,Not Missable,Kondor
Chest,Mount Rydell (Chest) #8,mr_2_2,Not Missable,Kondor
Chest,Mount Rydell (Chest) #9,mr_2_6,Not Missable,Kondor
Chest,Mount Rydell (Chest) #10,mr_3_3,Not Missable,Kondor
Chest,Mount Rydell (Chest) #11,mr_2_3,Not Missable,Kondor
Chest,Mount Rydell (Chest) #12,mr_2_5,Not Missable,Kondor
Chest,Mount Rydell (Chest) #13,mr_3_2,Not Missable,Kondor
Chest,Mount Rydell (Chest) #14,mr_3_1,Not Missable,Kondor
Boss,Kortara Kondor (Boss) #1,kortaraKondor0,Not Missable,Kondor
Boss,Kortara Kondor (Boss) #2,kortaraKondor1,Not Missable,Kondor
Boss,Kortara Kondor (Boss) #3,kortaraKondor2,Not Missable,Kondor
// OPEN WORLD SECTION
Chest,Rohlan Fields SE (Chest) #2,rf_mech_3_3,Not Missable,Fridolyn
Chest,Rohlan Fields S (Chest) #6,rf_2_3_8,Not Missable,Fridolyn
Chest,Rohlan Fields NW (Chest) #3,rf_1_1_4,Not Missable,Fridolyn
Chest,Rohlan Fields NW (Chest) #4,rf_1_1_3,Not Missable,Fridolyn
Chest,Rohlan Fields NW (Chest) #5,rf_mech_1,Not Missable,Fridolyn
// MANOR KEY
Chest,Rohlan Fields NW (Chest) #6,rf_1_1_5,Not Missable,Fridolyn
// INSIDE MANOR
// KEY ITEM Rusty Rapier
Chest,Manor (Chest) #1,rf_2_1_5,Not Missable,Manor
// KEY ITEM Charon's Coin Bag
Chest,Manor (Chest) #2,rf_2_1_4,Not Missable,Manor
// OUT OF MANOR
Chest,Kortara Mountan Range SE (Chest) #3,kmr_mech_3_3_2,Not Missable,Fridolyn
Chest,Kortara Mountan Range SE (Chest) #4,kmr_mech_3_3_1,Not Missable,Fridolyn
Chest,Kortara Mountan Range SE (Chest) #5,kmr_3_3_2,Not Missable,Fridolyn
Chest,Kortara Mountan Range S (Buried) #2,kmrburied_2_3_2,Not Missable,Fridolyn
Board,Find buried treasures in Kortara (Board),Board180,Not Missable,Fridolyn
Chest,Kortara Mountan Range S (Chest) #2,kmr_mech_2_3_1,Not Missable,Fridolyn
Chest,Kortara Mountan Range S (Chest) #3,kmr_mech_2_3_2,Not Missable,Fridolyn
Chest,Kortara Mountan Range SW (Chest) #2,kmr_mech_1_3_1,Not Missable,Fridolyn
Chest,Kortara Mountan Range NE (Chest) #2,kmr_mech_3_1_1,Not Missable,Fridolyn
Chest,Kortara Mountan Range NE (Chest) #3,kmr_mech_3_1_2,Not Missable,Fridolyn
Board,Defeat 6 Alphoarns (Board),Board143,Not Missable,Fridolyn
Emblem,Bandit (Emblem),Bandit,Not Missable,Fridolyn
Board,Find a Class Emblem in Kortara (Board),Board126,Missable,Fridolyn
ChainBoard,Reward Board (Chain) 64,Chain64,Not Missable,Fridolyn
Board,Unique: Dwelly of the Valley (Board),Board182,Not Missable,Fridolyn
Board,Unique: Gol D. Waterfly (Board),Board160,Not Missable,Fridolyn
Chest,Fiorwoods W (Chest) #3,fw_1_2_3,Not Missable,Fridolyn
Chest,Fiorwoods W (Chest) #4,fw_1_2_2,Not Missable,Fridolyn
Chest,Wyrnshire S (Chest) #1,ws_south_3,Not Missable,Fridolyn
Chest,Wyrnshire S (Shiny) #1,wsshiny_south_1,Not Missable,Fridolyn
Chest,Wyrnshire S (Chest) #2,ws_south_6,Not Missable,Fridolyn
Chest,Wyrnshire S (Shiny) #2,wsshiny_south_2,Not Missable,Fridolyn
Chest,Wyrnshire S (Chest) #3,ws_south_5,Not Missable,Fridolyn
Chest,Wyrnshire S (Shiny) #3,wsshiny_south_3,Not Missable,Fridolyn
Chest,Wyrnshire S (Chest) #4,ws_south_2,Not Missable,Fridolyn
Chest,Wyrnshire S (Chest) #5,ws_south_4,Not Missable,Fridolyn
Chest,Wyrnshire S (Chest) #6,ws_south_1,Not Missable,Fridolyn
Board,Step into Wyrnshire (Board),Board229,Not Missable,Fridolyn
Board,Explore Wyrnshire (Board),Board189,Not Missable,Fridolyn
Chest,Wyrnshire N (Chest) #1,ws_north_3,Not Missable,Fridolyn
Chest,Wyrnshire N (Chest) #2,ws_north_2,Not Missable,Fridolyn
Chest,Wyrnshire N (Chest) #3,ws_north_4,Not Missable,Fridolyn
Chest,Wyrnshire N (Chest) #4,ws_north_1,Not Missable,Fridolyn
Chest,Wyrnshire N (Chest) #5,ws_north_5,Not Missable,Fridolyn
Board,Find chests in Wyrnshire (Board),Board209,Not Missable,Fridolyn
Chest,Arkant Archipelago (Shiny),aashiney_house,Not Missable,Fridolyn
Board,Step Into Arkant (Board),Board192,Not Missable,Fridolyn
Chest,Arkant Archipelago NW (Chest) #1,aa_1_1_3,Not Missable,Fridolyn
Chest,Arkant Archipelago NW (Chest) #2,aa_1_1_6,Not Missable,Fridolyn
Chest,Arkant Archipelago NE (Chest) #1,aa_2_1_1,Not Missable,Fridolyn
Chest,Arkant Archipelago NE (Buried),aaburied_2_1,Not Missable,Fridolyn
Board,Defeat 1 Adamant Crab (Board),Board173,Not Missable,Fridolyn
Board,Find 5 Collectibles in Arkant (Board),Board155,Not Missable,Fridolyn
Chest,Arkant Archipelago NW (Chest) #3,aa_1_1_4,Not Missable,Fridolyn
Board,Find 10 Collectibles in Arkant (Board),Board193,Not Missable,Fridolyn
Chest,Arkant Archipelago NW (Chest) #4,aa_1_1_5,Not Missable,Fridolyn
Board,Reach level 2 with your clan (Board),Board230,Not Missable,Fridolyn
Chest,Arkant Archipelago SE (Chest) #1,aa_2_2_1,Not Missable,Fridolyn
Chest,Arkant Archipelago SE (Chest) #2,aa_2_2_2,Not Missable,Fridolyn
Board,Explore Arkant (Board),Board215,Not Missable,Fridolyn
Board,Defeat Sea Monks without switching gear in Sky Armors (Board),Board213,Not Missable,Fridolyn
Chest,Arkant Archipelago SW (Chest) #1,aa_1_2_2,Not Missable,Fridolyn
Board,Survive two actions by Sea Monks on foot (Board),Board195,Not Missable,Fridolyn
Chest,Arkant Archipelago SW (Chest) #2,aa_1_2_4,Not Missable,Fridolyn
Chest,Arkant Archipelago SW (Chest) #3,aa_1_2_8,Not Missable,Fridolyn
Emblem,Summoner (Emblem),Summoner,Not Missable,Fridolyn
Board,Find a Class Emblem in Arkant (Board),Board153,Missable,Fridolyn
Board,Destroy all ASACs (Board),Board214,Not Missable,Fridolyn
ChainBoard,Reward Board (Chain) 72,Chain72,Not Missable,Fridolyn
Chest,Arkant Archipelago SW (Buried),aaburied_1_2,Not Missable,Fridolyn
Board,Find buried treasures in Arkant (Board),Board191,Not Missable,Fridolyn
Chest,Arkant Archipelago SE (Buried),aaburied_2_2,Not Missable,Fridolyn
Chest,Arkant Archipelago NE (Chest) #2,aa_2_1_2,Not Missable,Fridolyn
Board,Find chests in Arkant (Board),Board232,Not Missable,Fridolyn
Chest,Arkant Archipelago NE (Chest) #3,aa_2_1_3,Not Missable,Fridolyn
Board,Find hidden caves in Arkant (Board),Board171,Not Missable,Fridolyn
Board,Unique: Otter Nobunaga (Board),Board233,Not Missable,Fridolyn
Board,Defeat 5 Purple Whales (Board),Board154,Not Missable,Fridolyn
ChainBoard,Reward Board (Chain) 80,Chain80,Not Missable,Fridolyn
Chest,Arkant Archipelago NW (Chest) #5,aa_1_1_1,Not Missable,Fridolyn
Chest,Arkant Archipelago NW (Chest) #6,aa_1_1_2,Not Missable,Fridolyn
Board,Win an encounter naked on foot (Board),Board175,Not Missable,Fridolyn
Board,Defeat 14 Sea Monks (Board),Board190,Not Missable,Fridolyn
ChainBoard,Reward Board (Chain) 88,Chain88,Not Missable,Fridolyn
Chest,The Hooge (Chest) #1,ho_3,Not Missable,Fridolyn
Chest,The Hooge (Chest) #2,ho_2,Not Missable,Fridolyn
Deal,Tome of Fiends (Deal),Tome of Fiends,Not Missable,Fridolyn
Board,Quest: The Food the Cap and the Hungry (Board),Board92,Not Missable,Fridolyn
Chest,The Hooge (Chest) #3,ho_5,Not Missable,Fridolyn
Chest,The Hooge (Chest) #4,ho_4,Not Missable,Fridolyn
Chest,The Hooge (Chest) #5,ho_6,Not Missable,Fridolyn
Chest,The Hooge (Chest) #6,ho_1,Not Missable,Fridolyn
Chest,New Wyrnshire Castle (Chest),ws_castle,Not Missable,Fridolyn
Boss,Fridolyn (Boss) #1,fridolynBoss0,Not Missable,Fridolyn
Boss,Fridolyn (Boss) #2,fridolynBoss1,Not Missable,Fridolyn
Boss,Fridolyn (Boss) #3,fridolynBoss2,Not Missable,Fridolyn
Board,Quest: A Little Vacation (Board),Board211,Not Missable,Matthye
Chest,Resort Island (Chest) #1,va_resortIsland1,Not Missable,Matthye
Chest,Flower Fields of Perpetua C (Chest) #9,ffp_mech_2_2_1,Not Missable,Matthye
Chest,Flower Fields of Perpetua W (Chest) #7,ffp_mech_1_2_1,Not Missable,Matthye
Chest,Flower Fields of Perpetua NW (Chest) #2,ffp_mech_1_1_1,Not Missable,Matthye
Chest,Flower Fields of Perpetua SW (Chest) #1,ffp_1_3_3,Not Missable,Matthye
Chest,Flower Fields of Perpetua SW (Chest) #2,ffp_1_3_1,Not Missable,Matthye
Chest,Flower Fields of Perpetua SW (Chest) #3,ffp_1_3_2,Not Missable,Matthye
Chest,Flower Fields of Perpetua S (Chest) #1,ffp_2_3_1,Not Missable,Matthye
Board,Find hidden caves in Perpetua (Board),Board79,Not Missable,Matthye
Chest,Flower Fields of Perpetua (Chest)?,0,Not Missable,Matthye
Chest,Flower Fields of Perpetua S (Chest) #2,ffp_2_3_2,Not Missable,Matthye
Chest,Flower Fields of Perpetua SE (Chest) #1,ffp_3_3_1,Not Missable,Matthye
Chest,Flower Fields of Perpetua SE (Buried),ffpburied_3_3,Not Missable,Matthye
Board,Find buried treasures in Perpetua (Board),Board99,Not Missable,Matthye
Chest,Flower Fields of Perpetua E (Chest) #1,ffp_3_2_1,Not Missable,Matthye
Chest,Flower Fields of Perpetua E (Chest) #2,ffp_3_2_2,Not Missable,Matthye
Chest,Flower Fields of Perpetua E (Chest) #3,ffp_3_2_3,Not Missable,Matthye
Board,Explore Perpetura (Board),Board38,Not Missable,Matthye
Board,Unique: Da Capo (Board),Board19,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #1,po_west_9,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #2,po_west_1,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #3,po_west_10,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #4,po_west_7,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #5,po_west_2,Not Missable,Matthye
Deal,Light & Heavy Armor 6 (Deal),Light & Heavy Armor 6,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #6,po_west_6,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #7,po_west_5,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #8,po_west_4,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #9,po_west_3,Not Missable,Matthye
Deal,Clothes & Robes 6 (Deal),Clothes & Robes 6,Not Missable,Matthye
Deal,Sword 6 (Deal),Sword 6,Not Missable,Matthye
Chest,Phyon Oasis W (Chest) #10,po_west_8,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #1,po_east_4,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #2,po_east_10,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #3,po_east_8,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #4,po_east_7,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #5,po_east_9,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #6,po_east_11,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #7,po_east_2,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #8,po_east_5,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #9,po_east_6,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #10,po_east_3,Not Missable,Matthye
Deal,Mystic Ring (Deal),Mystic Ring,Not Missable,Matthye
Chest,Phyon Oasis E (Chest) #11,po_east_1,Not Missable,Matthye
Boss,Matthye (Boss) #1,forgottenMatthye0,Not Missable,Matthye
Boss,Matthye (Boss) #2,forgottenMatthye1,Not Missable,Matthye
Boss,Matthye (Boss) #3,forgottenMatthye2,Not Missable,Matthye
// INSIDE MIND
Chest,Inside Mind (Chest) #1,dr_first_3,Missable,Donner
Chest,Inside Mind (Chest) #2,dr_first_4,Missable,Donner
Chest,Inside Mind (Chest) #3,dr_first_1,Missable,Donner
Chest,Inside Mind (Chest) #4,dr_first_2,Missable,Donner
// OUTSIDE MIND
Board,Quest: Into the Maelstrom (Board),Board6,Not Missable,Donner
// OGRANE GROTTO (Maybe can be done before Matthye and Phyion Oasis?)
Chest,Ograne Grottos SW (Buried),ogburied_1_3,Not Missable,Donner
Chest,Ograne Grottos SW (Chest) #2,og_1_3_1,Not Missable,Donner
Chest,Ograne Grottos SW (Chest) #3,og_1_3_2,Not Missable,Donner
Chest,Ograne Grottos S (Chest) #1,og_2_3_1,Not Missable,Donner
Chest,Ograne Grottos S (Chest) #2,og_2_3_2,Not Missable,Donner
Chest,Ograne Grottos C (Chest) #1,og_2_2_2,Not Missable,Donner
Chest,Ograne Grottos C (Chest) #2,og_2_2_3,Not Missable,Donner
Chest,Ograne Grottos C (Chest) #3,og_2_2_1,Not Missable,Donner
Chest,Ograne Grottos C (Chest) #4,og_2_2_4,Not Missable,Donner
Chest,Ograne Grottos C (Buried),ogburied_2_2,Not Missable,Donner
Chest,Ograne Grottos NW (Chest) #1,og_1_1_1,Not Missable,Donner
Chest,Ograne Grottos N (Buried),ogburied_2_1,Not Missable,Donner
Board,Find buried treasures in Ograne Grottos (Board),Board89,Not Missable,Donner
Board,Step Into Nhysa (Board),Board226,Not Missable,Donner
Board,Quest: Door to Nhysa (Board),Board166,Not Missable,Donner
ChainBoard,Reward Board (Chain) 96,Chain96,Not Missable,Donner
Chest,Ograne Grottos W (Chest) #1,og_1_2_1,Not Missable,Donner
Chest,Ograne Grottos W (Chest) #2,og_1_2_2,Not Missable,Donner
// END OGRANE GROTTO SECTION
// TORMUND CASTLE STORMING
Chest,Tormund Castle (Chest) #2,tc_3_7,Not Missable,Donner
Chest,Tormund Castle (Chest) #3,tc_3_8,Not Missable,Donner
Chest,Tormund Castle (Chest) #4,tc_3_9,Not Missable,Donner
Chest,Tormund Castle (Chest) #5,tc_3_12,Not Missable,Donner
Chest,Tormund Castle (Chest) #6,tc_3_11,Not Missable,Donner
Chest,Tormund Castle (Chest) #7,tc_3_3,Not Missable,Donner
Chest,Tormund Castle (Chest) #8,tc_3_13,Not Missable,Donner
Chest,Tormund Castle (Chest) #9,tc_3_14,Not Missable,Donner
Chest,Tormund Castle (Chest) #10,tc_3_1,Not Missable,Donner
Chest,Tormund Castle (Chest) #11,tc_3_2,Not Missable,Donner
Deal,Almost Ultimate Material Pack (Deal),Almost Ultimate Material Pack,Not Missable,Donner
Chest,Tormund Castle (Chest) #12,tc_3_5,Not Missable,Donner
Chest,Tormund Castle (Chest) #13,tc_3_15,Not Missable,Donner
Chest,Tormund Castle (Chest) #14,tc_3_6,Not Missable,Donner
Chest,Tormund Castle (Chest) #15,tc_3_10,Not Missable,Donner
Chest,Tormund Castle (Chest) #16,tc_3_4,Not Missable,Donner
Chest,Tormund Castle (Chest) #17,tc_1_2,Not Missable,Donner
Chest,Tormund Castle (Chest) #18,tc_1_3,Not Missable,Donner
Chest,Tormund Castle (Chest) #19,tc_1_6,Not Missable,Donner
Chest,Tormund Castle (Chest) #20,tc_1_1,Not Missable,Donner
Chest,Tormund Castle (Chest) #21,tc_1_4,Not Missable,Donner
Chest,Tormund Castle (Chest) #22,tc_1_5,Not Missable,Donner
Chest,Tormund Castle (Chest) #23,tc_1_7,Not Missable,Donner
Boss,Donner (Boss) #1,donner0,Not Missable,Donner
Boss,Donner (Boss) #2,donner1,Not Missable,Donner
Boss,Donner (Boss) #3,donner2,Not Missable,Donner
// END TORMUND CASTLE STORMING
// SHAMBALA
Board,Step into Shambala (Board),Board139,Not Missable,Godfrey
Chest,Shambala S (Chest) #1,sh_2_3_2,Not Missable,Godfrey
Chest,Shambala S (Chest) #2,sh_2_3_1,Not Missable,Godfrey
Chest,Shambala S (Chest) #3,sh_2_3_3,Not Missable,Godfrey
Chest,Shambala S (Buried),shburied_2_3,Not Missable,Godfrey
Chest,Shambala SE (Chest) #1,sh_3_3_1,Not Missable,Godfrey
Chest,Shambala SE (Chest) #2,sh_3_3_2,Not Missable,Godfrey
Chest,Shambala E (Chest) #1,sh_3_2_4,Not Missable,Godfrey
Chest,Shambala E (Chest) #2,sh_3_2_1,Not Missable,Godfrey
Chest,Shambala E (Chest) #3,sh_3_2_3,Not Missable,Godfrey
Chest,Shambala C (Chest) #1,sh_2_2_5,Not Missable,Godfrey
Board,Find 5 Collectibles in Shambala (Board),Board157,Not Missable,Godfrey
Chest,Shambala C (Chest) #2,sh_2_2_1,Not Missable,Godfrey
Chest,Shambala C (Chest) #3,sh_2_2_3,Not Missable,Godfrey
Chest,Shambala C (Chest) #4,sh_2_2_2,Not Missable,Godfrey
Chest,Shambala C (Chest) #5,sh_2_2_4,Not Missable,Godfrey
Board,Find 10 Collectibles in Shambala (Board),Board217,Not Missable,Godfrey
Chest,Shambala N (Chest) #1,sh_2_1_1,Not Missable,Godfrey
Chest,Shambala N (Buried),shburied_2_1,Not Missable,Godfrey
Board,Defeat 7 Toucibris (Board),Board137,Not Missable,Godfrey
Chest,Shambala W (Chest) #1,sh_1_2_2,Not Missable,Godfrey
Chest,Shambala W (Chest) #2,sh_1_2_4,Not Missable,Godfrey
Chest,Shambala W (Chest) #3,sh_1_2_1,Not Missable,Godfrey
Chest,Shambala W (Buried),shburied_1_2,Not Missable,Godfrey
Board,Defeat 10 Sky Monkeys (Board),Board156,Not Missable,Godfrey
Board,Find buried treasures in Shambala (Board),Board219,Not Missable,Godfrey
Chest,Shambala W (Chest) #4,sh_1_2_3,Not Missable,Godfrey
Chest,Shambala W (Chest) #5,sh_1_2_6,Not Missable,Godfrey
Chest,Shambala W (Chest) #6,sh_1_2_5,Not Missable,Godfrey
Chest,Shambala W (Chest) #7,sh_1_2_7,Not Missable,Godfrey
Board,Find chests in Shambala (Board),Board216,Not Missable,Godfrey
Board,Find hidden caves in Shambala (Board),Board138,Not Missable,Godfrey
Emblem,Chemist (Emblem),Chemist,Not Missable,Godfrey
Board,Find a Class Emblem in Shambala (Board),Board117,Missable,Godfrey
Board,Obtain 8 Class Emblems anywhere (Board),Board228,Missable,Godfrey
ChainBoard,Reward Board (Chain) 104,Chain104,Not Missable,Godfrey
Chest,Shambala NE (Chest) #1,sh_3_1_1,Not Missable,Godfrey
Board,Defeat 5 Ancient Turtles (Board),Board199,Not Missable,Godfrey
Board,Win an encounter against Shell Turtles witout using magic skills (Board),Board178,Not Missable,Godfrey
Board,Defeat 5 Sky Monkey with Egyl and Robb (Board),Board159,Not Missable,Godfrey
Board,Unique: Aurora the Dragon (Board),Board179,Not Missable,Godfrey
Board,Explore Shambala (Board),Board218,Not Missable,Godfrey
Chest,Shambala NW (Chest) #1,sh_1_1_1,Not Missable,Godfrey
Board,Buy equipment in Shambala (Board),Board177,Not Missable,Godfrey
ChainBoard,Reward Board (Chain) 112,Chain112,Not Missable,Godfrey
Deal,Material Pack Surprise (Deal),Material Pack Surprise,Not Missable,Godfrey
Deal,Material Pack Surprise 2 (Deal),Material Pack Surprise 2,Not Missable,Godfrey
Chest,Shambala E (Chest) #4,sh_3_2_5,Not Missable,Godfrey
Chest,Shambala E (Chest) #5,sh_3_2_2,Not Missable,Godfrey
Boss,Godfrey (Boss) #1,godfreyFlame0,Not Missable,Godfrey
Boss,Godfrey (Boss) #2,godfreyFlame1,Not Missable,Godfrey
Boss,Godfrey (Boss) #3,godfreyFlame2,Not Missable,Godfrey
// END SHAMBALA
// FOR THE LOVE OF FOOD
Chest,Sandworm (Chest) #1,sw_4,Missable,Shaved Head
Chest,Sandworm (Chest) #2,sw_5,Missable,Shaved Head
Chest,Sandworm (Chest) #3,sw_1,Missable,Shaved Head
Chest,Sandworm (Chest) #4,sw_2,Missable,Shaved Head
Chest,Sandworm (Chest) #5,sw_3,Missable,Shaved Head
Board,Quest: For the Love of Food (Board),Board149,Not Missable,Shaved Head
// END FOR THE LOVE OF FOOD
Chest,Empyrean Ruins 1 (Chest) #1,er_firstPart_2,Not Missable,Shaved Head
Chest,Empyrean Ruins 1 (Chest) #2,er_firstPart_1,Not Missable,Shaved Head
Chest,Empyrean Ruins 1 (Chest) #3,er_firstPart_3,Not Missable,Shaved Head
Chest,Empyrean Ruins 1 (Chest) #4,er_firstPart_4,Not Missable,Shaved Head
Chest,Empyrean Ruins 1 (Chest) #5,er_firstPart_5,Not Missable,Shaved Head
Chest,Empyrean Ruins 1 (Chest) #6,er_firstPart_6,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #1,er_secondPart_1_5,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #2,er_secondPart_1_2,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #3,er_secondPart_1_3,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #4,er_secondPart_1_1,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #5,er_secondPart_1_4,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #6,er_secondPart_2_2,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #7,er_secondPart_2_1,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #8,er_secondPart_3_2,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #9,er_secondPart_3_3,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #10,er_secondPart_3_4,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #11,er_secondPart_3_5,Not Missable,Shaved Head
Chest,Empyrean Ruins 2 (Chest) #12,er_secondPart_3_1,Not Missable,Shaved Head
Boss,Shaved Head (Boss) #1,shavedHead0,Not Missable,Shaved Head
Boss,Shaved Head (Boss) #2,shavedHead1,Not Missable,Shaved Head
Boss,Shaved Head (Boss) #3,shavedHead2,Not Missable,Shaved Head
Deal,Clothes & Robes 8 (Deal),Clothes & Robes 8,Not Missable,Endahrt
Deal,Light & Heavy Armor 8 (Deal),Light & Heavy Armor 8,Not Missable,Endahrt
Deal,Claws 8 (Deal),Claws 8,Not Missable,Endahrt
Deal,Anchor 8 (Deal),Anchor 8,Not Missable,Endahrt
Deal,Thief’s Gloves (Deal),Thief’s Gloves,Not Missable,Endahrt
Deal,Leaf Hood (Deal),Leaf Hood,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #1,er_thirdPart_1_9,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #2,er_thirdPart_1_6,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #3,er_thirdPart_1_1,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #4,er_thirdPart_1_2,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #5,er_thirdPart_1_8,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #6,er_thirdPart_1_5,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #7,er_thirdPart_1_3,Not Missable,Endahrt
Chest,Empyrean Ruins 3 (Chest) #8,er_thirdPart_1_4,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #1,er_finalPart_5,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #2,er_finalPart_3,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #3,er_finalPart_4,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #4,er_finalPart_2,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #5,er_finalPart_7,Not Missable,Endahrt
// KEY ITEM CHURCH KEY
Chest,Empyrean Ruins 4 (Chest) #6,er_finalPart_8,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #7,er_finalPart_1,Not Missable,Endahrt
Chest,Empyrean Ruins 4 (Chest) #8,er_finalPart_6,Not Missable,Endahrt
Boss,Endahrt (Boss) #1,endahrt0,Not Missable,Endahrt
Boss,Endahrt (Boss) #2,endahrt1,Not Missable,Endahrt
Boss,Endahrt (Boss) #3,endahrt2,Not Missable,Endahrt
// CHURCH
Board,Find the hidden stone tablets (Board),Board119,Not Missable,Church
// END CHURCH
// GOBLIN'S DILEMMA
Chest,Ograne Grottos NE (Chest) #1,og_3_1_1,Not Missable,Living Wall
Chest,Ograne Grottos NE (Chest) #2,og_3_1_3,Not Missable,Living Wall
// MINER'S KEY
Chest,Ograne Grottos NE (Chest) #3,og_3_1_2,Not Missable,Miner's Section
Board,Quest: A Goblin’s Dilemma (Board),Board20,Not Missable,Miner's Section
// END GOBLIN'S DILEMMA
// MINER'S KEY (AND MAYBE GOBLIN BOOK)
// DARK TABLET
// END MINER'S KEY
// BAIBAI X
Chest,Flower Fields of Perpetua NE (Chest) #1,ffp_3_1_1,Not Missable,Baibai X
Board,Find chests in Perpetua (Board),Board18,Not Missable,Baibai X
Chest,Flower Fields of Perpetua NE (Chest) #2,ffp_3_1_2,Not Missable,Baibai X
Chest,Flower Fields of Perpetua NE (Chest) #3,ffp_3_1_4,Not Missable,Baibai X
Chest,Flower Fields of Perpetua NE (Chest) #4,ffp_3_1_3,Not Missable,Baibai X
// TODO: ASSASSIN GIRL
// END BAIBAI X
Emblem,Mage Warrior (Emblem),Mage Warrior,Not Missable,Living Wall
Board,Defeat 4 Tadeyes (Board),Board129,Not Missable,Living Wall
Board,Find a Class Emblem in Ograne Grottos (Board),Board130,Missable,Living Wall
Emblem,Gambler (Emblem),Gambler,Not Missable,Living Wall
Chest,Leonar (Chest) #1,va_leonar3,Not Missable,Living Wall
Emblem,Pyromancer (Emblem),Pyromancer,Not Missable,Living Wall
Chest,Leonar (Chest) #2,va_leonar2,Not Missable,Living Wall
Emblem,Rune Knight (Emblem),Rune Knight,Not Missable,Living Wall
Chest,Reina's Grave (Chest) #1,gr_1_3,Missable,Living Wall
Chest,Reina's Grave (Chest) #2,gr_1_1,Missable,Living Wall
Chest,Reina's Grave (Chest) #3,gr_1_4,Missable,Living Wall
Chest,Reina's Grave (Chest) #4,gr_1_2,Missable,Living Wall
Chest,Reina's Grave (Chest) #5,gr_1_5,Missable,Living Wall
Boss,Living Wall (Boss) #1,livingWall0,Not Missable,Living Wall
Boss,Living Wall (Boss) #2,livingWall1,Not Missable,Living Wall
Boss,Living Wall (Boss) #3,livingWall2,Not Missable,Living Wall
Chest,Marylea Lower (Chest) #1,ml_slaveFloor_2,Missable,Marylea
Chest,Marylea Lower (Chest) #2,ml_slaveFloor_1,Missable,Marylea
Deal,Holy Symbol (Deal),Holy Symbol,Not Missable,Marylea
Chest,Marylea (Chest) #1,ml_city_3,Missable,Marylea
Chest,Marylea (Chest) #2,ml_city_5,Missable,Marylea
Chest,Marylea (Chest) #3,ml_city_4,Missable,Marylea
Chest,Marylea (Chest) #4,ml_city_2,Missable,Marylea
Chest,Marylea (Chest) #5,ml_city_1,Missable,Marylea
Chest,Marylea Dungeon (Chest) #1,ml_dungeon1_1,Missable,Marylea
// KEY ITEM: KEY CARD A (Needed before or at this check)
Chest,Marylea Dungeon (Chest) #2,ml_dungeon1_6,Missable,Raphael
Chest,Marylea Dungeon (Chest) #3,ml_dungeon1_2,Missable,Raphael
// KEY ITEM: KEY CARD B (Needed before or at this check)
Chest,Marylea Dungeon (Chest) #4,ml_dungeon1_7,Missable,Raphael
Chest,Marylea Dungeon (Chest) #5,ml_dungeon1_10,Missable,Raphael
// KEY ITEM: KEY CARD C (Needed before or at this check)
Chest,Marylea Dungeon (Chest) #6,ml_dungeon1_8,Missable,Raphael
Chest,Marylea Dungeon (Chest) #7,ml_dungeon1_4,Missable,Raphael
// KEY ITEM: KEY CARD D (Needed before or at this check)
Chest,Marylea Dungeon (Chest) #8,ml_dungeon1_9,Missable,Raphael
Chest,Marylea Dungeon (Chest) #9,ml_dungeon1_11,Missable,Raphael
Chest,Marylea Dungeon (Chest) #10,ml_dungeon1_3,Missable,Raphael
Chest,Marylea Dungeon (Chest) #11,ml_dungeon1_5,Missable,Raphael
Chest,Marylea Dungeon (Chest) #12,ml_dungeon2_2,Missable,Raphael
Chest,Marylea Dungeon (Chest) #13,ml_dungeon2_3,Missable,Raphael
Chest,Marylea Dungeon (Chest) #15,ml_dungeon2_1,Missable,Raphael
Boss,Raphael (Boss) #1,raphael1,Not Missable,Raphael
Boss,Raphael (Boss) #2,raphael0,Not Missable,Raphael
Boss,Raphael (Boss) #3,raphael2,Not Missable,Raphael
Chest,Glenn's Mind (Chest) #1,dr_glenn02_1,Missable,Chained Echo
Chest,Glenn's Mind (Chest) #2,dr_glenn02_2,Missable,Chained Echo
Chest,Glenn's Mind (Chest) #3,dr_glenn02_3,Missable,Chained Echo
Chest,Glenn's Mind (Chest) #4,dr_glenn01_2,Missable,Chained Echo
Chest,Glenn's Mind (Chest) #5,dr_glenn01_1,Missable,Chained Echo
Boss,Behemoth (Boss) #1,behemoth0,Not Missable,Chained Echo
Boss,Behemoth (Boss) #2,behemoth1,Not Missable,Chained Echo
Boss,Behemoth (Boss) #3,behemoth2,Not Missable,Chained Echo
Boss,Chained Echo (Boss) #1,chainedEcho0,Not Missable,Chained Echo
Boss,Chained Echo (Boss) #2,chainedEcho1,Not Missable,Chained Echo
Boss,Chained Echo (Boss) #3,chainedEcho2,Not Missable,Chained Echo
Chest,Fiorwoods S (Chest) #2,fw_2_3_3,Not Missable,Maria
Board,Find chests in Fiorwoods (Board),Board71,Not Missable,Maria
// A WILL TO LIVE
Chest,Kortara Mountan Range SE (Chest) #2,kmr_3_3_5,Missable,Maria
Board,Quest: A Will to Live (Board),Board7,Not Missable,Maria
// END A WILL TO LIVE
// TWO WINGED ANGEL
// KEY ITEM: NORGART'S KEY
Chest,Kortara Mountan Range C (Chest) #1,kmr_2_2_1,Not Missable,Norgant
Board,Quest: Two Winged Angel (Board),Board144,Not Missable,Norgant
// END TWO WINGED ANGEL
// FALFALARAN
Chest,Inner Sactum (Chest) #2,is_4,Missable,Maria
Chest,Inner Sactum (Chest) #3,is_3,Missable,Maria
Chest,Inner Sactum (Chest) #4,is_6,Missable,Maria
Chest,Inner Sactum (Chest) #5,is_5,Missable,Maria
Chest,Inner Sactum (Chest) #6,is_1,Missable,Maria
Boss,Fairy Queen (Boss) #1,fairyQueen (1)0,Not Missable,Maria
Boss,Fairy Queen (Boss) #2,fairyQueen (1)1,Not Missable,Maria
Boss,Fairy Queen (Boss) #3,fairyQueen (1)2,Not Missable,Maria
Board,Quest: Falfalaran Sings the Fairy (Board),Board115,Not Missable,Maria
// END FALFALARAN
ChainBoard,Reward Board (Chain) 120,Chain120,Not Missable,Maria
// NO PLACE FOR HAPPY ENDINGS
Board,Explore Kortara (Board),Board164,Not Missable,Maria
Chest,Kortara Mountan Range NW (Chest) #1,kmr_1_1_6,Not Missable,Maria
Chest,Kortara Mountan Range NW (Chest) #2,kmr_1_1_2,Not Missable,Maria
Board,Find chests in Kortara (Board),Board184,Not Missable,Maria
Chest,Kortara Mountan Range NW (Chest) #3,kmr_1_1_5,Not Missable,Maria
Chest,Kortara Mountan Range NW (Chest) #4,kmr_1_1_4,Not Missable,Maria
Chest,Kortara Mountan Range NW (Chest) #5,kmr_1_1_3,Not Missable,Maria
Chest,Kortara Mountan Range NW (Chest) #6,kmr_1_1_1,Not Missable,Maria
Boss,Thoma (Boss) #1,thoma0,Not Missable,Maria
Boss,Thoma (Boss) #2,thoma1,Not Missable,Maria
Boss,Thoma (Boss) #3,thoma2,Not Missable,Maria
Board,Quest: No Place for Happy Ends (Board),Board161,Not Missable,Maria
// END NO PLACE FOR HAPPY ENDINGS
Chest,Hermit’s Isle outside (Chest) #1,hi_outside_5,Not Missable,Maria
Chest,Hermit’s Isle outside (Chest) #2,hi_outside_3,Not Missable,Maria
Chest,Hermit’s Isle outside (Chest) #3,hi_outside_4,Not Missable,Maria
Chest,Hermit’s Isle outside (Chest) #4,hi_outside_1,Not Missable,Maria
Chest,Hermit’s Isle outside (Chest) #5,hi_outside_2,Not Missable,Maria
Chest,Hermit's Isle inside (Chest) #1,hi_inside_1,Not Missable,Maria
// RAMINAS TOWER
Chest,Ramina's Tower (Chest) #1,rt_upperFloors_1,Not Missable,Maria
Chest,Ramina's Tower (Chest) #2,rt_upperFloors_2,Not Missable,Maria
Chest,Ramina's Tower (Chest) #3,rt_upperFloors_3,Not Missable,Maria
Chest,Ramina's Tower (Chest) #4,rt_upperFloors_8,Not Missable,Maria
Chest,Ramina's Tower (Chest) #5,rt_upperFloors_4,Not Missable,Maria
Chest,Ramina's Tower (Chest) #6,rt_upperFloors_9,Not Missable,Maria
Chest,Ramina's Tower (Chest) #7,rt_upperFloors_6,Not Missable,Maria
Chest,Ramina's Tower (Chest) #8,rt_upperFloors_7,Not Missable,Maria
Boss,Maria (Boss) #1,maria0,Not Missable,Maria
Boss,Maria (Boss) #2,maria1,Not Missable,Maria
Boss,Maria (Boss) #3,maria2,Not Missable,Maria
// END RAMINAS TOWER
Boss,Krakun (Boss) #1,krakun_tentacle10,Not Missable,Nhysa
Boss,Krakun (Boss) #2,krakun_tentacle11,Not Missable,Nhysa
Boss,Krakun (Boss) #3,krakun_tentacle12,Not Missable,Nhysa
Chest,Valandis Ocean (Chest) #1,va_ocean_3,Not Missable,Nhysa
Chest,Valandis Ocean (Chest) #2,va_ocean_2,Not Missable,Nhysa
Chest,Valandis Ocean (Chest) #3,va_ocean_4,Not Missable,Nhysa
// KEY ITEM: WIND TABLET
Chest,Valandis Ocean (Chest) #4,va_ocean_1,Not Missable,Nhysa
Boss,Armored Guardian (Boss) #1,armoredGuardian0,Not Missable,Nhysa
Boss,Armored Guardian (Boss) #2,armoredGuardian1,Not Missable,Nhysa
Boss,Armored Guardian (Boss) #3,armoredGuardian2,Not Missable,Nhysa
Board,Find the Secret Place (Board),Board135,Not Missable,Nhysa
Chest,Secret Place (Chest) #1,aa_1_2_7,Not Missable,Nhysa
Chest,Secret Place (Chest) #2,aa_1_2_3,Not Missable,Nhysa
Chest,Secret Place (Chest) #3,aa_1_2_6,Not Missable,Nhysa
Chest,Secret Place (Chest) #4,aa_1_2_5,Not Missable,Nhysa
Chest,Secret Place (Chest) #5,aa_1_2_1,Not Missable,Nhysa
Chest,Nhysa Lower (Chest) #1,nh_lowerCity03_2,Not Missable,Nhysa
Chest,Nhysa Lower (Chest) #2,nh_lowerCity03_3,Not Missable,Nhysa
Chest,Nhysa Lower (Chest) #3,nh_lowerCity03_1,Not Missable,Nhysa
Chest,Nhysa Lower (Chest) #4,nh_lowerCity03_4,Not Missable,Nhysa
Board,Find 5 Collectibles in Nhysa (Board),Board224,Not Missable,Nhysa
Chest,Nhysa (Buried) #1,nhburied_3,Not Missable,Nhysa
Chest,Nhysa park (Shiny),nhshiny_park_1,Not Missable,Nhysa
Chest,Nhysa park (Chest) #1,nh_park_4,Not Missable,Nhysa
Chest,Nhysa park (Chest) #2,nh_park_6,Not Missable,Nhysa
Chest,Nhysa park (Chest) #3,nh_park_3,Not Missable,Nhysa
Chest,Nhysa park (Chest) #4,nh_park_5,Not Missable,Nhysa
Chest,Nhysa park (Chest) #5,nh_park_2,Not Missable,Nhysa
Chest,Nhysa park (Chest) #6,nh_park_1,Not Missable,Nhysa
Board,Defeat 6 Blemmyaes (Board),Board223,Not Missable,Nhysa
Board,Find 10 Collectibles in Nhysa (Board),Board186,Not Missable,Nhysa
Chest,Nhysa Upper (Chest) #1,nh_upper_1,Not Missable,Nhysa
// KEY ITEM: SILVER KEY
Chest,Nhysa Upper (Chest) #2,nhupper_3,Not Missable,Black Sun
Chest,Nhysa Upper (Chest) #3,nh_upper_2,Not Missable,Black Sun
Chest,Nhysa (Buried) #2,nhburied_2,Not Missable,Black Sun
Chest,Nhysa Port (Chest) #1,nh_port_1,Not Missable,Black Sun
Chest,Nhysa Port (Chest) #2,nh_port_6,Not Missable,Black Sun
// KEY ITEM: BRONZE KEY GOTTEN FROM BOSS
Boss,Black Sun (Boss) #1,blackSun_galfried0,Not Missable,Black Sun
Boss,Black Sun (Boss) #2,blackSun_galfried1,Not Missable,Black Sun
Boss,Black Sun (Boss) #3,blackSun_galfried2,Not Missable,Black Sun
Chest,Nhysa Port (Chest) #3,nhport_7,Not Missable,Memory
Chest,Nhysa Port (Chest) #4,nhport_8,Not Missable,Memory
Chest,Nhysa Port (Chest) #5,nhport_9,Not Missable,Memory
Chest,Nhysa Port (Chest) #6,nhport_10,Not Missable,Memory
Chest,Nhysa Port (Chest) #7,nh_port_2,Not Missable,Memory
Chest,Nhysa Lower (Chest) #5,nh_lowerCity02_1,Not Missable,Memory
Chest,Nhysa Lower (Chest) #6,nh_lowerCity02_5,Not Missable,Memory
Deal,Light & Heavy Armor 9 (Deal),Light & Heavy Armor 9,Not Missable,Memory
Deal,Clothes & Robes 9 (Deal),Clothes & Robes 9,Not Missable,Memory
Deal,Nectar (Deal),Nectar,Not Missable,Memory
Deal,Ambrosia (Deal),Ambrosia,Not Missable,Memory
Deal,Rubber Duck (Deal),Rubber Duck,Not Missable,Memory
Deal,Ultra Material Pack (Deal),Ultra Material Pack,Not Missable,Memory
Chest,Nhysa (Buried) #3,nhburied_1,Not Missable,Memory
Board,Defeat 6 Earthworms (Board),Board187,Not Missable,Memory
Board,Find buried treasures in Nhysa (Board),Board227,Not Missable,Memory
Chest,Nhysa Port (Chest) #8,nh_port_4,Not Missable,Memory
Chest,Nhysa Port (Chest) #9,nh_port_3,Not Missable,Memory
Chest,Nhysa Port (Chest) #10,nh_port_5,Not Missable,Memory
Board,Explore Nhysa (Board),Board203,Not Missable,Memory
Chest,Nhysa Cellar (Chest) #1,nh_wineCellar_5,Not Missable,Memory
Chest,Nhysa Cellar (Chest) #2,nh_wineCellar_3,Not Missable,Memory
Board,Survive Earth Worms on foot (Board),Board183,Not Missable,Memory
Chest,Nhysa Lower (Chest) #7,nh_lowerCity02_2,Not Missable,Memory
Board,Defeat 8 Two Headed Wyverns (Board),Board188,Not Missable,Memory
Chest,Nhysa Lower (Chest) #8,nh_lowerCity02_3,Not Missable,Memory
Chest,Nhysa Lower (Chest) #9,nh_loverCity01_4,Not Missable,Memory
Chest,Nhysa Lower (Chest) #10,nh_loverCity01_1,Not Missable,Memory
Chest,Nhysa Cellar (Chest) #3,nh_wineCellar_6,Not Missable,Memory
Chest,Nhysa Cellar (Chest) #4,nh_wineCellar_7,Not Missable,Memory
Chest,Nhysa Cellar (Chest) #5,nh_wineCellar_8,Not Missable,Memory
Board,Find hidden caves in Nhysa (Board),Board185,Not Missable,Memory
Chest,Nhysa Lower (Chest) #11,nh_loverCity01_3,Not Missable,Memory
Chest,Nhysa Lower (Chest) #12,nh_loverCity01_2,Not Missable,Memory
Chest,Nhysa Cellar (Chest) #6,nh_wineCellar_1,Not Missable,Memory
Boss,Wiedergänger (Boss) #1,wiedergaenger0,Not Missable,Memory
Boss,Wiedergänger (Boss) #2,wiedergaenger1,Not Missable,Memory
Boss,Wiedergänger (Boss) #3,wiedergaenger2,Not Missable,Memory
Chest,Nhysa Mansion (Chest) #1,nh_manion_4,Not Missable,Memory
Chest,Nhysa Mansion (Chest) #2,nh_manion_1,Not Missable,Memory
Chest,Nhysa Mansion (Chest) #3,nh_manion_2,Not Missable,Memory
Boss,Memory (Boss) #1,memory0,Not Missable,Memory
Boss,Memory (Boss) #2,memory1,Not Missable,Memory
Boss,Memory (Boss) #3,memory2,Not Missable,Memory
// KEY ITEM: GOLD KEY
Chest,Nhysa Mansion (Chest) #4,nhmanion_3,Not Missable,Whyatt
Chest,Nhysa Cellar (Chest) #7,nh_wineCellar_4,Not Missable,Whyatt
Boss,Whyatt (Boss) #1,whyatt0,Not Missable,Whyatt
Boss,Whyatt (Boss) #2,whyatt1,Not Missable,Whyatt
Boss,Whyatt (Boss) #3,whyatt2,Not Missable,Whyatt
// KEY ITEM: ELEVATOR KEY
Chest,Nhysa Academy (Chest),nh_academy_1,Not Missable,Endgame
Chest,Nhysa Cellar (Chest) #8,nh_wineCellar_2,Not Missable,Endgame
Chest,Nhysa Cellar (Chest) #9,nh_wineCellar_9,Not Missable,Endgame
Board,Find chests in Nhysa (Board),Board206,Not Missable,Endgame
Deal,Shadow Garb (Deal),Shadow Garb,Not Missable,Endgame
Board,Quest: A Hammer Beating in the Sky (Board),Board239,Not Missable,Endgame
// USING KEY ITEM: ELEVATOR KEY
Chest,Ramina's Tower LF (Chest) #1,rt_lowerFloors_6,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #2,rt_lowerFloors_7,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #3,rt_lowerFloors_4,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #4,rt_lowerFloors_3,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #5,rt_lowerFloors_2,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #6,rt_lowerFloors_8,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #7,rt_lowerFloors_1,Not Missable,Eastern Ograne
Chest,Ramina's Tower LF (Chest) #8,rt_lowerFloors_5,Not Missable,Eastern Ograne
Board,Unique: Bog the Real Gob (Board),Board151,Not Missable,Eastern Ograne
// USING KEY ITEM: CHARON'S COIN BAG (WHILE INSIDE THE AREA RESTRICTED BY ELEVATOR KEY)
Chest,Ograne Grottos E (Chest) #1,og_3_2_1,Not Missable,Baalrut
Board,Explore Ograne Grottos (Board),Board169,Not Missable,Baalrut
Chest,Ograne Grottos SE (Chest) #1,og_3_3_3,Not Missable,Baalrut
Chest,Ograne Grottos SE (Chest) #2,og_3_3_5,Not Missable,Baalrut
Board,Find hidden caves in Ograne Grottos (Board),Board132,Not Missable,Baalrut
Chest,Ograne Grottos SE (Chest) #3,og_3_3_2,Not Missable,Baalrut
Chest,Ograne Grottos SE (Chest) #4,og_3_3_4,Not Missable,Baalrut
Board,Find chests in Ograne Grottos (Board),Board88,Not Missable,Baalrut
Board,Defeat 15 Vampires (Board),Board108,Not Missable,Baalrut
Board,Defeat 4 Hana Dolls (Board),Board86,Not Missable,Baalrut
Chest,Ograne Grottos SE (Chest) #5,og_3_3_1,Not Missable,Baalrut
Boss,Randomage (Boss) #1,randomage (1)0,Not Missable,Baalrut
Boss,Randomage (Boss) #2,randomage (1)1,Not Missable,Baalrut
Boss,Randomage (Boss) #3,randomage (1)2,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #1,br_tunnel_7,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #2,br_tunnel_3,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #3,br_tunnel_4,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #4,br_tunnel_8,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #5,br_tunnel_5,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #6,br_tunnel_6,Not Missable,Baalrut
Chest,Rohlan Fields NE (Chest) #4,rf_3_1_5,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #7,br_tunnel_1,Not Missable,Baalrut
Boss,Chel (Boss) #1,chel0,Not Missable,Baalrut
Boss,Chel (Boss) #2,chel1,Not Missable,Baalrut
Boss,Chel (Boss) #3,chel2,Not Missable,Baalrut
Chest,Eastern Sewers (Chest) #1,ns_east_b1_2,Not Missable,Baalrut
Chest,Eastern Sewers (Chest) #2,ns_east_b1_4,Not Missable,Baalrut
// KEY ITEM: WATER HANDLE
Chest,Eastern Sewers (Chest) #3,ns_east_b2_2,Not Missable,Sewers
Chest,Eastern Sewers (Chest) #4,ns_east_b2_1,Not Missable,Sewers
Deal,Ultimate Trove (Deal),Ultimate Trove,Not Missable,Sewers
Deal,Ultimate Heavy Armor (Deal),Ultimate Heavy Armor,Not Missable,Sewers
Chest,Eastern Sewers (Chest) #5,ns_east_b1_3,Not Missable,Sewers
// REQUIRES KEY ITEM: WATER HANDLE
Chest,Eastern Sewers (Chest) #6,ns_east_b1_1,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #8,br_tunnel_2,Not Missable,Baalrut
Chest,Baalrut Tunnel (Chest) #9,br_tunnel_9,Not Missable,Baalrut
Board,Take a trip by boat (Board),Board91,Not Missable,Baalrut
Board,Defeat 20 Purple Pig Ears (Board),Board225,Not Missable,Baalrut
Boss,Boutrous (Boss) #1,boutrous0,Not Missable,Baalrut
Boss,Boutrous (Boss) #2,boutrous1,Not Missable,Baalrut
Boss,Boutrous (Boss) #3,boutrous2,Not Missable,Baalrut
// END CHARON'S COIN BAG AND ELEVATOR KEY
// ASSASSIN GIRL CAN BE DONE EARLIER, BUT STILL HERE BECAUSE TOO MUCH WORK TO REROUTE
Boss,Assassin Girl (Boss) #1,assassineGirl0,Not Missable,Endgame
Boss,Assassin Girl (Boss) #2,assassineGirl1,Not Missable,Endgame
Boss,Assassin Girl (Boss) #3,assassineGirl2,Not Missable,Endgame
Board,Find all elemental tablets (Board),Board111,Not Missable,Endgame
Deal,Ultimate Clothes (Deal),Ultimate Clothes,Not Missable,Endgame
Deal,Ultimate Robes (Deal),Ultimate Robes,Not Missable,Endgame
Deal,Ultimate Light Armor (Deal),Ultimate Light Armor,Not Missable,Endgame
Deal,Ultimate Material Pack (Deal),Ultimate Material Pack,Not Missable,Endgame
Boss,Old King Gaemdriel (Boss) #1,oldKingGaemdriel0,Not Missable,Endgame
Boss,Old King Gaemdriel (Boss) #2,oldKingGaemdriel1,Not Missable,Endgame
Boss,Old King Gaemdriel (Boss) #3,oldKingGaemdriel2,Not Missable,Endgame
Board,Unique: God King Gaemdriel (Board),Board131,Not Missable,Endgame
Board,Defeat all Unique Monsters (Board),Board95,Not Missable,Endgame
Boss,Labrodia-Dervinas (Boss) #1,kylian0,Not Missable,Endgame
Boss,Labrodia-Dervinas (Boss) #2,kylian1,Not Missable,Endgame
Boss,Labrodia-Dervinas (Boss) #3,kylian2,Not Missable,Endgame
Boss,Alfreed (Boss) #1,alf_tank0,Not Missable,Endgame
Boss,Alfreed (Boss) #2,alf_tank1,Not Missable,Endgame
Boss,Alfreed (Boss) #3,alf_tank2,Not Missable,Endgame
'''

# Map string classifications to `LocationProgressType`
progress_type_map = {
    "Not Missable": LocationProgressType.DEFAULT,
    "Missable": LocationProgressType.EXCLUDED,
}

# Parse the location data from the text
LOCATION_ID_START = 8501000
current_id = LOCATION_ID_START
for line in locations_txt.strip().splitlines():
    if line.startswith("//"):  # Skip comments
        continue
    parts = line.split(",")
    if len(parts) < 5:
        print(f"Malformed line: {line}")  # Debugging output
        continue

    location_data_table.append(ChainedEchoesLocation(
        id=current_id,
        location_type=parts[0].strip(),
        user_friendly_name=parts[1].strip(),
        game_id=parts[2].strip(),  # Only for reference; not used in APWorld
        classification=parts[3].strip(),
        region=parts[4].strip(),
    ))
    current_id += 1


def create_locations(world: "ChainedEchoesWorld"):
    """
    Dynamically create locations for the game world and assign them to regions.
    """
    for location in location_data_table:
        # Use the user-friendly name as the location name
        location_name = location.user_friendly_name

        # Determine the progress type based on classification
        progress_type = progress_type_map.get(location.classification, LocationProgressType.DEFAULT)

        # Get the region where the location belongs
        try:
            region = world.multiworld.get_region(location.region, world.player)
        except KeyError:
            raise ValueError(f"Region '{location.region}' not found for location '{location_name}'.")

        # Create the location and assign it to the region
        game_location = Location(world.player, location_name, location.id, region)
        game_location.progress_type = progress_type

        # Assign the location to its parent region
        region.locations.append(game_location)
        
        
location_table: Dict[str, int] = {location.user_friendly_name: location.id for location in location_data_table}

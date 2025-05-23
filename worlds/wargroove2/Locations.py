from BaseClasses import Location
from typing import Dict, Optional

location_table: Dict[str, Optional[int]] = {
    "Humble Beginnings Rebirth: Talk to Nadia": 253001,
    "Humble Beginnings Rebirth: Victory": 253002,
    "Humble Beginnings Rebirth: Good Dog": 253003,
    #########################################################
    "Nuru's Vengeance: Victory": 253005,
    "Nuru's Vengeance: Spearman Destroys the Gate": 253006,
    "Nuru's Vengeance: Defeat all Dogs": 253007,
    "Cherrystone Landing: Smacked a Trebuchet": 253008,
    "Cherrystone Landing: Smacked a Fortified Village": 253009,
    "Cherrystone Landing: Victory": 253010,
    "Den-Two-Away: Victory": 253011,
    "Den-Two-Away: Commander Captures the Lumbermill": 253012,
    "Skydiving: Victory": 253013,
    "Skydiving: Dragon Defeats Stronghold": 253014,
    "Terrible Tributaries: Victory": 253015,
    "Terrible Tributaries: Swimming Knights": 253016,
    "Terrible Tributaries: Steal Code Names": 253017,
    "Beached: Victory": 253018,
    "Beached: Turtle Power": 253019,
    "Beached: Happy Turtle": 253020,
    "Riflemen Blockade: Victory": 253021,
    "Riflemen Blockade: From the Mountains": 253022,
    "Riflemen Blockade: To the Road": 253023,
    "Wagon Freeway: Victory": 253024,
    "Wagon Freeway: All Mine Now": 253025,
    "Wagon Freeway: Pigeon Carrier": 253026,
    "Kraken Strait: Victory": 253027,
    "Kraken Strait: Well Defended": 253028,
    "Kraken Strait: Clipped Wings": 253029,
    "A Ribbitting Time: Victory": 253030,
    "A Ribbitting Time: Leap Frog": 253031,
    "A Ribbitting Time: Frogway Robbery": 253032,
    "Precarious Cliffs: Victory": 253033,
    "Precarious Cliffs: No Crit for You": 253034,
    "Precarious Cliffs: Out Ranged": 253035,
    "Grand Theft Village: Victory": 253036,
    "Grand Theft Village: Stand Tall": 253037,
    "Grand Theft Village: Pillager": 253038,
    "Bridge Brigade: Victory": 253039,
    "Bridge Brigade: From the Depths": 253040,
    "Bridge Brigade: Back to the Depths": 253041,
    "Swimming at the Docks: Victory": 253042,
    "Swimming at the Docks: Dogs Counter Knights": 253043,
    "Swimming at the Docks: Kayaking": 253044,
    "Ancient Discoveries: Victory": 253045,
    "Ancient Discoveries: So many Choices": 253046,
    "Ancient Discoveries: Height Advantage": 253047,
    "Observation Isle: Victory": 253048,
    "Observation Isle: Become the Watcher": 253049,
    "Observation Isle: Execute the Watcher": 253050,
    "Majestic Mountain: Victory": 253051,
    "Majestic Mountain: Mountain Climbing": 253052,
    "Majestic Mountain: Legend of the Mountains": 253053,
    "Floran Trap: Victory": 253054,
    "Floran Trap: Means of Production": 253055,
    "Floran Trap: Aerial Reconnaissance": 253056,
    #########################################################
    "Slippery Bridge: Victory": 253300,
    "Slippery Bridge: Control all Sea Villages": 253301,
    #########################################################
    "Spire Fire: Victory": 253305,
    "Spire Fire: Kill Enemy Sky Rider": 253306,
    "Spire Fire: Win without losing your Dragon": 253307,
    #########################################################
    "Sunken Forest: Victory": 253310,
    "Sunken Forest: High Ground": 253311,
    "Sunken Forest: Coastal Siege": 253312,
    #########################################################
    "Tenri\'s Mistake: Victory": 253315,
    "Tenri\'s Mistake: Mighty Barracks": 253316,
    "Tenri\'s Mistake: Commander Arrives": 253317,
    #########################################################
    "Enmity Cliffs: Victory": 253320,
    "Enmity Cliffs: Spear Flood": 253321,
    "Enmity Cliffs: Across the Gap": 253322,
    #########################################################
    "Portal Peril: Victory": 253325,
    "Portal Peril: Unleash the Hounds": 253326,
    "Portal Peril: Overcharged": 253327,
    #########################################################
    "Towers of the Abyss: Victory": 253330,
    "Towers of the Abyss: Siege Master": 253331,
    "Towers of the Abyss: Perfect Defense": 253332,
    #########################################################
    "Gnarled Mountaintop: Victory": 253335,
    "Gnarled Mountaintop: Watch the Watchtower": 253336,
    "Gnarled Mountaintop: Vine Skip": 253337,
    #########################################################
    "Gold Rush: Victory": 253340,
    "Gold Rush: Lumber Island": 253341,
    "Gold Rush: Starglass Rush": 253342,
    #########################################################
    "Finishing Blow: Victory": 253345,
    "Finishing Blow: Mass Destruction": 253346,
    "Finishing Blow: Defortification": 253347,
    #########################################################
    "Frantic Inlet: Victory": 253350,
    "Frantic Inlet: Plug the Gap": 253351,
    "Frantic Inlet: Portal Detour": 253352,
    #########################################################
    "Operation Seagull: Victory": 253355,
    "Operation Seagull: Crack the Crystal": 253356,
    "Operation Seagull: Counter Break": 253357,
    #########################################################
    "Air Support: Victory": 253360,
    "Air Support: Roadkill": 253361,
    "Air Support: Flight Economy": 253362,
    #########################################################
    "Fortification: Victory": 253365,
    "Fortification: Hyper Repair": 253366,
    "Fortification: Defensive Artillery": 253367,
    #########################################################
    "Split Valley: Victory": 253370,
    "Split Valley: Longshot": 253371,
    "Split Valley: Ranged Trinity": 253372,
    #########################################################
    "Humble Beginnings Rebirth: Talk to Nadia Extra 1": 260000,
    "Humble Beginnings Rebirth: Talk to Nadia Extra 2": 260001,
    "Humble Beginnings Rebirth: Talk to Nadia Extra 3": 260002,
    "Humble Beginnings Rebirth: Talk to Nadia Extra 4": 260003,
    "Humble Beginnings Rebirth: Victory Extra 1": 260004,
    "Humble Beginnings Rebirth: Victory Extra 2": 260005,
    "Humble Beginnings Rebirth: Victory Extra 3": 260006,
    "Humble Beginnings Rebirth: Victory Extra 4": 260007,
    "Humble Beginnings Rebirth: Good Dog Extra 1": 260008,
    "Humble Beginnings Rebirth: Good Dog Extra 2": 260009,
    "Humble Beginnings Rebirth: Good Dog Extra 3": 260010,
    "Humble Beginnings Rebirth: Good Dog Extra 4": 260011,
    "Nuru's Vengeance: Victory Extra 1": 260012,
    "Nuru's Vengeance: Victory Extra 2": 260013,
    "Nuru's Vengeance: Victory Extra 3": 260014,
    "Nuru's Vengeance: Victory Extra 4": 260015,
    "Nuru's Vengeance: Spearman Destroys the Gate Extra 1": 260016,
    "Nuru's Vengeance: Spearman Destroys the Gate Extra 2": 260017,
    "Nuru's Vengeance: Spearman Destroys the Gate Extra 3": 260018,
    "Nuru's Vengeance: Spearman Destroys the Gate Extra 4": 260019,
    "Nuru's Vengeance: Defeat all Dogs Extra 1": 260020,
    "Nuru's Vengeance: Defeat all Dogs Extra 2": 260021,
    "Nuru's Vengeance: Defeat all Dogs Extra 3": 260022,
    "Nuru's Vengeance: Defeat all Dogs Extra 4": 260023,
    "Cherrystone Landing: Smacked a Trebuchet Extra 1": 260024,
    "Cherrystone Landing: Smacked a Trebuchet Extra 2": 260025,
    "Cherrystone Landing: Smacked a Trebuchet Extra 3": 260026,
    "Cherrystone Landing: Smacked a Trebuchet Extra 4": 260027,
    "Cherrystone Landing: Smacked a Fortified Village Extra 1": 260028,
    "Cherrystone Landing: Smacked a Fortified Village Extra 2": 260029,
    "Cherrystone Landing: Smacked a Fortified Village Extra 3": 260030,
    "Cherrystone Landing: Smacked a Fortified Village Extra 4": 260031,
    "Cherrystone Landing: Victory Extra 1": 260032,
    "Cherrystone Landing: Victory Extra 2": 260033,
    "Cherrystone Landing: Victory Extra 3": 260034,
    "Cherrystone Landing: Victory Extra 4": 260035,
    "Den-Two-Away: Victory Extra 1": 260036,
    "Den-Two-Away: Victory Extra 2": 260037,
    "Den-Two-Away: Victory Extra 3": 260038,
    "Den-Two-Away: Victory Extra 4": 260039,
    "Den-Two-Away: Commander Captures the Lumbermill Extra 1": 260040,
    "Den-Two-Away: Commander Captures the Lumbermill Extra 2": 260041,
    "Den-Two-Away: Commander Captures the Lumbermill Extra 3": 260042,
    "Den-Two-Away: Commander Captures the Lumbermill Extra 4": 260043,
    "Skydiving: Victory Extra 1": 260044,
    "Skydiving: Victory Extra 2": 260045,
    "Skydiving: Victory Extra 3": 260046,
    "Skydiving: Victory Extra 4": 260047,
    "Skydiving: Dragon Defeats Stronghold Extra 1": 260048,
    "Skydiving: Dragon Defeats Stronghold Extra 2": 260049,
    "Skydiving: Dragon Defeats Stronghold Extra 3": 260050,
    "Skydiving: Dragon Defeats Stronghold Extra 4": 260051,
    "Terrible Tributaries: Victory Extra 1": 260052,
    "Terrible Tributaries: Victory Extra 2": 260053,
    "Terrible Tributaries: Victory Extra 3": 260054,
    "Terrible Tributaries: Victory Extra 4": 260055,
    "Terrible Tributaries: Swimming Knights Extra 1": 260056,
    "Terrible Tributaries: Swimming Knights Extra 2": 260057,
    "Terrible Tributaries: Swimming Knights Extra 3": 260058,
    "Terrible Tributaries: Swimming Knights Extra 4": 260059,
    "Terrible Tributaries: Steal Code Names Extra 1": 260060,
    "Terrible Tributaries: Steal Code Names Extra 2": 260061,
    "Terrible Tributaries: Steal Code Names Extra 3": 260062,
    "Terrible Tributaries: Steal Code Names Extra 4": 260063,
    "Beached: Victory Extra 1": 260064,
    "Beached: Victory Extra 2": 260065,
    "Beached: Victory Extra 3": 260066,
    "Beached: Victory Extra 4": 260067,
    "Beached: Turtle Power Extra 1": 260068,
    "Beached: Turtle Power Extra 2": 260069,
    "Beached: Turtle Power Extra 3": 260070,
    "Beached: Turtle Power Extra 4": 260071,
    "Beached: Happy Turtle Extra 1": 260072,
    "Beached: Happy Turtle Extra 2": 260073,
    "Beached: Happy Turtle Extra 3": 260074,
    "Beached: Happy Turtle Extra 4": 260075,
    "Riflemen Blockade: Victory Extra 1": 260076,
    "Riflemen Blockade: Victory Extra 2": 260077,
    "Riflemen Blockade: Victory Extra 3": 260078,
    "Riflemen Blockade: Victory Extra 4": 260079,
    "Riflemen Blockade: From the Mountains Extra 1": 260080,
    "Riflemen Blockade: From the Mountains Extra 2": 260081,
    "Riflemen Blockade: From the Mountains Extra 3": 260082,
    "Riflemen Blockade: From the Mountains Extra 4": 260083,
    "Riflemen Blockade: To the Road Extra 1": 260084,
    "Riflemen Blockade: To the Road Extra 2": 260085,
    "Riflemen Blockade: To the Road Extra 3": 260086,
    "Riflemen Blockade: To the Road Extra 4": 260087,
    "Wagon Freeway: Victory Extra 1": 260088,
    "Wagon Freeway: Victory Extra 2": 260089,
    "Wagon Freeway: Victory Extra 3": 260090,
    "Wagon Freeway: Victory Extra 4": 260091,
    "Wagon Freeway: All Mine Now Extra 1": 260092,
    "Wagon Freeway: All Mine Now Extra 2": 260093,
    "Wagon Freeway: All Mine Now Extra 3": 260094,
    "Wagon Freeway: All Mine Now Extra 4": 260095,
    "Wagon Freeway: Pigeon Carrier Extra 1": 260096,
    "Wagon Freeway: Pigeon Carrier Extra 2": 260097,
    "Wagon Freeway: Pigeon Carrier Extra 3": 260098,
    "Wagon Freeway: Pigeon Carrier Extra 4": 260099,
    "Kraken Strait: Victory Extra 1": 260100,
    "Kraken Strait: Victory Extra 2": 260101,
    "Kraken Strait: Victory Extra 3": 260102,
    "Kraken Strait: Victory Extra 4": 260103,
    "Kraken Strait: Well Defended Extra 1": 260104,
    "Kraken Strait: Well Defended Extra 2": 260105,
    "Kraken Strait: Well Defended Extra 3": 260106,
    "Kraken Strait: Well Defended Extra 4": 260107,
    "Kraken Strait: Clipped Wings Extra 1": 260108,
    "Kraken Strait: Clipped Wings Extra 2": 260109,
    "Kraken Strait: Clipped Wings Extra 3": 260110,
    "Kraken Strait: Clipped Wings Extra 4": 260111,
    "A Ribbitting Time: Victory Extra 1": 260112,
    "A Ribbitting Time: Victory Extra 2": 260113,
    "A Ribbitting Time: Victory Extra 3": 260114,
    "A Ribbitting Time: Victory Extra 4": 260115,
    "A Ribbitting Time: Leap Frog Extra 1": 260116,
    "A Ribbitting Time: Leap Frog Extra 2": 260117,
    "A Ribbitting Time: Leap Frog Extra 3": 260118,
    "A Ribbitting Time: Leap Frog Extra 4": 260119,
    "A Ribbitting Time: Frogway Robbery Extra 1": 260120,
    "A Ribbitting Time: Frogway Robbery Extra 2": 260121,
    "A Ribbitting Time: Frogway Robbery Extra 3": 260122,
    "A Ribbitting Time: Frogway Robbery Extra 4": 260123,
    "Precarious Cliffs: Victory Extra 1": 260124,
    "Precarious Cliffs: Victory Extra 2": 260125,
    "Precarious Cliffs: Victory Extra 3": 260126,
    "Precarious Cliffs: Victory Extra 4": 260127,
    "Precarious Cliffs: No Crit for You Extra 1": 260128,
    "Precarious Cliffs: No Crit for You Extra 2": 260129,
    "Precarious Cliffs: No Crit for You Extra 3": 260130,
    "Precarious Cliffs: No Crit for You Extra 4": 260131,
    "Precarious Cliffs: Out Ranged Extra 1": 260132,
    "Precarious Cliffs: Out Ranged Extra 2": 260133,
    "Precarious Cliffs: Out Ranged Extra 3": 260134,
    "Precarious Cliffs: Out Ranged Extra 4": 260135,
    "Grand Theft Village: Victory Extra 1": 260136,
    "Grand Theft Village: Victory Extra 2": 260137,
    "Grand Theft Village: Victory Extra 3": 260138,
    "Grand Theft Village: Victory Extra 4": 260139,
    "Grand Theft Village: Stand Tall Extra 1": 260140,
    "Grand Theft Village: Stand Tall Extra 2": 260141,
    "Grand Theft Village: Stand Tall Extra 3": 260142,
    "Grand Theft Village: Stand Tall Extra 4": 260143,
    "Grand Theft Village: Pillager Extra 1": 260144,
    "Grand Theft Village: Pillager Extra 2": 260145,
    "Grand Theft Village: Pillager Extra 3": 260146,
    "Grand Theft Village: Pillager Extra 4": 260147,
    "Bridge Brigade: Victory Extra 1": 260148,
    "Bridge Brigade: Victory Extra 2": 260149,
    "Bridge Brigade: Victory Extra 3": 260150,
    "Bridge Brigade: Victory Extra 4": 260151,
    "Bridge Brigade: From the Depths Extra 1": 260152,
    "Bridge Brigade: From the Depths Extra 2": 260153,
    "Bridge Brigade: From the Depths Extra 3": 260154,
    "Bridge Brigade: From the Depths Extra 4": 260155,
    "Bridge Brigade: Back to the Depths Extra 1": 260156,
    "Bridge Brigade: Back to the Depths Extra 2": 260157,
    "Bridge Brigade: Back to the Depths Extra 3": 260158,
    "Bridge Brigade: Back to the Depths Extra 4": 260159,
    "Slippery Bridge: Victory Extra 1": 260160,
    "Slippery Bridge: Victory Extra 2": 260161,
    "Slippery Bridge: Victory Extra 3": 260162,
    "Slippery Bridge: Victory Extra 4": 260163,
    "Slippery Bridge: Control all Sea Villages Extra 1": 260164,
    "Slippery Bridge: Control all Sea Villages Extra 2": 260165,
    "Slippery Bridge: Control all Sea Villages Extra 3": 260166,
    "Slippery Bridge: Control all Sea Villages Extra 4": 260167,
    "Spire Fire: Victory Extra 1": 260168,
    "Spire Fire: Victory Extra 2": 260169,
    "Spire Fire: Victory Extra 3": 260170,
    "Spire Fire: Victory Extra 4": 260171,
    "Spire Fire: Kill Enemy Sky Rider Extra 1": 260172,
    "Spire Fire: Kill Enemy Sky Rider Extra 2": 260173,
    "Spire Fire: Kill Enemy Sky Rider Extra 3": 260174,
    "Spire Fire: Kill Enemy Sky Rider Extra 4": 260175,
    "Spire Fire: Win without losing your Dragon Extra 1": 260176,
    "Spire Fire: Win without losing your Dragon Extra 2": 260177,
    "Spire Fire: Win without losing your Dragon Extra 3": 260178,
    "Spire Fire: Win without losing your Dragon Extra 4": 260179,
    "Sunken Forest: Victory Extra 1": 260180,
    "Sunken Forest: Victory Extra 2": 260181,
    "Sunken Forest: Victory Extra 3": 260182,
    "Sunken Forest: Victory Extra 4": 260183,
    "Sunken Forest: High Ground Extra 1": 260184,
    "Sunken Forest: High Ground Extra 2": 260185,
    "Sunken Forest: High Ground Extra 3": 260186,
    "Sunken Forest: High Ground Extra 4": 260187,
    "Sunken Forest: Coastal Siege Extra 1": 260188,
    "Sunken Forest: Coastal Siege Extra 2": 260189,
    "Sunken Forest: Coastal Siege Extra 3": 260190,
    "Sunken Forest: Coastal Siege Extra 4": 260191,
    "Tenri's Mistake: Victory Extra 1": 260192,
    "Tenri's Mistake: Victory Extra 2": 260193,
    "Tenri's Mistake: Victory Extra 3": 260194,
    "Tenri's Mistake: Victory Extra 4": 260195,
    "Tenri's Mistake: Mighty Barracks Extra 1": 260196,
    "Tenri's Mistake: Mighty Barracks Extra 2": 260197,
    "Tenri's Mistake: Mighty Barracks Extra 3": 260198,
    "Tenri's Mistake: Mighty Barracks Extra 4": 260199,
    "Tenri's Mistake: Commander Arrives Extra 1": 260200,
    "Tenri's Mistake: Commander Arrives Extra 2": 260201,
    "Tenri's Mistake: Commander Arrives Extra 3": 260202,
    "Tenri's Mistake: Commander Arrives Extra 4": 260203,
    "Enmity Cliffs: Victory Extra 1": 260204,
    "Enmity Cliffs: Victory Extra 2": 260205,
    "Enmity Cliffs: Victory Extra 3": 260206,
    "Enmity Cliffs: Victory Extra 4": 260207,
    "Enmity Cliffs: Spear Flood Extra 1": 260208,
    "Enmity Cliffs: Spear Flood Extra 2": 260209,
    "Enmity Cliffs: Spear Flood Extra 3": 260210,
    "Enmity Cliffs: Spear Flood Extra 4": 260211,
    "Enmity Cliffs: Across the Gap Extra 1": 260212,
    "Enmity Cliffs: Across the Gap Extra 2": 260213,
    "Enmity Cliffs: Across the Gap Extra 3": 260214,
    "Enmity Cliffs: Across the Gap Extra 4": 260215,
    "Portal Peril: Victory Extra 1": 260216,
    "Portal Peril: Victory Extra 2": 260217,
    "Portal Peril: Victory Extra 3": 260218,
    "Portal Peril: Victory Extra 4": 260219,
    "Portal Peril: Unleash the Hounds Extra 1": 260220,
    "Portal Peril: Unleash the Hounds Extra 2": 260221,
    "Portal Peril: Unleash the Hounds Extra 3": 260222,
    "Portal Peril: Unleash the Hounds Extra 4": 260223,
    "Portal Peril: Overcharged Extra 1": 260224,
    "Portal Peril: Overcharged Extra 2": 260225,
    "Portal Peril: Overcharged Extra 3": 260226,
    "Portal Peril: Overcharged Extra 4": 260227,
    "Towers of the Abyss: Victory Extra 1": 260228,
    "Towers of the Abyss: Victory Extra 2": 260229,
    "Towers of the Abyss: Victory Extra 3": 260230,
    "Towers of the Abyss: Victory Extra 4": 260231,
    "Towers of the Abyss: Siege Master Extra 1": 260232,
    "Towers of the Abyss: Siege Master Extra 2": 260233,
    "Towers of the Abyss: Siege Master Extra 3": 260234,
    "Towers of the Abyss: Siege Master Extra 4": 260235,
    "Towers of the Abyss: Perfect Defense Extra 1": 260236,
    "Towers of the Abyss: Perfect Defense Extra 2": 260237,
    "Towers of the Abyss: Perfect Defense Extra 3": 260238,
    "Towers of the Abyss: Perfect Defense Extra 4": 260239,
    "Gnarled Mountaintop: Victory Extra 1": 260240,
    "Gnarled Mountaintop: Victory Extra 2": 260241,
    "Gnarled Mountaintop: Victory Extra 3": 260242,
    "Gnarled Mountaintop: Victory Extra 4": 260243,
    "Gnarled Mountaintop: Watch the Watchtower Extra 1": 260244,
    "Gnarled Mountaintop: Watch the Watchtower Extra 2": 260245,
    "Gnarled Mountaintop: Watch the Watchtower Extra 3": 260246,
    "Gnarled Mountaintop: Watch the Watchtower Extra 4": 260247,
    "Gnarled Mountaintop: Vine Skip Extra 1": 260248,
    "Gnarled Mountaintop: Vine Skip Extra 2": 260249,
    "Gnarled Mountaintop: Vine Skip Extra 3": 260250,
    "Gnarled Mountaintop: Vine Skip Extra 4": 260251,
    "Gold Rush: Victory Extra 1": 260252,
    "Gold Rush: Victory Extra 2": 260253,
    "Gold Rush: Victory Extra 3": 260254,
    "Gold Rush: Victory Extra 4": 260255,
    "Gold Rush: Lumber Island Extra 1": 260256,
    "Gold Rush: Lumber Island Extra 2": 260257,
    "Gold Rush: Lumber Island Extra 3": 260258,
    "Gold Rush: Lumber Island Extra 4": 260259,
    "Gold Rush: Starglass Rush Extra 1": 260260,
    "Gold Rush: Starglass Rush Extra 2": 260261,
    "Gold Rush: Starglass Rush Extra 3": 260262,
    "Gold Rush: Starglass Rush Extra 4": 260263,
    "Finishing Blow: Victory Extra 1": 260264,
    "Finishing Blow: Victory Extra 2": 260265,
    "Finishing Blow: Victory Extra 3": 260266,
    "Finishing Blow: Victory Extra 4": 260267,
    "Finishing Blow: Mass Destruction Extra 1": 260268,
    "Finishing Blow: Mass Destruction Extra 2": 260269,
    "Finishing Blow: Mass Destruction Extra 3": 260270,
    "Finishing Blow: Mass Destruction Extra 4": 260271,
    "Finishing Blow: Defortification Extra 1": 260272,
    "Finishing Blow: Defortification Extra 2": 260273,
    "Finishing Blow: Defortification Extra 3": 260274,
    "Finishing Blow: Defortification Extra 4": 260275,
    "Frantic Inlet: Victory Extra 1": 260276,
    "Frantic Inlet: Victory Extra 2": 260277,
    "Frantic Inlet: Victory Extra 3": 260278,
    "Frantic Inlet: Victory Extra 4": 260279,
    "Frantic Inlet: Plug the Gap Extra 1": 260280,
    "Frantic Inlet: Plug the Gap Extra 2": 260281,
    "Frantic Inlet: Plug the Gap Extra 3": 260282,
    "Frantic Inlet: Plug the Gap Extra 4": 260283,
    "Frantic Inlet: Portal Detour Extra 1": 260284,
    "Frantic Inlet: Portal Detour Extra 2": 260285,
    "Frantic Inlet: Portal Detour Extra 3": 260286,
    "Frantic Inlet: Portal Detour Extra 4": 260287,
    "Operation Seagull: Victory Extra 1": 260288,
    "Operation Seagull: Victory Extra 2": 260289,
    "Operation Seagull: Victory Extra 3": 260290,
    "Operation Seagull: Victory Extra 4": 260291,
    "Operation Seagull: Crack the Crystal Extra 1": 260292,
    "Operation Seagull: Crack the Crystal Extra 2": 260293,
    "Operation Seagull: Crack the Crystal Extra 3": 260294,
    "Operation Seagull: Crack the Crystal Extra 4": 260295,
    "Operation Seagull: Counter Break Extra 1": 260296,
    "Operation Seagull: Counter Break Extra 2": 260297,
    "Operation Seagull: Counter Break Extra 3": 260298,
    "Operation Seagull: Counter Break Extra 4": 260299,
    "Air Support: Victory Extra 1": 260300,
    "Air Support: Victory Extra 2": 260301,
    "Air Support: Victory Extra 3": 260302,
    "Air Support: Victory Extra 4": 260303,
    "Air Support: Roadkill Extra 1": 260304,
    "Air Support: Roadkill Extra 2": 260305,
    "Air Support: Roadkill Extra 3": 260306,
    "Air Support: Roadkill Extra 4": 260307,
    "Air Support: Flight Economy Extra 1": 260308,
    "Air Support: Flight Economy Extra 2": 260309,
    "Air Support: Flight Economy Extra 3": 260310,
    "Air Support: Flight Economy Extra 4": 260311,
    "Fortification: Victory Extra 1": 260312,
    "Fortification: Victory Extra 2": 260313,
    "Fortification: Victory Extra 3": 260314,
    "Fortification: Victory Extra 4": 260315,
    "Fortification: Hyper Repair Extra 1": 260316,
    "Fortification: Hyper Repair Extra 2": 260317,
    "Fortification: Hyper Repair Extra 3": 260318,
    "Fortification: Hyper Repair Extra 4": 260319,
    "Fortification: Defensive Artillery Extra 1": 260320,
    "Fortification: Defensive Artillery Extra 2": 260321,
    "Fortification: Defensive Artillery Extra 3": 260322,
    "Fortification: Defensive Artillery Extra 4": 260323,
    "Split Valley: Victory Extra 1": 260324,
    "Split Valley: Victory Extra 2": 260325,
    "Split Valley: Victory Extra 3": 260326,
    "Split Valley: Victory Extra 4": 260327,
    "Split Valley: Longshot Extra 1": 260328,
    "Split Valley: Longshot Extra 2": 260329,
    "Split Valley: Longshot Extra 3": 260330,
    "Split Valley: Longshot Extra 4": 260331,
    "Split Valley: Ranged Trinity Extra 1": 260332,
    "Split Valley: Ranged Trinity Extra 2": 260333,
    "Split Valley: Ranged Trinity Extra 3": 260334,
    "Split Valley: Ranged Trinity Extra 4": 260335,
    "Swimming at the Docks: Victory Extra 1": 260336,
    "Swimming at the Docks: Victory Extra 2": 260337,
    "Swimming at the Docks: Victory Extra 3": 260338,
    "Swimming at the Docks: Victory Extra 4": 260339,
    "Swimming at the Docks: Dogs Counter Knights Extra 1": 260340,
    "Swimming at the Docks: Dogs Counter Knights Extra 2": 260341,
    "Swimming at the Docks: Dogs Counter Knights Extra 3": 260342,
    "Swimming at the Docks: Dogs Counter Knights Extra 4": 260343,
    "Swimming at the Docks: Kayaking Extra 1": 260344,
    "Swimming at the Docks: Kayaking Extra 2": 260345,
    "Swimming at the Docks: Kayaking Extra 3": 260346,
    "Swimming at the Docks: Kayaking Extra 4": 260347,
    "Ancient Discoveries: Victory Extra 1": 260348,
    "Ancient Discoveries: Victory Extra 2": 260349,
    "Ancient Discoveries: Victory Extra 3": 260350,
    "Ancient Discoveries: Victory Extra 4": 260351,
    "Ancient Discoveries: So many Choices Extra 1": 260352,
    "Ancient Discoveries: So many Choices Extra 2": 260353,
    "Ancient Discoveries: So many Choices Extra 3": 260354,
    "Ancient Discoveries: So many Choices Extra 4": 260355,
    "Ancient Discoveries: Height Advantage Extra 1": 260356,
    "Ancient Discoveries: Height Advantage Extra 2": 260357,
    "Ancient Discoveries: Height Advantage Extra 3": 260358,
    "Ancient Discoveries: Height Advantage Extra 4": 260359,
    "Observation Isle: Victory Extra 1": 260360,
    "Observation Isle: Victory Extra 2": 260361,
    "Observation Isle: Victory Extra 3": 260362,
    "Observation Isle: Victory Extra 4": 260363,
    "Observation Isle: Become the Watcher Extra 1": 260364,
    "Observation Isle: Become the Watcher Extra 2": 260365,
    "Observation Isle: Become the Watcher Extra 3": 260366,
    "Observation Isle: Become the Watcher Extra 4": 260367,
    "Observation Isle: Execute the Watcher Extra 1": 260368,
    "Observation Isle: Execute the Watcher Extra 2": 260369,
    "Observation Isle: Execute the Watcher Extra 3": 260370,
    "Observation Isle: Execute the Watcher Extra 4": 260371,
    "Majestic Mountain: Victory Extra 1": 260372,
    "Majestic Mountain: Victory Extra 2": 260373,
    "Majestic Mountain: Victory Extra 3": 260374,
    "Majestic Mountain: Victory Extra 4": 260375,
    "Majestic Mountain: Mountain Climbing Extra 1": 260376,
    "Majestic Mountain: Mountain Climbing Extra 2": 260377,
    "Majestic Mountain: Mountain Climbing Extra 3": 260378,
    "Majestic Mountain: Mountain Climbing Extra 4": 260379,
    "Majestic Mountain: Legend of the Mountains Extra 1": 260380,
    "Majestic Mountain: Legend of the Mountains Extra 2": 260381,
    "Majestic Mountain: Legend of the Mountains Extra 3": 260382,
    "Majestic Mountain: Legend of the Mountains Extra 4": 260383,
    "Floran Trap: Victory Extra 1": 260384,
    "Floran Trap: Victory Extra 2": 260385,
    "Floran Trap: Victory Extra 3": 260386,
    "Floran Trap: Victory Extra 4": 260387,
    "Floran Trap: Means of Production Extra 1": 260388,
    "Floran Trap: Means of Production Extra 2": 260389,
    "Floran Trap: Means of Production Extra 3": 260390,
    "Floran Trap: Means of Production Extra 4": 260391,
    "Floran Trap: Aerial Reconnaissance Extra 1": 260392,
    "Floran Trap: Aerial Reconnaissance Extra 2": 260393,
    "Floran Trap: Aerial Reconnaissance Extra 3": 260394,
    "Floran Trap: Aerial Reconnaissance Extra 4": 260395,
    #########################################################
    "Disastrous Crossing: Victory": None,
    "Dark Mirror: Victory": None,
    "Doomed Metropolis: Victory": None,
    "Dementia Castle: Victory": None,
    "Skipped Finale #1: Victory": None,
    "Skipped Finale #2: Victory": None,
    "Skipped Finale #3: Victory": None,
    "Skipped Finale #4: Victory": None,
    "Wargroove 2: Victory": None
}

location_id_name: Dict[int, str] = {}
for name in location_table.keys():
    id = location_table[name]
    if id is not None:
        location_id_name[id] = name


class Wargroove2Location(Location):
    game: str = "Wargroove 2"

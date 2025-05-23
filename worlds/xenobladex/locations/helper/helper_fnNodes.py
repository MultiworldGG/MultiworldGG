import json
import sys

# https://xenoblade.github.io/xbx/bdat/common_local_us/SEG_ProbeList.html
# flake8: noqa
nodes = [
1,
3,
2,
4,
21,
5,
0,
6,
7,
8,
9,
10,
11,
12,
13,
14,
15,
16,
17,
18,
19,
20,
22,
23,
24,
25,
26,
27,
28,
29,
30,
31,
32,
33,
34,
35,
36,
37,
38,
39,
40,
41,
42,
43,
44,
45,
46,
49,
50,
51,
52,
53,
54,
55,
56,
57,
58,
59,
60,
61,
62,
63,
64,
65,
66,
67,
68,
69,
70,
94,
95,
96,
97,
98,
99,
100,
101,
102,
103,
104,
105,
106,
107,
108,
109,
74,
75,
76,
77,
78,
79,
80,
81,
82,
83,
84,
85,
86,
87,
88,
89,
90,
91,
92,
93,
]

veins = [85, #https://xenoblade.github.io/xbx/bdat/common_local_us/FnetVeinList.html
86,
87,
88,
89,
91,
92,
93,
94,
95,
96,
97,
98,
99,
100,
101,
102,
103,
104,
105,
106,
169,
170,
171,
172,
173,
174,
175,
176,
177,
178,
179,
180,
181,
182,
183,
184,
185,
186,
187,
188,
189,
190,
191,
192,
193,
174,
175,
244,
245,
246,
247,
248,
249,
250,
251,
252,
253,
254,
255,
256,
257,
258,
259,
260,
261,
262,
263,
264,
265,
256,
257,
258,
314,
315,
316,
317,
318,
319,
320,
321,
322,
323,
324,
325,
326,
327,
328,
329,
330,
331,
332,
333,
375,
376,
377,
378,
379,
380,
381,
382,
383,
384,
385,
386,
387,
388,
389,
390,
]

# https://xenoblade.github.io/xbx/bdat/common_local_us/FLD_Location.html
names = [
"Barracks Interior",
"Interior",
"West Gate",
"Central Industrial District",
"Integrated Production Plant",
"Outfitters Test Hangar",
"Repenta Diner",
"Professor B's Lab",
"West Melville Street",
"Central Melville Street",
"East Melville Street",
"Barista Court",
"North Founders Street",
"Nopon Bazaar",
"Deck",
"Starboard",
"Port Side",
"Water Purification Plant",
"Deliverance Park",
"Cathedral",
"Sports Complex",
"Ishmael Hills",
"Division Drive",
"Armory Alley",
"Yardley's Hideaway",
"East Gate",
"BLADE Tower",
"BLADE Concourse",
"BLADE Barracks",
"Mimeosome Maintenance Center",
"Hangar",
"Restricted Hangar Entrance",
"Bedrock Hold",
"Stonelattice Cavern",
"Greater Gemini Bridge",
"Castaway Cavern",
"Stickstone Rise",
"Lesser Gemini Bridge",
"Plundered Ruin",
"Unicorn Rock",
"Turtle Nest",
"Molten Hollow",
"Bedrock Hold Approach",
"Biahno River",
"Green Threshold",
"Headwater Cavern",
"Headwater Summit",
"Headwater Cliff",
"Biahno Water-Purification Plant",
"Biahno Lake",
"Fallshorn Isle",
"Grieving Plains",
"Biahno Grassland",
"Drop Shaft",
"Silent Mire",
"Seaswept Base",
"Wonderment Bluff",
"Sickle Rock Rise",
"Roof Rock",
"Janpath Lake",
"La Mancha",
"North Janpath Plain",
"Arendt Bridge",
"Tallpach Peak",
"Beasts' Lair",
"Northpointe Cove",
"Northpointe Beach",
"East Janpath Plain",
"South Janpath Plain",
"West Janpath Plain",
"Cliffside Beach",
"East Gate Plain",
"West Gate Plain",
"Talon Rock Prominence",
"Talon Rock Third Terrane",
"Talon Rock Second Terrane",
"Sayram Northeast Plain",
"Shadow Rise",
"Biahno Hills",
"Starfall Basin",
"Rock Cavern",
"Seaswept Rise",
"Sayram Lake",
"Talon Rock Summit",
"FN Site 101",
"FN Site 102",
"FN Site 103",
"FN Site 104",
"FN Site 106",
"Seaswept Ridge",
"FN Site 108",
"FN Site 107",
"FN Site 109",
"FN Site 110",
"FN Site 111",
"FN Site 112",
"FN Site 113",
"FN Site 114",
"FN Site 115",
"FN Site 116",
"FN Site 117",
"FN Site 118",
"FN Site 119",
"FN Site 120",
"FN Site 121",
"FN Site 105",
"Rustpool Banks",
"Potter's Rock",
"Whale's Gullet",
"Rust Lake",
"Waterway Tangle",
"Ensanguined Font",
"Lakeview Stronghold",
"Jasper Incline",
"Old Dragontail Tree",
"Redsnake Pass",
"Whale's Nostril",
"Yagami's Vista",
"Sapphire Carpet",
"Sapphire Table",
"Garden Spring",
"Tripod Rock",
"Humdrum Peaks",
"Goblin's Narrow",
"Sunlit Spring",
"Orochi's Belly",
"Elephant's Trunk",
"Seabound Coil Tree",
"Nopon Highroad",
"Coil Tree Cape",
"Decapotamon Vista",
"Decapotamon",
"Cascade Isle",
"Serpentine Pass",
"Vitriol Cesspool",
"Qing Long Glade",
"Rockmole's Burrow",
"Fukai Pass",
"Everwhelm Falls",
"Sato Headwater",
"Weeping Whitewood",
"Ensconced Citadel",
"Suncatch Ravine",
"Middle Hushflood",
"Great Trident Crossing",
"Bloodpond Basin",
"Millstone Ridge",
"Dead Man's Gulch",
"Shark's Jaws",
"Dead Man's Ingress",
"Upper Hushflood",
"Divine Roost",
"Whale's Weeper",
"Nopon Braidbridge",
"Skybound Coil Tree",
"Great Nail",
"Bident Crossing",
"Blackback Bridge",
"Narcissus Tree",
"Celestial Ascent",
"Celestial Cleave",
"Sentinel's Nest",
"Canopied Nightwood",
"Lotus Keep Building Site",
"Twin Hammers",
"Breakwater Narrow",
"Skygazer's Atrium",
"Idyll Beach",
"FN Site 201",
"FN Site 202",
"FN Site 203",
"FN Site 204",
"FN Site 205",
"FN Site 206",
"FN Site 207",
"FN Site 208",
"FN Site 209",
"FN Site 210",
"FN Site 211",
"FN Site 212",
"FN Site 213",
"FN Site 214",
"FN Site 215",
"FN Site 216",
"FN Site 217",
"FN Site 218",
"FN Site 219",
"FN Site 220",
"FN Site 221",
"FN Site 222",
"FN Site 223",
"FN Site 224",
"FN Site 225",
"Oblivia Ingress",
"Yawning Giant",
"Mesa Fortress",
"Demon's Pocket",
"Scabland Fortress",
"River Isle",
"Rooney Cavern",
"Atop the Giant Ring",
"Ejiri Promontory",
"Leaning Ring",
"Drowning Ring",
"Beachside Trove",
"Azure Lagoon",
"Balance Rock",
"South Coast",
"Barbarich Desert",
"Primeval Meadow",
"Cryptic Sign",
"Jair Fortress",
"Sea Whisper Valley",
"West Ibra Ravine",
"Central Ibra Ravine",
"East Ibra Ravine",
"Victory Rock",
"Alexander Ridge",
"Wrothian Stronghold",
"Dorian Caravan",
"Lake Basel",
"Floating Reef",
"Ruins on the Sandbank",
"King's Falls",
"Milligan Supply Base",
"North Coast",
"Big Arch",
"Ruins on the Butte",
"Kintrees",
"Aaroy Plain",
"Twin Arches",
"Devil's Colony",
"Great Washington Isle",
"Cliffside Camp",
"Crater Oasis",
"North Ant's Nest",
"Ant's Nest",
"South Ant's Nest",
"Keegan Ridge",
"Stoyanov Trail",
"Mount Edge Peak",
"Beehive Rock",
"Eddie's Conquest",
"FN Site 301",
"FN Site 302",
"FN Site 303",
"FN Site 304",
"FN Site 305",
"FN Site 306",
"FN Site 307",
"FN Site 308",
"FN Site 309",
"FN Site 310",
"FN Site 311",
"FN Site 312",
"FN Site 313",
"FN Site 314",
"FN Site 315",
"FN Site 316",
"FN Site 317",
"FN Site 318",
"FN Site 320",
"FN Site 321",
"FN Site 319",
"FN Site 322",
"Seabird's Beak",
"Needle Rock Sandsea",
"South Silent Sandsea",
"North Silent Sandsea",
"Lake Ciel",
"South Ciel Sandsea",
"West Ciel Sandsea",
"East Ciel Sandsea",
"North Ciel Sandsea",
"Shivering Sands",
"Xanadu Overlook",
"Cleansing Spring",
"Badr Stonebridge",
"Anvil Rock Two",
"Anvil Rock One",
"Anvil Sandplain",
"South Hardheart Canyon",
"Hardheart Canyon",
"North Hardheart Canyon",
"Southern Searoad",
"Sylvalum Searoad",
"Northern Searoad",
"Delusians North Summit",
"Gehenna Span",
"Delusians South Summit",
"South Cinderdunes",
"West Cinderdunes",
"North Cinderdunes",
"Samuel Incline",
"Cauldros Threshold",
"Hilal Meadow",
"Hilal Stronghold",
"Badr Basin",
"Badr Stronghold",
"Secluded Lava Lake",
"Cavernous Abyss",
"Banshee Cave",
"Quay Hollows",
"Den of the Dead",
"Behemoth's Shadows",
"Sandsprint Slope",
"Lesser Anvil",
"Arc Rock",
"Abyss Reservoir",
"Noctilucent Sphere",
"Lower Delusian Mountains",
"Sandsprint Cavity",
"Noctilucent Sphere Interior",
"FN Site 401",
"FN Site 402",
"FN Site 403",
"FN Site 404",
"FN Site 405",
"FN Site 406",
"FN Site 407",
"FN Site 408",
"FN Site 409",
"FN Site 410",
"FN Site 411",
"FN Site 412",
"FN Site 413",
"FN Site 414",
"FN Site 415",
"FN Site 416",
"FN Site 417",
"FN Site 418",
"FN Site 419",
"FN Site 420",
"Drongo Caravan",
"Scholes Battlegrounds",
"Infernal Ledges",
"Ancient Warscape",
"Wildcat Fortress",
"White Phosphor Lake",
"O'rrh Sim Gate",
"Ganglion Antropolis",
"Ruined City of O'rrh Sim",
"G'nahan Villa",
"Emerian Battlegrounds",
"Forgotten Mining Frigates",
"Adder Byroad",
"Bandits' Refuge",
"Slavebird Isle",
"Ganglion Weapons Hangar",
"O'rrh Sim Castle Ruins",
"Tengu's Playground",
"T'phnom Shelf",
"Kitsune Stronghold",
"Sunset Falls",
"Kw'arah Villa",
"Kw'arah Cloister",
"Boxtrap Checkpoint",
"M'gando Mineral Spring",
"Bestial Utopia",
"M'gando Volcanic Crater",
"Mount M'gando",
"Old Ceremonial Hollow",
"Old Ceremonial Hollow",
"Beneath O'rrh Sim Keep",
"Dragonbone Promontory",
"Ternion Fork",
"Abandoned Bivouac",
"M'gando Gorge",
"Titan's Table",
"Cauldros Gate",
"Capital Wreckage",
"O'rrh Sim Capital Remains",
"O'rrh Sim Watchtowers",
"Far Isle of Tzu'o",
"FN Site 501",
"FN Site 502",
"FN Site 503",
"FN Site 504",
"FN Site 505",
"FN Site 506",
"FN Site 507",
"FN Site 508",
"FN Site 509",
"FN Site 510",
"FN Site 511",
"FN Site 512",
"FN Site 513",
"FN Site 514",
"FN Site 515",
"FN Site 516",
"Shadow Rise BC",
"Shadow Beach BC",
"East Gate BC",
"South Janpath BC",
"Biahno Grassland BC",
"North Janpath BC",
"Sayram Lake BC",
"Roof Rock BC",
"camp1501_09",
"camp1501_10",
"Rustpool Banks BC",
"Whale's Nostril BC",
"Tripod Rock BC",
"Canopied Nightwood BC",
"Decapotamon BC",
"Qing Long Glade BC",
"Bloodpond Basin BC",
"Dead Man's Ingress BC",
"camp1601_09",
"camp1601_10",
"Oblivia Ingress BC",
"Aaroy Plain BC",
"Needle Bridge BC",
"Broken Hill BC",
"River Isle BC",
"Balance Rock BC",
"North Coast BC",
"Cliff's Edge BC",
"camp1701_09",
"camp1701_10",
"Ancient Warscape BC",
"Titan's Table BC",
"Emerian Battlegrounds BC",
"Rocky Lagoon BC",
"Adder Byroad BC",
"Ternion Fork BC",
"T'phnom Shelf BC",
"M'gando Gorge BC",
"camp2001_09",
"camp2001_10",
"Seabird's Beak BC",
"Needle Rock BC",
"NW Ciel Sandsea BC",
"Hardheart Ravine BC",
"Delusians North Summit BC",
"Samuel Incline BC",
"North Silent Sandsea BC",
"Cauldros Threshold BC",
"camp2201_09",
"camp2201_10",
"NLA Last Defense Line",
"NLA Primary Defense Line",
"Zu Pharg Interception Line",
"Lifehold Core",
"O'rrh Sim Keep",
]

with open('helper_fnNodes.txt', 'w') as f:
	sys.stdout = f
	for ids in veins:
		print(f"{json.dumps(names[ids - 1])},")
import random

girllist = (
    "tiffany",
    "aiko",
    "kyanna",
    "audrey",
    "lola",
    "nikki",
    "jessie",
    "beli",
    "kyu",
    "momo",
    "celeste",
    "venus",
)

defaultgirlgifts = {
    "tiffany": [
        49,#"Decorative Pens",
        50,#"Glossy Notebook",
        51,#"Graduation Cap",
        52,#"Textbooks",
        53,#"Girly Backpack",
        54,#"Laptop Pro",
        67,#"Baby Binky",
        68,#"Bead Bracelet",
        69,#"Glow Sticks",
        70,#"Rainbow Wig",
        71,#"Fuzzy Boots",
        72,#"Fairy Wings",
        109,#"Swimmers Cap",
        110,#"Goggles",
        111,#"Snorkel",
        112,#"Flippers",
        113,#"Lifesaver",
        114,#"Diving Tank",
        193,#"Double Hair Bow",
        194,#"Glitter Bottles",
        195,#"Twirly Baton",
        196,#"Megaphone",
        197,#"Pom-poms",
        198,#"Cheerleading Uniform",
    ],
    "aiko": [
        55,#"Old Fashioned Yoyo",
        56,#"Puzzle Cube",
        57,#"Sudoku Books",
        58,#"Dart Board",
        59,#"Board Game",
        60,#"Chess Set",
        79,#"Sketching Pencils",
        80,#"Paint Brushes",
        81,#"Drawing Mannequin",
        82,#"Sketch Pad",
        83,#"Paint Palette",
        84,#"Canvas & Easel",
        115,#"Flower Seeds",
        116,#"Garden Shovel",
        117,#"Flower Pots",
        118,#"Watering Can",
        119,#"Garden Gnome",
        120,#"Wooden Birdhouse",
        199,#"Chopsticks",
        200,#"Riceballs",
        201,#"Bonsai Tree",
        202,#"Wooden Sandals",
        203,#"Kimono",
        204,#"Samurai Helmet",
    ],
    "kyanna": [
        61,#"Water Bottle",
        62,#"Cardio Weights",
        63,#"Skipping Rope",
        64,#"Kettle Bell",
        65,#"Boxing Gloves",
        66,#"Punching Bag",
        91,#"Yoga Belt",
        92,#"Yoga Blocks",
        93,#"Yoga Bag",
        94,#"Yoga Mat",
        95,#"Yoga Ball",
        96,#"Yoga Outfit",
        97,#"Tango Rose",
        98,#"Sweatbands",
        99,#"Leg Warmers",
        100,#"Dancing Fan",
        101,#"Pink Tutu",
        102,#"Stripper Pole",
        205,#"Maracas",
        206,#"Sombrero",
        207,#"Poncho",
        208,#"Luchador Mask",
        209,#"Pinata",
        210,#"Vinuela",
    ],
    "audrey": [
        67,#"Baby Binky",
        68,#"Bead Bracelet",
        69,#"Glow Sticks",
        70,#"Rainbow Wig",
        71,#"Fuzzy Boots",
        72,#"Fairy Wings",
        55,#"Old Fashioned Yoyo",
        56,#"Puzzle Cube",
        57,#"Sudoku Books",
        58,#"Dart Board",
        59,#"Board Game",
        60,#"Chess Set",
        103,#"Synthetic Seaweed",
        104,#"Synthetic Coral",
        105,#"Tank Gravel",
        106,#"Bag of Goldfish",
        107,#"Fishy Castle",
        108,#"Fish Tank",
        211,#"Cigarette Pack",
        212,#"Lighter",
        213,#"Glass Pipe",
        214,#"Glass Bong",
        215,#"Blotter Tabs",
        216,#"Happy Pills",
    ],
    "lola": [
        73,#"Tennis Balls",
        74,#"Tennis Racket",
        75,#"Flying Disc",
        76,#"Basket Ball",
        77,#"Volley Ball",
        78,#"Soccer Ball",
        85,#"Baking Utensils",
        86,#"Measuring Cup",
        87,#"Rolling Pin",
        88,#"Oven Timer",
        89,#"Mixing Bowl",
        90,#"Oven Mitts",
        109,#"Swimmers Cap",
        110,#"Goggles",
        111,#"Snorkel",
        112,#"Flippers",
        113,#"Lifesaver",
        114,#"Diving Tank",
        217,#"Wing Pin",
        218,#"Compass",
        219,#"Pilot's Cap",
        220,#"Travel Suitcase",
        221,#"Rolling Luggage",
        222,#"High Def Camera",
    ],
    "nikki": [
        79,#"Sketching Pencils",
        80,#"Paint Brushes",
        81,#"Drawing Mannequin",
        82,#"Sketch Pad",
        83,#"Paint Palette",
        84,#"Canvas & Easel",
        49,#"Decorative Pens",
        50,#"Glossy Notebook",
        51,#"Graduation Cap",
        52,#"Textbooks",
        53,#"Girly Backpack",
        54,#"Laptop Pro",
        103,#"Synthetic Seaweed",
        104,#"Synthetic Coral",
        105,#"Tank Gravel",
        106,#"Bag of Goldfish",
        107,#"Fishy Castle",
        108,#"Fish Tank",
        223,#"Retro Controller",
        224,#"Arcade Joystick",
        225,#"Zappy Gun",
        226,#"Gamer Glove",
        227,#"Handheld Game",
        228,#"Arcade Cabinet",
    ],
    "jessie": [
        85,#"Baking Utensils",
        86,#"Measuring Cup",
        87,#"Rolling Pin",
        88,#"Oven Timer",
        89,#"Mixing Bowl",
        90,#"Oven Mitts",
        61,#"Water Bottle",
        62,#"Cardio Weights",
        63,#"Skipping Rope",
        64,#"Kettle Bell",
        65,#"Boxing Gloves",
        66,#"Punching Bag",
        97,#"Tango Rose",
        98,#"Sweatbands",
        99,#"Leg Warmers",
        100,#"Dancing Fan",
        101,#"Pink Tutu",
        102,#"Stripper Pole",
        229,#"Mistletoe",
        230,#"Gingerbread Man",
        231,#"Round Ornament",
        232,#"Ribbon Wreath",
        233,#"Fuzzy Stocking",
        234,#"Jolly Old Cap",
    ],
    "beli": [
        91,#"Yoga Belt",
        92,#"Yoga Blocks",
        93,#"Yoga Bag",
        94,#"Yoga Mat",
        95,#"Yoga Ball",
        96,#"Yoga Outfit",
        73,#"Tennis Balls",
        74,#"Tennis Racket",
        75,#"Flying Disc",
        76,#"Basket Ball",
        77,#"Volley Ball",
        78,#"Soccer Ball",
        115,#"Flower Seeds",
        116,#"Garden Shovel",
        117,#"Flower Pots",
        118,#"Watering Can",
        119,#"Garden Gnome",
        120,#"Wooden Birdhouse",
        235,#"Acorns",
        236,#"Maple Leaf",
        237,#"Pinecone",
        238,#"Mushrooms",
        239,#"Seashell",
        240,#"Four Leaf Clover",
    ],
    "kyu": [
        97,#"Tango Rose",
        98,#"Sweatbands",
        99,#"Leg Warmers",
        100,#"Dancing Fan",
        101,#"Pink Tutu",
        102,#"Stripper Pole",
        67,#"Baby Binky",
        68,#"Bead Bracelet",
        69,#"Glow Sticks",
        70,#"Rainbow Wig",
        71,#"Fuzzy Boots",
        72,#"Fairy Wings",
        79,#"Sketching Pencils",
        80,#"Paint Brushes",
        81,#"Drawing Mannequin",
        82,#"Sketch Pad",
        83,#"Paint Palette",
        84,#"Canvas & Easel",
        241,#"Endurance Ring",
        242,#"Pocket Vibe",
        243,#"Fairy's Tail",
        244,#"Bliss Beads",
        245,#"Magic Wand",
        246,#"Royal Scepter",
    ],
    "momo": [
        103,#"Synthetic Seaweed",
        104,#"Synthetic Coral",
        105,#"Tank Gravel",
        106,#"Bag of Goldfish",
        107,#"Fishy Castle",
        108,#"Fish Tank",
        55,#"Old Fashioned Yoyo",
        56,#"Puzzle Cube",
        57,#"Sudoku Books",
        58,#"Dart Board",
        59,#"Board Game",
        60,#"Chess Set",
        73,#"Tennis Balls",
        74,#"Tennis Racket",
        75,#"Flying Disc",
        76,#"Basket Ball",
        77,#"Volley Ball",
        78,#"Soccer Ball",
        247,#"Ball of Yarn",
        248,#"Lattice Ball",
        249,#"Squeaky Mouse",
        250,#"Feather Pole",
        251,#"Laser Pointer",
        252,#"Scratch Post",
    ],
    "celeste": [
        109,#"Swimmers Cap",
        110,#"Goggles",
        111,#"Snorkel",
        112,#"Flippers",
        113,#"Lifesaver",
        114,#"Diving Tank",
        49,#"Decorative Pens",
        50,#"Glossy Notebook",
        51,#"Graduation Cap",
        52,#"Textbooks",
        53,#"Girly Backpack",
        54,#"Laptop Pro",
        61,#"Water Bottle",
        62,#"Cardio Weights",
        63,#"Skipping Rope",
        64,#"Kettle Bell",
        65,#"Boxing Gloves",
        66,#"Punching Bag",
        253,#"Model Rocket",
        254,#"Miniature UFO",
        255,#"Armillary Sphere",
        256,#"Telescope",
        257,#"Space Helmet",
        258,#"Moonrock",
    ],
    "venus": [
        115,#"Flower Seeds",
        116,#"Garden Shovel",
        117,#"Flower Pots",
        118,#"Watering Can",
        119,#"Garden Gnome",
        120,#"Wooden Birdhouse",
        85,#"Baking Utensils",
        86,#"Measuring Cup",
        87,#"Rolling Pin",
        88,#"Oven Timer",
        89,#"Mixing Bowl",
        90,#"Oven Mitts",
        91,#"Yoga Belt",
        92,#"Yoga Blocks",
        93,#"Yoga Bag",
        94,#"Yoga Mat",
        95,#"Yoga Ball",
        96,#"Yoga Outfit",
        259,#"Sapphire",
        260,#"Ruby",
        261,#"Emerald",
        262,#"Topaz",
        263,#"Amethyst",
        264,#"Diamond",
    ],
}

defaultgirltraits = {
    "tiffany": [1,3],
    "aiko": [3,0],
    "kyanna": [0,2],
    "audrey": [1,2],
    "lola": [2,0],
    "nikki": [0,3],
    "jessie": [3,2],
    "beli": [2,1],
    "kyu": [1,0],
    "momo": [2,3],
    "celeste": [0,1],
    "venus": [3,1],
}

gift_id_to_name = {
49:"Decorative Pens",
50:"Glossy Notebook",
51:"Graduation Cap",
52:"Textbooks",
53:"Girly Backpack",
54:"Laptop Pro",
55:"Old Fashioned Yoyo",
56:"Puzzle Cube",
57:"Sudoku Books",
58:"Dart Board",
59:"Board Game",
60:"Chess Set",
61:"Water Bottle",
62:"Cardio Weights",
63:"Skipping Rope",
64:"Kettle Bell",
65:"Boxing Gloves",
66:"Punching Bag",
67:"Baby Binky",
68:"Bead Bracelet",
69:"Glow Sticks",
70:"Rainbow Wig",
71:"Fuzzy Boots",
72:"Fairy Wings",
73:"Tennis Balls",
74:"Tennis Racket",
75:"Flying Disc",
76:"Basket Ball",
77:"Volley Ball",
78:"Soccer Ball",
79:"Sketching Pencils",
80:"Paint Brushes",
81:"Drawing Mannequin",
82:"Sketch Pad",
83:"Paint Palette",
84:"Canvas & Easel",
85:"Baking Utensils",
86:"Measuring Cup",
87:"Rolling Pin",
88:"Oven Timer",
89:"Mixing Bowl",
90:"Oven Mitts",
91:"Yoga Belt",
92:"Yoga Blocks",
93:"Yoga Bag",
94:"Yoga Mat",
95:"Yoga Ball",
96:"Yoga Outfit",
97:"Tango Rose",
98:"Sweatbands",
99:"Leg Warmers",
100:"Dancing Fan",
101:"Pink Tutu",
102:"Stripper Pole",
103:"Synthetic Seaweed",
104:"Synthetic Coral",
105:"Tank Gravel",
106:"Bag of Goldfish",
107:"Fishy Castle",
108:"Fish Tank",
109:"Swimmers Cap",
110:"Goggles",
111:"Snorkel",
112:"Flippers",
113:"Lifesaver",
114:"Diving Tank",
115:"Flower Seeds",
116:"Garden Shovel",
117:"Flower Pots",
118:"Watering Can",
119:"Garden Gnome",
120:"Wooden Birdhouse",
193:"Double Hair Bow",
194:"Glitter Bottles",
195:"Twirly Baton",
196:"Megaphone",
197:"Pom-poms",
198:"Cheerleading Uniform",
199:"Chopsticks",
200:"Riceballs",
201:"Bonsai Tree",
202:"Wooden Sandals",
203:"Kimono",
204:"Samurai Helmet",
205:"Maracas",
206:"Sombrero",
207:"Poncho",
208:"Luchador Mask",
209:"Pinata",
210:"Vinuela",
211:"Cigarette Pack",
212:"Lighter",
213:"Glass Pipe",
214:"Glass Bong",
215:"Blotter Tabs",
216:"Happy Pills",
217:"Wing Pin",
218:"Compass",
219:"Pilot's Cap",
220:"Travel Suitcase",
221:"Rolling Luggage",
222:"High Def Camera",
223:"Retro Controller",
224:"Arcade Joystick",
225:"Zappy Gun",
226:"Gamer Glove",
227:"Handheld Game",
228:"Arcade Cabinet",
229:"Mistletoe",
230:"Gingerbread Man",
231:"Round Ornament",
232:"Ribbon Wreath",
233:"Fuzzy Stocking",
234:"Jolly Old Cap",
235:"Acorns",
236:"Maple Leaf",
237:"Pinecone",
238:"Mushrooms",
239:"Seashell",
240:"Four Leaf Clover",
241:"Endurance Ring",
242:"Pocket Vibe",
243:"Fairy's Tail",
244:"Bliss Beads",
245:"Magic Wand",
246:"Royal Scepter",
247:"Ball of Yarn",
248:"Lattice Ball",
249:"Squeaky Mouse",
250:"Feather Pole",
251:"Laser Pointer",
252:"Scratch Post",
253:"Model Rocket",
254:"Miniature UFO",
255:"Armillary Sphere",
256:"Telescope",
257:"Space Helmet",
258:"Moonrock",
259:"Sapphire",
260:"Ruby",
261:"Emerald",
262:"Topaz",
263:"Amethyst",
264:"Diamond",
}

gift_ids = [
    49,#//academy gift 1 | Decorative Pens
    50,#//academy gift 2 | Glossy Notebook
    51,#//academy gift 3 | Graduation Cap
    52,#//academy gift 4 | Textbooks
    53,#//academy gift 5 | Girly Backpack
    54,#//academy gift 6 | Laptop Pro
    55,#//toys gift 1 | Old Fashioned Yoyo
    56,#//toys gift 2 | Puzzle Cube
    57,#//toys gift 3 | Sudoku Books
    58,#//toys gift 4 | Dart Board
    59,#//toys gift 5 | Board Game
    60,#//toys gift 6 | Chess Set
    61,#//fitness gift 1 | Water Bottle
    62,#//fitness gift 2 | Cardio Weights
    63,#//fitness gift 3 | Skipping Rope
    64,#//fitness gift 4 | Kettle Bell
    65,#//fitness gift 5 | Boxing Gloves
    66,#//fitness gift 6 | Punching Bag
    67,#//rave gift 1 | Baby Binky
    68,#//rave gift 2 | Bead Bracelet
    69,#//rave gift 3 | Glow Sticks
    70,#//rave gift 4 | Rainbow Wig
    71,#//rave gift 5 | Fuzzy Boots
    72,#//rave gift 6 | Fairy Wings
    73,#//sports gift 1 | Tennis Balls
    74,#//sports gift 2 | Tennis Racket
    75,#//sports gift 3 | Flying Disc
    76,#//sports gift 4 | Basket Ball
    77,#//sports gift 5 | Volley Ball
    78,#//sports gift 6 | Soccer Ball
    79,#//artist gift 1 | Sketching Pencils
    80,#//artist gift 2 | Paint Brushes
    81,#//artist gift 3 | Drawing Mannequin
    82,#//artist gift 4 | Sketch Pad
    83,#//artist gift 5 | Paint Palette
    84,#//artist gift 6 | Canvas & Easel
    85,#//baking gift 1 | Baking Utensils
    86,#//baking gift 2 | Measuring Cup
    87,#//baking gift 3 | Rolling Pin
    88,#//baking gift 4 | Oven Timer
    89,#//baking gift 5 | Mixing Bowl
    90,#//baking gift 6 | Oven Mitts
    91,#//yoga gift 1 | Yoga Belt
    92,#//yoga gift 2 | Yoga Blocks
    93,#//yoga gift 3 | Yoga Bag
    94,#//yoga gift 4 | Yoga Mat
    95,#//yoga gift 5 | Yoga Ball
    96,#//yoga gift 6 | Yoga Outfit
    97,#//dancer gift 1 | Tango Rose
    98,#//dancer gift 2 | Sweatbands
    99,#//dancer gift 3 | Leg Warmers
    100,#//dancer gift 4 | Dancing Fan
    101,#//dancer gift 5 | Pink Tutu
    102,#//dancer gift 6 | Stripper Pole
    103,#//aquarium gift 1 | Synthetic Seaweed
    104,#//aquarium gift 2 | Synthetic Coral
    105,#//aquarium gift 3 | Tank Gravel
    106,#//aquarium gift 4 | Bag of Goldfish
    107,#//aquarium gift 5 | Fishy Castle
    108,#//aquarium gift 6 | Fish Tank
    109,#//scuba gift 1 | Swimmers Cap
    110,#//scuba gift 2 | Goggles
    111,#//scuba gift 3 | Snorkel
    112,#//scuba gift 4 | Flippers
    113,#//scuba gift 5 | Lifesaver
    114,#//scuba gift 6 | Diving Tank
    115,#//garden gift 1 | Flower Seeds
    116,#//garden gift 2 | Garden Shovel
    117,#//garden gift 3 | Flower Pots
    118,#//garden gift 4 | Watering Can
    119,#//garden gift 5 | Garden Gnome
    120,#//garden gift 6 | Wooden Birdhouse
    193,#//tiffany gift 1 | Double Hair Bow
    194,#//tiffany gift 2 | Glitter Bottles
    195,#//tiffany gift 3 | Twirly Baton
    196,#//tiffany gift 4 | Megaphone
    197,#//tiffany gift 5 | Pom-poms
    198,#//tiffany gift 6 | Cheerleading Uniform
    199,#//aiko gift 1 | Chopsticks
    200,#//aiko gift 2 | Riceballs
    201,#//aiko gift 3 | Bonsai Tree
    202,#//aiko gift 4 | Wooden Sandals
    203,#//aiko gift 5 | Kimono
    204,#//aiko gift 6 | Samurai Helmet
    205,#//kyanna gift 1 | Maracas
    206,#//kyanna gift 2 | Sombrero
    207,#//kyanna gift 3 | Poncho
    208,#//kyanna gift 4 | Luchador Mask
    209,#//kyanna gift 5 | Pinata
    210,#//kyanna gift 6 | Vinuela
    211,#//audrey gift 1 | Cigarette Pack
    212,#//audrey gift 2 | Lighter
    213,#//audrey gift 3 | Glass Pipe
    214,#//audrey gift 4 | Glass Bong
    215,#//audrey gift 5 | Blotter Tabs
    216,#//audrey gift 6 | Happy Pills
    217,#//lola gift 1 | Wing Pin
    218,#//lola gift 2 | Compass
    219,#//lola gift 3 | Pilot's Cap
    220,#//lola gift 4 | Travel Suitcase
    221,#//lola gift 5 | Rolling Luggage
    222,#//lola gift 6 | High Def Camera
    223,#//nikki gift 1 | Retro Controller
    224,#//nikki gift 2 | Arcade Joystick
    225,#//nikki gift 3 | Zappy Gun
    226,#//nikki gift 4 | Gamer Glove
    227,#//nikki gift 5 | Handheld Game
    228,#//nikki gift 6 | Arcade Cabinet
    229,#//jessie gift 1 | Mistletoe
    230,#//jessie gift 2 | Gingerbread Man
    231,#//jessie gift 3 | Round Ornament
    232,#//jessie gift 4 | Ribbon Wreath
    233,#//jessie gift 5 | Fuzzy Stocking
    234,#//jessie gift 6 | Jolly Old Cap
    235,#//beli gift 1 | Acorns
    236,#//beli gift 2 | Maple Leaf
    237,#//beli gift 3 | Pinecone
    238,#//beli gift 4 | Mushrooms
    239,#//beli gift 5 | Seashell
    240,#//beli gift 6 | Four Leaf Clover
    241,#//kyu gift 1 | Endurance Ring
    242,#//kyu gift 2 | Pocket Vibe
    243,#//kyu gift 3 | Fairy's Tail
    244,#//kyu gift 4 | Bliss Beads
    245,#//kyu gift 5 | Magic Wand
    246,#//kyu gift 6 | Royal Scepter
    247,#//momo gift 1 | Ball of Yarn
    248,#//momo gift 2 | Lattice Ball
    249,#//momo gift 3 | Squeaky Mouse
    250,#//momo gift 4 | Feather Pole
    251,#//momo gift 5 | Laser Pointer
    252,#//momo gift 6 | Scratch Post
    253,#//celeste gift 1 | Model Rocket
    254,#//celeste gift 2 | Miniature UFO
    255,#//celeste gift 3 | Armillary Sphere
    256,#//celeste gift 4 | Telescope
    257,#//celeste gift 5 | Space Helmet
    258,#//celeste gift 6 | Moonrock
    259,#//venus gift 1 | Sapphire
    260,#//venus gift 2 | Ruby
    261,#//venus gift 3 | Emerald
    262,#//venus gift 4 | Topaz
    263,#//venus gift 5 | Amethyst
    264,#//venus gift 6 | Diamond
]

date_gifts_ids = [
1,#Coffee
2,#Orange Juice
3,#Bagel
4,#Muffin
5,#Omelette
6,#Pancakes
7,#Cookies
8,#Cupcakes
9,#Sundae
10,#Pumpkin Pie
11,#Fruit Tart Pie
12,#Wedding Cake
13,#Orange
14,#Lemon
15,#Mango
16,#Pinapple
17,#Coconut
18,#Watermelon
19,#Carrot
20,#Cucumber
21,#Tomatos
22,#Bell Peppers
23,#Eggplant
24,#Cabbage
25,#Heart Candies
26,#Jelly Beans
27,#Bubble Gum
28,#Lollipop
29,#Cotton Candy
30,#Chocolate
31,#Soda
32,#Popcorn
33,#French Fries
34,#Corndog
35,#Hamburger
36,#Pizza
37,#Beer
38,#Sake
39,#Wine
40,#Champagne
41,#Pina Colada
42,#Daiquiri
43,#Mojito
44,#Lime Margarita
45,#Martini
46,#Cocktail
47,#Lemon Drop
48,#Whisky
121,#Hoop Earrings
122,#Gold Earrings
123,#Heart Necklace
124,#Pearl Necklace
125,#Silver Ring
126,#Lovely Ring
127,#Nail Polish
128,#Shiny Lipstick
129,#Hair Brush
130,#Makeup Kit
131,#Eyelash Curler
132,#Compact Mirror
133,#Peep Toe Heels
134,#Cork Wedge Sandals
135,#Vintage Platforms
136,#Leopard Print Pumps
137,#Pink Mary Janes
138,#Suede Ankle Booties
139,#Blue Orchid
140,#White Pansy
141,#Orange Cosmos
142,#Red Tulip
143,#Pink Lily
144,#Sunflower
145,#Stuffed Bear
146,#Stuffed Cat
147,#Stuffed Sheep
148,#Stuffed Monkey
149,#Stuffed Penguin
150,#Stuffed Whale
151,#Sea Breeze Perfume
152,#Green Tea Perfume
153,#Peach Perfume
154,#Cinnamon Perfume
155,#Rose Perfume
156,#Lilac Perfume
]



#traits = ["Talent","Flirtation","Romance","Sexuality"]
traits = [
    0,#"Talent",
    1,#"Flirtation",
    2,#"Romance",
    3,#"Sexuality"
]

def rand_girl_data(options, random):
    outdict = {}
    giftlist = [*gift_ids]
    usedgifts = []
    for girl in girllist:
        outdict[girl] = {}

        if options.randomize_girl_gifts.value!=0:
            t = random.sample(giftlist,24)
            outdict[girl]["gift1"] = t[0]
            outdict[girl]["gift2"] = t[1]
            outdict[girl]["gift3"] = t[2]
            outdict[girl]["gift4"] = t[3]
            outdict[girl]["gift5"] = t[4]
            outdict[girl]["gift6"] = t[5]
            outdict[girl]["gift7"] = t[6]
            outdict[girl]["gift8"] = t[7]
            outdict[girl]["gift9"] = t[8]
            outdict[girl]["gift10"] = t[9]
            outdict[girl]["gift11"] = t[10]
            outdict[girl]["gift12"] = t[11]
            outdict[girl]["gift13"] = t[12]
            outdict[girl]["gift14"] = t[13]
            outdict[girl]["gift15"] = t[14]
            outdict[girl]["gift16"] = t[15]
            outdict[girl]["gift17"] = t[16]
            outdict[girl]["gift18"] = t[17]
            outdict[girl]["gift19"] = t[18]
            outdict[girl]["gift20"] = t[19]
            outdict[girl]["gift21"] = t[20]
            outdict[girl]["gift22"] = t[21]
            outdict[girl]["gift23"] = t[22]
            outdict[girl]["gift24"] = t[23]
            if options.randomize_girl_gifts.value==1:
                for i in t:
                    giftlist.remove(i)
                if len(giftlist)==0:
                    giftlist = [*gift_ids]
        else:
            outdict[girl]["gift1"] = defaultgirlgifts[girl][0]
            outdict[girl]["gift2"] = defaultgirlgifts[girl][1]
            outdict[girl]["gift3"] = defaultgirlgifts[girl][2]
            outdict[girl]["gift4"] = defaultgirlgifts[girl][3]
            outdict[girl]["gift5"] = defaultgirlgifts[girl][4]
            outdict[girl]["gift6"] = defaultgirlgifts[girl][5]
            outdict[girl]["gift7"] = defaultgirlgifts[girl][6]
            outdict[girl]["gift8"] = defaultgirlgifts[girl][7]
            outdict[girl]["gift9"] = defaultgirlgifts[girl][8]
            outdict[girl]["gift10"] = defaultgirlgifts[girl][9]
            outdict[girl]["gift11"] = defaultgirlgifts[girl][10]
            outdict[girl]["gift12"] = defaultgirlgifts[girl][11]
            outdict[girl]["gift13"] = defaultgirlgifts[girl][12]
            outdict[girl]["gift14"] = defaultgirlgifts[girl][13]
            outdict[girl]["gift15"] = defaultgirlgifts[girl][14]
            outdict[girl]["gift16"] = defaultgirlgifts[girl][15]
            outdict[girl]["gift17"] = defaultgirlgifts[girl][16]
            outdict[girl]["gift18"] = defaultgirlgifts[girl][17]
            outdict[girl]["gift19"] = defaultgirlgifts[girl][18]
            outdict[girl]["gift20"] = defaultgirlgifts[girl][19]
            outdict[girl]["gift21"] = defaultgirlgifts[girl][20]
            outdict[girl]["gift22"] = defaultgirlgifts[girl][21]
            outdict[girl]["gift23"] = defaultgirlgifts[girl][22]
            outdict[girl]["gift24"] = defaultgirlgifts[girl][23]

        if options.randomize_girl_trait.value:
            t = random.sample(traits,2)
            outdict[girl]["loves"] = t[0]
            outdict[girl]["hates"] = t[1]
        else:
            outdict[girl]["loves"] = defaultgirltraits[girl][0]
            outdict[girl]["hates"] = defaultgirltraits[girl][1]

    return outdict

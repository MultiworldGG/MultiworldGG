GAME_NAME: str = "Pokemon Snap"
CLIENT_NAME: str = "Pokemon Snap Client"
MIN_UNIVERSAL_TRACKER_VERSION: tuple  = (0, 2, 11)

ADAPTER_SCRIPT_NAME: str = "ap_psnap_pj64_adapter_30.js"
PJ64_ENCODING: str = "cp1252"
PJ64_PORT_KEY_NAME: str = "psnap_ap_port"

INITIAL_STATUS: str = "Waiting to connect to Project 64"
DISCONNECTED_STATUS: str = "Unable to connect to Project 64. Attempting again in 5 seconds..."
WRONG_GAME: str = "Wrong game was detected, please load a North American version of Pokemon Snap"
CONNECTING_STATUS: str = "Connected to Project64."
CONNECTED_STATUS: str = "Connected to Project64 and Archipelago, ready to play!"

course = lambda name, course: f'{name} ({course})'

# Courses
START_GAME  = "Start Game"
LVL_BEACH   = "Beach"
LVL_TUNNEL  = "Tunnel"
LVL_VOLCANO = "Volcano"
LVL_RIVER   = "River"
LVL_CAVE    = "Cave"
LVL_VALLEY  = "Valley"
LVL_CLOUD   = "Rainbow Cloud"

ALL_MAIN_LEVELS = [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY]
ALL_LEVELS      = ALL_MAIN_LEVELS + [LVL_CLOUD]

# Items
FILM_UPGRADE  = "Film Capacity Upgrade"
PESTER_BALL   = "Pester Balls"
POKEMON_FOOD  = "Pokemon Food"
APPLE         = "Apples"
POKEFLUTE     = "PokeFlute"
DASH_ENGINE   = "Dash Engine"
SIGN_DETECTOR = "Pokemon Sign Detector"
WDFL_SCORING  = "Good Technique Scoring"
MULT_SCORING  = "Multiple Pokemon Scoring"
PROG_SCORING  = "Progressive Scoring"

L_TO_STOP     = "Press L to Stop"
MULT_WO_WDFL  = "Multiple without Wonderful"

VICTORY_ITEM_NAME = "A Picture of the Rare Pokémon Mew"
VICTORY_ITEM_ID = 10000

# Signs
BEACH_SIGN   = "Kingler Rock"
TUNNEL_SIGN  = "Pinsir's Shadow"
VOLCANO_SIGN = "Koffing Smoke"
RIVER_SIGN   = "Cubone Tree"
CAVE_SIGN    = "The Mewtwo Constellation"
VALLEY_SIGN  = "Dugtrio Mountain"

ALL_SIGNS = [BEACH_SIGN, TUNNEL_SIGN, VOLCANO_SIGN, RIVER_SIGN, CAVE_SIGN, VALLEY_SIGN]

# Special Poses
SURFING_PIKACHU       = "Surfing Pikachu"
PIKACHU_ON_A_BALL     = "Pikachu on a Ball"
BALLOON_PIKACHU       = "Balloon Pikachu"
SPEED_PIKACHU         = "Speed Pikachu"
PIKACHU_ON_A_STUMP    = "Pikachu on a Stump"
FLYING_PIKACHU        = "Flying Pikachu"

GUST_USING_PIDGEY     = "Gust-Using Pidgey"
JIGGLYPUFF_ON_STAGE   = "Jigglypuff on Stage"
GRAVELERS_GROUP_DANCE = "Graveler's Group Dance"
RARE_POKEMON_MEW      = "Rare Pokemon Mew"
FIGHTING_MAGMAR       = "Fighting Magmar"
JIGGLYPUFF_TRIO       = "Jigglypuff Trio on Stage"

# Oak Rewards
POKEMON_TOTAL_6  = "6 Pokemon Photographed"
POKEMON_TOTAL_22 = "22 Pokemon Photographed"
POKEMON_TOTAL_40 = "40 Pokemon Photographed"

REPORT_SCORE_24_000  = "24,000 PKMN Report Score"
REPORT_SCORE_72_500  = "72,500 PKMN Report Score"
REPORT_SCORE_130_000 = "130,000 PKMN Report Score"

# Pokemon Species (in-game)
ARCANINE = "Arcanine"
ARTICUNO = "Articuno"
BULBASAUR = "Bulbasaur"
BUTTERFREE = "Butterfree"
CHANSEY = "Chansey"
CHARIZARD = "Charizard"
CHARMANDER = "Charmander"
CHARMELEON = "Charmeleon"
CLOYSTER = "Cloyster"
DIGLETT = "Diglett"
DITTO = "Ditto"
DODUO = "Doduo"
DRAGONITE = "Dragonite"
DRATINI = "Dratini"
DUGTRIO = "Dugtrio"
EEVEE = "Eevee"
ELECTABUZZ = "Electabuzz"
ELECTRODE = "Electrode"
GEODUDE = "Geodude"
GOLDEEN = "Goldeen"
GRAVELER = "Graveler"
GRIMER = "Grimer"
GROWLITHE = "Growlithe"
GYARADOS = "Gyarados"
HAUNTER = "Haunter"
JIGGLYPUFF = "Jigglypuff"
JYNX = "Jynx"
KAKUNA = "Kakuna"
KANGASKHAN = "Kangaskhan"
KOFFING = "Koffing"
LAPRAS = "Lapras"
MAGIKARP = "Magikarp"
MAGMAR = "Magmar"
MAGNEMITE = "Magnemite"
MAGNETON = "Magneton"
MANKEY = "Mankey"
MEOWTH = "Meowth"
METAPOD = "Metapod"
MEW = "Mew"
MOLTRES = "Moltres"
MUK = "Muk"
PIDGEY = "Pidgey"
PIKACHU = "Pikachu"
POLIWAG = "Poliwag"
PORYGON = "Porygon"
PSYDUCK = "Psyduck"
RAPIDASH = "Rapidash"
SANDSHREW = "Sandshrew"
SANDSLASH = "Sandslash"
SCYTHER = "Scyther"
SHELLDER = "Shellder"
SLOWBRO = "Slowbro"
SLOWPOKE = "Slowpoke"
SNORLAX = "Snorlax"
SQUIRTLE = "Squirtle"
STARMIE = "Starmie"
STARYU = "Staryu"
VICTREEBEL = "Victreebel"
VILEPLUME = "Vileplume"
VULPIX = "Vulpix"
WEEPINBELL = "Weepinbell"
ZAPDOS = "Zapdos"
ZUBAT = "Zubat"

ALL_INGAME_POKEMON = [
    ARCANINE, ARTICUNO, BULBASAUR, BUTTERFREE, CHANSEY, CHARIZARD, 
    CHARMANDER, CHARMELEON, CLOYSTER, DIGLETT, DITTO, DODUO, DRAGONITE, 
    DRATINI, DUGTRIO, EEVEE, ELECTABUZZ, ELECTRODE, GEODUDE, GOLDEEN, 
    GRAVELER, GRIMER, GROWLITHE, GYARADOS, HAUNTER, JIGGLYPUFF, JYNX, 
    KAKUNA, KANGASKHAN, KOFFING, LAPRAS, MAGIKARP, MAGMAR, MAGNEMITE, 
    MAGNETON, MANKEY, MEOWTH, METAPOD, MEW, MOLTRES, MUK, PIDGEY, PIKACHU, 
    POLIWAG, PORYGON, PSYDUCK, RAPIDASH, SANDSHREW, SANDSLASH, SCYTHER, 
    SHELLDER, SLOWBRO, SLOWPOKE, SNORLAX, SQUIRTLE, STARMIE, STARYU, 
    VICTREEBEL, VILEPLUME, VULPIX, WEEPINBELL, ZAPDOS, ZUBAT, 
]

ORIGINAL_151 = [
    "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle",
    "Wartortle", "Blastoise", "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna",
    "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata", "Raticate", "Spearow", "Fearow",
    "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran", "Nidorina",
    "Nidoqueen", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales",
    "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras",
    "Parasect", "Venonat", "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck",
    "Golduck", "Mankey", "Primeape", "Growlithe", "Arcanine", "Poliwag", "Poliwhirl",
    "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp", "Bellsprout",
    "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem",
    "Ponyta", "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd",
    "Doduo", "Dodrio", "Seel", "Dewgong", "Grimer", "Muk", "Shellder", "Cloyster", "Gastly",
    "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby", "Kingler", "Voltorb",
    "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan",
    "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela",
    "Kangaskhan", "Horsea", "Seadra", "Goldeen", "Seaking", "Staryu", "Starmie",
    "Mr.Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir", "Tauros", "Magikarp",
    "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon",
    "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno",
    "Zapdos", "Moltres", "Dratini", "Dragonair", "Dragonite", "Mewtwo", "Mew"
]

TRASH_PIC_ADJECTIVES = [
    "Scuffed", "Tarnished", "Torn", 
    "Burned", "Waterlogged", "Damp", 
    "Dusty", "Musty", "Singed", 
    "Faded", "Pretty Bad"
]

GOAL_SIGN_PICS = 0
GOAL_POKEMON_PICS = 1

SIGN_PIC_NAME    = "Sign Picture"
POKEMON_PIC_NAME = "Pokemon Picture"

DEFAULT_GOAL_TYPE = GOAL_SIGN_PICS
DEFAULT_SIGN_REQUIREMENT = 6
DEFAULT_POKEMON_REQUIREMENT = 50

SIMPLE_TRASH_ITEM_NAME = "Bad Picture"
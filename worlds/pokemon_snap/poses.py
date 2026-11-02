from typing import NamedTuple

from .constants import *

class PokemonSnapPoseData(NamedTuple):
    id: int
    pokemon: str
    score: int
    phrase: str

regular_pose = lambda pose_data:  f'{pose_data.pokemon} Pose: "{pose_data.phrase}"'

def regular_pose_id(game_pose_id: int, pokemon_slot_id: int):
    ap_pose_id = POSE_REMAPPING.get(game_pose_id, game_pose_id)
    return 100000 + 1000 * pokemon_slot_id + ap_pose_id


# Beach
PIDGEY_SCREECH      = PokemonSnapPoseData(id=1,   score=1250, pokemon=PIDGEY,     phrase="Oh! It seems to be screeching.")
MEOWTH_FUNNY        = PokemonSnapPoseData(id=128, score=800,  pokemon=MEOWTH,     phrase="It's pretty funny.")
MEOWTH_FAINTED      = PokemonSnapPoseData(id=129, score=800,  pokemon=MEOWTH,     phrase="It seems to have fainted.")
MEOWTH_PESTER       = PokemonSnapPoseData(id=130, score=800,  pokemon=MEOWTH,     phrase="You've thrown a PESTER BALL.")
MEOWTH_DANCING      = PokemonSnapPoseData(id=131, score=1200, pokemon=MEOWTH,     phrase="Oh! A dancing MEOWTH!")
DODUO_HIT           = PokemonSnapPoseData(id=123, score=1300, pokemon=DODUO,      phrase="Oh! You hit 'em!")
DODUO_FAINTED       = PokemonSnapPoseData(id=124, score=1300, pokemon=DODUO,      phrase="Oh! It just fainted.")
DODUO_WAKING        = PokemonSnapPoseData(id=125, score=1300, pokemon=DODUO,      phrase="Oh! It's about to wake up.")
CHANSEY_JOLLY       = PokemonSnapPoseData(id=122, score=1200, pokemon=CHANSEY,    phrase="Oh! It looks jolly.")
CHANSEY_FUNNY       = PokemonSnapPoseData(id=161, score=1000, pokemon=CHANSEY,    phrase="What a funny pose.")
KANGASKHAN_ANGRY    = PokemonSnapPoseData(id=126, score=1000, pokemon=KANGASKHAN, phrase="This angry shot is pretty cool.")
KANGASKHAN_DANCE    = PokemonSnapPoseData(id=127, score=1050, pokemon=KANGASKHAN, phrase="Oh! What an interesting pose!")
SCYTHER_FIGHTING    = PokemonSnapPoseData(id=2,   score=1300, pokemon=SCYTHER,    phrase="Oh! This is a fighting pose.")
LAPRAS_RELAXED      = PokemonSnapPoseData(id=4,   score=1000, pokemon=LAPRAS,     phrase="This is a relaxed pose.")
EEVEE_HAPPY         = PokemonSnapPoseData(id=3,   score=1250, pokemon=EEVEE,      phrase="Oh! It's happy.")
SNORLAX_FOR_SURE    = PokemonSnapPoseData(id=132, score=800,  pokemon=SNORLAX,    phrase="That's SNORLAX for sure!")
SNORLAX_JOLLY       = PokemonSnapPoseData(id=133, score=1200, pokemon=SNORLAX,    phrase="Oh! What a jolly dance!")
SNORLAX_WAKING      = PokemonSnapPoseData(id=162, score=800,  pokemon=SNORLAX,    phrase="It's about to get up.")
SNORLAX_SCRATCHING  = PokemonSnapPoseData(id=163, score=1000, pokemon=SNORLAX,    phrase="It's scratching its tummy.")

PIKACHU_BEACH_ZAPS_EVEN_ME  = PokemonSnapPoseData(id=134, score=1300, pokemon=course(PIKACHU,  LVL_BEACH), phrase="This pose zaps even me!")
PIKACHU_BEACH_VERY_LIVELY   = PokemonSnapPoseData(id=135, score=1250, pokemon=course(PIKACHU,  LVL_BEACH), phrase="Oh! This is very lively!")
MAGIKARP_BEACH_GOOD_SPLASH  = PokemonSnapPoseData(id=50,  score=1000, pokemon=course(MAGIKARP, LVL_BEACH), phrase="That's a good splash.")

# Tunnel
DIGLETT_UNDERGROUND = PokemonSnapPoseData(id=35,  score=1000, pokemon=DIGLETT,    phrase="It's trying to go underground.")
DIGLETT_POP_UP      = PokemonSnapPoseData(id=160, score=1000, pokemon=DIGLETT,    phrase="It's about to pop up.")
DUGTRIO_UNDERGROUND = PokemonSnapPoseData(id=37,  score=1000, pokemon=DUGTRIO,    phrase="It's trying to go underground.")
DUGTRIO_POP_UP      = PokemonSnapPoseData(id=158, score=1000, pokemon=DUGTRIO,    phrase="It's about to pop up.")
# MAGNEMITE_SURPRISED = PokemonSnapPoseData(id=33,  score=1200, pokemon=MAGNEMITE,  phrase="Oh! It's surprised!")
MAGNEMITE_HAPPY     = PokemonSnapPoseData(id=34,  score=800,  pokemon=MAGNEMITE,  phrase="It sure is happy!")
ELECTRODE_ROLLING   = PokemonSnapPoseData(id=27,  score=500,  pokemon=ELECTRODE,  phrase="It's rolling...")
ELECTRODE_EXPLODED  = PokemonSnapPoseData(id=28,  score=1200, pokemon=ELECTRODE,  phrase="Oh! It exploded!")
ELECTABUZZ_BLAST    = PokemonSnapPoseData(id=29,  score=800,  pokemon=ELECTABUZZ, phrase="It's a blast!")
ELECTABUZZ_FAINTED  = PokemonSnapPoseData(id=30,  score=800,  pokemon=ELECTABUZZ, phrase="Oh dear, it fainted.")
ELECTABUZZ_PESTER   = PokemonSnapPoseData(id=31,  score=800,  pokemon=ELECTABUZZ, phrase="You've thrown a PESTER BALL.")
ELECTABUZZ_ANGRY    = PokemonSnapPoseData(id=32,  score=1000, pokemon=ELECTABUZZ, phrase="It must be angry.")
ELECTABUZZ_YUMMY    = PokemonSnapPoseData(id=154, score=1200, pokemon=ELECTABUZZ, phrase="Oh! It looks yummy!")
ZAPDOS_THUNDER      = PokemonSnapPoseData(id=13,  score=1350, pokemon=ZAPDOS,     phrase="Oh! What a Thunder Jolt!")

MAGIKARP_TUNNEL_SPLASHED    = PokemonSnapPoseData(id=49,  score=800,  pokemon=course(MAGIKARP, LVL_TUNNEL), phrase="It splashed!")
PIKACHU_TUNNEL_ZAPS_EVEN_ME = PokemonSnapPoseData(id=134, score=1300, pokemon=course(PIKACHU,  LVL_TUNNEL), phrase="This pose zaps even me!")
PIKACHU_TUNNEL_VERY_LIVELY  = PokemonSnapPoseData(id=135, score=1250, pokemon=course(PIKACHU,  LVL_TUNNEL), phrase="Oh! This is very lively!")
PIKACHU_TUNNEL_THATS_PIKA   = PokemonSnapPoseData(id=145, score=1400, pokemon=course(PIKACHU,  LVL_TUNNEL), phrase="Oh! That's PIKA!")

# Volcano
CHARMANDER_UNSTABLE = PokemonSnapPoseData(id=103, score=800,  pokemon=CHARMANDER, phrase="It's unstable...")
CHARMANDER_HMM      = PokemonSnapPoseData(id=104, score=800,  pokemon=CHARMANDER, phrase="Hmm...")
CHARMANDER_PESTER   = PokemonSnapPoseData(id=105, score=800,  pokemon=CHARMANDER, phrase="You've thrown a PESTER BALL.")
CHARMANDER_HAPPY    = PokemonSnapPoseData(id=106, score=1200, pokemon=CHARMANDER, phrase="Oh! It looks happy!")
CHARMELEON_FALL     = PokemonSnapPoseData(id=112, score=800,  pokemon=CHARMELEON, phrase="It's about to fall.")
CHARMELEON_FAINTED  = PokemonSnapPoseData(id=113, score=800,  pokemon=CHARMELEON, phrase="It seems to have fainted.")
CHARMELEON_AWOKEN   = PokemonSnapPoseData(id=114, score=800,  pokemon=CHARMELEON, phrase="It seems to have woken up.")
CHARMELEON_ROARING  = PokemonSnapPoseData(id=115, score=1200, pokemon=CHARMELEON, phrase="Oh! It's roaring!")
CHARIZARD_SHOCKED   = PokemonSnapPoseData(id=101, score=900,  pokemon=CHARIZARD,  phrase="It looks like it's shocked.")
CHARIZARD_FLAME     = PokemonSnapPoseData(id=102, score=1250, pokemon=CHARIZARD,  phrase="Oh! What a flame!")
VULPIX_PESTER       = PokemonSnapPoseData(id=116, score=800,  pokemon=VULPIX,     phrase="You've thrown a PESTER BALL.")
# VULPIX_117          = PokemonSnapPoseData(id=117, score=800,  pokemon=VULPIX,     phrase="You've thrown a PESTER BALL.")
# VULPIX_118          = PokemonSnapPoseData(id=118, score=800,  pokemon=VULPIX,     phrase="You've thrown a PESTER BALL.")
VULPIX_HAPPY        = PokemonSnapPoseData(id=119, score=1000, pokemon=VULPIX,     phrase="Hmm... It looks happy.")
GROWLITHE_EMBERS    = PokemonSnapPoseData(id=7,   score=1300, pokemon=GROWLITHE,  phrase="Oh! Tons of embers!")
ARCANINE_EMBERS     = PokemonSnapPoseData(id=6,   score=1200, pokemon=ARCANINE,   phrase="Oh! So many embers!")
RAPIDASH_NEIGHING   = PokemonSnapPoseData(id=5,   score=1200, pokemon=RAPIDASH,   phrase="Oh! It's neighing.")
MAGMAR_UNSTABLE     = PokemonSnapPoseData(id=108, score=800,  pokemon=MAGMAR,     phrase="It's unstable...")
MAGMAR_PRETTY_FUNNY = PokemonSnapPoseData(id=109, score=800,  pokemon=MAGMAR,     phrase="This is pretty funny!")
MAGMAR_SO_FUNNY     = PokemonSnapPoseData(id=110, score=800,  pokemon=MAGMAR,     phrase="Ha, ha, ha! This is so funny!")
MAGMAR_DIZZY        = PokemonSnapPoseData(id=107, score=1000, pokemon=MAGMAR,     phrase="Interesting! It's dizzy!")
MAGMAR_HOT          = PokemonSnapPoseData(id=111, score=1200, pokemon=MAGMAR,     phrase="Oh! It looks hot!")
MOLTRES_WONDERFUL   = PokemonSnapPoseData(id=100, score=1350, pokemon=MOLTRES,    phrase="Oh! What a wonderful pose!")

MAGIKARP_VOLCANO_GOOD_SPLASH = PokemonSnapPoseData(id=50,  score=1000, pokemon=course(MAGIKARP, LVL_VOLCANO), phrase="That's a good splash.")

# River
VILEPLUME_FUN_DANCE = PokemonSnapPoseData(id=84,  score=1000, pokemon=VILEPLUME,  phrase="Isn't the Pokémon dance fun?")
VILEPLUME_ROCKIN    = PokemonSnapPoseData(id=85,  score=1200, pokemon=VILEPLUME,  phrase="Oh! It's rockin'!")
VILEPLUME_WAKING    = PokemonSnapPoseData(id=86,  score=1350, pokemon=VILEPLUME,  phrase="Oh! It's about to wake up!")
PSYDUCK_SUBMERGING  = PokemonSnapPoseData(id=95,  score=800,  pokemon=PSYDUCK,    phrase="It's submerging.")
PSYDUCK_IT_JUMPED   = PokemonSnapPoseData(id=91,  score=800,  pokemon=PSYDUCK,    phrase="It jumped.")
PSYDUCK_FALLING     = PokemonSnapPoseData(id=93,  score=1000, pokemon=PSYDUCK,    phrase="It's about to fall.")
PSYDUCK_NICE_JUMP   = PokemonSnapPoseData(id=90,  score=1000, pokemon=PSYDUCK,    phrase="Nice jump.")
PSYDUCK_UNIQUE      = PokemonSnapPoseData(id=94,  score=1000, pokemon=PSYDUCK,    phrase="Quite unique!")
PSYDUCK_WHAT_A_JUMP = PokemonSnapPoseData(id=92,  score=1200, pokemon=PSYDUCK,    phrase="Oh! What a jump!")
POLIWAG_DIZZY       = PokemonSnapPoseData(id=55,  score=800,  pokemon=POLIWAG,    phrase="It's dizzy.")
POLIWAG_FAINTED     = PokemonSnapPoseData(id=56,  score=800,  pokemon=POLIWAG,    phrase="Oh dear, it fainted.")
POLIWAG_WAKING      = PokemonSnapPoseData(id=57,  score=800,  pokemon=POLIWAG,    phrase="Oh! It's about to wake up.")
POLIWAG_JUMPING     = PokemonSnapPoseData(id=53,  score=800,  pokemon=POLIWAG,    phrase="It's jumping.")
POLIWAG_NICE_JUMP   = PokemonSnapPoseData(id=52,  score=1000, pokemon=POLIWAG,    phrase="Nice jump.")
POLIWAG_JUMPING_IN  = PokemonSnapPoseData(id=58,  score=1150, pokemon=POLIWAG,    phrase="Oh! It's about to jump in!")
POLIWAG_WHAT_A_JUMP = PokemonSnapPoseData(id=54,  score=1200, pokemon=POLIWAG,    phrase="Oh! What a jump!")
SLOWPOKE_WILL_FISH  = PokemonSnapPoseData(id=89,  score=1000, pokemon=SLOWPOKE,   phrase="It looks like it's going to fish.")
SLOWPOKE_FISHING    = PokemonSnapPoseData(id=156, score=1000, pokemon=SLOWPOKE,   phrase="Gone fishing...")
SLOWPOKE_OH_A_BITE  = PokemonSnapPoseData(id=157, score=1200, pokemon=SLOWPOKE,   phrase="Oh! It got a bite!")
SLOWBRO_EATING      = PokemonSnapPoseData(id=11,  score=1300, pokemon=SLOWBRO,    phrase="Oh! It's enjoying the food.")
SHELLDER_CAUGHT     = PokemonSnapPoseData(id=87,  score=1200, pokemon=SHELLDER,   phrase="Oh! It's been caught!")
SHELLDER_SNAPPING   = PokemonSnapPoseData(id=88,  score=1200, pokemon=SHELLDER,   phrase="Oh! It's snapping!")
PORYGON_HAPPY       = PokemonSnapPoseData(id=81,  score=1000, pokemon=PORYGON,    phrase="Hmm... It looks happy.")
PORYGON_LOOKS_JOLLY = PokemonSnapPoseData(id=82,  score=1000, pokemon=PORYGON,    phrase="Hmm... It looks jolly.")
PORYGON_SURE_JOLLY  = PokemonSnapPoseData(id=83,  score=1400, pokemon=PORYGON,    phrase="Oh! It sure is jolly!")

BULBASAUR_RIVER_PESTER       = PokemonSnapPoseData(id=96,  score=800,  pokemon=course(BULBASAUR, LVL_RIVER), phrase="You've thrown a PESTER BALL.")
# BULBASAUR_RIVER_97           = PokemonSnapPoseData(id=97,  score=800,  pokemon=BULBASAUR,  phrase="You've thrown a PESTER BALL.")
# BULBASAUR_RIVER_98           = PokemonSnapPoseData(id=98,  score=800,  pokemon=BULBASAUR,  phrase="You've thrown a PESTER BALL.")
BULBASAUR_RIVER_HAPPY        = PokemonSnapPoseData(id=99,  score=1200, pokemon=course(BULBASAUR, LVL_RIVER), phrase="Oh! What a happy face!")
MAGIKARP_RIVER_GOOD_SPLASH   = PokemonSnapPoseData(id=50,  score=1000, pokemon=course(MAGIKARP,  LVL_RIVER), phrase="That's a good splash.")
MAGIKARP_RIVER_SPLASHED      = PokemonSnapPoseData(id=49,  score=800,  pokemon=course(MAGIKARP,  LVL_RIVER), phrase="It splashed!")
MAGIKARP_RIVER_WHAT_A_SPLASH = PokemonSnapPoseData(id=48,  score=1200, pokemon=course(MAGIKARP,  LVL_RIVER), phrase="Oh! What a splash!")
PIKACHU_RIVER_ZAPS_EVEN_ME   = PokemonSnapPoseData(id=134, score=1300, pokemon=course(PIKACHU,   LVL_RIVER), phrase="This pose zaps even me!")

# Cave
JIGGLYPUFF_DANCE    = PokemonSnapPoseData(id=24,  score=1000, pokemon=JIGGLYPUFF, phrase="JIGGLYPUFF's dance is great!")
JIGGLYPUFF_SHAME    = PokemonSnapPoseData(id=25,  score=1200, pokemon=JIGGLYPUFF, phrase="Oh! That's a shame...")
JIGGLYPUFF_SINGING  = PokemonSnapPoseData(id=26,  score=1400, pokemon=JIGGLYPUFF, phrase="Oh! It's singing cheerfully.")
VICTREEBEL_LEAPING  = PokemonSnapPoseData(id=10,  score=1300, pokemon=VICTREEBEL, phrase="Oh! It's about to leap out!")
GRIMER_HAPPY        = PokemonSnapPoseData(id=16,  score=1150, pokemon=GRIMER,     phrase="Oh! It's happy.")
MUK_HAPPY           = PokemonSnapPoseData(id=15,  score=1000, pokemon=MUK,        phrase="It looks happy.")
JYNX_JOLLY_DANCE    = PokemonSnapPoseData(id=17,  score=1200, pokemon=JYNX,       phrase="Oh! What a jolly dance!")
DITTO_HAPPY         = PokemonSnapPoseData(id=14,  score=1150, pokemon=DITTO,      phrase="Oh! It's happy.")
ARTICUNO_BEAUTIFUL  = PokemonSnapPoseData(id=18,  score=1350, pokemon=ARTICUNO,   phrase="Oh! How beautiful!")
KOFFING_WEIRD_DANCE = PokemonSnapPoseData(id=155, score=1200, pokemon=KOFFING,    phrase="Oh! What a weird dance.")

MAGIKARP_CAVE_WHAT_A_SPLASH = PokemonSnapPoseData(id=48,  score=1200, pokemon=course(MAGIKARP, LVL_CAVE),   phrase="Oh! What a splash!")
PIKACHU_CAVE_VERY_LIVELY    = PokemonSnapPoseData(id=135, score=1250, pokemon=course(PIKACHU, LVL_CAVE),    phrase="Oh! This is very lively!")
PIKACHU_CAVE_ZAPS_EVEN_ME   = PokemonSnapPoseData(id=134, score=1300, pokemon=course(PIKACHU, LVL_CAVE),    phrase="This pose zaps even me!")

# Valley
SQUIRTLE_PESTER     = PokemonSnapPoseData(id=74,  score=800,  pokemon=SQUIRTLE,   phrase="You've thrown a PESTER BALL.")
# SQUIRTLE_75         = PokemonSnapPoseData(id=75,  score=800,  pokemon=SQUIRTLE,   phrase="You've thrown a PESTER BALL.")
# SQUIRTLE_76         = PokemonSnapPoseData(id=76,  score=800,  pokemon=SQUIRTLE,   phrase="You've thrown a PESTER BALL.")
SQUIRTLE_WITHDRAW   = PokemonSnapPoseData(id=77,  score=500,  pokemon=SQUIRTLE,   phrase="It's about to withdraw.")
SQUIRTLE_SHELL      = PokemonSnapPoseData(id=78,  score=150,  pokemon=SQUIRTLE,   phrase="I only see its shell.")
SQUIRTLE_COMING_OUT = PokemonSnapPoseData(id=79,  score=900,  pokemon=SQUIRTLE,   phrase="It's about to come out.")
SQUIRTLE_HAPPY      = PokemonSnapPoseData(id=80,  score=1100, pokemon=SQUIRTLE,   phrase="Oh! It's happy!")
SANDSHREW_PESTER    = PokemonSnapPoseData(id=59,  score=800,  pokemon=SANDSHREW,  phrase="You've thrown a PESTER BALL.")
# SANDSHREW_60        = PokemonSnapPoseData(id=60,  score=800,  pokemon=SANDSHREW,  phrase="You've thrown a PESTER BALL.")
# SANDSHREW_61        = PokemonSnapPoseData(id=61,  score=800,  pokemon=SANDSHREW,  phrase="You've thrown a PESTER BALL.")
SANDSHREW_POP_UP    = PokemonSnapPoseData(id=62,  score=1350, pokemon=SANDSHREW,  phrase="Oh! It's about to pop up.")
# SANDSHREW_GO_UNDER  = PokemonSnapPoseData(id=63,  score=800,  pokemon=SANDSHREW,  phrase="It's about to go underground.")
SANDSHREW_JOLLY     = PokemonSnapPoseData(id=64,  score=1000, pokemon=SANDSHREW,  phrase="Hmm... It looks jolly.")
SANDSLASH_STUMBLED  = PokemonSnapPoseData(id=65,  score=800,  pokemon=SANDSLASH,  phrase="It stumbled.")
# SANDSLASH_66        = PokemonSnapPoseData(id=66,  score=800,  pokemon=SANDSLASH,  phrase="It stumbled.")
# SANDSLASH_67        = PokemonSnapPoseData(id=67,  score=800,  pokemon=SANDSLASH,  phrase="It stumbled.")
SANDSLASH_POP_UP    = PokemonSnapPoseData(id=68,  score=1400, pokemon=SANDSLASH,  phrase="Oh! It's about to pop up.")
SANDSLASH_GO_UNDER  = PokemonSnapPoseData(id=69,  score=850,  pokemon=SANDSLASH,  phrase="It's about to go underground.")
SANDSLASH_HAPPY     = PokemonSnapPoseData(id=70,  score=1050, pokemon=SANDSLASH,  phrase="Oh! It's happy.")
MANKEY_IN_THE_SKY   = PokemonSnapPoseData(id=44,  score=1250, pokemon=MANKEY,     phrase="Oh! It's MANKEY in the sky!")
MANKEY_BLASTED      = PokemonSnapPoseData(id=45,  score=1250, pokemon=MANKEY,     phrase="Oh! MANKEY got blasted!")
MANKEY_PESTER       = PokemonSnapPoseData(id=46,  score=800,  pokemon=MANKEY,     phrase="You've thrown a PESTER BALL.")
GRAVELER_FALLING    = PokemonSnapPoseData(id=41,  score=1200, pokemon=GRAVELER,   phrase="Oh! It's falling.")
# GRAVELER_42         = PokemonSnapPoseData(id=42,  score=1200, pokemon=GRAVELER,   phrase="Oh! It's falling.")
GRAVELER_FELL       = PokemonSnapPoseData(id=43,  score=1200, pokemon=GRAVELER,   phrase="Oh! It fell.")
GOLDEEN_GOOD_SPLASH = PokemonSnapPoseData(id=71,  score=1000, pokemon=GOLDEEN,    phrase="That's a good splash!")
GOLDEEN_SPLASHING   = PokemonSnapPoseData(id=72,  score=800,  pokemon=GOLDEEN,    phrase="It's splashing.")
GOLDEEN_WHAT_A      = PokemonSnapPoseData(id=73,  score=1200, pokemon=GOLDEEN,    phrase="Oh! What a splash!")
GYARADOS_POWERFUL   = PokemonSnapPoseData(id=19,  score=1350, pokemon=GYARADOS,   phrase="Oh! How powerful!")
GYARADOS_SHOW_FACE  = PokemonSnapPoseData(id=20,  score=1000, pokemon=GYARADOS,   phrase="It just showed its face.")
GYARADOS_SCARY      = PokemonSnapPoseData(id=21,  score=1000, pokemon=GYARADOS,   phrase="Umm... looks scary!")
GYARADOS_FURIOUS    = PokemonSnapPoseData(id=22,  score=1200, pokemon=GYARADOS,   phrase="Oh! It's furious!")
GYARADOS_ASTONISHED = PokemonSnapPoseData(id=23,  score=1200, pokemon=GYARADOS,   phrase="Oh! It looks astonished!")
DRATINI_AMAZING     = PokemonSnapPoseData(id=38,  score=1200, pokemon=DRATINI,    phrase="Oh! What an amazing jump!")
DRATINI_GOOD        = PokemonSnapPoseData(id=39,  score=1000, pokemon=DRATINI,    phrase="That's a pretty good jump.")
DRATINI_JUMPING     = PokemonSnapPoseData(id=40,  score=800,  pokemon=DRATINI,    phrase="It's jumping.")
DRAGONITE_OH_IT_IS  = PokemonSnapPoseData(id=12,  score=1200, pokemon=DRAGONITE,  phrase="Oh! It's DRAGONITE!")

MAGIKARP_VALLEY_WHAT_A_SPLASH = PokemonSnapPoseData(id=48,  score=1200, pokemon=course(MAGIKARP, LVL_VALLEY),   phrase="Oh! What a splash!")
MAGIKARP_VALLEY_IT_SPLASHED   = PokemonSnapPoseData(id=49,  score=800,  pokemon=course(MAGIKARP, LVL_VALLEY),   phrase="It splashed!")
MAGIKARP_VALLEY_GOOD_SPLASH   = PokemonSnapPoseData(id=50,  score=1000, pokemon=course(MAGIKARP, LVL_VALLEY),   phrase="That's a good splash.")
MAGIKARP_VALLEY_ITS_SPLASHING = PokemonSnapPoseData(id=51,  score=1200, pokemon=course(MAGIKARP, LVL_VALLEY),   phrase="Oh! It's splashing.")

# Rainbow Cloud
# MEW_FACING          = PokemonSnapPoseData(id=149, score=800,  pokemon=MEW,        phrase="If only it were facing you...")
# MEW_150             = PokemonSnapPoseData(id=150, score=800,  pokemon=MEW,        phrase="If only it were facing you...")
MEW_WELL_DONE       = PokemonSnapPoseData(id=151, score=1350, pokemon=MEW,        phrase="Oh! Well done!")
MEW_SPINNING        = PokemonSnapPoseData(id=152, score=1250, pokemon=MEW,        phrase="Oh! It's spinning.")
MEW_PERFECT         = PokemonSnapPoseData(id=153, score=1500, pokemon=MEW,        phrase="Why, it's perfect!")


POSE_REMAPPING = {
    42: 41,
    60: 59,
    61: 59,
    66: 65,
    67: 65,
    75: 74,
    76: 74,
    97: 96,
    98: 96,
    117: 116,
    118: 116,
}


pose_location_data = {
    LVL_BEACH: [
        PIDGEY_SCREECH,
        MEOWTH_FUNNY,
        MEOWTH_FAINTED,
        MEOWTH_PESTER,
        MEOWTH_DANCING,
        DODUO_HIT,
        DODUO_FAINTED,
        DODUO_WAKING,
        CHANSEY_JOLLY,
        CHANSEY_FUNNY,
        KANGASKHAN_ANGRY,
        KANGASKHAN_DANCE,
        SCYTHER_FIGHTING,
        LAPRAS_RELAXED,
        EEVEE_HAPPY,
        SNORLAX_FOR_SURE,
        SNORLAX_JOLLY,
        SNORLAX_WAKING,
        SNORLAX_SCRATCHING,
        PIKACHU_BEACH_ZAPS_EVEN_ME,
        PIKACHU_BEACH_VERY_LIVELY,
        MAGIKARP_BEACH_GOOD_SPLASH,
    ],
    LVL_TUNNEL: [
        DIGLETT_UNDERGROUND,
        DIGLETT_POP_UP,
        DUGTRIO_UNDERGROUND,
        DUGTRIO_POP_UP,
        MAGNEMITE_HAPPY,
        ELECTRODE_ROLLING,
        ELECTRODE_EXPLODED,
        ELECTABUZZ_BLAST,
        ELECTABUZZ_FAINTED,
        ELECTABUZZ_PESTER,
        ELECTABUZZ_ANGRY,
        ELECTABUZZ_YUMMY,
        ZAPDOS_THUNDER,
        MAGIKARP_TUNNEL_SPLASHED,
        PIKACHU_TUNNEL_ZAPS_EVEN_ME,
        PIKACHU_TUNNEL_VERY_LIVELY,
        PIKACHU_TUNNEL_THATS_PIKA,
    ],
    LVL_VOLCANO: [
        CHARMANDER_UNSTABLE,
        CHARMANDER_HMM,
        CHARMANDER_PESTER,
        CHARMANDER_HAPPY,
        CHARMELEON_FALL,
        CHARMELEON_FAINTED,
        CHARMELEON_AWOKEN,
        CHARMELEON_ROARING,
        CHARIZARD_SHOCKED,
        CHARIZARD_FLAME,
        VULPIX_PESTER,
        VULPIX_HAPPY,
        GROWLITHE_EMBERS,
        ARCANINE_EMBERS,
        RAPIDASH_NEIGHING,
        MAGMAR_DIZZY,
        MAGMAR_UNSTABLE,
        MAGMAR_PRETTY_FUNNY,
        MAGMAR_SO_FUNNY,
        MAGMAR_HOT,
        MOLTRES_WONDERFUL,
        MAGIKARP_VOLCANO_GOOD_SPLASH,
    ],
    LVL_RIVER: [
        VILEPLUME_FUN_DANCE,
        VILEPLUME_ROCKIN,
        VILEPLUME_WAKING,
        PSYDUCK_NICE_JUMP,
        PSYDUCK_IT_JUMPED,
        PSYDUCK_WHAT_A_JUMP,
        PSYDUCK_FALLING,
        PSYDUCK_UNIQUE,
        PSYDUCK_SUBMERGING,
        POLIWAG_NICE_JUMP,
        POLIWAG_JUMPING,
        POLIWAG_WHAT_A_JUMP,
        POLIWAG_DIZZY,
        POLIWAG_FAINTED,
        POLIWAG_WAKING,
        POLIWAG_JUMPING_IN,
        SLOWPOKE_WILL_FISH,
        SLOWPOKE_FISHING,
        SLOWPOKE_OH_A_BITE,
        SLOWBRO_EATING,
        SHELLDER_CAUGHT,
        SHELLDER_SNAPPING,
        PORYGON_HAPPY,
        PORYGON_LOOKS_JOLLY,
        PORYGON_SURE_JOLLY,
        BULBASAUR_RIVER_PESTER,
        BULBASAUR_RIVER_HAPPY,
        MAGIKARP_RIVER_WHAT_A_SPLASH,
        MAGIKARP_RIVER_SPLASHED,
        MAGIKARP_RIVER_GOOD_SPLASH,
        PIKACHU_RIVER_ZAPS_EVEN_ME,
    ],
    LVL_CAVE: [
        JIGGLYPUFF_DANCE,
        JIGGLYPUFF_SHAME,
        JIGGLYPUFF_SINGING,
        VICTREEBEL_LEAPING,
        GRIMER_HAPPY,
        MUK_HAPPY,
        JYNX_JOLLY_DANCE,
        DITTO_HAPPY,
        ARTICUNO_BEAUTIFUL,
        KOFFING_WEIRD_DANCE,
        MAGIKARP_CAVE_WHAT_A_SPLASH,
        PIKACHU_CAVE_ZAPS_EVEN_ME,
        PIKACHU_CAVE_VERY_LIVELY,
    ],
    LVL_VALLEY: [
        SQUIRTLE_PESTER,
        SQUIRTLE_WITHDRAW,
        SQUIRTLE_SHELL,
        SQUIRTLE_COMING_OUT,
        SQUIRTLE_HAPPY,
        SANDSHREW_PESTER,
        SANDSHREW_POP_UP,
        SANDSHREW_JOLLY,
        SANDSLASH_STUMBLED,
        SANDSLASH_POP_UP,
        SANDSLASH_GO_UNDER,
        SANDSLASH_HAPPY,
        MANKEY_IN_THE_SKY,
        MANKEY_BLASTED,
        MANKEY_PESTER,
        GRAVELER_FALLING,
        GRAVELER_FELL,
        GOLDEEN_GOOD_SPLASH,
        GOLDEEN_SPLASHING,
        GOLDEEN_WHAT_A,
        GYARADOS_POWERFUL,
        GYARADOS_SHOW_FACE,
        GYARADOS_SCARY,
        GYARADOS_FURIOUS,
        GYARADOS_ASTONISHED,
        DRATINI_AMAZING,
        DRATINI_GOOD,
        DRATINI_JUMPING,
        DRAGONITE_OH_IT_IS,
        MAGIKARP_VALLEY_WHAT_A_SPLASH,
        MAGIKARP_VALLEY_IT_SPLASHED,
        MAGIKARP_VALLEY_GOOD_SPLASH,
        MAGIKARP_VALLEY_ITS_SPLASHING,
    ],
    LVL_CLOUD: [
        MEW_WELL_DONE,
        MEW_SPINNING,
        MEW_PERFECT,
    ],
}

ALL_POSE_DATA = [pose_data for level in pose_location_data.values() for pose_data in level]

RNG_POSES = [
    # River
    regular_pose(MAGIKARP_RIVER_SPLASHED),
    regular_pose(MAGIKARP_RIVER_GOOD_SPLASH),
    regular_pose(MAGIKARP_RIVER_WHAT_A_SPLASH),
    regular_pose(POLIWAG_NICE_JUMP),
    regular_pose(POLIWAG_JUMPING),
    regular_pose(POLIWAG_WHAT_A_JUMP),
    regular_pose(PSYDUCK_NICE_JUMP),
    regular_pose(PSYDUCK_IT_JUMPED),
    regular_pose(PSYDUCK_WHAT_A_JUMP),
    # Valley
    regular_pose(GOLDEEN_SPLASHING),
    regular_pose(GOLDEEN_GOOD_SPLASH),
    regular_pose(GOLDEEN_WHAT_A),
    regular_pose(DRATINI_JUMPING),
    regular_pose(DRATINI_GOOD),
    regular_pose(DRATINI_AMAZING),
    regular_pose(MAGIKARP_VALLEY_IT_SPLASHED),
    regular_pose(MAGIKARP_VALLEY_GOOD_SPLASH),
    regular_pose(MAGIKARP_VALLEY_WHAT_A_SPLASH),
]

HARD_POSES = [
    # River
    regular_pose(SHELLDER_CAUGHT),
    regular_pose(MAGIKARP_RIVER_WHAT_A_SPLASH),
    regular_pose(POLIWAG_WHAT_A_JUMP),
    regular_pose(PSYDUCK_FALLING),
    regular_pose(PSYDUCK_WHAT_A_JUMP),
    # Cave
    regular_pose(PIKACHU_CAVE_VERY_LIVELY),
    regular_pose(PIKACHU_CAVE_ZAPS_EVEN_ME),
    # Valley
    regular_pose(GOLDEEN_WHAT_A),
    regular_pose(DRATINI_AMAZING),
    regular_pose(MAGIKARP_VALLEY_WHAT_A_SPLASH),
]
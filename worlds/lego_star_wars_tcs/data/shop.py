from .characters import Character, UnlockMethod

# The order that characters appear in the characters shop.
# Indices into this tuple match up with the indices used by the game (unless the game is modded).
CHARACTER_SHOP_SLOTS: tuple[Character, ...] = (
    Character.GONK_DROID,
    Character.PK_DROID,

    Character.BATTLE_DROID,
    Character.BATTLE_DROID_SECURITY,
    Character.BATTLE_DROID_COMMANDER,
    Character.DROIDEKA,

    Character.CAPTAIN_TARPALS,
    Character.BOSS_NASS,

    Character.ROYAL_GUARD,
    Character.PADME,

    Character.WATTO,
    Character.PIT_DROID,

    Character.DARTH_MAUL,

    Character.ZAM_WESELL,
    Character.DEXTER_JETTSTER,

    Character.CLONE,
    Character.LAMA_SU,
    Character.TAUN_WE,

    Character.GEONOSIAN,
    Character.BATTLE_DROID_GEONOSIS,

    Character.SUPER_BATTLE_DROID,
    Character.JANGO_FETT,
    Character.BOBA_FETT_BOY,
    Character.LUMINARA,
    Character.KI_ADI_MUNDI,
    Character.KIT_FISTO,
    Character.SHAAK_TI,
    Character.AAYLA_SECURA,
    Character.PLO_KOON,

    Character.COUNT_DOOKU,
    Character.GRIEVOUS_BODYGUARD,

    Character.GENERAL_GRIEVOUS,

    Character.WOOKIEE,
    Character.CLONE_EPISODE_III,
    Character.CLONE_EPISODE_III_PILOT,
    Character.CLONE_EPISODE_III_SWAMP,
    Character.CLONE_EPISODE_III_WALKER,

    Character.MACE_WINDU_EPISODE_III,
    Character.DISGUISED_CLONE,

    Character.REBEL_TROOPER,
    Character.STORMTROOPER,
    Character.IMPERIAL_SHUTTLE_PILOT,

    Character.TUSKEN_RAIDER,
    Character.JAWA,

    Character.SANDTROOPER,
    Character.GREEDO,
    Character.IMPERIAL_SPY,

    Character.BEACH_TROOPER,
    Character.DEATH_STAR_TROOPER,
    Character.TIE_FIGHTER_PILOT,
    Character.IMPERIAL_OFFICER,
    Character.GRAND_MOFF_TARKIN,

    Character.HAN_SOLO_HOOD,
    Character.REBEL_TROOPER_HOTH,
    Character.REBEL_PILOT,
    Character.SNOWTROOPER,
    Character.LUKE_SKYWALKER_HOTH,

    Character.LOBOT,
    Character.UGNAUGHT,
    Character.BESPIN_GUARD,
    Character.PRINCESS_LEIA_PRISONER,

    Character.GAMORREAN_GUARD,
    Character.BIB_FORTUNA,
    Character.PALACE_GUARD,
    Character.BOSSK,

    Character.SKIFF_GUARD,
    Character.BOBA_FETT,

    Character.EWOK,

    Character.IMPERIAL_GUARD,
    Character.THE_EMPEROR,

    Character.ADMIRAL_ACKBAR,

    Character.IG_88,
    Character.DENGAR,
    Character.FOUR_LOM,
    Character.BEN_KENOBI_GHOST,
    Character.ANAKIN_SKYWALKER_GHOST,
    Character.YODA_GHOST,
    Character.R2_Q5,

    Character.INDIANA_JONES,

    Character.SEBULBAS_POD,

    Character.ZAMS_AIRSPEEDER,

    Character.DROID_TRIFIGHTER,
    Character.VULTURE_DROID,
    Character.CLONE_ARCFIGHTER,

    Character.TIE_FIGHTER,
    Character.TIE_INTERCEPTOR,
    Character.TIE_FIGHTER_DARTH_VADER,

    Character.TIE_BOMBER,
    Character.IMPERIAL_SHUTTLE,
)

def _make_unlock_requirement_to_characters() -> dict[UnlockMethod, list[Character]]:
    requirement_to_characters = {}
    for character in CHARACTER_SHOP_SLOTS:
        requirement_to_characters.setdefault(character.unlock_method, []).append(character)
    return requirement_to_characters
UNLOCK_REQUIREMENT_TO_CHARACTERS: dict[UnlockMethod, list[Character]] = _make_unlock_requirement_to_characters()
del _make_unlock_requirement_to_characters

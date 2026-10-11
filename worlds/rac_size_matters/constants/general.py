"""This module contains string constants for each general game location"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5Locations:
    """String constants for locations"""

    POKITARU_FIGHT = "Pokitaru: Fight some robots (Complete Luna's photoshoot)"
    POKITARU_CHESTPLATE = "Pokitaru: Wildfire Chestplate on bridge"
    POKITARU_GLOVES = "Pokitaru: Wildfire Gloves in the skuttle crab cave"

    RYLLUS_BOOTS = "Ryllus: Sludge Mk9 Boots behind breakable rock"
    RYLLUS_SPROUT = "Ryllus: Receive Sprout-O-Matic"
    RYLLUS_HELMET = "Ryllus: Wildfire Helmet before temple entrance"
    RYLLUS_ARTIFACT = "Ryllus: Investigate the artifact (Reach the temple)"
    RYLLUS_TEMPLE = "Ryllus: Unlock the temple"

    KALIDON_WIN = "Kalidon: Win the skyboard race (Complete Learner's Permit)"
    KALIDON_SHRINK = "Kalidon: Receive Shrink Ray"
    KALIDON_CHESTPLATE = "Kalidon: Sludge Mk9 Chestplate from Mungo Fight"
    KALIDON_BOOTS = "Kalidon: Wildfire Boots inside factory"

    METALIS_WAR = "Metalis: Survive Robot War III (Complete Buzzsaw Blitz)"
    METALIS_ESCAPE = "Metalis: Escape the planet (Giant Clank)"
    METALIS_GLOVES = "Metalis: Electroshock Gloves from Giant Clank"

    DREAMTIME_COMPLETE = "Dreamtime: Complete Dreamtime"
    DREAMTIME_CHESTPLATE = "Dreamtime: Crystallix Chestplate after Giant Clank chase"

    OUTPOST_OMEGA_ESCAPE = "Outpost Omega: Escape the medical facility"
    OUTPOST_OMEGA_BOOTS = "Outpost Omega: Crystallix Boots during escape"
    OUTPOST_OMEGA_REMATCH = "Outpost Omega: Rematch - Skyboard racers (Complete Interior Decorating)"

    CHALLAX_CLANK = "Challax: Destroy the space fortress (Giant Clank)"
    CHALLAX_HELMET = "Challax: Electroshock Helmet after Dropship fight"
    CHALLAX_CHESTPLATE = "Challax: Electroshock Chestplate"

    DAYNI_MOON = "Dayni Moon: Catch Luna"
    DAYNI_MOON_HELMET = "Dayni Moon: Mega Bomb Helmet before Luna fight"
    DAYNI_MOON_LUNA = "Dayni Moon: Defeat Luna"

    INSIDE_CLANK_TECHNOMITES = "Inside Clank: Defeat all Technomites"
    INSIDE_CLANK_ESCAPE = "Inside Clank: Escape from Clank"
    INSIDE_CLANK_CHESTPLATE = "Inside Clank: Mega Bomb Chestplate"

    QUODRONA_FIND = "Quodrona: Find Otto Destruct"
    QUODRONA_GOAL = "Quodrona: Defeat Otto Destruct"

    POKITARU_HYPERBOREAN_GLOVES = "Pokitaru: Hyperborean Gloves"
    RYLLUS_HYPERBOREAN_BOOTS = "Ryllus: Hyperborean Boots"
    DREAMTIME_HYPERBOREAN_CHESTPLATE = "Dreamtime: Hyperborean Chestplate"
    CHALLAX_HYPERBOREAN_HELMET = "Challax: Hyperborean Helmet"
    POKITARU_CHAMELEON_BOOTS = "Pokitaru: Chameleon Boots"
    KALIDON_CHAMELEON_CHESTPLATE = "Kalidon: Chameleon Chestplate"
    OUTPOST_OMEGA_CHAMELEON_GLOVES = "Outpost Omega: Chameleon Gloves"
    INSIDE_CLANK_CHAMELEON_HELMET = "Inside Clank: Chameleon Helmet"

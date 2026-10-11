"""This module contains string constants used for items"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5Armours:
    """String constants for each armour piece"""

    WILDFIRE_CHESTPLATE = "Wildfire Chestplate"
    WILDFIRE_HELMET = "Wildfire Helmet"
    WILDFIRE_GLOVES = "Wildfire Gloves"
    WILDFIFE_BOOTS = "Wildfire Boots"

    SLUDGE_MK9_CHESTPLATE = "Sludge Mk9 Chestplate"
    SLUDGE_MK9_HELMET = "Sludge Mk9 Helmet"
    SLUDGE_MK9_GLOVES = "Sludge Mk9 Gloves"
    SLUDGE_MK9_BOOTS = "Sludge Mk9 Boots"

    CRYSTALLIX_CHESTPLATE = "Crystallix Chestplate"
    CRYSTALLIX_HELMET = "Crystallix Helmet"
    CRYSTALLIX_GLOVES = "Crystallix Gloves"
    CRYSTALLIX_BOOTS = "Crystallix Boots"

    ELECTROSHOCK_CHESTPLATE = "Electroshock Chestplate"
    ELECTROSHOCK_HELMET = "Electroshock Helmet"
    ELECTROSHOCK_GLOVES = "Electroshock Gloves"
    ELECTROSHOCK_BOOTS = "Electroshock Boots"

    MEGA_BOMB_CHESTPLATE = "Mega Bomb Chestplate"
    MEGA_BOMB_HELMET = "Mega Bomb Helmet"
    MEGA_BOMB_GLOVES = "Mega Bomb Gloves"
    MEGA_BOMB_BOOTS = "Mega Bomb Boots"

    HYPERBOREAN_CHESTPLATE = "Hyperborean Chestplate"
    HYPERBOREAN_HELMET = "Hyperborean Helmet"
    HYPERBOREAN_GLOVES = "Hyperborean Gloves"
    HYPERBOREAN_BOOTS = "Hyperborean Boots"

    CHAMELEON_CHESTPLATE = "Chameleon Chestplate"
    CHAMELEON_HELMET = "Chameleon Helmet"
    CHAMELEON_GLOVES = "Chameleon Gloves"
    CHAMELEON_BOOTS = "Chameleon Boots"


@dataclass(frozen=True)
class Rac5ProgressiveArmours:
    """String constants for each progressive armour piece"""

    PROGRESSIVE_WILDFIRE = "Progressive Wildfire Armor"
    PROGRESSIVE_SLUDGE_MK9 = "Progressive Sludge Mk9 Armor"
    PROGRESSIVE_CRYSTALLIX = "Progressive Crystallix Armor"
    PROGRESSIVE_ELECTROSHOCK = "Progressive Electroshock Armor"
    PROGRESSIVE_MEGA_BOMB = "Progressive Mega Bomb Armor"
    PROGRESSIVE_HYPERBOREAN = "Progressive Hyperborean Armor"
    PROGRESSIVE_CHAMELEON = "Progressive Chameleon Armor"

    PROGRESSIVE_ARMOUR = "Progressive Armour"


@dataclass(frozen=True)
class Rac5Infobots:
    """String constants for each infobot"""

    POKITARU = "Infobot: Pokitaru"
    RYLLUS = "Infobot: Ryllus"
    KALIDON = "Infobot: Kalidon"
    METALIS = "Infobot: Metalis"
    OUTPOST_OMEGA = "Infobot: Outpost Omega"
    CHALLAX = "Infobot: Challax"
    DAYNI_MOON = "Infobot: Dayni Moon"
    QUODRONA = "Infobot: Quodrona"


class Rac5Filler:
    """String constants for each filler item"""

    BOLTS = "Bolts"


class Rac5Traps:
    """String constants for each trap"""

    TRAP_FEVERDREAMTIME = "Trap: Feverdream"
    TRAP_RESET_LEVEL = "Trap: Reset Level"
    TRAP_BRIGHTNESS = "Trap: Whats Gamma?"
    TRAP_MIRROR_LEVEL = "Trap: Mirror Level"
    TRAP_REVERSE_CONTROLS = "Trap: Reverse Controls"
    TRAP_WEAPON_SWITCHING = "Trap: Weapon Switching"
    TRAP_NO_CLANK = "Trap: No Clank"

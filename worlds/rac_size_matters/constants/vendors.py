"""This module provides a class with all the string constants used for Weapon Vendor names."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5VendorLocations:
    """Constant strings for each Weapon location name."""

    POKITARU_LACERATOR = "Pokitaru: Gadgetron Vendor: Lacerator - 0"
    POKITARU_ACID = "Pokitaru: Gadgetron Vendor: Acid Bomb Glove - 0"
    POKITARU_CONCUSSION = "Pokitaru: Gadgetron Vendor: Concussion Gun - 10,000"
    POKITARU_HYPERSHOT = "Pokitaru: Gadgetron Vendor: Hypershot - 5,000"

    RYLLUS_AGENTS = "Ryllus: Gadgetron Vendor: Agents of Doom - 25,000"
    KALIDON_SCORCHER = "Kalidon: Gadgetron Vendor: Scorcher - 20,000"

    DREAMTIME_SUCK = "Dreamtime: Gadgetron Vendor: Suck Cannon - 30,000"

    OUTPOST_OMEGA_BEE = "Outpost Omega: Gadgetron Vendor: Bee Mine Glove - 50,000"
    OUTPOST_OMEGA_BOX_BREAKER = "Outpost Omega: Gadgetron Vendor: Box Breaker - 20,000"

    CHALLAX_SNIPER = "Challax: Gadgetron Vendor: Sniper Mine - 50,000"
    CHALLAX_PDA = "Challax: Gadgetron Vendor: PDA - 50,000"
    CHALLAX_BOLT_GRABBER = "Challax: Gadgetron Vendor: Bolt Grabber - 5,000"

    DAYNI_MOON_SHOCK = "Dayni Moon: Gadgetron Vendor: Shock Rocket - 55,000"
    DAYNI_MOON_MAP = "Dayni Moon: Gadgetron Vendor: Map-O-Matic - 50,000"

    INSIDE_CLANK_STATIC = "Inside Clank: Gadgetron Vendor: Static Barrier - 65,000"

    QUODRONA_LASER = "Quodrona: Gadgetron Vendor: Laser Tracer - 85,000"

    POKITARU_RYNO = "Pokitaru: Gadgetron Vendor: RYNO - 9,990,000"


class Rac5ModVendorLocations:
    """String constants for Weapon Mod locations"""

    KALIDON_LACERATOR_LOCK = "Kalidon: Slim Cognito: Lacerator Lock On Mod - 5,000"
    KALIDON_CONCUSSION_SPLIT = "Kalidon: Slim Cognito: Concussion Gun Split Barrel Mod - 15,000"

    CHALLAX_LACERATOR_DOUBLE = "Challax: Slim Cognito: Lacerator Double Barrel Mod - 30,000"
    CHALLAX_ACID_BURN = "Challax: Slim Cognito: Acid Bomb Acid Burn Mod - 30,000"
    CHALLAX_ACID_EPOXY = "Challax: Slim Cognito: Acid Bomb Epoxy Mod - 50,000"
    CHALLAX_CONCUSSION_LOCK = "Challax: Slim Cognito: Concussion Gun Lock On Mod - 5,000"
    CHALLAX_CONCUSSION_CHARGE = "Challax: Slim Cognito: Concussion Gun Charge Up Mod - 50,000"
    CHALLAX_BEE_WORKER = "Challax: Slim Cognito: Bee Mine Glove Worker Mod - 5,000"

    QUODRONA_AGENTS_LAUNCHER = "Quodrona: Slim Cognito: Agents of Doom Launcher Mod - 20,000"
    QUODRONA_SCORCHER_SPITFIRE = "Quodrona: Slim Cognito: Scorcher Spitfire Mod - 15,000"
    QUODRONA_SNIPER_SPLIT = "Quodrona: Slim Cognito: Sniper Mine Split Beam Mod - 25,000"
    QUODRONA_SHOCK_LOCK = "Quodrona: Slim Cognito: Shock Rocket Lock On Mod - 5,000"
    QUODRONA_SHOCK_AFTER = "Quodrona: Slim Cognito: Shock Rocket After Shock Mod - 25,000"

    KALIDON_AGENTS_EXPLOSIVE = "Kalidon: Slim Cognito: Agents of Doom Explosive Mod - 450,000"
    KALIDON_SCORCHER_SUNFLARE = "Kalidon: Slim Cognito: Scorcher Sunflare Mod - 200,000"
    KALIDON_SUCK_CANNON_BOUNCE = "Kalidon: Slim Cognito: Suck Cannon Bounce Mod - 600,000"
    KALIDON_BEE_HIVE_BOMB = "Kalidon: Slim Cognito: Bee Mine Glove Hive Bomb Mod - 300,000"
    CHALLAX_SNIPER_SMART_REFLECTOR = "Challax: Slim Cognito: Sniper Mine Smart Reflector Mod - 750,000"
    CHALLAX_SHOCK_MULTI_LAUNCHER = "Challax: Slim Cognito: Shock Rocket Multi Launcher Mod - 2,000,000"
    KALIDON_STATIC_REFLECTION = "Kalidon: Slim Cognito: Static Barrier Reflection Mod - 250,000"
    QUODRONA_STATIC_MIRAGE = "Quodrona: Slim Cognito: Static Barrier Mirage Mod - 1,250,000"
    CHALLAX_LASER_PIERCE = "Challax: Slim Cognito: Laser Tracer Pierce Mod - 1,250,000"
    QUODRONA_LASER_RICOCHET = "Quodrona: Slim Cognito: Laser Tracer Ricochet Mod - 500,000"


class Rac5TitanVendorLocations:
    """String constants for Titan variant purchase locations (Challenge Mode
    1+ only). Buying a weapon's Titan variant floors its level at 5 and opens
    up leveling to 8. RYNO has no Titan variant."""

    POKITARU_LACERATOR_TITAN = "Pokitaru: Gadgetron Vendor: Lacerator Titan - 250,000"
    POKITARU_ACID_TITAN = "Pokitaru: Gadgetron Vendor: Acid Bomb Glove Titan - 250,000"
    POKITARU_CONCUSSION_TITAN = "Pokitaru: Gadgetron Vendor: Concussion Gun Titan - 250,000"
    RYLLUS_AGENTS_TITAN = "Ryllus: Gadgetron Vendor: Agents of Doom Titan - 250,000"
    KALIDON_SCORCHER_TITAN = "Kalidon: Gadgetron Vendor: Scorcher Titan - 250,000"
    DREAMTIME_SUCK_TITAN = "Dreamtime: Gadgetron Vendor: Suck Cannon Titan - 300,000"
    OUTPOST_OMEGA_BEE_TITAN = "Outpost Omega: Gadgetron Vendor: Bee Mine Glove Titan - 250,000"
    CHALLAX_SNIPER_TITAN = "Challax: Gadgetron Vendor: Sniper Mine Titan - 500,000"
    DAYNI_MOON_MOOTATOR_TITAN = "Dayni Moon: Gadgetron Vendor: Mootator Titan - 1,500,000"
    DAYNI_MOON_SHOCK_TITAN = "Dayni Moon: Gadgetron Vendor: Shock Rocket Titan - 1,250,000"
    INSIDE_CLANK_STATIC_TITAN = "Inside Clank: Gadgetron Vendor: Static Barrier Titan - 2,500,000"
    QUODRONA_LASER_TITAN = "Quodrona: Gadgetron Vendor: Laser Tracer Titan - 250,000"

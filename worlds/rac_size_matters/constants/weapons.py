"""String constants for weapons and weapon mods."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5Weapons:
    """String constants for weapons"""

    LACERATOR = "Lacerator"
    CONCUSSION_GUN = "Concussion Gun"
    ACID_BOMB_GLOVE = "Acid Bomb Glove"
    AGENTS_OF_DOOM = "Agents of Doom"
    BEE_MINE_GLOVE = "Bee Mine Glove"
    STATIC_BARRIER = "Static Barrier"
    SHOCK_ROCKET = "Shock Rocket"
    SNIPER_MINE = "Sniper Mine"
    LASER_TRACER = "Laser Tracer"
    SCORCHER = "Scorcher"
    SUCK_CANNON = "Suck Cannon"
    MOOTATOR = "Mootator"
    RYNO = "RYNO"


@dataclass(frozen=True)
class Rac5ProgressiveWeapons:
    """String constants for progressive weapons"""

    LACERATOR = "Progressive Lacerator"
    CONCUSSION_GUN = "Progressive Concussion Gun"
    ACID_BOMB_GLOVE = "Progressive Acid Bomb Glove"
    AGENTS_OF_DOOM = "Progressive Agents of Doom"
    BEE_MINE_GLOVE = "Progressive Bee Mine Glove"
    STATIC_BARRIER = "Progressive Static Barrier"
    SHOCK_ROCKET = "Progressive Shock Rocket"
    SNIPER_MINE = "Progressive Sniper Mine"
    LASER_TRACER = "Progressive Laser Tracer"
    SCORCHER = "Progressive Scorcher"
    SUCK_CANNON = "Progressive Suck Cannon"
    MOOTATOR = "Progressive Mootator"
    RYNO = "Progressive RYNO"


@dataclass(frozen=True)
class Rac5WeaponMods:
    """String constants for weapon mods"""

    LACERATOR_MOD_LOCK_ON = "Lacerator: Lock On Mod"
    LACERATOR_MOD_DOUBLE_BARREL = "Lacerator: Double Barrel Mod"
    CONCUSSION_GUN_MOD_SPLIT_BARREL = "Concussion Gun: Wide Barrel Mod"
    CONCUSSION_GUN_MOD_LOCK_ON = "Concussion Gun: Lock On Mod"
    CONCUSSION_GUN_MOD_CHARGE_UP = "Concussion Gun: Charge Up Mod"
    ACID_BOMB_GLOVE_MOD_ACID_BOMB = "Acid Bomb Glove: Acid Bomb Mod"
    ACID_BOMB_GLOVE_MOD_EPOXY = "Acid Bomb Glove: Epoxy Mod"
    AGENTS_OF_DOOM_MOD_LAUNCHER = "Agents of Doom: Launcher Mod"
    AGENTS_OF_DOOM_MOD_EXPLOSIVE = "Agents of Doom: Explosive Mod"
    BEE_MINE_GLOVE_MOD_WORKER = "Bee Mine Glove: Worker Mod"
    BEE_MINE_GLOVE_MOD_HIVE_BOMB = "Bee Mine Glove: Hive Bomb Mod"
    STATIC_BARRIER_MOD_REFLECTION = "Static Barrier: Reflection Mod"
    STATIC_BARRIER_MOD_MIRAGE = "Static Barrier: Mirage Mod"
    SHOCK_ROCKET_MOD_LOCK_ON = "Shock Rocket: Lock On Mod"
    SHOCK_ROCKET_MOD_AFTER_SHOCK = "Shock Rocket: After Shock Mod"
    SHOCK_ROCKET_MOD_MULTI_LAUNCHER = "Shock Rocket: Multi Launcher Mod"
    SNIPER_MINE_MOD_SPLIT_BEAM = "Sniper Mine: Split Beam Mod"
    SNIPER_MINE_MOD_SMART_REFLECTOR = "Sniper Mine: Smart Reflector Mod"
    SCORCHER_MOD_SPLIT_FIRE = "Scorcher: Split Fire Mod"
    SCORCHER_MOD_SUNFLARE = "Scorcher: Sunflare Mod"
    LASER_TRACER_MOD_PIERCE = "Laser Tracer: Pierce Mod"
    LASER_TRACER_MOD_RICOCHET = "Laser Tracer: Ricochet Mod"
    SUCK_CANNON_MOD_BOUNCE = "Suck Cannon: Bounce Mod"


@dataclass(frozen=True)
class Rac5ProgressiveWeaponMods:
    """String constants for progressive weapon mods"""

    LACERATOR = "Progressive Lacerator Mod"
    CONCUSSION_GUN = "Progressive Concussion Gun Mod"
    ACID_BOMB_GLOVE = "Progressive Acid Bomb Glove Mod"
    AGENTS_OF_DOOM = "Progressive Agents of Doom Mod"
    BEE_MINE_GLOVE = "Progressive Bee Mine Glove Mod"
    STATIC_BARRIER = "Progressive Static Barrier Mod"
    SHOCK_ROCKET = "Progressive Shock Rocket Mod"
    SNIPER_MINE = "Progressive Sniper Mine Mod"
    SCORCHER = "Progressive Scorcher Mod"
    LASER_TRACER = "Progressive Laser Tracer Mod"
    SUCK_CANNON = "Progressive Suck Cannon Mod"

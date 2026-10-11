"""This module provides a class with all the string constants used for Weapon Level location names."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5WeaponLevels:
    """Constant strings for each Weapon Level location name — one location per
    weapon per level (2-4; level 1 is synonymous with owning the weapon at
    all, so it isn't modelled as its own location).

    Levels 5-8 (Challenge Mode only, see Rac5TitanVendorLocations) exist for
    every weapon except RYNO, which has no Titan variant and stays capped
    at level 4."""

    LACERATOR_LEVEL_2 = "Weapon Level: Lacerator V2"
    LACERATOR_LEVEL_3 = "Weapon Level: Lacerator V3"
    LACERATOR_LEVEL_4 = "Weapon Level: Lacerator V4"
    LACERATOR_LEVEL_5 = "Weapon Level: Lacerator V5"
    LACERATOR_LEVEL_6 = "Weapon Level: Lacerator V6"
    LACERATOR_LEVEL_7 = "Weapon Level: Lacerator V7"
    LACERATOR_LEVEL_8 = "Weapon Level: Lacerator V8"

    CONCUSSION_GUN_LEVEL_2 = "Weapon Level: Concussion Gun V2"
    CONCUSSION_GUN_LEVEL_3 = "Weapon Level: Concussion Gun V3"
    CONCUSSION_GUN_LEVEL_4 = "Weapon Level: Concussion Gun V4"
    CONCUSSION_GUN_LEVEL_5 = "Weapon Level: Concussion Gun V5"
    CONCUSSION_GUN_LEVEL_6 = "Weapon Level: Concussion Gun V6"
    CONCUSSION_GUN_LEVEL_7 = "Weapon Level: Concussion Gun V7"
    CONCUSSION_GUN_LEVEL_8 = "Weapon Level: Concussion Gun V8"

    ACID_BOMB_GLOVE_LEVEL_2 = "Weapon Level: Acid Bomb Glove V2"
    ACID_BOMB_GLOVE_LEVEL_3 = "Weapon Level: Acid Bomb Glove V3"
    ACID_BOMB_GLOVE_LEVEL_4 = "Weapon Level: Acid Bomb Glove V4"
    ACID_BOMB_GLOVE_LEVEL_5 = "Weapon Level: Acid Bomb Glove V5"
    ACID_BOMB_GLOVE_LEVEL_6 = "Weapon Level: Acid Bomb Glove V6"
    ACID_BOMB_GLOVE_LEVEL_7 = "Weapon Level: Acid Bomb Glove V7"
    ACID_BOMB_GLOVE_LEVEL_8 = "Weapon Level: Acid Bomb Glove V8"

    AGENTS_OF_DOOM_LEVEL_2 = "Weapon Level: Agents of Doom V2"
    AGENTS_OF_DOOM_LEVEL_3 = "Weapon Level: Agents of Doom V3"
    AGENTS_OF_DOOM_LEVEL_4 = "Weapon Level: Agents of Doom V4"
    AGENTS_OF_DOOM_LEVEL_5 = "Weapon Level: Agents of Doom V5"
    AGENTS_OF_DOOM_LEVEL_6 = "Weapon Level: Agents of Doom V6"
    AGENTS_OF_DOOM_LEVEL_7 = "Weapon Level: Agents of Doom V7"
    AGENTS_OF_DOOM_LEVEL_8 = "Weapon Level: Agents of Doom V8"

    BEE_MINE_GLOVE_LEVEL_2 = "Weapon Level: Bee Mine Glove V2"
    BEE_MINE_GLOVE_LEVEL_3 = "Weapon Level: Bee Mine Glove V3"
    BEE_MINE_GLOVE_LEVEL_4 = "Weapon Level: Bee Mine Glove V4"
    BEE_MINE_GLOVE_LEVEL_5 = "Weapon Level: Bee Mine Glove V5"
    BEE_MINE_GLOVE_LEVEL_6 = "Weapon Level: Bee Mine Glove V6"
    BEE_MINE_GLOVE_LEVEL_7 = "Weapon Level: Bee Mine Glove V7"
    BEE_MINE_GLOVE_LEVEL_8 = "Weapon Level: Bee Mine Glove V8"

    STATIC_BARRIER_LEVEL_2 = "Weapon Level: Static Barrier V2"
    STATIC_BARRIER_LEVEL_3 = "Weapon Level: Static Barrier V3"
    STATIC_BARRIER_LEVEL_4 = "Weapon Level: Static Barrier V4"
    STATIC_BARRIER_LEVEL_5 = "Weapon Level: Static Barrier V5"
    STATIC_BARRIER_LEVEL_6 = "Weapon Level: Static Barrier V6"
    STATIC_BARRIER_LEVEL_7 = "Weapon Level: Static Barrier V7"
    STATIC_BARRIER_LEVEL_8 = "Weapon Level: Static Barrier V8"

    SHOCK_ROCKET_LEVEL_2 = "Weapon Level: Shock Rocket V2"
    SHOCK_ROCKET_LEVEL_3 = "Weapon Level: Shock Rocket V3"
    SHOCK_ROCKET_LEVEL_4 = "Weapon Level: Shock Rocket V4"
    SHOCK_ROCKET_LEVEL_5 = "Weapon Level: Shock Rocket V5"
    SHOCK_ROCKET_LEVEL_6 = "Weapon Level: Shock Rocket V6"
    SHOCK_ROCKET_LEVEL_7 = "Weapon Level: Shock Rocket V7"
    SHOCK_ROCKET_LEVEL_8 = "Weapon Level: Shock Rocket V8"

    SNIPER_MINE_LEVEL_2 = "Weapon Level: Sniper Mine V2"
    SNIPER_MINE_LEVEL_3 = "Weapon Level: Sniper Mine V3"
    SNIPER_MINE_LEVEL_4 = "Weapon Level: Sniper Mine V4"
    SNIPER_MINE_LEVEL_5 = "Weapon Level: Sniper Mine V5"
    SNIPER_MINE_LEVEL_6 = "Weapon Level: Sniper Mine V6"
    SNIPER_MINE_LEVEL_7 = "Weapon Level: Sniper Mine V7"
    SNIPER_MINE_LEVEL_8 = "Weapon Level: Sniper Mine V8"

    LASER_TRACER_LEVEL_2 = "Weapon Level: Laser Tracer V2"
    LASER_TRACER_LEVEL_3 = "Weapon Level: Laser Tracer V3"
    LASER_TRACER_LEVEL_4 = "Weapon Level: Laser Tracer V4"
    LASER_TRACER_LEVEL_5 = "Weapon Level: Laser Tracer V5"
    LASER_TRACER_LEVEL_6 = "Weapon Level: Laser Tracer V6"
    LASER_TRACER_LEVEL_7 = "Weapon Level: Laser Tracer V7"
    LASER_TRACER_LEVEL_8 = "Weapon Level: Laser Tracer V8"

    SCORCHER_LEVEL_2 = "Weapon Level: Scorcher V2"
    SCORCHER_LEVEL_3 = "Weapon Level: Scorcher V3"
    SCORCHER_LEVEL_4 = "Weapon Level: Scorcher V4"
    SCORCHER_LEVEL_5 = "Weapon Level: Scorcher V5"
    SCORCHER_LEVEL_6 = "Weapon Level: Scorcher V6"
    SCORCHER_LEVEL_7 = "Weapon Level: Scorcher V7"
    SCORCHER_LEVEL_8 = "Weapon Level: Scorcher V8"

    SUCK_CANNON_LEVEL_2 = "Weapon Level: Suck Cannon V2"
    SUCK_CANNON_LEVEL_3 = "Weapon Level: Suck Cannon V3"
    SUCK_CANNON_LEVEL_4 = "Weapon Level: Suck Cannon V4"
    SUCK_CANNON_LEVEL_5 = "Weapon Level: Suck Cannon V5"
    SUCK_CANNON_LEVEL_6 = "Weapon Level: Suck Cannon V6"
    SUCK_CANNON_LEVEL_7 = "Weapon Level: Suck Cannon V7"
    SUCK_CANNON_LEVEL_8 = "Weapon Level: Suck Cannon V8"

    MOOTATOR_LEVEL_2 = "Weapon Level: Mootator V2"
    MOOTATOR_LEVEL_3 = "Weapon Level: Mootator V3"
    MOOTATOR_LEVEL_4 = "Weapon Level: Mootator V4"
    MOOTATOR_LEVEL_5 = "Weapon Level: Mootator V5"
    MOOTATOR_LEVEL_6 = "Weapon Level: Mootator V6"
    MOOTATOR_LEVEL_7 = "Weapon Level: Mootator V7"
    MOOTATOR_LEVEL_8 = "Weapon Level: Mootator V8"

    RYNO_LEVEL_2 = "Weapon Level: RYNO V2"
    RYNO_LEVEL_3 = "Weapon Level: RYNO V3"
    RYNO_LEVEL_4 = "Weapon Level: RYNO V4"

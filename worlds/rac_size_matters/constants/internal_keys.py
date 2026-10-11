"""String constants for the game's internal weapon/gadget identifiers.

These match the lowercase snake_case names used to address memory structs
(see core/weapons.py WEAPON_ORDER/GADGET_ORDER) and are distinct from the
player-facing display names in Rac5Items. Kept import-free so both
core/weapons.py and items.py can depend on it without a circular import.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Rac5WeaponKeys:
    LACERATOR = "lacerator"
    CONCUSSION_GUN = "concussion_gun"
    ACID_BOMB_GLOVE = "acid_bomb_glove"
    AGENTS_OF_DOOM = "agents_of_doom"
    BEE_MINE_GLOVE = "bee_mine_glove"
    STATIC_BARRIER = "static_barrier"
    SHOCK_ROCKET = "shock_rocket"
    SNIPER_MINE = "sniper_mine"
    SCORCHER = "scorcher"
    LASER_TRACER = "laser_tracer"
    SUCK_CANNON = "suck_cannon"
    MOOTATOR = "mootator"
    RYNO = "ryno"


@dataclass(frozen=True)
class Rac5GadgetKeys:
    HYPERSHOT = "hypershot"
    SPROUT_O_MATIC = "sprout_o_matic"
    POLARIZER = "polarizer"
    PDA = "pda"
    SHRINK_RAY = "shrink_ray"
    BOLT_GRABBER = "bolt_grabber"
    MAP_O_MATIC = "map_o_matic"
    BOX_BREAKER = "box_breaker"

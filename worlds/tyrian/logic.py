# Archipelago MultiWorld integration for Tyrian
#
# This file is copyright (C) Kay "Kaito" Sinclaire,
# and is released under the terms of the zlib license.
# See "LICENSE" for more details.

from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, lru_cache
from itertools import product
from typing import TYPE_CHECKING, cast

from BaseClasses import LocationProgressType as LPType

from worlds.generic.Rules import add_rule

from .options import LogicDifficulty
from .twiddles import SpecialValues

if TYPE_CHECKING:
    from BaseClasses import CollectionState

    from . import TyrianWorld


@dataclass(frozen=True)
class DPS:
    active: float = 0.0
    passive: float = 0.0
    sideways: float = 0.0
    piercing: float = 0.0

    @cached_property
    def _type_active(self):
        return self.active > 0.0

    @cached_property
    def _type_passive(self):
        return self.passive > 0.0

    @cached_property
    def _type_sideways(self):
        return self.sideways > 0.0

    @cached_property
    def _type_piercing(self):
        return self.piercing > 0.0

    def __sub__(self, other: "DPS") -> "DPS":
        return DPS(
            self.active - other.active,
            self.passive - other.passive,
            self.sideways - other.sideways,
            self.piercing - other.piercing
        )

    def meets_requirements(self, requirements: "DPS") -> tuple[bool, float]:
        distance = 0.0

        # Apply some weighting to distance
        # Rear weapons can easily take care of passive and sideways requirements
        # But active is much harder, and piercing is entirely impossible
        if requirements._type_piercing and self.piercing < requirements.piercing:
            return (False, 99999.0)
        if requirements._type_active and self.active < requirements.active:
            distance += (requirements.active - self.active) * 4.0
        if requirements._type_passive and self.passive < requirements.passive:
            distance += (requirements.passive - self.passive) * 0.8
        if requirements._type_sideways and self.sideways < requirements.sideways:
            distance += (requirements.sideways - self.sideways) * 1.8

        return ((distance < 0.0001), distance)

    # As above, but doesn't check for distance and early-outs on failure.
    def fast_meets_requirements(self, requirements: "DPS") -> bool:
        return (
              not (requirements._type_active and self.active < requirements.active)
              and not (requirements._type_passive and self.passive < requirements.passive)
              and not (requirements._type_sideways and self.sideways < requirements.sideways)
              and not (requirements._type_piercing and self.piercing < requirements.piercing)
        )


class DamageTables:
    # Local versions, used when instantiated, holds all rules for a given logic difficulty merged together
    local_power_provided: list[int]
    local_weapon_dps: dict[str, list[DPS]]

    # Multiplier for all target values, based on options.logic_difficulty
    logic_difficulty_multiplier: float

    # ================================================================================================================
    # Maximum amount of generator power use we expect for each logic difficulty
    generator_power_provided: dict[int, list[int]] = {
        # Difficulty --------------Power  Non MR9 M12 C12 SMF AMF GPW
        LogicDifficulty.option_beginner: [  0,  9, 12, 16, 21, 25, 41],  # -1, -2, -3, -4, -5, -9 (for shield recharge)
        LogicDifficulty.option_standard: [  0, 10, 14, 19, 25, 30, 50],  # Base power levels of each generator
        LogicDifficulty.option_expert:   [  0, 11, 16, 21, 28, 33, 55],  # +1, +2, +2, +3, +3, +5
        LogicDifficulty.option_master:   [  0, 12, 17, 23, 30, 35, 58],  # +2, +3, +4, +5, +5, +8
        LogicDifficulty.option_no_logic: [ 99, 99, 99, 99, 99, 99, 99],
    }

    # ================================================================================================================
    # Generator break-even points (demand == production)
    # For reference: Basic shield break-even point is 9 power
    generator_power_required: dict[str, list[int]] = {
        # Front Weapons ----------- Power  --1- --2- --3- --4- --5- --6- --7- --8- --9- -10- -11-
        "Pulse-Cannon":                   [  8,   6,   6,   6,   5,   5,   5,   5,   5,   5,   5],
        "Multi-Cannon (Front)":           [ 10,  10,   8,   8,   7,   7,   7,   7,   7,   7,   7],
        "Mega Cannon":                    [ 13,  13,  13,  13,  13,  13,  13,  13,  13,  13,  13],
        "Laser":                          [ 20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20],
        "Zica Laser":                     [  9,  10,  10,  11,  11,  11,  11,  13,  13,  11,  11],
        "Protron Z":                      [ 14,  12,  14,  14,  12,  14,  14,  14,  14,  14,  14],
        "Vulcan Cannon (Front)":          [ 10,  10,  10,  10,  10,  10,   7,   7,   7,  10,  20],
        "Lightning Cannon":               [ 12,  12,  12,  12,  12,  12,  12,  12,  12,  23,  35],
        "Protron (Front)":                [ 10,   8,   8,   7,   7,   7,   7,   7,   7,   7,   7],
        "Missile Launcher":               [  6,   5,   5,   4,   4,   4,   4,   4,   4,   4,   4],
        "Mega Pulse (Front)":             [ 15,  20,  12,  15,  20,  10,  10,  10,  10,  10,  10],
        "Heavy Missile Launcher (Front)": [ 10,  13,  18,   8,  10,  13,  18,  15,  13,  11,   9],
        "Banana Blast (Front)":           [  3,   3,   4,   4,   4,   5,   4,   4,   3,   4,   5],
        "HotDog (Front)":                 [ 10,  13,   8,  10,   8,  10,   8,   7,   7,   6,   6],
        "Hyper Pulse":                    [ 17,  12,  17,  12,  17,  17,  12,  12,  10,  10,  12],
        "Shuriken Field":                 [ 14,  14,  14,  14,  14,  14,  14,  14,  14,  14,  14],
        "Poison Bomb":                    [  9,  11,  13,  13,  17,  17,  20,  15,  20,  20,  20],
        "Protron Wave":                   [  8,   5,   6,   6,   6,   6,   6,   6,   6,   6,   6],
        "Guided Bombs":                   [  8,  10,  12,  10,   6,   6,   6,   8,   4,   4,   4],
        "The Orange Juicer":              [  6,   7,   7,   7,   7,   5,   5,   6,   7,   6,   6],
        "NortShip Super Pulse":           [ 12,  12,  12,  12,  12,  12,  12,  12,  12,  12,  12],
        "Atomic RailGun":                 [ 25,  25,  25,  25,  25,  25,  25,  25,  25,  25,  25],
        "Widget Beam":                    [ 13,  13,  10,  10,  10,  10,  10,  10,  10,  10,  10],
        "Sonic Impulse":                  [ 12,  17,  12,  12,  12,  17,  12,  12,  12,  12,  12],
        "RetroBall":                      [ 10,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10],
        "Needle Laser":                   [  6,   7,   7,   6,   6,   6,   6,   6,   6,   6,   6],
        "Pretzel Missile":                [  8,   8,   8,   8,   8,   8,   8,   8,   8,   8,   8],
        "Dragon Frost":                   [  6,   5,   4,   4,   4,   4,   3,   3,   3,   3,   2],
        "Dragon Flame":                   [  8,   8,  10,   7,  10,   7,   8,  10,   5,   7,   4],
        # Rear Weapons ------------ Power  --1- --2- --3- --4- --5- --6- --7- --8- --9- -10- -11-
        "Starburst":                      [  7,   7,  10,  10,   7,   7,  10,  10,   7,   5,   7],
        "Multi-Cannon (Rear)":            [  8,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6],
        "Sonic Wave":                     [  7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7],
        "Protron (Rear)":                 [  6,   6,   6,   6,   6,   6,   6,   6,   6,   6,   6],
        "Wild Ball":                      [  7,   7,   7,   7,   7,   7,   7,   7,   7,   7,   7],
        "Vulcan Cannon (Rear)":           [  7,   7,   5,   5,   7,   7,  10,   7,   7,   7,  10],
        "Fireball":                       [  4,   4,   4,   4,   4,   4,   4,   4,   4,   4,   4],
        "Heavy Missile Launcher (Rear)":  [ 10,  13,  10,  11,  10,  13,  11,  13,  15,  13,  15],
        "Mega Pulse (Rear)":              [ 30,  22,  17,  15,  13,  13,  13,  13,  13,  13,  13],
        "Banana Blast (Rear)":            [  4,   4,   4,   4,   4,   1,   1,   1,   1,   1,   1],
        "HotDog (Rear)":                  [ 13,  10,  10,  10,  10,   8,   8,   8,   7,   6,   6],
        "Guided Micro Bombs":             [  4,   5,   5,   5,   5,   5,   5,   6,   6,   6,   6],
        "Heavy Guided Bombs":             [  4,   4,   4,   4,   4,   4,   4,   4,   4,   5,   4],
        "Scatter Wave":                   [  8,   8,   7,   7,   7,   7,   7,   7,   7,   7,   7],
        "NortShip Spreader":              [ 12,  12,  12,  12,  12,  12,  12,  12,  12,  12,  12],
        "NortShip Spreader B":            [ 15,  10,  10,  10,  10,  10,  10,  10,  10,  10,  10],
        "People Pretzels":                [  6,   7,   8,  10,  10,   7,   5,   4,   4,   3,   3],
    }

    # ================================================================================================================
    # Damage focused on single direct target
    base_active: dict[int, dict[str, list[float]]] = {
        # Base level: Assumes a reasonable distance kept from enemy, and directly below (or only a slight adjustment)
        LogicDifficulty.option_beginner: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Pulse-Cannon":                   [10.6, 12.6, 16.8, 16.8, 17.5, 21.1, 21.1, 24.5,  27.3,  27.3,  32.1],
            "Multi-Cannon (Front)":           [10.6,    0,  4.7,  9.3,  3.8,  7.8,  3.8,  7.8,   3.8,   7.8,   7.8],
            "Mega Cannon":                    [ 5.3,  5.3, 10.0,  5.3, 10.0, 10.0, 10.0, 10.2,  21.1,  21.1,  21.2],
            "Laser":                          [ 7.8, 15.5, 23.3, 23.5, 35.0, 46.5, 46.8, 58.3,  81.6,  93.3, 140.0],
            "Zica Laser":                     [16.3, 23.4, 28.8, 38.2, 49.0, 52.0, 17.1, 53.3,  73.3, 110.0, 127.5],
            "Protron Z":                      [14.0, 19.0, 14.0, 23.3, 23.5, 37.3, 46.7, 60.7,  37.3,  37.3,  37.3],
            "Vulcan Cannon (Front)":          [11.7,  8.8,  5.8,  9.8,  5.7,  5.7,  7.8, 13.0,   7.8,  11.7,  23.3],
            "Lightning Cannon":               [11.5, 15.5, 19.5, 19.5, 15.5, 15.5, 23.0, 23.0,  23.0,  46.7,  93.3],
            "Protron (Front)":                [ 9.3,  7.8,  7.8,  3.3,  6.7, 13.3,  6.7, 13.3,  13.3,  10.0,  23.3],
            "Missile Launcher":               [ 5.1,  5.1,  8.4, 11.7, 14.9, 14.1, 14.1, 16.6,  30.0,  32.0,  15.0],
            "Mega Pulse (Front)":             [12.0, 15.6, 18.7, 23.2, 31.0, 19.5, 31.0, 23.0,  23.0,  31.0,  54.8],
            "Heavy Missile Launcher (Front)": [10.4, 13.3, 18.7,  8.7, 10.4, 33.3, 46.7, 22.8,  40.0,  46.0,  37.3],
            "Banana Blast (Front)":           [ 7.8,  7.8,  9.3,  6.2, 14.0,  5.6,  9.3, 14.0,  15.8,  18.7,  23.5],
            "HotDog (Front)":                 [11.6, 15.6, 18.7, 23.4, 28.0, 35.2, 28.0, 23.3,  23.8,  20.0,  26.7],
            "Hyper Pulse":                    [ 7.8,  5.8,  7.8, 11.8, 15.4, 23.3, 17.5, 23.3,  14.0,  18.7,  17.5],
            "Shuriken Field":                 [ 9.3,  9.3,  9.3,  9.3,  9.3,  9.3,  9.3,  9.3,  18.7,  18.7,  37.3],
            "Poison Bomb":                    [14.2, 17.2, 20.6, 20.6, 26.7, 26.7, 23.6, 37.4,  38.0,  58.0,  90.5],
            "Protron Wave":                   [ 4.7,  5.9,  6.7,  6.7,  6.7,  6.7, 13.3, 13.3,  13.3,  13.3,  13.3],
            "Guided Bombs":                   [10.5,  6.7,  5.3, 13.3, 13.3, 11.0,  7.8,  7.8,  15.0,  10.0,  15.0],
            "The Orange Juicer":              [   0,  7.4,  7.4, 14.8, 14.8,  9.0,  9.0,  9.0,   9.0,   9.0,   9.0],
            "NortShip Super Pulse":           [ 5.9, 11.6, 11.6, 17.6, 23.2, 28.0,  8.6,  8.6,  28.9,  14.5,  76.0],
            "Atomic RailGun":                 [17.5, 35.0, 52.5, 70.0, 81.5, 82.0, 93.6, 99.0, 105.0, 140.0, 140.0],
            "Widget Beam":                    [ 7.8, 15.3, 11.7, 17.4, 11.7, 17.4, 11.8, 11.8,  11.8,  11.8,  17.5],
            "Sonic Impulse":                  [11.6,  7.6, 11.6, 17.5, 23.2, 10.2, 11.6, 11.5,  11.8,  11.6,  11.8],
            "RetroBall":                      [ 9.3,  4.7,  4.7,  9.3,  4.7,  4.7,  9.3,  9.3,   9.3,   9.3,   9.3],
            "Needle Laser":                   [ 5.7, 10.0,  6.7, 10.5, 11.7, 11.7, 17.5, 20.5,  29.4,  17.5,  23.4],
            "Pretzel Missile":                [ 7.8, 11.7, 15.6, 11.7, 11.7, 11.7, 23.7, 23.7,  31.2,  35.1,  35.1],
            "Dragon Frost":                   [ 8.8,    0,  5.8,  9.2,  5.0,  7.5,  7.5,  7.5,   9.7,   9.5,   9.3],
            "Dragon Flame":                   [ 7.7,  7.7,  9.3, 10.0,  9.3, 16.7, 19.8, 23.3,  36.4,  46.7,  22.8],
            # Rear Weapons ------------ Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Sonic Wave":                     [ 6.7, 10.0,  6.7,  6.7,  6.7, 20.0, 20.0, 20.0,  20.0,  20.0,  20.0],
            "Wild Ball":                      [ 5.0,  5.0,  5.0,  7.5,  7.5,  7.5,    0,  5.0,     0,  18.2,  18.2],
            "Fireball":                       [ 3.0,  6.0,    0,    0,  4.0,  8.0,  6.7,  8.0,  15.2,  15.2,  15.2],
            "Mega Pulse (Rear)":              [   0,    0,    0,    0,    0,    0,  6.7,    0,     0,     0,  40.0],
            "Banana Blast (Rear)":            [   0,    0,    0,    0,    0, 35.0, 35.0, 25.0,  25.0,  35.0,  45.0],
            "HotDog (Rear)":                  [   0,    0,    0,    0,    0,    0,    0,    0,     0,   6.7,     0],
            "Scatter Wave":                   [   0,    0,    0,  3.8,  3.8,  1.9,    0,  3.8,   7.5,     0,     0],
            "NortShip Spreader B":            [   0,    0,    0,    0,    0,    0,    0,  2.3,     0,   2.3,   2.3],
            "People Pretzels":                [   0,  3.5,  2.5,  1.8,  1.8,  2.5,  3.2,  3.4,   5.5,   4.5,   3.8],
        },

        # Expert level: Assumes getting up closer to an enemy so more bullets can hit
        LogicDifficulty.option_expert: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Mega Cannon":                    [ 7.8, 15.2, 14.1,  7.8, 15.2, 16.0, 16.0, 16.0,  26.0,  26.0,  26.0],
            "Zica Laser":                     [16.3, 23.4, 28.8, 38.2, 49.0, 52.0, 56.4, 96.7, 106.7, 110.0, 127.5],
            "Protron Z":                      [14.0, 19.0, 14.0, 23.3, 23.5, 37.3, 46.7, 60.7,  51.3,  60.7,  37.3],
            "Vulcan Cannon (Front)":          [11.7, 11.7, 11.7, 11.7, 10.2, 10.2, 15.6, 15.6,  13.7,  20.0,  40.0],
            "Protron (Front)":                [ 9.3, 11.5, 11.5, 10.0, 13.3, 13.3, 20.0, 33.3,  33.3,  26.7,  43.3],
            "Banana Blast (Front)":           [ 7.8, 15.6, 14.0,  9.3, 28.0, 11.8, 18.7, 28.0,  31.2,  37.3,  47.0],
            "Hyper Pulse":                    [ 7.8, 11.6, 15.6, 17.5, 23.5, 31.1, 29.2, 35.0,  23.3,  28.0,  29.0],
            "Protron Wave":                   [ 4.7,  5.9,  6.7,  6.7,  6.7,  6.7, 13.3, 13.3,  13.3,  20.0,  26.7],
            "Guided Bombs":                   [10.7, 13.3, 10.4, 26.7, 18.2, 13.0, 11.0, 11.0,  17.3,  12.0,  19.3],
            "The Orange Juicer":              [ 9.4,  9.4,  9.4, 18.8, 18.8, 17.0, 17.0, 20.0,  23.0,  30.0,  40.0],
            "Widget Beam":                    [ 7.8, 15.3, 11.7, 17.4, 11.7, 17.4, 17.4, 11.8,  11.8,  17.4,  17.5],
            "Sonic Impulse":                  [11.6, 10.5, 29.2, 17.5, 23.2, 21.8, 23.1, 23.3,  23.3,  30.0,  30.0],
            "RetroBall":                      [ 9.3,  9.3,  9.3,  9.3,  9.3,  9.3, 14.0, 14.0,  18.7,  18.7,  18.7],
            "Pretzel Missile":                [ 7.8, 11.7, 15.6, 11.7, 15.8, 19.2, 23.7, 27.5,  31.2,  35.1,  35.1],
        },

        # Master level: Assumes abuse of mechanics (e.g.: using mode switch to reset weapon state)
        LogicDifficulty.option_master: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Vulcan Cannon (Front)":          [11.7, 11.7, 11.7, 11.7, 11.7, 11.7, 15.6, 15.6,  15.6,  23.3,  46.7],
            "The Orange Juicer":              [ 9.4, 11.4, 11.4, 22.8, 22.8, 17.0, 17.0, 20.0,  23.0,  30.0,  40.0],
            # Rear Weapons ------------ Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Fireball":                       [ 6.0,  6.0,    0,    0,  8.0,  8.0,  9.3, 11.6,  15.2,  15.2,  15.2],
            "People Pretzels":                [   0,  4.5,  4.0,  2.5,  2.5,  3.5,  3.2,  3.4,   5.5,   4.5,   3.8],
        },
    }

    # ================================================================================================================
    # Damage aimed away from the above single target, used to get a general idea of how defensive a build can be
    base_passive: dict[int, dict[str, list[float]]] = {
        # Base level: Damage to any other area except the above single targeted area
        LogicDifficulty.option_beginner: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Pulse-Cannon":                   [   0,    0,    0,    0,    0,    0,    0,    0,   7.0,  13.9,  13.9],
            "Multi-Cannon (Front)":           [   0, 11.8,  9.3,  9.3, 15.5, 15.5, 24.0, 24.0,  31.5,  31.5,  38.9],
            "Mega Cannon":                    [   0,  6.0,    0,  9.0, 10.0,    0, 13.0, 10.2,     0,  13.0,  20.4],
            "Zica Laser":                     [   0,    0,    0,    0,    0,    0, 39.7, 43.4,  33.3,     0,     0],
            "Protron Z":                      [   0,    0,    0,    0,    0,    0,    0,    0,  28.0,  46.7,  46.7],
            "Vulcan Cannon (Front)":          [   0,  3.3,  3.3,  2.0,  5.8,  2.8,  4.0,  2.8,   4.0,   5.8,  11.6],
            "Lightning Cannon":               [   0,    0,    0,    0, 15.1, 30.2, 15.1, 30.2,  30.2,     0,     0],
            "Protron (Front)":                [   0,  3.8,  7.8, 13.3, 13.3,  6.7, 20.0, 26.6,  30.0,  43.3,  40.0],
            "Missile Launcher":               [   0,  4.5,  4.5,  4.5,    0,  3.3,  7.3,  7.3,     0,   7.3,   9.0],
            "Mega Pulse (Front)":             [   0,    0,    0,    0,    0,  7.2,    0,    0,  11.8,  31.2,  31.2],
            "Heavy Missile Launcher (Front)": [   0,    0,    0,  8.7, 10.4,    0,    0, 18.6,  33.3,  18.0,  43.3],
            "Banana Blast (Front)":           [   0,  7.8,  9.3, 12.7, 14.0, 17.5, 28.0, 41.8,  47.6,  56.0,  69.6],
            "HotDog (Front)":                 [   0,    0,    0,    0,    0,    0, 18.6, 23.3,  23.8,  26.7,  26.7],
            "Hyper Pulse":                    [   0,  5.8,  7.8,  5.8,  7.8,  7.8, 11.7, 11.7,  23.3,  23.3,  34.9],
            "Shuriken Field":                 [   0,  9.3, 18.6, 28.0, 37.3, 46.7, 56.0, 46.7,  46.7,  56.0,  37.3],
            "Poison Bomb":                    [   0,    0,    0, 21.3, 26.7, 53.3, 31.1, 47.8,  62.1,  62.1,  62.1],
            "Protron Wave":                   [   0,    0,    0,  6.7,  6.7, 13.3,  6.7, 13.3,  13.3,  26.7,  33.3],
            "Guided Bombs":                   [   0,  6.7,  9.0, 13.3, 16.0,  8.0, 12.3, 10.3,  12.3,  16.3,  16.3],
            "The Orange Juicer":              [   0,  5.7,  5.7, 11.4, 11.4,  9.0,  9.0, 20.0,  24.0,  40.0,  50.0],
            "NortShip Super Pulse":           [ 5.9,  5.9, 11.6, 11.6, 17.4, 17.5,  5.8,  8.8,  11.8,  33.7,  23.5],
            "Widget Beam":                    [   0,    0,    0,    0,  5.8,    0,  5.8,  5.8,  11.6,  17.0,  17.5],
            "Sonic Impulse":                  [   0,  5.3, 10.6, 12.0, 16.0, 11.2, 15.9, 21.2,  21.2,  45.0,  50.0],
            "RetroBall":                      [   0,  4.7,  9.3,  9.3, 14.0, 18.7, 18.7,  9.3,   9.3,  18.7,  18.7],
            "Needle Laser":                   [   0,    0,    0,    0,    0,    0,    0,    0,     0,   5.8,  11.5],
            "Pretzel Missile":                [   0,    0,    0,    0,  3.8,  7.6,    0,  7.6,   7.6,  15.5,  23.1],
            "Dragon Frost":                   [   0, 14.0, 11.5, 11.2, 16.7, 15.8, 23.1, 27.5,  13.0,  19.0,  30.0],
            "Dragon Flame":                   [   0,    0,    0,    0,    0,    0,    0,    0,     0,     0,  22.8],
            # Rear Weapons ------------ Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Starburst":                      [15.3, 12.0, 22.7, 18.0, 31.3, 23.8, 37.5, 34.8,  47.1,  69.8,  93.3],
            "Multi-Cannon (Rear)":            [ 4.6,  6.7, 13.3, 13.3, 20.0, 20.0, 26.7, 33.3,  46.7,  53.3,  60.0],
            "Sonic Wave":                     [ 6.7,  6.7, 13.0, 13.3, 17.5, 30.0, 43.0, 40.0,  40.0,  40.0,  58.0],
            "Protron (Rear)":                 [ 5.8, 11.6, 11.7, 17.3, 22.8, 28.4, 34.3, 40.9,  46.3,  40.9,  46.3],
            "Wild Ball":                      [   0,  4.9,  9.9,  7.7, 15.4, 20.9, 25.5, 31.4,  31.1,  18.2,  28.6],
            "Vulcan Cannon (Rear)":           [ 7.8,  7.8, 11.5, 11.5, 15.4, 15.4, 23.3, 23.5,  31.2,  31.2,  46.1],
            "Fireball":                       [ 3.0,  6.0, 19.2, 27.2,  4.0,  8.0, 11.8, 15.7,  15.2,  31.1,  39.7],
            "Heavy Missile Launcher (Rear)":  [ 8.1, 10.0, 15.2, 18.1, 30.5, 39.1, 50.7, 61.0, 102.7,  60.0,  79.5],
            "Mega Pulse (Rear)":              [15.6, 23.5, 28.5, 23.8, 40.0, 46.7, 46.7, 40.0,  38.0,  86.7,  86.7],
            "Banana Blast (Rear)":            [18.7, 18.7, 18.7, 18.7, 18.7,    0, 13.3,    0,   9.6,  13.3,  20.0],
            "HotDog (Rear)":                  [15.6, 23.1, 23.1, 23.1, 23.1, 18.7, 18.7, 18.7,  15.5,  13.3,  26.7],
            "Guided Micro Bombs":             [ 2.6,  4.0,  8.6,  8.6, 14.8, 17.3, 30.0, 24.0,  25.0,  26.0,  28.0],
            "Heavy Guided Bombs":             [ 4.6,  4.6,  9.1, 14.0, 17.3, 17.3, 22.5, 20.0,  20.0,  28.0,  36.0],
            "Scatter Wave":                   [ 9.3,  9.3, 15.5,  7.8, 15.5, 23.4, 30.8, 30.8,  30.8,  46.5,  46.5],
            "NortShip Spreader":              [11.7, 11.7, 23.4, 35.1, 46.8, 46.8, 58.5, 70.0, 105.0, 128.4, 128.4],
            "NortShip Spreader B":            [17.8, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6, 24.6,  50.0,  50.0,  50.0],
            "People Pretzels":                [ 8.5,  6.5,  9.5,  8.0,  6.7, 10.2, 11.8, 13.1,  22.0,  21.5,  23.3],
        }
    }

    # ================================================================================================================
    # Damage focused at a 90 degree, or close to 90 degree angle
    base_sideways: dict[int, dict[str, list[float]]] = {
        # Base level: Assumes enough distance to react to enemy movement
        LogicDifficulty.option_beginner: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Protron Wave":                   [   0,    0,    0,  3.3,  3.3,  6.7,  3.3,  6.7,   6.7,   6.7,   3.3],
            "Guided Bombs":                   [   0,    0,  2.7,    0,  5.1,  4.0,  2.1,  2.6,   3.3,   6.7,   6.7],
            "The Orange Juicer":              [10.0,    0,    0,    0,    0,    0,    0,    0,     0,     0,     0],
            # Rear Weapons ------------ Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Starburst":                      [ 7.7,  7.7, 11.8, 11.8, 15.8, 15.8, 23.3, 23.3,  31.2,  35.6,  46.8],
            "Multi-Cannon (Rear)":            [ 2.3,  3.3,  6.7,  6.7, 10.0, 10.0, 13.3, 16.7,  23.3,  26.7,  30.0],
            "Sonic Wave":                     [ 3.3,  3.3,  3.3,  6.7,  6.7, 13.3, 20.0, 20.0,  20.0,  20.0,  20.0],
            "Protron (Rear)":                 [ 2.9,  5.8,  5.8,  8.6, 11.4, 14.2, 17.1, 20.4,  24.1,  20.4,  24.1],
            "Mega Pulse (Rear)":              [ 4.0,  5.8,  9.3,  7.8, 13.3, 16.7, 16.7, 13.3,  10.0,  33.3,  33.3],
            "Banana Blast (Rear)":            [ 9.3,  9.3,  9.3,  9.3,  9.3,    0,  6.7,    0,   4.0,     0,     0],
            "Guided Micro Bombs":             [   0,    0,    0,    0,    0,  4.5,  8.6,  9.3,  18.6,  16.3,  18.6],
            "Heavy Guided Bombs":             [   0,  1.1,  2.3,  5.8,  5.8,  5.8,  8.2,  5.8,   8.2,  13.3,  26.6],
            "Scatter Wave":                   [ 4.7,  4.7,  7.8,  3.9,  7.8, 11.7, 15.4, 15.4,  15.4,  23.3,  23.3],
            "NortShip Spreader":              [   0,    0,  5.8, 11.7, 11.7,    0,  5.8, 17.5,  35.0,     0,     0],
            "People Pretzels":                [   0,    0,  2.5,  2.0,  1.8,  2.7,  3.0,  3.3,   5.5,   4.8,  10.0],
        },

        # Expert level: May need to move in closer to deal damage
        LogicDifficulty.option_expert: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "The Orange Juicer":              [10.0,    0,    0,    0,    0,    0, 14.0, 14.0,  14.0,  28.0,  28.0],
        },

        # Master level: Assumes abuse of mechanics (e.g.: using mode switch to reset weapon state)
        LogicDifficulty.option_master: {
            # Rear Weapons ------------ Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Starburst":                      [10.0, 10.0, 14.3, 14.3, 15.8, 15.8, 23.3, 23.3,  31.2,  35.6,  46.8],
            "Mega Pulse (Rear)":              [ 5.4,  5.8,  9.3,  7.8, 13.3, 16.7, 16.7, 13.3,  10.0,  33.3,  33.3],
            "Heavy Guided Bombs":             [   0,  2.3,  2.3,  5.8,  5.8,  5.8,  8.2,  5.8,   8.2,  13.3,  26.6],
            "People Pretzels":                [   0,    0, 11.7, 13.6, 13.6, 10.0,  7.8,  6.5,   5.5,   4.8,  10.0],
        },
    }

    # ================================================================================================================
    # Similar to active, but assumes that the projectile has already passed through a solid object
    base_piercing: dict[int, dict[str, list[float]]] = {
        LogicDifficulty.option_beginner: {
            # Front Weapons ----------- Power  --1-- --2-- --3-- --4-- --5-- --6-- --7-- --8-- ---9-- --10-- --11--
            "Mega Cannon":                    [ 5.3,  5.3, 10.0,  5.3, 10.0, 10.0, 10.0, 10.2,  21.1,  21.1,  21.2],
            "Sonic Impulse":                  [11.6,  7.6, 11.6, 17.5, 23.2, 10.2, 11.6, 11.5,  11.8,  11.6,  11.8],
            "Needle Laser":                   [ 5.7, 10.0,  6.7, 10.5, 11.7, 11.7, 17.5, 20.5,  29.4,  17.5,  23.4],
            "Dragon Frost":                   [   0,    0,    0,    0,    0,    0,    0,    0,   9.7,   9.5,   9.3],
            "Dragon Flame":                   [   0,    0,    0,    0,    0,    0,    0,    0,  36.4,  46.7,  22.8],
        }
    }

    # ================================================================================================================

    def __init__(self, logic_difficulty: int):
        # Combine every difficulty up to logic_difficulty into one table.
        temp_active = {}
        temp_passive = {}
        temp_sideways = {}
        temp_piercing = {}

        # Default all weapons in all temp tables to 0.0 at all power levels
        # generator_power_required is guaranteed to have every single weapon in it, so we use the keys of it here
        for weapon in self.generator_power_required.keys():
            temp_active[weapon] = [0.0] * 11
            temp_passive[weapon] = [0.0] * 11
            temp_sideways[weapon] = [0.0] * 11
            temp_piercing[weapon] = [0.0] * 11

        for difficulty in range(logic_difficulty + 1):
            temp_active.update(self.base_active.get(difficulty, {}))
            temp_passive.update(self.base_passive.get(difficulty, {}))
            temp_sideways.update(self.base_sideways.get(difficulty, {}))
            temp_piercing.update(self.base_piercing.get(difficulty, {}))

        # From the temporary tables above, create a final table with DPS class objects
        self.local_dps = {}
        for weapon in self.generator_power_required.keys():
            self.local_dps[weapon] = [DPS(active=temp_active[weapon][i],
                                          passive=temp_passive[weapon][i],
                                          sideways=temp_sideways[weapon][i],
                                          piercing=temp_piercing[weapon][i])
                                      for i in range(11)]

        # ---------------------------------------------------------------------

        self.local_power_provided = self.generator_power_provided[logic_difficulty]

        if logic_difficulty == LogicDifficulty.option_beginner:   self.logic_difficulty_multiplier = 1.20
        elif logic_difficulty == LogicDifficulty.option_standard: self.logic_difficulty_multiplier = 1.10
        elif logic_difficulty == LogicDifficulty.option_expert:   self.logic_difficulty_multiplier = 1.07
        else:                                                     self.logic_difficulty_multiplier = 1.00

        # The two methods below are hot, but they also take a considerable amount of time.
        # Where possible we want to cache their results, but just wrapping them in @lru_cache would make the cache
        # global, and we don't want that (not least because it results in memory leaks).
        # The max sizes have been chosen to keep cache misses low without making the cache too big.
        self.can_meet_dps = lru_cache(maxsize=1024)(self.can_meet_dps)  # type: ignore[method-assign]
        self.get_dps_shot_types = lru_cache(maxsize=512)(self.get_dps_shot_types)  # type: ignore[method-assign]

    def can_meet_dps(self, target_dps: DPS, weapons: tuple[str, ...],
          max_power_level: int = 11, rest_energy: int = 99) -> bool:
        for (weapon, power) in product(weapons, range(max_power_level)):
            if self.generator_power_required[weapon][power] > rest_energy:
                continue

            if self.local_dps[weapon][power].fast_meets_requirements(target_dps):
                return True
        return False

    def get_dps_shot_types(self, target_dps: DPS, weapons: tuple[str, ...],
          max_power_level: int = 11, rest_energy: int = 99) -> bool | dict[int, DPS]:
        best_distances: dict[int, float] = {}  # energy required: distance
        best_dps: dict[int, DPS] = {}  # energy required: best DPS object

        for (weapon, power) in product(weapons, range(max_power_level)):
            cur_energy_req = self.generator_power_required[weapon][power]
            if cur_energy_req > rest_energy:
                continue

            cur_dps = self.local_dps[weapon][power]
            success, distance = cur_dps.meets_requirements(target_dps)

            if success:  # Target DPS has been met, abandon further searching
                return True
            elif distance < best_distances.get(cur_energy_req, 512.0):
                best_distances[cur_energy_req] = distance
                best_dps[cur_energy_req] = cur_dps

        # Nothing is usable. This only happens if we either have none of the required weapons,
        # or if piercing is a requirement and nothing provides enough of it.
        if not best_distances:
            return False

        return {energy: target_dps - cur_dps for (energy, cur_dps) in best_dps.items()}

    # Makes a DPS object that is scaled based on difficulty.
    def make_dps(self, active: float = 0.0, passive: float = 0.0, sideways: float = 0.0, piercing: float = 0.0) -> DPS:
        return DPS(active=active * self.logic_difficulty_multiplier,
                   passive=passive * self.logic_difficulty_multiplier,
                   sideways=sideways * self.logic_difficulty_multiplier,
                   piercing=piercing * self.logic_difficulty_multiplier)


# =================================================================================================


def scale_health(difficulty: int, health: int) -> int:
    health_scale: dict[int, Callable[[int], int]] = {
        1: lambda x: int(x * 0.75) + 1,
        2: lambda x: x,
        3: lambda x: min(254, int(x * 1.2)),
        4: lambda x: min(254, int(x * 1.5)),
        5: lambda x: min(254, int(x * 1.8)),
        6: lambda x: min(254, int(x * 2)),
        7: lambda x: min(254, int(x * 3)),
        8: lambda x: min(254, int(x * 4)),
        9: lambda x: min(254, int(x * 8)),
    }
    difficulty = min(max(1, difficulty), 9)
    return health_scale[difficulty](health)


def get_logic_difficulty_choice(world: "TyrianWorld",
      base: tuple[int, int, int, int], hard_contact: tuple[int, int, int, int] | None = None):
    if world.options.logic_difficulty == "no_logic":
        return 5
    if hard_contact is not None and world.options.contact_bypasses_shields:
        return hard_contact[world.options.logic_difficulty.value - 1]
    return base[world.options.logic_difficulty.value - 1]


def has_twiddle(world: "TyrianWorld", action: SpecialValues) -> bool:
    if world.options.logic_difficulty < LogicDifficulty.option_master:
        return False
    for twiddle in world.twiddles:
        if action == twiddle.action:
            return True
    return False


# =================================================================================================


# If piercing is in a DPS requirement at ALL, we use this order for front weapons.
# As an optimization, only the five front weapons that can actually pierce are here, because rear can't help with this.
ordered_front_table_piercing = [
    "Needle Laser", "Sonic Impulse", "Mega Cannon", "Dragon Frost", "Dragon Flame"
]


# If active is in a DPS requirement, we use this order for front weapons.
ordered_front_table_active = [
    "Atomic RailGun", "Zica Laser", "Laser", "Lightning Cannon", "Poison Bomb", "Mega Pulse (Front)", "Protron Z",
    "NortShip Super Pulse", "Pulse-Cannon", "Heavy Missile Launcher (Front)", "HotDog (Front)", "Hyper Pulse",
    "Guided Bombs", "The Orange Juicer", "Dragon Flame", "Pretzel Missile", "Vulcan Cannon (Front)",
    "Missile Launcher", "Needle Laser", "Mega Cannon", "Shuriken Field", "Widget Beam", "Banana Blast (Front)",
    "Protron (Front)", "Multi-Cannon (Front)", "Sonic Impulse", "Dragon Frost", "RetroBall", "Protron Wave"
]


# Otherwise, we use this order.
ordered_front_table_other = [
    "Shuriken Field", "NortShip Super Pulse", "Banana Blast (Front)", "Multi-Cannon (Front)", "Dragon Frost",
    "Poison Bomb", "Sonic Impulse", "Protron (Front)", "The Orange Juicer", "Hyper Pulse", "Guided Bombs",
    "Lightning Cannon", "Heavy Missile Launcher (Front)", "RetroBall", "HotDog (Front)", "Mega Cannon",
    "Mega Pulse (Front)", "Widget Beam", "Missile Launcher", "Protron Wave", "Pretzel Missile", "Protron Z",
    "Vulcan Cannon (Front)", "Zica Laser", "Pulse-Cannon", "Needle Laser", "Dragon Flame", "Laser"
]


def get_front_weapon_state(state: "CollectionState", player: int, target_dps: DPS) -> list[str]:
    keys = state.prog_items[player].keys()
    if target_dps._type_piercing:
        return [name for name in ordered_front_table_piercing if name in keys]
    elif target_dps._type_active:
        return [name for name in ordered_front_table_active if name in keys]
    else:
        return [name for name in ordered_front_table_other if name in keys]


# =================================================================================================


# If sideways is in a DPS requirement, we use this order for rear weapons.
# If we've gotten to this point, we NEED sideways DPS, so we can exclude rear weapons which don't give it.
ordered_rear_table_sideways = [
    "Starburst", "Scatter Wave", "Mega Pulse (Rear)", "Multi-Cannon (Rear)", "Sonic Wave", "Protron (Rear)",
    "Heavy Guided Bombs", "Banana Blast (Rear)", "NortShip Spreader", "People Pretzels", "Guided Micro Bombs"
]


# If passive is in a DPS requirement, we use this order for rear weapons.
ordered_rear_table_passive = [
    "NortShip Spreader", "Starburst", "Mega Pulse (Rear)", "NortShip Spreader B", "HotDog (Rear)",
    "Heavy Missile Launcher (Rear)", "Protron (Rear)", "Multi-Cannon (Rear)", "Sonic Wave", "Scatter Wave",
    "Vulcan Cannon (Rear)", "Banana Blast (Rear)", "Fireball", "Wild Ball", "Heavy Guided Bombs",
    "Guided Micro Bombs", "People Pretzels"
]


# Otherwise, we use this order.
# Again, the only possible way we get here is if only active is remaining, so we can exclude weapons that can't help.
ordered_rear_table_other = [
    "Banana Blast (Rear)", "Sonic Wave", "Wild Ball", "Fireball", "People Pretzels", "Mega Pulse (Rear)",
    "Scatter Wave", "NortShip Spreader B", "HotDog (Rear)"
]


def get_rear_weapon_state(state: "CollectionState", player: int, target_dps: DPS) -> list[str]:
    keys = state.prog_items[player].keys()
    if target_dps._type_sideways:
        return [name for name in ordered_rear_table_sideways if name in keys]
    elif target_dps._type_passive:
        return [name for name in ordered_rear_table_passive if name in keys]
    else:
        return [name for name in ordered_rear_table_other if name in keys]


# =================================================================================================


def get_generator_level(state: "CollectionState", player: int) -> int:
    # Handle progressive and non-progressive generators independently
    # Otherwise collecting in different orders could result in different generator levels
    if state.has("Gravitron Pulse-Wave", player):   return 6
    elif state.has("Advanced MicroFusion", player): return 5
    elif state.has("Standard MicroFusion", player): return 4
    elif state.has("Gencore Custom MR-12", player): return 3
    elif state.has("Advanced MR-12", player):       return 2
    return min(6, 1 + state.count("Progressive Generator", player))


# =================================================================================================


def can_deal_damage(state: "CollectionState", player: int, target_dps: DPS, energy_adjust: int = 0,
      exclude: list[str] = []) -> bool:
    damage_tables = state.multiworld.worlds[player].damage_tables
    owned_front = get_front_weapon_state(state, player, target_dps)
    owned_rear = get_rear_weapon_state(state, player, target_dps)

    # Some weapons may be excluded by logic for a region/location due to infeasibility of use.
    for excluded_weapon in exclude:
        if excluded_weapon in owned_front:
            owned_front.remove(excluded_weapon)
        elif excluded_weapon in owned_rear:
            owned_rear.remove(excluded_weapon)

    power_level_max = min(11, 1 + state.count("Maximum Power Up", player))
    start_energy = damage_tables.local_power_provided[get_generator_level(state, player)] + energy_adjust

    result = damage_tables.get_dps_shot_types(target_dps, tuple(owned_front), power_level_max, start_energy)

    if type(result) is bool:  # Immediate pass/fail
        return result

    for (used_energy, rest_dps) in result.items():
        rest_energy = start_energy - used_energy
        if damage_tables.can_meet_dps(rest_dps, tuple(owned_rear), power_level_max, rest_energy):
            return True
    return False


def has_armor_level(state: "CollectionState", player: int, armor_level: int) -> bool:
    return True if armor_level <= 5 else state.has("Armor Up", player, armor_level - 5)


def has_power_level(state: "CollectionState", player: int, power_level: int) -> bool:
    return True if power_level <= 1 else state.has("Maximum Power Up", player, power_level - 1)


def has_generator_level(state: "CollectionState", player: int, gen_level: int) -> bool:
    return get_generator_level(state, player) >= gen_level


def has_invulnerability(state: "CollectionState", player: int) -> bool:
    return state.has("Invulnerability", player) \
          or has_twiddle(cast("TyrianWorld", state.multiworld.worlds[player]), SpecialValues.Invulnerability)


def has_repulsor(state: "CollectionState", player: int) -> bool:
    return state.has("Repulsor", player) \
          or has_twiddle(cast("TyrianWorld", state.multiworld.worlds[player]), SpecialValues.Repulsor)


# Alternative to the can_deal_damage, that checks for a specific loadout without doing calculations.
# Basically used to give the generator outs in extreme difficulties, where we know something works
# even if it doesn't fit the exact DPS numbers we're looking for.
def has_specific_loadout(state: "CollectionState", player: int,
      front_weapon: tuple[str, int], rear_weapon: tuple[str, int] | None = None):
    damage_tables = state.multiworld.worlds[player].damage_tables
    usable_energy = damage_tables.local_power_provided[get_generator_level(state, player)]

    required_energy = damage_tables.generator_power_required[front_weapon[0]][front_weapon[1] - 1]
    required_power = front_weapon[1]
    if rear_weapon is not None:
        required_energy += damage_tables.generator_power_required[rear_weapon[0]][rear_weapon[1] - 1]
        required_power = max(front_weapon[1], rear_weapon[1])

    return (usable_energy >= required_energy
          and has_power_level(state, player, required_power)
          and state.has(front_weapon[0], player)
          and (rear_weapon is None or state.has(rear_weapon[0], player)))


# =================================================================================================


def can_ever_have_invulnerability(world: "TyrianWorld") -> bool:
    return has_invulnerability(world.multiworld.get_all_state(False, allow_partial_entrances=True), world.player)


# =================================================================================================


def logic_entrance_rule(world: "TyrianWorld", entrance_name: str, rule: Callable[..., bool]) -> None:
    entrance = world.multiworld.get_entrance(entrance_name, world.player)
    add_rule(entrance, rule)


def logic_location_rule(world: "TyrianWorld", location_name: str, rule: Callable[..., bool]) -> None:
    location = world.multiworld.get_location(location_name, world.player)
    add_rule(location, rule)


def logic_location_exclude(world: "TyrianWorld", location_name: str) -> None:
    location = world.multiworld.get_location(location_name, world.player)
    location.progress_type = LPType.EXCLUDED


# The actual rules start here!


# -------------------------------------------------------------------------------------------------
# =================================================================================================
#                                        EPISODE 1 (ESCAPE)
# =================================================================================================
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# TYRIAN (Episode 1) - 10 locations
# =================================================================================================
def rules_e1_tyrian(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "TYRIAN (Episode 1) - HOLES Warp Orb")
        logic_location_exclude(world, "TYRIAN (Episode 1) - SOH JIN Warp Orb")
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "TYRIAN (Episode 1) - Tank Turn-and-fire Secret")

    # Four trigger enemies among the starting U-Ship sets, need enough damage to clear them out
    if difficulty >= 3:  # Hard or above -- layout differences, this is trivial in Easy or Normal
        dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 19) / 2.0)
        dps_passive = world.damage_tables.make_dps(passive=scale_health(difficulty, 19) / 1.5)
        logic_location_rule(world, "TYRIAN (Episode 1) - HOLES Warp Orb", lambda state, dps1=dps_active, dps2=dps_passive:
              can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))

    # Rock health: 20
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 3.6)
    logic_location_rule(world, "TYRIAN (Episode 1) - BUBBLES Warp Rock", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Boss health: Unscaled 254; Wing health: 100
    wanted_armor = get_logic_difficulty_choice(world, base=(5, 5, 5, 5), hard_contact=(6, 6, 5, 5))
    dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 100) + 254) / 35.0)
    dps_piercing = world.damage_tables.make_dps(piercing=254 / 35.0)

    def boss_destroy_rule(state, dps1=dps_active, dps2=dps_piercing):
        return (can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))
    def boss_timeout_rule(state, armor=wanted_armor, base_rule=boss_destroy_rule):
        return (has_armor_level(state, world.player, armor)
              or has_invulnerability(state, world.player)
              or base_rule(state))

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "TYRIAN (Episode 1) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "TYRIAN (Episode 1) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "TYRIAN (Episode 1) - Boss", boss_destroy_rule)


# =================================================================================================
# BUBBLES (Episode 1) - 6 locations
# =================================================================================================
def rules_e1_bubbles(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "BUBBLES (Episode 1) - Coin Rain, First Line")
        logic_location_exclude(world, "BUBBLES (Episode 1) - Coin Rain, Fourth Line")
        logic_location_exclude(world, "BUBBLES (Episode 1) - Coin Rain, Sixth Line")

    # Health of red bubbles (in all cases): 20
    enemy_health = scale_health(difficulty, 20)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 3.1)
    logic_entrance_rule(world, "BUBBLES (Episode 1) @ Pass Bubble Lines", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    dps_active = world.damage_tables.make_dps(active=enemy_health / 1.6)
    logic_entrance_rule(world, "BUBBLES (Episode 1) @ Speed Up Section", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    dps_active = world.damage_tables.make_dps(active=enemy_health / 2.2)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 3.1)
    logic_location_rule(world, "BUBBLES (Episode 1) - Orbiting Bubbles", lambda state, dps1=dps_active, dps2=dps_piercing:
          can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer"])
          or can_deal_damage(state, world.player, dps2))

    dps_active = world.damage_tables.make_dps(active=enemy_health / 1.2)
    # dps_piercing: unchanged
    logic_location_rule(world, "BUBBLES (Episode 1) - Shooting Bubbles", lambda state, dps1=dps_active, dps2=dps_piercing:
          can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer"])
          or can_deal_damage(state, world.player, dps2))


# =================================================================================================
# HOLES (Episode 1) - 7 locations
# =================================================================================================
def rules_e1_holes(world: "TyrianWorld", difficulty: int) -> None:
    dps_mixed = world.damage_tables.make_dps(active=8.0, passive=21.0)
    wanted_armor = get_logic_difficulty_choice(world, base=(5, 5, 5, 5), hard_contact=(8, 7, 6, 5))
    logic_entrance_rule(world, "HOLES (Episode 1) @ Pass Spinner Gauntlet", lambda state, dps1=dps_mixed, armor=wanted_armor:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-3))

    # Boss ship flyby health: Unscaled 254; Wing health: 100
    dps_mixed = world.damage_tables.make_dps(active=(scale_health(difficulty, 100) + 254) / 5.0, passive=21.0)
    logic_entrance_rule(world, "HOLES (Episode 1) @ Destroy Boss Ships", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1, energy_adjust=-3))


# =================================================================================================
# SOH JIN (Episode 1) - 7 locations
# =================================================================================================
def rules_e1_soh_jin(world: "TyrianWorld", difficulty: int) -> None:
    # Single wall tile: 40
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 40) / 4.4)
    logic_entrance_rule(world, "SOH JIN (Episode 1) @ Destroy Walls", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer", "Guided Bombs", "Guided Micro Bombs", "Heavy Guided Bombs"]))


# =================================================================================================
# ASTEROID1 (Episode 1) - 7 locations
# =================================================================================================
def rules_e1_asteroid1(world: "TyrianWorld", difficulty: int) -> None:
    # Face rock: 25; destructible pieces before it: 5
    enemy_health = scale_health(difficulty, 25) + (scale_health(difficulty, 5) * 2)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 4.4)
    logic_location_rule(world, "ASTEROID1 (Episode 1) - ASTEROID? Warp Orb", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Boss dome: 100; Shields itself with blocks
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 100) / 12.0)
    dps_piercing = world.damage_tables.make_dps(piercing=scale_health(difficulty, 100) / 30.0)
    logic_entrance_rule(world, "ASTEROID1 (Episode 1) @ Destroy Boss", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2, exclude=["The Orange Juicer"]))


# =================================================================================================
# ASTEROID2 (Episode 1) - 8 locations
# =================================================================================================
def rules_e1_asteroid2(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "ASTEROID2 (Episode 1) - Tank Turn-around Secret 1")
        logic_location_exclude(world, "ASTEROID2 (Episode 1) - Tank Turn-around Secret 2")
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "ASTEROID2 (Episode 1) - Tank Assault, Right Tank Secret")

    # All tanks: 30
    enemy_health = scale_health(difficulty, 30)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 2.1)
    logic_location_rule(world, "ASTEROID2 (Episode 1) - Tank Bridge", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Tank Turn-around Secrets 1 and 2:
    # On Standard or below, assume most damage will come only after the tank secret items are active
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        dps_active = world.damage_tables.make_dps(active=enemy_health / 2.3)
        logic_location_rule(world, "ASTEROID2 (Episode 1) - Tank Turn-around Secret 1", lambda state, dps1=dps_active:
              can_deal_damage(state, world.player, dps1))

        dps_active = world.damage_tables.make_dps(active=enemy_health / 3.9)
        logic_location_rule(world, "ASTEROID2 (Episode 1) - Tank Turn-around Secret 2", lambda state, dps1=dps_active:
              can_deal_damage(state, world.player, dps1))

    # Face rock containing orb: 25
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 25) / 4.4)
    logic_location_rule(world, "ASTEROID2 (Episode 1) - MINEMAZE Warp Orb", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Boss tank: 80
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 80) / 8.0)
    logic_entrance_rule(world, "ASTEROID2 (Episode 1) @ Destroy Boss", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# ASTEROID? (Episode 1) - 6 locations
# =================================================================================================
def rules_e1_asteroidq(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "ASTEROID? (Episode 1) - WINDY Warp Orb")

    # Launchers: 40
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 40) / 3.5)
    logic_entrance_rule(world, "ASTEROID? (Episode 1) @ Initial Welcome", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Secret ships: also 40
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 40) / 1.36)
    logic_entrance_rule(world, "ASTEROID? (Episode 1) @ Quick Shots", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    wanted_armor = get_logic_difficulty_choice(world, base=(6, 5, 5, 5), hard_contact=(8, 7, 7, 6))
    logic_entrance_rule(world, "ASTEROID? (Episode 1) @ Final Gauntlet", lambda state, armor=wanted_armor:
          has_armor_level(state, world.player, armor))


# =================================================================================================
# MINEMAZE (Episode 1) - 6 locations
# =================================================================================================
def rules_e1_minemaze(world: "TyrianWorld", difficulty: int) -> None:
    # Gates: 20
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 3.8)
    logic_entrance_rule(world, "MINEMAZE (Episode 1) @ Destroy Gates", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# WINDY (Episode 1) - 1 location
# =================================================================================================
def rules_e1_windy(world: "TyrianWorld", difficulty: int) -> None:
    # Regular block: 10
    # Time is based on when the shooting blocks start to fire, instead of the maximum possible for damage
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 10) / 1.0)
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 7, 5, 5), hard_contact=(11, 11, 8, 6))
    logic_entrance_rule(world, "WINDY (Episode 1) @ Fly Through", lambda state, dps1=dps_active, armor=wanted_armor:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1))

    # Question mark block: 20
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 1.4)
    logic_location_rule(world, "WINDY (Episode 1) - Central Question Mark", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    if world.options.logic_difficulty == LogicDifficulty.option_master:
        # Always assumed reachable. Take a big bite out of your armor if you need to.
        wanted_armor = 14 if world.options.contact_bypasses_shields else 12
        logic_entrance_rule(world, "WINDY (Episode 1) @ Phase Through Walls", lambda state, armor=wanted_armor:
              has_invulnerability(state, world.player) or has_armor_level(state, world.player, armor))
    else:
        # If we don't have a way to get invulnerability, we consider the location realistically unreachable.
        if not can_ever_have_invulnerability(world):
            logic_entrance_rule(world, "WINDY (Episode 1) @ Phase Through Walls", lambda state:
                  has_armor_level(state, world.player, 14))
            logic_location_exclude(world, "WINDY (Episode 1) - Central Question Mark")
        else:
            logic_entrance_rule(world, "WINDY (Episode 1) @ Phase Through Walls", lambda state:
                  has_invulnerability(state, world.player))
            if world.options.logic_difficulty <= LogicDifficulty.option_standard:
                logic_location_exclude(world, "WINDY (Episode 1) - Central Question Mark")


# =================================================================================================
# SAVARA (Episode 1) - 7 locations
# =================================================================================================
def rules_e1_savara(world: "TyrianWorld", difficulty: int) -> None:
    # Huge planes: 60
    # On Lord of the Game, this needs a very specific loadout to destroy in time.
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 60) / 1.125)
    logic_location_rule(world, "SAVARA (Episode 1) - Huge Plane, Speeds By", lambda state, dps1=dps_active:
          has_specific_loadout(state, world.player, front_weapon=("Atomic RailGun", 11), rear_weapon=("Mega Pulse (Rear)", 11))
          or (
              has_generator_level(state, world.player, 3)
              and can_deal_damage(state, world.player, dps1)
          ))

    # Vulcan plane containing item: 14
    # The vulcan shots hurt a lot, so optimal kill would be with passive DPS if possible
    dps_active = world.damage_tables.make_dps(passive=scale_health(difficulty, 14) / 2.4)
    dps_passive = world.damage_tables.make_dps(active=scale_health(difficulty, 14) / 1.6)
    logic_location_rule(world, "SAVARA (Episode 1) - Vulcan Plane", lambda state, dps1=dps_active, dps2=dps_passive:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Damage estimate: 254 health for the boss, shooting through 15 ticks and 4 missiles
    boss_health = scale_health(difficulty, 254) + (scale_health(difficulty, 6) * 15) + (scale_health(difficulty, 10) * 4)
    savara_boss_active = world.damage_tables.make_dps(active=boss_health / 30.0)
    savara_tick_sideways = world.damage_tables.make_dps(sideways=scale_health(difficulty, 6) / 1.2)

    def boss_destroy_rule(state, dps1=savara_boss_active):
        return (can_deal_damage(state, world.player, dps1))
    # Also need enough damage to destroy things the boss shoots at you, when dodging isn't an option
    def boss_timeout_rule(state, dps2=savara_tick_sideways, base_rule=boss_destroy_rule):
        return (has_invulnerability(state, world.player)
              or can_deal_damage(state, world.player, dps2)
              or base_rule(state))

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "SAVARA (Episode 1) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "SAVARA (Episode 1) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "SAVARA (Episode 1) - Boss", boss_destroy_rule)


# =================================================================================================
# SAVARA II (Episode 1) - 7 locations
# =================================================================================================
def rules_e1_savara_ii(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(8, 7, 6, 5))
    logic_entrance_rule(world, "SAVARA II (Episode 1) @ Base Requirements", lambda state, armor=wanted_armor:
          has_power_level(state, world.player, 2)
          and has_armor_level(state, world.player, armor))

    dps_active = world.damage_tables.make_dps(active=7.0)
    logic_entrance_rule(world, "SAVARA II (Episode 1) @ Destroy Green Planes", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Huge planes: 60 (difficulty -1 due to level)
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty - 1, 60) / 2.3)
    logic_location_rule(world, "SAVARA II (Episode 1) - Huge Plane Amidst Turrets", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Same vulcan DPS as SAVARA, we re-use the DPS made for it (plus accounting for difficulty adjust)
    dps_active = world.damage_tables.make_dps(passive=scale_health(difficulty - 1, 14) / 2.4)
    dps_passive = world.damage_tables.make_dps(active=scale_health(difficulty - 1, 14) / 1.6)
    logic_location_rule(world, "SAVARA II (Episode 1) - Vulcan Planes Near Blimp", lambda state, dps1=dps_passive, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Same boss as SAVARA, we re-use the rules we made for it (plus accounting for difficulty adjust)
    boss_health = scale_health(difficulty - 1, 254) + (scale_health(difficulty - 1, 6) * 15) + (scale_health(difficulty - 1, 10) * 4)
    savara_boss_active = world.damage_tables.make_dps(active=boss_health / 30.0)
    savara_tick_sideways = world.damage_tables.make_dps(sideways=scale_health(difficulty, 6) / 1.2)

    def boss_destroy_rule(state, dps1=savara_boss_active):
        return (can_deal_damage(state, world.player, dps1))
    # Also need enough damage to destroy things the boss shoots at you, when dodging isn't an option
    def boss_timeout_rule(state, dps2=savara_tick_sideways, base_rule=boss_destroy_rule):
        return (has_invulnerability(state, world.player)
              or can_deal_damage(state, world.player, dps2)
              or base_rule(state))

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "SAVARA (Episode 1) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "SAVARA (Episode 1) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "SAVARA (Episode 1) - Boss", boss_destroy_rule)


# =================================================================================================
# BONUS (Episode 1) - No locations
# =================================================================================================
def rules_e1_bonus(world: "TyrianWorld", difficulty: int) -> None:
    # Keep this from occurring too early.
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 10), passive=scale_health(difficulty, 10))
    logic_entrance_rule(world, "BONUS (Episode 1) @ Destroy Patterns", lambda state, dps1=dps_mixed:
          has_power_level(state, world.player, 2)
          and can_deal_damage(state, world.player, dps1))


# =================================================================================================
# MINES (Episode 1) - 5 locations
# =================================================================================================
def rules_e1_mines(world: "TyrianWorld", difficulty: int) -> None:
    # Rotating orbs: 20
    enemy_health = scale_health(difficulty, 20)  # Rotating Orbs
    dps_active = world.damage_tables.make_dps(active=enemy_health / 1.4)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 2.7)
    logic_entrance_rule(world, "MINES (Episode 1) @ Destroy First Orb", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    dps_active = world.damage_tables.make_dps(active=enemy_health / 0.8)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 1.2)
    logic_entrance_rule(world, "MINES (Episode 1) @ Destroy Second Orb", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Blue mine has static health (does not depend on difficulty)
    dps_active = world.damage_tables.make_dps(active=30 / 3.0)
    logic_location_rule(world, "MINES (Episode 1) - Blue Mine", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# DELIANI (Episode 1) - 8 locations
# =================================================================================================
def rules_e1_deliani(world: "TyrianWorld", difficulty: int) -> None:
    # Rail turret: 30
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 2.2)
    logic_location_rule(world, "DELIANI (Episode 1) - Tricky Rail Turret", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Two-tile wide turret ships: 25
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 25) / 1.6)
    wanted_armor = get_logic_difficulty_choice(world, base=(10, 9, 8, 6))
    logic_entrance_rule(world, "DELIANI (Episode 1) @ Pass Ambush", lambda state, dps1=dps_active, armor=wanted_armor:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1))

    # Repulsor orbs: 80; boss: 200
    boss_health = (scale_health(difficulty, 80) * 3) + scale_health(difficulty, 200)
    dps_active = world.damage_tables.make_dps(active=boss_health / 22.0)
    logic_entrance_rule(world, "DELIANI (Episode 1) @ Destroy Boss", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# SAVARA V (Episode 1) - 7 locations
# =================================================================================================
def rules_e1_savara_v(world: "TyrianWorld", difficulty: int) -> None:
    # Blimp: 70
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 70) / 1.5)
    logic_location_rule(world, "SAVARA V (Episode 1) - Super Blimp", lambda state, dps1=dps_active:
          has_specific_loadout(state, world.player, front_weapon=("Atomic RailGun", 11), rear_weapon=("Mega Pulse (Rear)", 11))
          or can_deal_damage(state, world.player, dps1))

    dps_active = world.damage_tables.make_dps(active=254 / 15.0)
    logic_entrance_rule(world, "SAVARA V (Episode 1) @ Destroy Bosses", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# ASSASSIN (Episode 1) - 1 location, goal level
# =================================================================================================
def rules_e1_assassin(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 8, 7, 5))
    wanted_energy = get_logic_difficulty_choice(world, base=(3, 2, 2, 1))
    dps_active = world.damage_tables.make_dps(active=508 / 20.0)
    logic_entrance_rule(world, "ASSASSIN (Episode 1) @ Destroy Boss", lambda state, dps1=dps_active, armor=wanted_armor, energy=wanted_energy:
          has_power_level(state, world.player, 5)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, energy)
          and can_deal_damage(state, world.player, dps1))


# -------------------------------------------------------------------------------------------------
# Grand total for Episode 1: 93 locations across 16 levels
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# =================================================================================================
#                                      EPISODE 2 (TREACHERY)
# =================================================================================================
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# TORM (Episode 2) - 8 locations
# =================================================================================================
def rules_e2_torm(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "TORM (Episode 2) - Ship Fleeing Dragon Secret")

    # On standard or below, require killing the dragon behind the secret ship
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        # Dragon: 40
        dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 40) / 1.6)
        logic_location_rule(world, "TORM (Episode 2) - Ship Fleeing Dragon Secret", lambda state, dps1=dps_active:
              can_deal_damage(state, world.player, dps1))

    dps_active = world.damage_tables.make_dps(active=254 / 4.4)
    logic_location_rule(world, "TORM (Episode 2) - Boss Ship Fly-By", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Technically this boss has 254 health, but compensating for constant movement all over the screen
    dps_active = world.damage_tables.make_dps(active=(254 * 1.75) / 32.0)

    def boss_destroy_rule(state, dps1=dps_active):
        return can_deal_damage(state, world.player, dps1)
    # No timeout rule, attainable with an empty loadout

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "TORM (Episode 2) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "TORM (Episode 2) - Boss", boss_destroy_rule)


# =================================================================================================
# GYGES (Episode 2) - 7 locations
# =================================================================================================
def rules_e2_gyges(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "GYGES (Episode 2) - GEM WAR Warp Orb")

    # Orbsnakes: 10 (x6)
    dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 10) * 6) / 5.0)
    dps_piercing = world.damage_tables.make_dps(active=scale_health(difficulty, 10) / 5.0)
    logic_location_rule(world, "GYGES (Episode 2) - Orbsnake", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Either the repulsor mitigates the bullets in the speed up section,
    # or you have a decent loadout and can destroy a few things to make your life easier
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 7, 6, 6))
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 10) / 1.3, passive=(scale_health(difficulty, 10) * 3) / 1.3)
    logic_entrance_rule(world, "GYGES (Episode 2) @ After Speed Up Section", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_armor_level(state, world.player, armor)
          and
          (
              has_repulsor(state, world.player)
              or can_deal_damage(state, world.player, dps1, energy_adjust=-3)
          ))

    dps_active = world.damage_tables.make_dps(active=254 / 15.0)
    logic_entrance_rule(world, "GYGES (Episode 2) @ Destroy Boss", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1, energy_adjust=-3))


# =================================================================================================
# BONUS 1 (Episode 2) - No locations
# =================================================================================================
def rules_e2_bonus_1(world: "TyrianWorld", difficulty: int) -> None:
    # Keep this from occurring too early.
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 10), passive=scale_health(difficulty, 10))
    logic_entrance_rule(world, "BONUS 1 (Episode 2) @ Destroy Patterns", lambda state, dps1=dps_mixed:
          has_power_level(state, world.player, 2)
          and can_deal_damage(state, world.player, dps1))


# =================================================================================================
# ASTCITY (Episode 2) - 10 locations
# =================================================================================================
def rules_e2_astcity(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "ASTCITY (Episode 2) - MISTAKES Warp Orb")

    # This level throws superbombs at you like they're candy, so we only bother checking for passive DPS.
    wanted_armor = get_logic_difficulty_choice(world, base=(8, 7, 7, 5))
    dps_mixed = world.damage_tables.make_dps(passive=scale_health(difficulty, 15) / 1.1)
    logic_entrance_rule(world, "ASTCITY (Episode 2) @ Base Requirements", lambda state, dps1=dps_mixed, armor=wanted_armor:
          has_armor_level(state, world.player, (armor - 1) if has_repulsor(state, world.player) else armor)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-2))


# =================================================================================================
# BONUS 2 (Episode 2) - No locations
# =================================================================================================
def rules_e2_bonus_2(world: "TyrianWorld", difficulty: int) -> None:
    pass  # Logicless - flythrough only, no items, easily doable without firing a shot


# =================================================================================================
# GEM WAR (Episode 2) - 6 locations
# =================================================================================================
def rules_e2_gem_war(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 7, 6, 5), hard_contact=(9, 9, 8, 6))
    logic_entrance_rule(world, "GEM WAR (Episode 2) @ Base Requirements", lambda state, armor=wanted_armor:
          has_power_level(state, world.player, 4)
          and has_armor_level(state, world.player, armor))

    # Red gem ship: Unscaled 254
    # We compensate for their movement, and other enemies being nearby
    wanted_passive = 20.0 if world.options.contact_bypasses_shields else 12.0
    dps_mixed = world.damage_tables.make_dps(active=(254 * 1.4) / 20.0, passive=wanted_passive)
    logic_entrance_rule(world, "GEM WAR (Episode 2) @ Red Gem Leaders Easy", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))  # 2 and 3

    dps_mixed = world.damage_tables.make_dps(active=(254 * 1.4) / 17.5, passive=wanted_passive)
    logic_entrance_rule(world, "GEM WAR (Episode 2) @ Red Gem Leaders Medium", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))  # 1

    dps_mixed = world.damage_tables.make_dps(active=(254 * 1.4) / 13.0, passive=wanted_passive)
    logic_entrance_rule(world, "GEM WAR (Episode 2) @ Red Gem Leaders Hard", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))  # 4

    # Center of boss ship: 20
    # Flanked by three ships with unscaled health 254, either destroy the one in front, or have a piercing weapon
    dps_mixed = world.damage_tables.make_dps(active=(254 + scale_health(difficulty, 20)) / 16.0, passive=wanted_passive)
    dps_piercemix = world.damage_tables.make_dps(piercing=scale_health(difficulty, 20) / 16.0, passive=wanted_passive)
    logic_entrance_rule(world, "GEM WAR (Episode 2) @ Blue Gem Bosses", lambda state, dps1=dps_piercemix, dps2=dps_mixed:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))


# =================================================================================================
# MARKERS (Episode 2) - 5 locations
# =================================================================================================
def rules_e2_markers(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "MARKERS (Episode 2) - Car Destroyer Secret")

    # Turrets: 20 -- Just a bare minimum, to enter the level
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 3.8)
    # Flying through this stage is relatively easy *unless* HardContact is turned on.
    wanted_armor = get_logic_difficulty_choice(world, base=(5, 5, 5, 5), hard_contact=(9, 8, 8, 6))
    logic_entrance_rule(world, "MARKERS (Episode 2) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_active:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer"]))

    # Minelayer: 30; Mine: 6 (estimated 5 mines hit)
    # This is good enough to beat the level and collect everything else
    enemy_health = scale_health(difficulty, 30) + (scale_health(difficulty, 6) * 5)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 6.5)
    logic_entrance_rule(world, "MARKERS (Episode 2) @ Through Minelayer Blockade", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer"]))


# =================================================================================================
# MISTAKES (Episode 2) - 10 locations
# =================================================================================================
def rules_e2_mistakes(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "MISTAKES (Episode 2) - Orbsnakes, Trigger Enemy 1")
        logic_location_exclude(world, "MISTAKES (Episode 2) - Claws, Trigger Enemy 1")
        logic_location_exclude(world, "MISTAKES (Episode 2) - Claws, Trigger Enemy 2")
        logic_location_exclude(world, "MISTAKES (Episode 2) - Super Bubble Spawner")
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "MISTAKES (Episode 2) - Orbsnakes, Trigger Enemy 2")
        logic_location_exclude(world, "MISTAKES (Episode 2) - Anti-Softlock")

    wanted_armor = get_logic_difficulty_choice(world, base=(6, 6, 5, 5), hard_contact=(9, 8, 7, 5))
    wanted_energy = get_logic_difficulty_choice(world, base=(3, 3, 2, 2))
    logic_entrance_rule(world, "MISTAKES (Episode 2) @ Base Requirements", lambda state, armor=wanted_armor, energy=wanted_energy:
          has_armor_level(state, world.player, armor)
          and
          (
              has_generator_level(state, world.player, energy)
              or has_repulsor(state, world.player)
          ))

    # Most trigger enemies: 10
    enemy_health = scale_health(difficulty, 10)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 1.2)
    logic_entrance_rule(world, "MISTAKES (Episode 2) @ Bubble Spawner Path", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Orbsnakes: 10 (x6)
    dps_active = world.damage_tables.make_dps(active=(enemy_health * 6) / 5.5)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 5.5)
    logic_location_rule(world, "MISTAKES (Episode 2) - Orbsnakes, Trigger Enemy 1", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    dps_active = world.damage_tables.make_dps(active=(enemy_health * 6) / 0.8)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 0.8)
    # The hardcoded solution for this is to use the Banana Blast (Rear)'s banana bombs to weaken the orbsnake
    # so that the piercing Sonic Impulse can do enough damage. This is required in Lord of the Game.
    logic_entrance_rule(world, "MISTAKES (Episode 2) @ Softlock Path", lambda state, dps1=dps_piercing, dps2=dps_active:
          has_specific_loadout(state, world.player, front_weapon=("Sonic Impulse", 5), rear_weapon=("Banana Blast (Rear)", 6))
          or can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))


# =================================================================================================
# SOH JIN (Episode 2) - 7 locations
# =================================================================================================
def rules_e2_soh_jin(world: "TyrianWorld", difficulty: int) -> None:
    # Brown claw enemy: 15
    # These enemies don't contain any items, but they home in on you and are a bit more difficult to dodge because
    # of that, so lock the whole level behind being able to destroy them; it's enough DPS to get locations here
    wanted_energy = get_logic_difficulty_choice(world, base=(3, 2, 2, 2))
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 1.8)
    logic_entrance_rule(world, "SOH JIN (Episode 2) @ Base Requirements", lambda state, dps1=dps_active, energy=wanted_energy:
          has_power_level(state, world.player, 3)
          and
          (
              has_generator_level(state, world.player, energy)
              or has_repulsor(state, world.player)
          )
          and can_deal_damage(state, world.player, dps1))

    # Paddle... things?: 100
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 100) / 9.0)
    dps_alternate = world.damage_tables.make_dps(active=scale_health(difficulty, 100) / 15.0, sideways=10.0)
    logic_entrance_rule(world, "SOH JIN (Episode 2) @ Destroy Second Wave Paddles", lambda state, dps1=dps_active, dps2=dps_alternate:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Dodging these orbs is surprisingly difficult, because of the erratic vertical movement with their oscillation
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 8, 7, 5), hard_contact=(11, 10, 9, 7))
    logic_entrance_rule(world, "SOH JIN (Episode 2) @ Fly Through Third Wave Orbs", lambda state, armor=wanted_armor:
          has_armor_level(state, world.player, (armor - 2) if has_invulnerability(state, world.player) else armor))

    dps_mixed = world.damage_tables.make_dps(active=254 / 20.0, sideways=254 / 20.0)
    logic_entrance_rule(world, "SOH JIN (Episode 2) @ Destroy Third Wave Orbs", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# BOTANY A (Episode 2) - 6 locations
# =================================================================================================
def rules_e2_botany_a(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "BOTANY A (Episode 2) - End of Path Secret 1")
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "BOTANY A (Episode 2) - End of Path Secret 2")

    wanted_armor = get_logic_difficulty_choice(world, base=(9, 9, 8, 6))
    wanted_generator = 3 if world.options.logic_difficulty <= LogicDifficulty.option_standard else 2
    if (difficulty + 1) >= 4:  # Impossible or above
        wanted_armor += 2

    logic_entrance_rule(world, "BOTANY A (Episode 2) @ Beyond Starting Area", lambda state, armor=wanted_armor, generator=wanted_generator:
          has_power_level(state, world.player, 4)
          and (
              has_armor_level(state, world.player, armor)
              or (
                  has_repulsor(state, world.player)
                  and has_generator_level(state, world.player, generator)  # For shield recovery
                  and has_armor_level(state, world.player, armor - 2)
              )
          ))

    # Moving turret: 15 (difficulty +1 due to level)
    enemy_health = scale_health(difficulty + 1, 15)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 2.0)
    logic_entrance_rule(world, "BOTANY A (Episode 2) @ Can Destroy Turrets", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1, energy_adjust=-4))

    dps_active = world.damage_tables.make_dps(active=enemy_health / 1.0)
    logic_location_rule(world, "BOTANY A (Episode 2) - Mobile Turret Approaching Head-On", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1, energy_adjust=-4))

    # This one comes before "Beyond Starting Area"...
    dps_active = world.damage_tables.make_dps(active=enemy_health / 3.0)
    logic_location_rule(world, "BOTANY A (Episode 2) - Retreating Mobile Turret", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Green ship: 20 (difficulty +1 due to level)
    enemy_health = scale_health(difficulty + 1, 20)
    # The backmost ship is the one with the item, expect to destroy at least one other ship to reach it
    # (except if you can do enough piercing damage, of course)
    dps_active = world.damage_tables.make_dps(active=(enemy_health * 2) / 3.0)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 3.0)
    logic_location_rule(world, "BOTANY A (Episode 2) - Green Ship Pincer", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1, energy_adjust=-4)
          or can_deal_damage(state, world.player, dps2, energy_adjust=-4))

    dps_boss = world.damage_tables.make_dps(active=(254 * 1.8) / 24.0)
    def boss_destroy_rule(state, dps1=dps_boss):
        return can_deal_damage(state, world.player, dps1, energy_adjust=-4)
    # No additional things needed to be able to timeout

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "BOTANY A (Episode 2) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "BOTANY A (Episode 2) - Boss", boss_destroy_rule)


# =================================================================================================
# BOTANY B (Episode 2) - 6 locations
# =================================================================================================
def rules_e2_botany_b(world: "TyrianWorld", difficulty: int) -> None:
    # Destructible sensor: 6 (difficulty +1 due to level)
    # Start of level, nothing nearby dangerous, only need to destroy it
    dps_active = world.damage_tables.make_dps(scale_health(difficulty + 1, 6) / 4.0)
    logic_location_rule(world, "BOTANY B (Episode 2) - Starting Platform Sensor", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    wanted_armor = get_logic_difficulty_choice(world, base=(8, 7, 7, 5))
    if (difficulty + 1) >= 4:  # Impossible or above
        wanted_armor += 2

    # Turret: 15 (difficulty +1 due to level)
    enemy_health = scale_health(difficulty + 1, 15)
    # Past this point is when the game starts demanding more of you.
    # Need enough damage to clear out the screen of turrets
    dps_active = world.damage_tables.make_dps(active=(enemy_health * 4) / 4.5)
    dps_passive = world.damage_tables.make_dps(passive=(enemy_health * 4) / 3.0)
    logic_entrance_rule(world, "BOTANY B (Episode 2) @ Beyond Starting Platform", lambda state, armor=wanted_armor, dps1=dps_active, dps2=dps_passive:
          has_power_level(state, world.player, 4)
          and has_armor_level(state, world.player, armor)
          and (
              can_deal_damage(state, world.player, dps1, energy_adjust=-5)
              or can_deal_damage(state, world.player, dps2, energy_adjust=-5)
          ))

    # Same boss as BOTANY A, re-use rule from it
    dps_boss = world.damage_tables.make_dps(active=(254 * 1.8) / 24.0)
    def boss_destroy_rule(state, dps1=dps_boss):
        return can_deal_damage(state, world.player, dps1, energy_adjust=-5)
    # No additional things needed to be able to timeout

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "BOTANY B (Episode 2) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "BOTANY B (Episode 2) - Boss", boss_destroy_rule)


# =================================================================================================
# GRYPHON (Episode 2) - 10 locations, goal level
# =================================================================================================
def rules_e2_gryphon(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(10, 9, 8, 7), hard_contact=(11, 10, 10, 8))
    dps_mixed = world.damage_tables.make_dps(active=22.0, passive=16.0)
    logic_entrance_rule(world, "GRYPHON (Episode 2) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_power_level(state, world.player, 5)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 3)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-5))


# -------------------------------------------------------------------------------------------------
# Grand total for Episode 2: 75 locations
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# =================================================================================================
#                                   EPISODE 3 (MISSION: SUICIDE)
# =================================================================================================
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# GAUNTLET (Episode 3) - 8 locations
# =================================================================================================
def rules_e3_gauntlet(world: "TyrianWorld", difficulty: int) -> None:
    # Capsule ships: 10 (difficulty -1 due to level)
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty - 1, 10) / 1.3)
    logic_location_rule(world, "GAUNTLET (Episode 3) - Capsule Ships Near Mace", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Gates: 20 (difficulty -1 due to level)
    enemy_health = scale_health(difficulty - 1, 20)

    dps_active = world.damage_tables.make_dps(active=(enemy_health * 2) / 4.4)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 4.4)
    logic_location_rule(world, "GAUNTLET (Episode 3) - Doubled-up Gates", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # These two use the same DPS rule, but are in different sub-regions
    dps_active = world.damage_tables.make_dps(active=enemy_health / 1.5)
    logic_location_rule(world, "GAUNTLET (Episode 3) - Split Gates, Left", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))
    logic_location_rule(world, "GAUNTLET (Episode 3) - Gate near Freebie Item", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Weak point orb: 6 (difficulty -1 due to level)
    enemy_health = scale_health(difficulty - 1, 6)
    dps_active = world.damage_tables.make_dps(active=enemy_health / 0.5)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 1.2)
    # Invulnerability lets you safely pass through without damaging
    logic_entrance_rule(world, "GAUNTLET (Episode 3) @ Clear Orb Tree", lambda state, dps1=dps_piercing, dps2=dps_active:
          has_invulnerability(state, world.player)
          or can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))
    logic_location_rule(world, "GAUNTLET (Episode 3) - Tree of Spinning Orbs", lambda state, dps1=dps_piercing, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))


# =================================================================================================
# IXMUCANE (Episode 3) - 7 locations
# =================================================================================================
def rules_e3_ixmucane(world: "TyrianWorld", difficulty: int) -> None:
    # Minelayer: Unscaled 254, or 10 (weak point); Dropped mines: 20
    # Need sideways + active to be able to hit the weak points of the center minelayers while damaging other things,
    # Piercing to hit those weak points through other things anyway, or just a lot of active damage altogether.
    # Alternatively, Invulnerability can also fill piercing's role.
    dps_option1 = world.damage_tables.make_dps(piercing=scale_health(difficulty, 10) / 8.0)
    dps_option2 = world.damage_tables.make_dps(active=8.0, sideways=scale_health(difficulty, 10) / 8.0)
    dps_option3 = world.damage_tables.make_dps(active=((scale_health(difficulty, 20) * 3) + 254) / 8.0)
    logic_entrance_rule(world, "IXMUCANE (Episode 3) @ Pass Minelayers Requirements", lambda state, dps1=dps_option1, dps2=dps_option2, dps3=dps_option3:
          has_invulnerability(state, world.player)
          or can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2)
          or can_deal_damage(state, world.player, dps3))

    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 0.7)
    logic_location_rule(world, "IXMUCANE (Episode 3) - Enemy From Behind", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # This boss keeps itself guarded inside an indestructible rock at almost all times, and there's a second
    # destructible target in front of the actual weak point... But none of this matters if you can pierce.
    # It also summons a mass of tiny rocks as an attack, so if we aren't cheesing it, we want at least some passive.
    boss_health = scale_health(difficulty, 25)
    dps_option1 = world.damage_tables.make_dps(piercing=boss_health / 24.0)
    dps_option2 = world.damage_tables.make_dps(active=(boss_health * 2) / 3.8, passive=12.0)
    dps_safety = world.damage_tables.make_dps(passive=15.0)

    def boss_destroy_rule(state, dps1=dps_option1, dps2=dps_option2):
        return (can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2, energy_adjust=-4, exclude=["The Orange Juicer", "Guided Bombs", "Protron Z", "Wild Ball", "Fireball", "Banana Blast (Rear)"]))
    # Need some passive if we want to time out the boss, or invulnerability to ignore the rocks
    def boss_timeout_rule(state, dps3=dps_safety, base_rule=boss_destroy_rule):
        return (has_invulnerability(state, world.player)
              or boss_destroy_rule(state)
              or can_deal_damage(state, world.player, dps3, energy_adjust=-4))

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "IXMUCANE (Episode 3) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "IXMUCANE (Episode 3) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "IXMUCANE (Episode 3) - Boss", boss_destroy_rule)


# =================================================================================================
# BONUS (Episode 3) - 5 locations
# =================================================================================================
def rules_e3_bonus(world: "TyrianWorld", difficulty: int) -> None:
    # Turrets have only one health; they die to any damage, but are guarded from front and back.
    dps_passive = world.damage_tables.make_dps(passive=0.2)
    dps_piercing = world.damage_tables.make_dps(piercing=0.2)
    if world.options.logic_difficulty <= LogicDifficulty.option_expert:
        logic_location_rule(world, "BONUS (Episode 3) - Lone Turret 1", lambda state, dps1=dps_piercing, dps2=dps_passive:
              can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))
        logic_location_rule(world, "BONUS (Episode 3) - Sonic Wave Hell Turret", lambda state, dps1=dps_piercing, dps2=dps_passive:
              can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))

    # Doesn't sway left/right like the other two
    logic_location_rule(world, "BONUS (Episode 3) - Lone Turret 2", lambda state, dps1=dps_piercing, dps2=dps_passive:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # To pass the turret onslaught
    # Two-wide turret: 25; but we only need to take it down to damaged (non-firing) state
    enemy_health = scale_health(difficulty, 25) - 10
    dps_active = world.damage_tables.make_dps(active=(enemy_health * 4) / 3.6)
    logic_entrance_rule(world, "BONUS (Episode 3) @ Pass Onslaughts", lambda state, dps1=dps_active:
          has_generator_level(state, world.player, 3)  # For shield recovery
          and has_armor_level(state, world.player, 8)
          and (
              has_repulsor(state, world.player)
              or can_deal_damage(state, world.player, dps1)
          ))

    # Do you have knowledge of the safe spot through this section? Master assumes you do, anything else doesn't.
    # If we're not assuming safe spot knowledge, we need the repulsor, or some sideways DPS and more armor.
    if world.options.logic_difficulty < LogicDifficulty.option_master:
        dps_mixed = world.damage_tables.make_dps(active=(enemy_health * 4) / 3.6, sideways=4.0)
        logic_entrance_rule(world, "BONUS (Episode 3) @ Sonic Wave Hell", lambda state, dps1=dps_mixed:
              has_repulsor(state, world.player)
              or (
                  has_armor_level(state, world.player, 12)
                  and can_deal_damage(state, world.player, dps_mixed)
              ))

    # To actually get the items from turret onslaught; two two-tile turrets, plus item ship
    enemy_health = scale_health(difficulty, 25)
    ship_health = scale_health(difficulty, 3)
    dps_active = world.damage_tables.make_dps(active=((enemy_health * 2) + ship_health) / 1.8)
    logic_entrance_rule(world, "BONUS (Episode 3) @ Get Items from Onslaughts", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# STARGATE (Episode 3) - 7 locations
# =================================================================================================
def rules_e3_stargate(world: "TyrianWorld", difficulty: int) -> None:
    # Just need some way of combating the bubble spam that happens after the last normal location
    dps_passive = world.damage_tables.make_dps(passive=7.0)
    logic_entrance_rule(world, "STARGATE (Episode 3) @ Reach Bubble Spawner", lambda state, dps1=dps_passive:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# AST. CITY (Episode 3) - 9 locations
# =================================================================================================
def rules_e3_ast_city(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5), hard_contact=(8, 8, 7, 5))
    logic_entrance_rule(world, "AST. CITY (Episode 3) @ Base Requirements", lambda state, armor=wanted_armor:
          has_armor_level(state, world.player, armor))

    # Boss domes: 100 (difficulty -1 due to level)
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty - 1, 100) / 4.5)
    logic_entrance_rule(world, "AST. CITY (Episode 3) @ Destroy Boss Domes", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# SAWBLADES (Episode 3) - 7 locations
# =================================================================================================
def rules_e3_sawblades(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "SAWBLADES (Episode 3) - SuperCarrot Secret Drop")

    # Periodically, tiny rocks get spammed all over the screen throughout this level.
    # We need to have some passive and some armor to be able to deal with these moments.
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5), hard_contact=(10, 9, 8, 6))
    dps_mixed = world.damage_tables.make_dps(active=10.0, passive=scale_health(difficulty, 2) * 6)
    logic_entrance_rule(world, "SAWBLADES (Episode 3) @ Base Requirements", lambda state, dps1=dps_mixed, armor=wanted_armor:
          has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 2)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-4))

    # Blue Sawblade: 60
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 60) / 4.1, passive=scale_health(difficulty, 2) * 6)
    logic_location_rule(world, "SAWBLADES (Episode 3) - Waving Sawblade", lambda state, dps1=dps_mixed:
        can_deal_damage(state, world.player, dps1, energy_adjust=-4))


# =================================================================================================
# CAMANIS (Episode 3) - 6 locations
# =================================================================================================
def rules_e3_camanis(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 8, 8, 6), hard_contact=(11, 10, 9, 7))
    wanted_energy = get_logic_difficulty_choice(world, base=(3, 3, 2, 2))
    dps_mixed = world.damage_tables.make_dps(active=12.0, passive=16.0)
    logic_entrance_rule(world, "CAMANIS (Episode 3) @ Base Requirements", lambda state, dps1=dps_mixed, armor=wanted_armor, energy=wanted_energy:
          has_armor_level(state, world.player, armor)
          and has_power_level(state, world.player, 3)
          and has_generator_level(state, world.player, energy)
          and can_deal_damage(state, world.player, dps1))

    dps_mixed = world.damage_tables.make_dps(active=(254 * 1.6) / 20.0, passive=16.0)

    def boss_destroy_rule(state, dps1=dps_mixed):
        return can_deal_damage(state, world.player, dps1)
    # Empty timeout rule, passive DPS requirements covered by base requirements already

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "CAMANIS (Episode 3) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "CAMANIS (Episode 3) - Boss", boss_destroy_rule)


# =================================================================================================
# MACES (Episode 3) - 5 locations
# =================================================================================================
def rules_e3_maces(world: "TyrianWorld", difficulty: int) -> None:
    pass  # Logicless - purely a test of dodging skill


# =================================================================================================
# TYRIAN X (Episode 3) - 8 locations
# =================================================================================================
def rules_e3_tyrian_x(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "TYRIAN X (Episode 3) - First U-Ship Secret")
        logic_location_exclude(world, "TYRIAN X (Episode 3) - Second Secret, Same as the First")
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "TYRIAN X (Episode 3) - Tank Turn-and-fire Secret")

    wanted_armor = get_logic_difficulty_choice(world, base=(6, 6, 5, 5))
    logic_entrance_rule(world, "TYRIAN X (Episode 3) @ Base Requirements", lambda state, armor=wanted_armor:
          has_repulsor(state, world.player)
          or has_armor_level(state, world.player, armor))

    # Spinners: 6 (difficulty +1 due to level)
    # Because this level goes to difficulty 9(!) on Lord of the Game, DPS kinda breaks down a bit.
    # (8x enemy health is frankly absurd.)
    enemy_health = scale_health(difficulty + 1, 6)
    dps_active = world.damage_tables.make_dps(active=(enemy_health * 6) / 1.4)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 1.4)
    logic_location_rule(world, "TYRIAN X (Episode 3) - Platform Spinner Sequence", lambda state, dps1=dps_piercing, dps2=dps_active:
          has_specific_loadout(state, world.player, front_weapon=("Atomic RailGun", 11), rear_weapon=("Banana Blast (Rear)", 11))
          or can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Tanks: 10 (difficulty +1 due to level); purple structures: 6 (same)
    structure_health = scale_health(difficulty + 1, 6) * 3  # Purple structure
    enemy_health = scale_health(difficulty + 1, 10)  # Tank
    dps_active = world.damage_tables.make_dps(active=(structure_health + enemy_health) / 1.25)
    dps_piercing = world.damage_tables.make_dps(piercing=enemy_health / 1.25)
    logic_entrance_rule(world, "TYRIAN X (Episode 3) @ Tanks Behind Structures", lambda state, dps1=dps_piercing, dps2=dps_active:
          has_specific_loadout(state, world.player, front_weapon=("Atomic RailGun", 11), rear_weapon=("Banana Blast (Rear)", 11))
          or can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # The boss is almost identical to its appearance in Tyrian, so the conditions are the similar.
    # Only the wing's health has changed (254, instead of scaled 100)
    dps_active = world.damage_tables.make_dps(active=508 / 30.0)
    dps_piercing = world.damage_tables.make_dps(piercing=254 / 30.0)

    def boss_destroy_rule(state, dps1=dps_piercing, dps2=dps_active):
        return (can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))
    # Empty timeout rule, base requirements are high enough already

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "TYRIAN X (Episode 3) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "TYRIAN X (Episode 3) - Boss", boss_destroy_rule)


# =================================================================================================
# SAVARA Y (Episode 3) - 7 locations
# =================================================================================================
def rules_e3_savara_y(world: "TyrianWorld", difficulty: int) -> None:
    # Blimp: 70
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 70) / 3.6)
    # On Master, you're expected to know how to dodge this when enemies are blocking the entire screen.
    # Otherwise, we should make you can blow up the blimp.
    if world.options.logic_difficulty <= LogicDifficulty.option_expert:
        logic_entrance_rule(world, "SAVARA Y (Episode 3) @ Through Blimp Blockade", lambda state, dps1=dps_active:
              has_invulnerability(state, world.player)
              or can_deal_damage(state, world.player, dps1))

    dps_active = world.damage_tables.make_dps(active=254 / 4.4)
    logic_location_rule(world, "SAVARA Y (Episode 3) - Boss Ship Fly-By", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Vulcan planes with items: 14
    # As in Episode 1, prefer kills with passive
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 14) / 1.6)
    dps_passive = world.damage_tables.make_dps(passive=scale_health(difficulty, 14) / 2.4)
    logic_location_rule(world, "SAVARA Y (Episode 3) - Vulcan Plane Set", lambda state, dps1=dps_passive, dps2=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 14) / 1.2)
    logic_entrance_rule(world, "SAVARA Y (Episode 3) @ Death Plane Set", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Same boss as Episode 1 Savaras; here, though, the boss here has no patience and leaves VERY fast
    boss_health = 254 + (scale_health(difficulty, 6) * 15) + (scale_health(difficulty, 10) * 4)
    dps_active = world.damage_tables.make_dps(active=boss_health / 13.0)
    dps_tick = world.damage_tables.make_dps(sideways=scale_health(difficulty, 6) / 1.2)

    def boss_destroy_rule(state, dps1=dps_active):
        return can_deal_damage(state, world.player, dps1)
    # Also need enough damage to destroy things the boss shoots at you, when dodging isn't an option
    def boss_timeout_rule(state, dps2=dps_tick, base_rule=boss_destroy_rule):
        return (has_invulnerability(state, world.player)
              or can_deal_damage(state, world.player, dps2)
              or base_rule(state))

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "SAVARA Y (Episode 3) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "SAVARA Y (Episode 3) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "SAVARA Y (Episode 3) - Boss", boss_destroy_rule)


# =================================================================================================
# NEW DELI (Episode 3) - 7 locations
# =================================================================================================
def rules_e3_new_deli(world: "TyrianWorld", difficulty: int) -> None:
    # Turrets: 10
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 10) / 1.8)
    wanted_armor = get_logic_difficulty_choice(world, base=(12, 12, 11, 9))
    logic_entrance_rule(world, "NEW DELI (Episode 3) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_active:
          (
              has_repulsor(state, world.player)
              and has_armor_level(state, world.player, armor - 3)
              and has_generator_level(state, world.player, 3)
              and has_power_level(state, world.player, 4)
              and can_deal_damage(state, world.player, dps1)
          ) or (
              has_armor_level(state, world.player, armor)
              and has_generator_level(state, world.player, 4)
              and has_power_level(state, world.player, 4)
              and can_deal_damage(state, world.player, dps1)
          ))

    # Repulsor orbs: 80
    # One pops up on the screen during all this mess. Getting it OFF the screen quickly is the goal here.
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 80) / 5.0)
    logic_entrance_rule(world, "NEW DELI (Episode 3) @ The Gauntlet Begins", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Same boss as DELIANI (Episode 1), copied from there.
    # Repulsor orbs: 80; boss: 200
    boss_health = (scale_health(difficulty, 80) * 3) + scale_health(difficulty, 200)
    dps_active = world.damage_tables.make_dps(active=boss_health / 22.0)
    logic_entrance_rule(world, "NEW DELI (Episode 3) @ Destroy Boss", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# FLEET (Episode 3) - 5 locations, goal level
# =================================================================================================
def rules_e3_fleet(world: "TyrianWorld", difficulty: int) -> None:
    # Item ships: 20 -- These flee quickly; and using them to lock off the entire level is convenient
    wanted_armor = get_logic_difficulty_choice(world, base=(11, 10, 10, 7), hard_contact=(13, 12, 11, 9))
    wanted_energy = get_logic_difficulty_choice(world, base=(4, 4, 3, 3), hard_contact=(4, 4, 4, 3))
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 1.5)
    logic_entrance_rule(world, "FLEET (Episode 3) @ Base Requirements", lambda state, dps1=dps_active, armor=wanted_armor, energy=wanted_energy:
          has_power_level(state, world.player, 6)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, energy)
          and can_deal_damage(state, world.player, dps1))

    # Attractor crane: 50; arms are invulnerable, damage that can be dealt to it is limited
    # Piercing option is always available for both attractor cranes
    # If you have invulnerability, you can also use that to pierce briefly.
    dps_pierceopt = world.damage_tables.make_dps(piercing=scale_health(difficulty, 50) / 10.0)
    dps_invulnopt = world.damage_tables.make_dps(active=scale_health(difficulty, 50) / 3.0)
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 50) / 1.4)

    def crane_destroy_rule(state, dps1=dps_pierceopt, dps2=dps_invulnopt, dps3=dps_active):
        return (can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2 if has_invulnerability(state, world.player) else dps3))

    if world.options.logic_difficulty == LogicDifficulty.option_master:
        # You have invulnerability at the start of the level. Exploit it.
        logic_location_rule(world, "FLEET (Episode 3) - Attractor Crane, Entrance", lambda state, dps1=dps_pierceopt, dps2=dps_invulnopt:
              can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))
    else:
        logic_location_rule(world, "FLEET (Episode 3) - Attractor Crane, Entrance", crane_destroy_rule)
    logic_location_rule(world, "FLEET (Episode 3) - Attractor Crane, Mid-Fleet", crane_destroy_rule)

    # This boss regularly heals, spams enemies across the screen, etc...
    dps_active = world.damage_tables.make_dps(active=(254 * 1.5) / 8.0)
    logic_entrance_rule(world, "FLEET (Episode 3) @ Destroy Boss", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# -------------------------------------------------------------------------------------------------
# Grand total for Episode 3: 81 locations across 12 levels
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# =================================================================================================
#                                    EPISODE 4 (AN END TO FATE)
# =================================================================================================
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# SURFACE (Episode 4) - 8 locations
# =================================================================================================
def rules_e4_surface(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "SURFACE (Episode 4) - Secret Orb Wheel")

    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5))
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 2.4)
    logic_entrance_rule(world, "SURFACE (Episode 4) @ Destroy Mid-Boss", lambda state, armor=wanted_armor, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # We nerfed this orb wheel hard (it no longer fires), and it still hurts a lot.
    # We need a good loadout to handle everything going on while we try to destroy it.
    wanted_armor = get_logic_difficulty_choice(world, base=(14, 12, 11, 10))
    dps_active = world.damage_tables.make_dps(active=254 / 4.6, passive=scale_health(difficulty + 1, 20) / 1.2)
    logic_location_rule(world, "SURFACE (Episode 4) - Secret Orb Wheel", lambda state, armor=wanted_armor, dps1=dps_active:
          has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 4)
          and has_power_level(state, world.player, 5)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-4))

    # Hands: 150 (difficulty + 1 at this point in the level)
    # Boss Lightning Gun: Fixed 254
    # Interestingly, the thing that keeps you in place here is not the lightning gun, but the hands.
    # So if you can destroy both with sideways, you can finish the level without getting the item.
    # If you're doing that, we assume cheap shots on them are going to be taken with active before they're in place.
    dps_boss = world.damage_tables.make_dps(active=254 / 10.0)
    dps_hands = world.damage_tables.make_dps(active=80 / 6.0, sideways=((scale_health(difficulty + 1, 150) * 2) - 80) / 15.0)
    logic_entrance_rule(world, "SURFACE (Episode 4) @ Destroy Hands or Boss", lambda state, dps1=dps_boss, dps2=dps_hands:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))
    logic_location_rule(world, "SURFACE (Episode 4) - Boss", lambda state, dps1=dps_boss:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# WINDY (Episode 4) - 5 locations
# =================================================================================================
def rules_e4_windy(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        logic_location_exclude(world, "WINDY (Episode 4) - Extra Section, Start")
        logic_location_exclude(world, "WINDY (Episode 4) - Extra Section, End")

    # Regular block: 10 -- No armor requirement to fly through because nothing shoots at you.
    # Just need to either be able to break through some lines of solid blocks, or Invulnerability past.
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 10) / 1.4)
    logic_entrance_rule(world, "WINDY (Episode 4) @ Fly Through", lambda state, dps1=dps_active:
          has_invulnerability(state, world.player)
          or can_deal_damage(state, world.player, dps1))

    # Special blocks: 20 (chevrons for secret area, and question marks for items)
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 1.4)
    logic_entrance_rule(world, "WINDY (Episode 4) @ Destroy Blocks", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # To get to the Extra section, you need to break all the chevron blocks.
    # Two of the necessary blocks have some cover in front of them, and are right next to each other, so logically we
    # want either enough active to knock out both rapidly, or to defeat one with active and one with passive.
    # Guaranteeing we can get those should be enough to get all of them.
    dps_option1 = world.damage_tables.make_dps(active=(scale_health(difficulty, 20) * 2) / 0.7)
    dps_option2 = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 1.0, passive=scale_health(difficulty, 20) / 0.7)
    logic_entrance_rule(world, "WINDY (Episode 4) @ Reach Extra Section", lambda state, dps1=dps_option1, dps2=dps_option2:
          can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer", "Wild Ball", "Fireball"])
          or can_deal_damage(state, world.player, dps2, exclude=["The Orange Juicer", "Wild Ball", "Fireball"]))


# =================================================================================================
# LAVA RUN (Episode 4) - 5 locations
# =================================================================================================
def rules_e4_lava_run(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5), hard_contact=(10, 9, 9, 8))
    if difficulty >= 4:  # Impossible or above
        wanted_armor = get_logic_difficulty_choice(world, base=(9, 8, 7, 5), hard_contact=(11, 11, 10, 8))

    # The difficulty of this level changes drastically with this option, so we have an alternate set of rules for it.
    if world.options.contact_bypasses_shields:
        dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 3.5, sideways=scale_health(difficulty, 6) / 1.2)
        logic_entrance_rule(world, "LAVA RUN (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
              has_armor_level(state, world.player, (armor - 2) if has_invulnerability(state, world.player) else armor)
              and can_deal_damage(state, world.player, dps1, energy_adjust=-3))

        # Laser turret: 30
        # Prefer killing the laser turret with passive, if possible.
        dps_option1 = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 3.5, sideways=scale_health(difficulty, 6) / 1.2, passive=scale_health(difficulty, 30) / 2.5)
        dps_option2 = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 1.5, sideways=scale_health(difficulty, 6) / 1.2)
        logic_location_rule(world, "LAVA RUN (Episode 4) - Laser Turret", lambda state, dps1=dps_option1, dps2=dps_option2:
              can_deal_damage(state, world.player, dps1, energy_adjust=-3)
              or can_deal_damage(state, world.player, dps2, energy_adjust=-3))

        # Option 1 requires invulnerability, option 2 expects the boss to be dead sooner.
        dps_option1 = world.damage_tables.make_dps(active=254 / 14.0, sideways=scale_health(difficulty, 6) / 1.2)
        dps_option2 = world.damage_tables.make_dps(active=254 / 8.5, sideways=scale_health(difficulty, 6) / 1.2)
        def boss_destroy_rule(state, dps1=dps_option1, dps2=dps_option2):
            return can_deal_damage(state, world.player, dps1 if has_invulnerability(state, world.player) else dps2, energy_adjust=-3)
        def boss_timeout_rule(state, base_rule=boss_destroy_rule):
            return (has_invulnerability(state, world.player)
                  or base_rule(state))

        if not world.options.logic_boss_timeout:
            logic_entrance_rule(world, "LAVA RUN (Episode 4) @ Pass Boss (can time out)", boss_destroy_rule)
        else:
            logic_entrance_rule(world, "LAVA RUN (Episode 4) @ Pass Boss (can time out)", boss_timeout_rule)
            logic_location_rule(world, "LAVA RUN (Episode 4) - Boss", boss_destroy_rule)

    # And now for the regular variant of the rules. They're tamer by comparison.
    else:
        dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 3.7, passive=scale_health(difficulty, 6) / 0.8)
        logic_entrance_rule(world, "LAVA RUN (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
              has_armor_level(state, world.player, armor)
              and can_deal_damage(state, world.player, dps1, energy_adjust=-3))

        # Laser turret: 30
        # Prefer killing the laser turret with passive, if possible.
        dps_option1 = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 3.7, passive=scale_health(difficulty, 30) / 2.7)
        dps_option2 = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 1.8, passive=scale_health(difficulty, 6) / 0.8)
        logic_location_rule(world, "LAVA RUN (Episode 4) - Laser Turret", lambda state, dps1=dps_option1, dps2=dps_option2:
              can_deal_damage(state, world.player, dps1, energy_adjust=-3)
              or can_deal_damage(state, world.player, dps2, energy_adjust=-3))

        dps_mixed = world.damage_tables.make_dps(active=254 / 14.0, passive=scale_health(difficulty, 6) / 0.8)
        def boss_destroy_rule_easy(state, dps1=dps_mixed):
            return can_deal_damage(state, world.player, dps1, energy_adjust=-3)
        # Empty timeout rule

        if not world.options.logic_boss_timeout:
            logic_entrance_rule(world, "LAVA RUN (Episode 4) @ Pass Boss (can time out)", boss_destroy_rule_easy)
        else:
            logic_location_rule(world, "LAVA RUN (Episode 4) - Boss", boss_destroy_rule_easy)


# =================================================================================================
# CORE (Episode 4) - 7 locations
# =================================================================================================
def rules_e4_core(world: "TyrianWorld", difficulty: int) -> None:
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 6) / 0.95)
    logic_entrance_rule(world, "CORE (Episode 4) @ Starting Section", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))

    # Core flames: 10; many, *many* of these get spawned
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 8, 7, 5), hard_contact=(13, 12, 10, 8))
    dps_mixed = world.damage_tables.make_dps(active=(scale_health(difficulty, 10) * 2) / 1.3, passive=(scale_health(difficulty, 10) * 3) / 1.3)
    logic_entrance_rule(world, "CORE (Episode 4) @ Critical Core", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 2)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-3))

    # Core boss: 254, heals twice mid-fight. Due to the sheer amount of bullets being fired at you,
    # staying in position to hit the boss is difficult without the repulsor.
    # While this boss can be timed out, doing so results in a special "mission failure" exit;
    # this does NOT count as completing the level, so defeating the boss is mandatory.
    dps_boss_norepulse = world.damage_tables.make_dps(active=254 / 6.4, passive=(scale_health(difficulty, 10) * 3) / 1.3)
    dps_boss_repulse = world.damage_tables.make_dps(active=254 / 10.0, passive=(scale_health(difficulty, 10) * 3) / 1.3)
    logic_entrance_rule(world, "CORE (Episode 4) @ Destroy Boss", lambda state, dps1=dps_boss_norepulse, dps2=dps_boss_repulse:
          can_deal_damage(state, world.player, dps2 if has_repulsor(state, world.player) else dps1, energy_adjust=-2, exclude=["The Orange Juicer"]))


# =================================================================================================
# LAVA EXIT (Episode 4) - 6 locations
# =================================================================================================
def rules_e4_lava_exit(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(8, 7, 6, 0), hard_contact=(9, 8, 6, 0))
    if difficulty >= 8:  # Lord of the Game (super fast firing)
        wanted_armor += 2

    # On beginner, we add in an extra damage requirement to clear out lava bubbles, instead of expecting some dodging.
    # This will also likely give Beginner logic most of the damage requirements for checks for free, too
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 10) * 5) / 3.8)
        logic_entrance_rule(world, "LAVA EXIT (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_active:
              has_armor_level(state, world.player, armor)
              and can_deal_damage(state, world.player, dps1))
    else:
        logic_entrance_rule(world, "LAVA EXIT (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor:
              has_armor_level(state, world.player, armor))

    # Lightning Turret: 4, guarded by bubbles.
    # Fun fact, the turret with the item is actually two overlapping turrets, linked together. Doesn't affect damage.
    dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 4) + scale_health(difficulty, 10)) / 1.0)
    logic_location_rule(world, "LAVA EXIT (Episode 4) - Central Lightning Turret", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Collective rule for the four item drops with fixed (non-difficulty adjusted) health
    # Orb wheel weakspots have 40, but stay for a while. Final lava bubbles have 20 but don't stay as long.
    # So in the end, they both require about the same level of DPS.
    dps_active = world.damage_tables.make_dps(active=40 / 3.0)
    logic_entrance_rule(world, "LAVA EXIT (Episode 4) @ Items with Fixed Health", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Boss has fixed 254 health, constantly fires shots of lava with scaled 10 health
    dps_boss = world.damage_tables.make_dps(active=(254 + scale_health(difficulty, 10) * 8) / 16.0)

    def boss_destroy_rule(state, dps1=dps_boss):
        return can_deal_damage(state, world.player, dps1)
    # No timeout rule -- Boss can be trivially timed out pacifist damageless.

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "LAVA EXIT (Episode 4) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "LAVA EXIT (Episode 4) - Boss", boss_destroy_rule)


# =================================================================================================
# DESERTRUN (Episode 4) - 6 locations
# =================================================================================================
def rules_e4_desertrun(world: "TyrianWorld", difficulty: int) -> None:
    # Simple fly through but a lot of things shoot bullets at you.
    # No need to destroy anything, so no damage requirements.
    wanted_armor = get_logic_difficulty_choice(world, base=(6, 5, 4, 3))
    if difficulty >= 8:  # Lord of the Game (super fast firing)
        wanted_armor += 5
    elif difficulty >= 3:  # Hard or above (fast firing)
        wanted_armor += 2

    logic_entrance_rule(world, "DESERTRUN (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor:
          has_repulsor(state, world.player)
          or has_invulnerability(state, world.player)
          or has_armor_level(state, world.player, armor))


# =================================================================================================
# SIDE EXIT (Episode 4) - 3 locations
# =================================================================================================
def rules_e4_side_exit(world: "TyrianWorld", difficulty: int) -> None:
    # Homing lava bubbles: 254, Laser turret: 30
    # We still want to kill the turrets passively, and this level makes a whole lot of them
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5), hard_contact=(8, 7, 7, 5))
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 254) / 15.0, passive=scale_health(difficulty, 30) / 2.5)
    logic_entrance_rule(world, "SIDE EXIT (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
          (
              has_invulnerability(state, world.player)
              or has_armor_level(state, world.player, armor)
          )
          and can_deal_damage(state, world.player, dps1))


# =================================================================================================
# ?TUNNEL? (Episode 4) - 1 location
# =================================================================================================
def rules_e4_qtunnelq(world: "TyrianWorld", difficulty: int) -> None:
    # This stage is a simple timed boss with a fixed HP pool of 762.
    # We fudge the numbers a bit to compensate for the boss's extremely erratic movement in phase 2.
    # Though this boss can be timed out, doing so also results in a "mission failure" exit.
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 9, 8, 6), hard_contact=(10, 10, 8, 6))
    dps_boss = world.damage_tables.make_dps(active=(762 * 1.25) / 40.0)
    logic_entrance_rule(world, "?TUNNEL? (Episode 4) @ Destroy Boss", lambda state, dps1=dps_boss, armor=wanted_armor:
          has_power_level(state, world.player, 5)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 4)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-2))


# =================================================================================================
# ICE EXIT (Episode 4) - 4 locations
# =================================================================================================
def rules_e4_ice_exit(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(8, 8, 7, 5), hard_contact=(10, 10, 9, 7))
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 1.0, passive=(scale_health(difficulty, 15) * 2) / 1.6)
    logic_entrance_rule(world, "ICE EXIT (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 2)
          and can_deal_damage(state, world.player, dps1))

    # Boss has 254 health unscaled, lava bubble friends have 254 scaled. There's two, but...
    # realistically, however? The lava bubbles are going to soak up a bunch of that passive damage.
    dps_boss = world.damage_tables.make_dps(active=(254 + (scale_health(difficulty, 254) * 1.2)) / 24.0, passive=(scale_health(difficulty, 15) * 2) / 1.6)
    logic_entrance_rule(world, "ICE EXIT (Episode 4) @ Destroy Boss", lambda state, dps1=dps_boss:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# ICESECRET (Episode 4) - 9 locations
# =================================================================================================
def rules_e4_icesecret(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(10, 9, 8, 6), hard_contact=(11, 10, 9, 7))
    wanted_energy = get_logic_difficulty_choice(world, base=(3, 3, 2, 2))

    # The amount of time we spend at the mid-boss directly determines how far we can go into the level
    # and what we can accomplish. It has fixed 254 health, and two bubbles that hover around you with the same health.
    # The bubbles are only a minor annoyance since they don't make contact with you, but we compensate for the
    # shots that they eat up in a time-sensitive battle.
    dps_timegate1 = world.damage_tables.make_dps(active=(254 * 1.25) / 19.0)  # Basic weapons -- Pulse-Cannon:5
    dps_timegate2 = world.damage_tables.make_dps(active=(254 * 1.25) / 9.5)  # Mid-tier weapons -- Protron Z:6
    dps_timegate3 = world.damage_tables.make_dps(active=(254 * 1.25) / 6.0)  # High-end weapons -- Atomic RailGun:3

    logic_entrance_rule(world, "ICESECRET (Episode 4) @ Time Gate, To Station Start", lambda state, energy=wanted_energy, armor=wanted_armor, dps1=dps_timegate1:
          has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, wanted_energy)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-3))
    logic_entrance_rule(world, "ICESECRET (Episode 4) @ Time Gate, To Midpoint", lambda state, energy=wanted_energy, dps2=dps_timegate2:
          has_generator_level(state, world.player, wanted_energy + 1)
          and can_deal_damage(state, world.player, dps2, energy_adjust=-3))
    logic_entrance_rule(world, "ICESECRET (Episode 4) @ Time Gate, To Ending", lambda state, energy=wanted_energy, dps3=dps_timegate3:
          has_generator_level(state, world.player, wanted_energy + 2)
          and can_deal_damage(state, world.player, dps3, energy_adjust=-3))

    # Ice blocks: 15
    # This one falls really fast, so need additional DPS to get it despite being early
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 0.7)
    logic_location_rule(world, "ICESECRET (Episode 4) - Ice Block, After Mid-Boss", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# HARVEST (Episode 4) - 10 locations
# =================================================================================================
def rules_e4_harvest(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(8, 8, 7, 6))
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 1.6)
    logic_entrance_rule(world, "HARVEST (Episode 4) @ Base Requirements", lambda state, dps1=dps_active, armor=wanted_armor:
          has_power_level(state, world.player, 3)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 2)
          and can_deal_damage(state, world.player, dps1))

    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 0.8)
    logic_location_rule(world, "HARVEST (Episode 4) - V Formation, High Speed", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Energy Blasters: 40
    # Basically every time they show up with an item, they're blocked by a bunch of enemies, so we compensate for that
    dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 40) + (scale_health(difficulty, 15) * 3)) / 4.7)
    logic_entrance_rule(world, "HARVEST (Episode 4) @ Destroy Energy Blasters", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Not quite the same boss as DELIANI / NEW DELI.
    # Has more health, plus exploding bubbles continue to spawn through the entire fight.
    dps_mixed = world.damage_tables.make_dps(active=(254 * 1.5) / 22.0, passive=scale_health(difficulty, 15) / 1.2)
    logic_entrance_rule(world, "HARVEST (Episode 4) @ Destroy Boss", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))


# =================================================================================================
# UNDERDELI (Episode 4) - 8 locations
# =================================================================================================
def rules_e4_underdeli(world: "TyrianWorld", difficulty: int) -> None:
    # The requirements are so high for this level because the semi-homing missiles absolutely wreck you if you are
    # unprepared for them, and frequently the platforms launching them are blocked by other ground objects.
    # This is like, the one level where I think I'd prefer a good piercing weapon over *anything* else.
    # ... But, piercing doesn't go high enough in Lord of the Game, essentially requiring a god-tier loadout.
    wanted_armor_no_inv = get_logic_difficulty_choice(world, base=(10, 9, 9, 7), hard_contact=(13, 12, 12, 10))
    wanted_armor_inv = get_logic_difficulty_choice(world, base=(9, 8, 8, 6), hard_contact=(11, 10, 9, 7))
    dps_normalopt = world.damage_tables.make_dps(active=(scale_health(difficulty, 50) + scale_health(difficulty, 30)) / 2.8, sideways=(scale_health(difficulty, 3) * 5) / 1.2)
    dps_pierceopt = world.damage_tables.make_dps(piercing=scale_health(difficulty, 50) / 2.8, sideways=(scale_health(difficulty, 3) * 5) / 1.2)
    logic_entrance_rule(world, "UNDERDELI (Episode 4) @ Base Requirements", lambda state, armor1=wanted_armor_no_inv, armor2=wanted_armor_inv, dps1=dps_normalopt, dps2=dps_pierceopt:
          has_power_level(state, world.player, 5)
          and has_generator_level(state, world.player, 3)
          and has_armor_level(state, world.player, armor2 if has_invulnerability(state, world.player) else armor1)
          and
          (
              has_specific_loadout(state, world.player, front_weapon=("Atomic RailGun", 11), rear_weapon=("Mega Pulse (Rear)", 11))
              or can_deal_damage(state, world.player, dps2)
              or can_deal_damage(state, world.player, dps1)
          ))

    # We're primarily concerned with phase 2, where you need to hit a small target on the boss immediately after
    # it attacks. Piercing can just hit the target at any time, trivializing the phase.
    # All phases of this boss can be timed out, although it takes some time to do so.
    dps_normalopt = world.damage_tables.make_dps(active=(254 / 6.0), sideways=(scale_health(difficulty, 3) * 5) / 1.2)
    # dps_pierceopt remains unchanged from above

    def boss_destroy_rule(state, dps1=dps_normalopt, dps2=dps_pierceopt):
        return (has_specific_loadout(state, world.player, front_weapon=("Atomic RailGun", 11), rear_weapon=("Mega Pulse (Rear)", 11))
              or can_deal_damage(state, world.player, dps2)
              or can_deal_damage(state, world.player, dps1))
    # Empty timeout rule, base requirements exceed anything necessary already

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "UNDERDELI (Episode 4) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "UNDERDELI (Episode 4) - Boss", boss_destroy_rule)


# =================================================================================================
# APPROACH (Episode 4) - 5 locations
# =================================================================================================
def rules_e4_approach(world: "TyrianWorld", difficulty: int) -> None:
    # Comparatively easy for its placement in the game, just needs a relatively basic loadout.
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 6) / 0.8, passive=scale_health(difficulty, 6) / 0.8)
    logic_entrance_rule(world, "APPROACH (Episode 4) @ Base Requirements", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))

    wanted_armor = get_logic_difficulty_choice(world, base=(6, 6, 5, 5))
    dps_mixed = world.damage_tables.make_dps(active=(254 / 16.0), passive=scale_health(difficulty, 6) / 0.8)
    logic_entrance_rule(world, "APPROACH (Episode 4) @ Destroy Boss Orb", lambda state, dps1=dps_mixed, armor=wanted_armor:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1))


# =================================================================================================
# SAVARA IV (Episode 4) - 5 locations
# =================================================================================================
def rules_e4_savara_iv(world: "TyrianWorld", difficulty: int) -> None:
    # Drunk planes: 80 (center) / 40 (wings). However they fly erratically... hence their name.
    # So we figure you're not going to be reliably hitting just one wing, and probably hitting the center a good deal.
    dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 40) * 2.5) / 5.5)
    logic_entrance_rule(world, "SAVARA IV (Episode 4) @ Destroy Drunk Planes", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    # Aaaaand here's the actual problem point. The boss for Savara IV has a significantly more aggressive pattern than
    # any of the other Savara levels, and also is immune to attacks from the front, necessitating pierce or sideways.
    # We also need to be able to shoot down the spinners that it creates a ton of, otherwise they kill very fast.
    # Those have 6 health each.
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 8, 7, 6), hard_contact=(12, 11, 11, 9))
    dps_option1 = world.damage_tables.make_dps(piercing=(254 + (scale_health(difficulty, 6) * 10)) / 20.0, passive=(scale_health(difficulty, 6) * 3) / 0.9)
    dps_option2 = world.damage_tables.make_dps(sideways=254 / 9.0, passive=(scale_health(difficulty, 6) * 3) / 0.9)
    dps_safety = world.damage_tables.make_dps(active=scale_health(difficulty, 40) / 2.8, passive=(scale_health(difficulty, 6) * 3) / 0.9)

    def stat_requirement_rule(state, armor=wanted_armor):
        return (has_generator_level(state, world.player, 3)
              and has_armor_level(state, world.player, (armor - 2) if has_invulnerability(state, world.player) else armor))
    def boss_destroy_rule(state, stat_rule=stat_requirement_rule, dps1=dps_option1, dps2=dps_option2):
        return (stat_rule(state)
              and (
                  can_deal_damage(state, world.player, dps1)
                  or can_deal_damage(state, world.player, dps2, exclude=["The Orange Juicer"])
              ))
    def boss_timeout_rule(state, stat_rule=stat_requirement_rule, dps3=dps_safety):
        return (stat_rule(state)
              and can_deal_damage(state, world.player, dps3))

    # Alright, but here's the deal: If you can time the boss out, you can get SuperBombs from a really late enemy
    # and use that to destroy it. On Master logic, we expect that at all times.
    if world.options.logic_difficulty == LogicDifficulty.option_master:
        logic_entrance_rule(world, "SAVARA IV (Episode 4) @ Pass Boss (can time out)", boss_timeout_rule)
    elif not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "SAVARA IV (Episode 4) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "SAVARA IV (Episode 4) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "SAVARA IV (Episode 4) - Boss", boss_destroy_rule)


# =================================================================================================
# DREAD-NOT (Episode 4) - 1 location
# =================================================================================================
def rules_e4_dread_not(world: "TyrianWorld", difficulty: int) -> None:
    # This stage is one gigantic boss, with a fixed total HP pool of 2,540.
    # The torpedoes it fires have 20 HP, and the red blood-cell-like enemies have 30 HP, both scaled.
    wanted_power = get_logic_difficulty_choice(world, base=(6, 6, 5, 5))
    wanted_armor = get_logic_difficulty_choice(world, base=(13, 12, 11, 10), hard_contact=(14, 13, 12, 10))
    boss_hp = 2540 + (scale_health(difficulty, 20) * 14) + (scale_health(difficulty, 30) * 18)
    dps_boss = world.damage_tables.make_dps(active=boss_hp/90.0)

    logic_entrance_rule(world, "DREAD-NOT (Episode 4) @ Destroy Boss", lambda state, dps1=dps_boss, armor=wanted_armor, power=wanted_power:
          has_power_level(state, world.player, power)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 4)
          and can_deal_damage(state, world.player, dps1, exclude=["The Orange Juicer", "Shuriken Field"]))


# =================================================================================================
# EYESPY (Episode 4) - 7 locations
# =================================================================================================
def rules_e4_eyespy(world: "TyrianWorld", difficulty: int) -> None:
    if world.options.logic_difficulty == LogicDifficulty.option_beginner:
        logic_location_exclude(world, "EYESPY (Episode 4) - Billiard Break Secret")

    # Lips: 30, Green eyes, 20, Blue eyes: 10 (but have multiple overlapping enemies), small spam eyes: 4
    wanted_power = get_logic_difficulty_choice(world, base=(6, 6, 5, 5))
    wanted_armor = get_logic_difficulty_choice(world, base=(13, 12, 11, 10), hard_contact=(14, 13, 12, 10))
    wanted_passive = (scale_health(difficulty, 4) * 6) / 1.6
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 30) / 1.6, passive=wanted_passive)
    logic_entrance_rule(world, "EYESPY (Episode 4) @ Base Requirements", lambda state, armor=wanted_armor, power=wanted_power, dps1=dps_mixed:
          has_power_level(state, world.player, power)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 4)
          and can_deal_damage(state, world.player, dps1))

    dps_normalopt = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 0.85, passive=wanted_passive)
    dps_pierceopt = world.damage_tables.make_dps(piercing=scale_health(difficulty, 20) / 2.5, passive=wanted_passive)

    # Static eye is almost impossible to damage with active, so requires piercing only
    # NortShip Spreader at max also hits from behind hard enough
    # The Banana Blast isn't strictly necessary, but we need *a* front weapon and it's the least generator expensive
    logic_location_rule(world, "EYESPY (Episode 4) - Guarded Green Eye, Static", lambda state, dps1=dps_pierceopt:
          has_specific_loadout(state, world.player, front_weapon=("Banana Blast (Front)", 11), rear_weapon=("NortShip Spreader", 11))
          or can_deal_damage(state, world.player, dps1))
    logic_location_rule(world, "EYESPY (Episode 4) - Guarded Green Eye, Swaying", lambda state, dps1=dps_pierceopt, dps2=dps_normalopt:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2, exclude=["The Orange Juicer", "Guided Bombs", "Banana Blast (Rear)"]))

    dps_boss = world.damage_tables.make_dps(active=(762 + (scale_health(difficulty, 20) * 4)) / 22.0)
    logic_entrance_rule(world, "EYESPY (Episode 4) @ Destroy Boss", lambda state, dps1=dps_boss:
          can_deal_damage(state, world.player, dps1))

# =================================================================================================
# BRAINIAC (Episode 4) - 9 locations
# =================================================================================================
def rules_e4_brainiac(world: "TyrianWorld", difficulty: int) -> None:
    # Embedded turrets have 28 health, destructible wall segments have 20.
    # Contact does an abnormally high amount of damage in this stage.
    wanted_power = get_logic_difficulty_choice(world, base=(6, 6, 5, 5))
    wanted_armor = get_logic_difficulty_choice(world, base=(13, 13, 12, 10), hard_contact=(14, 13, 12, 10))
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 28) / 1.4, passive=scale_health(difficulty, 20) / 1.4)

    logic_entrance_rule(world, "BRAINIAC (Episode 4) @ Base Requirements", lambda state, dps1=dps_mixed, armor=wanted_armor, power=wanted_power:
          has_power_level(state, world.player, power)
          and has_armor_level(state, world.player, (armor - 1) if has_invulnerability(state, world.player) else armor)
          and has_generator_level(state, world.player, 4)
          and can_deal_damage(state, world.player, dps1))

    # Fire mid-boss: Fixed 254 -- Behaves similarly to the LAVA EXIT boss, except doesn't stay around as long.
    dps_mixed = world.damage_tables.make_dps(active=(254 + scale_health(difficulty, 10) * 6) / 13.0, passive=scale_health(difficulty, 20) / 1.4)
    logic_location_rule(world, "BRAINIAC (Episode 4) - Fire Mid-Boss", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))

    # Orb wheel weakpoint: Fixed 100
    dps_mixed = world.damage_tables.make_dps(active=100 / 4.0, passive=scale_health(difficulty, 20) / 1.4)
    logic_location_rule(world, "BRAINIAC (Episode 4) - Rolling Orb Wheel", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))

    # Ice mid-boss: Fixed 100 -- Hangs out at the bottom of the screen.
    # Either we use sideways DPS and swoop in to get the item, or we just overpower it before it gets to the bottom.
    dps_option1 = world.damage_tables.make_dps(active=100 / 2.8, passive=scale_health(difficulty, 20) / 1.4)
    dps_option2 = world.damage_tables.make_dps(active=scale_health(difficulty, 28) / 1.4, passive=scale_health(difficulty, 20) / 1.4, sideways=100 / 9.8)
    logic_location_rule(world, "BRAINIAC (Episode 4) - Ice Mid-Boss", lambda state, dps1=dps_option1, dps2=dps_option2:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2))

    # Brain boss: Fixed 254, guarded by close to 30(!) cells with scaled 254 health.
    # Destroying about eight of them is good enough to make a hole to hit the boss with, or we could just pierce.
    # Note that the cells have difficulty-1 modifier, but we still want the unmodified difficulty for passive.
    dps_option1 = world.damage_tables.make_dps(piercing=254 / 15.0, passive=scale_health(difficulty, 20) / 1.4)
    dps_option2 = world.damage_tables.make_dps(active=(254 + (scale_health(difficulty - 1, 254) * 8)) / 55.0, passive=scale_health(difficulty, 20) / 1.4)
    dps_master = world.damage_tables.make_dps(active=254 / 9.0, passive=scale_health(difficulty, 20) / 1.4)

    if world.options.logic_difficulty == LogicDifficulty.option_master:
        # Or... if you have invulnerability, you can use it to "pierce" anyway.
        # We restrict this to master because using it like this implies NOT using it to dodge everything coming at you
        logic_entrance_rule(world, "BRAINIAC (Episode 4) @ Destroy Boss", lambda state, dps1=dps_option1, dps2=dps_option2, dps3=dps_master:
              can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps3 if has_invulnerability(state, world.player) else dps2))
    else:
        logic_entrance_rule(world, "BRAINIAC (Episode 4) @ Destroy Boss", lambda state, dps1=dps_option1, dps2=dps_option2:
              can_deal_damage(state, world.player, dps1)
              or can_deal_damage(state, world.player, dps2))


# =================================================================================================
# NOSE DRIP (Episode 4) - 1 location, goal level
# =================================================================================================
def rules_e4_nose_drip(world: "TyrianWorld", difficulty: int) -> None:
    # This stage is another gigantic boss with a fixed total HP pool of 1,524.
    wanted_power = get_logic_difficulty_choice(world, base=(7, 7, 7, 6))
    wanted_armor = get_logic_difficulty_choice(world, base=(14, 13, 12, 10))
    dps_boss = world.damage_tables.make_dps(active=1524 / 32.0)

    logic_entrance_rule(world, "NOSE DRIP (Episode 4) @ Destroy Boss", lambda state, dps1=dps_boss, armor=wanted_armor, power=wanted_power:
          has_power_level(state, world.player, power)
          and has_armor_level(state, world.player, armor)
          and has_generator_level(state, world.player, 5)
          and can_deal_damage(state, world.player, dps1))


# -------------------------------------------------------------------------------------------------
# Grand total for Episode 4: 100 locations across 18 levels
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# =================================================================================================
#                                    EPISODE 5 (HAZUDRA FODDER)
# =================================================================================================
# -------------------------------------------------------------------------------------------------


# =================================================================================================
# ASTEROIDS (Episode 5) - 8 locations
# =================================================================================================
def rules_e5_asteroids(world: "TyrianWorld", difficulty: int) -> None:
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 2.2)
    logic_entrance_rule(world, "ASTEROIDS (Episode 5) @ Destroy Spinning Orbs", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1))

    dps_boss = world.damage_tables.make_dps(active=scale_health(difficulty, 200) / 15.0)
    wanted_armor = get_logic_difficulty_choice(world, base=(6, 6, 5, 4))
    if difficulty >= 4:  # Impossible or above
        wanted_armor += 1

    logic_entrance_rule(world, "ASTEROIDS (Episode 5) @ Destroy Boss", lambda state, armor=wanted_armor, dps1=dps_boss:
          has_armor_level(state, world.player, (armor - 1) if has_repulsor(state, world.player) else armor)
          and can_deal_damage(state, world.player, dps1))


# =================================================================================================
# AST ROCK (Episode 5) - 9 locations
# =================================================================================================
def rules_e5_ast_rock(world: "TyrianWorld", difficulty: int) -> None:
    # This level is just inherently difficult to write logic for, as it contains almost no direct enemy spawns.
    # Instead, it uses level enemies to spawn in turrets and such... completely at random.
    # So we just ask for an "okay" loadout and a little armor.
    wanted_active = scale_health(difficulty, 20) / 1.35
    wanted_passive = scale_health(difficulty, 20) / 1.15

    # Compensate a little more than we normally would in lower logic difficulties.
    if world.options.logic_difficulty <= LogicDifficulty.option_standard:
        wanted_active *= 1.2
        wanted_passive *= 1.2

    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5), hard_contact=(8, 7, 7, 6))
    dps_mixed = world.damage_tables.make_dps(active=wanted_active, passive=wanted_passive)
    logic_entrance_rule(world, "AST ROCK (Episode 5) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_armor_level(state, world.player, (armor - 1) if has_repulsor(state, world.player) else armor)
          and can_deal_damage(state, world.player, dps1, exclude=["Multi-Cannon (Rear)", "Starburst", "Scatter Wave"]))

    # Boss: 100, guarded by four plasma turrets: 12
    # Compensate for enemies *still* spawning at this point, too.
    boss_health = scale_health(difficulty, 100) + (scale_health(difficulty, 12) * 4) + (scale_health(difficulty, 10) * 8)
    dps_mixed = world.damage_tables.make_dps(active=boss_health / 9.1, passive=wanted_passive)
    logic_entrance_rule(world, "AST ROCK (Episode 5) @ Destroy Boss", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1, exclude=["Multi-Cannon (Rear)", "Starburst", "Scatter Wave"]))


# =================================================================================================
# MINERS (Episode 5) - 7 locations
# =================================================================================================
def rules_e5_miners(world: "TyrianWorld", difficulty: int) -> None:
    wanted_armor = get_logic_difficulty_choice(world, base=(6, 6, 5, 5), hard_contact=(8, 7, 6, 5))
    logic_entrance_rule(world, "MINERS (Episode 5) @ Base Requirements", lambda state, armor=wanted_armor:
          has_armor_level(state, world.player, (armor - 1) if has_repulsor(state, world.player) else armor))

    # Rock hauler: 10, guarded by the rock it's holding: 40
    dps_normalopt = world.damage_tables.make_dps(active=(scale_health(difficulty, 10) + scale_health(difficulty, 40)) / 1.4)
    dps_pierceopt = world.damage_tables.make_dps(piercing=scale_health(difficulty, 10) / 1.4)
    logic_location_rule(world, "MINERS (Episode 5) - Rock Hauler", lambda state, dps1=dps_normalopt, dps2=dps_pierceopt:
          can_deal_damage(state, world.player, dps2)
          or can_deal_damage(state, world.player, dps1))

    # There's a narrow path through to this enemy ignoring all the surrounding ones, on Master we expect that.
    if world.options.logic_difficulty < LogicDifficulty.option_master:
        dps_normalopt = world.damage_tables.make_dps(active=(scale_health(difficulty, 10) + scale_health(difficulty, 40) + scale_health(difficulty, 4)) / 2.8)
        dps_pierceopt = world.damage_tables.make_dps(piercing=scale_health(difficulty, 4) / 2.8)
        logic_location_rule(world, "MINERS (Episode 5) - Bat-Ship Guarded By Rocks", lambda state, dps1=dps_normalopt, dps2=dps_pierceopt:
              can_deal_damage(state, world.player, dps2)
              or can_deal_damage(state, world.player, dps1))

    # Train head: 20, train carts: 15
    # As the train is a ground enemy and doesn't collide with the player, we expect moving through the head to hit it
    dps_normalopt = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 1.3)
    logic_location_rule(world, "MINERS (Episode 5) - Monorail Train", lambda state, dps1=dps_normalopt:
          can_deal_damage(state, world.player, dps1))

    # Missile launchers: 60, dropping missiles: 2
    dps_normalopt = world.damage_tables.make_dps(active=(scale_health(difficulty, 60) + scale_health(difficulty, 2) * 12) / 5.0)
    logic_entrance_rule(world, "MINERS (Episode 5) @ Destroy Missile Launchers", lambda state, dps1=dps_normalopt:
          can_deal_damage(state, world.player, dps1))

    # Large train boss: Fixed 254, with drill in front: 50
    dps_boss = world.damage_tables.make_dps(active=(254 + scale_health(difficulty, 50)) / 12.2)
    def boss_destroy_rule(state, dps1=dps_boss):
        return can_deal_damage(state, world.player, dps1)
    # Empty timeout rule

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "MINERS (Episode 5) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "MINERS (Episode 5) - Boss", boss_destroy_rule)


# =================================================================================================
# SAVARA (Episode 5) - 9 locations
# =================================================================================================
def rules_e5_savara(world: "TyrianWorld", difficulty: int) -> None:
    # Green Vulcan plane: 15 -- Prefer killing with passive
    # Using this as a general rule for destroying item planes
    dps_option1 = world.damage_tables.make_dps(passive=scale_health(difficulty, 15) / 1.2)
    dps_option2 = world.damage_tables.make_dps(active=scale_health(difficulty, 15) / 1.1)
    logic_entrance_rule(world, "SAVARA (Episode 5) @ Destroy Most Planes", lambda state, dps1=dps_option1, dps2=dps_option2:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2, energy_adjust=-2))

    # Huge Planes: 60
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 60) / 3.2)
    logic_entrance_rule(world, "SAVARA (Episode 5) @ Destroy Huge Planes", lambda state, dps1=dps_mixed:
          can_deal_damage(state, world.player, dps1))

    # Look, it's just E1 SAVARA's boss yet again, we reuse the rules we made for it
    boss_health = 254 + (scale_health(difficulty, 6) * 15) + (scale_health(difficulty, 10) * 4)
    savara_boss_active = world.damage_tables.make_dps(active=boss_health / 30.0)
    savara_tick_sideways = world.damage_tables.make_dps(sideways=scale_health(difficulty, 6) / 1.2)

    def boss_destroy_rule(state, dps1=savara_boss_active):
        return (can_deal_damage(state, world.player, dps1))
    # Also need enough damage to destroy things the boss shoots at you, when dodging isn't an option
    def boss_timeout_rule(state, dps2=savara_tick_sideways, base_rule=boss_destroy_rule):
        return (has_invulnerability(state, world.player)
              or can_deal_damage(state, world.player, dps2)
              or base_rule(state))

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "SAVARA (Episode 5) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_entrance_rule(world, "SAVARA (Episode 5) @ Pass Boss (can time out)", boss_timeout_rule)
        logic_location_rule(world, "SAVARA (Episode 5) - Boss", boss_destroy_rule)


# =================================================================================================
# CORAL (Episode 5) - 8 locations
# =================================================================================================
def rules_e5_coral(world: "TyrianWorld", difficulty: int) -> None:
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 6) / 1.2)
    logic_location_rule(world, "CORAL (Episode 5) - Breakaway Dolphin", lambda state, dps1=dps_active:
          can_deal_damage(state, world.player, dps1, exclude=["Protron Wave"]))

    # Protron Eels: 60 -- Lightning Stingrays: 20 (but move faster)
    wanted_armor = get_logic_difficulty_choice(world, base=(7, 6, 6, 5))
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 60) / 3.8)
    logic_entrance_rule(world, "CORAL (Episode 5) @ After Opening", lambda state, armor=wanted_armor, dps1=dps_active:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1))

    # Starfish: 20 (after they rise)
    # These are really painful homing enemies, especially on hard contact...
    wanted_armor = get_logic_difficulty_choice(world, base=(9, 7, 7, 5), hard_contact=(10, 9, 9, 7))
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 20) / 1.5, passive=scale_health(difficulty, 20) / 1.0)
    logic_entrance_rule(world, "CORAL (Episode 5) @ Pass Starfish", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1, energy_adjust=-2))

    # Boss has two eyes with fixed 254 health
    dps_boss = world.damage_tables.make_dps(active=(508 + scale_health(difficulty, 20) * 3) / 24.0, passive=scale_health(difficulty, 20) / 1.0)
    logic_entrance_rule(world, "CORAL (Episode 5) @ Destroy Boss", lambda state, dps1=dps_boss:
          can_deal_damage(state, world.player, dps1, energy_adjust=-2))


# =================================================================================================
# CANYONRUN (Episode 5) - N/A locations
# =================================================================================================
def rules_e5_canyonrun(world: "TyrianWorld", difficulty: int) -> None:
    pass  # (exists as a placeholder for future use)


# =================================================================================================
# STATION (Episode 5) - 10 locations
# =================================================================================================
def rules_e5_station(world: "TyrianWorld", difficulty: int) -> None:
    # This level is odd because it's designed for Timed Battle mode; most enemies that drop items are very weak,
    # because it's intended to be played with a near-empty loadout.
    if difficulty >= 6:  # Suicide or above
        # Bullet speed is fast enough that we now need to concern ourselves with stopping the turret ships from firing.
        wanted_armor = get_logic_difficulty_choice(world, base=(10, 9, 7, 6), hard_contact=(11, 10, 8, 7))
        dps_active = world.damage_tables.make_dps(active=(scale_health(difficulty, 25) - 10) / 1.6)
        logic_entrance_rule(world, "STATION (Episode 5) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_active:
              has_generator_level(state, world.player, 3)
              and has_armor_level(state, world.player, (armor - 1) if has_repulsor(state, world.player) else armor)
              and can_deal_damage(state, world.player, dps1, energy_adjust=-5))
    else:
        # More chill requirements
        wanted_armor = get_logic_difficulty_choice(world, base=(9, 9, 8, 6), hard_contact=(10, 10, 9, 7))
        dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 8) / 0.9)
        logic_entrance_rule(world, "STATION (Episode 5) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_active:
              has_armor_level(state, world.player, (armor - 2) if has_repulsor(state, world.player) else armor)
              and can_deal_damage(state, world.player, dps1, energy_adjust=-5))

    wanted_armor = get_logic_difficulty_choice(world, base=(11, 10, 8, 7), hard_contact=(12, 11, 9, 7))
    logic_entrance_rule(world, "STATION (Episode 5) @ Survive Crane", lambda state, armor=wanted_armor:
          has_generator_level(state, world.player, 3)
          and has_armor_level(state, world.player, armor))

    # Attractor Crane is the same as the ones in E3 FLEET, copied from there
    dps_pierceopt = world.damage_tables.make_dps(piercing=scale_health(difficulty, 50) / 10.0)
    dps_invulnopt = world.damage_tables.make_dps(active=scale_health(difficulty, 50) / 3.0)
    dps_active = world.damage_tables.make_dps(active=scale_health(difficulty, 50) / 1.4)
    logic_location_rule(world, "STATION (Episode 5) - Attractor Crane", lambda state, dps1=dps_pierceopt, dps2=dps_invulnopt, dps3=dps_active:
          can_deal_damage(state, world.player, dps1)
          or can_deal_damage(state, world.player, dps2 if has_invulnerability(state, world.player) else dps3))

    # Boss has 254 health and sits in place, times out relatively fast
    dps_active = world.damage_tables.make_dps(active=254 / 13.3)
    def boss_destroy_rule(state, dps1=dps_active):
        return can_deal_damage(state, world.player, dps1)
    # Empty timeout rule

    if not world.options.logic_boss_timeout:
        logic_entrance_rule(world, "STATION (Episode 5) @ Pass Boss (can time out)", boss_destroy_rule)
    else:
        logic_location_rule(world, "STATION (Episode 5) - Boss", boss_destroy_rule)


# =================================================================================================
# FRUIT (Episode 5) - 5 locations, goal level
# =================================================================================================
def rules_e5_fruit(world: "TyrianWorld", difficulty: int) -> None:
    # Almost everything fired at you in this level is an enemy, not a bullet.
    # We need a good passive loadout along with a lot of damage to get through safely.
    # Any loadout safe enough to get through also has enough to destroy the boss, so we leave that rule empty.
    wanted_armor = get_logic_difficulty_choice(world, base=(10, 10, 9, 7), hard_contact=(12, 12, 11, 9))
    dps_mixed = world.damage_tables.make_dps(active=scale_health(difficulty, 60) / 2.5, passive=(scale_health(difficulty, 6) * 3) / 1.1)
    logic_entrance_rule(world, "FRUIT (Episode 5) @ Base Requirements", lambda state, armor=wanted_armor, dps1=dps_mixed:
          has_generator_level(state, world.player, 4)
          and has_power_level(state, world.player, 5)
          and has_armor_level(state, world.player, armor)
          and can_deal_damage(state, world.player, dps1))


# -------------------------------------------------------------------------------------------------
# Grand total for Episode 5: 56 locations across 7 (current) levels
# -------------------------------------------------------------------------------------------------


# -------------------------------------------------------------------------------------------------
# =================================================================================================
# -------------------------------------------------------------------------------------------------


level_rules: dict[str, Callable[["TyrianWorld", int], None]] = {
    "TYRIAN (Episode 1)":    rules_e1_tyrian,
    "BUBBLES (Episode 1)":   rules_e1_bubbles,
    "HOLES (Episode 1)":     rules_e1_holes,
    "SOH JIN (Episode 1)":   rules_e1_soh_jin,
    "ASTEROID1 (Episode 1)": rules_e1_asteroid1,
    "ASTEROID2 (Episode 1)": rules_e1_asteroid2,
    "ASTEROID? (Episode 1)": rules_e1_asteroidq,
    "MINEMAZE (Episode 1)":  rules_e1_minemaze,
    "WINDY (Episode 1)":     rules_e1_windy,
    "SAVARA (Episode 1)":    rules_e1_savara,
    "SAVARA II (Episode 1)": rules_e1_savara_ii,
    "BONUS (Episode 1)":     rules_e1_bonus,
    "MINES (Episode 1)":     rules_e1_mines,
    "DELIANI (Episode 1)":   rules_e1_deliani,
    "SAVARA V (Episode 1)":  rules_e1_savara_v,
    "ASSASSIN (Episode 1)":  rules_e1_assassin,

    "TORM (Episode 2)":      rules_e2_torm,
    "GYGES (Episode 2)":     rules_e2_gyges,
    "BONUS 1 (Episode 2)":   rules_e2_bonus_1,
    "ASTCITY (Episode 2)":   rules_e2_astcity,
    "BONUS 2 (Episode 2)":   rules_e2_bonus_2,
    "GEM WAR (Episode 2)":   rules_e2_gem_war,
    "MARKERS (Episode 2)":   rules_e2_markers,
    "MISTAKES (Episode 2)":  rules_e2_mistakes,
    "SOH JIN (Episode 2)":   rules_e2_soh_jin,
    "BOTANY A (Episode 2)":  rules_e2_botany_a,
    "BOTANY B (Episode 2)":  rules_e2_botany_b,
    "GRYPHON (Episode 2)":   rules_e2_gryphon,

    "GAUNTLET (Episode 3)":  rules_e3_gauntlet,
    "IXMUCANE (Episode 3)":  rules_e3_ixmucane,
    "BONUS (Episode 3)":     rules_e3_bonus,
    "STARGATE (Episode 3)":  rules_e3_stargate,
    "AST. CITY (Episode 3)": rules_e3_ast_city,
    "SAWBLADES (Episode 3)": rules_e3_sawblades,
    "CAMANIS (Episode 3)":   rules_e3_camanis,
    "MACES (Episode 3)":     rules_e3_maces,
    "TYRIAN X (Episode 3)":  rules_e3_tyrian_x,
    "SAVARA Y (Episode 3)":  rules_e3_savara_y,
    "NEW DELI (Episode 3)":  rules_e3_new_deli,
    "FLEET (Episode 3)":     rules_e3_fleet,

    "SURFACE (Episode 4)":   rules_e4_surface,
    "WINDY (Episode 4)":     rules_e4_windy,
    "LAVA RUN (Episode 4)":  rules_e4_lava_run,
    "CORE (Episode 4)":      rules_e4_core,
    "LAVA EXIT (Episode 4)": rules_e4_lava_exit,
    "DESERTRUN (Episode 4)": rules_e4_desertrun,
    "SIDE EXIT (Episode 4)": rules_e4_side_exit,
    "?TUNNEL? (Episode 4)":  rules_e4_qtunnelq,
    "ICE EXIT (Episode 4)":  rules_e4_ice_exit,
    "ICESECRET (Episode 4)": rules_e4_icesecret,
    "HARVEST (Episode 4)":   rules_e4_harvest,
    "UNDERDELI (Episode 4)": rules_e4_underdeli,
    "APPROACH (Episode 4)":  rules_e4_approach,
    "SAVARA IV (Episode 4)": rules_e4_savara_iv,
    "DREAD-NOT (Episode 4)": rules_e4_dread_not,
    "EYESPY (Episode 4)":    rules_e4_eyespy,
    "BRAINIAC (Episode 4)":  rules_e4_brainiac,
    "NOSE DRIP (Episode 4)": rules_e4_nose_drip,

    "ASTEROIDS (Episode 5)": rules_e5_asteroids,
    "AST ROCK (Episode 5)":  rules_e5_ast_rock,
    "MINERS (Episode 5)":    rules_e5_miners,
    "SAVARA (Episode 5)":    rules_e5_savara,
    "CORAL (Episode 5)":     rules_e5_coral,
    "CANYONRUN (Episode 5)": rules_e5_canyonrun,
    "STATION (Episode 5)":   rules_e5_station,
    "FRUIT (Episode 5)":     rules_e5_fruit,
}


def set_level_rules(world: "TyrianWorld") -> None:
    # If in no logic mode, we do none of this.
    # Notably, logic for unlocking levels functions outside of this, so you won't have self-locking levels or
    # other impossible scenarios like that. Just an assumption that you can beat anything thrown at you.
    if world.options.logic_difficulty == LogicDifficulty.option_no_logic:
        return

    # Iterate through all levels that we added to the item pool, and add their rules.
    # Level difficulty exists as an argument because in the future, we may allow different difficulties per level.
    for level in world.all_levels:
        level_rules[level](world, world.options.difficulty.value)

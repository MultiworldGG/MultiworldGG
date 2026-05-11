### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ...enums import ChaliceCheckMode, ChaliceMode, GradeCheckMode, WeaponMode
from ...options import CupheadOptions
from . import depbase
from .depbase import Dep, dep

# Deps define a dependency with specific configurations.

DEPS = depbase.DEPS

def dep_none(c: CupheadOptions) -> bool:
    return True

def dep_and(*deps: Dep) -> Dep:
    return lambda c: all(d(c) for d in deps)
def dep_or(*deps: Dep) -> Dep:
    return lambda c: any(d(c) for d in deps)
def dep_not(d: Dep) -> Dep:
    return lambda c: not d(c)

@dep
def dep_dlc(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue
@dep
def dep_freemove(c: CupheadOptions) -> bool:
    return c.freemove_isles.bvalue
@dep
def dep_shortcuts(c: CupheadOptions) -> bool:
    return c.require_secret_shortcuts.bvalue
@dep
def dep_agrade_quest(c: CupheadOptions) -> bool:
    return c.silverworth_quest.bvalue
@dep
def dep_pacifist_quest(c: CupheadOptions) -> bool:
    return c.pacifist_quest.bvalue
@dep
def dep_lucien_quest(c: CupheadOptions) -> bool:
    return c.lucien_quest.bvalue
@dep
def dep_music_quest(c: CupheadOptions) -> bool:
    return c.music_quest.bvalue
@dep
def dep_dicepalace_sanity(c: CupheadOptions) -> bool:
    return c.kingdice_bosssanity.bvalue
@dep
def dep_expert_mode(c: CupheadOptions) -> bool:
    return c.expert_mode.bvalue
@dep
def dep_hard_logic(c: CupheadOptions) -> bool:
    return c.logic_mode.evalue > 0
@dep
def dep_is_pacifist(c: CupheadOptions) -> bool:
    return dep_pacifist_quest(c) or c.rungun_grade_checks == GradeCheckMode.PACIFIST
@dep
def dep_is_any_pacifist(c: CupheadOptions) -> bool:
    return dep_pacifist_quest(c) or dep_is_pacifist(c)
@dep
def dep_rando_abilities(c: CupheadOptions) -> bool:
    return c.randomize_abilities.bvalue
@dep
def dep_no_start_weapon(c: CupheadOptions) -> bool:
    return c.start_weapon.is_none()
@dep
def dep_weapon_ex_rando(c: CupheadOptions) -> bool:
    return c.weapon_mode.evalue & (WeaponMode.PROGRESSIVE | WeaponMode.EX_SEPARATE) > 0
@dep
def dep_weapon_ex_separate(c: CupheadOptions) -> bool:
    return c.weapon_mode.evalue & WeaponMode.EX_SEPARATE > 0
@dep
def dep_dlc_chalice(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and c.dlc_chalice.value > 0

@dep
def dep_dlc_chalice_only(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and c.dlc_chalice.evalue == ChaliceMode.CHALICE_ONLY

@dep
def dep_dlc_chalice_not_separate(c: CupheadOptions) -> bool:
    return (
        dep_dlc_chalice(c) and (
            (c.dlc_boss_chalice_checks & ChaliceCheckMode.SEPARATE) == 0 or
            c.dlc_chalice.evalue == ChaliceMode.CHALICE_ONLY
        )
    )

@dep
def dep_dlc_cookie(c: CupheadOptions) -> bool:
    return (
        c.use_dlc.bvalue and
        (
            c.dlc_chalice.evalue == ChaliceMode.VANILLA or
            c.dlc_chalice.evalue == ChaliceMode.RANDOMIZED
        )
    )
@dep
def dep_dlc_chaliced_grade_required(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and (c.dlc_boss_chalice_checks.evalue & ChaliceCheckMode.GRADE_REQUIRED) > 0
@dep
def dep_dlc_rungun_chaliced_grade_required(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and (c.dlc_rungun_chalice_checks.evalue & ChaliceCheckMode.GRADE_REQUIRED) > 0
@dep
def dep_dlc_boatitem(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and c.dlc_randomize_boat.bvalue
@dep
def dep_dlc_boat_mausoleum(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and c.dlc_requires_mausoleum.bvalue
@dep
def dep_dlc_cactusgirl_quest(c: CupheadOptions) -> bool:
    return c.use_dlc.bvalue and c.dlc_cactusgirl_quest.bvalue

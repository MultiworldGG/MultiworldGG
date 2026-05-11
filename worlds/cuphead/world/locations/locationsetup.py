### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable

from BaseClasses import LocationProgressType

from ..enums import ChaliceMode, ChessCastleMode, GameMode, GradeCheckMode, WeaponMode
from ..names import locationnames
from ..options import CupheadOptions
from . import locationdefs as ld
from .locationbase import LocationData


def add_location(locations_ref: dict[str, LocationData], loc_name: str):
    locations_ref[loc_name] = ld.locations_all[loc_name]

def add_locations(locations_ref: dict[str, LocationData], loc_names: Iterable[str]):
    [add_location(locations_ref, loc) for loc in loc_names]

def exclude_location(locations_ref: dict[str,LocationData], loc_name: str):
    #print(f"Exclude {loc_name}")
    locations_ref[loc_name] = locations_ref[loc_name].with_progress_type(LocationProgressType.EXCLUDED)

def exclude_locations(locations_ref: dict[str, LocationData], loc_names: Iterable[str], strict: bool = False):
    [exclude_location(locations_ref, loc) for loc in loc_names if (strict or loc in locations_ref)]

def setup_grade_check_locations(locations_ref: dict[str,LocationData], options: CupheadOptions):
    boss_grade_checks = options.boss_grade_checks.evalue
    rungun_grade_checks = options.rungun_grade_checks.evalue
    if boss_grade_checks>0:
        locations_ref.update(ld.location_level_boss_topgrade)
        if not options.are_bits_satisfied(options.mode, GameMode.BEAT_DEVIL, GameMode.DLC_BEAT_SALTBAKER):
            locations_ref.update(ld.location_level_boss_final_topgrade)
    if rungun_grade_checks>0:
        if rungun_grade_checks>=1 and rungun_grade_checks<=3:
            locations_ref.update(ld.location_level_rungun_agrade)
        elif rungun_grade_checks==GradeCheckMode.PACIFIST:
            locations_ref.update(ld.location_level_rungun_pacifist)

def setup_boss_phase_check_locations(locations_ref: dict[str, LocationData], options: CupheadOptions):
    pass # TODO: Finish

def setup_quest_locations(locations_ref: dict[str,LocationData], options: CupheadOptions):
    def _add_location(name: str):
        add_location(locations_ref, name)
    if options.buster_quest.bvalue:
        _add_location(locationnames.loc_quest_buster)
    if options.ginger_quest.bvalue:
        _add_location(locationnames.loc_quest_ginger)
        _add_location(locationnames.loc_event_isle2_shortcut)
    if options.fourmel_quest.bvalue:
        _add_location(locationnames.loc_quest_4mel)
        _add_location(locationnames.loc_event_quest_4mel_4th)
    if options.lucien_quest.bvalue:
        _add_location(locationnames.loc_quest_lucien)
    if options.music_quest.bvalue:
        _add_location(locationnames.loc_quest_music)
        _add_location(locationnames.loc_event_quest_ludwig)
        _add_location(locationnames.loc_event_quest_wolfgang)
    if options.silverworth_quest.bvalue:
        locations_ref.update(ld.locations_event_agrade)
        locations_ref.update(ld.location_level_boss_final_event_agrade)
        _add_location(locationnames.loc_quest_silverworth)
    if options.pacifist_quest.bvalue:
        locations_ref.update(ld.location_level_rungun_event_pacifist)
        _add_location(locationnames.loc_quest_pacifist)

def setup_boss_final_locations(
        locations_ref: dict[str,LocationData],
        options: CupheadOptions,
        base_final: dict[str,LocationData],
        dlc_final: dict[str,LocationData],
    ):
    if not options.are_bits_satisfied(options.mode, GameMode.BEAT_DEVIL, GameMode.DLC_BEAT_SALTBAKER):
        locations_ref.update(base_final)
        #if (
        #    options.are_bits_satisfied(options.mode, GameMode.COLLECT_CONTRACTS, GameMode.DLC_COLLECT_INGREDIENTS) and
        #    options.contract_requirements.value == options.contract_goal_requirements.value
        #):
        #    exclude_locations(locations_ref, ld.locations_kingdice_all.keys())
        #    exclude_locations(locations_ref, base_final.keys())
    if (
        options.use_dlc.bvalue and
        not options.are_bits_satisfied(options.mode, GameMode.DLC_BEAT_SALTBAKER, GameMode.BEAT_DEVIL)
    ):
        locations_ref.update(dlc_final)
        #if (
        #    options.are_bits_satisfied(options.mode, GameMode.DLC_COLLECT_INGREDIENTS, GameMode.COLLECT_CONTRACTS) and
        #    options.dlc_ingredient_requirements.value == options.dlc_ingredient_goal_requirements.value
        #):
        #    exclude_locations(locations_ref, dlc_final.keys())

def setup_dlc_chalice_locations(locations_ref: dict[str,LocationData], options: CupheadOptions):
    if options.dlc_chalice.evalue == ChaliceMode.RANDOMIZED:
        add_location(locations_ref, locationnames.loc_dlc_cookie)
    elif options.dlc_chalice.evalue == ChaliceMode.VANILLA:
        add_location(locations_ref, locationnames.loc_event_dlc_cookie)
    if options.dlc_boss_chalice_checks.value:
        locations_ref.update(ld.locations_dlc_boss_chaliced)
        if not options.are_bits_satisfied(options.mode, GameMode.BEAT_DEVIL, GameMode.DLC_BEAT_SALTBAKER):
            locations_ref.update(ld.location_level_boss_final_dlc_chaliced)
        if not options.are_bits_satisfied(options.mode, GameMode.DLC_BEAT_SALTBAKER, GameMode.BEAT_DEVIL):
            locations_ref.update(ld.location_level_dlc_boss_final_dlc_chaliced)
    if options.dlc_rungun_chalice_checks.value:
        locations_ref.update(ld.location_level_rungun_dlc_chaliced)
    if options.dlc_kingdice_chalice_checks.value:
        locations_ref.update(ld.location_level_dicepalace_dlc_chaliced)
    if options.dlc_chess_chalice_checks.value:
        locations_ref.update(ld.location_level_dlc_chesscastle_dlc_chaliced)
    if options.dlc_cactusgirl_quest.value:
        locations_ref.update(ld.locations_dlc_event_boss_chaliced)
        setup_boss_final_locations(
            locations_ref,
            options,
            ld.location_level_boss_final_event_dlc_chaliced,
            ld.location_level_dlc_boss_final_event_dlc_chaliced,
        )
        add_location(locations_ref, locationnames.loc_dlc_quest_cactusgirl)

def setup_dlc_locations(locations_ref: dict[str,LocationData], options: CupheadOptions):
    locations_ref.update(ld.locations_dlc)
    if options.boss_grade_checks.value > 0:
        locations_ref.update(ld.location_level_dlc_boss_topgrade)
        if not options.are_bits_satisfied(options.mode, GameMode.DLC_BEAT_SALTBAKER, GameMode.BEAT_DEVIL):
            locations_ref.update(ld.location_level_dlc_boss_final_topgrade)
    if options.dlc_requires_mausoleum.bvalue:
        add_location(locations_ref, locationnames.loc_event_mausoleum)
    if options.dlc_chalice.value > 0:
        if (options.mode.evalue & GameMode.DLC_NO_ISLE4) == 0:
            locations_ref.update(ld.location_level_dlc_tutorial)
        setup_dlc_chalice_locations(locations_ref, options)
    if options.dlc_kingsleap.evalue != ChessCastleMode.INCLUDE_ALL:
        _kingsleap_locs = [x for x in [
            *ld.location_level_dlc_chesscastle.keys(), *ld.location_level_dlc_chesscastle_dlc_chaliced.keys()
        ] if x in locations_ref]
        for loc in ld.location_level_dlc_chesscastle.keys():
            if (
                (
                    options.dlc_kingsleap.evalue == ChessCastleMode.EXCLUDE_GAUNTLET and
                    (
                        loc == locationnames.loc_level_dlc_chesscastle_run or
                        loc == locationnames.loc_level_dlc_chesscastle_run_dlc_chaliced
                    )
                ) or (
                    options.dlc_kingsleap.evalue == ChessCastleMode.GAUNTLET_ONLY and
                    (
                        loc != locationnames.loc_level_dlc_chesscastle_run and
                        loc != locationnames.loc_level_dlc_chesscastle_run_dlc_chaliced
                    )
                ) or options.dlc_kingsleap.evalue == ChessCastleMode.EXCLUDE
            ):
                exclude_location(locations_ref, loc)

def setup_locations(options: CupheadOptions) -> dict[str,LocationData]:
    use_dlc = options.use_dlc.bvalue
    locations: dict[str,LocationData] = {**ld.locations_base}

    if not options.start_weapon.is_none():
        add_location(locations, locationnames.loc_event_start_weapon)
        if (options.weapon_mode.evalue & WeaponMode.EXCEPT_START) > 0:
            add_location(locations, locationnames.loc_event_start_weapon_ex)

    setup_grade_check_locations(locations, options)

    if options.boss_secret_checks.bvalue:
        locations.update(ld.location_level_boss_secret)
        if use_dlc:
            locations.update(ld.location_level_dlc_boss_secret)

    setup_quest_locations(locations, options)
    setup_boss_phase_check_locations(locations, options)

    if use_dlc:
        setup_dlc_locations(locations, options)

    if options.is_goal_used(locationnames.loc_event_goal_devil):
        locations.update(ld.location_goal)
    if use_dlc and options.is_goal_used(locationnames.loc_event_dlc_goal_saltbaker):
        locations.update(ld.location_dlc_goal)

    setup_boss_final_locations(
        locations,
        options,
        ld.location_level_boss_final,
        ld.location_level_dlc_boss_final
    )

    return locations

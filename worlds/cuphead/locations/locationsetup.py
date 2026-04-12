from __future__ import annotations
from BaseClasses import LocationProgressType
from .locationbase import LocationData
from ..enums import GameMode, GradeCheckMode, WeaponMode, ChessCastleMode, ChaliceMode
from ..names import LocationNames
from ..wconf import WorldConfig
from . import locationdefs as ld

def add_location(locations_ref: dict[str,LocationData], loc_name: str):
    locations_ref[loc_name] = ld.locations_all[loc_name]

def exclude_location(locations_ref: dict[str,LocationData], loc_name: str):
    #print(f"Exclude {loc_name}")
    locations_ref[loc_name] = locations_ref[loc_name].with_progress_type(LocationProgressType.EXCLUDED)

def setup_grade_check_locations(locations_ref: dict[str,LocationData], wconf: WorldConfig):
    boss_grade_checks = wconf.boss_grade_checks
    rungun_grade_checks = wconf.rungun_grade_checks
    if boss_grade_checks>0:
        locations_ref.update(ld.location_level_boss_topgrade)
        if wconf.mode != GameMode.BEAT_DEVIL:
            locations_ref.update(ld.location_level_boss_final_topgrade)
    if rungun_grade_checks>0:
        if rungun_grade_checks>=1 and rungun_grade_checks<=3:
            locations_ref.update(ld.location_level_rungun_agrade)
        elif rungun_grade_checks==GradeCheckMode.PACIFIST:
            locations_ref.update(ld.location_level_rungun_pacifist)

def setup_quest_locations(locations_ref: dict[str,LocationData], wconf: WorldConfig):
    def _add_location(name: str):
        add_location(locations_ref, name)
    if wconf.buster_quest:
        _add_location(LocationNames.loc_quest_buster)
    if wconf.ginger_quest:
        _add_location(LocationNames.loc_quest_ginger)
        _add_location(LocationNames.loc_event_isle2_shortcut)
    if wconf.fourmel_quest:
        _add_location(LocationNames.loc_quest_4mel)
        _add_location(LocationNames.loc_event_quest_4mel_4th)
    if wconf.lucien_quest:
        _add_location(LocationNames.loc_quest_lucien)
    if wconf.music_quest:
        _add_location(LocationNames.loc_quest_music)
        _add_location(LocationNames.loc_event_quest_ludwig)
        _add_location(LocationNames.loc_event_quest_wolfgang)
    if wconf.silverworth_quest:
        locations_ref.update(ld.locations_event_agrade)
        locations_ref.update(ld.location_level_boss_final_event_agrade)
        _add_location(LocationNames.loc_quest_silverworth)
    if wconf.pacifist_quest:
        locations_ref.update(ld.location_level_rungun_event_pacifist)
        _add_location(LocationNames.loc_quest_pacifist)

def setup_boss_final_locations(
        locations_ref: dict[str,LocationData],
        wconf: WorldConfig,
        base_final: dict[str,LocationData],
        dlc_final: dict[str,LocationData],
    ):
    if wconf.mode != GameMode.BEAT_DEVIL:
        locations_ref.update(base_final)
    if wconf.use_dlc and wconf.mode != GameMode.DLC_BEAT_SALTBAKER:
        locations_ref.update(dlc_final)

def setup_dlc_chalice_locations(locations_ref: dict[str,LocationData], wconf: WorldConfig):
    locations_ref.update(ld.location_level_dlc_tutorial)
    if wconf.dlc_chalice == ChaliceMode.RANDOMIZED:
        add_location(locations_ref, LocationNames.loc_dlc_cookie)
    elif wconf.dlc_chalice == ChaliceMode.VANILLA:
        add_location(locations_ref, LocationNames.loc_event_dlc_cookie)
    if wconf.dlc_boss_chalice_checks:
        locations_ref.update(ld.locations_dlc_boss_chaliced)
        if wconf.mode != GameMode.BEAT_DEVIL:
            locations_ref.update(ld.location_level_boss_final_dlc_chaliced)
        if wconf.mode != GameMode.DLC_BEAT_SALTBAKER:
            locations_ref.update(ld.location_level_dlc_boss_final_dlc_chaliced)
    if wconf.dlc_rungun_chalice_checks:
        locations_ref.update(ld.location_level_rungun_dlc_chaliced)
    if wconf.dlc_kingdice_chalice_checks:
        locations_ref.update(ld.location_level_dicepalace_dlc_chaliced)
    if wconf.dlc_chess_chalice_checks:
        locations_ref.update(ld.location_level_dlc_chesscastle_dlc_chaliced)
    if wconf.dlc_cactusgirl_quest:
        locations_ref.update(ld.locations_dlc_event_boss_chaliced)
        setup_boss_final_locations(
            locations_ref,
            wconf,
            ld.location_level_boss_final_event_dlc_chaliced,
            ld.location_level_dlc_boss_final_event_dlc_chaliced,
        )
        add_location(locations_ref, LocationNames.loc_dlc_quest_cactusgirl)

def setup_dlc_locations(locations_ref: dict[str,LocationData], wconf: WorldConfig):
    locations_ref.update(ld.locations_dlc)
    if wconf.boss_grade_checks>0:
        locations_ref.update(ld.location_level_dlc_boss_topgrade)
        if wconf.mode != GameMode.DLC_BEAT_SALTBAKER:
            locations_ref.update(ld.location_level_dlc_boss_final_topgrade)
    if wconf.dlc_requires_mausoleum:
        add_location(locations_ref, LocationNames.loc_event_mausoleum)
    if wconf.dlc_chalice > 0:
        setup_dlc_chalice_locations(locations_ref, wconf)
    if wconf.dlc_kingsleap != ChessCastleMode.INCLUDE_ALL:
        _kingsleap_locs = [x for x in [
            *ld.location_level_dlc_chesscastle.keys(), *ld.location_level_dlc_chesscastle_dlc_chaliced.keys()
        ] if x in locations_ref]
        for loc in ld.location_level_dlc_chesscastle.keys():
            if (
                (
                    wconf.dlc_kingsleap == ChessCastleMode.EXCLUDE_GAUNTLET and
                    (
                        loc == LocationNames.loc_level_dlc_chesscastle_run or
                        loc == LocationNames.loc_level_dlc_chesscastle_run_dlc_chaliced
                    )
                ) or (
                    wconf.dlc_kingsleap == ChessCastleMode.GAUNTLET_ONLY and
                    (
                        loc != LocationNames.loc_level_dlc_chesscastle_run and
                        loc != LocationNames.loc_level_dlc_chesscastle_run_dlc_chaliced
                    )
                ) or wconf.dlc_kingsleap == ChessCastleMode.EXCLUDE
            ):
                exclude_location(locations_ref, loc)

def setup_locations(wconf: WorldConfig) -> dict[str,LocationData]:
    use_dlc = wconf.use_dlc
    locations: dict[str,LocationData] = {**ld.locations_base}

    add_location(locations, LocationNames.loc_event_start_weapon)
    if (wconf.weapon_mode & WeaponMode.EXCEPT_START) > 0:
        add_location(locations, LocationNames.loc_event_start_weapon_ex)

    setup_grade_check_locations(locations, wconf)

    if wconf.boss_secret_checks:
        locations.update(ld.location_level_boss_secret)
        if use_dlc:
            locations.update(ld.location_level_dlc_boss_secret)

    setup_quest_locations(locations, wconf)

    if use_dlc:
        setup_dlc_locations(locations, wconf)

    if wconf.is_goal_used(LocationNames.loc_event_goal_devil):
        locations.update(ld.location_goal)
    if use_dlc and wconf.is_goal_used(LocationNames.loc_event_dlc_goal_saltbaker):
        locations.update(ld.location_dlc_goal)

    setup_boss_final_locations(
        locations,
        wconf,
        ld.location_level_boss_final,
        ld.location_level_dlc_boss_final
    )

    return locations

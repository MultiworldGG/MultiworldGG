### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from ..names import locationnames

s_plane_locations_lv: set[str] = {
    locationnames.loc_level_boss_plane_blimp,
    locationnames.loc_level_boss_plane_genie,
    locationnames.loc_level_boss_plane_bird,
    locationnames.loc_level_boss_plane_mermaid,
    locationnames.loc_level_boss_plane_robot,
    locationnames.loc_level_dlc_boss_plane_cowboy
}
s_plane_locations_topgrade: set[str] = {
    locationnames.loc_level_boss_plane_blimp_topgrade,
    locationnames.loc_level_boss_plane_genie_topgrade,
    locationnames.loc_level_boss_plane_bird_topgrade,
    locationnames.loc_level_boss_plane_mermaid_topgrade,
    locationnames.loc_level_boss_plane_robot_topgrade,
    locationnames.loc_level_dlc_boss_plane_cowboy_topgrade
}
s_plane_locations_event_agrade: set[str] = {
    locationnames.loc_level_boss_plane_blimp_event_agrade,
    locationnames.loc_level_boss_plane_genie_event_agrade,
    locationnames.loc_level_boss_plane_bird_event_agrade,
    locationnames.loc_level_boss_plane_mermaid_event_agrade,
    locationnames.loc_level_boss_plane_robot_event_agrade,
}
s_plane_locations_dlc_chaliced: set[str] = {
    locationnames.loc_level_boss_plane_blimp_dlc_chaliced,
    locationnames.loc_level_boss_plane_genie_dlc_chaliced,
    locationnames.loc_level_boss_plane_bird_dlc_chaliced,
    locationnames.loc_level_boss_plane_mermaid_dlc_chaliced,
    locationnames.loc_level_boss_plane_robot_dlc_chaliced,
    locationnames.loc_level_dlc_boss_plane_cowboy_dlc_chaliced
}
s_plane_locations_dlc_event_chaliced: set[str] = {
    locationnames.loc_level_boss_plane_blimp_event_dlc_chaliced,
    locationnames.loc_level_boss_plane_genie_event_dlc_chaliced,
    locationnames.loc_level_boss_plane_bird_event_dlc_chaliced,
    locationnames.loc_level_boss_plane_mermaid_event_dlc_chaliced,
    locationnames.loc_level_boss_plane_robot_event_dlc_chaliced,
    locationnames.loc_level_dlc_boss_plane_cowboy_event_dlc_chaliced,
}

s_plane_locations: set[str] = {
    *s_plane_locations_lv,
    *s_plane_locations_topgrade,
    *s_plane_locations_event_agrade,
    *s_plane_locations_dlc_chaliced,
    *s_plane_locations_dlc_event_chaliced,
}

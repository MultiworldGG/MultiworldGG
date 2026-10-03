from typing import Dict, Optional, Tuple, Union

from ..enums import (
    ZorkGrandInquisitorDeathsanity,
    ZorkGrandInquisitorGoals,
    ZorkGrandInquisitorItemTransforms,
    ZorkGrandInquisitorItems,
    ZorkGrandInquisitorLandmarksanity,
    ZorkGrandInquisitorLocations,
    ZorkGrandInquisitorLocationTransforms,
    ZorkGrandInquisitorStartingLocations,
)


item_data_transforms: Dict[
    Union[
        ZorkGrandInquisitorStartingLocations,
        ZorkGrandInquisitorGoals,
        ZorkGrandInquisitorDeathsanity,
        ZorkGrandInquisitorLandmarksanity,
    ],
    Optional[Dict[ZorkGrandInquisitorItemTransforms, Tuple[ZorkGrandInquisitorItems, ...]]]
] = {
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS,
        ),
    },
    ZorkGrandInquisitorStartingLocations.CROSSROADS: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS,
        ),
    },
    ZorkGrandInquisitorStartingLocations.DM_LAIR: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
        ),
    },
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_CROSSROADS,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_DM_LAIR,
        ),
    },
    ZorkGrandInquisitorStartingLocations.GUE_TECH: None,
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_SPELL_LAB,
        ),
    },
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_HADES,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_HADES,
        ),
    },
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_FLOOD_CONTROL_DAM,
        ),
    },
    ZorkGrandInquisitorStartingLocations.MONASTERY: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.MONASTERY_ROPE,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
        ),
    },
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.MONASTERY_ROPE,
            ZorkGrandInquisitorItems.SUBWAY_DESTINATION_MONASTERY,
            ZorkGrandInquisitorItems.TELEPORTER_DESTINATION_MONASTERY,
        ),
    },
    ZorkGrandInquisitorGoals.THREE_ARTIFACTS: None,
    ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT: None,
    ZorkGrandInquisitorGoals.SPELL_HEIST: {
        ZorkGrandInquisitorItemTransforms.MAKE_DEPRIORITIZED_SKIP_BALANCING: (
            ZorkGrandInquisitorItems.SPELL_BEBURTT,
            ZorkGrandInquisitorItems.SPELL_GLORF,
            ZorkGrandInquisitorItems.SPELL_GOLGATEM,
            ZorkGrandInquisitorItems.SPELL_IGRAM,
            ZorkGrandInquisitorItems.SPELL_KENDALL,
            ZorkGrandInquisitorItems.SPELL_NARWILE,
            ZorkGrandInquisitorItems.SPELL_OBIDIL,
            ZorkGrandInquisitorItems.SPELL_REZROV,
            ZorkGrandInquisitorItems.SPELL_SNAVIG,
            ZorkGrandInquisitorItems.SPELL_THROCK,
            ZorkGrandInquisitorItems.SPELL_YASTARD,
        ),
    },
    ZorkGrandInquisitorGoals.ZORK_TOUR: None,
    ZorkGrandInquisitorGoals.GRIM_JOURNEY: None,
    ZorkGrandInquisitorDeathsanity.OFF: {
        ZorkGrandInquisitorItemTransforms.MAKE_FILLER: (
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_INFINITY,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_NEWARK_NEW_JERSEY,
            ZorkGrandInquisitorItems.TOTEMIZER_DESTINATION_SURFACE_OF_MERZ,
        ),
    },
    ZorkGrandInquisitorDeathsanity.ON: None,
    ZorkGrandInquisitorLandmarksanity.OFF: None,
    ZorkGrandInquisitorLandmarksanity.ON: None,
}

location_data_transforms: Dict[
    Union[
        ZorkGrandInquisitorStartingLocations,
        ZorkGrandInquisitorGoals,
        ZorkGrandInquisitorDeathsanity,
        ZorkGrandInquisitorLandmarksanity,
    ],
    Optional[Dict[ZorkGrandInquisitorLocationTransforms, Tuple[ZorkGrandInquisitorLocations, ...]]]
] = {
    ZorkGrandInquisitorStartingLocations.PORT_FOOZLE: None,
    ZorkGrandInquisitorStartingLocations.CROSSROADS: None,
    ZorkGrandInquisitorStartingLocations.DM_LAIR: None,
    ZorkGrandInquisitorStartingLocations.DM_LAIR_INTERIOR: None,
    ZorkGrandInquisitorStartingLocations.GUE_TECH: None,
    ZorkGrandInquisitorStartingLocations.SPELL_LAB: None,
    ZorkGrandInquisitorStartingLocations.HADES_SHORE: None,
    ZorkGrandInquisitorStartingLocations.SUBWAY_FLOOD_CONTROL_DAM: None,
    ZorkGrandInquisitorStartingLocations.MONASTERY: None,
    ZorkGrandInquisitorStartingLocations.MONASTERY_EXHIBIT: None,
    ZorkGrandInquisitorGoals.THREE_ARTIFACTS: None,
    ZorkGrandInquisitorGoals.ARTIFACT_OF_MAGIC_HUNT: {
        ZorkGrandInquisitorLocationTransforms.REMOVE: (
            ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT,
            ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG,
            ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP,
        ),
    },
    ZorkGrandInquisitorGoals.SPELL_HEIST: {
        ZorkGrandInquisitorLocationTransforms.REMOVE: (
            ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT,
            ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG,
            ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP,
        ),
    },
    ZorkGrandInquisitorGoals.ZORK_TOUR: {
        ZorkGrandInquisitorLocationTransforms.REMOVE: (
            ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT,
            ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG,
            ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP,
        ),
    },
    ZorkGrandInquisitorGoals.GRIM_JOURNEY: {
        ZorkGrandInquisitorLocationTransforms.REMOVE: (
            ZorkGrandInquisitorLocations.COME_TO_PAPA_YOU_NUT,
            ZorkGrandInquisitorLocations.GOOD_PUZZLE_SMART_BROG,
            ZorkGrandInquisitorLocations.YOU_LOSE_MUFFET_ANTE_UP,
        ),
    },
    ZorkGrandInquisitorDeathsanity.OFF: {
        ZorkGrandInquisitorLocationTransforms.REMOVE: (
            ZorkGrandInquisitorLocations.DEATH_ARRESTED_WITH_JACK,
            ZorkGrandInquisitorLocations.DEATH_ATTACKED_THE_QUELBEES,
            ZorkGrandInquisitorLocations.DEATH_CLIMBED_OUT_OF_THE_WELL,
            ZorkGrandInquisitorLocations.DEATH_CUT_THE_POWER_CORD_WITH_THE_SWORD,
            ZorkGrandInquisitorLocations.DEATH_CUT_THE_RADIO_TOWER_CABLE,
            ZorkGrandInquisitorLocations.DEATH_EATEN_BY_A_GRUE,
            ZorkGrandInquisitorLocations.DEATH_ENTERED_THE_GUARDS_TENT,
            ZorkGrandInquisitorLocations.DEATH_JUMPED_IN_BOTTOMLESS_PIT,
            ZorkGrandInquisitorLocations.DEATH_LOST_GAME_OF_STRIP_GRUE_FIRE_WATER,
            ZorkGrandInquisitorLocations.DEATH_LOST_SOUL_TO_OLD_SCRATCH,
            ZorkGrandInquisitorLocations.DEATH_OUTSMARTED_BY_THE_QUELBEES,
            ZorkGrandInquisitorLocations.DEATH_RILED_THE_FISHWIFE,
            ZorkGrandInquisitorLocations.DEATH_SLICED_UP_BY_THE_INVISIBLE_GUARD,
            ZorkGrandInquisitorLocations.DEATH_SNUCK_PAST_THE_GUARDS_TENT,
            ZorkGrandInquisitorLocations.DEATH_STEPPED_INTO_THE_INFINITE,
            ZorkGrandInquisitorLocations.DEATH_SWALLOWED_BY_A_DRAGON,
            ZorkGrandInquisitorLocations.DEATH_THROCKED_THE_GRASS,
            ZorkGrandInquisitorLocations.DEATH_TOOK_THE_OMEGA_HAMMER,
            ZorkGrandInquisitorLocations.DEATH_TOOK_THE_PSI_HAMMER,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_INFINITY,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_NEWARK_NEW_JERSEY,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_HALLS_OF_INQUISITION,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_INFINITY,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_NEWARK_NEW_JERSEY,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_STRAIGHT_TO_HELL,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_PERMANENTLY_SURFACE_OF_MERZ,
            ZorkGrandInquisitorLocations.DEATH_TOTEMIZED_SURFACE_OF_MERZ,
            ZorkGrandInquisitorLocations.DEATH_TOUCHED_THE_ELECTRIFIED_FENCE,
            ZorkGrandInquisitorLocations.DEATH_WALKED_INTO_THE_ELECTRICAL_FIELD,
            ZorkGrandInquisitorLocations.DEATH_YOURE_NOT_CHARON,
            ZorkGrandInquisitorLocations.DEATH_ZORK_ROCKS_EXPLODED,
        ),
    },
    ZorkGrandInquisitorDeathsanity.ON: None,
    ZorkGrandInquisitorLandmarksanity.OFF: {
        ZorkGrandInquisitorLocationTransforms.REMOVE: (
            ZorkGrandInquisitorLocations.LANDMARK_DRAGON_ARCHIPELAGO,
            ZorkGrandInquisitorLocations.LANDMARK_DUNGEON_MASTERS_HOUSE,
            ZorkGrandInquisitorLocations.LANDMARK_FLATHEAD_MESA,
            ZorkGrandInquisitorLocations.LANDMARK_FLOOD_CONTROL_DAM_3,
            ZorkGrandInquisitorLocations.LANDMARK_GATES_OF_HELL,
            ZorkGrandInquisitorLocations.LANDMARK_GREAT_UNDERGROUND_EMPIRE_ENTRANCE,
            ZorkGrandInquisitorLocations.LANDMARK_GUE_TECH_FOUNTAIN_INSIDE,
            ZorkGrandInquisitorLocations.LANDMARK_GUE_TECH_FOUNTAIN_OUTSIDE,
            ZorkGrandInquisitorLocations.LANDMARK_HADES_SHORE,
            ZorkGrandInquisitorLocations.LANDMARK_INFINITE_CORRIDOR,
            ZorkGrandInquisitorLocations.LANDMARK_INQUISITION_HEADQUARTERS,
            ZorkGrandInquisitorLocations.LANDMARK_JACKS_SHOP,
            ZorkGrandInquisitorLocations.LANDMARK_MIRROR_ROOM,
            ZorkGrandInquisitorLocations.LANDMARK_OUTSIDE_THE_MONASTERY_EXHIBIT,
            ZorkGrandInquisitorLocations.LANDMARK_PAST_PORT_FOOZLE,
            ZorkGrandInquisitorLocations.LANDMARK_PORT_FOOZLE,
            ZorkGrandInquisitorLocations.LANDMARK_SPELL_CHECKER,
            ZorkGrandInquisitorLocations.LANDMARK_TOP_OF_THE_RADIO_TOWER,
            ZorkGrandInquisitorLocations.LANDMARK_TOTEMIZER,
            ZorkGrandInquisitorLocations.LANDMARK_UMBRELLA_TREE,
            ZorkGrandInquisitorLocations.LANDMARK_UNDERGROUND_UNDERGROUND_ENTRANCE,
            ZorkGrandInquisitorLocations.LANDMARK_WALKING_CASTLES_HEART,
            ZorkGrandInquisitorLocations.LANDMARK_WHITE_HOUSE,
        ),
    },
    ZorkGrandInquisitorLandmarksanity.ON: None,
}

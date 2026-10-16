"""Physical sources for Lore Tablet randomization."""

from __future__ import annotations

from dataclasses import dataclass


LORE_TABLET_CATEGORY = "LoreTablet"


@dataclass(frozen=True)
class LoreTabletIdentity:
    scene_name: str
    hierarchy_path: str
    sheet: str
    key: str


@dataclass(frozen=True)
class LoreTabletSource:
    location_name: str
    marker_scene_name: str
    marker_x: float
    marker_y: float
    scene_width: float
    scene_height: float
    act_number: int
    path_name: str
    identities: tuple[LoreTabletIdentity, ...]
    requires_needolin: bool = False

    @property
    def item_name(self) -> str:
        return f"Lore: {self.location_name}"


def _identity(
    scene_name: str,
    hierarchy_path: str,
    sheet: str,
    key: str,
) -> LoreTabletIdentity:
    return LoreTabletIdentity(scene_name, hierarchy_path, sheet, key)


LORE_TABLET_SOURCES: tuple[LoreTabletSource, ...] = (
    LoreTabletSource(
        "Abyss - Upper Lore Stone",
        "Abyss_02b", 148.78, 47.05, 228.0, 55.0,
        3, "Abyss - Void Tendrils",
        (_identity(
            "abyss_02b",
            "Abyss_lore_stone/Inspect Region",
            "Inspect",
            "ABYSS_LORE_STONE_TOP",
        ),),
    ),
    LoreTabletSource(
        "Abyss - Lower Lore Stone",
        "Abyss_06", 42.13, 45.82, 60.0, 51.0,
        3, "Abyss - Void Tendrils",
        (_identity(
            "abyss_06",
            "Abyss_lore_stone/Inspect Region",
            "Inspect",
            "ABYSS_LORE_STONE_BASE",
        ),),
    ),
    LoreTabletSource(
        "Putrified Ducts - White Lake Weaver Sign",
        "Aqueduct_05", 187.51, 9.34, 332.0, 100.0,
        2, "Putrified Ducts - Bellway",
        (
            _identity(
                "aqueduct_05_caravan",
                "Caravan_States/Fleatopia/weaver_harp_sign (2)/Inspect Region",
                "Inspect",
                "WEAVE_WHITE_LAKE",
            ),
            _identity(
                "aqueduct_05_festival",
                "Caravan_States/Flea_Festival_Intro/weaver_harp_sign (3)/Inspect Region",
                "Inspect",
                "WEAVE_WHITE_LAKE",
            ),
            _identity(
                "aqueduct_05_pre",
                "Caravan_States/Pre_Fleatopia/weaver_harp_sign (1)/Inspect Region",
                "Inspect",
                "WEAVE_WHITE_LAKE",
            ),
        ),
        requires_needolin=True,
    ),
    LoreTabletSource(
        "Memorium - Lower Plaque",
        "Arborium_01", 14.22, 19.79, 29.0, 151.0,
        2, "Outlying Citadel - Memorium",
        (_identity(
            "arborium_01", "Inspect Region", "Inspect", "ARBORIUM_PLAQUE",
        ),),
    ),
    LoreTabletSource(
        "Blasted Steps - Shellwood Entrance Sign",
        "Coral_19", 299.188232, 39.795497, 427.0, 55.0,
        1, "Blasted Steps - Bellway",
        (_identity(
            "coral_19",
            "Black Thread States Thread Only Variant/Normal World/Inspect Region",
            "Inspect",
            "CORAL_JUDGEMENT_SIGN",
        ),),
    ),
    LoreTabletSource(
        "The Cradle - Terminus Commandment",
        "Tube_Hub", 118.279995, 39.840001, 135.0, 145.0,
        2, "The Cradle - Terminus",
        (_identity(
            "tube_hub",
            "Black Thread States/Normal World/Inspect Region",
            "Inspect",
            "TUBE_HUB_NOTICE",
        ),),
    ),
    LoreTabletSource(
        "Memorium - Orders",
        "Arborium_03", 17.91, 98.269997, 29.0, 110.0,
        2, "Outlying Citadel - Memorium",
        (_identity(
            "arborium_03", "Inspect Region", "Inspect", "ARBORIUM_ORDERS",
        ),),
    ),
    LoreTabletSource(
        "The Marrow - Entrance Inscription",
        "Bone_01c", 185.759995, 8.38, 198.0, 91.0,
        1, "The Marrow - Toll",
        (_identity(
            "bone_01c", "Inspect Region", "Lore", "MARROW_START_SIGN",
        ),),
    ),
    LoreTabletSource(
        "The Marrow - Pilgrim Diary",
        "Bone_18", 30.95, 7.30, 49.0, 33.0,
        1, "The Marrow - Shooting Gallery",
        (_identity(
            "bone_18",
            "Inspect Region",
            "Inspect",
            "CURIOUS_PILGRIM_DIARY",
        ),),
    ),
    LoreTabletSource(
        "Far Fields - Weavenest Cindril Inscription",
        "Bone_East_Weavehome", 58.59, 65.450836, 205.0, 120.0,
        1, "Far Fields - Bellway",
        (_identity(
            "bone_east_weavehome",
            "Group/Inspect Region (2)",
            "Inspect",
            "WEAVE_WILDS",
        ),),
    ),
    LoreTabletSource(
        "Verdania - Oath Plaque",
        "Clover_10", 56.01, 8.36, 136.0, 54.0,
        3, "Greymoor - Bellshrine",
        (_identity(
            "clover_10",
            "Plaque_Scene/Plaque/Inspect Region",
            "Inspect",
            "CLOVER_OATH_PLAQUE",
        ),),
    ),
    LoreTabletSource(
        "Verdania - Lake Plaque",
        "Clover_18", 114.080002, 9.35, 195.0, 80.0,
        3, "Greymoor - Bellshrine",
        (_identity(
            "clover_18",
            "Fountains Group/Plaque/Up/Inspect Region",
            "Inspect",
            "CLOVER_LAKE_PLAQUE",
        ),),
    ),
    LoreTabletSource(
        "Sands of Karak - Upper Coral Tablet",
        "Coral_25", 129.485153, 85.096017, 149.0, 98.0,
        1, "Sands of Karak - Sands of Karak",
        (_identity(
            "coral_25",
            "Coral Crust Lore Tablet/Interact",
            "Lore",
            "CORAL_CRUST_TAB_1",
        ),),
    ),
    LoreTabletSource(
        "Blasted Steps - Judge Nursery Record",
        "Coral_36", 17.07, 31.98, 70.0, 58.0,
        1, "Blasted Steps - Bellway",
        (_identity(
            "coral_36", "Inspect Region", "Inspect", "JUDGE_NURSERY",
        ),),
    ),
    LoreTabletSource(
        "Sands of Karak - Lower Coral Tablet",
        "Coral_Tower_01", 24.66, 5.85, 138.0, 22.0,
        1, "Sands of Karak - Coral Tower",
        (_identity(
            "coral_tower_01",
            "Coral Crust Lore Tablet/Interact",
            "Lore",
            "CORAL_CRUST_TAB_2",
        ),),
    ),
    LoreTabletSource(
        "The Cradle - Upper Cage Inscription",
        "Cradle_02b", 8.26, 30.74, 48.0, 47.0,
        2, "The Cradle - Terminus",
        (_identity(
            "cradle_02b", "Inspect Region", "Inspect", "CRADLE_CAGE_01",
        ),),
    ),
    LoreTabletSource(
        "The Cradle - Middle Cage Inscription",
        "Cradle_02b", 7.73, 15.83, 48.0, 47.0,
        2, "The Cradle - Terminus",
        (_identity(
            "cradle_02b",
            "Inspect Region (1)",
            "Inspect",
            "CRADLE_CAGE_02",
        ),),
    ),
    LoreTabletSource(
        "The Cradle - Lower Cage Inscription",
        "Cradle_02b", 23.959999, 7.51, 48.0, 47.0,
        2, "The Cradle - Terminus",
        (_identity(
            "cradle_02b",
            "Inspect Region (2)",
            "Inspect",
            "CRADLE_CAGE_03",
        ),),
    ),
    LoreTabletSource(
        "Greymoor - Orders",
        "Greymoor_03", 15.49515, 128.444397, 120.0, 140.0,
        1, "Greymoor - Halfway House",
        (_identity(
            "greymoor_03", "Inspect Region", "Inspect", "GREY_ORDERS",
        ),),
    ),
    LoreTabletSource(
        "Greymoor - Cage Record",
        "Greymoor_16", 56.879997, 52.200001, 171.0, 60.0,
        1, "Greymoor - Halfway House",
        (_identity(
            "greymoor_16", "Inspect Region", "Inspect", "GREY_LORE",
        ),),
    ),
    LoreTabletSource(
        "Greymoor - Nuu's Scrolls",
        "Halfway_01", 23.60, 21.059999, 56.0, 32.0,
        1, "Greymoor - Halfway House",
        (_identity(
            "halfway_01",
            "_NPCs/Hunter Fan Control/Nuu_Scrolls/Inspect Region",
            "Wanderers",
            "HUNTER_FAN_SCROLL_INSPECT",
        ),),
    ),
    LoreTabletSource(
        "Whispering Vaults - Theatre Desk",
        "Library_13b", 21.91, 7.37, 73.0, 25.0,
        2, "Outlying Citadel - Library",
        (
            _identity(
                "library_13b",
                "Desk Inspect and Quill/Group/desk_inspect/Inspect Region Act 2",
                "Inspect",
                "LIBRARY_THEATRE_LINES",
            ),
            _identity(
                "library_13b",
                "Desk Inspect and Quill/Group/desk_inspect/Inspect Region Act 3",
                "Inspect",
                "LIBRARY_THEATRE_LINES_ACT3",
            ),
        ),
    ),
    LoreTabletSource(
        "Mosshome - Moss Plaque",
        "Mosstown_02", 86.859999, 35.179999, 160.0, 65.0,
        1, "The Marrow - Mosshome Gate",
        (_identity(
            "mosstown_02",
            "lore_tablet/moss_bone_plaque/Inspect Region",
            "Inspect",
            "MOSSTOWN_STONE",
        ),),
    ),
    LoreTabletSource(
        "Mosshome - Weaver Harp Inscription",
        "Mosstown_02", 86.83778, 35.479999, 160.0, 65.0,
        1, "The Marrow - Mosshome Gate",
        (_identity(
            "mosstown_02",
            "lore_tablet/weaver_harp_sign/Inspect Region",
            "Inspect",
            "WEAVE_HARP_MOSSTOWN",
        ),),
        requires_needolin=True,
    ),
    LoreTabletSource(
        "Mount Fay - Weaver Inscription",
        "Peak_10", 15.076999, 33.959999, 80.0, 50.0,
        2, "Mount Fay - Shakra",
        (_identity(
            "peak_10", "Inspect Region (2)", "Inspect", "WEAVE_PEAK",
        ),),
    ),
    LoreTabletSource(
        "Deep Docks - Forge Note",
        "Room_Forge", 27.41, 17.32, 140.0, 69.0,
        1, "Deep Docks - Forge",
        (_identity(
            "room_forge", "Inspect Region", "Inspect", "DOCKS_NOTE_1",
        ),),
    ),
    LoreTabletSource(
        "Bilewater - Storeroom Record",
        "Shadow_08", 38.27, 8.47, 100.0, 55.0,
        1, "Bilewater - Bellway",
        (_identity(
            "shadow_08", "Inspect Region", "Inspect", "SWAMP_STOREROOM",
        ),),
    ),
    LoreTabletSource(
        "Bilewater - Bilehaven Plaque",
        "Shadow_18", 94.550003, 36.290001, 117.0, 45.0,
        1, "Bilewater - Bilehaven",
        (_identity(
            "shadow_18", "Inspect Region", "Inspect", "BILEHAVEN_PLAQUE",
        ),),
    ),
    LoreTabletSource(
        "Bilewater - Weaver Workshop Scroll",
        "Shadow_Weavehome", 172.052002, 39.34, 177.0, 68.0,
        1, "Bilewater - Bellway",
        (_identity(
            "shadow_weavehome",
            "Inspect Region (1)",
            "Inspect",
            "WEAVE_WORKSHOP_SCROLL",
        ),),
    ),
    LoreTabletSource(
        "Shellwood - Shellgrave Inscription",
        "Shellgrave", 92.799116, 0.5, 138.0, 22.0,
        1, "Shellwood - Greyroot",
        (_identity(
            "shellgrave",
            "Black Thread States Thread Only Variant/Normal World/Inspect Region",
            "Inspect",
            "SHELLGRAVE",
        ),),
    ),
    LoreTabletSource(
        "Shellwood - Weaver Harp Inscription",
        "Shellwood_10", 40.34, 12.210614, 79.0, 102.0,
        1, "Shellwood - Central Toll",
        (_identity(
            "shellwood_10",
            "weaver_harp_sign/Inspect Region",
            "Inspect",
            "WEAVE_HARP_SHELLWOOD",
        ),),
        requires_needolin=True,
    ),
    LoreTabletSource(
        "The Slab - Left Orders",
        "Slab_08", 20.45, 13.87, 35.0, 40.0,
        2, "The Slab - Capture Event",
        (_identity(
            "slab_08",
            "dock_b__0051_lore_sign_hang/Inspect Region",
            "Inspect",
            "SLAB_ORDERS_1",
        ),),
    ),
    LoreTabletSource(
        "The Slab - Right Orders",
        "Slab_08", 27.050001, 13.87, 35.0, 40.0,
        2, "The Slab - Capture Event",
        (_identity(
            "slab_08",
            "dock_b__0051_lore_sign_hang (1)/Inspect Region",
            "Inspect",
            "SLAB_ORDERS_2",
        ),),
    ),
    LoreTabletSource(
        "The Slab - Weaver Gate Inscription",
        "Slab_10c", 22.812537, 12.817337, 42.0, 65.0,
        2, "The Slab - Capture Event",
        (_identity(
            "slab_10c",
            "Break Gate Group/Group/gate/Inspect Region",
            "Inspect",
            "SLAB_WEAVER_GATE",
        ),),
    ),
    LoreTabletSource(
        "Moss Grotto - Shaman Storeroom Record",
        "Tut_04", 79.080002, 9.18, 87.0, 36.0,
        1, "Mosslands - Moss Grotto",
        (_identity(
            "tut_04", "Inspect Region", "Inspect", "SHAMAN_STORE_ROOM",
        ),),
    ),
    LoreTabletSource(
        "Whiteward - Oath",
        "Ward_07", 121.709991, 10.820001, 130.0, 20.0,
        2, "Underworks - Whiteward",
        (_identity(
            "ward_07", "Group/Inspect Region", "Inspect", "WARD_OATH",
        ),),
    ),
    LoreTabletSource(
        "Weavenest Atla - Archive Inscription",
        "Weave_08", 40.209, 30.365993, 77.0, 67.0,
        1, "Weavenest - Atla",
        (_identity(
            "weave_08",
            "Group/Inspect Region (1)",
            "Inspect",
            "WEAVE_ARCHIVE_RIGHT",
        ),),
    ),
    LoreTabletSource(
        "Bellhart - Outer Sign",
        "Belltown_07", 57.874252, 5.059642, 70.0, 34.0,
        1, "Bellhart - Bellhart",
        (_identity(
            "belltown_07",
            "Black Thread States Thread Only Variant/Normal World/Inspect Region",
            "Inspect",
            "BELLTOWN_OUTER_SIGN",
        ),),
    ),
)


ADDITIONAL_LORE_TABLET_SOURCES = (
    LoreTabletSource(
        "Grand Gate - Nyleth Shrine Inscription",
        "Shellwood_11b", 59.065552, 149.047134, 120.0, 170.0,
        2, "Grand Gate - Grand Gate",
        (_identity("shellwood_11b", "Inspect Region", "Inspect", "SHELLWOOD_SHRINE_SIGN"),),
    ),
    LoreTabletSource(
        "Bellhart - East Sign",
        "Belltown_06", 14.92, 8.37, 80.0, 83.0,
        1, "Bellhart - Bellhart",
        (_identity("belltown_06", "Inspect Region", "Inspect", "BELLTOWN_OUTER_SIGN"),),
    ),
)
LORE_TABLET_SOURCES += ADDITIONAL_LORE_TABLET_SOURCES

LORE_TABLET_LOCATION_NAMES: tuple[str, ...] = tuple(
    source.location_name for source in LORE_TABLET_SOURCES
)
LORE_TABLET_ITEM_NAMES: tuple[str, ...] = tuple(
    source.item_name for source in LORE_TABLET_SOURCES
)
LORE_TABLET_ITEM_BY_LOCATION: dict[str, str] = {
    source.location_name: source.item_name
    for source in LORE_TABLET_SOURCES
}
LORE_TABLET_ACT_THREE_LOCATION_NAMES: frozenset[str] = frozenset(
    source.location_name
    for source in LORE_TABLET_SOURCES
    if source.act_number == 3 and source.location_name != "Verdania - Lake Plaque"
)

LORE_TABLET_COMMUNITY_BACKED_LOCATION_NAMES: frozenset[str] = frozenset((
    "Bellhart - Outer Sign",
    "Bellhart - East Sign",
    "Grand Gate - Nyleth Shrine Inscription",
    "The Marrow - Entrance Inscription",
    "The Marrow - Pilgrim Diary",
    "Deep Docks - Forge Note",
    "Blasted Steps - Judge Nursery Record",
    "Whispering Vaults - Theatre Desk",
    "Whiteward - Oath",
    "Weavenest Atla - Archive Inscription",
    "Mosshome - Moss Plaque",
    "Shellwood - Shellgrave Inscription",
    "Shellwood - Weaver Harp Inscription",
    "Sands of Karak - Upper Coral Tablet",
    "The Slab - Left Orders",
    "The Slab - Right Orders",
))
LORE_TABLET_JUNK_ONLY_LOCATION_NAMES: frozenset[str] = (
    frozenset(LORE_TABLET_LOCATION_NAMES)
    - LORE_TABLET_COMMUNITY_BACKED_LOCATION_NAMES
    - {"Verdania - Lake Plaque"}
)

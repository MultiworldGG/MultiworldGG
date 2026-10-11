from ..constants.options import Rac5Options
from ..data.challenges import (
    CHALLENGE_GROUP_DERBY as CHALLENGE_GROUP_DERBY,
    CHALLENGE_GROUP_GADGETBOT as CHALLENGE_GROUP_GADGETBOT,
    CHALLENGE_GROUP_GADGETBOT_TOSS as CHALLENGE_GROUP_GADGETBOT_TOSS,
    DEFAULT_CLANK_CHALLENGE_GROUPS as DEFAULT_CLANK_CHALLENGE_GROUPS,
)
from ..items import WEAPON_DISPLAY_TO_INTERNAL
from .armour_sets import LOCATIONS as ARMOUR_SET_RECORDS
from .challax import LOCATIONS as CHALLAX_LOCATIONS
from .dayni_moon import LOCATIONS as DAYNI_MOON_LOCATIONS
from .dreamtime import LOCATIONS as DREAMTIME_LOCATIONS
from .inside_clank import LOCATIONS as INSIDE_CLANK_LOCATIONS
from .kalidon import LOCATIONS as KALIDON_LOCATIONS
from .menu import LOCATIONS as MENU_LOCATIONS
from .metalis import LOCATIONS as METALIS_LOCATIONS
from .model import BASE_ID as BASE_ID, LocationView, Rac5Locations
from .outpost_omega import LOCATIONS as OUTPOST_OMEGA_LOCATIONS
from .pokitaru import LOCATIONS as POKITARU_LOCATIONS
from .quodrona import LOCATIONS as QUODRONA_LOCATIONS
from .ryllus import LOCATIONS as RYLLUS_LOCATIONS
from .weapon_levels import LOCATIONS as WEAPON_LEVEL_RECORDS

LOCATIONS = tuple(
    sorted(
        (
            *POKITARU_LOCATIONS,
            *RYLLUS_LOCATIONS,
            *KALIDON_LOCATIONS,
            *METALIS_LOCATIONS,
            *DREAMTIME_LOCATIONS,
            *OUTPOST_OMEGA_LOCATIONS,
            *CHALLAX_LOCATIONS,
            *DAYNI_MOON_LOCATIONS,
            *INSIDE_CLANK_LOCATIONS,
            *QUODRONA_LOCATIONS,
            *MENU_LOCATIONS,
            *WEAPON_LEVEL_RECORDS,
            *ARMOUR_SET_RECORDS,
        ),
        key=lambda location: location.definition_order,
    )
)

MENU_REGION = "Menu"
PLANET_ORDER = (
    "Pokitaru",
    "Ryllus",
    "Kalidon",
    "Metalis",
    "Dreamtime",
    "Outpost Omega",
    "Challax",
    "Dayni Moon",
    "Inside Clank",
    "Quodrona",
)
RACLocationData = Rac5Locations
ALL_LOCATIONS = {location.name: location for location in LOCATIONS}
LOCATION_ID_TO_NAME = LocationView(LOCATIONS, key=lambda location: location.code, value=lambda location: location.name)
TITANIUM_BOLT_LOCATIONS = LocationView(LOCATIONS, lambda location: "titanium_bolt" in location.categories)
ARMOUR_PICKUP_LOCATIONS = LocationView(LOCATIONS, lambda location: "armour_pickup" in location.categories)
BOSS_LOCATIONS = LocationView(LOCATIONS, lambda location: "boss" in location.categories)
WEAPON_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_vendor" in location.categories)
GADGET_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "gadget_vendor" in location.categories)
WEAPON_MOD_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_mod_vendor" in location.categories)
WEAPON_TITAN_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_titan_vendor" in location.categories)
WEAPON_LEVEL_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_level" in location.categories)
WEAPON_MAX_LEVEL_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_max_level" in location.categories)
WEAPON_SUB_MAX_LEVEL_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_sub_max_level" in location.categories)
NANOTECH_LEVEL_LOCATIONS = LocationView(LOCATIONS, lambda location: "nanotech_level" in location.categories)
ARMOUR_SET_CHECK_LOCATIONS = LocationView(LOCATIONS, lambda location: "armour_set_check" in location.categories)
NG_PLUS_WEAPON_LEVEL_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "ng_plus_weapon_level" in location.categories)
)
CHALLENGE_MODE_MAX_LEVEL_LOCATIONS = LocationView(
    LOCATIONS, lambda location: "challenge_mode_max_level" in location.categories
)
CHALLENGE_MODE_SUB_MAX_LEVEL_LOCATIONS = LocationView(
    LOCATIONS, lambda location: "challenge_mode_sub_max_level" in location.categories
)
CHALLENGE_MODE_WEAPON_LEVEL_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_weapon_level" in location.categories)
)
NG_PLUS_ARMOUR_SET_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "ng_plus_armour_set" in location.categories)
)
CHALLENGE_MODE_1_ARMOUR_SET_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_1_armour_set" in location.categories)
)
CHALLENGE_MODE_2_ARMOUR_SET_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_2_armour_set" in location.categories)
)
CHALLENGE_MODE_1_ARMOUR_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_1_armour" in location.categories)
)
CHALLENGE_MODE_2_ARMOUR_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_2_armour" in location.categories)
)
CHALLENGE_MODE_RYNO_LOCATION = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_ryno" in location.categories)
)
CHALLENGE_MODE_MOD_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: "challenge_mode_mod" in location.categories)
)
GIANT_CLANK_LOCATIONS = frozenset(
    LocationView(LOCATIONS, lambda location: Rac5Options.GIANT_CLANK in location.categories)
)
SKILL_POINT_LOCATIONS = LocationView(LOCATIONS, lambda location: "skill_point" in location.categories)
EASY_SKILL_POINT_LOCATIONS = LocationView(LOCATIONS, lambda location: "easy_skill_point" in location.categories)
HARD_SKILL_POINT_LOCATIONS = LocationView(LOCATIONS, lambda location: "hard_skill_point" in location.categories)
CLANK_CHALLENGE_SKILL_POINT_LOCATIONS = LocationView(
    LOCATIONS, lambda location: "clank_challenge_skill_point" in location.categories
)
SKYBOARD_CHALLENGE_SKILL_POINT_LOCATIONS = LocationView(
    LOCATIONS, lambda location: "skyboard_challenge_skill_point" in location.categories
)
GADGET_PICKUP_LOCATIONS = LocationView(LOCATIONS, lambda location: "gadget_pickup" in location.categories)
SKYBOARD_ITEM_LOCATIONS = LocationView(LOCATIONS, lambda location: "skyboard_item" in location.categories)
EXTRA_SKYBOARD_LOCATIONS = LocationView(LOCATIONS, lambda location: "extra_skyboard" in location.categories)
SHRINK_RAY_SKIP_LOCATIONS = LocationView(LOCATIONS, lambda location: "shrink_ray_skip" in location.categories)
CHALLENGE_LOCATIONS = LocationView(LOCATIONS, lambda location: "challenge" in location.categories)
ALL_CLANK_LOCATIONS = LocationView(LOCATIONS, lambda location: "all_clank" in location.categories)
STORY_MISSION_LOCATIONS = LocationView(LOCATIONS, lambda location: "story_mission" in location.categories)
CUTSCENE_LOCATIONS = LocationView(LOCATIONS, lambda location: "cutscene" in location.categories)
MISSION_LOCATIONS = LocationView(LOCATIONS, lambda location: "mission" in location.categories)
VENDOR_WEAPON_LOC = LocationView(
    LOCATIONS,
    lambda location: "weapon_vendor" in location.categories,
    key=lambda location: location.name,
    value=lambda location: location.weapon,
)
VENDOR_TITAN_LOC = LocationView(
    LOCATIONS,
    lambda location: "weapon_titan_vendor" in location.categories,
    key=lambda location: location.name,
    value=lambda location: location.weapon,
)
VENDOR_GADGET_LOC = LocationView(
    LOCATIONS,
    lambda location: "gadget_vendor" in location.categories,
    key=lambda location: location.name,
    value=lambda location: location.gadget,
)
SKILL_POINT_WEAPON_LOC = LocationView(
    LOCATIONS,
    lambda location: "skill_point" in location.categories and location.weapon is not None,
    key=lambda location: location.name,
    value=lambda location: location.weapon,
)
WEAPON_INTERNAL_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: "weapon_vendor" in location.categories,
    key=lambda location: location.weapon,
    value=lambda location: location.name,
)
TITAN_INTERNAL_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: "weapon_titan_vendor" in location.categories,
    key=lambda location: location.weapon,
    value=lambda location: location.name,
)
GADGET_INTERNAL_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: "gadget_vendor" in location.categories,
    key=lambda location: location.gadget,
    value=lambda location: location.name,
)
MOD_INTERNAL_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: location.mod_slot is not None,
    key=lambda location: (location.weapon, location.mod_slot),
    value=lambda location: location.name,
)
MOD_INTERNAL_TO_VENDOR_SLOT_LOCATION = LocationView(
    LOCATIONS,
    lambda location: location.mod_slot is not None,
    key=lambda location: (location.weapon, location.mod_slot.removeprefix("mod_slot_")),
    value=lambda location: location.name,
)
WEAPON_LEVEL_LOOKUP = LocationView(
    LOCATIONS,
    lambda location: "weapon_level" in location.categories,
    key=lambda location: (location.weapon, location.level),
    value=lambda location: location.name,
)
NANOTECH_LEVEL_LOOKUP = LocationView(
    LOCATIONS,
    lambda location: "nanotech_level" in location.categories,
    key=lambda location: location.level,
    value=lambda location: location.name,
)


def enabled_clank_challenge_names(group_weights):
    return frozenset(
        (
            location.name
            for location in LOCATIONS
            if location.options is not None and location.options.challenge_group in group_weights
        )
    )


def nanotech_level_locations_for(interval, max_level):
    return LocationView(
        LOCATIONS,
        lambda location: (
            "nanotech_level" in location.categories
            and interval > 0
            and (location.level % interval == 0)
            and (location.level <= max_level)
        ),
    )


def disabled_weapon_location_names(enabled_weapons):
    enabled = {WEAPON_DISPLAY_TO_INTERNAL[name] for name in enabled_weapons}
    return frozenset(
        (location.name for location in LOCATIONS if location.weapon is not None and location.weapon not in enabled)
    )


def for_planet(planet, *sources):
    names = frozenset((name for source in sources for name in source)) if sources else None
    return LocationView(
        LOCATIONS, lambda location: location.planet == planet and (names is None or location.name in names)
    )

# ruff: noqa: I001 -- import order sets location IDs, see the comment above the location imports.
from ..constants.options import Rac5Options
# Import order is load-bearing: location IDs are handed out as each module is first imported
# (see model.py's _LOCATION_IDS), so reordering these renumbers every location after the move.
from .armour_sets import LOCATIONS as ARMOUR_SET_RECORDS
from .challax import LOCATIONS as CHALLAX_LOCATIONS
from .dayni_moon import LOCATIONS as DAYNI_MOON_LOCATIONS
from .dreamtime import LOCATIONS as DREAMTIME_LOCATIONS
from .inside_clank import LOCATIONS as INSIDE_CLANK_LOCATIONS
from .kalidon import LOCATIONS as KALIDON_LOCATIONS
from .nanotech_levels import LOCATIONS as NANOTECH_LEVEL_RECORDS
from .metalis import LOCATIONS as METALIS_LOCATIONS
from .model import TIERED_SKILL_POINT_CATEGORIES, LocationView, Rac5Categories, Rac5CompletionSources
from .outpost_omega import LOCATIONS as OUTPOST_OMEGA_LOCATIONS
from .pokitaru import LOCATIONS as POKITARU_LOCATIONS
from .quodrona import LOCATIONS as QUODRONA_LOCATIONS
from .ryllus import LOCATIONS as RYLLUS_LOCATIONS
from .weapon_levels import LOCATIONS as WEAPON_LEVEL_RECORDS
from .hig_treehouse import LOCATIONS as HIG_TREEHOUSE_LOCATIONS

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
            *NANOTECH_LEVEL_RECORDS,
            *WEAPON_LEVEL_RECORDS,
            *ARMOUR_SET_RECORDS,
            *HIG_TREEHOUSE_LOCATIONS,
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
    "HIG Treehouse",
)
ALL_LOCATIONS = {location.name: location for location in LOCATIONS}


def required_skill_points(options) -> tuple[str, ...]:
    """Skill point locations the All Skill Points check and goal wait on."""
    return tuple(
        location.name
        for location in LOCATIONS
        if location.categories & TIERED_SKILL_POINT_CATEGORIES and location.available(options)
    )


def required_clank_challenges(options) -> tuple[str, ...]:
    """Clank Challenge locations the All Clank Challenges goal waits on."""
    return tuple(
        location.name
        for location in LOCATIONS
        if location.completed.source == Rac5CompletionSources.CHALLENGES and location.available(options)
    )


_GROUP_CATEGORIES = {
    "Titanium Bolts": Rac5Categories.TITANIUM_BOLT,
    "Armour Pickups": Rac5Categories.ARMOUR_PICKUP,
    "Armour Set Checks": Rac5Categories.ARMOUR_SET_CHECK,
    "Bosses": Rac5Categories.BOSS,
    "Gadget Pickups": Rac5Categories.GADGET_PICKUP,
    "Weapon Vendors": Rac5Categories.WEAPON_VENDOR,
    "Gadget Vendors": Rac5Categories.GADGET_VENDOR,
    "Titan Vendors": Rac5Categories.WEAPON_TITAN_VENDOR,
    "Mod Vendors": Rac5Categories.WEAPON_MOD_VENDOR,
    "Missions": Rac5Categories.MISSION,
    "Story Missions": Rac5Categories.STORY_MISSION,
    "Cutscenes": Rac5Categories.CUTSCENE,
    "Skill Points": Rac5Categories.SKILL_POINT,
    "Easy Skill Points": Rac5Categories.EASY_SKILL_POINT,
    "Hard Skill Points": Rac5Categories.HARD_SKILL_POINT,
    "Clank Challenge Skill Points": Rac5Categories.CLANK_CHALLENGE_SKILL_POINT,
    "Skyboard Challenge Skill Points": Rac5Categories.SKYBOARD_CHALLENGE_SKILL_POINT,
    "Clank Challenges": Rac5Categories.CHALLENGE,
    "Skyboard Items": Rac5Categories.SKYBOARD_ITEM,
    "Extra Skyboard": Rac5Categories.EXTRA_SKYBOARD,
    "Shrink Ray Skips": Rac5Categories.SHRINK_RAY_SKIP,
    "Weapon Levels": Rac5Categories.WEAPON_LEVEL,
    "Nanotech Levels": Rac5Categories.NANOTECH_LEVEL,
}
LOCATION_NAME_GROUPS: dict[str, set[str]] = {
    **{
        group: {location.name for location in LOCATIONS if category in location.categories}
        for group, category in _GROUP_CATEGORIES.items()
    },
    **{planet: {location.name for location in LOCATIONS if location.planet == planet} for planet in PLANET_ORDER},
}
TITANIUM_BOLT_LOCATIONS = LocationView(LOCATIONS, lambda location: "titanium_bolt" in location.categories)
ARMOUR_PICKUP_LOCATIONS = LocationView(LOCATIONS, lambda location: "armour_pickup" in location.categories)
BOSS_LOCATIONS = LocationView(LOCATIONS, lambda location: "boss" in location.categories)
WEAPON_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_vendor" in location.categories)
GADGET_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "gadget_vendor" in location.categories)
WEAPON_MOD_VENDOR_LOCATIONS = LocationView(LOCATIONS, lambda location: "weapon_mod_vendor" in location.categories)
ARMOUR_SET_CHECK_LOCATIONS = LocationView(LOCATIONS, lambda location: "armour_set_check" in location.categories)
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
GADGET_PICKUP_LOCATIONS = LocationView(LOCATIONS, lambda location: "gadget_pickup" in location.categories)
SHRINK_RAY_SKIP_LOCATIONS = LocationView(LOCATIONS, lambda location: "shrink_ray_skip" in location.categories)
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
WEAPON_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: "weapon_vendor" in location.categories,
    key=lambda location: location.weapon,
    value=lambda location: location.name,
)
TITAN_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: "weapon_titan_vendor" in location.categories,
    key=lambda location: location.weapon,
    value=lambda location: location.name,
)
GADGET_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: "gadget_vendor" in location.categories,
    key=lambda location: location.gadget,
    value=lambda location: location.name,
)
MOD_TO_LOCATION = LocationView(
    LOCATIONS,
    lambda location: location.mod_slot is not None,
    key=lambda location: (location.weapon, location.mod_slot),
    value=lambda location: location.name,
)
WEAPON_LEVEL_LOOKUP = LocationView(
    LOCATIONS,
    lambda location: "weapon_level" in location.categories,
    key=lambda location: (location.weapon, location.level),
    value=lambda location: location.name,
)

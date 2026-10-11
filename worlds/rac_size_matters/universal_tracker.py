from .constants.options import Rac5Options

"""Universal Tracker integration for Ratchet & Clank: Size Matters"""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from worlds.rac_size_matters.world import RACSizeMatterWorld

PLANET_TO_MAP_INDEX: dict[str, int] = {
    "Pokitaru": 1,
    "Ryllus": 2,
    "Kalidon": 3,
    "Metalis": 4,
    "Dreamtime": 5,
    "Outpost Omega": 6,
    "Challax": 7,
    "Dayni Moon": 8,
    "Inside Clank": 9,
    "Quodrona": 10,
}

PLANET_ID_TO_REGION: dict[int, str] = {
    0x01: "Pokitaru",
    0x02: "Ryllus",
    0x03: "Kalidon",
    0x04: "Metalis",
    0x05: "Dreamtime",
    0x06: "Outpost Omega",
    0x07: "Challax",
    0x08: "Dayni Moon",
    0x09: "Inside Clank",
    0x0A: "Quodrona",
    0x16: "Kalidon",
    0x17: "Outpost Omega",
}


def setup_options_from_slot_data(world: "RACSizeMatterWorld") -> None:
    """Set options from passthrough slot data when re-generating for Universal Tracker."""
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if world.game in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough[world.game]
            world.options.all_missions.value = world.passthrough.get(Rac5Options.ALL_MISSIONS, True)
            world.options.clank_pack.value = world.passthrough.get(Rac5Options.CLANK_PACK, False)
            world.options.all_cutscenes.value = world.passthrough.get(Rac5Options.ALL_CUTSCENES, False)
            world.options.giant_clank.value = world.passthrough.get(Rac5Options.GIANT_CLANK, False)
            world.options.progressive_weapons.value = world.passthrough[Rac5Options.PROGRESSIVE_WEAPONS]
            world.options.progressive_mods.value = world.passthrough.get(Rac5Options.PROGRESSIVE_MODS, False)
            world.options.progressive_armour.value = world.passthrough[Rac5Options.PROGRESSIVE_ARMOUR]
            world.options.enabled_weapons.value = world.passthrough.get(
                Rac5Options.ENABLED_WEAPONS, dict(world.options.enabled_weapons.default)
            )
            world.options.death_link.value = world.passthrough[Rac5Options.DEATH_LINK]
            world.options.clank_challenges.value = world.passthrough.get(Rac5Options.CLANK_CHALLENGES, 0)
            world.options.clank_challenge_groups.value = world.passthrough.get(
                Rac5Options.CLANK_CHALLENGE_GROUPS, dict(world.options.clank_challenge_groups.default)
            )
            world.options.skyboard_challenges.value = world.passthrough.get(Rac5Options.SKYBOARD_CHALLENGES, 0)
            world.options.shrink_ray_options.value = world.passthrough.get(Rac5Options.SHRINK_RAY_OPTIONS, 1)
            world.options.skill_points.value = world.passthrough.get(Rac5Options.SKILL_POINTS, True)
            world.options.enable_clank_challenge_skill_points.value = world.passthrough.get(
                Rac5Options.ENABLE_CLANK_CHALLENGE_SKILL_POINTS, False
            )
            world.options.enable_skyboard_challenge_skill_points.value = world.passthrough.get(
                Rac5Options.ENABLE_SKYBOARD_CHALLENGE_SKILL_POINTS, False
            )

            world.options.armour_set_checks.value = world.passthrough[Rac5Options.ARMOUR_SET_CHECKS]
            world.options.ng_plus_items.value = world.passthrough.get(Rac5Options.NG_PLUS_ITEMS, True)
            world.options.challenge_mode.value = world.passthrough.get(Rac5Options.CHALLENGE_MODE, 0)
            world.options.progressive_challenge_mode.value = world.passthrough.get(
                Rac5Options.PROGRESSIVE_CHALLENGE_MODE, False
            )
            world.options.random_starting_planet.value = world.passthrough.get(Rac5Options.RANDOM_STARTING_PLANET, 0)
            world.options.starting_weapons.value = world.passthrough[Rac5Options.STARTING_WEAPONS]
            world.options.starting_gadgets.value = world.passthrough[Rac5Options.STARTING_GADGETS]
            world.options.starting_bolts.value = world.passthrough[Rac5Options.STARTING_BOLTS]
            world.options.experimental_skins.value = world.passthrough.get(Rac5Options.EXPERIMENTAL_SKINS, False)
            world.options.starting_skin.value = world.passthrough.get(Rac5Options.STARTING_SKIN, 0)
            world.options.ap_icon.value = world.options.ap_icon.options.get(
                world.passthrough.get(Rac5Options.AP_ICON, "original"), 0
            )
            world.options.death_amnesty.value = world.passthrough[Rac5Options.DEATH_AMNESTY]
            world.options.weapon_level_checks.value = world.passthrough.get(Rac5Options.WEAPON_LEVEL_CHECKS, 0)
            world.options.nanotech_level_interval.value = world.passthrough.get(Rac5Options.NANOTECH_LEVEL_INTERVAL, 0)
            world.options.nanotech_level_max.value = world.passthrough.get(Rac5Options.NANOTECH_LEVEL_MAX, 75)
            world.options.weapon_experience_multiplier.value = world.passthrough.get(
                Rac5Options.WEAPON_EXPERIENCE_MULTIPLIER, 0
            )
            world.options.bolt_multiplier.value = world.passthrough.get(Rac5Options.BOLT_MULTIPLIER, 0)
            world.options.nanotech_experience_multiplier.value = world.passthrough.get(
                Rac5Options.NANOTECH_EXPERIENCE_MULTIPLIER, 0
            )
        else:
            world.using_ut = False
    else:
        world.using_ut = False


def map_page_index(data: str) -> int:
    """Return the maps.json index for the given planet name. Defaults to Galaxy (0)."""
    return PLANET_TO_MAP_INDEX.get(data, 0)


tracker_world: dict[str, Any] = {
    "map_page_maps": "tracker/maps.json",
    "map_page_locations": "tracker/locations.json",
    "map_page_setting_key": r"rsm_current_planet_{player}_{team}",
    "map_page_index": map_page_index,
}

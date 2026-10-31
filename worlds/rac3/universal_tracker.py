"""This module contains functionality for universal tracker"""

from typing import Any, TYPE_CHECKING

from worlds.rac3.constants.data.location import UT_MAPPING
from worlds.rac3.constants.data.region import RAC3_REGION_DATA_TABLE
from worlds.rac3.constants.options import RAC3OPTION
from worlds.rac3.constants.region import RAC3REGION

if TYPE_CHECKING:
    from worlds.rac3.world import RaC3World


def setup_options_from_slot_data(world: "RaC3World") -> None:
    """Set the option values to the values already generated"""
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if world.game in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough[world.game]
            world.options.start_inventory_from_pool.value = world.passthrough[RAC3OPTION.START_INVENTORY_FROM_POOL]
            world.options.generation_behavior.value = world.passthrough[RAC3OPTION.GENERATION_BEHAVIOR]
            world.options.starting_weapons.value = world.passthrough[RAC3OPTION.STARTING_WEAPONS]
            world.options.bolt_and_xp_multiplier.value = world.passthrough[RAC3OPTION.BOLT_AND_XP_MULTIPLIER]
            world.options.progressive_weapons.value = world.passthrough[RAC3OPTION.PROGRESSIVE_WEAPONS]
            world.options.weapon_mods.value = world.passthrough[RAC3OPTION.WEAPON_MODS]
            world.options.progressive_wrench.value = world.passthrough[RAC3OPTION.PROGRESSIVE_WRENCH]
            world.options.armor_upgrade.value = world.passthrough[RAC3OPTION.ARMOR_UPGRADE]
            world.options.skill_points.value = world.passthrough[RAC3OPTION.SKILL_POINTS]
            world.options.skill_points_pick_and_mix.value = world.passthrough[RAC3OPTION.SKILL_POINTS_PICK_AND_MIX]
            world.options.trophies.value = world.passthrough[RAC3OPTION.TROPHIES]
            world.options.titanium_bolts.value = world.passthrough[RAC3OPTION.TITANIUM_BOLTS]
            world.options.nanotech_milestones.value = world.passthrough[RAC3OPTION.NANOTECH_MILESTONES]
            world.options.ship_nose.value = world.passthrough[RAC3OPTION.SHIP_NOSE]
            world.options.ship_wings.value = world.passthrough[RAC3OPTION.SHIP_WINGS]
            world.options.ship_skin.value = world.passthrough[RAC3OPTION.SHIP_SKIN]
            world.options.player_skin.value = world.passthrough[RAC3OPTION.PLAYER_SKIN]
            world.options.traps_enabled.value = world.passthrough[RAC3OPTION.ENABLE_TRAPS]
            world.options.trap_weight.value = world.passthrough[RAC3OPTION.TRAP_WEIGHT]
            world.options.trap_magnitude.value = world.passthrough[RAC3OPTION.TRAP_MAGNITUDE]
            world.options.filler_magnitude.value = world.passthrough[RAC3OPTION.FILLER_MAGNITUDE]
            world.options.rangers.value = world.passthrough[RAC3OPTION.RANGERS]
            world.options.arena.value = world.passthrough[RAC3OPTION.ARENA]
            world.options.vidcomics.value = world.passthrough[RAC3OPTION.VIDCOMICS]
            world.options.exclude_locations.value = world.passthrough[RAC3OPTION.EXCLUDE]
            world.options.deathlink.value = world.passthrough[RAC3OPTION.DEATHLINK]
            world.options.vr_challenges.value = world.passthrough[RAC3OPTION.VR_CHALLENGES]
            world.options.sewer_crystals.value = world.passthrough[RAC3OPTION.SEWER_CRYSTALS]
            world.options.sewer_limitation.value = world.passthrough[RAC3OPTION.SEWER_LIMITATION]
            world.options.nanotech_limitation.value = world.passthrough[RAC3OPTION.NANOTECH_LIMITATION]
            world.options.weapon_vendors.value = world.passthrough[RAC3OPTION.WEAPON_VENDORS]
            world.options.filler_weight.value = world.passthrough[RAC3OPTION.FILLER_WEIGHT]
            world.options.one_hp_challenge.value = world.passthrough[RAC3OPTION.ONE_HP_CHALLENGE]
            world.options.clank_options.value = world.passthrough[RAC3OPTION.CLANK_OPTIONS]
            world.options.ship_vendor.value = world.passthrough[RAC3OPTION.SHIP_VENDOR]
            world.options.armor_vendor.value = world.passthrough[RAC3OPTION.ARMOR_VENDOR]
            world.options.scout_vendors.value = world.passthrough[RAC3OPTION.SCOUT_VENDORS]
            world.options.shortcuts.value = world.passthrough[RAC3OPTION.SHORTCUTS]
            world.options.speedups.value = world.passthrough[RAC3OPTION.SPEEDUPS]
            world.options.ngplus_items.value = world.passthrough[RAC3OPTION.NGPLUS_ITEMS]
            world.options.ngplus_vendors.value = world.passthrough[RAC3OPTION.NGPLUS_VENDOR]
            world.options.ngplus_start.value = world.passthrough[RAC3OPTION.NGPLUS_START]
            world.options.helpdesk.value = world.passthrough[RAC3OPTION.HELP_DESK]
            world.options.weapon_level_locations.value = world.passthrough[RAC3OPTION.WEAPON_LEVEL_LOCATIONS]
            world.options.vendor_access.value = world.passthrough[RAC3OPTION.VENDOR_ACCESS]
            world.options.bonus_vidcomic_health.value = world.passthrough[RAC3OPTION.BONUS_VIDCOMIC_HEALTH]
            world.options.vidcomic_health_upgrades.value = world.passthrough[RAC3OPTION.VIDCOMIC_HEALTH_UPGRADES]
            world.options.deathlink_behavior.value = world.passthrough[RAC3OPTION.DEATHLINK_BEHAVIOR]
            world.options.lock_command_center.value = world.passthrough[RAC3OPTION.LOCK_CC]
            world.options.goal_bio.value = world.passthrough[RAC3OPTION.GOAL_BIO]
            world.options.goal_nef.value = world.passthrough[RAC3OPTION.GOAL_NEF]
            world.options.goal_nano.value = world.passthrough[RAC3OPTION.GOAL_NANO]
            world.options.goal_crystal.value = world.passthrough[RAC3OPTION.GOAL_CRYSTAL]
            world.options.goal_tbolts.value = world.passthrough[RAC3OPTION.GOAL_TBOLTS]
            world.options.goal_skillpoints.value = world.passthrough[RAC3OPTION.GOAL_SKILLPOINTS]
            world.options.goal_qwark.value = world.passthrough[RAC3OPTION.GOAL_QWARK]
            world.options.goal_museum.value = world.passthrough[RAC3OPTION.GOAL_MUSEUM]
            world.options.goal_planets.value = world.passthrough[RAC3OPTION.GOAL_PLANETS]
            world.options.goal_completion.value = world.passthrough[RAC3OPTION.GOAL_COMPLETION]
            world.options.goal_boss_qwark.value = world.passthrough[RAC3OPTION.GOAL_BOSS_QWARK]
            world.options.goal_boss_two.value = world.passthrough[RAC3OPTION.GOAL_BOSS_TWO]
            world.options.goal_boss_noid.value = world.passthrough[RAC3OPTION.GOAL_BOSS_NOID]
            world.options.goal_boss_warship.value = world.passthrough[RAC3OPTION.GOAL_BOSS_WARSHIP]
            world.options.goal_boss_scorpio.value = world.passthrough[RAC3OPTION.GOAL_BOSS_SCORPIO]
            world.options.goal_boss_talos.value = world.passthrough[RAC3OPTION.GOAL_BOSS_TALOS]
            world.options.goal_boss_gears.value = world.passthrough[RAC3OPTION.GOAL_BOSS_GEARS]
            world.options.goal_boss_klunk.value = world.passthrough[RAC3OPTION.GOAL_BOSS_KLUNK]
        else:
            world.using_ut = False
    else:
        world.using_ut = False


def map_page_index(data: str) -> int:
    """Lookup the ID of the current map page"""
    if data:
        return RAC3_REGION_DATA_TABLE[data].ID
    return RAC3_REGION_DATA_TABLE[RAC3REGION.GALAXY].ID


tracker_world: dict[str, Any] = {
    "map_page_maps": "tracker/maps.json",
    "map_page_locations": "tracker/locations.json",
    "map_page_setting_key": r"rac3_current_planet_{player}_{team}",
    "map_page_index": map_page_index,
    "poptracker_name_mapping": UT_MAPPING,
}

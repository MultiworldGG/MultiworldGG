"""This module contains UnitTesting for the Goal condition"""

from BaseClasses import CollectionState
from Options import Accessibility, DeathLink, PlandoItem, ProgressionBalancing
from worlds.rac3.options.prog_wrench_options import ProgressiveWrench
from worlds.rac3.options.skillpoints_pick_and_mix_options import SkillPointsPickAndMix
from worlds.rac3.constants.event import RAC3EVENT
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.general import RAC3LOCATION
from worlds.rac3.constants.region import RAC3REGION
from worlds.rac3.options.arena_options import Arena
from worlds.rac3.options.armor_upgrade_options import ArmorUpgrade
from worlds.rac3.options.armor_vendor_options import ArmorVendors
from worlds.rac3.options.bonus_vidcomic_health_options import BonusVidComicHealthUpgrades
from worlds.rac3.options.clank_options import ClankOptions
from worlds.rac3.options.deathlink_behavior_options import DeathlinkBehavior
from worlds.rac3.options.filler_magnitude_options import FillerMagnitude
from worlds.rac3.options.filler_weight_options import FillerWeight
from worlds.rac3.options.generation_behavior_options import GenerationBehavior
from worlds.rac3.options.goal_bio_options import GoalBio
from worlds.rac3.options.goal_boss_gears_options import GoalBossGears
from worlds.rac3.options.goal_boss_klunk_options import GoalBossKlunk
from worlds.rac3.options.goal_boss_noid_options import GoalBossNoid
from worlds.rac3.options.goal_boss_qwark_options import GoalBossQwark
from worlds.rac3.options.goal_boss_scorpio_options import GoalBossScorpio
from worlds.rac3.options.goal_boss_talos_options import GoalBossTalos
from worlds.rac3.options.goal_boss_two_options import GoalBossTwo
from worlds.rac3.options.goal_boss_warship_options import GoalBossWarship
from worlds.rac3.options.goal_crystal_options import GoalCrystal
from worlds.rac3.options.goal_museum_options import GoalMuseum
from worlds.rac3.options.goal_nano_options import GoalNano
from worlds.rac3.options.goal_nef_options import GoalNef
from worlds.rac3.options.goal_percentage_options import GoalCompletion
from worlds.rac3.options.goal_planets_options import GoalPlanets
from worlds.rac3.options.goal_qwark_options import GoalQwark
from worlds.rac3.options.goal_skillpoints_options import GoalSkillpoints
from worlds.rac3.options.goal_tbolts_options import GoalTbolts
from worlds.rac3.options.helpdesk_options import HelpDesk
from worlds.rac3.options.lock_cc_options import LockCommandCenter
from worlds.rac3.options.multiplier_options import BoltAndXPMultiplier
from worlds.rac3.options.nanotech_limitation_options import NanotechLimitation
from worlds.rac3.options.nanotech_options import NanotechMilestones
from worlds.rac3.options.ngplus_item_options import NGPlusItems
from worlds.rac3.options.ngplus_start_options import NGPlusStart
from worlds.rac3.options.ngplus_vendor_options import NGPlusVendor
from worlds.rac3.options.one_hp_options import OneHpChallenge
from worlds.rac3.options.prog_weapons_options import ProgressiveWeapons
from worlds.rac3.options.rangers_options import Rangers
from worlds.rac3.options.ratchet_skins_options import RatchetSkin
from worlds.rac3.options.scout_vendors_options import ScoutVendors
from worlds.rac3.options.sewer_limitation_options import SewerLimitation
from worlds.rac3.options.sewer_options import SewerCrystals
from worlds.rac3.options.ship_nose_options import ShipNose
from worlds.rac3.options.ship_skin_options import ShipSkin
from worlds.rac3.options.ship_vendor_options import ShipVendors
from worlds.rac3.options.ship_wings_options import ShipWings
from worlds.rac3.options.shortcuts_options import Shortcuts
from worlds.rac3.options.skillpoints_options import SkillPoints
from worlds.rac3.options.speedups_options import Speedups
from worlds.rac3.options.starting_weapons_options import StartingWeapons
from worlds.rac3.options.titanium_bolts_options import TitaniumBolts
from worlds.rac3.options.trap_magitude_options import TrapMagnitude
from worlds.rac3.options.trap_weight_options import TrapWeight
from worlds.rac3.options.traps_options import EnableTraps
from worlds.rac3.options.trophies_options import Trophies
from worlds.rac3.options.vendor_access_options import VendorAccess
from worlds.rac3.options.vidcomic_health_options import VidComicHealthUpgrades
from worlds.rac3.options.vidcomics_options import VidComics
from worlds.rac3.options.vr_challenges_options import VRChallenges
from worlds.rac3.options.weapon_mods_options import WeaponMods
from worlds.rac3.options.weapon_vendors_options import WeaponVendors
from worlds.rac3.test.base import RAC3TestBase


class TestDefaults(RAC3TestBase):
    options = {
        # "deathlink": DeathLink.default,
        # "start_inventory_from_pool": StartInventoryPool.default,
        # "generation_behavior": GenerationBehavior.default,
        # "starting_weapons": StartingWeapons.default,
        # "bolt_and_xp_multiplier": BoltAndXPMultiplier.default,
        # "progressive_weapons": ProgressiveWeapons.default,
        # "weapon_mods": WeaponMods.default,
        # "progressive_wrench": ProgressiveWrench.default,
        # "armor_upgrade": ArmorUpgrade.default,
        # "filler_weight": FillerWeight.default,
        # "traps_enabled": EnableTraps.default,
        # "trap_weight": TrapWeight.default,
        # "trap_magnitude": TrapMagnitude.default,
        # "filler_magnitude": FillerMagnitude.default,
        # "weapon_vendors": WeaponVendors.default,
        # "skill_points": SkillPoints.default,
        # "skill_points_pick_and_mix": SkillPointsPickAndMix.default
        # "trophies": Trophies.default,
        # "titanium_bolts": TitaniumBolts.default,
        # "rangers": Rangers.default,
        # "vidcomics": VidComics.default,
        # "vr_challenges": VRChallenges.default,
        # "arena": Arena.default,
        # "sewer_crystals": SewerCrystals.default,
        # "sewer_limitation": SewerLimitation.default,
        # "nanotech_milestones": NanotechMilestones.default,
        # "nanotech_limitation": NanotechLimitation.default,
        # "exclude_locations": RAC3ExcludeLocations.default,
        # "ship_nose": ShipNose.default,
        # "ship_wings": ShipWings.default,
        # "ship_skin": ShipSkin.default,
        # "player_skin": RatchetSkin.default,
        # "one_hp_challenge": OneHpChallenge.default,
        # "clank_options": ClankOptions.default,
        # "ship_vendor": ShipVendors.default,
        # "armor_vendor": ArmorVendors.default,
        # "scout_vendors": ScoutVendors.default,
        # "shortcuts": Shortcuts.default,
        # "speedups": Speedups.default,
        # "ngplus_items": NGPlusItems.default,
        # "ngplus_vendors": NGPlusVendor.default,
        # "ngplus_start": NGPlusStart.default,
        # "helpdesk": HelpDesk.default,
        # "vendor_access": VendorAccess.default,
        # "weapon_level_locations": WeaponLevels.default,
        # "bonus_vidcomic_health": BonusVidComicHealthUpgrades.default,
        # "vidcomic_health_upgrades": VidComicHealthUpgrades.default,
        # "deathlink_behavior": DeathlinkBehavior.default,
        # "lock_command_center": LockCommandCenter.default,
        # "goal_bio": GoalBio.default,
        # "goal_nef": GoalNef.default,
        # "goal_nano": GoalNano.default,
        # "goal_crystal": GoalCrystal.default,
        # "goal_tbolts": GoalTbolts.default,
        # "goal_skillpoints": GoalSkillpoints.default,
        # "goal_qwark": GoalQwark.default,
        # "goal_museum": GoalMuseum.default,
        # "goal_planets": GoalPlanets.default,
        # "goal_completion": GoalCompletion.default,
        # "goal_boss_qwark": GoalBossQwark.default,
        # "goal_boss_two": GoalBossTwo.default,
        # "goal_boss_noid": GoalBossNoid.default,
        # "goal_boss_warship": GoalBossWarship.default,
        # "goal_boss_scorpio": GoalBossScorpio.default,
        # "goal_boss_talos": GoalBossTalos.default,
        # "goal_boss_gears": GoalBossGears.default,
        # "goal_boss_klunk": GoalBossKlunk.default,

        # "progression_balancing": ProgressionBalancing.default,
        # "accessibility": Accessibility.default,
        # "local_items": LocalItems.default,
        # "non_local_items": NonLocalItems.default,
        # "start_inventory": StartInventory.default,
        # "start_hints": StartHints.default,
        # "start_location_hints": StartLocationHints.default,
        # "priority_locations": PriorityLocations.default,
        # "item_links": ItemLinks.default,
        # "plando_items": PlandoItems.default,
    }

    def test_beatable(self):
        state: CollectionState = self.multiworld.state.copy()
        with self.subTest("No items collected test"):
            self.assertTrue(self.can_reach_region(RAC3REGION.VELDIN), "Can't start on Veldin")
            self.assertFalse(self.can_reach_region(RAC3REGION.FLORANA), "Florana reachable without coordinates")
            self.assertTrue(self.can_reach_region(RAC3REGION.STARSHIP_PHOENIX),
                            "Starship Phoenix not reachable from start")
            self.assertFalse(self.can_reach_location(RAC3LOCATION.COMMAND_CENTER_INFOBOT),
                             "Command Center Infobot collectable too early")
            self.assertFalse(self.can_reach_region(RAC3REGION.COMMAND_CENTER), "Command Center reachable from Veldin")
            self.assertFalse(self.can_reach_location(RAC3EVENT.VICTORY[0]), "Goal location reachable from Start")
            self.assertBeatable(False)
        with self.subTest("Sphere 1 collected test"):
            state.sweep_for_advancements()
            # self.assertTrue(self.can_reach_region(RAC3REGION.FLORANA), "Can't reach Florana from Veldin")
            # self.assertTrue(self.can_reach_region(RAC3REGION.STARSHIP_PHOENIX), "Can't reach Starship Phoenix from
            # Veldin")
            self.assertFalse(self.can_reach_region(RAC3REGION.COMMAND_CENTER), "Command Center reachable from Florana")
            self.assertFalse(self.can_reach_location(RAC3EVENT.VICTORY[0]), "Goal location reachable from Florana")
            self.assertBeatable(False)
        with self.subTest("Command Center access test"):
            self.collect_by_name(RAC3ITEM.COMMAND_CENTER)
            self.assertTrue(self.can_reach_region(RAC3REGION.COMMAND_CENTER),
                            "Can't reach Command Center with coordinates")
            self.assertFalse(self.can_reach_location(RAC3EVENT.VICTORY[0]), "Goal location reachable with no items")
            self.assertBeatable(False)
        with self.subTest("Biobliterator access test"):
            self.collect_by_name([RAC3ITEM.HYPERSHOT, RAC3ITEM.GRAV_BOOTS, RAC3ITEM.TYHRRA_GUISE, RAC3ITEM.HACKER,
                                  RAC3ITEM.REFRACTOR])
            self.assertTrue(self.can_reach_location(RAC3EVENT.NANOTECH[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.SEWER[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.SKILLS[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.T_BOLT[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.PLANETS[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.COMPLETION[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.CC_ACCESS[0]), "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.COMMAND_CENTER_NEFARIOUS[0]),
                            "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.COMMAND_CENTER_BIOBLITERATOR[0]),
                            "Goal location not reachable with items")
            self.assertTrue(self.can_reach_location(RAC3EVENT.VICTORY[0]), "Goal location not reachable with items")
            self.assertBeatable(True)

    def test_event_duplicates(self):
        names: dict[str, str] = {}
        for location in self.multiworld.get_locations(self.player):
            item = location.item
            if item is None:
                continue
            with self.subTest(f"Location {location.name}"):
                self.assertIsNotNone(item, f"{location.name} contains no item")
                if item.name not in self.multiworld.worlds[self.player].item_name_to_id.keys():
                    self.assertNotIn(item.name, names.values(), f"Event {item.name} not unique")
                    names[location.name] = item.name


class TestNotDefault(RAC3TestBase):
    options = {
        "deathlink": DeathLink.option_true,
        "start_inventory_from_pool": {RAC3ITEM.TYHRRA_GUISE: 1},
        "generation_behavior": GenerationBehavior.option_error,
        "starting_weapons": dict.fromkeys(StartingWeapons.valid_keys, StartingWeapons.max),
        "bolt_and_xp_multiplier": BoltAndXPMultiplier.option_x16,
        "progressive_weapons": ProgressiveWeapons.option_automatic_leveling,
        "weapon_mods": WeaponMods.option_individual_mods,
        "progressive_wrench": ProgressiveWrench.option_enabled,
        "armor_upgrade": ArmorUpgrade.range_end,
        "filler_weight": dict.fromkeys(FillerWeight.default.keys(), FillerWeight.max),
        "traps_enabled": EnableTraps.option_true,
        "trap_weight": dict.fromkeys(TrapWeight.valid_keys, TrapWeight.max),
        "trap_magnitude": dict.fromkeys(TrapMagnitude.valid_keys, TrapMagnitude.max),
        "filler_magnitude": dict.fromkeys(FillerMagnitude.valid_keys, FillerMagnitude.max),
        "weapon_vendors": WeaponVendors.option_false,
        "skill_points": SkillPoints.option_all,
        "skill_points_pick_and_mix": SkillPointsPickAndMix.valid_keys,
        "trophies": Trophies.option_all,
        "titanium_bolts": TitaniumBolts.option_false,
        "rangers": Rangers.option_story_missions,
        "vidcomics": VidComics.option_false,
        "vr_challenges": VRChallenges.option_false,
        "arena": Arena.option_second_only,
        "sewer_crystals": SewerCrystals.option_all,
        "sewer_limitation": SewerLimitation.range_end,
        "nanotech_milestones": NanotechMilestones.option_all,
        "nanotech_limitation": NanotechLimitation.range_end,
        "exclude_locations": set(),
        "ship_nose": ShipNose.option_scoop,
        "ship_wings": ShipWings.option_heavy_ordinance,
        "ship_skin": ShipSkin.option_Zeldren_Sunset,
        "player_skin": RatchetSkin.option_constructo_bot,
        "one_hp_challenge": dict.fromkeys(OneHpChallenge.valid_keys, 1),
        "clank_options": ClankOptions.option_shuffled_progressive,
        "ship_vendor": ShipVendors.option_false,
        "armor_vendor": ArmorVendors.option_false,
        "scout_vendors": dict.fromkeys(ScoutVendors.valid_keys, 1),
        "shortcuts": dict.fromkeys(Shortcuts.valid_keys, 1),
        "speedups": dict.fromkeys(Speedups.valid_keys, 1),
        "ngplus_items": NGPlusItems.option_true,
        "ngplus_vendors": NGPlusVendor.option_true,
        "ngplus_start": NGPlusStart.option_enabled_with_multiplier,
        "helpdesk": HelpDesk.option_false,
        "vendor_access": VendorAccess.option_infobot,
        "weapon_level_locations": frozenset({"V2, V3, V4, V5"}),
        "bonus_vidcomic_health": BonusVidComicHealthUpgrades.range_start,
        "vidcomic_health_upgrades": VidComicHealthUpgrades.option_false,
        "deathlink_behavior": DeathlinkBehavior.option_nanopak_save,
        "lock_command_center": LockCommandCenter.option_true,
        "goal_bio": GoalBio.option_false,
        "goal_nef": GoalNef.option_true,
        "goal_nano": GoalNano.range_end,
        "goal_crystal": GoalCrystal.range_end,
        "goal_tbolts": GoalTbolts.range_end,
        "goal_skillpoints": GoalSkillpoints.range_end,
        "goal_qwark": GoalQwark.option_true,
        "goal_museum": GoalMuseum.option_true,
        "goal_planets": GoalPlanets.range_end,
        "goal_completion": GoalCompletion.range_end,
        "goal_boss_qwark": GoalBossQwark.option_true,
        "goal_boss_two": GoalBossTwo.option_true,
        "goal_boss_noid": GoalBossNoid.option_true,
        "goal_boss_warship": GoalBossWarship.option_true,
        "goal_boss_scorpio": GoalBossScorpio.option_true,
        "goal_boss_talos": GoalBossTalos.option_true,
        "goal_boss_gears": GoalBossGears.option_true,
        "goal_boss_klunk": GoalBossKlunk.option_true,

        "progression_balancing": ProgressionBalancing.range_end,
        "accessibility": Accessibility.option_minimal,
        "local_items": {RAC3ITEM.HACKER},
        "non_local_items": {RAC3ITEM.CHARGE_BOOTS},
        "start_inventory": {RAC3ITEM.HYPERSHOT: 1},
        "start_hints": {RAC3ITEM.COMMAND_CENTER},
        "start_location_hints": {RAC3LOCATION.DAXX_FACILITY},
        "priority_locations": {RAC3LOCATION.DAXX_CHARGE_BOOTS},
        "item_links": [{
            "name": RAC3ITEM.PROGRESSIVE_ARMOR,
            "item_pool": [RAC3ITEM.PROGRESSIVE_PACK],
            "replacement_item": RAC3ITEM.GRAV_BOOTS,
        }],
        "plando_items": [PlandoItem(
            items=[RAC3ITEM.INFECTOR],
            locations=[RAC3LOCATION.PHOENIX_MEET_SASHA],
            world=1,
            from_pool=False,
            force=True,
            count=1,
            percentage=100)],
    }

    def test_options_match(self):
        """Test every option value used for generation was the value defined"""
        for name, option in self.options.items():
            if name in ["filler_weight", "goal_tbolts", "goal_skillpoints", "goal_museum", "goal_planets"]:
                continue
            with self.subTest(f"Test match: {name}"):
                self.assertEqual(option, getattr(self.world.options, name).value,
                                 f"{name} set to {getattr(self.world.options, name).value}, but it should be {option}")

    def test_not_default(self):
        """Test every option is not the default value"""
        options = self.world.options.__dict__
        for name, option in options.items():
            if name in ["goal_museum"]:
                continue
            with self.subTest(f"Test not default: {name}"):
                self.assertNotEqual(option, getattr(self.world.options, name).default,
                                    f"{name} is still the default value {option}, add test cases")

    def test_goal_items_placed(self):
        """Test that the required items to beat the game have been placed somewhere"""
        infobot: bool = False
        starting_pool = {*self.world.options.start_inventory.value.keys(),
                         *self.world.options.start_inventory_from_pool.value.keys()}
        if RAC3ITEM.COMMAND_CENTER in starting_pool:
            infobot = True
            self.assertTrue(infobot, "Infobot item was started with, but not??????")
        items = [getattr(self.world.get_location(RAC3LOCATION.COMMAND_CENTER_INFOBOT).item, "name", None)]
        locations = []
        if RAC3ITEM.COMMAND_CENTER in items:
            infobot = True
            self.assertTrue(infobot, "Infobot item was placed, but not found??????")
        iterate = 0
        for loc in self.world.get_locations():
            iterate += 1
            if infobot:
                break
            if loc.item is None:
                continue
            if loc.item.name == RAC3ITEM.COMMAND_CENTER:
                infobot = True
                locations += [loc.name]
                self.assertTrue(infobot, f"Infobot item found at {loc.name}, but doesn't count??????")
                continue
            with self.subTest(f"Empty: {loc.name}"):
                self.assertTrue(loc.item, f"{loc.name} had no item")
        with self.subTest("Search for Command Center Infobot"):
            self.assertTrue(infobot,
                            f"{RAC3ITEM.COMMAND_CENTER} not found with value {infobot}, items placed were: {items}, "
                            f"locations found: {locations}")

    def test_inaccessible_goal_skip(self):
        state = self.multiworld.get_all_state()
        state.sweep_for_advancements()
        for loc in self.multiworld.get_locations():
            if loc.address:
                with self.subTest(f"Location: {loc.name}"):
                    self.assertTrue(loc.can_reach(state), f"logic not met: {loc.access_rule}")
            else:
                with self.subTest(f"Event: {loc.name}"):
                    self.assertTrue(loc.can_reach(state), f"logic not met: {loc.access_rule}")

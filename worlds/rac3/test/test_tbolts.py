"""This module contains UnitTesting for the Titanium Bolt Options"""

from BaseClasses import CollectionState
from worlds.rac3.constants.event import RAC3EVENT
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.constants.locations.trophies import RAC3TROPHY
from worlds.rac3.options.arena_options import Arena
from worlds.rac3.options.ngplus_item_options import NGPlusItems
from worlds.rac3.options.rangers_options import Rangers
from worlds.rac3.options.titanium_bolts_options import TitaniumBolts
from worlds.rac3.options.trophies_options import Trophies
from worlds.rac3.options.vidcomics_options import VidComics
from worlds.rac3.options.vr_challenges_options import VRChallenges
from worlds.rac3.test.base import RAC3TestBase


class TestNoTBoltLocs(RAC3TestBase):
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
        # "skill_points_pick_and_mix": SkillPointsPickAndMix.default,
        # "trophies": Trophies.default,
        "titanium_bolts": TitaniumBolts.option_false,
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
    }
    run_default_tests = False

    def test_dont_exist(self):
        with self.subTest(f"Test items dont exist"):
            self.assertFalse(self.get_items_by_name(RAC3ITEM.TITANIUM_BOLT),
                             "Titanium Bolts added to the pool when they should not")
        for loc in self.world.location_name_groups[RAC3TAG.T_BOLT]:
            with self.subTest(f"Test {loc} does not exist"):
                try:
                    self.world.get_location(loc)
                except KeyError:
                    continue
                else:
                    if self.world.get_location(loc).address:
                        self.fail(f"{loc} should not exist, but does")


class TestTBoltLocs(RAC3TestBase):
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
        # "weapon_vendors": WeaponVendors.default,
        # "skill_points": SkillPoints.default,
        # "skill_points_pick_and_mix": SkillPointsPickAndMix.default,
        "trophies": Trophies.option_all,
        "titanium_bolts": TitaniumBolts.option_true,
        "rangers": Rangers.option_all,
        "vidcomics": VidComics.option_true,
        "vr_challenges": VRChallenges.option_true,
        "arena": Arena.option_all,
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
        "ngplus_items": NGPlusItems.option_true,
        # "ngplus_vendors": NGPlusVendor.default,
        # "ngplus_start": NGPlusStart.default,
        # "helpdesk": HelpDesk.default,
        # "vendor_access": VendorAccess.default,
        # "weapon_level_locations": WeaponLevels.default,
        # "bonus_vidcomic_health": BonusVidComicHealthUpgrades.default,
        # "vidcomic_health_upgrades": VidComicHealthUpgrades.default,
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
    }

    def test_locations_start(self):
        for loc in self.world.location_name_groups[RAC3TAG.T_BOLT]:
            with self.subTest(f"Test {loc} exists and is not reachable"):
                try:
                    self.world.get_location(loc)
                except KeyError:
                    self.fail(f"{loc} should exist, but it doesn't.")
                self.assertFalse(self.can_reach_location(loc), f"{loc} was reached with no items")

    def test_tbolt_trophy(self):
        with self.subTest("Test there are 40 Titanium Bolts in the pool"):
            count = len(self.get_items_by_name(RAC3ITEM.TITANIUM_BOLT))
            self.assertEqual(count, 40, f"Counted {count} Titanium Bolts in the pool when there should be 40")
        with self.subTest("Test Titanium Collector Trophy Dependency"):
            self.assertAccessDependency([RAC3TROPHY.PHOENIX_TITANIUM_COLLECTOR], [[RAC3ITEM.TITANIUM_BOLT]],
                                        only_check_listed=True)

    def test_locations_all(self):
        state: CollectionState = self.multiworld.state
        self.collect_all_but(RAC3EVENT.VICTORY[1], state)
        for loc in self.world.location_name_groups[RAC3TAG.T_BOLT]:
            with self.subTest(f"Check {loc}"):
                self.assertTrue(self.can_reach_location(loc), f"{loc} was not reachable with all items collected")
        self.assertTrue(self.can_reach_location(RAC3EVENT.VICTORY[0]), "Cannot reach the goal")

"""This module contains UnitTesting for the Goal condition"""
from options.skillpoints_pick_and_mix_options import SkillPointsPickAndMix
from worlds.rac3.constants.event import ALL_GOALS, ALL_PLANETS, RAC3EVENT
from worlds.rac3.constants.items import RAC3ITEM
from worlds.rac3.constants.locations.tags import RAC3TAG
from worlds.rac3.locations import location_groups
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
from worlds.rac3.options.lock_cc_options import LockCommandCenter
from worlds.rac3.options.ngplus_item_options import NGPlusItems
from worlds.rac3.options.vidcomics_options import VidComics
from worlds.rac3.test.base import RAC3TestBase


class TestAllGoals(RAC3TestBase):
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
        # "titanium_bolts": TitaniumBolts.default,
        # "rangers": Rangers.default,
        "vidcomics": VidComics.option_true,
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
        "ngplus_items": NGPlusItems.option_true,
        # "ngplus_vendors": NGPlusVendor.default,
        # "ngplus_start": NGPlusStart.default,
        # "helpdesk": HelpDesk.default,
        # "vendor_access": VendorAccess.default,
        # "weapon_level_locations": WeaponLevels.default,
        # "bonus_vidcomic_health": BonusVidComicHealthUpgrades.default,
        # "vidcomic_health_upgrades": VidComicHealthUpgrades.default,
        # "deathlink_behavior": DeathlinkBehavior.default,
        "lock_command_center": LockCommandCenter.option_false,
        "goal_bio": GoalBio.option_true,
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

    def test_each_goal(self):
        state = self.multiworld.get_all_state()
        for event in ALL_GOALS:
            with self.subTest(event):
                self.assertTrue(state.can_reach_location(event, self.player), f"{event} cannot be reached")

        with self.subTest("Completion Percentage"):
            total = {loc for loc in self.world.get_locations() if loc.address and
                     loc.name not in {RAC3EVENT.COMMAND_CENTER_NEFARIOUS[0], RAC3EVENT.COMMAND_CENTER_BIOBLITERATOR[0]}}
            reachable = set()
            unreachable = set()
            for loc in total:
                if loc.can_reach(state):
                    reachable.add(loc.name)
                else:
                    unreachable.add(loc.name)
            total = len(total)
            reachable = len(reachable)
            msg = (f"{reachable}/{total} ({100 * reachable / total}%), but {self.world.options.goal_completion}% is "
                   f"required, missing {total - reachable} locations: {unreachable}")
            self.assertTrue(reachable / total >= self.world.options.goal_completion / 100, msg)

        with self.subTest("Planet Completion"):
            planets = set()
            for planet in ALL_PLANETS:
                if state.has(planet, self.player):
                    planets.add(planet)
            msg = (f"{len(planets)}/{self.world.options.goal_planets} planets completed, could not complete: "
                   f"{planets.difference(ALL_PLANETS)}")
            self.assertTrue(len(planets) >= self.world.options.goal_planets, msg)

        with self.subTest("Nanotech"):
            pass
        with self.subTest("Crystals"):
            pass
        with self.subTest("Titanium Bolts"):
            msg = (f"{state.count(RAC3ITEM.TITANIUM_BOLT, self.player)}/{self.world.options.titanium_bolts.value}"
                   f"Titanium bolts available")
            self.assertTrue(state.has(RAC3ITEM.TITANIUM_BOLT, self.player, self.world.options.titanium_bolts.value),
                            msg)

        with self.subTest("Skillpoints"):
            count, total = 0, 0
            locations = [loc.name for loc in self.world.get_locations() if
                         loc.name in location_groups[RAC3TAG.SKILLPOINT]]
            for _i, loc in enumerate(locations):
                total = _i
                if state.can_reach_location(loc, self.player):
                    count += 1
            msg = (f"{count}/{self.world.options.goal_skillpoints.value} Skill points collected, with "
                   f"{1 + total - count} remaining out of logic")
            # Todo: This test needs turning back on once RuleBuilder rework allows testing for each logic option even
            #  when they are not included in the current generation.
            self.assertTrue(count >= self.world.options.goal_skillpoints.value, msg)

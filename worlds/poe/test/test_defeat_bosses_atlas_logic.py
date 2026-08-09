"""
Reproduction for reported bug: defeat_bosses goal with a mix of campaign and
atlas/pinnacle bosses in bosses_available never opens logic past early Act 1.

Reporter: Erbs, AP After Dark discord, 2026-07-09. Attached yaml (erbs-poe.yaml):

    goal: defeat_bosses
    number_of_bosses: 10
    bosses_available: [hydra, phoenix, chimera, minotaur, shaper, uber_shaper,
        elder, uber_elder, uber_uber_elder, atziri, uber_atziri, al-hezmin, baran, drox,
        veritania, sirus, uber_sirus, maven, uber_maven, exarch, uber_exarch,
        eater, uber_eater, incarnation_of_neglect, uber_incarnation_of_neglect,
        incarnation_of_fear, uber_incarnation_of_fear, incarnation_of_dread,
        uber_incarnation_of_dread, cortex, uber_cortex]
    progression_balancing: 0
    accessibility: full
    death_link: true
    ascendancies_available_per_class: 3
    usable_starting_gear: starting_weapon
    gear_upgrades_per_act: 8
    flasks_per_act: 1
    max_links_per_act: 5
    skill_gems_per_act: 3
    support_gems_per_act: 2

Player reported: tracker shows only "sphere 1" (early Act 1) in logic
regardless of items received, despite having substantial gear already
(rare weapon, several 3-5 link items per gear-status screenshot).

If this is a genuine logic bug, even the fully-collected all-items state
(WorldTestBase.test_all_state_can_reach_everything, run automatically for
every options combo below) should fail to reach every location / fail
Beatable. If it passes, the world is technically completable and the
player's confusion is a yaml-tuning/progression_balancing issue rather
than a code bug — this test's *result* is the actual repro artifact,
not just its existence.
"""

from . import PoeTestBase


ERBS_BOSSES_AVAILABLE = [
    "hydra", "phoenix", "chimera", "minotaur", "shaper", "uber_shaper",
    "elder", "uber_elder", "uber_uber_elder", "atziri", "uber_atziri", "al-hezmin", "baran",
    "drox", "veritania", "sirus", "uber_sirus", "maven", "uber_maven",
    "exarch", "uber_exarch", "eater", "uber_eater", "incarnation_of_neglect",
    "uber_incarnation_of_neglect", "incarnation_of_fear", "uber_incarnation_of_fear",
    "incarnation_of_dread", "uber_incarnation_of_dread", "cortex", "uber_cortex",
]


class TestDefeatBossesWithAtlasBossesReported(PoeTestBase):
    """Exact options reported by Erbs (7/9/2026) minus non_local_items
    (irrelevant to single-player reachability) and death_link (irrelevant
    to logic). Uses default starting_character since it wasn't in the
    reported yaml."""
    options = {
        "goal": "defeat_bosses",
        "number_of_bosses": 10,
        "bosses_available": ERBS_BOSSES_AVAILABLE,
        "progression_balancing": 0,
        "accessibility": "full",
        "ascendancies_available_per_class": 3,
        "usable_starting_gear": "starting_weapon",
        "gear_upgrades_per_act": 8,
        "flasks_per_act": 1,
        "max_links_per_act": 5,
        "skill_gems_per_act": 3,
        "support_gems_per_act": 2,
    }

    def test_goal_act_is_set_to_endgame(self):
        """Sanity check: defeat_bosses should map to the endgame/act-11 goal act."""
        self.assertEqual(self.multiworld.worlds[1].goal_act, 11,
                         "defeat_bosses should resolve to goal_act 11 (beyond campaign)")

    def test_bosses_for_goal_includes_atlas_only_bosses(self):
        """Sanity check: the sampled goal bosses actually include atlas-only bosses,
        confirming this reproduces the reported yaml combo (not just campaign bosses)."""
        world = self.multiworld.worlds[1]
        atlas_only = {"uber_shaper", "sirus", "uber_sirus", "maven", "uber_maven",
                       "exarch", "uber_exarch", "eater", "uber_eater", "cortex",
                       "uber_cortex", "uber_uber_elder"}
        self.assertTrue(set(world.bosses_for_goal) & atlas_only,
                        f"Expected at least one atlas-only boss sampled for the goal; got: {world.bosses_for_goal}")

    # test_all_state_can_reach_everything (from WorldTestBase) runs automatically
    # for this class and is the actual reproduction: it fails if any location,
    # including the boss/atlas locations, is unreachable even with every item
    # in the pool collected.


class TestDefeatBossesCampaignBossesOnlyControl(PoeTestBase):
    """Control: same options but restricted to campaign-reachable bosses only
    (no atlas/pinnacle bosses). If this passes while the class above fails,
    that isolates the break to atlas-only boss locations specifically."""
    options = {
        "goal": "defeat_bosses",
        "number_of_bosses": 4,
        "bosses_available": ["atziri", "al-hezmin", "baran", "drox", "veritania"],
        "progression_balancing": 0,
        "accessibility": "full",
        "ascendancies_available_per_class": 3,
        "usable_starting_gear": "starting_weapon",
        "gear_upgrades_per_act": 8,
        "flasks_per_act": 1,
        "max_links_per_act": 5,
        "skill_gems_per_act": 3,
        "support_gems_per_act": 2,
    }

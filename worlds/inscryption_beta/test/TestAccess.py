from . import InscryptionTestBase
from ..Rules import InscryptionRules, WOODLANDS_BATTLE, WOODLANDS_BOSS, LATER_BATTLE, LATER_BOSS


class AccessTestGeneral(InscryptionTestBase):

    def test_dagger(self) -> None:
        self.assertAccessDependency(["Act 1 - Magnificus Eye"], [["Dagger"]])

    def test_caged_wolf(self) -> None:
        self.assertAccessDependency(["Act 1 - Dagger"], [["Caged Wolf Card"]])

    def test_magnificus_eye(self) -> None:
        self.assertAccessDependency(["Act 1 - Clock Main Compartment"], [["Magnificus Eye"]])

    def test_wardrobe_key(self) -> None:
        self.assertAccessDependency(
            ["Act 1 - Wardrobe Drawer 1", "Act 1 - Wardrobe Drawer 2",
             "Act 1 - Wardrobe Drawer 3", "Act 1 - Wardrobe Drawer 4"],
            [["Wardrobe Key"]]
        )

    def test_ancient_obol(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Bone Lord Femur", "Act 2 - Bone Lord Horn", "Act 2 - Bone Lord Holo Key"],
            [["Ancient Obol"]]
        )

    def test_holo_pelt(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Trader 1", "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5"],
            [["Holo Pelt"]]
        )

    def test_inspectometer_battery(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Trader 1", "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5",
             "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt", "Act 3 - Forest Holo Pelt", "Act 3 - Clock",
             "Act 3 - Crypt Holo Pelt", "Act 3 - Gems Drone", "Act 3 - Nano Armor Generator", "Act 3 - Extra Battery",
             "Act 3 - Tower Holo Pelt", "Act 3 - The Great Transcendence", "Act 3 - Boss Mycologists",
             "Act 3 - Bone Lord Room", "Act 3 - Well", "Act 3 - Luke's File Entry 1", "Act 3 - Luke's File Entry 2",
             "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4", "Act 3 - Goobert's Painting"],
            [["Inspectometer Battery"]]
        )

    def test_gem_drone(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Unfinished", "Act 3 - Boss G0lly", "Act 3 - Trader 1", "Act 3 - Trader 2",
             "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Shop Holo Pelt", "Act 3 - Clock",
             "Act 3 - Tower Holo Pelt", "Act 3 - The Great Transcendence", "Act 3 - Luke's File Entry 4",
             "Act 3 - Nano Armor Generator", "Act 3 - Goobert's Painting"],
            [["Gems Module"]]
        )

    def test_mycologists_holo_key(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Mycologists"],
            [["Mycologists Holo Key"]]
        )

    def test_bone_lord_holo_key(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Bone Lord Room"],
            [["Bone Lord Holo Key"]]
        )

    def test_quill(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Archivist", "Act 3 - The Great Transcendence",
             "Act 3 - Luke's File Entry 1", "Act 3 - Luke's File Entry 2",
             "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4"],
            [["Quill"]]
        )


class AccessTestOrdered(InscryptionTestBase):
    options = {
        "act_unlocks": 0,
    }

    def test_film_roll(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper", "Act 2 - Battle Sawyer",
             "Act 2 - Battle Royal", "Act 2 - Battle Kaycee", "Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert",
             "Act 2 - Battle Lonely Wizard", "Act 2 - Battle Inspector", "Act 2 - Battle Melter",
             "Act 2 - Battle Dredger", "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Forest Meadow Chest", "Act 2 - Forest Cabin Chest", "Act 2 - Cabin Wardrobe Drawer",
             "Act 2 - Cabin Safe", "Act 2 - Crypt Casket 1", "Act 2 - Crypt Casket 2", "Act 2 - Crypt Well",
             "Act 2 - Camera Replica", "Act 2 - Clover", "Act 2 - Epitaph Piece 1", "Act 2 - Epitaph Piece 2",
             "Act 2 - Epitaph Piece 3", "Act 2 - Epitaph Piece 4", "Act 2 - Epitaph Piece 5", "Act 2 - Epitaph Piece 6",
             "Act 2 - Epitaph Piece 7", "Act 2 - Epitaph Piece 8", "Act 2 - Epitaph Piece 9", "Act 2 - Dock Chest",
             "Act 2 - Tentacle", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1",
             "Act 2 - Ancient Obol", "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle", "Act 2 - Boss Leshy",
             "Act 2 - Boss Grimora", "Act 2 - Boss Magnificus", "Act 2 - Boss P03", "Act 2 - Mycologists Holo Key",
             "Act 2 - Bone Lord Femur", "Act 2 - Bone Lord Horn", "Act 2 - Bone Lord Holo Key",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Film Roll"]]
        )

    def test_epitaphs_and_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Battle Inspector", "Act 2 - Battle Melter", "Act 2 - Battle Dredger",
             "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3", "Act 2 - Forest Meadow Chest",
             "Act 2 - Tentacle", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1", "Act 2 - Ancient Obol",
             "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle", "Act 2 - Boss Leshy",
             "Act 2 - Boss Grimora", "Act 2 - Boss Magnificus", "Act 2 - Boss P03", "Act 2 - Mycologists Holo Key",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Epitaph Piece", "Camera Replica", "Pile Of Meat"]]
        )

    def test_epitaphs(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Boss Grimora",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Epitaph Piece"]]
        )

    def test_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Boss Leshy", "Act 2 - Forest Meadow Chest",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Camera Replica", "Pile Of Meat"]]
        )

    def test_monocle(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Goobert", "Act 2 - Battle Pike Mage", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Boss Magnificus", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Tentacle", "Act 2 - Ancient Obol", "Act 2 - Mycologists Holo Key",
             "Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 3 - Boss Unfinished", "Act 3 - Boss G0lly",
             "Act 3 - Boss Mycologists", "Act 3 - Bone Lord Room", "Act 3 - Shop Holo Pelt", "Act 3 - Middle Holo Pelt",
             "Act 3 - Forest Holo Pelt", "Act 3 - Crypt Holo Pelt", "Act 3 - Tower Holo Pelt", "Act 3 - Trader 1",
             "Act 3 - Trader 2", "Act 3 - Trader 3", "Act 3 - Trader 4", "Act 3 - Trader 5", "Act 3 - Drawer 1",
             "Act 3 - Drawer 2", "Act 3 - Clock", "Act 3 - Extra Battery", "Act 3 - Nano Armor Generator",
             "Act 3 - Chest", "Act 3 - Goobert's Painting", "Act 3 - Luke's File Entry 1", "Act 3 - Gems Drone",
             "Act 3 - Luke's File Entry 2", "Act 3 - Luke's File Entry 3", "Act 3 - Luke's File Entry 4",
             "Act 3 - Inspectometer Battery", "Act 3 - Gems Drone", "Act 3 - The Great Transcendence", "Act 3 - Well"],
            [["Monocle"]]
        )


class AccessTestUnordered(InscryptionTestBase):
    options = {
        "act_unlocks": 1,
    }

    def test_epitaphs_and_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Battle Pike Mage", "Act 2 - Battle Goobert", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Battle Inspector", "Act 2 - Battle Melter", "Act 2 - Battle Dredger",
             "Act 2 - Tower Chest 1", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3", "Act 2 - Forest Meadow Chest",
             "Act 2 - Tentacle", "Act 2 - Factory Trash Can", "Act 2 - Factory Drawer 1", "Act 2 - Ancient Obol",
             "Act 2 - Factory Drawer 2", "Act 2 - Factory Chest 1", "Act 2 - Factory Chest 2",
             "Act 2 - Factory Chest 3", "Act 2 - Factory Chest 4", "Act 2 - Monocle", "Act 2 - Boss Leshy",
             "Act 2 - Boss Grimora", "Act 2 - Boss Magnificus", "Act 2 - Boss P03", "Act 2 - Mycologists Holo Key"],
            [["Epitaph Piece", "Camera Replica", "Pile Of Meat"]]
        )

    def test_epitaphs(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Boss Grimora"],
            [["Epitaph Piece"]]
        )

    def test_forest_items(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Prospector", "Act 2 - Battle Angler", "Act 2 - Battle Trapper",
             "Act 2 - Boss Leshy", "Act 2 - Forest Meadow Chest"],
            [["Camera Replica", "Pile Of Meat"]]
        )

    def test_monocle(self) -> None:
        self.assertAccessDependency(
            ["Act 2 - Battle Goobert", "Act 2 - Battle Pike Mage", "Act 2 - Battle Lonely Wizard",
             "Act 2 - Boss Magnificus", "Act 2 - Tower Chest 2", "Act 2 - Tower Chest 3",
             "Act 2 - Tentacle", "Act 2 - Ancient Obol", "Act 2 - Mycologists Holo Key"],
            [["Monocle"]]
        )

class AccessTestGrizzliesWithRandomizedNodes(InscryptionTestBase):
    options = {
        "randomize_nodes": 1,
        "randomize_challenges": 2,
    }

    bypass_items = ["Progressive Grizzlies", "Backpack Node", "Dagger", "Angler Hook"]

    def test_prospector_takes_dagger_and_hook_or_backpack(self) -> None:
        self.collect_all_but(self.bypass_items)
        self.assertFalse(self.can_reach_location("Act 1 - Boss Prospector"))
        self.collect_by_name(["Dagger", "Angler Hook"])
        self.assertTrue(self.can_reach_location("Act 1 - Boss Prospector"))

    def test_angler_takes_the_backpack_node(self) -> None:
        self.collect_all_but(self.bypass_items)
        self.collect_by_name(["Dagger", "Angler Hook"])
        self.assertFalse(self.can_reach_location("Act 1 - Boss Angler"))
        self.collect_by_name("Backpack Node")
        self.assertTrue(self.can_reach_location("Act 1 - Boss Angler"))


class AccessTestTotemChallengeOnBosses(InscryptionTestBase):
    options = {
        "randomize_nodes": 1,
        "randomize_challenges": 2,
    }

    # 27 points, one short of the Angler's grizzly-inflated 28, with the backpack node the
    # grizzly bypass wants so the points are what decides the fight.
    base_items = ["Tipped Scales Challenge", "Backpack Node", "Progressive Candle",
                  "Progressive Squirrel", "Angler Hook", "Oil Painting's Clover Plant"]

    def test_totem_challenge_cannot_pay_for_a_boss(self) -> None:
        rules = InscryptionRules(self.world)
        state = self.multiworld.state
        self.collect_by_name(self.base_items)
        self.assertEqual(rules.act1_battle_points(state, LATER_BOSS), 27)
        self.assertFalse(rules.has_angler_requirements(state))

        # All Totem Battles only turns regular map nodes into totem battles, so a boss gets
        # nothing from it and no boss rule can move. A regular battle does get its points.
        self.collect_by_name("All Totem Battles Challenge")
        self.assertEqual(rules.act1_battle_points(state, LATER_BOSS), 27)
        self.assertEqual(rules.act1_battle_points(state, LATER_BATTLE), 30)
        self.assertFalse(rules.has_angler_requirements(state))

        # An item the boss does get tips the same fight over.
        self.collect_by_name("Greater Smoke")
        self.assertTrue(rules.has_angler_requirements(state))

    # The mirror of the above: a regular battle gets nothing from the boss-only items.
    def test_a_regular_battle_gets_nothing_from_the_boss_items(self) -> None:
        rules = InscryptionRules(self.world)
        state = self.multiworld.state
        self.collect_by_name(self.base_items)
        before = rules.act1_battle_points(state, LATER_BATTLE)

        self.collect_by_name(["Boss Totems Challenge", "Greater Smoke"])
        self.assertEqual(rules.act1_battle_points(state, LATER_BATTLE), before)
        self.assertEqual(rules.act1_battle_points(state, LATER_BOSS), before + 4)

    # Nothing that only spawns from the wetlands on may pay for a woodlands fight, including the
    # pairing that only exists out there.
    def test_the_woodlands_gets_nothing_from_the_later_nodes(self) -> None:
        rules = InscryptionRules(self.world)
        state = self.multiworld.state
        before = rules.act1_battle_points(state, WOODLANDS_BATTLE)

        self.collect_by_name(["Mycologists Node", "Bone Altar Node"])
        self.assertEqual(rules.act1_battle_points(state, WOODLANDS_BATTLE), before)
        self.assertEqual(rules.act1_battle_points(state, LATER_BATTLE), before + 2)

        self.collect_by_name(["Sacrifice Stones Node", "Goobert Node"])
        beyond = rules.act1_battle_points(state, LATER_BATTLE)
        woodlands = rules.act1_battle_points(state, WOODLANDS_BATTLE)
        self.assertEqual(beyond - woodlands, 3)  # both nodes, plus their pairing


class AccessTestWetlandsAreaTwoNodes(InscryptionTestBase):
    options = {
        "randomize_nodes": 1,
        "randomize_challenges": 0,
    }

    def test_area_two_nodes_count_for_wetlands_battles(self) -> None:
        rules = InscryptionRules(self.world)
        state = self.multiworld.state
        # 4 points clears the Prospector but leaves the wetlands a point short of its 5.
        self.collect_by_name(["Woodcarver Node", "Backpack Node"])
        self.assertTrue(rules.has_prospector_requirements(state))
        self.assertFalse(rules.has_wetlands_requirements(state))

        # The wetlands is where this node starts spawning, so it counts towards those battles.
        self.collect_by_name("Mycologists Node")
        self.assertTrue(rules.has_wetlands_requirements(state))


class AccessTestGrizzliesWithFixedNodes(InscryptionTestBase):
    options = {
        "randomize_nodes": 0,
        "randomize_challenges": 2,
    }

    def test_bosses_need_no_bypass(self) -> None:
        self.collect_all_but(["Progressive Grizzlies", "Dagger", "Angler Hook"])
        self.assertTrue(self.can_reach_location("Act 1 - Boss Angler"))
        self.assertTrue(self.can_reach_location("Act 1 - Boss Trapper"))


class AccessTestBalancedPaintings(InscryptionTestBase):
    options = {
        "painting_checks_balancing": 1,
    }

    def test_paintings(self) -> None:
        self.assertAccessDependency(["Act 1 - Painting 2", "Act 1 - Painting 3"],
                                    [["Oil Painting's Clover Plant", "Squirrel Totem Head"]])


class AccessTestRandomizedBridgeSequential(InscryptionTestBase):
    options = {
        "act2_randomize_bridge": 1,
        "act_unlocks": 0,
    }

    def test_beating_act_2_needs_the_bridge(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Photographer", "Act 3 - Boss Archivist", "Act 2 - Boss P03"],
            [["Act 2 Bridge Repair"]],
            only_check_listed=True
        )


class AccessTestLeftSideBridgeSequential(InscryptionTestBase):
    options = {
        "act2_randomize_bridge": 2,
        "act_unlocks": 0,
    }

    def test_beating_act_2_needs_the_bridge_from_the_left(self) -> None:
        self.assertAccessDependency(
            ["Act 3 - Boss Photographer", "Act 2 - Boss Leshy", "Act 2 - Boss Grimora"],
            [["Act 2 Bridge Repair"]],
            only_check_listed=True
        )

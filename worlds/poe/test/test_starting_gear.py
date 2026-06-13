"""
Integration tests for usable_starting_gear option with progressive_gear.

Each class runs full world generation and checks which items are precollected.

usable_starting_gear modes:
  no_starting_gear              → only character class precollected
  starting_weapon               → weapon precollected (Progressive or Normal based on progressive_gear)
  starting_weapon_and_flask_slots → weapon + flask slots precollected
  starting_weapon_and_gems      → weapon + starting gem + support gem precollected
  starting_weapon_flask_and_gems → all of the above (default)

All tests use Marauder (starting weapon = Mace) for deterministic weapon name checks.
"""

from . import PoeTestBase
from .. import Items


def _precollected_names(multiworld, player=1):
    return {item.name for item in multiworld.precollected_items[player]}


def _precollected_list(multiworld, player=1):
    return [item.name for item in multiworld.precollected_items[player]]


_GEM_CATEGORIES = {"MainSkillGem", "SupportGem"}

_ALL_GEM_NAMES = {
    item["name"] for item in Items.item_table.values()
    if any(c in item.get("category", []) for c in _GEM_CATEGORIES)
}


class TestNoStartingGear(PoeTestBase):
    """usable_starting_gear = no_starting_gear → only character class item precollected."""
    options = {
        "usable_starting_gear": "no_starting_gear",
        "progressive_gear": "enabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_character_class_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Marauder", names)

    def test_no_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(any("Mace" in n for n in names),
                         f"No weapon should be precollected; got: {names}")

    def test_no_flasks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(any("Flask" in n for n in names),
                         f"No flasks should be precollected; got: {names}")

    def test_no_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(names & _ALL_GEM_NAMES,
                         f"No gems should be precollected; got: {names & _ALL_GEM_NAMES}")


class TestStartingWeaponProgressive(PoeTestBase):
    """starting_weapon + progressive_gear=enabled → Progressive Mace precollected, no flasks/gems."""
    options = {
        "usable_starting_gear": "starting_weapon",
        "progressive_gear": "enabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_progressive_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Progressive Mace", names,
                      f"Progressive Mace should be precollected; got: {names}")

    def test_no_normal_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertNotIn("Normal Mace", names)

    def test_no_flasks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(any("Flask" in n for n in names),
                         f"starting_weapon only — no flasks expected; got: {names}")

    def test_no_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(names & _ALL_GEM_NAMES,
                         f"starting_weapon only — no gems expected; got: {names & _ALL_GEM_NAMES}")


class TestStartingWeaponNormal(PoeTestBase):
    """starting_weapon + progressive_gear=disabled → Normal Mace precollected."""
    options = {
        "usable_starting_gear": "starting_weapon",
        "progressive_gear": "disabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_normal_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Normal Mace", names,
                      f"Normal Mace should be precollected in non-progressive mode; got: {names}")

    def test_no_progressive_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertNotIn("Progressive Mace", names)

    def test_no_flasks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(any("Flask" in n for n in names))


class TestStartingWeaponAndFlasksProgressive(PoeTestBase):
    """starting_weapon_and_flask_slots + progressive_gear=enabled → weapon + 3x Progressive Flask Unlock."""
    options = {
        "usable_starting_gear": "starting_weapon_and_flask_slots",
        "progressive_gear": "enabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_progressive_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Progressive Mace", names)

    def test_three_flask_unlocks_precollected(self):
        items = _precollected_list(self.multiworld)
        flask_count = items.count("Progressive Flask Unlock")
        self.assertEqual(flask_count, 3,
                         f"Expected 3 Progressive Flask Unlock precollected, got {flask_count}")

    def test_no_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(names & _ALL_GEM_NAMES,
                         f"starting_weapon_and_flask_slots — no gems expected; got: {names & _ALL_GEM_NAMES}")


class TestStartingWeaponAndFlasksNormal(PoeTestBase):
    """starting_weapon_and_flask_slots + progressive_gear=disabled → Normal Mace + normal flasks."""
    options = {
        "usable_starting_gear": "starting_weapon_and_flask_slots",
        "progressive_gear": "disabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_normal_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Normal Mace", names)

    def test_normal_flasks_precollected(self):
        items = _precollected_list(self.multiworld)
        flask_names = [n for n in items if "Flask" in n]
        self.assertTrue(len(flask_names) > 0,
                        "Some normal flasks should be precollected in non-progressive mode")

    def test_no_progressive_flask_unlocks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertNotIn("Progressive Flask Unlock", names)


class TestStartingWeaponAndGemsProgressive(PoeTestBase):
    """starting_weapon_and_gems + progressive_gear=enabled → weapon + skill gem + support gem."""
    options = {
        "usable_starting_gear": "starting_weapon_and_gems",
        "progressive_gear": "enabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_progressive_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Progressive Mace", names)

    def test_starting_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertTrue(names & _ALL_GEM_NAMES,
                        f"Starting gem and support gem should be precollected; got: {names}")

    def test_no_flasks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(any("Flask" in n for n in names))


class TestStartingWeaponAndGemsNormal(PoeTestBase):
    """starting_weapon_and_gems + progressive_gear=disabled → Normal Mace + gems."""
    options = {
        "usable_starting_gear": "starting_weapon_and_gems",
        "progressive_gear": "disabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_normal_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Normal Mace", names)

    def test_starting_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertTrue(names & _ALL_GEM_NAMES,
                        f"Starting gems should be precollected; got: {names}")

    def test_no_flasks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertFalse(any("Flask" in n for n in names))


class TestStartingWeaponFlaskAndGemsProgressive(PoeTestBase):
    """starting_weapon_flask_and_gems (default) + progressive_gear=enabled → weapon + flasks + gems."""
    options = {
        "usable_starting_gear": "starting_weapon_flask_and_gems",
        "progressive_gear": "enabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_progressive_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Progressive Mace", names)

    def test_three_flask_unlocks_precollected(self):
        items = _precollected_list(self.multiworld)
        flask_count = items.count("Progressive Flask Unlock")
        self.assertEqual(flask_count, 3)

    def test_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertTrue(names & _ALL_GEM_NAMES,
                        f"Starting gems should be precollected; got: {names}")


class TestStartingWeaponFlaskAndGemsNormal(PoeTestBase):
    """starting_weapon_flask_and_gems + progressive_gear=disabled → Normal Mace + normal flasks + gems."""
    options = {
        "usable_starting_gear": "starting_weapon_flask_and_gems",
        "progressive_gear": "disabled",
        "goal": "complete_act_1",
        "starting_character": "marauder",
        "add_flasks_to_item_pool": True,
    }

    def test_normal_weapon_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertIn("Normal Mace", names)

    def test_normal_flasks_precollected(self):
        items = _precollected_list(self.multiworld)
        flask_names = [n for n in items if "Flask" in n]
        self.assertTrue(len(flask_names) > 0)

    def test_no_progressive_flask_unlocks_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertNotIn("Progressive Flask Unlock", names)

    def test_gems_precollected(self):
        names = _precollected_names(self.multiworld)
        self.assertTrue(names & _ALL_GEM_NAMES,
                        f"Starting gems should be precollected; got: {names}")

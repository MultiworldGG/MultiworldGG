from ..names import ItemNames, LocationNames
from . import CupheadTestBase

class TestLogicBasic(CupheadTestBase):
    def test_default(self):
        test = TestLogicBasic()
        test.world_setup()
        test.assertBeatable(False)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.assertFalse(test.can_reach_region(LocationNames.level_mausoleum_i))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.assertTrue(test.can_reach_region(LocationNames.level_mausoleum_i))
        contracts = test.get_items_by_name(ItemNames.item_contract)
        test.collect(contracts)
        test.collect_by_name(ItemNames.item_plane_gun)
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertBeatable(True)

class TestLogicBasicDlc(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
    }

    def test_dlc(self):
        test = TestLogicBasicDlc()
        test.world_setup()
        test.assertBeatable(False)
        test.assertFalse(test.can_reach_region(LocationNames.world_dlc_inkwell_4))
        test.collect_by_name(ItemNames.item_dlc_boat)
        test.assertFalse(test.can_reach_region(LocationNames.world_dlc_inkwell_4))
        test.assertFalse(test.can_reach_region(LocationNames.level_mausoleum_i))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_region(LocationNames.level_mausoleum_i))
        test.assertTrue(test.can_reach_region(LocationNames.world_dlc_inkwell_4))
        contracts = test.get_items_by_name(ItemNames.item_contract)
        test.collect(contracts)
        ingredients = test.get_items_by_name(ItemNames.item_dlc_ingredient)
        test.collect(ingredients)
        test.collect_by_name(ItemNames.item_plane_gun)
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertBeatable(True)

class TestLogicTopGrade(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_topgrade(self):
        test = TestLogicTopGrade()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

        test.collect_by_name(ItemNames.item_plane_gun)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_ability_plane_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

class TestLogicProgressiveWeapons(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "start_weapon": "chaser",
        "weapon_mode": "progressive",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_progressive_weapons(self):
        test = TestLogicProgressiveWeapons()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_super_i)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_super_i)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect(test.get_item_by_name(ItemNames.item_p_weapon_spread))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect(test.get_item_by_name(ItemNames.item_p_weapon_spread))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_p_weapon_spread)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect(test.get_item_by_name(ItemNames.item_p_weapon_chaser))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove(test.get_item_by_name(ItemNames.item_p_weapon_chaser))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name([ItemNames.item_ability_parry, ItemNames.item_ability_dash])
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

        test.collect_by_name(ItemNames.item_plane_gun)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_ability_plane_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.remove_by_name(ItemNames.item_plane_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_super)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.remove_by_name(ItemNames.item_ability_plane_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))

class TestLogicProgressiveWeaponsExceptStart(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "disabled",
        "start_weapon": "peashooter",
        "weapon_mode": "progressive_except_start",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_progressive_weapons_except_start(self):
        test = TestLogicProgressiveWeaponsExceptStart()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

class TestLogicWeaponEX(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "disabled",
        "start_weapon": "peashooter",
        "weapon_mode": "ex_separate",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_weapon_ex(self):
        test = TestLogicWeaponEX()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_super_i)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_super_i)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_weapon_peashooter_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_weapon_peashooter_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_weapon_spread_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.remove_by_name(ItemNames.item_weapon_spread_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.collect_by_name([ItemNames.item_ability_parry, ItemNames.item_ability_dash])
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))

        test.collect_by_name([ItemNames.item_plane_gun, ItemNames.item_ability_plane_parry])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_ex)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.remove_by_name(ItemNames.item_plane_ex)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))
        test.collect_by_name(ItemNames.item_plane_super)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_topgrade))

class TestLogicWeaponEXExceptStart(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "disabled",
        "start_weapon": "spread",
        "weapon_mode": "ex_separate_except_start",
        "freemove_isles": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_weapon_ex_except_start(self):
        test = TestLogicWeaponEXExceptStart()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))

class TestLogicParry(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "start_weapon": "peashooter",
        "freemove_isles": "true",
        "randomize_abilities": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_parry(self):
        test = TestLogicParry()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_event_agrade))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_event_agrade))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_tree_agrade))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_tree_event_agrade))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_topgrade))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_event_agrade))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_agrade))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_event_agrade))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_tree_agrade))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_tree_event_agrade))

class TestLogicDash(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "start_weapon": "peashooter",
        "freemove_isles": "true",
        "randomize_abilities": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade"
    }

    def test_dash(self):
        test = TestLogicDash()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_coin4))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_tree))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_tree_coin4))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_coin4))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_tree))
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_tree_coin4))

class TestLogicChalice(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "freemove_isles": "true",
        "randomize_abilities": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade",
        "dlc_boss_chalice_checks": "enabled",
        "dlc_rungun_chalice_checks": "enabled"
    }

    def test_chalice(self):
        test = TestLogicChalice()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.remove_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))

class TestLogicChaliceStart(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "start",
        "freemove_isles": "true",
        "randomize_abilities": "true",
        "boss_grade_checks": "a_minus_grade",
        "rungun_grade_checks": "a_minus_grade",
        "dlc_boss_chalice_checks": "enabled",
        "dlc_rungun_chalice_checks": "enabled"
    }

    def test_chalice_start(self):
        test = TestLogicChaliceStart()
        test.world_setup()
        test.assertBeatable(False)

        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))

class TestLogicChalicedGradeRequired(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "freemove_isles": "true",
        "dlc_boss_chalice_checks": "grade_required",
        "dlc_rungun_chalice_checks": "grade_required"
    }

    def test_chaliced_grade_required(self):
        test = TestLogicChalicedGradeRequired()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.remove_by_name([ItemNames.item_charm_dlc_cookie, ItemNames.item_ability_dash])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

        test.collect_by_name(ItemNames.item_plane_gun)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_plane_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))
        test.remove_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))

class TestLogicChalicedGradeRequiredSeparate(CupheadTestBase):
    options = {
        "use_dlc": True,
        "mode": "dlc_beat_both",
        "dlc_chalice": "randomized",
        "freemove_isles": "true",
        "dlc_boss_chalice_checks": "separate_grade_required",
        "dlc_rungun_chalice_checks": "separate_grade_required"
    }

    def test_chaliced_grade_required_separate(self):
        test = TestLogicChalicedGradeRequiredSeparate()
        test.world_setup()
        test.assertBeatable(False)

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_parry)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))
        test.remove_by_name([ItemNames.item_charm_dlc_cookie, ItemNames.item_ability_dash])
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_veggies_dlc_chaliced))

        test.collect_by_name(ItemNames.item_plane_gun)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_plane_parry)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))
        test.remove_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_boss_plane_blimp_dlc_chaliced))

        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_ability_dash)
        test.assertFalse(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))
        test.collect_by_name(ItemNames.item_charm_dlc_cookie)
        test.assertTrue(test.can_reach_location(LocationNames.loc_level_rungun_forest_dlc_chaliced))

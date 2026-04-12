from . import UltrakillTestBase

goal_max: int = 42


class TestLevelItems(UltrakillTestBase):
    def test_level_items(self) -> None:
        start_item = self.world.start_level.full_name
        goal_item = self.world.goal_level.full_name

        item_names = [i.name for i in self.multiworld.get_items()]

        self.assertNotIn(start_item, item_names)
        self.assertNotIn(goal_item, item_names)


# 0-1: INTO THE FIRE -> 0-2: THE MEATGRINDER
class TestS1G2(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 0-3: DOUBLE DOWN
class TestS1G3(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 0-4: A ONE-MACHINE ARMY
class TestS1G4(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 0-5: CERBERUS
class TestS1G5(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 0-S: SOMETHING WICKED
class TestS1G0(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 1-1: HEART OF THE SUNRISE
class TestS1G6(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 1-2: THE BURNING WORLD
class TestS1G7(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 1-3: HALLS OF SACRED REMAINS
class TestS1G8(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 1-4: CLAIR DE LUNE
class TestS1G9(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 1-S: THE WITLESS
class TestS1GN1(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 2-1: BRIDGEBURNER
class TestS1G10(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 2-2: DEATH AT 20,000 VOLTS
class TestS1G11(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 2-3: SHEER HEART ATTACK
class TestS1G12(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 2-4: COURT OF THE CORPSE KING
class TestS1G13(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 2-S: ALL IMPERFECT LOVE SONG
class TestS1GN2(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 3-1: BELLY OF THE BEAST
class TestS1G14(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 3-2: IN THE FLESH
class TestS1G15(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 4-1: SLAVES TO POWER
class TestS1G16(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 4-2: GOD DAMN THE SUN
class TestS1G17(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 4-3: A SHOT IN THE DARK
class TestS1G18(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 4-4: CLAIR DE SOLEIL
class TestS1G19(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 4-S: CLASH OF THE BRANDICOOT
class TestS1GN4(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 5-1: IN THE WAKE OF POSEIDON
class TestS1G20(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 5-2: WAVES OF THE STARLESS SEA
class TestS1G21(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 5-3: SHIP OF FOOLS
class TestS1G22(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 5-4: LEVIATHAN
class TestS1G23(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 5-S: I ONLY SAY MORNING
class TestS1GN5(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 6-1: CRY FOR THE WEEPER
class TestS1G24(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 6-2: AESTHETICS OF HATE
class TestS1G25(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 7-1: GARDEN OF FORKING PATHS
class TestS1G26(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 7-2: LIGHT UP THE NIGHT
class TestS1G27(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 7-3: NO SOUND, NO MEMORY
class TestS1G28(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS1G29(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 7-S: HELL BATH NO FURY
class TestS1GN7(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 8-1: HURTBREAK WONDERLAND
class TestS1G30(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 8-2: THROUGH THE MIRROR
class TestS1G31(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 8-3: DISINTEGRATION LOOP
class TestS1G32(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 8-4: FINAL FLIGHT
class TestS1G33(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS1G100(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> 1-E: ...THEN FELL THE ASHES
class TestS1G101(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> P-1: SOUL SURVIVOR
class TestS1G666(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-1: INTO THE FIRE -> P-2: WAIT OF THE WORLD
class TestS1G667(TestLevelItems):
    options = {
        "start_level": 1,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 0-1: INTO THE FIRE
class TestS2G1(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 0-3: DOUBLE DOWN
class TestS2G3(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 0-4: A ONE-MACHINE ARMY
class TestS2G4(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 0-5: CERBERUS
class TestS2G5(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 0-S: SOMETHING WICKED
class TestS2G0(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 1-1: HEART OF THE SUNRISE
class TestS2G6(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 1-2: THE BURNING WORLD
class TestS2G7(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 1-3: HALLS OF SACRED REMAINS
class TestS2G8(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 1-4: CLAIR DE LUNE
class TestS2G9(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 1-S: THE WITLESS
class TestS2GN1(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 2-1: BRIDGEBURNER
class TestS2G10(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 2-2: DEATH AT 20,000 VOLTS
class TestS2G11(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 2-3: SHEER HEART ATTACK
class TestS2G12(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 2-4: COURT OF THE CORPSE KING
class TestS2G13(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 2-S: ALL IMPERFECT LOVE SONG
class TestS2GN2(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 3-1: BELLY OF THE BEAST
class TestS2G14(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 3-2: IN THE FLESH
class TestS2G15(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 4-1: SLAVES TO POWER
class TestS2G16(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 4-2: GOD DAMN THE SUN
class TestS2G17(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 4-3: A SHOT IN THE DARK
class TestS2G18(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 4-4: CLAIR DE SOLEIL
class TestS2G19(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 4-S: CLASH OF THE BRANDICOOT
class TestS2GN4(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 5-1: IN THE WAKE OF POSEIDON
class TestS2G20(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 5-2: WAVES OF THE STARLESS SEA
class TestS2G21(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 5-3: SHIP OF FOOLS
class TestS2G22(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 5-4: LEVIATHAN
class TestS2G23(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 5-S: I ONLY SAY MORNING
class TestS2GN5(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 6-1: CRY FOR THE WEEPER
class TestS2G24(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 6-2: AESTHETICS OF HATE
class TestS2G25(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 7-1: GARDEN OF FORKING PATHS
class TestS2G26(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 7-2: LIGHT UP THE NIGHT
class TestS2G27(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 7-3: NO SOUND, NO MEMORY
class TestS2G28(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS2G29(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 7-S: HELL BATH NO FURY
class TestS2GN7(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 8-1: HURTBREAK WONDERLAND
class TestS2G30(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 8-2: THROUGH THE MIRROR
class TestS2G31(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 8-3: DISINTEGRATION LOOP
class TestS2G32(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 8-4: FINAL FLIGHT
class TestS2G33(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS2G100(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> 1-E: ...THEN FELL THE ASHES
class TestS2G101(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> P-1: SOUL SURVIVOR
class TestS2G666(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 0-2: THE MEATGRINDER -> P-2: WAIT OF THE WORLD
class TestS2G667(TestLevelItems):
    options = {
        "start_level": 2,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-1: INTO THE FIRE
class TestS6G1(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-2: THE MEATGRINDER
class TestS6G2(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-3: DOUBLE DOWN
class TestS6G3(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-4: A ONE-MACHINE ARMY
class TestS6G4(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-5: CERBERUS
class TestS6G5(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-S: SOMETHING WICKED
class TestS6G0(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 1-2: THE BURNING WORLD
class TestS6G7(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 1-3: HALLS OF SACRED REMAINS
class TestS6G8(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 1-4: CLAIR DE LUNE
class TestS6G9(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 1-S: THE WITLESS
class TestS6GN1(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 2-1: BRIDGEBURNER
class TestS6G10(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 2-2: DEATH AT 20,000 VOLTS
class TestS6G11(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 2-3: SHEER HEART ATTACK
class TestS6G12(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 2-4: COURT OF THE CORPSE KING
class TestS6G13(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 2-S: ALL IMPERFECT LOVE SONG
class TestS6GN2(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 3-1: BELLY OF THE BEAST
class TestS6G14(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 3-2: IN THE FLESH
class TestS6G15(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 4-1: SLAVES TO POWER
class TestS6G16(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 4-2: GOD DAMN THE SUN
class TestS6G17(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 4-3: A SHOT IN THE DARK
class TestS6G18(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 4-4: CLAIR DE SOLEIL
class TestS6G19(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 4-S: CLASH OF THE BRANDICOOT
class TestS6GN4(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 5-1: IN THE WAKE OF POSEIDON
class TestS6G20(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 5-2: WAVES OF THE STARLESS SEA
class TestS6G21(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 5-3: SHIP OF FOOLS
class TestS6G22(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 5-4: LEVIATHAN
class TestS6G23(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 5-S: I ONLY SAY MORNING
class TestS6GN5(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 6-1: CRY FOR THE WEEPER
class TestS6G24(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 6-2: AESTHETICS OF HATE
class TestS6G25(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 7-1: GARDEN OF FORKING PATHS
class TestS6G26(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 7-2: LIGHT UP THE NIGHT
class TestS6G27(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 7-3: NO SOUND, NO MEMORY
class TestS6G28(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS6G29(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 7-S: HELL BATH NO FURY
class TestS6GN7(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 8-1: HURTBREAK WONDERLAND
class TestS6G30(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 8-2: THROUGH THE MIRROR
class TestS6G31(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 8-3: DISINTEGRATION LOOP
class TestS6G32(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 8-4: FINAL FLIGHT
class TestS6G33(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS6G100(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> 1-E: ...THEN FELL THE ASHES
class TestS6G101(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> P-1: SOUL SURVIVOR
class TestS6G666(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-1: HEART OF THE SUNRISE -> P-2: WAIT OF THE WORLD
class TestS6G667(TestLevelItems):
    options = {
        "start_level": 6,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-1: INTO THE FIRE
class TestS7G2(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-2: THE MEATGRINDER
class TestS7G2(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-3: DOUBLE DOWN
class TestS7G3(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-4: A ONE-MACHINE ARMY
class TestS7G4(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-5: CERBERUS
class TestS7G5(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-S: SOMETHING WICKED
class TestS7G0(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 1-1: HEART OF THE SUNRISE
class TestS7G6(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 1-3: HALLS OF SACRED REMAINS
class TestS7G8(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 1-4: CLAIR DE LUNE
class TestS7G9(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 1-S: THE WITLESS
class TestS7GN1(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 2-1: BRIDGEBURNER
class TestS7G10(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 2-2: DEATH AT 20,000 VOLTS
class TestS7G11(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 2-3: SHEER HEART ATTACK
class TestS7G12(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 2-4: COURT OF THE CORPSE KING
class TestS7G13(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 2-S: ALL IMPERFECT LOVE SONG
class TestS7GN2(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 3-1: BELLY OF THE BEAST
class TestS7G14(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 3-2: IN THE FLESH
class TestS7G15(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 4-1: SLAVES TO POWER
class TestS7G16(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 4-2: GOD DAMN THE SUN
class TestS7G17(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 4-3: A SHOT IN THE DARK
class TestS7G18(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 4-4: CLAIR DE SOLEIL
class TestS7G19(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 4-S: CLASH OF THE BRANDICOOT
class TestS7GN4(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 5-1: IN THE WAKE OF POSEIDON
class TestS7G20(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 5-2: WAVES OF THE STARLESS SEA
class TestS7G21(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 5-3: SHIP OF FOOLS
class TestS7G22(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 5-4: LEVIATHAN
class TestS7G23(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 5-S: I ONLY SAY MORNING
class TestS7GN5(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 6-1: CRY FOR THE WEEPER
class TestS7G24(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 6-2: AESTHETICS OF HATE
class TestS7G25(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 7-1: GARDEN OF FORKING PATHS
class TestS7G26(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 7-2: LIGHT UP THE NIGHT
class TestS7G27(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 7-3: NO SOUND, NO MEMORY
class TestS7G28(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS7G29(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 7-S: HELL BATH NO FURY
class TestS7GN7(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 8-1: HURTBREAK WONDERLAND
class TestS7G30(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 8-2: THROUGH THE MIRROR
class TestS7G31(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 8-3: DISINTEGRATION LOOP
class TestS7G32(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 8-4: FINAL FLIGHT
class TestS7G33(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS7G100(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> 1-E: ...THEN FELL THE ASHES
class TestS7G101(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> P-1: SOUL SURVIVOR
class TestS7G666(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-2: THE BURNING WORLD -> P-2: WAIT OF THE WORLD
class TestS7G667(TestLevelItems):
    options = {
        "start_level": 7,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-1: INTO THE FIRE
class TestS8G1(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-2: THE MEATGRINDER
class TestS8G2(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-3: DOUBLE DOWN
class TestS8G3(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-4: A ONE-MACHINE ARMY
class TestS8G4(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-5: CERBERUS
class TestS8G5(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-S: SOMETHING WICKED
class TestS8G0(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 1-1: HEART OF THE SUNRISE
class TestS8G7(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 1-2: THE BURNING WORLD
class TestS8G8(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 1-4: CLAIR DE LUNE
class TestS8G9(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 1-S: THE WITLESS
class TestS8GN1(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 2-1: BRIDGEBURNER
class TestS8G10(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 2-2: DEATH AT 20,000 VOLTS
class TestS8G11(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 2-3: SHEER HEART ATTACK
class TestS8G12(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 2-4: COURT OF THE CORPSE KING
class TestS8G13(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 2-S: ALL IMPERFECT LOVE SONG
class TestS8GN2(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 3-1: BELLY OF THE BEAST
class TestS8G14(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 3-2: IN THE FLESH
class TestS8G15(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 4-1: SLAVES TO POWER
class TestS8G16(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 4-2: GOD DAMN THE SUN
class TestS8G17(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 4-3: A SHOT IN THE DARK
class TestS8G18(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 4-4: CLAIR DE SOLEIL
class TestS8G19(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 4-S: CLASH OF THE BRANDICOOT
class TestS8GN4(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 5-1: IN THE WAKE OF POSEIDON
class TestS8G20(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 5-2: WAVES OF THE STARLESS SEA
class TestS8G21(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 5-3: SHIP OF FOOLS
class TestS8G22(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 5-4: LEVIATHAN
class TestS8G23(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 5-S: I ONLY SAY MORNING
class TestS8GN5(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 6-1: CRY FOR THE WEEPER
class TestS8G24(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 6-2: AESTHETICS OF HATE
class TestS8G25(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 7-1: GARDEN OF FORKING PATHS
class TestS8G26(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 7-2: LIGHT UP THE NIGHT
class TestS8G27(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 7-3: NO SOUND, NO MEMORY
class TestS8G28(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS8G29(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 7-S: HELL BATH NO FURY
class TestS8GN7(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 8-1: HURTBREAK WONDERLAND
class TestS8G30(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 8-2: THROUGH THE MIRROR
class TestS8G31(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 8-3: DISINTEGRATION LOOP
class TestS8G32(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 8-4: FINAL FLIGHT
class TestS8G33(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS8G100(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> 1-E: ...THEN FELL THE ASHES
class TestS8G101(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> P-1: SOUL SURVIVOR
class TestS8G666(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 1-3: HALLS OF SACRED REMAINS -> P-2: WAIT OF THE WORLD
class TestS8G667(TestLevelItems):
    options = {
        "start_level": 8,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-1: INTO THE FIRE
class TestS12G1(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-2: THE MEATGRINDER
class TestS12G2(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-3: DOUBLE DOWN
class TestS12G3(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-4: A ONE-MACHINE ARMY
class TestS12G4(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-5: CERBERUS
class TestS12G5(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-S: SOMETHING WICKED
class TestS12G0(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 1-1: HEART OF THE SUNRISE
class TestS12G7(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 1-2: THE BURNING WORLD
class TestS12G8(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 1-3: HALLS OF SACRED REMAINS
class TestS12G8(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 1-4: CLAIR DE LUNE
class TestS12G9(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 1-S: THE WITLESS
class TestS12GN1(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 2-1: BRIDGEBURNER
class TestS12G10(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 2-2: DEATH AT 20,000 VOLTS
class TestS12G11(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 2-4: COURT OF THE CORPSE KING
class TestS12G13(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 2-S: ALL IMPERFECT LOVE SONG
class TestS12GN2(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 3-1: BELLY OF THE BEAST
class TestS12G14(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 3-2: IN THE FLESH
class TestS12G15(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 4-1: SLAVES TO POWER
class TestS12G16(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 4-2: GOD DAMN THE SUN
class TestS12G17(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 4-3: A SHOT IN THE DARK
class TestS12G18(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 4-4: CLAIR DE SOLEIL
class TestS12G19(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 4-S: CLASH OF THE BRANDICOOT
class TestS12GN4(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 5-1: IN THE WAKE OF POSEIDON
class TestS12G20(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 5-2: WAVES OF THE STARLESS SEA
class TestS12G21(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 5-3: SHIP OF FOOLS
class TestS12G22(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 5-4: LEVIATHAN
class TestS12G23(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 5-S: I ONLY SAY MORNING
class TestS12GN5(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 6-1: CRY FOR THE WEEPER
class TestS12G24(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 6-2: AESTHETICS OF HATE
class TestS12G25(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 7-1: GARDEN OF FORKING PATHS
class TestS12G26(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 7-2: LIGHT UP THE NIGHT
class TestS12G27(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 7-3: NO SOUND, NO MEMORY
class TestS12G28(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS12G29(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 7-S: HELL BATH NO FURY
class TestS12GN7(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 8-1: HURTBREAK WONDERLAND
class TestS12G30(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 8-2: THROUGH THE MIRROR
class TestS12G31(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 8-3: DISINTEGRATION LOOP
class TestS12G32(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 8-4: FINAL FLIGHT
class TestS12G33(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS12G100(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> 1-E: ...THEN FELL THE ASHES
class TestS12G101(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> P-1: SOUL SURVIVOR
class TestS12G666(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 2-3: SHEER HEART ATTACK -> P-2: WAIT OF THE WORLD
class TestS12G667(TestLevelItems):
    options = {
        "start_level": 12,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-1: INTO THE FIRE
class TestS14G1(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-2: THE MEATGRINDER
class TestS14G2(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-3: DOUBLE DOWN
class TestS14G3(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-4: A ONE-MACHINE ARMY
class TestS14G4(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-5: CERBERUS
class TestS14G5(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-S: SOMETHING WICKED
class TestS14G0(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 1-1: HEART OF THE SUNRISE
class TestS14G7(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 1-2: THE BURNING WORLD
class TestS14G8(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 1-3: HALLS OF SACRED REMAINS
class TestS14G8(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 1-4: CLAIR DE LUNE
class TestS14G9(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 1-S: THE WITLESS
class TestS14GN1(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 2-1: BRIDGEBURNER
class TestS14G10(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 2-2: DEATH AT 20,000 VOLTS
class TestS14G11(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 2-3: SHEER HEART ATTACK
class TestS14G12(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 2-4: COURT OF THE CORPSE KING
class TestS14G13(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 2-S: ALL IMPERFECT LOVE SONG
class TestS14GN2(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 3-2: IN THE FLESH
class TestS14G15(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 4-1: SLAVES TO POWER
class TestS14G16(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 4-2: GOD DAMN THE SUN
class TestS14G17(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 4-3: A SHOT IN THE DARK
class TestS14G18(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 4-4: CLAIR DE SOLEIL
class TestS14G19(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 4-S: CLASH OF THE BRANDICOOT
class TestS14GN4(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 5-1: IN THE WAKE OF POSEIDON
class TestS14G20(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 5-2: WAVES OF THE STARLESS SEA
class TestS14G21(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 5-3: SHIP OF FOOLS
class TestS14G22(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 5-4: LEVIATHAN
class TestS14G23(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 5-S: I ONLY SAY MORNING
class TestS14GN5(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 6-1: CRY FOR THE WEEPER
class TestS14G24(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 6-2: AESTHETICS OF HATE
class TestS14G25(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 7-1: GARDEN OF FORKING PATHS
class TestS14G26(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 7-2: LIGHT UP THE NIGHT
class TestS14G27(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 7-3: NO SOUND, NO MEMORY
class TestS14G28(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS14G29(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 7-S: HELL BATH NO FURY
class TestS14GN7(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 8-1: HURTBREAK WONDERLAND
class TestS14G30(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 8-2: THROUGH THE MIRROR
class TestS14G31(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 8-3: DISINTEGRATION LOOP
class TestS14G32(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 8-4: FINAL FLIGHT
class TestS14G33(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS14G100(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> 1-E: ...THEN FELL THE ASHES
class TestS14G101(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> P-1: SOUL SURVIVOR
class TestS14G666(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 3-1: BELLY OF THE BEAST -> P-2: WAIT OF THE WORLD
class TestS14G667(TestLevelItems):
    options = {
        "start_level": 14,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-1: INTO THE FIRE
class TestS17G1(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-2: THE MEATGRINDER
class TestS17G2(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-3: DOUBLE DOWN
class TestS17G3(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-4: A ONE-MACHINE ARMY
class TestS17G4(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-5: CERBERUS
class TestS17G5(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-S: SOMETHING WICKED
class TestS17G0(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 1-1: HEART OF THE SUNRISE
class TestS17G7(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 1-2: THE BURNING WORLD
class TestS17G8(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 1-3: HALLS OF SACRED REMAINS
class TestS17G8(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 1-4: CLAIR DE LUNE
class TestS17G9(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 1-S: THE WITLESS
class TestS17GN1(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 2-1: BRIDGEBURNER
class TestS17G10(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 2-2: DEATH AT 20,000 VOLTS
class TestS17G11(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 2-3: SHEER HEART ATTACK
class TestS17G12(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 2-4: COURT OF THE CORPSE KING
class TestS17G13(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 2-S: ALL IMPERFECT LOVE SONG
class TestS17GN2(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 3-1: BELLY OF THE BEAST
class TestS17G14(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 3-2: IN THE FLESH
class TestS17G15(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 4-1: SLAVES TO POWER
class TestS17G16(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 4-3: A SHOT IN THE DARK
class TestS17G18(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 4-4: CLAIR DE SOLEIL
class TestS17G19(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 4-S: CLASH OF THE BRANDICOOT
class TestS17GN4(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 5-1: IN THE WAKE OF POSEIDON
class TestS17G20(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 5-2: WAVES OF THE STARLESS SEA
class TestS17G21(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 5-3: SHIP OF FOOLS
class TestS17G22(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 5-4: LEVIATHAN
class TestS17G23(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 5-S: I ONLY SAY MORNING
class TestS17GN5(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 6-1: CRY FOR THE WEEPER
class TestS17G24(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 6-2: AESTHETICS OF HATE
class TestS17G25(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 7-1: GARDEN OF FORKING PATHS
class TestS17G26(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 7-2: LIGHT UP THE NIGHT
class TestS17G27(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 7-3: NO SOUND, NO MEMORY
class TestS17G28(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS17G29(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 7-S: HELL BATH NO FURY
class TestS17GN7(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 8-1: HURTBREAK WONDERLAND
class TestS17G30(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 8-2: THROUGH THE MIRROR
class TestS17G31(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 8-3: DISINTEGRATION LOOP
class TestS17G32(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 8-4: FINAL FLIGHT
class TestS17G33(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS17G100(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> 1-E: ...THEN FELL THE ASHES
class TestS17G100(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> P-1: SOUL SURVIVOR
class TestS17G666(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 4-2: GOD DAMN THE SUN -> P-2: WAIT OF THE WORLD
class TestS17G667(TestLevelItems):
    options = {
        "start_level": 17,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-1: INTO THE FIRE
class TestS31G1(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-2: THE MEATGRINDER
class TestS31G2(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-3: DOUBLE DOWN
class TestS31G3(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-4: A ONE-MACHINE ARMY
class TestS31G4(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-5: CERBERUS
class TestS31G5(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-S: SOMETHING WICKED
class TestS31G0(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 1-1: HEART OF THE SUNRISE
class TestS31G6(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 1-2: THE BURNING WORLD
class TestS31G7(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 1-3: HALLS OF SACRED REMAINS
class TestS31G8(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 1-4: CLAIR DE LUNE
class TestS31G9(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 1-S: THE WITLESS
class TestS31GN1(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 2-1: BRIDGEBURNER
class TestS31G10(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 2-2: DEATH AT 20,000 VOLTS
class TestS31G11(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 2-3: SHEER HEART ATTACK
class TestS31G12(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 2-4: COURT OF THE CORPSE KING
class TestS31G13(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 2-S: ALL IMPERFECT LOVE SONG
class TestS31GN2(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 3-1: BELLY OF THE BEAST
class TestS31G14(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 3-2: IN THE FLESH
class TestS31G15(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 4-1: SLAVES TO POWER
class TestS31G16(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 4-2: GOD DAMN THE SUN
class TestS31G17(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 4-3: A SHOT IN THE DARK
class TestS31G18(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 4-4: CLAIR DE SOLEIL
class TestS31G19(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 4-S: CLASH OF THE BRANDICOOT
class TestS31GN4(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 5-1: IN THE WAKE OF POSEIDON
class TestS31G20(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 5-2: WAVES OF THE STARLESS SEA
class TestS31G21(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 5-3: SHIP OF FOOLS
class TestS31G22(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 5-4: LEVIATHAN
class TestS31G23(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 5-S: I ONLY SAY MORNING
class TestS31GN5(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 6-1: CRY FOR THE WEEPER
class TestS31G24(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 6-2: AESTHETICS OF HATE
class TestS31G25(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 7-1: GARDEN OF FORKING PATHS
class TestS31G26(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 7-2: LIGHT UP THE NIGHT
class TestS31G27(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 7-3: NO SOUND, NO MEMORY
class TestS31G28(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS31G29(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 7-S: HELL BATH NO FURY
class TestS31GN7(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 8-1: HURTBREAK WONDERLAND
class TestS31G30(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 8-3: DISINTEGRATION LOOP
class TestS31G32(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 32,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 8-4: FINAL FLIGHT
class TestS31G33(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS31G100(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> 1-E: ...THEN FELL THE ASHES
class TestS31G101(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> P-1: SOUL SURVIVOR
class TestS31G666(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-2: THROUGH THE MIRROR -> P-2: WAIT OF THE WORLD
class TestS31G667(TestLevelItems):
    options = {
        "start_level": 31,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-1: INTO THE FIRE
class TestS32G1(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-2: THE MEATGRINDER
class TestS32G2(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-3: DOUBLE DOWN
class TestS32G3(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 3,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-4: A ONE-MACHINE ARMY
class TestS32G4(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-5: CERBERUS
class TestS32G5(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-S: SOMETHING WICKED
class TestS32G0(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 0,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 1-1: HEART OF THE SUNRISE
class TestS32G6(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 6,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 1-2: THE BURNING WORLD
class TestS32G7(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 1-3: HALLS OF SACRED REMAINS
class TestS32G8(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 8,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 1-4: CLAIR DE LUNE
class TestS32G9(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 9,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 1-S: THE WITLESS
class TestS32GN1(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": -1,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 2-1: BRIDGEBURNER
class TestS32G10(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 10,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 2-2: DEATH AT 20,000 VOLTS
class TestS32G11(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 11,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 2-3: SHEER HEART ATTACK
class TestS32G12(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 12,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 2-4: COURT OF THE CORPSE KING
class TestS32G13(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 13,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 2-S: ALL IMPERFECT LOVE SONG
class TestS32GN2(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": -2,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 3-1: BELLY OF THE BEAST
class TestS32G14(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 14,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 3-2: IN THE FLESH
class TestS32G15(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 15,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 4-1: SLAVES TO POWER
class TestS32G16(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 16,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 4-2: GOD DAMN THE SUN
class TestS32G17(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 17,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 4-3: A SHOT IN THE DARK
class TestS32G18(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 18,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 4-4: CLAIR DE SOLEIL
class TestS32G19(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 19,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 4-S: CLASH OF THE BRANDICOOT
class TestS32GN4(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": -4,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 5-1: IN THE WAKE OF POSEIDON
class TestS32G20(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 20,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 5-2: WAVES OF THE STARLESS SEA
class TestS32G21(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 21,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 5-3: SHIP OF FOOLS
class TestS32G22(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 22,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 5-4: LEVIATHAN
class TestS32G23(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 23,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 5-S: I ONLY SAY MORNING
class TestS32GN5(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": -5,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 6-1: CRY FOR THE WEEPER
class TestS32G24(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 24,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 6-2: AESTHETICS OF HATE
class TestS32G25(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 25,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 7-1: GARDEN OF FORKING PATHS
class TestS32G26(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 26,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 7-2: LIGHT UP THE NIGHT
class TestS32G27(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 27,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 7-3: NO SOUND, NO MEMORY
class TestS32G28(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 28,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 7-4: ...LIKE ANTENNAS TO HEAVEN
class TestS32G29(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 29,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 7-S: HELL BATH NO FURY
class TestS32GN7(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": -7,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 8-1: HURTBREAK WONDERLAND
class TestS32G30(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 30,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 8-2: THROUGH THE MIRROR
class TestS32G31(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 31,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 8-4: FINAL FLIGHT
class TestS32G33(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 33,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 0-E: THIS HEAT, AN EVIL HEAT
class TestS32G100(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 100,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> 1-E: ...THEN FELL THE ASHES
class TestS32G101(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 101,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> P-1: SOUL SURVIVOR
class TestS32G666(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 666,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }


# 8-3: DISINTEGRATION LOOP -> P-2: WAIT OF THE WORLD
class TestS32G667(TestLevelItems):
    options = {
        "start_level": 32,
        "goal_level": 667,
        "goal_requirement": goal_max,
        "skipped_levels": {}
    }

from . import UltrakillTestBase
from ..Locations import location_list, UKEnemyLocation

goal_min: int = 5


def GetEnemyLocation(name: str) -> UKEnemyLocation:
    for loc in location_list:
        if loc.name == name:
            return loc
    return None


# not possible for Filth, Stray to be inaccessible due to start levels

class TestSchism(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Schism").applicable_levels,
        "enemy_rewards": "all"
    }


class TestSoldier(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Soldier").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMinos(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: The Corpse of King Minos").applicable_levels,
        "enemy_rewards": "all"
    }


class TestStalker(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Stalker").applicable_levels,
        "enemy_rewards": "all"
    }


class TestInsurrectionist(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Insurrectionist").applicable_levels,
        "enemy_rewards": "all"
    }


class TestFerryman(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Ferryman").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMirrorReaper(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Mirror Reaper").applicable_levels,
        "enemy_rewards": "all"
    }


class TestSwordsmachine(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Swordsmachine").applicable_levels,
        "enemy_rewards": "all"
    }


class TestDrone(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Drone").applicable_levels,
        "enemy_rewards": "all"
    }


class TestStreetcleaner(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Streetcleaner").applicable_levels,
        "enemy_rewards": "all"
    }


class TestV2(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: V2").applicable_levels,
        "enemy_rewards": "all"
    }


class TestV2Second(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: V2 (2nd)").applicable_levels,
        "enemy_rewards": "all"
    }


class TestSentry(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Sentry").applicable_levels,
        "enemy_rewards": "all"
    }


class TestGutterman(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Gutterman").applicable_levels,
        "enemy_rewards": "all"
    }


class TestGuttertank(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Guttertank").applicable_levels,
        "enemy_rewards": "all"
    }


class TestEarthmover(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Earthmover").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMaliciousFace(UltrakillTestBase):
    options = {
        "start_level": "0_2",
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Malicious Face").applicable_levels,
        "enemy_rewards": "all"
    }


class TestCerberus(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Cerberus").applicable_levels,
        "enemy_rewards": "all"
    }


class TestHideousMass(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Hideous Mass").applicable_levels,
        "enemy_rewards": "all"
    }


class TestIdol(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Idol").applicable_levels,
        "enemy_rewards": "all"
    }


class TestLeviathan(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Leviathan").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMannequin(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Mannequin").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMinotaur(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Minotaur").applicable_levels,
        "enemy_rewards": "all"
    }


class TestDeathcatcher(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Deathcatcher").applicable_levels,
        "enemy_rewards": "all"
    }


class TestGeryon(UltrakillTestBase):
    options = {
        "goal_level": "7_4",
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Geryon, Watcher of the Skies").applicable_levels,
        "enemy_rewards": "all"
    }


class TestGabriel(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Gabriel, Judge of Hell").applicable_levels,
        "enemy_rewards": "all"
    }


class TestVirtue(UltrakillTestBase):
    options = {
        "goal_level": "7_4",
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Virtue").applicable_levels,
        "enemy_rewards": "all"
    }


class TestGabrielSecond(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Gabriel, Apostate of Hate").applicable_levels,
        "enemy_rewards": "all"
    }


class TestProvidence(UltrakillTestBase):
    options = {
        "goal_level": "7_4",
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Providence").applicable_levels,
        "enemy_rewards": "all"
    }


class TestPower(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Enemy: Power").applicable_levels,
        "enemy_rewards": "all"
    }


class TestFleshPrison(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Flesh Prison").applicable_levels,
        "enemy_rewards": "all"
    }


class TestFleshPanopticon(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Flesh Panopticon").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMinosPrime(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Minos Prime").applicable_levels,
        "enemy_rewards": "all"
    }


class TestSisyphusPrime(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Sisyphus Prime").applicable_levels,
        "enemy_rewards": "all"
    }


class TestRodent(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Very Cancerous Rodent").applicable_levels,
        "enemy_rewards": "all"
    }


class TestMDK(UltrakillTestBase):
    options = {
        "goal_requirement": goal_min,
        "skipped_levels": GetEnemyLocation("Boss: Mysterious Druid Knight (& Owl)").applicable_levels,
        "enemy_rewards": "all"
    }

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest
from dataclasses import fields
from types import SimpleNamespace
from typing import TYPE_CHECKING, Any, ClassVar, cast

from Options import PerGameCommonOptions

from ..world.enums import WeaponMode
from ..world.items import itemdefs as idefs
from ..world.items import itemsetup, weapons
from ..world.names import itemnames
from . import CupheadTestBase

if TYPE_CHECKING:
    from ..world.options import CupheadOptions


def _is_hashable(obj: Any) -> bool:
    try:
        hash(obj)
        return True
    except TypeError:
        return False

class TestAPWorldOptionsWConf(unittest.TestCase):
    exclude_options: ClassVar[set[str]] = {
        "version",
        "start_maxhealth",
        "start_maxhealth_p2",
        "deathlink",
        "deathlink_grace_count",
        "extra_coins",
        "music_shuffle",
        "ducklock_platdrop",
    }
    exclude_options_start: ClassVar[set[str]] = {
        "filler_weight_",
        "trap_weight_",
    }

    _base_options: ClassVar[set[str]] = {x.name for x in fields(PerGameCommonOptions)}

    @classmethod
    def _check_option_name_is_valid(cls, oname: str) -> bool:
        if oname in cls.exclude_options or oname in cls._base_options:
            return False

        for eopt in cls.exclude_options_start:
            if oname.startswith(eopt):
                return False

        return True

class TestAPWorldItemSetup(unittest.TestCase):
    @staticmethod
    def _options_for_weapon_mode(mode: WeaponMode):
        return SimpleNamespace(
            weapon_mode=SimpleNamespace(evalue=mode),
            start_weapon=SimpleNamespace(value=0, is_none=lambda: False),
            use_dlc=SimpleNamespace(bvalue=True),
            boss_grade_checks=SimpleNamespace(evalue=0),
            rungun_grade_checks=SimpleNamespace(evalue=0),
            dlc_boss_chalice_checks=SimpleNamespace(evalue=0),
        )

    def test_setup_weapons(self):
        _start_weapon = itemnames.item_weapon_peashooter

        self.assertEqual(weapons.weapon_dict[0], _start_weapon)

        modes: list[tuple[str, WeaponMode]] = [
            ("Normal", WeaponMode.NORMAL),
            ("Progressive", WeaponMode.PROGRESSIVE),
            ("Progressive Except Start", WeaponMode.PROGRESSIVE_EXCEPT_START),
            ("Ex Separate", WeaponMode.EX_SEPARATE),
            ("Ex Separate Except Start", WeaponMode.EX_SEPARATE_EXCEPT_START),
        ]

        for mode_name, mode_value in modes:
            with self.subTest(mode_name):
                options = cast("CupheadOptions", self._options_for_weapon_mode(mode_value))
                items = {**idefs.items_base}
                weapon_dict = weapons.get_weapon_dict(options, True)
                itemsetup.setup_weapons(items, options, weapon_dict)

                expected_weapons = set(weapon_dict.values())
                self.assertTrue(expected_weapons.issubset(items.keys()))

                if (mode_value & WeaponMode.EX_SEPARATE) > 0:
                    expected_ex = {
                        x
                        for i, x in weapons.weapon_ex_dict.items()
                        if i in weapons.get_weapon_dict(options, True)
                    }
                    self.assertTrue(expected_ex.issubset(items.keys()))
                else:
                    self.assertTrue(set(idefs.item_all_weapon_ex.keys()).isdisjoint(items.keys()))

                if (mode_value & WeaponMode.PROGRESSIVE) > 0 or (mode_value & WeaponMode.EX_SEPARATE) > 0:
                    self.assertEqual(items[itemnames.item_plane_ex].quantity, 1)
                else:
                    self.assertEqual(items[itemnames.item_plane_ex].quantity, 0)

class TestAPWorldStartWeapon(CupheadTestBase):
    def test_explicit_start_weapon_is_resolved(self):
        for start_weapon, expected_index in (("peashooter", 0), ("chaser", 2)):
            with self.subTest(start_weapon):
                test_world = TestAPWorldStartWeapon()
                test_world.options = {
                    "start_weapon": start_weapon,
                }
                test_world.world_setup()

                self.assertEqual(expected_index, test_world.world.resolved_start_weapon_index)

class TestAPWorldUTSupport(CupheadTestBase):
    def test_sdata_re_gen(self):
        test_world = TestAPWorldUTSupport()
        test_world.options = {
            "boss_secret_checks": True
        }
        test_world.world_setup()

        #goptions = test_world.world.options.dump()

        slot_data = dict(test_world.world.fill_slot_data())

        test_worldb = TestAPWorldUTSupport()
        test_worldb.options = {
            "test_overrides": {"ut": {self.game: slot_data}}
        }
        test_worldb.world_setup()

        #goptionsb = test_world.world.options.dump()

        slot_datab = dict(test_worldb.world.fill_slot_data())

        for sdkey, sdvalue in slot_datab.items():
            self.assertIn(sdkey, slot_data)
            _sdatav = slot_data[sdkey]
            if isinstance(sdvalue, list):
                sdatavb: Any = tuple(sdvalue)  # type: ignore
            elif isinstance(sdvalue, dict):
                sdatavb: Any = tuple(sorted(sdvalue.items()))  # type: ignore
            else:
                sdatavb = sdvalue
            if isinstance(_sdatav, list):
                sdatav: tuple[Any, ...] = tuple(_sdatav)  # type: ignore
            elif isinstance(_sdatav, dict):
                sdatav: Any = tuple(sorted(_sdatav.items()))  # type: ignore
            else:
                sdatav = _sdatav
            self.assertTrue(_is_hashable(sdatavb), msg=f"For {sdkey}")
            self.assertTrue(_is_hashable(sdatav), msg=f"For {sdkey}")

            self.assertEqual(hash(sdatav), hash(sdatavb), msg=f"For {sdkey}: {sdatav!r} != {sdatavb!r}")

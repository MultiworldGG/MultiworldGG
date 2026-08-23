### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest
from collections.abc import Sequence
from pathlib import Path
from random import Random
from types import SimpleNamespace
from typing import TYPE_CHECKING, cast

from ..tools import gentemplateyaml
from ..world.enums import LevelShuffleMode
from ..world.levels import levelids, levelshuffle
from ..world.names import regionnames
from ..world.options import optionresolver
from ..world.options.optionbase import _levelset

if TYPE_CHECKING:
    from random import Random

    from ..world.options import CupheadOptions


class TestCode(unittest.TestCase):
    def test_level_set(self) -> None:
        self.assertEqual(_levelset.levels, set(levelids.level_ids.values()))


class TestCodeOptionResolver(unittest.TestCase):
    class _TrackingRandom:
        def __init__(self) -> None:
            self.pools: list[tuple[int, ...]] = []

        def choice(self, seq: Sequence[int]) -> int:
            pool = tuple(seq)
            self.pools.append(pool)
            return pool[-1]

        def randint(self, start: int, end: int) -> int:
            del start, end
            raise AssertionError("randint should not be used for start_weapon resolution")

        def choices(
            self,
            population: str,
            weights: Sequence[float] | None = None,
            *,
            cum_weights: Sequence[float] | None = None,
            k: int = 1,
        ) -> list[str]:
            del population, weights, cum_weights
            return ["0"] * k

    @staticmethod
    def _make_options(start_weapon_value: int, use_dlc: bool) -> "CupheadOptions":
        start_weapon = SimpleNamespace(
            value=start_weapon_value,
            random_value=-1,
            option_random_weapon=-2,
            option_peashooter=0,
            option_roundabout=5,
            option_dlc_twistup=8,
            option_none=127,
        )
        return cast(
            "CupheadOptions",
            SimpleNamespace(
                mode=SimpleNamespace(value=0),
                use_dlc=SimpleNamespace(value=use_dlc),
                start_weapon=start_weapon,
                boss_grade_checks=SimpleNamespace(value=0),
                level_shuffle_seed=SimpleNamespace(value="seed"),
            ),
        )

    def test_random_weapon_uses_explicit_base_weapons_only(self) -> None:
        options = self._make_options(-2, False)
        rand = self._TrackingRandom()

        optionresolver.resolve_random_options(options, cast("Random", rand))

        self.assertEqual(rand.pools, [tuple(range(0, 6))])
        self.assertEqual(options.start_weapon.value, 5)

    def test_random_weapon_uses_explicit_dlc_weapons_when_enabled(self) -> None:
        options = self._make_options(-2, True)
        rand = self._TrackingRandom()

        optionresolver.resolve_random_options(options, cast("Random", rand))

        self.assertEqual(rand.pools, [tuple(range(0, 9))])
        self.assertEqual(options.start_weapon.value, 8)

    def test_random_includes_none_but_not_random_weapon_without_dlc(self) -> None:
        options = self._make_options(-1, False)
        rand = self._TrackingRandom()

        optionresolver.resolve_random_options(options, cast("Random", rand))

        self.assertEqual(rand.pools, [(*range(0, 6), 127)])
        self.assertEqual(options.start_weapon.value, 127)

    def test_random_includes_none_but_not_random_weapon_with_dlc(self) -> None:
        options = self._make_options(-1, True)
        rand = self._TrackingRandom()

        optionresolver.resolve_random_options(options, cast("Random", rand))

        self.assertEqual(rand.pools, [(*range(0, 9), 127)])
        self.assertEqual(options.start_weapon.value, 127)

class TestCodeLevelShuffle(unittest.TestCase):
    def _check_level_shuffle_map(self, shuffle_map: dict[int, int]):
        used_k: set[int] = set()
        used_v: set[int] = set()

        for k, v in shuffle_map.items():
            self.assertNotIn(k, used_k)
            self.assertNotIn(v, used_v)

            used_k.add(k)
            used_v.add(v)

    def test_level_shuffle_no_dupes(self):
        rand = Random(655)
        shuffle_map = levelshuffle.get_level_shuffle_map(rand, True, LevelShuffleMode.ENABLED, True)

        self._check_level_shuffle_map(shuffle_map)

    def test_level_shuffle_w_level_placements(self):
        rand = Random(655)
        level_placements = {regionnames.level_boss_clown: regionnames.level_boss_clown}
        shuffle_map = levelshuffle.get_level_shuffle_map(rand, True, LevelShuffleMode.ENABLED, True, level_placements)

        self._check_level_shuffle_map(shuffle_map)

class TestCodeGenTemplateYaml(unittest.TestCase):
    def test_start_weapon_keeps_negative_option_values(self) -> None:
        root = Path(__file__).resolve().parents[1]
        classes = gentemplateyaml.parse_optiondefs(str(root / "world" / "options" / "options.py"))

        start_weapon = next(node for node in classes if node.name == "StartWeapon")
        options = gentemplateyaml.get_option_fields(start_weapon)
        attrs = gentemplateyaml.get_class_attrs(start_weapon)
        default = gentemplateyaml.get_default_option(attrs, ["ChoiceEx", "NamedOption"], options)

        self.assertEqual(options["random_weapon"], -2)
        self.assertEqual(default, "random_weapon")

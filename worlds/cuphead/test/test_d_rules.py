### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import unittest
from typing import Any, cast

from rule_builder.rules import Has, Rule

from ..world.rules.dep import deps
from ..world.rules.dep.depbase import Dep
from ..world.rules.dep.depfilter import DepFilter
from ..world.rules.levelrules.levelrulebase import InheritMode, LevelDef, LocationDef
from ..world.rules.levelrules.levelrulecomp import LevelRuleComp


class TestDepFilter(unittest.TestCase):
    @staticmethod
    def _dep_true(_: object) -> bool:
        return True

    @staticmethod
    def _dep_false(_: object) -> bool:
        return False

    def test_depfilter_all_mode(self):
        true_dep: Dep = cast(Dep, self._dep_true)
        false_dep: Dep = cast(Dep, self._dep_false)

        self.assertTrue(DepFilter((true_dep, true_dep), value=True, any=False)(object()))  # type: ignore[arg-type]
        self.assertFalse(DepFilter((true_dep, false_dep), value=True, any=False)(object()))  # type: ignore[arg-type]
        self.assertFalse(DepFilter((true_dep, false_dep), value=False, any=False)(object()))  # type: ignore[arg-type]
        self.assertTrue(DepFilter((false_dep, false_dep), value=False, any=False)(object()))  # type: ignore[arg-type]

    def test_depfilter_any_mode(self):
        true_dep: Dep = cast(Dep, self._dep_true)
        false_dep: Dep = cast(Dep, self._dep_false)

        self.assertTrue(DepFilter((false_dep, true_dep), value=True, any=True)(object()))  # type: ignore[arg-type]
        self.assertFalse(DepFilter((false_dep, false_dep), value=True, any=True)(object()))  # type: ignore[arg-type]
        self.assertTrue(DepFilter((true_dep, false_dep), value=False, any=True)(object()))  # type: ignore[arg-type]
        self.assertTrue(DepFilter((false_dep, false_dep), value=False, any=True)(object()))  # type: ignore[arg-type]

    def test_depfilter_dict_roundtrip(self):
        single = DepFilter(deps.dep_hard_logic)
        single_roundtrip = DepFilter.from_dict(single.to_dict())
        self.assertEqual(single.to_dict(), single_roundtrip.to_dict())

        multi = DepFilter((deps.dep_dlc_chalice_not_separate, deps.dep_hard_logic), value=False, any=True)
        multi_roundtrip = DepFilter.from_dict(multi.to_dict())
        self.assertEqual(multi.to_dict(), multi_roundtrip.to_dict())

    def test_depfilter_to_dict_shapes(self):
        single = DepFilter(deps.dep_hard_logic).to_dict()
        self.assertEqual(single["when"], "hard_logic")
        self.assertIs(single["condition"], True)
        self.assertIs(single["any"], False)

        multi = DepFilter((deps.dep_hard_logic, deps.dep_rando_abilities), value=False, any=True).to_dict()
        self.assertEqual(multi["when"], ("hard_logic", "rando_abilities"))
        self.assertIs(multi["condition"], False)
        self.assertIs(multi["any"], True)

    def test_depfilter_from_dict_defaults(self):
        parsed = DepFilter.from_dict({"when": "hard_logic"})
        self.assertEqual(parsed.to_dict(), {"when": "hard_logic", "condition": True, "any": False})

    def test_depfilter_from_dict_invalid_when(self):
        with self.assertRaisesRegex(ValueError, "^Dep dict must contain a non-empty string 'when' value\\.$"):
            DepFilter.from_dict({"when": " "})
        with self.assertRaisesRegex(ValueError, "^Dep dict 'when' tuple/list cannot be empty\\.$"):
            DepFilter.from_dict({"when": []})
        with self.assertRaisesRegex(
            ValueError,
            "^Dep dict 'when' list/tuple must contain only non-empty strings\\.$"
        ):
            DepFilter.from_dict({"when": ["hard_logic", ""]})
        with self.assertRaisesRegex(
            ValueError,
            "^Dep dict must contain either a string or list/tuple of strings for 'when'\\.$"
        ):
            DepFilter.from_dict({"when": 7})  # type: ignore[arg-type]

    def test_depfilter_from_dict_invalid_flags_and_unknown(self):
        with self.assertRaisesRegex(ValueError, "^Dep dict 'condition' must be a bool\\.$"):
            DepFilter.from_dict({"when": "hard_logic", "condition": 1})  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "^Dep dict 'any' must be a bool\\.$"):
            DepFilter.from_dict({"when": "hard_logic", "any": "no"})  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "^Unknown dep name\\(s\\): not_real_dep\\.$"):
            DepFilter.from_dict({"when": "not_real_dep"})

    def test_depfilter_init_validation(self):
        with self.assertRaisesRegex(ValueError, "^DepFilter requires at least one dep\\.$"):
            DepFilter(())  # type: ignore[arg-type]
        with self.assertRaisesRegex(ValueError, "^DepFilter deps must be callable\\.$"):
            DepFilter((deps.dep_hard_logic, cast(Dep, 5)))  # type: ignore[arg-type]

    def test_depfilter_check_invalid_options(self):
        with self.assertRaisesRegex(ValueError, "^DepFilter options is invalid\\.$"):
            DepFilter(deps.dep_hard_logic).check(cast(object, object()))  # type: ignore[arg-type]

    def test_depfilter_str(self):
        self.assertEqual(str(DepFilter(deps.dep_hard_logic)), "hard_logic")
        self.assertEqual(str(DepFilter(deps.dep_hard_logic, value=False)), "!hard_logic")
        self.assertEqual(
            str(DepFilter((deps.dep_hard_logic, deps.dep_rando_abilities), value=True, any=False)),
            "(hard_logic&rando_abilities)",
        )
        self.assertEqual(
            str(DepFilter((deps.dep_hard_logic, deps.dep_rando_abilities), value=False, any=True)),
            "!(hard_logic|rando_abilities)",
        )


class _TestableLevelRuleComp(LevelRuleComp):
    def compile_location_rule_for_test(
        self,
        inherit: InheritMode,
        base: Rule[Any] | None = None,
        loc_rule: Rule[Any] | None = None,
    ) -> Rule[Any] | None:
        return self._compile_location_rule(
            LevelDef(locations={}, base=base),
            LocationDef(rule=loc_rule, inherit=inherit),
        )


class TestLevelRuleComp(unittest.TestCase):
    @staticmethod
    def _compile_location_rule(
        inherit: InheritMode,
        base: Rule[Any] | None = None,
        loc_rule: Rule[Any] | None = None,
    ) -> Rule[Any] | None:
        comp = _TestableLevelRuleComp.__new__(_TestableLevelRuleComp)
        return comp.compile_location_rule_for_test(inherit, base=base, loc_rule=loc_rule)

    def test_compile_location_rule_inherit_and(self):
        base = Has("base")
        loc_rule = Has("loc")

        self.assertIsNone(self._compile_location_rule(InheritMode.AND))
        self.assertEqual(self._compile_location_rule(InheritMode.AND, loc_rule=loc_rule), loc_rule)
        self.assertEqual(self._compile_location_rule(InheritMode.AND, base=base), base)
        self.assertEqual(self._compile_location_rule(InheritMode.AND, base=base, loc_rule=loc_rule), base & loc_rule)

    def test_compile_location_rule_inherit_or(self):
        base = Has("base")
        loc_rule = Has("loc")

        self.assertIsNone(self._compile_location_rule(InheritMode.OR))
        self.assertIsNone(self._compile_location_rule(InheritMode.OR, loc_rule=loc_rule))
        self.assertIsNone(self._compile_location_rule(InheritMode.OR, base=base))
        self.assertEqual(self._compile_location_rule(InheritMode.OR, base=base, loc_rule=loc_rule), base | loc_rule)

    def test_compile_location_rule_inherit_none(self):
        base = Has("base")
        loc_rule = Has("loc")

        self.assertIsNone(self._compile_location_rule(InheritMode.NONE))
        self.assertEqual(self._compile_location_rule(InheritMode.NONE, loc_rule=loc_rule), loc_rule)
        self.assertIsNone(self._compile_location_rule(InheritMode.NONE, base=base))
        self.assertEqual(self._compile_location_rule(InheritMode.NONE, base=base, loc_rule=loc_rule), loc_rule)

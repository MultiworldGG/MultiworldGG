from collections import Counter
from inspect import get_annotations, getattr_static
from types import UnionType
from typing import get_origin, get_args, Any, Mapping, Sequence, AbstractSet, Union, ClassVar, Callable

from . import LegoStarWarsWorldTestBase
from ..options import (
    get_option_name,
    ChapterUnlockRequirement,
    EnableBonusLocations,
    Ridesanity,
    GoalChapter,
    StartingChapter,
)
from ..option_resolution.universal_tracker import UTAttribute


_MISSING = object()

# todo: This test should be replaced with a fuzzer hook.

class TestWorldAttributes(LegoStarWarsWorldTestBase):
    """Sanity check that world attributes are the expected types. A type checker should find most issues with attributes
    being set to the wrong type, but PyCharm's type checker struggles sometimes."""
    options = {
        get_option_name(ChapterUnlockRequirement): ChapterUnlockRequirement.option_random_characters,
        get_option_name(EnableBonusLocations): True,
        get_option_name(Ridesanity): True,
        get_option_name(GoalChapter): GoalChapter.option_random_enabled_chapter,
        get_option_name(StartingChapter): StartingChapter.option_random_chapter,
    }
    def _make_type_match_func(self, type_hint: Any, do_assert: bool = True) -> Callable[[Any], bool]:
        if isinstance(type_hint, type):
            def check(x: Any):
                if do_assert:
                    self.assertIsInstance(x, type_hint)
                    return True
                else:
                    return isinstance(x, type_hint)
            return check
        origin = get_origin(type_hint)
        if origin is not None:
            return self._make_type_match_func_alias(origin, get_args(type_hint), do_assert)
        raise NotImplementedError("")

    def _make_type_match_func_alias(self, origin: Any, args: Any, do_assert: bool = True):
        if origin in (Union, UnionType):
            if not isinstance(args, tuple):
                raise TypeError("")
            if not args:
                raise Exception("Missing type hint args for Union/UnionType")
            match_funcs = tuple(self._make_type_match_func(arg, False) for arg in args)

            def check(v: Any) -> bool:
                for func in match_funcs:
                    if func(v):
                        return True
                if do_assert:
                    self.fail(f"{v} is not a type in {args}")
                return False

            return check
        if origin is ClassVar or origin is UTAttribute:
            if not isinstance(args, tuple):
                raise TypeError("")
            if len(args) < 1:
                raise Exception(f"Missing type hint args for {origin.__name__}")
            if len(args) > 1:
                raise Exception(f"Too many type hint args for {origin.__name__}")
            return self._make_type_match_func(args[0])
        if issubclass(origin, Mapping):
            if not isinstance(args, tuple):
                raise TypeError("")
            if issubclass(origin, Counter):
                args = args + (int,)
            if len(args) == 0:
                raise Exception("Missing type hint args for Mapping")
            if len(args) < 2:
                raise Exception("Missing type hint args for Mapping")
            if len(args) > 2:
                raise Exception("Too many type hint args for Mapping")
            key_type, value_type = args
            key_check = self._make_type_match_func(key_type)
            value_check = self._make_type_match_func(value_type)

            def check(v: Any) -> bool:
                if not isinstance(v, Mapping):
                    return False
                for k, v in v.items():
                    if not key_check(k):
                        return False
                    if not value_check(v):
                        return False
                return True

            return check
        if origin is tuple:
            if len(args) == 2 and args[-1] is ...:
                # Treat tuple[T, ...] as Sequence[T].
                return self._make_type_match_func(Sequence[args[0]])
            else:
                check_functions = [self._make_type_match_func(arg, do_assert) for arg in args]

                def check(v: Any) -> bool:
                    if not type(v) is tuple:
                        return False
                    if len(v) != len(check_functions):
                        return False
                    for e, element_check in zip(v, check_functions):
                        if not element_check(e):
                            return False
                    return True

                return check
        if issubclass(origin, (Sequence, AbstractSet)):
            if not isinstance(args, tuple):
                raise TypeError("")
            if len(args) == 0:
                raise Exception("Missing type hint args for Sequence/AbstractSet")
            if len(args) > 1:
                raise Exception("Too many type hint args for Sequence/AbstractSet")
            element_check = self._make_type_match_func(args[0])

            def check(v: Any) -> bool:
                if not isinstance(v, (Sequence, AbstractSet)):
                    return False
                for element in v:
                    if not element_check(element):
                        return False
                return True

            return check
        raise NotImplementedError(f"TypeAlias {origin}[{' | '.join(args)}] not supported")

    @property
    def run_default_tests(self) -> bool:
        return False

    def test_attribute_types(self):
        for k, v in get_annotations(type(self.world)).items():
            with self.subTest(name=k):
                static_attr = getattr_static(type(self.world), k, None)
                if isinstance(static_attr, UTAttribute) and not static_attr.has_default():
                    value = getattr(self.world, k, _MISSING)
                    if value is _MISSING:
                        self.skipTest("Universal Tracker attribute without a default value was not present during "
                                      "normal generation.")
                else:
                    value = getattr(self.world, k)
                if get_origin(v) is ClassVar:
                    self.assertNotIn(k, self.world.__dict__)
                check = self._make_type_match_func(v)
                self.assertTrue(check(value), f"{k}: {value}")

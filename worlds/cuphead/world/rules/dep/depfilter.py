### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

import dataclasses
from typing import Any, Self, cast

from typing_extensions import override

from Options import CommonOptions
from rule_builder.options import OptionFilter

from ...options import CupheadOptions
from .depbase import DEPS, Dep

# DepFilters integrate Deps into rule_builder.

@dataclasses.dataclass(frozen=True, init=False)
class DepFilter(OptionFilter):
    fns: tuple[Dep, ...]
    value: bool
    any: bool
    _dep_names: tuple[str, ...]

    def __init__(self, fns: Dep | tuple[Dep, ...], value: bool = True, any: bool = False):
        dep_args: tuple[Dep, ...]
        if isinstance(fns, tuple):
            dep_args = cast(tuple[Dep, ...], fns)
        else:
            dep_args = (fns,)

        if not dep_args:
            raise ValueError("DepFilter requires at least one dep.")
        if not all(callable(dep) for dep in dep_args):
            raise ValueError("DepFilter deps must be callable.")
        super().__init__(None, None)  # pyright: ignore[reportArgumentType]
        object.__setattr__(self, "fns", dep_args)
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "any", any)
        object.__setattr__(self, "_dep_names", tuple(dep.__name__.removeprefix("dep_") for dep in dep_args))

    def _eval(self, c: CupheadOptions) -> bool:
        dep_matches = (fn(c) == self.value for fn in self.fns)
        return any(dep_matches) if self.any else all(dep_matches)

    def __call__(self, c: CupheadOptions) -> bool:
        return self._eval(c)

    @override
    def to_dict(self) -> dict[str, Any]:
        """Returns a JSON compatible dict representation of this Dep"""
        dep_names: str | tuple[str, ...]
        if len(self._dep_names) == 1:
            dep_names = self._dep_names[0]
        else:
            dep_names = self._dep_names
        return {
            "when": dep_names,
            "condition": self.value,
            "any": self.any,
        }

    @override
    def check(self, options: CommonOptions) -> bool:
        """Tests the given options dataclass to see if it passes this Dep"""
        if isinstance(options, CupheadOptions):
            return self._eval(options)
        raise ValueError("DepFilter options is invalid.")

    @classmethod
    @override
    def from_dict(cls, data: dict[str, Any]) -> Self:  # type: ignore
        """Returns a new Dep instance from a dict representation"""
        expr = data.get("when")
        dep_names: tuple[str, ...]
        if isinstance(expr, str):
            if not expr.strip():
                raise ValueError("Dep dict must contain a non-empty string 'when' value.")
            dep_names = (expr,)
        elif isinstance(expr, (list, tuple)):
            if not expr:
                raise ValueError("Dep dict 'when' tuple/list cannot be empty.")
            names: list[str] = []
            expr_items = cast(list[Any] | tuple[Any, ...], expr)
            for raw_name in expr_items:
                if not isinstance(raw_name, str) or not raw_name.strip():
                    raise ValueError("Dep dict 'when' list/tuple must contain only non-empty strings.")
                names.append(raw_name)
            dep_names = tuple(names)
        else:
            raise ValueError("Dep dict must contain either a string or list/tuple of strings for 'when'.")

        value = data.get("condition", True)
        any_mode = data.get("any", False)
        if not isinstance(value, bool):
            raise ValueError("Dep dict 'condition' must be a bool.")
        if not isinstance(any_mode, bool):
            raise ValueError("Dep dict 'any' must be a bool.")

        unknown = [name for name in dep_names if name not in DEPS]
        if unknown:
            raise ValueError(f"Unknown dep name(s): {', '.join(unknown)}.")

        dep_fns = tuple(DEPS[name] for name in dep_names)
        dep_param: Dep | tuple[Dep, ...] = dep_fns[0] if len(dep_fns) == 1 else dep_fns
        return cls(dep_param, value=value, any=any_mode)

    @override
    def __str__(self) -> str:
        joiner = "|" if self.any else "&"
        expr = joiner.join(self._dep_names)
        if len(self._dep_names) > 1:
            expr = f"({expr})"
        return f"!{expr}" if not self.value else expr

    @override
    def __repr__(self) -> str:
        fns_expr = str(self._dep_names) if len(self._dep_names) != 1 else self._dep_names[0]
        value_expr = ", value=False" if not self.value else ""
        any_expr = ", any=True" if self.any else ""
        return f"{__class__.__name__}({fns_expr}{value_expr}{any_expr})"

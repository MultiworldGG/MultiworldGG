### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Callable

from ...options import CupheadOptions

Dep = Callable[[CupheadOptions], bool]

DEPS: dict[str, Dep] = {}
def dep(fn: Dep) -> Dep:
    _name = getattr(fn, "__name__", "").removeprefix("dep_")
    if _name:
        DEPS[_name] = fn
    return fn

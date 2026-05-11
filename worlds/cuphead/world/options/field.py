### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Callable
from dataclasses import field
from typing import Any, TypeVar

T = TypeVar("T")

def create_field(
    converter: Callable[[Any], T],
    option_def: Any,
    default: T | None = None,
):
    try:
        if default is None:
            return field(
                default_factory=lambda: converter(option_def.default),
                metadata={"conv": converter, "odef": option_def, "oname": option_def.name},
            )
        return field(
            default=default,
            metadata={"conv": converter, "odef": option_def, "oname": option_def.name},
        )
    except NameError as err:
        raise ValueError("option_def is not a valid Option Definition!") from err

def create_special_field(
    converter: Callable[[Any], T],
    default: T
):
    try:
        return field(
            default_factory=lambda: converter(default),
            metadata={"conv": converter,},
        )
    except NameError as err:
        raise ValueError("cannot create special field") from err

### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    class NamedOption(Protocol):
        name: str

    class CupheadBaseOption(NamedOption, Protocol):
        @property
        def current_key(self) -> str:
            return ""

    class CupheadNumericOption(CupheadBaseOption, Protocol):
        value: int

    class CupheadOptionSet(CupheadBaseOption, Protocol):
        value: set[str]
else:
    class NamedOption:
        name: str

    class CupheadBaseOption(NamedOption):
        @property
        def current_key(self) -> str:
            return ""

    class CupheadNumericOption(CupheadBaseOption):
        value: int

    class CupheadOptionSet(CupheadBaseOption):
        value: set[str]

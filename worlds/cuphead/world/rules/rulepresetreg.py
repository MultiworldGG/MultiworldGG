### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from dataclasses import dataclass

from typing_extensions import override

from rule_builder.rules import Rule


@dataclass(init=False)
class RulePresetReg:
    _reg: dict[str, Rule.Resolved]

    def __init__(self):
        self._reg = {}

    def clear_reg(self):
        self._reg.clear()

    def in_reg(self, pname: str) -> bool:
        return pname in self._reg

    def get(self, pname: str) -> Rule.Resolved | None:
        return self._reg.get(pname)

    def set(self, pname: str, rule: Rule.Resolved):
        self._reg[pname] = rule

    def update(self, **kwargs: Rule.Resolved):
        self._reg.update(**kwargs)

    def pop(self, pname: str) -> Rule.Resolved | None:
        return self._reg.pop(pname, None)

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self._reg!s})"

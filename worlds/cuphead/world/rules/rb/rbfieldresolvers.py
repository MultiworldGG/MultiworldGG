### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from abc import ABC
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from typing_extensions import override

from rule_builder.field_resolvers import FieldResolver

from ....varis import game_name as ch
from ...options.options import ContractRequirements, DlcIngredientRequirements

if TYPE_CHECKING:
    from worlds.AutoWorld import World


@dataclass(frozen=True)
class BaseOptionResolver(FieldResolver, ABC, game=ch):
    _option_name: ClassVar[str]

    @override
    def resolve(self, world: "World") -> Any:
        if not hasattr(world.options, self._option_name):
            raise KeyError(f"{self._option_name} is not an option in {world.__name__}")
        return getattr(world.options, self._option_name).value

@dataclass(frozen=True)
class OptionResolver(FieldResolver, game=ch):
    option_name: str

    @override
    def resolve(self, world: "World") -> Any:
        if not hasattr(world.options, self.option_name):
            raise KeyError(f"{self.option_name} is not an option in {world.__name__}")
        return getattr(world.options, self.option_name).value

@dataclass(frozen=True)
class ContractReqsResolver(BaseOptionResolver, game=ch):
    _option_name: ClassVar[str] = ContractRequirements.name

@dataclass(frozen=True)
class DlcIngredientReqsResolver(BaseOptionResolver, game=ch):
    _option_name: ClassVar[str] = DlcIngredientRequirements.name

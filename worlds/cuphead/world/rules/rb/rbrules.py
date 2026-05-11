### Copyright 2025-2026 JKLeckr
### SPDX-License-Identifier: MPL-2.0

from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Self

from typing_extensions import override

from BaseClasses import CollectionState
from NetUtils import JSONMessagePart
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAnyCount, Rule, WrapperRule

from ....varis import game_name as ch
from ...enums import WeaponMode
from ...items import weapons
from ...names import itemnames, regionnames
from .rbbase import PresetData

if TYPE_CHECKING:
    from worlds.AutoWorld import World

    from .... import CupheadWorld

@dataclass(init=False)
class Preset(WrapperRule["CupheadWorld"], game=ch):
    pname: str

    def __init__(
        self,
        preset: PresetData,
        *,
        options: Iterable[OptionFilter] = (),
        filtered_resolution: bool = False
    ):
        self.pname = preset.name
        self.child = preset.rule
        self.options = options
        self.filtered_resolution = filtered_resolution

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        _reg = world.rulereg.presets
        if rrule := _reg.get(self.pname):
            return rrule
        rrule = self.Resolved(
            self.child.resolve(world),
            self.pname,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )
        _reg.set(self.pname, rrule)
        return rrule

    @override
    def to_dict(self) -> dict[str, Any]:
        data = super().to_dict()
        data["preset_name"] = self.pname
        return data

    @override
    @classmethod
    def from_dict(cls, data: Mapping[str, Any], world_cls: "type[World]") -> Self:
        res = super().from_dict(data, world_cls)
        if not (_pname := data.get("preset_name", "")):
            raise ValueError("preset_name is not a valid name")
        res.pname = _pname
        return res

    @override
    def __str__(self) -> str:
        return f"{self.__class__.__name__}[{self.child}]"

    class Resolved(WrapperRule.Resolved):
        name: str

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": str(self)}]
            msg: list[JSONMessagePart] = [
                {"type": "color", "color": "green" if self(state) else "salmon", "text": self.name},
                {"type": "color", "color": "white", "text": "["},
            ]
            msg.extend(self.child.explain_json(state))
            msg.append({"type": "color", "color": "white", "text": "]"})
            return msg

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            return f"{self.name}: {state is not None} ({self.child.explain_str(state)})"

        @override
        def __str__(self) -> str:
            return f"{self.name}[{self.child}]"

@dataclass
class HasAnyWeapon(Rule["CupheadWorld"], game=ch):
    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        _weapon_dict = world.weapon_dict
        return HasAny.Resolved(
            tuple(_weapon_dict.values()),
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

@dataclass
class HasAnyWeaponEx(HasAnyWeapon, game=ch):
    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        _weapon_dict = world.weapon_ex_dict
        if (world.options.weapon_mode.evalue & WeaponMode.EX_SEPARATE) > 0:
            return HasAny.Resolved(
                tuple(_weapon_dict.values()),
                player=world.player,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )
        if (world.options.weapon_mode.evalue & WeaponMode.PROGRESSIVE) > 0:
            return HasAnyCount.Resolved(
                tuple((w, 2) for w in _weapon_dict.values()),
                player=world.player,
                caching_enabled=getattr(world, "rule_caching_enabled", False),
            )
        return super()._instantiate(world)

@dataclass
class HasWeapon(Rule["CupheadWorld"], game=ch):
    weapon_name: str

    @override
    def __post_init__(self):
        if self.weapon_name not in weapons.weapon_to_index.keys():
            raise KeyError(f"{self.weapon_name} not in weapon_dict")
        return super().__post_init__()

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        _weapon_name = weapons.weapon_to_index[self.weapon_name]
        return Has.Resolved(
            _weapon_name,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

@dataclass
class HasWeaponEx(HasWeapon, game=ch):
    @override
    def __post_init__(self):
        if self.weapon_name not in weapons.weapon_to_index.keys():
            raise KeyError(f"{self.weapon_name} not in weapon_dict")
        return super().__post_init__()

    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        if (world.options.weapon_mode.value & WeaponMode.EX_SEPARATE) > 0:
            _weapon_name = world.weapon_ex_dict[weapons.weapon_to_index[self.weapon_name]]
            _count = 1
        elif (world.options.weapon_mode.evalue & WeaponMode.PROGRESSIVE) > 0:
            _weapon_name = world.weapon_p_dict[weapons.weapon_to_index[self.weapon_name]]
            _count = 2
        else:
            _weapon_name = self.weapon_name
            _count = 1
        return Has.Resolved(
            _weapon_name,
            count=_count,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

@dataclass
class CanBuyOutShop(Rule["CupheadWorld"], game=ch):
    @override
    def _instantiate(self, world: "CupheadWorld") -> Rule.Resolved:
        return self.Resolved(
            regionnames.shop_sets if world.use_dlc else regionnames.base_shop_sets,
            player=world.player,
            caching_enabled=getattr(world, "rule_caching_enabled", False),
        )

    class Resolved(Rule.Resolved):
        region_names: tuple[str, ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return all(state.can_reach_region(rname, self.player) for rname in self.region_names)

        @override
        def item_dependencies(self) -> dict[str, set[int]]:
            return {itemnames.item_coin: {id(self)}}

        @override
        def region_dependencies(self) -> dict[str, set[int]]:
            return {rname: {id(self)} for rname in self.region_names}

        @override
        def explain_json(self, state: CollectionState | None = None) -> list[JSONMessagePart]:
            if state is None:
                return [{"type": "text", "text": "Can buy out shop"}]
            msg: list[JSONMessagePart] = [{"type": "text", "text": "Can buy out shop: "}]
            ans = ("green", "Yes") if self(state) else ("salmon", "No")
            msg.append({"type": "color", "color": ans[0], "text": ans[1]})
            return msg

        @override
        def explain_str(self, state: CollectionState | None = None) -> str:
            if state is None:
                return str(self)
            ans = "Yes" if self(state) else "No"
            return f"Can buy out shop: {ans}"

        @override
        def __str__(self) -> str:
            return "Can buy out shop"

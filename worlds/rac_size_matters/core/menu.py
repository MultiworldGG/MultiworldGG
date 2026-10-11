from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING

from .address_maps import MENU_ADDR_BY_PLANET_ID

if TYPE_CHECKING:
    from ..pypine import Pine

_STATE_OFFSET  = 0x00
_UPDATE_OFFSET = 0x04


class MenuStateValue(IntEnum):
    CLOSED            = 0x00
    PAUSE_MENU        = 0x03
    WEAPONS_VENDOR    = 0x09
    QUICK_SELECT_MENU = 0x0A
    MOD_VENDOR        = 0x0E
    PLANET_MENU       = 0x10
    PDA               = 0x12
    SKYBOARD_MENU     = 0x15


class MenuStateSlot:
    """Pine-backed accessor for the current menu state byte."""

    def __get__(self, instance, owner) -> MenuStateValue | None:
        if instance is None or instance.base is None:
            return None
        try:
            return MenuStateValue(instance.pine.read_int8(instance.base + _STATE_OFFSET))
        except ValueError:
            return None

    def __set__(self, instance, value: MenuStateValue) -> None:
        if instance.base is None:
            return
        instance.pine.write_int8(instance.base + _STATE_OFFSET, int(value))

    def __delete__(self, instance) -> None:
        if instance.base is None:
            return
        instance.pine.write_int8(instance.base + _STATE_OFFSET, int(MenuStateValue.CLOSED))


class MenuUpdateSlot:
    """Pine-backed accessor for the menu-change-request byte (write-only in practice)."""

    def __get__(self, instance, owner) -> int | None:
        if instance is None or instance.base is None:
            return None
        return instance.pine.read_int8(instance.base + _UPDATE_OFFSET)

    def __set__(self, instance, value: MenuStateValue) -> None:
        if instance.base is None:
            return
        instance.pine.write_int8(instance.base + _UPDATE_OFFSET, int(value))

    def __delete__(self, instance) -> None:
        if instance.base is None:
            return
        instance.pine.write_int8(instance.base + _UPDATE_OFFSET, 0)


class MenuInventory:
    """Pine-backed live accessor for the current menu state. Planet-dependent:
    call set_base(planet_id) whenever the loaded planet changes."""

    current = MenuStateSlot()
    update  = MenuUpdateSlot()

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self.base: int | None = None

    def set_base(self, planet_id: int) -> None:
        self.base = MENU_ADDR_BY_PLANET_ID.get(planet_id)

    def get(self) -> MenuStateValue | None:
        return self.current

    def set(self, value: MenuStateValue) -> None:
        """Request a menu change by writing to the update field."""
        self.update = value

    def delete(self) -> None:
        self.current = MenuStateValue.CLOSED

    @property
    def is_vendor(self) -> bool:
        return self.current in (MenuStateValue.WEAPONS_VENDOR, MenuStateValue.MOD_VENDOR, MenuStateValue.PDA)

    @property
    def is_weapons_vendor(self) -> bool:
        return self.current == MenuStateValue.WEAPONS_VENDOR

    @property
    def is_mod_vendor(self) -> bool:
        return self.current == MenuStateValue.MOD_VENDOR

    @property
    def is_pause_menu(self) -> bool:
        return self.current == MenuStateValue.PAUSE_MENU

    @property
    def is_planet_menu(self) -> bool:
        return self.current == MenuStateValue.PLANET_MENU

    @property
    def is_quick_select_menu(self) -> bool:
        return self.current == MenuStateValue.QUICK_SELECT_MENU

    def __repr__(self) -> str:
        return f"MenuInventory(current={self.current})"

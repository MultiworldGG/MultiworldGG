from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import TYPE_CHECKING

from .patches.skins import MODEL_IDS
from .structs.game import SkinStruct

if TYPE_CHECKING:
    from ..pypine import Pine


@dataclass(frozen=True)
class SkinData:
    unlock_mask: int | None
    equip_id:    int


class Skin(Enum):
    """Unlock mask / equip id pairs for each player skin."""
    DEFAULT          = SkinData(unlock_mask=0x01, equip_id=0x00)
    PIRATE_RATCHET   = SkinData(unlock_mask=0x02, equip_id=0x01)
    GODZILLA_RATCHET = SkinData(unlock_mask=0x04, equip_id=0x02)
    TRASH_RATCHET    = SkinData(unlock_mask=0x08,  equip_id=0x03)
    SWIM_RATCHET     = SkinData(unlock_mask=0x10,  equip_id=0x04)
    KANGA_RATCHET    = SkinData(unlock_mask=0x20,  equip_id=0x05)
    HIRO_RATCHET     = SkinData(unlock_mask=0x40,  equip_id=0x06)
    MP_RATCHET = SkinData(None, 7)
    SNOWMAN = SkinData(None, 8)
    HOTBOT = SkinData(None, 9)
    QWARK = SkinData(None, 10)
    NINJA = SkinData(None, 11)
    TRAINING_BOT = SkinData(None, 12)
    NURSE = SkinData(None, 13)
    TECHNOMITE = SkinData(None, 14)
    DAN = SkinData(None, 15)
    LOW_RIDER_RATCHET = SkinData(None, 16)
    SAMURAI_RATCHET = SkinData(None, 17)
    KANGAROO_RATCHET = SkinData(None, 18)
    TUXEDO_RATCHET = SkinData(None, 19)

    @property
    def unlock_mask(self) -> int | None:
        return self.value.unlock_mask

    @property
    def equip_id(self) -> int:
        return self.value.equip_id


SKIN_BY_EQUIP_ID: dict[int, Skin] = {s.equip_id: s for s in Skin}
ALL_SKINS_UNLOCK_MASK: int = 0x7F


class SkinSlot:
    """Pine-backed accessor for one SkinStruct field (unlocked bitmask or equipped id)."""

    def __init__(self, field: str) -> None:
        self.field = field

    @property
    def address(self):
        return SkinStruct.address_of(self.field)

    def __get__(self, instance, owner) -> int | None:
        if instance is None:
            return None
        return instance.pine.read_int8(self.address)

    def __set__(self, instance, value: int) -> None:
        if instance is None:
            return
        instance.pine.write_int8(self.address, value)

    def __delete__(self, instance) -> None:
        if instance is None:
            return
        instance.pine.write_int8(self.address, 0)


class SkinInventory:
    """Pine-backed live accessor for the equipped/unlocked skin bytes, replacing SkinState."""

    unlocked = SkinSlot("unlocked")
    equipped = SkinSlot("equipped")

    def __init__(self, pine: Pine) -> None:
        self.pine = pine
        self._skin: Skin = Skin.DEFAULT
        self._apply_pending = False

    def get(self) -> Skin:
        return SKIN_BY_EQUIP_ID.get(self.equipped, Skin.DEFAULT)

    def set(self, skin: Skin) -> None:
        self._skin = skin
        self.equipped = skin.equip_id
        self.unlocked = ALL_SKINS_UNLOCK_MASK
        self._apply_pending = True

    def set_by_option(self, value: int) -> None:
        self.set(SKIN_BY_EQUIP_ID.get(value, Skin.DEFAULT))

    def delete(self) -> None:
        self.set(Skin.DEFAULT)

    def setup(self) -> None:
        """Write the currently selected skin's unlock/equip bytes into game memory."""
        self.equipped = self._skin.equip_id
        self.unlocked = ALL_SKINS_UNLOCK_MASK
        self._apply_pending = True

    def apply_pending(self, plan, *, allowed: bool) -> None:
        """Queue a game-thread model refresh without opening the skin menu."""
        if plan is None or not allowed:
            return
        if not self._apply_pending:
            # Keep a skin selected in the game menu on the next planet too.
            self._skin = self.get()
            return
        plan._validate(replacement=True)
        if MODEL_IDS[self._skin.equip_id] >= plan.model_count:
            return  # Wait for a level with the extended loader installed.
        self.pine.write_int8(plan.request, MODEL_IDS[self._skin.equip_id])
        self._apply_pending = False

    def __repr__(self) -> str:
        return f"SkinInventory(skin={self._skin.name})"

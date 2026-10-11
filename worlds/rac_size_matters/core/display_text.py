from __future__ import annotations

import asyncio
import struct
from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pypine import Pine


class TextColour:
    YELLOW  = bytes([0x90, 0x10])
    PURPLE = bytes([0x90, 0x04])
    RED = bytes([0x90, 0x03])
    ORANGE = bytes([0x90, 0x02])
    WHITE  = bytes([0x90, 0x01])


def colored_text(*parts: bytes | str) -> bytes:
    """Build a null-terminated byte string from text and TextColour constants."""
    buf = bytearray()
    for part in parts:
        buf.extend(part if isinstance(part, (bytes, bytearray)) else part.encode("ascii"))
    buf.append(0x00)
    return bytes(buf)


from . import address_maps
from .address_maps import (
    MULTI_LINE_TEXT_BOX_BY_PLANET,
    SMALL_TEXT_BOX_BY_PLANET,
    STATIC_TEXT_BUFFER as _STATIC_TEXT_BUFFER,
)


@dataclass(frozen=True)
class SmallTextBox:
    planet_id: int
    base_addr: int

    @property
    def countdown_timer(self) -> int:     return self.base_addr
    @property
    def is_visible(self) -> int:          return self.base_addr + 0x20
    @property
    def message_str_pointer(self) -> int: return self.base_addr + 0x28

    def write_message(self, ipc, msg_id: int) -> None:
        ipc.write_int16(self.message_str_pointer, msg_id)

    def write_text(self, ipc, text: bytes) -> None:
        if address_maps.STATIC_TEXT_BUFFER is None:
            raise RuntimeError("This region requires native text notifications")
        ipc.write_bytes(address_maps.STATIC_TEXT_BUFFER, text)
        ipc.write_int32(self.message_str_pointer, address_maps.STATIC_TEXT_BUFFER)
        ipc.write_int8(self.countdown_timer, 0xAA)
        trigger_addr = self.base_addr + 0x39
        ipc.write_int8(trigger_addr, 0x02)
        asyncio.get_event_loop().call_later(7.0, lambda: ipc.write_int8(trigger_addr, 0x01))


@dataclass(frozen=True)
class MultiLineTextBox:
    planet_id: int
    base_addr: int

    @property
    def countdown_timer(self) -> int:     return self.base_addr
    @property
    def is_visible(self) -> int:          return self.base_addr + 0x20
    @property
    def message_str_pointer(self) -> int: return self.base_addr + 0x28

    def write_message(self, ipc, msg_id: int) -> None:
        ipc.write_int16(self.message_str_pointer, msg_id)

    def write_text(self, ipc, text: bytes) -> None:
        if address_maps.STATIC_TEXT_BUFFER is None:
            raise RuntimeError("This region requires native text notifications")
        ipc.write_bytes(address_maps.STATIC_TEXT_BUFFER, text)
        ipc.write_int32(self.message_str_pointer, address_maps.STATIC_TEXT_BUFFER)
        ipc.write_int8(self.countdown_timer, 0xFF)
        trigger_addr = self.base_addr + 0x39
        ipc.write_int8(trigger_addr, 0x02)
        asyncio.get_event_loop().call_later(5.0, lambda: ipc.write_int8(trigger_addr, 0x01))


TextBoxConfig = SmallTextBox | MultiLineTextBox


SmallTextBoxAddrs: list[SmallTextBox] = [
    SmallTextBox(planet_id=pid, base_addr=addr)
    for pid, addr in SMALL_TEXT_BOX_BY_PLANET.items()
]

MultiLineTextBoxAddrs: list[MultiLineTextBox] = [
    MultiLineTextBox(planet_id=pid, base_addr=addr)
    for pid, addr in MULTI_LINE_TEXT_BOX_BY_PLANET.items()
]


class TextBoxInventory:
    """Pine-backed accessor for a planet's text box (small or multi-line).
    Planet-dependent: call set_base(planet_id) whenever the loaded planet changes."""

    def __init__(self, pine: Pine, boxes: list[TextBoxConfig]) -> None:
        self.pine = pine
        self._by_planet: dict[int, TextBoxConfig] = {tb.planet_id: tb for tb in boxes}
        self._config: TextBoxConfig | None = None

    def set_base(self, planet_id: int) -> None:
        self._config = self._by_planet.get(planet_id)

    def get(self) -> str | None:
        cfg = self._config
        if cfg is None:
            return None
        timer = struct.unpack_from("<f", self.pine.read_bytes(cfg.countdown_timer, 4))[0]
        if timer <= 0:
            return None
        ptr = self.pine.read_int32(cfg.message_str_pointer)
        if ptr != address_maps.STATIC_TEXT_BUFFER:
            return None
        return self.pine.read_string(address_maps.STATIC_TEXT_BUFFER, 256)

    def set(self, text: bytes | str) -> None:
        cfg = self._config
        if cfg is None:
            return
        data = text if isinstance(text, (bytes, bytearray)) else colored_text(text)
        cfg.write_text(self.pine, data)

    def delete(self) -> None:
        cfg = self._config
        if cfg is None:
            return
        self.pine.write_int8(cfg.countdown_timer, 0)
        self.pine.write_int8(cfg.base_addr + 0x39, 0x01)

    @property
    def is_displayed(self) -> bool:
        return self.get() is not None

    def __repr__(self) -> str:
        return f"TextBoxInventory(displayed={self.is_displayed})"


def small_text_box_inventory(pine: Pine) -> TextBoxInventory:
    return TextBoxInventory(pine, [SmallTextBox(pid, addr) for pid, addr in SMALL_TEXT_BOX_BY_PLANET.items()])


def multi_line_text_box_inventory(pine: Pine) -> TextBoxInventory:
    return TextBoxInventory(pine, [MultiLineTextBox(pid, addr) for pid, addr in MULTI_LINE_TEXT_BOX_BY_PLANET.items()])

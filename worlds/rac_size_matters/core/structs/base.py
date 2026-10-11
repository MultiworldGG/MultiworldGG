from __future__ import annotations

import ctypes
from typing import Any


class MemoryStruct(ctypes.LittleEndianStructure):

    BASE_ADDRESS: int = 0x0000

    @classmethod
    def address_of(cls, field_name: str) -> int:
        return cls.BASE_ADDRESS + getattr(cls, field_name).offset

    @classmethod
    def size(cls) -> int:
        return ctypes.sizeof(cls)

    @classmethod
    def field_size(cls, field_name: str) -> int:
        return getattr(cls, field_name).size

    @classmethod
    def field_offset(cls, field_name: str) -> int:
        return getattr(cls, field_name).offset

    @classmethod
    def field_names(cls) -> list[str]:
        return [name for name, *_ in cls._fields_]

    @classmethod
    def from_bytes(cls, raw: bytes) -> MemoryStruct:
        instance = cls()
        ctypes.memmove(ctypes.addressof(instance), raw, ctypes.sizeof(cls))
        return instance

    def to_bytes(self) -> bytes:
        return bytes(self)

    def to_dict(self) -> dict[str, Any]:
        return {name: getattr(self, name) for name in self.field_names()}

    def update_from_dict(self, data: dict[str, Any]) -> None:
        for name, value in data.items():
            if hasattr(self, name):
                setattr(self, name, value)

    def __repr__(self) -> str:
        fields = ", ".join(f"{k}={v!r}" for k, v in self.to_dict().items())
        return f"{self.__class__.__name__}({fields})"

import abc
from struct import Struct

from .type_aliases import TCSContext


AREA_ID_CANTINA = 66


class StaticUChar(int):
    def get(self, ctx: TCSContext) -> int:
        return ctx.read_uchar(self)

    def set(self, ctx: TCSContext, value: int):
        ctx.write_byte(self, value)


class StaticFloat(int):
    def get(self, ctx: TCSContext) -> float:
        return ctx.read_float(self)

    def set(self, ctx: TCSContext, value: float):
        ctx.write_float(self, value)


class StaticUint(int):
    def get(self, ctx: TCSContext) -> int:
        return ctx.read_uint(self)

    def set(self, ctx: TCSContext, value: int):
        ctx.write_uint(self, value)


class StaticInt(int):
    def get(self, ctx: TCSContext) -> int:
        return ctx.read_int(self)

    def set(self, ctx: TCSContext, value: int):
        ctx.write_int(self, value)


class StaticBOOL(StaticUint):
    """Microsoft 4-byte BOOL"""
    def get(self, ctx: TCSContext) -> bool:
        return super().get(ctx) != 0


class FloatField(int):
    def get(self, ctx: TCSContext, raw_address: int) -> float:
        return ctx.read_float(raw_address + self, raw=True)

    def set(self, ctx: TCSContext, raw_address: int, value: float):
        ctx.write_float(raw_address + self, value, raw=True)


class UintField(int):
    def get(self, ctx: TCSContext, raw_address: int) -> int:
        return ctx.read_uint(raw_address + self, raw=True)

    def set(self, ctx: TCSContext, raw_address: int, value: int):
        ctx.write_uint(raw_address + self, value, raw=True)


class UCharField(int):
    def get(self, ctx: TCSContext, raw_address: int) -> int:
        return ctx.read_uchar(raw_address + self, raw=True)

    def set(self, ctx: TCSContext, raw_address: int, value: int):
        ctx.write_byte(raw_address + self, value, raw=True)


class UShortField(int):
    def get(self, ctx: TCSContext, raw_address: int) -> int:
        return ctx.read_ushort(raw_address + self, raw=True)

    def set(self, ctx: TCSContext, raw_address: int, value: int):
        ctx.write_ushort(raw_address + self, value, raw=True)


class NuVecField(int):
    _struct = Struct("<3f")

    def get(self, ctx: TCSContext, raw_address: int) -> tuple[float, float, float]:
        return self._struct.unpack(ctx.read_bytes(raw_address + self, self._struct.size, raw=True))  # type: ignore

    def set(self, ctx: TCSContext, raw_address: int, value: tuple[float, float, float]) -> None:
        ctx.write_bytes(raw_address + self, self._struct.pack(*value), self._struct.size, raw=True)


class ClientComponent(abc.ABC):
    pass

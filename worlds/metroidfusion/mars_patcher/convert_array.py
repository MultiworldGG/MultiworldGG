from .common_types import BytesLike
from .rom import ROM_OFFSET


def u8_to_u16(data: BytesLike | list[int]) -> list[int]:
    """Converts a bytes object or list of 8-bit integers to a list of 16-bit integers."""
    assert len(data) % 2 == 0, "Data length must be a multiple of 2"
    return [data[i] | (data[i + 1] << 8) for i in range(0, len(data), 2)]


def u16_to_u8(data: list[int]) -> bytes:
    """Converts a list of 16-bit integers to a bytes object of 8-bit integers."""
    output = bytearray()
    for val in data:
        output.append(val & 0xFF)
        output.append(val >> 8)
    return bytes(output)


def ptr_to_u8(val: int) -> bytes:
    """Converts a single pointer to a bytes object of 8-bit integers."""
    assert val < ROM_OFFSET, f"Pointer should be less than {ROM_OFFSET:X} but is {val:X}"
    val += ROM_OFFSET
    return bytes([val & 0xFF, (val >> 8) & 0xFF, (val >> 16) & 0xFF, val >> 24])

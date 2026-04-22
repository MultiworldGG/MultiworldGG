
import struct
from io import BytesIO
from typing import BinaryIO, Any
from types import GenericAlias

PADDING_BYTES = b"This is padding data to alignme"

class InvalidOffsetError(Exception):
  pass

def data_len(data: BinaryIO) -> int:
  data_length = data.seek(0, 2)
  return data_length

def make_copy_data(data: BinaryIO) -> BytesIO:
  copy_data = read_all_bytes(data)
  return BytesIO(copy_data)

def read_sub_data(data: BinaryIO, offset: int, length: int) -> BytesIO:
  data.seek(offset)
  return BytesIO(data.read(length))


def read_all_bytes(data: BinaryIO) -> bytes:
  data.seek(0)
  return data.read()

def read_bytes(data: BinaryIO, offset: int, length: int) -> bytes:
  data.seek(offset)
  return data.read(length)

def write_bytes(data: BinaryIO, offset: int, raw_bytes: bytes):
  data.seek(offset)
  data.write(raw_bytes)

def read_and_unpack_bytes(data: BinaryIO, offset: int, length: int, format_string: str):
  data.seek(offset)
  requested_data = data.read(length)
  unpacked_data = struct.unpack(format_string, requested_data)
  return unpacked_data

def write_and_pack_bytes(data: BinaryIO, offset: int, new_values: list[Any], format_string: str | bytes):
  packed_data = struct.pack(format_string, *new_values)
  data.seek(offset)
  data.write(packed_data)


def read_str(data: BinaryIO, offset: int, length: int) -> str:
  data_length = data.seek(0, 2)
  if offset+length > data_length:
    raise InvalidOffsetError("Offset 0x%X, length 0x%X is past the end of the data (length 0x%X)." % (offset, length, data_length))
  data.seek(offset)
  string = data.read(length).decode("shift_jis")
  string = string.rstrip("\0") # Remove trailing null bytes
  return string

def try_read_str(data: BinaryIO, offset: int, length: int):
  try:
    return read_str(data, offset, length)
  except UnicodeDecodeError:
    return None
  except InvalidOffsetError:
    return None

def read_str_until_null_character(data: BinaryIO, offset: int) -> str:
  data_length = data.seek(0, 2)
  if offset > data_length:
    raise InvalidOffsetError("Offset 0x%X is past the end of the data (length 0x%X)." % (offset, data_length))
  
  temp_offset = offset
  str_length = 0
  while temp_offset < data_length:
    data.seek(temp_offset)
    char = data.read(1)
    if char == b"\0":
      break
    else:
      str_length += 1
    temp_offset += 1
  
  data.seek(offset)
  string = data.read(str_length).decode("shift_jis")
  
  return string

def write_str(data: BinaryIO, offset: int, new_string: str, max_length: int):
  # Writes a fixed-length string.
  # Although it is fixed-length, it still must have a null character terminating it, so the real max length is one less than the passed max_length argument.
  
  str_len = len(new_string)
  if str_len >= max_length:
    raise Exception("String \"%s\" is too long (max length including null byte: 0x%X)" % (new_string, max_length))
  
  padding_length = max_length - str_len
  null_padding = b"\x00"*padding_length
  new_value = new_string.encode("shift_jis") + null_padding
  
  data.seek(offset)
  data.write(new_value)

def write_magic_str(data: BinaryIO, offset: int, new_string: str, max_length: int):
  # Writes a fixed-length string that does not have to end with a null byte.
  # This is for magic file format identifiers.
  
  str_len = len(new_string)
  if str_len > max_length:
    raise Exception("String %s is too long (max length 0x%X)" % (new_string, max_length))
  
  padding_length = max_length - str_len
  null_padding = b"\x00"*padding_length
  new_value = new_string.encode("shift_jis") + null_padding
  
  data.seek(offset)
  data.write(new_value)

def write_str_with_null_byte(data: BinaryIO, offset: int, new_string: str):
  # Writes a non-fixed length string.
  
  str_len = len(new_string)
  write_str(data, offset, new_string, str_len+1)


def read_u8(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">B", data.read(1))[0]

def read_u16(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">H", data.read(2))[0]

def read_u24(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">I", b'\0' + data.read(3))[0]

def read_u32(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">I", data.read(4))[0]

def read_float(data: BinaryIO, offset: int) -> float:
  data.seek(offset)
  return struct.unpack(">f", data.read(4))[0]


def read_s8(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">b", data.read(1))[0]

def read_s16(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">h", data.read(2))[0]

def read_s32(data: BinaryIO, offset: int) -> int:
  data.seek(offset)
  return struct.unpack(">i", data.read(4))[0]


def write_u8(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">B", new_value)
  data.seek(offset)
  data.write(new_bytes)

def write_u16(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">H", new_value)
  data.seek(offset)
  data.write(new_bytes)

def write_u24(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">I", new_value)
  assert new_bytes[0] == 0
  data.seek(offset)
  data.write(new_bytes[1:])

def write_u32(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">I", new_value)
  data.seek(offset)
  data.write(new_bytes)

def write_float(data: BinaryIO, offset: int, new_value: float):
  new_bytes = struct.pack(">f", new_value)
  data.seek(offset)
  data.write(new_bytes)


def write_s8(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">b", new_value)
  data.seek(offset)
  data.write(new_bytes)

def write_s16(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">h", new_value)
  data.seek(offset)
  data.write(new_bytes)

def write_s32(data: BinaryIO, offset: int, new_value: int):
  new_bytes = struct.pack(">i", new_value)
  data.seek(offset)
  data.write(new_bytes)


def bit_cast_float_to_int(value: float) -> int:
  raw_bytes = struct.pack(">f", value)
  return struct.unpack(">I", raw_bytes)[0]

def bit_cast_int_to_float(value: int) -> float:
  raw_bytes = struct.pack(">I", value)
  return struct.unpack(">f", raw_bytes)[0]


def align_data_to_nearest(data: BinaryIO, size: int, padding_bytes:bytes=PADDING_BYTES):
  current_end = data_len(data)
  next_offset = current_end + (size - current_end % size) % size
  padding_needed = next_offset - current_end
  data.seek(current_end)
  padding = padding_bytes*(padding_needed // len(padding_bytes))
  padding += padding_bytes[:padding_needed % len(padding_bytes)]
  data.write(padding)

def pad_offset_to_nearest(offset: int, size: int) -> int:
  next_offset = offset + (size - offset % size) % size
  return next_offset

def align_data_and_pad_offset(data: BinaryIO, offset: int, size: int, padding_bytes:bytes=PADDING_BYTES) -> int:
  next_offset = offset + (size - offset % size) % size
  padding_needed = next_offset - offset
  data.seek(offset)
  padding = padding_bytes*(padding_needed // len(padding_bytes))
  padding += padding_bytes[:padding_needed % len(padding_bytes)]
  data.write(padding)
  return next_offset


class u32(int):
  pass

class u24(int):
  pass

class u16(int):
  pass

class u8(int):
  pass

class s32(int):
  pass

class s16(int):
  pass

class s8(int):
  pass

class u16Rot(u16):
  pass

class FixedStr(str):
  def __class_getitem__(cls, klass: type):
    return GenericAlias(cls, klass)

class MagicStr(str):
  def __class_getitem__(cls, klass: type):
    return GenericAlias(cls, klass)

class MappedBool(u8):
  VALID_VALUES = {
    0x00: False,
    0x01: True,
  }
  
  def __init__(self, raw_value: int):
    assert 0 <= raw_value <= 255
    self.raw_value = raw_value
  
  def __bool__(self):
    return self.VALID_VALUES[self.raw_value]

class Bool255isFalse(MappedBool):
  VALID_VALUES = {
    0x00: False,
    0x01: True,
    0xFF: False,
  }

PRIMITIVE_TYPE_TO_BYTE_SIZE = {
  u32  : 4,
  u24  : 3,
  u16  : 2,
  u8   : 1,
  s32  : 4,
  s16  : 2,
  s8   : 1,
  float: 4,
}

PRIMITIVE_TYPE_TO_READ_FUNC = {
  u32  : read_u32,
  u24  : read_u24,
  u16  : read_u16,
  u8   : read_u8,
  s32  : read_s32,
  s16  : read_s16,
  s8   : read_s8,
  float: read_float,
}

PRIMITIVE_TYPE_TO_WRITE_FUNC = {
  u32  : write_u32,
  u24  : write_u24,
  u16  : write_u16,
  u8   : write_u8,
  s32  : write_s32,
  s16  : write_s16,
  s8   : write_s8,
  float: write_float,
}

PRIMITIVE_TYPE_IS_SIGNED = {
  u32  : False,
  u24  : False,
  u16  : False,
  u8   : False,
  s32  : True,
  s16  : True,
  s8   : True,
  float: True,
}

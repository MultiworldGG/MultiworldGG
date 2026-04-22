from typing import BinaryIO, ClassVar
from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import BUNFOE, bunfoe, field

class MDLCommand(BUNFOE):
  VALID_REGISTERS: ClassVar[list[Enum]] = []
  
  @classmethod
  def new_from_register(cls, register: Enum, data: BinaryIO):
    # When instantiating the base class, try to find if any subclasses are for this register.
    for subcls in cls.__subclasses__():
      if register in subcls.VALID_REGISTERS:
        return subcls(data)
    # If not, just return a generic version of the command that holds a bitfield.
    return cls(data)
  
  def assert_valid(self):
    raise NotImplementedError
  
  def read(self, offset: int) -> int:
    offset = super().read(offset)
    self.assert_valid()
    return offset
  
  def save(self, offset: int) -> int:
    self.assert_valid()
    return super().save(offset)

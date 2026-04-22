import dataclasses
from dataclasses import MISSING, InitVar
from enum import Enum
from typing import Any, BinaryIO, ClassVar, Self, Type, TypeVar, dataclass_transform
from types import GenericAlias
import typing
import types
import functools
from io import BytesIO
import copy

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr, MappedBool

# TODO: implement read_only attribute (for stuff like magic strings)
# TODO: implement hidden attribute (for e.g. array length fields)
# TODO: implement valid_range attribute (for integers that aren't allowed to take up the full range their bit size allows)
# TODO: assert that bitfield bits we never even read are always 0? maybe make it an option when creating the bitfield, assert_unread_zero?
# TODO: allow @property decorator functions to appear in the GUI as if they were fields?
# TODO: need to split the ignore option into two:
#       one would prevent it from being read automatically (e.g. MDL3.entries). maybe call it noread.
#       the other would make it hidden and not show up in fields()/asdict()? e.g. INF1.parent

T = TypeVar('T')

# A sentinel object to detect if a field with no default value hasn't been read yet.
# Use a class to give it a better repr.
class _UNREAD_TYPE:
  pass
UNREAD = _UNREAD_TYPE()


PRINT_INVALID_VALUE_WARNINGS = True


class Field(dataclasses.Field):
  __slots__ = ('name', 'type', 'default', 'default_factory', 'repr',
               'hash', 'init', 'compare', 'metadata', 'kw_only',
               '_field_type',  # Private: not to be used by user code.
               # Custom.
               'length', 'length_calculator', 'ignore', 'bitfield', 'bits', 'assert_default',
               )

  def __init__(self, default, default_factory, init, repr, hash, compare, metadata, kw_only,
               length, length_calculator, ignore, bitfield, bits, assert_default):
    self.name = None
    self.type = None
    self.default = default
    self.default_factory = default_factory
    self.init = init
    self.repr = repr
    self.hash = hash
    self.compare = compare
    self.metadata = (dataclasses._EMPTY_METADATA
                      if metadata is None else
                      types.MappingProxyType(metadata))
    self.kw_only = kw_only
    self._field_type = None
    
    # Custom.
    self.length = length
    self.length_calculator = length_calculator
    self.ignore = ignore
    self.bitfield = bitfield
    self.bits = bits
    self.assert_default = assert_default

  @dataclasses._recursive_repr
  def __repr__(self):
    return ('Field('
            f'name={self.name!r},'
            f'type={self.type!r},'
            f'default={self.default!r},'
            f'default_factory={self.default_factory!r},'
            f'init={self.init!r},'
            f'repr={self.repr!r},'
            f'hash={self.hash!r},'
            f'compare={self.compare!r},'
            f'metadata={self.metadata!r},'
            f'kw_only={self.kw_only!r},'
            f'_field_type={self._field_type},'
            
            # Custom.
            f'length={self.length!r},'
            f'length_calculator={self.length_calculator!r},'
            f'ignore={self.ignore!r},'
            f'bitfield={self.bitfield!r},'
            f'bits={self.bits!r},'
            f'assert_default={self.assert_default!r},'
            ')')


def field(*, default=MISSING, default_factory=MISSING, init=True, repr=True,
          hash=None, compare=True, metadata=None, kw_only=MISSING,
          length=MISSING, length_calculator=MISSING, ignore=False, bitfield=False, bits=None,
          assert_default=False) -> Any:
  if assert_default and default is MISSING:
    raise ValueError('must specify default when assert_default is specified')
  if default is MISSING and default_factory is MISSING:
    # If no default was specified for this field, we don't want to make it a required argument to
    # __init__ when instantiating the class, as that would interfere with creating a blank instance
    # with no arguments, which is done immediately prior to calling read(). So instead, we set the
    # default to a special object we call UNREAD, which acts as a sentinel that this instance hasn't
    # had its values properly unpacked yet.
    default = UNREAD
  if length is not MISSING and length_calculator is not MISSING:
    raise ValueError('cannot specify both length and length_calculator')
  if bitfield and bits is not None:
    raise ValueError('cannot specify both bitfield and bits')
  if bitfield and default == UNREAD:
    default = 0
  return Field(default, default_factory, init, repr, hash, compare,
               metadata, kw_only, length, length_calculator, ignore, bitfield, bits, assert_default)

def fields(class_or_instance, include_ignored=False) -> tuple[Field, ...]:
  if not isinstance(class_or_instance, BUNFOE) and not issubclass(class_or_instance, BUNFOE):
    raise TypeError(f'{class_or_instance} does not inherit from BUNFOE') from None
  if not hasattr(class_or_instance, dataclasses._FIELDS):
    raise TypeError(f'{class_or_instance} does not use the @bunfoe decorator') from None
  dataclass_fields = dataclasses.fields(class_or_instance)
  if not include_ignored:
    dataclass_fields = [f for f in dataclass_fields if not f.ignore]
  return dataclass_fields


def _process_class(cls, init, repr, eq, order, unsafe_hash, frozen,
                   match_args, kw_only, slots, weakref_slot):
  cls_annotations = cls.__dict__.get('__annotations__', {})
  for field_name, field_type in cls_annotations.items():
    default = getattr(cls, field_name, MISSING)
    if not isinstance(default, Field):
      if isinstance(default, dataclasses.Field):
        raise ValueError("Used a dataclass field instead of a BUNFOE field")
      setattr(cls, field_name, field(default=default))
  
  cls = dataclasses._process_class(cls, init, repr, eq, order, unsafe_hash, frozen,
                                   match_args, kw_only, slots, weakref_slot)
  
  try:
    base_class = BUNFOE # @IgnoreException
    assert issubclass(cls, base_class), f"Class {cls.__name__} must inherit from BUNFOE"
  except NameError:
    # BUNFOE isn't defined yet as we're still in the middle of creating that class.
    assert cls.__name__ == "BUNFOE"
  
  return cls

@dataclass_transform(kw_only_default=True, field_specifiers=(field, Field))
def bunfoe(cls=None, /, *,
           # Dataclass arguments. Most defaults are left the same, but kw_only is changed from False
           # to True in order to make normal fields keyword arguments by default.
           init=True, repr=True, eq=True, order=False,
           unsafe_hash=False, frozen=False, match_args=True,
           kw_only=True, slots=False, weakref_slot=False,
           ):
  def wrap(cls):
    return _process_class(cls,
      init=init, repr=repr, eq=eq, order=order,
      unsafe_hash=unsafe_hash, frozen=frozen, match_args=match_args,
      kw_only=kw_only, slots=slots, weakref_slot=weakref_slot
    )

  if cls is None:
    # Called as @bunfoe() with parentheses.
    return wrap

  # Called as @bunfoe without parentheses.
  return wrap(cls)


@bunfoe(eq=False)
class BUNFOE:
  """Binary-UNpacking Field-Owning Entity.
  
  This is a wrapper around dataclasses that implements automatic reading and writing of binary
  struct data."""
  
  # data is the binary data the instance will be unpacked from upon calling read().
  # If not passed upon instantiation, it will default to a new blank BytesIO.
  data: BinaryIO = field(default_factory=BytesIO, repr=False, compare=False, kw_only=False, ignore=True)
  
  DATA_SIZE: ClassVar = None
  # TODO: automatically calculate BYTE_SIZE based on the size of all the fields combined?
  
  def __post_init__(self):
    # This doesn't do anything, it's just a dummy in case any child classes want to call super.
    pass
  
  def copy(self, /, **changes) -> Self:
    return dataclasses.replace(self, **changes)
  
  def asdict(self) -> dict:
    result = []
    for field in fields(self):
      result.append((field.name, self._asdict_inner(getattr(self, field.name))))
    return dict(result)
  
  def _asdict_inner(self, obj):
    if isinstance(obj, BUNFOE):
      return obj.asdict()
    elif isinstance(obj, (list, tuple)):
      return type(obj)(self._asdict_inner(v) for v in obj)
    elif issubclass(type(obj), Enum):
      return str(obj)
    else:
      return copy.deepcopy(obj)
  
  @staticmethod
  @functools.cache
  def get_byte_size(field_type: Type) -> int:
    if field_type in fs.PRIMITIVE_TYPE_TO_BYTE_SIZE:
      return fs.PRIMITIVE_TYPE_TO_BYTE_SIZE[field_type]
    elif field_type == bool or issubclass(field_type, MappedBool):
      return BUNFOE.get_byte_size(u8)
    elif issubclass(field_type, u16Rot):
      return BUNFOE.get_byte_size(u16)
    elif isinstance(field_type, GenericAlias) and field_type.__origin__ in [FixedStr, MagicStr]:
      return typing.get_args(field_type)[0]
    elif issubclass(field_type, Enum):
      for base_class in field_type.__mro__:
        if issubclass(base_class, int) and base_class in fs.PRIMITIVE_TYPE_TO_BYTE_SIZE:
          return BUNFOE.get_byte_size(base_class)
      raise TypeError(f"Enum {field_type} must inherit from a primitive int subclass.")
    elif issubclass(field_type, BUNFOE):
      # NOTE: This currently relies on the class defining all fields, including any trailing
      # padding. Maybe in the future it could double check a DATA_SIZE/BYTE_SIZE constant.
      size = 0
      for subfield in fields(field_type):
        if subfield.bits is not None:
          continue
        if isinstance(subfield.type, GenericAlias) and subfield.type.__origin__ == list:
          if subfield.length is not MISSING:
            size += BUNFOE.get_list_field_byte_size(subfield)
          else:
            # Impossible to statically determine the byte size of a dynamically-sized field.
            return None
        else:
          size += BUNFOE.get_byte_size(subfield.type)
      return size
    else:
      raise NotImplementedError
  
  @staticmethod
  def get_field_byte_size(field: Field):
    if field.bits is not None:
      return None
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      if field.length is not MISSING:
        return BUNFOE.get_list_field_byte_size(field)
      else:
        # Impossible to statically determine the byte size of a dynamically-sized field.
        return None
    else:
      return BUNFOE.get_byte_size(field.type)
  
  @staticmethod
  def get_list_field_byte_size(field: Field):
    assert field.length is not MISSING and field.length > 0
    type_args = typing.get_args(field.type)
    assert len(type_args) == 1
    arg_type = type_args[0]
    
    arg_size = BUNFOE.get_byte_size(arg_type)
    return arg_size * field.length
  
  #region Reading
  def read(self, offset: int) -> int:
    orig_offset = offset
    bitfield = None
    bit_offset = None
    for field in fields(self):
      if bitfield is None:
        assert field.bits is None, "Specified the bits argument when no bitfield was active."
      else:
        if field.bits is None:
          # Reached the end of the current bitfield.
          # This next field isn't part of the last bitfield we saw.
          bitfield = None
          bit_offset = None
        else:
          bit_offset = self.read_bitfield_property(bitfield, field, bit_offset)
          continue
      
      # print(f"0x{offset - orig_offset:X} {field.name}")
      offset = self.read_field(field, offset)
      if field.bitfield:
        bitfield = field
        bit_offset = 0
    
    assert offset >= orig_offset
    if self.DATA_SIZE is not None:
      size_read = offset - orig_offset
      assert size_read == self.DATA_SIZE, f"Expected {self.__class__.__name__} to be 0x{self.DATA_SIZE:X} bytes, but read 0x{size_read:X} bytes"
    
    return offset
  
  def read_field(self, field: Field, offset: int) -> int:
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      value, offset = self.read_list_field(field, offset)
    else:
      value = self.read_value(field.type, offset)
      offset += self.get_byte_size(field.type)
    
    setattr(self, field.name, value)
    if field.assert_default:
      assert value == field.default, f"Field {field.name} expected value {field.default}, but got {value}"
    return offset
  
  def get_list_length(self, field: Field):
    if field.length is not MISSING:
      return field.length
    if field.length_calculator is not MISSING:
      # length_calculator is a lambda that takes a BUNFOE instance as its only argument and calculates the dynamic list
      # length based on that instance's earlier fields.
      return field.length_calculator(self)
    raise NotImplementedError
  
  def read_list_field(self, field: Field, offset: int) -> tuple[list, int]:
    type_args = typing.get_args(field.type)
    assert len(type_args) == 1
    arg_type = type_args[0]
    
    value = []
    for i in range(self.get_list_length(field)):
      element = self.read_value(arg_type, offset)
      offset += self.get_byte_size(arg_type)
      value.append(element)
    
    return value, offset
  
  def read_bitfield_property(self, bitfield: Field, field: Field, bit_offset: int):
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      value, bit_offset = self.read_bitfield_property_list_field(bitfield, field, bit_offset)
    else:
      value = self.read_bitfield_property_value(bitfield, field.type, bit_offset, field.bits)
      bit_offset += field.bits
    
    setattr(self, field.name, value)
    if field.assert_default:
      assert value == field.default, f"Field {field.name} expected value {field.default}, but got {value}"
    return bit_offset
  
  def read_bitfield_property_list_field(self, bitfield: Field, field: Field, bit_offset: int) -> tuple[list, int]:
    type_args = typing.get_args(field.type)
    assert len(type_args) == 1
    arg_type = type_args[0]
    
    value = []
    for i in range(self.get_list_length(field)):
      element = self.read_bitfield_property_value(bitfield, arg_type, bit_offset, field.bits)
      bit_offset += field.bits
      value.append(element)
    
    return value, bit_offset
  
  def read_bitfield_property_value(self, bitfield: Field, field_type: Type[T], bit_offset: int, bits: int) -> T:
    total_bits = self.get_byte_size(bitfield.type)*8
    assert 0 <= bit_offset < total_bits
    assert 1 <= bits <= total_bits
    assert 1 <= bit_offset+bits <= total_bits
    
    bitfield_value = getattr(self, bitfield.name)
    bit_mask = (1 << bits) - 1
    raw_value = (bitfield_value >> bit_offset) & bit_mask
    bit_offset += bits
    
    if field_type == bool:
      assert raw_value in [0, 1], f"Boolean must be zero or one, but got value: {raw_value}"
    elif issubclass(field_type, MappedBool):
      assert PRINT_INVALID_VALUE_WARNINGS and raw_value in field_type.VALID_VALUES, f"Boolean value not valid: {raw_value}"
    
    if issubclass(field_type, Enum):
      if raw_value in field_type:
        value = field_type(raw_value)
      else:
        if PRINT_INVALID_VALUE_WARNINGS:
          print(f"Invalid value for enum {field_type}: {raw_value}")
        value = raw_value
    elif issubclass(field_type, int) or issubclass(field_type, bool):
      value = field_type(raw_value)
    elif issubclass(field_type, float):
      value = field_type(fs.bit_cast_int_to_float(raw_value))
    else:
      raise NotImplementedError(f"Reading type {field_type} from a bitfield is not currently implemented")
    
    return value
  
  def read_value(self, field_type: Type[T], offset: int) -> T:
    if field_type in fs.PRIMITIVE_TYPE_TO_READ_FUNC:
      read_func = fs.PRIMITIVE_TYPE_TO_READ_FUNC[field_type]
      return read_func(self.data, offset)
    elif field_type == bool:
      raw_value = self.read_value(u8, offset)
      assert raw_value in [0, 1], f"Boolean must be zero or one, but got value: {raw_value}"
      return bool(raw_value)
    elif issubclass(field_type, MappedBool):
      raw_value = self.read_value(u8, offset)
      assert raw_value in field_type.VALID_VALUES, f"Boolean value not valid: {raw_value}"
      return field_type(raw_value)
    elif issubclass(field_type, u16Rot):
      return self.read_value(u16, offset)
    elif isinstance(field_type, GenericAlias) and field_type.__origin__ in [FixedStr, MagicStr]:
      str_len = typing.get_args(field_type)[0]
      return fs.read_str(self.data, offset, str_len)
    elif issubclass(field_type, Enum):
      for base_class in field_type.__mro__:
        if issubclass(base_class, int) and base_class in fs.PRIMITIVE_TYPE_TO_BYTE_SIZE:
          raw_value = self.read_value(base_class, offset)
          if raw_value in field_type:
            return field_type(raw_value)
          else:
            if PRINT_INVALID_VALUE_WARNINGS:
              print(f"Invalid value for enum {field_type}: {raw_value}")
            return raw_value
      raise TypeError(f"Enum {field_type} must inherit from a primitive int subclass.")
    elif issubclass(field_type, BUNFOE):
      value = field_type(self.data)
      value.read(offset)
      return value
    else:
      raise NotImplementedError
  #endregion
  
  #region Saving
  def save(self, offset: int) -> int:
    orig_offset = offset
    bitfield = None
    bit_offset = None
    for field in fields(self):
      if field.bitfield:
        # Don't save the bitfield as soon as we see it.
        # We need to update its value with the values of each of its properties first.
        bitfield = field
        bit_offset = 0
        continue
      
      if bitfield is None:
        assert field.bits is None, "Specified the bits argument when no bitfield was active."
      else:
        if field.bits is None:
          # Reached the end of the current bitfield.
          # Save the bitfield itself now that it has its final value.
          offset = self.save_field(bitfield, offset)
          bitfield = None
          bit_offset = None
        else:
          bit_offset = self.save_bitfield_property(bitfield, field, bit_offset)
          continue
      
      offset = self.save_field(field, offset)
    
    if bitfield is not None:
      # Bitfield continued until the end of this class so it didn't get saved in the loop.
      # Save it now instead.
      offset = self.save_field(bitfield, offset)
    
    assert offset >= orig_offset
    if self.DATA_SIZE is not None:
      size_saved = offset - orig_offset
      assert size_saved == self.DATA_SIZE
    
    return offset
  
  def save_field(self, field: Field, offset: int) -> int:
    value = getattr(self, field.name)
    
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      offset = self.save_list_field(field, offset, value)
    else:
      self.save_value(field.type, offset, value)
      offset += self.get_byte_size(field.type)
    
    return offset
  
  def save_list_field(self, field: Field, offset: int, value) -> int:
    assert len(value) == self.get_list_length(field)
    type_args = typing.get_args(field.type)
    assert len(type_args) == 1
    arg_type = type_args[0]
    
    for i in range(self.get_list_length(field)):
      self.save_value(arg_type, offset, value[i])
      offset += self.get_byte_size(arg_type)
    
    return offset
  
  def save_bitfield_property(self, bitfield: Field, field: Field, bit_offset: int):
    value = getattr(self, field.name)
    
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      bit_offset = self.save_bitfield_property_list_field(bitfield, field, bit_offset, value)
    else:
      self.save_bitfield_property_value(bitfield, field.type, bit_offset, field.bits, value)
      bit_offset += field.bits
    
    return bit_offset
  
  def save_bitfield_property_list_field(self, bitfield: Field, field: Field, bit_offset: int, value) -> int:
    assert len(value) == self.get_list_length(field)
    type_args = typing.get_args(field.type)
    assert len(type_args) == 1
    arg_type = type_args[0]
    
    for i in range(self.get_list_length(field)):
      self.save_bitfield_property_value(bitfield, arg_type, bit_offset, field.bits, value[i])
      bit_offset += field.bits
    
    return bit_offset
  
  def save_bitfield_property_value(self, bitfield: Field, field_type: Type[T], bit_offset: int, bits: int, value: T):
    total_bits = self.get_byte_size(bitfield.type)*8
    assert 0 <= bit_offset < total_bits
    assert 1 <= bits <= total_bits
    assert 1 <= bit_offset+bits <= total_bits
    
    bitfield_value = getattr(self, bitfield.name)
    bit_mask = ((1 << bits) - 1) << bit_offset
    bitfield_value &= ~bit_mask
    
    if issubclass(field_type, Enum):
      if isinstance(value, field_type):
        raw_value = value.value
      elif isinstance(value, int):
        raw_value = value
      else:
        raise TypeError(f"Invalid value {repr(value)}, expected to have type {field_type} but was {type(value)} instead.")
    elif issubclass(field_type, int) or issubclass(field_type, bool):
      raw_value = int(value) # TODO: use field_type?
    elif issubclass(field_type, float):
      raw_value = fs.bit_cast_float_to_int(value)
    else:
      raise NotImplementedError(f"Writing type {field_type} to a bitfield is not currently implemented")
    bitfield_value |= (raw_value << bit_offset) & bit_mask
    setattr(self, bitfield.name, bitfield_value)
  
  def save_value(self, field_type: Type[T], offset: int, value: T) -> None:
    # TODO: assert that value is an instance of field_type?
    if field_type in fs.PRIMITIVE_TYPE_TO_WRITE_FUNC:
      write_func = fs.PRIMITIVE_TYPE_TO_WRITE_FUNC[field_type]
      write_func(self.data, offset, value)
    elif field_type == bool:
      self.save_value(u8, offset, int(value))
    elif issubclass(field_type, MappedBool):
      if isinstance(value, bool):
        raw_value = int(value)
      elif isinstance(value, MappedBool):
        raw_value = value.raw_value
      else:
        raise Exception(f"Invalid MappedBool: {value!r}")
      self.save_value(u8, offset, raw_value)
    elif issubclass(field_type, u16Rot):
      self.save_value(u16, offset, value)
    elif isinstance(field_type, GenericAlias) and field_type.__origin__ == FixedStr:
      str_len = typing.get_args(field_type)[0]
      fs.write_str(self.data, offset, value, str_len)
    elif isinstance(field_type, GenericAlias) and field_type.__origin__ == MagicStr:
      str_len = typing.get_args(field_type)[0]
      fs.write_magic_str(self.data, offset, value, str_len)
    elif issubclass(field_type, Enum):
      for base_class in field_type.__mro__:
        if issubclass(base_class, int) and base_class in fs.PRIMITIVE_TYPE_TO_BYTE_SIZE:
          if isinstance(value, field_type):
            raw_value = value.value
          elif isinstance(value, int):
            raw_value = value
          else:
            raise TypeError(f"Invalid value {repr(value)}, expected to have type {field_type} but was {type(value)} instead.")
          self.save_value(base_class, offset, raw_value)
          return
      raise TypeError(f"Enum {field_type} must inherit from a primitive int subclass.")
    elif issubclass(field_type, BUNFOE):
      value.save(offset)
    else:
      raise NotImplementedError
  #endregion

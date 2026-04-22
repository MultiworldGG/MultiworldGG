from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.jchunk import JChunk
from gclib.bunfoe import bunfoe, field, BUNFOE
from gclib.bunfoe_types import Vec3float

class ShapeMatrixType(u8, Enum):
  Single_Matrix = 0x00
  Billboard     = 0x01
  Y_Billboard   = 0x02
  Multi_Matrix  = 0x03

@bunfoe
class Shape(BUNFOE):
  DATA_SIZE = 0x28
  
  matrix_type             : ShapeMatrixType = ShapeMatrixType.Single_Matrix
  _padding_1              : u8 = 0xFF
  matrix_group_count      : u16
  first_attribute_offset  : u16
  first_matrix_data_index : u16
  first_matrix_group_index: u16
  _padding_2              : u16 = 0xFFFF
  bounding_sphere_radius  : float
  bounding_box_min        : Vec3float
  bounding_box_max        : Vec3float

class SHP1(JChunk):
  def read_chunk_specific_data(self):
    self.shape_count = fs.read_u16(self.data, 0x08)
    self.shape_data_offset = fs.read_u32(self.data, 0x0C)
    self.name_table_offset = fs.read_u32(self.data, 0x14)
    self.attribute_table_offset = fs.read_u32(self.data, 0x18)
    self.matrix_table_offset = fs.read_u32(self.data, 0x1C)
    self.primitive_data_offset = fs.read_u32(self.data, 0x20)
    self.mtx_group_table_offset = fs.read_u32(self.data, 0x28)
    
    self.shape_names = self.read_string_table(self.name_table_offset)
    self.shapes = []
    shape_offset = self.shape_data_offset
    for shape_index in range(self.shape_count):
      shape = Shape(self.data)
      shape.read(shape_offset)
      self.shapes.append(shape)
      shape_offset += Shape.DATA_SIZE
  
  def save_chunk_specific_data(self):
    shape_offset = self.shape_data_offset
    for shape in self.shapes:
      shape.save(shape_offset)
      shape_offset += Shape.DATA_SIZE

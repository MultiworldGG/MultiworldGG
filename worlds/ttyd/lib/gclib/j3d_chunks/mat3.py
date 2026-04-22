import typing
from types import GenericAlias
from typing import Type, Any
from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import BUNFOE, Field, bunfoe, field, fields
from gclib.bunfoe_types import Vec2float, Vec3float, Matrix2x3, Matrix4x4, RGBAu8, RGBAs16
from gclib.jchunk import JChunk
import gclib.gx_enums as GX

@bunfoe
class ZMode(BUNFOE):
  depth_test : bool           = True
  depth_func : GX.CompareType = GX.CompareType.Less_Equal
  depth_write: bool           = True
  _padding_1 : u8             = 0xFF

@bunfoe
class ColorChannel(BUNFOE):
  lighting_enabled    : bool                   = True
  mat_color_src       : GX.ColorSrc            = GX.ColorSrc.Register
  lit_mask            : u8                     = field(bitfield=True, init=False)
  used_lights         : list[bool]             = field(bits=1, length=8, default_factory=lambda: [True]*8)
  diffuse_function    : GX.DiffuseFunction     = GX.DiffuseFunction.Clamp
  attenuation_function: GX.AttenuationFunction = GX.AttenuationFunction.Spot
  ambient_color_src   : GX.ColorSrc            = GX.ColorSrc.Register
  _padding            : u16                    = 0xFFFF

@bunfoe
class AlphaCompare(BUNFOE):
  comp0    : GX.CompareType = GX.CompareType.Greater_Equal
  ref0     : u8             = 128
  operation: GX.AlphaOp     = GX.AlphaOp.AND
  comp1    : GX.CompareType = GX.CompareType.Less_Equal
  ref1     : u8             = 255
  _padding : u24            = 0xFFFFFF

@bunfoe
class BlendMode(BUNFOE):
  mode              : GX.BlendMode
  source_factor     : GX.BlendFactor
  destination_factor: GX.BlendFactor
  logic_op          : GX.LogicOp

@bunfoe
class TevOrder(BUNFOE):
  tex_coord_id: GX.TexCoordID
  tex_map_id  : GX.TexMapID
  channel_id  : GX.ColorChannelID
  _padding    : u8 = 0xFF

@bunfoe
class TevStage(BUNFOE):
  tev_mode    : u8
  color_in_a  : GX.CombineColor
  color_in_b  : GX.CombineColor
  color_in_c  : GX.CombineColor
  color_in_d  : GX.CombineColor
  color_op    : GX.TevOp
  color_bias  : GX.TevBias
  color_scale : GX.TevScale
  color_clamp : bool
  color_reg_id: GX.Register
  alpha_in_a  : GX.CombineAlpha
  alpha_in_b  : GX.CombineAlpha
  alpha_in_c  : GX.CombineAlpha
  alpha_in_d  : GX.CombineAlpha
  alpha_op    : GX.TevOp
  alpha_bias  : GX.TevBias
  alpha_scale : GX.TevScale
  alpha_clamp : bool
  alpha_reg_id: GX.Register
  _padding_1  : u8

@bunfoe
class TexCoord(BUNFOE):
  type_           : GX.TexGenType
  source          : GX.TexGenSrc
  tex_gen_matrix  : GX.TexGenMatrix
  _padding_1      : u8 = 0xFF

class TexMtxProjection(u8, Enum):
  MTX3x4 = 0x00
  MTX2x4 = 0x01

class TexMtxMapMode(u8, Enum):
  None_              = 0x00
  EnvmapBasic        = 0x01
  ProjmapBasic       = 0x02
  ViewProjmapBasic   = 0x03
  UNKNOWN_04         = 0x04
  UNKNOWN_05         = 0x05
  EnvmapOld          = 0x06
  Envmap             = 0x07
  Projmap            = 0x08
  ViewProjmap        = 0x09
  EnvmapOldEffectMtx = 0x0A
  EnvmapEffectMtx    = 0x0B

@bunfoe
class TexMatrix(BUNFOE):
  DATA_SIZE = 0x64
  
  projection   : TexMtxProjection = TexMtxProjection.MTX2x4
  bitfield_1   : u8               = field(bitfield=True)
  map_mode     : TexMtxMapMode    = field(bits=6, default=TexMtxMapMode.None_)
  unknown_1    : bool             = field(bits=1, default=False, assert_default=True)
  is_maya      : bool             = field(bits=1, default=False)
  _padding_1   : u16              = 0xFFFF
  center       : Vec3float        = field(default_factory=lambda: Vec3float(x=0.5, y=0.5, z=0.5))
  scale        : Vec2float        = field(default_factory=lambda: Vec2float(x=1.0, y=1.0))
  rotation     : u16Rot           = 0
  _padding_2   : u16              = 0xFFFF
  translation  : Vec2float        = field(default_factory=Vec2float)
  effect_matrix: Matrix4x4        = field(default_factory=Matrix4x4)

@bunfoe
class TevSwapMode(BUNFOE):
  ras_sel   : u8
  tex_sel   : u8
  _padding_1: u16

@bunfoe
class TevSwapModeTable(BUNFOE):
  r: u8
  g: u8
  b: u8
  a: u8

@bunfoe
class FogInfo(BUNFOE):
  DATA_SIZE = 0x2C
  
  fog_type         : GX.FogType
  # TODO: fog_type & 0x08 may be projection? need to find an example of orthographic fog...
  enable           : bool
  center           : u16
  start_z          : float
  end_z            : float
  near_z           : float
  far_z            : float
  color            : RGBAu8
  range_adjustments: list[u16] = field(length=10)

@bunfoe
class NBTScale(BUNFOE):
  enable  : bool
  _padding: u24 = 0xFFFFFF
  scale   : Vec3float

@bunfoe
class Material(BUNFOE):
  DATA_SIZE = 0x14C
  
  mat3: 'MAT3' = field(default=None, repr=False, compare=False, kw_only=False, ignore=True)
  tex_indirect: 'TextureIndirect' = field(default=None, repr=False, compare=False, kw_only=False, ignore=True)
  
  pixel_engine_mode   : GX.PixelEngineMode     = GX.PixelEngineMode.Opaque
  cull_mode           : GX.CullMode            = field(metadata={'indexed_by': (u8,  'cull_mode_list_offset')})
  num_color_chans     : u8                     = field(metadata={'indexed_by': (u8,  'num_color_chans_list_offset')})
  num_tex_gens        : u8                     = field(metadata={'indexed_by': (u8,  'num_tex_gens_list_offset')})
  num_tev_stages      : u8                     = field(metadata={'indexed_by': (u8,  'num_tev_stages_list_offset')})
  z_compare           : bool                   = field(metadata={'indexed_by': (u8,  'z_compare_list_offset')})
  z_mode              : ZMode                  = field(metadata={'indexed_by': (u8,  'z_mode_list_offset')})
  dither              : bool                   = field(metadata={'indexed_by': (u8,  'dither_list_offset')})
  material_colors     : list[RGBAu8]           = field(metadata={'indexed_by': (u16, 'mat_color_list_offset')}, length=2)
  color_channels      : list[ColorChannel]     = field(metadata={'indexed_by': (u16, 'color_channel_list_offset')}, length=4)
  ambient_colors      : list[RGBAu8]           = field(metadata={'indexed_by': (u16, 'ambient_color_list_offset')}, length=2)
  light_colors        : list[RGBAu8]           = field(metadata={'indexed_by': (u16, 'light_color_list_offset')}, length=8)
  tex_coord_gens      : list[TexCoord]         = field(metadata={'indexed_by': (u16, 'tex_coord_gen_list_offset')}, length=8)
  post_tex_coord_gens : list[TexCoord]         = field(metadata={'indexed_by': (u16, 'post_tex_coord_gen_list_offset')}, length=8)
  tex_matrixes        : list[TexMatrix]        = field(metadata={'indexed_by': (u16, 'tex_matrix_list_offset')}, length=10)
  post_tex_matrixes   : list[TexMatrix]        = field(metadata={'indexed_by': (u16, 'post_tex_matrix_list_offset')}, length=20)
  textures            : list[u16]              = field(metadata={'indexed_by': (u16, 'texture_remap_table_offset')}, length=8)
  tev_konst_colors    : list[RGBAu8]           = field(metadata={'indexed_by': (u16, 'tev_konst_color_list_offset')}, length=4)
  tev_konst_color_sels: list[GX.KonstColorSel] = field(length=16)
  tev_konst_alpha_sels: list[GX.KonstAlphaSel] = field(length=16)
  tev_orders          : list[TevOrder]         = field(metadata={'indexed_by': (u16, 'tev_order_list_offset')}, length=16)
  tev_colors          : list[RGBAs16]          = field(metadata={'indexed_by': (u16, 'tev_color_list_offset')}, length=4)
  tev_stages          : list[TevStage]         = field(metadata={'indexed_by': (u16, 'tev_stage_list_offset')}, length=16)
  tev_swap_modes      : list[TevSwapMode]      = field(metadata={'indexed_by': (u16, 'tev_swap_mode_list_offset')}, length=16)
  tev_swap_mode_tables: list[TevSwapModeTable] = field(metadata={'indexed_by': (u16, 'tev_swap_mode_table_list_offset')}, length=16)
  fog_info            : FogInfo                = field(metadata={'indexed_by': (u16, 'fog_list_offset')})
  alpha_compare       : AlphaCompare           = field(metadata={'indexed_by': (u16, 'alpha_compare_list_offset')})
  blend_mode          : BlendMode              = field(metadata={'indexed_by': (u16, 'blend_mode_list_offset')})
  nbt_scale           : NBTScale               = field(metadata={'indexed_by': (u16, 'nbt_scale_list_offset')})
  
  def read_field(self, field: Field, offset: int) -> int:
    if 'indexed_by' not in field.metadata:
      return super().read_field(field, offset)
    
    index_type, list_attr_name = field.metadata['indexed_by']
    
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      max_index_to_read = None
      if list_attr_name == 'tev_swap_mode_table_list_offset' and any(self.tev_swap_modes):
        # These indexes are themselves indexed by the ras/tex sels of tev_swap_mode_list_offset.
        # The problem is that if we just read all of these indexes, the later ones that aren't
        # actually used frequently have junk data for indexes, which would result in us reading out
        # of bounds. So we have to ensure we *only* read the valid indexes that are used.
        max_index_to_read = max(
          max(sm.ras_sel, sm.tex_sel)
          for sm in self.tev_swap_modes
          if sm is not None
        )
      
      assert isinstance(field.length, int) and field.length > 0
      type_args = typing.get_args(field.type)
      assert len(type_args) == 1
      arg_type = type_args[0]
      value = []
      for i in range(field.length):
        if max_index_to_read is not None and i > max_index_to_read:
          offset += self.get_byte_size(index_type)
          value.append(None)
          continue
        element, offset = self.read_indexed_value(arg_type, offset, index_type, list_attr_name)
        value.append(element)
    else:
      value, offset = self.read_indexed_value(field.type, offset, index_type, list_attr_name)
    
    setattr(self, field.name, value)
    return offset
  
  def read_indexed_value(self, value_type: Type, offset: int, index_type: Type, list_attr_name: str) -> tuple[Any, int]:
    index = self.read_value(index_type, offset)
    offset += self.get_byte_size(index_type)
    
    assert index_type in fs.PRIMITIVE_TYPE_IS_SIGNED and not fs.PRIMITIVE_TYPE_IS_SIGNED[index_type]
    max_val = (1 << self.get_byte_size(index_type)*8) - 1
    if index == max_val:
      return None, offset
    
    value = self.mat3.read_indexed_value(value_type, list_attr_name, index)
    
    return value, offset
  
  def save_field(self, field: Field, offset: int) -> int:
    if 'indexed_by' not in field.metadata:
      return super().save_field(field, offset)
    
    value = getattr(self, field.name)
    
    index_type, list_attr_name = field.metadata['indexed_by']
    
    if isinstance(field.type, GenericAlias) and field.type.__origin__ == list:
      assert isinstance(field.length, int) and field.length > 0
      assert len(value) == field.length
      type_args = typing.get_args(field.type)
      assert len(type_args) == 1
      arg_type = type_args[0]
      for i in range(field.length):
        offset = self.save_indexed_value(arg_type, offset, value[i], index_type, list_attr_name)
    else:
      offset = self.save_indexed_value(field.type, offset, value, index_type, list_attr_name)
    
    return offset
  
  def save_indexed_value(self, value_type: Type, offset: int, value: Any, index_type: Type, list_attr_name: str) -> int:
    # if value == -1 and not fs.PRIMITIVE_TYPE_IS_SIGNED[index_type]:
    if value is None:
      max_val = (1 << self.get_byte_size(index_type)*8) - 1
      index = max_val
    else:
      index = self.mat3.queue_indexed_value_write(value, value_type, list_attr_name)
    self.save_value(index_type, offset, index)
    offset += self.get_byte_size(index_type)
    
    return offset

@bunfoe
class IndirectTevOrder(BUNFOE): 
  tex_coord_id: GX.TexCoordID = GX.TexCoordID.TEXCOORD_NULL
  tex_map_id  : GX.TexMapID   = GX.TexMapID.TEXMAP_NULL
  _padding_1  : u16           = 0xFFFF

@bunfoe
class IndirectTexMatrix(BUNFOE):
  matrix        : Matrix2x3 = field(default_factory=Matrix2x3)
  scale_exponent: s8        = 1
  _padding      : u24       = 0xFFFFFF

@bunfoe
class IndirectTexScale(BUNFOE):
  scale_s : GX.IndirectTexScale = GX.IndirectTexScale._1
  scale_t : GX.IndirectTexScale = GX.IndirectTexScale._1
  _padding: u16                 = 0xFFFF

@bunfoe
class IndirectTevStage(BUNFOE):
  tev_stage: GX.IndTexStageID
  format   : GX.IndTexFormat
  bias_sel : GX.IndTexBiasSel
  mtx_sel  : GX.IndTexMtxSel
  wrap_s   : GX.IndTexWrap
  wrap_t   : GX.IndTexWrap
  add_prev : bool
  utc_lod  : bool
  alpha_sel: GX.IndTexAlphaSel
  _padding : u24 = 0xFFFFFF

@bunfoe
class TextureIndirect(BUNFOE):
  DATA_SIZE = 0x138
  
  enable            : bool
  num_ind_tex_stages: u8
  _padding_1        : u16 = 0xFFFF
  tev_orders        : list[IndirectTevOrder]  = field(length=4)
  tex_matrixes      : list[IndirectTexMatrix] = field(length=3)
  scales            : list[IndirectTexScale]  = field(length=4)
  tev_stages        : list[IndirectTevStage]  = field(length=16)

@bunfoe
class MAT3(JChunk):
  material_count                 : u16
  _padding_1                     : u16 = 0xFFFF
  material_data_offset           : u32
  material_remap_table_offset    : u32
  mat_names_table_offset         : u32
  indirect_list_offset           : u32
  cull_mode_list_offset          : u32
  mat_color_list_offset          : u32
  num_color_chans_list_offset    : u32
  color_channel_list_offset      : u32
  ambient_color_list_offset      : u32
  light_color_list_offset        : u32
  num_tex_gens_list_offset       : u32
  tex_coord_gen_list_offset      : u32
  post_tex_coord_gen_list_offset : u32
  tex_matrix_list_offset         : u32
  post_tex_matrix_list_offset    : u32
  texture_remap_table_offset     : u32
  tev_order_list_offset          : u32
  tev_color_list_offset          : u32
  tev_konst_color_list_offset    : u32
  num_tev_stages_list_offset     : u32
  tev_stage_list_offset          : u32
  tev_swap_mode_list_offset      : u32
  tev_swap_mode_table_list_offset: u32
  fog_list_offset                : u32
  alpha_compare_list_offset      : u32
  blend_mode_list_offset         : u32
  z_mode_list_offset             : u32
  z_compare_list_offset          : u32
  dither_list_offset             : u32
  nbt_scale_list_offset          : u32
  
  def __post_init__(self):
    super().__post_init__()
    
    self.queued_values_to_write: dict[str, list] = {}
    self.queued_list_data_types: dict[str, type] = {}
  
  def read_chunk_specific_data(self):
    BUNFOE.read(self, 0)
    
    self.materials: list[Material] = []
    for mat_index in range(self.material_count):
      remap_index = fs.read_u16(self.data, self.material_remap_table_offset + mat_index*2)
      offset = self.material_data_offset + remap_index*Material.DATA_SIZE
      mat = Material(self.data, self)
      mat.read(offset)
      self.materials.append(mat)
  
    self.mat_names = self.read_string_table(self.mat_names_table_offset)
    
    self.indirects: list[TextureIndirect] = []
    indirect_offset = self.indirect_list_offset
    if indirect_offset != self.mat_names_table_offset:
      for mat_index in range(self.material_count):
        indirect = TextureIndirect(self.data)
        indirect.read(indirect_offset)
        self.indirects.append(indirect)
        indirect_offset += TextureIndirect.DATA_SIZE
        self.materials[mat_index].tex_indirect = indirect
  
  def read_indexed_value(self, value_type: Type, list_attr_name: str, index: int) -> Any:
    list_offset = getattr(self, list_attr_name)
    assert isinstance(list_offset, int)
    if list_offset == 0:
      # Sometimes the material's index can be valid, but the MAT3's list is nonexistent.
      # e.g. cc.bmd's first material has one post tex matrix with index 0, but the list offset is 0.
      return None
    value_offset = list_offset + index*self.get_byte_size(value_type)
    value = self.read_value(value_type, value_offset)
    return value
  
  def queue_indexed_value_write(self, value, data_type: type, list_attr_name: str) -> int:
    if list_attr_name not in self.queued_values_to_write:
      self.queued_values_to_write[list_attr_name] = []
      self.queued_list_data_types[list_attr_name] = data_type
    if value not in self.queued_values_to_write[list_attr_name]:
      self.queued_values_to_write[list_attr_name].append(value)
    return self.queued_values_to_write[list_attr_name].index(value)
  
  def save_chunk_specific_data(self):
    # Cut off all the data, we're rewriting it entirely.
    self.data.truncate(0)
    
    # De-duplicate the materials.
    self.material_count = len(self.materials)
    unique_materials: list[Material] = []
    # seen_materials = set()
    remap_indexes: list[int] = []
    for mat in self.materials:
      if mat not in unique_materials:
        unique_materials.append(mat)
      remap_index = unique_materials.index(mat)
      remap_indexes.append(remap_index)
    
    # # Print which materials are duplicates of one another (for debugging).
    # for mat in unique_materials:
    #   mat_indexes = [i for i, other in enumerate(self.materials) if other == mat]
    #   print(", ".join(self.mat_names[i] for i in mat_indexes))
    
    # Clear out the queues from any previous saves.
    self.queued_values_to_write.clear()
    self.queued_list_data_types.clear()
    # For some reason, certain lists always seem to have certain values in them, even if those values are not used by
    # any materials in this model.
    # While these should not have any practical effect, we write them anyway so that resaving the model with no changes
    # does not change its bytes in any way.
    self.queue_indexed_value_write(GX.CullMode.Cull_Back, GX.CullMode, 'cull_mode_list_offset')
    self.queue_indexed_value_write(GX.CullMode.Cull_Front, GX.CullMode, 'cull_mode_list_offset')
    self.queue_indexed_value_write(GX.CullMode.Cull_None, GX.CullMode, 'cull_mode_list_offset')
    self.queue_indexed_value_write(False, bool, 'z_compare_list_offset')
    self.queue_indexed_value_write(True, bool, 'z_compare_list_offset')
    self.queue_indexed_value_write(False, bool, 'dither_list_offset')
    self.queue_indexed_value_write(True, bool, 'dither_list_offset')
    
    # Write the unique materials to material_data_offset.
    # The materials will call MAT3.queue_indexed_value_write to queue a value to write to the MAT3
    # chunk and get their value indexes in return, allowing the materials to be written now, without
    # waiting for the data that comes after them to be written.
    offset = self.material_data_offset # This offset is constant, always 0x84.
    for mat in unique_materials:
      offset = mat.save(offset)
    
    # Write the material remap table.
    self.material_remap_table_offset = offset
    for remap_index in remap_indexes:
      fs.write_u16(self.data, offset, remap_index)
      offset += 2
    
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    # Write the material names.
    self.mat_names_table_offset = offset
    offset = self.write_string_table(self.mat_names_table_offset, self.mat_names)
    offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    if len(self.indirects) == 0:
      self.indirect_list_offset = self.mat_names_table_offset
    else:
      assert len(self.indirects) == len(self.materials)
      self.indirect_list_offset = offset
      for indirect in self.indirects:
        indirect.save(offset)
        offset += TextureIndirect.DATA_SIZE
      offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    # First clear all of these fields to be safe so we don't accidentally write stale data.
    for field in fields(self):
      if field.name == "indirect_list_offset":
        continue
      if field.name.endswith("_list_offset") or field.name == "texture_remap_table_offset":
        setattr(self, field.name, None)
    
    # Now we can write the material values that were queued for writing earlier.
    # for list_attr_name, values in self.queued_values_to_write.items():
    for field in fields(self):
      if getattr(self, field.name) is None:
        self.set_dummy_blank_list_offset(field.name, offset)
      if field.name not in self.queued_values_to_write:
        continue
      list_attr_name = field.name
      values = self.queued_values_to_write[list_attr_name]
      
      if len(values) == 0:
        self.set_dummy_blank_list_offset(field.name, offset)
        continue
      
      # Also recalculate the offset so this can be stored in the header at the end.
      setattr(self, list_attr_name, offset)
      
      data_type = self.queued_list_data_types[list_attr_name]
      for value in values:
        self.save_value(data_type, offset, value)
        offset += self.get_byte_size(data_type)
      
      offset = fs.align_data_and_pad_offset(self.data, offset, 4)
    
    # Finally, save the new offsets to each list back to the header.
    BUNFOE.save(self, 0)
  
  def set_dummy_blank_list_offset(self, list_attr_name, offset):
    # TODO: in some cases it writes the offset of the next list, while in others just 0.
    # I'm not sure how to tell the difference, look into this more.
    # num_tex_gens_list_offset: copies offset of next list.
    # post_tex_coord_gen_list_offset: writes 0.
    # post_tex_matrix_list_offset: writes 0.
    # light_colors: copies offset of next list.
    if list_attr_name in ['post_tex_coord_gen_list_offset', 'post_tex_matrix_list_offset']:
      dummy_offset = 0
    else:
      dummy_offset = offset
    
    setattr(self, list_attr_name, dummy_offset)

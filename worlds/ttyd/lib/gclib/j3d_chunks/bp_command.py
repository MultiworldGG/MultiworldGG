from typing import ClassVar
from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import BUNFOE, bunfoe, field, InitVar
from gclib.j3d_chunks.mdl_command import MDLCommand
import gclib.gx_enums as GX
from gclib.gx_enums import MDLCommandType, BPRegister
from gclib.texture_utils import ImageFormat, PaletteFormat

@bunfoe
class BPCommand(MDLCommand):
  cmd_type: MDLCommandType = field(default=MDLCommandType.BP, assert_default=True) # TODO hide from GUI
  register: BPRegister # TODO read only # TODO hide from gui
  reg_index: InitVar[int | None] = None
  bitfield: u24 = field(bitfield=True)
  
  DATA_SIZE = 5
  VALID_REGISTERS: ClassVar[list[BPRegister]] = []
  
  def assert_valid(self):
    assert self.cmd_type == MDLCommandType.BP
    if self.__class__ is not BPCommand:
      assert self.register in self.VALID_REGISTERS
  
  def __post_init__(self, reg_index=None):
    super().__post_init__()
    if reg_index is not None:
      if not self.VALID_REGISTERS:
        raise ValueError("Specified register index for a command class that doesn't have any valid registers.")
      if reg_index < 0 or reg_index >= len(self.VALID_REGISTERS):
        raise ValueError(f"Specified register index is out of range (max {len(self.VALID_REGISTERS)-1}).")
      self.register = self.VALID_REGISTERS[reg_index]

@bunfoe
class TX_SETIMAGE0(BPCommand):
  width_minus_1 : u16         = field(bits=10)
  height_minus_1: u16         = field(bits=10)
  format        : ImageFormat = field(bits=4)
  
  VALID_REGISTERS = [
    BPRegister.TX_SETIMAGE0_I0, BPRegister.TX_SETIMAGE0_I1, BPRegister.TX_SETIMAGE0_I2, BPRegister.TX_SETIMAGE0_I3,
    BPRegister.TX_SETIMAGE0_I4, BPRegister.TX_SETIMAGE0_I5, BPRegister.TX_SETIMAGE0_I6, BPRegister.TX_SETIMAGE0_I7,
  ]

@bunfoe
class TX_SETIMAGE3(BPCommand):
  texture_index: u24 = field(bits=24)
  
  VALID_REGISTERS = [
    BPRegister.TX_SETIMAGE3_I0, BPRegister.TX_SETIMAGE3_I1, BPRegister.TX_SETIMAGE3_I2, BPRegister.TX_SETIMAGE3_I3,
    BPRegister.TX_SETIMAGE3_I4, BPRegister.TX_SETIMAGE3_I5, BPRegister.TX_SETIMAGE3_I6, BPRegister.TX_SETIMAGE3_I7,
  ]

# For some reason, TX_SETMODE0's min filter doesn't match GX.FilterMode?
class MDLFilterMode(Enum):
  Nearest              = 0
  Linear               = 4
  NearestMipmapNearest = 1
  NearestMipmapLinear  = 5
  LinearMipmapNearest  = 2
  LinearMipmapLinear   = 6

@bunfoe
class TX_SETMODE0(BPCommand):
  wrap_s    : GX.WrapMode   = field(bits=2)
  wrap_t    : GX.WrapMode   = field(bits=2)
  mag_filter: GX.FilterMode = field(bits=1)
  min_filter: MDLFilterMode = field(bits=3)
  diag_lod  : bool          = field(bits=1)
  lod_bias  : u8            = field(bits=8)
  unknown   : u8            = field(bits=2, default=0, assert_default=True)
  max_aniso : u8            = field(bits=2)
  lod_clamp : bool          = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.TX_SETMODE0_I0, BPRegister.TX_SETMODE0_I1, BPRegister.TX_SETMODE0_I2, BPRegister.TX_SETMODE0_I3,
    BPRegister.TX_SETMODE0_I4, BPRegister.TX_SETMODE0_I5, BPRegister.TX_SETMODE0_I6, BPRegister.TX_SETMODE0_I7,
  ]

@bunfoe
class TX_SETMODE1(BPCommand):
  min_lod: u8 = field(bits=8)
  max_lod: u8 = field(bits=8)
  
  VALID_REGISTERS = [
    BPRegister.TX_SETMODE1_I0, BPRegister.TX_SETMODE1_I1, BPRegister.TX_SETMODE1_I2, BPRegister.TX_SETMODE1_I3,
    BPRegister.TX_SETMODE1_I4, BPRegister.TX_SETMODE1_I5, BPRegister.TX_SETMODE1_I6, BPRegister.TX_SETMODE1_I7,
  ]

@bunfoe
class BP_MASK(BPCommand):
  mask: u24 = field(bits=24)
  
  VALID_REGISTERS = [
    BPRegister.BP_MASK,
  ]

@bunfoe
class TEX_LOADTLUT0(BPCommand):
  src: u24 = field(bits=24)
  
  VALID_REGISTERS = [
    BPRegister.TEX_LOADTLUT0,
  ]

@bunfoe
class TEX_LOADTLUT1(BPCommand):
  tmem_addr      : u16 = field(bits=10)
  tmem_line_count: u16 = field(bits=11)
  unknown        : u8  = field(bits=3, default=0, assert_default=True)
  
  VALID_REGISTERS = [
    BPRegister.TEX_LOADTLUT1,
  ]

@bunfoe
class TX_LOADTLUT(BPCommand):
  tmem_offset: u16           = field(bits=10)
  format     : PaletteFormat = field(bits=2)
  unknown    : u16           = field(bits=12, default=0, assert_default=True)
  
  VALID_REGISTERS = [
    BPRegister.TX_LOADTLUT0, BPRegister.TX_LOADTLUT1, BPRegister.TX_LOADTLUT2, BPRegister.TX_LOADTLUT3,
  ]

@bunfoe
class SU_SSIZE(BPCommand):
  width_minus_1: u16 = field(bits=16)
  unknown      : u8  = field(bits=1, default=0, assert_default=True)
  # TODO:
  # bias: 1 bit
  # wrap: 1 bit?
  
  VALID_REGISTERS = [
    BPRegister.SU_SSIZE0, BPRegister.SU_SSIZE1, BPRegister.SU_SSIZE2, BPRegister.SU_SSIZE3,
    BPRegister.SU_SSIZE4, BPRegister.SU_SSIZE5, BPRegister.SU_SSIZE6, BPRegister.SU_SSIZE7,
  ]

@bunfoe
class SU_TSIZE(BPCommand):
  height_minus_1: u16 = field(bits=16)
  unknown       : u8  = field(bits=1, default=0, assert_default=True)
  # TODO:
  # bias: 1 bit
  # wrap: 1 bit?
  
  VALID_REGISTERS = [
    BPRegister.SU_TSIZE0, BPRegister.SU_TSIZE1, BPRegister.SU_TSIZE2, BPRegister.SU_TSIZE3,
    BPRegister.SU_TSIZE4, BPRegister.SU_TSIZE5, BPRegister.SU_TSIZE6, BPRegister.SU_TSIZE7,
  ]

@bunfoe
class TEV_REGISTERL(BPCommand):
  r       : u16  = field(bits=11)
  unknown : bool = field(bits=1, default=False, assert_default=True)
  a       : u16  = field(bits=11)
  is_konst: bool = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.TEV_REGISTERL_0, BPRegister.TEV_REGISTERL_1, BPRegister.TEV_REGISTERL_2, BPRegister.TEV_REGISTERL_3,
  ]

@bunfoe
class TEV_REGISTERH(BPCommand):
  b       : u16  = field(bits=11)
  unknown : bool = field(bits=1, default=False, assert_default=True)
  g       : u16  = field(bits=11)
  is_konst: bool = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.TEV_REGISTERH_0, BPRegister.TEV_REGISTERH_1, BPRegister.TEV_REGISTERH_2, BPRegister.TEV_REGISTERH_3,
  ]

class MDLColorChannelID(u8, Enum):
  COLOR0       = 0x00
  COLOR1       = 0x01
  ALPHA0       = 0x00
  ALPHA1       = 0x01
  COLOR0A0     = 0x00
  COLOR1A1     = 0x01
  COLOR_ZERO   = 0x07
  ALPHA_BUMP   = 0x05
  ALPHA_BUMP_N = 0x06
  COLOR_NULL   = 0x07

@bunfoe
class RAS1_TREF(BPCommand):
  tex_map_0   : GX.TexMapID       = field(bits=3, default=GX.TexMapID.TEXMAP0)
  tex_coord_0 : GX.TexCoordID     = field(bits=3, default=GX.TexCoordID.TEXCOORD0)
  enable_0    : bool              = field(bits=1, default=False)
  channel_id_0: MDLColorChannelID = field(bits=3, default=MDLColorChannelID(0))
  unknown_2_0 : u8                = field(bits=2, default=0, assert_default=True)
  tex_map_1   : GX.TexMapID       = field(bits=3, default=GX.TexMapID.TEXMAP0)
  tex_coord_1 : GX.TexCoordID     = field(bits=3, default=GX.TexCoordID.TEXCOORD0)
  enable_1    : bool              = field(bits=1, default=False)
  channel_id_1: MDLColorChannelID = field(bits=3, default=MDLColorChannelID(0))
  unknown_2_1 : u8                = field(bits=2, default=0, assert_default=True)
  
  VALID_REGISTERS = [
    BPRegister.RAS1_TREF0, BPRegister.RAS1_TREF1, BPRegister.RAS1_TREF2, BPRegister.RAS1_TREF3,
    BPRegister.RAS1_TREF4, BPRegister.RAS1_TREF5, BPRegister.RAS1_TREF6, BPRegister.RAS1_TREF7,
  ]

# @bunfoe
# class RAS1_IREF_TevOrder(BUNFOE):
#   tex_coord_id: GX.TexCoordID = field(bits=3)
#   tex_map_id  : GX.TexMapID   = field(bits=3)

@bunfoe
class RAS1_IREF(BPCommand):
  # TODO: this should be an array once BUNFOE supports arrays of objects in bitfields
  # tev_orders: list[RAS1_IREF_TevOrder] = field(length=4)
  
  tex_coord_id_0: GX.TexCoordID = field(bits=3)
  tex_map_id_0  : GX.TexMapID   = field(bits=3)
  tex_coord_id_1: GX.TexCoordID = field(bits=3)
  tex_map_id_1  : GX.TexMapID   = field(bits=3)
  tex_coord_id_2: GX.TexCoordID = field(bits=3)
  tex_map_id_2  : GX.TexMapID   = field(bits=3)
  tex_coord_id_3: GX.TexCoordID = field(bits=3)
  tex_map_id_3  : GX.TexMapID   = field(bits=3)
  
  VALID_REGISTERS = [
    BPRegister.RAS1_IREF,
  ]

@bunfoe
class IND_IMASK(BPCommand):
  mask: u8 = field(bits=8)
  
  VALID_REGISTERS = [
    BPRegister.IND_IMASK,
  ]

@bunfoe
class RAS1_SS0(BPCommand):
  scale_s_0 : GX.IndirectTexScale = field(bits=4, default=GX.IndirectTexScale._1)
  scale_t_0 : GX.IndirectTexScale = field(bits=4, default=GX.IndirectTexScale._1)
  scale_s_1 : GX.IndirectTexScale = field(bits=4, default=GX.IndirectTexScale._1)
  scale_t_1 : GX.IndirectTexScale = field(bits=4, default=GX.IndirectTexScale._1)

  VALID_REGISTERS = [
    BPRegister.RAS1_SS0, BPRegister.RAS1_SS1,
  ]

@bunfoe
class TEV_COLOR_ENV(BPCommand):
  color_in_d  : GX.CombineColor = field(bits=4)
  color_in_c  : GX.CombineColor = field(bits=4)
  color_in_b  : GX.CombineColor = field(bits=4)
  color_in_a  : GX.CombineColor = field(bits=4)
  color_bias  : GX.TevBias      = field(bits=2)
  color_op    : GX.TevOp        = field(bits=1) # Or color_comparison, when bias is compare
  color_clamp : bool            = field(bits=1)
  color_scale : GX.TevScale     = field(bits=2) # Or color_compare_mode, when bias is compare
  color_reg_id: GX.Register     = field(bits=2)
  
  VALID_REGISTERS = [
     BPRegister.TEV_COLOR_ENV_0, BPRegister.TEV_COLOR_ENV_1, BPRegister.TEV_COLOR_ENV_2, BPRegister.TEV_COLOR_ENV_3,
     BPRegister.TEV_COLOR_ENV_4, BPRegister.TEV_COLOR_ENV_5, BPRegister.TEV_COLOR_ENV_6, BPRegister.TEV_COLOR_ENV_7,
     BPRegister.TEV_COLOR_ENV_8, BPRegister.TEV_COLOR_ENV_9, BPRegister.TEV_COLOR_ENV_A, BPRegister.TEV_COLOR_ENV_B,
     BPRegister.TEV_COLOR_ENV_C, BPRegister.TEV_COLOR_ENV_D, BPRegister.TEV_COLOR_ENV_E, BPRegister.TEV_COLOR_ENV_F,
  ]

@bunfoe
class TEV_ALPHA_ENV(BPCommand):
  ras_sel     : u8              = field(bits=2)
  tex_sel     : u8              = field(bits=2)
  alpha_in_d  : GX.CombineAlpha = field(bits=3)
  alpha_in_c  : GX.CombineAlpha = field(bits=3)
  alpha_in_b  : GX.CombineAlpha = field(bits=3)
  alpha_in_a  : GX.CombineAlpha = field(bits=3)
  alpha_bias  : GX.TevBias      = field(bits=2)
  alpha_op    : GX.TevOp        = field(bits=1) # Or alpha_comparison, when bias is compare
  alpha_clamp : bool            = field(bits=1)
  alpha_scale : GX.TevScale     = field(bits=2) # Or alpha_compare_mode, when bias is compare
  alpha_reg_id: GX.Register     = field(bits=2)
  
  VALID_REGISTERS = [
     BPRegister.TEV_ALPHA_ENV_0, BPRegister.TEV_ALPHA_ENV_1, BPRegister.TEV_ALPHA_ENV_2, BPRegister.TEV_ALPHA_ENV_3,
     BPRegister.TEV_ALPHA_ENV_4, BPRegister.TEV_ALPHA_ENV_5, BPRegister.TEV_ALPHA_ENV_6, BPRegister.TEV_ALPHA_ENV_7,
     BPRegister.TEV_ALPHA_ENV_8, BPRegister.TEV_ALPHA_ENV_9, BPRegister.TEV_ALPHA_ENV_A, BPRegister.TEV_ALPHA_ENV_B,
     BPRegister.TEV_ALPHA_ENV_C, BPRegister.TEV_ALPHA_ENV_D, BPRegister.TEV_ALPHA_ENV_E, BPRegister.TEV_ALPHA_ENV_F,
  ]

@bunfoe
class IND_MTXA(BPCommand):
  ma: s32 = field(bits=11)
  mb: s32 = field(bits=11)
  s0: u32 = field(bits=2)
  
  VALID_REGISTERS = [
    BPRegister.IND_MTXA0, BPRegister.IND_MTXA1, BPRegister.IND_MTXA2,
  ]

@bunfoe
class IND_MTXB(BPCommand):
  mc: s32 = field(bits=11)
  md: s32 = field(bits=11)
  s1: u32 = field(bits=2)
  
  VALID_REGISTERS = [
    BPRegister.IND_MTXB0, BPRegister.IND_MTXB1, BPRegister.IND_MTXB2,
  ]

@bunfoe
class IND_MTXC(BPCommand):
  me: s32 = field(bits=11)
  mf: s32 = field(bits=11)
  s2: u32 = field(bits=2) # Note: According to Dolphin, hardware ignores the topmost scale bit here.
  
  VALID_REGISTERS = [
    BPRegister.IND_MTXC0, BPRegister.IND_MTXC1, BPRegister.IND_MTXC2,
  ]

@bunfoe
class IND_CMD(BPCommand):
  tev_stage: GX.IndTexStageID  = field(bits=2)
  format   : GX.IndTexFormat   = field(bits=2)
  bias_sel : GX.IndTexBiasSel  = field(bits=3)
  alpha_sel: GX.IndTexAlphaSel = field(bits=2)
  mtx_sel  : GX.IndTexMtxSel   = field(bits=4)
  wrap_s   : GX.IndTexWrap     = field(bits=3)
  wrap_t   : GX.IndTexWrap     = field(bits=3)
  utc_lod  : bool              = field(bits=1)
  add_prev : bool              = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.IND_CMD0, BPRegister.IND_CMD1, BPRegister.IND_CMD2, BPRegister.IND_CMD3,
    BPRegister.IND_CMD4, BPRegister.IND_CMD5, BPRegister.IND_CMD6, BPRegister.IND_CMD7,
    BPRegister.IND_CMD8, BPRegister.IND_CMD9, BPRegister.IND_CMDA, BPRegister.IND_CMDB,
    BPRegister.IND_CMDC, BPRegister.IND_CMDD, BPRegister.IND_CMDE, BPRegister.IND_CMDF,
  ]

@bunfoe
class TEV_KSEL(BPCommand):
  r_or_b     : u8               = field(bits=2, default=0)
  g_or_a     : u8               = field(bits=2, default=0)
  color_sel_0: GX.KonstColorSel = field(bits=5)
  alpha_sel_0: GX.KonstAlphaSel = field(bits=5)
  color_sel_1: GX.KonstColorSel = field(bits=5)
  alpha_sel_1: GX.KonstAlphaSel = field(bits=5)
  
  VALID_REGISTERS = [
    BPRegister.TEV_KSEL_0, BPRegister.TEV_KSEL_1, BPRegister.TEV_KSEL_2, BPRegister.TEV_KSEL_3,
    BPRegister.TEV_KSEL_4, BPRegister.TEV_KSEL_5, BPRegister.TEV_KSEL_6, BPRegister.TEV_KSEL_7,
  ]

@bunfoe
class TEV_FOG_PARAM_0(BPCommand):
  mantissa: u16 = field(bits=11)
  exponent: u8  = field(bits=8)
  sign    : u8  = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.TEV_FOG_PARAM_0,
  ]

@bunfoe
class TEV_FOG_PARAM_1(BPCommand):
  magnitude: u24 = field(bits=24)
  
  VALID_REGISTERS = [
    BPRegister.TEV_FOG_PARAM_1,
  ]

@bunfoe
class TEV_FOG_PARAM_2(BPCommand):
  shift: u24 = field(bits=24)
  
  VALID_REGISTERS = [
    BPRegister.TEV_FOG_PARAM_2,
  ]

@bunfoe
class TEV_FOG_PARAM_3(BPCommand):
  mantissa  : u16              = field(bits=11)
  exponent  : u8               = field(bits=8)
  sign      : u8               = field(bits=1)
  projection: GX.FogProjection = field(bits=1)
  fog_type  : GX.FogType       = field(bits=3)
  
  VALID_REGISTERS = [
    BPRegister.TEV_FOG_PARAM_3,
  ]

@bunfoe
class TEV_FOG_COLOR(BPCommand):
  b: u8 = field(bits=8)
  g: u8 = field(bits=8)
  r: u8 = field(bits=8)

  VALID_REGISTERS = [
    BPRegister.TEV_FOG_COLOR,
  ]

@bunfoe
class FOG_RANGE(BPCommand):
  center : u16  = field(bits=10)
  enabled: bool = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.FOG_RANGE,
  ]

@bunfoe
class FOG_RANGE_ADJ(BPCommand):
  hi: u16 = field(bits=12)
  lo: u16 = field(bits=12)
  
  VALID_REGISTERS = [
    BPRegister.FOG_RANGE_ADJ_0, BPRegister.FOG_RANGE_ADJ_1, BPRegister.FOG_RANGE_ADJ_2,
    BPRegister.FOG_RANGE_ADJ_3, BPRegister.FOG_RANGE_ADJ_4,
  ]

@bunfoe
class TEV_ALPHAFUNC(BPCommand):
  ref0     : u8             = field(bits=8, default=128)
  ref1     : u8             = field(bits=8, default=255)
  comp0    : GX.CompareType = field(bits=3, default=GX.CompareType.Greater_Equal)
  comp1    : GX.CompareType = field(bits=3, default=GX.CompareType.Less_Equal)
  operation: GX.AlphaOp     = field(bits=2, default=GX.AlphaOp.AND)
  
  VALID_REGISTERS = [
    BPRegister.TEV_ALPHAFUNC,
  ]

@bunfoe
class PE_CMODE0(BPCommand):
  blend             : bool           = field(bits=1, default=False)
  logic             : bool           = field(bits=1, default=False)
  dither            : bool           = field(bits=1)
  unknown_1         : u8             = field(bits=2, default=0, assert_default=True)
  destination_factor: GX.BlendFactor = field(bits=3)
  source_factor     : GX.BlendFactor = field(bits=3)
  subtract          : bool           = field(bits=1, default=False)
  logic_op          : GX.LogicOp     = field(bits=4)
  unknown_2         : u8             = field(bits=8, default=0, assert_default=True)
  
  VALID_REGISTERS = [
    BPRegister.PE_CMODE0,
  ]

@bunfoe
class PE_ZMODE(BPCommand):
  depth_test : bool           = field(bits=1)
  depth_func : GX.CompareType = field(bits=3)
  depth_write: bool           = field(bits=1)
  
  VALID_REGISTERS = [
    BPRegister.PE_ZMODE,
  ]

@bunfoe
class PE_CONTROL(BPCommand):
  unknown_1: u8    = field(bits=6, default=0, assert_default=True)
  z_compare: bool  = field(bits=1)
  unknown_2: u16   = field(bits=17, default=0, assert_default=True)
  
  VALID_REGISTERS = [
    BPRegister.PE_CONTROL,
  ]

class MDLCullMode(Enum):
  Cull_None  = 0x00
  Cull_Front = 0x02
  Cull_Back  = 0x01

@bunfoe
class GEN_MODE(BPCommand):
  num_tex_gens          : u8          = field(bits=4)
  num_color_chans       : u8          = field(bits=3)
  unknown_1             : u8          = field(bits=3, default=0, assert_default=True) # upper bits of num_color_chans?
  num_tev_stages_minus_1: u8          = field(bits=4)
  cull_mode             : MDLCullMode = field(bits=2)
  num_ind_tex_stages    : u8          = field(bits=8)
  
  VALID_REGISTERS = [
    BPRegister.GEN_MODE,
  ]

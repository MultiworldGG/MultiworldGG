from typing import ClassVar
from enum import Enum

from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import BUNFOE, bunfoe, field
from gclib.bunfoe_types import RGBAu8
from gclib.j3d_chunks.mdl_command import MDLCommand
import gclib.gx_enums as GX
from gclib.gx_enums import MDLCommandType, XFRegister

@bunfoe
class XFArgument(BUNFOE):
  bitfield: u32 = field(bitfield=True)
  
  DATA_SIZE = 4

@bunfoe
class XFCommand(MDLCommand):
  cmd_type: MDLCommandType = field(default=MDLCommandType.XF, assert_default=True) # TODO hide from GUI
  num_args_minus_1: u16 = 0
  register: XFRegister # TODO read only # TODO hide from gui
  args: list[XFArgument] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)
  
  VALID_REGISTERS: ClassVar[list[XFRegister]] = []
  
  def assert_valid(self):
    assert self.cmd_type == MDLCommandType.XF
    if self.__class__ is not XFCommand:
      assert self.register in self.VALID_REGISTERS
  
  def save(self, offset: int) -> int:
    assert 1 <= len(self.args) <= 0x10000
    self.num_args_minus_1 = len(self.args)-1
    return super().save(offset)

@bunfoe
class TEXMTX_Arg(XFArgument):
  value: float = field(bits=32)

@bunfoe
class TEXMTX(XFCommand):
  args: list[TEXMTX_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)
  
  VALID_REGISTERS = [
    XFRegister.TEXMTX0, XFRegister.TEXMTX1, XFRegister.TEXMTX2, XFRegister.TEXMTX3,
    XFRegister.TEXMTX4, XFRegister.TEXMTX5, XFRegister.TEXMTX6, XFRegister.TEXMTX7,
    XFRegister.TEXMTX8, XFRegister.TEXMTX9,
  ]

class TexSize(Enum):
  ST  = 0
  STQ = 1

class TexInputForm(Enum):
  AB11 = 0
  ABC1 = 1

class TexGenType(Enum):
  Regular   = 0
  EmbossMap = 1
  Color0    = 2
  Color1    = 3

class SourceRow(Enum):
  Geom      = 0
  Normal    = 1
  Colors    = 2
  BinormalT = 3
  BinormalB = 4
  Tex0      = 5
  Tex1      = 6
  Tex2      = 7
  Tex3      = 8
  Tex4      = 9
  Tex5      = 10
  Tex6      = 11
  Tex7      = 12

@bunfoe
class TEXMTXINFO_Arg(XFArgument):
  unknown_00         : u8           = field(bits=1, default=0, assert_default=True)
  projection         : TexSize      = field(bits=1, default=TexSize.ST)
  input_form         : TexInputForm = field(bits=1, default=TexInputForm.AB11)
  unknown_03         : u8           = field(bits=1, default=0, assert_default=True)
  tex_gen_type       : TexGenType   = field(bits=3)
  source_row         : SourceRow    = field(bits=5)
  emboss_source_shift: u8           = field(bits=3, default=5)
  emboss_light_shift : u8           = field(bits=3, default=0)
  unknown_18         : u16          = field(bits=14, default=0, assert_default=True)

@bunfoe
class TEXMTXINFO(XFCommand):
  args: list[TEXMTXINFO_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)
  
  VALID_REGISTERS = [
    XFRegister.TEXMTXINFO,
  ]

@bunfoe
class POSMTXINFO_Arg(XFArgument):
  unknown_00: u8   = field(bits=6, default=61, assert_default=True)
  unknown_06: u8   = field(bits=2, default=0, assert_default=True)
  unknown_08: bool = field(bits=1, default=False, assert_default=True)
  unknown_09: u32  = field(bits=23, default=0, assert_default=True)

@bunfoe
class POSMTXINFO(XFCommand):
  args: list[POSMTXINFO_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.POSMTXINFO,
  ]

@bunfoe
class CHAN0_MATCOLOR_Arg(XFArgument):
  a: u8 = field(bits=8)
  b: u8 = field(bits=8)
  g: u8 = field(bits=8)
  r: u8 = field(bits=8)

@bunfoe
class CHAN0_MATCOLOR(XFCommand):
  args: list[CHAN0_MATCOLOR_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.CHAN0_MATCOLOR,
  ]

@bunfoe
class CHAN0_AMBCOLOR_Arg(XFArgument):
  a: u8 = field(bits=8)
  b: u8 = field(bits=8)
  g: u8 = field(bits=8)
  r: u8 = field(bits=8)

@bunfoe
class CHAN0_AMBCOLOR(XFCommand):
  args: list[CHAN0_AMBCOLOR_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.CHAN0_AMBCOLOR,
  ]

@bunfoe
class CHAN0_COLOR_Arg(XFArgument):
  mat_color_src       : GX.ColorSrc        = field(bits=1)
  lighting_enabled    : bool               = field(bits=1)
  used_lights_0123    : list[bool]         = field(bits=1, length=4, default_factory=lambda: [True]*4)
  ambient_color_src   : GX.ColorSrc        = field(bits=1)
  diffuse_function    : GX.DiffuseFunction = field(bits=2)
  attenuation_enabled : bool               = field(bits=1)
  use_spot_attenuation: bool               = field(bits=1)
  used_lights_4567    : list[bool]         = field(bits=1, length=4, default_factory=lambda: [True]*4)
  unknown_15          : u32                = field(bits=17, default=0, assert_default=True)

@bunfoe
class CHAN0_COLOR(XFCommand):
  args: list[CHAN0_COLOR_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.CHAN0_COLOR,
  ]

@bunfoe
class NUMCHAN_Arg(XFArgument):
  num_color_chans: u32 = field(bits=32)

@bunfoe
class NUMCHAN(XFCommand):
  args: list[NUMCHAN_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.NUMCHAN,
  ]

@bunfoe
class NUMTEXGENS_Arg(XFArgument):
  num_tex_gens: u32 = field(bits=32)

@bunfoe
class NUMTEXGENS(XFCommand):
  args: list[NUMTEXGENS_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.NUMTEXGENS,
  ]

@bunfoe
class LIGHT0_LPX_Arg(XFArgument):
  value: float = field(bits=32)

@bunfoe
class LIGHT0_LPX(XFCommand):
  args: list[LIGHT0_LPX_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.LIGHT0_LPX,
  ]

@bunfoe
class LIGHT0_A0_Arg(XFArgument):
  value: float = field(bits=32)

@bunfoe
class LIGHT0_A0(XFCommand):
  args: list[LIGHT0_A0_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.LIGHT0_A0,
  ]

@bunfoe
class LIGHT0_COLOR_Arg(XFArgument):
  # color: RGBAu8 = field(bits=32)
  color: u32 = field(bits=32) # TODO: should be RGBAu8, but BUNFOE doesn't support that in a bitfield yet

@bunfoe
class LIGHT0_COLOR(XFCommand):
  args: list[LIGHT0_COLOR_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.LIGHT0_COLOR,
  ]

@bunfoe
class LIGHT0_DHX_Arg(XFArgument):
  value: float = field(bits=32)

@bunfoe
class LIGHT0_DHX(XFCommand):
  args: list[LIGHT0_DHX_Arg] = field(length_calculator=lambda inst: inst.num_args_minus_1 + 1, default_factory=list)

  VALID_REGISTERS = [
    XFRegister.LIGHT0_DHX,
  ]

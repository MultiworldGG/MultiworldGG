from enum import Enum
from gclib.fs_helpers import u32, u16, u8

class ImageFormat(u8, Enum):
  I4     = 0x0
  I8     = 0x1
  IA4    = 0x2
  IA8    = 0x3
  RGB565 = 0x4
  RGB5A3 = 0x5
  RGBA32 = 0x6
  C4     = 0x8
  C8     = 0x9
  C14X2  = 0xA
  CMPR   = 0xE

class PaletteFormat(Enum):
  IA8    = 0
  RGB565 = 1
  RGB5A3 = 2

class WrapMode(Enum):
  ClampToEdge    = 0
  Repeat         = 1
  MirroredRepeat = 2

class FilterMode(Enum):
  Nearest              = 0
  Linear               = 1
  NearestMipmapNearest = 2
  NearestMipmapLinear  = 3
  LinearMipmapNearest  = 4
  LinearMipmapLinear   = 5

class Attr(u32, Enum):
  PositionMatrixIndex   = 0x00
  Tex0MatrixIndex       = 0x01
  Tex1MatrixIndex       = 0x02
  Tex2MatrixIndex       = 0x03
  Tex3MatrixIndex       = 0x04
  Tex4MatrixIndex       = 0x05
  Tex5MatrixIndex       = 0x06
  Tex6MatrixIndex       = 0x07
  Tex7MatrixIndex       = 0x08
  Position              = 0x09
  Normal                = 0x0A
  Color0                = 0x0B
  Color1                = 0x0C
  Tex0                  = 0x0D
  Tex1                  = 0x0E
  Tex2                  = 0x0F
  Tex3                  = 0x10
  Tex4                  = 0x11
  Tex5                  = 0x12
  Tex6                  = 0x13
  Tex7                  = 0x14
  PositionMatrixArray   = 0x15
  NormalMatrixArray     = 0x16
  TextureMatrixArray    = 0x17
  LitMatrixArray        = 0x18
  NormalBinormalTangent = 0x19
  NULL                  = 0xFF

class ComponentCount(u32, Enum):
  Position_XY  = 0x00
  Position_XYZ = 0x01

  Normal_XYZ  = 0x00
  Normal_NBT  = 0x01
  Normal_NBT3 = 0x02

  Color_RGB  = 0x00
  Color_RGBA = 0x01

  TexCoord_S  = 0x00
  TexCoord_ST = 0x01

class ComponentType(u32, Enum):
  Unsigned8  = 0x00
  Signed8    = 0x01
  Unsigned16 = 0x02
  Signed16   = 0x03
  Float32    = 0x04
  
  RGB565 = 0x00
  RGB8   = 0x01
  RGBX8  = 0x02
  RGBA4  = 0x03
  RGBA6  = 0x04
  RGBA8  = 0x05

class PixelEngineMode(u8, Enum):
  Opaque      = 0x01
  Alpha_Test  = 0x02
  Translucent = 0x04

class CullMode(u32, Enum):
  Cull_None  = 0x00
  Cull_Front = 0x01
  Cull_Back  = 0x02
  Cull_All   = 0x03

class CompareType(u8, Enum):
  Never         = 0
  Less          = 1
  Equal         = 2
  Less_Equal    = 3
  Greater       = 4
  Not_Equal     = 5
  Greater_Equal = 6
  Always        = 7

class AlphaOp(u8, Enum):
  AND  = 0x00
  OR   = 0x01
  XOR  = 0x02
  XNOR = 0x03

class ColorSrc(u8, Enum):
  Register = 0x00
  Vertex   = 0x01

class DiffuseFunction(u8, Enum):
  None_  = 0x00
  Signed = 0x01
  Clamp  = 0x02

class AttenuationFunction(u8, Enum):
  Specular = 0x00
  Spot     = 0x01
  None_    = 0x02

class BlendMode(u8, Enum):
  None_    = 0x00
  Blend    = 0x01
  Logic    = 0x02
  Subtract = 0x03

class BlendFactor(u8, Enum):
  Zero                      = 0x00
  One                       = 0x01
  Source_Color              = 0x02
  Inverse_Source_Color      = 0x03
  Source_Alpha              = 0x04
  Inverse_Source_Alpha      = 0x05
  Destination_Alpha         = 0x06
  Inverse_Destination_Alpha = 0x07

class LogicOp(u8, Enum):
  CLEAR   = 0x00
  AND     = 0x01
  REVAND  = 0x02
  COPY    = 0x03
  INVAND  = 0x04
  NOOP    = 0x05
  XOR     = 0x06
  OR      = 0x07
  NOR     = 0x08
  EQUIV   = 0x09
  INV     = 0x0A
  REVOR   = 0x0B
  INVCOPY = 0x0C
  INVOR   = 0x0D
  NAND    = 0x0E
  SET     = 0x0F

class TexCoordID(u8, Enum):
  TEXCOORD0     = 0x00
  TEXCOORD1     = 0x01
  TEXCOORD2     = 0x02
  TEXCOORD3     = 0x03
  TEXCOORD4     = 0x04
  TEXCOORD5     = 0x05
  TEXCOORD6     = 0x06
  TEXCOORD7     = 0x07
  TEXCOORD_NULL = 0xFF

class TexMapID(u8, Enum):
  TEXMAP0     = 0x00
  TEXMAP1     = 0x01
  TEXMAP2     = 0x02
  TEXMAP3     = 0x03
  TEXMAP4     = 0x04
  TEXMAP5     = 0x05
  TEXMAP6     = 0x06
  TEXMAP7     = 0x07
  TEXMAP_NULL = 0xFF

class IndirectTexScale(u8, Enum):
  _1   = 0x00
  _2   = 0x01
  _4   = 0x02
  _8   = 0x03
  _16  = 0x04
  _32  = 0x05
  _64  = 0x06
  _128 = 0x07
  _256 = 0x08

class IndTexStageID(u8, Enum):
  STAGE0 = 0
  STAGE1 = 1
  STAGE2 = 2
  STAGE3 = 3

class IndTexFormat(u8, Enum):
  _8 = 0 # 8-bit texture offset
  _5 = 1 # 5-bit texture offset
  _4 = 2 # 4-bit texture offset
  _3 = 3 # 3-bit texture offset

class IndTexBiasSel(u8, Enum):
  NONE = 0
  S    = 1
  T    = 2
  ST   = 3
  U    = 4
  SU   = 5
  TU   = 6
  STU  = 7

class IndTexAlphaSel(u8, Enum):
  OFF = 0
  S   = 1
  T   = 2
  U   = 3

class IndTexMtxSel(u8, Enum):
  OFF = 0
  _0  = 1
  _1  = 2
  _2  = 3
  S0  = 5
  S1  = 6
  S2  = 7
  T0  = 9
  T1  = 10
  T2  = 11

class IndTexWrap(u8, Enum):
  OFF  = 0
  _256 = 1
  _128 = 2
  _64  = 3
  _32  = 4
  _16  = 5
  _0   = 6

class ColorChannelID(u8, Enum):
  COLOR0       = 0x00
  COLOR1       = 0x01
  ALPHA0       = 0x02
  ALPHA1       = 0x03
  COLOR0A0     = 0x04
  COLOR1A1     = 0x05
  COLOR_ZERO   = 0x06
  ALPHA_BUMP   = 0x07
  ALPHA_BUMP_N = 0x08
  COLOR_NULL   = 0xFF

class CombineColor(u8, Enum):
  CPREV = 0x00 # Use the color value from previous TEV stage
  APREV = 0x01 # Use the alpha value from previous TEV stage
  C0    = 0x02 # Use the color value from the color/output register 0
  A0    = 0x03 # Use the alpha value from the color/output register 0
  C1    = 0x04 # Use the color value from the color/output register 1
  A1    = 0x05 # Use the alpha value from the color/output register 1
  C2    = 0x06 # Use the color value from the color/output register 2
  A2    = 0x07 # Use the alpha value from the color/output register 2
  TEXC  = 0x08 # Use the color value from texture
  TEXA  = 0x09 # Use the alpha value from texture
  RASC  = 0x0A # Use the color value from rasterizer
  RASA  = 0x0B # Use the alpha value from rasterizer
  ONE   = 0x0C
  HALF  = 0x0D
  KONST = 0x0E
  ZERO  = 0x0F # Use to pass zero value

class CombineAlpha(u8, Enum):
  APREV = 0x00 # Use the alpha value from previous TEV stage
  A0    = 0x01 # Use the alpha value from the color/output register 0
  A1    = 0x02 # Use the alpha value from the color/output register 1
  A2    = 0x03 # Use the alpha value from the color/output register 2
  TEXA  = 0x04 # Use the alpha value from texture
  RASA  = 0x05 # Use the alpha value from rasterizer
  KONST = 0x06
  ZERO  = 0x07 # Use to pass zero value

class TevOp(u8, Enum):
  ADD           = 0x00
  SUB           = 0x01
  COMP_R8_GT    = 0x08
  COMP_R8_EQ    = 0x09
  COMP_GR16_GT  = 0x0A
  COMP_GR16_EQ  = 0x0B
  COMP_BGR24_GT = 0x0C
  COMP_BGR24_EQ = 0x0D
  COMP_RGB8_GT  = 0x0E
  COMP_RGB8_EQ  = 0x0F
  COMP_A8_GT    = COMP_RGB8_GT
  COMP_A8_EQ    = COMP_RGB8_EQ

class TevBias(u8, Enum):
  ZERO        = 0x00
  ADDHALF     = 0x01
  SUBHALF     = 0x02
  
  # Used to denote the compare ops to the HW.
  HWB_COMPARE = 0x03

class TevScale(u8, Enum):
  SCALE_1   = 0x00
  SCALE_2   = 0x01
  SCALE_4   = 0x02
  DIVIDE_2  = 0x03

  # Used to denote the width of the compare op.
  HWB_R8    = 0x00
  HWB_GR16  = 0x01
  HWB_BGR24 = 0x02
  HWB_RGB8  = 0x03

class Register(u8, Enum):
  PREV = 0x00
  REG0 = 0x01
  REG1 = 0x02
  REG2 = 0x03

class TexGenType(u8, Enum):
  MTX3x4 = 0x00
  MTX2x4 = 0x01
  BUMP0  = 0x02
  BUMP1  = 0x03
  BUMP2  = 0x04
  BUMP3  = 0x05
  BUMP4  = 0x06
  BUMP5  = 0x07
  BUMP6  = 0x08
  BUMP7  = 0x09
  SRTG   = 0x0A

class TexGenSrc(u8, Enum):
  POS       = 0x00
  NRM       = 0x01
  BINRM     = 0x02
  TANGENT   = 0x03
  TEX0      = 0x04
  TEX1      = 0x05
  TEX2      = 0x06
  TEX3      = 0x07
  TEX4      = 0x08
  TEX5      = 0x09
  TEX6      = 0x0A
  TEX7      = 0x0B
  TEXCOORD0 = 0x0C
  TEXCOORD1 = 0x0D
  TEXCOORD2 = 0x0E
  TEXCOORD3 = 0x0F
  TEXCOORD4 = 0x10
  TEXCOORD5 = 0x11
  TEXCOORD6 = 0x12
  COLOR0    = 0x13
  COLOR1    = 0x14

class TexGenMatrix(u8, Enum):
  IDENTITY = 60
  TEXMTX0  = 30
  TEXMTX1  = 33
  TEXMTX2  = 36
  TEXMTX3  = 39
  TEXMTX4  = 42
  TEXMTX5  = 45
  TEXMTX6  = 48
  TEXMTX7  = 51
  TEXMTX8  = 54
  TEXMTX9  = 57

  # Clever games can use PNMTX as inputs to texgen.
  PNMTX0   = 0
  PNMTX1   = 3
  PNMTX2   = 6
  PNMTX3   = 9
  PNMTX4   = 12
  PNMTX5   = 15
  PNMTX6   = 18
  PNMTX7   = 21
  PNMTX8   = 24
  PNMTX9   = 27

class KonstColorSel(u8, Enum):
  _1     = 0x00 # constant 1.0
  _7_8th = 0x01 # constant 7/8
  _6_8th = 0x02 # constant 6/8
  _5_8th = 0x03 # constant 5/8
  _4_8th = 0x04 # constant 4/8
  _3_8th = 0x05 # constant 3/8
  _2_8th = 0x06 # constant 2/8
  _1_8th = 0x07 # constant 1/8
  K0     = 0x0C # K0[RGB] register
  K1     = 0x0D # K1[RGB] register
  K2     = 0x0E # K2[RGB] register
  K3     = 0x0F # K3[RGB] register
  K0_R   = 0x10 # K0[RRR] register
  K1_R   = 0x11 # K1[RRR] register
  K2_R   = 0x12 # K2[RRR] register
  K3_R   = 0x13 # K3[RRR] register
  K0_G   = 0x14 # K0[GGG] register
  K1_G   = 0x15 # K1[GGG] register
  K2_G   = 0x16 # K2[GGG] register
  K3_G   = 0x17 # K3[GGG] register
  K0_B   = 0x18 # K0[BBB] register
  K1_B   = 0x19 # K1[BBB] register
  K2_B   = 0x1A # K2[BBB] register
  K3_B   = 0x1B # K3[RBB] register
  K0_A   = 0x1C # K0[AAA] register
  K1_A   = 0x1D # K1[AAA] register
  K2_A   = 0x1E # K2[AAA] register
  K3_A   = 0x1F # K3[AAA] register

class KonstAlphaSel(u8, Enum):
  _1     = 0x00 # constant 1.0
  _7_8th = 0x01 # constant 7/8
  _6_8th = 0x02 # constant 6/8
  _5_8th = 0x03 # constant 5/8
  _4_8th = 0x04 # constant 4/8
  _3_8th = 0x05 # constant 3/8
  _2_8th = 0x06 # constant 2/8
  _1_8th = 0x07 # constant 1/8
  K0_R   = 0x10 # K0[R] register
  K1_R   = 0x11 # K1[R] register
  K2_R   = 0x12 # K2[R] register
  K3_R   = 0x13 # K3[R] register
  K0_G   = 0x14 # K0[G] register
  K1_G   = 0x15 # K1[G] register
  K2_G   = 0x16 # K2[G] register
  K3_G   = 0x17 # K3[G] register
  K0_B   = 0x18 # K0[B] register
  K1_B   = 0x19 # K1[B] register
  K2_B   = 0x1A # K2[B] register
  K3_B   = 0x1B # K3[B] register
  K0_A   = 0x1C # K0[A] register
  K1_A   = 0x1D # K1[A] register
  K2_A   = 0x1E # K2[A] register
  K3_A   = 0x1F # K3[A] register

class FogProjection(Enum):
  PERSPECTIVE  = 0x00
  ORTHOGRAPHIC = 0x01

class FogType(u8, Enum):
  OFF     = 0x00
  LINEAR  = 0x02
  EXP     = 0x04
  EXP2    = 0x05
  REVEXP  = 0x06
  REVEXP2 = 0x07

class MDLCommandType(u8, Enum):
  END_MARKER = 0x00
  XF = 0x10
  BP = 0x61

class BPRegister(u8, Enum):
  GEN_MODE = 0x00
  
  IND_MTXA0 = 0x06
  IND_MTXB0 = 0x07
  IND_MTXC0 = 0x08
  IND_MTXA1 = 0x09
  IND_MTXB1 = 0x0A
  IND_MTXC1 = 0x0B
  IND_MTXA2 = 0x0C
  IND_MTXB2 = 0x0D
  IND_MTXC2 = 0x0E
  
  IND_IMASK = 0x0F
  
  IND_CMD0 = 0x10
  IND_CMD1 = 0x11
  IND_CMD2 = 0x12
  IND_CMD3 = 0x13
  IND_CMD4 = 0x14
  IND_CMD5 = 0x15
  IND_CMD6 = 0x16
  IND_CMD7 = 0x17
  IND_CMD8 = 0x18
  IND_CMD9 = 0x19
  IND_CMDA = 0x1A
  IND_CMDB = 0x1B
  IND_CMDC = 0x1C
  IND_CMDD = 0x1D
  IND_CMDE = 0x1E
  IND_CMDF = 0x1F
  
  SCISSOR_0 = 0x20
  SCISSOR_1 = 0x21
  
  SU_LPSIZE = 0x22
  SU_COUNTER = 0x23
  RAS_COUNTER = 0x24
  
  RAS1_SS0 = 0x25
  RAS1_SS1 = 0x26
  
  RAS1_IREF = 0x27
  
  RAS1_TREF0 = 0x28
  RAS1_TREF1 = 0x29
  RAS1_TREF2 = 0x2A
  RAS1_TREF3 = 0x2B
  RAS1_TREF4 = 0x2C
  RAS1_TREF5 = 0x2D
  RAS1_TREF6 = 0x2E
  RAS1_TREF7 = 0x2F
  
  SU_SSIZE0 = 0x30
  SU_TSIZE0 = 0x31
  SU_SSIZE1 = 0x32
  SU_TSIZE1 = 0x33
  SU_SSIZE2 = 0x34
  SU_TSIZE2 = 0x35
  SU_SSIZE3 = 0x36
  SU_TSIZE3 = 0x37
  SU_SSIZE4 = 0x38
  SU_TSIZE4 = 0x39
  SU_SSIZE5 = 0x3A
  SU_TSIZE5 = 0x3B
  SU_SSIZE6 = 0x3C
  SU_TSIZE6 = 0x3D
  SU_SSIZE7 = 0x3E
  SU_TSIZE7 = 0x3F
  
  PE_ZMODE = 0x40
  PE_CMODE0 = 0x41
  PE_CMODE1 = 0x42
  PE_CONTROL = 0x43
  field_mask = 0x44
  PE_DONE = 0x45
  clock = 0x46
  PE_TOKEN = 0x47
  PE_TOKEN_INT = 0x48
  EFB_SOURCE_RECT_TOP_LEFT = 0x49
  EFB_SOURCE_RECT_WIDTH_HEIGHT = 0x4A
  XFB_TARGET_ADDRESS = 0x4B
  
  DISP_COPY_Y_SCALE = 0x4E
  PE_COPY_CLEAR_AR = 0x4F
  PE_COPY_CLEAR_GB = 0x50
  PE_COPY_CLEAR_Z = 0x51
  PE_COPY_EXECUTE = 0x52
  
  SCISSOR_BOX_OFFSET = 0x59
  
  TEX_LOADTLUT0 = 0x64
  TEX_LOADTLUT1 = 0x65
  
  TX_SETMODE0_I0 = 0x80
  TX_SETMODE0_I1 = 0x81
  TX_SETMODE0_I2 = 0x82
  TX_SETMODE0_I3 = 0x83
  TX_SETMODE1_I0 = 0x84
  TX_SETMODE1_I1 = 0x85
  TX_SETMODE1_I2 = 0x86
  TX_SETMODE1_I3 = 0x87
  
  TX_SETIMAGE0_I0 = 0x88
  TX_SETIMAGE0_I1 = 0x89
  TX_SETIMAGE0_I2 = 0x8A
  TX_SETIMAGE0_I3 = 0x8B
  TX_SETIMAGE1_I0 = 0x8C
  TX_SETIMAGE1_I1 = 0x8D
  TX_SETIMAGE1_I2 = 0x8E
  TX_SETIMAGE1_I3 = 0x8F
  TX_SETIMAGE2_I0 = 0x90
  TX_SETIMAGE2_I1 = 0x91
  TX_SETIMAGE2_I2 = 0x92
  TX_SETIMAGE2_I3 = 0x93
  TX_SETIMAGE3_I0 = 0x94
  TX_SETIMAGE3_I1 = 0x95
  TX_SETIMAGE3_I2 = 0x96
  TX_SETIMAGE3_I3 = 0x97
  
  TX_LOADTLUT0 = 0x98
  TX_LOADTLUT1 = 0x99
  TX_LOADTLUT2 = 0x9A
  TX_LOADTLUT3 = 0x9B
  
  TX_SETMODE0_I4 = 0xA0
  TX_SETMODE0_I5 = 0xA1
  TX_SETMODE0_I6 = 0xA2
  TX_SETMODE0_I7 = 0xA3
  TX_SETMODE1_I4 = 0xA4
  TX_SETMODE1_I5 = 0xA5
  TX_SETMODE1_I6 = 0xA6
  TX_SETMODE1_I7 = 0xA7
  
  TX_SETIMAGE0_I4 = 0xA8
  TX_SETIMAGE0_I5 = 0xA9
  TX_SETIMAGE0_I6 = 0xAA
  TX_SETIMAGE0_I7 = 0xAB
  TX_SETIMAGE1_I4 = 0xAC
  TX_SETIMAGE1_I5 = 0xAD
  TX_SETIMAGE1_I6 = 0xAE
  TX_SETIMAGE1_I7 = 0xAF
  TX_SETIMAGE2_I4 = 0xB0
  TX_SETIMAGE2_I5 = 0xB1
  TX_SETIMAGE2_I6 = 0xB2
  TX_SETIMAGE2_I7 = 0xB3
  TX_SETIMAGE3_I4 = 0xB4
  TX_SETIMAGE3_I5 = 0xB5
  TX_SETIMAGE3_I6 = 0xB6
  TX_SETIMAGE3_I7 = 0xB7
  
  TX_SETTLUT_I4 = 0xB8
  TX_SETTLUT_I5 = 0xB9
  TX_SETTLUT_I6 = 0xBA
  TX_SETTLUT_I7 = 0xBB
  
  TEV_COLOR_ENV_0 = 0xC0
  TEV_ALPHA_ENV_0 = 0xC1
  TEV_COLOR_ENV_1 = 0xC2
  TEV_ALPHA_ENV_1 = 0xC3
  TEV_COLOR_ENV_2 = 0xC4
  TEV_ALPHA_ENV_2 = 0xC5
  TEV_COLOR_ENV_3 = 0xC6
  TEV_ALPHA_ENV_3 = 0xC7
  TEV_COLOR_ENV_4 = 0xC8
  TEV_ALPHA_ENV_4 = 0xC9
  TEV_COLOR_ENV_5 = 0xCA
  TEV_ALPHA_ENV_5 = 0xCB
  TEV_COLOR_ENV_6 = 0xCC
  TEV_ALPHA_ENV_6 = 0xCD
  TEV_COLOR_ENV_7 = 0xCE
  TEV_ALPHA_ENV_7 = 0xCF
  TEV_COLOR_ENV_8 = 0xD0
  TEV_ALPHA_ENV_8 = 0xD1
  TEV_COLOR_ENV_9 = 0xD2
  TEV_ALPHA_ENV_9 = 0xD3
  TEV_COLOR_ENV_A = 0xD4
  TEV_ALPHA_ENV_A = 0xD5
  TEV_COLOR_ENV_B = 0xD6
  TEV_ALPHA_ENV_B = 0xD7
  TEV_COLOR_ENV_C = 0xD8
  TEV_ALPHA_ENV_C = 0xD9
  TEV_COLOR_ENV_D = 0xDA
  TEV_ALPHA_ENV_D = 0xDB
  TEV_COLOR_ENV_E = 0xDC
  TEV_ALPHA_ENV_E = 0xDD
  TEV_COLOR_ENV_F = 0xDE
  TEV_ALPHA_ENV_F = 0xDF
  
  TEV_REGISTERL_0 = 0xE0
  TEV_REGISTERH_0 = 0xE1
  TEV_REGISTERL_1 = 0xE2
  TEV_REGISTERH_1 = 0xE3
  TEV_REGISTERL_2 = 0xE4
  TEV_REGISTERH_2 = 0xE5
  TEV_REGISTERL_3 = 0xE6
  TEV_REGISTERH_3 = 0xE7
  
  FOG_RANGE = 0xE8
  FOG_RANGE_ADJ_0 = 0xE9
  FOG_RANGE_ADJ_1 = 0xEA
  FOG_RANGE_ADJ_2 = 0xEB
  FOG_RANGE_ADJ_3 = 0xEC
  FOG_RANGE_ADJ_4 = 0xED
  
  TEV_FOG_PARAM_0 = 0xEE
  TEV_FOG_PARAM_1 = 0xEF
  TEV_FOG_PARAM_2 = 0xF0
  TEV_FOG_PARAM_3 = 0xF1
  
  TEV_FOG_COLOR = 0xF2
  
  TEV_ALPHAFUNC = 0xF3
  TEV_Z_ENV_0 = 0xF4
  TEV_Z_ENV_1 = 0xF5
  
  TEV_KSEL_0 = 0xF6
  TEV_KSEL_1 = 0xF7
  TEV_KSEL_2 = 0xF8
  TEV_KSEL_3 = 0xF9
  TEV_KSEL_4 = 0xFA
  TEV_KSEL_5 = 0xFB
  TEV_KSEL_6 = 0xFC
  TEV_KSEL_7 = 0xFD
  
  BP_MASK = 0xFE

class XFRegister(u16, Enum):
  TEXMTX0 = 0x0078
  TEXMTX1 = 0x0084
  TEXMTX2 = 0x0090
  TEXMTX3 = 0x009C
  TEXMTX4 = 0x00A8
  TEXMTX5 = 0x00B4
  TEXMTX6 = 0x00C0
  TEXMTX7 = 0x00CC
  TEXMTX8 = 0x00D8
  TEXMTX9 = 0x00E4
  
  # 0x600-0x67F are 8 lights. Each is 0x10 bytes, the first 3 bytes are unused.
  LIGHT0_COLOR = 0x0603
  LIGHT0_A0 = 0x0604 # Cosine attenuation
  LIGHT0_A1 = 0x0605
  LIGHT0_A2 = 0x0606
  LIGHT0_K0 = 0x0607 # Distance attenuation
  LIGHT0_K1 = 0x0608
  LIGHT0_K2 = 0x0609
  LIGHT0_LPX = 0x060A
  LIGHT0_LPY = 0x060B
  LIGHT0_LPZ = 0x060C
  LIGHT0_DHX = 0x060D
  LIGHT0_DHY = 0x060E
  LIGHT0_DHZ = 0x060F
  
  NUMCHAN = 0x1009
  CHAN0_AMBCOLOR = 0x100A
  CHAN0_MATCOLOR = 0x100C
  CHAN0_COLOR = 0x100E
  NUMTEXGENS = 0x103F
  TEXMTXINFO = 0x1040
  POSMTXINFO = 0x1050

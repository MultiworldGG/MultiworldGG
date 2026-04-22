
from gclib import fs_helpers as fs
from gclib.jchunk import JPAChunk
from gclib.jpa_enums import JPACVersion
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import BUNFOE, bunfoe, field
from gclib.bunfoe_types import Vec2float, Vec3float, Matrix2x3, Matrix4x4, RGBAu8, RGBAs16

class SSP1(JPAChunk):
  def __new__(cls, *args, **kwargs):
    if cls != SSP1:
      return super().__new__(cls)
    data, version = args
    if version == JPACVersion.JPAC1_00:
      return SSP1_JPC100(data, version)
    elif version == JPACVersion.JPAC2_10:
      return SSP1_JPC210(data, version)
    return super().__new__(cls)

@bunfoe
class SSP1_JPC100(SSP1): # JPASweepShape
  DATA_SIZE = 0x50
  
  flags: u32
  position_random: float
  base_velocity: float
  base_velocity_random: float
  velocity_inf_rate: float
  gravity: float
  timing: float
  lifetime: s16
  rate: s16
  step: u8
  _padding_1: u24
  scale: Vec2float
  rotate_speed: float
  inherit_scale: float
  inherit_alpha: float
  inherit_rgb: float
  color_prm: RGBAu8
  color_env: RGBAu8
  texture_index: u8
  _padding_2: u24

@bunfoe
class SSP1_JPC210(SSP1): # JPAChildShape
  DATA_SIZE = 0x48
  
  flags: u32
  position_random: float
  base_velocity: float
  base_velocity_random: float
  velocity_inf_rate: float
  gravity: float
  scale: Vec2float
  inherit_scale: float
  inherit_alpha: float
  inherit_rgb: float
  color_prm: RGBAu8
  color_env: RGBAu8
  timing: float
  lifetime: s16
  rate: s16
  step: u8
  texture_index: u8
  rotate_speed: s16

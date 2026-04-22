
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr
from gclib.bunfoe import bunfoe, field, BUNFOE

class Vector(BUNFOE):
  pass

class Vector2(Vector):
  @property
  def xy(self):
    return (self.x, self.y)
  
  @xy.setter
  def xy(self, value):
    self.x, self.y = value

class Vector3(Vector):
  @property
  def xyz(self):
    return (self.x, self.y, self.z)
  
  @xyz.setter
  def xyz(self, value):
    self.x, self.y, self.z = value

@bunfoe
class Vec2float(Vector2):
  x: float = 0.0
  y: float = 0.0

@bunfoe
class Vec3float(Vector3):
  x: float = 0.0
  y: float = 0.0
  z: float = 0.0

@bunfoe
class Vec3u16Rot(Vector3):
  x: u16Rot = 0
  y: u16Rot = 0
  z: u16Rot = 0

class Matrix(BUNFOE):
  pass

@bunfoe
class Matrix2x3(Matrix):
  r0: list[float] =  field(length=3, default_factory=lambda: [0.5, 0.0, 0.0])
  r1: list[float] =  field(length=3, default_factory=lambda: [0.0, 0.5, 0.0])

@bunfoe
class Matrix4x4(Matrix):
  r0: list[float] = field(length=4, default_factory=lambda: [1.0, 0.0, 0.0, 0.0])
  r1: list[float] = field(length=4, default_factory=lambda: [0.0, 1.0, 0.0, 0.0])
  r2: list[float] = field(length=4, default_factory=lambda: [0.0, 0.0, 1.0, 0.0])
  r3: list[float] = field(length=4, default_factory=lambda: [0.0, 0.0, 0.0, 1.0])

class RGB(BUNFOE):
  @property
  def rgb(self):
    return (self.r, self.g, self.b)
  
  @rgb.setter
  def rgb(self, value):
    self.r, self.g, self.b = value

class RGBA(RGB):
  @property
  def rgba(self):
    return (self.r, self.g, self.b, self.a)
  
  @rgba.setter
  def rgba(self, value):
    self.r, self.g, self.b, self.a = value

@bunfoe
class RGBu8(RGBA):
  r: u8 = 0
  g: u8 = 0
  b: u8 = 0

@bunfoe
class RGBAu8(RGBA):
  r: u8 = 0
  g: u8 = 0
  b: u8 = 0
  a: u8 = 0

@bunfoe
class RGBAs16(RGBA):
  r: s16 = 0
  g: s16 = 0
  b: s16 = 0
  a: s16 = 0

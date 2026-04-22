
from gclib import fs_helpers as fs
from gclib.fs_helpers import u32, u24, u16, u8, s32, s16, s8, u16Rot, FixedStr, MagicStr, Bool255isFalse
from gclib.jchunk import JChunk
from gclib.bunfoe import bunfoe, field, BUNFOE
from gclib.bunfoe_types import Vec3float, Vec3u16Rot

@bunfoe
class Joint(BUNFOE):
  DATA_SIZE = 0x40
  
  matrix_type           : u16            = 0
  no_inherit_scale      : Bool255isFalse = False
  _padding_1            : u8             = 0xFF
  scale                 : Vec3float      = field(default_factory=Vec3float)
  rotation              : Vec3u16Rot     = field(default_factory=Vec3u16Rot)
  _padding_2            : u16            = 0xFFFF
  translation           : Vec3float      = field(default_factory=Vec3float)
  bounding_sphere_radius: float          = 0.0
  bounding_box_min      : Vec3float      = field(default_factory=Vec3float)
  bounding_box_max      : Vec3float      = field(default_factory=Vec3float)

class JNT1(JChunk):
  def read_chunk_specific_data(self):
    self.joint_count = fs.read_u16(self.data, 0x08)
    self.joint_data_offset = fs.read_u32(self.data, 0x0C)
    self.string_table_offset = fs.read_u32(self.data, 0x14)
    
    offset = self.joint_data_offset
    self.joints = []
    for joint_index in range(self.joint_count):
      joint = Joint(self.data)
      joint.read(offset)
      self.joints.append(joint)
      offset += Joint.DATA_SIZE
    
    self.joint_names = self.read_string_table(self.string_table_offset)
    self.joints_by_name = {}
    for joint_index, joint in enumerate(self.joints):
      joint_name = self.joint_names[joint_index]
      self.joints_by_name[joint_name] = joint
  
  def save_chunk_specific_data(self):
    offset = self.joint_data_offset
    for joint in self.joints:
      joint.save(offset)
      offset += Joint.DATA_SIZE

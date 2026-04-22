
from gclib import fs_helpers as fs
from gclib.jchunk import JPAChunk
from gclib.jpa_enums import JPACVersion

class ColorAnimationKeyframe:
  def __init__(self, time, color):
    self.time = time
    self.color = color

class BSP1(JPAChunk):
  def read_chunk_specific_data(self):
    if self.version == JPACVersion.JPAC1_00:
      self.read_chunk_specific_data_jpc100()
    elif self.version == JPACVersion.JPAC2_10:
      self.read_chunk_specific_data_jpc210()
  
  def save_chunk_specific_data(self):
    if self.version == JPACVersion.JPAC1_00:
      self.save_chunk_specific_data_jpc100()
    elif self.version == JPACVersion.JPAC2_10:
      self.save_chunk_specific_data_jpc210()
    
  def read_chunk_specific_data_jpc100(self):
    self.color_flags = fs.read_u8(self.data, 0xC + 0x1B)
    
    r = fs.read_u8(self.data, 0xC + 0x20)
    g = fs.read_u8(self.data, 0xC + 0x21)
    b = fs.read_u8(self.data, 0xC + 0x22)
    a = fs.read_u8(self.data, 0xC + 0x23)
    self.color_prm = (r, g, b, a)
    r = fs.read_u8(self.data, 0xC + 0x24)
    g = fs.read_u8(self.data, 0xC + 0x25)
    b = fs.read_u8(self.data, 0xC + 0x26)
    a = fs.read_u8(self.data, 0xC + 0x27)
    self.color_env = (r, g, b, a)
    
    self.color_prm_anm_data_count = 0
    self.color_prm_anm_table = []
    if self.color_flags & 0x02 != 0:
      self.color_prm_anm_data_offset = fs.read_u16(self.data, 0xC + 0x4)
      self.color_prm_anm_data_count = fs.read_u8(self.data, 0xC + 0x1C)
      self.color_prm_anm_table = self.read_color_table(self.color_prm_anm_data_offset, self.color_prm_anm_data_count)
    
    self.color_env_anm_data_count = 0
    self.color_env_anm_table = []
    if self.color_flags & 0x08 != 0:
      self.color_env_anm_data_offset = fs.read_u16(self.data, 0xC + 0x6)
      self.color_env_anm_data_count = fs.read_u8(self.data, 0xC + 0x1D)
      self.color_env_anm_table = self.read_color_table(self.color_env_anm_data_offset, self.color_env_anm_data_count)
  
  def read_chunk_specific_data_jpc210(self):
    self.color_flags = fs.read_u8(self.data, 0x21)
    
    r = fs.read_u8(self.data, 0x26)
    g = fs.read_u8(self.data, 0x27)
    b = fs.read_u8(self.data, 0x28)
    a = fs.read_u8(self.data, 0x29)
    self.color_prm = (r, g, b, a)
    r = fs.read_u8(self.data, 0x2A)
    g = fs.read_u8(self.data, 0x2B)
    b = fs.read_u8(self.data, 0x2C)
    a = fs.read_u8(self.data, 0x2D)
    self.color_env = (r, g, b, a)
    
    self.color_prm_anm_data_count = 0
    self.color_prm_anm_table = []
    if self.color_flags & 0x02 != 0:
      self.color_prm_anm_data_offset = fs.read_u16(self.data, 0xC)
      self.color_prm_anm_data_count = fs.read_u8(self.data, 0x22)
      self.color_prm_anm_table = self.read_color_table(self.color_prm_anm_data_offset, self.color_prm_anm_data_count)
    
    self.color_env_anm_data_count = 0
    self.color_env_anm_table = []
    if self.color_flags & 0x08 != 0:
      self.color_env_anm_data_offset = fs.read_u16(self.data, 0xE)
      self.color_env_anm_data_count = fs.read_u8(self.data, 0x23)
      self.color_env_anm_table = self.read_color_table(self.color_env_anm_data_offset, self.color_env_anm_data_count)
  
  def save_chunk_specific_data_jpc100(self):
    fs.write_u8(self.data, 0xC + 0x1B, self.color_flags)
    
    r, g, b, a = self.color_prm
    fs.write_u8(self.data, 0xC + 0x20, r)
    fs.write_u8(self.data, 0xC + 0x21, g)
    fs.write_u8(self.data, 0xC + 0x22, b)
    fs.write_u8(self.data, 0xC + 0x23, a)
    r, g, b, a = self.color_env
    fs.write_u8(self.data, 0xC + 0x24, r)
    fs.write_u8(self.data, 0xC + 0x25, g)
    fs.write_u8(self.data, 0xC + 0x26, b)
    fs.write_u8(self.data, 0xC + 0x27, a)
    
    if self.color_flags & 0x02 != 0:
      # Changing size not implemented.
      assert len(self.color_prm_anm_table) == self.color_prm_anm_data_count
      self.save_color_table(self.color_prm_anm_table, self.color_prm_anm_data_offset)
    
    if self.color_flags & 0x08 != 0:
      # Changing size not implemented.
      assert len(self.color_env_anm_table) == self.color_env_anm_data_count
      self.save_color_table(self.color_env_anm_table, self.color_env_anm_data_offset)
  
  def save_chunk_specific_data_jpc210(self):
    fs.write_u8(self.data, 0x21, self.color_flags)
    
    r, g, b, a = self.color_prm
    fs.write_u8(self.data, 0x26, r)
    fs.write_u8(self.data, 0x27, g)
    fs.write_u8(self.data, 0x28, b)
    fs.write_u8(self.data, 0x29, a)
    r, g, b, a = self.color_env
    fs.write_u8(self.data, 0x2A, r)
    fs.write_u8(self.data, 0x2B, g)
    fs.write_u8(self.data, 0x2C, b)
    fs.write_u8(self.data, 0x2D, a)
    
    if self.color_flags & 0x02 != 0:
      # Changing size not implemented.
      assert len(self.color_prm_anm_table) == self.color_prm_anm_data_count
      self.save_color_table(self.color_prm_anm_table, self.color_prm_anm_data_offset)
    
    if self.color_flags & 0x08 != 0:
      # Changing size not implemented.
      assert len(self.color_env_anm_table) == self.color_env_anm_data_count
      self.save_color_table(self.color_env_anm_table, self.color_env_anm_data_offset)
  
  def read_color_table(self, color_data_offset, color_data_count):
    color_table = []
    for i in range(color_data_count):
      keyframe_time = fs.read_u16(self.data, color_data_offset+i*6 + 0)
      r = fs.read_u8(self.data, color_data_offset+i*6 + 2)
      g = fs.read_u8(self.data, color_data_offset+i*6 + 3)
      b = fs.read_u8(self.data, color_data_offset+i*6 + 4)
      a = fs.read_u8(self.data, color_data_offset+i*6 + 5)
      color_table.append(ColorAnimationKeyframe(keyframe_time, (r, g, b, a)))
    
    return color_table
  
  def save_color_table(self, color_table, color_data_offset):
    for i, keyframe in enumerate(color_table):
      r, g, b, a = keyframe.color
      fs.write_u16(self.data, color_data_offset+i*6 + 0, keyframe.time)
      fs.write_u8(self.data, color_data_offset+i*6 + 2, r)
      fs.write_u8(self.data, color_data_offset+i*6 + 3, g)
      fs.write_u8(self.data, color_data_offset+i*6 + 4, b)
      fs.write_u8(self.data, color_data_offset+i*6 + 5, a)

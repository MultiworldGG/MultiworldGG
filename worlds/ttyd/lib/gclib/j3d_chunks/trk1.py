
from gclib import fs_helpers as fs
from gclib.jchunk import JChunk
from gclib.animation import Animation, AnimationTrack, LoopMode

class ColorAnimation(Animation):
  DATA_SIZE = 4*AnimationTrack.DATA_SIZE + 4
  
  def read(self, data, offset, r_track_data, g_track_data, b_track_data, a_track_data):
    offset = self.read_track("r", data, offset, r_track_data)
    offset = self.read_track("g", data, offset, g_track_data)
    offset = self.read_track("b", data, offset, b_track_data)
    offset = self.read_track("a", data, offset, a_track_data)
    
    self.color_id = fs.read_u8(data, offset)
    offset += 4
  
  def save(self, data, offset, r_track_data, g_track_data, b_track_data, a_track_data):
    offset = self.save_track("r", data, offset, r_track_data)
    offset = self.save_track("g", data, offset, g_track_data)
    offset = self.save_track("b", data, offset, b_track_data)
    offset = self.save_track("a", data, offset, a_track_data)
    
    fs.write_u8(data, offset, self.color_id)
    fs.write_u8(data, offset+1, 0xFF)
    fs.write_u8(data, offset+2, 0xFF)
    fs.write_u8(data, offset+3, 0xFF)
    offset += 4

class TRK1(JChunk):
  def read_chunk_specific_data(self):
    assert fs.read_str(self.data, 0, 4) == "TRK1"
    
    self.loop_mode = LoopMode(fs.read_u8(self.data, 0x08))
    assert fs.read_u8(self.data, 0x09) == 0xFF
    self.duration = fs.read_u16(self.data, 0x0A)
    
    reg_color_anims_count = fs.read_u16(self.data, 0x0C)
    konst_color_anims_count = fs.read_u16(self.data, 0x0E)
    
    reg_r_count = fs.read_u16(self.data, 0x10)
    reg_g_count = fs.read_u16(self.data, 0x12)
    reg_b_count = fs.read_u16(self.data, 0x14)
    reg_a_count = fs.read_u16(self.data, 0x16)
    konst_r_count = fs.read_u16(self.data, 0x18)
    konst_g_count = fs.read_u16(self.data, 0x1A)
    konst_b_count = fs.read_u16(self.data, 0x1C)
    konst_a_count = fs.read_u16(self.data, 0x1E)
    
    reg_color_anims_offset = fs.read_u32(self.data, 0x20)
    konst_color_anims_offset = fs.read_u32(self.data, 0x24)
    
    reg_remap_table_offset = fs.read_u32(self.data, 0x28)
    konst_remap_table_offset = fs.read_u32(self.data, 0x2C)
    
    reg_mat_names_table_offset = fs.read_u32(self.data, 0x30)
    konst_mat_names_table_offset = fs.read_u32(self.data, 0x34)
    
    reg_r_offset = fs.read_u32(self.data, 0x38)
    reg_g_offset = fs.read_u32(self.data, 0x3C)
    reg_b_offset = fs.read_u32(self.data, 0x40)
    reg_a_offset = fs.read_u32(self.data, 0x44)
    konst_r_offset = fs.read_u32(self.data, 0x48)
    konst_g_offset = fs.read_u32(self.data, 0x4C)
    konst_b_offset = fs.read_u32(self.data, 0x50)
    konst_a_offset = fs.read_u32(self.data, 0x54)
    
    # Ensure the remap tables are identity.
    # Actual remapping not currently supported by this implementation.
    for i in range(reg_color_anims_count):
      assert i == fs.read_u16(self.data, reg_remap_table_offset+i*2)
    for i in range(konst_color_anims_count):
      assert i == fs.read_u16(self.data, konst_remap_table_offset+i*2)
    
    reg_mat_names = self.read_string_table(reg_mat_names_table_offset)
    konst_mat_names = self.read_string_table(konst_mat_names_table_offset)
    
    reg_r_track_data = []
    for i in range(reg_r_count):
      r = fs.read_s16(self.data, reg_r_offset+i*2)
      reg_r_track_data.append(r)
    reg_g_track_data = []
    for i in range(reg_g_count):
      g = fs.read_s16(self.data, reg_g_offset+i*2)
      reg_g_track_data.append(g)
    reg_b_track_data = []
    for i in range(reg_b_count):
      b = fs.read_s16(self.data, reg_b_offset+i*2)
      reg_b_track_data.append(b)
    reg_a_track_data = []
    for i in range(reg_a_count):
      a = fs.read_s16(self.data, reg_a_offset+i*2)
      reg_a_track_data.append(a)
    konst_r_track_data = []
    for i in range(konst_r_count):
      r = fs.read_s16(self.data, konst_r_offset+i*2)
      konst_r_track_data.append(r)
    konst_g_track_data = []
    for i in range(konst_g_count):
      g = fs.read_s16(self.data, konst_g_offset+i*2)
      konst_g_track_data.append(g)
    konst_b_track_data = []
    for i in range(konst_b_count):
      b = fs.read_s16(self.data, konst_b_offset+i*2)
      konst_b_track_data.append(b)
    konst_a_track_data = []
    for i in range(konst_a_count):
      a = fs.read_s16(self.data, konst_a_offset+i*2)
      konst_a_track_data.append(a)
    
    reg_animations = []
    konst_animations = []
    self.mat_name_to_reg_anims: dict[str, list[ColorAnimation]] = {}
    self.mat_name_to_konst_anims: dict[str, list[ColorAnimation]] = {}
    
    offset = reg_color_anims_offset
    for i in range(reg_color_anims_count):
      anim = ColorAnimation()
      anim.read(self.data, offset, reg_r_track_data, reg_g_track_data, reg_b_track_data, reg_a_track_data)
      offset += ColorAnimation.DATA_SIZE
      
      reg_animations.append(anim)
      
      mat_name = reg_mat_names[i]
      if mat_name not in self.mat_name_to_reg_anims:
        self.mat_name_to_reg_anims[mat_name] = []
      self.mat_name_to_reg_anims[mat_name].append(anim)
    
    offset = konst_color_anims_offset
    for i in range(konst_color_anims_count):
      anim = ColorAnimation()
      anim.read(self.data, offset, konst_r_track_data, konst_g_track_data, konst_b_track_data, konst_a_track_data)
      offset += ColorAnimation.DATA_SIZE
      
      konst_animations.append(anim)
      
      mat_name = konst_mat_names[i]
      if mat_name not in self.mat_name_to_konst_anims:
        self.mat_name_to_konst_anims[mat_name] = []
      self.mat_name_to_konst_anims[mat_name].append(anim)
  
  def save_chunk_specific_data(self):
    # Cut off all the data, we're rewriting it entirely.
    self.data.truncate(0)
    
    # Placeholder for the header.
    self.data.seek(0)
    self.data.write(b"\0"*0x58)
    
    fs.align_data_to_nearest(self.data, 0x20)
    offset = self.data.tell()
    
    reg_animations: list[ColorAnimation] = []
    konst_animations: list[ColorAnimation] = []
    reg_mat_names = []
    konst_mat_names = []
    for mat_name, anims in self.mat_name_to_reg_anims.items():
      for anim in anims:
        reg_animations.append(anim)
        reg_mat_names.append(mat_name)
    for mat_name, anims in self.mat_name_to_konst_anims.items():
      for anim in anims:
        konst_animations.append(anim)
        konst_mat_names.append(mat_name)
    
    reg_r_track_data = []
    reg_g_track_data = []
    reg_b_track_data = []
    reg_a_track_data = []
    reg_color_anims_offset = offset
    if not reg_animations:
      reg_color_anims_offset = 0
    for anim in reg_animations:
      anim.save(self.data, offset, reg_r_track_data, reg_g_track_data, reg_b_track_data, reg_a_track_data)
      offset += ColorAnimation.DATA_SIZE
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    
    konst_r_track_data = []
    konst_g_track_data = []
    konst_b_track_data = []
    konst_a_track_data = []
    konst_color_anims_offset = offset
    if not konst_animations:
      konst_color_anims_offset = 0
    for anim in konst_animations:
      anim.save(self.data, offset, konst_r_track_data, konst_g_track_data, konst_b_track_data, konst_a_track_data)
      offset += ColorAnimation.DATA_SIZE
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    reg_r_offset = offset
    if not reg_r_track_data:
      reg_r_offset = 0
    for r in reg_r_track_data:
      fs.write_s16(self.data, offset, r)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    reg_g_offset = offset
    if not reg_g_track_data:
      reg_g_offset = 0
    for g in reg_g_track_data:
      fs.write_s16(self.data, offset, g)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    reg_b_offset = offset
    if not reg_b_track_data:
      reg_b_offset = 0
    for b in reg_b_track_data:
      fs.write_s16(self.data, offset, b)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    reg_a_offset = offset
    if not reg_a_track_data:
      reg_a_offset = 0
    for a in reg_a_track_data:
      fs.write_s16(self.data, offset, a)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    konst_r_offset = offset
    if not konst_r_track_data:
      konst_r_offset = 0
    for r in konst_r_track_data:
      fs.write_s16(self.data, offset, r)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    konst_g_offset = offset
    if not konst_g_track_data:
      konst_g_offset = 0
    for g in konst_g_track_data:
      fs.write_s16(self.data, offset, g)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    konst_b_offset = offset
    if not konst_b_track_data:
      konst_b_offset = 0
    for b in konst_b_track_data:
      fs.write_s16(self.data, offset, b)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    konst_a_offset = offset
    if not konst_a_track_data:
      konst_a_offset = 0
    for a in konst_a_track_data:
      fs.write_s16(self.data, offset, a)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    
    # Remap tables always written as identity, remapping not supported.
    reg_remap_table_offset = offset
    if not reg_animations:
      reg_remap_table_offset = 0
    for i in range(len(reg_animations)):
      fs.write_u16(self.data, offset, i)
      offset += 2
    
    konst_remap_table_offset = offset
    if not konst_animations:
      konst_remap_table_offset = 0
    for i in range(len(konst_animations)):
      fs.write_u16(self.data, offset, i)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    
    reg_mat_names_table_offset = offset
    self.write_string_table(reg_mat_names_table_offset, reg_mat_names)
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    
    konst_mat_names_table_offset = offset
    self.write_string_table(konst_mat_names_table_offset, konst_mat_names)
    
    
    # Write the header.
    fs.write_magic_str(self.data, 0, "TRK1", 4)
    
    fs.write_u8(self.data, 0x08, self.loop_mode.value)
    fs.write_u8(self.data, 0x09, 0xFF)
    fs.write_u16(self.data, 0x0A, self.duration)
    
    fs.write_u16(self.data, 0x0C, len(reg_animations))
    fs.write_u16(self.data, 0x0E, len(konst_animations))
    
    fs.write_s16(self.data, 0x10, len(reg_r_track_data))
    fs.write_s16(self.data, 0x12, len(reg_g_track_data))
    fs.write_s16(self.data, 0x14, len(reg_b_track_data))
    fs.write_s16(self.data, 0x16, len(reg_a_track_data))
    fs.write_s16(self.data, 0x18, len(konst_r_track_data))
    fs.write_s16(self.data, 0x1A, len(konst_g_track_data))
    fs.write_s16(self.data, 0x1C, len(konst_b_track_data))
    fs.write_s16(self.data, 0x1E, len(konst_a_track_data))
    
    fs.write_u32(self.data, 0x20, reg_color_anims_offset)
    fs.write_u32(self.data, 0x24, konst_color_anims_offset)
    
    fs.write_u32(self.data, 0x28, reg_remap_table_offset)
    fs.write_u32(self.data, 0x2C, konst_remap_table_offset)
    
    fs.write_u32(self.data, 0x30, reg_mat_names_table_offset)
    fs.write_u32(self.data, 0x34, konst_mat_names_table_offset)
    
    fs.write_u32(self.data, 0x38, reg_r_offset)
    fs.write_u32(self.data, 0x3C, reg_g_offset)
    fs.write_u32(self.data, 0x40, reg_b_offset)
    fs.write_u32(self.data, 0x44, reg_a_offset)
    fs.write_u32(self.data, 0x48, konst_r_offset)
    fs.write_u32(self.data, 0x4C, konst_g_offset)
    fs.write_u32(self.data, 0x50, konst_b_offset)
    fs.write_u32(self.data, 0x54, konst_a_offset)

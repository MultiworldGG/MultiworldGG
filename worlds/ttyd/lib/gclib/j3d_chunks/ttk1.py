from enum import Enum

from gclib import fs_helpers as fs
from gclib.jchunk import JChunk
from gclib.animation import Animation, AnimationTrack, LoopMode

class MatrixMode(Enum):
  BASIC_MODE = 0
  MAYA_MODE = 1

class UVAnimation(Animation):
  DATA_SIZE = 3*3*AnimationTrack.DATA_SIZE
  
  def read(self, data, offset, tex_gen_indexes, center_coords_data, scale_track_data, rotation_track_data, translation_track_data):
    self.tex_gen_index = tex_gen_indexes.pop(0)
    self.center_coords = center_coords_data.pop(0)
    
    offset = self.read_track("scale_s",       data, offset, scale_track_data)
    offset = self.read_track("rotation_s",    data, offset, rotation_track_data)
    offset = self.read_track("translation_s", data, offset, translation_track_data)
    offset = self.read_track("scale_t",       data, offset, scale_track_data)
    offset = self.read_track("rotation_t",    data, offset, rotation_track_data)
    offset = self.read_track("translation_t", data, offset, translation_track_data)
    offset = self.read_track("scale_q",       data, offset, scale_track_data)
    offset = self.read_track("rotation_q",    data, offset, rotation_track_data)
    offset = self.read_track("translation_q", data, offset, translation_track_data)
  
  def save(self, data, offset, tex_gen_indexes, center_coords_data, scale_track_data, rotation_track_data, translation_track_data):
    tex_gen_indexes.append(self.tex_gen_index)
    center_coords_data.append(self.center_coords)
    
    offset = self.save_track("scale_s",       data, offset, scale_track_data)
    offset = self.save_track("rotation_s",    data, offset, rotation_track_data)
    offset = self.save_track("translation_s", data, offset, translation_track_data)
    offset = self.save_track("scale_t",       data, offset, scale_track_data)
    offset = self.save_track("rotation_t",    data, offset, rotation_track_data)
    offset = self.save_track("translation_t", data, offset, translation_track_data)
    offset = self.save_track("scale_q",       data, offset, scale_track_data)
    offset = self.save_track("rotation_q",    data, offset, rotation_track_data)
    offset = self.save_track("translation_q", data, offset, translation_track_data)

class TTK1(JChunk):
  def read_chunk_specific_data(self):
    assert fs.read_str(self.data, 0, 4) == "TTK1"
    
    self.loop_mode = LoopMode(fs.read_u8(self.data, 0x08))
    self.rotation_frac = fs.read_u8(self.data, 0x09)
    self.duration = fs.read_u16(self.data, 0x0A)
    
    keyframe_count = fs.read_u16(self.data, 0x0C)
    anims_count = keyframe_count//3
    
    scale_table_count = fs.read_u16(self.data, 0x0E)
    rotation_table_count = fs.read_u16(self.data, 0x10)
    translation_table_count = fs.read_u16(self.data, 0x12)
    
    anims_offset = fs.read_u32(self.data, 0x14)
    
    remap_table_offset = fs.read_u32(self.data, 0x18)
    
    mat_names_table_offset = fs.read_u32(self.data, 0x1C)
    
    tex_gen_index_table_offset = fs.read_u32(self.data, 0x20)
    center_coord_table_offset = fs.read_u32(self.data, 0x24)
    scale_table_offset = fs.read_u32(self.data, 0x28)
    rotation_table_offset = fs.read_u32(self.data, 0x2C)
    translation_table_offset = fs.read_u32(self.data, 0x30)
    
    self.post_matrix_data = fs.read_bytes(self.data, 0x34, 0x28)
    
    if fs.read_u32(self.data, 0x5C) == 1:
      self.matrix_mode = MatrixMode.MAYA_MODE
    else:
      self.matrix_mode = MatrixMode.BASIC_MODE
    
    # Ensure the remap tables are identity.
    # Actual remapping not currently supported by this implementation.
    for i in range(anims_count):
      assert i == fs.read_u16(self.data, remap_table_offset+i*2)
    
    mat_names = self.read_string_table(mat_names_table_offset)
    
    tex_gen_indexes = []
    for i in range(anims_count):
      tex_gen_index = fs.read_u8(self.data, tex_gen_index_table_offset+i)
      tex_gen_indexes.append(tex_gen_index)
    center_coords_data = []
    for i in range(anims_count):
      center_s = fs.read_float(self.data, center_coord_table_offset+i*0xC+0)
      center_t = fs.read_float(self.data, center_coord_table_offset+i*0xC+4)
      center_q = fs.read_float(self.data, center_coord_table_offset+i*0xC+8)
      center_coords_data.append((center_s, center_t, center_q))
    scale_track_data = []
    for i in range(scale_table_count):
      scale = fs.read_float(self.data, scale_table_offset+i*4)
      scale_track_data.append(scale)
    rotation_track_data = []
    for i in range(rotation_table_count):
      rotation = fs.read_s16(self.data, rotation_table_offset+i*2)
      rotation_track_data.append(rotation)
    translation_track_data = []
    for i in range(translation_table_count):
      translation = fs.read_float(self.data, translation_table_offset+i*4)
      translation_track_data.append(translation)
    
    animations = []
    self.mat_name_to_anims = {}
    
    offset = anims_offset
    for i in range(anims_count):
      anim = UVAnimation()
      anim.read(self.data, offset, tex_gen_indexes, center_coords_data, scale_track_data, rotation_track_data, translation_track_data)
      offset += UVAnimation.DATA_SIZE
      
      animations.append(anim)
      
      mat_name = mat_names[i]
      if mat_name not in self.mat_name_to_anims:
        self.mat_name_to_anims[mat_name] = []
      self.mat_name_to_anims[mat_name].append(anim)
  
  def save_chunk_specific_data(self):
    # Cut off all the data, we're rewriting it entirely.
    self.data.truncate(0)
    
    # Placeholder for the header.
    self.data.seek(0)
    self.data.write(b"\0"*0x60)
    
    fs.align_data_to_nearest(self.data, 0x20)
    offset = self.data.tell()
    
    animations: list[UVAnimation] = []
    mat_names = []
    for mat_name, anims in self.mat_name_to_anims.items():
      for anim in anims:
        animations.append(anim)
        mat_names.append(mat_name)
    
    tex_gen_indexes = []
    center_coords_data = []
    scale_track_data = []
    rotation_track_data = []
    translation_track_data = []
    anims_offset = offset
    if not animations:
      anims_offset = 0
    for anim in animations:
      anim.save(self.data, offset, tex_gen_indexes, center_coords_data, scale_track_data, rotation_track_data, translation_track_data)
      offset += UVAnimation.DATA_SIZE
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    
    # Remap tables always written as identity, remapping not supported.
    remap_table_offset = offset
    if not animations:
      remap_table_offset = 0
    for i in range(len(animations)):
      fs.write_u16(self.data, offset, i)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    
    mat_names_table_offset = offset
    self.write_string_table(mat_names_table_offset, mat_names)
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    tex_gen_index_table_offset = offset
    if not tex_gen_indexes:
      tex_gen_index_table_offset = 0
    for tex_gen_index in tex_gen_indexes:
      fs.write_u8(self.data, offset, tex_gen_index)
      offset += 1
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    center_coord_table_offset = offset
    if not center_coords_data:
      center_coord_table_offset = 0
    for center_coords in center_coords_data:
      fs.write_float(self.data, offset+0, center_coords[0])
      fs.write_float(self.data, offset+4, center_coords[1])
      fs.write_float(self.data, offset+8, center_coords[2])
      offset += 0xC
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    scale_table_offset = offset
    if not scale_track_data:
      scale_table_offset = 0
    for scale in scale_track_data:
      fs.write_float(self.data, offset, scale)
      offset += 4
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    rotation_table_offset = offset
    if not rotation_track_data:
      rotation_table_offset = 0
    for rotation in rotation_track_data:
      fs.write_s16(self.data, offset, rotation)
      offset += 2
    
    fs.align_data_to_nearest(self.data, 4)
    offset = self.data.tell()
    translation_table_offset = offset
    if not translation_track_data:
      translation_table_offset = 0
    for translation in translation_track_data:
      fs.write_float(self.data, offset, translation)
      offset += 4
    
    
    # Write the header.
    fs.write_magic_str(self.data, 0, "TTK1", 4)
    
    fs.write_u8(self.data, 0x08, self.loop_mode.value)
    fs.write_u8(self.data, 0x09, self.rotation_frac)
    fs.write_u16(self.data, 0x0A, self.duration)
    
    fs.write_u16(self.data, 0x0C, len(animations)*3)
    
    fs.write_s16(self.data, 0x0E, len(scale_track_data))
    fs.write_s16(self.data, 0x10, len(rotation_track_data))
    fs.write_s16(self.data, 0x12, len(translation_track_data))
    
    fs.write_u32(self.data, 0x14, anims_offset)
    
    fs.write_u32(self.data, 0x18, remap_table_offset)
    
    fs.write_u32(self.data, 0x1C, mat_names_table_offset)
    
    fs.write_u32(self.data, 0x20, tex_gen_index_table_offset)
    fs.write_u32(self.data, 0x24, center_coord_table_offset)
    fs.write_u32(self.data, 0x28, scale_table_offset)
    fs.write_u32(self.data, 0x2C, rotation_table_offset)
    fs.write_u32(self.data, 0x30, translation_table_offset)
    
    assert len(self.post_matrix_data) == 0x28
    fs.write_bytes(self.data, 0x34, self.post_matrix_data)
  
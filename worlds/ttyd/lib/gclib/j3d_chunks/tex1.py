
from gclib import fs_helpers as fs
from gclib.jchunk import JChunk
from gclib.bti import BTI

class TEX1(JChunk):
  def read_chunk_specific_data(self):
    self.textures: list[BTI] = []
    self.num_textures = fs.read_u16(self.data, 8)
    self.texture_header_list_offset = fs.read_u32(self.data, 0x0C)
    for texture_index in range(self.num_textures):
      bti_header_offset = self.texture_header_list_offset + texture_index*0x20
      texture = BTI(self.data, bti_header_offset)
      self.textures.append(texture)
    
    self.string_table_offset = fs.read_u32(self.data, 0x10)
    self.texture_names = self.read_string_table(self.string_table_offset)
    self.textures_by_name: dict[str, list[BTI]] = {}
    for i, texture in enumerate(self.textures):
      texture_name = self.texture_names[i]
      if texture_name not in self.textures_by_name:
        self.textures_by_name[texture_name] = []
      self.textures_by_name[texture_name].append(texture)
  
  def save_chunk_specific_data(self):
    # Does not support adding new textures currently.
    assert len(self.textures) == self.num_textures
    
    next_available_data_offset = 0x20 + self.num_textures*0x20 # Right after the last header ends
    self.data.truncate(next_available_data_offset)
    self.data.seek(next_available_data_offset)
    
    image_data_offsets = {}
    for i, texture in enumerate(self.textures):
      filename = self.texture_names[i]
      format_and_filename = "%X_%s" % (texture.image_format.value, filename)
      if format_and_filename in image_data_offsets:
        texture.image_data_offset = image_data_offsets[format_and_filename] - texture.header_offset
        continue
      
      self.data.seek(next_available_data_offset)
      
      texture.image_data_offset = next_available_data_offset - texture.header_offset
      image_data_offsets[format_and_filename] = next_available_data_offset
      texture.image_data.seek(0)
      self.data.write(texture.image_data.read())
      fs.align_data_to_nearest(self.data, 0x20)
      next_available_data_offset = fs.data_len(self.data)
    
    palette_data_offsets = {}
    for i, texture in enumerate(self.textures):
      filename = self.texture_names[i]
      format_and_filename = "%X_%s" % (texture.palette_format.value, filename)
      if format_and_filename in palette_data_offsets:
        texture.palette_data_offset = palette_data_offsets[format_and_filename] - texture.header_offset
        continue
      
      self.data.seek(next_available_data_offset)
      
      if texture.needs_palettes():
        texture.palette_data_offset = next_available_data_offset - texture.header_offset
        palette_data_offsets[format_and_filename] = next_available_data_offset
        texture.palette_data.seek(0)
        self.data.write(texture.palette_data.read())
        fs.align_data_to_nearest(self.data, 0x20)
        next_available_data_offset = fs.data_len(self.data)
      else:
        # If the image doesn't use palettes its palette offset is just the same as the first texture's image offset.
        first_texture = self.textures[0]
        texture.palette_data_offset = first_texture.image_data_offset + first_texture.header_offset - texture.header_offset
        palette_data_offsets[format_and_filename] = first_texture.image_data_offset + first_texture.header_offset
    
    for texture in self.textures:
      texture.save_header_changes()
    
    self.string_table_offset = next_available_data_offset
    fs.write_u32(self.data, 0x10, self.string_table_offset)
    self.write_string_table(self.string_table_offset, self.texture_names)
